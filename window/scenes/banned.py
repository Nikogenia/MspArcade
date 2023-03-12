# Standard
from __future__ import annotations
from typing import TYPE_CHECKING
import math

# External
import nikocraft as nc
import pygame as pg

# Local
from constants import *
from user.user import User
from user.player import Player
from window.draw_utils import black_rect, draw_button, split_text

if TYPE_CHECKING:
    from window.window import Window


class BannedScene(nc.Scene):

    def __init__(self, window: Window, args):

        super(BannedScene, self).__init__(window, args)

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

        self.player: Player = self.window.main.user_manager.get_player_by_auth_id(self.window.main.user_manager.current)
        self.user: User = self.window.main.user_manager.get_user(self.player.user_id)

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
        text = font.render("DU WURDEST GESPERRT!", True, nc.RGB.INDIANRED1)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 150))

        # Player name
        font = self.window.font.get("text", 55)
        text = font.render(self.player.name, True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 310))

        # User name
        font = self.window.font.get("text", 28)
        text = font.render(self.user.name.upper(), True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 400))

        # Info box
        black_rect(self.screen, self.width / 2 - 550, 520, 1100, 450, 60, True, 2)
        font = self.window.font.get("text", 30)
        text = font.render("Begründung:", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 580))
        lines = split_text(self.window.main.user_manager.get_ban_reason(self.user.id), 30)
        for i, line in enumerate(lines):
            text = font.render(line, True, nc.RGB.WHITE)
            self.screen.blit(text, ((self.width - text.get_width()) / 2, 620 + i * 40))

        # Render activity request
        if self.activity_request_tick != self.activity_request_tick_target or self.activity_request_tick == 20:
            height = 310 * (self.activity_request_tick / 20) - 300
            black_rect(self.screen, self.width / 2 - 700, height, 1400, 230, 200, True, 3)
            font = self.window.font.get("title", 110)
            text = font.render("BIST DU NOCH DA?", True, nc.RGB.WHITE)
            self.screen.blit(text, ((self.width - text.get_width()) / 2, height + 30))
            font = self.window.font.get("text", 35)
            text = font.render("Bestätige deine Anwesenheit mit  !", True, nc.RGB.WHITE)
            self.screen.blit(text, ((self.width - text.get_width()) / 2, height + 140))
            draw_button(self.screen, font, 32, (self.width - text.get_width()) / 2, height + 140, ACTIVITY_BUTTON)

    def update(self) -> None:

        self.tick += self.dt

        # Scene switching
        if self.tick - self.timeout > 1200:
            self.window.change_scene("idle", transition_duration=12, transition_pause=7)

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

    def quit(self) -> None:

        # Log out user and reset game selection
        self.window.main.user_manager.current = ""
        self.window.main.game_manager.current = None

    def event(self, event: pg.event.Event) -> None:

        if event.type == pg.KEYDOWN:

            # Reset timeout
            self.activity_request_tick_target = 0
            self.timeout = self.tick

            if event.key == pg.K_LEFT:

                self.window.change_scene("idle", transition_duration=12, transition_pause=7)
                self.back_x = -1
