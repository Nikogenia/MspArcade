# Eigene Module
from konstanten import *
from gui.szene import Szene

# Externe Bibliotheken
import pygame as pg


# Lade Szene Klasse
class LadeSzene(Szene):

    # Konstruktor
    def __init__(self, gui, daten):

        # Initialisiere Szene
        Szene.__init__(self, gui, daten)

        # Definiere Frame
        self.frame = 0

    # Starten
    def starten(self):
        pass

    # Render
    def render(self):

        # Fülle das Bild schwarz
        self.bild.fill(Farben.DUNKEL_SCHWARZ)

        # Zeichne Texte
        titel = self.gui.schriftarten.standard(160).render(PROJEKT_NAME, True, Farben.WEISS)
        self.bild.blit(titel, ((self.bild.get_width() - titel.get_width()) // 2, (self.bild.get_height() - titel.get_height()) // 2 - 50))
        laden = self.gui.schriftarten.standard(60).render(self.daten["text"] if "text" in self.daten else "Laden", True, Farben.WEISS)
        self.bild.blit(laden, ((self.bild.get_width() - laden.get_width()) // 2, (self.bild.get_height() - laden.get_height()) // 2 + 40))

        # Zeichne Laden
        punkte = self.gui.schriftarten.standard(200).render("." * (self.frame // 25), True, Farben.WEISS)
        self.bild.blit(punkte, ((self.bild.get_width() - punkte.get_width()) // 2, (self.bild.get_height() - punkte.get_height()) // 2 + 100))

    # Aktualisieren
    def aktualisieren(self):

        # Erhöhe Frame
        self.frame += 1

        # Setze Frame zurück
        if self.frame >= 100:
            self.frame = 0

            self.wechsel_szene("idle", Uebergaenge.BLENDE_NORMAL, {})

    # Beenden
    def beenden(self):
        pass
