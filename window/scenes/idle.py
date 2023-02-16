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


class IdleScene(nc.Scene):

    def __init__(self, window: Window, args):

        super(IdleScene, self).__init__(window, args)

        self.window: Window = window

        self.brightness: int = 100

        self.tick: float = 0

    def render(self) -> None:

        font = self.window.font.get("title", 150)
        text = font.render("MAKER SPACE ARCADE", True, nc.RGB.BLACK)
        self.screen.blit(text, ((self.width - text.get_width()) / 2 + 5, 145))
        text = font.render("MAKER SPACE ARCADE", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 140))

        pg.draw.rect(self.screen, nc.RGB.BLACK, ((self.width - text.get_width() - 80) / 2 + 5, 125, text.get_width() + 80, text.get_height()), 6)
        pg.draw.rect(self.screen, nc.RGB.WHITE, ((self.width - text.get_width() - 80) / 2, 120, text.get_width() + 80, text.get_height()), 6)

        font = self.window.font.get("text", 40)
        height = math.sin(self.tick / 10) * 15 + 860
        text = font.render("Betätige einen beliebigen Knopf!", True, nc.RGB.BLACK)
        self.screen.blit(text, ((self.width - text.get_width()) / 2 + 4, height + 4))
        text = font.render("Betätige einen beliebigen Knopf!", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, height))

    def update(self) -> None:

        self.tick += self.dt

        # Debug screen
        self.window.debug_screen_left.append("")
        self.window.debug_screen_left.append(f"Tick: {self.tick:.1f}")

    def event(self, event: pg.event.Event) -> None:

        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_RETURN, pg.K_SPACE):
                self.window.change_scene("menu")
