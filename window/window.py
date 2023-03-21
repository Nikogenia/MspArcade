# Standard
from __future__ import annotations
from typing import TYPE_CHECKING
import threading as th
import multiprocessing as mp
from queue import Empty
import os
import math

# External
import nikocraft as nc
import pygame as pg
import cv2

# Local
from constants import *
from configs import ConfigError
from window.draw_utils import black_rect, draw_button
from window.scenes.loading import LoadingScene
from window.scenes.idle import IdleScene
from window.scenes.menu import MenuScene
from window.scenes.login import LoginScene
from window.scenes.details import DetailsScene
from window.scenes.overview import OverviewScene
from window.scenes.play import PlayScene
from window.scenes.rating import RatingScene
from window.scenes.banned import BannedScene
from window import input_controller
from window import cv_utils
if TYPE_CHECKING:
    from main import Main


class Window(nc.Window):

    def __init__(self, main: Main):

        super(Window, self).__init__(main,
                                     fps=GUI_FPS,
                                     width=GUI_WIDTH,
                                     height=GUI_HEIGHT,
                                     flags=pg.FULLSCREEN,
                                     scene_mode=True,
                                     start_scene="loading")

        self.main: Main = main

        self.running = True

        # Select second monitor
        if SELECT_SECOND_MONITOR:
            os.environ['SDL_VIDEO_WINDOW_POS'] = f"-1920,0"

        # Resolution scaling on windows
        if DISABLE_RESOLUTION_SCALING:
            self.disable_resolution_scaling()

        # Register scenes
        self.register_scene("loading", LoadingScene)
        self.register_scene("idle", IdleScene)
        self.register_scene("menu", MenuScene)
        self.register_scene("login", LoginScene)
        self.register_scene("details", DetailsScene)
        self.register_scene("overview", OverviewScene)
        self.register_scene("play", PlayScene)
        self.register_scene("rating", RatingScene)
        self.register_scene("banned", BannedScene)

        # Define fonts
        self.font.define("title", f"{PATH_FONT}/Arcade.ttf")
        self.font.define("text", f"{PATH_FONT}/PressStart2P.ttf")

        # Debug screen
        self.debug_screen: nc.DebugScreen = nc.DebugScreen(self)
        self.debug_screen_left: list[str] = []
        self.debug_screen_right: list[str] = []
        self.debug_screen_active: bool = SHOW_FPS_DEFAULT

        # Load background
        if self.main.main_config.background_mode == "image":
            self.logger.info("Load background image ...")
            if nc.file.exists(f"{PATH_DATA}/{self.main.main_config.background_file_name}"):
                self.background: pg.Surface = pg.image.load(
                    f"{PATH_DATA}/{self.main.main_config.background_file_name}")
                self.background_mode: str = "image"
            else:
                self.logger.warning(f"Couldn't load background image at '{PATH_DATA}/" +
                                    f"{self.main.main_config.background_file_name}'! Use black ...")
                self.background: pg.Surface = pg.Surface(self.dimension)
                self.background_mode: str = "error"

        elif self.main.main_config.background_mode == "video":
            self.logger.info("Load background video ...")
            if nc.file.exists(f"{PATH_DATA}/{self.main.main_config.background_file_name}"):
                self.background: pg.Surface = pg.Surface(self.dimension)
                self.video: cv2.VideoCapture = cv2.VideoCapture(
                    f"{PATH_DATA}/{self.main.main_config.background_file_name}")
                self.background_mode: str = "video"
                self.background_update: float = 0
            else:
                self.logger.warning(f"Couldn't load background video at '{PATH_DATA}/" +
                                    f"{self.main.main_config.background_file_name}'! Use black ...")
                self.background: pg.Surface = pg.Surface(self.dimension)
                self.background_mode: str = "error"

        elif self.main.main_config.background_mode == "off":
            self.logger.info("Background disabled.")
            self.background: pg.Surface = pg.Surface(self.dimension)
            self.background_mode: str = "off"

        else:
            raise ConfigError("Invalid background mode in config! Please use 'image', 'video' or 'off' ...")

        # Load background brightness
        self.background_black: pg.Surface = pg.Surface(self.dimension)
        self.background_black.fill(nc.RGB.BLACK)

        # Background video update
        self.background_video_update: bool = True

        # Help popup
        self.help_open: bool = False
        self.help_tick: float = 0
        self.help_tick_target: float = 0
        self.help_timeout: float = 0

        # FPS log
        self.fps_log = []

        # Deactivate joysticks
        pg.joystick.quit()

        # Load input controller
        self.input_controller_queue: mp.Queue = mp.Queue()
        self.input_controller_proc: mp.Process = mp.Process(
            target=input_controller.run, args=(self.input_controller_queue,), name="Input Controller", daemon=True)

        # Controller input data
        self.controller_left: bool = False
        self.controller_right: bool = False
        self.controller_up: bool = False
        self.controller_down: bool = False
        self.controller_reset: bool = False
        self.controller_quit: bool = False
        self.controller_b1: bool = False
        self.controller_b2: bool = False
        self.controller_b3: bool = False
        self.controller_b4: bool = False

    def render(self) -> None:

        # Render background
        self.screen.blit(self.background, (0, 0))
        self.background_black.set_alpha(self.scene.brightness)
        self.screen.blit(self.background_black, (0, 0))

        # Render scene content
        self.render_scene()

        # Offline info
        if not self.main.user_manager.online:
            font = self.font.get("text", 14)
            text = font.render("HINWEIS: Die Datenbank kann aktuell nicht erreicht werden!", True, nc.RGB.RED1)
            black_rect(self.screen, -10, self.height - 50, text.get_width() + 20, 70, 220, True, 1)
            self.screen.blit(text, (7, self.height - 42))
            text = font.render("         Neue Registrierungen sind daher nicht verfügbar!", True, nc.RGB.RED1)
            self.screen.blit(text, (7, self.height - 22))

        # Help info
        if self.help_tick < 0.85:
            font = self.font.get("text", 20)
            text = font.render("Hilfe? Drücke  !", True, nc.RGB.WHITE)
            black_rect(self.screen, self.width - text.get_width() - 10,
                       self.height - 37, text.get_width() + 20, 50, 220, True, 1)
            self.screen.blit(text, (self.width - text.get_width(), self.height - 27))
            draw_button(self.screen, font, 14, self.width - text.get_width(), self.height - 27, HELP_BUTTON)
        self.draw_help_popup()

        # Render debug screen
        if self.debug_screen_active:
            self.debug_screen.render(self.debug_screen_left, self.debug_screen_right)
        self.debug_screen_left = self.debug_screen.left_content()
        self.debug_screen_right = self.debug_screen.right_content()

    def event(self, event: pg.event.Event) -> None:

        if event.type == pg.KEYDOWN:

            # Quitting
            if event.key == pg.K_ESCAPE:
                self.running = False

            # Toggle debug screen
            if event.key == pg.K_F3:
                self.debug_screen_active = not self.debug_screen_active

            # Toggle help popup
            if event.key == pg.K_h:
                self.help_open = not self.help_open
                if self.help_open:
                    self.help_timeout = nc.time.bench_time()
                    self.help_tick_target = 1
                else:
                    self.help_tick_target = 0

            # Close help popup
            if event.key == pg.K_r:
                self.help_open = False
                self.help_tick_target = 0

    def update(self) -> None:

        self.update_input()

        # Animate help popup
        if abs(self.help_tick_target - self.help_tick) < 0.09:
            self.help_tick = self.help_tick_target
        if self.help_tick > self.help_tick_target:
            self.help_tick -= self.dt / 13
        elif self.help_tick < self.help_tick_target:
            self.help_tick += self.dt / 13

        if nc.time.bench_time() - self.help_timeout > 25:
            self.help_open = False
            self.help_tick_target = 0

        # Debug screen information
        if self.background_mode == "video":
            self.debug_screen_left.append("")
            self.debug_screen_left.append(f"Background Update: {self.background_update * 1000:.2f} ms")

        current_game = self.main.game_manager.current
        self.debug_screen_left.append("")
        self.debug_screen_left.append(f"Current Game: {None if current_game is None else current_game.name}")

        self.debug_screen_right.append("")
        self.debug_screen_right.append("Database Update")
        if self.main.user_manager.last_update == 0:
            self.debug_screen_right.append(f"-")
        else:
            self.debug_screen_right.append(
                f"{nc.time.epoch_time() - self.main.user_manager.last_update:.1f} seconds")

        if SHOW_USERS_IN_DEBUG_SCREEN:
            current_player = self.main.user_manager.current
            self.debug_screen_right.append("")
            self.debug_screen_right.append("Current Player")
            self.debug_screen_right.append(f"{None if current_player == '' else current_player}")
            self.debug_screen_right.append("")
            self.debug_screen_right.append("Players")
            for player in self.main.user_manager.players:
                self.debug_screen_right.append("")
                self.debug_screen_right.append(player.auth_id)
                self.debug_screen_right.append(f"{player.time} - {player.name}")

        if FPS_LOG:
            self.fps_log.append((f"{self.clock.available_fps:.2f}", f"{self.clock.available_fps_low:.2f}",
                                 f"{self.clock.available_fps_lazy:.2f}"))

    def init(self) -> None:

        self.input_controller_proc.start()

        if self.background_mode == "video":
            th.Thread(target=self.background_thread, name="Background").start()

    def quit(self) -> None:

        for normal, low, lazy in self.fps_log:
            print(f"{normal:<10} {low:<10} {lazy:<10}")

        pg.quit()

        self.input_controller_proc.kill()

    def background_thread(self) -> None:

        clock = pg.time.Clock()

        while self.running:

            clock.tick(30)

            if not self.background_video_update:
                continue

            start = nc.time.bench_time()

            _, frame = self.video.read()

            if not _:
                self.video.release()
                self.video: cv2.VideoCapture = cv2.VideoCapture(
                    f"{PATH_DATA}/{self.main.main_config.background_file_name}")
                _, frame = self.video.read()

            self.background = cv_utils.cv_to_pygame(frame)

            end = nc.time.bench_time()
            self.background_update = end - start

        self.logger.info("Release background video ...")
        self.video.release()

    def early_update(self) -> None:

        if not self.main.running:
            self.running = False

    @staticmethod
    def reset() -> None:

        pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_r}))

    def update_input(self) -> None:

        try:

            while True:

                code, state, device = self.input_controller_queue.get(block=False)
                self.logger.debug((code, state, device))

                match code:

                    case "BTN_TRIGGER":
                        if state:
                            pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_RETURN}))
                            pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_SPACE}))
                        self.controller_b1 = bool(state)
                    case "BTN_THUMB":
                        if state:
                            pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_SPACE}))
                        self.controller_b2 = bool(state)
                    case "BTN_THUMB2":
                        if state:
                            pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_SPACE}))
                        self.controller_b3 = bool(state)
                    case "BTN_TOP":
                        if state:
                            pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_h}))
                            pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_SPACE}))
                        self.controller_b4 = bool(state)
                    case "BTN_PINKIE":
                        if state:
                            self.reset()
                        self.controller_reset = bool(state)
                    case "BTN_TOP2":
                        if state:
                            pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_q}))
                            pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_SPACE}))
                        self.controller_quit = bool(state)
                    case "ABS_X":
                        if state == 127:
                            self.controller_left = False
                            self.controller_right = False
                        elif state == 0:
                            pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_LEFT}))
                            pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_SPACE}))
                            self.controller_left = True
                            self.controller_right = False
                        elif state == 255:
                            pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_RIGHT}))
                            pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_SPACE}))
                            self.controller_left = False
                            self.controller_right = True
                    case "ABS_Y":
                        if state == 127:
                            self.controller_up = False
                            self.controller_down = False
                        elif state == 0:
                            pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_UP}))
                            pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_SPACE}))
                            self.controller_up = True
                            self.controller_down = False
                        elif state == 255:
                            pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_DOWN}))
                            pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_SPACE}))
                            self.controller_up = False
                            self.controller_down = True

        except Empty:
            pass

    def draw_help_popup(self) -> None:

        if self.help_tick <= 0.2:
            return

        width = 1895 * self.help_tick
        height = 1055 * self.help_tick

        black_rect(self.screen, (self.width - width) / 2, (self.height - height) / 2, width, height,
                   int(self.help_tick * 210), True, math.ceil(self.help_tick * 5), nc.RGB.WHITE * self.help_tick)

        if self.help_tick != 1:
            return

        font = self.font.get("text", 40)
        text = font.render("Schließen  ", True, nc.RGB.WHITE)
        self.screen.blit(text, (self.width - text.get_width() - 40, 40))
        draw_button(self.screen, font, 10, self.width - text.get_width() - 40, 40 - 2, HELP_BUTTON)

        y = 35

        font = self.font.get("title", 130)
        text = font.render("Hilfe", True, nc.RGB.WHITE)
        self.screen.blit(text, (50, y))

        font = self.font.get("title", 100)
        text = font.render("Credits", True, nc.RGB.WHITE)
        self.screen.blit(text, (50, 700))

        font = self.font.get("text", 24)
        text = font.render("MAKER SPACE © 2023 - Open Source (MIT Licence)", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 980))
        font = self.font.get("text", 16)
        text = font.render("Bodensee-Gymnasium Lindau", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 1020))
