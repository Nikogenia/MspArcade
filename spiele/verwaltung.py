# Eigene Module
from konstanten import *


# Spiele Verwaltung Klasse
class Spiele:

    # Konstruktor
    def __init__(self, main):

        # Speichere die Main
        self.main = main

        # Aktuelles Spiel
        self.aktuelles_spiel = None

    # Starten Funktion
    def starten(self):

        # Öffne GUI
        self.bildschirm = pg.display.set_mode(GUI_DIMENSION, pg.FULLSCREEN)

        # Kreislauf
        self.aktiv = True
        while self.aktiv:

            # Warte auf Uhr
            self.uhr.tick(GUI_FPS)

            # Verarbeite Szenen
            self.szene.aktualisieren()
            if self.szene.szenenwechsel_name != "":
                exec(f"from {SZENEN[self.szene.szenenwechsel_name][0]} import {SZENEN[self.szene.szenenwechsel_name][1]}")
                self.letzte_szene = self.szene
                exec(f"self.szene = {SZENEN[self.szene.szenenwechsel_name][1]}(self, self.szene.szenenwechsel_daten)")

            # Verarbeite Uebergang
            if self.letzte_szene:
                uebergaenge.verarbeite(self)

            # Verarbeite Events
            self.verarbeite_events()

            # Render Bildschirm
            self.render_bildschirm()

        # Beende Main
        self.main.beenden()

    # Beenden Funktion
    def beenden(self):

        # Beende GUI
        pg.quit()

    # Render Bildschirm
    def render_bildschirm(self):

        # Render Hintergrund
        self.hintergrund.render()
        self.bildschirm.blit(self.hintergrund.bild, (0, 0))

        # Render Szene
        if self.letzte_szene:
            uebergaenge.render(self)
        else:
            self.szene.render()
            self.bildschirm.blit(self.szene.bild, (0, 0))

        # Zeichne Debug Informationen
        if self.main.debug:
            name = self.schriftarten.standard(40).render(PROJEKT_NAME, False, Farben.HELL_WEISS)
            self.bildschirm.blit(name, (10, 10))
            version = self.schriftarten.standard(40).render(PROJEKT_VERSION, False, Farben.HELL_WEISS)
            self.bildschirm.blit(version, (10, 40))
            fps = self.schriftarten.standard(40).render(f"FPS: {self.uhr.get_fps():.1f}", False, Farben.HELL_WEISS)
            self.bildschirm.blit(fps, (10, 90))
            szene = self.schriftarten.standard(40).render(f"Szene: {self.szene.__class__.__name__}", False, Farben.HELL_WEISS)
            self.bildschirm.blit(szene, (10, 120))

        # Aktualisiere den Bildschirm
        pg.display.flip()

    # Verarbeite Events
    def verarbeite_events(self):

        # Hole neue Events
        for event in pg.event.get():

            # Schließ Event
            if event.type == pg.QUIT:

                # Beende
                self.aktiv = False

            # Tastatur Event
            if event.type == pg.KEYDOWN:

                # Escape Taste
                if event.key == pg.K_ESCAPE:

                    # Beende
                    self.aktiv = False
