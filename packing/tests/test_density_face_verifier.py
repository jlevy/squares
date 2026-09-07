"""Hand-set face-depth controls; no retained target candidate is constructed."""

from __future__ import annotations

import json
from dataclasses import replace
from fractions import Fraction

import pytest

from devtools.check_full_size_density_pair_separator import control_family
from devtools.density_face_verifier import (
    Arrangement,
    Facet,
    check_excess_box,
    clip_line,
    facet_probes,
    main,
    normalized_line,
    verify_density,
)
from sqpack.field import NumberField
from sqpack.full_size_density.support_ceiling import (
    BoundaryPointError,
    Support,
    SupportError,
    axis_square,
    necessary_row,
)


def test_edge_and_corner_contacts_do_not_count_as_positive_area_overlap() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    squares = tuple(
        axis_square(q(x), q(y)) for x, y in (("1/2", "1/2"), ("3/2", "1/2"), ("3/2", "3/2"))
    )
    result = verify_density(squares, q(2), (Fraction(1),) * 3)
    assert result.maximum == 1
    assert result.witness is None
    assert result.probes


def test_complete_depth_detects_pair_invisible_triple_and_exact_equal_case() -> None:
    for name, maximum in (
        ("toy-overlap-v1", Fraction(3, 2)),
        ("toy-equal-v1", Fraction(1)),
        ("toy-triple-v1", Fraction(6, 5)),
        ("toy-gap-v1", Fraction(1)),
    ):
        family = control_family(name)
        result = verify_density(
            tuple(entry.square for entry in family.placements),
            family.side,
            tuple(entry.weight for entry in family.placements),
        )
        assert result.maximum == maximum
        assert (result.witness is not None) == (maximum > 1)
        if result.witness is not None:
            check_excess_box(result.family, result.witness)
            assert len(result.witness.members) == (3 if name == "toy-triple-v1" else 2)


def test_rational_sliver_has_a_directly_checked_positive_area_box() -> None:
    family = control_family("toy-narrow-overlap-v1")
    result = verify_density(
        tuple(entry.square for entry in family.placements),
        family.side,
        tuple(entry.weight for entry in family.placements),
    )
    assert result.maximum == Fraction(3, 2)
    box = result.witness
    assert box is not None
    assert 0 < box.radius < Fraction(1, 10**30)
    # Independent axis-aligned oracle checks every corner, not producer forms.
    for sx, sy in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
        x, y = box.point[0] + sx * box.radius, box.point[1] + sy * box.radius
        assert 0 < x < family.side
        assert 0 < y < family.side
        for entry in family.placements:
            xs, ys = zip(*entry.square, strict=True)
            assert min(xs) < x < max(xs)
            assert min(ys) < y < max(ys)
    for altered in (
        replace(box, radius=Fraction()),
        replace(box, radius=Fraction(1)),
        replace(box, excess=Fraction(1)),
        replace(box, members=(box.members[0],) * 2),
    ):
        with pytest.raises(SupportError):
            check_excess_box(family, altered)


def test_degree_eight_rotation_is_ordered_by_field_value_not_coefficients() -> None:
    family = control_family("toy-rotated-algebraic-v1")
    result = verify_density(
        tuple(tuple(reversed(entry.square)) for entry in family.placements),
        family.side,
        tuple(entry.weight for entry in family.placements),
    )
    assert family.side.field.degree == 8
    assert result.maximum == Fraction(3, 2)
    assert result.witness is not None
    check_excess_box(result.family, result.witness)
    for facet in result.arrangement.facets:
        line = result.arrangement.lines[facet.line]
        coordinate = 0 if not line.b.is_zero() else 1
        assert facet.start[coordinate] < facet.end[coordinate]


def test_a_tiny_interior_triple_face_is_not_lost_between_event_lines() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    width = Fraction(1, 10**12)
    squares = tuple(
        axis_square(q(x), q(y))
        for x, y in (
            (Fraction(1, 2), Fraction(1, 2)),
            (Fraction(3, 2) - width, Fraction(1, 2)),
            (Fraction(1, 2), Fraction(3, 2) - width),
        )
    )
    result = verify_density(squares, q(2), (Fraction(2, 5),) * 3)
    assert result.maximum == Fraction(6, 5)
    assert result.witness is not None
    assert len(result.witness.members) == 3
    assert all(1 - width < coordinate < 1 for coordinate in result.witness.point)
    assert result.witness.radius < width / 2


