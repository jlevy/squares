"""Lane L109's census of the accepted certificate's margins and wall clearances by decade.

Usage: python -I -B l109_census.py CERT.yaml TWIN.json OUT.json

Decides nothing: it reads the certificate with the frozen reader, computes every pair
margin and wall clearance with method A's arithmetic, and reports how many lie in each
decade from 1e-17 to 1, with the extremes of each, so the review can describe the margins
the check accepted.
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction as Q

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l109_axes as A  # noqa: E402
import l109_check as C  # noqa: E402
import l109_reader as R  # noqa: E402

PROGRAMS = ["l109_reader.py", "l109_axes.py", "l109_check.py", "l109_census.py"]


def decade(v: Q) -> int:
    k = 0
    while v < Q(1, 10**k) and k < 40:
        k += 1
    return k  # v in [1e-k, 1e-(k-1))


def main() -> int:
    cert, twin, out = sys.argv[1:4]
    rd = R.read_files(cert, twin)
    side = Q(*rd.side)
    sq = [A.make([(Q(*x), Q(*y)) for x, y in s]) for s in rd.corners]
    n = len(sq)
    pairs: dict[int, list[tuple[Q, int, int]]] = {}
    for i in range(n):
        for j in range(i + 1, n):
            m = A.margin(sq[i], sq[j])
            if 0 < m < 1:
                pairs.setdefault(decade(m), []).append((m, i + 1, j + 1))
    walls: dict[int, list[tuple[Q, int, str]]] = {}
    for i in range(n):
        for w, v in A.walls(sq[i], side).items():
            if 0 < v < 1:
                walls.setdefault(decade(v), []).append((v, i + 1, w))

    def rows(d: dict[int, list[tuple[Q, int, object]]]) -> list[dict[str, object]]:
        out_rows = []
        for k in sorted(d, reverse=True):
            vals = sorted(d[k])
            out_rows.append(
                {
                    "decade": f"[1e-{k}, 1e-{k - 1})",
                    "count": len(vals),
                    "least": [vals[0][1], vals[0][2], f"{float(vals[0][0]):.6e}"],
                    "greatest": [vals[-1][1], vals[-1][2], f"{float(vals[-1][0]):.6e}"],
                    "members": [[v[1], v[2], f"{float(v[0]):.6e}"] for v in vals] if len(vals) <= 6 else None,
                }
            )
        return out_rows

    receipt = {
        "program": "l109_census.py",
        "programs_sha256": C.program_digests(PROGRAMS),
        "decides": "nothing",
        "pair_margins_below_1": rows(pairs),  # type: ignore[arg-type]
        "positive_wall_clearances_below_1": rows(walls),  # type: ignore[arg-type]
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=1)
        f.write("\n")
    print("census written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
