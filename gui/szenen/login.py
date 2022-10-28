# System Module
import threading as th

# Eigene Module
from konstanten import *
from gui.szene import Szene
from werkzeuge import zeit

# Externe Bibliotheken
import pygame as pg


# Login Szene Klasse
class LoginSzene(Szene):

    # Konstruktor
    def __init__(self, gui, daten):

        # Initialisiere Szene
        Szene.__init__(self, gui, daten)

        # Definiere Frame
        self.frame = 0
        self.richtung = 0.6

        # Definiere Timeout Zeit
        self.timeout = zeit.laufzeit_zeit()

    # Starten
    def starten(self):
        pass

    # Render
    def render(self):

        # Fülle das Bild schwarz
        self.bild.fill(Farben.DUNKEL_SCHWARZ)

        # Zeichne Hinweis
        hinweis = self.gui.schriftarten.standard(40).render("HAAAAALLLLLLLLOOOOOOOO", True, Farben.WEISS)
        hinweis = pg.transform.scale(hinweis, (hinweis.get_width() + self.frame * 4, hinweis.get_height() + self.frame * 0.2))
        self.bild.blit(hinweis, ((self.bild.get_width() - hinweis.get_width()) // 2, self.bild.get_height() - 70 - hinweis.get_height() // 2))

    # Aktualisieren
    def aktualisieren(self, no_input=False):

        # Erhöhe Frame
        self.frame += self.richtung

        # Setze Frame zurück
        if self.frame >= 15:
            self.richtung = -0.6
        elif self.frame <= 0:
            self.richtung = 0.6

        if self.timeout + 5 < zeit.laufzeit_zeit():
            self.wechsel_szene("menu", Uebergaenge.BLENDE_NORMAL, {})

    # Beenden
    def beenden(self):
        pass

    # Event
    def event(self, event):
        pass
