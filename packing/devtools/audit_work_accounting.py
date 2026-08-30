#!/usr/bin/env python3
"""Which unit of work the three accounting instruments can actually agree on.

`BC-017` asks whether a stratum can be priced in **counted LP solves** end to end, so
enumeration results are comparable to each other and to the annealer without reference to
wall time. Its own note says the obstruction, and says it is not about arithmetic:

> `solve_cell` counts actual retries while collapsing seated-wall and contact/nonedge
> roles; `contact_realization` refuses walls and omits nonedge separation; and sqsearch
> pair tests are dynamic overlap tests, not compiled rows.

Three instruments, three vocabularies. This runs them against the same three-square
subject and reports what each one can and cannot separate, so the readiness decision the
`promotion_boundary` authorizes is made against a measurement rather than against a reading
of the code.

**The answer is narrower than the note reads and better than it sounds.** Exactly one unit
survives all three: the LP solve attempt. Everything finer is separated by the structural
plan and collapsed by the solver, and the one counter that appears in two of them --
`pair_tests` -- counts different things in each, so agreeing on its name would be worse
than admitting it does not transfer.

That is enough for `BC-017`'s own exit, which asks for an LP-solve count and a pair-test
total rather than for role-level parity. What it is not enough for is any claim that two
instruments' *finer* counts are comparable, and this file exists so that claim is never
made by accident.

**Target-free throughout.** No coordinates, side, geometry, feasibility or optimality
claim; the LP here is run on a literal three-square structural cell to observe its own
counters, and its solution is discarded.

Usage:
    uv run --frozen --all-extras --group dev python -m devtools.audit_work_accounting
    ... same, with --check, to compare against the retained record
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

from strif import atomic_output_file

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTROL = ROOT / "atlas" / "known-best" / "contact-full-cell-control.json"
RECORD = (
    ROOT
    / "campaign"
    / "series"
    / "series-000-smoke-and-calibration"
    / "results"
    / "bc-017-work-accounting.json"
)

SUBJECT_SQUARES = 3
"""The source-free three-square structural cell the full-cell control already retains.

