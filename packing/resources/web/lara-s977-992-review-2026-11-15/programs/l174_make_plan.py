"""Lane L174: state the controls and their outcomes before any construction is decided.

Usage: ``python -I -B l174_make_plan.py PLAN.json FACTS.json``

Decides nothing geometric.  It counts, from the indices alone, the contacts the
construction argument implies, and states each control's outcome from them:

* in a k x k diamond array, 2k(k-1) edge-sharing and 2(k-1)^2 corner-sharing pairs;
* in a staircase of row widths w_r, the horizontal, vertical, diagonal and
  anti-diagonal neighbours of the grid cells;
* the corner-on-edge contacts with the diamond: a bottom-left cell (c, r) whose
  upper-right corner (c+1, r+1) lies on the diamond's lower-left edge line x + y = 17,
  that is c + r = 15.  Its edge coordinate, measured from the left vertex
  (C - R, C) along (1, -1)/sqrt 2, is t = (15/2 - r) sqrt 2 + 21/2, irrational, so the
  corner lies inside exactly one diamond square's edge, square D(0, 20 - floor t);
* for the 22 x 22 diamond (control C5) the edge line is x + y = 17 - 1/sqrt 2, the
  contact cell's corner region is a triangle whose base on that line has length 1 and
  edge coordinates [t - 1, t] with t = (15/2 - r) sqrt 2 + 23/2, so it overlaps exactly
  the two squares D(0, 21 - floor t) and D(0, 22 - floor t);
* the images of all of these under the quarter turns about the centre, which map the
  array index (i, j) to (k-1-j, i).
"""

from __future__ import annotations

import json
import sys
from decimal import Decimal, getcontext
from pathlib import Path

WIDTHS = (15, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2)
CORNERS = ("BL", "BR", "TR", "TL")

getcontext().prec = 60
ROOT2 = Decimal(2).sqrt()


def diamond_adjacency(k: int) -> dict[str, int]:
    return {"edge": 2 * k * (k - 1), "corner": 2 * (k - 1) ** 2}


def stair_adjacency(w: tuple[int, ...]) -> dict[str, int]:
    rows = len(w)
    horizontal = sum(x - 1 for x in w)
    vertical = sum(min(w[r], w[r + 1]) for r in range(rows - 1))
    diagonal = sum(max(0, min(w[r], w[r + 1] - 1)) for r in range(rows - 1))
    anti = sum(max(0, min(w[r] - 1, w[r + 1])) for r in range(rows - 1))
    return {"horizontal": horizontal, "vertical": vertical, "diagonal": diagonal, "anti": anti}


def contact_cells(w: tuple[int, ...]) -> list[tuple[int, int]]:
    return [(c, r) for r, x in enumerate(w) for c in range(x) if c + r + 2 == 17]


def rot(k: int, ij: tuple[int, int], quarter: int) -> tuple[int, int]:
    i, j = ij
    for _ in range(quarter):
        i, j = k - 1 - j, i
    return (i, j)


def floor_t(r: int, const: Decimal) -> int:
    t = (Decimal(15) / 2 - r) * ROOT2 + const
    m = int(t.to_integral_value(rounding="ROUND_FLOOR"))
    frac = t - m
    if frac < Decimal("1e-6") or frac > 1 - Decimal("1e-6"):
        msg = f"t too close to an integer at r={r}"
        raise ArithmeticError(msg)
    return m


def k0_contacts() -> list[list[str]]:
    out: list[list[str]] = []
    for q, corner in enumerate(CORNERS):
        for c, r in contact_cells(WIDTHS):
            m = floor_t(r, Decimal(21) / 2)
            i, j = rot(21, (0, 20 - m), q)
            out.append([f"D({i},{j})", f"{corner}({c},{r})"])
    return out


def c5_overlaps() -> list[list[str]]:
    out: list[list[str]] = []
    for q, corner in enumerate(CORNERS):
        for c, r in contact_cells(WIDTHS):
            m = floor_t(r, Decimal(23) / 2)
            for jj in (21 - m, 22 - m):
                i, j = rot(22, (0, jj), q)
                out.append([f"D({i},{j})", f"{corner}({c},{r})"])
    return out


