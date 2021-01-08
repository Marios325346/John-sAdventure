# COPYRIGHT 2020-2021 version 0.0.4
import pygame, sys, os, json, random  # Libraries
from pygame import mixer
pygame.init()
screen = pygame.display.set_mode((640, 480))  # Setup screen
clock = pygame.time.Clock()
pygame.display.set_caption("John's Adventure  v0.0.5 Semi-stable Chapter 1")
icon = pygame.image.load('data/ui/logo.ico')
pygame.display.set_icon(icon)
black = (0, 0, 0)  # Color black
red = (255, 0, 0)
lime = (0, 255, 0)
Pixel_font = pygame.font.Font("data/fonts/pixelfont.ttf", 14)
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
catalogImg = pygame.image.load('data/ui/catalog_bubble.png')
blacksmithImg = pygame.image.load('data/npc/blacksmith_shop.png')
blacksmithRect = blacksmithImg.get_rect()
blacksmithRect.center = (467, 60)
transparent_black = pygame.image.load("data/ui/black_overlay.png")
note = pygame.image.load('data/items/note.png')
cynthias_Note = pygame.image.load('data/items/cynthias_note.png')
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
music_list = [
    mixer.Sound("data/sound/forest_theme_part1.flac"),  #0
    mixer.Sound("data/sound/home_theme.flac"), #1
    mixer.Sound("data/sound/forest_theme.flac"), #2 
    mixer.Sound("data/sound/dramatic.flac"), #3 
    mixer.Sound("data/sound/Select_UI.wav") #4            
             ]
for i in range(len(music_list)):
    music_list[i].set_volume(0.3)
# IMAGES
playerImg = pygame.image.load('data/sprites/player/playeridle.png')  # Player
sword_Image = pygame.image.load("data/items/hitbox.png")
swordRect = sword_Image.get_rect()
# BOOLEANS
LeftIdle, RightIdle, UpIdle, DownIdle = False, False, False, True
left, right, down, up = False, False, False, False
canChange, paused = False, False
showCatalog = True
menu, sword_Task = True, True
player_equipped, interactable, readNote, task_3, dummy_task = False, False, False, False, False
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
music_counter = 0
player_hitbox = pygame.image.load('data/items/hitbox.png')
player_rect = player_hitbox.get_rect()
world_value, counter = 0, 0  # spawn points, counter
i, j, pl, walkCount, interact_value = 0, 0, 0, 0, 0  # Counters
y = 0
playCount, settingsCount, quitCount, menuCount = 0,0,0,0
player_money = 0 #  Currency
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

# Classes
class chest(object):

    def __init__(self): 
        self.isOpened = False   
        self.counter = 0
        self.value = 0
      
    def update(self, x, y, interactable, player_rect):
        global player_money
        self.x = x
        self.y = y
        #Images
        chestImg = pygame.image.load('data/sprites/chest.png')
        chestRect = chestImg.get_rect()
        chestRect.center = (self.x, self.y)

        if chestRect.collidepoint(player_rect[0] + 15, player_rect[1]):
            catalog_bubble("Helloo owooo")
            if interactable and not self.isOpened:  
                while self.counter < 1:
                    player_money += 40                   
                    self.counter += 1
                self.isOpened = True       
            if self.isOpened:
                if self.value == 0:
                    catalog_bubble("You found 40 coins")
                else:
                    catalog_bubble("The chest is now empty")
            else:
                catalog_bubble("Open the chest?")
                
        if not chestRect.collidepoint(player_rect[0] + 15, player_rect[1]) and self.isOpened:
            self.value += 1

        screen.blit(chestImg, chestRect)
