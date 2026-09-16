"""Typed, versioned packing-animation interchange records."""

from __future__ import annotations

import json
import math
from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import Literal, cast

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
type Pose = tuple[float, float, float]
type HueSchemeName = Literal["identity", "angle-class", "uniform"]
type ShadeSchemeName = Literal["none", "full-side-contact", "evidence"]


@dataclass(frozen=True, slots=True)
class AnimationSource:
    strategy: str | None
    records: tuple[int, ...]
    commit: str | None
    seed: int | None
    configuration: dict[str, object] | None


@dataclass(frozen=True, slots=True)
class AnimationPalette:
    hue: HueSchemeName | None
    shade: ShadeSchemeName | None


@dataclass(frozen=True, slots=True)
class AnimationReference:
    best_known: float | None
    proved_lower_bound: float | None


@dataclass(frozen=True, slots=True)
class FairReach:
    """What an ascent step's unguided settle reached, beside the record it aimed at.

    `fair_side` and `excess_pct` are None exactly when `packing_valid` is False: an
    arrangement the geometry check rejected reached no side. `packing_valid` is None
    only for a row written before validity was recorded; its side is unchecked.
    """

    n: int
    fair_side: float | None
    record: float
    excess_pct: float | None
    packing_valid: bool | None = None


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
    guided_ancestry: bool
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
    palette: AnimationPalette | None
    reference: AnimationReference | None
    fair_reach: tuple[FairReach, ...]
    frames: tuple[AnimationFrame, ...]

    @property
    def record_guided(self) -> bool:
        return self.source is not None and bool(self.source.records)

    def frame_is_guided(self, frame: AnimationFrame) -> bool:
        """Preserve animation and record-derived ancestry through every later frame."""
        return self.guided or self.record_guided or frame.guided_ancestry


def decode_animation(value: object) -> AnimationDocument:
    """Decode an explicitly versioned animation and check its geometry and timeline."""
    return _decode_animation(value)


def decode_legacy_animation(value: object) -> AnimationDocument:
    """Decode the pre-version-field animation format used by retained local tools."""
    if isinstance(value, AnimationDocument):
        return decode_animation(value)
    row = _required_mapping(value, "animation")
    if "contract" in row:
        return decode_animation(value)
    migrated: dict[str, object] = dict(row)
    migrated["contract"] = ANIMATION_CONTRACT
    return _decode_animation(migrated)


def animation_to_row(document: AnimationDocument) -> dict[str, object]:
    """Encode one checked animation using the canonical v1 field spellings."""
    row: dict[str, object] = {
        "contract": document.contract,
        "name": document.name,
        "n": document.n,
        "guided": document.guided,
        "frames": [
            _frame_to_row(frame, guided=document.frame_is_guided(frame))
            for frame in document.frames
        ],
    }
    if document.source is not None:
        source: dict[str, object] = {"records": list(document.source.records)}
        if document.source.strategy is not None:
            source["strategy"] = document.source.strategy
        if document.source.commit is not None:
            source["commit"] = document.source.commit
        if document.source.seed is not None:
            source["seed"] = document.source.seed
        if document.source.configuration is not None:
            source["configuration"] = document.source.configuration
        row["source"] = source
    if document.duration_seconds is not None:
        row["duration_seconds"] = document.duration_seconds
    if document.palette is not None:
        palette: dict[str, object] = {}
        if document.palette.hue is not None:
            palette["hue"] = document.palette.hue
        if document.palette.shade is not None:
            palette["shade"] = document.palette.shade
        row["palette"] = palette
    if document.reference is not None:
        reference: dict[str, object] = {}
        if document.reference.best_known is not None:
            reference["best_known"] = document.reference.best_known
        if document.reference.proved_lower_bound is not None:
            reference["proved_lower_bound"] = document.reference.proved_lower_bound
        row["reference"] = reference
    if document.fair_reach:
        row["fair_reach"] = [
            {
                "n": item.n,
                "fair_side": item.fair_side,
                "record": item.record,
                "excess_pct": item.excess_pct,
                **({} if item.packing_valid is None else {"packing_valid": item.packing_valid}),
            }
            for item in document.fair_reach
        ]
    return row


