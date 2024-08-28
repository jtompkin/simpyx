import shutil
import sys
from math import ceil
from typing import TextIO

# pyright: strict

WIDTH, HEIGHT = shutil.get_terminal_size()


class Color:
    def __init__(self, r: int, g: int, b: int) -> None:
        self._r = r
        self._g = g
        self._b = b
        self.brightness: float = 1

    def get_rgb(self) -> tuple[int, int, int]:
        assert (
            self.brightness >= 0
        ), "brightnesss must be greater than or equal to zero"
        return (
            round(self._r * self.brightness),
            round(self._g * self.brightness),
            round(self._b * self.brightness),
        )

    def __repr__(self) -> str:
        return f"Color(({self._r}, {self._g}, {self._b}))"

    def __str__(self) -> str:
        return str((self._r, self._g, self._b))


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

    def flush(self) -> None:
        self._file.flush()

    def print(self, msg: str) -> int:
        return self._file.write(msg)

    def __enter__(self):
        return self

    def __exit__(self) -> None:
        self.flush()
        self.show_cursor()
        self._file.close()


class Pixels:
    def __init__(
        self,
        n: int,
        pixel_str: str = "■ ",
        header: str = "[ ",
        footer: str = "]",
        screen: Screen | None = None,
    ) -> None:
        self.pix_str = pixel_str
        self.header = header
        self.footer = footer
        self._pixel_array = [Color(0, 0, 0)] * n
        self._changed = {i: True for i in range(len(self._pixel_array))}

        if screen is None:
            screen = Screen().__enter__()
        self._screen = screen
        self._screen.hide_cursor()
        self._screen.clear()
        self._screen.set_cursor()
        self._screen.print(self.header)
        self._screen.set_cursor(
            (len(self) + len(self.pix_str)) * len(self.pix_str) % WIDTH,
            ceil(len(self) * len(self.pix_str) / WIDTH),
        )
        self._screen.print(self.footer)

    def fill(self, color: Color) -> None:
        self._pixel_array = [color] * len(self)
        self._changed = {i: True for i in range(len(self._pixel_array))}

    def show(self) -> None:
        x = len(self.header) + 1
        for i, c in enumerate(self._pixel_array):
            y = ceil(x / WIDTH)
            if self._changed[i]:
                self._screen.set_cursor(x % WIDTH, y)
                self._screen.print_color(self.pix_str, *c.get_rgb())
                self._changed[i] = False
            x += len(self.pix_str)
        self._screen.flush()

    def __getitem__(self, i: int) -> Color:
        return self._pixel_array[i]

    def __setitem__(self, i: int, c: Color) -> None:
        self._pixel_array[i] = c
        self._changed[i] = True

    # def __iter__(self):
    #    i = 0
    #    while i < len(self):
    #        yield self[i]
    #        i += 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:  # pyright: ignore
        self._screen.__exit__()

    def __len__(self) -> int:
        return len(self._pixel_array)

    def __repr__(self) -> str:
        return (
            f"Pixels({len(self)}, {self.pix_str} ,{self.header}, {self.footer})"
        )

    def __str__(self) -> str:
        return str(self._pixel_array)
