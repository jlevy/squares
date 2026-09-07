"""Hand-set open-slab controls; no Trump source or target candidate is constructed."""

from __future__ import annotations

import json
from dataclasses import replace
from fractions import Fraction
from itertools import pairwise
from typing import cast

import pytest

from devtools import density_slab_verifier as reader
from devtools.check_full_size_density_pair_separator import control_family
from devtools.density_slab_verifier import verify_density_slabs
from sqpack.field import NumberField
from sqpack.full_size_density.support_ceiling import Square, SupportError, axis_square


def test_touching_unit_squares_have_depth_one_on_open_bands() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    squares = tuple(
        axis_square(q(x), q(y)) for x, y in (("1/2", "1/2"), ("3/2", "1/2"), ("3/2", "3/2"))
    )
    result = verify_density_slabs(squares, q(2), (Fraction(1),) * 3)
    assert result.maximum == 1
    assert result.x_events == (q(0), q(1), q(2))
    assert len(result.slabs) == 2
    assert sum(slab.bands for slab in result.slabs) == 4


def test_a_thin_triple_face_produces_a_directly_checkable_excess_box() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    width = Fraction(1, 10**30)
    squares = tuple(
        axis_square(q(x), q(y))
        for x, y in (
            (Fraction(1, 2), Fraction(1, 2)),
            (Fraction(3, 2) - width, Fraction(1, 2)),
            (Fraction(1, 2), Fraction(3, 2) - width),
        )
    )
    weights = (Fraction(2, 5),) * 3
    result = verify_density_slabs(squares, q(2), weights)
    assert result.maximum == Fraction(6, 5)
    witness = result.witness
    assert witness is not None
    assert witness.excess == Fraction(1, 5)
    assert len(witness.members) == 3
    assert 0 < witness.radius < width / 2
    reader.check_witness(squares, q(2), weights, witness)
    for sx, sy in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
        x, y = witness.point[0] + sx * witness.radius, witness.point[1] + sy * witness.radius
        for square in squares:
            xs, ys = zip(*square, strict=True)
            assert min(xs) < x < max(xs)
            assert min(ys) < y < max(ys)
    for altered in (
        replace(witness, radius=Fraction()),
        replace(witness, radius=Fraction(1)),
        replace(witness, excess=Fraction(1)),
        replace(witness, members=(0, 0)),
        replace(witness, members=(-1, 0)),
        replace(witness, members=(0, 99)),
        replace(witness, members=(1, 0)),
        replace(witness, members=(True,)),
        replace(witness, members=()),
        replace(witness, point=(q(0), q(0))),
        replace(witness, radius=cast(Fraction, 0.1)),
        replace(witness, excess=cast(Fraction, True)),  # noqa: FBT003 -- invalid input control
    ):
        with pytest.raises(SupportError):
            reader.check_witness(squares, q(2), weights, altered)


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("toy-overlap-v1", Fraction(3, 2)),
        ("toy-edge-v1", Fraction(1)),
        ("toy-corner-v1", Fraction(1)),
        ("toy-gap-v1", Fraction(1)),
        ("toy-equal-v1", Fraction(1)),
        ("toy-triple-v1", Fraction(6, 5)),
        ("toy-narrow-overlap-v1", Fraction(3, 2)),
        ("toy-algebraic-v1", Fraction(3, 2)),
        ("toy-rotated-algebraic-v1", Fraction(3, 2)),
    ],
)
def test_declared_non_target_controls(name: str, expected: Fraction) -> None:
    family = control_family(name)
    squares = tuple(entry.square for entry in family.placements)
    weights = tuple(entry.weight for entry in family.placements)
    result = verify_density_slabs(squares, family.side, weights)
    assert result.maximum == expected
    assert all(left < right for left, right in pairwise(result.x_events))
    assert (result.witness is not None) == (expected > 1)
    if result.witness is not None:
        reader.check_witness(squares, family.side, weights, result.witness)
    if name == "toy-rotated-algebraic-v1":
        # Sorting coefficient tuples would not order these real x-coordinates.
        assert list(result.x_events) != sorted(result.x_events, key=lambda value: value.coeffs)
        recornered = tuple(tuple(reversed(square[1:] + square[:1])) for square in squares)
        reordered = verify_density_slabs(recornered, family.side, weights)
        assert reordered.maximum == expected
        assert reordered.x_events == result.x_events


