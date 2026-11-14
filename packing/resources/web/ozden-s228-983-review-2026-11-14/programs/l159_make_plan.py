"""Lane L159's controls plan: state 20 controls and the outcome of each, in advance.

Clean-room code written for the stage 4 review of issue #983. It decides nothing. It
reads the check receipt and the plan facts and writes the plan, which is hashed before
l159_controls.py exists. "Contact" is a margin or clearance of exactly 0, and "past" is
1e-30 beyond it.

Usage: l159_make_plan.py CHECK.json PLAN_FACTS.json OUT_PLAN.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

EPS_TEXT = "-1/1000000000000000000000000000000"


def main(argv: list[str]) -> int:
    check_path, facts_path, out_path = (Path(a) for a in argv[1:4])
    check = json.loads(check_path.read_text(encoding="utf-8"))
    facts = json.loads(facts_path.read_text(encoding="utf-8"))
    contacts = check["wall_contacts"]
    digest = check["margin_list_sha256"]
    n = check["n"]
    left_bottom = [c for c in contacts if c[1] in ("left", "bottom")]
    swap = {"left": "bottom", "bottom": "left", "right": "top", "top": "right"}
    turn = {"left": "bottom", "bottom": "right", "right": "top", "top": "left"}
    s4 = facts["s4_chosen"]
    i4, j4 = s4["pair"]
    mover = s4["mover"]
    other = i4 if mover == j4 else j4

    def whole(**expect: object) -> dict[str, object]:
        base: dict[str, object] = {"disagreements": 0}
        base.update(expect)
        return base

    controls = [
        {
            "id": "G1",
            "change": f"square {n} given square 1's corners",
            "kind": "file",
            "stated": f"refused: exactly the pair (1, {n}) overlapping, margin -1, area 1; contacts unchanged",
            "expect": whole(verdict="REFUSE", overlapping=[[1, n]], overlap_exact=[[1, n, "-1", "1"]], touching=[], wall_contacts=contacts, wall_crossings=[], not_contained=[], senses="ccw"),
        },
        {
            "id": "G2",
            "change": "square 1 translated by (S, 0)",
            "kind": "file",
            "stated": "refused: square 1 across the right wall by both methods and not inside by B's area test; no pair overlapping or touching (square 1's left clearance is "
            + facts["square1_clearances"][0]
            + "); contacts unchanged",
            "expect": whole(verdict="REFUSE", overlapping=[], touching=[], wall_contacts=contacts, wall_crossings=[[1, "right"]], not_contained=[1], senses="ccw"),
        },
        {"id": "G3", "change": f"square {n}'s entry deleted, in the YAML and the twin", "kind": "reader", "stated": f"the reader refuses: {n - 1} entries", "expect": {"reason": f"{n - 1} entries for n = {n}"}},
        {"id": "G4", "change": f"square {n}'s id set to 1, in the YAML and the twin", "kind": "reader", "stated": "the reader refuses the id", "expect": {"reason": f"square {n}: id"}},
        {
            "id": "G5",
            "change": "square 1's third corner moved 1e-30 in x",
            "kind": "file",
            "stated": "refused: square 1 not a unit square by either method",
            "expect": {"verdict": "REFUSE", "not_unit_a": [1], "not_unit_b": [1]},
        },
        {
            "id": "G6",
            "change": "every square reflected in its own horizontal centre line (the rotation read the other way)",
            "kind": "file",
            "stated": "refused for overlapping pairs, the same classes by both methods; every square still a unit square inside, contacts unchanged, all listed clockwise",
            "expect": whole(verdict="REFUSE", overlapping="at_least_one", wall_contacts=contacts, wall_crossings=[], not_contained=[], senses="cw"),
        },
        {"id": "G7", "change": "the twin's side altered in its last digit (the YAML unchanged)", "kind": "reader", "stated": "the reader refuses: the twin differs", "expect": {"reason": "twin differs at $.witness.side"}},
        {
            "id": "G8",
            "change": "every corner transposed, (x, y) to (y, x)",
            "kind": "file",
            "stated": "accepted, contacts transposed, all listed clockwise, the SHA-256 of the exact margin list unchanged",
            "expect": whole(verdict="ACCEPT", overlapping=[], touching=[], wall_contacts=sorted([[i, swap[w]] for i, w in contacts]), wall_crossings=[], not_contained=[], senses="cw", margin_digest=digest),
        },
        {"id": "G9", "change": "the side written as 2p/2q, in the YAML and the twin", "kind": "reader", "stated": "the reader refuses: not in lowest terms", "expect": {"reason": "side: not in lowest terms"}},
        {
            "id": "G10",
            "change": "every square listed from its second corner",
            "kind": "file",
            "stated": "accepted, contacts and margin list unchanged, all counterclockwise",
            "expect": whole(verdict="ACCEPT", overlapping=[], touching=[], wall_contacts=contacts, wall_crossings=[], not_contained=[], senses="ccw", margin_digest=digest),
        },
        {
            "id": "G11",
            "change": "every square listed in the reverse cyclic order",
            "kind": "file",
            "stated": "accepted, contacts and margin list unchanged, all listed clockwise",
            "expect": whole(verdict="ACCEPT", overlapping=[], touching=[], wall_contacts=contacts, wall_crossings=[], not_contained=[], senses="cw", margin_digest=digest),
        },
        {
            "id": "G12",
            "change": "the whole packing turned a quarter counterclockwise about the box centre, (x, y) to (S - y, x)",
            "kind": "file",
            "stated": "accepted, contacts turned, all counterclockwise, margin list unchanged",
            "expect": whole(verdict="ACCEPT", overlapping=[], touching=[], wall_contacts=sorted([[i, turn[w]] for i, w in contacts]), wall_crossings=[], not_contained=[], senses="ccw", margin_digest=digest),
        },
        {
            "id": "S1a",
            "change": "the side lowered by 1/q, one unit of its own last place",
            "kind": "file",
            "side": "minus_1_over_q",
            "stated": "refused: exactly " + ", ".join(f"square {i} at the {w}" for i, w in facts["side_lowered_by_1_over_q_out"]) + " across",
            "expect": whole(verdict="REFUSE", overlapping=[], touching=[], wall_contacts=facts["contacts_after_1_over_q"], wall_crossings=facts["side_lowered_by_1_over_q_out"], not_contained=sorted({i for i, _ in facts["side_lowered_by_1_over_q_out"]}), senses="ccw", margin_digest=digest),
        },
        {
            "id": "S1b",
            "change": "the side lowered by 1e-30",
            "kind": "file",
            "side": "minus_eps",
            "stated": "the same, since no positive right or top clearance is below 1e-30 (the least is " + facts["least_positive_right_or_top_clearance"] + ")",
            "expect": whole(verdict="REFUSE", overlapping=[], touching=[], wall_contacts=facts["contacts_after_eps"], wall_crossings=facts["side_lowered_by_eps_out"], not_contained=sorted({i for i, _ in facts["side_lowered_by_eps_out"]}), senses="ccw", margin_digest=digest),
        },
        {
            "id": "S1c",
            "change": "the side set to its 12-place floor, " + facts["floor12"],
            "kind": "file",
            "side": "floor12",
            "stated": f"refused: exactly the {len(facts['floor12_out'])} right or top clearances below the drop of {facts['side_less_floor12']}",
            "expect": whole(verdict="REFUSE", overlapping=[], touching=[], wall_contacts=facts["contacts_after_floor12"], wall_crossings=facts["floor12_out"], not_contained=sorted({i for i, _ in facts["floor12_out"]}), senses="ccw", margin_digest=digest),
        },
        {
            "id": "S1d",
            "change": "the side set to its 12-place ceiling, the claim " + facts["ceil12"],
            "kind": "file",
            "side": "ceil12",
            "stated": "accepted, contacts at the left and bottom walls only",
            "expect": whole(verdict="ACCEPT", overlapping=[], touching=[], wall_contacts=facts["contacts_at_ceil12"], wall_crossings=[], not_contained=[], senses="ccw", margin_digest=digest),
        },
        {
            "id": "S4c",
            "change": f"square {mover} moved toward square {other} along their centre line to exact contact",
            "kind": "file",
            "move": {"pair": [i4, j4], "mover": mover, "to": "contact"},
            "stated": f"that pair alone touching by both, margin exactly 0, square {mover} inside; accepted",
            "expect": whole(verdict="ACCEPT", overlapping=[], touching=[[i4, j4]], touching_margin_zero=True, wall_contacts=contacts, wall_crossings=[], not_contained=[], senses="ccw"),
        },
        {
            "id": "S4p",
            "change": f"the same, 1e-30 past contact",
            "kind": "file",
            "move": {"pair": [i4, j4], "mover": mover, "to": "past"},
            "stated": "that pair alone overlapping by both, margin exactly -1e-30",
            "expect": whole(verdict="REFUSE", overlapping=[[i4, j4]], overlap_exact=[[i4, j4, EPS_TEXT, "positive"]], touching=[], wall_contacts=contacts, wall_crossings=[], not_contained=[], senses="ccw"),
        },
        {
            "id": "S5",
            "change": f"every pair below 1e-12 ({facts['pairs_below_1e-12']}) closed along its centre line, the second square moving (pair-level)",
            "kind": "pairs",
            "stated": "touching at contact by both, overlapping past, margins exactly 0 and -1e-30",
            "expect": {"pairs": facts["s5_pairs"], "closing_times_sha256": facts["s5_closing_times_sha256"], "contact_margin": "0", "past_margin": EPS_TEXT},
        },
        {
            "id": "S6",
            "change": "every square moved to its nearest wall by its clearance (square-level)",
            "kind": "squares",
            "stated": "contact at, across past, by both, clearance exactly 0 and -1e-30; inside at contact and not inside past by B's area test",
            "expect": {"nearest_walls": facts["nearest_walls"], "nearest_walls_sha256": facts["nearest_walls_sha256"], "contact_clearance": "0", "past_clearance": EPS_TEXT},
        },
    ]
    plan = {
        "program": "l159_make_plan.py",
        "certificate_sha256": check["certificate_sha256"],
        "original": {"wall_contacts": contacts, "margin_list_sha256": digest, "left_bottom_contacts": left_bottom},
        "controls": controls,
    }
    out_path.write_text(json.dumps(plan, indent=1) + "\n", encoding="utf-8")
    print(len(controls), "controls stated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
