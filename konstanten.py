# System Module
from enum import Enum

# Projekt Details
PROJEKT_NAME = "Maker Space Arcade"
PROJEKT_VERSION = "Alpha 1.1.1"
PROJEKT_KURZ_BESCHREIBUNG = "Ein MAKER SPACE Projekt für den Arcade Spielautomaten der Schule"
PROJEKT_BESCHREIBUNG = "Dieses Projekt beinhaltet die Kernsoftware für den Spielautomaten des Bodensee Gymnasiums Lindau. Sie soll die einzelnen Spiele verwalten und die Schüler auf den Automaten aufmerksam machen."
PROJEKT_AUTOREN = ["Nikolas (aka Nikocraft)", "Samuel (aka MakerSam)", "Linus"]
PYTHON_VERSION = "1.10.5"
PYTHON_BIBLIOTHEKEN = ["Pygame"]

# Datei Pfade
PFAD_RESSOURCEN = "./ressourcen"
PFAD_BILDER = f"{PFAD_RESSOURCEN}/bilder"
PFAD_SCHRIFTARTEN = f"{PFAD_RESSOURCEN}/schriftarten"
PFAD_DATEN = "./daten"
PFAD_PROTOKOLLE = f"{PFAD_DATEN}/protokolle"
PFAD_SPIELE = f"{PFAD_DATEN}/spiele"
PFAD_KONFIGURATIONEN = f"{PFAD_DATEN}/konfigurationen"

# GUI
GUI_WIDTH = 1920
GUI_HEIGHT = 1080
GUI_DIMENSION = [GUI_WIDTH, GUI_HEIGHT]
GUI_FPS = 60

# Szenen
SZENEN = {
    "lade": ("gui.szenen.lade", "LadeSzene"),
    "idle": ("gui.szenen.idle", "IdleSzene")
}


# Übergänge
class Uebergaenge(Enum):

    # Keine
    KEINE = 0

    # Blende
    BLENDE_NORMAL = 1
    BLENDE_SCHNELL = 2
    BLENDE_LANGSAM = 3

    # Wischen
    WISCHEN_LINKS = 4
    WISCHEN_RECHTS = 5
    WISCHEN_OBEN = 6
    WISCHEN_UNTEN = 7


# Farben
class Farben:

    # Grautöne
    DUNKEL_SCHWARZ = (0, 0, 0)
    SCHWARZ = (20, 20, 20)
    DUNKEL_GRAU = (60, 60, 60)
    GRAU = (110, 110, 110)
    HELL_GRAU = (190, 190, 190)
    WEISS = (230, 230, 230)
    HELL_WEISS = (255, 255, 255)

    # Rottöne
    HELL_GELB = (252, 255, 163)
    GELB = (255, 255, 25)
    DUNKEL_GELB = (224, 217, 0)
    ORANGE = (255, 187, 51)
    DUNKEL_ORANGE = (230, 153, 0)
    HELL_ROT = (255, 136, 77)
    ROT = (255, 0, 0)
    DUNKEL_ROT = (204, 0, 0)
    PINK = (255, 102, 255)
    HELL_VIOLETT = (196, 77, 255)
    VIOLETT = (115, 0, 230)
    DUNKEL_VIOLETT = (64, 0, 128)
    BRAUN = (117, 0, 0)
    DUNKEL_BRAUN = (74, 0, 0)

    # Blautöne
    HELL_CYAN = (153, 255, 255)
    CYAN = (0, 255, 255)
    DUNKEL_CYAN = (0, 179, 179)
    HELL_BLAU = (128, 170, 255)
    BLAU = (0, 42, 255)
    DUNKEL_BLAU = (0, 0, 179)

    # Grüntöne
    HELL_LIMONE = (179, 255, 179)
    LIMONE = (128, 255, 149)
    DUNKEL_LIMONE = (0, 255, 0)
    GRUEN = (0, 204, 0)
    DUNKEL_GRUEN = (0, 128, 0)