def test_all_zero_weights_and_duplicate_aliases_do_not_inflate_depth() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    square = axis_square(q(1), q(1))
    reflected = tuple(reversed(square))
    zero = verify_density_slabs((square,), q(3), (Fraction(),))
    assert zero.x_events == (q(0), q(3))
    assert zero.maximum == 0
    assert zero.witness is None
    assert len(zero.slabs) == 1
    assert zero.slabs[0].bands == 1
    duplicate = verify_density_slabs((square, reflected), q(3), (Fraction(3, 4),) * 2)
    assert len(duplicate.family.placements) == 1
    assert duplicate.maximum == Fraction(3, 4)
    extra = axis_square(q("3/2"), q("3/2"))
    augmented = verify_density_slabs((square, extra), q(3), (Fraction(3, 4), Fraction()))
    assert augmented.maximum == duplicate.maximum
    assert augmented.x_events == duplicate.x_events
    with pytest.raises(SupportError, match="inconsistent"):
        verify_density_slabs((square, reflected), q(3), (Fraction(1), Fraction(1, 2)))


def test_one_overweight_square_and_foreign_field_witness_refusal() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    square = axis_square(q("1/2"), q("1/2"))
    weights = (Fraction(3, 2),)
    result = verify_density_slabs((square,), q(1), weights)
    assert result.maximum == Fraction(3, 2)
    witness = result.witness
    assert witness is not None
    assert witness.members == (0,)
    assert witness.radius == Fraction(1, 4)
    other_field = NumberField((1, 0), ("-1", "1"))
    foreign = replace(witness, point=(other_field.rational("1/2"), q("1/2")))
    with pytest.raises(SupportError, match="malformed"):
        reader.check_witness((square,), q(1), weights, foreign)


def test_supporting_line_crossings_outside_y_still_partition_x() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    first = tuple(
        (q(x), q(y)) for x, y in ((1, 1), ("8/5", "9/5"), ("4/5", "12/5"), ("1/5", "8/5"))
    )
    second = tuple((x + 1, y + q("1/2")) for x, y in first)
    result = verify_density_slabs((first, second), q(3), (Fraction(1, 2),) * 2)
    # The lines y=4*x/3+4/3 and y=-3*x/4+17/4 meet at (7/5,16/5).
    # Their intersection is above the container; its x still belongs to this reader.
    assert q("7/5") in result.x_events
    # Translation dot (3/5,4/5) equals 1, hence only an edge contact.
    assert result.maximum == Fraction(1, 2)
    assert result.witness is None


def test_sections_exclude_vertical_edges_and_vertex_only_contacts() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    square = axis_square(q(1), q(1))
    assert reader.vertical_section(square, q("1/2"), q(3)) is None
    assert reader.vertical_section(square, q("3/2"), q(3)) is None
    assert reader.vertical_section(square, q(1), q(3)) == (q("1/2"), q("3/2"))
    rotated = tuple(
        (q(x), q(y)) for x, y in ((1, 1), ("8/5", "9/5"), ("4/5", "12/5"), ("1/5", "8/5"))
    )
    assert reader.vertical_section(rotated, q("1/5"), q(3)) is None
    assert reader.vertical_section(rotated, q("8/5"), q(3)) is None


def test_malformed_or_empty_families_are_refused_before_enumeration() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    square = axis_square(q(1), q(1))
    bad_order = (square[0], square[2], square[1], square[3])
    outside = axis_square(q(0), q(0))
    other_field = NumberField((1, 0), ("-1", "1"))
    foreign = axis_square(other_field.rational(1), other_field.rational(1))
    for squares, side, weights in (
        ((), q(3), ()),
        ((square,), q(0), (Fraction(1),)),
        ((square,), q(3), ()),
        ((square,) * 61, q(3), (Fraction(1),) * 61),
        ((square,), q(3), (Fraction(-1),)),
        ((square,), q(3), (cast(Fraction, True),)),  # noqa: FBT003 -- invalid input control
        ((square,), q(3), (cast(Fraction, 0.5),)),
        ((bad_order,), q(3), (Fraction(1),)),
        ((outside,), q(3), (Fraction(1),)),
        ((foreign,), q(3), (Fraction(1),)),
        ((cast(Square, square[:3]),), q(3), (Fraction(1),)),
    ):
        with pytest.raises(SupportError):
            verify_density_slabs(squares, side, weights)


@pytest.mark.parametrize(("name", "expected"), [("contacts", "1"), ("triple", "6/5")])
def test_cli_exposes_only_small_declared_controls(
    name: str, expected: str, capsys: pytest.CaptureFixture[str]
) -> None:
    assert reader.main(["--control", name]) == 0
    receipt = json.loads(capsys.readouterr().out)
    assert receipt["scope"] == "toy-only-ae-depth"
    assert receipt["control"] == name
    assert receipt["maximum"] == expected
    assert receipt["slabs"] == receipt["x_events"] - 1
    with pytest.raises(SystemExit) as stopped:
        reader.main(["--control", "trump11-v1"])
    assert stopped.value.code == 2
