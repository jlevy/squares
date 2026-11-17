"""Lane L180: describe the certificate (tilts, near pairs, near walls, extents); decides nothing.

Written for the blind stage 4 review of issue #996 as a clean-room implementation.
It imports nothing from this repository or the source, and reuses no code of any
earlier review. Exact values come from the check receipt and from fractions; angles
are printed in binary64 degrees from the exact (cos, sin) and are descriptive only.

Usage: l180_describe.py JSON CHECK_RECEIPT OUT
"""

from __future__ import annotations

import json
import math
import os
import sys
from collections import Counter
from fractions import Fraction as F
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l180_reader as R  # noqa: E402
from l180_decide import fstr, sci  # noqa: E402


def tilt_degrees(c: F, s: F) -> float:
    """The square's turn from upright, reduced to (-45, 45] degrees (a square repeats every 90)."""
    a = math.degrees(math.atan2(float(s), float(c)))
    while a > 45:
        a -= 90
    while a <= -45:
        a += 90
    return a


def decimals(v: F, places: int) -> str:
    q = v.numerator * 10**places // v.denominator
    s = str(q)
    return f"{s[:-places]}.{s[-places:]}"


def ceil_places(v: F, places: int) -> str:
    q = -((-v.numerator * 10**places) // v.denominator)
    s = str(q)
    return f"{s[:-places]}.{s[-places:]}"


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__)
        return 2
    r = R.read_json(argv[1])
    with open(argv[2], encoding="utf-8") as fh:
        dec = json.load(fh)["decision"]
    out: dict[str, Any] = {"program": "l180_describe.py", "lane": "L180"}
    S = r.side
    out["side"] = {"exact": fstr(S), "places_30": decimals(S, 30), "ceil_12": ceil_places(S, 12), "floor_12": decimals(S, 12)}

    tilts = [tilt_degrees(p.c, p.s) for p in r.poses]
    exact_upright = [k + 1 for k, p in enumerate(r.poses) if p.c == 0 or p.s == 0]
    tiny = [k + 1 for k, a in enumerate(tilts) if abs(a) < 1e-6 and (k + 1) not in exact_upright]
    small = [k + 1 for k, a in enumerate(tilts) if 1e-6 <= abs(a) < 0.5]
    leaning = [k + 1 for k, a in enumerate(tilts) if abs(a) >= 0.5]
    dirs = Counter((p.c, p.s) for p in r.poses)
    orient = [max([(p.c, p.s), (-p.s, p.c), (-p.c, -p.s), (p.s, -p.c)]) for p in r.poses]
    by_angle: dict[str, set[tuple[F, F]]] = {}
    for k, o in enumerate(orient):
        by_angle.setdefault(f"{tilts[k]:.6f}", set()).add(o)
    shared = {
        a: [k + 1 for k in range(len(tilts)) if f"{tilts[k]:.6f}" == a]
        for a, os_ in by_angle.items()
        if len(os_) > 1
    }
    tiny_dirs = Counter((fstr(r.poses[k - 1].c), fstr(r.poses[k - 1].s)) for k in tiny)
    out["tilts"] = {
        "exactly_upright": exact_upright,
        "within_1e-6_degrees_not_exact": {"count": len(tiny), "directions": [{"cos": c, "sin": s, "squares": n} for (c, s), n in tiny_dirs.items()], "tilts_degrees": sorted({f"{tilts[k - 1]:.6e}" for k in tiny})},
        "between_1e-6_and_0.5_degrees": [{"square": k, "degrees": round(tilts[k - 1], 6)} for k in small],
        "beyond_0.5_degrees": {"count": len(leaning), "clockwise": sum(1 for k in leaning if tilts[k - 1] < 0), "counterclockwise": sum(1 for k in leaning if tilts[k - 1] > 0), "range": [round(min(tilts[k - 1] for k in leaning), 4), round(max(tilts[k - 1] for k in leaning), 4)] if leaning else None},
        "leaning_by_degrees_6": dict(Counter(f"{tilts[k - 1]:.6f}" for k in leaning).most_common()),
        "distinct_exact_directions": len(dirs),
        "distinct_exact_orientations_modulo_quarter_turns": len(set(orient)),
        "distinct_tilts_to_six_places": len(by_angle),
        "six_place_tilts_under_several_exact_orientations": shared,
        "per_square_degrees": [round(a, 9) for a in tilts],
    }
    near = dec["near_pairs"]
    gaps = sorted(F(p["exact"]) for p in near if F(p["exact"]) < F(1, 10**9))
    out["near_pairs"] = {
        "below_1e-9": len(gaps),
        "range": [sci(gaps[0]), sci(gaps[-1])] if gaps else None,
        "median": sci(gaps[len(gaps) // 2]) if gaps else None,
        "distinct_exact": len(set(gaps)),
        "binding_normals": dict(Counter(p["binding_normals"] for p in near if F(p["exact"]) < F(1, 10**9))),
        "next_after": [p for p in near if F(p["exact"]) >= F(1, 10**9)][:6],
        "commonest": [{"margin": sci(v, 6), "pairs": n} for v, n in Counter(gaps).most_common(5)],
    }
    clear = dec["near_walls"]
    out["near_walls"] = clear
    lpc = dec["least_positive_clearance"]
    least_left = F(0) if dec["wall_contacts"]["left"] else F(lpc["left"]["exact"])
    least_bottom = F(0) if dec["wall_contacts"]["bottom"] else F(lpc["bottom"]["exact"])
    least_right = F(0) if dec["wall_contacts"]["right"] else F(lpc["right"]["exact"])
    least_top = F(0) if dec["wall_contacts"]["top"] else F(lpc["top"]["exact"])
    wx = S - least_left - least_right
    wy = S - least_bottom - least_top
    out["extent"] = {
        "width_x": fstr(wx),
        "width_y": fstr(wy),
        "side_minus_width_x": sci(S - wx),
        "side_minus_width_y": sci(S - wy),
        "width_x_places_30": decimals(wx, 30),
    }
    with open(argv[3], "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(
        f"upright exactly {len(exact_upright)}, within 1e-6 deg {len(tiny)}, small {len(small)}, leaning {len(leaning)}; "
        f"near pairs {len(gaps)} from {out['near_pairs']['range']}; extent x {out['extent']['side_minus_width_x']} below S"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
