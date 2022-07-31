from pygame import mixer, event
import math, random
import pygame

# Initialize Pygame
pygame.init()


# Create a screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Background
background = pygame.image.load('background.png')


# Sound
# mixer.music.load('background.wav')
# mixer.music.play(-1)


# Caption and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)


# Player 
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0


# Enemy
enemyImg = []
enemyX = []
enemy_flag = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randrange(0, 756, 5))
    enemyY.append(random.randrange(50, 150, 10))
    enemyX_change.append(4)
    enemyY_change.append(0.5)
    enemy_flag.append("normal")


# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Font
font = pygame.font.SysFont("comicsansms", 18)

FPSCLOCK = pygame.time.Clock()

#Score
SCORE = 0
HIGHEST = 0

SPEED = 0

def textObject(text, font, text_color):
        myText = font.render(text, True, text_color)
        return myText, myText.get_rect()

def message_to_screen(msg, color, font, y_displace = 0):
        TextSurface, TextRect = textObject(msg, font, color)
        # y_dispalce is used to get y displacement from centre
        TextRect.center = (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2) + y_displace         
        screen.blit(TextSurface, TextRect)

def total_score():
        
        global SCORE, HIGHEST
        
        paused = True
        
        totalScoreFont = pygame.font.SysFont('Arial', 25, 'b') 
        message_to_screen(f"Total Score: {SCORE}", (255, 40, 0), totalScoreFont, -100)
        message_to_screen("Press Enter and Goto the Main Screen", (0, 0, 0), font, 203)
        
        if(HIGHEST < SCORE):
            HIGHEST = SCORE
        SCORE = 0

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    paused = False

            pygame.display.update()		

def pause():
        paused = True
        message_to_screen("Paused", (255, 40, 0), font, -100)
        message_to_screen("Press Escape to continue or q to quit", (0, 0, 0), font, -20)

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_ESCAPE:
                        paused = False
            pygame.display.update()	
	

def button(bx, by, width, height, color, color2, text_color, text):
        mouse = pygame.mouse.get_pos()

        if bx + width > mouse[0] > bx and by + height > mouse[1] > by:
            pygame.draw.rect(screen, color2, (bx,by,width,height))
        else:
            pygame.draw.rect(screen, color, (bx,by,width,height))
        TextSurf, TextRect = textObject(text, font, text_color)
        TextRect.center = ((bx + (width/2)), (by + (height/2)))
        screen.blit(TextSurf, TextRect)

def welcomeScreen():
        """
        Shows welcome images on the screen
        """
        global enemyY_change, SPEED

        easyButton = {'x': 220, 'y': 450,'width': 80, 'height': 40, 'color': (255,255,255), 'color2': (57,255,20), 'text_color': (0,0,0), 'text': "Easy"}
        mediumButton = {'x': 370, 'y': 450,'width': 80, 'height': 40, 'color': (255,255,255), 'color2': (57,255,20), 'text_color':  (0,0,0), 'text': "Medium"}
        hardButton = {'x': 520, 'y': 450,'width': 80, 'height': 40, 'color': (255,255,255), 'color2': (57,255,20), 'text_color': (0,0,0), 'text': "Hard"}
        startButton = {'x': 370, 'y': 545,'width': 80, 'height': 40, 'color': (255,255,255), 'color2': (57,255,20), 'text_color':  (0,0,0), 'text': "Start"}

        
        while True:
            for event in pygame.event.get():
                # if user clicks on cross button, close the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                elif event.type ==pygame.MOUSEBUTTONDOWN:
                    if ((pygame.mouse.get_pos()[0] > easyButton['x'] and pygame.mouse.get_pos()[0] < easyButton['x'] + easyButton['width']) and
                    (pygame.mouse.get_pos()[1] > easyButton['y'] and pygame.mouse.get_pos()[1] < easyButton['y'] + easyButton['height'])):
                        SPEED = 60
                        mixer.Sound('swoosh.wav').play()

                    elif ((pygame.mouse.get_pos()[0] > mediumButton['x'] and pygame.mouse.get_pos()[0] < mediumButton['x'] + mediumButton['width']) and
                    (pygame.mouse.get_pos()[1] > mediumButton['y'] and pygame.mouse.get_pos()[1] < mediumButton['y'] + mediumButton['height'])):
                        SPEED = 70
                        mixer.Sound('swoosh.wav').play()
                        enemyY_change.clear()
                        for _ in range(num_of_enemies):
                            enemyY_change.append(0.7)

                    elif ((pygame.mouse.get_pos()[0] > hardButton['x'] and pygame.mouse.get_pos()[0] < hardButton['x'] + hardButton['width']) and
                    (pygame.mouse.get_pos()[1] > hardButton['y'] and pygame.mouse.get_pos()[1] < hardButton['y'] + hardButton['height'])):
                        SPEED = 100
                        mixer.Sound('swoosh.wav').play()
                        enemyY_change.clear()
                        for _ in range(num_of_enemies):
                            enemyY_change.append(1)

                    elif ((pygame.mouse.get_pos()[0] > startButton['x'] and pygame.mouse.get_pos()[0] < startButton['x'] + startButton['width']) and
                        (pygame.mouse.get_pos()[1] > startButton['y'] and pygame.mouse.get_pos()[1] < startButton['y'] + startButton['height']) and SPEED != 0):
                            mixer.Sound('swoosh.wav').play()
                            return

                    elif ((pygame.mouse.get_pos()[0] > startButton['x'] and pygame.mouse.get_pos()[0] < startButton['x'] + startButton['width']) and
                        (pygame.mouse.get_pos()[1] > startButton['y'] and pygame.mouse.get_pos()[1] < startButton['y'] + startButton['height'])):
                            mixer.Sound('hit.wav').play()
                else:
                    
                    screen.blit(background, (0, 0))


                    button(easyButton['x'], easyButton['y'], easyButton['width'], easyButton['height'], easyButton['color'], easyButton['color2'], easyButton['text_color'], easyButton['text'])
                    button(mediumButton['x'], mediumButton['y'], mediumButton['width'], mediumButton['height'], mediumButton['color'], mediumButton['color2'], mediumButton['text_color'], mediumButton['text'])
                    button(hardButton['x'], hardButton['y'], hardButton['width'], hardButton['height'], hardButton['color'], hardButton['color2'], hardButton['text_color'], hardButton['text'])
                    button(startButton['x'], startButton['y'], startButton['width'], startButton['height'], startButton['color'], startButton['color2'], startButton['text_color'], startButton['text'])
                    # pygame.display.flip() 
                    

                    # This is for showing the highest SCORE lable on the welcome screen.
                    TextSurface, TextRect = textObject(f"Highest: {HIGHEST}", font, (255, 255, 255))
                    TextRect.center = (50), (20)
                    screen.blit(TextSurface, TextRect)
                    
                    pygame.display.update()
                FPSCLOCK.tick(SPEED)



