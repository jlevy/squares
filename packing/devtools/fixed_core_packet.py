#!/usr/bin/env python3
"""Run one source-bound fixed-core threshold packet under an external deadline.

This module is an instrument. Its geometry is fixed to the BC329 preflight packet; its
tests and source checks do not execute that scientific target. The raw sweep keeps the
T-025 weights on their original scale. Only a complete minimum strictly above ``M/11``
may create normalized bytes, and every retaining reader consumes those same bytes.
"""

# The retained certificate gate deliberately exposes no structured result API. This
# runner uses its independently implemented dense/slab direction helper and the limit
# record builder, then adds byte and progress binding around them.
# pyright: reportPrivateUsage=false

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.metadata
import importlib.util
import json
import math
import os
import platform
import signal
import subprocess
import sys
import sysconfig
import time
import tomllib
from collections.abc import Callable, Collection, Iterator, Sequence
from concurrent.futures import FIRST_COMPLETED, Future, ProcessPoolExecutor, wait
from contextlib import suppress
from dataclasses import dataclass
from fractions import Fraction
from multiprocessing import get_context
from pathlib import Path, PurePosixPath
from typing import Any, Literal, Protocol, cast

from strif import atomic_write_text

from devtools.decide_threshold_certificate import (
    _dense_and_slab,
    _placement_membership,
    load,
)
from devtools.dilation_corollary import (
    THRESHOLD_LIMIT_RECORD_SCHEMA,
    _decimal,
    build_limit_record,
    sharp_dilation_ceiling,
)
from devtools.measure_net_refinement import half_gap_tangent, uniform_net
from devtools.measure_threshold_net_refinement import at, rescaled_record
from sqpack.fractional.interval import DirectionOutcome, IntervalInputError
from sqpack.fractional.threshold import (
    Point,
    ThresholdCertificate,
    ThresholdSweepDeadlineError,
    closed_form_threshold_conditions,
    exact_charge,
    minimum_charge,
)
from sqpack.fractional.threshold_interval import (
    scaled_threshold_masses,
    verify_threshold_by_intervals,
)

PACKING = Path(__file__).resolve().parents[1]
RUNNING_REPOSITORY = PACKING.parent.resolve()
RUNNING_ENTRY_POINT = Path(__file__).resolve()

SOURCE_PATH = "packing/cases/n11_threshold_certificate/certificate.json"
T026_PATH = "packing/cases/n11_threshold_certificate/t-026-dilation-limit-corollary.json"
SOURCE_BLOB = "684a6b7adf4524691a4fb996fa3625d909d171ac"
SOURCE_SHA256 = "3935651af614eb3e9a1926179925f98643beb17ed1764a323fe83a527f4bad5c"
SOURCE_BYTES = 673639
T026_BLOB = "baeb8c4329cebf783ebe3546a9400710664ef317"
T026_SHA256 = "04fd6bbca1941671ddbabbe359219011b8217818b0a291f4c9a00f5fa7834f8e"
T026_BOUNDED_SIDE_SQUARED = Fraction(
    472793799119770550224225000000,
    32290909254655439869209770001,
)
PROJECT_RUNTIME_PATHS = (
    "packing/.python-version",
    "packing/pyproject.toml",
    "packing/uv.lock",
)
RUNTIME_DISTRIBUTIONS = ("numpy", "strif")
PACKET_CORE_SIDE = Fraction(9981, 10000)
PACKET_STEPS = 2880
PACKET_ANGLE_LIMIT = Fraction(207107, 500000)
PACKET_HALF_GAP = Fraction(207107, 1440000000)
SOURCE_BUDGET = Fraction(685457679, 62500000)
RAW_THRESHOLD = SOURCE_BUDGET / 11
RAW_DIRECTIONS = PACKET_STEPS + 1
INTERVAL_DIRECTIONS = 2 * PACKET_STEPS + 1
DEFAULT_GRACE_SECONDS = 2.0
MAX_WORKERS = 4
IN_FLIGHT_WORK_PER_WORKER = 2
STRIF_ATOMIC_UID_LENGTH = 13
RESULT_SCHEMA = "fixed-core-threshold-packet/v4"
PREFLIGHT_SCHEMA = "fixed-core-threshold-packet-preflight/v2"
NORMALIZATION_SETTING = "alpha=1/m after complete strict acceptance"
SCIENTIFIC_DEADLINE_SCOPE = (
    "parent invocation through supervised source and runtime preflight, source replay, "
    "all retaining readers, publication, and independent readback; expiration revokes "
    "acceptance"
)
EXTERNAL_DEADLINE_SCOPE = (
    "clocked from parent invocation through supervised worker process-group "
    "termination; enforcement excludes time blocked inside the operating-system "
    "process-launch call, checks the deadline immediately before and after that call, "
    "and allows termination grace after the deadline"
)
RUNTIME_ATTESTATION_SCOPE = (
    "source and observed runtime identities for this execution; no interpreter-binary, "
    "installed-wheel, operating-system, CPU, scheduling, or cross-host byte-equivalence "
    "claim"
)
CLAIM_LIMIT = (
    "the fixed BC329 packet with the T-025 sites, thresholds and relative weights, "
    "B=9981/10000 and the 2880-step half-tangent net; no other core, net, weights, "
    "atoms, conditional domain or global optimization conclusion"
)

Clock = Callable[[], float]
Publisher = Callable[[Path, dict[str, object]], None]


class PacketError(ValueError):
    """A source, invocation, result, or reader violated the fixed packet contract."""


class PacketOperationalError(RuntimeError):
    """The host failed while collecting or supervising fixed packet evidence."""


class _SupervisorSignal(BaseException):
    """Transfer POSIX termination to the synchronous process-group cleanup path."""

    def __init__(self, signum: int) -> None:
        self.signum = signum
        super().__init__(signum)


class PacketDeadlineError(PacketError):
    """A packet deadline expired before the next accepted checkpoint."""


@dataclass(frozen=True, slots=True)
class PackageRuntimeObservation:
    """One imported distribution as observed before the packet starts."""

    name: str
    metadata_version: str
    module_version: str
    module_origin: Path


@dataclass(frozen=True, slots=True)
class RuntimeObservation:
    """Read-only interpreter and distribution facts used to build a runtime binding."""

    implementation: str
    version: str
    abi: str
    gil_enabled: bool
    environment: Path
    executable: Path
    resolved_executable: Path
    build: str
    packages: tuple[PackageRuntimeObservation, ...]


RuntimeObserver = Callable[[], RuntimeObservation]


class ExactReaderDisagreementError(PacketError):
    """The dense and slab readers disagreed on one retained exact direction."""

    def __init__(
        self,
        *,
        completed: int,
        completed_directions: tuple[int, ...],
        minimum: Fraction,
        argmin: int,
        witness: Point,
        direction: int,
        dense: tuple[Fraction, Point],
        slab: tuple[Fraction, Point],
    ) -> None:
        super().__init__(f"normalized exact readers disagreed at direction {direction}")
        self.completed = completed
        self.completed_directions = completed_directions
        self.minimum = minimum
        self.argmin = argmin
        self.witness = witness
        self.direction = direction
        self.dense = dense
        self.slab = slab


@dataclass(frozen=True, slots=True)
class RawMinimum:
    minimum: Fraction
    direction: int
    witness: Point
    completed: int


@dataclass(frozen=True, slots=True)
class ExactRoute:
    minimum: Fraction
    direction: int
    witness: Point
    completed: int
    disagreements: int


@dataclass(frozen=True, slots=True)
class IntervalRoute:
    lower: Fraction
    upper: Fraction
    completed: int
    stalled: int
    budget_exhausted: int
    accepted: bool


@dataclass(frozen=True, slots=True)
class IntervalReadback:
    enclosure: tuple[Fraction, Fraction] | None
    completed: int
    stalled: int
    budget_exhausted: int
    accepted: bool


class RawRunner(Protocol):
    def __call__(
        self,
        certificate: ThresholdCertificate,
        *,
        workers: int,
        deadline: float,
        clock: Clock,
        progress: Callable[[int, tuple[int, ...], Fraction, int, Point], None],
        log: Path,
    ) -> RawMinimum: ...


class ExactRunner(Protocol):
    def __call__(
        self,
        certificate: ThresholdCertificate,
        *,
        workers: int,
        deadline: float,
        clock: Clock,
        progress: Callable[[int, tuple[int, ...], Fraction, int, Point], None],
        log: Path,
    ) -> ExactRoute: ...


class IntervalRunner(Protocol):
    def __call__(
        self,
        certificate: ThresholdCertificate,
        *,
        workers: int,
        deadline: float,
        clock: Clock,
        progress: Callable[[DirectionOutcome], None],
        log: Path,
    ) -> IntervalRoute: ...


class DilationRunner(Protocol):
    def __call__(
        self,
        path: Path,
        *,
        workers: int,
        deadline: float,
        clock: Clock,
        progress: Callable[[int, Fraction, str], None],
    ) -> dict[str, object]: ...


RawWitnessReplay = Callable[[ThresholdCertificate, RawMinimum], tuple[Fraction, bool]]


def _git(repository: Path, *arguments: str, deadline: float | None = None) -> str:
    remaining = None if deadline is None else deadline - time.perf_counter()
    if remaining is not None and remaining <= 0:
        raise PacketDeadlineError("Git deadline reached before output-guard command")
    try:
        result = subprocess.run(
            ("git", *arguments),
            cwd=repository,
            check=False,
            capture_output=True,
            text=True,
            timeout=remaining,
        )
    except subprocess.TimeoutExpired as error:
        raise PacketDeadlineError("Git deadline reached during output-guard command") from error
    if deadline is not None and time.perf_counter() >= deadline:
        raise PacketDeadlineError("Git deadline reached during output-guard command")
    if result.returncode:
        detail = result.stderr.strip() or "no diagnostic"
        raise PacketOperationalError(
            f"git {' '.join(arguments)} failed with status {result.returncode}: {detail}"
        )
    return result.stdout.strip()


def _local_module_path(repository: Path, module: str) -> Path | None:
    parts = module.split(".")
    roots = {
        "cases": repository / "packing" / "cases",
        "devtools": repository / "packing" / "devtools",
        "sqpack": repository / "packing" / "src" / "sqpack",
    }
    root = roots.get(parts[0])
    if root is None:
        return None
    candidate = root.joinpath(*parts[1:])
    module_path = candidate.with_suffix(".py")
    if module_path.is_file():
        return module_path
    package_path = candidate / "__init__.py"
    return package_path if package_path.is_file() else None


def _imported_local_modules(module: str, path: Path) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except OSError as error:
        raise PacketOperationalError(
            f"could not read dependency {path}: {type(error).__name__}: {error}"
        ) from error
    except SyntaxError as error:
        raise PacketError(f"could not inspect dependency {path}: {error}") from error
    package = module if path.name == "__init__.py" else module.rpartition(".")[0]
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                relative = f"{'.' * node.level}{base}"
                try:
                    base = importlib.util.resolve_name(relative, package)
                except ImportError as error:
                    raise PacketError(
                        f"could not resolve relative import {relative!r} in {path}"
                    ) from error
            if base:
                imported.add(base)
                imported.update(f"{base}.{alias.name}" for alias in node.names)
    return imported


def discover_implementation_paths(repository: Path) -> tuple[str, ...]:
    """Return every repository input that fixes the packet's source and runtime."""

    pending = ["devtools.fixed_core_packet"]
    visited: set[str] = set()
    paths = {SOURCE_PATH, T026_PATH, *PROJECT_RUNTIME_PATHS}
    while pending:
        module = pending.pop()
        if module in visited:
            continue
        path = _local_module_path(repository.resolve(), module)
        if path is None:
            continue
        visited.add(module)
        paths.add(path.relative_to(repository.resolve()).as_posix())
        parts = module.split(".")
        for length in range(1, len(parts)):
            package = ".".join(parts[:length])
            if package not in visited and _local_module_path(repository, package) is not None:
                pending.append(package)
        pending.extend(
            imported
            for imported in _imported_local_modules(module, path)
            if imported not in visited and _local_module_path(repository, imported) is not None
        )
    return tuple(sorted(paths))


def _validate_loaded_modules(repository: Path, paths: Sequence[str]) -> None:
    expected_entry = repository / "packing" / "devtools" / RUNNING_ENTRY_POINT.name
    if repository.resolve() != RUNNING_REPOSITORY or expected_entry != RUNNING_ENTRY_POINT:
        raise PacketError("repository must contain the running fixed-core instrument")
    for relative in paths:
        path = Path(relative)
        if path.suffix != ".py":
            continue
        parts = path.with_suffix("").parts
        if parts[-1] == "__init__":
            parts = parts[:-1]
        if parts[:3] == ("packing", "src", "sqpack"):
            module = ".".join(parts[2:])
        elif parts[:2] in (("packing", "devtools"), ("packing", "cases")):
            module = ".".join(parts[1:])
        else:
            continue
        loaded = sys.modules.get(module)
        if module == "devtools.fixed_core_packet" and loaded is None:
            loaded = sys.modules.get("__main__")
        if loaded is None:
            continue
        origin = getattr(loaded, "__file__", None)
        if type(origin) is not str or Path(origin).resolve() != (repository / relative):
            raise PacketError(f"loaded project module {module} comes from another checkout")


def source_manifest(
    repository: Path,
    revision: str,
    *,
    result_directory: Path | None = None,
) -> list[dict[str, str]]:
    """Bind the exact source and recursive implementation closure to one clean revision."""

    if len(revision) != 40 or any(c not in "0123456789abcdef" for c in revision):
        raise PacketError("expected revision must be 40 lowercase hexadecimal digits")
    repository = repository.resolve()
    paths = discover_implementation_paths(repository)
    _validate_loaded_modules(repository, paths)
    if _git(repository, "rev-parse", "HEAD") != revision:
        raise PacketError("current Git revision differs from the frozen instrument")
    revision_paths = set(
        _git(repository, "ls-tree", "-r", "--name-only", revision).splitlines()
    )
    changed = _git(repository, "status", "--porcelain", "--", *paths)
    if changed:
        raise PacketError("fixed source or implementation closure is not clean")
    status_arguments = ["status", "--porcelain", "--untracked-files=all"]
    if result_directory is not None:
        resolved_result = result_directory.resolve()
        if resolved_result.is_relative_to(repository):
            relative_result = resolved_result.relative_to(repository).as_posix()
            result_path = PurePosixPath(relative_result)
            if any(
                PurePosixPath(tracked_path).is_relative_to(result_path)
                or result_path.is_relative_to(PurePosixPath(tracked_path))
                for tracked_path in revision_paths
            ):
                raise PacketError(
                    "result directory overlaps a path tracked at the frozen revision"
                )
            status_arguments.extend(
                (
                    "--",
                    ".",
                    f":(exclude,top,literal){relative_result}",
                )
            )
    if _git(repository, *status_arguments):
        raise PacketError("instrument checkout must be clean before the run")
    tracked = set(
        _git(repository, "ls-tree", "-r", "--name-only", revision, "--", *paths).splitlines()
    )
    if tracked != set(paths):
        missing = ", ".join(sorted(set(paths) - tracked))
        raise PacketError(f"frozen source or implementation closure is incomplete: {missing}")
    manifest: list[dict[str, str]] = []
    for relative in paths:
        blob = _git(repository, "rev-parse", f"{revision}:{relative}")
        frozen = subprocess.run(
            ("git", "cat-file", "blob", blob),
            cwd=repository,
            check=False,
            capture_output=True,
        )
        if frozen.returncode:
            detail = frozen.stderr.decode("utf-8", errors="replace").strip()
            raise PacketOperationalError(
                f"could not read frozen Git blob for {relative}: {detail}"
            )
        data = (repository / relative).read_bytes()
        # Git status can omit tracked edits marked assume-unchanged or skip-worktree.
        # Bind the exported digest to the actual revision bytes, independent of flags.
        if data != frozen.stdout:
            raise PacketError(f"{relative} bytes differ from the frozen Git blob")
        manifest.append(
            {"path": relative, "git_blob": blob, "sha256": hashlib.sha256(data).hexdigest()}
        )
    identities = {row["path"]: (row["git_blob"], row["sha256"]) for row in manifest}
    if identities[SOURCE_PATH] != (SOURCE_BLOB, SOURCE_SHA256):
        raise PacketError("T-025 source identity differs from the admitted artifact")
    if identities[T026_PATH] != (T026_BLOB, T026_SHA256):
        raise PacketError("T-026 comparison identity differs from the admitted artifact")
    if (repository / SOURCE_PATH).stat().st_size != SOURCE_BYTES:
        raise PacketError("T-025 source byte count differs from the admitted artifact")
    return manifest


def _observe_runtime() -> RuntimeObservation:
    """Read the running interpreter and the two imported third-party distributions."""

    abi = sysconfig.get_config_var("SOABI")
    gil_probe = getattr(sys, "_is_gil_enabled", None)
    if not isinstance(abi, str) or not abi or not callable(gil_probe):
        raise PacketError("running Python does not expose the required ABI and GIL identity")
    packages: list[PackageRuntimeObservation] = []
    for name in RUNTIME_DISTRIBUTIONS:
        module = importlib.import_module(name)
        module_version = getattr(module, "__version__", None)
        module_origin = getattr(module, "__file__", None)
        if not isinstance(module_version, str) or not isinstance(module_origin, str):
            raise PacketError(f"runtime package {name} lacks a version or module origin")
        packages.append(
            PackageRuntimeObservation(
                name=name,
                metadata_version=importlib.metadata.version(name),
                module_version=module_version,
                module_origin=Path(module_origin).resolve(),
            )
        )
    executable = Path(sys.executable).absolute()
    return RuntimeObservation(
        implementation=sys.implementation.name,
        version=platform.python_version(),
        abi=abi,
        gil_enabled=cast(Callable[[], bool], gil_probe)(),
        environment=Path(sys.prefix).resolve(),
        executable=executable,
        resolved_executable=executable.resolve(),
        build=sys.version,
        packages=tuple(packages),
    )


