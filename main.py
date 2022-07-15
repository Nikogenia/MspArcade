# System Module
import sys
import os
import logging
import threading

# Eigene Module
from konstanten import *
from werkzeuge.konfigurierung import Konfigurierung
from werkzeuge import zeit


# Main Klasse
class Main:

    # Konstruktor
    def __init__(self, args):

        # Gebe Projekt Details in der Konsole aus
        print(PROJEKT_NAME.upper())
        print("-" * len(PROJEKT_NAME))
        print()
        print(PROJEKT_KURZ_BESCHREIBUNG)
        print()
        print("BESCHREIBUNG")
        print(PROJEKT_BESCHREIBUNG)
        print()
        print("DETAILS")
        print(f"Projekt Version: {PROJEKT_VERSION}")
        print("Projekt Autoren:")
        for autor in PROJEKT_AUTOREN:
            print(f"- {autor}")
        print(f"Python Version: {PYTHON_VERSION}")
        print("Python Bibliotheken:")
        for bibliothek in PYTHON_BIBLIOTHEKEN:
            print(f"- {bibliothek}")
        print()

        # Prüfe für Konsolen Argumente
        self.debug = "-d" in args

        # Erstelle Verzeichnisse
        for pfad in [PFAD_PROTOKOLLE, PFAD_SPIELE, PFAD_KONFIGURATIONEN]:
            if not os.path.exists(pfad):
                os.makedirs(pfad)

        # Räume das Protokollverzeichnis auf
        protokoll_dateien = []
        for eintrag in os.scandir(PFAD_PROTOKOLLE):
            if eintrag.is_file():
                if os.path.splitext(eintrag.name)[1] == ".log":
                    protokoll_dateien.append(eintrag.path)
        if len(protokoll_dateien) > 10:
            for i in range(10, len(protokoll_dateien)):
                os.remove(protokoll_dateien[i - 10])

        # Definiere Protokollierung
        self.protokollierung_format = logging.Formatter("[%(asctime)s] [%(name)s - %(threadName)s] [%(levelname)s] %(message)s", '%d/%b/%y %H:%M:%S')
        self.protokollierung_datei = logging.FileHandler(f"{PFAD_PROTOKOLLE}/protokoll_{zeit.protokollierung()}.log")
        self.protokollierung_konsole = logging.StreamHandler(sys.stdout)
        self.protokollierung_datei.setFormatter(self.protokollierung_format)
        self.protokollierung_konsole.setFormatter(self.protokollierung_format)
        self.protokollierung = logging.Logger(PROJEKT_NAME.upper(), logging.DEBUG if self.debug else logging.INFO)
        self.protokollierung.addHandler(self.protokollierung_datei)
        self.protokollierung.addHandler(self.protokollierung_konsole)

        # Gebe Laufzeitinformationen aus
        self.protokollierung.info(f"Debug Modus: {'Ja' if self.debug else 'Nein'}")
        self.protokollierung.info(f"Laufzeit Pfad: {os.path.abspath('.')}")
        self.protokollierung.info(f"Ressourcen Pfad: {os.path.abspath(PFAD_RESSOURCEN)}")
        self.protokollierung.info(f"Daten Pfad: {os.path.abspath(PFAD_DATEN)}")

    # Run Funktion
    def run(self):
        pass


# MAIN
if __name__ == '__main__':

    threading.main_thread().name = "Main"

    # Definiere Main Objekt
    main = Main(sys.argv)

    # Führe die Main aus
    main.run()
