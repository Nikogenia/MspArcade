# Standard
from __future__ import annotations
from typing import TYPE_CHECKING

# External
import nikocraft as nc
import pygame as pg

# Local
from constants import *
from scenes.loading import LoadingScene
from scenes.idle import IdleScene
from scenes.menu import MenuScene
from scenes.login import LoginScene
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
        self.debug_screen_active: bool = False

        # Load background
        if self.main.main_config.background_mode == "image":
            if nc.file.exists(f"{PATH_DATA}/{self.main.main_config.background_file_name}"):
                self.background: pg.Surface = pg.image.load(f"{PATH_DATA}/{self.main.main_config.background_file_name}")
            else:
                self.logger.warning(f"Couldn't load background image at '{PATH_DATA}/{self.main.main_config.background_file_name}'! Use black ...")
                self.background: pg.Surface = pg.Surface(self.dimension)
                self.background.fill(nc.RGB.BLACK)

        elif self.main.main_config.background_mode == "video":
            # TODO Video background
            raise ValueError("The video background is not available yet!")

        else:
            raise ValueError("Invalid background mode in config! Please use 'image' or 'video' ...")

        # Load background brightness
        self.background_black: pg.Surface = pg.Surface(self.dimension)
        self.background_black.fill(nc.RGB.BLACK)

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
