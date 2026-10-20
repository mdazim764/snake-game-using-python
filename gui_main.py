import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reinforcement Learning AI Lab - Snake Arena")

# Colors
BG_COLOR = (15, 15, 20)
BUTTON_COLOR = (40, 40, 50)
HOVER_COLOR = (0, 230, 118)
TEXT_COLOR = (255, 255, 255)

font_title = pygame.font.SysFont("consolas", 40, bold=True)
font_btn = pygame.font.SysFont("consolas", 20, bold=True)

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = BUTTON_COLOR

    def draw(self, surface):
        # Hover effect logic
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, HOVER_COLOR, self.rect, border_radius=8)
            pygame.draw.rect(surface, (255,255,255), self.rect, 2, border_radius=8) # White border
            text_surf = font_btn.render(self.text, True, (0, 0, 0)) # Black text on hover
        else:
            pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
            pygame.draw.rect(surface, (100, 100, 120), self.rect, 2, border_radius=8)
            text_surf = font_btn.render(self.text, True, TEXT_COLOR)

        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def draw_gui():
    clock = pygame.time.Clock()
    
    # Button definitions
    btn_width, btn_height = 450, 50
    start_x = (WIDTH - btn_width) // 2
    
    # Menu Options
    b1 = Button(start_x, 150, btn_width, btn_height, "1. Train & Benchmark Agent")
    b2 = Button(start_x, 220, btn_width, btn_height, "2. Human vs AI Agent (Battle Mode)")
    b3 = Button(start_x, 290, btn_width, btn_height, "3. Human Interference (Adversarial Mode)")
    b4 = Button(start_x, 360, btn_width, btn_height, "4. Normal vs Optimized AI (Coming Soon)")
    b5 = Button(start_x, 430, btn_width, btn_height, "5. Multi-Agent RL: 3 AIs (Coming Soon)")
    b6 = Button(start_x, 500, btn_width, btn_height, "6. Exit")

    buttons = [b1, b2, b3, b4, b5, b6]

    running = True
    while running:
        screen.fill(BG_COLOR)
        
        # Title
        title_surf = font_title.render("RL AGENT EXPERIMENT LAB", True, HOVER_COLOR)
        screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 50))
        
        # Subtitle
        sub_surf = font_btn.render("Select an environment to launch:", True, (150, 150, 150))
        screen.blit(sub_surf, (WIDTH//2 - sub_surf.get_width()//2, 100))

        # Draw Buttons
        for btn in buttons:
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
                
            # Handle Clicks
            if b1.is_clicked(event):
                import train
                train.train_and_benchmark()
            elif b2.is_clicked(event):
                from modes.battle_mode import BattleArena
                arena = BattleArena()
                arena.run_match()
            elif b3.is_clicked(event):
                from modes import interference_mode
                interference_mode.run_interference_experiment()
            elif b4.is_clicked(event):
                from modes import compare_mode
                compare_mode.run_comparison()
            elif b5.is_clicked(event):
                print("Feature in development...")
            elif b6.is_clicked(event):
                running = False
                pygame.quit()
                sys.exit()

        if not pygame.get_init() or not pygame.display.get_init():
            running = False
            break

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    draw_gui()