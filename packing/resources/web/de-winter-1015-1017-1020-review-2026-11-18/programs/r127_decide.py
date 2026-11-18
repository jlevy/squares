"""Decide a packing by both methods, every square, every wall and every pair.

Lane r127-1118.  Written for this review; imports only its own modules.

The verdict is ACCEPT only when both methods find every square a unit square, every
square inside the box (method A: all four clearances >= 0; method B: no wall crossed
and area exactly 1 inside), and no pair overlapping, with the two methods' classes
equal for every square-wall and every pair decision.  There is no distance filter and
no tolerance.

``decide_patch`` re-decides only what a change can reach: the walls and pairs of the
squares that changed, and every wall when the side changed; the rest is carried from
the base decision, which is valid because each pair decision is a function of the two
squares alone and each wall decision of the square and the side.  The self-test holds
the patched decision equal to a fresh one.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import r127_area as B
import r127_axes as A


@dataclass
class Decision:
    n: int
    side: Fraction
    sqA: list
    polys: list
    unitA: list
    unitB: list
    senseA: list
    senseB: list
    clearA: list
    wallB: list
    insideB: list
    mA: dict
    cB: dict


def _sideq(side):
    return B.mpq(side.numerator, side.denominator)


def _square(corners):
    sa = A.prepare(corners)
    raw = B.to_mpq(corners)
    okb, senseb = B.unit_square(raw)
    return sa, B.ccw(raw), okb, senseb


def decide_full(packing) -> Decision:
    n = packing.n
    sqA, polys, unitA, unitB, senseA, senseB = [], [], [], [], [], []
    for c in packing.corners:
        sa, poly, okb, sb = _square(c)
        sqA.append(sa)
        polys.append(poly)
        unitA.append(sa.unit)
        unitB.append(okb)
        senseA.append(sa.sense)
        senseB.append(sb)
    side = packing.side
    sq = _sideq(side)
    clearA = [A.walls(s, side) for s in sqA]
    wallB, insideB = [], []
    for P in polys:
        w, a = B.wall_classes(P, sq)
        wallB.append(w)
        insideB.append(a)
    mA, cB = {}, {}
    for i in range(n):
        for j in range(i + 1, n):
            mA[(i, j)] = A.margin(sqA[i], sqA[j])
            cB[(i, j)] = B.pair_class(polys[i], polys[j])
    return Decision(n, side, sqA, polys, unitA, unitB, senseA, senseB, clearA, wallB,
                    insideB, mA, cB)


def decide_patch(base: Decision, packing, changed) -> Decision:
    """Re-decide the squares in ``changed`` (indices) and, if the side changed, every
    wall; carry the rest from ``base``.  The count must be unchanged."""
    assert packing.n == base.n
    d = Decision(base.n, packing.side, list(base.sqA), list(base.polys), list(base.unitA),
                 list(base.unitB), list(base.senseA), list(base.senseB), list(base.clearA),
                 list(base.wallB), list(base.insideB), dict(base.mA), dict(base.cB))
    changed = sorted(set(changed))
    for i in changed:
        sa, poly, okb, sb = _square(packing.corners[i])
        d.sqA[i], d.polys[i], d.unitA[i], d.unitB[i] = sa, poly, sa.unit, okb
        d.senseA[i], d.senseB[i] = sa.sense, sb
    side_changed = packing.side != base.side
    sq = _sideq(packing.side)
    redo_walls = range(d.n) if side_changed else changed
    for i in redo_walls:
        d.clearA[i] = A.walls(d.sqA[i], packing.side)
        w, a = B.wall_classes(d.polys[i], sq)
        d.wallB[i], d.insideB[i] = w, a
    cs = set(changed)
    for i in changed:
        for j in range(d.n):
            if j == i or (j in cs and j < i):
                continue
            key = (min(i, j), max(i, j))
            d.mA[key] = A.margin(d.sqA[key[0]], d.sqA[key[1]])
            d.cB[key] = B.pair_class(d.polys[key[0]], d.polys[key[1]])
    return d


def wall_class_a(c: Fraction) -> str:
    return "clear" if c > 0 else ("touch" if c == 0 else "cross")


WALLS = ("left", "bottom", "right", "top")


def summarize(d: Decision) -> dict:
    """The facts and the verdict of a decision, as JSON-ready values (exact fractions as
    strings, and short decimal prints)."""
    problems: list[str] = []
    for i in range(d.n):
        if not d.unitA[i] or not d.unitB[i]:
            problems.append(f"square {i + 1} not a unit square (A {d.unitA[i]}, B {d.unitB[i]})")
    agree_walls = 0
    contacts = {w: [] for w in WALLS}
    least_clear = {w: None for w in WALLS}
    for i in range(d.n):
        for k, w in enumerate(WALLS):
            ca = wall_class_a(d.clearA[i][k])
            cb = d.wallB[i][k]
            if ca == cb:
                agree_walls += 1
            else:
                problems.append(f"square {i + 1} {w}: A {ca}, B {cb}")
            if ca == "cross" or cb == "cross":
                problems.append(f"square {i + 1} crosses the {w} wall")
            if ca == "touch":
                contacts[w].append(i + 1)
            cur = least_clear[w]
            if cur is None or d.clearA[i][k] < cur[0]:
                least_clear[w] = (d.clearA[i][k], i + 1)
        if d.insideB[i] != 1:
            problems.append(f"square {i + 1}: area inside the box {d.insideB[i]}, not 1")
    counts = {"apart": 0, "contact": 0, "overlap": 0}
    agree_pairs = 0
    least = None
    touching = []
    overlapping = []
    for key, m in d.mA.items():
        ca = A.cls(m)
        cb = d.cB[key][0]
        counts[ca] += 1
        if ca == cb:
            agree_pairs += 1
        else:
            problems.append(f"pair {key[0] + 1},{key[1] + 1}: A {ca}, B {cb}")
        if ca == "contact":
            touching.append((key[0] + 1, key[1] + 1))
        if ca == "overlap" or cb == "overlap":
            overlapping.append((key[0] + 1, key[1] + 1))
        if least is None or m < least[0]:
            least = (m, key)
    if overlapping:
        problems.append(f"{len(overlapping)} overlapping pairs")
    below = {f"1e-{k}": sum(1 for m in d.mA.values() if 0 < m < Fraction(1, 10**k))
             for k in (30, 20, 15, 14, 13, 12, 11, 10, 9, 6, 3, 1)}
    xs_hi = max(d.side - c[2] for c in d.clearA)
    ys_hi = max(d.side - c[3] for c in d.clearA)
    xs_lo = min(c[0] for c in d.clearA)
    ys_lo = min(c[1] for c in d.clearA)
    out = {
        "n": d.n,
        "side": fs(d.side),
        "side_decimal": dec(d.side, 30),
        "units_A": sum(d.unitA), "units_B": sum(d.unitB),
        "senses_A": {"ccw": d.senseA.count(1), "cw": d.senseA.count(-1)},
        "senses_B": {"ccw": d.senseB.count(1), "cw": d.senseB.count(-1)},
        "pairs": len(d.mA), "pair_classes_A": counts, "pair_classes_agree": agree_pairs,
        "overlap_area_sum_B": str(sum((v[1] for v in d.cB.values()), B.ZERO)),
        "touching_pairs": touching,
        "overlapping_pairs": overlapping[:20],
        "least_margin": None if least is None else {
            "pair": [least[1][0] + 1, least[1][1] + 1], "exact": fs(least[0]),
            "decimal": sci(least[0])},
        "positive_margins_below": below,
        "square_wall_decisions": 4 * d.n, "square_wall_agree": agree_walls,
        "wall_contacts": contacts,
        "least_clearance": {w: {"square": v[1], "exact": fs(v[0]), "decimal": sci(v[0])}
                            for w, v in least_clear.items() if v is not None},
        "extent": {"min_x": fs(xs_lo), "max_x": fs(xs_hi), "min_y": fs(ys_lo),
                   "max_y": fs(ys_hi), "width": fs(xs_hi - xs_lo), "height": fs(ys_hi - ys_lo),
                   "side_less_max_x": sci(d.side - xs_hi), "side_less_max_y": sci(d.side - ys_hi)},
        "areas_inside_all_one": all(a == 1 for a in d.insideB),
        "problems": problems[:50], "problem_count": len(problems),
        "verdict": "ACCEPT" if not problems else "REFUSE",
    }
    return out


def fs(q: Fraction) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def dec(q: Fraction, places: int) -> str:
    """Truncated decimal print with ``places`` digits after the point."""
    sign = "-" if q < 0 else ""
    q = abs(q)
    ip = q.numerator // q.denominator
    frac = q - ip
    digits = (frac.numerator * 10**places) // frac.denominator
    return f"{sign}{ip}.{digits:0{places}d}"


def sci(q: Fraction, figs: int = 6) -> str:
    """A short scientific print of an exact value, truncated, for reading only."""
    if q == 0:
        return "0"
    sign = "-" if q < 0 else ""
    a = abs(q)
    e = len(str(a.numerator)) - len(str(a.denominator))
    # adjust so that 1 <= a / 10^e < 10
    while Fraction(10) ** e > a:
        e -= 1
    while Fraction(10) ** (e + 1) <= a:
        e += 1
    m = a / Fraction(10) ** e
    digits = (m.numerator * 10 ** (figs - 1)) // m.denominator
    s = str(digits)
    return f"{sign}{s[0]}.{s[1:]}e{e:+d}"
