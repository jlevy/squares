#!/usr/bin/env python3
"""Independently admit one retained fixed-core calibration profile.

This reader intentionally shares no code with the calibration producer.  It rebuilds
the frozen n=2 cross, its rational direction net, threshold charges, normalization,
interval witness checks, dilation algebra, resource summaries, and worker topology
from the retained bytes.  Its proof is calibration-only evidence.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import math
import stat
import subprocess
import sys
from collections.abc import Collection, Sequence
from decimal import ROUND_HALF_UP, Decimal, localcontext
from fractions import Fraction
from itertools import pairwise
from pathlib import Path, PurePosixPath
from typing import Never, cast

READER_SCHEMA = "fixed-core-calibration-source-distinct-readback/v1"
RECEIPT_SCHEMA = "fixed-core-packet-calibration/v1"
FIXTURE_ID = "fixed-core-calibration-cross/v1"
NORMALIZED_ID = "fixed-core-calibration-cross-normalized/v1"
FIXTURE_PATH = "packing/cases/n02_fixed_core_packet_calibration/fixture.json"
FIXTURE_SHA256 = "1aface38ab79526397b7b9f24325df844e2eb9717d3e29a094fcdefe8822f539"
FIXTURE_BYTES = 935
FIXTURE_PROVENANCE = {
    "kind": "synthetic fixed-core packet calibration fixture",
    "construction": "center point and horizontal/vertical two-of-three cross",
    "purpose": "known-answer execution-path calibration",
}
CALIBRATION_SCOPE = (
    "execution-path calibration for the frozen n=2 cross fixture; observed timing, "
    "box, CPU, and RSS measurements describe this invocation only"
)
PHASE_DURATION_SCOPE = (
    "phase durations use one monotonic origin, include checkpoint publications inside "
    "the phase, and exclude the closing checkpoint that publishes the duration; "
    "external lifetime ends at the parent final readback; terminal admission runs from "
    "that readback through metrics and invocation validation and the first complete "
    "receipt validation, serialization, and staging; it excludes the second staging "
    "needed to embed that duration and the atomic operating-system replace; those final "
    "steps remain subject to a fresh deadline and cancellation check immediately before "
    "the replace"
)
CPU_SCOPE = (
    "coordinator process_time plus cumulative user/system time of its reaped direct "
    "children between retained start and end observations; neither is process-group "
    "CPU time and parent readback CPU is excluded"
)
RSS_SCOPE = (
    "sampled sum of resident-set sizes for observed members of the supervised process "
    "group; samples can miss transient peaks and can count shared pages more than once"
)
TOPOLOGY_SCOPE = (
    "route-scoped coordinator and completed process-pool task lifetimes observed by "
    "the calibration worker; configured workers are reported separately from actual "
    "child identities and simultaneous task execution, and no process arguments or "
    "unrelated host-process metadata are retained"
)
RUNTIME_SCOPE = (
    "source and observed runtime identities for this execution; no interpreter-binary, "
    "installed-wheel, operating-system, CPU, scheduling, or cross-host byte-equivalence "
    "claim"
)

N = 2
OUTER_SIDE = Fraction(3, 4)
CORE_SIDE = Fraction(1, 2)
STEPS = 2_880
RAW_DIRECTIONS = STEPS + 1
INTERVAL_DIRECTIONS = 2 * STEPS + 1
TOTAL_DIRECTION_ROWS = 3 * RAW_DIRECTIONS + INTERVAL_DIRECTIONS
HALF_GAP = Fraction(1, 5_760)
RAW_BUDGET = Fraction(2)
RAW_MINIMUM = Fraction(2)
NORMALIZATION = Fraction(1, 2)
NORMALIZED_BUDGET = Fraction(1)
NORMALIZED_MINIMUM = Fraction(1)
INTEGER_SCALE = 8
FACTOR_SQUARED = Fraction(132_710_404, 33_189_121)
SIDE_SQUARED = Fraction(298_598_409, 132_756_484)
DILATION_SCHEMA = "packing.squares:FractionalDilationLimitCorollary/v3"

TOP_LEVEL_KEYS = {
    "schema",
    "status",
    "disposition",
    "evidence_scope",
    "fixture",
    "sources",
    "invocation",
    "settings",
    "clocks",
    "resources",
    "raw",
    "normalized",
    "routes",
    "artifacts",
    "supervision",
    "phase",
    "error",
}
FORBIDDEN_KEYS = {
    "scientific_decision",
    "packet",
    "strictly_above_t026",
    "t026_path",
    "t026_sha256",
}
FORBIDDEN_VALUES = (
    "packet-accepted",
    "BC329",
    "T-025",
    "T-026",
    "n11_threshold_certificate",
)
OBSERVABLE_PHASES = (
    "preflight",
    "raw-sweep",
    "normalized-exact",
    "reflected-interval",
    "dilation-replay",
    "readback",
    "awaiting-worker-exit",
)
ARTIFACTS = (
    ("raw-directions", "raw-directions", RAW_DIRECTIONS, True),
    ("normalized-exact-directions", "normalized-exact-directions", RAW_DIRECTIONS, True),
    (
        "normalized-interval-directions",
        "normalized-interval-directions",
        INTERVAL_DIRECTIONS,
        True,
    ),
    ("dilation-directions", "dilation-directions", RAW_DIRECTIONS, True),
    ("normalized-candidate", "candidate.json", 1, False),
    ("generic-dilation-record", "dilation.json", 1, False),
    ("rss-observations", "rss-samples.json", 1, False),
    ("raw-worker-topology", "raw-worker-topology.json", 1, False),
    (
        "normalized-exact-worker-topology",
        "normalized-exact-worker-topology.json",
        1,
        False,
    ),
    ("calibration-receipt", "result.json", 1, False),
)

POINT = (Fraction(3, 8), Fraction(3, 8))
HORIZONTAL = (
    (Fraction(3, 16), Fraction(3, 8)),
    POINT,
    (Fraction(9, 16), Fraction(3, 8)),
)
VERTICAL = (
    (Fraction(3, 8), Fraction(3, 16)),
    POINT,
    (Fraction(3, 8), Fraction(9, 16)),
)


class ReadbackRefusalError(ValueError):
    """Retained bytes do not satisfy the source-distinct calibration contract."""


def _refuse(message: str) -> Never:
    raise ReadbackRefusalError(message)


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            _refuse(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def _reject_constant(value: str) -> Never:
    _refuse(f"non-finite JSON constant {value!r}")


def _json_bytes(data: bytes, label: str) -> dict[str, object]:
    try:
        value = json.loads(
            data, object_pairs_hook=_unique_object, parse_constant=_reject_constant
        )
    except ReadbackRefusalError:
        raise
    except (UnicodeDecodeError, ValueError) as error:
        raise ReadbackRefusalError(f"{label} is not strict JSON: {error}") from error
    if not isinstance(value, dict):
        _refuse(f"{label} must be a JSON object")
    return cast(dict[str, object], value)


def _json(path: Path, label: str) -> tuple[bytes, dict[str, object]]:
    try:
        data = path.read_bytes()
    except OSError as error:
        raise ReadbackRefusalError(f"cannot read {label}: {error}") from error
    return data, _json_bytes(data, label)


def _artifact_filenames(relative: str) -> set[str]:
    if relative == "normalized-interval-directions":
        return {f"{index}.json" for index in range(RAW_DIRECTIONS)} | {
            f"{index}'.json" for index in range(1, RAW_DIRECTIONS)
        }
    return {f"{index}.json" for index in range(RAW_DIRECTIONS)}


def _mode(path: Path, label: str) -> int:
    try:
        return path.lstat().st_mode
    except OSError as error:
        raise ReadbackRefusalError(f"cannot inspect {label}: {error}") from error


def _preflight_artifacts(output: Path) -> None:
    """Reject absent, extra, linked, or special artifacts before opening any of them."""
    expected_names = {relative for _role, relative, _count, _directory in ARTIFACTS}
    try:
        entries = tuple(output.iterdir())
    except OSError as error:
        raise ReadbackRefusalError(f"cannot enumerate profile output: {error}") from error
    if {entry.name for entry in entries} != expected_names:
        _refuse("retained artifact set has missing or extra entries")
    for _role, relative, _expected_count, directory in ARTIFACTS:
        path = output / relative
        mode = _mode(path, f"artifact {relative}")
        if (
            stat.S_ISLNK(mode)
            or (directory and not stat.S_ISDIR(mode))
            or (not directory and not stat.S_ISREG(mode))
        ):
            _refuse(f"artifact has the wrong type: {relative}")
        if not directory:
            continue
        try:
            children = tuple(path.iterdir())
        except OSError as error:
            raise ReadbackRefusalError(
                f"cannot enumerate artifact {relative}: {error}"
            ) from error
        if {child.name for child in children} != _artifact_filenames(relative):
            _refuse(f"artifact row set changed: {relative}")
        if any(
            not stat.S_ISREG(_mode(child, f"artifact row {relative}/{child.name}"))
            for child in children
        ):
            _refuse(f"artifact row has the wrong type: {relative}")


def _object(value: object, keys: Collection[str], label: str) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != set(keys):
        _refuse(f"{label} fields changed")
    return cast(dict[str, object], value)


def _array(value: object, length: int | None, label: str) -> list[object]:
    if not isinstance(value, list) or (length is not None and len(value) != length):
        _refuse(f"{label} is malformed")
    return cast(list[object], value)


def _hex(value: object, length: int, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != length
        or any(character not in "0123456789abcdef" for character in value)
    ):
        _refuse(f"{label} is malformed")
    return value


def _number(value: object, label: str) -> float:
    if type(value) not in (int, float):
        _refuse(f"{label} is not a finite nonnegative number")
    try:
        result = float(cast(int | float, value))
    except (OverflowError, ValueError) as error:
        raise ReadbackRefusalError(f"{label} is not a finite nonnegative number") from error
    if not math.isfinite(result) or result < 0:
        _refuse(f"{label} is not a finite nonnegative number")
    return result


def _finite_real(value: object, label: str) -> int | float:
    if type(value) not in (int, float):
        _refuse(f"{label} is not a finite real number")
    try:
        finite = math.isfinite(float(cast(int | float, value)))
    except (OverflowError, ValueError) as error:
        raise ReadbackRefusalError(f"{label} is not a finite real number") from error
    if not finite:
        _refuse(f"{label} is not a finite real number")
    return cast(int | float, value)


def _same_typed(actual: object, expected: object) -> bool:
    """Compare a fixed JSON shape without Python's bool/int/float equality aliases."""
    if isinstance(expected, dict):
        return (
            isinstance(actual, dict)
            and actual.keys() == expected.keys()
            and all(_same_typed(actual[key], value) for key, value in expected.items())
        )
    if isinstance(expected, list):
        return (
            isinstance(actual, list)
            and len(actual) == len(expected)
            and all(
                _same_typed(left, right) for left, right in zip(actual, expected, strict=True)
            )
        )
    if type(expected) is float:
        if type(actual) not in (int, float):
            return False
        try:
            return math.isfinite(float(cast(int | float, actual))) and actual == expected
        except OverflowError, ValueError:
            return False
    return type(actual) is type(expected) and actual == expected


