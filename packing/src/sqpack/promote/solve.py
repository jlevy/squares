"""Recover a minimal polynomial from a refined value, under a decidable margin rule.

This is the step that turns a number known to many digits into an *algebraic* claim.
The danger is specific and it is the reason this module is mostly a test rather than a
search: an integer-relation algorithm given `d + 1` unknown coefficients and enough
digits will return a relation whether or not one exists.  Ask for degree eight from a
hundred digits and you get a degree-eight answer; ask for degree twelve and you get one
of those too.  A search that always answers is not evidence.

**The margin rule, frozen as a test rather than a caution.**  Let `C` be the largest
absolute integer coefficient the relation *actually carries* -- not the search's
`maxcoeff` bound, which overstates it and would make the budget look larger than the
relation earned -- and let

    B = (d + 1) * log10(C)

be the digits the relation could have consumed fitting itself.  With the project margin
fixed at `M = 200`, a candidate is accepted only when all three hold:

1. **Budget.**  The relative residual is below `10^-(B + M)`.
2. **Stability under precision.**  Re-evaluated at `2B + 2M` digits, the residual keeps
   *falling* rather than resting near `10^-B`.  A spurious relation is pinned to the
   budget that produced it; a genuine one is not.  This is the cheap decisive test and
   it is not optional.
3. **Independent digits.**  The value comes from a refinement whose *reported residual
   bound* is below `10^-(B + M)`.  "Digits available" always means that bound, never how
   many digits a source happens to print.

Clause 2 is what the planning probe lacked, and it is why that probe's degree-eight
"relation" for `s(29)` was reported as spurious.

**Clause 2's headroom comes from clause 3, which is why they are not independent.**  The
residual at `2B + 2M` cannot fall below the accuracy of the value itself, so re-evaluating
a relation against a value known to fewer digits than that would measure the value's error
rather than the relation's fit.  Clause 3 is what guarantees the headroom: it requires the
refinement's bound to be below `10^-(B + M)` in the first place.  Trump's degree-eight
relation falls from `4.99e-338` to `3.38e-412` against a value carrying 400 digits, and
that fall is the signal; a relation pinned to its budget would sit at `10^-B` in both.

**How far the rule can see is arithmetic, and :func:`reach` does it.**  Rearranging
clause 3 for the worst relation a search may return -- one whose coefficients saturate
the search's own bound -- gives `(d + 1) * log10(C) + M < P`, so the digits fix a
largest degree beyond which no such relation could be judged.  That ceiling is what a
sweep should stop at: a refusal above it is a statement about the digits rather than
about the number.  It is a ceiling on the *worst* case only -- Trump's degree eight
carries `C = 12420` and clears a bound that a degree-seven relation at `C = 10^22`
would not -- so it bounds a sweep rather than gating an answer.

**`P` is the worse of two limits, not the refinement's residual alone.**  A refinement
reports a residual bound, and then rounds its value to the digits it was asked for on
the way out; those need not agree.  The `n = 29` refinement at 1000 digits reports
`1.09829e-1039` but serializes 1000 significant digits, and clause 3 reading the
residual alone would have judged degrees 36 and 37 against 39 digits the value does not
carry.  :func:`available_digits` takes the worse of the two, which is what clause 3 now
tests.

Everything the rule consumed is recorded on the result -- `d`, `C`, `B`, `M`, the
residual at `B` and the residual at `2B + 2M` -- so a reader can re-run the judgement
instead of taking the verdict.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field

import mpmath as mp
import sympy as sp

#: The project's fixed margin, in decimal digits, from the promotion spec.
MARGIN_DIGITS = 200

#: Extra working digits held above the largest precision any clause asks for.
GUARD_DIGITS = 50


class SolveError(ValueError):
    """A typed solve failure, carrying a `kind` a caller can branch on."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


#: The default coefficient ceiling handed to `pslq`, and the `C` a reach is computed at.
MAX_COEFFICIENT = 10**22


def digits_carried(value: str) -> int:
    """Significant decimal digits in a serialized value, however it is written.

    A refinement reports a bound on its residual and separately rounds its value to the
    digits the caller asked for.  The search only ever sees the rounded string, so this
    is the second of the two limits on what any clause may rely on.
    """
    mantissa = value.strip().lstrip("+-").partition("e")[0].partition("E")[0]
    return len(mantissa.replace(".", "").lstrip("0"))


