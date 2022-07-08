from random import seed as set_seed
from typing import Callable, Optional
from logic.exceptions import (
    CollapseEmptyCellException,
    ConstrainedCollapsedCellException,
    GetValueFromUncollapsedCellException,
)
from logic.free_boxes import fill_free_boxes
from logic.types import (
    Collapsed,
    Coords,
    Grid,
    Dimensions,
    CoefficientMatrix,
    History,
    OuterVisualiser,
    Visualiser,
    Weights,
)
from logic.wave_function import (
    collapse,
    create_coef_matrix,
    get_collapsed_value,
    propagate,
    backtrack,
)
from logic.weights import initialise_weights


def get_all_collapsed(coef_matrix: CoefficientMatrix) -> Grid:
    """
    Creates a matrix of collapsed cells in `coef_matrix`.  If a cell isn't
    collapsed, " " goes in its place.
    """
    return [
        [" " if len(coefs) != 1 else get_collapsed_value(coefs) for coefs in row]
        for row in coef_matrix
    ]


def get_uncollapsed(
    coef_matrix: CoefficientMatrix, collapsed: Collapsed
) -> Coords | None:
    """
    Get the coords of an uncollapsed cell.  Returns None if all
    cells are collapsed.
    """
    uncollapsed_coords: Coords | None = None
    all_uncollapsed_coords: list[Coords] = [
        (y, x)
        for y in range(len(coef_matrix))
        for x in range(len(coef_matrix))
        if (y, x) not in collapsed
    ]
    get_size: Callable[[Coords], int] = lambda t: len(coef_matrix[t[0]][t[1]])
    all_coords_sorted_by_num_coefs: list[Coords] = sorted(
        all_uncollapsed_coords, key=get_size, reverse=True
    )
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
    visualise: Optional[Visualiser] = None,
) -> None:
    """
    Repeat the collapse -> propagate loop until there are no
    uncollapsed cells left.
    """
    uncollapsed_coords = get_uncollapsed(coef_matrix, collapsed)
    while uncollapsed_coords:
        try:
            collapse(
                coef_matrix, uncollapsed_coords, weights, collapsed, history, seed=seed
            )
        except CollapseEmptyCellException:
            backtrack(collapsed, weights, coef_matrix, history)
            if visualise is not None:
                visualise(coef_matrix, box_dimensions)
        if visualise is not None:
            visualise(
                coef_matrix,
                box_dimensions,
                new_collapse=uncollapsed_coords,
            )
        try:
            propagate(
                coef_matrix,
                box_dimensions,
                uncollapsed_coords,
                weights,
                collapsed,
                visualise=visualise,
            )
        except (
            ConstrainedCollapsedCellException,
            GetValueFromUncollapsedCellException,
        ):
            backtrack(collapsed, weights, coef_matrix, history)
            if visualise is not None:
                visualise(coef_matrix, box_dimensions)
        uncollapsed_coords = get_uncollapsed(coef_matrix, collapsed)


def create_grid(
    box_dimensions: Dimensions = {"w": 3, "h": 3},
    difficulty: int = 1,
    seed: Optional[int] = None,
    passed_weights: Optional[Weights] = None,
    outer_visualise: Optional[OuterVisualiser] = None,
) -> tuple[Grid, CoefficientMatrix]:
    """
    Create a valid sudoku grid.
    """
    visualise = None
    if seed is not None:
        set_seed(seed)
    grid_size = box_dimensions["w"] * box_dimensions["h"]
    coef_matrix = create_coef_matrix(grid_size)
    if outer_visualise is not None:
        visualise = outer_visualise(coef_matrix, box_dimensions)
    weights = (
        passed_weights if passed_weights is not None else initialise_weights(grid_size)
    )
    collapsed: Collapsed = set()
    history: History = []

    fill_free_boxes(
        coef_matrix,
        box_dimensions,
        weights,
        collapsed,
        visualise=visualise,
    )
    iterate(
        coef_matrix,
        box_dimensions,
        weights,
        collapsed,
        history,
        visualise=visualise,
    )

    return get_all_collapsed(coef_matrix), coef_matrix
