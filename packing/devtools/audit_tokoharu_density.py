"""Audit exact Tokoharu density inputs and replay the retained external checker.

The rational preflight is independent of ``certify.py``. It binds every interval,
the complete axis event set, symmetry expansion, and target mass to the candidate
decimals. Global rotated coverage is still decided by the external C++ checker.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from collections.abc import Iterator
from contextlib import suppress
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools.retained_data import read_retained_text

REPO = Path(__file__).resolve().parents[2]
SOURCE = REPO / "packing/resources/web/external-square-certificates-2026-09-22/tokoharu-density"
REVISION = "b543990f7794b8c511cb46cf3854b7e8166c3674"
CASES = {11: "cert_n11_L381", 26: "cert_n26_L5508", 29: "cert_n29_L571"}
SIDES = {11: Fraction(381, 100), 26: Fraction(1377, 250), 29: Fraction(571, 100)}
GAP = Fraction(83, 40000)
EPSILON = Fraction(1, 20000)
ANGLE_COUNT = 201
TARGET = Fraction(10001, 10000)
DEFAULT_TIMEOUT = 900
Rect = tuple[Fraction, Fraction, Fraction, Fraction, Fraction]
Point = tuple[Fraction, Fraction]
PROBE_ANGLES = (0, 1, 25, 100, 200)
PROBE_RECTANGLES_PER_CASE = 12


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(), parse_float=Fraction, object_pairs_hook=_pairs)
    if not isinstance(value, dict):
        raise TypeError(f"expected JSON object: {path}")
    return value


def load_json(path: Path) -> dict[str, Any]:
    """Read a certificate JSON object with exact decimals and no duplicate keys.

    Unlike this module's own reads, it accepts a file stored as ``path.gz``: packets
    after this one keep large retained data as deterministic gzip.
    """
    value = json.loads(read_retained_text(path), parse_float=Fraction, object_pairs_hook=_pairs)
    if not isinstance(value, dict):
        raise TypeError(f"expected JSON object: {path}")
    return value


def _rational(value: object) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, int | str | Fraction):
        raise TypeError(f"not an exact rational: {value!r}")
    return Fraction(value)


def source_provenance(source: Path) -> dict[str, Any]:
    """Bind executable external source to Git or the retained acquisition checksums."""
    if (source / ".git").exists():
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=source,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        changed = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=source,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if revision != REVISION or changed:
            raise ValueError("source checkout is dirty or differs from the reviewed revision")
        return {"kind": "clean-git-checkout", "revision": revision}
    if source.resolve() != SOURCE.resolve():
        raise ValueError("non-checkout source must be the retained acquisition archive")
    manifest = SOURCE.parent / "acquisition/sources.json"
    file_manifest = manifest.with_name("tokoharu-density.sha256")
    sources = _json(manifest).get("sources")
    if not isinstance(sources, list):
        raise TypeError("acquisition manifest must contain a source list")
    entries = [
        entry
        for entry in sources
        if isinstance(entry, dict) and entry.get("id") == "tokoharu-density"
    ]
    if len(entries) != 1:
        raise ValueError("acquisition manifest must identify exactly one Tokoharu source")
    entry = entries[0]
    if (
        entry.get("source_commit") != REVISION
        or entry.get("archived_path") != str(SOURCE.relative_to(REPO))
        or entry.get("file_manifest") != str(file_manifest.relative_to(REPO))
    ):
        raise ValueError("acquisition manifest does not bind the reviewed revision and archive")

    expected: dict[Path, str] = {}
    for line in file_manifest.read_text().splitlines():
        digest, separator, name = line.partition("  ")
        path = Path(name)
        if (
            not separator
            or len(digest) != 64
            or any(char not in "0123456789abcdef" for char in digest)
            or not name.startswith("./")
            or path.is_absolute()
            or ".." in path.parts
            or path in expected
        ):
            raise ValueError(f"invalid or duplicate archive checksum entry: {line!r}")
        expected[path] = digest
    if not expected or len(expected) != entry.get("file_count"):
        raise ValueError("archive checksum manifest has the wrong file count")

    actual: set[Path] = set()
    for path in source.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"archive contains an unexpected symlink: {path}")
        if path.is_file():
            actual.add(path.relative_to(source))
    if actual != set(expected):
        missing = sorted(map(str, set(expected) - actual))
        extra = sorted(map(str, actual - set(expected)))
        raise ValueError(f"archive file set mismatch: missing={missing}, extra={extra}")
    total_bytes = 0
    for path, digest in expected.items():
        data = (source / path).read_bytes()
        if hashlib.sha256(data).hexdigest() != digest:
            raise ValueError(f"archive SHA-256 mismatch: {path}")
        total_bytes += len(data)
    if total_bytes != entry.get("total_bytes"):
        raise ValueError("archive byte count differs from the acquisition manifest")
    return {
        "kind": "verified-acquisition-archive",
        "revision": REVISION,
        "manifest": str(manifest.relative_to(REPO)),
        "file_manifest": str(file_manifest.relative_to(REPO)),
        "files_verified": len(expected),
        "bytes_verified": total_bytes,
    }


def density(data: dict[str, Any]) -> tuple[Fraction, Fraction, Fraction, list[Rect]]:
    """Reconstruct all eight orbit images with multiplicity from exact decimals."""
    side, shrink = _rational(data["L"]), _rational(data["B"])
    if not (
        side > 0
        and 0 < shrink < 1
        and side * side > 2 * shrink * shrink
        and shrink * (1 + GAP) + 3 * EPSILON < 1
    ):
        raise ValueError("invalid side, shrink, or angular/smoothing margin")
    rows, weights = data["rectangles"], data["weights"]
    if not isinstance(rows, list) or not isinstance(weights, list) or len(rows) != len(weights):
        raise ValueError("rectangle and weight arrays must have equal lengths")
    result: list[Rect] = []
    total = Fraction(0)
    for row, raw_weight in zip(rows, weights, strict=True):
        weight = _rational(raw_weight)
        if weight < 0:
            raise ValueError("negative rectangle weight")
        if weight == 0:
            continue
        if not isinstance(row, list) or len(row) != 4:
            raise ValueError("rectangle needs four coordinates")
        x0, y0, x1, y1 = map(_rational, row)
        if not (EPSILON < x0 < x1 < side - EPSILON and EPSILON < y0 < y1 < side - EPSILON):
            raise ValueError("rectangle outside smoothing-safe interior")
        total += weight
        rho = weight / (8 * (x1 - x0) * (y1 - y0))
        for a, b, d, e in ((x0, y0, x1, y1), (y0, x0, y1, x1)):
            for left, right in ((a, d), (side - d, side - a)):
                for bottom, top in ((b, e), (side - e, side - b)):
                    result.append((left, bottom, right, top, rho))
    if total <= 0:
        raise ValueError("empty density")
    integrated = sum((rho * (d - a) * (e - b) for a, b, d, e, rho in result), Fraction())
    if integrated != total:
        raise ValueError("orbit normalization changed total mass")
    return side, shrink, total, result


def _interval(tokens: Iterator[str], expected: Fraction, context: str) -> None:
    lower, upper = float.fromhex(next(tokens)), float.fromhex(next(tokens))
    if not math.isfinite(lower) or not math.isfinite(upper):
        raise ValueError(f"nonfinite interval: {context}")
    if not Fraction(lower) <= expected <= Fraction(upper):
        raise ValueError(f"interval fails exact enclosure: {context}")


def preflight(case: Path, n: int, expected_side: Fraction | None = None) -> dict[str, Any]:
    """Bind raw intervals to exact data and prove all non-coverage obligations.

    ``expected_side`` defaults to the reviewed Tokoharu side for ``n``; other packets in
    the same format (Hosono's rectangle certificates) pass their own pinned side.
    """
    data = _json(case / "certified_candidate.json")
    side, shrink, total, rectangles = density(data)
    if side != (SIDES[n] if expected_side is None else expected_side) or total >= n:
        raise ValueError("declared side mismatch or total mass fails strict n bound")
    end = (ANGLE_COUNT - 1) * GAP
    if end * end + 2 * end - 1 < 0:
        raise ValueError("angle net does not reach pi/4")
    centers = {side / 2, side - shrink / 2}
    for a, b, d, e, _rho in rectangles:
        for edge in (a, b, d, e):
            for candidate in (edge - shrink / 2, edge + shrink / 2):
                if side / 2 <= candidate <= side - shrink / 2:
                    centers.add(candidate)
    tokens = iter((case / "certificate_input.txt").read_text().split())
    try:
        _interval(tokens, side, "L")
        _interval(tokens, shrink, "B")
        if int(next(tokens)) != len(rectangles):
            raise ValueError("rectangle count mismatch")
        for index, rectangle in enumerate(rectangles):
            for field, value in enumerate(rectangle):
                _interval(tokens, value, f"rectangle {index}, field {field}")
        if int(next(tokens)) != len(centers):
            raise ValueError("incomplete axis-event count")
        for index, center in enumerate(sorted(centers)):
            _interval(tokens, center, f"axis event {index}")
        if next(tokens, None) is not None:
            raise ValueError("unexpected trailing interval input")
    except StopIteration as error:
        raise ValueError("truncated interval input") from error
    metadata = _json(case / "certificate_metadata.json")
    for key, expected in (("L", side), ("B", shrink), ("mass_exact", total)):
        if _rational(metadata[key]) != expected:
            raise ValueError(f"metadata mismatch: {key}")
    return {
        "status": "PASS",
        "n": n,
        "L": str(side),
        "B": str(shrink),
        "mass_exact": str(total),
        "mass_below_n_exact": str(n - total),
        "net_safety_exact": str(shrink * (1 + GAP)),
        "smoothing_safety_exact": str(shrink * (1 + GAP) + 3 * EPSILON),
        "net_endpoint_polynomial_exact": str(end * end + 2 * end - 1),
        "positive_basis_rectangles": len(rectangles) // 8,
        "expanded_rectangles": len(rectangles),
        "axis_event_count": len(centers),
        "axis_vertex_count": len(centers) ** 2,
    }


def square_polygon(
    x: Fraction, y: Fraction, c: Fraction, s: Fraction, b: Fraction
) -> list[Point]:
    """Exact corners, in boundary order, for the independent rational oracle."""
    return [
        (x + b * (c * u - s * v) / 2, y + b * (s * u + c * v) / 2)
        for u, v in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    ]


def exact_area(rectangle: Rect, polygon: list[Point]) -> Fraction:
    """Clip in rational arithmetic; no external geometry or interval code is used."""
    a, b, d, e, _rho = rectangle
    for axis, edge, sign in ((0, a, 1), (0, d, -1), (1, b, 1), (1, e, -1)):
        clipped: list[Point] = []
        if not polygon:
            return Fraction()
        previous = polygon[-1]
        previous_depth = sign * (previous[axis] - edge)
        for current in polygon:
            depth = sign * (current[axis] - edge)
            if (depth >= 0) != (previous_depth >= 0):
                ratio = previous_depth / (previous_depth - depth)
                clipped.append(
                    (
                        previous[0] + ratio * (current[0] - previous[0]),
                        previous[1] + ratio * (current[1] - previous[1]),
                    )
                )
            if depth >= 0:
                clipped.append(current)
            previous, previous_depth = current, depth
        polygon = clipped
    if not polygon:
        return Fraction()
    return (
        abs(
            sum(
                (
                    point[0] * polygon[(index + 1) % len(polygon)][1]
                    - point[1] * polygon[(index + 1) % len(polygon)][0]
                    for index, point in enumerate(polygon)
                ),
                Fraction(),
            )
        )
        / 2
    )


def _enclose(lower: Fraction, upper: Fraction | None = None) -> str:
    upper = lower if upper is None else upper
    lo, hi = float(lower), float(upper)
    if Fraction(lo) > lower:
        lo = math.nextafter(lo, -math.inf)
    if Fraction(hi) < upper:
        hi = math.nextafter(hi, math.inf)
    return f"{lo.hex()} {hi.hex()}"


def enclose(value: Fraction) -> str:
    """The checker's input form: the tightest binary64 interval around an exact value."""
    return _enclose(value)


def _line_length(polygon: list[Point], x: Fraction, lo: Fraction, hi: Fraction) -> Fraction:
    intersections: list[Fraction] = []
    for index, first in enumerate(polygon):
        second = polygon[(index + 1) % len(polygon)]
        if first[0] == second[0]:
            if x == first[0]:
                intersections.extend((first[1], second[1]))
        elif min(first[0], second[0]) <= x <= max(first[0], second[0]):
            ratio = (x - first[0]) / (second[0] - first[0])
            intersections.append(first[1] + ratio * (second[1] - first[1]))
    if not intersections:
        return Fraction()
    return max(Fraction(), min(hi, max(intersections)) - max(lo, min(intersections)))


def adversarial(source: Path, output: Path) -> dict[str, Any]:
    """Test lower-area and slice enclosures against exact rational geometry."""
    commands: list[str] = []
    expected: list[tuple[str, list[Fraction]]] = []
    for name in CASES.values():
        _side, shrink, _total, rectangles = density(
            _json(source / "certificates" / name / "certified_candidate.json")
        )
        stride = max(1, len(rectangles) // PROBE_RECTANGLES_PER_CASE)
        for rectangle in rectangles[::stride][:PROBE_RECTANGLES_PER_CASE]:
            a, b, d, e, _rho = rectangle
            for angle in PROBE_ANGLES:
                tangent = angle * GAP
                c = (1 - tangent * tangent) / (1 + tangent * tangent)
                s = 2 * tangent / (1 + tangent * tangent)
                extent = shrink * (c + s) / 2
                for x, y in (
                    ((a + d) / 2, (b + e) / 2),
                    (a - extent, (b + e) / 2),
                    (d + extent, (b + e) / 2),
                    (d + extent - Fraction(1, 10**8), e),
                    ((a + d) / 2 + extent, (b + e) / 2 - shrink * (c - s) / 2),
                    ((a + d) / 2 - extent, (b + e) / 2 + shrink * (c - s) / 2),
                ):
                    arguments = [*rectangle[:4], x, y, c, s, shrink]
                    commands.append("area " + " ".join(_enclose(value) for value in arguments))
                    expected.append(
                        (
                            "area",
                            [
                                exact_area(rectangle, square_polygon(x, y, c, s, shrink)),
                                (d - a) * (e - b),
                            ],
                        )
                    )
                if angle:
                    x, y = (a + d) / 2, (b + e) / 2
                    width = Fraction(1, 64)
                    arguments = [
                        _enclose(a),
                        _enclose(x - width, x + width),
                        _enclose(y - width, y + width),
                        _enclose(b),
                        _enclose(e),
                        _enclose(shrink / (2 * s)),
                        _enclose(shrink / (2 * c)),
                        _enclose(-c / s),
                        _enclose(s / c),
                    ]
                    commands.append("slice " + " ".join(arguments))
                    expected.append(
                        (
                            "slice",
                            [
                                _line_length(
                                    square_polygon(x + dx, y + dy, c, s, shrink), a, b, e
                                )
                                for dx in (-width, Fraction(), width)
                                for dy in (-width, Fraction(), width)
                            ],
                        )
                    )
    output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="tokoharu-probe-") as directory:
        executable = Path(directory) / "probe"
        compile_command = [
            "g++",
            "-O2",
            "-std=c++17",
            "-fno-fast-math",
            "-ffp-contract=off",
            "-I",
            str(source / "src"),
            str(Path(__file__).with_name("tokoharu_density_probe.cpp")),
            "-o",
            str(executable),
        ]
        compile_result = subprocess.run(
            compile_command, capture_output=True, text=True, check=True
        )
        atomic_write_text(output / "compile.log", compile_result.stdout + compile_result.stderr)
        result = subprocess.run(
            [str(executable)],
            input="\n".join(commands) + "\n",
            capture_output=True,
            text=True,
            check=True,
            timeout=DEFAULT_TIMEOUT,
        )
    atomic_write_text(output / "input.txt", "\n".join(commands) + "\n")
    atomic_write_text(output / "stdout.log", result.stdout)
    atomic_write_text(output / "stderr.log", result.stderr)
    rows = result.stdout.splitlines()
    if len(rows) != len(expected):
        raise ValueError("probe omitted results")
    positive_areas = 0
    positive_partial_areas = 0
    for index, (row, (kind, values)) in enumerate(zip(rows, expected, strict=True)):
        actual = [Fraction(float.fromhex(token)) for token in row.split()]
        if kind == "area":
            if len(actual) != 1 or not 0 <= actual[0] <= values[0]:
                raise ValueError(f"inscribed area exceeds exact intersection at probe {index}")
            positive_areas += actual[0] > 0
            positive_partial_areas += 0 < actual[0] < values[1] and values[0] < values[1]
        elif len(actual) != 2 or any(not actual[0] <= value <= actual[1] for value in values):
            raise ValueError(f"slice interval misses exact section at probe {index}")
    record = {
        "status": "PASS",
        "scope": "Deterministic adversarial samples; not independent global coverage",
        "area_probes": sum(kind == "area" for kind, _ in expected),
        "positive_area_lower_bounds": positive_areas,
        "positive_partial_area_lower_bounds": positive_partial_areas,
        "slice_boxes": sum(kind == "slice" for kind, _ in expected),
        "exact_slice_samples": sum(len(values) for kind, values in expected if kind == "slice"),
        "angles": list(PROBE_ANGLES),
        "compile_command": compile_command,
    }
    atomic_write_text(output / "probe.json", json.dumps(record, indent=2) + "\n")
    return record


def driver_controls(source: Path, output: Path) -> dict[str, Any]:
    """Reproduce starting-certificate acceptance without the target-n and data checks."""
    output.mkdir(parents=True, exist_ok=False)
    records: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="tokoharu-driver-") as directory:
        scratch = Path(directory)
        original = source / "certificates" / CASES[29]
        stale = scratch / "stale"
        stale.mkdir()
        for name in (
            "certified_candidate.json",
            "certificate_metadata.json",
            "verification_summary.json",
        ):
            shutil.copyfile(original / name, stale / name)
        metadata = json.loads((stale / "certificate_metadata.json").read_text())
        metadata["L"] = "100"
        atomic_write_text(stale / "certificate_metadata.json", json.dumps(metadata) + "\n")
        atomic_write_text(output / "stale-metadata.json", json.dumps(metadata, indent=2) + "\n")
        for name, n, target, certificate in (
            ("wrong-target-n", 1, "5.71", original),
            ("stale-side-metadata", 29, "100", stale),
        ):
            command = [
                sys.executable,
                str(source / "src/push.py"),
                "--n",
                str(n),
                "--from",
                str(certificate),
                "--target",
                target,
                "--out",
                str(scratch / name),
            ]
            result = subprocess.run(
                command, capture_output=True, text=True, timeout=60, check=False
            )
            atomic_write_text(output / f"{name}.stdout.log", result.stdout)
            atomic_write_text(output / f"{name}.stderr.log", result.stderr)
            rows = [json.loads(line) for line in result.stdout.splitlines()]
            reproduced = (
                result.returncode == 0
                and any(row.get("status") == "TARGET_REACHED" for row in rows)
                and rows[-1].get("n") == n
                and Fraction(str(rows[-1].get("best_L"))) == Fraction(target)
            )
            records.append(
                {
                    "control": name,
                    "command": command,
                    "returncode": result.returncode,
                    "invalid_initial_bound_accepted": reproduced,
                    "finite_grid_upper_bound": math.isqrt(n - 1) + 1,
                }
            )
    record = {"status": "OBSERVED", "controls": records}
    atomic_write_text(output / "driver-controls.json", json.dumps(record, indent=2) + "\n")
    return record


