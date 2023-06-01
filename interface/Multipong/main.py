# Importerer bibliotekene som trengs for filen
import pygame
import random
import math
from pygame.locals import (K_LEFT, K_RIGHT)

import asyncio



pygame.init()

#Lager et pygame vindu med bredde og høyde basert på variabel verdiene over
vindu= pygame.display.set_mode([800,800])



#Lager en klasse for ball
class Ball:
    def __init__(self,x,y,radius,farge,vindusobjekt,xFart,yFart ):
        self.x=x
        self.y=y
        self.radius=radius
        self.farge=farge
        self.vindusobjekt=vindusobjekt
        self.xFart=xFart
        self.yFart=yFart

#Metode som tegner ballen
    def tegn(self):
        pygame.draw.circle(self.vindusobjekt,self.farge,(self.x,self.y),self.radius)
#Metode som gjør det mulig for ballen å forflytte seg
    def flytt(self):
        if ((self.x - self.radius) <= 0) or ((self.x + self.radius) >= self.vindusobjekt.get_width()):
            self.xFart = -self.xFart
        if ((self.y - self.radius) <= 0) or ((self.y + self.radius) >= self.vindusobjekt.get_height()):
            self.yFart = -self.yFart

        self.x = self.x + self.xFart
        self.y =self.y + self.yFart


#Lager en klasse for spiller(altså paddelen nederst i vinduet)
class Spiller:
    def __init__(self,x1,y1,x2,y2,farge,vindusobjekt,fart,tykkelse):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
        self.farge=farge
        self.vindusobjekt=vindusobjekt
        self.fart=fart
        self.tykkelse=tykkelse
#Metode som tegner spiller
    def tegn(self):
        pygame.draw.line(self.vindusobjekt,self.farge,(self.x1,self.y1),(self.x2,self.y2),self.tykkelse)
#Metode for å forflytte seg, uten å forlate spill vinduet
    def flytt(self,taster):
        if taster[K_LEFT]:
            if self.x1<=0:
                self.x1=0
                self.x2=200
            else:
                self.x1 -= self.fart
                self.x2 -= self.fart
        if taster[K_RIGHT]:
            if self.x1>=600:
                self.x1=600
                self.x2=800
            else:
                self.x1 =self.x1 + self.fart
                self.x2 =self.x2 + self.fart
#Metode som håndterer kollisjon mellom ballen og spiller
    def kollidering(self,ball):
        for ball in liste_med_baller:
                if ball.x>=self.x1 and ball.x<=self.x2 and ball.y+25 >= self.y1 and ball.y <= self.y1+1 :
                    ball.yFart = -ball.yFart
                    nyball(liste_med_baller)
                elif ball.x>=self.x1 and ball.x<=self.x2 and ball.y <= self.y1:
                    ball.yFart = ball.yFart
                elif ball.y>700:
                    global fortsett
                    fortsett = False
            



#Definerer en funksjon som tar imot en liste,lager ett nytt ball objekt og appender den i listen.
def nyball(liste):
    ball=Ball(100, 100, 20, (0, 0, 255), vindu,random.uniform(0,7) ,random.uniform(2,7))
    liste.append(ball)



async def main():
    '''
    #Definerer hvilken font som skal brukse, hvis eventuell tekst dukker opp i pygame vinduet
    font = pygame.font.SysFont("Sora", 24)
    '''

    #Definerer bildefrekvensen til pygame vinduet
    FPS = 60
    fpsClock = pygame.time.Clock()
    
    global liste_med_baller
    liste_med_baller=[]
    nyball(liste_med_baller)
    #Definerer global variabel som styrer hovedløkken
    global fortsett
    fortsett=True



    #Lager spiller objekt
    spiller1=Spiller(300,600,500,600,(255,255,255),vindu,10,15)

    #Hovedløkken som kjører pygame vinduet
    while fortsett:
        #Når pygame vinduet lukkes, vil løkken stoppe å kjøre
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fortsett = False

            #Definerer variabel som tar imot informasjon av hvilken tast som er trykket ned
        trykkede_taster= pygame.key.get_pressed()
        #Gir bakgrunnen til pygame vinduet en farge
        vindu.fill((65, 39, 94))

            #Tegner spiller objektet, og bruker flytt og kollidering metodene for å kunne flytte den samt ha kollisjon mellom ball og spiller
        spiller1.tegn()
        spiller1.flytt(trykkede_taster)
        spiller1.kollidering(liste_med_baller)
            #Går igjennom listen med baller og tegner dem samt gir dem egenskapen til å flytte seg
        for item in liste_med_baller:
            item.tegn()
            item.flytt()

            #Oppdaterer innholdet på pygame vinduet
        pygame.display.flip()
        await asyncio.sleep(0)
        '''
            #Bildefrekvensen blir satt til øvre grense 60 per sekund
        fpsClock.tick(FPS)
        '''

asyncio.run( main() )

