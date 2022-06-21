from typing import Any
from pytest import fixture
from logic.create_grid import create_coef_matrix
from logic.free_boxes import fill_free_boxes
from logic.types import (
    CoefficientMatrix,
    Collapsed,
    Dimensions,
    Coords,
    History,
    Weights,
)
from logic.weights import initialise_weights

IterateSetup = tuple[CoefficientMatrix, Dimensions, Weights, Collapsed, History]


@fixture(
    scope="package",
    params=((0, 0), (0, 1), (0, 3), (1, 0), (3, 3), (1, 1)),
    ids=lambda d: f"({d[0]}, {d[1]})",
)
def coords(request: Any) -> Coords:
    return request.param


@fixture(
    scope="package",
    params=((2, 2), (2, 3), (3, 2), (3, 3), (3, 4), (3, 5), (4, 4), (5, 5)),
    ids=lambda d: f"{d[0]}x{d[1]}",
)
def box_dimensions(request: Any) -> Dimensions:
    return {"w": request.param[0], "h": request.param[1]}


@fixture(scope="package")
def size(box_dimensions: Dimensions):
    return box_dimensions["w"] * box_dimensions["h"]


@fixture(scope="function")
def matrix_dimensions(box_dimensions: Dimensions):
    return (
        create_coef_matrix(box_dimensions["w"] * box_dimensions["h"]),
        box_dimensions,
    )


@fixture(scope="function")
def iterate_setup(
    matrix_dimensions: tuple[CoefficientMatrix, Dimensions]
) -> IterateSetup:
    size = len(matrix_dimensions[0])
    weights = initialise_weights(size)
    collapsed: set[Coords] = set()
    history: History = []
    return (matrix_dimensions[0], matrix_dimensions[1], weights, collapsed, history)


@fixture(scope="function")
def iterate_setup_boxes(iterate_setup: IterateSetup) -> IterateSetup:
    coef_matrix = iterate_setup[0]
    box_dimensions = iterate_setup[1]
    weights = iterate_setup[2]
    collapsed = iterate_setup[3]
    fill_free_boxes(coef_matrix, box_dimensions, weights, collapsed)
    return (coef_matrix, box_dimensions, weights, collapsed, iterate_setup[4])


@fixture(scope="function")
def matrix_of_ints_4x4():
    return [[*range(i * 4, i * 4 + 4)] for i in range(4)]


@fixture(scope="package")
def box_dimensions_2x2():
    return {"w": 2, "h": 2}


@fixture(
    scope="function",
    params=(
        ({"1": 0, "2": 3, "3": 2, "4": 2}, "2"),
        ({"1": 4, "2": 2, "3": 2, "4": 2}, "1"),
        ({"1": 3, "2": 3, "3": 4, "4": 3}, "3"),
        ({"1": 1, "2": 0, "3": 0, "4": 0}, "1"),
        ({"1": 0, "2": 0, "3": 0, "4": 0}, "4"),
        ({"1": 1, "2": 0, "3": 1, "4": 0}, "3"),
    ),
)
def weights_with_expected(request: Any):
    return request.param[0].copy(), request.param[1]
