from typing import Any
from logic.create_grid import (create_coefficient_matrix, create_grid,
                               fill_free_boxes, get_free_coords, initialise_weights, iterate)
from logic.get_groups import get_coords_in_box
from logic.types import CoefficientMatrix, Dimensions
from util.coords_converters import make_coords


def test_get_coords_in_box(benchmark: Any, box_dimensions: Dimensions):
    w, h = box_dimensions["w"], box_dimensions["h"]
    benchmark(get_coords_in_box, box_dimensions, make_coords(h - 1, w - 1))


def test_create_matrix(benchmark: Any, box_dimensions: Dimensions):
    size = box_dimensions["w"] * box_dimensions["h"]
    benchmark(create_coefficient_matrix, size)


def test_get_free_coords(benchmark: Any, box_dimensions: Dimensions):
    benchmark(get_free_coords, box_dimensions)


def test_fill_free_boxes(
        benchmark: Any,
        coef_matrix_with_box_dimensions: tuple[CoefficientMatrix, Dimensions]):
    weights = initialise_weights(len(coef_matrix_with_box_dimensions[0]))
    benchmark(fill_free_boxes, coef_matrix_with_box_dimensions[0], coef_matrix_with_box_dimensions[1], weights, seed=0)


def test_iterate(
        benchmark: Any,
        coef_matrix_with_box_dimensions: tuple[CoefficientMatrix, Dimensions]):
    weights = initialise_weights(len(coef_matrix_with_box_dimensions[0]))
    benchmark(iterate, coef_matrix_with_box_dimensions[0], coef_matrix_with_box_dimensions[1], weights, seed=0)


def test_create_grid(benchmark: Any, box_dimensions: Dimensions):
    result_grid, _ = benchmark(create_grid, box_dimensions, seed=0)
    assert len(result_grid) == box_dimensions["w"] * box_dimensions["h"]
