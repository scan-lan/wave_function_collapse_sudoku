from typing import TypeVar
from logic.types import Dimensions, Coords, Matrix

T = TypeVar("T")


def get_coords_in_box(box_dimensions: Dimensions, box_coords: Coords) -> list[Coords]:
    """
    Fetches the coords of the items in the box at `box_coords`,
    for matrices with given `box_dimensions`.
    """
    y_offset = box_coords[0] * box_dimensions["h"]
    x_offset = box_coords[1] * box_dimensions["w"]
    return [(y_offset + y, x_offset + x) for y in range(box_dimensions["h"]) for x in range(box_dimensions["w"])]


def get_row(matrix: Matrix[T], index: int) -> list[T]:
    """
    Fetches the items in the row at `index` for 2d array `matrix`
    with dimensions `box_dimensions`.
    """
    return matrix[index]


def get_col(matrix: Matrix[T], index: int) -> list[T]:
    """
    Fetches the items in the col at `index` for 2d array `matrix`
    with dimensions `box_dimensions`.
    """
    return [row[index] for row in matrix]


def get_box(matrix: Matrix[T], box_dimensions: Dimensions, box_coords: Coords) -> list[T]:
    """
    Fetches the items in the box at `box_coords` for 2d array
    `matrix` with dimensions `box_dimensions`.
    """
    return [matrix[y][x] for y, x in get_coords_in_box(box_dimensions, box_coords)]


def get_row_from_coords(matrix: Matrix[T], coords: Coords) -> list[T]:
    """
    Fetches the items in the row containing `coords`.
    """
    return get_row(matrix, coords[0])


def get_col_from_coords(matrix: Matrix[T], coords: Coords) -> list[T]:
    """
    Fetches the items in the column containing `coords`.
    """
    return get_col(matrix, coords[1])


def get_box_from_coords(matrix: Matrix[T], box_dimensions: Dimensions, coords: Coords) -> list[T]:
    """
    Fetches the items in the box containing `coords`.
    """
    box_coords = get_box_coords_from_matrix_coords(box_dimensions, coords)
    return [matrix[y][x] for y, x in get_coords_in_box(box_dimensions, box_coords)]


def get_box_coords_from_matrix_coords(box_dimensions: Dimensions, coords: Coords) -> Coords:
    """
    Get coordinates of box containing `coords`.
    """
    y, x = coords
    box_y, box_x = y // box_dimensions['h'], x // box_dimensions['w']
    return (box_y, box_x)
