"""Lane L182: #997's certificate against #996's, square by square, wall by wall, pair by pair.

Written for the addendum to lane L180's blind stage 4 review of issue #996, after the
controls on #997's certificate were run. It decides nothing about the bound. Both files
are read by ``l180_reader`` and both check receipts are those of ``l180_check.py``,
unchanged. Moves, turns, contacts and margins are exact (fractions); the degrees and the
lengths printed beside them are binary64 and descriptive only.

Square k of one file is compared with square k of the other. The program first checks
exactly that this is the nearest-centre pairing: every square's nearest centre in the
other file has its own number.

Usage: l182_compare.py JSON_997 JSON_996 CHECK_997 CHECK_996 OUT
"""

from __future__ import annotations

import json
import math
import os
import sys
from collections import Counter
from fractions import Fraction as F
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
L180 = os.path.normpath(os.path.join(HERE, "..", "..", "programs"))
sys.path.insert(0, L180)

import l180_reader as R  # noqa: E402
from l180_decide import fstr, sci  # noqa: E402
from l180_reader import Pose  # noqa: E402

WALLS = ("left", "bottom", "right", "top")


def tilt(p: Pose) -> float:
    a = math.degrees(math.atan2(float(p.s), float(p.c)))
    while a > 45:
        a -= 90
    while a <= -45:
        a += 90
    return a


def relative(p: Pose, q: Pose) -> tuple[F, F]:
    """The exact rotation taking q's edge direction to p's, reduced to (-45, 45] degrees."""
    c, s = p.c * q.c + p.s * q.s, p.s * q.c - p.c * q.s
    best = (c, s)
    for _ in range(3):
        c, s = -s, c
        if c > best[0]:
            best = (c, s)
    return best


def corners_on_wall(p: Pose, wall: str, side: F) -> int:
    cs = R.json_corners(p)
    if wall in ("left", "right"):
        vals = [x for x, _ in cs]
    else:
        vals = [y for _, y in cs]
    target = F(0) if wall in ("left", "bottom") else side
    return sum(1 for v in vals if v == target)


def near_set(check: dict[str, Any], below: F) -> dict[tuple[int, int], F]:
    return {(p["pair"][0], p["pair"][1]): F(p["exact"]) for p in check["decision"]["near_pairs"] if F(p["exact"]) < below}


def close_pairs(poses: tuple[Pose, ...]) -> set[tuple[int, int]]:
    out = set()
    for i in range(len(poses)):
        for k in range(i + 1, len(poses)):
            dx, dy = poses[i].x - poses[k].x, poses[i].y - poses[k].y
            if dx * dx + dy * dy < 2:
                out.add((i + 1, k + 1))
    return out