def main(argv: list[str]) -> int:
    d21 = diamond_adjacency(21)
    d22 = diamond_adjacency(22)
    st = stair_adjacency(WIDTHS)
    contacts = contact_cells(WIDTHS)
    per_stair = sum(st.values())
    n_stair = sum(WIDTHS)
    touch_k0 = sum(d21.values()) + 4 * per_stair + 4 * len(contacts)
    touch_no_contact = sum(d21.values()) + 4 * per_stair
    touch_c5 = sum(d22.values()) + 4 * per_stair
    wall_cells_left = sum(1 for x in WIDTHS if x > 0)  # cells with c = 0, one per row
    wall_cells_bottom = WIDTHS[0]  # cells with r = 0
    wall_pairs = 4 * (wall_cells_left + wall_cells_bottom)
    wall_squares = 4 * (wall_cells_left + wall_cells_bottom - 1)
    # C1: the right and top walls carry BR's and TR's bottom-row images (right) and TR's and
    # TL's left-column images (top); TR's corner cell is at both.
    half_pairs = 2 * wall_cells_bottom + 2 * wall_cells_left
    half_squares = half_pairs - 1
    n0 = 21 * 21 + 4 * n_stair
    n5 = 22 * 22 + 4 * n_stair
    contacts_k0 = k0_contacts()
    over_c5 = c5_overlaps()

    facts = {
        "diamond_21_adjacency": d21,
        "diamond_22_adjacency": d22,
        "staircase_cells": n_stair,
        "staircase_adjacency": st,
        "staircase_adjacent_pairs": per_stair,
        "contact_cells_bottom_left": [f"BL({c},{r})" for c, r in contacts],
        "contact_t_values_K0": {
            f"r={r}": f"(15/2-{r}) sqrt2 + 21/2 = {(Decimal(15) / 2 - r) * ROOT2 + Decimal(21) / 2:.12f}"
            for _, r in contacts
        },
        "contacts_K0": contacts_k0,
        "overlaps_C5": over_c5,
        "wall_contact_pairs": wall_pairs,
        "wall_contact_squares": wall_squares,
        "touching_K0": touch_k0,
        "touching_without_diamond_staircase_contacts": touch_no_contact,
        "touching_C5": touch_c5,
        "n_K0": n0,
        "n_C5": n5,
    }

    def pairs_total(n: int) -> int:
        return n * (n - 1) // 2

    plan = {
        "stated_by": "lane L174 (bold-ritchie-l174), before any construction file was decided",
        "delta": "1/1000000",
        "rule": (
            "Each control is decided by both methods (l174_decide.py) over every square, wall "
            "and pair. 'As stated' means every listed quantity equals the stated value and the "
            "two methods agree on every pair class, wall class and unit test."
        ),
        "controls": {
            "K0": {
                "what": "the construction as stated: side 17 + 21/sqrt 2",
                "n": n0,
                "angles": {"0": 4 * n_stair, "45": 441},
                "apart": pairs_total(n0) - touch_k0,
                "touching": touch_k0,
                "overlapping": 0,
                "overlapping_pairs": [],
                "wall_touching": wall_pairs,
                "wall_touching_squares": wall_squares,
                "wall_crossing": 0,
                "non_unit": 0,
                "verdict": "packing",
            },
            "C1": {
                "what": "K0's squares in the container of side L - 1e-6",
                "n": n0,
                "touching": touch_k0,
                "overlapping": 0,
                "wall_crossing": half_pairs,
                "wall_crossing_squares": half_squares,
                "wall_crossing_walls": "right and top only (BR, TR at right; TR, TL at top)",
                "wall_touching": half_pairs,
                "wall_touching_squares": half_squares,
                "non_unit": 0,
                "verdict": "not a packing",
            },
            "C2": {
                "what": "the construction rebuilt at side L - 1e-6",
                "n": n0,
                "touching": touch_k0 - len(contacts_k0),
                "overlapping": len(contacts_k0),
                "overlapping_pairs": contacts_k0,
                "wall_touching": wall_pairs,
                "wall_crossing": 0,
                "non_unit": 0,
                "verdict": "not a packing",
            },
            "C3": {
                "what": "K0 with BL(14,1) moved by (+1e-6, 0)",
                "n": n0,
                "touching": touch_k0 - 4,
                "touching_note": (
                    "BL(14,1) loses BL(13,1), BL(13,0), BL(13,2) and its diamond contact "
                    "(now overlapping); keeps BL(14,0)"
                ),
                "overlapping": 1,
                "overlapping_pairs": [p for p in contacts_k0 if p[1] == "BL(14,1)"],
                "wall_touching": wall_pairs,
                "wall_crossing": 0,
                "verdict": "not a packing",
            },
            "C4": {
                "what": "K0 with D(10,10) moved by (+1e-6, 0)",
                "n": n0,
                "touching": touch_k0 - 8,
                "touching_note": "D(10,10) loses all 8 neighbours as contacts: 5 apart, 3 overlapping",
                "overlapping": 3,
                "overlapping_pairs": [
                    ["D(10,9)", "D(10,10)"],
                    ["D(10,10)", "D(11,9)"],
                    ["D(10,10)", "D(11,10)"],
                ],
                "wall_touching": wall_pairs,
                "wall_crossing": 0,
                "verdict": "not a packing",
            },
            "C5": {
                "what": "the diamond enlarged to 22 x 22 at the same side",
                "n": n5,
                "angles": {"0": 4 * n_stair, "45": 484},
                "touching": touch_c5,
                "overlapping": len(over_c5),
                "overlapping_pairs": over_c5,
                "wall_touching": wall_pairs,
                "wall_crossing": 0,
                "non_unit": 0,
                "verdict": "not a packing",
            },
            "C6": {
                "what": "the diamond enlarged by 1 + 1e-6 about the centre",
                "n": n0,
                "touching": touch_k0 - len(contacts_k0),
                "overlapping": len(contacts_k0),
                "overlapping_pairs": contacts_k0,
                "wall_touching": wall_pairs,
                "wall_crossing": 0,
                "non_unit": 441,
                "verdict": "not a packing",
            },
            "C7": {
                "what": "the construction rebuilt at the CSV's side 637/20 = 31.85",
                "n": n0,
                "touching": touch_no_contact,
                "overlapping": 0,
                "wall_touching": wall_pairs,
                "wall_crossing": 0,
                "non_unit": 0,
                "verdict": "packing",
            },
        },
    }
    Path(argv[1]).write_text(json.dumps(plan, indent=1) + "\n", encoding="utf-8")
    Path(argv[2]).write_text(json.dumps(facts, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: facts[k] for k in ("touching_K0", "touching_C5", "n_K0", "n_C5", "wall_contact_pairs")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
