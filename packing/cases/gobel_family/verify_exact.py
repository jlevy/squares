#!/usr/bin/env python3
"""Replay Goebel's family at `n = 65` and `n = 89` with exact algebraic predicates.

These are the two sizes where the family's side is exactly the best known this repository
retains and no exact construction was held -- `n = 5` and `n = 40` are the other two and
have their own case packages. Both verify here in seconds: 2080 and 3916 pairs, every one
decided by an exact sign over `Q(sqrt 2)`.

Three things are checked and the second and third are what make the first worth having.

**The constructions are feasible, exactly.** No tolerance anywhere, and the corner
coordinates that sit on the container boundary sit on it exactly.

**A duplicated square is rejected.** The negative control, without which "valid" only means
the checker returned.

**They agree with the retained witnesses to `5e-33`** -- which identifies those witnesses
rather than merely permitting them. Nothing independently optimised lands within `1e-32` of
a construction it was not built from, so `n = 65` and `n = 89`'s decimal records **are**
materialisations of this family, exactly as `n = 40`'s turned out to be. That is the third
check and the one that says what these records have been all along.

Nothing is promoted. Feasible at the retained side is not optimal, and moving either
witness to `exact-algebraic` is an assurance-contract question this does not open.

Usage:
    uv run --frozen python -m cases.gobel_family.verify_exact
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from pathlib import Path

from cases.gobel_family.packing import build, count
from sqpack.verify import Report, exact_sign, verify_packing
from sqpack.witness import load_witness

ROOT = Path(__file__).resolve().parent.parent.parent
WITNESSES = ROOT / "witnesses" / "known-best"
WITNESS_SCHEMA = ROOT / "witnesses" / "witness.schema.yaml"

SUBJECTS = ((4, 5), (4, 7))
"""`(a, b)` for `n = 65` and `n = 89`: the family's sizes that had no construction here."""

CERTIFIES = (65, 89)
"""The sizes `SUBJECTS` decides. See `CERTIFIES` in `cases/gobel5`."""

WITNESS_ROUNDING = Decimal("1e-32")
"""The witnesses' own rounding, rounded up -- and the measurement that identifies them.

This started at `1e-11`, on the reasoning that both records are `numerical-multiprecision`
and might be independently optimised numerics that merely land on the same side. They are
not. They agree with this construction to `4.81e-33` and `3.28e-33`, which is far below any
precision an independent optimisation would reach and is instead these witnesses' own
rounding at the digits they carry.

So the comparison identifies rather than merely permits: `n = 65` and `n = 89`'s retained
witnesses **are** materialisations of Goebel's family, exactly as `n = 40`'s turned out to
be. The bound sits just above the measured figures rather than at a round number, because a
tolerance with slack in it would stop being a statement about the witnesses.

**The two sizes differ in sign, and only one direction is comfortable.** Each witness is
the exact side correctly rounded to thirty-two fractional digits, and which way that goes
depends on the omitted tail. At `n = 65` it rounds up, so the witness sits `4.80e-33`
*above* `5 + (5/2)sqrt(2)` and the exact construction fits inside it. At `n = 89` it rounds
down, so the witness sits `3.27e-33` *below* `5 + (7/2)sqrt(2)` -- and the exact
construction does **not** fit inside the witness's own declared side.

Nothing here is wrong as a result: both witnesses are `numerical-multiprecision` records
checked at `tolerance: 1e-8`, and `3e-33` is far inside that. But it means `n = 89` cannot
be promoted to an exact record by relabelling. An exact claim at the witness's declared
side would be false, so a promotion has to carry coordinates and a side computed from the
construction rather than inherited from the witness. See `D-398`.

What this does not show is optimality. Being at the best known side is a fact about the
retained record.
"""


def _decimal(element) -> Decimal:
    rational, root = element.coeffs
    return (
        Decimal(rational.numerator) / Decimal(rational.denominator)
        + (Decimal(root.numerator) / Decimal(root.denominator)) * Decimal(2).sqrt()
    )


def verify(a: int, b: int) -> Report:
    """The exact separating-axis report for the construction at `(a, b)`."""
    squares, side, _field = build(a, b)
    return verify_packing(squares, side, sign=exact_sign)


def witness_disagreement(a: int, b: int) -> Decimal | None:
    """Largest centre-coordinate gap against the retained witness, or `None` if absent."""
    getcontext().prec = 60
    path = WITNESSES / f"n-{count(a, b):03d}.yaml"
    if not path.is_file():
        return None
    squares, _side, _field = build(a, b)
    mine = sorted(
        (
            _decimal(sum((corner[0] for corner in square[1:]), square[0][0])) / 4,
            _decimal(sum((corner[1] for corner in square[1:]), square[0][1])) / 4,
        )
        for square in squares
    )
    witness = load_witness(path, fallback_schema=WITNESS_SCHEMA)
    theirs = sorted(
        (Decimal(str(square["center"][0])), Decimal(str(square["center"][1])))
        for square in witness["squares"]
    )
    return max(
        max(abs(a[0] - b[0]), abs(a[1] - b[1])) for a, b in zip(mine, theirs, strict=True)
    )


def main() -> int:
    for a, b in SUBJECTS:
        n = count(a, b)
        report = verify(a, b)
        print(report)
        if not report.valid or report.n != n:
            return 1
        if report.pairs_tested != n * (n - 1) // 2:
            print(f"n={n}: {report.pairs_tested} pairs tested, expected all of them")
            return 1

        squares, side, _field = build(a, b)
        duplicate = verify_packing([*squares, squares[0]], side, sign=exact_sign)
        if duplicate.valid:
            print(f"n={n}: negative control failed, duplicated square was accepted")
            return 1

        gap = witness_disagreement(a, b)
        if gap is None:
            print(f"n={n}: no retained witness to compare against")
        elif gap > WITNESS_ROUNDING:
            print(f"n={n}: disagrees with the retained witness by {gap}")
            return 1
        else:
            print(f"n={n}: agrees with the retained witness to {gap}")
        print(f"n={n}: negative control rejected a duplicated square")
    print("field preconditions: x^2-2 irreducible; (1,2) isolates its positive root")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
