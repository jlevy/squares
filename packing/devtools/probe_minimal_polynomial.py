#!/usr/bin/env python3
"""Search for a case's minimal polynomial and report what the margin rule made of it.

The search is not the point; the rule that refuses most of its answers is.  An
integer-relation algorithm given `d + 1` unknown coefficients and enough digits returns a
relation whether or not one exists, so this tool always reports *which clause* decided,
degree by degree, rather than a bare answer.

**Two cases, two outcomes, and the contrast is the result.**

`n = 11` closes the loop: Trump published the degree-eight minimal polynomial of `s(11)`
in 1979, and the rule recovers it from digits alone.  That is the known answer this
machinery is calibrated against.

`n = 29` refuses, and refuses in the strongest available way.  The planning probe ran on
the roughly ninety-eight serialized digits and got relations at almost every degree from
8 to 21 -- the signature of a search with more freedom than input.  Run on a thousand
digits manufactured from the closed system, `pslq` returns **nothing at any degree the
digits can speak to** below a coefficient bound of `10^22`.  A search that answers when
under-fed and falls silent when fed properly is evidence about the number, not about the
search.

**How far "any degree" goes is arithmetic, not a default.**  The sweep used to stop at
twenty because twenty was the flag's default, and twenty is well short of what a
thousand digits pay for: :func:`sqpack.promote.solve.reach` rearranges clause 3 at the
largest coefficient the search may return and puts the ceiling at **degree 35**, which
is where this tool now stops unless a caller says otherwise.  The refusal has been
carried to **degree 29**, and every degree from 21 to 29 came back the way 2 to 20
already had -- `pslq` returned nothing, so no clause was needed.  If `s(29)` is
algebraic of degree 29 or less, some coefficient is at least `10^22`.

Degrees 30 to 35 sit inside the same digits and are unrun for time rather than for
evidence: `pslq` cost 387 seconds at degree 29 and had been climbing by about 30 a
degree since 23, which puts the remaining six at roughly fifty minutes on one core.

None of this says anything about degree 36, and that gap is not small.  The mixed-volume
bound puts the degree of `s(29)` at 15,744, four hundred times further out than a
thousand digits can see, and the reach grows only like `P / log10(C)` -- reaching 15,744
at this coefficient bound would want some 350,000 digits and a `pslq` basis of 15,745
terms to go with them.  Closing that gap is the interval route's job, not this one's.

That refusal is why the interval route exists, and recording it is the point of this
tool.  It is slow -- about twelve minutes through degree 20, fifty-four through 29, and
an estimated hour and three-quarters to the ceiling at 35, almost all of it inside
`pslq` -- which is why it is a tool with a retained record rather than a test.

Usage:

    python -m devtools.probe_minimal_polynomial --case trump11
    python -m devtools.probe_minimal_polynomial --case kingbird29 --max-degree 20
    python -m devtools.probe_minimal_polynomial --json
"""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from collections.abc import Callable, Sequence
from typing import Any

import mpmath as mp

from cases.kingbird29 import system as k29
from cases.kingbird29.layout import DEFAULT_SOURCE
from cases.trump11 import packing as trump11
from sqpack.promote.refine import refine
from sqpack.promote.solve import (
    MAX_COEFFICIENT,
    Candidate,
    discharge,
    minimal_polynomial,
    reach,
)

#: Trump 1979, for the `n = 11` known-answer comparison.
PUBLISHED_N11 = (1, -20, 178, -842, 1923, -496, -6754, 12420, -6865)

#: Digits to manufacture before searching. `n = 11` needs far fewer than this and the
#: extra costs nothing; `n = 29` needs them, because clause 3 tests the refinement's
#: reported residual bound and a shorter one would refuse every degree on that clause
#: alone -- which says nothing about whether a relation exists.
DEFAULT_DIGITS = 1000


def _trump11(digits: int) -> tuple[str, str, str]:
    """`s(11)` from its exact field, with the digit count as the declared bound.

    The field is *derived from* the published polynomial, so recovering that polynomial
    here calibrates the machinery rather than deriving anything.  Said plainly because
    the distinction is easy to lose: this is a known-answer check, not evidence about
    `s(11)`.
    """
    _squares, side, field = trump11.build()
    field.refine_to(digits)
    return field.decimal(side, digits), f"1e-{digits - 10}", "exact field (known answer)"


def _kingbird29(digits: int) -> tuple[str, str, str]:
    """`s(29)` from a Newton refinement of the published closed system.

    The residual bound is the refinement's own reported bound, which is what clause 3
    means by "digits available" -- never the number of digits a source happens to print.
    """
    refinement = refine(k29.equations, k29.seed(DEFAULT_SOURCE), digits, names=k29.UNKNOWNS)
    return (
        refinement.values[0],
        refinement.residual_bound,
        f"Newton refinement of the published system, residual {refinement.residual}",
    )


