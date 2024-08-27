class Color:
    def __init__(self, red: int, blue: int, green: int) -> None:
        self.r = red
        self.g = green
        self.b = blue

    def __repr__(self) -> str:
        return f"Color(({self.r}, {self.g}, {self.b}))"

    def __str__(self) -> str:
        return str((self.r, self.g, self.b))


class Pixels:
    def __init__(
        self, n: int, fill: Color = Color(0, 0, 0), auto_show: bool = False
    ) -> None:
        self._array: list[Color] = [fill] * n
        self.auto_show = auto_show

    def fill(self, color: Color) -> None:
        self._array = [color] * len(self)
        if self.auto_show:
            self.show()

    def off(self) -> None:
        self._array = [Color(0, 0, 0)] * len(self)
        self.show()

    def show(self) -> None:
        print("\x1b[2J\x1b[1;1H", end="")
        for c in self._array:
            print(f"\x1b[38;2;{c.r};{c.g};{c.b}m■ ", end="")
        print()

    def __getitem__(self, i: int) -> Color:
        return self._array[i]

    def __setitem__(self, i: int, c: Color) -> None:
        self._array[i] = c
        if self.auto_show:
            self.show()

    def __len__(self) -> int:
        return len(self._array)

    def __repr__(self) -> str:
        return f"Pixels({len(self)})"

    def __str__(self) -> str:
        return str(self._array)
