"""Decide a packing with both methods of the L70 review, and write a receipt.

Clean room (9 November 2026). Every square, every wall and every pair is decided by
method A (``l70_sat``, separating axes in ``Fraction``) and by method B
(``l70_clip``, exact clipped areas in ``gmpy2.mpq``), with no distance filter. The
two share only the reader (``l70_reader``), which returns integers.

The verdict is ACCEPT exactly when both methods find every square a unit square
inside ``[0, S]^2`` and no two interiors meeting, and they agree on every square's
containment, every wall contact and every pair's class (apart, touch, overlap).

Usage (from any directory; the script puts its own directory first on sys.path)::

    python -I l70_check.py FILE --format cert|corners [--sense ccw|cw]
        --label NAME --out RECEIPT.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import l70_clip as B  # noqa: E402
import l70_reader as R  # noqa: E402
import l70_sat as A  # noqa: E402
from gmpy2 import mpq  # noqa: E402

CHECKER_FILES = ("l70_reader.py", "l70_sat.py", "l70_clip.py", "l70_check.py")
NEAR = Fraction(1, 10**9)
WALLS = ("left", "bottom", "right", "top")


def file_digests(names: tuple[str, ...] = CHECKER_FILES) -> dict[str, str]:
    return {nm: hashlib.sha256((HERE / nm).read_bytes()).hexdigest() for nm in names}


def frac_str(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def floor_places(x: Fraction, k: int) -> str:
    sign = "-" if x < 0 else ""
    ax = -x if x < 0 else x
    v = (ax.numerator * 10**k) // ax.denominator
    if sign:  # floor of a negative number rounds away from zero
        if (ax.numerator * 10**k) % ax.denominator:
            v += 1
    s = str(v).rjust(k + 1, "0")
    return f"{sign}{s[:-k]}.{s[-k:]}" if k else f"{sign}{s}"


def ceil_places(x: Fraction, k: int) -> str:
    """Round up at k places: ceil(x) = -floor(-x)."""
    s = floor_places(-x, k)
    if s.startswith("-"):
        return s[1:]
    return s if set(s) <= {"0", "."} else "-" + s


def mpq_to_fraction(v: Any) -> Fraction:
    q = mpq(v)
    return Fraction(int(q.numerator), int(q.denominator))


def decide(pk: R.Packing, keep_near: bool = True) -> dict[str, Any]:
    """Decide one packing by both methods; return the full result (no file metadata)."""
    t0 = time.process_time()
    side_f = Fraction(pk.side[0], pk.side[1])
    side_q = mpq(pk.side[0], pk.side[1])
    n = pk.n
    ids = pk.ids
    # ---------------- method A
    ta = time.process_time()
    sa = A.build(pk)
    a_unit_bad = [ids[i] for i, s in enumerate(sa) if not s.unit]
    a_sense = {"ccw": 0, "cw": 0, "none": 0}
    for s in sa:
        a_sense[s.sense] += 1
    a_out: list[str] = []
    least: dict[str, tuple[Fraction, list[str]] | None] = {w: None for w in WALLS}
    a_contacts: dict[str, list[str]] = {w: [] for w in WALLS}
    near_walls: list[list[Any]] = []
    sq_wall_below_1e12 = 0
    for i, s in enumerate(sa):
        cl = A.wall_clearances(s, side_f)
        if min(cl) < 0:
            a_out.append(ids[i])
        for w, v in zip(WALLS, cl, strict=True):
            cur = least[w]
            if cur is None or v < cur[0]:
                least[w] = (v, [ids[i]])
            elif v == cur[0]:
                cur[1].append(ids[i])
            if v == 0:
                a_contacts[w].append(ids[i])
            if v < Fraction(1, 10**12):
                sq_wall_below_1e12 += 1
            if v < NEAR:
                near_walls.append([ids[i], w, v])
    a_touch: set[tuple[int, int]] = set()
    a_overlap: set[tuple[int, int]] = set()
    a_least: tuple[Fraction, int, int, int] | None = None
    below = {"1e-12": 0, "1e-10": 0, "1e-9": 0}
    th = {"1e-12": Fraction(1, 10**12), "1e-10": Fraction(1, 10**10), "1e-9": NEAR}
    near_pairs: list[list[Any]] = []
    overlap_depth: Fraction | None = None
    for i in range(n):
        si = sa[i]
        for j in range(i + 1, n):
            m, k = A.pair_margin(si, sa[j])
            if a_least is None or m < a_least[0]:
                a_least = (m, i, j, k)
            if m <= 0:
                if m == 0:
                    a_touch.add((i, j))
                else:
                    a_overlap.add((i, j))
                    if overlap_depth is None or m < overlap_depth:
                        overlap_depth = m
            for key, lim in th.items():
                if m < lim:
                    below[key] += 1
            if keep_near and m < NEAR:
                near_pairs.append([ids[i], ids[j], m, k])
    ta = time.process_time() - ta
    # extent (method A corners)
    minx = min(s.minx for s in sa)
    miny = min(s.miny for s in sa)
    maxx = max(s.maxx for s in sa)
    maxy = max(s.maxy for s in sa)
    # ---------------- method B
    tb = time.process_time()
    sb = B.build(pk)
    b_unit_bad = [ids[i] for i, s in enumerate(sb) if not s.unit]
    b_out = [ids[i] for i, s in enumerate(sb) if not B.inside_box(s, side_q)]
    b_contacts: dict[str, list[str]] = {w: [] for w in WALLS}
    for i, s in enumerate(sb):
        for w, hit in zip(WALLS, B.wall_touches(s, side_q), strict=True):
            if hit:
                b_contacts[w].append(ids[i])
    b_touch: set[tuple[int, int]] = set()
    b_overlap: set[tuple[int, int]] = set()
    b_max_area = mpq(0)
    for i in range(n):
        si = sb[i]
        for j in range(i + 1, n):
            cls, ar = B.pair_class(si, sb[j])
            if cls == "touch":
                b_touch.add((i, j))
            elif cls == "overlap":
                b_overlap.add((i, j))
                if ar > b_max_area:
                    b_max_area = ar
    tb = time.process_time() - tb
    # ---------------- agreement
    agree = {
        "unit": a_unit_bad == b_unit_bad,
        "inside": a_out == b_out,
        "wall_contacts": all(a_contacts[w] == b_contacts[w] for w in WALLS),
        "pair_touch": a_touch == b_touch,
        "pair_overlap": a_overlap == b_overlap,
    }
    reasons = []
    if a_unit_bad or b_unit_bad:
        reasons.append("not every square is a unit square")
    if a_out or b_out:
        reasons.append("a square is outside the box")
    if a_overlap or b_overlap:
        reasons.append("interiors meet")
    if not all(agree.values()):
        reasons.append("methods disagree")
    verdict = "ACCEPT" if not reasons else "REFUSE"
    pairs = n * (n - 1) // 2

    def pl(s: set[tuple[int, int]], cap: int = 60) -> list[list[str]]:
        return [[ids[i], ids[j]] for (i, j) in sorted(s)[:cap]]

    # near lists: exact for the 40 smallest, binary64 for the rest (receipts stay small)
    near_pairs.sort(key=lambda e: e[2])
    near_pairs_out = [
        [e[0], e[1], frac_str(e[2]) if r < 40 else None, float(e[2]), e[3]] for r, e in enumerate(near_pairs)
    ]
    near_walls.sort(key=lambda e: e[2])
    near_walls_out = [[e[0], e[1], frac_str(e[2]) if r < 40 else None, float(e[2])] for r, e in enumerate(near_walls)]

    assert a_least is not None or n < 2
    res: dict[str, Any] = {
        "n": n,
        "side": frac_str(side_f),
        "side_denominator_digits": len(str(side_f.denominator)),
        "side_floor_40": floor_places(side_f, 40),
        "side_ceil_12": ceil_places(side_f, 12),
        "side_ceil_16": ceil_places(side_f, 16),
        "verdict": verdict,
        "reasons": reasons,
        "agree": agree,
        "pairs": pairs,
        "A": {
            "method": "separating axes over the four edge normals, fractions.Fraction",
            "not_unit": a_unit_bad,
            "listing_sense": a_sense,
            "outside": a_out,
            "walls": {
                w: {
                    "least": frac_str(least[w][0]),  # type: ignore[index]
                    "least_float": float(least[w][0]),  # type: ignore[index]
                    "at": least[w][1][:20],  # type: ignore[index]
                    "contacts": a_contacts[w],
                }
                for w in WALLS
            },
            "square_wall_pairs_below_1e-12": sq_wall_below_1e12,
            "extent": {
                "min_x": frac_str(minx),
                "min_y": frac_str(miny),
                "side_minus_max_x": frac_str(side_f - maxx),
                "side_minus_max_y": frac_str(side_f - maxy),
                "side_minus_max_x_float": float(side_f - maxx),
                "side_minus_max_y_float": float(side_f - maxy),
                "min_x_float": float(minx),
                "min_y_float": float(miny),
            },
            "classes": {
                "apart": pairs - len(a_touch) - len(a_overlap),
                "touch": len(a_touch),
                "overlap": len(a_overlap),
            },
            "least_margin": frac_str(a_least[0]) if a_least else None,
            "least_margin_float": float(a_least[0]) if a_least else None,
            "least_pair": [ids[a_least[1]], ids[a_least[2]]] if a_least else None,
            "least_pair_normal": a_least[3] if a_least else None,
            "pairs_below": below,
            "touching_pairs": pl(a_touch),
            "overlapping_pairs": pl(a_overlap),
            "deepest_overlap_margin_float": float(overlap_depth) if overlap_depth is not None else None,
            "cpu_seconds": round(ta, 3),
        },
        "B": {
            "method": "Sutherland-Hodgman clipping and shoelace areas, gmpy2.mpq",
            "not_unit": b_unit_bad,
            "outside": b_out,
            "wall_contacts": b_contacts,
            "classes": {
                "apart": pairs - len(b_touch) - len(b_overlap),
                "touch": len(b_touch),
                "overlap": len(b_overlap),
            },
            "touching_pairs": pl(b_touch),
            "overlapping_pairs": pl(b_overlap),
            "largest_overlap_area_float": float(b_max_area),
            "cpu_seconds": round(tb, 3),
        },
        "near_pairs_below_1e-9": near_pairs_out if keep_near else None,
        "near_walls_below_1e-9": near_walls_out if keep_near else None,
        "near_format": "[id, id, exact margin (40 smallest) or null, binary64 margin, normal 0-3: a.e1, a.e2, b.e1, b.e2]",
        "cpu_seconds_total": round(time.process_time() - t0, 3),
    }
    return res


def read(path: str, fmt: str, sense: str) -> R.Packing:
    if fmt == "cert":
        return R.read_cert(path, sense=sense)
    if fmt == "corners":
        return R.read_corners_yaml(path, sense=sense)
    raise SystemExit(f"unknown format {fmt}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--format", required=True, choices=("cert", "corners"))
    ap.add_argument("--sense", default="ccw", choices=("ccw", "cw"))
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True)
    ns = ap.parse_args(argv)
    t0 = time.process_time()
    try:
        pk = read(ns.path, ns.format, ns.sense)
    except R.ReadError as exc:
        receipt = {"label": ns.label, "verdict": "REFUSE", "reasons": [f"reader: {exc}"]}
        receipt["program_digests"] = file_digests()
        Path(ns.out).write_text(json.dumps(receipt, indent=1) + "\n")
        print(ns.label, "REFUSE (reader)", exc)
        return 0
    res = decide(pk)
    receipt = {
        "label": ns.label,
        "program": "l70_check.py",
        "program_digests": file_digests(),
        "python": sys.version.split()[0],
        "gmpy2": B.version(),
        "input": pk.meta,
        **res,
        "cpu_seconds_with_read": round(time.process_time() - t0, 3),
    }
    Path(ns.out).write_text(json.dumps(receipt, indent=1) + "\n")
    print(
        ns.label,
        res["verdict"],
        "least margin",
        res["A"]["least_margin_float"],
        "pair",
        res["A"]["least_pair"],
        "classes A",
        res["A"]["classes"],
        "B",
        res["B"]["classes"],
        "cpu",
        res["cpu_seconds_total"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
