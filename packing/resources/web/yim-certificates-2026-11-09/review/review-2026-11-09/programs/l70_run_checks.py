"""Run l70_check.py over every certificate this review decides, two at a time.

Usage::

    python -I l70_run_checks.py --src SRC --repo REPO --out OUT [--workers 2] [--only LABEL ...]

SRC holds the two extracted trees of vitamoon/vitamoon, ``SRC/ac14112/`` and
``SRC/78eb9ea/``. REPO is a checkout of jlevy/squares at ``ef1af4933`` (the
predecessors' retained files). Each job writes ``OUT/check-LABEL.json``.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
BH = (553, 599, 600, 601, 602, 604, 645, 647, 648, 699, 700)
WEB = "packing/resources/web"


def jobs(src: Path, repo: Path) -> list[tuple[str, str, Path]]:
    out: list[tuple[str, str, Path]] = []
    head = src / "ac14112"
    out.append(("yim-n130", "cert", head / "n130.cert"))
    out.append(("yim-n299", "cert", head / "n299.cert"))
    out.append(("yim-n303", "cert", head / "n303.cert"))
    out.append(("yim-n303-first", "cert", src / "78eb9ea" / "n303.cert"))
    for n in BH:
        out.append((f"yim-n{n}", "cert", head / f"n{n}.cert"))
    out.append(("house-t277-n299", "corners", repo / WEB / "ozden-s299-upper-bound-2026-11-09/source/n-299-candidate.yaml"))
    out.append(("house-t278-n303", "corners", repo / WEB / "ozden-s303-upper-bound-2026-11-09/source/n-303-candidate.yaml"))
    out.append(("house-t259-n130", "cert", repo / WEB / "mishapolk-issue846-2026-10-30/source/certificates/0000-0999/n130.cert"))
    for n in BH:
        if n == 604:
            p = repo / WEB / "couzo-43f666c-2026-10-24/source/certificates/best/n604.cert"
        else:
            p = repo / WEB / f"couzo-issue763-2026-10-23/source/certificates/best/n{n}.cert"
        out.append((f"couzo-n{n}", "cert", p))
    return out


def run(job: tuple[str, str, Path], out: Path) -> tuple[str, float, str]:
    label, fmt, path = job
    t0 = time.time()
    cmd = [
        "nice", "-n", "19", sys.executable, "-I", "-B", str(HERE / "l70_check.py"), str(path),
        "--format", fmt, "--label", label, "--out", str(out / f"check-{label}.json"),
    ]
    p = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return label, time.time() - t0, (p.stdout + p.stderr).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--only", nargs="*")
    ns = ap.parse_args()
    if ns.workers > 2:
        raise SystemExit("at most two workers")
    out = Path(ns.out)
    out.mkdir(parents=True, exist_ok=True)
    todo = [j for j in jobs(Path(ns.src), Path(ns.repo)) if not ns.only or j[0] in ns.only]
    with ThreadPoolExecutor(max_workers=ns.workers) as ex:
        for label, wall, text in ex.map(lambda j: run(j, out), todo):
            print(f"[{wall:7.1f}s wall] {text}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
