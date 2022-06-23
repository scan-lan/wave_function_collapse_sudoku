import curses
from typing import Optional

from ui.types import Dimensions, Window


def centre_x(
    width: int, string: Optional[str] = None, str_len: Optional[int] = None
) -> int:
    if string is not None:
        return width // 2 - len(string) // 2
    elif str_len is not None:
        return width // 2 - str_len // 2
    else:
        return width // 2


def centre_y(
    height: int, string: Optional[str] = None, num_lines: Optional[int] = None
) -> int:
    if num_lines is not None:
        return height // 2 - num_lines
    elif string is not None:
        num_lines = len(string.splitlines())
        return height // 2 - num_lines
    else:
        return height // 2


def add_quit_message(
    screen: Window, terminal_size: Dimensions, quit_message: str
) -> None:
    height, width = terminal_size
    screen.addstr(height - 1, 0, quit_message)
    screen.chgat(height - 1, 0, width, curses.A_REVERSE)


def add_title(
    screen: Window,
    terminal_size: Dimensions,
    title_str: str,
    tagline_str: Optional[str] = None,
):
    height, width = terminal_size
    title_string_length = max([len(line) for line in title_str.splitlines()])
    num_lines_vertical = len(title_str.splitlines())
    title_start_y = centre_y(height, num_lines=num_lines_vertical)
    title_x = centre_x(width, str_len=title_string_length)

    for i, line in enumerate(title_str.splitlines()):
        screen.addstr(title_start_y + i, title_x, line, curses.A_BLINK)

    if tagline_str is not None:
        tagline_start_x = centre_x(width, tagline_str)
        tagline_start_y = title_start_y + num_lines_vertical + 2
        screen.addstr(tagline_start_y, tagline_start_x, tagline_str)


def splash_screen(screen: Window, terminal_size: Dimensions, splash_time: int) -> None:
    height, width = terminal_size
    title = """____________________________________/\\\\\\_____________________________\
_______________
 ___________________________________\\/\\\\\\_________________/\\\\\\__________________\
_____
  ___________________________________\\/\\\\\\________________\\/\\\\\\________________\
_______
   __/\\\\\\\\\\\\\\\\\\\\__/\\\\\\____/\\\\\\________\\/\\\\\\______/\\\\\\\\\\____\\/\
\\\\\\\\\\\\\\\\_____/\\\\\\____/\\\\\\_
    _\\/\\\\\\//////__\\/\\\\\\___\\/\\\\\\___/\\\\\\\\\\\\\\\\\\____/\\\\\\///\\\\\\__\
\\/\\\\\\////\\\\\\__\\/\\\\\\___\\/\\\\\\_
     _\\/\\\\\\\\\\\\\\\\\\\\_\\/\\\\\\___\\/\\\\\\__/\\\\\\////\\\\\\___/\\\\\\__\\//\
\\\\\\_\\/\\\\\\\\\\\\\\\\/___\\/\\\\\\___\\/\\\\\\_
      _\\////////\\\\\\_\\/\\\\\\___\\/\\\\\\_\\/\\\\\\__\\/\\\\\\__\\//\\\\\\__/\\\\\\\
__\\/\\\\\\///\\\\\\___\\/\\\\\\___\\/\\\\\\_
       __/\\\\\\\\\\\\\\\\\\\\_\\//\\\\\\\\\\\\\\\\\\__\\//\\\\\\\\\\\\\\/\\\\__\\///\\\
\\\\\\\\/___\\/\\\\\\_\\///\\\\\\_\\//\\\\\\\\\\\\\\\\\\__
        _\\//////////___\\/////////____\\///////\\//_____\\/////_____\\///____\\///___\
\\/////////___"""

    title_tagline = "A puzzle experience by Luke Scanlan"

    if width < 95 or height < 25:
        title = """                   __      __
   _______  ______/ /___  / /____  __
  / ___/ / / / __  / __ \\/ //_/ / / /
 (__  ) /_/ / /_/ / /_/ / ,< / /_/ /
/____/\\__,_/\\__,_/\\____/_/|_|\\__,_/"""

    screen.erase()
    curses.curs_set(0)
    add_title(screen, terminal_size, title, title_tagline)
    screen.refresh()
    curses.doupdate()
    curses.napms(splash_time)


def show_start_menu(screen: Window, terminal_size: Dimensions):
    quit_message = 'Press "q" at any time to quit'

    screen.erase()
    add_quit_message(screen, terminal_size, quit_message)
    curses.doupdate()

    k = screen.getch()
    return k


def start(screen: Window, splash_time: int = 2000):
    curses.noecho()
    screen.keypad(True)
    active = True
    cursor_y = 0
    cursor_x = 0

    screen.erase()
    while active:
        terminal_size = screen.getmaxyx()
        screen.move(cursor_y, cursor_x)
        splash_screen(screen, terminal_size, splash_time)
        next_menu = show_start_menu(screen, terminal_size)

        if next_menu == ord("q"):
            active = False

    end(screen)


def end(screen: "curses._CursesWindow"):
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()


if __name__ == "__main__":
    curses.wrapper(start)
