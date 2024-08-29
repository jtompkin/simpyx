from typing import TextIO
import sys


class Screen:
    def __init__(self, file: TextIO = sys.stdout) -> None:
        self._file = file

    def clear(self):
        self._file.write("\x1b[2J")

    def hide_cursor(self) -> None:
        self._file.write("\x1b[?25l")

    def show_cursor(self) -> None:
        self._file.write("\x1b[?25h")

    def set_cursor(self, x: int = 1, y: int = 1) -> None:
        self._file.write(f"\x1b[{y};{x}H")

    def print_color(self, msg: str, r: int, g: int, b: int) -> None:
        self._file.write(f"\x1b[38;2;{r};{g};{b}m{msg}")

    def print(self, msg: str) -> int:
        return self._file.write(msg)

    def flush(self) -> None:
        self._file.flush()

    def __enter__(self):
        return self

    def __exit__(self) -> None:
        self.flush()
        self.show_cursor()
        self._file.close()