def player(x , y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
    

def isCollide(enemyX, enemyY, bulletX, bulletY):
    enemies_width_range_of_numbers = []
    enemies_height_range_of_numbers = []

    enemyY = round(enemyY)
    for j in range(enemyX - 35, enemyX + 36):
        enemies_width_range_of_numbers.append(j)
    
    for j in range(enemyY - 20, enemyY + 20):
        enemies_height_range_of_numbers.append(j)

    if(bulletX in enemies_width_range_of_numbers and bulletY in enemies_height_range_of_numbers):
        return True
    else:
        return False

def show_score():
    score_text = font.render(f"Score = {SCORE}", True, (255,255,255))
    screen.blit(score_text, (0,0))


FPSCLOCK = pygame.time.Clock()

welcomeScreen()

# Game Loop 
running = True
while running:

    screen.fill((0,0,0))


    # Setting the background.
    screen.blit(background, (0, 0))


    # Danger Line
    danger_line = font.render('-' * 800, True, (255, 0, 0))
    screen.blit(danger_line, (0, 480))


    # calling show_score() function which will show us a score of the current game.
    show_score()

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        elif event.type == pygame.KEYDOWN and  (event.key == pygame.K_ESCAPE):
            pause()
        elif(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_RIGHT):
                playerX_change = 5
            if(event.key == pygame.K_LEFT):
                playerX_change = - 5
            if(event.key == pygame.K_SPACE):
                if(bullet_state == "ready"):
                    mixer.Sound('laser.wav').play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                   
    playerX += playerX_change
    if(playerX >= 736):
        playerX = 736
    elif(playerX <= 0):
        playerX = 0

    # Enemy Movement
    for i in range(num_of_enemies):

        if(enemyY[i] >= 440):
            total_score()
            welcomeScreen()

        if(enemy_flag[i] == "normal"):
            enemyX[i] += enemyX_change[i]
        
        if(enemy_flag[i] == "reverse"):
            enemyX[i] -= enemyX_change[i]
            enemyY[i] += enemyY_change[i]
        
        enemy(enemyX[i], enemyY[i], i)

        if(enemyX[i] <= 0):
            enemy_flag[i] = "normal"
        if(enemyX[i] >= 736):
            enemy_flag[i] = "reverse"


    # Bullet Movement
    if(bulletY <= 0):
        bulletY = 480
        bullet_state = "ready"

    if(bullet_state == "fire"):
        fire_bullet(bulletX, bulletY)
        for i in range(num_of_enemies):
            if(isCollide(enemyX[i], enemyY[i], bulletX, bulletY)):
                mixer.Sound('explosion.wav').play()
                SCORE += 1
                enemyX[i] = random.randrange(0, 756, 5)
                enemyY[i] = random.randrange(50, 150, 5)

        bulletY -= bulletY_change  


    player(playerX, playerY)
    pygame.display.update()
    FPSCLOCK.tick(SPEED)

