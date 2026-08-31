"""The n=5 packing flexes in exactly one direction, and that direction curves shut.

`BC-049` asked whether the packings the catalogue annotates "Rigid." are rigid on evidence
of our own. At n = 5 the answer is sharper than the word: fourteen of the fifteen degrees
of freedom are pinned by exact Farkas certificates, the fifteenth -- rotation of the middle
square about its own centre -- is free at first order because no contact mentions it, and
that fifteenth is then refused at second order by a verified self-stress.

These assertions exist because that is a surprising result to leave to a generated record.
A future change to the pose, the contact enumeration or the linearization that moved the
cone's dimension, or that softened the obstruction into a failed search, would otherwise
change a published claim silently.
"""

from __future__ import annotations

import pytest

from devtools.assess_n5_rigidity import (
    active_contacts,
    assess,
    constraint_rows,
    contact_axes,
    incident_contacts,
    load_pose,
    obstruction,
    propose_self_stress,
    propose_weights,
    rationalize,
    row_scales,
    second_order_terms,
    unconstrained,
    variable_names,
    verify_self_stress,
    verify_weights,
)


def test_the_contact_inventory_is_what_the_geometry_says() -> None:
    """Four corner squares against two walls each, and four corners on the middle square.

    The middle square touches no wall: its extreme coordinate is `s/2 + sqrt(2)/2`, about
    `2.06`, inside a container of side `2.71`. If that ever changes, every row below is
    describing a different packing.
    """
    pose = load_pose()
    contacts = active_contacts(pose)
    assert sum(1 for c in contacts if c.kind == "wall") == 16
    assert sum(1 for c in contacts if c.kind == "pair") == 4
    assert {c.host for c in contacts if c.kind == "pair"} == {4}
    assert not [c for c in contacts if c.kind == "wall" and c.moving == 4]


def test_the_middle_square_rotation_is_absent_from_every_constraint() -> None:
    """The finding, in its sharpest form.

    Each corner square's inner corner rests on the foot of the perpendicular from the middle
    square's centre, so `(p - c) . n_perp` is identically zero and the rotation drops out of
    all four pair constraints. It is not that the search for a bound failed; the coefficient
    is exactly zero in all twenty rows.
    """
    pose = load_pose()
    rows = rationalize(pose, constraint_rows(pose, active_contacts(pose)))
    names = variable_names(pose.count)
    free = [names[index] for index in range(len(names)) if unconstrained(rows, index)]
    assert free == ["w4"]


def test_every_other_coordinate_is_pinned_by_an_exact_certificate() -> None:
    """A failed search is not a proof; a verified Farkas combination is.

    For each pinned coordinate the record carries non-negative row weights summing to `+e_k`
    and to `-e_k`. Re-checking them here in the field is what makes the pinning evidence:
    the weights are proposed in floating point and would otherwise never be confirmed.
    """
    pose = load_pose()
    contacts = active_contacts(pose)
    rows = rationalize(pose, constraint_rows(pose, contacts))
    names = variable_names(pose.count)
    result = assess()
    pinned = {row["coordinate"] for row in result["first_order_cone"]["pinned"]}

    assert pinned == set(names) - {"w4"}
    assert result["first_order_cone"]["uncertified"] == []
    assert len(pinned) == 14

    # Re-derive one certificate from scratch rather than trusting the record's own copy.
    index = names.index("vx0")
    for sign in (1, -1):
        weights = propose_weights(rows, index, sign)
        assert weights is not None
        assert verify_weights(pose, rows, weights, index, sign)


def test_the_packing_is_not_infinitesimally_rigid_and_the_record_says_so() -> None:
    """The verdict must not be rounded to the nearest familiar word.

    "Not infinitesimally rigid" is not "not rigid": no motion has been exhibited, and the
    first-order direction is not a motion until a continuation realizes it. The record has
    to keep that distinction, because it is the whole difference between a finding and an
    overclaim.
    """
    result = assess()
    assert result["verdict"]["infinitesimally_rigid"] is False
    assert result["first_order_cone"]["dimension"] == 1
    assert "Local rigidity itself" in result["scope"]["not_established"]


def test_the_certificate_rests_on_the_exact_pose_not_the_witness() -> None:
    """The retained decimal witness is infeasible at the scale this argument works at.

    Its middle-square centre sits `2.4e-30` off the diagonal, which the escape screen
    records as a negative pair separation. Certifying rigidity of an infeasible pose would
    be worse than not certifying anything.
    """
    result = assess()
    assert result["subject"]["pose"] == "cases.gobel5.packing.build"
    assert "infeasible" in result["subject"]["why_not_the_witness"]


