"""Facts the controls plan is stated from (lane L72, bead think-qqyg). Decides nothing.

Usage: python -I -B l72_plan_facts.py CERT.yaml CHECK.json OUT.json

From the certificate and its check receipt only: the exact wall clearances of every
square (method A's arithmetic), the side less its 12-place floor, the squares whose
clearance to a wall lies below the steps the controls take, and, for the least-margin
pair, the centre-line closing parameter and move vector with both squares' clearances,
so the plan can say which square to move. No modified file is decided here.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fractions import Fraction  # noqa: E402

import l72_reader as reader  # noqa: E402
import l72_sat as sat  # noqa: E402
import l72_util as util  # noqa: E402

EPS = Fraction(1, 10**30)


def centre(P):
    return ((P[0][0] + P[2][0]) / 2, (P[0][1] + P[2][1]) / 2)


def closing_parameter(Pi, ai, Pj, aj, d):
    """Least s at which Pj + s d touches Pi (Pi, Pj apart at s = 0, concentric at s = 1)."""
    best = None
    for a in (ai[0], ai[1], aj[0], aj[1]):
        lo_i, hi_i = sat.proj_range(Pi, a)
        lo_j, hi_j = sat.proj_range(Pj, a)
        da = d[0] * a[0] + d[1] * a[1]
        for alpha, beta in ((lo_j - hi_i, da), (lo_i - hi_j, -da)):
            if alpha > 0:
                root = alpha / -beta
                if best is None or root > best:
                    best = root
    return best


def main(argv):
    cert, check, out = argv[1], argv[2], argv[3]
    data = reader.read_files(cert)
    rc = json.load(open(check))
    n = data["n"]
    p, q = data["side"]
    S = Fraction(p, q)
    ids = data["ids"]
    P = [sat.corners_frac(c) for c in data["corners"]]
    axes = [sat.square(x)[2] for x in P]
    cl = [sat.wall_clearances(x, S) for x in P]
    floor12 = Fraction(util.floor_decimal(S, 12).replace(".", "")) / 10**12
    ceil12 = Fraction(util.ceil_decimal(S, 12).replace(".", "")) / 10**12
    drop = S - floor12

    def below(w, t):
        return [ids[i] for i in range(n) if cl[i][w] < t]

    facts = {
        "certificate": os.path.basename(cert),
        "n": n,
        "side_minus_floor12": util.sci(drop, 8),
        "ceil12_minus_side": util.sci(ceil12 - S, 8),
        "one_over_q": f"1/{q}",
        "contacts": rc["walls"]["contacts"],
        "right_or_top_below_one_over_q": sorted(set(below(1, Fraction(1, q)) + below(3, Fraction(1, q)))),
        "right_or_top_below_1e-30": sorted(set(below(1, EPS) + below(3, EPS))),
        "right_or_top_below_side_minus_floor12": sorted(set(below(1, drop) + below(3, drop))),
        "left_below_1e-30": below(0, EPS),
        "right_below_1e-30": below(1, EPS),
        "bottom_below_1e-30": below(2, EPS),
        "top_below_1e-30": below(3, EPS),
        "least_clearance_per_wall": {
            w: {"id": ids[min(range(n), key=lambda i: cl[i][k])], "sci": util.sci(min(c[k] for c in cl))}
            for k, w in enumerate(sat.WALLS)
        },
        "least_positive_clearance_per_wall": {
            w: util.sci(min(c[k] for c in cl if c[k] > 0)) for k, w in enumerate(sat.WALLS)
        },
    }
    lp = rc["pairs"]["least_margin"]["pair"]
    i, j = ids.index(lp[0]), ids.index(lp[1])
    rows = {}
    for mover, fixed in ((j, i), (i, j)):
        ci, cj = centre(P[fixed]), centre(P[mover])
        d = (ci[0] - cj[0], ci[1] - cj[1])
        s = closing_parameter(P[fixed], axes[fixed], P[mover], axes[mover], d)
        v = (s * d[0], s * d[1])
        rows[str(ids[mover])] = {
            "moves_toward": ids[fixed],
            "closing_parameter": util.sci(s, 10),
            "move_x": util.sci(v[0], 6),
            "move_y": util.sci(v[1], 6),
            "clearances_left_right_bottom_top": [util.sci(c) for c in cl[mover]],
            "move_crosses_a_wall_at_contact": bool(
                (v[0] < 0 and -v[0] > cl[mover][0])
                or (v[0] > 0 and v[0] > cl[mover][1])
                or (v[1] < 0 and -v[1] > cl[mover][2])
                or (v[1] > 0 and v[1] > cl[mover][3])
            ),
        }
    facts["least_pair"] = {"pair": lp, "margin": rc["pairs"]["least_margin"]["sci"], "movers": rows}
    facts["pairs_below_1e-12"] = rc["pairs"]["nonnegative_margins_below"]["1e-12"]
    util.write_receipt(out, facts)
    print(json.dumps(facts, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
