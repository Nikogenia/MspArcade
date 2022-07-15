# Eigene Module
from konstanten import *

# Externe Bibliotheken
import pygame as pg


# Hintergrund Klasse
class Hintergrund:

    # Konstruktor
    def __init__(self, gui):

        # Speichere die GUI
        self.gui = gui

        # Definiere bild
        self.bild = pg.Surface(GUI_DIMENSION)

        # Lade Bilder
        self.retro = pg.image.load(f"{PFAD_BILDER}/retro_hintergrund.jpg")
        self.retro = pg.transform.scale(self.retro, GUI_DIMENSION)

    # Render
    def render(self):

        # Projiziere Bild
        self.bild.blit(self.retro, dest=((GUI_WIDTH - self.retro.get_width()) / 2, (GUI_HEIGHT - self.retro.get_height()) / 2))

        # Bild verdunkeln
        schwarz = pg.Surface(GUI_DIMENSION)
        schwarz.set_alpha(200)
        self.bild.blit(schwarz, dest=(0, 0))

    # Aktualisieren
    def aktualisieren(self):
        pass
