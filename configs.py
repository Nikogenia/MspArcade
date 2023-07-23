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
        self.database_auth_token: str = ""
        self.database_auto_update: int = 300
        self.database_fast_update: int = 22

        self.background_mode: str = "image"
        self.background_file_name: str = "background.png"

        self.listener_port: int = 42000
        self.listener_key: str = "DefaultKey"

        self.debug_screen_show_default: bool = False
        self.debug_screen_show_users: bool = False

        self.log_response: bool = False
        self.log_fps: bool = False

        self.windows_disable_resolution_scaling: bool = False
        self.windows_select_second_monitor: bool = False

        self.account_default_time: int = 300
        self.account_reset_timeout: int = 604800
        self.account_time_refresh: bool = False

        self.show_offline_warning: bool = True

        self.restart_on_crash: bool = True

        self.email_send: bool = False
        self.email_server_address: str = ""
        self.email_server_port: int = 465
        self.email_server_user: str = ""
        self.email_server_password: str = ""
        self.email_sender: str = ""
        self.email_targets: list[str] = []

        self.key_left: str = "j"
        self.key_right: str = "l"
        self.key_up: str = "i"
        self.key_down: str = "k"
        self.key_reset: str = "n"
        self.key_quit: str = "m"
        self.key_b1: str = "x"
        self.key_b2: str = "c"
        self.key_b3: str = "v"
        self.key_b4: str = "b"


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
                "image_name": "Template.png",
                "url": "https://www.bodensee-gymnasium.de/"
            }
        ]


class UserConfig(nc.Config):

    def __init__(self, logger):

        super(UserConfig, self).__init__(f"{PATH_CONFIG}/user.json", logger)

        self.users: list[dict[str, Any]] = []
        self.players: list[dict[str, Any]] = []

        self.admins: list[int] = []
        self.banned: list[int] = []

        self.last_refresh: int = 0
