# Eigene Module
from konstanten import *
from gui.hintergrund import Hintergrund

# Externe Bibliotheken
import pygame as pg


# GUI Verwaltung Klasse
class GUIVerwaltung:

    # Konstruktor
    def __init__(self, main):

        # Speichere die Main
        self.main = main

        # Initialisiere GUI
        self.bildschirm = pg.Surface(GUI_DIMENSION)
        self.uhr = pg.time.Clock()
        self.aktiv = False
        pg.init()
        pg.display.set_caption("Maker Space Arcade")
        pg.mouse.set_visible(False)

        # Initialisiere Hintergrund
        self.hintergrund = Hintergrund(self)

    # Starten Funktion
    def starten(self):

        # Öffne GUI
        self.bildschirm = pg.display.set_mode(GUI_DIMENSION, pg.FULLSCREEN)

        # Kreislauf
        self.aktiv = True
        while self.aktiv:

            # Warte auf Uhr
            self.uhr.tick(GUI_FPS)

            # Verarbeite Events
            self.verarbeite_events()

            # Render Bildschirm
            self.render_bildschirm()

        # Beende Main
        self.main.beenden()

    # Beenden Funktion
    def beenden(self):

        # Beende GUI
        pg.quit()

    # Render Bildschirm
    def render_bildschirm(self):

        # Render Hintergrund
        self.hintergrund.render()
        self.bildschirm.blit(self.hintergrund.bild, (0, 0))

        # Aktualisiere den Bildschirm
        pg.display.flip()

    # Verarbeite Events
    def verarbeite_events(self):

        # Hole neue Events
        for event in pg.event.get():

            # Schließ Event
            if event.type == pg.QUIT:

                # Beende
                self.aktiv = False

            # Tastatur Event
            if event.type == pg.KEYDOWN:

                # Escape Taste
                if event.key == pg.K_ESCAPE:

                    # Beende
                    self.aktiv = False
