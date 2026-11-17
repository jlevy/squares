"""A packing decided by both methods: every square, every wall and every pair.

Lane c-review-1009-1117, stage 4 blind review of issue #1009. Clean-room.

``decide`` is handed poses for method A and corners for method B, with the side. It
applies no distance filter and no tolerance. The verdict is ``ACCEPT`` only when both
methods accept every square, wall and pair and their classes are equal everywhere.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction

import rv1009_axes as axes
import rv1009_clip as clip
from gmpy2 import mpq

WALLS = ("left", "bottom", "right", "top")
A_CLASS = {1: "apart", 0: "touch", -1: "overlap"}


def sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def decide(
    poses: list[axes.Pose],
    quads: list[list[clip.Point]],
    side: tuple[int, int],
    *,
    keep_margins: bool = True,
    only: set[int] | None = None,
) -> dict:
    """Decide a packing. ``poses[k]`` and ``quads[k]`` describe square ``k + 1``; method A
    reads only the poses and method B only the corners.

    Returns exact facts. ``margins`` (when kept) lists every pair's margin by method A in
    the order (1,2), (1,3), ..., (n-1,n).

    With ``only`` (a set of square numbers) every square and wall is still decided, and
    of the pairs only those holding a square of the set: a partial decision, for a control
    that changes those squares and nothing else. Its verdict is ``PARTIAL`` when nothing
    it decided is refused, and its margins are in ``margins_of`` by pair.
    """
    n = len(poses)
    if len(quads) != n:
        msg = "poses and corners differ in number"
        raise ValueError(msg)
    side_q = mpq(side[0], side[1])
    problems: list[str] = []

    # squares
    unit_a = [axes.is_unit_pose(p) for p in poses]
    senses = [clip.unit_sense(q) for q in quads]
    unit_b = [s != 0 for s in senses]
    for k in range(n):
        if not unit_a[k]:
            problems.append(f"square {k + 1}: not a unit pose (A)")
        if not unit_b[k]:
            problems.append(f"square {k + 1}: not a unit square (B)")
    if problems:
        return {
            "verdict": "REFUSE",
            "n": n,
            "problems": problems,
            "not_unit_a": [k + 1 for k in range(n) if not unit_a[k]],
            "not_unit_b": [k + 1 for k in range(n) if not unit_b[k]],
        }
    ccw = [clip.counterclockwise(q) for q in quads]
    lines = [clip.edge_lines(q) for q in ccw]

    # walls
    clearances = [axes.wall_clearances(p, side) for p in poses]
    wall_b = [clip.wall_classes(q, side_q) for q in ccw]
    inside_b = [clip.area_in_box(q, side_q) for q in ccw]
    wall_disagree = []
    crossing_a = []
    touching_a = []
    not_inside_b = []
    outside_area = mpq(0)
    for k in range(n):
        for w in range(4):
            cls_a = A_CLASS[sign(clearances[k][w])]
            cls_b, area = wall_b[k][w]
            outside_area += area
            if cls_a != cls_b:
                wall_disagree.append((k + 1, WALLS[w], cls_a, cls_b))
            if cls_a == "overlap":
                crossing_a.append((k + 1, WALLS[w]))
            elif cls_a == "touch":
                touching_a.append((k + 1, WALLS[w]))
        if inside_b[k] != 1:
            not_inside_b.append(k + 1)
    crossing_squares = sorted({k for k, _w in crossing_a})
    if crossing_squares != not_inside_b:
        problems.append("containment by area (B) and by clearance (A) differ")
    if wall_disagree:
        problems.append(f"{len(wall_disagree)} wall classes differ between A and B")

    # pairs
    margins: list[Fraction] = []
    margins_of: dict[tuple[int, int], Fraction] = {}
    decided = 0
    counts_a = {"apart": 0, "touch": 0, "overlap": 0}
    counts_b = {"apart": 0, "touch": 0, "overlap": 0}
    pair_disagree = []
    overlapping = []
    touching = []
    overlap_area = mpq(0)
    least = None
    least_pair = None
    digest = hashlib.sha256()
    for i in range(n):
        pi = poses[i]
        qi = ccw[i]
        for j in range(i + 1, n):
            if only is not None and i + 1 not in only and j + 1 not in only:
                continue
            decided += 1
            m = axes.pair_margin(pi, poses[j])
            cls_a = A_CLASS[sign(m)]
            cls_b, area = clip.pair_class(qi, ccw[j], lines[i], lines[j])
            counts_a[cls_a] += 1
            counts_b[cls_b] += 1
            overlap_area += area
            if cls_a != cls_b:
                pair_disagree.append((i + 1, j + 1, cls_a, cls_b))
            if cls_a == "overlap":
                overlapping.append((i + 1, j + 1))
            elif cls_a == "touch":
                touching.append((i + 1, j + 1))
            if least is None or m < least:
                least = m
                least_pair = (i + 1, j + 1)
            digest.update(f"{i + 1} {j + 1} {m.numerator}/{m.denominator}\n".encode())
            if only is not None:
                margins_of[(i + 1, j + 1)] = m
            elif keep_margins:
                margins.append(m)
    if pair_disagree:
        problems.append(f"{len(pair_disagree)} pair classes differ between A and B")

    accept = (
        not problems
        and not crossing_a
        and not not_inside_b
        and not overlapping
        and counts_b["overlap"] == 0
    )
    least_wall = []
    for w in range(4):
        value = min(clearances[k][w] for k in range(n))
        least_wall.append((value, [k + 1 for k in range(n) if clearances[k][w] == value]))
    if not accept:
        verdict = "REFUSE"
    else:
        verdict = "ACCEPT" if only is None else "PARTIAL"
    return {
        "verdict": verdict,
        "n": n,
        "pairs_decided": decided,
        "margins_of": margins_of if only is not None else None,
        "problems": problems,
        "senses": senses,
        "clearances": clearances,
        "least_wall": least_wall,
        "wall_touching": touching_a,
        "wall_crossing": crossing_a,
        "wall_disagree": wall_disagree,
        "not_inside_b": not_inside_b,
        "area_outside_b": outside_area,
        "pairs": n * (n - 1) // 2,
        "pair_counts_a": counts_a,
        "pair_counts_b": counts_b,
        "pair_disagree": pair_disagree,
        "pair_touching": touching,
        "pair_overlapping": overlapping,
        "overlap_area_b": overlap_area,
        "least_margin": least,
        "least_pair": least_pair,
        "margins": margins if keep_margins and only is None else None,
        "margins_sha256": digest.hexdigest() if only is None else None,
    }


def pair_index(n: int, i: int, j: int) -> int:
    """The position of pair (i, j), 1 <= i < j <= n, in the order ``decide`` lists."""
    i0 = i - 1
    return i0 * n - i0 * (i0 + 1) // 2 + (j - i - 1)
