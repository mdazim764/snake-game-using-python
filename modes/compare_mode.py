import pygame
import os
from src.q_agent import QLearningAgent
from src.snake_env import UP, DOWN, LEFT, RIGHT

# Colors
BLACK = (15, 15, 20)
GRAY = (40, 40, 50)
WHITE = (255, 255, 255)
CYAN = (0, 200, 255)       # Normal Agent
GREEN = (0, 230, 118)      # Optimized Agent
RED = (255, 60, 60)        # Shared Food

class SharedArena:
    def __init__(self, width=800, height=600, grid_size=20):
        self.w = width
        self.h = height
        self.grid_size = grid_size
        self.food = None
        
        # Win stats
        self.normal_wins = 0
        self.opt_wins = 0
        self.ties = 0

    def reset_match(self):
        # Normal Agent (Cyan) starts from left
        self.norm_head = [200, 300]
        self.norm_body = [list(self.norm_head), [200-self.grid_size, 300], [200-2*self.grid_size, 300]]
        self.norm_dir = RIGHT
        self.norm_score = 0
        self.norm_alive = True
        
        # Optimized Agent (Green) starts from right
        self.opt_head = [600, 300]
        self.opt_body = [list(self.opt_head), [600+self.grid_size, 300], [600+2*self.grid_size, 300]]
        self.opt_dir = LEFT
        self.opt_score = 0
        self.opt_alive = True
        
        self.steps_taken = 0
        self._spawn_food()

    def _spawn_food(self):
        import random
        while True:
            fx = random.randint(0, (self.w - self.grid_size) // self.grid_size) * self.grid_size
            fy = random.randint(0, (self.h - self.grid_size) // self.grid_size) * self.grid_size
            self.food = [fx, fy]
            if self.food not in self.norm_body and self.food not in self.opt_body:
                break

    def get_state(self, head, direction, body):
        hx, hy = head
        g = self.grid_size
        pt_up, pt_right, pt_down, pt_left = [hx, hy-g], [hx+g, hy], [hx, hy+g], [hx-g, hy]
        d_up, d_right, d_down, d_left = (direction == UP), (direction == RIGHT), (direction == DOWN), (direction == LEFT)

        def is_collision(pt):
            # Check border
            if pt[0] < 0 or pt[0] >= self.w or pt[1] < 0 or pt[1] >= self.h:
                return True
            # Check self or other agent's body (Dono ek dusre ko block kar sakte hain!)
            if pt in self.norm_body or pt in self.opt_body:
                return True
            return False

        danger_straight = (d_up and is_collision(pt_up)) or (d_right and is_collision(pt_right)) or (d_down and is_collision(pt_down)) or (d_left and is_collision(pt_left))
        danger_right = (d_up and is_collision(pt_right)) or (d_right and is_collision(pt_down)) or (d_down and is_collision(pt_left)) or (d_left and is_collision(pt_up))
        danger_left = (d_up and is_collision(pt_left)) or (d_right and is_collision(pt_up)) or (d_down and is_collision(pt_right)) or (d_left and is_collision(pt_down))

        return (
            int(danger_straight), int(danger_right), int(danger_left),
            int(d_up), int(d_right), int(d_down), int(d_left),
            int(self.food[1] < hy), int(self.food[0] > hx),
            int(self.food[1] > hy), int(self.food[0] < hx)
        )

def run_comparison():
    if not os.path.exists("q_table_normal.pkl") or not os.path.exists("q_table.pkl"):
        print("[ERROR] Models missing. Please train both agents first!")
        return

    agent_norm = QLearningAgent()
    agent_norm.load_model("q_table_normal.pkl")
    
    agent_opt = QLearningAgent()
    agent_opt.load_model("q_table.pkl")

    pygame.init()
    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("MARL Experiment: Normal AI (Cyan) vs Optimized AI (Green)")
    font = pygame.font.SysFont("consolas", 20, bold=True)
    large_font = pygame.font.SysFont("consolas", 35, bold=True)
    clock = pygame.time.Clock()

    arena = SharedArena()
    match_count = 0
    max_matches = 3  # Best of 3 Tournament
    
    running = True
    while running and match_count < max_matches:
        arena.reset_match()
        match_active = True
        
        while match_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    match_active = False

            # --- NORMAL AGENT MOVE ---
            if arena.norm_alive:
                state_norm = arena.get_state(arena.norm_head, arena.norm_dir, arena.norm_body)
                action_norm = agent_norm.get_action(state_norm, train_mode=False)
                
                if action_norm == 1: arena.norm_dir = (arena.norm_dir + 1) % 4
                elif action_norm == 2: arena.norm_dir = (arena.norm_dir - 1) % 4

                if arena.norm_dir == UP: arena.norm_head[1] -= arena.grid_size
                elif arena.norm_dir == RIGHT: arena.norm_head[0] += arena.grid_size
                elif arena.norm_dir == DOWN: arena.norm_head[1] += arena.grid_size
                elif arena.norm_dir == LEFT: arena.norm_head[0] -= arena.grid_size

                # Check if it hits wall, itself, or the other agent
                if arena.get_state(arena.norm_head, arena.norm_dir, arena.norm_body)[0] == 1 and action_norm == 0:
                     arena.norm_alive = False
                elif arena.norm_head[0] < 0 or arena.norm_head[0] >= arena.w or arena.norm_head[1] < 0 or arena.norm_head[1] >= arena.h or arena.norm_head in arena.norm_body or arena.norm_head in arena.opt_body:
                     arena.norm_alive = False
                else:
                    arena.norm_body.insert(0, list(arena.norm_head))
                    if arena.norm_head == arena.food:
                        arena.norm_score += 1
                        arena._spawn_food()
                    else:
                        arena.norm_body.pop()

            # --- OPTIMIZED AGENT MOVE ---
            if arena.opt_alive:
                state_opt = arena.get_state(arena.opt_head, arena.opt_dir, arena.opt_body)
                action_opt = agent_opt.get_action(state_opt, train_mode=False)
                
                if action_opt == 1: arena.opt_dir = (arena.opt_dir + 1) % 4
                elif action_opt == 2: arena.opt_dir = (arena.opt_dir - 1) % 4

                if arena.opt_dir == UP: arena.opt_head[1] -= arena.grid_size
                elif arena.opt_dir == RIGHT: arena.opt_head[0] += arena.grid_size
                elif arena.opt_dir == DOWN: arena.opt_head[1] += arena.grid_size
                elif arena.opt_dir == LEFT: arena.opt_head[0] -= arena.grid_size

                if arena.opt_head[0] < 0 or arena.opt_head[0] >= arena.w or arena.opt_head[1] < 0 or arena.opt_head[1] >= arena.h or arena.opt_head in arena.opt_body or arena.opt_head in arena.norm_body:
                     arena.opt_alive = False
                else:
                    arena.opt_body.insert(0, list(arena.opt_head))
                    if arena.opt_head == arena.food:
                        arena.opt_score += 1
                        arena._spawn_food()
                    else:
                        arena.opt_body.pop()

            arena.steps_taken += 1
            
            # Match ends if both die or one dominates (score > 10)
            if not arena.norm_alive and not arena.opt_alive:
                match_active = False
            elif arena.norm_score >= 10:
                arena.opt_alive = False
                match_active = False
            elif arena.opt_score >= 10:
                arena.norm_alive = False
                match_active = False
            elif arena.steps_taken > 1000: # Timeout prevention
                 match_active = False

            # --- RENDER ---
            window.fill(BLACK)
            for x in range(0, arena.w, arena.grid_size):
                pygame.draw.line(window, GRAY, (x, 0), (x, arena.h))
            for y in range(0, arena.h, arena.grid_size):
                pygame.draw.line(window, GRAY, (0, y), (arena.w, y))

            if arena.norm_alive:
                for block in arena.norm_body: pygame.draw.rect(window, CYAN, (block[0], block[1], 19, 19))
            if arena.opt_alive:
                for block in arena.opt_body: pygame.draw.rect(window, GREEN, (block[0], block[1], 19, 19))
            
            pygame.draw.rect(window, RED, (arena.food[0], arena.food[1], 19, 19))

            hud = font.render(f"Match {match_count+1}/3 | Normal (Cyan): {arena.norm_score} | Opt (Green): {arena.opt_score}", True, WHITE)
            window.blit(hud, (10, 10))
            pygame.display.flip()
            clock.tick(15)

        # Post-match scoring
        if arena.norm_score > arena.opt_score: arena.normal_wins += 1
        elif arena.opt_score > arena.norm_score: arena.opt_wins += 1
        else: arena.ties += 1
        
        match_count += 1

    # --- FINAL REPORT SCREEN ---
    if running:
        window.fill(BLACK)
        report_title = large_font.render("--- FINAL MARL EXPERIMENT REPORT ---", True, WHITE)
        norm_txt = font.render(f"Normal Agent Wins: {arena.normal_wins}", True, CYAN)
        opt_txt = font.render(f"Optimized Agent Wins: {arena.opt_wins}", True, GREEN)
        ties_txt = font.render(f"Ties: {arena.ties}", True, WHITE)
        
        if arena.opt_wins > arena.normal_wins:
            conc = large_font.render("Conclusion: Optimized (Aggressive) is Better!", True, GREEN)
        elif arena.normal_wins > arena.opt_wins:
            conc = large_font.render("Conclusion: Normal (Safe) is Better!", True, CYAN)
        else:
            conc = large_font.render("Conclusion: Both strategies are evenly matched.", True, WHITE)

        window.blit(report_title, (50, 100))
        window.blit(norm_txt, (50, 200))
        window.blit(opt_txt, (50, 250))
        window.blit(ties_txt, (50, 300))
        window.blit(conc, (50, 400))
        
        exit_hint = font.render("Press any key to exit to Main Menu...", True, GRAY)
        window.blit(exit_hint, (50, 500))
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    waiting = False

    pygame.quit()

if __name__ == "__main__":
    run_comparison()