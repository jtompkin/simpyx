#!/usr/bin/env python3
import time

import pixels


DELAY = 0.05
N = 60


def main() -> None:
    pix = pixels.Pixels(N)
    delta = 255 // len(pix)
    toggle = True
    offset = {True: 0, False: len(pix) - 1}
    while True:
        for i in range(len(pix)):
            pix[i - offset[toggle]] = pixels.Color(
                i * delta, 255 - i * delta, 50
            )
            pix.show()
            time.sleep(DELAY)
        pix.off()
        toggle = not toggle


if __name__ == "__main__":
    main()