def test_the_one_free_direction_curves_into_the_obstacle() -> None:
    """The second-order term, which the first-order question cannot reach.

    Turning the middle square moves each contact off the midpoint of the edge it rests on,
    and the midpoint is the nearest point of that edge line to the centre. So the gap can
    only shorten, at every one of the four pair contacts and at neither sign of the turn.
    The walls contribute nothing because the middle square touches none of them.
    """
    pose = load_pose()
    contacts = active_contacts(pose)
    names = variable_names(pose.count)
    unit = [
        pose.field.rational(1 if position == names.index("w4") else 0)
        for position in range(len(names))
    ]
    terms = second_order_terms(pose, contacts, unit)

    half = pose.field.rational(1) / pose.field.rational(2)
    curved = [
        (contact, term)
        for contact, term in zip(contacts, terms, strict=True)
        if term.sign() != 0
    ]

    assert len(curved) == 4
    assert {contact.kind for contact, _ in curved} == {"pair"}
    assert all((term + half).sign() == 0 for _, term in curved)
    assert all(
        term.sign() == 0
        for contact, term in zip(contacts, terms, strict=True)
        if contact.kind == "wall"
    )


def test_the_obstruction_is_a_verified_self_stress_not_a_failed_search() -> None:
    """What makes the refusal evidence rather than an absence.

    A second-order correction `y` would have to satisfy `A y >= -q`. Non-negative weights
    with `w . A = 0` make that impossible: `w . (A y)` is zero for every `y`, while
    `-w . q` is positive. Re-checking the weights in the field here is what turns the
    linear program's proposal into the certificate.
    """
    pose = load_pose()
    contacts = active_contacts(pose)
    raw = constraint_rows(pose, contacts)
    rows = rationalize(pose, raw)
    scales = row_scales(pose, raw)
    names = variable_names(pose.count)
    unit = [
        pose.field.rational(1 if position == names.index("w4") else 0)
        for position in range(len(names))
    ]
    scaled = [
        term * scale
        for term, scale in zip(second_order_terms(pose, contacts, unit), scales, strict=True)
    ]

    certificate = obstruction(pose, rows, scaled, contacts)
    assert certificate is not None
    assert certificate["self_stress"]

    # Re-derive it rather than trusting the record, and check the two halves separately.
    support = [position for position, value in enumerate(scaled) if value.sign() < 0]
    weights = propose_self_stress(rows, support)
    assert weights is not None
    assert verify_self_stress(pose, rows, weights)
    total = pose.field.rational(0)
    for weight, value in zip(weights, scaled, strict=True):
        if weight:
            total = total + value * pose.field.rational(weight)
    assert total.sign() < 0


def test_the_record_says_second_order_rigid_and_stops_there() -> None:
    """Second-order rigidity is not local rigidity, and the record must not blur them.

    Every twice-differentiable arc leaving this pose with a nonzero derivative is refused.
    An arc whose derivative vanishes is not, and the semi-algebraic argument that would
    rule those out is cited in the scope rather than run. Recording the stronger word here
    would be exactly the promotion `D-354` exists to prevent, one level up.
    """
    result = assess()
    assert result["verdict"]["infinitesimally_rigid"] is False
    assert result["verdict"]["second_order_rigid"] is True
    assert result["second_order"]["every_first_order_flex_is_obstructed"] is True
    assert "Local rigidity itself" in result["scope"]["not_established"]
    assert "fixed side" in result["scope"]["not_established"]


def test_a_mixed_row_is_refused_rather_than_answered() -> None:
    """The limitation that would otherwise report a motion that is not there.

    `rationalize` scales a row by `sqrt 2` when every entry is a pure multiple of it. That
    dichotomy is exhaustive at `n = 5` and not in general: Göbel's `n = 40` construction,
    exact in the same field, has 184 of its 400 contact rows carrying both a rational and a
    `sqrt 2` part -- 296 of 608 when the measurement was taken, before `D-390` removed the
    incidences that are not contacts. No positive scalar rationalizes such a row, so the
    rational-weight search would answer a different system -- and before this guard it did,
    reporting all 120 of that pose's coordinates unpinned, which reads as a motion.
    """
    from cases.gobel40.packing import build  # noqa: PLC0415 - heavy exact construction
    from devtools.assess_n5_rigidity import MixedRowError, Pose  # noqa: PLC0415

    squares, side, field = build()
    pose = Pose(field, side, tuple(tuple(square) for square in squares))

    with pytest.raises(MixedRowError, match="both a rational and a sqrt"):
        rationalize(pose, constraint_rows(pose, active_contacts(pose)))


