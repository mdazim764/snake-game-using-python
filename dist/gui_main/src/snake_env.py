import pygame
import random
import numpy as np

# Initialize Pygame
pygame.init()

# Directions (Clockwise order: UP -> RIGHT -> DOWN -> LEFT)
# Is order se Right turn (+1) aur Left turn (-1) calculate karna bahut aasan ho jata hai
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class SnakeEnv:
    def __init__(self, width=700, height=500, grid_size=20, render_mode=True):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.render_mode = render_mode
        
        # Colors
        self.BLACK = (15, 15, 20)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 230, 118)
        self.DARK_GREEN = (0, 150, 70)
        self.RED = (255, 60, 60)
        self.GRAY = (40, 40, 50)

        if self.render_mode:
            self.window = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("RL Snake - Benchmark Environment")
            self.font = pygame.font.SysFont("consolas", 24, bold=True)
            self.clock = pygame.time.Clock()

        self.reset()

    def reset(self):
        """Har naye episode ke start me game ko reset karta hai"""
        start_x = (self.width // 2 // self.grid_size) * self.grid_size
        start_y = (self.height // 2 // self.grid_size) * self.grid_size
        
        self.head = [start_x, start_y]
        # Starting me snake 3 blocks lamba hoga
        self.snake_body = [
            list(self.head),
            [start_x - self.grid_size, start_y],
            [start_x - (2 * self.grid_size), start_y]
        ]
        self.direction = RIGHT
        self.score = 0
        self.steps_without_food = 0
        self._spawn_food()
        
        return self.get_state()

    def _spawn_food(self):
        """Grid ke andar random jagah food place karta hai"""
        while True:
            fx = random.randint(0, (self.width - self.grid_size) // self.grid_size) * self.grid_size
            fy = random.randint(0, (self.height - self.grid_size) // self.grid_size) * self.grid_size
            self.food = [fx, fy]
            if self.food not in self.snake_body:
                break

    def is_collision(self, point=None):
        """Check karta hai ki di gayi position par wall ya snake body toh nahi hai"""
        if point is None:
            point = self.head
            
        # 1. Border Collision
        if point[0] < 0 or point[0] >= self.width or point[1] < 0 or point[1] >= self.height:
            return True
        # 2. Self Body Collision
        if point in self.snake_body[1:]:
            return True
            
        return False

    def get_state(self):
        """
        Current environment se 11-values ka state tuple banata hai Q-Table ke liye:
        [danger_straight, danger_right, danger_left,
         dir_up, dir_right, dir_down, dir_left,
         food_up, food_right, food_down, food_left]
        """
        hx, hy = self.head
        g = self.grid_size

        # Neighbouring points
        pt_up = [hx, hy - g]
        pt_right = [hx + g, hy]
        pt_down = [hx, hy + g]
        pt_left = [hx - g, hy]

        # Current direction booleans
        d_up = (self.direction == UP)
        d_right = (self.direction == RIGHT)
        d_down = (self.direction == DOWN)
        d_left = (self.direction == LEFT)

        # Danger check relative to current moving direction
        danger_straight = (
            (d_up and self.is_collision(pt_up)) or
            (d_right and self.is_collision(pt_right)) or
            (d_down and self.is_collision(pt_down)) or
            (d_left and self.is_collision(pt_left))
        )
        danger_right = (
            (d_up and self.is_collision(pt_right)) or
            (d_right and self.is_collision(pt_down)) or
            (d_down and self.is_collision(pt_left)) or
            (d_left and self.is_collision(pt_up))
        )
        danger_left = (
            (d_up and self.is_collision(pt_left)) or
            (d_right and self.is_collision(pt_up)) or
            (d_down and self.is_collision(pt_right)) or
            (d_left and self.is_collision(pt_down))
        )

        # Tuple return kar रहे hain taaki Q-table dictionary me as a key use ho sake
        state = (
            int(danger_straight),
            int(danger_right),
            int(danger_left),
            int(d_up),
            int(d_right),
            int(d_down),
            int(d_left),
            int(self.food[1] < hy),  # Food is UP
            int(self.food[0] > hx),  # Food is RIGHT
            int(self.food[1] > hy),  # Food is DOWN
            int(self.food[0] < hx)   # Food is LEFT
        )
        return state

    def step(self, action, fps=60):
        """
        AI se action (0: Straight, 1: Right Turn, 2: Left Turn) leta hai,
        game ko 1 step aage badhata hai aur (next_state, reward, done, score) return karta hai.
        """
        if self.render_mode:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        # Distance to food before moving (for shaping reward)
        old_dist = abs(self.head[0] - self.food[0]) + abs(self.head[1] - self.food[1])

        # 1. Update Direction based on action
        # 0 = Straight (no change), 1 = Right turn (+1), 2 = Left turn (-1)
        if action == 1:
            self.direction = (self.direction + 1) % 4
        elif action == 2:
            self.direction = (self.direction - 1) % 4

        # 2. Move Head
        if self.direction == UP:
            self.head[1] -= self.grid_size
        elif self.direction == RIGHT:
            self.head[0] += self.grid_size
        elif self.direction == DOWN:
            self.head[1] += self.grid_size
        elif self.direction == LEFT:
            self.head[0] -= self.grid_size

        self.snake_body.insert(0, list(self.head))
        self.steps_without_food += 1

        # 3. Check Collision or Infinite Loop
        reward = 0
        done = False
        if self.is_collision() or self.steps_without_food > 100 * len(self.snake_body):
            done = True
            reward = -100  # Heavy punishment on death
            self.snake_body.pop()
            return self.get_state(), reward, done, self.score

        # 4. Check Food Eaten
        if self.head == self.food:
            self.score += 1
            reward = 50  # Big positive reward for eating food
            self.steps_without_food = 0
            self._spawn_food()
        else:
            self.snake_body.pop()
            # Small guiding reward: +1 if moving closer to food, -1.5 if moving away
            new_dist = abs(self.head[0] - self.food[0]) + abs(self.head[1] - self.food[1])
            if new_dist < old_dist:
                reward = 1
            else:
                reward = -1.5

        # 5. Render UI
        if self.render_mode:
            self.render(fps)

        return self.get_state(), reward, done, self.score

    def render(self, fps=60, extra_text=""):
        self.window.fill(self.BLACK)
        
        # Draw subtle grid lines
        for x in range(0, self.width, self.grid_size):
            pygame.draw.line(self.window, self.GRAY, (x, 0), (x, self.height))
        for y in range(0, self.height, self.grid_size):
            pygame.draw.line(self.window, self.GRAY, (0, y), (self.width, y))

        # Draw Snake
        for idx, block in enumerate(self.snake_body):
            color = self.GREEN if idx == 0 else self.DARK_GREEN
            pygame.draw.rect(
                self.window, color, 
                pygame.Rect(block[0], block[1], self.grid_size - 1, self.grid_size - 1)
            )

        # Draw Food
        pygame.draw.rect(
            self.window, self.RED, 
            pygame.Rect(self.food[0], self.food[1], self.grid_size - 1, self.grid_size - 1)
        )

        # Draw Score & Info
        header = f"Score: {self.score}  {extra_text}"
        text_surf = self.font.render(header, True, self.WHITE)
        self.window.blit(text_surf, (10, 10))

        pygame.display.flip()
        self.clock.tick(fps)


# --- QUICK TEST BLOCK ---
# Is file ko direct run karne par ek Random Agent khelta hua dikhega
if __name__ == "__main__":
    env = SnakeEnv(render_mode=True)
    for episode in range(1, 4):
        state = env.reset()
        done = False
        while not done:
            # Random action: 0 (Straight), 1 (Right), 2 (Left)
            random_action = random.randint(0, 2)
            next_state, reward, done, score = env.step(random_action, fps=15)
        print(f"Test Episode {episode} Ended | Score: {score}")
    pygame.quit()