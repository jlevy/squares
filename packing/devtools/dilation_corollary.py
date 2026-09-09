#!/usr/bin/env python3
"""The sharp dilation-limit corollary of a fractional certificate.

Dilate every atom position, the container side ``L`` and the shrunken side ``B`` by a
positive rational factor ``q``, and leave the weights and direction net alone.
Condition 1 is equivariant under common scaling, Conditions 2 and 3 are unchanged, and
inverse dilation bijects placements while preserving covered mass, so Condition 5 is
unchanged.

The retained theorem uses the sufficient containment test ``B (1 + D) < 1``. Its proof
contains a sharper identity. If ``t = tan(d) <= D < 1`` is the angular error, then
``cos(d) + sin(d) = (1 + t) / sqrt(1 + t^2)`` is at most
``(1 + D) / sqrt(1 + D^2)``. The rational dilation therefore remains valid exactly when
``q^2 B^2 (1 + D)^2 < 1 + D^2``. Every quantity in that decision is rational even
though the factor supremum is a quadratic irrational.

No member of the strict rational family attains the supremum. Rational density and
upward embedding nevertheless promote the supremum to a weak lower bound. This limit
corollary neither certifies nor decides fit at the endpoint, and it never licenses
dividing ``L`` by ``B``.

Section 4 of the 2026-09-05 adversarial review read this off the retained
``s(11) >= 381/100`` certificate at ``a = 250001/250000``, giving
``s(11) >= 95250381/25000000 = 3.81001524``. This tool recomputes it from the file::

    uv run --frozen python -m devtools.dilation_corollary \\
        cases/n11_fractional_certificate/certificate.json --factor 250001/250000

The explicit-factor mode decides Conditions 1 to 3 and the sharpened containment test,
then inherits Condition 5 from the input file's retained decision. The
``--check-limit-record`` mode instead replays all five source conditions from the frozen
bytes before deriving and comparing the sharpened limit proof record.

A *threshold* certificate (`sqpack.fractional.threshold`) is accepted as a source too,
and is read by `devtools.decide_threshold_certificate`'s own strict decoder rather than
the point decoder, which would silently ignore its ``threshold_atoms`` and decide a
weaker object. The geometry is the point certificate's: ``B`` and ``D`` are the same
numbers, so the factor supremum is the same formula. What changes is the vocabulary and
what must be scaled. Conditions 1 and 1' are equivariant under common scaling once every
threshold atom's points move with the point atoms, Conditions 2' and 3 are unchanged,
and Condition 5' is preserved by inverse dilation for the reason Condition 5 is: the
trace of a core on a threshold atom's points is a function of containment, and dilation
is a containment-preserving bijection on placements. A threshold source declares
``total_budget`` and ``least_cell_charge`` where a point source declares ``total_mass``
and ``least_cell_mass``, and its limit record is written in the ``v3`` schema, whose
``source.variant`` says which shape it was derived from. Point sources keep emitting the
``v2`` record unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from dataclasses import dataclass, replace
from decimal import ROUND_HALF_UP, Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import cast

from strif import atomic_output_file

from devtools.decide_certificate import load_frozen_bytes, read_bounded
from devtools.decide_threshold_certificate import load as load_threshold_bytes
from sqpack.fractional.certificate import (
    Certificate,
    ConditionReport,
    Verdict,
    closed_form_conditions,
    verify,
)
from sqpack.fractional.threshold import (
    ThresholdCertificate,
    closed_form_threshold_conditions,
    verify_threshold,
)

AnyCertificate = Certificate | ThresholdCertificate
"""Either shape of frozen source this tool derives a limit corollary from."""

LIMIT_RECORD_SCHEMA = "packing.squares:FractionalDilationLimitCorollary/v2"
"""Record type emitted by the strict-family limit proof from a point certificate."""

THRESHOLD_LIMIT_RECORD_SCHEMA = "packing.squares:FractionalDilationLimitCorollary/v3"
"""Record type emitted from a threshold certificate; ``source.variant`` names the shape."""

POINT_VARIANT = "point"
THRESHOLD_VARIANT = "threshold"

LIMIT_DECIMAL_PLACES = 15
"""Reader decimal carried beside the exact limit; it never enters a decision."""


def point_view(certificate: AnyCertificate) -> Certificate:
    """The point certificate carrying the geometry the dilation theorem reads."""

    if isinstance(certificate, ThresholdCertificate):
        return certificate.point_certificate
    return certificate


def _closed_form(certificate: AnyCertificate) -> tuple[ConditionReport, ...]:
    if isinstance(certificate, ThresholdCertificate):
        return closed_form_threshold_conditions(certificate)
    return closed_form_conditions(certificate)


def _declared_budget(certificate: AnyCertificate) -> Fraction:
    """``Condition 2'``'s budget for a threshold source, the total mass for a point one."""

    if isinstance(certificate, ThresholdCertificate):
        return certificate.total_budget
    return certificate.total_mass


def _declares_threshold_atoms(raw: bytes) -> bool:
    """Peek at a record's shape to choose a decoder.

    This decides nothing: whichever strict decoder it selects reads the same bytes again
    and refuses everything it refuses today, duplicate keys and inexact numbers included.
    A record that declares neither the threshold variant nor threshold atoms is read by
    the point decoder exactly as before.
    """

    try:
        peeked = cast(object, json.loads(raw))
    except UnicodeError, ValueError, RecursionError:
        return False
    if not isinstance(peeked, dict):
        return False
    record = cast(dict[str, object], peeked)
    return record.get("variant") == THRESHOLD_VARIANT or "threshold_atoms" in record


def load_source(raw: bytes) -> tuple[AnyCertificate, dict[str, object]]:
    """Rebuild a frozen source with the strict decoder that matches its shape."""

    if _declares_threshold_atoms(raw):
        return load_threshold_bytes(raw)
    return load_frozen_bytes(raw)


def coarse_condition_four_ceiling(certificate: AnyCertificate) -> Fraction:
    """The rational factor ceiling from the retained theorem's sufficient Condition 4."""

    point = point_view(certificate)
    return 1 / (point.square_side * (1 + point.largest_half_gap_tangent))


