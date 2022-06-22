from logic.types import Coords


def get_y(coords: Coords) -> str:
    return coords.split(", ")[0]


def get_x(coords: Coords) -> str:
    return coords.split(", ")[1]
