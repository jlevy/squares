#!/usr/bin/env python3
"""Contract for the minimal-polynomial search and the margin rule that judges it.

An integer-relation algorithm given `d + 1` unknown coefficients and enough digits will
return a relation whether or not one exists, so the search is not the deliverable -- the
rule that refuses most of its answers is.  This file checks that the rule accepts a
polynomial we already know and refuses the case that motivated it.

**The known answer is Trump's.**  `s(11)` satisfies a degree-eight minimal polynomial
published in 1979, and recovering it from digits alone is what says the machinery works.
It came back negated on the first run, which is why the module normalises: an integer
relation is determined only up to a unit and a common factor.

**The refused case is the planning probe's.**  Running the same search on the ~98
serialized digits of `s(29)` returned relations at almost every degree from 8 to 21 --
the signature of an under-determined search -- and a degree-eight candidate whose
relative residual of order `1e-90` had consumed almost exactly the 90 digits it was
allowed.  The rule refuses every one of them, and this file asserts *which clause* does
the refusing rather than only that a refusal happens.

Clause 2, stability under precision, is mandatory and **has no exercised case here**.
Clauses 3 and 1 fire first on everything available: a spurious relation found at low
precision fails the independent-digits test, and one found at high precision fails the
budget test, because its residual sits near the digits it consumed rather than below
`10^-(B + M)`. A relation that passes both and is still pinned to its budget would be
needed to reach clause 2, and none has turned up. Saying so is better than contriving
one, and the clause stays because it is the cheap test that catches what the other two
would not.
"""

from __future__ import annotations

import mpmath as mp
import sympy as sp

from cases.trump11 import packing as trump11
from sqpack.promote.solve import (
    Candidate,
    Refusal,
    SolveError,
    discharge,
    minimal_polynomial,
)

#: Trump 1979, the minimal polynomial of `s(11)`, highest degree first.
PUBLISHED_N11 = (1, -20, 178, -842, 1923, -496, -6754, 12420, -6865)

#: The digits of `s(29)` the archived source serializes, which is the case the rule was
#: written against.
SERIALIZED_N29 = "5.938393132858199"


def n11_value(digits: int) -> str:
    _squares, side, field = trump11.build()
    field.refine_to(digits)
    return field.decimal(side, digits)


def the_rule_recovers_a_published_polynomial() -> None:
    """The known answer: Trump's degree eight, from digits and nothing else."""
    value = n11_value(400)
    found = minimal_polynomial(value, residual_bound="1e-390", max_degree=12)
    assert isinstance(found, Candidate), (
        f"the rule refused a value whose minimal polynomial is published: "
        f"{found.summary() if isinstance(found, Refusal) else found}"
    )
    assert found.degree == 8, f"recovered degree {found.degree}, not Trump's eight"
    assert found.coefficients == PUBLISHED_N11, (
        f"recovered {found.coefficients}, which is not the published polynomial"
    )
    # The numbers the rule used are recorded, so the verdict can be re-run rather than
    # taken. C is the coefficient the relation carries, not the search's bound.
    assert found.largest_coefficient == 12420
    assert float(found.budget_digits) < 40, (
        f"B = {found.budget_digits}: a budget this large would mean C was read from the "
        "search bound rather than from the relation"
    )
    assert mp.mpf(found.residual_at_double) < mp.mpf(found.residual_at_budget), (
        "clause 2 passed without the residual actually falling"
    )


def a_lower_degree_is_preferred_to_a_multiple_of_it() -> None:
    """Degrees are tried upward, because every multiple of a relation is a relation."""
    value = n11_value(400)
    found = minimal_polynomial(value, residual_bound="1e-390", max_degree=20)
    assert isinstance(found, Candidate)
    assert found.degree == 8, (
        f"the search returned degree {found.degree}; searching downward or unordered "
        "would find 16 or 24 just as readily, and none of them is minimal"
    )


def the_serialized_digits_are_refused() -> None:
    """The case the rule exists for: a search that answers because it was under-fed."""
    found = minimal_polynomial(
        SERIALIZED_N29, residual_bound="1e-15", max_degree=12, min_degree=8
    )
    assert isinstance(found, Refusal), (
        f"fifteen serialized digits produced an accepted polynomial: {found}"
    )
    assert found.attempts, "nothing was tried, so nothing was refused"
    assert set(found.kinds) <= {"digits-not-independent", "no-relation"}, (
        f"the refusals came from unexpected clauses: {sorted(set(found.kinds))}"
    )
    assert "digits-not-independent" in found.kinds, (
        "clause 3 did not fire on a value with fifteen digits behind it, which is the "
        "one thing it exists to catch"
    )


