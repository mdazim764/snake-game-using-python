# Importing Some Modules
import pygame
import random
import os
# from random import randint
# -------------------------------------

# Load Background Musics...
pygame.mixer.init()

# Set Game Window Size
pygame.init()
screen_width = 700
screen_height = 500
game_window = pygame.display.set_mode((screen_width, screen_height))
#-------------------------------------------
# Background Images
bgimg2 = pygame.image.load(os.path.join("img_music", "s1.jpg"))
bgimg2 = pygame.transform.scale(bgimg2, (screen_width, screen_height)).convert_alpha()
bgimg = pygame.image.load(os.path.join("img_music", "s2.jpg"))
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
bgimg1 = pygame.image.load(os.path.join("img_music", "s3.jpg"))
bgimg1 = pygame.transform.scale(bgimg1, (screen_width, screen_height)).convert_alpha()

#----------------------------------------------
# Game title
pygame.display.set_caption("Snake Game..")
pygame.display.update()

font = pygame.font.SysFont(None,55)
#function name def
def text_screen(text,color,x,y):
    screen_text = font.render(text,True,color)
    game_window.blit(screen_text,[x,y])


def plot_snake(game_window, color,snk_list, snak_size) :
    for x,y in snk_list :
        pygame.draw.rect(game_window, color, [x,y, snak_size, snak_size])


# Welcome loop
black = (0, 0, 0)
white = (255, 255, 255)
clock = pygame.time.Clock()


#welcome page
def welcome():
    exit_game = False
    while not exit_game :
        game_window.fill(white)
        game_window.blit(bgimg2, (0, 0))


        text_screen("Welcome to Snakes Game",white, 100, 300)
        text_screen("Press Space Bar To Play Game", white, 70, 350)
        text_screen("Press E Key to Exit" ,pygame.Color("red"), 70, 400)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Load Background Musics...
                    pygame.mixer.music.load(os.path.join("img_music", "game_back.mp3"))
                    pygame.mixer.music.play(-1)
                    gameloop()
                elif event.key == pygame.K_e:
                    return  # Return to Main Menu without quitting Pygame

        pygame.display.update()
        clock.tick(60)


#Game loop..
def gameloop():

    # colors
    white = (255, 255, 255)
    red = (255, 20, 10)
    black = (0, 0, 0)
    green = (0, 255, 0)
    pink = (255, 0, 100)
    color1 = (150, 25, 0)
    color2 = (0, 25, 150)
    color3 = (25, 0, 60)
    color = [red, green, pink, color1, color2, color3]
    food_color = random.choice(color)
    score_color = random.choice(color)
    hiscore_color = random.choice(color)

