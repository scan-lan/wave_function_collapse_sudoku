import pytest
from typing import Any
from logic.create_grid import (create_coefficient_matrix, create_grid,
                               fill_free_boxes, get_free_coords, iterate)
from logic.types import CoefficientMatrix, Dimensions
from pytest_lazyfixture import lazy_fixture

dimensions_args = ([
    lazy_fixture("box_dimensions_2x2"),
    lazy_fixture("box_dimensions_2x3"),
    lazy_fixture("box_dimensions_3x2"),
    lazy_fixture("box_dimensions_3x3"),
    lazy_fixture("box_dimensions_4x4"),
    lazy_fixture("box_dimensions_5x5")],
    ["2x2", "2x3", "3x2", "3x3", "4x4", "5x5"])

coefs_dimensions_args = ([
    (lazy_fixture("coef_matrix_4x4"), lazy_fixture("box_dimensions_2x2")),
    (lazy_fixture("coef_matrix_6x6"), lazy_fixture("box_dimensions_2x3")),
    (lazy_fixture("coef_matrix_6x6"), lazy_fixture("box_dimensions_3x2")),
    (lazy_fixture("coef_matrix_9x9"), lazy_fixture("box_dimensions_3x3")),
    (lazy_fixture("coef_matrix_16x16"), lazy_fixture("box_dimensions_4x4")),
    (lazy_fixture("coef_matrix_25x25"), lazy_fixture("box_dimensions_5x5"))],
    ["2x2", "2x3", "3x2", "3x3", "4x4", "5x5"])


@pytest.mark.parametrize("box_dimensions", dimensions_args[0], ids=dimensions_args[1])
def test_create_matrix(benchmark: Any, box_dimensions: Dimensions):
    size = box_dimensions["w"] * box_dimensions["h"]
    benchmark(create_coefficient_matrix, size)


@pytest.mark.parametrize("box_dimensions", dimensions_args[0], ids=dimensions_args[1])
def test_get_free_coords(benchmark: Any, box_dimensions: Dimensions):
    benchmark(get_free_coords, box_dimensions)


@pytest.mark.parametrize("coef_matrix,box_dimensions", coefs_dimensions_args[0], ids=coefs_dimensions_args[1])
def test_fill_free_boxes(
        benchmark: Any,
        coef_matrix: CoefficientMatrix,
        box_dimensions: Dimensions):
    benchmark(fill_free_boxes, coef_matrix, box_dimensions, seed=0)


@pytest.mark.parametrize("coef_matrix,box_dimensions", coefs_dimensions_args[0], ids=coefs_dimensions_args[1])
def test_iterate(
        benchmark: Any,
        coef_matrix: CoefficientMatrix,
        box_dimensions: Dimensions):
    benchmark(iterate, coef_matrix, box_dimensions, seed=0)


@pytest.mark.parametrize("box_dimensions", dimensions_args[0], ids=dimensions_args[1])
def test_create_grid(benchmark: Any, box_dimensions: Dimensions):
    result_grid, _ = benchmark(create_grid, box_dimensions, seed=0)
    assert len(result_grid) == box_dimensions["w"] * box_dimensions["h"]