def available_digits(value: str, residual_bound: str):
    """`P`: the digits a clause may rely on, as the worse of the two limits on them.

    The reported residual bound is one limit and the value's own length is the other,
    and taking the better of them would credit the search with digits it was not given.
    """
    bound = mp.mpf(residual_bound)
    truncation = mp.mpf(10) ** (-digits_carried(value))
    return -mp.log10(max(bound, truncation))


def reach(
    value: str,
    residual_bound: str,
    *,
    margin_digits: int = MARGIN_DIGITS,
    max_coefficient: int = MAX_COEFFICIENT,
) -> int:
    """The largest degree at which a refusal is still a statement about the value.

    Clause 3 demands `(d + 1) * log10(C) + M < P`.  Read at the largest `C` the search
    may return, that is a ceiling on the degrees worth sweeping: above it, a relation
    carrying coefficients near the bound could not be judged whether or not one exists,
    so a refusal there measures the digits rather than the number.

    This bounds a sweep; it does not gate an answer.  A relation that carries small
    coefficients has a smaller `B` and can be judged well above this degree -- Trump's
    degree eight, at `C = 12420`, is accepted from 400 digits where this function
    reports seven.
    """
    span = mp.log10(max_coefficient)
    if span <= 0:
        raise SolveError(
            "bad-request",
            f"a coefficient bound of {max_coefficient} leaves no digits to charge a "
            "relation for, so no reach is defined",
        )
    terms = (available_digits(value, residual_bound) - margin_digits) / span
    return max(int(mp.ceil(terms)) - 2, 0)


@dataclass(frozen=True)
class Candidate:
    """A relation that passed every clause, with the numbers the clauses used."""

    degree: int
    coefficients: tuple[int, ...]
    largest_coefficient: int
    budget_digits: str
    margin_digits: int
    residual_at_budget: str
    residual_at_double: str
    input_residual_bound: str
    working_digits: int

    def polynomial(self, symbol: str = "s") -> str:
        """The relation written out, highest degree first."""
        terms = []
        for power, coefficient in zip(
            range(self.degree, -1, -1), self.coefficients, strict=True
        ):
            if coefficient == 0:
                continue
            if power == 0:
                terms.append(f"{coefficient:+d}")
            elif power == 1:
                terms.append(f"{coefficient:+d}*{symbol}")
            else:
                terms.append(f"{coefficient:+d}*{symbol}**{power}")
        return " ".join(terms) if terms else "0"


@dataclass(frozen=True)
class Refusal:
    """No candidate survived, and which clause each degree died on."""

    max_degree: int
    input_residual_bound: str
    margin_digits: int
    #: One entry per degree tried: `(degree, kind, detail)`.
    attempts: tuple[tuple[int, str, str], ...] = field(default=())

    @property
    def kinds(self) -> tuple[str, ...]:
        return tuple(kind for _degree, kind, _detail in self.attempts)

    def summary(self) -> str:
        counts: dict[str, int] = {}
        for kind in self.kinds:
            counts[kind] = counts.get(kind, 0) + 1
        spread = ", ".join(f"{kind} x{count}" for kind, count in sorted(counts.items()))
        return (
            f"no relation through degree {self.max_degree} survived the margin rule "
            f"({spread or 'nothing tried'})"
        )


