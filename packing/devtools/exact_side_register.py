#!/usr/bin/env python3
"""The exact-side register: each exact side fact the record stands behind, decided again.

Usage, from `packing/`, after `uv run --frozen --all-extras --group dev`::

    python -m devtools.exact_side_register            # the register as a table
    python -m devtools.exact_side_register --update   # write the register
    python -m devtools.exact_side_register --check    # rebuild, decide and compare

The register, `packing/frontier/exact-side-register.json`, lists one entry per exact
side fact: its count, its degree, the minimal polynomial written inline in
`exact_sides.polynomial_text` notation or held by a digest-pinned asset, an interval
about the side, who states it, and whether the fact is about the house or about a named
configuration. It is a view: case records keep what `adopt_houses` writes, and nothing
here writes a record, moves a bound or registers a result. The plan is
`docs/project/specs/active/plan-2026-10-25-exact-side-register.md` (bead think-vgsw,
tracker issue 811).

**Subjects.** An entry's `subject` is one of three:

- `house`: the case record's verified upper bound is this side, its `exact_form` written
  in main's notation, `root(p, low, high)` or a quadratic's closed form
  (`exact_sides.form`);
- `staged-house`: a validated side the house rule names as the house, its adoption
  staged in `select_houses.PENDING_ADOPTION` with the bead that owes it;
- `configuration`: the side of a named configuration that is not the house: a packing's
  limit side that no certificate decides at that side (T-246 at 29, T-244 at 172 and
  263, the catalogue's degree at 83), or a validated side above the house (T-193 at 204).

**Sources.** Slice 1 reads five:

- every case record whose house is written in main's notation (`read_form`), held to its
  reported lane's `algebraic_degree` and `minimal_polynomial`;
- T-193's sixteen counts, from the ledger `select_houses` reads (`T193_LEDGER`): a
  house where the record already holds the same side, a staged house where
  `PENDING_ADOPTION` names T-193, and otherwise a configuration;
- T-244's two, from the 25 October ledger, held to the polynomials its packet keeps;
- T-246, s(29)'s degree-7213 polynomial, by the archive `release.json` pins and the
  facts it measured, with the source's Krawczyk enclosure of the side;
- n = 83's degree-672 polynomial, by the Kingbird picture the 5 October pictures receipt
  pins and the facts `devtools.kingbird_root_polynomial` measured from it (`N83_RECEIPT`).

Houses written in older notations, such as n = 5's `2 + (1/2)sqrt(2)` and n = 11's
`root(P_trump11, ...)`, are not read yet; `--check` names them as the next slice's.

**Bases.** An interval's `basis`, and an entry's `irreducible`, say how far the record
checked the fact: `decided` (decided by every run of this module), `measured` (decided
once from the pinned asset, with a retained receipt) or `reported` (the source's claim).

**Deciding a side** (`decide`). Irreducibility over Q is decided by SymPy's
factorization over Z (`irreducible`), the route T-193's and T-244's reviews used; by
Gauss's lemma a primitive polynomial that is irreducible over Z is irreducible over Q.
Isolation is decided by Descartes' rule of signs on the interval's Moebius transform
(`variations`), in exact integer arithmetic, bisecting where a piece shows two or more
sign changes (`root_count`): one change is exactly one root. Measured on 25 October
2026, the 22 inline polynomials, of degree 2 to 41, decide in about a quarter of a
second; `exact_sides.algebraic`, which counts by Sturm sequences over Q, takes 14 s for
T-193's sixteen, 10 s of it at degree 41. Each `form` is the text `exact_sides.form`
writes, its interval cut at forty places and doubled where forty do not isolate the
side (`interval_text`), and the tests hold the two writers to the same text where
Sturm's route is cheap, to degree 24.

**The check** (`--check`) rebuilds the register from its inputs, deciding every inline
polynomial, and fails, naming each entry, where the committed file differs or where two
inputs that state one side disagree. A house that moves, as when think-ot5c adopts a
staged T-193 count, fails it until the adopting change runs `--update`.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import re
import sys
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from decimal import Context, Decimal
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

import sympy as sp
from gmpy2 import mpz
from strif import atomic_output_file

from devtools import exact_sides, select_houses
from devtools.check_results import scope_values
from devtools.exact_sides import Algebraic, Side
from sqpack import retained_json
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
FRONTIER = ROOT / "frontier"
REGISTER = FRONTIER / "exact-side-register.json"
REGISTER_PATH = REGISTER.relative_to(REPO).as_posix()
RESULTS = FRONTIER / "results.yaml"
CONTRACT = "packing.squares:ExactSideRegister/v1"
SCHEMA = "exact-side-register.schema.yaml"
GENERATOR = "python -m devtools.exact_side_register"
SPEC = "docs/project/specs/active/plan-2026-10-25-exact-side-register.md"
COUNTS = range(1, select_houses.HORIZON + 1)

#: The places a side's interval is cut at, doubled where they do not isolate it, as a
#: case record's `root(p, low, high)` is written.
PLACES = exact_sides.FORM_PLACES
#: How many times `root_count` halves a piece Descartes' rule leaves open before it says
#: the count is undecided: far past any separation the record's sides need.
MAX_SPLITS = 96

HOUSE, STAGED, CONFIGURATION = "house", "staged-house", "configuration"
SUBJECTS = (HOUSE, STAGED, CONFIGURATION)
DECIDED, MEASURED, REPORTED = "decided", "measured", "reported"
BASES = (DECIDED, MEASURED, REPORTED)
IS, BELOW, ABOVE, UNDECIDED = "is", "below", "above", "undecided"

T193, T244, T246 = "T-193", "T-244", "T-246"
#: T-193's sides, as the 16 October intake tabulated them and `select_houses` reads them.
T193_LEDGER = select_houses.EVAND_EXACT_SIDES
#: T-244's sides, decided offline by the 25 October intake, and the derived fact its
#: packet keeps of the polynomials the issue's attachment states.
T244_LEDGER = ROOT / "campaign/issue-intake/upper-bounds-issue804-20261025/exact-sides.json"
T244_FACT = ROOT / "resources/web/hyukdongkim-exact-forms-2026-10-25/facts/exact-forms.json"
#: T-246's packet: the release's custody record, which pins the archive and the
#: polynomial member by digest and records the facts measured from it, and the Krawczyk
#: box the archive holds, retained unpacked.
S29_PACKET = ROOT / "resources/web/evand-exact-data-2026-10-12"
S29_RELEASE = S29_PACKET / "acquisition/release.json"
S29_KRAWCZYK = S29_PACKET / "acquisition/release/s29/n29_krawczyk.json"
S29_ARCHIVE = "s29-minpoly.tar.zst"
#: The places the s(29) enclosure is written at, outward: its radius is about 1.07e-48.
S29_PLACES = 50
#: The Kingbird pictures receipt that pins n = 83's picture, and the receipt of the
#: polynomial `devtools.kingbird_root_polynomial` measured from it.
KINGBIRD_RECEIPTS = ROOT / "resources/web/known-best-packings/receipts"
PICTURES = KINGBIRD_RECEIPTS / "kingbird-2026-10-05-pictures.json"
N83_RECEIPT = KINGBIRD_RECEIPTS / "kingbird-n083-root-polynomial.json"
KINGBIRD_KEY = "[Kingbird]"

#: What each configuration is, by the result or source that states its side.
CONFIGURATIONS = {
    T193: (
        "The packing T-193's exact certificate describes, at its side; a smaller "
        "packing is the house"
    ),
    T244: (
        "The packing the house certifies, at the side the KKT closure of its active "
        "contacts fixes; no packing at that side is decided"
    ),
    T246: (
        "The packing the house certifies, at the side its contact system fixes; no "
        "packing at that side is decided"
    ),
    KINGBIRD_KEY: (
        "The catalogue's packing, which the house certifies at a rational side, at the "
        "side its contact system fixes, printed in the picture as Root[p, 27]; no "
        "packing at that side is decided"
    ),
}


class RegisterError(ValueError):
    """An input states a side the register cannot stand behind, or two inputs disagree."""


# --------------------------------------------------------------------------- deciding a side


def primitive(coefficients: Iterable[int | Fraction]) -> tuple[int, ...]:
    """Integer coefficients, highest degree first, coprime, the leading one positive."""
    values = [Fraction(value) for value in coefficients]
    while values and values[0] == 0:
        values.pop(0)
    if not values:
        raise RegisterError("the zero polynomial states no side")
    scale = math.lcm(*(value.denominator for value in values))
    integers = [int(value * scale) for value in values]
    content = math.gcd(*integers)
    integers = [value // content for value in integers]
    return tuple(-value for value in integers) if integers[0] < 0 else tuple(integers)


def evaluate(polynomial: Sequence[int], point: Fraction) -> int:
    """`b^d p(a/b)` at `point = a/b`: the polynomial's value times a positive integer."""
    numerator, denominator = point.numerator, point.denominator
    total, power = polynomial[0], 1
    for coefficient in polynomial[1:]:
        power *= denominator
        total = total * numerator + coefficient * power
    return total


