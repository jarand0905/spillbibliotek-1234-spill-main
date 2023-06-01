import pygame as pg
import time
import colorsys
import random
import sys

class Button:
    """ Klasse for knapper med tekst i pygame.
    
    Attributter:
        window (pg.Surface): pygame overflate (Surface) som knappen tegnes på
        text (str): teksten som skal stå på knappen
        default_color (tuple(int, int, int)): RGB-farge på knappen når musa ikke er over knappen
        hovered_color (tuple(int, int, int)): RGB-farge på knappen når musa er over knappen
        font (pg.font.Font): font for teksten til knappen
        center (tuple(int, int)): sentrum av rektangelet som omfavner teksten
        text_render (pg.Surface): rendering av teksten
        text_rect (pg.Rect): rektangel rundt teksten
        button_rect (pg.Rect): rektangel som danner grensene til knappen
        mouse_is_over (bool): er musa over knappen eller ikke
    
    Krever:
        pygame as pg

    """

    def __init__(self, window, text, default_color, hovered_color, text_size, center):
        """ Konstruktør 
        
        Parametre:
            window (pg.Surface): pygame overflate (Surface) som knappen tegnes på
            text (str): teksten som skal stå på knappen
            default_color (tuple(int, int, int)): RGB-farge på knappen når musa ikke er over knappen
            hovered_color (tuple(int, int, int)): RGB-farge på knappen når musa er over knappen
            text_size (int): størrelse på teksten
            center (tuple(int, int)): sentrum av rektangelet som omfavner teksten
        """
        
        self.window = window
        self.text = text
        self.default_color = default_color
        self.hovered_color = hovered_color
        self.font = pg.font.Font('freesansbold.ttf', text_size)
        self.center = center
        self.text_render = None
        self.text_rect = None
        self.button_rect = None
        self.mouse_is_over = False

    def render(self):
        """ Lager teksten og plasserer der den skal være (self.center) """
        # Lag tekst til knappen
        self.text_render = self.font.render(self.text, False, self.default_color)
        # Generer rektangelet som er rundt teksten
        self.text_rect = self.text_render.get_rect()
        # Plasser senter av teksten og rektangelet til angitt posisjon
        self.text_rect.center = self.center
        # Avstand fra teksten til kanten av rektangelet rundt
        border = self.text_rect.h/4
        # Rektangel rundt teksten som markerer knappen
        self.button_rect = pg.Rect(self.text_rect.x-border, self.text_rect.y-border, self.text_rect.width+2*border, self.text_rect.height+2*border)

    def mouse_is_over_button(self, mouse_x, mouse_y):
        """ Sjekker om gitt koordinat er over knappen 
        
        Parametre:
            mouse_x (int): x-posisjon til objektet man vil sjekke om er over knappen
            mouse_y (int): y-posisjon til objektet man vil sjekke om er over knappen
        
        Returnerer:
            True hvis objektet er over, ellers False

        """
        self.mouse_is_over = self.button_rect.x <= mouse_x <= self.button_rect.right and self.button_rect.y <= mouse_y <= self.button_rect.bottom
        return self.mouse_is_over

    def draw(self):
        """ Tegner knappen på skjermen """
        # Endre knappen på teksten dersom musa er over teksten
        if self.mouse_is_over:
            color = self.hovered_color
        else:
            color = self.default_color

        # Render teksten med riktig farge
        text_render = self.font.render(self.text, False, color)
        # Tegn en ramme (knapp) rundt teksten
        pg.draw.rect(self.window, color, self.button_rect, 2, int(self.button_rect.h/5))
        # Tegn teksten på skjermen
        self.window.blit(text_render, self.text_rect)
    
    def get_button_rect(self):
        """ Returnerer rektangelet (pg.Rect) som utgjør knappen"""
        return self.button_rect

