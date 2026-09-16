"""Typed, versioned strategy declarations and execution receipts."""

from __future__ import annotations

import json
import math
import secrets
from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Literal, cast

import jsonschema

from sqpack.project import configured_project_root
from sqpack.yamlio import safe_load
from workbench_tools.packing_contracts import GeometryCheck

STRATEGY_CONTRACT = "packing.squares:PackingStrategy/v1"
STRATEGY_RUN_CONTRACT = "packing.squares:PackingStrategyRun/v1"
UINT32_MAX = 2**32 - 1

type Pose = tuple[float, float, float]
type Mechanism = Literal[
    "scatter", "grid", "assemble", "project", "ratchet", "relax", "guide", "container"
]
type StructureRung = Literal[
    "none", "partition", "contact-graph", "contact-graph-with-types", "with-wall-contacts"
]
type StructureControl = Literal["none", "thinned", "rewired"]
type SideReference = Literal["record", "grid", "current"]
type TargetMatch = Literal["by-motion", "as-given"]


@dataclass(frozen=True, slots=True)
class SideSpec:
    relative_to: SideReference | None = None
    factor: float | None = None


@dataclass(frozen=True, slots=True)
class StructureSpec:
    rung: StructureRung
    source: Literal["record", "given", "random"] | None = None
    control: StructureControl | None = None
    keep: int | None = None


@dataclass(frozen=True, slots=True)
class ConstraintSpec:
    band: float | None = None
    weight: float | None = None


@dataclass(frozen=True, slots=True)
class UntilSpec:
    feasible: bool | None = None
    steps: int | None = None
    stalled_for: int | None = None
    frames: int | None = None


@dataclass(frozen=True, slots=True)
class ScheduleSpec:
    start: float | None = None
    halve_on_failure: bool | None = None
    floor: float | None = None
    attempts: int | None = None
    attempts_ceiling: int | None = None
    cold: float | None = None


@dataclass(frozen=True, slots=True)
class TargetSpec:
    source: Literal["record"] | None = None
    match: TargetMatch | None = None
    steps: int | None = None
    pull: float | None = None


@dataclass(frozen=True, slots=True)
class StrategyPhase:
    mechanism: Mechanism
    label: str | None = None
    relaxation: float | None = None
    structure: StructureSpec | None = None
    constraints: ConstraintSpec | None = None
    until: UntilSpec | None = None
    side: SideSpec | None = None
    schedule: ScheduleSpec | None = None
    target: TargetSpec | None = None


@dataclass(frozen=True, slots=True)
class PackingStrategy:
    contract: str
    name: str
    n: int
    seed: int | None
    phases: tuple[StrategyPhase, ...]


@dataclass(frozen=True, slots=True)
class StrategyTraceFrame:
    side: float
    poses: tuple[Pose, ...]
    phase: str
    guided: bool
    geometry: GeometryCheck


@dataclass(frozen=True, slots=True)
class StrategyPhaseReceipt:
    index: int
    mechanism: Mechanism
    label: str
    rung: str
    side: float
    violation: float
    geometry: GeometryCheck
    frame_count: int
    solved: bool | None = None
    steps: int | None = None
    calls: int | None = None
    settled: bool | None = None
    residual: float | None = None


@dataclass(frozen=True, slots=True)
class StrategyRun:
    contract: str
    configuration: PackingStrategy
    poses: tuple[Pose, ...]
    side: float
    geometry: GeometryCheck
    phases: tuple[StrategyPhaseReceipt, ...]
    trace: tuple[StrategyTraceFrame, ...]
    guided: bool
    answer_sources: tuple[str, ...]


def decode_strategy(value: object) -> PackingStrategy:
    """Decode an explicitly versioned strategy and reject unsupported capabilities."""
    return _decode_strategy(value)


def decode_legacy_strategy(value: object) -> PackingStrategy:
    """Decode the pre-version-field form accepted by historical Python callers."""
    if isinstance(value, PackingStrategy):
        return decode_strategy(value)
    row = _required_mapping(value, "strategy")
    if "contract" in row:
        return decode_strategy(value)
    migrated: dict[str, object] = dict(row)
    migrated["contract"] = STRATEGY_CONTRACT
    return _decode_strategy(migrated)


