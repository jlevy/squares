#!/usr/bin/env python3
"""What a certificate's Condition 4 margin proves: the dilation corollary.

Dilate every atom position, the container side ``L`` and the shrunken side ``B`` by one
factor ``a > 0``, and leave the weights and the direction net alone. The inverse dilation
is a bijection between the placements of the two certificates that carries covered mass
to covered mass, so Condition 5 is unchanged, and so are Conditions 1 to 3, which never
look at a length. Only Condition 4 moves: ``B (1 + D)`` becomes ``a B (1 + D)``. So an
accepted certificate for ``s(n) >= L`` proves ``s(n) >= a L`` for every ``a`` below
``1 / (B (1 + D))`` -- an algebraic corollary of the retained data, not a further
certificate, and one that never licenses dividing ``L`` by ``B``: the ceiling is
``1 / (B (1 + D))``, a supremum that Condition 4's strictness keeps out of reach.

Section 4 of the 2026-09-05 adversarial review read this off the retained
``s(11) >= 381/100`` certificate at ``a = 250001/250000``, giving
``s(11) >= 95250381/25000000 = 3.81001524``. This tool recomputes it from the file::

    uv run --frozen python -m devtools.dilation_corollary \\
        cases/n11_fractional_certificate/certificate.json --factor 250001/250000

It decides Conditions 1 to 4 of the dilated certificate and nothing more. Condition 5
is inherited from the input file's own retained decision, which this tool does not
repeat; the corollary is only as good as that decision, and the output says so. The
margin it measures is better spent before a search than after one: setting ``B``
nearer its Condition 4 ceiling makes the side the search runs at the side the
certificate proves.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path

from devtools.declare_least_cell_mass import load_candidate
from sqpack.fractional.certificate import Certificate, closed_form_conditions


def dilation_ceiling(certificate: Certificate) -> Fraction:
    """``1 / (B (1 + D))``: the supremum of the factors Condition 4 admits, not attained."""

    return 1 / (certificate.square_side * (1 + certificate.largest_half_gap_tangent))


def dilate(certificate: Certificate, factor: Fraction) -> Certificate:
    """Positions, ``L`` and ``B`` scaled by ``factor``; weights, net and symmetry kept.

    Refuses a factor at or above the ceiling, because the result would fail Condition 4
    and be a corollary of nothing, and a factor that is not positive.
    """

    if factor <= 0:
        raise ValueError(f"a dilation factor must be positive, not {factor}")
    ceiling = dilation_ceiling(certificate)
    if factor >= ceiling:
        raise ValueError(
            f"factor {factor} is not below the ceiling {ceiling} = 1 / (B (1 + D)); "
            "the dilated certificate would fail Condition 4"
        )
    return replace(
        certificate,
        outer_side=certificate.outer_side * factor,
        square_side=certificate.square_side * factor,
        atoms=tuple(
            replace(atom, x=atom.x * factor, y=atom.y * factor) for atom in certificate.atoms
        ),
    )


@dataclass(frozen=True, slots=True)
class Corollary:
    """The numbers the corollary turns on, all exact."""

    factor: Fraction
    half_gap_tangent: Fraction
    containment: Fraction
    dilated_containment: Fraction
    ceiling: Fraction
    ceiling_side: Fraction
    bounded_side: Fraction
    closed_form_failures: tuple[str, ...]


def corollary(certificate: Certificate, factor: Fraction) -> Corollary:
    """The dilated certificate's Condition 4 and the bound it carries, from the data.

    ``dilated_containment`` is computed on the dilated certificate itself, so it is
    literally its Condition 4 and not ``factor`` times the original's.
    """

    dilated = dilate(certificate, factor)
    gap = certificate.largest_half_gap_tangent
    ceiling = dilation_ceiling(certificate)
    return Corollary(
        factor=factor,
        half_gap_tangent=gap,
        containment=certificate.square_side * (1 + gap),
        dilated_containment=dilated.square_side * (1 + dilated.largest_half_gap_tangent),
        ceiling=ceiling,
        ceiling_side=certificate.outer_side * ceiling,
        bounded_side=dilated.bounded_side,
        closed_form_failures=tuple(
            condition.name
            for condition in closed_form_conditions(dilated)
            if not condition.holds
        ),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "certificate", type=Path, help="a certificate.json in the retained shape"
    )
    parser.add_argument(
        "--factor",
        type=Fraction,
        default=None,
        help="the dilation a, an exact rational such as 250001/250000; "
        "without it only the ceiling is reported",
    )
    args = parser.parse_args(argv)
    certificate, record = load_candidate(args.certificate)
    gap = certificate.largest_half_gap_tangent
    containment = certificate.square_side * (1 + gap)
    ceiling = dilation_ceiling(certificate)
    print(
        f"certificate {record.get('id', '?')}: n = {certificate.n}, "
        f"L = {certificate.outer_side}, B = {certificate.square_side}"
    )
    print(f"  D = {gap}, B(1 + D) = {containment} = {float(containment):.12f}")
    print(
        f"  ceiling 1 / (B(1 + D)) = {ceiling} = {float(ceiling):.12f}, a supremum; "
        f"L at the ceiling {certificate.outer_side * ceiling} "
        f"= {float(certificate.outer_side * ceiling):.9f}, not attained"
    )
    print(
        "  Condition 5 is inherited from the file's retained decision "
        f"(declared least_cell_mass {record.get('least_cell_mass')}), not replayed here"
    )
    if args.factor is None:
        return 0
    try:
        result = corollary(certificate, args.factor)
    except ValueError as error:
        print(f"REFUSED: {error}")
        return 1
    print(
        f"  a = {result.factor}: a B(1 + D) = {result.dilated_containment} "
        f"= {float(result.dilated_containment):.18f} < 1"
    )
    if result.closed_form_failures:
        print(
            f"REFUSED: the dilated certificate fails {', '.join(result.closed_form_failures)}"
        )
        return 1
    print("  Conditions 1 to 4 of the dilated certificate hold")
    print(
        f"COROLLARY: s({certificate.n}) >= {result.bounded_side} "
        f"= {float(result.bounded_side):.9f}, an algebraic consequence of the accepted "
        "certificate and not a further certificate"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