class Game:
    """ Klasse som håndterer poengscore, game-over-skjerm og start-skjerm 
    
    Attributter:
        window (pg.Surface): pygame overflate (Surface) som ting tegnes på
        score (int): poengscoren til spilleren
        high_score (int): highscoren til spilleren
        high_score_font (pg.font.Font): fonttype for highscoren
        point_font (pg.font.Font): fonttype for scoren
        score_text_blinker (int): tellevariabel som anvendes for å få scoren til å 
            blinke når spilleren får en ny highscore

    Krever:
        sys (module)
        pygame as pg (module)
        Button (class)
        json (module)

    """

    def __init__(self, window):    
        """ Konstruktør 
        
        Parametre:
            window (pg.Surface): pygame overflate (Surface) som knappen tegnes på
        """


        self.window = window
        self.score = 0
        self.point_font = pg.font.Font('freesansbold.ttf', int(self.window.get_width()/2))
        self.score_text_blinker = 0
        
    def start_screen(self):
        """ Returnerer når spilleren har trykket på startknappen """

        # Lag knappen for å spille på nytt
        start_btn = Button(self.window, "Play", (255, 255, 255), (169, 169, 169), int(self.window.get_width()/15), (int(self.window.get_width()/2), int(self.window.get_height()/2)))
        start_btn.render()

        # Kjør til spilleren trykker på knappen eller lukker vinduet
        while True:
            # Lag en bakgrunn av svart på skjermen 
            self.window.fill((0,0,0))
            # Les museposisjon
            mouse = pg.mouse.get_pos()
            for ev in pg.event.get():
                # Stopp programmet
                if ev.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                # Sjekk om restart-knappen er klikket
                if start_btn.mouse_is_over_button(mouse[0], mouse[1]) and ev.type == pg.MOUSEBUTTONDOWN:
                    return

            start_btn.draw()
            # Oppdaterer deler av skjermen (området med knapp)
            pg.display.update(start_btn.get_button_rect())


    def draw_score(self):
        """ Tegner scoren til spilleren på skjermen. Dersom det er en highscore blinker teksten """
        # Fargen på teksten
        text_color = (255, 255, 255)

        text = self.point_font.render(str(self.score), False, text_color)
        # Generer rektangelet rundt teksten
        text_rect = text.get_rect()
        # Sentrer rektangelet (og teksten) til midt på skjermen
        text_rect.center = (self.window.get_width()/2, self.window.get_height()/2)
        self.window.blit(text, text_rect)
    
    def game_over_screen(self):
        """ Viser skjerm med high score og 'Spill på nytt' knapp frem 
        til brukeren trykker på den, da retunerer funksjonen """

        # Lag knapp for å spille på nytt
        restart_btn = Button(self.window, "Play again", (255, 255, 255), (169, 169, 169), int(self.window.get_width()/15), (self.window.get_width()/2, self.window.get_height()/2))
        restart_btn.render()


        # Kjør til spilleren spiller igjen eller lukker vinduet
        while True:
            self.window.fill((0,0,0))
            # Les museposisjon
            mouse = pg.mouse.get_pos()
            for ev in pg.event.get():
                # Stopp programmet
                if ev.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                # Sjekk om restart-knappen er klikket
                if restart_btn.mouse_is_over_button(mouse[0], mouse[1]) and ev.type == pg.MOUSEBUTTONDOWN:
                    return

            restart_btn.draw()
            # Oppdaterer deler av skjermen (områdene med knapp og tekst)
            pg.display.update(restart_btn.get_button_rect())

