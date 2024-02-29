# Standard
from __future__ import annotations
from typing import TYPE_CHECKING

# External
import nikocraft as nc
import pygame as pg

# Local
if TYPE_CHECKING:
    from window.window import Window


class PlayScene(nc.Scene):

    def __init__(self, window: Window, args):

        super(PlayScene, self).__init__(window, args)

        self.window: Window = window

        self.brightness: int = 180

        self.tick: float = 0

        self.reset: bool = False

    def render(self) -> None:

        font = self.window.font.get("title", 150)
        text = font.render("Lade Spiel", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 400))

        font = self.window.font.get("text", 30)
        text = font.render("Einen Moment Geduld bitte ...", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 600))

        font = self.window.font.get("title", 200)
        text = font.render("." * int((self.tick % 100) // 25), True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 650))

    def update(self) -> None:

        self.tick += self.dt

        if not self.window.main.game_manager.running_game:
            if self.reset:
                self.window.main.user_manager.current = ""
                self.window.change_scene("idle", transition_duration=12, transition_pause=7)
            else:
                self.window.change_scene("rating", transition_duration=12, transition_pause=7)

        # HALL OF FAME

        # by Valis World
        # Hallo Welt

        # by Linicus
        # Hello World

        # Debug screen
        self.window.debug_screen_left.append("")
        self.window.debug_screen_left.append(f"Tick: {self.tick:.1f}")

    def event(self, event: pg.event.Event) -> None:

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_n:
                self.window.main.game_manager.close_browser()
            if event.key == pg.K_m:
                self.window.main.game_manager.close_browser()
                self.reset = True

    def init(self) -> None:

        self.window.main.game_manager.start_game = True
