"""Lane L182: state L180's 26 controls for #997's certificate, before any control is run.

Written for the addendum to lane L180's blind stage 4 review of issue #996, on the
replacement certificate of issue #997. It imports nothing from this repository or the
source, and decides nothing.

1. It runs ``l180_make_plan.main``, unchanged, on #997's check receipt and the plan
   facts of ``l182_plan_facts.py`` into SCRATCH. Every square, pair, value and digest a
   control names is re-derived there by L180's own rules from #997's certificate.
2. It re-targets by hand the three texts in which L180's program prints a value of
   #996's certificate as a constant: G7b's "...187", S1e's "= 9.994038857546" and S1f's
   "9.994038857545". Each replacement must find its old text exactly once.
3. It re-targets G5 where L180's program assumes its premise. L180's G5a always expects
   the turn by t = +1e-30 to be accepted and G5b the turn by -1e-30 to be refused, which
   holds when the square touches its wall at a single corner. Here each turn's
   expectation follows the sign of the closed form's clearance for that turn, from the
   plan facts: positive is accepted with the contact gone, negative refused with the
   square across the wall, zero accepted with the contact kept. On #996's facts this
   rule gives L180's G5 expectations exactly; a control whose expectation it changes is
   restated.
4. It checks the preconditions L180's texts assert in words (squares 1 and 90 on no
   wall, every margin (1, j) positive, square 1 clear of the left wall, a G5 square and
   an S4 pair found, no right or top contact, the twin listed as L180's twin controls
   assume), and records them.
5. It compares every control with L180's kept plan for #996 and records which stated
   texts and which expectations differ.

Usage: l182_make_plan.py CHECK_RECEIPT PLAN_FACTS L180_PLAN SCRATCH OUT
"""

from __future__ import annotations

import json
import math
import os
import sys
from fractions import Fraction as F
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
L180 = os.path.normpath(os.path.join(HERE, "..", "..", "programs"))
sys.path.insert(0, L180)

import l180_make_plan as MP  # noqa: E402

WALLS = ("left", "bottom", "right", "top")


def write_plan(path: str, plan: dict[str, Any]) -> None:
    """L180's layout: one line per control."""
    controls = plan["controls"]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("{\n")
        keys = list(plan)
        for k, key in enumerate(keys):
            if key == "controls":
                fh.write(' "controls": {\n')
                cks = list(controls)
                for m, cid in enumerate(cks):
                    fh.write(f"  {json.dumps(cid)}: {json.dumps(controls[cid])}{',' if m < len(cks) - 1 else ''}\n")
                fh.write(" }")
            else:
                fh.write(f" {json.dumps(key)}: {json.dumps(plan[key])}")
            fh.write(",\n" if k < len(keys) - 1 else "\n")
        fh.write("}\n")


