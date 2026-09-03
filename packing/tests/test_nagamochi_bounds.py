#!/usr/bin/env python3
"""The register's most load-bearing citation is checked as arithmetic, not just as a link.

`E-nagamochi-lower` carries the verified lower bound for 86 of the hundred cases (88
until 2026-08-31, when the first-party green17 certificate took over `n = 17` and
`n = 18`); the next most-cited evidence record carries two. `assurance.py` checks that
such a bound cites verified evidence of the right claim and scope, which is a statement
about the citation. A transcription slip in any one of the 86 values would have passed
every existing check.
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
    """Eighty-five, and none outside the record's declared scope of 4 to 100."""
    covered = citing()
    assert len(covered) == 85
    assert min(covered) >= 4
    assert max(covered) <= 100
    # The two cases the green17 certificate took over cite it no longer.
    assert 17 not in covered
    assert 18 not in covered
    # `n = 19` left on 2026-09-03, when `T-016` adopted the source-backed 4.5058
    # bound and beat Theorem 2's `1 + sqrt(12)` there.
    assert 19 not in covered


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
        # Poison a case this record still carries. `n = 19` was the target until
        # `T-016` took it over on 2026-09-03, at which point poisoning it stopped
        # reaching the checker at all and this control passed without biting.
        # The value has to miss by more than one unit in its own last place: the
        # tolerance is `10 ** -places`, so against `n = 20`'s `4.6055...` both `4.6`
        # and `4.7` are accepted at one decimal place, and only `4.8` disagrees.
        # It also has to stay under the reported upper bound of 5.0, or the checker
        # reports an inversion instead and the control passes for the wrong reason.
        found[20]["verified_lower_bound"]["value"] = "4.8"
        return found

    monkeypatch.setattr(nagamochi, "cases", poisoned)
    assert nagamochi.main() == 1
