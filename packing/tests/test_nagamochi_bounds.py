#!/usr/bin/env python3
"""The register's most load-bearing citation is checked as arithmetic, not just as a link.

`E-nagamochi-lower` carries the verified lower bound for 88 of the hundred cases; the next
most-cited evidence record carries two. `assurance.py` checks that such a bound cites
verified evidence of the right claim and scope, which is a statement about the citation.
A transcription slip in any one of the 88 values would have passed every existing check.
"""

from __future__ import annotations

import math
from decimal import Decimal, localcontext

import pytest

import devtools.check_nagamochi_bounds as nagamochi
from devtools.check_nagamochi_bounds import RECORD, cases, main, theorem_two


def citing() -> dict[int, dict]:
    return {
        n: case
        for n, case in cases().items()
        if RECORD in ((case.get("verified_lower_bound") or {}).get("evidence") or [])
    }


def test_the_recorded_bounds_re_derive() -> None:
    assert main() == 0


def test_it_covers_the_cases_it_claims_to() -> None:
    """Eighty-eight, and none outside the record's declared scope of 4 to 100."""
    covered = citing()
    assert len(covered) == 88
    assert min(covered) >= 4
    assert max(covered) <= 100


@pytest.mark.parametrize("n", [4, 7, 8, 9, 14, 15, 16, 99, 100])
def test_the_exact_cases_give_an_integer(n: int) -> None:
    """`N` in `{m^2, m^2-1, m^2-2}` is Theorem 2's own special case and gives `s(N) >= m`."""
    value, exact = theorem_two(n)
    assert exact, n
    assert value == value.to_integral_value(), n
    assert value == math.isqrt(n - 1) + 1


@pytest.mark.parametrize("n", [17, 29, 50, 77])
def test_the_general_cases_give_the_root_form(n: int) -> None:
    """Otherwise `s(N) >= sqrt(N - 2k + 1) + 1` with `k = floor(sqrt(N))`."""
    value, exact = theorem_two(n)
    assert not exact, n
    root = math.isqrt(n)
    # Pin the precision: `theorem_two` works at 80 digits and the ambient context is 28,
    # so recomputing the root outside a pinned block compares two different numbers.
    with localcontext() as context:
        context.prec = 80
        assert abs(value - (Decimal(n - 2 * root + 1).sqrt() + 1)) < Decimal("1e-70")


def test_no_recorded_lower_bound_exceeds_its_upper() -> None:
    """The inversion would be a soundness defect, not a bookkeeping one."""
    for n, case in citing().items():
        lower = Decimal(str(case["verified_lower_bound"]["value"]))
        upper = (case.get("reported_upper_bound") or {}).get("value")
        if upper is not None:
            assert lower <= Decimal(str(upper)), n


def test_a_wrong_value_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    """The guard has to bite; a checker that only ever passes is decoration."""
    real = nagamochi.cases

    def poisoned() -> dict[int, dict]:
        found = real()
        found[17]["verified_lower_bound"]["value"] = "4.5"
        return found

    monkeypatch.setattr(nagamochi, "cases", poisoned)
    assert nagamochi.main() == 1
