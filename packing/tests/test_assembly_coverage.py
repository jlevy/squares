"""Seventeen records carry a certificate and thirteen carry a typed limitation.

`BC-019`'s exit asks for a versioned contact-assembly contract with sliding degrees of
freedom, complexity cost, canonical ties, **and per-record certificates or typed
limitations**. The contract carried the first three and never the fourth.

The assertions worth having here are about the two things the coverage pass declines to
compute rather than about the counts. `internal_slide_dof` is zero by the `rigid-lattice`
primitive's own semantics and not by evaluating a rank, and the contact normal axis is
absent from the census and is not reconstructed from lattice deltas. Both would be easy to
fill in and both would be assumptions dressed as measurements.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from devtools.certify_assembly_coverage import (
    HORIZON,
    RECORD,
    RIGID_LATTICE,
    coverage,
    serialized,
)

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR = ROOT / "atlas/known-best/contact-assembly-grammar.yaml"


def _record() -> dict:
    return json.loads(RECORD.read_text(encoding="utf-8"))


def test_every_record_under_the_horizon_gets_one_or_the_other() -> None:
    """Neither a gap nor a record answering twice."""
    built = _record()
    covered = [item["n"] for item in built["certified"]] + [
        item["n"] for item in built["limited"]
    ]

    assert sorted(covered) == list(range(1, HORIZON + 1))
    assert len(covered) == len(set(covered))
    assert built["totals"] == {"records": 30, "certified": 17, "limited": 13}


def test_the_slide_freedom_is_zero_by_semantics_and_says_so() -> None:
    """A number with a reason attached, because the reason is the load-bearing part.

    The contract's `D = 2m - rank(A_normal) - 2` prices a contact scaffold, whose tangential
    offsets stay LP variables. A rigid lattice has fixed integer offsets in one fitted
    orientation and so has no internal slide at all. Reporting a rank here would be pricing
    a primitive this corpus does not contain.
    """
    for item in _record()["certified"]:
        complexity = item["complexity"]
        assert complexity["internal_slide_dof"] == 0
        assert "rigid-lattice primitive's semantics" in complexity["internal_slide_dof_basis"]
        assert "not by evaluating" in complexity["internal_slide_dof_basis"]


def test_the_normal_axis_is_declared_missing_rather_than_inferred() -> None:
    """The gap the contract's own `label_fields` opens, stated instead of filled."""
    unfilled = _record()["unfilled_contract_fields"]
    fields = {item["field"] for item in unfilled}

    assert "mandatory contact graph with normal axis and sign" in fields
    reason = next(
        item["why"] for item in unfilled if item["field"].startswith("mandatory contact")
    )
    assert "assumption about the fit" in reason


def test_every_unexpressed_component_is_untilted() -> None:
    """`X-008`'s finding, seen again from the record that has to act on it.

    The missing grammar move is a primitive for axis-aligned polyominoes. If a tilted
    component ever appeared here, that sentence would be wrong and the contract would be
    pointing at the wrong extension.
    """
    for item in _record()["limited"]:
        components = item["limitation"]["components"]
        assert components
        for component in components:
            assert component["tilted"] is False, (item["n"], component)
            assert component["shape"] not in RIGID_LATTICE
        assert "not about tilted assemblies" in item["limitation"]["missing_move"]


def test_the_contract_points_at_this_record_and_agrees_with_it() -> None:
    """The contract and the corpus cannot drift into disagreeing silently."""
    grammar = yaml.safe_load(GRAMMAR.read_text(encoding="utf-8"))["grammar"]
    block = grammar["per_record_coverage"]

    assert grammar["version"] == "contact-assembly-v2-draft"
    assert block["horizon"] == HORIZON
    assert block["certificate_record"].endswith("bc-019-assembly-coverage.json")
    assert "certify_assembly_coverage --check" in block["replay"]
    assert len(block["unfilled_here"]) == len(_record()["unfilled_contract_fields"])


def test_no_verdict_is_emitted_anywhere_in_the_record() -> None:
    """Descriptive is a commitment. A table of certificates reads like a conclusion."""
    built = _record()

    assert "H-044 is untouched" in built["subject"]["emits_no_verdict"]
    for item in built["limited"]:
        assert "not a refutation" in item["limitation"]["not_a_verdict"]


def test_the_record_round_trips() -> None:
    assert RECORD.read_text(encoding="utf-8") == serialized(coverage())
