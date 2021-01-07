# COPYRIGHT 2020-2021 version 0.0.4
import pygame
from pygame import mixer
screen = pygame.display.set_mode((640, 480))
pygame.init()
black = (0, 0, 0)  # Colors
Pixel_font = pygame.font.Font("data/fonts/pixelfont.ttf", 14)
cynthiaImg = pygame.image.load("data/npc/Cynthia.png")
catalogImg = pygame.image.load('data/ui/catalog_bubble.png')
candyImg = pygame.image.load("data/npc/candy.png")
candySleeping = pygame.image.load("data/npc/candy_sleeping.png")
blacksmithImg = pygame.image.load('data/npc/blacksmith_shop.png')
blacksmithRect = blacksmithImg.get_rect()
blacksmithRect.center = (467, 60)
transparent_black = pygame.image.load("data/ui/black_overlay.png")
note = pygame.image.load('data/items/note.png')
cynthias_Note = pygame.image.load('data/items/cynthias_note.png')
manosImg = pygame.image.load("data/npc/manos.png")
showCatalog = True
y, pl = 0, 0




# OLD CODE BUT IT SOULDN'T BE REMOVED FOR NOW
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


player_money = 0 #  Currency
def player_pocket():
    global coinX,coinY
    global player_money
    money = Pixel_font.render(str(player_money) + "€", True, black)
    screen.blit(money, (coin_pos[0] + 40, coin_pos[1] + 15))

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


