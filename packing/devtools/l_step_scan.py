"""The bounds the L step and monotonicity carry between the case records' ceilings, exactly.

Two one-line lemmas move an upper bound from one count to another. **The L step** (DS7,
section 2): a packing of ``n'`` unit squares in a square of side ``s`` gives one of
``n' + 2 floor(s) + 1`` in side ``s + 1``, by adding a row of ``floor(s) + 1`` unit squares
along one wall and a column of ``floor(s)`` along the next. **Monotonicity**: deleting a
square gives ``s(n) <= s(n + 1)``. X049's family census measures the first against the
atlas's binary64 sides within a tolerance of 1e-9 (`classify_known_best_families.l_bound`);
this module decides both exactly, from each case record's verified ceiling as the house
selection holds it (`select_houses.load_case`): a fraction, or the isolated root of an
irreducible polynomial, which the L step shifts by one exactly (`plus_one`).

For each count ``n'`` of the case corpus the L step lands at ``n = n' + 2 floor(U') + 1``;
where ``n`` is in the corpus, ``U' + 1`` below ``U(n)`` is a bound the record's ceiling at
``n`` does not hold (``l_step.improves``), and equal to it an L-extension
(``l_step.extensions``). For each ``n`` below the horizon, ``U(n + 1)`` below ``U(n)`` is a
ceiling that monotonicity improves (``monotonicity.improves``). Each such bound says
whether it rounds up at 12 places to its ceiling's print (``same_print``), the print the
restatement ruling reads, since a gain inside the print is the padding class think-ruu2's
RV-3 puts to the owner. A ceiling no reader here holds exactly
(`select_houses.Case.unread`) decides nothing and is listed under ``unread``.
``--with N=SIDE`` stands a candidate's exact rational side in for the ceiling at ``N``
where it is lower, as an import's would stand once adopted, so a lane can see what an
adoption leaves to carry; it refuses a count outside the corpus or one whose ceiling is
unread.

What it decides is narrower than every consequence of the two lemmas. It reads each L
step at its landing count only, and monotonicity between adjacent held counts only. A
composite (an L step, then monotonicity down to a lower count) shows only where it makes
an adjacent inversion: one whose landing lies beyond the horizon, or whose way down
crosses an unread count, is not decided. Adding that check before the scan becomes a
gate is think-lzjw's.

The scan decides nothing about the register: a bound it lists follows from two recorded
ceilings, and whether such a consequence is recorded, and how, is the import runbook's
(``campaign/result-import.md``) and the owner's (think-ruu2's RV-3 and RV-4). It was
written for issue 938 (think-1goz), which reported the L step from T-282 at 172 to 199
with a witness of its own.

From ``packing/``, with the project interpreter::

    python -m devtools.l_step_scan [--with N=FRACTION ...] [--out PATH]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from collections.abc import Mapping, Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import exact_sides
from devtools import select_houses as houses
from devtools.exact_sides import Algebraic, Side

FORMAT = "l-step-scan-v1"
#: The width an algebraic ceiling is narrowed to before its floor is read, halved until
#: both ends of its interval share one; an irrational side is never an integer.
FLOOR_WIDTH = Fraction(1, 2**20)
#: The places an issue prints a side at, rounded up, and the restatement ruling reads.
PRINT = 12


class ScanError(ValueError):
    """An input this module refuses."""


def floor(side: Side) -> int:
    """The greatest integer at or below ``side``, exactly."""
    if not isinstance(side, Algebraic):
        return math.floor(side)
    width = FLOOR_WIDTH
    for _step in range(exact_sides.MAX_BISECTIONS):
        low, high = exact_sides.enclosure(side, width)
        if math.floor(low) == math.floor(high):
            return math.floor(low)
        width /= 2
    raise ScanError(f"{exact_sides.literal(side)}: no integer floor separated")


def _shifted(polynomial: Sequence[int]) -> tuple[int, ...]:
    """The coefficients of ``p(s - 1)``, highest degree first, by Horner's rule."""
    result: list[int] = []
    for coefficient in polynomial:
        # Multiply the running polynomial by the factor s minus one, then add the next.
        product = [*result, 0]
        for index, value in enumerate(result):
            product[index + 1] -= value
        product[-1] += coefficient
        result = product
    return tuple(result)


def plus_one(side: Side) -> Side:
    """``side + 1`` exactly: an algebraic side is the root of ``p(s - 1)`` in the interval
    moved by one, which translation keeps irreducible, primitive and isolated."""
    if not isinstance(side, Algebraic):
        return side + 1
    return Algebraic(_shifted(side.polynomial), side.low + 1, side.high + 1)


