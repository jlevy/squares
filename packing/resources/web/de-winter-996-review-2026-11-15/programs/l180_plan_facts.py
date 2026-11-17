"""Lane L180 plan facts: the exact facts the controls plan states its outcomes from.

Written for the blind stage 4 review of issue #996 as a clean-room implementation.
It imports nothing from this repository or the source, and reuses no code of any
earlier review. It runs neither method on a modified file: every number here comes
from the closed form of ``l180_geom`` (corner projections in fractions), a third
formulation apart from both methods, and from the check receipt.

Usage: l180_plan_facts.py JSON TWIN CHECK_RECEIPT OUT
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from fractions import Fraction as F
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l180_geom as G  # noqa: E402
import l180_reader as R  # noqa: E402
from l180_decide import fstr, sci  # noqa: E402
from l180_reader import Pose  # noqa: E402

TINY = F(1, 10**30)
WALLS = ("left", "bottom", "right", "top")


def all_margins(poses: list[Pose]) -> dict[tuple[int, int], F]:
    n = len(poses)
    return {(i + 1, j + 1): G.margin(poses[i], poses[j]) for i in range(n) for j in range(i + 1, n)}


def all_clear(poses: list[Pose], side: F) -> dict[tuple[int, str], F]:
    out: dict[tuple[int, str], F] = {}
    for i, p in enumerate(poses):
        for w, c in G.clearances(p, side).items():
            out[(i + 1, w)] = c
    return out


def digest_margins(m: dict[tuple[int, int], F]) -> str:
    return hashlib.sha256("".join(f"{i} {j} {fstr(v)}\n" for (i, j), v in sorted(m.items())).encode()).hexdigest()


def digest_clear(c: dict[tuple[int, str], F]) -> str:
    return hashlib.sha256("".join(f"{i} {w} {fstr(v)}\n" for (i, w), v in sorted(c.items())).encode()).hexdigest()


def classes(m: dict[tuple[int, int], F]) -> dict[str, list[list[int]]]:
    return {
        "overlapping": sorted([list(k) for k, v in m.items() if v < 0]),
        "touching": sorted([list(k) for k, v in m.items() if v == 0]),
    }


def wall_lists(c: dict[tuple[int, str], F]) -> dict[str, dict[str, list[int]]]:
    return {
        "contacts": {w: sorted(i for (i, ww), v in c.items() if ww == w and v == 0) for w in WALLS},
        "crossings": {w: sorted(i for (i, ww), v in c.items() if ww == w and v < 0) for w in WALLS},
    }


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(__doc__)
        return 2
    jpath, tpath, cpath, out = argv[1:]
    t0 = time.process_time()
    r = R.read_json(jpath)
    tw = R.read_twin(tpath)
    with open(cpath, encoding="utf-8") as fh:
        check = json.load(fh)
    dec = check["decision"]
    poses = list(r.poses)
    side = r.side
    n = r.n
    facts: dict[str, Any] = {"program": "l180_plan_facts.py", "lane": "L180", "n": n, "side": fstr(side)}

    margins = all_margins(poses)
    clear = all_clear(poses, side)
    facts["closed_form"] = {
        "margin_list_sha256": digest_margins(margins),
        "clearance_list_sha256": digest_clear(clear),
        "equals_method_a_margins": digest_margins(margins) == dec["margin_list_sha256"],
        "equals_method_a_clearances": digest_clear(clear) == dec["clearance_list_sha256"],
        "pair_classes": classes(margins),
        "walls": wall_lists(clear),
    }

    # G1: square n given square 1's pose.
    facts["G1"] = {
        "margins_1_j_positive_for_j_not_n": all(margins[(1, j)] > 0 for j in range(2, n)),
        "square_1_clearances": {w: fstr(clear[(1, w)]) for w in WALLS},
        "square_n_clearances": {w: fstr(clear[(n, w)]) for w in WALLS},
    }

    # G2: square 1 translated by (S, 0).
    p1 = poses[0]
    g2 = Pose(p1.x + side, p1.y, p1.c, p1.s)
    g2_margins = [G.margin(g2, poses[j]) for j in range(1, n)]
    g2_clear = G.clearances(g2, side)
    facts["G2"] = {
        "clearances": {w: fstr(v) for w, v in g2_clear.items()},
        "right_clearance_approx": sci(g2_clear["right"]),
        "least_margin_with_others": sci(min(g2_margins)),
        "left_clearance_before_positive": clear[(1, "left")] > 0,
    }

    # G5: rotation sense at a square on a wall.
    contacts = facts["closed_form"]["walls"]["contacts"]
    on_wall = {}
    for w in WALLS:
        for i in contacts[w]:
            on_wall.setdefault(i, []).append(w)
    g5: dict[str, Any] = {}
    for i in sorted(on_wall):
        if len(on_wall[i]) != 1:
            continue
        wall = on_wall[i][0]
        others = [clear[(i, w)] for w in WALLS if w != wall]
        near = min(v for (a, b), v in margins.items() if i in (a, b))
        if min(others) > F(1, 10**20) and near > F(1, 10**20):
            g5 = {"square": i, "wall": wall, "least_other_clearance": sci(min(others)), "least_margin": sci(near)}
            break
    if g5:
        i = g5["square"]
        p = poses[i - 1]
        for name, t in (("plus", TINY), ("minus", -TINY)):
            q = G.rotated(p, t)
            cl = G.clearances(q, side)
            ms = [G.margin(q, poses[j]) for j in range(n) if j != i - 1]
            g5[name] = {
                "wall_clearance": fstr(cl[g5["wall"]]),
                "wall_clearance_approx": sci(cl[g5["wall"]]),
                "other_clearances_positive": all(cl[w] > 0 for w in WALLS if w != g5["wall"]),
                "least_margin": sci(min(ms)),
            }
    facts["G5"] = g5

    # G6: every (c, s) read as (c, -s).
    refl = [Pose(p.x, p.y, p.c, -p.s) for p in poses]
    refl_m = all_margins(refl)
    refl_c = all_clear(refl, side)
    least = min(refl_m, key=lambda k: refl_m[k])
    facts["G6"] = {
        **classes(refl_m),
        "overlapping_count": sum(1 for v in refl_m.values() if v < 0),
        "least_margin": {"pair": list(least), "approx": sci(refl_m[least])},
        "clearance_list_sha256": digest_clear(refl_c),
        "clearances_unchanged": digest_clear(refl_c) == digest_clear(clear),
    }

    # S1: the side lowered or raised.
    rt = {k: v for k, v in clear.items() if k[1] in ("right", "top")}
    q = side.denominator
    least_rt = min(v for v in rt.values() if v > 0)
    claim = F(9994038857546, 10**12)
    floor12 = F(9994038857545, 10**12)
    facts["S1"] = {
        "side_denominator": str(q),
        "one_unit_of_last_place": fstr(F(1, q)),
        "right_top_below_one_unit": sorted([[i, w] for (i, w), v in rt.items() if v < F(1, q)]),
        "least_positive_right_top": {"exact": fstr(least_rt), "approx": sci(least_rt)},
        "right_top_at_least": sorted([[i, w] for (i, w), v in rt.items() if v == least_rt]),
        "right_top_below_1e-30": sorted([[i, w] for (i, w), v in rt.items() if v < TINY]),
        "right_top_contacts": sorted([[i, w] for (i, w), v in rt.items() if v == 0]),
        "claim": fstr(claim),
        "claim_minus_side": sci(claim - side),
        "claim_at_least_side": claim >= side,
        "floor12": fstr(floor12),
        "side_minus_floor12": sci(side - floor12),
        "right_top_below_side_minus_floor12": sorted([[i, w] for (i, w), v in rt.items() if v < side - floor12]),
        "next_right_top_after_least": sci(min(v for v in rt.values() if v > least_rt)),
    }

    # S4: the tightest pair whose closing move past contact is shorter than every other
    # margin and every clearance of the moved square.
    order = sorted(margins, key=lambda k: margins[k])
    s4: dict[str, Any] = {}
    tried = 0
    for i, j in order:
        for mover, other in ((j, i), (i, j)):
            tried += 1
            pm, po = poses[mover - 1], poses[other - 1]
            moved, t = G.close_pair(po, pm, -TINY)
            l2 = (moved.x - pm.x) ** 2 + (moved.y - pm.y) ** 2
            rest = [v for (a, b), v in margins.items() if mover in (a, b) and {a, b} != {i, j}]
            walls = [clear[(mover, w)] for w in WALLS]
            if all(v > 0 and l2 < v * v for v in rest) and all(v > 0 and l2 < v * v for v in walls):
                s4 = {
                    "pair": [i, j],
                    "moving": mover,
                    "toward": other,
                    "margin": sci(margins[(i, j)]),
                    "closing_time_past": fstr(t),
                    "move_length_squared_approx": sci(l2),
                    "next_margin_of_mover": sci(min(rest)),
                    "least_clearance_of_mover": sci(min(walls)),
                    "orders_tried": tried,
                }
                break
        if s4:
            break
    facts["S4"] = s4

    # S5: every pair closed along its centre line, j toward i, to contact and past.
    lines = []
    for i in range(n):
        for j in range(i + 1, n):
            t_at = G.closing_time(poses[i], poses[j], F(0))
            t_past = G.closing_time(poses[i], poses[j], -TINY)
            lines.append(f"{i + 1} {j + 1} {fstr(t_at)} {fstr(t_past)}\n")
    facts["S5"] = {"pairs": len(lines), "closing_times_sha256": hashlib.sha256("".join(lines).encode()).hexdigest()}

    # S6: every square to its nearest wall.
    nearest: dict[str, int] = dict.fromkeys(WALLS, 0)
    already = 0
    for i in range(1, n + 1):
        w = min(WALLS, key=lambda ww: (clear[(i, ww)], WALLS.index(ww)))
        nearest[w] += 1
        already += clear[(i, w)] == 0
    facts["S6"] = {"nearest_wall_counts": nearest, "squares_already_touching_their_nearest_wall": already}

    facts["twin"] = {"n": tw.n, "side_equal": tw.side == r.side, "agree": R.compare_twin(r, tw)["agree"]}
    facts["cpu_seconds"] = round(time.process_time() - t0, 2)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(facts, fh, indent=1)
        fh.write("\n")
    print(
        f"closed form equals A: margins {facts['closed_form']['equals_method_a_margins']}, "
        f"clearances {facts['closed_form']['equals_method_a_clearances']}; G5 {g5.get('square')} {g5.get('wall')}; "
        f"G6 {facts['G6']['overlapping_count']} overlapping; S1 below 1/q {len(facts['S1']['right_top_below_one_unit'])}; "
        f"S4 {s4.get('pair')} moving {s4.get('moving')}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