def _fraction(value: object, label: str) -> Fraction:
    if not isinstance(value, str):
        _refuse(f"{label} is not a canonical rational")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ReadbackRefusalError(f"{label} is not a canonical rational") from error
    if str(result) != value:
        _refuse(f"{label} is not a canonical rational")
    return result


def _point(value: object, label: str) -> tuple[Fraction, Fraction]:
    row = _array(value, 2, label)
    return _fraction(row[0], label), _fraction(row[1], label)


def _decimal_root(coefficient: Fraction, radicand: int) -> str:
    """Present a positive quadratic root at 15 places, rounded half up."""
    with localcontext() as context:
        context.prec = 50
        value = (
            Decimal(coefficient.numerator)
            * Decimal(radicand).sqrt()
            / Decimal(coefficient.denominator)
        )
        return format(value.quantize(Decimal("0.000000000000001"), rounding=ROUND_HALF_UP), "f")


def _walk_receipt(value: object) -> None:
    if isinstance(value, dict):
        for key, nested in cast(dict[str, object], value).items():
            if key in FORBIDDEN_KEYS:
                _refuse(f"calibration receipt carries forbidden field {key!r}")
            _walk_receipt(nested)
    elif isinstance(value, list):
        for nested in cast(list[object], value):
            _walk_receipt(nested)
    elif isinstance(value, str) and any(term in value for term in FORBIDDEN_VALUES):
        _refuse("calibration receipt carries scientific-target vocabulary")


def _git(repository: Path, *arguments: str, binary: bool = False) -> bytes | str:
    result = subprocess.run(
        ("git", *arguments),
        cwd=repository,
        check=False,
        capture_output=True,
        text=not binary,
    )
    if result.returncode:
        stderr = result.stderr.decode() if binary else cast(str, result.stderr)
        _refuse(stderr.strip() or f"git {' '.join(arguments)} failed")
    return cast(bytes | str, result.stdout)


def _bind_revisions(repository: Path, execution: str, reader: str) -> None:
    _hex(execution, 40, "expected execution revision")
    _hex(reader, 40, "expected reader revision")
    if cast(str, _git(repository, "cat-file", "-t", execution)).strip() != "commit":
        _refuse("expected execution revision is not a Git commit")
    head = cast(str, _git(repository, "rev-parse", "HEAD")).strip()
    if head != reader:
        _refuse("current checkout differs from the expected reader revision")
    relative = "packing/devtools/read_fixed_core_calibration_profile.py"
    expected_entry = (repository / relative).resolve()
    if Path(__file__).resolve() != expected_entry:
        _refuse("running reader comes from another file or checkout")


def _execution_source_paths(repository: Path, revision: str) -> tuple[str, ...]:
    """Discover the local import closure from Git objects at the execution revision."""
    tracked = set(
        cast(str, _git(repository, "ls-tree", "-r", "--name-only", revision)).splitlines()
    )
    roots = {
        "cases": "packing/cases",
        "devtools": "packing/devtools",
        "sqpack": "packing/src/sqpack",
    }

    def module_path(module: str) -> str | None:
        parts = module.split(".")
        root = roots.get(parts[0])
        if root is None:
            return None
        stem = "/".join((root, *parts[1:]))
        for candidate in (f"{stem}.py", f"{stem}/__init__.py"):
            if candidate in tracked:
                return candidate
        return None

    pending = ["devtools.calibrate_fixed_core_packet"]
    visited: set[str] = set()
    paths = {
        FIXTURE_PATH,
        "packing/.python-version",
        "packing/pyproject.toml",
        "packing/uv.lock",
    }
    while pending:
        module = pending.pop()
        if module in visited:
            continue
        path = module_path(module)
        if path is None:
            continue
        visited.add(module)
        paths.add(path)
        data = cast(bytes, _git(repository, "show", f"{revision}:{path}", binary=True))
        try:
            tree = ast.parse(data.decode("utf-8"), filename=path)
        except (UnicodeDecodeError, SyntaxError) as error:
            raise ReadbackRefusalError(
                f"execution dependency cannot be parsed: {path}"
            ) from error
        package = module if path.endswith("/__init__.py") else module.rpartition(".")[0]
        pending.extend(
            ".".join(module.split(".")[:length]) for length in range(1, len(module.split(".")))
        )
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                pending.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                base = node.module or ""
                if node.level:
                    try:
                        base = importlib.util.resolve_name(f"{'.' * node.level}{base}", package)
                    except ImportError as error:
                        raise ReadbackRefusalError(
                            f"execution dependency has invalid relative import: {path}"
                        ) from error
                if base:
                    pending.append(base)
                    pending.extend(f"{base}.{alias.name}" for alias in node.names)
    if not paths.issubset(tracked):
        _refuse("execution revision omits a required fixture or runtime declaration")
    return tuple(sorted(paths))


def _validate_sources(repository: Path, sources: object, execution_revision: str) -> None:
    source = _object(
        sources, {"implementation_revision", "manifest", "runtime"}, "receipt sources"
    )
    if source["implementation_revision"] != execution_revision:
        _refuse("receipt execution revision differs from the expected revision")
    manifest = _array(source["manifest"], None, "source manifest")
    if not manifest:
        _refuse("source manifest is empty")
    paths: set[str] = set()
    for value in manifest:
        row = _object(value, {"path", "git_blob", "sha256"}, "source manifest row")
        path = row["path"]
        if (
            not isinstance(path, str)
            or not path
            or PurePosixPath(path).is_absolute()
            or PurePosixPath(path).as_posix() != path
            or any(part in (".", "..") for part in path.split("/"))
            or path in paths
        ):
            _refuse("source manifest path is malformed or duplicated")
        paths.add(path)
    expected_paths = _execution_source_paths(repository, execution_revision)
    if [cast(dict[str, object], row)["path"] for row in manifest] != list(expected_paths):
        _refuse("source manifest differs from the complete execution import closure")
    # The rows' blob ids and digests are the run's own record of its bytes, history the
    # reader keeps without comparing (development.md, 2026-10-03); the profile's
    # contents are what the reader checks.
    fixture_data = cast(
        bytes,
        _git(repository, "show", f"{execution_revision}:{FIXTURE_PATH}", binary=True),
    )
    if (
        len(fixture_data) != FIXTURE_BYTES
        or hashlib.sha256(fixture_data).hexdigest() != FIXTURE_SHA256
    ):
        _refuse("execution revision does not contain the frozen fixture bytes")
    runtime = _object(source["runtime"], {"python", "packages", "attestation_scope"}, "runtime")
    python = _object(
        runtime["python"],
        {
            "implementation",
            "version",
            "abi",
            "gil_enabled",
            "environment",
            "executable",
            "resolved_executable",
            "build",
        },
        "runtime Python",
    )
    if (
        any(
            not isinstance(python[key], str) or not cast(str, python[key])
            for key in (
                "implementation",
                "version",
                "abi",
                "environment",
                "executable",
                "resolved_executable",
                "build",
            )
        )
        or type(python["gil_enabled"]) is not bool
    ):
        _refuse("runtime Python identity is malformed")
    packages = _object(runtime["packages"], {"numpy", "strif"}, "runtime packages")
    if not all(isinstance(value, str) and value for value in packages.values()):
        _refuse("runtime package versions are malformed")
    if runtime["attestation_scope"] != RUNTIME_SCOPE:
        _refuse("runtime attestation scope changed")


