# System Module
from abc import ABC, abstractmethod

# Eigene Module
from konstanten import *

# Externe Bibliotheken
import pygame as pg


# Szene Klasse
class Szene(ABC):

    # Konstruktor
    def __init__(self, gui, daten):

        # Speichere die GUI
        self.gui = gui

        # Speichere die Daten
        self.daten = daten

        # Definiere Bild
        self.bild = pg.Surface(GUI_DIMENSION)
        self.bild.set_colorkey(Farben.DUNKEL_SCHWARZ)

        # Definiere Szenenwechsel
        self.szenenwechsel_name = ""
        self.szenenwechsel_uebergang = Uebergaenge.KEINE
        self.szenenwechsel_daten = {}

    # Starten
    @abstractmethod
    def starten(self):
        pass

    # Render
    @abstractmethod
    def render(self):
        pass

    # Aktualisieren
    @abstractmethod
    def aktualisieren(self):
        pass

    # Beenden
    @abstractmethod
    def beenden(self):
        pass

    # Wechsel Szene
    def wechsel_szene(self, name, uebergang, daten):

        # Setze Szenenwechsel
        self.szenenwechsel_name = name
        self.szenenwechsel_uebergang = uebergang
        self.szenenwechsel_daten = daten
