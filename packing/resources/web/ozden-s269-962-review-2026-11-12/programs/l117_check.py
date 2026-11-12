"""Lane L117: decide a corners/rational Witness/v2 certificate by two methods.

Clean-room code for the stage 4 review of jlevy/squares#962. Every square, every wall
and every pair is decided by method A (l117_sat, separating axes in Python integers)
and method B (l117_hull, hull of the intersection in gmpy2 rationals), with no distance
filter. The two share only the reader's integers. The verdict is ACCEPT only when both
methods accept every square, wall and pair, their classes agree everywhere, and their
listing senses agree.

Usage: python -I -B l117_check.py CERT.yaml TWIN.json OUT.json
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l117_hull as hb  # noqa: E402
import l117_reader as rd  # noqa: E402
import l117_sat as sa  # noqa: E402

THRESHOLDS = ["1e-15", "1e-13", "1e-12", "1e-9", "1e-6", "1e-3"]


def sci(x: Fraction, digits: int = 15) -> str:
    """x in scientific notation, truncated toward zero to `digits` significant digits."""
    if x == 0:
        return "0"
    sign = "-" if x < 0 else ""
    a = abs(x)
    e = len(str(a.numerator // a.denominator)) - 1 if a >= 1 else 0
    if a < 1:
        e = -1
        while a * Fraction(10) ** (-e) < 1:
            e -= 1
    m = a / Fraction(10) ** e
    mi = int(m * 10 ** (digits - 1))
    s = str(mi)
    return f"{sign}{s[0]}.{s[1:]}e{e:+d}"


def floor_places(x: Fraction, k: int) -> str:
    """x truncated toward minus infinity at k decimal places (x >= 0)."""
    f = (x.numerator * 10**k) // x.denominator
    s = str(f).rjust(k + 1, "0")
    return f"{s[:-k]}.{s[-k:]}"


def ceil_places(x: Fraction, k: int) -> str:
    f = -((-x.numerator * 10**k) // x.denominator)
    s = str(f).rjust(k + 1, "0")
    return f"{s[:-k]}.{s[-k:]}"


def frac_str(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


class Model:
    """Both methods' views of one packing."""

    def __init__(self, side: tuple[int, int], squares: list[list[sa.Corner]]) -> None:
        self.n = len(squares)
        self.side = Fraction(side[0], side[1])
        self.side_q = hb.mpq(side[0], side[1])
        self.A = [sa.SquareA(c) for c in squares]
        self.Bpts = [hb.to_points(c) for c in squares]
        self.Bsense = [hb.unit_sense(p) for p in self.Bpts]
        self.Bccw = [hb.ccw(p) for p in self.Bpts]
        self.slab = hb.slabs(self.side_q)

    def pair(self, i: int, j: int) -> tuple[str, str, Fraction | None, object]:
        """(class A, class B, margin A, overlap area B) for 0-based i < j."""
        a, b = self.A[i], self.A[j]
        m = sa.pair_margin(a, b) if (a.unit and b.unit) else None
        ca = sa.pair_class(m) if m is not None else "not-unit"
        cb, area = hb.classify(self.Bccw[i], self.Bccw[j])
        return ca, cb, m, area

    def walls(self, i: int) -> tuple[dict[str, Fraction], dict[str, str], dict[str, str], bool]:
        cl = sa.wall_clearances(self.A[i], self.side)
        ca = {k: sa.wall_class(v) for k, v in cl.items()}
        cb, centre_in = hb.walls(self.Bccw[i], self.side_q, self.slab)
        return cl, ca, cb, centre_in


