from typing import Any
from pytest import fixture
from logic.create_grid import create_coef_matrix
from logic.types import Dimensions, Coords


@fixture(scope="package")
def coords_0_0() -> Coords:
    return {"y": 0, "x": 0}


@fixture(scope="package", params=((0, 0), (0, 1), (0, 3), (1, 0), (3, 3), (1, 1)), ids=lambda d: f"({d[0]}, {d[1]})")
def coords(request: Any) -> Coords:
    return {"y": request.param[0], "x": request.param[1]}


@fixture(scope="package", params=((2, 2), (2, 3), (3, 2), (3, 3), (4, 4), (5, 5)), ids=lambda d: f"{d[0]}x{d[1]}")
def box_dimensions(request: Any) -> Dimensions:
    return {"w": request.param[0], "h": request.param[1]}


@fixture(scope="function",
         params=(
             {"w": 2, "h": 2},
             {"w": 2, "h": 3},
             {"w": 3, "h": 2},
             {"w": 3, "h": 3},
             {"w": 4, "h": 4},
             {"w": 5, "h": 5},),
         ids=lambda bd: f"{bd['w']}x{bd['h']}")
def coef_matrix_with_box_dimensions(request: Any):
    return (create_coef_matrix(request.param['w'] * request.param['h']), request.param)


@fixture(scope="function")
def matrix_of_ints_4x4():
    return [[*range(i * 4, i * 4 + 4)] for i in range(4)]


@fixture(scope="package")
def box_dimensions_2x2():
    return {"w": 2, "h": 2}


@fixture(scope="function",
         params=(
             ({"1": 0, "2": 3, "3": 2, "4": 2}, "2"),
             ({"1": 4, "2": 2, "3": 2, "4": 2}, "1"),
             ({"1": 3, "2": 3, "3": 4, "4": 3}, "3"),
             ({"1": 1, "2": 0, "3": 0, "4": 0}, "1"),
             ({"1": 0, "2": 0, "3": 0, "4": 0}, "4"),
             ({"1": 1, "2": 0, "3": 1, "4": 0}, "3"),
         ))
def weights_with_expected(request: Any):
    return request.param[0].copy(), request.param[1]