class Segment():
    """ Klasse for hvert ledd i slangen.
    
    Klasseattributter:
        objects (list): liste over alle instanser av dette objektet.
        colors (list): liste med RGB med farger som følger regnbuen delt opp i antall ledd
            det er i slangen.
    
    Attributter:
        window (pg.Surface): pygame overflate (Surface) som ballen tegnes på
        parent (Segmen): Segment-instants som er foran denne instansen i slangen
        size (int): størrelsen på siden i kvadratet i hvert segment
        pos (list(int, int)): posisjonskoordinater til øvre venstre hjørne til kvadratet
        color (tuple(int, int, int)): RGB-fargen til dette segmentet

    Krever:
        colorsys (module)
        pygame as pg (module)
    """

    objects =  []
    colors = []

    def __init__(self, window, parent_segment, size, start_pos):
        """ Konstruktør
        
        Parametre:
            window (pg.Surface): pygame overflate (Surface) som ballen tegnes på
            parent_segment (Segmen): Segment-instants som er foran denne instansen i slangen
            size (int): størrelsen på siden i kvadratet i hvert segment
            start_pos (list(int, int)): posisjonskoordinater til øvre venstre hjørne til kvadratet
        """

        self.window = window        
        self.parent = parent_segment
        self.size = size
        self.pos = start_pos
        self.color = None
        # Legg til den nye segmentet i slangen i starten (indeks 0) av arrayen,
        # slik at den hodet av slangen er sist i arrayen (indeks -1)
        self.objects.insert(0, self)
        
    def move(self):
        """ Oppdaterer posisjonen til segmentet """
        # Flytt segmentet en posisjon frem i rekken
        self.pos = self.parent.pos
        self.draw()

    def draw(self):
        """ Tegner segmentet på skjermen i korrekt farge"""
        # Finn fargen segmentet skal ha
        color = self.colors[self.objects.index(self)-1]
        # Svart ramme rundt hver segment
        border = 4
        # Tegn et rektangel som er 2px mindre i alle retninger enn self.size
        # for å få en svart (bakgrunnsfargen) kant rundt alle segmenter
        pg.draw.rect(self.window, (color), pg.Rect(self.pos[0]+border, self.pos[1]+border, self.size-border, self.size-border))
 
    @classmethod
    def gen_rainbow(self, n):
        """ Lager en liste med RGB-farger som har lengde lik antall segmenter i listen.
        
        Parametre:
            n (int): antall farger den skal lage (og dermed hvor mange deler den 
                splitte regnbuen i)
        """
        hsv_color = []
        # Generer farger med maks saturation, lightness,
        # men med varierende hue, for å skape en regnbue
        for i in range(n):
            hsv_color.append((i/(n), 1, 1))
        rgb_color = []
        for hsv in hsv_color:
            # Konverter HSV-fargen til RGB
            rgb_color.append(colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2]))
            # Skaler fargen med 255
            rgb_color[-1] = [int(rgb_color[-1][0]*255), int(rgb_color[-1][1]*255), int(rgb_color[-1][2]*255)]        
        # Oppdater farge-listen
        self.colors = rgb_color 

    @classmethod
    def get_all_segment_pos(self):
        """ Returnere en liste med tupler av posisjonene til alle segmentene """
        positions = []
        for i in self.objects:
            positions.append(i.pos)
        return positions

class LeaderSegment(Segment):
    """ Klasse for hodet til slangen 
    
    Attributter:
        movement_speed (int): hvor fort (mange piksler) hodet beveger seg hver gang
            posisjonen oppdateres. Denne må være lik sidene i kvadratet
        speed (tuple(int, int)): momentanfarten til hodet i x- og y-retning.
    
    Krever:
        pygame as pg (module)
        Segment (class)
    """
    def __init__(self, window, size, start_pos):
        """ Konstruktør
        
        Parametre:
            window (pg.Surface): pygame overflate (Surface) som ballen tegnes på
            size (int): størrelsen på siden i kvadratet i hvert segment
            start_pos (list(int, int)): posisjonskoordinater til øvre venstre hjørne til kvadratet
        """

        super().__init__(window, None, size, start_pos)
        self.movement_speed = size
        self.speed = [self.movement_speed, 0]
    
    def move(self):
        """ Oppdaterer posisjonen til slange-hodet basert på hastigheten """
        # Legg sammen indeks 0 av pos og speed listen, tilsvarende for indeks 1
        self.pos = [x + y for x, y in zip(self.pos, self.speed)]
        self.draw()

    def pressed_key(self, keys):
        """ Endrer fartsretningen til slangen basert på hvilken tast brukeren har trykket på.
        Om man taster motsatt retning av den veien slangen beveger seg dør man ikke. 
        
        Parametre:
            keys (pg.key): tastene som har blitt trykket
        
        Returnerer:
            True om et av tastetrykkene endret fartsretningen til slangen, ellers False.
        """

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            # Kun endre retning til venstre dersom den beveger seg i y-retning
            if self.speed[0] == 0:
                self.speed = [-self.movement_speed, 0]
                return True

        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            # Kun endre retning til høyre dersom den beveger seg i y-retning
            if self.speed[0] == 0:
                self.speed = [self.movement_speed, 0]
                return True

        elif keys[pg.K_UP] or keys[pg.K_w]:
            # Kun endre retning til opp dersom den beveger seg i x-retning
            if self.speed[1] == 0:
                self.speed = [0, -self.movement_speed]
                return True
        
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            # Kun endre retning til ned dersom den beveger seg i x-retning
            if self.speed[1] == 0:
                self.speed = [0, self.movement_speed]
                return True
        else:
            # Tastetrykket endret ikke retningen
            return False

    def touch_self(self):
        """ Sjekker om hodet til slangen har samme posisjon som noen 
        andre segmenter på slangen.
        
        Returnerer:
            True hvis hodet rører kroppen, ellers False
        """
        
        for i in super().objects[:-1]:
            if self.pos == i.pos:
                return True
        return False

    def is_outside_screen(self):
        """ Lar slangen gå rundt skjermen om den går ut av skjermen"""
        # Om slange-hodet er utenfor på høyre-siden
        # plasser det til venstre
        if self.pos[0] >= self.window.get_width():
            self.pos[0] = 0
            self.draw()

        # Om slange-hodet er utenfor på venstre-siden
        # plasser det til høyre
        if self.pos[0] < 0:
            self.pos[0] = self.window.get_width() - self.size
            self.draw()

        # Om slange-hodet er utenfor på bunnen
        # plasser det på toppen
        if self.pos[1] >= self.window.get_height():
            self.pos[1] = 0
            self.draw()

        # Om slange-hodet er utenfor på toppen
        # plasser det på bunnen
        if self.pos[1] < 0 :
            self.pos[1] = self.window.get_height() - self.size
            self.draw()

