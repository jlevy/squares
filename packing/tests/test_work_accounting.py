"""The two instruments agree on every total and disagree on every composition.

`BC-017` asks whether a stratum can be priced in counted LP solves, and its own note names
the obstruction: `solve_cell` collapses the seated-wall and contact/non-edge roles the
structural plan separates. That is true and it is not the whole shape of it.

Measured on the same three-square subject, the structural plan reports 4 seated-wall
equalities and 8 open-wall inequalities against 2 contact equalities and 1 non-edge
inequality; `solve_cell` builds 12 containment rows and 3 pair rows. **The same twelve and
the same three.** The information that goes missing is entirely composition, and that is
exactly why an LP-solve price transfers between them and a role-level price does not.

The assertion below that matters most is the one holding the two apart: if a future change
made `solve_cell` report role-level counts, the audit's verdict would be wrong in the
generous direction, and a price that does not transfer would start looking like one that
does.
"""

from __future__ import annotations

import json

from devtools.audit_work_accounting import RECORD, audit, roles, serialized


def _record() -> dict:
    return json.loads(RECORD.read_text(encoding="utf-8"))


def test_the_totals_agree_exactly() -> None:
    """The measurement the verdict rests on, taken from the record rather than quoted."""
    built = _record()
    modes = built["instruments"]["structural_plan"]["row_modes"]
    rows = built["instruments"]["solve_cell"]["rows_built"]

    walls = modes["seated-wall-equality"] + modes["open-wall-inequality"]
    pairs = modes["contact-equality"] + modes["nonedge-inequality"]

    assert walls == rows["containment"] == 12
    assert pairs == rows["pair"] == 3


def test_the_only_shared_unit_is_the_lp_solve_attempt() -> None:
    """`BC-017`'s own unit, and the only one that survives all three vocabularies."""
    verdict = _record()["verdict"]

    assert verdict["shared_units"] == ["LP solve attempt"]
    assert sorted(verdict["roles_lost_to_the_solver"]) == [
        "contact equality",
        "non-edge inequality",
        "open-wall inequality",
        "seated-wall equality",
    ]


def test_the_pair_test_counter_is_declared_not_reconcilable() -> None:
    """The trap: one name, two meanings, in two instruments that both report it.

    Compiled rows in the structural plan; dynamic overlap tests in sqsearch. Calling the
    exit's "pair-test total" satisfied by either would be a category error, so the record
    says the number is not one number until someone decides which sense is meant.
    """
    verdict = _record()["verdict"]

    assert "counts different things" in verdict["not_reconcilable"]
    assert "not a measurement" in verdict["not_reconcilable"]

    pair = next(row for row in roles() if row["role"] == "pair test")
    assert pair["structural_plan"] != pair["sqsearch_pair_meter"]
    assert pair["solve_cell"] == "absent"


def test_the_solver_still_cannot_see_the_roles() -> None:
    """The guard against the verdict quietly becoming too generous.

    If `solve_cell` ever gained role-level counters this fails, which is the right time to
    revisit the verdict rather than the moment someone assumes it.
    """
    solver = _record()["instruments"]["solve_cell"]

    assert solver["finest_role_distinction_available"] == (
        "containment vs pair, via max_violation_kind"
    )
    for row in roles():
        if row["role"] in {"seated-wall equality", "contact equality"}:
            assert "collapsed" in row["solve_cell"]


def test_the_audit_claims_nothing_about_a_packing() -> None:
    """Target-free is what makes this runnable before the semantics are frozen."""
    subject = _record()["subject"]

    assert "no coordinates, side, geometry" in subject["evidence_role"]
    assert "no enumerated stratum is priced here" in subject["evidence_role"]


def test_the_record_round_trips() -> None:
    assert RECORD.read_text(encoding="utf-8") == serialized(audit())