def runtime_binding(
    repository: Path, *, observer: RuntimeObserver | None = None
) -> dict[str, object]:
    """Validate the project environment and return its closed, read-only identity.

    ``observer`` is the narrow test seam. Production callers omit it and must be
    running in this repository's own ``packing/.venv``.
    """

    repository = repository.resolve()
    observation = (observer or _observe_runtime)()
    expected_environment = (repository / "packing" / ".venv").resolve()
    if observation.environment.resolve() != expected_environment:
        raise PacketError("fixed-core packet must run in the repository packing/.venv")
    try:
        expected_version = (repository / PROJECT_RUNTIME_PATHS[0]).read_text().strip()
    except OSError as error:
        raise PacketOperationalError(
            f"could not read the bound Python version: {type(error).__name__}: {error}"
        ) from error
    if (
        observation.implementation != "cpython"
        or observation.version != expected_version
        or not observation.abi
        or type(observation.gil_enabled) is not bool
        or not observation.build
    ):
        raise PacketError("Python runtime differs from the project interpreter identity")
    if (
        not observation.executable.is_absolute()
        or not observation.executable.is_file()
        or observation.resolved_executable != observation.executable.resolve()
        or not observation.resolved_executable.is_file()
    ):
        raise PacketError("Python executable identity is missing or inconsistent")

    try:
        lock_text = (repository / "packing" / "uv.lock").read_text()
    except OSError as error:
        raise PacketOperationalError(
            f"could not read the bound uv.lock: {type(error).__name__}: {error}"
        ) from error
    try:
        lock = tomllib.loads(lock_text)
    except tomllib.TOMLDecodeError as error:
        raise PacketError(f"could not read the bound uv.lock: {error}") from error
    package_rows = lock.get("package")
    if not isinstance(package_rows, list):
        raise PacketError("uv.lock has no package rows")
    locked: dict[str, str] = {}
    for raw_row in cast(list[object], package_rows):
        if not isinstance(raw_row, dict):
            raise PacketError("uv.lock package row is malformed")
        row = cast(dict[str, object], raw_row)
        name = row.get("name")
        if name not in RUNTIME_DISTRIBUTIONS:
            continue
        version = row.get("version")
        if not isinstance(version, str) or name in locked:
            raise PacketError(f"uv.lock runtime package {name!r} is missing or duplicated")
        locked[cast(str, name)] = version

    observed = {package.name: package for package in observation.packages}
    if set(observed) != set(RUNTIME_DISTRIBUTIONS) or set(locked) != set(RUNTIME_DISTRIBUTIONS):
        raise PacketError("runtime package set differs from the fixed import closure")
    versions: dict[str, str] = {}
    for name in RUNTIME_DISTRIBUTIONS:
        package = observed[name]
        if (
            package.metadata_version != locked[name]
            or package.module_version != locked[name]
            or not package.module_origin.is_relative_to(expected_environment)
        ):
            raise PacketError(f"runtime package {name} differs from the bound uv.lock")
        versions[name] = locked[name]

    return {
        "python": {
            "implementation": observation.implementation,
            "version": observation.version,
            "abi": observation.abi,
            "gil_enabled": observation.gil_enabled,
            "environment": str(observation.environment),
            "executable": str(observation.executable),
            "resolved_executable": str(observation.resolved_executable),
            "build": observation.build,
        },
        "packages": versions,
        "attestation_scope": RUNTIME_ATTESTATION_SCOPE,
    }


def load_packet_source(raw: bytes) -> tuple[ThresholdCertificate, dict[str, object]]:
    """Load T-025 and refuse any source that changes the fixed packet's scale."""

    certificate, record = load(raw)
    expected = {
        "id": "C-n011-threshold-191-50",
        "variant": "threshold",
        "n": 11,
        "outer_side": "191/50",
        "square_side": "9977/10000",
        "angle_limit": str(PACKET_ANGLE_LIMIT),
        "direction_steps": 180,
        "total_budget": str(SOURCE_BUDGET),
    }
    for key, value in expected.items():
        if record.get(key) != value:
            raise PacketError(f"T-025 source field {key!r} differs from {value!r}")
    if certificate.total_budget != SOURCE_BUDGET:
        raise PacketError("T-025 recomputed budget differs from the fixed source scale")
    packet = at(
        certificate,
        uniform_net(PACKET_ANGLE_LIMIT, PACKET_STEPS),
        PACKET_CORE_SIDE,
    )
    if len(packet.directions) != RAW_DIRECTIONS:
        raise PacketError("fixed packet does not have 2881 exact directions")
    if half_gap_tangent(packet.half_tangents) != PACKET_HALF_GAP:
        raise PacketError("fixed packet half-gap differs from the preflight value")
    return packet, record


def load_t026_reference(raw: bytes) -> dict[str, object]:
    """Read the published T-026 comparison and bind its claim semantics directly."""

    record = _strict_json_bytes(raw, T026_PATH)
    conclusion = record.get("conclusion")
    if (
        record.get("schema") != THRESHOLD_LIMIT_RECORD_SCHEMA
        or not isinstance(conclusion, dict)
        or conclusion.get("bounded_side_squared") != str(T026_BOUNDED_SIDE_SQUARED)
        or conclusion.get("relation") != ">="
        or conclusion.get("endpoint_certificate") is not False
    ):
        raise PacketError("T-026 comparison differs from the published lower-bound claim")
    return record


def normalized_record(
    source_record: dict[str, object],
    raw_minimum: Fraction,
    *,
    source_revision: str,
) -> dict[str, object]:
    """Create the sole normalized record after the strict raw threshold is crossed."""

    if raw_minimum <= RAW_THRESHOLD:
        raise PacketError("normalization requires the complete raw minimum to exceed M/11")
    if len(source_revision) != 40 or any(
        character not in "0123456789abcdef" for character in source_revision
    ):
        raise PacketError("normalization requires a frozen implementation revision")
    result = rescaled_record(
        cast(dict[str, Any], source_record),
        PACKET_STEPS,
        PACKET_CORE_SIDE,
        1 / raw_minimum,
    )
    result["id"] = "C-n011-threshold-191-50-bc329-B9981-10000-net2880"
    result["least_cell_charge"] = "1"
    provenance = cast(dict[str, object], result.get("provenance"))
    provenance.update(
        {
            "derived_from": SOURCE_PATH,
            "packet": "BC329",
            "core_side": str(PACKET_CORE_SIDE),
            "direction_steps": PACKET_STEPS,
            "normalization": f"every weight multiplied by {1 / raw_minimum}",
            "bc329": {
                "source_path": SOURCE_PATH,
                "source_revision": source_revision,
                "source_git_blob": SOURCE_BLOB,
                "source_sha256": SOURCE_SHA256,
                "raw_minimum": str(raw_minimum),
                "weight_scale": str(1 / raw_minimum),
                "weight_transformation": (
                    "multiply every point-atom and threshold-atom weight by weight_scale"
                ),
                "relative_weight_ratios_preserved": True,
                "core_side": str(PACKET_CORE_SIDE),
                "direction_steps": PACKET_STEPS,
            },
        }
    )
    return cast(dict[str, object], result)


def normalized_bytes(
    source_record: dict[str, object], raw_minimum: Fraction, *, source_revision: str
) -> bytes:
    return (
        json.dumps(
            normalized_record(
                source_record,
                raw_minimum,
                source_revision=source_revision,
            ),
            indent=1,
            allow_nan=False,
        )
        + "\n"
    ).encode()


def raw_decision(minimum: Fraction) -> Literal["accepted", "rejected"]:
    """Equality is a rejection of this fixed relative-weight packet."""

    return "accepted" if minimum > RAW_THRESHOLD else "rejected"


def replay_raw_witness(
    certificate: ThresholdCertificate, result: RawMinimum
) -> tuple[Fraction, bool]:
    """Re-evaluate the raw argmin by exact membership and physical admissibility."""

    if not 0 <= result.direction < len(certificate.directions):
        raise PacketError("raw argmin direction is outside the fixed net")
    direction = certificate.directions[result.direction]
    u, v = result.witness
    x = direction.ux * u + direction.vx * v
    y = direction.uy * u + direction.vy * v
    x_extent = certificate.square_side * (abs(direction.ux) + abs(direction.vx)) / 2
    y_extent = certificate.square_side * (abs(direction.uy) + abs(direction.vy)) / 2
    admissible = (
        x_extent <= x <= certificate.outer_side - x_extent
        and y_extent <= y <= certificate.outer_side - y_extent
    )
    charge = exact_charge(
        certificate.atoms,
        certificate.threshold_atoms,
        _placement_membership(certificate, result.direction, result.witness),
    )
    return charge, admissible


def _expired(deadline: float, clock: Clock, phase: str) -> None:
    if clock() >= deadline:
        raise PacketDeadlineError(f"scientific deadline reached {phase}")


@dataclass(slots=True)
class SharedPacket:
    certificate: ThresholdCertificate | None = None


SHARED_PACKET = SharedPacket()


def _raw_direction(index: int) -> tuple[int, Fraction, Point]:
    certificate = SHARED_PACKET.certificate
    if certificate is None:
        raise PacketError("fixed packet was not installed before the raw sweep")
    minimum, witness = minimum_charge(
        certificate.atoms,
        certificate.threshold_atoms,
        certificate.directions[index],
        certificate.outer_side,
        certificate.square_side,
    )
    return index, minimum, witness


def _exact_direction(
    index: int,
) -> tuple[int, tuple[Fraction, Point], tuple[Fraction, Point]]:
    certificate = SHARED_PACKET.certificate
    if certificate is None:
        raise PacketError("fixed packet was not installed before the exact route")
    dense, slab = _dense_and_slab(certificate, index)
    return index, dense, slab


def _write_direction(directory: Path, index: int | str, row: dict[str, object]) -> None:
    """Atomically retain one completed direction independently of later work."""

    directory.mkdir(parents=True, exist_ok=True)
    atomic_write_text(
        directory / f"{index}.json", json.dumps(row, indent=1, allow_nan=False) + "\n"
    )


def _direction_digest(paths: Sequence[Path]) -> str:
    """Hash one canonically ordered retained direction set, including its filenames."""

    digest = hashlib.sha256()
    for path in paths:
        data = path.read_bytes()
        name = path.name.encode()
        digest.update(len(name).to_bytes(4, "big"))
        digest.update(name)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def _bounded_completion_batches[DirectionResult](
    pool: ProcessPoolExecutor,
    worker: Callable[[int], DirectionResult],
    *,
    total: int,
    limit: int,
    deadline: float,
    clock: Clock,
    phase: str,
) -> Iterator[tuple[tuple[int, Future[DirectionResult]], ...]]:
    """Yield bounded batches of completed futures, ordered by their net index."""

    pending: dict[Future[DirectionResult], int] = {}
    next_index = 0

    def fill() -> None:
        nonlocal next_index
        while next_index < total and len(pending) < limit:
            pending[pool.submit(worker, next_index)] = next_index
            next_index += 1

    fill()
    while pending:
        landed = {future for future in pending if future.done()}
        if not landed:
            remaining = max(0.0, deadline - clock())
            done, _not_done = wait(
                tuple(pending), timeout=remaining, return_when=FIRST_COMPLETED
            )
            landed = set(done)
        if not landed:
            _expired(deadline, clock, phase)
            continue
        while more := {future for future in pending if future not in landed and future.done()}:
            landed.update(more)
        batch = tuple(
            sorted(
                ((pending.pop(future), future) for future in landed),
                key=lambda item: item[0],
            )
        )
        yield batch
        fill()


def run_raw_sweep(
    certificate: ThresholdCertificate,
    *,
    workers: int,
    deadline: float,
    clock: Clock,
    progress: Callable[[int, tuple[int, ...], Fraction, int, Point], None],
    log: Path,
) -> RawMinimum:
    """Sweep all raw directions, publishing only an observed upper bound until complete."""

    worst: Fraction | None = None
    worst_index = -1
    worst_witness: Point | None = None
    completed = 0
    completed_directions: set[int] = set()
    SHARED_PACKET.certificate = certificate
    total = len(certificate.directions)
    pool: ProcessPoolExecutor | None = None
    succeeded = False

    def retain(result: tuple[int, Fraction, Point]) -> None:
        nonlocal completed, worst, worst_index, worst_witness
        index, minimum, witness = result
        _write_direction(
            log,
            index,
            {
                "direction": index,
                "charge": str(minimum),
                "witness": [str(witness[0]), str(witness[1])],
            },
        )
        completed += 1
        completed_directions.add(index)
        if worst is None or minimum < worst or (minimum == worst and index < worst_index):
            worst, worst_index, worst_witness = minimum, index, witness

    try:
        if workers > 1 and total > 1:
            effective_workers = min(workers, total)
            pool = ProcessPoolExecutor(
                max_workers=effective_workers, mp_context=get_context("fork")
            )
            batches = _bounded_completion_batches(
                pool,
                _raw_direction,
                total=total,
                limit=IN_FLIGHT_WORK_PER_WORKER * effective_workers,
                deadline=deadline,
                clock=clock,
                phase="during raw sweep",
            )
            for batch in batches:
                completed_before = completed
                landed: list[tuple[int, Fraction, Point]] = []
                failure: Exception | None = None
                for _index, future in batch:
                    try:
                        landed.append(future.result())
                    except Exception as error:  # noqa: BLE001 -- retain peer completions first
                        if failure is None:
                            failure = error
                for result in landed:
                    try:
                        retain(result)
                    except Exception as error:  # noqa: BLE001 -- retain every landed peer
                        if failure is None:
                            failure = error
                if completed > completed_before:
                    progress(
                        completed,
                        tuple(sorted(completed_directions)),
                        cast(Fraction, worst),
                        worst_index,
                        cast(Point, worst_witness),
                    )
                if failure is not None:
                    raise failure
            _expired(deadline, clock, "during raw sweep")
        else:
            for index in range(total):
                retain(_raw_direction(index))
                if completed % 16 == 0 or completed == total:
                    progress(
                        completed,
                        tuple(sorted(completed_directions)),
                        cast(Fraction, worst),
                        worst_index,
                        cast(Point, worst_witness),
                    )
                _expired(deadline, clock, "during raw sweep")
        if worst is None or worst_witness is None or completed != total:
            raise PacketError("raw sweep did not complete every fixed direction")
        succeeded = True
        return RawMinimum(worst, worst_index, worst_witness, completed)
    finally:
        if pool is not None:
            if succeeded:
                pool.shutdown()
            else:
                with suppress(Exception):
                    pool.terminate_workers()


def run_exact_route(
    certificate: ThresholdCertificate,
    *,
    workers: int,
    deadline: float,
    clock: Clock,
    progress: Callable[[int, tuple[int, ...], Fraction, int, Point], None],
    log: Path,
) -> ExactRoute:
    """Run dense and slab exact coverage on every normalized net direction."""

    SHARED_PACKET.certificate = certificate
    total = len(certificate.directions)
    pool: ProcessPoolExecutor | None = None
    worst: Fraction | None = None
    worst_index = -1
    worst_witness: Point | None = None
    completed = 0
    completed_directions: set[int] = set()
    disagreements = 0
    succeeded = False

    def retain(
        result: tuple[int, tuple[Fraction, Point], tuple[Fraction, Point]],
    ) -> tuple[int, tuple[Fraction, Point], tuple[Fraction, Point]] | None:
        nonlocal completed, disagreements, worst, worst_index, worst_witness
        index, dense, slab = result
        dense_minimum, witness = dense
        _write_direction(
            log,
            index,
            {
                "direction": index,
                "dense": str(dense_minimum),
                "slab": str(slab[0]),
                "agree": dense == slab,
                "witness": [str(witness[0]), str(witness[1])],
                "slab_witness": [str(slab[1][0]), str(slab[1][1])],
            },
        )
        completed += 1
        completed_directions.add(index)
        if dense != slab:
            disagreements += 1
        if (
            worst is None
            or dense_minimum < worst
            or (dense_minimum == worst and index < worst_index)
        ):
            worst, worst_index, worst_witness = dense_minimum, index, witness
        return result if dense != slab else None

    def raise_disagreement(
        disagreement: tuple[int, tuple[Fraction, Point], tuple[Fraction, Point]],
    ) -> None:
        index, dense, slab = disagreement
        raise ExactReaderDisagreementError(
            completed=completed,
            completed_directions=tuple(sorted(completed_directions)),
            minimum=cast(Fraction, worst),
            argmin=worst_index,
            witness=cast(Point, worst_witness),
            direction=index,
            dense=dense,
            slab=slab,
        )

    try:
        if workers > 1 and total > 1:
            effective_workers = min(workers, total)
            pool = ProcessPoolExecutor(
                max_workers=effective_workers, mp_context=get_context("fork")
            )
            batches = _bounded_completion_batches(
                pool,
                _exact_direction,
                total=total,
                limit=IN_FLIGHT_WORK_PER_WORKER * effective_workers,
                deadline=deadline,
                clock=clock,
                phase="during normalized exact route",
            )
            for batch in batches:
                completed_before = completed
                landed: list[tuple[int, tuple[Fraction, Point], tuple[Fraction, Point]]] = []
                failure: Exception | None = None
                for _index, future in batch:
                    try:
                        landed.append(future.result())
                    except Exception as error:  # noqa: BLE001 -- retain peer completions first
                        if failure is None:
                            failure = error
                completed_disagreements: list[
                    tuple[int, tuple[Fraction, Point], tuple[Fraction, Point]]
                ] = []
                for result in landed:
                    try:
                        disagreement = retain(result)
                    except Exception as error:  # noqa: BLE001 -- retain every landed peer
                        if failure is None:
                            failure = error
                    else:
                        if disagreement is not None:
                            completed_disagreements.append(disagreement)
                if completed_disagreements:
                    raise_disagreement(min(completed_disagreements, key=lambda row: row[0]))
                if completed > completed_before:
                    progress(
                        completed,
                        tuple(sorted(completed_directions)),
                        cast(Fraction, worst),
                        worst_index,
                        cast(Point, worst_witness),
                    )
                if failure is not None:
                    raise failure
            _expired(deadline, clock, "during normalized exact route")
        else:
            for index in range(total):
                disagreement = retain(_exact_direction(index))
                if disagreement is not None:
                    raise_disagreement(disagreement)
                if completed % 16 == 0 or completed == total:
                    progress(
                        completed,
                        tuple(sorted(completed_directions)),
                        cast(Fraction, worst),
                        worst_index,
                        cast(Point, worst_witness),
                    )
                _expired(deadline, clock, "during normalized exact route")
        if worst is None or worst_witness is None or completed != total:
            raise PacketError("normalized exact route did not complete every direction")
        replay = exact_charge(
            certificate.atoms,
            certificate.threshold_atoms,
            _placement_membership(certificate, worst_index, worst_witness),
        )
        if replay != worst:
            raise PacketError("normalized exact witness disagrees with membership replay")
        succeeded = True
        return ExactRoute(worst, worst_index, worst_witness, completed, disagreements)
    finally:
        if pool is not None:
            if succeeded:
                pool.shutdown()
            else:
                with suppress(Exception):
                    pool.terminate_workers()


def _interval_row(outcome: DirectionOutcome) -> dict[str, object]:
    return {
        "label": outcome.label,
        "status": outcome.status,
        "lower": outcome.lower,
        "upper": outcome.upper,
        "witness": None if outcome.witness is None else list(outcome.witness),
        "boxes": outcome.boxes,
        "stalled": outcome.stalled,
        "budget_exhausted": outcome.budget_exhausted,
    }


