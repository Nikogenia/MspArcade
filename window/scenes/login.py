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
from window.draw_utils import black_rect, draw_button

if TYPE_CHECKING:
    from window.window import Window


class LoginScene(nc.Scene):

    def __init__(self, window: Window, args):

        super(LoginScene, self).__init__(window, args)

        self.window: Window = window

        self.brightness: int = 180

        self.tick: float = 0
        self.timeout: float = 0

        self.running: bool = True

        if "back" not in self.args:
            self.args["back"] = "menu"

        self.left_arrow: pg.Surface = pg.transform.smoothscale(
            pg.image.load(f"{PATH_IMAGE}/left_arrow.png").convert(), (60, 60))
        self.back_x: float = 0

        # Activity request data
        self.activity_request_tick: float = 0
        self.activity_request_tick_target: float = 0

        # Mebis QR Code image
        self.mebis_qr_code: pg.Surface = pg.image.load(f"{PATH_IMAGE}/mebis.png").convert()

        # Camera data
        self.camera: cv2.VideoCapture | None = None
        self.camera_size: nc.Vec | None = None
        self.camera_frame: pg.Surface = pg.Surface((800, 460))
        font = self.window.font.get("title", 80)
        text = font.render("LADE KAMERA", True, nc.RGB.WHITE)
        self.camera_update: float = 0
        self.camera_frame.blit(text, (400 - text.get_width() / 2, 230 - text.get_height() / 2))

        # QR code input
        self.input: list[str] = []
        self.invalid: list[str] = []
        self.success: str = ""

        # Scan status
        self.status: int = 0
        self.status_update: int = 0
        self.status_index: dict[int, tuple[nc.RGBColor, str]] = {
            0: (nc.RGB.GRAY70, "Suche QR-Code ..."),
            1: (nc.RGB.ORANGE, "Überprüfe gefundenen QR-Code ..."),
            2: (nc.RGB.RED1, "Ungültiger QR-Code! Login fehlgeschlagen!"),
            3: (nc.RGB.GREEN1, "Verifizierung erfolgreich! Willkommen!")
        }

    def render(self) -> None:

        # Back arrow
        size = math.sin(self.tick / 5) / 30 + 0.9
        left_arrow = pg.transform.smoothscale_by(self.left_arrow, size)
        self.screen.blit(left_arrow, (30 - left_arrow.get_width() / 2 + self.back_x, 40 - left_arrow.get_height() / 2))
        size = math.sin(self.tick / 5) / 50 + 0.9
        font = self.window.font.get("text", 45)
        text = pg.transform.smoothscale_by(font.render("Zurück", True, nc.RGB.WHITE), size)
        self.screen.blit(text, (190 - text.get_width() / 2 + self.back_x, 42 - text.get_height() / 2))

        # Login title
        font = self.window.font.get("title", 130)
        text = font.render("Login", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, 80))

        # QR-Code scanner
        font = self.window.font.get("title", 65)
        text = font.render("QR-CODE SCANNER", True, nc.RGB.WHITE)
        self.screen.blit(text, (500 - text.get_width() / 2, 260))
        self.screen.blit(self.camera_frame, (100, 310))
        pg.draw.rect(self.screen, nc.RGB.WHITE, (100, 310, 800, 460), 3)
        font = self.window.font.get("text", 22)
        text = font.render(self.status_index[self.status][1], True, self.status_index[self.status][0])
        black_rect(self.screen, 500 - text.get_width() / 2 - 13, 776, text.get_width() + 20, 37, 120, True, 1)
        self.screen.blit(text, (500 - text.get_width() / 2, 784))

        # Register info box
        black_rect(self.screen, 1150, 250, 650, 246, 70, True)
        black_rect(self.screen, 1150, 493, 650, 370, 220, True)

        # Mebis QR-Code
        pg.draw.rect(self.screen, nc.RGB.BLACK, (990, 580, 250, 250))
        self.screen.blit(self.mebis_qr_code, (1000, 590))
        pg.draw.rect(self.screen, nc.RGB.WHITE, (990, 580, 250, 250), 3)

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

        # Register guide
        font = self.window.font.get("text", 16)
        link_font = self.window.font.get("text", 10)
        info_font = self.window.font.get("text", 13)
        text = font.render("1. Scanne und öffne den QR-Code links.", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2, 515))
        text = link_font.render("https://lernplattform.mebis.bayern.de/mod/data/view?d=146523", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2, 540))
        text = font.render("2. Melde dich, wenn nötig, mit   ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 570))
        text = font.render("   deinem Mebis Account an.      ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 595))
        text = font.render("3. Drücke 'Eintrag hinzufügen'.  ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 630))
        text = font.render("4. Gebe einen Spielernamen ein   ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 665))
        text = font.render("   und bestätige mit 'Speichern'.", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 690))
        text = font.render("5. Jetzt siehst du deinen        ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 725))
        text = font.render("   QR-Code, den du zum einloggen ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 750))
        text = font.render("   nutzen kannst. Glückwunsch!   ", True, nc.RGB.WHITE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 775))
        text = info_font.render("Es kann unter Umständen einige Minuten  ", True, nc.RGB.ORANGE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 810))
        text = info_font.render("dauern, bis der QR-Code funktioniert!   ", True, nc.RGB.ORANGE)
        self.screen.blit(text, (1475 - text.get_width() / 2 + 50, 830))

        # Login prompt
        font = self.window.font.get("text", 35)
        height = math.sin(self.tick / 10) * 15 + 950
        text = font.render("Halte deinen QR-Code vor die Kamera!", True, nc.RGB.WHITE)
        self.screen.blit(text, ((self.width - text.get_width()) / 2, height))

        # Render activity request
        if self.activity_request_tick != self.activity_request_tick_target or self.activity_request_tick == 20:
            height = 310 * (self.activity_request_tick / 20) - 300
            black_rect(self.screen, self.width / 2 - 700, height, 1400, 230, 200, True, 3)
            font = self.window.font.get("title", 110)
            text = font.render("BIST DU NOCH DA?", True, nc.RGB.WHITE)
            self.screen.blit(text, ((self.width - text.get_width()) / 2, height + 30))
            font = self.window.font.get("text", 35)
            text = font.render("Bestätige deine Anwesenheit mit  !", True, nc.RGB.WHITE)
            self.screen.blit(text, ((self.width - text.get_width()) / 2, height + 140))
            draw_button(self.screen, font, 32, (self.width - text.get_width()) / 2, height + 140, ACTIVITY_BUTTON)

    def update(self) -> None:

        self.tick += self.dt

        if self.window.help_open:
            self.timeout = self.tick
            self.activity_request_tick = 0

        # Scene switching
        if self.tick - self.timeout > 2000:
            self.window.main.game_manager.current = None
            self.window.change_scene("idle", transition_duration=12, transition_pause=7)
        if self.status == 3:
            player = self.window.main.user_manager.get_player_by_auth_id(self.window.main.user_manager.current)
            if self.window.main.user_manager.is_banned(player.user_id):
                self.window.change_scene("banned", transition_duration=12, transition_pause=7)
            else:
                self.window.change_scene("overview", {"back": self.args["back"]},
                                         transition_duration=12, transition_pause=7)

        # Status reset
        if self.tick - self.status_update > 60 and self.status not in (0, 3):
            self.status_update = 0
            self.status = 0

        if self.back_x != 0:
            self.back_x -= self.dt * 3

        # Show activity request
        if self.tick - self.timeout > 1700:
            self.activity_request_tick_target = 20

        # Animate activity request
        if abs(self.activity_request_tick_target - self.activity_request_tick) < 1.5:
            self.activity_request_tick = self.activity_request_tick_target
        if self.activity_request_tick > self.activity_request_tick_target:
            self.activity_request_tick -= self.dt
        elif self.activity_request_tick < self.activity_request_tick_target:
            self.activity_request_tick += self.dt

        # Debug screen
        self.window.debug_screen_left.append("")
        self.window.debug_screen_left.append(f"Tick: {self.tick:.1f}")
        self.window.debug_screen_left.append(f"Timeout: {2000 - (self.tick - self.timeout):.1f}")
        self.window.debug_screen_left.append("")
        if self.camera_size is None:
            self.window.debug_screen_left.append(f"Camera: <off>")
        else:
            self.window.debug_screen_left.append(f"Camera: {self.camera_size.x} x {self.camera_size.y}")
            self.window.debug_screen_left.append(f"Camera Update: {self.camera_update * 1000:.2f} ms")
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

            # Reset timeout
            self.activity_request_tick_target = 0
            self.timeout = self.tick

            if event.key == pg.K_LEFT:
                self.window.change_scene(self.args["back"], transition_duration=12, transition_pause=7)
                self.back_x = -1
            if event.key == pg.K_r:
                self.window.main.game_manager.current = None
                self.window.change_scene("idle", transition_duration=12, transition_pause=7)

    def quit(self) -> None:

        self.running = False

    def init(self) -> None:

        th.Thread(target=self.camera_thread, name="Camera").start()

    def camera_thread(self) -> None:

        self.logger.info("Setup camera ...")
        self.camera: cv2.VideoCapture = cv2.VideoCapture(0)

        clock = pg.time.Clock()

        while self.running:

            # Tick and benchmark
            clock.tick(30)
            start = nc.time.bench_time()

            # Read camera
            _, frame = self.camera.read()
            if frame is None:
                continue
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

            # Benchmark
            end = nc.time.bench_time()
            self.camera_update = end - start

        self.logger.info("Release camera ...")
        self.camera.release()

    def decode_qr(self, image: np.ndarray) -> None:

        # Get gray scaled image
        gray_img = cv2.cvtColor(image, 0)

        # Decode QR codes
        codes = decode(gray_img)

        for code in codes:

            # Get content
            data = code.data.decode("utf-8")

            # New
            color = (0, 128, 255)
            if data not in self.input:
                self.input.append(data)

            # Success
            if data == self.success:
                color = (0, 255, 0)

            # Error
            elif data in self.invalid:
                if self.status != 3:
                    self.status = 2
                    self.status_update = self.tick
                color = (0, 0, 255)
            # New
            else:
                if self.status in (0, 1):
                    self.status = 1
                    self.status_update = self.tick

            # Draw border
            points = code.polygon
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(image, [pts], True, color, 4)
