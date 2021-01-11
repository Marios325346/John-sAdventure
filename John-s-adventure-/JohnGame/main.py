# COPYRIGHT 2020-2021 version 0.0.5 Marios Papazogloy
import pygame, sys, os, json, random  # Libraries
from pygame import mixer
# INITIALIZE
pygame.init()
screen = pygame.display.set_mode((640, 480))  # Setup screen
clock = pygame.time.Clock()
pygame.display.set_caption("John's Adventure  v0.0.5 Semi-stable Chapter 1")
icon = pygame.image.load('data/ui/logo.ico')
pygame.display.set_icon(icon)
# COLORS
black = (0, 0, 0)  # Color black
red = (255, 0, 0)
lime = (0, 255, 0)
# FONTS AND IMAGES
playerImg = pygame.image.load('data/sprites/player/playeridle.png')  # Player
sword_Image = pygame.image.load("data/items/hitbox2.png")
swordRect = sword_Image.get_rect()
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
player_hitbox = pygame.image.load('data/items/hitbox.png')
player_rect = player_hitbox.get_rect()
transparent_black = pygame.image.load("data/ui/black_overlay.png")
# CONTROLLER SUPPORT
controller_value = pygame.joystick.get_init()
joysticks = []  # Initialize controller
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
for joystick in joysticks:
    joystick.init()
analog_keys = {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: -1}
with open(os.path.join("data/controller_keys.json"), 'r+') as file:
    button_keys = json.load(file)
music_list = [mixer.Sound("data/sound/forest_theme_part1.flac"),mixer.Sound("data/sound/home_theme.flac"),mixer.Sound("data/sound/forest_theme.flac"),mixer.Sound("data/sound/dramatic.flac"),mixer.Sound("data/sound/Select_UI.wav")]
for i in range(len(music_list)): # MUSIC & SOUND VOLUME
    music_list[i].set_volume(0.2)
# BOOLEANS
LeftIdle, RightIdle, UpIdle, DownIdle = False, False, False, True
left, right, down, up = False, False, False, False
menu, sword_Task, showCatalog = True, True, True
player_equipped, interactable, readNote, task_3, dummy_task, canChange, paused = False, False, False, False, False, False, False
john_room, kitchen, basement = True, False, False  # Chunks & World Values
route1, route2, route3, route4, training_field, manosHut, credits_screen = False, False, False, False, False, False, False
# VALUES
cooldown, health = 3000, 100
i, j, pl, walkCount, interact_value, y, world_value, counter, options = 0, 0, 0, 0, 0, 0, 0, 0, 0  # Counters
playCount, settingsCount, quitCount, menuCount, player_money, music_counter = 0, 0, 0, 0, 0, 0  # and storage
try:  # Checks if there is a controller else leave it
    if joysticks[2]:
        menuValue = 0
except:
    menuValue = 4  # Kinda disables controller ui changes
# CLASSES
class chest(object):
    def __init__(self):
        self.isOpened = False
        self.counter = 0
        self.value = 0
    def update(self, x, y):
        global player_money, interactable, player_rect
        self.x = x
        self.y = y
        chestImg = pygame.image.load('data/sprites/chest.png')
        chestRect = chestImg.get_rect()  # Images
        chestRect.center = (self.x, self.y)
        if chestRect.collidepoint(player_rect[0] + 15, player_rect[1]):
            if interactable:
                self.value += 1
                interactable = False
            if not self.isOpened:
                if self.value == 1:
                    interact_bubble("Open the chest?")
                elif self.value == 2:
                    interact_bubble("You found 40 coins")
                elif self.value == 3:
                    self.isOpened = True
                    while self.counter < 1:
                        player_money += 40
                        self.counter += 1
            else:
                if self.value == 1:
                    interact_bubble("Open the chest?")
                elif self.value == 2:
                    interact_bubble("The chest is empty")
        else:
            self.value = 0
        screen.blit(chestImg, chestRect)
