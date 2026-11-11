"""Lane L109's plan facts: the exact facts the controls plan states its outcomes from.

Usage: python -I -B l109_plan_facts.py CERT.yaml TWIN.json OUT.json

It decides no modified file. From the certificate as read by the frozen reader, it
computes every square's four exact wall clearances (method A's arithmetic), the side's
12-place floor and ceiling, which squares lie nearer the far walls than each side drop
the plan uses, each near pair's exact closing time along its centre line (and whether the
move is shorter than every other margin and wall clearance of the moved square), and each
square's nearest wall.
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction as Q

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l109_axes as A  # noqa: E402
import l109_check as C  # noqa: E402
import l109_geom as G  # noqa: E402
import l109_reader as R  # noqa: E402

E = Q(1, 10**30)
PROGRAMS = ["l109_reader.py", "l109_axes.py", "l109_check.py", "l109_geom.py", "l109_plan_facts.py"]


def ap(q: Q) -> str:
    return f"{float(q):.12e}"


def main() -> int:
    cert, twin, out = sys.argv[1], sys.argv[2], sys.argv[3]
    rd = R.read_files(cert, twin)
    side = Q(rd.side[0], rd.side[1])
    pts = [[(Q(*x), Q(*y)) for x, y in sq] for sq in rd.corners]
    sq = [A.make(p) for p in pts]
    n = len(sq)
    cl = [A.walls(s, side) for s in sq]
    f12 = int(side * 10**12)  # side > 0, so this is the floor
    floor12 = Q(f12, 10**12)
    c12 = f12 if floor12 == side else f12 + 1
    ceil12 = Q(c12, 10**12)
    drop = side - floor12
    one_q = Q(1, side.denominator)

    def far_below(d: Q) -> list[list[object]]:
        return [[i + 1, w] for i in range(n) for w in ("right", "top") if cl[i][w] < d]

    far_pos = sorted((cl[i][w], i + 1, w) for i in range(n) for w in ("right", "top") if cl[i][w] > 0)
    at_ceil = [[i + 1, w] for i in range(n) for w in A.WALLS if (cl[i][w] + (ceil12 - side if w in ("right", "top") else 0)) == 0]
    nearest = []
    for i in range(n):
        w = min(A.WALLS, key=lambda k: cl[i][k])
        nearest.append([i + 1, w, ap(cl[i][w]), cl[i][w] == 0])

    # all margins (method A arithmetic), kept per square for the move checks
    margins: dict[tuple[int, int], Q] = {}
    for i in range(n):
        for j in range(i + 1, n):
            margins[(i, j)] = A.margin(sq[i], sq[j])
    near = sorted((m, i, j) for (i, j), m in margins.items() if 0 < m < Q(1, 10**12))

    def other_min(k: int, excl: int) -> Q:
        vals = [margins[(min(k, x), max(k, x))] for x in range(n) if x not in (k, excl)]
        vals += [cl[k][w] for w in A.WALLS]
        return min(vals)

    pair_facts = []
    for m, i, j in near:
        # move the second square toward the first; if that move is not shorter than its
        # other margins and wall clearances, try moving the first toward the second
        chosen = None
        for mover, still in ((j, i), (i, j)):
            info = G.close_along_centres(pts[still], pts[mover], E)
            t1, d = info["t1"], info["d"]
            assert isinstance(t1, Q) and isinstance(d, tuple)
            len2_t1 = info["len2_t1"]
            assert isinstance(len2_t1, Q)
            om = other_min(mover, still)
            # translation by a vector of length L changes each gap by at most L, so the
            # other margins and clearances keep their class when L < om
            shorter = om > 0 and len2_t1 < om * om
            rec = {
                "pair": [i + 1, j + 1],
                "margin": ap(m),
                "mover": mover + 1,
                "still": still + 1,
                "t0": ap(info["t0"]),  # type: ignore[arg-type]
                "move_len_t1": f"{float(len2_t1) ** 0.5:.6e}",
                "other_min_of_mover": ap(om),
                "move_shorter_than_other_margins": shorter,
                "margin_at_past_is_minus_1e-30": info["margin_at_t1"] == -E,
            }
            if shorter:
                chosen = rec
                break
            if chosen is None:
                chosen = rec
        pair_facts.append(chosen)
    least = pair_facts[0] if pair_facts else None

    facts = {
        "program": "l109_plan_facts.py",
        "programs_sha256": C.program_digests(PROGRAMS),
        "side_approx": f"{float(side):.15f}",
        "side_denominator_digits": len(str(side.denominator)),
        "floor12": f"{f12 // 10**12}.{f12 % 10**12:012d}",
        "ceil12": f"{c12 // 10**12}.{c12 % 10**12:012d}",
        "drop_to_floor12": ap(drop),
        "ceil12_less_side": ap(ceil12 - side),
        "one_over_q": ap(one_q),
        "far_wall_clearance_below_one_over_q": far_below(one_q),
        "far_wall_clearance_below_1e-30": far_below(E),
        "far_wall_clearance_below_drop": far_below(drop),
        "least_positive_far_wall_clearance": [far_pos[0][1], far_pos[0][2], ap(far_pos[0][0])],
        "contacts_at_ceil12": at_ceil,
        "wall_contacts": [[i + 1, w] for i in range(n) for w in A.WALLS if cl[i][w] == 0],
        "square_1_clearances": {w: ap(v) for w, v in cl[0].items()},
        "square_last_clearances": {w: ap(v) for w, v in cl[-1].items()},
        "near_pairs_count": len(near),
        "near_pairs_all_move_shorter": all(p["move_shorter_than_other_margins"] for p in pair_facts),
        "near_pairs_all_past_margin_exact": all(p["margin_at_past_is_minus_1e-30"] for p in pair_facts),
        "least_pair": least,
        "near_pairs": pair_facts,
        "nearest_walls": nearest,
        "squares_already_at_their_nearest_wall": [x[0] for x in nearest if x[3]],
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(facts, f, indent=1)
        f.write("\n")
    print(
        "facts:",
        f"near={len(near)}",
        f"all_shorter={facts['near_pairs_all_move_shorter']}",
        f"all_past_exact={facts['near_pairs_all_past_margin_exact']}",
        f"floor12={facts['floor12']}",
        f"ceil12={facts['ceil12']}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
