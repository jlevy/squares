"""Versioned annealing trial records and one admission rule for every consumer."""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum
from functools import cache
from typing import cast

from sqpack.project import configured_project_root
from sqpack.yamlio import safe_load
from workbench_tools.packing_contracts import (
    DEFAULT_VALIDITY_TOLERANCE,
    GeometryIssue,
    PackingContractError,
    check_unit_square_packing,
)

TRIAL_CONTRACT = "packing.squares:AnnealingTrial/v2"
CONFIGURATION_CONTRACT = "packing.squares:AnnealingConfiguration/v2"
SOURCE_CONTRACT = "packing.squares:WorkbenchSource/v1"
REPAIR_CONTRACT = "packing.squares:OverlapRepair/v1"
ATTEMPT_FAILURE_CONTRACT = "packing.squares:AnnealingAttemptFailure/v1"

#: Geometry is admitted under the workbench's one validity contract and nothing looser: the raw
#: and repaired arrangements, the reported overlaps, the fitted origin and the fitted side.
VALIDITY_TOLERANCE = DEFAULT_VALIDITY_TOLERANCE

#: Arithmetic identity, not geometry: a recorded reference side, excess, score or cost must
#: equal the value recomputed from the same inputs, to within float64 rounding at these sizes.
REFERENCE_TOLERANCE = 1e-9


@dataclass(frozen=True, slots=True)
class PackingReference:
    """The canonical retained upper bound against which one trial was scored."""

    n: int
    side: float
    source: str


type ReferenceLookup = Callable[[int], PackingReference]


@cache
def canonical_reference(n: int) -> PackingReference:
    """Read the canonical retained witness side for ``n`` from the configured project."""
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("a canonical reference needs a positive integer n")
    relative = f"witnesses/known-best/n-{n:03d}.yaml"
    path = configured_project_root() / relative
    document: object = safe_load(path.read_text(encoding="utf-8"))
    outer = _mapping(document)
    witness = _mapping(outer.get("witness")) if outer is not None else None
    if witness is None:
        raise ValueError(f"canonical reference {relative} has no witness object")
    witness_n = _record_integer(witness.get("n"))
    side = _reference_number(witness.get("side"))
    if witness_n != n or not math.isfinite(side) or side <= 0:
        raise ValueError(f"canonical reference {relative} has inconsistent n or side")
    return PackingReference(n=n, side=side, source=f"packing/{relative}")


def below_record_side(record: float) -> float:
    """The side under which an admitted arrangement would beat the record, and is refused.

    Squares that pass the contract at tolerance t still fit, shrunk by 2t, without overlap, so
    a side s implies a true packing at s / (1 - 2t). Below `record (1 - 2t) - t` that would be a
    new record, which a float64 benchmark cannot establish: such a trial is refused as
    `below-record` and needs exact verification before any claim.
    """
    return record * (1 - 2 * VALIDITY_TOLERANCE) - VALIDITY_TOLERANCE


def check_success_band(tolerance_pct: float, record: float) -> None:
    """Refuse a success band, in per cent of the record, finer than the validity tolerance."""
    if not math.isfinite(tolerance_pct) or tolerance_pct < 0:
        raise ValueError("success tolerance must be finite and nonnegative")
    if record * tolerance_pct / 100 < VALIDITY_TOLERANCE:
        raise ValueError(
            f"a {tolerance_pct:g}% success band at side {record:g} is finer than the validity "
            f"tolerance {VALIDITY_TOLERANCE:g}, so it would rank arrangements the contract "
            "cannot tell apart"
        )


def gap_closed(n: int, record: float, excess: float) -> float | None:
    """Return the normalized record-to-grid score, or ``None`` for a zero gap."""
    grid = math.ceil(math.sqrt(n))
    gap = (grid / record - 1) * 100
    if gap <= REFERENCE_TOLERANCE:
        return None
    return 1 - excess / gap


@dataclass(frozen=True, slots=True)
class PhysicsLaw:
    """One force law as the page ran it: the pair law or the wall law."""

    rigidity: float
    repulsion: float
    attraction: float
    range: float

    def row(self) -> dict[str, object]:
        return {
            "rigidity": self.rigidity,
            "repulsion": self.repulsion,
            "attraction": self.attraction,
            "range": self.range,
        }


@dataclass(frozen=True, slots=True)
class BeatTiming:
    """The page's beat in seconds, which sets how many physics steps a trajectory takes."""

    dwell: float
    move: float
    correct: float
    settle: float

    def row(self) -> dict[str, object]:
        return {
            "dwell": self.dwell,
            "move": self.move,
            "correct": self.correct,
            "settle": self.settle,
        }


