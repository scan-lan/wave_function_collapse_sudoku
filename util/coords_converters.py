from logic.types import Coords


def coords_to_tuple(coords: Coords) -> tuple[int, int]:
    return coords['y'], coords['x']


def make_coords(y: int, x: int) -> Coords:
    return {"y": y, "x": x}
