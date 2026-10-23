"""Run the bounds probe clean at scale and under each deliberate mutation; one receipt.

The clean runs must find no failure. Each mutation (``bounds_probe.MUTATIONS``) is one
deliberate error in the transcribed bound; the suite records whether the probe detects
it, which is what shows the probe can see an error of that kind. A mutation the probe
does not detect is reported as such, with no claim made for it.

Usage::

    python -I probe_suite.py --density c6715.json > probe-suite.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bounds_probe  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--density", type=Path, required=True)
    parser.add_argument("--seeds", type=int, nargs="+", default=[11, 12, 13])
    parser.add_argument("--boxes", type=int, default=900)
    parser.add_argument("--density-boxes", type=int, default=120)
    parser.add_argument("--mutation-boxes", type=int, default=150)
    args = parser.parse_args()
    clean = [bounds_probe.run_probe(seed, args.boxes, 24, 6, args.density, args.density_boxes, None)
             for seed in args.seeds]
    mutations = {}
    for name in bounds_probe.MUTATIONS:
        r = bounds_probe.run_probe(2, args.mutation_boxes, 16, 6, None, 0, name)
        mutations[name] = {"detected": r["failure_count"] > 0, "failures": r["failures"], "boxes": r["boxes"]}
    totals: dict[str, int] = {}
    for r in clean:
        for k, v in r["checks"].items():
            totals[k] = totals.get(k, 0) + v
    receipt = {
        "clean_runs": clean,
        "clean_checks_total": totals,
        "clean_failures_total": sum(r["failure_count"] for r in clean),
        "mutations": mutations,
        "mutations_detected": sum(1 for m in mutations.values() if m["detected"]),
        "mutations_total": len(mutations),
    }
    json.dump(receipt, sys.stdout, indent=2, default=str)
    print()
    return 0 if receipt["clean_failures_total"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
