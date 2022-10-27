# Eigene Module
from konstanten import *
from werkzeuge import bild

# Externe Bibliotheken
import pygame as pg
import cv2


# Hintergrund Klasse
class Hintergrund:

    # Konstruktor
    def __init__(self, gui):

        # Speichere die GUI
        self.gui = gui

        # Definiere Bild
        self.bild = pg.Surface(GUI_DIMENSION)

        # Lade Capture
        self.capture = cv2.VideoCapture(self.gui.main.main_konfigurierung.inhalt["hintergrund"].replace("$DATEN", PFAD_DATEN))

        # Definiere Frame
        self.frame = pg.Surface(GUI_DIMENSION)

    # Render
    def render(self):

        # Projiziere Bild
        self.bild.blit(self.frame, (0, 0))

        # Bild verdunkeln
        schwarz = pg.Surface(GUI_DIMENSION)
        schwarz.set_alpha(200)
        self.bild.blit(schwarz, dest=(0, 0))

    # Aktualisieren
    def aktualisieren(self):

        _, frame = self.capture.read()

        if not _:

            self.capture.release()

            self.capture = cv2.VideoCapture(self.gui.main.main_konfigurierung.inhalt["hintergrund"].replace("$DATEN", PFAD_DATEN))

            _, frame = self.capture.read()

        self.frame = bild.cv_zu_pygame(frame)
