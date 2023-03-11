# External
import pygame as pg
import nikocraft as nc


def black_rect(surf: pg.Surface, x: int | float, y: int | float, width: int | float, height: int | float,
               alpha: int, border: bool = False, border_width: int = 3,
               border_color: nc.RGBColor = nc.RGB.WHITE) -> None:
    """Draw a black rectangle with a specific alpha value"""

    black = pg.Surface((width, height))
    black.set_alpha(alpha)

    surf.blit(black, (x, y))

    if border:
        pg.draw.rect(surf, border_color, (x, y, width, height), border_width)


def split_text(text: str, line_length: int) -> list[str]:

    lines: list[str] = []
    words: list[str] = text.split(" ")

    line: str = ""
    while words:

        if len(line) + len(words[0]) + 1 > line_length:
            lines.append(line)
            line = ""

        if len(words[0]) > line_length:
            line = words[0][:line_length]
            words[0] = words[0][line_length:]
            continue

        if line:
            line += " " + words[0]
        else:
            line = words[0]
        del words[0]

    lines.append(line)

    return lines


def draw_button(surf: pg.Surface, font: pg.font.Font, char: int,
                x: int | float, y: int | float, color: nc.RGBColor) -> None:

    width, height = font.size(" ")

    pg.draw.circle(surf, color, (x + width * char + width / 2 - 2, y + height / 2), width / 2)
    pg.draw.circle(surf, nc.RGB.GRAY75, (x + width * char + width / 2 - 2, y + height / 2),
                   width / 2 + 1, int(width / 10))
