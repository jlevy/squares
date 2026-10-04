#!/usr/bin/env python3
# ruff: noqa: RUF001 -- the record's typography (minus signs, superscripts) is matched as written.
"""Inventory what in the record rests on T-007, and what else holds each item up.

T-007 is Nagamochi 2005, Theorem 2: `s(N) >= min(ceil(sqrt N), sqrt(N - 2 floor(sqrt N) + 1)
+ 1)`, with `s(k^2 - 1) = s(k^2 - 2) = k` as its exact cases. Karakuş (arXiv:2609.37410v1,
29 September 2026) gives counterexamples to the scoring assertion in Nagamochi's Lemma 1,
so the published proof of the rectangle bound behind the theorem is incomplete. His
separate strip-measure argument re-proves `s(k^2 - 1) = k` for every `k >= 2` and gives a
weaker explicit bound for every nonsquare `N >= 8`; it does not establish the full bound or
`s(k^2 - 2) = k`. Whether Nagamochi's lemma can be repaired is a separate audit. This
program answers the inventory question only, for every case record: does the operative
verified lower bound cite `E-nagamochi-lower`, and if so, what independent support covers
the same value or a weaker one.

Independent support is kept in separate fields, never merged:

- Karakuş's Corollary 1.2 (`s(k^2 - 1) = k`) and Corollary 6.2's explicit bound (6.1), as
  the archived preprint states them, each cited by its line there. Nothing here replays them.
- The register's own lower bounds at every `m <= n` whose evidence does not cite
  `E-nagamochi-lower`, carried to `n` by monotonicity (`s` is nondecreasing: delete squares).
  The verified and reported lanes stay apart; only the verified lane can clear a case.
- The area bound `sqrt(n)`, and Nagamochi's excess over it.
- chelokot's Lean re-proof of `s(n^2 - 2) = n`, located in his archived note and the
  archived Evand sources that report it. Since 2 October 2026 it is replayed here
  (`devtools.replay_chelokot_lean`, with its axiom receipt) and registered as
  `E-chelokot-square-minus-two-lean` (`T-086`), so a `k^2 - 2` case's operative bound cites
  it like any other verified evidence. This entry says whether the register holds the
  family theorem as verified, read from that evidence record; the individual values the
  same sources list stay reported pointers.
- Published proofs a case's own lower-bound prose cites without an evidence record (El
  Moumni 1999, Friedman's DS7 theorems), with any defect the same section names.
- Where an independent proof imports one of Nagamochi's auxiliary lemmas (Bentz 2010 and
  2016), the source says which, so its independence can be weighed.

Exposure classes, decided in this order for a case whose operative bound cites the record
(a case whose operative bound does not is `unaffected` outright):

1. `unaffected` -- the area bound or a registered verified independent bound reaches
   Nagamochi's value.
2. `k2-minus-1-reproved` -- `n = k^2 - 1`, covered only by Karakuş's Corollary 1.2.
3. `weakened-to` -- a nontrivial independent bound exists and falls short; the best is given.
4. `rests-on-t007-only` -- nothing beyond the area bound.

Every case is also classified with Karakuş removed, so the inventory stands whichever way
the audit of his argument goes.

Comparisons are exact: each value is a rational combination of square roots of squarefree
integers, whose sign is decided by linear independence (zero test) and integer square-root
enclosures (nonzero sign). The one verified value outside that arithmetic, the `n = 11`
root of Trump's polynomial, is compared by its display decimal with one unit in the last
place of slack, and a comparison that slack cannot separate is refused rather than guessed.

The document inventory is lexical, not semantic. Over the reader-facing documents, the
register, the research reports, the site templates and the case-prose generator, a line
`states` the theorem when it carries the closed form or a `k^2 - 2` identity or names
Nagamochi beside a proof word, `relies` on it when it names him beside a bound or floor, and
otherwise `mentions` him; a line is `qualified` once its paragraph names Karakuş's finding.
The retained record keeps, per document, only the counts and the deciding phrases -- no line
numbers, so an edit elsewhere in a document does not make it stale -- and `--report` scans
afresh and prints the lines.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.audit_t007_consumers --update
    uv run --frozen --all-extras --group dev python -m devtools.audit_t007_consumers --check
    uv run --frozen --all-extras --group dev python -m devtools.audit_t007_consumers --report
"""

from __future__ import annotations

import argparse
import ast
import json
import math
import re
from collections import Counter
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import check_nagamochi_bounds as nagamochi
from sqpack import retained_json
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
OUTPUT = (
    ROOT
    / "campaign/series/series-000-smoke-and-calibration/results"
    / "t007-consumer-audit.json"
)
GENERATOR = "python -m devtools.audit_t007_consumers"
RECORD = nagamochi.RECORD
T007 = "T-007"
#: Decimal places printed for every value, always rounded toward negative infinity.
PLACES = 12

UNAFFECTED = "unaffected"
REPROVED = "k2-minus-1-reproved"
WEAKENED = "weakened-to"
ONLY = "rests-on-t007-only"
CLASSES = (UNAFFECTED, REPROVED, WEAKENED, ONLY)

#: Result kinds that carry a lower bound on `s(n)`, for the per-case list of other results.
LOWER_KINDS = frozenset({"lower-bound", "optimality", "simplification", "audit", "correction"})

KARAKUS_ARCHIVE = "packing/resources/papers/karakus-2026-counterexample-nagamochi-scoring-lemma"
KARAKUS_TEXT = f"{KARAKUS_ARCHIVE}.md"
KARAKUS = {
    "citation": (
        "H. Karakuş, A counterexample to Nagamochi's scoring lemma and a new rectangle "
        "packing bound, arXiv:2609.37410v1 [math.CO], 29 September 2026"
    ),
    "url": "https://arxiv.org/abs/2609.37410",
    "archived": [f"{KARAKUS_ARCHIVE}.{suffix}" for suffix in ("pdf", "md", "raw.md")],
    "pdf_sha256": "39ae2ae44f063e6555240c4a246b47f687578c57196b70a9f5d66953d5cf6513",
    "status": (
        "Unrefereed preprint. Its mathematics is audited separately; nothing in this "
        "inventory replays it, and its two statements are used exactly as printed."
    ),
    "defect": (
        "Counterexamples to the scoring assertion of Nagamochi's Lemma 1, from an "
        "edge-incidence condition missing where Nagamochi's Lemma 6 is applied in his "
        "Section 5.5, Case 6 (Karakuş, Section 1, printed p. 3; construction in Section 4). "
        "They show the published proof incomplete and do not disprove the bound."
    ),
    "k2_minus_1": {
        "statement": "s(k^2 - 1) = k for every integer k >= 2",
        "location": (
            "Corollary 1.2, printed p. 3; proved in Section 6 from Corollary 6.1 "
            "(printed pp. 11-12)"
        ),
        "note": (
            "k = 2, s(3) = 2, is the classical case the paper cites to Friedman "
            "[4, Theorem 1]; the new proof covers k >= 3."
        ),
    },
    "explicit_bound": {
        "statement": (
            "s(N) >= 1/2 + sqrt(N - floor(sqrt(N)) + 1/4) > sqrt(N) for every nonsquare "
            "integer N >= 8"
        ),
        "location": "Corollary 6.2, eq. (6.1), printed p. 12",
        "exact_form_used_here": "1/2 + (1/2)*sqrt(4*N - 4*floor(sqrt(N)) + 1)",
        "note": "At N = k^2 - 1 with k >= 3 the bound is exactly k (printed p. 12).",
    },
    "not_established": (
        "Nagamochi's full rectangle bound, the identity s(k^2 - 2) = k, and the general "
        "lower bound of Nagamochi's Theorem 2 (Section 7, printed pp. 12-13)."
    ),
}
#: Where each statement above sits in the archived transcription. The needles are the
#: printed text, so the inventory fails rather than cite a formula the archive no longer
#: carries -- (6.1)'s needle is the formula `karakus_bound` evaluates.
KARAKUS_AT = {
    "defect_at": "edge-incidence condition missing from the application of [1, Lemma 6]",
    "k2_minus_1_at": "**Corollary 1.2.** *For every integer $k \\geq 2$, $s(k^2-1) = k$.*",
    "explicit_bound_at": (
        "s(N) \\geq \\frac{1}{2}+\\sqrt{N-\\lfloor\\sqrt{N}\\rfloor+\\frac{1}{4}} > \\sqrt{N}. "
        "\\tag{6.1}"
    ),
    "explicit_bound_endpoint_at": "the lower bound in (6.1) is exactly $n$",
    "not_established_at": "The present argument does not establish or disprove",
}

