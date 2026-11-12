"""State the 20 controls and the outcome of each, before the controls program exists.

Lane L127, clean room. Decides nothing. Usage:

    python -I -B l127_make_plan.py CHECK.json FACTS.json PLAN.json

Each control names its change, what decides it (the reader, or both methods over every
square, wall and pair of the changed file, or a pair-level or square-level decision), and
its stated outcome as keys the controls program compares exactly.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def main(argv: list[str]) -> int:
    rec = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    facts = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    contacts = sorted(rec["wall_contacts"])
    sha = rec["margin_list_sha256"]
    n = rec["n"]
    assert contacts == sorted(facts["contacts"])

    def moved_contacts(mapping: dict[str, str]) -> list[list[Any]]:
        return sorted([k, mapping[w]] for k, w in contacts)

    left_bottom = sorted([k, w] for k, w in contacts if w in ("left", "bottom"))
    s1 = facts["S1"]
    s4 = facts["S4"]["chosen"]
    pair = facts["S4"]["pair"]

    def whole(**expect: Any) -> dict[str, Any]:
        base = {
            "not_unit_a": [],
            "not_unit_b": [],
            "pair_disagreements": [],
            "wall_disagreements": [],
            "touching_pairs": [],
            "overlapping_pairs": [],
            "outside_a": [],
            "outside_b": [],
            "not_inside_b": [],
            "wall_contacts": contacts,
        }
        base.update(expect)
        return base

    controls: list[dict[str, Any]] = [
        {
            "id": "G1",
            "change": "square 269 given square 1's corners",
            "decided_by": "both methods, whole file",
            "expect": whole(verdict="REFUSE", overlapping_pairs=[[1, 269]], overlap_margin="-1", overlap_area="1"),
            "statement": "refused: exactly the pair (1, 269) overlapping, margin -1, area 1; contacts unchanged",
        },
        {
            "id": "G2",
            "change": "square 1 translated by (S, 0)",
            "decided_by": "both methods, whole file",
            "expect": whole(verdict="REFUSE", outside_a=[[1, "right"]], outside_b=[[1, "right"]], not_inside_b=[1]),
            "statement": (
                "refused: square 1 outside the right wall by both methods and not inside by B's "
                f"area test; no pair overlapping or touching (square 1 clears the left wall by {facts['G2']['square1_left_clearance']}); "
                "contacts unchanged"
            ),
        },
        {
            "id": "G3",
            "change": "square 269's entry deleted, in the YAML and the twin",
            "decided_by": "the reader",
            "expect": {"refused": "268 entries for n = 269"},
            "statement": "the reader refuses: 268 entries",
        },
        {
            "id": "G4",
            "change": "square 269's id set to 1, in the YAML and the twin",
            "decided_by": "the reader",
            "expect": {"refused": "squares[268]: id is not 269"},
            "statement": "the reader refuses the id",
        },
        {
            "id": "G5",
            "change": "square 1's third corner moved 1e-30 in x",
            "decided_by": "both methods, whole file",
            "expect": {"verdict": "REFUSE", "not_unit_a": [1], "not_unit_b": [1]},
            "statement": "refused: square 1 not a unit square by either method",
        },
        {
            "id": "G6",
            "change": "every square reflected in its own horizontal centre line (the rotation read the other way)",
            "decided_by": "both methods, whole file",
            "expect": whole(verdict="REFUSE", overlapping_pairs="nonempty", cw_count=n, ccw_count=0),
            "statement": (
                "refused for overlapping pairs, the same classes by both methods; every square still a unit square "
                "inside (each reflection keeps the square's bounding box), contacts unchanged, all listed clockwise"
            ),
        },
        {
            "id": "G7",
            "change": "the twin's side altered in its last digit",
            "decided_by": "the reader",
            "expect": {"refused": "json twin differs"},
            "statement": "the reader refuses: the twin differs",
        },
        {
            "id": "G8",
            "change": "every corner transposed, (x, y) -> (y, x)",
            "decided_by": "both methods, whole file",
            "expect": whole(
                verdict="ACCEPT",
                wall_contacts=moved_contacts({"left": "bottom", "bottom": "left", "top": "right", "right": "top"}),
                cw_count=n,
                ccw_count=0,
                margin_list_sha256=sha,
            ),
            "statement": "accepted, contacts transposed, all listed clockwise, the SHA-256 of the exact margin list unchanged",
        },
        {
            "id": "G9",
            "change": "the side written as 2p/2q, in the YAML and the twin",
            "decided_by": "the reader",
            "expect": {"refused": "scalar not in lowest terms at side"},
            "statement": "the reader refuses: not in lowest terms",
        },
        {
            "id": "G10",
            "change": "every square listed from its second corner",
            "decided_by": "both methods, whole file",
            "expect": whole(verdict="ACCEPT", ccw_count=n, cw_count=0, margin_list_sha256=sha),
            "statement": "accepted, contacts and margin list unchanged",
        },
        {
            "id": "G11",
            "change": "every square listed in the reverse cyclic order",
            "decided_by": "both methods, whole file",
            "expect": whole(verdict="ACCEPT", cw_count=n, ccw_count=0, margin_list_sha256=sha),
            "statement": "accepted, contacts and margin list unchanged, all listed clockwise",
        },
        {
            "id": "G12",
            "change": "the whole packing turned a quarter about the box centre, (x, y) -> (S - y, x)",
            "decided_by": "both methods, whole file",
            "expect": whole(
                verdict="ACCEPT",
                wall_contacts=moved_contacts({"left": "bottom", "bottom": "right", "right": "top", "top": "left"}),
                ccw_count=n,
                cw_count=0,
                margin_list_sha256=sha,
            ),
            "statement": "accepted, contacts turned, all counterclockwise, margin list unchanged",
        },
        {
            "id": "S1a",
            "change": "the side lowered by 1/q, one unit of its own last place",
            "decided_by": "both methods, whole file",
            "expect": whole(
                verdict="REFUSE",
                outside_a=s1["S1a_one_unit_of_last_place"]["outside"],
                outside_b=s1["S1a_one_unit_of_last_place"]["outside"],
                not_inside_b=sorted({k for k, _ in s1["S1a_one_unit_of_last_place"]["outside"]}),
                wall_contacts=left_bottom,
                margin_list_sha256=sha,
            ),
            "statement": "refused: exactly square 199 outside, at the top wall",
        },
        {
            "id": "S1b",
            "change": "the side lowered by 1e-30",
            "decided_by": "both methods, whole file",
            "expect": whole(
                verdict="REFUSE",
                outside_a=s1["S1b_1e-30"]["outside"],
                outside_b=s1["S1b_1e-30"]["outside"],
                not_inside_b=sorted({k for k, _ in s1["S1b_1e-30"]["outside"]}),
                wall_contacts=left_bottom,
                margin_list_sha256=sha,
            ),
            "statement": (
                "the same, since no positive right or top clearance is below 1e-30 "
                f"(the least is {facts['least_far_clearances'][0]['sci']})"
            ),
        },
        {
            "id": "S1c",
            "change": f"the side set to its 12-place floor, {facts['floor12_decimal']}",
            "decided_by": "both methods, whole file",
            "expect": whole(
                verdict="REFUSE",
                outside_a=s1["S1c_floor12"]["outside"],
                outside_b=s1["S1c_floor12"]["outside"],
                not_inside_b=sorted({k for k, _ in s1["S1c_floor12"]["outside"]}),
                wall_contacts=left_bottom,
                margin_list_sha256=sha,
            ),
            "statement": (
                f"refused: exactly the {len(s1['S1c_floor12']['outside'])} right or top clearances below the drop of "
                f"{s1['S1c_floor12']['drop_sci']}"
            ),
        },
        {
            "id": "S1d",
            "change": f"the side set to its 12-place ceiling, the claim {facts['ceil12_decimal']}",
            "decided_by": "both methods, whole file",
            "expect": whole(verdict="ACCEPT", wall_contacts=left_bottom, margin_list_sha256=sha),
            "statement": "accepted, contacts at the bottom and left walls only",
        },
        {
            "id": "S4c",
            "change": f"square {s4['move']} moved toward square {s4['towards']} along their centre line to exact contact",
            "decided_by": "both methods, whole file",
            "expect": whole(verdict="ACCEPT", touching_pairs=[pair], least_margin_value="0"),
            "statement": f"the pair ({pair[0]}, {pair[1]}) alone touching by both, margin exactly 0, square {s4['move']} inside; accepted",
        },
        {
            "id": "S4p",
            "change": "the same, 1e-30 past (over the least binding rate)",
            "decided_by": "both methods, whole file",
            "expect": whole(
                verdict="REFUSE",
                overlapping_pairs=[pair],
                least_margin_value="-1/1000000000000000000000000000000",
            ),
            "statement": "that pair alone overlapping by both, margin exactly -1e-30",
        },
        {
            "id": "S5",
            "change": "every pair below 1e-12 closed along its centre line, to contact and 1e-30 past",
            "decided_by": "both methods, pair level",
            "expect": {
                "pairs": facts["S5"]["count"],
                "at": {"margin": "0", "class_a": "touch", "class_b": "touch"},
                "past": {"margin": "the closed form, -1e-30 for all", "class_a": "overlap", "class_b": "overlap"},
                "closing_digest": facts["S5"]["closing_digest"],
            },
            "statement": f"{facts['S5']['count']} of {facts['S5']['count']}: touching at contact by both, overlapping past, margins exactly 0 and -1e-30",
        },
        {
            "id": "S6",
            "change": "every square moved to its nearest wall by its clearance, and 1e-30 past",
            "decided_by": "both methods, square level",
            "expect": {
                "squares": n,
                "at": {"clearance": "0", "class_a": "touch", "class_b": "touch"},
                "past": {"clearance": "-1/1000000000000000000000000000000", "class_a": "outside", "class_b": "outside", "inside_b": False},
            },
            "statement": f"{n} of {n}: contact at, outside past, by both, clearance exactly 0 and -1e-30",
        },
    ]
    plan = {
        "program": "l127_make_plan.py",
        "certificate_margin_list_sha256": sha,
        "certificate_contacts": contacts,
        "contact_means": "a margin or clearance of exactly 0; past means 1e-30 beyond it",
        "controls": controls,
    }
    Path(argv[3]).write_text(json.dumps(plan, indent=1) + "\n", encoding="utf-8")
    print(len(controls), "controls stated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
