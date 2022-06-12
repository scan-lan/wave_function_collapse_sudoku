from util.is_collapsed import is_collapsed
from logic.get_groups import get_box_coords_from_matrix_coords
from typing import Callable, TypeVar

T = TypeVar("T")


def get_row_neighbours_coords(size: int, coords: Coords) -> list[Coords]:
    return [{"y": coords["y"], "x": x} for x in range(size) if x != coords["x"]]


def get_col_neighbours_coords(size: int, coords: Coords) -> list[Coords]:
    return [{"y": y, "x": coords["x"]} for y in range(size) if y != coords["y"]]


def get_box_neighbours_coords(box_dimensions: BoxDimensions, coords: Coords) -> list[Coords]:
    box_coords: Coords = get_box_coords_from_matrix_coords(box_dimensions, coords)
    width, height = box_dimensions["w"], box_dimensions["h"]
    offset_y = box_coords["y"] * height; offset_x = box_coords["x"] * width
    make_coords: Callable[[int, int], Coords] = lambda y, x: {"y" : offset_y + y, "x": offset_x + x}
    return [make_coords(y, x) for y in range(height) for x in range(width) if x != coords["x"] or y != coords["y"]]


def get_row_neighbours(matrix: Matrix[T], coords: Coords) -> list[T]:
    """
    Gets all cells in the given `coords` row, excluding the one at `coords`.
    """
    neighbour_coords = get_row_neighbours_coords(len(matrix), coords)
    return [matrix[n_coords["y"]][n_coords["x"]] for n_coords in neighbour_coords]


def get_col_neighbours(matrix: Matrix[T], coords: Coords) -> list[T]:
    """
    Gets all cells in the given `coords` column, excluding the one at `coords`.
    """
    return [matrix[n_coords["y"]][n_coords["x"]] for n_coords in get_col_neighbours_coords(len(matrix), coords)]


def get_box_neighbours(matrix: Matrix[T], box_dimensions: BoxDimensions, coords: Coords) -> list[T]:
    """
    Gets all cells in the given `coords` box, excluding the one
    at `coords`.
    """
    neighbour_coords: set[Coords] = set(get_box_neighbours_coords(box_dimensions, coords))
    neighbours: list[T] = []
    for n_coord in neighbour_coords:
        neighbours.append(matrix[n_coord['y']][n_coord['x']])
    return neighbours
