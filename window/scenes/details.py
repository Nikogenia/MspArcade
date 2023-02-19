# Standard
from __future__ import annotations
from typing import TYPE_CHECKING
import math

# External
import nikocraft as nc
import pygame as pg

# Local
from constants import *
from game.game import Game
from window.draw_utils import black_rect, split_text

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

        # Star data
        img = pg.image.load(f"{PATH_IMAGE}/star.png")
        self.star_mask: pg.Mask = pg.mask.from_surface(img)
        self.stars: float = 0
        self.rating_count: int = 0

        self.game: Game = self.window.main.game_manager.current
        if nc.file.exists(f"{PATH_GAME}/{self.game.image_name}"):
            self.image: pg.Surface = pg.transform.scale(pg.image.load(f"{PATH_GAME}/{self.game.image_name}"), (650, 650))
        else:
            self.logger.warning(f"Couldn't load game image at '{PATH_GAME}/{self.game.image_name}'! Use black ...")
            self.image: pg.Surface = pg.Surface((650, 650))

    def render(self) -> None:

        # Render stars
        for star in range(5):
            value_mask = pg.mask.Mask((max(self.stars - star, 0) * 64, 64), True)
            overlap_mask = self.star_mask.overlap_mask(value_mask, (0, 0))
            self.screen.blit(self.star_mask.to_surface(setcolor=nc.RGB.GRAY60, unsetcolor=(0, 0, 0, 0)), (self.width / 2 - 200 + star * 80, 40))
            self.screen.blit(overlap_mask.to_surface(setcolor=nc.RGB.GOLD1, unsetcolor=(0, 0, 0, 0)), (self.width / 2 - 200 + star * 80, 40))
            outline = self.star_mask.outline(1)
            for i, p in enumerate(outline):
                pg.draw.line(self.screen, nc.RGB.WHITE, nc.Vec(self.width / 2 - 200 + star * 80, 40) + p, nc.Vec(self.width / 2 - 200 + star * 80, 40) + outline[i - 1], 1)

        # Game title
        font = self.window.font.get("title", 120)
        text = font.render(self.game.name, True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 120))

        # Description box
        short_description_lines = split_text(self.game.short_description, 35)
        description_lines = split_text(self.game.description, 52)
        black_rect(self.screen, 758, 240, 1095, 45 + len(short_description_lines) * 40 + len(description_lines) * 32, 80, True, 3)

        # Game short description
        font = self.window.font.get("text", 30)
        height = 260
        for i, line in enumerate(short_description_lines):
            text = font.render(line, True, nc.RGB.WHITE)
            self.screen.blit(text, (780, height))
            height += 40

        # Game description
        font = self.window.font.get("text", 20)
        height += 20
        for i, line in enumerate(description_lines):
            text = font.render(line, True, nc.RGB.WHITE)
            self.screen.blit(text, (780, height))
            height += 32

        # Game author
        font = self.window.font.get("text", 28)
        text = font.render(f"von {self.game.author}", True, nc.RGB.WHITE)
        self.screen.blit(text, (780, height + 25))

        # Render image
        self.screen.blit(self.image, (70, 240))
        pg.draw.rect(self.screen, nc.RGB.WHITE, (70, 240, 650, 650), 3)

        # Continue prompt
        font = self.window.font.get("text", 35)
        height = math.sin(self.tick / 10) * 15 + 950
        text = font.render("Drücke #, um mit diesem Spiel fortzufahren!", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, height))

    def update(self) -> None:

        self.tick += self.dt

        # Scene switching
        if self.tick - self.timeout > 1200:
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
