from typing import Any, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from _curses import _CursesWindow

    Window = _CursesWindow
else:
    Window = Any

MenuName = Literal["start", "play", "generate", "solve"]
MenuEntry = tuple[int, MenuName, str]
Quit = Literal["quit"]
Dimensions = tuple[int, int]  # height, width
Justify = Literal["left", "right"]
