#!/usr/bin/env python3
"""Exercise the fixed-core packet machinery on one frozen known-answer fixture.

The outer receipt is calibration evidence only.  The normalized candidate and dilation
record inside the output are ordinary generic threshold-certificate artifacts for the
``n=2`` fixture; their mathematical validity does not promote the calibration receipt
into a research claim or a fixed-core packet decision.
"""

# The retained packet module owns generic route and row kernels as well as a separate,
# target-bound state machine.  This command imports only the generic kernels.
# pyright: reportPrivateUsage=false

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import math
import os
import platform
import resource
import signal
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable, Collection, Sequence
from contextlib import suppress
from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime
from fractions import Fraction
from itertools import pairwise
from pathlib import Path
from typing import Any, Literal, Never, cast

from strif import atomic_write_text

from devtools.decide_threshold_certificate import _placement_membership, load
from devtools.dilation_corollary import (
    THRESHOLD_LIMIT_RECORD_SCHEMA,
    THRESHOLD_VARIANT,
    _decimal,
    point_view,
    sharp_dilation_ceiling,
)
from devtools.fixed_core_packet import (
    ExactReaderDisagreementError,
    ExactRoute,
    IntervalReadback,
    IntervalRoute,
    PacketDeadlineError,
    PacketError,
    RawMinimum,
    WorkerTaskObservation,
    _direction_digest,
    _direction_files,
    _exact_row,
    _interval_row,
    _interval_row_readback,
    _raw_row,
    _reconstruct_dilation_directions,
    _reconstruct_exact_directions,
    _reconstruct_interval_directions,
    _reconstruct_raw_directions,
    _strict_json,
    _strict_json_bytes,
    _validate_runtime_record,
    _write_direction,
    replay_raw_witness,
    run_dilation_replay,
    run_exact_route,
    run_interval_route,
    run_raw_sweep,
    runtime_binding,
)
from sqpack.fractional.model import Atom
from sqpack.fractional.threshold import (
    Point,
    ThresholdAtom,
    ThresholdCertificate,
    closed_form_threshold_conditions,
    exact_charge,
    expansion_terms,
)
from sqpack.fractional.threshold_interval import (
    exact_charge_at_witness,
    scaled_threshold_masses,
)

PACKING = Path(__file__).resolve().parents[1]
RUNNING_REPOSITORY = PACKING.parent.resolve()
RUNNING_ENTRY_POINT = Path(__file__).resolve()

RESULT_SCHEMA = "fixed-core-packet-calibration/v1"
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

FIXTURE_N = 2
FIXTURE_OUTER_SIDE = Fraction(3, 4)
FIXTURE_CORE_SIDE = Fraction(1, 2)
FIXTURE_ANGLE_LIMIT = Fraction(1, 2)
FIXTURE_STEPS = 2880
FIXTURE_HALF_GAP = Fraction(1, 5760)
RAW_DIRECTIONS = FIXTURE_STEPS + 1
INTERVAL_DIRECTIONS = 2 * FIXTURE_STEPS + 1
TOTAL_DIRECTION_ROWS = 3 * RAW_DIRECTIONS + INTERVAL_DIRECTIONS
RAW_MINIMUM = Fraction(2)
RAW_BUDGET = Fraction(2)
RAW_THRESHOLD = RAW_BUDGET / FIXTURE_N
NORMALIZATION_ALPHA = Fraction(1, 2)
NORMALIZED_MINIMUM = Fraction(1)
NORMALIZED_BUDGET = Fraction(1)
NORMALIZED_SCALE = 8
EXPECTED_INTERVAL_BOUND = 8
EXPECTED_FACTOR_SQUARED = Fraction(132710404, 33189121)
EXPECTED_SIDE_SQUARED = Fraction(298598409, 132756484)
EXPECTED_STRICT_LEFT = Fraction(33189121, 132710400)
EXPECTED_STRICT_RIGHT = Fraction(33177601, 33177600)

MAX_WORKERS = 4
DEFAULT_GRACE_SECONDS = 2.0
RSS_SAMPLE_SECONDS = 0.1
MINIMUM_TERMINAL_RSS_SAMPLES = 2
RSS_OBSERVABLE_PHASES = (
    "preflight",
    "raw-sweep",
    "normalized-exact",
    "reflected-interval",
    "dilation-replay",
    "readback",
    "awaiting-worker-exit",
)
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
WORKER_DISJOINT_PHASES = (
    "preflight_seconds",
    "raw_seconds",
    "normalization_publication_seconds",
    "exact_seconds",
    "interval_seconds",
    "dilation_seconds",
    "full_readback_seconds",
)
# Account for floating-point subtraction and serialization of the phase observations.
PHASE_ROUNDING_REL_TOL = 1e-9
PHASE_ROUNDING_ABS_TOL = 1e-9
RSS_SCOPE = (
    "sampled sum of resident-set sizes for observed members of the supervised process "
    "group; samples can miss transient peaks and can count shared pages more than once"
)
WORKER_TOPOLOGY_SCHEMA = "fixed-core-packet-calibration-worker-topology/v1"
WORKER_TOPOLOGY_ROUTE_SCHEMA = "fixed-core-packet-calibration-worker-route/v1"
WORKER_TOPOLOGY_SCOPE = (
    "route-scoped coordinator and completed process-pool task lifetimes observed by "
    "the calibration worker; configured workers are reported separately from actual "
    "child identities and simultaneous task execution, and no process arguments or "
    "unrelated host-process metadata are retained"
)
CPU_SCOPE = (
    "coordinator process_time plus cumulative user/system time of its reaped direct "
    "children between retained start and end observations; neither is process-group "
    "CPU time and parent readback CPU is excluded"
)

FORBIDDEN_RECEIPT_KEYS = {
    "scientific_decision",
    "packet",
    "strictly_above_t026",
    "t026_path",
    "t026_sha256",
}
FORBIDDEN_RECEIPT_VALUES = (
    "packet-accepted",
    "BC329",
    "T-025",
    "T-026",
    "n11_threshold_certificate",
)

Clock = Callable[[], float]


class CalibrationError(ValueError):
    """A fixture, invocation, result, or reader violated the calibration contract."""


class CalibrationDeadlineError(CalibrationError):
    """The calibration deadline expired after the last atomic checkpoint."""


class CalibrationOperationalError(RuntimeError):
    """A transient host or process failure left the calibration unresolved."""


class _SupervisorSignal(BaseException):
    """Transfer POSIX termination to synchronous process-group cleanup."""

    def __init__(self, signum: int) -> None:
        self.signum = signum
        super().__init__(signum)


def _refuse(message: str) -> Never:
    raise CalibrationError(message)


@dataclass(frozen=True, slots=True)
class RouteKernels:
    """Test seam for the four generic kernels; the command line has no injection switch."""

    raw: Callable[..., RawMinimum] = run_raw_sweep
    exact: Callable[..., ExactRoute] = run_exact_route
    interval: Callable[..., IntervalRoute] = run_interval_route
    dilation: Callable[..., dict[str, object]] = run_dilation_replay


REAL_KERNELS = RouteKernels()


def _expected_fixture_record() -> dict[str, object]:
    center = ["3/8", "3/8"]
    return {
        "id": FIXTURE_ID,
        "variant": "threshold",
        "n": FIXTURE_N,
        "claim": "s(2) >= 3/4",
        "outer_side": str(FIXTURE_OUTER_SIDE),
        "square_side": str(FIXTURE_CORE_SIDE),
        "angle_limit": str(FIXTURE_ANGLE_LIMIT),
        "direction_steps": FIXTURE_STEPS,
        "symmetry": "D4",
        "point_mass": "1/2",
        "threshold_budget": "3/2",
        "total_budget": str(RAW_BUDGET),
        "atoms": [[*center, "1/2"]],
        "threshold_atoms": [
            {
                "points": [["3/16", "3/8"], center, ["9/16", "3/8"]],
                "threshold": 2,
                "weight": "3/4",
            },
            {
                "points": [["3/8", "3/16"], center, ["3/8", "9/16"]],
                "threshold": 2,
                "weight": "3/4",
            },
        ],
        "provenance": FIXTURE_PROVENANCE,
    }


def load_fixture(raw: bytes) -> tuple[ThresholdCertificate, dict[str, object]]:
    """Read the byte-frozen cross fixture and verify its mathematical construction."""

    if len(raw) != FIXTURE_BYTES or hashlib.sha256(raw).hexdigest() != FIXTURE_SHA256:
        raise CalibrationError("calibration fixture bytes differ from the frozen source")
    certificate, record = load(raw)
    if record != _expected_fixture_record():
        raise CalibrationError("calibration fixture fields or ordering changed")
    if (
        certificate.n != FIXTURE_N
        or certificate.outer_side != FIXTURE_OUTER_SIDE
        or certificate.square_side != FIXTURE_CORE_SIDE
        or certificate.total_budget != RAW_BUDGET
        or len(certificate.directions) != RAW_DIRECTIONS
        or certificate.half_tangents
        != tuple(Fraction(index, 5760) for index in range(RAW_DIRECTIONS))
    ):
        raise CalibrationError("calibration fixture reconstruction changed")
    _validate_fixture_oracles(certificate)
    return certificate, record


def _normalized_record(source: dict[str, object]) -> dict[str, object]:
    """Construct the sole normalized candidate without target-derived provenance."""

    if source != _expected_fixture_record():
        raise CalibrationError("normalization requires the frozen calibration fixture")
    record = deepcopy(source)
    record.update(
        {
            "id": NORMALIZED_ID,
            "point_mass": "1/4",
            "threshold_budget": "3/4",
            "total_budget": str(NORMALIZED_BUDGET),
            "least_cell_charge": str(NORMALIZED_MINIMUM),
        }
    )
    cast(list[list[str]], record["atoms"])[0][2] = "1/4"
    for atom in cast(list[dict[str, object]], record["threshold_atoms"]):
        atom["weight"] = "3/8"
    record["provenance"] = {
        "kind": "normalized synthetic fixed-core packet calibration fixture",
        "construction": FIXTURE_PROVENANCE["construction"],
        "purpose": FIXTURE_PROVENANCE["purpose"],
        "derived_from": FIXTURE_PATH,
        "source_id": FIXTURE_ID,
        "normalization": "every weight multiplied by 1/2 after raw minimum 2",
    }
    return record


def normalized_bytes(source: dict[str, object]) -> bytes:
    return (json.dumps(_normalized_record(source), indent=1, allow_nan=False) + "\n").encode()


def load_normalized(raw: bytes) -> tuple[ThresholdCertificate, dict[str, object]]:
    certificate, record = load(raw)
    expected = _normalized_record(_expected_fixture_record())
    if record != expected:
        raise CalibrationError("normalized candidate differs from the frozen derivation")
    conditions = closed_form_threshold_conditions(certificate)
    if (
        certificate.total_budget != NORMALIZED_BUDGET
        or certificate.point_mass != Fraction(1, 4)
        or certificate.threshold_budget != Fraction(3, 4)
        or scaled_threshold_masses(certificate)[:4]
        != (NORMALIZED_SCALE, [2], [3, 3], EXPECTED_INTERVAL_BOUND)
        or not all(report.holds for report in conditions)
    ):
        raise CalibrationError("normalized candidate fails exact scale or closed-form checks")
    return certificate, record


def raw_decision(minimum: Fraction, *, n: int = FIXTURE_N) -> Literal["passed", "refused"]:
    """Require a strict raw minimum above ``M/n``; equality is a refusal."""

    return "passed" if minimum > RAW_BUDGET / n else "refused"


def _validate_fixture_oracles(certificate: ThresholdCertificate) -> None:
    if certificate.atoms != (Atom("0000", Fraction(3, 8), Fraction(3, 8), Fraction(1, 2)),):
        raise CalibrationError("calibration point atom changed")
    expected_thresholds = (
        ThresholdAtom(
            (
                (Fraction(3, 16), Fraction(3, 8)),
                (Fraction(3, 8), Fraction(3, 8)),
                (Fraction(9, 16), Fraction(3, 8)),
            ),
            2,
            Fraction(3, 4),
        ),
        ThresholdAtom(
            (
                (Fraction(3, 8), Fraction(3, 16)),
                (Fraction(3, 8), Fraction(3, 8)),
                (Fraction(3, 8), Fraction(9, 16)),
            ),
            2,
            Fraction(3, 4),
        ),
    )
    if certificate.threshold_atoms != expected_thresholds:
        raise CalibrationError("calibration threshold atoms or their order changed")
    anchors = (
        ((Fraction(9, 32), Fraction(9, 32)), RAW_MINIMUM, (2, 2)),
        ((Fraction(3, 8), Fraction(3, 8)), RAW_MINIMUM, (3, 3)),
    )
    for witness, expected_charge, expected_counts in anchors:
        contains = _placement_membership(certificate, 0, witness)
        counts = tuple(atom.trace_count(contains) for atom in certificate.threshold_atoms)
        if (
            counts != expected_counts
            or exact_charge(certificate.atoms, certificate.threshold_atoms, contains)
            != expected_charge
        ):
            raise CalibrationError("calibration membership anchor changed")
    if expansion_terms(3, 2) != ((2, 1), (3, -2)):
        raise CalibrationError("two-of-three inclusion-exclusion expansion changed")


def larger_domain_zero_control() -> tuple[Fraction, bool]:
    """Return the exact below-threshold charge and admissibility of the design control."""

    center = Fraction(3, 4)
    offset = Fraction(3, 16)
    certificate = ThresholdCertificate(
        n=FIXTURE_N,
        outer_side=Fraction(3, 2),
        square_side=FIXTURE_CORE_SIDE,
        atoms=(Atom("0000", center, center, Fraction(1, 4)),),
        threshold_atoms=(
            ThresholdAtom(
                (
                    (center - offset, center),
                    (center, center),
                    (center + offset, center),
                ),
                2,
                Fraction(3, 8),
            ),
            ThresholdAtom(
                (
                    (center, center - offset),
                    (center, center),
                    (center, center + offset),
                ),
                2,
                Fraction(3, 8),
            ),
        ),
        half_tangents=(Fraction(0), FIXTURE_ANGLE_LIMIT),
    )
    witness = (Fraction(15, 32), center)
    result = RawMinimum(Fraction(0), 0, witness, 1)
    replayed, admissible = replay_raw_witness(certificate, result)
    return replayed, admissible


def _expired(deadline: float, clock: Clock, phase: str) -> None:
    if clock() >= deadline:
        raise CalibrationDeadlineError(f"calibration deadline reached {phase}")


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _interval_labels(steps: int = FIXTURE_STEPS) -> tuple[str, ...]:
    return tuple(str(index) for index in range(steps + 1)) + tuple(
        f"{index}'" for index in range(1, steps + 1)
    )


def _ordered_labels(labels: Collection[str]) -> list[str]:
    order = {label: index for index, label in enumerate(_interval_labels())}
    return sorted(labels, key=order.__getitem__)


def _check_raw_rows(
    directory: Path, certificate: ThresholdCertificate, *, expected: int
) -> RawMinimum:
    files = _direction_files(
        directory, allowed_labels={str(index) for index in range(expected)}
    )
    if set(files) != {str(index) for index in range(expected)}:
        raise CalibrationError("raw known-answer row set is incomplete")
    rows: list[tuple[int, Fraction, Point]] = []
    for index in range(expected):
        charge, witness = _raw_row(files[str(index)], index)
        replayed, admissible = replay_raw_witness(
            certificate, RawMinimum(charge, index, witness, 1)
        )
        if charge != RAW_MINIMUM or replayed != RAW_MINIMUM or not admissible:
            raise CalibrationError(f"raw known-answer check failed at direction {index}")
        rows.append((index, charge, witness))
    first = rows[0]
    return RawMinimum(first[1], first[0], first[2], len(rows))


def _check_exact_rows(
    directory: Path, certificate: ThresholdCertificate, *, expected: int
) -> ExactRoute:
    files = _direction_files(
        directory, allowed_labels={str(index) for index in range(expected)}
    )
    if set(files) != {str(index) for index in range(expected)}:
        raise CalibrationError("normalized exact known-answer row set is incomplete")
    first_witness: Point | None = None
    for index in range(expected):
        dense, slab = _exact_row(files[str(index)], index)
        for name, (charge, witness) in (("dense", dense), ("slab", slab)):
            replayed, admissible = replay_raw_witness(
                certificate, RawMinimum(charge, index, witness, 1)
            )
            if charge != NORMALIZED_MINIMUM or replayed != charge or not admissible:
                raise CalibrationError(
                    f"normalized {name} known-answer check failed at direction {index}"
                )
        if dense != slab:
            raise CalibrationError(f"normalized readers disagree at direction {index}")
        if index == 0:
            first_witness = dense[1]
    if first_witness is None:
        raise CalibrationError("normalized exact route has no rows")
    return ExactRoute(NORMALIZED_MINIMUM, 0, first_witness, expected, 0)


def _check_interval_rows(
    directory: Path,
    certificate: ThresholdCertificate,
    *,
    labels: Sequence[str],
) -> tuple[IntervalReadback, int]:
    files = _direction_files(directory, allowed_labels=set(labels))
    if set(files) != set(labels):
        raise CalibrationError("reflected interval known-answer row set is incomplete")
    boxes = 0
    for label in labels:
        outcome = _interval_row_readback(_strict_json(files[label]), label, str(files[label]))
        if (
            outcome.status != "certified"
            or outcome.lower != EXPECTED_INTERVAL_BOUND
            or outcome.upper != EXPECTED_INTERVAL_BOUND
            or outcome.witness is None
            or outcome.boxes <= 0
            or outcome.stalled != 0
            or outcome.budget_exhausted
        ):
            raise CalibrationError(f"interval known-answer check failed at direction {label}")
        witness = exact_charge_at_witness(certificate, label, outcome.witness)
        if not witness.admissible or witness.charge != NORMALIZED_MINIMUM:
            raise CalibrationError(f"interval witness check failed at direction {label}")
        boxes += outcome.boxes
    return (
        IntervalReadback(
            (NORMALIZED_MINIMUM, NORMALIZED_MINIMUM),
            len(labels),
            0,
            0,
            accepted=True,
        ),
        boxes,
    )


