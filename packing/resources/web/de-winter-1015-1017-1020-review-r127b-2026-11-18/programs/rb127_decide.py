"""Decide a packing by both methods, every square, wall and pair (lane r127b-1118).

Method A (``rb127_axes``) is handed poses, method B (``rb127_clip``) corners; nothing
else passes between them. There is no distance filter and no tolerance.

The verdict is ``ACCEPT`` only when every square is a unit square by both methods, every
square lies in the box by both (A: four clearances at least 0; B: no wall crossed and
area exactly 1 inside), every pair has disjoint interiors by both (A: margin at least 0;
B: no overlap), the two methods give the same class at every wall and every pair, and
method B's two clippings of every pair agree. A decision restricted to some squares and
pairs is ``PARTIAL`` when all of those hold on what it decided, else ``REFUSE``.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from typing import Any

from gmpy2 import mpq

import rb127_axes as A
import rb127_clip as B

Q = tuple[int, int]
A_WALL = {1: "clear", 0: "touch", -1: "cross"}
B_WALL = {"apart": "clear", "contact": "touch", "overlap": "cross"}
A_PAIR = {1: "apart", 0: "contact", -1: "overlap"}


def _sign(f: Fraction) -> int:
    return (f > 0) - (f < 0)


def prepare(poses: list[tuple[Q, Q, Q, Q]], corners: list[tuple[tuple[Q, Q], ...]]) -> dict[str, Any]:
    ip = [A.to_ipose(*row) for row in poses]
    pts = [B.to_points(c) for c in corners]
    unit_a = [A.is_unit(p) for p in ip]
    unit_b = []
    ccw_pts = []
    senses = []
    for p in pts:
        ok, sense = B.unit_square(p)
        unit_b.append(ok)
        senses.append(sense)
        ccw_pts.append(B.ccw(p, sense) if ok else p)
    return {"ip": ip, "pts": ccw_pts, "unit_a": unit_a, "unit_b": unit_b, "senses": senses}


def decide(
    poses: list[tuple[Q, Q, Q, Q]],
    corners: list[tuple[tuple[Q, Q], ...]],
    side: Q,
    *,
    squares: list[int] | None = None,
    pairs: list[tuple[int, int]] | None = None,
    prepared: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Decide the listed squares and pairs (0-based), or all of them."""
    n = len(poses)
    if len(corners) != n:
        raise ValueError("poses and corners differ in count")
    full = squares is None and pairs is None
    sq_idx = list(range(n)) if squares is None else list(squares)
    pr_idx = list(combinations(range(n), 2)) if pairs is None else list(pairs)
    pre = prepared if prepared is not None else prepare(poses, corners)
    ip, pts = pre["ip"], pre["pts"]
    S_b = mpq(side[0], side[1])
    problems: list[str] = []
    wall_rows = []
    for k in sq_idx:
        ua, ub = pre["unit_a"][k], pre["unit_b"][k]
        if not ua:
            problems.append(f"square {k + 1}: not a unit square by A")
        if not ub:
            problems.append(f"square {k + 1}: not a unit square by B")
        cl = A.clearances(ip[k], side) if ua else None
        if ub:
            wcls, inside = B.walls(pts[k], S_b)
        else:
            wcls, inside = None, None
        row = {"square": k + 1, "unit_a": ua, "unit_b": ub, "sense_b": pre["senses"][k]}
        if cl is not None:
            row["clearances_a"] = cl
            row["classes_a"] = [A_WALL[_sign(c)] for c in cl]
        if wcls is not None:
            row["classes_b"] = [B_WALL[c] for c, _ in wcls]
            row["areas_out_b"] = [a for _, a in wcls]
            row["inside_b"] = inside
        if cl is not None:
            if any(c < 0 for c in cl):
                problems.append(f"square {k + 1}: crosses a wall by A")
        if wcls is not None:
            if any(B_WALL[c] == "cross" for c, _ in wcls):
                problems.append(f"square {k + 1}: crosses a wall by B")
            if inside != 1:
                problems.append(f"square {k + 1}: area inside the box {inside} by B")
        if cl is not None and wcls is not None and row["classes_a"] != row["classes_b"]:
            problems.append(f"square {k + 1}: wall classes differ, A {row['classes_a']} B {row['classes_b']}")
        wall_rows.append(row)
    pair_rows = []
    for i, j in pr_idx:
        row: dict[str, Any] = {"pair": (i + 1, j + 1)}
        if pre["unit_a"][i] and pre["unit_a"][j]:
            m = A.margin(ip[i], ip[j])
            row["margin_a"] = m
            row["class_a"] = A_PAIR[_sign(m)]
            if m < 0:
                problems.append(f"pair {i + 1},{j + 1}: overlap by A")
        if pre["unit_b"][i] and pre["unit_b"][j]:
            cls, ar, agree = B.pair(pts[i], pts[j])
            row["class_b"] = cls
            row["area_b"] = ar
            if not agree:
                problems.append(f"pair {i + 1},{j + 1}: B's two clippings disagree")
            if cls == "overlap":
                problems.append(f"pair {i + 1},{j + 1}: overlap by B")
        if "class_a" in row and "class_b" in row and row["class_a"] != row["class_b"]:
            problems.append(f"pair {i + 1},{j + 1}: classes differ, A {row['class_a']} B {row['class_b']}")
        pair_rows.append(row)
    if full:
        verdict = "ACCEPT" if not problems else "REFUSE"
    else:
        verdict = "PARTIAL" if not problems else "REFUSE"
    return {"verdict": verdict, "problems": problems, "walls": wall_rows, "pairs": pair_rows, "n": n}


