import pygame
from pygame import Vector2
from ball import Ball
from cars import Car
from boost import Boost, Timer
from variables import *

pygame.init()

print(WIDTH, HEIGHT)
#imp = pygame.image.load("C:\\Users\\onuca001\\OneDrive - Osloskolen\\Skrivebord\\IT2\\foo.png").convert()
bg = pygame.transform.scale(pygame.image.load('map.png').convert_alpha(), (1366, 768))

BACKGROUND_COLOR = (150, 150, 150, 225)
running = True

cars = pygame.sprite.Group()
clock = pygame.time.Clock()
ball_group = pygame.sprite.GroupSingle()
goals = pygame.sprite.Group()
boosts = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
game_over = False

class all_sprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
    
    def reset(self):
        for sprite in self.sprites():
            sprite.__init__()

a_s = all_sprites()

def createboosts(p1, p2):
    b1 = Boost([WIDTH/4, HEIGHT * 0.3])
    b2 = Boost([WIDTH/2, HEIGHT * 0.1])
    b3 = Boost([WIDTH/4 * 3, HEIGHT * 0.3])
    b4 = Boost([WIDTH/4, HEIGHT * 0.7])
    b5 = Boost([WIDTH/2, HEIGHT * 0.9])
    b6 = Boost([WIDTH/4 * 3, HEIGHT * 0.7])
    boosts.add(b1, b2, b3, b4, b5, b6)
    for sprite in boosts.sprites():
        sprite.cars.append(p1)
        sprite.cars.append(p2)


def main():
    global seconds, elapsed
    p1goal = Goal('p1')
    p2goal = Goal('p2')
    player1 = Car([50, HEIGHT / 2], -90, 'p1', 'car.png')
    player2 = Car([WIDTH - 50, HEIGHT / 2], 90, 'p2', 'car2.png')
    ball = Ball()
    ball_group.add(ball)
    goals.add(p1goal, p2goal)
    cars.add(player1, player2)
    ball.goals.append(p1goal)
    ball.goals.append(p2goal)
    ball.cars.append(player1)
    ball.cars.append(player2)
    a_s.add(p1goal, p2goal, player1, player2, ball)
    createboosts(player1, player2)

    while running:
        seconds = elapsed/1000.0
        WIN.fill(BACKGROUND_COLOR)
        WIN.blit(bg, (0, 0))
        checkEvents()
        boosts.update()
        goals.update()
        cars.update(seconds)
        ball_group.update(seconds)
        pygame.display.update()
        elapsed = clock.tick(120)

def checkEvents():
    global game_over
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
        if event.type == pygame.KEYDOWN and game_over and event.key == pygame.K_r:
            game_over = False
            for sprite in a_s.sprites():
                sprite.reset_pos()
            

font = pygame.font.Font("freesansbold.ttf", 32)
font2 = pygame.font.Font("freesansbold.ttf", 100)

class Goal(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.goals = 0
        self.thickness = 3
        self.player = player
        if self.player == 'p1':
            self.text_pos = WIDTH/2 + WIDTH*0.05
            self.line = [Vector2(WIDTH * 0.021, HEIGHT * 20/56), Vector2(WIDTH * 0.021, HEIGHT * 36/56)]
        elif self.player == 'p2':
            self.text_pos = WIDTH/2 - WIDTH*0.05 
            self.line = [Vector2(WIDTH * 0.979, HEIGHT * 20/56), Vector2(WIDTH * 0.979, HEIGHT * 36/56)]

    def reset_pos(self):
        self.goals = 0

    def update(self):
        pygame.draw.line(WIN, (0, 0, 0), self.line[0], self.line[1], self.thickness)
        self.display_score()

    def display_score(self):
        global game_over
        if self.goals >= 10:
            game_over = True
        if game_over:
            text = font2.render("Player " + str(self.player[1]) + " vinner!", True, pygame.Color("black"))
            textRect = text.get_rect()
            textRect.center = (WIDTH/2,  100)
        else:
            text = font.render(str(self.goals), True, pygame.Color("black"))
            textRect = text.get_rect()
            textRect.center = (self.text_pos, 50)

        WIN.blit(text, textRect)

main()