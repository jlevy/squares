#!/usr/bin/env python3
"""Replay Göbel's forty-square construction with exact algebraic predicates.

Two things are checked and the second is what makes the first worth having.

**The construction is feasible, exactly.** Every one of the 780 pairs is decided by an
exact sign over `Q(sqrt 2)`, not by a tolerance, and 48 corner coordinates sit exactly on
the container boundary.

**It is the packing the corpus already holds.** The retained `n = 40` witness is a decimal
record, and the exact pose reproduces it to `6.04e-31` -- which is not a coincidence and
not an error term of this construction. It is the witness's own rounding: its side is
`4 + 2 sqrt(2)` correctly rounded to twenty-nine fractional digits, which puts it that far
*above* the exact value, and the coordinates computed from the side inherit it. Agreement
to the limit of the witness's precision, with the residual explained rather than tolerated,
is the check worth running; agreement to some declared epsilon would not have been.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from pathlib import Path

from cases.gobel40.packing import build
from sqpack.verify import Report, exact_sign, verify_packing
from sqpack.witness import load_witness

CERTIFIES = (40,)
"""The sizes this module decides by exact predicate. See `CERTIFIES` in `cases/gobel5`."""

ROOT = Path(__file__).resolve().parent.parent.parent
WITNESS = ROOT / "witnesses" / "known-best" / "n-040.yaml"
WITNESS_SCHEMA = ROOT / "witnesses" / "witness.schema.yaml"

WITNESS_ROUNDING = Decimal("7e-31")
"""The witness's own rounding, rounded up.

Its side is `4 + 2 sqrt(2)` correctly rounded to twenty-nine fractional digits, which puts
it `6.0384e-31` *above* the exact value -- the omitted tail is `...41939615...`, so the
last kept digit rounds up. Nothing in the construction may disagree by more than that, and
the ceiling is deliberately just above the measured figure rather than a round number: a
tolerance with slack in it would stop being a statement about the witness.

The direction is worth stating rather than leaving to the magnitude, because it is not the
same at every size and the other case is the interesting one. A witness rounded *down*
sits below the exact side, and the exact construction then does not fit inside the
witness's own declared side. That happens at `n = 89`; see `cases/gobel_family`. Here it
does not.
"""


def verify() -> Report:
    """Return the exact separating-axis report for the construction."""
    squares, side, _field = build()
    return verify_packing(squares, side, sign=exact_sign)


def _decimal(element) -> Decimal:
    rational, root = element.coeffs
    return (
        Decimal(rational.numerator) / Decimal(rational.denominator)
        + (Decimal(root.numerator) / Decimal(root.denominator)) * Decimal(2).sqrt()
    )


def witness_disagreement() -> Decimal:
    """The largest centre-coordinate gap between the construction and the witness."""
    with localcontext() as context:
        context.prec = 120
        squares, _side, _field = build()
        mine = sorted(
            (
                _decimal(sum((corner[0] for corner in square[1:]), square[0][0])) / 4,
                _decimal(sum((corner[1] for corner in square[1:]), square[0][1])) / 4,
            )
            for square in squares
        )
        witness = load_witness(WITNESS, fallback_schema=WITNESS_SCHEMA)
        theirs = sorted(
            (Decimal(str(square["center"][0])), Decimal(str(square["center"][1])))
            for square in witness["squares"]
        )
        return max(
            max(abs(a[0] - b[0]), abs(a[1] - b[1])) for a, b in zip(mine, theirs, strict=True)
        )


def main() -> int:
    report = verify()
    print(report)
    if not report.valid or report.n != 40 or report.pairs_tested != 780:
        return 1

    squares, side, _field = build()
    duplicate = verify_packing([*squares, squares[0]], side, sign=exact_sign)
    if duplicate.valid:
        print("negative control failed: duplicated square was accepted")
        return 1

    gap = witness_disagreement()
    if gap > WITNESS_ROUNDING:
        print(f"construction disagrees with the retained witness by {gap}")
        return 1

    print("field preconditions: x^2-2 irreducible; (1,2) isolates its positive root")
    print("negative control: duplicated square rejected")
    print(f"agrees with the retained witness to {gap} -- the witness's own rounding")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
