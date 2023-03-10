# Standard
from __future__ import annotations
from typing import TYPE_CHECKING
from multiprocessing.connection import Listener as ConnectionListener
from multiprocessing import AuthenticationError
import threading as th
from logging import Logger

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
            return

        if "type" not in task:
            self.logger.info("Connection failed! Missing type!")
            return

        match task["type"]:

            case "quit":
                self.logger.info("Connection successful! Quit ...")
                self.main.running = False

            case "restart":
                self.logger.info("Connection successful! Restart ...")
                self.main.running = False
                self.main.exit_code = 2

            case _:
                self.logger.info("Connection failed! Invalid task!")
