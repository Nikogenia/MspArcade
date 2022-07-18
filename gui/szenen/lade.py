# Eigene Module
from konstanten import *
from gui.szene import Szene

# Externe Bibliotheken
import pygame as pg


# Lade Szene Klasse
class LadeSzene(Szene):

    # Konstruktor
    def __init__(self, gui):

        # Initialisiere Szene
        Szene.__init__(self, gui)

    # Starten
    def starten(self):
        pass

    # Render
    def render(self):

        # Fülle das Bild schwarz
        self.bild.fill(Farben.DUNKEL_SCHWARZ)

        # Zeichne Texte
        titel = self.gui.schriftart_standard_extrem_gross.render(PROJEKT_NAME, False, Farben.WEISS)
        self.bild.blit(titel, ((self.bild.get_width() - titel.get_width()) // 2, (self.bild.get_height() - titel.get_height()) // 2 - 50))
        loading = self.gui.schriftart_standard_normal.render("Loading ...", False, Farben.WEISS)
        self.bild.blit(loading, ((self.bild.get_width() - loading.get_width()) // 2, (self.bild.get_height() - loading.get_height()) // 2 + 40))

    # Aktualisieren
    def aktualisieren(self):
        pass

    # Beenden
    def beenden(self):
        pass
