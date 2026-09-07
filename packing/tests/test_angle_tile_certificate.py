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
    fixed_grid_triangles,
    grid_obligations,
    membership_polynomials,
)
from sqpack.field import NumberField


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


def test_quadratic_coefficients_keep_exact_zero_and_refuse_mixed_embeddings() -> None:
    field = NumberField((1, 0, -2), ("1", "2"))
    alpha = field.alpha
    assert certify_nonnegative((alpha * alpha - 2,), Fraction(0), Fraction(1)).proved
    assert certify_nonnegative((alpha - 1,), Fraction(0), Fraction(1)).proved
    assert not certify_nonnegative((1 - alpha,), Fraction(0), Fraction(1)).proved
    assert bernstein_coefficients((field.zero, alpha, -alpha), Fraction(0), Fraction(1)) == (
        field.zero,
        alpha / 2,
        field.zero,
    )
    other_field = NumberField((1, 0, -2), ("1", "2"))
    for polynomial in (
        (alpha, other_field.alpha),
        (NumberField((1, 0, -2), ("-2", "-1")).alpha,),
        (NumberField((1, 0, -3), ("1", "2")).alpha,),
    ):
        try:
            certify_nonnegative(polynomial, Fraction(0), Fraction(1))
        except ValueError:
            pass
        else:
            raise AssertionError("mixed or unsupported quadratic field accepted")


def test_quadratic_side_toy_uses_the_same_map_without_algebraic_vertices() -> None:
    field = NumberField((1, 0, -2), ("1", "2"))
    side = field.alpha
    result = check_cover(
        side,
        ((side / 2, side / 2),),
        (Fraction(0), Fraction(0)),
        (TileSlab(Fraction(0), Fraction(0), (("0", 0), ("1", 0))),),
    )
    assert result.proved
    assert result.inequalities_checked == 24
    other_field = NumberField((1, 0, -2), ("1", "2"))
    try:
        check_cover(
            side,
            ((other_field.alpha / 2, other_field.alpha / 2),),
            (Fraction(0), Fraction(0)),
            (TileSlab(Fraction(0), Fraction(0), (("0", 0), ("1", 0))),),
        )
    except ValueError as error:
        assert "field" in str(error)
    else:
        raise AssertionError("mixed geometry fields accepted")


def test_fixed_grid_covers_all_closed_cells_in_a_deterministic_inventory() -> None:
    triangles = fixed_grid_triangles()
    assert len(triangles) == 36
    assert next(iter(triangles)) == (0, 0, 0)
    assert list(triangles)[-1] == (2, 5, 1)
    assert triangles[0, 0, 0] == (
        (Fraction(0), Fraction(0)),
        (Fraction(1, 6), Fraction(0)),
        (Fraction(1, 6), Fraction(1, 3)),
    )
    assert triangles[0, 0, 1] == (
        (Fraction(0), Fraction(0)),
        (Fraction(1, 6), Fraction(1, 3)),
        (Fraction(0), Fraction(1, 3)),
    )
    total_area = Fraction(0)
    for triangle in triangles.values():
        a, b, c = triangle
        area = ((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])) / 2
        assert area == Fraction(1, 36)
        total_area += area
    assert total_area == 1
    labels = ((0,) * 6,) * 3
    results = tuple(
        grid_obligations(
            Fraction(3, 2),
            ((Fraction(3, 4), Fraction(3, 4)),),
            labels,
        )
    )
    assert len(results) == 432
    assert results[0][0] == (0, 0, 0, 0, 0)
    assert results[-1][0] == (2, 5, 1, 2, 3)
    assert all(proved for _, proved in results)


def test_fixed_grid_refuses_missing_rows_columns_or_changed_labels() -> None:
    for labels in (
        ((0,) * 6,) * 2,
        ((0,) * 5,) * 3,
        ((1,) * 6,) * 3,
        ((True,) * 6,) * 3,
    ):
        try:
            tuple(
                grid_obligations(
                    Fraction(2),
                    ((Fraction(1), Fraction(1)),),
                    labels,
                )
            )
        except ValueError:
            pass
        else:
            raise AssertionError("incomplete or mislabeled grid accepted")


def test_fixed_grid_closed_interval_charts_and_endpoint_refusals() -> None:
    labels = ((0,) * 6,) * 3
    points = ((Fraction(3, 4), Fraction(3, 4)),)
    zero = Fraction(0)
    for low, high in ((Fraction(-1, 8), zero), (zero, Fraction(1, 8))):
        results = tuple(grid_obligations(Fraction(3, 2), points, labels, low=low, high=high))
        assert len(results) == 432
        assert all(proved for _index, proved in results)
    for low, high, expected in (
        (Fraction(-1, 8), Fraction(1, 8), "split"),
        (Fraction(1, 8), zero, "domain"),
        (zero, Fraction(1, 4), "chart"),
        (0.0, Fraction(1, 8), "Fraction"),
    ):
        try:
            tuple(
                grid_obligations(
                    Fraction(3, 2),
                    points,
                    labels,
                    low=low,  # pyright: ignore[reportArgumentType]
                    high=high,
                )
            )
        except ValueError as error:
            assert expected in str(error)
        else:
            raise AssertionError("invalid grid angle chart accepted")