# check if high score fil exit
    if(not os.path.exists("high_score.txt")) :
        with open("high_score.txt", "w") as f:
            f.write("0")
    with open("high_score.txt", "r") as f:
        hiscore = f.read()

    # Game specific variable

    exit_game = False
    game_over = False

    # snake specification
    snak_x = 45 # Make it a multiple of 15
    snak_y = 45 # Make it a multiple of 15
    snak_size = 15
    fps = 15
    velo_x = 0
    velo_y = 0
    init_velo = 15 # Ensure snake moves by EXACTLY 1 grid size per tick! (was 5)

    # Food coding (Aligned to 15-pixel grid)
    score = 0
    # randint(range) * grid_size ensures it falls exactly on the grid
    food_x = random.randint(3, (screen_width // snak_size) - 3) * snak_size
    food_y = random.randint(3, (screen_height // snak_size) - 3) * snak_size

    clock = pygame.time.Clock()
#snake length 
    snk_list = []
    snk_length = 1
#here the main game start
    while not exit_game:
        if game_over :
            if score>=int(hiscore) :
                with open("high_score.txt", "w") as f:
                    f.write(str(hiscore))
            game_window.fill(white)

            game_window.blit(bgimg1, (0, 0))
            text_screen("High score :" + str(hiscore), green, 30, 40)
            text_screen("score :" + str(score), green, 470, 136)
            text_screen("Game Over!",red,230,270)
            text_screen("Press Enter to Continue ",green,20,420)
            text_screen("Press E Key End for Exit", red, 20, 460)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:#enter button
                        # Load Background Musics...
                        pygame.mixer.music.load(os.path.join("img_music", "game_back.mp3"))
                        pygame.mixer.music.play(-1)
                        gameloop()
                    elif event.key == pygame.K_e:
                        exit_game = True


                    if event.key == pygame.K_END:
                        exit_game = True

        else:

        # Keys Handling
            for event in pygame.event.get():
                # print(event)
                if event.type==pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velo_x = + init_velo
                        velo_y = 0

                    if event.key == pygame.K_LEFT:
                        velo_x = - init_velo
                        velo_y = 0

                    if event.key == pygame.K_UP:
                        velo_y = - init_velo
                        velo_x = 0

                    if event.key == pygame.K_DOWN:
                        velo_y = + init_velo
                        velo_x = 0

                    if event.key == pygame.K_q:#for cheating purpose or increasing score 
                        score += 2

                    if event.key == pygame.K_f:#game fast 
                        init_velo += 2

                    if event.key == pygame.K_l:#for slow
                        init_velo -= 2


                    if event.key == pygame.K_s:# for stop
                        velo_x = 0.00000001
                        velo_y = 0.00000001





            snak_x = snak_x + velo_x
            snak_y = snak_y + velo_y

        # score printing snake increse the length
            if abs(snak_x-food_x)<10 and abs(snak_y-food_y)<10 and abs(snak_x-food_x)>-10 and abs(snak_y-food_y)>-10 :
                # Load Background Musics...
                food = pygame.mixer.Sound(os.path.join("img_music", "Drop.ogg"))
                food.play()

                score += 1   
                # New aligned food
                food_x = random.randint(3, (screen_width // snak_size) - 3) * snak_size
                food_y = random.randint(3, (screen_height // snak_size) - 3) * snak_size
                food_color = random.choice(color)#color showing randomly
                score_color = random.choice(color)
                snk_length +=3
#high score overlapped previous score then updated the high score
                if score>int(hiscore):
                    hiscore = score
                    hiscore_color = random.choice(color)

            game_window.fill(white)
            game_window.blit(bgimg, (0,0))
            # 🔥 Draw Transparent Grid (20-30% Opacity)
            # Pygame doesn't support alpha on direct line drawing easily, 
            # so we create a transparent surface, draw lines on it, and blit it.
            grid_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            grid_color = (255, 255, 255, 50) # White color with ~20% alpha (50/255)
            
            for x in range(0, screen_width, snak_size):
                pygame.draw.line(grid_surface, grid_color, (x, 0), (x, screen_height))
            for y in range(0, screen_height, snak_size):
                pygame.draw.line(grid_surface, grid_color, (0, y), (screen_width, y))
                
            game_window.blit(grid_surface, (0, 0)) # Put the grid over the background

            # Texts and Food
            text_screen("High Score :" + str(hiscore), hiscore_color, 250, 5)
            text_screen("Score :" + str(score ), score_color, 0, 5)
            # pygame.draw.circle(game_window, food_color, [food_x, food_y], 10)
            pygame.draw.rect(game_window, food_color, [food_x, food_y, snak_size, snak_size])
#snak head increase code
            head =[]
            head.append(snak_x)
            head.append(snak_y)
            snk_list.append(head)

            if len(snk_list)>snk_length :
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
               
                pygame.mixer.music.load(os.path.join("img_music", "gameover.mp3"))
                pygame.mixer.music.play()
#if snake touches window line then game over
            if snak_x<0 or snak_x>=screen_width or snak_y<0 or snak_y>=screen_height :
                game_over = True
               
                pygame.mixer.music.load(os.path.join("img_music", "gameover.mp3"))
                pygame.mixer.music.play()


            # pygame.draw.rect(game_window, black,[snak_x, snak_y, snak_size, snak_size])
            plot_snake(game_window, black,snk_list, snak_size)

        pygame.display.update()
        clock.tick(fps)


    # pygame.quit()
    # quit()
    return  # Return to Main Menu without quitting Pygame

  
def run_game():
    pygame.mixer.music.load(os.path.join("img_music", "welcome.mp3"))
    pygame.mixer.music.play(-1)
    welcome()


if __name__ == "__main__":
    run_game()
