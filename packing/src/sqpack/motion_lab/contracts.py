"""Versioned, deterministic data contracts shared by Motion Lab scenarios.

The browser shell should not have to guess whether a frame is exact, numerical, or
illustrative. These small immutable records put that distinction at the transport
boundary. They deliberately use only the standard library so retained artifacts and
loopback services share one representation without introducing a web framework.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, fields, is_dataclass
from enum import StrEnum
from typing import ClassVar

MOTION_LAB_SCHEMA_VERSION = 1
MAX_INTERACTIVE_SQUARES = 20
MAX_QUENCH_SWEEPS = 1_000
MAX_QUENCH_TIME_BUDGET_SECONDS = 300.0


class ScenarioRunner(StrEnum):
    """How a scenario obtains frames for the shared timeline."""

    ANALYTIC = "analytic"
    RECORDED = "recorded"
    INTERACTIVE_SOLVER = "interactive-solver"


class Capability(StrEnum):
    """An operation the shell may expose for a scenario."""

    EDIT_POSE = "edit-pose"
    SETUP_SNAPPING = "setup-snapping"
    RANDOMIZE = "randomize"
    RUN_QUENCH = "run-quench"
    PLAYBACK = "playback"
    SCRUB = "scrub"
    DOWNLOAD_TRACE = "download-trace"


_CAPABILITY_ORDER = {value: index for index, value in enumerate(Capability)}


class FrameKind(StrEnum):
    """Epistemic kind of geometry shown in one visible frame."""

    EDITOR_PREVIEW = "editor-preview"
    EXACT_PATH = "exact-path"
    NUMERICAL_STATE = "numerical-state"
    PROBE = "probe"
    ILLUSTRATIVE_TWEEN = "illustrative-tween"


class OverlayKind(StrEnum):
    """Typed auxiliary geometry that the shared stage may draw."""

    CONTACT = "contact"
    TRAIL = "trail"
    TANGENT = "tangent"
    CELL_AXIS = "cell-axis"
    SELECTION = "selection"


class Phase(StrEnum):
    """Named optimization or analytic phase associated with a frame."""

    SETUP = "setup"
    ANALYTIC_PATH = "analytic-path"
    FIXED_ANGLE_LP = "fixed-angle-lp"
    ANGULAR_PROBE = "angular-probe"
    ANGLE_ACCEPTED = "angle-accepted"
    CELL_CHANGE = "cell-change"
    STOP = "stop"


class EvidenceStatus(StrEnum):
    """Claim boundary carried beside every frame."""

    EDITOR_INPUT = "editor-input"
    ILLUSTRATIVE = "illustrative"
    NUMERICALLY_CHECKED = "numerically-checked"
    EXACT_CERTIFIED_PATH = "exact-certified-path"
    SECOND_ORDER_OBSTRUCTION = "second-order-obstruction"


class SolverKind(StrEnum):
    """Phase 1 numerical runner exposed by the loopback service."""

    QUENCH_BRACKET = "quench-bracket"


class TimelineEventKind(StrEnum):
    """A retained decision or state in an analytic or numerical run."""

    SETUP_RELEASED = "setup-released"
    FIXED_POINT = "fixed-point"
    ANGLE_PROBE = "angle-probe"
    ANGLE_ACCEPTED = "angle-accepted"
    CELL_CHANGED = "cell-changed"
    STOP = "stop"


class ProbeOutcome(StrEnum):
    """Disposition of a numerical probe already made by the solver."""

    EVALUATED = "evaluated"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    UNSETTLED = "unsettled"
    INFEASIBLE = "infeasible"
    BUDGET_CUTOFF = "budget-cutoff"


def _require_text(value: str, name: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_finite(values: tuple[float, ...], name: str) -> None:
    if not all(math.isfinite(value) for value in values):
        raise ValueError(f"{name} must be finite")


def _to_record(value: object) -> object:
    """Convert immutable contract values to JSON primitives in declared field order."""
    if isinstance(value, StrEnum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        output: dict[str, object] = {}
        contract = getattr(value, "CONTRACT", None)
        schema_version = getattr(value, "SCHEMA_VERSION", None)
        if contract is not None:
            output["contract"] = contract
        if schema_version is not None:
            output["schema_version"] = schema_version
        for definition in fields(value):
            item = getattr(value, definition.name)
            if item is not None:
                output[definition.name] = _to_record(item)
        return output
    if isinstance(value, tuple | list):
        return [_to_record(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _to_record(item) for key, item in value.items()}
    return value


class _ContractRecord:
    """Serialization mixin for immutable contract records."""

    def to_record(self) -> dict[str, object]:
        record = _to_record(self)
        if not isinstance(record, dict):
            raise TypeError("contract did not serialize to a record")
        return record


@dataclass(frozen=True)
class Evidence(_ContractRecord):
    """The claim a viewer may draw from one frame."""

    status: EvidenceStatus
    claim: str
    source: str = ""

    def __post_init__(self) -> None:
        _require_text(self.claim, "evidence claim")


@dataclass(frozen=True)
class SquarePose(_ContractRecord):
    """One unit square's center and angle in mathematical coordinates."""

    square_id: int
    x: float
    y: float
    theta: float
    palette_index: int

    def __post_init__(self) -> None:
        if self.square_id < 0:
            raise ValueError("square ID must be non-negative")
        if self.palette_index < 0:
            raise ValueError("palette index must be non-negative")
        _require_finite((self.x, self.y, self.theta), "square pose")