def test_concurrent_crossings_split_every_incident_line_without_duplicate_events() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    rotated = tuple(
        (q(x), q(y)) for x, y in (("1", "1"), ("8/5", "9/5"), ("4/5", "12/5"), ("1/5", "8/5"))
    )
    result = verify_density(
        (axis_square(q("3/2"), q("3/2")), rotated), q(3), (Fraction(1, 2),) * 2
    )
    assert result.maximum == 1
    assert len({(line.a, line.b, line.c) for line in result.arrangement.lines}) == len(
        result.arrangement.lines
    )
    incident = [
        index
        for index, line in enumerate(result.arrangement.lines)
        if line.at((q(1), q(1))).is_zero()
    ]
    assert len(incident) == 4
    for index in incident:
        assert any(
            facet.line == index and (q(1), q(1)) in (facet.start, facet.end)
            for facet in result.arrangement.facets
        )
    for facet in result.arrangement.facets:
        for line in result.arrangement.lines:
            assert line.at(facet.start).sign() * line.at(facet.end).sign() >= 0


def test_coincident_lines_duplicate_geometry_and_zero_weights_do_not_add_depth() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    square = axis_square(q(1), q(1))
    base = verify_density((square,), q(2), (Fraction(1),))
    duplicate = verify_density((square, tuple(reversed(square))), q(2), (Fraction(1),) * 2)
    assert duplicate.maximum == base.maximum == 1
    assert len(duplicate.family.placements) == 1
    assert duplicate.arrangement == base.arrangement
    # This zero-weight boundary passes through a retained base probe.
    point = base.probes[0].point
    x = point[0] if point[0] <= 1 else point[0] - 1
    zero_square = axis_square(x + Fraction(1, 2), q(1))
    with_zero = verify_density((square, zero_square), q(2), (Fraction(1), Fraction()))
    assert with_zero.maximum == base.maximum
    assert tuple(probe.point for probe in with_zero.probes) == tuple(
        probe.point for probe in base.probes
    )
    with pytest.raises(BoundaryPointError):
        necessary_row(Support(q(2), ((square,), (zero_square,))), point)
    all_zero = verify_density((square,), q(2), (Fraction(),))
    assert all_zero.maximum == 0
    assert len(all_zero.arrangement.lines) == 4
    assert len(all_zero.probes) == 4
    with pytest.raises(SupportError, match="inconsistent"):
        verify_density((square, square), q(2), (Fraction(1), Fraction(1, 2)))


def test_clipping_distinguishes_empty_point_and_wall_segment() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    assert clip_line(normalized_line(q(1), q(1), q(-1)), q(2)) == ()
    assert clip_line(normalized_line(q(1), q(1), q(0)), q(2)) == ((q(0), q(0)),)
    wall = normalized_line(q(0), q(-2), q(0))
    assert clip_line(wall, q(2)) == ((q(0), q(0)), (q(2), q(0)))
    assert wall == normalized_line(q(0), q(1), q(0))
    with pytest.raises(SupportError, match="nonzero"):
        normalized_line(q(0), q(0), q(1))


def test_unsplit_concurrent_crossing_and_missing_adjacent_side_are_refused() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    horizontal = normalized_line(q(0), q(1), q(1))
    vertical = normalized_line(q(1), q(0), q(1))
    facet = Facet(0, (q(0), q(1)), (q(2), q(1)))
    with pytest.raises(SupportError, match="unsplit"):
        facet_probes(Arrangement((horizontal, vertical), (facet,), ()), facet, q(2))
    wall = normalized_line(q(0), q(1), q(0))
    wall_facet = Facet(0, (q(0), q(0)), (q(2), q(0)))
    with pytest.raises(SupportError, match="every contained adjacent side"):
        facet_probes(Arrangement((wall,), (wall_facet,), ()), wall_facet, q(2))
    with pytest.raises(SupportError, match="zero-length"):
        facet_probes(Arrangement((horizontal,), (), ()), replace(facet, end=facet.start), q(2))


def test_toy_cli_has_no_candidate_dispatch(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(("triple",)) == 0
    packet = json.loads(capsys.readouterr().out)
    assert packet["maximum"] == "6/5"
    assert packet["scope"] == "complete-a.e.-control"
    with pytest.raises(SystemExit) as failure:
        main(("--target",))
    assert failure.value.code == 2
