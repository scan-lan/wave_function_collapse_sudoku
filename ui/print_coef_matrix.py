import time
from colorama import Back, Fore
from typing import Callable, Optional
from logic.types import Coefficients, Coords, Dimensions, Cell, CoefficientMatrix

FORE_BG_RESET = Fore.RESET + Back.RESET
TARGET_COLOUR: Callable[[str], str] = (
    lambda s: Back.LIGHTMAGENTA_EX + Fore.BLACK + s + FORE_BG_RESET
)
NEW_COLLAPSE_COLOUR: Callable[[str], str] = (
    lambda s: Back.LIGHTGREEN_EX + Fore.BLACK + s + FORE_BG_RESET
)
COLLAPSED_COLOUR: Callable[[str], str] = lambda s: Fore.GREEN + s + Fore.RESET
CONSTRAINT_COLOUR: Callable[[str], str] = (
    lambda s: Back.YELLOW + Fore.BLACK + s + FORE_BG_RESET
)
CONSTRAINED_COLOUR: Callable[[str], str] = (
    lambda s: Back.RED + Fore.WHITE + s + Back.LIGHTMAGENTA_EX + Fore.BLACK
)


def pad_cell(cell: Cell, cell_width: int) -> str:
    return (" " * (cell_width - len(cell))) + cell


def format_box_part(
    coefs: Coefficients,
    box_part: list[Cell],
    cell_width: int,
    new_collapse: bool = False,
    constraint: bool = False,
    target: bool = False,
    constraint_value: Optional[Cell] = None,
) -> str:
    part_str = ""
    for cell in box_part:
        if cell in coefs:
            if constraint:
                cell = CONSTRAINT_COLOUR(cell)
            elif constraint_value is not None and cell == constraint_value:
                cell = CONSTRAINED_COLOUR(cell)
            elif new_collapse:
                cell = NEW_COLLAPSE_COLOUR(cell)
            elif len(coefs) == 1:
                cell = COLLAPSED_COLOUR(cell)
            part_str += pad_cell(cell, cell_width)
        else:
            part_str += f"{Back.RED} {Back.RESET}" if len(coefs) == 0 else " "
    if target:
        part_str = TARGET_COLOUR(part_str)
    return part_str


def print_coef_matrix(
    matrix: CoefficientMatrix,
    box_dimensions: Dimensions,
    new_collapse: Optional[Coords] = None,
    constraint_coords: Optional[Coords] = None,
    target_coords: Optional[Coords] = None,
    constraint_value: Optional[Cell] = None,
    sleep: float = 0,
) -> None:
    matrix_str = ""
    width, height = box_dimensions["w"], box_dimensions["h"]
    size = width * height
    sorted_coefs: list[Cell] = sorted([str(n) for n in range(1, size + 1)], key=int)
    cell_width = len(str(size))
    grid_line_coef = (width * cell_width + 1) * width * height + (height - 1) * 2

    print(f"{'*' * grid_line_coef}\n")
    for y, row in enumerate(matrix):
        for start, stop in enumerate(range(1, height + 1)):
            string_row: list[str] = []
            for x, coefs in enumerate(row):
                box_part = sorted_coefs[start * width : width * stop]
                padded_coefs = format_box_part(coefs, box_part, cell_width)
                if (
                    constraint_coords
                    and x == constraint_coords[1]
                    and y == constraint_coords[0]
                ):
                    padded_coefs = format_box_part(
                        coefs, box_part, cell_width, constraint=True
                    )
                elif (
                    target_coords
                    and constraint_value
                    and x == target_coords[1]
                    and y == target_coords[0]
                ):
                    padded_coefs = format_box_part(
                        coefs,
                        box_part,
                        cell_width,
                        target=True,
                        constraint_value=constraint_value,
                    )
                elif new_collapse and x == new_collapse[1] and y == new_collapse[0]:
                    padded_coefs = format_box_part(
                        coefs, box_part, cell_width, new_collapse=True
                    )
                string_row.append(
                    padded_coefs
                    + (" | " if x % width == width - 1 and x != len(row) - 1 else " ")
                )
            matrix_str += "".join(string_row) + "\n"
        matrix_str += (
            "—" if y % height == height - 1 and y != size - 1 else " "
        ) * grid_line_coef + "\n"

    print(f"{matrix_str}{'*' * grid_line_coef}\n")
    if sleep:
        time.sleep(sleep)