def main(argv: list[str]) -> int:
    if len(argv) != 6:
        print(__doc__)
        return 2
    cpath, fpath, l180_plan_path, scratch, out = argv[1:]
    rc = MP.main(["l180_make_plan.py", cpath, fpath, scratch])
    if rc != 0:
        return rc
    with open(scratch, encoding="utf-8") as fh:
        plan: dict[str, Any] = json.load(fh)
    with open(cpath, encoding="utf-8") as fh:
        check = json.load(fh)
    with open(fpath, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(l180_plan_path, encoding="utf-8") as fh:
        old = json.load(fh)
    dec = check["decision"]
    side = F(dec["side"])
    c = plan["controls"]

    raised = side.numerator + 4
    texts = [
        ("G7b", "(...187, still in lowest terms)", f"(...{str(raised)[-3:]}, still in lowest terms)", "L180's text prints #996's raised numerator"),
        ("S1e", "= 9.994038857546,", "= 9.994038766610,", "L180's text prints #996's claim; #997 claims 9.994038766610"),
        ("S1f", "floor 9.994038857545,", "floor 9.994038766609,", "L180's text prints #996's floor; #997's is 9.994038766609"),
    ]
    by_hand: dict[str, Any] = {}
    for cid, was, now, why in texts:
        stated = c[cid]["stated"]
        if stated.count(was) != 1:
            print(f"{cid}: the text to re-target is not found exactly once")
            return 1
        c[cid]["stated"] = stated.replace(was, now)
        by_hand[cid] = {"was": was, "now": now, "why": why}
    by_hand["S1e"]["also"] = "the expectation's side is the facts' S1 claim, re-targeted by l182_plan_facts.py"
    by_hand["S1f"]["also"] = "the expectation's side and crossing list come from the facts' S1 floor, re-targeted by l182_plan_facts.py"

    contacts = dec["wall_contacts"]
    g5 = facts["G5"]
    sq5, wall5 = g5["square"], g5["wall"]
    none: dict[str, list[int]] = {w: [] for w in WALLS}
    minus5 = {w: [i for i in contacts[w] if not (i == sq5 and w == wall5)] for w in WALLS}
    signs = {key: (F(g5[key]["wall_clearance"]) > 0) - (F(g5[key]["wall_clearance"]) < 0) for key in ("plus", "minus")}
    same_sign = signs["plus"] == signs["minus"]
    for cid, key, tt in (("G5a", "plus", "+1e-30"), ("G5b", "minus", "-1e-30")):
        v, ap = g5[key]["wall_clearance"], g5[key]["wall_clearance_approx"]
        clr = {f"{sq5} {wall5}": v}
        base = {"overlapping": [], "touching": []}
        if signs[key] > 0:
            exp = {"verdict": "ACCEPT", **base, "contacts": minus5, "crossings": none, "clearances": clr}
            outcome = f"accepted, its {wall5} clearance exactly the plan's {ap}; that contact gone and no other class changed"
        elif signs[key] < 0:
            exp = {"verdict": "REFUSE", **base, "contacts": minus5, "crossings": {**none, wall5: [sq5]}, "clearances": clr}
            outcome = f"refused, square {sq5} across the {wall5} wall by exactly the plan's {ap}, not inside by method B's area; no pair changes class"
        else:
            exp = {"verdict": "ACCEPT", **base, "contacts": contacts, "crossings": none, "clearances": clr}
            outcome = f"accepted, its {wall5} contact kept; no class changed"
        if exp == c[cid]["expect"]:
            continue
        note = ""
        if same_sign:
            note = (
                f" Both turns give square {sq5} the same {wall5} clearance, so it lies on the wall along an edge and a "
                "turn either way moves a corner the same way; the rotation sense is not decided at this wall, and G6 decides it."
            )
        c[cid]["expect"] = exp
        c[cid]["stated"] = (
            f"Square {sq5}, the lowest-numbered square touching exactly one wall ({wall5}), turned about its centre by "
            f"t = tan(phi/2) = {tt}: {outcome}.{note}"
        )
        by_hand[cid] = {
            "why": "L180's G5 expects the turn by +1e-30 accepted and by -1e-30 refused, true of a single-corner contact; "
            "the expectation now follows the sign of the closed form's clearance for this turn",
            "plus_and_minus_same_sign": same_sign,
            "closed_form_clearance": v,
        }
    on_wall = {i for w in contacts for i in contacts[w]}
    pre = {
        "G1: squares 1 and 90 touch no wall": 1 not in on_wall and 90 not in on_wall,
        "G1: every margin (1, j), j < 90, positive": facts["G1"]["margins_1_j_positive_for_j_not_n"],
        "G2: square 1 clear of the left wall": facts["G2"]["left_clearance_before_positive"],
        "G5: a square touching exactly one wall found": bool(facts["G5"]),
        "G7b: the raised side still in lowest terms": math.gcd(raised, side.denominator) == 1,
        "G7c, G7d: the twin listed counterclockwise from C + (u + v)/2": check["twin"]["listings"] == {"start 0, sense +": 90},
        "S1: no right or top contact": not contacts["right"] and not contacts["top"],
        "S1b: no positive right or top clearance below 1e-30": facts["S1"]["right_top_below_1e-30"] == [],
        "S1e: the claim at least the side": facts["S1"]["claim_at_least_side"],
        "S4: a pair found": bool(facts["S4"]),
    }
    differs: dict[str, Any] = {}
    for cid in c:
        o = old["controls"].get(cid)
        if o is None:
            differs[cid] = "not in L180's plan"
            continue
        keys = sorted(k for k in set(o["expect"]) | set(c[cid]["expect"]) if o["expect"].get(k) != c[cid]["expect"].get(k))
        entry: dict[str, Any] = {}
        if o["stated"] != c[cid]["stated"]:
            entry["stated"] = "differs"
        if keys:
            entry["expect"] = keys
        if entry:
            differs[cid] = entry
    plan["program"] = "l182_make_plan.py (l180_make_plan.py unchanged; three texts re-targeted)"
    plan["lane"] = "L182"
    plan["l182"] = {
        "re_targeted_by_hand": by_hand,
        "preconditions": pre,
        "all_preconditions_hold": all(pre.values()),
        "differs_from_l180_plan": differs,
        "same_as_l180_plan": sorted(cid for cid in c if cid not in differs),
        "l180_g5": old["g5"],
        "l180_s4": old["s4"],
    }
    write_plan(out, plan)
    with open(out, encoding="utf-8") as fh:
        if json.load(fh) != json.loads(json.dumps(plan)):
            print("plan does not read back")
            return 1
    print(
        f"{len(c)} controls stated; re-targeted by hand {sorted(by_hand)}; preconditions hold {all(pre.values())}; "
        f"G5 {plan['g5']} (L180 {old['g5']}); S4 {plan['s4']} (L180 {old['s4']}); "
        f"same as L180's plan {plan['l182']['same_as_l180_plan']}"
    )
    return 0 if all(pre.values()) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