def a_bound_that_is_not_a_bound_is_refused() -> None:
    """Clause 3 is only meaningful if the caller must supply a real residual bound."""
    for bad in ("0", "-1e-40"):
        try:
            minimal_polynomial(n11_value(80), residual_bound=bad)
        except SolveError as error:
            assert error.kind == "bad-request", error.kind
        else:
            raise AssertionError(
                f"a residual bound of {bad} was accepted, which makes clause 3 vacuous"
            )


def the_relation_is_reported_in_canonical_form() -> None:
    """Up to a unit and a common factor, so a comparison against a source is meaningful."""
    found = minimal_polynomial(n11_value(400), residual_bound="1e-390", max_degree=12)
    assert isinstance(found, Candidate)
    assert found.coefficients[0] > 0, (
        f"leading coefficient {found.coefficients[0]} is negative; `pslq` returns either "
        "sign and an un-normalised answer reads as a mismatch against a published one"
    )
    text = found.polynomial()
    assert text.startswith("+1*s**8"), text


def the_published_polynomial_discharges_as_an_algebraic_claim() -> None:
    """Fitting is not minimality: the relation must also be irreducible and isolated.

    Any multiple of the minimal polynomial vanishes at the value just as well, so a
    relation that passes the margin rule is not yet a statement about the value's
    degree.  Irreducibility over Q makes it one, and an isolating interval containing
    the refined value says *which* of the polynomial's roots the packing is.
    """
    value = n11_value(400)
    found = minimal_polynomial(value, residual_bound="1e-390", max_degree=12)
    assert isinstance(found, Candidate)
    result = discharge(found, value)
    assert result.discharged, result.refusal
    assert result.irreducible
    assert result.real_root_count == 2, (
        f"Trump's degree-eight polynomial reports {result.real_root_count} real roots, "
        "not two; the isolation is not describing the polynomial we recovered"
    )
    assert result.root_interval is not None
    low, high = result.root_interval
    # Pinned, for the reason `tests/test_witness_interval.py` exists: parsing 60-digit
    # endpoints at mpmath's ambient default of 15 collapses both onto the same number and
    # the containment reads false. `discharge` pins its own; this is the caller's.
    saved = mp.mp.dps
    mp.mp.dps = 200
    try:
        assert mp.mpf(low) < mp.mpf(value) < mp.mpf(high)
    finally:
        mp.mp.dps = saved


def a_reducible_relation_is_refused_as_not_minimal() -> None:
    """The square of the published polynomial vanishes just as well and is not minimal."""
    value = n11_value(120)
    squared = sp.Poly(
        sp.expand(
            sum(
                int(c) * sp.Symbol("s") ** p
                for p, c in zip(range(8, -1, -1), PUBLISHED_N11, strict=True)
            )
            ** 2
        ),
        sp.Symbol("s"),
    )
    reducible = Candidate(
        degree=16,
        coefficients=tuple(int(c) for c in squared.all_coeffs()),
        largest_coefficient=max(abs(int(c)) for c in squared.all_coeffs()),
        budget_digits="0",
        margin_digits=200,
        residual_at_budget="0",
        residual_at_double="0",
        input_residual_bound="1e-110",
        working_digits=120,
    )
    result = discharge(reducible, value)
    assert not result.discharged
    assert not result.irreducible, (
        "the square of the published polynomial was reported irreducible, so nothing "
        "here distinguishes a minimal polynomial from a multiple of one"
    )
    assert result.refusal is not None and "factors over Q" in result.refusal, (
        f"a reducible relation was refused for the wrong reason: {result.refusal}"
    )


def main() -> int:
    the_rule_recovers_a_published_polynomial()
    a_lower_degree_is_preferred_to_a_multiple_of_it()
    the_serialized_digits_are_refused()
    a_bound_that_is_not_a_bound_is_refused()
    the_relation_is_reported_in_canonical_form()
    the_published_polynomial_discharges_as_an_algebraic_claim()
    a_reducible_relation_is_refused_as_not_minimal()
    print("minimal polynomial and margin rule contract selftest passed")
    return 0


def test_promote_solve() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
