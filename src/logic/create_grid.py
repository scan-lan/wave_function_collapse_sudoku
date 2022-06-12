from random import shuffle
from typing import Optional
from logic.get_neighbours import get_constraints_by_group, get_group_neighbours_coords
from logic.types import Cell, Coords, Grid, BoxDimensions, Coefficients, CoefficientMatrix, GroupName
from ui.print_coef_matrix import print_coef_matrix
from logic.get_groups import get_box_coords

# rows = [[(j + (floor(i / 3)) + (i % 3) * 3) % 9 + 1 for j in range(9)] for i in range(9)]

def create_coefficient_matrix(size: int) -> CoefficientMatrix:
    coefficients: Coefficients = set([str(n) for n in range(1, size+1)])
    coefficient_matrix: CoefficientMatrix = []
    for _ in range(size):
        row = [coefficients.copy() for _ in range(size)]
        coefficient_matrix.append(row)

    return coefficient_matrix


def get_free_cell_coords(box_dimensions: BoxDimensions) -> list[Coords]:
    num_free_boxes = min(box_dimensions.values())
    return [coord for i in range(num_free_boxes) for coord in get_box_coords(box_dimensions, {"y": i, "x": i})]


def check_compatibility(coef_matrix: CoefficientMatrix, box_dimensions: BoxDimensions, coords: Coords, value: Cell) -> tuple[bool, list[GroupName]]:
    incompatible_groups: list[GroupNames] = []
    group_constraints = get_constraints_by_group(coef_matrix, box_dimensions, coords)
    for group, constraints in group_constraints.items():
        if value in constraints:
            incompatible_groups.append(group)
    return len(incompatible_groups) == 0, incompatible_groups


def constrain(coef_matrix: CoefficientMatrix, coords: Coords, forbidden: Cell) -> CoefficientMatrix:
    coef_matrix[coords["y"]][coords["x"]].remove(forbidden)
    return coef_matrix


def collapse(coef_matrix: CoefficientMatrix, coords: Coords, value: Optional[Cell]) -> CoefficientMatrix:
    if value:
        coef_matrix[coords["y"]][coords["x"]] = set([value])
    else:
        options = list(coef_matrix[coords["y"]][coords["x"]])
        coef_matrix[coords["y"]][coords["x"]] = set([options.pop()])

    return coef_matrix


def propagate(coef_matrix: CoefficientMatrix, box_dimensions: BoxDimensions, initial_coords: Coords) -> CoefficientMatrix:
    stack: list[Coords] = [initial_coords]
    while len(stack) > 0:
        coords = stack.pop()
        y, x = initial_coords["y"], initial_coords["x"]
        current_options = coef_matrix[y][x]
        if len(current_options) == 1:
            continue
        if len(current_options) < 1:
            print("No options, error state")
            raise Exception
        for option in current_options:
            # TODO: Fix this, the group(s) NOT returned should be added to the stack
            compatible, incompatible_groups = check_compatibility(coef_matrix, box_dimensions, coords, option)
            if not compatible:
                coef_matrix = constrain(coef_matrix, coords, option)
                for group in incompatible_groups:
                    stack += get_group_neighbours_coords(group, box_dimensions, coords)
                coef_matrix = propagate(coef_matrix, box_dimensions, stack.pop())
    return coef_matrix


def get_random_values(grid_size: int) -> list[Cell]:
    values = [str(val) for val in range(1, grid_size+1)]
    shuffle(values)
    return values


def fill_free_boxes(coef_matrix: CoefficientMatrix, box_dimensions: BoxDimensions) -> CoefficientMatrix:
    free_cell_coords = get_free_cell_coords(box_dimensions)
    values = get_random_values(box_dimensions["h"] * box_dimensions["w"])
    for coords in free_cell_coords:
        if len(values) == 0:
            values = get_random_values(box_dimensions["h"] * box_dimensions["w"])
        coef_matrix = collapse(coef_matrix, coords, values.pop())
        coef_matrix = propagate(coef_matrix, box_dimensions, coords)
    return coef_matrix


def get_collapsed(coef_matrix: CoefficientMatrix) -> Grid:
    return [[" " if len(coefs) != 1 else coefs.pop() for coefs in row] for row in coef_matrix]

def create_grid(box_dimensions: BoxDimensions = {"w": 3, "h": 3}, difficulty: int = 1) -> Grid:
    grid_size = box_dimensions["w"] * box_dimensions["h"]
    # solution_grid = [["0"] * grid_size for _ in range(grid_size)]
    coefficient_matrix = create_coefficient_matrix(grid_size)
    print_coef_matrix(coefficient_matrix, box_dimensions)
    coefficient_matrix = fill_free_boxes(coefficient_matrix, box_dimensions)
    print_coef_matrix(coefficient_matrix, box_dimensions)
    return get_collapsed(coefficient_matrix)
