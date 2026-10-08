#!/usr/bin/env python3
r"""Read the exact content a Kingbird catalogue SVG carries, and check its polynomial.

A catalogue picture opens with a comment. Its first paragraph is the attribution, which
`devtools.derive_kingbird_facts` already reads; below it, where there is one, is the
derivation: a Mathematica model of the packing, the system of contact equations it
solves, and for some counts the side as a `Root[poly &, k]` object. The DOCTYPE above the
drawing then declares the side, the angles and the offsets as entities, to 30 to 100
digits. For `n = 83` that comment is the only place the catalogue prints the side's
degree-672 minimal polynomial (review of 2026-10-05, think-krbs), and for `n = 55` and
`71` it is where the credited "exact analytic solution" would be (think-xy91).

This tool reads that content and checks it. It never writes the SVG: the bytes are read
from a local file or fetched into memory, as `derive_kingbird_facts` fetches them, and
only the facts are kept, under the retention policy in
`resources/web/known-best-packings/README.md`. A polynomial and a system of equations
are mathematical facts; the picture is not retained.

**What it reads.**

- The attribution paragraph, the entities with the formulas their own comments give,
  the comment's Mathematica statements, and every solver call in them (`FindRoot`,
  `Solve`, `NSolve`, `Reduce`, `Eliminate`, `RootReduce` and the minimizers) with its
  equations, unknowns and `WorkingPrecision`.
- Every `Root[...]` object, with the name it is assigned to. A body that is a sum of
  integer multiples of powers of `#` (or `#1`) is read into integer coefficients and
  printed in the catalogue's notation by `sqpack.exact_values.format_polynomial`; any
  other body is recorded with the reason it was not read.

**What it checks, for each integer `Root` assigned to the side `s`.**

- *Degree and form.* The coefficients are made primitive with a positive leading term.
- *Irreducibility over the rationals*, by a modular degree-pattern certificate. For a
  prime `p` that divides neither the leading coefficient nor the discriminant, the
  degrees of the irreducible factors of `f mod p` (a distinct-degree factorization over
  `GF(p)`) bound the degree of any factor over the integers: it must be a sum of a
  sub-multiset of them. The sets allowed by successive primes are intersected; when no
  degree between 1 and `deg f - 1` survives, `f` is irreducible, and the primes and their
  patterns are the certificate. A reducible `f` never yields one. The arithmetic is numpy
  `int64` with primes below `2^20`, so no sum can overflow.
- *A real root at the recorded side*, isolated in exact integer arithmetic. Newton's
  method in mpmath, from the reference decimal, gives a centre `c` with enough digits;
  then, with `M2` an upper bound for `|f''|` near `c` and a radius `r = 10^-m` chosen so
  that `2 r M2 <= |f'(c)|`, `f'` keeps one sign on `[c - r, c + r]`, so `f` is monotone
  there, and opposite signs of `f` at the two ends, computed exactly, leave exactly one
  root inside. Each reference decimal is then compared with that root, and the bound on
  the difference includes the radius.
- *The `Root` index*, where SymPy can count the real roots below the interval quickly
  enough (`--index-max-degree`). Mathematica numbers the real roots of a `Root` object
  first, in increasing order, so index `k` means `k - 1` real roots lie below.

The default references are the side the SVG's own `s` entity declares, the frontier
record's printed side (which the catalogue truncates), and Evan Daniel's KKT value of
the record's packing (`S_exact` in `batch/results.json` of the 5 October packet).

**Writing the record.** With `--write-record`, a verified polynomial for the side goes
into the frontier record's `minimal_polynomial`, only where the record's degree is the
verified degree, its `algebraic_source` is `catalogue` and its polynomial is null. The
three fields are then rewritten as `devtools.backfill_algebraic_facts` writes them, so
that tool's `--check` stays clean.

**The `record` command** runs the same checks on a polynomial a frontier record already
holds, which the source-coverage gate compares with the catalogue's text but does not
check as mathematics.

Usage, from `packing/`, each after `uv run --frozen --all-extras --group dev`::

    python -m devtools.extract_kingbird_svg_exact svg 83 --out FACTS.json
    python -m devtools.extract_kingbird_svg_exact svg 83 --svg PATH --write-record
    python -m devtools.extract_kingbird_svg_exact record 69

The first fetches `square-83.svg` into memory and compares its SHA-256 with the reading
of 2026-10-05 (`resources/web/known-best-packings/receipts/`); the second reads a local
copy, which a session without access to the catalogue host can be handed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from collections.abc import Sequence
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from decimal import ROUND_CEILING, Decimal, InvalidOperation, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp
import numpy as np
import numpy.typing as npt
from strif import atomic_output_file

from devtools.backfill_algebraic_facts import backfilled
from devtools.derive_kingbird_facts import (
    DerivationRefusedError,
    fetch_picture,
    picture_credits,
)
from devtools.retained_data import read_retained_bytes
from sqpack.exact_values import format_polynomial, primitive
from sqpack.kingbird_catalogue import normalized_polynomial
from sqpack.known_best import KINGBIRD_BASE_URL
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
#: The reading of all 98 retained Kingbird pictures on 2026-10-05: each one's size,
#: SHA-256 and `Last-Modified`, against which a new fetch is compared.
READING_RECEIPT = (
    ROOT / "resources/web/known-best-packings/receipts/kingbird-2026-10-05-pictures.json"
)
#: Evan Daniel's KKT re-solve of every record packing, at 80 digits, printed to 39.
KKT_RESULTS = (
    ROOT
    / "resources/web/evand-square-packing-2026-10-05/square-packing/s12/search/exact/batch"
    / "results.json"
)
KKT_LABEL = "Evan Daniel's KKT side (evand/square-packing@13ee36e5, batch/results.json)"

FORMAT = "kingbird-svg-exact-facts-v1"
SIDE = "s"

#: The certificate's primes start here and stay below `PRIME_LIMIT`, where numpy's
#: `int64` holds every product of two residues summed over a row of `2^20` terms.
FIRST_PRIME = 100_003
PRIME_LIMIT = 1 << 20
DEFAULT_PRIMES = 12
#: SymPy counts real roots by Sturm sequences, which grow quickly with the degree.
DEFAULT_INDEX_MAX_DEGREE = 64
#: A `Root` body longer than this is elided from the recorded statements; its
#: coefficients are in `roots`.
ELIDE_ABOVE = 200

SOLVERS = (
    "FindRoot",
    "NSolve",
    "Solve",
    "Reduce",
    "Eliminate",
    "RootReduce",
    "Resultant",
    "GroebnerBasis",
    "FindMinimum",
    "NMinimize",
    "Minimize",
)
_SOLVER_CALL = re.compile(r"\b(" + "|".join(SOLVERS) + r")\[")
_ROOT_CALL = re.compile(r"\bRoot\[")
_ENTITY = re.compile(r'<!ENTITY\s+([\w.-]+)\s+"([^"]*)"\s*>(?P<tail>[^\n]*)')
_COMMENT = re.compile(r"<!--(.*?)-->", re.DOTALL)
_TERM = re.compile(r"([+-])?\s*(\d+)?\s*(?:\*?\s*(#1?)(?:\s*\^\s*(\d+))?)?\s*")
_ASSIGNED = re.compile(r"(\w+)\s*(?:=|->)\s*$")
_OPENERS = {"[": "]", "{": "}", "(": ")"}
_CLOSERS = frozenset(_OPENERS.values())

type Vector = npt.NDArray[np.int64]


class ExtractionError(RuntimeError):
    """The SVG, or a polynomial in it, cannot be read as this tool reads it."""


# --------------------------------------------------------------------------- reading


def _matching(text: str, start: int) -> int:
    """The index of the bracket that closes the one opening at `start`."""
    stack: list[str] = []
    for index in range(start, len(text)):
        char = text[index]
        if char in _OPENERS:
            stack.append(_OPENERS[char])
        elif char in _CLOSERS:
            if not stack or stack.pop() != char:
                raise ExtractionError(f"unbalanced {char!r} at offset {index}")
            if not stack:
                return index
    raise ExtractionError(f"bracket opened at offset {start} is never closed")


def top_level_split(text: str, separator: str = ",") -> list[str]:
    """Split on `separator` where no bracket is open, and strip each part."""
    parts: list[str] = []
    depth = 0
    current: list[str] = []
    for char in text:
        if char in _OPENERS:
            depth += 1
        elif char in _CLOSERS:
            depth -= 1
        if char == separator and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    parts.append("".join(current).strip())
    return parts


def head_comment(text: str) -> str:
    """The body of the comment the SVG opens with, before any DOCTYPE or drawing."""
    head = text.split("<svg", 1)[0].split("<!DOCTYPE", 1)[0]
    match = _COMMENT.search(head)
    return match.group(1) if match else ""


@dataclass(frozen=True)
class Entity:
    """One `<!ENTITY>` the drawing uses, with the formulas its trailing comments give."""

    name: str
    value: str
    notes: tuple[str, ...] = ()


def entities(text: str) -> list[Entity]:
    found: list[Entity] = []
    for match in _ENTITY.finditer(text.split("<svg", 1)[0]):
        notes = tuple(note.strip() for note in _COMMENT.findall(match["tail"]))
        found.append(Entity(match.group(1), match.group(2), notes))
    return found


def _looks_like_code(chunk: str) -> bool:
    return "[" in chunk and ("=" in chunk or re.match(r"\s*[A-Za-z]\w*\[", chunk) is not None)


def _balance(chunk: str) -> int:
    return sum(chunk.count(o) for o in _OPENERS) - sum(chunk.count(c) for c in _CLOSERS)


def statements(comment: str) -> list[str]:
    """The comment's Mathematica statements, each joined across its lines.

    A line that opens a bracket it does not close continues onto the next ones, but
    only when it reads as code, so an unbalanced parenthesis in prose cannot swallow
    the lines after it. Prose, blank lines and `(* ... *)` remarks are dropped.
    """
    found: list[str] = []
    pending: list[str] = []
    for line in comment.splitlines():
        stripped = line.strip()
        if pending:
            pending.append(stripped)
            joined = " ".join(pending)
            if _balance(joined) <= 0:
                found.append(joined.removesuffix(";").strip())
                pending = []
            continue
        if not stripped or not _looks_like_code(stripped):
            continue
        if _balance(stripped) > 0:
            pending = [stripped]
        else:
            found.append(stripped.removesuffix(";").strip())
    if pending:
        found.append(" ".join(pending))
    return found


@dataclass(frozen=True)
class SolverCall:
    """One solver call: its equations, its unknowns and any `WorkingPrecision`."""

    solver: str
    equations: tuple[str, ...]
    unknowns: tuple[str, ...]
    working_precision: int | None
    text: str


def _list_items(argument: str) -> tuple[str, ...]:
    argument = argument.strip()
    if argument.startswith("{") and _matching(argument, 0) == len(argument) - 1:
        return tuple(item for item in top_level_split(argument[1:-1]) if item)
    return (argument,) if argument else ()


def _unknown_name(item: str) -> str:
    """`s` from `s` and from FindRoot's `{s, 5.9339}`."""
    items = _list_items(item)
    return items[0] if item.strip().startswith("{") and items else item.strip()


