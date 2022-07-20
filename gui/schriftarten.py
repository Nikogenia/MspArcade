# Eigene Module
from konstanten import *

# Externe Bibliotheken
import pygame as pg


# Schriftarten
class Schriftarten:

    # Konstruktor
    def __init__(self, gui):

        # Speichere GUI
        self.gui = gui

        # Definiere Cache
        self.cache = {}

    # Standard Schriftart
    def standard(self, groesse, *, fett = False, kursiv = False, unterstrichen = False):

        # Prüfe für Cache
        if ("standard", groesse) in self.cache.keys():

            # Hole Schriftart
            schriftart = self.cache[("standard", groesse)]

        # Ansonsten
        else:

            # Lade Schriftart
            schriftart = pg.font.Font(f"{PFAD_SCHRIFTARTEN}/standard.ttf", groesse)

            # Speichere Schriftart
            self.cache[("standard", groesse)] = schriftart

        # Formatiere Schriftart
        schriftart.bold = fett
        schriftart.italic = kursiv
        schriftart.underline = unterstrichen

        # Gebe Schriftart zurück
        return schriftart
