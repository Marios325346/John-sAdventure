# COPYRIGHT 2020-2021 version 0.0.4
import pygame, sys, os, json  # Libraries
from pygame import mixer
from data.engine import *
pygame.init()
screen = pygame.display.set_mode((640, 480))  # Setup screen
clock = pygame.time.Clock()
pygame.display.set_caption("John's Adventure  v0.0.4 Demo")
icon = pygame.image.load('data/ui/logo.ico')
pygame.display.set_icon(icon)
black = (0, 0, 0)  # Color black
red = (255, 0, 0)
lime = (0, 255, 0)
Pixel_font = pygame.font.Font("data/fonts/pixelfont.ttf", 18)
menu_background = pygame.image.load('data/sprites/mainmenu.png')
cursor = pygame.image.load('data/sprites/j_g_mouse.png')
pygame.mouse.set_visible(False)
playImg = pygame.image.load("data/ui/button interface.png").convert()
playButton = playImg.get_rect()
playButton.center = (320, 305)
quitImg = pygame.image.load("data/ui/quit.png").convert()
quitButton = quitImg.get_rect()
quitButton.center = (320, 445)
aboutImg = pygame.image.load('data/ui/about.png').convert()
aboutButton = aboutImg.get_rect()
aboutButton.center = (320, 375)
aboutUI = pygame.image.load('data/ui/about_screen.png')
aboutRect = aboutUI.get_rect()
aboutRect.center = (320, 250)
controller_value = pygame.joystick.get_init()
joysticks = []  # Initialize controller
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
for joystick in joysticks:
    joystick.init()
# 0: Left analog horizontal, 1: Left Analog Vertical, 2: Right Analog Horizontal
# 3: Right Analog Vertical 4: Left Trigger, 5: Right Trigger
analog_keys = {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: -1}
with open(os.path.join("data/controller_keys.json"), 'r+') as file:
    button_keys = json.load(file)
# MUSIC & SOUND
music_list = [mixer.Sound("data/sound/forest_theme_part1.flac"), mixer.Sound("data/sound/home_theme.flac"),
              mixer.Sound("data/sound/forest_theme.flac"), mixer.Sound("data/sound/press_start_sound.wav")]
for i in range(len(music_list)):
    music_list[i].set_volume(0.3)
# IMAGES
playerImg = pygame.image.load('data/sprites/player/playeridle.png')  # Player
sword_Image = pygame.image.load("data/items/hitbox.png")
swordRect = sword_Image.get_rect()
dummieImg = pygame.image.load('data/npc/training_dummie.png')
dummieRect = dummieImg.get_rect()
# BOOLEANS
LeftIdle, RightIdle, UpIdle, DownIdle = False, False, False, True
left, right, down, up = False, False, False, False
canChange, paused, showHp = False, False, False
menu, sword_Task = True, True
attackEnemy, player_equipped, interactable, readNote, task_3, dummie_task = False, False, False, False, False, False
john_room, kitchen, basement = False, False, False  # Chunks & World Values
route1, route2, route3, route4, training_field, manosHut, credits_screen = False, False, False, False, False, False, False
john_room = True  # [The world] you want to start with
# VALUES
playerX, playerX_change = 0, 0
playerY, playerY_change = 0, 0
health = 100
world_value, counter, currency = 0, 0, 0  # spawn points, counter, player currency
i, j, pl, walkCount, interact_value = 0, 0, 0, 0, 0  # Counters
# Lists
walkRight = [pygame.image.load('data/sprites/player/playerright1.png'),
             pygame.image.load('data/sprites/player/playerright2.png'),
             pygame.image.load('data/sprites/player/playerright1.png')]
walkLeft = [pygame.image.load('data/sprites/player/playerleft1.png'),
            pygame.image.load('data/sprites/player/playerleft2.png'),
            pygame.image.load('data/sprites/player/playerleft1.png')]
