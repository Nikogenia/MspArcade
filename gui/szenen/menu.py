# Eigene Module
from konstanten import *
from gui.szene import Szene
from werkzeuge import zeit

# Externe Bibliotheken
import pygame as pg


# Menu Szene Klasse
class MenuSzene(Szene):

    # Konstruktor
    def __init__(self, gui, daten):

        # Initialisiere Szene
        Szene.__init__(self, gui, daten)

        # Definiere Index
        self.index = 0

    # Starten
    def starten(self):
        pass

    # Render
    def render(self):

        # Fülle das Bild schwarz
        self.bild.fill(Farben.DUNKEL_SCHWARZ)

        # Zeichne Texte
        temp = self.gui.schriftarten.standard(200).render(str(self.index), True, Farben.WEISS)
        self.bild.blit(temp, ((self.bild.get_width() - temp.get_width()) // 2, self.bild.get_height() - 200))

    # Aktualisieren
    def aktualisieren(self):
        pass

    # Beenden
    def beenden(self):
        pass

    # Event
    def event(self, event):

        # Scroll System
        if len(self.gui.main.spielverwaltung.spiele) > 0:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    if self.index == 0:
                        self.index = len(self.gui.main.spielverwaltung.spiele) - 1
                    else:
                        self.index -= 1
                if event.key == pg.K_RIGHT:
                    if self.index == len(self.gui.main.spielverwaltung.spiele) - 1:
                        self.index = 0
                    else:
                        self.index += 1

        # Ausführen
        if len(self.gui.main.spielverwaltung.spiele) > 0:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.gui.main.tasks.append(self.gui.main.spielverwaltung.spiele[self.index].ausfuehren)
                    zeit.warte(20)
                    self.gui.main.spielverwaltung.spiele[self.index].beenden()
