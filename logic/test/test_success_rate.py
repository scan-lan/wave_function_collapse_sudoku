from copy import deepcopy
import pytest
from logic.create_grid import create_grid, get_all_collapsed, iterate
from logic.get_groups import get_box, get_col, get_row
from logic.test.conftest import IterateSetup
from logic.types import Dimensions, Grid

rounds = 100
max_size = 4


def valid(grid: Grid, box_dimensions: Dimensions):
    length = box_dimensions["w"] * box_dimensions["h"]
    for y, x in [
        (y, x) for y in range(box_dimensions["h"]) for x in range(box_dimensions["w"])
    ]:
        i = y * max(box_dimensions.values()) + x
        if len({*get_row(grid, length, i)}) != length:
            return False
        if len({*get_col(grid, length, i)}) != length:
            return False
        box_coords = f"{y}, {x}"
        if len({*get_box(grid, box_dimensions, box_coords)}) != length:
            return False
    return True


@pytest.mark.success_rate
def test_create_grid_success_rates(box_dimensions: Dimensions):
    num_failures = 0
    if box_dimensions["w"] > max_size or box_dimensions["h"] > max_size:
        pytest.skip(
            reason=(
                f'{box_dimensions["w"]}x{box_dimensions["h"]} '
                "too large for current implementation"
            )
        )
    for _ in range(rounds):
        grid = create_grid(box_dimensions)[0]
        if not valid(grid, box_dimensions):
            num_failures += 1
    assert num_failures == 0


@pytest.mark.success_rate
def test_iterate_success_rate(iterate_setup: IterateSetup):
    num_failures = 0
    dimensions = iterate_setup[1]
    if dimensions["w"] > max_size or dimensions["h"] > max_size:
        pytest.skip(
            reason=(
                f'{dimensions["w"]}x{dimensions["h"]} '
                "too large for current implementation"
            )
        )
    for _ in range(rounds):
        matrix = deepcopy(iterate_setup[0])
        weights = iterate_setup[2].copy()
        collapsed = iterate_setup[3].copy()
        history = iterate_setup[4].copy()
        iterate(matrix, dimensions, weights, collapsed, history)
        grid = get_all_collapsed(matrix)
        if not valid(grid, dimensions):
            num_failures += 1
    assert num_failures == 0
