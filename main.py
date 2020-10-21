# COPYRIGHT 2020-2021
# version 0.0.3


from engine import cynthia
import os, pygame, random, math, time, sys
from pygame import mixer
from pygame import *

from catalogs import catalog_bubble

pygame.init()

# screen
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# Logo
pygame.display.set_caption("John's Adventure")
icon = pygame.image.load('items/logo.png')
pygame.display.set_icon(icon)

# Colors
black = (0, 0, 0)

# Main menu
myfont = pygame.font.SysFont("Comic Sans Ms", 24)
title_font = pygame.font.SysFont("Comic Sans Ms", 84)
menu_background = pygame.image.load('sprites/mainmenu.png')
cursor = pygame.image.load('sprites/j_g_mouse.png')
pygame.mouse.set_visible(False)
start_text = myfont.render("Press Enter/Click \n to start the game", True, black)

# Background music
# pygame.mixer.music.load("sound/home.mp3")
# pygame.mixer.music.play(-1)

#Controls
def controls():
    global playerX, playerY
    global playerX_change, playerY_change
    global walkCount
    global left, right, up, down
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

            # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            # Left
            if event.key == pygame.K_LEFT:
                playerX_change = -7
                left = True
                right, up, down = False, False, False
            # Right
            if event.key == pygame.K_RIGHT:
                playerX_change = 7
                right = True
                up, left, down = False, False, False
            # Up
            if event.key == pygame.K_UP:
                playerY_change = 7
                up = True
                down, right, left = False, False, False
            # Down
            if event.key == pygame.K_DOWN:
                playerY_change = -7
                down = True
                left, right, up = False, False, False
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0
                left, right, up, down = False, False, False, False
                walkCount = 0

Pixel_font = pygame.font.Font("fonts/pixelfont.ttf", 18)

def framerate():
    fps = str(int(clock.get_fps()))
    fps_text = Pixel_font.render(fps, 1, pygame.Color("yellow"))
    return fps_text

catalogImg = pygame.image.load('sprites/catalog.png')
def stairs_catalog():
    global catalogImg, game, main_room
    text = Pixel_font.render("Go downstairs?", True, (255, 255, 255))
    changeMap = False
    if playerX >= 440 and playerX <= 530 and playerY >= 60 and playerY <= 120:
        screen.blit(catalogImg, (100, 340))
        screen.blit(text, (120, 350))
        if event.key == pygame.K_RETURN:
                print("Next level")
                game = not game
                main_room = True
            #time.wait(1000)
            #changeMap = True
        #if changeMap:
            #game = not game
            #main_room = True

menu = True
while menu:
    screen.fill((0, 0, 0))
    # background image load
    screen.blit(menu_background, (1, 1))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.MOUSEBUTTONDOWN:
                menu = False
                StartSound = mixer.Sound("sound/press_start_sound.wav")
                StartSound.play()
                game = True
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            menu = not menu
            game = True
    screen.blit(framerate(), (10, 0))
    screen.blit(cursor, (pygame.mouse.get_pos()))
    screen.blit(start_text, (100, 300))
    pygame.display.update()

# //- JOHNS ROOM -\\#
background = pygame.image.load('sprites/Johns_room.png')
# Player
# playerImg = pygame.image.load('playeridle.png') #Player must be sowhere around 128pixels (maybe)
playerImg = pygame.image.load('sprites/player/playeridle.png')  # Player must be sowhere around 128pixels (maybe)
playerX = 100
playerY = 100
playerX_change = 0
playerY_change = 0

# Player Animation
walkCount = 0
# Walk Right
walkRight = [pygame.image.load('sprites/player/playerright1.png'), pygame.image.load('sprites/player/playerright2.png'), pygame.image.load('sprites/player/playerright1.png')]
# Walk Left
walkLeft = [pygame.image.load('sprites/player/playerleft1.png'), pygame.image.load('sprites/player/playerleft2.png'), pygame.image.load('sprites/player/playerleft1.png')]
# Walk Up
walkUp = [pygame.image.load('sprites/player/playerup1.png'), pygame.image.load('sprites/player/playerup2.png'), pygame.image.load('sprites/player/playerup1.png')]
# Walk Down
walkDown = [pygame.image.load('sprites/player/playerdown1.png'), pygame.image.load('sprites/player/playerdown2.png'), pygame.image.load('sprites/player/playerdown1.png')]

