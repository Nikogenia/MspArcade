# Standard
from __future__ import annotations
from typing import TYPE_CHECKING
import threading as th
import multiprocessing as mp
from logging import Logger
import subprocess as sp
import os

# External
import nikocraft as nc
from pynput.mouse import Controller as MouseController

# Local
from configs import ConfigError
from game.game import Game
from game import time_display
if TYPE_CHECKING:
    from main import Main


CODE = """
export DISPLAY=:0

sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/maker/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/maker/.config/chromium/Default/Preferences

exec /usr/bin/chromium --start-fullscreen #URL#
"""


class GameManager(th.Thread):

    def __init__(self, main: Main):

        super(GameManager, self).__init__(name="Game")

        self.main: Main = main

        self.running: bool = True

        self.games: list[Game] = []

        self.current: Game | None = None

        self.start_game: bool = False

        self.browser: sp.Popen | None = None

        self.time_display_proc: mp.Process | None = None
        self.time_display_queue: mp.Queue = mp.Queue()

        self.sim_running_browser: bool = False

        self.reload: bool = False

    # PROPERTIES

    @property
    def logger(self) -> Logger:
        return self.main.logger

    # METHODS

    def run(self) -> None:

        try:

            self.load()

            while self.running:

                if self.reload:
                    self.start_game = False
                    self.current: Game | None = None
                    self.load()
                    self.reload = False

                if self.start_game:

                    self.logger.info(f"Start game '{self.current.name}' ...")
                    self.open()
                    self.start_game = False
                    self.main.window.background_video_update = False

                    while self.running_game:

                        if (not self.running) or self.reload:
                            self.close()
                            continue

                        if self.current.type == "makecode":
                            mouse = MouseController()
                            mouse.move(-10, -10)
                            nc.time.wait(0.1)
                            mouse.move(10, 10)

                        player = self.main.user_manager.get_player_by_auth_id(self.main.user_manager.current)
                        if player is None:
                            self.close()
                            continue

                        admin = self.main.user_manager.is_admin(player.user_id) or \
                            player.user_id in self.current.owners

                        if player.time <= 0:
                            self.close()
                        else:
                            if not admin:
                                player.time -= 1
                            self.time_display_queue.put(86400 if admin else player.time)
                            nc.time.wait(1)

                    self.time_display_queue.put("QUIT")
                    self.main.window.background_video_update = True
                    self.logger.info("Game closed.")

                nc.time.wait(0.6)

        except Exception:
            self.main.handle_crash()

    def open(self) -> None:

        if self.current.type in ("web", "makecode", "scratch"):
            self.open_browser()

    def close(self) -> None:

        if self.current.type in ("web", "makecode", "scratch"):
            self.close_browser()

    def open_browser(self) -> None:

        if os.name == "nt":
            self.logger.debug("Running on windows. Use simulation ...")
            self.sim_running_browser = True
        else:
            url = self.current.data["url"] if "url" in self.current.data else "https://bodensee-gymnasium.de/"
            self.logger.debug(f"Open URL {url} ...")
            self.browser = sp.Popen(CODE.replace("#URL#", url), shell=True)

            nc.time.wait(2.5)

            self.logger.debug("Open time display ...")
            self.time_display_proc: mp.Process = mp.Process(
                target=time_display.run, args=(self.time_display_queue,), name="Time Display", daemon=True)
            self.time_display_proc.start()

    def close_browser(self) -> None:

        if os.name == "nt":
            self.logger.debug("Stop simulation ...")
            self.sim_running_browser = False
        else:
            self.logger.debug("Kill browser ...")
            self.browser.kill()

    @property
    def running_game(self) -> bool:

        if os.name == "nt":
            return self.start_game or self.sim_running_browser

        return self.start_game or (self.browser is not None and self.browser.poll() is None)

    def load(self) -> None:

        self.logger.info("Load games from config ...")

        self.games.clear()

        ids = []

        for data in self.main.game_config.games:
            game = Game.from_json(data, self.logger)
            if game is None:
                continue
            if game.id in ids:
                raise ConfigError(f"Duplicated game ID {game.id} found in config!")
            self.logger.debug(f"Game '{game.name}' ({game.author}) [{game.type}] loaded.")
            self.games.append(game)
            ids.append(game.id)

        self.logger.info(f"Successfully loaded {len(self.games)} games!")

    def get_game(self, name: str) -> Game:

        for game in self.games:
            if game.name == name:
                return game
