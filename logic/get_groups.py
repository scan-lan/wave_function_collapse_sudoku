from typing import TypeVar
from logic.types import BoxDimensions, Coords, Matrix
from util.coords_converters import coords_to_tuple

T = TypeVar("T")


def get_coords_in_box(box_dimensions: BoxDimensions, box_coords: Coords) -> list[Coords]:
    """
    Fetches the coords of the items in the box at `box_coords`,
    for matrices with given `box_dimensions`.
    """
    coords: list[Coords] = []
    box_offset_y = box_coords["y"] * box_dimensions["h"]
    box_offset_x = box_coords["x"] * box_dimensions["w"]
    for y in range(box_dimensions["h"]):
        for x in range(box_dimensions["w"]):
            coords.append({"y" : box_offset_y + y, "x": box_offset_x + x})
    return coords


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


def get_box(matrix: Matrix[T], box_dimensions: BoxDimensions, box_coords: Coords) -> list[T]:
    """
    Fetches the items in the box at `box_coords` for 2d array
    `matrix` with dimensions `box_dimensions`.
    """
    coords = [coords_to_tuple(b_coords) for b_coords in get_coords_in_box(box_dimensions, box_coords)]
    return [matrix[y][x] for y, x in coords]


def get_row_from_coords(matrix: Matrix[T], coords: Coords) -> list[T]:
    """
    Fetches the items in the row containing `coords`.
    """
    return get_row(matrix, coords["y"])


def get_col_from_coords(matrix: Matrix[T], coords: Coords) -> list[T]:
    """
    Fetches the items in the column containing `coords`.
    """
    return get_col(matrix, coords["x"])


def get_box_from_coords(matrix: Matrix[T], box_dimensions: BoxDimensions, coords: Coords) -> list[T]:
    """
    Fetches the items in the box containing `coords`.
    """
    box_coords = get_box_coords_from_matrix_coords(box_dimensions, coords)
    matrix_coords = get_coords_in_box(box_dimensions, box_coords)
    return [matrix[m_coords["y"]][m_coords["x"]] for m_coords in matrix_coords]


def get_box_coords_from_matrix_coords(box_dimensions: BoxDimensions, coords: Coords) -> Coords:
    """
    Get coordinates of box containing `coords`.
    """
    y, x = coords_to_tuple(coords)
    box_y, box_x = y // box_dimensions['h'], x // box_dimensions['w']
    return {'y': box_y, 'x': box_x}
