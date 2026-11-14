"""Lane L163 description of a certificate; decides nothing.

Usage: l163_describe.py LABEL MAIN.json CHECK.json OUT.json

Reports the tilts, the near-pair margins, the near-wall clearances, the packing's two
extents against the side, the pairs whose centres are closer than sqrt 2, and the
`side_decimal_info_only` string against the side's digits. Margins and clearances come
from method A over every pair; the check receipt is read for comparison only.
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fractions import Fraction as F  # noqa: E402

import l163_geom as geom  # noqa: E402
import l163_sat as sat  # noqa: E402
from l163_reader import read_json  # noqa: E402

WALLS = ("left", "bottom", "right", "top")


def deg(t: F) -> float:
    """The square's angle in degrees, reduced to (-45, 45]."""
    a = math.degrees(2 * math.atan(float(t)))
    while a > 45:
        a -= 90
    while a <= -45:
        a += 90
    return a


def main() -> None:
    label, main_json, check_json, out = sys.argv[1:5]
    t0 = time.process_time()
    cert = read_json(main_json)
    with open(check_json, encoding="utf-8") as fh:
        check = json.load(fh)
    side = F(*cert.side)
    rows = cert.squares
    n = cert.n
    sq = [sat.prepare(r) for r in rows]
    rec: dict[str, object] = {"label": label, "lane": "L163", "program": "l163_describe.py"}
    info = cert.info.get("side_decimal_info_only", "")
    digits = info.rstrip("…")
    places = len(digits.split(".")[1]) if "." in digits else 0
    rec["side_decimal_info_only"] = {
        "string": info,
        "floor_at_its_places": geom.floor_places(side, places),
        "equals_floor": digits == geom.floor_places(side, places),
        "side_45_places": geom.floor_places(side, 45),
    }
    # tilts
    ang = [(i + 1, deg(F(r[4], r[5]))) for i, r in enumerate(rows)]
    exact0 = [i for i, r in enumerate(rows, 1) if r[4] == 0]
    absd = [abs(a) for _, a in ang]
    tilted = [(i, a) for i, a in ang if abs(a) > 0.5]
    rec["tilts"] = {
        "exactly_upright": len(exact0),
        "below_1e-9_deg_nonzero": sum(1 for (_, a), r in zip(ang, rows, strict=True) if r[4] != 0 and abs(a) < 1e-9),
        "below_1e-3_deg": sum(1 for x in absd if x < 1e-3),
        "below_0.5_deg": sum(1 for x in absd if x <= 0.5),
        "beyond_0.5_deg": len(tilted),
        "beyond_0.5_positive": sum(1 for _, a in tilted if a > 0),
        "beyond_0.5_negative": sum(1 for _, a in tilted if a < 0),
        "beyond_0.5_range": [round(min(a for _, a in tilted), 4), round(max(a for _, a in tilted), 4)] if tilted else [],
        "beyond_0.5_abs_mean": round(sum(abs(a) for _, a in tilted) / len(tilted), 4) if tilted else None,
        "beyond_0.5_rounded_0.01_top": Counter(round(a, 2) for _, a in tilted).most_common(8),
        "between_1e-3_and_0.5_deg": [[i, round(a, 6)] for i, a in ang if 1e-3 <= abs(a) <= 0.5],
        "largest_t_digits": max(len(str(r[5])) for r in rows),
        "distinct_t": len({(r[4], r[5]) for r in rows}),
    }
    # pairs
    near: list[tuple[F, int, int]] = []
    close2 = 0
    for i in range(n):
        for j in range(i + 1, n):
            m = sat.margin(sq[i], sq[j])
            if m < F(1, 1000):
                near.append((m, i + 1, j + 1))
            dx = F(rows[j][0], rows[j][1]) - F(rows[i][0], rows[i][1])
            dy = F(rows[j][2], rows[j][3]) - F(rows[i][2], rows[i][3])
            close2 += dx * dx + dy * dy < 2
    near.sort()
    small = [m for m, _, _ in near if m < F(1, 10**6)]
    rec["pairs"] = {
        "centres_closer_than_sqrt2": close2,
        "below_1e-3": len(near),
        "below_1e-6": len(small),
        "below_1e-6_range_sci": [geom.sci(small[0]), geom.sci(small[-1])] if small else [],
        "below_1e-6_median_sci": geom.sci(small[len(small) // 2]) if small else None,
        "below_1e-6_distinct_6_figures": len({geom.sci(m) for m in small}),
        "below_1e-6_common_6_figures": Counter(geom.sci(m) for m in small).most_common(5),
        "first_above_1e-6": [geom.sci(near[len(small)][0]), near[len(small)][1], near[len(small)][2]] if len(near) > len(small) else None,
        "least_10": [[i, j, geom.sci(m)] for m, i, j in near[:10]],
    }
    # walls and extents
    clear = [sat.clearances(s, cert.side) for s in sq]
    by_wall = {}
    for w in range(4):
        vals = sorted((cl[w], i + 1) for i, cl in enumerate(clear))
        by_wall[WALLS[w]] = {
            "contacts": [i for c, i in vals if c == 0],
            "positive_below_1e-12": len([c for c, _ in vals if 0 < c < F(1, 10**12)]),
            "least_positive": [geom.sci(next(c for c, _ in vals if c > 0)), next(i for c, i in vals if c > 0)],
        }
    rec["walls"] = by_wall
    lo = [min(cl[w] for cl in clear) for w in range(4)]
    rec["extents"] = {
        "x_extent_less_side_sci": geom.sci(-(lo[0] + lo[2])),
        "y_extent_less_side_sci": geom.sci(-(lo[1] + lo[3])),
        "walls_touched": [WALLS[w] for w in range(4) if lo[w] == 0],
        "side_is_x_extent": lo[0] + lo[2] == 0,
        "side_is_y_extent": lo[1] + lo[3] == 0,
    }
    rec["check_least_margin"] = check["main"]["least_margin_sci"]
    rec["cpu_seconds"] = round(time.process_time() - t0, 1)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1)
    print(label, "tilted>0.5", len(tilted), "upright", len(exact0), "near<1e-6", len(small), "close<sqrt2", close2, "walls", rec["extents"]["walls_touched"])


if __name__ == "__main__":
    main()
