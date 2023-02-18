# Standard
from __future__ import annotations
from typing import TYPE_CHECKING
import math

# External
import nikocraft as nc
import pygame as pg

# Local
from constants import *
from window.draw_utils import black_rect
from game.game import Game
if TYPE_CHECKING:
    from window.window import Window


class MenuScene(nc.Scene):

    def __init__(self, window: Window, args):

        super(MenuScene, self).__init__(window, args)

        self.window: Window = window

        self.brightness: int = 180

        self.tick: float = 0
        self.timeout: float = 0

        # All game images
        self.images: list[tuple[pg.Surface, Game]] = []

        # Current position
        self.position: int = 0

        # Animation state
        self.animation_type: int = 0
        self.animation_start: float = 0
        self.animation_switched: bool = False

        # Animation slots (image, position, size, start_pos, end_pos, start_size, end_size, alpha, start_alpha, end_alpha)
        self.slots: list[list[pg.Surface, nc.Vec, nc.Vec, nc.Vec, nc.Vec, nc.Vec, nc.Vec, int, int, int]] = []

        # Text width
        self.text = ""
        self.text_width: int = 0
        self.text_width_start: int = 0
        self.text_width_end: int = 0

        # Game image positions
        self.POS1: nc.Vec = nc.Vec(-260, 490)
        self.POS2: nc.Vec = nc.Vec(360, 490)
        self.POS3: nc.Vec = nc.Vec(self.width / 2, 490)
        self.POS4: nc.Vec = nc.Vec(self.width - 360, 490)
        self.POS5: nc.Vec = nc.Vec(self.width + 260, 490)

        # Game image size
        self.SIZE1: nc.Vec = nc.Vec(500, 500)
        self.SIZE2: nc.Vec = nc.Vec(700, 700)
        self.SIZE3: nc.Vec = nc.Vec(800, 800)

        # Duration of the animation
        self.ANIMATION_DURATION: int = 12

    def render(self) -> None:

        # No animation
        if self.animation_type == 0:
            self.screen.blit(pg.transform.scale(self.get_surf(self.position - 1), self.SIZE2), self.POS2 - self.SIZE2 / 2)
            black_rect(self.screen, *(self.POS2 - self.SIZE2 / 2), *self.SIZE2, 180, True, 1)
            self.screen.blit(pg.transform.scale(self.get_surf(self.position + 1), self.SIZE2), self.POS4 - self.SIZE2 / 2)
            black_rect(self.screen, *(self.POS4 - self.SIZE2 / 2), *self.SIZE2, 180, True, 1)
            self.screen.blit(self.get_surf(self.position), self.POS3 - self.SIZE3 / 2)
            black_rect(self.screen, *(self.POS3 - self.SIZE3 / 2), *self.SIZE3, 90, True, 1)

        # Animation running
        else:
            for surf, pos, size, p_start, p_end, s_start, s_end, alpha, a_start, a_end in self.slots:
                self.screen.blit(pg.transform.scale(surf, size), pos - size / 2)
                black_rect(self.screen, *(pos - size / 2), *size, alpha, True, 1)

        font = self.window.font.get("title", 120)
        text = font.render(self.text, True, nc.RGB.WHITE)
        if self.animation_type != 0:
            text.set_alpha(int(abs(255 * ((self.tick - self.animation_start) - self.ANIMATION_DURATION / 2) / self.ANIMATION_DURATION * 2)))
        black_rect(self.screen, (self.width - self.text_width) / 2 - 30, 115, self.text_width + 55, 110, 160, True, 2)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 125))

        # Menu prompt
        font = self.window.font.get("text", 35)
        height = math.sin(self.tick / 10) * 15 + 970
        text = font.render("Wähle ein Spiel aus!", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, height))

    def update(self) -> None:

        self.tick += self.dt

        # Scene switching
        if self.tick - self.timeout > 600:
            self.window.change_scene("idle")

        # Animation running
        if self.animation_type != 0:

            # Reset animation
            if self.tick - self.animation_start >= self.ANIMATION_DURATION:
                self.animation_type = 0
                self.slots.clear()
                for surf, game in self.images:
                    surf.set_alpha(255)
                font = self.window.font.get("title", 120)
                size = font.size(self.images[self.position % len(self.images)][1].name)
                self.text_width = size[0]

            # Switch slot render order
            if self.tick - self.animation_start >= self.ANIMATION_DURATION / 2 and not self.animation_switched:
                slot1 = self.slots[1]
                self.slots[1] = self.slots[2]
                self.slots[2] = self.slots[3]
                self.slots[3] = slot1
                self.text = self.images[self.position % len(self.images)][1].name
                self.animation_switched = True

            # Update slot position, size and alpha
            for index, slot in enumerate(self.slots):
                self.slots[index][1] = slot[3] + (slot[4] - slot[3]) / self.ANIMATION_DURATION * (self.tick - self.animation_start)
                self.slots[index][2] = slot[5] + (slot[6] - slot[5]) / self.ANIMATION_DURATION * (self.tick - self.animation_start)
                self.slots[index][7] = slot[8] + (slot[9] - slot[8]) / self.ANIMATION_DURATION * (self.tick - self.animation_start)

            # Update text width
            if self.animation_type != 0:
                self.text_width = int(self.text_width_start + (self.text_width_end - self.text_width_start) / self.ANIMATION_DURATION * (self.tick - self.animation_start))

        # Debug screen
        self.window.debug_screen_left.append("")
        self.window.debug_screen_left.append(f"Tick: {self.tick:.1f}")
        self.window.debug_screen_left.append(f"Timeout: {600 - (self.tick - self.timeout):.1f}")

    def event(self, event: pg.event.Event) -> None:

        if event.type == pg.KEYDOWN:

            # Switch scene
            if event.key == pg.K_RETURN:
                self.window.change_scene("login")

            # Scroll
            if event.key in (pg.K_LEFT, pg.K_RIGHT):
                self.timeout = self.tick
                self.animation_start = self.tick
                self.animation_switched = False
                self.slots.clear()
                self.text_width_start = self.text_width
                if self.animation_type != 0:
                    self.text = self.images[self.position % len(self.images)][1].name

            # Scroll to left
            if event.key == pg.K_LEFT:
                self.position -= 1
                self.animation_type = 1
                self.slots.append([self.get_surf(self.position - 1), self.POS1, self.SIZE1, self.POS1, self.POS2, self.SIZE1, self.SIZE2, 230, 230, 180])
                self.slots.append([self.get_surf(self.position), self.POS2, self.SIZE2, self.POS2, self.POS3, self.SIZE2, self.SIZE3, 180, 180, 90])
                self.slots.append([self.get_surf(self.position + 2), self.POS4, self.SIZE2, self.POS4, self.POS5, self.SIZE2, self.SIZE1, 180, 180, 230])
                self.slots.append([self.get_surf(self.position + 1), self.POS3, self.SIZE3, self.POS3, self.POS4, self.SIZE3, self.SIZE2, 90, 90, 180])
                font = self.window.font.get("title", 120)
                size = font.size(self.images[self.position % len(self.images)][1].name)
                self.text_width_end = size[0]

            # Scroll to right
            if event.key == pg.K_RIGHT:
                self.position += 1
                self.animation_type = 2
                self.slots.append([self.get_surf(self.position + 1), self.POS5, self.SIZE1, self.POS5, self.POS4, self.SIZE1, self.SIZE2, 230, 230, 180])
                self.slots.append([self.get_surf(self.position), self.POS4, self.SIZE2, self.POS4, self.POS3, self.SIZE2, self.SIZE3, 180, 180, 90])
                self.slots.append([self.get_surf(self.position - 2), self.POS2, self.SIZE2, self.POS2, self.POS1, self.SIZE2, self.SIZE1, 180, 180, 230])
                self.slots.append([self.get_surf(self.position - 1), self.POS3, self.SIZE3, self.POS3, self.POS2, self.SIZE3, self.SIZE2, 90, 90, 180])
                font = self.window.font.get("title", 120)
                size = font.size(self.images[self.position % len(self.images)][1].name)
                self.text_width_end = size[0]

    def init(self) -> None:

        self.logger.debug("Load game images ...")

        for game in self.window.main.game_manager.games:
            if nc.file.exists(f"{PATH_GAME}/{game.image_name}"):
                image = pg.image.load(f"{PATH_GAME}/{game.image_name}").convert()
            else:
                self.logger.warning(f"Couldn't load game image at '{PATH_GAME}/{game.image_name}'! Use black ...")
                image = pg.Surface((800, 800))
            self.images.append((image, game))

        if not self.images:
            raise ValueError("At least one game is required for the menu!")

        self.text = self.images[self.position % len(self.images)][1].name
        font = self.window.font.get("title", 120)
        size = font.size(self.text)
        self.text_width = size[0]

    def get_surf(self, pos: int) -> pg.Surface:
        return self.images[pos % len(self.images)][0]
