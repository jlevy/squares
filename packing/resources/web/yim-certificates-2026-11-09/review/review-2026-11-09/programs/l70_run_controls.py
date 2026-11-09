"""Run l70_controls.py over every file of the frozen plan, at most two at a time.

Usage: python -I l70_run_controls.py --src SRC --plan controls-plan.json --checks OUTDIR --out OUTDIR [--only LABEL ...]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--checks", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--only", nargs="*")
    ns = ap.parse_args()
    if ns.workers > 2:
        raise SystemExit("at most two workers")
    labels = [k for k in json.loads(Path(ns.plan).read_text())["files"] if not ns.only or k in ns.only]

    def one(label: str) -> str:
        t0 = time.time()
        cmd = ["nice", "-n", "19", sys.executable, "-I", "-B", str(HERE / "l70_controls.py"), "--src", ns.src, "--plan", ns.plan,
               "--label", label, "--checks", ns.checks, "--out", str(Path(ns.out) / f"controls-{label}.json")]
        p = subprocess.run(cmd, capture_output=True, text=True, check=False)
        last = (p.stdout.strip().splitlines() or [""])[-1]
        return f"[{time.time() - t0:7.1f}s wall] {last} {p.stderr.strip()[-400:]}"

    with ThreadPoolExecutor(max_workers=ns.workers) as ex:
        for line in ex.map(one, labels):
            print(line, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
