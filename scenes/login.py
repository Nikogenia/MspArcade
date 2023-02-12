# Standard
from __future__ import annotations
from typing import TYPE_CHECKING
import math

# External
import nikocraft as nc
import pygame as pg

# Local
from constants import *
if TYPE_CHECKING:
    from window import Window


class LoginScene(nc.Scene):

    def __init__(self, window: Window, args):

        super(LoginScene, self).__init__(window, args)

        self.brightness: int = 180

        self.tick: int = 0
        self.timeout: int = 0

    def render(self) -> None:

        # Login title
        font = self.window.font.get("title", 130)
        text = font.render("Login", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 80))

        # QR-Code scanner
        pg.draw.rect(self.screen, nc.RGB.BLACK, (100, 300, 800, 460))
        pg.draw.rect(self.screen, nc.RGB.WHITE, (100, 300, 800, 460), 3)

        # Scanner description
        font = self.window.font.get("text", 30)
        text = font.render("QR-CODE SCANNER", True, nc.RGB.WHITE)
        self.screen.blit(text, (500 - text.get_width() / 2, 770))

        # Register info box
        pg.draw.rect(self.screen, nc.RGB.BLACK, (1150, 250, 650, 600))
        pg.draw.rect(self.screen, nc.RGB.WHITE, (1150, 250, 650, 600), 3)

        # Mebis QR-Code
        pg.draw.rect(self.screen, nc.RGB.BLACK, (1000, 575, 250, 250))
        pg.draw.rect(self.screen, nc.RGB.WHITE, (1010, 585, 230, 230))
        pg.draw.rect(self.screen, nc.RGB.WHITE, (1000, 575, 250, 250), 3)

        # Register title
        font = self.window.font.get("title", 90)
        text = font.render("Registrierung", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2, 260))

        # Register introduction
        font = self.window.font.get("text", 21)
        text = font.render("DU HAST NOCH KEINEN QR-CODE?", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2, 345))
        text = font.render("Kein Problem! Registriere", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2, 380))
        text = font.render("dich doch jetzt einfach.", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2, 415))
        text = font.render("So funktioniert es ...", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2, 450))

        # Register guide
        font = self.window.font.get("text", 16)
        link_font = self.window.font.get("text", 10)
        text = font.render("1. Scanne und öffne den QR-Code links.", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2, 510))
        text = link_font.render(" lernplattform.mebis.bayern.de/mod/data/view?d=146523", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2, 535))
        text = font.render("2. Melde dich, wenn nötig, mit  ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 570))
        text = font.render("   deinem Mebis Account an.     ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 595))
        text = font.render("3. Drücke 'Eintrag hinzufügen'. ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 630))
        text = font.render("4. Gebe einen Spielernamen ein. ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 665))
        text = font.render("5. Stelle sicher, dass die      ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 700))
        text = font.render("   Einzelansicht ausgewählt ist.", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 725))
        text = font.render("6. Jetzt siehst du deinen       ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 760))
        text = font.render("   QR-Code, den du zum einloggen", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 785))
        text = font.render("   nutzen kannst! Glückwunsch!  ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 810))

        # Login prompt
        font = self.window.font.get("text", 35)
        height = math.sin(self.tick / 10) * 15 + 960
        text = font.render("Halte deinen QR-Code vor die Kamera!", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, height))

    def update(self) -> None:

        self.tick += self.dt
        self.timeout += self.dt

        if self.timeout > 10000:
            self.window.change_scene("idle")

    def event(self, event: pg.event.Event) -> None:

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                self.window.change_scene("menu")
