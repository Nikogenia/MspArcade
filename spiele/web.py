# System Module
import subprocess

# Eigene Module
from konstanten import *
from spiele.spiel import Spiel

# Externe Bibliotheken
import pygame as pg


# Web Spiel Klasse
class WebSpiel(Spiel):

    # Konstruktor
    def __init__(self, main, daten):

        # Initialisiere Spiel
        Spiel.__init__(self, main, daten)

        # Lade daten
        self.url = daten["url"]

        # Definiere Prozess
        self.prozess = None

    # Ausführen Funktion
    def ausfuehren(self):
        return

        # Führe Prozess aus
        self.prozess = subprocess.Popen([self.main.main_konfigurierung.inhalt["browser"], "--start-fullscreen", self.url])
        self.prozess.wait()
        self.prozess = None

    # Aktiv Funktion
    def aktiv(self):
        return self.prozess is not None

    # Beenden Funktion
    def beenden(self):

        # Prozess beenden
        self.prozess.terminate()

    # Menü Funktion
    def menue(self):

        # Erstelle neues Bild
        self.ui = pg.Surface((800, 900))

        # Versuche Bild zu laden
        try:
            self.ui.blit(pg.image.load(self.bild.replace("$SPIELE", PFAD_SPIELE)), (0, 0))
        except OSError:
            self.ui.fill(Farben.GRAU)

        # Zeichne Titel
        #title = self.main.gui.schriftarten.standard(80).render(self.name, True, Farben.WEISS)
        #self.ui.blit(title, ((self.ui.get_width() - title.get_width()) // 2, 100))

        # Zeichne Rahmen
        pg.draw.rect(self.ui, Farben.WEISS, (0, 0, self.ui.get_width(), self.ui.get_height()), 5)

        # Skaliere Bild
        self.ui = pg.transform.scale(self.ui, self.ui_groesse)

        # Bild verdunkeln
        if self.ui_groesse == (640, 720):
            schwarz = pg.Surface(self.ui_groesse)
            schwarz.fill(Farben.SCHWARZ)
            schwarz.set_alpha(100)
            self.ui.blit(schwarz, (0, 0))
