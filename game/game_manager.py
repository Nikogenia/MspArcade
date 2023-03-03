# Standard
from __future__ import annotations
from typing import TYPE_CHECKING
import threading as th
from logging import Logger
import subprocess as sp

# External
import nikocraft as nc

# Local
from configs import ConfigError
from game.game import Game
if TYPE_CHECKING:
    from main import Main


class GameManager(th.Thread):

    def __init__(self, main: Main):

        super(GameManager, self).__init__(name="Game")

        self.main: Main = main

        self.running: bool = True

        self.games: list[Game] = []

        self.current: Game | None = None

        self.start_game: bool = False

        self.browser: sp.Popen | None = None

    # PROPERTIES

    @property
    def logger(self) -> Logger:
        return self.main.logger

    # METHODS

    def run(self) -> None:

        try:

            self.load()

            while self.running:

                if self.start_game:
                    self.open_browser()
                    self.start_game = False

                nc.time.wait(1)

        except Exception:
            self.main.running = False
            self.main.window.running = False
            self.main.user_manager.running = False
            raise

    def open_browser(self) -> None:

        self.browser = sp.Popen("./open.sh")

        nc.time.wait(8)

    def close_browser(self) -> None:

        self.browser.kill()

    @property
    def running_game(self) -> bool:
        return self.start_game or (self.browser is not None and self.browser.poll() is None)

    def load(self) -> None:

        self.logger.info("Load games from config ...")

        self.games.clear()

        ids = []

        for data in self.main.game_config.games:
            game = Game.from_json(data)
            if game is None:
                self.logger.warning(f"Failed to load a game! Data: {data}")
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
