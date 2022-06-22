from logic.coords import get_x, get_y
from logic.get_groups import (
    get_box,
    get_box_coords_from_matrix_coords,
    get_box_from_coords,
    get_col_from_coords,
    get_coords_in_box,
    get_row,
    get_col,
    get_row_from_coords,
)
from logic.types import Dimensions, Coords, Matrix


def test_get_row_size_correct(matrix_of_ints_4x4: Matrix[int]):
    assert len(get_row(matrix_of_ints_4x4, 4, 0)) == 4


def test_get_row_returns_expected_items(matrix_of_ints_4x4: Matrix[int]):
    assert get_row(matrix_of_ints_4x4, 4, 0) == [*range(4)]


def test_get_row_can_get_last_row(matrix_of_ints_4x4: Matrix[int]):
    length = 4
    assert get_row(matrix_of_ints_4x4, length, length - 1) == [*range(12, 16)]


def test_get_col_size_correct(matrix_of_ints_4x4: Matrix[int]):
    assert len(get_col(matrix_of_ints_4x4, 4, 0)) == 4


def test_get_col_returns_expected_items(matrix_of_ints_4x4: Matrix[int]):
    assert get_col(matrix_of_ints_4x4, 4, 1) == [*range(1, 16, 4)]


def test_get_col_can_get_last_col(matrix_of_ints_4x4: Matrix[int]):
    length = 4
    assert get_col(matrix_of_ints_4x4, length, length - 1) == [*range(3, 16, 4)]


def test_get_box_size_correct(
    matrix_of_ints_4x4: Matrix[int],
    box_dimensions_2x2: Dimensions,
):
    assert len(get_box(matrix_of_ints_4x4, box_dimensions_2x2, "0, 0")) == 4


def test_get_box_returns_expected_items(
    matrix_of_ints_4x4: Matrix[int], box_dimensions_2x2: Dimensions
):
    assert get_box(matrix_of_ints_4x4, box_dimensions_2x2, "0, 0") == [
        0,
        1,
        4,
        5,
    ]


def test_get_box_can_get_last_box(
    matrix_of_ints_4x4: Matrix[int], box_dimensions_2x2: Dimensions
):
    last_box_coords = f'{box_dimensions_2x2["w"] - 1}, {box_dimensions_2x2["h"] - 1}'
    assert get_box(matrix_of_ints_4x4, box_dimensions_2x2, last_box_coords) == [
        10,
        11,
        14,
        15,
    ]


def test_get_row_from_coords(matrix_of_ints_4x4: Matrix[int], coords: Coords):
    assert get_row_from_coords(matrix_of_ints_4x4, 4, coords) == get_row(
        matrix_of_ints_4x4, 4, int(get_y(coords))
    )


def test_get_col_from_coords(matrix_of_ints_4x4: Matrix[int], coords: Coords):
    assert get_col_from_coords(matrix_of_ints_4x4, 4, coords) == get_col(
        matrix_of_ints_4x4, 4, int(get_x(coords))
    )


def test_get_box_from_coords(
    matrix_of_ints_4x4: Matrix[int], box_dimensions_2x2: Dimensions, coords: Coords
):
    box_coords = get_box_coords_from_matrix_coords(box_dimensions_2x2, coords)
    expected_box = get_box(matrix_of_ints_4x4, box_dimensions_2x2, box_coords)
    assert (
        get_box_from_coords(matrix_of_ints_4x4, box_dimensions_2x2, coords)
        == expected_box
    )


def test_get_coords_in_box_is_expected_length(box_dimensions: Dimensions):
    coords_extremes: list[Coords] = [
        "0, 0",
        f'0, {box_dimensions["h"] - 1}',
        f'{box_dimensions["w"] - 1}, 0',
        f'{box_dimensions["w"] - 1}, {box_dimensions["h"] - 1}',
    ]
    for coords in coords_extremes:
        coords_list = get_coords_in_box(box_dimensions, coords)
        expected_length = box_dimensions["w"] * box_dimensions["h"]
        assert len(coords_list) == expected_length
