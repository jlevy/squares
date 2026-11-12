"""Lane L117: the exact facts the controls plan states its outcomes from. Decides nothing.

Clean-room code for the stage 4 review of jlevy/squares#962. Reads the certificate (via
the frozen reader) and the frozen check receipt. Computes the wall clearances from the
corner extents, the side's 12-place floor and ceiling, the squares each side control
would push out, the closest pair's closing move against every other margin and
clearance of the moved square (closed form of l117_geom, on the unmodified file), and
each near pair's closing times. It decides no modified file.

Usage: python -I -B l117_plan_facts.py CERT.yaml TWIN.json CHECK.json CLAIM OUT.json
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l117_check as ck  # noqa: E402
import l117_geom as g  # noqa: E402
import l117_reader as rd  # noqa: E402

E30 = F(1, 10**30)
WALLS = ("left", "bottom", "right", "top")


def clearances(pts: list[g.Pt], S: F) -> dict[str, F]:
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return {"left": min(xs), "bottom": min(ys), "right": S - max(xs), "top": S - max(ys)}


def sqrt_sci(x2: F) -> str:
    """sqrt(x2) printed to 6 significant digits, via an exact integer square root."""
    r = math.isqrt(x2.numerator * 10**80 // x2.denominator)
    return ck.sci(F(r, 10**40), 6)


def main(argv: list[str]) -> int:
    ypath, jpath, cpath, claim, opath = argv[1:6]
    rec = rd.read_files(ypath, jpath)
    side = rec["side"]
    assert isinstance(side, tuple)
    S = F(side[0], side[1])
    sq = rec["squares"]
    assert isinstance(sq, list)
    pts = [g.from_rat(c) for c in sq]
    n = len(pts)
    with open(cpath, encoding="utf-8") as fh:
        check = json.load(fh)
    cl = [clearances(p, S) for p in pts]

    contacts = sorted([k + 1, w] for k in range(n) for w in WALLS if cl[k][w] == 0)
    far = sorted((cl[k][w], k + 1, w) for k in range(n) for w in ("right", "top"))
    far_pos = [x for x in far if x[0] > 0]
    f12 = F(ck.floor_places(S, 12))
    c12 = F(ck.ceil_places(S, 12))
    drop12 = S - f12
    q = side[1]

    def pushed(drop: F) -> dict[str, object]:
        return {
            "outside": [[k, w] for c, k, w in far if c < drop],
            "contact": [[k, w] for c, k, w in far if c == drop],
        }

    # S4: the closest pair, closed along the centre line
    lm = check["pairs"]["least_margin"]
    i0, j0 = lm[0] - 1, lm[1] - 1
    cm = {(i, j): g.closed_margin(pts[i], pts[j]) for i in range(n) for j in range(i + 1, n)}
    cm_least = min((m, i + 1, j + 1) for (i, j), m in cm.items())
    margins_all = {ij: m for ij, m in cm.items() if i0 in ij or j0 in ij}
    s4 = {}
    for fixed, mover in ((i0, j0), (j0, i0)):
        t_star, t_past, L2, nb = g.closing(pts[fixed], pts[mover], E30)
        others = [
            (m, a + 1, b + 1)
            for (a, b), m in margins_all.items()
            if mover in (a, b) and {a, b} != {i0, j0}
        ]
        least_other = min(others)
        clear_min = min(cl[mover].values())
        s4[f"move {mover + 1} toward {fixed + 1}"] = {
            "binding_axes": nb,
            "move_length_sci": sqrt_sci(L2),
            "move_length_squared_below_every_other_margin_squared": all(L2 < m * m for m, _, _ in others),
            "least_other_margin": [least_other[1], least_other[2], ck.sci(least_other[0], 6)],
            "move_length_squared_below_least_clearance_squared": L2 < clear_min * clear_min,
            "least_clearance": ck.sci(clear_min, 6),
            "closed_form_margin_at_contact": str(g.margin_at(pts[fixed], pts[mover], t_star)),
            "closed_form_margin_past": ck.frac_str(g.margin_at(pts[fixed], pts[mover], t_past)),
        }

    # S5: every pair below 1e-12, closed along its centre line
    near = sorted(ij for ij, m in cm.items() if m < F(1, 10**12))
    hist: dict[int, int] = {}
    ok_contact = ok_past = 0
    h = hashlib.sha256()
    for i, j in near:
        t_star, t_past, _, nb = g.closing(pts[i], pts[j], E30)
        hist[nb] = hist.get(nb, 0) + 1
        ok_contact += g.margin_at(pts[i], pts[j], t_star) == 0
        ok_past += g.margin_at(pts[i], pts[j], t_past) == -E30
        h.update(f"{i + 1} {j + 1} {ck.frac_str(t_star)} {ck.frac_str(t_past)}\n".encode())
    mid = [[m_i, m_j, ck.sci(m, 6)] for m, m_i, m_j in sorted(
        (m, i + 1, j + 1) for (i, j), m in cm.items() if F(1, 10**12) <= m < F(1, 10**4)
    )]

    # S6: every square's nearest wall
    nearest = []
    for k in range(n):
        c = min(cl[k][w] for w in WALLS)
        w = next(w for w in WALLS if cl[k][w] == c)
        nearest.append([k + 1, w, ck.sci(c, 6)])
    sq1 = cl[0]
    out = {
        "program": "l117_plan_facts.py",
        "side": ck.frac_str(S),
        "side_denominator_digits": len(str(q)),
        "floor_12": ck.floor_places(S, 12),
        "ceil_12": ck.ceil_places(S, 12),
        "claim": claim,
        "claim_is_ceil_12": ck.ceil_places(S, 12) == claim,
        "claim_less_side": ck.sci(F(claim) - S, 6),
        "contacts": contacts,
        "least_positive_far_clearance": [far_pos[0][1], far_pos[0][2], ck.sci(far_pos[0][0], 6)],
        "far_positive_below_1e-30": sum(1 for c, _, _ in far_pos if c < E30),
        "S1a_lower_by_1_over_q": pushed(F(1, q)),
        "S1b_lower_by_1e-30": pushed(E30),
        "S1c_floor_12_drop": ck.sci(drop12, 6),
        "S1c_floor_12": pushed(drop12),
        "S1d_ceil_12_rise": ck.sci(c12 - S, 6),
        "square_1_clearances": {w: ck.sci(sq1[w], 6) for w in WALLS},
        "square_1_touches_wall": any(v == 0 for v in sq1.values()),
        "square_269_clearances": {w: ck.sci(cl[n - 1][w], 6) for w in WALLS},
        "S4_closest_pair": [lm[0], lm[1], lm[3]],
        "closed_form_least_margin_equals_check": [cm_least[1], cm_least[2], ck.frac_str(cm_least[0])] == lm[0:3],
        "S4": s4,
        "S5_pairs_below_1e-12": len(near),
        "S5_binding_axes_histogram": {str(k): v for k, v in sorted(hist.items())},
        "S5_closed_form_zero_at_contact": ok_contact,
        "S5_closed_form_minus_1e-30_past": ok_past,
        "S5_times_sha256": h.hexdigest(),
        "pairs_from_1e-12_to_1e-4": mid,
        "S6_nearest_wall": nearest,
        "S6_nearest_wall_counts": {w: sum(1 for r in nearest if r[1] == w) for w in WALLS},
    }
    with open(opath, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    for k, v in out.items():
        if k not in ("S6_nearest_wall", "side"):
            print(k, v)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
