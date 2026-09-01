"""Exact data and canonical manifests for weighted-point certificate checks."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, is_dataclass
from fractions import Fraction
from typing import Any


@dataclass(frozen=True, slots=True)
class Atom:
    label: str
    x: Fraction
    y: Fraction
    weight: Fraction


@dataclass(frozen=True, slots=True)
class Direction:
    label: str
    ux: Fraction
    uy: Fraction
    vx: Fraction
    vy: Fraction

    def __post_init__(self) -> None:
        if self.ux * self.vy == self.uy * self.vx:
            raise ValueError("direction axes must be linearly independent")


@dataclass(frozen=True, slots=True)
class TranslationDomain:
    x_low: Fraction
    x_high: Fraction
    y_low: Fraction
    y_high: Fraction

    def __post_init__(self) -> None:
        if self.x_high < self.x_low or self.y_high < self.y_low:
            raise ValueError("translation-domain bounds are reversed")


@dataclass(frozen=True, slots=True)
class Fixture:
    atoms: tuple[Atom, ...]
    directions: tuple[Direction, ...]
    window_side: Fraction
    domain: TranslationDomain

    def __post_init__(self) -> None:
        if not self.atoms:
            raise ValueError("fixture must contain an atom")
        if not self.directions:
            raise ValueError("fixture must contain a direction")
        if self.window_side <= 0:
            raise ValueError("window side must be positive")
        labels = [atom.label for atom in self.atoms]
        if len(set(labels)) != len(labels):
            raise ValueError("atom labels must be unique")


@dataclass(frozen=True, slots=True)
class DirectionManifest:
    label: str
    direction: tuple[Fraction, Fraction, Fraction, Fraction]
    x_events: tuple[Fraction, ...]
    y_events: tuple[Fraction, ...]
    x_event_hash: str
    y_event_hash: str
    event_cell_count: int
    evaluated_state_count: int
    minimum: Fraction
    witness: tuple[Fraction, Fraction]


@dataclass(frozen=True, slots=True)
class CertificateManifest:
    atom_count: int
    atom_hash: str
    total_weight: Fraction
    direction_count: int
    direction_hash: str
    rows: tuple[DirectionManifest, ...]
    global_minimum: Fraction


def _jsonable(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return _jsonable(asdict(value))
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in sorted(value.items())}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def canonical_json(value: object) -> str:
    """Serialize dataclass or collection values without float conversion."""

    return json.dumps(_jsonable(value), sort_keys=True, separators=(",", ":"))


def canonical_hash(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def scaling_preconditions(
    *, outer_side: Fraction, internal_side: Fraction, shrink_margin: Fraction
) -> tuple[bool, bool, bool]:
    """Return the exact positivity and decomposition guards used by the wrapper."""

    return (
        outer_side > 0,
        internal_side > 0 and shrink_margin > 0,
        outer_side == internal_side + shrink_margin,
    )