@dataclass(frozen=True, slots=True)
class EffectiveConfiguration:
    """The browser settings actually used after its setters applied their contracts.

    Version 2 adds the pair and wall laws, the beat and the annealed span, so trials run
    before and after a change of the page's defaults are told apart by more than the commit.
    """

    style: str
    mode: str
    seed: int
    inflate: float
    anneal: int
    pair_law: PhysicsLaw
    wall_law: PhysicsLaw
    timing: BeatTiming
    anneal_span: float
    contract: str = CONFIGURATION_CONTRACT

    def row(self) -> dict[str, object]:
        return {
            "contract": self.contract,
            "style": self.style,
            "mode": self.mode,
            "seed": self.seed,
            "inflate": self.inflate,
            "anneal": self.anneal,
            "pair_law": self.pair_law.row(),
            "wall_law": self.wall_law.row(),
            "timing": self.timing.row(),
            "anneal_span": self.anneal_span,
        }


@dataclass(frozen=True, slots=True)
class SourceReceipt:
    """The exact source, generated page, probe, browser, and Python runtime used."""

    commit: str
    dirty: bool
    page: str
    page_sha256: str
    benchmark: str
    browser: str
    browser_version: str
    browser_executable: str
    playwright_version: str
    python_version: str
    platform: str
    viewport_width: int
    viewport_height: int
    contract: str = SOURCE_CONTRACT

    def row(self) -> dict[str, object]:
        return {
            "contract": self.contract,
            "commit": self.commit,
            "dirty": self.dirty,
            "page": self.page,
            "page_sha256": self.page_sha256,
            "benchmark": self.benchmark,
            "browser": self.browser,
            "browser_version": self.browser_version,
            "browser_executable": self.browser_executable,
            "playwright_version": self.playwright_version,
            "python_version": self.python_version,
            "platform": self.platform,
            "viewport": {
                "width": self.viewport_width,
                "height": self.viewport_height,
            },
        }


@dataclass(frozen=True, slots=True)
class RepairReceipt:
    """The bounded translation repair and the work it added after browser physics."""

    sweeps: int
    sweep_limit: int
    converged: bool
    physics_ms: float
    repair_ms: float
    contract: str = REPAIR_CONTRACT

    def row(self) -> dict[str, object]:
        return {
            "contract": self.contract,
            "sweeps": self.sweeps,
            "sweep_limit": self.sweep_limit,
            "converged": self.converged,
            "physics_ms": self.physics_ms,
            "repair_ms": self.repair_ms,
        }


@dataclass(slots=True)
class Trial:
    """One blind run, including its raw and repaired states and execution receipts."""

    n: int
    seed: int
    style: str
    excess: float
    side: float
    record: float
    closed: float | None
    overlap: float
    resolved_side: float
    resolved_closed: float | None
    resolved_overlap: float
    steps: int
    ms: float
    centre: float
    angle: float
    params: dict[str, float | int] | None = field(default_factory=dict)
    poses: tuple[tuple[float, float, float], ...] | None = None
    resolved_poses: tuple[tuple[float, float, float], ...] | None = None
    record_source: str = ""
    configuration: EffectiveConfiguration | None = None
    source: SourceReceipt | None = None
    repair: RepairReceipt | None = None
    contract: str = TRIAL_CONTRACT

    def row(self) -> dict[str, object]:
        """Return the complete versioned wire representation without legacy defaults.

        `raw_valid` and `resolved_valid` say whether the raw and repaired arrangements pass the
        validity contract in their fitted boxes, so no side or excess is written without it.
        They are derived here and never read back: admission rechecks the geometry itself.
        """
        return {
            "contract": self.contract,
            "n": self.n,
            "seed": self.seed,
            "style": self.style,
            "raw_valid": _passes_contract(self.poses, self.side, self.n),
            "excess": self.excess,
            "closed": self.closed,
            "overlap": self.overlap,
            "resolved_valid": _passes_contract(self.resolved_poses, self.resolved_side, self.n),
            "resolved_side": self.resolved_side,
            "resolved_closed": self.resolved_closed,
            "resolved_overlap": self.resolved_overlap,
            "side": self.side,
            "record": self.record,
            "record_source": self.record_source,
            "steps": self.steps,
            "ms": self.ms,
            "centre": self.centre,
            "angle": self.angle,
            "params": self.params,
            "poses": self.poses,
            "resolved_poses": self.resolved_poses,
            "configuration": self.configuration.row() if self.configuration else None,
            "source": self.source.row() if self.source else None,
            "repair": self.repair.row() if self.repair else None,
        }