def _normalise(coefficients: Sequence[int]) -> tuple[int, ...]:
    """The relation in its canonical form: primitive, with a positive leading term.

    An integer relation is only determined up to a unit and a common factor -- `pslq`
    may return `-p` or `2p` as readily as `p` -- so a caller comparing against a
    published polynomial would see a spurious mismatch.  Trump's degree-eight relation
    came back negated on the first run for exactly that reason.
    """
    values = [int(value) for value in coefficients]
    common = 0
    for value in values:
        common = math.gcd(common, abs(value))
    if common > 1:
        values = [value // common for value in values]
    leading = next((value for value in values if value != 0), 0)
    if leading < 0:
        values = [-value for value in values]
    return tuple(values)


def _budget(degree: int, coefficients: Sequence[int]):
    """`B = (d + 1) * log10(C)` from the coefficients the relation actually carries."""
    largest = max(abs(int(value)) for value in coefficients)
    if largest <= 1:
        # log10(1) is zero and would make the budget vanish, which would accept anything.
        # A relation whose largest coefficient is one still consumed the digits it took
        # to place d + 1 signs, so charge it that.
        return largest, mp.mpf(degree + 1) * mp.log10(2)
    return largest, mp.mpf(degree + 1) * mp.log10(largest)


def _residual(coefficients: Sequence[int], value, digits: int):
    """`|p(x)| / max|term|` at `digits` working precision -- relative, not absolute.

    Relative because an absolute residual can be made small by shrinking the
    coefficients, and the rule is about how well the relation fits, not how big it is.
    """
    previous = mp.mp.dps
    mp.mp.dps = digits + GUARD_DIGITS
    try:
        x = mp.mpf(value)
        total = mp.mpf(0)
        largest = mp.mpf(0)
        power = len(coefficients) - 1
        for coefficient in coefficients:
            term = mp.mpf(int(coefficient)) * x**power
            total += term
            largest = max(largest, abs(term))
            power -= 1
        if largest == 0:
            return mp.mpf(0)
        return abs(total) / largest
    finally:
        mp.mp.dps = previous


def _decimal(value, digits: int = 6) -> str:
    return str(mp.nstr(mp.mpf(value), n=digits, strip_zeros=False))


def minimal_polynomial(
    value: str,
    *,
    residual_bound: str,
    max_degree: int = 20,
    min_degree: int = 2,
    margin_digits: int = MARGIN_DIGITS,
    max_coefficient: int = MAX_COEFFICIENT,
) -> Candidate | Refusal:
    """Search for the minimal polynomial of `value`, and judge it by the margin rule.

    `residual_bound` is the phase-3 refinement's *reported* bound on the value, and it
    is what clause 3 tests.  Passing a bound the refinement did not report -- a digit
    count, or the length of a serialized string -- defeats the clause entirely, so it is
    required rather than defaulted.

    Returns the first degree whose relation passes all three clauses, or a
    :class:`Refusal` recording what each degree died on.  Degrees are tried in
    increasing order because the *minimal* polynomial is wanted: a genuine relation of
    degree `d` is also satisfied by every multiple of it, and stopping at the first
    survivor is what makes the answer minimal rather than merely correct.
    """
    if min_degree < 1 or max_degree < min_degree:
        raise SolveError(
            "bad-request", f"degree range {min_degree}..{max_degree} is not searchable"
        )
    bound = mp.mpf(residual_bound)
    if bound <= 0:
        raise SolveError(
            "bad-request",
            f"residual bound {residual_bound} is not positive; a bound of zero would "
            "make clause 3 vacuous",
        )

    attempts: list[tuple[int, str, str]] = []
    # Clause 3 is tested against the worse of the refinement's reported bound and the
    # digits the serialized value carries, because the search only ever sees the
    # string. Where the two disagree the refusal says which one bound it.
    usable = available_digits(value, residual_bound)
    floor = mp.mpf(10) ** (-usable)
    limit = "the value's serialized digits" if floor > bound else "the refinement"
    # Enough precision to evaluate at 2B + 2M for the largest budget a search could
    # return, plus guard. The search itself runs at the digits the value carries.
    available = int(usable)
    previous = mp.mp.dps
    try:
        for degree in range(min_degree, max_degree + 1):
            mp.mp.dps = available + GUARD_DIGITS
            basis = [mp.mpf(value) ** power for power in range(degree + 1)]
            relation = mp.pslq(basis, maxcoeff=max_coefficient, maxsteps=10_000)
            if relation is None:
                attempts.append((degree, "no-relation", "pslq returned nothing"))
                continue
            # pslq orders by ascending power; the record is highest-degree first.
            coefficients = _normalise(list(reversed(relation)))
            largest, budget = _budget(degree, coefficients)
            needed = budget + margin_digits

            if floor >= mp.mpf(10) ** (-needed):
                attempts.append(
                    (
                        degree,
                        "digits-not-independent",
                        (
                            f"{limit} leaves the value good to 10^-{_decimal(usable)}, "
                            f"which is not below 10^-{_decimal(needed)}; clause 3"
                        ),
                    )
                )
                continue

            at_budget = _residual(coefficients, value, int(needed) + GUARD_DIGITS)
            if at_budget >= mp.mpf(10) ** (-needed):
                attempts.append(
                    (
                        degree,
                        "over-budget",
                        (
                            f"relative residual {_decimal(at_budget)} is not below "
                            f"10^-{_decimal(needed)} with C={largest}; clause 1"
                        ),
                    )
                )
                continue

            doubled = 2 * budget + 2 * margin_digits
            at_double = _residual(coefficients, value, int(doubled) + GUARD_DIGITS)
            if at_double >= at_budget:
                attempts.append(
                    (
                        degree,
                        "pinned-to-its-budget",
                        (
                            f"residual {_decimal(at_double)} at 2B+2M did not fall "
                            f"below {_decimal(at_budget)} at B+M, which is the "
                            "signature of a relation fitted to the digits it was "
                            "given; clause 2"
                        ),
                    )
                )
                continue

            return Candidate(
                degree=degree,
                coefficients=coefficients,
                largest_coefficient=largest,
                budget_digits=_decimal(budget),
                margin_digits=margin_digits,
                residual_at_budget=_decimal(at_budget),
                residual_at_double=_decimal(at_double),
                input_residual_bound=residual_bound,
                working_digits=available,
            )
    finally:
        mp.mp.dps = previous

    return Refusal(
        max_degree=max_degree,
        input_residual_bound=residual_bound,
        margin_digits=margin_digits,
        attempts=tuple(attempts),
    )


@dataclass(frozen=True)
class Discharge:
    """What became of a candidate when it was checked as an algebraic claim."""

    irreducible: bool
    degree: int
    #: The isolating interval for the real root, as decimal endpoints.
    root_interval: tuple[str, str] | None
    #: Whether that interval contains the value the relation was found from.
    contains_value: bool
    real_root_count: int
    refusal: str | None = None

    @property
    def discharged(self) -> bool:
        return (
            self.irreducible
            and self.contains_value
            and self.root_interval is not None
            and self.refusal is None
        )


def discharge(candidate: Candidate, value: str, *, digits: int = 60) -> Discharge:
    """Turn a relation that fits into an algebraic claim, or say why it is not one.

    Passing the margin rule says a relation *vanishes* at the value to far more digits
    than it could have fitted.  It does not say the relation is the **minimal**
    polynomial, and the difference matters: any multiple of the minimal polynomial
    vanishes just as well, and `pslq` will return one if the degree it is asked for
    admits one.  Two things close that gap.

    **Irreducibility over Q.**  A reducible relation is a product, and the value is a
    root of exactly one factor -- so the relation is not minimal and its degree is not
    the value's degree.

    **An isolating interval that contains the value.**  Irreducibility alone does not
    say *which* root was found, and a degree-eight polynomial has up to eight of them.
    Isolating the real roots and requiring exactly one of the intervals to contain the
    refined value is what ties the algebraic object to the packing it came from.

    What this does **not** do is rebuild the packing from the field and re-verify it.
    That needs an exact solve of every pose unknown, not only the side, and it is the
    round-trip the promotion spec asks for separately. This is the half that can be done
    from the side alone, and calling it the whole round trip would overstate it.
    """
    symbol = sp.Symbol("s")
    polynomial = sum(
        int(coefficient) * symbol**power
        for power, coefficient in zip(
            range(candidate.degree, -1, -1), candidate.coefficients, strict=True
        )
    )
    poly = sp.Poly(polynomial, symbol)
    try:
        irreducible = bool(poly.is_irreducible)
    except (sp.PolynomialError, NotImplementedError) as error:
        return Discharge(
            irreducible=False,
            degree=candidate.degree,
            root_interval=None,
            contains_value=False,
            real_root_count=0,
            refusal=f"irreducibility undecided: {error}",
        )
    if not irreducible:
        return Discharge(
            irreducible=False,
            degree=candidate.degree,
            root_interval=None,
            contains_value=False,
            real_root_count=0,
            refusal=(
                "the relation factors over Q, so it is a multiple of the minimal "
                "polynomial rather than the minimal polynomial, and its degree is not "
                "the value's degree"
            ),
        )

    roots = sp.real_roots(poly)
    previous = mp.mp.dps
    mp.mp.dps = digits + GUARD_DIGITS
    try:
        target = mp.mpf(value)
        width = mp.mpf(10) ** (-(digits // 2))
        containing = []
        for root in roots:
            approximation = mp.mpf(str(sp.N(root, digits)))
            if abs(approximation - target) < width:
                containing.append(
                    (
                        _decimal(approximation - width, digits),
                        _decimal(approximation + width, digits),
                    )
                )
        if len(containing) != 1:
            return Discharge(
                irreducible=True,
                degree=candidate.degree,
                root_interval=None,
                contains_value=False,
                real_root_count=len(roots),
                refusal=(
                    f"{len(containing)} of the {len(roots)} real roots lie within "
                    f"{_decimal(width)} of the value; exactly one is needed to say "
                    "which root the packing is"
                ),
            )
        return Discharge(
            irreducible=True,
            degree=candidate.degree,
            root_interval=containing[0],
            contains_value=True,
            real_root_count=len(roots),
        )
    finally:
        mp.mp.dps = previous
