from random import shuffle
from logic.types import Grid, BoxDimensions, Coefficients, CoefficientMatrix

# rows = [[(j + (floor(i / 3)) + (i % 3) * 3) % 9 + 1 for j in range(9)] for i in range(9)]

def create_coefficient_matrix(size: int) -> CoefficientMatrix:
    coefficients: Coefficients = set([str(n) for n in range(1, size+1)])
    coefficient_matrix: CoefficientMatrix = []
    for _ in range(size):
        row = [coefficients.copy() for _ in range(size)]
        coefficient_matrix.append(row)

    return coefficient_matrix


def create_grid(box_dimensions: BoxDimensions = {"w": 3, "h": 3}, difficulty: int = 1) -> Grid:
    grid_size = box_dimensions["w"] * box_dimensions["h"]
    # solution_grid = [["0"] * grid_size for _ in range(grid_size)]
    coefficient_matrix = create_coefficient_matrix(grid_size)
    return [[]]
