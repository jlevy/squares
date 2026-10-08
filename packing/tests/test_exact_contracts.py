"""Fast contracts for the reusable exact-arithmetic and verification boundary."""

from __future__ import annotations

from fractions import Fraction

import mpmath as mp
import pytest

from sqpack import verify
from sqpack.field import NumberField
from sqpack.prepared_verify import prepared_verify_packing
from sqpack.verify import verify_packing


def _fraction_sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def test_number_field_reduces_equal_elements_and_decides_sign() -> None:
    field = NumberField([1, 0, -2], (Fraction(7, 5), Fraction(3, 2)))
    alpha = field.alpha

    assert alpha * alpha - 2 == field.zero
    assert field.sign(alpha - Fraction(7, 5)) > 0
    assert field.sign(alpha - Fraction(3, 2)) < 0


def test_exact_verifier_distinguishes_contact_from_rational_overlap() -> None:
    first = [
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(1)),
        (Fraction(0), Fraction(1)),
    ]
    touching = [
        (Fraction(1), Fraction(0)),
        (Fraction(2), Fraction(0)),
        (Fraction(2), Fraction(1)),
        (Fraction(1), Fraction(1)),
    ]
    overlapping = [
        (Fraction(99, 100), Fraction(0)),
        (Fraction(199, 100), Fraction(0)),
        (Fraction(199, 100), Fraction(1)),
        (Fraction(99, 100), Fraction(1)),
    ]

    valid = verify_packing([first, touching], Fraction(2), _fraction_sign)
    invalid = verify_packing([first, overlapping], Fraction(2), _fraction_sign)

    assert valid.valid
    assert valid.touching_pairs == 1
    assert invalid.valid is False
    assert invalid.failures == [("overlap", "squares 0 and 1 overlap")]


def _unit_square(x: Fraction, y: Fraction) -> list[tuple[Fraction, Fraction]]:
    return [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]


def _four_squares() -> list[list[tuple[Fraction, Fraction]]]:
    return [
        _unit_square(Fraction(0), Fraction(0)),
        _unit_square(Fraction(1), Fraction(0)),
        _unit_square(Fraction(0), Fraction(1)),
        [
            (Fraction(3), Fraction(3)),
            (Fraction(18, 5), Fraction(19, 5)),
            (Fraction(14, 5), Fraction(22, 5)),
            (Fraction(11, 5), Fraction(18, 5)),
        ],
    ]


@pytest.mark.parametrize("scalar", ["fraction", "float", "mpf"])
@pytest.mark.parametrize("precision", [15, 50])
@pytest.mark.parametrize("bucket", [False, True])
def test_verifier_reuse_preserves_full_exact_and_tolerant_reports(
    scalar: str, precision: int, *, bucket: bool
) -> None:
    with mp.workdps(precision):
        rational = _four_squares()
        if scalar == "fraction":
            squares = rational
            sign = _fraction_sign
        elif scalar == "float":
            squares = [[(float(x), float(y)) for x, y in square] for square in rational]
            sign = verify.float_sign(1e-12)
        else:
            squares = [
                [
                    (mp.mpf(x.numerator) / x.denominator, mp.mpf(y.numerator) / y.denominator)
                    for x, y in square
                ]
                for square in rational
            ]
            sign = verify.float_sign(mp.mpf("1e-12"))
        pairs = list(verify.candidate_pairs(squares, bucket=bucket))
        assert [verify.separated(squares[i], squares[j], sign) for i, j in pairs] == [
            0,
            0,
            1,
            0,
            1,
            1,
        ]
        reference = verify_packing(squares, 5, sign, bucket=bucket)
        assert prepared_verify_packing(squares, 5, sign, bucket=bucket) == reference
        assert reference == verify.Report(
            valid=True,
            n=4,
            container_contacts=8,
            touching_pairs=3,
            strict_pairs=3,
            pairs_tested=6,
            touching_pair_indices=[(0, 1), (0, 2), (1, 2)],
        )


def test_verifier_recomputes_after_geometry_or_tolerance_changes() -> None:
    squares = [
        _unit_square(Fraction(0), Fraction(0)),
        _unit_square(Fraction(999, 1000), Fraction(0)),
    ]
    loose = prepared_verify_packing(squares, 3, verify.float_sign(1e-2))
    tight = prepared_verify_packing(squares, 3, verify.float_sign(1e-4))
    assert loose.valid
    assert loose.touching_pair_indices == [(0, 1)]
    assert not tight.valid
    assert tight.failures == [("overlap", "squares 0 and 1 overlap")]

    squares[1][:] = _unit_square(Fraction(2), Fraction(0))
    moved = prepared_verify_packing(squares, 3, _fraction_sign)
    assert moved.valid
    assert moved.strict_pairs == 1
    assert moved.touching_pair_indices == []
    squares[1][:] = squares[0]
    assert prepared_verify_packing(squares, 3, _fraction_sign).failures == [
        ("overlap", "squares 0 and 1 overlap")
    ]


