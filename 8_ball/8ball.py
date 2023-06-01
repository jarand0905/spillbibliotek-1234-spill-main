import pygame as pg
import pymunk

import math

# Initialiserer/starter pygame
pg.init()

# Oppretter et vindu der vi skal "tegne" innholdet vårt
VINDU_BREDDE = 400
VINDU_HOYDE  = 500
vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])
    

class Ball:
  """Klasse for å representere en ball"""
  def __init__(self, x, y, xfart, yfart, radius, vindusobjekt):
    """Konstruktør"""
    self.x = x
    self.y = y
    self.xfart = xfart
    self.yfart = yfart
    self.radius = radius
    self.vindusobjekt = vindusobjekt
  
  def tegn_sirkel(self):
    """Metode for å tegne ballen"""
    pg.draw.circle(self.vindusobjekt, (255, 69, 0), (self.x, self.y), self.radius)

  def flytt_x(self):
    """Metode for å flytte ballen"""
    # Sjekker om ballen er utenfor høyre/venstre kant
    if ((self.x - self.radius) <= 0) or ((self.x + self.radius) >= self.vindusobjekt.get_width()):
      self.xfart = -self.xfart
    
    # Flytter ballen
    self.x += self.xfart

  def flytt_y(self):
    """Metode for å flytte ballen"""
    # Sjekker om ballen er utenfor høyre/venstre kant
    if ((self.y - self.radius) <= 0) or ((self.y + self.radius) >= self.vindusobjekt.get_height()):
      self.yfart = -self.yfart
        # Flytter ballen
    self.y += self.yfart

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
    pg.draw.line(vindu, (self.r, self.g, self.b), [self.x_start, self.y_start], [self.x_slutt, self.y_slutt], 3)


# Lager et Ball-objekt
ball = Ball(210, 250, 0, 0, 15, vindu)

friksjon = 0.01


# Gjenta helt til brukeren lukker vinduet
fortsett = True
while fortsett:
    pg.time.Clock().tick(120)
    # Sjekker om brukeren har lukket vinduet
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False
        
    #friksjon
    if ball.xfart > 0:
        ball.xfart = abs(ball.xfart) - friksjon
    if ball.yfart > 0:
        ball.yfart = abs(ball.yfart) - friksjon
    
    #mouse position
    mouse_position_x = pg.mouse.get_pos()[0]
    mouse_position_y = pg.mouse.get_pos()[1]

    #linje objekt
    linje = Linje(200,200,200, ball.x, ball.y, mouse_position_x, mouse_position_y )


    #registerer museklikk
    #fikse nestegang at man kan holde inne
    left, middle, right = pg.mouse.get_pressed()
    if left:
        linje.g = 0
        linje.b = 0
        lengde = math.sqrt((abs(linje.x_slutt) - abs(linje.x_start))**2 + (abs(linje.y_slutt) - abs(linje.y_start))**2)
        ball.xfart = lengde/100
        ball.yfart =lengde/100
        
        

    # Farger bakgrunnen lyseblå
    vindu.fill((0, 100, 0))

    # Tegner og flytter ballen
    ball.tegn_sirkel()
    ball.flytt_x()
    ball.flytt_y()

    linje.tegn_linje()


    #pg.draw.rect(vindu, (100, 0, 0), (ball.x, ball.y, 10, mouse_position))
    

    pg.draw.circle(vindu, (0, 0, 0), (13, 15), 15)
    pg.draw.circle(vindu, (0, 0, 0), (13, 242), 15)
    pg.draw.circle(vindu, (0, 0, 0), (13, 485), 15)
    #Høyre_hull
    pg.draw.circle(vindu, (0, 0, 0), (387, 15), 15)
    pg.draw.circle(vindu, (0, 0, 0), (387, 242), 15)
    pg.draw.circle(vindu, (0, 0, 0), (387, 485), 15)

    # Oppdaterer alt innholdet i vinduet
    pg.display.flip()

# Avslutter pygame
pg.quit()