def run_interval_route(
    certificate: ThresholdCertificate,
    *,
    workers: int,
    deadline: float,
    clock: Clock,
    progress: Callable[[DirectionOutcome], None],
    log: Path,
) -> IntervalRoute:
    """Run the complete reflected interval route and retain every landed direction."""

    def landed(outcome: DirectionOutcome) -> None:
        _write_direction(log, outcome.label, _interval_row(outcome))
        progress(outcome)
        _expired(deadline, clock, "during reflected interval route")

    try:
        verdict = verify_threshold_by_intervals(
            certificate,
            enclose=True,
            workers=workers,
            progress=landed,
        )
    except IntervalInputError as error:
        raise PacketError(f"reflected interval route refused its input: {error}") from error
    enclosure = verdict.enclosure
    if enclosure is None:
        raise PacketError("reflected interval route returned no complete enclosure")
    return IntervalRoute(
        enclosure[0],
        enclosure[1],
        len(verdict.directions),
        sum(row.stalled for row in verdict.directions),
        sum(row.budget_exhausted for row in verdict.directions),
        verdict.accepted,
    )


def run_dilation_replay(
    path: Path,
    *,
    workers: int,
    deadline: float,
    clock: Clock,
    progress: Callable[[int, Fraction, str], None],
) -> dict[str, object]:
    try:
        return build_limit_record(
            path,
            source_name="candidate.json",
            workers=workers,
            deadline=deadline,
            clock=clock,
            progress=progress,
        )
    except ThresholdSweepDeadlineError as error:
        raise PacketDeadlineError(
            "scientific deadline reached during dilation replay"
        ) from error


def _deadline_settings(
    *,
    workers: int,
    scientific_seconds: float,
    external_seconds: float,
    grace_seconds: float,
) -> dict[str, object]:
    return {
        "workers": workers,
        "scientific_seconds": scientific_seconds,
        "scientific_deadline_scope": SCIENTIFIC_DEADLINE_SCOPE,
        "external_seconds": external_seconds,
        "external_deadline_scope": EXTERNAL_DEADLINE_SCOPE,
        "termination_grace_seconds": grace_seconds,
    }


def initial_preflight_document(
    revision: str,
    *,
    workers: int,
    scientific_seconds: float,
    external_seconds: float,
    grace_seconds: float,
) -> dict[str, object]:
    """Seed the only receipt available until supervised source preflight completes."""

    return {
        "schema": PREFLIGHT_SCHEMA,
        "status": "partial",
        "outcome": "preflight-pending",
        "scientific_decision": "unresolved",
        "claim_limit": CLAIM_LIMIT,
        "sources": {
            "implementation_revision": revision,
            "source_path": SOURCE_PATH,
            "t026_path": T026_PATH,
        },
        "settings": _deadline_settings(
            workers=workers,
            scientific_seconds=scientific_seconds,
            external_seconds=external_seconds,
            grace_seconds=grace_seconds,
        ),
        "clocks": {
            "process_seconds": 0.0,
            "external_lifetime_seconds": None,
        },
        "supervision": {
            "status": "pending",
            "worker_exit_status": None,
            "supervisor_signal": None,
        },
        "phase": "preflight",
        "error": "source and runtime preflight has not completed",
    }


def _initial_document(
    revision: str,
    manifest: list[dict[str, str]],
    runtime: dict[str, object],
    *,
    workers: int,
    scientific_seconds: float,
    external_seconds: float,
    grace_seconds: float,
) -> dict[str, object]:
    return {
        "schema": RESULT_SCHEMA,
        "status": "partial",
        "outcome": "incomplete",
        "scientific_decision": "unresolved",
        "claim_limit": CLAIM_LIMIT,
        "sources": {
            "implementation_revision": revision,
            "manifest": manifest,
            "source_path": SOURCE_PATH,
            "source_git_blob": next(
                row["git_blob"] for row in manifest if row["path"] == SOURCE_PATH
            ),
            "source_sha256": next(
                row["sha256"] for row in manifest if row["path"] == SOURCE_PATH
            ),
            "t026_path": T026_PATH,
            "t026_git_blob": next(
                row["git_blob"] for row in manifest if row["path"] == T026_PATH
            ),
            "t026_sha256": next(row["sha256"] for row in manifest if row["path"] == T026_PATH),
            "runtime": runtime,
        },
        "settings": {
            "core_side": str(PACKET_CORE_SIDE),
            "direction_steps": PACKET_STEPS,
            "angle_limit": str(PACKET_ANGLE_LIMIT),
            "half_gap_tangent": str(PACKET_HALF_GAP),
            "raw_threshold_M_over_11": str(RAW_THRESHOLD),
            "normalization": NORMALIZATION_SETTING,
            **_deadline_settings(
                workers=workers,
                scientific_seconds=scientific_seconds,
                external_seconds=external_seconds,
                grace_seconds=grace_seconds,
            ),
        },
        "clocks": {
            "source_seconds": 0.0,
            "scientific_seconds": 0.0,
            "process_seconds": 0.0,
            "external_lifetime_seconds": None,
        },
        "supervision": {
            "status": "pending",
            "worker_exit_status": None,
            "supervisor_signal": None,
        },
        "phase": "source-replay",
        "raw": {
            "directions_expected": RAW_DIRECTIONS,
            "directions_completed": 0,
            "completed_directions": [],
            "observed_minimum_upper_bound": None,
            "observed_argmin": None,
            "observed_witness": None,
            "raw_minimum": None,
            "comparison": None,
            "witness_replay_charge": None,
            "witness_admissible": None,
            "directions_sha256": None,
        },
        "normalized": None,
        "routes": {
            "exact": None,
            "reflected_interval": None,
            "dilation": None,
        },
        "error": None,
    }


def _exact_rational(value: object, label: str) -> Fraction:
    if not isinstance(value, str):
        raise PacketError(f"{label} is not an exact rational string")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise PacketError(f"{label} is not an exact rational string") from error


def _exact_point(value: object, label: str) -> Point:
    if not isinstance(value, list) or len(value) != 2:
        raise PacketError(f"{label} must have two exact coordinates")
    return (
        _exact_rational(value[0], f"{label} first coordinate"),
        _exact_rational(value[1], f"{label} second coordinate"),
    )


def _direction_index(value: object, expected: int, label: str) -> None:
    if type(value) is not int or not 0 <= cast(int, value) < expected:
        raise PacketError(f"{label} is outside its declared direction set")


def _completed_direction_indices(
    value: object,
    *,
    completed: int,
    expected: int,
    label: str,
) -> tuple[int, ...]:
    if not isinstance(value, list) or len(value) != completed:
        raise PacketError(f"{label} does not match its completed direction count")
    if any(type(index) is not int or not 0 <= index < expected for index in value):
        raise PacketError(f"{label} contains an out-of-range direction")
    indices = cast(list[int], value)
    if indices != sorted(set(indices)):
        raise PacketError(f"{label} is not canonical, sorted, and unique")
    return tuple(indices)


def _completed_direction_labels(
    value: object,
    *,
    completed: int,
    labels: Sequence[str],
    label: str,
) -> tuple[str, ...]:
    if not isinstance(value, list) or len(value) != completed:
        raise PacketError(f"{label} does not match its completed direction count")
    positions = {direction_label: index for index, direction_label in enumerate(labels)}
    if len(positions) != len(labels):
        raise PacketError(f"{label} has duplicate labels in its canonical direction set")
    if any(not isinstance(direction, str) or direction not in positions for direction in value):
        raise PacketError(f"{label} contains an unknown direction")
    directions = cast(list[str], value)
    if directions != sorted(set(directions), key=positions.__getitem__):
        raise PacketError(f"{label} is not canonical, ordered, and unique")
    return tuple(directions)


def _sha256(value: object, label: str) -> None:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise PacketError(f"{label} is not a lowercase SHA-256 digest")


def _validate_runtime_record(value: object) -> None:
    if not isinstance(value, dict) or set(value) != {
        "python",
        "packages",
        "attestation_scope",
    }:
        raise PacketError("runtime fields do not match the closed packet schema")
    python = value.get("python")
    if not isinstance(python, dict) or set(python) != {
        "implementation",
        "version",
        "abi",
        "gil_enabled",
        "environment",
        "executable",
        "resolved_executable",
        "build",
    }:
        raise PacketError("Python runtime fields do not match the closed packet schema")
    version = python.get("version")
    if (
        python.get("implementation") != "cpython"
        or not isinstance(version, str)
        or len(version.split(".")) != 3
        or any(not component.isdigit() for component in version.split("."))
        or not isinstance(python.get("abi"), str)
        or not python.get("abi")
        or type(python.get("gil_enabled")) is not bool
        or not isinstance(python.get("build"), str)
        or not python.get("build")
    ):
        raise PacketError("Python runtime identity is malformed")
    for key in ("environment", "executable", "resolved_executable"):
        path = python.get(key)
        if not isinstance(path, str) or not path or not Path(path).is_absolute():
            raise PacketError(f"Python runtime {key} is not an absolute path")
    packages = value.get("packages")
    if (
        not isinstance(packages, dict)
        or set(packages) != set(RUNTIME_DISTRIBUTIONS)
        or any(
            not isinstance(package_version, str) or not package_version
            for package_version in packages.values()
        )
    ):
        raise PacketError("runtime package identities are malformed")
    if value.get("attestation_scope") != RUNTIME_ATTESTATION_SCOPE:
        raise PacketError("runtime attestation scope changed")


def _is_raw_normalization_checkpoint(
    document: dict[str, object], routes: dict[str, object]
) -> bool:
    if document.get("scientific_decision") != "unresolved" or any(
        value is not None for value in routes.values()
    ):
        return False
    state = (document.get("status"), document.get("outcome"), document.get("phase"))
    return state in {
        ("partial", "incomplete", "raw-sweep"),
        ("partial", "incomplete", "timeout"),
        ("partial", "incomplete", "incomplete"),
        ("invalid", "invalid", "invalid"),
    }


def validate_preflight_document(document: dict[str, object]) -> None:
    """Validate a non-scientific receipt from the supervised preflight interval."""

    if (
        set(document)
        != {
            "schema",
            "status",
            "outcome",
            "scientific_decision",
            "claim_limit",
            "sources",
            "settings",
            "clocks",
            "supervision",
            "phase",
            "error",
        }
        or document.get("schema") != PREFLIGHT_SCHEMA
    ):
        raise PacketError("document does not match the closed preflight schema")
    if (
        document.get("claim_limit") != CLAIM_LIMIT
        or document.get("scientific_decision") != "unresolved"
        or document.get("phase") != "preflight"
    ):
        raise PacketError("preflight receipt changed its scientific scope")
    state = (document.get("status"), document.get("outcome"))
    if state not in {
        ("partial", "preflight-pending"),
        ("partial", "preflight-timeout"),
        ("partial", "preflight-failed"),
        ("invalid", "preflight-invalid"),
    }:
        raise PacketError("preflight receipt has an impossible state")
    if not isinstance(document.get("error"), str) or not document["error"]:
        raise PacketError("preflight receipt lacks its unresolved reason")

    sources = document.get("sources")
    if not isinstance(sources, dict) or set(sources) != {
        "implementation_revision",
        "source_path",
        "t026_path",
    }:
        raise PacketError("preflight source fields do not match the closed schema")
    revision = sources.get("implementation_revision")
    if (
        not isinstance(revision, str)
        or len(revision) != 40
        or any(character not in "0123456789abcdef" for character in revision)
        or sources.get("source_path") != SOURCE_PATH
        or sources.get("t026_path") != T026_PATH
    ):
        raise PacketError("preflight source request is malformed")

    settings = document.get("settings")
    if not isinstance(settings, dict) or set(settings) != {
        "workers",
        "scientific_seconds",
        "scientific_deadline_scope",
        "external_seconds",
        "external_deadline_scope",
        "termination_grace_seconds",
    }:
        raise PacketError("preflight settings do not match the closed schema")
    workers = settings.get("workers")
    scientific = settings.get("scientific_seconds")
    external = settings.get("external_seconds")
    grace = settings.get("termination_grace_seconds")
    if (
        type(workers) is not int
        or not 1 <= cast(int, workers) <= MAX_WORKERS
        or not isinstance(scientific, (int, float))
        or isinstance(scientific, bool)
        or not isinstance(external, (int, float))
        or isinstance(external, bool)
        or not isinstance(grace, (int, float))
        or isinstance(grace, bool)
        or not all(math.isfinite(float(value)) for value in (scientific, external, grace))
        or not 0 < scientific <= external
        or grace <= 0
        or settings.get("scientific_deadline_scope") != SCIENTIFIC_DEADLINE_SCOPE
        or settings.get("external_deadline_scope") != EXTERNAL_DEADLINE_SCOPE
    ):
        raise PacketError("preflight deadline settings are malformed")

    clocks = document.get("clocks")
    if not isinstance(clocks, dict) or set(clocks) != {
        "process_seconds",
        "external_lifetime_seconds",
    }:
        raise PacketError("preflight clocks do not match the closed schema")
    process_seconds = clocks.get("process_seconds")
    external_lifetime = clocks.get("external_lifetime_seconds")
    if (
        not isinstance(process_seconds, (int, float))
        or isinstance(process_seconds, bool)
        or not math.isfinite(process_seconds)
        or process_seconds < 0
        or (
            external_lifetime is not None
            and (
                not isinstance(external_lifetime, (int, float))
                or isinstance(external_lifetime, bool)
                or not math.isfinite(external_lifetime)
                or external_lifetime < 0
            )
        )
    ):
        raise PacketError("preflight clocks are malformed")

    supervision = document.get("supervision")
    if not isinstance(supervision, dict) or set(supervision) != {
        "status",
        "worker_exit_status",
        "supervisor_signal",
    }:
        raise PacketError("preflight supervision fields do not match the closed schema")
    supervision_status = supervision.get("status")
    worker_status = supervision.get("worker_exit_status")
    supervisor_signal = supervision.get("supervisor_signal")
    if supervision_status not in {
        "pending",
        "observed-exit",
        "deadline-before-launch",
        "deadline-terminated",
        "launch-failed",
        "supervisor-interrupted",
    } or (worker_status is not None and type(worker_status) is not int):
        raise PacketError("preflight supervision is malformed")
    if supervisor_signal is not None and (
        type(supervisor_signal) is not int
        or supervisor_signal not in {signal.SIGHUP, signal.SIGTERM, signal.SIGINT}
    ):
        raise PacketError("preflight supervisor signal is malformed")
    if supervision_status != "supervisor-interrupted" and supervisor_signal is not None:
        raise PacketError("preflight signal provenance lacks an interrupted supervisor")
    if supervision_status == "pending" and (
        worker_status is not None or external_lifetime is not None
    ):
        raise PacketError("pending preflight supervision carries a completed observation")
    if supervision_status != "pending" and external_lifetime is None:
        raise PacketError("completed preflight supervision lacks external lifetime")
    if supervision_status == "observed-exit" and worker_status is None:
        raise PacketError("observed preflight exit lacks its status")
    if supervision_status in {"deadline-before-launch", "launch-failed"} and (
        worker_status is not None
    ):
        raise PacketError("prelaunch supervision cannot carry a worker exit status")
    if state == ("partial", "preflight-pending") and supervision_status != "pending":
        raise PacketError("completed supervision retained a pending preflight state")
    if state == ("partial", "preflight-timeout") and supervision_status not in {
        "deadline-before-launch",
        "deadline-terminated",
    }:
        raise PacketError("preflight timeout lacks deadline supervision")
    if state == ("partial", "preflight-failed") and supervision_status not in {
        "pending",
        "observed-exit",
        "launch-failed",
        "supervisor-interrupted",
    }:
        raise PacketError("preflight failure has incompatible supervision")
    if state == ("invalid", "preflight-invalid") and supervision_status not in {
        "pending",
        "observed-exit",
        "deadline-terminated",
        "supervisor-interrupted",
    }:
        raise PacketError("invalid preflight has incompatible supervision")


