from typing import Any

import pytest
from logic.create_grid import (
    create_coef_matrix,
    create_grid,
    fill_free_boxes,
    iterate,
)
from logic.free_boxes import get_free_coords
from logic.get_groups import get_coords_in_box
from logic.test.conftest import IterateSetup
from logic.types import Dimensions


@pytest.mark.performance
def test_get_coords_in_box(benchmark: Any, box_dimensions: Dimensions):
    w, h = box_dimensions["w"], box_dimensions["h"]
    benchmark(get_coords_in_box, box_dimensions, f"{h - 1}, {w - 1}")


@pytest.mark.performance
def test_create_coef_matrix(benchmark: Any, size: int):
    benchmark(create_coef_matrix, size)


@pytest.mark.performance
def test_get_free_coords(benchmark: Any, box_dimensions: Dimensions):
    benchmark(get_free_coords, box_dimensions)


@pytest.mark.performance
def test_fill_free_boxes(benchmark: Any, iterate_setup: IterateSetup):
    benchmark(
        fill_free_boxes,
        iterate_setup[0],
        iterate_setup[1],
        iterate_setup[2],
        iterate_setup[3],
        seed=0,
    )


@pytest.mark.performance
def test_iterate_no_filled(benchmark: Any, iterate_setup: IterateSetup):
    """
    Tests iterate() with no boxes filled by fill_free_boxes().
    """
    if iterate_setup[1]["w"] == 5 and iterate_setup[1]["h"] == 5:
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
    # if box_dimensions["w"] == 5 and box_dimensions["h"] == 5:
    #     pytest.skip(reason="5x5 too large for current implementation")
    benchmark(create_grid, box_dimensions, seed=0)