walkUp = [pygame.image.load('data/sprites/player/playerup1.png'),
          pygame.image.load('data/sprites/player/playerup2.png'),
          pygame.image.load('data/sprites/player/playerup1.png')]
walkDown = [pygame.image.load('data/sprites/player/playerdown1.png'),
            pygame.image.load('data/sprites/player/playerdown2.png'),
            pygame.image.load('data/sprites/player/playerdown1.png')]
wooden_sword = [
    pygame.image.load('data/items/wooden_sword_up.png'),
    pygame.image.load('data/items/wooden_sword_down.png'),
    pygame.image.load('data/items/wooden_sword_left.png'),
    pygame.image.load('data/items/wooden_sword_right.png')
]
# Functions
def framerate():
    fps = str(int(clock.get_fps()))
    fps_text = Pixel_font.render(fps, 1, pygame.Color("yellow"))
    return fps_text
def settings_catalog():
    global settingsUI, setUIRect, unmuted, counter
    text = Pixel_font.render("Welcome to John's Adventure!", True, (0, 0, 0))
    text2 = Pixel_font.render("Controls:", True, (0, 0, 0))
    controls = Pixel_font.render("UP/Down/Left/Right/Enter/Shift", True, (0, 0, 0))
    controller_guide = pygame.image.load('data/ui/controller_guide.png')
    screen.blit(aboutUI, aboutRect)
    screen.blit(text, (116, 190)), screen.blit(text2, (250, 225))
    screen.blit(controls, (100, 260)), screen.blit(controller_guide, (150, 300))
def exit_button():
    global canChange
    exitImg = pygame.image.load('data/ui/exit_button.png')
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
def hitbox():
    global up, down, left, right, playerX, playerY, player_equipped
    if left or LeftIdle:
        swordRect.center = (playerX - 16, playerY + 35)
        screen.blit(sword_Image, swordRect)
        if player_equipped:
            screen.blit(wooden_sword[2], (playerX - 60, playerY + 10))
    elif right or RightIdle:
        swordRect.center = (playerX + 80, playerY + 35)
        screen.blit(sword_Image, swordRect)
        if player_equipped:
            screen.blit(wooden_sword[3], (playerX + 15, playerY + 10))
    elif down or DownIdle:
        swordRect.center = (playerX + 30, playerY + 80)
        screen.blit(sword_Image, swordRect)
        if player_equipped:
            screen.blit(wooden_sword[1], swordRect)
    elif up or UpIdle:
        swordRect.center = (playerX + 30, playerY - 25)
        screen.blit(sword_Image, swordRect)
        if player_equipped:
            screen.blit(wooden_sword[0], swordRect)
    return swordRect
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
def controls():  # Player Controls
    global playerX, playerY, playerX_change, playerY_change, walkCount
    global LeftIdle, RightIdle, UpIdle, DownIdle, left, right, up, down
    global interactable, currency, attackEnemy, counter, paused, interact_value
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # CONTROLLER INPUT
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == button_keys['left_arrow']:
                playerX_change = -3
                left = True
                right, up, down = False, False, False
            if event.button == button_keys['right_arrow']:
                playerX_change = 3
                right = True
                up, left, down = False, False, False
            if event.button == button_keys['down_arrow']:
                playerY_change = -3
                down = True
                left, right, up = False, False, False
            if event.button == button_keys['up_arrow']:
                playerY_change = 3
                up = True
                down, right, left = False, False, False
            if event.button == button_keys['square']:
                attackEnemy = True
                hitbox()
                counter = 0
            else:
                attackEnemy = False
            if event.button == button_keys['x']:
                interactable = True
                if interact_value != 3:
                    interact_value += 1
                else:
                    interact_value = 1
            else:
                interactable = False
        if event.type == pygame.JOYBUTTONUP:
            if event.button == button_keys['left_arrow']:
                playerX_change = 0
                playerY_change = 0
                left, right, up, down = False, False, False, False
                LeftIdle = True
                DownIdle, RightIdle, UpIdle = False, False, False
                walkCount = 0
            if event.button == button_keys['right_arrow']:
                playerX_change = 0
                playerY_change = 0
                left, right, up, down = False, False, False, False
                RightIdle = True
                DownIdle, LeftIdle, UpIdle = False, False, False
                walkCount = 0
            if event.button == button_keys['down_arrow']:
                playerX_change = 0
                playerY_change = 0
                left, right, up, down = False, False, False, False
                DownIdle = True
                LeftIdle, RightIdle, UpIdle = False, False, False
                walkCount = 0
            if event.button == button_keys['up_arrow']:
                playerX_change = 0
                playerY_change = 0
                left, right, up, down = False, False, False, False
                UpIdle = True
                DownIdle, RightIdle, LeftIdle = False, False, False
                walkCount = 0
            if event.button == button_keys["options"]:
                paused = True
                # HANDLES ANALOG INPUTS
        # KEYBOARD INPUT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
                left = True
                right, up, down = False, False, False
            # Right
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
                right = True
                up, left, down = False, False, False
            # Up
            if event.key == pygame.K_UP:
                playerY_change = 3
                up = True
                down, right, left = False, False, False
            # Down
            if event.key == pygame.K_DOWN:
                playerY_change = -3
                down = True
                left, right, up = False, False, False
            if event.key == pygame.K_ESCAPE:
                paused = True
            #  Player Interact
            if event.key == pygame.K_RETURN:
                interactable = True

                if interact_value != 3:
                    interact_value += 1
                else:
                    interact_value = 1
                print(interact_value)
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
                walkCount = 0
