import pygame, random
screen = pygame.display.set_mode((640, 480))
pygame.init()

black = (0, 0, 0) # Colors
Pixel_font = pygame.font.Font("data/fonts/pixelfont.ttf", 14)
def hearts():
    health = 100
    max_health = 100
    heartX = 20
    heartY = 400
    heartImg = pygame.image.load('data/sprites/player/john_ui.png')
    hp_text = Pixel_font.render(str(health), True, (255, 0, 0))
    screen.blit(heartImg, (heartX, heartY))
    screen.blit(hp_text, (heartX + 87, heartY + 12))

# ----------- NON PLAYER CHARACTERS (NPC) ------------
catalogImg = pygame.image.load('data/sprites/catalog.png')
chestImg = pygame.image.load('data/sprites/chest.png')
chestRect = chestImg.get_rect()
def player_pocket(x):
    money = Pixel_font.render(str(x) + "€", True, black)
    screen.blit(money, (105, 443))

def chest(x, y, playerX, playerY, bool):
    global catalogImg
    chestRect.center = (x, y)
    screen.blit(chestImg, chestRect)
    text = Pixel_font.render("You opened the chest and found ", True, (255, 255, 255))
    text2 = Pixel_font.render("some coins. Now it's empty.", True, (255, 255, 255))
    if playerX >= x - 150 and playerX <= x + 150 and playerY <= y + 100:
        if bool:
            screen.blit(catalogImg, (100, 340))
            screen.blit(text, (120, 350))
            screen.blit(text2, (120, 380))
    return x, y

cynthiaImg = pygame.image.load("data/npc/Cynthia.png")
def cynthia(cynthiaX, cynthiaY, playerX, playerY):
    global catalogImg, cynthiaImg

    screen.blit(cynthiaImg, (cynthiaX, cynthiaY))
    cynthia_text = Pixel_font.render("Good morning brother, your sword", True, (255, 255, 255))
    cynthia_text2 = Pixel_font.render("is in the basement, your teacher", True, (255, 255, 255))
    cynthia_text3 = Pixel_font.render("is waiting for you in the training", True, (255, 255, 255))
    cynthia_text4 = Pixel_font.render("field.   -Cynthia", True, (255, 255, 255))
    if playerX >= cynthiaX - 50 and playerX <= cynthiaX + 50 and playerY >= cynthiaY + 10 and playerY <= cynthiaY + 60:
        screen.blit(catalogImg, (100, 340))
        screen.blit(cynthia_text, (120, 350))
        screen.blit(cynthia_text2, (120, 370))
        screen.blit(cynthia_text3, (120, 390))
        screen.blit(cynthia_text4, (120, 410))

    return cynthiaX, cynthiaY

candyImg = pygame.image.load("data/npc/candy.png")
candySleeping = pygame.image.load("data/npc/candy_sleeping.png")
def candy(catX, catY, playerX, playerY, count):
    global catalogImg, candyImg
    gatoulis_text = Pixel_font.render("Meow meow meow", True, (255, 255, 255))
    gatoulis_text2 = Pixel_font.render("-Candy", True, (255, 255, 255))

    sleepyCandyText = Pixel_font.render("Zzzz zzzz zzzz...", True, (255, 255, 255))
    sleepyCandyText2 = Pixel_font.render("She fell asleep on the warm carpet.", True, (255, 255, 255))

    if playerX >= catX - 50 and playerX <= catX + 50 and playerY >= catY - 50 and playerY <= catY + 50:
        screen.blit(catalogImg, (100, 340))
        if count == 0:
            screen.blit(gatoulis_text, (120, 350))
            screen.blit(gatoulis_text2, (430, 430))
        else:
            screen.blit(sleepyCandyText, (120, 350))
            screen.blit(sleepyCandyText2, (120, 370))
            screen.blit(gatoulis_text2, (430, 430))
    if count == 0:
        screen.blit(candyImg, (catX, catY))
    else:
        screen.blit(candySleeping, (catX, catY))
    return catX, catY

mauImg = pygame.image.load("data/npc/Mau.png")
mauRect = mauImg.get_rect()
mauRect.center = (250, 450)
def mau():
    global catalogImg, mauImg
    screen.blit(mauImg, mauRect)

