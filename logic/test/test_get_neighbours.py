
from logic.get_neighbours import get_box_neighbours_coords, get_col_neighbours_coords, get_row_neighbours_coords
from logic.types import Dimensions, Coords


def test_get_row_neighbours_coords_correct_size(coords: Coords):
    assert len(get_row_neighbours_coords(9, coords)) == 8


def test_get_col_neighbours_coords_correct_size(coords: Coords):
    assert len(get_col_neighbours_coords(9, coords)) == 8


def test_get_box_neighbhours_coords_correct_size(box_dimensions: Dimensions, coords: Coords):
    expected_size = box_dimensions['w'] * box_dimensions['h'] - 1
    assert len(get_box_neighbours_coords(box_dimensions, coords)) == expected_size


def test_get_row_neighbours_coords_not_contain_arg_coords(coords: Coords):
    assert coords not in get_row_neighbours_coords(9, coords)


def test_get_col_neighbours_coords_not_contain_arg_coords(coords: Coords):
    assert coords not in get_col_neighbours_coords(9, coords)


def test_get_box_neighbours_coords_not_contain_arg_coords(box_dimensions: Dimensions, coords: Coords):
    assert coords not in get_box_neighbours_coords(box_dimensions, coords)
