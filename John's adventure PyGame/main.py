#COPYRIGHT 2020-2021
#THE DEMO HAS BEEN DISCONTINUED DUE TO PERSONAL REASONS

import pygame
import random
import math
import time
import random
from pygame import mixer
from pygame import *

pygame.init()

#screen
screen = pygame.display.set_mode((1200,900))
clock = pygame.time.Clock()

#Logo 
pygame.display.set_caption("John's Adventure")
icon = pygame.image.load('items/logo.png')
pygame.display.set_icon(icon)

#Colors 
black = (0,0,0)

#Main menu
myfont = pygame.font.SysFont("Comic Sans Ms", 30)
title_font = pygame.font.SysFont("Comic Sans Ms", 84)
menu_background = pygame.image.load('mainmenu.png')

start_text = myfont.render("Press Enter to start the game", True, black)

#Background music
pygame.mixer.music.load("sound/home.mp3")
pygame.mixer.music.play(-1)

menu = True
while menu:
    screen.fill((0,0,0))
    #background image load
    screen.blit(menu_background,(0,0))
    for event in pygame.event.get():
       if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                menu = False
                StartSound = mixer.Sound("sound/press_start_sound.wav")
                StartSound.play()
                game = True
            elif event.key == pygame.K_ESCAPE:
                time.sleep(1)
                pygame.quit()   
    screen.blit(start_text , (400, 600))
    pygame.display.update()

#//-   T U T O R I A L    L E V E L   -\\#

#background
background = pygame.image.load('images/Johns_room.png')
# Player
#playerImg = pygame.image.load('playeridle.png') #Player must be sowhere around 128pixels (maybe)
playerImg = pygame.image.load('images/beta player.png') #Player must be sowhere around 128pixels (maybe)
playerX = 550
playerY = 400
playerX_change = 0
playerY_change = 0

#Hearts
heartImg = pygame.image.load('heart.png')
heartX = 25
heartY = 775
# Player Animation
walkCount = 0
#Walk Right
walkRight = [pygame.image.load('images/right/playerright1.png'),pygame.image.load('images/right/playerright2.png'),pygame.image.load('images/right/playerright3.png'),pygame.image.load('images/right/playerright4.png'),pygame.image.load('images/right/playerright5.png'),pygame.image.load('images/right/playerright6.png'),pygame.image.load('images/right/playerright7.png'),pygame.image.load('images/right/playerright8.png'),pygame.image.load('images/right/playerright1.png')]
#Walk Left
walkLeft = [pygame.image.load('images/left/playerleft1.png'),pygame.image.load('images/left/playerleft2.png'),pygame.image.load('images/left/playerleft3.png'),pygame.image.load('images/left/playerleft4.png'),pygame.image.load('images/left/playerleft5.png'),pygame.image.load('images/left/playerleft6.png'),pygame.image.load('images/left/playerleft7.png'),pygame.image.load('images/left/playerleft8.png'),pygame.image.load('images/left/playerleft1.png')]
#Walk Up
walkUp = [pygame.image.load('images/up/playerup1.png'),pygame.image.load('images/up/playerup2.png'),pygame.image.load('images/up/playerup3.png'),pygame.image.load('images/up/playerup4.png'),pygame.image.load('images/up/playerup5.png'),pygame.image.load('images/up/playerup6.png'),pygame.image.load('images/up/playerup7.png'),pygame.image.load('images/up/playerup8.png'),pygame.image.load('images/up/playerup9.png')]
#Walk Down
walkDown = [pygame.image.load('images/idle_animation/idle1.png'), pygame.image.load('images/idle_animation/idle1.png'), pygame.image.load('images/idle_animation/idle1.png')]
#Attack Animation
upAttack = [pygame.image.load('playerup1.png'), pygame.image.load('playerup2.png'),pygame.image.load('playerupattack1.png'),pygame.image.load('playerupattack2.png')]
downAttack = [pygame.image.load('playerdown1.png'),pygame.image.load('playerdown2.png'),pygame.image.load('playerdownattack1.png'),pygame.image.load('playerdownattack2.png')]
rightAttack = [pygame.image.load('playerright1.png'), pygame.image.load('playerright2.png'),pygame.image.load('playerrightattack1.png'),pygame.image.load('playerrightattack2.png')]
leftAttack= [pygame.image.load('playerleft1.png'), pygame.image.load('playerleft2.png'),pygame.image.load('playerleftattack1.png'),pygame.image.load('playerleftattack2.png')]
#Idle
playerIdle = [pygame.image.load('images/idle_animation/idle1.png'),pygame.image.load('images/idle_animation/idle2.png'),pygame.image.load('images/idle_animation/idle3.png'),pygame.image.load('images/idle_animation/idle4.png'),pygame.image.load('images/idle_animation/idle5.png'),pygame.image.load('images/idle_animation/idle6.png'),pygame.image.load('images/idle_animation/idle7.png'),pygame.image.load('images/idle_animation/idle8.png'),pygame.image.load('images/idle_animation/idle9.png')]
left = False
right = False
up = False
down = False


