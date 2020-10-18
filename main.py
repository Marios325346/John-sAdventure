#COPYRIGHT 2020-2021
#version 0.

import os, pygame, random , math , time , sys
from pygame import mixer
from pygame import *

pygame.init()

#screen
screen = pygame.display.set_mode((640,480))
clock = pygame.time.Clock()

#Logo
pygame.display.set_caption("John's Adventure")
icon = pygame.image.load('items/logo.png')
pygame.display.set_icon(icon)

#Colors 
black = (0,0,0)

#Main menu
myfont = pygame.font.SysFont("Comic Sans Ms", 24)
title_font = pygame.font.SysFont("Comic Sans Ms", 84)
menu_background = pygame.image.load('sprites/mainmenu.png')
cursor = pygame.image.load('sprites/j_g_mouse.png')
pygame.mouse.set_visible(False)
start_text = myfont.render("Press Enter/Click \n to start the game", True, black)


#Background music
#pygame.mixer.music.load("sound/home.mp3")
#pygame.mixer.music.play(-1)

Arial_font = pygame.font.SysFont("Arial",28)
def framerate():
    fps = str(int(clock.get_fps()))
    fps_text = Arial_font.render(fps, 1, pygame.Color("yellow"))
    return fps_text

menu = True
while menu:
    screen.fill((0,0,0))
    #background image load
    screen.blit(menu_background,(1,1))
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
    screen.blit(framerate(), (10,0))
    screen.blit(cursor,(pygame.mouse.get_pos()))
    screen.blit(start_text , (100, 300))
    pygame.display.update()

#//-   T U T O R I A L    L E V E L   -\\#

#background
background = pygame.image.load('sprites/Johns_room.png')
# Player
#playerImg = pygame.image.load('playeridle.png') #Player must be sowhere around 128pixels (maybe)
playerImg = pygame.image.load('sprites/player/playeridle.png') #Player must be sowhere around 128pixels (maybe)
playerX = 100
playerY = 100
playerX_change = 0
playerY_change = 0

# Player Animation
walkCount = 0
#Walk Right
walkRight = [pygame.image.load('sprites/player/playerright1.png'),pygame.image.load('sprites/player/playerright2.png'),pygame.image.load('sprites/player/playerright1.png')]
#Walk Left
walkLeft = [pygame.image.load('sprites/player/playerleft1.png'),pygame.image.load('sprites/player/playerleft2.png'),pygame.image.load('sprites/player/playerleft1.png')]
#Walk Up
walkUp = [pygame.image.load('sprites/player/playerup1.png'),pygame.image.load('sprites/player/playerup2.png'),pygame.image.load('sprites/player/playerup1.png')]
#Walk Down
walkDown = [pygame.image.load('sprites/player/playerdown1.png'),pygame.image.load('sprites/player/playerdown2.png'),pygame.image.load('sprites/player/playerdown1.png')]

