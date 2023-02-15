# Standard
from __future__ import annotations
from typing import TYPE_CHECKING
import threading as th
from logging import Logger

# External
import nikocraft as nc

# Local
from constants import *
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

    # PROPERTIES

    @property
    def logger(self) -> Logger:
        return self.main.logger

    # METHODS

    def run(self) -> None:

        self.load()

        while self.running:

            nc.time.wait(1)

    def load(self) -> None:

        self.logger.info("Load games from config ...")

        self.games.clear()

        for data in self.main.game_config.games:
            game = Game.from_json(data)
            if game is None:
                self.logger.warning(f"Failed to load a game! Data: {data}")
                continue
            self.logger.debug(f"Game '{game.name}' ({game.author}) [{game.type}] loaded.")
            self.games.append(game)

        self.logger.info(f"Successfully loaded {len(self.games)} games!")

    def get_game(self, name: str) -> Game:

        for game in self.games:
            if game.name == name:
                return game