LITERATURE = (
    "packing/resources/web/evand-square-packing-2026-09-26/square-packing/s12/notes/"
    "literature-s32.md"
)
SOURCES_PAGE = (
    "packing/resources/web/evand-square-packing-2026-10-01/source/site/www/sources.html"
)
CHELOKOT_ARCHIVE = "packing/resources/web/chelokot-nagamochi-counterexample-2026-10-02"
CHELOKOT_NOTE = f"{CHELOKOT_ARCHIVE}/upstream/docs/nagamochi-score-counterexample.md"
CHELOKOT_README = f"{CHELOKOT_ARCHIVE}/README.md"
CHELOKOT = {
    "repository": "https://github.com/chelokot/square-packing-archive",
    "archived": CHELOKOT_ARCHIVE,
    "kind": "Lean theorem, replayed here with its axiom receipt",
    "claim": (
        "A closed Lean theorem, Records.NearSquare.squareMinusTwo_isMinimumSide, that "
        "s(n^2 - 2) = n for every integer n >= 2, compensating low-scoring squares with "
        "other squares of the packing instead of assuming Nagamochi's Lemma 1."
    ),
    "claim_document": (
        "docs/nagamochi-compensation-proof.md at upstream head 753079eb, pinned by digest in "
        "the archive README and not retained"
    ),
    "evidence": "E-chelokot-square-minus-two-lean",
    "result": "T-086",
    "receipt": (
        "packing/campaign/series/series-000-smoke-and-calibration/results/"
        "chelokot-lean-replay/receipt.json"
    ),
    "status": (
        "Replayed here on 2 October 2026: the archive built at 753079eb with its pinned "
        "toolchain, and the theorem's axioms are exactly propext, Classical.choice and "
        "Quot.sound. A `k^2 - 2` case's operative bound cites it directly."
    ),
}
#: Where the archived sources report chelokot's Lean claim. Each needle must occur in its
#: file, and the line it is found on is what the inventory cites.
CHELOKOT_REPORTS = (
    (
        CHELOKOT_NOTE,
        "The square-container result now has a [separate Lean proof]",
    ),
    (
        CHELOKOT_README,
        "closed Lean theorem, `Records.NearSquare.squareMinusTwo_isMinimumSide`",
    ),
    (
        LITERATURE,
        "s(n²-2) = n re-proved by a replacement argument",
    ),
    (
        LITERATURE,
        "s(n²-2) = n, s(6), s(10), s(13), s(22), s(33), s(46) (+47, 48, 23, 34)",
    ),
    (
        SOURCES_PAGE,
        "kernel-checked proof: s(n²−2) = n",
    ),
)
#: The cases the same source names individually, beyond the `n^2 - 2` family.
CHELOKOT_INDIVIDUAL = (
    (
        (23, 34),
        LITERATURE,
        "chelokot generalizes (s(23): 3×4 + 2×5 = 22 pts; s(34): 3×5 + 3×6 = 33 pts)",
        "a staggered-lattice unavoidable set of n - 1 points, generalizing Bentz's s(46)",
    ),
    (
        (23, 34, 47, 48),
        LITERATURE,
        "s(n²-2) = n, s(6), s(10), s(13), s(22), s(33), s(46) (+47, 48, 23, 34)",
        "listed among the archive's kernel-checked values",
    ),
)

#: Independent published proofs that import one of Nagamochi's auxiliary lemmas. Neither
#: lemma is the Lemma 1 scoring assertion Karakuş refutes, but a reader weighing the
#: independence of these routes should know they share a citation with T-007.
SHARED_LEMMAS = {
    "E-bentz-2010-proof": (
        "packing/resources/papers/bentz-2010-optimal-packings-13-and-46.md",
        "**Lemma 1** (Nagamochi [7], Stromquist [8])",
        "packing/resources/papers/nagamochi-2005-packing-unit-squares-in-a-rectangle.raw.md",
        "Lemma 7 Let S be a",
        "Bentz 2010, Lemma 1 is Nagamochi's Lemma 7(ii), co-credited there to Stromquist.",
    ),
    "E-bentz-2016-proof": (
        "packing/resources/papers/bentz-2016-optimal-packings-22-and-33.md",
        "**Lemma 4** (Nagamochi [8])",
        "packing/resources/papers/nagamochi-2005-packing-unit-squares-in-a-rectangle.raw.md",
        "Lemma 2 Let S be a",
        "Bentz 2016, Lemma 4 is the unit-box case of Nagamochi's Lemma 2.",
    ),
}


# ---------------------------------------------------------------------------------------
# Exact arithmetic over sums of square roots.
# ---------------------------------------------------------------------------------------


def _square_split(value: int) -> tuple[int, int]:
    """`(s, r)` with `value = s * s * r` and `r` squarefree, for a positive integer."""
    outside, inside, factor = 1, value, 2
    while factor * factor <= inside:
        while inside % (factor * factor) == 0:
            inside //= factor * factor
            outside *= factor
        factor += 1 if factor == 2 else 2
    return outside, inside


def _fixed(scaled: int, places: int) -> str:
    sign = "-" if scaled < 0 else ""
    digits = str(abs(scaled)).rjust(places + 1, "0")
    return f"{sign}{digits[:-places]}.{digits[-places:]}"


