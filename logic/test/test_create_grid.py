from logic.create_grid import create_grid, collapse, initialise_weights
from logic.get_groups import get_box, get_col, get_row
from logic.types import Cell, CoefficientMatrix, Coords, Dimensions, Grid, Weights


def test_collapse_gives_expected_result(
    matrix_dimensions: tuple[CoefficientMatrix, Dimensions],
    coords: Coords,
    weights_with_expected: tuple[Weights, Cell],
):
    collapse(matrix_dimensions[0], coords, weights_with_expected[0], set())
    assert matrix_dimensions[0][coords].pop() == weights_with_expected[1]


def test_collapse_results_in_cell_length_one(
    matrix_dimensions: tuple[CoefficientMatrix, Dimensions],
    coords: Coords,
    weights_with_expected: tuple[Weights, Cell],
):
    collapse(matrix_dimensions[0], coords, weights_with_expected[0], set())
    assert len(matrix_dimensions[0][coords]) == 1


def test_create_grid_seed_results_in_same_grid(box_dimensions: Dimensions):
    grid1 = create_grid(box_dimensions, seed=64)[0]
    grid2 = create_grid(box_dimensions, seed=64)[0]
    grid_size = box_dimensions["w"] * box_dimensions["h"]
    result = True

    for y in range(grid_size):
        for x in range(grid_size):
            if grid1[f"{y}, {x}"] != grid2[f"{y}, {x}"]:
                result = False
                break
        if not result:
            break

    assert result


def test_create_grid_rows_unique(box_dimensions: Dimensions):
    length = box_dimensions["w"] * box_dimensions["h"]
    grid: Grid = create_grid(box_dimensions, seed=0)[0]
    row_sizes: set[int] = {len({*get_row(grid, length, i)}) for i in range(length)}
    assert len(row_sizes) == 1


def test_create_grid_cols_unique(box_dimensions: Dimensions):
    length = box_dimensions["w"] * box_dimensions["h"]
    grid: Grid = create_grid(box_dimensions, seed=0)[0]
    col_sizes: set[int] = {len({*get_col(grid, length, i)}) for i in range(length)}
    assert len(col_sizes) == 1


def test_create_grid_boxes_unique(box_dimensions: Dimensions):
    w, h = box_dimensions["w"], box_dimensions["h"]
    grid: Grid = create_grid(box_dimensions, seed=0)[0]
    box_sizes = {
        len({*get_box(grid, box_dimensions, f"{y}, {x}")})
        for y in range(w)
        for x in range(h)
    }
    assert len(box_sizes) == 1


def test_create_grid_all_weights_zero(box_dimensions: Dimensions):
    weights = initialise_weights(box_dimensions["w"] * box_dimensions["h"])
    create_grid(box_dimensions, passed_weights=weights, seed=0)
    assert sum(weights.values()) == 0