class coin_system(object):
    def __init__(self, x, y):  # Intialize the object and gives X, Y position
        self.x = x
        self.y = y
        self.coinCount = 0
        self.visibility = True
        self.currency = 0  # Value of the coin
    def update(self, player_rect):
        global player_money  # Player bank
        self.PickupSound = mixer.Sound('data/sound/Pickup_Coin.wav')
        self.PickupSound.set_volume(0.2)
        coin_hitbox = pygame.image.load('data/items/hitbox.png')
        hitbox_rect = coin_hitbox.get_rect()
        hitbox_rect.center = (self.x - 1, self.y)
        coin_anim = [pygame.image.load('data/items/coin1.png'),pygame.image.load('data/items/coin2.png'),pygame.image.load('data/items/coin3.png'),pygame.image.load('data/items/coin4.png'),pygame.image.load('data/items/coin5.png')]  # Animation
        coin_rect = coin_anim[0].get_rect()  # Rect 2 for animation
        coin_rect.center = (self.x, self.y)
        if self.coinCount >= 26:  # Conditions
            self.coinCount = 0
        if hitbox_rect.collidepoint(player_rect[0] + 15, player_rect[1]) and self.visibility:
            self.PickupSound.play()  # Plays sound
            self.currency += 1  # Player gets 1 coin
            player_money += self.currency  # Adds it to players pocket
            self.visibility = False  # The Coin disappears
        if self.visibility:  # If player hasn't touch the coin do this
            screen.blit(coin_anim[self.coinCount // 9], coin_rect)
            screen.blit(coin_hitbox, hitbox_rect)
            self.coinCount += 1
class cloud(object):
    def __init__(self, x, y):
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
        screen.blit(cloudImg, (self.x, self.y))
class dummy(object):
    def __init__(self, x, y):  # Initialize the dummy
        self.x = x
        self.y = y
        self.hp = 100  # Health
        self.showHPbar = False
        self.coinCount = 0
        self.attacked = False
    def update(self, sword_rect):
        global counter, coin_storage, dummy_task, cooldown
        dummyImg = pygame.image.load('data/npc/training_dummie.png')
        dummyRect = dummyImg.get_rect()
        dummyRect.center = (self.x, self.y)  # Position of the dummy
        self.Hit = mixer.Sound('data/sound/sword_hit.flac')
        self.Hit.set_volume(0.2)
        if dummyRect.collidepoint(sword_rect[0], sword_rect[1]):
            self.showHPbar = True  # Show HP bar
            self.attacked = True
            while counter < 1 and self.hp > 0 and cooldown == 0:  # Play a sound on hit, decrease hp
                self.hp -= 10
                self.Hit.play()  # Plays sound
                counter += 1
            self.attacked = False
        if self.hp <= 0:  # if THE DUMMY IS DEAD, turn off the hp bar
            self.showHPbar = False
            screen.blit(pygame.image.load('data/npc/broken_dummie.png'), dummyRect)  # Broken dummy
            for i in range(3):  # Drops 3 coins
                ranX = random.randint(self.x - 30, self.x + 30)  # Random number around dummy's x
                ranY = random.randint(self.y - 30, self.y + 30)  # Random number around dummy's y
                coin_storage.append(coin_system(ranX, ranY))  # append the positions
            coin_storage[0].update(player_rect),coin_storage[1].update(player_rect), coin_storage[2].update(player_rect)  # Spawn coin.
            dummy_task = True  # Completed your first mission
        else:  # Dummy is still alive
            screen.blit(dummyImg, dummyRect)
        if self.showHPbar:
            pygame.draw.rect(screen, (0, 0, 0), (self.x - 49, self.y - 60, 102, 10)), pygame.draw.rect(screen, (255, 0, 0), (self.x - 49, self.y - 59, 100, 8)),pygame.draw.rect(screen, (0, 255, 0), (self.x - 49, self.y - 59, self.hp, 8))  # lime bar
class cynthia_npc(object):
    def __init__(self):
        self.counter = 0
    def update(self, x, y, player_rect):
        global playerX, playerY, interactable, interact_value
        self.x = x
        self.y = y
        cynthiaImg = pygame.image.load("data/npc/cynthia.png")
        cynthiaRect = cynthiaImg.get_rect()
        cynthiaRect.center = (self.x, self.y)
        cynthiaY = cynthiaRect[1]
        cynthiaX = cynthiaRect[0]
        name = Pixel_font.render('-Cynthia', True, (0, 0, 0))
        npc_icon = pygame.image.load('data/npc/npc_cynthia_icon.png')
        if John.x >= cynthiaX - 45 and John.x <= cynthiaX + 25 and John.y >= cynthiaY - 60 and John.y <= cynthiaY - 55:
            John.y = cynthiaY - 60 # Top collision
        if John.x >= cynthiaX - 45 and John.x <= cynthiaX + 25 and John.y <= cynthiaY + 25 and John.y >= cynthiaY + 20:
            John.y = cynthiaY + 25 # Bottom collision
            if interactable:
                self.counter += 1
                interactable = False
            if self.counter == 1:
                catalog_bubble("Good morning big brother", "your teacher is waiting for you")
                screen.blit(npc_icon, (120, 352))
                screen.blit(name, (430, 430))
            elif self.counter == 2:
                catalog_bubble("Your sword is on the basement", None)
                screen.blit(npc_icon, (120, 352))
                screen.blit(name, (430, 430))
            elif self.counter == 3:
                pass  # Don't show anything
            elif self.counter > 3:
                self.counter = 0
        else:
            self.counter = 0
        if John.x >= cynthiaX - 45 and John.x <= cynthiaX - 40 and John.y <= cynthiaY + 25 and John.y >= cynthiaY - 60:
            John.x = cynthiaX - 45    # Left collision
        if John.x <= cynthiaX + 35 and John.x >= cynthiaX + 25 and John.y <= cynthiaY + 25 and John.y >= cynthiaY - 60:
            John.x = cynthiaX + 35  # Right collision
        screen.blit(cynthiaImg, cynthiaRect)
class manos_npc(object):
    def __init__(self):
        self.counter = 0
    def update(self, x, y, player_rect, condition):
        global interactable, interact_value, dummy_task
        self.x = x
        self.y = y
        manosImg = pygame.image.load("data/npc/manos.png")
        manosRect = manosImg.get_rect()
        manosRect.center = (self.x, self.y)
        manosY = manosRect[1]
        manosX = manosRect[0]
        name = Pixel_font.render('-Manos', True, (0, 0, 0))
        npc_icon = pygame.image.load('data/npc/npc_manos_icon.png')
        if John.x >= manosX - 45 and John.x <= manosX + 25 and John.y >= manosY - 60 and John.y <= manosY - 55:
            John.y = manosY - 60 # Top collision
        if John.x >= manosX - 45 and John.x <= manosX + 25 and John.y <= manosY + 25 and John.y >= manosY + 20:
            John.y = manosY + 25  # Bottom collision
            if interactable:
                self.counter += 1
                interactable = False
            if condition == "mission1":
                if not dummy_task:  # Player has not beaten the dummy
                    if self.counter == 1:
                        catalog_bubble("Hey John! What's Up?", "Here for your daily training?")
                        screen.blit(name, (450, 430))
                        screen.blit(npc_icon, (120, 352))
                    elif self.counter == 2:
                        catalog_bubble("Good. Lets get started!", "Beat down that dummy!")
                        screen.blit(name, (450, 430))
                        screen.blit(npc_icon, (120, 352))
                    elif self.counter == 3:
                        interact_bubble("(Press LSHIFT or [] to attack.)")
                        screen.blit(name, (450, 430))
                    elif self.counter == 4:
                        pass
                    elif self.counter > 4:
                        self.counter = 0
                else:  # Player has beaten the dummy
                    if self.counter == 1:
                        catalog_bubble("Good Job!", "You can keep the coins")
                        screen.blit(npc_icon, (120, 352))
                        screen.blit(name, (450, 430))
                    elif self.counter == 2:
                        catalog_bubble("Anyway, that's it for today.", "See ya later")
                        screen.blit(npc_icon, (120, 352))
                        screen.blit(name, (450, 430))
                    elif self.counter == 3:
                        catalog_bubble("Say hi from me to Cynthia", None)
                        screen.blit(npc_icon, (120, 352))
                        screen.blit(name, (450, 430))
                    elif self.counter == 4:
                        pass
                    elif self.counter > 4:
                        self.counter = 0
            elif condition == "mission2":
                if self.counter == 1:
                    catalog_bubble("Hey John! what's the rush?", None)
                    screen.blit(npc_icon, (120, 352))
                    screen.blit(name, (450, 430))
                elif self.counter == 2:
                    catalog_bubble('"My sister is missing.', 'and I found this letter." ')
                elif self.counter == 3:
                    catalog_bubble('"Know anything about it?"', None)
                elif self.counter == 4:
                    catalog_bubble("Mhm.", "I know who is behind this.")
                    screen.blit(name, (450, 430))
                    screen.blit(npc_icon, (120, 352))
                elif self.counter == 5:
                    catalog_bubble("Meet me outside.", "I'll explain later.")
                    screen.blit(name, (450, 430))
                    screen.blit(npc_icon, (120, 352))
                elif self.counter == 6:
                    pass  # Dont show anything
                elif self.counter > 6:
                    self.counter = 0
        else:
            self.counter = 0
        if John.x >= manosX - 45 and John.x <= manosX - 40 and John.y <= manosY + 25 and John.y >= manosY - 60:
            John.x = manosX - 45   # Left collision
        if John.x <= manosX + 35 and John.x >= manosX + 25 and John.y <= manosY + 25 and John.y >= manosY - 60:
            John.x = manosX + 35   # Right collision
        screen.blit(manosImg, manosRect)
class mau(object):
    def __init__(self):
        self.counter = 0
        self.isAutakias = False
        self.point = 0
    def update(self, x, y):
        global interactable
        self.x = x
        self.y = y
        mauImg = pygame.image.load("data/npc/Mau.png")
        mauRect = mauImg.get_rect()
        mauRect.center = (self.x, self.y)
        mauY = mauRect[1]
        mauX = mauRect[0]
        npc_icon = pygame.image.load('data/npc/npc_mau_icon.png')
        name = Pixel_font.render('-Mau', True, (0, 0, 0))
        mau_anim = [pygame.image.load('data/npc/Mau.png'),pygame.image.load('data/npc/Mau2.png'),    pygame.image.load('data/npc/Mau.png')]  # Animation
        if self.counter >= 26:
            self.counter = 0  # Top collision
        if John.x >= mauX - 45 and John.x <= mauX + 25 and John.y >= mauY - 60 and John.y <= mauY - 55:
            John.y = mauY - 60  # Bottom collision
        if John.x >= mauX - 45 and John.x <= mauX + 25 and John.y <= mauY + 25 and John.y >= mauY + 20:
            John.y = mauY + 25  # Left collision
        if John.x >= mauX - 45 and John.x <= mauX - 40 and John.y <= mauY + 25 and John.y >= mauY - 60:
            John.x = mauX - 45  # Right collision
        if John.x <= mauX + 35 and John.x >= mauX + 25 and John.y <= mauY + 25 and John.y >= mauY - 60:
            John.x = mauX + 35
            if mauRect.collidepoint(player_rect[0], player_rect[1]):  # In Mau you interact where he is looking
                if interactable:
                    catalog_bubble("Meow meow meow", None)
                    screen.blit(name, (450, 430))
                    screen.blit(npc_icon, (120, 352))
                    while self.point < 1:
                        r_number = random.randint(1, 10)
                        if r_number == 3:
                            self.isAutakias = True  # Something secret.. >:))))
                        else:
                            self.isAutakias = False
                        self.point += 1
        else:  # When player leaves the interaction
            self.point = 0
        if self.isAutakias:  # >:))))))
            self.counter += 1
            screen.blit(mau_anim[self.counter // 9], mauRect)
        else:
            screen.blit(mauImg, mauRect)
class candy(object):
    def __init__(self):
        self.counter = 0
        self.isYpnaras = False
    def update(self, x, y, player_rect, condition):
        global interactable, interact_value
        self.x = x
        self.y = y
        candyImg = pygame.image.load("data/npc/candy.png")
        candyRect = candyImg.get_rect()
        candyRect.center = (self.x, self.y)
        candyY = candyRect[1]
        candyX = candyRect[0]
        name = Pixel_font.render('-Candy', True, (0, 0, 0))
        npc_icon = pygame.image.load('data/npc/npc_candy_icon.png')
        candy_anim = [pygame.image.load('data/npc/candy_sleeping.png'),pygame.image.load('data/npc/candy_sleeping.png'),  pygame.image.load('data/npc/candy_sleeping2.png'),pygame.image.load('data/npc/candy_sleeping2.png'),  pygame.image.load('data/npc/candy_sleeping.png')]   # Animation
        if condition == "sleeping":
            self.isYpnaras = True
        elif condition == "awake":
            self.isYpnaras = False
        if John.x >= candyX - 45 and John.x <= candyX + 25 and John.y >= candyY - 60 and John.y <= candyY - 55:
            John.y = candyY - 60  # Top collision
        if John.x >= candyX - 45 and John.x <= candyX + 25 and John.y <= candyY + 25 and John.y >= candyY + 20:
            John.y = candyY + 25  # Bottom collision
            if candyRect.collidepoint(player_rect[0] + 15, player_rect[1]):  # In Mau you interact where he is looking
                if interactable:
                    if self.isYpnaras:
                        if interact_value == 1:
                            interact_bubble("Zzzzzz....")
                        elif interact_value == 2:
                            interact_bubble("She fell asleep on the warm carpet.")
                        elif interact_value == 3:
                            pass
                        else:
                            interact_value = False
                    else:  # Candy is awake
                        catalog_bubble("Meow meow meow", None),screen.blit(name, (450, 430)), screen.blit(npc_icon, (120, 352))
        if John.x >= candyX - 45 and John.x <= candyX - 40 and John.y <= candyY + 25 and John.y >= candyY - 60:
            John.x = candyX - 45    # Left collision
        if John.x <= candyX + 35 and John.x >= candyX + 25 and John.y <= candyY + 25 and John.y >= candyY - 60:
            John.x = candyX + 35   # Right collision
        if not candyRect.collidepoint(player_rect[0], player_rect[1]):  # When player leaves the interaction reset the value
            interact_value, self.point = 0,0
        if self.isYpnaras:
            if self.counter >= 174:  # Thats a lot of frames...
                self.counter = 0
            self.counter += 1
            screen.blit(candy_anim[self.counter // 35], candyRect)
        else:
            screen.blit(candyImg, candyRect)
class cynthia_note(object):
    def __init__(self, x, y):
        self.counter = 0
        self.x = x
        self.y = y
    def update(self):
        global interactable, readNote
        note = pygame.image.load('data/items/note.png')
        Big_note = pygame.image.load('data/items/cynthias_note.png')
        screen.blit(note, (self.x, self.y))
        if John.x < self.x + 35 and John.y < self.y + 15 and John.y > self.y - 40:
            if interactable:
                self.counter += 1
                interactable = False
            if self.counter == 1:
                interact_bubble("Whats this?")
            elif self.counter == 2:
                screen.blit(transparent_black, (0, 0)), screen.blit(Big_note, (220, 110))
                readNote = True
            elif self.counter == 3:
                interact_bubble("I have to show this to Manos..")
            elif self.counter == 4:
                pass
            else:
                self.counter = 0
class Player:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.velY = 0
        self.velX = 0
        self.speed = 3
        self.left_pressed = False  # Keystrokes vvv
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.walkCount = 0
        self.LeftIdle = False # Idle vvv
        self.RightIdle = False
        self.DownIdle = True
        self.UpIdle = False
        self.attack = False
        self.up = False  # Movement vvv
        self.down = False
        self.left = False
        self.right = False
    def update(self):
        global cooldown
        self.velX = 0
        self.velY = 0
        wooden_sword = [pygame.image.load('data/items/wooden_sword_up.png'),pygame.image.load('data/items/wooden_sword_left.png')]  # Lists vvv
        attack_down = [pygame.image.load('data/sprites/player/playerdown1.png'),pygame.image.load('data/sprites/player/playerdownattack1.png'),pygame.image.load('data/sprites/player/playerdownattack2.png')]
        attack_up = [pygame.image.load('data/sprites/player/playerup1.png'),pygame.image.load('data/sprites/player/playerupattack1.png'),pygame.image.load('data/sprites/player/playerupattack2.png')]
        attack_right = [pygame.image.load('data/sprites/player/playerright1.png'), pygame.image.load('data/sprites/player/playerrightattack1.png'), pygame.image.load('data/sprites/player/playerrightattack2.png')]
        attack_left = [pygame.image.load('data/sprites/player/playerleft1.png'),pygame.image.load('data/sprites/player/playerleftattack1.png'), pygame.image.load('data/sprites/player/playerleftattack2.png')]
        walkRight = [pygame.image.load('data/sprites/player/playerright1.png'), pygame.image.load('data/sprites/player/playerright2.png'),pygame.image.load('data/sprites/player/playerright1.png')]
        walkLeft = [pygame.image.load('data/sprites/player/playerleft1.png'), pygame.image.load('data/sprites/player/playerleft2.png'),pygame.image.load('data/sprites/player/playerleft1.png')]
        walkUp = [pygame.image.load('data/sprites/player/playerup1.png'), pygame.image.load('data/sprites/player/playerup2.png'),pygame.image.load('data/sprites/player/playerup1.png')]
        walkDown = [pygame.image.load('data/sprites/player/playerdown1.png'),pygame.image.load('data/sprites/player/playerdown2.png'), pygame.image.load('data/sprites/player/playerdown1.png')]
        if self.walkCount + 1 >= 27:  # Animation Counter
            self.walkCount = 0
            if self.attack:
                while cooldown > 0:
                    cooldown -= 10
        if cooldown == 0:
            self.attack = False
        if self.up_pressed:   # Player Movement and Animation
            self.velY = -self.speed
            if self.up:
                screen.blit(walkUp[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
        if self.down_pressed:
            self.velY = self.speed
            if self.down:
                screen.blit(walkDown[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
        if self.left_pressed:
            self.velX = -self.speed
            if self.right_pressed and self.left_pressed:
                self.velX = -self.speed
            if self.left:
                self.velX = -self.speed
                screen.blit(walkLeft[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
        if self.right_pressed:
            self.velX = self.speed
            if self.right_pressed and self.left_pressed:
                self.velX = -self.speed
            if self.right:
                screen.blit(walkRight[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
        if not self.right and not self.left and not self.up and not self.down:  # ANIMATION BACKUP DO NOT TOUCH
            if self.right_pressed:
                screen.blit(walkRight[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
            if self.left_pressed:
                screen.blit(walkLeft[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
            if self.up_pressed:
                screen.blit(walkUp[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
            if self.down_pressed:
                screen.blit(walkDown[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
        if self.left_pressed or self.right_pressed or self.down_pressed or self.up_pressed: # Player is idle/ attacking
            self.LeftIdle = False
            self.RightIdle = False
            self.DownIdle = False
            self.UpIdle = False
        if self.LeftIdle:
            if self.attack and cooldown > 0 and player_equipped:
                screen.blit(wooden_sword[1], (self.x - 40, self.y + 17))
                screen.blit(attack_left[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
                swordRect.center = (John.x - 16, John.y + 35)
                screen.blit(sword_Image, swordRect)
            else:
                screen.blit(walkLeft[0], (self.x, self.y))
        elif self.RightIdle:
            if self.attack and cooldown > 0 and player_equipped:
                screen.blit(attack_right[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
                swordRect.center = (John.x + 80, John.y + 35)
                screen.blit(sword_Image, swordRect)
            else:
                screen.blit(walkRight[0], (self.x, self.y))
        elif self.UpIdle:
            if self.attack and cooldown > 0 and player_equipped:
                screen.blit(wooden_sword[0], (self.x + 7, self.y - 40))
                screen.blit(attack_up[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
                swordRect.center = (John.x + 32, John.y - 25)
                screen.blit(sword_Image, swordRect)
            else:
                screen.blit(walkUp[0], (self.x, self.y))
        elif self.DownIdle:
            if self.attack and cooldown > 0 and player_equipped:
                screen.blit(attack_down[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
                swordRect.center = (John.x + 35, John.y + 80)
                screen.blit(sword_Image, swordRect)
            else:
                screen.blit(playerImg, (self.x, self.y))
        player_stuff()
        self.x += self.velX
        self.y += self.velY
    def controls(self):
        global paused, interact_value, interactable, counter, cooldown, menuValue, options
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.left_pressed = True
                    self.left = True
                    self.right, self.up, self.down = False, False, False
                    self.right_pressed = False
                if event.key == pygame.K_RIGHT:
                    John.right_pressed = True
                    self.right = True
                    self.left, self.up, self.down = False, False, False
                    self.left_pressed = False
                if event.key == pygame.K_UP:
                    self.up_pressed = True
                    self.up = True
                    self.down, self.left, self.right = False, False, False
                    self.down_pressed = False
                if event.key == pygame.K_DOWN:
                    self.down_pressed = True
                    self.down = True
                    self.up, self.left, self.right = False, False, False
                    self.up_pressed = False
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
                    John.walkCount = 0
                    John.attack = True
                    counter = 0
                    cooldown = 2000
                else:
                    John.attack = False
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == button_keys["left_arrow"]:
                    self.left_pressed = True
                    self.left = True
                    self.right, self.up, self.down = False, False, False
                    self.right_pressed = False
                if event.button == button_keys["right_arrow"]:
                    John.right_pressed = True
                    self.right = True
                    self.left, self.up, self.down = False, False, False
                    self.left_pressed = False
                if event.button == button_keys["up_arrow"]:
                    self.up_pressed = True
                    self.up = True
                    self.down, self.left, self.right = False, False, False
                    if paused:
                        if menuValue < 1:
                            menuValue += 1
                    self.down_pressed = False
                if event.button == button_keys["down_arrow"]:
                    self.down_pressed = True
                    self.down = True
                    self.up, self.left, self.right = False, False, False
                    self.up_pressed = False
                    if paused:
                        if menuValue > 0:
                            menuValue -= 1
                if event.button == button_keys["options"]:
                    if options < 1:
                        options += 1
                        paused = True
                    else:
                        paused = False
                        options = 0
                if event.button == button_keys["x"]:    #  Player Interact
                    interactable = True
                    interact_value += 1
                else:
                    interactable = False
                #  Player attack
                if event.button == button_keys["square"]:
                    John.walkCount = 0
                    John.attack = True
                    counter = 0
                    cooldown = 2000
                else:
                    John.attack = False
            if event.type == pygame.JOYBUTTONUP:
                if event.button == button_keys["left_arrow"]:
                    self.left_pressed = False
                    self.LeftIdle = True
                    self.left = False
                if event.button == button_keys["right_arrow"]:
                    self.right_pressed = False
                    self.RightIdle = True
                    self.right = False
                if event.button == button_keys["up_arrow"]:
                    self.up_pressed = False
                    self.UpIdle = True
                    self.up = False
                if event.button == button_keys["down_arrow"]:
                    self.down_pressed = False
                    self.DownIdle = True
                    self.down = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left_pressed = False
                    self.LeftIdle = True
                    self.left = False
                if event.key == pygame.K_RIGHT:
                    self.right_pressed = False
                    self.RightIdle = True
                    self.right = False
                if event.key == pygame.K_UP:
                    self.up_pressed = False
                    self.UpIdle = True
                    self.up = False
                if event.key == pygame.K_DOWN:
                    self.down_pressed = False
                    self.DownIdle = True
                    self.down = False
John = Player(0, 0)
npcs = [cynthia_npc(), manos_npc(),mau(),candy()]
cloud1 = cloud(550, 50)
cloud2 = cloud(350, 70)
cloud3 = cloud(450, 90)
note = cynthia_note(125, 170)
# Functions
def isOnMenu():
    global john_room, kitchen, basement, route1, route2, route3, route4, training_field, manosHut, credits_screen, world_value, sword_Task
    global i, j, pl, walkCount, interact_value, player_equipped, interactable, readNote, task_3, dummy_task, player_money, chests, coin_storage, y
    player_equipped, interactable, readNote, task_3, dummy_task = False, False, False, False, False
    john_room, kitchen, basement = False, False, False  # Chunks & World Values
    route1, route2, route3, route4, training_field, manosHut, credits_screen = False, False, False, False, False, False, False
    sword_Task,john_room = True, True
    i, j, pl, walkCount, interact_value, y, world_value, player_money = 0, 0, 0, 0, 0, 0, 0, 0  # Counters
    chests = [chest(),chest(),chest()]
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
    screen.blit(aboutUI, aboutRect),screen.blit(text, (116, 190)), screen.blit(text2, (250, 225)), screen.blit(controls, (100, 260)), screen.blit(controller_guide, (150, 300))
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
def player_stuff():
    coinX = 533
    coinY = 4
    coinImg = pygame.image.load('data/ui/coin_ui.png')
    heartX = 4
    heartY = 4
    health = 100
    HeartImg = pygame.image.load('data/ui/heart_ui.png')
    healthTxt = Pixel_font.render(str(health), True, (0, 0, 0))
    money = Pixel_font.render(str(player_money) + "€", True, black)
    player_rect.center = (John.x + 32, John.y + 40)
    screen.blit(coinImg, (coinX, coinY))
    screen.blit(money, (coinX + 40, coinY + 15))
    screen.blit(HeartImg, (heartX, heartY))
    screen.blit(healthTxt, (heartX + 40, heartY + 15))
    screen.blit(player_hitbox, player_rect)
def sword_task(posX, posY):
    global catalogImg, interactable, sword_Task, player_equipped, interact_value, pl
    sword = pygame.image.load('data/items/wooden_sword_item.png')
    rotate_sword = pygame.transform.rotate(sword, 90)
    sword_text = Pixel_font.render("Take sword?", True, (0, 0, 0))
    if sword_Task:
        screen.blit(rotate_sword, (posX, posY))
    if John.x >= posX - 50 and John.x <= posX + 50 and John.y >= posY - 50 and John.y <= posY + 50:
        if interactable:
            screen.blit(catalogImg, (100, 340))
            while pl < 1:
                interact_value = 0
                pl += 1
            if interact_value < 1:
                screen.blit(sword_text, (120, 350))  # Text that asks if player wants to equip his sword
            elif interact_value == 1:
                sword_text = Pixel_font.render("You took the sword.", True, (0, 0, 0))
                player_equipped = True  # Player has globally his equipment
                sword_Task = False
                screen.blit(sword_text, (120, 350))
            elif interact_value >= 2:
                sword_text = Pixel_font.render("You already took the sword.", True, (0, 0, 0))
                screen.blit(sword_text, (120, 350))
    else:
        if sword_Task:
            interact_value = 0
    return posX, posY
def out_of_bounds():
    global playerX, playerY
    if John.x <= 5:
        John.x = 5
    elif John.x >= 580:
        John.x = 580
    if John.y <= 10:
        John.y = 10
    elif John.y >= 410:
        John.y = 410
    elif route2:
        if John.y >= 290:
            John.y = 290
def pause_menu():
    global transparent_black, paused, interactable, paused, menuValue
    Pixel_fontL = pygame.font.Font("data/fonts/pixelfont.ttf", 36)
    text = Pixel_fontL.render('PAUSED', True, (255, 255, 255))
    text2 = Pixel_font.render('To continue press Enter or Start', True, (255, 255, 255))
    exitImg = pygame.image.load('data/ui/exit_button.png')
    exitBtn = exitImg.get_rect()
    exitBtn.center = (522, 138)
    def menu_button():
        global menu, game, menuCount, menuValue, paused
        menuImg = pygame.image.load('data/ui/Menu.png')
        menuBtn = menuImg.get_rect()
        menuBtn.center = (326, 300)
        if menuBtn.collidepoint(pygame.mouse.get_pos()):
            menuImg = pygame.image.load('data/ui/Menu_hover.png')
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game, menu, paused = False, True, False
                    for i in range(len(music_list)):
                        music_list[i].stop()
                    menu_screen()
        else:
            menuImg = pygame.image.load('data/ui/Menu.png')
        if menuBtn.collidepoint(pygame.mouse.get_pos()):
            while menuCount < 2:
                music_list[4].play()
                menuCount += 1
        else:
            menuCount = 0
        if menuValue == 1:
            menuImg = pygame.image.load('data/ui/Menu_hover.png')
            if interactable:
                game, menu, paused = False, True, False
                for i in range(len(music_list)):
                    music_list[i].stop()
                menu_screen()
        screen.blit(menuImg, menuBtn)
    def quit_button():
        global quitCount, menuValue
        quitImg = pygame.image.load("data/ui/quit.png")
        quitButton = quitImg.get_rect()
        quitButton.center = (326, 375)
        if quitButton.collidepoint(pygame.mouse.get_pos()):
            quitImg = pygame.image.load('data/ui/quit_hover.png')
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit(),sys.exit()
        else:
            quitImg = pygame.image.load('data/ui/quit.png')
        if quitButton.collidepoint(pygame.mouse.get_pos()):
            while quitCount < 2:
                music_list[4].play()
                quitCount += 1
        else:
            quitCount = 0
        if menuValue == 0:
            quitImg = pygame.image.load('data/ui/quit_hover.png')
            if interactable:
                pygame.quit(),sys.exit()
        screen.blit(quitImg, quitButton)
    if paused:
        John.speed = 0
        screen.blit(transparent_black, (0, 0)), screen.blit(text, (225, 100)),screen.blit(text2, (100, 200)),menu_button(),quit_button()
    else:
        John.speed = 3
def blacksmith_shop():
    global catalogImg, blacksmithImg
    if John.y <= 70 and John.x >= 320:
        John.x = 320
    if John.y > 70 and John.y <= 80 and John.x > 320:
        John.y = 80
        interact_bubble('Shop is currently closed')
    screen.blit(blacksmithImg, blacksmithRect)
def catalog_bubble(text, text1):
    global catalogImg
    catalogText = Pixel_font.render(text, True, (0, 0, 0))
    catalogText2 = Pixel_font.render(text1, True, (0, 0, 0))
    screen.blit(catalogImg, (100, 340)),screen.blit(catalogText, (170, 365))
    if text1 != None:
        screen.blit(catalogText2, (120, 390))
def interact_bubble(text):
    global catalogImg
    catalogText = Pixel_font.render(text, True, (0, 0, 0))
    screen.blit(catalogImg, (100, 340)),screen.blit(catalogText, (130, 350))
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
    screen.blit(text0, (140, 250 - y)), screen.blit(text1, (140, 350 - y))
    screen.blit(text2, (140, 500 - y)), screen.blit(text3, (140, 550 - y))
    screen.blit(text5, (140, 670 - y)), screen.blit(text6, (140, 690 - y))
    screen.blit(text7, (140, 740 - y)), screen.blit(text9, (140, 760 - y))
    screen.blit(text8, (140, 810 - y))
def menu_screen():
    global menu, game, playCount, quitCount, settingsCount, MenuCounter, canChange, paused, menuValue
    if menu:
        isOnMenu(), music_list[0].play(-1)
        MenuCounter, paused = 0, False
    while menu:
        menu_anim = [pygame.image.load('data/ui/mainmenubackground1.png'),pygame.image.load('data/ui/mainmenubackground1.png'),pygame.image.load('data/ui/mainmenubackground2.png'), pygame.image.load('data/ui/mainmenubackground2.png'), pygame.image.load('data/ui/mainmenubackground1.png')]
        menu_tile = pygame.image.load('data/ui/mainmenutile.png')
        if MenuCounter >= 114:
            MenuCounter = 0
        MenuCounter += 1
        screen.blit(menu_anim[MenuCounter // 23], (1, 1)),cloud1.update(),cloud2.update(),cloud3.update(), screen.blit(menu_tile, (1, 1))  # Clouds
        if not canChange:
            if playButton.collidepoint(pygame.mouse.get_pos()):
                while playCount < 2:
                    music_list[4].play()
                    playCount += 1
            else:
                playCount = 0
            if aboutButton.collidepoint(pygame.mouse.get_pos()):
                while settingsCount < 2:
                    music_list[4].play()
                    settingsCount += 1
            else:
                settingsCount = 0
            if quitButton.collidepoint(pygame.mouse.get_pos()):
                while quitCount < 2:
                    music_list[4].play()
                    quitCount += 1
            else:
                quitCount = 0
            if playButton.collidepoint(pygame.mouse.get_pos()):   # Play Button
                playImg = pygame.image.load('data/ui/button interface hover.png')
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        menu = False
                        music_list[0].stop()
                        game = True
                        music_list[1].play(-1)
            else:
                playImg = pygame.image.load('data/ui/button interface.png')
            if aboutButton.collidepoint(pygame.mouse.get_pos()):    # Settings
                aboutImg = pygame.image.load('data/ui/about_hover.png')
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        canChange = True
            else:
                aboutImg = pygame.image.load('data/ui/about.png')
            if quitButton.collidepoint(pygame.mouse.get_pos()):    # Quit
                quitImg = pygame.image.load('data/ui/quit_hover.png')
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit(), sys.exit()
            else:
                quitImg = pygame.image.load('data/ui/quit.png')
        if menuValue == 1:
            playImg = pygame.image.load('data/ui/button interface hover.png')
        elif menuValue == 0:
            aboutImg = pygame.image.load('data/ui/about_hover.png')
        elif menuValue == -1:
            quitImg = pygame.image.load('data/ui/quit_hover.png')
        screen.blit(playImg, playButton),screen.blit(quitImg, quitButton), screen.blit(aboutImg, aboutButton)
        if canChange:  # When player clicks settings
            settings_catalog(), exit_button()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(), sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(), sys.exit()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == button_keys['up_arrow']:
                    if menuValue < 1:
                        menuValue += 1
                if event.button == button_keys['down_arrow']:
                    if menuValue > -1:
                        menuValue -= 1
                if event.button == button_keys['circle']:
                    canChange = False
                if event.button == button_keys['x']:
                    if not canChange:
                        if menuValue == 1:
                            menu = False
                            music_list[0].stop()
                            music_list[1].play(-1)
                            game = True
                        elif menuValue == 0:
                            canChange = True
                        elif menuValue == -1:
                            pygame.quit(),sys.exit()
        screen.blit(cursor, (pygame.mouse.get_pos())),pygame.display.update()
menu_screen()
while game:
    if john_room:
        background = pygame.image.load('data/sprites/world/Johns_room.png')
        if world_value == 0:
            John.x, John.y = 150, 150
        else:
            John.x, John.y = 550, 90
    while john_room:
        screen.blit(background, (0, 0)),npcs[2].update(250, 250), chests[0].update(400, 105),John.update(), John.controls(),pause_menu()
        if John.x >= 440 and John.x <= 530 and John.y >= 60 and John.y <= 120:   # Downstairs collision
            interact_bubble("Wanna go downstairs?")
            if interactable:
                john_room, kitchen, world_value = False, True, 1
        if John.y <= 40:  # Out of bounds collisions vvv
            John.y = 40
        elif John.y >= 410:
            John.y = 410
        if John.x <= 100:
            John.x = 100
        elif John.x >= 580:
            John.x = 580
        if John.x > 510 and John.x < 515 and John.y >= 160:  # Computer collisions vvv
            John.x = 510
        if John.x >= 515 and John.y >= 160 and John.y <= 165:
            John.y = 160
        if John.x < 280 and John.y <= 130:  # Desks collisions vvv
            John.y = 130
        if John.x >= 280 and John.x <= 285 and John.y <= 130:
            John.x = 285
        if John.x >= 340 and John.x <= 400 and John.y <= 80:  # Bottom Chest collisions vvv
            John.y = 80
        if John.x >= 335 and John.x <= 340 and John.y <= 80:
            John.x = 335  # Left
        if John.x >= 400 and John.x <= 410 and John.y <= 80:
            John.x = 410  # Right
        screen.blit(framerate(), (10, 0)),screen.blit(cursor, (pygame.mouse.get_pos())),clock.tick(60),pygame.display.update()
    if kitchen:
        background = pygame.image.load("data/sprites/world/main_room.png")
        if world_value == 3:
            John.x, John.y = 280, 350
        elif world_value == 1:
            John.x, John.y = 470, 30
        else:
            John.x, John.y = 480, 320
    while kitchen:
        screen.blit(background, (0, 0)),John.controls(),  out_of_bounds()
        if not dummy_task:
            npcs[0].update(400, 150, player_rect)  # Cynthia NPC
            John.update()
        else:
            John.update()
            note.update()
        if John.y >= 260 and John.y <= 350 and John.x >= 540:  # Player interacts with basement's door
            interact_bubble("Wanna go to basement?")
            if interactable:
                kitchen, basement = not kitchen, True
        elif John.x >= 503 and John.y <= 45:  # Player interacts with the stairs
            interact_bubble("Wanna go to upstairs?")
            if interactable:
                kitchen, john_room, basement, world_value = False, True, False, 1
        elif John.y >= 370 and John.x >= 220 and John.x <= 320:  # Player interacts with the exit door
            if player_equipped:  # Checks if player has done task 1 which is to get his sword
                interact_bubble("Want to go outside?")
                if interactable:
                    kitchen, route1, basement, world_value = False, True, False, 0
                    music_list[1].stop()
            else:
                interact_bubble("Door is locked")
        if John.x > 135 and John.x <= 145 and John.y <= 305:  # Table collisions
            John.x = 145
        if John.x < 145 and John.y < 315:
            John.y = 315
        if John.y <= 40 and John.x <= 245:  # Kitchen collision
            John.y = 40
        pause_menu(),  screen.blit(framerate(), (10, 0)),  screen.blit(cursor, (pygame.mouse.get_pos())), clock.tick(60), pygame.display.update()
    if basement:
        John.x, John.y, pl = 80, 340, 0
        background = pygame.image.load('data/sprites/world/basement.png')
    while basement:
        screen.blit(background, (0, 0)), sword_task(140, 25), John.update(), pause_menu(), John.controls()
        if John.y >= 270 and John.x <= 20:  # Collision checking & World change
            interact_bubble("Go back to kitchen?")
            if interactable:
                basement, kitchen, world_value = False, True, 5
        if John.y <= 65 and John.x >= -10 and John.y <= 520:  # Furniture Collisions
            John.y = 65
        if John.y >= 0 and John.y <= 360 and John.x >= 355:
            John.x = 355
        if John.y >= 350 and John.x >= -20 and John.x <= 520:
            John.y = 350
        if John.x <= 5 and John.y <= 400:  # Out of bounds
            John.x = 5
        screen.blit(cursor, (pygame.mouse.get_pos())),screen.blit(framerate(), (10, 0)), clock.tick(60), pygame.display.update()
    if route1:
        background = pygame.image.load('data/sprites/world/route1.png')
        if world_value == 0:
            John.x, John.y = 285, 70
            music_list[2].play(-1)
        else:
            John.x = 550
        if readNote:
            music_list[2].stop()
    while route1:
        screen.blit(background, (0, 0)),John.update(), out_of_bounds(), John.controls()
        if John.x <= 20:
            interact_bubble('You have no access to this route')
        if John.y <= 55 and John.x >= 270 and John.x <= 320:  # Return to john's house
            interact_bubble("Return home?")
            if interactable:
                route1, kitchen, basement, world_value = False, True, False, 3
                music_list[2].stop()
                if task_3:
                    music_list[3].play(-1)
                else:
                    music_list[1].play(-1)
        if John.x >= 360 and John.y <= 65:  # Fence collision
            John.y = 65
        elif John.x <= 220 and John.y <= 65:
            John.y = 65
        if John.y <= 40 and John.x <= 245:
            John.y = 40
        if John.x >= 580 and John.y < 295:
            route1, route2, world_value = False, True, 0
        pause_menu(),screen.blit(cursor, (pygame.mouse.get_pos())),screen.blit(framerate(),(10, 0)),clock.tick(60),pygame.display.update()
    if route2:
        background = pygame.image.load('data/sprites/world/route2.png')
        if world_value == 0:
            John.x = 50
        else:
            John.x = 520
    while route2:
        screen.blit(background, (0, 0)),John.update(), out_of_bounds(), John.controls(), chests[1].update(530, 410)
        if John.y <= 40 and John.x < 105:
            playerY = 40
        if John.y <= 40 and John.x >= 106 and John.x <= 115:
            playerX = 115
        if John.x >= 580 and John.y < 295:
            world_value, route2, route3 = 0, False, True  # World value, bool0 , bool1
        elif John.x <= 10 and John.y < 295:
            world_value, route2, route1 = 1, False, True
        if John.y < 150 and John.x > 200:
            John.y = 150
        if John.x > 190 and John.x <= 200 and John.y <= 150:
            John.x = 190
        pause_menu(),screen.blit(cursor, (pygame.mouse.get_pos())),screen.blit(framerate(), (10, 0)),clock.tick(60), pygame.display.update()
    if route3:
        background = pygame.image.load('data/sprites/world/route3.png')
        if world_value == 0:
            John.x = 50
        elif world_value == 2:
            John.y = 350
            if dummy_task:
                task_3 = True
        else:
            John.y, John.x = 110, 285
    while route3:
        screen.blit(background, (0, 0)),John.update(), out_of_bounds(), John.controls()  # Player
        if John.y >= 400 and John.x >= 95:  # Get to route 4
            route3, route4, world_value = False, True, 0
        elif John.x <= 10 and John.y < 295 and John.y >= 150:  # Get to route 2
            route3, route2, world_value = False, True, 1
        if John.x >= 465:  # Just a simple collision
            John.x = 465
        if John.x >= 80 and John.x <= 470 and John.y >= 80 and John.y <= 85:
            John.y = 85
        if John.x >= 70 and John.x < 80 and John.y < 85:
            John.x = 70
        if John.y < 90 and John.x > 470 and John.x <= 490:
            John.x = 490
        if John.y < 90 and John.x > 255 and John.x < 305:
            if dummy_task and task_3 and readNote:
                interact_bubble('Get inside?')
                if interactable:
                    route3, manosHut = False, True
                    world_value = 0
            else:
                interact_bubble('This place is locked')
        pause_menu(),screen.blit(cursor, (pygame.mouse.get_pos())), screen.blit(framerate(), (10, 0)),clock.tick(60), pygame.display.update()
    if manosHut:
        John.y, interact_value, pl, background = 360, 0, 0, pygame.image.load('data/sprites/world/manos_hut.png')
    while manosHut:
        screen.blit(background, (0, 0)), chests[2].update(580, 300), John.controls(), npcs[3].update(100, 250, player_rect, "sleeping"),npcs[1].update(325, 240, player_rect, "mission2"), John.update(),  pause_menu()
        if John.x >= 580:
            John.x = 580
        if John.y >= 410:
            John.y = 410
        if John.x > 260 and John.x <= 300 and John.y >= 170 and John.y <= 180:
            John.y = 181
        if John.x >= 250 and John.x <= 365 and John.y > 380:
            interact_bubble('Go outside?')
            if interactable:  # Door Checker
                credits_screen, manosHut, world_value = True, False, 3
        if John.y < 150 and John.x < 590:
            John.y = 150  # Room collisions vvvvvv
        if John.x < 60:
            John.x = 60
        if John.x >= 480 and John.y < 280:
            John.x = 480  # Bed Left col
        if John.x >= 480 and John.y >= 280 and John.y < 300:
            John.y = 300  # Bed Bottom col
        if John.y <= 320 and John.x > 200 and John.x < 210:
            John.x = 210  # Sofa
        if John.y <= 330 and John.x > 120 and John.x < 200:
            John.y = 330
        if John.y < 330 and John.x >= 110 and John.x < 120:
            John.x = 110
        screen.blit(cursor, (pygame.mouse.get_pos())),screen.blit(framerate(), (10, 0)), clock.tick(60),pygame.display.update()
    if route4:
        background = pygame.image.load('data/sprites/world/route4.png')
        if world_value == 0:
            John.y = 50
        else:
            John.x = 520
    while route4:
        screen.blit(background, (0, 0)),John.update(), out_of_bounds(), John.controls()
        if John.x >= 580:
            route4, training_field, world_value = False, True, 0
        if John.y <= 10 and John.x <= 465:
            route3, route4, world_value = True, False, 2
        if John.x <= 90:
            John.x = 90
        if John.y >= 130 and John.y <= 175 and John.x <= 95 and interactable:
            interact_bubble("OUT OF ORDER")
        if John.y > 175 and John.y < 270 and John.x <= 95 and interactable:
            interact_bubble("You can't get in for now.")
        if John.y >= 270 and John.y <= 320 and John.x <= 95 and interactable:
            interact_bubble("OUT OF ORDER")
        pause_menu(),screen.blit(cursor, (pygame.mouse.get_pos())),screen.blit(framerate(), (10, 0)), clock.tick(60),pygame.display.update()
    if training_field:
        interact_value, pl, background = 0, 0, pygame.image.load('data/sprites/world/training_field.png')
        Dummy = dummy(385, 290)
        John.x = 50
    while training_field:
        screen.blit(background, (0, 0)), blacksmith_shop(), John.controls()
        if not task_3:
            npcs[3].update(100, 100, player_rect, "awake"),npcs[1].update(150, 100, player_rect, "mission1"),Dummy.update(swordRect)  # Training Dummie
        John.update(),pause_menu(), out_of_bounds()
        if John.x <= 10:
            route4, training_field, world_value = True, False, 2
            if dummy_task:
                task_3 = True
        pause_menu(),screen.blit(cursor, (pygame.mouse.get_pos())),screen.blit(framerate(), (10, 0)),clock.tick(60),pygame.display.update()
    while credits_screen:
        screen.fill((0, 0, 0)),John.controls(),credits_text(),screen.blit(cursor, (pygame.mouse.get_pos())),pause_menu(),clock.tick(60),pygame.display.update()