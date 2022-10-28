# Externe Bibliotheken
import pygame as pg


# CV zu Pygame
def cv_zu_pygame(bild):
    return pg.image.frombuffer(bild.tobytes(), (bild.shape[1], bild.shape[0]), "BGR")
