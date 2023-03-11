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

        self.left_arrow: pg.Surface = pg.transform.smoothscale(
            pg.image.load(f"{PATH_IMAGE}/left_arrow.png").convert(), (60, 60))
        self.back_x: float = 0

        # Activity request data
        self.activity_request_tick: float = 0
        self.activity_request_tick_target: float = 0

        self.game: Game = self.window.main.game_manager.current
        if nc.file.exists(f"{PATH_GAME}/{self.game.image_name}"):
            self.image: pg.Surface = pg.transform.scale(
                pg.image.load(f"{PATH_GAME}/{self.game.image_name}"), (650, 650))
        else:
            self.logger.warning(f"Couldn't load game image at '{PATH_GAME}/" +
                                f"{self.game.image_name}'! Use black ...")
            self.image: pg.Surface = pg.Surface((650, 650))

        # Star data
        img = pg.image.load(f"{PATH_IMAGE}/star.png")
        self.star_mask: pg.Mask = pg.mask.from_surface(img)
        self.stars: float = self.window.main.user_manager.get_ratings(self.game.id)[0]
        self.rating_count: int = self.window.main.user_manager.get_ratings(self.game.id)[1]

    def render(self) -> None:

        # Back arrow
        size = math.sin(self.tick / 5) / 30 + 0.9
        left_arrow = pg.transform.smoothscale_by(self.left_arrow, size)
        self.screen.blit(left_arrow, (30 - left_arrow.get_width() / 2 + self.back_x, 40 - left_arrow.get_height() / 2))
        size = math.sin(self.tick / 5) / 50 + 0.9
        font = self.window.font.get("text", 45)
        text = pg.transform.smoothscale_by(font.render("Zurück", True, nc.RGB.WHITE), size)
        self.screen.blit(text, (190 - text.get_width() / 2 + self.back_x, 42 - text.get_height() / 2))

        # Render stars
        if self.stars:
            for star in range(5):
                value_mask = pg.mask.Mask((max(self.stars - star, 0) * 64, 64), True)
                overlap_mask = self.star_mask.overlap_mask(value_mask, (0, 0))
                self.screen.blit(self.star_mask.to_surface(setcolor=nc.RGB.GRAY60, unsetcolor=(0, 0, 0, 0)),
                                 (self.width / 2 - 200 + star * 80, 40))
                self.screen.blit(overlap_mask.to_surface(setcolor=nc.RGB.GOLD1, unsetcolor=(0, 0, 0, 0)),
                                 (self.width / 2 - 200 + star * 80, 40))
                outline = self.star_mask.outline(1)
                for i, p in enumerate(outline):
                    pg.draw.line(self.screen, nc.RGB.WHITE, nc.Vec(self.width / 2 - 200 + star * 80, 40) + nc.Vec(*p),
                                 nc.Vec(self.width / 2 - 200 + star * 80, 40) + nc.Vec(*outline[i - 1]), 1)
            font = self.window.font.get("text", 36)
            text = font.render(f"{self.stars:.1f}" if self.stars else " - ", True, nc.RGB.GRAY95)
            self.screen.blit(text, (630, 72 - text.get_height() / 2 + 5))
            text = font.render(f"({self.rating_count})", True, nc.RGB.GRAY95)
            self.screen.blit(text, (1165, 72 - text.get_height() / 2 + 5))

        # Game title
        font = self.window.font.get("title", 120)
        text = font.render(self.game.name, True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 120))

        # Description box
        short_description_lines = split_text(self.game.short_description, 35)
        description_lines = split_text(self.game.description, 52)
        black_rect(self.screen, 758, 240, 1095,
                   45 + len(short_description_lines) * 40 + len(description_lines) * 32, 80, True, 3)

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

        # Render activity request
        if self.activity_request_tick != self.activity_request_tick_target or self.activity_request_tick == 20:
            height = 310 * (self.activity_request_tick / 20) - 300
            black_rect(self.screen, self.width / 2 - 700, height, 1400, 230, 200, True, 3)
            font = self.window.font.get("title", 110)
            text = font.render("BIST DU NOCH DA?", True, nc.RGB.WHITE)
            self.screen.blit(text, ((self.width - text.get_width()) / 2, height + 30))
            font = self.window.font.get("text", 35)
            text = font.render("Bestätige deine Anwesenheit mit #!", True, nc.RGB.WHITE)
            self.screen.blit(text, ((self.width - text.get_width()) / 2, height + 140))

        # Continue prompt
        font = self.window.font.get("text", 35)
        height = math.sin(self.tick / 10) * 15 + 950
        text = font.render("Drücke #, um mit diesem Spiel fortzufahren!", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, height))

    def update(self) -> None:

        self.tick += self.dt

        # Scene switching
        if self.tick - self.timeout > 1200:
            self.window.change_scene("idle", transition_duration=12, transition_pause=7)

        if self.back_x != 0:
            self.back_x -= self.dt * 3

        # Show activity request
        if self.tick - self.timeout > 1000:
            self.activity_request_tick_target = 20

        # Animate activity request
        if abs(self.activity_request_tick_target - self.activity_request_tick) < 1.5:
            self.activity_request_tick = self.activity_request_tick_target
        if self.activity_request_tick > self.activity_request_tick_target:
            self.activity_request_tick -= self.dt
        elif self.activity_request_tick < self.activity_request_tick_target:
            self.activity_request_tick += self.dt

        # Debug screen
        self.window.debug_screen_left.append("")
        self.window.debug_screen_left.append(f"Tick: {self.tick:.1f}")
        self.window.debug_screen_left.append(f"Timeout: {1200 - (self.tick - self.timeout):.1f}")
        self.window.debug_screen_left.append("")

    def event(self, event: pg.event.Event) -> None:

        if event.type == pg.KEYDOWN:

            # Reset timeout
            self.activity_request_tick_target = 0
            self.timeout = self.tick

            if event.key == pg.K_LEFT:
                self.window.change_scene("menu", transition_duration=8, transition_pause=4)
                self.back_x = -1
            if event.key == pg.K_RETURN:
                self.window.change_scene("login", {"back": "details"}, transition_duration=12, transition_pause=7)