def admission_reason(  # noqa: PLR0911 - each ordered refusal is part of the wire contract
    trial: Trial, *, reference_for: ReferenceLookup = canonical_reference
) -> str | None:
    """Recheck canonical provenance, exact geometry, and costs before ranking a trial."""
    if trial.contract != TRIAL_CONTRACT:
        return "unsupported-contract"
    if (
        isinstance(trial.n, bool)
        or not isinstance(trial.n, int)
        or trial.n < 1
        or isinstance(trial.seed, bool)
        or not isinstance(trial.seed, int)
        or not 0 <= trial.seed <= 0xFFFF_FFFF
        or isinstance(trial.steps, bool)
        or not isinstance(trial.steps, int)
        or trial.steps < 0
    ):
        return "invalid-configuration"
    metrics = (
        trial.side,
        trial.record,
        trial.excess,
        trial.overlap,
        trial.resolved_side,
        trial.resolved_overlap,
        trial.ms,
        trial.centre,
        trial.angle,
    )
    if not _finite_metrics(metrics, trial.closed, trial.resolved_closed):
        return "nonfinite"
    if (
        trial.record <= 0
        or trial.side <= 0
        or trial.resolved_side <= 0
        or trial.ms < 0
        or trial.resolved_overlap < 0
        or trial.overlap < 0
    ):
        return "invalid-configuration"
    try:
        reference = reference_for(trial.n)
    except FileNotFoundError, OSError, TypeError, ValueError:
        return "reference-unavailable"
    grid = math.ceil(math.sqrt(trial.n))
    if (
        isinstance(reference.n, bool)
        or not isinstance(reference.n, int)
        or reference.n != trial.n
        or not _finite_number(reference.side)
        or reference.side <= 0
        or reference.side > grid + REFERENCE_TOLERANCE
    ):
        return "invalid-reference"
    if trial.record_source != reference.source or not math.isclose(
        trial.record,
        reference.side,
        rel_tol=REFERENCE_TOLERANCE,
        abs_tol=REFERENCE_TOLERANCE,
    ):
        return "reference-mismatch"
    reason = _configuration_reason(trial)
    if reason is not None:
        return reason
    reason = _source_reason(trial.source)
    if reason is not None:
        return reason
    reason = _repair_reason(trial)
    if reason is not None:
        return reason
    if trial.poses is None or trial.resolved_poses is None:
        return "missing-geometry"
    try:
        raw = check_unit_square_packing(
            trial.poses,
            side=trial.side,
            expected_count=trial.n,
            tolerance=VALIDITY_TOLERANCE,
        )
        repaired = check_unit_square_packing(
            trial.resolved_poses,
            side=trial.resolved_side,
            expected_count=trial.n,
            tolerance=VALIDITY_TOLERANCE,
        )
    except PackingContractError, OverflowError, TypeError, ValueError:
        return "malformed-geometry"
    if GeometryIssue.NONFINITE in raw.issues or GeometryIssue.NONFINITE in repaired.issues:
        return "nonfinite-geometry"
    malformed = {GeometryIssue.SHAPE, GeometryIssue.COUNT, GeometryIssue.DIMENSIONS}
    if malformed.intersection(raw.issues) or GeometryIssue.WALL_ESCAPE in raw.issues:
        return "raw-geometry"
    reported_overlap = trial.overlap > VALIDITY_TOLERANCE
    checked_overlap = GeometryIssue.PAIR_OVERLAP in raw.issues
    if reported_overlap != checked_overlap:
        return "inconsistent-raw-overlap"
    if not repaired.passed or trial.resolved_overlap > VALIDITY_TOLERANCE:
        return "invalid-packing"
    if not _fitted_side_agrees(trial.poses, trial.side):
        return "inconsistent-raw-side"
    if not _fitted_side_agrees(trial.resolved_poses, trial.resolved_side):
        return "inconsistent-resolved-side"
    expected_excess = (trial.side / trial.record - 1) * 100
    if not math.isclose(
        trial.excess, expected_excess, rel_tol=REFERENCE_TOLERANCE, abs_tol=REFERENCE_TOLERANCE
    ):
        return "inconsistent-excess"
    if not _score_agrees(trial.closed, gap_closed(trial.n, trial.record, expected_excess)):
        return "inconsistent-score"
    resolved_excess = (trial.resolved_side / trial.record - 1) * 100
    expected_resolved = gap_closed(trial.n, trial.record, resolved_excess)
    if not _score_agrees(trial.resolved_closed, expected_resolved):
        return "inconsistent-score"
    if trial.resolved_side < below_record_side(trial.record):
        return "below-record"
    return None


