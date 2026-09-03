"""Frozen side semantics for the digest-bound UnitSquare n = 68 parent.

Exp-054 admitted a production adapter whose reported side token is deliberately
unbound, so `production_model_factory(..., side=None)` returns three typed
`serialization-refusal` outcomes.  This module is the exp-057 binding: it reads the
reported token under each declared serialization model and returns the exact rational
side that model admits, refusing an unbound or malformed token, a wrong direction, a
wrong quantum, a threshold wider than one quarter of the released gain, and a changed
released gain.

Nothing here parses a source, opens a channel or edits a frozen file.  Every guard
raises a typed error rather than asserting, so receipts are identical under `python -O`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from fractions import Fraction
from typing import Final, Literal

from cases.unitsquare_precision.production.adapter import REPORTED_SIDE_TOKEN

type SideDirection = Literal["exact", "symmetric", "away-from-zero"]

RELEASED_GAIN: Final = Fraction(768618004216131, 10**19)
"""The released n = 68 improvement `7.68618004216131e-5`, as an exact rational."""

QUARTER_GAIN: Final = RELEASED_GAIN / 4
"""X-011's directional ceiling: every threshold is at most one quarter of the gain."""

SIX_DECIMAL_QUANTUM: Final = Fraction(1, 1_000_000)
"""The quantum the `nearest-6` and `truncate-6` models already declare."""

MODEL_ORDER: Final = ("declared:svg-literal", "nearest-6", "truncate-6")
"""X-011's fixed parent model order: `declared:<stable-id>`, `nearest-6`, `truncate-6`."""

MODEL_DIRECTIONS: Final[dict[str, SideDirection]] = {
    "declared:svg-literal": "exact",
    "nearest-6": "symmetric",
    "truncate-6": "away-from-zero",
}
"""Each model's declared interval placement, mirroring `adapter._source_interval`."""

_EXACT_DECIMAL = re.compile(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)\Z")


class SideSemanticsError(ValueError):
    """A typed refusal in the frozen side binding."""


class UnboundTokenError(SideSemanticsError):
    """No reported side token was supplied, so no side may be invented."""


class MalformedTokenError(SideSemanticsError):
    """The reported side token is not one exact finite decimal."""


class UnknownModelError(SideSemanticsError):
    """The requested model is not one of the three declared models."""


class DirectionError(SideSemanticsError):
    """The declared interval direction contradicts the model's own rule."""


class QuantumError(SideSemanticsError):
    """The declared quantum is not the frozen six-decimal quantum."""


class ThresholdError(SideSemanticsError):
    """A directional threshold exceeds one quarter of the released gain."""


class ReleasedGainError(SideSemanticsError):
    """The released gain is not the frozen `7.68618004216131e-5`."""


@dataclass(frozen=True, slots=True)
class SideBinding:
    """One model's admitted side interval and the scalar the frozen factory accepts."""

    model: str
    lower: Fraction
    upper: Fraction
    scalar: Fraction
    direction: SideDirection
    quantum: Fraction

    def __post_init__(self) -> None:
        if self.lower > self.upper:
            raise SideSemanticsError("side interval is empty")
        if self.lower <= 0:
            raise SideSemanticsError("normalized side interval must be positive")
        if not self.lower <= self.scalar <= self.upper:
            raise SideSemanticsError("admitted scalar lies outside its declared interval")

    @property
    def width(self) -> Fraction:
        """The declared container-side interval width, exactly."""

        return self.upper - self.lower

    def to_document(self) -> dict[str, str]:
        """Sanitized exact strings for a canonical receipt; no source text is retained."""

        return {
            "model": self.model,
            "direction": self.direction,
            "lower": str(self.lower),
            "upper": str(self.upper),
            "scalar": str(self.scalar),
            "quantum": str(self.quantum),
            "width": str(self.width),
        }


def _exact_decimal(token: str | None) -> Fraction:
    if token is None or not token.strip():
        raise UnboundTokenError("reported side token is unbound")
    text = token.strip()
    if _EXACT_DECIMAL.fullmatch(text) is None:
        raise MalformedTokenError("reported side token is not one exact finite decimal")
    try:
        value = Fraction(text)
    except (ValueError, ZeroDivisionError) as error:
        raise MalformedTokenError("reported side token is not an exact rational") from error
    if value <= 0:
        raise MalformedTokenError("reported side token must be positive")
    return value


def bind_side(
    model: str,
    *,
    token: str | None = REPORTED_SIDE_TOKEN,
    direction: SideDirection | None = None,
    quantum: Fraction = SIX_DECIMAL_QUANTUM,
    released_gain: Fraction = RELEASED_GAIN,
) -> SideBinding:
    """Bind one declared model's side from the reported token, or refuse with a type.

    The literal model keeps the exact decimal rational the token prints.  The two
    six-decimal models keep the closed one-quantum interval they already declare for a
    source coordinate token: symmetric about the printed value for `nearest-6`, and away
    from zero for `truncate-6`.  Each returns the single scalar the frozen
    `production_model_factory` accepts, which lies inside its own declared interval.
    """

    if released_gain != RELEASED_GAIN:
        raise ReleasedGainError("released gain is not the frozen 7.68618004216131e-5")
    if model not in MODEL_ORDER:
        raise UnknownModelError(f"unknown declared model: {model}")
    declared = MODEL_DIRECTIONS[model]
    if direction is not None and direction != declared:
        raise DirectionError(f"{model} declares direction {declared}, not {direction}")
    if quantum <= 0:
        raise QuantumError("declared quantum must be positive")
    if quantum > released_gain / 4:
        raise ThresholdError("declared threshold exceeds one quarter of the released gain")
    if quantum != SIX_DECIMAL_QUANTUM:
        raise QuantumError("declared quantum is not the frozen six-decimal quantum")
    value = _exact_decimal(token)
    if declared == "exact":
        lower, upper = value, value
    elif declared == "symmetric":
        lower, upper = value - quantum / 2, value + quantum / 2
    else:
        lower, upper = value, value + quantum
    if upper - lower > released_gain / 4:
        raise ThresholdError("side interval width exceeds one quarter of the released gain")
    return SideBinding(model, lower, upper, value, declared, quantum)


def bind_all_sides(
    *,
    token: str | None = REPORTED_SIDE_TOKEN,
    quantum: Fraction = SIX_DECIMAL_QUANTUM,
    released_gain: Fraction = RELEASED_GAIN,
) -> tuple[SideBinding, ...]:
    """Bind every declared model in X-011's frozen order, refusing on the first fault."""

    return tuple(
        bind_side(model, token=token, quantum=quantum, released_gain=released_gain)
        for model in MODEL_ORDER
    )


def semantics_document(*, token: str | None = REPORTED_SIDE_TOKEN) -> dict[str, object]:
    """Canonical, sanitized receipt fields for the frozen binding."""

    bindings = bind_all_sides(token=token)
    return {
        "format": "UnitSquareBoundSideSemantics/v1",
        "reported_side_token": (token or "").strip(),
        "released_improvement": str(RELEASED_GAIN),
        "quarter_threshold": str(QUARTER_GAIN),
        "model_order": list(MODEL_ORDER),
        "bindings": [binding.to_document() for binding in bindings],
    }
