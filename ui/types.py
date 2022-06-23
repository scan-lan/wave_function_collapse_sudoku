from typing import Any, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from _curses import _CursesWindow

    Window = _CursesWindow
else:
    Window = Any

Menu = Literal["start", "play", "generate", "solve"]
Dimensions = tuple[int, int]  # height, width
