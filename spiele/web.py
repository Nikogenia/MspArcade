# System Module
import subprocess

# Eigene Module
from spiele.spiel import Spiel

# Externe Bibliotheken
import webview

# Web Spiel Klasse
class WebSpiel(Spiel):

    # Konstruktor
    def __init__(self, main, daten):

        # Initialisiere Spiel
        Spiel.__init__(self, main, daten)

        # Lade daten
        self.url = daten["url"]

        # Definiere Fenster
        self.fenster = None

    # Ausführen Funktion
    def ausfuehren(self):
        self.fenster = webview.create_window(self.name, url="https://www.google.com/")
        webview.start(gui="cef")

    # Aktiv Funktion
    def aktiv(self):
        return not self.fenster.closed

    # Beenden Funktion
    def beenden(self):
        self.fenster.destroy()

    # Menü Funktion
    def menue(self):
        pass
