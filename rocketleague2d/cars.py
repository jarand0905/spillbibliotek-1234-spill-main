import pygame
from pygame import Vector2
from variables import *

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

class Car(pygame.sprite.Sprite):
    def __init__(self, pos, rotation, player, image):
        super().__init__()
        self.startpos = [pos[0], pos[1]]
        self.pos = pos
        self.player = player
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (SCALEWIDTH, SCALEHEIGHT))
        self.rect = self.image.get_bounding_rect()
        self.mass = 100
        self.velocity = 0
        self.acceleration = 0
        self.startrotation = rotation
        self.rotation = rotation
        self.rotation_inc = 0
        self.boost = 1
        self.boost_amount = 25
        self.sladding = 1
        self.max_speed = 250
        self.invul = Timer(1000)

        self.corners = [self.get_corner(self.rect.topleft), self.get_corner(self.rect.topright),
        self.get_corner(self.rect.bottomright), self.get_corner(self.rect.bottomleft)]

    def display_boost(self):
        font = pygame.font.Font("freesansbold.ttf", 32)
        text = font.render(str(int(self.boost_amount)), True, pygame.Color("black"))
        textRect = text.get_rect()
        if self.player == 'p1':
            textRect.center = (WIDTH / 10, HEIGHT * 0.06)
        elif self.player == 'p2':
            textRect.center = (WIDTH / 10 * 9, HEIGHT * 0.06)
        WIN.blit(text, textRect)

    def reset_pos(self):
        self.pos = [self.startpos[0], self.startpos[1]]
        self.rotation = self.startrotation
        self.velocity = 0
        self.boost_amount = 25

    def controls(self, key, seconds):
        self.direction = Vector2(self.corners[1].x - self.corners[2].x, self.corners[2].y - self.corners[1].y).normalize() 

        if self.player == 'p1':
            if key[pygame.K_LSHIFT] and self.boost_amount > 0:
                self.boost = 1.5
                self.boost_amount -= 20*seconds
            else:
                self.boost = 1
            if key[pygame.K_SPACE]:
                self.sladding = 2
            else:
                self.sladding = 1
            if key[pygame.K_w]:
                if self.velocity < 0:
                    self.acceleration = 15*self.boost
                else:
                    self.acceleration = 6*self.boost
            elif key[pygame.K_s]:
                if self.velocity > 0:
                    self.acceleration = -20
                else:
                    self.acceleration = -2
            else:
                if self.velocity < -1:
                    self.acceleration = 2
                elif self.velocity > 1:
                    self.acceleration = -2
                else:
                    self.acceleration = 0
                    self.velocity = 0

            if key[pygame.K_a]:
                self.rotation_inc = 100*self.sladding
            elif key[pygame.K_d]:
                self.rotation_inc = -100*self.sladding
            else:
                self.rotation_inc = 0
            
            if self.boost == 1 and self.velocity >= self.max_speed:
                self.acceleration = -2

            if self.velocity > 0:
                if self.velocity + self.acceleration < self.velocity:
                    self.velocity += self.acceleration
                elif self.velocity + self.acceleration < self.max_speed*self.boost:
                    self.velocity += self.acceleration
            elif self.velocity + self.acceleration > -self.max_speed:
                self.velocity += self.acceleration
        
        elif self.player == "p2":
            if key[pygame.K_k] and self.boost_amount > 0:
                self.boost_amount -= 20*seconds
                self.boost = 1.5
            else:
                self.boost = 1
            if key[pygame.K_l]:
                self.sladding = 2
            else:
                self.sladding = 1
            if key[pygame.K_UP]:
                if self.velocity < 0:
                    self.acceleration = 8*self.boost
                else:
                    self.acceleration = 2*self.boost
            elif key[pygame.K_DOWN]:
                if self.velocity > 0:
                    self.acceleration = -8
                else:
                    self.acceleration = -2
            else:
                if self.velocity < -1:
                    self.acceleration = 2
                elif self.velocity > 1:
                    self.acceleration = -2
                else:
                    self.acceleration = 0
                    self.velocity = 0

            if key[pygame.K_LEFT]:
                self.rotation_inc = 100*self.sladding
            elif key[pygame.K_RIGHT]:
                self.rotation_inc = -100*self.sladding
            else:
                self.rotation_inc = 0
            
            if self.boost == 1 and self.velocity >= self.max_speed:
                self.acceleration = -2

            if self.velocity > 0:
                if self.velocity + self.acceleration < self.velocity:
                    self.velocity += self.acceleration
                elif self.velocity + self.acceleration < self.max_speed*self.boost:
                    self.velocity += self.acceleration
            elif self.velocity + self.acceleration > -self.max_speed:
                self.velocity += self.acceleration
                
        self.rotation += self.rotation_inc * seconds
        self.image_copy = pygame.transform.rotate(self.image, self.rotation)

    def movement(self, seconds):
        new_pos_x = self.pos[0] + self.direction.x * self.velocity * seconds
        new_pos_y = self.pos[1] - self.direction.y * self.velocity * seconds
        if new_pos_x >= WIDTH * 0.02 and new_pos_x <= WIDTH * 0.98:
            self.pos[0] = new_pos_x
        else:
            self.velocity = 0
        if new_pos_y >= HEIGHT * 0.03 and new_pos_y <= HEIGHT * 0.97:
            self.pos[1] = new_pos_y
        else:
            self.velocity = 0

    def get_corner(self, corner):
        return (Vector2(corner) - Vector2(self.rect.center)).rotate(-self.rotation) + Vector2(self.rect.center)
    
    def update(self, seconds):
        if self.invul.active:
            self.invul.update()
        self.controls(pygame.key.get_pressed(), seconds)
        self.movement(seconds)
        self.rect.center = self.pos

        self.corners = [self.get_corner(self.rect.topleft), self.get_corner(self.rect.topright),
        self.get_corner(self.rect.bottomright), self.get_corner(self.rect.bottomleft)]

        self.collision_lines = [[self.corners[0], self.corners[1]], [self.corners[1], self.corners[2]],
        [self.corners[2], self.corners[3]], [self.corners[3], self.corners[0]]]

        pygame.draw.lines(WIN, (255, 255, 0), True, self.corners, 3)
        WIN.blit(self.image_copy, ((self.rect.bottomright[0] - self.rect.bottomleft[0]) / 2 + self.rect.bottomleft[0] - self.image_copy.get_width() / 2, (self.rect.bottomright[1] - self.rect.topright[1]) / 2 + self.rect.topright[1] - self.image_copy.get_height() / 2))
        self.display_boost()
