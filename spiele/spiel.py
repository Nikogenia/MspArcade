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

    # Abstrakte Ausführen Funktion
    @abstractmethod
    def ausführen(self):
        pass
