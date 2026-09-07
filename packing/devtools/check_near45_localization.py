"""Independent H-123 polynomial reader; imports arithmetic, not producer geometry.

Target polynomials are reconstructed lazily. The source-free seams below operate on
unrelated widths and polynomials; a failed sufficient certificate is never a refutation.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from math import comb
from pathlib import Path
from typing import Any

from sqpack.field import FieldElement, NumberField

type Polynomial = tuple[FieldElement, ...]
type Slab = tuple[Fraction, Fraction]

MAX_PACKET_BYTES = 65536
INVENTORY = ((0, "F"), (0, "G"), (1, "F"), (1, "G"))
KEYS = {
    "version",
    "kind",
    "hypothesis",
    "side",
    "width",
    "coefficient_basis",
    "half_angle_slabs",
    "coefficients",
    "obligations",
    "status",
    "stop_reason",
}


@dataclass(frozen=True)
class Specification:
    field: NumberField
    side: Fraction
    width: Fraction
    slabs: tuple[Slab, Slab]
    polynomials: dict[str, Polynomial]


@dataclass(frozen=True)
class Obligation:
    slab: int
    polynomial: str
    coefficients: Polynomial
    claimed: bool


class GuardError(ValueError):
    """The receipt or sufficient certificate does not establish the claim."""


def make_field() -> NumberField:
    """The fixed positive sqrt(2) embedding for all exact coefficient arithmetic."""
    return NumberField((1, 0, -2), (1, 2))


def poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
    """Preserve the declared coefficient lengths, including trailing zeros."""
    if not left or not right:
        raise GuardError("empty polynomial")
    zero = left[0].field.zero
    return tuple(
        (left[i] if i < len(left) else zero) + (right[i] if i < len(right) else zero)
        for i in range(max(len(left), len(right)))
    )


def poly_scale(poly: Polynomial, factor: Fraction) -> Polynomial:
    return tuple(value * factor for value in poly)


def poly_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    if not left or not right:
        raise GuardError("empty polynomial")
    result = [left[0].field.zero for _ in range(len(left) + len(right) - 1)]
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = result[i + j] + a * b
    return tuple(result)


def guard_polynomials(field: NumberField, width: Fraction) -> dict[str, Polynomial]:
    """Derive DF and D^2G by symbolic polynomial operations, not a copied coefficient list."""
    one, zero, root_half = field.one, field.zero, field.alpha / 2
    denominator = (one, zero, one)
    cosine_numerator = (root_half, -2 * root_half, -root_half)
    sine_numerator = (root_half, 2 * root_half, -root_half)
    combination = poly_add(cosine_numerator, poly_scale(sine_numerator, Fraction(1, 2)))
    f_guard = poly_add(denominator, poly_scale(combination, -width))
    g_guard = poly_add(
        poly_multiply(
            denominator, poly_scale(poly_add(cosine_numerator, sine_numerator), Fraction(1, 2))
        ),
        poly_scale(poly_multiply(sine_numerator, combination), -width),
    )
    return {"F": f_guard, "G": g_guard}


def bernstein(poly: Polynomial, lower: Fraction, upper: Fraction) -> Polynomial:
    """Affine substitution followed by the exact monomial-to-Bernstein identity."""
    if (
        not poly
        or not isinstance(lower, Fraction)
        or not isinstance(upper, Fraction)
        or lower >= upper
    ):
        raise GuardError(
            "Bernstein conversion requires a nonempty polynomial and exact increasing endpoints"
        )
    degree = len(poly) - 1
    field = poly[0].field
    power = tuple(
        sum(
            (
                poly[k] * comb(k, j) * lower ** (k - j) * (upper - lower) ** j
                for k in range(j, degree + 1)
            ),
            field.zero,
        )
        for j in range(degree + 1)
    )
    return tuple(
        sum(
            (power[j] * Fraction(comb(i, j), comb(degree, j)) for j in range(i + 1)), field.zero
        )
        for i in range(degree + 1)
    )


def reconstruct_target(field: NumberField) -> Specification:
    """Scientific construction: call only in a prospectively authorized reader run."""
    side = Fraction(1939, 500)
    width = side / 2 - 1
    radius = Fraction(110880, 50803079)
    return Specification(
        field,
        side,
        width,
        ((-radius, Fraction(0)), (Fraction(0), radius)),
        guard_polynomials(field, width),
    )


def _rational(raw: Any) -> Fraction:
    if not isinstance(raw, str) or not raw or len(raw) > 512:
        raise GuardError("expected a bounded canonical rational string")
    try:
        value = Fraction(raw)
    except (ValueError, ZeroDivisionError) as exc:
        raise GuardError("invalid rational coefficient") from exc
    if str(value) != raw:
        raise GuardError("noncanonical rational coefficient")
    return value


def _polynomial(raw: Any, field: NumberField, length: int) -> Polynomial:
    if not isinstance(raw, list) or len(raw) != length:
        raise GuardError("truncated or extended native coefficient inventory")
    result: list[FieldElement] = []
    for pair in raw:
        if not isinstance(pair, list) or len(pair) != 2:
            raise GuardError("each coefficient needs the exact two-element basis")
        result.append(field.element(tuple(_rational(value) for value in pair)))
    return tuple(result)


def _parse(raw: Any, field: NumberField) -> tuple[Specification, tuple[Obligation, ...]]:
    """Complete admission precedes any reconstruction of scientific polynomials."""
    if not isinstance(raw, dict) or set(raw) != KEYS:
        raise GuardError("missing, extra, or nonobject packet fields")
    if (
        type(raw["version"]) is not int
        or raw["version"] != 1
        or raw["kind"] != "fixed-side-near45-localization-overlap"
        or raw["hypothesis"] != "H-123"
        or raw["coefficient_basis"] != ["1", "sqrt2-positive"]
    ):
        raise GuardError("foreign version, hypothesis, kind, or field embedding")
    if raw["status"] != "proved" or raw["stop_reason"] != "complete":
        raise GuardError("incomplete, failed, or interrupted sufficient certificate")
    side, width = _rational(raw["side"]), _rational(raw["width"])
    slab_data = raw["half_angle_slabs"]
    if not isinstance(slab_data, list) or len(slab_data) != 2:
        raise GuardError("both closed slabs are required")
    slabs: list[Slab] = []
    for pair in slab_data:
        if not isinstance(pair, list) or len(pair) != 2:
            raise GuardError("each slab requires two exact endpoints")
        lower, upper = _rational(pair[0]), _rational(pair[1])
        if lower >= upper:
            raise GuardError("slab endpoints must be increasing")
        slabs.append((lower, upper))
    powers = raw["coefficients"]
    if not isinstance(powers, dict) or set(powers) != {"F", "G"}:
        raise GuardError("both reconstructed power polynomials are required")
    polynomials = {
        name: _polynomial(powers[name], field, length) for name, length in (("F", 3), ("G", 5))
    }
    entries = raw["obligations"]
    if not isinstance(entries, list) or len(entries) != 4:
        raise GuardError("complete four-obligation inventory is required")
    obligations: list[Obligation] = []
    for entry, (index, name) in zip(entries, INVENTORY, strict=True):
        if (
            not isinstance(entry, dict)
            or set(entry) != {"slab", "polynomial", "bernstein", "proved"}
            or type(entry["slab"]) is not int
            or entry["slab"] != index
            or entry["polynomial"] != name
            or type(entry["proved"]) is not bool
        ):
            raise GuardError("duplicate, foreign, or malformed obligation")
        coefficients = _polynomial(entry["bernstein"], field, 3 if name == "F" else 5)
        obligations.append(Obligation(index, name, coefficients, entry["proved"]))
    return Specification(field, side, width, (slabs[0], slabs[1]), polynomials), tuple(
        obligations
    )


def _verify(
    actual: Specification, obligations: tuple[Obligation, ...], expected: Specification
) -> dict[str, Any]:
    if (
        actual.side != expected.side
        or actual.width != expected.width
        or actual.slabs != expected.slabs
        or actual.polynomials != expected.polynomials
    ):
        raise GuardError("receipt differs from independently reconstructed identity or powers")
    checked = 0
    for obligation in obligations:
        lower, upper = expected.slabs[obligation.slab]
        recomputed = bernstein(expected.polynomials[obligation.polynomial], lower, upper)
        if recomputed != obligation.coefficients:
            raise GuardError(
                "carried Bernstein coefficients disagree with independent arithmetic"
            )
        if not all(value.sign() >= 0 for value in recomputed):
            raise GuardError(
                "sufficient Bernstein guard unresolved; this is not a counterexample"
            )
        if not obligation.claimed:
            raise GuardError("claimed boolean disagrees with the recomputed sufficient guard")
        checked += len(recomputed)
    return {
        "status": "proved",
        "complete": True,
        "obligations_checked": len(obligations),
        "bernstein_coefficients_checked": checked,
        "unresolved": [],
        "hypothesis": "H-123",
        "side": str(expected.side),
        "width": str(expected.width),
        "half_angle_slabs": [[str(value) for value in slab] for slab in expected.slabs],
        "scope": "Both polynomial guards only; geometric reduction is a separate premise.",
    }


def check_packet(raw: Any, *, expected: Specification) -> dict[str, Any]:
    """Generic source-free seam, with an explicit independently specified toy identity."""
    actual, obligations = _parse(raw, expected.field)
    return _verify(actual, obligations, expected)


def check_target_packet(raw: Any) -> dict[str, Any]:
    field = make_field()
    actual, obligations = _parse(raw, field)
    radius = Fraction(110880, 50803079)
    if (
        actual.side != Fraction(1939, 500)
        or actual.width != Fraction(939, 1000)
        or actual.slabs != ((-radius, Fraction(0)), (Fraction(0), radius))
    ):
        raise GuardError("foreign fixed side, width, or closed slab identity")
    return _verify(actual, obligations, reconstruct_target(field))


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise GuardError("duplicate JSON object key")
        result[key] = value
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        with args.input.open("rb") as stream:
            data = stream.read(MAX_PACKET_BYTES + 1)
        if len(data) > MAX_PACKET_BYTES:
            raise GuardError("packet exceeds the reader byte cap")
        raw = json.loads(data, object_pairs_hook=_unique_object)
        result = check_target_packet(raw)
    except (OSError, ValueError, RecursionError) as exc:
        reason = str(exc)
        print(
            json.dumps(
                {
                    "status": "unresolved",
                    "complete": False,
                    "unresolved": [reason],
                    "scope": "No counterexample or global packing conclusion.",
                },
                sort_keys=True,
            )
        )
        print(f"reader unresolved: {reason}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
