# COPYRIGHT 2020-2021 version 0.0.4
import pygame, sys, os, json, random  # Libraries
from pygame import mixer
from data.engine import *
pygame.init()
screen = pygame.display.set_mode((640, 480))  # Setup screen
clock = pygame.time.Clock()
pygame.display.set_caption("John's Adventure  v0.0.412 Demo")
icon = pygame.image.load('data/ui/logo.ico')
pygame.display.set_icon(icon)
black = (0, 0, 0)  # Color black
red = (255, 0, 0)
lime = (0, 255, 0)
Pixel_font = pygame.font.Font("data/fonts/pixelfont.ttf", 18)
menu_background = pygame.image.load('data/sprites/mainmenu.png')
cursor = pygame.image.load('data/ui/j_g_mouse.png')
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
music_list = [mixer.Sound("data/sound/forest_theme_part1.flac"),  #0
              mixer.Sound("data/sound/home_theme.flac"), #1
              mixer.Sound("data/sound/forest_theme.flac"), #2 
              mixer.Sound("data/sound/dramatic.flac"), #3 
              mixer.Sound("data/sound/press_start_sound.wav")
              ]
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
canChange, paused = False, False
menu, sword_Task = True, True
player_equipped, interactable, readNote, task_3, dummie_task = False, False, False, False, False
john_room, kitchen, basement = False, False, False  # Chunks & World Values
route1, route2, route3, route4, training_field, manosHut, credits_screen = False, False, False, False, False, False, False
john_room = True  # [The world] you want to start with
# VALUES
playerX, playerX_change = 0, 0
playerY, playerY_change = 0, 0
health = 100
walking = False
attacking = False
idling = True
cooldown = 0
player_hitbox = pygame.image.load('data/items/hitbox.png')
player_rect = player_hitbox.get_rect()

world_value, counter = 0, 0  # spawn points, counter
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
    pygame.image.load('data/items/wooden_sword_left.png')
]

attack_down = [pygame.image.load('data/sprites/player/playerdown1.png'),
               pygame.image.load('data/sprites/player/playerdownattack1.png'),
               pygame.image.load('data/sprites/player/playerdownattack2.png')]

attack_up = [pygame.image.load('data/sprites/player/playerup1.png'),
             pygame.image.load('data/sprites/player/playerupattack1.png'),
             pygame.image.load('data/sprites/player/playerupattack2.png')]



attack_right = [pygame.image.load('data/sprites/player/playerright1.png'),
                pygame.image.load('data/sprites/player/playerrightattack1.png'),
                pygame.image.load('data/sprites/player/playerrightattack2.png')]

attack_left = [ pygame.image.load('data/sprites/player/playerleft1.png'),
                pygame.image.load('data/sprites/player/playerleftattack1.png'),
                pygame.image.load('data/sprites/player/playerleftattack2.png')]



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
    global playerX, playerY, player_equipped
    if LeftIdle:
        swordRect.center = (playerX - 16, playerY + 35)
        screen.blit(sword_Image, swordRect)
    elif RightIdle:
        swordRect.center = (playerX + 80, playerY + 35)
        screen.blit(sword_Image, swordRect)
    elif DownIdle:
        swordRect.center = (playerX + 35, playerY + 80)
        screen.blit(sword_Image, swordRect)
    elif UpIdle:
        swordRect.center = (playerX + 32, playerY - 25)
        screen.blit(sword_Image, swordRect)  
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
    global playerX, playerY, playerX_change, playerY_change, walkCount, walking, attacking, idling, cooldown
    global LeftIdle, RightIdle, UpIdle, DownIdle, left, right, up, down
    global interactable, currency, attackEnemy, counter, paused, interact_value
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # KEYBOARD INPUT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                walking = True
                idling, attacking = False, False
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
            else:
                interactable = False

            #  Player attack
            if event.key == pygame.K_LSHIFT:            
                if not walking:
                    attacking = True
                counter = 0
                cooldown = 2000 #Delay of the attack
            else:
                attacking = False

        # When user stops doing a key input
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change, playerY_change = 0, 0
                left, right, up, down = False, False, False, False
                walking = False
                idling = True
                walkCount = 0
            if event.key == pygame.K_LEFT:
                LeftIdle = True
                DownIdle, RightIdle, UpIdle = False, False, False      
            if event.key == pygame.K_RIGHT:
                RightIdle = True
                DownIdle, LeftIdle, UpIdle = False, False, False             
            if event.key == pygame.K_UP:
                UpIdle = True
                DownIdle, RightIdle, LeftIdle = False, False, False     
            if event.key == pygame.K_DOWN:
                DownIdle = True
                LeftIdle, RightIdle, UpIdle = False, False, False                    
