
from logic.get_neighbours import get_box_neighbours_coords, get_col_neighbours_coords, get_row_neighbours_coords
from logic.types import Dimensions, Coords


def test_get_row_neighbours_coords_correct_size(coords_0_0: Coords):
    assert len(get_row_neighbours_coords(9, coords_0_0)) == 8


def test_get_col_neighbours_coords_correct_size(coords_0_0: Coords):
    assert len(get_col_neighbours_coords(9, coords_0_0)) == 8


def test_get_box_neighbhours_coords_correct_size(box_dimensions_3x3: Dimensions, coords_0_0: Coords):
    expected_size = box_dimensions_3x3['w'] * box_dimensions_3x3['h'] - 1
    assert len(get_box_neighbours_coords(box_dimensions_3x3, coords_0_0)) == expected_size


def test_get_box_neighbhours_coords_correct_size_uneven_box_dimensions(
    box_dimensions_3x2: Dimensions,
    box_dimensions_2x3: Dimensions,
    coords_0_0: Coords
):
    expected_size = box_dimensions_3x2['w'] * box_dimensions_3x2['h'] - 1
    assert len(get_box_neighbours_coords(box_dimensions_3x2, coords_0_0)) == expected_size
    assert len(get_box_neighbours_coords(box_dimensions_2x3, coords_0_0)) == expected_size


def test_get_row_neighbours_coords_not_contain_arg_coords(coords_0_1: Coords):
    assert coords_0_1 not in get_row_neighbours_coords(9, coords_0_1)


def test_get_col_neighbours_coords_not_contain_arg_coords(coords_0_1: Coords):
    assert coords_0_1 not in get_col_neighbours_coords(9, coords_0_1)


def test_get_box_neighbours_coords_not_contain_arg_coords(box_dimensions_3x3: Dimensions, coords_0_1: Coords):
    assert coords_0_1 not in get_box_neighbours_coords(box_dimensions_3x3, coords_0_1)


def test_get_box_neighbours_coords_not_contain_arg_coords_uneven_box_dimensions(box_dimensions_3x2: Dimensions, box_dimensions_2x3: Dimensions, coords_0_1: Coords):
    assert coords_0_1 not in get_box_neighbours_coords(box_dimensions_2x3, coords_0_1)
    assert coords_0_1 not in get_box_neighbours_coords(box_dimensions_3x2, coords_0_1)
