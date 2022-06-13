from logic.create_grid import create_grid
from logic.get_groups import get_box, get_col
from logic.types import Dimensions, Grid
from util.coords_converters import tuple_to_coords


def _test_create_grid_boxes_unique(box_dimensions: Dimensions):
    w, h = box_dimensions["w"], box_dimensions['w']
    expected_size = box_dimensions['w'] * box_dimensions['h']
    grid: Grid = create_grid(box_dimensions, seed=0)[0]
    for y in range(h):
        for x in range(w):
            current_box = get_box(grid, box_dimensions, tuple_to_coords((y, x)))
            assert len({*current_box}) == expected_size


def _test_create_grid_seed_results_in_same_grid(box_dimensions: Dimensions):
    grid1 = create_grid(box_dimensions, seed=64)
    grid2 = create_grid(box_dimensions, seed=64)
    grid_size = len(grid1)
    result = True

    for y in range(grid_size):
        for x in range(grid_size):
            if grid1[y][x] != grid2[y][x]:
                result = False
                break
        if not result:
            break

    assert result


def test_create_grid_rows_unique(box_dimensions_3x3: Dimensions):
    expected_size = box_dimensions_3x3['w'] * box_dimensions_3x3['h']
    grid: Grid = create_grid(box_dimensions_3x3, seed=0)[0]
    for row in grid:
        assert len({*row}) == expected_size


def test_create_grid_cols_unique(box_dimensions_3x3: Dimensions):
    expected_size = box_dimensions_3x3['w'] * box_dimensions_3x3['h']
    grid: Grid = create_grid(box_dimensions_3x3, seed=0)[0]
    col_sizes: set[int] = {len({*get_col(grid, i)}) for i in range(expected_size)}
    assert len(col_sizes) == 1


def test_create_grid_boxes_unique_for_multiple_box_sizes(
    box_dimensions_2x2: Dimensions,
    box_dimensions_2x3: Dimensions,
    box_dimensions_3x2: Dimensions,
    box_dimensions_3x3: Dimensions,
    box_dimensions_5x5: Dimensions,
):
    box_dimensions_list = [
        box_dimensions_2x2,
        box_dimensions_2x3,
        box_dimensions_3x2,
        box_dimensions_3x3,
        box_dimensions_5x5
    ]
    for box_dimensions in box_dimensions_list:
        _test_create_grid_boxes_unique(box_dimensions)


def test_create_grid_boxes_unique(box_dimensions_3x3: Dimensions):
    _test_create_grid_boxes_unique(box_dimensions_3x3)


def test_create_grid_seed_results_in_same_grid_multiple_sizes(
    box_dimensions_2x2: Dimensions,
    box_dimensions_2x3: Dimensions,
    box_dimensions_3x2: Dimensions,
    box_dimensions_3x3: Dimensions,
    box_dimensions_5x5: Dimensions,
):
    box_dimensions_list = [
        box_dimensions_2x2,
        box_dimensions_2x3,
        box_dimensions_3x2,
        box_dimensions_3x3,
        box_dimensions_5x5
    ]
    for box_dimensions in box_dimensions_list:
        _test_create_grid_seed_results_in_same_grid(box_dimensions)
