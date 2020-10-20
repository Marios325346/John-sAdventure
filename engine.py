import pygame
from pygame import *

screen = pygame.display.set_mode((640, 480))
pygame.init()
 

catalogImg = pygame.image.load('sprites/catalog.png')
Pixel_font = pygame.font.Font("fonts/pixelfont.ttf", 18)

cynthiaImg = pygame.image.load("npc/Cynthia.png")
def cynthia(cynthiaX,cynthiaY):
    global playerX , playerY
    global catalogImg, cynthiaImg
    screen.blit(cynthiaImg, (cynthiaX, cynthiaY))
    cynthia_text = Pixel_font.render("Good morning brother, your things are in the basement \n  once you get them meet your friend in the training field", True, (255,255,255))
    #if playerX >= 460 and playerX <= 575 and playerY >= 204 and playerY <= 290:
        #if event.key == pygame.K_RETURN:
            #screen.blit(catalogImg, (100, 340))
            #screen.blit(catalogText, (120, 350))
    return cynthiaX, cynthiaY
