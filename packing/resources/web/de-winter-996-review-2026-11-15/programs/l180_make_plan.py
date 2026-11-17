"""Lane L180: state the controls and the outcome of each, before any control is run.

Written for the blind stage 4 review of issue #996 as a clean-room implementation.
It imports nothing from this repository or the source, and reuses no code of any
earlier review. It decides nothing: it writes ``controls-plan.json`` from the check
receipt and the plan facts.

Usage: l180_make_plan.py CHECK_RECEIPT PLAN_FACTS OUT

Every whole-file control is decided by both methods over every square, wall and pair,
after the modified certificate is written as text and read back through the reader.
"Contact" is a margin or clearance of exactly 0; "past" is 1e-30 beyond it.
"""

from __future__ import annotations

import json
import sys
from typing import Any

WALLS = ("left", "bottom", "right", "top")


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__)
        return 2
    with open(argv[1], encoding="utf-8") as fh:
        check = json.load(fh)
    with open(argv[2], encoding="utf-8") as fh:
        facts = json.load(fh)
    dec = check["decision"]
    base_contacts: dict[str, list[int]] = dec["wall_contacts"]
    none: dict[str, list[int]] = {w: [] for w in WALLS}
    md, cd = dec["margin_list_sha256"], dec["clearance_list_sha256"]
    s1 = facts["S1"]
    rt_least = {w: sorted(i for i, ww in s1["right_top_at_least"] if ww == w) for w in WALLS}
    rt_below_q = {w: sorted(i for i, ww in s1["right_top_below_one_unit"] if ww == w) for w in WALLS}
    rt_below_floor = {w: sorted(i for i, ww in s1["right_top_below_side_minus_floor12"] if ww == w) for w in WALLS}
    lb_only = {w: (base_contacts[w] if w in ("left", "bottom") else []) for w in WALLS}
    g5 = facts["G5"]
    sq5, wall5 = g5["square"], g5["wall"]
    minus5 = {w: [i for i in base_contacts[w] if not (i == sq5 and w == wall5)] for w in WALLS}
    s4 = facts["S4"]

    def whole(stated: str, verdict: str, **exp: Any) -> dict[str, Any]:
        return {"kind": "whole-file", "stated": stated, "expect": {"verdict": verdict, **exp}}

    controls: dict[str, dict[str, Any]] = {
        "G1": whole(
            "Square 90 given square 1's centre and direction: refused, exactly the pair (1, 90) overlapping, "
            "margin -1, method B area 1; no other pair touches or overlaps (every margin (1, j) is positive); "
            "wall contacts unchanged (neither square 1 nor square 90 touches a wall).",
            "REFUSE",
            overlapping=[[1, 90]],
            touching=[],
            contacts=base_contacts,
            crossings=none,
            pair_values={"1 90": {"margin": "-1", "area_b": "1"}},
        ),
        "G2": whole(
            "Square 1 translated by (S, 0): refused, square 1 across the right wall by both methods (right "
            f"clearance {facts['G2']['right_clearance_approx']}, the plan's exact value), its area inside the "
            "box 0; no pair touching or overlapping (its least margin is "
            f"{facts['G2']['least_margin_with_others']}).",
            "REFUSE",
            overlapping=[],
            touching=[],
            contacts=base_contacts,
            crossings={**none, "right": [1]},
            clearances={"1 right": facts["G2"]["clearances"]["right"]},
            inside_area={"1": "0"},
        ),
        "G3": {"kind": "reader", "stated": "Square 90's entry deleted: the reader refuses (n is 90, 89 entries).", "expect": {"verdict": "READER_REFUSES", "reason_contains": "squares has 89 entries"}},
        "G4": {"kind": "reader", "stated": "The side written as 2p/2q: the reader refuses (not in lowest terms).", "expect": {"verdict": "READER_REFUSES", "reason_contains": "lowest terms"}},
        "G5a": whole(
            f"Square {sq5}, the lowest-numbered square touching exactly one wall ({wall5}), turned about its centre "
            "by t = tan(phi/2) = +1e-30: accepted, its "
            f"{wall5} clearance exactly the plan's {g5['plus']['wall_clearance_approx']}; that contact gone and "
            "no other class changed.",
            "ACCEPT",
            overlapping=[],
            touching=[],
            contacts=minus5,
            crossings=none,
            clearances={f"{sq5} {wall5}": g5["plus"]["wall_clearance"]},
        ),
        "G5b": whole(
            f"The same with t = -1e-30: refused, square {sq5} across the {wall5} wall by exactly the plan's "
            f"{g5['minus']['wall_clearance_approx']}, not inside by method B's area; no pair changes class.",
            "REFUSE",
            overlapping=[],
            touching=[],
            contacts=minus5,
            crossings={**none, wall5: [sq5]},
            clearances={f"{sq5} {wall5}": g5["minus"]["wall_clearance"]},
        ),
        "G6": whole(
            "Every (c, s) read as (c, -s), each square reflected in its own horizontal centre line (the rotation "
            f"read the other way): refused for exactly the plan's {facts['G6']['overlapping_count']} overlapping "
            "pairs, none touching; the exact clearance list unchanged.",
            "REFUSE",
            overlapping=facts["G6"]["overlapping"],
            touching=facts["G6"]["touching"],
            contacts=base_contacts,
            crossings=none,
            clearance_sha256=cd,
        ),
        "G7a": {
            "kind": "twin",
            "stated": "The twin's first corner of square 1 moved by 1e-30 in x: the twin differs from the JSON at "
            "square 1 alone, and method B refuses square 1 of the twin as not a unit square.",
            "expect": {"twin_agree": False, "twin_problems": ["square 1: corners differ"], "verdict": "REFUSE", "not_unit_b": [1], "not_unit_a": []},
        },
        "G7b": {
            "kind": "twin",
            "stated": "The twin's side numerator raised by 4 in its last digit (...187, still in lowest terms): "
            "the reader reads it and the twin differs from the JSON in its side.",
            "expect": {"twin_agree": False, "twin_problems": ["side differs", "side text differs"]},
        },
        "G7c": {
            "kind": "twin",
            "stated": "Every square of the twin listed clockwise: the twin agrees (each listing the JSON's corners "
            "from its fourth, reversed) and the certificate is accepted with the margin and clearance lists unchanged; "
            "method B reads all 90 listings as clockwise.",
            "expect": {"twin_agree": True, "listings": {"start 3, sense -": 90}, "verdict": "ACCEPT", "margin_sha256": md, "clearance_sha256": cd, "sense_b": {"counterclockwise": 0, "clockwise": 90}},
        },
        "G7d": {
            "kind": "twin",
            "stated": "Every square of the twin listed from its second corner: the twin agrees and the certificate "
            "is accepted with the lists unchanged.",
            "expect": {"twin_agree": True, "listings": {"start 1, sense +": 90}, "verdict": "ACCEPT", "margin_sha256": md, "clearance_sha256": cd},
        },
        "G8": whole(
            "Every square transposed, (x, y, c, s) -> (y, x, s, c): accepted, the margin list unchanged, the "
            "clearances transposed (left and bottom exchanged, right and top exchanged).",
            "ACCEPT",
            overlapping=[],
            touching=[],
            contacts={"left": base_contacts["bottom"], "bottom": base_contacts["left"], "right": base_contacts["top"], "top": base_contacts["right"]},
            crossings=none,
            margin_sha256=md,
        ),
        "G9": whole(
            "Every edge direction replaced by the other, (c, s) -> (-s, c): accepted, margin and clearance lists unchanged.",
            "ACCEPT",
            overlapping=[],
            touching=[],
            contacts=base_contacts,
            crossings=none,
            margin_sha256=md,
            clearance_sha256=cd,
        ),
        "G10": whole(
            "Every edge direction negated, (c, s) -> (-c, -s): accepted, margin and clearance lists unchanged.",
            "ACCEPT",
            overlapping=[],
            touching=[],
            contacts=base_contacts,
            crossings=none,
            margin_sha256=md,
            clearance_sha256=cd,
        ),
        "G11": whole(
            "The packing turned a quarter about the box centre, (x, y, c, s) -> (S - y, x, -s, c): accepted, the "
            "margin list unchanged, the clearances turned (new left, bottom, right, top = old top, left, bottom, right).",
            "ACCEPT",
            overlapping=[],
            touching=[],
            contacts={"left": base_contacts["top"], "bottom": base_contacts["left"], "right": base_contacts["bottom"], "top": base_contacts["right"]},
            crossings=none,
            margin_sha256=md,
        ),
        "G12": whole(
            "Square 1's sin raised by 1e-30: refused, square 1 not a unit square by either method.",
            "REFUSE",
            not_unit_a=[1],
            not_unit_b=[1],
        ),
        "S1a": whole(
            f"The side lowered by 1/q = {s1['one_unit_of_last_place']}, one unit of its own last place: refused, "
            f"exactly the {len(s1['right_top_below_one_unit'])} right and top clearances of "
            f"{s1['least_positive_right_top']['approx']} crossing; the left and bottom contacts unchanged.",
            "REFUSE",
            overlapping=[],
            touching=[],
            contacts=lb_only,
            crossings=rt_below_q,
        ),
        "S1b": whole(
            "The side lowered by 1e-30: accepted, no new contact (no positive right or top clearance is below 1e-30).",
            "ACCEPT",
            overlapping=[],
            touching=[],
            contacts=base_contacts,
            crossings=none,
        ),
        "S1c": whole(
            "The side lowered by the least right-or-top clearance, to the packing's extent: accepted, exactly those "
            f"{len(s1['right_top_at_least'])} square-wall pairs touching, with the left and bottom contacts.",
            "ACCEPT",
            overlapping=[],
            touching=[],
            contacts={w: (base_contacts[w] if w in ("left", "bottom") else rt_least[w]) for w in WALLS},
            crossings=none,
        ),
        "S1d": whole(
            "That, less 1e-30 more: refused, exactly those square-wall pairs crossing.",
            "REFUSE",
            overlapping=[],
            touching=[],
            contacts=lb_only,
            crossings=rt_least,
        ),
        "S1e": whole(
            f"The side set to the claim {s1['claim']} = 9.994038857546, {s1['claim_minus_side']} above the side: "
            "accepted, wall contacts only at the left and bottom.",
            "ACCEPT",
            overlapping=[],
            touching=[],
            contacts=lb_only,
            crossings=none,
        ),
        "S1f": whole(
            f"The side set to its 12-place floor 9.994038857545, {s1['side_minus_floor12']} below the side: refused, "
            "exactly the right and top square-wall pairs of S1a crossing.",
            "REFUSE",
            overlapping=[],
            touching=[],
            contacts=lb_only,
            crossings=rt_below_floor,
        ),
        "S4c": whole(
            f"Square {s4['moving']} moved toward square {s4['toward']} along their centre line to exact contact: "
            "that pair alone touching by both methods, margin exactly 0, method B area 0; accepted.",
            "ACCEPT",
            overlapping=[],
            touching=[s4["pair"]],
            contacts=base_contacts,
            crossings=none,
            pair_values={f"{s4['pair'][0]} {s4['pair'][1]}": {"margin": "0", "area_b": "0"}},
        ),
        "S4p": whole(
            "The same, 1e-30 past contact: that pair alone overlapping by both methods, margin exactly -1e-30.",
            "REFUSE",
            overlapping=[s4["pair"]],
            touching=[],
            contacts=base_contacts,
            crossings=none,
            pair_values={f"{s4['pair'][0]} {s4['pair'][1]}": {"margin": "-1/1000000000000000000000000000000"}},
        ),
        "S5": {
            "kind": "pair-level",
            "stated": "Every pair (4,005) closed along its centre line, the higher-numbered square moving: touching at "
            "contact by both methods with margin exactly 0 by method A and the closed form, overlapping 1e-30 past "
            "with margin exactly -1e-30; the closing times' digest the plan's.",
            "expect": {"pairs": 4005, "closing_times_sha256": facts["S5"]["closing_times_sha256"]},
        },
        "S6": {
            "kind": "square-level",
            "stated": "Every square moved to its nearest wall by its clearance: contact at, crossing 1e-30 past, by "
            "both methods; clearance exactly 0 and -1e-30; inside by method B's area at contact, not past.",
            "expect": {"squares": 90, "nearest_wall_counts": facts["S6"]["nearest_wall_counts"]},
        },
    }
    plan = {
        "program": "l180_make_plan.py",
        "lane": "L180",
        "certificate": check["inputs"],
        "base": {"margin_sha256": md, "clearance_sha256": cd, "contacts": base_contacts},
        "g5": {"square": sq5, "wall": wall5},
        "s4": {"pair": s4["pair"], "moving": s4["moving"], "toward": s4["toward"]},
        "past": "1/1000000000000000000000000000000",
        "controls": controls,
    }
    with open(argv[3], "w", encoding="utf-8") as fh:
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
    with open(argv[3], encoding="utf-8") as fh:
        if json.load(fh) != json.loads(json.dumps(plan)):
            print("plan does not read back")
            return 1
    print(f"{len(controls)} controls stated")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
