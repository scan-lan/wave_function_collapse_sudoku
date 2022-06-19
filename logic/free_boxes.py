from random import shuffle, seed as set_seed
from typing import Optional
from logic.get_groups import get_coords_in_box

from logic.types import (Cell, CoefficientMatrix, Collapsed,
                         Coords, Dimensions, Weights)
from logic.wave_function import collapse, propagate
from ui.print_coef_matrix import print_coef_matrix


def get_random_values(grid_size: int) -> list[Cell]:
    """
    Creates a list from 1 - `grid_size + 1` and randomises the
    order.
    """
    values = [str(val) for val in range(1, grid_size + 1)]
    shuffle(values)
    return values


def get_free_coords(box_dimensions: Dimensions) -> list[Coords]:
    """
    Gets a list of the coords in the free boxes for a matrix with
    box dimensions of `box_dimensions`. These are all the coords
    which don't constrain each other beyond the box-level.
    """
    num_free_boxes = min(box_dimensions.values())
    if tuple(box_dimensions.values()) == (2, 2):
        num_free_boxes = 1
    return [coord for i in range(num_free_boxes) for coord in get_coords_in_box(box_dimensions, (i, i))]


def fill_free_boxes(
        coef_matrix: CoefficientMatrix,
        box_dimensions: Dimensions,
        weights: Weights,
        collapsed: Collapsed,
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
    collapsed.update(free_cell_coords)
    for coords in free_cell_coords:
        if len(values) == 0:
            values = get_random_values(box_size)
        collapse(coef_matrix, coords, weights, values.pop())
        if visualise:
            print_coef_matrix(coef_matrix, box_dimensions, sleep=(2 / speed), new_collapse=coords)
        propagate(coef_matrix, box_dimensions, coords, weights, collapsed,
                  skip=["box"], visualise=visualise, speed=speed)
