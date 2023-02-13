# Standard
from typing import Any

# External
import nikocraft as nc

# Local
from constants import *


class MainConfig(nc.Config):

    def __init__(self, logger):

        super(MainConfig, self).__init__(f"{PATH_CONFIG}/main.json", logger)

        self.database_id: str = ""
        self.auth_token: str = ""

        self.background_mode: str = "image"
        self.background_file_name: str = "background.png"


class GameConfig(nc.Config):

    def __init__(self, logger):

        super(GameConfig, self).__init__(f"{PATH_CONFIG}/game.json", logger)

        self.games: list[dict[str, Any]] = [
            {
                "name": "Template",
                "type": "web",
                "short_description": "Hello World",
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

        self.time_changes: list[dict[str, Any]] = []
        self.rating_changes: list[dict[str, Any]] = []
        self.last_login_changes: list[dict[str, Any]] = []
