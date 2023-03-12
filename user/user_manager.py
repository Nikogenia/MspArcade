# Standard
from __future__ import annotations
from typing import TYPE_CHECKING
import threading as th
from logging import Logger

# External
import nikocraft as nc
import requests as rq

# Local
from constants import *
from user.user import User
from user.player import Player
from window.scenes.login import LoginScene
if TYPE_CHECKING:
    from main import Main


class UserManager(th.Thread):

    def __init__(self, main: Main):

        super(UserManager, self).__init__(name="User")

        self.main: Main = main

        self.running: bool = True

        self.db_id: str = self.main.main_config.database_id
        self.token: str = self.main.main_config.auth_token

        self.users: list[User] = []
        self.players: list[Player] = []

        self.last_update: float = 0
        self.fast_update: bool = False

        self.online: bool = True

        self.current: str = ""

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
                    self.do_reload()

                if isinstance(self.main.window.scene, LoginScene):
                    self.handle_login()

                if (nc.time.epoch_time() - self.last_update > AUTO_UPDATE) or \
                        (nc.time.epoch_time() - self.last_update > FAST_UPDATE and self.fast_update):
                    self.fast_update = False
                    data = self.get_entries()
                    self.online = data is not None
                    if self.online:
                        self.update(data)
                        if isinstance(self.main.window.scene, LoginScene):
                            self.main.window.scene.invalid.clear()
                    self.last_update = nc.time.epoch_time()

                nc.time.wait(0.5)

            self.save()

        except Exception:
            self.main.handle_crash()

    def get_entries(self) -> dict | None:

        self.logger.info(f"Start get entry request to database {self.db_id} ...")

        params = {
            "wstoken": self.token,
            "wsfunction": "mod_data_get_entries",
            "moodlewsrestformat": "json",
            "databaseid": self.db_id,
            "returncontents": 1
        }

        try:
            response = rq.post(DATABASE_URL, params=params)
        except rq.ConnectionError as e:
            self.logger.error("Failed to connect to database! Error message:")
            self.logger.error(e)
            return None

        self.logger.debug("Got response! Decode ...")

        if response.status_code != 200:
            self.logger.error(f"Got response with status code {response.status_code}!")
            return None

        try:
            data = response.json()
        except rq.JSONDecodeError as e:
            self.logger.error("Failed to parse JSON! Invalid response! Error message:")
            self.logger.error(e)
            return None

        if "exception" in data:
            self.logger.error(f"Exception occurred! Type: '{data['exception']}' Error code: '{data['errorcode']}'")
            self.logger.error(f"Error message: {data['message']}")
            return None

        if "entries" not in data:
            self.logger.error(f"Failed to get entries! Missing in dictionary ...")
            return None

        self.logger.info("Received and decoded entries from database.")

        return data["entries"]

    def update_time(self, entry: int, value: int) -> None:

        self.logger.info(f"Start update entry request to database {self.db_id} ...")

        params = {
            "wstoken": self.token,
            "wsfunction": "mod_data_update_entry",
            "moodlewsrestformat": "json",
        }

        try:
            response = rq.post(DATABASE_URL, params=params)
        except rq.ConnectionError as e:
            self.logger.error("Failed to connect to database! Error message:")
            self.logger.error(e)
            return None

        self.logger.debug("Got response! Decode ...")

        if response.status_code != 200:
            self.logger.error(f"Got response with status code {response.status_code}!")
            return None

        try:
            data = response.json()
        except rq.JSONDecodeError as e:
            self.logger.error("Failed to parse JSON! Invalid response! Error message:")
            self.logger.error(e)
            return None

        if "exception" in data:
            self.logger.error(f"Exception occurred! Type: '{data['exception']}' Error code: '{data['errorcode']}'")
            self.logger.error(f"Error message: {data['message']}")
            return None

        if "updated" not in data or not data["updated"]:
            self.logger.error(f"Failed to get entries! Missing in dictionary ...")
            return None

        self.logger.info("Received and decoded entries from database.")

        return data["entries"]

    def load(self) -> None:

        self.logger.info("Load users from config ...")

        self.users.clear()

        for data in self.main.user_config.users:
            user = User.from_json(data, self.logger)
            if user is None:
                self.logger.warning("Failed to load a user!")
                continue
            self.logger.debug(f"User {user.id} ({user.name}) loaded.")
            self.users.append(user)

        self.logger.info(f"Successfully loaded {len(self.users)} users!")

        self.logger.info("Load players from config ...")

        self.players.clear()

        for data in self.main.user_config.players:
            player = Player.from_json(data, self.logger)
            if player is None:
                self.logger.warning("Failed to load a player!")
                continue
            if self.get_user(player.user_id) is None:
                self.logger.warning(f"Failed to load player {player.id} ({player.name})! " +
                                    f"No matched user for {player.user_id}!")
                continue
            self.logger.debug(f"Player {player.id} [{player.auth_id}] ({player.name}) loaded.")
            self.players.append(player)

        self.logger.info(f"Successfully loaded {len(self.players)} players!")

    def save(self) -> None:

        self.logger.info("Save users to config ...")

        self.main.user_config.users.clear()

        for user in self.users:
            self.main.user_config.users.append(user.json())

        self.logger.info("Save players to config ...")

        self.main.user_config.players.clear()

        for player in self.players:
            self.main.user_config.players.append(player.json())

    def update(self, data: dict) -> None:

        self.logger.info("Update and merge data into database ...")

        deleted_players = []
        for player in self.players:
            deleted_players.append(player.id)

        for entry in data:

            try:
                player = Player(
                    entry["userid"],
                    entry["id"],
                    entry["contents"][0]["content"],
                    entry["contents"][2]["content"],
                    entry["timecreated"],
                    entry["contents"][1]["content"],
                    {}
                )
                user = User(
                    entry["userid"],
                    entry["fullname"],
                    0
                )
            except KeyError as e:
                self.logger.warning(f"Error on parsing data: {e}")
                continue

            self.logger.debug(f"Parsed player {player.id} [{player.auth_id}] ({player.name}).")
            self.logger.debug(f"Parsed user {user.id} ({user.name}).")

            if self.get_user(user.id) is None:
                self.logger.debug(f"New user {user.id} ({user.name}) added.")
                self.users.append(user)
            else:
                self.get_user(user.id).name = user.name

            if self.get_player_by_id(player.id) is None:
                self.logger.debug(f"New player {player.id} [{player.auth_id}] ({player.name}) added.")
                player.time = DEFAULT_TIME
                if self.get_user(player.user_id) is not None and \
                        nc.time.epoch_time() - self.get_user(player.user_id).last_login < TIME_RESET_TIMEOUT:
                    player.time = 0
                self.players.append(player)
            else:
                self.get_player_by_id(player.id).name = player.name
                deleted_players.remove(player.id)

        for player_id in deleted_players:
            self.players.remove(self.get_player_by_id(player_id))

    def get_player_by_id(self, player_id: int) -> Player:
        for player in self.players:
            if player.id == player_id:
                return player

    def get_player_by_auth_id(self, player_auth_id: str) -> Player:
        for player in self.players:
            if player.auth_id == player_auth_id:
                return player

    def get_user(self, user_id: int) -> User:
        for user in self.users:
            if user.id == user_id:
                return user

    def handle_login(self) -> None:

        scene: LoginScene = self.main.window.scene

        if scene.status == 3:
            return

        for value in scene.input:

            if self.get_player_by_auth_id(value) is not None:
                self.current = value
                self.get_user(self.get_player_by_auth_id(value).user_id).last_login = int(nc.time.epoch_time())
                scene.success = value
                scene.status = 3
                scene.status_update = scene.tick
                continue

            self.fast_update = True

            if value in scene.invalid:
                continue

            scene.invalid.append(value)
            scene.status = 2
            scene.status_update = scene.tick

        scene.input.clear()

    def get_ratings(self, game_id: int) -> tuple[float, int]:

        ratings = []

        for player in self.players:
            if str(game_id) in player.ratings:
                ratings.append(player.ratings[str(game_id)])

        if len(ratings) == 0:
            return 0, 0

        return sum(ratings) / len(ratings), len(ratings)

    def get_rating(self, player_auth_id: str, game_id: int) -> int:

        player = self.get_player_by_auth_id(player_auth_id)

        if player is None or str(game_id) not in player.ratings:
            return 0

        return player.ratings[str(game_id)]

    def set_rating(self, player_auth_id: str, game_id: int, value: int) -> None:

        player = self.get_player_by_auth_id(player_auth_id)

        if player is None:
            return

        player.ratings[str(game_id)] = value

    def do_reload(self):

        self.save()
        self.main.user_config.save()

        self.db_id = self.main.main_config.database_id
        self.token = self.main.main_config.auth_token

        self.last_update = 0
        self.fast_update = False

        self.current = ""

        self.main.user_config.load()
        self.load()

        self.reload = False