@dataclass(frozen=True)
class FrameOverlay(_ContractRecord):
    """Typed contact, trail, axis, tangent, or selection annotation."""

    kind: OverlayKind
    square_ids: tuple[int, ...] = ()
    points: tuple[tuple[float, float], ...] = ()
    label: str = ""

    def __post_init__(self) -> None:
        if any(square_id < 0 for square_id in self.square_ids):
            raise ValueError("overlay square IDs must be non-negative")
        if tuple(sorted(set(self.square_ids))) != self.square_ids:
            raise ValueError("overlay square IDs must be unique and stable")
        _require_finite(
            tuple(coordinate for point in self.points for coordinate in point),
            "overlay points",
        )


@dataclass(frozen=True)
class PoseFrame(_ContractRecord):
    """The normalized visible geometry consumed by the shared stage."""

    CONTRACT: ClassVar[str] = "packing.squares:MotionLabFrame/v1"
    SCHEMA_VERSION: ClassVar[int] = MOTION_LAB_SCHEMA_VERSION

    scenario_id: str
    frame_kind: FrameKind
    container_side: float
    squares: tuple[SquarePose, ...]
    phase: Phase
    evidence: Evidence
    overlays: tuple[FrameOverlay, ...] = ()

    def __post_init__(self) -> None:
        _require_text(self.scenario_id, "scenario ID")
        if not math.isfinite(self.container_side) or self.container_side <= 0:
            raise ValueError("container side must be finite and positive")
        if not self.squares:
            raise ValueError("pose frame must contain squares")
        ids = [square.square_id for square in self.squares]
        if ids != sorted(ids) or len(ids) != len(set(ids)):
            raise ValueError("pose frame requires unique, stable square-ID order")
        known_ids = set(ids)
        if any(not set(overlay.square_ids) <= known_ids for overlay in self.overlays):
            raise ValueError("overlay references a square outside its pose frame")


@dataclass(frozen=True)
class ScenarioDefinition(_ContractRecord):
    """Scenario identity and operations presented by the shared shell."""

    CONTRACT: ClassVar[str] = "packing.squares:MotionLabScenario/v1"
    SCHEMA_VERSION: ClassVar[int] = MOTION_LAB_SCHEMA_VERSION

    scenario_id: str
    title: str
    runner: ScenarioRunner
    capabilities: tuple[Capability, ...]
    initial_frame: PoseFrame

    def __post_init__(self) -> None:
        _require_text(self.scenario_id, "scenario ID")
        _require_text(self.title, "scenario title")
        if self.initial_frame.scenario_id != self.scenario_id:
            raise ValueError("initial frame must belong to its scenario")
        if len(self.capabilities) != len(set(self.capabilities)):
            raise ValueError("scenario capabilities must be unique")
        ranks = [_CAPABILITY_ORDER[value] for value in self.capabilities]
        if ranks != sorted(ranks):
            raise ValueError("scenario capabilities must use stable order")