def test_verifier_reuses_only_own_axis_arithmetic_within_each_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    squares = _four_squares()
    square_indices = {id(square): index for index, square in enumerate(squares)}
    axes_calls = 0
    axis_owners: dict[int, tuple[int, int]] = {}
    trace: list[tuple[int, int, int]] = []
    original_axes, original_project = verify.edge_axes, verify.project

    def counted_axes(square):
        nonlocal axes_calls
        axes_calls += 1
        axes = original_axes(square)
        for slot, axis in enumerate(axes):
            axis_owners[id(axis)] = (square_indices[id(square)], slot)
        return axes

    def counted_project(square, axis, sign):
        owner, slot = axis_owners[id(axis)]
        trace.append((square_indices[id(square)], owner, slot))
        return original_project(square, axis, sign)

    monkeypatch.setattr(verify, "edge_axes", counted_axes)
    monkeypatch.setattr(verify, "project", counted_project)
    for i, j in verify.candidate_pairs(squares):
        verify.separated(squares[i], squares[j], _fraction_sign)
    assert axes_calls == 12
    baseline_trace = list(trace)
    expected = []
    seen_own = set()
    for target, owner, slot in baseline_trace:
        if target == owner:
            if (owner, slot) in seen_own:
                continue
            seen_own.add((owner, slot))
        expected.append((target, owner, slot))
    assert 0 < len(expected) < len(baseline_trace)

    axes_calls = 0
    trace.clear()
    first = prepared_verify_packing(squares, 5, _fraction_sign)
    assert axes_calls == 4
    assert trace == expected
    axes_calls = 0
    trace.clear()
    assert prepared_verify_packing(squares, 5, _fraction_sign) == first
    assert axes_calls == 4
    assert trace == expected


def test_verifier_builds_both_axis_lists_before_a_strict_early_return() -> None:
    first = _unit_square(Fraction(0), Fraction(0))
    malformed = [(Fraction(0), Fraction(3)), (Fraction(1), Fraction(3))]
    with pytest.raises(IndexError):
        verify.separated(first, malformed, _fraction_sign)
    with pytest.raises(IndexError):
        prepared_verify_packing([first, malformed], 5, _fraction_sign, check_shapes=False)


def test_verifier_leaves_unpaired_axes_and_unreached_projections_unused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # With no pair, check_shapes=False never asks whether a piece has three vertices.
    assert prepared_verify_packing(
        [[(Fraction(1), Fraction(1))]], 5, _fraction_sign, check_shapes=False
    ) == verify.Report(valid=True, n=1)
    first = _unit_square(Fraction(0), Fraction(0))
    second = _unit_square(Fraction(0), Fraction(3))
    calls = []
    original_project = verify.project

    def checked_project(square, axis, sign):
        calls.append((square, axis))
        return original_project(square, axis, sign)

    monkeypatch.setattr(verify, "project", checked_project)
    assert prepared_verify_packing([first, second], 5, _fraction_sign).valid
    assert calls == [(first, (0, 1)), (second, (0, 1))]


def test_verifier_keeps_degenerate_shape_disabled_pair_semantics() -> None:
    squares = [
        [(Fraction(0), Fraction(0))] * 4,
        _unit_square(Fraction(1), Fraction(1)),
        _unit_square(Fraction(3), Fraction(3)),
    ]
    assert [
        verify.separated(squares[i], squares[j], _fraction_sign)
        for i, j in verify.candidate_pairs(squares)
    ] == [1, 1, 1]
    assert prepared_verify_packing(
        squares, 5, _fraction_sign, check_shapes=False
    ) == verify.Report(valid=True, n=3, container_contacts=8, strict_pairs=3, pairs_tested=3)


def test_verifier_reuse_preserves_an_exact_algebraic_rotated_square() -> None:
    field = NumberField([1, 0, -2], (Fraction(7, 5), Fraction(3, 2)))
    squares = [
        [(field.rational(x), field.rational(y)) for x, y in square]
        for square in _four_squares()[:3]
    ]
    diagonal = field.alpha / 2
    three = field.rational(3)
    squares.append(
        [
            (three, three),
            (three + diagonal, three + diagonal),
            (three, three + 2 * diagonal),
            (three - diagonal, three + diagonal),
        ]
    )
    assert [
        verify.separated(squares[i], squares[j], field.sign)
        for i, j in verify.candidate_pairs(squares)
    ] == [0, 0, 1, 0, 1, 1]
    reference = verify_packing(squares, field.rational(5), field.sign)
    assert prepared_verify_packing(squares, field.rational(5), field.sign) == reference
    assert reference == verify.Report(
        valid=True,
        n=4,
        container_contacts=8,
        touching_pairs=3,
        strict_pairs=3,
        pairs_tested=6,
        touching_pair_indices=[(0, 1), (0, 2), (1, 2)],
    )


@pytest.mark.parametrize("failure", ["shape", "container", "overlap"])
@pytest.mark.parametrize("bucket", [False, True])
def test_prepared_verifier_preserves_complete_failure_reports(
    failure: str, *, bucket: bool
) -> None:
    squares = _four_squares()
    if failure == "shape":
        x, y = squares[3][2]
        squares[3][2] = (x + Fraction(1, 10), y)
    elif failure == "container":
        squares[0] = [(x - Fraction(1, 10), y) for x, y in squares[0]]
    else:
        squares[1] = [(x - Fraction(1, 10), y) for x, y in squares[1]]
    reference = verify_packing(squares, 5, _fraction_sign, bucket=bucket)
    prepared = prepared_verify_packing(squares, 5, _fraction_sign, bucket=bucket)
    assert prepared == reference
    assert not reference.valid
    assert any(kind == failure for kind, _ in reference.failures)
