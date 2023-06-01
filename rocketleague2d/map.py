import pygame
import math

WIDTH=900
HEIGHT=500
BLACK=(0,0,0)
WHITE=(255,255,255)
imp = pg.image.load("C:\\Users\\onuca001\\OneDrive - Osloskolen\\Skrivebord\\IT2\\foo.png").convert()

screen=pygame.display.set_mode((WIDTH,HEIGHT))

def paint_back():
    screen.fill(BLACK)
    pygame.draw.line(screen,WHITE,(WIDTH//2,0),(WIDTH//2,HEIGHT),2)




pygame.display.update()