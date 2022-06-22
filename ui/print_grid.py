from colorama import init, Fore

from logic.types import Dimensions, Grid

init()


def print_grid(grid: Grid, box_dimensions: Dimensions) -> None:
    width, height = box_dimensions["w"], box_dimensions["h"]
    size = width * height
    str_length = len(f"{size}")
    grid_str = "\n"
    for y in range(size):
        if y != 0 and y % height == 0:
            box_bottom = ("—" * (str_length + 1)) * box_dimensions["w"] + "—+"
            grid_str += (box_bottom * box_dimensions["h"])[:-1] + "\n"
        for x in range(size):
            cell = grid[f"{y}, {x}"]
            if x != 0 and x % width == 0:
                grid_str += " |"
            grid_str += f" {cell}" if size < 10 or str_length > 1 else f" {cell} "
            if x + 1 == size:
                grid_str += f"  {Fore.CYAN}{y + 1}{Fore.RESET}\n"
        if y + 1 == size:
            grid_str += ((" " * (str_length + 1)) * width + " |") * (height - 1)
            col_indices = [
                f" {k}" if size < 10 or k > 9 else f" {k} " for k in range(1, size + 1)
            ]
            col_indices = [
                f"  {char}" if i != 0 and i % width * 2 == 0 else char
                for i, char in enumerate(col_indices)
            ]
            grid_str += f'\n{Fore.CYAN + "".join(col_indices) + Fore.RESET}'

    print(grid_str)
