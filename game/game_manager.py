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
from pynput.mouse import Button

# Local
from configs import ConfigError
from game.game import Game
from game import time_display
from game import info_display
if TYPE_CHECKING:
    from main import Main


BROWSER_CODE = """
export DISPLAY=:0

sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/maker/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/maker/.config/chromium/Default/Preferences

exec /usr/bin/chromium --kiosk #URL#
"""


class GameManager(th.Thread):

    def __init__(self, main: Main):

        super(GameManager, self).__init__(name="Game")

        self.main: Main = main

        self.running: bool = True

        self.games: list[Game] = []

        self.current: Game | None = None

        self.start_game: bool = False

        self.game_process: sp.Popen | None = None

        self.time_display_proc: mp.Process | None = None
        self.time_display_queue: mp.Queue = mp.Queue()
        self.info_display_proc: mp.Process | None = None
        self.info_display_queue: mp.Queue = mp.Queue()

        self.sim_running_game: bool = False

        self.reload: bool = False

        self.scratch_initial_reset: bool = False

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
                    start_time = nc.time.bench_time()
                    self.scratch_initial_reset = False

                    while self.running_game:

                        delay = 0

                        if (not self.running) or self.reload:
                            self.close()
                            continue

                        if self.current.type == "makecode" and nc.time.bench_time() - start_time >= 3:
                            BUTTON_X = 1850
                            BUTTON_Y = 800
                            mouse = MouseController()
                            mouse.move(BUTTON_X - mouse.position[0], BUTTON_Y - mouse.position[1])
                            nc.time.wait(0.1)
                            delay += 0.1
                            mouse.click(Button.left, 1)
                            mouse.move(5, 5)

                        if self.current.type == "scratch" and not self.scratch_initial_reset and nc.time.bench_time() - start_time >= 10:
                            self.scratch_initial_reset = True
                            BUTTON_X = 297
                            BUTTON_Y = 27
                            mouse = MouseController()
                            mouse.move(BUTTON_X - mouse.position[0], BUTTON_Y - mouse.position[1])
                            self.logger.info(f"Mouse click at position ({mouse.position[0]}, {mouse.position[1]}) for game restart")
                            nc.time.wait(0.1)
                            delay += 0.1
                            mouse.click(Button.left, 1)

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
                            nc.time.wait(1 - delay)

                    self.time_display_queue.put("QUIT")
                    if self.current.type == "scratch":
                        self.info_display_queue.put("QUIT")
                    self.main.window.background_video_update = True
                    self.logger.info("Game closed.")

                nc.time.wait(0.6)

        except Exception:
            self.main.handle_crash()

    def open(self) -> None:

        if os.name == "nt":
            self.logger.debug("Running on windows. Use simulation ...")
            self.sim_running_game = True
        else:
            if self.current.type in ("web", "makecode", "scratch"):
                self.open_browser()
            if self.current.type == "exec":
                self.open_exec()

            nc.time.wait(2.5)

            self.logger.debug("Open time display ...")
            self.time_display_proc: mp.Process = mp.Process(
                target=time_display.run, args=(self.time_display_queue,), name="Time Display", daemon=True)
            self.time_display_proc.start()

            if self.current.type == "scratch":
                self.logger.debug("Open info display ...")
                self.info_display_proc: mp.Process = mp.Process(
                    target=info_display.run, args=(self.info_display_queue,), name="Info Display", daemon=True)
                self.info_display_proc.start()

    def close(self) -> None:

        if os.name == "nt":
            self.logger.debug("Stop simulation ...")
            self.sim_running_game = False
        else:
            if self.current.type in ("web", "makecode", "scratch"):
                self.close_browser()
            if self.current.type == "exec":
                self.close_exec()

        self.main.window.focus()

    def open_browser(self) -> None:

        url = self.current.data["url"] if "url" in self.current.data else "https://bodensee-gymnasium.de/"
        self.logger.debug(f"Open URL {url} ...")
        self.game_process = sp.Popen(BROWSER_CODE.replace("#URL#", url), shell=True)

    def open_exec(self) -> None:

        command = self.current.data["command"] if "command" in self.current.data else ""
        command = f"export DISPLAY=:0 && {command}"
        self.logger.debug(f"Execute command {command} ...")
        self.game_process = sp.Popen(command, shell=True)

    def close_browser(self) -> None:

        self.logger.debug("Kill browser ...")
        self.game_process.kill()

    def close_exec(self) -> None:

        self.logger.debug("Terminate game ...")
        self.game_process.terminate()
        nc.time.wait(2)
        if self.game_process.poll() is None:
            self.logger.debug("Kill game ...")
            self.game_process.kill()

    @property
    def running_game(self) -> bool:

        if os.name == "nt":
            return self.start_game or self.sim_running_game

        return self.start_game or (self.game_process is not None and self.game_process.poll() is None)

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

    def reset_button(self) -> bool:

        if self.running_game and self.current.type == "scratch":
            self.scratch_initial_reset = True
            BUTTON_X = 297
            BUTTON_Y = 27
            mouse = MouseController()
            mouse.move(BUTTON_X - mouse.position[0], BUTTON_Y - mouse.position[1])
            self.logger.info(f"Mouse click at position ({mouse.position[0]}, {mouse.position[1]}) for game restart")
            nc.time.wait(0.1)
            mouse.click(Button.left, 1)
            return False
        
        return True