def partition_trials(
    trials: list[Trial], *, reference_for: ReferenceLookup = canonical_reference
) -> tuple[list[Trial], dict[str, int]]:
    """Count each refused attempt once while retaining the admitted seed order."""
    admitted: list[Trial] = []
    refused: Counter[str] = Counter()
    for trial in trials:
        reason = admission_reason(trial, reference_for=reference_for)
        if reason is None:
            admitted.append(trial)
        else:
            refused[reason] += 1
    return admitted, dict(refused)


def valid(
    trials: list[Trial], *, reference_for: ReferenceLookup = canonical_reference
) -> list[Trial]:
    """Return only canonical, finite, independently checked packing snapshots."""
    return partition_trials(trials, reference_for=reference_for)[0]


class AttemptFailureReason(StrEnum):
    """Why a planned attempt produced no trial record."""

    #: The probe answered with an error, such as a page that carries no pair into this n.
    PROBE_ERROR = "probe-error"
    #: The probe's result could not be read as a trial: a missing, non-finite or mistyped field.
    MALFORMED_RESULT = "malformed-result"
    #: The canonical witness for this n could not be read.
    REFERENCE_UNAVAILABLE = "reference-unavailable"
    #: The browser call itself failed.
    BROWSER_ERROR = "browser-error"


@dataclass(frozen=True, slots=True)
class AttemptFailure:
    """A planned (n, seed) attempt that produced no trial, retained so it is counted."""

    n: int
    seed: int
    style: str
    params: dict[str, float | int]
    reason: str
    detail: str
    source: SourceReceipt | None
    contract: str = ATTEMPT_FAILURE_CONTRACT

    def row(self) -> dict[str, object]:
        return {
            "contract": self.contract,
            "n": self.n,
            "seed": self.seed,
            "style": self.style,
            "params": self.params,
            "reason": self.reason,
            "detail": self.detail,
            "source": self.source.row() if self.source else None,
        }


def attempt_to_json(attempt: Trial | AttemptFailure) -> str:
    """Serialize a trial or a failed attempt as one strict JSON line."""
    return json.dumps(attempt.row(), allow_nan=False, separators=(",", ":"), sort_keys=True)


def attempt_from_json(text: str) -> Trial | AttemptFailure:
    """Parse one benchmark line: a failed attempt by its contract, anything else as a trial."""
    loaded: object = json.loads(text, parse_constant=_reject_json_constant)
    row = _mapping(loaded)
    if row is None:
        raise ValueError("an attempt JSON value must be an object with string keys")
    if row.get("contract") != ATTEMPT_FAILURE_CONTRACT:
        return trial_from_row(row)
    reason = row.get("reason")
    if reason not in {member.value for member in AttemptFailureReason}:
        raise ValueError(f"unsupported attempt failure reason {reason!r}")
    params = _record_params(row.get("params"))
    if params is None or set(row) != {
        "contract",
        "n",
        "seed",
        "style",
        "params",
        "reason",
        "detail",
        "source",
    }:
        raise ValueError("an attempt failure row has unexpected, missing or malformed fields")
    return AttemptFailure(
        n=_required_integer(row["n"], "n"),
        seed=_required_integer(row["seed"], "seed"),
        style=_required_string(row["style"], "style"),
        params=params,
        reason=cast(str, reason),
        detail=_record_string(row["detail"]),
        source=source_receipt_from_row(row["source"]),
    )


def trial_to_json(trial: Trial) -> str:
    """Serialize one trial as strict JSON; non-finite values are never spellable."""
    return json.dumps(trial.row(), allow_nan=False, separators=(",", ":"), sort_keys=True)


def trial_from_json(text: str) -> Trial:
    """Parse one strict JSON trial without accepting JavaScript NaN/Infinity tokens."""
    loaded: object = json.loads(text, parse_constant=_reject_json_constant)
    row = _mapping(loaded)
    if row is None:
        raise ValueError("a trial JSON value must be an object with string keys")
    return trial_from_row(row)


