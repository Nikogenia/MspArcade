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


class RatingScene(nc.Scene):

    def __init__(self, window: Window, args):

        super(RatingScene, self).__init__(window, args)

        self.window: Window = window

        self.brightness: int = 180

        self.tick: float = 0
        self.timeout: float = 0

        self.running: bool = True

        self.left_arrow: pg.Surface = pg.transform.smoothscale(
            pg.image.load(f"{PATH_IMAGE}/left_arrow.png").convert(), (60, 60))
        self.up_arrow: pg.Surface = pg.transform.smoothscale(
            pg.image.load(f"{PATH_IMAGE}/up_arrow.png").convert(), (70, 70))
        self.down_arrow: pg.Surface = pg.transform.smoothscale(
            pg.image.load(f"{PATH_IMAGE}/down_arrow.png").convert(), (70, 70))
        self.back_x: float = 0

        # Activity request data
        self.activity_request_tick: float = 0
        self.activity_request_tick_target: float = 0

        # TODO TEMP
        nc.time.wait(2)
        self.window.main.game_manager.current = self.window.main.game_manager.games[1]
        self.window.main.user_manager.current = self.window.main.user_manager.players[0].auth_id

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
        img = pg.image.load(f"{PATH_IMAGE}/star.png")
        self.star_mask: pg.Mask = pg.mask.from_surface(img)
        self.stars: int = 3
        self.stars_last: float = 3
        self.update_tick: float = 0

    def render(self) -> None:

        # Back arrow
        size = math.sin(self.tick / 5) / 30 + 0.9
        left_arrow = pg.transform.smoothscale_by(self.left_arrow, size)
        self.screen.blit(left_arrow, (30 - left_arrow.get_width() / 2 + self.back_x, 40 - left_arrow.get_height() / 2))
        size = math.sin(self.tick / 5) / 50 + 0.9
        font = self.window.font.get("text", 45)
        text = pg.transform.smoothscale_by(font.render("Zurück", True, nc.RGB.WHITE), size)
        self.screen.blit(text, (190 - text.get_width() / 2 + self.back_x, 42 - text.get_height() / 2))

        # Thanks title
        font = self.window.font.get("title", 130)
        text = font.render("Vielen Dank!", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 80))
        font = self.window.font.get("text", 42)
        text = font.render("Wir hoffen, du hattest Spaß!", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 220))

        # Rating request
        font = self.window.font.get("text", 32)
        text = font.render("Nimm dir bitte kurz Zeit,", True, nc.RGB.WHITE)
        self.screen.blit(text, (1340 - text.get_width() / 2, 345))
        text = font.render("um das Spiel zu bewerten:", True, nc.RGB.WHITE)
        self.screen.blit(text, (1340 - text.get_width() / 2, 395))

        # Render image
        self.screen.blit(self.image, (218, 330))
        black_rect(self.screen, 218, 330, 550, 550, 90, True, 2, nc.RGB.GRAY60)

        # Game title
        font = self.window.font.get("title", 75)
        text = font.render(self.game.name, True, nc.RGB.WHITE)
        black_rect(self.screen, 495 - text.get_width() / 2 - 15, 345, text.get_width() + 25, 65, 160, True, 2)
        self.screen.blit(text, (495 - text.get_width() / 2, 350))

        # Game author
        font = self.window.font.get("text", 22)
        text = font.render(f"von {self.game.author}", True, nc.RGB.BLACK)
        self.screen.blit(text, (495 - text.get_width() / 2 + 2, 427))
        text = font.render(f"von {self.game.author}", True, nc.RGB.WHITE)
        self.screen.blit(text, (495 - text.get_width() / 2, 425))

        # Game short description
        font = self.window.font.get("text", 20)
        if self.game.short_description_split == 0:
            text = font.render(self.game.short_description, True, nc.RGB.WHITE)
            black_rect(self.screen, 495 - text.get_width() / 2 - 15, 815, text.get_width() + 25, 50, 100, True, 2)
        else:
            text = font.render(self.game.short_description[self.game.short_description_split + 1:], True, nc.RGB.WHITE)
            text2 = font.render(self.game.short_description[:self.game.short_description_split], True, nc.RGB.WHITE)
            width = max(text.get_width(), text2.get_width())
            black_rect(self.screen, 495 - width / 2 - 15, 785, width + 25, 80, 100, True, 2)
            self.screen.blit(text2, (495 - text2.get_width() / 2, 800))
        self.screen.blit(text, (495 - text.get_width() / 2, 830))

        # Rating box
        black_rect(self.screen, 1010, 470, 648, 380, 150, True, 2)

        # Render stars
        stars = self.stars
        if self.stars != self.stars_last:
            stars = self.stars_last + (self.stars - self.stars_last) * (self.tick - self.update_tick) / 12
        for star in range(5):
            value_mask = pg.mask.Mask((max(stars - star, 0) * 64, 64), True)
            overlap_mask = self.star_mask.overlap_mask(value_mask, (0, 0))
            self.screen.blit(self.star_mask.to_surface(setcolor=nc.RGB.GRAY60, unsetcolor=(0, 0, 0, 0)),
                             (1140 + star * 80, 574))
            self.screen.blit(overlap_mask.to_surface(setcolor=nc.RGB.GOLD1, unsetcolor=(0, 0, 0, 0)),
                             (1140 + star * 80, 574))
            outline = self.star_mask.outline(1)
            for i, p in enumerate(outline):
                pg.draw.line(self.screen, nc.RGB.WHITE, nc.Vec(1140 + star * 80, 574) + nc.Vec(*p),
                             nc.Vec(1140 + star * 80, 574) + nc.Vec(*outline[i - 1]), 1)

        # Render arrows
        size = math.sin(self.tick / 5) / 25 + 0.9
        up_arrow = pg.transform.smoothscale_by(self.up_arrow, size)
        down_arrow = pg.transform.smoothscale_by(self.down_arrow, size)
        self.screen.blit(up_arrow, (1332 - up_arrow.get_width() / 2, 515 - up_arrow.get_height() / 2))
        self.screen.blit(down_arrow, (1332 - down_arrow.get_width() / 2, 710 - down_arrow.get_height() / 2))

        # Rating number
        surf = pg.Surface((150, 150))
        surf.set_colorkey((0, 0, 0))
        surf.set_alpha(210)
        font = self.window.font.get("title", 190)
        text = font.render(f"{self.stars}", True, nc.RGB.WHITE)
        surf.blit(text, (75 - text.get_width() / 2, 75 - text.get_height() / 2))
        self.screen.blit(surf, (1340 - surf.get_width() / 2, 565))

        # Save prompt
        font = self.window.font.get("text", 30)
        text = font.render("Speichern #", True, nc.RGB.WHITE)
        self.screen.blit(text, (1332 - text.get_width() / 2, 780))

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

        # Rating prompt
        font = self.window.font.get("text", 35)
        height = math.sin(self.tick / 10) * 15 + 950
        text = font.render("Bewerte das Spiel oder kehre zum Menü zurück!", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, height))

    def update(self) -> None:

        self.tick += self.dt

        # Scene switching
        if self.tick - self.timeout > 900:
            self.window.change_scene("idle")

        if self.back_x != 0:
            self.back_x -= self.dt * 3

        # Show activity request
        if self.tick - self.timeout > 700:
            self.activity_request_tick_target = 20

        if self.tick - self.update_tick > 12:
            self.stars_last = self.stars

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
        self.window.debug_screen_left.append(f"Timeout: {900 - (self.tick - self.timeout):.1f}")
        self.window.debug_screen_left.append("")

    def quit(self) -> None:

        # Log out user
        self.window.main.user_manager.current = ""

    def event(self, event: pg.event.Event) -> None:

        if event.type == pg.KEYDOWN:

            # Reset timeout
            self.activity_request_tick_target = 0
            self.timeout = self.tick

            if event.key == pg.K_LEFT:
                self.window.change_scene("idle")
                self.back_x = -1
            if event.key == pg.K_RETURN:
                self.window.change_scene("idle")

            if event.key == pg.K_UP:
                if self.stars < 5:
                    self.stars_last = self.stars
                    self.stars += 1
                    self.update_tick = self.tick
            if event.key == pg.K_DOWN:
                if self.stars > 0:
                    self.stars_last = self.stars
                    self.stars -= 1
                    self.update_tick = self.tick
