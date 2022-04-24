from typing import List
from random import shuffle
from logic.Grid import Grid

# def check_grid_valid(grid: Grid):
#     for i in range(len(grid)):
#         for j in range(len(grid)):
#             if grid[i][j] in 

def create_grid(difficulty :int, box_width: int = 3, box_height: int = 3) -> Grid:
    number_of_cells = box_width * box_height
    rows: List[List[int]] = []
    for _ in range(number_of_cells):
        cells = list(range(1, number_of_cells + 1))
        shuffle(cells)
        rows.append(cells)

    return Grid(rows, rows, box_width, box_height)
