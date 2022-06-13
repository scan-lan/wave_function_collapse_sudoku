from logic.types import Coords


def coords_to_tuple(coords: Coords) -> tuple[int, int]:
    return coords['y'], coords['x']


def tuple_to_coords(tup: tuple[int, int]) -> Coords:
    return {"y": tup[0], "x": tup[1]}
