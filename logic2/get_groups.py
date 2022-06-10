
from typing import Dict, List, Tuple


def get_box(grid: List[List[str]], index: int) -> List[str]:
    return grid[index]

def get_col(grid: List[List[str]], index: int, box_dimensions: Dict[str, int]):
    first_box = index // box_dimensions["width"]
    first_cell = index % box_dimensions["width"]
    return [cell for box in grid[first_box::box_dimensions["width"]] for cell in box [first_cell::box_dimensions["height"]]]

def get_row(grid: List[List[str]], index: int, box_dimensions: Dict[str, int]):
    first_box = index - (index % box_dimensions["height"])
    first_cell = (index % box_dimensions["height"]) * box_dimensions["width"]
    return [cell for box in grid[first_box:first_box + box_dimensions["height"]] for cell in box [first_cell:first_cell + box_dimensions["width"]]]

def get_coordinate(box_index: int, cell_index: int, box_dimensions: Dict[str, int]) -> Tuple[int, int]:
    col = (box_index % box_dimensions["height"]) * box_dimensions["width"] + cell_index % box_dimensions["width"]
    row = box_index - (box_index % box_dimensions["height"]) + cell_index // box_dimensions["height"]
    return (col, row)
