import pygame
from pygame import *

screen = pygame.display.set_mode((640, 480))
pygame.init()

catalogImg = pygame.image.load('sprites/catalog.png')
Pixel_font = pygame.font.Font("fonts/pixelfont.ttf", 18)


def catalog_bubble(text):
    global catalogImg , interactable

    catalogText = Pixel_font.render(text, True, (255, 255, 255))
    screen.blit(catalogImg, (100, 340))
    screen.blit(catalogText, (120, 350))
    return(text)


