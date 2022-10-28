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
        self.richtung = 0.4

    # Starten
    def starten(self):
        pass

    # Render
    def render(self):

        # Fülle das Bild schwarz
        self.bild.fill(Farben.DUNKEL_SCHWARZ)

        # Zeichne Texte
        hinweis = self.gui.schriftarten.standard(60).render("Drücke eine beliebige Taste", True, Farben.WEISS)
        hinweis = pg.transform.scale(hinweis, (hinweis.get_width() + self.frame * 4, hinweis.get_height() + self.frame * 0.2))
        self.bild.blit(hinweis, ((self.bild.get_width() - hinweis.get_width()) // 2, self.bild.get_height() - 200 - hinweis.get_height() // 2))

    # Aktualisieren
    def aktualisieren(self, no_input=False):

        # Erhöhe Frame
        self.frame += self.richtung

        # Setze Frame zurück
        if self.frame >= 15:
            self.richtung = -0.4
        elif self.frame <= 0:
            self.richtung = 0.4

    # Beenden
    def beenden(self):
        pass

    # Event
    def event(self, event):

        # Wenn eine beliebige Taste gedrückt wurde, Gehe zu Menu
        if event.type == pg.KEYDOWN:
            self.wechsel_szene("menu", Uebergaenge.BLENDE_NORMAL, {})
