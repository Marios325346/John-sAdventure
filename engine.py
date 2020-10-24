import pygame, random
from pygame import *

screen = pygame.display.set_mode((640, 480))
pygame.init()
 

catalogImg = pygame.image.load('sprites/catalog.png')
Pixel_font = pygame.font.Font("fonts/pixelfont.ttf", 14)

cynthiaImg = pygame.image.load("npc/Cynthia.png")

def cynthia(cynthiaX,cynthiaY,playerX,playerY):
    global catalogImg, cynthiaImg
    playerX = playerX
    playerY = playerY
    screen.blit(cynthiaImg, (cynthiaX, cynthiaY))
    cynthia_text = Pixel_font.render("Good morning brother, your sword", True, (255,255,255))
    cynthia_text2 = Pixel_font.render("is in the basement, your teacher", True, (255,255,255))
    cynthia_text3 = Pixel_font.render("is waiting for you in the training", True, (255, 255, 255))
    cynthia_text4 = Pixel_font.render("field.   -Cynthia", True, (255, 255, 255))
    if playerX >= cynthiaX - 50 and playerX <= cynthiaX + 50 and playerY >= cynthiaY + 10  and playerY <= cynthiaY + 60:
        print("Cynthia input")
        screen.blit(catalogImg, (100, 340))
        screen.blit(cynthia_text, (120, 350))
        screen.blit(cynthia_text2, (120, 370))
        screen.blit(cynthia_text3, (120, 390))
        screen.blit(cynthia_text4, (120, 410))
    return cynthiaX, cynthiaY

gatoulisImg = pygame.image.load("npc/gatoulis.png")
def gatoulis(catX , catY, playerX,playerY):
    global catalogImg , gatoulisImg
    playerX = playerX
    playerY = playerY
    screen.blit(gatoulisImg, (catX, catY))
    gatoulis_text = Pixel_font.render("Meow meow meow", True, (255, 255, 255))
    gatoulis_text2 = Pixel_font.render("-Gatoulis", True, (255, 255, 255))
    if playerX >= catX - 50 and playerX <= catX + 50 and playerY >= catY - 50 and playerY <= catY + 50:
        screen.blit(catalogImg, (100, 340))
        screen.blit(gatoulis_text, (120, 350))
        screen.blit(gatoulis_text2, (430, 430))
    return catX, catY





