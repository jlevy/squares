"""Source/toy controls only; no H-036 target coordinates or angle evaluation."""

from __future__ import annotations

from fractions import Fraction

from devtools.angle_tile_certificate import (
    TileSlab,
    bernstein_coefficients,
    certify_nonnegative,
    check_cover,
    closed_tiles,
    evaluate,
    membership_polynomials,
)


def test_bernstein_proves_closed_endpoint_zeros_but_not_sampled_positivity() -> None:
    assert bernstein_coefficients(
        (Fraction(0), Fraction(1), Fraction(-1)), Fraction(0), Fraction(1)
    ) == (Fraction(0), Fraction(1, 2), Fraction(0))
    assert certify_nonnegative(
        (Fraction(0), Fraction(1), Fraction(-1)), Fraction(0), Fraction(1)
    ).proved
    negative_middle = (Fraction(3, 16), Fraction(-1), Fraction(1))
    result = certify_nonnegative(negative_middle, Fraction(0), Fraction(1))
    assert not result.proved
    assert result.unresolved == ((Fraction(0), Fraction(1)),)


def test_rational_interior_zero_requires_split_and_irrational_zero_stays_unresolved() -> None:
    rational_tangency = (Fraction(1, 4), Fraction(-1), Fraction(1))
    assert not certify_nonnegative(rational_tangency, Fraction(0), Fraction(1)).proved
    assert certify_nonnegative(rational_tangency, Fraction(0), Fraction(1), max_depth=1).proved
    irrational_tangency = (Fraction(1, 4), Fraction(0), Fraction(-1), Fraction(0), Fraction(1))
    result = certify_nonnegative(irrational_tangency, Fraction(0), Fraction(1), max_depth=4)
    assert not result.proved
    assert result.unresolved == ((Fraction(11, 16), Fraction(3, 4)),)
    assert certify_nonnegative((Fraction(0),), Fraction(-1), Fraction(1)).proved


def test_closed_binary_mesh_retains_seams_and_refuses_missing_or_duplicate_tiles() -> None:
    tiles = closed_tiles(("00", "01", "1"))
    assert list(closed_tiles(("1", "01", "00")).items()) == list(tiles.items())
    assert tiles["00"] == (
        (Fraction(1), Fraction(1)),
        (Fraction(0), Fraction(0)),
        (Fraction(1, 2), Fraction(0)),
    )
    assert tiles["01"] == (
        (Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(1)),
        (Fraction(1, 2), Fraction(0)),
    )
    for paths in (("00", "1"), ("0",), ("0", "0", "1"), ("0", "00", "1")):
        try:
            closed_tiles(paths)
        except ValueError:
            pass
        else:
            raise AssertionError(f"incomplete or overlapping tree accepted: {paths}")


def test_fixed_axis_closed_contact_and_two_moving_sign_charts() -> None:
    assignments = (("0", 0), ("1", 0))
    fixed = check_cover(
        Fraction(2),
        ((Fraction(1), Fraction(1)),),
        (Fraction(0), Fraction(0)),
        (TileSlab(Fraction(0), Fraction(0), assignments),),
    )
    assert fixed.proved
    assert fixed.inequalities_checked == 24
    moving = check_cover(
        Fraction(3, 2),
        ((Fraction(3, 4), Fraction(3, 4)),),
        (Fraction(-1, 8), Fraction(1, 8)),
        (
            TileSlab(Fraction(-1, 8), Fraction(0), assignments),
            TileSlab(Fraction(0), Fraction(1, 8), assignments),
        ),
    )
    assert moving.proved
    assert moving.inequalities_checked == 48
    for low, high, value in (
        (Fraction(-1, 8), Fraction(0), Fraction(-1, 8)),
        (Fraction(0), Fraction(1, 8), Fraction(1, 8)),
    ):
        z = (Fraction(1, 3), Fraction(2, 5))
        point = (Fraction(2, 3), Fraction(4, 5))
        polynomials = membership_polynomials(Fraction(3, 2), point, z, low, high)
        denominator = 1 + value * value
        cosine, sine = (1 - value * value) / denominator, 2 * value / denominator
        half_width = (abs(cosine) + abs(sine)) / 2
        center = tuple(
            half_width + (Fraction(3, 2) - 2 * half_width) * coordinate for coordinate in z
        )
        dx, dy = point[0] - center[0], point[1] - center[1]
        along, across = cosine * dx + sine * dy, -sine * dx + cosine * dy
        expected = tuple(
            denominator**2 * (Fraction(1, 2) - dot) for dot in (along, -along, across, -across)
        )
        assert tuple(evaluate(polynomial, value) for polynomial in polynomials) == expected
        assert all(len(polynomial) <= 5 for polynomial in polynomials)


