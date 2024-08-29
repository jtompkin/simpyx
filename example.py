#!/usr/bin/env python3
import argparse

from simpyx import shows, pixels


def _positive_int(s: str) -> int:
    if (arg := int(s)) < 1:
        raise argparse.ArgumentTypeError("must be an integer greater than 0")
    return arg


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="simpyx", description="Simulate neopixels in the terminal."
    )
    parser.add_argument(
        "-n",
        type=_positive_int,
        default=100,
        help="Provide the number of pixels to simulate.",
    )
    args = parser.parse_args(argv)
    with pixels.PixelDrawer(args.n) as pixel_drawer:
        shows.cycle(pixel_drawer)


if __name__ == "__main__":
    main()
