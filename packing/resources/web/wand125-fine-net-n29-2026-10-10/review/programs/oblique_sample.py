"""Run oblique_decide.py over a list of directions, at most JOBS at a time, keep
each direction's receipt and write a summary (review think-1lri).  It decides
nothing itself: each verdict is oblique_decide's.

Usage: python3 -I oblique_sample.py CANDIDATE.json[.gz] OUTDIR --directions a,b,c
       [--scale 1] [--jobs 2] [--domain full] [--tag NAME] [--crate-log RUN.jsonl.gz]
With --crate-log, each direction's row of the source's run log is set beside it
(nodes, least certified bound, CPU), for comparison only.
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate", type=Path)
    ap.add_argument("outdir", type=Path)
    ap.add_argument("--directions", required=True)
    ap.add_argument("--scale", default="1")
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--domain", default="full")
    ap.add_argument("--tag", default="oblique")
    ap.add_argument("--crate-log", type=Path)
    ap.add_argument("--timeout", type=int, default=1700)
    args = ap.parse_args()
    dirs = [int(x) for x in args.directions.split(",") if x]
    args.outdir.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1")
    crate = {}
    if args.crate_log:
        with gzip.open(args.crate_log, "rt") as fh:
            for line in fh:
                if line.startswith("{"):
                    row = json.loads(line)
                    if "r" in row:
                        crate[row["r"]] = {k: row.get(k) for k in ("nodes", "min_certified_lower_bound", "cpu_seconds")}

    def one(r):
        out = args.outdir / f"{args.tag}-r{r:04d}.json"
        cmd = [sys.executable, "-I", str(HERE / "oblique_decide.py"), str(args.candidate), str(r),
               "--domain", args.domain, "--scale", args.scale, "--out", str(out)]
        t = time.time()
        p = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=args.timeout)
        res = json.loads(out.read_text()) if out.exists() else {"status": "NO_OUTPUT", "stderr": p.stderr[-500:]}
        return r, p.returncode, time.time() - t, res

    t0 = time.time()
    rows = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for r, code, wall, res in pool.map(one, dirs):
            lc = res.get("least_centre_exact") or {}
            rows.append({"r": r, "status": res.get("status"), "exit": code, "boxes": res.get("boxes"),
                         "max_depth": res.get("max_depth_accepted"), "least_accepted": res.get("least_accepted_lower_bound"),
                         "least_capture_found_exact": lc.get("exact_approx"), "least_capture_at": lc.get("centre"),
                         "witness": res.get("witness"), "cpu_seconds": res.get("cpu_seconds"), "wall_seconds": wall,
                         "crate": crate.get(r)})
            print(json.dumps(rows[-1]), flush=True)
    summary = {
        "candidate": str(args.candidate), "scale": args.scale, "domain": args.domain, "directions": dirs,
        "statuses": {s: sum(1 for x in rows if x["status"] == s) for s in sorted({x["status"] for x in rows})},
        "cpu_seconds": sum(x["cpu_seconds"] or 0 for x in rows), "wall_seconds": time.time() - t0,
        "least_capture_found": min((x["least_capture_found_exact"] for x in rows if x["least_capture_found_exact"]), default=None),
        "rows": sorted(rows, key=lambda x: x["r"]),
    }
    (args.outdir / f"{args.tag}-summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "rows"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
