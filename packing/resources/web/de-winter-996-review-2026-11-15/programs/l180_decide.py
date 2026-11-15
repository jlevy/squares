"""Lane L180: decide a packing by both methods, every square, wall and pair.

Written for the blind stage 4 review of issue #996 as a clean-room implementation.
It imports nothing from this repository or the source, and reuses no code of any
earlier review.

Method A (``l180_axes``) decides the poses of the JSON form; method B (``l180_clip``)
decides corners. For the certificate itself B is handed the twin's own corners, which
the reader has shown equal the JSON's exactly; for a modified certificate in the
controls it is handed the corners the reader derives from the modified poses.

The verdict is ACCEPT only when every square is a unit square by both methods, every
pair is apart or touching by both with equal classes, every square-wall pair is inside
or touching by both with equal classes, and every square's area inside the box is
exactly 1.
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any

import l180_axes as A
import l180_clip as B
from gmpy2 import mpq
from l180_reader import Point, Pose


@dataclass
class Decision:
    n: int
    side: Fraction
    unit_a: list[bool] = field(default_factory=list)
    unit_b: list[bool] = field(default_factory=list)
    sense_b: list[int] = field(default_factory=list)
    margins: dict[tuple[int, int], Fraction] = field(default_factory=dict)
    binding: dict[tuple[int, int], int] = field(default_factory=dict)
    class_a: dict[tuple[int, int], str] = field(default_factory=dict)
    class_b: dict[tuple[int, int], str] = field(default_factory=dict)
    area_b: dict[tuple[int, int], mpq] = field(default_factory=dict)
    both_orders: dict[tuple[int, int], bool] = field(default_factory=dict)
    clear: dict[tuple[int, str], Fraction] = field(default_factory=dict)
    wall_a: dict[tuple[int, str], str] = field(default_factory=dict)
    wall_b: dict[tuple[int, str], str] = field(default_factory=dict)
    inside_area: list[mpq] = field(default_factory=list)
    verdict: str = ""
    reasons: list[str] = field(default_factory=list)


def decide(n: int, side: Fraction, poses: Sequence[Pose], corners: Sequence[Sequence[Point]]) -> Decision:
    """Both methods over every square, wall and pair; squares are numbered from 1."""
    d = Decision(n=n, side=side)
    if len(poses) != n or len(corners) != n:
        d.verdict = "REFUSE"
        d.reasons.append("count")
        return d
    ints = [A.to_ints(p.x, p.y, p.c, p.s) for p in poses]
    qs: list[list[B.Pt]] = []
    for k in range(n):
        d.unit_a.append(A.is_unit(ints[k]))
        cs = B.to_mpq(corners[k])
        ok, sense = B.unit_square(cs)
        d.unit_b.append(ok)
        d.sense_b.append(sense)
        qs.append(B.ccw(cs) if ok else cs)
    bad_a = [k + 1 for k in range(n) if not d.unit_a[k]]
    bad_b = [k + 1 for k in range(n) if not d.unit_b[k]]
    if bad_a or bad_b:
        d.verdict = "REFUSE"
        d.reasons.append(f"not unit squares: method A {bad_a}, method B {bad_b}")
        return d
    side_q = mpq(side.numerator, side.denominator)
    for i in range(n):
        for j in range(i + 1, n):
            m, nb = A.pair_margin(ints[i], ints[j])
            key = (i + 1, j + 1)
            d.margins[key] = m
            d.binding[key] = nb
            d.class_a[key] = A.pair_class(m)
            cb, ab, agree = B.pair(qs[i], qs[j])
            d.class_b[key] = cb
            d.area_b[key] = ab
            d.both_orders[key] = agree
    for i in range(n):
        cl = A.wall_clearances(ints[i], side)
        wb = B.walls(qs[i], side_q)
        for w in A.WALLS:
            d.clear[(i + 1, w)] = cl[w]
            d.wall_a[(i + 1, w)] = A.wall_class(cl[w])
            d.wall_b[(i + 1, w)] = wb[w][0]
        d.inside_area.append(B.area_inside(qs[i], side_q))
    reasons = d.reasons
    disagree = [k for k in d.class_a if d.class_a[k] != d.class_b[k]]
    if disagree:
        reasons.append(f"pair classes disagree: {disagree[:10]} ({len(disagree)})")
    one_way = [k for k in d.both_orders if not d.both_orders[k]]
    if one_way:
        reasons.append(f"method B's two clipping orders disagree: {one_way[:10]}")
    overlaps = [k for k in d.class_a if d.class_a[k] == A.OVERLAP or d.class_b[k] == B.OVERLAP]
    if overlaps:
        reasons.append(f"overlapping pairs: {overlaps[:10]} ({len(overlaps)})")
    wd = [k for k in d.wall_a if d.wall_a[k] != d.wall_b[k]]
    if wd:
        reasons.append(f"wall classes disagree: {wd[:10]} ({len(wd)})")
    crossing = [k for k in d.wall_a if d.wall_a[k] == A.CROSS or d.wall_b[k] == B.CROSS]
    if crossing:
        reasons.append(f"squares crossing a wall: {crossing[:10]} ({len(crossing)})")
    not_in = [k + 1 for k in range(n) if d.inside_area[k] != 1]
    if not_in:
        reasons.append(f"squares not inside the box by area: {not_in[:10]} ({len(not_in)})")
    if (not_in and not crossing) or (crossing and not not_in):
        reasons.append("containment by area disagrees with the wall classes")
    d.verdict = "REFUSE" if reasons else "ACCEPT"
    return d


# ----------------------------------------------------------------------------- summaries


def fstr(v: Fraction) -> str:
    return f"{v.numerator}/{v.denominator}" if v.denominator != 1 else str(v.numerator)


def sci(v: Fraction, digits: int = 12) -> str:
    """A decimal print of an exact rational, to ``digits`` significant figures."""
    if v == 0:
        return "0"
    sign = "-" if v < 0 else ""
    a = abs(v)
    e = len(str(a.numerator)) - len(str(a.denominator))
    while Fraction(10) ** e > a:
        e -= 1
    while Fraction(10) ** (e + 1) <= a:
        e += 1
    mant = a / Fraction(10) ** e
    scaled = round(mant * 10 ** (digits - 1))
    if scaled >= 10**digits:
        scaled //= 10
        e += 1
    s = str(scaled)
    return f"{sign}{s[0]}.{s[1:]}e{e:+d}"


def margin_digest(d: Decision) -> str:
    text = "".join(f"{i} {j} {fstr(m)}\n" for (i, j), m in sorted(d.margins.items()))
    return hashlib.sha256(text.encode()).hexdigest()


def clearance_digest(d: Decision) -> str:
    text = "".join(f"{i} {w} {fstr(c)}\n" for (i, w), c in sorted(d.clear.items()))
    return hashlib.sha256(text.encode()).hexdigest()


def summary(d: Decision) -> dict[str, Any]:
    """What a receipt keeps of a decision: counts, extremes, digests, near lists."""
    out: dict[str, Any] = {"verdict": d.verdict, "reasons": d.reasons, "n": d.n, "side": fstr(d.side)}
    out["unit_a"] = sum(d.unit_a)
    out["unit_b"] = sum(d.unit_b)
    out["sense_b"] = {"counterclockwise": d.sense_b.count(1), "clockwise": d.sense_b.count(-1)}
    if not d.margins:
        return out
    counts: dict[str, dict[str, int]] = {"A": {}, "B": {}}
    for k in d.margins:
        counts["A"][d.class_a[k]] = counts["A"].get(d.class_a[k], 0) + 1
        counts["B"][d.class_b[k]] = counts["B"].get(d.class_b[k], 0) + 1
    out["pairs"] = len(d.margins)
    out["pair_classes"] = counts
    out["pair_classes_agree"] = all(d.class_a[k] == d.class_b[k] for k in d.margins)
    out["method_b_both_orders_agree"] = all(d.both_orders.values())
    total_area = sum(d.area_b.values(), mpq(0))
    out["sum_overlap_area_b"] = str(total_area)
    out["touching_pairs"] = sorted([list(k) for k in d.margins if d.class_a[k] == A.TOUCH])
    out["overlapping_pairs"] = sorted([list(k) for k in d.margins if d.class_a[k] == A.OVERLAP])
    pos = {k: m for k, m in d.margins.items() if m > 0}
    if pos:
        kmin = min(pos, key=lambda k: pos[k])
        out["least_positive_margin"] = {"pair": list(kmin), "exact": fstr(pos[kmin]), "approx": sci(pos[kmin])}
    least = min(d.margins, key=lambda k: d.margins[k])
    out["least_margin"] = {"pair": list(least), "exact": fstr(d.margins[least]), "approx": sci(d.margins[least])}
    out["positive_pairs_below"] = {
        t: sum(1 for m in pos.values() if m < Fraction(1, 10**e))
        for t, e in (("1e-15", 15), ("1e-12", 12), ("1e-11", 11), ("1e-9", 9), ("1e-6", 6), ("1e-3", 3), ("1e-1", 1))
    }
    near = sorted((m, k) for k, m in d.margins.items() if m < Fraction(1, 10**3))
    out["near_pairs"] = [
        {"pair": list(k), "margin": sci(m), "exact": fstr(m), "binding_normals": d.binding[k], "class": d.class_a[k]}
        for m, k in near
    ]
    out["margin_list_sha256"] = margin_digest(d)
    wc: dict[str, dict[str, int]] = {"A": {}, "B": {}}
    for k in d.clear:
        wc["A"][d.wall_a[k]] = wc["A"].get(d.wall_a[k], 0) + 1
        wc["B"][d.wall_b[k]] = wc["B"].get(d.wall_b[k], 0) + 1
    out["square_wall_pairs"] = len(d.clear)
    out["wall_classes"] = wc
    out["wall_classes_agree"] = all(d.wall_a[k] == d.wall_b[k] for k in d.clear)
    out["wall_contacts"] = {
        w: sorted(i for (i, ww), c in d.clear.items() if ww == w and c == 0) for w in A.WALLS
    }
    out["wall_crossings"] = {w: sorted(i for (i, ww), c in d.clear.items() if ww == w and c < 0) for w in A.WALLS}
    least_pos_wall: dict[str, Any] = {}
    for w in A.WALLS:
        vals = {i: c for (i, ww), c in d.clear.items() if ww == w and c > 0}
        if vals:
            mv = min(vals.values())
            least_pos_wall[w] = {"squares": sorted(i for i, c in vals.items() if c == mv), "exact": fstr(mv), "approx": sci(mv)}
    out["least_positive_clearance"] = least_pos_wall
    near_w = sorted((c, i, w) for (i, w), c in d.clear.items() if c < Fraction(1, 10**3))
    out["near_walls"] = [{"square": i, "wall": w, "clearance": sci(c), "exact": fstr(c)} for c, i, w in near_w]
    out["clearance_list_sha256"] = clearance_digest(d)
    out["inside_area_one"] = sum(1 for a in d.inside_area if a == 1)
    return out
