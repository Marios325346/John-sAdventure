# COPYRIGHT 2020-2021 version 0.0.378
import pygame, sys # Libraries
from pygame import mixer
from data.engine import *
pygame.init()
screen = pygame.display.set_mode((640, 480))  # Setup screen
clock = pygame.time.Clock()
pygame.display.set_caption("John's Adventure  v0.0.378")
icon = pygame.image.load('data/ui/logo.ico')
pygame.display.set_icon(icon)
black = (0, 0, 0)  # Color black
red = (255, 0, 0)
lime = (0, 255, 0)
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

# main_theme = mixer.Sound("data/sound/forest_theme.flac") # Background music
# main_theme.play(-1)
def framerate():
    fps = str(int(clock.get_fps()))
    fps_text = Pixel_font.render(fps, 1, pygame.Color("yellow"))
    return fps_text
exitImg = pygame.image.load('data/ui/exit_button.png')
def exit_button():
    global exitImg, canChange
    exitBtn = exitImg.get_rect()
    exitBtn.center = (522, 138)
    if exitBtn.collidepoint(pygame.mouse.get_pos()):
        exitImg = pygame.image.load('data/ui/exit_button_hover.png')
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                canChange = False
    else:
        exitImg = pygame.image.load('data/ui/exit_button.png')

    screen.blit(exitImg, exitBtn)
settingsUI = pygame.image.load('data/ui/settings_screen.png')
setUIRect = settingsUI.get_rect()
setUIRect.center = (320, 250)
muteImg = [pygame.image.load('data/ui/unmuted.png'), pygame.image.load('data/ui/muted.png')]
muteRect = muteImg[0].get_rect()
muteRect.center = (140, 150)
unmuted = False
def settings_catalog():
    global settingsUI, setUIRect, unmuted, counter

    if muteRect.collidepoint(pygame.mouse.get_pos()):
        counter = 0
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                while counter <= 1 and not unmuted:
                    unmuted = True
                    counter += 1
                    # main_theme.stop()

    screen.blit(settingsUI, setUIRect)
    if unmuted:
        screen.blit(muteImg[1], muteRect)
    else:
        screen.blit(muteImg[0], muteRect)
canChange = False
menu = True
while menu:
    screen.fill((0, 0, 0))
    # background image load
    screen.blit(menu_background, (1, 1))
    #StartSound = mixer.Sound("data/sound/button_Sound.wav")

    # Play Button
    if playButton.collidepoint(pygame.mouse.get_pos()):
        playImg = pygame.image.load('data/ui/button interface hover.png')
        #  StartSound.set_volume(0.05)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu = False
                #StartSound = mixer.Sound("data/sound/press_start_sound.wav")
                #StartSound.play()
                game = True
    else:
        playImg = pygame.image.load('data/ui/button interface.png')

    # Settings
    if settingsButton.collidepoint(pygame.mouse.get_pos()):
        settingsImg = pygame.image.load('data/ui/settings_hover.png')
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                canChange = True
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

    # When player clicks settings
    if canChange:
        settings_catalog()
        exit_button()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    screen.blit(cursor, (pygame.mouse.get_pos()))
    pygame.display.update()

walkCount = 0  # Player Animation Counter
walkRight = [pygame.image.load('data/sprites/player/playerright1.png'), pygame.image.load('data/sprites/player/playerright2.png'), pygame.image.load('data/sprites/player/playerright1.png')]  # Walk Right
walkLeft = [pygame.image.load('data/sprites/player/playerleft1.png'), pygame.image.load('data/sprites/player/playerleft2.png'), pygame.image.load('data/sprites/player/playerleft1.png')]  # Walk Left
walkUp = [pygame.image.load('data/sprites/player/playerup1.png'),pygame.image.load('data/sprites/player/playerup2.png'), pygame.image.load('data/sprites/player/playerup1.png')]  # Walk Up
walkDown = [pygame.image.load('data/sprites/player/playerdown1.png'),pygame.image.load('data/sprites/player/playerdown2.png'), pygame.image.load('data/sprites/player/playerdown1.png')]  # Walk Down