@dataclass(frozen=True, slots=True)
class PositiveQuadraticSurd:
    """A positive value ``coefficient * sqrt(radicand)``, carried without rounding."""

    coefficient: Fraction
    radicand: int

    def __post_init__(self) -> None:
        if self.coefficient <= 0 or self.radicand <= 0:
            raise ValueError("a positive quadratic surd needs positive inputs")

    @property
    def squared(self) -> Fraction:
        """The exact rational square of the value."""

        return self.coefficient * self.coefficient * self.radicand

    @property
    def exact(self) -> str:
        """A deterministic radical expression for records and prose."""

        numerator = self.coefficient.numerator
        denominator = self.coefficient.denominator
        if denominator == 1:
            prefix = "" if numerator == 1 else f"{numerator}*"
            return f"{prefix}sqrt({self.radicand})"
        return f"{numerator}*sqrt({self.radicand})/{denominator}"

    @property
    def irrational(self) -> bool:
        """Whether the integer radicand is not a perfect square."""

        root = math.isqrt(self.radicand)
        return root * root != self.radicand

    @property
    def defining_polynomial(self) -> str:
        """A primitive integer polynomial whose positive root is this value."""

        leading = self.coefficient.denominator**2
        constant = self.coefficient.numerator**2 * self.radicand
        content = math.gcd(leading, constant)
        return f"{leading // content}*x^2 - {constant // content}"

    def scaled(self, factor: Fraction) -> PositiveQuadraticSurd:
        """Multiply the surd by a positive rational factor."""

        if factor <= 0:
            raise ValueError("a positive quadratic surd needs a positive scale")
        return PositiveQuadraticSurd(self.coefficient * factor, self.radicand)


def sharp_dilation_ceiling(certificate: AnyCertificate) -> PositiveQuadraticSurd:
    """``sqrt(1 + D^2) / (B (1 + D))``, the unattained sharp factor supremum.

    The proof uses monotonicity of ``(1 + t) / sqrt(1 + t^2)`` on ``0 <= t <= D``.
    This implementation deliberately refuses ``D >= 1`` rather than silently applying
    that monotonicity outside its domain. A threshold certificate carries the same two
    numbers, so it gets the same formula from its point view.
    """

    point = point_view(certificate)
    gap = point.largest_half_gap_tangent
    if not (0 <= gap < 1):
        raise ValueError(f"the sharpened dilation proof requires 0 <= D < 1, not {gap}")
    numerator = gap.numerator
    denominator = gap.denominator
    radicand = denominator * denominator + numerator * numerator
    coefficient = Fraction(
        point.square_side.denominator,
        point.square_side.numerator * (denominator + numerator),
    )
    return PositiveQuadraticSurd(coefficient, radicand)


