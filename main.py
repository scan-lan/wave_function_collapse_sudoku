import sys
from curses import wrapper
from typing import Final

from logic.types import Dimensions
from ui.app import start

VALID_OPTS: Final = ["--splash-time"]
BOX_WIDTH = 3
BOX_HEIGHT = 3
BOX_DIMENSIONS: Dimensions = {"w": BOX_WIDTH, "h": BOX_HEIGHT}


def main():
    splash_time = 2000
    opts = [arg for arg in sys.argv if arg.startswith("-")]
    if opts:
        for opt in opts:
            if opt.split("=")[0] not in VALID_OPTS:
                raise SystemExit(f"Usage: {sys.argv[0]} (--splash-time=1000)")
            else:
                if opt.startswith("--splash-time"):
                    splash_time = int(opt.split("=")[1])

    wrapper(start, splash_time)


if __name__ == "__main__":
    main()


#  rtiusdfknadfkgn
