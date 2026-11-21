"""C6 (after the freeze): locate real optimal packings in case 53's cut tree.

Usage: python -I r1050_locate.py --rack R --construction C --cases full-endpoint-mask-cases.json
           --out out.json

Written after checker freeze 2, with the source's cut semantics as read from its code
(split_variant.py, angle_split_variant.py, verify_full_endpoint_mask.py): a cut (j, t, v)
on the tile owning mark j means x <= v, x >= v, y <= v, y >= v for t = 0..3 (v in units
of 10^-6) and angle row < v, >= v for t = 4, 5, with B = 128 rows uniform in
t = tan(theta/2) over [0, 1] (theta the tile's angle mod pi/2). A slab (a, b) adds
y5 >= a, x15 >= a, x5 <= M - a, y15 <= M - a and y5 <= b. The packing is placed in
[0, U]^2 at offsets 0 and U - H, under each symmetry of the box that fixes case 53;
every tile is assigned its nearest mark exactly (r1050_q7). Each terminal that contains
an image is listed with its label: a real packing in a terminal labelled 'empty' would
refute that terminal. Decisions are exact in Q(sqrt 7).
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from r1050_orbits import nearest, sym_point, sym_vec  # noqa: E402
from r1050_q7 import Q7, Tile, load_construction  # noqa: E402
from r1050_rack import load_rack  # noqa: E402

B_ROWS = 128


def rows_of(t: Tile) -> set[int]:
    """Angle rows (closed, uniform in tan(theta/2) on [0, 1]) containing the tile's angle."""
    u = t.u
    # Representative axis in the closed first quadrant: rotate by quarter turns.
    for _ in range(4):
        if u[0] > 0 and not u[1] < 0:
            break
        u = (-u[1], u[0])
    cs, sn = u
    if sn == 0:
        return {0, B_ROWS - 1}  # theta = 0, the same orientation as theta = pi/2
    # t = sin / (1 + cos) in Q(sqrt 7); row k holds t in [k/B, (k+1)/B].
    out = set()
    for k in range(B_ROWS):
        lo, hi = Fraction(k, B_ROWS), Fraction(k + 1, B_ROWS)
        # lo <= sn/(1+cs) <= hi  <=>  lo (1+cs) <= sn <= hi (1+cs), since 1 + cs > 0.
        if (Q7(lo) * (Q7(1) + cs)) <= sn and sn <= (Q7(hi) * (Q7(1) + cs)):
            out.add(k)
    return out


def holds(tile: Tile, t: int, v: int, rows: set[int]) -> bool:
    val = Q7(Fraction(v, 10**6))
    x, y = tile.c
    if t == 0:
        return x <= val
    if t == 1:
        return x >= val
    if t == 2:
        return y <= val
    if t == 3:
        return y >= val
    if t == 4:
        return any(k < v for k in rows)
    return any(k >= v for k in rows)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rack", type=Path, required=True)
    ap.add_argument("--construction", type=Path, required=True)
    ap.add_argument("--cases", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    cap_f, scale, _e, lattice, _n = load_rack(a.rack)
    cap = Q7(cap_f)
    M = 4822876
    marks = [(Q7(Fraction(x) * cap_f / scale), Q7(Fraction(y) * cap_f / scale)) for x, y in lattice]
    side, base = load_construction(a.construction)
    rows_json = json.loads(a.cases.read_text())
    found = []
    for off in (Q7(0), cap - side):
        for k in range(8):
            tiles = []
            for t in base:
                c = (t.c[0] + off, t.c[1] + off)
                tiles.append(Tile(t.tid, sym_point(k, c, cap), sym_vec(k, t.u), sym_vec(k, t.v)))
            owner: dict[int, Tile] = {}
            for t in tiles:
                ks, _best = nearest(t, marks)
                assert len(ks) == 1
                owner[ks[0]] = t
            free = sorted(set(range(21)) - set(owner))
            if [lattice[i] for i in free] != [(617, 617), (1000, 1000), (1383, 1383)]:
                continue  # this symmetry does not fix the case's representative
            t5, t15 = owner[5], owner[15]
            tau = min(t5.c[1], t15.c[0], cap - t5.c[0], cap - t15.c[1])
            rows = {j: rows_of(t) for j, t in owner.items()}
            for a_, b_, terms in rows_json:
                base_cuts = ([(5, 3, a_), (15, 1, a_), (5, 0, M - a_), (15, 2, M - a_)] if a_ else [])
                base_cuts += [(5, 2, b_)] if b_ else []
                if not all(holds(owner[j], t, v, rows[j]) for j, t, v in base_cuts):
                    continue
                for p, r, out in terms:
                    cuts = [tuple(p[i:i + 3]) for i in range(0, len(p), 3)]
                    if all(holds(owner[j], t, v, rows[j]) for j, t, v in cuts):
                        found.append({"offset": float(off), "symmetry": k, "tau": float(tau),
                                      "slab": [a_, b_], "path": p, "params": r, "label": out})
    labels = sorted({json.dumps(f["label"]) for f in found})
    # The chord guard's roles (2,0,1,18,13,5,11) at the base placement: P is the upper-right
    # corner of the square owning mark 1, Q the lower-left corner of the square owning
    # mark 13 (its tip in the reflected frame). At equality |Q - P| = 2 and (Q - P)/2 is
    # the tilted axis, so each of the squares owning marks 5 and 11 is crossed by a chord
    # of length exactly 1.
    equality: dict[str, object] = {}
    owner0: dict[int, Tile] = {}
    for t in base:
        ks, _best = nearest(t, marks)
        owner0[ks[0]] = t
    if all(j in owner0 for j in (1, 13, 5, 11)):
        p1, q13 = owner0[1], owner0[13]
        half = Fraction(1, 2)
        P = (p1.c[0] + half, p1.c[1] + half) if p1.u[1] == 0 else None
        Q = (q13.c[0] - half, q13.c[1] - half) if q13.u[1] == 0 else None
        if P is not None and Q is not None:
            d = (Q[0] - P[0], Q[1] - P[1])
            n2 = d[0] * d[0] + d[1] * d[1]
            ax = owner0[5].u
            equality = {
                "P": [P[0].text(), P[1].text()], "Q": [Q[0].text(), Q[1].text()],
                "QP_squared": n2.text(), "QP_is_2": n2 == 4,
                "half_QP_is_tilted_axis_of_mark5_square": (d[0].scale(half) == ax[0]
                                                           and d[1].scale(half) == ax[1]),
                "projections_on_axis": {
                    str(j): [((P[0] - owner0[j].c[0]) * owner0[j].u[0]
                              + (P[1] - owner0[j].c[1]) * owner0[j].u[1]).text(),
                             ((Q[0] - owner0[j].c[0]) * owner0[j].u[0]
                              + (Q[1] - owner0[j].c[1]) * owner0[j].u[1]).text()]
                    for j in (5, 11)},
            }
    rep = {"program": "r1050_locate.py", "construction": str(a.construction.name),
           "terminals_found": len(found), "labels": labels,
           "any_empty_terminal": any(f["label"] == ["empty"] for f in found),
           "chord_equality_at_base_placement": equality,
           "found": found[:40]}
    a.out.write_text(json.dumps(rep, indent=1) + "\n")
    print(rep["construction"], "terminals", len(found), "labels", labels,
          "EMPTY_TERMINAL_HOLDS_A_PACKING" if rep["any_empty_terminal"] else "NO_EMPTY_TERMINAL_HOLDS_A_PACKING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
