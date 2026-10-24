"""Göbel's classical construction at every count, each side proved final by the area bound.

Göbel's side at a count m is the least side of any member of the three closed-form
families the Kingbird catalogue states, archived in this repository, at a count n >= m (a
packing of n squares, less n - m of them, packs m):

- **Göbel squares** ([Kingbird-Göbel-squares], ``packing/resources/web/
  kingbird-squares-in-squares-gobel-squares.md``): for positive integers a, b with
  a - 1 < b sqrt(2)/2 < a + 1, n = 2(a + 1)a + b^2 at side a + 1 + (b/2) sqrt(2);
- **Göbel strips** ([Kingbird-Göbel-strips], ``kingbird-squares-in-squares-gobel-strips.md``):
  for a positive integer a and b = 1 + floor((a - 1) sqrt(2)), n = (a + 1)a + 2 + b at
  side a + 1 + sqrt(2)/2;
- **the strip touching the two corner squares**, which the same page states "starting at
  s(18)": n = (a + 1)a + 3 + b at side 2 + (b + 1) sqrt(2)/2, the same b, for n >= 18.

The families generalize Frits Göbel's constructions ([Göbel 1979]), as the pages say.
Nothing here verifies a construction again: the catalogue states them, and the record
trusts that statement (think-llit's plan, Non-Goals). What this module adds is reach.

**Every member to a build limit.** `families` builds every member whose count is at most
the limit, with loop bounds derived from it rather than fixed: a square packs
n = 2(a + 1)a + b^2 > 2a^2 and > b^2, and a strip n > a^2, so no member at or below the
limit has a or b above its integer square root. Within each a, the squares' b are exactly
those with 2(a - 1)^2 < b^2 < 2(a + 1)^2.

**Every side proved final.** `table` takes Göbel's side at every count up to the limit in
one descending pass: the least member at that count or above. A member at count k packs k
unit squares, so its side is at least sqrt(k). The least side S at m among the members to
the limit B is therefore final once S^2 < B + 1: every member above B has a side of at
least sqrt(B + 1). The test is exact, p^2 + 2q^2 + 2pq sqrt(2) < B + 1 for
S = p + q sqrt(2) (`final`). `side` builds to `BUILD`, then to twice that while the count
is not proved, and refuses a count no build to `MAX_BUILD` proves (`GoebelError`), so the
reach follows the counts asked for. `reach` is the last count a build proves together with
every count below it beyond the corpus: 10,345 for `BUILD`, so the build every reader
starts from decides every count any report has reached (#732's largest is 9913).

**The retained program.** ``packing/resources/web/couzo-verified-bounds-2026-10-14/review/
goebel_beyond_horizon.py`` is the record of 15 October, the regression oracle, and the
source of every frozen receipt, which names it in its ``program`` field: this module
neither imports nor runs it. Its loops stop at a < 40 and b < 80, so raised past its limit
of 1100 they build no strip above 1617 and give a side that is too large at 1,573 counts
from 1682 to 6116, and none above 6256; to 1100 its largest member packs 1073, the reach
the record held until this module (`tests/test_goebel_construction.py` holds both, and
this module's agreement with it at every count to 1073).

Every side is held exactly as p + q sqrt(2) with p, q rational, and a rational side s is
compared with it by an exact sign (`sign`), squaring only where both sides of the
comparison are non-negative; floor((a - 1) sqrt(2)) is ``math.isqrt(2 (a - 1)^2)``.
"""

from __future__ import annotations

import functools
import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

#: The corpus is ``n = 1..324``; every reader asks for counts beyond it.
HORIZON = 324
#: The build every reading starts from: it proves every count from 325 to 10,345 (`reach`).
BUILD = 10_500
#: The largest build `side` makes before it refuses a count it cannot prove final.
MAX_BUILD = 1_000_000
SQUARE = "Göbel square"
STRIP = "Göbel strip"
CORNER = "corner-touching Göbel strip"
#: The count the corner-touching strips start at, as the catalogue states them.
CORNER_FROM = 18
#: What a comparison receipt says the families are, as the frozen receipts say it.
FAMILIES = "Göbel squares, Göbel strips and corner-touching strips, with deletion"
FORMULAS = (
    "Göbel square: n = 2(a+1)a + b^2, s = a + 1 + (b/2) sqrt 2, a - 1 < b sqrt(2)/2 < a + 1",
    "Göbel strip: n = (a+1)a + 2 + b, s = a + 1 + sqrt(2)/2, b = 1 + floor((a-1) sqrt 2)",
    "corner-touching strip: n = (a+1)a + 3 + b, s = 2 + (b+1) sqrt(2)/2, same b, n >= 18",
)
_HALF = Fraction(1, 2)
#: The relations a comparison names, by the sign of the side less the construction.
RELATIONS = ("above", "equal", "below")


