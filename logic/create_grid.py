from typing import List
from random import shuffle
from logic.Grid import Grid
from math import floor

def check_grid_valid(grid: Grid):
    for i in range(1, len(grid.grid)):
        for group in [grid.row, grid.col, grid.box]:
            if len(set(group(i))) < len(grid.grid):
                return False
    return True

# rows: List[List[int]] = [[0] * number_of_cells for _ in range(number_of_cells)]
# rows = [[(j + (floor(i / 3)) + (i % 3) * 3) % 9 + 1 for j in range(9)] for i in range(9)]

def create_test_grid() -> Grid:
    rows = [[(j + (floor(i / 3)) + (i % 3) * 3) % 9 + 1 for j in range(9)] for i in range(9)]
    return Grid(rows, rows, 3, 3)

def create_random_grid(box_width: int = 3, box_height: int = 3) -> Grid:
    number_of_cells = box_width * box_height
    rows: List[List[int]] = [[0] * number_of_cells for _ in range(number_of_cells)]

    free_boxes = min([box_width, box_height])
    for i in range(free_boxes):
        values = [*range(1, number_of_cells + 1)]
        shuffle(values)
        for j in range(box_height):
            values_index = j * box_width
            rows[i * box_height + j][i*box_width:i*box_width+box_width] = values[values_index:values_index+box_width]
    
    grid = Grid(rows, rows, box_width, box_height)

    return grid

def create_grid(box_width: int = 3, box_height: int = 3, difficulty: int = 1) -> Grid:
    grid = create_random_grid(box_width, box_height)
    # while not check_grid_valid(grid):
    #     grid = create_random_grid(box_width, box_height)
    
    return grid