def validate_result_document(document: dict[str, object]) -> None:  # noqa: C901
    """Validate the closed top-level state machine and its decisive invariants."""

    keys = {
        "schema",
        "status",
        "outcome",
        "scientific_decision",
        "claim_limit",
        "sources",
        "settings",
        "clocks",
        "supervision",
        "phase",
        "raw",
        "normalized",
        "routes",
        "error",
    }
    if set(document) != keys or document.get("schema") != RESULT_SCHEMA:
        raise PacketError("result document does not match the closed packet schema")
    if document["claim_limit"] != CLAIM_LIMIT:
        raise PacketError("result claim limit changed")
    status = document["status"]
    decision = document["scientific_decision"]
    outcome = document["outcome"]
    allowed_states = {
        ("complete", "packet-accepted", "accepted", "complete"),
        ("complete", "raw-threshold-rejected", "rejected", "complete"),
    }
    if status not in ("complete", "partial", "invalid"):
        raise PacketError("result status is invalid")
    if decision not in ("accepted", "rejected", "unresolved"):
        raise PacketError("scientific decision is invalid")
    error = document["error"]
    if status == "partial" and (
        decision != "unresolved" or not isinstance(error, str) or not error.strip()
    ):
        raise PacketError("partial result must retain an unresolved reason")
    if status == "invalid" and (
        decision != "unresolved" or not isinstance(error, str) or not error.strip()
    ):
        raise PacketError("invalid run must remain scientifically unresolved")
    if status == "complete" and outcome == "packet-accepted" and decision != "accepted":
        raise PacketError("accepted packet has the wrong scientific decision")
    if (
        status == "complete"
        and (status, outcome, decision, document["phase"]) not in allowed_states
    ):
        raise PacketError("complete result has an impossible outcome or scientific decision")
    if status == "complete" and document["error"] is not None:
        raise PacketError("complete result cannot retain an error")
    if status == "partial" and outcome != "incomplete":
        raise PacketError("partial run must have the incomplete execution outcome")
    if status == "partial" and document["phase"] not in {
        "source-replay",
        "raw-sweep",
        "normalized-exact",
        "reflected-interval",
        "dilation-replay",
        "incomplete",
        "timeout",
    }:
        raise PacketError("partial run has an impossible phase")
    if status == "invalid" and outcome not in ("invalid", "reader-disagreement"):
        raise PacketError("invalid run has an impossible execution outcome")
    if status == "invalid" and document["phase"] != "invalid":
        raise PacketError("invalid run has an impossible phase")
    raw = cast(dict[str, object], document["raw"])
    if set(raw) != {
        "directions_expected",
        "directions_completed",
        "completed_directions",
        "observed_minimum_upper_bound",
        "observed_argmin",
        "observed_witness",
        "raw_minimum",
        "comparison",
        "witness_replay_charge",
        "witness_admissible",
        "directions_sha256",
    }:
        raise PacketError("raw result fields do not match the closed packet schema")
    if raw.get("directions_expected") != RAW_DIRECTIONS:
        raise PacketError("raw direction count changed")
    completed = raw.get("directions_completed")
    if type(completed) is not int or not 0 <= cast(int, completed) <= RAW_DIRECTIONS:
        raise PacketError("raw completed direction count is invalid")
    completed_indices = _completed_direction_indices(
        raw.get("completed_directions"),
        completed=cast(int, completed),
        expected=RAW_DIRECTIONS,
        label="raw completed directions",
    )
    if completed == RAW_DIRECTIONS and completed_indices != tuple(range(RAW_DIRECTIONS)):
        raise PacketError("complete raw sweep does not name the full direction set")
    if completed < RAW_DIRECTIONS and document["phase"] not in {
        "source-replay",
        "raw-sweep",
        "timeout",
        "incomplete",
        "invalid",
    }:
        raise PacketError("partial raw direction set is incompatible with the result phase")
    if completed < RAW_DIRECTIONS and raw.get("raw_minimum") is not None:
        raise PacketError("partial observed minimum was mislabeled as the global minimum")
    if raw.get("raw_minimum") is None and document["normalized"] is not None:
        raise PacketError("normalization appeared before a complete raw minimum")
    if cast(int, completed) == 0:
        if any(
            raw.get(key) is not None
            for key in (
                "observed_minimum_upper_bound",
                "observed_argmin",
                "observed_witness",
            )
        ):
            raise PacketError("empty raw prefix carries observed-minimum fields")
    else:
        _exact_rational(raw.get("observed_minimum_upper_bound"), "raw observed minimum")
        _direction_index(raw.get("observed_argmin"), RAW_DIRECTIONS, "raw observed argmin")
        if raw.get("observed_argmin") not in completed_indices:
            raise PacketError("raw observed argmin is absent from completed directions")
        _exact_point(raw.get("observed_witness"), "raw observed witness")
    if (
        cast(int, completed) == RAW_DIRECTIONS
        and raw.get("raw_minimum") is None
        and status != "invalid"
    ):
        raise PacketError("complete raw sweep does not report its global minimum")
    if raw.get("raw_minimum") is not None:
        minimum = _exact_rational(raw["raw_minimum"], "raw global minimum")
        expected = "accepted" if minimum > RAW_THRESHOLD else "rejected"
        if raw.get("comparison") != expected:
            raise PacketError("raw threshold comparison is not strict")
        if (
            raw.get("witness_replay_charge") != str(minimum)
            or raw.get("witness_admissible") is not True
        ):
            raise PacketError("complete raw minimum lacks its exact admissible witness replay")
        _sha256(raw.get("directions_sha256"), "raw retained-direction digest")
    elif raw.get("directions_sha256") is not None:
        raise PacketError("incomplete raw sweep carries a complete-direction digest")
    sources = cast(dict[str, object], document["sources"])
    if set(sources) != {
        "implementation_revision",
        "manifest",
        "source_path",
        "source_git_blob",
        "source_sha256",
        "t026_path",
        "t026_git_blob",
        "t026_sha256",
        "runtime",
    }:
        raise PacketError("source fields do not match the closed packet schema")
    if sources.get("source_path") != SOURCE_PATH or sources.get("t026_path") != T026_PATH:
        raise PacketError("result source paths changed")
    revision = sources.get("implementation_revision")
    if (
        not isinstance(revision, str)
        or len(revision) != 40
        or any(character not in "0123456789abcdef" for character in revision)
    ):
        raise PacketError("result implementation revision is malformed")
    manifest = sources.get("manifest")
    if not isinstance(manifest, list) or not manifest:
        raise PacketError("result source manifest is empty or malformed")
    for row in cast(list[object], manifest):
        if not isinstance(row, dict) or set(row) != {"path", "git_blob", "sha256"}:
            raise PacketError("result source manifest row is malformed")
        path = row.get("path")
        blob = row.get("git_blob")
        digest = row.get("sha256")
        if (
            not isinstance(path, str)
            or Path(path).is_absolute()
            or ".." in Path(path).parts
            or not isinstance(blob, str)
            or len(blob) != 40
            or any(character not in "0123456789abcdef" for character in blob)
            or not isinstance(digest, str)
            or len(digest) != 64
            or any(character not in "0123456789abcdef" for character in digest)
        ):
            raise PacketError("result source manifest identity is malformed")
    manifest_paths = [cast(dict[str, str], row)["path"] for row in manifest]
    if (
        manifest_paths != sorted(manifest_paths)
        or len(manifest_paths) != len(set(manifest_paths))
        or not {SOURCE_PATH, T026_PATH, *PROJECT_RUNTIME_PATHS}.issubset(manifest_paths)
    ):
        raise PacketError("result source manifest is unsorted, duplicated, or incomplete")
    by_path = {cast(dict[str, str], row)["path"]: cast(dict[str, str], row) for row in manifest}
    if (
        by_path.get(SOURCE_PATH, {}).get("sha256") != sources.get("source_sha256")
        or by_path.get(SOURCE_PATH, {}).get("git_blob") != sources.get("source_git_blob")
        or by_path.get(T026_PATH, {}).get("sha256") != sources.get("t026_sha256")
        or by_path.get(T026_PATH, {}).get("git_blob") != sources.get("t026_git_blob")
    ):
        raise PacketError("result source identities differ from the manifest")
    if (
        sources.get("source_sha256") != SOURCE_SHA256
        or sources.get("t026_sha256") != T026_SHA256
        or sources.get("source_git_blob") != SOURCE_BLOB
        or sources.get("t026_git_blob") != T026_BLOB
        or by_path.get(SOURCE_PATH, {}).get("git_blob") != SOURCE_BLOB
        or by_path.get(T026_PATH, {}).get("git_blob") != T026_BLOB
    ):
        raise PacketError("result does not name the admitted T-025 and T-026 sources")
    _validate_runtime_record(sources.get("runtime"))
    settings = cast(dict[str, object], document["settings"])
    if set(settings) != {
        "core_side",
        "direction_steps",
        "angle_limit",
        "half_gap_tangent",
        "raw_threshold_M_over_11",
        "normalization",
        "workers",
        "scientific_seconds",
        "scientific_deadline_scope",
        "external_seconds",
        "external_deadline_scope",
        "termination_grace_seconds",
    }:
        raise PacketError("settings fields do not match the closed packet schema")
    if (
        settings.get("core_side") != str(PACKET_CORE_SIDE)
        or settings.get("direction_steps") != PACKET_STEPS
        or settings.get("angle_limit") != str(PACKET_ANGLE_LIMIT)
        or settings.get("half_gap_tangent") != str(PACKET_HALF_GAP)
        or settings.get("raw_threshold_M_over_11") != str(RAW_THRESHOLD)
        or settings.get("normalization") != NORMALIZATION_SETTING
        or settings.get("scientific_deadline_scope") != SCIENTIFIC_DEADLINE_SCOPE
        or settings.get("external_deadline_scope") != EXTERNAL_DEADLINE_SCOPE
    ):
        raise PacketError("fixed packet settings changed")
    workers = settings.get("workers")
    scientific = settings.get("scientific_seconds")
    external = settings.get("external_seconds")
    grace = settings.get("termination_grace_seconds")
    if (
        type(workers) is not int
        or not 1 <= cast(int, workers) <= MAX_WORKERS
        or not isinstance(scientific, (int, float))
        or isinstance(scientific, bool)
        or not isinstance(external, (int, float))
        or isinstance(external, bool)
        or not isinstance(grace, (int, float))
        or isinstance(grace, bool)
        or not all(math.isfinite(float(value)) for value in (scientific, external, grace))
        or not 0 < scientific <= external
        or grace <= 0
    ):
        raise PacketError("worker or deadline settings are malformed")
    clocks = cast(dict[str, object], document["clocks"])
    if set(clocks) != {
        "source_seconds",
        "scientific_seconds",
        "process_seconds",
        "external_lifetime_seconds",
    } or any(
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(value)
        or value < 0
        for key, value in clocks.items()
        if key != "external_lifetime_seconds"
    ):
        raise PacketError("result clocks are malformed")
    external_lifetime = clocks["external_lifetime_seconds"]
    if external_lifetime is not None and (
        not isinstance(external_lifetime, (int, float))
        or isinstance(external_lifetime, bool)
        or not math.isfinite(external_lifetime)
        or external_lifetime < 0
    ):
        raise PacketError("external lifetime clock is malformed")
    if status == "complete" and any(
        cast(float, clocks[key]) >= scientific
        for key in ("scientific_seconds", "process_seconds")
    ):
        raise PacketError("complete receipt exceeds its scientific deadline")
    supervision = document["supervision"]
    if not isinstance(supervision, dict) or set(supervision) != {
        "status",
        "worker_exit_status",
        "supervisor_signal",
    }:
        raise PacketError("supervision fields do not match the closed packet schema")
    supervision_status = supervision.get("status")
    worker_exit_status = supervision.get("worker_exit_status")
    supervisor_signal = supervision.get("supervisor_signal")
    if supervision_status not in {
        "pending",
        "observed-exit",
        "deadline-before-launch",
        "deadline-terminated",
        "launch-failed",
        "supervisor-interrupted",
    }:
        raise PacketError("supervision status is malformed")
    if worker_exit_status is not None and type(worker_exit_status) is not int:
        raise PacketError("supervised worker exit status is malformed")
    if supervisor_signal is not None and (
        type(supervisor_signal) is not int
        or supervisor_signal not in {signal.SIGHUP, signal.SIGTERM, signal.SIGINT}
    ):
        raise PacketError("supervisor signal is malformed")
    if supervision_status != "supervisor-interrupted" and supervisor_signal is not None:
        raise PacketError("signal provenance lacks an interrupted supervisor")
    if supervision_status == "pending" and (
        worker_exit_status is not None or external_lifetime is not None
    ):
        raise PacketError("pending supervision carries a completed observation")
    if supervision_status != "pending" and external_lifetime is None:
        raise PacketError("completed supervision lacks external lifetime")
    if supervision_status == "observed-exit" and worker_exit_status is None:
        raise PacketError("observed worker exit lacks its status")
    if supervision_status in {"deadline-before-launch", "launch-failed"} and (
        worker_exit_status is not None
    ):
        raise PacketError("prelaunch supervision cannot carry a worker exit status")
    normalized = document["normalized"]
    if normalized is not None:
        if not isinstance(normalized, dict) or set(normalized) != {
            "path",
            "sha256",
            "alpha",
            "least_cell_charge",
            "total_budget",
            "closed_form_conditions",
        }:
            raise PacketError("normalized fields do not match the closed packet schema")
        if (
            normalized.get("path") != "candidate.json"
            or normalized.get("least_cell_charge") != "1"
        ):
            raise PacketError("normalized byte identity or minimum declaration changed")
        digest = normalized.get("sha256")
        conditions = normalized.get("closed_form_conditions")
        _sha256(digest, "normalized source digest")
        if (
            not isinstance(conditions, list)
            or not conditions
            or any(
                not isinstance(row, dict)
                or set(row) != {"name", "detail", "holds"}
                or not isinstance(row.get("name"), str)
                or not isinstance(row.get("detail"), str)
                or row.get("holds") is not True
                for row in conditions
            )
        ):
            raise PacketError("normalized digest or closed-form decisions are malformed")
        minimum = _exact_rational(raw["raw_minimum"], "normalization raw minimum")
        total_budget = _exact_rational(normalized.get("total_budget"), "normalized budget")
        alpha = _exact_rational(normalized.get("alpha"), "normalization alpha")
        if (
            normalized.get("alpha") != str(1 / minimum)
            or normalized.get("total_budget") != str(SOURCE_BUDGET / minimum)
            or alpha != 1 / minimum
            or total_budget != SOURCE_BUDGET / minimum
            or total_budget >= 11
        ):
            raise PacketError("normalized scale or budget differs from alpha=1/m")
    routes = cast(dict[str, object], document["routes"])
    if set(routes) != {"exact", "reflected_interval", "dilation"}:
        raise PacketError("route fields do not match the closed packet schema")
    exact = routes["exact"]
    if exact is not None and (
        not isinstance(exact, dict)
        or exact.get("status") not in ("partial", "complete", "invalid")
        or exact.get("directions_expected") != RAW_DIRECTIONS
    ):
        raise PacketError("exact route state is malformed")
    if isinstance(exact, dict):
        exact_complete = exact.get("status") == "complete"
        exact_invalid = exact.get("status") == "invalid"
        if exact_invalid and (
            status != "invalid"
            or document["phase"] != "invalid"
            or outcome != "reader-disagreement"
        ):
            raise PacketError("invalid exact route is incompatible with the result state")
        if (
            not exact_complete
            and not exact_invalid
            and (
                status != "partial"
                or document["phase"] not in {"normalized-exact", "timeout", "incomplete"}
            )
        ):
            raise PacketError("partial exact route is incompatible with the result state")
        if exact_complete:
            expected_exact_keys = {
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
            }
        elif exact_invalid:
            expected_exact_keys = {
                "status",
                "source_sha256",
                "directions_expected",
                "directions_completed",
                "completed_directions",
                "observed_minimum_upper_bound",
                "argmin",
                "witness",
                "reader_disagreement",
            }
        else:
            expected_exact_keys = {
                "status",
                "source_sha256",
                "directions_expected",
                "directions_completed",
                "completed_directions",
                "observed_minimum_upper_bound",
                "argmin",
                "witness",
            }
        if set(exact) != expected_exact_keys:
            raise PacketError("exact route fields do not match its state")
        exact_completed = exact.get("directions_completed")
        if (
            type(exact_completed) is not int
            or not 0 <= cast(int, exact_completed) <= RAW_DIRECTIONS
        ):
            raise PacketError("exact route completed count is malformed")
        exact_indices = _completed_direction_indices(
            exact.get("completed_directions"),
            completed=cast(int, exact_completed),
            expected=RAW_DIRECTIONS,
            label="exact completed directions",
        )
        if exact.get("argmin") not in exact_indices:
            raise PacketError("exact route argmin is absent from completed directions")
        _direction_index(exact.get("argmin"), RAW_DIRECTIONS, "exact route argmin")
        _exact_point(exact.get("witness"), "exact route witness")
        if exact_complete:
            if exact_completed != RAW_DIRECTIONS:
                raise PacketError("complete exact route lacks every direction")
            if exact_indices != tuple(range(RAW_DIRECTIONS)):
                raise PacketError("complete exact route does not name the full direction set")
            _exact_rational(exact.get("minimum"), "exact route minimum")
            disagreements = exact.get("dense_slab_disagreements")
            if type(disagreements) is not int or cast(int, disagreements) < 0:
                raise PacketError("exact route disagreement count is malformed")
            _sha256(exact.get("directions_sha256"), "exact retained-direction digest")
        else:
            if not exact_invalid and exact_completed == RAW_DIRECTIONS:
                raise PacketError("partial exact route names a complete direction set")
            _exact_rational(
                exact.get("observed_minimum_upper_bound"),
                "exact route observed minimum",
            )
            if exact_invalid:
                disagreement = exact.get("reader_disagreement")
                if not isinstance(disagreement, dict) or set(disagreement) != {
                    "direction",
                    "dense",
                    "dense_witness",
                    "slab",
                    "slab_witness",
                }:
                    raise PacketError("exact reader disagreement is malformed")
                _direction_index(
                    disagreement.get("direction"),
                    RAW_DIRECTIONS,
                    "exact disagreement direction",
                )
                if disagreement.get("direction") not in exact_indices:
                    raise PacketError(
                        "exact disagreement direction is absent from completed directions"
                    )
                dense = (
                    _exact_rational(disagreement.get("dense"), "exact disagreement dense"),
                    _exact_point(
                        disagreement.get("dense_witness"),
                        "exact disagreement dense witness",
                    ),
                )
                slab = (
                    _exact_rational(disagreement.get("slab"), "exact disagreement slab"),
                    _exact_point(
                        disagreement.get("slab_witness"),
                        "exact disagreement slab witness",
                    ),
                )
                if dense == slab:
                    raise PacketError("exact reader disagreement names equal reader results")
    interval = routes["reflected_interval"]
    if interval is not None and (
        not isinstance(interval, dict)
        or interval.get("status") not in ("partial", "complete")
        or interval.get("directions_expected") != INTERVAL_DIRECTIONS
    ):
        raise PacketError("interval route state is malformed")
    if isinstance(interval, dict):
        interval_complete = interval.get("status") == "complete"
        expected_interval_keys = (
            {
                "status",
                "source_sha256",
                "directions_expected",
                "directions_completed",
                "enclosure",
                "stalled",
                "budget_exhausted",
                "accepted",
                "directions_sha256",
            }
            if interval_complete
            else {
                "status",
                "source_sha256",
                "directions_expected",
                "directions_completed",
                "completed_directions",
                "last",
            }
        )
        if set(interval) != expected_interval_keys:
            raise PacketError("interval route fields do not match its state")
        interval_completed = interval.get("directions_completed")
        if (
            type(interval_completed) is not int
            or not 0 <= cast(int, interval_completed) <= INTERVAL_DIRECTIONS
        ):
            raise PacketError("interval route completed count is malformed")
        if interval_complete:
            if interval_completed != INTERVAL_DIRECTIONS:
                raise PacketError("complete interval route lacks every direction")
            enclosure = interval.get("enclosure")
            if not isinstance(enclosure, list) or len(enclosure) != 2:
                raise PacketError("interval enclosure is malformed")
            lower = _exact_rational(enclosure[0], "interval lower enclosure")
            upper = _exact_rational(enclosure[1], "interval upper enclosure")
            if lower > upper:
                raise PacketError("interval enclosure is reversed")
            for label in ("stalled", "budget_exhausted"):
                value = interval.get(label)
                if type(value) is not int or cast(int, value) < 0:
                    raise PacketError(f"interval {label} count is malformed")
            if type(interval.get("accepted")) is not bool:
                raise PacketError("interval acceptance flag is malformed")
            _sha256(interval.get("directions_sha256"), "interval retained-direction digest")
        else:
            interval_labels = tuple(str(index) for index in range(PACKET_STEPS + 1)) + tuple(
                f"{index}'" for index in range(1, PACKET_STEPS + 1)
            )
            interval_completed_labels = _completed_direction_labels(
                interval.get("completed_directions"),
                completed=cast(int, interval_completed),
                labels=interval_labels,
                label="interval completed directions",
            )
            last = interval.get("last")
            if not isinstance(last, dict):
                raise PacketError("partial interval route lacks its last retained direction")
            if last.get("label") not in interval_completed_labels:
                raise PacketError(
                    "partial interval last row is absent from completed directions"
                )
    normalized_digest = normalized.get("sha256") if isinstance(normalized, dict) else None
    if isinstance(exact, dict) and exact.get("source_sha256") != normalized_digest:
        raise PacketError("exact route names different normalized bytes")
    if isinstance(interval, dict) and interval.get("source_sha256") != normalized_digest:
        raise PacketError("interval route names different normalized bytes")
    dilation = routes["dilation"]
    if dilation is not None and (
        not isinstance(dilation, dict) or dilation.get("status") not in {"partial", "complete"}
    ):
        raise PacketError("dilation route state is malformed")
    if isinstance(dilation, dict):
        dilation_complete = dilation.get("status") == "complete"
        expected_dilation_keys = (
            {
                "status",
                "source_sha256",
                "directions_expected",
                "directions_completed",
                "directions_sha256",
                "record_sha256",
                "bounded_side",
                "bounded_side_squared",
                "strictly_above_t026",
            }
            if dilation_complete
            else {
                "status",
                "source_sha256",
                "directions_expected",
                "directions_completed",
                "completed_directions",
                "last",
            }
        )
        if set(dilation) != expected_dilation_keys:
            raise PacketError("dilation route fields do not match its state")
        _sha256(dilation.get("source_sha256"), "dilation source digest")
        if dilation.get("directions_expected") != RAW_DIRECTIONS:
            raise PacketError("dilation direction count changed")
        dilation_completed = dilation.get("directions_completed")
        if (
            type(dilation_completed) is not int
            or not 0 <= cast(int, dilation_completed) <= RAW_DIRECTIONS
        ):
            raise PacketError("dilation completed count is malformed")
        if dilation_complete:
            if dilation_completed != RAW_DIRECTIONS:
                raise PacketError("complete dilation replay lacks every direction")
            _sha256(dilation.get("directions_sha256"), "dilation direction digest")
            _sha256(dilation.get("record_sha256"), "dilation record digest")
            if not isinstance(dilation.get("bounded_side"), str) or not dilation.get(
                "bounded_side"
            ):
                raise PacketError("dilation bounded side is malformed")
            _exact_rational(dilation.get("bounded_side_squared"), "dilation squared side")
            if dilation.get("strictly_above_t026") is not True:
                raise PacketError("dilation comparison flag is malformed")
        else:
            dilation_completed_labels = _completed_direction_labels(
                dilation.get("completed_directions"),
                completed=cast(int, dilation_completed),
                labels=tuple(str(index) for index in range(RAW_DIRECTIONS)),
                label="dilation completed directions",
            )
            last = dilation.get("last")
            if not isinstance(last, dict):
                raise PacketError("partial dilation replay lacks its last retained direction")
            if last.get("label") not in dilation_completed_labels:
                raise PacketError(
                    "partial dilation last row is absent from completed directions"
                )
    if interval is not None and not (
        isinstance(exact, dict) and exact.get("status") == "complete"
    ):
        raise PacketError("interval route appeared before exact completion")
    if dilation is not None and not (
        isinstance(interval, dict) and interval.get("status") == "complete"
    ):
        raise PacketError("dilation route appeared before interval completion")
    if (
        raw.get("comparison") == "accepted"
        and normalized is None
        and not _is_raw_normalization_checkpoint(document, routes)
    ):
        raise PacketError(
            "accepted raw minimum without normalized bytes is not a checkpoint gap"
        )
    if (
        status == "complete"
        and outcome == "raw-threshold-rejected"
        and (
            document["normalized"] is not None
            or any(value is not None for value in routes.values())
        )
    ):
        raise PacketError("raw rejection carries post-normalization evidence")
    if (
        status == "complete"
        and outcome == "packet-accepted"
        and (
            not isinstance(normalized, dict)
            or not all(
                isinstance(routes[name], dict)
                and cast(dict[str, object], routes[name]).get("status") == "complete"
                for name in ("exact", "reflected_interval", "dilation")
            )
        )
    ):
        raise PacketError("accepted packet lacks complete retaining readers")
    if status == "complete" and outcome == "packet-accepted":
        accepted_exact = cast(dict[str, object], routes["exact"])
        accepted_interval = cast(dict[str, object], routes["reflected_interval"])
        accepted_dilation = cast(dict[str, object], routes["dilation"])
        if (
            raw.get("comparison") != "accepted"
            or accepted_exact.get("minimum") != "1"
            or accepted_exact.get("dense_slab_disagreements") != 0
            or accepted_interval.get("enclosure") != ["1", "1"]
            or accepted_interval.get("stalled") != 0
            or accepted_interval.get("budget_exhausted") != 0
            or accepted_interval.get("accepted") is not True
            or accepted_dilation.get("source_sha256")
            != cast(dict[str, object], normalized).get("sha256")
            or accepted_dilation.get("strictly_above_t026") is not True
        ):
            raise PacketError("accepted packet carries a non-accepting reader result")


