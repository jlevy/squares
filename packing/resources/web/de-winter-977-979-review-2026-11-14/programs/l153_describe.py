"""Lane L153 description of a certificate: decides nothing.

Clean-room: written for this review, importing nothing from this repository or the
source, and reusing no code of any earlier review.

It prints the side's decimals, the tilt of every square (its angle reduced to
(-45, 45] degrees), the distribution of the near-pair margins and positive clearances
from the frozen check receipt, and the gaps' exact values where they repeat.

Usage: l153_describe.py LABEL CERT.json [TWIN.yaml] CHECK.json OUT.json
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l153_geom as G  # noqa: E402
import l153_sat as A  # noqa: E402
import l153_reader as reader  # noqa: E402
from l153_check import floor_places, sci  # noqa: E402


def tilt(c: Fraction, s: Fraction) -> float:
    a = math.degrees(math.atan2(float(s), float(c)))
    while a <= -45:
        a += 90
    while a > 45:
        a -= 90
    return a


def main(argv: list[str]) -> int:
    label = argv[1]
    cert = argv[2]
    twin = argv[3] if len(argv) == 6 else None
    check = json.loads(Path(argv[-2]).read_text())
    data = reader.read(cert, twin)
    side = Fraction(*data["side"])
    sq = [G.decode(s) for s in data["squares"]]
    n = len(sq)
    tilts = [tilt(c, s) for _, _, c, s in sq]
    exactly_upright = [k + 1 for k, (_, _, c, s) in enumerate(sq) if c == 0 or s == 0]
    tilted = [(k + 1, tilts[k]) for k in range(n) if abs(tilts[k]) > 1]
    slight = [(k + 1, tilts[k]) for k in range(n) if 0 < abs(tilts[k]) <= 1]
    pos = [t for _, t in tilted if t > 0]
    neg = [t for _, t in tilted if t < 0]
    near = check["pairs"]["near_below_1e-9"]
    margins = Counter(x[2] for x in near)
    # The gap structure: every pair margin (method A's closed form), split at 10^-30.
    prep = [A.prepare(G.encode(s)) for s in sq]
    tiny = Fraction(1, 10**30)
    small: list[Fraction] = []
    above: tuple[Fraction, int, int] | None = None
    for i in range(n):
        for j in range(i + 1, n):
            m = A.margin(prep[i], prep[j])
            if 0 < m < tiny:
                small.append(m)
            elif m >= tiny and (above is None or m < above[0]):
                above = (m, i + 1, j + 1)
    clears = sorted(
        (v, k + 1, w)
        for k, s in enumerate(sq)
        for w, v in A.clearances(prep[k], side).items()
        if v > 0
    )
    small_clear = [c for c in clears if c[0] < tiny]
    next_clear = next((c for c in clears if c[0] >= tiny), None)
    gaps = {
        "positive_pairs_below_1e-30": len(small),
        "pair_range": [sci(min(small), 10), sci(max(small), 10)] if small else None,
        "next_pair": None if above is None else [above[1], above[2], sci(above[0], 8)],
        "positive_clearances_below_1e-30": len(small_clear),
        "clearance_range": [sci(small_clear[0][0], 10), sci(small_clear[-1][0], 10)] if small_clear else None,
        "their_walls": dict(Counter(c[2] for c in small_clear)),
        "next_clearance": None if next_clear is None else [next_clear[1], next_clear[2], sci(next_clear[0], 8)],
    }
    denominators = Counter()
    for _, _, c, s in sq:
        denominators[max(c.denominator, s.denominator)] += 1
    out = {
        "program": "l153_describe.py",
        "label": label,
        "n": n,
        "side_floor_40": floor_places(side, 40),
        "side_floor_15": floor_places(side, 15),
        "tilts": {
            "exactly_upright": len(exactly_upright),
            "turned_but_within_1_degree": len(slight),
            "beyond_1_degree": len(tilted),
            "beyond_1_degree_positive": [len(pos), round(min(pos), 4) if pos else None, round(max(pos), 4) if pos else None],
            "beyond_1_degree_negative": [len(neg), round(min(neg), 4) if neg else None, round(max(neg), 4) if neg else None],
            "tilted_squares": [[k, round(t, 4)] for k, t in tilted],
            "basis_denominator_digits": sorted({len(str(d)) for d in denominators}),
        },
        "near_pairs": {
            "below_1e-9": len(near),
            "most_common_margins_8_digits": margins.most_common(6),
        },
        "gaps": gaps,
        "walls": check["walls"]["positive_below_1e-t"],
        "least_positive_clearance": check["walls"]["least_positive"],
        "centre_extent": {
            "x": [sci(min(s[0] for s in sq), 10), sci(max(s[0] for s in sq), 10)],
            "y": [sci(min(s[1] for s in sq), 10), sci(max(s[1] for s in sq), 10)],
        },
    }
    Path(argv[-1]).write_text(json.dumps(out, indent=1) + "\n")
    print(label, "upright exactly", len(exactly_upright), "within 1 degree", len(slight),
          "tilted beyond 1 degree", len(tilted), f"(+{len(pos)} / -{len(neg)})",
          "ranges", out["tilts"]["beyond_1_degree_positive"], out["tilts"]["beyond_1_degree_negative"],
          "gaps", json.dumps(gaps))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