def _rotation(index: int, *, reflected: bool = False) -> tuple[Fraction, Fraction]:
    tangent = Fraction(index, 5_760)
    denominator = 1 + tangent * tangent
    cosine = (1 - tangent * tangent) / denominator
    sine = 2 * tangent / denominator
    return (sine, cosine) if reflected else (cosine, sine)


def _charge(
    label: str, witness: tuple[Fraction, Fraction], *, normalized: bool
) -> tuple[Fraction, bool]:
    reflected = label.endswith("'")
    index = int(label.rstrip("'"))
    if not 0 <= index <= STEPS:
        _refuse(f"direction label is outside the frozen net: {label}")
    cosine, sine = _rotation(index, reflected=reflected)
    u, v = witness
    x = cosine * u - sine * v
    y = sine * u + cosine * v
    margin = CORE_SIDE * (cosine + sine) / 2
    admissible = margin <= x <= OUTER_SIDE - margin and margin <= y <= OUTER_SIDE - margin
    half = CORE_SIDE / 2

    def contains(point: tuple[Fraction, Fraction]) -> bool:
        px, py = point
        return (
            abs(cosine * px + sine * py - u) <= half
            and abs(-sine * px + cosine * py - v) <= half
        )

    scale = NORMALIZATION if normalized else Fraction(1)
    charge = Fraction(1, 2) * scale if contains(POINT) else Fraction(0)
    for sites in (HORIZONTAL, VERTICAL):
        if sum(contains(site) for site in sites) >= 2:
            charge += Fraction(3, 4) * scale
    return charge, admissible