def write_result(path: Path, document: dict[str, object]) -> None:
    if document.get("schema") == PREFLIGHT_SCHEMA:
        validate_preflight_document(document)
    else:
        validate_result_document(document)
    atomic_write_text(path, json.dumps(document, indent=2, allow_nan=False) + "\n")


def _source_record(document: dict[str, object]) -> dict[str, object]:
    return cast(dict[str, object], document["sources"])


def _routes(document: dict[str, object]) -> dict[str, object]:
    return cast(dict[str, object], document["routes"])


def _require(condition: object, message: str) -> None:
    if not condition:
        raise PacketError(message)


def _validate_dilation_readback(
    record: dict[str, object],
    certificate: ThresholdCertificate,
    candidate_sha: str,
) -> None:
    """Re-derive the dilation summary from normalized geometry and close its schema."""

    if (
        set(record)
        != {
            "schema",
            "source",
            "sharpened_containment",
            "strict_dilation_family",
            "conclusion",
            "proof",
        }
        or record.get("schema") != THRESHOLD_LIMIT_RECORD_SCHEMA
    ):
        raise PacketError("dilation record fields or schema changed")
    point = certificate.point_certificate
    gap = point.largest_half_gap_tangent
    factor = sharp_dilation_ceiling(certificate)
    bounded = factor.scaled(certificate.outer_side)
    source = cast(dict[str, object], record["source"])
    expected_conditions = [
        report.name for report in closed_form_threshold_conditions(certificate)
    ] + ["Condition 5' every reachable cell is charged at least 1"]
    expected_source = {
        "certificate": "candidate.json",
        "sha256": candidate_sha,
        "n": certificate.n,
        "outer_side": str(certificate.outer_side),
        "square_side": str(certificate.square_side),
        "half_gap_tangent": str(gap),
        "coarse_containment": str(certificate.square_side * (1 + gap)),
        "total_budget": str(certificate.total_budget),
        "minimum_cell_charge": "1",
        "accepted_conditions": expected_conditions,
        "variant": "threshold",
        "point_atoms": len(certificate.atoms),
        "threshold_atoms": len(certificate.threshold_atoms),
    }
    if source != expected_source:
        raise PacketError("dilation source summary differs from normalized bytes")

    conclusion = cast(dict[str, object], record["conclusion"])
    expected_conclusion = {
        "bounded_side": bounded.exact,
        "bounded_side_squared": str(bounded.squared),
        "bounded_side_defining_polynomial": bounded.defining_polynomial,
        "decimal": _decimal(bounded),
        "relation": ">=",
        "endpoint_certificate": False,
    }
    if conclusion != expected_conclusion:
        raise PacketError("dilation conclusion differs from the rederived exact limit")

    containment = cast(dict[str, object], record["sharpened_containment"])
    left = certificate.square_side**2 * (1 + gap) ** 2
    right = 1 + gap * gap
    if (
        set(containment)
        != {
            "identity",
            "gap_domain",
            "monotonicity_identity",
            "strict_factor_test",
            "strict_factor_test_left_multiplier",
            "strict_factor_test_right",
            "source_gap_below_one",
        }
        or containment.get("strict_factor_test_left_multiplier") != str(left)
        or containment.get("strict_factor_test_right") != str(right)
        or containment.get("strict_factor_test") != f"q^2 * {left} < {right}"
        or containment.get("gap_domain") != f"0 <= t <= D = {gap} < 1"
        or containment.get("source_gap_below_one") is not True
    ):
        raise PacketError("dilation containment summary differs from normalized geometry")

    family = cast(dict[str, object], record["strict_dilation_family"])
    if (
        set(family)
        != {
            "factor_supremum",
            "factor_supremum_squared",
            "factor_supremum_decimal",
            "factor_supremum_irrational",
            "factor_supremum_defining_polynomial",
            "factor_domain",
            "scaled_containment_test",
            "invariants",
        }
        or family.get("factor_supremum") != factor.exact
        or family.get("factor_supremum_squared") != str(factor.squared)
        or family.get("factor_supremum_decimal") != _decimal(factor)
        or family.get("factor_supremum_irrational") != factor.irrational
        or family.get("factor_supremum_defining_polynomial") != factor.defining_polynomial
        or family.get("factor_domain") != f"q in Q with q > 0 and q^2 < {factor.squared}"
        or not isinstance(family.get("invariants"), list)
        or len(cast(list[object], family["invariants"])) != 3
    ):
        raise PacketError("dilation family summary differs from normalized geometry")
    proof = cast(dict[str, object], record["proof"])
    if (
        set(proof)
        != {
            "strict_family",
            "density_step",
            "embedding_step",
            "order_step",
            "requires_compactness",
            "endpoint_status",
        }
        or proof.get("requires_compactness") is not False
        or any(
            not isinstance(proof.get(key), str) or not proof.get(key)
            for key in set(proof) - {"requires_compactness"}
        )
    ):
        raise PacketError("dilation proof summary is malformed")


def execute_packet(  # noqa: PLR0911
    source: bytes,
    t026_source: bytes,
    *,
    revision: str,
    manifest: list[dict[str, str]],
    runtime: dict[str, object],
    output_dir: Path,
    workers: int,
    scientific_seconds: float,
    external_seconds: float,
    grace_seconds: float,
    process_deadline: float,
    invocation_started: float | None = None,
    clock: Clock = time.perf_counter,
    raw_runner: RawRunner = run_raw_sweep,
    exact_runner: ExactRunner = run_exact_route,
    interval_runner: IntervalRunner = run_interval_route,
    dilation_runner: DilationRunner = run_dilation_replay,
    raw_witness_replay: RawWitnessReplay = replay_raw_witness,
    publisher: Publisher = write_result,
) -> dict[str, object]:
    """Execute the fixed packet and checkpoint every phase under one outer deadline."""

    started = clock() if invocation_started is None else invocation_started
    deadline = min(started + scientific_seconds, process_deadline)
    result_path = output_dir / "result.json"
    document = _initial_document(
        revision,
        manifest,
        runtime,
        workers=workers,
        scientific_seconds=scientific_seconds,
        external_seconds=external_seconds,
        grace_seconds=grace_seconds,
    )

    def record_elapsed() -> None:
        elapsed = clock() - started
        clocks = cast(dict[str, object], document["clocks"])
        clocks["scientific_seconds"] = elapsed
        clocks["process_seconds"] = elapsed

    document["error"] = "source replay has not completed"
    record_elapsed()
    publisher(result_path, document)
    if clock() >= deadline:
        document.update(
            {
                "status": "partial",
                "outcome": "incomplete",
                "scientific_decision": "unresolved",
                "phase": "timeout",
                "error": "scientific deadline reached before source replay",
            }
        )
        record_elapsed()
        publisher(result_path, document)
        return document

    source_started = clock()
    manifest_by_path = {row["path"]: row for row in manifest}
    source_digest = hashlib.sha256(source).hexdigest()
    t026_digest = hashlib.sha256(t026_source).hexdigest()
    _require(
        len(source) == SOURCE_BYTES
        and source_digest == SOURCE_SHA256
        and manifest_by_path.get(SOURCE_PATH, {}).get("sha256") == source_digest,
        "executed T-025 bytes differ from the pinned source manifest",
    )
    _require(
        t026_digest == T026_SHA256
        and manifest_by_path.get(T026_PATH, {}).get("sha256") == t026_digest,
        "executed T-026 bytes differ from the pinned source manifest",
    )
    t026 = load_t026_reference(t026_source)
    packet, source_record = load_packet_source(source)
    source_finished = clock()
    # The scientific deadline starts at parent invocation, before source binding and
    # replay. ``source_seconds`` names just the in-function byte replay/parsing slice;
    # ``scientific_seconds`` and ``process_seconds`` use the invocation clock.
    cast(dict[str, object], document["clocks"])["source_seconds"] = (
        source_finished - source_started
    )
    document["phase"] = "raw-sweep"
    document["error"] = "raw sweep is incomplete"
    record_elapsed()
    publisher(result_path, document)
    if clock() >= deadline:
        document.update(
            {
                "status": "partial",
                "outcome": "incomplete",
                "scientific_decision": "unresolved",
                "phase": "timeout",
                "error": "scientific deadline reached before raw sweep",
            }
        )
        record_elapsed()
        publisher(result_path, document)
        return document

    def raw_progress(
        completed: int,
        completed_directions: tuple[int, ...],
        observed: Fraction,
        argmin: int,
        witness: Point,
    ) -> None:
        # The complete direction set is not yet a global minimum until its argmin has
        # passed the independent exact membership/admissibility replay below. Every
        # completed direction is already atomically retained in ``raw-directions`` here.
        if completed == RAW_DIRECTIONS:
            return
        raw = cast(dict[str, object], document["raw"])
        raw.update(
            {
                "directions_completed": completed,
                "completed_directions": list(completed_directions),
                "observed_minimum_upper_bound": str(observed),
                "observed_argmin": argmin,
                "observed_witness": [str(witness[0]), str(witness[1])],
            }
        )
        record_elapsed()
        publisher(result_path, document)

    try:
        raw_result = raw_runner(
            packet,
            workers=workers,
            deadline=deadline,
            clock=clock,
            progress=raw_progress,
            log=output_dir / "raw-directions",
        )
        _require(
            raw_result.completed == RAW_DIRECTIONS,
            "raw runner returned an incomplete global minimum",
        )
        replayed_charge, witness_admissible = raw_witness_replay(packet, raw_result)
        _require(
            replayed_charge == raw_result.minimum,
            "raw argmin charge disagrees with exact membership replay",
        )
        _require(witness_admissible, "raw argmin witness is not physically admissible")
        raw = cast(dict[str, object], document["raw"])
        raw.update(
            {
                "directions_completed": raw_result.completed,
                "completed_directions": list(range(RAW_DIRECTIONS)),
                "observed_minimum_upper_bound": str(raw_result.minimum),
                "observed_argmin": raw_result.direction,
                "observed_witness": [
                    str(raw_result.witness[0]),
                    str(raw_result.witness[1]),
                ],
            }
        )
        raw["raw_minimum"] = str(raw_result.minimum)
        raw["comparison"] = raw_decision(raw_result.minimum)
        raw["witness_replay_charge"] = str(replayed_charge)
        raw["witness_admissible"] = witness_admissible
        raw["directions_sha256"] = _direction_digest(
            tuple(
                output_dir / "raw-directions" / f"{index}.json"
                for index in range(RAW_DIRECTIONS)
            )
        )
        record_elapsed()
        publisher(result_path, document)

        if raw_decision(raw_result.minimum) == "rejected":
            document.update(
                {
                    "status": "complete",
                    "outcome": "raw-threshold-rejected",
                    "scientific_decision": "rejected",
                    "phase": "complete",
                    "error": None,
                }
            )
            record_elapsed()
            _expired(deadline, clock, "before complete receipt publication")
            publisher(result_path, document)
            return document

        candidate = normalized_bytes(
            source_record,
            raw_result.minimum,
            source_revision=revision,
        )
        candidate_path = output_dir / "candidate.json"
        atomic_write_text(candidate_path, candidate.decode())
        candidate_sha = hashlib.sha256(candidate).hexdigest()
        normalized, normalized_source = load(candidate)
        _require(
            normalized_source.get("least_cell_charge") == "1",
            "normalized bytes do not declare least_cell_charge=1",
        )
        expected_budget = SOURCE_BUDGET / raw_result.minimum
        _require(
            normalized.total_budget == expected_budget and normalized.total_budget < 11,
            "normalized bytes do not serialize M/m < 11 exactly",
        )
        closed_form = [
            {"name": report.name, "detail": report.detail, "holds": report.holds}
            for report in closed_form_threshold_conditions(normalized)
        ]
        _require(
            all(cast(bool, row["holds"]) for row in closed_form),
            "normalized bytes fail a closed-form certificate condition",
        )
        document["normalized"] = {
            "path": "candidate.json",
            "sha256": candidate_sha,
            "alpha": str(1 / raw_result.minimum),
            "least_cell_charge": "1",
            "total_budget": str(normalized.total_budget),
            "closed_form_conditions": closed_form,
        }
        document["phase"] = "normalized-exact"
        document["error"] = "normalized exact route is incomplete"
        record_elapsed()
        publisher(result_path, document)
        _expired(deadline, clock, "before normalized exact route")

        def exact_progress(
            completed: int,
            completed_directions: tuple[int, ...],
            observed: Fraction,
            argmin: int,
            witness: Point,
        ) -> None:
            if completed == RAW_DIRECTIONS:
                return
            _routes(document)["exact"] = {
                "status": "partial",
                "source_sha256": candidate_sha,
                "directions_expected": RAW_DIRECTIONS,
                "directions_completed": completed,
                "completed_directions": list(completed_directions),
                "observed_minimum_upper_bound": str(observed),
                "argmin": argmin,
                "witness": [str(witness[0]), str(witness[1])],
            }
            record_elapsed()
            publisher(result_path, document)

        try:
            exact = exact_runner(
                normalized,
                workers=workers,
                deadline=deadline,
                clock=clock,
                progress=exact_progress,
                log=output_dir / "normalized-exact-directions",
            )
        except ExactReaderDisagreementError as error:
            _routes(document)["exact"] = {
                "status": "invalid",
                "source_sha256": candidate_sha,
                "directions_expected": RAW_DIRECTIONS,
                "directions_completed": error.completed,
                "completed_directions": list(error.completed_directions),
                "observed_minimum_upper_bound": str(error.minimum),
                "argmin": error.argmin,
                "witness": [str(error.witness[0]), str(error.witness[1])],
                "reader_disagreement": {
                    "direction": error.direction,
                    "dense": str(error.dense[0]),
                    "dense_witness": [
                        str(error.dense[1][0]),
                        str(error.dense[1][1]),
                    ],
                    "slab": str(error.slab[0]),
                    "slab_witness": [
                        str(error.slab[1][0]),
                        str(error.slab[1][1]),
                    ],
                },
            }
            document.update(
                {
                    "status": "invalid",
                    "outcome": "reader-disagreement",
                    "scientific_decision": "unresolved",
                    "phase": "invalid",
                    "error": str(error),
                }
            )
            record_elapsed()
            publisher(result_path, document)
            return document
        if exact.completed != RAW_DIRECTIONS:
            exact_checkpoint = _routes(document)["exact"]
            _require(
                isinstance(exact_checkpoint, dict)
                and exact_checkpoint.get("status") == "partial"
                and exact_checkpoint.get("directions_completed") == exact.completed
                and exact_checkpoint.get("observed_minimum_upper_bound") == str(exact.minimum)
                and exact_checkpoint.get("argmin") == exact.direction
                and exact_checkpoint.get("witness")
                == [str(exact.witness[0]), str(exact.witness[1])],
                "incomplete exact runner did not publish its exact completed direction set",
            )
            document.update(
                {
                    "status": "partial",
                    "outcome": "incomplete",
                    "scientific_decision": "unresolved",
                    "phase": "incomplete",
                    "error": "normalized exact route was incomplete",
                }
            )
            record_elapsed()
            publisher(result_path, document)
            return document
        _routes(document)["exact"] = {
            "status": "complete",
            "source_sha256": candidate_sha,
            "directions_expected": RAW_DIRECTIONS,
            "directions_completed": exact.completed,
            "completed_directions": list(range(RAW_DIRECTIONS)),
            "minimum": str(exact.minimum),
            "argmin": exact.direction,
            "witness": [str(exact.witness[0]), str(exact.witness[1])],
            "dense_slab_disagreements": exact.disagreements,
            "directions_sha256": _direction_digest(
                tuple(
                    output_dir / "normalized-exact-directions" / f"{index}.json"
                    for index in range(RAW_DIRECTIONS)
                )
            ),
        }
        if exact.disagreements:
            document.update(
                {
                    "status": "invalid",
                    "outcome": "reader-disagreement",
                    "scientific_decision": "unresolved",
                    "phase": "invalid",
                    "error": "normalized exact route disagreed internally",
                }
            )
            record_elapsed()
            publisher(result_path, document)
            return document
        document["phase"] = "reflected-interval"
        document["error"] = "reflected interval route is incomplete"
        record_elapsed()
        publisher(result_path, document)
        _expired(deadline, clock, "before reflected interval route")

        interval_labels = tuple(str(index) for index in range(PACKET_STEPS + 1)) + tuple(
            f"{index}'" for index in range(1, PACKET_STEPS + 1)
        )
        interval_label_positions = {label: index for index, label in enumerate(interval_labels)}
        interval_completed_labels: set[str] = set()

        def interval_progress(outcome: DirectionOutcome) -> None:
            _require(
                outcome.label in interval_label_positions,
                "interval progress named an unknown direction",
            )
            _require(
                outcome.label not in interval_completed_labels,
                "interval progress repeated a completed direction",
            )
            interval_completed_labels.add(outcome.label)
            _routes(document)["reflected_interval"] = {
                "status": "partial",
                "source_sha256": candidate_sha,
                "directions_expected": INTERVAL_DIRECTIONS,
                "directions_completed": len(interval_completed_labels),
                "completed_directions": sorted(
                    interval_completed_labels, key=interval_label_positions.__getitem__
                ),
                "last": _interval_row(outcome),
            }
            record_elapsed()
            publisher(result_path, document)

        interval = interval_runner(
            normalized,
            workers=workers,
            deadline=deadline,
            clock=clock,
            progress=interval_progress,
            log=output_dir / "normalized-interval-directions",
        )
        if interval.completed != INTERVAL_DIRECTIONS:
            document.update(
                {
                    "status": "partial",
                    "outcome": "incomplete",
                    "scientific_decision": "unresolved",
                    "phase": "incomplete",
                    "error": "reflected interval route was incomplete",
                }
            )
            record_elapsed()
            publisher(result_path, document)
            return document
        _routes(document)["reflected_interval"] = {
            "status": "complete",
            "source_sha256": candidate_sha,
            "directions_expected": INTERVAL_DIRECTIONS,
            "directions_completed": interval.completed,
            "enclosure": [str(interval.lower), str(interval.upper)],
            "stalled": interval.stalled,
            "budget_exhausted": interval.budget_exhausted,
            "accepted": interval.accepted,
            "directions_sha256": _direction_digest(
                tuple(
                    output_dir / "normalized-interval-directions" / f"{label}.json"
                    for label in interval_labels
                )
            ),
        }

        invalid_problem = None
        incomplete_problem = None
        if interval.stalled or interval.budget_exhausted:
            incomplete_problem = "reflected interval route did not certify every direction"
        elif interval.lower != interval.upper:
            incomplete_problem = "reflected interval route returned a nonzero-width enclosure"
        elif exact.minimum != interval.lower or exact.minimum != 1 or not interval.accepted:
            invalid_problem = "normalized exact and interval routes do not both report one"
        if incomplete_problem is not None:
            document.update(
                {
                    "status": "partial",
                    "outcome": "incomplete",
                    "scientific_decision": "unresolved",
                    "phase": "incomplete",
                    "error": incomplete_problem,
                }
            )
            record_elapsed()
            publisher(result_path, document)
            return document
        if invalid_problem is not None:
            document.update(
                {
                    "status": "invalid",
                    "outcome": "reader-disagreement",
                    "scientific_decision": "unresolved",
                    "phase": "invalid",
                    "error": invalid_problem,
                }
            )
            record_elapsed()
            publisher(result_path, document)
            return document

        _require(
            candidate_path.read_bytes() == candidate,
            "normalized candidate changed before dilation replay",
        )
        document["phase"] = "dilation-replay"
        document["error"] = "dilation replay is incomplete"
        record_elapsed()
        publisher(result_path, document)
        _expired(deadline, clock, "before dilation replay")
        dilation_labels = tuple(direction.label for direction in normalized.directions)
        dilation_label_positions = {label: index for index, label in enumerate(dilation_labels)}
        _require(
            len(dilation_label_positions) == len(dilation_labels),
            "dilation direction labels are not unique",
        )
        dilation_completed_labels: set[str] = set()

        def dilation_progress(index: int, minimum: Fraction, label: str) -> None:
            _require(
                0 <= index < len(dilation_labels) and dilation_labels[index] == label,
                "dilation progress named the wrong direction",
            )
            _require(
                label not in dilation_completed_labels,
                "dilation progress repeated a completed direction",
            )
            dilation_completed_labels.add(label)
            row: dict[str, object] = {
                "direction": index,
                "label": label,
                "minimum": str(minimum),
            }
            _write_direction(output_dir / "dilation-directions", index, row)
            _routes(document)["dilation"] = {
                "status": "partial",
                "source_sha256": candidate_sha,
                "directions_expected": RAW_DIRECTIONS,
                "directions_completed": len(dilation_completed_labels),
                "completed_directions": sorted(
                    dilation_completed_labels, key=dilation_label_positions.__getitem__
                ),
                "last": row,
            }
            record_elapsed()
            publisher(result_path, document)
            _expired(deadline, clock, "during dilation replay")

        dilation = dilation_runner(
            candidate_path,
            workers=workers,
            deadline=deadline,
            clock=clock,
            progress=dilation_progress,
        )
        _require(
            candidate_path.read_bytes() == candidate,
            "normalized candidate changed during dilation replay",
        )
        dilation_source = cast(dict[str, object], dilation.get("source"))
        conclusion = cast(dict[str, object], dilation.get("conclusion"))
        _require(
            dilation_source.get("sha256") == candidate_sha,
            "dilation replay names different normalized bytes",
        )
        old_conclusion = cast(dict[str, object], t026.get("conclusion"))
        new_squared = Fraction(cast(str, conclusion.get("bounded_side_squared")))
        old_squared = Fraction(cast(str, old_conclusion.get("bounded_side_squared")))
        _require(
            new_squared > old_squared,
            "dilation replay does not exceed the T-026 lower bound",
        )
        dilation_bytes = (json.dumps(dilation, indent=2, allow_nan=False) + "\n").encode()
        _routes(document)["dilation"] = {
            "status": "complete",
            "source_sha256": candidate_sha,
            "directions_expected": RAW_DIRECTIONS,
            "directions_completed": RAW_DIRECTIONS,
            "directions_sha256": _direction_digest(
                tuple(
                    output_dir / "dilation-directions" / f"{index}.json"
                    for index in range(RAW_DIRECTIONS)
                )
            ),
            "record_sha256": hashlib.sha256(dilation_bytes).hexdigest(),
            "bounded_side": conclusion.get("bounded_side"),
            "bounded_side_squared": str(new_squared),
            "strictly_above_t026": True,
        }
        atomic_write_text(output_dir / "dilation.json", dilation_bytes.decode())
        _expired(deadline, clock, "before final byte checks")
        _require(
            candidate_path.read_bytes() == candidate,
            "normalized candidate changed before final publication",
        )
        document.update(
            {
                "status": "complete",
                "outcome": "packet-accepted",
                "scientific_decision": "accepted",
                "phase": "complete",
                "error": None,
            }
        )
        record_elapsed()
        _expired(deadline, clock, "before complete receipt publication")
        publisher(result_path, document)
        return document  # noqa: TRY300 -- the two exception classes publish distinct receipts
    except PacketDeadlineError as error:
        document.update(
            {
                "status": "partial",
                "outcome": "incomplete",
                "scientific_decision": "unresolved",
                "phase": "timeout",
                "error": str(error),
            }
        )
        record_elapsed()
        publisher(result_path, document)
        return document
    except (PacketError, OSError, ValueError, TypeError) as error:
        document.update(
            {
                "status": "invalid",
                "outcome": "invalid",
                "scientific_decision": "unresolved",
                "phase": "invalid",
                "error": str(error),
            }
        )
        record_elapsed()
        publisher(result_path, document)
        return document


