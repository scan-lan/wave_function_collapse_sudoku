from typing import TypeVar
from logic.coords import get_x, get_y
from logic.types import Dimensions, Coords, Matrix

T = TypeVar("T")


def get_coords_in_box(box_dimensions: Dimensions, box_coords: Coords) -> list[Coords]:
    """
    Fetches the coords of the items in the box at `box_coords`,
    for matrices with given `box_dimensions`.
    """
    y_offset = int(get_y(box_coords)) * box_dimensions["h"]
    x_offset = int(get_x(box_coords)) * box_dimensions["w"]
    return [
        f"{y_offset + y}, {x_offset + x}"
        for y in range(box_dimensions["h"])
        for x in range(box_dimensions["w"])
    ]


def get_row(matrix: Matrix[T], length: int, index: int) -> list[T]:
    """
    Fetches the items in the row at `index` for 2d array `matrix`
    with dimensions `box_dimensions`.
    """
    return [matrix[f"{index}, {x}"] for x in range(length)]


def get_col(matrix: Matrix[T], length: int, index: int) -> list[T]:
    """
    Fetches the items in the col at `index` for 2d array `matrix`
    with dimensions `box_dimensions`.
    """
    return [matrix[f"{y}, {index}"] for y in range(length)]


def get_box(
    matrix: Matrix[T], box_dimensions: Dimensions, box_coords: Coords
) -> list[T]:
    """
    Fetches the items in the box at `box_coords` for 2d array
    `matrix` with dimensions `box_dimensions`.
    """
    return [matrix[coords] for coords in get_coords_in_box(box_dimensions, box_coords)]


def get_row_from_coords(matrix: Matrix[T], length: int, coords: Coords) -> list[T]:
    """
    Fetches the items in the row containing `coords`.
    """
    return get_row(matrix, length, int(get_y(coords)))


def get_col_from_coords(matrix: Matrix[T], length: int, coords: Coords) -> list[T]:
    """
    Fetches the items in the column containing `coords`.
    """
    return get_col(matrix, length, int(get_x(coords)))


def get_box_from_coords(
    matrix: Matrix[T], box_dimensions: Dimensions, coords: Coords
) -> list[T]:
    """
    Fetches the items in the box containing `coords`.
    """
    box_coords = get_box_coords_from_matrix_coords(box_dimensions, coords)
    return [matrix[coords] for coords in get_coords_in_box(box_dimensions, box_coords)]


def get_box_coords_from_matrix_coords(
    box_dimensions: Dimensions, coords: Coords
) -> Coords:
    """
    Get coordinates of box containing `coords`.
    """
    y, x = int(get_y(coords)), int(get_x(coords))
    box_y, box_x = y // box_dimensions["h"], x // box_dimensions["w"]
    return f"{box_y}, {box_x}"
