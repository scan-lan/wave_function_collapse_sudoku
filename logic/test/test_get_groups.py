
from logic.get_groups import get_box, get_box_from_coords, get_col_from_coords, get_row, get_col, get_row_from_coords
from logic.types import Dimensions, Coords, Matrix
from util.coords_converters import make_coords


def test_get_row_size_correct(matrix_of_ints_4x4: Matrix[int]):
    assert len(matrix_of_ints_4x4) == len(get_row(matrix_of_ints_4x4, 0))


def test_get_row_returns_expected_items(matrix_of_ints_4x4: Matrix[int]):
    assert get_row(matrix_of_ints_4x4, 0) == [*range(4)]


def test_get_row_can_get_last_row(matrix_of_ints_4x4: Matrix[int]):
    assert get_row(matrix_of_ints_4x4, len(matrix_of_ints_4x4) - 1) == [*range(12, 16)]


def test_get_col_size_correct(matrix_of_ints_4x4: Matrix[int]):
    assert len(matrix_of_ints_4x4) == len(get_col(matrix_of_ints_4x4, 0))


def test_get_col_returns_expected_items(matrix_of_ints_4x4: Matrix[int]):
    assert get_col(matrix_of_ints_4x4, 1) == [*range(1, 16, 4)]


def test_get_col_can_get_last_col(matrix_of_ints_4x4: Matrix[int]):
    assert get_col(matrix_of_ints_4x4, len(matrix_of_ints_4x4) - 1) == [*range(3, 16, 4)]


def test_get_box_size_correct(
    matrix_of_ints_4x4: Matrix[int],
    box_dimensions_2x2: Dimensions,
    coords_0_0: Coords
):
    assert len(matrix_of_ints_4x4) == len(get_box(matrix_of_ints_4x4, box_dimensions_2x2, coords_0_0))


def test_get_box_returns_expected_items(matrix_of_ints_4x4: Matrix[int], box_dimensions_2x2: Dimensions, coords_0_0: Coords):
    assert get_box(matrix_of_ints_4x4, box_dimensions_2x2, coords_0_0) == [0, 1, 4, 5]


def test_get_box_can_get_last_box(matrix_of_ints_4x4: Matrix[int], box_dimensions_2x2: Dimensions):
    last_box_coords = make_coords(box_dimensions_2x2['w'] - 1, box_dimensions_2x2['h'] - 1)
    assert get_box(matrix_of_ints_4x4, box_dimensions_2x2, last_box_coords) == [10, 11, 14, 15]


def test_get_row_from_coords(matrix_of_ints_4x4: Matrix[int], coords_0_1: Coords):
    assert get_row_from_coords(matrix_of_ints_4x4, coords_0_1) == get_row(matrix_of_ints_4x4, coords_0_1['y'])


def test_get_col_from_coords(matrix_of_ints_4x4: Matrix[int], coords_0_1: Coords):
    assert get_col_from_coords(matrix_of_ints_4x4, coords_0_1) == get_col(matrix_of_ints_4x4, coords_0_1['x'])


def test_get_box_from_coords(matrix_of_ints_4x4: Matrix[int], box_dimensions_2x2: Dimensions, coords_0_1: Coords):
    assert get_box_from_coords(matrix_of_ints_4x4, box_dimensions_2x2, coords_0_1) == get_box(matrix_of_ints_4x4, box_dimensions_2x2, tuple_to_coords((0, 0)))
