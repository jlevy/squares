"""Compare two rational centre-basis witnesses (Witness/v2) as packings.

For each of the box's 8 symmetries, match every square of A to the nearest unused square
of B, greedily, and report the best symmetry's largest centre displacement and how many
squares lie within 1e-6, 1e-3 and 0.1. A geometric measurement only; it decides nothing.
Each argument is a repository-relative path to a fact, `.yaml` or `.yaml.gz`.

The review of 2026-10-14 compared #573's 153 and 207 with PingYou Ltd's T-148 and T-147
(`compare_geometry-output.txt`). #573's facts are in the mishapolk lane's packet
`mishapolk-exact-certificates-2026-10-12`, on its branch and not on `main` when this copy
was made, so that output is retained; T-148's and T-147's facts are on `main`.

From `packing/`, with the project interpreter::

    python campaign/issue-intake/upper-bounds-20261014/review/compare_geometry.py A B
"""

from __future__ import annotations

import gzip
import math
import sys
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml

#: The repository root: this file is packing/campaign/issue-intake/<directory>/review/.
REPO = Path(__file__).resolve().parents[5]
Point = tuple[Fraction, Fraction]


def load(path: Path) -> tuple[Fraction, list[Point]]:
    raw = path.read_bytes()
    text = gzip.decompress(raw).decode("utf-8") if path.suffix == ".gz" else raw.decode("utf-8")
    witness: dict[str, Any] = yaml.safe_load(text)["witness"]
    side = witness["side"]
    if isinstance(side, list):
        interval = witness["scalar"]["isolating_interval"]
        side = (Fraction(interval[0]) + Fraction(interval[1])) / 2
    squares = []
    for square in witness["squares"]:
        centre = square["center"]
        if isinstance(centre[0], list):
            raise SystemExit(f"{path}: algebraic coordinates, not compared")
        squares.append((Fraction(centre[0]), Fraction(centre[1])))
    return Fraction(side), squares


def symmetries(side: Fraction) -> list[Callable[[Fraction, Fraction], Point]]:
    return [
        lambda x, y: (x, y),
        lambda x, y: (side - x, y),
        lambda x, y: (x, side - y),
        lambda x, y: (side - x, side - y),
        lambda x, y: (y, x),
        lambda x, y: (side - y, x),
        lambda x, y: (y, side - x),
        lambda x, y: (side - y, side - x),
    ]


def matched(points: list[Point], others: list[Point]) -> list[float]:
    """Each point's distance to the nearest point of ``others`` not yet taken."""
    used: set[int] = set()
    distances = []
    for x, y in points:
        index, distance = min(
            (
                (j, math.hypot(float(x - other_x), float(y - other_y)))
                for j, (other_x, other_y) in enumerate(others)
                if j not in used
            ),
            key=lambda pair: pair[1],
        )
        used.add(index)
        distances.append(distance)
    return distances


def compare(first: Path, second: Path) -> str:
    side_a, squares_a = load(first)
    side_b, squares_b = load(second)
    best: tuple[int, float, list[float]] | None = None
    for index, transform in enumerate(symmetries(side_a)):
        distances = matched([transform(x, y) for x, y in squares_a], squares_b)
        if best is None or max(distances) < best[1]:
            best = (index, max(distances), distances)
    assert best is not None
    index, largest, distances = best
    within = [sum(d < tolerance for d in distances) for tolerance in (1e-6, 1e-3, 0.1)]
    return (
        f"{first.name} vs {second.name}: sides {float(side_a):.15f} vs {float(side_b):.15f} "
        f"(diff {float(side_a - side_b):.3e}); best symmetry {index}: max centre distance "
        f"{largest:.3e}; within 1e-6: {within[0]}, within 1e-3: {within[1]}, within 0.1: "
        f"{within[2]} of {len(squares_a)}"
    )


if __name__ == "__main__":
    print(compare(REPO / sys.argv[1], REPO / sys.argv[2]))
