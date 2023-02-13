# Standard
from __future__ import annotations
from typing import TYPE_CHECKING
import math
import threading as th

# External
from pyzbar.pyzbar import decode
import nikocraft as nc
import cv2
import pygame as pg
import numpy as np

# Local
from constants import *
from window import cv_utils

if TYPE_CHECKING:
    from window.window import Window


class LoginScene(nc.Scene):

    def __init__(self, window: Window, args):

        super(LoginScene, self).__init__(window, args)

        self.window: Window = window

        self.brightness: int = 180

        self.tick: int = 0
        self.timeout: int = 0

        self.mebis_qr_code: pg.Surface = pg.image.load(f"{PATH_IMAGE}/mebis.png")

        self.camera: cv2.VideoCapture | None = None
        self.camera_size: nc.Vec | None = None
        self.camera_frame: pg.Surface = pg.Surface((800, 460))
        self.camera_frame.fill(nc.RGB.BLACK)
        font = self.window.font.get("title", 80)
        text = font.render("LOADING", True, nc.RGB.WHITE)
        self.camera_frame.blit(text, (400 - text.get_width() / 2, 230 - text.get_height() / 2))

        self.input: list[str] = []
        self.invalid: list[str] = ["0025dc18-7172-4fb0-9020-10746cf7840b"]
        self.success: str = "04ea044a-a23a-4a1b-8bdf-2a329d393191"

    def render(self) -> None:

        # Login title
        font = self.window.font.get("title", 130)
        text = font.render("Login", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 80))

        # QR-Code scanner
        font = self.window.font.get("text", 30)
        text = font.render("QR-CODE SCANNER", True, nc.RGB.WHITE)
        self.screen.blit(text, (500 - text.get_width() / 2, 260))
        self.screen.blit(self.camera_frame, (100, 300))
        pg.draw.rect(self.screen, nc.RGB.WHITE, (100, 300, 800, 460), 3)

        # Register info box
        pg.draw.rect(self.screen, nc.RGB.BLACK, (1150, 250, 650, 600))
        pg.draw.rect(self.screen, nc.RGB.WHITE, (1150, 250, 650, 600), 3)

        # Mebis QR-Code
        pg.draw.rect(self.screen, nc.RGB.BLACK, (1000, 575, 250, 250))
        self.screen.blit(self.mebis_qr_code, (1010, 585))
        pg.draw.rect(self.screen, nc.RGB.WHITE, (1000, 575, 250, 250), 3)

        # Register title
        font = self.window.font.get("title", 90)
        text = font.render("Registrierung", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2, 260))

        # Register introduction
        font = self.window.font.get("text", 21)
        text = font.render("DU HAST NOCH KEINEN QR-CODE?", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2, 345))
        text = font.render("Kein Problem! Registriere", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2, 385))
        text = font.render("dich doch jetzt einfach.", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2, 420))
        text = font.render("So funktioniert es ...", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2, 455))
        pg.draw.line(self.screen, nc.RGB.WHITE, (1150, 495), (1799, 495), 3)

        # Register guide
        font = self.window.font.get("text", 16)
        link_font = self.window.font.get("text", 10)
        text = font.render("1. Scanne und öffne den QR-Code links.", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2, 515))
        text = link_font.render("https://lernplattform.mebis.bayern.de/mod/data/view?d=146523", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2, 540))
        text = font.render("2. Melde dich, wenn nötig, mit  ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 570))
        text = font.render("   deinem Mebis Account an.     ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 595))
        text = font.render("3. Drücke 'Eintrag hinzufügen'. ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 630))
        text = font.render("4. Gebe einen Spielernamen ein. ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 665))
        text = font.render("5. Stelle sicher, dass die      ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 700))
        text = font.render("   Einzelansicht ausgewählt ist.", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 725))
        text = font.render("6. Jetzt siehst du deinen       ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 760))
        text = font.render("   QR-Code, den du zum einloggen", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 785))
        text = font.render("   nutzen kannst! Glückwunsch!  ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 810))

        # Login prompt
        font = self.window.font.get("text", 35)
        height = math.sin(self.tick / 10) * 15 + 960
        text = font.render("Halte deinen QR-Code vor die Kamera!", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, height))

    def update(self) -> None:

        if self.camera is not None:

            # Read camera
            _, frame = self.camera.read()
            self.camera_size = nc.Vec(frame.shape[1], frame.shape[0])

            # Decode
            self.decode_qr(frame)

            # Transform
            pg_frame = cv_utils.cv_to_pygame(frame)
            pg_frame = pg.transform.flip(pg_frame, True, False)
            factor = 800 / pg_frame.get_width()
            pg_frame = pg.transform.scale_by(pg_frame, factor)

            # Render
            self.camera_frame.blit(pg_frame, (0, 230 - pg_frame.get_height() / 2))

        self.tick += self.dt

        if self.tick - self.timeout > 10000:
            self.window.change_scene("idle")

        # Debug screen
        self.window.debug_screen_left.append("")
        self.window.debug_screen_left.append(f"Tick: {self.tick:.1f}")
        self.window.debug_screen_left.append(f"Timeout: {self.tick - self.timeout:.1f}")
        self.window.debug_screen_left.append("")
        if self.camera_size is None:
            self.window.debug_screen_left.append(f"Camera: <off>")
        else:
            self.window.debug_screen_left.append(f"Camera: {self.camera_size.x} x {self.camera_size.y}")
        self.window.debug_screen_left.append("")
        self.window.debug_screen_left.append(f"QR Input:")
        for data in self.input:
            self.window.debug_screen_left.append(f"- {data}")
        self.window.debug_screen_left.append(f"QR Invalid:")
        for data in self.invalid:
            self.window.debug_screen_left.append(f"- {data}")
        self.window.debug_screen_left.append(f"QR Success: {self.success}")

    def event(self, event: pg.event.Event) -> None:

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                self.window.change_scene("menu")

    def quit(self) -> None:

        self.camera.release()

        self.logger.debug(self.input)
        self.logger.debug(self.invalid)

    def init(self) -> None:

        th.Thread(target=self.init_camera, name="Init camera").start()

    def init_camera(self) -> None:

        self.camera: cv2.VideoCapture = cv2.VideoCapture(0)

    def decode_qr(self, image: np.ndarray) -> None:

        gray_img = cv2.cvtColor(image, 0)

        codes = decode(gray_img)

        for code in codes:

            data = code.data.decode("utf-8")

            color = (0, 128, 255)
            if data not in self.input:
                self.input.append(data)
            if data == self.success:
                color = (0, 255, 0)
            if data in self.invalid:
                color = (0, 0, 255)

            points = code.polygon
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(image, [pts], True, color, 4)
