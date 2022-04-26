from typing import List
from logic.Grid import Grid

def get_row_neighbours(grid: Grid, row: int, col: int) -> List[str]:
    neighbours = [cell for i, cell in enumerate(grid.grid[row]) if i != col]
    return neighbours

def get_column_neighbours(grid: Grid, row: int, col: int) -> List[str]:
    neighbours = [grid_row[col] for i, grid_row in enumerate(grid.grid) if i != row]
    return neighbours

def get_box_neighbours(grid: Grid, row: int, col: int) -> List[str]:
    # box_index = grid.box_height * (row // grid.box_height) + col // grid.box_width
    box_row = row - (row % grid.box_height)
    box_col = col - (col % grid.box_width)
    neighbours = [cell for row in grid.grid[box_row:box_row + grid.box_height] for cell in row[box_col:box_col + grid.box_width]]
    return neighbours
