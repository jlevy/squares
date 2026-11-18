"""Describe the four certificates of s(127) (lane r127b-1118). Decides nothing.

Written after the checker's freeze. Usage:

    python -I -B rb127_describe.py T305.yaml E1015.json E1017.json E1020.json OUT.json

For each certificate: its side against its extent (the least number of decimal places at
which the extent rounded up is the side, if any), its walls and the squares that touch
them, the spread of its near pairs' margins and contact factors, and every square that
is turned but by less than one degree, with its angle. Exact values are computed from
the rationals; angles are printed through binary64 and are descriptions only.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as Fr
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rb127_axes as A  # noqa: E402
import rb127_fmt as F  # noqa: E402
import rb127_read as R  # noqa: E402
import rb127_twin as T  # noqa: E402


def describe(rows: list, side: tuple[int, int]) -> dict:
    ip = [A.to_ipose(*r) for r in rows]
    S = Fr(side[0], side[1])
    n = len(ip)
    lo_x = min(A.centre(p)[0] - A.half_extent(p) for p in ip)
    hi_x = max(A.centre(p)[0] + A.half_extent(p) for p in ip)
    lo_y = min(A.centre(p)[1] - A.half_extent(p) for p in ip)
    hi_y = max(A.centre(p)[1] + A.half_extent(p) for p in ip)
    ext = max(hi_x - lo_x, hi_y - lo_y)
    k_up = next((k for k in range(0, 400) if F.ceil_places(ext, k) == F.floor_places(S, k) and Fr(F.ceil_places(ext, k)) == S), None)
    margins = []
    factors = []
    for i, j in combinations(range(n), 2):
        M, Hn, L = A.pair_numbers(ip[i], ip[j])
        m = Fr(M - Hn, L)
        if m < Fr(1, 10**3):
            margins.append((m, (i + 1, j + 1)))
            factors.append(1 - Fr(Hn, M))
    margins.sort()
    bands: dict[str, int] = {}
    for m, _ in margins:
        e = "0" if m == 0 else F.sci(m, 1).split("e")[1]
        bands[e] = bands.get(e, 0) + 1
    near_upright = []
    for k, r in enumerate(rows, 1):
        c, s = Fr(*r[2]), Fr(*r[3])
        if c * s == 0:
            continue
        a, b = abs(c), abs(s)
        lo, hi = (a, b) if a < b else (b, a)
        deg = math.degrees(math.atan2(float(lo), float(hi)))
        if deg < 1:
            near_upright.append({"square": k, "degrees": f"{deg:.6e}", "tan_sci": F.sci(lo / hi, 6)})
    clear = [A.clearances(p, side) for p in ip]
    touching = {w: [k + 1 for k in range(n) if clear[k][i] == 0] for i, w in enumerate(("left", "bottom", "right", "top"))}
    return {
        "side": F.exact(S),
        "extent": F.exact(ext),
        "extent_floor_20": F.floor_places(ext, 20),
        "side_less_extent_sci": F.sci(S - ext, 8),
        "side_is_extent_rounded_up_at_places": k_up,
        "extent_terminates_at_places": F.terminating_places(ext),
        "walls_touched": touching,
        "near_pairs_below_1e-3": len(margins),
        "near_pair_margins_by_decade": dict(sorted(bands.items(), key=lambda t: int(t[0]) if t[0] != "0" else -999)),
        "tightest_pairs": [{"pair": list(p), "margin_sci": F.sci(m, 8)} for m, p in margins[:12]],
        "distinct_near_margins": len({m for m, _ in margins}),
        "one_less_contact_factor_least_sci": F.sci(min(factors), 6) if factors else None,
        "one_less_contact_factor_greatest_sci": F.sci(max(factors), 6) if factors else None,
        "turned_by_less_than_one_degree": near_upright,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 6:
        print(__doc__)
        return 2
    t305 = R.read_form_c(Path(argv[1]).read_bytes())
    out = {"program": "rb127_describe.py",
           "T-305": describe([T.pose_of_corners(c) for c in t305["corners"]], t305["side"])}
    for label, path in zip(("1015", "1017", "1020"), argv[2:5], strict=True):
        J = R.read_form_j(Path(path).read_bytes())
        out[label] = describe(J["rows"], J["side"])
    Path(argv[5]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    for k, v in out.items():
        if k != "program":
            print(k, v["side_less_extent_sci"], v["side_is_extent_rounded_up_at_places"], v["near_pair_margins_by_decade"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
