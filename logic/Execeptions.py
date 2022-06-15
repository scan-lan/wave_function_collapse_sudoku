
from logic.types import Coefficients, Coords


class ConstrainedCollapsedCellException(Exception):
    def __init__(self, coords: Coords, coefs: Coefficients):
        self.coords = coords
        self.coefs = coefs
        self.message = "Tried to constrain a cell with < 2 coefficients"

    def __str__(self):
        return f"{self.message}\nCoords: {self.coords}; Coefficients: {self.coefs}"