def sign(polynomial: Sequence[int], point: Fraction) -> int:
    """The sign of the polynomial at a rational point, decided in integers."""
    found = evaluate(polynomial, point)
    return (found > 0) - (found < 0)


def variations(polynomial: Sequence[int], low: Fraction, high: Fraction) -> int:
    """The sign changes of `(1 + x)^d p((low + high x) / (1 + x))`, highest degree first.

    `x` in `(0, oo)` maps one to one and increasingly onto `(low, high)`, so the
    transformed polynomial's positive roots are `p`'s roots in the open interval, with
    their multiplicities. By Descartes' rule of signs they number at most these
    changes, with the same parity: none for none, exactly one for one.
    With `low = a/m` and `high = b/m`, the polynomial times `m^d` is
    `sum c_k (a + b x)^(d - k) (m (1 + x))^k`, built by Horner's rule in integers. The
    integers are GMP's (`gmpy2.mpz`): at n = 83's degree 672 Python's own took over ten
    minutes and GMP's about one.
    """
    scale = mpz(low.denominator * high.denominator)
    a = mpz(low.numerator * high.denominator)
    b = mpz(high.numerator * low.denominator)
    zero = mpz(0)
    built = [mpz(polynomial[0])]
    power = [mpz(1)]
    for coefficient in polynomial[1:]:
        grown = [zero] * (len(built) + 1)
        for index, term in enumerate(built):
            grown[index] += term * a
            grown[index + 1] += term * b
        widened = [zero] * (len(power) + 1)
        for index, term in enumerate(power):
            widened[index] += term * scale
            widened[index + 1] += term * scale
        power = widened
        if coefficient:
            factor = mpz(coefficient)
            for index, term in enumerate(power):
                grown[index] += factor * term
        built = grown
    signs = [term > 0 for term in built if term]
    return sum(left != right for left, right in itertools.pairwise(signs))


