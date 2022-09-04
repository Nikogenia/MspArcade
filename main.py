# System Module
import sys
import os
import logging
import threading

# Eigene Module
from konstanten import *
from werkzeuge.konfigurierung import Konfigurierung
from werkzeuge import zeit
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""
from gui.verwaltung import GUI


# Main Klasse
class Main:

    # Konstruktor
    def __init__(self, args):

        # Prüfe für Konsolen Argumente
        self.debug = "-d" in args

        # Definiere Protokolldateipfad
        protokoll_pfad = f"{PFAD_PROTOKOLLE}/protokoll_{zeit.protokollierung()}.log"

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

        # Gebe Projekt Details aus
        print(projekt_details())
        with open(protokoll_pfad, "w", encoding="utf-8") as file:
            file.write(projekt_details() + "\n")

        # Definiere Protokollierung
        self.protokollierung_format = logging.Formatter("[%(asctime)s] [%(name)s - %(threadName)s] [%(levelname)s] %(message)s", '%d/%b/%y %H:%M:%S')
        self.protokollierung_datei = logging.FileHandler(protokoll_pfad, encoding="utf-8")
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

        # Lade Konfigurierungen
        self.protokollierung.info("Lade Konfigurierungen ...")
        self.main_konfigurierung = Konfigurierung(f"{PFAD_KONFIGURATIONEN}/main.json")
        self.spiele_konfigurierung = Konfigurierung(f"{PFAD_KONFIGURATIONEN}/spiele.json")

        # Initialisiere GUI
        self.protokollierung.info("Initialisiere GUI ...")
        self.gui = GUI(self)

    # Starten Funktion
    def starten(self):

        # Starte GUI
        self.protokollierung.info("Starte GUI ...")
        self.gui.starten()

    # Beenden Funktion
    def beenden(self):

        # Beende GUI
        self.protokollierung.info("Beende GUI ...")
        self.gui.beenden()

        # Speichere Konfigurierungen
        self.protokollierung.info("Speichere Konfigurierungen ...")
        self.main_konfigurierung.speichern()
        self.spiele_konfigurierung.speichern()


# Projekt Details
def projekt_details():

    # Baue den Text
    text = f"{PROJEKT_NAME.upper()}\n{'-' * len(PROJEKT_NAME)}\n\n{PROJEKT_KURZ_BESCHREIBUNG}\n\nBESCHREIBUNG\n{PROJEKT_BESCHREIBUNG}\n\n"
    text += f"DETAILS\nProjekt Version: {PROJEKT_VERSION}\nProjekt Autoren:\n"
    for autor in PROJEKT_AUTOREN:
        text += f"- {autor}\n"
    text += f"Python Version: {PYTHON_VERSION}\nPython Bibliotheken:\n"
    for bibliothek in PYTHON_BIBLIOTHEKEN:
        text += f"- {bibliothek}\n"

    # Gebe den Text zurück
    return text


# Main
if __name__ == '__main__':

    # Setze den Namen des Main Threads
    threading.main_thread().name = "Main"

    # Definiere Main Objekt
    main = Main(sys.argv)

    # Führe die Main aus
    main.starten()
