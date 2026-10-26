import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Agentic Snake - RL Lab")

# Updated Modern Colors
BG_COLOR = (18, 18, 24)       # Darker, cleaner background
BUTTON_COLOR = (45, 45, 60)
HOVER_COLOR = (0, 200, 150)   # Teal hover
TEXT_COLOR = (240, 240, 240)
BORDER_COLOR = (100, 100, 130)

font_title = pygame.font.SysFont("segoe ui", 42, bold=True)
font_subtitle = pygame.font.SysFont("segoe ui", 22, italic=True)
font_btn = pygame.font.SysFont("consolas", 18, bold=True)

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = BUTTON_COLOR

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, HOVER_COLOR, self.rect, border_radius=12)
            pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=12)
            text_surf = font_btn.render(self.text, True, (10, 10, 15))
        else:
            pygame.draw.rect(surface, self.color, self.rect, border_radius=12)
            pygame.draw.rect(surface, BORDER_COLOR, self.rect, 2, border_radius=12)
            text_surf = font_btn.render(self.text, True, TEXT_COLOR)

        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def draw_gui():
    global screen
    clock = pygame.time.Clock()
    
    # Button layout optimizations
    btn_width, btn_height = 460, 50
    start_x = (WIDTH - btn_width) // 2
    spacing = 65
    start_y = 170
    
    # Menu Options
    b1 = Button(start_x, start_y, btn_width, btn_height, "1. Train & Benchmark Agent")
    b2 = Button(start_x, start_y + spacing*1, btn_width, btn_height, "2. Human vs AI Agent (Battle Mode)")
    b3 = Button(start_x, start_y + spacing*2, btn_width, btn_height, "3. Human Interference (Adversarial Mode)")
    b4 = Button(start_x, start_y + spacing*3, btn_width, btn_height, "4. Normal vs Optimized AI")
    b5 = Button(start_x, start_y + spacing*4, btn_width, btn_height, "5. Play Traditional Snake Game")
    b6 = Button(start_x, start_y + spacing*5, btn_width, btn_height, "6. Exit")

    buttons = [b1, b2, b3, b4, b5, b6]

    running = True
    while running:
        # Guarantee window is active
        if not pygame.display.get_init():
            pygame.init()
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Agentic Snake")

        screen.fill(BG_COLOR)
        
        # Title UI
        title_text = "AGENTIC SNAKE"
        title_surf = font_title.render(title_text, True, (0, 230, 118))
        title_x = WIDTH//2 - title_surf.get_width()//2
        screen.blit(title_surf, (title_x, 40))
        
        # 🔥 EMOJI JUGAAD: Use your existing snake icon as an emoji!
        try:
            icon = pygame.image.load("snake.png").convert_alpha()
            icon = pygame.transform.scale(icon, (50, 50)) # Resize to match font height
            icon1=pygame.image.load("snake1.png").convert_alpha()
            icon1 = pygame.transform.scale(icon1, (50, 50)) # Resize to match font height
            screen.blit(icon1, (title_x - 60, 40)) # Place it just before the text
            screen.blit(icon, (title_x + title_surf.get_width() + 15, 40)) # Place it after the text
        except:
            pass # Agar icon load nahi hua to game crash nahi hoga

        sub_surf = font_subtitle.render("Select an environment to launch:", True, (170, 170, 180))
        screen.blit(sub_surf, (WIDTH//2 - sub_surf.get_width()//2, 100))

        for btn in buttons:
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if b1.is_clicked(event):
                import train
                train.train_and_benchmark()
                # Restore display after training is done (it uses render_mode=False and True)
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption("Reinforcement Learning AI Lab - Snake Arena")

            elif b2.is_clicked(event):
                from modes.battle_mode import BattleArena
                arena = BattleArena()
                arena.run_match()
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption("Reinforcement Learning AI Lab - Snake Arena")

            elif b3.is_clicked(event):
                from modes import interference_mode
                interference_mode.run_interference_experiment()
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption("Reinforcement Learning AI Lab - Snake Arena")

            elif b4.is_clicked(event):
                from modes import compare_mode
                compare_mode.run_comparison()
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption("Reinforcement Learning AI Lab - Snake Arena")

            elif b5.is_clicked(event):
                from modes import snake_game
                snake_game.run_game() 
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption("Reinforcement Learning AI Lab - Snake Arena")

            elif b6.is_clicked(event):
                running = False

        if pygame.display.get_init():
            pygame.display.flip()
            clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    draw_gui()