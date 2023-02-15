# External
import pygame as pg
import nikocraft as nc


def black_rect(surf: pg.Surface, x: int | float, y: int | float, width: int | float, height: int | float, alpha: int, white_border: bool = False, border_width: int = 3) -> None:
    """Draw a black rectangle with a specific alpha value"""

    black = pg.Surface((width, height))
    black.set_alpha(alpha)

    surf.blit(black, (x, y))

    if white_border:
        pg.draw.rect(surf, nc.RGB.WHITE, (x, y, width, height), border_width)
