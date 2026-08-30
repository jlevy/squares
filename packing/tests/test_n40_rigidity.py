"""`n = 40` is infinitesimally flexible, and the witness is what has to be protected.

This is a first-party finding against a source that annotates the packing "Rigid.", so the
assertions are written to fail loudly if the witness ever stops being one. Three things
have to hold together and each is checked from the pose rather than read back from the
record: the motion is nonzero, it has exactly zero gap rate on every contact that holds in
all branches, and every pair that touches at a corner still has an axis that separates
along it. Drop any one and the vector stops being a motion.

The other assertion worth its place is the negative one. An assessor that intersects the
corner disjunctions reports all 120 coordinates pinned -- that is, reports this pose rigid.
`D-391` is therefore a defect with a measured consequence rather than a counterfactual one,
and the test says so, because a future "simplification" that reinstates the intersection
would otherwise look like it agreed with the catalogue.
"""

from __future__ import annotations

import json

import pytest

from devtools.assess_n5_rigidity import (
    DOF,
    active_contacts,
    constraint_rows,
    contact_axes,
    disjunctive_pairs,
    gap_rate,
    incident_contacts,
    nullspace,
    separating,
)
from devtools.assess_n40_rigidity import (
    OUT,
    assess,
    axis_groups,
    find_witness,
    load_pose,
    single_axis_contacts,
)


def _record() -> dict:
    return json.loads(OUT.read_text(encoding="utf-8"))


def test_the_witness_is_a_motion_checked_from_the_pose() -> None:
    """The finding, re-derived. Nothing here trusts the record's copy of it."""
    pose = load_pose()
    contacts = active_contacts(pose)
    found = find_witness(pose, contacts)
    assert found is not None
    motion, selection = found

    assert any(value.sign() != 0 for value in motion)

    single = constraint_rows(pose, single_axis_contacts(pose, contacts))
    assert len(single) == 248
    assert all(gap_rate(row, motion).sign() == 0 for row in single)

    groups = axis_groups(pose, contacts)
    assert len(groups) == 42
    for pair, group in groups.items():
        rows = constraint_rows(pose, group[selection[pair]])
        assert all(gap_rate(row, motion).sign() >= 0 for row in rows), pair


def test_only_the_tilted_block_moves() -> None:
    """Sixteen squares turning together, and no frame square displaced at all.

    The shape of the motion is the reason every earlier instrument missed it: the
    translation-escape screen decides one square translating, and this is sixteen turning.
    """
    witness = _record()["witness"]

    assert witness["squares_that_turn"] == list(range(24, 40))
    assert witness["squares_that_move"] == list(range(24, 40))
    assert witness["frame_squares_move"] == []


def test_intersecting_the_disjunctions_reports_the_pose_rigid() -> None:
    """`D-391`'s cost, measured on this pose rather than argued in the abstract."""
    reported = _record()["what_an_intersecting_assessor_reports"]

    assert reported["pinned"] == 120
    assert reported["uncertified"] == []
    assert "which is false" in reported["verdict_it_would_report"]

    verification = _record()["witness"]["verification"]
    assert verification["rows_violated_if_the_disjunctions_are_intersected"] == 42
    assert verification["disjunctive_pairs_with_an_admissible_axis"] == 42


def test_the_null_space_is_what_makes_the_candidate_exact() -> None:
    """No rounding anywhere: a null vector is in the cone by construction.

    A direction proposed by a linear program has to be rationalized before it can be
    checked in the field, and a rationalized vertex generally stops satisfying the system
    it came from -- which is what made the first search for this witness find nothing.
    """
    pose = load_pose()
    contacts = active_contacts(pose)
    rows = constraint_rows(pose, single_axis_contacts(pose, contacts))
    basis = nullspace(pose, rows)

    assert len(basis) == 5
    for vector in basis:
        assert all(gap_rate(row, vector).sign() == 0 for row in rows)


def test_flexibility_is_not_promoted_to_not_rigid() -> None:
    """The distinction the record exists to keep.

    An infinitesimal flex is a first-order object. Along this one the gaps curve shut at
    order `t^2`, so it is not a motion, and moving `n = 40` to `not-rigid` would assert
    something nobody has shown.
    """
    built = _record()

    assert built["verdict"]["infinitesimally_rigid"] is False
    assert "stays undetermined" in built["subject"]["promotes_nothing"]
    assert "not a motion" in built["subject"]["promotes_nothing"]
    assert "local rigidity" in built["verdict"]["what_is_not_claimed"]
    assert "t^2" in built["witness"]["second_order_behaviour"]


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


def test_the_witness_turns_every_block_square_at_the_same_rate() -> None:
    """What the motion is, geometrically: the block's squares counter-rotating in place."""
    pose = load_pose()
    found = find_witness(pose, active_contacts(pose))
    assert found is not None
    motion, _ = found

    spins = {index: motion[index * DOF + 2] for index in range(24, 40)}
    first = spins[24]
    assert first.sign() != 0
    for index, spin in spins.items():
        assert (spin - first).sign() == 0, index
    for index in range(24):
        assert motion[index * DOF + 2].sign() == 0


@pytest.mark.exhaustive_exact
def test_the_record_round_trips() -> None:
    """Minutes: the intersecting-assessor section runs 240 linear programs."""
    assert _record() == assess()
