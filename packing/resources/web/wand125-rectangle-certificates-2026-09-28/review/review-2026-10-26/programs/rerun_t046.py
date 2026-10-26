#!/usr/bin/env python3
"""Single directions of T-046 census rows, re-run with a sqverify-fast binary.

Written for the stage 4 review of T-046 (bead think-buaj). For each selected
certificate and direction it runs the binary at one thread at Tokoharu's threshold, with
`--confirm`, as the census does, and compares every field of the direction's row with
the census receipt's, apart from timings. It records the binary's SHA-256, so the
receipt says which build re-ran them.

Usage, from packing/:
  .venv/bin/python3 -I PROGRAMS/rerun_t046.py --packing . \
    --binary sqverify_fast/target/release/sqverify-fast --out OUT.json
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from certificates_t046 import write_report  # noqa: E402

CENSUS = "benchmarks/measure-verifier/census"
WEB = "resources/web"
#: (certificate, packet, directions): the largest side and a row re-run on 25 October;
#: the most orbits, a row of 3 October; the n - 1/1000 certificate at the axis and at its
#: control direction; and the least certified bound of the 46.
SELECTED = [
    ("rect_n95_L98418", "2026-09-28", "least,200"),
    ("rect_n72_L874", "2026-09-28", "least"),
    ("rect_n27_L56", "2026-09-27", "0,197"),
    ("rect_n94_L9795", "2026-09-28", "least"),
]
TIMING = {"seconds", "cpu_seconds", "wall_seconds", "elapsed", "time"}


def receipt_rows(path: Path) -> dict[int, dict]:
    rows = [json.loads(line) for line in gzip.decompress(path.read_bytes()).splitlines()]
    return {int(row["r"]): row for row in rows if "r" in row}


def strip(row: dict) -> dict:
    return {key: value for key, value in row.items() if key not in TIMING}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--packing", type=Path, required=True)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    packing = args.packing.resolve()
    binary = args.binary.resolve()
    census = json.loads((packing / CENSUS / "census.json").read_text(encoding="utf-8"))["cases"]
    results = []
    for name, packet, spec in SELECTED:
        row = census[name]
        receipts = receipt_rows(packing / CENSUS / packet / f"{name}.jsonl.gz")
        least = min((r for r in receipts if r >= 1), key=lambda r: receipts[r]["min_certified_lower_bound"])
        directions = [least if part == "least" else int(part) for part in spec.split(",")]
        candidate = (
            packing / WEB / f"wand125-rectangle-certificates-{packet}"
            / "wand125-rectangles/certificates" / name / "certified_candidate.json.gz"
        )
        for r in directions:
            argv = [
                str(binary), "--candidate", str(candidate), "--n", str(row["n"]),
                "--side", row["L"], "--directions", str(r), "--threshold", "10001/10000",
                "--threads", "1", "--confirm",
            ]
            start = time.monotonic()
            done = subprocess.run(argv, capture_output=True, text=True, check=False)
            wall = time.monotonic() - start
            lines = [json.loads(line) for line in done.stdout.splitlines() if line.strip()]
            (fresh,) = [line for line in lines if "r" in line]
            summary = next(line for line in lines if line.get("kind") == "sqverify-fast-summary/v1")
            differs = sorted(
                key
                for key in set(strip(fresh)) | set(strip(receipts[r]))
                if strip(fresh).get(key) != strip(receipts[r]).get(key)
            )
            results.append({
                "certificate": name,
                "r": r,
                "returncode": done.returncode,
                "verdict": fresh["verdict"],
                "nodes": fresh.get("nodes"),
                "min_certified_lower_bound": fresh.get("min_certified_lower_bound"),
                "fields_compared": len(strip(fresh)),
                "fields_differing": differs,
                "summary_build": summary.get("build"),
                "wall_seconds": round(wall, 2),
            })
            print(f"{name} r={r}: {fresh['verdict']} exit {done.returncode}, "
                  f"{len(strip(fresh))} fields, differing {differs or 'none'}, {wall:.1f}s", flush=True)
    report = {
        "kind": "t046-review-reruns/v1",
        "binary_sha256": hashlib.sha256(binary.read_bytes()).hexdigest(),
        "runs": results,
        "status": "PASS"
        if all(run["returncode"] == 0 and not run["fields_differing"] for run in results)
        else "FAIL",
    }
    write_report(args.out, report)
    print(f"{report['status']}: {len(results)} directions on binary {report['binary_sha256'][:8]}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
