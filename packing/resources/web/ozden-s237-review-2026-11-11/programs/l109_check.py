"""Lane L109's checker: decides a corners Witness/v2 file by two exact methods.

Usage: python -I -B l109_check.py CERT.yaml TWIN.json OUT.json

Every square, every square-wall pair and every pair of squares is decided by method A
(``l109_axes``, separating axes in ``fractions.Fraction``) and by method B
(``l109_clip``, exact clipping in ``gmpy2.mpq``), with no distance filter. The two
share only the reader (``l109_reader``), which hands them integers. The verdict is
ACCEPT only when both methods accept every square, wall and pair and their three-way
classes (apart, contact, overlap; clear, contact, outside) agree everywhere.

Imports nothing from the repository or the source.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from fractions import Fraction as Q
from typing import Any

import gmpy2
from gmpy2 import mpq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l109_axes as A  # noqa: E402
import l109_clip as B  # noqa: E402
import l109_reader as R  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PROGRAMS = ["l109_reader.py", "l109_axes.py", "l109_clip.py", "l109_check.py"]
THRESHOLDS = [Q(1, 10**k) for k in (15, 13, 12, 9, 6, 3)]
THRESHOLD_NAMES = ["1e-15", "1e-13", "1e-12", "1e-9", "1e-6", "1e-3"]


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def program_digests(names: list[str]) -> dict[str, str]:
    return {n: sha256_file(os.path.join(HERE, n)) for n in names}


def approx(q: Q | int) -> str:
    return f"{float(q):.12e}"


def exact(q: Q) -> str:
    return f"{q.numerator}/{q.denominator}" if q.denominator != 1 else str(q.numerator)


def to_q(r: tuple[int, int]) -> Q:
    return Q(r[0], r[1])


def build(corners: list[list[tuple[tuple[int, int], tuple[int, int]]]]):
    """Both methods' squares; a failure is recorded, not raised."""
    sa: list[A.SquareA | None] = []
    sb: list[B.SquareB | None] = []
    fails: list[dict[str, Any]] = []
    for i, pts in enumerate(corners, start=1):
        qa = [(to_q(x), to_q(y)) for x, y in pts]
        qb = [(B.as_mpq(x), B.as_mpq(y)) for x, y in pts]
        a_ok = b_ok = True
        try:
            sa.append(A.make(qa))
        except A.NotUnit as exc:
            sa.append(None)
            a_ok = False
            fails.append({"square": i, "method": "A", "why": str(exc)})
        try:
            sb.append(B.make(qb))
        except B.NotUnit as exc:
            sb.append(None)
            b_ok = False
            fails.append({"square": i, "method": "B", "why": str(exc)})
        if a_ok != b_ok:
            fails.append({"square": i, "method": "both", "why": "methods disagree on the unit square"})
    return sa, sb, fails


def decide_pair(a1: A.SquareA, a2: A.SquareA, b1: B.SquareB, b2: B.SquareB) -> tuple[Q, str, str, mpq]:
    m = A.margin(a1, a2)
    cb, ar = B.pair(b1, b2)
    return m, A.sign_class(m), cb, ar


def decide_walls(a: A.SquareA, b: B.SquareB, side_q: Q, side_m: mpq) -> dict[str, tuple[Q, str, str, mpq]]:
    cl = A.walls(a, side_q)
    outer = B.outer_walls(side_m)
    out = {}
    for w in A.WALLS:
        cb, ar = B.wall(b, outer[w])
        out[w] = (cl[w], A.wall_class(cl[w]), cb, ar)
    return out