class coin_system(object):

    def __init__(self,x,y): # Intialize the object and gives X, Y position
        self.x = x
        self.y = y
        self.coinCount = 0
        self.visibility = True
        self.currency = 0  # Value of the coin
         
    def update(self, player_rect):  # Updates the object's condition (Animation etc.)    
        global player_money
        # Sound
        self.PickupSound = mixer.Sound('data/sound/Pickup_Coin.wav')
        #Rect 1
        coin_hitbox = pygame.image.load('data/items/hitbox.png')
        hitbox_rect = coin_hitbox.get_rect()
        hitbox_rect.center = (self.x - 1 , self.y)      
        #Animation
        coin_anim = [
            pygame.image.load('data/items/coin1.png'),
            pygame.image.load('data/items/coin2.png'),
            pygame.image.load('data/items/coin3.png'),
            pygame.image.load('data/items/coin4.png'),
            pygame.image.load('data/items/coin5.png')
        ] 
        # Rect 2 for animation
        coin_rect = coin_anim[0].get_rect()
        coin_rect.center = (self.x, self.y)        
        # Conditions
        if self.coinCount >= 26:
           self.coinCount = 0             
           
        if hitbox_rect.collidepoint(player_rect[0] + 15, player_rect[1]) and self.visibility:
            self.PickupSound.play() # Plays sound
            self.currency +=1 #Player gets 1 coin
            player_money += self.currency #Adds it to players pocket
            self.visibility = False # The Coin disappears       

        if self.visibility: # If player hasn't touch the coin do this
            screen.blit(coin_anim[self.coinCount // 9], coin_rect)
            screen.blit(coin_hitbox, hitbox_rect)
            self.coinCount += 1
class cloud(object):

    def __init__(self,x,y):   
        self.x = x
        self.y = y 
        self.cloudSpeed = 0.05
        self.left = False
        self.right = False

    def update(self):
        cloudImg = pygame.image.load('data/ui/cloud.png') 

        if self.right:
             self.x = 650
        
        if self.left:
           self.x -= self.cloudSpeed

        if self.x < 650 and self.x <= -200:
            self.right = True
            self.left = False

        elif self.x >= 0:
            self.left = True
            self.right = False
        screen.blit(cloudImg, (self.x , self.y ))
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
        global counter, coin_storage, dummy_task, cooldown
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
            dummy_task = True # Completed your first mission
           
        else: # Dummy is stil alive  
             screen.blit(dummyImg, dummyRect)
                              
        if self.showHPbar:
                pygame.draw.rect(screen, ( 0, 0, 0), (self.x - 49,self.y - 60, 102, 10))  # black bar
                pygame.draw.rect(screen, (255, 0, 0), (self.x - 49,self.y - 59, 100, 8))  # red bar
                pygame.draw.rect(screen, (0, 255, 0), (self.x - 49,self.y - 59, self.hp, 8))  # lime bar    
class cynthia_npc(object):

    def __init__(self):
        self.counter = 0

    def update(self, x, y, player_rect):
        global playerX, playerY, interactable, interact_value
        self.x = x
        self.y = y
        cynthiaImg = pygame.image.load("data/npc/cynthia.png")
        cynthiaRect = cynthiaImg.get_rect()
        cynthiaRect.center = (self.x , self.y)
        cynthiaY = cynthiaRect[1]
        cynthiaX = cynthiaRect[0]
        
        #Top collision
        if playerX >= cynthiaX - 45 and playerX <= cynthiaX + 25 and playerY >= cynthiaY - 60 and playerY <= cynthiaY - 55:
            playerY = cynthiaY - 60
        
        #Bottom collision
        if playerX >= cynthiaX - 45 and playerX <= cynthiaX + 25 and playerY <= cynthiaY + 25 and playerY >= cynthiaY + 20:
           playerY = cynthiaY + 25     
           
           if interactable:
                self.counter += 1
                interactable = False
                print(self.counter)      
                
           if  self.counter == 1:
                catalog_bubble("Good morning big brother")
           elif  self.counter == 2:
                catalog_bubble("your teacher is waiting for you")
           elif  self.counter == 3:
                catalog_bubble("pick your sword from the basement")
           elif  self.counter  == 4:                     
                pass # Dont show anything
           elif self.counter > 4:
                    self.counter = 0

        if not cynthiaRect.collidepoint(player_rect[0], player_rect[1]): # When player leaves the interaction reset the value
            self.counter = 0
      
        # Left collision
        if playerX >= cynthiaX - 45 and playerX <= cynthiaX - 40 and playerY <= cynthiaY + 25 and playerY >= cynthiaY - 60:
            playerX = cynthiaX - 45

        # Right collision
        if playerX <= cynthiaX + 35 and playerX >= cynthiaX + 25 and playerY <= cynthiaY + 25 and playerY >= cynthiaY - 60:
            playerX = cynthiaX + 35   

            
        screen.blit(cynthiaImg, cynthiaRect) 
class manos_npc(object):

    def __init__(self):
        self.counter = 0

    def update(self, x, y, player_rect, condition):
        global playerX, playerY, interactable, interact_value, dummy_task
        self.x = x
        self.y = y
        manosImg = pygame.image.load("data/npc/manos.png")
        manosRect = manosImg.get_rect()
        manosRect.center = (self.x , self.y)
        manosY = manosRect[1]
        manosX = manosRect[0]
        
        #Top collision
        if playerX >= manosX - 45 and playerX <= manosX + 25 and playerY >= manosY - 60 and playerY <= manosY - 55:
            playerY = manosY - 60
        
        #Bottom collision
        if playerX >= manosX - 45 and playerX <= manosX + 25 and playerY <= manosY + 25 and playerY >= manosY + 20:
           playerY = manosY + 25                         
           if interactable:
                self.counter += 1
                interactable = False     
           if condition == "mission1":
               if not dummy_task: # Player has not beaten the dummy
                   if  self.counter == 1:
                        catalog_bubble("Hey John! What's Up?")
                   elif  self.counter == 2:
                        catalog_bubble("Here for your daily training?")
                   elif  self.counter == 3:
                        catalog_bubble("Good. Lets get started!")
                   elif  self.counter  == 4:                     
                        catalog_bubble("Beat down that dummy!")              
                   elif  self.counter  == 5:                     
                        catalog_bubble("(Press LSHIFT or [] to attack.)")
                   elif  self.counter  == 6:
                        pass
                   elif self.counter > 6:
                            self.counter = 0
               else: # Player has beaten the dummy
                   if self.counter == 1:
                        catalog_bubble("Good Job!")
                   elif self.counter == 2:
                        catalog_bubble("You can keep the coins!")
                   elif self.counter == 3:
                        catalog_bubble("Anyway, that's it for today.")
                   elif self.counter  == 4:                     
                        catalog_bubble("See ya later!")              
                   elif self.counter  == 5:                     
                        pass
                   elif self.counter > 5:
                            self.counter = 0

           elif condition == "mission2":
               if  self.counter == 1:
                    catalog_bubble("Hey John! what's the rush?")
               elif  self.counter == 2:
                    catalog_bubble('"My sister is missing."')
               elif  self.counter == 3:
                    catalog_bubble('"I found this letter."')
               elif  self.counter == 4:
                    catalog_bubble('"Know anything about it?"')
               elif  self.counter == 5:
                    catalog_bubble("Mhm.")
               elif  self.counter == 6:
                    catalog_bubble("I know who is behind this.")
               elif  self.counter == 7:
                    catalog_bubble("Meet me outside.")
               elif  self.counter == 8:
                    catalog_bubble("I'll explain later.")
               elif  self.counter  == 9:                     
                    pass # Dont show anything
               elif self.counter > 9:
                        self.counter = 0
               

        if not manosRect.collidepoint(player_rect[0], player_rect[1]): # When player leaves the interaction reset the value
            self.counter = 0
      
        # Left collision
        if playerX >= manosX - 45 and playerX <= manosX - 40 and playerY <= manosY + 25 and playerY >= manosY - 60:
            playerX = manosX - 45

        # Right collision
        if playerX <= manosX + 35 and playerX >= manosX + 25 and playerY <= manosY + 25 and playerY >= manosY - 60:
            playerX = manosX + 35   
            
        screen.blit(manosImg, manosRect) 
class mau(object):
    def __init__(self):
        self.counter = 0
        self.isAutakias = False
        self.point = 0

    def update(self, x, y):
        global playerX, playerY, interactable
        self.x = x
        self.y = y
        mauImg = pygame.image.load("data/npc/Mau.png")
        mauRect = mauImg.get_rect()
        mauRect.center = (self.x, self.y) 

        mauY = mauRect[1]
        mauX = mauRect[0]
        #Animation
        mau_anim = [
            pygame.image.load('data/npc/Mau.png'),
            pygame.image.load('data/npc/Mau2.png'),
            pygame.image.load('data/npc/Mau.png')
        ] 

        if self.counter >= 26:
           self.counter = 0  

        #Top collision
        if playerX >= mauX  - 45 and playerX <= mauX + 25 and playerY >= mauY - 60 and playerY <= mauY - 55:
            playerY = mauY - 60       
        #Bottom collision
        if playerX >= mauX - 45 and playerX <= mauX + 25 and playerY <= mauY + 25 and playerY >= mauY + 20:
           playerY = mauY + 25                    
        # Left collision
        if playerX >= mauX - 45 and playerX <= mauX - 40 and playerY <= mauY + 25 and playerY >= mauY - 60:
            playerX = mauX - 45
        # Right collision
        if playerX <= mauX + 35 and playerX >= mauX + 25 and playerY <= mauY + 25 and playerY >= mauY - 60:
            playerX = mauX + 35  
            if mauRect.collidepoint(player_rect[0], player_rect[1]): # In Mau you interact where he is looking
                if interactable:
                    catalog_bubble("Meow meow meow")            
                    while self.point < 1:
                        r_number = random.randint(1,10)
                        if r_number == 3:
                            self.isAutakias = True # Something secret.. >:))))
                        else:
                            self.isAutakias = False
                        self.point += 1
            
        if not mauRect.collidepoint(player_rect[0], player_rect[1]): # When player leaves the interaction reset the value
            interact_value = 0  
            self.point = 0
                
        if self.isAutakias: # >:))))))
            self.counter += 1
            screen.blit(mau_anim[self.counter // 9], mauRect)          
        else:
            screen.blit(mauImg, mauRect) 
class candy(object):
    def __init__(self):
        self.counter = 0
        self.isYpnaras = False

    def update(self, x, y, player_rect, condition):
        global playerX, playerY, interactable, interact_value
        self.x = x
        self.y = y
        candyImg = pygame.image.load("data/npc/candy.png")
        candyRect = candyImg.get_rect()
        candyRect.center = (self.x, self.y) 

        candyY = candyRect[1]
        candyX = candyRect[0]
        #Animation
        candy_anim = [
            pygame.image.load('data/npc/candy_sleeping.png'),
            pygame.image.load('data/npc/candy_sleeping.png'),
            pygame.image.load('data/npc/candy_sleeping2.png'),
            pygame.image.load('data/npc/candy_sleeping2.png'),
            pygame.image.load('data/npc/candy_sleeping.png')
        ] 

        if condition == "sleeping":
            self.isYpnaras = True
        elif condition == "awake":
            self.isYpnaras = False
        
        #Top collision
        if playerX >=  candyX  - 45 and playerX <=  candyX + 25 and playerY >=  candyY - 60 and playerY <=  candyY - 55:
            playerY =  candyY - 60       
        #Bottom collision
        if playerX >=  candyX - 45 and playerX <=  candyX + 25 and playerY <=  candyY + 25 and playerY >=  candyY + 20:
           playerY =  candyY + 25    
           if candyRect.collidepoint(player_rect[0] + 15, player_rect[1]): # In Mau you interact where he is looking
               if interactable:
                    if self.isYpnaras:
                        if interact_value == 1:
                            catalog_bubble("Zzzzzz....")
                        elif interact_value == 2:
                            catalog_bubble("She fell asleep on the warm carpet.")
                        elif interact_value == 3:
                            pass
                        else:
                            interact_value = False                    
                    else:                      
                        catalog_bubble("Meow meow meow")
        # Left collision
        if playerX >=  candyX - 45 and playerX <=  candyX - 40 and playerY <=  candyY + 25 and playerY >=  candyY - 60:
            playerX =  candyX - 45
        # Right collision
        if playerX <=  candyX + 35 and playerX >=  candyX + 25 and playerY <= candyY + 25 and playerY >=  candyY - 60:
            playerX =  candyX + 35  

        if not candyRect.collidepoint(player_rect[0], player_rect[1]): # When player leaves the interaction reset the value
            interact_value = 0  
            self.point = 0    
                
        if self.isYpnaras:
            if self.counter >= 174: # Thats a lot of frames...
                self.counter = 0  
            self.counter += 1
            screen.blit(candy_anim[self.counter // 35], candyRect)          
        else:
            screen.blit(candyImg, candyRect) 

npcs = [
   cynthia_npc(), #0 cynthia
   manos_npc(), #1 manos
   mau(), #2 mau
   candy() #3 candy
]

cloud1 = cloud(550,50)
cloud2 = cloud(350,70)
cloud3 = cloud(450,90)


# Functions
def isOnMenu():
    global john_room, kitchen, basement, route1, route2, route3, route4, training_field, manosHut, credits_screen, world_value,sword_Task
    global i, j, pl, walkCount, interact_value, player_equipped, interactable, readNote, task_3, dummy_task, player_money, chests, coin_storage,y
    player_equipped, interactable, readNote, task_3, dummy_task = False, False, False, False, False
    john_room, kitchen, basement = False, False, False  # Chunks & World Values
    route1, route2, route3, route4, training_field, manosHut, credits_screen = False, False, False, False, False, False, False
    sword_Task = True
    john_room = True  # [The world] you want to start with
    world_value = 0  # spawn points, counter
    player_money = 0 #  Currency
    i, j, pl, walkCount, interact_value, y= 0, 0, 0, 0, 0,0  # Counters
   
    chests = [
    chest(), #0 johns room
    chest(), #1 Route 2
    chest()  #2 Manos Hut
    ]
    coin_storage = []
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
        if dummy_task and task_3 and readNote:
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
                interact_value += 1        
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
    heart_ui()
    coin_ui()
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
            elif interact_value == 1:
                sword_text = Pixel_font.render("You took the sword.", True, (0,0,0))
                player_equipped = True  # Player has globally his equipment
                sword_Task = False
                screen.blit(sword_text, (120, 350))
            elif interact_value >= 2:
                sword_text = Pixel_font.render("You already took the sword.", True, (0,0,0))
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
    global transparent_black, paused, playerX_change, playerY_change, interactable, closedGame, paused
    Pixel_fontL = pygame.font.Font("data/fonts/pixelfont.ttf", 36)
    text = Pixel_fontL.render('PAUSED', True, (255, 255, 255))
    text2 = Pixel_font.render('To continue press Enter or (X)', True, (255, 255, 255))
    exitImg = pygame.image.load('data/ui/exit_button.png')
    exitBtn = exitImg.get_rect()
    exitBtn.center = (522, 138)

    def menu_button():
        global menu, game, menuCount
        menuImg = pygame.image.load('data/ui/Menu.png')
        menuBtn = menuImg.get_rect()
        menuBtn.center = (326, 300)

        if menuBtn.collidepoint(pygame.mouse.get_pos()):
            menuImg = pygame.image.load('data/ui/Menu_hover.png')
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game, menu = False, True
                    for i in range(len(music_list)):
                        music_list[i].stop()
                    print(game,'closed')
                    menu_screen()
                    paused = False
        else:
            menuImg = pygame.image.load('data/ui/Menu.png')

        if menuBtn.collidepoint(pygame.mouse.get_pos()) : #or aboutButton.collidepoint(pygame.mouse.get_pos()) or 
           while menuCount < 2:
                 music_list[4].play()
                 menuCount += 1

        if not menuBtn.collidepoint(pygame.mouse.get_pos()):
            menuCount = 0

        screen.blit(menuImg, menuBtn)
    
    def quit_button():
        global quitCount
        quitImg = pygame.image.load("data/ui/quit.png")
        quitButton = quitImg.get_rect()
        quitButton.center = (326, 375)

        if quitButton.collidepoint(pygame.mouse.get_pos()):
            quitImg = pygame.image.load('data/ui/quit_hover.png')
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()
                    sys.exit()
        else:
            quitImg = pygame.image.load('data/ui/quit.png')

        if quitButton.collidepoint(pygame.mouse.get_pos()) : #or aboutButton.collidepoint(pygame.mouse.get_pos()) or 
            while quitCount < 2:
                 music_list[4].play()
                 quitCount += 1

        if not quitButton.collidepoint(pygame.mouse.get_pos()):
            quitCount = 0

        screen.blit(quitImg, quitButton)
        
    if paused:
        playerX_change, playerY_change = 0, 0
        screen.blit(transparent_black, (0, 0))
        screen.blit(text, (225, 100))
        screen.blit(text2, (100, 200))
        menu_button()
        quit_button()

        if interactable:
            paused = False
def player_pocket():
    global coinX,coinY
    global player_money
    money = Pixel_font.render(str(player_money) + "€", True, black)
    screen.blit(money, (coin_pos[0] + 40, coin_pos[1] + 15))
def coin_ui():
    coinX = 533
    coinY = 4
    coinImg = pygame.image.load('data/ui/coin_ui.png')
    screen.blit(coinImg, (coinX, coinY))
    return coinX, coinY
coin_pos = coin_ui()
def heart_ui():
    heartX = 4 
    heartY = 4
    health = 100
    HeartImg = pygame.image.load('data/ui/heart_ui.png')
    healthTxt = Pixel_font.render(str(health), True, (0, 0, 0))  
    screen.blit(HeartImg, (heartX, heartY))
    screen.blit(healthTxt, (heartX + 40, heartY + 15))
def cynthia_Note(playerX, playerY, bool):
    screen.blit(note, (120, 180))
    if playerX < 190 and playerY > 130 and playerY < 190:
        if bool:
            screen.blit(transparent_black, (0, 0)),screen.blit(cynthias_Note, (220, 110))
def blacksmith_shop():
    global catalogImg, blacksmithImg
    screen.blit(blacksmithImg, blacksmithRect)
def catalog_bubble(text):
    global catalogImg
    catalogText = Pixel_font.render(text, True, (0,0,0))
    screen.blit(catalogImg, (100, 340)), screen.blit(catalogText, (120, 350))    
    return text
def catalog_bubble2(text):
    catalogText = Pixel_font.render(text, True, (0,0,0))
    screen.blit(catalogText, (120, 380))
    return text
def credits_text():
    global y
    text0 = Pixel_font.render("JOHN'S ADVENTURE CHAPTER 1", True, (255, 255, 255))
    text1 = Pixel_font.render('Thank you for playing the game!', True, (255, 255, 255))
    text2 = Pixel_font.render('Credits', True, (255, 255, 255))
    text3 = Pixel_font.render('Story writer Manos Danezis', True, (255, 255, 255))
    text5 = Pixel_font.render('__Programming Team__', True, (255, 255, 255))
    text6 = Pixel_font.render('Programmer Leader Marios Papazogloy', True, (255, 255, 255))
    text7 = Pixel_font.render('Level/ Art Design Marios Papazogloy', True, (255, 255, 255))
    text8 = Pixel_font.render('Music Design Thanos Pallis', True, (255, 255, 255))
    text9 = Pixel_font.render('Manos Danezis', True, (255, 255, 255))
    for i in range(1):
        y += 0.2
    screen.blit(text0, (140, 250-y)),screen.blit(text1, (140, 350-y))  
    screen.blit(text2, (140, 500-y)),screen.blit(text3, (140, 550-y)) 
    screen.blit(text5, (140, 670 - y)),screen.blit(text6, (140, 690 - y))
    screen.blit(text7, (140, 740 - y)),screen.blit(text9, (140, 760 - y))  
    screen.blit(text8, (140, 810 - y))
def menu_screen():
    global menu, game,playCount,quitCount,settingsCount, MenuCounter, canChange, paused
    if menu:
        isOnMenu()
        music_list[0].play()
        MenuCounter = 0  
        paused = False
    while menu:
        screen.fill((0, 0, 0))
        # background image load
        menu_anim = [
            pygame.image.load('data/ui/mainmenubackground1.png'),
            pygame.image.load('data/ui/mainmenubackground1.png'),
            pygame.image.load('data/ui/mainmenubackground2.png'),
            pygame.image.load('data/ui/mainmenubackground2.png'),
            pygame.image.load('data/ui/mainmenubackground1.png')
        ]

        menu_tile = pygame.image.load('data/ui/mainmenutile.png')

        if MenuCounter >= 114:
            MenuCounter = 0  

        MenuCounter += 1
        screen.blit(menu_anim[MenuCounter // 23], (1, 1)) # Background 
        #Clouds
        cloud1.update()
        cloud2.update()
        cloud3.update()
        screen.blit(menu_tile,(1,1)) # Tile 1

        if playButton.collidepoint(pygame.mouse.get_pos()) : #or aboutButton.collidepoint(pygame.mouse.get_pos()) or 
            while playCount < 2:
                music_list[4].play()
                playCount += 1

        if aboutButton.collidepoint(pygame.mouse.get_pos()) : #or aboutButton.collidepoint(pygame.mouse.get_pos()) or 
            while settingsCount < 2:
                 music_list[4].play()
                 settingsCount += 1

        if quitButton.collidepoint(pygame.mouse.get_pos()) : #or aboutButton.collidepoint(pygame.mouse.get_pos()) or 
            while quitCount < 2:
                 music_list[4].play()
                 quitCount += 1

        if not playButton.collidepoint(pygame.mouse.get_pos()):
             playCount = 0

        if not aboutButton.collidepoint(pygame.mouse.get_pos()):
            settingsCount = 0

        if not quitButton.collidepoint(pygame.mouse.get_pos()):
            quitCount = 0

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

menu_screen()
while game:
    if john_room and world_value == 0:
        playerX, playerY = 150, 150
        music_list[1].play(-1)      
    elif john_room and world_value == 1:
        playerX, playerY = 420, 150
    while john_room:
        background = pygame.image.load('data/sprites/world/Johns_room.png')
        screen.blit(background, (0, 0))  # Display the background image
        npcs[2].update(250,250) # Mau
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
        out_of_bounds()
        if not dummy_task:
            npcs[0].update(400,150, player_rect) # Cynthia NPC
        player()
        if dummy_task:
            cynthia_Note(playerX, playerY, interactable)
            if playerX < 190 and playerY > 130 and playerY < 190:
                readNote = True
                if interactable:
                    music_list[1].stop()
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

        pause_menu()
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
        sword_task(140, 25), player(), pause_menu(), 
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
        player(), out_of_bounds()  # Player
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
        pause_menu()
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
        player(), out_of_bounds()  # Player
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
        pause_menu()
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
        if dummy_task:
            task_3 = True
    elif route3 and world_value == 3:
        playerY, playerX = 110, 285
    while route3:
        background = pygame.image.load('data/sprites/world/route3.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        player(), out_of_bounds(), manos_hut()  # Player
        if playerY >= 400 and playerX >= 95: # Get to route 4
            route3, route4, world_value = False, True, 0
        elif playerX <= 10 and playerY < 295 and playerY >= 150: # Get to route 2
            route3, route2, world_value = False, True, 1
        if playerX >= 465: # Just a simple collision
            playerX = 465
        pause_menu()
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
        npcs[3].update(100,250, player_rect, "sleeping") # Cat npc
        npcs[1].update(325,240, player_rect, "mission2")
        player()
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

        if playerX >= 480 and playerY < 280:
            playerX = 480  # Bed Left col
        if playerX >= 480 and playerY >= 280 and playerY < 300:
            playerY = 300 # Bed Bottom col


        if playerY <= 320 and playerX > 200 and playerX < 210:
            playerX = 210  # Sofa
        if playerY <= 330 and playerX > 120 and playerX < 200:
            playerY = 330
        if playerY < 330 and playerX >= 110 and playerX < 120:
            playerX = 110
        pause_menu()
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
        player(), out_of_bounds()
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
        pause_menu()
        playerX += playerX_change  # MOVEMENT X
        playerY -= playerY_change  # AND Y
        screen.blit(cursor, (pygame.mouse.get_pos()))
        screen.blit(framerate(), (10, 0))
        clock.tick(60)
        pygame.display.update()
    if training_field:
        interact_value, pl = 0, 0
        if world_value == 0:
            Dummy = dummy(385,290)
            playerX = 50
    while training_field:
        background = pygame.image.load('data/sprites/world/training_field.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        blacksmith_shop()
        if not task_3:
            npcs[3].update(100,100, player_rect, "awake") # Cat npc
            npcs[1].update(150,100, player_rect, "mission1") # Manos NPC
            Dummy.update(swordRect)# Training Dummie             
        player()  # Player
        blacksmith_col(), pause_menu(), out_of_bounds()
        if playerX <= 10:
            route4, training_field,  world_value = True, False, 2
            if dummy_task:
                task_3 = True
        pause_menu()
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
        pause_menu()
        clock.tick(60)
        pygame.display.update()
