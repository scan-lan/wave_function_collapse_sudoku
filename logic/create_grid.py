from random import seed as set_seed
from typing import Callable, Optional
from logic.Exceptions import (ConstrainedCollapsedCellException,
                              GetValueFromUncollapsedCellException)
from logic.free_boxes import fill_free_boxes
from logic.types import (Collapsed, Coords, Grid, Dimensions,
                         CoefficientMatrix, History, Weights)
from logic.wave_function import (collapse, create_coef_matrix,
                                 get_collapsed_value, propagate,
                                 revert_to_before_last_collapse)
from logic.weights import initialise_weights
from ui.print_coef_matrix import print_coef_matrix


def get_all_collapsed(coef_matrix: CoefficientMatrix) -> Grid:
    """
    Creates a matrix of collapsed cells in `coef_matrix`.  If a cell isn't
    collapsed, " " goes in its place.
    """
    return [[" " if len(coefs) != 1 else get_collapsed_value(coefs) for coefs in row] for row in coef_matrix]


def get_uncollapsed(coef_matrix: CoefficientMatrix, collapsed: Collapsed) -> Coords | None:
    """
    Get the coords of an uncollapsed cell.  Returns None if all
    cells are collapsed.
    """
    uncollapsed_coords: Coords | None = None
    all_uncollapsed_coords: list[Coords] = [(y, x) for y in range(
        len(coef_matrix)) for x in range(len(coef_matrix)) if (y, x) not in collapsed]
    get_size: Callable[[Coords], int] = lambda t: len(coef_matrix[t[0]][t[1]])
    all_coords_sorted_by_num_coefs: list[Coords] = sorted(all_uncollapsed_coords, key=get_size, reverse=True)
    if all_coords_sorted_by_num_coefs:
        uncollapsed_coords = all_coords_sorted_by_num_coefs.pop()
    return uncollapsed_coords


def iterate(
        coef_matrix: CoefficientMatrix,
        box_dimensions: Dimensions,
        weights: Weights,
        collapsed: Collapsed,
        history: History,
        seed: Optional[int] = None,
        visualise: bool = False,
        speed: float = 1) -> None:
    """
    Repeat the collapse -> propagate loop until there are no
    uncollapsed cells left.
    """
    uncollapsed_coords = get_uncollapsed(coef_matrix, collapsed)
    while uncollapsed_coords:
        collapse(coef_matrix, uncollapsed_coords, weights, collapsed, history, seed=seed)
        if visualise:
            print_coef_matrix(coef_matrix, box_dimensions, sleep=(2 / speed), new_collapse=uncollapsed_coords)
        try:
            propagate(
                coef_matrix,
                box_dimensions,
                uncollapsed_coords,
                weights,
                collapsed,
                visualise=visualise,
                speed=speed)
        except (ConstrainedCollapsedCellException, GetValueFromUncollapsedCellException):
            revert_to_before_last_collapse(collapsed, weights, coef_matrix, history)
            if visualise:
                print_coef_matrix(coef_matrix, box_dimensions, sleep=5)
        uncollapsed_coords = get_uncollapsed(coef_matrix, collapsed)


def create_grid(box_dimensions: Dimensions = {"w": 3, "h": 3},
                difficulty: int = 1,
                seed: Optional[int] = None,
                passed_weights: Optional[Weights] = None,
                visualise: bool = False,
                speed: float = 1,
                skip_free_boxes: bool = False) -> tuple[Grid, CoefficientMatrix]:
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
    collapsed: Collapsed = set()
    history: History = []

    fill_free_boxes(
        coef_matrix,
        box_dimensions,
        weights,
        collapsed,
        visualise=(visualise and not skip_free_boxes),
        speed=5 * speed)
    iterate(coef_matrix, box_dimensions, weights, collapsed, history, visualise=visualise, speed=3 * speed)
    # print("; ".join([f"{value}: {weight}" for value, weight in weights.items()]))

    return get_all_collapsed(coef_matrix), coef_matrix
