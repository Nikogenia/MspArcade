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

        self.images: list[tuple[pg.Surface, Game]] = []

        self.position: int = 0

        self.animation_type: int = 0
        self.animation_start: float = 0
        self.animation_switched: bool = False

        self.slots: list[list[pg.Surface, nc.Vec, nc.Vec, nc.Vec, nc.Vec, nc.Vec, nc.Vec, int, int, int]] = []

        self.POS1: nc.Vec = nc.Vec(-260, 490)
        self.POS2: nc.Vec = nc.Vec(360, 490)
        self.POS3: nc.Vec = nc.Vec(self.width / 2, 490)
        self.POS4: nc.Vec = nc.Vec(self.width - 360, 490)
        self.POS5: nc.Vec = nc.Vec(self.width + 260, 490)

        self.SIZE1: nc.Vec = nc.Vec(500, 500)
        self.SIZE2: nc.Vec = nc.Vec(700, 700)
        self.SIZE3: nc.Vec = nc.Vec(800, 800)

        self.ANIMATION_DURATION: int = 12

    def render(self) -> None:

        if self.animation_type == 0:
            self.screen.blit(pg.transform.scale(self.get_surf(self.position - 1), self.SIZE2), self.POS2 - self.SIZE2 / 2)
            black_rect(self.screen, *(self.POS2 - self.SIZE2 / 2), *self.SIZE2, 180, True)
            self.screen.blit(pg.transform.scale(self.get_surf(self.position + 1), self.SIZE2), self.POS4 - self.SIZE2 / 2)
            black_rect(self.screen, *(self.POS4 - self.SIZE2 / 2), *self.SIZE2, 180, True)
            self.screen.blit(self.get_surf(self.position), self.POS3 - self.SIZE3 / 2)
            black_rect(self.screen, *(self.POS3 - self.SIZE3 / 2), *self.SIZE3, 90, True)
        else:
            img_alpha = int(255 - 20 / (self.ANIMATION_DURATION - self.ANIMATION_DURATION / 2) * (self.tick - self.animation_start))
            for surf, pos, size, p_start, p_end, s_start, s_end, alpha, a_start, a_end in self.slots:
                surf.set_alpha(img_alpha)
                self.screen.blit(pg.transform.scale(surf, size), pos - size / 2)
                black = pg.Surface(size)
                black.set_alpha(alpha - 235 + img_alpha)
                pg.draw.rect(black, nc.RGB.WHITE, (0, 0, black.get_width(), black.get_height()), 3)
                self.screen.blit(black, pos - size / 2)

        font = self.window.font.get("text", 35)
        height = math.sin(self.tick / 10) * 15 + 970
        text = font.render("Wähle ein Spiel aus!", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, height))

    def update(self) -> None:

        self.tick += self.dt

        if self.tick - self.timeout > 600:
            self.window.change_scene("idle")

        if self.animation_type != 0:

            if self.tick - self.animation_start >= self.ANIMATION_DURATION:
                self.animation_type = 0
                self.slots.clear()
                for surf, game in self.images:
                    surf.set_alpha(255)

            if self.tick - self.animation_start >= self.ANIMATION_DURATION / 2 and not self.animation_switched:
                slot3 = self.slots[3]
                self.slots[3] = self.slots[1]
                self.slots[1] = slot3
                self.animation_switched = True

            for index, slot in enumerate(self.slots):
                self.slots[index][1] = slot[3] + (slot[4] - slot[3]) / self.ANIMATION_DURATION * (self.tick - self.animation_start)
                self.slots[index][2] = slot[5] + (slot[6] - slot[5]) / self.ANIMATION_DURATION * (self.tick - self.animation_start)
                self.slots[index][7] = slot[8] + (slot[9] - slot[8]) / self.ANIMATION_DURATION * (self.tick - self.animation_start)

        # Debug screen
        self.window.debug_screen_left.append("")
        self.window.debug_screen_left.append(f"Tick: {self.tick:.1f}")
        self.window.debug_screen_left.append(f"Timeout: {600 - (self.tick - self.timeout):.1f}")

    def event(self, event: pg.event.Event) -> None:

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.window.change_scene("login")
            if event.key == pg.K_LEFT:
                self.position -= 1
                self.timeout = self.tick
                self.animation_type = 1
                self.animation_start = self.tick
                self.animation_switched = False
                self.slots.clear()
                self.slots.append([self.get_surf(self.position - 1), self.POS1, self.SIZE1, self.POS1, self.POS2, self.SIZE1, self.SIZE2, 210, 210, 180])
                self.slots.append([self.get_surf(self.position), self.POS2, self.SIZE2, self.POS2, self.POS3, self.SIZE2, self.SIZE3, 180, 180, 90])
                self.slots.append([self.get_surf(self.position + 2), self.POS4, self.SIZE2, self.POS4, self.POS5, self.SIZE2, self.SIZE1, 180, 180, 210])
                self.slots.append([self.get_surf(self.position + 1), self.POS3, self.SIZE3, self.POS3, self.POS4, self.SIZE3, self.SIZE2, 90, 90, 180])
            if event.key == pg.K_RIGHT:
                self.position += 1
                self.timeout = self.tick
                self.animation_type = 2
                self.animation_start = self.tick
                self.animation_switched = False
                self.slots.clear()
                self.slots.append([self.get_surf(self.position + 1), self.POS5, self.SIZE1, self.POS5, self.POS4, self.SIZE1, self.SIZE2, 210, 210, 180])
                self.slots.append([self.get_surf(self.position), self.POS4, self.SIZE2, self.POS4, self.POS3, self.SIZE2, self.SIZE3, 180, 180, 90])
                self.slots.append([self.get_surf(self.position - 2), self.POS2, self.SIZE2, self.POS2, self.POS1, self.SIZE2, self.SIZE1, 180, 180, 210])
                self.slots.append([self.get_surf(self.position - 1), self.POS3, self.SIZE3, self.POS3, self.POS2, self.SIZE3, self.SIZE2, 90, 90, 180])

    def init(self) -> None:

        self.logger.debug("Load game images ...")

        for game in self.window.main.game_manager.games:
            if nc.file.exists(f"{PATH_GAME}/{game.image_name}"):
                image = pg.image.load(f"{PATH_GAME}/{game.image_name}")
            else:
                self.logger.warning(f"Couldn't load game image at '{PATH_GAME}/{game.image_name}'! Use black ...")
                image = pg.Surface((800, 800))
            self.images.append((image, game))

        if not self.images:
            raise ValueError("At least one game is required for the menu!")

    def get_surf(self, pos: int) -> pg.Surface:
        return self.images[pos % len(self.images)][0]