def sharp_containment_holds(certificate: AnyCertificate, factor: Fraction) -> bool:
    """Decide the sharpened strict containment inequality using rationals only."""

    if factor <= 0:
        return False
    point = point_view(certificate)
    gap = point.largest_half_gap_tangent
    if not (0 <= gap < 1):
        raise ValueError(f"the sharpened dilation proof requires 0 <= D < 1, not {gap}")
    return (factor * point.square_side * (1 + gap)) ** 2 < 1 + gap * gap


def dilate[C: AnyCertificate](certificate: C, factor: Fraction) -> C:
    """Scale the geometric data after deciding the sharpened containment theorem.

    Every atom coordinate moves, threshold-atom points included: they are container
    coordinates of the same kind, and a threshold atom whose points stayed behind would
    charge a different set of cores.
    """

    if factor <= 0:
        raise ValueError(f"a dilation factor must be positive, not {factor}")
    ceiling = sharp_dilation_ceiling(certificate)
    if not sharp_containment_holds(certificate, factor):
        raise ValueError(
            f"factor {factor} has square {factor * factor}, not below the sharp ceiling "
            f"square {ceiling.squared}; strict containment fails"
        )
    scaled = replace(
        certificate,
        outer_side=certificate.outer_side * factor,
        square_side=certificate.square_side * factor,
        atoms=tuple(
            replace(atom, x=atom.x * factor, y=atom.y * factor) for atom in certificate.atoms
        ),
    )
    if isinstance(scaled, ThresholdCertificate):
        return cast(
            C,
            replace(
                scaled,
                threshold_atoms=tuple(
                    replace(
                        threshold_atom,
                        points=tuple(
                            (x * factor, y * factor) for x, y in threshold_atom.points
                        ),
                    )
                    for threshold_atom in scaled.threshold_atoms
                ),
            ),
        )
    return scaled


@dataclass(frozen=True, slots=True)
class Corollary:
    """The rational-factor corollary's exact decision values."""

    factor: Fraction
    half_gap_tangent: Fraction
    coarse_containment: Fraction
    sharp_containment_left_squared: Fraction
    sharp_containment_right: Fraction
    factor_supremum: PositiveQuadraticSurd
    bounded_side: Fraction
    unchanged_condition_failures: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class LimitCorollary:
    """The weak bound obtained from every strict rational dilation."""

    factor_supremum: PositiveQuadraticSurd
    bounded_side: PositiveQuadraticSurd
    relation: str = ">="
    endpoint_certificate: bool = False
    requires_compactness: bool = False


def corollary(certificate: AnyCertificate, factor: Fraction) -> Corollary:
    """Decide one rational member of the sharpened strict dilation family."""

    dilated = dilate(certificate, factor)
    point = point_view(certificate)
    gap = point.largest_half_gap_tangent
    ceiling = sharp_dilation_ceiling(certificate)
    unchanged = tuple(
        condition.name
        for condition in _closed_form(dilated)
        if not condition.holds and not condition.name.startswith("Condition 4 ")
    )
    return Corollary(
        factor=factor,
        half_gap_tangent=gap,
        coarse_containment=point.square_side * (1 + gap),
        sharp_containment_left_squared=(factor * point.square_side * (1 + gap)) ** 2,
        sharp_containment_right=1 + gap * gap,
        factor_supremum=ceiling,
        bounded_side=point_view(dilated).bounded_side,
        unchanged_condition_failures=unchanged,
    )


def _accepted_source(certificate: AnyCertificate, verdict: Verdict) -> None:
    """Refuse a limit argument whose finite certificate premise was not decided."""

    expected = _closed_form(certificate)
    reported = {condition.name: condition for condition in verdict.conditions}
    closed_form_matches = all(
        reported.get(condition.name) == condition for condition in expected
    )
    has_condition_five = any(
        name.startswith(("Condition 5 ", "Condition 5' ")) for name in reported
    )
    if (
        not verdict.accepted
        or not all(condition.holds for condition in expected)
        or not closed_form_matches
        or not has_condition_five
    ):
        raise ValueError("source certificate is not accepted on all five conditions")
    if verdict.total_mass != _declared_budget(certificate):
        raise ValueError("source verdict's total mass does not match the certificate")
    if verdict.minimum_cell_mass is None or verdict.minimum_cell_mass < 1:
        raise ValueError("source verdict has no accepted Condition 5 minimum")


