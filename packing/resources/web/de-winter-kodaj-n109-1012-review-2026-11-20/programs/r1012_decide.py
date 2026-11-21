"""Lane r1012: a packing decided by both methods, every square, wall and pair.

The verdict is ACCEPT only when both methods accept every square as a unit
square, place every square inside the box (no wall crossed; method B's area
inside exactly 1), find no overlapping pair, and agree on every class:
the unit-square verdict, each of the four wall classes of every square, and the
class of every pair (method B's two clipping orders agreeing as well).
"""

from fractions import Fraction

import r1012_clip
import r1012_sat


def decide(side, quads):
    a = r1012_sat.decide(side, quads)
    b = r1012_clip.decide(side, quads)
    n = len(quads)
    disagreements = []
    problems = []
    for k in range(n):
        if a["unit"][k] != b["unit"][k]:
            disagreements.append(("unit", k, a["unit"][k], b["unit"][k]))
        if not a["unit"][k] or not b["unit"][k]:
            problems.append(("not a unit square", k))
            continue
        if a["sense"][k] != b["sense"][k]:
            disagreements.append(("sense", k, a["sense"][k], b["sense"][k]))
        if a["wall_class"][k] != b["wall_class"][k]:
            disagreements.append(("walls", k, a["wall_class"][k], b["wall_class"][k]))
        for w, cls in enumerate(a["wall_class"][k]):
            if cls == "cross":
                problems.append(("crosses wall", k, "LBRT"[w]))
        inside_ok = b["inside_area"][k] == 1
        a_inside = all(c != "cross" for c in a["wall_class"][k])
        if inside_ok != a_inside:
            disagreements.append(("inside", k, a_inside, inside_ok))
        if not inside_ok:
            problems.append(("area inside the box below 1", k))
    for key, cls in a["pair_class"].items():
        if cls is None:
            continue
        if cls != b["pair_class"][key]:
            disagreements.append(("pair", key, cls, b["pair_class"][key]))
        if cls == "overlap" or b["pair_class"][key] == "overlap":
            problems.append(("overlap", key))
    for key in b["order_disagree"]:
        disagreements.append(("clip orders", key))
    verdict = "ACCEPT" if not problems and not disagreements else "REFUSE"
    return {
        "verdict": verdict,
        "problems": problems,
        "disagreements": disagreements,
        "a": a,
        "b": b,
    }


def frac(pair_or_fraction):
    if isinstance(pair_or_fraction, tuple):
        return Fraction(pair_or_fraction[0], pair_or_fraction[1])
    return Fraction(pair_or_fraction)
