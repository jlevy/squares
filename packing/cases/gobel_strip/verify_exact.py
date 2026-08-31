#!/usr/bin/env python3
"""Replay Goebel's diagonal-strip family at `a = 4..8` with exact algebraic predicates.

Five sizes, one rule: `n = 27, 38, 52, 67, 84` are the open cases where the strip is
exactly the best known this repository retains, and every one verifies here with no
tolerance anywhere -- all pairs and all four walls decided by an exact sign over
`Q(sqrt 2)` at side `a + 1 + sqrt(2)/2`.

Three controls per size, because the interesting number is the diamond count:

**A duplicated square is rejected** -- the standard floor.

**One more diamond is rejected.** Goebel's count `floor((a-1) sqrt(2)) + 1` is a theorem
about the row, not a transcription, and the refusal of the next diamond is the half of it
a feasibility check can exercise.

**The retained witness's side is this side.** Each witness declares the exact value
correctly rounded at its own digits; the comparison identifies the declared side without
claiming the layout, since the strip has translation slack and the witnesses take other
slack choices than this construction's symmetric one.

Nothing is promoted here, and nothing about optimality is claimed anywhere: `a = 3` is
`n = 17`, where the same rule is beaten by Bidwell's packing.

Usage:
    uv run --frozen python -m cases.gobel_strip.verify_exact
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from pathlib import Path

from cases.gobel_strip.packing import build, count, diamonds, extra_diamond
from sqpack.verify import exact_sign, verify_packing
from sqpack.witness import load_witness

ROOT = Path(__file__).resolve().parent.parent.parent
WITNESSES = ROOT / "witnesses" / "known-best"
WITNESS_SCHEMA = ROOT / "witnesses" / "witness.schema.yaml"

SUBJECTS = (4, 5, 6, 7, 8)
"""`a` for `n = 27, 38, 52, 67, 84`: the sizes where the strip is the retained record."""

CERTIFIES = (27, 38, 52, 67, 84)
"""The sizes `SUBJECTS` decides. See `CERTIFIES` in `cases/gobel5`."""

WITNESS_ROUNDING = Decimal("1e-29")
"""The witnesses' own rounding at the digits they declare -- and its direction.

All five witnesses share the same fractional part, `sqrt(2)/2`, and all five truncate it
the same way, sitting `4.849e-30` *below* the exact side. That is `D-398`'s uncomfortable
direction: the exact construction does not fit inside any witness's own declared side, so
these certificates carry the construction's coordinates and side, never a relabelling of
a witness -- exactly the situation `cases/gobel_family` records at `n = 89`.
"""


def _decimal(element) -> Decimal:
    rational, root = element.coeffs
    return (
        Decimal(rational.numerator) / Decimal(rational.denominator)
        + (Decimal(root.numerator) / Decimal(root.denominator)) * Decimal(2).sqrt()
    )


def main() -> int:
    for a in SUBJECTS:
        n = count(a)
        squares, side, field = build(a)
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
            [*squares, extra_diamond(a, side, field)], side, sign=exact_sign
        )
        if overfull.valid:
            print(f"n={n}: negative control failed, diamond {diamonds(a) + 1} was accepted")
            return 1
        print(f"n={n}: negative controls rejected a duplicate and diamond {diamonds(a) + 1}")

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