def root_count(
    polynomial: Sequence[int], low: Fraction, high: Fraction, splits: int = MAX_SPLITS
) -> int | None:
    """How many real roots the polynomial has in the open interval, with multiplicity:
    by Descartes' rule where it decides, bisecting a piece it leaves open (Vincent,
    Collins and Akritas); None where `splits` halvings leave a piece undecided."""
    found = variations(polynomial, low, high)
    if found <= 1:
        return found
    if splits == 0:
        return None
    middle = (low + high) / 2
    left = root_count(polynomial, low, middle, splits - 1)
    right = root_count(polynomial, middle, high, splits - 1)
    if left is None or right is None:
        return None
    return left + right + int(sign(polynomial, middle) == 0)


def isolates(polynomial: Sequence[int], low: Fraction, high: Fraction) -> bool:
    """Whether the polynomial has exactly one root in `(low, high)` and none at its ends."""
    return (
        low < high
        and sign(polynomial, low) != 0
        and sign(polynomial, high) != 0
        and root_count(polynomial, low, high) == 1
    )


_SYMBOL = sp.Symbol("s")


@cache
def irreducible(polynomial: tuple[int, ...]) -> bool:
    """Whether the primitive polynomial is irreducible over Q: SymPy factors it over Z
    into one factor of its own degree, of multiplicity one."""
    if len(polynomial) <= 2:
        return True
    _content, factors = sp.Poly(list(polynomial), _SYMBOL, domain=sp.ZZ).factor_list()
    return (
        len(factors) == 1
        and factors[0][1] == 1
        and factors[0][0].degree() == (len(polynomial) - 1)
    )


def decide(coefficients: Iterable[int | Fraction], interval: Sequence[Fraction]) -> Side:
    """The side a polynomial, highest degree first, states in an open interval, decided:
    the root of a polynomial of degree one, inside it, or the one root there of an
    irreducible polynomial of degree two or more."""
    polynomial = primitive(coefficients)
    low, high = (Fraction(end) for end in interval)
    text = exact_sides.polynomial_text(polynomial)
    if not low < high:
        raise RegisterError(f"{text}: an isolating interval must be nonempty")
    if len(polynomial) == 2:
        root = Fraction(-polynomial[1], polynomial[0])
        if not low < root < high:
            raise RegisterError(f"{text}: its root is not inside ({low}, {high})")
        return root
    if not irreducible(polynomial):
        raise RegisterError(f"{text}: reducible over Q, so not a minimal polynomial")
    if not isolates(polynomial, low, high):
        raise RegisterError(f"{text}: not exactly one root in ({low}, {high})")
    return Algebraic(polynomial, low, high)


