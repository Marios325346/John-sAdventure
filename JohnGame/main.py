# COPYRIGHT 2020-2021
# version 0.0.3
# Libraries
import pygame, sys, random, math, time, os
from pygame import mixer
from data.catalogs import *
from data.engine import *
from pygame.locals import *

pygame.init()

# screen
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# Logo
pygame.display.set_caption("John's Adventure  v0.0.3")
icon = pygame.image.load('data/ui/logo.ico')
pygame.display.set_icon(icon)

# Colors
black = (0, 0, 0)

# Main menu
myfont = pygame.font.SysFont("Comic Sans Ms", 24)
title_font = pygame.font.SysFont("Comic Sans Ms", 84)
menu_background = pygame.image.load('data/sprites/mainmenu.png')
cursor = pygame.image.load('data/sprites/j_g_mouse.png')
pygame.mouse.set_visible(False)
# Button UI
playImg = pygame.image.load("data/ui/button interface.png").convert()
playButton = playImg.get_rect()
playButton.center = (320, 305)

quitImg = pygame.image.load("data/ui/quit.png").convert()
quitButton = quitImg.get_rect()
quitButton.center = (320, 445)

settingsImg = pygame.image.load('data/ui/settings.png').convert()
settingsButton = settingsImg.get_rect()
settingsButton.center = (320, 375)

Pixel_font = pygame.font.Font("data/fonts/pixelfont.ttf", 18)

# Background music
pygame.mixer.music.load("data/sound/forest_theme.flac")
pygame.mixer.music.play(-1)


# Controls
def controls():
    global playerX, playerY
    global playerX_change, playerY_change
    global walkCount
    global left, right, up, down
    global interactable

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

            # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            # Left
            if event.key == pygame.K_LEFT:
                playerX_change = -5
                left = True
                right, up, down = False, False, False
            # Right
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
                right = True
                up, left, down = False, False, False
            # Up
            if event.key == pygame.K_UP:
                playerY_change = 5
                up = True
                down, right, left = False, False, False
            # Down
            if event.key == pygame.K_DOWN:
                playerY_change = -5
                down = True
                left, right, up = False, False, False
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RETURN:
                interactable = True
            else:
                interactable = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0
                left, right, up, down = False, False, False, False
                walkCount = 0
def framerate():
    fps = str(int(clock.get_fps()))
    fps_text = Pixel_font.render(fps, 1, pygame.Color("yellow"))
    return fps_text


menu = True
while menu:
    screen.fill((0, 0, 0))
    # background image load
    screen.blit(menu_background, (1, 1))
    StartSound = mixer.Sound("data/sound/button_Sound.wav")

    # Play Button
    if playButton.collidepoint(pygame.mouse.get_pos()):
        playImg = pygame.image.load('data/ui/button interface hover.png')
        #  StartSound.set_volume(0.05)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu = False
                StartSound = mixer.Sound("data/sound/press_start_sound.wav")
                StartSound.play()
                game = True
    else:
        playImg = pygame.image.load('data/ui/button interface.png')

    #Settings

    if settingsButton.collidepoint(pygame.mouse.get_pos()):
        settingsImg = pygame.image.load('data/ui/settings_hover.png')
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("You clicked on the settings button")
    else:
        settingsImg = pygame.image.load('data/ui/settings.png')

    # Quit
    if quitButton.collidepoint(pygame.mouse.get_pos()):
        #  StartSound.set_volume(0.05)
        #  StartSound.play(1)
        quitImg = pygame.image.load('data/ui/quit_hover.png')
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()
    else:
        quitImg = pygame.image.load('data/ui/quit.png')

    screen.blit(playImg, playButton)
    screen.blit(quitImg, quitButton)
    screen.blit(settingsImg, settingsButton)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    screen.blit(framerate(), (10, 0))
    screen.blit(cursor, (pygame.mouse.get_pos()))
    pygame.display.update()

# Player Animation
walkCount = 0
# Walk Right
walkRight = [pygame.image.load('data/sprites/player/playerright1.png'),
             pygame.image.load('data/sprites/player/playerright2.png'),
             pygame.image.load('data/sprites/player/playerright1.png')]
