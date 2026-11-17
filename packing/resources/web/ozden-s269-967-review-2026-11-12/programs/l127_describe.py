"""Descriptive statistics of the certificate for the review's tables. Decides nothing.

Lane L127, clean room. Usage: python -I -B l127_describe.py CERT.yaml TWIN.json OUT.json

Uses the reader and method A's exact margins and clearances (the deciding runs are
l127_check.py's); prints the side's decimals, the distribution of pair margins below
1e-3 and of wall clearances below 1e-3 by wall, and the squares' tilts in degrees
(binary64, descriptive only).
"""

from __future__ import annotations

import json
import math
import statistics
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l127_reader as rd  # noqa: E402
import l127_sat as ma  # noqa: E402


def decimals(x: F, places: int) -> str:
    q, r = divmod(x.numerator * 10**places, x.denominator)
    s = str(q).rjust(places + 1, "0")
    return f"{s[:-places]}.{s[-places:]}"


def main(argv: list[str]) -> int:
    doc = rd.read_certificate(Path(argv[1]).read_text(encoding="utf-8"), Path(argv[2]).read_text(encoding="utf-8"))
    side = F(*doc["side"])
    sq = [ma.make_square(c) for c in doc["squares"]]
    n = len(sq)
    margins: list[tuple[F, int, int]] = []
    for i in range(n):
        for j in range(i + 1, n):
            m = ma.pair_margin(sq[i], sq[j])
            v = F(m[0], m[1])
            if v < F(1, 1000):
                margins.append((v, i + 1, j + 1))
    margins.sort()
    walls: list[tuple[F, int, str]] = []
    for k, s in enumerate(sq):
        for w, c in ma.wall_clearances(s, doc["side"]).items():
            v = F(c[0], c[1])
            if v < F(1, 1000):
                walls.append((v, k + 1, w))
    walls.sort()
    near = [m for m in margins if m[0] < F(1, 10**12)]
    mid = [m for m in margins if F(1, 10**12) <= m[0]]
    near_vals = [float(m[0]) for m in near]

    def fmt(t: tuple[F, int, Any]) -> dict[str, Any]:
        return {"at": [t[1], t[2]], "sci": f"{float(t[0]):.4e}"}

    tilt = []
    for s in sq:
        a = math.degrees(math.atan2(float(F(s.u[1], s.d)), float(F(s.u[0], s.d))))
        a = (a + 45) % 90 - 45  # tilt from upright, in (-45, 45]
        tilt.append(a)
    exact_upright = sum(1 for s in sq if s.u[0] == 0 or s.u[1] == 0)
    by_wall_13: dict[str, int] = {}
    for v, _, w in walls:
        if 0 < v < F(1, 10**13):
            by_wall_13[w] = by_wall_13.get(w, 0) + 1
    beyond = [t for t in walls if t[0] >= F(1, 10**13)]
    out = {
        "program": "l127_describe.py",
        "side_floor_40": decimals(side, 40),
        "side_digits": [len(str(side.numerator)), len(str(side.denominator))],
        "near_pairs": {
            "count": len(near),
            "least": fmt(near[0]),
            "greatest": fmt(near[-1]),
            "median_sci": f"{statistics.median(near_vals):.4e}",
        },
        "pairs_1e-12_to_1e-3": {
            "count": len(mid),
            "first": [fmt(t) for t in mid[:6]],
            "below_1e-4": sum(1 for t in mid if t[0] < F(1, 10**4)),
        },
        "wall_clearances_positive_below_1e-13_by_wall": by_wall_13,
        "wall_clearances_positive_below_1e-13_range": [fmt(t) for t in walls if 0 < t[0] < F(1, 10**13)][:1]
        + [fmt(t) for t in walls if 0 < t[0] < F(1, 10**13)][-1:],
        "wall_clearances_1e-13_to_1e-3": [fmt(t) for t in beyond],
        "least_right_clearance": fmt(min((t for t in walls if t[2] == "right"), key=lambda t: t[0])),
        "tilts": {
            "exactly_upright": exact_upright,
            "beyond_0.5_deg": sum(1 for a in tilt if abs(a) > 0.5),
            "beyond_1_deg": sum(1 for a in tilt if abs(a) > 1),
            "positive_beyond_0.5": sum(1 for a in tilt if a > 0.5),
            "negative_beyond_0.5": sum(1 for a in tilt if a < -0.5),
            "range_beyond_0.5": [round(min((abs(a) for a in tilt if abs(a) > 0.5), default=0), 3), round(max(abs(a) for a in tilt), 3)],
            "clusters_0.01_deg": sorted(
                ({"deg": round(a, 2), "count": c} for a, c in _clusters([a for a in tilt if abs(a) > 0.5]).items()),
                key=lambda d: -d["count"],
            )[:6],
        },
    }
    Path(argv[3]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out)[:600])
    return 0


def _clusters(angles: list[float]) -> dict[float, int]:
    out: dict[float, int] = {}
    for a in angles:
        key = round(a, 2)
        out[key] = out.get(key, 0) + 1
    return out


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
