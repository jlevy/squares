"""Write controls-plan.json from the plan facts, before any control is run (review L83).

Usage: python -I -B l83_make_plan.py OUT_DIR PLAN.json
"""

import json
import sys
from pathlib import Path

GENERAL = {
    "contact": "a margin or clearance of exactly 0; touching by method B is a nonempty clipped set of area 0",
    "past": "10^-30 beyond contact: for a pair, the centre-line parameter 10^-30 beyond its contact value (a move of 10^-30 times the centres' distance); for a wall or a side, 10^-30 in length",
    "centre-line method": "square b of a pair moves by t * (c_a - c_b); t at contact is exact (l83_geom.closing_parameter)",
    "scope of incremental controls": "G1, G2, G5, S4c and S4p change one square: they are decided by both methods on every pair of the changed square and on its walls; every other square and pair is byte-identical to the accepted base check. S1a to S1d change only the side: every square's walls are decided again by both methods, and the pairs, which do not depend on the side, are the base check's.",
    "whole-file controls": "G6 and G8 are decided by both methods over every square, wall and pair",
}


def main(argv):
    out_dir, plan_path = Path(argv[1]), Path(argv[2])
    plan = {"general": GENERAL, "counts": {}}
    for n in (156, 180, 268, 269):
        f = json.loads((out_dir / f"plan-facts-n{n}.json").read_text())
        lp = f["least_pair"]
        far = sorted({i for i, _ in f["far_wall_contacts"]})
        near_contacts = [c for c in f["all_contacts"] if c[1] in ("left", "bottom")]
        swap = {"left": "bottom", "bottom": "left", "right": "top", "top": "right"}
        plan["counts"][str(n)] = {
            "G1": f"square {n} given square 1's corners: refused, exactly the pair (1, {n}) overlapping, margin -1, area 1; no other pair of square {n} overlapping or touching",
            "G2": "square 1 translated by (S, 0): refused, square 1 outside the right wall; no pair of square 1 overlapping or touching",
            "G3": f"the YAML entry of square {n} deleted: the reader refuses ({n - 1} squares for n = {n})",
            "G4": f"square {n}'s id set to 1: the reader refuses (repeated id)",
            "G5": "square 1's third corner moved 10^-30 in x: refused, square 1 not a unit square by either method",
            "G6": "every square reflected in its own horizontal centre line (rotation read the other way): refused for at least one overlapping pair; every square still a unit square by both methods, inside, with the base contacts",
            "G8": {"statement": "every corner transposed (x, y) -> (y, x): accepted, every pair margin exactly the base margin, contacts transposed", "contacts": sorted([c[0], swap[c[1]]] for c in f["all_contacts"])},
            "S1a": {"statement": "side lowered by 1/q, q its denominator: refused, exactly the far-wall contact squares outside", "outside": far},
            "S1b": {"statement": "side lowered by 10^-30: refused, exactly the far-wall contact squares outside (no positive clearance is below 10^-30)", "outside": far},
            "S1c": {"statement": "side set to its 12-place floor: refused, exactly the squares whose right or top clearance is below the drop", "outside": f["s1c_squares_below_drop"]},
            "S1d": {"statement": "side set to its 12-place ceiling, the claim: accepted, contacts only at the left and bottom walls", "contacts": near_contacts},
            "S4c": {"statement": f"square {lp[1]} moved along the centre line of the least pair {tuple(lp)} to contact: that pair touching by both methods, every other pair of square {lp[1]} clear, square {lp[1]} inside with its walls' classes unchanged", "pair": lp},
            "S4p": {"statement": f"the same, 10^-30 past: that pair overlapping by both methods, every other pair of square {lp[1]} clear, square {lp[1]} inside", "pair": lp},
            "S5": {"statement": "every pair below 10^-12 closed along its centre line (pair-level): touching by both methods at contact, overlapping by both past", "pairs": f["pairs_below_1e-12"]},
            "S6": {"statement": "every square moved to its nearest wall by its clearance (square-level): contact with that wall by both methods, the square still inside; past, outside that wall by both", "squares": n},
        }
    plan_path.write_text(json.dumps(plan, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
