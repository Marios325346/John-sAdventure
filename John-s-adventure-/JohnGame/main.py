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
    mixer.Sound("data/sound/forest_theme_part1.flac"),  # 0
    mixer.Sound("data/sound/home_theme.flac"),  # 1
    mixer.Sound("data/sound/forest_theme.flac"),  # 2
    mixer.Sound("data/sound/dramatic.flac"),  # 3
    mixer.Sound("data/sound/Select_UI.wav")  # 4
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
health = 100
music_counter = 0
player_hitbox = pygame.image.load('data/items/hitbox.png')
player_rect = player_hitbox.get_rect()
world_value, counter = 0, 0  # spawn points, counter
i, j, pl, walkCount, interact_value = 0, 0, 0, 0, 0  # Counters
y = 0
playCount, settingsCount, quitCount, menuCount = 0, 0, 0, 0
player_money = 0  # Currency
menuValue = 0

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
        # Images
        chestImg = pygame.image.load('data/sprites/chest.png')
        chestRect = chestImg.get_rect()
        chestRect.center = (self.x, self.y)
        if chestRect.collidepoint(player_rect[0] + 15, player_rect[1]):
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
    def __init__(self, x, y):  # Intialize the object and gives X, Y position
        self.x = x
        self.y = y
        self.coinCount = 0
        self.visibility = True
        self.currency = 0  # Value of the coin        

    def update(self, player_rect):  # Updates the object's condition (Animation etc.)
        global player_money
        # Sound
        self.PickupSound = mixer.Sound('data/sound/Pickup_Coin.wav')
        # Rect 1
        coin_hitbox = pygame.image.load('data/items/hitbox.png')
        hitbox_rect = coin_hitbox.get_rect()
        hitbox_rect.center = (self.x - 1, self.y)
        # Animation
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
        self.counter = 0
        self.coinCount = 0
        self.attacked = False

    def update(self, sword_rect):
        global counter, coin_storage, dummy_task, cooldown
        dummyImg = pygame.image.load('data/npc/training_dummie.png')
        dummyRect = dummyImg.get_rect()
        dummyRect.center = (self.x, self.y)  # Position of the dummy
        self.Hit = mixer.Sound('data/sound/sword_hit.flac')
        if dummyRect.collidepoint(sword_rect[0], sword_rect[1]):
            self.showHPbar = True  # Show HP bar
            self.attacked = True
            while counter < 1 and self.hp > 0 and cooldown <= 0:  # Play a sound on hit, decrease hp
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
            coin_storage[0].update(player_rect)  # Spawn coin.
            coin_storage[1].update(player_rect)  # Spawn coin.
            coin_storage[2].update(player_rect)  # Spawn coin.
            dummy_task = True  # Completed your first mission
        else:  # Dummy is still alive
            screen.blit(dummyImg, dummyRect)
        if self.showHPbar:
            pygame.draw.rect(screen, (0, 0, 0), (self.x - 49, self.y - 60, 102, 10))  # black bar
            pygame.draw.rect(screen, (255, 0, 0), (self.x - 49, self.y - 59, 100, 8))  # red bar
            pygame.draw.rect(screen, (0, 255, 0), (self.x - 49, self.y - 59, self.hp, 8))  # lime bar


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
        # Top collision
        if John.x >= cynthiaX - 45 and John.x <= cynthiaX + 25 and John.y >= cynthiaY - 60 and John.y <= cynthiaY - 55:
            John.y = cynthiaY - 60
            # Bottom collision
        if John.x >= cynthiaX - 45 and John.x <= cynthiaX + 25 and John.y <= cynthiaY + 25 and John.y >= cynthiaY + 20:
            John.y = cynthiaY + 25
            if interactable:
                self.counter += 1
                interactable = False
            if self.counter == 1:
                catalog_bubble("Good morning big brother")
                screen.blit(name, (430, 430))
            elif self.counter == 2:
                catalog_bubble("your teacher is waiting for you")
                screen.blit(name, (430, 430))
            elif self.counter == 3:
                catalog_bubble("pick your sword from the basement")
                screen.blit(name, (430, 430))
            elif self.counter == 4:
                pass  # Don't show anything
            elif self.counter > 4:
                self.counter = 0
        if not John.x >= cynthiaX - 45 and John.x <= cynthiaX + 25 and John.y <= cynthiaY + 25 and John.y >= cynthiaY + 20:  # When player leaves the interaction reset the value
            self.counter = 0
            # Left collision
        if John.x >= cynthiaX - 45 and John.x  <= cynthiaX - 40 and John.y <= cynthiaY + 25 and John.y >= cynthiaY - 60:
            John.x = cynthiaX - 45
        # Right collision
        if John.x <= cynthiaX + 35 and John.x  >= cynthiaX + 25 and John.y <= cynthiaY + 25 and John.y >= cynthiaY - 60:
           John.x = cynthiaX + 35
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
        # Top collision
        if John.x >= manosX - 45 and John.x <= manosX + 25 and John.y >= manosY - 60 and John.y <= manosY - 55:
            John.y = manosY - 60
            # Bottom collision
        if John.x >= manosX - 45 and John.x <= manosX + 25 and John.y <= manosY + 25 and John.y >= manosY + 20:
            John.y = manosY + 25
            if interactable:
                self.counter += 1
                interactable = False
            if condition == "mission1":
                if not dummy_task:  # Player has not beaten the dummy
                    if self.counter == 1:
                        catalog_bubble("Hey John! What's Up?")
                        screen.blit(name, (450, 430))
                    elif self.counter == 2:
                        catalog_bubble("Here for your daily training?")
                        screen.blit(name, (450, 430))
                    elif self.counter == 3:
                        catalog_bubble("Good. Lets get started!")
                        screen.blit(name, (450, 430))
                    elif self.counter == 4:
                        catalog_bubble("Beat down that dummy!")
                        screen.blit(name, (450, 430))
                    elif self.counter == 5:
                        catalog_bubble("(Press LSHIFT or [] to attack.)")
                        screen.blit(name, (450, 430))
                    elif self.counter == 6:
                        pass
                    elif self.counter > 6:
                        self.counter = 0
                else:  # Player has beaten the dummy
                    if self.counter == 1:
                        catalog_bubble("Good Job!")
                        screen.blit(name, (450, 430))
                    elif self.counter == 2:
                        catalog_bubble("You can keep the coins!")
                        screen.blit(name, (450, 430))
                    elif self.counter == 3:
                        catalog_bubble("Anyway, that's it for today.")
                        screen.blit(name, (450, 430))
                    elif self.counter == 4:
                        catalog_bubble("See ya later!")
                        screen.blit(name, (450, 430))
                    elif self.counter == 5:
                        pass
                    elif self.counter > 5:
                        self.counter = 0
            elif condition == "mission2":
                if self.counter == 1:
                    catalog_bubble("Hey John! what's the rush?")
                    screen.blit(name, (450, 430))
                elif self.counter == 2:
                    catalog_bubble('"My sister is missing."')
                elif self.counter == 3:
                    catalog_bubble('"I found this letter."')
                elif self.counter == 4:
                    catalog_bubble('"Know anything about it?"')
                elif self.counter == 5:
                    catalog_bubble("Mhm.")
                    screen.blit(name, (450, 430))
                elif self.counter == 6:
                    catalog_bubble("I know who is behind this.")
                    screen.blit(name, (450, 430))
                elif self.counter == 7:
                    catalog_bubble("Meet me outside.")
                    screen.blit(name, (450, 430))
                elif self.counter == 8:
                    catalog_bubble("I'll explain later.")
                    screen.blit(name, (450, 430))
                elif self.counter == 9:
                    pass  # Dont show anything
                elif self.counter > 9:
                    self.counter = 0

        if not John.x >= manosX - 45 and John.x <= manosX + 25 and  John.y <= manosY + 25 and  John.y >= manosY + 20:  # When player leaves the interaction reset the value
            self.counter = 0

        # Left collision
        if John.x >= manosX - 45 and John.x <= manosX - 40 and  John.y <= manosY + 25 and  John.y >= manosY - 60:
            John.x = manosX - 45

        # Right collision
        if John.x <= manosX + 35 and John.x >= manosX + 25 and  John.y <= manosY + 25 and  John.y >= manosY - 60:
            John.x = manosX + 35

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

        name = Pixel_font.render('-Mau', True, (0, 0, 0))
        # Animation
        mau_anim = [
            pygame.image.load('data/npc/Mau.png'),
            pygame.image.load('data/npc/Mau2.png'),
            pygame.image.load('data/npc/Mau.png')
        ]
        if self.counter >= 26:
            self.counter = 0
            # Top collision
        if John.x >= mauX - 45 and John.x <= mauX + 25 and John.y >= mauY - 60 and John.y <= mauY - 55:
            John.y = mauY - 60
            # Bottom collision
        if John.x >= mauX - 45 and John.x <= mauX + 25 and John.y <= mauY + 25 and John.y >= mauY + 20:
            John.y = mauY + 25
            # Left collision
        if John.x >= mauX - 45 and John.x <= mauX - 40 and John.y <= mauY + 25 and John.y >= mauY - 60:
            John.x = mauX - 45
        # Right collision
        if John.x <= mauX + 35 and John.x >= mauX + 25 and John.y <= mauY + 25 and John.y >= mauY - 60:
            John.x = mauX + 35
            if mauRect.collidepoint(player_rect[0], player_rect[1]):  # In Mau you interact where he is looking
                if interactable:
                    catalog_bubble("Meow meow meow")
                    screen.blit(name, (450, 430))
                    while self.point < 1:
                        r_number = random.randint(1, 10)
                        if r_number == 3:
                            self.isAutakias = True  # Something secret.. >:))))
                        else:
                            self.isAutakias = False
                        self.point += 1
        if not mauRect.collidepoint(player_rect[0],player_rect[1]):  # When player leaves the interaction reset the value
            interact_value = 0
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
        # Animation
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
            # Top collision
        if John.x >= candyX - 45 and John.x <= candyX + 25 and John.y >= candyY - 60 and John.y <= candyY - 55:
            John.y = candyY - 60
            # Bottom collision
        if John.x >= candyX - 45 and John.x <= candyX + 25 and John.y <= candyY + 25 and John.y >= candyY + 20:
            John.y = candyY + 25
            if candyRect.collidepoint(player_rect[0] + 15, player_rect[1]):  # In Mau you interact where he is looking
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
                        screen.blit(name, (450, 430))
                        # Left collision
        if John.x >= candyX - 45 and John.x <= candyX - 40 and  John.y <= candyY + 25 and  John.y >= candyY - 60:
            John.x = candyX - 45
        # Right collision
        if John.x <= candyX + 35 and John.x >= candyX + 25 and  John.y <= candyY + 25 and  John.y >= candyY - 60:
            John.x = candyX + 35
        if not candyRect.collidepoint(player_rect[0],player_rect[1]):  # When player leaves the interaction reset the value
            interact_value = 0
            self.point = 0
        if self.isYpnaras:
            if self.counter >= 174:  # Thats a lot of frames...
                self.counter = 0
            self.counter += 1
            screen.blit(candy_anim[self.counter // 35], candyRect)
        else:
            screen.blit(candyImg, candyRect)


class Player:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.velY = 0
        self.velX = 0
        self.speed = 3
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.walkCount = 0
        self.LeftIdle = False
        self.RightIdle = False
        self.DownIdle = True
        self.UpIdle = False
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.attack = False
        self.cooldown = 3000

    def update(self):
        self.velX = 0
        self.velY = 0
        player_stuff()
        # Lists
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

        attack_left = [pygame.image.load('data/sprites/player/playerleft1.png'),
                       pygame.image.load('data/sprites/player/playerleftattack1.png'),
                       pygame.image.load('data/sprites/player/playerleftattack2.png')]

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

        #Animation Counter
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
            if self.attack:
                while self.cooldown > 0:
                    self.cooldown -= 10
                else:
                    self.attack = False

        # Player is walking
        if self.left_pressed or self.right_pressed or self.down_pressed or self.up_pressed:
            self.LeftIdle = False
            self.RightIdle = False
            self.DownIdle = False
            self.UpIdle = False
        # When player presses keys
        if self.left_pressed:
            self.velX = -self.speed
            if self.left:
                screen.blit(walkLeft[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
        if self.right_pressed:
            self.velX = self.speed
            if self.right:
                screen.blit(walkRight[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
        if self.down_pressed:
            self.velY = self.speed
            if self.down:
                screen.blit(walkDown[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
        if self.up_pressed:
            self.velY = -self.speed
            if self.up:
                screen.blit(walkUp[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1

        # Player is idle/ attacking
        if self.LeftIdle or self.DownIdle or self.UpIdle or self.RightIdle:
            hitbox()
        if self.LeftIdle:
            if self.attack:
                screen.blit(wooden_sword[1], (self.x - 40, self.y + 17))
                screen.blit(attack_left[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
            else:
                screen.blit(walkLeft[0], (self.x, self.y))
        elif self.RightIdle:
            if self.attack:
                screen.blit(attack_right[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
            else:
                screen.blit(walkRight[0], (self.x, self.y))
        elif self.UpIdle:
            if self.attack:
                screen.blit(wooden_sword[0], (self.x + 7, self.y - 40))
                screen.blit(attack_up[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
            else:
                screen.blit(walkUp[0], (self.x, self.y))
        elif self.DownIdle:
            if self.attack:
                screen.blit(attack_down[self.walkCount // 9], (self.x, self.y))
                self.walkCount += 1
            else:
                screen.blit(playerImg, (self.x, self.y))

        self.x += self.velX
        self.y += self.velY

    def controls(self):
        global paused, interact_value, interactable, counter, cooldown
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    John.left_pressed = True
                    John.left = True
                    John.right, John.up, John.down = False, False, False
                if event.key == pygame.K_RIGHT:
                    John.right_pressed = True
                    John.right = True
                    John.left, John.up, John.down = False, False, False
                if event.key == pygame.K_UP:
                    John.up_pressed = True
                    John.up = True
                    John.down, John.left, John.right = False, False, False
                if event.key == pygame.K_DOWN:
                    John.down_pressed = True
                    John.down = True
                    John.up, John.left, John.right = False, False, False
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
                else:
                    John.attack = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    John.left_pressed = False
                    John.LeftIdle = True
                if event.key == pygame.K_RIGHT:
                    John.right_pressed = False
                    John.RightIdle = True
                if event.key == pygame.K_UP:
                    John.up_pressed = False
                    John.UpIdle = True
                if event.key == pygame.K_DOWN:
                    John.down_pressed = False
                    John.DownIdle = True

John = Player(250, 300)

npcs = [
    cynthia_npc(),  # 0 cynthia
    manos_npc(),  # 1 manos
    mau(),  # 2 mau
    candy()  # 3 candy
]

cloud1 = cloud(550, 50)
cloud2 = cloud(350, 70)
cloud3 = cloud(450, 90)


# Functions
def isOnMenu():
    global john_room, kitchen, basement, route1, route2, route3, route4, training_field, manosHut, credits_screen, world_value, sword_Task
    global i, j, pl, walkCount, interact_value, player_equipped, interactable, readNote, task_3, dummy_task, player_money, chests, coin_storage, y
    player_equipped, interactable, readNote, task_3, dummy_task = False, False, False, False, False
    john_room, kitchen, basement = False, False, False  # Chunks & World Values
    route1, route2, route3, route4, training_field, manosHut, credits_screen = False, False, False, False, False, False, False
    sword_Task = True
    john_room = True  # [The world] you want to start with
    world_value = 0  # spawn points, counter
    player_money = 0  # Currency
    i, j, pl, walkCount, interact_value, y = 0, 0, 0, 0, 0, 0  # Counters
    chests = [
        chest(),  # 0 johns room
        chest(),  # 1 Route 2
        chest()  # 2 Manos Hut
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
        swordRect.center = (John.x - 16, John.y + 35)
        screen.blit(sword_Image, swordRect)
    elif RightIdle:
        swordRect.center = (John.x + 80, John.y + 35)
        screen.blit(sword_Image, swordRect)
    elif DownIdle:
        swordRect.center = (John.x + 35, John.y + 80)
        screen.blit(sword_Image, swordRect)
    elif UpIdle:
        swordRect.center = (John.x + 32, John.y - 25)
        screen.blit(sword_Image, swordRect)
    return swordRect


def manos_hut():
    global interactable, route3, manosHut, world_value, readNote
    if John.x >= 80 and John.x <= 470 and John.y >= 80 and John.y <= 85:
        John.x = 85
    if John.x >= 70 and John.x < 80 and John.y < 85:
        John.x = 70
    if John.y < 85 and John.x > 470 and John.x <= 490:
        John.x = 490
    if John.y < 90 and John.x > 255 and John.x < 305:
        if dummy_task and task_3 and readNote:
            catalog_bubble('Get inside?')
            if interactable:
                route3, manosHut = False, True
                world_value = 0
        else:
            catalog_bubble('This place is locked')

def player_stuff():
    heart_ui()
    coin_ui()
    player_pocket()
    player_rect.center = (John.x + 32, John.y + 40)
    screen.blit(player_hitbox, player_rect)


def sword_task(posX, posY):
    global catalogImg, playerY, playerX, interactable, sword_Task, player_equipped, interact_value, pl
    sword = pygame.image.load('data/items/wooden_sword_item.png')
    rotate_sword = pygame.transform.rotate(sword, 90)
    sword_text = Pixel_font.render("Take sword?", True, (0, 0, 0))
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


def blacksmith_col():  # Blacksmith collisions
    if John.y <= 70 and John.x >= 320:
        playerX = 320
    if John.y > 70 and John.y <= 80 and John.x > 320:
        John.y = 80
        catalog_bubble('Shop is currently closed')


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
    global transparent_black, paused, playerX_change, playerY_change, interactable, closedGame, paused, menuValue
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
                    game, menu = False, True
                    for i in range(len(music_list)):
                        music_list[i].stop()
                    menu_screen()
                    paused = False
        else:
            menuImg = pygame.image.load('data/ui/Menu.png')
        if menuBtn.collidepoint(pygame.mouse.get_pos()):  # or aboutButton.collidepoint(pygame.mouse.get_pos()) or
            while menuCount < 2:
                music_list[4].play()
                menuCount += 1
        if not menuBtn.collidepoint(pygame.mouse.get_pos()):
            menuCount = 0
        if menuValue == 1:
            menuImg = pygame.image.load('data/ui/Menu_hover.png')
            if interactable:
                game, menu = False, True
                for i in range(len(music_list)):
                    music_list[i].stop()
                menu_screen()
                paused = False
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
                    pygame.quit()
                    sys.exit()
        else:
            quitImg = pygame.image.load('data/ui/quit.png')
        if quitButton.collidepoint(pygame.mouse.get_pos()):  # or aboutButton.collidepoint(pygame.mouse.get_pos()) or
            while quitCount < 2:
                music_list[4].play()
                quitCount += 1
        if not quitButton.collidepoint(pygame.mouse.get_pos()):
            quitCount = 0
        if menuValue == 0:
            quitImg = pygame.image.load('data/ui/quit_hover.png')
            if interactable:
                pygame.quit()
                sys.exit()

        screen.blit(quitImg, quitButton)

    if paused:
        John.speed = 0
        screen.blit(transparent_black, (0, 0))
        screen.blit(text, (225, 100))
        screen.blit(text2, (100, 200))
        menu_button()
        quit_button()


def player_pocket():
    global coinX, coinY
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
    if John.x < 190 and John.y > 130 and John.y < 190:
        if bool:
            screen.blit(transparent_black, (0, 0)), screen.blit(cynthias_Note, (220, 110))


def blacksmith_shop():
    global catalogImg, blacksmithImg
    screen.blit(blacksmithImg, blacksmithRect)


def catalog_bubble(text):
    global catalogImg
    catalogText = Pixel_font.render(text, True, (0, 0, 0))
    screen.blit(catalogImg, (100, 340)), screen.blit(catalogText, (120, 350))
    return text


def catalog_bubble2(text):
    catalogText = Pixel_font.render(text, True, (0, 0, 0))
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
    screen.blit(text0, (140, 250 - y)), screen.blit(text1, (140, 350 - y))
    screen.blit(text2, (140, 500 - y)), screen.blit(text3, (140, 550 - y))
    screen.blit(text5, (140, 670 - y)), screen.blit(text6, (140, 690 - y))
    screen.blit(text7, (140, 740 - y)), screen.blit(text9, (140, 760 - y))
    screen.blit(text8, (140, 810 - y))


def menu_screen():
    global menu, game, playCount, quitCount, settingsCount, MenuCounter, canChange, paused, menuValue
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
        screen.blit(menu_anim[MenuCounter // 23], (1, 1))  # Background
        # Clouds
        cloud1.update()
        cloud2.update()
        cloud3.update()
        screen.blit(menu_tile, (1, 1))  # Tile 1
        if playButton.collidepoint(pygame.mouse.get_pos()):  # or aboutButton.collidepoint(pygame.mouse.get_pos()) or
            while playCount < 2:
                music_list[4].play()
                playCount += 1
        if aboutButton.collidepoint(pygame.mouse.get_pos()):  # or aboutButton.collidepoint(pygame.mouse.get_pos()) or
            while settingsCount < 2:
                music_list[4].play()
                settingsCount += 1
        if quitButton.collidepoint(pygame.mouse.get_pos()):  # or aboutButton.collidepoint(pygame.mouse.get_pos()) or
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
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    menu = False
                    music_list[0].stop()
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

        if menuValue == 1:
            playImg = pygame.image.load('data/ui/button interface hover.png')
        elif menuValue == 0:
            aboutImg = pygame.image.load('data/ui/about_hover.png')
        elif menuValue == -1:
            quitImg = pygame.image.load('data/ui/quit_hover.png')

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
                            game = True
                        elif menuValue == 0:
                            canChange = True
                        elif menuValue == -1:
                            pygame.quit()
                            sys.exit()
        screen.blit(cursor, (pygame.mouse.get_pos()))
        pygame.display.update()


menu_screen()
while game:
    if john_room and world_value == 0:
        John.x, John.y = 150, 150
        music_list[1].play(-1)
    elif john_room and world_value == 1:
        John.x, John.y = 420, 150
    while john_room:
        background = pygame.image.load('data/sprites/world/Johns_room.png')
        screen.blit(background, (0, 0))  # Display the background image
        npcs[2].update(250, 250)  # Mau
        chests[0].update(400, 105, interactable, player_rect)

        John.update()
        John.controls()
        pause_menu()  # Player
        # Downstairs collision
        if John.x >= 440 and John.x <= 530 and John.y >= 60 and John.y <= 120:
            catalog_bubble("Wanna go downstairs?")
            if interactable:
                john_room, kitchen = False, True
        # Out of bounds collisions
        if John.y <= 40:
            John.y = 40
        elif John.y >= 410:
            John.y = 410
        if John.x <= 100:
            John.x = 100
        elif John.x >= 580:
            John.x = 580
        # Computer collisions
        if John.x  > 510 and John.x < 515 and John.y >= 160:
            John.x = 510
        if John.x >= 515 and John.y >= 160 and John.y  <= 165:
            John.y = 160
        # Desks collisions
        if John.x < 280 and John.y <= 130:
            John.y = 130
        if John.x >= 280 and John.x <= 285 and John.y <= 130:
            John.x = 285
        # Chest collisions
        if John.x >= 340 and John.x <= 400 and John.y <= 80:
            John.y = 80  # Bottom
        if John.x >= 335 and John.x <= 340 and John.y <= 80:
            John.x = 335  # Left
        if John.x >= 400 and John.x <= 410 and John.y <= 80:
            John.x = 410  # Right

        screen.blit(framerate(), (10, 0))
        screen.blit(cursor, (pygame.mouse.get_pos()))
        clock.tick(60)
        pygame.display.update()
    if kitchen and world_value == 3:
        John.x, John.y = 280, 350
    elif kitchen and world_value == 5:
        John.x, John.y = 480, 320
    while kitchen:
        background = pygame.image.load("data/sprites/world/main_room.png")
        screen.blit(background, (0, 0))
        out_of_bounds()
        if not dummy_task:
            npcs[0].update(400, 150, player_rect)  # Cynthia NPC
        John.update()
        John.controls()
        if dummy_task:
            cynthia_Note(John.x, John.y, interactable)
            if John.x < 190 and John.y > 130 and John.y < 190:
                readNote = True
                if interactable:
                    music_list[1].stop()
        if John.y >= 260 and playerY <= 350 and John.x >= 540:  # Player interacts with basement's door
            catalog_bubble("Wanna go to basement?")
            if interactable:
                kitchen, basement = not kitchen, True
        elif John.x >= 503 and John.y <= 45:  # Player interacts with the stairs
            catalog_bubble("Wanna go to upstairs?")
            if interactable:
                kitchen, john_room, basement, world_value = False, True, False, 1
        elif John.y >= 370 and John.x >= 220 and John.x <= 320:  # Player interacts with the exit door
            if player_equipped:  # Checks if player has done task 1 which is to get his sword
                catalog_bubble("Want to go outside?")
                if interactable:
                    kitchen, route1, basement, world_value = False, True, False, 0
                    music_list[1].stop()
            else:
                catalog_bubble("Door is locked")
        if John.x > 135 and John.x <= 145 and John.y <= 305:  # Table collisions
            John.x = 145
        if John.x < 145 and John.y < 315:
            John.y = 315
        if John.y <= 40 and John.x <= 245:  # Kitchen collision
            John.y = 40
        pause_menu()
        screen.blit(framerate(), (10, 0))
        screen.blit(cursor, (pygame.mouse.get_pos()))
        clock.tick(60)
        pygame.display.update()

    if basement:
        John.x, John.y, pl = 80, 340, 0
    while basement:
        background = pygame.image.load('data/sprites/world/basement.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        sword_task(140, 25), John.update(), pause_menu()
        John.controls()
        if John.y >= 270 and John.x <= 20:  # Collision checking & World change
            catalog_bubble("Go back to kitchen?")
            if interactable:
                basement, kitchen, world_value = False, True, 5
        if John.y <= 65 and John.x >= -10 and John.y <= 520:  # Furniture Collisions
            John.y = 65
        if John.y >= 0 and John.y <= 360 and John.x >= 355:
            playerX = 355
        if John.y  >= 350 and John.x >= -20 and John.x <= 520:
            John.y = 350
        if John.x <= 5 and John.y <= 400:  # Out of bounds
            John.x = 5
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
                if task_3:
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
        chests[1].update(530, 410, interactable, player_rect)
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
        if playerY >= 400 and playerX >= 95:  # Get to route 4
            route3, route4, world_value = False, True, 0
        elif playerX <= 10 and playerY < 295 and playerY >= 150:  # Get to route 2
            route3, route2, world_value = False, True, 1
        if playerX >= 465:  # Just a simple collision
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
        chests[2].update(580, 300, interactable, player_rect)  # Mano's hut chest
        out_of_bounds()
        npcs[3].update(100, 250, player_rect, "sleeping")  # Cat npc
        npcs[1].update(325, 240, player_rect, "mission2")
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
            playerY = 300  # Bed Bottom col
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
            Dummy = dummy(385, 290)
            playerX = 50
    while training_field:
        background = pygame.image.load('data/sprites/world/training_field.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        blacksmith_shop()
        if not task_3:
            npcs[3].update(100, 100, player_rect, "awake")  # Cat npc
            npcs[1].update(150, 100, player_rect, "mission1")  # Manos NPC
            Dummy.update(swordRect)  # Training Dummie
        player()  # Player
        blacksmith_col(), pause_menu(), out_of_bounds()
        if playerX <= 10:
            route4, training_field, world_value = True, False, 2
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