def test_the_n5_dichotomy_really_is_exhaustive_there() -> None:
    """Why the limitation went unnoticed: at `n = 5` there is nothing to notice."""
    pose = load_pose()
    rows = constraint_rows(pose, active_contacts(pose))

    mixed = [
        row
        for row in rows
        if any(entry.coeffs[0] != 0 for entry in row)
        and any(entry.coeffs[1] != 0 for entry in row)
    ]
    assert mixed == []


def test_an_incidence_is_not_a_contact() -> None:
    """`D-390`: a corner on an edge's endpoint constrains nothing, and 208 rows said it did.

    Squares 0 and 6 of the `n = 40` pose are edge-to-edge neighbours at `(1/2, 1/2)` and
    `(3/2, 1/2)`, separated by the line `x = 1` and by nothing else. The first square's
    corners `(1, 0)` and `(1, 1)` land on the endpoints of the second's bottom and top
    edges, so the raw incidence relation reports contacts on the vertical axis too --
    asserting that a square free to move down may not.
    """
    from cases.gobel40.packing import build  # noqa: PLC0415 - heavy exact construction
    from devtools.assess_n5_rigidity import Pose, separating  # noqa: PLC0415

    squares, side, field = build()
    pose = Pose(field, side, tuple(tuple(square) for square in squares))

    incident = [one for one in incident_contacts(pose) if one.kind == "pair"]
    contacts = [one for one in active_contacts(pose) if one.kind == "pair"]
    assert (len(incident), len(contacts)) == (560, 352)

    between = [one for one in incident if {one.moving, one.host} == {0, 6}]
    normals: set[int] = set()
    kept = 0
    for one in between:
        assert one.host is not None and one.edge is not None
        if separating(pose, one.host, one.edge, one.moving):
            kept += 1
            normals.add(pose.normal(one.host, one.edge)[1].sign())
    assert kept < len(between)
    assert normals == {0}, "the surviving rows are horizontal, which is the only real axis"


def test_n5_has_no_merely_incident_row() -> None:
    """Why `D-390` went unnoticed, and why the `n = 5` result is unaffected."""
    pose = load_pose()

    assert incident_contacts(pose) == active_contacts(pose)


def test_a_disjunctive_pose_is_refused_rather_than_answered() -> None:
    """`D-391`: two squares touching at a corner may separate either way, not both ways.

    Intersecting the two half-spaces is a subset of each branch, so the cone comes out too
    small and the pose reads as more rigid than it is. The assessor refuses rather than
    answering, because the answer would be wrong in the flattering direction.
    """
    from cases.gobel40.packing import build  # noqa: PLC0415 - heavy exact construction
    from devtools.assess_n5_rigidity import (  # noqa: PLC0415
        DisjunctiveContactError,
        Pose,
        disjunctive_pairs,
        require_intersection_semantics,
    )

    squares, side, field = build()
    pose = Pose(field, side, tuple(tuple(square) for square in squares))
    contacts = active_contacts(pose)

    assert len(disjunctive_pairs(pose, contacts)) == 42
    assert len(contact_axes(pose, contacts)) == 98

    with pytest.raises(DisjunctiveContactError, match="two axes at once"):
        require_intersection_semantics(pose, contacts)


def test_n5_has_no_disjunctive_pair() -> None:
    """The exemption `X-007` argued in prose, as a check.

    Each of the four contacts is a corner on the *interior* of a middle-square edge, so one
    axis holds each pair and the tangent cone really is an intersection there.
    """
    from devtools.assess_n5_rigidity import disjunctive_pairs  # noqa: PLC0415

    pose = load_pose()
    contacts = active_contacts(pose)

    assert disjunctive_pairs(pose, contacts) == []
    assert len(contact_axes(pose, contacts)) == 4


def test_the_ordered_field_search_reaches_what_the_restricted_cone_does() -> None:
    """`certify` runs two searches, and the cheap one must not be silently doing nothing.

    Bounding `p` and `q` below by zero refuses positive weights like `3 - sqrt 2`; leaving
    them free and ordering by `p + sqrt(2) q >= 0` is complete over the field but
    unbounded, and loses certificates to conditioning. Each reaches what the other cannot,
    so the assertion is that both are live at `n = 5`.
    """
    from devtools.assess_n5_rigidity import (  # noqa: PLC0415
        certify,
        propose_field_weights,
        verify_field_weights,
    )

    pose = load_pose()
    rows = constraint_rows(pose, active_contacts(pose))
    names = variable_names(pose.count)

    restricted = 0
    for index, name in enumerate(names):
        if unconstrained(rows, index):
            continue
        assert certify(pose, rows, index, 1) is not None, name
        weights = propose_field_weights(pose, rows, index, 1, ordered=False)
        if weights is not None and verify_field_weights(pose, rows, weights, index, 1):
            restricted += 1
    assert restricted == 14, "the cheap cone carries n=5 on its own"