def main(argv: list[str]) -> int:
    if len(argv) != 6:
        print(__doc__)
        return 2
    j7, j6, c7p, c6p, out = argv[1:]
    r7, r6 = R.read_json(j7), R.read_json(j6)
    with open(c7p, encoding="utf-8") as fh:
        c7 = json.load(fh)
    with open(c6p, encoding="utf-8") as fh:
        c6 = json.load(fh)
    n = r7.n
    res: dict[str, Any] = {"program": "l182_compare.py", "lane": "L182"}
    res["sides"] = {"997": fstr(r7.side), "996": fstr(r6.side), "996_minus_997": fstr(r6.side - r7.side), "approx": sci(r6.side - r7.side)}

    # The pairing: each square's nearest centre in the other file, exactly.
    def nearest(a: Pose, others: tuple[Pose, ...]) -> int:
        d = [(o.x - a.x) ** 2 + (o.y - a.y) ** 2 for o in others]
        m = min(d)
        hits = [k + 1 for k, v in enumerate(d) if v == m]
        return hits[0] if len(hits) == 1 else -1

    res["nearest_centre_is_own_number"] = {
        "997_to_996": all(nearest(p, r6.poses) == k for k, p in enumerate(r7.poses, start=1)),
        "996_to_997": all(nearest(p, r7.poses) == k for k, p in enumerate(r6.poses, start=1)),
    }

    rows = []
    for k in range(n):
        p, q = r7.poses[k], r6.poses[k]
        dx, dy = p.x - q.x, p.y - q.y
        d2 = dx * dx + dy * dy
        rc, rs = relative(p, q)
        t = rs / (1 + rc)
        rows.append(
            {
                "square": k + 1,
                "move_squared": fstr(d2),
                "move": float(math.sqrt(d2)) if d2 else 0.0,
                "dx": float(dx),
                "dy": float(dy),
                "centre_997": [round(float(p.x), 6), round(float(p.y), 6)],
                "tilt_996": tilt(q),
                "tilt_997": tilt(p),
                "turn_degrees": math.degrees(math.atan2(float(rs), float(rc))),
                "turn_half_tangent": fstr(t),
                "same_pose": d2 == 0 and rs == 0,
                "upright_997": p.c == 0 or p.s == 0,
                "upright_996": q.c == 0 or q.s == 0,
            }
        )
    upright7 = [r["square"] for r in rows if r["upright_997"]]
    tilted = [r for r in rows if not r["upright_997"]]
    near_up_dirs = Counter((fstr(r6.poses[k - 1].c), fstr(r6.poses[k - 1].s)) for k in upright7)
    res["tilts"] = {
        "exactly_upright_997": len(upright7),
        "exactly_upright_996": sum(1 for r in rows if r["upright_996"]),
        "upright_997_were_996_direction": [{"cos": c, "sin": s, "squares": m} for (c, s), m in near_up_dirs.items()],
        "upright_997_turn_half_tangents": dict(Counter(rows[k - 1]["turn_half_tangent"] for k in upright7)),
        "upright_997_turn_degrees": sorted({f"{rows[k - 1]['turn_degrees']:.6e}" for k in upright7}),
        "tilted_997": len(tilted),
        "tilted_turns": sorted(({"square": r["square"], "tilt_996": round(r["tilt_996"], 6), "tilt_997": round(r["tilt_997"], 6), "turn": round(r["turn_degrees"], 6)} for r in tilted), key=lambda e: -abs(e["turn"])),
        "tilted_unturned_exactly": [r["square"] for r in tilted if r["turn_half_tangent"] == "0"],
        "turned_beyond": {str(c): sum(1 for r in rows if abs(r["turn_degrees"]) > c) for c in (1e-9, 1e-6, 1e-3, 1e-2, 1e-1, 1.0)},
    }
    moves = sorted(rows, key=lambda r: -r["move"])
    res["moves"] = {
        "unmoved_exactly": [r["square"] for r in rows if r["move_squared"] == "0"],
        "same_pose_exactly": [r["square"] for r in rows if r["same_pose"]],
        "beyond": {str(c): sum(1 for r in rows if r["move"] > c) for c in (1e-12, 1e-9, 1e-6, 1e-3, 1e-2, 1e-1)},
        "largest": [{k: (round(v, 9) if isinstance(v, float) else v) for k, v in r.items() if k not in ("move_squared", "turn_half_tangent", "same_pose", "upright_996")} for r in moves[:16]],
        "beyond_1e-3_squares": sorted(r["square"] for r in rows if r["move"] > 1e-3),
        "beyond_1e-6_squares": sorted(r["square"] for r in rows if r["move"] > 1e-6),
    }

    walls: dict[str, Any] = {}
    for name, rr, cc in (("997", r7, c7), ("996", r6, c6)):
        con = cc["decision"]["wall_contacts"]
        kinds = Counter()
        for w in WALLS:
            for i in con[w]:
                kinds[corners_on_wall(rr.poses[i - 1], w, rr.side)] += 1
        walls[name] = {
            "contacts": con,
            "count": sum(len(v) for v in con.values()),
            "corners_on_the_wall_per_contact": {str(k): v for k, v in kinds.items()},
            "least_positive_clearance": {w: {"squares": v["squares"], "approx": v["approx"], "exact": v["exact"]} for w, v in cc["decision"]["least_positive_clearance"].items()},
        }
    c7c, c6c = walls["997"]["contacts"], walls["996"]["contacts"]
    walls["contacts_lost"] = {w: sorted(set(c6c[w]) - set(c7c[w])) for w in WALLS}
    walls["contacts_gained"] = {w: sorted(set(c7c[w]) - set(c6c[w])) for w in WALLS}
    lp7, lp6 = walls["997"]["least_positive_clearance"], walls["996"]["least_positive_clearance"]
    walls["right_top_slack"] = {
        "997": {"approx": lp7["right"]["approx"], "right": lp7["right"]["squares"], "top": lp7["top"]["squares"]},
        "996": {"approx": lp6["right"]["approx"], "right": lp6["right"]["squares"], "top": lp6["top"]["squares"]},
    }
    res["walls"] = walls

    tiny = F(1, 10**9)
    n7, n6 = near_set(c7, tiny), near_set(c6, tiny)
    common = sorted(set(n7) & set(n6))
    ratios = [n7[k] / n6[k] for k in common]
    res["near_pairs_below_1e-9"] = {
        "997": len(n7),
        "996": len(n6),
        "common": len(common),
        "only_996": sorted([list(k) for k in set(n6) - set(n7)]),
        "only_997": sorted([list(k) for k in set(n7) - set(n6)]),
        "least_997": {"pair": list(min(n7, key=lambda k: n7[k])), "approx": sci(min(n7.values()))},
        "least_996": {"pair": list(min(n6, key=lambda k: n6[k])), "approx": sci(min(n6.values()))},
        "greatest_997": sci(max(n7.values())),
        "greatest_996": sci(max(n6.values())),
        "common_ratio_997_over_996": [f"{float(min(ratios)):.4f}", f"{float(max(ratios)):.4f}"] if ratios else None,
        "common_wider_in_997": sum(1 for x in ratios if x > 1),
        "common_narrower_in_997": sum(1 for x in ratios if x < 1),
        "next_after_997": [{"pair": p["pair"], "approx": p["margin"]} for p in c7["decision"]["near_pairs"] if F(p["exact"]) >= tiny][:3],
        "next_after_996": [{"pair": p["pair"], "approx": p["margin"]} for p in c6["decision"]["near_pairs"] if F(p["exact"]) >= tiny][:3],
    }
    cp7, cp6 = close_pairs(r7.poses), close_pairs(r6.poses)
    res["centres_closer_than_sqrt2"] = {"997": len(cp7), "996": len(cp6), "only_996": sorted([list(k) for k in cp6 - cp7]), "only_997": sorted([list(k) for k in cp7 - cp6])}
    res["per_square"] = [{k: (round(v, 12) if isinstance(v, float) else v) for k, v in r.items()} for r in rows]
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    print(
        f"nearest own number {res['nearest_centre_is_own_number']}; upright 997 {len(upright7)}; moves beyond {res['moves']['beyond']}; "
        f"turned beyond {res['tilts']['turned_beyond']}; contacts 997 {walls['997']['count']} {walls['997']['corners_on_the_wall_per_contact']}, "
        f"996 {walls['996']['count']} {walls['996']['corners_on_the_wall_per_contact']}; near pairs 997 {len(n7)} 996 {len(n6)} common {len(common)}; "
        f"close pairs 997 {len(cp7)} 996 {len(cp6)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
