from random import shuffle
from typing import Optional
from logic.get_neighbours import get_all_neighbours_coords
from logic.get_constraints import get_constraints_by_group
from logic.types import Cell, Coords, Grid, BoxDimensions, Coefficients, CoefficientMatrix, GroupName
from logic.get_groups import get_coords_in_box
from util.coords_converters import coords_to_tuple

GROUP_NAMES: frozenset[GroupName] = frozenset({"row", "col", "box"})
# rows = [[(j + (floor(i / 3)) + (i % 3) * 3) % 9 + 1 for j in range(9)] for i in range(9)]

def create_coefficient_matrix(size: int) -> CoefficientMatrix:
    coefficients: Coefficients = {str(n) for n in range(1, size+1)}
    coefficient_matrix: CoefficientMatrix = []
    for _ in range(size):
        row = [coefficients.copy() for _ in range(size)]
        coefficient_matrix.append(row)

    return coefficient_matrix


def get_free_cell_coords(box_dimensions: BoxDimensions) -> list[Coords]:
    num_free_boxes = min(box_dimensions.values())
    return [coord for i in range(num_free_boxes) for coord in get_coords_in_box(box_dimensions, {"y": i, "x": i})]


def check_compatibility(coef_matrix: CoefficientMatrix, box_dimensions: BoxDimensions, coords: Coords, value: Cell) -> tuple[bool, list[GroupName]]:
    compatible_groups = set(GROUP_NAMES)
    group_constraints = get_constraints_by_group(coef_matrix, box_dimensions, coords)
    for group, constraints in group_constraints.items():
        if value in constraints:
            compatible_groups.remove(group)
    return len(compatible_groups) == len(GROUP_NAMES), list(compatible_groups)


def constrain(coef_matrix: CoefficientMatrix, coords: Coords, constrained_coef: Cell) -> None:
    y, x = coords_to_tuple(coords)
    coef_matrix[y][x].remove(constrained_coef)


def collapse(coef_matrix: CoefficientMatrix, coords: Coords, value: Optional[Cell]=None) -> None:
    y, x = coords_to_tuple(coords)
    if value:
        coef_matrix[y][x] = {value}
    else:
        options = coef_matrix[y][x].copy()
        coef_matrix[y][x] = {options.pop()}


def get_collapsed_value(coefs: Coefficients) -> Cell:
    return coefs.copy().pop()


def propagate(coef_matrix: CoefficientMatrix, box_dimensions: BoxDimensions, initial_coords: Coords) -> None:
    y, x = coords_to_tuple(initial_coords)
    constraint = get_collapsed_value(coef_matrix[y][x])
    for current_coords in get_all_neighbours_coords(box_dimensions, initial_coords):
        cur_y, cur_x = coords_to_tuple(current_coords)
        if constraint in coef_matrix[cur_y][cur_x]:
            constrain(coef_matrix, current_coords, constraint)
            if len(coef_matrix[cur_y][cur_x]) == 1:
                propagate(coef_matrix, box_dimensions, current_coords)


def get_random_values(grid_size: int) -> list[Cell]:
    values = [str(val) for val in range(1, grid_size+1)]
    shuffle(values)
    return values


def fill_free_boxes(coef_matrix: CoefficientMatrix, box_dimensions: BoxDimensions) -> None:
    free_cell_coords = get_free_cell_coords(box_dimensions)
    values = get_random_values(box_dimensions["h"] * box_dimensions["w"])
    for coords in free_cell_coords:
        if len(values) == 0:
            values = get_random_values(box_dimensions["h"] * box_dimensions["w"])
        collapse(coef_matrix, coords, values.pop())
        propagate(coef_matrix, box_dimensions, coords)


def get_collapsed(coef_matrix: CoefficientMatrix) -> Grid:
    return [[" " if len(coefs) != 1 else coefs.pop() for coefs in row] for row in coef_matrix]

def create_grid(box_dimensions: BoxDimensions = {"w": 3, "h": 3}, difficulty: int = 1) -> tuple[Grid, CoefficientMatrix]:
    grid_size = box_dimensions["w"] * box_dimensions["h"]
    coefficient_matrix = create_coefficient_matrix(grid_size)
    fill_free_boxes(coefficient_matrix, box_dimensions)
    return get_collapsed(coefficient_matrix), coefficient_matrix