def load_strategy(path: Path) -> PackingStrategy:
    """Load an enforced softschema strategy document from a filesystem path."""
    raw = safe_load(path.read_text(encoding="utf-8"))
    document = _required_mapping(raw, "strategy document")
    metadata = _required_mapping(document.get("softschema"), "strategy softschema")
    if metadata.get("contract") != STRATEGY_CONTRACT:
        raise ValueError(f"unsupported strategy contract {metadata.get('contract')!r}")
    return decode_strategy(document.get("strategy"))


def choose_seed(
    strategy: PackingStrategy,
    seed_source: Callable[[], int] | None = None,
) -> int:
    """Choose and validate the replay seed before execution starts."""
    chosen = strategy.seed
    if chosen is None:
        chosen = secrets.randbits(32) if seed_source is None else seed_source()
    if isinstance(chosen, bool) or not isinstance(chosen, int) or not 0 <= chosen <= UINT32_MAX:
        raise ValueError("strategy seed must be an unsigned 32-bit integer")
    return chosen


def materialize_configuration(
    strategy: PackingStrategy,
    *,
    seed: int,
    record_contact_count: Callable[[int], int] | None = None,
) -> PackingStrategy:
    """Materialize every supported executor default needed for exact replay."""
    if isinstance(seed, bool) or not 0 <= seed <= UINT32_MAX:
        raise ValueError("strategy seed must be an unsigned 32-bit integer")
    phases: list[StrategyPhase] = []
    for phase in strategy.phases:
        side = phase.side
        if side is not None:
            side = replace(
                side,
                relative_to=side.relative_to or "current",
                factor=1.0 if side.factor is None else side.factor,
            )
        structure = phase.structure
        if structure is not None:
            control = structure.control or "none"
            keep = structure.keep
            if control != "none" and keep is None:
                if record_contact_count is None:
                    raise ValueError(
                        "materializing a structure control requires the record contact count"
                    )
                divisor = 2 if control == "thinned" else 4
                keep = record_contact_count(strategy.n) // divisor
            structure = replace(
                structure,
                source=structure.source or "record",
                control=control,
                keep=keep,
            )
        relaxation = phase.relaxation
        until = phase.until
        constraints = phase.constraints
        schedule = phase.schedule
        target = phase.target
        if phase.mechanism in {"project", "relax", "ratchet"}:
            relaxation = 0.1 if relaxation is None else relaxation
            until = until or UntilSpec()
            steps = 6000 if until.steps is None else until.steps
            until = replace(
                until,
                steps=steps,
                stalled_for=(
                    max(1, steps // 3) if until.stalled_for is None else until.stalled_for
                ),
            )
        if phase.mechanism in {"project", "ratchet"}:
            constraints = constraints or ConstraintSpec()
            constraints = replace(
                constraints,
                band=0.02 if constraints.band is None else constraints.band,
                weight=1.0 if constraints.weight is None else constraints.weight,
            )
        if phase.mechanism == "ratchet":
            schedule = schedule or ScheduleSpec()
            schedule = replace(
                schedule,
                halve_on_failure=(
                    True if schedule.halve_on_failure is None else schedule.halve_on_failure
                ),
                floor=1e-3 if schedule.floor is None else schedule.floor,
                attempts=5 if schedule.attempts is None else schedule.attempts,
                attempts_ceiling=(
                    24 if schedule.attempts_ceiling is None else schedule.attempts_ceiling
                ),
                cold=0.0 if schedule.cold is None else schedule.cold,
            )
        if phase.mechanism == "guide":
            target = target or TargetSpec()
            target = replace(
                target,
                source=target.source or "record",
                match=target.match or "by-motion",
                steps=400 if target.steps is None else target.steps,
                pull=5.0 if target.pull is None else target.pull,
            )
        if phase.mechanism == "container":
            until = until or UntilSpec()
            until = replace(until, frames=24 if until.frames is None else until.frames)
        phases.append(
            replace(
                phase,
                relaxation=relaxation,
                structure=structure,
                constraints=constraints,
                until=until,
                side=side,
                schedule=schedule,
                target=target,
            )
        )
    return replace(strategy, seed=seed, phases=tuple(phases))


def strategy_to_row(strategy: PackingStrategy) -> dict[str, object]:
    """Encode one strategy using canonical v1 field spellings."""
    row: dict[str, object] = {
        "contract": strategy.contract,
        "name": strategy.name,
        "n": strategy.n,
        "phases": [_phase_to_row(phase) for phase in strategy.phases],
    }
    if strategy.seed is not None:
        row["seed"] = strategy.seed
    return row


def strategy_to_json(strategy: PackingStrategy, *, indent: int | None = None) -> str:
    """Serialize v1 without admitting non-JSON numeric values."""
    return json.dumps(strategy_to_row(strategy), allow_nan=False, indent=indent, sort_keys=True)


def _decode_strategy(value: object) -> PackingStrategy:
    if isinstance(value, PackingStrategy):
        # Typed construction must not bypass the same numeric and capability checks
        # applied to a wire record.
        return _decode_strategy(strategy_to_row(value))
    schema_path = configured_project_root() / "strategies/packing-strategy.schema.yaml"
    schema = cast(Mapping[str, object], safe_load(schema_path.read_text(encoding="utf-8")))
    jsonschema.validate(value, schema)
    row = _required_mapping(value, "strategy")
    contract = _required_string(row.get("contract"), "strategy contract")
    if contract != STRATEGY_CONTRACT:
        raise ValueError(f"unsupported strategy contract {contract!r}")
    phases = tuple(
        _phase(item, index=index)
        for index, item in enumerate(_required_list(row["phases"], "strategy phases"))
    )
    return PackingStrategy(
        contract=contract,
        name=_required_string(row["name"], "strategy name"),
        n=_positive_integer(row["n"], "strategy n"),
        seed=(_uint32(row["seed"], "strategy seed") if "seed" in row else None),
        phases=phases,
    )


def _phase(value: object, *, index: int) -> StrategyPhase:
    row = _required_mapping(value, f"phase {index}")
    mechanism = _enum(
        row["mechanism"],
        {
            "scatter",
            "grid",
            "assemble",
            "project",
            "ratchet",
            "relax",
            "guide",
            "container",
        },
        f"phase {index} mechanism",
    )
    phase = StrategyPhase(
        mechanism=cast(Mechanism, mechanism),
        label=_optional_string(row.get("label")),
        relaxation=(
            _bounded_number(row["relaxation"], f"phase {index} relaxation", 0, 1)
            if "relaxation" in row
            else None
        ),
        structure=_structure(row.get("structure"), index=index),
        constraints=_constraints(row.get("constraints"), index=index),
        until=_until(row.get("until"), index=index),
        side=_side(row.get("side"), index=index),
        schedule=_schedule(row.get("schedule"), index=index),
        target=_target(row.get("target"), index=index),
    )
    _validate_capabilities(phase, present_fields=set(row))
    return phase


def _validate_capabilities(phase: StrategyPhase, *, present_fields: set[str]) -> None:
    allowed: dict[Mechanism, frozenset[str]] = {
        "scatter": frozenset({"mechanism", "label", "side"}),
        "grid": frozenset({"mechanism", "label", "side"}),
        "assemble": frozenset({"mechanism", "label", "structure", "side"}),
        "project": frozenset(
            {"mechanism", "label", "relaxation", "structure", "constraints", "until", "side"}
        ),
        "relax": frozenset({"mechanism", "label", "relaxation", "until", "side"}),
        "ratchet": frozenset(
            {
                "mechanism",
                "label",
                "relaxation",
                "structure",
                "constraints",
                "until",
                "schedule",
            }
        ),
        "guide": frozenset({"mechanism", "label", "target"}),
        "container": frozenset({"mechanism", "label", "side", "until"}),
    }
    unsupported = sorted(present_fields - allowed[phase.mechanism])
    if unsupported:
        raise ValueError(
            f"{phase.mechanism} does not support phase field(s): {', '.join(unsupported)}"
        )
    structure = phase.structure
    if structure is not None:
        source = structure.source or "record"
        if source != "record":
            raise ValueError(f"structure source {source!r} is not implemented")
        if structure.keep is not None and (structure.control or "none") == "none":
            raise ValueError("structure keep requires a thinned or rewired control")
    if phase.mechanism == "assemble":
        if structure is None or structure.rung != "contact-graph-with-types":
            raise ValueError("assemble requires record contact-graph-with-types structure")
        if (structure.control or "none") != "none":
            raise ValueError("assemble does not implement structure controls")
    if phase.until is not None:
        if phase.until.feasible is not None:
            raise ValueError("until.feasible is not implemented by the Python executor")
        if phase.mechanism == "container":
            if phase.until.steps is not None or phase.until.stalled_for is not None:
                raise ValueError("container does not support until steps or stalled_for")
        elif phase.until.frames is not None:
            raise ValueError(f"{phase.mechanism} does not support until.frames")
    if phase.schedule is not None:
        if phase.schedule.start is not None:
            raise ValueError("schedule.start is not implemented by the Python executor")
        if phase.schedule.halve_on_failure is False:
            raise ValueError("schedule.halve_on_failure=false is not implemented")


def _structure(value: object, *, index: int) -> StructureSpec | None:
    if value is None:
        return None
    row = _required_mapping(value, f"phase {index} structure")
    rung = _enum(
        row["rung"],
        {
            "none",
            "partition",
            "contact-graph",
            "contact-graph-with-types",
            "with-wall-contacts",
        },
        f"phase {index} structure rung",
    )
    source = _optional_string(row.get("source"))
    control = _optional_string(row.get("control"))
    return StructureSpec(
        rung=cast(StructureRung, rung),
        source=cast(Literal["record", "given", "random"] | None, source),
        control=cast(StructureControl | None, control),
        keep=(
            _nonnegative_integer(row["keep"], f"phase {index} structure keep")
            if "keep" in row
            else None
        ),
    )


def _constraints(value: object, *, index: int) -> ConstraintSpec | None:
    if value is None:
        return None
    row = _required_mapping(value, f"phase {index} constraints")
    return ConstraintSpec(
        band=(
            _nonnegative_number(row["band"], f"phase {index} constraint band")
            if "band" in row
            else None
        ),
        weight=(
            _nonnegative_number(row["weight"], f"phase {index} constraint weight")
            if "weight" in row
            else None
        ),
    )


def _until(value: object, *, index: int) -> UntilSpec | None:
    if value is None:
        return None
    row = _required_mapping(value, f"phase {index} until")
    return UntilSpec(
        feasible=(
            _required_bool(row["feasible"], f"phase {index} until feasible")
            if "feasible" in row
            else None
        ),
        steps=(
            _positive_integer(row["steps"], f"phase {index} until steps")
            if "steps" in row
            else None
        ),
        stalled_for=(
            _positive_integer(row["stalled_for"], f"phase {index} until stalled_for")
            if "stalled_for" in row
            else None
        ),
        frames=(
            _positive_integer(row["frames"], f"phase {index} until frames")
            if "frames" in row
            else None
        ),
    )


def _side(value: object, *, index: int) -> SideSpec | None:
    if value is None:
        return None
    row = _required_mapping(value, f"phase {index} side")
    relative_to = _optional_string(row.get("relative_to"))
    return SideSpec(
        relative_to=cast(SideReference | None, relative_to),
        factor=(
            _positive_number(row["factor"], f"phase {index} side factor")
            if "factor" in row
            else None
        ),
    )


def _schedule(value: object, *, index: int) -> ScheduleSpec | None:
    if value is None:
        return None
    row = _required_mapping(value, f"phase {index} schedule")
    return ScheduleSpec(
        start=(
            _positive_number(row["start"], f"phase {index} schedule start")
            if "start" in row
            else None
        ),
        halve_on_failure=(
            _required_bool(row["halve_on_failure"], f"phase {index} halve-on-failure")
            if "halve_on_failure" in row
            else None
        ),
        floor=(
            _positive_number(row["floor"], f"phase {index} schedule floor")
            if "floor" in row
            else None
        ),
        attempts=(
            _positive_integer(row["attempts"], f"phase {index} schedule attempts")
            if "attempts" in row
            else None
        ),
        attempts_ceiling=(
            _positive_integer(
                row["attempts_ceiling"], f"phase {index} schedule attempts ceiling"
            )
            if "attempts_ceiling" in row
            else None
        ),
        cold=(
            _closed_interval(row["cold"], f"phase {index} schedule cold", 0, 1)
            if "cold" in row
            else None
        ),
    )


def _target(value: object, *, index: int) -> TargetSpec | None:
    if value is None:
        return None
    row = _required_mapping(value, f"phase {index} target")
    source = _optional_string(row.get("source"))
    match = _optional_string(row.get("match"))
    return TargetSpec(
        source=cast(Literal["record"] | None, source),
        match=cast(TargetMatch | None, match),
        steps=(
            _positive_integer(row["steps"], f"phase {index} target steps")
            if "steps" in row
            else None
        ),
        pull=(
            _positive_number(row["pull"], f"phase {index} target pull")
            if "pull" in row
            else None
        ),
    )


def _phase_to_row(phase: StrategyPhase) -> dict[str, object]:
    row: dict[str, object] = {"mechanism": phase.mechanism}
    if phase.label is not None:
        row["label"] = phase.label
    if phase.relaxation is not None:
        row["relaxation"] = phase.relaxation
    row.update(
        {
            name: value
            for name, value in (
                ("structure", _structure_to_row(phase.structure)),
                ("constraints", _constraints_to_row(phase.constraints)),
                ("until", _until_to_row(phase.until)),
                ("side", _side_to_row(phase.side)),
                ("schedule", _schedule_to_row(phase.schedule)),
                ("target", _target_to_row(phase.target)),
            )
            if value is not None
        }
    )
    return row


def _structure_to_row(value: StructureSpec | None) -> dict[str, object] | None:
    if value is None:
        return None
    row: dict[str, object] = {"rung": value.rung}
    return _optional_fields(
        row,
        source=value.source,
        control=value.control,
        keep=value.keep,
    )


def _constraints_to_row(value: ConstraintSpec | None) -> dict[str, object] | None:
    return None if value is None else _optional_fields({}, band=value.band, weight=value.weight)


def _until_to_row(value: UntilSpec | None) -> dict[str, object] | None:
    return (
        None
        if value is None
        else _optional_fields(
            {},
            feasible=value.feasible,
            steps=value.steps,
            stalled_for=value.stalled_for,
            frames=value.frames,
        )
    )


def _side_to_row(value: SideSpec | None) -> dict[str, object] | None:
    return (
        None
        if value is None
        else _optional_fields({}, relative_to=value.relative_to, factor=value.factor)
    )


def _schedule_to_row(value: ScheduleSpec | None) -> dict[str, object] | None:
    return (
        None
        if value is None
        else _optional_fields(
            {},
            start=value.start,
            halve_on_failure=value.halve_on_failure,
            floor=value.floor,
            attempts=value.attempts,
            attempts_ceiling=value.attempts_ceiling,
            cold=value.cold,
        )
    )


def _target_to_row(value: TargetSpec | None) -> dict[str, object] | None:
    return (
        None
        if value is None
        else _optional_fields(
            {},
            source=value.source,
            match=value.match,
            steps=value.steps,
            pull=value.pull,
        )
    )


def _optional_fields(row: dict[str, object], **values: object) -> dict[str, object]:
    row.update({name: value for name, value in values.items() if value is not None})
    return row


def _required_mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be an object")
    raw = cast(dict[object, object], value)
    if any(not isinstance(key, str) for key in raw):
        raise TypeError(f"{label} keys must be strings")
    return {cast(str, key): item for key, item in raw.items()}


def _required_list(value: object, label: str) -> list[object]:
    if not isinstance(value, list):
        raise TypeError(f"{label} must be a list")
    return cast(list[object], value)


def _required_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise TypeError(f"{label} must be a non-empty string")
    return value


def _optional_string(value: object) -> str | None:
    if value is None:
        return None
    return _required_string(value, "strategy string")


def _enum(value: object, choices: set[str], label: str) -> str:
    text = _required_string(value, label)
    if text not in choices:
        raise ValueError(f"unsupported {label} {text!r}")
    return text


def _number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be a finite number")
    try:
        number = float(value)
    except (OverflowError, TypeError, ValueError) as error:
        raise ValueError(f"{label} must be a finite number") from error
    if not math.isfinite(number):
        raise ValueError(f"{label} must be a finite number")
    return number


def _positive_number(value: object, label: str) -> float:
    number = _number(value, label)
    if number <= 0:
        raise ValueError(f"{label} must be positive")
    return number


def _nonnegative_number(value: object, label: str) -> float:
    number = _number(value, label)
    if number < 0:
        raise ValueError(f"{label} must be nonnegative")
    return number


def _bounded_number(value: object, label: str, lower: float, upper: float) -> float:
    number = _number(value, label)
    if not lower <= number <= upper or number == lower:
        raise ValueError(f"{label} must be above {lower} and at most {upper}")
    return number


def _closed_interval(value: object, label: str, lower: float, upper: float) -> float:
    number = _number(value, label)
    if not lower <= number <= upper:
        raise ValueError(f"{label} must be between {lower} and {upper}")
    return number


def _positive_integer(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise TypeError(f"{label} must be a positive integer")
    return value


def _nonnegative_integer(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise TypeError(f"{label} must be a nonnegative integer")
    return value


def _uint32(value: object, label: str) -> int:
    value = _nonnegative_integer(value, label)
    if value > UINT32_MAX:
        raise ValueError(f"{label} must be an unsigned 32-bit integer")
    return value


def _required_bool(value: object, label: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{label} must be a boolean")
    return value
