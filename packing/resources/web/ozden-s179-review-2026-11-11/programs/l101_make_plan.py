"""Write the controls plan: each control and its stated outcome, before any control runs.

Usage: python -I -B l101_make_plan.py CHECK.json PLAN_FACTS.json OUT.json

The outcomes are stated from the accepted base's check receipt and the plan facts. No
controls program exists when this runs.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    check = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    facts = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    n = check["reading"]["n"]
    contacts = sorted(check["wall_contacts"])
    swap = {"left": "bottom", "bottom": "left", "right": "top", "top": "right"}
    lp = facts["least_pair"]
    near = len(check["near_pairs_exact"])
    controls = [
        {"id": "G1", "change": f"square {n} given square 1's corners",
         "decided": f"every pair and wall of square {n}, both methods",
         "stated": {"verdict": "REFUSE", "overlapping_pairs": [[1, n]], "margin": "-1", "area": "1",
                    "touching_pairs": [], "wall_outside": []}},
        {"id": "G2", "change": "square 1 translated by (S, 0)",
         "decided": "every pair and wall of square 1, both methods",
         "stated": {"verdict": "REFUSE", "wall_outside": [[1, "right"]], "overlapping_pairs": [],
                    "touching_pairs": [],
                    "why": f"square 1 clears the left wall by {facts['square1_left_clearance']}, so it lands wholly beyond x = S"}},
        {"id": "G3", "change": f"square {n}'s entry deleted from the YAML and the twin",
         "decided": "the reader", "stated": {"reader": "refuses", "reason_contains": f"holds {n - 1} entries"}},
        {"id": "G4", "change": f"square {n}'s id set to 1 in the YAML and the twin",
         "decided": "the reader", "stated": {"reader": "refuses", "reason_contains": "is not"}},
        {"id": "G5", "change": "square 1's third corner moved 1e-30 in x",
         "decided": "square 1's shape, both methods",
         "stated": {"verdict": "REFUSE", "not_unit_A": [1], "not_unit_B": [1]}},
        {"id": "G6", "change": "every square reflected in its horizontal centre line (the rotation read the other way)",
         "decided": "every square, wall and pair, both methods",
         "stated": {"verdict": "REFUSE", "overlapping_pairs": "some (count reported)", "not_unit": [],
                    "wall_contacts": contacts, "wall_outside": [], "classes_agree": True}},
        {"id": "G7", "change": "the twin's side altered in its last digit",
         "decided": "the reader", "stated": {"reader": "refuses", "reason_contains": "JSON twin"}},
        {"id": "G8", "change": "every corner transposed, (x, y) to (y, x)",
         "decided": "every square, wall and pair, both methods",
         "stated": {"verdict": "ACCEPT", "wall_contacts": sorted([s, swap[wl]] for s, wl in contacts),
                    "margins_sha256": check["margins_sha256"], "classes_agree": True}},
        {"id": "G9", "change": "the side written as 2p/2q in the YAML and the twin",
         "decided": "the reader", "stated": {"reader": "refuses", "reason_contains": "lowest terms"}},
        {"id": "S1a", "change": "the side lowered by 1/q, one unit of its own last place",
         "decided": "every square's walls, both methods",
         "stated": {"verdict": "REFUSE", "wall_outside": facts["far_wall_contacts"],
                    "why": "no positive far-wall clearance is below 1/q"
                    if facts["least_positive_far_clearance_above_1_over_q"] else "UNEXPECTED"}},
        {"id": "S1b", "change": "the side lowered by 1e-30",
         "decided": "every square's walls, both methods",
         "stated": {"verdict": "REFUSE", "wall_outside": facts["far_wall_contacts"],
                    "why": f"the least positive far-wall clearance is {facts['least_positive_far_clearance']['value']}"
                    if facts["least_positive_far_clearance_above_1e-30"] else "UNEXPECTED"}},
        {"id": "S1c", "change": f"the side set to its 12-place floor, {facts['floor12']}",
         "decided": "every square's walls, both methods",
         "stated": {"verdict": "REFUSE", "squares_outside": facts["cut_by_floor12"],
                    "why": f"exactly these squares' right or top clearance is below the drop {facts['drop_to_floor12']}"}},
        {"id": "S1d", "change": f"the side set to its 12-place ceiling, the claim {facts['ceil12_decimal']}",
         "decided": "every square's walls, both methods",
         "stated": {"verdict": "ACCEPT", "wall_contacts": facts["near_wall_contacts"], "wall_outside": []}},
        {"id": "S4c", "change": f"square {lp['moved']} moved toward square {lp['fixed']} along the line of centres to exact contact (t = t_contact)",
         "decided": f"every pair and wall of square {lp['moved']}, both methods",
         "stated": {"verdict": "ACCEPT", "touching_pairs": [sorted([lp["fixed"], lp["moved"]])],
                    "overlapping_pairs": [],
                    "margin": "0", "wall_outside": [], "wall_contacts_of_moved": [],
                    "why": f"the move, {lp['move_euclid_approx']} in length, is below every other margin of square {lp['moved']} (least {lp['least_other_margin_of_moved']})"}},
        {"id": "S4p", "change": "the same, to t_past",
         "decided": f"every pair and wall of square {lp['moved']}, both methods",
         "stated": {"verdict": "REFUSE", "overlapping_pairs": [sorted([lp["fixed"], lp["moved"]])],
                    "margin": "-1e-30", "touching_pairs": [], "wall_outside": []}},
        {"id": "S5", "change": f"each of the {near} pairs below 1e-12 closed along its line of centres, pair by pair",
         "decided": "that pair alone, both methods, at t_contact and t_past",
         "stated": {"at_contact": "contact by both, margin exactly 0",
                    "past": "overlap by both, margin exactly -1e-30", "pairs": near,
                    "why": "every active piece decreases at contact"
                    if facts["near_pairs_all_decreasing"] else "UNEXPECTED"}},
        {"id": "S6", "change": "each square moved toward its nearest wall by its clearance, and 1e-30 past",
         "decided": "that square's four walls, both methods",
         "stated": {"at": "contact with that wall by both", "past": "outside that wall by both",
                    "squares": n, "ties": facts["nearest_wall_ties"]}},
    ]
    plan = {
        "program": "l101_make_plan.py",
        "base_check_sha256_of_margins": check["margins_sha256"],
        "plan_facts_program": facts["program"],
        "controls": controls,
    }
    Path(sys.argv[3]).write_text(json.dumps(plan, indent=1) + "\n", encoding="utf-8")
    print(len(controls), "controls stated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