def animation_to_json(document: AnimationDocument, *, indent: int | None = None) -> str:
    """Serialize v1 without admitting non-JSON numeric values."""
    return json.dumps(
        animation_to_row(document),
        allow_nan=False,
        indent=indent,
        sort_keys=True,
    )


def _decode_animation(value: object) -> AnimationDocument:
    if isinstance(value, AnimationDocument):
        # Dataclasses are a convenient internal representation, not an admission
        # bypass. Re-encode them so geometry receipts and every wire constraint are
        # derived again before a public consumer trusts the document.
        return _decode_animation(animation_to_row(value))
    schema_path = configured_project_root() / "strategies/packing-animation.schema.yaml"
    schema = cast(Mapping[str, object], safe_load(schema_path.read_text(encoding="utf-8")))
    jsonschema.validate(value, schema)
    row = _required_mapping(value, "animation")
    contract = _required_string(row.get("contract"), "animation contract")
    if contract != ANIMATION_CONTRACT:
        raise ValueError(f"unsupported animation contract {contract!r}")
    n = _positive_integer(row["n"], "animation n")
    source = _source(row.get("source"))
    raw_frames = _required_list(row["frames"], "animation frames")
    frames: list[AnimationFrame] = []
    stable_ids: tuple[int, ...] | None = None
    previous_time = -math.inf
    guided_ancestry = _optional_bool(row.get("guided"), default=False) or (
        source is not None and bool(source.records)
    )
    for index, item in enumerate(raw_frames):
        frame = _frame(item, n=n, index=index)
        guided_ancestry = guided_ancestry or frame.guided
        frame = replace(frame, guided_ancestry=guided_ancestry)
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
        palette=_palette(row.get("palette")),
        reference=_reference(row.get("reference")),
        fair_reach=_fair_reach(row.get("fair_reach")),
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
    if len(records) != len(set(records)):
        raise ValueError("animation source records must be unique")
    configuration = (
        _json_object(row["configuration"], "source configuration")
        if "configuration" in row
        else None
    )
    return AnimationSource(
        strategy=_optional_string(row.get("strategy")),
        records=records,
        commit=_optional_string(row.get("commit")),
        seed=(_uint32(row["seed"], "source seed") if "seed" in row else None),
        configuration=configuration,
    )


def _palette(value: object) -> AnimationPalette | None:
    if value is None:
        return None
    row = _required_mapping(value, "animation palette")
    hue = _optional_string(row.get("hue"))
    shade = _optional_string(row.get("shade"))
    if hue not in {None, "identity", "angle-class", "uniform"}:
        raise ValueError(f"unsupported animation hue scheme {hue!r}")
    if shade not in {None, "none", "full-side-contact", "evidence"}:
        raise ValueError(f"unsupported animation shade scheme {shade!r}")
    return AnimationPalette(
        hue=cast(HueSchemeName | None, hue),
        shade=cast(ShadeSchemeName | None, shade),
    )


def _reference(value: object) -> AnimationReference | None:
    if value is None:
        return None
    row = _required_mapping(value, "animation reference")
    return AnimationReference(
        best_known=(
            _positive_number(row["best_known"], "best-known reference")
            if "best_known" in row
            else None
        ),
        proved_lower_bound=(
            _positive_number(row["proved_lower_bound"], "proved lower bound")
            if "proved_lower_bound" in row
            else None
        ),
    )


def _fair_reach(value: object) -> tuple[FairReach, ...]:
    if value is None:
        return ()
    return tuple(
        _fair_reach_row(_required_mapping(item, "fair-reach row"))
        for item in _required_list(value, "fair reach")
    )


