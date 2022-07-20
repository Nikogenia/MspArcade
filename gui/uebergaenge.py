# Eigene Module
from konstanten import Uebergaenge, GUI_DIMENSION, Farben

# Externe Bibliotheken
import pygame as pg


# Verarbeite Übergang
def verarbeite(gui):

    # Verarbeite richtigen Übergang
    if gui.letzte_szene.szenenwechsel_uebergang in [Uebergaenge.BLENDE_NORMAL, Uebergaenge.BLENDE_LANGSAM, Uebergaenge.BLENDE_SCHNELL]:
        beendet = verarbeite_blende(gui)
    elif gui.letzte_szene.szenenwechsel_uebergang in [Uebergaenge.WISCHEN_LINKS, Uebergaenge.WISCHEN_RECHTS, Uebergaenge.WISCHEN_OBEN, Uebergaenge.WISCHEN_UNTEN]:
        beendet = verarbeite_wischen(gui)
    else:
        beendet = True

    # Wenn der Übergang beendet ist
    if beendet:
        gui.letzte_szene = None
        gui.uebergang_daten.clear()


# Render Übergang
def render(gui):

    # Render richtigen Übergang
    if gui.letzte_szene.szenenwechsel_uebergang in [Uebergaenge.BLENDE_NORMAL, Uebergaenge.BLENDE_LANGSAM, Uebergaenge.BLENDE_SCHNELL]:
        render_blende(gui)


# Verarbeite Blende
def verarbeite_blende(gui):

    if "dauer" not in gui.uebergang_daten:
        gui.uebergang_daten["dauer"] = 60

    gui.uebergang_daten["dauer"] = gui.uebergang_daten["dauer"] - 1

    return gui.uebergang_daten["dauer"] <= 0


# Verarbeite Wischen
def verarbeite_wischen(gui):

    if "position" not in gui.uebergang_daten:
        gui.uebergang_daten["position"] = 100

    gui.uebergang_daten["position"] = gui.uebergang_daten["position"] - 1

    return gui.uebergang_daten["position"] <= 0


# Render Blende
def render_blende(gui):

    gui.szene.render()
    gui.letzte_szene.render()
    gui.szene.bild.set_alpha(255 - gui.uebergang_daten["dauer"] * 4.2)
    gui.letzte_szene.bild.set_alpha(gui.uebergang_daten["dauer"] * 4.2)

    gui.bildschirm.blit(gui.szene.bild, (0, 0))
    gui.bildschirm.blit(gui.letzte_szene.bild, (0, 0))


# Render Wischen
def render_wischen(gui):

    gui.szene.render()
    gui.letzte_szene.render()
    gui.szene.bild.set_alpha(255 - gui.uebergang_daten["dauer"] * 4.2)
    gui.letzte_szene.bild.set_alpha(gui.uebergang_daten["dauer"] * 4.2)

    gui.bildschirm.blit(gui.szene.bild, (0, 0))
    gui.bildschirm.blit(gui.letzte_szene.bild, (0, 0))