LeftIdle, RightIdle, UpIdle, DownIdle = False, False, False, True
left, right, down, up = False, False, False, False
def controls(): # Player Controls
    global playerX, playerY, playerX_change, playerY_change, walkCount
    global LeftIdle, RightIdle, UpIdle, DownIdle, left, right, up, down
    global interactable, currency, attackEnemy, counter

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Detect Key inputs
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
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            #  Player Interact
            if event.key == pygame.K_RETURN:
                interactable = True
            else:
                interactable = False

            #  Player attack
            if event.key == pygame.K_LSHIFT:
                attackEnemy = True
                hitbox()
                counter = 0
            else:
                attackEnemy = False

        # When user stops doing a key input
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change = 0
                playerY_change = 0
                left, right, up, down = False, False, False, False
                LeftIdle = True
                DownIdle, RightIdle, UpIdle = False, False, False
                walkCount = 0

            if event.key == pygame.K_RIGHT:
                playerX_change = 0
                playerY_change = 0
                left, right, up, down = False, False, False, False
                RightIdle = True
                DownIdle, LeftIdle, UpIdle = False, False, False
                walkCount = 0

            if event.key == pygame.K_UP:
                playerX_change = 0
                playerY_change = 0
                left, right, up, down = False, False, False, False
                UpIdle = True
                DownIdle, RightIdle, LeftIdle = False, False, False
                walkCount = 0
            if event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0
                left, right, up, down = False, False, False, False
                DownIdle = True
                LeftIdle, RightIdle, UpIdle = False, False, False
                walkCount = 0# Controls fefe


sword_Image = pygame.image.load("data/items/hitbox.png")
swordRect = sword_Image.get_rect()
def hitbox():
    global up, down, left, right, playerX, playerY
    if left or LeftIdle:
        swordRect.center = (playerX - 16, playerY + 35)
        screen.blit(sword_Image, swordRect)
    elif right or RightIdle:
        swordRect.center = (playerX + 80, playerY + 35)
        screen.blit(sword_Image, swordRect)
    elif down or DownIdle:
        swordRect.center = (playerX + 30, playerY + 80)
        screen.blit(sword_Image, swordRect)
    elif up or UpIdle:
        swordRect.center = (playerX + 30, playerY - 25)
        screen.blit(sword_Image, swordRect)
    return swordRect

def gameWindow():  # This function is responsible for player's animation
    global walkCount
    global left, right, up, down
    global upAttack, downAttack, leftAttack, rightAttack
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
        if LeftIdle:
            screen.blit(walkLeft[0], (playerX, playerY))
        elif RightIdle:
            screen.blit(walkRight[0], (playerX, playerY))
        elif UpIdle:
            screen.blit(walkUp[0], (playerX, playerY))
        elif DownIdle:
            screen.blit(playerImg, (playerX, playerY))

catalogImg = pygame.image.load('data/sprites/catalog.png').convert()
def stairs_catalog():
    global catalogImg, game, john_room, kitchen, interactable
    text = Pixel_font.render("Go downstairs?", True, (255, 255, 255))
    if playerX >= 440 and playerX <= 530 and playerY >= 60 and playerY <= 120:
        screen.blit(catalogImg, (100, 340))
        screen.blit(text, (120, 350))
        if interactable:
            john_room = False
            kitchen = True
def manos_hut():
    global playerX, playerY, interactable, route3, manosHut, world_value, readNote
    if playerX >= 80 and playerX <= 470 and playerY >= 80 and playerY <= 85:
        playerY = 85
    if playerX >= 70 and playerX < 80 and playerY < 85:
        playerX = 70
    if playerY < 85 and playerX > 470 and playerX <= 490:
        playerX = 490

    if playerY < 90 and playerX > 255 and playerX < 305:
        if dummie_task and task_3 and readNote:
            catalog_bubble('Get inside?')
            if interactable:
                route3, manosHut = False, True
                world_value = 0
        else:
            catalog_bubble('This place is locked')

sword_Task = True
def sword_task(posX, posY):
    global catalogImg, playerY, playerX, interactable, sword_Task, player_equipped
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
                player_equipped = True  # Player has globally his equipment

    return posX, posY


def blacksmith_col():  # Blacksmith collisions
    global playerX, playerY
    if playerY <= 70 and playerX >= 320:
        playerX = 320
    if playerY > 70 and playerY <= 80 and playerX > 320:
        playerY = 80
        catalog_bubble('Shop is currently closed')

