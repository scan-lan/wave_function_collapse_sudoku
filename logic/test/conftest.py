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


@fixture(scope="package")
def box_dimensions_2x2() -> Dimensions:
    return {"w": 2, "h": 2}


@fixture(scope="function")
def coef_matrix_4x4():
    return create_coefficient_matrix(4)


@fixture(scope="module")
def box_dimensions_2x3() -> Dimensions:
    return {"w": 2, "h": 3}


@fixture(scope="function")
def coef_matrix_6x6():
    return create_coefficient_matrix(6)


@fixture(scope="module")
def box_dimensions_3x2() -> Dimensions:
    return {"w": 3, "h": 2}


@fixture(scope="module")
def box_dimensions_3x3() -> Dimensions:
    return {"w": 3, "h": 3}


@fixture(scope="function")
def coef_matrix_9x9():
    return create_coefficient_matrix(9)


@fixture(scope="function")
def matrix_of_ints_4x4():
    return [[*range(i*4, i*4+4)] for i in range(4)]
