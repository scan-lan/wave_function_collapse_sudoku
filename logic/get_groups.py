from logic.types import BoxDimensions, Coords


def get_row(grid: List[List[int]], index: int):
    return grid[index]

def get_col(grid: List[List[int]], index: int):
    return [row[index] for row in grid]


def get_box_coords(box_dimensions: BoxDimensions, box_coords: Coords) -> list[Coords]:
    coords: list[Coords] = []
    box_offset_y = box_coords["y"] * box_dimensions["h"]
    box_offset_x = box_coords["x"] * box_dimensions["w"]
    for y in range(box_dimensions["h"]):
        for x in range(box_dimensions["w"]):
            coords.append({"y" : box_offset_y + y, "x": box_offset_x + x})
    return coords