def decide(
    side: tuple[int, int],
    corners: list[list[tuple[tuple[int, int], tuple[int, int]]]],
    pairs: list[tuple[int, int]] | None = None,
    squares: list[int] | None = None,
    keep_margins: bool = False,
) -> dict[str, Any]:
    """Decide the given pairs and squares' walls (all of them when None), 0-based indices."""
    n = len(corners)
    side_q = to_q(side)
    side_m = B.as_mpq(side)
    sa, sb, fails = build(corners)
    unit_ok = not fails
    sq_idx = list(range(n)) if squares is None else squares
    pr_idx = [(i, j) for i in range(n) for j in range(i + 1, n)] if pairs is None else pairs
    wall_rows: list[dict[str, Any]] = []
    wall_disagree: list[Any] = []
    outside: list[Any] = []
    inside_b_fail: list[int] = []
    for i in sq_idx:
        a, b = sa[i], sb[i]
        if a is None or b is None:
            continue
        ws = decide_walls(a, b, side_q, side_m)
        for w, (cl, ca, cb, ar) in ws.items():
            if ca != cb:
                wall_disagree.append([i + 1, w, ca, cb])
            if ca == "outside" or cb == "outside":
                outside.append([i + 1, w, ca, cb])
            wall_rows.append({"square": i + 1, "wall": w, "clearance": cl, "class": ca, "area_b": ar})
        ib = B.inside(b, side_m)
        a_in = all(v[0] >= 0 for v in ws.values())
        if ib != a_in:
            wall_disagree.append([i + 1, "inside", a_in, ib])
        if not ib:
            inside_b_fail.append(i + 1)
    pair_disagree: list[Any] = []
    overlaps: list[Any] = []
    contacts: list[Any] = []
    margins: list[tuple[int, int, Q]] = []
    area_sum = mpq(0)
    least: tuple[Q, int, int] | None = None
    counts = [0] * len(THRESHOLDS)
    hasher = hashlib.sha256()
    for i, j in pr_idx:
        a1, a2, b1, b2 = sa[i], sa[j], sb[i], sb[j]
        if a1 is None or a2 is None or b1 is None or b2 is None:
            continue
        m, ca, cb, ar = decide_pair(a1, a2, b1, b2)
        area_sum += ar
        hasher.update(f"{i + 1} {j + 1} {exact(m)}\n".encode())
        if ca != cb:
            pair_disagree.append([i + 1, j + 1, ca, cb])
        if ca == "overlap" or cb == "overlap":
            overlaps.append([i + 1, j + 1, approx(m), str(ar)[:60]])
        elif ca == "contact" or cb == "contact":
            contacts.append([i + 1, j + 1])
        if m > 0:
            if least is None or m < least[0]:
                least = (m, i + 1, j + 1)
            for k, t in enumerate(THRESHOLDS):
                if m < t:
                    counts[k] += 1
        if keep_margins:
            margins.append((i + 1, j + 1, m))
    accept = (
        unit_ok
        and not wall_disagree
        and not outside
        and not inside_b_fail
        and not pair_disagree
        and not overlaps
    )
    pos_walls = sorted((r for r in wall_rows if r["clearance"] > 0), key=lambda r: r["clearance"])
    wall_counts = [sum(1 for r in pos_walls if r["clearance"] < t) for t in THRESHOLDS]
    res: dict[str, Any] = {
        "verdict": "ACCEPT" if accept else "REFUSE",
        "squares_decided": len(sq_idx),
        "pairs_decided": len(pr_idx),
        "unit_failures": fails,
        "ccw_squares": sum(1 for a in sa if a is not None and a.ccw),
        "cw_squares": sum(1 for a in sa if a is not None and not a.ccw),
        "wall_disagreements": wall_disagree,
        "outside": outside,
        "inside_b_failures": inside_b_fail,
        "wall_contacts": [[r["square"], r["wall"]] for r in wall_rows if r["class"] == "contact"],
        "least_positive_wall_clearance": (
            {"square": pos_walls[0]["square"], "wall": pos_walls[0]["wall"], "approx": approx(pos_walls[0]["clearance"])}
            if pos_walls
            else None
        ),
        "positive_wall_clearances_below": dict(zip(THRESHOLD_NAMES, wall_counts, strict=True)),
        "pair_disagreements": pair_disagree,
        "overlapping_pairs": overlaps,
        "touching_pairs": contacts,
        "sum_of_clipped_pair_areas": str(area_sum),
        "least_positive_margin": (
            {"pair": [least[1], least[2]], "approx": approx(least[0]), "exact": exact(least[0])} if least else None
        ),
        "positive_margins_below": dict(zip(THRESHOLD_NAMES, counts, strict=True)),
        "margin_list_sha256": hasher.hexdigest(),
    }
    res["_wall_rows"] = wall_rows
    res["_margins"] = margins
    return res


def main() -> int:
    cert, twin, out = sys.argv[1], sys.argv[2], sys.argv[3]
    t0 = time.process_time()
    rd = R.read_files(cert, twin)
    res = decide(rd.side, rd.corners, keep_margins=True)
    wall_rows = res.pop("_wall_rows")
    margins = res.pop("_margins")
    near = sorted((m for m in margins if m[2] < Q(1, 10**12)), key=lambda m: m[2])
    near_walls = [r for r in wall_rows if 0 < r["clearance"] < Q(1, 10**9)]
    side_q = to_q(rd.side)
    receipt = {
        "program": "l109_check.py",
        "programs_sha256": program_digests(PROGRAMS),
        "python": sys.version.split()[0],
        "gmpy2": gmpy2.version(),
        "certificate": os.path.basename(cert),
        "certificate_sha256": sha256_file(cert),
        "twin": os.path.basename(twin),
        "twin_sha256": sha256_file(twin),
        "read": {
            "n": rd.n,
            "scalars": rd.scalars,
            "integer_scalars": rd.integer_scalars,
            "side_digits": [len(str(rd.side[0])), len(str(rd.side[1]))],
            "side_approx": f"{float(side_q):.15f}",
            "twin_equal": True,
        },
        **res,
        "pairs_below_1e-12": [[i, j, approx(m)] for i, j, m in near],
        "walls_below_1e-9": [[r["square"], r["wall"], approx(r["clearance"])] for r in near_walls],
        "walls_contact": [[r["square"], r["wall"]] for r in wall_rows if r["clearance"] == 0],
        "cpu_seconds": round(time.process_time() - t0, 1),
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=1)
        f.write("\n")
    print(
        receipt["verdict"],
        f"pairs={res['pairs_decided']}",
        f"least={res['least_positive_margin']}",
        f"contacts={res['wall_contacts']}",
        f"cpu={receipt['cpu_seconds']}s",
    )
    return 0 if receipt["verdict"] == "ACCEPT" else 1


if __name__ == "__main__":
    raise SystemExit(main())