@dataclass(frozen=True)
class Surd:
    """A finite sum of rational multiples of square roots of squarefree integers.

    `terms` is sorted by radicand, radicand `1` is the rational part, and no coefficient is
    zero, so two equal values have equal terms.
    """

    terms: tuple[tuple[int, Fraction], ...] = ()

    @classmethod
    def rational(cls, value: Fraction | int) -> Surd:
        value = Fraction(value)
        return cls(((1, value),)) if value else cls()

    @classmethod
    def root(cls, value: Fraction | int) -> Surd:
        value = Fraction(value)
        if value < 0:
            raise ValueError(f"square root of a negative number: {value}")
        if not value:
            return cls()
        outside, inside = _square_split(value.numerator * value.denominator)
        return cls(((inside, Fraction(outside, value.denominator)),))

    @staticmethod
    def combine(pairs: Iterable[tuple[int, Fraction]]) -> Surd:
        totals: dict[int, Fraction] = {}
        for radicand, coefficient in pairs:
            totals[radicand] = totals.get(radicand, Fraction()) + coefficient
        return Surd(tuple(sorted((r, c) for r, c in totals.items() if c)))

    def __add__(self, other: Surd) -> Surd:
        return Surd.combine((*self.terms, *other.terms))

    def __neg__(self) -> Surd:
        return Surd(tuple((radicand, -coefficient) for radicand, coefficient in self.terms))

    def __sub__(self, other: Surd) -> Surd:
        return self + (-other)

    def __mul__(self, other: Surd) -> Surd:
        pairs: list[tuple[int, Fraction]] = []
        for left, a in self.terms:
            for right, b in other.terms:
                outside, inside = _square_split(left * right)
                pairs.append((inside, a * b * outside))
        return Surd.combine(pairs)

    def __truediv__(self, other: Surd) -> Surd:
        if len(other.terms) != 1:
            raise ValueError(
                "division by zero or by a sum of radicals is outside this arithmetic"
            )
        radicand, coefficient = other.terms[0]
        return self * Surd(((radicand, 1 / (coefficient * radicand)),))

    @property
    def as_rational(self) -> Fraction | None:
        if all(radicand == 1 for radicand, _ in self.terms):
            return sum((coefficient for _, coefficient in self.terms), Fraction())
        return None

    def enclosure(self, digits: int) -> tuple[Fraction, Fraction]:
        """Rational bounds on the value, each radical bracketed to `digits` places."""
        scale = 10**digits
        low = high = Fraction()
        for radicand, coefficient in self.terms:
            if radicand == 1:
                low += coefficient
                high += coefficient
                continue
            floor = math.isqrt(radicand * scale * scale)
            ends = (
                coefficient * Fraction(floor, scale),
                coefficient * Fraction(floor + 1, scale),
            )
            low += min(ends)
            high += max(ends)
        return low, high

    def sign(self) -> int:
        """The exact sign.

        Square roots of distinct squarefree integers are linearly independent over the
        rationals, so a sum with any term is nonzero and refining its enclosure separates it
        from zero in finitely many steps.
        """
        if not self.terms:
            return 0
        digits = 16
        while digits <= 4096:
            low, high = self.enclosure(digits)
            if low > 0:
                return 1
            if high < 0:
                return -1
            digits *= 2
        raise ArithmeticError(f"sign not separated at 4096 digits: {self.render()}")

    def floor(self) -> int:
        rational = self.as_rational
        if rational is not None:
            return math.floor(rational)
        digits = 16
        while digits <= 4096:
            low, high = self.enclosure(digits)
            if math.floor(low) == math.floor(high):
                return math.floor(low)
            digits *= 2
        raise ArithmeticError(f"floor not separated at 4096 digits: {self.render()}")

    def decimal(self, places: int = PLACES) -> str:
        """The value to `places` decimals, rounded toward negative infinity."""
        low, _ = self.enclosure(places + 8)
        return _fixed(math.floor(low * 10**places), places)

    def render(self) -> str:
        if not self.terms:
            return "0"
        parts: list[str] = []
        for radicand, coefficient in self.terms:
            if radicand == 1:
                parts.append(str(coefficient))
            elif coefficient == 1:
                parts.append(f"sqrt({radicand})")
            elif coefficient.denominator == 1:
                parts.append(f"{coefficient}*sqrt({radicand})")
            else:
                parts.append(f"({coefficient})*sqrt({radicand})")
        return " + ".join(parts).replace("+ -", "- ").replace("+ (-", "- (")


_IMPLICIT_PRODUCT = re.compile(r"(?<=[0-9)])\s*(?=sqrt\(|\()")
_BINARY: dict[type[ast.operator], Callable[[Surd, Surd], Surd]] = {
    ast.Add: Surd.__add__,
    ast.Sub: Surd.__sub__,
    ast.Mult: Surd.__mul__,
    ast.Div: Surd.__truediv__,
}


def parse_exact(text: str) -> Surd:
    """Parse the register's exact forms: rationals, `sqrt` of a rational, `floor`, + - * /."""
    source = _IMPLICIT_PRODUCT.sub("*", text)

    def visit(node: ast.AST) -> Surd:
        if isinstance(node, ast.Constant) and type(node.value) in {int, float}:
            literal = ast.get_source_segment(source, node)
            if literal is None:
                raise ValueError(f"unsupported exact expression: {text!r}")
            return Surd.rational(Fraction(literal))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub | ast.UAdd):
            value = visit(node.operand)
            return -value if isinstance(node.op, ast.USub) else value
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY:
            return _BINARY[type(node.op)](visit(node.left), visit(node.right))
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in {"sqrt", "floor"}
            and len(node.args) == 1
            and not node.keywords
        ):
            argument = visit(node.args[0])
            if node.func.id == "floor":
                return Surd.rational(argument.floor())
            rational = argument.as_rational
            if rational is None:
                raise ValueError(f"nested radical in exact expression: {text!r}")
            return Surd.root(rational)
        raise ValueError(f"unsupported exact expression: {text!r}")

    try:
        tree = ast.parse(source, mode="eval")
    except SyntaxError as error:
        raise ValueError(f"unsupported exact expression: {text!r}") from error
    return visit(tree.body)


@dataclass(frozen=True)
class Quantity:
    """A value and how it was obtained. `slack` bounds how far the true value may sit."""

    value: Surd
    basis: str
    slack: Fraction = Fraction()


def compare(left: Quantity, right: Quantity) -> int:
    """Exact sign of `left - right`, or a refusal when display slack cannot decide it."""
    difference = left.value - right.value
    slack = left.slack + right.slack
    if not slack:
        return difference.sign()
    digits = 16
    while digits <= 256:
        low, high = difference.enclosure(digits)
        if low > slack:
            return 1
        if high < -slack:
            return -1
        digits *= 2
    raise ValueError(
        f"cannot separate {left.basis} from {right.basis} within display slack {slack}"
    )


def quantity_entry(quantity: Quantity) -> dict[str, Any]:
    return {
        "exact": quantity.value.render(),
        "decimal": quantity.value.decimal(),
        "basis": quantity.basis,
    }


# ---------------------------------------------------------------------------------------
# The theorems.
# ---------------------------------------------------------------------------------------


def family(n: int) -> tuple[str, int] | None:
    """Which of Nagamochi's exact families `n` belongs to, and its `k`."""
    root = math.isqrt(n)
    if root * root == n:
        return "k^2", root
    above = root + 1
    if n == above * above - 1:
        return "k^2-1", above
    if n == above * above - 2:
        return "k^2-2", above
    return None


