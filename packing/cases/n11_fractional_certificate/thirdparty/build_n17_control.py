#!/usr/bin/env python3
"""Rebuild Massaccesi's published n = 17 certificate as plain data.

Usage:
    python3 build_n17_control.py                 # print the JSON
    python3 build_n17_control.py --check FILE    # confirm FILE is what this prints

The constants below are transcribed from the verifier Gustavo Massaccesi
published on 2026-08 (a modification of Sam Burns's), at
https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html
Only the certificate's DATA is taken from that file: the container side L,
the empty border M, the shrunken side B, the net parameters T and KMAX, the
weight scale, the 29 x 29 grid coord[i] = M/2 + i (L - M) / 28, and the 23
orbit representatives (i, j, w), each of which gives weight w / 576 to every
distinct image of grid point (i, j) under the container's eight symmetries.
None of the published verification logic is reused; verify.py decides.

Expected: 168 atoms, total weight 9744/576 = 203/12, and L = 22529/5000 =
4.5058, the value the source reports. Standard library only.
"""

import json
import sys
from fractions import Fraction as F

L = F(45058, 10000)
M = F(15513, 10000)
B = F(9973, 10000)
T = F(207107, 500000)
KMAX = 180
WEIGHT_SCALE = 576
NGRID = 29
LAST = NGRID - 1

CERT = [
    (0, 2, 165),
    (0, 11, 129),
    (1, 8, 36),
    (1, 10, 21),
    (1, 11, 15),
    (2, 2, 246),
    (2, 8, 129),
    (2, 9, 105),
    (2, 10, 36),
    (2, 11, 105),
    (5, 10, 36),
    (6, 10, 63),
    (6, 11, 12),
    (7, 10, 21),
    (8, 9, 33),
    (8, 11, 15),
    (9, 11, 75),
    (9, 14, 39),
    (10, 11, 25),
    (10, 12, 21),
    (10, 13, 24),
    (10, 14, 3),
    (11, 11, 16),
]


def orbit(i, j):
    n = LAST
    return {(i, j), (n - i, j), (i, n - j), (n - i, n - j),
            (j, i), (n - j, i), (j, n - i), (n - j, n - i)}


def build():
    step = (L - M) / LAST
    coord = [M / 2 + step * i for i in range(NGRID)]
    by_index = {}
    for i, j, w in CERT:
        for ij in orbit(i, j):
            if ij in by_index:
                raise ValueError("two representatives reach grid point %s" % (ij,))
            by_index[ij] = w
    atoms = [[str(coord[i]), str(coord[j]), str(F(w, WEIGHT_SCALE))]
             for (i, j), w in sorted(by_index.items())]
    total = sum(F(w, WEIGHT_SCALE) for _, _, w in
                ((None, None, w) for w in by_index.values()))
    return {
        "id": "control-n17-massaccesi-4.5058",
        "n": 17,
        "claim": "s(17) >= %s" % L,
        "outer_side": str(L),
        "square_side": str(B),
        "angle_limit": str(T),
        "direction_steps": KMAX,
        "total_mass": str(total),
        "symmetry": "D4",
        "source": "https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html",
        "atoms": atoms,
    }


def render(record):
    return json.dumps(record, indent=1) + "\n"


def main(argv):
    text = render(build())
    if len(argv) == 3 and argv[1] == "--check":
        with open(argv[2]) as handle:
            shipped = handle.read()
        if shipped == text:
            print("control data rebuilt from the published constants: identical to %s" % argv[2])
            return 0
        print("MISMATCH: %s differs from the rebuilt control data" % argv[2])
        return 1
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