class GoebelError(ValueError):
    """Refuse a count whose side no build proves final, or a build that is not one."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise GoebelError(message)


@dataclass(frozen=True, slots=True)
class Form:
    """A side p + q sqrt(2), the family that gives it, and the count it packs."""

    p: Fraction
    q: Fraction
    family: str
    count: int

    def text(self) -> str:
        """The side as the record writes it, ``p + q*sqrt(2)``."""
        return f"{self.p} + {self.q}*sqrt(2)"

    def margin(self, side: Fraction) -> float:
        """side - (p + q sqrt 2), with sqrt 2 to 60 places, then rounded to a float."""
        root = Fraction(math.isqrt(2 * 10**120), 10**60)
        return float(side - self.p - self.q * root)


def _sign(a: Fraction, b: Fraction) -> int:
    """The sign of a + b sqrt(2), exactly."""
    if a >= 0 and b >= 0:
        return 0 if a == b == 0 else 1
    if a <= 0 and b <= 0:
        return -1
    lhs, rhs = a * a, 2 * b * b
    return (1 if a > 0 else -1) if lhs > rhs else (1 if b > 0 else -1)


def sign(side: Fraction, form: Form) -> int:
    """The sign of side - (p + q sqrt 2), exactly: 1 above, 0 equal, -1 below."""
    return _sign(side - form.p, -form.q)


def less(x: Form, y: Form) -> bool:
    """Whether x's side is strictly below y's, exactly."""
    return _sign(y.p - x.p, y.q - x.q) > 0


def families(limit: int) -> list[Form]:
    """Every member of the three families whose count is at most ``limit``, a outer and b
    inner as the retained program orders them; the bounds on a and b follow from the limit
    (the module docstring)."""
    _require(limit >= 1, f"a build to {limit} holds no member")
    forms: list[Form] = []
    for a in range(1, math.isqrt(limit) + 2):
        low, high = math.isqrt(2 * (a - 1) ** 2) + 1, math.isqrt(2 * (a + 1) ** 2 - 1)
        for b in range(low, high + 1):
            n = 2 * (a + 1) * a + b * b
            if n <= limit:
                forms.append(Form(Fraction(a + 1), _HALF * b, SQUARE, n))
        b = 1 + math.isqrt(2 * (a - 1) ** 2)
        n = (a + 1) * a + 2 + b
        if n <= limit:
            forms.append(Form(Fraction(a + 1), _HALF, STRIP, n))
        n = (a + 1) * a + 3 + b
        if CORNER_FROM <= n <= limit:
            forms.append(Form(Fraction(2), _HALF * (b + 1), CORNER, n))
    return forms


def least_table(forms: Iterable[Form], limit: int) -> tuple[Form | None, ...]:
    """Each count's least side among ``forms``, indexed by count to ``limit``: one
    descending pass, the least member at that count or above. Index 0 is unused; a count
    above every member's has None."""
    by_count: dict[int, list[Form]] = {}
    for form in forms:
        by_count.setdefault(form.count, []).append(form)
    least: list[Form | None] = [None] * (limit + 1)
    best: Form | None = None
    for m in range(limit, 0, -1):
        for form in by_count.get(m, ()):
            if best is None or less(form, best):
                best = form
        least[m] = best
    return tuple(least)


@functools.cache
def table(limit: int) -> tuple[Form | None, ...]:
    """Göbel's side at every count to ``limit`` from the build to it (`least_table`)."""
    return least_table(families(limit), limit)


def final(form: Form, limit: int) -> bool:
    """Whether a least side from a build to ``limit`` is final by the area bound: its square,
    p^2 + 2q^2 + 2pq sqrt(2), is below limit + 1, exactly."""
    return _sign(form.p * form.p + 2 * form.q * form.q - (limit + 1), 2 * form.p * form.q) < 0


def proved(n: int, limit: int | None = None) -> bool:
    """Whether the build to ``limit`` proves Göbel's side at ``n`` final (`final`); by
    default the build `side` would read, so every count `side` does not refuse."""
    if limit is None:
        try:
            build_for(n)
        except GoebelError:
            return False
        return True
    if not 1 <= n <= limit:
        return False
    form = table(limit)[n]
    return form is not None and final(form, limit)


def builds() -> list[int]:
    """The builds `side` tries in order: `BUILD`, doubled while under `MAX_BUILD`, then
    `MAX_BUILD` itself."""
    limit, found = min(BUILD, MAX_BUILD), []
    while limit < MAX_BUILD:
        found.append(limit)
        limit *= 2
    return [*found, MAX_BUILD]


def build_for(n: int) -> int:
    """The first build of `builds` that proves Göbel's side at ``n`` final; refused when
    none does."""
    _require(n >= 1, f"n = {n}: no count")
    tried = builds()
    for limit in tried:
        if proved(n, limit):
            return limit
    raise GoebelError(f"n = {n}: no build to {tried[-1]} proves Göbel's side final")


def side(n: int) -> Form:
    """Göbel's construction at ``n``: the least side of any member at ``n`` or above, from a
    build that proves it final (`build_for`)."""
    form = table(build_for(n))[n]
    assert form is not None
    return form


def reach(limit: int = BUILD) -> int:
    """The last count the build to ``limit`` proves final together with every count from
    `HORIZON` + 1 to it; `HORIZON` when it proves none."""
    found = HORIZON
    while proved(found + 1, limit):
        found += 1
    return found


def compare(label: str, rows: Sequence[tuple[int, Fraction, str]]) -> dict[str, Any]:
    """Each row's exact side against Göbel's construction at its count, in the shape the
    frozen receipts' retained program writes: the relation by exact sign, the form, its
    family and count, and the margin as a float. Every count must be proved (`side`)."""
    out = []
    for n, value, note in rows:
        form = side(n)
        relation = {1: "above", 0: "equal", -1: "below"}[sign(value, form)]
        out.append(
            {
                "n": n,
                "side": f"{value.numerator}/{value.denominator}",
                "goebel": form.text(),
                "goebel_family": form.family,
                "goebel_from_count": form.count,
                "relation": relation,
                "margin": form.margin(value),
                "note": note,
            }
        )
    tally = {name: sum(1 for item in out if item["relation"] == name) for name in RELATIONS}
    return {
        "set": label,
        "rows": len(out),
        "tally": tally,
        "above": [item["n"] for item in out if item["relation"] == "above"],
        "detail": out,
    }
