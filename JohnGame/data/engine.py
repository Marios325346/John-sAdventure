import pygame, random
from pygame import *

screen = pygame.display.set_mode((640, 480))
pygame.init()

# Colors
black = (0, 0, 0)

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
cynthiaImg = pygame.image.load("data/npc/Cynthia.png")


def player_pocket(currency):
    money = Pixel_font.render(str(currency) + "€", True, black)
    screen.blit(money, (105, 443))


chestImg = pygame.image.load('data/sprites/chest.png')
chestRect = chestImg.get_rect()
chestRect.center = (400, 105)


def chest():
    global catalogImg
    screen.blit(chestImg, chestRect)


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
def manos(mx, my,playerX, playerY, bool, count):
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


blacksmithImg = pygame.image.load('data/npc/blacksmith_shop.png')
blacksmithRect = blacksmithImg.get_rect()
blacksmithRect.center = (500, 60)


def blacksmith_shop():
    global catalogImg, blacksmithImg
    screen.blit(blacksmithImg, blacksmithRect)