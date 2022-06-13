from logic.get_groups import get_box_coords_from_matrix_coords, get_coords_in_box
from logic.types import Dimensions, Coords, GroupName, Matrix
from typing import TypeVar

T = TypeVar("T")


def get_row_neighbours_coords(size: int, coords: Coords) -> list[Coords]:
    return [{"y": coords["y"], "x": x} for x in range(size) if x != coords["x"]]


def get_col_neighbours_coords(size: int, coords: Coords) -> list[Coords]:
    return [{"y": y, "x": coords["x"]} for y in range(size) if y != coords["y"]]


def get_box_neighbours_coords(box_dimensions: Dimensions, coords: Coords) -> list[Coords]:
    coords_in_box: list[Coords] = get_coords_in_box(box_dimensions, get_box_coords_from_matrix_coords(box_dimensions, coords))
    return [n_coords for n_coords in coords_in_box if n_coords["y"] != coords["y"] or n_coords["x"] != coords["x"]]


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


def get_box_neighbours(matrix: Matrix[T], box_dimensions: Dimensions, coords: Coords) -> list[T]:
    """
    Gets all cells in the given `coords` box, excluding the one
    at `coords`.
    """
    neighbour_coords: set[Coords] = {*get_box_neighbours_coords(box_dimensions, coords)}
    neighbours: list[T] = []
    for n_coord in neighbour_coords:
        neighbours.append(matrix[n_coord['y']][n_coord['x']])
    return neighbours


GROUP_NAME_MAP = {
    "row": get_row_neighbours_coords,
    "col": get_col_neighbours_coords
}


def get_group_neighbours_coords(name: GroupName, box_dimensions: Dimensions, coords: Coords) -> list[Coords]:
    if name != "box":
        return GROUP_NAME_MAP[name](box_dimensions["w"] * box_dimensions["h"], coords)
    return get_box_neighbours_coords(box_dimensions, coords)


def get_all_neighbours_coords(box_dimensions: Dimensions, coords: Coords) -> list[Coords]:
    neighbours_coords: list[Coords] = []
    group_names: list[GroupName] = ["box", "row", "col"]
    for name in group_names:
        group_coords = get_group_neighbours_coords(name, box_dimensions, coords)
        neighbours_coords += [coords for coords in group_coords if coords not in neighbours_coords]
    return neighbours_coords
