"""The houses decided, and their uniform-contraction margins (lane L72, bead think-qqyg).

Usage: python -I -B l72_houses.py STATEMENTS.json SIDES.json REPO_ROOT OUT.json

Each house witness on main is read as exact corners (l72_house) and decided by the frozen
checker at its own side (l72_check.decide_data, both methods, every square, wall and pair).

Its uniform-contraction margin is then computed exactly. Every centre is scaled by a common
factor lambda <= 1 about a fixed point, orientations kept, and the box shrinks to the
packing's extent E(lambda). For a pair (i, j) each of the eight gap pieces on the four axes
is linear in lambda, alpha + beta lambda, with alpha < 0 (concentric squares overlap); the
pair stays apart for lambda >= b_ij, the least root -alpha/beta of its increasing pieces.
lambda* is the largest b_ij, where the first pair touches, and the margin is
S_house - E(lambda*): the side the house certificate gives up against its own packing
contracted to first contact, wall clearance included. The contracted packing is then
decided at lambda* (expected: accepted, the binding pair touching) and at lambda* - 1e-30
(expected: refused, that pair overlapping), placed at [0, E]^2.
Each claim's gain is then measured as a share of that margin.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fractions import Fraction  # noqa: E402

import l72_check as chk  # noqa: E402
import l72_house as house  # noqa: E402
import l72_sat as sat  # noqa: E402
import l72_util as util  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
EPS = Fraction(1, 10**30)


def contraction(hw):
    n = hw["n"]
    S = Fraction(*hw["side"])
    P = [sat.corners_frac(c) for c in hw["corners"]]
    C = hw["centres"]
    axes = [sat.square(x)[2] for x in P]
    # corner offsets from the centre, fixed under contraction
    off = [[(p[0] - C[i][0], p[1] - C[i][1]) for p in P[i]] for i in range(n)]
    lam_star = None
    binding = None
    for i in range(n):
        for j in range(i + 1, n):
            b = None
            for a in (axes[i][0], axes[i][1], axes[j][0], axes[j][1]):
                oi = [o[0] * a[0] + o[1] * a[1] for o in off[i]]
                oj = [o[0] * a[0] + o[1] * a[1] for o in off[j]]
                dc = (C[j][0] - C[i][0]) * a[0] + (C[j][1] - C[i][1]) * a[1]
                for alpha, beta in ((min(oj) - max(oi), dc), (min(oi) - max(oj), -dc)):
                    if beta > 0:
                        root = -alpha / beta
                        if b is None or root < b:
                            b = root
            if b is not None and (lam_star is None or b > lam_star):
                lam_star = b
                binding = (hw["ids"][i], hw["ids"][j])

    def extent(lam):
        xs_hi = max(lam * C[i][0] + max(o[0] for o in off[i]) for i in range(n))
        xs_lo = min(lam * C[i][0] + min(o[0] for o in off[i]) for i in range(n))
        ys_hi = max(lam * C[i][1] + max(o[1] for o in off[i]) for i in range(n))
        ys_lo = min(lam * C[i][1] + min(o[1] for o in off[i]) for i in range(n))
        return xs_hi - xs_lo, ys_hi - ys_lo, xs_lo, ys_lo

    ex1, ey1, _, _ = extent(Fraction(1))
    exs, eys, x0, y0 = extent(lam_star)
    E1 = max(ex1, ey1)
    Es = max(exs, eys)

    def placed(lam):
        _, _, xl, yl = extent(lam)
        out = []
        for i in range(n):
            pts = [(lam * C[i][0] + o[0] - xl, lam * C[i][1] + o[1] - yl) for o in off[i]]
            out.append(tuple((x.numerator, x.denominator, y.numerator, y.denominator) for x, y in pts))
        return out

    checks = {}
    for label, lam in (("at_first_contact", lam_star), ("past_first_contact", lam_star - EPS)):
        ex, ey, _, _ = extent(lam)
        E = max(ex, ey)
        d = {"n": n, "side": (E.numerator, E.denominator), "ids": hw["ids"], "corners": placed(lam)}
        r = chk.decide_data(d)
        pairs = r.get("pairs") or {}
        checks[label] = {
            "verdict": r["verdict"],
            "touching": [t["pair"] for t in pairs.get("touching", [])][:10],
            "overlapping": [o["pair"] for o in pairs.get("overlapping", [])][:10],
            "classes_A": pairs.get("classes_A"),
            "classes_B": pairs.get("classes_B"),
        }
    return {
        "lambda_star": util.frac_str(lam_star),
        "one_minus_lambda_star": util.sci(1 - lam_star, 8),
        "binding_pair": list(binding),
        "extent_at_1": util.sci(E1, 20),
        "wall_slack_S_minus_E1": util.sci(S - E1, 8),
        "pair_contraction_E1_minus_Estar": util.sci(E1 - Es, 8),
        "margin_exact": util.frac_str(S - Es),
        "margin": util.sci(S - Es, 8),
        "contracted_side": util.sci(Es, 25),
        "decided": checks,
        "_margin_fraction": S - Es,
    }


def main(argv):
    statements = json.load(open(argv[1]))
    sides = json.load(open(argv[2]))
    repo_root, out = argv[3], argv[4]
    t0 = util.cpu_seconds()
    report = {"program": "l72_houses.py", "lane": "L72", "bead": "think-qqyg", "environment": util.environment()}
    report["program_digests"] = util.program_digests(
        [os.path.join(HERE, f) for f in ("l72_houses.py", "l72_house.py", "l72_check.py", "l72_sat.py", "l72_clip.py", "l72_reader.py", "l72_util.py")]
    )
    for count in ("172", "270"):
        st = statements[count]
        hw = house.read_center_basis(os.path.join(repo_root, st["house_witness"]))
        r = chk.decide_data(hw)
        pairs = r["pairs"]
        row = {
            "entry": st["record_entry"],
            "witness": st["house_witness"],
            "verdict": r["verdict"],
            "problems": r["problems"],
            "side": r["side"],
            "contacts": r["walls"]["contacts"],
            "least_wall_clearance": r["walls"]["least_positive_clearance"],
            "least_pair": pairs["least_margin"],
            "pair_classes_A": pairs["classes_A"],
            "pair_classes_B": pairs["classes_B"],
            "pairs_below_1e-12": pairs["nonnegative_margins_below"]["1e-12"],
        }
        con = contraction(hw)
        margin = con.pop("_margin_fraction")
        gap = Fraction(*map(int, sides[count]["gap"]["exact"].split("/")))
        con["gain"] = util.sci(gap, 12)
        con["gain_over_margin"] = util.sci(gap / margin, 6)
        con["margin_share_of_gain"] = util.sci(margin / gap, 6)
        con["gain_inside_margin"] = gap <= margin
        row["contraction"] = con
        report[count] = row
        print(count, json.dumps(row, indent=1), flush=True)
    report["cpu_seconds"] = round(util.cpu_seconds() - t0, 2)
    util.write_receipt(out, report)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
