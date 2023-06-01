import pygame
from pygame import Vector2
from variables import *

class Car(pygame.sprite.Sprite):
    def __init__(self, pos, rotation, player):
        super().__init__()
        self.pos = pos
        self.player = player
        if self.player == 'p1':
            self.image = pygame.transform.scale(pygame.image.load('car.png').convert_alpha(), (SCALEWIDTH, SCALEHEIGHT))
        elif self.player == 'p2':
            self.image = pygame.transform.scale(pygame.image.load('car2.png').convert_alpha(), (SCALEWIDTH, SCALEHEIGHT))
        self.rect = self.image.get_bounding_rect()
        self.mass = 100
        self.velocity = Vector2(0, 0)
        self.rotation = rotation
        self.rotation_inc = 0
        self.boosting = False
        self.boost = 100
        self.boost_multiplier = 1.5
        self.sladding = False
        self.p0 = (Vector2(self.rect.topleft) - Vector2(self.rect.center)).rotate(-self.rotation) + Vector2(self.rect.center)
        self.p1 = (Vector2(self.rect.topright) - Vector2(self.rect.center)).rotate(-self.rotation) + Vector2(self.rect.center) 
        self.p2 = (Vector2(self.rect.bottomright) - Vector2(self.rect.center)).rotate(-self.rotation) + Vector2(self.rect.center) 
        self.p3 = (Vector2(self.rect.bottomleft) - Vector2(self.rect.center)).rotate(-self.rotation) + Vector2(self.rect.center) 

    def controls(self, key, seconds):
        if self.player == 'p1':
            if key[pygame.K_LALT] and self.boost > 0:
                self.boosting = True
            else:
                self.boosting = False
            if key[pygame.K_LSHIFT]:
                self.sladding = True
            else:
                self.sladding = False
            if key[pygame.K_w]:
                if self.boosting:
                    self.velocity = Vector2(self.p1.x - self.p2.x, self.p2.y - self.p1.y).normalize() * 250 * self.boost_multiplier
                else:
                    self.velocity = Vector2(self.p1.x - self.p2.x, self.p2.y - self.p1.y).normalize() * 250
            elif key[pygame.K_s]:
                if self.boosting:
                    self.velocity = Vector2(self.p1.x - self.p2.x, self.p2.y - self.p1.y).normalize() * 250 * self.boost_multiplier
                else:
                    self.velocity = Vector2(self.p1.x - self.p2.x, self.p2.y - self.p1.y).normalize() * -250
            else:
                self.velocity = Vector2(0, 0)
                self.rotation_inc = 0
            if self.velocity.length() > 0:
                if key[pygame.K_a]:
                    if self.sladding:
                        self.rotation_inc = 250
                    else:
                        self.rotation_inc = 150
                elif key[pygame.K_d]:
                    if self.sladding:
                        self.rotation_inc = -250
                    else:
                        self.rotation_inc = -150
                else:
                    self.rotation_inc = 0
            self.rotation += self.rotation_inc * seconds
            self.image_copy = pygame.transform.rotate(self.image, self.rotation)

        elif self.player == 'p2':
            if key[pygame.K_RALT] and self.boost > 0:
                self.boosting = True
            else:
                self.boosting = False
            if key[pygame.K_RSHIFT]:
                self.sladding = True
            else:
                self.sladding = False
            if key[pygame.K_o]:
                if self.boosting:
                    self.velocity = Vector2(self.p1.x - self.p2.x, self.p2.y - self.p1.y).normalize() * 250 * self.boost_multiplier
                else:
                    self.velocity = Vector2(self.p1.x - self.p2.x, self.p2.y - self.p1.y).normalize() * 250
            elif key[pygame.K_l]:
                if self.boosting:
                    self.velocity = Vector2(self.p1.x - self.p2.x, self.p2.y - self.p1.y).normalize() * 250 * self.boost_multiplier
                else:
                    self.velocity = Vector2(self.p1.x - self.p2.x, self.p2.y - self.p1.y).normalize() * -250
            else:
                self.velocity = Vector2(0, 0)
                self.rotation_inc = 0
            if self.velocity.length() > 0:
                if key[pygame.K_k]:
                    if self.sladding:
                        self.rotation_inc = 250
                    else:
                        self.rotation_inc = 150
                elif key[pygame.K_SEMICOLON]:
                    if self.sladding:
                        self.rotation_inc = -250
                    else:
                        self.rotation_inc = -150
                else:
                    self.rotation_inc = 0
            self.rotation += self.rotation_inc * seconds
            self.image_copy = pygame.transform.rotate(self.image, self.rotation)

    def movement(self, seconds):
        self.pos[0] += self.velocity.x * seconds
        self.pos[1] -= self.velocity.y * seconds

    def update(self, seconds):
        self.controls(pygame.key.get_pressed(), seconds)
        self.movement(seconds)
        self.rect.center = self.pos
        self.p0 = (Vector2(self.rect.topleft) - Vector2(self.rect.center)).rotate(-self.rotation) + Vector2(self.rect.center)
        self.p1 = (Vector2(self.rect.topright) - Vector2(self.rect.center)).rotate(-self.rotation) + Vector2(self.rect.center) 
        self.p2 = (Vector2(self.rect.bottomright) - Vector2(self.rect.center)).rotate(-self.rotation) + Vector2(self.rect.center) 
        self.p3 = (Vector2(self.rect.bottomleft) - Vector2(self.rect.center)).rotate(-self.rotation) + Vector2(self.rect.center) 
        self.collision_lines = [[self.p0, self.p1], [self.p1, self.p2], [self.p2, self.p3], [self.p3, self.p0]]
        #self.collision_lines = [[self.p0, self.p1]]
        pygame.draw.lines(WIN, (255, 255, 0), True, [self.p0, self.p1, self.p2, self.p3], 3)
        WIN.blit(self.image_copy, ((self.rect.bottomright[0] - self.rect.bottomleft[0]) / 2 + self.rect.bottomleft[0] - self.image_copy.get_width() / 2, (self.rect.bottomright[1] - self.rect.topright[1]) / 2 + self.rect.topright[1] - self.image_copy.get_height() / 2))

