"""Measure exact resident Rust singleton versus batch transport on fixed work.

This is a geometry transport diagnostic, not a verifier or packing proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import shutil
import subprocess
import time
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from statistics import median

from sqpack import rectangle_density, rust_rectangle_geometry
from sqpack.rectangle_density import ANGLE_STEP, load_candidate, square_polygon
from sqpack.rust_rectangle_geometry import RustRectangleGeometry

PROJECT = Path(__file__).resolve().parents[1]
CANDIDATE = (
    PROJECT
    / "resources/web/external-square-certificates-2026-09-22/tokoharu-density"
    / "certificates/cert_n11_L381/certified_candidate.json"
)
COUNT = 128
PAIRS = 3
MAX_SECONDS = 30
MAX_BUILD_SECONDS = 180
CRATE = PROJECT / "sqverify_exact"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _build_variants(target_root: Path) -> tuple[Path, Path, dict[str, object]]:
    """Build both experimental arms from this source, with one bounded toolchain."""
    if not all(os.environ.get(name) for name in ("TMPDIR", "UV_CACHE_DIR", "CARGO_TARGET_DIR")):
        raise ValueError("external TMPDIR, UV_CACHE_DIR, and CARGO_TARGET_DIR are required")
    if not target_root.is_absolute():
        raise ValueError("variant target root must be absolute and outside the source tree")
    target_root = target_root.resolve()
    if target_root.is_relative_to(PROJECT.parent):
        raise ValueError("variant target root must be absolute and outside the source tree")
    target_root.mkdir(parents=True, exist_ok=True)
    source_paths = (
        CRATE / "Cargo.toml",
        CRATE / "Cargo.lock",
        CRATE / "rust-toolchain.toml",
        CRATE / "src/lib.rs",
        CRATE / "src/main.rs",
    )
    source_before = {str(path): _sha(path) for path in source_paths}
    build_deadline = time.monotonic() + MAX_BUILD_SECONDS
    rustc = subprocess.run(
        ["rustc", "-vV"],
        cwd=CRATE,
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    ).stdout.strip()
    cargo_version = subprocess.run(
        ["cargo", "--version"],
        cwd=CRATE,
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    ).stdout.strip()
    binaries: dict[str, Path] = {}
    builds: list[dict[str, object]] = []
    for label, feature in (
        ("baseline", "experimental-normalized-mul"),
        ("candidate", "experimental-coprime-mul"),
    ):
        target = target_root / label
        target.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ)
        env["CARGO_TARGET_DIR"] = str(target)
        command = [
            "cargo",
            "build",
            "--offline",
            "--locked",
            "--release",
            "--no-default-features",
            "--features",
            feature,
        ]
        started = time.perf_counter()
        remaining = build_deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("experimental variant build exceeded 180 seconds")
        completed = subprocess.run(
            command,
            cwd=CRATE,
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=remaining,
        )
        if completed.returncode != 0:
            raise RuntimeError(f"{feature} build failed: {completed.stderr[-2000:]}")
        built = target / "release/sqverify-exact"
        binary = target_root / f"sqverify-exact-{label}"
        shutil.copy2(built, binary)
        binaries[label] = binary
        builds.append(
            {
                "label": label,
                "command": command,
                "feature": feature,
                "target_dir": str(target),
                "wall_seconds": time.perf_counter() - started,
                "binary_sha256": _sha(binary),
            }
        )
    if source_before != {str(path): _sha(path) for path in source_paths}:
        raise AssertionError("Rust source changed during experimental variant builds")
    if _sha(binaries["baseline"]) == _sha(binaries["candidate"]):
        raise AssertionError("experimental variant binaries have identical bytes")
    return (
        binaries["candidate"],
        binaries["baseline"],
        {
            "source_sha256": source_before,
            "rustc_version": rustc,
            "cargo_version": cargo_version,
            "rustflags": os.environ.get("RUSTFLAGS", ""),
            "cargo_encoded_rustflags": os.environ.get("CARGO_ENCODED_RUSTFLAGS", ""),
            "build_ceiling_seconds": MAX_BUILD_SECONDS,
            "builds": builds,
        },
    )


def _run(
    binary: Path,
    rectangles: tuple[rectangle_density.DensityRectangle, ...],
    polygons: tuple[rectangle_density.Polygon, ...],
    mode: str,
    deadline: float,
) -> tuple[tuple[Fraction, ...], dict[str, float]]:
    child_before = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu_before = time.process_time()
    wall_before = time.perf_counter()
    with RustRectangleGeometry(rectangles, binary, deadline=deadline) as engine:
        query_before = time.perf_counter()
        if mode == "singleton":
            values = tuple(engine.coverage(polygon) for polygon in polygons)
        else:
            values = engine.coverages(polygons)
        query_wall = time.perf_counter() - query_before
    child_after = resource.getrusage(resource.RUSAGE_CHILDREN)
    return values, {
        "session_wall_seconds": time.perf_counter() - wall_before,
        "query_wall_seconds": query_wall,
        "coordinator_cpu_seconds": time.process_time() - cpu_before,
        "child_cpu_seconds": (
            child_after.ru_utime
            + child_after.ru_stime
            - child_before.ru_utime
            - child_before.ru_stime
        ),
    }


def _run_python(
    candidate: rectangle_density.RectangleDensityCandidate,
    polygons: tuple[rectangle_density.Polygon, ...],
    deadline: float,
) -> tuple[tuple[Fraction, ...], dict[str, float]]:
    cpu_before = time.process_time()
    wall_before = time.perf_counter()
    # Use the verifier's exact internal path on its own generated polygons.
    coverage = rectangle_density._coverage_polygon  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    values_list: list[Fraction] = []
    for polygon in polygons:
        if time.monotonic() >= deadline:
            raise TimeoutError("Python exact coverage exceeded the diagnostic deadline")
        values_list.append(coverage(candidate, polygon))
    if time.monotonic() >= deadline:
        raise TimeoutError("Python exact coverage exceeded the diagnostic deadline")
    values = tuple(values_list)
    return values, {
        "wall_seconds": time.perf_counter() - wall_before,
        "process_cpu_seconds": time.process_time() - cpu_before,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path)
    parser.add_argument("--baseline-binary", type=Path)
    parser.add_argument("--build-variants", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    build: dict[str, object] | None = None
    if args.build_variants is not None:
        if args.binary is not None or args.baseline_binary is not None:
            parser.error("--build-variants cannot be combined with binary paths")
        binary, baseline_binary, build = _build_variants(args.build_variants)
    else:
        if args.binary is None:
            parser.error("--binary is required unless --build-variants is used")
        binary = args.binary.resolve(strict=True)
        baseline_binary = (
            args.baseline_binary.resolve(strict=True)
            if args.baseline_binary is not None
            else None
        )
    if baseline_binary == binary:
        parser.error("baseline and candidate binaries must be distinct paths")
    if baseline_binary is not None and _sha(baseline_binary) == _sha(binary):
        parser.error("baseline and candidate binaries have identical bytes")
    candidate = load_candidate(CANDIDATE, n=11)
    cosine = (1 - ANGLE_STEP * ANGLE_STEP) / (1 + ANGLE_STEP * ANGLE_STEP)
    sine = 2 * ANGLE_STEP / (1 + ANGLE_STEP * ANGLE_STEP)
    lower = candidate.side / 2
    span = candidate.side - candidate.core_side * (cosine + sine) / 2 - lower
    polygons = tuple(
        square_polygon(
            lower + span * Fraction(index % 16, 15),
            lower + span * Fraction(index // 16, 7),
            cosine,
            sine,
            candidate.core_side,
        )
        for index in range(COUNT)
    )
    source_paths = (
        Path(__file__),
        Path(rectangle_density.__file__),
        Path(rust_rectangle_geometry.__file__),
        CANDIDATE,
        PROJECT / "sqverify_exact/src/lib.rs",
        PROJECT / "sqverify_exact/src/main.rs",
        PROJECT / "sqverify_exact/Cargo.toml",
        PROJECT / "sqverify_exact/Cargo.lock",
        PROJECT / "sqverify_exact/rust-toolchain.toml",
        binary,
    ) + ((baseline_binary,) if baseline_binary is not None else ())
    before = {str(path): _sha(path) for path in source_paths}
    deadline = time.monotonic() + MAX_SECONDS
    records: list[dict[str, object]] = []
    paired_ratios: list[float] = []
    for pair in range(PAIRS):
        order = ("singleton", "batch") if pair % 2 == 0 else ("batch", "singleton")
        pair_values: dict[str, tuple[Fraction, ...]] = {}
        pair_timings: dict[str, dict[str, float]] = {}
        for mode in order:
            values, timing = _run(binary, candidate.rectangles, polygons, mode, deadline)
            pair_values[mode] = values
            pair_timings[mode] = timing
        if pair_values["singleton"] != pair_values["batch"]:
            raise AssertionError("singleton and batch exact coverages differ")
        if len(pair_values["batch"]) != COUNT:
            raise AssertionError("batch coverage count changed")
        paired_ratios.append(
            pair_timings["batch"]["query_wall_seconds"]
            / pair_timings["singleton"]["query_wall_seconds"]
        )
        values_digest = hashlib.sha256(
            json.dumps([str(value) for value in pair_values["batch"]]).encode()
        ).hexdigest()
        records.append(
            {
                "pair": pair,
                "order": order,
                "timing": pair_timings,
                "exact_values_sha256": values_digest,
                "exact_values_equal": True,
            }
        )
    arithmetic_ab: dict[str, object] | None = None
    if baseline_binary is not None:
        comparisons: list[dict[str, object]] = []
        cpu_ratios: list[float] = []
        baseline_cpus: list[float] = []
        candidate_cpus: list[float] = []
        for pair in range(PAIRS):
            order = ("baseline", "candidate") if pair % 2 == 0 else ("candidate", "baseline")
            python_values, python_timing = _run_python(candidate, polygons, deadline)
            values_by_name: dict[str, tuple[Fraction, ...]] = {}
            timing_by_name: dict[str, dict[str, float]] = {}
            for name in order:
                selected = baseline_binary if name == "baseline" else binary
                values, timing = _run(
                    selected, candidate.rectangles, polygons, "batch", deadline
                )
                values_by_name[name] = values
                timing_by_name[name] = timing
            if not (python_values == values_by_name["baseline"] == values_by_name["candidate"]):
                raise AssertionError(
                    "Python, baseline Rust, and candidate Rust coverages differ"
                )
            baseline_cpu = timing_by_name["baseline"]["child_cpu_seconds"]
            candidate_cpu = timing_by_name["candidate"]["child_cpu_seconds"]
            baseline_cpus.append(baseline_cpu)
            candidate_cpus.append(candidate_cpu)
            cpu_ratios.append(candidate_cpu / baseline_cpu)
            comparisons.append(
                {
                    "pair": pair,
                    "order": order,
                    "python": python_timing,
                    "rust": timing_by_name,
                    "exact_values_equal": True,
                }
            )
        arithmetic_ab = {
            "status": "FIXED_WORK_ARITHMETIC_AB_DIAGNOSTIC_ONLY",
            "baseline_binary_sha256": before[str(baseline_binary)],
            "candidate_binary_sha256": before[str(binary)],
            "build": build if build is not None else "user-supplied binary provenance",
            "observations": comparisons,
            "paired_candidate_over_baseline_child_cpu": cpu_ratios,
            "baseline_child_cpu_median_seconds": median(baseline_cpus),
            "baseline_child_cpu_range_seconds": [min(baseline_cpus), max(baseline_cpus)],
            "candidate_child_cpu_median_seconds": median(candidate_cpus),
            "candidate_child_cpu_range_seconds": [min(candidate_cpus), max(candidate_cpus)],
            "criterion": (
                "candidate child CPU median <= 0.90 * baseline median, and "
                "the candidate and baseline child CPU ranges do not overlap"
            ),
            "criterion_met": (
                median(candidate_cpus) <= 0.9 * median(baseline_cpus)
                and max(candidate_cpus) < min(baseline_cpus)
            ),
            "scope": (
                "Exactly the same 128 generated polygons and fixed rectangle table. "
                "The Rust child CPU includes parsing, convexity checks, clipping, "
                "arithmetic, and output encoding; Python CPU covers its internal "
                "coverage path. No verifier branching or certificate decision is timed."
            ),
        }
    if before != {str(path): _sha(path) for path in source_paths}:
        raise AssertionError("source or binary changed during transport diagnostic")
    if time.monotonic() >= deadline:
        raise TimeoutError("transport diagnostic exceeded its 30-second ceiling")
    receipt: dict[str, object] = {
        "status": "FIXED_WORK_TRANSPORT_DIAGNOSTIC_ONLY",
        "created_utc": datetime.now(UTC).isoformat(),
        "source_sha256": before,
        "work": {"polygons": COUNT, "pairs": PAIRS, "angle_index": 1},
        "criterion": "batch query wall <= 0.75 * singleton query wall in all three pairs",
        "criterion_met": all(ratio <= 0.75 for ratio in paired_ratios),
        "paired_batch_over_singleton_query_wall": paired_ratios,
        "observations": records,
        "scope": (
            "Exact area queries only. Session wall includes child startup/shutdown; "
            "query wall includes JSON encode/write/read/decode and Rust arithmetic. "
            "Child CPU excludes coordinator; no verifier proof or speed claim."
        ),
    }
    if arithmetic_ab is not None:
        receipt["arithmetic_ab"] = arithmetic_ab
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