dummieImg = pygame.image.load('data/npc/training_dummie.png')
dummieRect = dummieImg.get_rect()
counter = 0
health = 100
showHp = False
def training_dummie(x, y):
    global catalogImg, dummieImg, dummie_task, counter, health, showHp
    dummieRect.center = (x, y)

    if showHp:
        pygame.draw.rect(screen, black, (x - 49, y - 60, 102, 10))  # black bar
        pygame.draw.rect(screen, red, (x - 49, y - 59, 100, 8))  # red bar
        pygame.draw.rect(screen, lime, (x - 49, y - 59, health, 8))  # lime bar

    if dummieRect.collidepoint(swordRect[0], swordRect[1]):
        if attackEnemy:
            while counter < 1 and health > 0:  # Play a sound on hit, decrease hp, and hit vfx
                health -= 10
                counter += 1
            showHp = True
            print("Dummie HP:", health)
    if health <= 0:
        dummieImg = pygame.image.load('data/npc/broken_dummie.png')
        dummie_task = True
    else:
        dummieImg = pygame.image.load('data/npc/training_dummie.png')
    screen.blit(dummieImg, dummieRect)


def status():
    print('___________________W O R L D S___________________')
    print('| Johns room:' + str(john_room), '       Route 1:' + str(route1), '         |')
    print('| Kitchen:' + str(kitchen), '          Route 2:' + str(route2), '        |')
    print('| Basement:' + str(basement), '         Route 3:' + str(route3), '        |')
    print('| Training Field:' + str(training_field), '   Route 4:' + str(route4), '        |')
    print('|_____________________TASKS_____________________|')
    print('|  Tutorial:' + str(player_equipped) + '          Dummie: False        |')
    print('|  Cynthia note: None      Manos Hut: None      |')
    print('|  Credits: None                                |')
    print('|_______________________________________________|')


def out_of_bounds():
    global playerX, playerY
    if playerX <= 5:
        playerX = 5
    elif playerX >= 580:
        playerX = 580
    if playerY <= 10:
        playerY = 10
    elif playerY >= 410:
        playerY = 410

playerImg = pygame.image.load('data/sprites/player/playeridle.png')  # Player
playerX_change = 0
playerY_change = 0
playerX = 0
playerY = 0

