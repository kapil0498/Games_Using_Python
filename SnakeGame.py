import pygame, random, os
# Initialize the pygame module by using init() function
pygame.init()

# Define Colours
# rgb is colour set with value(0-255)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

# Creating window
screen_width = 700
screen_height = 400
gameWindow = pygame.display.set_mode((screen_width,screen_height))

# Game Title
pygame.display.set_caption("Snake Game")
# Without giving update command it will not run the code written for title
pygame.display.update()
font = pygame.font.SysFont("Arial", 40)
clock = pygame.time.Clock()


def score_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text,[x,y]) #Update the window

def plot_snake(gameWindow, color, snake_list, snake_size):
    for x,y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((150,150,150))
        score_screen("Welcome to the Snake Game",black,150,145)
        score_screen("Press Enter to Start the Game", black, 140, 185)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()
        pygame.display.update()
        clock.tick(60)

def game_loop():
    # Game Specific Variable
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 10
    food_x = random.randint(20, screen_width/2)
    food_y = random.randint(20, screen_height/2)
    food_size = 10
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5
    score = 0
    snake_list = []
    snake_length = 1
    fps = 20  # Frames Per Second
    # Check if High_Score.txt file exists or not; if not create it
    if (not os.path.exists("High_Score.txt")):
        with open("High_Score.txt", "w") as f:
            f.write("0")
    with open("High_Score.txt", "r") as f:
        high_score = f.read()

    # Creating a Game Loop
    while not exit_game:
        if game_over == True:
            #Update the High Score
            with open("High_Score.txt", "w") as f:
                f.write(str(high_score))

            gameWindow.fill(black)
            score_screen("Game Over..!!  Press ENTER to Restart",red,screen_width/10,screen_height/2.5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_DOWN:
                        velocity_x = 0
                        velocity_y = init_velocity
                    if event.key == pygame.K_UP:
                        velocity_x = 0
                        velocity_y = -init_velocity

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            #Food eaten by snake and new food plotted for snake
            if abs(snake_x - food_x)<6 and abs(snake_y - food_y)<6:
                score += 10
                #print(f"Score : {score * 10}")
                food_x = random.randint(20, screen_width/2)
                food_y = random.randint(20, screen_height/2)
                snake_length = snake_length + 1
                if score>int(high_score):
                    high_score = score

            # Giving the color to the display which is by default black using rgb color
            gameWindow.fill(black)
            #score_screen(f"High Score : {high_score}", red,5,5)
            score_screen(f"Score : {score}                   High Score : {high_score}", white, 5, 5)
            pygame.draw.rect(gameWindow, green,[food_x, food_y, food_size,food_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list)>snake_length:
                del snake_list[0]

            #Use Slicing to overlap the body of snake excluding snake head whose position is -1
            if head in snake_list[:-1]:
                game_over = True

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True

            #pygame.draw.rect(gameWindow, white,[snake_x, snake_y, snake_size, snake_size])
            plot_snake(gameWindow, red, snake_list, snake_size)

        pygame.display.update()
        clock.tick(fps)


    pygame.quit()
    quit()
welcome()