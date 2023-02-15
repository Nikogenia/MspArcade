# Standard
from __future__ import annotations
from typing import TYPE_CHECKING
import threading as th

# External
import nikocraft as nc
import pygame as pg
import cv2

# Local
from constants import *
from window.scenes.loading import LoadingScene
from window.scenes.idle import IdleScene
from window.scenes.menu import MenuScene
from window.scenes.login import LoginScene
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

        #self.disable_resolution_scaling()

        # Register scenes
        self.register_scene("loading", LoadingScene)
        self.register_scene("idle", IdleScene)
        self.register_scene("menu", MenuScene)
        self.register_scene("login", LoginScene)

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
                self.background: pg.Surface = pg.image.load(f"{PATH_DATA}/{self.main.main_config.background_file_name}")
                self.background_mode: str = "image"
            else:
                self.logger.warning(f"Couldn't load background image at '{PATH_DATA}/{self.main.main_config.background_file_name}'! Use black ...")
                self.background: pg.Surface = pg.Surface(self.dimension)
                self.background_mode: str = "error"

        elif self.main.main_config.background_mode == "video":
            self.logger.info("Load background video ...")
            if nc.file.exists(f"{PATH_DATA}/{self.main.main_config.background_file_name}"):
                self.background: pg.Surface = pg.Surface(self.dimension)
                self.video: cv2.VideoCapture = cv2.VideoCapture(f"{PATH_DATA}/{self.main.main_config.background_file_name}")
                self.background_mode: str = "video"
                self.background_update: float = 0
            else:
                self.logger.warning(f"Couldn't load background video at '{PATH_DATA}/{self.main.main_config.background_file_name}'! Use black ...")
                self.background: pg.Surface = pg.Surface(self.dimension)
                self.background_mode: str = "error"

        else:
            raise ValueError("Invalid background mode in config! Please use 'image' or 'video' ...")

        # Load background brightness
        self.background_black: pg.Surface = pg.Surface(self.dimension)
        self.background_black.fill(nc.RGB.BLACK)

        self.fps_log = []

    def render(self) -> None:

        # Render background
        self.screen.blit(self.background, (0, 0))
        self.background_black.set_alpha(self.scene.brightness)
        self.screen.blit(self.background_black, (0, 0))

        self.render_scene()

        if self.debug_screen_active:
            self.debug_screen.render(self.debug_screen_left, self.debug_screen_right)
        self.debug_screen_left = self.debug_screen.left_content()
        self.debug_screen_right = self.debug_screen.right_content()

    def event(self, event: pg.event.Event) -> None:

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.running = False
            if event.key == pg.K_F3:
                self.debug_screen_active = not self.debug_screen_active

    def update(self) -> None:

        self.debug_screen_left.append("")
        self.debug_screen_left.append(f"Background Update: {self.background_update * 1000:.2f} ms")

        self.debug_screen_right.append("")
        self.debug_screen_right.append("Database Update")
        if self.main.user_manager.last_update == 0:
            self.debug_screen_right.append(f"-")
        else:
            self.debug_screen_right.append(f"{nc.time.epoch_time() - self.main.user_manager.last_update:.1f} seconds")

        if SHOW_USERS_IN_DEBUG_SCREEN:
            self.debug_screen_right.append("")
            self.debug_screen_right.append("Players")
            for player in self.main.user_manager.players:
                self.debug_screen_right.append("")
                self.debug_screen_right.append(player.auth_id)
                self.debug_screen_right.append(f"{player.time} - {player.name}")

        if FPS_LOG:
            self.fps_log.append((f"{self.clock.available_fps:.2f}", f"{self.clock.available_fps_low:.2f}", f"{self.clock.available_fps_lazy:.2f}"))

    def init(self) -> None:

        self.running = True

        if self.background_mode == "video":
            th.Thread(target=self.background_thread, name="Background").start()

    def quit(self) -> None:

        for normal, low, lazy in self.fps_log:
            print(f"{normal:<10} {low:<10} {lazy:<10}")

    def background_thread(self) -> None:

        clock = pg.time.Clock()

        while self.running:

            clock.tick(30)

            start = nc.time.bench_time()

            _, frame = self.video.read()

            if not _:
                self.video.release()
                self.video: cv2.VideoCapture = cv2.VideoCapture(f"{PATH_DATA}/{self.main.main_config.background_file_name}")
                _, frame = self.video.read()

            self.background = cv_utils.cv_to_pygame(frame)

            end = nc.time.bench_time()
            self.background_update = end - start

        self.logger.info("Release background video ...")
        self.video.release()
