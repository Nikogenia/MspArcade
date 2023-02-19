# Standard
from __future__ import annotations
from typing import TYPE_CHECKING
import math
import threading as th

# External
import nikocraft as nc
import pygame as pg

# Local
from constants import *
from game.game import Game
from window.draw_utils import black_rect

if TYPE_CHECKING:
    from window.window import Window


class DetailsScene(nc.Scene):

    def __init__(self, window: Window, args):

        super(DetailsScene, self).__init__(window, args)

        self.window: Window = window

        self.brightness: int = 180

        self.tick: float = 0
        self.timeout: float = 0

        self.running: bool = True

        self.game: Game = self.window.main.game_manager.current
        if nc.file.exists(f"{PATH_GAME}/{self.game.image_name}"):
            self.image: pg.Surface = pg.image.load(f"{PATH_GAME}/{self.game.image_name}")
        else:
            self.logger.warning(f"Couldn't load game image at '{PATH_GAME}/{self.game.image_name}'! Use black ...")
            self.image: pg.Surface = pg.Surface((800, 800))

    def render(self) -> None:

        # Game title
        font = self.window.font.get("title", 130)
        text = font.render(self.game.name, True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 80))

        # Game short description

        # Continue prompt
        font = self.window.font.get("text", 35)
        height = math.sin(self.tick / 10) * 15 + 960
        text = font.render("Drücke #, um mit diesem Spiel fortzufahren!", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, height))

    def update(self) -> None:

        self.tick += self.dt

        # Scene switching
        if self.tick - self.timeout > 800:
            self.window.change_scene("idle")

        # Debug screen
        self.window.debug_screen_left.append("")
        self.window.debug_screen_left.append(f"Tick: {self.tick:.1f}")
        self.window.debug_screen_left.append(f"Timeout: {800 - (self.tick - self.timeout):.1f}")
        self.window.debug_screen_left.append("")

    def event(self, event: pg.event.Event) -> None:

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                self.window.change_scene("menu", transition_duration=7, transition_pause=3)
            if event.key == pg.K_RETURN:
                self.window.change_scene("login")