def decide(
    side: tuple[int, int],
    squares: list[list[sa.Corner]],
    pairs: list[tuple[int, int]] | None = None,
    wall_squares: list[int] | None = None,
    keep_margins: bool = False,
) -> dict[str, object]:
    """Decide squares, walls and pairs (0-based); None means all of them."""
    t0 = time.process_time()
    M = Model(side, squares)
    n = M.n
    sq_rows = []
    unit_a = unit_b = sense_agree = 0
    for i in range(n):
        sA, sB = M.A[i].sense, M.Bsense[i]
        unit_a += sA != 0
        unit_b += sB != 0
        sense_agree += sA == sB
        sq_rows.append((sA, sB))
    all_unit = unit_a == n and unit_b == n and sense_agree == n

    wl = range(n) if wall_squares is None else wall_squares
    wall_rows: dict[int, dict[str, object]] = {}
    wall_disagree = 0
    outside_a: list[list[object]] = []
    outside_b: list[list[object]] = []
    centre_out: list[int] = []
    contacts: list[list[object]] = []
    positive: list[tuple[Fraction, int, str]] = []
    for i in wl:
        cl, ca, cb, cin = M.walls(i)
        wall_rows[i] = {"clear": cl, "A": ca, "B": cb, "centre_in": cin}
        if not cin:
            centre_out.append(i + 1)
        for w in ("left", "bottom", "right", "top"):
            if ca[w] != cb[w]:
                wall_disagree += 1
            if ca[w] == "outside":
                outside_a.append([i + 1, w])
            if cb[w] == "outside":
                outside_b.append([i + 1, w])
            if ca[w] == "contact":
                contacts.append([i + 1, w])
            elif cl[w] > 0:
                positive.append((cl[w], i + 1, w))
    tA = time.process_time()

    pl = [(i, j) for i in range(n) for j in range(i + 1, n)] if pairs is None else pairs
    disagree: list[list[object]] = []
    over_a: list[list[int]] = []
    over_b: list[list[int]] = []
    touch_a: list[list[int]] = []
    touch_b: list[list[int]] = []
    least: tuple[Fraction, int, int] | None = None
    margins: dict[tuple[int, int], Fraction] = {}
    area_sum = hb.mpq(0)
    h = hashlib.sha256()
    for i, j in pl:
        ca, cb, m, area = M.pair(i, j)
        area_sum += area
        if ca != cb:
            disagree.append([i + 1, j + 1, ca, cb])
        if ca == "overlap":
            over_a.append([i + 1, j + 1])
        if cb == "overlap":
            over_b.append([i + 1, j + 1])
        if ca == "contact":
            touch_a.append([i + 1, j + 1])
        if cb == "contact":
            touch_b.append([i + 1, j + 1])
        if m is not None:
            h.update(f"{i + 1} {j + 1} {frac_str(m)}\n".encode())
            if least is None or m < least[0]:
                least = (m, i + 1, j + 1)
            if keep_margins:
                margins[(i, j)] = m
    t1 = time.process_time()

    accept = (
        all_unit
        and not outside_a
        and not outside_b
        and not centre_out
        and wall_disagree == 0
        and not over_a
        and not over_b
        and not disagree
    )
    positive.sort()
    out: dict[str, object] = {
        "verdict": "ACCEPT" if accept else "REFUSE",
        "n": n,
        "side": frac_str(M.side),
        "squares": {
            "unit_by_A": unit_a,
            "unit_by_B": unit_b,
            "senses_agree": sense_agree,
            "counterclockwise": sum(1 for a, b in sq_rows if a == 1 and b == 1),
            "clockwise": sum(1 for a, b in sq_rows if a == -1 and b == -1),
            "not_unit_A": [k + 1 for k, (a, _) in enumerate(sq_rows) if a == 0],
            "not_unit_B": [k + 1 for k, (_, b) in enumerate(sq_rows) if b == 0],
        },
        "walls": {
            "squares_decided": len(wall_rows),
            "square_wall_pairs": 4 * len(wall_rows),
            "class_disagreements": wall_disagree,
            "outside_A": outside_a,
            "outside_B": outside_b,
            "centre_outside_B": centre_out,
            "contacts": contacts,
            "least_positive": (
                [positive[0][1], positive[0][2], frac_str(positive[0][0]), sci(positive[0][0])]
                if positive
                else None
            ),
            "positive_below": {t: sum(1 for c, _, _ in positive if c < Fraction(t)) for t in THRESHOLDS},
            "positive_below_1e-3": [[k, w, sci(c, 6)] for c, k, w in positive if c < Fraction("1e-3")],
        },
        "pairs": {
            "decided": len(pl),
            "class_disagreements": disagree,
            "overlap_A": over_a,
            "overlap_B": over_b,
            "contact_A": touch_a,
            "contact_B": touch_b,
            "overlap_area_sum_B": str(area_sum),
            "least_margin": [least[1], least[2], frac_str(least[0]), sci(least[0])] if least else None,
            "margin_list_sha256": h.hexdigest(),
        },
        "cpu_seconds": {"squares_and_walls": round(tA - t0, 1), "pairs": round(t1 - tA, 1)},
    }
    if keep_margins:
        out["_margins"] = margins
        out["_walls"] = wall_rows
    return out


def near_pairs(margins: dict[tuple[int, int], Fraction]) -> dict[str, object]:
    below = {t: sum(1 for m in margins.values() if m < Fraction(t)) for t in THRESHOLDS}
    rows = sorted((m, i + 1, j + 1) for (i, j), m in margins.items() if m < Fraction("1e-3"))
    return {
        "below": below,
        "below_1e-3": [[i, j, sci(m, 6)] for m, i, j in rows],
    }


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main(argv: list[str]) -> int:
    ypath, jpath, opath = argv[1], argv[2], argv[3]
    rec = rd.read_files(ypath, jpath)
    side = rec["side"]
    squares = rec["squares"]
    assert isinstance(side, tuple) and isinstance(squares, list)
    res = decide(side, squares, keep_margins=True)
    margins = res.pop("_margins")
    res.pop("_walls")
    assert isinstance(margins, dict)
    meta = rec["meta"]
    assert isinstance(meta, dict)
    S = Fraction(side[0], side[1])
    receipt = {
        "program": "l117_check.py",
        "source": {
            "yaml": os.path.basename(ypath),
            "yaml_sha256": sha256_file(ypath),
            "json": os.path.basename(jpath),
            "json_sha256": sha256_file(jpath),
        },
        "reading": {
            "n": rec["n"],
            "ids_in_order": True,
            "scalars_read": meta["scalars_read"],
            "zero_scalars": meta["zero_scalars"],
            "side_digits": [len(str(side[0])), len(str(side[1]))],
            "side_floor_30": floor_places(S, 30),
            "twin_same_tree": True,
            "certificate_block": meta["certificate"],
        },
        **res,
        "near_pairs": near_pairs(margins),
    }
    with open(opath, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=1, sort_keys=False)
        fh.write("\n")
    p = receipt["pairs"]
    w = receipt["walls"]
    assert isinstance(p, dict) and isinstance(w, dict)
    print(receipt["verdict"], "n", rec["n"], "pairs", p["decided"], "least", p["least_margin"][0:2], p["least_margin"][3])
    print("contacts", w["contacts"], "least positive wall", w["least_positive"][0:2], w["least_positive"][3])
    return 0 if receipt["verdict"] == "ACCEPT" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
