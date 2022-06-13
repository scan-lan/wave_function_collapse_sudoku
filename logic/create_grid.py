from random import shuffle
from typing import Optional
from logic.get_neighbours import get_all_neighbours_coords
from logic.types import Cell, Coords, Grid, BoxDimensions, Coefficients, CoefficientMatrix, GroupName
from logic.get_groups import get_coords_in_box
from util.coords_converters import coords_to_tuple

GROUP_NAMES: frozenset[GroupName] = frozenset({"row", "col", "box"})
# rows = [[(j + (floor(i / 3)) + (i % 3) * 3) % 9 + 1 for j in range(9)] for i in range(9)]

def create_coefficient_matrix(size: int) -> CoefficientMatrix:
    """
    Creates a matrix (2d array) with `size` rows full of `size`
    copies of a set of every possible cell value.
    """
    coefficients: Coefficients = {str(n) for n in range(1, size+1)}
    coefficient_matrix: CoefficientMatrix = []
    for _ in range(size):
        row = [coefficients.copy() for _ in range(size)]
        coefficient_matrix.append(row)

    return coefficient_matrix


def get_free_cell_coords(box_dimensions: BoxDimensions) -> list[Coords]:
    """
    Gets a list of the coords in the free boxes for a matrix with
    box dimensions of `box_dimensions`. These are all the coords
    which don't constrain each other beyond the box-level.
    """
    num_free_boxes = min(box_dimensions.values())
    return [coord for i in range(num_free_boxes) for coord in get_coords_in_box(box_dimensions, {"y": i, "x": i})]


def constrain(coef_matrix: CoefficientMatrix, coords: Coords, constrained_coef: Cell) -> None:
    """
    Removes `constrained_coef` from coefs at `coords` in
    `coef_matrix`.
    """
    y, x = coords_to_tuple(coords)
    coef_matrix[y][x].remove(constrained_coef)


def collapse(coef_matrix: CoefficientMatrix, coords: Coords, value: Optional[Cell]=None) -> None:
    """
    Collapses coefficients at `coords` in coef_matrix to `value`.
    If `value` is not provided, choose random value from current
    coefs.
    """
    y, x = coords_to_tuple(coords)
    if value and value in coef_matrix[y][x]:
        coef_matrix[y][x] = {value}
    else:
        options = coef_matrix[y][x].copy()
        coef_matrix[y][x] = {options.pop()}


def get_collapsed_value(coefs: Coefficients) -> Cell:
    """
    Get the value of a collapsed cell. If the cell isn't
    collapsed, i.e. it has more than one remaining member, throw
    an error.
    """
    if len(coefs) != 1:
        raise Exception
    return coefs.copy().pop()


def propagate(coef_matrix: CoefficientMatrix, box_dimensions: BoxDimensions, initial_coords: Coords) -> None:
    """
    Takes the coordinates of a collapsed cell `initial_coords`
    and propagates the consequences of that collapse onto its
    neighbours. In sudoku's case, this is the cells in the same
    row, column and box as `initial_coords`. If any cells
    collapse as a consequence of this propagation, the function
    recurses with the newly-collapsed cell's coords.
    """
    y, x = coords_to_tuple(initial_coords)
    constraint = get_collapsed_value(coef_matrix[y][x])
    for current_coords in get_all_neighbours_coords(box_dimensions, initial_coords):
        cur_y, cur_x = coords_to_tuple(current_coords)
        if constraint in coef_matrix[cur_y][cur_x]:
            constrain(coef_matrix, current_coords, constraint)
            if len(coef_matrix[cur_y][cur_x]) == 1:
                propagate(coef_matrix, box_dimensions, current_coords)


def get_random_values(grid_size: int) -> list[Cell]:
    """
    Creates a list from 1 - `grid_size + 1` and randomises the
    order.
    """
    values = [str(val) for val in range(1, grid_size+1)]
    shuffle(values)
    return values


def get_all_collapsed(coef_matrix: CoefficientMatrix) -> Grid:
    """
    Creates a matrix of collapsed cells in `coef_matrix`. If a cell isn't
    collapsed, " " goes in its place.
    """
    return [[" " if len(coefs) != 1 else get_collapsed_value(coefs) for coefs in row] for row in coef_matrix]


def fill_free_boxes(coef_matrix: CoefficientMatrix, box_dimensions: BoxDimensions) -> None:
    """
    Fills the cells in `coef_matrix` which constrain each other
    at the box level only.
    """
    free_cell_coords = get_free_cell_coords(box_dimensions)
    box_size = box_dimensions["h"] * box_dimensions["w"]
    values = get_random_values(box_size)
    for coords in free_cell_coords:
        if len(values) == 0:
            values = get_random_values(box_size)
        collapse(coef_matrix, coords, values.pop())
        propagate(coef_matrix, box_dimensions, coords)


def create_grid(box_dimensions: BoxDimensions = {"w": 3, "h": 3}, difficulty: int = 1) -> tuple[Grid, CoefficientMatrix]:
    """
    Create a valid sudoku grid.
    """
    grid_size = box_dimensions["w"] * box_dimensions["h"]
    coefficient_matrix = create_coefficient_matrix(grid_size)
    fill_free_boxes(coefficient_matrix, box_dimensions)
    return get_all_collapsed(coefficient_matrix), coefficient_matrix
