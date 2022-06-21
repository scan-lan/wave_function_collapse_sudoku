
from logic.types import Coefficients, Coords


class ConstrainedCollapsedCellException(Exception):
    def __init__(self, coords: Coords, coefs: Coefficients):
        self.coords = coords
        self.coefs = coefs
        self.message = "Tried to constrain a cell with < 2 coefficients"

    def __str__(self):
        return f"{self.message}\nCoords: {self.coords}; Coefficients: {self.coefs}"


class GetValueFromUncollapsedCellException(Exception):
    def __init__(self, coefs: Coefficients):
        self.coefs = coefs
        self.message = f"Attempted to get collapsed value from uncollaped cell with coefs: {self.coefs}"

    def __str__(self):
        return self.message


class CollapseEmptyCellException(Exception):
    def __init__(self, coords: Coords):
        self.coords = coords
        self.message = f"Attempted to collapse empty cell at: {self.coords}"

    def __str__(self):
        return self.message
