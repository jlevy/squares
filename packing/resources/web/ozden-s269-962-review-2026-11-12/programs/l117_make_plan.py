"""Lane L117: state the controls and their outcomes. Decides nothing.

Clean-room code for the stage 4 review of jlevy/squares#962. Reads the frozen check
receipt and the plan facts and writes controls-plan.json, which is hashed before
l117_controls.py is written.

Usage: python -I -B l117_make_plan.py CHECK.json FACTS.json OUT.json
"""

from __future__ import annotations

import json
import sys

ALL = "both methods, every square, wall and pair"
WALLS_ONLY = "both methods, every square's four walls (no pair depends on the side)"


def main(argv: list[str]) -> int:
    with open(argv[1], encoding="utf-8") as fh:
        check = json.load(fh)
    with open(argv[2], encoding="utf-8") as fh:
        facts = json.load(fh)
    n = check["n"]
    contacts = sorted(check["walls"]["contacts"])
    sha = check["pairs"]["margin_list_sha256"]
    least = check["pairs"]["least_margin"][0:3]
    transpose = {"left": "bottom", "bottom": "left", "right": "top", "top": "right"}
    rot90 = {"left": "bottom", "bottom": "right", "top": "left", "right": "top"}
    i0, j0 = facts["S4_closest_pair"][0:2]
    near_walls_only = sorted(c for c in contacts if c[1] in ("left", "bottom"))
    controls = [
        {"id": "G1", "what": "square 269 given square 1's corners", "decided_by": ALL,
         "expect": {"verdict": "REFUSE", "overlap_pairs": [[1, n]], "contact_pairs": [],
                    "least_margin": [1, n, "-1"], "overlap_area_sum_B": "1", "contacts": contacts}},
        {"id": "G2", "what": "square 1 translated by (S, 0)", "decided_by": ALL,
         "expect": {"verdict": "REFUSE", "outside": [[1, "right"]], "centre_outside_B": [1],
                    "overlap_pairs": [], "contact_pairs": [], "contacts": contacts},
         "basis": f"square 1 clears the left wall by {facts['square_1_clearances']['left']}, so the moved square lies strictly right of x = S"},
        {"id": "G3", "what": "square 269's entry deleted, in the YAML and the twin", "decided_by": "the reader",
         "expect": {"refused_for": f"{n - 1} squares for n = {n}"}},
        {"id": "G4", "what": "square 269's id set to 1, in the YAML and the twin", "decided_by": "the reader",
         "expect": {"refused_for": f"square {n} id"}},
        {"id": "G5", "what": "square 1's third corner moved 1e-30 in x", "decided_by": ALL,
         "expect": {"verdict": "REFUSE", "not_unit_A": [1], "not_unit_B": [1]}},
        {"id": "G6", "what": "every square reflected in its own horizontal centre line (the rotation read the other way)",
         "decided_by": ALL,
         "expect": {"verdict": "REFUSE", "unit_both": n, "clockwise": n, "outside": [], "contacts": contacts,
                    "overlap_pairs": "non-empty, the same by both methods", "class_disagreements": 0}},
        {"id": "G7", "what": "the twin's side altered in its last digit (twin only)", "decided_by": "the reader",
         "expect": {"refused_for": "json twin differs"}},
        {"id": "G8", "what": "every corner transposed, (x, y) to (y, x)", "decided_by": ALL,
         "expect": {"verdict": "ACCEPT", "clockwise": n,
                    "contacts": sorted([k, transpose[w]] for k, w in contacts),
                    "margin_list_sha256": sha, "least_margin": least}},
        {"id": "G9", "what": "the side written as 2p/2q, in the YAML and the twin", "decided_by": "the reader",
         "expect": {"refused_for": "scalar not in lowest terms"}},
        {"id": "G10", "what": "every square listed from its second corner", "decided_by": ALL,
         "expect": {"verdict": "ACCEPT", "counterclockwise": n, "contacts": contacts,
                    "margin_list_sha256": sha, "least_margin": least}},
        {"id": "G11", "what": "every square listed in the reverse cyclic order", "decided_by": ALL,
         "expect": {"verdict": "ACCEPT", "clockwise": n, "contacts": contacts,
                    "margin_list_sha256": sha, "least_margin": least}},
        {"id": "G12", "what": "the whole packing turned a quarter about the box centre, (x, y) to (S - y, x)",
         "decided_by": ALL,
         "expect": {"verdict": "ACCEPT", "counterclockwise": n,
                    "contacts": sorted([k, rot90[w]] for k, w in contacts),
                    "margin_list_sha256": sha, "least_margin": least}},
        {"id": "S1a", "what": "the side lowered by 1/q, one unit of its own last place", "decided_by": WALLS_ONLY,
         "expect": {"verdict": "REFUSE", "outside": sorted(facts["S1a_lower_by_1_over_q"]["outside"])}},
        {"id": "S1b", "what": "the side lowered by 1e-30", "decided_by": WALLS_ONLY,
         "expect": {"verdict": "REFUSE", "outside": sorted(facts["S1b_lower_by_1e-30"]["outside"])},
         "basis": f"no positive far-wall clearance is below 1e-30; the least is {facts['least_positive_far_clearance']}"},
        {"id": "S1c", "what": f"the side set to its 12-place floor, {facts['floor_12']}", "decided_by": WALLS_ONLY,
         "expect": {"verdict": "REFUSE", "outside": sorted(facts["S1c_floor_12"]["outside"])},
         "basis": f"exactly the right and top clearances below the drop of {facts['S1c_floor_12_drop']}"},
        {"id": "S1d", "what": f"the side set to its 12-place ceiling, the claim {facts['claim']}", "decided_by": WALLS_ONLY,
         "expect": {"verdict": "ACCEPT", "outside": [], "contacts": near_walls_only}},
        {"id": "S4c", "what": f"square {j0} moved toward square {i0} along their centre line to exact contact",
         "decided_by": f"both methods, every pair of square {j0} and every square's walls",
         "expect": {"verdict": "ACCEPT", "contact_pairs": [[i0, j0]], "overlap_pairs": [],
                    "least_margin": [i0, j0, "0"], "outside": []},
         "basis": facts["S4"][f"move {j0} toward {i0}"]},
        {"id": "S4p", "what": "the same, 1e-30 past contact", "decided_by": f"both methods, every pair of square {j0} and every square's walls",
         "expect": {"verdict": "REFUSE", "contact_pairs": [], "overlap_pairs": [[i0, j0]],
                    "least_margin": [i0, j0, "-1/" + "1" + "0" * 30], "outside": []}},
        {"id": "S5", "what": "every pair below 1e-12 closed along its centre line, the second square moved (pair-level)",
         "decided_by": "both methods, that pair",
         "expect": {"pairs": facts["S5_pairs_below_1e-12"], "at_contact": "contact by both, margin exactly 0",
                    "past": "overlap by both, margin exactly -1e-30"}},
        {"id": "S6", "what": "every square moved to its nearest wall by its clearance, and 1e-30 past (square-level)",
         "decided_by": "both methods, that square's four walls",
         "expect": {"squares": n, "at_contact": "that wall contact by both, clearance exactly 0, no wall outside",
                    "past": "that wall outside by both, clearance exactly -1e-30, no other wall outside"}},
    ]
    plan = {
        "program": "l117_make_plan.py",
        "certificate_sha256": check["source"]["yaml_sha256"],
        "conventions": "contact is a margin or clearance of exactly 0; past is 1e-30 beyond it; "
        "pairs and contacts are 1-based ids; outside lists [square, wall] by both methods",
        "controls": controls,
    }
    with open(argv[3], "w", encoding="utf-8") as fh:
        json.dump(plan, fh, indent=1)
        fh.write("\n")
    print(len(controls), "controls stated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
