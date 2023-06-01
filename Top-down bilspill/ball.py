import pygame
import math
from pygame import Vector2
from variables import *

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = Vector2(WIDTH / 2, HEIGHT / 2)
        self.bounce = 1.5
        self.friction = 0.99
        self.mass = 10

        self.image = pygame.transform.scale(pygame.image.load('ball.png').convert_alpha(), (SCALEWIDTH, SCALEHEIGHT))
        self.rect = self.image.get_bounding_rect()

        self.velocity = Vector2(-500, 0)
        self.cars = []

    def update(self, seconds):
        if self.pos[0] > WIDTH or self.pos[0] < 0:
            self.velocity.x *= -1
        if self.pos[1] > HEIGHT or self.pos[1] < 0:
            self.velocity.y *= -1
        if self.velocity.length() >= self.friction:
            self.velocity *= self.friction
        else:
            self.velocity = Vector2(0, 0)
        self.movement(seconds)
        self.rect.center = self.pos
        WIN.blit(self.image, ((self.rect.bottomright[0] - self.rect.bottomleft[0]) / 2 + self.rect.bottomleft[0] - self.image.get_width() / 2, (self.rect.bottomright[1] - self.rect.topright[1]) / 2 + self.rect.topright[1] - self.image.get_height() / 2))
        pygame.draw.circle(WIN, (0,0,255), self.rect.center, self.rect.width / 2)
        self.closest_point_on_seg(seconds)

    def movement(self, seconds):
        self.pos += Vector2(self.velocity.x, -self.velocity.y) * seconds
    
    def closest_point_on_seg(self, seconds):
        for car in self.cars:
            for line in car.collision_lines:
                closest = Vector2(0, 0)
                seg_v = Vector2(line[1] - line[0])
                pt_v = Vector2(self.rect.centerx - line[0].x, self.rect.centery - line[0].y)
                seg_v_unit = Vector2(seg_v.x / seg_v.length(), seg_v.y / seg_v.length())
                proj = pt_v.dot(seg_v_unit)
                if proj <= 0:
                    closest = line[0]
                elif proj >= seg_v.length():
                    closest = line[1]
                else:
                    proj_v = Vector2(seg_v_unit.x * proj, seg_v_unit.y * proj)
                    closest = proj_v + line[0]
                pygame.draw.line(WIN, (0,0,0), self.rect.center, closest)
                dist_v = Vector2(self.rect.centerx - closest.x, self.rect.centery - closest.y)
                if dist_v.length() <= self.rect.width / 2:
                    print('intersecting')
                    pygame.draw.circle(WIN, (0,0,0), closest, 4)
                    if closest == line[0]:
                        self.velocity *= -1
                        angle = seg_v.angle_to(Vector2(-1, 0))
                        self.velocity.rotate_ip(-angle)
                        self.velocity = Vector2(-self.velocity.x, self.velocity.y)
                        self.velocity.rotate_ip(angle)
                        self.velocity *= 0.6
                        self.velocity += car.velocity
                        self.movement(seconds)
                    if closest == line[1]:
                        self.velocity *= -1
                        angle = seg_v.angle_to(Vector2(-1, 0))
                        self.velocity.rotate_ip(-angle)
                        self.velocity = Vector2(-self.velocity.x, self.velocity.y)
                        self.velocity.rotate_ip(angle)
                        self.velocity += car.velocity * 1/2
                        self.velocity *= 0.6
                        self.movement(seconds)
                    else:
                        self.velocity *= -1
                        angle = seg_v.angle_to(Vector2(-1, 0))
                        self.velocity.rotate_ip(-angle)
                        self.velocity = Vector2(-self.velocity.x, self.velocity.y)
                        self.velocity.rotate_ip(angle)
                        self.velocity += car.velocity
                        self.velocity *= 1.2
                        self.movement(seconds)

                else:
                    pygame.draw.circle(WIN, (0,0,255), closest, 4)