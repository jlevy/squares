"""The counterexample to Nagamochi's Lemma 1 is recomputed exactly, not read off a paper.

`T-007` cites [Nagamochi 2005] Theorem 2 for the verified lower bound at most open
cases. Theorem 2 rests on Theorem 1, whose only proof in the paper sums Lemma 1. Karakus
(arXiv:2609.37410) and chelokot's Lean archive each give a square of side just above one
whose score is below one. These tests hold the devtool to the printed facts as exact
rational equalities, control it with a member outside the family's range, and pin the
comparison between Karakus's replacement bound and Theorem 2's closed form.
"""

from __future__ import annotations

import math
from decimal import Decimal
from fractions import Fraction

import pytest

from devtools.check_nagamochi_bounds import theorem_two
from devtools.check_nagamochi_lemma1_counterexample import (
    CHELOKOT_LEAN_CEILING,
    CHELOKOT_SCORE,
    DECLARED_CONTAINERS,
    DECLARED_T,
    SIDE_CEILING,
    CounterexampleError,
    axis_square,
    centre,
    check_chelokot_instance,
    check_karakus_member,
    check_local_repairs,
    compare_bounds,
    karakus_above_area,
    karakus_at_most_nagamochi,
    karakus_bound,
    karakus_contact_square,
    karakus_strip_measure,
    karakus_total,
    main,
    nagamochi_measure,
    nagamochi_total,
    shrink,
    shrink_factor,
    side_squared,
)

FOUR = Fraction(4)


def test_the_tool_passes_end_to_end() -> None:
    assert main() == 0


@pytest.mark.parametrize("t", DECLARED_T)
@pytest.mark.parametrize(("a", "b"), DECLARED_CONTAINERS)
def test_each_declared_member_scores_below_one(t: Fraction, a: Fraction, b: Fraction) -> None:
    report = check_karakus_member(t, a, b)
    # Appendix A's polynomial, and (4.8)'s bound at the family's largest t.
    assert report["contact_closed"] == Fraction(29, 20) + t + t * t / 2 + t**3 / 2
    assert report["contact_without_P"] <= Fraction(242551, 250000) < 1
    assert report["shrunk_interior"] < 1
    assert report["shrunk_closed"] < 1
    assert report["vertex_shrunk_interior"] < 1
    assert report["strip_measure_interior"] > 1


def test_the_worst_member_matches_the_printed_value() -> None:
    report = check_karakus_member(Fraction(1, 50), FOUR, FOUR)
    assert report["contact_without_P"] == Fraction(242551, 250000)


def test_the_score_does_not_depend_on_the_container() -> None:
    """The family is local to one corner: every container in (4.1) gives the same score."""
    scores = {
        check_karakus_member(Fraction(1, 100), a, b)["shrunk_interior"]
        for a, b in DECLARED_CONTAINERS
    }
    assert len(scores) == 1


def test_a_member_outside_the_range_is_refused_not_passed() -> None:
    """Control: at t = 1/10 the contact square scores 1.0555 and (4.3) fails; say so."""
    with pytest.raises(CounterexampleError, match="outside"):
        check_karakus_member(Fraction(1, 10), FOUR, FOUR)
    k = karakus_contact_square(Fraction(1, 10))
    measure = nagamochi_measure(FOUR, FOUR)
    assert measure.score(k, closed=False) > 1


def test_a_container_too_small_for_the_family_is_refused() -> None:
    """At a = 3 the point (2, 9/10) belongs to Q and L4 sits on x = 2; (4.3) excludes it."""
    with pytest.raises(CounterexampleError, match=r"\(4\.3\)"):
        check_karakus_member(Fraction(1, 50), Fraction(3), Fraction(4))


def test_a_corrupted_vertex_is_caught() -> None:
    """Control: nudging one vertex of K_t is detected as not a square."""
    k = list(karakus_contact_square(Fraction(1, 50)))
    k[2] = (k[2][0] + Fraction(1, 10**6), k[2][1])
    with pytest.raises(CounterexampleError):
        side_squared(tuple(k))


