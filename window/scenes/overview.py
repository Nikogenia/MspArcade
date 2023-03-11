# Standard
from __future__ import annotations
from typing import TYPE_CHECKING
import math
import datetime as dt

# External
import nikocraft as nc
import pygame as pg

# Local
from constants import *
from game.game import Game
from user.user import User
from user.player import Player
from window.draw_utils import black_rect

if TYPE_CHECKING:
    from window.window import Window


class OverviewScene(nc.Scene):

    def __init__(self, window: Window, args):

        super(OverviewScene, self).__init__(window, args)

        self.window: Window = window

        self.brightness: int = 180

        self.tick: float = 0
        self.timeout: float = 0

        self.running: bool = True

        if "back" not in self.args:
            self.args["back"] = "menu"

        self.left_arrow: pg.Surface = pg.transform.smoothscale(
            pg.image.load(f"{PATH_IMAGE}/left_arrow.png").convert(), (60, 60))
        self.back_x: float = 0

        # Activity request data
        self.activity_request_tick: float = 0
        self.activity_request_tick_target: float = 0

        self.game: Game = self.window.main.game_manager.current
        if nc.file.exists(f"{PATH_GAME}/{self.game.image_name}"):
            self.image: pg.Surface = pg.transform.scale(
                pg.image.load(f"{PATH_GAME}/{self.game.image_name}"), (550, 550))
        else:
            self.logger.warning(f"Couldn't load game image at '{PATH_GAME}/{self.game.image_name}'! Use black ...")
            self.image: pg.Surface = pg.Surface((400, 400))

        self.player: Player = self.window.main.user_manager.get_player_by_auth_id(self.window.main.user_manager.current)
        self.user: User = self.window.main.user_manager.get_user(self.player.user_id)

        # Star data
        img = pg.transform.smoothscale(pg.image.load(f"{PATH_IMAGE}/star.png"), (50, 50))
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

        # Overview title
        font = self.window.font.get("title", 130)
        text = font.render("Herzlich Willkommen!", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 80))

        # Player name
        font = self.window.font.get("text", 55)
        text = font.render(self.player.name, True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 200))

        # User name
        font = self.window.font.get("text", 28)
        text = font.render(self.user.name.upper(), True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 290))

        # Info box
        black_rect(self.screen, 200, 400, 600, 460, 60, True, 2)

        # Time left
        font = self.window.font.get("text", 35)
        text = font.render("Zeit übrig:", True, nc.RGB.WHITE)
        self.screen.blit(text, (505 - text.get_width() / 2, 450))
        font = self.window.font.get("text", 45)
        text = font.render(f"{self.player.time // 3600:02d}:{self.player.time // 60:02d}:{self.player.time % 60:02d}",
                           True, nc.RGB.WHITE if self.player.time > 5 else nc.RGB.INDIANRED1)
        self.screen.blit(text, (500 - text.get_width() / 2, 510))

        # Created
        font = self.window.font.get("text", 35)
        text = font.render("Beigetreten:", True, nc.RGB.WHITE)
        self.screen.blit(text, (500 - text.get_width() / 2, 615))
        font = self.window.font.get("text", 30)
        text = font.render(f"{dt.datetime.fromtimestamp(self.player.created).strftime('%d.%m.%y %H:%M:%S')}",
                           True, nc.RGB.WHITE)
        self.screen.blit(text, (500 - text.get_width() / 2, 675))

        # Time refill
        font = self.window.font.get("text", 17)
        text = font.render("Deine Spielzeit wird immer", True, nc.RGB.WHITE)
        self.screen.blit(text, (500 - text.get_width() / 2, 765))
        text = font.render("am Montag wieder aufgeladen!", True, nc.RGB.WHITE)
        self.screen.blit(text, (500 - text.get_width() / 2, 795))

        # Render image
        self.screen.blit(self.image, (1100, 360))
        black_rect(self.screen, 1100, 360, 550, 550, 90, True, 2, nc.RGB.GRAY60)

        # Game title
        font = self.window.font.get("title", 75)
        text = font.render(self.game.name, True, nc.RGB.WHITE)
        black_rect(self.screen, 1375 - text.get_width() / 2 - 15, 375, text.get_width() + 25, 65, 160, True, 2)
        self.screen.blit(text, (1375 - text.get_width() / 2, 380))

        # Game author
        font = self.window.font.get("text", 22)
        text = font.render(f"von {self.game.author}", True, nc.RGB.BLACK)
        self.screen.blit(text, (1375 - text.get_width() / 2 + 2, 457))
        text = font.render(f"von {self.game.author}", True, nc.RGB.WHITE)
        self.screen.blit(text, (1375 - text.get_width() / 2, 455))

        # Render stars
        if self.stars:
            for star in range(5):
                value_mask = pg.mask.Mask((max(self.stars - star, 0) * 50, 50), True)
                overlap_mask = self.star_mask.overlap_mask(value_mask, (0, 0))
                self.screen.blit(self.star_mask.to_surface(setcolor=nc.RGB.GRAY60, unsetcolor=(0, 0, 0, 0)),
                                 (1375 - 150 + star * 60, 500))
                self.screen.blit(overlap_mask.to_surface(setcolor=nc.RGB.GOLD1, unsetcolor=(0, 0, 0, 0)),
                                 (1375 - 150 + star * 60, 500))
                outline = self.star_mask.outline(1)
                for i, p in enumerate(outline):
                    pg.draw.line(self.screen, nc.RGB.WHITE, nc.Vec(1375 - 150 + star * 60, 500) + nc.Vec(*p),
                                 nc.Vec(1375 - 150 + star * 60, 500) + nc.Vec(*outline[i - 1]), 1)
            font = self.window.font.get("text", 20)
            text = font.render(f"{self.stars:.1f}", True, nc.RGB.GRAY85)
            self.screen.blit(text, (1158, 525 - text.get_height() / 2 + 2))
            text = font.render(f"({self.rating_count})", True, nc.RGB.GRAY85)
            self.screen.blit(text, (1520, 525 - text.get_height() / 2 + 2))

        # Game short description
        font = self.window.font.get("text", 20)
        if self.game.short_description_split == 0:
            text = font.render(self.game.short_description, True, nc.RGB.WHITE)
            black_rect(self.screen, 1375 - text.get_width() / 2 - 15, 845, text.get_width() + 25, 50, 100, True, 2)
        else:
            text = font.render(self.game.short_description[self.game.short_description_split + 1:], True, nc.RGB.WHITE)
            text2 = font.render(self.game.short_description[:self.game.short_description_split], True, nc.RGB.WHITE)
            width = max(text.get_width(), text2.get_width())
            black_rect(self.screen, 1375 - width / 2 - 15, 815, width + 25, 80, 100, True, 2)
            self.screen.blit(text2, (1375 - text2.get_width() / 2, 830))
        self.screen.blit(text, (1375 - text.get_width() / 2, 860))

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

        # Continue or sorry prompt
        content = "Starte das Spiel mit #!" if self.player.time > 5 else "Du hast leider nicht mehr genug Zeit übrig!"
        font = self.window.font.get("text", 35)
        height = math.sin(self.tick / 10) * 15 + 960
        text = font.render(content, True, nc.RGB.WHITE if self.player.time > 5 else nc.RGB.INDIANRED1)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, height))

    def update(self) -> None:

        self.tick += self.dt

        # Scene switching
        if self.tick - self.timeout > 1200:

            self.window.change_scene("idle", transition_duration=12, transition_pause=7)

            # Log out user
            self.window.main.user_manager.current = ""

        if self.back_x != 0:
            self.back_x -= self.dt * 3

        # Show activity request
        if self.tick - self.timeout > 900:
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

                self.window.change_scene(self.args["back"], transition_duration=12, transition_pause=7)
                self.back_x = -1

                # Log out user
                self.window.main.user_manager.current = ""

            if event.key == pg.K_RETURN:
                if self.player.time > 5:
                    self.window.change_scene("play", transition_duration=12, transition_pause=7)
