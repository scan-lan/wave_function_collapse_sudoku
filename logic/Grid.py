
from typing import List


class Grid:
    grid: List[List[str]]
    solution: List[List[str]]
    box_width: int
    box_height: int
    box_num: int
    cell_num: int

    def __init__(self, grid: List[List[int]], solution: List[List[int]], box_width: int, box_height: int):
        self.grid = list(map(lambda row: list(map(lambda cell: str(cell) if cell != 0 else " ", row)), grid))
        self.solution = list(map(lambda row: list(map(lambda cell: str(cell), row)), solution))
        self.box_width = box_width
        self.box_height = box_height
        self.box_num = box_width * box_height
        self.cell_num = self.box_num

    def row(self, index: int) -> List[str]:
        return self.grid[index]
    
    def col(self, index: int) -> List[str]:
        return list(map(lambda row: row[index], self.grid))

    # def box(self, index: int) -> List[str]:
    #     box: List[str] = []
    #     for i in range(self.box_width):
    #         for j in range(self.box_height):
    #             row = 
    #     return box

    def __str__(self):
        grid_str = ""
        for i, row in enumerate(self.grid):
            if i != 0 and i % self.box_height == 0:
                sample_line = list(grid_str.split("\n")[0])
                sample_line.pop()
                grid_str += "".join(map(lambda char: "+" if char == "|" else "—", sample_line)) + "\n"
            for j, cell in enumerate(row):
                if j == 0:
                    grid_str += " "
                if j != 0 and j % self.box_width == 0:
                    grid_str += "| "
                grid_str += f"{cell} " if self.cell_num < 10 or int(cell) > 9 else f"{cell}  "
                if j + 1 == len(row):
                    grid_str += " \n"
            # if i + 1 == len(self.grid):
            #     grid_str += "".join(list(map(lambda num: f"{num} ", range(1, len(self.grid) + 1))))

        return grid_str