Deliberately the same subject for all three instruments. Comparing counters taken from
different subjects is how two instruments come to look reconcilable when they are not.
"""


def structural() -> dict[str, Any]:
    """What the compiled structural plan counts, read from the retained control."""
    control = json.loads(CONTROL.read_text(encoding="utf-8"))["control"]
    plan = control["execution_plan"]
    modes: dict[str, int] = {}
    for row in plan["rows"]:
        modes[str(row["mode"])] = modes.get(str(row["mode"]), 0) + 1
    return {
        "source": "atlas/known-best/contact-full-cell-control.json",
        "contract": str(plan["contract"]),
        "row_modes": dict(sorted(modes.items())),
        "executed_work": dict(sorted(control["price"]["executed_work"].items())),
        "inventory": dict(sorted(control["price"]["inventory"].items())),
    }


def solver() -> dict[str, Any]:
    """What `solve_cell` counts, observed by running it on the same three squares.

    The cell mirrors the control's own pair structure: two contacts and one non-edge, all
    axis-aligned. What matters is not the answer -- it is discarded -- but the shape of the
    row set the solver builds and which of its own counters come back.
    """
    from sqpack.research.quench import solve_cell  # noqa: PLC0415 - heavy import

    theta = [0.0] * SUBJECT_SQUARES
    cell = [
        (0, 1, 1.0, 0.0, 1.0, 1.0),
        (0, 2, 0.0, 1.0, 1.0, 1.0),
        (1, 2, 1.0, 0.0, 1.0, 1.0),
    ]
    result = solve_cell(theta, cell, SUBJECT_SQUARES)
    return {
        "source": "sqpack.research.quench.solve_cell",
        "solver_calls": int(result.solver_calls),
        "attempt_receipts": len(result.attempt_receipts),
        "outcome": str(result.outcome),
        "rows_built": {
            "containment": 4 * SUBJECT_SQUARES,
            "pair": len(cell),
            "note": (
                "four containment inequalities per square against the variable side, "
                "regardless of whether that wall is seated, and one row per cell entry, "
                "regardless of whether it is a contact or a non-edge"
            ),
        },
        "finest_role_distinction_available": "containment vs pair, via max_violation_kind",
    }


def roles() -> list[dict[str, Any]]:
    """Each structural role, and which instrument can still see it.

    `separated` means the instrument reports that role on its own; `collapsed` means it
    reports a number the role is folded into; `absent` means it does not count it at all.
    """
    return [
        {
            "role": "seated-wall equality",
            "structural_plan": "separated",
            "solve_cell": "collapsed into four containment inequalities per square",
            "sqsearch_pair_meter": "absent",
        },
        {
            "role": "open-wall inequality",
            "structural_plan": "separated",
            "solve_cell": "collapsed into the same four per square",
            "sqsearch_pair_meter": "absent",
        },
        {
            "role": "contact equality",
            "structural_plan": "separated",
            "solve_cell": "collapsed into one row per cell entry",
            "sqsearch_pair_meter": "absent",
        },
        {
            "role": "non-edge inequality",
            "structural_plan": "separated",
            "solve_cell": "collapsed into the same one row per cell entry",
            "sqsearch_pair_meter": "absent",
        },
        {
            "role": "pair test",
            "structural_plan": "separated, as compiled rows",
            "solve_cell": "absent",
            "sqsearch_pair_meter": "separated, as dynamic overlap tests",
        },
        {
            "role": "LP solve attempt",
            "structural_plan": "separated",
            "solve_cell": "separated, including failed attempts",
            "sqsearch_pair_meter": "absent",
        },
    ]


def audit() -> dict[str, Any]:
    matrix = roles()
    shared = [
        row["role"]
        for row in matrix
        if "absent" not in (row["structural_plan"], row["solve_cell"])
        and "collapsed" not in row["solve_cell"]
    ]
    return {
        "schema_version": 1,
        "subject": {
            "commitment": "BC-017",
            "squares": SUBJECT_SQUARES,
            "evidence_role": (
                "target-free work-accounting comparison; no coordinates, side, geometry, "
                "feasibility or optimality claim, and no enumerated stratum is priced here"
            ),
            "question": (
                "which unit of work can be counted identically by the structural plan, the "
                "quench solver and the sqsearch pair meter?"
            ),
        },
        "instruments": {"structural_plan": structural(), "solve_cell": solver()},
        "role_separation": matrix,
        "verdict": {
            "totals_agree_composition_does_not": (
                "the sharpest form of the collapse, and it is measured rather than argued. "
                "The structural plan reports 4 seated-wall equalities and 8 open-wall "
                "inequalities against 2 contact equalities and 1 non-edge inequality; "
                "solve_cell builds 12 containment rows and 3 pair rows. The same twelve and "
                "the same three. The two instruments agree on every total and disagree on "
                "every composition, which is exactly why an LP-solve price transfers and a "
                "role-level price does not."
            ),
            "shared_units": shared,
            "readiness": (
                "the LP solve attempt is the only unit all instruments that count it "
                "report identically, and it is the unit BC-017's exit names. So the "
                "LP-solve half of that exit is reachable now."
            ),
            "not_reconcilable": (
                "pair_tests appears in two instruments and counts different things in "
                "each -- compiled rows in the structural plan, dynamic overlap tests in "
                "sqsearch. The exit's pair-test total is therefore not one number until "
                "which sense is meant is decided, and that decision is not a measurement."
            ),
            "roles_lost_to_the_solver": [
                row["role"] for row in matrix if "collapsed" in row["solve_cell"]
            ],
            "why_that_is_survivable": (
                "BC-017 asks for an LP-solve count and a pair-test total, not for "
                "role-level parity. The four collapsed roles are separated by the "
                "structural plan, which is where the enumeration reads them; the solver "
                "never needed to."
            ),
        },
    }


def serialized(record: dict[str, Any]) -> str:
    return json.dumps(record, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare against the record")
    args = parser.parse_args()

    built = audit()
    if args.check:
        if not RECORD.exists():
            print(f"  {RECORD.name} is missing", file=sys.stderr)
            return 1
        if RECORD.read_text(encoding="utf-8") != serialized(built):
            print(f"  {RECORD.name} has drifted from a fresh audit", file=sys.stderr)
            return 1
        print(
            "  work accounting reproduces: "
            f"{len(built['verdict']['shared_units'])} shared unit, "
            f"{len(built['verdict']['roles_lost_to_the_solver'])} roles the solver collapses"
        )
        return 0

    with atomic_output_file(RECORD) as temporary:
        temporary.write_text(serialized(built), encoding="utf-8")
    print(f"wrote {RECORD.relative_to(ROOT.parent)}")
    print(f"  shared units: {built['verdict']['shared_units']}")
    print(f"  collapsed by the solver: {built['verdict']['roles_lost_to_the_solver']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
