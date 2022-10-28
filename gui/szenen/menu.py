# System Module
import threading as th

# Eigene Module
from konstanten import *
from gui.szene import Szene
from werkzeuge import zeit

# Externe Bibliotheken
import pygame as pg


# Menu Szene Klasse
class MenuSzene(Szene):

    # Konstruktor
    def __init__(self, gui, daten):

        # Initialisiere Szene
        Szene.__init__(self, gui, daten)

        # Definiere Index
        self.index = 0

        # Definiere Frame
        self.frame = 0
        self.richtung = 0.6

        # Definiere Timeout Zeit
        self.timeout = zeit.laufzeit_zeit()

    # Starten
    def starten(self):

        # Rendere Spiele Panels
        self.render_spiele()

    # Render
    def render(self):

        # Fülle das Bild schwarz
        self.bild.fill(Farben.DUNKEL_SCHWARZ)

        # Zeichne Spiele Panels
        if len(self.gui.main.spielverwaltung.spiele) > 0:
            panel = self.hole_spiel(self.index - 1).ui
            self.bild.blit(panel, ((self.bild.get_width() - panel.get_width()) // 2 - 600, (self.bild.get_height() - panel.get_height()) // 2 - 50))
            panel = self.hole_spiel(self.index + 1).ui
            self.bild.blit(panel, ((self.bild.get_width() - panel.get_width()) // 2 + 600, (self.bild.get_height() - panel.get_height()) // 2 - 50))
            panel = self.hole_spiel(self.index).ui
            self.bild.blit(panel, ((self.bild.get_width() - panel.get_width()) // 2, (self.bild.get_height() - panel.get_height()) // 2 - 42 - self.frame))

        # Zeichne Hinweis
        hinweis = self.gui.schriftarten.standard(40).render("Drücke START zum Spielen", True, Farben.WEISS)
        hinweis = pg.transform.scale(hinweis, (hinweis.get_width() + self.frame * 4, hinweis.get_height() + self.frame * 0.2))
        self.bild.blit(hinweis, ((self.bild.get_width() - hinweis.get_width()) // 2, self.bild.get_height() - 70 - hinweis.get_height() // 2))

    # Aktualisieren
    def aktualisieren(self, no_input=False):

        # Erhöhe Frame
        self.frame += self.richtung

        # Setze Frame zurück
        if self.frame >= 15:
            self.richtung = -0.6
        elif self.frame <= 0:
            self.richtung = 0.6

        if self.timeout + GUI_MENU_TIMEOUT < zeit.laufzeit_zeit():
            self.wechsel_szene("idle", Uebergaenge.BLENDE_NORMAL, {})

    # Beenden
    def beenden(self):
        pass

    # Event
    def event(self, event):

        # Scroll System
        if len(self.gui.main.spielverwaltung.spiele) > 0:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    if self.index == 0:
                        self.index = len(self.gui.main.spielverwaltung.spiele) - 1
                    else:
                        self.index -= 1
                    self.render_spiele()
                    self.timeout = zeit.laufzeit_zeit()
                if event.key == pg.K_RIGHT:
                    if self.index == len(self.gui.main.spielverwaltung.spiele) - 1:
                        self.index = 0
                    else:
                        self.index += 1
                    self.render_spiele()
                    self.timeout = zeit.laufzeit_zeit()

        # Ausführen
        if len(self.gui.main.spielverwaltung.spiele) > 0:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.wechsel_szene("login", Uebergaenge.BLENDE_NORMAL, {})
                    #th.Thread(target=self.gui.main.spielverwaltung.spiele[self.index].ausfuehren, name="Web Process").start()
                    #zeit.warte(6)
                    #self.hole_spiel(self.index).beenden()

    # Hole Spiel
    def hole_spiel(self, index):
        if index >= len(self.gui.main.spielverwaltung.spiele):
            return self.gui.main.spielverwaltung.spiele[0]
        return self.gui.main.spielverwaltung.spiele[index]

    # Render Spiele
    def render_spiele(self):
        self.hole_spiel(self.index - 1).ui_groesse = (640, 720)
        self.hole_spiel(self.index - 1).menue()
        self.hole_spiel(self.index + 1).ui_groesse = (640, 720)
        self.hole_spiel(self.index + 1).menue()
        self.hole_spiel(self.index).ui_groesse = (800, 900)
        self.hole_spiel(self.index).menue()
