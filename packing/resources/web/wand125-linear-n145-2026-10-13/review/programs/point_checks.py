"""Exact captures of the linear measure at a few centres of chosen net angles.

Usage: ``python3 -I point_checks.py CANDIDATE.json ANGLE [ANGLE ...]``

At each angle it evaluates, exactly and apart from every checker, the mass the closed core
captures at five centres of Tokoharu's domain: the container's centre, the domain's far
corner, the two edge midpoints and the quadrant's centre. A capture below one at any of
them would refute the certificate at that angle; captures at or above one decide nothing,
since the claim is over every centre. It prints the five captures and their least.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import linear_exact as exact


def main(argv: list[str]) -> int:
    candidate = exact.load_json(Path(argv[1]).read_bytes())
    measure = exact.read_measure(candidate)
    half = measure.side / 2
    outcome = []
    for index in (int(value) for value in argv[2:]):
        width = exact.half_width(measure, index)
        poses = {
            "centre": (half, half),
            "far_corner": (half + width, half + width),
            "edge_x": (half + width, half),
            "edge_y": (half, half + width),
            "quadrant_centre": (half + width / 2, half + width / 2),
        }
        captures = {name: exact.capture(measure, x, y, index) for name, (x, y) in poses.items()}
        outcome.append(
            {
                "angle": index,
                "half_width": str(width),
                "captures": {name: float(value) for name, value in captures.items()},
                "least": float(min(captures.values())),
                "all_at_least_1": all(value >= 1 for value in captures.values()),
            }
        )
    sys.stdout.write(
        json.dumps({"n": measure.n, "L": str(measure.side), "angles": outcome}, indent=1) + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