def gameWindow():  # This function is responsible for player's animation
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
        if LeftIdle:
            screen.blit(walkLeft[0], (playerX, playerY))
        elif RightIdle:
            screen.blit(walkRight[0], (playerX, playerY))
        elif UpIdle:
            screen.blit(walkUp[0], (playerX, playerY))
        elif DownIdle:
            screen.blit(playerImg, (playerX, playerY))
def player():
    gameWindow()  # Player
    hearts()  # Player UI
    controls()  # Player Controls
    player_pocket(currency)
def sword_task(posX, posY):
    global catalogImg, playerY, playerX, interactable, sword_Task, player_equipped, interact_value, pl
    sword = pygame.image.load('data/items/wooden_sword_item.png')
    rotate_sword = pygame.transform.rotate(sword, 90)
    sword_text = Pixel_font.render("Take sword?", True, (255, 255, 255))
    if sword_Task:
        screen.blit(rotate_sword, (posX, posY))
    if playerX >= posX - 50 and playerX <= posX + 50 and playerY >= posY - 50 and playerY <= posY + 50:
        if interactable:
            screen.blit(catalogImg, (100, 340))
            while pl < 1:
                interact_value = 0
                pl += 1
            if interact_value < 1:
                screen.blit(sword_text, (120, 350))  # Text that asks if player wants to equip his sword
            else:
                sword_text = Pixel_font.render("You took the sword.", True, (255, 255, 255))
                player_equipped = True  # Player has globally his equipment
                sword_Task = False
                screen.blit(sword_text, (120, 350))
    return posX, posY
def blacksmith_col():  # Blacksmith collisions
    global playerX, playerY
    if playerY <= 70 and playerX >= 320:
        playerX = 320
    if playerY > 70 and playerY <= 80 and playerX > 320:
        playerY = 80
        catalog_bubble('Shop is currently closed')
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
    if health <= 0:
        dummieImg = pygame.image.load('data/npc/broken_dummie.png')
        dummie_task = True
    else:
        dummieImg = pygame.image.load('data/npc/training_dummie.png')
    screen.blit(dummieImg, dummieRect)
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
    elif route2:
        if playerY >= 290:
            playerY = 290