def trial_from_probe(
    value: object,
    *,
    n: int,
    seed: int,
    style: str,
    params: dict[str, float | int],
    source: SourceReceipt,
    reference_for: ReferenceLookup = canonical_reference,
) -> Trial:
    """Adapt the exact browser probe result into the versioned retained contract."""
    row = _mapping(value)
    expected = {
        "configuration",
        "excess",
        "side",
        "record",
        "centre",
        "angle",
        "overlap",
        "poses",
        "resolvedPoses",
        "resolvedSide",
        "resolvedOverlap",
        "repairSweeps",
        "repairSweepLimit",
        "repairConverged",
        "steps",
        "physicsMs",
        "repairMs",
        "ms",
    }
    if row is None or set(row) != expected:
        raise ValueError("browser trial result has unexpected or missing fields")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("trial n must be a positive integer")
    if isinstance(seed, bool) or not isinstance(seed, int) or not 0 <= seed <= 0xFFFF_FFFF:
        raise ValueError("trial seed must fit uint32")
    if style not in {"physics", "bodies"}:
        raise ValueError("trial style is unsupported")
    configuration_row = _mapping(row["configuration"])
    configuration_fields = {
        "style",
        "mode",
        "seed",
        "inflate",
        "anneal",
        "pairLaw",
        "wallLaw",
        "timing",
        "annealSpan",
    }
    if configuration_row is None or set(configuration_row) != configuration_fields:
        raise ValueError("browser effective configuration is malformed")
    configuration = EffectiveConfiguration(
        style=_required_string(configuration_row["style"], "configuration.style"),
        mode=_required_string(configuration_row["mode"], "configuration.mode"),
        seed=_required_integer(configuration_row["seed"], "configuration.seed"),
        inflate=_required_number(configuration_row["inflate"], "configuration.inflate"),
        anneal=_required_integer(configuration_row["anneal"], "configuration.anneal"),
        pair_law=_required_law(configuration_row["pairLaw"], "configuration.pairLaw"),
        wall_law=_required_law(configuration_row["wallLaw"], "configuration.wallLaw"),
        timing=_required_timing(configuration_row["timing"], "configuration.timing"),
        anneal_span=_required_number(
            configuration_row["annealSpan"], "configuration.annealSpan"
        ),
    )
    poses = pose_rows(row["poses"])
    resolved_poses = pose_rows(row["resolvedPoses"])
    if poses is None or resolved_poses is None:
        raise ValueError("browser trial poses must be numeric triples")
    if not all(math.isfinite(value) for pose in (*poses, *resolved_poses) for value in pose):
        raise ValueError("browser trial poses must be finite")
    record = _required_number(row["record"], "record")
    excess = _required_number(row["excess"], "excess")
    resolved_side = _required_number(row["resolvedSide"], "resolvedSide")
    reference = reference_for(n)
    return Trial(
        n=n,
        seed=seed,
        style=style,
        excess=excess,
        side=_required_number(row["side"], "side"),
        record=record,
        closed=gap_closed(n, record, excess),
        overlap=_required_number(row["overlap"], "overlap"),
        resolved_side=resolved_side,
        resolved_closed=gap_closed(n, record, (resolved_side / record - 1) * 100),
        resolved_overlap=_required_number(row["resolvedOverlap"], "resolvedOverlap"),
        steps=_required_integer(row["steps"], "steps"),
        ms=_required_number(row["ms"], "ms"),
        centre=_required_number(row["centre"], "centre"),
        angle=_required_number(row["angle"], "angle"),
        params=dict(params),
        poses=poses,
        resolved_poses=resolved_poses,
        record_source=reference.source,
        configuration=configuration,
        source=source,
        repair=RepairReceipt(
            sweeps=_required_integer(row["repairSweeps"], "repairSweeps"),
            sweep_limit=_required_integer(row["repairSweepLimit"], "repairSweepLimit"),
            converged=_required_bool(row["repairConverged"], "repairConverged"),
            physics_ms=_required_number(row["physicsMs"], "physicsMs"),
            repair_ms=_required_number(row["repairMs"], "repairMs"),
        ),
    )


def trial_from_row(row: dict[str, object]) -> Trial:
    """Read a trial fail-closed; malformed legacy fields remain inspectable but inadmissible."""
    return Trial(
        n=_record_integer(row.get("n")),
        seed=_record_integer(row.get("seed")),
        style=_record_string(row.get("style")),
        excess=_record_number(row.get("excess")),
        side=_record_number(row.get("side")),
        record=_record_number(row.get("record")),
        closed=_optional_record_number(row.get("closed")),
        overlap=_record_number(row.get("overlap")),
        resolved_side=_record_number(row.get("resolved_side")),
        resolved_closed=_optional_record_number(row.get("resolved_closed")),
        resolved_overlap=_record_number(row.get("resolved_overlap")),
        steps=_record_integer(row.get("steps")),
        ms=_record_number(row.get("ms")),
        centre=_record_number(row.get("centre")),
        angle=_record_number(row.get("angle")),
        params=_record_params(row.get("params")),
        poses=pose_rows(row.get("poses")),
        resolved_poses=pose_rows(row.get("resolved_poses")),
        record_source=_record_string(row.get("record_source")),
        configuration=configuration_from_row(row.get("configuration")),
        source=source_receipt_from_row(row.get("source")),
        repair=repair_receipt_from_row(row.get("repair")),
        contract=_record_string(row.get("contract")),
    )


