import shutil
from collections.abc import Callable
from math import ceil
from typing import Self

from screen import Screen

# pyright: strict

WIDTH, HEIGHT = shutil.get_terminal_size()


class Pixel:
    def __init__(self, r: int, g: int, b: int, brightness: float = 1) -> None:
        self._r = r
        self._g = g
        self._b = b
        self._brightness: float = brightness
        self._changed = True

    @property
    def brightness(self) -> float:
        return self._brightness

    @brightness.setter
    def brightness(self, f: float) -> None:
        self.changed = True
        self._brightness = f
        assert (
            self.brightness >= 0
        ), "brightnesss must be greater than or equal to zero"

    @property
    def changed(self) -> bool:
        return self._changed

    @changed.setter
    def changed(self, b: bool) -> None:
        self._changed = b

    def get_rgb(self) -> tuple[int, int, int]:
        return (
            round(self._r * self.brightness),
            round(self._g * self.brightness),
            round(self._b * self.brightness),
        )

    def set_rgb(self, r: int, g: int, b: int) -> None:
        self._r = r
        self._g = g
        self._b = b
        self.changed = True

    def __repr__(self) -> str:
        return f"Color({self._r}, {self._g}, {self._b})"

    def __str__(self) -> str:
        return str((self._r, self._g, self._b))


class PixelDrawer:
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
        self._pixel_array = [Pixel(0, 0, 0) for _ in range(n)]

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

    def fill(self, r: int, g: int, b: int, brightness: float = 1) -> None:
        self._pixel_array = [
            Pixel(r, g, b, brightness) for _ in range(len(self))
        ]

    def show(self) -> None:
        x = len(self.header) + 1
        for p in self._pixel_array:
            y = ceil(x / WIDTH)
            if p.changed:
                self._screen.set_cursor(x % WIDTH, y)
                self._screen.print_color(self.pix_str, *p.get_rgb())
                p.changed = False
            x += len(self.pix_str)
        self._screen.flush()

    def run(self, program: Callable[[Self], None]) -> None:
        program(self)

    def __getitem__(self, i: int) -> Pixel:
        return self._pixel_array[i]

    def __setitem__(self, i: int, pixel: Pixel) -> None:
        self._pixel_array[i] = pixel

    def __iter__(self):
        i = 0
        while i < len(self):
            yield self[i]
            i += 1

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
