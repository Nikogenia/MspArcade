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

        self.left_arrow: pg.Surface = pg.image.load(f"{PATH_IMAGE}/left_arrow.png").convert()
        self.right_arrow: pg.Surface = pg.image.load(f"{PATH_IMAGE}/right_arrow.png").convert()
        self.down_arrow: pg.Surface = pg.transform.smoothscale(pg.image.load(f"{PATH_IMAGE}/down_arrow.png").convert(), (60, 40))

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

        # Title data
        self.title: str = ""
        self.title_width: int = 0
        self.title_width_start: int = 0
        self.title_width_end: int = 0

        # Author data
        self.author: str = ""

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
            black_rect(self.screen, *(self.POS2 - self.SIZE2 / 2), *self.SIZE2, 190, True, 1)
            self.screen.blit(pg.transform.scale(self.get_surf(self.position + 1), self.SIZE2), self.POS4 - self.SIZE2 / 2)
            black_rect(self.screen, *(self.POS4 - self.SIZE2 / 2), *self.SIZE2, 190, True, 1)
            self.screen.blit(self.get_surf(self.position), self.POS3 - self.SIZE3 / 2)
            black_rect(self.screen, *(self.POS3 - self.SIZE3 / 2), *self.SIZE3, 110, True, 1)

        # Animation running
        else:
            for surf, pos, size, p_start, p_end, s_start, s_end, alpha, a_start, a_end in self.slots:
                self.screen.blit(pg.transform.scale(surf, size), pos - size / 2)
                black_rect(self.screen, *(pos - size / 2), *size, alpha, True, 1)

        # Render title
        font = self.window.font.get("title", 120)
        text = font.render(self.title, True, nc.RGB.WHITE)
        if self.animation_type != 0:
            text.set_alpha(int(abs(255 * ((self.tick - self.animation_start) - self.ANIMATION_DURATION / 2) / self.ANIMATION_DURATION * 2)))
        black_rect(self.screen, (self.width - self.title_width) / 2 - 30, 115, self.title_width + 55, 110, 150, True, 2)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 125))

        # Render author
        font = self.window.font.get("text", 25)
        text = font.render("entwickelt von", True, nc.RGB.BLACK)
        self.screen.blit(text, ((self.width - text.get_width()) / 2 + 5, 255))
        text = font.render("entwickelt von", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 250))
        font = self.window.font.get("text", 35)
        text = font.render(self.author, True, nc.RGB.BLACK)
        if self.animation_type != 0:
            text.set_alpha(int(abs(255 * ((self.tick - self.animation_start) - self.ANIMATION_DURATION / 2) / self.ANIMATION_DURATION * 2)))
        self.screen.blit(text, ((self.width - text.get_width()) / 2 + 5, 295))
        text = font.render(self.author, True, nc.RGB.WHITE)
        if self.animation_type != 0:
            text.set_alpha(int(abs(255 * ((self.tick - self.animation_start) - self.ANIMATION_DURATION / 2) / self.ANIMATION_DURATION * 2)))
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 290))

        # Render more details
        font = self.window.font.get("text", 22)
        text = font.render("Mehr Details", True, nc.RGB.BLACK)
        if self.animation_type != 0:
            text.set_alpha(int(abs(255 * ((self.tick - self.animation_start) - self.ANIMATION_DURATION / 2) / self.ANIMATION_DURATION * 2)))
        self.screen.blit(text, ((self.width - text.get_width()) / 2 + 2, 812))
        text = font.render("Mehr Details", True, nc.RGB.WHITE)
        if self.animation_type != 0:
            text.set_alpha(int(abs(255 * ((self.tick - self.animation_start) - self.ANIMATION_DURATION / 2) / self.ANIMATION_DURATION * 2)))
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 810))
        if self.animation_type != 0:
            self.down_arrow.set_alpha(int(abs(255 * ((self.tick - self.animation_start) - self.ANIMATION_DURATION / 2) / self.ANIMATION_DURATION * 2)))
        self.screen.blit(self.down_arrow, ((self.width - self.down_arrow.get_width()) / 2, 835))

        # Render arrows
        size = math.sin(self.tick / 5) * 6 + 100
        if self.animation_type == 1:
            offset = int(35 - abs(35 * ((self.tick - self.animation_start) - self.ANIMATION_DURATION / 2) / self.ANIMATION_DURATION * 2))
            self.screen.blit(pg.transform.smoothscale(self.left_arrow, (size, size)), (60 - size / 2 - offset, 490 - size / 2))
            self.screen.blit(pg.transform.smoothscale(self.right_arrow, (size, size)), (self.width - 60 - size / 2, 490 - size / 2))
        elif self.animation_type == 2:
            offset = int(35 - abs(35 * ((self.tick - self.animation_start) - self.ANIMATION_DURATION / 2) / self.ANIMATION_DURATION * 2))
            self.screen.blit(pg.transform.smoothscale(self.right_arrow, (size, size)), (self.width - 60 - size / 2 + offset, 490 - size / 2))
            self.screen.blit(pg.transform.smoothscale(self.left_arrow, (size, size)), (60 - size / 2, 490 - size / 2))
        else:
            self.screen.blit(pg.transform.smoothscale(self.left_arrow, (size, size)), (60 - size / 2, 490 - size / 2))
            self.screen.blit(pg.transform.smoothscale(self.right_arrow, (size, size)), (self.width - 60 - size / 2, 490 - size / 2))

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
                self.title_width = size[0]

            # Switch slot render order
            if self.tick - self.animation_start >= self.ANIMATION_DURATION / 2 and not self.animation_switched:
                slot1 = self.slots[1]
                self.slots[1] = self.slots[2]
                self.slots[2] = self.slots[3]
                self.slots[3] = slot1
                self.title = self.images[self.position % len(self.images)][1].name
                self.author = self.images[self.position % len(self.images)][1].author
                self.animation_switched = True

            # Update slot position, size and alpha
            for index, slot in enumerate(self.slots):
                self.slots[index][1] = slot[3] + (slot[4] - slot[3]) / self.ANIMATION_DURATION * (self.tick - self.animation_start)
                self.slots[index][2] = slot[5] + (slot[6] - slot[5]) / self.ANIMATION_DURATION * (self.tick - self.animation_start)
                self.slots[index][7] = slot[8] + (slot[9] - slot[8]) / self.ANIMATION_DURATION * (self.tick - self.animation_start)

            # Update title width
            if self.animation_type != 0:
                self.title_width = int(self.title_width_start + (self.title_width_end - self.title_width_start) / self.ANIMATION_DURATION * (self.tick - self.animation_start))

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
                self.title_width_start = self.title_width
                if self.animation_type != 0:
                    self.title = self.images[self.position % len(self.images)][1].name

            # Scroll to left
            if event.key == pg.K_LEFT:
                self.position -= 1
                self.animation_type = 1
                self.slots.append([self.get_surf(self.position - 1), self.POS1, self.SIZE1, self.POS1, self.POS2, self.SIZE1, self.SIZE2, 240, 240, 190])
                self.slots.append([self.get_surf(self.position), self.POS2, self.SIZE2, self.POS2, self.POS3, self.SIZE2, self.SIZE3, 190, 190, 110])
                self.slots.append([self.get_surf(self.position + 2), self.POS4, self.SIZE2, self.POS4, self.POS5, self.SIZE2, self.SIZE1, 190, 190, 240])
                self.slots.append([self.get_surf(self.position + 1), self.POS3, self.SIZE3, self.POS3, self.POS4, self.SIZE3, self.SIZE2, 110, 110, 190])
                font = self.window.font.get("title", 120)
                size = font.size(self.images[self.position % len(self.images)][1].name)
                self.title_width_end = size[0]

            # Scroll to right
            if event.key == pg.K_RIGHT:
                self.position += 1
                self.animation_type = 2
                self.slots.append([self.get_surf(self.position + 1), self.POS5, self.SIZE1, self.POS5, self.POS4, self.SIZE1, self.SIZE2, 240, 240, 190])
                self.slots.append([self.get_surf(self.position), self.POS4, self.SIZE2, self.POS4, self.POS3, self.SIZE2, self.SIZE3, 190, 190, 110])
                self.slots.append([self.get_surf(self.position - 2), self.POS2, self.SIZE2, self.POS2, self.POS1, self.SIZE2, self.SIZE1, 190, 190, 240])
                self.slots.append([self.get_surf(self.position - 1), self.POS3, self.SIZE3, self.POS3, self.POS2, self.SIZE3, self.SIZE2, 110, 110, 190])
                font = self.window.font.get("title", 120)
                size = font.size(self.images[self.position % len(self.images)][1].name)
                self.title_width_end = size[0]

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

        self.title = self.images[self.position % len(self.images)][1].name
        font = self.window.font.get("title", 120)
        size = font.size(self.title)
        self.title_width = size[0]

        self.author = self.images[self.position % len(self.images)][1].author

    def get_surf(self, pos: int) -> pg.Surface:
        return self.images[pos % len(self.images)][0]
