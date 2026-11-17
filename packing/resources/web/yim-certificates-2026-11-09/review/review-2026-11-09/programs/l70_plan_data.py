"""Facts the controls plan states its expectations from (L70 review).

For each certificate: 1/q of the side, the exact least clearance at each wall and the
squares within 1e-30 of it, the exact least pair margin and the pairs within 1e-30
of it, how many squares are turned (t not 0 or +-1), and the 12-place floor's
shortfall. Uses the frozen reader and method A only to gather facts; it decides
nothing.

Usage: python -I l70_plan_data.py --src SRC --out plan-data.json
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import l70_check as C  # noqa: E402
import l70_reader as R  # noqa: E402
import l70_sat as A  # noqa: E402

EPS = F(1, 10**30)
BH = (553, 599, 600, 601, 602, 604, 645, 647, 648, 699, 700)


def facts(label: str, pk: R.Packing) -> dict[str, Any]:
    side = F(pk.side[0], pk.side[1])
    sa = A.build(pk)
    cl = [A.wall_clearances(s, side) for s in sa]
    walls: dict[str, Any] = {}
    for k, w in enumerate(C.WALLS):
        vals = [c[k] for c in cl]
        m = min(vals)
        walls[w] = {
            "least": C.frac_str(m),
            "least_float": float(m),
            "at": [pk.ids[i] for i, v in enumerate(vals) if v == m],
            "within_1e-30_of_least": [pk.ids[i] for i, v in enumerate(vals) if v < m + EPS],
            "below_least_plus_1_over_q": [pk.ids[i] for i, v in enumerate(vals) if v < m + F(1, pk.side[1])],
        }
    far = min(F(walls["right"]["least"]), F(walls["top"]["least"]))
    floor12 = F(C.floor_places(side, 12))
    one_q = F(1, pk.side[1])
    outside_c_eps = [pk.ids[i] for i, c in enumerate(cl) if c[2] < far + EPS or c[3] < far + EPS]
    outside_1q = [pk.ids[i] for i, c in enumerate(cl) if c[2] < one_q or c[3] < one_q]
    # least pair margins: method A over all pairs, keep the 5 smallest
    n = pk.n
    small: list[tuple[F, int, int, int]] = []
    for i in range(n):
        for j in range(i + 1, n):
            m, k = A.pair_margin(sa[i], sa[j])
            if len(small) < 5 or m < small[-1][0]:
                small.append((m, i, j, k))
                small.sort(key=lambda e: e[0])
                del small[5:]
    least = small[0][0]
    tilted = 0
    if pk.kind == "cert":
        for row in pk.squares:
            t = F(row[4], row[5])
            if t not in (0, 1, -1):
                tilted += 1
    return {
        "label": label,
        "n": n,
        "side_q_digits": len(str(pk.side[1])),
        "one_over_q_float": float(F(1, pk.side[1])),
        "least_far_clearance": C.frac_str(far),
        "least_far_clearance_float": float(far),
        "one_over_q_below_least_far_clearance": F(1, pk.side[1]) < far,
        "floor12_shortfall_float": float(side - floor12),
        "squares_outside_side_minus_far_minus_1e-30": outside_c_eps,
        "squares_outside_side_minus_1_over_q": outside_1q,
        "squares_outside_at_floor12": [pk.ids[i] for i, c in enumerate(cl) if c[2] < side - floor12 or c[3] < side - floor12],
        "walls": walls,
        "least_pairs": [[pk.ids[i], pk.ids[j], C.frac_str(m), float(m), k] for m, i, j, k in small],
        "pairs_within_1e-30_of_least": [[pk.ids[i], pk.ids[j]] for m, i, j, _k in small if m < least + EPS],
        "turned_squares": tilted,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ns = ap.parse_args()
    src = Path(ns.src)
    head = src / "ac14112"
    files = [("yim-n130", head / "n130.cert"), ("yim-n299", head / "n299.cert"), ("yim-n303", head / "n303.cert"), ("yim-n303-first", src / "78eb9ea" / "n303.cert")]
    files += [(f"yim-n{n}", head / f"n{n}.cert") for n in BH]
    out = {"program": "l70_plan_data.py", "program_digests": C.file_digests(C.CHECKER_FILES + ("l70_plan_data.py",)), "facts": {}}
    for label, path in files:
        f = facts(label, R.read_cert(path))
        out["facts"][label] = f
        w = f["walls"]
        print(label, "1/q", f"{f['one_over_q_float']:.1e}", "far", f"{f['least_far_clearance_float']:.3e}", "1/q<far", f["one_over_q_below_least_far_clearance"], "turned", f["turned_squares"],
              "| L", w["left"]["at"], len(w["left"]["within_1e-30_of_least"]), "B", w["bottom"]["at"], len(w["bottom"]["within_1e-30_of_least"]),
              "R", w["right"]["at"], len(w["right"]["within_1e-30_of_least"]), "T", w["top"]["at"], len(w["top"]["within_1e-30_of_least"]),
              "| least pairs", [(a, b, f"{v:.3e}") for a, b, _e, v, _k in f["least_pairs"][:3]], "within", f["pairs_within_1e-30_of_least"], "| floor12 out", len(f["squares_outside_at_floor12"]), flush=True)
    Path(ns.out).write_text(json.dumps(out, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