manosImg = pygame.image.load("data/npc/manos.png")
def manos(mx, my, playerX, playerY, bool, count):
    global catalogImg, manosImg
    Pixel_font2 = pygame.font.Font("data/fonts/pixelfont.ttf", 12)
    dummieTask_Text = Pixel_font.render("hey man what's up? here for", True, (255, 255, 255))
    dummieTask_Text2 = Pixel_font.render("your daily training? good.", True, (255, 255, 255))
    dummieTask_Text3 = Pixel_font.render("start by showing me what you got", True, (255, 255, 255))
    controls_guide = Pixel_font2.render("(Press left shift to attack)", True, (255, 255, 255))
    taskText = Pixel_font.render("Well done, i gotta go now see ya", True, (255, 255, 255))

    hutText1 = Pixel_font.render("Hey John what happened?", True, (255, 255, 255))

    screen.blit(manosImg, (mx, my))
    if playerX >= mx - 50 and playerX <= mx + 50 and playerY >= my - 50 and playerY <= my + 50:
        screen.blit(catalogImg, (100, 340))
        if not bool and count == 0:
            screen.blit(dummieTask_Text, (120, 355))
            screen.blit(dummieTask_Text2, (120, 380))
            screen.blit(dummieTask_Text3, (120, 405))
            screen.blit(controls_guide, (180, 435))
        elif bool and count == 0:
            screen.blit(taskText, (120, 355))
        elif bool and count == 1:
            screen.blit(hutText1, (120, 355))

    return mx, my

transparent_black = pygame.image.load("data/ui/black_overlay.png")
note = pygame.image.load('data/items/note.png')
cynthias_Note = pygame.image.load('data/items/cynthias_note.png')
def cynthia_Note(playerX, playerY, bool):
    screen.blit(note, (120, 180))
    if playerX < 190 and playerY > 130 and playerY < 190:
        if bool:
            screen.blit(transparent_black, (0, 0))
            screen.blit(cynthias_Note, (220, 110))

blacksmithImg = pygame.image.load('data/npc/blacksmith_shop.png')
blacksmithRect = blacksmithImg.get_rect()
blacksmithRect.center = (500, 60)
def blacksmith_shop():
    global catalogImg, blacksmithImg
    screen.blit(blacksmithImg, blacksmithRect)

def catalog_bubble(text):
    global catalogImg

    catalogText = Pixel_font.render(text, True, (255, 255, 255))
    screen.blit(catalogImg, (100, 340))
    screen.blit(catalogText, (120, 350))
    return text

def catalog_bubble2(text):
    catalogText = Pixel_font.render(text, True, (255, 255, 255))
    screen.blit(catalogText, (120, 380))
    return text


def controller(bool):
    controllerImg = pygame.image.load('data/ui/controller.png')
    if bool:
        screen.blit(controllerImg, (550, 430))


y = 0
def credits_text():
    global y
    john_logo = pygame.image.load('data/ui/logo.png')
    text0 = Pixel_font.render("JOHN'S ADVENTURE CHAPTER 1", True, (255, 255, 255))
    text1 = Pixel_font.render('Thank you for playing the game!', True, (255, 255, 255))
    text2 = Pixel_font.render('Credits', True, (255, 255, 255))
    text3 = Pixel_font.render('Story writer Manos Dazenis', True, (255, 255, 255))
    text4 = Pixel_font.render('Assistant Marios Papazogloy', True, (255, 255, 255))
    text5 = Pixel_font.render('__Programming Team__', True, (255, 255, 255))
    text6 = Pixel_font.render('Programmer Leader Marios Papazogloy', True, (255, 255, 255))
    text7 = Pixel_font.render('Level/ Art Design Marios Papazogloy', True, (255, 255, 255))
    text8 = Pixel_font.render('Music Design Thanos Pallis', True, (255, 255, 255))

    for i in range(1):
        y += 0.2
    screen.blit(text0, (140, 250-y))
    screen.blit(text1, (140, 350-y))
    screen.blit(john_logo, (140, 530))
    screen.blit(text2, (140, 500-y))
    screen.blit(text3, (140, 550-y))
    screen.blit(text4, (140, 570 - y))
    screen.blit(text5, (140, 670 - y))
    screen.blit(text6, (140, 690 - y))
    screen.blit(text7, (140, 770 - y))
    screen.blit(text8, (140, 810 - y))
