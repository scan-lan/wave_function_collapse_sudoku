import curses
from typing import Final, Optional
from logic.types import Cell, CoefficientMatrix, Coords, Dimensions

from ui.types import Window

DEFAULT: Final[int] = 1
TARGET: Final[int] = 2
NEW_COLLAPSE: Final[int] = 3
COLLAPSED: Final[int] = 4
CONSTRAINT: Final[int] = 5
CONSTRAINED: Final[int] = 6


def print_matrix(
    screen: Window,
    coef_matrix: CoefficientMatrix,
    box_dimensions: Dimensions,
    start_y: int = 0,
    start_x: int = 0,
    new_collapse: Optional[Coords] = None,
    constraint_coords: Optional[Coords] = None,
    target_coords: Optional[Coords] = None,
    constraint_value: Optional[Cell] = None,
) -> None:
    box_width, box_height = box_dimensions["w"], box_dimensions["h"]
    size = box_width * box_height
    sorted_coefs: list[Cell] = sorted([str(n) for n in range(1, size + 1)], key=int)
    coef_width = len(str(size))
    cell_width = coef_width * box_height
    cell_height = box_width
    box_str_width = (cell_width + 1) * box_width

    screen.erase()

    for y, row in enumerate(coef_matrix):
        screen_y = start_y + y * (cell_height + 1)
        for x, coefs in enumerate(row):
            screen_x = start_x + x * (box_width + coef_width)
            colour = DEFAULT
            if new_collapse and (y, x) == new_collapse:
                colour = NEW_COLLAPSE
            elif target_coords and (y, x) == target_coords:
                colour = TARGET
            elif len(coefs) == 1:
                colour = COLLAPSED
            for offset, coef in enumerate(sorted_coefs):
                y_offset = offset // box_height
                x_offset = offset % box_width
                cell_val = coef if coef in coefs else " "
                if (
                    constraint_value
                    and (y, x) == target_coords
                    and cell_val == constraint_value
                ):
                    screen.addstr(
                        screen_y + y_offset,
                        screen_x + x_offset,
                        f"{cell_val:>{coef_width}}",
                        curses.color_pair(CONSTRAINED),
                    )
                elif (
                    constraint_coords
                    and (y, x) == constraint_coords
                    and cell_val != " "
                ):
                    screen.addstr(
                        screen_y + y_offset,
                        screen_x + x_offset,
                        f"{cell_val:>{coef_width}}",
                        curses.color_pair(CONSTRAINT),
                    )
                else:
                    screen.addstr(
                        screen_y + y_offset,
                        screen_x + x_offset,
                        f"{cell_val:>{coef_width}}",
                        curses.color_pair(colour),
                    )

            if (x + 1) % box_width == 0 and x != size - 1:
                screen.vline(
                    screen_y,
                    screen_x + coef_width * box_width,
                    curses.ACS_VLINE,
                    box_height + (0 if (y + 1) % box_height == 0 else 1),
                )

        if (y + 1) % box_height == 0 and y != size - 1:
            for i in range(box_height):
                screen.hline(
                    screen_y + cell_height,
                    start_x + i * box_str_width,
                    curses.ACS_HLINE,
                    box_str_width - 1,
                )
                if i != 0:
                    screen.addch(
                        screen_y + cell_height,
                        start_x + box_str_width * i - 1,
                        curses.ACS_PLUS,
                    )

    screen.noutrefresh()