def nagamochi_value(n: int) -> Surd:
    """Theorem 2 at `n`, exactly; its exactness test is `check_nagamochi_bounds`'s own."""
    approximate, is_exact = nagamochi.theorem_two(n)
    value = (
        Surd.rational(math.isqrt(n - 1) + 1)
        if is_exact
        else Surd.rational(1) + Surd.root(n - 2 * math.isqrt(n) + 1)
    )
    low, high = value.enclosure(76)
    if not low - Fraction(1, 10**70) <= Fraction(approximate) <= high + Fraction(1, 10**70):
        raise ValueError(f"n={n}: exact value {value.render()} disagrees with {approximate}")
    return value


def karakus_bound(n: int) -> Surd | None:
    """Karakuş's (6.1) at `n`, or `None` where Corollary 6.2 does not apply."""
    root = math.isqrt(n)
    if n < 8 or root * root == n:
        return None
    return Surd.rational(Fraction(1, 2)) + Surd.root(Fraction(4 * (n - root) + 1, 4))


def area_bound(n: int) -> Surd:
    return Surd.root(n)


# ---------------------------------------------------------------------------------------
# The register.
# ---------------------------------------------------------------------------------------


def covers(scope: Mapping[str, Any], n: int) -> bool:
    if "n_values" in scope:
        return n in scope["n_values"]
    return scope["n_min"] <= n <= scope["n_max"]


@dataclass(frozen=True)
class Register:
    cases: dict[int, dict[str, Any]]
    results: tuple[dict[str, Any], ...]
    evidence: dict[str, dict[str, Any]]

    def results_for(self, evidence: Sequence[str], n: int) -> list[str]:
        """Results at `n` citing this evidence: every one of it, else any of it."""
        wanted = set(evidence)
        covering = [result for result in self.results if covers(result["scope"], n)]
        whole = [r["id"] for r in covering if wanted <= set(r.get("evidence") or ())]
        if whole:
            return whole
        return [r["id"] for r in covering if wanted & set(r.get("evidence") or ())]

    def result(self, identifier: str) -> dict[str, Any]:
        return next(result for result in self.results if result["id"] == identifier)


@cache
def register() -> Register:
    found = nagamochi.cases()
    expected = list(range(1, max(found) + 1))
    if sorted(found) != expected:
        raise ValueError(f"case records are not contiguous from 1: {sorted(found)[:5]}...")
    results = load_yaml(nagamochi.RESULTS.read_text(encoding="utf-8"))["results"]
    evidence = load_yaml(nagamochi.EVIDENCE.read_text(encoding="utf-8"))["evidence"]
    return Register(found, tuple(results), {record["id"]: record for record in evidence})


def lane_quantity(bound: Mapping[str, Any], *, verified: bool) -> Quantity:
    """A lane's value: its exact form when the arithmetic covers it, else its display.

    A verified display (only the `n = 11` root) carries one unit in its last place of slack.
    A reported display is taken as printed, since a reported bound never clears a case.
    """
    form = bound.get("exact_form")
    if form is not None and not str(form).startswith("root("):
        return Quantity(parse_exact(str(form)), "exact-form")
    display = str(bound["value"])
    places = len(display.partition(".")[2])
    if verified:
        return Quantity(
            Surd.rational(Fraction(display)), "display-decimal", Fraction(1, 10**places)
        )
    return Quantity(Surd.rational(Fraction(display)), "display-decimal-as-printed")


@dataclass(frozen=True)
class Source:
    """A lower bound recorded at case `n`, independent of the record under audit."""

    n: int
    quantity: Quantity
    evidence: tuple[str, ...]
    results: tuple[str, ...]
    proved_by: tuple[str, ...] = ()


def independent_sources(lane: str) -> dict[int, Source]:
    """Each case's `lane` bound, where its evidence does not cite `E-nagamochi-lower`."""
    reg = register()
    found: dict[int, Source] = {}
    for n, case in sorted(reg.cases.items()):
        bound = case[lane]
        evidence = tuple(bound.get("evidence") or ())
        if RECORD in evidence or bound.get("kind") == "nagamochi":
            continue
        found[n] = Source(
            n,
            lane_quantity(bound, verified=lane == "verified_lower_bound"),
            evidence,
            tuple(reg.results_for(evidence, n)),
            tuple(bound.get("proved_by") or ()),
        )
    return found


def monotone_best(sources: Mapping[int, Source], last: int) -> dict[int, list[Source]]:
    """For each `n`, the strongest sources at some `m <= n`, one per distinct evidence set.

    Within one evidence set the smallest `m` is kept, since a later case carrying the same
    evidence is that bound's own monotonicity copy.
    """
    best: list[Source] = []
    table: dict[int, list[Source]] = {}
    for n in range(1, last + 1):
        source = sources.get(n)
        if source is not None:
            sign = 1 if not best else compare(source.quantity, best[0].quantity)
            if sign > 0:
                best = [source]
            elif sign == 0 and all(set(source.evidence) != set(kept.evidence) for kept in best):
                best = [*best, source]
        table[n] = list(best)
    return table


@cache
def pointer(path: str, needle: str) -> str:
    """`path:line` of the first line containing `needle`; the needle must be there."""
    # Split on newlines only: `splitlines` also breaks at the form feeds pdfminer leaves in
    # the archive, which would put the cited line out of step with every editor and grep.
    for number, line in enumerate((REPO / path).read_text(encoding="utf-8").split("\n"), 1):
        if needle in line:
            return f"{path}:{number}"
    raise ValueError(f"{path} no longer contains {needle!r}")


def shared_lemma(evidence: Sequence[str], results: Sequence[str]) -> dict[str, Any] | None:
    reg = register()
    hits = [key for key in evidence if key in SHARED_LEMMAS]
    if not hits:
        return None
    key = hits[0]
    paper, citing, original, lemma, summary = SHARED_LEMMAS[key]
    others = sorted(
        {
            identifier
            for result in results
            for identifier in reg.result(result).get("evidence") or ()
            if identifier not in evidence
            and reg.evidence.get(identifier, {}).get("assurance") == "verified"
            and reg.evidence[identifier].get("claim") in {"lower-bound", "exact-value"}
        }
    )
    return {
        "evidence": key,
        "summary": summary,
        "cited_at": pointer(paper, citing),
        "nagamochi_lemma_at": pointer(original, lemma),
        "other_verified_evidence_in_the_same_results": others,
    }


def source_entry(source: Source, n: int) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "n": source.n,
        "via": "direct" if source.n == n else "monotonicity",
        "evidence": list(source.evidence),
        "results": list(source.results),
    }
    if source.proved_by:
        entry["proved_by"] = list(source.proved_by)
    caveat = shared_lemma(source.evidence, source.results)
    if caveat is not None:
        entry["shares_a_nagamochi_lemma"] = caveat
    return entry


def support_entry(
    sources: list[Source], n: int, target: Quantity | None
) -> dict[str, Any] | None:
    if not sources:
        return None
    quantity = sources[0].quantity
    entry = {
        **quantity_entry(quantity),
        "sources": [source_entry(source, n) for source in sources],
        "reaches_nagamochi": None if target is None else compare(quantity, target) >= 0,
    }
    if target is not None:
        entry["shortfall_below_nagamochi"] = (target.value - quantity.value).decimal()
    return entry


