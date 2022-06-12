
from typing import Dict, List
from logic2.get_groups import get_row
from ui.Colours import Colours


def print_grid(grid: List[List[str]], box_dimensions: Dict[str, int]) -> None:
    cell_num = box_dimensions["width"] * box_dimensions["height"]
    grid_str = "\n"
    for i, row in enumerate([get_row(grid, j, box_dimensions) for j in range(len(grid))]):
        if i != 0 and i % box_dimensions["height"] == 0:
            grid_str += f"{((('——' if cell_num < 10 else '———') * box_dimensions['width'] + '—+') * box_dimensions['height'])[:-1]}\n"
        for j, cell in enumerate(row):
            if j != 0 and j % box_dimensions["width"] == 0:
                grid_str += " |"
            grid_str += f" {cell}" if cell_num < 10 or len(cell) > 1 else f" {cell} "
            if j + 1 == len(row):
                grid_str += f"  {Colours.OKCYAN}{i + 1}{Colours.END}\n"
        if i + 1 == len(grid):
            grid_str += ("  " if cell_num < 10 else "   " * box_dimensions["width"] + " |") * (box_dimensions["height"] - 1)
            col_indices = [f" {k}" if cell_num < 10 or k > 9 else f" {k} " for k in range(1, cell_num + 1)]
            col_indices = [f"  {char}" if i != 0 and i % box_dimensions["width"] * 2 == 0 else char for i, char in enumerate(col_indices)]
            grid_str += f"\n{Colours.OKCYAN + ''.join(col_indices) + Colours.END}"

    print(grid_str)