def summary(dec: dict[str, Any]) -> dict[str, Any]:
    """Counts and extremes of a decision, as exact fractions printed as strings."""
    pairs = dec["pairs"]
    walls = dec["walls"]
    margins = [(r["margin_a"], r["pair"]) for r in pairs if "margin_a" in r]
    margins.sort(key=lambda t: (t[0], t[1]))
    cls_a: dict[str, int] = {}
    cls_b: dict[str, int] = {}
    for r in pairs:
        if "class_a" in r:
            cls_a[r["class_a"]] = cls_a.get(r["class_a"], 0) + 1
        if "class_b" in r:
            cls_b[r["class_b"]] = cls_b.get(r["class_b"], 0) + 1
    wall_least: list[Any] = [None, None, None, None]
    wall_at: list[list[int]] = [[], [], [], []]
    wcls_a: dict[str, int] = {}
    wcls_b: dict[str, int] = {}
    for r in walls:
        if "clearances_a" in r:
            for w in range(4):
                c = r["clearances_a"][w]
                if wall_least[w] is None or c < wall_least[w]:
                    wall_least[w] = c
                    wall_at[w] = [r["square"]]
                elif c == wall_least[w]:
                    wall_at[w].append(r["square"])
            for c in r["classes_a"]:
                wcls_a[c] = wcls_a.get(c, 0) + 1
        if "classes_b" in r:
            for c in r["classes_b"]:
                wcls_b[c] = wcls_b.get(c, 0) + 1
    out = {
        "verdict": dec["verdict"],
        "problems": dec["problems"][:50],
        "problem_count": len(dec["problems"]),
        "squares_decided": len(walls),
        "pairs_decided": len(pairs),
        "pair_classes_a": cls_a,
        "pair_classes_b": cls_b,
        "wall_classes_a": wcls_a,
        "wall_classes_b": wcls_b,
    }
    if margins:
        out["least_margins"] = [
            {"pair": list(p), "margin": str(m), "margin_float": f"{float(m):.12e}"} for m, p in margins[:12]
        ]
    out["least_wall_clearances"] = [
        None if wall_least[w] is None else {
            "wall": ("left", "bottom", "right", "top")[w],
            "clearance": str(wall_least[w]),
            "clearance_float": f"{float(wall_least[w]):.12e}",
            "squares": wall_at[w],
        }
        for w in range(4)
    ]
    return out
