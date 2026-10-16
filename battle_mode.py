import pygame
import random
from q_agent import QLearningAgent

# Directions
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class BattleArena:
    def __init__(self, width=800, height=600, grid_size=20):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        
        # Colors
        self.BLACK = (15, 15, 20)
        self.GRAY = (40, 40, 50)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 230, 118)      # AI Snake
        self.DARK_GREEN = (0, 150, 70)
        self.CYAN = (0, 229, 255)       # Human Snake
        self.DARK_CYAN = (0, 120, 140)
        self.RED = (255, 60, 60)        # Food
        self.YELLOW = (255, 235, 59)

        # Ensure pygame and display are initialized safely
        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Grand Battle: Human (Cyan) vs AI Agent (Green)")
        self.font = pygame.font.SysFont("consolas", 24, bold=True)
        self.large_font = pygame.font.SysFont("consolas", 45, bold=True)
        self.clock = pygame.time.Clock()

    def reset_battle(self):
        # AI Snake (Left side)
        ai_x, ai_y = 200, 200
        self.ai_body = [[ai_x, ai_y], [ai_x - self.grid_size, ai_y], [ai_x - 2*self.grid_size, ai_y]]
        self.ai_dir = RIGHT
        self.ai_score = 0
        self.ai_alive = True

        # Human Snake (Right side - Direction ko RIGHT kiya taaki piche apni body me na ghuse)
        hum_x, hum_y = 600, 400
        self.hum_body = [[hum_x, hum_y], [hum_x - self.grid_size, hum_y], [hum_x - 2*self.grid_size, hum_y]]
        self.hum_dir = RIGHT
        self.hum_score = 0
        self.hum_alive = True

        self._spawn_food()
        self.start_ticks = pygame.time.get_ticks()

    def _spawn_food(self):
        while True:
            fx = random.randint(0, (self.width - self.grid_size) // self.grid_size) * self.grid_size
            fy = random.randint(0, (self.height - self.grid_size) // self.grid_size) * self.grid_size
            self.food = [fx, fy]
            if self.food not in self.ai_body and self.food not in self.hum_body:
                break

    def get_ai_state(self):
        hx, hy = self.ai_body[0]
        g = self.grid_size
        pt_up, pt_right, pt_down, pt_left = [hx, hy-g], [hx+g, hy], [hx, hy+g], [hx-g, hy]
        d_up, d_right, d_down, d_left = (self.ai_dir == UP), (self.ai_dir == RIGHT), (self.ai_dir == DOWN), (self.ai_dir == LEFT)

        danger_straight = (d_up and self.is_collision(pt_up)) or (d_right and self.is_collision(pt_right)) or (d_down and self.is_collision(pt_down)) or (d_left and self.is_collision(pt_left))
        danger_right = (d_up and self.is_collision(pt_right)) or (d_right and self.is_collision(pt_down)) or (d_down and self.is_collision(pt_left)) or (d_left and self.is_collision(pt_up))
        danger_left = (d_up and self.is_collision(pt_left)) or (d_right and self.is_collision(pt_up)) or (d_down and self.is_collision(pt_right)) or (d_left and self.is_collision(pt_down))

        return (
            int(danger_straight), int(danger_right), int(danger_left),
            int(d_up), int(d_right), int(d_down), int(d_left),
            int(self.food[1] < hy), int(self.food[0] > hx),
            int(self.food[1] > hy), int(self.food[0] < hx)
        )

    def is_collision(self, pt):
        if pt[0] < 0 or pt[0] >= self.width or pt[1] < 0 or pt[1] >= self.height:
            return True
        if pt in self.ai_body or pt in self.hum_body:
            return True
        return False

    def run_match(self):
        agent = QLearningAgent()
        if not agent.load_model("q_table.pkl"):
            print("[ERROR] Model file missing!")
            return

        self.reset_battle()
        
        # --- WAIT FOR FIRST HUMAN KEY PRESS ---
        waiting = True
        while waiting:
            self.window.fill(self.BLACK)
            
            # Render static arena before start
            for x in range(0, self.width, self.grid_size):
                pygame.draw.line(self.window, self.GRAY, (x, 0), (x, self.height))
            for y in range(0, self.height, self.grid_size):
                pygame.draw.line(self.window, self.GRAY, (0, y), (self.width, y))

            for idx, pt in enumerate(self.ai_body):
                col = self.GREEN if idx == 0 else self.DARK_GREEN
                pygame.draw.rect(self.window, col, pygame.Rect(pt[0], pt[1], self.grid_size-1, self.grid_size-1))
            for idx, pt in enumerate(self.hum_body):
                col = self.CYAN if idx == 0 else self.DARK_CYAN
                pygame.draw.rect(self.window, col, pygame.Rect(pt[0], pt[1], self.grid_size-1, self.grid_size-1))
            pygame.draw.rect(self.window, self.RED, pygame.Rect(self.food[0], self.food[1], self.grid_size-1, self.grid_size-1))

            # Display prompt message
            prompt_surf = self.large_font.render("PRESS ANY ARROW KEY TO START", True, self.YELLOW)
            sub_surf = self.font.render("Human (Cyan) vs AI (Green)", True, self.WHITE)
            self.window.blit(prompt_surf, (self.width//2 - prompt_surf.get_width()//2, 220))
            self.window.blit(sub_surf, (self.width//2 - sub_surf.get_width()//2, 290))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        if event.key == pygame.K_UP: self.hum_dir = UP
                        elif event.key == pygame.K_DOWN: self.hum_dir = DOWN
                        elif event.key == pygame.K_LEFT: self.hum_dir = LEFT
                        elif event.key == pygame.K_RIGHT: self.hum_dir = RIGHT
                        waiting = False

        # Reset timer exact jab game start ho
        self.start_ticks = pygame.time.get_ticks()
        match_duration = 60  # 60 Seconds Match
        running = True

        while running:
            seconds_passed = (pygame.time.get_ticks() - self.start_ticks) // 1000
            time_left = max(0, match_duration - seconds_passed)

            if time_left == 0 or (not self.ai_alive and not self.hum_alive):
                running = False
                break

            # Human Keyboard Input Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.hum_dir != DOWN:
                        self.hum_dir = UP
                    elif event.key == pygame.K_DOWN and self.hum_dir != UP:
                        self.hum_dir = DOWN
                    elif event.key == pygame.K_RIGHT and self.hum_dir != LEFT:
                        self.hum_dir = RIGHT
                    elif event.key == pygame.K_LEFT and self.hum_dir != RIGHT:
                        self.hum_dir = LEFT

            # AI Move Calculation
            if self.ai_alive:
                ai_state = self.get_ai_state()
                ai_action = agent.get_action(ai_state, train_mode=False)
                if ai_action == 1:
                    self.ai_dir = (self.ai_dir + 1) % 4
                elif ai_action == 2:
                    self.ai_dir = (self.ai_dir - 1) % 4

                ai_head = list(self.ai_body[0])
                if self.ai_dir == UP: ai_head[1] -= self.grid_size
                elif self.ai_dir == RIGHT: ai_head[0] += self.grid_size
                elif self.ai_dir == DOWN: ai_head[1] += self.grid_size
                elif self.ai_dir == LEFT: ai_head[0] -= self.grid_size

                if self.is_collision(ai_head):
                    self.ai_alive = False
                else:
                    self.ai_body.insert(0, ai_head)
                    if ai_head == self.food:
                        self.ai_score += 1
                        self._spawn_food()
                    else:
                        self.ai_body.pop()

            # Human Move Calculation
            if self.hum_alive:
                hum_head = list(self.hum_body[0])
                if self.hum_dir == UP: 
                    hum_head[1] -= self.grid_size
                elif self.hum_dir == RIGHT: 
                    hum_head[0] += self.grid_size
                elif self.hum_dir == DOWN: 
                    hum_head[1] += self.grid_size
                elif self.hum_dir == LEFT: 
                    hum_head[0] -= self.grid_size

                if self.is_collision(hum_head):
                    self.hum_alive = False
                else:
                    self.hum_body.insert(0, hum_head)
                    if hum_head == self.food:
                        self.hum_score += 1
                        self._spawn_food()
                    else:
                        self.hum_body.pop()

            # Render Battle Arena
            self.window.fill(self.BLACK)
            for x in range(0, self.width, self.grid_size):
                pygame.draw.line(self.window, self.GRAY, (x, 0), (x, self.height))
            for y in range(0, self.height, self.grid_size):
                pygame.draw.line(self.window, self.GRAY, (0, y), (self.width, y))

            # Draw AI Snake (Green)
            for idx, pt in enumerate(self.ai_body):
                col = self.GREEN if idx == 0 else self.DARK_GREEN
                pygame.draw.rect(self.window, col, pygame.Rect(pt[0], pt[1], self.grid_size-1, self.grid_size-1))

            # Draw Human Snake (Cyan)
            for idx, pt in enumerate(self.hum_body):
                col = self.CYAN if idx == 0 else self.DARK_CYAN
                pygame.draw.rect(self.window, col, pygame.Rect(pt[0], pt[1], self.grid_size-1, self.grid_size-1))

            # Draw Food
            pygame.draw.rect(self.window, self.RED, pygame.Rect(self.food[0], self.food[1], self.grid_size-1, self.grid_size-1))

            # UI HUD
            hud = f"AI Score: {self.ai_score} | HUMAN Score: {self.hum_score} | Time Left: {time_left}s"
            self.window.blit(self.font.render(hud, True, self.WHITE), (15, 15))
            pygame.display.flip()
            self.clock.tick(10)

        self.show_winner_screen()

    def show_winner_screen(self):
        # Re-initialize display safely to prevent video system error
        self.window = pygame.display.set_mode((self.width, self.height))
        self.window.fill(self.BLACK)
        
        if self.ai_score > self.hum_score:
            msg = "🏆 WINNER: AI AGENT!"
            col = self.GREEN
        elif self.hum_score > self.ai_score:
            msg = "🏆 WINNER: HUMAN PLAYER!"
            col = self.CYAN
        else:
            msg = "🤝 IT'S A TIE MATCH!"
            col = self.YELLOW

        s1 = self.large_font.render(msg, True, col)
        s2 = self.font.render(f"Final Score -> AI: {self.ai_score} | Human: {self.hum_score}", True, self.WHITE)
        s3 = self.font.render("Press [ENTER] to Restart Match or [ESC] to Exit", True, self.GRAY)

        self.window.blit(s1, (self.width//2 - s1.get_width()//2, 200))
        self.window.blit(s2, (self.width//2 - s2.get_width()//2, 280))
        self.window.blit(s3, (self.width//2 - s3.get_width()//2, 360))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                        self.run_match()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

if __name__ == "__main__":
    arena = BattleArena()
    arena.run_match()