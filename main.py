from logic.create_grid import create_grid
from logic.types import Dimensions
from ui.print_coef_matrix import print_coef_matrix
from ui.print_grid import print_grid

BOX_WIDTH = 3
BOX_HEIGHT = 3
BOX_DIMENSIONS: Dimensions = {"w": BOX_WIDTH, "h": BOX_HEIGHT}

def main():
    grid, coef_matrix = create_grid(BOX_DIMENSIONS, seed=64)

    print("Coef matrix returned:")
    print_coef_matrix(coef_matrix, BOX_DIMENSIONS)
    print_grid(grid, BOX_DIMENSIONS)


if __name__ == "__main__":
    main()
