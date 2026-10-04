"""Bašić and Slivková's piercing lower bound on s(n), exactly, for every case.

Bašić and Slivková 2018 (`[Basic-Slivkova 2018]`, Discrete Applied Mathematics 247)
bound the piercing number of the open unit squares inside a square of side `x`
(Theorem 7, by an explicit equilateral-lattice piercing set), and no more than that many
unit squares can be packed in the square (Proposition 8). Writing

    m(x) = ⌊(2/√3)(x + 1 - 2√2)⌋,
    B(x) = ⌊x⌋(m(x) + 2)                         if {x} < 1/2,
    B(x) = ⌊x⌋(m(x) + 2) + ⌊(m(x) + 2)/2⌋        if {x} ≥ 1/2,

at most `B(x)` unit squares fit in side `x`, so `s(n) > x` wherever `B(x) ≤ n - 1`.
`B` is a nondecreasing step function, right-continuous, whose steps fall only where `x`
is an integer, a half-integer, or `(√3/2)j + 2√2 - 1` for an integer `j`. The bound
`s(n) ≥ x*(n)` therefore holds at the first such point with `B(x*) ≥ n`, and that point
is computed here exactly, as an algebraic number, with `sympy`. The paper's own use is
Theorem 10, `s(61) ≥ 7√3/2 + 2√2 - 1 ≈ 7.8906`; this tool asks the same question of
every case and compares the answer with each case record's verified lower bound.

Nothing here depends on Nagamochi 2005: the paper cites it only for the values it
reproduces. The theorem is a published proof read here (2026-10-03), not replayed; this
tool replays only its arithmetic.

From `packing/`, with `uv run --frozen --all-extras --group dev` before each:

    python -m devtools.check_piercing_lower_bounds
    python -m devtools.check_piercing_lower_bounds --update
    python -m devtools.check_piercing_lower_bounds --check
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from decimal import Decimal
from functools import cache
from pathlib import Path
from typing import Any

import sympy

from sqpack import retained_json
from sqpack.known_best import KNOWN_BEST_CORPUS

ROOT = Path(__file__).resolve().parents[1]
FRONTIER = ROOT / "frontier"
RESULT = (
    ROOT
    / "campaign"
    / "series"
    / "series-000-smoke-and-calibration"
    / "results"
    / "piercing-lower-bounds.json"
)

SQRT2 = sympy.sqrt(2)
SQRT3 = sympy.sqrt(3)
#: Digits each bound is printed with, rounded down so a printed bound is still a bound.
DIGITS = 12


#: Digits a floor is decided at. A value nearer an integer than this is decided exactly.
PRECISION = 80


def exact_floor(value: sympy.Expr) -> int:
    """`⌊value⌋` for an algebraic `value`, decided at `PRECISION` digits and exactly where
    the value is within `10^-60` of an integer: `sympy.floor` of an unevaluated sum of
    surds can round a value a billionth below an integer up to it."""
    approx = sympy.N(value, PRECISION)
    nearest = int(sympy.Integer(round(approx)))
    if abs(approx - nearest) < sympy.Rational(1, 10**60):
        difference = sympy.nsimplify(sympy.simplify(value - nearest))
        if difference == 0:
            return nearest
        return nearest if difference > 0 else nearest - 1
    return int(sympy.floor(approx))


def m_of(x: sympy.Expr) -> int:
    """`⌊(2/√3)(x + 1 - 2√2)⌋`, the rows of the paper's lattice less two."""
    return exact_floor(2 / SQRT3 * (x + 1 - 2 * SQRT2))


def pierce_bound(x: sympy.Expr) -> int:
    """Theorem 7's bound on the piercing number of the unit squares in side `x`."""
    whole = exact_floor(x)
    rows = m_of(x) + 2
    base = whole * rows
    if x - whole < sympy.Rational(1, 2):
        return base
    return base + rows // 2


