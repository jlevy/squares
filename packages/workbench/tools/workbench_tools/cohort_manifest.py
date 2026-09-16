"""Versioned, explicit seed and work manifests for reproducible block reports."""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from enum import StrEnum

SCHEMA = "squares.workbench.cohort/v1"


def strict_json(text: str) -> object:
    """Read manifest/envelope JSON without nonstandard NaN or Infinity tokens."""
    return json.loads(text, parse_constant=_invalid_constant)


def _invalid_constant(token: str) -> object:
    raise ValueError(f"nonfinite JSON token {token} is not supported")


class AttemptStatus(StrEnum):
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    NOT_STARTED = "not-started"


class Partition(StrEnum):
    EXPLORATORY = "exploratory"
    TUNING = "tuning"
    HELD_OUT = "held-out"


class Purpose(StrEnum):
    SOFTWARE_VALIDATION = "software-validation"
    RESEARCH = "research"


@dataclass(frozen=True, slots=True)
class Attempt:
    seed: int
    status: AttemptStatus
    # Non-completed attempts can retain partial cost; absence means unknown, never zero.
    steps: int | None = None
    milliseconds: float | None = None


@dataclass(frozen=True, slots=True)
class Cohort:
    identifier: str
    n: int
    style: str
    params: dict[str, float | int]
    partition: Partition
    block_size: int
    max_steps: int
    repair_budget: int
    attempts: tuple[Attempt, ...]


@dataclass(frozen=True, slots=True)
class Manifest:
    source_commit: str
    reference_source: str
    instrument: str
    purpose: Purpose
    cohorts: tuple[Cohort, ...]


def _mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ValueError(f"{label} must be an object with string keys")
    return dict(value)


def _keys(value: dict[str, object], allowed: set[str], required: set[str]) -> None:
    if set(value) - allowed or required - set(value):
        raise ValueError(
            f"unexpected fields {sorted(set(value) - allowed)}; "
            f"missing fields {sorted(required - set(value))}"
        )


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a nonempty string")
    return value


def _integer(value: object, label: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{label} must be an integer >= {minimum}")
    return value


def _finite(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be a finite number")
    try:
        number = float(value)
    except OverflowError as error:
        raise ValueError(f"{label} must be a finite number") from error
    if not math.isfinite(number):
        raise ValueError(f"{label} must be a finite number")
    return number


def _attempt(value: object) -> Attempt:
    row = _mapping(value, "attempt")
    _keys(row, {"seed", "status", "steps", "milliseconds"}, {"seed", "status"})
    seed = _integer(row["seed"], "seed")
    if seed > 0xFFFF_FFFF:
        raise ValueError("seed must fit uint32")
    status = AttemptStatus(_text(row["status"], "status"))
    steps = _integer(row["steps"], "steps") if row.get("steps") is not None else None
    ms = (
        _finite(row["milliseconds"], "milliseconds")
        if row.get("milliseconds") is not None
        else None
    )
    if ms is not None and ms < 0:
        raise ValueError("milliseconds must be nonnegative")
    if status in {AttemptStatus.COMPLETED, AttemptStatus.NOT_STARTED} and (
        steps is not None or ms is not None
    ):
        raise ValueError(
            "completed costs come from trial rows; not-started attempts have no cost"
        )
    return Attempt(seed, status, steps, ms)


def _cohort(value: object) -> Cohort:
    row = _mapping(value, "cohort")
    fields = {
        "id",
        "n",
        "style",
        "params",
        "partition",
        "block_size",
        "max_steps",
        "repair_budget",
        "attempts",
    }
    _keys(row, fields, fields)
    parameters = _mapping(row["params"], "params")
    params = {key: _finite(number, f"parameter {key}") for key, number in parameters.items()}
    raw_attempts = row["attempts"]
    if not isinstance(raw_attempts, list):
        raise TypeError("attempts must be an ordered list")
    attempts = tuple(_attempt(item) for item in raw_attempts)
    if len({attempt.seed for attempt in attempts}) != len(attempts):
        raise ValueError("seeds must be unique within a cohort")
    return Cohort(
        identifier=_text(row["id"], "id"),
        n=_integer(row["n"], "n", 1),
        style=_text(row["style"], "style"),
        params=params,
        partition=Partition(_text(row["partition"], "partition")),
        block_size=_integer(row["block_size"], "block_size", 1),
        max_steps=_integer(row["max_steps"], "max_steps", 1),
        repair_budget=_integer(row["repair_budget"], "repair_budget", 1),
        attempts=attempts,
    )


def read_manifest(value: object) -> Manifest:
    """Reject ambiguous partitions, duplicate seeds, and unbounded work declarations."""
    row = _mapping(value, "manifest")
    fields = {"schema", "source_commit", "reference_source", "instrument", "purpose", "cohorts"}
    _keys(row, fields, fields)
    if row["schema"] != SCHEMA:
        raise ValueError(f"unsupported manifest schema; expected {SCHEMA}")
    commit = _text(row["source_commit"], "source_commit")
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise ValueError("source_commit must be a full Git revision")
    raw_cohorts = row["cohorts"]
    if not isinstance(raw_cohorts, list):
        raise TypeError("cohorts must be a list")
    cohorts = tuple(_cohort(value) for value in raw_cohorts)
    if len({cohort.identifier for cohort in cohorts}) != len(cohorts):
        raise ValueError("cohort IDs must be unique")
    tuning = {
        attempt.seed
        for cohort in cohorts
        if cohort.partition is Partition.TUNING
        for attempt in cohort.attempts
    }
    held_out = {
        attempt.seed
        for cohort in cohorts
        if cohort.partition is Partition.HELD_OUT
        for attempt in cohort.attempts
    }
    if tuning & held_out:
        raise ValueError("tuning and held-out seed partitions must be disjoint")
    return Manifest(
        source_commit=commit,
        reference_source=_text(row["reference_source"], "reference_source"),
        instrument=_text(row["instrument"], "instrument"),
        purpose=Purpose(_text(row["purpose"], "purpose")),
        cohorts=cohorts,
    )
