from curses import wrapper
from logic.types import Dimensions
from ui.app import start

BOX_WIDTH = 3
BOX_HEIGHT = 3
BOX_DIMENSIONS: Dimensions = {"w": BOX_WIDTH, "h": BOX_HEIGHT}


def main():
    wrapper(start, 200)
    # grid, _ = create_grid(
    #     BOX_DIMENSIONS, visualise=True, skip_free_boxes=False, speed=15
    # )
    # print(grid_to_string(grid, BOX_DIMENSIONS))


if __name__ == "__main__":
    main()
