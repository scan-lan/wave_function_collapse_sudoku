from typing import Any

import pytest
from logic.create_grid import (create_coef_matrix, create_grid,
                               fill_free_boxes, initialise_weights, iterate)
from logic.free_boxes import get_free_coords
from logic.get_groups import get_coords_in_box
from logic.test.conftest import IterateSetup
from logic.types import CoefficientMatrix, Coords, Dimensions


@pytest.mark.performance
def test_get_coords_in_box(benchmark: Any, box_dimensions: Dimensions):
    w, h = box_dimensions["w"], box_dimensions["h"]
    benchmark(get_coords_in_box, box_dimensions, (h - 1, w - 1))


@pytest.mark.performance
def test_create_coef_matrix(benchmark: Any, size: int):
    benchmark(create_coef_matrix, size)


@pytest.mark.performance
def test_create_matrix(benchmark: Any, box_dimensions: Dimensions):
    size = box_dimensions["w"] * box_dimensions["h"]
    benchmark(create_coef_matrix, size)


@pytest.mark.performance
def test_get_free_coords(benchmark: Any, box_dimensions: Dimensions):
    benchmark(get_free_coords, box_dimensions)


@pytest.mark.performance
def test_fill_free_boxes(benchmark: Any,
                         matrix_dimensions: tuple[CoefficientMatrix, Dimensions]):
    weights = initialise_weights(len(matrix_dimensions[0]))
    collapsed: set[Coords] = set()
    benchmark(fill_free_boxes, matrix_dimensions[0],
              matrix_dimensions[1], weights, collapsed, seed=0)


@pytest.mark.performance
def test_iterate_no_filled(benchmark: Any, iterate_setup: IterateSetup):
    """
    Tests iterate() with no boxes filled by fill_free_boxes().
    """
    if iterate_setup[1]['w'] == 5 and iterate_setup[1]['h'] == 5:
        pytest.skip(reason="5x5 too large for current implementation")
    benchmark(iterate, *iterate_setup, seed=0)


@pytest.mark.performance
def test_iterate_filled(benchmark: Any, iterate_setup_boxes: IterateSetup):
    """
    Tests iterate() with boxes filled by fill_free_boxes().  Effectively
    create_grid() but with the setup (box filling, weight initialisation,
    collapsed set creation, history creation) not included in the benchmark.
    """
    benchmark(iterate, *iterate_setup_boxes, seed=0)


@pytest.mark.performance
def test_create_grid(benchmark: Any, box_dimensions: Dimensions):
    result_grid, _ = benchmark(create_grid, box_dimensions, seed=0)
    assert len(result_grid) == box_dimensions["w"] * box_dimensions["h"]
