from random import shuffle, seed as set_seed
from typing import Optional
# from logic.Execeptions import ConstrainedCollapsedCellException
from logic.get_neighbours import get_all_neighbours_coords
from logic.types import (Cell, Coords, Grid, Dimensions, Coefficients,
                         CoefficientMatrix, GroupName, Weights)
from logic.get_groups import get_coords_in_box
from ui.print_coef_matrix import print_coef_matrix
from util.coords_converters import coords_to_tuple, make_coords


def update_weights(weights: Weights, value: Cell):
    weights[value] -= 1


def create_coef_matrix(size: int) -> CoefficientMatrix:
    """
    Creates a matrix (2d array) with `size` rows full of `size`
    copies of a set of every possible cell value.
    """
    coefficients: Coefficients = {str(n) for n in range(1, size + 1)}
    coefficient_matrix: CoefficientMatrix = []
    for _ in range(size):
        row = [coefficients.copy() for _ in range(size)]
        coefficient_matrix.append(row)

    return coefficient_matrix


def initialise_weights(size: int) -> Weights:
    return {str(n): size for n in range(1, size + 1)}


def get_free_coords(box_dimensions: Dimensions) -> list[Coords]:
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
    # if len(coef_matrix[y][x]) < 2:
    #     raise ConstrainedCollapsedCellException(coords, coef_matrix[y][x])
    coef_matrix[y][x].remove(constrained_coef)


def collapse(
        coef_matrix: CoefficientMatrix,
        coords: Coords,
        weights: Weights,
        value: Optional[Cell] = None,
        seed: Optional[int] = None) -> None:
    """
    Collapses coefficients at `coords` in coef_matrix to `value`.
    If `value` is not provided, choose random value from current
    coefs.
    """
    if seed is not None:
        set_seed(seed)
    y, x = coords_to_tuple(coords)
    if value and value in coef_matrix[y][x]:
        update_weights(weights, value)
        coef_matrix[y][x] = {value}
    else:
        options = [value for value, _ in sorted(weights.items(), key=lambda itm: itm[1]) if value in coef_matrix[y][x]]
        value = options.pop()
        update_weights(weights, value)
        coef_matrix[y][x] = {value}


def get_collapsed_value(coefs: Coefficients) -> Cell:
    """
    Get the value of a collapsed cell. If the cell isn't
    collapsed, i.e. it has more than one remaining member, throw
    an error.
    """
    if len(coefs) != 1:
        # raise Exception
        return ""
    return coefs.copy().pop()


def propagate(coef_matrix: CoefficientMatrix,
              box_dimensions: Dimensions,
              initial_coords: Coords,
              weights: Weights,
              skip: Optional[list[GroupName]] = None,
              visualise: bool = False,
              speed: float = 1) -> None:
    """
    Takes the coordinates of a collapsed cell `initial_coords`
    and propagates the consequences of that collapse onto its
    neighbours. In sudoku's case, this is the cells in the same
    row, column and box as `initial_coords`. If any cells
    collapse as a consequence of this propagation, the function
    recurses with the newly-collapsed cell's coords.
    """
    coords_stack: list[Coords] = [initial_coords]
    while coords_stack:
        current_coords = coords_stack.pop()
        y, x = coords_to_tuple(current_coords)
        constraint = get_collapsed_value(coef_matrix[y][x])
        for neighbour_coords in get_all_neighbours_coords(box_dimensions, current_coords, skip=skip):
            neighbour_y, neighbour_x = coords_to_tuple(neighbour_coords)
            if visualise:
                print_coef_matrix(
                    coef_matrix,
                    box_dimensions,
                    constraint_coords=current_coords,
                    target_coords=neighbour_coords,
                    constraint_value=constraint,
                    sleep=(1 / speed))
            if constraint in coef_matrix[neighbour_y][neighbour_x]:
                constrain(coef_matrix, neighbour_coords, constraint)
                if len(coef_matrix[neighbour_y][neighbour_x]) == 1:
                    update_weights(weights, get_collapsed_value(coef_matrix[neighbour_y][neighbour_x]))
                    if visualise:
                        print_coef_matrix(coef_matrix, box_dimensions, sleep=(2 / speed), new_collapse=neighbour_coords)
                    coords_stack.append(neighbour_coords)


