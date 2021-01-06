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
mauImg = pygame.image.load("data/npc/Mau.png")
mauRect = mauImg.get_rect()
mauRect.center = (250, 455)
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
def hearts():
    health = 100
    max_health = 100
    heartX = 20
    heartY = 400
    heartImg = pygame.image.load('data/sprites/player/john_ui.png')
    hp_text = Pixel_font.render(str(health), True, (255, 0, 0))
    screen.blit(heartImg, (heartX, heartY))
    screen.blit(hp_text, (heartX + 87, heartY + 12))

def candy(catX, catY, playerX, playerY, count):
    global catalogImg, candyImg
    gatoulis_text = Pixel_font.render("Meow meow meow", True, (0,0,0))
    gatoulis_text2 = Pixel_font.render("-Candy", True, (0,0,0))
    sleepyCandyText = Pixel_font.render("Zzzz zzzz zzzz...", True, (0,0,0))
    sleepyCandyText2 = Pixel_font.render("She fell asleep on the warm carpet.", True, (0,0,0))
    if playerX >= catX - 50 and playerX <= catX + 50 and playerY >= catY - 50 and playerY <= catY + 50:
        screen.blit(catalogImg, (100, 340))
        if count == 0:
            screen.blit(gatoulis_text, (120, 350)),screen.blit(gatoulis_text2, (430, 430))       
        else:
            screen.blit(sleepyCandyText, (120, 350)),screen.blit(sleepyCandyText2, (120, 370))         
            screen.blit(gatoulis_text2, (430, 430))
    if count == 0:
        screen.blit(candyImg, (catX, catY))
    else:
        screen.blit(candySleeping, (catX, catY))
    return catX, catY

def mau():
    global catalogImg, mauImg
    screen.blit(mauImg, mauRect)

def manos(mx, my, playerX, playerY, bool, count, interact_value):
    global catalogImg, manosImg
    Pixel_font = pygame.font.Font("data/fonts/pixelfont.ttf", 12)
    Pixel_font2 = pygame.font.Font("data/fonts/pixelfont.ttf", 13)
    dummieTask_Text = Pixel_font.render("hey man what's up?", True, (0,0,0))
    dummieTask_Text2 = Pixel_font.render("here for your daily training? good.", True, (0,0,0))
    dummieTask_Text3 = Pixel_font.render("start by showing me what you got", True, (0,0,0))
    controls_guide = Pixel_font2.render("(Press left shift or [] to attack)", True, (0,0,0))
    taskText = Pixel_font.render("not bad, we'll practice tomorrow.", True, (0,0,0))
    screen.blit(manosImg, (mx, my))
    if playerX >= mx - 50 and playerX <= mx + 50 and playerY >= my - 50 and playerY <= my + 30:
        screen.blit(catalogImg, (100, 340))
        if not bool and count == 0:  # Text before you defeat the dummy
            if interact_value == 0 or interact_value == 1:
                screen.blit(dummieTask_Text, (120, 355))
            elif interact_value == 2:
                screen.blit(dummieTask_Text2, (120, 380)), screen.blit(dummieTask_Text3, (120, 405))              
            else:
                screen.blit(controls_guide, (130, 390))
        elif bool and count == 0:  # Text when you defeat the dummy
            screen.blit(taskText, (120, 355))
            task1 = Pixel_font.render("if you wanna hang out,", True, (0,0,0))
            task2 = Pixel_font.render("come by my house later.", True, (0,0,0))
            screen.blit(task1, (120, 375)), screen.blit(task2, (120, 395))          
        elif bool and count == 1:  # Text when you talk at him in the hut
            manos1 = Pixel_font.render('hey John why did you come by so early?', True, (0,0,0))
            john1 = Pixel_font.render('"I found a letter at my house and"', True, (0,0,0))
            john2 = Pixel_font.render('my sister was missing.', True, (0,0,0))
            john3 = Pixel_font.render('Know anything about it?"', True, (0,0,0))
            manos2 = Pixel_font.render("I might have an idea what happened", True, (0,0,0))
            manos3 = Pixel_font.render("to your sister. Meet me outside.", True, (0,0,0))
            manos4 = Pixel_font.render("I'll explain everything later.", True, (0,0,0))
            if interact_value == 0 or interact_value == 1:
                screen.blit(manos1, (120, 355))
            elif interact_value == 2:
                screen.blit(john1, (120, 355)),screen.blit(john2, (120, 375)),screen.blit(john3, (120, 395))                           
            else:
                screen.blit(manos2, (120, 355)),screen.blit(manos3, (120, 375)),screen.blit(manos4, (120, 395))              
    return mx, my

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
    global player_money
    money = Pixel_font.render(str(player_money) + "€", True, black)
    screen.blit(money, (115, 445))


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