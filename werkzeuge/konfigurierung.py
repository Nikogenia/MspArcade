# System Module
import json


# Konfigurierung Klasse
class Konfigurierung:

    # Konstruktor
    def __init__(self, pfad):

        # Speichere den Pfad
        self.pfad = pfad

        # Definiere Inhalt
        self.inhalt = {}

        # Lade Inhalt
        self.laden()

    # Laden
    def laden(self):

        # Versuche
        try:

            # Öffne Datei
            with open(self.pfad, mode="r", encoding="utf-8") as file:

                # Lade JSON String zu Dictionary
                self.inhalt = json.load(file)

        # Bei einem Fehler
        except (IOError, json.JSONDecodeError):

            # Setze den Inhalt zu einem leeren Dictionary
            self.inhalt = {}

    # Speichern
    def speichern(self):

        # Öffne Datei
        with open(self.pfad, mode="w", encoding="utf-8") as file:

            # Speichere Dictionary zu JSON String
            json.dump(self.inhalt, file, indent=4, separators=(',', ': '))
