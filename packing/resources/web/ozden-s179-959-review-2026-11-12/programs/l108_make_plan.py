"""State the controls and their outcomes before any control is run.

Lane L108, blind stage 4 review of jlevy/squares#959. Reads the frozen check receipt and
the plan facts; writes programs/controls-plan.json. Decides nothing.

Usage: python -I -B l108_make_plan.py CHECK.json FACTS.json PLAN.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def main(argv: list[str]) -> int:
    check = json.loads(Path(argv[1]).read_text(encoding="utf-8"))["result"]
    facts = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    base_contacts = check["wall_contacts"]
    base_sha = check["margin_list_sha256"]
    s4 = facts["s4"]
    a, b = s4["pair"]
    # The mover is the square of the pair whose move is shorter than all its other margins
    # and which stays inside; prefer the second.
    mover = b if s4[f"move_square_{b}"]["move_shorter_than_every_other_margin"] and s4[f"move_square_{b}"]["inside_at_contact_and_past"] else a
    assert s4[f"move_square_{mover}"]["move_shorter_than_every_other_margin"]
    assert s4[f"move_square_{mover}"]["inside_at_contact_and_past"]
    assert s4[f"move_square_{mover}"]["margin_past_is_minus_1e-30"]
    transposed = []
    swap = {"left": "bottom", "bottom": "left", "right": "top", "top": "right"}
    for c in base_contacts:
        k, w = c.split()
        transposed.append(f"{k} {swap[w]}")
    controls: list[dict[str, Any]] = [
        {
            "id": "G1",
            "change": "square 179 given square 1's corners",
            "scope": "every square, wall and pair",
            "expect": {"verdict": "REFUSE", "overlapping_pairs": [[1, 179]], "pair_margins": {"1 179": "-1"}, "pair_areas": {"1 179": "1"}, "touching_pairs": [], "walls_outside": [], "wall_contacts": base_contacts},
        },
        {
            "id": "G2",
            "change": "square 1 translated by (S, 0)",
            "scope": "every square, wall and pair",
            "why": f"square 1 clears the left wall by {facts['square_1_clearances']['left']}, so it lands wholly beyond the right wall",
            "expect": {"verdict": "REFUSE", "overlapping_pairs": [], "touching_pairs": [], "walls_outside": [[1, "right"]], "wall_contacts": base_contacts},
        },
        {"id": "G3", "change": "square 179's entry deleted (YAML and twin)", "expect": {"reader_refuses": "179"}},
        {"id": "G4", "change": "square 179's id set to 1 (YAML and twin)", "expect": {"reader_refuses": "square 179: id"}},
        {
            "id": "G5",
            "change": "square 1's third corner moved 1e-30 in x",
            "scope": "every square",
            "expect": {"verdict": "REFUSE", "not_unit_a": [1], "not_unit_b": [1]},
        },
        {
            "id": "G6",
            "change": "every square reflected in its own horizontal centre line (the rotation read the other way)",
            "scope": "every square, wall and pair",
            "why": "a reflection in the centre line keeps each square's bounding box, so every clearance is unchanged",
            "expect": {"verdict": "REFUSE", "overlapping_pairs": "at least one", "not_unit_a": [], "not_unit_b": [], "walls_outside": [], "wall_contacts": base_contacts, "counterclockwise": 0, "clockwise": 179},
        },
        {"id": "G7", "change": "the twin's side altered in its last digit", "expect": {"reader_refuses": "twin"}},
        {
            "id": "G8",
            "change": "every corner transposed, (x, y) to (y, x)",
            "scope": "every square, wall and pair",
            "expect": {"verdict": "ACCEPT", "wall_contacts_set": transposed, "margin_list_sha256": base_sha, "counterclockwise": 0, "clockwise": 179},
        },
        {"id": "G9", "change": "the side written as 2p/2q (YAML and twin)", "expect": {"reader_refuses": "lowest terms"}},
        {
            "id": "G10",
            "change": "every square listed from its second corner (a cyclic shift)",
            "scope": "every square, wall and pair",
            "expect": {"verdict": "ACCEPT", "wall_contacts": base_contacts, "margin_list_sha256": base_sha, "counterclockwise": 179, "clockwise": 0},
        },
        {
            "id": "G11",
            "change": "every square listed in the reverse cyclic order",
            "scope": "every square, wall and pair",
            "expect": {"verdict": "ACCEPT", "wall_contacts": base_contacts, "margin_list_sha256": base_sha, "counterclockwise": 0, "clockwise": 179},
        },
        {
            "id": "S1a",
            "change": "the side lowered by 1/q, one unit of its own last place",
            "scope": "every square's walls (pairs do not depend on the side)",
            "expect": {"verdict": "REFUSE", "walls_outside": facts["far_wall_below_1_over_q"]},
        },
        {
            "id": "S1b",
            "change": "the side lowered by 1e-30",
            "scope": "every square's walls",
            "expect": {"verdict": "REFUSE", "walls_outside": facts["far_wall_below_1e-30"]},
        },
        {
            "id": "S1c",
            "change": f"the side set to its 12-place floor, {facts['side_floor_12_decimal']}",
            "scope": "every square's walls",
            "why": f"the drop is {facts['side_less_floor']}",
            "expect": {"verdict": "REFUSE", "walls_outside": facts["far_wall_below_drop_to_floor"]},
        },
        {
            "id": "S1d",
            "change": f"the side set to its 12-place ceiling, the claim {facts['side_ceil_12_decimal']}",
            "scope": "every square's walls",
            "expect": {"verdict": "ACCEPT", "walls_outside": [], "wall_contacts": [f"{k} {w}" for k, w in facts["at_ceiling_contacts"]]},
        },
        {
            "id": "S4c",
            "change": f"square {mover} moved toward square {a if mover == b else b} along their centre line to exact contact",
            "scope": f"every pair and wall of square {mover}",
            "why": f"the move is shorter than square {mover}'s next margin ({s4[f'move_square_{mover}']['next_margin']})",
            "expect": {"verdict": "ACCEPT", "touching_pairs": [[a, b]], "overlapping_pairs": [], "pair_margins": {f"{a} {b}": "0"}, "walls_outside": [], "wall_contacts": base_contacts},
        },
        {
            "id": "S4p",
            "change": f"the same, 1e-30 past contact (on the binding axis)",
            "scope": f"every pair and wall of square {mover}",
            "expect": {"verdict": "REFUSE", "touching_pairs": [], "overlapping_pairs": [[a, b]], "pair_margins": {f"{a} {b}": "-1/1000000000000000000000000000000"}, "walls_outside": []},
        },
        {
            "id": "S5",
            "change": "every pair with margin below 1e-12 closed along its centre line (the second square moves), at contact and 1e-30 past",
            "scope": "each pair alone",
            "expect": {"pairs": facts["s5"]["pairs"], "at_contact": "margin exactly 0 by A, contact by B", "past": "margin exactly -1e-30 by A, overlap by B", "as_stated": facts["s5"]["pairs"]},
        },
        {
            "id": "S6",
            "change": "every square moved to its nearest wall by its clearance, and 1e-30 past",
            "scope": "each square's four walls",
            "expect": {"squares": 179, "at": "contact at that wall by both", "past": "outside at that wall by both", "as_stated": 179},
        },
    ]
    plan = {
        "lane": "L108",
        "stated_from": ["out/check-n179.json", "out/plan-facts-n179.json"],
        "conventions": "contact is a margin or clearance of exactly 0; past is 1e-30 beyond it; a reader control changes the YAML and the twin alike unless it says otherwise",
        "s4_mover": mover,
        "controls": controls,
    }
    Path(argv[3]).write_text(json.dumps(plan, indent=1) + "\n", encoding="utf-8")
    print(len(controls), "controls stated; S4 mover", mover)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
