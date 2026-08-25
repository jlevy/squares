"""Source-preserving numeric projection and stable SVG formatting."""

from __future__ import annotations

import math
from decimal import Decimal, InvalidOperation, localcontext
from fractions import Fraction
from typing import Protocol

from sqpack.render.model import EvidenceTier, ScalarKind, ScalarSource, validate_scalar_source

DEFAULT_SIGNIFICANT_DIGITS = 17
EXACT_SIGNIFICANT_DIGITS = 32
VISIBLE_DIGITS = 10
MAX_PLAIN_DECIMAL_EXPONENT = 100


class ExactDecimal(Protocol):
    def __float__(self) -> float: ...


def project_decimal(value: Decimal, significant_digits: int) -> Decimal:
    if significant_digits < 1 or not value.is_finite():
        raise ValueError("projection requires a finite value and positive precision")
    if value.is_zero():
        return Decimal(0)
    with localcontext() as context:
        context.prec = significant_digits
        return +value


def scalar_from_float(
    value: float, *, precision: int = DEFAULT_SIGNIFICANT_DIGITS
) -> ScalarSource:
    if not math.isfinite(value):
        raise ValueError("binary64 scalar must be finite")
    source = repr(value)
    result = ScalarSource(
        ScalarKind.BINARY64, source, project_decimal(Decimal(source), precision), precision
    )
    validate_scalar_source(result)
    return result


def scalar_from_decimal(
    value: Decimal | str | int, *, precision: int | None = None
) -> ScalarSource:
    try:
        decimal_value = value if isinstance(value, Decimal) else Decimal(value)
    except InvalidOperation as error:
        raise ValueError("invalid decimal scalar") from error
    digits = precision or max(1, len(decimal_value.as_tuple().digits))
    source = str(value)
    result = ScalarSource(
        ScalarKind.DECIMAL, source, project_decimal(decimal_value, digits), digits
    )
    validate_scalar_source(result)
    return result


def scalar_from_fraction(
    value: Fraction, *, precision: int = EXACT_SIGNIFICANT_DIGITS
) -> ScalarSource:
    source = (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )
    with localcontext() as context:
        context.prec = precision + 8
        projected = Decimal(value.numerator) / Decimal(value.denominator)
    result = ScalarSource(
        ScalarKind.RATIONAL, source, project_decimal(projected, precision), precision, source
    )
    validate_scalar_source(result)
    return result


def scalar_from_exact(
    source: str,
    projected: Decimal | str | float,
    *,
    precision: int = EXACT_SIGNIFICANT_DIGITS,
) -> ScalarSource:
    decimal_value = (
        Decimal(repr(projected)) if isinstance(projected, float) else Decimal(projected)
    )
    result = ScalarSource(
        ScalarKind.EXACT, source, project_decimal(decimal_value, precision), precision, source
    )
    validate_scalar_source(result)
    return result


def format_svg_number(value: Decimal | ScalarSource | Fraction | int | float) -> str:
    if isinstance(value, ScalarSource):
        decimal_value = value.projected
    elif isinstance(value, Fraction):
        decimal_value = Decimal(value.numerator) / Decimal(value.denominator)
    elif isinstance(value, Decimal):
        decimal_value = value
    else:
        decimal_value = Decimal(str(value))
    if not decimal_value.is_finite():
        raise ValueError("SVG number must be finite")
    if decimal_value.is_zero():
        return "0"
    if abs(decimal_value.adjusted()) > MAX_PLAIN_DECIMAL_EXPONENT:
        raise ValueError("SVG number lies outside the plain-decimal policy")
    text = format(decimal_value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def format_visible_number(
    value: ScalarSource,
    evidence: EvidenceTier,
    *,
    digits: int = VISIBLE_DIGITS,
) -> tuple[str, str]:
    projected = project_decimal(value.projected, digits)
    relation = "=" if value.kind in (ScalarKind.RATIONAL, ScalarKind.EXACT) else "~"
    if evidence is EvidenceTier.CERTIFIED_UPPER_BOUND:
        relation = "<="
    return relation, format_svg_number(projected)


def format_points(points) -> str:
    return " ".join(
        f"{format_svg_number(point.x)},{format_svg_number(point.y)}" for point in points
    )


def format_values(values) -> str:
    return " ".join(format_svg_number(value) for value in values)
