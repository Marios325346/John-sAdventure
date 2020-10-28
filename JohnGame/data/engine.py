import pygame, random
from pygame import *

screen = pygame.display.set_mode((640, 480))
pygame.init()

Pixel_font = pygame.font.Font("data/fonts/pixelfont.ttf", 14)

# Settings UI
settingsUI = pygame.image.load('data/ui/settings_screen.png')
setUIRect = settingsUI.get_rect()
setUIRect.center = (320, 250)

def settings_catalog():
    global settingsUI, setUIRect
    screen.blit(settingsUI, setUIRect)

# ----------- NON PLAYER CHARACTERS (NPC) ------------

catalogImg = pygame.image.load('data/sprites/catalog.png')
cynthiaImg = pygame.image.load("data/npc/Cynthia.png")


def cynthia(cynthiaX, cynthiaY, playerX, playerY):
    global catalogImg, cynthiaImg
    cynthia_x = cynthiaX
    cynthia_y = cynthiaY

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


gatoulisImg = pygame.image.load("data/npc/candy.png")


def candy(catX, catY, playerX, playerY):
    global catalogImg, gatoulisImg
    screen.blit(gatoulisImg, (catX, catY))
    gatoulis_text = Pixel_font.render("Meow meow meow", True, (255, 255, 255))
    gatoulis_text2 = Pixel_font.render("-Candy", True, (255, 255, 255))
    if playerX >= catX - 50 and playerX <= catX + 50 and playerY >= catY - 50 and playerY <= catY + 50:
        screen.blit(catalogImg, (100, 340))
        screen.blit(gatoulis_text, (120, 350))
        screen.blit(gatoulis_text2, (430, 430))
    return catX, catY


mauImg = pygame.image.load("data/npc/Mau.png")
mauRect = mauImg.get_rect()
mauRect.center = (250, 450)


def mau():
    global catalogImg, mauImg
    screen.blit(mauImg, mauRect)


manosImg = pygame.image.load("data/npc/manos.png")
manosRect = manosImg.get_rect()
manosRect.center = (240, 200)


def manos():
    global catalogImg, manosImg
    screen.blit(manosImg, manosRect)


traning_dummieImg = pygame.image.load('data/npc/training_dummie.png')
traning_dummieRect = traning_dummieImg.get_rect()
traning_dummieRect.center = (385, 290)


def training_dummie():
    global catalogImg, traning_dummieImg
    screen.blit(traning_dummieImg, traning_dummieRect)


blacksmithImg = pygame.image.load('data/npc/blacksmith_shop.png')
blacksmithRect = blacksmithImg.get_rect()
blacksmithRect.center = (400, 80)


def blacksmith_shop():
    global catalogImg, blacksmithImg
    screen.blit(blacksmithImg, blacksmithRect)