def test_chelokot_instance_recomputes_to_the_printed_fraction() -> None:
    report = check_chelokot_instance()
    assert report["interior"] == CHELOKOT_SCORE
    assert report["interior"] < CHELOKOT_LEAN_CEILING
    # No weighted point is on the boundary, so the two conventions agree.
    assert report["closed"] == report["interior"]


@pytest.mark.parametrize(("a", "b"), DECLARED_CONTAINERS)
def test_measure_totals_match_the_printed_right_hand_sides(a: Fraction, b: Fraction) -> None:
    assert nagamochi_measure(a, b).total() == nagamochi_total(a, b)
    if b >= 3:
        assert karakus_strip_measure(a, b).total() == a * b - (a + 1 - math.ceil(a))
    assert karakus_total(a) == a * a - (a + 1 - math.ceil(a))


def test_integer_containers_lose_exactly_two_and_one() -> None:
    for k in range(3, 12):
        side = Fraction(k)
        assert nagamochi_total(side, side) == k * k - 2
        assert karakus_total(side) == k * k - 1


def test_local_repairs_each_fail_on_the_axis_parallel_corner_square() -> None:
    report = check_local_repairs(FOUR, FOUR)
    assert report["nagamochi"]["alpha"] == Fraction(10191, 10000)
    assert report["nagamochi"]["beta"] < 1
    for variant in ("weight", "slide"):
        assert report[variant]["total"] == report["nagamochi"]["total"]
        assert report[variant]["beta"] > 1
        assert report[variant]["alpha"] == Fraction(9691, 10000)
    assert report["augment"]["total"] == report["nagamochi"]["total"] + Fraction(2, 5)
    assert report["augment"]["alpha"] > 1
    assert report["augment"]["beta"] > 1


def test_the_shrunken_side_stays_in_the_lemma_s_range() -> None:
    for t in DECLARED_T:
        k = karakus_contact_square(t)
        s = shrink(k, shrink_factor(t), centre(k))
        assert 1 < side_squared(s) <= SIDE_CEILING**2


def test_axis_square_helper_is_a_square() -> None:
    assert side_squared(axis_square(Fraction(1), Fraction(2), Fraction(3, 2))) == Fraction(9, 4)


def test_karakus_bound_is_between_area_and_theorem_two_exactly() -> None:
    for n in range(8, 1001):
        if math.isqrt(n) ** 2 == n:
            continue
        below, equal = karakus_at_most_nagamochi(n)
        assert below
        assert karakus_above_area(n)
        assert equal == (n == (math.isqrt(n) + 1) ** 2 - 1)


def test_karakus_bound_is_the_integer_at_m_squared_minus_one() -> None:
    for m in range(3, 20):
        assert karakus_bound(m * m - 1) == Decimal(m)
        assert theorem_two(m * m - 1)[0] == Decimal(m)


def test_karakus_bound_at_review_values() -> None:
    # (1 + sqrt(4N - 4k + 1)) / 2 with k = floor(sqrt N): the radicands are 37, 45, 77,
    # 85, 117, 165, 293 and 353.
    expected = {
        12: "3.541381",
        14: "3.854102",
        23: "4.887482",
        26: "5.109772",
        34: "5.908327",
        47: "6.922616",
        82: "9.058621",
        97: "9.894147",
    }
    for n, text in expected.items():
        values = compare_bounds(n)
        area, nagamochi, karakus = values["area"], values["nagamochi"], values["karakus"]
        assert area is not None
        assert nagamochi is not None
        assert karakus is not None
        assert f"{karakus:.6f}" == text
        assert area < karakus <= nagamochi


def test_corollary_six_two_is_not_stated_below_eight() -> None:
    with pytest.raises(ValueError, match="nonsquare N >= 8"):
        karakus_bound(7)
    assert compare_bounds(7)["karakus"] is None
    with pytest.raises(ValueError, match="nonsquare"):
        karakus_bound(16)
