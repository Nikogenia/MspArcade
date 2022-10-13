# Eigene Module
from konstanten import *
from werkzeuge import zeit


# Spiele Verwaltung Klasse
class SpielVerwaltung:

    # Konstruktor
    def __init__(self, main):

        # Speichere die Main
        self.main = main

        # Aktuelles Spiel
        self.aktuelles_spiel = -1

        # Definiere Spiele
        self.spiele = []

        # Definiere initialisiert
        self.initialisiert = False

    # Starten Funktion
    def starten(self):

        # Lade Spiele
        if "spiele" in self.main.spiele_konfigurierung.inhalt:
            for spiel in self.main.spiele_konfigurierung.inhalt["spiele"]:
                exec(f"from {SPIELARTEN[spiel['typ']][0]} import {SPIELARTEN[spiel['typ']][1]}")
                exec(f"self.spiele.append({SPIELARTEN[spiel['typ']][1]}(self.main, spiel))")

        zeit.warte(1)

        # Setze initialisiert auf true
        self.initialisiert = True

    # Beenden Funktion
    def beenden(self):
        pass

    # Ist initialisiert Funktion
    def ist_initialisiert(self):
        return self.initialisiert
