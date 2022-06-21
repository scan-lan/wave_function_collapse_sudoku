from logic.create_grid import create_grid
from logic.types import Dimensions
from ui.print_grid import print_grid

BOX_WIDTH = 3
BOX_HEIGHT = 3
BOX_DIMENSIONS: Dimensions = {"w": BOX_WIDTH, "h": BOX_HEIGHT}


def main():
    grid, _ = create_grid(BOX_DIMENSIONS, visualise=True, speed=2, skip_free_boxes=True)
    print_grid(grid, BOX_DIMENSIONS)


if __name__ == "__main__":
    main()
