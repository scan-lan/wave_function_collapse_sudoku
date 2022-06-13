from pytest import fixture

from logic.types import Coords
from util.coords_converters import coords_to_tuple, tuple_to_coords


@fixture(scope="package")
def coords_0_1() -> Coords:
    return {"y": 0, "x": 1}


@fixture(scope="package")
def tuple_0_1():
    return (0, 1)


def test_tuple_to_coords_returns_correct_size(tuple_0_1: tuple[int, int]):
    assert len(tuple_to_coords(tuple_0_1)) == 2


def test_tuple_to_coords_returns_expected_dict(tuple_0_1: tuple[int, int], coords_0_1: Coords):
    assert tuple_to_coords(tuple_0_1) == coords_0_1


def test_coords_to_tuple_returns_correct_size(coords_0_1: Coords):
    assert len(coords_to_tuple(coords_0_1)) == 2


def test_coords_to_tuple_returns_expected_dict(tuple_0_1: tuple[int, int], coords_0_1: Coords):
    assert coords_to_tuple(coords_0_1) == tuple_0_1
