"""Lane L159's description of the certificate: decides nothing.

Clean-room code written for the stage 4 review of issue #983. It reads the certificate
through the reader and the check receipt, and reports the side's decimals, the
distribution of the near pair margins and the near wall clearances, and the tilts.
Angles are printed in binary64 from the exact unit edge vectors; nothing here decides.

Usage: l159_describe.py CERT.yaml TWIN.json CHECK.json OUT.json
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l159_geom as geom  # noqa: E402
import l159_sat as sat  # noqa: E402
from l159_reader import read_paths  # noqa: E402

WALLS = ("left", "bottom", "right", "top")


def tilt_degrees(u: tuple[Fraction, Fraction]) -> float:
    """The square's turn from upright, folded into (-45, 45] degrees."""
    angle = math.degrees(math.atan2(float(u[1]), float(u[0])))
    while angle > 45:
        angle -= 90
    while angle <= -45:
        angle += 90
    return angle


def main(argv: list[str]) -> int:
    cert, twin, check_path, out_path = (Path(a) for a in argv[1:5])
    w = read_paths(cert, twin)
    check = json.loads(check_path.read_text(encoding="utf-8"))
    side = Fraction(*w.side)
    frames = [geom.centre_frame(c) for c in w.squares]
    out: dict[str, object] = {"program": "l159_describe.py"}
    out["side_floor_40"] = geom.floor_places(side, 40)
    out["side_floor_12"] = geom.floor_places(side, 12)
    out["side_ceil_12"] = geom.ceil_places(side, 12)
    out["side_ceil_15"] = geom.ceil_places(side, 15)
    out["side_floor_15"] = geom.floor_places(side, 15)

    # Tilts.
    tilts = []
    exact_upright = []
    for i, (_, u, _) in enumerate(frames, start=1):
        if u[0] == 0 or u[1] == 0:
            exact_upright.append(i)
            tilts.append((0.0, i))
        else:
            tilts.append((tilt_degrees(u), i))
    tilted = [(t, i) for t, i in tilts if abs(t) > 0.5]
    out["tilted_beyond_half_degree"] = len(tilted)
    out["tilted_beyond_one_degree"] = sum(1 for t, _ in tilts if abs(t) > 1)
    pos = sorted(t for t, _ in tilted if t > 0)
    neg = sorted(t for t, _ in tilted if t < 0)
    out["tilted_positive"] = {"count": len(pos), "min": pos[0] if pos else None, "max": pos[-1] if pos else None}
    out["tilted_negative"] = {"count": len(neg), "min": neg[0] if neg else None, "max": neg[-1] if neg else None}
    out["tilted_squares"] = sorted(i for _, i in tilted)
    band = sorted((t, i) for t, i in tilted if abs(t) > 10)
    out["band_beyond_10_degrees"] = {
        "count": len(band),
        "min": band[0] if band else None,
        "max": band[-1] if band else None,
        "mean": sum(t for t, _ in band) / len(band) if band else None,
        "squares": sorted(i for _, i in band),
    }
    out["tilted_half_to_10_degrees"] = sorted([i, t] for t, i in tilted if abs(t) <= 10)
    near_upright = [(abs(t), i) for t, i in tilts if abs(t) <= 0.5 and i not in exact_upright]
    out["exactly_upright"] = exact_upright
    out["near_upright_count"] = len(near_upright)
    out["near_upright_beyond"] = {
        str(b): sum(1 for t, _ in near_upright if t > b) for b in (1e-12, 1e-9, 1e-6, 1e-3)
    }
    out["near_upright_largest"] = max(near_upright) if near_upright else None
    out["tilt_histogram_degrees"] = {}
    for t, _ in tilted:
        key = str(round(t))
        out["tilt_histogram_degrees"][key] = out["tilt_histogram_degrees"].get(key, 0) + 1  # type: ignore[index]

    # Near pairs, recomputed exactly by method A for the description.
    prepared = [sat.prepare(c) for c in w.squares]
    near = []
    for i, j, _ in check["near_pairs"]:
        m = sat.margin_fraction(sat.margin(prepared[i - 1], prepared[j - 1]))  # type: ignore[arg-type]
        near.append((m, i, j))
    near.sort()
    tight = [x for x in near if x[0] < Fraction(1, 10**12)]
    out["pairs_below_1e-12"] = len(tight)
    out["tight_min"] = [geom.sci(tight[0][0], 6), tight[0][1], tight[0][2]]
    out["tight_max"] = [geom.sci(tight[-1][0], 6), tight[-1][1], tight[-1][2]]
    out["tight_median"] = geom.sci(tight[len(tight) // 2][0], 6)
    distinct: dict[str, int] = {}
    for m, _, _ in tight:
        key = geom.sci(m, 6)
        distinct[key] = distinct.get(key, 0) + 1
    out["tight_distinct_values"] = len(distinct)
    out["tight_most_common"] = sorted(distinct.items(), key=lambda kv: -kv[1])[:8]
    rest = [x for x in near if x[0] >= Fraction(1, 10**12)]
    out["next_pair_above_1e-12"] = [geom.sci(rest[0][0], 6), rest[0][1], rest[0][2]] if rest else None
    out["pairs_1e-12_to_1e-6"] = sum(1 for m, _, _ in rest if m < Fraction(1, 10**6))
    out["pairs_1e-6_to_1e-4"] = sum(1 for m, _, _ in rest if Fraction(1, 10**6) <= m < Fraction(1, 10**4))
    out["pairs_1e-4_to_1e-3"] = sum(1 for m, _, _ in rest if Fraction(1, 10**4) <= m < Fraction(1, 10**3))

    # Near walls.
    walls_tiny = [x for x in check["near_walls"] if float(x[2]) < 1e-13]
    out["positive_clearances_below_1e-13"] = len(walls_tiny)
    out["positive_clearances_below_1e-13_by_wall"] = {wall: sum(1 for x in walls_tiny if x[1] == wall) for wall in WALLS}
    out["positive_clearances_below_1e-13_largest"] = max(walls_tiny, key=lambda x: float(x[2])) if walls_tiny else None
    others = [x for x in check["near_walls"] if float(x[2]) >= 1e-13]
    out["next_clearances"] = others[:10]
    # Turns of the squares that sit within 1e-13 of a wall without touching it.
    turns = {}
    for i, wall, _ in walls_tiny:
        _, u, _ = frames[i - 1]
        turns[str(i)] = tilt_degrees(u) if u[0] != 0 and u[1] != 0 else 0.0
    out["turns_of_squares_within_1e-13_of_a_wall_degrees"] = turns
    out_path.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print("tilted >0.5:", out["tilted_beyond_half_degree"], out["tilted_positive"], out["tilted_negative"], "| exact upright", len(exact_upright), "| tight", out["tight_min"], out["tight_max"], out["tight_median"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
