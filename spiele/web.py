# System Module
import subprocess

# Eigene Module
from spiele.spiel import Spiel

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
        pass