def get_random_values(grid_size: int) -> list[Cell]:
    """
    Creates a list from 1 - `grid_size + 1` and randomises the
    order.
    """
    values = [str(val) for val in range(1, grid_size + 1)]
    shuffle(values)
    return values


def get_all_collapsed(coef_matrix: CoefficientMatrix) -> Grid:
    """
    Creates a matrix of collapsed cells in `coef_matrix`. If a cell isn't
    collapsed, " " goes in its place.
    """
    return [[" " if len(coefs) != 1 else get_collapsed_value(coefs) for coefs in row] for row in coef_matrix]


def fill_free_boxes(
        coef_matrix: CoefficientMatrix,
        box_dimensions: Dimensions,
        weights: Weights,
        seed: Optional[int] = None,
        visualise: bool = False,
        speed: float = 1) -> None:
    """
    Fills the cells in `coef_matrix` which constrain each other
    at the box level only.
    """
    if seed is not None:
        set_seed(seed)
    free_cell_coords = get_free_coords(box_dimensions)
    box_size = box_dimensions["h"] * box_dimensions["w"]
    values = get_random_values(box_size)
    for coords in free_cell_coords:
        if len(values) == 0:
            values = get_random_values(box_size)
        collapse(coef_matrix, coords, weights, values.pop())
        if visualise:
            print_coef_matrix(coef_matrix, box_dimensions, sleep=(2 / speed), new_collapse=coords)
        propagate(coef_matrix, box_dimensions, coords, weights, skip=["box"], visualise=visualise, speed=speed)


def get_uncollapsed(coef_matrix: CoefficientMatrix) -> Coords | None:
    """
    Get the coords of an uncollapsed cell. Returns None if all
    cells are collapsed.
    """
    for y, row in enumerate(coef_matrix):
        for x, coefs in enumerate(row):
            if len(coefs) > 1:
                return make_coords(y, x)
    return None


def iterate(
        coef_matrix: CoefficientMatrix,
        box_dimensions: Dimensions,
        weights: Weights,
        seed: Optional[int] = None,
        visualise: bool = False,
        speed: float = 1) -> None:
    """
    Repeat the collapse -> propagate loop until there are no
    uncollapsed cells left.
    """
    uncollapsed_coords = get_uncollapsed(coef_matrix)
    while uncollapsed_coords:
        collapse(coef_matrix, uncollapsed_coords, weights, seed=seed)
        if visualise:
            print_coef_matrix(coef_matrix, box_dimensions, sleep=(2 / speed), new_collapse=uncollapsed_coords)
        propagate(coef_matrix, box_dimensions, uncollapsed_coords, weights, visualise=visualise, speed=speed)
        uncollapsed_coords = get_uncollapsed(coef_matrix)


def create_grid(box_dimensions: Dimensions = {"w": 3, "h": 3},
                difficulty: int = 1,
                seed: Optional[int] = None,
                passed_weights: Optional[Weights] = None,
                visualise: bool = False,
                speed: float = 1) -> tuple[Grid, CoefficientMatrix]:
    """
    Create a valid sudoku grid.
    """
    if seed is not None:
        set_seed(seed)
    grid_size = box_dimensions["w"] * box_dimensions["h"]
    coef_matrix = create_coef_matrix(grid_size)
    if visualise:
        print_coef_matrix(coef_matrix, box_dimensions, sleep=2 / speed)
    weights = passed_weights if passed_weights is not None else initialise_weights(grid_size)

    fill_free_boxes(coef_matrix, box_dimensions, weights, visualise=visualise, speed=2 * speed)
    iterate(coef_matrix, box_dimensions, weights, visualise=visualise, speed=1 * speed)

    return get_all_collapsed(coef_matrix), coef_matrix