def _direction_digest(paths: Sequence[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        data = path.read_bytes()
        name = path.name.encode()
        digest.update(len(name).to_bytes(4, "big"))
        digest.update(name)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def _files(directory: Path, labels: Sequence[str], label: str) -> tuple[Path, ...]:
    if directory.is_symlink() or not directory.is_dir():
        _refuse(f"{label} is not a retained directory")
    expected = {f"{item}.json" for item in labels}
    actual = {item.name for item in directory.iterdir()}
    if actual != expected or any(
        item.is_symlink() or not item.is_file() for item in directory.iterdir()
    ):
        _refuse(f"{label} has missing, extra, or non-file rows")
    return tuple(directory / f"{item}.json" for item in labels)


def _read_rows(output: Path, receipt: dict[str, object]) -> dict[str, object]:
    labels = [str(index) for index in range(RAW_DIRECTIONS)]
    interval_labels = labels + [f"{index}'" for index in range(1, RAW_DIRECTIONS)]
    raw_paths = _files(output / "raw-directions", labels, "raw directions")
    exact_paths = _files(
        output / "normalized-exact-directions", labels, "normalized exact directions"
    )
    interval_paths = _files(
        output / "normalized-interval-directions", interval_labels, "interval directions"
    )
    dilation_paths = _files(output / "dilation-directions", labels, "dilation directions")

    first_raw: tuple[Fraction, Fraction] | None = None
    first_exact: tuple[Fraction, Fraction] | None = None
    boxes = 0
    for index, path in enumerate(raw_paths):
        _data, row = _json(path, f"raw row {index}")
        _object(row, {"direction", "charge", "witness"}, f"raw row {index}")
        witness = _point(row["witness"], f"raw witness {index}")
        charge, admissible = _charge(str(index), witness, normalized=False)
        if (
            not _same_typed(row["direction"], index)
            or _fraction(row["charge"], "raw charge") != charge
        ):
            _refuse(f"raw row differs from exact membership at direction {index}")
        if charge != RAW_MINIMUM or not admissible:
            _refuse(f"raw witness is not an admissible known answer at direction {index}")
        first_raw = witness if first_raw is None else first_raw

    for index, path in enumerate(exact_paths):
        _data, row = _json(path, f"exact row {index}")
        _object(
            row,
            {"direction", "dense", "slab", "agree", "witness", "slab_witness"},
            f"exact row {index}",
        )
        dense_witness = _point(row["witness"], f"exact witness {index}")
        slab_witness = _point(row["slab_witness"], f"slab witness {index}")
        dense = _fraction(row["dense"], "dense charge")
        slab = _fraction(row["slab"], "slab charge")
        dense_replay = _charge(str(index), dense_witness, normalized=True)
        slab_replay = _charge(str(index), slab_witness, normalized=True)
        if (
            not _same_typed(row["direction"], index)
            or type(row["agree"]) is not bool
            or row["agree"] is not True
            or dense != slab
            or dense_witness != slab_witness
            or dense != NORMALIZED_MINIMUM
            or dense_replay != (dense, True)
            or slab_replay != (slab, True)
        ):
            _refuse(f"normalized exact row fails independent replay at direction {index}")
        first_exact = dense_witness if first_exact is None else first_exact

    for label, path in zip(interval_labels, interval_paths, strict=True):
        _data, row = _json(path, f"interval row {label}")
        _object(
            row,
            {
                "label",
                "status",
                "lower",
                "upper",
                "witness",
                "boxes",
                "stalled",
                "budget_exhausted",
            },
            f"interval row {label}",
        )
        witness_values = _array(row["witness"], 2, f"interval witness {label}")
        coordinates = [
            _finite_real(value, f"interval witness {label}") for value in witness_values
        ]
        witness = (
            Fraction(coordinates[0]),
            Fraction(coordinates[1]),
        )
        replay = _charge(label, witness, normalized=True)
        if (
            row["label"] != label
            or row["status"] != "certified"
            or not _same_typed(row["lower"], INTEGER_SCALE)
            or not _same_typed(row["upper"], INTEGER_SCALE)
            or type(row["boxes"]) is not int
            or cast(int, row["boxes"]) <= 0
            or not _same_typed(row["stalled"], 0)
            or row["budget_exhausted"] is not False
            or replay != (NORMALIZED_MINIMUM, True)
        ):
            _refuse(f"interval row fails independent replay at direction {label}")
        boxes += cast(int, row["boxes"])

    for index, path in enumerate(dilation_paths):
        _data, row = _json(path, f"dilation row {index}")
        expected = {"direction": index, "label": str(index), "minimum": "1"}
        if not _same_typed(row, expected):
            _refuse(f"dilation row differs from the normalized answer at direction {index}")

    if first_raw is None or first_exact is None:
        _refuse("raw or normalized exact route has no retained rows")

    raw_receipt = _object(
        receipt["raw"],
        {
            "directions_expected",
            "directions_completed",
            "completed_directions",
            "observed_minimum_upper_bound",
            "observed_argmin",
            "observed_witness",
            "raw_minimum",
            "budget",
            "threshold_M_over_n",
            "comparison",
            "witness_replay_charge",
            "witness_admissible",
            "directions_sha256",
        },
        "raw receipt",
    )
    if not _same_typed(
        raw_receipt,
        {
            "directions_expected": RAW_DIRECTIONS,
            "directions_completed": RAW_DIRECTIONS,
            "completed_directions": list(range(RAW_DIRECTIONS)),
            "observed_minimum_upper_bound": "2",
            "observed_argmin": 0,
            "observed_witness": [str(first_raw[0]), str(first_raw[1])],
            "raw_minimum": "2",
            "budget": "2",
            "threshold_M_over_n": "1",
            "comparison": "passed",
            "witness_replay_charge": "2",
            "witness_admissible": True,
            "directions_sha256": _direction_digest(raw_paths),
        },
    ):
        _refuse("raw receipt does not reconstruct from every retained row")

    routes = _object(
        receipt["routes"], {"normalized_exact", "reflected_interval", "dilation"}, "routes"
    )
    candidate_sha = hashlib.sha256((output / "candidate.json").read_bytes()).hexdigest()
    common_int = {
        "status": "complete",
        "source_sha256": candidate_sha,
        "directions_expected": RAW_DIRECTIONS,
        "directions_completed": RAW_DIRECTIONS,
    }
    exact = _object(
        routes["normalized_exact"],
        {
            "status",
            "source_sha256",
            "directions_expected",
            "directions_completed",
            "completed_directions",
            "minimum",
            "argmin",
            "witness",
            "dense_slab_disagreements",
            "directions_sha256",
        },
        "normalized exact route",
    )
    if not _same_typed(
        exact,
        common_int
        | {
            "completed_directions": list(range(RAW_DIRECTIONS)),
            "minimum": "1",
            "argmin": 0,
            "witness": [str(first_exact[0]), str(first_exact[1])],
            "dense_slab_disagreements": 0,
            "directions_sha256": _direction_digest(exact_paths),
        },
    ):
        _refuse("normalized exact receipt does not reconstruct")
    interval = _object(
        routes["reflected_interval"],
        {
            "status",
            "source_sha256",
            "directions_expected",
            "directions_completed",
            "completed_directions",
            "integer_scale",
            "integer_enclosure",
            "enclosure",
            "stalled",
            "budget_exhausted",
            "accepted",
            "boxes_observed",
            "directions_sha256",
        },
        "interval route",
    )
    if not _same_typed(
        interval,
        {
            "status": "complete",
            "source_sha256": candidate_sha,
            "directions_expected": INTERVAL_DIRECTIONS,
            "directions_completed": INTERVAL_DIRECTIONS,
            "completed_directions": interval_labels,
            "integer_scale": INTEGER_SCALE,
            "integer_enclosure": [INTEGER_SCALE, INTEGER_SCALE],
            "enclosure": ["1", "1"],
            "stalled": 0,
            "budget_exhausted": 0,
            "accepted": True,
            "boxes_observed": boxes,
            "directions_sha256": _direction_digest(interval_paths),
        },
    ):
        _refuse("interval receipt does not reconstruct")
    dilation = _object(
        routes["dilation"],
        {
            "status",
            "source_sha256",
            "directions_expected",
            "directions_completed",
            "completed_directions",
            "directions_sha256",
            "record_sha256",
            "generic_record_schema",
            "generic_record_scope",
            "factor_supremum",
            "factor_supremum_squared",
            "bounded_side",
            "bounded_side_squared",
            "relation",
            "endpoint_certificate",
            "requires_compactness",
        },
        "dilation route",
    )
    dilation_raw = (output / "dilation.json").read_bytes()
    expected_dilation = common_int | {
        "completed_directions": labels,
        "directions_sha256": _direction_digest(dilation_paths),
        "record_sha256": hashlib.sha256(dilation_raw).hexdigest(),
        "generic_record_schema": DILATION_SCHEMA,
        "generic_record_scope": (
            "valid normalized n=2 calibration fixture; no campaign or fixed-packet evidence"
        ),
        "factor_supremum": "2*sqrt(33177601)/5761",
        "factor_supremum_squared": str(FACTOR_SQUARED),
        "bounded_side": "3*sqrt(33177601)/11522",
        "bounded_side_squared": str(SIDE_SQUARED),
        "relation": ">=",
        "endpoint_certificate": False,
        "requires_compactness": False,
    }
    if not _same_typed(dilation, expected_dilation):
        _refuse("dilation receipt does not reconstruct")
    return {
        "raw": _direction_digest(raw_paths),
        "normalized_exact": _direction_digest(exact_paths),
        "reflected_interval": _direction_digest(interval_paths),
        "dilation": _direction_digest(dilation_paths),
        "boxes_observed": boxes,
    }


def _expected_candidate() -> dict[str, object]:
    return {
        "id": NORMALIZED_ID,
        "variant": "threshold",
        "n": N,
        "claim": "s(2) >= 3/4",
        "outer_side": "3/4",
        "square_side": "1/2",
        "angle_limit": "1/2",
        "direction_steps": STEPS,
        "symmetry": "D4",
        "point_mass": "1/4",
        "threshold_budget": "3/4",
        "total_budget": "1",
        "atoms": [["3/8", "3/8", "1/4"]],
        "threshold_atoms": [
            {
                "points": [["3/16", "3/8"], ["3/8", "3/8"], ["9/16", "3/8"]],
                "threshold": 2,
                "weight": "3/8",
            },
            {
                "points": [["3/8", "3/16"], ["3/8", "3/8"], ["3/8", "9/16"]],
                "threshold": 2,
                "weight": "3/8",
            },
        ],
        "provenance": {
            "kind": "normalized synthetic fixed-core packet calibration fixture",
            "construction": FIXTURE_PROVENANCE["construction"],
            "purpose": FIXTURE_PROVENANCE["purpose"],
            "derived_from": FIXTURE_PATH,
            "source_id": FIXTURE_ID,
            "normalization": "every weight multiplied by 1/2 after raw minimum 2",
        },
        "least_cell_charge": "1",
    }


def _validate_candidate(output: Path, receipt: dict[str, object]) -> None:
    data, candidate = _json(output / "candidate.json", "normalized candidate")
    if not _same_typed(candidate, _expected_candidate()):
        _refuse("normalized candidate geometry or weights changed")
    point_weights = [
        Fraction(cast(str, row[2])) for row in cast(list[list[str]], candidate["atoms"])
    ]
    threshold_atoms = cast(list[dict[str, object]], candidate["threshold_atoms"])
    threshold_budget = sum(
        (
            Fraction(cast(str, row["weight"]))
            * (len(cast(list[object], row["points"])) // cast(int, row["threshold"]))
            for row in threshold_atoms
        ),
        start=Fraction(0),
    )
    derived_scale = math.lcm(
        *(weight.denominator for weight in point_weights),
        *(Fraction(cast(str, row["weight"])).denominator for row in threshold_atoms),
    )
    if RAW_BUDGET / N != 1 or RAW_MINIMUM <= RAW_BUDGET / N:
        _refuse("raw strict comparison no longer permits normalization")
    if (
        sum(point_weights, start=Fraction(0)) + threshold_budget != NORMALIZED_BUDGET
        or derived_scale != INTEGER_SCALE
        or NORMALIZATION * RAW_BUDGET != NORMALIZED_BUDGET
        or NORMALIZATION * RAW_MINIMUM != NORMALIZED_MINIMUM
    ):
        _refuse("normalization does not reconstruct the normalized budget")
    normalized = _object(
        receipt["normalized"],
        {
            "path",
            "sha256",
            "source_fixture_sha256",
            "id",
            "alpha",
            "point_mass",
            "threshold_budget",
            "total_budget",
            "least_cell_charge",
            "integer_scale",
            "closed_form_conditions",
        },
        "normalized receipt",
    )
    conditions = _array(normalized["closed_form_conditions"], 5, "closed-form conditions")
    for condition in conditions:
        row = _object(condition, {"name", "detail", "holds"}, "closed-form condition")
        if (
            not isinstance(row["name"], str)
            or not isinstance(row["detail"], str)
            or row["holds"] is not True
        ):
            _refuse("normalized closed-form condition is malformed or false")
    expected_names = [
        "Condition 1 atoms carry the declared symmetry",
        "Condition 1' threshold atoms carry the declared symmetry",
        "Condition 2' total budget below n",
        "Condition 3 net reaches pi/4",
        "Condition 4 containment B(1 + D) < 1",
    ]
    if [cast(dict[str, object], row)["name"] for row in conditions] != expected_names:
        _refuse("normalized closed-form condition set changed")
    expected = {
        "path": "candidate.json",
        "sha256": hashlib.sha256(data).hexdigest(),
        "source_fixture_sha256": FIXTURE_SHA256,
        "id": NORMALIZED_ID,
        "alpha": "1/2",
        "point_mass": "1/4",
        "threshold_budget": "3/4",
        "total_budget": "1",
        "least_cell_charge": "1",
        "integer_scale": INTEGER_SCALE,
        "closed_form_conditions": conditions,
    }
    if not _same_typed(normalized, expected):
        _refuse("normalized receipt differs from candidate bytes")


def _validate_dilation(output: Path) -> None:
    _data, record = _json(output / "dilation.json", "dilation record")
    _object(
        record,
        {
            "schema",
            "source",
            "sharpened_containment",
            "strict_dilation_family",
            "conclusion",
            "proof",
        },
        "dilation record",
    )
    source = _object(
        record["source"],
        {
            "certificate",
            "sha256",
            "n",
            "outer_side",
            "square_side",
            "half_gap_tangent",
            "coarse_containment",
            "total_budget",
            "minimum_cell_charge",
            "accepted_conditions",
            "variant",
            "point_atoms",
            "threshold_atoms",
        },
        "dilation source",
    )
    candidate = (output / "candidate.json").read_bytes()
    if (
        not _same_typed(
            source,
            {
                "certificate": "candidate.json",
                "sha256": hashlib.sha256(candidate).hexdigest(),
                "n": N,
                "outer_side": "3/4",
                "square_side": "1/2",
                "half_gap_tangent": "1/5760",
                "coarse_containment": "5761/11520",
                "total_budget": "1",
                "minimum_cell_charge": "1",
                "accepted_conditions": [
                    "Condition 1 atoms carry the declared symmetry",
                    "Condition 1' threshold atoms carry the declared symmetry",
                    "Condition 2' total budget below n",
                    "Condition 3 net reaches pi/4",
                    "Condition 4 containment B(1 + D) < 1",
                    "Condition 5' every reachable cell is charged at least 1",
                ],
                "variant": "threshold",
                "point_atoms": 1,
                "threshold_atoms": 2,
            },
        )
        or record["schema"] != DILATION_SCHEMA
    ):
        _refuse("dilation source does not reconstruct from the normalized fixture")
    containment = _object(
        record["sharpened_containment"],
        {
            "identity",
            "gap_domain",
            "monotonicity_identity",
            "strict_factor_test",
            "strict_factor_test_left_multiplier",
            "strict_factor_test_right",
            "source_gap_below_one",
        },
        "sharpened containment",
    )
    left = CORE_SIDE**2 * (1 + HALF_GAP) ** 2
    right = 1 + HALF_GAP**2
    factor_squared = right / left
    side_squared = OUTER_SIDE**2 * factor_squared
    if factor_squared != FACTOR_SQUARED or side_squared != SIDE_SQUARED:
        _refuse("dilation containment algebra changed")
    expected_containment = {
        "identity": "cos(d) + sin(d) = (1 + t) / sqrt(1 + t^2), where t = tan(d)",
        "gap_domain": f"0 <= t <= D = {HALF_GAP} < 1",
        "monotonicity_identity": (
            "(1 + D)^2(1 + t^2) - (1 + t)^2(1 + D^2) = 2(D - t)(1 - Dt) >= 0"
        ),
        "strict_factor_test": f"q^2 * {left} < {right}",
        "strict_factor_test_left_multiplier": str(left),
        "strict_factor_test_right": str(right),
        "source_gap_below_one": True,
    }
    if not _same_typed(containment, expected_containment):
        _refuse("dilation containment statement changed")
    family = _object(
        record["strict_dilation_family"],
        {
            "factor_supremum",
            "factor_supremum_squared",
            "factor_supremum_decimal",
            "factor_supremum_irrational",
            "factor_supremum_defining_polynomial",
            "factor_domain",
            "scaled_containment_test",
            "invariants",
        },
        "strict dilation family",
    )
    conclusion = _object(
        record["conclusion"],
        {
            "bounded_side",
            "bounded_side_squared",
            "bounded_side_defining_polynomial",
            "decimal",
            "relation",
            "endpoint_certificate",
        },
        "dilation conclusion",
    )
    proof = _object(
        record["proof"],
        {
            "strict_family",
            "density_step",
            "embedding_step",
            "order_step",
            "requires_compactness",
            "endpoint_status",
        },
        "dilation proof",
    )
    denominator_root = math.isqrt(factor_squared.denominator)
    radicand = factor_squared.numerator // 4
    factor_coefficient = Fraction(2, denominator_root)
    side_coefficient = OUTER_SIDE * factor_coefficient
    if (
        denominator_root**2 != factor_squared.denominator
        or factor_coefficient**2 * radicand != factor_squared
        or side_coefficient**2 * radicand != side_squared
        or math.isqrt(radicand) ** 2 == radicand
    ):
        _refuse("dilation positive-root representation is inconsistent")
    factor_exact = (
        f"{factor_coefficient.numerator}*sqrt({radicand})/{factor_coefficient.denominator}"
    )
    side_exact = f"{side_coefficient.numerator}*sqrt({radicand})/{side_coefficient.denominator}"
    expected_family = {
        "factor_supremum": factor_exact,
        "factor_supremum_squared": str(factor_squared),
        "factor_supremum_decimal": _decimal_root(factor_coefficient, radicand),
        "factor_supremum_irrational": True,
        "factor_supremum_defining_polynomial": (
            f"{factor_squared.denominator}*x^2 - {factor_squared.numerator}"
        ),
        "factor_domain": f"q in Q with q > 0 and q^2 < {factor_squared}",
        "scaled_containment_test": (
            "q^2 B^2 (1 + D)^2 < 1 + D^2; this rational inequality is "
            "equivalent to strict geometric containment"
        ),
        "invariants": [
            (
                "Conditions 1 and 1' D4 symmetry of the point and threshold atoms "
                "is equivariant under common scaling"
            ),
            "Conditions 2' and 3 (total budget and direction net) are unchanged",
            (
                "Condition 5' charge is preserved by inverse dilation of placements: "
                "a core's trace on each threshold atom's scaled points is unchanged"
            ),
        ],
    }
    expected_conclusion = {
        "bounded_side": side_exact,
        "bounded_side_squared": str(side_squared),
        "bounded_side_defining_polynomial": (
            f"{side_squared.denominator}*x^2 - {side_squared.numerator}"
        ),
        "decimal": _decimal_root(side_coefficient, radicand),
        "relation": ">=",
        "endpoint_certificate": False,
    }
    expected_proof = {
        "strict_family": (
            "for every rational q > 0 with q^2 below factor_supremum_squared, "
            "the sharpened containment theorem and the scaled source data rule out "
            "a packing at side q * outer_side"
        ),
        "density_step": (
            "for every real x below bounded_side, rational density supplies q with "
            "x / outer_side < q < factor_supremum"
        ),
        "embedding_step": (
            "a packing at side x embeds in the larger side q * outer_side, "
            "contradicting that strict-subfactor no-fit proof"
        ),
        "order_step": (
            "equivalently, s(n) is at least every strict rational subbound and "
            "therefore at least their real supremum"
        ),
        "requires_compactness": False,
        "endpoint_status": (
            f"the dilation-limit theorem establishes s({N}) >= {side_exact}; "
            "at the factor supremum the sharpened containment inequality is equality, "
            "so endpoint_certificate is false because the proof supplies no individual "
            f"certificate at that side; the method does not establish s({N}) > "
            f"{side_exact}"
        ),
    }
    if not all(
        _same_typed(actual, expected)
        for actual, expected in (
            (family, expected_family),
            (conclusion, expected_conclusion),
            (proof, expected_proof),
        )
    ):
        _refuse("dilation surd, presentation, or proof semantics changed")


def _maximum_simultaneous(tasks: list[dict[str, object]], label: str) -> int:
    active: set[int] = set()
    maximum = 0
    events = sorted(
        (when, order, cast(int, task["pid"]))
        for task in tasks
        for when, order in (
            (cast(float, task["finished_seconds"]), 0),
            (cast(float, task["started_seconds"]), 1),
        )
    )
    for _when, order, pid in events:
        if order == 0:
            if pid not in active:
                _refuse(f"{label} task lifetimes overlap for one child")
            active.remove(pid)
        else:
            if pid in active:
                _refuse(f"{label} task lifetimes overlap for one child")
            active.add(pid)
            maximum = max(maximum, len(active))
    if active:
        _refuse(f"{label} task lifetimes are unbalanced")
    return maximum


def _not_later(first: float, second: float) -> bool:
    """Allow only roundoff in differences of measured monotonic clocks."""
    if not math.isfinite(first) or not math.isfinite(second):
        return False
    return first <= second or first - second <= 8 * max(math.ulp(first), math.ulp(second))


def _validate_topology_route(
    route: object,
    *,
    phase: str,
    workers: int,
    coordinator: dict[str, object],
    worker_elapsed: float,
    phase_duration: float,
) -> dict[str, object]:
    row = _object(
        route,
        {
            "phase",
            "execution_model",
            "configured_workers",
            "directions_expected",
            "directions_completed",
            "child_tasks_observed",
            "observed_child_count",
            "maximum_simultaneous_children",
            "tasks",
            "children",
        },
        f"{phase} topology route",
    )
    if (
        row["phase"] != phase
        or any(
            type(row[key]) is not int
            for key in (
                "configured_workers",
                "directions_expected",
                "directions_completed",
                "child_tasks_observed",
                "observed_child_count",
                "maximum_simultaneous_children",
            )
        )
        or row["configured_workers"] != workers
        or row["directions_expected"] != RAW_DIRECTIONS
        or row["directions_completed"] != RAW_DIRECTIONS
    ):
        _refuse(f"{phase} topology route identity changed")
    tasks = _array(row["tasks"], None, f"{phase} tasks")
    children = _array(row["children"], None, f"{phase} children")
    parsed_tasks: list[dict[str, object]] = []
    for value in tasks:
        task = _object(
            value,
            {"direction", "pid", "ppid", "pgid", "started_seconds", "finished_seconds"},
            f"{phase} task",
        )
        _number(task["started_seconds"], "task start")
        _number(task["finished_seconds"], "task finish")
        if (
            type(task["direction"]) is not int
            or not 0 <= cast(int, task["direction"]) < RAW_DIRECTIONS
            or type(task["pid"]) is not int
            or cast(int, task["pid"]) <= 0
            or type(task["ppid"]) is not int
            or type(task["pgid"]) is not int
            or task["ppid"] != coordinator["pid"]
            or task["pgid"] != coordinator["pgid"]
            or task["pid"] == coordinator["pid"]
            or task["pid"] == coordinator["ppid"]
            or task["pid"] == task["ppid"]
            or cast(float, task["started_seconds"]) < 0
            or cast(float, task["finished_seconds"]) <= cast(float, task["started_seconds"])
            or not _not_later(cast(float, task["finished_seconds"]), worker_elapsed)
        ):
            _refuse(f"{phase} task is malformed")
        parsed_tasks.append(task)
    if workers == 1:
        if (
            tasks
            or children
            or row["execution_model"] != "coordinator-serial"
            or any(
                row[key] != 0
                for key in (
                    "child_tasks_observed",
                    "observed_child_count",
                    "maximum_simultaneous_children",
                )
            )
        ):
            _refuse(f"serial {phase} topology is incoherent")
        return {
            "configured_workers": 1,
            "execution_model": "coordinator-serial",
            "observed_child_count": 0,
            "maximum_simultaneous_children": 0,
        }
    directions = [task["direction"] for task in parsed_tasks]
    if directions != list(range(RAW_DIRECTIONS)):
        _refuse(f"{phase} tasks do not bind every direction")
    parsed_children: list[dict[str, object]] = []
    for value in children:
        child = _object(
            value,
            {
                "role",
                "phase",
                "pid",
                "ppid",
                "pgid",
                "tasks_completed",
                "first_task_started_seconds",
                "last_task_finished_seconds",
            },
            f"{phase} child",
        )
        if (
            child["role"] != "route-worker"
            or child["phase"] != phase
            or type(child["pid"]) is not int
            or cast(int, child["pid"]) <= 0
            or type(child["ppid"]) is not int
            or type(child["pgid"]) is not int
            or child["ppid"] != coordinator["pid"]
            or child["pgid"] != coordinator["pgid"]
            or child["pid"] == coordinator["pid"]
            or child["pid"] == coordinator["ppid"]
            or child["pid"] == child["ppid"]
            or type(child["tasks_completed"]) is not int
            or cast(int, child["tasks_completed"]) <= 0
            or _number(child["first_task_started_seconds"], "child first task") < 0
            or _number(child["last_task_finished_seconds"], "child last task")
            < cast(float, child["first_task_started_seconds"])
        ):
            _refuse(f"{phase} child identity is malformed")
        parsed_children.append(child)
    pids = sorted({cast(int, task["pid"]) for task in parsed_tasks})
    expected_children = []
    for pid in pids:
        owned = [task for task in parsed_tasks if task["pid"] == pid]
        expected_children.append(
            {
                "role": "route-worker",
                "phase": phase,
                "pid": pid,
                "ppid": coordinator["pid"],
                "pgid": coordinator["pgid"],
                "tasks_completed": len(owned),
                "first_task_started_seconds": min(
                    cast(float, task["started_seconds"]) for task in owned
                ),
                "last_task_finished_seconds": max(
                    cast(float, task["finished_seconds"]) for task in owned
                ),
            }
        )
    maximum = _maximum_simultaneous(parsed_tasks, phase)
    span = max(cast(float, task["finished_seconds"]) for task in parsed_tasks) - min(
        cast(float, task["started_seconds"]) for task in parsed_tasks
    )
    if (
        not _same_typed(parsed_children, expected_children)
        or not _not_later(span, phase_duration)
        or row["execution_model"] != "process-pool"
        or row["child_tasks_observed"] != RAW_DIRECTIONS
        or row["observed_child_count"] != len(pids)
        or row["maximum_simultaneous_children"] != maximum
        or not 1 <= len(pids) <= workers
    ):
        _refuse(f"{phase} topology does not reconstruct")
    return {
        "configured_workers": workers,
        "execution_model": "process-pool",
        "observed_child_count": len(pids),
        "maximum_simultaneous_children": maximum,
    }


def _validate_topology(output: Path, receipt: dict[str, object]) -> dict[str, object]:
    resources = cast(dict[str, object], receipt["resources"])
    summary = _object(
        resources["worker_topology"],
        {"schema", "scope", "coordinator", "routes"},
        "worker topology summary",
    )
    coordinator = _object(
        summary["coordinator"], {"role", "pid", "ppid", "pgid"}, "topology coordinator"
    )
    if (
        coordinator["role"] != "coordinator"
        or type(coordinator["pid"]) is not int
        or cast(int, coordinator["pid"]) <= 0
        or type(coordinator["ppid"]) is not int
        or cast(int, coordinator["ppid"]) <= 0
        or type(coordinator["pgid"]) is not int
        or coordinator["pgid"] != coordinator["pid"]
        or coordinator["ppid"] == coordinator["pid"]
    ):
        _refuse("topology coordinator is malformed")
    if (
        summary["schema"] != "fixed-core-packet-calibration-worker-topology/v1"
        or summary["scope"] != TOPOLOGY_SCOPE
    ):
        _refuse("worker topology schema or scope changed")
    settings = cast(dict[str, object], receipt["settings"])
    clocks = cast(dict[str, object], receipt["clocks"])
    worker_elapsed = _number(clocks["worker_elapsed_seconds"], "worker elapsed")
    configured = cast(dict[str, object], settings["effective_workers"])
    summaries = _object(summary["routes"], {"raw", "normalized_exact"}, "topology routes")
    result: dict[str, object] = {}
    spans: dict[str, tuple[float, float]] = {}
    for name, phase, filename in (
        ("raw", "raw-sweep", "raw-worker-topology.json"),
        ("normalized_exact", "normalized-exact", "normalized-exact-worker-topology.json"),
    ):
        data, sidecar = _json(output / filename, filename)
        _object(sidecar, {"schema", "scope", "coordinator", "route"}, filename)
        if (
            sidecar["schema"] != "fixed-core-packet-calibration-worker-route/v1"
            or sidecar["scope"] != TOPOLOGY_SCOPE
            or not _same_typed(sidecar["coordinator"], coordinator)
        ):
            _refuse(f"{filename} identity changed")
        derived = _validate_topology_route(
            sidecar["route"],
            phase=phase,
            workers=cast(int, configured[name]),
            coordinator=coordinator,
            worker_elapsed=worker_elapsed,
            phase_duration=_number(
                clocks["raw_seconds" if name == "raw" else "exact_seconds"],
                f"{name} phase duration",
            ),
        )
        route = cast(dict[str, object], sidecar["route"])
        tasks = cast(list[dict[str, object]], route["tasks"])
        if tasks:
            spans[name] = (
                min(cast(float, task["started_seconds"]) for task in tasks),
                max(cast(float, task["finished_seconds"]) for task in tasks),
            )
        expected = derived | {
            "record_path": filename,
            "record_sha256": hashlib.sha256(data).hexdigest(),
        }
        if not _same_typed(summaries[name], expected):
            _refuse(f"{name} topology summary does not reconstruct")
        result[name] = derived
    if (
        "raw" in spans
        and "normalized_exact" in spans
        and not _not_later(spans["raw"][1], spans["normalized_exact"][0])
    ):
        _refuse("normalized exact tasks precede raw task completion")
    # Each duration occupies one sequential worker phase. A task span can slide
    # within its phase, but no phase may start before its predecessor completes.
    earliest_start = 0.0
    for phase, key in (
        (None, "preflight_seconds"),
        ("raw", "raw_seconds"),
        (None, "normalization_publication_seconds"),
        ("normalized_exact", "exact_seconds"),
        (None, "interval_seconds"),
        (None, "dilation_seconds"),
        (None, "full_readback_seconds"),
    ):
        duration = _number(clocks[key], f"{key} duration")
        if phase is not None and phase in spans:
            observed_start, observed_finish = spans[phase]
            earliest_start = max(earliest_start, observed_finish - duration)
            if not _not_later(earliest_start, observed_start):
                _refuse(f"{phase} tasks cannot fit their sequential worker phase")
        earliest_start = _number(earliest_start + duration, "worker phase schedule")
    if not _not_later(earliest_start, worker_elapsed):
        _refuse("worker phases and task observations exceed worker lifetime")
    supervision = cast(dict[str, object], receipt["supervision"])
    if (
        supervision["coordinator_pid"] != coordinator["pid"]
        or supervision["coordinator_process_group_id"] != coordinator["pgid"]
    ):
        _refuse("worker topology differs from parent supervision")
    return result


def _validate_resources(output: Path, receipt: dict[str, object]) -> dict[str, object]:
    resources = _object(
        receipt["resources"],
        {
            "cpu_scope",
            "cpu_observations",
            "coordinator_process_seconds",
            "reaped_direct_children_user_seconds",
            "reaped_direct_children_system_seconds",
            "rss",
            "worker_topology",
        },
        "resources",
    )
    if resources["cpu_scope"] != CPU_SCOPE:
        _refuse("CPU scope changed")
    observations = _object(
        resources["cpu_observations"],
        {
            "coordinator_start_seconds",
            "coordinator_end_seconds",
            "direct_children_user_start_seconds",
            "direct_children_user_end_seconds",
            "direct_children_system_start_seconds",
            "direct_children_system_end_seconds",
        },
        "CPU observations",
    )
    cpu_pairs = (
        ("coordinator_start_seconds", "coordinator_end_seconds", "coordinator_process_seconds"),
        (
            "direct_children_user_start_seconds",
            "direct_children_user_end_seconds",
            "reaped_direct_children_user_seconds",
        ),
        (
            "direct_children_system_start_seconds",
            "direct_children_system_end_seconds",
            "reaped_direct_children_system_seconds",
        ),
    )
    cpu: dict[str, float] = {}
    for start, end, elapsed in cpu_pairs:
        start_value = _number(observations[start], start)
        end_value = _number(observations[end], end)
        elapsed_value = _number(resources[elapsed], elapsed)
        if end_value < start_value or not math.isclose(
            end_value - start_value, elapsed_value, rel_tol=1e-12, abs_tol=1e-12
        ):
            _refuse("CPU summary does not reconstruct from retained observations")
        cpu[elapsed] = elapsed_value
    rss = _object(
        resources["rss"],
        {
            "scope",
            "sample_interval_seconds",
            "minimum_terminal_samples",
            "sample_count",
            "positive_sample_count",
            "maximum_actual_gap_seconds",
            "observation_lifetime_seconds",
            "unobserved_leading_seconds",
            "unobserved_trailing_seconds",
            "peak_sampled_rss_bytes",
            "peak_sample_time_seconds",
            "observed_pids",
            "pids_by_phase",
            "observed_phases",
            "unobserved_phases",
            "observer_errors",
            "samples_path",
            "samples_sha256",
        },
        "RSS summary",
    )
    data, record = _json(output / "rss-samples.json", "RSS samples")
    _object(record, {"schema", "samples"}, "RSS sample record")
    if record["schema"] != "fixed-core-packet-calibration-rss/v1":
        _refuse("RSS schema changed")
    samples = _array(record["samples"], None, "RSS samples")
    parsed: list[dict[str, object]] = []
    for value in samples:
        sample = _object(
            value, {"elapsed_seconds", "phase", "pids", "rss_bytes", "error"}, "RSS sample"
        )
        _number(sample["elapsed_seconds"], "RSS sample time")
        pids = _array(sample["pids"], None, "RSS PIDs")
        if (
            not isinstance(sample["phase"], str)
            or sample["phase"] not in OBSERVABLE_PHASES
            or any(type(pid) is not int or cast(int, pid) <= 0 for pid in pids)
            or pids != sorted(set(cast(list[int], pids)))
            or type(sample["rss_bytes"]) is not int
            or cast(int, sample["rss_bytes"]) < 0
            or (sample["error"] is not None and not isinstance(sample["error"], str))
        ):
            _refuse("RSS sample is malformed")
        parsed.append(sample)
    times = [float(cast(int | float, row["elapsed_seconds"])) for row in parsed]
    if times != sorted(times):
        _refuse("RSS sample times are not monotonic")
    lifetime = _number(rss["observation_lifetime_seconds"], "RSS observation lifetime")
    if times and times[-1] > lifetime:
        _refuse("RSS sample follows its observation lifetime")
    errors = [cast(str, row["error"]) for row in parsed if row["error"] is not None]
    positive = sum(
        bool(cast(list[int], row["pids"]))
        and cast(int, row["rss_bytes"]) > 0
        and row["error"] is None
        for row in parsed
    )
    peak = max(parsed, key=lambda row: cast(int, row["rss_bytes"]), default=None)
    observed_pids = sorted(
        {cast(int, pid) for row in parsed for pid in cast(list[object], row["pids"])}
    )
    by_phase: dict[str, set[int]] = {}
    for row in parsed:
        by_phase.setdefault(cast(str, row["phase"]), set()).update(cast(list[int], row["pids"]))
    expected_rss = {
        "scope": RSS_SCOPE,
        "sample_interval_seconds": 0.1,
        "minimum_terminal_samples": 2,
        "sample_count": len(parsed),
        "positive_sample_count": positive,
        "maximum_actual_gap_seconds": max(
            (right - left for left, right in pairwise(times)), default=0.0
        ),
        "observation_lifetime_seconds": lifetime,
        "unobserved_leading_seconds": times[0] if times else lifetime,
        "unobserved_trailing_seconds": lifetime - times[-1] if times else lifetime,
        "peak_sampled_rss_bytes": 0 if peak is None else peak["rss_bytes"],
        "peak_sample_time_seconds": None if peak is None else peak["elapsed_seconds"],
        "observed_pids": observed_pids,
        "pids_by_phase": {phase: sorted(pids) for phase, pids in sorted(by_phase.items())},
        "observed_phases": sorted(by_phase),
        "unobserved_phases": sorted(set(OBSERVABLE_PHASES) - set(by_phase)),
        "observer_errors": errors,
        "samples_path": "rss-samples.json",
        "samples_sha256": hashlib.sha256(data).hexdigest(),
    }
    if not _same_typed(rss, expected_rss) or len(parsed) < 2 or positive < 2 or errors:
        _refuse("RSS summary does not reconstruct with terminal coverage")
    return {
        "cpu": cpu,
        "rss": {
            "sample_count": len(parsed),
            "peak_sampled_rss_bytes": expected_rss["peak_sampled_rss_bytes"],
        },
    }


def _validate_receipt_schema(receipt: dict[str, object], run_order: int) -> None:
    if set(receipt) != TOP_LEVEL_KEYS or receipt["schema"] != RECEIPT_SCHEMA:
        _refuse("calibration receipt fields or schema changed")
    _walk_receipt(receipt)
    if (
        receipt["status"] != "complete"
        or receipt["disposition"] != "calibration-passed"
        or receipt["phase"] != "complete"
        or receipt["error"] is not None
        or receipt["evidence_scope"] != CALIBRATION_SCOPE
    ):
        _refuse("calibration receipt is not a terminal calibration-only pass")
    if not _same_typed(
        receipt["fixture"],
        {
            "id": FIXTURE_ID,
            "source_path": FIXTURE_PATH,
            "source_sha256": FIXTURE_SHA256,
            "source_bytes": FIXTURE_BYTES,
            "provenance": FIXTURE_PROVENANCE,
        },
    ):
        _refuse("calibration fixture identity changed")
    invocation = _object(
        receipt["invocation"],
        {
            "started_utc",
            "monotonic_origin",
            "host",
            "platform",
            "run_order",
            "cache_observation",
            "background_load",
            "identity",
        },
        "invocation",
    )
    if not _same_typed(invocation["run_order"], run_order) or not all(
        isinstance(invocation[key], str) and cast(str, invocation[key]).strip()
        for key in ("started_utc", "host", "platform", "cache_observation", "background_load")
    ):
        _refuse("calibration invocation metadata changed")
    origin = _number(invocation["monotonic_origin"], "invocation origin")
    if origin < 0:
        _refuse("invocation origin must be nonnegative")
    settings = _object(
        receipt["settings"],
        {
            "requested_workers",
            "effective_workers",
            "calibration_seconds",
            "external_seconds",
            "termination_grace_seconds",
            "rss_sample_interval_seconds",
            "core_side",
            "direction_steps",
            "angle_limit",
            "half_gap_tangent",
            "raw_threshold_M_over_n",
            "expected_direction_rows",
        },
        "settings",
    )
    workers = settings["requested_workers"]
    if type(workers) is not int or not 1 <= cast(int, workers) <= 4:
        _refuse("requested workers are malformed")
    effective = _object(
        settings["effective_workers"],
        {"raw", "normalized_exact", "reflected_interval", "dilation"},
        "effective workers",
    )
    execution_platform = cast(str, invocation["platform"])
    platform_workers = cast(int, workers) if execution_platform.startswith("Linux") else 1
    expected_effective = {
        "raw": workers,
        "normalized_exact": workers,
        "reflected_interval": platform_workers,
        "dilation": platform_workers,
    }
    if (
        not _same_typed(effective, expected_effective)
        or not _same_typed(settings["rss_sample_interval_seconds"], 0.1)
        or settings["core_side"] != "1/2"
        or not _same_typed(settings["direction_steps"], STEPS)
        or settings["angle_limit"] != "1/2"
        or settings["half_gap_tangent"] != "1/5760"
        or settings["raw_threshold_M_over_n"] != "1"
        or not _same_typed(settings["expected_direction_rows"], TOTAL_DIRECTION_ROWS)
        or Fraction(cast(str, settings["angle_limit"])) / cast(int, settings["direction_steps"])
        != HALF_GAP
    ):
        _refuse("settings differ from the independently derived fixture/net")
    calibration_seconds = _number(settings["calibration_seconds"], "calibration allowance")
    external_seconds = _number(settings["external_seconds"], "external allowance")
    grace = _number(settings["termination_grace_seconds"], "termination grace")
    if not 0 < calibration_seconds <= external_seconds or grace <= 0:
        _refuse("deadline settings are incoherent")
    calibration_deadline = _number(origin + calibration_seconds, "calibration deadline")
    external_deadline = _number(origin + external_seconds, "external deadline")
    source = _object(
        receipt["sources"],
        {"implementation_revision", "manifest", "runtime"},
        "sources",
    )
    if not isinstance(source["implementation_revision"], str):
        _refuse("source implementation revision is malformed")
    identity = _object(
        invocation["identity"],
        {
            "implementation_revision",
            "requested_workers",
            "calibration_seconds",
            "external_seconds",
            "termination_grace_seconds",
            "monotonic_origin",
            "calibration_deadline_monotonic",
            "external_deadline_monotonic",
            "run_order",
            "cache_observation",
            "background_load",
        },
        "invocation identity",
    )
    expected_identity = {
        "implementation_revision": source["implementation_revision"],
        "requested_workers": workers,
        "calibration_seconds": calibration_seconds,
        "external_seconds": external_seconds,
        "termination_grace_seconds": grace,
        "monotonic_origin": origin,
        "calibration_deadline_monotonic": calibration_deadline,
        "external_deadline_monotonic": external_deadline,
        "run_order": run_order,
        "cache_observation": invocation["cache_observation"],
        "background_load": invocation["background_load"],
    }
    if not _same_typed(identity, expected_identity):
        _refuse("invocation identity does not reconstruct")
    clocks = _object(
        receipt["clocks"],
        {
            "phase_duration_scope",
            "preflight_seconds",
            "launch_seconds",
            "source_loading_seconds",
            "raw_seconds",
            "normalization_publication_seconds",
            "exact_seconds",
            "interval_seconds",
            "dilation_seconds",
            "full_readback_seconds",
            "parent_final_readback_seconds",
            "terminal_admission_seconds",
            "worker_elapsed_seconds",
            "worker_exit_seconds",
            "supervisor_cleanup_seconds",
            "external_lifetime_seconds",
        },
        "clocks",
    )
    if clocks["phase_duration_scope"] != PHASE_DURATION_SCOPE:
        _refuse("phase duration scope changed")
    clock_values: dict[str, float] = {}
    for key, value in clocks.items():
        if key != "phase_duration_scope":
            measured = _number(value, f"clock {key}")
            if measured < 0:
                _refuse(f"clock {key} must be nonnegative")
            clock_values[key] = measured
    terminal_external_elapsed = _number(
        clock_values["external_lifetime_seconds"] + clock_values["terminal_admission_seconds"],
        "terminal external elapsed",
    )
    if (
        clock_values["worker_elapsed_seconds"] >= calibration_seconds
        or terminal_external_elapsed >= external_seconds
        or clock_values["worker_elapsed_seconds"] > clock_values["external_lifetime_seconds"]
    ):
        _refuse("terminal calibration exceeded or contradicted a declared deadline")
    worker_elapsed = clock_values["worker_elapsed_seconds"]
    worker_exit = clock_values["worker_exit_seconds"]
    external_lifetime = clock_values["external_lifetime_seconds"]
    if (
        not _not_later(worker_elapsed, worker_exit)
        or not _not_later(worker_exit, external_lifetime)
        or not _not_later(
            clock_values["parent_final_readback_seconds"], external_lifetime - worker_exit
        )
    ):
        _refuse("worker exit or parent readback contradicts external lifetime")
    if (
        not _not_later(
            clock_values["source_loading_seconds"], clock_values["preflight_seconds"]
        )
        or not _not_later(clock_values["launch_seconds"], worker_exit)
        or not _not_later(
            clock_values["supervisor_cleanup_seconds"], external_lifetime - worker_exit
        )
    ):
        _refuse("nested preflight or supervisor durations contradict invocation lifetime")
    disjoint_worker_phases = (
        "preflight_seconds",
        "raw_seconds",
        "normalization_publication_seconds",
        "exact_seconds",
        "interval_seconds",
        "dilation_seconds",
        "full_readback_seconds",
    )
    worker_phase_total = _number(
        sum(clock_values[key] for key in disjoint_worker_phases), "worker phase total"
    )
    if any(
        not _not_later(clock_values[key], worker_elapsed)
        for key in (*disjoint_worker_phases, "source_loading_seconds")
    ) or not _not_later(worker_phase_total, worker_elapsed):
        _refuse("worker phase durations contradict worker lifetime")
    resources = _object(
        receipt["resources"],
        {
            "cpu_scope",
            "cpu_observations",
            "coordinator_process_seconds",
            "reaped_direct_children_user_seconds",
            "reaped_direct_children_system_seconds",
            "rss",
            "worker_topology",
        },
        "resources",
    )
    rss = _object(
        resources["rss"],
        {
            "scope",
            "sample_interval_seconds",
            "minimum_terminal_samples",
            "sample_count",
            "positive_sample_count",
            "maximum_actual_gap_seconds",
            "observation_lifetime_seconds",
            "unobserved_leading_seconds",
            "unobserved_trailing_seconds",
            "peak_sampled_rss_bytes",
            "peak_sample_time_seconds",
            "observed_pids",
            "pids_by_phase",
            "observed_phases",
            "unobserved_phases",
            "observer_errors",
            "samples_path",
            "samples_sha256",
        },
        "RSS summary",
    )
    if (
        _number(rss["observation_lifetime_seconds"], "RSS observation lifetime")
        != clock_values["external_lifetime_seconds"]
    ):
        _refuse("RSS observation lifetime differs from invocation lifetime")
    supervision = _object(
        receipt["supervision"],
        {
            "status",
            "worker_exit_status",
            "process_group_reaped",
            "supervisor_signal",
            "coordinator_pid",
            "coordinator_process_group_id",
        },
        "supervision",
    )
    if (
        supervision["status"] != "observed-exit"
        or not _same_typed(supervision["worker_exit_status"], 0)
        or supervision["process_group_reaped"] is not True
        or supervision["supervisor_signal"] is not None
        or type(supervision["coordinator_pid"]) is not int
        or cast(int, supervision["coordinator_pid"]) <= 0
        or type(supervision["coordinator_process_group_id"]) is not int
        or supervision["coordinator_process_group_id"] != supervision["coordinator_pid"]
    ):
        _refuse("parent supervision is not a successful reaped execution")


def _validate_artifacts(output: Path, receipt: dict[str, object]) -> list[dict[str, object]]:
    expected_names = {relative for _role, relative, _count, _directory in ARTIFACTS}
    actual_names = {path.name for path in output.iterdir()}
    if actual_names != expected_names:
        _refuse("retained artifact set has missing or extra entries")
    rows: list[dict[str, object]] = []
    for role, relative, expected_count, directory in ARTIFACTS:
        path = output / relative
        if (
            path.is_symlink()
            or (directory and not path.is_dir())
            or (not directory and not path.is_file())
        ):
            _refuse(f"artifact has the wrong type: {relative}")
        files = tuple(path.iterdir()) if directory else (path,)
        if len(files) != expected_count or any(
            item.is_symlink() or not item.is_file() for item in files
        ):
            _refuse(f"artifact row count changed: {relative}")
        rows.append(
            {
                "role": role,
                "path": relative,
                "count": len(files),
                "bytes": sum(item.stat().st_size for item in files),
            }
        )
    if not _same_typed(receipt["artifacts"], rows):
        _refuse("receipt artifact inventory does not reconstruct from retained bytes")
    return rows


def read_profile(
    *,
    repository: Path,
    execution_revision: str,
    reader_revision: str,
    output_dir: Path,
    run_order: int,
) -> dict[str, object]:
    """Return one strict JSON-compatible proof or raise ``ReadbackRefusalError``."""
    repository = repository.resolve()
    if output_dir.is_symlink():
        _refuse("profile output must not be a symlink")
    output = output_dir.resolve()
    if output.is_relative_to(repository) or not stat.S_ISDIR(_mode(output, "profile output")):
        _refuse("profile output must be a real directory outside the repository")
    if type(run_order) is not int or run_order < 1:
        _refuse("run order must be a positive integer")
    _preflight_artifacts(output)
    _bind_revisions(repository, execution_revision, reader_revision)
    receipt_bytes, receipt = _json(output / "result.json", "calibration receipt")
    _validate_receipt_schema(receipt, run_order)
    _validate_sources(repository, receipt["sources"], execution_revision)
    _validate_candidate(output, receipt)
    row_proof = _read_rows(output, receipt)
    _validate_dilation(output)
    resource_proof = _validate_resources(output, receipt)
    topology_proof = _validate_topology(output, receipt)
    artifacts = _validate_artifacts(output, receipt)
    invocation = cast(dict[str, object], receipt["invocation"])
    return {
        "schema": READER_SCHEMA,
        "status": "accepted",
        "evidence_scope": (
            "source-distinct admission of one target-free n=2 calibration profile"
        ),
        "execution_revision": execution_revision,
        "reader_revision": reader_revision,
        "run_order": run_order,
        "profile_directory": str(output),
        "invocation_identity": invocation["identity"],
        "receipt": {
            "path": "result.json",
            "bytes": len(receipt_bytes),
            "sha256": hashlib.sha256(receipt_bytes).hexdigest(),
        },
        "fixture": {
            "n": N,
            "outer_side": "3/4",
            "core_side": "1/2",
            "direction_steps": STEPS,
            "half_gap_tangent": "1/5760",
            "raw_budget": "2",
            "raw_minimum": "2",
            "normalization": "1/2",
            "normalized_budget": "1",
            "normalized_minimum": "1",
        },
        "route_digests": {
            key: row_proof[key]
            for key in ("raw", "normalized_exact", "reflected_interval", "dilation")
        },
        "interval_boxes_observed": row_proof["boxes_observed"],
        "resources": resource_proof,
        "worker_topology": topology_proof,
        "artifacts": artifacts,
        "limitations": (
            "admits only this retained n=2 calibration execution; it makes no "
            "scientific-target or runtime-extrapolation claim"
        ),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--expect-execution-revision", required=True)
    parser.add_argument("--expect-reader-revision", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--run-order", required=True, type=int)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        proof = read_profile(
            repository=args.repository,
            execution_revision=args.expect_execution_revision,
            reader_revision=args.expect_reader_revision,
            output_dir=args.output_dir,
            run_order=args.run_order,
        )
    except (OSError, ReadbackRefusalError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(proof, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