def solver_calls(statement: str) -> list[SolverCall]:
    calls: list[SolverCall] = []
    for match in _SOLVER_CALL.finditer(statement):
        open_at = match.end() - 1
        close_at = _matching(statement, open_at)
        arguments = top_level_split(statement[open_at + 1 : close_at])
        options = [argument for argument in arguments if "->" in argument]
        positional = [argument for argument in arguments if "->" not in argument]
        precision: int | None = None
        for option in options:
            name, _, value = option.partition("->")
            if name.strip() == "WorkingPrecision" and value.strip().isdigit():
                precision = int(value.strip())
        equations = _list_items(positional[0]) if positional else ()
        unknowns = (
            tuple(_unknown_name(item) for item in _list_items(positional[1]))
            if len(positional) > 1
            else ()
        )
        calls.append(
            SolverCall(
                match.group(1),
                equations,
                unknowns,
                precision,
                statement[match.start() : close_at + 1],
            )
        )
    return calls


@dataclass(frozen=True)
class RootObject:
    """One `Root[poly &, k]`: its integer coefficients, or why they were not read."""

    assigned_to: str | None
    index: int | None
    coefficients: tuple[int, ...] | None
    """Primitive, highest degree first, with a positive leading coefficient."""
    problem: str | None
    body_characters: int
    span: tuple[int, int] = field(compare=False)

    @property
    def degree(self) -> int | None:
        return None if self.coefficients is None else len(self.coefficients) - 1

    @property
    def polynomial(self) -> str | None:
        return None if self.coefficients is None else format_polynomial(self.coefficients)