def _check_dilation_rows(
    directory: Path, certificate: ThresholdCertificate, *, expected: int
) -> None:
    files = _direction_files(
        directory, allowed_labels={str(index) for index in range(expected)}
    )
    if set(files) != {str(index) for index in range(expected)}:
        raise CalibrationError("dilation known-answer row set is incomplete")
    for index, direction in enumerate(certificate.directions):
        row = _strict_json(files[str(index)])
        if set(row) != {"direction", "label", "minimum"} or row != {
            "direction": index,
            "label": direction.label,
            "minimum": str(NORMALIZED_MINIMUM),
        }:
            raise CalibrationError(f"dilation known-answer check failed at direction {index}")


def _expected_dilation_record(
    certificate: ThresholdCertificate, source_sha256: str
) -> dict[str, object]:
    point = point_view(certificate)
    gap = point.largest_half_gap_tangent
    factor = sharp_dilation_ceiling(certificate)
    side = factor.scaled(certificate.outer_side)
    left = point.square_side**2 * (1 + gap) ** 2
    right = 1 + gap * gap
    expected = {
        "schema": THRESHOLD_LIMIT_RECORD_SCHEMA,
        "source": {
            "certificate": "candidate.json",
            "sha256": source_sha256,
            "n": FIXTURE_N,
            "outer_side": str(certificate.outer_side),
            "square_side": str(point.square_side),
            "half_gap_tangent": str(gap),
            "coarse_containment": str(point.square_side * (1 + gap)),
            "total_budget": str(NORMALIZED_BUDGET),
            "minimum_cell_charge": str(NORMALIZED_MINIMUM),
            "accepted_conditions": [
                condition.name for condition in closed_form_threshold_conditions(certificate)
            ]
            + ["Condition 5' every reachable cell is charged at least 1"],
            "variant": THRESHOLD_VARIANT,
            "point_atoms": len(certificate.atoms),
            "threshold_atoms": len(certificate.threshold_atoms),
        },
        "sharpened_containment": {
            "identity": "cos(d) + sin(d) = (1 + t) / sqrt(1 + t^2), where t = tan(d)",
            "gap_domain": f"0 <= t <= D = {gap} < 1",
            "monotonicity_identity": (
                "(1 + D)^2(1 + t^2) - (1 + t)^2(1 + D^2) = 2(D - t)(1 - Dt) >= 0"
            ),
            "strict_factor_test": f"q^2 * {left} < {right}",
            "strict_factor_test_left_multiplier": str(left),
            "strict_factor_test_right": str(right),
            "source_gap_below_one": True,
        },
        "strict_dilation_family": {
            "factor_supremum": factor.exact,
            "factor_supremum_squared": str(factor.squared),
            "factor_supremum_decimal": _decimal(factor),
            "factor_supremum_irrational": factor.irrational,
            "factor_supremum_defining_polynomial": factor.defining_polynomial,
            "factor_domain": f"q in Q with q > 0 and q^2 < {factor.squared}",
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
        },
        "conclusion": {
            "bounded_side": side.exact,
            "bounded_side_squared": str(side.squared),
            "bounded_side_defining_polynomial": side.defining_polynomial,
            "decimal": _decimal(side),
            "relation": ">=",
            "endpoint_certificate": False,
        },
        "proof": {
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
                f"the dilation-limit theorem establishes s({FIXTURE_N}) >= {side.exact}; "
                "at the factor supremum the sharpened containment inequality is equality, "
                "so endpoint_certificate is false because the proof supplies no individual "
                f"certificate at that side; the method does not establish s({FIXTURE_N}) > "
                f"{side.exact}"
            ),
        },
    }
    if scaled_threshold_masses(certificate)[0] != NORMALIZED_SCALE:
        raise CalibrationError("dilation source does not use normalized scale 8")
    return expected


def _check_dilation_record(
    record: dict[str, object], certificate: ThresholdCertificate, source_sha256: str
) -> None:
    expected = _expected_dilation_record(certificate, source_sha256)
    if record != expected:
        raise CalibrationError("dilation record differs from the exact calibration oracle")


def _walk_receipt(value: object) -> None:
    if isinstance(value, dict):
        for key, nested in cast(dict[object, object], value).items():
            if key in FORBIDDEN_RECEIPT_KEYS:
                raise CalibrationError(f"calibration receipt carries forbidden field {key!r}")
            _walk_receipt(nested)
    elif isinstance(value, list):
        for nested in cast(list[object], value):
            _walk_receipt(nested)
    elif isinstance(value, str) and any(term in value for term in FORBIDDEN_RECEIPT_VALUES):
        raise CalibrationError("calibration receipt carries scientific target vocabulary")


PROJECT_RUNTIME_PATHS = (
    "packing/.python-version",
    "packing/pyproject.toml",
    "packing/uv.lock",
)


def _git(repository: Path, *arguments: str) -> str:
    result = subprocess.run(
        ("git", *arguments), cwd=repository, check=False, capture_output=True, text=True
    )
    if result.returncode:
        raise CalibrationOperationalError(
            result.stderr.strip() or f"git {' '.join(arguments)} failed"
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
    except (OSError, SyntaxError) as error:
        raise CalibrationError(f"could not inspect dependency {path}: {error}") from error
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
                    raise CalibrationError(
                        f"could not resolve relative import {relative!r} in {path}"
                    ) from error
            if base:
                imported.add(base)
                imported.update(f"{base}.{alias.name}" for alias in node.names)
    return imported


def discover_implementation_paths(repository: Path) -> tuple[str, ...]:
    """Return the fixture, runtime declarations, and recursive local code closure."""

    repository = repository.resolve()
    pending = ["devtools.calibrate_fixed_core_packet"]
    visited: set[str] = set()
    paths = {FIXTURE_PATH, *PROJECT_RUNTIME_PATHS}
    while pending:
        module = pending.pop()
        if module in visited:
            continue
        path = _local_module_path(repository, module)
        if path is None:
            continue
        visited.add(module)
        paths.add(path.relative_to(repository).as_posix())
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
        raise CalibrationError("repository must contain the running calibration command")
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
        if module == "devtools.calibrate_fixed_core_packet" and loaded is None:
            loaded = sys.modules.get("__main__")
        if loaded is None:
            continue
        origin = getattr(loaded, "__file__", None)
        if type(origin) is not str or Path(origin).resolve() != repository / relative:
            raise CalibrationError(
                f"loaded project module {module} comes from another checkout"
            )


def source_manifest(
    repository: Path,
    revision: str,
    *,
    result_directory: Path | None = None,
) -> list[dict[str, str]]:
    """Record the calibration source and implementation closure the run executes.

    Each row names a path, its blob at `revision` and the SHA-256 of the bytes on disk,
    so an uncommitted edit shows in the receipt instead of refusing the run. `revision`
    is the operator's statement of the commit being run and must be the checkout's
    `HEAD`, because it is what the receipt records; any commit satisfies that.
    """

    if len(revision) != 40 or any(c not in "0123456789abcdef" for c in revision):
        raise CalibrationError("expected revision must be 40 lowercase hexadecimal digits")
    repository = repository.resolve()
    if result_directory is not None and result_directory.resolve().is_relative_to(repository):
        raise CalibrationError("calibration output must be outside the repository")
    paths = discover_implementation_paths(repository)
    _validate_loaded_modules(repository, paths)
    if _git(repository, "rev-parse", "HEAD") != revision:
        raise CalibrationError("current Git revision differs from the stated revision")
    tracked = set(
        _git(repository, "ls-tree", "-r", "--name-only", revision, "--", *paths).splitlines()
    )
    if tracked != set(paths):
        missing = ", ".join(sorted(set(paths) - tracked))
        raise CalibrationError(f"calibration source closure is not committed: {missing}")
    manifest = [
        {
            "path": relative,
            "git_blob": _git(repository, "rev-parse", f"{revision}:{relative}"),
            "sha256": hashlib.sha256((repository / relative).read_bytes()).hexdigest(),
        }
        for relative in paths
    ]
    fixture = next(row for row in manifest if row["path"] == FIXTURE_PATH)
    if fixture["sha256"] != FIXTURE_SHA256:
        raise CalibrationError("fixture manifest differs from the frozen source identity")
    return manifest


def _effective_workers(requested: int) -> dict[str, int]:
    parallel_generic = requested if sys.platform.startswith("linux") else 1
    return {
        "raw": min(requested, RAW_DIRECTIONS),
        "normalized_exact": min(requested, RAW_DIRECTIONS),
        "reflected_interval": min(parallel_generic, INTERVAL_DIRECTIONS),
        "dilation": min(parallel_generic, RAW_DIRECTIONS),
    }


def _settings(
    *,
    workers: int,
    calibration_seconds: float,
    external_seconds: float,
    grace_seconds: float,
) -> dict[str, object]:
    return {
        "requested_workers": workers,
        "effective_workers": _effective_workers(workers),
        "calibration_seconds": calibration_seconds,
        "external_seconds": external_seconds,
        "termination_grace_seconds": grace_seconds,
        "rss_sample_interval_seconds": RSS_SAMPLE_SECONDS,
        "core_side": str(FIXTURE_CORE_SIDE),
        "direction_steps": FIXTURE_STEPS,
        "angle_limit": str(FIXTURE_ANGLE_LIMIT),
        "half_gap_tangent": str(FIXTURE_HALF_GAP),
        "raw_threshold_M_over_n": str(RAW_THRESHOLD),
        "expected_direction_rows": TOTAL_DIRECTION_ROWS,
    }


def _invocation_identity(
    revision: str,
    *,
    workers: int,
    calibration_seconds: float,
    external_seconds: float,
    grace_seconds: float,
    invocation_started: float,
    run_order: int,
    cache_observation: str,
    background_load: str,
) -> dict[str, object]:
    calibration_deadline = invocation_started + calibration_seconds
    external_deadline = invocation_started + external_seconds
    if not math.isfinite(calibration_deadline) or not math.isfinite(external_deadline):
        raise CalibrationError("derived invocation deadlines are not finite")
    return {
        "implementation_revision": revision,
        "requested_workers": workers,
        "calibration_seconds": calibration_seconds,
        "external_seconds": external_seconds,
        "termination_grace_seconds": grace_seconds,
        "monotonic_origin": invocation_started,
        "calibration_deadline_monotonic": calibration_deadline,
        "external_deadline_monotonic": external_deadline,
        "run_order": run_order,
        "cache_observation": cache_observation,
        "background_load": background_load,
    }


def initial_document(
    revision: str,
    *,
    workers: int,
    calibration_seconds: float,
    external_seconds: float,
    grace_seconds: float,
    invocation_started: float,
    run_order: int,
    cache_observation: str,
    background_load: str,
) -> dict[str, object]:
    """Seed the calibration receipt before the bounded worker preflight starts."""

    return {
        "schema": RESULT_SCHEMA,
        "status": "partial",
        "disposition": "incomplete",
        "evidence_scope": CALIBRATION_SCOPE,
        "fixture": {
            "id": FIXTURE_ID,
            "source_path": FIXTURE_PATH,
            "source_sha256": FIXTURE_SHA256,
            "source_bytes": FIXTURE_BYTES,
            "provenance": FIXTURE_PROVENANCE,
        },
        "sources": {
            "implementation_revision": revision,
            "manifest": None,
            "runtime": None,
        },
        "invocation": {
            "started_utc": datetime.now(UTC).isoformat(),
            "monotonic_origin": invocation_started,
            "host": platform.node(),
            "platform": platform.platform(),
            "run_order": run_order,
            "cache_observation": cache_observation,
            "background_load": background_load,
            "identity": _invocation_identity(
                revision,
                workers=workers,
                calibration_seconds=calibration_seconds,
                external_seconds=external_seconds,
                grace_seconds=grace_seconds,
                invocation_started=invocation_started,
                run_order=run_order,
                cache_observation=cache_observation,
                background_load=background_load,
            ),
        },
        "settings": _settings(
            workers=workers,
            calibration_seconds=calibration_seconds,
            external_seconds=external_seconds,
            grace_seconds=grace_seconds,
        ),
        "clocks": {
            "phase_duration_scope": PHASE_DURATION_SCOPE,
            "preflight_seconds": None,
            "launch_seconds": None,
            "source_loading_seconds": None,
            "raw_seconds": None,
            "normalization_publication_seconds": None,
            "exact_seconds": None,
            "interval_seconds": None,
            "dilation_seconds": None,
            "full_readback_seconds": None,
            "parent_final_readback_seconds": None,
            "terminal_admission_seconds": None,
            "worker_elapsed_seconds": None,
            "worker_exit_seconds": None,
            "supervisor_cleanup_seconds": None,
            "external_lifetime_seconds": None,
        },
        "resources": {
            "cpu_scope": CPU_SCOPE,
            "cpu_observations": None,
            "coordinator_process_seconds": None,
            "reaped_direct_children_user_seconds": None,
            "reaped_direct_children_system_seconds": None,
            "rss": None,
            "worker_topology": None,
        },
        "raw": {
            "directions_expected": RAW_DIRECTIONS,
            "directions_completed": 0,
            "completed_directions": [],
            "observed_minimum_upper_bound": None,
            "observed_argmin": None,
            "observed_witness": None,
            "raw_minimum": None,
            "budget": str(RAW_BUDGET),
            "threshold_M_over_n": str(RAW_THRESHOLD),
            "comparison": None,
            "witness_replay_charge": None,
            "witness_admissible": None,
            "directions_sha256": None,
        },
        "normalized": None,
        "routes": {
            "normalized_exact": None,
            "reflected_interval": None,
            "dilation": None,
        },
        "artifacts": [],
        "supervision": {
            "status": "pending",
            "worker_exit_status": None,
            "process_group_reaped": False,
            "supervisor_signal": None,
            "coordinator_pid": None,
            "coordinator_process_group_id": None,
        },
        "phase": "preflight",
        "error": "source and runtime preflight has not completed",
    }


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


def _finite_nonnegative(value: object, label: str, *, optional: bool = True) -> None:
    if value is None and optional:
        return
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(value)
        or value < 0
    ):
        raise CalibrationError(f"{label} is not a finite nonnegative observation")


def _validate_worker_phase_durations(clocks: dict[str, object]) -> None:
    for name in (*WORKER_DISJOINT_PHASES, "worker_elapsed_seconds"):
        _finite_nonnegative(clocks.get(name), f"clock {name}", optional=False)
    try:
        total = math.fsum(cast(float, clocks[name]) for name in WORKER_DISJOINT_PHASES)
    except OverflowError as error:
        raise CalibrationError("worker phase durations exceed worker elapsed") from error
    elapsed = cast(float, clocks["worker_elapsed_seconds"])
    if not math.isfinite(total) or (
        total > elapsed
        and not math.isclose(
            total, elapsed, rel_tol=PHASE_ROUNDING_REL_TOL, abs_tol=PHASE_ROUNDING_ABS_TOL
        )
    ):
        raise CalibrationError("worker phase durations exceed worker elapsed")