@dataclass(frozen=True)
class QuenchRequest(_ContractRecord):
    """Strict Phase 1 numerical payload; editor groups cannot cross this boundary.

    `side` is the *editor's* container, carried so the released setup frame can be drawn
    at the scale the user placed squares in. It is not a solver input and not a bound:
    `quench_bracket` takes only centers and angles and re-minimizes the side itself, so
    two requests differing only in `side` produce identical numerical results.
    """

    CONTRACT: ClassVar[str] = "packing.squares:QuenchRequest/v1"
    SCHEMA_VERSION: ClassVar[int] = MOTION_LAB_SCHEMA_VERSION

    side: float
    x: tuple[float, ...]
    y: tuple[float, ...]
    theta: tuple[float, ...]
    solver: SolverKind = SolverKind.QUENCH_BRACKET
    max_sweeps: int = 12
    time_budget: float = 10.0

    def __post_init__(self) -> None:
        lengths = {len(self.x), len(self.y), len(self.theta)}
        if lengths == {0} or len(lengths) != 1:
            raise ValueError("x, y, and theta must have the same non-zero length")
        if len(self.x) > MAX_INTERACTIVE_SQUARES:
            raise ValueError(
                f"interactive quench supports at most {MAX_INTERACTIVE_SQUARES} squares"
            )
        if not math.isfinite(self.side) or self.side <= 0:
            raise ValueError("request side must be finite and positive")
        _require_finite(self.x + self.y + self.theta, "request pose")
        if isinstance(self.max_sweeps, bool) or not 1 <= self.max_sweeps <= MAX_QUENCH_SWEEPS:
            raise ValueError(
                f"max_sweeps must be an integer from 1 through {MAX_QUENCH_SWEEPS}"
            )
        if (
            not math.isfinite(self.time_budget)
            or not 0 < self.time_budget <= MAX_QUENCH_TIME_BUDGET_SECONDS
        ):
            raise ValueError(
                "time_budget must be finite and at most "
                f"{MAX_QUENCH_TIME_BUDGET_SECONDS:g} seconds"
            )


@dataclass(frozen=True)
class QuenchResultRecord(_ContractRecord):
    """Serializable projection of the numerical quench endpoint."""

    side: float
    x: tuple[float, ...]
    y: tuple[float, ...]
    theta: tuple[float, ...]
    lp_solves: int
    angle_steps: int
    converged: bool
    cell_changes: int
    reason: str
    contacts: tuple[tuple[int, int], ...] = ()
    fixed_point_evaluations: int = 0
    fixed_point_settled: int = 0
    fixed_point_unsettled: int = 0

    def __post_init__(self) -> None:
        lengths = {len(self.x), len(self.y), len(self.theta)}
        if lengths == {0} or len(lengths) != 1:
            raise ValueError("result arrays must have the same non-zero length")
        _require_finite((self.side, *self.x, *self.y, *self.theta), "quench result")
        _require_text(self.reason, "quench stop reason")
        counters = (
            self.lp_solves,
            self.angle_steps,
            self.cell_changes,
            self.fixed_point_evaluations,
            self.fixed_point_settled,
            self.fixed_point_unsettled,
        )
        if any(value < 0 for value in counters):
            raise ValueError("quench counters must be non-negative")
        if any(i < 0 or j <= i for i, j in self.contacts):
            raise ValueError("contacts must use increasing non-negative square IDs")
        if tuple(sorted(set(self.contacts))) != self.contacts:
            raise ValueError("contacts must be unique and stable")


@dataclass(frozen=True)
class TimelineEvent(_ContractRecord):
    """One retained solver decision or analytic state.

    The counters are scoped to the single solver call this event reports, never to the
    run: `call_lp_solves` on a `fixed-point` event is the LP work of that fixed-point
    solve alone. Run totals live in `QuenchResultRecord` and must be read from there.
    Summing counters across event kinds double-counts, because one LP call is reported
    both as the `fixed-point` state it produced and as the `angle-probe` that asked for
    it. `fixed-point` events are the ones in bijection with LP calls, and the gate pins
    their sum to `QuenchResultRecord.lp_solves` for runs that stop normally. The two
    disagree when a free sweep aborts on its budget or on an unsettled cell (D-349):
    the events retain LP work that `quench_bracket`'s own counter drops.
    """

    sequence: int
    event_kind: TimelineEventKind
    phase: Phase
    frame: PoseFrame
    detail: str
    outcome: ProbeOutcome | None = None
    call_lp_solves: int | None = None
    call_cell_changes: int | None = None

    def __post_init__(self) -> None:
        if self.sequence < 0:
            raise ValueError("event sequence must be non-negative")
        _require_text(self.detail, "timeline-event detail")
        for value in (self.call_lp_solves, self.call_cell_changes):
            if value is not None and value < 0:
                raise ValueError("timeline-event counters must be non-negative")


