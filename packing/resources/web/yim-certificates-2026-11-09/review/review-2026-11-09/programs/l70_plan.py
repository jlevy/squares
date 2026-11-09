"""Write the L70 controls plan: every control and its expected outcome, per file.

Stated from plan-data.json and the check receipts before any controls program
exists. The plan is then hashed and frozen.

Usage: python -I l70_plan.py --data plan-data.json --checks OUTDIR --out controls-plan.json
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path
from typing import Any

DEFS = {
    "contact": "method A margin exactly 0; method B intersection nonempty with area exactly 0",
    "past": "1e-30 beyond contact (a length for translations and sides; a factor 1 - 1e-30 on the centre distance for pair closings)",
    "closing a pair": "square j's centre moved along the centre line to c_i + lambda (c_j - c_i), lambda = T / max_w |w.(c_j - c_i)| over the four edge normals, T = (1 + |u_i.u_j| + |u_i.v_j|)/2: the factor at which the largest projection gap is exactly 0",
    "whole-file": "every square, wall and pair decided by both methods (l70_check.decide)",
    "wall-level": "every square's shape, containment and wall contacts decided by both methods; the pairs are unchanged by construction (a side change or a common translation changes no pair margin and no intersection), and were decided in the check",
    "pair-level": "the two squares alone, decided by both methods",
    "square-level": "the square alone, decided by both methods",
    "reader": "the frozen reader on the mutated bytes",
}


def far_contacts(f: dict[str, Any]) -> list[str]:
    w = f["walls"]
    c = F(f["least_far_clearance"])
    out = []
    for wall in ("right", "top"):
        if F(w[wall]["least"]) == c:
            out += [f"{wall}:{s}" for s in w[wall]["at"]]
    return out


def s7_outside(path: Path, sid: str) -> list[str]:
    """Exact: is square sid outside once enlarged by 1 + 1e-30 about its centre?

    Each wall clearance falls by 1e-30 * h, h = (|cos| + |sin|)/2 the square's half-extent.
    """
    import sys

    here = Path(__file__).resolve().parent
    if str(here) not in sys.path:
        sys.path.insert(0, str(here))
    import l70_reader as R
    import l70_sat as A

    pk = R.read_cert(path)
    k = pk.ids.index(sid)
    side = F(pk.side[0], pk.side[1])
    sq = A.build(R.Packing(n=1, side=pk.side, kind="cert", squares=(pk.squares[k],), ids=(sid,)))[0]
    t = F(pk.squares[k][4], pk.squares[k][5])
    c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
    h = (abs(c) + abs(s)) / 2
    return [sid] if min(A.wall_clearances(sq, side)) < F(1, 10**30) * h else []


def plan_for(label: str, f: dict[str, Any], receipt: dict[str, Any], path: Path) -> list[dict[str, Any]]:
    n = f["n"]
    w = f["walls"]
    i, j = f["least_pairs"][0][0], f["least_pairs"][0][1]
    past_out = f["squares_outside_side_minus_far_minus_1e-30"]
    one_q_ok = f["one_over_q_below_least_far_clearance"]
    controls = [
        {"id": "G1", "level": "whole-file", "what": "the last square replaced by a copy of the first",
         "expect": {"verdict": "REFUSE", "overlapping_pairs": [["1", str(n)]], "outside": [], "A_least_margin": "-1", "B_largest_overlap_area": "1"}},
        {"id": "G2", "level": "whole-file", "what": "square 1 translated by (S, 0)",
         "expect": {"verdict": "REFUSE", "outside": ["1"], "overlapping_pairs": []}},
        {"id": "G3", "level": "reader", "what": "the last row deleted, header unchanged",
         "expect": {"reader": "refuse", "reason_contains": f"file has {n - 1} rows"}},
        {"id": "G4", "level": "reader", "what": "the header count raised by one",
         "expect": {"reader": "refuse", "reason_contains": f"header says {n + 1} squares"}},
        {"id": "G5", "level": "reader", "what": "row 1's t token replaced by 1.5",
         "expect": {"reader": "refuse", "reason_contains": "not a rational token"}},
        {"id": "G6", "level": "whole-file", "what": "the rotation read the other way: every t negated (each square reflected in its horizontal centre line)",
         "expect": {"verdict": "REFUSE", "overlapping_pairs": "at least one, equal sets by both methods"} if f["turned_squares"] else {"verdict": "ACCEPT"}},
        {"id": "S1a", "level": "wall-level", "what": "the side lowered by 1/q, one unit of its own last place",
         "expect": {"verdict": "ACCEPT", "outside": []} if one_q_ok else {"verdict": "REFUSE", "outside": f["squares_outside_side_minus_1_over_q"]},
         "note": f"1/q = {f['one_over_q_float']:.1e}; least far-wall clearance {f['least_far_clearance_float']:.3e}"},
        {"id": "S1b", "level": "wall-level", "what": "the side lowered by its least far-wall clearance c",
         "expect": {"verdict": "ACCEPT", "far_wall_contacts": far_contacts(f)}},
        {"id": "S1c", "level": "wall-level", "what": "the side lowered by c + 1e-30",
         "expect": {"verdict": "REFUSE", "outside": past_out}},
        {"id": "S1d", "level": "wall-level", "what": "the side set to its 12-place ceiling (the print)",
         "expect": {"verdict": "ACCEPT", "outside": []}},
        {"id": "S1e", "level": "wall-level", "what": "the side set to its 12-place floor",
         "expect": {"verdict": "REFUSE", "outside": f["squares_outside_at_floor12"]}},
        {"id": "S3a", "level": "wall-level", "what": "every square moved left by the least left clearance",
         "expect": {"verdict": "ACCEPT", "left_contacts": w["left"]["at"]}},
        {"id": "S3b", "level": "wall-level", "what": "every square moved left by the least left clearance + 1e-30",
         "expect": {"verdict": "REFUSE", "outside": w["left"]["within_1e-30_of_least"]}},
        {"id": "S3c", "level": "wall-level", "what": "every square moved down by the least bottom clearance",
         "expect": {"verdict": "ACCEPT", "bottom_contacts": w["bottom"]["at"]}},
        {"id": "S3d", "level": "wall-level", "what": "every square moved down by the least bottom clearance + 1e-30",
         "expect": {"verdict": "REFUSE", "outside": w["bottom"]["within_1e-30_of_least"]}},
        {"id": "S4c", "level": "whole-file", "what": f"the least-margin pair ({i}, {j}) closed along its centre line to contact (square {j} moved)",
         "expect": {"verdict": "ACCEPT", "touching_pairs": [[i, j]], "overlapping_pairs": []}},
        {"id": "S4p", "level": "whole-file", "what": f"the pair ({i}, {j}) closed 1e-30 past contact",
         "expect": {"verdict": "REFUSE", "overlapping_pairs": [[i, j]]}},
        {"id": "S5", "level": "pair-level", "what": "every pair with margin below 1e-12 closed along its centre line, at contact and 1e-30 past",
         "expect": {"pairs": receipt["A"]["pairs_below"]["1e-12"], "at_contact": "touch by both methods, every pair", "past": "overlap by both methods, every pair"}},
        {"id": "S6", "level": "square-level", "what": "every square moved to its nearest wall by its exact clearance, and 1e-30 past",
         "expect": {"squares": n, "at_contact": "inside with that wall contact by both methods, every square", "past": "outside by both methods, every square"}},
        {"id": "S7", "level": "whole-file", "what": f"square {i} (as four corners) enlarged by 1 + 1e-30 about its centre; the packing decided as corners",
         "expect": {"verdict": "REFUSE", "not_unit": [i], "outside": s7_outside(path, i), "overlapping_pairs": []}},
    ]
    return controls


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--checks", required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ns = ap.parse_args()
    data = json.loads(Path(ns.data).read_text())
    src = Path(ns.src)
    plan: dict[str, Any] = {
        "plan": "L70 controls, stated before any controls program exists",
        "definitions": DEFS,
        "files": {},
    }
    for label, f in data["facts"].items():
        receipt = json.loads((Path(ns.checks) / f"check-{label}.json").read_text())
        path = src / "78eb9ea" / "n303.cert" if label == "yim-n303-first" else src / "ac14112" / f"n{f['n']}.cert"
        plan["files"][label] = {
            "input": str(path.relative_to(src)),
            "input_sha256": receipt["input"]["sha256"],
            "controls": plan_for(label, f, receipt, path),
        }
    Path(ns.out).write_text(json.dumps(plan, indent=1) + "\n")
    print("controls per file:", {k: len(v["controls"]) for k, v in plan["files"].items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
