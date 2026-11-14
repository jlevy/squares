"""Lane L153 controls plan: state every control and its outcome before running any.

Clean-room: written for this review, importing nothing from this repository or the
source, and reusing no code of any earlier review.

It decides nothing. From the three check receipts and the three plan-facts files it
writes `controls-plan.json`, which states for each certificate the controls below and
the outcome each must have; `l153_controls.py` is written after this plan is hashed.

Usage: l153_make_plan.py OUT.json (LABEL CHECK.json FACTS.json HAS_TWIN)...
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

WALL_ORDER = ("left", "right", "bottom", "top")
TRANSPOSE = {"left": "bottom", "bottom": "left", "right": "top", "top": "right"}
QUARTER = {"left": "bottom", "bottom": "right", "right": "top", "top": "left"}


def sort_walls(items: list[list]) -> list[list]:
    return sorted(([k, w] for k, w in items), key=lambda x: (x[0], WALL_ORDER.index(x[1])))


def sort_pairs(items) -> list[list[int]]:
    return sorted([min(p), max(p)] for p in items)


def plan_for(label: str, check: dict, facts: dict, has_twin: bool) -> list[dict]:
    n = check["n"]
    walls = check["walls"]["contacts"]
    contacts = sort_pairs(check["pairs"]["contacts"])
    msha = check["pairs"]["margin_list_sha256"]
    csha = check["walls"]["clearance_list_sha256"]
    lb_walls = sort_walls([x for x in walls if x[1] in ("left", "bottom")])
    out: list[dict] = []

    def add(cid: str, what: str, outcome: dict) -> None:
        out.append({"id": cid, "what": what, "outcome": outcome})

    sq1_walls = facts["square_1_wall_contacts"]
    add(
        "G1",
        f"square {n} given square 1's pose",
        {
            "verdict": "REFUSE",
            "overlaps": [[1, n]],
            "overlap_margin": "-1",
            "overlap_area": "1",
            "contacts": sort_pairs(
                [p for p in contacts if n not in p]
                + [
                    [p[0] + p[1] - 1, n]
                    for p in facts["square_1_pair_contacts"]
                    if n not in p
                ]
            ),
            "wall_contacts": sort_walls(
                [x for x in walls if x[0] != n] + [[n, w] for _, w in sq1_walls]
            ),
            "crossing": [],
        },
    )
    if not facts["G2_no_touch"]:
        raise SystemExit("G2's no-touch condition fails; restate G2")
    new1 = [[1, w] for w, v in facts["square_1_after_G2"].items() if v == "0"]
    add(
        "G2",
        "square 1 translated by (S, 0)",
        {
            "verdict": "REFUSE",
            "overlaps": [],
            "contacts": sort_pairs([p for p in contacts if 1 not in p]),
            "wall_contacts": sort_walls([x for x in walls if x[0] != 1] + new1),
            "crossing": [[1, "right"]],
            "not_inside_b": [1],
        },
    )
    add("G3", f"square {n}'s entry deleted" + (" (JSON and twin)" if has_twin else ""),
        {"reader_refuses": "squares listed"})
    add("G4", "the side written as 2p/2q" + (" (JSON and twin)" if has_twin else ""),
        {"reader_refuses": "not in lowest terms"})
    add(
        "G5",
        "square 1's sin moved by 10^-30",
        {"verdict": "REFUSE", "not_unit": [1], "unit_disagree": []},
    )
    add(
        "G6",
        "every basis (c, s) read as (c, -s): each square reflected in its own horizontal "
        "centre line, the rotation read the other way",
        {
            "verdict": "REFUSE",
            "overlaps_nonempty": True,
            "wall_contacts": sort_walls(walls),
            "crossing": [],
            "clearance_list_sha256": csha,
        },
    )
    if has_twin:
        add("G7", "the twin's side altered in its last digit (3 to 1)",
            {"reader_refuses": "twin's side differs"})
    add(
        "G8",
        "every square transposed: (cx, cy, c, s) to (cy, cx, s, c)",
        {
            "verdict": "ACCEPT",
            "contacts": contacts,
            "wall_contacts": sort_walls([[k, TRANSPOSE[w]] for k, w in walls]),
            "margin_list_sha256": msha,
        },
    )
    add(
        "G9",
        "every basis replaced by the square's other edge direction (-s, c)",
        {
            "verdict": "ACCEPT",
            "contacts": contacts,
            "wall_contacts": sort_walls(walls),
            "margin_list_sha256": msha,
            "clearance_list_sha256": csha,
        },
    )
    add(
        "G10",
        "every basis negated (-c, -s)",
        {
            "verdict": "ACCEPT",
            "contacts": contacts,
            "wall_contacts": sort_walls(walls),
            "margin_list_sha256": msha,
            "clearance_list_sha256": csha,
        },
    )
    add(
        "G11",
        "the packing turned a quarter about the box centre: (x, y) to (S - y, x), "
        "basis (c, s) to (-s, c)",
        {
            "verdict": "ACCEPT",
            "contacts": contacts,
            "wall_contacts": sort_walls([[k, QUARTER[w]] for k, w in walls]),
            "margin_list_sha256": msha,
        },
    )
    for cid, key, what in (
        ("S1a", "S1a", "the side lowered by 1/q, one unit of its own last place"),
        ("S1b", "S1b", "the side lowered by 10^-90"),
        ("S1c", "S1c", f"the side set to its 12-place floor, {facts['floor12']}"),
    ):
        pushed = sort_walls(facts[f"{key}_pushed"])
        touching = sort_walls(facts[f"{key}_touching"])
        add(
            cid,
            what,
            {
                "verdict": "REFUSE",
                "crossing": pushed,
                "not_inside_b": sorted({k for k, _ in pushed}),
                "wall_contacts": sort_walls(lb_walls + touching),
                "contacts": contacts,
                "margin_list_sha256": msha,
            },
        )
    add(
        "S1d",
        f"the side set to its 12-place ceiling, the claim {facts['ceil12']}",
        {
            "verdict": "ACCEPT",
            "wall_contacts": sort_walls(facts["S1d_contacts"]),
            "contacts": contacts,
            "margin_list_sha256": msha,
        },
    )
    s4 = facts["S4"]
    pair = s4["pair"]
    add(
        "S4c",
        f"square {s4['mover']} moved toward square {s4['toward']} along their centre line "
        f"to exact contact (t = t_contact of the plan facts)",
        {
            "verdict": "ACCEPT",
            "overlaps": [],
            "contacts": sort_pairs(contacts + [pair]),
            "pair_margin": {"pair": pair, "value": "0"},
            "wall_contacts": sort_walls(walls),
        },
    )
    add(
        "S4p",
        f"the same, 10^-90 past contact over the slowest binding rate (t = t_past)",
        {
            "verdict": "REFUSE",
            "overlaps": [pair],
            "overlap_margin": s4["margin_past"],
            "contacts": contacts,
            "wall_contacts": sort_walls(walls),
        },
    )
    add(
        "S5",
        f"every positive pair below 10^-12 ({facts['S5']['pairs']}) closed along its "
        "centre line, the second square moving (pair-level, both methods)",
        {
            "pairs": facts["S5"]["pairs"],
            "at_contact": "margin exactly 0 by A, contact by B",
            "past": "margin exactly the plan's closed-form value by A, overlap by B",
            "digest_times_and_past_margins": facts["S5"]["digest_times_and_past_margins"],
            "past_margin_minus_1e90_exactly": facts["S5"]["past_margin_minus_1e90_exactly"],
        },
    )
    add(
        "S6",
        f"every square ({n}) moved to its nearest wall by its clearance, and 10^-90 past "
        "(square-level, both methods)",
        {
            "squares": n,
            "at": "clearance exactly 0 by A, contact by B",
            "past": "clearance exactly -10^-90 by A, crossing by B",
            "by_wall": facts["S6"]["by_wall"],
        },
    )
    return out


def main(argv: list[str]) -> int:
    out_path = argv[1]
    rest = argv[2:]
    plan: dict = {
        "program": "l153_make_plan.py",
        "past": "1/10^90",
        "rule": "every whole-file control is decided by both methods over every square, "
        "wall and pair; S5 and S6 decide the moved pair or square; an outcome lists only "
        "what it states, and every control also requires the two methods to agree on every "
        "class they decide",
        "files": {},
    }
    for k in range(0, len(rest), 4):
        label, check_path, facts_path, has_twin = rest[k : k + 4]
        check = json.loads(Path(check_path).read_text())
        facts = json.loads(Path(facts_path).read_text())
        plan["files"][label] = {
            "check_receipt_sha256": hashlib.sha256(Path(check_path).read_bytes()).hexdigest(),
            "plan_facts_sha256": hashlib.sha256(Path(facts_path).read_bytes()).hexdigest(),
            "controls": plan_for(label, check, facts, has_twin == "twin"),
        }
    # One control per line, so the plan stays small and reads line by line.
    lines = ["{"]
    for key in ("program", "past", "rule"):
        lines.append(f" {json.dumps(key)}: {json.dumps(plan[key])},")
    lines.append(' "files": {')
    labels = list(plan["files"])
    for li, label in enumerate(labels):
        entry = plan["files"][label]
        lines.append(f"  {json.dumps(label)}: {{")
        lines.append(f'   "check_receipt_sha256": {json.dumps(entry["check_receipt_sha256"])},')
        lines.append(f'   "plan_facts_sha256": {json.dumps(entry["plan_facts_sha256"])},')
        lines.append('   "controls": [')
        controls = entry["controls"]
        for ci, control in enumerate(controls):
            comma = "," if ci < len(controls) - 1 else ""
            lines.append("    " + json.dumps(control, separators=(", ", ": ")) + comma)
        lines.append("   ]")
        lines.append("  }" + ("," if li < len(labels) - 1 else ""))
    lines.append(" }")
    lines.append("}")
    text = "\n".join(lines) + "\n"
    if json.loads(text) != plan:
        raise SystemExit("the plan's layout does not round-trip")
    Path(out_path).write_text(text)
    for label, entry in plan["files"].items():
        print(label, len(entry["controls"]), "controls:", " ".join(c["id"] for c in entry["controls"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
