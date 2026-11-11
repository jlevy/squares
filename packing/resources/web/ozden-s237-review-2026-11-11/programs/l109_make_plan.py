"""Lane L109's controls plan: states each control and its outcome before any is run.

Usage: python -I -B l109_make_plan.py CHECK.json FACTS.json PLAN.json

Decides nothing. Reads the check receipt and the plan facts and writes the plan, with
each outcome stated both in words and as the exact fields the controls program must find.
"""

from __future__ import annotations

import json
import sys


def main() -> int:
    check_path, facts_path, plan_path = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(check_path, encoding="utf-8") as f:
        chk = json.load(f)
    with open(facts_path, encoding="utf-8") as f:
        fx = json.load(f)
    n = chk["read"]["n"]
    contacts = chk["wall_contacts"]
    transposed = {"left": "bottom", "bottom": "left", "right": "top", "top": "right"}
    lp = fx["least_pair"]
    controls = [
        {
            "id": "G1",
            "change": f"square {n} given square 1's corners",
            "scope": "whole file, both methods",
            "stated": f"refused: exactly the pair (1, {n}) overlapping, margin -1, area 1; no wall outside",
            "expect": {"verdict": "REFUSE", "overlapping_pairs": [[1, n]], "margin": "-1", "area": "1", "outside": [], "touching_pairs": []},
        },
        {
            "id": "G2",
            "change": "square 1 translated by (S, 0)",
            "scope": "square 1's pairs and walls, both methods",
            "stated": f"refused: square 1 outside the right wall only; no pair overlapping or touching (square 1 clears the left wall by {fx['square_1_clearances']['left']})",
            "expect": {"verdict": "REFUSE", "outside": [[1, "right"]], "overlapping_pairs": [], "touching_pairs": []},
        },
        {
            "id": "G3",
            "change": f"square {n}'s entry deleted (YAML and twin)",
            "scope": "the reader",
            "stated": f"the reader refuses: {n - 1} squares listed",
            "expect": {"reader_refuses_with": f"{n - 1} squares listed, n = {n}"},
        },
        {
            "id": "G4",
            "change": f"square {n}'s id set to 1 (YAML and twin)",
            "scope": "the reader",
            "stated": "the reader refuses the id",
            "expect": {"reader_refuses_with": f"square {n}: id 1"},
        },
        {
            "id": "G5",
            "change": "square 1's third corner moved 1e-30 in x",
            "scope": "square 1, both methods",
            "stated": "refused: square 1 not a unit square by either method",
            "expect": {"verdict": "REFUSE", "unit_failures_squares": [1], "unit_failures_methods": ["A", "B"]},
        },
        {
            "id": "G6",
            "change": "every square reflected in its own horizontal centre line (the rotation read the other way)",
            "scope": "whole file, both methods",
            "stated": "refused for overlapping pairs (at least one); every square still a unit square, now clockwise, inside, wall contacts unchanged",
            "expect": {"verdict": "REFUSE", "overlapping_pairs_at_least": 1, "unit_failures": [], "cw_squares": n, "outside": [], "wall_contacts": contacts},
        },
        {
            "id": "G7",
            "change": "the twin's side altered in its last digit (YAML unchanged)",
            "scope": "the reader",
            "stated": "the reader refuses: the twin differs",
            "expect": {"reader_refuses_with": "the JSON twin differs: $.witness.side: value differs"},
        },
        {
            "id": "G8",
            "change": "every corner transposed, (x, y) to (y, x)",
            "scope": "whole file, both methods",
            "stated": "accepted, contacts transposed, every margin exactly unchanged (same margin-list digest), every square now clockwise",
            "expect": {
                "verdict": "ACCEPT",
                "wall_contacts": sorted([[i, transposed[w]] for i, w in contacts]),
                "margin_list_sha256": chk["margin_list_sha256"],
                "cw_squares": n,
                "sum_of_clipped_pair_areas": "0",
            },
        },
        {
            "id": "G9",
            "change": "the side written as 2p/2q (YAML and twin)",
            "scope": "the reader",
            "stated": "the reader refuses: not in lowest terms",
            "expect": {"reader_refuses_with": "side: not in lowest terms"},
        },
        {
            "id": "S1a",
            "change": "the side lowered by 1/q, one unit of its own last place",
            "scope": "every square's walls, both methods",
            "stated": f"refused: exactly {fx['far_wall_clearance_below_one_over_q']} outside",
            "expect": {"verdict": "REFUSE", "outside": fx["far_wall_clearance_below_one_over_q"]},
        },
        {
            "id": "S1b",
            "change": "the side lowered by 1e-30",
            "scope": "every square's walls, both methods",
            "stated": f"refused: exactly {fx['far_wall_clearance_below_1e-30']} outside (least positive far-wall clearance {fx['least_positive_far_wall_clearance']})",
            "expect": {"verdict": "REFUSE", "outside": fx["far_wall_clearance_below_1e-30"]},
        },
        {
            "id": "S1c",
            "change": f"the side set to its 12-place floor, {fx['floor12']}",
            "scope": "every square's walls, both methods",
            "stated": f"refused: exactly the squares whose right or top clearance is below the drop of {fx['drop_to_floor12']}: {fx['far_wall_clearance_below_drop']}",
            "expect": {"verdict": "REFUSE", "outside": fx["far_wall_clearance_below_drop"]},
        },
        {
            "id": "S1d",
            "change": f"the side set to its 12-place ceiling, the claim {fx['ceil12']}",
            "scope": "every square's walls, both methods",
            "stated": f"accepted, wall contacts {fx['contacts_at_ceil12']} only",
            "expect": {"verdict": "ACCEPT", "wall_contacts": fx["contacts_at_ceil12"]},
        },
        {
            "id": "S4c",
            "change": f"square {lp['mover']} moved toward square {lp['still']} along their centre line to exact contact",
            "scope": f"square {lp['mover']}'s pairs and walls, both methods",
            "stated": f"that pair alone touching by both, margin exactly 0; square {lp['mover']} inside (move {lp['move_len_t1']} shorter than its next margin or clearance {lp['other_min_of_mover']})",
            "expect": {"verdict": "ACCEPT", "touching_pairs": [sorted(lp["pair"])], "overlapping_pairs": [], "outside": [], "margin": "0"},
        },
        {
            "id": "S4p",
            "change": "the same, 1e-30 past contact",
            "scope": f"square {lp['mover']}'s pairs and walls, both methods",
            "stated": "that pair alone overlapping by both, margin exactly -1e-30",
            "expect": {"verdict": "REFUSE", "overlapping_pairs": [sorted(lp["pair"])], "touching_pairs": [], "outside": [], "margin": "-1/1000000000000000000000000000000"},
        },
        {
            "id": "S5",
            "change": f"every pair below 1e-12 ({fx['near_pairs_count']}) closed along its centre line, and 1e-30 past",
            "scope": "pair-level, both methods",
            "stated": "touching by both at contact with margin exactly 0; overlapping by both past it with margin exactly -1e-30",
            "expect": {"pairs": fx["near_pairs_count"], "all_as_stated": True},
        },
        {
            "id": "S6",
            "change": "every square moved to its nearest wall by its clearance, and 1e-30 past",
            "scope": "square-level, both methods",
            "stated": "contact at that wall by both; outside it by both past it",
            "expect": {"squares": n, "all_as_stated": True},
        },
    ]
    plan = {
        "program": "l109_make_plan.py",
        "certificate_sha256": chk["certificate_sha256"],
        "definitions": "contact: a margin or clearance of exactly 0; past: 1e-30 beyond it",
        "controls": controls,
    }
    with open(plan_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=1)
        f.write("\n")
    print(f"plan: {len(controls)} controls")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