def chelokot_replayed() -> bool:
    """Whether the register holds chelokot's family theorem as verified evidence."""
    record = register().evidence.get(str(CHELOKOT["evidence"]))
    return (
        record is not None
        and record.get("assurance") == "verified"
        and record.get("replay_status") == "passed"
    )


def chelokot_entry(n: int) -> dict[str, Any] | None:
    shape = family(n)
    family_verified = chelokot_replayed()
    claims: list[dict[str, Any]] = []
    if shape is not None and shape[0] in {"k^2-2", "k^2-1"} and shape[1] >= 2:
        claims.append(
            {
                "statement": "s(n^2 - 2) = n for every n >= 2, by a Lean compensation proof",
                "applies": "direct" if shape[0] == "k^2-2" else "monotonicity from s(k^2 - 2)",
                "value": shape[1],
                "verified": family_verified,
                "reported_at": [pointer(path, needle) for path, needle in CHELOKOT_REPORTS],
            }
        )
    for values, path, needle, statement in CHELOKOT_INDIVIDUAL:
        if n in values:
            claims.append(
                {
                    "statement": f"s({n}): {statement}",
                    "applies": "direct",
                    "value": math.isqrt(n - 1) + 1,
                    "verified": False,
                    "reported_at": [pointer(path, needle)],
                }
            )
    if not claims:
        return None
    return {
        "kind": CHELOKOT["kind"],
        "verified": any(claim["verified"] for claim in claims),
        "claims": claims,
    }


_PAPER_LINK = re.compile(r"\[([^\]]+)\]\(\.\./resources/papers/([^)#]+)\)")
_DEFECT_LINK = re.compile(r"\[(D-\d+(?:[–-]D-\d+)?)\]")


def prose_published_proofs(n: int) -> dict[str, Any] | None:
    """Papers other than Nagamochi's that the case's lower-bound prose cites as proofs.

    They are archived but carry no evidence record, so they count as published support
    the register has not adopted; defects named in the same section travel with them.
    """
    path = f"packing/frontier/n-{n:03d}.md"
    lines = (REPO / path).read_text(encoding="utf-8").split("\n")
    start = next((i for i, line in enumerate(lines) if line == "## The lower bound"), None)
    if start is None:
        return None
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith(("## ", "<!--"))),
        len(lines),
    )
    proofs = [
        {
            "label": match.group(1),
            "source": f"packing/resources/papers/{match.group(2)}",
            "at": f"{path}:{i + 1}",
        }
        for i in range(start, end)
        for match in _PAPER_LINK.finditer(lines[i])
        if "nagamochi" not in match.group(2)
    ]
    if not proofs:
        return None
    defects = sorted(
        {m.group(1) for i in range(start, end) for m in _DEFECT_LINK.finditer(lines[i])}
    )
    return {"status": "published-archived-unregistered", "proofs": proofs, "defects": defects}


def classify(
    *,
    cites_t007: bool,
    target: Quantity | None,
    area: Quantity,
    registered: Quantity | None,
    shape: tuple[str, int] | None,
    karakus: Quantity | None,
) -> dict[str, Any]:
    """The exposure class, by the order in the module docstring.

    Passing `karakus=None` and a `shape` of `None` for `n = k^2 - 1` is how the
    classification without Karakuş is asked for.
    """
    if not cites_t007:
        return {
            "class": UNAFFECTED,
            "reason": "operative-bound-independent",
            "weakened_to": None,
        }
    if target is None:
        raise ValueError("a case citing the record must have a Nagamochi value")
    if compare(area, target) >= 0:
        return {"class": UNAFFECTED, "reason": "area-bound", "weakened_to": None}
    if registered is not None and compare(registered, target) >= 0:
        return {
            "class": UNAFFECTED,
            "reason": "registered-verified-bound-covers-it",
            "weakened_to": None,
        }
    if shape is not None and shape[0] == "k^2-1" and shape[1] >= 2:
        return {"class": REPROVED, "reason": "karakus-corollary-1.2", "weakened_to": None}
    candidates: list[tuple[str, Quantity]] = []
    if registered is not None and compare(registered, area) > 0:
        candidates.append(("registered-verified-bound", registered))
    if karakus is not None:
        candidates.append(("karakus-6.1", karakus))
    if not candidates:
        return {"class": ONLY, "reason": "area-bound-only", "weakened_to": None}
    label, best = candidates[0]
    for other_label, other in candidates[1:]:
        if compare(other, best) > 0:
            label, best = other_label, other
    return {
        "class": WEAKENED,
        "reason": label,
        "weakened_to": {
            **quantity_entry(best),
            "source": label,
            "shortfall_below_nagamochi": (target.value - best.value).decimal(),
        },
    }


def case_row(
    n: int,
    verified: list[Source],
    reported: list[Source],
) -> dict[str, Any]:
    reg = register()
    case = reg.cases[n]
    lower = case["verified_lower_bound"]
    evidence = list(lower.get("evidence") or ())
    cites = RECORD in evidence
    scope = reg.evidence[RECORD]["scope"]
    applies = covers(scope, n)
    target = Quantity(nagamochi_value(n), "nagamochi-theorem-2") if applies else None
    area = Quantity(area_bound(n), "area")
    shape = family(n)
    karakus_value = karakus_bound(n)
    karakus = None if karakus_value is None else Quantity(karakus_value, "karakus-6.1")
    registered = verified[0].quantity if verified else None
    reported_lower = case["reported_lower_bound"]
    others = [
        {
            "id": result["id"],
            "kind": result["kind"],
            "verification": result["verification"],
            "confirmation": result["confirmation"],
        }
        for result in reg.results
        if result["id"] != T007 and result["kind"] in LOWER_KINDS and covers(result["scope"], n)
    ]
    karakus_k2 = None
    if shape is not None and shape[0] == "k^2-1" and shape[1] >= 2:
        karakus_k2 = {"value": shape[1], "statement": f"s({n}) = {shape[1]}"}
    karakus_explicit = None
    if karakus is not None:
        karakus_explicit = {
            **quantity_entry(karakus),
            "reaches_nagamochi": None if target is None else compare(karakus, target) >= 0,
        }
        if target is not None:
            karakus_explicit["shortfall_below_nagamochi"] = (
                target.value - karakus.value
            ).decimal()
    area_entry: dict[str, Any] = quantity_entry(area)
    if target is not None:
        area_entry["nagamochi_excess"] = (target.value - area.value).decimal()
    primary = classify(
        cites_t007=cites,
        target=target,
        area=area,
        registered=registered,
        shape=shape,
        karakus=karakus,
    )
    without = classify(
        cites_t007=cites,
        target=target,
        area=area,
        registered=registered,
        shape=None,
        karakus=None,
    )
    return {
        "n": n,
        "status": case["status"],
        "reported_status": case["reported_status"],
        "family": None if shape is None else {"form": shape[0], "k": shape[1]},
        "operative_lower_bound": {
            "value": str(lower["value"]),
            "exact_form": lower.get("exact_form"),
            "evidence": evidence,
            "results": reg.results_for(evidence, n),
            "cites_t007": cites,
            "t007_scope_covers_n": covers(reg.result(T007)["scope"], n),
        },
        "reported_lower_bound": {
            "value": str(reported_lower["value"]),
            "evidence": list(reported_lower.get("evidence") or ()),
            "cites_t007": RECORD in (reported_lower.get("evidence") or ()),
        },
        "nagamochi": None
        if target is None
        else {**quantity_entry(target), "exact_case": shape is not None and shape[1] >= 2},
        "exact_value_claim": case["status"] == "proved",
        "exact_value_lower_half_cites_t007": case["status"] == "proved" and cites,
        "support": {
            "karakus_k2_minus_1": karakus_k2,
            "karakus_explicit_bound": karakus_explicit,
            "registered_verified": support_entry(verified, n, target),
            "registered_reported": support_entry(reported, n, target),
            "other_registered_results_at_n": others,
            "area_bound": area_entry,
            "chelokot_lean": chelokot_entry(n),
            "case_prose_published_proofs": prose_published_proofs(n),
        },
        "exposure_class": primary["class"],
        "exposure_reason": primary["reason"],
        "weakened_to": primary["weakened_to"],
        "exposure_class_without_karakus": without["class"],
        "exposure_reason_without_karakus": without["reason"],
        "weakened_to_without_karakus": without["weakened_to"],
    }