def _decide_limit(
    certificate: AnyCertificate, *, workers: int | None = None
) -> tuple[LimitCorollary, Verdict]:
    """Replay the source certificate and derive the sharp limit from that verdict.

    A threshold source is replayed by the threshold theorem's own exact sweep, the same
    route the retention gate's exact side runs; nothing here reuses a stored verdict.
    """

    if isinstance(certificate, ThresholdCertificate):
        verdict = verify_threshold(certificate, workers=workers or 1)
    else:
        verdict = verify(certificate, workers=workers)
    _accepted_source(certificate, verdict)
    factor_supremum = sharp_dilation_ceiling(certificate)
    return (
        LimitCorollary(
            factor_supremum=factor_supremum,
            bounded_side=factor_supremum.scaled(certificate.outer_side),
        ),
        verdict,
    )


def limit_corollary(
    certificate: AnyCertificate, *, workers: int | None = None
) -> LimitCorollary:
    """Return the supremum bound carried by all strict rational dilations.

    For each rational ``q`` with ``0 < q < c``, where
    ``c = sqrt(1 + D^2) / (B (1 + D))``, the sharpened containment theorem gives a
    strict-subfactor no-fit proof at ``q L``. Therefore ``s(n) >= q L`` for every such
    ``q``. Their supremum is ``c L``, so order completeness gives ``s(n) >= c L``.
    Equivalently, if a real ``x < c L`` admitted a packing, rational density would give
    ``x/L < q < c``; embedding that packing in side ``q L`` would contradict the
    corresponding strict-subfactor proof.

    At equality the sharpened containment inequality is no longer strict. The argument
    neither supplies an endpoint certificate nor decides whether a packing exists at
    ``c L``. It uses no compactness or attainment theorem.
    """

    result, _verdict = _decide_limit(certificate, workers=workers)
    return result


def rational_subfactor_above(certificate: AnyCertificate, candidate_side: Fraction) -> Fraction:
    """A rational factor ``q < c`` whose no-fit side exceeds a rational candidate.

    A direct rational increment against the exact square of the irrational ceiling
    produces the witness. The theorem for an arbitrary real candidate uses density of
    the rationals in the same open interval.
    """

    if candidate_side < 0:
        raise ValueError(
            f"a candidate container side must be nonnegative, not {candidate_side}"
        )
    result = sharp_dilation_ceiling(certificate)
    bounded_side_squared = certificate.outer_side**2 * result.squared
    if candidate_side * candidate_side >= bounded_side_squared:
        raise ValueError(
            f"candidate side {candidate_side} is not below the positive limit whose "
            f"square is {bounded_side_squared}"
        )
    lower_factor = candidate_side / certificate.outer_side
    square_slack = result.squared - lower_factor * lower_factor
    increment = min(Fraction(1), square_slack / (2 * (2 * lower_factor + 1)))
    factor = lower_factor + increment
    if not (factor > lower_factor and factor * factor < result.squared):  # pragma: no cover
        raise AssertionError("direct rational witness missed the strict dilation interval")
    return factor


def _decimal(value: PositiveQuadraticSurd) -> str:
    quantum = Decimal(1).scaleb(-LIMIT_DECIMAL_PLACES)
    with localcontext() as context:
        context.prec = (
            max(
                len(str(value.coefficient.numerator)),
                len(str(value.coefficient.denominator)),
                len(str(value.radicand)),
            )
            + LIMIT_DECIMAL_PLACES
            + 20
        )
        decimal = (
            Decimal(value.coefficient.numerator)
            * Decimal(value.radicand).sqrt()
            / Decimal(value.coefficient.denominator)
        )
        return format(decimal.quantize(quantum, rounding=ROUND_HALF_UP), "f")


