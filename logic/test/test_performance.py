from typing import Any
from logic.create_grid import (create_coefficient_matrix, create_grid,
                               fill_free_boxes, get_free_coords, iterate)
from logic.types import CoefficientMatrix, Dimensions


def test_create_matrix(benchmark: Any, box_dimensions: Dimensions):
    size = box_dimensions["w"] * box_dimensions["h"]
    benchmark(create_coefficient_matrix, size)


def test_get_free_coords(benchmark: Any, box_dimensions: Dimensions):
    benchmark(get_free_coords, box_dimensions)


def test_fill_free_boxes(
        benchmark: Any,
        coef_matrix: CoefficientMatrix,
        box_dimensions: Dimensions):
    benchmark(fill_free_boxes, coef_matrix, box_dimensions, seed=0)


def test_iterate(
        benchmark: Any,
        coef_matrix: CoefficientMatrix,
        box_dimensions: Dimensions):
    benchmark(iterate, coef_matrix, box_dimensions, seed=0)


def test_create_grid(benchmark: Any, box_dimensions: Dimensions):
    result_grid, _ = benchmark(create_grid, box_dimensions, seed=0)
    assert len(result_grid) == box_dimensions["w"] * box_dimensions["h"]