def cut(number: Fraction, places: int, *, up: bool) -> str:
    """A rational cut down, or rounded up, at `places` decimals."""
    scaled = number * 10**places
    whole = -(-scaled.numerator // scaled.denominator) if up else math.floor(scaled)
    text = str(whole).rjust(places + 1, "0")
    return f"{text[:-places]}.{text[-places:]}"


def interval_text(side: Algebraic, places: int = PLACES) -> tuple[str, str]:
    """The side cut down and rounded up at `places` decimals, with more places wherever
    those do not isolate it: the ends `exact_sides.form` writes for a root form."""
    for _step in range(8):
        low, high = exact_sides.enclosure(side, Fraction(1, 10 ** (places + 2)))
        below, above = cut(low, places, up=False), cut(high, places, up=True)
        if isolates(side.polynomial, Fraction(below), Fraction(above)):
            return below, above
        places *= 2
    raise RegisterError(f"no decimal interval isolates {exact_sides.literal(side)}")


def form(side: Algebraic) -> str:
    """The side as a case record writes it: of degree two its closed form, otherwise
    `root(p, low, high)`, as `exact_sides.form` writes it."""
    if side.degree == 2:
        return exact_sides.quadratic_text(side)
    low, high = interval_text(side)
    return f"root({exact_sides.polynomial_text(side.polynomial)}, {low}, {high})"


_ROOT_FORM = re.compile(
    r"root\((?P<polynomial>[0-9s^{}+\- ]+),\s*(?P<low>[0-9]+\.[0-9]+),\s*"
    r"(?P<high>[0-9]+\.[0-9]+)\)"
)
_QUADRATIC = re.compile(r"\(-?[0-9]+[+-]([0-9]+\*)?sqrt\([0-9]+\)\)/[0-9]+")


def read_form(text: str) -> Algebraic | None:
    """The algebraic side an exact form in main's notation writes, decided here and held
    to the text the house writer writes for it; None for any other text, a fraction or a
    closed form in an older notation."""
    text = text.strip()
    match = _ROOT_FORM.fullmatch(text)
    if match is not None:
        side = decide(
            exact_sides.read_polynomial(match["polynomial"]),
            (Fraction(match["low"]), Fraction(match["high"])),
        )
    elif _QUADRATIC.fullmatch(text):
        held = exact_sides.read_form(text)
        if not isinstance(held, Algebraic):
            return None
        side = decide(held.polynomial, (held.low, held.high))
    else:
        return None
    if not isinstance(side, Algebraic):
        raise RegisterError(f"{text!r} states a rational side, which is written as a fraction")
    if form(side) != text:
        raise RegisterError(
            f"{text!r} is not written as the house writer writes it: {form(side)!r}"
        )
    return side


def exact(text: object) -> Side | None:
    """A case record's exact form held exactly: a fraction, a side in main's notation, or
    None for a text no reader here holds."""
    if text is None:
        return None
    try:
        return Fraction(str(text).strip())
    except ValueError:
        return read_form(str(text))


def scientific(number: Fraction) -> str:
    """A positive rational to four figures in scientific notation, `9.882e-20`."""
    quotient = Context(prec=12).divide(Decimal(number.numerator), Decimal(number.denominator))
    return f"{quotient:.3e}"


def gap(first: Side, second: Side) -> str:
    """The distance between two different sides, for reading, to four figures: from
    rational bounds on it narrowed until they agree to a millionth of it."""
    high, low = (first, second) if exact_sides.compare(first, second) > 0 else (second, first)
    places = 60
    for _step in range(8):
        width = Fraction(1, 10**places)
        above, below = exact_sides.enclosure(high, width), exact_sides.enclosure(low, width)
        least, most = above[0] - below[1], above[1] - below[0]
        if least > 0 and (most - least) * 10**6 <= least:
            return scientific((least + most) / 2)
        places *= 2
    raise RegisterError("two different sides did not separate to four figures")


def relation(side: Side, house: Side) -> str:
    return {-1: BELOW, 0: IS, 1: ABOVE}[exact_sides.compare(side, house)]


# --------------------------------------------------------------------------- the inputs


@dataclass(frozen=True)
class Case:
    """What a case record says of its upper bounds."""

    n: int
    verified: Mapping[str, Any]
    reported: Mapping[str, Any]

    @property
    def house_form(self) -> str | None:
        form_text = self.verified.get("exact_form")
        return None if form_text is None else str(form_text)


@dataclass(frozen=True)
class Record:
    """The register's inputs from the record: results by id and the case records."""

    results: Mapping[str, Mapping[str, Any]]
    cases: Mapping[int, Case]

    def result(self, identifier: str) -> Mapping[str, Any]:
        found = self.results.get(identifier)
        if found is None:
            raise RegisterError(f"{identifier} is not in {RESULTS.relative_to(REPO)}")
        return found

    def holders(self, n: int) -> list[str]:
        """The results the case's verified upper bound rests on: those in scope at the
        count that carry its evidence."""
        cited = {str(item) for item in self.cases[n].verified.get("evidence") or []}
        return [
            identifier
            for identifier, entry in self.results.items()
            if n in scope_values(dict(entry["scope"]))
            and cited & set(entry.get("evidence") or [])
        ]

    def house_side(self, n: int) -> Side:
        side = exact(self.cases[n].house_form)
        if side is None:
            raise RegisterError(f"n={n}: the house's exact form is not one this module reads")
        return side


def frontmatter(path: Path) -> Mapping[str, Any]:
    return safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])["packing"]


