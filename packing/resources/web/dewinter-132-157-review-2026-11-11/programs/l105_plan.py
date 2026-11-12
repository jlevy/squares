"""Lane L105's controls plan: exact facts of the unmodified files, then the
stated outcome of every control. Decides no modified file.

Usage: python -I -B l105_plan.py SOURCE_DIR OUT_DIR PLAN_JSON

Reads each folder's JSON through the frozen reader, computes with the frozen
method A on the *unmodified* squares only (clearances, near-pair margins), and with
`l105_geom` the exact closing and wall moves. Writes OUT_DIR/plan-facts-nNNN.json
and the plan PLAN_JSON, whose outcomes `l105_controls.py` (written afterwards) must
meet exactly.
"""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import l105_check as K  # noqa: E402
import l105_geom as G  # noqa: E402
import l105_reader as R  # noqa: E402
import l105_sat as A  # noqa: E402

EPS = F(1, 10**30)
NEAR = F(1, 10**50)
WALLS = ("left", "bottom", "right", "top")
TRANSPOSE_WALL = {"left": "bottom", "bottom": "left", "right": "top", "top": "right"}


def floor_places(v: F, k: int) -> F:
    return F((v.numerator * 10**k) // v.denominator, 10**k)


def ceil_places(v: F, k: int) -> F:
    return F(-((-v.numerator * 10**k) // v.denominator), 10**k)


def wall_set(rows: list[tuple[int, str]]) -> list[list[Any]]:
    return sorted([k, w] for k, w in rows)


def facts_and_plan(src: Path, n: int) -> tuple[dict[str, Any], dict[str, Any]]:
    pk = R.read_json(src / f"n{n}" / f"n{n}_exact.json")
    S = A.frac(pk["side"])
    q = S.denominator
    sqs = pk["squares"]
    sa = [A.build(s) for s in sqs]
    clr = [A.clearances(x, S) for x in sa]
    base_contacts = [(k + 1, WALLS[w]) for k in range(n) for w in range(4) if clr[k][w] == 0]
    margins: dict[tuple[int, int], F] = {}
    for i in range(n):
        for j in range(i + 1, n):
            margins[(i + 1, j + 1)] = A.margin(sa[i], sa[j])[0]
    base_sha = hashlib.sha256(
        "\n".join(f"{i} {j} {K.frac_text(m)}" for (i, j), m in margins.items()).encode()
    ).hexdigest()
    near = sorted(((p, m) for p, m in margins.items() if m < NEAR), key=lambda t: t[1])
    floor12, ceil12 = floor_places(S, 12), ceil_places(S, 12)

    def side_case(new_side: F) -> dict[str, Any]:
        drop = S - new_side
        outside, contacts = [], []
        for k in range(n):
            for w in range(4):
                c = clr[k][w] - (drop if WALLS[w] in ("right", "top") else 0)
                if c < 0:
                    outside.append((k + 1, WALLS[w]))
                elif c == 0:
                    contacts.append((k + 1, WALLS[w]))
        return {
            "side": K.frac_text(new_side),
            "drop_sci": K.sci(drop),
            "expect": {
                "verdict": "REFUSE" if outside else "ACCEPT",
                "walls_outside": wall_set(outside),
                "wall_contacts": wall_set(contacts),
                "overlapping_pairs": [],
                "touching_pairs": [],
            },
        }

    # S3: the tightest near pair whose closing move to contact is shorter than every
    # other margin and every wall clearance of the moved square (exactly, by squares).
    s3: dict[str, Any] | None = None
    for (i, j), m in near:
        for mover, other in ((j, i), (i, j)):
            moved = G.close_pair(sqs[other - 1], sqs[mover - 1], F(0))
            w = (G.fr(moved[0]) - sa[mover - 1].x, G.fr(moved[1]) - sa[mover - 1].y)
            w2 = w[0] ** 2 + w[1] ** 2
            others = [mm for (a, b), mm in margins.items() if mover in (a, b) and {a, b} != {i, j}]
            ok = all(w2 < mm * mm for mm in others) and all(c > 0 and w2 < c * c for c in clr[mover - 1])
            if ok:
                s3 = {
                    "pair": [i, j],
                    "moved": mover,
                    "margin_sci": K.sci(m, 12),
                    "move_length_sq_sci": K.sci(w2, 6),
                    "least_other_margin_sci": K.sci(min(others), 6),
                    "least_wall_clearance_sci": K.sci(min(clr[mover - 1]), 6),
                    "expect": {
                        "verdict": "ACCEPT",
                        "touching_pairs": [sorted([i, j])],
                        "overlapping_pairs": [],
                        "walls_outside": [],
                    },
                }
                break
        if s3:
            break

    nearest = []
    for k in range(n):
        wi = min(range(4), key=lambda w: clr[k][w])
        nearest.append({"square": k + 1, "wall": WALLS[wi], "clearance_sci": K.sci(clr[k][wi])})

    facts = {
        "program": "l105_plan.py",
        "n": n,
        "side": K.frac_text(S),
        "side_denominator_digits": len(str(q)),
        "side_sci": K.sci(S, 20),
        "floor12": str(floor12),
        "ceil12": str(ceil12),
        "base_wall_contacts": wall_set(base_contacts),
        "base_margin_list_sha256": base_sha,
        "near_threshold": "1e-50",
        "near_pairs": [{"pair": list(p), "sci": K.sci(m, 12)} for p, m in near],
        "nearest_walls": nearest,
        "right_top_clearances_below_1e-3": sorted(
            [[k + 1, WALLS[w], K.sci(clr[k][w], 8)] for k in range(n) for w in (2, 3) if clr[k][w] < F(1, 1000)],
            key=lambda r: (r[0], r[1]),
        ),
    }
    plan: dict[str, Any] = {
        "n": n,
        "G1_duplicate": {
            "what": f"square {n} given square 1's four scalars; whole file decided by both methods",
            "expect": {
                "verdict": "REFUSE",
                "overlapping_pairs": [[1, n]],
                "touching_pairs": [],
                "walls_outside": [],
                "margin_1n": "-1",
                "area_1n": "1",
                "margins_k_n_equal_base_k_1": True,
            },
        },
        "G2_translated": {
            "what": "square 1 translated by (side, 0); whole file",
            "expect": {"verdict": "REFUSE", "walls_outside": [[1, "right"]], "overlapping_pairs": [], "touching_pairs": []},
        },
        "G3_deleted": {
            "what": f"square {n}'s entry deleted from the JSON and from the YAML",
            "expect": {"json_reader": "refuses: entries", "yaml_reader": "refuses: entries"},
        },
        "G4_id": {"what": "YAML square 2's id set to 1", "expect": {"yaml_reader": "refuses: order"}},
        "G5_not_unit": {
            "what": "square 1's cos increased by 1e-30; whole file",
            "expect": {"verdict": "REFUSE", "unit_squares_a": n - 1, "unit_squares_b": n - 1},
        },
        "G6_rotation_reversed": {
            "what": "every square's sin negated (the rotation read the other way); whole file",
            "expect": {
                "verdict": "REFUSE",
                "overlapping_pairs_at_least": 1,
                "pair_class_disagreement_count": 0,
                "unit_squares_a": n,
                "unit_squares_b": n,
                "walls_outside": [],
                "wall_contacts": wall_set(base_contacts),
                "clearances_equal_base": True,
            },
        },
        "G7_twin_side": {
            "what": "the YAML side's last numerator digit changed; the JSON unchanged",
            "expect": {"same_packing": False, "side_equal": False, "scalar_difference_count": 0},
        },
        "G7b_twin_scalar": {
            "what": "the YAML square 2's centre x last numerator digit changed",
            "expect": {"same_packing": False, "side_equal": True, "scalar_difference_count": 1},
        },
        "G8_transposed": {
            "what": "every square (x, y, c, s) -> (y, x, s, c); whole file",
            "expect": {
                "verdict": "ACCEPT",
                "wall_contacts": wall_set([(k, TRANSPOSE_WALL[w]) for k, w in base_contacts]),
                "touching_pairs": [],
                "overlapping_pairs": [],
                "margin_list_sha256": base_sha,
                "clearances_transposed_exactly": True,
            },
        },
        "S1a_side_minus_1_over_q": side_case(S - F(1, q)),
        "S1b_side_minus_1e-30": side_case(S - EPS),
        "S1c_side_floor12": side_case(floor12),
        "S1d_side_ceil12": side_case(ceil12),
        "S3_tightest_pair_contact": s3
        or {"what": "no near pair's move is shorter than the moved square's other margins", "expect": None},
        "S4_near_pairs": {
            "what": "every pair with margin below 1e-50 closed along its centre line (the second square moved): pair-level, both methods",
            "pairs": len(near),
            "expect": {"contact": "A margin exactly 0, B contact", "past": "A margin exactly -1e-30, B overlap"},
        },
        "S5_walls": {
            "what": "every square moved normal to its nearest wall by its clearance, and 1e-30 further: square-level, both methods",
            "squares": n,
            "expect": {
                "contact": "A clearance exactly 0, B contact, B clearance equal",
                "past": "A clearance exactly -1e-30, B outside, B clearance equal",
            },
        },
    }
    return facts, plan


def main() -> None:
    sys.set_int_max_str_digits(0)
    src, out, planp = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    plans = {}
    for n in (132, 157):
        facts, plan = facts_and_plan(src, n)
        (out / f"plan-facts-n{n}.json").write_text(json.dumps(facts, indent=1) + "\n")
        plans[str(n)] = plan
        s3 = plan["S3_tightest_pair_contact"]
        print(
            f"n={n} near={len(facts['near_pairs'])} floor12={facts['floor12']} ceil12={facts['ceil12']} "
            f"S1a out={len(plan['S1a_side_minus_1_over_q']['expect']['walls_outside'])} "
            f"S1b out={len(plan['S1b_side_minus_1e-30']['expect']['walls_outside'])} "
            f"S1c out={len(plan['S1c_side_floor12']['expect']['walls_outside'])} "
            f"S1d={plan['S1d_side_ceil12']['expect']['verdict']} S3={s3.get('pair')} moved={s3.get('moved')}"
        )
    me = {p: hashlib.sha256((HERE / p).read_bytes()).hexdigest() for p in ("l105_plan.py", "l105_geom.py", "l105_reader.py", "l105_sat.py", "l105_check.py")}
    planp.write_text(json.dumps({"program_sha256": me, "plans": plans}, indent=1) + "\n")


if __name__ == "__main__":
    main()
