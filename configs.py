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

        self.database_url: str = "https://lernplattform.mebis.bycs.de/webservice/rest/server.php?"
        self.database_id: str = ""
        self.database_auth_token: str = ""
        self.database_auto_update: int = 300
        self.database_fast_update: int = 10

        self.background_mode: str = "image"
        self.background_file_name: str = "background.png"

        self.listener_port: int = 42000
        self.listener_key: str = "makerspace"

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

        self.email_active: bool = False
        self.email_server_address: str = "mail.nikogenia.de"
        self.email_server_port: int = 465
        self.email_server_user: str = "arcade@nikogenia.de"
        self.email_server_password: str = ""
        self.email_sender: str = "arcade@nikogenia.de"
        self.email_targets: list[str] = [
            "arcade@nikogenia.de"
        ]

        self.key_p1_up: str = "w"
        self.key_p1_left: str = "a"
        self.key_p1_down: str = "s"
        self.key_p1_right: str = "d"
        self.key_p1_a: str = "q"
        self.key_p1_b: str = "e"
        self.key_p1_c: str = "g"
        self.key_p1_d: str = "f"
        self.key_p2_up: str = "i"
        self.key_p2_left: str = "j"
        self.key_p2_down: str = "k"
        self.key_p2_right: str = "l"
        self.key_p2_a: str = "u"
        self.key_p2_b: str = "o"
        self.key_p2_c: str = "r"
        self.key_p2_d: str = "p"
        self.key_quit: str = "t"
        self.key_reset: str = "z"


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
                "description": "This is a template game!",
                "author": "Makerspace",
                "image_name": "Template.png",
                "url": "https://www.bodensee-gymnasium.de/"
            }
        ]


class UserConfig(nc.Config):

    def __init__(self, logger):

        super(UserConfig, self).__init__(f"{PATH_CONFIG}/user.json", logger)

        self.admins: list[int] = []
        self.banned: list[int] = []


class CacheConfig(nc.Config):

    def __init__(self, logger):

        super(CacheConfig, self).__init__(f"{PATH_CONFIG}/cache.json", logger)

        self.users: list[dict[str, Any]] = []
        self.players: list[dict[str, Any]] = []

        self.last_refresh: int = 0
