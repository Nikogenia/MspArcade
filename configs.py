# Standard
from typing import Any

# External
import nikocraft as nc

# Local
from constants import *


class ConfigError(Exception):
    pass


class MainConfig(nc.Config):

    def __init__(self, logger):

        super(MainConfig, self).__init__(f"{PATH_CONFIG}/main.json", logger)

        self.database_id: str = ""
        self.auth_token: str = ""

        self.background_mode: str = "image"
        self.background_file_name: str = "background.png"

        self.admin_users: list[str] = []
        self.banned_users: list[str] = []


class GameConfig(nc.Config):

    def __init__(self, logger):

        super(GameConfig, self).__init__(f"{PATH_CONFIG}/game.json", logger)

        self.games: list[dict[str, Any]] = [
            {
                "id": 0,
                "name": "Template",
                "type": "web",
                "short_description": "Hello World",
                "short_description_split": 0,
                "description": "This is a cool game!",
                "author": "Maker Space",
                "image_name": "template.png",
                "url": "https://www.bodensee-gymnasium.de/"
            }
        ]


class UserConfig(nc.Config):

    def __init__(self, logger):

        super(UserConfig, self).__init__(f"{PATH_CONFIG}/user.json", logger)

        self.users: list[dict[str, Any]] = []
        self.players: list[dict[str, Any]] = []