def build_limit_record(
    certificate_path: Path,
    *,
    source_name: str | None = None,
    workers: int | None = None,
) -> dict[str, object]:
    """Re-decide a frozen certificate and derive its strict-family limit record."""

    raw = read_bounded(certificate_path)
    certificate, declared = load_source(raw)
    result, verdict = _decide_limit(certificate, workers=workers)
    if read_bounded(certificate_path) != raw:
        raise ValueError("source certificate changed while the limit record was built")

    threshold = isinstance(certificate, ThresholdCertificate)
    total_field = "total_budget" if threshold else "total_mass"
    least_field = "least_cell_charge" if threshold else "least_cell_mass"
    declared_total = declared.get(total_field)
    declared_minimum = declared.get(least_field)
    if declared_total is None or Fraction(str(declared_total)) != verdict.total_mass:
        raise ValueError(f"source record's declared {total_field} does not match the decision")
    if (
        declared_minimum is None
        or verdict.minimum_cell_mass is None
        or Fraction(str(declared_minimum)) != verdict.minimum_cell_mass
    ):
        raise ValueError(f"source record's declared {least_field} does not match the decision")

    point = point_view(certificate)
    gap = point.largest_half_gap_tangent
    coarse_containment = point.square_side * (1 + gap)
    sharp_left_multiplier = point.square_side**2 * (1 + gap) ** 2
    sharp_right = 1 + gap * gap
    source = source_name or certificate_path.as_posix()
    source_block: dict[str, object] = {
        "certificate": source,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "n": certificate.n,
        "outer_side": str(certificate.outer_side),
        "square_side": str(point.square_side),
        "half_gap_tangent": str(gap),
        "coarse_containment": str(coarse_containment),
        total_field: str(verdict.total_mass),
        ("minimum_cell_charge" if threshold else "minimum_cell_mass"): str(
            verdict.minimum_cell_mass
        ),
        "accepted_conditions": [condition.name for condition in verdict.conditions],
    }
    if isinstance(certificate, ThresholdCertificate):
        source_block["variant"] = THRESHOLD_VARIANT
        source_block["point_atoms"] = len(certificate.atoms)
        source_block["threshold_atoms"] = len(certificate.threshold_atoms)
    return {
        "schema": THRESHOLD_LIMIT_RECORD_SCHEMA if threshold else LIMIT_RECORD_SCHEMA,
        "source": source_block,
        "sharpened_containment": {
            "identity": "cos(d) + sin(d) = (1 + t) / sqrt(1 + t^2), where t = tan(d)",
            "gap_domain": f"0 <= t <= D = {gap} < 1",
            "monotonicity_identity": (
                "(1 + D)^2(1 + t^2) - (1 + t)^2(1 + D^2) = 2(D - t)(1 - Dt) >= 0"
            ),
            "strict_factor_test": f"q^2 * {sharp_left_multiplier} < {sharp_right}",
            "strict_factor_test_left_multiplier": str(sharp_left_multiplier),
            "strict_factor_test_right": str(sharp_right),
            "source_gap_below_one": gap < 1,
        },
        "strict_dilation_family": {
            "factor_supremum": result.factor_supremum.exact,
            "factor_supremum_squared": str(result.factor_supremum.squared),
            "factor_supremum_decimal": _decimal(result.factor_supremum),
            "factor_supremum_irrational": result.factor_supremum.irrational,
            "factor_supremum_defining_polynomial": (result.factor_supremum.defining_polynomial),
            "factor_domain": (f"q in Q with q > 0 and q^2 < {result.factor_supremum.squared}"),
            "scaled_containment_test": (
                "q^2 B^2 (1 + D)^2 < 1 + D^2; this rational inequality is "
                "equivalent to strict geometric containment"
            ),
            "invariants": (
                [
                    (
                        "Conditions 1 and 1' D4 symmetry of the point and threshold atoms "
                        "is equivariant under common scaling"
                    ),
                    "Conditions 2' and 3 (total budget and direction net) are unchanged",
                    (
                        "Condition 5' charge is preserved by inverse dilation of "
                        "placements: a core's trace on each threshold atom's scaled "
                        "points is unchanged"
                    ),
                ]
                if threshold
                else [
                    "Condition 1 D4 symmetry is equivariant under common scaling",
                    "Conditions 2 and 3 (total mass and direction net) are unchanged",
                    "Condition 5 covered mass is preserved by inverse dilation of placements",
                ]
            ),
        },
        "conclusion": {
            "bounded_side": result.bounded_side.exact,
            "bounded_side_squared": str(result.bounded_side.squared),
            "bounded_side_defining_polynomial": result.bounded_side.defining_polynomial,
            "decimal": _decimal(result.bounded_side),
            "relation": result.relation,
            "endpoint_certificate": result.endpoint_certificate,
        },
        "proof": {
            "strict_family": (
                "for every rational q > 0 with q^2 below factor_supremum_squared, "
                "the sharpened containment theorem and the scaled source data rule out "
                "a packing at side q * outer_side"
            ),
            "density_step": (
                "for every real x below bounded_side, rational density supplies q with "
                "x / outer_side < q < factor_supremum"
            ),
            "embedding_step": (
                "a packing at side x embeds in the larger side q * outer_side, "
                "contradicting that strict-subfactor no-fit proof"
            ),
            "order_step": (
                "equivalently, s(n) is at least every strict rational subbound and "
                "therefore at least their real supremum"
            ),
            "requires_compactness": result.requires_compactness,
            "endpoint_status": (
                "the sharpened containment inequality is equality at the factor "
                "supremum; the weak limit bound does not assert an endpoint certificate, "
                "no-fit at the endpoint, or a strict lower bound"
            ),
        },
    }