def configuration_from_row(value: object) -> EffectiveConfiguration | None:
    row = _mapping(value)
    if row is None:
        return None
    return EffectiveConfiguration(
        style=_record_string(row.get("style")),
        mode=_record_string(row.get("mode")),
        seed=_record_integer(row.get("seed")),
        inflate=_record_number(row.get("inflate")),
        anneal=_record_integer(row.get("anneal")),
        pair_law=_record_law(row.get("pair_law")),
        wall_law=_record_law(row.get("wall_law")),
        timing=_record_timing(row.get("timing")),
        anneal_span=_record_number(row.get("anneal_span")),
        contract=_record_string(row.get("contract")),
    )


def source_receipt_from_row(value: object) -> SourceReceipt | None:
    row = _mapping(value)
    if row is None:
        return None
    viewport = _mapping(row.get("viewport"))
    return SourceReceipt(
        commit=_record_string(row.get("commit")),
        dirty=_record_bool(row.get("dirty"), invalid=True),
        page=_record_string(row.get("page")),
        page_sha256=_record_string(row.get("page_sha256")),
        benchmark=_record_string(row.get("benchmark")),
        browser=_record_string(row.get("browser")),
        browser_version=_record_string(row.get("browser_version")),
        browser_executable=_record_string(row.get("browser_executable")),
        playwright_version=_record_string(row.get("playwright_version")),
        python_version=_record_string(row.get("python_version")),
        platform=_record_string(row.get("platform")),
        viewport_width=_record_integer(viewport.get("width")) if viewport else -1,
        viewport_height=_record_integer(viewport.get("height")) if viewport else -1,
        contract=_record_string(row.get("contract")),
    )


def repair_receipt_from_row(value: object) -> RepairReceipt | None:
    row = _mapping(value)
    if row is None:
        return None
    return RepairReceipt(
        sweeps=_record_integer(row.get("sweeps")),
        sweep_limit=_record_integer(row.get("sweep_limit")),
        converged=_record_bool(row.get("converged"), invalid=False),
        physics_ms=_record_number(row.get("physics_ms")),
        repair_ms=_record_number(row.get("repair_ms")),
        contract=_record_string(row.get("contract")),
    )


def pose_rows(value: object) -> tuple[tuple[float, float, float], ...] | None:
    """Read canonical lower-left, radian poses without inventing missing geometry."""
    if not isinstance(value, (list, tuple)):
        return None
    poses: list[tuple[float, float, float]] = []
    for row in value:
        if not isinstance(row, (list, tuple)) or len(row) != 3:
            return None
        numbers: list[float] = []
        for number in row:
            if isinstance(number, bool) or not isinstance(number, (int, float)):
                return None
            try:
                numbers.append(float(number))
            except OverflowError, TypeError, ValueError:
                return None
        poses.append((numbers[0], numbers[1], numbers[2]))
    return tuple(poses)


def _configuration_reason(  # noqa: PLR0911 - preserves distinct configuration refusals
    trial: Trial,
) -> str | None:
    configuration = trial.configuration
    if configuration is None:
        return "missing-configuration"
    if configuration.contract != CONFIGURATION_CONTRACT:
        return "unsupported-configuration-contract"
    # The benchmark measures blind runs only. No snapped or guided control is admitted, and
    # none is needed: geometry is checked at the contract tolerance, not a measured one.
    if (
        configuration.style != trial.style
        or configuration.mode != "blind"
        or configuration.seed != trial.seed
        or configuration.style not in {"physics", "bodies"}
        or not _finite_number(configuration.inflate)
        or not 1 <= configuration.inflate <= 2
        or isinstance(configuration.anneal, bool)
        or not isinstance(configuration.anneal, int)
        or not 0 <= configuration.anneal <= 20
        or not _sound_law(configuration.pair_law)
        or not _sound_law(configuration.wall_law)
        or not _sound_timing(configuration.timing)
        or not _finite_number(configuration.anneal_span)
        or configuration.anneal_span <= 0
    ):
        return "invalid-effective-configuration"
    if trial.params is None or set(trial.params) - {"inflate", "anneal"}:
        return "invalid-requested-configuration"
    requested_inflate = trial.params.get("inflate")
    requested_anneal = trial.params.get("anneal")
    if requested_inflate is not None and requested_inflate != configuration.inflate:
        return "configuration-mismatch"
    if requested_anneal is not None and requested_anneal != configuration.anneal:
        return "configuration-mismatch"
    return None


