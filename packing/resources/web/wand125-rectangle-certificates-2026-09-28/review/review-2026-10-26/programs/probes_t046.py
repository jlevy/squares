#!/usr/bin/env python3
"""Exact captures of T-046's 46 standing certificates, by this review's own evaluator.

Written for the stage 4 review of T-046 (bead think-buaj). It samples coverage; it
decides no direction. With `exact_capture_t046` (written from SOUNDNESS.md's density
alone), for each certificate it:

- recomputes the control receipt's capture at its centre, and each mutant's capture at
  its refusal's witness (the factor times the original's capture there), and requires
  them equal, as exact rationals, to the receipt's;
- recomputes the census row's least-bound leaf capture and requires it equal;
- evaluates all 200 oblique least-bound leaf centres of the census receipts and checks
  that the control's index is the least (finding FT-11 of the format T route review);
- evaluates the corner (L - a_r, L - a_r) of Tokoharu's quarter domain at all 201
  directions, and 201 seeded uniform poses in that quarter, one per direction;
- runs a seeded local search, from the least of those poses, for a pose that captures
  less than 10001/10000.

Any pose in the domain with exact capture below 10001/10000 would contradict the census
row and the source's accepting run, and one below 1 would contradict the bound.

Usage, from packing/:
  .venv/bin/python3 -I PROGRAMS/probes_t046.py --packing . --out OUT.json [--workers 2]
"""

from __future__ import annotations

import argparse
import gzip
import json
import random
import sys
import time
from fractions import Fraction as Q
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import exact_capture_t046 as ec  # noqa: E402
from certificates_t046 import STANDING, write_report  # noqa: E402

CENSUS = "benchmarks/measure-verifier/census"
WEB = "resources/web"
THRESHOLD = Q(10001, 10000)
DIRECTIONS = 201
SEED = 20261026
SEARCH_STEPS = 120


def clamp(value: Q, low: Q, high: Q) -> Q:
    return min(max(value, low), high)


