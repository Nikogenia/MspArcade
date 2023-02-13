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
    from window.window import Window


class MenuScene(nc.Scene):

    def __init__(self, window: Window, args):

        super(MenuScene, self).__init__(window, args)

        self.window: Window = window

        self.brightness: int = 180

        self.tick: int = 0
        self.timeout: int = 0

    def render(self) -> None:

        font = self.window.font.get("text", 35)
        height = math.sin(self.tick / 10) * 15 + 940
        text = font.render("Wähle ein Spiel aus!", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, height))

    def update(self) -> None:

        self.tick += self.dt

        if self.tick - self.timeout > 150:
            self.window.change_scene("idle")

        # Debug screen
        self.window.debug_screen_left.append("")
        self.window.debug_screen_left.append(f"Tick: {self.tick:.1f}")
        self.window.debug_screen_left.append(f"Timeout: {self.tick - self.timeout:.1f}")

    def event(self, event: pg.event.Event) -> None:

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.window.change_scene("login")