def read_pure_function(body: str) -> tuple[int, ...]:
    r"""Integer coefficients, highest first, of a Mathematica polynomial in `#` or `#1`.

    The body is a sum of terms `c*#^k`, `c #^k`, `#^k`, `c*#`, `#` and `c`, where `c` is a
    non-negative integer; each term after the first carries its sign. A line continuation
    (`\` and a newline) joins what it splits, and whitespace may separate the parts of a
    term but not the digits of a number. Anything else -- a rational or radical
    coefficient, a bracket, a power of a sum, a number broken across a line without a
    continuation -- is refused rather than guessed.
    """
    text = re.sub(r"\\\s*\n\s*", "", body).strip()
    if not text:
        raise ExtractionError("empty polynomial")
    terms: dict[int, int] = {}
    position = 0
    while position < len(text):
        match = _TERM.match(text, position)
        where = f"at {position}: {text[position : position + 40]!r}"
        if match is None or match.end() == position:
            raise ExtractionError(f"unreadable term {where}")
        sign, digits, variable, power = match.groups()
        if digits is None and variable is None:
            raise ExtractionError(f"unreadable term {where}")
        if position and sign is None:
            raise ExtractionError(f"term has no sign {where}")
        if match.end() < len(text) and text[match.end()] not in "+-":
            raise ExtractionError(f"unreadable term {where}")
        magnitude = int(digits) if digits is not None else 1
        exponent = 0 if variable is None else int(power) if power is not None else 1
        terms[exponent] = terms.get(exponent, 0) + (-magnitude if sign == "-" else magnitude)
        position = match.end()
    degree = max((power for power, value in terms.items() if value), default=0)
    if degree == 0:
        raise ExtractionError("polynomial has no positive-degree term")
    return tuple(terms.get(power, 0) for power in range(degree, -1, -1))


def _root_object(text: str, start: int, prefix: str) -> RootObject:
    open_at = start + len("Root")
    close_at = _matching(text, open_at)
    arguments = top_level_split(text[open_at + 1 : close_at])
    assigned = _ASSIGNED.search(prefix)
    name = assigned.group(1) if assigned else None
    index = int(arguments[1]) if len(arguments) == 2 and arguments[1].isdigit() else None
    body = arguments[0]
    span = (start, close_at + 1)
    # Mathematica writes `poly &`; the catalogue's comments often drop the `&`.
    if body.startswith("Function["):
        return RootObject(
            name, index, None, "a Function[...] body is not read", len(body), span
        )
    try:
        coefficients = primitive(read_pure_function(body.removesuffix("&")))
    except ExtractionError as error:
        return RootObject(name, index, None, str(error), len(body), span)
    return RootObject(name, index, coefficients, None, len(body), span)


def root_objects(statement: str) -> list[RootObject]:
    """Every `Root[...]` in one statement, with the name it is assigned to, if any."""
    found: list[RootObject] = []
    for match in _ROOT_CALL.finditer(statement):
        if any(start <= match.start() < end for start, end in (r.span for r in found)):
            continue
        found.append(_root_object(statement, match.start(), statement[: match.start()]))
    return found


def _elided(statement: str, roots: Sequence[RootObject]) -> str:
    pieces: list[str] = []
    cursor = 0
    for root in roots:
        start, end = root.span
        if root.body_characters <= ELIDE_ABOVE:
            continue
        what = (
            f"degree-{root.degree} polynomial, in roots"
            if root.degree is not None
            else f"{root.body_characters}-character body"
        )
        index = "" if root.index is None else f", {root.index}"
        pieces.extend((statement[cursor:start], f"Root[<{what}>{index}]"))
        cursor = end
    pieces.append(statement[cursor:])
    return "".join(pieces)


@dataclass
class SvgContent:
    """Everything this tool reads from one SVG, none of it the drawing."""

    credits: tuple[str, ...]
    entities: list[Entity]
    statements: list[str]
    solver_calls: list[SolverCall]
    roots: list[RootObject]

    def entity(self, name: str) -> str | None:
        return next((entity.value for entity in self.entities if entity.name == name), None)

    def side_roots(self) -> list[RootObject]:
        return [root for root in self.roots if root.assigned_to == SIDE]


def read_svg(text: str) -> SvgContent:
    comment = head_comment(text)
    found_statements = statements(comment)
    roots: list[RootObject] = []
    calls: list[SolverCall] = []
    kept: list[str] = []
    for statement in found_statements:
        here = root_objects(statement)
        roots.extend(here)
        calls.extend(solver_calls(statement))
        kept.append(_elided(statement, here))
    return SvgContent(picture_credits(text), entities(text), kept, calls, roots)


# --------------------------------------------------------------------------- modulo p