def probe(job: tuple[str, str, str]) -> dict:
    packing_text, packet, name = job
    packing = Path(packing_text)
    started = time.process_time()
    path = (
        packing / WEB / f"wand125-rectangle-certificates-{packet}"
        / "wand125-rectangles/certificates" / name / "certified_candidate.json.gz"
    )
    g = ec.density(ec.load(path))
    census = json.loads((packing / CENSUS / "census.json").read_text(encoding="utf-8"))["cases"][name]
    control = json.loads((packing / CENSUS / packet / f"{name}.control.json").read_text(encoding="utf-8"))
    rows = [
        json.loads(line)
        for line in gzip.decompress((packing / CENSUS / packet / f"{name}.jsonl.gz").read_bytes()).splitlines()
    ]
    failed: list[str] = []
    index = control["index"]
    at_centre = ec.capture(g, index, ec.pose(control["centre"]))
    if not (at_centre == Q(control["exact_capture_independent"]) == Q(control["exact_capture_crate"])):
        failed.append("control centre capture differs from the receipt")
    witnesses: dict[str, str] = {}
    for run in control["runs"]:
        mutation = run.get("mutation")
        if mutation is None:
            continue
        factor = Q(mutation["factor"])
        if factor * at_centre != Q(mutation["capture_at_centre"]):
            failed.append(f"{run['name']}: capture at centre differs")
        witness = run.get("witness")
        if witness and mutation.get("capture_at_witness") is not None:
            value = factor * ec.capture(g, index, ec.pose(witness["exact_pose"]))
            if value != Q(mutation["capture_at_witness"]) or value != Q(witness["exact_coverage"]):
                failed.append(f"{run['name']}: capture at witness differs")
            witnesses[run["name"]] = str(float(value))
    least = census["least_bound_leaf_exact"]
    leaf = ec.capture(g, int(least["r"]), ec.pose(least["centre"]))
    if leaf != Q(least["exact_coverage"]):
        failed.append("census least-bound leaf capture differs")
    # FT-11: every oblique least-bound leaf centre, by exact capture.
    scan: list[tuple[Q, int]] = []
    for row in rows:
        if "r" in row and int(row["r"]) >= 1:
            box = row["least_bound_box"]
            scan.append((ec.capture(g, int(row["r"]), ec.pose([box["x"], box["y"]])), int(row["r"])))
    scan.sort()
    tightest = scan[0]
    if tightest[1] != index or tightest[0] != at_centre:
        failed.append(f"FT-11: the least of the 200 centres is index {tightest[1]}, not {index}")
    if any(value < THRESHOLD for value, _ in scan):
        failed.append("a least-bound leaf centre captures below the threshold")
    # Corners and uniform poses of the quarter domain at every direction.
    rng = random.Random(f"{SEED}-{name}")
    half = g.side / 2
    lowest: tuple[Q, int, ec.Point] | None = None
    corner_min: tuple[Q, int] | None = None
    uniform_min: tuple[Q, int] | None = None
    for r in range(DIRECTIONS):
        a = ec.half_extent(g.core, r)
        top = g.side - a
        corner = ec.capture(g, r, (top, top))
        if corner_min is None or corner < corner_min[0]:
            corner_min = (corner, r)
        point = (
            half + Q(rng.randrange(2**30 + 1), 2**30) * (top - half),
            half + Q(rng.randrange(2**30 + 1), 2**30) * (top - half),
        )
        value = ec.capture(g, r, point)
        if uniform_min is None or value < uniform_min[0]:
            uniform_min = (value, r)
        for candidate in ((corner, r, (top, top)), (value, r, point)):
            if lowest is None or candidate[0] < lowest[0]:
                lowest = candidate
    assert lowest is not None and corner_min is not None and uniform_min is not None
    # A local search from the least sampled pose, and from the tightest leaf centre.
    searched: list[tuple[Q, int]] = []
    for start in (lowest, (tightest[0], tightest[1], ec.pose(control["centre"]))):
        value, r, (x, y) = start
        a = ec.half_extent(g.core, r)
        low, high = half, g.side - a
        step = (high - low) / 8
        for _ in range(SEARCH_STEPS):
            trial = (
                clamp(x + step * Q(rng.randrange(-1024, 1025), 1024), low, high),
                clamp(y + step * Q(rng.randrange(-1024, 1025), 1024), low, high),
            )
            found = ec.capture(g, r, trial)
            if found < value:
                value, (x, y) = found, trial
            else:
                step = step * Q(7, 8)
        searched.append((value, r))
    search_min = min(searched)
    sampled_min = min(corner_min[0], uniform_min[0], search_min[0], tightest[0])
    if sampled_min < THRESHOLD:
        failed.append(f"a sampled pose captures {float(sampled_min)} < 10001/10000")
    return {
        "certificate": name,
        "packet": packet,
        "control_index": index,
        "control_capture": float(at_centre),
        "witness_captures": witnesses,
        "least_leaf_capture": float(leaf),
        "ft11_tightest": [tightest[1], float(tightest[0])],
        "ft11_next": [scan[1][1], float(scan[1][0])],
        "corner_min": [corner_min[1], float(corner_min[0])],
        "uniform_min": [uniform_min[1], float(uniform_min[0])],
        "search_min": [search_min[1], float(search_min[0])],
        "sampled_min": float(sampled_min),
        "evaluations": 3 + 200 + 2 * DIRECTIONS + 2 * SEARCH_STEPS + len(witnesses),
        "cpu_seconds": round(time.process_time() - started, 2),
        "failed": failed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--packing", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--only", default="")
    args = parser.parse_args()
    packing = str(args.packing.resolve())
    only = {name for name in args.only.split(",") if name}
    jobs = [
        (packing, packet, name)
        for packet, names in STANDING.items()
        for name in names
        if not only or name in only
    ]
    with Pool(args.workers) as pool:
        results = []
        for result in pool.imap(probe, jobs):
            results.append(result)
            print(
                f"{result['certificate']:17} control r={result['control_index']} "
                f"FT-11 {result['ft11_tightest'][0]} sampled min {result['sampled_min']:.10f} "
                f"cpu {result['cpu_seconds']}s {'; '.join(result['failed']) or 'ok'}",
                flush=True,
            )
    report = {
        "kind": "t046-review-probes/v1",
        "seed": SEED,
        "rows": results,
        "evaluations": sum(row["evaluations"] for row in results),
        "cpu_seconds": round(sum(row["cpu_seconds"] for row in results), 1),
        "sampled_min": min((row["sampled_min"], row["certificate"]) for row in results),
        "failed": sum(len(row["failed"]) for row in results),
    }
    report["status"] = "PASS" if report["failed"] == 0 else "FAIL"
    write_report(args.out, report)
    print(f"{report['status']}: {len(results)} certificates, {report['evaluations']} exact captures, "
          f"{report['cpu_seconds']} CPU s, least sampled {report['sampled_min']}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