def test_quartic_identity_at_a_moving_wall_corner() -> None:
    # H=(1+2t-t^2)/2, p*d-H=1/4-t+5t^2/4 in each coordinate.
    along, _, across, _ = membership_polynomials(
        Fraction(3, 2),
        (Fraction(3, 4), Fraction(3, 4)),
        (Fraction(0), Fraction(0)),
        Fraction(0),
        Fraction(1, 8),
    )
    assert along == (
        Fraction(1, 4),
        Fraction(1, 2),
        Fraction(2),
        Fraction(-7, 2),
        Fraction(7, 4),
    )
    assert across == (
        Fraction(1, 4),
        Fraction(3, 2),
        Fraction(-2),
        Fraction(3, 2),
        Fraction(7, 4),
    )


def test_domain_and_label_tampering_cannot_produce_a_cover() -> None:
    assignments = (("0", 0), ("1", 0))
    domain = (Fraction(-1, 8), Fraction(1, 8))
    points = ((Fraction(3, 4), Fraction(3, 4)),)
    bad_slabs = (
        (TileSlab(Fraction(0), Fraction(1, 8), assignments),),
        (TileSlab(Fraction(-1, 8), Fraction(0), assignments),),
        (TileSlab(Fraction(-1, 8), Fraction(1, 8), assignments),),
        (
            TileSlab(Fraction(-1, 8), Fraction(-1, 16), assignments),
            TileSlab(Fraction(0), Fraction(1, 8), assignments),
        ),
        (
            TileSlab(Fraction(-1, 8), Fraction(0), (("0", 0),)),
            TileSlab(Fraction(0), Fraction(1, 8), assignments),
        ),
        (
            TileSlab(Fraction(-1, 8), Fraction(0), (("0", 1), ("1", 0))),
            TileSlab(Fraction(0), Fraction(1, 8), assignments),
        ),
    )
    for slabs in bad_slabs:
        try:
            check_cover(Fraction(3, 2), points, domain, slabs)
        except ValueError:
            pass
        else:
            raise AssertionError("incomplete or mislabeled certificate accepted")
    two_points = ((Fraction(1), Fraction(1)), (Fraction(1, 2), Fraction(1)))
    changed_label = check_cover(
        Fraction(2),
        two_points,
        (Fraction(0), Fraction(0)),
        (TileSlab(Fraction(0), Fraction(0), (("0", 1), ("1", 0))),),
    )
    assert not changed_label.proved
    assert changed_label.inequalities_checked == 24
    assert all(failure.tile == "0" for failure in changed_label.unresolved)
    # The unchanged other point covers everything: this failed assignment is not
    # an avoider of the marked-point set, much less a packing counterexample.
    assert check_cover(
        Fraction(2),
        two_points,
        (Fraction(0), Fraction(0)),
        (TileSlab(Fraction(0), Fraction(0), assignments),),
    ).proved


def test_zero_width_and_invalid_sign_limits_are_refused() -> None:
    try:
        check_cover(
            Fraction(1),
            ((Fraction(1, 2), Fraction(1, 2)),),
            (Fraction(0), Fraction(0)),
            (TileSlab(Fraction(0), Fraction(0), (("0", 0), ("1", 0))),),
        )
    except ValueError as error:
        assert "positive center-box width" in str(error)
    else:
        raise AssertionError("zero-width center domain accepted")
    for depth in (-1, 9):
        try:
            certify_nonnegative((Fraction(1),), Fraction(0), Fraction(1), max_depth=depth)
        except ValueError as error:
            assert "depth" in str(error)
        else:
            raise AssertionError("out-of-budget sign subdivision accepted")


def test_degree_and_arithmetic_guards_do_not_silently_round() -> None:
    for polynomial in ((Fraction(1),) * 6, (Fraction(2**2048),)):
        try:
            certify_nonnegative(polynomial, Fraction(0), Fraction(1))
        except ValueError:
            pass
        else:
            raise AssertionError("out-of-contract polynomial accepted")
    # Below zero by an exact rational too small to distinguish by float rounding.
    tiny_negative = (Fraction(-1, 2**1024),)
    result = certify_nonnegative(tiny_negative, Fraction(0), Fraction(0))
    assert not result.proved
    assert result.unresolved == ((Fraction(0), Fraction(0)),)
