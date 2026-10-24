"""The stratified sample of net directions that capture.py decides, fixed in advance.

Usage: python3 -I sample_plan.py CANDIDATE RUN_LOG STRATA OUTPUT.json

The plan, chosen before any of its directions ran:

- strata: the directions 1 .. last split into STRATA runs of near-equal length, one
  direction drawn uniformly from each with a generator seeded by the first 16 hex
  digits of the candidate's SHA-256 (so anyone can redraw it);
- fixed: the axis direction 0, the two smallest angles 1 and 2, the middle of the net,
  the last two directions (the last tangent is past tan(pi/8)), the six directions the
  intake lane's diagnostic ran (296 ... 1776), the twelve directions with the smallest
  least certified bound in the source's run log, and the four with the most nodes.

Reads the source's run log only to name the fixed directions; the decisions do not use
it. Writes the plan and prints the directions in run order.
"""

from __future__ import annotations

import gzip
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import n31_exact as nx  # noqa: E402


def main() -> int:
    cand = nx.read_candidate(Path(sys.argv[1]))
    rows = [json.loads(line) for line in gzip.open(sys.argv[2], "rt")]
    strata = int(sys.argv[3])
    out = Path(sys.argv[4])
    last = cand["last"]
    seed = int(cand["sha256"][:16], 16)
    rng = random.Random(seed)
    drawn = []
    lo = 1
    for k in range(strata):
        hi = 1 + ((k + 1) * last) // strata - 1
        drawn.append(rng.randint(lo, hi))
        lo = hi + 1
    dirs = [r for r in rows if "r" in r]
    tight = [r["r"] for r in sorted(dirs, key=lambda r: r["min_certified_lower_bound"])[:12]]
    heavy = [r["r"] for r in sorted((r for r in dirs if r.get("nodes")),
                                    key=lambda r: -r["nodes"])[:4]]
    fixed = sorted({0, 1, 2, last // 2, last - 1, last, 296, 592, 888, 1184, 1480, 1776,
                    *tight, *heavy})
    order = sorted(set(drawn) | set(fixed))
    plan = {"kind": "review-2026-10-23-n31-sample-plan/v1", "seed": seed,
            "seed_rule": "int(candidate_sha256[:16], 16)", "strata": strata,
            "drawn": drawn, "fixed": fixed, "source_tightest_12": tight,
            "source_most_nodes_4": heavy, "directions": order, "count": len(order),
            "program_sha256": nx.sha256_file(Path(__file__))}
    out.write_text(json.dumps(plan, indent=1) + "\n")
    print(" ".join(str(j) for j in order))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