def _text(side: Side) -> str:
    return exact_sides.literal(side)


def _gap(high: Side, low: Side) -> str:
    return f"{float(exact_sides.lower_gap(high, low)):.6e}"


def _consequence(n: int, source: int, bound: Side, ceiling: Side) -> dict[str, Any]:
    """One bound a step carries below a ceiling, with whether the 12-place print both
    round up to is the same, the print the restatement ruling reads (think-fwa9)."""
    return {
        "n": n,
        "from": source,
        "bound": _text(bound),
        "ceiling": _text(ceiling),
        "gain": _gap(ceiling, bound),
        "same_print": exact_sides.ceiling(bound, PRINT) == exact_sides.ceiling(ceiling, PRINT),
    }


def ceilings(
    counts: Sequence[int], candidates: Mapping[int, Fraction]
) -> tuple[dict[int, Side], dict[int, str], dict[int, str]]:
    """Each count's ceiling held exactly, the candidate standing in where it is lower; the
    counts whose ceiling no reader holds, with why; and where a candidate stood in."""
    held: dict[int, Side] = {}
    unread: dict[int, str] = {}
    replaced: dict[int, str] = {}
    for n in counts:
        case = houses.load_case(n)
        if not case.exact:
            if n in candidates:
                raise ScanError(f"--with {n}: its ceiling is unread ({case.unread})")
            unread[n] = str(case.unread)
            continue
        held[n] = case.verified
        side = candidates.get(n)
        if side is not None and exact_sides.compare(side, case.verified) < 0:
            held[n] = side
            replaced[n] = _text(case.verified)
    unknown = sorted(set(candidates) - set(counts))
    if unknown:
        raise ScanError(f"--with names counts outside the corpus: {unknown}")
    return held, unread, replaced


def scan(counts: Sequence[int], candidates: Mapping[int, Fraction]) -> dict[str, Any]:
    """The receipt: every L step and monotone step between the held ceilings, decided."""
    held, unread, replaced = ceilings(counts, candidates)
    improves: list[dict[str, Any]] = []
    extensions: list[dict[str, int]] = []
    above = 0
    for parent, side in sorted(held.items()):
        n = parent + 2 * floor(side) + 1
        if n not in held:
            continue
        stepped = plus_one(side)
        order = exact_sides.compare(stepped, held[n])
        if order < 0:
            improves.append(_consequence(n, parent, stepped, held[n]))
        elif order == 0:
            extensions.append({"n": n, "from": parent})
        else:
            above += 1
    monotone: list[dict[str, Any]] = []
    for n, side in sorted(held.items()):
        following = held.get(n + 1)
        if following is not None and exact_sides.compare(following, side) < 0:
            monotone.append(_consequence(n, n + 1, following, side))
    return {
        "format": FORMAT,
        "counts": [min(counts), max(counts)],
        "with": {str(n): _text(side) for n, side in sorted(candidates.items())},
        "replaced": {str(n): ceiling for n, ceiling in sorted(replaced.items())},
        "unread": {str(n): why for n, why in sorted(unread.items())},
        "l_step": {"improves": improves, "extensions": extensions, "above": above},
        "monotonicity": {"improves": monotone},
    }


def _candidate(text: str) -> tuple[int, Fraction]:
    count, _sep, side = text.partition("=")
    try:
        return int(count), Fraction(side.strip())
    except ValueError as error:
        raise ScanError(f"--with {text!r}: give N=FRACTION") from error


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="The bounds the L step and monotonicity carry between case ceilings."
    )
    parser.add_argument(
        "--with",
        dest="candidates",
        action="append",
        default=[],
        metavar="N=FRACTION",
        help="stand a candidate's exact side in for the ceiling at N where it is lower",
    )
    parser.add_argument("--out", type=Path, help="write the receipt here as well")
    args = parser.parse_args(argv)
    started = time.process_time()
    try:
        candidates = dict(_candidate(text) for text in args.candidates)
        receipt = scan(range(1, houses.HORIZON + 1), candidates)
    except (ScanError, houses.SelectionError, exact_sides.ExactSideError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    receipt["cpu_seconds"] = round(time.process_time() - started, 2)
    text = json.dumps(receipt, indent=1, ensure_ascii=False) + "\n"
    if args.out is not None:
        with atomic_output_file(args.out) as temporary:
            Path(temporary).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
