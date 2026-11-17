"""Lane L169 controls plan: states each control and its outcome before any is run.

Usage: l169_make_plan.py CHECK_JSON PLAN_FACTS_JSON OUT_PLAN_JSON

It decides nothing. Every outcome is stated from the check receipt (the unmodified
certificate's lists) and from the plan facts (the closed form of l169_geom.py).
"""

from __future__ import annotations

import json
import sys
import time

EPS = "1/1000000000000000000000000000000"


def main(argv: list[str]) -> int:
    check = json.load(open(argv[1]))
    pf = json.load(open(argv[2]))
    dec = check["decision"]
    n = pf["n"]
    ml0, cl0 = dec["margin_list_sha256"], dec["clearance_list_sha256"]
    none = {"overlapping_pairs": [], "touching_pairs": [], "wall_contacts": [], "wall_crossings": []}
    g5 = pf["G5"]
    s1 = pf["S1"]
    s4 = pf["S4"]["chosen"]
    controls = [
        {"id": "G1", "kind": "file", "what": f"square {n} given square 1's centre and t",
         "op": {"name": "copy_square", "from": 1, "to": n},
         "expect": {"verdict": "REFUSE", "overlapping_pairs": [[1, n]], "touching_pairs": [], "wall_contacts": [],
                    "wall_crossings": [], "not_inside_by_B_area": [],
                    "pair": {"pair": [1, n], "A_margin": "-1/1", "B_class": "overlap", "B_area": "1/1"}}},
        {"id": "G2", "kind": "file", "what": "square 1 translated by (S, 0)",
         "op": {"name": "translate_square", "square": 1, "dx": pf["side"], "dy": "0/1"},
         "expect": {"verdict": "REFUSE", **none, "wall_crossings": [[1, "right"]], "not_inside_by_B_area": [1],
                    "clearance": {"square": 1, "wall": "right", "value": pf["G2"]["clearances_square_1_moved"]["right"]}}},
        {"id": "G3", "kind": "reader", "what": f"square {n}'s row deleted",
         "op": {"name": "delete_last_row"},
         "expect": {"reader_refuses": f"header says {n} squares, the file has {n - 1} rows"}},
        {"id": "G4", "kind": "reader", "what": "the side written as 2p/2q",
         "op": {"name": "side_doubled_text"},
         "expect": {"reader_refuses": "not in lowest terms"}},
        {"id": "G5a", "kind": "file",
         "what": f"square {g5['square']}, the turned square nearest a wall, moved to the {g5['wall']} wall by its clearance, then t + 1e-30",
         "op": {"name": "wall_then_turn", "square": g5["square"], "wall": g5["wall"], "by": g5["clearance"], "dt": EPS},
         "expect": {"verdict": "ACCEPT", **none,
                    "clearance": {"square": g5["square"], "wall": g5["wall"], "value": g5["G5a"]["clearance_at_wall"]}}},
        {"id": "G5b", "kind": "file", "what": "the same, then t - 1e-30",
         "op": {"name": "wall_then_turn", "square": g5["square"], "wall": g5["wall"], "by": g5["clearance"], "dt": "-" + EPS},
         "expect": {"verdict": "REFUSE", **none, "wall_crossings": [[g5["square"], g5["wall"]]],
                    "not_inside_by_B_area": [g5["square"]],
                    "clearance": {"square": g5["square"], "wall": g5["wall"], "value": g5["G5b"]["clearance_at_wall"]}}},
        {"id": "G6", "kind": "file", "what": "every t negated (the rotation read the other way)",
         "op": {"name": "negate_t"},
         "expect": {"verdict": "REFUSE", "overlapping_pairs": pf["G6"]["overlapping"], "touching_pairs": [],
                    "wall_contacts": [], "wall_crossings": [], "clearance_list_sha256": cl0}},
        {"id": "G7a", "kind": "file", "what": "the text with LF line ends",
         "op": {"name": "lf_text"},
         "expect": {"verdict": "ACCEPT", **none, "margin_list_sha256": ml0, "clearance_list_sha256": cl0}},
        {"id": "G7b", "kind": "reader", "what": f"the header's count written as {n + 1}",
         "op": {"name": "header_count", "value": n + 1},
         "expect": {"reader_refuses": f"header says {n + 1} squares, the file has {n} rows"}},
        {"id": "G8", "kind": "file", "what": "every square transposed, (x, y, t) -> (y, x, -t)",
         "op": {"name": "transpose"},
         "expect": {"verdict": "ACCEPT", **none, "margin_list_sha256": ml0,
                    "clearance_list_sha256": pf["G8_clearance_list_sha256"]}},
        {"id": "G9", "kind": "file", "what": "every t -> (t + 1)/(1 - t), the angle plus 90 degrees",
         "op": {"name": "rebase_plus"},
         "expect": {"verdict": "ACCEPT", **none, "margin_list_sha256": ml0, "clearance_list_sha256": cl0}},
        {"id": "G10", "kind": "file", "what": "every t -> (t - 1)/(1 + t), the angle less 90 degrees",
         "op": {"name": "rebase_minus"},
         "expect": {"verdict": "ACCEPT", **none, "margin_list_sha256": ml0, "clearance_list_sha256": cl0}},
        {"id": "G11", "kind": "file", "what": "the packing turned a quarter about the box centre, (x, y, t) -> (S - y, x, t)",
         "op": {"name": "quarter_turn"},
         "expect": {"verdict": "ACCEPT", **none, "margin_list_sha256": ml0,
                    "clearance_list_sha256": pf["G11_clearance_list_sha256"]}},
        {"id": "S1a", "kind": "file", "what": "the side lowered by 1/q, one unit of its own last place",
         "op": {"name": "side_minus", "by": s1["one_unit_of_last_place"]},
         "expect": {"verdict": "REFUSE", **none, "wall_crossings": s1["S1a_crossings"],
                    "margin_list_sha256": ml0}},
        {"id": "S1b", "kind": "file", "what": "the side lowered by 1e-30",
         "op": {"name": "side_minus", "by": EPS},
         "expect": {"verdict": "ACCEPT", **none, "margin_list_sha256": ml0}},
        {"id": "S1c", "kind": "file", "what": "the side lowered by the least right-or-top clearance",
         "op": {"name": "side_minus", "by": s1["least_right_or_top_clearance"]},
         "expect": {"verdict": "ACCEPT", **none, "wall_contacts": s1["S1c_contacts"]}},
        {"id": "S1d", "kind": "file", "what": "the side lowered by that clearance and 1e-30 more",
         "op": {"name": "side_minus", "by": s1["least_right_or_top_clearance"], "and": EPS},
         "expect": {"verdict": "REFUSE", **none, "wall_crossings": s1["S1c_contacts"]}},
        {"id": "S1e", "kind": "file",
         "what": "the packing translated by minus the least left and bottom clearances, in the box of its extent",
         "op": {"name": "fit_box", "dx": s1["S1e"]["shift"][0], "dy": s1["S1e"]["shift"][1], "side": s1["S1e"]["side"]},
         "expect": {"verdict": "ACCEPT", **none, "wall_contacts": s1["S1e"]["contacts"], "margin_list_sha256": ml0}},
        {"id": "S1f", "kind": "file", "what": "the same box less 1e-30",
         "op": {"name": "fit_box", "dx": s1["S1e"]["shift"][0], "dy": s1["S1e"]["shift"][1], "side": s1["S1e"]["side"], "and": EPS},
         "expect": {"verdict": "REFUSE", **none,
                    "wall_contacts": [c for c in s1["S1e"]["contacts"] if c[1] in ("left", "bottom")],
                    "wall_crossings": s1["S1f_crossings"]}},
        {"id": "S4c", "kind": "file",
         "what": f"square {s4['mover']} moved toward {s4['toward']} along their centre line to exact contact",
         "op": {"name": "close_pair", "mover": s4["mover"], "toward": s4["toward"], "tau": s4["tau_contact"]},
         "expect": {"verdict": "ACCEPT", **none, "touching_pairs": [sorted([s4["mover"], s4["toward"]])],
                    "pair": {"pair": sorted([s4["mover"], s4["toward"]]), "A_margin": "0/1", "B_class": "contact", "B_area": "0/1"}}},
        {"id": "S4p", "kind": "file", "what": "the same, 1e-30 past contact",
         "op": {"name": "close_pair", "mover": s4["mover"], "toward": s4["toward"], "tau": s4["tau_past"]},
         "expect": {"verdict": "REFUSE", **none, "overlapping_pairs": [sorted([s4["mover"], s4["toward"]])],
                    "pair": {"pair": sorted([s4["mover"], s4["toward"]]), "A_margin": "-" + EPS, "B_class": "overlap"}}},
        {"id": "S5", "kind": "pair-level",
         "what": "every pair closed along its centre line to exact contact and 1e-30 past it",
         "op": {"name": "close_every_pair"},
         "expect": {"pairs": pf["S5"]["pairs"], "at_contact": {"A_margin": "0/1", "B_class": "contact"},
                    "past": {"A_margin": "-" + EPS, "B_class": "overlap"},
                    "closing_times_sha256": pf["S5"]["closing_times_sha256"]}},
        {"id": "S6", "kind": "square-level",
         "what": "every square moved to its nearest wall by its clearance, and 1e-30 past",
         "op": {"name": "every_square_to_wall"},
         "expect": {"squares": n, "at_contact": {"A_clearance": "0/1", "B_class": "contact", "B_area_in_box": "1/1"},
                    "past": {"A_clearance": "-" + EPS, "B_class": "crossing", "B_area_in_box_below_1": True},
                    "list_sha256": pf["S6"]["list_sha256"]}},
    ]
    plan = {
        "program": "l169_make_plan.py",
        "stated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "certificate_sha256": check["sha256"],
        "check_receipt_margin_list_sha256": ml0,
        "check_receipt_clearance_list_sha256": cl0,
        "epsilon": EPS,
        "rule": "every whole-file control is written as text, read back through the reader and decided by both methods over every square, wall and pair; each stated field must equal the decision's exactly",
        "controls": controls,
    }
    with open(argv[3], "w") as fh:
        json.dump(plan, fh, indent=1)
        fh.write("\n")
    print(f"stated {len(controls)} controls at {plan['stated_at']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
