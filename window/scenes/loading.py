# Standard
from __future__ import annotations
from typing import TYPE_CHECKING

# External
import nikocraft as nc
import pygame as pg

# Local
from constants import *
if TYPE_CHECKING:
    from window.window import Window


class LoadingScene(nc.Scene):

    def __init__(self, window: Window, args):

        super(LoadingScene, self).__init__(window, args)

        self.window: Window = window

        self.brightness: int = 180

        self.tick: int = 0

    def render(self) -> None:

        font = self.window.font.get("title", 150)
        text = font.render("Lade Ressourcen", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 400))

        font = self.window.font.get("text", 30)
        text = font.render("Einen Moment Geduld bitte ...", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 600))

        font = self.window.font.get("title", 200)
        text = font.render("." * int((self.tick % 100) // 25), True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 650))

    def update(self) -> None:

        self.tick += self.dt

        if self.tick > 40:
            self.window.change_scene("idle")

        # Debug screen
        self.window.debug_screen_left.append("")
        self.window.debug_screen_left.append(f"Tick: {self.tick:.1f}")
