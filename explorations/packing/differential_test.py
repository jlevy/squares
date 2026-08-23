#!/usr/bin/env python3
"""Differential test: sqsearch's pair energy against sqpack's validity predicate.

The two live in this repository and never meet. `sqsearch` owns move-loop *energy* --
`pair_depth` is a penetration metric, shaped for annealing, and it is allowed to differ
from a verdict in ways that do not matter to a search. `sqpack` owns *validity*. The one
thing that must hold between them is the boundary:

    pair_depth == 0   <=>   sqpack says separated (strictly or by exact contact)

If that ever drifts, a search would be optimising against a different notion of overlap
than the one the record is checked with, and nothing else in the pipeline would notice.
Pairs are generated near contact on purpose, because that is the only regime where a
disagreement could hide.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sqpack.verify import float_sign, separated  # noqa: E402

BIN = Path(__file__).resolve().parent / "sqsearch/target/release/sqsearch"
TOL = 1e-12


def corners(x: float, y: float, t: float) -> list[tuple[float, float]]:
    """The four corners of a unit square, in the order sqpack expects."""
    c, s = math.cos(t), math.sin(t)
    ux, uy = 0.5 * c, 0.5 * s
    vx, vy = -0.5 * s, 0.5 * c
    return [
        (x - ux - vx, y - uy - vy),
        (x + ux - vx, y + uy - vy),
        (x + ux + vx, y + uy + vy),
        (x - ux + vx, y - uy + vy),
    ]


def main() -> int:
    pairs = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    out = subprocess.run(
        [str(BIN), "--pairdump", "--pairs", str(pairs)],
        capture_output=True, text=True, check=True,
    ).stdout

    sign = float_sign(TOL)
    disagreements, contacts, overlaps = [], 0, 0
    rows = [json.loads(line) for line in out.splitlines()]
    for row in rows:
        a = corners(row["xi"], row["yi"], row["ti"])
        b = corners(row["xj"], row["yj"], row["tj"])
        verdict = separated(a, b, sign)          # 1 strict, 0 exact contact, None overlap
        search_says_clear = row["depth"] <= TOL
        oracle_says_clear = verdict is not None
        if search_says_clear != oracle_says_clear:
            disagreements.append((row, verdict))
        overlaps += verdict is None
        contacts += verdict == 0

    print(f"  {len(rows)} near-contact pairs: {overlaps} overlapping, {contacts} touching")
    if disagreements:
        print(f"  DISAGREEMENTS: {len(disagreements)}")
        for row, verdict in disagreements[:5]:
            print(f"    depth={row['depth']:.3e} oracle={verdict} {row}")
        return 1
    print("  sqsearch pair energy and sqpack validity agree on every pair")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
