from logic2.create_grid import create_grid
from ui.print_grid import print_grid
# from logic2.get_groups import get_coordinate, get_row, get_col

BOX_WIDTH = 3
BOX_HEIGHT = 3
BOX_DIMENSIONS = {"width": BOX_WIDTH, "height": BOX_HEIGHT}

def main():
    grid = create_grid(BOX_DIMENSIONS)

    print_grid(grid, BOX_DIMENSIONS)

    # row = int(input("row\n")) - 1
    # col = int(input("col\n")) - 1
    # print(get_row(grid, row, BOX_DIMENSIONS)[col])

if __name__ == "__main__":
    main()
