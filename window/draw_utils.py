# External
import pygame as pg
import nikocraft as nc


def black_rect(surf: pg.Surface, x: int | float, y: int | float, width: int | float, height: int | float, alpha: int,
               border: bool = False, border_width: int = 3, border_color: nc.RGBColor = nc.RGB.WHITE) -> None:
    """Draw a black rectangle with a specific alpha value"""

    black = pg.Surface((width, height))
    black.set_alpha(alpha)

    surf.blit(black, (x, y))

    if border:
        pg.draw.rect(surf, border_color, (x, y, width, height), border_width)
