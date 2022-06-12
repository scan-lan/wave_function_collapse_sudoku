from logic.create_grid import create_grid
from logic.types import BoxDimensions
from ui.print_grid import print_grid

BOX_WIDTH = 3
BOX_HEIGHT = 3
BOX_DIMENSIONS: BoxDimensions = {"w": BOX_WIDTH, "h": BOX_HEIGHT}

def main():
    grid = create_grid(BOX_DIMENSIONS)

    print_grid(grid, BOX_DIMENSIONS)

if __name__ == "__main__":
    main()
