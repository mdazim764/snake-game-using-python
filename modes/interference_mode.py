import pygame
from src.snake_env import SnakeEnv, UP, RIGHT, DOWN, LEFT
from src.q_agent import QLearningAgent

class InterferenceEnv(SnakeEnv):
    def __init__(self, width=700, height=500, grid_size=20):
        super().__init__(width, height, grid_size, render_mode=True)
        pygame.display.set_caption("Experiment 1: Human Interference Mode (Adversarial RL)")
        self.ORANGE = (255, 165, 0)
        self.YELLOW = (255, 235, 59)
        self.CYAN = (0, 229, 255)
        
        self.sabotage_count = 0
        self.sabotage_flash_timer = 0

    def reset_experiment(self):
        self.sabotage_count = 0
        self.sabotage_flash_timer = 0
        return self.reset()

    def step_with_interference(self, action, is_sabotaged=False, fps=12):
        """AI ya Human Override action ko execute karta hai bina event queue clear kiye"""
        if is_sabotaged:
            self.sabotage_count += 1
            self.sabotage_flash_timer = 5  # 5 frames tak snake Orange dikhega

        old_dist = abs(self.head[0] - self.food[0]) + abs(self.head[1] - self.food[1])

        # 1. Update Direction (0: Straight, 1: Right Turn, 2: Left Turn)
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

        # 3. Check Collision
        reward = 0
        done = False
        if self.is_collision() or self.steps_without_food > 100 * len(self.snake_body):
            done = True
            reward = -100
            self.snake_body.pop()
            return self.get_state(), reward, done, self.score

        # 4. Check Food
        if self.head == self.food:
            self.score += 1
            reward = 50
            self.steps_without_food = 0
            self._spawn_food()
        else:
            self.snake_body.pop()
            new_dist = abs(self.head[0] - self.food[0]) + abs(self.head[1] - self.food[1])
            reward = 1 if new_dist < old_dist else -1.5

        # 5. Render Custom UI
        self.render_interference_ui(fps)
        return self.get_state(), reward, done, self.score

    def render_interference_ui(self, fps):
        self.window.fill(self.BLACK)

        # Grid lines
        for x in range(0, self.width, self.grid_size):
            pygame.draw.line(self.window, self.GRAY, (x, 0), (x, self.height))
        for y in range(0, self.height, self.grid_size):
            pygame.draw.line(self.window, self.GRAY, (0, y), (self.width, y))

        # Draw Snake (Flash Orange/Yellow when Human Sabotages!)
        for idx, block in enumerate(self.snake_body):
            if self.sabotage_flash_timer > 0:
                color = self.YELLOW if idx == 0 else self.ORANGE
            else:
                color = self.GREEN if idx == 0 else self.DARK_GREEN

            pygame.draw.rect(
                self.window, color,
                pygame.Rect(block[0], block[1], self.grid_size - 1, self.grid_size - 1)
            )

        if self.sabotage_flash_timer > 0:
            self.sabotage_flash_timer -= 1

        # Draw Food
        pygame.draw.rect(
            self.window, self.RED,
            pygame.Rect(self.food[0], self.food[1], self.grid_size - 1, self.grid_size - 1)
        )

        # Top HUD
        hud_text = f"Score: {self.score} | Sabotages Survived: {self.sabotage_count} | Speed: {fps} FPS"
        self.window.blit(self.font.render(hud_text, True, self.WHITE), (10, 8))

        # Sabotage Alert Banner
        if self.sabotage_flash_timer > 0:
            alert_surf = self.font.render("⚡ HUMAN INTERFERENCE! AI RECOVERING...", True, self.YELLOW)
            self.window.blit(alert_surf, (10, 40))
        else:
            help_font = pygame.font.SysFont("consolas", 16)
            help_surf = help_font.render("Controls: [Arrow Keys] Sabotage AI | [F/S] Faster/Slower | [R] Reset", True, self.CYAN)
            self.window.blit(help_surf, (10, self.height - 25))

        pygame.display.flip()
        self.clock.tick(fps)


def direction_to_relative_action(current_dir, target_dir):
    """
    Human ki arrow key (UP, RIGHT, DOWN, LEFT) ko relative action (0, 1, 2) me badalta hai.
    Note: 180-degree opposite turn ignore karega kyunki wo instant suicide hota hai.
    """
    if target_dir == current_dir:
        return 0  # Straight
    elif target_dir == (current_dir + 1) % 4:
        return 1  # Right Turn
    elif target_dir == (current_dir - 1) % 4:
        return 2  # Left Turn
    else:
        return None  # Ignore 180-degree instant self-neck hit


def run_interference_experiment():
    env = InterferenceEnv()
    agent = QLearningAgent()

    if not agent.load_model("q_table.pkl"):
        print("[ERROR] 'q_table.pkl' nahi mila! Pehle 'python train.py' run karo.")
        return

    fps = 12  
    episode = 1
    lives = 3  # 🔥 3 Lives add kar di

    # 🔥 Ab loop tab tak chalega jab tak lives > 0 hain
    while lives > 0:
        state = env.reset_experiment()
        done = False
        print(f"\n--- Starting Interference Episode {episode} | Lives Left: {lives} ---")

        while not done:
            human_target_dir = None

            # 1. Listen for Human Keyboard Sabotage
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: human_target_dir = UP
                    elif event.key == pygame.K_RIGHT: human_target_dir = RIGHT
                    elif event.key == pygame.K_DOWN: human_target_dir = DOWN
                    elif event.key == pygame.K_LEFT: human_target_dir = LEFT
                    elif event.key == pygame.K_f: fps = min(60, fps + 3)
                    elif event.key == pygame.K_s: fps = max(5, fps - 3)
                    elif event.key == pygame.K_r: done = True

            # 2. Decide Action: AI Policy vs Human Override
            ai_action = agent.get_action(state, train_mode=False)
            final_action = ai_action
            is_sabotaged = False

            if human_target_dir is not None:
                rel_action = direction_to_relative_action(env.direction, human_target_dir)
                if rel_action is not None:
                    final_action = rel_action
                    is_sabotaged = True

            # 3. Step Environment
            next_state, reward, done, score = env.step_with_interference(
                final_action, is_sabotaged=is_sabotaged, fps=fps
            )
            agent.learn(state, final_action, reward, next_state, done)
            state = next_state
            
            # 🔥 HUD ke top-right corner par LIVES dikhane ke liye
            lives_surf = env.font.render(f"LIVES: {lives}", True, env.RED)
            env.window.blit(lives_surf, (env.width - 120, 8))
            pygame.display.flip()

        print(f"Episode {episode} Over | Score: {score} | Sabotages Survived: {env.sabotage_count}")
        episode += 1
        lives -= 1  # 🔥 Game over hone par ek life minus kar di

    # --- 🔥 GAME OVER SCREEN 🔥 ---
    env.window.fill(env.BLACK)
    go_font = pygame.font.SysFont("consolas", 40, bold=True)
    txt1 = go_font.render("GAME OVER! NO LIVES LEFT.", True, env.RED)
    txt2 = env.font.render("Press any key to Exit...", True, env.GRAY)
    
    env.window.blit(txt1, (env.width//2 - txt1.get_width()//2, env.height//2 - 30))
    env.window.blit(txt2, (env.width//2 - txt2.get_width()//2, env.height//2 + 20))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False
    pygame.quit()

if __name__ == "__main__":
    run_interference_experiment()