def _fair_reach_row(row: dict[str, object]) -> FairReach:
    packing_valid = (
        _required_bool(row["packing_valid"], "fair-reach packing validity")
        if "packing_valid" in row
        else None
    )
    n = _positive_integer(row["n"], "fair-reach n")
    record = _positive_number(row["record"], "fair-reach record")
    if packing_valid is False:
        if row["fair_side"] is not None or row["excess_pct"] is not None:
            raise ValueError("a fair-reach settle that is not a packing reached no side")
        return FairReach(
            n=n, fair_side=None, record=record, excess_pct=None, packing_valid=False
        )
    return FairReach(
        n=n,
        fair_side=_positive_number(row["fair_side"], "fair-reach side"),
        record=record,
        excess_pct=_number(row["excess_pct"], "fair-reach excess"),
        packing_valid=packing_valid,
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
    if len(square_ids) != n or len(set(square_ids)) != n:
        raise ValueError(f"frame {index} square IDs must be complete and unique")
    locked: tuple[bool, ...] | None = None
    if "locked" in row:
        locked = tuple(
            _required_bool(item, f"frame {index} locked flag")
            for item in _required_list(row["locked"], f"frame {index} locked flags")
        )
        if len(locked) != n:
            raise ValueError(f"frame {index} locked count does not match animation n")
    return AnimationFrame(
        logical_time=_unit_interval(row["t"], f"frame {index} logical time"),
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
        guided_ancestry=False,
        feasible=(
            _required_bool(row["feasible"], f"frame {index} feasible")
            if "feasible" in row
            else None
        ),
        label=_optional_text(row.get("label")),
        geometry=geometry,
    )


def _frame_to_row(frame: AnimationFrame, *, guided: bool) -> dict[str, object]:
    row: dict[str, object] = {
        "t": frame.logical_time,
        "side": frame.side,
        "squares": [list(pose) for pose in frame.squares],
        "square_ids": list(frame.square_ids),
        "phase": frame.phase,
        # Materialize inherited guidance so a later editor can trim the ancestry source
        # without making a guided frame look independently found.
        "guided": guided,
    }
    if frame.record is not None:
        row["record"] = frame.record
    if frame.locked is not None:
        row["locked"] = list(frame.locked)
    if frame.feasible is not None:
        row["feasible"] = frame.feasible
    if frame.label is not None:
        row["label"] = frame.label
    return row


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


def _json_object(value: object, label: str, *, depth: int = 0) -> dict[str, object]:
    if depth > 32:
        raise ValueError(f"{label} nesting exceeds 32 levels")
    row = _required_mapping(value, label)
    return {key: _json_value(item, label, depth=depth + 1) for key, item in row.items()}


def _json_value(value: object, label: str, *, depth: int) -> object:
    if depth > 32:
        raise ValueError(f"{label} nesting exceeds 32 levels")
    if value is None or isinstance(value, (bool, str)):
        return value
    if isinstance(value, int):
        _number(value, label)
        return value
    if isinstance(value, float):
        return _number(value, label)
    if isinstance(value, list):
        return [_json_value(item, label, depth=depth + 1) for item in value]
    if isinstance(value, dict):
        return _json_object(value, label, depth=depth)
    raise TypeError(f"{label} must contain only JSON values")


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


def _unit_interval(value: object, label: str) -> float:
    number = _number(value, label)
    if not 0 <= number <= 1:
        raise ValueError(f"{label} must be between zero and one")
    return number


def _positive_integer(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise TypeError(f"{label} must be a positive integer")
    return value


def _uint32(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value < 2**32:
        raise TypeError(f"{label} must be an unsigned 32-bit integer")
    return value


def _required_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise TypeError(f"{label} must be a non-empty string")
    return value


def _optional_string(value: object) -> str | None:
    if value is None:
        return None
    return _required_string(value, "animation string")


def _optional_text(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError("animation text must be a string")
    return value


def _required_bool(value: object, label: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{label} must be a boolean")
    return value


def _optional_bool(value: object, *, default: bool) -> bool:
    return default if value is None else _required_bool(value, "animation boolean")
