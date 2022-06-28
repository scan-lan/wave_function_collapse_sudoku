from typing import Optional


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
