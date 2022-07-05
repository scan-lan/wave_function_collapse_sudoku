import curses
from typing import Iterable, Optional

from ui.align import centre_x, centre_y
from ui.types import Justify, Window


def add_status_message(
    screen: Window, status_message: str, justify: Justify = "left", start_x: int = 0
) -> None:
    if justify == "right":
        start_x = curses.COLS - 1 - len(status_message)
    screen.attron(curses.A_REVERSE)
    screen.addstr(curses.LINES - 1, start_x, status_message, curses.A_REVERSE)
    screen.attroff(curses.A_REVERSE)
    screen.noutrefresh()


def add_title(
    screen: Window,
    title_str: str,
    tagline_str: Optional[str] = None,
    pad_args: Optional[Iterable[int]] = None,
    start_y: Optional[int] = None,
    start_x: Optional[int] = None,
):
    title_string_length = max([len(line) for line in title_str.splitlines()])
    num_lines_vertical = len(title_str.splitlines())
    if start_y is None:
        start_y = centre_y(curses.LINES, num_lines=num_lines_vertical)
    if start_x is None:
        start_x = centre_x(curses.COLS, str_len=title_string_length)

    for i, line in enumerate(title_str.splitlines()):
        screen.addstr(start_y + i, start_x, line)

    if tagline_str is not None:
        tagline_start_x = centre_x(curses.COLS, tagline_str)
        tagline_start_y = start_y + num_lines_vertical + 2
        screen.addstr(tagline_start_y, tagline_start_x, tagline_str)
    if pad_args is None:
        screen.noutrefresh()
    else:
        screen.noutrefresh(0, 0, 0, 0, 22, 79)
