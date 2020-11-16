import pygame
screen = pygame.display.set_mode((640, 480))
pygame.init()
black = (0, 0, 0)  # Colors
Pixel_font = pygame.font.Font("data/fonts/pixelfont.ttf", 14)

cynthiaImg = pygame.image.load("data/npc/Cynthia.png")
catalogImg = pygame.image.load('data/sprites/catalog.png')
chestImg = pygame.image.load('data/sprites/chest.png')
chestRect = chestImg.get_rect()
candyImg = pygame.image.load("data/npc/candy.png")
candySleeping = pygame.image.load("data/npc/candy_sleeping.png")
mauImg = pygame.image.load("data/npc/Mau.png")
mauRect = mauImg.get_rect()
mauRect.center = (250, 450)
blacksmithImg = pygame.image.load('data/npc/blacksmith_shop.png')
blacksmithRect = blacksmithImg.get_rect()
blacksmithRect.center = (500, 60)
transparent_black = pygame.image.load("data/ui/black_overlay.png")
note = pygame.image.load('data/items/note.png')
cynthias_Note = pygame.image.load('data/items/cynthias_note.png')
manosImg = pygame.image.load("data/npc/manos.png")
showCatalog = True
y = 0
pl = 0

def hearts():
    health = 100
    max_health = 100
    heartX = 20
    heartY = 400
    heartImg = pygame.image.load('data/sprites/player/john_ui.png')
    hp_text = Pixel_font.render(str(health), True, (255, 0, 0))
    screen.blit(heartImg, (heartX, heartY))
    screen.blit(hp_text, (heartX + 87, heartY + 12))

def player_pocket(x):
    money = Pixel_font.render(str(x) + "€", True, black)
    screen.blit(money, (105, 443))

def chest(x, y, playerX, playerY, bool):
    global catalogImg
    chestRect.center = (x, y)
    screen.blit(chestImg, chestRect)
    text = Pixel_font.render("You opened the chest and found ", True, (255, 255, 255))
    text2 = Pixel_font.render("some coins. Now it's empty.", True, (255, 255, 255))
    if playerX >= x - 80 and playerX <= x and playerY <= y + 80:
        if bool:
            screen.blit(catalogImg, (100, 340))
            screen.blit(text, (120, 350))
            screen.blit(text2, (120, 380))
    return x, y


def cynthia(cynthiaX, cynthiaY, playerX, playerY, bool, interact_value):
    global catalogImg, cynthiaImg, showCatalog
    screen.blit(cynthiaImg, (cynthiaX, cynthiaY))
    cynthia_text = Pixel_font.render("Good morning brother.", True, (255, 255, 255))
    cynthia_text2 = Pixel_font.render("your sword is in the basement", True, (255, 255, 255))
    cynthia_text3 = Pixel_font.render("your teacher is waiting for you ", True, (255, 255, 255))
    cynthia_text4 = Pixel_font.render("in the training field. -Cynthia", True, (255, 255, 255))
    if playerX >= cynthiaX - 50 and playerX <= cynthiaX + 50 and playerY >= cynthiaY + 10 and playerY <= cynthiaY + 60:
        if bool:
            showCatalog = True
            if showCatalog:
                if interact_value == 1:
                    screen.blit(catalogImg, (100, 340))
                    screen.blit(cynthia_text, (120, 370))
                    screen.blit(cynthia_text2, (120, 390))
                elif interact_value == 2:
                    screen.blit(catalogImg, (100, 340))
                    screen.blit(cynthia_text3, (120, 370))
                    screen.blit(cynthia_text4, (120, 390))
                else:
                    showCatalog = False
    return cynthiaX, cynthiaY

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

def mau():
    global catalogImg, mauImg
    screen.blit(mauImg, mauRect)

def manos(mx, my, playerX, playerY, bool, count, interact_value):
    global catalogImg, manosImg
    Pixel_font = pygame.font.Font("data/fonts/pixelfont.ttf", 12)
    Pixel_font2 = pygame.font.Font("data/fonts/pixelfont.ttf", 13)
    dummieTask_Text = Pixel_font.render("hey man what's up?", True, (255, 255, 255))
    dummieTask_Text2 = Pixel_font.render("here for your daily training? good.", True, (255, 255, 255))
    dummieTask_Text3 = Pixel_font.render("start by showing me what you got", True, (255, 255, 255))
    controls_guide = Pixel_font2.render("(Press left shift or [] to attack)", True, (255, 255, 255))
    taskText = Pixel_font.render("not bad, we'll practice tomorrow.", True, (255, 255, 255))
    screen.blit(manosImg, (mx, my))
    if playerX >= mx - 50 and playerX <= mx + 50 and playerY >= my - 50 and playerY <= my + 50:
        screen.blit(catalogImg, (100, 340))
        if not bool and count == 0:  # Text before you defeat the dummy
            if interact_value == 0 or interact_value == 1:
                screen.blit(dummieTask_Text, (120, 355))
            elif interact_value == 2:
                screen.blit(dummieTask_Text2, (120, 380))
                screen.blit(dummieTask_Text3, (120, 405))
            else:
                screen.blit(controls_guide, (130, 390))
        elif bool and count == 0:  # Text when you defeat the dummy
            screen.blit(taskText, (120, 355))
            task1 = Pixel_font.render("if you wanna hang out,", True, (255, 255, 255))
            task2 = Pixel_font.render("come by my house later.", True, (255, 255, 255))
            screen.blit(task1, (120, 375))
            screen.blit(task2, (120, 395))
        elif bool and count == 1:  # Text when you talk at him in the hut
            manos1 = Pixel_font.render('hey John why did you come by so early?', True, (255, 255, 255))
            john1 = Pixel_font.render('"I found a letter at my house and"', True, (255, 255, 255))
            john2 = Pixel_font.render('my sister was missing.', True, (255, 255, 255))
            john3 = Pixel_font.render('Know anything about it?"', True, (255, 255, 255))
            manos2 = Pixel_font.render("I might have an idea what happened", True, (255, 255, 255))
            manos3 = Pixel_font.render("to your sister. Meet me outside.", True, (255, 255, 255))
            manos4 = Pixel_font.render("I'll explain everything later.", True, (255, 255, 255))
            if interact_value == 0 or interact_value == 1:
                screen.blit(manos1, (120, 355))
            elif interact_value == 2:
                screen.blit(john1, (120, 355))
                screen.blit(john2, (120, 375))
                screen.blit(john3, (120, 395))
            else:
                screen.blit(manos2, (120, 355))
                screen.blit(manos3, (120, 375))
                screen.blit(manos4, (120, 395))
    return mx, my

def cynthia_Note(playerX, playerY, bool):
    screen.blit(note, (120, 180))
    if playerX < 190 and playerY > 130 and playerY < 190:
        if bool:
            screen.blit(transparent_black, (0, 0))
            screen.blit(cynthias_Note, (220, 110))


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
    screen.blit(text0, (140, 250-y))
    screen.blit(text1, (140, 350-y))
    screen.blit(text2, (140, 500-y))
    screen.blit(text3, (140, 550-y))
    screen.blit(text5, (140, 670 - y))
    screen.blit(text6, (140, 690 - y))
    screen.blit(text7, (140, 740 - y))
    screen.blit(text9, (140, 760 - y))
    screen.blit(text8, (140, 810 - y))
