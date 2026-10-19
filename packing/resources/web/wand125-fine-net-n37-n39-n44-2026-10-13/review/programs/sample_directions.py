"""A sample of directions run by the reviewed sqverify-fast, judged by the exact evaluator here.

Usage::

    python3 -I sample_directions.py BINARY BINARY_SHA256 CANDIDATE.json N L \\
        [--log RUN.jsonl.gz] [--factor F] [--expect-source SRC_SHA256] R [R ...]

Runs the binary at each direction ``R`` with ``--confirm``, one thread, one at a time,
on the candidate or, with ``--factor``, on a copy with every mass scaled by ``F`` written
to the scratch directory beside the candidate. For a verified direction it recomputes the
exact capture at the least-bound leaf's centre here and compares the row with the
source's log; for a refusal it evaluates the crate's witness here on the scaled measure
and checks that it lies in the per-bin domain with a capture below one. CPU is the
child's, by ``wait4``. A sample decides only the directions it ran.
"""

from __future__ import annotations

import gzip
import json
import os
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fine_net_exact as exact


def run(
    binary: Path, candidate: Path, n: int, side: str, index: int
) -> tuple[dict[str, Any], dict[str, Any], int, float, float]:
    argv = [str(binary), "--candidate", str(candidate), "--n", str(n), "--side", side]
    argv += ["--directions", str(index), "--threads", "1", "--confirm"]
    before = os.times()
    start = time.monotonic()
    result = subprocess.run(argv, capture_output=True, text=True, check=False, timeout=3600)
    wall = time.monotonic() - start
    after = os.times()
    cpu = (after.children_user - before.children_user) + (
        after.children_system - before.children_system
    )
    lines = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
    row = next((line for line in lines if line.get("r") == index), {})
    summary = next(
        (line for line in lines if line.get("kind") == "sqverify-fast-summary/v1"), {}
    )
    return row, summary, result.returncode, cpu, wall


def scaled_copy(candidate: Path, factor: Fraction) -> Path:
    data = exact.load_json(candidate.read_bytes())
    for row in data["rectangles"]:
        row["mass"] = str(Fraction(row["mass"]) * factor)
    data["total_mass"] = str(
        sum((Fraction(row["mass"]) for row in data["rectangles"]), Fraction(0))
    )
    target = candidate.with_name(
        f"{candidate.stem}-scaled-{factor.numerator}-{factor.denominator}.json"
    )
    target.write_text(json.dumps(data), encoding="utf-8")
    return target


def judge(
    row: dict[str, Any], measure: exact.Measure, factor: Fraction, index: int
) -> dict[str, Any]:
    low, high = exact.domain(measure.side, measure.step, index)
    verdict = row.get("verdict")
    if verdict == "verified":
        box = row.get("least_bound_box")
        if index == 0 or not box:
            pose = row.get("argmin")
            x, y = (Fraction(value) for value in pose) if pose else (None, None)
        else:
            x, y = Fraction(box["x"]), Fraction(box["y"])
        if x is None or y is None:
            return {"pose": None}
        value = factor * exact.capture(measure, x, y, index)
        return {
            "pose": [str(x), str(y)] if index == 0 else [box["x"], box["y"]],
            "in_domain": low <= x <= high and low <= y <= high,
            "exact_capture": float(value),
            "at_least_1": value >= 1,
            "at_least_certified_bound": value >= Fraction(row["min_certified_lower_bound"]),
        }
    witness = row.get("witness") or {}
    pose = row.get("argmin") if index == 0 else witness.get("exact_pose")
    if not pose:
        return {"pose": None}
    x, y = Fraction(pose[0]), Fraction(pose[1])
    value = factor * exact.capture(measure, x, y, index)
    crate = witness.get("exact_coverage")
    return {
        "pose": pose,
        "in_domain": low <= x <= high and low <= y <= high,
        "scaled_capture": float(value),
        "below_1": value < 1,
        "equals_crate_exact_coverage": crate is not None and Fraction(crate) == value,
        "crate_exact_below_threshold": witness.get("exact_below_threshold"),
        "original_capture_at_pose_at_least_1": value / factor >= 1,
    }


def main(argv: list[str]) -> int:
    binary, expected = Path(argv[1]), argv[2]
    candidate, n, side = Path(argv[3]), int(argv[4]), argv[5]
    rest = argv[6:]
    log: Path | None = None
    factor = Fraction(1)
    expect_source: str | None = None
    while rest and rest[0].startswith("--"):
        flag, value, rest = rest[0], rest[1], rest[2:]
        if flag == "--log":
            log = Path(value)
        elif flag == "--factor":
            factor = Fraction(value)
        elif flag == "--expect-source":
            expect_source = value
    indices = [int(value) for value in rest]
    if exact.sha256(binary.read_bytes()) != expected:
        msg = f"{binary} is not the binary {expected}"
        raise SystemExit(msg)
    original = exact.read_measure(exact.load_json(candidate.read_bytes()))
    logged: dict[int, dict[str, Any]] = {}
    if log is not None:
        with gzip.open(log, "rt", encoding="utf-8") as stream:
            logged = {int(line["r"]): line for line in map(json.loads, stream) if "r" in line}
    target = scaled_copy(candidate, factor) if factor != 1 else candidate
    rows = []
    builds = set()
    for index in indices:
        row, summary, code, cpu, wall = run(binary, target, n, side, index)
        builds.add(json.dumps(summary.get("build"), sort_keys=True))
        theirs = logged.get(index, {})
        rows.append(
            {
                "r": index,
                "returncode": code,
                "verdict": row.get("verdict"),
                "method": row.get("method"),
                "nodes": row.get("nodes"),
                "min_certified_lower_bound": row.get("min_certified_lower_bound"),
                "thread_cpu_seconds": row.get("cpu_seconds"),
                "process_cpu_seconds": cpu,
                "wall_seconds": wall,
                "judged_here": judge(row, original, factor, index),
                "source_log": {
                    "verdict": theirs.get("verdict"),
                    "nodes": theirs.get("nodes"),
                    "min_certified_lower_bound": theirs.get("min_certified_lower_bound"),
                    "cpu_seconds": theirs.get("cpu_seconds"),
                    "agrees": bool(theirs)
                    and theirs.get("verdict") == row.get("verdict")
                    and theirs.get("nodes") == row.get("nodes")
                    and theirs.get("min_certified_lower_bound")
                    == row.get("min_certified_lower_bound"),
                },
                "premises": summary.get("premises"),
            }
        )
    report = {
        "binary_sha256": expected,
        "build": json.loads(next(iter(builds))) if len(builds) == 1 else sorted(builds),
        "build_source_is_expected": expect_source is None
        or all(json.loads(build).get("source_sha256") == expect_source for build in builds),
        "candidate_sha256": exact.sha256(candidate.read_bytes()),
        "input_sha256": exact.sha256(target.read_bytes()),
        "factor": str(factor),
        "n": n,
        "L": side,
        "directions": indices,
        "rows": rows,
        "process_cpu_seconds": sum(row["process_cpu_seconds"] for row in rows),
        "load_average": os.getloadavg(),
    }
    sys.stdout.write(json.dumps(report, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