def _canonical_rational_text(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        return str(Fraction(value)) == value
    except ValueError, ZeroDivisionError:
        return False


def _rational_point(value: object) -> bool:
    return (
        isinstance(value, list)
        and len(value) == 2
        and all(_canonical_rational_text(coordinate) for coordinate in value)
    )


def _digest(value: object, *, length: int = 64) -> bool:
    return (
        isinstance(value, str)
        and len(value) == length
        and all(character in "0123456789abcdef" for character in value)
    )


def _validate_route_receipt(name: str, receipt: object) -> None:
    if receipt is None:
        return
    if not isinstance(receipt, dict):
        raise CalibrationError(f"{name} route receipt is malformed")
    status = receipt.get("status")
    common = {
        "status",
        "source_sha256",
        "directions_expected",
        "directions_completed",
        "completed_directions",
    }
    partial = {
        "normalized_exact": common | {"observed_minimum_upper_bound", "argmin", "witness"},
        "reflected_interval": common | {"last"},
        "dilation": common | {"last"},
    }
    complete = {
        "normalized_exact": common
        | {
            "minimum",
            "argmin",
            "witness",
            "dense_slab_disagreements",
            "directions_sha256",
        },
        "reflected_interval": common
        | {
            "integer_scale",
            "integer_enclosure",
            "enclosure",
            "stalled",
            "budget_exhausted",
            "accepted",
            "boxes_observed",
            "directions_sha256",
        },
        "dilation": common
        | {
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
    }
    if status == "partial":
        if set(receipt) != partial[name] or (
            name != "normalized_exact" and not isinstance(receipt.get("last"), dict)
        ):
            raise CalibrationError(f"{name} partial route fields changed")
    elif status == "complete":
        if set(receipt) != complete[name]:
            raise CalibrationError(f"{name} complete route fields changed")
    else:
        raise CalibrationError(f"{name} route status is malformed")
    expected = INTERVAL_DIRECTIONS if name == "reflected_interval" else RAW_DIRECTIONS
    completed = receipt.get("directions_completed")
    completed_directions = receipt.get("completed_directions")
    if (
        receipt.get("directions_expected") != expected
        or type(completed) is not int
        or not 0 <= cast(int, completed) <= expected
        or not isinstance(completed_directions, list)
        or len(completed_directions) != completed
        or not _digest(receipt.get("source_sha256"))
    ):
        raise CalibrationError(f"{name} route progress is malformed")
    if name == "reflected_interval":
        allowed = set(_interval_labels())
        if (
            any(
                not isinstance(label, str) or label not in allowed
                for label in completed_directions
            )
            or len(set(cast(list[str], completed_directions))) != completed
            or completed_directions != _ordered_labels(cast(list[str], completed_directions))
        ):
            raise CalibrationError("reflected interval completed labels are malformed")
    elif name == "dilation":
        allowed = {str(index) for index in range(RAW_DIRECTIONS)}
        if (
            any(
                not isinstance(label, str) or label not in allowed
                for label in completed_directions
            )
            or len(set(cast(list[str], completed_directions))) != completed
            or completed_directions
            != sorted(set(cast(list[str], completed_directions)), key=int)
        ):
            raise CalibrationError("dilation completed labels are malformed")
    elif any(type(index) is not int for index in completed_directions) or (
        completed_directions != sorted(set(cast(list[int], completed_directions)))
    ):
        raise CalibrationError(f"{name} completed directions are malformed")
    if status != "complete":
        return
    if (
        completed != expected
        or (name == "reflected_interval" and completed_directions != list(_interval_labels()))
        or (
            name == "dilation"
            and completed_directions != [str(index) for index in range(RAW_DIRECTIONS)]
        )
        or (name == "normalized_exact" and completed_directions != list(range(RAW_DIRECTIONS)))
        or not _digest(receipt.get("directions_sha256"))
    ):
        raise CalibrationError(f"{name} complete direction binding is malformed")
    if name == "normalized_exact" and (
        receipt.get("minimum") != str(NORMALIZED_MINIMUM)
        or receipt.get("argmin") != 0
        or not _rational_point(receipt.get("witness"))
        or receipt.get("dense_slab_disagreements") != 0
    ):
        raise CalibrationError("normalized exact known-answer summary changed")
    if name == "reflected_interval" and (
        receipt.get("integer_scale") != NORMALIZED_SCALE
        or receipt.get("integer_enclosure")
        != [EXPECTED_INTERVAL_BOUND, EXPECTED_INTERVAL_BOUND]
        or receipt.get("enclosure") != [str(NORMALIZED_MINIMUM), str(NORMALIZED_MINIMUM)]
        or receipt.get("stalled") != 0
        or receipt.get("budget_exhausted") != 0
        or receipt.get("accepted") is not True
        or type(receipt.get("boxes_observed")) is not int
        or cast(int, receipt["boxes_observed"]) <= 0
    ):
        raise CalibrationError("reflected interval known-answer summary changed")
    if name == "dilation" and (
        not _digest(receipt.get("record_sha256"))
        or receipt.get("generic_record_schema") != THRESHOLD_LIMIT_RECORD_SCHEMA
        or receipt.get("generic_record_scope")
        != "valid normalized n=2 calibration fixture; no campaign or fixed-packet evidence"
        or receipt.get("factor_supremum") != "2*sqrt(33177601)/5761"
        or receipt.get("factor_supremum_squared") != str(EXPECTED_FACTOR_SQUARED)
        or receipt.get("bounded_side") != "3*sqrt(33177601)/11522"
        or receipt.get("bounded_side_squared") != str(EXPECTED_SIDE_SQUARED)
        or receipt.get("relation") != ">="
        or receipt.get("endpoint_certificate") is not False
        or receipt.get("requires_compactness") is not False
    ):
        raise CalibrationError("dilation known-answer summary changed")


def _validate_artifact_receipts(value: object) -> None:
    if not isinstance(value, list):
        raise CalibrationError("artifact inventory is malformed")
    seen: set[str] = set()
    for row in cast(list[object], value):
        if not isinstance(row, dict) or set(row) != {"role", "path", "count", "bytes"}:
            raise CalibrationError("artifact inventory row fields changed")
        role = row.get("role")
        path = row.get("path")
        if (
            not isinstance(role, str)
            or role in seen
            or not isinstance(path, str)
            or Path(path).is_absolute()
            or ".." in Path(path).parts
            or type(row.get("count")) is not int
            or cast(int, row["count"]) < 0
            or type(row.get("bytes")) is not int
            or cast(int, row["bytes"]) < 0
        ):
            raise CalibrationError("artifact inventory row is malformed")
        seen.add(role)


def _validate_worker_topology_summary(
    value: object,
    settings: dict[str, object],
    *,
    required: bool,
) -> None:
    if value is None:
        if required:
            raise CalibrationError("terminal calibration lacks worker topology")
        return
    if not isinstance(value, dict) or set(value) != {
        "schema",
        "scope",
        "coordinator",
        "routes",
    }:
        raise CalibrationError("worker topology fields changed")
    coordinator = value.get("coordinator")
    routes = value.get("routes")
    if (
        value.get("schema") != WORKER_TOPOLOGY_SCHEMA
        or value.get("scope") != WORKER_TOPOLOGY_SCOPE
        or not isinstance(coordinator, dict)
        or set(coordinator) != {"role", "pid", "ppid", "pgid"}
        or not isinstance(routes, dict)
        or set(routes) != {"raw", "normalized_exact"}
    ):
        raise CalibrationError("worker topology is malformed")
    coordinator_pid = coordinator.get("pid")
    coordinator_group = coordinator.get("pgid")
    if (
        coordinator.get("role") != "coordinator"
        or type(coordinator_pid) is not int
        or cast(int, coordinator_pid) <= 0
        or type(coordinator.get("ppid")) is not int
        or cast(int, coordinator["ppid"]) <= 0
        or coordinator_group != coordinator_pid
    ):
        raise CalibrationError("worker topology coordinator identity is malformed")
    configured = settings.get("effective_workers")
    if not isinstance(configured, dict):
        raise CalibrationError("worker topology lacks configured route workers")
    for name, record_path in (
        ("raw", "raw-worker-topology.json"),
        ("normalized_exact", "normalized-exact-worker-topology.json"),
    ):
        route = routes.get(name)
        if route is None:
            if required:
                raise CalibrationError(f"terminal calibration lacks {name} worker topology")
            continue
        expected_workers = configured.get(name)
        if not isinstance(route, dict) or set(route) != {
            "configured_workers",
            "execution_model",
            "observed_child_count",
            "maximum_simultaneous_children",
            "record_path",
            "record_sha256",
        }:
            raise CalibrationError(f"{name} worker topology summary fields changed")
        observed_count = route.get("observed_child_count")
        maximum_simultaneous = route.get("maximum_simultaneous_children")
        parallel = type(expected_workers) is int and cast(int, expected_workers) > 1
        if (
            route.get("configured_workers") != expected_workers
            or route.get("execution_model")
            != ("process-pool" if parallel else "coordinator-serial")
            or route.get("record_path") != record_path
            or not _digest(route.get("record_sha256"))
            or type(observed_count) is not int
            or type(maximum_simultaneous) is not int
            or (
                parallel
                and not (
                    1
                    <= cast(int, maximum_simultaneous)
                    <= cast(int, observed_count)
                    <= cast(int, expected_workers)
                )
            )
            or (not parallel and (observed_count != 0 or maximum_simultaneous != 0))
        ):
            raise CalibrationError(f"{name} worker topology summary is malformed")


def _maximum_simultaneous_children(
    intervals: Sequence[tuple[float, float, int]],
    *,
    phase: str,
) -> int:
    active: set[int] = set()
    maximum = 0
    events = sorted(
        (
            (when, event_order, pid)
            for started, finished, pid in intervals
            for when, event_order in ((finished, 0), (started, 1))
        )
    )
    for _when, event_order, pid in events:
        if event_order == 0:
            if pid not in active:
                raise CalibrationError(f"{phase} child task lifetimes overlap per worker")
            active.remove(pid)
        else:
            if pid in active:
                raise CalibrationError(f"{phase} child task lifetimes overlap per worker")
            active.add(pid)
            maximum = max(maximum, len(active))
    if active:
        raise CalibrationError(f"{phase} child task lifetimes are unbalanced")
    return maximum


def _build_route_worker_topology(
    phase: str,
    *,
    configured_workers: int,
    directions_expected: int,
    coordinator_pid: int,
    coordinator_group: int,
    invocation_started: float,
    observations: Sequence[WorkerTaskObservation],
) -> dict[str, object]:
    if configured_workers == 1:
        if observations:
            raise CalibrationError(f"serial {phase} route reported process-pool children")
        return {
            "phase": phase,
            "execution_model": "coordinator-serial",
            "configured_workers": 1,
            "directions_expected": directions_expected,
            "directions_completed": directions_expected,
            "child_tasks_observed": 0,
            "observed_child_count": 0,
            "maximum_simultaneous_children": 0,
            "tasks": [],
            "children": [],
        }
    if len(observations) != directions_expected:
        raise CalibrationError(f"{phase} route lacks a child observation for every direction")
    if sorted(observation.direction for observation in observations) != list(
        range(directions_expected)
    ):
        raise CalibrationError(f"{phase} child observations do not bind every direction")
    by_pid: dict[int, list[WorkerTaskObservation]] = {}
    for observation in observations:
        if (
            type(observation.direction) is not int
            or observation.pid <= 0
            or observation.ppid != coordinator_pid
            or observation.pgid != coordinator_group
            or not math.isfinite(observation.started)
            or not math.isfinite(observation.finished)
            or observation.started < invocation_started
            or observation.finished <= observation.started
        ):
            raise CalibrationError(f"{phase} child identity or lifetime is malformed")
        by_pid.setdefault(observation.pid, []).append(observation)
    child_pids = set(by_pid)
    if not child_pids or len(child_pids) > configured_workers:
        raise CalibrationError(f"{phase} observed child count exceeds its worker setting")
    intervals = tuple(
        (observation.started, observation.finished, observation.pid)
        for observation in observations
    )
    maximum_simultaneous = _maximum_simultaneous_children(intervals, phase=phase)
    tasks = [
        {
            "direction": observation.direction,
            "pid": observation.pid,
            "ppid": observation.ppid,
            "pgid": observation.pgid,
            "started_seconds": observation.started - invocation_started,
            "finished_seconds": observation.finished - invocation_started,
        }
        for observation in sorted(observations, key=lambda row: row.direction)
    ]
    children = [
        {
            "role": "route-worker",
            "phase": phase,
            "pid": pid,
            "ppid": coordinator_pid,
            "pgid": coordinator_group,
            "tasks_completed": len(rows),
            "first_task_started_seconds": min(row.started for row in rows) - invocation_started,
            "last_task_finished_seconds": max(row.finished for row in rows)
            - invocation_started,
        }
        for pid, rows in sorted(by_pid.items())
    ]
    return {
        "phase": phase,
        "execution_model": "process-pool",
        "configured_workers": configured_workers,
        "directions_expected": directions_expected,
        "directions_completed": directions_expected,
        "child_tasks_observed": len(observations),
        "observed_child_count": len(children),
        "maximum_simultaneous_children": maximum_simultaneous,
        "tasks": tasks,
        "children": children,
    }


def _write_worker_topology(
    output_dir: Path,
    *,
    invocation_started: float,
    configured_workers: dict[str, int],
    raw_observations: Sequence[WorkerTaskObservation],
    exact_observations: Sequence[WorkerTaskObservation] | None,
) -> dict[str, object]:
    coordinator_pid = os.getpid()
    coordinator_group = os.getpgid(0)
    raw = _build_route_worker_topology(
        "raw-sweep",
        configured_workers=configured_workers["raw"],
        directions_expected=RAW_DIRECTIONS,
        coordinator_pid=coordinator_pid,
        coordinator_group=coordinator_group,
        invocation_started=invocation_started,
        observations=raw_observations,
    )
    exact = (
        None
        if exact_observations is None
        else _build_route_worker_topology(
            "normalized-exact",
            configured_workers=configured_workers["normalized_exact"],
            directions_expected=RAW_DIRECTIONS,
            coordinator_pid=coordinator_pid,
            coordinator_group=coordinator_group,
            invocation_started=invocation_started,
            observations=exact_observations,
        )
    )
    coordinator: dict[str, object] = {
        "role": "coordinator",
        "pid": coordinator_pid,
        "ppid": os.getppid(),
        "pgid": coordinator_group,
    }

    def retain_route(name: str, route: dict[str, object]) -> dict[str, object]:
        filename = f"{name.replace('_', '-')}-worker-topology.json"
        record = {
            "schema": WORKER_TOPOLOGY_ROUTE_SCHEMA,
            "scope": WORKER_TOPOLOGY_SCOPE,
            "coordinator": coordinator,
            "route": route,
        }
        encoded = (json.dumps(record, indent=2, allow_nan=False) + "\n").encode()
        path = output_dir / filename
        if path.exists():
            if path.is_symlink() or not path.is_file():
                raise CalibrationError(f"{name} worker topology has the wrong artifact type")
            try:
                retained = path.read_bytes()
            except OSError as error:
                raise CalibrationError(
                    f"{name} worker topology cannot be read after publication"
                ) from error
            if retained != encoded:
                raise CalibrationError(f"{name} worker topology changed after publication")
        else:
            atomic_write_text(path, encoded.decode())
        return {
            "configured_workers": route["configured_workers"],
            "execution_model": route["execution_model"],
            "observed_child_count": route["observed_child_count"],
            "maximum_simultaneous_children": route["maximum_simultaneous_children"],
            "record_path": filename,
            "record_sha256": hashlib.sha256(encoded).hexdigest(),
        }

    return {
        "schema": WORKER_TOPOLOGY_SCHEMA,
        "scope": WORKER_TOPOLOGY_SCOPE,
        "coordinator": coordinator,
        "routes": {
            "raw": retain_route("raw", raw),
            "normalized_exact": (
                None if exact is None else retain_route("normalized_exact", exact)
            ),
        },
    }


def validate_document(document: dict[str, object]) -> None:
    """Validate the closed calibration wrapper without interpreting generic artifacts."""

    if set(document) != TOP_LEVEL_KEYS or document.get("schema") != RESULT_SCHEMA:
        raise CalibrationError("fields do not match fixed-core-packet-calibration/v1")
    _walk_receipt(document)
    status = document.get("status")
    disposition = document.get("disposition")
    if status not in {"partial", "invalid", "complete"}:
        raise CalibrationError("calibration status is malformed")
    if disposition not in {"incomplete", "calibration-refused", "calibration-passed"}:
        raise CalibrationError("calibration disposition is malformed")
    if document.get("evidence_scope") != CALIBRATION_SCOPE:
        raise CalibrationError("calibration evidence scope changed")
    fixture = document.get("fixture")
    if fixture != {
        "id": FIXTURE_ID,
        "source_path": FIXTURE_PATH,
        "source_sha256": FIXTURE_SHA256,
        "source_bytes": FIXTURE_BYTES,
        "provenance": FIXTURE_PROVENANCE,
    }:
        raise CalibrationError("calibration fixture identity or provenance changed")
    sources = document.get("sources")
    if not isinstance(sources, dict) or set(sources) != {
        "implementation_revision",
        "manifest",
        "runtime",
    }:
        raise CalibrationError("calibration source fields changed")
    revision = sources.get("implementation_revision")
    if (
        not isinstance(revision, str)
        or len(revision) != 40
        or any(c not in "0123456789abcdef" for c in revision)
    ):
        raise CalibrationError("calibration revision is malformed")
    if (sources.get("manifest") is None) is not (sources.get("runtime") is None):
        raise CalibrationError("manifest and runtime preflight must appear together")
    manifest = sources.get("manifest")
    if manifest is not None:
        if not isinstance(manifest, list) or not isinstance(sources.get("runtime"), dict):
            raise CalibrationError("manifest or runtime preflight is malformed")
        for row in cast(list[object], manifest):
            if (
                not isinstance(row, dict)
                or set(row) != {"path", "git_blob", "sha256"}
                or not isinstance(row.get("path"), str)
                or Path(cast(str, row["path"])).is_absolute()
                or ".." in Path(cast(str, row["path"])).parts
                or not _digest(row.get("git_blob"), length=40)
                or not _digest(row.get("sha256"))
            ):
                raise CalibrationError("source manifest row is malformed")
    invocation = document.get("invocation")
    if not isinstance(invocation, dict) or set(invocation) != {
        "started_utc",
        "monotonic_origin",
        "host",
        "platform",
        "run_order",
        "cache_observation",
        "background_load",
        "identity",
    }:
        raise CalibrationError("calibration invocation fields changed")
    if (
        not isinstance(invocation.get("started_utc"), str)
        or not isinstance(invocation.get("host"), str)
        or not isinstance(invocation.get("platform"), str)
        or type(invocation.get("run_order")) is not int
        or cast(int, invocation["run_order"]) < 1
        or not isinstance(invocation.get("cache_observation"), str)
        or not cast(str, invocation["cache_observation"]).strip()
        or not isinstance(invocation.get("background_load"), str)
        or not cast(str, invocation["background_load"]).strip()
        or not isinstance(invocation.get("identity"), dict)
    ):
        raise CalibrationError("calibration invocation metadata is malformed")
    _finite_nonnegative(invocation.get("monotonic_origin"), "monotonic origin", optional=False)
    settings = document.get("settings")
    if not isinstance(settings, dict) or set(settings) != {
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
    }:
        raise CalibrationError("calibration settings changed or are malformed")
    requested = settings["requested_workers"]
    calibration_seconds = settings["calibration_seconds"]
    external_seconds = settings["external_seconds"]
    grace_seconds = settings["termination_grace_seconds"]
    if (
        type(requested) is not int
        or not 1 <= requested <= MAX_WORKERS
        or not all(
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(value)
            for value in (calibration_seconds, external_seconds, grace_seconds)
        )
        or not 0 < calibration_seconds <= external_seconds
        or grace_seconds <= 0
        or settings
        != _settings(
            workers=requested,
            calibration_seconds=cast(float, calibration_seconds),
            external_seconds=cast(float, external_seconds),
            grace_seconds=cast(float, grace_seconds),
        )
    ):
        raise CalibrationError("worker or deadline settings are malformed")
    expected_identity = _invocation_identity(
        cast(str, revision),
        workers=cast(int, requested),
        calibration_seconds=cast(float, calibration_seconds),
        external_seconds=cast(float, external_seconds),
        grace_seconds=cast(float, grace_seconds),
        invocation_started=cast(float, invocation["monotonic_origin"]),
        run_order=cast(int, invocation["run_order"]),
        cache_observation=cast(str, invocation["cache_observation"]),
        background_load=cast(str, invocation["background_load"]),
    )
    if invocation.get("identity") != expected_identity:
        raise CalibrationError("calibration invocation identity changed")
    clocks = document.get("clocks")
    if (
        not isinstance(clocks, dict)
        or set(clocks)
        != {
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
        }
        or clocks.get("phase_duration_scope") != PHASE_DURATION_SCOPE
    ):
        raise CalibrationError("calibration clock fields changed")
    for key, value in clocks.items():
        if key != "phase_duration_scope":
            _finite_nonnegative(value, f"clock {key}")
    resources = document.get("resources")
    if (
        not isinstance(resources, dict)
        or set(resources)
        != {
            "cpu_scope",
            "cpu_observations",
            "coordinator_process_seconds",
            "reaped_direct_children_user_seconds",
            "reaped_direct_children_system_seconds",
            "rss",
            "worker_topology",
        }
        or resources.get("cpu_scope") != CPU_SCOPE
    ):
        raise CalibrationError("calibration resource fields changed")
    for key in (
        "coordinator_process_seconds",
        "reaped_direct_children_user_seconds",
        "reaped_direct_children_system_seconds",
    ):
        _finite_nonnegative(resources.get(key), f"resource {key}")
    cpu_observations = resources.get("cpu_observations")
    if cpu_observations is not None:
        if not isinstance(cpu_observations, dict) or set(cpu_observations) != {
            "coordinator_start_seconds",
            "coordinator_end_seconds",
            "direct_children_user_start_seconds",
            "direct_children_user_end_seconds",
            "direct_children_system_start_seconds",
            "direct_children_system_end_seconds",
        }:
            raise CalibrationError("CPU observation fields changed")
        for key, value in cpu_observations.items():
            _finite_nonnegative(value, f"CPU observation {key}", optional=False)
    if status == "complete":
        if cpu_observations is None or any(
            resources.get(key) is None
            for key in (
                "coordinator_process_seconds",
                "reaped_direct_children_user_seconds",
                "reaped_direct_children_system_seconds",
            )
        ):
            raise CalibrationError("terminal calibration lacks CPU observations")
        rss_summary = resources.get("rss")
        sample_count = (
            rss_summary.get("sample_count") if isinstance(rss_summary, dict) else None
        )
        positive_sample_count = (
            rss_summary.get("positive_sample_count") if isinstance(rss_summary, dict) else None
        )
        if (
            not isinstance(rss_summary, dict)
            or type(sample_count) is not int
            or cast(int, sample_count) < MINIMUM_TERMINAL_RSS_SAMPLES
            or type(positive_sample_count) is not int
            or cast(int, positive_sample_count) < MINIMUM_TERMINAL_RSS_SAMPLES
        ):
            raise CalibrationError("terminal calibration lacks minimum RSS coverage")
    raw = document.get("raw")
    if (
        not isinstance(raw, dict)
        or set(raw)
        != {
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
        }
        or raw.get("directions_expected") != RAW_DIRECTIONS
    ):
        raise CalibrationError("calibration raw fields changed")
    completed = raw.get("directions_completed")
    completed_directions = raw.get("completed_directions")
    if (
        type(completed) is not int
        or not 0 <= cast(int, completed) <= RAW_DIRECTIONS
        or not isinstance(completed_directions, list)
        or len(completed_directions) != completed
        or any(type(index) is not int for index in completed_directions)
        or completed_directions != sorted(set(cast(list[int], completed_directions)))
    ):
        raise CalibrationError("raw completed direction set is malformed")
    if raw.get("budget") != str(RAW_BUDGET) or raw.get("threshold_M_over_n") != str(
        RAW_THRESHOLD
    ):
        raise CalibrationError("raw budget declaration changed")
    if raw.get("observed_minimum_upper_bound") is not None and (
        not _canonical_rational_text(raw.get("observed_minimum_upper_bound"))
        or type(raw.get("observed_argmin")) is not int
        or not _rational_point(raw.get("observed_witness"))
    ):
        raise CalibrationError("raw progress summary is malformed")
    if raw.get("raw_minimum") is not None and (
        completed != RAW_DIRECTIONS
        or completed_directions != list(range(RAW_DIRECTIONS))
        or raw.get("raw_minimum") != str(RAW_MINIMUM)
        or raw.get("comparison") != "passed"
        or raw.get("witness_replay_charge") != str(RAW_MINIMUM)
        or raw.get("witness_admissible") is not True
        or raw.get("observed_argmin") != 0
        or not _digest(raw.get("directions_sha256"))
    ):
        raise CalibrationError("raw known-answer summary changed")
    normalized = document.get("normalized")
    if normalized is not None and (
        not isinstance(normalized, dict)
        or set(normalized)
        != {
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
        }
        or normalized.get("path") != "candidate.json"
        or not _digest(normalized.get("sha256"))
        or normalized.get("source_fixture_sha256") != FIXTURE_SHA256
        or normalized.get("id") != NORMALIZED_ID
        or normalized.get("alpha") != str(NORMALIZATION_ALPHA)
        or normalized.get("point_mass") != "1/4"
        or normalized.get("threshold_budget") != "3/4"
        or normalized.get("total_budget") != str(NORMALIZED_BUDGET)
        or normalized.get("least_cell_charge") != str(NORMALIZED_MINIMUM)
        or normalized.get("integer_scale") != NORMALIZED_SCALE
        or not isinstance(normalized.get("closed_form_conditions"), list)
    ):
        raise CalibrationError("normalized known-answer summary changed")
    routes = document.get("routes")
    if not isinstance(routes, dict) or set(routes) != {
        "normalized_exact",
        "reflected_interval",
        "dilation",
    }:
        raise CalibrationError("calibration route fields changed")
    for name, receipt in routes.items():
        _validate_route_receipt(name, receipt)
    raw_complete = raw.get("raw_minimum") is not None
    exact_receipt = routes["normalized_exact"]
    interval_receipt = routes["reflected_interval"]
    dilation_receipt = routes["dilation"]
    exact_complete = (
        isinstance(exact_receipt, dict) and exact_receipt.get("status") == "complete"
    )
    interval_complete = (
        isinstance(interval_receipt, dict) and interval_receipt.get("status") == "complete"
    )
    dilation_complete = (
        isinstance(dilation_receipt, dict) and dilation_receipt.get("status") == "complete"
    )
    if normalized is not None and not raw_complete:
        raise CalibrationError("normalization appeared before complete raw coverage")
    if exact_receipt is not None and normalized is None:
        raise CalibrationError("normalized exact route appeared before normalization")
    if interval_receipt is not None and not exact_complete:
        raise CalibrationError("interval route appeared before complete exact readback")
    if dilation_receipt is not None and not interval_complete:
        raise CalibrationError("dilation route appeared before complete interval readback")
    if status == "complete" and not (
        raw_complete
        and normalized is not None
        and exact_complete
        and interval_complete
        and dilation_complete
    ):
        raise CalibrationError("terminal calibration lacks complete known-answer routes")
    if status == "complete":
        _validate_worker_phase_durations(clocks)
    worker_topology = resources.get("worker_topology")
    _validate_worker_topology_summary(
        worker_topology,
        settings,
        required=status == "complete",
    )
    if worker_topology is not None:
        assert isinstance(worker_topology, dict)
        topology_routes = worker_topology["routes"]
        assert isinstance(topology_routes, dict)
        if (topology_routes["raw"] is not None) != raw_complete or (
            topology_routes["normalized_exact"] is not None
        ) != exact_complete:
            raise CalibrationError("worker topology appeared outside a completed route")
    _validate_artifact_receipts(document.get("artifacts"))
    supervision = document.get("supervision")
    if not isinstance(supervision, dict) or set(supervision) != {
        "status",
        "worker_exit_status",
        "process_group_reaped",
        "supervisor_signal",
        "coordinator_pid",
        "coordinator_process_group_id",
    }:
        raise CalibrationError("calibration supervision fields changed")
    if (
        supervision.get("status")
        not in {
            "pending",
            "observed-exit",
            "deadline-before-launch",
            "deadline-terminated",
            "launch-failed",
            "cleanup-failed",
            "supervisor-interrupted",
        }
        or type(supervision.get("process_group_reaped")) is not bool
    ):
        raise CalibrationError("calibration supervision state is malformed")
    exit_status = supervision.get("worker_exit_status")
    if exit_status is not None and type(exit_status) is not int:
        raise CalibrationError("worker exit status is malformed")
    supervisor_signal = supervision.get("supervisor_signal")
    if supervisor_signal is not None and (
        type(supervisor_signal) is not int
        or supervisor_signal not in {signal.SIGHUP, signal.SIGINT, signal.SIGTERM}
        or supervision.get("status") != "supervisor-interrupted"
    ):
        raise CalibrationError("supervisor signal provenance is malformed")
    coordinator_pid = supervision.get("coordinator_pid")
    coordinator_group = supervision.get("coordinator_process_group_id")
    if (coordinator_pid is None) is not (coordinator_group is None) or (
        coordinator_pid is not None
        and (
            type(coordinator_pid) is not int
            or cast(int, coordinator_pid) <= 0
            or coordinator_group != coordinator_pid
        )
    ):
        raise CalibrationError("supervised coordinator identity is malformed")
    if status == "complete" and (
        disposition != "calibration-passed"
        or document.get("phase") != "complete"
        or supervision
        != {
            "status": "observed-exit",
            "worker_exit_status": 0,
            "process_group_reaped": True,
            "supervisor_signal": None,
            "coordinator_pid": coordinator_pid,
            "coordinator_process_group_id": coordinator_pid,
        }
        or coordinator_pid is None
    ):
        raise CalibrationError("complete calibration lacks successful parent supervision")
    if (
        (status == "complete" and disposition != "calibration-passed")
        or (status == "invalid" and disposition != "calibration-refused")
        or (status == "partial" and disposition != "incomplete")
    ):
        raise CalibrationError("calibration status and disposition disagree")
    if disposition == "calibration-passed" and status != "complete":
        raise CalibrationError("calibration pass appeared before terminal supervision")
    if document.get("phase") not in {
        "preflight",
        "raw-sweep",
        "normalized-exact",
        "reflected-interval",
        "dilation-replay",
        "readback",
        "awaiting-worker-exit",
        "complete",
        "timeout",
        "operational-failure",
        "invalid",
        "metrics-refused",
    }:
        raise CalibrationError("calibration phase is malformed")
    if status == "complete" and document.get("error") is not None:
        raise CalibrationError("complete calibration retains an error")
    if document.get("error") is not None and not isinstance(document.get("error"), str):
        raise CalibrationError("calibration error is malformed")


def _artifact_inventory(
    output_dir: Path,
    receipt_bytes: int,
    worker_topology: object,
) -> list[dict[str, object]]:
    roles = [
        ("raw-directions", "raw-directions", True),
        ("normalized-exact-directions", "normalized-exact-directions", True),
        ("normalized-interval-directions", "normalized-interval-directions", True),
        ("dilation-directions", "dilation-directions", True),
        ("normalized-candidate", "candidate.json", False),
        ("generic-dilation-record", "dilation.json", False),
        ("rss-observations", "rss-samples.json", False),
    ]
    if isinstance(worker_topology, dict):
        topology_routes = worker_topology.get("routes")
        if isinstance(topology_routes, dict):
            for name, role in (
                ("raw", "raw-worker-topology"),
                ("normalized_exact", "normalized-exact-worker-topology"),
            ):
                route = topology_routes.get(name)
                if isinstance(route, dict) and isinstance(route.get("record_path"), str):
                    roles.append((role, cast(str, route["record_path"]), False))
    rows: list[dict[str, object]] = []
    for role, relative, directory in roles:
        path = output_dir / relative
        if not path.exists():
            continue
        if (
            path.is_symlink()
            or (directory and not path.is_dir())
            or (not directory and not path.is_file())
        ):
            raise CalibrationError(f"retained artifact has the wrong type: {relative}")
        files = (
            tuple(item for item in path.iterdir() if item.is_file() and not item.is_symlink())
            if directory
            else (path,)
        )
        rows.append(
            {
                "role": role,
                "path": relative,
                "count": len(files),
                "bytes": sum(item.stat().st_size for item in files),
            }
        )
    rows.append(
        {
            "role": "calibration-receipt",
            "path": "result.json",
            "count": 1,
            "bytes": receipt_bytes,
        }
    )
    return rows


def _serialized_document(output_dir: Path, document: dict[str, object]) -> str:
    size = 0
    for _attempt in range(8):
        document["artifacts"] = _artifact_inventory(
            output_dir,
            size,
            cast(dict[str, object], document["resources"])["worker_topology"],
        )
        encoded = json.dumps(document, indent=2, allow_nan=False) + "\n"
        next_size = len(encoded.encode())
        if next_size == size:
            return encoded
        size = next_size
    raise CalibrationError("receipt byte-size inventory did not reach a fixed point")


def write_result(output_dir: Path, document: dict[str, object]) -> None:
    """Validate and atomically publish one calibration-only checkpoint."""

    validate_document(document)
    encoded = _serialized_document(output_dir, document)
    validate_document(_strict_json_bytes(encoded.encode(), "calibration receipt"))
    atomic_write_text(output_dir / "result.json", encoded)


def _stage_result(output_dir: Path, document: dict[str, object]) -> Path:
    """Prepare validated terminal bytes without replacing the partial receipt."""

    validate_document(document)
    encoded = _serialized_document(output_dir, document)
    validate_document(_strict_json_bytes(encoded.encode(), "calibration receipt"))
    descriptor, temporary = tempfile.mkstemp(
        dir=output_dir,
        prefix=".result-admission-",
        suffix=".json",
    )
    stream = None
    try:
        path = Path(temporary)
        stream = os.fdopen(descriptor, "w", encoding="utf-8")
        descriptor = -1
        with stream:
            stream.write(encoded)
            stream.flush()
    except BaseException:
        if descriptor >= 0:
            with suppress(OSError):
                os.close(descriptor)
        if stream is not None:
            with suppress(OSError):
                stream.close()
        with suppress(OSError):
            Path(temporary).unlink()
        raise
    return path


def _promote_staged_result(staged: Path, destination: Path) -> None:
    """Perform the single operating-system boundary for terminal publication."""

    staged.replace(destination)


def _routes(document: dict[str, object]) -> dict[str, object]:
    return cast(dict[str, object], document["routes"])


def _clocks(document: dict[str, object]) -> dict[str, object]:
    return cast(dict[str, object], document["clocks"])


def _update_worker_elapsed(document: dict[str, object], started: float, clock: Clock) -> None:
    _clocks(document)["worker_elapsed_seconds"] = clock() - started


def execute_calibration(
    certificate: ThresholdCertificate,
    source_record: dict[str, object],
    *,
    document: dict[str, object],
    output_dir: Path,
    workers: int,
    deadline: float,
    invocation_started: float,
    clock: Clock = time.perf_counter,
    kernels: RouteKernels = REAL_KERNELS,
) -> dict[str, object]:
    """Run all four generic routes and publish calibration-only checkpoints."""

    effective_workers = cast(
        dict[str, int], cast(dict[str, object], document["settings"])["effective_workers"]
    )
    raw_observations: list[WorkerTaskObservation] = []
    exact_observations: list[WorkerTaskObservation] = []

    def publish() -> None:
        _update_worker_elapsed(document, invocation_started, clock)
        write_result(output_dir, document)

    try:
        document.update(
            {
                "phase": "raw-sweep",
                "error": "raw sweep is incomplete",
            }
        )
        publish()
        _expired(deadline, clock, "before raw sweep")
        raw_started = clock()

        def raw_progress(
            completed: int,
            completed_directions: tuple[int, ...],
            observed: Fraction,
            argmin: int,
            witness: Point,
        ) -> None:
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
            publish()

        raw_observers: dict[str, object] = {}
        if kernels.raw is run_raw_sweep:
            raw_observers = {
                "task_observer": raw_observations.append,
            }
        raw_result = kernels.raw(
            certificate,
            workers=workers,
            deadline=deadline,
            clock=clock,
            progress=raw_progress,
            log=output_dir / "raw-directions",
            **raw_observers,
        )
        if raw_result.completed != RAW_DIRECTIONS:
            _refuse("raw kernel returned an incomplete global minimum")
        retained_raw = _check_raw_rows(
            output_dir / "raw-directions", certificate, expected=RAW_DIRECTIONS
        )
        if raw_result != retained_raw or raw_result.direction != 0:
            _refuse("raw kernel summary differs from per-direction readback")
        replayed, admissible = replay_raw_witness(certificate, raw_result)
        raw = cast(dict[str, object], document["raw"])
        raw.update(
            {
                "directions_completed": RAW_DIRECTIONS,
                "completed_directions": list(range(RAW_DIRECTIONS)),
                "observed_minimum_upper_bound": str(raw_result.minimum),
                "observed_argmin": raw_result.direction,
                "observed_witness": [
                    str(raw_result.witness[0]),
                    str(raw_result.witness[1]),
                ],
                "raw_minimum": str(raw_result.minimum),
                "comparison": raw_decision(raw_result.minimum),
                "witness_replay_charge": str(replayed),
                "witness_admissible": admissible,
                "directions_sha256": _direction_digest(
                    tuple(
                        output_dir / "raw-directions" / f"{index}.json"
                        for index in range(RAW_DIRECTIONS)
                    )
                ),
            }
        )
        cast(dict[str, object], document["resources"])["worker_topology"] = (
            _write_worker_topology(
                output_dir,
                invocation_started=invocation_started,
                configured_workers=effective_workers,
                raw_observations=raw_observations,
                exact_observations=None,
            )
        )
        _clocks(document)["raw_seconds"] = clock() - raw_started
        publish()
        if raw_decision(raw_result.minimum) != "passed":
            _refuse("raw minimum did not strictly exceed M/n")

        normalization_started = clock()
        candidate = normalized_bytes(source_record)
        candidate_path = output_dir / "candidate.json"
        atomic_write_text(candidate_path, candidate.decode())
        candidate_sha = hashlib.sha256(candidate).hexdigest()
        normalized, _normalized_record_readback = load_normalized(candidate_path.read_bytes())
        closed_form = [
            {"name": report.name, "detail": report.detail, "holds": report.holds}
            for report in closed_form_threshold_conditions(normalized)
        ]
        document["normalized"] = {
            "path": "candidate.json",
            "sha256": candidate_sha,
            "source_fixture_sha256": FIXTURE_SHA256,
            "id": NORMALIZED_ID,
            "alpha": str(NORMALIZATION_ALPHA),
            "point_mass": "1/4",
            "threshold_budget": "3/4",
            "total_budget": str(NORMALIZED_BUDGET),
            "least_cell_charge": str(NORMALIZED_MINIMUM),
            "integer_scale": NORMALIZED_SCALE,
            "closed_form_conditions": closed_form,
        }
        document["phase"] = "normalized-exact"
        document["error"] = "normalized exact route is incomplete"
        _clocks(document)["normalization_publication_seconds"] = clock() - normalization_started
        publish()
        _expired(deadline, clock, "before normalized exact route")
        exact_started = clock()

        def exact_progress(
            completed: int,
            completed_directions: tuple[int, ...],
            observed: Fraction,
            argmin: int,
            witness: Point,
        ) -> None:
            if completed == RAW_DIRECTIONS:
                return
            _routes(document)["normalized_exact"] = {
                "status": "partial",
                "source_sha256": candidate_sha,
                "directions_expected": RAW_DIRECTIONS,
                "directions_completed": completed,
                "completed_directions": list(completed_directions),
                "observed_minimum_upper_bound": str(observed),
                "argmin": argmin,
                "witness": [str(witness[0]), str(witness[1])],
            }
            publish()

        exact_observers: dict[str, object] = {}
        if kernels.exact is run_exact_route:
            exact_observers = {
                "task_observer": exact_observations.append,
            }
        exact = kernels.exact(
            normalized,
            workers=workers,
            deadline=deadline,
            clock=clock,
            progress=exact_progress,
            log=output_dir / "normalized-exact-directions",
            **exact_observers,
        )
        if exact.completed != RAW_DIRECTIONS:
            _refuse("normalized exact kernel returned incomplete")
        retained_exact = _check_exact_rows(
            output_dir / "normalized-exact-directions",
            normalized,
            expected=RAW_DIRECTIONS,
        )
        if exact != retained_exact or exact.direction != 0 or exact.disagreements != 0:
            _refuse("normalized exact summary differs from known answers")
        _routes(document)["normalized_exact"] = {
            "status": "complete",
            "source_sha256": candidate_sha,
            "directions_expected": RAW_DIRECTIONS,
            "directions_completed": RAW_DIRECTIONS,
            "completed_directions": list(range(RAW_DIRECTIONS)),
            "minimum": str(NORMALIZED_MINIMUM),
            "argmin": 0,
            "witness": [str(exact.witness[0]), str(exact.witness[1])],
            "dense_slab_disagreements": 0,
            "directions_sha256": _direction_digest(
                tuple(
                    output_dir / "normalized-exact-directions" / f"{index}.json"
                    for index in range(RAW_DIRECTIONS)
                )
            ),
        }
        cast(dict[str, object], document["resources"])["worker_topology"] = (
            _write_worker_topology(
                output_dir,
                invocation_started=invocation_started,
                configured_workers=effective_workers,
                raw_observations=raw_observations,
                exact_observations=exact_observations,
            )
        )
        _clocks(document)["exact_seconds"] = clock() - exact_started
        document["phase"] = "reflected-interval"
        document["error"] = "reflected interval route is incomplete"
        publish()
        _expired(deadline, clock, "before reflected interval route")
        interval_started = clock()
        interval_completed: set[str] = set()

        def interval_progress(outcome: object) -> None:
            row = _interval_row(cast(Any, outcome))
            label = cast(str, row["label"])
            interval_completed.add(label)
            _routes(document)["reflected_interval"] = {
                "status": "partial",
                "source_sha256": candidate_sha,
                "directions_expected": INTERVAL_DIRECTIONS,
                "directions_completed": len(interval_completed),
                "completed_directions": _ordered_labels(interval_completed),
                "last": row,
            }
            publish()

        interval = kernels.interval(
            normalized,
            workers=workers,
            deadline=deadline,
            clock=clock,
            progress=interval_progress,
            log=output_dir / "normalized-interval-directions",
        )
        labels = _interval_labels()
        if interval.completed != INTERVAL_DIRECTIONS:
            _refuse("reflected interval kernel returned incomplete")
        retained_interval, interval_boxes = _check_interval_rows(
            output_dir / "normalized-interval-directions",
            normalized,
            labels=labels,
        )
        if (
            interval.lower != NORMALIZED_MINIMUM
            or interval.upper != NORMALIZED_MINIMUM
            or interval.completed != retained_interval.completed
            or interval.stalled != 0
            or interval.budget_exhausted != 0
            or not interval.accepted
        ):
            _refuse("reflected interval summary differs from known answers")
        _routes(document)["reflected_interval"] = {
            "status": "complete",
            "source_sha256": candidate_sha,
            "directions_expected": INTERVAL_DIRECTIONS,
            "directions_completed": INTERVAL_DIRECTIONS,
            "completed_directions": list(labels),
            "integer_scale": NORMALIZED_SCALE,
            "integer_enclosure": [EXPECTED_INTERVAL_BOUND, EXPECTED_INTERVAL_BOUND],
            "enclosure": [str(NORMALIZED_MINIMUM), str(NORMALIZED_MINIMUM)],
            "stalled": 0,
            "budget_exhausted": 0,
            "accepted": True,
            "boxes_observed": interval_boxes,
            "directions_sha256": _direction_digest(
                tuple(
                    output_dir / "normalized-interval-directions" / f"{label}.json"
                    for label in labels
                )
            ),
        }
        _clocks(document)["interval_seconds"] = clock() - interval_started
        document["phase"] = "dilation-replay"
        document["error"] = "dilation replay is incomplete"
        publish()
        _expired(deadline, clock, "before dilation replay")
        dilation_started = clock()
        dilation_completed: set[str] = set()

        def dilation_progress(index: int, minimum: Fraction, label: str) -> None:
            row: dict[str, object] = {
                "direction": index,
                "label": label,
                "minimum": str(minimum),
            }
            _write_direction(output_dir / "dilation-directions", index, row)
            dilation_completed.add(label)
            _routes(document)["dilation"] = {
                "status": "partial",
                "source_sha256": candidate_sha,
                "directions_expected": RAW_DIRECTIONS,
                "directions_completed": len(dilation_completed),
                "completed_directions": sorted(dilation_completed, key=int),
                "last": row,
            }
            publish()
            _expired(deadline, clock, "during dilation replay")

        dilation = kernels.dilation(
            candidate_path,
            workers=workers,
            deadline=deadline,
            clock=clock,
            progress=dilation_progress,
        )
        if candidate_path.read_bytes() != candidate:
            _refuse("normalized candidate changed during dilation replay")
        _check_dilation_rows(
            output_dir / "dilation-directions", normalized, expected=RAW_DIRECTIONS
        )
        _check_dilation_record(dilation, normalized, candidate_sha)
        dilation_bytes = (json.dumps(dilation, indent=2, allow_nan=False) + "\n").encode()
        atomic_write_text(output_dir / "dilation.json", dilation_bytes.decode())
        conclusion = cast(dict[str, object], dilation["conclusion"])
        family = cast(dict[str, object], dilation["strict_dilation_family"])
        _routes(document)["dilation"] = {
            "status": "complete",
            "source_sha256": candidate_sha,
            "directions_expected": RAW_DIRECTIONS,
            "directions_completed": RAW_DIRECTIONS,
            "completed_directions": [str(index) for index in range(RAW_DIRECTIONS)],
            "directions_sha256": _direction_digest(
                tuple(
                    output_dir / "dilation-directions" / f"{index}.json"
                    for index in range(RAW_DIRECTIONS)
                )
            ),
            "record_sha256": hashlib.sha256(dilation_bytes).hexdigest(),
            "generic_record_schema": THRESHOLD_LIMIT_RECORD_SCHEMA,
            "generic_record_scope": (
                "valid normalized n=2 calibration fixture; no campaign or fixed-packet evidence"
            ),
            "factor_supremum": family["factor_supremum"],
            "factor_supremum_squared": str(EXPECTED_FACTOR_SQUARED),
            "bounded_side": conclusion["bounded_side"],
            "bounded_side_squared": str(EXPECTED_SIDE_SQUARED),
            "relation": ">=",
            "endpoint_certificate": False,
            "requires_compactness": False,
        }
        _clocks(document)["dilation_seconds"] = clock() - dilation_started
        document.update(
            {
                "phase": "readback",
                "error": "full retained-byte readback has not completed",
            }
        )
        publish()
        return document  # noqa: TRY300
    except ExactReaderDisagreementError as error:
        failure: Exception = CalibrationError(str(error))
    except (CalibrationDeadlineError, PacketDeadlineError) as error:
        document.update(
            {
                "status": "partial",
                "disposition": "incomplete",
                "phase": "timeout",
                "error": str(error),
            }
        )
        publish()
        return document
    except (OSError, CalibrationOperationalError) as error:
        document.update(
            {
                "status": "partial",
                "disposition": "incomplete",
                "phase": "operational-failure",
                "error": str(error),
            }
        )
        publish()
        return document
    except (CalibrationError, PacketError, ValueError, TypeError) as error:
        failure = error
    document.update(
        {
            "status": "invalid",
            "disposition": "calibration-refused",
            "phase": "invalid",
            "error": str(failure),
        }
    )
    publish()
    return document


def _validate_retained_artifact_set(output_dir: Path) -> None:
    allowed = {
        "result.json",
        "candidate.json",
        "dilation.json",
        "rss-samples.json",
        "raw-worker-topology.json",
        "normalized-exact-worker-topology.json",
        "raw-directions",
        "normalized-exact-directions",
        "normalized-interval-directions",
        "dilation-directions",
    }
    entries = {path.name for path in output_dir.iterdir()}
    if not entries.issubset(allowed):
        raise CalibrationError("calibration output contains an unexpected artifact")


def _validate_worker_topology_route(
    name: str,
    value: object,
    *,
    phase: str,
    configured_workers: int,
    directions_expected: int,
    coordinator_pid: int,
    coordinator_group: int,
    required: bool,
    worker_elapsed_seconds: float | None = None,
) -> dict[str, object] | None:
    if value is None:
        if required:
            raise CalibrationError(f"calibration lacks completed {name} worker topology")
        return None
    if not isinstance(value, dict) or set(value) != {
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
    }:
        raise CalibrationError(f"{name} worker topology fields changed")
    integer_fields = (
        "configured_workers",
        "directions_expected",
        "directions_completed",
        "child_tasks_observed",
        "observed_child_count",
        "maximum_simultaneous_children",
    )
    if any(type(value.get(key)) is not int for key in integer_fields):
        raise CalibrationError(f"{name} worker topology counts are malformed")
    if (
        value.get("phase") != phase
        or value.get("configured_workers") != configured_workers
        or value.get("directions_expected") != directions_expected
        or value.get("directions_completed") != directions_expected
    ):
        raise CalibrationError(f"{name} worker topology identity changed")
    children = value.get("children")
    tasks = value.get("tasks")
    if not isinstance(children, list) or not isinstance(tasks, list):
        raise CalibrationError(f"{name} worker topology observations are malformed")
    parsed_tasks: list[dict[str, object]] = []
    for task in cast(list[object], tasks):
        if not isinstance(task, dict) or set(task) != {
            "direction",
            "pid",
            "ppid",
            "pgid",
            "started_seconds",
            "finished_seconds",
        }:
            raise CalibrationError(f"{name} child task fields changed")
        _finite_nonnegative(
            task.get("started_seconds"), f"{name} child task start", optional=False
        )
        _finite_nonnegative(
            task.get("finished_seconds"), f"{name} child task finish", optional=False
        )
        if (
            type(task.get("direction")) is not int
            or not 0 <= cast(int, task["direction"]) < directions_expected
            or type(task.get("pid")) is not int
            or cast(int, task["pid"]) <= 0
            or task.get("ppid") != coordinator_pid
            or task.get("pgid") != coordinator_group
            or cast(float, task["finished_seconds"]) <= cast(float, task["started_seconds"])
            or (
                worker_elapsed_seconds is not None
                and cast(float, task["finished_seconds"]) > worker_elapsed_seconds
            )
        ):
            raise CalibrationError(f"{name} child task is malformed")
        parsed_tasks.append(cast(dict[str, object], task))
    directions = [cast(int, task["direction"]) for task in parsed_tasks]
    if configured_workers > 1 and directions != list(range(directions_expected)):
        raise CalibrationError(f"{name} child tasks do not bind every direction")
    parsed_children: list[dict[str, object]] = []
    for child in cast(list[object], children):
        if not isinstance(child, dict) or set(child) != {
            "role",
            "phase",
            "pid",
            "ppid",
            "pgid",
            "tasks_completed",
            "first_task_started_seconds",
            "last_task_finished_seconds",
        }:
            raise CalibrationError(f"{name} child topology fields changed")
        for key in ("first_task_started_seconds", "last_task_finished_seconds"):
            _finite_nonnegative(child.get(key), f"{name} child {key}", optional=False)
        if (
            child.get("role") != "route-worker"
            or child.get("phase") != phase
            or type(child.get("pid")) is not int
            or cast(int, child["pid"]) <= 0
            or child.get("ppid") != coordinator_pid
            or child.get("pgid") != coordinator_group
            or type(child.get("tasks_completed")) is not int
            or cast(int, child["tasks_completed"]) <= 0
            or cast(float, child["last_task_finished_seconds"])
            < cast(float, child["first_task_started_seconds"])
        ):
            raise CalibrationError(f"{name} child topology is malformed")
        parsed_children.append(cast(dict[str, object], child))
    child_pids = [cast(int, child["pid"]) for child in parsed_children]
    if child_pids != sorted(set(child_pids)):
        raise CalibrationError(f"{name} child identities are duplicated or unordered")
    observed_count = len(parsed_children)
    task_pids = {cast(int, task["pid"]) for task in parsed_tasks}
    maximum_simultaneous = _maximum_simultaneous_children(
        tuple(
            (
                cast(float, task["started_seconds"]),
                cast(float, task["finished_seconds"]),
                cast(int, task["pid"]),
            )
            for task in parsed_tasks
        ),
        phase=name,
    )
    child_tasks = sum(cast(int, child["tasks_completed"]) for child in parsed_children)
    expected_children = [
        {
            "role": "route-worker",
            "phase": phase,
            "pid": pid,
            "ppid": coordinator_pid,
            "pgid": coordinator_group,
            "tasks_completed": len(pid_tasks),
            "first_task_started_seconds": min(
                cast(float, task["started_seconds"]) for task in pid_tasks
            ),
            "last_task_finished_seconds": max(
                cast(float, task["finished_seconds"]) for task in pid_tasks
            ),
        }
        for pid in sorted(task_pids)
        for pid_tasks in ([task for task in parsed_tasks if cast(int, task["pid"]) == pid],)
    ]
    if configured_workers == 1:
        if (
            value.get("execution_model") != "coordinator-serial"
            or children
            or tasks
            or value.get("child_tasks_observed") != 0
            or value.get("observed_child_count") != 0
            or value.get("maximum_simultaneous_children") != 0
        ):
            raise CalibrationError(f"serial {name} topology reported pool execution")
    elif (
        value.get("execution_model") != "process-pool"
        or not parsed_tasks
        or child_tasks != directions_expected
        or value.get("child_tasks_observed") != child_tasks
        or value.get("observed_child_count") != observed_count
        or value.get("maximum_simultaneous_children") != maximum_simultaneous
        or not 1 <= observed_count <= configured_workers
        or not 1 <= maximum_simultaneous <= observed_count
        or set(child_pids) != task_pids
        or parsed_children != expected_children
    ):
        raise CalibrationError(f"{name} topology does not reconstruct from child tasks")
    return {
        "configured_workers": configured_workers,
        "execution_model": value["execution_model"],
        "observed_child_count": observed_count,
        "maximum_simultaneous_children": maximum_simultaneous,
    }


def _validate_worker_topology(
    output_dir: Path,
    resources: dict[str, object],
    settings: dict[str, object],
    supervision: dict[str, object],
    *,
    required_routes: Collection[str],
    require_supervisor_binding: bool,
    expected_directions: dict[str, int] | None = None,
    worker_elapsed_seconds: float | None = None,
) -> None:
    _finite_nonnegative(worker_elapsed_seconds, "worker elapsed topology bound", optional=True)
    summary = resources.get("worker_topology")
    if summary is None and required_routes:
        raise CalibrationError("completed route lacks worker topology")
    _validate_worker_topology_summary(summary, settings, required=False)
    coordinator_summary: dict[str, object] | None = None
    route_summaries: dict[str, object] = {}
    if isinstance(summary, dict):
        coordinator_summary = cast(dict[str, object], summary["coordinator"])
        route_summaries = cast(dict[str, object], summary["routes"])
        if require_supervisor_binding and (
            supervision.get("coordinator_pid") != coordinator_summary["pid"]
            or supervision.get("coordinator_process_group_id") != coordinator_summary["pgid"]
        ):
            raise CalibrationError("worker topology differs from the supervised coordinator")
    configured = settings.get("effective_workers")
    assert isinstance(configured, dict)
    directions = expected_directions or {
        "raw": RAW_DIRECTIONS,
        "normalized_exact": RAW_DIRECTIONS,
    }
    route_tasks: dict[str, list[dict[str, object]]] = {}

    for name, phase, filename in (
        ("raw", "raw-sweep", "raw-worker-topology.json"),
        (
            "normalized_exact",
            "normalized-exact",
            "normalized-exact-worker-topology.json",
        ),
    ):
        route_summary = route_summaries.get(name)
        path = output_dir / filename
        if not path.exists():
            if route_summary is not None or name in required_routes:
                raise CalibrationError(f"calibration lacks retained {name} worker topology")
            continue
        if path.is_symlink() or not path.is_file():
            raise CalibrationError(f"{name} worker topology has the wrong artifact type")
        try:
            raw = path.read_bytes()
        except OSError as error:
            raise CalibrationError(f"{name} worker topology cannot be read") from error
        sidecar = _strict_json_bytes(raw, filename)
        if (
            set(sidecar) != {"schema", "scope", "coordinator", "route"}
            or sidecar.get("schema") != WORKER_TOPOLOGY_ROUTE_SCHEMA
            or sidecar.get("scope") != WORKER_TOPOLOGY_SCOPE
        ):
            raise CalibrationError(f"{name} worker topology uses an unknown schema or scope")
        coordinator = sidecar.get("coordinator")
        if not isinstance(coordinator, dict) or set(coordinator) != {
            "role",
            "pid",
            "ppid",
            "pgid",
        }:
            raise CalibrationError(f"{name} worker topology coordinator fields changed")
        coordinator_pid = coordinator.get("pid")
        coordinator_group = coordinator.get("pgid")
        if (
            coordinator.get("role") != "coordinator"
            or type(coordinator_pid) is not int
            or cast(int, coordinator_pid) <= 0
            or type(coordinator.get("ppid")) is not int
            or cast(int, coordinator["ppid"]) <= 0
            or coordinator_group != coordinator_pid
            or (coordinator_summary is not None and coordinator != coordinator_summary)
        ):
            raise CalibrationError(f"{name} worker topology coordinator is malformed")
        derived = _validate_worker_topology_route(
            name,
            sidecar.get("route"),
            phase=phase,
            configured_workers=cast(int, configured[name]),
            directions_expected=directions[name],
            coordinator_pid=cast(int, coordinator_pid),
            coordinator_group=cast(int, coordinator_group),
            required=True,
            worker_elapsed_seconds=worker_elapsed_seconds,
        )
        assert derived is not None
        if route_summary is None:
            if name in required_routes:
                raise CalibrationError(f"completed {name} topology is not receipt-bound")
            continue
        expected_summary = derived | {
            "record_path": filename,
            "record_sha256": hashlib.sha256(raw).hexdigest(),
        }
        if route_summary != expected_summary:
            raise CalibrationError(f"{name} worker topology summary does not reconstruct")
        route_tasks[name] = cast(
            list[dict[str, object]], cast(dict[str, object], sidecar["route"])["tasks"]
        )
    raw_tasks = route_tasks.get("raw", [])
    exact_tasks = route_tasks.get("normalized_exact", [])
    if (
        raw_tasks
        and exact_tasks
        and max(cast(float, task["finished_seconds"]) for task in raw_tasks)
        > min(cast(float, task["started_seconds"]) for task in exact_tasks)
    ):
        raise CalibrationError("raw tasks finish after normalized exact tasks start")


def _validate_rss_observations(
    output_dir: Path, resources: dict[str, object], *, required: bool
) -> None:
    rss = resources.get("rss")
    path = output_dir / "rss-samples.json"
    if rss is None:
        if required:
            raise CalibrationError("terminal calibration lacks RSS observations")
        return
    if not isinstance(rss, dict) or set(rss) != {
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
    }:
        raise CalibrationError("RSS summary fields changed")
    if (
        rss.get("scope") != RSS_SCOPE
        or rss.get("sample_interval_seconds") != RSS_SAMPLE_SECONDS
        or rss.get("minimum_terminal_samples") != MINIMUM_TERMINAL_RSS_SAMPLES
    ):
        raise CalibrationError("RSS observation scope or interval changed")
    raw = path.read_bytes()
    if (
        rss.get("samples_path") != "rss-samples.json"
        or rss.get("samples_sha256") != hashlib.sha256(raw).hexdigest()
    ):
        raise CalibrationError("RSS observations differ from their byte binding")
    record = _strict_json_bytes(raw, "rss-samples.json")
    if set(record) != {"schema", "samples"} or record.get("schema") != (
        "fixed-core-packet-calibration-rss/v1"
    ):
        raise CalibrationError("RSS observations use an unknown schema")
    samples = record.get("samples")
    if not isinstance(samples, list):
        raise CalibrationError("RSS observations are not a list")
    parsed: list[dict[str, object]] = []
    for sample in cast(list[object], samples):
        if not isinstance(sample, dict) or set(sample) != {
            "elapsed_seconds",
            "phase",
            "pids",
            "rss_bytes",
            "error",
        }:
            raise CalibrationError("RSS sample fields changed")
        _finite_nonnegative(sample.get("elapsed_seconds"), "RSS sample time", optional=False)
        pids = sample.get("pids")
        if (
            not isinstance(sample.get("phase"), str)
            or not isinstance(pids, list)
            or any(type(pid) is not int or pid <= 0 for pid in pids)
            or pids != sorted(set(cast(list[int], pids)))
            or type(sample.get("rss_bytes")) is not int
            or cast(int, sample["rss_bytes"]) < 0
            or (sample.get("error") is not None and not isinstance(sample.get("error"), str))
        ):
            raise CalibrationError("RSS sample is malformed")
        parsed.append(cast(dict[str, object], sample))
    times = [cast(float, row["elapsed_seconds"]) for row in parsed]
    if times != sorted(times):
        raise CalibrationError("RSS sample times are not monotonic")
    gaps = [right - left for left, right in pairwise(times)]
    peak = max(parsed, key=lambda row: cast(int, row["rss_bytes"]), default=None)
    pids = sorted({cast(int, pid) for row in parsed for pid in cast(list[object], row["pids"])})
    by_phase: dict[str, set[int]] = {}
    errors: list[str] = []
    positive_sample_count = 0
    for row in parsed:
        phase = cast(str, row["phase"])
        if phase not in RSS_OBSERVABLE_PHASES:
            raise CalibrationError("RSS sample names an unknown calibration phase")
        by_phase.setdefault(phase, set()).update(cast(list[int], row["pids"]))
        if row["error"] is not None:
            errors.append(cast(str, row["error"]))
        elif cast(list[int], row["pids"]) and cast(int, row["rss_bytes"]) > 0:
            positive_sample_count += 1
    lifetime = rss.get("observation_lifetime_seconds")
    _finite_nonnegative(lifetime, "RSS observation lifetime", optional=False)
    observation_lifetime = cast(float, lifetime)
    if times and times[-1] > observation_lifetime:
        raise CalibrationError("RSS sample occurs after its observation lifetime")
    expected = {
        "scope": RSS_SCOPE,
        "sample_interval_seconds": RSS_SAMPLE_SECONDS,
        "minimum_terminal_samples": MINIMUM_TERMINAL_RSS_SAMPLES,
        "sample_count": len(parsed),
        "positive_sample_count": positive_sample_count,
        "maximum_actual_gap_seconds": max(gaps, default=0.0),
        "observation_lifetime_seconds": observation_lifetime,
        "unobserved_leading_seconds": times[0] if times else observation_lifetime,
        "unobserved_trailing_seconds": (
            observation_lifetime - times[-1] if times else observation_lifetime
        ),
        "peak_sampled_rss_bytes": 0 if peak is None else peak["rss_bytes"],
        "peak_sample_time_seconds": None if peak is None else peak["elapsed_seconds"],
        "observed_pids": pids,
        "pids_by_phase": {
            phase: sorted(phase_pids) for phase, phase_pids in sorted(by_phase.items())
        },
        "observed_phases": sorted(by_phase),
        "unobserved_phases": sorted(set(RSS_OBSERVABLE_PHASES) - set(by_phase)),
        "observer_errors": errors,
        "samples_path": "rss-samples.json",
        "samples_sha256": hashlib.sha256(raw).hexdigest(),
    }
    if rss != expected:
        raise CalibrationError("RSS summary does not reconstruct from retained samples")
    if required and (
        len(parsed) < MINIMUM_TERMINAL_RSS_SAMPLES
        or positive_sample_count < MINIMUM_TERMINAL_RSS_SAMPLES
        or errors
    ):
        raise CalibrationError("RSS metrics admission requires observed, error-free samples")


def _validate_cpu_observations(resources: dict[str, object], *, required: bool) -> None:
    observations = resources.get("cpu_observations")
    values = (
        resources.get("coordinator_process_seconds"),
        resources.get("reaped_direct_children_user_seconds"),
        resources.get("reaped_direct_children_system_seconds"),
    )
    if observations is None:
        if required or any(value is not None for value in values):
            raise CalibrationError("terminal calibration lacks CPU observations")
        return
    if not isinstance(observations, dict) or set(observations) != {
        "coordinator_start_seconds",
        "coordinator_end_seconds",
        "direct_children_user_start_seconds",
        "direct_children_user_end_seconds",
        "direct_children_system_start_seconds",
        "direct_children_system_end_seconds",
    }:
        raise CalibrationError("CPU observation fields changed")
    for key, value in observations.items():
        _finite_nonnegative(value, f"CPU observation {key}", optional=False)
    pairs = (
        ("coordinator_start_seconds", "coordinator_end_seconds", values[0]),
        ("direct_children_user_start_seconds", "direct_children_user_end_seconds", values[1]),
        (
            "direct_children_system_start_seconds",
            "direct_children_system_end_seconds",
            values[2],
        ),
    )
    for start_key, end_key, elapsed in pairs:
        _finite_nonnegative(elapsed, f"CPU elapsed {start_key}", optional=False)
        start = cast(float, observations[start_key])
        end = cast(float, observations[end_key])
        if end < start or not math.isclose(
            end - start, cast(float, elapsed), rel_tol=1e-12, abs_tol=1e-12
        ):
            raise CalibrationError("CPU elapsed values differ from retained observations")


def load_result(
    output_dir: Path,
    *,
    repository: Path,
    expected_revision: str,
    require_supervision: bool = True,
    require_complete_candidate: bool = False,
    expected_invocation: dict[str, object] | None = None,
) -> dict[str, object]:
    """Reconstruct every calibration artifact and known answer from retained bytes."""

    document = _strict_json(output_dir / "result.json")
    validate_document(document)
    if require_supervision and document["status"] != "complete":
        raise CalibrationError("calibration receipt is not terminally admitted")
    if require_complete_candidate and document.get("phase") not in {
        "awaiting-worker-exit",
        "complete",
    }:
        raise CalibrationError("calibration candidate has not completed full readback")
    sources = cast(dict[str, object], document["sources"])
    if sources.get("implementation_revision") != expected_revision:
        raise CalibrationError("calibration revision differs from requested readback")
    invocation = cast(dict[str, object], document["invocation"])
    if expected_invocation is not None and invocation.get("identity") != expected_invocation:
        raise CalibrationError("calibration invocation differs from requested readback")
    if require_supervision and document["status"] == "complete" and expected_invocation is None:
        raise CalibrationError("terminal readback requires an expected invocation identity")
    # The recorded manifest and runtime describe the run and stay in the receipt as its
    # history. Neither is a condition on reading it back, so a later commit,
    # interpreter, lock or host reads the same retained bytes (development.md, Hashes
    # and Repository-Owned Artifacts, 2026-10-03). Only the runtime's shape is checked.
    _validate_runtime_record(sources.get("runtime"))
    fixture_raw = (repository / FIXTURE_PATH).read_bytes()
    fixture, source_record = load_fixture(fixture_raw)
    _validate_retained_artifact_set(output_dir)
    raw_receipt = cast(dict[str, object], document["raw"])
    raw_complete = raw_receipt.get("raw_minimum") is not None
    retained_raw = _reconstruct_raw_directions(
        output_dir / "raw-directions",
        raw_receipt,
        expected=RAW_DIRECTIONS,
        complete=raw_complete,
    )
    if raw_complete:
        checked_raw = _check_raw_rows(
            output_dir / "raw-directions", fixture, expected=RAW_DIRECTIONS
        )
        if retained_raw != checked_raw or checked_raw.direction != 0:
            raise CalibrationError("raw stable argmin differs from the known-answer rows")
        if (
            raw_receipt.get("raw_minimum") != str(RAW_MINIMUM)
            or raw_receipt.get("comparison") != "passed"
            or raw_receipt.get("witness_replay_charge") != str(RAW_MINIMUM)
            or raw_receipt.get("witness_admissible") is not True
        ):
            raise CalibrationError("raw receipt differs from the exact calibration oracle")
    normalized_receipt = document["normalized"]
    candidate_path = output_dir / "candidate.json"
    rebuilt: ThresholdCertificate | None = None
    candidate_sha: str | None = None
    if normalized_receipt is None:
        if candidate_path.exists() or any(
            value is not None for value in _routes(document).values()
        ):
            raise CalibrationError("post-normalization artifacts appeared before normalization")
    else:
        if not isinstance(normalized_receipt, dict) or set(normalized_receipt) != {
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
        }:
            raise CalibrationError("normalized summary fields changed")
        candidate = candidate_path.read_bytes()
        expected = normalized_bytes(source_record)
        candidate_sha = hashlib.sha256(candidate).hexdigest()
        if candidate != expected or normalized_receipt != {
            "path": "candidate.json",
            "sha256": candidate_sha,
            "source_fixture_sha256": FIXTURE_SHA256,
            "id": NORMALIZED_ID,
            "alpha": str(NORMALIZATION_ALPHA),
            "point_mass": "1/4",
            "threshold_budget": "3/4",
            "total_budget": str(NORMALIZED_BUDGET),
            "least_cell_charge": str(NORMALIZED_MINIMUM),
            "integer_scale": NORMALIZED_SCALE,
            "closed_form_conditions": [
                {"name": row.name, "detail": row.detail, "holds": row.holds}
                for row in closed_form_threshold_conditions(load_normalized(candidate)[0])
            ],
        }:
            raise CalibrationError("normalized summary differs from its frozen bytes")
        rebuilt, _record = load_normalized(candidate)
    routes = _routes(document)
    exact_receipt = cast(dict[str, object] | None, routes["normalized_exact"])
    interval_receipt = cast(dict[str, object] | None, routes["reflected_interval"])
    dilation_receipt = cast(dict[str, object] | None, routes["dilation"])
    if rebuilt is not None:
        exact_complete = exact_receipt is not None and exact_receipt.get("status") == "complete"
        reconstructed_exact = _reconstruct_exact_directions(
            output_dir / "normalized-exact-directions",
            exact_receipt,
            expected=RAW_DIRECTIONS,
            complete=exact_complete,
        )
        if exact_complete and exact_receipt is not None:
            checked = _check_exact_rows(
                output_dir / "normalized-exact-directions",
                rebuilt,
                expected=RAW_DIRECTIONS,
            )
            if reconstructed_exact != checked or exact_receipt != {
                "status": "complete",
                "source_sha256": candidate_sha,
                "directions_expected": RAW_DIRECTIONS,
                "directions_completed": RAW_DIRECTIONS,
                "completed_directions": list(range(RAW_DIRECTIONS)),
                "minimum": str(NORMALIZED_MINIMUM),
                "argmin": 0,
                "witness": exact_receipt["witness"],
                "dense_slab_disagreements": 0,
                "directions_sha256": exact_receipt["directions_sha256"],
            }:
                raise CalibrationError("normalized exact receipt differs from known answers")
        labels = _interval_labels()
        interval_complete = (
            interval_receipt is not None and interval_receipt.get("status") == "complete"
        )
        reconstructed_interval = _reconstruct_interval_directions(
            output_dir / "normalized-interval-directions",
            interval_receipt,
            labels=labels,
            scale=NORMALIZED_SCALE,
            complete=interval_complete,
        )
        if interval_complete and interval_receipt is not None:
            checked_interval, boxes = _check_interval_rows(
                output_dir / "normalized-interval-directions", rebuilt, labels=labels
            )
            if (
                reconstructed_interval != checked_interval
                or interval_receipt.get("completed_directions") != list(labels)
                or interval_receipt.get("integer_scale") != NORMALIZED_SCALE
                or interval_receipt.get("integer_enclosure")
                != [EXPECTED_INTERVAL_BOUND, EXPECTED_INTERVAL_BOUND]
                or interval_receipt.get("boxes_observed") != boxes
            ):
                raise CalibrationError("interval receipt differs from known answers")
        dilation_complete = (
            dilation_receipt is not None and dilation_receipt.get("status") == "complete"
        )
        _reconstruct_dilation_directions(
            output_dir / "dilation-directions",
            dilation_receipt,
            labels=tuple(direction.label for direction in rebuilt.directions),
            complete=dilation_complete,
        )
        if dilation_complete and dilation_receipt is not None:
            _check_dilation_rows(
                output_dir / "dilation-directions", rebuilt, expected=RAW_DIRECTIONS
            )
            dilation_raw = (output_dir / "dilation.json").read_bytes()
            dilation = _strict_json_bytes(dilation_raw, "dilation.json")
            _check_dilation_record(dilation, rebuilt, cast(str, candidate_sha))
            if (
                dilation_receipt.get("completed_directions")
                != [str(index) for index in range(RAW_DIRECTIONS)]
                or dilation_receipt.get("record_sha256")
                != hashlib.sha256(dilation_raw).hexdigest()
                or dilation_receipt.get("generic_record_schema")
                != THRESHOLD_LIMIT_RECORD_SCHEMA
                or dilation_receipt.get("generic_record_scope")
                != (
                    "valid normalized n=2 calibration fixture; no campaign or "
                    "fixed-packet evidence"
                )
                or dilation_receipt.get("factor_supremum")
                != cast(dict[str, object], dilation["strict_dilation_family"])[
                    "factor_supremum"
                ]
                or dilation_receipt.get("factor_supremum_squared")
                != cast(dict[str, object], dilation["strict_dilation_family"])[
                    "factor_supremum_squared"
                ]
                or dilation_receipt.get("bounded_side")
                != cast(dict[str, object], dilation["conclusion"])["bounded_side"]
                or dilation_receipt.get("bounded_side_squared")
                != cast(dict[str, object], dilation["conclusion"])["bounded_side_squared"]
                or dilation_receipt.get("relation")
                != cast(dict[str, object], dilation["conclusion"])["relation"]
                or dilation_receipt.get("endpoint_certificate")
                is not cast(dict[str, object], dilation["conclusion"])["endpoint_certificate"]
                or dilation_receipt.get("requires_compactness")
                is not cast(dict[str, object], dilation["proof"])["requires_compactness"]
            ):
                raise CalibrationError("dilation receipt differs from known answers")
    candidate_complete = all(
        isinstance(routes[name], dict)
        and cast(dict[str, object], routes[name]).get("status") == "complete"
        for name in routes
    )
    if (require_complete_candidate or document["status"] == "complete") and not (
        raw_complete and rebuilt is not None and candidate_complete
    ):
        raise CalibrationError("calibration candidate lacks a complete route")
    complete = document["status"] == "complete"
    resources = cast(dict[str, object], document["resources"])
    _validate_cpu_observations(resources, required=complete)
    _validate_rss_observations(
        output_dir,
        resources,
        required=complete,
    )
    required_topology = {"raw"} if raw_complete else set()
    if exact_receipt is not None and exact_receipt.get("status") == "complete":
        required_topology.add("normalized_exact")
    supervision = cast(dict[str, object], document["supervision"])
    _validate_worker_topology(
        output_dir,
        resources,
        cast(dict[str, object], document["settings"]),
        supervision,
        required_routes=required_topology,
        require_supervisor_binding=supervision.get("coordinator_pid") is not None,
        worker_elapsed_seconds=cast(float | None, _clocks(document)["worker_elapsed_seconds"]),
    )
    if document["artifacts"] != _artifact_inventory(
        output_dir,
        (output_dir / "result.json").stat().st_size,
        resources["worker_topology"],
    ):
        raise CalibrationError("artifact inventory does not reconstruct from retained bytes")
    if complete:
        direction_counts = {
            cast(str, row["role"]): cast(int, row["count"])
            for row in cast(list[dict[str, object]], document["artifacts"])
        }
        if (
            direction_counts.get("raw-directions") != RAW_DIRECTIONS
            or direction_counts.get("normalized-exact-directions") != RAW_DIRECTIONS
            or direction_counts.get("normalized-interval-directions") != INTERVAL_DIRECTIONS
            or direction_counts.get("dilation-directions") != RAW_DIRECTIONS
            or sum(
                direction_counts.get(role, 0)
                for role in (
                    "raw-directions",
                    "normalized-exact-directions",
                    "normalized-interval-directions",
                    "dilation-directions",
                )
            )
            != TOTAL_DIRECTION_ROWS
        ):
            raise CalibrationError("terminal artifact inventory does not contain 14,404 rows")
        clocks = _clocks(document)
        required_clocks = (
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
        )
        if any(clocks[key] is None for key in required_clocks):
            raise CalibrationError("terminal calibration lacks a required clock")
        rss = cast(dict[str, object], resources["rss"])
        if rss.get("observation_lifetime_seconds") != clocks["external_lifetime_seconds"]:
            raise CalibrationError("RSS observation lifetime differs from invocation lifetime")
        if cast(float, clocks["worker_elapsed_seconds"]) >= cast(
            float, cast(dict[str, object], document["settings"])["calibration_seconds"]
        ) or (
            cast(float, clocks["external_lifetime_seconds"])
            + cast(float, clocks["terminal_admission_seconds"])
            >= cast(float, cast(dict[str, object], document["settings"])["external_seconds"])
        ):
            raise CalibrationError("terminal calibration exceeded a declared deadline")
    return document


def prepare_output_dir(output_dir: Path, repository: Path) -> Path:
    """Create a fresh output outside the checkout and every tracked source path."""

    resolved = output_dir.resolve()
    repository = repository.resolve()
    if resolved.exists():
        raise CalibrationError("output directory must be fresh")
    if resolved.is_relative_to(repository):
        raise CalibrationError("calibration output must be outside the repository")
    resolved.mkdir(parents=True)
    return resolved


def _receipt_phase(result_path: Path) -> str:
    try:
        document = _strict_json(result_path)
    except PacketError, OSError:
        return "unreadable-checkpoint"
    phase = document.get("phase")
    return phase if isinstance(phase, str) else "unreadable-checkpoint"


def _sample_process_group(
    process_group: int,
    *,
    elapsed: float,
    phase: str,
    timeout_seconds: float,
) -> dict[str, object]:
    try:
        result = subprocess.run(
            ("ps", "-axo", "pid=,pgid=,rss="),
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return {
            "elapsed_seconds": elapsed,
            "phase": phase,
            "pids": [],
            "rss_bytes": 0,
            "error": f"ps observation exceeded {timeout_seconds:g} seconds",
        }
    except OSError as error:
        return {
            "elapsed_seconds": elapsed,
            "phase": phase,
            "pids": [],
            "rss_bytes": 0,
            "error": f"ps launch failed: {error}",
        }
    if result.returncode:
        return {
            "elapsed_seconds": elapsed,
            "phase": phase,
            "pids": [],
            "rss_bytes": 0,
            "error": result.stderr.strip() or f"ps exited {result.returncode}",
        }
    pids: list[int] = []
    rss_kib = 0
    try:
        for line in result.stdout.splitlines():
            pid_text, group_text, rss_text = line.split()
            if int(group_text) == process_group:
                pids.append(int(pid_text))
                rss_kib += int(rss_text)
    except (TypeError, ValueError) as error:
        return {
            "elapsed_seconds": elapsed,
            "phase": phase,
            "pids": [],
            "rss_bytes": 0,
            "error": f"could not parse ps output: {error}",
        }
    return {
        "elapsed_seconds": elapsed,
        "phase": phase,
        "pids": sorted(pids),
        "rss_bytes": rss_kib * 1024,
        "error": None,
    }


def _write_rss_samples(
    output_dir: Path,
    samples: list[dict[str, object]],
    *,
    observation_lifetime: float | None = None,
) -> dict[str, object]:
    path = output_dir / "rss-samples.json"
    encoded = (
        json.dumps(
            {
                "schema": "fixed-core-packet-calibration-rss/v1",
                "samples": samples,
            },
            indent=1,
            allow_nan=False,
        )
        + "\n"
    ).encode()
    atomic_write_text(path, encoded.decode())
    times = [cast(float, sample["elapsed_seconds"]) for sample in samples]
    gaps = [right - left for left, right in pairwise(times)]
    lifetime = max(times, default=0.0) if observation_lifetime is None else observation_lifetime
    peak = max(samples, key=lambda row: cast(int, row["rss_bytes"]), default=None)
    pids = sorted(
        {cast(int, pid) for sample in samples for pid in cast(list[object], sample["pids"])}
    )
    by_phase: dict[str, set[int]] = {}
    errors: list[str] = []
    positive_sample_count = 0
    for sample in samples:
        phase = cast(str, sample["phase"])
        by_phase.setdefault(phase, set()).update(cast(list[int], sample["pids"]))
        if sample["error"] is not None:
            errors.append(cast(str, sample["error"]))
        elif cast(list[int], sample["pids"]) and cast(int, sample["rss_bytes"]) > 0:
            positive_sample_count += 1
    return {
        "scope": RSS_SCOPE,
        "sample_interval_seconds": RSS_SAMPLE_SECONDS,
        "minimum_terminal_samples": MINIMUM_TERMINAL_RSS_SAMPLES,
        "sample_count": len(samples),
        "positive_sample_count": positive_sample_count,
        "maximum_actual_gap_seconds": max(gaps, default=0.0),
        "observation_lifetime_seconds": lifetime,
        "unobserved_leading_seconds": times[0] if times else lifetime,
        "unobserved_trailing_seconds": lifetime - times[-1] if times else lifetime,
        "peak_sampled_rss_bytes": 0 if peak is None else peak["rss_bytes"],
        "peak_sample_time_seconds": None if peak is None else peak["elapsed_seconds"],
        "observed_pids": pids,
        "pids_by_phase": {
            phase: sorted(phase_pids) for phase, phase_pids in sorted(by_phase.items())
        },
        "observed_phases": sorted(by_phase),
        "unobserved_phases": sorted(set(RSS_OBSERVABLE_PHASES) - set(by_phase)),
        "observer_errors": errors,
        "samples_path": "rss-samples.json",
        "samples_sha256": hashlib.sha256(encoded).hexdigest(),
    }


def _group_exists(process_group: int) -> bool:
    # Only ESRCH proves the group is gone. EPERM means it still exists with no member
    # this process may signal: macOS reports it while the last member is exiting and
    # not yet reaped, so the reaper keeps polling to its deadline.
    try:
        os.killpg(process_group, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _reap_process_group(
    process: subprocess.Popen[bytes], *, grace_seconds: float
) -> tuple[int, float]:
    cleanup_started = time.perf_counter()
    if _group_exists(process.pid):
        with suppress(ProcessLookupError, PermissionError):
            os.killpg(process.pid, signal.SIGTERM)
    try:
        status = process.wait(timeout=grace_seconds)
    except subprocess.TimeoutExpired:
        with suppress(ProcessLookupError, PermissionError):
            os.killpg(process.pid, signal.SIGKILL)
        status = process.wait()
    # The leader can exit while a termination-resistant descendant keeps the session
    # alive. Send SIGKILL after the group-wide grace interval in either case.
    if _group_exists(process.pid):
        with suppress(ProcessLookupError, PermissionError):
            os.killpg(process.pid, signal.SIGKILL)
    final_deadline = time.perf_counter() + grace_seconds
    while _group_exists(process.pid) and time.perf_counter() < final_deadline:
        time.sleep(0.01)
    if _group_exists(process.pid):
        raise CalibrationOperationalError("worker process group remained alive after SIGKILL")
    return status, time.perf_counter() - cleanup_started


def _load_receipt_for_supervisor(output_dir: Path) -> dict[str, object] | None:
    try:
        document = _strict_json(output_dir / "result.json")
        validate_document(document)
    except CalibrationError, PacketError, OSError:
        return None
    return document


def _record_supervision(
    output_dir: Path,
    *,
    status: str,
    worker_status: int | None,
    group_reaped: bool,
    samples: list[dict[str, object]],
    launch_seconds: float | None,
    worker_exit_seconds: float | None,
    cleanup_seconds: float,
    external_lifetime: float,
    error: str | None,
    supervisor_signal: int | None = None,
    coordinator_pid: int | None = None,
) -> dict[str, object] | None:
    document = _load_receipt_for_supervisor(output_dir)
    if document is None:
        return None
    rss = _write_rss_samples(output_dir, samples, observation_lifetime=external_lifetime)
    cast(dict[str, object], document["resources"])["rss"] = rss
    clocks = _clocks(document)
    clocks.update(
        {
            "launch_seconds": launch_seconds,
            "worker_exit_seconds": worker_exit_seconds,
            "supervisor_cleanup_seconds": cleanup_seconds,
            "external_lifetime_seconds": external_lifetime,
        }
    )
    cast(dict[str, object], document["supervision"]).update(
        {
            "status": status,
            "worker_exit_status": worker_status,
            "process_group_reaped": group_reaped,
            "supervisor_signal": supervisor_signal,
            "coordinator_pid": coordinator_pid,
            "coordinator_process_group_id": coordinator_pid,
        }
    )
    if error is not None:
        document.update(
            {
                "status": "partial",
                "disposition": "incomplete",
                "phase": "timeout" if status.startswith("deadline") else "operational-failure",
                "error": error,
            }
        )
    write_result(output_dir, document)
    return document


def _parent_readback_command(command: Sequence[str]) -> tuple[str, ...]:
    readback = list(command)
    try:
        worker_flag = readback.index("--worker")
    except ValueError as error:
        raise CalibrationOperationalError(
            "supervised worker command lacks the readback identity arguments"
        ) from error
    readback[worker_flag] = "--readback-only"
    return tuple(readback)


def supervise_worker(  # noqa: PLR0911
    command: Sequence[str],
    output_dir: Path,
    *,
    repository: Path,
    expected_revision: str,
    external_seconds: float,
    grace_seconds: float,
    invocation_started: float,
    external_deadline: float,
    expected_invocation: dict[str, object] | None = None,
) -> int:
    """Sample, terminate, reap, and finally admit one worker process group."""

    command_arguments = tuple(command)
    bindings: tuple[tuple[str, str], ...] = (
        ("--repository", str(repository.resolve())),
        ("--expect-implementation-revision", expected_revision),
    )
    for flag, expected in bindings:
        if flag in command_arguments:
            index = command_arguments.index(flag)
            if index + 1 == len(command_arguments) or command_arguments[index + 1] != expected:
                raise CalibrationError(f"supervised command {flag} differs from its seed")
    if (
        expected_invocation is not None
        and expected_invocation.get("implementation_revision") != expected_revision
    ):
        raise CalibrationError("supervisor revision differs from its invocation identity")

    handled_signals = (signal.SIGTERM, signal.SIGHUP, signal.SIGINT)
    previous_mask = signal.pthread_sigmask(signal.SIG_BLOCK, handled_signals)
    previous_handlers: dict[signal.Signals, Any] = {}
    active_process: subprocess.Popen[bytes] | None = None
    worker_status: int | None = None
    coordinator_pid: int | None = None
    interrupted_signal: int | None = None
    launching = False
    samples: list[dict[str, object]] = []
    launch_seconds: float | None = None
    worker_exit_seconds: float | None = None
    cleanup_seconds = 0.0
    staged_result: Path | None = None
    staging_depth = 0

    def handle_signal(signum: int, _frame: object) -> None:
        nonlocal interrupted_signal
        if interrupted_signal is None:
            interrupted_signal = signum
        if active_process is not None or (not launching and staging_depth == 0):
            raise _SupervisorSignal(signum)

    def raise_if_interrupted() -> None:
        if interrupted_signal is not None:
            raise _SupervisorSignal(interrupted_signal)

    def stage_owned_result(document: dict[str, object]) -> None:
        nonlocal staged_result, staging_depth
        # The mask protects the ordinary single-threaded CLI path. The depth guard also
        # defers Python handler exceptions when another eligible thread receives a
        # process-directed signal while this thread acquires the staging resource.
        staging_mask = signal.pthread_sigmask(signal.SIG_BLOCK, handled_signals)
        staging_depth += 1
        stage_error: BaseException | None = None
        try:
            staged_result = _stage_result(output_dir, document)
        except BaseException as error:  # noqa: BLE001 -- signal provenance takes priority
            stage_error = error
        finally:
            staging_depth -= 1
            signal.pthread_sigmask(signal.SIG_SETMASK, staging_mask)
        raise_if_interrupted()
        if stage_error is not None:
            raise stage_error

    def record_deadline(message: str, *, before_launch: bool = False) -> int:
        _record_supervision(
            output_dir,
            status="deadline-before-launch" if before_launch else "deadline-terminated",
            worker_status=worker_status,
            group_reaped=True,
            samples=samples,
            launch_seconds=launch_seconds,
            worker_exit_seconds=worker_exit_seconds,
            cleanup_seconds=cleanup_seconds,
            external_lifetime=time.perf_counter() - invocation_started,
            error=message,
            coordinator_pid=coordinator_pid,
        )
        return 1

    try:
        for signal_number in handled_signals:
            previous_handlers[signal_number] = signal.signal(signal_number, handle_signal)
        signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
        raise_if_interrupted()
        if time.perf_counter() >= external_deadline:
            return record_deadline(
                (
                    f"worker process group exceeded the {external_seconds:g}-second "
                    "external deadline before launch"
                ),
                before_launch=True,
            )

        launch_started = time.perf_counter()
        launching = True
        try:
            active_process = subprocess.Popen(tuple(command), start_new_session=True)
            coordinator_pid = active_process.pid
        except OSError as launch_error:
            launch_seconds = time.perf_counter() - launch_started
            _record_supervision(
                output_dir,
                status="launch-failed",
                worker_status=None,
                group_reaped=True,
                samples=[],
                launch_seconds=launch_seconds,
                worker_exit_seconds=None,
                cleanup_seconds=0.0,
                external_lifetime=time.perf_counter() - invocation_started,
                error=f"worker process launch failed: {launch_error}",
            )
            raise_if_interrupted()
            return 1
        finally:
            launching = False
        raise_if_interrupted()
        launch_seconds = time.perf_counter() - launch_started
        if time.perf_counter() >= external_deadline:
            worker_status, cleanup_seconds = _reap_process_group(
                active_process, grace_seconds=grace_seconds
            )
            active_process = None
            return record_deadline(
                f"worker process group exceeded the {external_seconds:g}-second deadline"
            )

        timed_out = False
        while active_process.poll() is None:
            now = time.perf_counter()
            remaining = external_deadline - now
            if remaining <= 0:
                timed_out = True
                break
            samples.append(
                _sample_process_group(
                    active_process.pid,
                    elapsed=now - invocation_started,
                    phase=_receipt_phase(output_dir / "result.json"),
                    timeout_seconds=min(RSS_SAMPLE_SECONDS, remaining),
                )
            )
            raise_if_interrupted()
            remaining = external_deadline - time.perf_counter()
            if remaining <= 0:
                timed_out = True
                break
            time.sleep(min(RSS_SAMPLE_SECONDS, remaining))

        exit_observed = time.perf_counter()
        worker_exit_seconds = max(0.0, exit_observed - invocation_started)
        worker_status, cleanup_seconds = _reap_process_group(
            active_process, grace_seconds=grace_seconds
        )
        active_process = None
        if timed_out:
            return record_deadline(
                f"worker process group exceeded the {external_seconds:g}-second deadline"
            )

        document = _record_supervision(
            output_dir,
            status="observed-exit",
            worker_status=worker_status,
            group_reaped=True,
            samples=samples,
            launch_seconds=launch_seconds,
            worker_exit_seconds=worker_exit_seconds,
            cleanup_seconds=cleanup_seconds,
            external_lifetime=time.perf_counter() - invocation_started,
            error=None,
            coordinator_pid=coordinator_pid,
        )
        if document is None:
            return 1
        if worker_status != 0 or document.get("phase") != "awaiting-worker-exit":
            document.update(
                {
                    "status": "partial" if document.get("status") != "invalid" else "invalid",
                    "disposition": (
                        "incomplete"
                        if document.get("status") != "invalid"
                        else "calibration-refused"
                    ),
                    "phase": (
                        "operational-failure"
                        if document.get("status") != "invalid"
                        else "invalid"
                    ),
                    "error": (
                        "worker exited without a complete candidate with status "
                        f"{worker_status}"
                    ),
                }
            )
            write_result(output_dir, document)
            return 2 if document["status"] == "invalid" else 1

        identity = expected_invocation or cast(
            dict[str, object], cast(dict[str, object], document["invocation"])["identity"]
        )
        try:
            readback_command = _parent_readback_command(command)
        except CalibrationOperationalError as error:
            document.update(
                {
                    "status": "partial",
                    "disposition": "incomplete",
                    "phase": "operational-failure",
                    "error": str(error),
                }
            )
            write_result(output_dir, document)
            return 1
        readback_started = time.perf_counter()
        remaining = external_deadline - readback_started
        if remaining <= 0:
            return record_deadline("external deadline reached before parent final readback")
        launching = True
        try:
            active_process = subprocess.Popen(readback_command, start_new_session=True)
        except OSError as readback_launch_error:
            document.update(
                {
                    "status": "partial",
                    "disposition": "incomplete",
                    "phase": "operational-failure",
                    "error": f"parent readback launch failed: {readback_launch_error}",
                }
            )
            write_result(output_dir, document)
            raise_if_interrupted()
            return 1
        finally:
            launching = False
        raise_if_interrupted()
        remaining = external_deadline - time.perf_counter()
        if remaining <= 0:
            _readback_status, readback_cleanup = _reap_process_group(
                active_process, grace_seconds=grace_seconds
            )
            cleanup_seconds += readback_cleanup
            active_process = None
            return record_deadline("external deadline reached during parent final readback")
        try:
            readback_status = active_process.wait(timeout=remaining)
        except subprocess.TimeoutExpired:
            readback_status, readback_cleanup = _reap_process_group(
                active_process, grace_seconds=grace_seconds
            )
            cleanup_seconds += readback_cleanup
            active_process = None
            return record_deadline("external deadline reached during parent final readback")
        _readback_status, readback_cleanup = _reap_process_group(
            active_process, grace_seconds=grace_seconds
        )
        cleanup_seconds += readback_cleanup
        active_process = None
        readback_finished = time.perf_counter()
        if readback_finished >= external_deadline:
            return record_deadline("external deadline reached during parent final readback")
        document = _load_receipt_for_supervisor(output_dir)
        if document is None:
            return 1
        if readback_status != 0:
            invalid = readback_status == 2
            document.update(
                {
                    "status": "invalid" if invalid else "partial",
                    "disposition": "calibration-refused" if invalid else "incomplete",
                    "phase": "invalid" if invalid else "operational-failure",
                    "error": f"parent final readback exited with status {readback_status}",
                }
            )
            write_result(output_dir, document)
            return readback_status if invalid else 1

        clocks = _clocks(document)
        clocks["parent_final_readback_seconds"] = readback_finished - readback_started
        clocks["supervisor_cleanup_seconds"] = cleanup_seconds
        clocks["external_lifetime_seconds"] = readback_finished - invocation_started
        admission_started = readback_finished
        resources = cast(dict[str, object], document["resources"])
        resources["rss"] = _write_rss_samples(
            output_dir,
            samples,
            observation_lifetime=cast(float, clocks["external_lifetime_seconds"]),
        )
        try:
            _validate_worker_phase_durations(clocks)
            _validate_cpu_observations(resources, required=True)
            _validate_rss_observations(output_dir, resources, required=True)
            _validate_worker_topology(
                output_dir,
                resources,
                cast(dict[str, object], document["settings"]),
                cast(dict[str, object], document["supervision"]),
                required_routes={"raw", "normalized_exact"},
                require_supervisor_binding=True,
                worker_elapsed_seconds=cast(float, clocks["worker_elapsed_seconds"]),
            )
        except CalibrationError as error:
            document.update(
                {
                    "status": "invalid",
                    "disposition": "calibration-refused",
                    "phase": "metrics-refused",
                    "error": f"metrics admission refused: {error}",
                }
            )
            write_result(output_dir, document)
            return 2
        if cast(dict[str, object], document["invocation"])["identity"] != identity:
            document.update(
                {
                    "status": "invalid",
                    "disposition": "calibration-refused",
                    "phase": "invalid",
                    "error": "parent final readback observed a different invocation identity",
                }
            )
            write_result(output_dir, document)
            return 2
        clocks["terminal_admission_seconds"] = 0.0
        document.update(
            {
                "status": "complete",
                "disposition": "calibration-passed",
                "phase": "complete",
                "error": None,
            }
        )
        stage_owned_result(document)
        admission_finished = time.perf_counter()
        clocks["terminal_admission_seconds"] = admission_finished - admission_started
        raise_if_interrupted()
        if admission_finished >= external_deadline:
            return record_deadline("external deadline reached during terminal admission")
        assert staged_result is not None
        staged_result.unlink()
        staged_result = None
        stage_owned_result(document)
        raise_if_interrupted()
        if time.perf_counter() >= external_deadline:
            return record_deadline("external deadline reached during terminal serialization")
        assert staged_result is not None
        _promote_staged_result(staged_result, output_dir / "result.json")
        staged_result = None
        if time.perf_counter() >= external_deadline:
            return record_deadline("external deadline reached during terminal publication")
        return 0  # noqa: TRY300 -- every earlier branch records its terminal disposition
    except _SupervisorSignal as error:
        signal.pthread_sigmask(signal.SIG_BLOCK, handled_signals)
        group_reaped = active_process is None and not launching
        if active_process is not None:
            try:
                interrupted_status, interrupted_cleanup = _reap_process_group(
                    active_process, grace_seconds=grace_seconds
                )
                cleanup_seconds += interrupted_cleanup
                if worker_status is None:
                    worker_status = interrupted_status
                group_reaped = True
            except OSError, CalibrationOperationalError:
                group_reaped = False
            active_process = None
        signal_number = signal.Signals(interrupted_signal or error.signum)
        _record_supervision(
            output_dir,
            status="supervisor-interrupted",
            worker_status=worker_status,
            group_reaped=group_reaped,
            samples=samples,
            launch_seconds=launch_seconds,
            worker_exit_seconds=worker_exit_seconds,
            cleanup_seconds=cleanup_seconds,
            external_lifetime=time.perf_counter() - invocation_started,
            error=f"supervisor interrupted by {signal_number.name} ({signal_number.value})",
            supervisor_signal=signal_number.value,
            coordinator_pid=coordinator_pid,
        )
        interrupted_signal = signal_number.value
    except BaseException as error:
        signal.pthread_sigmask(signal.SIG_BLOCK, handled_signals)
        group_reaped = active_process is None and not launching
        if active_process is not None:
            try:
                interrupted_status, interrupted_cleanup = _reap_process_group(
                    active_process, grace_seconds=grace_seconds
                )
                cleanup_seconds += interrupted_cleanup
                if worker_status is None:
                    worker_status = interrupted_status
                group_reaped = True
            except OSError, CalibrationOperationalError:
                group_reaped = False
            active_process = None
        _record_supervision(
            output_dir,
            status="supervisor-interrupted",
            worker_status=worker_status,
            group_reaped=group_reaped,
            samples=samples,
            launch_seconds=launch_seconds,
            worker_exit_seconds=worker_exit_seconds,
            cleanup_seconds=cleanup_seconds,
            external_lifetime=time.perf_counter() - invocation_started,
            error=f"supervisor interrupted by {type(error).__name__}",
            coordinator_pid=coordinator_pid,
        )
        raise
    finally:
        signal.pthread_sigmask(signal.SIG_BLOCK, handled_signals)
        if staged_result is not None:
            staged_result.unlink(missing_ok=True)
        for signal_number, previous_handler in previous_handlers.items():
            signal.signal(signal_number, previous_handler)
        signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)

    if interrupted_signal is not None:
        signal.raise_signal(interrupted_signal)
        return 128 + interrupted_signal
    raise AssertionError("calibration supervisor left its process state without an outcome")


def _record_worker_failure(
    output_dir: Path, *, error: str, elapsed: float, invalid: bool
) -> None:
    document = _load_receipt_for_supervisor(output_dir)
    if document is None:
        return
    _clocks(document)["worker_elapsed_seconds"] = elapsed
    document.update(
        {
            "status": "invalid" if invalid else "partial",
            "disposition": "calibration-refused" if invalid else "incomplete",
            "phase": "invalid" if invalid else "operational-failure",
            "error": error,
        }
    )
    write_result(output_dir, document)


def run_worker(
    repository: Path,
    revision: str,
    output_dir: Path,
    *,
    workers: int,
    calibration_seconds: float,
    external_seconds: float,
    grace_seconds: float,
    invocation_started: float,
    calibration_deadline: float,
    external_deadline: float,
    run_order: int,
    cache_observation: str,
    background_load: str,
) -> int:
    """Run bounded preflight, all routes, and the first full byte readback."""

    preflight_started = time.perf_counter()
    cpu_started = time.process_time()
    children_started = resource.getrusage(resource.RUSAGE_CHILDREN)
    try:
        expected_identity = _invocation_identity(
            revision,
            workers=workers,
            calibration_seconds=calibration_seconds,
            external_seconds=external_seconds,
            grace_seconds=grace_seconds,
            invocation_started=invocation_started,
            run_order=run_order,
            cache_observation=cache_observation,
            background_load=background_load,
        )
        if (
            calibration_deadline != invocation_started + calibration_seconds
            or external_deadline != invocation_started + external_seconds
        ):
            _refuse("worker deadlines differ from its invocation allowances")
        document = _strict_json(output_dir / "result.json")
        validate_document(document)
        if cast(dict[str, object], document["invocation"])["identity"] != expected_identity:
            _refuse("worker arguments differ from the seeded invocation")
        manifest = source_manifest(
            repository,
            revision,
            result_directory=output_dir,
        )
        runtime = runtime_binding()
        source_started = time.perf_counter()
        fixture_raw = (repository / FIXTURE_PATH).read_bytes()
        certificate, source_record = load_fixture(fixture_raw)
        source_seconds = time.perf_counter() - source_started
        cast(dict[str, object], document["sources"]).update(
            {"manifest": manifest, "runtime": runtime}
        )
        _clocks(document).update(
            {
                "preflight_seconds": time.perf_counter() - preflight_started,
                "source_loading_seconds": source_seconds,
            }
        )
        document.update({"phase": "raw-sweep", "error": "raw sweep has not started"})
        write_result(output_dir, document)
        _expired(calibration_deadline, time.perf_counter, "after preflight")
        document = execute_calibration(
            certificate,
            source_record,
            document=document,
            output_dir=output_dir,
            workers=workers,
            deadline=min(calibration_deadline, external_deadline),
            invocation_started=invocation_started,
        )
        if document.get("phase") == "readback":
            readback_started = time.perf_counter()
            load_result(
                output_dir,
                repository=repository,
                expected_revision=revision,
                require_supervision=False,
                expected_invocation=expected_identity,
            )
            _clocks(document)["full_readback_seconds"] = time.perf_counter() - readback_started
            if time.perf_counter() >= calibration_deadline:
                document.update(
                    {
                        "status": "partial",
                        "disposition": "incomplete",
                        "phase": "timeout",
                        "error": "calibration deadline reached during full readback",
                    }
                )
            else:
                document.update(
                    {
                        "phase": "awaiting-worker-exit",
                        "error": "parent has not observed worker exit",
                    }
                )
    except (OSError, CalibrationOperationalError) as error:
        _record_worker_failure(
            output_dir,
            error=f"operational preflight or worker failure: {error}",
            elapsed=time.perf_counter() - invocation_started,
            invalid=False,
        )
        return 1
    except (CalibrationDeadlineError, PacketDeadlineError) as error:
        _record_worker_failure(
            output_dir,
            error=str(error),
            elapsed=time.perf_counter() - invocation_started,
            invalid=False,
        )
        return 1
    except (CalibrationError, PacketError, ValueError, TypeError, ImportError) as error:
        _record_worker_failure(
            output_dir,
            error=str(error),
            elapsed=time.perf_counter() - invocation_started,
            invalid=True,
        )
        return 2
    except Exception as error:  # noqa: BLE001 -- retain an unresolved operational receipt
        _record_worker_failure(
            output_dir,
            error=f"unexpected worker failure: {type(error).__name__}: {error}",
            elapsed=time.perf_counter() - invocation_started,
            invalid=False,
        )
        return 1
    children_finished = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu_finished = time.process_time()
    resources = cast(dict[str, object], document["resources"])
    resources.update(
        {
            "cpu_observations": {
                "coordinator_start_seconds": cpu_started,
                "coordinator_end_seconds": cpu_finished,
                "direct_children_user_start_seconds": children_started.ru_utime,
                "direct_children_user_end_seconds": children_finished.ru_utime,
                "direct_children_system_start_seconds": children_started.ru_stime,
                "direct_children_system_end_seconds": children_finished.ru_stime,
            },
            "coordinator_process_seconds": cpu_finished - cpu_started,
            "reaped_direct_children_user_seconds": (
                children_finished.ru_utime - children_started.ru_utime
            ),
            "reaped_direct_children_system_seconds": (
                children_finished.ru_stime - children_started.ru_stime
            ),
        }
    )
    _update_worker_elapsed(document, invocation_started, time.perf_counter)
    write_result(output_dir, document)
    return (
        0
        if document.get("phase") == "awaiting-worker-exit"
        else (2 if document.get("status") == "invalid" else 1)
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--expect-implementation-revision", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--calibration-seconds", type=float, required=True)
    parser.add_argument("--external-seconds", type=float, required=True)
    parser.add_argument("--grace-seconds", type=float, default=DEFAULT_GRACE_SECONDS)
    parser.add_argument("--run-order", type=int, required=True)
    parser.add_argument("--cache-observation", required=True)
    parser.add_argument("--background-load", required=True)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--readback-only", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--invocation-started-monotonic", type=float, help=argparse.SUPPRESS)
    parser.add_argument("--calibration-deadline-monotonic", type=float, help=argparse.SUPPRESS)
    parser.add_argument("--external-deadline-monotonic", type=float, help=argparse.SUPPRESS)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    invocation_started = time.perf_counter()
    options = _parser().parse_args(argv)
    repository = options.repository.resolve()
    revision = cast(str, options.expect_implementation_revision)
    if len(revision) != 40 or any(c not in "0123456789abcdef" for c in revision):
        raise CalibrationError("expected revision must be 40 lowercase hexadecimal digits")
    if not 1 <= options.workers <= MAX_WORKERS:
        raise CalibrationError(f"workers must be between 1 and {MAX_WORKERS}")
    if not all(
        math.isfinite(value)
        for value in (
            options.calibration_seconds,
            options.external_seconds,
            options.grace_seconds,
        )
    ):
        raise CalibrationError("deadlines and termination grace must be finite")
    if not 0 < options.calibration_seconds <= options.external_seconds:
        raise CalibrationError(
            "calibration deadline must be positive and within the external deadline"
        )
    if options.grace_seconds <= 0:
        raise CalibrationError("termination grace must be positive")
    if options.run_order < 1:
        raise CalibrationError("run order must be positive")
    if not options.cache_observation.strip() or not options.background_load.strip():
        raise CalibrationError("cache observation and background load must be recorded")
    inherited = (
        options.invocation_started_monotonic,
        options.calibration_deadline_monotonic,
        options.external_deadline_monotonic,
    )
    if options.worker and options.readback_only:
        raise CalibrationError("worker and readback modes are mutually exclusive")
    if options.worker or options.readback_only:
        if any(value is None or not math.isfinite(value) for value in inherited):
            raise CalibrationError("child mode requires finite parent deadline attestation")
        inherited_started = cast(float, options.invocation_started_monotonic)
        inherited_calibration = cast(float, options.calibration_deadline_monotonic)
        inherited_external = cast(float, options.external_deadline_monotonic)
        if (
            inherited_calibration != inherited_started + options.calibration_seconds
            or inherited_external != inherited_started + options.external_seconds
        ):
            raise CalibrationError("worker deadlines differ from the parent invocation clock")
        identity = _invocation_identity(
            revision,
            workers=options.workers,
            calibration_seconds=options.calibration_seconds,
            external_seconds=options.external_seconds,
            grace_seconds=options.grace_seconds,
            invocation_started=inherited_started,
            run_order=options.run_order,
            cache_observation=options.cache_observation,
            background_load=options.background_load,
        )
        if options.readback_only:
            try:
                load_result(
                    options.output_dir.resolve(),
                    repository=repository,
                    expected_revision=revision,
                    require_supervision=False,
                    require_complete_candidate=True,
                    expected_invocation=identity,
                )
            except CalibrationError, PacketError, OSError, ValueError, TypeError:
                return 2
            except Exception:  # noqa: BLE001 -- child status preserves operational failure
                return 1
            return 0
        return run_worker(
            repository,
            revision,
            options.output_dir.resolve(),
            workers=options.workers,
            calibration_seconds=options.calibration_seconds,
            external_seconds=options.external_seconds,
            grace_seconds=options.grace_seconds,
            invocation_started=inherited_started,
            calibration_deadline=inherited_calibration,
            external_deadline=inherited_external,
            run_order=options.run_order,
            cache_observation=options.cache_observation,
            background_load=options.background_load,
        )
    if any(value is not None for value in inherited):
        raise CalibrationError("parent invocation cannot accept inherited deadline fields")
    calibration_deadline = invocation_started + options.calibration_seconds
    external_deadline = invocation_started + options.external_seconds
    output = prepare_output_dir(options.output_dir, repository)
    seed = initial_document(
        revision,
        workers=options.workers,
        calibration_seconds=options.calibration_seconds,
        external_seconds=options.external_seconds,
        grace_seconds=options.grace_seconds,
        invocation_started=invocation_started,
        run_order=options.run_order,
        cache_observation=options.cache_observation,
        background_load=options.background_load,
    )
    write_result(output, seed)
    expected_invocation = _invocation_identity(
        revision,
        workers=options.workers,
        calibration_seconds=options.calibration_seconds,
        external_seconds=options.external_seconds,
        grace_seconds=options.grace_seconds,
        invocation_started=invocation_started,
        run_order=options.run_order,
        cache_observation=options.cache_observation,
        background_load=options.background_load,
    )
    command = [
        sys.executable,
        "-m",
        "devtools.calibrate_fixed_core_packet",
        "--worker",
        "--repository",
        str(repository),
        "--expect-implementation-revision",
        revision,
        "--output-dir",
        str(output),
        "--workers",
        str(options.workers),
        "--calibration-seconds",
        str(options.calibration_seconds),
        "--external-seconds",
        str(options.external_seconds),
        "--grace-seconds",
        str(options.grace_seconds),
        "--run-order",
        str(options.run_order),
        "--cache-observation",
        options.cache_observation,
        "--background-load",
        options.background_load,
        "--invocation-started-monotonic",
        repr(invocation_started),
        "--calibration-deadline-monotonic",
        repr(calibration_deadline),
        "--external-deadline-monotonic",
        repr(external_deadline),
    ]
    return supervise_worker(
        command,
        output,
        repository=repository,
        expected_revision=revision,
        external_seconds=options.external_seconds,
        grace_seconds=options.grace_seconds,
        invocation_started=invocation_started,
        external_deadline=external_deadline,
        expected_invocation=expected_invocation,
    )


__all__ = [
    "FIXTURE_ID",
    "FIXTURE_PATH",
    "FIXTURE_SHA256",
    "INTERVAL_DIRECTIONS",
    "RAW_DIRECTIONS",
    "RESULT_SCHEMA",
    "TOTAL_DIRECTION_ROWS",
    "CalibrationDeadlineError",
    "CalibrationError",
    "CalibrationOperationalError",
    "RouteKernels",
    "discover_implementation_paths",
    "execute_calibration",
    "larger_domain_zero_control",
    "load_fixture",
    "load_normalized",
    "load_result",
    "main",
    "normalized_bytes",
    "prepare_output_dir",
    "raw_decision",
    "run_worker",
    "source_manifest",
    "supervise_worker",
    "validate_document",
]


if __name__ == "__main__":
    raise SystemExit(main())