# ---------------------------------------------------------------------------------------
# The documents.
# ---------------------------------------------------------------------------------------

DOCUMENT_GROUPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("reader", ("README.md", "SYNOPSIS.md", "TUTORIAL.md")),
    ("frontier", ("packing/frontier/README.md",)),
    ("case-record", ("packing/frontier/n-*.md",)),
    (
        "register",
        (
            "packing/frontier/RESULTS.md",
            "packing/frontier/STATUS.md",
            "packing/frontier/INVENTORY.md",
            "packing/frontier/CERTIFICATE-REACH.md",
            "packing/frontier/results.yaml",
            "packing/frontier/evidence.yaml",
        ),
    ),
    ("research", ("docs/project/research/*.md",)),
    ("site-template", ("packing/devtools/templates/*.md", "packing/devtools/templates/*.html")),
    (
        "generator",
        ("packing/devtools/generate_frontier_case.py", "packing/devtools/render_overview.py"),
    ),
)
#: `s(k^2 - 2)`-style identities, in any variable the record uses for the side.
IDENTITY = re.compile(r"\b[kmnN]\s*(?:\^\s*2|²|\^\{2\})\s*[-−–]\s*2(?![0-9.a-zA-Z(])")
#: The closed form's distinctive `2 floor(sqrt N)` term, in each spelling the record uses.
CLOSED_FORM = re.compile(r"(?<![\w.-])2\s*\*?\s*(?:floor\s*\(|⌊|\\lfloor)|min\s*\(\s*ceil")
#: The author named as a person; identifiers such as `E-nagamochi-lower` are lowercase.
NAMES = re.compile(r"\bNagamochi\b")
#: Beside his name, words that state a theorem or a proof: the line `states` it.
STATES = re.compile(
    r"(?i)\b(?:prov(?:ed|es|en|ing)|establish\w*|theorem|identit(?:y|ies)|famil(?:y|ies)"
    r"|verified|exact values?)\b"
)
#: Beside his name, words that use his bound as a standing floor: the line `relies` on it.
RELIES = re.compile(
    r"(?i)\b(?:bound\w*|floor\w*|closed[ -]form|formula|governed|default|tight)\b"
)
#: A table cell holding only his name, as in a column of lower-bound sources.
CELL = re.compile(r"^\s*(?:Hiroshi\s+)?Nagamochi\s*$")
#: A paragraph naming Karakuş's finding already qualifies what it says. Generic caveat words
#: ("incomplete", "unproven") are not enough: in this record they are about other claims.
QUALIFIED = re.compile(
    r"(?i)karaku|scoring (?:lemma|assertion)|nagamochi[’']s lemma 1\b|lemma 1 of nagamochi"
)
#: How far either side of his name a cue word may sit and still be about him.
WINDOW = 80
EXCERPT = 160
TIERS = ("states", "relies", "mentions")


def paragraphs(lines: Sequence[str]) -> list[int]:
    """A paragraph index per line: blank lines separate, and each table row stands alone."""
    index, current, previous_blank = [], 0, True
    for line in lines:
        blank = not line.strip()
        row = line.lstrip().startswith("|")
        if blank or row or previous_blank:
            current += 1
        index.append(current)
        previous_blank = blank or row
    return index


def tier(line: str, kinds: Sequence[str], before: str = "", after: str = "") -> tuple[str, str]:
    """`states`, `relies` or `mentions`, and the phrase that decided it.

    The line is judged as a whole or, in a table, cell by cell. Cue words count only within
    `WINDOW` characters of his name -- reaching into the neighbouring lines of the same
    paragraph, since prose wraps -- and in a table only inside the cell naming him, so a
    lineage credit ("after Stromquist, Nagamochi, Burns") in a row whose kind column says
    "lower bound" stays a mention. The identity and the closed form state the theorem
    wherever they appear.
    """
    for kind, pattern in (("k2-minus-2-identity", IDENTITY), ("closed-form", CLOSED_FORM)):
        if kind in kinds and (match := pattern.search(line)) is not None:
            return "states", f"{kind}: {' '.join(match.group(0).split())}"
    if line.lstrip().startswith("|"):
        cells = line.split("|")
        if any(CELL.match(cell) for cell in cells):
            return "relies", "lone table cell"
        contexts = [
            cell[max(0, match.start() - WINDOW) : match.end() + WINDOW]
            for cell in cells
            for match in NAMES.finditer(cell)
        ]
    else:
        joined, offset = f"{before} {line} {after}", len(before) + 1
        contexts = [
            joined[max(0, offset + match.start() - WINDOW) : offset + match.end() + WINDOW]
            for match in NAMES.finditer(line)
        ]
    for name, pattern in (("states", STATES), ("relies", RELIES)):
        for context in contexts:
            if (match := pattern.search(context)) is not None:
                return name, f"beside: {match.group(0).lower()}"
    return "mentions", "name only"


def scan_text(text: str, first_line: int = 1) -> list[dict[str, Any]]:
    """Every line that states the theorem or the identity, or names Nagamochi."""
    lines = text.split("\n")
    owner = paragraphs(lines)
    text_of: dict[int, list[str]] = {}
    for i, line in enumerate(lines):
        text_of.setdefault(owner[i], []).append(line)
    qualified_paragraphs = {
        paragraph for paragraph, block in text_of.items() if QUALIFIED.search(" ".join(block))
    }
    hits: list[dict[str, Any]] = []
    for i, line in enumerate(lines):
        kinds = [
            name
            for name, pattern in (
                ("k2-minus-2-identity", IDENTITY),
                ("closed-form", CLOSED_FORM),
                ("names-nagamochi", NAMES),
            )
            if pattern.search(line)
        ]
        if not kinds:
            continue
        before = lines[i - 1] if i and owner[i - 1] == owner[i] else ""
        after = lines[i + 1] if i + 1 < len(lines) and owner[i + 1] == owner[i] else ""
        decided, phrase = tier(line, kinds, before, after)
        hits.append(
            {
                "line": first_line + i,
                "kinds": kinds,
                "tier": decided,
                "phrase": phrase,
                "qualified": owner[i] in qualified_paragraphs,
                "excerpt": line.strip()[:EXCERPT],
            }
        )
    return hits


