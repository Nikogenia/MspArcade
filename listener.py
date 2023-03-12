# Standard
from __future__ import annotations
from typing import TYPE_CHECKING
from multiprocessing.connection import Listener as ConnectionListener
from multiprocessing import AuthenticationError
import threading as th
from logging import Logger

# External
import nikocraft as nc

# Local
if TYPE_CHECKING:
    from main import Main


class Listener(th.Thread):

    def __init__(self, main: Main):

        super(Listener, self).__init__(name="Listener")

        self.main: Main = main

        self.running: bool = True

        self.port: int = self.main.main_config.listener_port
        self.key: str = self.main.main_config.listener_key

        if self.key == "DefaultKey":
            self.logger.warning("Using default key for listening! Please change for safety!")

        self.conn_listener: ConnectionListener | None = None

        self.reload: bool = False

    # PROPERTIES

    @property
    def logger(self) -> Logger:
        return self.main.logger

    # METHODS

    def run(self) -> None:

        try:

            self.logger.info(f"Listening on port {self.port} ...")
            self.conn_listener = ConnectionListener(("localhost", self.port),
                                                    authkey=self.key.encode("utf-8"))

            while self.running:

                if self.reload:
                    self.do_reload()

                try:
                    conn = self.conn_listener.accept()
                except AuthenticationError:
                    self.logger.info("Connection failed! Invalid key!")
                    continue
                except OSError:
                    continue

                self.logger.debug("New connection opened.")

                self.handle_conn(conn)

                conn.close()

            self.logger.info(f"Close listener ...")
            self.conn_listener.close()

        except Exception:
            self.main.handle_crash()

    def handle_conn(self, conn):

        task = conn.recv()

        if not isinstance(task, dict):
            self.logger.info("Connection failed! Dictionary expected!")
            conn.send((1, "Dictionary expected!"))
            return

        if "type" not in task:
            self.logger.info("Connection failed! Missing type!")
            conn.send((2, "Missing type!"))
            return

        match task["type"]:

            case "quit":
                self.logger.info("Connection successful! Quit ...")
                conn.send((0, ""))
                self.main.running = False

            case "restart":
                self.logger.info("Connection successful! Restart ...")
                conn.send((0, ""))
                self.main.running = False
                self.main.exit_code = 2

            case "reload":
                self.logger.info("Connection successful! Reload ...")
                conn.send((0, ""))
                self.main.window.change_scene("loading", transition_duration=0, transition_pause=0)
                nc.time.wait(0.1)
                self.main.main_config.load()
                self.main.game_config.load()
                self.main.game_manager.reload = True
                self.main.user_manager.reload = True
                self.reload = True

            case "debug_on":
                self.logger.info("Connection successful! Activate debug screen ...")
                conn.send((0, ""))
                self.main.window.debug_screen_active = True

            case "debug_off":
                self.logger.info("Connection successful! Deactivate debug screen ...")
                conn.send((0, ""))
                self.main.window.debug_screen_active = False

            case "debug_toggle":
                self.logger.info("Connection successful! Toggle debug screen ...")
                conn.send((0, ""))
                self.main.window.debug_screen_active = not self.main.window.debug_screen_active

            case _:
                self.logger.info("Connection failed! Invalid task!")
                conn.send((3, "Invalid task!"))

    def do_reload(self):

        self.port: int = self.main.main_config.listener_port
        self.key: str = self.main.main_config.listener_key

        if self.key == "DefaultKey":
            self.logger.warning("Using default key for listening! Please change for safety!")

        self.logger.info(f"Close listener ...")
        self.conn_listener.close()

        self.logger.info(f"Listening on port {self.port} ...")
        self.conn_listener = ConnectionListener(("localhost", self.port),
                                                authkey=self.key.encode("utf-8"))

        self.reload = False