def _strict_json(path: Path) -> dict[str, object]:
    try:
        data = path.read_bytes()
    except OSError as error:
        raise PacketError(f"could not read {path}: {error}") from error
    return _strict_json_bytes(data, str(path))


def _strict_json_bytes(data: bytes, label: str) -> dict[str, object]:
    def unique(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise PacketError(f"duplicate JSON key {key!r}")
            result[key] = value
        return result

    def reject_nonstandard_constant(value: str) -> object:
        raise PacketError(f"nonstandard JSON constant {value!r}")

    try:
        value = json.loads(
            data,
            object_pairs_hook=unique,
            parse_constant=reject_nonstandard_constant,
        )
    except (OSError, UnicodeError, ValueError) as error:
        raise PacketError(f"could not read {label}: {error}") from error
    if not isinstance(value, dict):
        raise PacketError(f"{label} is not a JSON object")
    return cast(dict[str, object], value)


def _canonical_rational(value: object, label: str) -> Fraction:
    rational = _exact_rational(value, label)
    if value != str(rational):
        raise PacketError(f"{label} is not in canonical exact form")
    return rational


def _canonical_point(value: object, label: str) -> Point:
    point = _exact_point(value, label)
    if value != [str(point[0]), str(point[1])]:
        raise PacketError(f"{label} is not in canonical exact form")
    return point


def _direction_files(directory: Path, *, allowed_labels: Collection[str]) -> dict[str, Path]:
    """Return the flat retained JSON set, rejecting every other directory entry."""

    if not directory.exists():
        return {}
    if not directory.is_dir() or directory.is_symlink():
        raise PacketError(f"retained direction path is not a directory: {directory}")
    files: dict[str, Path] = {}
    try:
        entries = tuple(directory.iterdir())
    except OSError as error:
        raise PacketError(
            f"could not list retained directions in {directory}: {error}"
        ) from error
    for path in entries:
        if path.is_symlink() or not path.is_file():
            raise PacketError(f"unexpected retained direction entry: {path}")
        if path.name.endswith(".partial"):
            temporary = path.name[: -len(".partial")]
            uid = temporary[-STRIF_ATOMIC_UID_LENGTH:]
            final_name = temporary[:-STRIF_ATOMIC_UID_LENGTH]
            final_path = Path(final_name)
            label = final_path.stem
            if (
                len(uid) == STRIF_ATOMIC_UID_LENGTH
                and all(
                    character in "0123456789abcdefghijklmnopqrstuvwxyz" for character in uid
                )
                and final_path.name == final_name
                and final_path.suffix == ".json"
                and final_name == f"{label}.json"
                and label in allowed_labels
            ):
                continue
            raise PacketError(f"unexpected retained direction entry: {path}")
        if path.suffix != ".json":
            raise PacketError(f"unexpected retained direction entry: {path}")
        label = path.stem
        if not label or label not in allowed_labels or label in files:
            raise PacketError(f"duplicate or empty retained direction filename: {path.name}")
        files[label] = path
    return files


def _indexed_direction_files(
    directory: Path,
    *,
    expected: int,
    reported: int,
    completed_directions: object,
    complete: bool,
) -> tuple[tuple[Path, ...], tuple[Path, ...]]:
    completed_indices = _completed_direction_indices(
        completed_directions,
        completed=reported,
        expected=expected,
        label="retained completed directions",
    )
    files = _direction_files(
        directory, allowed_labels={str(index) for index in range(expected)}
    )
    indexed: dict[int, Path] = {}
    for label, path in files.items():
        try:
            index = int(label)
        except ValueError as error:
            raise PacketError(f"unexpected indexed direction filename: {path.name}") from error
        if str(index) != label or not 0 <= index < expected:
            raise PacketError(f"unexpected indexed direction filename: {path.name}")
        indexed[index] = path
    actual = set(indexed)
    if complete:
        wanted = set(range(expected))
        if actual != wanted or completed_indices != tuple(range(expected)):
            raise PacketError("complete direction record has missing or extra filenames")
    if not set(completed_indices).issubset(actual):
        raise PacketError("receipt reports indexed directions that were not retained")
    return (
        tuple(indexed[index] for index in sorted(indexed)),
        tuple(indexed[index] for index in completed_indices),
    )


def _raw_row(path: Path, expected_direction: int) -> tuple[Fraction, Point]:
    row = _strict_json(path)
    if set(row) != {"direction", "charge", "witness"}:
        raise PacketError(f"raw direction row has the wrong schema: {path}")
    if type(row.get("direction")) is not int or row["direction"] != expected_direction:
        raise PacketError(f"raw direction row has the wrong label: {path}")
    return (
        _canonical_rational(row.get("charge"), f"raw charge in {path.name}"),
        _canonical_point(row.get("witness"), f"raw witness in {path.name}"),
    )


def _stable_minimum(rows: Sequence[tuple[int, Fraction, Point]]) -> RawMinimum | None:
    minimum: Fraction | None = None
    direction = -1
    witness: Point | None = None
    for index, charge, point in rows:
        if minimum is None or charge < minimum or (charge == minimum and index < direction):
            minimum, direction, witness = charge, index, point
    if minimum is None or witness is None:
        return None
    return RawMinimum(minimum, direction, witness, len(rows))


def _reconstruct_raw_directions(
    directory: Path,
    receipt: dict[str, object],
    *,
    expected: int,
    complete: bool,
) -> RawMinimum | None:
    reported = cast(int, receipt["directions_completed"])
    paths, reported_paths = _indexed_direction_files(
        directory,
        expected=expected,
        reported=reported,
        completed_directions=receipt.get("completed_directions"),
        complete=complete,
    )
    for path in paths:
        _raw_row(path, int(path.stem))
    reported_rows = tuple(
        (int(path.stem), *_raw_row(path, int(path.stem))) for path in reported_paths
    )
    observed = _stable_minimum(reported_rows)
    if reported == 0:
        return None
    if observed is None:
        raise PacketError("raw receipt has no reconstructible retained prefix")
    if (
        _exact_rational(receipt.get("observed_minimum_upper_bound"), "raw receipt minimum")
        != observed.minimum
        or receipt.get("observed_argmin") != observed.direction
        or _exact_point(receipt.get("observed_witness"), "raw receipt witness")
        != observed.witness
    ):
        raise PacketError("raw retained directions disagree with the receipt")
    if complete and receipt.get("directions_sha256") != _direction_digest(paths):
        raise PacketError("raw retained-direction digest differs from the receipt")
    if receipt.get("raw_minimum") is not None and (
        _exact_rational(receipt.get("raw_minimum"), "raw receipt global minimum")
        != observed.minimum
    ):
        raise PacketError("raw retained minimum disagrees with the receipt")
    return observed


def _exact_row(
    path: Path, expected_direction: int
) -> tuple[tuple[Fraction, Point], tuple[Fraction, Point]]:
    row = _strict_json(path)
    if set(row) != {
        "direction",
        "dense",
        "slab",
        "agree",
        "witness",
        "slab_witness",
    }:
        raise PacketError(f"normalized exact direction row has the wrong schema: {path}")
    if type(row.get("direction")) is not int or row["direction"] != expected_direction:
        raise PacketError(f"normalized exact direction row has the wrong label: {path}")
    if type(row.get("agree")) is not bool:
        raise PacketError(f"normalized exact agreement flag is malformed: {path}")
    dense = (
        _canonical_rational(row.get("dense"), f"dense charge in {path.name}"),
        _canonical_point(row.get("witness"), f"dense witness in {path.name}"),
    )
    slab = (
        _canonical_rational(row.get("slab"), f"slab charge in {path.name}"),
        _canonical_point(row.get("slab_witness"), f"slab witness in {path.name}"),
    )
    if row["agree"] is not (dense == slab):
        raise PacketError(f"normalized exact agreement flag disagrees with its row: {path}")
    return dense, slab


def _reconstruct_exact_directions(
    directory: Path,
    receipt: dict[str, object] | None,
    *,
    expected: int,
    complete: bool,
) -> ExactRoute | None:
    reported = 0 if receipt is None else cast(int, receipt["directions_completed"])
    completed_directions: object = (
        [] if receipt is None else receipt.get("completed_directions")
    )
    paths, reported_paths = _indexed_direction_files(
        directory,
        expected=expected,
        reported=reported,
        completed_directions=completed_directions,
        complete=complete,
    )
    for path in paths:
        _exact_row(path, int(path.stem))
    reported_rows = tuple(
        (int(path.stem), *_exact_row(path, int(path.stem))) for path in reported_paths
    )
    minimum = _stable_minimum(
        tuple((index, dense[0], dense[1]) for index, dense, _slab in reported_rows)
    )
    disagreements = sum(dense != slab for _index, dense, slab in reported_rows)
    if receipt is None or reported == 0:
        return None
    if minimum is None:
        raise PacketError("exact receipt has no reconstructible retained prefix")
    receipt_minimum = receipt.get(
        "minimum" if receipt.get("status") == "complete" else "observed_minimum_upper_bound"
    )
    if (
        _exact_rational(receipt_minimum, "exact receipt minimum") != minimum.minimum
        or receipt.get("argmin") != minimum.direction
        or _exact_point(receipt.get("witness"), "exact receipt witness") != minimum.witness
    ):
        raise PacketError("normalized exact retained directions disagree with the receipt")
    if receipt.get("status") == "invalid":
        first = next(
            ((index, dense, slab) for index, dense, slab in reported_rows if dense != slab),
            None,
        )
        if first is None:
            raise PacketError("exact invalid route has no retained reader disagreement")
        direction, dense, slab = first
        disagreement = cast(dict[str, object], receipt["reader_disagreement"])
        if disagreement != {
            "direction": direction,
            "dense": str(dense[0]),
            "dense_witness": [str(dense[1][0]), str(dense[1][1])],
            "slab": str(slab[0]),
            "slab_witness": [str(slab[1][0]), str(slab[1][1])],
        }:
            raise PacketError("exact retained disagreement differs from the receipt")
    if (
        receipt.get("status") == "complete"
        and receipt.get("dense_slab_disagreements") != disagreements
    ):
        raise PacketError("normalized exact disagreement count differs on readback")
    if complete and receipt.get("directions_sha256") != _direction_digest(paths):
        raise PacketError("normalized exact retained-direction digest differs from the receipt")
    return ExactRoute(
        minimum.minimum,
        minimum.direction,
        minimum.witness,
        reported,
        disagreements,
    )


def _interval_row_readback(
    row: dict[str, object], expected_label: str, source: str
) -> DirectionOutcome:
    if set(row) != {
        "label",
        "status",
        "lower",
        "upper",
        "witness",
        "boxes",
        "stalled",
        "budget_exhausted",
    }:
        raise PacketError(f"interval direction row has the wrong schema: {source}")
    if row.get("label") != expected_label:
        raise PacketError(f"interval direction row has the wrong label: {source}")
    status = row.get("status")
    if status not in ("certified", "refuted", "undecided"):
        raise PacketError(f"interval direction status is malformed: {source}")

    def optional_integer(value: object, label: str) -> int | None:
        if value is None:
            return None
        if type(value) is not int:
            raise PacketError(f"{label} is malformed: {source}")
        return cast(int, value)

    lower = optional_integer(row.get("lower"), "interval lower bound")
    upper = optional_integer(row.get("upper"), "interval upper bound")
    if lower is not None and upper is not None and lower > upper:
        raise PacketError(f"interval enclosure is reversed: {source}")
    witness_value = row.get("witness")
    witness: tuple[float, float] | None = None
    if witness_value is not None:
        if (
            not isinstance(witness_value, list)
            or len(witness_value) != 2
            or any(type(value) not in (int, float) for value in witness_value)
            or any(not math.isfinite(float(value)) for value in witness_value)
        ):
            raise PacketError(f"interval witness is malformed: {source}")
        witness = (float(witness_value[0]), float(witness_value[1]))
    boxes = row.get("boxes")
    stalled = row.get("stalled")
    budget_exhausted = row.get("budget_exhausted")
    if type(boxes) is not int or cast(int, boxes) < 0:
        raise PacketError(f"interval box count is malformed: {source}")
    if type(stalled) is not int or not 0 <= cast(int, stalled) <= cast(int, boxes):
        raise PacketError(f"interval stall count is malformed: {source}")
    if type(budget_exhausted) is not bool:
        raise PacketError(f"interval budget flag is malformed: {source}")
    return DirectionOutcome(
        expected_label,
        cast(Literal["certified", "refuted", "undecided"], status),
        lower,
        upper,
        witness,
        cast(int, boxes),
        cast(int, stalled),
        cast(bool, budget_exhausted),
    )


def _reconstruct_interval_directions(
    directory: Path,
    receipt: dict[str, object] | None,
    *,
    labels: Sequence[str],
    scale: int,
    complete: bool,
) -> IntervalReadback | None:
    expected = set(labels)
    files = _direction_files(directory, allowed_labels=expected)
    actual = set(files)
    if not actual.issubset(expected):
        raise PacketError("interval direction record has unexpected filenames")
    if complete and actual != expected:
        raise PacketError("complete interval direction record has missing or extra filenames")
    reported = 0 if receipt is None else cast(int, receipt["directions_completed"])
    if len(actual) < reported:
        raise PacketError("receipt reports interval directions that were not retained")
    rows = {
        label: _interval_row_readback(_strict_json(path), label, str(path))
        for label, path in files.items()
    }
    if receipt is None:
        return None
    if receipt.get("status") != "complete":
        completed_labels = _completed_direction_labels(
            receipt.get("completed_directions"),
            completed=reported,
            labels=labels,
            label="interval completed directions",
        )
        if not set(completed_labels).issubset(actual):
            raise PacketError("receipt reports interval directions that were not retained")
        last = cast(dict[str, object], receipt["last"])
        last_label = last.get("label")
        if not isinstance(last_label, str) or last_label not in completed_labels:
            raise PacketError("partial interval receipt does not name a published direction")
        _interval_row_readback(last, last_label, "partial interval receipt")
        if last != _strict_json(files[last_label]):
            raise PacketError("partial interval last row differs from retained bytes")
        return None
    ordered = tuple(rows[label] for label in labels)
    lows = [row.lower for row in ordered if row.lower is not None]
    highs = [row.upper for row in ordered if row.upper is not None]
    enclosure = (
        (Fraction(min(lows), scale), Fraction(min(highs), scale))
        if len(lows) == len(ordered) and highs
        else None
    )
    stalled = sum(row.stalled for row in ordered)
    budget_exhausted = sum(row.budget_exhausted for row in ordered)
    accepted = all(
        row.status == "certified" and row.lower is not None and row.lower >= scale
        for row in ordered
    )
    if enclosure is None:
        raise PacketError("complete interval directions do not reconstruct an enclosure")
    receipt_enclosure = cast(list[object], receipt["enclosure"])
    if (
        tuple(
            _exact_rational(value, f"interval receipt enclosure {index}")
            for index, value in enumerate(receipt_enclosure)
        )
        != enclosure
        or receipt.get("stalled") != stalled
        or receipt.get("budget_exhausted") != budget_exhausted
        or receipt.get("accepted") is not accepted
    ):
        raise PacketError("interval retained directions disagree with the receipt")
    if complete and receipt.get("directions_sha256") != _direction_digest(
        tuple(files[label] for label in labels)
    ):
        raise PacketError("interval retained-direction digest differs from the receipt")
    return IntervalReadback(
        enclosure,
        len(ordered),
        stalled,
        budget_exhausted,
        accepted,
    )


def _reconstruct_dilation_directions(
    directory: Path,
    receipt: dict[str, object] | None,
    *,
    labels: Sequence[str],
    complete: bool,
) -> None:
    files = _direction_files(
        directory, allowed_labels={str(index) for index in range(len(labels))}
    )
    indexed: dict[int, Path] = {}
    for label, path in files.items():
        try:
            index = int(label)
        except ValueError as error:
            raise PacketError(f"unexpected dilation direction filename: {path.name}") from error
        if str(index) != label or not 0 <= index < len(labels):
            raise PacketError(f"unexpected dilation direction filename: {path.name}")
        indexed[index] = path
    if complete and set(indexed) != set(range(len(labels))):
        raise PacketError("complete dilation record has missing or extra filenames")
    reported = 0 if receipt is None else cast(int, receipt["directions_completed"])
    if len(indexed) < reported:
        raise PacketError("receipt reports dilation directions that were not retained")

    rows: dict[int, dict[str, object]] = {}
    minima: list[Fraction] = []
    for index, path in indexed.items():
        row = _strict_json(path)
        if set(row) != {"direction", "label", "minimum"}:
            raise PacketError(f"dilation direction row has the wrong schema: {path}")
        if row.get("direction") != index or row.get("label") != labels[index]:
            raise PacketError(f"dilation direction row has the wrong identity: {path}")
        minima.append(
            _canonical_rational(row.get("minimum"), f"dilation minimum in {path.name}")
        )
        rows[index] = row
    if receipt is None:
        return
    if not complete:
        completed_labels = _completed_direction_labels(
            receipt.get("completed_directions"),
            completed=reported,
            labels=labels,
            label="dilation completed directions",
        )
        retained_labels = {cast(str, row["label"]) for row in rows.values()}
        if not set(completed_labels).issubset(retained_labels):
            raise PacketError("receipt reports dilation directions that were not retained")
        last = cast(dict[str, object], receipt["last"])
        last_index = last.get("direction")
        if type(last_index) is not int or last_index not in rows:
            raise PacketError("partial dilation receipt does not name a retained direction")
        if last.get("label") not in completed_labels:
            raise PacketError("partial dilation receipt does not name a published direction")
        if last != rows[cast(int, last_index)]:
            raise PacketError("partial dilation last row differs from retained bytes")
        return
    if not minima or min(minima) != 1:
        raise PacketError("complete dilation directions do not reconstruct minimum one")
    ordered = tuple(indexed[index] for index in range(len(labels)))
    if receipt.get("directions_sha256") != _direction_digest(ordered):
        raise PacketError("dilation retained-direction digest differs from the receipt")


def load_result(
    output_dir: Path,
    *,
    repository: Path,
    expected_revision: str,
    require_supervision: bool = True,
) -> dict[str, object]:
    """Independently bind a saved receipt to its source, revision and candidate bytes."""

    document = _strict_json(output_dir / "result.json")
    validate_result_document(document)
    if require_supervision:
        supervision = cast(dict[str, object], document["supervision"])
        if supervision["status"] == "pending":
            raise PacketError("result has not been attested by its parent supervisor")
        expected_exit = (
            0
            if document["status"] == "complete"
            else 2
            if document["status"] == "invalid"
            else 1
        )
        if (
            supervision["status"] == "observed-exit"
            and supervision["worker_exit_status"] != expected_exit
        ):
            raise PacketError("parent observation disagrees with the result classification")
        if supervision["status"] != "observed-exit" and document["status"] == "complete":
            raise PacketError("non-normal supervision cannot retain a complete result")
    sources = _source_record(document)
    if sources.get("implementation_revision") != expected_revision:
        raise PacketError("result revision differs from the requested readback revision")
    manifest = source_manifest(
        repository,
        expected_revision,
        result_directory=output_dir,
    )
    if sources.get("manifest") != manifest:
        raise PacketError("result source or implementation manifest differs on readback")
    if sources.get("runtime") != runtime_binding(repository):
        raise PacketError("result runtime differs from the readback environment")
    source = (repository / SOURCE_PATH).read_bytes()
    t026_source = (repository / T026_PATH).read_bytes()
    if (
        len(source) != SOURCE_BYTES
        or hashlib.sha256(source).hexdigest() != sources.get("source_sha256")
        or hashlib.sha256(t026_source).hexdigest() != sources.get("t026_sha256")
    ):
        raise PacketError("source bytes changed after readback manifest validation")
    t026 = load_t026_reference(t026_source)
    packet, source_record = load_packet_source(source)
    raw = cast(dict[str, object], document["raw"])
    raw_complete = raw.get("raw_minimum") is not None
    retained_raw = _reconstruct_raw_directions(
        output_dir / "raw-directions",
        raw,
        expected=len(packet.directions),
        complete=raw_complete,
    )
    rebuilt: ThresholdCertificate | None = None
    routes = _routes(document)
    candidate_path = output_dir / "candidate.json"
    if raw_complete:
        minimum = Fraction(cast(str, raw["raw_minimum"]))
        if raw.get("directions_completed") != len(packet.directions):
            raise PacketError("complete raw minimum lacks every fixed direction")
        if retained_raw is None:
            raise PacketError("complete raw result has no retained directions")
        raw_result = retained_raw
        replayed, admissible = replay_raw_witness(packet, raw_result)
        if replayed != minimum or not admissible:
            raise PacketError("raw argmin fails exact admissible readback replay")
        normalized = document["normalized"]
        if minimum > RAW_THRESHOLD:
            expected = normalized_bytes(
                source_record,
                minimum,
                source_revision=expected_revision,
            )
            if not isinstance(normalized, dict):
                if not _is_raw_normalization_checkpoint(document, routes):
                    raise PacketError("accepted raw minimum has no normalized-byte binding")
                if candidate_path.is_symlink() or (
                    candidate_path.exists() and not candidate_path.is_file()
                ):
                    raise PacketError("unpublished normalized candidate is not a regular file")
                if candidate_path.exists() and candidate_path.read_bytes() != expected:
                    raise PacketError(
                        "unpublished candidate differs from the strict raw derivation"
                    )
                normalized = None
            else:
                candidate = candidate_path.read_bytes()
                if candidate != expected or hashlib.sha256(
                    candidate
                ).hexdigest() != normalized.get("sha256"):
                    raise PacketError("normalized bytes differ from the strict raw derivation")
                rebuilt, rebuilt_record = load(candidate)
                conditions = closed_form_threshold_conditions(rebuilt)
                if (
                    rebuilt_record.get("least_cell_charge") != "1"
                    or rebuilt.total_budget != SOURCE_BUDGET / minimum
                    or rebuilt.total_budget >= 11
                    or not all(report.holds for report in conditions)
                ):
                    raise PacketError(
                        "normalized bytes fail exact scale or closed-form readback"
                    )
    if (
        document["normalized"] is None
        and raw.get("comparison") != "accepted"
        and (candidate_path.is_symlink() or candidate_path.exists())
    ):
        raise PacketError("normalized candidate exists before complete raw acceptance")
    exact_receipt = cast(dict[str, object] | None, routes["exact"])
    interval_receipt = cast(dict[str, object] | None, routes["reflected_interval"])
    dilation_receipt = cast(dict[str, object] | None, routes["dilation"])
    indexed_labels = {str(index) for index in range(len(packet.directions))}
    interval_source_labels = {
        *(str(index) for index in range(len(packet.half_tangents))),
        *(f"{index}'" for index in range(1, len(packet.half_tangents))),
    }
    if rebuilt is None:
        if (
            _direction_files(
                output_dir / "normalized-exact-directions",
                allowed_labels=indexed_labels,
            )
            or _direction_files(
                output_dir / "normalized-interval-directions",
                allowed_labels=interval_source_labels,
            )
            or _direction_files(
                output_dir / "dilation-directions",
                allowed_labels=indexed_labels,
            )
        ):
            raise PacketError("post-normalization directions exist without normalized bytes")
    else:
        exact_complete = exact_receipt is not None and exact_receipt.get("status") == "complete"
        _reconstruct_exact_directions(
            output_dir / "normalized-exact-directions",
            exact_receipt,
            expected=len(rebuilt.directions),
            complete=exact_complete,
        )
        interval_complete = (
            interval_receipt is not None and interval_receipt.get("status") == "complete"
        )
        interval_labels = tuple(
            str(index) for index in range(len(rebuilt.half_tangents))
        ) + tuple(f"{index}'" for index in range(1, len(rebuilt.half_tangents)))
        interval_scale = scaled_threshold_masses(rebuilt)[0]
        _reconstruct_interval_directions(
            output_dir / "normalized-interval-directions",
            interval_receipt,
            labels=interval_labels,
            scale=interval_scale,
            complete=interval_complete,
        )
        dilation_complete = (
            dilation_receipt is not None and dilation_receipt.get("status") == "complete"
        )
        _reconstruct_dilation_directions(
            output_dir / "dilation-directions",
            dilation_receipt,
            labels=tuple(direction.label for direction in rebuilt.directions),
            complete=dilation_complete,
        )
    if document["outcome"] == "packet-accepted":
        if rebuilt is None:
            raise PacketError("accepted receipt has no reconstructed normalized source")
        exact = cast(dict[str, object], routes["exact"])
        interval = cast(dict[str, object], routes["reflected_interval"])
        dilation = cast(dict[str, object], routes["dilation"])
        dilation_bytes = (output_dir / "dilation.json").read_bytes()
        dilation_document = _strict_json(output_dir / "dilation.json")
        _validate_dilation_readback(
            dilation_document,
            rebuilt,
            cast(str, cast(dict[str, object], document["normalized"])["sha256"]),
        )
        dilation_source = cast(dict[str, object], dilation_document.get("source"))
        dilation_conclusion = cast(dict[str, object], dilation_document.get("conclusion"))
        old_conclusion = cast(dict[str, object], t026.get("conclusion"))
        new_squared = Fraction(cast(str, dilation_conclusion.get("bounded_side_squared")))
        old_squared = Fraction(cast(str, old_conclusion.get("bounded_side_squared")))
        if (
            exact.get("directions_completed") != RAW_DIRECTIONS
            or exact.get("minimum") != "1"
            or exact.get("dense_slab_disagreements") != 0
            or interval.get("directions_completed") != INTERVAL_DIRECTIONS
            or interval.get("enclosure") != ["1", "1"]
            or interval.get("stalled") != 0
            or interval.get("budget_exhausted") != 0
            or interval.get("accepted") is not True
            or dilation.get("source_sha256")
            != cast(dict[str, object], document["normalized"]).get("sha256")
            or dilation.get("record_sha256") != hashlib.sha256(dilation_bytes).hexdigest()
            or dilation_source.get("sha256") != dilation.get("source_sha256")
            or dilation_conclusion.get("bounded_side") != dilation.get("bounded_side")
            or dilation_conclusion.get("bounded_side_squared")
            != dilation.get("bounded_side_squared")
            or new_squared <= old_squared
            or dilation.get("strictly_above_t026") is not True
        ):
            raise PacketError("accepted receipt does not bind all three retaining readers")
    return document


def prepare_output_dir(
    output_dir: Path, repository: Path, *, deadline: float | None = None
) -> Path:
    repository = repository.resolve()
    resolved = output_dir.resolve()
    if resolved.exists():
        raise PacketError("output directory must be fresh")
    git_directory = Path(
        _git(repository, "rev-parse", "--absolute-git-dir", deadline=deadline)
    ).resolve()
    common_text = _git(repository, "rev-parse", "--git-common-dir", deadline=deadline)
    common_directory = Path(common_text)
    if not common_directory.is_absolute():
        common_directory = repository / common_directory
    git_control_directories = {git_directory, common_directory.resolve()}
    if any(
        resolved == path or resolved.is_relative_to(path) for path in git_control_directories
    ):
        raise PacketError("output directory cannot be inside Git administrative data")
    protected = (
        repository / "packing" / "devtools",
        repository / "packing" / "src",
        repository / "packing" / "tests",
        repository / SOURCE_PATH,
        repository / T026_PATH,
    )
    if any(
        resolved == path.resolve() or resolved.is_relative_to(path.resolve())
        for path in protected
    ):
        raise PacketError("output directory cannot replace source, code, or tests")
    resolved.mkdir(parents=True)
    return resolved


def _supervision_receipt(path: Path) -> tuple[dict[str, object], bool]:
    document = _strict_json(path)
    if document.get("schema") == PREFLIGHT_SCHEMA:
        validate_preflight_document(document)
        return document, True
    validate_result_document(document)
    return document, False


def _record_external_timeout(
    path: Path,
    error: str,
    elapsed: float,
    *,
    worker_status: int | None = None,
    supervisor_signal: int | None = None,
    supervision_status: Literal[
        "deadline-before-launch",
        "deadline-terminated",
        "launch-failed",
        "supervisor-interrupted",
    ] = "deadline-terminated",
) -> None:
    """Record an outer kill without erasing a valid invalid-run classification."""

    try:
        document, preflight = _supervision_receipt(path)
    except PacketError:
        return
    if preflight:
        cast(dict[str, object], document["clocks"])["external_lifetime_seconds"] = elapsed
        cast(dict[str, object], document["supervision"]).update(
            {
                "status": supervision_status,
                "worker_exit_status": worker_status,
                "supervisor_signal": supervisor_signal,
            }
        )
        if document["status"] != "invalid":
            timeout = supervision_status in {
                "deadline-before-launch",
                "deadline-terminated",
            }
            document.update(
                {
                    "status": "partial",
                    "outcome": "preflight-timeout" if timeout else "preflight-failed",
                    "scientific_decision": "unresolved",
                    "phase": "preflight",
                    "error": error,
                }
            )
        write_result(path, document)
        return
    preserve_classification = document["status"] == "invalid" or (
        document["status"] == "partial"
        and document["phase"] == "timeout"
        and str(document["error"]).startswith("scientific deadline reached")
    )
    cast(dict[str, object], document["clocks"])["external_lifetime_seconds"] = elapsed
    cast(dict[str, object], document["supervision"]).update(
        {
            "status": supervision_status,
            "worker_exit_status": worker_status,
            "supervisor_signal": supervisor_signal,
        }
    )
    if preserve_classification:
        write_result(path, document)
        return
    document.update(
        {
            "status": "partial",
            "outcome": "incomplete",
            "scientific_decision": "unresolved",
            "phase": (
                "timeout"
                if supervision_status in {"deadline-before-launch", "deadline-terminated"}
                else "incomplete"
            ),
            "error": error,
        }
    )
    write_result(path, document)


def _record_worker_exit(path: Path, status: int, elapsed: float) -> None:
    """Attest a worker exit and preserve only classifications its exit supports."""

    try:
        document, preflight = _supervision_receipt(path)
    except PacketError:
        return
    cast(dict[str, object], document["clocks"])["external_lifetime_seconds"] = elapsed
    cast(dict[str, object], document["supervision"]).update(
        {
            "status": "observed-exit",
            "worker_exit_status": status,
            "supervisor_signal": None,
        }
    )
    if preflight:
        expected = 2 if document["status"] == "invalid" else 1
        if document["outcome"] == "preflight-pending" or status != expected:
            document.update(
                {
                    "status": "partial",
                    "outcome": "preflight-failed",
                    "scientific_decision": "unresolved",
                    "phase": "preflight",
                    "error": f"worker exited before completing preflight with status {status}",
                }
            )
        write_result(path, document)
        return
    expected = (
        0 if document["status"] == "complete" else 2 if document["status"] == "invalid" else 1
    )
    if document["status"] != "invalid" and status != expected:
        document.update(
            {
                "status": "partial",
                "outcome": "incomplete",
                "scientific_decision": "unresolved",
                "phase": "incomplete",
                "error": f"worker exited unexpectedly with status {status}",
            }
        )
    write_result(path, document)


def supervise_worker(  # noqa: PLR0911
    command: Sequence[str],
    result_path: Path,
    *,
    external_seconds: float,
    grace_seconds: float,
    invocation_started: float | None = None,
    external_deadline: float | None = None,
) -> int:
    """Own and reap the complete worker process group at the hard outer deadline."""

    started = time.perf_counter() if invocation_started is None else invocation_started
    deadline = started + external_seconds if external_deadline is None else external_deadline
    handled_signals = (signal.SIGTERM, signal.SIGHUP, signal.SIGINT)
    previous_mask = signal.pthread_sigmask(signal.SIG_BLOCK, handled_signals)
    previous_handlers: dict[signal.Signals, Any] = {}
    process: subprocess.Popen[bytes] | None = None
    interrupted_signal: int | None = None
    launching = False
    handling_interruption = False

    def handle_signal(signum: int, _frame: object) -> None:
        nonlocal interrupted_signal
        if interrupted_signal is not None:
            return
        interrupted_signal = signum
        # Deferral belongs in the handler: another eligible thread can receive a
        # process-directed signal while this thread masks it. Finish handle adoption
        # and cleanup before allowing a queued handler to unwind their owners.
        if not launching and not handling_interruption:
            raise _SupervisorSignal(signum)

    def raise_if_interrupted() -> None:
        if interrupted_signal is not None:
            raise _SupervisorSignal(interrupted_signal)

    def group_exists() -> bool:
        if process is None:
            return False
        try:
            os.killpg(process.pid, 0)
        except ProcessLookupError:
            return False
        return True

    def wait_for_group_absence() -> bool:
        group_deadline = time.perf_counter() + grace_seconds
        while group_exists():
            remaining_grace = group_deadline - time.perf_counter()
            if remaining_grace <= 0:
                return False
            time.sleep(min(0.01, remaining_grace))
        return True

    def reap_descendants_after_leader_exit() -> None:
        if process is None:
            return
        if not group_exists():
            return
        with suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGTERM)
        if wait_for_group_absence():
            return
        with suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGKILL)
        if not wait_for_group_absence():
            raise PacketError("worker process group remained alive after SIGKILL")

    def terminate_group() -> int | None:
        if process is None:
            return None
        with suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGTERM)
        worker_status: int | None = None
        with suppress(subprocess.TimeoutExpired):
            worker_status = process.wait(timeout=grace_seconds)
        # The leader may have exited while descendants remain. SIGKILL is therefore
        # sent to the session after every grace period; ESRCH means it is already gone.
        with suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGKILL)
        status = process.wait() if worker_status is None else worker_status
        if not wait_for_group_absence():
            raise PacketError("worker process group remained alive after SIGKILL")
        return status

    try:
        for signal_number in handled_signals:
            previous_handlers[signal_number] = signal.signal(signal_number, handle_signal)
        signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
        raise_if_interrupted()
        remaining = deadline - time.perf_counter()
        if remaining <= 0:
            _record_external_timeout(
                result_path,
                (
                    "worker process group exceeded the "
                    f"{external_seconds:g}-second external deadline before launch"
                ),
                time.perf_counter() - started,
                supervision_status="deadline-before-launch",
            )
            return 1

        launch_error: str | None = None
        launching = True
        try:
            process = subprocess.Popen(command, start_new_session=True)
        except OSError as error:
            launch_error = str(error)
        except Exception as error:  # noqa: BLE001 -- ordinary launch failures are operational
            launch_error = f"{type(error).__name__}: {error}"
        finally:
            launching = False
        raise_if_interrupted()
        if launch_error is not None:
            _record_external_timeout(
                result_path,
                f"worker process launch failed: {launch_error}",
                time.perf_counter() - started,
                supervision_status="launch-failed",
            )
            return 1
        if process is None:
            _record_external_timeout(
                result_path,
                "worker process launch returned no process handle",
                time.perf_counter() - started,
                supervision_status="launch-failed",
            )
            return 1

        remaining = deadline - time.perf_counter()
        if remaining <= 0:
            worker_status = terminate_group()
            _record_external_timeout(
                result_path,
                (
                    "worker process group exceeded the "
                    f"{external_seconds:g}-second external deadline"
                ),
                time.perf_counter() - started,
                worker_status=worker_status,
            )
            return 1
        try:
            status = process.wait(timeout=remaining)
            reap_descendants_after_leader_exit()
            _record_worker_exit(result_path, status, time.perf_counter() - started)
            return status  # noqa: TRY300 -- timeout has a process-group cleanup path
        except subprocess.TimeoutExpired:
            worker_status = terminate_group()
            _record_external_timeout(
                result_path,
                (
                    "worker process group exceeded the "
                    f"{external_seconds:g}-second external deadline"
                ),
                time.perf_counter() - started,
                worker_status=worker_status,
            )
            return 1
    except _SupervisorSignal as error:
        handling_interruption = True
        signal.pthread_sigmask(signal.SIG_BLOCK, handled_signals)
        worker_status = terminate_group()
        signal_number = signal.Signals(interrupted_signal or error.signum)
        _record_external_timeout(
            result_path,
            f"supervisor interrupted by {signal_number.name} ({signal_number.value})",
            time.perf_counter() - started,
            worker_status=worker_status,
            supervisor_signal=signal_number.value,
            supervision_status="supervisor-interrupted",
        )
        interrupted_signal = signal_number.value
    except BaseException as error:  # parent interruption must still reap the process group
        handling_interruption = True
        signal.pthread_sigmask(signal.SIG_BLOCK, handled_signals)
        worker_status = terminate_group()
        _record_external_timeout(
            result_path,
            f"supervisor interrupted by {type(error).__name__}",
            time.perf_counter() - started,
            worker_status=worker_status,
            supervision_status="supervisor-interrupted",
        )
        raise
    finally:
        signal.pthread_sigmask(signal.SIG_BLOCK, handled_signals)
        for signal_number, previous_handler in previous_handlers.items():
            signal.signal(signal_number, previous_handler)
        signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)

    if interrupted_signal is not None:
        signal.raise_signal(interrupted_signal)
        return 128 + interrupted_signal
    raise AssertionError("supervisor left its process state without an outcome")


