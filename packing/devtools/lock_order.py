#!/usr/bin/env python3
"""The order a packing assembles itself in, outside in, axis-aligned first.

An animation that moves every square at once reads as a crossfade. One that locks squares
into their final places in a legible order reads as the packing being *built*, and the
order that makes sense is the one the geometry suggests.

**Phase one: the squares that sit square to the container**, locked outside in -- corners
first, then edges, then any axis-aligned square further in. These are the majority at every
record measured here: 6 of 11, 10 of 17, 17 of 26, 22 of 37. Their positions are the ones a
viewer can predict, so locking them first is both the clearest thing to watch and the least
surprising.

**Phase two: everything else**, the tilted core, which adapts to the frame the first phase
built and is then forced home.

The same ordering is a candidate search strategy rather than only a way to draw one, which
is the more interesting reason to have it: if the axis-aligned majority can be placed by
construction and only the tilted remainder needs searching, the space a search has to cover
shrinks by more than half at every record above.
"""

from __future__ import annotations

import argparse
import math

from devtools.divide_and_concur import Array
from devtools.known_structure import record

SQUARE_TO_THE_WALL = 1e-9
"""How near an angle must be to a quarter turn to count as square to the container. The
records are exact: an axis-aligned square at a record is axis-aligned to the last digit,
not approximately, so this needs no tolerance beyond floating-point noise."""


def is_axis_aligned(angle: float, tol: float = SQUARE_TO_THE_WALL) -> bool:
    residual = abs(angle) % (math.pi / 2)
    return min(residual, math.pi / 2 - residual) < tol


def lock_order(poses: Array, side: float) -> list[int]:
    """Indices in the order they should lock: axis-aligned outside in, then the rest.

    Distance to the nearest wall is what "outside in" means, so a square in a corner --
    near two walls at once -- comes before one merely against an edge, and both come before
    anything floating in the middle.
    """

    def edge_distance(pose) -> float:
        return min(pose[0] - 0.5, pose[1] - 0.5, side - 0.5 - pose[0], side - 0.5 - pose[1])

    aligned = [i for i, p in enumerate(poses) if is_axis_aligned(float(p[2]))]
    tilted = [i for i in range(len(poses)) if i not in set(aligned)]
    aligned.sort(
        key=lambda i: (edge_distance(poses[i]), float(poses[i][0]), float(poses[i][1]))
    )
    tilted.sort(key=lambda i: (edge_distance(poses[i]), float(poses[i][0]), float(poses[i][1])))
    return aligned + tilted


def phases(poses: Array) -> tuple[list[int], list[int]]:
    """The two groups, as the owner's scheme describes them."""
    aligned = [i for i, p in enumerate(poses) if is_axis_aligned(float(p[2]))]
    return aligned, [i for i in range(len(poses)) if i not in set(aligned)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, nargs="+", default=[11, 17, 26, 29, 37])
    o = ap.parse_args()
    print(
        f"{'n':>4} {'square to wall':>15} {'tilted':>7} {'locks first':>12} {'locks last':>11}"
    )
    for n in o.n:
        poses, side = record(n)
        aligned, tilted = phases(poses)
        order = lock_order(poses, side)
        print(f"{n:>4} {len(aligned):>15} {len(tilted):>7} {order[0]:>12} {order[-1]:>11}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