# Main loop
player_equipped = False
attackEnemy = False
john_room, kitchen, basement = False, False, False  # Chunks & World Values
route1, route2, route3, route4, training_field, manosHut = False, False, False, False, False, False
world_value = 0  # Very important for place position between worlds
route1 = True  # The world you want to start with (Pretty useful to check maps faster)
counter = 0
currency = 0  # Player's bank  pls dont hack it brooo :((((((((((((((((
i = 0
j = 0
dummie_task = False  # Tasks
task_3 = False
readNote = False
while game:
    if john_room and world_value == 0:
        playerX = 150
        playerY = 150

    elif john_room and world_value == 1:
        playerX = 380
        playerY = 120
    while john_room:
        background = pygame.image.load('data/sprites/Johns_room.png')
        screen.blit(background, (0, 0))  # Display the background image
        gameWindow()  # Player
        hearts()  # Player UI
        stairs_catalog()  # Catalog when player gets the nearby stairs
        controls()  # Player Controls
        player_pocket(currency)
        mau()  # Spawn Mau the grey cat
        chest(400, 105, playerX, playerY, interactable)
        if playerX >= 360 and playerX <= 420 and playerY <= 105:
            playerY = 105
            if interactable:
                while i < 1:
                    currency += 40
                    i += 1
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

    if kitchen and world_value == 3:
        playerX = 280
        playerY = 350
    elif kitchen and world_value == 5:
        playerX = 480
        playerY = 320

    while kitchen:
        background = pygame.image.load("data/sprites/world/main_room.png")
        screen.blit(background, (0, 0))
        gameWindow()  # Player
        hearts()  # Player UI
        controls()  # Player controls
        player_pocket(currency)
        if dummie_task:
            cynthia_Note(playerX, playerY, interactable)
            if playerX < 190 and playerY > 130 and playerY < 190:
                readNote = True
        else:
            cynthia(350, 30, playerX, playerY)  # Cynthia NPC
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
        out_of_bounds()  # Out of bounds
        if playerX > 135 and playerX <= 145 and playerY <= 305:  # Table collisions
            playerX = 145
        if playerX < 145 and playerY < 315:
            playerY = 315
        if playerY <= 40 and playerX <= 245:  # Kitchen collision
            playerY = 40
        playerX += playerX_change  # Player X movement
        playerY -= playerY_change  # Player Y movement
        screen.blit(framerate(), (10, 0))
        screen.blit(cursor, (pygame.mouse.get_pos()))
        clock.tick(60)
        pygame.display.update()
        pygame.display.flip()

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
        player_pocket(currency)
        sword_task(135, 25)
        if playerY >= 270 and playerX <= 20:  # Collision checking & World change
            catalog_bubble("Go back to kitchen?")
            if interactable:
                basement = False
                kitchen = True
                world_value = 5
        if playerY <= 65 and playerX >= -10 and playerY <= 520:  # Furniture Collisions
            playerY = 65
        if playerY >= 0 and playerY <= 360 and playerX >= 520:
            playerX = 520
        if playerY >= 350 and playerX >= -20 and playerX <= 520:
            playerY = 350
        if playerX <= 5 and playerY <= 400:  # Out of bounds
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
        player_pocket(currency)
        if playerY <= 55 and playerX >= 270 and playerX <= 320:  # Return to john's house
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
        out_of_bounds()
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
        player_pocket(currency)
        out_of_bounds()  # Out of bounds
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
        if dummie_task:
            task_3 = True
    elif route3 and world_value == 3:
        playerY = 110
        playerX = 285
    while route3:
        background = pygame.image.load('data/sprites/world/route3.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        gameWindow()
        hearts()
        controls()
        player_pocket(currency)
        manos_hut()  # Manos hut with collisions and interfaces
        # Out of bounds
        out_of_bounds()
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

    if manosHut and world_value == 0:  # Player spawn in manos hut
        playerY = 360
    while manosHut:
        background = pygame.image.load('data/sprites/world/manos_hut.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        hearts()
        chest(580, 300, playerX, playerY, interactable)  # Spawns chest
        if playerX > 480 and playerY < 290:
            if interactable:
                while j < 1:
                    currency += 40
                    j += 1

        candy(90, 240, playerX, playerY, 1)  # Cat npc
        manos(280, 160, playerX, playerY, dummie_task, 1)  # Spawn Manos young master npc
        gameWindow()
        controls()
        player_pocket(currency)

        # print (playerX, playerY)

        if playerX >= 250 and playerX <= 365 and playerY > 380:
            catalog_bubble('Go outside?')
            if interactable:
                route3, manosHut = True, False
                world_value = 3

        # Room limits
        if playerY < 150 and playerX < 590:
            playerY = 150
        if playerX < 60:
            playerX = 60
        # Bed
        if playerX >= 480 and playerY < 240:
            playerX = 480
        if playerX > 480 and playerY > 240 and playerY < 260:
            playerY = 260
        # Sofa
        if playerY <= 320 and playerX > 200 and playerX < 210:
            playerX = 210
        if playerY <= 330 and playerX > 120 and playerX < 200:
            playerY = 330
        if playerY < 330 and playerX >= 110 and playerX < 120:
            playerX = 110

        out_of_bounds()  # Out of bounds
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
        player_pocket(currency)

        # Out of bounds
        out_of_bounds()

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

    if training_field:
        if world_value == 0:
            playerX = 50

    while training_field:
        background = pygame.image.load('data/sprites/world/training_field.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        blacksmith_shop()  # Blacksmith shop
        training_dummie(385, 290)  # Training Dummie
        hearts()

        if not task_3:
            candy(350, 120, playerX, playerY, 0)  # Cat npc
            manos(240, 100, playerX, playerY, dummie_task, 0)  # Spawn Manos young master npc
            # Manos collisions
            if playerX >= 195 and playerX <= 200 and playerY >= 70 and playerY <= 120:  # Left collision
                playerX = 195
            if playerY > 120 and playerY < 130 and playerX > 195 and playerX <= 270:  # Bottom collision
                playerY = 130
            if playerX > 270 and playerX <= 285 and playerY >= 70 and playerY <= 120:  # Right collision
                playerX = 285
            if playerX > 195 and playerX <= 270 and playerY >= 50 and playerY < 70:
                playerY = 50

        blacksmith_col()

        gameWindow()
        controls()
        player_pocket(currency)

        out_of_bounds()

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