def _trim(values: Vector) -> Vector:
    nonzero = np.flatnonzero(values)
    return values[: int(nonzero[-1]) + 1] if nonzero.size else values[:0]


def _monic(values: Vector, prime: int) -> Vector:
    inverse = pow(int(values[-1]), -1, prime)
    return (values * inverse) % prime


def _remainder(dividend: Vector, divisor: Vector, prime: int) -> Vector:
    """`dividend mod divisor` over GF(prime); coefficients lowest first."""
    monic = _monic(divisor, prime)
    degree = len(monic) - 1
    remainder = dividend.copy() % prime
    for top in range(len(remainder) - 1, degree - 1, -1):
        lead = int(remainder[top])
        if lead:
            window = remainder[top - degree : top + 1]
            remainder[top - degree : top + 1] = (window - lead * monic) % prime
    return _trim(remainder[:degree])


def _quotient(dividend: Vector, divisor: Vector, prime: int) -> Vector:
    """The exact quotient over GF(prime); refuses a nonzero remainder."""
    inverse = pow(int(divisor[-1]), -1, prime)
    degree = len(divisor) - 1
    remainder = dividend.copy() % prime
    quotient = np.zeros(len(dividend) - degree, dtype=np.int64)
    for top in range(len(remainder) - 1, degree - 1, -1):
        lead = (int(remainder[top]) * inverse) % prime
        if lead:
            quotient[top - degree] = lead
            window = remainder[top - degree : top + 1]
            remainder[top - degree : top + 1] = (window - lead * divisor) % prime
    if _trim(remainder).size:
        raise ExtractionError("division over GF(p) left a remainder")
    return quotient


def _gcd(first: Vector, second: Vector, prime: int) -> Vector:
    a, b = _trim(first % prime), _trim(second % prime)
    while b.size:
        a, b = b, _remainder(a, b, prime)
    return _monic(a, prime)


def _multiply_mod(first: Vector, second: Vector, modulus: Vector, prime: int) -> Vector:
    return _remainder(np.convolve(first, second) % prime, modulus, prime)


def _power_of_x(exponent: int, modulus: Vector, prime: int) -> Vector:
    result = np.array([1], dtype=np.int64)
    base = _remainder(np.array([0, 1], dtype=np.int64), modulus, prime)
    while exponent:
        if exponent & 1:
            result = _multiply_mod(result, base, modulus, prime)
        exponent >>= 1
        if exponent:
            base = _multiply_mod(base, base, modulus, prime)
    return result


