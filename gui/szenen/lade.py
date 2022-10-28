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

        # Lade Fertig Bedingung
        self.fertig = daten["fertig"]

        # Lade Folge Szene
        self.folge_szene = daten["folge_szene"]
        self.folge_uebergang = daten["folge_uebergang"]
        self.folge_argumente = daten["folge_argumente"]

    # Starten
    def starten(self):

        self.hintergrund_helligkeit = 100

    # Render
    def render(self):

        # Fülle das Bild schwarz
        self.bild.fill(Farben.DUNKEL_SCHWARZ)

        # Zeichne Texte
        titel = self.gui.schriftarten.standard(90).render(PROJEKT_NAME, True, Farben.WEISS)
        self.bild.blit(titel, ((self.bild.get_width() - titel.get_width()) // 2, (self.bild.get_height() - titel.get_height()) // 2 - 50))
        laden = self.gui.schriftarten.standard(40).render(self.daten["text"] if "text" in self.daten else "Laden", True, Farben.WEISS)
        self.bild.blit(laden, ((self.bild.get_width() - laden.get_width()) // 2, (self.bild.get_height() - laden.get_height()) // 2 + 40))

        # Zeichne Laden
        punkte = self.gui.schriftarten.standard(90).render("." * (self.frame // 25), True, Farben.WEISS)
        self.bild.blit(punkte, ((self.bild.get_width() - punkte.get_width()) // 2, (self.bild.get_height() - punkte.get_height()) // 2 + 100))

    # Aktualisieren
    def aktualisieren(self, no_input=False):

        # Erhöhe Frame
        self.frame += 1

        # Setze Frame zurück
        if self.frame >= 100:
            self.frame = 0

        # Ist fertig
        if self.fertig():
            self.wechsel_szene(self.folge_szene, self.folge_uebergang, self.folge_argumente)

    # Beenden
    def beenden(self):
        pass

    # Event
    def event(self, event):
        pass
