from logic.coords import get_x, get_y
from logic.get_groups import get_box_coords_from_matrix_coords, get_coords_in_box
from logic.types import Collapsed, Dimensions, Coords, GroupName, Matrix
from typing import Optional, TypeVar

T = TypeVar("T")
GROUP_NAMES: tuple[GroupName, GroupName, GroupName] = ("box", "row", "col")


def get_row_neighbours_coords(size: int, coords: Coords) -> list[Coords]:
    return [f"{get_y(coords)}, {x}" for x in range(size) if str(x) != get_x(coords)]


def get_col_neighbours_coords(size: int, coords: Coords) -> list[Coords]:
    return [f"{y}, {get_x(coords)}" for y in range(size) if str(y) != get_y(coords)]


def get_box_neighbours_coords(
    box_dimensions: Dimensions, coords: Coords
) -> list[Coords]:
    coords_in_box: list[Coords] = get_coords_in_box(
        box_dimensions, get_box_coords_from_matrix_coords(box_dimensions, coords)
    )
    return [b_coords for b_coords in coords_in_box if b_coords != coords]


def get_row_neighbours(matrix: Matrix[T], coords: Coords) -> list[T]:
    """
    Gets all cells in the given `coords` row, excluding the one at `coords`.
    """
    neighbour_coords = get_row_neighbours_coords(len(matrix), coords)
    return [matrix[n_coords] for n_coords in neighbour_coords]


def get_col_neighbours(matrix: Matrix[T], coords: Coords) -> list[T]:
    """
    Gets all cells in the given `coords` column, excluding the one at `coords`.
    """
    return [
        matrix[n_coords] for n_coords in get_col_neighbours_coords(len(matrix), coords)
    ]


def get_box_neighbours(
    matrix: Matrix[T], box_dimensions: Dimensions, coords: Coords
) -> list[T]:
    """
    Gets all cells in the given `coords` box, excluding the one
    at `coords`.
    """
    neighbour_coords: set[Coords] = {*get_box_neighbours_coords(box_dimensions, coords)}
    neighbours: list[T] = [matrix[n_coords] for n_coords in neighbour_coords]
    return neighbours


GROUP_NAME_MAP = {"row": get_row_neighbours_coords, "col": get_col_neighbours_coords}


def get_group_neighbours_coords(
    name: GroupName, box_dimensions: Dimensions, coords: Coords
) -> list[Coords]:
    if name != "box":
        return GROUP_NAME_MAP[name](box_dimensions["w"] * box_dimensions["h"], coords)
    return get_box_neighbours_coords(box_dimensions, coords)


def get_all_neighbours_coords(
    box_dimensions: Dimensions,
    coords: Coords,
    collapsed: Optional[Collapsed] = None,
    skip: Optional[list[GroupName]] = None,
) -> list[Coords]:
    neighbours_coords: set[Coords] = set()
    group_names: set[GroupName] = {*GROUP_NAMES}
    if skip:
        group_names.difference_update(skip)
    for name in group_names:
        group_coords = get_group_neighbours_coords(name, box_dimensions, coords)
        neighbours_coords.update(group_coords)
    if collapsed:
        return sorted(list(neighbours_coords.difference(collapsed)))
    return sorted(list(neighbours_coords))