# Walk Left
walkLeft = [pygame.image.load('data/sprites/player/playerleft1.png'),
            pygame.image.load('data/sprites/player/playerleft2.png'),
            pygame.image.load('data/sprites/player/playerleft1.png')]
# Walk Up
walkUp = [pygame.image.load('data/sprites/player/playerup1.png'),
          pygame.image.load('data/sprites/player/playerup2.png'),
          pygame.image.load('data/sprites/player/playerup1.png')]
# Walk Down
walkDown = [pygame.image.load('data/sprites/player/playerdown1.png'),
            pygame.image.load('data/sprites/player/playerdown2.png'),
            pygame.image.load('data/sprites/player/playerdown1.png')]

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
        screen.blit(walkLeft[walkCount // 9], (playerX, playerY))
        walkCount += 1
    elif right:
        screen.blit(walkRight[walkCount // 9], (playerX, playerY))
        walkCount += 1
    elif up:
        screen.blit(walkUp[walkCount // 9], (playerX, playerY))
        walkCount += 1
    elif down:
        screen.blit(walkDown[walkCount // 9], (playerX, playerY))
        walkCount += 1
    else:
        screen.blit(playerImg, (playerX, playerY))


def hearts():
    global myfont
    myfont = pygame.font.SysFont("Comic Sans Ms", 18)
    global heartX
    global heartY
    health = 10
    max_health = 10
    heartX = 20
    heartY = 400
    heartImg = pygame.image.load('data/sprites/player/john_ui.png')
    hp_text = myfont.render(str(health) + "  " + str(max_health), True, (255, 0, 0))
    screen.blit(heartImg, (heartX, heartY))
    screen.blit(hp_text, (heartX + 87, heartY + 12))

catalogImg = pygame.image.load('data/sprites/catalog.png').convert()
def stairs_catalog():
    global catalogImg, game, john_room, kitchen
    global interactable
    text = Pixel_font.render("Go downstairs?", True, (255, 255, 255))
    changeMap = False
    if playerX >= 440 and playerX <= 530 and playerY >= 60 and playerY <= 120:
        screen.blit(catalogImg, (100, 340))
        screen.blit(text, (120, 350))
        if interactable:
            john_room = False
            kitchen = True

sword_Task = True
def sword_task(posX, posY):
    global catalogImg, playerY, playerX , interactable, sword_Task, player_equipped
    sword = pygame.image.load('data/items/wooden_sword.png')
    rotate_sword = pygame.transform.rotate(sword, 90)
    sword_text = Pixel_font.render("Take sword?", True, (255, 255, 255))
    if sword_Task:
        screen.blit(rotate_sword, (posX, posY))
        #  Player/Item collision checking
        if playerX >= posX - 50 and playerX <= posX + 50 and playerY >= posY - 50 and playerY <= posY + 50:
            if sword_Task:
                screen.blit(catalogImg, (100, 340))
                screen.blit(sword_text, (120, 350))  # Text that asks if player wants to equip his sword
            if interactable:
                sword_Task = False
                #equipSound = mixer.Sound("data/sound/press_start_sound.wav")
                #equipSound.play(1)
                player_equipped = True # Player has globally his equipment

    return posX, posY

playerImg = pygame.image.load('data/sprites/player/playeridle.png')  # Player
playerX_change = 0
playerY_change = 0

# Main loop
john_room = True

equip_sword = False

player_equipped = False

# Chunks
john_room, kitchen, basement = False, False, False
route1, route2, route3, route4, training_field = False, False, False, False, False

# World Functions and Values
world_value = 0  # Very important for place position between worlds
route1 = True  # The world you want to start with (Pretty useful to check maps faster)

while game:
    if john_room and world_value == 0:
        playerX = 150
        playerY = 150
    elif john_room and world_value == 1:
        playerX = 380
        playerY = 120
    while john_room:
        # //- JOHNS ROOM -\\#
        background = pygame.image.load('data/sprites/Johns_room.png')
        screen.blit(background, (0, 0))  # Display the background image
        gameWindow()  # Player
        hearts()  # Player UI
        stairs_catalog()  # Catalog when player gets the nearby stairs
        controls()  # Player Controls
        mau()  # Spawn Mau the grey cat

        playerX += playerX_change  # Player X movement
        playerY -= playerY_change  # Player Y movement
        # John's room collisions
        if playerX <= 100:
            playerX = 100
        elif playerX >= 580:
            playerX = 580
        # Y Position 900
        if playerY <= 40:
            playerY = 40
        elif playerY >= 410:
            playerY = 410
        screen.blit(framerate(), (10, 0))
        screen.blit(cursor, (pygame.mouse.get_pos()))
        clock.tick(60)
        pygame.display.update()
    #  --------------- KITCHEN MAP   ---------------

    if kitchen and world_value == 3:
        playerX = 280
        playerY = 350
    elif kitchen and world_value == 5:
        playerX = 480
        playerY = 320

    while kitchen:
        background = pygame.image.load("data/sprites/main_room.png")
        screen.blit(background, (0, 0))
        gameWindow()  # Player
        hearts()  # Player UI
        cynthia(350, 30, playerX, playerY)  # Cynthia NPC
        controls()  # Player controls
        # ----------------- CONTENT --------------------

        if playerY <= 50 and playerX >= 310 and playerX <= 400:
            playerX = 400

        if playerY >= 41 and playerY <= 90 and playerX >= 300 and playerX <= 380:
            playerY = 90
        if playerX <= 290 and playerX >= 280 and playerY <= 50:
            playerX = 280


        if playerY >= 260 and playerY <= 340 and playerX >= 510:  # Player interacts with basement's door
            catalog_bubble("Wanna go to basement?")
            if interactable:
                kitchen = not kitchen
                basement = True

        elif playerX >= 503 and playerY <= 45:  # Player interacts with the stairs
            catalog_bubble("Wanna go to upstairs?")
            if interactable:
                kitchen = False
                john_room = True
                basement = False
                world_value = 1

        elif playerY >= 370 and playerX >= 220 and playerX <= 320:  # Player interacts with the exit door
            if player_equipped:  # Checks if player has done task 1 which is to get his sword
                catalog_bubble("Want to go outside?")
                if interactable:
                    kitchen = False
                    route1 = True
                    basement = False
                    world_value = 0
            else:
                catalog_bubble("Door is locked")

        # Out of bounds
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

        playerX += playerX_change  # Player X movement
        playerY -= playerY_change  # Player Y movement
        screen.blit(framerate(), (10, 0))
        screen.blit(cursor, (pygame.mouse.get_pos()))
        clock.tick(60)
        pygame.display.update()
    #  ----------------- BASEMENT  ---------------

    if basement:
        playerX = 80
        playerY = 340
    while basement:
        background = pygame.image.load('data/sprites/basement.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        gameWindow()
        hearts()
        controls()
        sword_task(135, 25)

        # World change
        if playerY >= 270 and playerX <= 20:  # Collision checking
            catalog_bubble("Go back to kitchen?")
            if interactable:
                basement = False
                kitchen = True
                world_value = 5
        # Furniture Collisions
        if playerY <= 65 and playerX >= -10 and playerY <= 520:
            playerY = 65
        if playerY >= 0 and playerY <= 360 and playerX >= 520:
            playerX = 520
        if playerY >= 350 and playerX >= -20 and playerX <= 520:
            playerY = 350

        # Out of bounds
        if playerX <= 5 and playerY <= 400:
            playerX = 5

        # MOVEMENT X AND Y
        playerX += playerX_change
        playerY -= playerY_change

        screen.blit(cursor, (pygame.mouse.get_pos()))
        screen.blit(framerate(), (10, 0))
        clock.tick(60)
        pygame.display.update()
    # ---------- OUTSIDE WORLD ---------
    if route1 and world_value == 0:
        playerX = 285
        playerY = 70
    elif route1 and world_value == 1:
        playerX = 550

    while route1:
        background = pygame.image.load('data/sprites/world/route1.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        gameWindow()
        hearts()
        controls()
        #Return to john's house
        if playerY <= 55 and playerX >= 270 and playerX <= 320:
            catalog_bubble("Return home?")
            if interactable:
                world_value = 3
                route1 = False
                kitchen = True
                basement = False

        #  Fence collision
        if playerX >= 360 and playerY <= 65:
            playerY = 65
        elif playerX <= 220 and playerY <= 65:
            playerY = 65

        # Out of bounds
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

        if playerX >= 580:
            route1 = False
            route2 = True
            basement = False
            world_value = 0


        # MOVEMENT X AND Y
        playerX += playerX_change
        playerY -= playerY_change
        screen.blit(cursor, (pygame.mouse.get_pos()))
        screen.blit(framerate(), (10, 0))
        clock.tick(60)
        pygame.display.update()

    if route2 and world_value == 0:
        playerX = 50
    elif world_value == 1:
        playerX = 520

    while route2:
        background = pygame.image.load('data/sprites/world/route2.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        gameWindow()
        hearts()
        controls()

        # Out of bounds
        if playerX <= 5:
            playerX = 5
        elif playerX >= 580:
            playerX = 580
        # Y Position 900
        if playerY <= 10:
            playerY = 10
        elif playerY >= 410:
            playerY = 410
        if playerY <= 40 and playerX <= 105:
            playerY = 40

        if playerX >= 580:
            world_value = 0
            route2 = False
            route3 = True

        elif playerX <= 10:
            world_value = 1
            route2 = False
            route1 = True
        # MOVEMENT X AND Y
        playerX += playerX_change
        playerY -= playerY_change
        screen.blit(cursor, (pygame.mouse.get_pos()))
        screen.blit(framerate(), (10, 0))
        clock.tick(60)
        pygame.display.update()

    if route3 and world_value == 0:
        playerX = 50
    elif route3 and world_value == 2:
        playerY = 350

    while route3:
        background = pygame.image.load('data/sprites/world/route3.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        gameWindow()
        hearts()
        controls()

        # Out of bounds
        if playerX <= 5:
            playerX = 5
        elif playerX >= 580:
            playerX = 580
        # Y Position 900
        if playerY <= 10:
            playerY = 10
        elif playerY >= 410:
            playerY = 410

        if playerY >= 400:
            route3 = False
            route4 = True
            world_value = 0
        elif playerX <= 10:
            world_value = 1
            route3 = False
            route2 = True
        # MOVEMENT X AND Y
        playerX += playerX_change
        playerY -= playerY_change
        screen.blit(cursor, (pygame.mouse.get_pos()))
        screen.blit(framerate(), (10, 0))
        clock.tick(60)
        pygame.display.update()

    if route4 and world_value == 0:
        playerY = 50
    elif world_value == 2:
        playerX = 520

    while route4:
        background = pygame.image.load('data/sprites/world/route4.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        gameWindow()
        hearts()
        controls()

        # Out of bounds
        if playerX <= 5:
            playerX = 5
        elif playerX >= 580:
            playerX = 580
        # Y Position 900
        if playerY <= 10:
            playerY = 10
        elif playerY >= 410:
            playerY = 410

        if playerX >= 580:
            route4, training_field = False, True
            world_value = 0
        if playerY <= 10:
            world_value = 2
            route3, route4 = True, False

        # MOVEMENT X AND Y
        playerX += playerX_change
        playerY -= playerY_change
        screen.blit(cursor, (pygame.mouse.get_pos()))
        screen.blit(framerate(), (10, 0))
        clock.tick(60)
        pygame.display.update()

    if training_field and world_value == 0:
        playerX = 50

    #elif world_value == 2:
       #pass
    while training_field:
        background = pygame.image.load('data/sprites/world/training_field.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        manos()  # Spawn Manos young master npc
        blacksmith_shop()  # Blacksmith shop
        training_dummie()  # Training Dummie
        gameWindow()
        hearts()
        controls()
        candy(290, 190, playerX, playerY)  # Cat npc

        # Out of bounds
        if playerX <= 5:
            playerX = 5
        elif playerX >= 580:
            playerX = 580
        # Y Position 900
        if playerY <= 10:
            playerY = 10
        elif playerY >= 410:
            playerY = 410

        if playerX <= 10:
            world_value = 2
            route4, training_field = True, False
        # MOVEMENT X AND Y
        playerX += playerX_change
        playerY -= playerY_change
        screen.blit(cursor, (pygame.mouse.get_pos()))
        screen.blit(framerate(), (10, 0))
        clock.tick(60)
        pygame.display.update()

