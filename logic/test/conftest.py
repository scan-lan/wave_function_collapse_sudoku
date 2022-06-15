from typing import Any
from pytest import fixture
from logic.create_grid import create_coefficient_matrix
from logic.types import Dimensions, Coords


@fixture(scope="package")
def coords_0_0() -> Coords:
    return {"y": 0, "x": 0}


@fixture(scope="package")
def coords_0_1() -> Coords:
    return {"y": 0, "x": 1}


@fixture(scope="package")
def coords_1_0() -> Coords:
    return {"y": 1, "x": 0}


@fixture(scope="package", params=((2, 2), (2, 3), (3, 2), (3, 3), (4, 4), (5, 5)), ids=lambda d: f"{d[0]}x{d[1]}")
def box_dimensions(request: Any) -> Dimensions:
    return {"w": request.param[0], "h": request.param[1]}


@fixture(scope="function", params=(4, 6, 9, 16, 25), ids=lambda n: f"{n}x{n}")
def coef_matrix(request: Any):
    return create_coefficient_matrix(request.param)


@fixture(scope="function")
def matrix_of_ints_4x4():
    return [[*range(i * 4, i * 4 + 4)] for i in range(4)]


@fixture(scope="package")
def box_dimensions_2x2():
    return {"w": 2, "h": 2}