def _record_worker_failure(
    path: Path,
    *,
    error: str,
    elapsed: float,
    invalid: bool,
) -> bool:
    """Retain a worker failure in whichever closed receipt schema is available."""

    try:
        document, preflight = _supervision_receipt(path)
    except PacketError:
        return False
    if preflight:
        document.update(
            {
                "status": "invalid" if invalid else "partial",
                "outcome": "preflight-invalid" if invalid else "preflight-failed",
                "scientific_decision": "unresolved",
                "phase": "preflight",
                "error": error,
            }
        )
        cast(dict[str, object], document["clocks"])["process_seconds"] = elapsed
    else:
        document.update(
            {
                "status": "invalid" if invalid else "partial",
                "outcome": "invalid" if invalid else "incomplete",
                "scientific_decision": "unresolved",
                "phase": "invalid" if invalid else "incomplete",
                "error": error,
            }
        )
        clocks = cast(dict[str, object], document["clocks"])
        clocks["scientific_seconds"] = elapsed
        clocks["process_seconds"] = elapsed
    write_result(path, document)
    return True


def run_worker(  # noqa: PLR0911
    repository: Path,
    revision: str,
    output_dir: Path,
    *,
    workers: int,
    scientific_seconds: float,
    external_seconds: float,
    grace_seconds: float,
    invocation_started: float | None = None,
    scientific_deadline: float | None = None,
    external_deadline: float | None = None,
) -> int:
    worker_started = time.perf_counter() if invocation_started is None else invocation_started
    scientific_deadline = (
        worker_started + scientific_seconds
        if scientific_deadline is None
        else scientific_deadline
    )
    external_deadline = (
        worker_started + external_seconds if external_deadline is None else external_deadline
    )
    try:
        manifest = source_manifest(
            repository,
            revision,
            result_directory=output_dir,
        )
        runtime = runtime_binding(repository)
        source = (repository / SOURCE_PATH).read_bytes()
        t026 = (repository / T026_PATH).read_bytes()
    except PacketError as error:
        elapsed = time.perf_counter() - worker_started
        _record_worker_failure(
            output_dir / "result.json",
            error=str(error),
            elapsed=elapsed,
            invalid=True,
        )
        return 2
    except Exception as error:  # noqa: BLE001 -- preflight host failures are unresolved
        elapsed = time.perf_counter() - worker_started
        _record_worker_failure(
            output_dir / "result.json",
            error=f"operational preflight failure: {type(error).__name__}: {error}",
            elapsed=elapsed,
            invalid=False,
        )
        return 1
    try:
        document = execute_packet(
            source,
            t026,
            revision=revision,
            manifest=manifest,
            runtime=runtime,
            output_dir=output_dir,
            workers=workers,
            scientific_seconds=scientific_seconds,
            external_seconds=external_seconds,
            grace_seconds=grace_seconds,
            process_deadline=min(scientific_deadline, external_deadline),
            invocation_started=worker_started,
        )
    except PacketError as error:
        elapsed = time.perf_counter() - worker_started
        _record_worker_failure(
            output_dir / "result.json",
            error=str(error),
            elapsed=elapsed,
            invalid=True,
        )
        return 2
    except Exception as error:  # noqa: BLE001 -- operational failures retain partial evidence
        elapsed = time.perf_counter() - worker_started
        _record_worker_failure(
            output_dir / "result.json",
            error=f"unexpected worker failure: {type(error).__name__}: {error}",
            elapsed=elapsed,
            invalid=False,
        )
        return 1
    if document["status"] == "complete":
        try:
            load_result(
                output_dir,
                repository=repository,
                expected_revision=revision,
                require_supervision=False,
            )
        except Exception as error:  # noqa: BLE001 -- every failed mandatory reader is retained
            document.update(
                {
                    "status": "invalid",
                    "outcome": "invalid",
                    "scientific_decision": "unresolved",
                    "phase": "invalid",
                    "error": f"independent readback refused: {error}",
                }
            )
            clocks = cast(dict[str, object], document["clocks"])
            elapsed = time.perf_counter() - worker_started
            clocks["scientific_seconds"] = elapsed
            clocks["process_seconds"] = elapsed
            write_result(output_dir / "result.json", document)
            return 2
        clocks = cast(dict[str, object], document["clocks"])
        finished = time.perf_counter()
        elapsed = finished - worker_started
        clocks["scientific_seconds"] = elapsed
        clocks["process_seconds"] = elapsed
        if finished >= scientific_deadline:
            document.update(
                {
                    "status": "partial",
                    "outcome": "incomplete",
                    "scientific_decision": "unresolved",
                    "phase": "timeout",
                    "error": (
                        "scientific deadline reached during final publication and "
                        "independent readback"
                    ),
                }
            )
        write_result(output_dir / "result.json", document)
        if document["status"] == "complete":
            published = time.perf_counter()
            if published >= scientific_deadline:
                # The embedded clock precedes its own atomic publication. Supervision
                # remains pending until this post-publication check permits success.
                document.update(
                    {
                        "status": "partial",
                        "outcome": "incomplete",
                        "scientific_decision": "unresolved",
                        "phase": "timeout",
                        "error": "scientific deadline reached during final receipt publication",
                    }
                )
                elapsed = published - worker_started
                clocks["scientific_seconds"] = elapsed
                clocks["process_seconds"] = elapsed
                write_result(output_dir / "result.json", document)
    else:
        clocks = cast(dict[str, object], document["clocks"])
        elapsed = time.perf_counter() - worker_started
        clocks["scientific_seconds"] = elapsed
        clocks["process_seconds"] = elapsed
        write_result(output_dir / "result.json", document)
    if document["status"] == "invalid":
        return 2
    return 0 if document["status"] == "complete" else 1


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--expect-implementation-revision", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--scientific-seconds", type=float, required=True)
    parser.add_argument("--external-seconds", type=float, required=True)
    parser.add_argument("--grace-seconds", type=float, default=DEFAULT_GRACE_SECONDS)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--invocation-started-monotonic", type=float, help=argparse.SUPPRESS)
    parser.add_argument("--scientific-deadline-monotonic", type=float, help=argparse.SUPPRESS)
    parser.add_argument("--external-deadline-monotonic", type=float, help=argparse.SUPPRESS)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    invocation_started = time.perf_counter()
    options = _parser().parse_args(argv)
    repository = options.repository.resolve()
    revision = cast(str, options.expect_implementation_revision)
    if len(revision) != 40 or any(c not in "0123456789abcdef" for c in revision):
        raise PacketError("expected revision must be 40 lowercase hexadecimal digits")
    if not 1 <= options.workers <= MAX_WORKERS:
        raise PacketError(f"workers must be between 1 and {MAX_WORKERS}")
    if not all(
        math.isfinite(value)
        for value in (
            options.scientific_seconds,
            options.external_seconds,
            options.grace_seconds,
        )
    ):
        raise PacketError("deadlines and termination grace must be finite")
    if not 0 < options.scientific_seconds <= options.external_seconds:
        raise PacketError(
            "scientific deadline must be positive and within the external deadline"
        )
    if options.grace_seconds <= 0:
        raise PacketError("termination grace must be positive")
    if options.worker:
        inherited = (
            options.invocation_started_monotonic,
            options.scientific_deadline_monotonic,
            options.external_deadline_monotonic,
        )
        if any(value is None or not math.isfinite(value) for value in inherited):
            raise PacketError("worker requires finite parent deadline attestation")
        inherited_started = cast(float, options.invocation_started_monotonic)
        inherited_scientific = cast(float, options.scientific_deadline_monotonic)
        inherited_external = cast(float, options.external_deadline_monotonic)
        if (
            inherited_scientific != inherited_started + options.scientific_seconds
            or inherited_external != inherited_started + options.external_seconds
        ):
            raise PacketError("worker deadlines differ from the parent invocation clock")
        return run_worker(
            repository,
            revision,
            options.output_dir.resolve(),
            workers=options.workers,
            scientific_seconds=options.scientific_seconds,
            external_seconds=options.external_seconds,
            grace_seconds=options.grace_seconds,
            invocation_started=inherited_started,
            scientific_deadline=inherited_scientific,
            external_deadline=inherited_external,
        )
    if any(
        value is not None
        for value in (
            options.invocation_started_monotonic,
            options.scientific_deadline_monotonic,
            options.external_deadline_monotonic,
        )
    ):
        raise PacketError("parent-only invocation cannot accept inherited deadline fields")
    scientific_deadline = invocation_started + options.scientific_seconds
    external_deadline = invocation_started + options.external_seconds
    output = prepare_output_dir(options.output_dir, repository, deadline=external_deadline)
    seed = initial_preflight_document(
        revision,
        workers=options.workers,
        scientific_seconds=options.scientific_seconds,
        external_seconds=options.external_seconds,
        grace_seconds=options.grace_seconds,
    )
    write_result(output / "result.json", seed)
    command = [
        sys.executable,
        "-m",
        "devtools.fixed_core_packet",
        "--worker",
        "--repository",
        str(repository),
        "--expect-implementation-revision",
        revision,
        "--output-dir",
        str(output),
        "--workers",
        str(options.workers),
        "--scientific-seconds",
        str(options.scientific_seconds),
        "--external-seconds",
        str(options.external_seconds),
        "--grace-seconds",
        str(options.grace_seconds),
        "--invocation-started-monotonic",
        repr(invocation_started),
        "--scientific-deadline-monotonic",
        repr(scientific_deadline),
        "--external-deadline-monotonic",
        repr(external_deadline),
    ]
    return supervise_worker(
        command,
        output / "result.json",
        external_seconds=options.external_seconds,
        grace_seconds=options.grace_seconds,
        invocation_started=invocation_started,
        external_deadline=external_deadline,
    )


__all__ = [
    "PREFLIGHT_SCHEMA",
    "ExactRoute",
    "IntervalRoute",
    "PackageRuntimeObservation",
    "PacketDeadlineError",
    "PacketError",
    "PacketOperationalError",
    "RawMinimum",
    "RuntimeObservation",
    "discover_implementation_paths",
    "execute_packet",
    "initial_preflight_document",
    "load_packet_source",
    "load_result",
    "load_t026_reference",
    "normalized_bytes",
    "normalized_record",
    "prepare_output_dir",
    "raw_decision",
    "runtime_binding",
    "source_manifest",
    "supervise_worker",
    "validate_preflight_document",
    "validate_result_document",
]


if __name__ == "__main__":
    raise SystemExit(main())