def gameWindow():  # This function is responsible for player's animation
    global walkCount, walking, attacking, idling, counter, cooldown, player_equipped,  attackEnemy
    global left, right, up, down

    if walkCount + 1 >= 27:
        walkCount = 0
    if walking:
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
        if idling:
            if LeftIdle:
                screen.blit(walkLeft[0], (playerX, playerY))
            elif RightIdle:
                screen.blit(walkRight[0], (playerX, playerY))
            elif UpIdle:
                screen.blit(walkUp[0], (playerX, playerY))
            elif DownIdle:
                screen.blit(playerImg, (playerX, playerY))
   
    if player_equipped:
        if cooldown == 0:
            attacking = False   
            idling = True
            attack = False
            attackEnemy = True

        if attacking:  # Attacking Mode turns on
            attack = True # Player starts attacking
            if walkCount + 1 >= 26: # Stuff when player finishes attacking                            
                while cooldown > 1:
                    cooldown -= 10                                                 
            walking, idling = False, False    
            if attack:        
                if LeftIdle or DownIdle or UpIdle or RightIdle:
                    hitbox()
                if LeftIdle: 
                    screen.blit(attack_left[walkCount // 9], (playerX - 5, playerY))
                    walkCount += 1
                elif RightIdle:
                    screen.blit(attack_right[walkCount // 9], (playerX, playerY))
                    walkCount += 1
                elif UpIdle:
                    screen.blit(attack_up[walkCount // 9], (playerX, playerY - 5))
                    walkCount += 1
                elif DownIdle:
                    screen.blit(attack_down[walkCount // 9], (playerX, playerY))
                    walkCount += 1
def player():
    global playerX, playerY
    gameWindow()  # Player
    hearts()  # Player UI
    controls()  # Player Controls
    player_pocket()
    player_rect.center = (playerX + 32, playerY + 40)
    screen.blit(player_hitbox, player_rect)
def sword_task(posX, posY):
    global catalogImg, playerY, playerX, interactable, sword_Task, player_equipped, interact_value, pl
    sword = pygame.image.load('data/items/wooden_sword_item.png')
    rotate_sword = pygame.transform.rotate(sword, 90)
    sword_text = Pixel_font.render("Take sword?", True, (0,0,0))
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
                sword_text = Pixel_font.render("You took the sword.", True, (0,0,0))
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

# Classes
coin_storage = []

class dummy(object):

    def __init__(self, x, y): # Initialize the dummy
        self.x = x
        self.y = y 
        self.hp = 100 # Health
        self.showHPbar = False
        self.counter = 0
        self.coinCount = 0
        self.attacked = False

    def update(self, sword_rect):
        global counter, coin_storage, dummie_task, cooldown
        dummyImg = pygame.image.load('data/npc/training_dummie.png')
        dummyRect = dummyImg.get_rect()
        dummyRect.center = (self.x, self.y) # Position of the dummy
        self.Hit = mixer.Sound('data/sound/sword_hit.flac')
        
        if dummyRect.collidepoint(sword_rect[0], sword_rect[1]):    
            self.showHPbar = True # Show HP bar
            self.attacked = True
            while counter < 1 and self.hp > 0 and cooldown <= 0:  # Play a sound on hit, decrease hp
                self.hp -= 10
                self.Hit.play() # Plays sound
                counter += 1 
            attacked = False

        if self.hp <= 0 : # if THE DUMMY IS DEAD, turn off the hp bar
            self.showHPbar = False        
            screen.blit(pygame.image.load('data/npc/broken_dummie.png'), dummyRect) # Broken dummy
            for i in range(3): # Drops 3 coins
                ranX = random.randint(self.x - 30, self.x + 30) # Random number around dummy's x
                ranY = random.randint(self.y - 30, self.y + 30) # Random number around dummy's y
                coin_storage.append(coin_system(ranX, ranY)) # append the positions     
            coin_storage[0].update(player_rect) # Spawn coin.
            coin_storage[1].update(player_rect) # Spawn coin.
            coin_storage[2].update(player_rect) # Spawn coin.
            dummie_task = True # Completed your first mission
           
        else: # Dummy is stil alive  
             screen.blit(dummyImg, dummyRect)
                              
        if self.showHPbar:
                pygame.draw.rect(screen, ( 0, 0, 0), (self.x - 49,self.y - 60, 102, 10))  # black bar
                pygame.draw.rect(screen, (255, 0, 0), (self.x - 49,self.y - 59, 100, 8))  # red bar
                pygame.draw.rect(screen, (0, 255, 0), (self.x - 49,self.y - 59, self.hp, 8))  # lime bar    

chests = [
    chest(), #0 johns room
    chest(), #1 Route 2
    chest()  #2 Manos Hut 
]  


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
        background = pygame.image.load('data/sprites/world/Johns_room.png')
        screen.blit(background, (0, 0))  # Display the background image
        mau()  # Spawn Mau the grey cat
        chests[0].update(400, 105,interactable, player_rect)
        player(), pause_menu()  # Player

        #Downstairs collision
        if playerX >= 440 and playerX <= 530 and playerY >= 60 and playerY <= 120:
            catalog_bubble("Wanna go downstairs?")
            if interactable:
                john_room, kitchen = False, True

        # Out of bounds collisions
        if playerY <= 40: 
            playerY = 40
        elif playerY >= 410:
            playerY = 410

        if playerX <= 100:  
            playerX = 100
        elif playerX >= 580:
            playerX = 580

        #Computer collisions
        if playerX > 510 and playerX < 515 and playerY >= 160:
            playerX = 510
        if playerX >= 515  and playerY >= 160 and playerY <= 165:
           playerY = 160

        # Desks collisions
        if playerX < 280 and playerY <= 130:
            playerY = 130
        if playerX >= 280 and playerX <= 285 and playerY <= 130:
            playerX = 285

        # Chest collisions
        if playerX >= 340 and playerX <= 400 and playerY <= 80:
            playerY = 80 # Bottom
        if playerX >= 335 and playerX <= 340 and playerY <= 80:
            playerX = 335 # Left
        if playerX >= 400 and playerX <= 410 and playerY <= 80:
            playerX = 410 # Right
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
                if interactable:
                    music_list[1].stop()
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
        background = pygame.image.load('data/sprites/world/basement.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        player(), pause_menu(), sword_task(100, 25)
        if playerY >= 270 and playerX <= 20:  # Collision checking & World change
            catalog_bubble("Go back to kitchen?")
            if interactable:
                basement, kitchen, world_value = False, True, 5
        if playerY <= 65 and playerX >= -10 and playerY <= 520:  # Furniture Collisions
            playerY = 65
        if playerY >= 0 and playerY <= 360 and playerX >= 355:
            playerX = 355
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
        if readNote:
            music_list[2].stop()
        else:
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
                if task_3 :
                    music_list[3].play(-1)
                else:
                    music_list[1].play(-1)
                
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
        chests[1].update(530, 410,interactable, player_rect)
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
        if playerY >= 400 and playerX >= 95: # Get to route 4
            route3, route4, world_value = False, True, 0
        elif playerX <= 10 and playerY < 295 and playerY >= 150: # Get to route 2
            route3, route2, world_value = False, True, 1
        if playerX >= 465: # Just a simple collision
            playerX = 465
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
        chests[2].update(580, 300,interactable, player_rect) # Mano's hut chest
        out_of_bounds()
        candy(90, 240, playerX, playerY, 1)  # Cat npc
        manos(280, 160, playerX, playerY, dummie_task, 1, interact_value),player()
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
        if playerY <= 10 and playerX <= 465:
            route3, route4, world_value = True, False, 2
        if playerX <= 90:
            playerX = 90

        if playerY >= 130 and playerY <= 175 and playerX <= 95:
            if interactable:
                catalog_bubble("OUT OF ORDER")
        if playerY > 175 and playerY < 270 and playerX <= 95:
            if interactable:
                catalog_bubble("You can't get in for now.")
        if playerY >= 270 and playerY <= 320 and playerX <= 95:
            if interactable:
                catalog_bubble("OUT OF ORDER")
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
        Dummy = dummy(385,290)
    while training_field:
        background = pygame.image.load('data/sprites/world/training_field.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        blacksmith_shop()
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
            Dummy.update(swordRect)# Training Dummie  
            
        player()  # Player
        blacksmith_col(), pause_menu(), out_of_bounds()
        if playerX <= 10:
            route4, training_field,  world_value = True, False, 2
            if dummie_task:
                task_3 = True
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