def load_record() -> Record:
    register = safe_load(RESULTS.read_text(encoding="utf-8"))
    cases = {}
    for n in COUNTS:
        packing = frontmatter(select_houses.case_path(n))
        cases[n] = Case(n, packing["verified_upper_bound"], packing["reported_upper_bound"])
    return Record(
        results={str(entry["id"]): entry for entry in register["results"]}, cases=cases
    )


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def repository_path(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


# --------------------------------------------------------------------------- entries


def stated_by(
    record: Record, results: Sequence[str], source_key: str | None, evidence: Sequence[str]
) -> dict[str, Any]:
    return {
        "results": [
            {
                "id": identifier,
                "kind": str(record.result(identifier)["kind"]),
                "rungs": (
                    f"{record.result(identifier)['verification']}/"
                    f"{record.result(identifier)['confirmation']}"
                ),
            }
            for identifier in results
        ],
        "source_key": source_key,
        "evidence": [str(item) for item in evidence],
    }


def result_source(record: Record, identifier: str) -> tuple[str | None, list[str]]:
    entry = record.result(identifier)
    keys = (entry.get("attribution") or {}).get("source_keys") or []
    return (str(keys[0]) if keys else None), [str(item) for item in entry["evidence"]]


def inline(side: Algebraic) -> dict[str, Any]:
    """The fields of a side this module decides: degree, polynomial, form and interval."""
    low, high = interval_text(side)
    return {
        "degree": side.degree,
        "polynomial": exact_sides.polynomial_text(side.polynomial),
        "reference": None,
        "measured": None,
        "form": form(side),
        "interval": {"low": low, "high": high, "basis": DECIDED},
        "irreducible": DECIDED,
    }


def house_relation(
    record: Record, n: int, side: Side | None, *, basis: str = DECIDED
) -> dict[str, Any]:
    house = record.house_side(n)
    if side is None:
        return {
            "results": record.holders(n),
            "relation": UNDECIDED,
            "gap": None,
            "basis": basis,
        }
    found = relation(side, house)
    return {
        "results": record.holders(n),
        "relation": found,
        "gap": None if found == IS else gap(side, house),
        "basis": basis,
    }


def entry(
    n: int,
    subject: str,
    stated: Mapping[str, Any],
    facts: Mapping[str, Any],
    house: Mapping[str, Any],
    *,
    configuration: str | None = None,
    staged: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    return {
        "n": n,
        "subject": subject,
        "configuration": configuration,
        "stated_by": dict(stated),
        **facts,
        "house": dict(house),
        "staged": None if staged is None else dict(staged),
    }


def house_entries(record: Record) -> tuple[list[dict[str, Any]], list[int]]:
    """Every house written in main's notation, held to its reported lane; and the counts
    whose house's exact form no reader here holds, the older notations, not read yet."""
    entries: list[dict[str, Any]] = []
    older: list[int] = []
    for n, case in record.cases.items():
        text = case.house_form
        side = exact(text)
        if side is None:
            if text is not None:
                older.append(n)
            continue
        if not isinstance(side, Algebraic):
            continue
        reported = case.reported
        same = str(reported.get("exact_form") or "").strip() == str(text).strip()
        degree, written = reported.get("algebraic_degree"), reported.get("minimal_polynomial")
        if same and (
            degree != side.degree
            or written is None
            or exact_sides.read_polynomial(str(written)) != side.polynomial
        ):
            raise RegisterError(
                f"n={n}: the reported lane's algebraic_degree {degree} and minimal_polynomial "
                f"{written!r} are not the house's side"
            )
        holders = record.holders(n)
        stated = stated_by(
            record,
            holders,
            str(reported["source_key"]) if same else None,
            [str(item) for item in case.verified["evidence"]],
        )
        relation_to_house = {"results": holders, "relation": IS, "gap": None, "basis": DECIDED}
        entries.append(entry(n, HOUSE, stated, inline(side), relation_to_house))
    return entries, older


@cache
def t193_rows() -> dict[int, Mapping[str, Any]]:
    return {int(row["n"]): row for row in read_json(T193_LEDGER)["rows"]}


def t193_side(n: int) -> Side:
    """T-193's side at `n`, as the ledger tabulates it, inside the source's interval."""
    row = t193_rows().get(n)
    if row is None:
        raise RegisterError(f"n={n}: T-193's ledger states no side")
    low, high = (Fraction(str(end)) for end in row["interval"])
    source_low, source_high = (Fraction(str(end)) for end in row["source_interval"])
    if not source_low <= low < high <= source_high:
        raise RegisterError(f"n={n}: T-193's tabulated interval is not inside the source's")
    coefficients = [int(str(term)) for term in reversed(row["polynomial_low_to_high"])]
    return decide(coefficients, (low, high))


def t193_entries(
    record: Record, houses: Mapping[int, Mapping[str, Any]]
) -> list[dict[str, Any]]:
    """T-193's counts: a house the record holds already is held to the ledger's side; a
    count `PENDING_ADOPTION` stages for T-193 is a staged house; any other is a
    configuration, ordered against the house."""
    entries: list[dict[str, Any]] = []
    source_key, evidence = result_source(record, T193)
    stated = stated_by(record, [T193], source_key, evidence)
    for n in sorted(scope_values(dict(record.result(T193)["scope"]))):
        side = t193_side(n)
        if not isinstance(side, Algebraic):
            raise RegisterError(f"n={n}: T-193's side is rational")
        if n in houses:
            if T193 not in houses[n]["house"]["results"] or (
                exact_sides.compare(side, record.house_side(n)) != 0
            ):
                raise RegisterError(f"n={n}: the house is not T-193's side")
            continue
        pending = select_houses.PENDING_ADOPTION.get(n)
        if pending is not None and pending.house == T193:
            facts = house_relation(record, n, side)
            if facts["relation"] != BELOW:
                raise RegisterError(f"n={n}: a staged house is not below the case's house")
            staged = {"bead": pending.bead, "why": pending.why}
            entries.append(entry(n, STAGED, stated, inline(side), facts, staged=staged))
            continue
        entries.append(
            entry(
                n,
                CONFIGURATION,
                stated,
                inline(side),
                house_relation(record, n, side),
                configuration=CONFIGURATIONS[T193],
            )
        )
    return entries


def t244_entries(record: Record) -> list[dict[str, Any]]:
    """T-244's sides, each held to the polynomial its packet keeps and decided in the
    ledger's interval: configurations of the packing the house certifies."""
    rows = {int(row["n"]): row for row in read_json(T244_LEDGER)["rows"]}
    kept = {int(item["n"]): item for item in read_json(T244_FACT)["forms"]}
    source_key, evidence = result_source(record, T244)
    stated = stated_by(record, [T244], source_key, evidence)
    entries = []
    for n in sorted(scope_values(dict(record.result(T244)["scope"]))):
        row, fact = rows.get(n), kept.get(n)
        if row is None or fact is None:
            raise RegisterError(f"n={n}: T-244's ledger or packet states no side")
        coefficients = [int(str(term)) for term in row["polynomial_high_to_low"]]
        if coefficients != [int(str(term)) for term in fact["polynomial_high_to_low"]]:
            raise RegisterError(f"n={n}: T-244's ledger and packet state different polynomials")
        low, high = (Fraction(str(end)) for end in row["interval"])
        side = decide(coefficients, (low, high))
        if not isinstance(side, Algebraic):
            raise RegisterError(f"n={n}: T-244's side is rational")
        if str(row["form"]) != form(side):
            raise RegisterError(
                f"n={n}: T-244's ledger writes {row['form']!r}, not {form(side)!r}"
            )
        entries.append(
            entry(
                n,
                CONFIGURATION,
                stated,
                inline(side),
                house_relation(record, n, side),
                configuration=CONFIGURATIONS[T244],
            )
        )
    return entries


def s29_entry(record: Record) -> dict[str, Any]:
    """T-246: s(29)'s side by the archive `release.json` pins and the facts it measured,
    with the source's Krawczyk enclosure of the side, written outward."""
    release = read_json(S29_RELEASE)
    asset = next(item for item in release["assets"] if item["name"] == S29_ARCHIVE)
    polynomial = release["s29_archive"]["polynomial"]
    metadata = polynomial["source_metadata"]
    degree = int(polynomial["degree"])
    if not (
        degree == int(polynomial["coefficient_count"]) - 1 == int(metadata["degree"])
        and int(polynomial["leading_coefficient_sign"]) == 1
        and metadata["irreducible_by_patterns"] is True
    ):
        raise RegisterError("n=29: release.json's measured polynomial is not one of its degree")
    box = read_json(S29_KRAWCZYK)
    if box["certified"] is not True:
        raise RegisterError("n=29: the Krawczyk box is not certified")
    middle, radius = Fraction(str(box["S_mid"])), Fraction(repr(float(box["S_rad"])))
    low = cut(middle - radius, S29_PLACES, up=False)
    high = cut(middle + radius, S29_PLACES, up=True)
    house = record.house_side(29)
    if not Fraction(low) < house < Fraction(high):
        raise RegisterError("n=29: the house is outside the source's enclosure; order it")
    source_key, evidence = result_source(record, T246)
    facts = {
        "degree": degree,
        "polynomial": None,
        "reference": {
            "asset": str(asset["url"]),
            "sha256": str(asset["sha256"]),
            "bytes": int(asset["bytes"]),
            "member": str(polynomial["member"]),
            "member_sha256": str(polynomial["sha256"]),
            "member_bytes": int(polynomial["bytes"]),
            "pinned_in": repository_path(S29_RELEASE),
        },
        "measured": {
            "coefficients": int(polynomial["coefficient_count"]),
            "leading_digits": int(polynomial["leading_coefficient_digits"]),
            "height_digits": int(polynomial["height_digits"]),
            "constant_digits": int(polynomial["constant_term_digits"]),
            "root_index": None,
            "receipt": repository_path(S29_RELEASE),
        },
        "form": None,
        "interval": {"low": low, "high": high, "basis": REPORTED},
        "irreducible": REPORTED,
    }
    return entry(
        29,
        CONFIGURATION,
        stated_by(record, [T246], source_key, evidence),
        facts,
        house_relation(record, 29, None, basis=REPORTED),
        configuration=CONFIGURATIONS[T246],
    )


def pinned_picture(n: int) -> Mapping[str, Any]:
    """The pictures receipt's reading of count `n`'s Kingbird picture."""
    readings = read_json(PICTURES)["readings"]
    found = [reading for reading in readings if int(reading["n"]) == n]
    if len(found) != 1:
        raise RegisterError(f"n={n}: the pictures receipt does not pin one picture")
    return found[0]


def n83_entry(record: Record) -> dict[str, Any]:
    """n = 83's degree-672 polynomial: the catalogue's statement, held by the picture the
    pictures receipt pins and the facts measured from it, its root isolated there."""
    picture = pinned_picture(83)
    receipt = read_json(N83_RECEIPT)
    measured = receipt["polynomial"]
    root = receipt["root"]
    reported = record.cases[83].reported
    degree = int(measured["degree"])
    if not (
        int(receipt["n"]) == 83
        and receipt["pinned_in"] == repository_path(PICTURES)
        and receipt["url"] == picture["url"]
        and int(receipt["bytes"]) == int(picture["bytes"])
    ):
        raise RegisterError("n=83: the receipt does not measure the pinned picture")
    if degree != reported.get("algebraic_degree") or reported.get("source_key") != KINGBIRD_KEY:
        raise RegisterError("n=83: the measured degree is not the catalogue's, as recorded")
    if not (measured["primitive"] is True and int(root["roots"]) == 1):
        raise RegisterError("n=83: the receipt does not isolate one root of a primitive p")
    low, high = Fraction(str(root["low"])), Fraction(str(root["high"]))
    house = record.house_side(83)
    found = BELOW if high < house else ABOVE if house < low else UNDECIDED
    facts = {
        "degree": degree,
        "polynomial": None,
        "reference": {
            "asset": str(picture["url"]),
            "sha256": str(picture["sha256"]),
            "bytes": int(picture["bytes"]),
            "member": None,
            "member_sha256": None,
            "member_bytes": None,
            "pinned_in": repository_path(PICTURES),
        },
        "measured": {
            "coefficients": int(measured["coefficients"]),
            "leading_digits": int(measured["leading_digits"]),
            "height_digits": int(measured["height_digits"]),
            "constant_digits": int(measured["constant_digits"]),
            "root_index": int(root["index"]),
            "receipt": repository_path(N83_RECEIPT),
        },
        "form": None,
        "interval": {"low": str(root["low"]), "high": str(root["high"]), "basis": MEASURED},
        "irreducible": REPORTED,
    }
    near = high if found == BELOW else low
    house_facts = {
        "results": record.holders(83),
        "relation": found,
        "gap": None if found == UNDECIDED else gap(house, near),
        "basis": MEASURED,
    }
    return entry(
        83,
        CONFIGURATION,
        stated_by(record, [], KINGBIRD_KEY, [str(item) for item in reported["evidence"]]),
        facts,
        house_facts,
        configuration=CONFIGURATIONS[KINGBIRD_KEY],
    )


# --------------------------------------------------------------------------- the register


@dataclass(frozen=True)
class Built:
    """The register as the inputs give it, and what it leaves for later slices."""

    document: dict[str, Any]
    older_houses: tuple[int, ...]
    other_staged: tuple[int, ...]


def entries_from(record: Record) -> tuple[list[dict[str, Any]], list[int]]:
    houses, older = house_entries(record)
    by_count = {item["n"]: item for item in houses}
    rows = [
        *houses,
        *t193_entries(record, by_count),
        *t244_entries(record),
        s29_entry(record),
        n83_entry(record),
    ]
    rows.sort(key=lambda item: (item["n"], SUBJECTS.index(item["subject"])))
    return rows, older


def totals(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    subjects = Counter(str(row["subject"]) for row in rows)
    bases = Counter(str(row["interval"]["basis"]) for row in rows)
    return {
        "entries": len(rows),
        "counts": len({row["n"] for row in rows}),
        "subjects": {subject: subjects[subject] for subject in SUBJECTS},
        "intervals": {basis: bases[basis] for basis in BASES},
        "largest_decided_degree": max(
            (int(row["degree"]) for row in rows if row["interval"]["basis"] == DECIDED),
            default=0,
        ),
    }


def document(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "softschema": {"contract": CONTRACT, "schema": SCHEMA, "status": "enforced"},
        "contract": CONTRACT,
        "generated_by": f"{GENERATOR} --update",
        "spec": SPEC,
        "totals": totals(rows),
        "entries": list(rows),
    }


def build(record: Record | None = None) -> Built:
    record = load_record() if record is None else record
    rows, older = entries_from(record)
    staged = tuple(
        sorted(
            n for n, pending in select_houses.PENDING_ADOPTION.items() if pending.house != T193
        )
    )
    return Built(document(rows), tuple(older), staged)


def text(register: Mapping[str, Any]) -> str:
    return retained_json.dumps(register, ensure_ascii=False) + "\n"


def differences(found: Mapping[str, Any], expected: Mapping[str, Any]) -> list[str]:
    """Where a register differs from the one the inputs give: each entry that differs, is
    missing or is extra, by count and subject, then each other field."""

    def key(item: Mapping[str, Any]) -> tuple[object, object]:
        return item.get("n"), item.get("subject")

    held: dict[tuple[object, object], Any] = {}
    problems: list[str] = []
    for item in found.get("entries") or []:
        if not isinstance(item, Mapping):
            problems.append(f"an entry is not an object: {item!r}")
            continue
        if key(item) in held:
            problems.append(f"n={item.get('n')} {item.get('subject')}: two entries")
        held[key(item)] = item
    for item in expected["entries"]:
        kept = held.pop(key(item), None)
        label = f"n={item['n']} {item['subject']}"
        if kept is None:
            problems.append(f"{label}: the register has no entry")
            continue
        for field_name, wanted in item.items():
            if kept.get(field_name) != wanted:
                problems.append(
                    f"{label}: {field_name} is {json.dumps(kept.get(field_name))}, "
                    f"the inputs give {json.dumps(wanted)}"
                )
        problems.extend(
            f"{label}: a field {name!r} the inputs do not give"
            for name in kept
            if name not in item
        )
    problems.extend(f"n={n} {subject}: an entry the inputs do not give" for n, subject in held)
    problems.extend(
        f"the register's {name} is not the inputs'"
        for name in expected
        if name != "entries" and found.get(name) != expected[name]
    )
    problems.extend(
        f"the register has a field {name!r}" for name in found if name not in expected
    )
    return problems


def summary(built: Built) -> str:
    counted = built.document["totals"]
    subjects = ", ".join(f"{count} {name}" for name, count in counted["subjects"].items())
    bases = ", ".join(f"{count} {name}" for name, count in counted["intervals"].items())
    return (
        f"{counted['entries']} entries at {counted['counts']} counts ({subjects}); "
        f"intervals {bases}; inline polynomials decided to degree "
        f"{counted['largest_decided_degree']}"
    )


def later(built: Built) -> list[str]:
    """What the register leaves to its later slices, said on every run."""
    notes = []
    if built.older_houses:
        listed = ", ".join(str(n) for n in built.older_houses)
        notes.append(f"houses in an older notation, not read yet (slice 2): {listed}")
    if built.other_staged:
        listed = ", ".join(str(n) for n in built.other_staged)
        notes.append(
            f"staged houses of other results, which this slice does not read: {listed}"
        )
    return notes


def update() -> int:
    built = build()
    content = text(built.document)
    if not REGISTER.is_file() or REGISTER.read_text(encoding="utf-8") != content:
        with atomic_output_file(REGISTER) as temporary:
            temporary.write_text(content, encoding="utf-8")
    print(f"exact-side register updated: {summary(built)}")
    for note in later(built):
        print(f"  {note}")
    return 0


def check(register: Path = REGISTER, record: Record | None = None) -> int:
    """Rebuild the register from its inputs, deciding every inline side, and compare."""
    if not register.is_file():
        print(f"{REGISTER_PATH} is missing; run `{GENERATOR} --update`")
        return 1
    try:
        built = build(record)
    except RegisterError as error:
        print(f"exact-side register: {error}")
        return 1
    content = register.read_text(encoding="utf-8")
    problems = differences(json.loads(content), built.document)
    if not problems and content != text(built.document):
        problems.append(f"the register is not laid out as `{GENERATOR} --update` writes it")
    for problem in problems:
        print(f"exact-side register: {problem}")
    if problems:
        print(f"{REGISTER_PATH} is stale; run `{GENERATOR} --update`")
        return 1
    print(f"exact-side register check passed: {summary(built)}")
    for note in later(built):
        print(f"  {note}")
    return 0


def table(built: Built) -> str:
    lines = [
        (
            f"{'n':>4}  {'subject':<13} {'stated by':<10} {'degree':>6}  {'interval':<9} "
            f"{'house':<10} gap"
        )
    ]
    for row in built.document["entries"]:
        stated = ", ".join(item["id"] for item in row["stated_by"]["results"]) or str(
            row["stated_by"]["source_key"]
        )
        house = row["house"]
        lines.append(
            f"{row['n']:>4}  {row['subject']:<13} {stated:<10} {row['degree']:>6}  "
            f"{row['interval']['basis']:<9} {house['relation']:<10} {house['gap'] or ''}"
        )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--update", action="store_true", help=f"write {REGISTER_PATH}")
    mode.add_argument(
        "--check",
        action="store_true",
        help="rebuild and decide every entry; exit 1, naming each entry, where it differs",
    )
    args = parser.parse_args(argv)
    if args.update:
        return update()
    if args.check:
        return check()
    built = build()
    print(table(built))
    print(summary(built))
    for note in later(built):
        print(f"  {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
