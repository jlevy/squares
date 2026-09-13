"""Typed, versioned decoding for renderer-independent packing animations."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import cast

import jsonschema

from sqpack.project import configured_project_root
from sqpack.yamlio import safe_load
from workbench_tools.packing_contracts import (
    DEFAULT_VALIDITY_TOLERANCE,
    GeometryCheck,
    GeometryIssue,
    check_unit_square_packing,
)

ANIMATION_CONTRACT = "packing.squares:PackingAnimation/v1"
Pose = tuple[float, float, float]


@dataclass(frozen=True, slots=True)
class AnimationSource:
    strategy: str | None
    records: tuple[int, ...]
    commit: str | None
    seed: int | None
    configuration: dict[str, object] | None


@dataclass(frozen=True, slots=True)
class AnimationFrame:
    logical_time: float
    side: float
    squares: tuple[Pose, ...]
    square_ids: tuple[int, ...]
    record: int | None
    locked: tuple[bool, ...] | None
    phase: str
    guided: bool
    feasible: bool | None
    label: str | None
    geometry: GeometryCheck


@dataclass(frozen=True, slots=True)
class AnimationDocument:
    contract: str
    name: str
    n: int
    guided: bool
    source: AnimationSource | None
    duration_seconds: float | None
    frames: tuple[AnimationFrame, ...]

    @property
    def record_guided(self) -> bool:
        return self.source is not None and bool(self.source.records)

    def frame_is_guided(self, frame: AnimationFrame) -> bool:
        """Preserve animation and record-derived ancestry through every later frame."""
        return self.guided or self.record_guided or frame.guided


def decode_animation(value: object) -> AnimationDocument:
    """Validate and decode one animation, including geometry and timeline semantics."""
    if isinstance(value, AnimationDocument):
        return value
    schema_path = configured_project_root() / "strategies/packing-animation.schema.yaml"
    schema = cast(Mapping[str, object], safe_load(schema_path.read_text(encoding="utf-8")))
    jsonschema.validate(value, schema)
    row = _required_mapping(value, "animation")
    contract = _optional_string(row.get("contract")) or ANIMATION_CONTRACT
    if contract != ANIMATION_CONTRACT:
        raise ValueError(f"unsupported animation contract {contract!r}")
    n = _positive_integer(row["n"], "animation n")
    source = _source(row.get("source"))
    raw_frames = _required_list(row["frames"], "animation frames")
    frames: list[AnimationFrame] = []
    stable_ids: tuple[int, ...] | None = None
    previous_time = -math.inf
    for index, item in enumerate(raw_frames):
        frame = _frame(item, n=n, index=index)
        if frame.logical_time < previous_time:
            raise ValueError("animation logical time must be non-decreasing")
        previous_time = frame.logical_time
        if stable_ids is None:
            stable_ids = frame.square_ids
        elif frame.square_ids != stable_ids:
            raise ValueError("square IDs changed between animation frames")
        frames.append(frame)
    return AnimationDocument(
        contract=contract,
        name=_required_string(row["name"], "animation name"),
        n=n,
        guided=_optional_bool(row.get("guided"), default=False),
        source=source,
        duration_seconds=(
            _positive_number(row["duration_seconds"], "animation duration")
            if "duration_seconds" in row
            else None
        ),
        frames=tuple(frames),
    )


def _source(value: object) -> AnimationSource | None:
    if value is None:
        return None
    row = _required_mapping(value, "animation source")
    records = tuple(
        _positive_integer(item, "source record")
        for item in _required_list(row.get("records", []), "source records")
    )
    configuration = (
        _required_mapping(row["configuration"], "source configuration")
        if "configuration" in row
        else None
    )
    return AnimationSource(
        strategy=_optional_string(row.get("strategy")),
        records=records,
        commit=_optional_string(row.get("commit")),
        seed=(_nonnegative_integer(row["seed"], "source seed") if "seed" in row else None),
        configuration=configuration,
    )


def _frame(value: object, *, n: int, index: int) -> AnimationFrame:
    row = _required_mapping(value, f"frame {index}")
    squares = _poses(row["squares"], f"frame {index} squares")
    side = _positive_number(row["side"], f"frame {index} side")
    geometry = check_unit_square_packing(
        squares,
        side=side,
        expected_count=n,
        tolerance=DEFAULT_VALIDITY_TOLERANCE,
    )
    if GeometryIssue.COUNT in geometry.issues:
        raise ValueError(f"frame {index} square count does not match animation n")
    if GeometryIssue.SHAPE in geometry.issues:
        raise ValueError(f"frame {index} square poses must be numeric triples")
    if GeometryIssue.NONFINITE in geometry.issues:
        raise ValueError(f"frame {index} side and poses must be finite")

    raw_ids = row.get("square_ids", list(range(1, n + 1)))
    square_ids = tuple(
        _positive_integer(item, f"frame {index} square ID")
        for item in _required_list(raw_ids, f"frame {index} square IDs")
    )
    if len(square_ids) != n or tuple(sorted(square_ids)) != square_ids:
        raise ValueError(f"frame {index} square IDs must be complete and stable")
    locked: tuple[bool, ...] | None = None
    if "locked" in row:
        locked = tuple(
            _required_bool(item, f"frame {index} locked flag")
            for item in _required_list(row["locked"], f"frame {index} locked flags")
        )
        if len(locked) != n:
            raise ValueError(f"frame {index} locked count does not match animation n")
    return AnimationFrame(
        logical_time=_nonnegative_number(row["t"], f"frame {index} logical time"),
        side=side,
        squares=squares,
        square_ids=square_ids,
        record=(
            _positive_integer(row["record"], f"frame {index} record")
            if "record" in row
            else None
        ),
        locked=locked,
        phase=_optional_string(row.get("phase")) or "frame",
        guided=_optional_bool(row.get("guided"), default=False),
        feasible=(
            _required_bool(row["feasible"], f"frame {index} feasible")
            if "feasible" in row
            else None
        ),
        label=_optional_string(row.get("label")),
        geometry=geometry,
    )


def _poses(value: object, label: str) -> tuple[Pose, ...]:
    rows = _required_list(value, label)
    poses: list[Pose] = []
    for row in rows:
        values = _required_list(row, label)
        if len(values) != 3:
            raise ValueError(f"{label} must contain numeric triples")
        poses.append(
            (
                _number(values[0], label),
                _number(values[1], label),
                _number(values[2], label),
            )
        )
    return tuple(poses)


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


def _number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must contain finite numbers")
    try:
        number = float(value)
    except (OverflowError, TypeError, ValueError) as error:
        raise ValueError(f"{label} must contain finite numbers") from error
    if not math.isfinite(number):
        raise ValueError(f"{label} must contain finite numbers")
    return number


def _positive_number(value: object, label: str) -> float:
    number = _number(value, label)
    if number <= 0:
        raise ValueError(f"{label} must be positive")
    return number


def _nonnegative_number(value: object, label: str) -> float:
    number = _number(value, label)
    if number < 0:
        raise ValueError(f"{label} must be non-negative")
    return number


def _nonnegative_integer(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise TypeError(f"{label} must be a non-negative integer")
    return value


def _positive_integer(value: object, label: str) -> int:
    number = _nonnegative_integer(value, label)
    if number < 1:
        raise ValueError(f"{label} must be positive")
    return number


def _required_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise TypeError(f"{label} must be a nonempty string")
    return value


def _optional_string(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _required_bool(value: object, label: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{label} must be boolean")
    return value


def _optional_bool(value: object, *, default: bool) -> bool:
    return value if isinstance(value, bool) else default
