# Standard
from __future__ import annotations
from typing import TYPE_CHECKING
import threading as th
import datetime as dt
import json
from logging import Logger

# External
import nikocraft as nc
import requests as rq

# Local
from constants import *
from user.user import User
from user.player import Player
from window.scenes.login import LoginScene
from window.scenes.idle import IdleScene
from window.scenes.loading import LoadingScene
if TYPE_CHECKING:
    from main import Main


class UserManager(th.Thread):

    def __init__(self, main: Main):

        super(UserManager, self).__init__(name="User")

        self.main: Main = main

        self.running: bool = True

        self.db_id: str = self.main.main_config.database_id
        self.token: str = self.main.main_config.database_auth_token

        self.users: list[User] = []
        self.players: list[Player] = []
        self.admins: list[int] = []
        self.banned: list[tuple[int, str]] = []

        self.last_update: float = 0
        self.fast_update: bool = False

        self.fields: tuple[int, int, int, int] | None = None

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

                if ((nc.time.epoch_time() - self.last_update > self.main.main_config.database_auto_update) or
                        (nc.time.epoch_time() - self.last_update > self.main.main_config.database_fast_update and self.fast_update)) and \
                        isinstance(self.main.window.scene, (IdleScene, LoadingScene)):
                    if self.main.main_config.account_time_refresh:
                        self.refresh_time()
                    self.fast_update = False
                    if self.fields is None:
                        self.get_fields()
                    data = self.get_entries()
                    self.online = data is not None
                    if self.online:
                        self.update(data)
                        if isinstance(self.main.window.scene, LoginScene):
                            self.main.window.scene.invalid.clear()
                    self.last_update = nc.time.epoch_time()
                    self.save()

                nc.time.wait(0.6)

            self.save()

        except Exception:
            self.main.handle_crash()

    def request(self, params: dict) -> dict | None:

        try:
            response = rq.post(self.main.main_config.database_url, params=params, timeout=2)
        except (rq.ConnectionError, rq.Timeout, TimeoutError) as e:
            self.logger.error("Failed to connect to database! Error message:")
            self.logger.error(e)
            return None

        self.logger.debug("Got response! Decode ...")

        if response.status_code != 200:
            self.logger.error(f"Got response with status code {response.status_code}!")
            return None

        if self.main.main_config.log_response:
            self.logger.debug(f"Response: {response.text}")

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

        if "warnings" in data and data["warnings"]:
            self.logger.warning(f"Warnings were given! Continue execution. {data['warnings']}")

        return data

    def get_entries(self) -> dict | None:

        self.logger.info(f"Start get entries request to database {self.db_id} ...")

        params = {
            "wstoken": self.token,
            "wsfunction": "mod_data_get_entries",
            "moodlewsrestformat": "json",
            "databaseid": self.db_id,
            "returncontents": 1,
            "perpage": 10000
        }

        data = self.request(params)
        if data is None:
            return None

        if "entries" not in data:
            self.logger.error(f"Failed to get entries! Missing in dictionary ...")
            return None

        self.logger.info("Received and decoded entries from database.")

        return data["entries"]

    def get_fields(self) -> bool:

        self.logger.info(f"Start get fields request to database {self.db_id} ...")

        params = {
            "wstoken": self.token,
            "wsfunction": "mod_data_get_fields",
            "moodlewsrestformat": "json",
            "databaseid": self.db_id,
        }

        data = self.request(params)
        if data is None:
            return False

        if "fields" not in data:
            self.logger.error(f"Failed to get fields! Missing in dictionary ...")
            return False

        if (not isinstance(data["fields"], list)) or len(data["fields"]) < 3:
            self.logger.error(f"Failed to get fields! Expected list with at least 3 fields ...")
            return False

        for field in data["fields"]:
            if "id" not in field or (not isinstance(field["id"], int)):
                self.logger.error(f"Failed to get fields! Fields with id as integer expected ...")
                return False

        self.fields = data["fields"][0]["id"], data["fields"][1]["id"], data["fields"][2]["id"], data["fields"][3]["id"]
        self.logger.debug(f"Parsed fields {self.fields[0]}, {self.fields[1]}, {self.fields[2]}, {self.fields[3]}.")

        self.logger.info("Received and decoded fields from database.")

        return True

    def update_time(self, player: Player) -> None:

        self.logger.info(f"Start update entry request to database {self.db_id} on entry {player.id} ...")

        params = {
            "wstoken": self.token,
            "wsfunction": "mod_data_update_entry",
            "moodlewsrestformat": "json",
            "entryid": player.id,
            "data[0][fieldid]": self.fields[0],
            "data[0][value]": f'"{player.auth_id}"',
            "data[1][fieldid]": self.fields[1],
            "data[1][value]": player.time,
            "data[2][fieldid]": self.fields[2],
            "data[2][value]": f'"{player.name}"',
            "data[3][fieldid]": self.fields[3],
            "data[3][value]": f'"{player.ratings}"'
        }

        data = self.request(params)
        if data is None:
            return None

        if "updated" not in data or not data["updated"]:
            self.logger.error(f"Failed to update entry!")
            return None

        self.logger.info("Entry successfully updated.")

    def refresh_time(self) -> None:
        last_refresh = dt.datetime.fromtimestamp(self.main.user_config.last_refresh)
        now = dt.datetime.now()
        if (last_refresh - dt.timedelta(last_refresh.weekday())).date() != (now - dt.timedelta(now.weekday())).date():

            self.main.user_config.last_refresh = int(now.timestamp())

            self.logger.info("Refresh time ...")

            for player in self.players:
                player.time = self.main.main_config.account_default_time
                if self.is_admin(player.user_id):
                    player.time = 86400

    def load(self) -> None:

        self.logger.info("Load users from config ...")

        self.users.clear()

        for data in self.main.cache_config.users:
            user = User.from_json(data, self.logger)
            if user is None:
                self.logger.warning("Failed to load a user!")
                continue
            self.logger.debug(f"User {user.id} ({user.name}) loaded.")
            self.users.append(user)

        self.logger.info(f"Successfully loaded {len(self.users)} users!")

        self.logger.info("Load players from config ...")

        self.players.clear()

        for data in self.main.cache_config.players:
            player = Player.from_json(data, self.logger, self.main.main_config.account_default_time)
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

        self.logger.info("Load admins from config ...")

        self.admins.clear()

        for admin in self.main.user_config.admins:
            if self.get_user(admin) is None:
                self.logger.warning(f"Failed to load admin {admin}! No user found!")
                continue
            self.admins.append(admin)
            for player in self.players:
                if player.user_id == admin:
                    player.time = 86400

        self.logger.info(f"Successfully loaded {len(self.admins)} admins!")

        self.logger.info("Load banned from config ...")

        self.banned.clear()

        for banned in self.main.user_config.banned:
            if (not isinstance(banned, list)) or len(banned) != 2:
                self.logger.warning(f"Failed to load banned {banned}! List of length 2 expected!")
                continue
            if (not isinstance(banned[0], int)) or (not isinstance(banned[1], str)):
                self.logger.warning(f"Failed to load banned {banned}! Type int and str expected!")
                continue
            if self.get_user(banned[0]) is None:
                self.logger.warning(f"Failed to load banned {banned}! No user found!")
                continue
            if banned[0] in self.admins:
                self.logger.warning(f"Failed to load banned {banned}! Cannot ban admin!")
                continue
            self.banned.append((banned[0], banned[1]))

        self.logger.info(f"Successfully loaded {len(self.banned)} banned!")

    def save(self) -> None:

        self.logger.info("Save users to config ...")

        self.main.cache_config.users.clear()

        for user in self.users:
            self.main.cache_config.users.append(user.json())

        self.logger.info("Save players to config ...")

        self.main.cache_config.players.clear()

        for player in self.players:
            self.main.cache_config.players.append(player.json())

        self.main.cache_config.save()

    def update(self, data: dict) -> None:

        self.logger.info("Update and merge data into database ...")

        deleted_players = []
        for player in self.players:
            deleted_players.append(player.id)

        for entry in data:

            new = False

            try:
                player = Player(
                    entry["userid"],
                    entry["id"],
                    entry["contents"][0]["content"],
                    entry["contents"][2]["content"],
                    entry["timecreated"],
                    None if entry["contents"][1]["content"] is None else int(entry["contents"][1]["content"]),
                    {} if entry["contents"][3]["content"] is None else json.loads(str(entry["contents"][3]["content"]).replace("'", '"'))
                )
                user = User(
                    entry["userid"],
                    entry["fullname"],
                    0
                )
            except (KeyError, ValueError, TypeError) as e:
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
                if player.time is None:
                    player.time = self.main.main_config.account_default_time
                    if self.is_admin(player.user_id):
                        player.time = 86400
                    if self.get_user(player.user_id) is not None and \
                            nc.time.epoch_time() - self.get_user(player.user_id).last_login < self.main.main_config.account_reset_timeout:
                        player.time = 0
                self.players.append(player)
                new = True
            else:
                self.get_player_by_id(player.id).name = player.name
                self.get_player_by_id(player.id).ratings = player.ratings | self.get_player_by_id(player.id).ratings
                deleted_players.remove(player.id)

            if (self.get_player_by_id(player.id).time != player.time) or new or \
                    (self.get_player_by_id(player.id).ratings != player.ratings):
                if self.fields is not None:
                    self.update_time(self.get_player_by_id(player.id))

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

    def is_admin(self, user_id: int) -> bool:
        return user_id in self.admins

    def is_banned(self, user_id: int) -> bool:
        return self.get_ban_reason(user_id) is not None

    def get_ban_reason(self, user_id: int) -> None | str:
        for banned in self.banned:
            if banned[0] == user_id:
                return banned[1]

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
                break

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
        self.main.cache_config.save()

        self.db_id = self.main.main_config.database_id
        self.token = self.main.main_config.database_auth_token

        self.last_update = 0
        self.fast_update = False

        self.fields = None

        self.current = ""

        self.main.cache_config.load()
        self.load()

        self.reload = False
