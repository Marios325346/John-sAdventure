import pygame
from pygame import *

screen = pygame.display.set_mode((640, 480))
pygame.init()

catalogImg = pygame.image.load('data/sprites/catalog.png')
Pixel_font = pygame.font.Font("data/fonts/pixelfont.ttf", 18)


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

