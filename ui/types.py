# pyright: reportPrivateUsage=false
from typing import Literal, TypeAlias
import curses  # noqa F401


MenuName: TypeAlias = Literal["start", "play", "generate", "solve"]
MenuEntry: TypeAlias = tuple[int, MenuName, str]
Quit: TypeAlias = Literal["quit"]
Justify: TypeAlias = Literal["left", "right"]
Window: TypeAlias = "curses._CursesWindow"
