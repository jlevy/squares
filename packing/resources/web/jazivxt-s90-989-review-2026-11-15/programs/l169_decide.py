"""Lane L169 decision: a reading decided by both methods over every square, wall and pair.

The verdict is ACCEPT only when
- both methods find every square a unit square, and method B finds it counterclockwise;
- every wall clearance of method A is >= 0, method B classes every square-wall pair as
  clear or contact, the two classes agree (A: > 0 clear, = 0 contact, < 0 crossing), and
  method B finds every square's area inside the box exactly 1;
- every pair margin of method A is >= 0, method B classes every pair apart or contact,
  and the two classes agree on every pair.

No pair is skipped: there is no distance filter.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction

import l169_clip as clipm
import l169_sat as sat

WALLS = ("left", "right", "bottom", "top")


def frac_str(f: Fraction) -> str:
    return f"{f.numerator}/{f.denominator}"


def sci(f: Fraction, digits: int = 6) -> str:
    """A decimal print of an exact fraction, for receipts (information only)."""
    if f == 0:
        return "0"
    neg = f < 0
    a = -f if neg else f
    e = 0
    while a >= 10:
        a /= 10
        e += 1
    while a < 1:
        a *= 10
        e -= 1
    scaled = round(a * 10 ** (digits - 1))
    if scaled >= 10**digits:
        scaled //= 10
        e += 1
    s = str(scaled)
    mant = s[0] + ("." + s[1:] if len(s) > 1 else "")
    return f"{'-' if neg else ''}{mant}e{e}"


def a_wall_class(c: Fraction) -> str:
    if c > 0:
        return "clear"
    if c == 0:
        return "contact"
    return "crossing"


def decide(reading: dict, side: tuple[int, int] | None = None, keep_lists: bool = True) -> dict:
    s = reading["side"] if side is None else side
    sq = reading["squares"]
    n = len(sq)
    a_sq = [sat.Square(*row) for row in sq]
    b_sq = [clipm.corners(*row) for row in sq]

    unit_a = [x.is_unit() for x in a_sq]
    ub = [clipm.is_unit_ccw(c) for c in b_sq]
    unit_b = [u for u, _ in ub]
    ccw_b = [c for _, c in ub]

    clear_a: list[dict[str, Fraction]] = []
    wall_rows = []
    wall_disagree = []
    area_in = []
    for k in range(n):
        ca = sat.clearances(a_sq[k], s)
        clear_a.append(ca)
        ain = clipm.area_in_box(b_sq[k], s)
        area_in.append(ain)
        for w in WALLS:
            ka = a_wall_class(ca[w])
            kb, area_out = clipm.wall_class(b_sq[k], w, s)
            wall_rows.append((k + 1, w, ca[w], ka, kb, area_out))
            if ka != kb:
                wall_disagree.append((k + 1, w, ka, kb))

    pairs = []
    pair_disagree = []
    for i in range(n):
        for j in range(i + 1, n):
            m = sat.pair_margin(a_sq[i], a_sq[j])
            ka = sat.classify(m)
            kb, area = clipm.pair_class(b_sq[i], b_sq[j])
            kb2, area2 = clipm.pair_class(b_sq[j], b_sq[i])
            if kb != kb2 or area != area2:
                kb = f"asymmetric:{kb}/{kb2}"
            pairs.append((i + 1, j + 1, m, ka, kb, area))
            if ka != kb:
                pair_disagree.append((i + 1, j + 1, ka, kb))

    overlapping = [(i, j) for i, j, m, ka, kb, _ in pairs if ka == "overlap" or kb == "overlap"]
    touching = [(i, j) for i, j, m, ka, kb, _ in pairs if ka == "contact" and kb == "contact"]
    crossing = [(k, w) for k, w, c, ka, kb, _ in wall_rows if ka == "crossing" or kb == "crossing"]
    contacts = [(k, w) for k, w, c, ka, kb, _ in wall_rows if ka == "contact" and kb == "contact"]
    not_inside = [k + 1 for k in range(n) if area_in[k] != 1]
    total_overlap_area = sum((r[5] for r in pairs), clipm.mpq(0))

    ok = (
        all(unit_a)
        and all(unit_b)
        and all(ccw_b)
        and not wall_disagree
        and not pair_disagree
        and not overlapping
        and not crossing
        and not not_inside
    )

    margins = [r[2] for r in pairs]
    pos = [(r[2], r[0], r[1]) for r in pairs if r[2] > 0]
    least_pos = min(pos) if pos else None
    least = min((r[2], r[0], r[1]) for r in pairs) if pairs else None
    allc = [(c, k, w) for k, w, c, _, _, _ in wall_rows]
    posc = [x for x in allc if x[0] > 0]
    least_posc = min(posc) if posc else None

    margin_list = "".join(f"{i} {j} {frac_str(m)}\n" for i, j, m, _, _, _ in pairs)
    clear_list = "".join(f"{k} {w} {frac_str(c)}\n" for k, w, c, _, _, _ in wall_rows)

    def below(vals: list[Fraction], th: Fraction) -> int:
        return sum(1 for v in vals if 0 < v < th)

    ths = {"1e-15": Fraction(1, 10**15), "1e-12": Fraction(1, 10**12),
           "1e-10": Fraction(1, 10**10), "1e-9": Fraction(1, 10**9),
           "1e-6": Fraction(1, 10**6), "1e-3": Fraction(1, 10**3)}
    walls_touched = sorted({w for _, w in contacts}, key=WALLS.index)
    least_by_wall = {}
    for w in WALLS:
        vals = [(c, k) for c, k, ww in allc if ww == w]
        c, k = min(vals)
        least_by_wall[w] = {"square": k, "clearance": frac_str(c), "approx": sci(c)}

    out = {
        "verdict": "ACCEPT" if ok else "REFUSE",
        "n": n,
        "side": frac_str(Fraction(*s)),
        "squares_unit_by_A": sum(unit_a),
        "squares_unit_by_B": sum(unit_b),
        "squares_ccw_by_B": sum(ccw_b),
        "squares_area_in_box_exactly_1": n - len(not_inside),
        "not_inside_by_B_area": not_inside,
        "pairs_decided": len(pairs),
        "pairs_class_counts_A": {c: sum(1 for r in pairs if r[3] == c) for c in ("apart", "contact", "overlap")},
        "pairs_class_counts_B": {c: sum(1 for r in pairs if r[4] == c) for c in ("apart", "contact", "overlap")},
        "pair_class_disagreements": pair_disagree,
        "overlapping_pairs": overlapping,
        "touching_pairs": touching,
        "sum_overlap_area_B": frac_str(Fraction(int(total_overlap_area.numerator), int(total_overlap_area.denominator))),
        "least_margin": None if least is None else {"pair": [least[1], least[2]], "margin": frac_str(least[0]), "approx": sci(least[0])},
        "least_positive_margin": None if least_pos is None else {"pair": [least_pos[1], least_pos[2]], "margin": frac_str(least_pos[0]), "approx": sci(least_pos[0])},
        "positive_pairs_below": {k: below(margins, v) for k, v in ths.items()},
        "square_wall_pairs_decided": len(wall_rows),
        "wall_class_disagreements": wall_disagree,
        "wall_contacts": contacts,
        "walls_touched": walls_touched,
        "wall_crossings": crossing,
        "least_clearance_by_wall": least_by_wall,
        "least_positive_clearance": None if least_posc is None else {"square": least_posc[1], "wall": least_posc[2], "clearance": frac_str(least_posc[0]), "approx": sci(least_posc[0])},
        "positive_clearances_below": {k: below([c for c, _, _ in allc], v) for k, v in ths.items()},
        "margin_list_sha256": hashlib.sha256(margin_list.encode()).hexdigest(),
        "clearance_list_sha256": hashlib.sha256(clear_list.encode()).hexdigest(),
    }
    if keep_lists:
        out["_pairs"] = pairs
        out["_walls"] = wall_rows
        out["_clear"] = clear_a
    return out


def public(result: dict) -> dict:
    return {k: v for k, v in result.items() if not k.startswith("_")}