class Apple():
    """ Klasse for eple som slangen kan spise for at slangen skal bli lengre.
    
    Attributter:
        window (pg.Surface): pygame overflate (Surface) som ballen tegnes på
        size (int): størrelsen på siden i kvadratet i eplet (må være samme som på Segment)
        start_pos (list(int, int)): posisjonskoordinater til øvre venstre hjørne til kvadratet
    
    Krever:
        random (module)
        pygame as pg (module)
    """
    
    def __init__(self, window, size, start_pos):
        """ Konstruktør
        
        Parametre:
            window (pg.Surface): pygame overflate (Surface) som ballen tegnes på
            size (int): størrelsen på siden i kvadratet i eplet (må være samme som på Segment)
            start_pos (list(int, int)): posisjonskoordinater til øvre venstre hjørne til kvadratet
        """

        self.window = window
        self.size = size
        self.pos = start_pos

    def generate_new_pos(self, taken_positions):
        """ Plasserer eplet på en posisjon på brettet som ikke er brukt av slangen 
        
        Parametre:
            taken_positions (list): liste med tupler av med x- og y-posisjoner (int, int) som er opptatte.
        """
        # Kjør til gyldig posisjon er funnet
        while True:
            # Velg en tilfeldig x- og y-posisjon
            x = random.randint(0, (self.window.get_width()/self.size) -1)*self.size
            y = random.randint(0, (self.window.get_height()/self.size) -1)*self.size
            # Sjekk om posisjonen er brukt av slangen
            taken = False
            for pos in taken_positions:
                if x == pos[0] and y == pos[1]:
                    taken = True
                    break
            # Hvis posisjonen ikke er brukt, kan eplet plassers der
            if not taken:
                self.pos = [x, y]
                return
    
    def draw(self):
        """ Tegner eplet på skjermen """
        pg.draw.rect(self.window, (255, 0, 0), pg.Rect(self.pos[0]+2, self.pos[1]+2, self.size-2, self.size-2))

    def is_eaten(self, snake_head_pos):
        """ Sjekker om slangehodet har samme posisjon som eplet.
        
        Parametre:
            snake_head_pos (tuple(int, int)): posisjonen til slangehodet
        
        Returnerer:
            True hvis slangehodet og eple har samme posisjon, ellers False.
        """
        
        if snake_head_pos == self.pos:
            return True



