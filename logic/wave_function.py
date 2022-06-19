from random import seed as set_seed
from typing import Optional

from logic.Exceptions import ConstrainedCollapsedCellException, GetValueFromUncollapsedCellException
from logic.get_neighbours import get_all_neighbours_coords
from logic.types import (Cell, Coefficients, Collapsed, Coords, Dimensions,
                         CoefficientMatrix, GroupName, Weights)
from logic.weights import update_weights
from ui.print_coef_matrix import print_coef_matrix


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


def constrain(coef_matrix: CoefficientMatrix, coords: Coords, constrained_coef: Cell) -> None:
    """
    Removes `constrained_coef` from coefs at `coords` in
    `coef_matrix`.
    """
    y, x = coords
    if len(coef_matrix[y][x]) < 2:
        raise ConstrainedCollapsedCellException(coords, coef_matrix[y][x])
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
    y, x = coords
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
        raise GetValueFromUncollapsedCellException(coefs)
    return coefs.copy().pop()


def propagate(coef_matrix: CoefficientMatrix,
              box_dimensions: Dimensions,
              initial_coords: Coords,
              weights: Weights,
              collapsed: Collapsed,
              skip: Optional[list[GroupName]] = None,
              visualise: bool = False,
              speed: float = 1) -> None:
    """
    Takes the coordinates of a collapsed cell `initial_coords`
    and propagates the consequences of that collapse onto its
    neighbours. In sudoku's case, this is the cells in the same
    row, column and box as `initial_coords`. If any cells
    collapse as a consequence of this propagation, their
    coordinates are added to a stack and the consequences are
    propagated afterwards; likewise if this results in a
    collapsed cell, and so on.
    """
    coords_stack: list[Coords] = [initial_coords]
    while coords_stack:
        current_coords = coords_stack.pop()
        y, x = current_coords
        constraint = get_collapsed_value(coef_matrix[y][x])
        for neighbour_coords in get_all_neighbours_coords(box_dimensions, current_coords, collapsed, skip=skip):
            neighbour_y, neighbour_x = neighbour_coords
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
                    collapsed.add(neighbour_coords)
                    update_weights(weights, get_collapsed_value(coef_matrix[neighbour_y][neighbour_x]))
                    if visualise:
                        print_coef_matrix(coef_matrix, box_dimensions, sleep=(2 / speed), new_collapse=neighbour_coords)
                    coords_stack.append(neighbour_coords)
