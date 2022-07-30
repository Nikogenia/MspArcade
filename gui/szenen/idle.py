# Eigene Module
from konstanten import *
from gui.szene import Szene

# Externe Bibliotheken
import pygame as pg


# IDLE Szene Klasse
class IdleSzene(Szene):

    # Konstruktor
    def __init__(self, gui, daten):

        # Initialisiere Szene
        Szene.__init__(self, gui, daten)

        # Definiere Frame
        self.frame = 0
        self.richtung = 0.3

    # Starten
    def starten(self):
        pass

    # Render
    def render(self):

        # Fülle das Bild schwarz
        self.bild.fill(Farben.DUNKEL_SCHWARZ)

        # Zeichne Texte
        deutsch = self.gui.schriftarten.standard(110).render("Druecke eine beliebige Taste", True, Farben.WEISS)
        self.bild.blit(deutsch, ((self.bild.get_width() - deutsch.get_width()) // 2, self.bild.get_height() - 200))

    # Aktualisieren
    def aktualisieren(self):

        # Erhöhe Frame
        self.frame += self.richtung

        # Setze Frame zurück
        if self.frame >= 10:
            self.richtung = -0.3
        elif self.frame <= 0:
            self.richtung = 0.3

    # Beenden
    def beenden(self):
        pass
