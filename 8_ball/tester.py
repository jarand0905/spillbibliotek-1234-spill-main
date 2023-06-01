import pygame
import pymunk

pygame.init()

display = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 50

body = pymunk.Body()
body.position = 200,200
shape = pymunk.Circle(body, 10)
space.add(body,shape )

def game():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            display.fill((255, 255, 255))
            x, y =body.position
            pygame.draw.circle(display, (255,0,0), (int(x), int(y), 10))

            pygame.display.update()
            clock.tick(FPS)
            space.step(1/FPS)

game()
pygame.quit


