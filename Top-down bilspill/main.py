import pygame
from pygame import Vector2
from ball import Ball
from cars import Car
from variables import *

#imp = pygame.image.load("C:\\Users\\onuca001\\OneDrive - Osloskolen\\Skrivebord\\IT2\\foo.png").convert()

BACKGROUND_COLOR = (150, 150, 150, 225)
running = True

cars = pygame.sprite.Group()
clock = pygame.time.Clock()
ball_group = pygame.sprite.GroupSingle()

keys = pygame.key.get_pressed()

def main():
    global seconds, elapsed
    pygame.init()
    player1 = Car([50, HEIGHT / 2], -90, 'p1')
    player2 = Car([WIDTH - 50, HEIGHT / 2], 90, 'p2')
    ball = Ball()
    ball_group.add(ball)
    cars.add(player1)
    cars.add(player2)
    ball.cars.append(player1)
    ball.cars.append(player2)
    while running:
        seconds = elapsed/1000.0
        WIN.fill(BACKGROUND_COLOR)
        checkEvents()
        cars.update(seconds)
        ball_group.update(seconds)
        pygame.display.update()
        elapsed = clock.tick(120)

def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()

main()