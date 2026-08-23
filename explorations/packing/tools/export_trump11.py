#!/usr/bin/env python3
"""Export Walter Trump's exact n = 11 packing as f64 poses, for seeding the search.

The packing lives in the degree-8 field Q(u); the search works in f64. This is the
one-way door between them, and it is a *tool*, never a verifier: nothing downstream
of this file may claim a record, because the conversion has already thrown away the
exactness that a record claim needs.

Emits {"x": [...], "y": [...], "t": [...]} plus the side, and asserts the round trip
is faithful to the tolerance the search screens at.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqpack.packings.trump11 import build

DIGITS = 40


def approx(element, u: float) -> float:
    """Evaluate a field element at the numeric root, low-order coefficient first."""
    return sum(float(c) * u**i for i, c in enumerate(element.coeffs))


def main() -> int:
    squares, side, field = build()
    field.refine_to(DIGITS)
    u = float((field._lo + field._hi) / 2)

    xs, ys, ts = [], [], []
    for corners in squares:
        px = [approx(c[0], u) for c in corners]
        py = [approx(c[1], u) for c in corners]
        # Centre is the corner mean; the angle comes from the first edge, folded into
        # [0, pi/2) because a unit square is invariant under a quarter turn.
        cx, cy = sum(px) / 4, sum(py) / 4
        angle = math.atan2(py[1] - py[0], px[1] - px[0]) % (math.pi / 2)
        # Edge lengths must be 1: the check that the conversion read the geometry right.
        for i in range(4):
            j = (i + 1) % 4
            edge = math.hypot(px[j] - px[i], py[j] - py[i])
            assert abs(edge - 1.0) < 1e-12, f"edge {edge} is not unit"
        xs.append(cx)
        ys.append(cy)
        ts.append(angle)

    side_f = approx(side, u)
    span_x = max(x + 0.5 * (abs(math.cos(t)) + abs(math.sin(t))) for x, t in zip(xs, ts)) - min(
        x - 0.5 * (abs(math.cos(t)) + abs(math.sin(t))) for x, t in zip(xs, ts)
    )
    span_y = max(y + 0.5 * (abs(math.cos(t)) + abs(math.sin(t))) for y, t in zip(ys, ts)) - min(
        y - 0.5 * (abs(math.cos(t)) + abs(math.sin(t))) for y, t in zip(ys, ts)
    )
    required = max(span_x, span_y)
    assert abs(required - side_f) < 1e-12, f"bounding box {required} != published side {side_f}"

    json.dump(
        {"n": len(xs), "side": side_f, "x": xs, "y": ys, "t": ts},
        sys.stdout,
        indent=1,
    )
    print()
    print(
        f"# side {side_f:.15f}, bounding box {required:.15f}, "
        f"distinct angles {sorted({round(t, 9) for t in ts})}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
