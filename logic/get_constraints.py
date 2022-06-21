from logic.types import (
    Dimensions,
    CoefficientMatrix,
    Coefficients,
    Coords,
    GroupConstraints,
)
from logic.get_neighbours import (
    get_box_neighbours,
    get_col_neighbours,
    get_row_neighbours,
)


def get_row_constraints(matrix: CoefficientMatrix, coords: Coords) -> Coefficients:
    """
    Adds the values of all collapsed coefficients in the row
    containing cell `coords` to a set.
    """
    constraints: Coefficients = {
        coefs.copy().pop()
        for coefs in get_row_neighbours(matrix, coords)
        if len(coefs) == 1
    }
    return constraints


def get_col_constraints(matrix: CoefficientMatrix, coords: Coords) -> Coefficients:
    """
    Adds the values of all collapsed coefficients in the column
    containing cell `coords` to a set.
    """
    constraints: Coefficients = {
        coefs.copy().pop()
        for coefs in get_col_neighbours(matrix, coords)
        if len(coefs) == 1
    }
    return constraints


def get_box_constraints(
    matrix: CoefficientMatrix, box_dimensions: Dimensions, coords: Coords
) -> Coefficients:
    """
    Adds the values of all collapsed coefficients in the box containing cell `coords` to
    a set.
    """
    constraints: Coefficients = {
        coefs.copy().pop()
        for coefs in get_box_neighbours(matrix, box_dimensions, coords)
        if len(coefs) == 1
    }
    return constraints


def get_all_constraints(
    matrix: CoefficientMatrix, box_dimensions: Dimensions, coords: Coords
) -> Coefficients:
    """
    Creates a set of all impossible values for the cell at the given `coords`.
    """
    return {
        *get_row_constraints(matrix, coords),
        *get_col_constraints(matrix, coords),
        *get_box_constraints(matrix, box_dimensions, coords),
    }


def get_constraints_by_group(
    matrix: CoefficientMatrix, box_dimensions: Dimensions, coords: Coords
) -> GroupConstraints:
    """
    Creates a dictionary of impossible values for each sudoku "group" the cell at the
    given `coords` is in.
    """
    constraints: GroupConstraints = {
        "row": get_row_constraints(matrix, coords),
        "col": get_col_constraints(matrix, coords),
        "box": get_box_constraints(matrix, box_dimensions, coords),
    }
    return constraints
