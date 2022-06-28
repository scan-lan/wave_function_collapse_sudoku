import curses
from typing import Iterable, Optional

from ui.types import Justify, MenuEntry, MenuName, Quit, Window


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
    screen: Window, quit_message: str, justify: Justify = "left"
) -> None:
    start_x = 0
    if justify == "right":
        start_x = curses.COLS - 1 - len(quit_message)
    screen.attron(curses.A_REVERSE)
    screen.addstr(curses.LINES - 1, start_x, quit_message, curses.A_REVERSE)
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


def splash_screen(screen: Window, splash_time: int, title: str) -> None:
    title_tagline = "A puzzle experience by Luke Scanlan"

    screen.erase()
    add_title(screen, title, title_tagline)
    curses.doupdate()
    curses.napms(splash_time)


def add_menu_options(
    screen: Window,
    menus: list[MenuEntry],
    highlighted: int = 0,
    start_y: Optional[int] = None,
):
    menu_height = len(menus)
    if start_y is None:
        start_y = centre_y(curses.LINES, num_lines=menu_height)
    start_x = centre_x(curses.COLS, str_len=30)

    for i, menu in enumerate(menus):
        if i == highlighted:
            screen.attron(curses.A_UNDERLINE)
        screen.addstr(start_y + i, start_x, menu[1])
        if i == highlighted:
            screen.attroff(curses.A_UNDERLINE)

    screen.noutrefresh()


def start_menu(screen: Window, title: str) -> MenuName | Quit:
    quit_message = 'Press "q" at any time to quit'
    menus: list[MenuEntry] = [
        (0, "play", "Attempt to complete a puzzle. No hints."),
        (1, "generate", "Generate a puzzle. The meat n potatoes of the code."),
        (2, "solve", "Cheat. Humiliate your gran."),
    ]
    max_menu_index = len(menus)
    highlighted = 0
    selected = "quit"
    k = ""

    while k.lower() != "q":
        screen.erase()
        screen.noutrefresh()
        try:
            k = screen.getkey()
            if k == "\n":
                return menus[highlighted][1]
            elif k == "KEY_UP":
                highlighted = (highlighted - 1) % max_menu_index
            elif k == "KEY_DOWN":
                highlighted = (highlighted + 1) % max_menu_index
            elif k == "KEY_RESIZE":
                curses.update_lines_cols()
        except curses.error:
            pass
        screen.addstr(0, 0, k)
        add_title(screen, title, start_y=3)
        add_quit_message(screen, quit_message)
        add_menu_options(screen, menus, highlighted=highlighted)
        curses.doupdate()
    return selected


def generate_menu(screen: Window) -> bool:
    quit_message = 'Quit: "q"'
    default_message = "Use default (9x9) grid? [y/n] > (y)"
    yn_error_msg = 'Please enter "y" or "n"'
    add_status_message(screen, quit_message, justify="right")
    add_status_message(screen, default_message)
    k = ""
    screen.addstr(curses.LINES // 2, curses.COLS // 2 - 4, "GENERATE")
    box_dimensions = {"w": 3, "h": 3}

    while k.lower() != "q":
        try:
            k = screen.getkey()
        except curses.error:
            pass
        if k.lower() == "y" or k == "\n":
            create_grid(screen, box_dimensions, visualiser=show_coefs)
        curses.doupdate()
    return False


def start(screen: Window, splash_time: int):
    curses.noecho()
    curses.cbreak(True)
    curses.curs_set(0)
    screen.keypad(True)
    screen.nodelay(True)

    active = True
    big_title = """____________________________________/\\\\\\_____________________________\
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
    small_title = """                   __      __
   _______  ______/ /___  / /____  __
  / ___/ / / / __  / __ \\/ //_/ / / /
 (__  ) /_/ / /_/ / /_/ / ,< / /_/ /
/____/\\__,_/\\__,_/\\____/_/|_|\\__,_/"""

    screen.erase()
    curses.update_lines_cols()
    if curses.LINES < 25 or curses.COLS < 95:
        splash_screen(screen, splash_time, small_title)
    else:
        splash_screen(screen, splash_time, big_title)

    while active:
        next_menu = start_menu(screen, small_title)
        if next_menu == "quit":
            active = False
        elif next_menu == "play":
            screen.erase()
            screen.noutrefresh
            screen.addstr("play")
            screen.refresh()
            curses.napms(500)
        elif next_menu == "generate":
            active = generate_menu(screen)
        elif next_menu == "solve":
            screen.erase()
            screen.noutrefresh
            screen.addstr("solve")
            screen.refresh()
            curses.napms(500)

    end(screen)


def end(screen: "curses._CursesWindow"):
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()


if __name__ == "__main__":
    curses.wrapper(start)
