from copy import deepcopy
from random import seed as set_seed
from typing import Optional

from logic.exceptions import (
    CollapseEmptyCellException,
    ConstrainedCollapsedCellException,
    GetValueFromUncollapsedCellException,
)
from logic.get_neighbours import get_all_neighbours_coords
from logic.types import (
    Cell,
    Coefficients,
    Collapsed,
    Coords,
    Dimensions,
    CoefficientMatrix,
    GroupName,
    History,
    Weights,
)
from logic.weights import update_weights
from ui.print_coef_matrix import print_coef_matrix


def create_coef_matrix(size: int) -> CoefficientMatrix:
    """
    Creates a matrix (2d array) with `size` rows full of `size`
    copies of a set of every possible cell value.
    """
    coefficients: Coefficients = {str(n) for n in range(1, size + 1)}
    coefficient_matrix: CoefficientMatrix = {
        f"{y}, {x}": coefficients.copy() for y in range(size) for x in range(size)
    }

    return coefficient_matrix


def constrain(
    coef_matrix: CoefficientMatrix, coords: Coords, constrained_coef: Cell
) -> None:
    """
    Removes `constrained_coef` from coefs at `coords` in
    `coef_matrix`.
    """
    if len(coef_matrix[coords]) < 2:
        raise ConstrainedCollapsedCellException(coords, coef_matrix[coords])
    coef_matrix[coords].remove(constrained_coef)


def collapse(
    coef_matrix: CoefficientMatrix,
    coords: Coords,
    weights: Weights,
    collapsed: Collapsed,
    history: Optional[History] = None,
    value: Optional[Cell] = None,
    seed: Optional[int] = None,
) -> None:
    """
    Collapses coefficients at `coords` in coef_matrix to `value`.
    If `value` is not provided, choose random value from current
    coefs.
    """
    if seed is not None:
        set_seed(seed)
    if len(coef_matrix[coords]) < 1:
        raise CollapseEmptyCellException(coords)
    if value is None or value not in coef_matrix[coords]:
        options = [
            value
            for value, _ in sorted(weights.items(), key=lambda itm: itm[1])
            if value in coef_matrix[coords]
        ]
        value = options.pop()
        if history is not None:
            history_matrix = deepcopy(coef_matrix)
            history_matrix[coords].remove(value)
            history.append((collapsed.copy(), weights.copy(), history_matrix))
    update_weights(weights, value)
    coef_matrix[coords] = {value}
    collapsed.add(coords)


def get_collapsed_value(coefs: Coefficients) -> Cell:
    """
    Get the value of a collapsed cell.  If the cell isn't
    collapsed, i.e. it has more than one remaining member, throw
    an error.
    """
    if len(coefs) != 1:
        raise GetValueFromUncollapsedCellException(coefs)
    return coefs.copy().pop()


def iterative_propagate(
    coef_matrix: CoefficientMatrix,
    box_dimensions: Dimensions,
    initial_coords: Coords,
    weights: Weights,
    collapsed: Collapsed,
    skip: Optional[list[GroupName]] = None,
    visualise: bool = False,
    speed: float = 1,
) -> None:
    """
    Takes the coordinates of a collapsed cell `initial_coords`
    and propagates the consequences of that collapse onto its
    neighbours.  In sudoku's case, this is the cells in the same
    row, column and box as `initial_coords`.  If any cells
    collapse as a consequence of this propagation, their
    coordinates are added to a stack and the consequences are
    propagated afterwards; likewise if this results in a
    collapsed cell, and so on.
    """
    coords_stack: list[Coords] = [initial_coords]
    while coords_stack:
        current_coords = coords_stack.pop()
        constraint = get_collapsed_value(coef_matrix[current_coords])
        for neighbour_coords in get_all_neighbours_coords(
            box_dimensions, current_coords, collapsed, skip=skip
        ):
            if visualise:
                print_coef_matrix(
                    coef_matrix,
                    box_dimensions,
                    constraint_coords=current_coords,
                    target_coords=neighbour_coords,
                    constraint_value=constraint,
                    sleep=(1 / speed),
                )
            if constraint in coef_matrix[neighbour_coords]:
                constrain(coef_matrix, neighbour_coords, constraint)
                if len(coef_matrix[neighbour_coords]) == 1:
                    collapsed.add(neighbour_coords)
                    update_weights(
                        weights,
                        get_collapsed_value(coef_matrix[neighbour_coords]),
                    )
                    if visualise:
                        print_coef_matrix(
                            coef_matrix,
                            box_dimensions,
                            sleep=(2 / speed),
                            new_collapse=neighbour_coords,
                        )
                    coords_stack.append(neighbour_coords)


def propagate(
    coef_matrix: CoefficientMatrix,
    box_dimensions: Dimensions,
    initial_coords: Coords,
    weights: Weights,
    collapsed: Collapsed,
    skip: Optional[list[GroupName]] = None,
    visualise: bool = False,
    speed: float = 1,
) -> None:
    """
    Takes the coordinates of a collapsed cell `initial_coords`
    and propagates the consequences of that collapse onto its
    neighbours.  In sudoku's case, this is the cells in the same
    row, column and box as `initial_coords`.  If any cells
    collapse as a consequence of this propagation, the function
    recurses with the newly-collapsed cell's coords.
    """
    constraint = get_collapsed_value(coef_matrix[initial_coords])
    for current_coords in get_all_neighbours_coords(
        box_dimensions, initial_coords, collapsed, skip=skip
    ):
        if visualise:
            print_coef_matrix(
                coef_matrix,
                box_dimensions,
                constraint_coords=initial_coords,
                target_coords=current_coords,
                constraint_value=constraint,
                sleep=(1 / speed),
            )
        if constraint in coef_matrix[current_coords]:
            constrain(coef_matrix, current_coords, constraint)
            if len(coef_matrix[current_coords]) == 1:
                collapsed.add(current_coords)
                update_weights(
                    weights, get_collapsed_value(coef_matrix[current_coords])
                )
                if visualise:
                    print_coef_matrix(
                        coef_matrix,
                        box_dimensions,
                        sleep=(2 / speed),
                        new_collapse=current_coords,
                    )
                propagate(
                    coef_matrix,
                    box_dimensions,
                    current_coords,
                    weights,
                    collapsed,
                    visualise=visualise,
                    speed=speed,
                )


def backtrack(
    collapsed: Collapsed,
    weights: Weights,
    coef_matrix: CoefficientMatrix,
    history: History,
) -> None:
    revision = history.pop()
    size = len(weights)
    collapsed.intersection_update(revision[0])
    for y in range(size):
        for x, cell in enumerate(weights.keys()):
            weights[cell] = revision[1][cell]
            coef_matrix[f"{y}, {x}"] = revision[2][f"{y}, {x}"]
