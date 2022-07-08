import curses
import time
from typing import Optional

from logic.types import (
    Cell,
    CoefficientMatrix,
    Coords,
    Dimensions,
    OuterVisualiser,
    Visualiser,
)
from ui.align import centre_x, centre_y
from ui.coef_matrix_to_string import coef_matrix_to_string
from ui.print_matrix import print_matrix
from ui.types import Window


def make_visualiser(
    screen: Window,
) -> OuterVisualiser:
    show_time = 0.5
    speed = 1.0

    def visualiser_outer(
        coef_matrix: CoefficientMatrix,
        box_dimensions: Dimensions,
    ) -> Visualiser:
        first_coef_str = coef_matrix_to_string(
            coef_matrix,
            box_dimensions,
        )
        coef_height = len(first_coef_str.splitlines())
        coef_width = len(first_coef_str.splitlines()[0])
        start_y = centre_y(curses.LINES - 1, num_lines=coef_height)
        start_x = centre_x(curses.COLS - 1, str_len=coef_width)

        print_matrix(screen, coef_matrix, box_dimensions, start_y, start_x)
        curses.doupdate()

        def visualiser(
            coef_matrix: CoefficientMatrix,
            box_dimensions: Dimensions,
            new_collapse: Optional[Coords] = None,
            constraint_coords: Optional[Coords] = None,
            target_coords: Optional[Coords] = None,
            constraint_value: Optional[Cell] = None,
        ) -> bool:

            screen.erase()
            print_matrix(
                screen,
                coef_matrix,
                box_dimensions,
                start_y,
                start_x,
                new_collapse,
                constraint_coords,
                target_coords,
                constraint_value,
            )
            nonlocal speed
            nonlocal show_time

            k = ""
            start = time.time()
            while (time.time() - start) < (show_time / speed):
                try:
                    k = screen.getkey()
                    if k.lower() == "q":
                        return False
                    elif k == "KEY_UP":
                        speed += 0.25
                    elif k == "KEY_DOWN":
                        speed -= 0.25
                    elif k == "KEY_RESIZE":
                        curses.update_lines_cols()
                except curses.error:
                    pass
                curses.doupdate()
            return True

        return visualiser

    return visualiser_outer
