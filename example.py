#!/usr/bin/env python3
# Copyright 2024 Josh Tompkin
# Licensed under the MIT license

import argparse
import time

from simpyx import shows, pixels


def _positive_int(s: str) -> int:
    if (arg := int(s)) < 1:
        raise argparse.ArgumentTypeError("must be an integer greater than 0")
    return arg


def loop(pix_drawer: pixels.PixelDrawer, delay: float) -> None:
    delta = 1 / len(pix_drawer)
    while True:
        pix_drawer.fill(0, 255, 0, 0)
        for i, p in enumerate(pix_drawer):
            p.brightness = (i + 1) * delta
            pix_drawer.show()
            time.sleep(delay)
        pix_drawer.redraw()


def cycle(pix_drawer: pixels.PixelDrawer, delay: float) -> None:
    delta = 255 / len(pix_drawer)
    while True:
        pix_drawer.redraw()
        pix_drawer.fill(0, 0, 0)
        pix_drawer.show()
        for i, p in enumerate(pix_drawer):
            p.set_rgb(round((i + 1) * delta), 0, 100)
            pix_drawer.show()
            time.sleep(delay)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="simpyx", description="Simulate neopixels in the terminal."
    )
    parser.add_argument(
        "-n",
        type=_positive_int,
        default=100,
        help="Specify the number of pixels to simulate.",
    )
    args = parser.parse_args(argv)
    try:
        with pixels.PixelDrawer(args.n, "■") as pixel_drawer:
            cycle(pixel_drawer, 0.03)
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