def document_paths() -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for group, patterns in DOCUMENT_GROUPS:
        for pattern in patterns:
            found.extend(
                (group, path.relative_to(REPO).as_posix())
                for path in sorted(REPO.glob(pattern))
            )
    return found


def scan_document(group: str, path: str) -> list[dict[str, Any]]:
    """The live hits in one document, with the line numbers `--report` prints."""
    text = (REPO / path).read_text(encoding="utf-8")
    first_line = 1
    if group == "case-record":
        # The front matter is data, inventoried per case above; only the prose is scanned.
        _, front, body = text.split("---\n", 2)
        first_line = 1 + front.count("\n") + 2
        text = body
    return scan_text(text, first_line)


def worklist() -> list[tuple[str, str, list[dict[str, Any]]]]:
    """Every scanned document with hits, as `(group, path, hits)`."""
    return [
        (group, path, hits)
        for group, path in document_paths()
        if (hits := scan_document(group, path))
    ]


def document_entry(group: str, path: str, hits: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """What the record keeps of one document: counts and phrases, never line numbers.

    A line number moves whenever anyone edits the document above it, which would make the
    retained inventory stale on every unrelated change; a count moves only when a statement
    is added, removed or re-tiered. `--report` prints the lines.
    """
    statements = {name: sum(hit["tier"] == name for hit in hits) for name in TIERS}
    statements |= {
        "unqualified_states": sum(
            hit["tier"] == "states" and not hit["qualified"] for hit in hits
        ),
        "qualified": sum(hit["qualified"] for hit in hits),
        "k2_minus_2_identity": sum("k2-minus-2-identity" in hit["kinds"] for hit in hits),
        "closed_form": sum("closed-form" in hit["kinds"] for hit in hits),
    }
    phrases = Counter(hit["phrase"] for hit in hits if hit["tier"] != "mentions")
    return {
        "path": path,
        "group": group,
        "statements": statements,
        "phrases": dict(sorted(phrases.items())),
    }


def site_data() -> dict[str, Any]:
    path = ROOT / "atlas/known-best/bound-citations.json"
    entries = json.loads(path.read_text(encoding="utf-8"))["citations"]["entries"]
    citing = [
        entry["n"]
        for entry in entries
        if (entry.get("lower") or {}).get("source_key") == "[Nagamochi 2005]"
    ]
    return {
        "path": path.relative_to(REPO).as_posix(),
        "role": "the workbench page's per-case bound citations",
        "lower_bounds_citing_nagamochi": len(citing),
        "n": ranges(citing),
    }


def documents() -> dict[str, Any]:
    files = [document_entry(group, path, hits) for group, path, hits in worklist()]
    return {
        "method": (
            "Lexical. A line is counted when it states a k^2 - 2 identity or Nagamochi's "
            "closed form, or names Nagamochi. It `states` the theorem when it carries the "
            "identity or the closed form, or names him beside a proof or theorem word; it "
            "`relies` on it when it names him beside a bound, floor or formula word, or as a "
            "lone table cell; otherwise it `mentions` him. Table rows are judged on the cells "
            "naming him. A line is `qualified` when its paragraph, or its table row, already "
            "names Karakuş's finding. Case-record front matter is excluded, since the "
            "per-case rows inventory it. The record keeps counts and the deciding phrases "
            "per document and no line numbers, so an edit elsewhere in a document leaves it "
            "current; `--report` prints the lines."
        ),
        "groups": {group: list(patterns) for group, patterns in DOCUMENT_GROUPS},
        "patterns": {
            "k2-minus-2-identity": IDENTITY.pattern,
            "closed-form": CLOSED_FORM.pattern,
            "names-nagamochi": NAMES.pattern,
            "states": STATES.pattern,
            "relies": RELIES.pattern,
            "lone-cell": CELL.pattern,
            "qualified": QUALIFIED.pattern,
        },
        "files": files,
        "files_stating_without_qualification": {
            group: sum(
                entry["group"] == group and entry["statements"]["unqualified_states"] > 0
                for entry in files
            )
            for group, _ in DOCUMENT_GROUPS
        },
        "site_data": site_data(),
    }


# ---------------------------------------------------------------------------------------
# The document.
# ---------------------------------------------------------------------------------------


def ranges(values: Iterable[int]) -> str:
    """`4, 7-9, 14` for a sorted run of integers."""
    ordered = sorted(set(values))
    parts: list[str] = []
    start = previous = None
    for value in [*ordered, None]:
        if value is not None and previous is not None and value == previous + 1:
            previous = value
            continue
        if start is not None:
            parts.append(str(start) if start == previous else f"{start}-{previous}")
        start = previous = value
    return ", ".join(parts)


def summary(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    operative = [row for row in rows if row["operative_lower_bound"]["cites_t007"]]

    def tally(selected: Iterable[dict[str, Any]], key: str) -> dict[str, int]:
        counts = Counter(row[key] for row in selected)
        return {name: counts[name] for name in CLASSES}

    def by_class(selected: Sequence[dict[str, Any]], key: str) -> dict[str, list[int]]:
        return {name: [row["n"] for row in selected if row[key] == name] for name in CLASSES}

    exact_claims = [row for row in rows if row["exact_value_lower_half_cites_t007"]]
    weakened = [row for row in rows if row["exposure_class"] == WEAKENED]
    shortfalls = sorted(
        weakened,
        key=lambda row: (Decimal(row["weakened_to"]["shortfall_below_nagamochi"]), row["n"]),
    )
    open_rows = [row for row in rows if row["status"] == "open"]
    return {
        "cases": len(rows),
        "operative_cites_t007": {
            "all": len(operative),
            "open": sum(row["status"] == "open" for row in operative),
            "proved": sum(row["status"] == "proved" for row in operative),
            "outside_t007_registered_scope": sum(
                not row["operative_lower_bound"]["t007_scope_covers_n"] for row in operative
            ),
            "outside_t007_registered_scope_n": ranges(
                row["n"]
                for row in operative
                if not row["operative_lower_bound"]["t007_scope_covers_n"]
            ),
        },
        "open_cases": len(open_rows),
        "reported_lower_bounds_citing_t007": ranges(
            row["n"] for row in rows if row["reported_lower_bound"]["cites_t007"]
        ),
        "classes": tally(rows, "exposure_class"),
        "classes_open": tally(open_rows, "exposure_class"),
        "classes_without_karakus": tally(rows, "exposure_class_without_karakus"),
        "classes_open_without_karakus": tally(open_rows, "exposure_class_without_karakus"),
        "exposure_reasons": {
            name: dict(
                sorted(
                    Counter(
                        row["exposure_reason"] for row in rows if row["exposure_class"] == name
                    ).items()
                )
            )
            for name in CLASSES
        },
        "exact_value_claims_citing_t007": [row["n"] for row in exact_claims],
        "exact_value_claims_by_class": by_class(exact_claims, "exposure_class"),
        "exact_value_claims_by_class_without_karakus": by_class(
            exact_claims, "exposure_class_without_karakus"
        ),
        "exact_value_claims_on_t007_alone": [
            row["n"] for row in exact_claims if row["exposure_class"] in {WEAKENED, ONLY}
        ],
        "exact_value_claims_on_t007_alone_without_karakus": [
            row["n"]
            for row in exact_claims
            if row["exposure_class_without_karakus"] in {WEAKENED, ONLY}
        ],
        "weakened_shortfall": None
        if not shortfalls
        else {
            "smallest": {
                "n": shortfalls[0]["n"],
                "shortfall": shortfalls[0]["weakened_to"]["shortfall_below_nagamochi"],
            },
            "largest": {
                "n": shortfalls[-1]["n"],
                "shortfall": shortfalls[-1]["weakened_to"]["shortfall_below_nagamochi"],
            },
        },
    }


@cache
def build_document() -> dict[str, Any]:
    reg = register()
    last = max(reg.cases)
    verified = monotone_best(independent_sources("verified_lower_bound"), last)
    reported = monotone_best(independent_sources("reported_lower_bound"), last)
    rows = [case_row(n, verified[n], reported[n]) for n in range(1, last + 1)]
    t007 = reg.result(T007)
    record = reg.evidence[RECORD]
    return {
        "contract": "packing.squares:T007ConsumerAudit/v1",
        "generated_by": GENERATOR,
        "claim_status": "inventory-no-verdict",
        "question": (
            "Which register values and documents rest on T-007 (Nagamochi 2005, Theorem 2), "
            "and what independent support each has, after Karakuş 2026 showed the published "
            "proof of Nagamochi's Lemma 1 incomplete. This decides nothing about whether "
            "Nagamochi's bound is true."
        ),
        "classes": {
            UNAFFECTED: (
                "The operative bound does not cite E-nagamochi-lower, or the area bound or a "
                "registered verified independent bound (at this n or, by monotonicity, a "
                "smaller one) reaches Nagamochi's value."
            ),
            REPROVED: "n = k^2 - 1 and only Karakuş's Corollary 1.2 covers the value.",
            WEAKENED: (
                "Only a weaker nontrivial independent bound exists: Karakuş's (6.1) or a "
                "registered verified bound above the area bound; the stronger is given."
            ),
            ONLY: "Nothing independent beyond the area bound sqrt(n).",
        },
        "conventions": {
            "decimals": f"{PLACES} places, rounded toward negative infinity",
            "monotonicity": "s(n) >= s(m) for m <= n, by deleting squares",
            "reported_lane": (
                "Reported support is listed but never clears a case; a reported display "
                "decimal without an exact form is taken as printed."
            ),
        },
        "sources": {
            "t007": {
                "result": T007,
                "evidence": RECORD,
                "result_scope": t007["scope"],
                "evidence_scope": record["scope"],
                "verification": t007["verification"],
                "confirmation": t007["confirmation"],
                "archived": list(t007.get("artifacts") or ()),
            },
            "karakus": {
                **KARAKUS,
                **{key: pointer(KARAKUS_TEXT, needle) for key, needle in KARAKUS_AT.items()},
            },
            "chelokot": {
                **CHELOKOT,
                "reported_at": [pointer(path, needle) for path, needle in CHELOKOT_REPORTS],
            },
        },
        "scope": {"n_min": 1, "n_max": last, "cases": len(rows)},
        "summary": summary(rows),
        "rows": rows,
        "documents": documents(),
    }


def render(document: Mapping[str, Any]) -> str:
    return retained_json.dumps(document, sort_keys=True, ensure_ascii=False)


def report(document: Mapping[str, Any]) -> str:
    totals = document["summary"]
    operative = totals["operative_cites_t007"]
    lines = [
        (
            f"{document['scope']['cases']} case records; the operative verified lower bound "
            f"cites {RECORD} at {operative['all']} ({operative['open']} of "
            f"{totals['open_cases']} open, {operative['proved']} proved), "
            f"{operative['outside_t007_registered_scope']} of them outside {T007}'s registered "
            f"scope ({operative['outside_t007_registered_scope_n']})."
        ),
        "",
        "exposure class               with Karakuş   without   (open: with / without)",
    ]
    for name in CLASSES:
        with_k, without_k = totals["classes"][name], totals["classes_without_karakus"][name]
        open_with = totals["classes_open"][name]
        open_without = totals["classes_open_without_karakus"][name]
        lines.append(
            f"  {name:<27} {with_k:>8} {without_k:>9}   ({open_with} / {open_without})"
        )
    lines.extend(
        [
            "",
            "exact-value claims whose lower half cites the record: "
            + ranges(totals["exact_value_claims_citing_t007"]),
        ]
    )
    lines.extend(
        f"  {name}: {ranges(values) or '-'}"
        for name, values in totals["exact_value_claims_by_class"].items()
    )
    lines.extend(
        [
            "on T-007 alone, with Karakuş: "
            + (ranges(totals["exact_value_claims_on_t007_alone"]) or "-"),
            "on T-007 alone, without Karakuş: "
            + (ranges(totals["exact_value_claims_on_t007_alone_without_karakus"]) or "-"),
        ]
    )
    if totals["weakened_shortfall"] is not None:
        smallest, largest = (
            totals["weakened_shortfall"]["smallest"],
            totals["weakened_shortfall"]["largest"],
        )
        lines.append(
            "weakened-to shortfall below Nagamochi: "
            f"{smallest['shortfall']} (n={smallest['n']}) to "
            f"{largest['shortfall']} (n={largest['n']})"
        )
    # Line numbers live only here, from a fresh scan; the record keeps counts.
    stating = [
        (
            group,
            path,
            [hit["line"] for hit in hits if hit["tier"] == "states" and not hit["qualified"]],
        )
        for group, path, hits in worklist()
    ]
    stating = [item for item in stating if item[2]]
    lines.extend(
        ["", f"documents stating the theorem or an identity unqualified: {len(stating)}"]
    )
    lines.extend(
        f"  {path}: {len(numbers)} line(s): {ranges(numbers)}"
        for group, path, numbers in stating
        if group != "case-record"
    )
    cases = [path for group, path, _ in stating if group == "case-record"]
    lines.append(f"  case-record bodies: {len(cases)} files")
    return "\n".join(lines)


def shown(path: Path) -> str:
    return path.relative_to(REPO).as_posix() if path.is_relative_to(REPO) else str(path)


def check() -> int:
    try:
        expected = render(build_document())
    except ValueError as error:
        # A cited anchor that has gone -- (6.1)'s formula among them -- is a failed check,
        # said in one line rather than a traceback.
        print(f"T-007 consumer audit cannot be built: {error}")
        return 1
    if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != expected:
        print(
            f"{shown(OUTPUT)} is missing or stale; "
            "rerun python -m devtools.audit_t007_consumers --update"
        )
        return 1
    print(f"T-007 consumer audit current: {len(build_document()['rows'])} cases")
    return 0


def update() -> None:
    text = render(build_document())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(OUTPUT) as temporary:
        temporary.write_text(text, encoding="utf-8")
    print(f"wrote {shown(OUTPUT)}")


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true", help="rewrite the retained JSON")
    mode.add_argument("--check", action="store_true", help="fail when it is stale")
    mode.add_argument("--report", action="store_true", help="print the summary")
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.update:
        update()
        return 0
    if args.check:
        return check()
    print(report(build_document()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
