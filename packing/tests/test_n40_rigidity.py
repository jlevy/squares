"""`n = 40` is bracketed, not decided, and the bracket is the thing to protect.

The interesting failure mode for this record is not drift in a number. It is someone
reading one side of the bracket as a verdict. The lower model's cone is trivial because it
imposes *more* than the geometry does, and that is the absence of a cheap flex rather than
rigidity; the upper model leaves 64 coordinates uncertified because it imposes *less*, and
those are not motions. Either half quoted alone says something false.

So the assertions below are mostly about the relationship between the two models -- that
they are nested the right way round, that neither is empty, and that the verdict stays
`None` while they disagree.
"""

from __future__ import annotations

import json

import pytest

from devtools.assess_n5_rigidity import (
    active_contacts,
    contact_axes,
    disjunctive_pairs,
    incident_contacts,
    separating,
)
from devtools.assess_n40_rigidity import OUT, assess, load_pose, relaxed_contacts


def _record() -> dict:
    return json.loads(OUT.read_text(encoding="utf-8"))


def test_the_verdict_is_withheld_while_the_models_disagree() -> None:
    """The assertion that stops half a bracket becoming a claim."""
    verdict = _record()["verdict"]

    assert verdict["decided"] is False
    assert verdict["infinitesimally_rigid"] is None
    assert "bracketed and not decided" in verdict["claim"]
    assert "2^42" in verdict["what_would_decide_it"]


def test_the_two_models_are_nested_the_right_way_round() -> None:
    """Upper contains every branch, lower is contained in every branch.

    Fewer rows can only pin fewer coordinates, so the upper model must be the smaller row
    set and the weaker result. If that inverted, the labels would be backwards and both
    soundness arguments with them.
    """
    bracket = _record()["bracket"]
    upper, lower = bracket["upper_model"], bracket["lower_model"]

    assert upper["rows"] < lower["rows"]
    assert upper["pinned"] < lower["pinned"]
    assert lower["pinned"] == 120
    assert upper["pinned"] == 56
    assert len(upper["uncertified"]) == 64


def test_the_relaxed_rows_really_are_a_subset() -> None:
    """Derived from the pose rather than read from the record, because it is the premise.

    "Pinned in the upper model implies pinned in every branch" holds only if every branch's
    row set contains the upper model's. That is a fact about contact selection, so it is
    checked against the geometry.
    """
    pose = load_pose()
    contacts = active_contacts(pose)
    relaxed = relaxed_contacts(pose, contacts)

    assert set(relaxed) < set(contacts)
    disjunctive = set(disjunctive_pairs(pose, contacts))
    for contact in relaxed:
        if contact.kind == "pair":
            assert frozenset((contact.moving, contact.host)) not in disjunctive


def test_the_contact_model_is_measured_not_assumed() -> None:
    """`D-390` and `D-391` in numbers, taken from the pose."""
    pose = load_pose()
    incident = incident_contacts(pose)
    contacts = active_contacts(pose)

    assert len(incident) == 608
    assert len(contacts) == 400
    assert len(disjunctive_pairs(pose, contacts)) == 42
    assert len(contact_axes(pose, contacts)) == 98

    dropped = [one for one in incident if one not in set(contacts)]
    assert len(dropped) == 208
    assert all(one.kind == "pair" for one in dropped), "no wall row is ever dropped"
    for one in dropped:
        assert one.host is not None and one.edge is not None
        assert not separating(pose, one.host, one.edge, one.moving)


def test_the_field_is_not_the_obstruction() -> None:
    """`D-388` named the mixed rows; the search that answers them exists and this is not it.

    Worth asserting because the record's whole point is that the blocker moved. A future
    reader finding `n = 40` undecided should not go and rebuild the ordered-field search.
    """
    verdict = _record()["verdict"]

    assert "the field" in verdict["what_is_not_the_obstruction"]
    assert "reproduces n = 5" in verdict["what_is_not_the_obstruction"]


def test_nothing_here_promotes_anything() -> None:
    subject = _record()["subject"]

    assert "stays undetermined" in subject["promotes_nothing"]
    assert "not a property" in subject["promotes_nothing"]


@pytest.mark.exhaustive_exact
def test_the_record_round_trips() -> None:
    """Three minutes: 240 linear programs, each proposal re-decided exactly in the field."""
    assert _record() == assess()