def _source_reason(source: SourceReceipt | None) -> str | None:
    if source is None:
        return "missing-source-receipt"
    if source.contract != SOURCE_CONTRACT:
        return "unsupported-source-contract"
    if (
        not isinstance(source.commit, str)
        or re.fullmatch(r"[0-9a-f]{40}", source.commit) is None
        or source.dirty is not False
    ):
        return "unreproducible-source"
    if (
        not isinstance(source.page, str)
        or not source.page.startswith("packing/")
        or not isinstance(source.page_sha256, str)
        or re.fullmatch(r"[0-9a-f]{64}", source.page_sha256) is None
        or not isinstance(source.benchmark, str)
        or not source.benchmark.startswith("packages/workbench/")
    ):
        return "invalid-source-artifact"
    labels = (
        source.browser,
        source.browser_version,
        source.browser_executable,
        source.playwright_version,
        source.python_version,
        source.platform,
    )
    if (
        any(not isinstance(label, str) or not label.strip() for label in labels)
        or not source.python_version.startswith("3.14.")
        or isinstance(source.viewport_width, bool)
        or not isinstance(source.viewport_width, int)
        or isinstance(source.viewport_height, bool)
        or not isinstance(source.viewport_height, int)
        or source.viewport_width < 1
        or source.viewport_height < 1
    ):
        return "invalid-runtime-receipt"
    return None


def _repair_reason(trial: Trial) -> str | None:
    repair = trial.repair
    if repair is None:
        return "missing-repair-receipt"
    if repair.contract != REPAIR_CONTRACT:
        return "unsupported-repair-contract"
    if (
        isinstance(repair.sweeps, bool)
        or not isinstance(repair.sweeps, int)
        or isinstance(repair.sweep_limit, bool)
        or not isinstance(repair.sweep_limit, int)
        or repair.sweep_limit < 1
        or not 0 <= repair.sweeps <= repair.sweep_limit
        or not _finite_number(repair.physics_ms)
        or not _finite_number(repair.repair_ms)
        or repair.physics_ms < 0
        or repair.repair_ms < 0
        or repair.physics_ms + repair.repair_ms > trial.ms + REFERENCE_TOLERANCE
        or not isinstance(repair.converged, bool)
    ):
        return "invalid-repair-receipt"
    converged = trial.resolved_overlap <= VALIDITY_TOLERANCE
    if repair.converged != converged:
        return "inconsistent-repair-receipt"
    if not repair.converged:
        # The gate on the repair is that it converged under the contract. A repair that hit its
        # sweep limit is refused here, however small its residual, before geometry is checked.
        return "repair-not-converged"
    return None


def _finite_metrics(
    metrics: tuple[float, ...], closed: float | None, resolved_closed: float | None
) -> bool:
    try:
        return all(math.isfinite(value) for value in metrics) and all(
            value is None or math.isfinite(value) for value in (closed, resolved_closed)
        )
    except OverflowError, TypeError, ValueError:
        return False


def _finite_number(value: object) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value)
    except OverflowError, TypeError, ValueError:
        return False


def _score_agrees(actual: float | None, expected: float | None) -> bool:
    if expected is None:
        return actual is None
    return actual is not None and math.isclose(
        actual, expected, rel_tol=REFERENCE_TOLERANCE, abs_tol=REFERENCE_TOLERANCE
    )


def _fitted_side_agrees(poses: tuple[tuple[float, float, float], ...], side: float) -> bool:
    low_x = math.inf
    low_y = math.inf
    high_x = -math.inf
    high_y = -math.inf
    for x, y, angle in poses:
        radius = (abs(math.cos(angle)) + abs(math.sin(angle))) / 2
        low_x = min(low_x, x - radius)
        low_y = min(low_y, y - radius)
        high_x = max(high_x, x + radius)
        high_y = max(high_y, y + radius)
    fitted = max(high_x - low_x, high_y - low_y)
    return (
        math.isclose(low_x, 0, rel_tol=0, abs_tol=VALIDITY_TOLERANCE)
        and math.isclose(low_y, 0, rel_tol=0, abs_tol=VALIDITY_TOLERANCE)
        and math.isclose(side, fitted, rel_tol=REFERENCE_TOLERANCE, abs_tol=VALIDITY_TOLERANCE)
    )


