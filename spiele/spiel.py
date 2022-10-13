# System Module
from abc import ABC
from abc import abstractmethod


# Abstrakte Spiel Klasse
class Spiel(ABC):

    # Konstruktor
    def __init__(self, main, daten):

        # Speichere die Main
        self.main = main

        # Lade daten
        self.name = daten["name"]
        self.kurz_beschreibung = daten["kurz_beschreibung"]
        self.beschreibung = daten["beschreibung"]
        self.autor = daten["autor"]
        self.bild = daten["bild"]

    # Abstrakte Ausführen Funktion
    @abstractmethod
    def ausfuehren(self):
        pass

    # Abstrakte Aktiv Funktion
    @abstractmethod
    def aktiv(self):
        pass

    # Abstrakte Beenden Funktion
    @abstractmethod
    def beenden(self):
        pass

    # Abstrakte Menü Funktion
    @abstractmethod
    def menue(self):
        pass
