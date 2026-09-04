#!/usr/bin/env python3
"""The register's most load-bearing citation is checked as arithmetic, not just as a link.

`E-nagamochi-lower` carries the verified lower bound for most of the hundred cases: 88
until 2026-08-31, when the first-party green17 certificate took over `n = 17` and
`n = 18`; 85 when the adopted 4.5058 bound took `n = 19` on 2026-09-03; 83 on
2026-09-04, when `T-020` took `n = 20` and `n = 21`. The next most-cited evidence
record carries two. `assurance.py` checks that such a bound cites verified evidence of
the right claim and scope, which is a statement about the citation. A transcription slip
in any one of the values would have passed every existing check.

Nothing below pins that count. Three tests here did, and each went stale the day a
result moved a case off the closed form -- one of them a poisoned-control test whose
target `n = 20` acquired, as a real result, the very value it was poisoning with, so the
control passed without biting for the second time in its life (`D-482`). What a test can
hold without going stale is the relation: a case cites the theorem only where its value
is the theorem's, and no case a retained certificate reaches still cites it.
"""

from __future__ import annotations

import json
import math
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import pytest

import devtools.check_nagamochi_bounds as nagamochi
from devtools.check_nagamochi_bounds import RECORD, cases, main, prose_counts, theorem_two
from sqpack.fractional.certificate import least_size_certified

CASES_DIR = Path(__file__).parents[1] / "cases"


def citing() -> dict[int, dict]:
    return {
        n: case
        for n, case in cases().items()
        if RECORD in ((case.get("verified_lower_bound") or {}).get("evidence") or [])
    }


def test_the_recorded_bounds_re_derive() -> None:
    assert main() == 0


def reached_by_retained_certificates() -> set[int]:
    """Every case a retained fractional certificate moves off the closed form.

    Read from the case packages, not from a list: a certificate of side `L` and
    total mass `M` certifies every `n` above `M`, and displaces Theorem 2 at each
    such `n` where the theorem's value is below `L`. The packages are the record.
    """
    reached: set[int] = set()
    for path in sorted(CASES_DIR.glob("n*_fractional_certificate/certificate.json")):
        record = json.loads(path.read_text())
        side = Fraction(record["outer_side"])
        mass = sum((Fraction(w) for _, _, w in record["atoms"]), Fraction(0))
        for n in range(least_size_certified(mass), 101):
            if theorem_two(n)[0] < Decimal(side.numerator) / Decimal(side.denominator):
                reached.add(n)
    return reached


def test_it_covers_the_cases_it_claims_to() -> None:
    """Every citing case sits in the theorem's scope, and none a certificate reaches cites it.

    The count is not pinned. It was 85 when this test was written and 83 by the
    evening of 2026-09-04; each time it moved, the literal here outlived the
    record it described (`D-482`). What holds is the relation.
    """
    covered = citing()
    assert min(covered) >= 4
    assert max(covered) <= 100
    reached = reached_by_retained_certificates()
    # The retained packages today: n = 11, 12, 17 and 20, reaching 11, 12, 17-21.
    assert {11, 12, 17, 18, 19, 20, 21} <= reached
    assert not (reached & set(covered)), sorted(reached & set(covered))
    # Everything still citing the theorem carries the theorem's own value; `main`
    # re-derives each one, and this is the same statement from the other side.
    for n, case in covered.items():
        value = Decimal(str(case["verified_lower_bound"]["value"]))
        exponent = value.as_tuple().exponent
        places = max(0, -exponent) if isinstance(exponent, int) else 0
        assert abs(value - theorem_two(n)[0]) <= Decimal(10) ** -places, n


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
        # Poison a case this record still carries -- chosen from the record, because
        # a fixed target goes blind. `n = 19` was the target until `T-016` took it
        # over on 2026-09-03; `n = 20` replaced it and was taken over by `T-020` on
        # 2026-09-04 with the very value this control poisoned it with, `4.8`, so
        # the poison became the truth and the control passed without biting (D-482).
        # The target is the largest citing case with at least 0.3 of room under its
        # reported upper bound, so the poison neither reads as an inversion nor
        # lands inside the checker's one-unit-in-the-last-place tolerance.
        target = max(
            n
            for n, case in found.items()
            if RECORD in ((case.get("verified_lower_bound") or {}).get("evidence") or [])
            and (case.get("reported_upper_bound") or {}).get("value") is not None
            and Decimal(str(case["reported_upper_bound"]["value"]))
            - Decimal(str(case["verified_lower_bound"]["value"]))
            >= Decimal("0.3")
        )
        value = Decimal(str(found[target]["verified_lower_bound"]["value"]))
        found[target]["verified_lower_bound"]["value"] = str(
            (value + Decimal("0.2")).quantize(Decimal("0.1"))
        )
        return found

    monkeypatch.setattr(nagamochi, "cases", poisoned)
    assert nagamochi.main() == 1


def test_the_prose_counts_agree_with_the_records() -> None:
    """The README and the case bodies quote the corpus, not a memory of it (D-430)."""
    assert prose_counts(cases()) == []


def test_a_stale_readme_count_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: pytest.TempPathFactory
) -> None:
    """The figure that outlived the 4.5058 adoption by a day would now fail the gate."""
    stale = tmp_path / "README.md"  # type: ignore[operator]
    stale.write_text(
        "Of the 65 open cases, **63** have\nNagamochi\u2019s general closed form.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(nagamochi, "README", stale)
    found = cases()
    open_cases = [case for case in found.values() if case.get("status") == "open"]
    governed = sum(
        RECORD in ((case.get("verified_lower_bound") or {}).get("evidence") or [])
        for case in open_cases
    )
    problems = prose_counts(found)
    assert len(problems) == 1
    assert "63 of 65" in problems[0]
    # The corpus figure is read from the record here, as the checker reads it: it
    # was 60 when this test was written and 58 a day later (D-482).
    assert f"{governed} of {len(open_cases)}" in problems[0]
    assert governed < 63
