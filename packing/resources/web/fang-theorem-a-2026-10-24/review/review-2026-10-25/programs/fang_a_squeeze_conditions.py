#!/usr/bin/env python3
"""Which closeness conditions fail in finding M-1's example (k = 43218), exactly.

Stage 4 review of issue #797, lane c-review-797-math, 25 October 2026. Written after the
review's findings and after its author read the maintained fang_theorem_a.py, to record a
detail of finding M-1 that fang_a_review.py's `squeeze` receipt states only as
close = false: which of conditions (a) to (d) fail at k - S = 10^-7, at t - 1/b = 10^-7,
and at every point of the same log scan of k - S from 1e-9 to 1e-5 where the waste reaches
4 sqrt(2k) + 2 = 1178. It imports fang_a_review.py (unchanged since it decided) for the
construction and decides nothing about the theorem.

    python3 -I fang_a_squeeze_conditions.py --out squeeze-conditions.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction as Q
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fang_a_review as R  # noqa: E402

K = 43218


def t_for_squeeze(b: int, e: Q) -> Q:
    """The t with b - W(t) = e, to a rational square root truncated at 50 digits."""
    disc = 1 + e * (2 * b - e)
    scale = 10**50
    return (1 + Q(math.isqrt(int(disc * scale * scale)), scale)) / (2 * b - e)


def failing(b: int, t: Q) -> list[str]:
    return [name for name, ok in R.close(R.angle(b, t)).items() if not ok]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    rows = []
    for b in R.odd_widths(K):
        t1 = t_for_squeeze(b, Q(1, 10**7))
        t2 = Q(1, b) + Q(1, 10**7)
        sets: dict[str, int] = {}
        reached = 0
        for j in range(1, 401):
            ex = -9 + 4 * j / 400
            e = Q(int(10 ** (ex + 30)), 10**30)
            t = t_for_squeeze(b, e)
            p = R.evaluate(K, b, t)
            if p.w >= 1178:
                reached += 1
                key = ",".join(failing(b, t)) or "none"
                sets[key] = sets.get(key, 0) + 1
        rows.append({
            "b": b,
            "k_minus_S_1e-7": {"failing": failing(b, t1), "w": R.evaluate(K, b, t1).w},
            "t_minus_1/b_1e-7": {"failing": failing(b, t2), "w": R.evaluate(K, b, t2).w},
            "scan_points_with_w_at_least_1178": reached,
            "failing_sets_at_those_points": sets,
        })
    receipt = {
        "program": Path(__file__).name,
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "imports": {"fang_a_review.py": hashlib.sha256(
            (Path(__file__).resolve().parent / "fang_a_review.py").read_bytes()).hexdigest()},
        "python": sys.version.split()[0],
        "k": K,
        "rows": rows,
    }
    args.out.write_text(json.dumps(receipt, indent=1) + "\n")
    for row in rows:
        print(row)
    return 0


if __name__ == "__main__":
    sys.exit(main())
