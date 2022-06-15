from logic.create_grid import create_coefficient_matrix, create_grid, get_all_collapsed, iterate
from logic.types import Dimensions
from ui.print_grid import print_grid

BOX_WIDTH = 5
BOX_HEIGHT = 5
BOX_DIMENSIONS: Dimensions = {"w": BOX_WIDTH, "h": BOX_HEIGHT}


def main():
    grid, _ = create_grid(BOX_DIMENSIONS, seed=0)
    print_grid(grid, BOX_DIMENSIONS)

    coef_matrix = create_coefficient_matrix(25)
    iterate(coef_matrix, BOX_DIMENSIONS, seed=0)
    grid2 = get_all_collapsed(coef_matrix)
    print_grid(grid2, BOX_DIMENSIONS)


if __name__ == "__main__":
    main()
