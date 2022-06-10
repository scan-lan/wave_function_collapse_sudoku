
from random import shuffle
from typing import Dict, List

# from logic2.get_groups import get_coordinate, get_row, get_col


def get_random_values(num: int):
    values = [str(x) for x in [*range(1, num + 1)]]
    shuffle(values)
    return values


def create_grid(box_dimensions: Dict[str, int]) -> List[List[str]]:
    """
    Creates a grid.

    1. Create array of array of empty strings representing grid -> boxes -> cells
    2. Calculate free boxes for grid size
    3. Fill free boxes with numbers 1-number_cells in a randomised order
    4. Iterate over remaining boxes, filling their values

    Terminology:
    Free box: a standard 9x9 grid has 3 free boxes, as numbers of any order
    can be placed into them with no constraints, as boxes diagonal to one
    another do not interact. e.g.:
        free | none | none
        —————+——————+—————
        none | free | none
        —————+——————+—————
        none | none | free
    """
    number_cells = box_dimensions["width"] * box_dimensions["height"]
    grid = [[" "] * number_cells for _ in range(number_cells)]

    free_boxes = min([box_dimensions["width"], box_dimensions["height"]])
    for i in range(free_boxes):
        values = get_random_values(number_cells)
        grid[i * box_dimensions["width"] + i] = values

    # for i, box in enumerate(grid):
    #     if box[0] != " ":
    #         continue
    #     values = get_random_values(number_cells)
    #     for j in range(len(box)):
    #         row, col = get_coordinate(i, j, box_dimensions)
    #         if values[-1] not in get_row(grid, row, box_dimensions) or get_col(grid, col, box_dimensions):
    #             grid[i][j] = values.pop()

    return grid


# shannon_entropy_for_square = log(sum(weight)) - (sum(weight * log(weight)) / sum(weight))