def pause_menu():
    global transparent_black, paused, playerX_change, playerY_change, interactable
    Pixel_fontL = pygame.font.Font("data/fonts/pixelfont.ttf", 36)
    text = Pixel_fontL.render('PAUSED', True, (255, 255, 255))
    text2 = Pixel_font.render('To continue press Enter or (X)', True, (255, 255, 255))
    if paused:
        playerX_change, playerY_change = 0, 0
        screen.blit(transparent_black, (0, 0))
        screen.blit(text, (220, 150))
        screen.blit(text2, (100, 300))
        if interactable:
            paused = False

if menu:
    music_list[0].play()
while menu:
    screen.fill((0, 0, 0))
    # background image load
    screen.blit(menu_background, (1, 1))
    controller(controller_value)
    # Play Button
    if playButton.collidepoint(pygame.mouse.get_pos()):
        playImg = pygame.image.load('data/ui/button interface hover.png')
        #  StartSound.set_volume(0.05)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu = False
                music_list[0].stop()
                # StartSound.play()
                game = True
    else:
        playImg = pygame.image.load('data/ui/button interface.png')
    # Settings
    if aboutButton.collidepoint(pygame.mouse.get_pos()):
        aboutImg = pygame.image.load('data/ui/about_hover.png')
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                canChange = True
    else:
        aboutImg = pygame.image.load('data/ui/about.png')
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
    screen.blit(aboutImg, aboutButton)
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
while game:
    if john_room and world_value == 0:
        playerX, playerY = 150, 150
        music_list[1].play(-1)
    elif john_room and world_value == 1:
        playerX, playerY = 420, 150
    while john_room:
        background = pygame.image.load('data/sprites/Johns_room.png')
        screen.blit(background, (0, 0))  # Display the background image
        mau()  # Spawn Mau the grey cat
        chest(400, 105, playerX, playerY, interactable)
        player(), pause_menu()  # Player
        if playerX >= 360 and playerX <= 420 and playerY <= 115:
            playerY = 115
            if interactable:
                while i < 1:
                    currency += 40
                    i += 1
        if playerX >= 440 and playerX <= 530 and playerY >= 60 and playerY <= 120:
            catalog_bubble("Wanna go downstairs?")
            if interactable:
                john_room, kitchen = False, True
        if playerX <= 100:  # John's room collisions
            playerX = 100
        elif playerX >= 580:
            playerX = 580
        if playerY <= 40:
            playerY = 40
        elif playerY >= 410:
            playerY = 410
        playerX += playerX_change  # Player X movement
        playerY -= playerY_change  # Player Y movement
        screen.blit(framerate(), (10, 0))
        screen.blit(cursor, (pygame.mouse.get_pos()))
        clock.tick(60)
        pygame.display.update()
    if kitchen and world_value == 3:
        playerX, playerY = 280, 350
    elif kitchen and world_value == 5:
        playerX, playerY = 480, 320
    while kitchen:
        background = pygame.image.load("data/sprites/world/main_room.png")
        screen.blit(background, (0, 0))
        player(), pause_menu(), out_of_bounds()
        if dummie_task:
            cynthia_Note(playerX, playerY, interactable)
            if playerX < 190 and playerY > 130 and playerY < 190:
                readNote = True
        else:
            cynthia(350, 30, playerX, playerY, interactable, interact_value)  # Cynthia NPC
        if playerY <= 50 and playerX >= 310 and playerX <= 400:
            playerX = 400
        if playerY >= 41 and playerY <= 90 and playerX >= 300 and playerX <= 380:
            playerY = 90
        if playerX <= 290 and playerX >= 280 and playerY <= 50:
            playerX = 280
        if playerY >= 260 and playerY <= 340 and playerX >= 510:  # Player interacts with basement's door
            catalog_bubble("Wanna go to basement?")
            if interactable:
                kitchen, basement = not kitchen, True
        elif playerX >= 503 and playerY <= 45:  # Player interacts with the stairs
            catalog_bubble("Wanna go to upstairs?")
            if interactable:
                kitchen, john_room, basement, world_value = False, True, False, 1
        elif playerY >= 370 and playerX >= 220 and playerX <= 320:  # Player interacts with the exit door
            if player_equipped:  # Checks if player has done task 1 which is to get his sword
                catalog_bubble("Want to go outside?")
                if interactable:
                    kitchen, route1, basement, world_value = False, True, False, 0
                    music_list[1].stop()
            else:
                catalog_bubble("Door is locked")
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
    if basement:
        playerX, playerY, pl = 80, 340, 0
    while basement:
        background = pygame.image.load('data/sprites/basement.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        player(), pause_menu(), sword_task(135, 25)
        if playerY >= 270 and playerX <= 20:  # Collision checking & World change
            catalog_bubble("Go back to kitchen?")
            if interactable:
                basement, kitchen, world_value = False, True, 5
        if playerY <= 65 and playerX >= -10 and playerY <= 520:  # Furniture Collisions
            playerY = 65
        if playerY >= 0 and playerY <= 360 and playerX >= 520:
            playerX = 520
        if playerY >= 350 and playerX >= -20 and playerX <= 520:
            playerY = 350
        if playerX <= 5 and playerY <= 400:  # Out of bounds
            playerX = 5
        playerX += playerX_change  # MOVEMENT X
        playerY -= playerY_change  # AND Y
        screen.blit(cursor, (pygame.mouse.get_pos()))
        screen.blit(framerate(), (10, 0))
        clock.tick(60)
        pygame.display.update()
    # ---------- OUTSIDE WORLD ---------
    if route1 and world_value == 0:
        playerX, playerY = 285, 70
        music_list[2].play(-1)
    elif route1 and world_value == 1:
        playerX = 550
    while route1:
        background = pygame.image.load('data/sprites/world/route1.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        player(), pause_menu(), out_of_bounds()  # Player
        if playerX <= 20:
            catalog_bubble('You have no access to this route')
        if playerY <= 55 and playerX >= 270 and playerX <= 320:  # Return to john's house
            catalog_bubble("Return home?")
            if interactable:
                route1, kitchen, basement, world_value = False, True, False, 3
                music_list[2].stop()
        if playerX >= 360 and playerY <= 65:  # Fence collision
            playerY = 65
        elif playerX <= 220 and playerY <= 65:
            playerY = 65
        if playerY <= 40 and playerX <= 245:
            playerY = 40
        if playerX >= 580 and playerY < 295:
            route1, route2, world_value = False, True, 0
        playerX += playerX_change  # MOVEMENT X
        playerY -= playerY_change  # AND Y
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
        player(), pause_menu(), out_of_bounds()  # Player
        chest(530, 410, playerX, playerY, interactable)
        if playerY <= 40 and playerX < 105:
            playerY = 40
        if playerY <= 40 and playerX >= 106 and playerX <= 115:
            playerX = 115
        if playerX >= 580 and playerY < 295:
            world_value, route2, route3 = 0, False, True  # World value, bool0 , bool1
        elif playerX <= 10 and playerY < 295:
            world_value, route2, route1 = 1, False, True
        if playerY < 150 and playerX > 200:
            playerY = 150
        if playerX > 190 and playerX <= 200 and playerY <= 150:
            playerX = 190
        playerX += playerX_change  # MOVEMENT X
        playerY -= playerY_change  # AND Y
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
        playerY, playerX = 110, 285
    while route3:
        background = pygame.image.load('data/sprites/world/route3.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        player(), pause_menu(), out_of_bounds(), manos_hut()  # Player
        if playerY >= 400:
            route3, route4, world_value = False, True, 0
        elif playerX <= 10 and playerY < 295 and playerY >= 150:
            route3, route2, world_value = False, True, 1
        playerX += playerX_change  # MOVEMENT X
        playerY -= playerY_change  # AND Y
        screen.blit(cursor, (pygame.mouse.get_pos()))
        screen.blit(framerate(), (10, 0))
        clock.tick(60)
        pygame.display.update()
    if manosHut and world_value == 0:  # Player spawn in manos hut
        playerY, interact_value, pl = 360, 0, 0
    while manosHut:
        background = pygame.image.load('data/sprites/world/manos_hut.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        chest(580, 300, playerX, playerY, interactable)  # Spawns chest
        if playerX > 480 and playerY < 290:
            if interactable:
                while j < 1:
                    currency += 40
                    j += 1
        out_of_bounds(), controls(),hearts(),player_pocket(currency)
        candy(90, 240, playerX, playerY, 1)  # Cat npc
        manos(280, 160, playerX, playerY, dummie_task, 1, interact_value),gameWindow()
        if playerX > 260 and playerX <= 300 and playerY >= 170 and playerY <= 180:
            interact_value, playerY = 0, 181
        if playerX >= 250 and playerX <= 365 and playerY > 380:
            catalog_bubble('Go outside?')
            if interactable:
                credits_screen, manosHut, world_value = True, False, 3
        if playerY < 150 and playerX < 590:  # Room limits
            playerY = 150
        if playerX < 60:
            playerX = 60
        if playerX >= 480 and playerY < 240:
            playerX = 480  # Bed
        if playerX > 480 and playerY > 240 and playerY < 260:
            playerY = 260
        if playerY <= 320 and playerX > 200 and playerX < 210:
            playerX = 210  # Sofa
        if playerY <= 330 and playerX > 120 and playerX < 200:
            playerY = 330
        if playerY < 330 and playerX >= 110 and playerX < 120:
            playerX = 110
        playerX += playerX_change  # MOVEMENT X
        playerY -= playerY_change  # AND Y
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
        player(), pause_menu(), out_of_bounds()
        if playerX >= 580:
            route4, training_field, world_value = False, True, 0
        if playerY <= 10:
            route3, route4, world_value = True, False, 2
        playerX += playerX_change  # MOVEMENT X
        playerY -= playerY_change  # AND Y
        screen.blit(cursor, (pygame.mouse.get_pos()))
        screen.blit(framerate(), (10, 0))
        clock.tick(60)
        pygame.display.update()
    if training_field:
        interact_value, pl = 0, 0
        if world_value == 0:
            playerX = 50
    while training_field:
        background = pygame.image.load('data/sprites/world/training_field.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        blacksmith_shop(), hearts(), player_pocket(currency)
        controls()
        if not task_3:
            candy(350, 120, playerX, playerY, 0)  # Cat npc
            manos(240, 100, playerX, playerY, dummie_task, 0, interact_value)  # Spawn Manos
            if playerX >= 195 and playerX <= 200 and playerY >= 70 and playerY <= 120:
                playerX = 195  # Left collision Manos
            if playerY > 120 and playerY < 130 and playerX > 195 and playerX <= 270:
                playerY, interact_value = 130, 0  # Bottom collision Manos
            if playerX > 270 and playerX <= 285 and playerY >= 70 and playerY <= 120:
                playerX = 285  # Right collision Manos
            if playerX > 195 and playerX <= 270 and playerY >= 50 and playerY < 70:
                playerY = 50
        gameWindow()  # Player
        if not task_3:
            training_dummie(385, 290)  # Training Dummie
        blacksmith_col(), pause_menu(), out_of_bounds()
        if playerX <= 10:
            route4, training_field,  world_value = True, False, 2
        playerX += playerX_change  # MOVEMENT X
        playerY -= playerY_change  # AND Y
        screen.blit(cursor, (pygame.mouse.get_pos()))
        screen.blit(framerate(), (10, 0))
        clock.tick(60)
        pygame.display.update()
    while credits_screen:
        screen.fill((0, 0, 0))
        controls()
        credits_text()
        screen.blit(cursor, (pygame.mouse.get_pos()))
        clock.tick(60)
        pygame.display.update()
