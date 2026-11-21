"""Lane r1052: decide one packing by both methods and compare them everywhere.

The verdict is ACCEPT only when both methods find every square a unit square, no square
crossing a wall, every square inside the box with area exactly 1 (method B), no pair
overlapping, and the two methods agree on every square's unit test, every wall's class
and clearance, and every pair's class; and, for every pair apart, method B's squared
Euclidean gap is at least the square of method A's margin, as it must be. No pair is
skipped and nothing is rounded.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any

import r1052_clip as clip
import r1052_poses as poses_a

WALLS = ("left", "bottom", "right", "top")


def decide(
    side: Fraction,
    *,
    poses: list[tuple[Fraction, Fraction, Fraction, Fraction]] | None = None,
    corners: list[list[tuple[Fraction, Fraction]]] | None = None,
    distance: bool = True,
) -> dict[str, Any]:
    a = poses_a.run(side, poses=poses, corners=corners)
    b = clip.run(side, poses=poses, corners=corners, distance=distance)
    n = a["n"]
    problems: list[str] = []
    disagreements: list[str] = []
    for k in range(n):
        if a["unit"][k] != b["unit"][k]:
            disagreements.append(f"square {k + 1}: unit A {a['unit'][k]} B {b['unit'][k]}")
        if not a["unit"][k] or not b["unit"][k]:
            problems.append(f"square {k + 1}: not a unit square")
    wall_rows: list[dict[str, Any] | None] = []
    for k in range(n):
        wa, wb = a["walls"][k], b["walls"][k]
        if wa is None or wb is None:
            wall_rows.append(None)
            continue
        row: dict[str, Any] = {"clearances": wa, "classes": {}}
        for w, name in enumerate(WALLS):
            ca = poses_a.wall_class(wa[w])
            cb = wb["classes"][name]
            row["classes"][name] = ca
            if ca != cb:
                disagreements.append(f"square {k + 1} {name}: A {ca} B {cb}")
            if clip.fr(wb["clearances"][w]) != wa[w]:
                disagreements.append(f"square {k + 1} {name}: clearances differ")
            if ca == "crossing":
                problems.append(f"square {k + 1}: crosses the {name} wall by {-wa[w]}")
        inside = clip.fr(wb["inside2"]) / 2
        row["inside_area"] = inside
        if inside != 1:
            problems.append(f"square {k + 1}: area {inside} inside the box")
        wall_rows.append(row)
    pair_rows: dict[tuple[int, int], tuple[Fraction, str, Fraction | None, Fraction]] = {}
    if set(a["margins"]) != set(b["pairs"]):
        disagreements.append("the methods decided different sets of pairs")
    for key, m in a["margins"].items():
        cls_a = poses_a.classify(m)
        got = b["pairs"].get(key)
        if got is None:
            continue
        cls_b, area2, g2 = got
        if cls_a != cls_b:
            disagreements.append(f"pair {key[0] + 1},{key[1] + 1}: A {cls_a} B {cls_b}")
        g = clip.fr(g2) if g2 is not None else None
        if cls_a == "apart" and g is not None and g < m * m:
            disagreements.append(f"pair {key[0] + 1},{key[1] + 1}: B's gap below A's margin")
        if cls_a == "overlap":
            problems.append(f"pair {key[0] + 1},{key[1] + 1}: overlap, margin {m}")
        pair_rows[key] = (m, cls_a, g, clip.fr(area2) / 2)
    verdict = "ACCEPT" if not problems and not disagreements else "REFUSE"
    return {
        "verdict": verdict,
        "n": n,
        "problems": problems,
        "disagreements": disagreements,
        "unit_a": a["unit"],
        "unit_b": b["unit"],
        "sense": b["sense"],
        "walls": wall_rows,
        "pairs": pair_rows,
    }
