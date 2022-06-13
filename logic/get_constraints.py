from logic.types import BoxDimensions, CoefficientMatrix, Coefficients, Coords, GroupConstraints
from logic.get_neighbours import get_box_neighbours, get_col_neighbours, get_row_neighbours
from util.is_collapsed import is_collapsed

def get_row_constraints(matrix: CoefficientMatrix, coords: Coords) -> Coefficients:
    """
    Adds the values of all collapsed coefficients in the row
    containing cell `coords` to a set.
    """
    constraints: Coefficients = set()
    for coefs in get_row_neighbours(matrix, coords):
        if is_collapsed(coefs):
            constraints.add(coefs.pop())
    return constraints


def get_col_constraints(matrix: CoefficientMatrix, coords: Coords) -> Coefficients:
    """
    Adds the values of all collapsed coefficients in the column
    containing cell `coords` to a set.
    """
    constraints: Coefficients = set()
    for coefs in get_col_neighbours(matrix, coords):
        if is_collapsed(coefs):
            constraints.add(coefs.pop())
    return constraints


def get_box_constraints(matrix: CoefficientMatrix, box_dimensions: BoxDimensions, coords: Coords) -> Coefficients:
    """
    Adds the values of all collapsed coefficients in the box
    containing cell `coords` to a set.
    """
    constraints: Coefficients = set()
    for coefs in get_box_neighbours(matrix, box_dimensions, coords):
        if is_collapsed(coefs):
            constraints.add(coefs.pop())
    return constraints


def get_all_constraints(matrix: CoefficientMatrix, box_dimensions: BoxDimensions, coords: Coords) -> Coefficients:
    """
    Creates a set of all impossible values for the cell at the
    given `coords`.
    """
    return {
        *get_row_constraints(matrix, coords),
        *get_col_constraints(matrix, coords),
        *get_box_constraints(matrix, box_dimensions, coords)
    }


def get_constraints_by_group(matrix: CoefficientMatrix, box_dimensions: BoxDimensions, coords: Coords) -> GroupConstraints:
    """
    Creates a dictionary of impossible values for each sudoku "group" the cell at the given `coords` is in.
    """
    constraints: GroupConstraints = {
        "row": get_row_constraints(matrix, coords),
        "col": get_col_constraints(matrix, coords),
        "box": get_box_constraints(matrix, box_dimensions, coords)
    }
    return constraints