@dataclass(frozen=True)
class QuenchTrace(_ContractRecord):
    """A deterministic replay of decisions already made by one quench call."""

    CONTRACT: ClassVar[str] = "packing.squares:QuenchTrace/v1"
    SCHEMA_VERSION: ClassVar[int] = MOTION_LAB_SCHEMA_VERSION

    request: QuenchRequest
    events: tuple[TimelineEvent, ...]
    result: QuenchResultRecord

    def __post_init__(self) -> None:
        sequences = [event.sequence for event in self.events]
        if sequences != list(range(len(self.events))):
            raise ValueError("timeline-event sequences must be contiguous from zero")
        if not self.events:
            raise ValueError("quench trace must contain events")
        if self.events[-1].event_kind is not TimelineEventKind.STOP:
            raise ValueError("quench trace must end with a stop event")
        if len(self.request.x) != len(self.result.x):
            raise ValueError("quench trace request and result sizes must match")
        if any(len(event.frame.squares) != len(self.request.x) for event in self.events):
            raise ValueError("quench trace frames must match the request size")
        if self.events[-1].phase is not Phase.STOP:
            raise ValueError("quench trace stop event must use the stop phase")


def canonical_json(value: _ContractRecord) -> str:
    """Serialize a contract without timestamps, host state, or unstable whitespace."""
    return (
        json.dumps(
            value.to_record(),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    )


def _float_tuple(value: object, name: str) -> tuple[float, ...]:
    if not isinstance(value, list) or any(
        isinstance(item, bool) or not isinstance(item, int | float) for item in value
    ):
        raise ValueError(f"{name} must be an array of numbers")
    return tuple(float(item) for item in value)


def quench_request_from_record(record: object) -> QuenchRequest:
    """Parse a request while refusing accidental Phase 2 constraint fields."""
    if not isinstance(record, dict) or any(not isinstance(key, str) for key in record):
        raise ValueError("quench request must be an object with string keys")
    expected = {
        "contract",
        "schema_version",
        "side",
        "x",
        "y",
        "theta",
        "solver",
        "max_sweeps",
        "time_budget",
    }
    unknown = sorted(set(record) - expected)
    if unknown:
        raise ValueError(f"unknown quench-request fields: {', '.join(unknown)}")
    missing = sorted(expected - set(record))
    if missing:
        raise ValueError(f"missing quench-request fields: {', '.join(missing)}")
    schema_version = record["schema_version"]
    if (
        record["contract"] != QuenchRequest.CONTRACT
        or isinstance(schema_version, bool)
        or schema_version != MOTION_LAB_SCHEMA_VERSION
    ):
        raise ValueError("unsupported quench-request contract or schema version")
    side = record["side"]
    max_sweeps = record["max_sweeps"]
    time_budget = record["time_budget"]
    if isinstance(side, bool) or not isinstance(side, int | float):
        raise TypeError("side must be a number")
    if isinstance(max_sweeps, bool) or not isinstance(max_sweeps, int):
        raise TypeError("max_sweeps must be an integer")
    if isinstance(time_budget, bool) or not isinstance(time_budget, int | float):
        raise TypeError("time_budget must be a number")
    try:
        solver = SolverKind(record["solver"])
    except (TypeError, ValueError) as error:
        raise ValueError("unsupported quench solver") from error
    return QuenchRequest(
        side=float(side),
        x=_float_tuple(record["x"], "x"),
        y=_float_tuple(record["y"], "y"),
        theta=_float_tuple(record["theta"], "theta"),
        solver=solver,
        max_sweeps=max_sweeps,
        time_budget=float(time_budget),
    )