pg.init()
SEGMENT_WIDTH = 30
WINDOW_WIDTH = SEGMENT_WIDTH*20
WINDOW_HEIGHT = SEGMENT_WIDTH*20
WINDOW = pg.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
CLOCK = pg.time.Clock()
# Pause mellom hver oppdatering av posisjon for å få slangen til å
# gå saktere (men uten å påvirke clockraten)
RUN_DELAY = 0.15
snake_head = LeaderSegment(WINDOW, SEGMENT_WIDTH, [300, 300])
# Antall ledd, i tillegg til hodet, i slangen ved starten av spillet
start_len = 2
# Generer regnbuefarger for slangen
Segment.gen_rainbow(start_len)
# Legg til start_len ledd
for i in range(start_len):
    Segment(WINDOW, Segment.objects[0], SEGMENT_WIDTH, [Segment.objects[0].pos[0]- SEGMENT_WIDTH, Segment.objects[0].pos[1]])
# Lag eplet
apple = Apple(WINDOW, SEGMENT_WIDTH, [None, None])
apple.generate_new_pos(Segment.get_all_segment_pos())
game = Game(WINDOW)

def run_game():
    """Kjører spill-loopen til spilleren dør"""
    time_last_run = time.time()
    # Kopier variablen ettersom den skal endres
    current_run_delay = RUN_DELAY
    # Noen ganger klarer spilleren å trykke to taster uten at posisjonen til 
    # slangen endres (hvis man har lav fart). Da får man en situasjon hvor 
    # slangen krasjer i seg selv. For å unngå dette slutter man å lese tastetrykk 
    # mellom oppdateringer av posisjonen til slangen når en tast som endrer retningen
    # til slangen har blitt trykket (f.eks. om man går oppover vil ikke pil opp endre 
    # retningen, så man vil fortsette å lese taster). 
    ready_for_key = True
    while True:
        # Frameraten bestemmer maks hastighet på spillet
        CLOCK.tick(60)
        WINDOW.fill((0, 0, 0))
        # Tegn scoren
        game.draw_score()

        for event in pg.event.get():
            # Stopp programmet
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # Les tastatur
        keys_pressed = pg.key.get_pressed()
        # Unngå dobbeltrykk av taster mellom oppdaterting av posisjon
        if ready_for_key:
            # Hvis tasten endrer retning
            if snake_head.pressed_key(keys_pressed):
                # Slutt å lese taster
                ready_for_key = False

        # Sjekk om det har passert mer enn run_delay 
        # tid siden sist oppdatering av posisjon
        now = time.time()
        if now  - time_last_run > current_run_delay:               
            # Flytt alle segmentene i slangen (begynnre med bakerste ledd)
            for i in Segment.objects:
                i.move()
            snake_head.is_outside_screen()
            
            # Posisjonen er oppdatert, så man kan igjen lese taster
            ready_for_key = True
            # Reset tiden for siste oppdatering av posisjon
            time_last_run = now

            if apple.is_eaten(Segment.objects[-1].pos):
                # Øk poengsummen
                game.score += 1
                # Legg til en ny link på slangen
                Segment(WINDOW, Segment.objects[0], SEGMENT_WIDTH, [Segment.objects[0].pos[0]- SEGMENT_WIDTH, Segment.objects[0].pos[1]])
                Segment.gen_rainbow(len(Segment.objects))
                # Lag et nytt eple
                apple.generate_new_pos(Segment.get_all_segment_pos())
                # Gjør pausene mellom hver gang slangens posisjon oppdateres mindre,
                # slik at den beveger seg fortere
                current_run_delay *= 0.95

            apple.draw()
            
            # Avslutt spill-loopen
            if snake_head.touch_self():
                return
            # Oppdater skjermen
            pg.display.flip()

def reset_game():
    """ Gjør spillet klar for en ny runde """
    # Generer regnbuefarger for slangen
    Segment.gen_rainbow(start_len)
    # Fjerner ledd i slangen slik at den blir start_len lang
    Segment.objects = Segment.objects[-start_len-1:]
    apple.generate_new_pos(Segment.get_all_segment_pos())
    # Resett scoren
    game.score = 0

# Vent på at spilleren er klar
game.start_screen()
while True:
    # Kjør spill-loopen
    run_game()
    # Vent på at spilleren starter spillet på nytt
    # eller lukker vinduet
    game.game_over_screen()
    # Resett spillet slik at det er klart for en ny runde
    reset_game()



