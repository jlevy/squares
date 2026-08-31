#!/usr/bin/env python3
"""Replay the `n = 82` construction with exact algebraic predicates.

Four checks, and the last two are what make the first worth having.

**The construction is feasible, exactly.** All 3321 pairs and every wall decided by an
exact sign over `Q(sqrt 2)`, no tolerance anywhere, at side `6 + (5/2)sqrt(2)`.

**A duplicated square is rejected**, and so is **a tenth column square**: the L's count is
a derived fact (nine fit against the right wall, a tenth does not), so the control that
would catch an over-full L is kept firing rather than assumed.

**The retained witness's side is this side.** The witness declares
`9.53553390593273762200422181052425`, which is the exact value correctly rounded up at
thirty-two fractional digits, so the exact construction fits inside the witness's own
declared side -- the comfortable direction of `D-398`'s rounding asymmetry, the same as
`n = 65` and unlike `n = 89`.

What is deliberately NOT checked is coordinate identification: the witness's centre set
matches none of this construction's eight dihedral images (every gap exceeds `6.8`), so the
retained drawing is a different layout at the same side. The evidence this replay supports
is about the construction, not the witness's geometry.

Nothing is promoted here. Feasible at the published side is not optimal.

Usage:
    uv run --frozen python -m cases.gobel82.verify_exact
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from pathlib import Path

from cases.gobel40.packing import corners
from cases.gobel82.packing import COLUMN, build, count
from sqpack.verify import exact_sign, verify_packing
from sqpack.witness import load_witness

ROOT = Path(__file__).resolve().parent.parent.parent
WITNESS = ROOT / "witnesses" / "known-best" / "n-082.yaml"
WITNESS_SCHEMA = ROOT / "witnesses" / "witness.schema.yaml"

CERTIFIES = (82,)
"""The size this replay decides. See `CERTIFIES` in `cases/gobel5`."""

WITNESS_ROUNDING = Decimal("1e-32")
"""The witness's own rounding at the thirty-two fractional digits it declares."""


def _decimal(element) -> Decimal:
    rational, root = element.coeffs
    return (
        Decimal(rational.numerator) / Decimal(rational.denominator)
        + (Decimal(root.numerator) / Decimal(root.denominator)) * Decimal(2).sqrt()
    )


def main() -> int:
    squares, side, field = build()
    n = count()
    report = verify_packing(squares, side, sign=exact_sign)
    print(report)
    if not report.valid or report.n != n:
        return 1
    if report.pairs_tested != n * (n - 1) // 2:
        print(f"n={n}: {report.pairs_tested} pairs tested, expected all of them")
        return 1

    duplicate = verify_packing([*squares, squares[0]], side, sign=exact_sign)
    if duplicate.valid:
        print(f"n={n}: negative control failed, duplicated square was accepted")
        return 1
    print(f"n={n}: negative control rejected a duplicated square")

    q = field.rational
    half = q(1) / q(2)
    tenth = corners((side - half, q(2 * COLUMN + 1) / q(2)), (half, q(0)), (q(0), half))
    overfull = verify_packing([*squares, tenth], side, sign=exact_sign)
    if overfull.valid:
        print(f"n={n}: negative control failed, a tenth column square was accepted")
        return 1
    print(f"n={n}: negative control rejected a tenth column square")

    with localcontext() as context:
        context.prec = 60
        witness = load_witness(WITNESS, fallback_schema=WITNESS_SCHEMA)
        declared = Decimal(str(witness["side"]))
        gap = declared - _decimal(side)
        if not (0 < gap <= WITNESS_ROUNDING):
            print(f"n={n}: witness side differs from the exact side by {gap}")
            return 1
        print(f"n={n}: witness side is the exact side, rounded up by {gap}")

    print("field preconditions: x^2-2 irreducible; (1,2) isolates its positive root")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