def hearts():
    global playerX
    global playerY
    global heartX
    global heartY
    
    heartX = playerX - 65
    heartY = playerY - 40
    if up:
        heartY = playerY - 50
    heartImg = pygame.image.load('heart.png')
    screen.blit(heartImg,(heartX,heartY))


def sword():
    global playerX
    global playerY
    global dummieX
    global dummieY
 
    swordX = playerX 
    swordY = playerY 

    if down:
        swordX = playerX + 5
        swordY = playerY + 50
        swordImg = pygame.image.load('images/sword_down.png')
        

    if right: 
        swordX = playerX + 100
        swordY = playerY + 5
        swordImg = pygame.image.load('images/sword_right.png')
        

    if up:
        swordX = playerX - 4
        swordY = playerY - 100
        swordImg = pygame.image.load('images/sword_up.png')

    if left:
        swordX = playerX - 100
        swordY = playerY + 10
        swordImg = pygame.image.load('images/sword_left.png')
    screen.blit(swordImg,(swordX,swordY))


#This function is responsible for player's animation
def gameWindow():
    global walkCount  
    if walkCount + 1 >= 27:
        walkCount = 0
    if left:  
      if event.key != pygame.K_z:
            screen.blit(walkLeft[walkCount//9], (playerX, playerY))
            walkCount += 1 


      #Left attack+
      if event.key == pygame.K_z:
            screen.blit(leftAttack[walkCount//9], (playerX, playerY))
            walkCount += 0
            #sword()
    elif right:
        if event.key != pygame.K_z:
            screen.blit(walkRight[walkCount//9], (playerX, playerY))
            walkCount += 1
        #Right attack
        if event.key == pygame.K_z:
            screen.blit(rightAttack[walkCount//9], (playerX, playerY))
            walkCount += 0
            #sword()
    elif up:
        if event.key != pygame.K_z:
            screen.blit(walkUp[walkCount//3], (playerX, playerY))
            walkCount += 1
        #Up attack
        if event.key == pygame.K_z:
            screen.blit(upAttack[walkCount//9], (playerX, playerY))
            walkCount += 0
            #sword()
    elif down:
        if event.key != pygame.K_z:
            screen.blit(walkDown[walkCount//9], (playerX, playerY))
            walkCount += 1
        #Down attack
        if event.key == pygame.K_z:
            playerY_change = 0
            screen.blit(downAttack[walkCount//9], (playerX, playerY))
            walkCount += 0
            #sword()             
    else:
         screen.blit(playerIdle[walkCount//3],(playerX, playerY))
         walkCount += 1
    #IT KINDA WORKS YALLL <3
    pygame.display.update()
 

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
catalogImg = pygame.image.load('images/catalog.png')
catalogX = 0
catalogY = 600
#Cynthia
cynthia = pygame.image.load("npc/Cynthia.png")
cynthiaX = 513
cynthiaY = 120
level_tutorial = True
#Cynthia Text
cynthia_text = myfont.render("Good morning big brother! Breakfast is ready, go to the kitchen", True, black)
cynthia_name =  myfont.render("-Cynthia", True, black)

while level_tutorial:
    screen.fill((0,0,0))
    #background image load
    screen.blit(background,(0,0))
    #Cynthia
    screen.blit(cynthia,(cynthiaX,cynthiaY))
    #Hearts 
    hearts()
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
    if playerX <= 85:
        playerX = 85
    elif playerX >= 990:
        playerX = 990
    #Y Position 900
    if playerY <= 0:
        playerY = 0
    elif playerY >= 625:
        playerY = 625
    #Johns bed collisions
    if playerX >= 85 and playerX <= 380 and playerY >= 150 and playerY <= 210:
        playerY = 200

    if playerX >= 350 and playerX <= 390 and playerY >= 210 and playerY <= 630:
        playerX = 390

    #Cynthia Collision
    #Cynthia's Bed
    if playerX >= 680 and playerX <= 990 and playerY >= 280 and playerY <= 650:
       playerX = 685
    if playerX >= 710 and playerX <= 1000 and playerY >= 254 and playerY <= 290:
       playerY = 250

    #Cynthia Bottom Collision (decent)
    if playerX >= 450 and playerX <= 575 and playerY >= 197 and playerY <= 204:
        playerY = 204
    #Cynthia Left Collision
    if playerX >= 408 and playerX <= 449 and playerY >= 43 and playerY <= 148:
        playerX = 408
    #Cynthia RightCollision
    if playerX >= 455 and playerX <= 600 and playerY >= 43 and playerY <= 148:
        playerX = 600
    #Cynthia Up Collision
    if playerX >= 450 and playerX <= 557 and playerY >= 0 and playerY <= 40:
        playerX = 557
    #Cynthia interaction checker
    if playerX >= 460 and playerX <= 575 and playerY >= 204 and playerY <= 290:
        if event.key == pygame.K_RETURN:
            screen.blit(catalogImg,(catalogX,catalogY))
            screen.blit(cynthia_text , (100, 630))
            screen.blit(cynthia_name , (900, 725))

    #Level2
    #Level2 collision
    if playerX >= 600 and playerX <= 800 and playerY >= 140 and playerY <= 160:
       playerY = 160
    if playerX >= 650 and playerX <= 800 and playerY >= 14 and playerY <= 126:
        level_tutorial  = False
        main_room = True
    # Framerate limiter
    clock.tick(60)
    gameWindow()

main_room = True
main_room_background = pygame.image.load('images/main_room.png')

while main_room:
    screen.fill((0,0,0))
    #background image load
    screen.blit(main_room_background,(0,0))
    #Hearts 
    hearts()
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
    clock.tick(60)
    gameWindow()

#BASEMENENT
playerX = 50
playerY = 600
basement_sprite = pygame.image.load("images/basement.png")

def dummie(dummieX,dummieY,health):
    global playerX
    global playerY
    #Sprite
    training_dummie = pygame.image.load("images/training dummy.png")
    dummieX = dummieX
    dummieY = dummieY
    health = health
    #Collisions
    if playerX >= dummieX - 80 and playerX <= dummieX:
        playerX = dummieX - 80
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                health -= 50
        #if swordX and Y is between dummie's X and Y do:                
            #gets damaged by 50 hp
            #health -= 50
            #Does 50-50 which is 0 and sets it a new value which is 0
            #health = health
    if health == 0:
        broken_dummie = pygame.image.load("images/broken dummie.png")
        #Draw
        screen.blit(broken_dummie,(dummieX,dummieY))       
    elif health > 0:
        screen.blit(training_dummie,(dummieX,dummieY))

while basement:
    #Sprite load
    screen.blit(basement_sprite,(0,0))
    hearts()
    #dummie(820,155,50)
    dummie(820,350,50)
    #dummie(820,545,50)

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
    #Stuff
    playerX += playerX_change
    playerY -= playerY_change
    clock.tick(60)
    gameWindow()