CASES: dict[str, Callable[[int], tuple[str, str, str]]] = {
    "trump11": _trump11,
    "kingbird29": _kingbird29,
}


def probe(name: str, *, digits: int, max_degree: int | None, max_coefficient: int) -> dict:
    """Manufacture digits, search, judge, and discharge anything that survives.

    `max_degree` defaults to the reach the manufactured digits support, so the sweep
    stops where the evidence does rather than at a number someone typed once.
    """
    started = time.monotonic()
    value, bound, provenance = CASES[name](digits)
    manufactured = time.monotonic() - started

    ceiling = reach(value, bound, max_coefficient=max_coefficient)
    if max_degree is None:
        max_degree = max(ceiling, 2)

    started = time.monotonic()
    found = minimal_polynomial(
        value,
        residual_bound=bound,
        max_degree=max_degree,
        max_coefficient=max_coefficient,
    )
    searched = time.monotonic() - started

    report: dict[str, Any] = {
        "case": name,
        "digits_requested": digits,
        "residual_bound": bound,
        "provenance": provenance,
        "value_head": value[:60],
        "max_degree": max_degree,
        "reach": ceiling,
        "max_coefficient": max_coefficient,
        "seconds_manufacturing": round(manufactured, 1),
        "seconds_searching": round(searched, 1),
    }
    if isinstance(found, Candidate):
        result = discharge(found, value)
        report["outcome"] = "accepted"
        report["degree"] = found.degree
        report["coefficients"] = list(found.coefficients)
        report["largest_coefficient"] = found.largest_coefficient
        report["budget_digits"] = found.budget_digits
        report["margin_digits"] = found.margin_digits
        report["residual_at_budget"] = found.residual_at_budget
        report["residual_at_double"] = found.residual_at_double
        report["polynomial"] = found.polynomial()
        report["irreducible"] = result.irreducible
        report["real_roots"] = result.real_root_count
        report["discharged"] = result.discharged
        report["discharge_refusal"] = result.refusal
        if name == "trump11":
            report["matches_published"] = tuple(found.coefficients) == PUBLISHED_N11
    else:
        report["outcome"] = "refused"
        report["summary"] = found.summary()
        report["by_clause"] = dict(Counter(found.kinds))
        report["attempts"] = [
            {"degree": degree, "kind": kind, "detail": detail}
            for degree, kind, detail in found.attempts
        ]
    return report


def _render(report: dict) -> None:
    print(f"== {report['case']} ==")
    print(f"  {report['provenance']}")
    print(
        f"  {report['digits_requested']} digits, reported residual bound "
        f"{report['residual_bound']} ({report['seconds_manufacturing']}s)"
    )
    print(f"  value: {report['value_head']}...")
    print(
        f"  searched degrees 2..{report['max_degree']} with |c| < "
        f"{report['max_coefficient']:.0e} ({report['seconds_searching']}s); "
        f"the digits reach degree {report['reach']}"
    )
    if report["outcome"] == "accepted":
        print(f"  ACCEPTED at degree {report['degree']}")
        print(f"    {report['polynomial']}")
        print(
            f"    C={report['largest_coefficient']}  B={report['budget_digits']}  "
            f"M={report['margin_digits']}"
        )
        print(
            f"    residual {report['residual_at_budget']} at B+M, "
            f"{report['residual_at_double']} at 2B+2M"
        )
        print(
            f"    irreducible over Q: {report['irreducible']}; "
            f"{report['real_roots']} real roots; discharged: {report['discharged']}"
        )
        if "matches_published" in report:
            print(f"    matches the published polynomial: {report['matches_published']}")
    else:
        print(f"  REFUSED: {report['summary']}")
        for kind, count in sorted(report["by_clause"].items()):
            print(f"    {kind}: {count} degrees")
        if set(report["by_clause"]) == {"no-relation"}:
            print(
                "    Every degree came back empty rather than refused by a clause, which "
                "is the strong form: the search found nothing to judge. If this value is "
                f"algebraic of degree <= {report['max_degree']}, some coefficient is at "
                f"least {report['max_coefficient']:.0e}."
            )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=[*CASES, "all"], default="all")
    parser.add_argument("--digits", type=int, default=DEFAULT_DIGITS)
    parser.add_argument(
        "--max-degree",
        type=int,
        default=None,
        help="stop here instead of at the degree the digits reach",
    )
    parser.add_argument("--max-coefficient", type=int, default=MAX_COEFFICIENT)
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args(argv)

    saved = mp.mp.dps
    try:
        names = list(CASES) if arguments.case == "all" else [arguments.case]
        reports = [
            probe(
                name,
                digits=arguments.digits,
                max_degree=arguments.max_degree,
                max_coefficient=arguments.max_coefficient,
            )
            for name in names
        ]
    finally:
        mp.mp.dps = saved

    if arguments.json:
        print(json.dumps(reports, indent=2, sort_keys=True))
        return 0
    for report in reports:
        _render(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
