import pygame
from pygame import Vector2
from variables import *
import math

class Timer:
	def __init__(self, duration):
		self.duration = duration
		self.active = False
		self.start_time = 0

	def activate(self):
		self.active = True
		self.start_time = pygame.time.get_ticks()

	def deactivate(self):
		self.active = False
		self.start_time = 0

	def update(self):
		current_time = pygame.time.get_ticks()
		if current_time - self.start_time >= self.duration:
			self.deactivate()

class Boost(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.w = 250
        self.h = 250
        self.position = pos
        self.cooldown = Timer(10000)
        self.images = ["boost.png", "disabledboost.png"]
        self.image = pygame.transform.scale(pygame.image.load(self.images[0]).convert_alpha(), (self.w, self.h))
        self.rect = self.image.get_bounding_rect()
        self.cars = []
        self.pickupdist = 30
    
    def update(self):
        for car in self.cars:
            dist = math.sqrt((car.pos[0]-self.position[0])**2 + (car.pos[1]-self.position[1])**2)
            if dist < self.pickupdist and not self.cooldown.active:
                self.cooldown.activate()
                self.image = pygame.transform.scale(pygame.image.load(self.images[1]).convert_alpha(), (self.w, self.h))
                if car.boost_amount + 50 > 100:
                    car.boost_amount = 100
                else:
                    car.boost_amount += 25
        if self.cooldown.active:
            self.cooldown.update()
            if not self.cooldown.active:
                self.image = pygame.transform.scale(pygame.image.load(self.images[0]).convert_alpha(), (self.w, self.h))

        self.rect.center = self.position
        WIN.blit(self.image, ((self.rect.bottomright[0] - self.rect.bottomleft[0]) / 2 + self.rect.bottomleft[0] - self.image.get_width() / 2, (self.rect.bottomright[1] - self.rect.topright[1]) / 2 + self.rect.topright[1] - self.image.get_height() / 2))

        