def replay(case: Path, output: Path, workers: int, timeout: int) -> dict[str, Any]:
    """Run unchanged upstream sources in scratch; retain text outputs, not a binary."""
    output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="tokoharu-density-") as directory:
        scratch = Path(directory)
        for name in ("verify.cpp", "run_verify.py", "certificate_input.txt"):
            shutil.copyfile(case / name, scratch / name)
        command = [sys.executable, "run_verify.py", "--workers", str(workers)]
        started = time.monotonic()
        with (
            (output / "stdout.log").open("w") as stdout,
            (output / "stderr.log").open("w") as stderr,
            subprocess.Popen(
                command, cwd=scratch, stdout=stdout, stderr=stderr, start_new_session=True
            ) as process,
        ):
            try:
                returncode = process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                # The runner owns verifier children; stop the whole group at the ceiling.
                with suppress(ProcessLookupError):
                    os.killpg(process.pid, signal.SIGKILL)
                process.wait()
                raise
        elapsed = time.monotonic() - started
        if returncode:
            raise ValueError(f"upstream replay exited {returncode}; see {output}")
        summary = _json(scratch / "verification_summary.json")
        rows = [
            json.loads(line)
            for line in (scratch / "verified_angles.jsonl").read_text().splitlines()
        ]
        if (
            summary.get("status") != "VERIFIED"
            or summary.get("angle_cases") != ANGLE_COUNT
            or sorted(row["r"] for row in rows) != list(range(ANGLE_COUNT))
            or any(
                row["status"] != "verified" or Fraction(row["lower_bound"]) < TARGET
                for row in rows
            )
        ):
            raise ValueError("incomplete or failed upstream angle coverage")
        for name in ("verification_summary.json", "verified_angles.jsonl"):
            shutil.copyfile(scratch / name, output / name)
        return {
            "status": "PASS",
            "command": command,
            "working_directory": "temporary copy of retained certificate directory",
            "elapsed_seconds_including_compile": elapsed,
            "timeout_seconds": timeout,
            "summary": summary,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--n", type=int, choices=tuple(CASES), action="append")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--adversarial", action="store_true")
    parser.add_argument("--driver-controls", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    args = parser.parse_args()
    record: dict[str, Any] = {
        "kind": "tokoharu-density-audit/v1",
        "source_revision": REVISION,
        "source": str(args.source.resolve()),
        "python": sys.version,
        "scope": "Independent exact preconditions; optional upstream global interval replay",
        "cases": [],
    }
    args.out.mkdir(parents=True, exist_ok=True)
    try:
        record["provenance"] = source_provenance(args.source)
        record["platform"] = platform.platform()
        compiler = subprocess.run(
            ["g++", "--version"], capture_output=True, text=True, check=True
        )
        record["compiler"] = compiler.stdout
        for n in args.n or CASES:
            case = args.source / "certificates" / CASES[n]
            item = preflight(case, n)
            record["cases"].append(item)
            atomic_write_text(
                args.out / "audit.json", json.dumps(record, indent=2, default=str) + "\n"
            )
            print(json.dumps(item), flush=True)
            if args.replay:
                item["replay"] = replay(case, args.out / CASES[n], args.workers, args.timeout)
                print(json.dumps({"n": n, "replay": "PASS"}), flush=True)
        if args.adversarial:
            record["adversarial"] = adversarial(args.source, args.out / "adversarial")
        if args.driver_controls:
            record["driver_controls"] = driver_controls(
                args.source, args.out / "driver-controls"
            )
        record["status"] = "PASS"
    except (OSError, TypeError, ValueError, subprocess.SubprocessError) as error:
        record["status"] = "FAIL"
        record["error"] = str(error)
        print(str(error), file=sys.stderr)
    atomic_write_text(args.out / "audit.json", json.dumps(record, indent=2, default=str) + "\n")
    return 0 if record["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
