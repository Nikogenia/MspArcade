# Standard
from __future__ import annotations
from typing import TYPE_CHECKING
import threading as th
import math
import random as rd

# External
import nikocraft as nc
import pygame as pg

# Local
from constants import *
from configs import ConfigError
from window.draw_utils import black_rect, draw_button
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
        self.down_arrow: pg.Surface = pg.transform.smoothscale(
            pg.image.load(f"{PATH_IMAGE}/down_arrow.png").convert(), (60, 40))

        # All game images
        self.images: list[tuple[pg.Surface, Game, float, int]] = []
        self.loaded: bool = False

        # Current position
        self.position: int = 0

        # Animation state
        self.animation_type: int = 0
        self.animation_start: float = 0
        self.animation_switched: bool = False

        # Animation slots (image, position, size, start_pos, end_pos,
        #                  start_size, end_size, alpha, start_alpha, end_alpha)
        self.slots: list[list[pg.Surface, nc.Vec, nc.Vec, nc.Vec, nc.Vec, nc.Vec, nc.Vec, int, int, int]] = []

        # Star data
        img = pg.transform.smoothscale(pg.image.load(f"{PATH_IMAGE}/star.png"), (50, 50))
        self.star_mask: pg.Mask = pg.mask.from_surface(img)
        self.star_start: float = 0
        self.star_end: float = 0
        self.rating_count_start: int = 0
        self.rating_count_end: int = 0

        # Title data
        self.title: str = ""
        self.title_width: int = 0
        self.title_width_start: int = 0
        self.title_width_end: int = 0

        # Author data
        self.author: str = ""

        # Description data
        self.description1: str = ""
        self.description2: str = ""
        self.description_height: int = 0
        self.description_height_start: int = 0
        self.description_height_end: int = 0
        self.description_width: int = 0
        self.description_width_start: int = 0
        self.description_width_end: int = 0

        # More details data
        self.details_y: float = 0

        # Activity request data
        self.activity_request_tick: float = 0
        self.activity_request_tick_target: float = 0

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

        # Render menu
        if self.loaded:
            self.render_menu()
        else:
            black_rect(self.screen, *(self.POS2 - self.SIZE2 / 2), *self.SIZE2, 255, True, 2, nc.RGB.GRAY60)
            black_rect(self.screen, *(self.POS4 - self.SIZE2 / 2), *self.SIZE2, 255, True, 2, nc.RGB.GRAY60)
            black_rect(self.screen, *(self.POS3 - self.SIZE3 / 2), *self.SIZE3, 255, True, 2, nc.RGB.GRAY60)

        # Menu prompt
        font = self.window.font.get("text", 35)
        height = math.sin(self.tick / 10) * 15 + 960
        text = font.render("Wähle mit   ein Spiel aus!", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, height))
        draw_button(self.screen, font, 10, (self.width - text.get_width()) / 2, height, BUTTON_A_COLOR)

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
            draw_button(self.screen, font, 32, (self.width - text.get_width()) / 2, height + 140, BUTTON_C_COLOR)

    def render_menu(self) -> None:

        # No animation
        if self.animation_type == 0:
            self.screen.blit(pg.transform.scale(self.get_surf(self.position - 1), self.SIZE2),
                             self.POS2 - self.SIZE2 / 2)
            black_rect(self.screen, *(self.POS2 - self.SIZE2 / 2), *self.SIZE2, 190, True, 2, nc.RGB.GRAY60)
            self.screen.blit(pg.transform.scale(self.get_surf(self.position + 1), self.SIZE2),
                             self.POS4 - self.SIZE2 / 2)
            black_rect(self.screen, *(self.POS4 - self.SIZE2 / 2), *self.SIZE2, 190, True, 2, nc.RGB.GRAY60)
            self.screen.blit(self.get_surf(self.position), self.POS3 - self.SIZE3 / 2)
            black_rect(self.screen, *(self.POS3 - self.SIZE3 / 2), *self.SIZE3, 70, True, 2, nc.RGB.GRAY60)

        # Animation running
        else:
            for surf, pos, size, p_start, p_end, s_start, s_end, alpha, a_start, a_end in self.slots:
                self.screen.blit(pg.transform.scale(surf, size), pos - size / 2)
                black_rect(self.screen, *(pos - size / 2), *size, alpha, True, 2, nc.RGB.GRAY60)

        # Render stars
        if self.animation_type == 0:
            stars = self.images[self.position % len(self.images)][2]
            rating_count = self.images[self.position % len(self.images)][3]
        else:
            stars = self.star_start + (self.star_end - self.star_start) / \
                    self.ANIMATION_DURATION * (self.tick - self.animation_start)
            rating_count = round(self.rating_count_start + (self.rating_count_end - self.rating_count_start) /
                                 self.ANIMATION_DURATION * (self.tick - self.animation_start))
        for star in range(5):
            value_mask = pg.mask.Mask((max(stars - star, 0) * 50, 50), True)
            overlap_mask = self.star_mask.overlap_mask(value_mask, (0, 0))
            self.screen.blit(self.star_mask.to_surface(setcolor=nc.RGB.GRAY60, unsetcolor=(0, 0, 0, 0)),
                             (self.width / 2 - 150 + star * 60, 20))
            self.screen.blit(overlap_mask.to_surface(setcolor=nc.RGB.GOLD1, unsetcolor=(0, 0, 0, 0)),
                             (self.width / 2 - 150 + star * 60, 20))
            outline = self.star_mask.outline(1)
            for i, p in enumerate(outline):
                pg.draw.line(self.screen, nc.RGB.WHITE, nc.Vec(self.width / 2 - 150 + star * 60, 20) + nc.Vec(*p),
                             nc.Vec(self.width / 2 - 150 + star * 60, 20) + nc.Vec(*outline[i - 1]), 1)
        font = self.window.font.get("text", 30)
        text = font.render(f"{stars:.1f}" if stars else " - ", True, nc.RGB.GRAY80)
        self.screen.blit(text, (700, 45 - text.get_height() / 2 + 3))
        text = font.render(f"({rating_count})", True, nc.RGB.GRAY80)
        self.screen.blit(text, (1115, 45 - text.get_height() / 2 + 3))

        # Render title
        font = self.window.font.get("title", 120)
        text = font.render(self.title, True, nc.RGB.WHITE)
        if self.animation_type != 0:
            text.set_alpha(int(abs(255 * ((self.tick - self.animation_start) -
                                          self.ANIMATION_DURATION / 2) / self.ANIMATION_DURATION * 2)))
        black_rect(self.screen, (self.width - self.title_width) / 2 - 30, 115,
                   self.title_width + 55, 110, 130, True, 2)
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
            text.set_alpha(int(abs(255 * ((self.tick - self.animation_start) -
                                          self.ANIMATION_DURATION / 2) / self.ANIMATION_DURATION * 2)))
        self.screen.blit(text, ((self.width - text.get_width()) / 2 + 5, 295))
        text = font.render(self.author, True, nc.RGB.WHITE)
        if self.animation_type != 0:
            text.set_alpha(int(abs(255 * ((self.tick - self.animation_start) -
                                          self.ANIMATION_DURATION / 2) / self.ANIMATION_DURATION * 2)))
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 290))

        # Render description
        font = self.window.font.get("text", 32)
        text1 = font.render(self.description1, True, nc.RGB.WHITE)
        text2 = font.render(self.description2, True, nc.RGB.WHITE)
        if self.animation_type != 0:
            text1.set_alpha(int(abs(255 * ((self.tick - self.animation_start) -
                                           self.ANIMATION_DURATION / 2) / self.ANIMATION_DURATION * 2)))
            text2.set_alpha(int(abs(255 * ((self.tick - self.animation_start) -
                                           self.ANIMATION_DURATION / 2) / self.ANIMATION_DURATION * 2)))
        black_rect(self.screen, (self.width - self.description_width) / 2 - 22, 715 - self.description_height,
                   self.description_width + 40, 70 + self.description_height, 80, True, 2)
        if self.description2 != "":
            self.screen.blit(text1, ((self.width - text1.get_width()) / 2, 680))
            self.screen.blit(text2, ((self.width - text2.get_width()) / 2, 735))
        else:
            self.screen.blit(text1, ((self.width - text1.get_width()) / 2, 735))

        # Render more details
        size = math.sin(self.tick / 5) / 30 + 0.9
        font = self.window.font.get("text", 20)
        text = pg.transform.smoothscale_by(font.render("Mehr Details", True, nc.RGB.BLACK), size)
        if self.animation_type != 0:
            text.set_alpha(int(abs(255 * ((self.tick - self.animation_start) -
                                          self.ANIMATION_DURATION / 2) / self.ANIMATION_DURATION * 2)))
        self.screen.blit(text, ((self.width - text.get_width()) / 2 + 2, 827 - text.get_height() / 2 + self.details_y))
        text = pg.transform.smoothscale_by(font.render("Mehr Details", True, nc.RGB.WHITE), size)
        if self.animation_type != 0:
            text.set_alpha(int(abs(255 * ((self.tick - self.animation_start) -
                                          self.ANIMATION_DURATION / 2) / self.ANIMATION_DURATION * 2)))
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 825 - text.get_height() / 2 + self.details_y))
        size = math.sin(self.tick / 5) / 20 + 0.9
        if self.animation_type != 0:
            self.down_arrow.set_alpha(int(abs(255 * ((self.tick - self.animation_start) -
                                                     self.ANIMATION_DURATION / 2) / self.ANIMATION_DURATION * 2)))
        scaled = pg.transform.smoothscale_by(self.down_arrow, size)
        self.screen.blit(scaled, ((self.width - scaled.get_width()) / 2,
                                  855 - scaled.get_height() / 2 + self.details_y))

        # Render arrows
        size = math.sin(self.tick / 5) * 6 + 100
        if self.animation_type == 1:
            offset = int(35 - abs(35 * ((self.tick - self.animation_start) - self.ANIMATION_DURATION / 2) /
                                  self.ANIMATION_DURATION * 2))
            self.screen.blit(pg.transform.smoothscale(self.left_arrow, (size, size)),
                             (60 - size / 2 - offset, 490 - size / 2))
            self.screen.blit(pg.transform.smoothscale(self.right_arrow, (size, size)),
                             (self.width - 60 - size / 2, 490 - size / 2))
        elif self.animation_type == 2:
            offset = int(35 - abs(35 * ((self.tick - self.animation_start) - self.ANIMATION_DURATION / 2) /
                                  self.ANIMATION_DURATION * 2))
            self.screen.blit(pg.transform.smoothscale(self.right_arrow, (size, size)),
                             (self.width - 60 - size / 2 + offset, 490 - size / 2))
            self.screen.blit(pg.transform.smoothscale(self.left_arrow, (size, size)),
                             (60 - size / 2, 490 - size / 2))
        else:
            self.screen.blit(pg.transform.smoothscale(self.left_arrow, (size, size)),
                             (60 - size / 2, 490 - size / 2))
            self.screen.blit(pg.transform.smoothscale(self.right_arrow, (size, size)),
                             (self.width - 60 - size / 2, 490 - size / 2))

    def update(self) -> None:

        self.tick += self.dt

        if self.window.help_open:
            self.timeout = self.tick
            self.activity_request_tick = 0

        # Scene switching
        if self.tick - self.timeout > 1200:
            self.window.main.game_manager.current = None
            self.window.change_scene("idle", transition_duration=12, transition_pause=7)

        # Update details y position
        if self.details_y != 0:
            self.details_y += self.dt * 3

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

        # Animation running
        if self.animation_type != 0:

            # Reset animation
            if self.tick - self.animation_start >= self.ANIMATION_DURATION:
                self.animation_type = 0
                self.slots.clear()
                font = self.window.font.get("title", 120)
                size = font.size(self.images[self.position % len(self.images)][1].name)
                self.title_width = size[0]
                font = self.window.font.get("text", 32)
                self.description_width = max(font.size(self.description1)[0], font.size(self.description2)[0])
                self.description_height = 55 if self.description2 != "" else 0

            # Switch slot render order and update text fields
            if self.tick - self.animation_start >= self.ANIMATION_DURATION / 2 and not self.animation_switched:
                slot1 = self.slots[1]
                self.slots[1] = self.slots[2]
                self.slots[2] = self.slots[3]
                self.slots[3] = slot1
                self.title = self.images[self.position % len(self.images)][1].name
                self.author = self.images[self.position % len(self.images)][1].author
                split = self.images[self.position % len(self.images)][1].short_description_split
                if split == 0:
                    self.description1 = self.images[self.position % len(self.images)][1].short_description
                    self.description2 = ""
                else:
                    self.description1 = self.images[self.position % len(self.images)][1].short_description[:split]
                    self.description2 = self.images[self.position % len(self.images)][1].short_description[split + 1:]
                self.animation_switched = True

            # Update slot position, size and alpha
            for index, slot in enumerate(self.slots):
                self.slots[index][1] = slot[3] + (slot[4] - slot[3]) / \
                    self.ANIMATION_DURATION * (self.tick - self.animation_start)
                self.slots[index][2] = slot[5] + (slot[6] - slot[5]) / \
                    self.ANIMATION_DURATION * (self.tick - self.animation_start)
                self.slots[index][7] = slot[8] + (slot[9] - slot[8]) / \
                    self.ANIMATION_DURATION * (self.tick - self.animation_start)

            # Update title width
            if self.animation_type != 0:
                self.title_width = int(self.title_width_start + (self.title_width_end - self.title_width_start) /
                                       self.ANIMATION_DURATION * (self.tick - self.animation_start))
                self.description_width = int(self.description_width_start +
                                             (self.description_width_end - self.description_width_start) /
                                             self.ANIMATION_DURATION * (self.tick - self.animation_start))
                self.description_height = int(self.description_height_start +
                                              (self.description_height_end - self.description_height_start) /
                                              self.ANIMATION_DURATION * (self.tick - self.animation_start))

        # Debug screen
        self.window.debug_screen_left.append("")
        self.window.debug_screen_left.append(f"Tick: {self.tick:.1f}")
        self.window.debug_screen_left.append(f"Timeout: {1200 - (self.tick - self.timeout):.1f}")

    def event(self, event: pg.event.Event) -> None:

        if event.type == pg.KEYDOWN:

            # Reset timeout
            self.activity_request_tick_target = 0
            self.timeout = self.tick

            # Switch scene
            if event.key == pg.K_RETURN:
                self.window.change_scene("login", {"back": "menu"}, transition_duration=12, transition_pause=7)

            if event.key == pg.K_m:
                self.window.main.game_manager.current = None
                self.window.change_scene("idle", transition_duration=12, transition_pause=7)

            if self.loaded:

                # More details
                if event.key == pg.K_DOWN:
                    self.window.change_scene("details", transition_duration=8, transition_pause=4)
                    self.details_y = 1

                # Scroll
                if event.key in (pg.K_LEFT, pg.K_RIGHT):
                    self.animation_start = self.tick
                    self.animation_switched = False
                    self.slots.clear()
                    if self.animation_type != 0:
                        self.title = self.images[self.position % len(self.images)][1].name
                    self.star_start = self.images[self.position % len(self.images)][2]
                    self.rating_count_start = self.images[self.position % len(self.images)][3]

                # Scroll to left
                if event.key == pg.K_LEFT:
                    self.position -= 1
                    self.animation_type = 1
                    self.slots.append([self.get_surf(self.position - 1), self.POS1, self.SIZE1,
                                       self.POS1, self.POS2, self.SIZE1, self.SIZE2, 240, 240, 190])
                    self.slots.append([self.get_surf(self.position), self.POS2, self.SIZE2,
                                       self.POS2, self.POS3, self.SIZE2, self.SIZE3, 190, 190, 70])
                    self.slots.append([self.get_surf(self.position + 2), self.POS4, self.SIZE2,
                                       self.POS4, self.POS5, self.SIZE2, self.SIZE1, 190, 190, 240])
                    self.slots.append([self.get_surf(self.position + 1), self.POS3, self.SIZE3,
                                       self.POS3, self.POS4, self.SIZE3, self.SIZE2, 70, 70, 190])

                # Scroll to right
                if event.key == pg.K_RIGHT:
                    self.position += 1
                    self.animation_type = 2
                    self.slots.append([self.get_surf(self.position + 1), self.POS5, self.SIZE1,
                                       self.POS5, self.POS4, self.SIZE1, self.SIZE2, 240, 240, 190])
                    self.slots.append([self.get_surf(self.position), self.POS4, self.SIZE2,
                                       self.POS4, self.POS3, self.SIZE2, self.SIZE3, 190, 190, 70])
                    self.slots.append([self.get_surf(self.position - 2), self.POS2, self.SIZE2,
                                       self.POS2, self.POS1, self.SIZE2, self.SIZE1, 190, 190, 240])
                    self.slots.append([self.get_surf(self.position - 1), self.POS3, self.SIZE3,
                                       self.POS3, self.POS2, self.SIZE3, self.SIZE2, 70, 70, 190])

                # Scroll
                if event.key in (pg.K_LEFT, pg.K_RIGHT):
                    self.star_end = self.images[self.position % len(self.images)][2]
                    self.rating_count_end = self.images[self.position % len(self.images)][3]
                    self.title_width_start = self.title_width
                    self.description_width_start = self.description_width
                    self.description_height_start = self.description_height
                    font = self.window.font.get("title", 120)
                    size = font.size(self.images[self.position % len(self.images)][1].name)
                    self.title_width_end = size[0]
                    font = self.window.font.get("text", 32)
                    split = self.images[self.position % len(self.images)][1].short_description_split
                    if split == 0:
                        description = self.images[self.position % len(self.images)][1].short_description
                        self.description_width_end = font.size(description)[0]
                        self.description_height_end = 0
                    else:
                        description1 = self.images[self.position % len(self.images)][1].short_description[:split]
                        description2 = self.images[self.position % len(self.images)][1].short_description[split + 1:]
                        self.description_width_end = max(font.size(description1)[0], font.size(description2)[0])
                        self.description_height_end = 55

    def init(self) -> None:

        th.Thread(target=self.load_menu, name="Load menu").start()

    def load_menu(self) -> None:

        self.logger.debug("Load game images ...")

        for game in self.window.main.game_manager.games:
            if nc.file.exists(f"{PATH_GAME}/{game.image_name}"):
                image = pg.image.load(f"{PATH_GAME}/{game.image_name}").convert()
            else:
                self.logger.warning(f"Couldn't load game image at '{PATH_GAME}/{game.image_name}'! Use black ...")
                image = pg.Surface((800, 800))
            stars, rating_count = self.window.main.user_manager.get_ratings(game.id)
            self.images.append((image, game, stars, rating_count))
            if game == self.window.main.game_manager.current:
                self.position = len(self.images) - 1

        if not self.images:
            raise ConfigError("At least one game is required for the menu!")

        self.title = self.images[self.position % len(self.images)][1].name
        font = self.window.font.get("title", 120)
        size = font.size(self.title)
        self.title_width = size[0]

        self.author = self.images[self.position % len(self.images)][1].author

        split = self.images[self.position % len(self.images)][1].short_description_split
        font = self.window.font.get("text", 32)
        if split == 0:
            self.description1 = self.images[self.position % len(self.images)][1].short_description
            self.description2 = ""
            self.description_width = font.size(self.description1)[0]
            self.description_height = 0
        else:
            self.description1 = self.images[self.position % len(self.images)][1].short_description[:split]
            self.description2 = self.images[self.position % len(self.images)][1].short_description[split + 1:]
            self.description_width = max(font.size(self.description1)[0], font.size(self.description2)[0])
            self.description_height = 55

        self.loaded = True

    def get_surf(self, pos: int) -> pg.Surface:
        return self.images[pos % len(self.images)][0]

    def quit(self) -> None:

        self.window.main.game_manager.current = self.images[self.position % len(self.images)][1]
