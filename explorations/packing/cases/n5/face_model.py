"""Exact equal-side feasible face for the retained five-square construction."""

from __future__ import annotations

from dataclasses import dataclass

from sqpack.field import FieldElement, NumberField


@dataclass(frozen=True)
class EqualSideFace:
    field: NumberField
    side: FieldElement
    delta: FieldElement
    fixed_centres: tuple[tuple[FieldElement, FieldElement], ...]
    moving_start: tuple[FieldElement, FieldElement]
    orientations: tuple[str, ...]


def build_equal_side_face() -> EqualSideFace:
    field = NumberField([1, 0, -2], (1, 2))
    q, root = field.rational, field.alpha
    side = q(1) + 5 * root / 4
    delta = 3 * root / 2 - 2
    fixed = (
        (q(1) / 2 + 5 * root / 4, q(1) / 2),
        (q(1) / 2, q(1) / 2),
        (q(1) + 3 * root / 4, q(1) + 3 * root / 4),
        (q(1) / 2 + 5 * root / 8, q(3) / 2 - root / 8),
    )
    return EqualSideFace(
        field,
        side,
        delta,
        fixed,
        (q(1) / 2, q(5) / 2 - root / 4),
        ("axis", "axis", "axis", "diagonal", "diagonal"),
    )


def centres_at(
    face: EqualSideFace, parameter: FieldElement
) -> tuple[tuple[FieldElement, FieldElement], ...]:
    if (
        parameter.field is not face.field
        or parameter.sign() < 0
        or (face.delta - parameter).sign() < 0
    ):
        raise ValueError("face parameter lies outside the certified interval")
    x, y = face.moving_start
    return ((x + parameter, y + parameter), *face.fixed_centres)
