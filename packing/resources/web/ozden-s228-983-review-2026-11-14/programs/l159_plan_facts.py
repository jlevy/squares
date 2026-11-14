"""Lane L159's plan facts: the exact facts the controls plan states its outcomes from.

Clean-room code written for the stage 4 review of issue #983. It decides no modified
file. From the certificate (through the reader) and the check receipt it computes, with
Fractions from the corners and the closed form of l159_geom:

- every square's wall clearances and its nearest wall;
- the side's 12-place floor and ceiling, and which right or top clearances fall below
  each side reduction the plan uses;
- for the closest pairs, the move along the centre line to contact and 1e-30 past it,
  and the closed-form margin of the moved square against every other square and its
  clearances after each move, to choose a control whose pair alone changes class;
- for every pair below 1e-12, the closing times, the binding normals and the closed-form
  margin at both times;
- square 1's clearances, for the translated-square control;
- the claim as the issue prints it.

Usage: l159_plan_facts.py CERT.yaml TWIN.json CHECK.json ISSUE.json OUT.json
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l159_geom as geom  # noqa: E402
from l159_reader import read_paths  # noqa: E402

EPS = Fraction(1, 10**30)
WALLS = ("left", "bottom", "right", "top")


def clearances(corners: tuple, side: Fraction) -> list[Fraction]:
    pts = geom.as_fraction_points(corners)
    xs = [x for x, _ in pts]
    ys = [y for _, y in pts]
    return [min(xs), min(ys), side - max(xs), side - max(ys)]


def frac_text(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def below(clear: list[list[Fraction]], drop: Fraction) -> list[list[object]]:
    """Squares whose right or top clearance is below a side reduction."""
    out = []
    for i, row in enumerate(clear, start=1):
        for k in (2, 3):
            if row[k] < drop:
                out.append([i, WALLS[k]])
    return out


def main(argv: list[str]) -> int:
    cert, twin, check_path, issue_path, out_path = (Path(a) for a in argv[1:6])
    w = read_paths(cert, twin)
    check = json.loads(check_path.read_text(encoding="utf-8"))
    issue = json.loads(issue_path.read_text(encoding="utf-8"))
    side = Fraction(*w.side)
    n = w.n
    frames = [geom.centre_frame(c) for c in w.squares]
    clear = [clearances(c, side) for c in w.squares]
    facts: dict[str, object] = {"program": "l159_plan_facts.py", "n": n}

    # The claim and the side's 12-place prints.
    claim_match = re.search(r"s\(228\) ≤ ([0-9.]+)", issue["title"])
    claim = claim_match.group(1) if claim_match else None
    floor12 = Fraction(geom.floor_places(side, 12))
    ceil12 = Fraction(geom.ceil_places(side, 12))
    facts["claim_from_issue_title"] = claim
    facts["floor12"] = geom.floor_places(side, 12)
    facts["ceil12"] = geom.ceil_places(side, 12)
    facts["claim_is_ceil12"] = claim == geom.ceil_places(side, 12)
    facts["side_less_floor12"] = geom.sci(side - floor12, 6)
    facts["ceil12_less_side"] = geom.sci(ceil12 - side, 6)

    # Side reductions.
    q = w.side[1]
    facts["side_lowered_by_1_over_q_out"] = below(clear, Fraction(1, q))
    facts["side_lowered_by_eps_out"] = below(clear, EPS)
    facts["floor12_out"] = below(clear, side - floor12)
    for name, drop in (("1_over_q", Fraction(1, q)), ("eps", EPS), ("floor12", side - floor12)):
        facts[f"contacts_after_{name}"] = [
            [i, WALLS[k]]
            for i, row in enumerate(clear, start=1)
            for k in range(4)
            if (row[k] if k < 2 else row[k] - drop) == 0
        ]
    positive_rt = [v for row in clear for v in row[2:] if v > 0]
    facts["least_positive_right_or_top_clearance"] = geom.sci(min(positive_rt), 6)
    facts["contacts"] = [[i, WALLS[k]] for i, row in enumerate(clear, start=1) for k in range(4) if row[k] == 0]
    facts["contacts_at_ceil12"] = [
        [i, WALLS[k]]
        for i, row in enumerate(clear, start=1)
        for k in range(4)
        if (row[k] if k < 2 else row[k] + ceil12 - side) == 0
    ]
    facts["ceil12_crossings"] = [
        [i, WALLS[k]] for i, row in enumerate(clear, start=1) for k in (2, 3) if row[k] + ceil12 - side < 0
    ]

    # Square 1, for the translated-square control.
    facts["square1_clearances"] = [geom.sci(v, 6) for v in clear[0]]
    facts["square1_left_clearance_positive"] = clear[0][0] > 0

    # Nearest walls, for the square-level wall control.
    nearest = []
    for i, row in enumerate(clear, start=1):
        k = min(range(4), key=lambda j: (row[j], j))
        nearest.append([i, WALLS[k], frac_text(row[k])])
    facts["nearest_wall_counts"] = {wall: sum(1 for r in nearest if r[1] == wall) for wall in WALLS}
    facts["nearest_walls"] = [[i, wall] for i, wall, _ in nearest]
    facts["nearest_walls_sha256"] = hashlib.sha256(
        "".join(f"{i} {wall} {v}\n" for i, wall, v in nearest).encode()
    ).hexdigest()

    # Pairs below 1e-12: closed form, closing times, binding normals.
    near = [(int(i), int(j)) for i, j, _ in check["near_pairs"]]
    closed: dict[tuple[int, int], Fraction] = {}
    for i, j in near:
        ci, ui, wi = frames[i - 1]
        cj, uj, wj = frames[j - 1]
        closed[(i, j)] = geom.closed_margin(ci, ui, wi, cj, uj, wj)
    tight = sorted((m, k) for k, m in closed.items() if m < Fraction(1, 10**12))
    facts["pairs_below_1e-12"] = len(tight)
    least = tight[0][0]
    facts["least_closed_margin"] = frac_text(least)
    facts["least_closed_margin_equals_receipt"] = frac_text(least) == check["least_margin"]["exact"]
    facts["pairs_at_least_margin"] = [list(k) for m, k in tight if m == least]
    lines = []
    binding_counts: dict[int, int] = {}
    s5 = []
    for m, (i, j) in tight:
        ci, ui, wi = frames[i - 1]
        cj, uj, wj = frames[j - 1]
        t0, t1, binding = geom.closing(ci, ui, wi, cj, uj, wj, EPS)
        binding_counts[binding] = binding_counts.get(binding, 0) + 1
        at0 = geom.closed_margin(ci, ui, wi, (cj[0] + t0 * (ci[0] - cj[0]), cj[1] + t0 * (ci[1] - cj[1])), uj, wj)
        at1 = geom.closed_margin(ci, ui, wi, (cj[0] + t1 * (ci[0] - cj[0]), cj[1] + t1 * (ci[1] - cj[1])), uj, wj)
        s5.append([i, j, binding, at0 == 0, at1 == -EPS])
        lines.append(f"{i} {j} {frac_text(t0)} {frac_text(t1)}\n")
    facts["s5_binding_normal_counts"] = {str(k): v for k, v in sorted(binding_counts.items())}
    facts["s5_all_closed_form_at_contact_zero"] = all(r[3] for r in s5)
    facts["s5_all_closed_form_past_minus_eps"] = all(r[4] for r in s5)
    facts["s5_pairs"] = [[i, j] for i, j, *_ in s5]
    facts["s5_closing_times_sha256"] = hashlib.sha256("".join(lines).encode()).hexdigest()

    # S4: a closest pair and a mover whose other margins and clearances stay positive
    # after the move past contact, decided on the closed form.
    def after_move(i: int, j: int, mover: int) -> dict[str, object]:
        other = i if mover == j else j
        co, uo, wo = frames[other - 1]
        cm, um, wm = frames[mover - 1]
        t0, t1, binding = geom.closing(co, uo, wo, cm, um, wm, EPS)
        result: dict[str, object] = {"pair": [i, j], "mover": mover, "binding_normals": binding}
        d2 = (co[0] - cm[0]) ** 2 + (co[1] - cm[1]) ** 2
        rest = []
        for k in range(1, n + 1):
            if k in (mover, other):
                continue
            ck, uk, wk = frames[k - 1]
            rest.append((geom.closed_margin(ck, uk, wk, cm, um, wm), k))
        next_margin, next_k = min(rest)
        result["move_length_past_squared_sci"] = geom.sci(t1 * t1 * d2, 6)
        result["next_margin"] = [next_k, geom.sci(next_margin, 6)]
        result["move_shorter_than_next_margin"] = t1 * t1 * d2 < next_margin * next_margin
        least_clear = min(clear[mover - 1])
        result["least_clearance"] = geom.sci(least_clear, 6)
        result["move_shorter_than_clearances"] = t1 * t1 * d2 < least_clear * least_clear
        ok = True
        for t, tag in ((t0, "contact"), (t1, "past")):
            cnew = (cm[0] + t * (co[0] - cm[0]), cm[1] + t * (co[1] - cm[1]))
            margins = []
            for k in range(1, n + 1):
                if k in (mover, other):
                    continue
                ck, uk, wk = frames[k - 1]
                margins.append(geom.closed_margin(ck, uk, wk, cnew, um, wm))
            moved = geom.translate(w.squares[mover - 1], (cnew[0] - cm[0], cnew[1] - cm[1]))
            cl = clearances(moved, side)
            pair_margin = geom.closed_margin(co, uo, wo, cnew, um, wm)
            result[f"{tag}_pair_margin"] = frac_text(pair_margin)
            result[f"{tag}_least_other_margin"] = geom.sci(min(margins), 6)
            result[f"{tag}_least_clearance"] = geom.sci(min(cl), 6)
            result[f"{tag}_contacts"] = [WALLS[k] for k in range(4) if cl[k] == 0]
            ok = ok and min(margins) > 0 and min(cl) > 0
        result["only_this_pair_changes"] = ok
        return result

    tried = []
    chosen = None
    for m, (i, j) in tight:
        for mover in (j, i):
            r = after_move(i, j, mover)
            tried.append(r)
            if r["only_this_pair_changes"]:
                chosen = r
                break
        if chosen:
            break
    facts["s4_tried"] = tried
    facts["s4_chosen"] = chosen
    out_path.write_text(json.dumps(facts, indent=1) + "\n", encoding="utf-8")
    print(
        "claim", claim, "ceil12", facts["ceil12"], "| S1a", facts["side_lowered_by_1_over_q_out"],
        "| S1c", len(facts["floor12_out"]), "| S4", chosen and chosen["pair"], chosen and chosen["mover"],
        "| S5", len(tight), facts["s5_binding_normal_counts"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
