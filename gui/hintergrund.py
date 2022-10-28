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

        # Aktuelle Hintergrund Helligkeit
        self.aktuelle_helligkeit = 100

    # Render
    def render(self):

        # Projiziere Bild
        self.bild.blit(self.frame, (0, 0))

        # Bild verdunkeln
        schwarz = pg.Surface(GUI_DIMENSION)
        schwarz.set_alpha(self.aktuelle_helligkeit)
        self.bild.blit(schwarz, dest=(0, 0))

    # Aktualisieren
    def aktualisieren(self):

        if self.aktuelle_helligkeit > self.gui.szene.hintergrund_helligkeit:
            self.aktuelle_helligkeit -= 5
        elif self.aktuelle_helligkeit < self.gui.szene.hintergrund_helligkeit:
            self.aktuelle_helligkeit += 5

        _, frame = self.capture.read()

        if not _:

            self.capture.release()

            self.capture = cv2.VideoCapture(self.gui.main.main_konfigurierung.inhalt["hintergrund"].replace("$DATEN", PFAD_DATEN))

            _, frame = self.capture.read()

        self.frame = bild.cv_zu_pygame(frame)
