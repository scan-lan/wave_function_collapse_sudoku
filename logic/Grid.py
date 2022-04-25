from math import floor
from typing import List
from ui.Colours import Colours


class Grid:
    grid: List[List[str]]
    solution: List[List[str]]
    box_width: int
    box_height: int
    cell_num: int

    def __init__(self, grid: List[List[int]], solution: List[List[int]], box_width: int, box_height: int):
        self.grid = list(map(lambda row: list(map(lambda cell: str(cell) if cell != 0 else " ", row)), grid))
        self.solution = list(map(lambda row: list(map(lambda cell: str(cell), row)), solution))
        self.box_width = box_width
        self.box_height = box_height
        self.cell_num = box_width * box_height

    def row(self, index: int) -> List[str]:
        return self.grid[index]
    
    def col(self, index: int) -> List[str]:
        return list(map(lambda row: row[index], self.grid))

    def box(self, index: int) -> List[str]:
        box: List[str] = []
        for i in range(self.box_height):
            row = floor(index / self.box_height) * self.box_height + i
            for j in range(self.box_width):
                col = j + (index % self.box_height) * self.box_width
                box.append(self.grid[row][col])
        return box

    def __str__(self):
        grid_str = ""
        for i, row in enumerate(self.grid):
            if i != 0 and i % self.box_height == 0:
                grid_str += f"{((('——' if self.cell_num < 10 else '———') * self.box_width + '—+') * self.box_height)[:-1]}\n"
            for j, cell in enumerate(row):
                if j != 0 and j % self.box_width == 0:
                    grid_str += " |"
                grid_str += f" {cell}" if self.cell_num < 10 or int(cell) > 9 else f" {cell} "
                if j + 1 == len(row):
                    grid_str += f"  {Colours.OKCYAN}{i + 1}{Colours.END}\n"
            if i + 1 == len(self.grid):
                grid_str += ("  " if self.cell_num < 10 else "   " * self.box_width + " |") * (self.box_height - 1)
                col_indices = [f" {k}" if self.cell_num < 10 or k > 9 else f" {k} " for k in range(1, self.cell_num + 1)]
                col_indices = [f"  {char}" if i != 0 and i % self.box_width * 2 == 0 else char for i, char in enumerate(col_indices)]
                grid_str += f"\n{Colours.OKCYAN + ''.join(col_indices) + Colours.END}"

        return grid_str
