#!/usr/bin/env python3
import argparse
from time import sleep

import pixels


def static(pix: pixels.PixelDrawer) -> None:
    pix[3] = pixels.Pixel(100, 20, 255)
    pix.show()
    input()


def cycle(pix: pixels.PixelDrawer) -> None:
    delta = 255 / len(pix)
    while True:
        for i, p in enumerate(pix):
            p.set_rgb(round((i + 1) * delta), 0, 100)
            pix.show()
            sleep(0.02)
        pix.fill(0, 0, 0)
        pix.show()


def brightness(pix: pixels.PixelDrawer) -> None:
    delta = 1 / len(pix)
    while True:
        pix.fill(255, 0, 0)
        pix.show()
        for i, p in enumerate(pix):
            p.brightness = (i + 1) * delta
            pix.show()
            sleep(0.04)


def main() -> None:
    with pixels.PixelDrawer(100) as pix:
        try:
            cycle(pix)
        except KeyboardInterrupt:
            print()


if __name__ == "__main__":
    main()
