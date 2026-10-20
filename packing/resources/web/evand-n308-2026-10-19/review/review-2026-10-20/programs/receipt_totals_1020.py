"""Sum the two packets' retained receipts: jobs, outcomes, pair decisions, route CPU and
job wall seconds, and the margins both routes state.

Written for the stage 4 review of 20 October 2026. It reads each receipt as data and
decides nothing; the maintained ``check --replay`` decided them again on this review's
run. A pair decision counts each pair once per route per job, 2 * C(n, 2) per job, which
is how the packets' READMEs count them.

Usage, from ``packing/``::

    python -I receipt_totals_1020.py --json OUT.json
"""

from __future__ import annotations

import argparse
import json
import lzma
import sys
from pathlib import Path

WEB = Path("resources/web")
PACKETS = ("evand-n308-2026-10-19", "evand-n154-sweep-2026-10-20")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args(argv)
    report: dict[str, object] = {}
    for name in PACKETS:
        receipt = json.loads(lzma.decompress((WEB / name / "receipts/exact-certification.json.xz").read_bytes()))
        jobs = []
        cpu = 0.0
        wall = 0.0
        pairs = 0
        for case in receipt["cases"]:
            n = case["n"]
            routes = receipt["routes"]
            outcome = {
                route: ("accepted" if not case[route]["failures"] else "refused: " + json.dumps(case[route]["failures"])[:90])
                for route in routes
            }
            jobs.append({"control": case["control"], "n": n, "outcome": outcome, "wall": round(case["wall_seconds"], 2), "cpu": {r: round(case["cpu_seconds"][r], 2) for r in routes}})
            cpu += sum(case["cpu_seconds"].values())
            wall += case["wall_seconds"]
            pairs += len(routes) * n * (n - 1) // 2
        positive = next(case for case in receipt["cases"] if case["control"] == "positive")
        report[name] = {
            "format": receipt["format"],
            "jobs": jobs,
            "pair_decisions": pairs,
            "route_cpu_seconds": round(cpu, 2),
            "job_wall_seconds": round(wall, 2),
            "longest_job_wall": round(max(case["wall_seconds"] for case in receipt["cases"]), 2),
            "margins": {
                route: {
                    "containment_clearance": positive[route].get("minimum_containment_clearance"),
                    "best_pair_gap": positive[route].get("minimum_best_pair_gap"),
                }
                for route in receipt["routes"]
            },
        }
        print(json.dumps({name: report[name]}, indent=1), flush=True)
    args.json.write_text(json.dumps(report, indent=1) + "\n", "utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