left = False
right = False
up = False
down = False


# This function is responsible for player's animation
def gameWindow():
    global walkCount
    global left, right, up, down
    if walkCount + 1 >= 27:
        walkCount = 0
    if left:
        if event.key != pygame.K_z:
            screen.blit(walkLeft[walkCount // 9], (playerX, playerY))
            walkCount += 1
        else:
            pass
    elif right:
        if event.key != pygame.K_z:
            screen.blit(walkRight[walkCount // 9], (playerX, playerY))
            walkCount += 1
        else:
            pass
    elif up:
        if event.key != pygame.K_z:
            screen.blit(walkUp[walkCount // 9], (playerX, playerY))
            walkCount += 1
        else:
            pass
    elif down:
        if event.key != pygame.K_z:
            screen.blit(walkDown[walkCount // 9], (playerX, playerY))
            walkCount += 1
        else:
            pass
    else:
        screen.blit(playerImg, (playerX, playerY))
    # IT KINDA WORKS YALLL <3
    pygame.display.update()


def hearts():
    global myfont
    myfont = pygame.font.SysFont("Comic Sans Ms", 18)
    global heartX
    global heartY
    health = 10
    max_health = 10
    heartX = 20
    heartY = 400
    heartImg = pygame.image.load('sprites/player/john_ui.png')
    hp_text = myfont.render(str(health) + "  " + str(max_health), True, (255, 0, 0))
    screen.blit(heartImg, (heartX, heartY))
    screen.blit(hp_text, (heartX + 87, heartY + 12))


# BEDROOM
while game:
    screen.fill((0, 0, 0))
    # background image load
    screen.blit(background, (0, 0))
    hearts()

    controls()
    # MOVEMENT X AND Y
    playerX += playerX_change
    playerY -= playerY_change

    # Stops the player from going out of bounds
    # X Position 1200
    if playerX <= 5:
        playerX = 5
    elif playerX >= 580:
        playerX = 580
    # Y Position 900
    if playerY <= 40:
        playerY = 40
    elif playerY >= 410:
        playerY = 410

    # Cynthia

    # print("X:",playerX,"Y",playerY)
    screen.blit(framerate(), (10, 0))
    screen.blit(cursor, (pygame.mouse.get_pos()))
    stairs_catalog()
    clock.tick(60)
    gameWindow()

main_room_background = pygame.image.load('sprites/main_room.png')
basement = False
while main_room:
    screen.fill((0, 0, 0))
    # background image load
    screen.blit(main_room_background, (0, 0))
    hearts()

    # Content

    cynthia(350, 30, playerX, playerY)


    #Controls
    controls()
    # Stops the player from going out of bounds
    if playerX <= 5:
        playerX = 5
    elif playerX >= 580:
        playerX = 580
    # Y Position 900
    if playerY <= 10:
        playerY = 10
    elif playerY >= 410:
        playerY = 410
    if playerY <= 40 and playerX <= 245:
        playerY = 40

    # BASEMENT or Outdoors
    if playerY >= 260 and playerY <= 340 and playerX >= 510:
        catalog_bubble("Wanna go to basement?")
        if event.key == K_RETURN:
            main_room = not main_room
            basement = True
    elif playerY >= 370 and playerX >= 220 and playerX <= 320:
        print("You went outside")

    # MOVEMENT X AND Y
    playerX += playerX_change
    playerY -= playerY_change
    #print("X:",playerX , "Y:",playerY)
    screen.blit(cursor, (pygame.mouse.get_pos()))
    screen.blit(framerate(), (10, 0))
    clock.tick(60)
    gameWindow()

basementImg = pygame.image.load('sprites/basement.png')
while basement:
    screen.fill((0, 0, 0))
    screen.blit(basementImg, (0, 0))
    hearts()

    controls()
    # MOVEMENT X AND Y
    playerX += playerX_change
    playerY -= playerY_change
    screen.blit(cursor, (pygame.mouse.get_pos()))
    screen.blit(framerate(), (10, 0))
    clock.tick(60)
    gameWindow()
