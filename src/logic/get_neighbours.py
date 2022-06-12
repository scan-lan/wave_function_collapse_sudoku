from util.is_collapsed import is_collapsed
from logic.get_groups import get_box_coords_from_matrix_coords
from logic.types import BoxDimensions, Coefficients, Coords, GroupConstraints, GroupName, Matrix, CoefficientMatrix
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
    neighbour_coords: set[Coords] = {*get_box_neighbours_coords(box_dimensions, coords)}
    neighbours: list[T] = []
    for n_coord in neighbour_coords:
        neighbours.append(matrix[n_coord['y']][n_coord['x']])
    return neighbours


def get_row_constraints(matrix: CoefficientMatrix, coords: Coords) -> Coefficients:
    """
    Adds the values of all collapsed coefficients in the row
    containing cell `coords` to a set.
    """
    constraints: Coefficients = set()
    for coefs in get_row_neighbours(matrix, coords):
        if is_collapsed(coefs):
            constraints.add(coefs.pop())
    return constraints


def get_col_constraints(matrix: CoefficientMatrix, coords: Coords) -> Coefficients:
    """
    Adds the values of all collapsed coefficients in the column
    containing cell `coords` to a set.
    """
    constraints: Coefficients = set()
    for coefs in get_col_neighbours(matrix, coords):
        if is_collapsed(coefs):
            constraints.add(coefs.pop())
    return constraints


def get_box_constraints(matrix: CoefficientMatrix, box_dimensions: BoxDimensions, coords: Coords) -> Coefficients:
    """
    Adds the values of all collapsed coefficients in the box
    containing cell `coords` to a set.
    """
    constraints: Coefficients = set()
    for coefs in get_box_neighbours(matrix, box_dimensions, coords):
        if is_collapsed(coefs):
            constraints.add(coefs.pop())
    return constraints


def get_all_constraints(matrix: CoefficientMatrix, box_dimensions: BoxDimensions, coords: Coords) -> Coefficients:
    """
    Creates a set of all impossible values for the cell at the
    given `coords`.
    """
    return set([
        *get_row_constraints(matrix, coords),
        *get_col_constraints(matrix, coords),
        *get_box_constraints(matrix, box_dimensions, coords)
    ])


def get_constraints_by_group(matrix: CoefficientMatrix, box_dimensions: BoxDimensions, coords: Coords) -> GroupConstraints:
    """
    Creates a dictionary of impossible values for each sudoku "group" the cell at the given `coords` is in.
    """
    constraints: GroupConstraints = {
        "row": get_row_constraints(matrix, coords),
        "col": get_col_constraints(matrix, coords),
        "box": get_box_constraints(matrix, box_dimensions, coords)
    }
    return constraints


GROUP_NAME_MAP = {
    "row": get_row_neighbours_coords,
    "col": get_col_neighbours_coords
}


def get_group_neighbours_coords(name: GroupName, box_dimensions: BoxDimensions, coords: Coords) -> list[Coords]:
    if name != "box":
        return GROUP_NAME_MAP[name](box_dimensions["w"] * box_dimensions["h"], coords)
    return get_box_neighbours_coords(box_dimensions, coords)
