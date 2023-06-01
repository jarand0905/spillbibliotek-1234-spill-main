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
        self.wall = 0

        self.image = pygame.transform.scale(pygame.image.load('ball.png').convert_alpha(), (SCALEWIDTH * 2, SCALEHEIGHT * 2))
        self.rect = self.image.get_bounding_rect()
        self.radius = self.rect.width / 2

        self.velocity = Vector2(0, 0)
        self.cars = []
        self.goals = []

        self.wall_collide = False
    
    def reset_pos(self):
        self.pos = Vector2(WIDTH / 2, HEIGHT / 2)
        self.velocity = Vector2(0, 0)

    def update(self, seconds):
        if self.pos[0] + self.radius >= WIDTH * 0.98:
            self.velocity.x *= -1.1
            self.wall = 1
            self.wall_collide = True
        elif self.pos[0] - self.radius <= WIDTH * 0.02:
            self.velocity.x *= -1.1
            self.wall = 2
            self.wall_collide = True
        elif self.pos[1] + self.radius > HEIGHT * 0.97:
            self.velocity.y *= -1.1
            self.wall = 3
            self.wall_collide = True
        elif self.pos[1] - self.radius < HEIGHT * 0.03:
            self.velocity.y *= -1.1
            self.wall = 4
            self.wall_collide = True
        else:
            self.wall_collide = False

        if self.velocity.length() >= self.friction:
            self.velocity *= self.friction
        else:
            self.velocity = Vector2(0, 0)
        self.movement(seconds)
        self.rect.center = self.pos
        WIN.blit(self.image, ((self.rect.bottomright[0] - self.rect.bottomleft[0]) / 2 + self.rect.bottomleft[0] - self.image.get_width() / 2, (self.rect.bottomright[1] - self.rect.topright[1]) / 2 + self.rect.topright[1] - self.image.get_height() / 2))
        #pygame.draw.circle(WIN, (0,0,255), self.rect.center, self.radius)
        self.car_collision(seconds)
        self.check_goal()

    def movement(self, seconds):
        self.pos += Vector2(self.velocity.x, -self.velocity.y) * seconds
    
    def check_goal(self):
        for goal in self.goals:
            line = goal.line
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
                self.reset_pos()
                for car in self.cars:
                    car.reset_pos()
                goal.goals += 1
                    

    def car_collision(self, seconds):
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
                if dist_v.length() <= self.rect.width / 2 and not car.invul.active:
                    pygame.draw.circle(WIN, (0,0,0), closest, 4)
                    self.car_velocity_force = 1.2
                    self.adjusted_angle = 0
                    if closest == line[0] or closest == line[1]:
                        self.car_velocity_force = 0.6
                    self.velocity *= -1
                    if self.wall_collide:
                        car.invul.activate()
                        if self.wall == 1:
                            if line[0].x < line[1].x:
                                self.adjusted_angle = 90
                            else:
                                self.adjusted_angle = -90
                        if self.wall == 2:
                            if line[0].x < line[1].x:
                                self.adjusted_angle = -90
                            else:
                                self.adjusted_angle = 90
                        if self.wall == 3:
                            if line[0].y < line[1].y:
                                self.adjusted_angle = 90
                            else:
                                self.adjusted_angle = -90
                        if self.wall == 4:
                            if line[0].y < line[1].y:
                                self.adjusted_angle = -90
                            else:
                                self.adjusted_angle = 90
                        
                    angle = seg_v.angle_to(Vector2(-1, 0))
                    self.velocity.rotate_ip(-angle)
                    self.velocity = Vector2(-self.velocity.x, self.velocity.y)
                    self.velocity.rotate_ip(angle)
                    self.velocity += car.velocity * car.direction * self.car_velocity_force
                    self.velocity.rotate_ip(self.adjusted_angle)
                    if self.velocity.length() > 300:
                        self.velocity.scale_to_length(300)     

                else:
                    pygame.draw.circle(WIN, (0,0,255), closest, 4)
        self.check_goal()
        self.movement(seconds)
        self.check_goal()