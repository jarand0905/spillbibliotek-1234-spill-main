import pygame
from pygame import Vector2

SCALEWIDTH = 100
SCALEHEIGHT = 100
WIDTH, HEIGHT = 1200, 620
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND_COLOR = (150, 150, 150, 225)
running = True

cars = pygame.sprite.Group()

def main():
    pygame.init()
    player1 = Car()
    while running:
        WIN.fill(BACKGROUND_COLOR)
        checkEvents()
        cars.update()
        pygame.display.update()

def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        cars.add(self)
        self.pos = [WIDTH / 2, HEIGHT / 2]

        self.image = pygame.transform.scale(pygame.image.load('car.png').convert_alpha(), (SCALEWIDTH, SCALEHEIGHT))
        self.rect = self.image.get_bounding_rect()

        self.direction_vector = Vector2(0, 1)
        self.velocity = 0
        self.rotation = 0
        self.rotation_inc = 0
        self.boosting = False
        self.boost = 100
        self.boost_multiplier = 1.5
        self.sladding = False

    def movement(self, keys):
        if keys[pygame.K_SPACE] and self.boost > 0:
            self.boosting = True
            
        else:
            self.boosting = False
        if keys[pygame.K_LSHIFT]:
            self.sladding = True
        else:
            self.sladding = False
        if keys[pygame.K_w]:
            if self.boosting:
                self.velocity = 0.25 * self.boost_multiplier
            else:
                self.velocity = 0.25
        elif keys[pygame.K_s]:
            if self.boosting:
                self.velocity = 0.25 * self.boost_multiplier
            else:
                self.velocity = -0.25
        else:
            self.velocity = 0
            self.rotation_inc = 0
        if self.velocity != 0:
            if keys[pygame.K_a]:
                if self.sladding:
                    self.rotation_inc = 0.15
                else:
                    self.rotation_inc = 0.1
            elif keys[pygame.K_d]:
                if self.sladding:
                    self.rotation_inc = -0.15
                else:
                    self.rotation_inc = -0.1
            else:
                self.rotation_inc = 0
        self.direction_vector.rotate_ip(self.rotation_inc)
        self.pos[0] += self.direction_vector.x * self.velocity
        self.pos[1] -= self.direction_vector.y * self.velocity
        self.rotation += self.rotation_inc
        self.image_copy = pygame.transform.rotate(self.image, self.rotation)

    def update(self):
        self.movement(pygame.key.get_pressed())
        self.rect.center = self.pos
        WIN.blit(self.image_copy, ((self.rect.bottomright[0] - self.rect.bottomleft[0]) / 2 + self.rect.bottomleft[0] - self.image_copy.get_width() / 2, (self.rect.bottomright[1] - self.rect.topright[1]) / 2 + self.rect.topright[1] - self.image_copy.get_height() / 2))

main()