def _mapping(value: object) -> dict[str, object] | None:
    if not isinstance(value, dict):
        return None
    raw = cast(dict[object, object], value)
    if any(not isinstance(key, str) for key in raw):
        return None
    return {cast(str, key): item for key, item in raw.items()}


def _record_number(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return math.nan
    try:
        return float(value)
    except OverflowError, TypeError, ValueError:
        return math.nan


def _reference_number(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        return math.nan
    try:
        return float(value)
    except OverflowError, TypeError, ValueError:
        return math.nan


def _required_number(value: object, label: str) -> float:
    number = _record_number(value)
    if not math.isfinite(number):
        raise ValueError(f"{label} must be a finite number")
    return number


def _required_integer(value: object, label: str) -> int:
    number = _record_integer(value)
    if number < 0:
        raise ValueError(f"{label} must be a non-negative integer")
    return number


def _required_string(value: object, label: str) -> str:
    text = _record_string(value)
    if not text:
        raise ValueError(f"{label} must be a nonempty string")
    return text


def _required_bool(value: object, label: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{label} must be boolean")
    return value


def _optional_record_number(value: object) -> float | None:
    return None if value is None else _record_number(value)


def _record_integer(value: object) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else -1


def _record_string(value: object) -> str:
    return value if isinstance(value, str) else ""


def _record_bool(value: object, *, invalid: bool) -> bool:
    return value if isinstance(value, bool) else invalid


def _record_params(value: object) -> dict[str, float | int] | None:
    row = _mapping(value)
    if row is None:
        return None
    params: dict[str, float | int] = {}
    for key, number in row.items():
        if isinstance(number, bool) or not isinstance(number, (int, float)):
            return None
        try:
            finite = math.isfinite(number)
        except OverflowError, TypeError, ValueError:
            return None
        if not finite:
            return None
        params[key] = number
    return params


def _reject_json_constant(token: str) -> None:
    raise ValueError(f"non-standard JSON number {token!r} is not allowed")


def _passes_contract(
    poses: tuple[tuple[float, float, float], ...] | None, side: float, n: int
) -> bool:
    if poses is None or isinstance(n, bool) or not isinstance(n, int) or n < 1:
        return False
    return check_unit_square_packing(
        poses, side=side, expected_count=n, tolerance=VALIDITY_TOLERANCE
    ).passed


def _record_law(value: object) -> PhysicsLaw:
    row = _mapping(value) or {}
    return PhysicsLaw(
        rigidity=_record_number(row.get("rigidity")),
        repulsion=_record_number(row.get("repulsion")),
        attraction=_record_number(row.get("attraction")),
        range=_record_number(row.get("range")),
    )


def _record_timing(value: object) -> BeatTiming:
    row = _mapping(value) or {}
    return BeatTiming(
        dwell=_record_number(row.get("dwell")),
        move=_record_number(row.get("move")),
        correct=_record_number(row.get("correct")),
        settle=_record_number(row.get("settle")),
    )


def _required_law(value: object, label: str) -> PhysicsLaw:
    row = _mapping(value)
    if row is None or set(row) != {"rigidity", "repulsion", "attraction", "range"}:
        raise ValueError(f"{label} must be a law with exactly its four parameters")
    return PhysicsLaw(
        rigidity=_required_number(row["rigidity"], f"{label}.rigidity"),
        repulsion=_required_number(row["repulsion"], f"{label}.repulsion"),
        attraction=_required_number(row["attraction"], f"{label}.attraction"),
        range=_required_number(row["range"], f"{label}.range"),
    )


def _required_timing(value: object, label: str) -> BeatTiming:
    row = _mapping(value)
    if row is None or set(row) != {"dwell", "move", "correct", "settle"}:
        raise ValueError(f"{label} must be a beat with exactly its four spans")
    return BeatTiming(
        dwell=_required_number(row["dwell"], f"{label}.dwell"),
        move=_required_number(row["move"], f"{label}.move"),
        correct=_required_number(row["correct"], f"{label}.correct"),
        settle=_required_number(row["settle"], f"{label}.settle"),
    )


def _sound_law(law: PhysicsLaw) -> bool:
    values = (law.rigidity, law.repulsion, law.attraction, law.range)
    return all(_finite_number(value) and value >= 0 for value in values) and law.rigidity > 0


def _sound_timing(timing: BeatTiming) -> bool:
    values = (timing.dwell, timing.move, timing.correct, timing.settle)
    return all(_finite_number(value) and value >= 0 for value in values) and timing.move > 0