def degree_pattern(coefficients: Sequence[int], prime: int) -> tuple[int, ...] | None:
    """The degrees of the irreducible factors of `f mod prime`, in increasing order.

    `coefficients` are integers, highest degree first. None when the prime divides the
    leading coefficient or `f mod prime` has a repeated factor, where the pattern says
    nothing about factors over the integers. The factorization is distinct-degree:
    `x^(p^i) mod f` by a Frobenius matrix, and `gcd(f, x^(p^i) - x)` collects the
    factors of degree `i`.
    """
    if not 2 < prime < PRIME_LIMIT or len(coefficients) > PRIME_LIMIT:
        raise ExtractionError(f"prime {prime} or degree outside the int64-safe range")
    low = np.array([value % prime for value in reversed(coefficients)], dtype=np.int64)
    if low[-1] == 0:
        return None
    polynomial = _monic(low, prime)
    degree = len(polynomial) - 1
    derivative = _trim(
        np.array(
            [(k * int(polynomial[k])) % prime for k in range(1, degree + 1)], dtype=np.int64
        )
    )
    if _gcd(polynomial, derivative, prime).size > 1:
        return None
    if degree == 1:
        return (1,)
    x_power_p = _power_of_x(prime, polynomial, prime)
    frobenius = np.zeros((degree, degree), dtype=np.int64)
    row = np.array([1], dtype=np.int64)
    for index in range(degree):
        frobenius[index, : len(row)] = row
        row = _multiply_mod(row, x_power_p, polynomial, prime)
    x = np.zeros(degree, dtype=np.int64)
    x[1] = 1
    power = x.copy()
    rest = polynomial
    degrees: list[int] = []
    step = 0
    while 2 * (step + 1) <= len(rest) - 1:
        step += 1
        power = (power @ frobenius) % prime
        common = _gcd(rest, (power - x) % prime, prime)
        if common.size > 1:
            degrees.extend([step] * ((len(common) - 1) // step))
            rest = _quotient(rest, common, prime)
    if len(rest) > 1:
        degrees.append(len(rest) - 1)
    return tuple(sorted(degrees))


def _next_prime(after: int) -> int:
    candidate = after + 1 + (after % 2)
    while any(candidate % d == 0 for d in range(3, math.isqrt(candidate) + 1, 2)):
        candidate += 2
    return candidate


@dataclass(frozen=True)
class IrreducibilityCertificate:
    """Degree patterns modulo primes, and the factor degrees none of them excludes."""

    degree: int
    patterns: tuple[tuple[int, tuple[int, ...]], ...]
    skipped_primes: tuple[int, ...]
    open_degrees: tuple[int, ...]

    @property
    def irreducible(self) -> bool:
        return not self.open_degrees

    def summary(self) -> dict[str, object]:
        return {
            "irreducible": self.irreducible,
            "degree": self.degree,
            "primes": [prime for prime, _ in self.patterns],
            "patterns": [
                {"prime": prime, "factor_degrees": _run_lengths(pattern)}
                for prime, pattern in self.patterns
            ],
            "skipped_primes": list(self.skipped_primes),
            "open_degrees": list(self.open_degrees),
        }


def _run_lengths(pattern: Sequence[int]) -> str:
    """`[1, 1, 3]` as `1^2 3`, the cycle-type notation."""
    counts: dict[int, int] = {}
    for degree in pattern:
        counts[degree] = counts.get(degree, 0) + 1
    return " ".join(f"{d}^{c}" if c > 1 else str(d) for d, c in sorted(counts.items()))


def irreducibility_certificate(
    coefficients: Sequence[int],
    *,
    max_primes: int = DEFAULT_PRIMES,
    first_prime: int = FIRST_PRIME,
) -> IrreducibilityCertificate:
    """Intersect the factor degrees allowed modulo successive good primes.

    Stops as soon as no degree from 1 to `deg f - 1` is allowed, which proves `f`
    irreducible over the rationals, or after `max_primes` good primes, which proves
    nothing either way.
    """
    degree = len(coefficients) - 1
    if degree < 1:
        raise ExtractionError("a constant is not a polynomial to certify")
    allowed = (1 << degree) - 2
    patterns: list[tuple[int, tuple[int, ...]]] = []
    skipped: list[int] = []
    prime = first_prime - 1
    while allowed and len(patterns) < max_primes and len(skipped) < 4 * max_primes:
        prime = _next_prime(prime)
        pattern = degree_pattern(coefficients, prime)
        if pattern is None:
            skipped.append(prime)
            continue
        sums = 1
        for part in pattern:
            sums |= sums << part
        allowed &= sums
        patterns.append((prime, pattern))
    open_degrees = tuple(k for k in range(1, degree) if allowed >> k & 1)
    return IrreducibilityCertificate(degree, tuple(patterns), tuple(skipped), open_degrees)


# --------------------------------------------------------------------------- the root


def _scaled_value(coefficients: Sequence[int], numerator: int, scale: int) -> int:
    """`f(numerator / 10^scale) * 10^(scale * deg f)`, an exact integer."""
    denominator = 10**scale
    total = coefficients[0]
    power = 1
    for coefficient in coefficients[1:]:
        power *= denominator
        total = total * numerator + coefficient * power
    return total


def _derivative(coefficients: Sequence[int]) -> tuple[int, ...]:
    degree = len(coefficients) - 1
    return tuple(c * (degree - i) for i, c in enumerate(coefficients[:-1]))


def _second_derivative_bound(coefficients: Sequence[int], radius: int) -> int:
    """An integer upper bound for `|f''|` on `[-radius, radius]`."""
    degree = len(coefficients) - 1
    total = 0
    for index, coefficient in enumerate(coefficients):
        power = degree - index
        if power >= 2:
            total += abs(coefficient) * power * (power - 1) * radius ** (power - 2)
    return total


def _log10(value: int) -> float:
    """`log10(|value|)` for integers far beyond a float."""
    value = abs(value)
    shift = max(value.bit_length() - 64, 0)
    return math.log10(value >> shift) + shift * math.log10(2)


@dataclass(frozen=True)
class IsolatedRoot:
    """The one real root of `f` in `[centre - 10^-radius_exponent, centre + ...]`.

    `centre` is `centre_numerator / 10^scale`.
    """

    centre_numerator: int
    scale: int
    radius_exponent: int

    @property
    def centre(self) -> Fraction:
        return Fraction(self.centre_numerator, 10**self.scale)

    @property
    def radius(self) -> Fraction:
        return Fraction(1, 10**self.radius_exponent)

    def decimal(self, places: int) -> str:
        """The centre to `places` decimals, truncated."""
        places = min(places, self.scale)
        whole = self.centre_numerator // 10 ** (self.scale - places)
        text = str(whole).rjust(places + 1, "0")
        return f"{text[:-places]}.{text[-places:]}" if places else text

    def truncation(self, places: int) -> str | None:
        """The root's own truncation to `places` decimals, where the interval decides it."""
        low = (self.centre - self.radius) * 10**places
        high = (self.centre + self.radius) * 10**places
        if math.floor(low) != math.floor(high):
            return None
        whole = str(math.floor(low)).rjust(places + 1, "0")
        return f"{whole[:-places]}.{whole[-places:]}" if places else whole


def _newton(coefficients: Sequence[int], start: str, digits: int, decimals: int) -> str:
    """Newton's method at `digits` working digits, to a step below `10^-(decimals + 15)`.

    Returned as a fixed-point decimal with every working digit.
    """
    with mp.workdps(digits):
        x = mp.mpf(start)
        tolerance = mp.mpf(10) ** (-(decimals + 15))
        for _ in range(200):
            value, slope = mp.polyval(list(coefficients), x, derivative=True)
            if slope == 0:
                raise ExtractionError(f"f' vanishes at the Newton iterate {mp.nstr(x, 20)}")
            step = value / slope
            x -= step
            if abs(step) <= tolerance * max(abs(x), 1):
                break
        else:
            raise ExtractionError(f"Newton's method did not converge from {start}")
        return str(
            mp.nstr(x, digits, strip_zeros=False, min_fixed=-math.inf, max_fixed=math.inf)
        )


def _decimal_parts(text: str) -> tuple[int, int]:
    """`(numerator, scale)` with `text == numerator / 10^scale`."""
    try:
        value = Decimal(text.strip())
    except InvalidOperation as error:
        raise ExtractionError(f"not a decimal: {text!r}") from error
    sign, digits, exponent = value.as_tuple()
    if not isinstance(exponent, int):
        raise ExtractionError(f"not a finite decimal: {text!r}")
    # In chunks: `int(str)` refuses more than 4,300 digits, and a Newton centre for a
    # high-degree polynomial can carry more.
    numerator = 0
    for start in range(0, len(digits), 1000):
        chunk = digits[start : start + 1000]
        numerator = numerator * 10 ** len(chunk) + int("".join(map(str, chunk)))
    numerator *= -1 if sign else 1
    if exponent >= 0:
        return numerator * 10**exponent, 0
    return numerator, -exponent


def isolate_root(
    coefficients: Sequence[int], near: str, *, decimals: int = 0, attempts: int = 6
) -> IsolatedRoot:
    """Certify exactly one real root of `f` near the decimal `near`, in exact integers.

    See the module docstring: `r = 10^-m` with `2 r M2 <= |f'(c)|` makes `f` monotone on
    `[c - r, c + r]`, and a sign change there leaves exactly one root. Any smaller radius
    keeps the argument, so `m` is raised to at least `decimals`, the precision a
    comparison with a reference needs.
    """
    start_numerator, start_scale = _decimal_parts(near)
    # Every point the argument touches lies in [-bound, bound]; the centre is kept within
    # bound - 1 of the origin and the radius below 1.
    bound = abs(start_numerator) // 10**start_scale + 2
    magnitude = _log10(sum(abs(c) for c in coefficients) * bound ** (len(coefficients) - 1) + 1)
    derivative = _derivative(coefficients)
    twice_m2 = 2 * _second_derivative_bound(coefficients, bound)
    wanted = max(start_scale, decimals) + 10
    for _ in range(attempts):
        # Enough working digits to survive the cancellation among terms of `magnitude`.
        digits = int(magnitude) + wanted + 40
        centre, scale = _decimal_parts(_newton(coefficients, near, digits, wanted))
        if scale > wanted:
            centre //= 10 ** (scale - wanted)
            scale = wanted
        if abs(centre) > (bound - 1) * 10**scale:
            raise ExtractionError(f"Newton's method left the neighbourhood of {near}")
        slope = abs(_scaled_value(derivative, centre, scale))
        if slope == 0:
            raise ExtractionError("f' vanishes at the centre")
        # 2 r M2 <= |f'(c)| with r = 10^-m and f'(c) = slope / 10^(scale * deg f').
        threshold = twice_m2 * 10 ** (scale * (len(derivative) - 1))
        needed = 0 if threshold == 0 else max(0, math.ceil(_log10(threshold) - _log10(slope)))
        while slope * 10**needed < threshold:
            needed += 1
        needed = max(needed, decimals)
        if needed + 5 > scale:
            wanted = needed + 10
            continue
        shift = 10 ** (scale - needed)
        below = _scaled_value(coefficients, centre - shift, scale)
        above = _scaled_value(coefficients, centre + shift, scale)
        if below == 0 or above == 0 or (below > 0) == (above > 0):
            raise ExtractionError(
                f"no sign change on the interval of radius 1e-{needed} about the Newton point"
            )
        return IsolatedRoot(centre, scale, needed)
    raise ExtractionError("the isolating radius kept outrunning the Newton precision")


@dataclass(frozen=True)
class Agreement:
    """How closely one reference decimal agrees with the isolated root."""

    label: str
    reference: str
    printed_decimals: int
    difference_bound: str
    decimals_agreeing: int
    within_last_place: bool
    truncation_of_root: bool


def agreement(root: IsolatedRoot, label: str, reference: str) -> Agreement:
    numerator, scale = _decimal_parts(reference)
    difference = abs(root.centre - Fraction(numerator, 10**scale)) + root.radius
    agreeing = 0
    while agreeing < 10_000 and difference * 10 ** (agreeing + 1) < 1:
        agreeing += 1
    with localcontext() as context:
        context.prec = 3
        context.rounding = ROUND_CEILING
        bound = Decimal(difference.numerator) / Decimal(difference.denominator)
    return Agreement(
        label=label,
        reference=reference,
        printed_decimals=scale,
        difference_bound=f"{bound:.2E}",
        decimals_agreeing=agreeing,
        within_last_place=difference * 10**scale < 1,
        truncation_of_root=root.truncation(scale) == _canonical(reference, scale),
    )


def _canonical(reference: str, scale: int) -> str:
    numerator, _ = _decimal_parts(reference)
    whole = str(numerator).rjust(scale + 1, "0")
    return f"{whole[:-scale]}.{whole[-scale:]}" if scale else whole


def root_index(coefficients: Sequence[int], root: IsolatedRoot, max_degree: int) -> int | None:
    """Mathematica's `Root` index of the isolated root, or None where not counted."""
    if len(coefficients) - 1 > max_degree:
        return None
    try:
        import sympy as sp  # noqa: PLC0415 - optional dependency, imported where it is used
    except ImportError:
        return None
    s = sp.Symbol(SIDE)
    polynomial = sp.Poly(list(coefficients), s, domain="ZZ")
    lower = root.centre - root.radius
    below = polynomial.count_roots(None, sp.Rational(lower.numerator, lower.denominator))
    return int(below) + 1


# --------------------------------------------------------------------------- reports


@dataclass(frozen=True)
class Reference:
    label: str
    value: str


@dataclass
class PolynomialCheck:
    """Everything checked about one polynomial for the side."""

    degree: int
    polynomial: str
    certificate: IrreducibilityCertificate
    root: IsolatedRoot | None
    root_problem: str | None
    agreements: list[Agreement]
    index_stated: int | None
    index_counted: int | None

    @property
    def verified(self) -> bool:
        return (
            self.certificate.irreducible
            and self.root is not None
            and bool(self.agreements)
            and all(item.within_last_place for item in self.agreements)
            and (self.index_counted is None or self.index_stated in {None, self.index_counted})
        )

    def summary(self) -> dict[str, object]:
        root: dict[str, object] | None = None
        if self.root is not None:
            root = {
                "centre": self.root.decimal(self.root.scale),
                "radius": f"1e-{self.root.radius_exponent}",
            }
        return {
            "verified": self.verified,
            "degree": self.degree,
            "irreducibility": self.certificate.summary(),
            "isolated_root": root,
            "root_problem": self.root_problem,
            "agreements": [asdict(item) for item in self.agreements],
            "root_index": {"stated": self.index_stated, "counted": self.index_counted},
        }


def check_polynomial(
    coefficients: Sequence[int],
    references: Sequence[Reference],
    *,
    index: int | None = None,
    max_primes: int = DEFAULT_PRIMES,
    index_max_degree: int = DEFAULT_INDEX_MAX_DEGREE,
) -> PolynomialCheck:
    """Certify irreducibility, isolate the root at the first reference, compare all."""
    coefficients = primitive(tuple(coefficients))
    certificate = irreducibility_certificate(coefficients, max_primes=max_primes)
    root: IsolatedRoot | None = None
    problem: str | None = None
    agreements: list[Agreement] = []
    counted: int | None = None
    if not references:
        problem = "no reference decimal to isolate a root at"
    else:
        try:
            decimals = max(_decimal_parts(item.value)[1] for item in references) + 5
            root = isolate_root(coefficients, references[0].value, decimals=decimals)
        except ExtractionError as error:
            problem = str(error)
    if root is not None:
        agreements = [agreement(root, item.label, item.value) for item in references]
        counted = root_index(coefficients, root, index_max_degree)
    return PolynomialCheck(
        degree=len(coefficients) - 1,
        polynomial=format_polynomial(coefficients),
        certificate=certificate,
        root=root,
        root_problem=problem,
        agreements=agreements,
        index_stated=index,
        index_counted=counted,
    )


def kkt_side(n: int, path: Path = KKT_RESULTS) -> str | None:
    """Evan Daniel's KKT side for the record packing at `n`, where his batch has one."""
    try:
        rows = json.loads(read_retained_bytes(path))
    except FileNotFoundError:
        return None
    return next(
        (str(row["S_exact"]) for row in rows if row.get("n") == n and row.get("S_exact")), None
    )


def record_upper(n: int, frontier: Path = FRONTIER) -> dict[str, Any]:
    text = (frontier / f"n-{n:03d}.md").read_text(encoding="utf-8")
    return safe_load(text.split("---", 2)[1])["packing"]["reported_upper_bound"]


def default_references(
    n: int, *, svg_side: str | None, frontier: Path = FRONTIER
) -> list[Reference]:
    references: list[Reference] = []
    if svg_side:
        references.append(Reference("the SVG's own s entity", svg_side))
    kkt = kkt_side(n)
    if kkt:
        references.append(Reference(KKT_LABEL, kkt))
    printed = record_upper(n, frontier).get("value")
    if printed:
        references.append(
            Reference(f"the frontier record's printed side (n-{n:03d}.md)", str(printed))
        )
    return references


def pinned_reading(n: int, receipt: Path = READING_RECEIPT) -> dict[str, Any] | None:
    readings = json.loads(receipt.read_text(encoding="utf-8")).get("readings", [])
    return next((row for row in readings if row.get("n") == n), None)


# --------------------------------------------------------------------------- the record


class RecordRefusedError(RuntimeError):
    """The frontier record is not in the state `--write-record` may change."""


def record_with_polynomial(text: str, n: int, check: PolynomialCheck) -> str:
    """The record's text with the verified polynomial as its `minimal_polynomial`."""
    if not check.verified:
        raise RecordRefusedError(f"n={n}: the polynomial did not verify")
    upper = safe_load(text.split("---", 2)[1])["packing"]["reported_upper_bound"]
    if upper.get("algebraic_degree") != check.degree:
        recorded = upper.get("algebraic_degree")
        raise RecordRefusedError(f"n={n}: record degree {recorded} is not {check.degree}")
    if upper.get("algebraic_source") != "catalogue":
        raise RecordRefusedError(
            f"n={n}: algebraic_source is {upper.get('algebraic_source')!r}"
        )
    if upper.get("minimal_polynomial") is not None:
        raise RecordRefusedError(f"n={n}: the record already holds a minimal_polynomial")
    recorded_side = upper.get("value")
    if check.root is None or recorded_side is None:
        raise RecordRefusedError(f"n={n}: record and check do not both hold a side")
    try:
        side_agreement = agreement(check.root, "the record's side", str(recorded_side))
    except ExtractionError as error:
        raise RecordRefusedError(
            f"n={n}: the record's side cannot be compared: {error}"
        ) from error
    if not side_agreement.within_last_place:
        raise RecordRefusedError(
            f"n={n}: the record's side {recorded_side} does not agree with the polynomial root"
        )
    line = "    minimal_polynomial: null\n"
    if text.count(line) != 1:
        raise RecordRefusedError(f"n={n}: expected one null minimal_polynomial line")
    inserted = text.replace(line, f"    minimal_polynomial: '{check.polynomial}'\n")
    # Rewritten as the backfill writes the three fields, so its `--check` stays clean.
    written = backfilled(inserted, n)
    stored = safe_load(written.split("---", 2)[1])["packing"]["reported_upper_bound"]
    if stored.get("minimal_polynomial") != check.polynomial:
        raise RecordRefusedError(f"n={n}: the written polynomial does not read back")
    return written


# --------------------------------------------------------------------------- commands


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _print_check(check: PolynomialCheck) -> None:
    certificate = check.certificate
    print(f"  degree {check.degree}; polynomial text {len(check.polynomial):,} characters")
    if certificate.irreducible:
        primes = ", ".join(str(prime) for prime, _ in certificate.patterns)
        print(f"  irreducible over Q: degree patterns mod {primes}")
    else:
        print(
            f"  irreducibility NOT certified after {len(certificate.patterns)} primes; "
            f"factor degrees still open: {list(certificate.open_degrees)[:12]}"
        )
    for prime, pattern in certificate.patterns:
        print(f"    mod {prime}: {_run_lengths(pattern)}")
    if check.root is None:
        print(f"  no isolated root: {check.root_problem}")
    else:
        radius = check.root.radius_exponent
        print(f"  one real root in {check.root.decimal(45)}... +/- 1e-{radius}")
    for item in check.agreements:
        verdict = "within the last printed place" if item.within_last_place else "DISAGREES"
        print(
            f"    {item.label}: {item.reference} -> |difference| <= {item.difference_bound}, "
            f"{item.decimals_agreeing} decimals; {verdict}"
            + ("; the root's truncation" if item.truncation_of_root else "")
        )
    print(f"  Root index stated {check.index_stated}, counted {check.index_counted}")
    print(f"  verified: {check.verified}")


def run_svg(args: argparse.Namespace) -> int:
    n: int = args.n
    url = f"{KINGBIRD_BASE_URL}/square-{n}.svg"
    if args.svg is not None:
        data = Path(args.svg).read_bytes()
        modified: str | None = None
        retrieved = None
    else:
        retrieved = _now()
        try:
            data, modified = fetch_picture(url)
        except DerivationRefusedError as error:
            print(f"{url}: not fetched at {retrieved}: {error.detail}")
            return 2
    digest = hashlib.sha256(data).hexdigest()
    pinned = pinned_reading(n)
    same = None if pinned is None else pinned.get("sha256") == digest
    content = read_svg(data.decode("utf-8"))
    print(f"square-{n}.svg: {len(data):,} bytes, sha256 {digest}")
    if pinned is not None:
        verdict = "same" if same else "DIFFERENT"
        print(f"  the reading of 2026-10-05 pinned {pinned.get('sha256')}: {verdict}")
    print(
        f"  {len(content.credits)} credit lines, {len(content.entities)} entities, "
        f"{len(content.statements)} statements, {len(content.solver_calls)} solver calls, "
        f"{len(content.roots)} Root objects"
    )
    for call in content.solver_calls:
        print(
            f"    {call.solver}: {len(call.equations)} equation(s) in {list(call.unknowns)}"
            + (f", WorkingPrecision {call.working_precision}" if call.working_precision else "")
        )
    references = [Reference("--reference", value) for value in args.reference]
    references += default_references(n, svg_side=content.entity(SIDE))
    checks: list[PolynomialCheck] = []
    for root in content.roots:
        print(
            f"  Root assigned to {root.assigned_to!r}, index {root.index}: "
            + (f"degree {root.degree}" if root.coefficients else f"not read ({root.problem})")
        )
        if root.assigned_to == SIDE and root.coefficients is not None:
            check = check_polynomial(
                root.coefficients,
                references,
                index=root.index,
                max_primes=args.primes,
                index_max_degree=args.index_max_degree,
            )
            _print_check(check)
            checks.append(check)
    facts = {
        "format": FORMAT,
        "n": n,
        "url": url,
        "retrieved_utc": retrieved,
        "read_from": "fetched into memory" if args.svg is None else "a local copy",
        "bytes": len(data),
        "sha256": digest,
        "last_modified": modified,
        "same_as_reading_of_2026_10_05": same,
        "credits": list(content.credits),
        "entities": [asdict(entity) for entity in content.entities],
        "statements": content.statements,
        "solver_calls": [asdict(call) for call in content.solver_calls],
        "roots": [
            {
                "assigned_to": root.assigned_to,
                "index": root.index,
                "degree": root.degree,
                "coefficients": (
                    list(root.coefficients) if root.coefficients is not None else None
                ),
                "polynomial": root.polynomial,
                "problem": root.problem,
            }
            for root in content.roots
        ],
        "checks": [check.summary() for check in checks],
    }
    if args.out is not None:
        with atomic_output_file(Path(args.out)) as temporary:
            Path(temporary).write_text(json.dumps(facts, indent=1) + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    if args.write_record:
        if same is not True:
            print("--write-record: source reading pin missing or mismatched; record unchanged")
            return 1
        verified = [check for check in checks if check.verified]
        if len(verified) != 1:
            print(
                f"--write-record: {len(verified)} verified side polynomials; record unchanged"
            )
            return 1
        path = FRONTIER / f"n-{n:03d}.md"
        written = record_with_polynomial(path.read_text(encoding="utf-8"), n, verified[0])
        with atomic_output_file(path) as temporary:
            Path(temporary).write_text(written, encoding="utf-8")
        print(f"wrote minimal_polynomial into {path.relative_to(ROOT.parent)}")
    return 0 if checks and all(check.verified for check in checks) else 1


def run_record(args: argparse.Namespace) -> int:
    n: int = args.n
    upper = record_upper(n)
    text = upper.get("minimal_polynomial")
    if not text:
        print(f"n={n}: the record holds no minimal_polynomial")
        return 1
    references = [Reference("--reference", value) for value in args.reference]
    references += default_references(n, svg_side=None)
    check = check_polynomial(
        normalized_polynomial(str(text)),
        references,
        max_primes=args.primes,
        index_max_degree=args.index_max_degree,
    )
    print(f"n-{n:03d}.md minimal_polynomial:")
    _print_check(check)
    if args.out is not None:
        with atomic_output_file(Path(args.out)) as temporary:
            Path(temporary).write_text(
                json.dumps(check.summary(), indent=1) + "\n", encoding="utf-8"
            )
    return 0 if check.verified else 1


def parser() -> argparse.ArgumentParser:
    built = argparse.ArgumentParser(
        description="Read the exact content of a Kingbird SVG and check its polynomial."
    )
    commands = built.add_subparsers(dest="command", required=True)
    svg = commands.add_parser("svg", help="read square-N.svg, fetched into memory or local")
    record = commands.add_parser("record", help="check a frontier record's minimal_polynomial")
    for command in (svg, record):
        command.add_argument("n", type=int)
        command.add_argument(
            "--reference",
            action="append",
            default=[],
            help="a decimal the root must agree with; the first one given seeds Newton",
        )
        command.add_argument("--primes", type=int, default=DEFAULT_PRIMES)
        command.add_argument("--index-max-degree", type=int, default=DEFAULT_INDEX_MAX_DEGREE)
        command.add_argument("--out", help="write the facts or the check as JSON here")
    svg.add_argument("--svg", help="read this local copy instead of fetching")
    svg.add_argument(
        "--write-record",
        action="store_true",
        help="store a verified side polynomial in the frontier record",
    )
    return built


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "svg":
        return run_svg(args)
    return run_record(args)


if __name__ == "__main__":
    sys.exit(main())
