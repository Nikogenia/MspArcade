# External
import pygame as pg
import numpy as np


def cv_to_pygame(image: np.ndarray) -> pg.Surface:
    """Convert a OpenCV image to a pygame surface"""
    return pg.image.frombuffer(image.tobytes(), (image.shape[1], image.shape[0]), "BGR")
