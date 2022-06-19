import pytest
from logic.create_grid import create_coef_matrix, create_grid, get_all_collapsed, initialise_weights, iterate
from logic.types import Coords, Dimensions, Grid


def valid(grid: Grid):
    expected_size = len(grid)
    for i in range(len(grid)):
        if len({*grid[i]}) != expected_size:
            return False
        if len({row[i] for row in grid}) != expected_size:
            return False
    return True


@pytest.mark.success_rate
def test_create_grid_success_rates(box_dimensions: Dimensions):
    num_failures = 0
    for _ in range(1000):
        grid = create_grid(box_dimensions)[0]
        if not valid(grid):
            num_failures += 1
    assert num_failures == 0


@pytest.mark.success_rate
def test_iterate_success_rate(box_dimensions: Dimensions):
    num_failures = 0
    size = box_dimensions['h'] * box_dimensions['w']
    for _ in range(1000):
        coef_matrix = create_coef_matrix(size)
        weights = initialise_weights(size)
        collapsed: set[Coords] = set()
        iterate(coef_matrix, box_dimensions, weights, collapsed)
        grid = get_all_collapsed(coef_matrix)
        if not valid(grid):
            num_failures += 1
    assert num_failures == 0
