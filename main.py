#!/usr/bin/env python3
import sys
from time import sleep

import pixels


def static(pix: pixels.Pixels) -> None:
    pix[3] = pixels.Color(100, 20, 255)
    pix.show()
    input()


def cycle(pix: pixels.Pixels) -> None:
    delta = 255 / len(pix)
    while True:
        pix.fill(pixels.Color(0, 0, 0))
        for i in range(len(pix)):
            pix[i] = pixels.Color(int((i + 1) * delta), 0, 100)
            pix.show()
            sleep(0.02)


def brightness(pix: pixels.Pixels) -> None:
    delta = 1 / len(pix)
    while True:
        pix.fill(pixels.Color(255, 0, 0))
        pix.show()
        input()
        # pix[0] = pixels.Color(100, 0, 0)
        for i in range(len(pix)):
            pix[i]._b = 255
        for c in pix:
            sys.stderr.write(f"{c.get_rgb()}\n")
        pix.show()
        input()
        continue
        for i, c in enumerate(pix):
            pix[i].brightness = (i + 1) * delta
            pix.show()
            sleep(0.04)


def main() -> None:
    with pixels.Pixels(500) as pix:
        try:
            brightness(pix)
        except KeyboardInterrupt:
            print()


if __name__ == "__main__":
    main()
