#!/usr/bin/env python3
"""Replay Friedman's off-centre family at `n = 26` and `n = 85` exactly.

Two sizes, one sentence of `[Friedman DS7]` section 3, every pair and wall decided by an
exact sign over `Q(sqrt 2)` at sides `(7 + 3 sqrt(2))/2` and `11/2 + 3 sqrt(2)`.

Three controls per size: a duplicated square is rejected; **one more column square is
rejected** -- the column holds exactly `2a + 1` because the `2a + 2`-nd would stand above
the container, and that refusal is the exercisable half of the count; and the retained
witness's declared side is identified as the exact side at the witness's own rounding.

Nothing is promoted here, and nothing about optimality is claimed.

Usage:
    uv run --frozen python -m cases.gobel_offcentre.verify_exact
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from pathlib import Path

from cases.gobel_offcentre.packing import build, column_height, count, extra_column_square
from sqpack.verify import exact_sign, verify_packing
from sqpack.witness import load_witness

ROOT = Path(__file__).resolve().parent.parent.parent
WITNESSES = ROOT / "witnesses" / "known-best"
WITNESS_SCHEMA = ROOT / "witnesses" / "witness.schema.yaml"

SUBJECTS = ((2, 3), (4, 6))
"""`(a, b)` for `n = 26` and `n = 85`: the two sizes DS7 names for this rule."""

CERTIFIES = (26, 85)
"""The sizes `SUBJECTS` decides. See `CERTIFIES` in `cases/gobel5`."""

WITNESS_ROUNDING = Decimal("1e-29")
"""The witnesses' own rounding at the digits they declare, in either direction."""


def _decimal(element) -> Decimal:
    rational, root = element.coeffs
    return (
        Decimal(rational.numerator) / Decimal(rational.denominator)
        + (Decimal(root.numerator) / Decimal(root.denominator)) * Decimal(2).sqrt()
    )


def main() -> int:
    for a, b in SUBJECTS:
        n = count(a, b)
        squares, side, field = build(a, b)
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

        overfull = verify_packing(
            [*squares, extra_column_square(a, side, field)], side, sign=exact_sign
        )
        if overfull.valid:
            print(
                f"n={n}: negative control failed, "
                f"column square {column_height(a) + 1} was accepted"
            )
            return 1
        print(
            f"n={n}: negative controls rejected a duplicate "
            f"and column square {column_height(a) + 1}"
        )

        with localcontext() as context:
            context.prec = 60
            witness = load_witness(
                WITNESSES / f"n-{n:03d}.yaml", fallback_schema=WITNESS_SCHEMA
            )
            gap = Decimal(str(witness["side"])) - _decimal(side)
            if abs(gap) > WITNESS_ROUNDING or gap == 0:
                print(f"n={n}: witness side differs from the exact side by {gap}")
                return 1
            print(f"n={n}: witness side is the exact side, rounded off by {gap}")
    print("field preconditions: x^2-2 irreducible; (1,2) isolates its positive root")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
