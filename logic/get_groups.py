from typing import List


def get_row(grid: List[List[int]], index: int):
    return grid[index]

def get_col(grid: List[List[int]], index: int):
    return [row[index] for row in grid]

def get_box(grid: List[List[int]]):
    pass