def _record_text(record: dict[str, object]) -> str:
    return json.dumps(record, indent=2, sort_keys=True) + "\n"


def _run_limit_record_mode(
    certificate: Path,
    *,
    source_name: str | None,
    update: Path | None,
    check: Path | None,
) -> int:
    target = update or check
    assert target is not None
    try:
        expected = _record_text(build_limit_record(certificate, source_name=source_name))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 1
    if check is not None:
        if not target.is_file() or target.read_text(encoding="utf-8") != expected:
            print(f"REFUSED: missing or stale limit record {target}", file=sys.stderr)
            return 1
        print(f"limit record agrees with the source certificate: {target}")
        return 0
    with atomic_output_file(target, make_parents=True) as temporary:
        temporary.write_text(expected, encoding="utf-8")
    print(f"wrote limit record {target}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "certificate", type=Path, help="a certificate.json in the retained shape"
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--factor",
        type=Fraction,
        default=None,
        help="the dilation a, an exact rational such as 250001/250000; "
        "without it only the ceiling is reported",
    )
    mode.add_argument(
        "--update-limit-record",
        type=Path,
        help="replay all five source conditions and atomically write the limit proof record",
    )
    mode.add_argument(
        "--check-limit-record",
        type=Path,
        help="replay all five source conditions and refuse a missing or stale proof record",
    )
    parser.add_argument(
        "--source-name",
        default=None,
        help="stable source label stored in a limit record; defaults to the supplied path",
    )
    args = parser.parse_args(argv)

    if args.update_limit_record is not None or args.check_limit_record is not None:
        return _run_limit_record_mode(
            args.certificate,
            source_name=args.source_name,
            update=args.update_limit_record,
            check=args.check_limit_record,
        )

    certificate, record = load_source(read_bounded(args.certificate))
    point = point_view(certificate)
    gap = point.largest_half_gap_tangent
    containment = point.square_side * (1 + gap)
    coarse_ceiling = coarse_condition_four_ceiling(certificate)
    sharp_ceiling = sharp_dilation_ceiling(certificate)
    sharp_side = sharp_ceiling.scaled(certificate.outer_side)
    print(
        f"certificate {record.get('id', '?')}: n = {certificate.n}, "
        f"L = {certificate.outer_side}, B = {point.square_side}"
    )
    print(f"  D = {gap}, B(1 + D) = {containment} = {float(containment):.12f}")
    print(
        f"  coarse Condition 4 ceiling 1 / (B(1 + D)) = {coarse_ceiling} "
        f"= {float(coarse_ceiling):.12f}"
    )
    print(
        f"  sharp factor supremum = {sharp_ceiling.exact} "
        f"(square {sharp_ceiling.squared}, decimal {_decimal(sharp_ceiling)}); "
        f"side supremum {sharp_side.exact} = {_decimal(sharp_side)}; "
        "no endpoint certificate"
    )
    print(
        "  Condition 5 is inherited from the file's retained decision "
        f"(declared least_cell_mass {record.get('least_cell_mass')}), not replayed here"
        if not isinstance(certificate, ThresholdCertificate)
        else "  Condition 5' is inherited from the file's retained decision "
        f"(declared least_cell_charge {record.get('least_cell_charge')}), not replayed here"
    )
    if args.factor is None:
        return 0
    try:
        result = corollary(certificate, args.factor)
    except ValueError as error:
        print(f"REFUSED: {error}")
        return 1
    print(
        f"  q = {result.factor}: q^2 B^2(1 + D)^2 = "
        f"{result.sharp_containment_left_squared} < 1 + D^2 = "
        f"{result.sharp_containment_right}"
    )
    if result.unchanged_condition_failures:
        print(
            "REFUSED: scaling failed an invariant condition: "
            f"{', '.join(result.unchanged_condition_failures)}"
        )
        return 1
    print("  Conditions 1 to 3 and the sharpened containment hypothesis hold")
    print(
        f"COROLLARY: s({certificate.n}) >= {result.bounded_side} "
        f"= {float(result.bounded_side):.9f}, an algebraic consequence of the accepted "
        "certificate and not a further certificate"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
