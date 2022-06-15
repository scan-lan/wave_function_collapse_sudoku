from logic.create_grid import create_grid
from logic.get_groups import get_box, get_col
from logic.types import Dimensions, Grid
from ui.print_grid import print_grid
from util.coords_converters import make_coords


def test_create_grid_boxes_unique(box_dimensions: Dimensions):
    w, h = box_dimensions["w"], box_dimensions['w']
    box_sizes: set[int] = set()
    grid: Grid = create_grid(box_dimensions, seed=0)[0]
    print_grid(grid, box_dimensions)
    for y in range(w):
        for x in range(h):
            box_sizes.add(len({*get_box(grid, box_dimensions, make_coords(y, x))}))
    assert len(box_sizes) == 1


def test_create_grid_seed_results_in_same_grid(box_dimensions: Dimensions):
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


def test_create_grid_rows_unique(box_dimensions: Dimensions):
    row_sizes: set[int] = set()
    grid: Grid = create_grid(box_dimensions, seed=0)[0]
    for row in grid:
        row_sizes.add(len({*row}))
    assert len(row_sizes) == 1


def test_create_grid_cols_unique(box_dimensions: Dimensions):
    expected_size = box_dimensions['w'] * box_dimensions['h']
    grid: Grid = create_grid(box_dimensions, seed=0)[0]
    col_sizes: set[int] = {len({*get_col(grid, i)}) for i in range(expected_size)}
    assert len(col_sizes) == 1
