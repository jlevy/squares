"""Lane L186: decide a packing by both methods, every square, wall and pair.

Method A (`l186_sat`) and method B (`l186_clip`) share only the reader's exact
rationals. The verdict is ACCEPT only when both accept every square as a unit
square, every square inside the box, and every pair with disjoint interiors,
with equal classes everywhere; REFUSE when both refuse something and agree
everywhere; DISAGREE when the two methods differ anywhere (a checker fault).
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from typing import Any

import l186_clip as mb
import l186_sat as ma
from l186_reader import Square

WALLS = ("left", "bottom", "right", "top")
THRESHOLDS = ("1e-15", "1e-12", "1e-11", "1e-10", "1e-9", "1e-6", "1e-3", "1e-1")


def ftext(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def sci(v: Fraction, digits: int = 12) -> str:
    """An exact value printed in scientific notation, truncated toward zero."""
    if v == 0:
        return "0"
    sign = "-" if v < 0 else ""
    a = abs(v)
    e = len(str(a.numerator)) - len(str(a.denominator))
    while a >= Fraction(10) ** (e + 1):
        e += 1
    while a < Fraction(10) ** e:
        e -= 1
    scaled = a / Fraction(10) ** e  # in [1, 10)
    m = int(scaled * 10 ** (digits - 1))
    s = str(m)
    return f"{sign}{s[0]}.{s[1:]}e{e:+d}"


def decimal_text(v: Fraction, places: int) -> str:
    """Exact value truncated toward zero at a number of decimal places."""
    sign = "-" if v < 0 else ""
    a = abs(v)
    whole = a.numerator // a.denominator
    frac = a - whole
    digits = int(frac * 10**places)
    return f"{sign}{whole}.{digits:0{places}d}"


def digest(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, separators=(",", ":")).encode()).hexdigest()


def decide(side: Fraction, squares: list[Square], keep_lists: bool = False) -> dict[str, Any]:
    n = len(squares)
    # ---- method A
    pa = [ma.prepare(sq) for sq in squares]
    unit_a = [p.unit for p in pa]
    clear_a = [ma.wall_clearances(p, side) for p in pa]
    # ---- method B
    pb = [mb.to_mpq(sq) for sq in squares]
    ub = [mb.unit_square(p) for p in pb]
    unit_b = [u for u, _ in ub]
    sense_b = [s for _, s in ub]
    sb = mb.mpq(side.numerator, side.denominator)
    ccw_b = [mb.ccw(p) for p in pb]
    walls_b = [mb.wall_classes(c, sb) for c in ccw_b]

    reasons: list[str] = []
    disagreements: list[str] = []
    non_unit_a = [i + 1 for i in range(n) if not unit_a[i]]
    non_unit_b = [i + 1 for i in range(n) if not unit_b[i]]
    if non_unit_a != non_unit_b:
        disagreements.append(f"unit squares differ: A {non_unit_a[:10]} B {non_unit_b[:10]}")
    if non_unit_a or non_unit_b:
        reasons.append(f"not a unit square: A {non_unit_a[:10]}, B {non_unit_b[:10]}")
    sense_a = [p.sense for p in pa]
    good = [unit_a[i] and unit_b[i] for i in range(n)]
    for i in range(n):
        if good[i] and sense_a[i] != sense_b[i]:
            disagreements.append(f"listing sense differs at square {i + 1}")

    # ---- walls
    wall_contacts: list[list[Any]] = []
    wall_cross: list[list[Any]] = []
    clear_list: list[list[str]] = []
    least_by_wall: dict[str, Any] = {}
    least_pos: Fraction | None = None
    least_pos_at: list[list[Any]] = []
    least_clear: Fraction | None = None
    not_contained: list[int] = []
    for i in range(n):
        clear_list.append([ftext(c) for c in clear_a[i]])
        if not good[i]:
            continue
        classes_b, area_in = walls_b[i]
        if area_in != 1:
            not_contained.append(i + 1)
        for w in range(4):
            c = clear_a[i][w]
            cls_a = "apart" if c > 0 else ("touch" if c == 0 else "cross")
            if cls_a != classes_b[w]:
                disagreements.append(f"wall {WALLS[w]} of square {i + 1}: A {cls_a} B {classes_b[w]}")
            if c == 0:
                wall_contacts.append([i + 1, WALLS[w]])
            elif c < 0:
                wall_cross.append([i + 1, WALLS[w], ftext(c)])
            cur = least_by_wall.get(WALLS[w])
            if cur is None or c < cur[0]:
                least_by_wall[WALLS[w]] = [c, [i + 1]]
            elif c == cur[0]:
                cur[1].append(i + 1)
            if least_clear is None or c < least_clear:
                least_clear = c
            if c > 0:
                if least_pos is None or c < least_pos:
                    least_pos = c
                    least_pos_at = [[i + 1, WALLS[w]]]
                elif c == least_pos:
                    least_pos_at.append([i + 1, WALLS[w]])
    if wall_cross:
        reasons.append(f"square across a wall: {wall_cross[:10]}")
    if not_contained:
        reasons.append(f"area inside the box is not 1 (B): {not_contained[:10]}")
    cross_b = [
        [i + 1, WALLS[w]]
        for i in range(n)
        if good[i]
        for w in range(4)
        if walls_b[i][0][w] == "cross"
    ]
    if cross_b and not wall_cross:
        disagreements.append("B finds a square across a wall that A does not")

    # ---- pairs
    margins: list[str] = []
    counts_a = {"apart": 0, "touch": 0, "overlap": 0}
    counts_b = {"apart": 0, "touch": 0, "overlap": 0}
    touching: list[list[int]] = []
    overlapping: list[list[Any]] = []
    least_m: Fraction | None = None
    least_at: list[list[int]] = []
    least_pos_m: Fraction | None = None
    least_pos_m_at: list[list[int]] = []
    below = {t: 0 for t in THRESHOLDS}
    tfr = {t: Fraction(t) for t in THRESHOLDS}
    area_sum = mb.mpq(0)
    clip_mismatch = 0
    decided = 0
    for i in range(n):
        for j in range(i + 1, n):
            if not (good[i] and good[j]):
                margins.append("")
                continue
            m = ma.pair_margin(pa[i], pa[j])
            margins.append(ftext(m))
            cls_a = ma.sign_class(m)
            cls_b, area, agree = mb.pair_class(ccw_b[i], ccw_b[j])
            decided += 1
            if not agree:
                clip_mismatch += 1
                disagreements.append(f"pair ({i + 1}, {j + 1}): B clipped two ways differ")
            if cls_a != cls_b:
                disagreements.append(f"pair ({i + 1}, {j + 1}): A {cls_a} B {cls_b}")
            counts_a[cls_a] += 1
            counts_b[cls_b] += 1
            area_sum += area
            if cls_a == "touch":
                touching.append([i + 1, j + 1])
            elif cls_a == "overlap":
                overlapping.append([i + 1, j + 1, ftext(m), str(area)])
            if least_m is None or m < least_m:
                least_m, least_at = m, [[i + 1, j + 1]]
            elif m == least_m:
                least_at.append([i + 1, j + 1])
            if m > 0:
                if least_pos_m is None or m < least_pos_m:
                    least_pos_m, least_pos_m_at = m, [[i + 1, j + 1]]
                elif m == least_pos_m:
                    least_pos_m_at.append([i + 1, j + 1])
                for t in THRESHOLDS:
                    if m < tfr[t]:
                        below[t] += 1
    if overlapping:
        reasons.append(f"overlapping pairs: {len(overlapping)}")

    if disagreements:
        verdict = "DISAGREE"
    elif reasons:
        verdict = "REFUSE"
    else:
        verdict = "ACCEPT"

    def wall_least(w: str) -> Any:
        v = least_by_wall.get(w)
        if v is None:
            return None
        return {"value": ftext(v[0]), "sci": sci(v[0]), "squares": v[1][:40], "count": len(v[1])}

    out: dict[str, Any] = {
        "verdict": verdict,
        "reasons": reasons,
        "disagreements": disagreements[:50],
        "disagreement_count": len(disagreements),
        "n": n,
        "squares_unit_by_A": sum(unit_a),
        "squares_unit_by_B": sum(unit_b),
        "non_unit_A": non_unit_a[:60],
        "non_unit_B": non_unit_b[:60],
        "senses": {"ccw": sense_a.count(1), "cw": sense_a.count(-1), "none": sense_a.count(0)},
        "walls": {
            "square_wall_pairs": 4 * n,
            "contacts": wall_contacts,
            "contact_count": len(wall_contacts),
            "crossing": wall_cross,
            "least_by_wall": {w: wall_least(w) for w in WALLS},
            "least_clearance": None if least_clear is None else ftext(least_clear),
            "least_clearance_sci": None if least_clear is None else sci(least_clear),
            "least_positive_clearance": None if least_pos is None else ftext(least_pos),
            "least_positive_clearance_sci": None if least_pos is None else sci(least_pos),
            "least_positive_at": least_pos_at[:60],
            "least_positive_count": len(least_pos_at),
            "all_area_inside_one_B": not not_contained and all(good),
            "not_contained_B": not_contained[:60],
        },
        "pairs": {
            "decided": decided,
            "of": n * (n - 1) // 2,
            "classes_A": counts_a,
            "classes_B": counts_b,
            "clip_two_ways_mismatch": clip_mismatch,
            "touching": touching,
            "overlapping": overlapping[:60],
            "overlapping_count": len(overlapping),
            "overlap_area_sum_B": str(area_sum),
            "least_margin": None if least_m is None else ftext(least_m),
            "least_margin_sci": None if least_m is None else sci(least_m),
            "least_margin_at": least_at[:20],
            "least_positive_margin": None if least_pos_m is None else ftext(least_pos_m),
            "least_positive_margin_sci": None if least_pos_m is None else sci(least_pos_m),
            "least_positive_margin_at": least_pos_m_at[:20],
            "positive_margins_below": below,
        },
        "digests": {
            "margins_sha256": digest(margins),
            "clearances_sha256": digest(clear_list),
        },
        "method_B": mb.version(),
    }
    if keep_lists:
        out["_margins"] = margins
        out["_clearances"] = clear_list
    return out