@cache
def steps(limit: int) -> tuple[sympy.Expr, ...]:
    """Every point in `[2√2 - 1, limit]` where `B` can step, in increasing order.

    Below `2√2 - 1` the lattice has no row to stand on (`m < 0`), and the paper does not
    use the bound there.
    """
    start = 2 * SQRT2 - 1
    points: set[sympy.Expr] = set()
    for k in range(1, limit + 1):
        points.add(sympy.Integer(k))
        points.add(sympy.Rational(2 * k + 1, 2))
    j = 0
    while True:
        point = SQRT3 / 2 * j + start
        if point > limit:
            break
        points.add(sympy.nsimplify(point))
        j += 1
    inside = [point for point in points if start <= point <= limit]
    return tuple(sorted(inside, key=lambda point: sympy.N(point, 50)))


@cache
def step_values(limit: int) -> tuple[tuple[sympy.Expr, int], ...]:
    """Each step and `B` at it, evaluated once: `B` is nondecreasing, so every case reads
    its bound from this one table rather than walking the steps again."""
    return tuple((point, pierce_bound(point)) for point in steps(limit))


def piercing_bound(n: int, limit: int = 40) -> sympy.Expr:
    """The largest `x` the paper proves `s(n) ≥ x` for: the first step with `B ≥ n`."""
    for point, value in step_values(limit):
        if value >= n:
            return point
    raise ValueError(f"n = {n}: no step of B up to {limit} reaches {n}")


def floor_decimal(value: sympy.Expr, digits: int = DIGITS) -> str:
    """`value` rounded down to `digits` significant digits, as the case records print."""
    magnitude = exact_floor(sympy.log(sympy.N(value, PRECISION), 10))
    scale = digits - 1 - magnitude
    floored = exact_floor(value * sympy.Integer(10) ** scale)
    return format(Decimal(floored).scaleb(-scale).normalize(), "f")


def verified_floor(n: int) -> float:
    """The case record's verified lower bound, as a float for comparison only."""
    text = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    front = text.split("---", 2)[1]
    block = front.split("verified_lower_bound:", 1)[1]
    value = block.split("value:", 1)[1].splitlines()[0].strip().strip("'\"")
    return float(sympy.N(sympy.sympify(value.replace("√", "sqrt")), 30))


def survey(numbers: Sequence[int]) -> dict[str, Any]:
    """Each case's piercing bound, and the cases where it beats the verified floor."""
    rows: list[dict[str, Any]] = []
    for n in numbers:
        bound = piercing_bound(n)
        floor = verified_floor(n)
        decimal = floor_decimal(bound)
        rows.append(
            {
                "n": n,
                "bound": str(bound),
                "decimal": decimal,
                "verified_lower": floor,
                # The record holds a value rounded down at DIGITS, so the bound holds the
                # floor where the floor is its printed decimal, and beats it where it is
                # strictly above.
                "holds": float(decimal) == floor,
                "improves": float(decimal) > floor,
            }
        )
    return {
        "source_key": "[Basic-Slivkova 2018]",
        "theorem": "Theorem 7 with Proposition 8",
        "cases": rows,
        "holds": [row["n"] for row in rows if row["holds"]],
        "improves": [row["n"] for row in rows if row["improves"]],
    }


def _text(record: dict[str, Any]) -> str:
    return retained_json.dumps(record, ensure_ascii=False)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--update", action="store_true", help="rewrite the retained record")
    mode.add_argument("--check", action="store_true", help="compare with the retained record")
    arguments = parser.parse_args(argv)
    record = survey(range(2, KNOWN_BEST_CORPUS.count + 1))
    text = _text(record)
    if arguments.update:
        RESULT.write_text(text, encoding="utf-8")
        print(f"wrote {RESULT.relative_to(ROOT.parent)}")
    elif arguments.check:
        if not RESULT.is_file() or RESULT.read_text(encoding="utf-8") != text:
            print(f"{RESULT.name} is stale; run with --update", file=sys.stderr)
            return 1
    print(
        f"piercing lower bounds checked for {len(record['cases'])} cases; holds the "
        f"verified floor at n = {record['holds']} and beats it at n = {record['improves']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
