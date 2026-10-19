"""Compare two exact Rust binaries on identical bounded verifier work.

This is a source-bound timing diagnostic. The capped external case remains
INCONCLUSIVE and no result here promotes a rectangle certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import tempfile
import time
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from statistics import median
from typing import Any

from benchmarks.bench_rectangle_verifier_parity import (
    ensure_external_scratch,
    run_command,
)
from sqpack import rectangle_density, rust_rectangle_geometry
from sqpack.rectangle_density import load_candidate, verify_candidate

PROJECT = Path(__file__).resolve().parents[1]
CRATE = PROJECT / "sqverify_exact"
ANALYTIC = PROJECT / "resources/web/wand125-tools-2026-09-29/native-analytic-control.json"
EXTERNAL = (
    PROJECT
    / "resources/web/external-square-certificates-2026-09-22/tokoharu-density"
    / "certificates/cert_n11_L381/certified_candidate.json"
)
EXPECTED_INPUT_SHA = {
    "analytic": "bfd6e4dea67a048321836c69c9c9fe782687ffc512ccb1afc43249212ba5f01e",
    "external": "8e3339eefb2fad81868f51e3f72cbc8487b40b66f9d8fbc711c1dbd5e5edeff4",
}
EXPECTED_REPORT_SHA = {
    "analytic": "bd878de9d1f469c749015aea091e96eceb98d8820db3fdc47f3e6562948117c8",
    "external": "68123cb6992b9971c370c1fd677985a1c6c5f31c74390e53c47303d5a5d49105",
}
PAIRS = 3
INTERNAL_SECONDS = 30
INVOCATION_SECONDS = 40
TOTAL_SECONDS = 300
BUILD_SECONDS = 90


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _external_scratch(path: Path) -> Path:
    """Admit declared scratch without a repository or relative-path fallback."""
    if not path.is_absolute():
        raise ValueError("scratch paths must be absolute")
    resolved = path.resolve()
    if resolved.is_relative_to(PROJECT.parent.resolve()):
        raise ValueError("scratch paths must be outside the repository")
    system = platform.system()
    if system == "Darwin":
        # Keep the original mounted-volume requirement on the original host.
        ensure_external_scratch(resolved)
    elif system == "Linux":
        if not resolved.parent.is_dir():
            raise ValueError("scratch parent must be existing writable storage")
        resolved.mkdir(exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=resolved) as probe:
            probe.write(b"writable")
            probe.flush()
    else:
        raise ValueError("paired verifier builds require Linux or macOS scratch")
    return resolved


def _build_environment(target: Path) -> dict[str, str]:
    names = ("TMPDIR", "UV_CACHE_DIR", "CARGO_TARGET_DIR")
    if not all(os.environ.get(name) for name in names):
        raise ValueError("external TMPDIR, UV_CACHE_DIR and CARGO_TARGET_DIR are required")
    environment = dict(os.environ)
    for name in names:
        environment[name] = str(_external_scratch(Path(environment[name])))
    environment["CARGO_TARGET_DIR"] = str(_external_scratch(target))
    return environment


def _build_command(arm: str) -> list[str]:
    command = ["cargo", "build", "--offline", "--locked", "--release"]
    if arm == "reference":
        command.append("--no-default-features")
    elif arm != "default":
        raise ValueError("unknown verifier build arm")
    return command


def _require_unchanged(sources: dict[str, str]) -> None:
    if sources != {name: _sha(Path(name)) for name in sources}:
        raise ValueError("verifier source, input, or binary changed during the benchmark")


def _build_variant(
    arm: str, target: Path, sources: dict[str, str]
) -> tuple[Path, dict[str, object]]:
    """Execute one release arm against the inventory frozen before either build."""
    command = _build_command(arm)
    environment = _build_environment(target)
    target = Path(environment["CARGO_TARGET_DIR"])
    _require_unchanged(sources)
    rustc = subprocess.run(
        ["rustc", "-vV"],
        cwd=CRATE,
        env=environment,
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    ).stdout.strip()
    cargo = subprocess.run(
        ["cargo", "--version"],
        cwd=CRATE,
        env=environment,
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    ).stdout.strip()
    started = time.perf_counter()
    completed = subprocess.run(
        command,
        cwd=CRATE,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
        timeout=BUILD_SECONDS,
    )
    if completed.returncode != 0:
        raise ValueError(f"{arm} release build failed: {completed.stderr[-500:]}")
    binary = target / "release/sqverify-exact"
    _require_unchanged(sources)
    return binary, {
        "arm": arm,
        "command": command,
        "default_features": arm == "default",
        "cwd": str(CRATE),
        "target_dir": str(target),
        "wall_seconds": time.perf_counter() - started,
        "ceiling_seconds": BUILD_SECONDS,
        "source_sha256": dict(sources),
        "rustc_version": rustc,
        "cargo_version": cargo,
        "rustflags": environment.get("RUSTFLAGS", ""),
        "cargo_encoded_rustflags": environment.get("CARGO_ENCODED_RUSTFLAGS", ""),
        "scratch_policy": (
            "darwin-mounted-agent-scratch"
            if platform.system() == "Darwin"
            else "linux-absolute-writable-outside-repository"
        ),
        "scratch_paths": {
            name: environment[name] for name in ("TMPDIR", "UV_CACHE_DIR", "CARGO_TARGET_DIR")
        },
        "binary_sha256": _sha(binary),
    }


def _admit_builds(
    binaries: dict[str, Path],
    builds: dict[str, dict[str, object]],
    sources: dict[str, str],
) -> dict[str, str]:
    """Admit executed reference/default builds, never a retained host-specific binary."""
    if set(binaries) != {"reference", "default"} or set(builds) != set(binaries):
        raise ValueError("paired build arms are missing or unexpected")
    _require_unchanged(sources)
    reference = builds["reference"]
    hashes: dict[str, str] = {}
    for arm, binary in binaries.items():
        build = builds[arm]
        if (
            build.get("arm") != arm
            or build.get("command") != _build_command(arm)
            or build.get("default_features") is not (arm == "default")
            or build.get("cwd") != str(CRATE)
            or build.get("target_dir") != str(binary.parent.parent)
        ):
            raise ValueError("build feature selection or target differs from its intended arm")
        if build.get("source_sha256") != sources:
            raise ValueError("paired builds used different source inventories")
        if not all(
            isinstance(build.get(field), str) and build[field]
            for field in ("rustc_version", "cargo_version")
        ):
            raise ValueError("build toolchain identity is missing")
        for field in (
            "rustc_version",
            "cargo_version",
            "rustflags",
            "cargo_encoded_rustflags",
            "scratch_policy",
        ):
            if build.get(field) != reference.get(field):
                raise ValueError("paired build environment differs")
        scratch = build.get("scratch_paths")
        reference_scratch = reference.get("scratch_paths")
        if (
            not isinstance(scratch, dict)
            or not isinstance(reference_scratch, dict)
            or scratch.get("CARGO_TARGET_DIR") != build["target_dir"]
            or any(
                scratch.get(name) != reference_scratch.get(name)
                for name in ("TMPDIR", "UV_CACHE_DIR")
            )
        ):
            raise ValueError("paired build scratch environment differs")
        hashes[arm] = _sha(binary)
        if build.get("binary_sha256") != hashes[arm]:
            raise ValueError("binary differs from its executed build")
    if (
        len({binary.resolve(strict=True) for binary in binaries.values()}) != 2
        or len(set(hashes.values())) != 2
    ):
        raise ValueError("reference and default binaries are identical")
    return hashes


def _normalized(report: dict[str, Any]) -> dict[str, Any]:
    expected_metadata = {
        "backend",
        "rust_binary_sha256",
        "rust_table_sha256",
        "backend_timeout",
    }
    if not expected_metadata <= report.keys():
        raise ValueError("Rust report is missing backend metadata")
    if report["backend"] != "rust" or report["backend_timeout"] is not False:
        raise ValueError("Rust report has an unadmitted backend state")
    return {key: value for key, value in report.items() if key not in expected_metadata}


def _report_sha(report: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _worker(dataset: str, binary: Path) -> int:
    source = ANALYTIC if dataset == "analytic" else EXTERNAL
    n = 3 if dataset == "analytic" else 11
    side = Fraction(3, 2) if dataset == "analytic" else Fraction(381, 100)
    candidate = load_candidate(source, n=n, expected_side=side)
    before_child = resource.getrusage(resource.RUSAGE_CHILDREN)
    parent_cpu = time.process_time()
    started = time.perf_counter()
    report = verify_candidate(
        candidate,
        angle_indices=tuple(range(201)) if dataset == "analytic" else (1,),
        max_nodes_per_angle=10_000 if dataset == "analytic" else 1_000,
        max_depth=20,
        max_seconds=INTERNAL_SECONDS,
        bound_mode="common-core",
        retain_pending_boxes=dataset == "external",
        backend="rust",
        rust_binary=binary,
    )
    verification_wall = time.perf_counter() - started
    coordinator_cpu = time.process_time() - parent_cpu
    after_child = resource.getrusage(resource.RUSAGE_CHILDREN)
    print(
        json.dumps(
            {
                "report": report.as_dict(),
                "verification_wall_seconds": verification_wall,
                "coordinator_cpu_seconds": coordinator_cpu,
                "rust_child_cpu_seconds": (
                    after_child.ru_utime
                    + after_child.ru_stime
                    - before_child.ru_utime
                    - before_child.ru_stime
                ),
            },
            sort_keys=True,
        )
    )
    return 0


def _assess(observations: list[dict[str, Any]]) -> dict[str, object]:
    metrics: dict[str, object] = {}
    if len(observations) != 4 * PAIRS:
        raise ValueError("paired verifier census is incomplete or unexpected")
    for dataset in ("analytic", "external"):
        rows = [row for row in observations if row["dataset"] == dataset]
        if len(rows) != 2 * PAIRS:
            raise ValueError("paired verifier census is incomplete")
        if {(row["pair"], row["arm"]) for row in rows} != {
            (pair, arm) for pair in range(PAIRS) for arm in ("reference", "default")
        }:
            raise ValueError("paired verifier identities are duplicated or missing")
        for field in ("rust_child_cpu_seconds", "invocation_wall_seconds"):
            baseline = [float(row[field]) for row in rows if row["arm"] == "reference"]
            candidate = [float(row[field]) for row in rows if row["arm"] == "default"]
            if len(baseline) != PAIRS or len(candidate) != PAIRS:
                raise ValueError("paired verifier arms are incomplete")
            metrics[f"{dataset}_{field}"] = {
                "reference_median": median(baseline),
                "reference_range": [min(baseline), max(baseline)],
                "default_median": median(candidate),
                "default_range": [min(candidate), max(candidate)],
                "default_over_reference_median": median(candidate) / median(baseline),
                "paired_default_over_reference": [
                    float(
                        next(
                            row[field]
                            for row in rows
                            if row["pair"] == pair and row["arm"] == "default"
                        )
                    )
                    / float(
                        next(
                            row[field]
                            for row in rows
                            if row["pair"] == pair and row["arm"] == "reference"
                        )
                    )
                    for pair in range(PAIRS)
                ],
            }
    external_cpu = metrics["external_rust_child_cpu_seconds"]
    external_wall = metrics["external_invocation_wall_seconds"]
    analytic_wall = metrics["analytic_invocation_wall_seconds"]
    assert isinstance(external_cpu, dict)
    assert isinstance(external_wall, dict)
    assert isinstance(analytic_wall, dict)
    metrics["material_bounded_verifier_improvement"] = (
        external_cpu["default_over_reference_median"] <= 0.90
        and external_cpu["default_range"][1] < external_cpu["reference_range"][0]
        and external_wall["default_over_reference_median"] <= 1.05
        and analytic_wall["default_over_reference_median"] <= 1.05
    )
    return metrics


def _publish_receipt(output: Path, result: dict[str, object]) -> None:
    """Publish complete JSON atomically, refusing even a late destination collision."""
    content = json.dumps(result, indent=2, sort_keys=True) + "\n"
    with tempfile.TemporaryDirectory(prefix=f".{output.name}.", dir=output.parent) as staging:
        temporary = Path(staging) / "receipt.json"
        with temporary.open("x", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, output)
        except FileExistsError as error:
            raise ValueError("refusing to overwrite a prior verifier A/B receipt") from error


def run(target_root: Path, output: Path) -> dict[str, object]:
    if not output.is_absolute():
        raise ValueError("benchmark output path must be absolute")
    output = output.resolve()
    _external_scratch(output.parent)
    target_root = _external_scratch(target_root)
    if output.exists():
        raise ValueError("refusing to overwrite a prior verifier A/B receipt")
    source_paths = (
        Path(__file__),
        Path(rectangle_density.__file__),
        Path(rust_rectangle_geometry.__file__),
        PROJECT / "benchmarks/bench_rectangle_verifier_parity.py",
        CRATE / "Cargo.toml",
        CRATE / "Cargo.lock",
        CRATE / "rust-toolchain.toml",
        CRATE / "src/lib.rs",
        CRATE / "src/main.rs",
        ANALYTIC,
        EXTERNAL,
    )
    # Freeze the complete instrument and input inventory before the first build.
    sources = {str(path): _sha(path) for path in source_paths}
    for dataset, path in (("analytic", ANALYTIC), ("external", EXTERNAL)):
        if sources[str(path)] != EXPECTED_INPUT_SHA[dataset]:
            raise ValueError(f"{dataset} input differs from the retained workload")
    binaries: dict[str, Path] = {}
    builds: dict[str, dict[str, object]] = {}
    for arm in ("reference", "default"):
        binaries[arm], builds[arm] = _build_variant(arm, target_root / arm, sources)
    binary_hashes = _admit_builds(binaries, builds, sources)
    before = sources | {str(binaries[arm]): sha for arm, sha in binary_hashes.items()}
    print(
        "PAIRED_BUILD_PREFLIGHT " + json.dumps(builds, sort_keys=True),
        file=sys.stderr,
        flush=True,
    )
    started = time.monotonic()
    observations: list[dict[str, Any]] = []
    for dataset in ("analytic", "external"):
        for pair in range(PAIRS):
            order = ("reference", "default") if pair % 2 == 0 else ("default", "reference")
            for arm in order:
                if time.monotonic() - started >= TOTAL_SECONDS - INVOCATION_SECONDS:
                    raise TimeoutError("paired verifier benchmark reached its total ceiling")
                _require_unchanged(before)
                binary = binaries[arm]
                command = [
                    sys.executable,
                    "-m",
                    "benchmarks.bench_rectangle_rust_verifier_ab",
                    "--worker",
                    dataset,
                    "--binary",
                    str(binary),
                ]
                outer, stdout, stderr = run_command(
                    command, cwd=PROJECT, timeout=INVOCATION_SECONDS
                )
                if outer["timed_out"] or outer["exit_code"] != 0 or stderr:
                    raise ValueError(
                        f"{dataset}/{pair}/{arm} refused or timed out: {stderr[-500:]}"
                    )
                payload: Any = json.loads(stdout)
                if not isinstance(payload, dict) or not isinstance(payload.get("report"), dict):
                    raise TypeError("worker omitted its exact verifier report")
                report: dict[str, Any] = payload["report"]
                if report["rust_binary_sha256"] != binary_hashes[arm]:
                    raise ValueError("worker used a different Rust binary")
                normalized = _normalized(report)
                expected_status = "VERIFIED" if dataset == "analytic" else "INCONCLUSIVE"
                expected_nodes = 1781 if dataset == "analytic" else 1000
                if (
                    normalized["status"] != expected_status
                    or sum(angle["nodes"] for angle in normalized["angles"]) != expected_nodes
                    or _report_sha(normalized) != EXPECTED_REPORT_SHA[dataset]
                ):
                    raise ValueError(
                        f"{dataset}/{pair}/{arm} changed the retained exact census"
                    )
                observations.append(
                    {
                        "dataset": dataset,
                        "pair": pair,
                        "arm": arm,
                        "order": order,
                        "status": normalized["status"],
                        "nodes": expected_nodes,
                        "normalized_report_sha256": _report_sha(normalized),
                        "invocation_wall_seconds": outer["wall_seconds"],
                        "verification_wall_seconds": payload["verification_wall_seconds"],
                        "coordinator_cpu_seconds": payload["coordinator_cpu_seconds"],
                        "rust_child_cpu_seconds": payload["rust_child_cpu_seconds"],
                    }
                )
    _require_unchanged(before)
    if time.monotonic() - started >= TOTAL_SECONDS:
        raise TimeoutError("paired verifier benchmark exceeded its total ceiling")
    result: dict[str, object] = {
        "status": "MATCHED_BOUNDED_VERIFIER_DIAGNOSTIC_ONLY",
        "created_utc": datetime.now(UTC).isoformat(),
        "source_sha256": sources,
        "binary_sha256": binary_hashes,
        "builds": builds,
        "scratch_paths": {"target_root": str(target_root), "output": str(output)},
        "python_executable": sys.executable,
        "python_version": sys.version,
        "settings": {
            "pairs": PAIRS,
            "arms": {
                "reference": "original Rust expressions, --no-default-features",
                "default": "production default features",
            },
            "internal_seconds": INTERNAL_SECONDS,
            "per_build_ceiling_seconds": BUILD_SECONDS,
            "per_invocation_ceiling_seconds": INVOCATION_SECONDS,
            "total_ceiling_seconds": TOTAL_SECONDS,
            "bound_mode": "common-core",
            "analytic": "all 201 angles, 10000 nodes/angle, depth 20, threshold 1",
            "external": "angle 1, 1000 nodes, depth 20, threshold 1, pending retained",
        },
        "observations": observations,
        "assessment": _assess(observations),
        "scope": (
            "Exploratory three-pair comparison of a complete analytic control and capped "
            "external angle only; the latter remains INCONCLUSIVE. Invocation wall includes "
            "Python startup/admission/serialization and resident Rust startup/shutdown. "
            "Child CPU measures the Rust subprocess; coordinator CPU excludes it. "
            "This is no full certificate or proof claim."
        ),
    }
    _publish_receipt(output, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", choices=("analytic", "external"))
    parser.add_argument("--binary", type=Path)
    parser.add_argument("--target-root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.worker is not None:
        if args.binary is None:
            parser.error("worker needs --binary")
        raise SystemExit(_worker(args.worker, args.binary))
    if args.binary is not None:
        parser.error("--binary is only accepted for a worker")
    if args.target_root is None or args.output is None:
        parser.error("paired run needs --target-root and --output")
    result = run(args.target_root, args.output)
    print(json.dumps({"status": result["status"], "assessment": result["assessment"]}))


if __name__ == "__main__":
    main()
