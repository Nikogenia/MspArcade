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


CODE = """
export DISPLAY=:0

sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/kiosk/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/kiosk/.config/chromium/Default/Preferences

exec /usr/bin/chromium-browser --window-size=1920,1080 --kiosk --window-position=0,0 #URL#
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

                while self.running_game:
                    player = self.main.user_manager.get_player_by_auth_id(self.main.user_manager.current)
                    if player.time <= 0:
                        self.close_browser()
                    else:
                        player.time -= 1
                        nc.time.wait(1)

                nc.time.wait(0.5)

        except Exception:
            self.main.running = False
            self.main.window.running = False
            self.main.user_manager.running = False
            raise

    def open_browser(self) -> None:

        url = self.current.data["url"] if "url" in self.current.data else "https://bodensee-gymnasium.de/"
        self.browser = sp.Popen(CODE.replace("#URL#", url), shell=True)
        nc.time.wait(3)

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