left = False
right = False
up = False
down = False
#This function is responsible for player's animation
def gameWindow():
    global walkCount  
    if walkCount + 1 >= 27:
        walkCount = 0
    if left:  
      if event.key != pygame.K_z:
            screen.blit(walkLeft[walkCount//9], (playerX, playerY))
            walkCount += 1    
    elif right:
        if event.key != pygame.K_z:
            screen.blit(walkRight[walkCount//9], (playerX, playerY))
            walkCount += 1  
    elif up:
        if event.key != pygame.K_z:
            screen.blit(walkUp[walkCount//9], (playerX, playerY))
            walkCount += 1
    elif down:
        if event.key != pygame.K_z:
            screen.blit(walkDown[walkCount//9], (playerX, playerY))
            walkCount += 1        
    else:
        screen.blit(playerImg,(playerX, playerY))
    #IT KINDA WORKS YALLL <3
    pygame.display.update()

    

def hearts():
    global myfont
    myfont = pygame.font.SysFont("Comic Sans Ms", 18)
    global heartX
    global heartY
    health = 10
    max_health = 10
    heartX = 20
    heartY = 405
    heartImg = pygame.image.load('sprites/player/john_ui.png')
    hp_text = myfont.render(str(health)+"  "+str(max_health) ,True , (255,0,0))
    screen.blit(heartImg,(heartX,heartY))
    screen.blit(hp_text,(heartX + 87, heartY + 12))
    

#Abilities
def sprint():
    global playerX_change
    global playerY_change
    if up:
        playerY_change = playerY_change + 10
    elif down:
        playerY_change = playerY_change - 10
    elif right:
        playerX_change = playerX_change + 10
    elif left:
        playerX_change = playerX_change - 10

# BEDROOM
#Catalog
catalogImg = pygame.image.load('sprites/catalog.png')
catalogX = 0
catalogY = 600
#Cynthia
cynthia = pygame.image.load("npc/Cynthia.png")
cynthiaX = 260
cynthiaY = 70

#Cynthia Text
cynthia_text = myfont.render("Good morning big brother! Breakfast is ready, go to the kitchen", True, black)
cynthia_name =  myfont.render("-Cynthia", True, black)

while game:
    screen.fill((0,0,0))
    #background image load
    screen.blit(background,(0,0))
    #Cynthia
    screen.blit(cynthia,(cynthiaX,cynthiaY))
    for event in pygame.event.get():          
        # if keystroke is pressed check whether its right or left
          if event.type == pygame.KEYDOWN:
            #Ragequit
            if event.key == pygame.K_ESCAPE:
                level_tutorial  = False
                time.sleep(1)
                pygame.quit() 
            #Left 
            if event.key == pygame.K_LEFT:
                playerX_change = -7
                left = True
                right = False
                up = False
                down = False
            #Right
            if event.key == pygame.K_RIGHT:
                playerX_change = 7
                left = False
                right = True
                up = False
                down = False

            #Up
            if event.key == pygame.K_UP:
                playerY_change = 7
                left = False
                right = False
                up = True
                down = False
             #Down
            if event.key == pygame.K_DOWN:
                playerY_change = -7
                left = False
                right = False
                up = False
                down = True
            #Sprint 
            if event.key == pygame.K_LSHIFT:
                sprint()                          

          if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0
                left = False
                right = False
                up = False
                down = False
                walkCount = 0

             
    #MOVEMENT X AND Y
    playerX += playerX_change
    playerY -= playerY_change

    #Stops the player from going out of bounds
    #X Position 1200
    if playerX <= 45:
        playerX = 45
    elif playerX >= 525:
        playerX = 525
    #Y Position 900
    if playerY <= 0:
        playerY = 0
    elif playerY >= 335:
        playerY = 335


    #Cynthia interaction checker
    #if playerX >= 460 and playerX <= 575 and playerY >= 204 and playerY <= 290:
       # if event.key == pygame.K_RETURN:
            #screen.blit(catalogImg,(catalogX,catalogY))
            #screen.blit(cynthia_text , (100, 630))
            #screen.blit(cynthia_name , (900, 725))

    #Level2
    if playerX >= 320 and playerX <= 420 and playerY >= 0 and playerY <= 70:
        game  = False
        main_room = True

    print("X:",playerX,"Y",playerY)
    screen.blit(framerate(), (10,0))
    hearts()
    clock.tick(60)
    gameWindow()

main_room = True
main_room_background = pygame.image.load('sprites/main_room.png')

while main_room:
    screen.fill((0,0,0))
    #background image load
    screen.blit(main_room_background,(0,0))
    #Hearts 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            time.sleep(1)
            pygame.quit() 
               
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
          #Left 
          if event.key == pygame.K_LEFT:
                playerX_change = -7
                left = True
                right = False
                up = False
                down = False
          #Right
          if event.key == pygame.K_RIGHT:
                playerX_change = 7
                left = False
                right = True
                up = False
                down = False
          #Up
          if event.key == pygame.K_UP:
                playerY_change = 7
                left = False
                right = False
                up = True
                down = False
          #Down
          if event.key == pygame.K_DOWN:
                playerY_change = -7
                left = False
                right = False
                up = False
                down = True
         #Sprint 
          if event.key == pygame.K_LSHIFT:
              sprint()                      

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0
                left = False
                right = False
                up = False
                down = False
                walkCount = 0
    #Stops the player from going out of bounds
    #X Position 1200
    if playerX <= 102:
        playerX = 102
    elif playerX >= 1050:
        playerX = 1050
    #Y Position 900
    if playerY <= -6:
        playerY = -6
    elif playerY >= 737:
        playerY = 737
    #Kitchen Collisions
    if playerY >= -6 and playerY <= 92 and playerX >= 101 and playerX <= 480:
        playerY = 96
    #Kitchen Wall Right collision
    if playerY >= -6 and playerY <= 285 and playerX >= 479 and playerX <= 673:
        playerX = 673
    #Kitchen Wall Left collision
    if playerY >= 96 and playerY <= 285 and playerX >= 470 and playerX <= 478:
        playerX = 471
    #Kitchen collision bottom
    if playerY >= 299 and playerY <= 36 and playerX >= 568 and playerX <= 582:
        playerY = 373

    #BASEMENT
    if playerY >= 430 and playerY <= 610 and playerX >= 1000:
        main_room = False
        basement = True

    #MOVEMENT X AND Y 
    playerX += playerX_change
    playerY -= playerY_change
    
    screen.blit(framerate(), (10,0))
    clock.tick(60)
    gameWindow()
