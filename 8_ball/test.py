import sys
 
import pygame
from pygame.locals import *

import pymunk

class Linje:
  def __init__(self, r, g, b, x_start, y_start, x_slutt, y_slutt):
    self.r = r
    self.g = g
    self.b = b
    self.x_start = x_start
    self.y_start = y_start
    self.x_slutt = x_slutt
    self.y_slutt = y_slutt


  def tegn_linje(self):
    "tegner linjen"
    pygame.draw.line(screen, (self.r, self.g, self.b), [self.x_start, self.y_start], [self.x_slutt, self.y_slutt], 3)


def create_Ball(space,height,width):
    body=pymunk.Body(1,100,body_type = pymunk.Body.DYNAMIC)
    body.position = (height,width)
    shape = pymunk.Circle(body,10)
    shape.elasticity = 1
    #body.velocity = (200,200)
    space.add(body,shape)
    return shape

def draw_balls(balls):
    for ball in balls:
        pos_x = int(ball.body.position.x)
        pos_y = int(ball.body.position.y)
        pygame.draw.circle(screen,(255,255,255),(pos_x,pos_y),10)
"""
def create_wall(space):
  body = pymunk.Body(1 , 100 , body_type = pymunk.Body.STATIC)
  body.position = (width,height)
  shape = pymunk.Segment(body, (0, height), (650, height), 5)
  space.add(body,shape)
  return shape

def draw_wall(walls):
  for wall in walls:
        pos_x = wall.body.position.x
        pos_y = wall.body.position.y
        print(pos_x)
        pygame.draw.line(screen,(0,0,0),(pos_x,pos_y),1)
"""
class Box:
    def __init__(self, p0=(0, 0), p1=(640, 480), d=2):
        self.p0 = p0
        self.p1 = p1
        x0, y0 = p0
        x1, y1 = p1
        self.pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for i in range(4):
            segment = pymunk.Segment(space.static_body, self.pts[i], self.pts[(i+1)%4], d)
            segment.elasticity = 0.5
            segment.friction = 1
            space.add(segment)



pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

space = pymunk.Space()
space.gravity = (0,0)

balls = []
balls.append(create_Ball(space,200,100))
balls.append(create_Ball(space,250,400))



walls = []
box=Box()
#walls.append(create_wall(space))
# Game loop.
while True:
  screen.fill((255, 255, 255))
  
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
      balls[1].body.velocity = (0,500)
    
  balls[1].body.velocity = balls[1].body.velocity * 0.99
  if abs(balls[0].body.velocity[0]) < 5 and abs(balls[0].body.velocity[1]) < 5:
    balls[0].body.velocity = (0,0)

  
  # Update.
  mouse_position_x = pygame.mouse.get_pos()[0]
  mouse_position_y = pygame.mouse.get_pos()[1]
  
  print(balls[0].body.position)
  screen.fill((0, 100, 0))
  pygame.draw.circle(screen, (0, 0, 0), (13, 15), 15)
  pygame.draw.circle(screen, (0, 0, 0), (13, 242), 15)
  pygame.draw.circle(screen, (0, 0, 0), (13, 460), 15)
  #HÃ¸yre_hull
  pygame.draw.circle(screen, (0, 0, 0), (620, 15), 15)
  pygame.draw.circle(screen, (0, 0, 0), (620, 242), 15)
  pygame.draw.circle(screen, (0, 0, 0), (620, 460), 15)
  
  
  # Draw.
  linje = Linje(200,200,200, balls[1].body.position.x, balls[1].body.position.y, mouse_position_x, mouse_position_y)
  linje.tegn_linje()
  
  draw_balls(balls)
  pygame.draw.rect(screen,(0,0,0),(box.p0+box.p1),6)
  #draw_wall(walls)
  space.step(1/50) 
  fpsClock.tick(fps)
  pygame.display.flip()