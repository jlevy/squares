"""`devtools.check_half_angle_area`: the third exact route for T-128, T-130 and T-131."""

from __future__ import annotations

from fractions import Fraction

import pytest

from devtools import check_half_angle_area as route
from devtools.check_half_angle_area import (
    AreaRouteError,
    Pose,
    controls,
    corners,
    decide,
    literal,
    overlaps,
    parse_certificate,
    rotation,
)

TINY = Fraction(1, 10**30)
#: Four axis-aligned unit squares filling the box of side 2: every pair touches.
GRID: tuple[Pose, ...] = tuple(
    (Fraction(x, 2), Fraction(y, 2), Fraction(0)) for y in (1, 3) for x in (1, 3)
)
#: c = 3/5, s = 4/5: the square reaches 7/10 either side of its centre along each axis.
HALF_TURN = Fraction(1, 2)


def test_literal_reads_each_form_the_format_names() -> None:
    assert literal("3") == 3
    assert literal("-3/4") == Fraction(-3, 4)
    assert literal("0.125") == Fraction(1, 8)
    assert literal("-2.50") == Fraction(-5, 2)


@pytest.mark.parametrize("text", ["1e3", "1/0", " 1", "1_000", "+1", "1/-2", "1/2/3", ""])
def test_literal_refuses_what_the_format_does_not_name(text: str) -> None:
    with pytest.raises(AreaRouteError):
        literal(text)


def test_parse_reads_header_rows_and_comments() -> None:
    side, poses = parse_certificate("# comment\n2 2\n\n1/2 1/2 0\n3/2 1/2 1/3\n", 2)
    assert side == 2
    assert poses[1] == (Fraction(3, 2), Fraction(1, 2), Fraction(1, 3))


@pytest.mark.parametrize(
    "text",
    [
        "3 2\n1/2 1/2 0\n3/2 1/2 0\n",
        "2 2\n1/2 1/2 0\n3/2 1/2 0\n1 1 0\n",
        "2 0\n1/2 1/2 0\n3/2 1/2 0\n",
        "2 2\n1/2 1/2\n3/2 1/2 0\n",
    ],
)
def test_parse_refuses_a_wrong_count_extra_row_side_or_field(text: str) -> None:
    with pytest.raises(AreaRouteError):
        parse_certificate(text, 2)


def test_half_angle_map_is_exact() -> None:
    assert rotation(Fraction(0)) == (1, 0)
    assert rotation(Fraction(1)) == (0, 1)
    assert rotation(HALF_TURN) == (Fraction(3, 5), Fraction(4, 5))


def test_touching_grid_is_accepted_in_the_closed_box() -> None:
    decision = decide(Fraction(2), GRID, measure=True)
    assert decision.passed
    assert decision.wall_clearance == 0
    assert decision.clipped == 4
    assert decision.closest is not None
    assert decision.closest[0] == 0


def test_an_overlap_far_below_binary64_is_refused() -> None:
    poses = (GRID[0], (Fraction(3, 2) - TINY, Fraction(1, 2), Fraction(0)))
    assert decide(Fraction(2), GRID[:2]).passed
    assert not decide(Fraction(2), poses).passed


def test_rotated_square_touching_an_edge_with_its_vertex() -> None:
    # The rotated square's leftmost vertex sits at (1, 3/5), on the other square's edge.
    left: Pose = (Fraction(1, 2), Fraction(3, 5), Fraction(0))
    right: Pose = (Fraction(17, 10), Fraction(7, 10), HALF_TURN)
    assert decide(Fraction(12, 5), (left, right)).passed
    moved: Pose = (right[0] - TINY, right[1], right[2])
    assert not decide(Fraction(12, 5), (left, moved)).passed
    assert not decide(Fraction(12, 5) - TINY, (left, right)).passed


def test_corner_contact_is_decided_by_the_disc_rule_and_a_push_by_the_area() -> None:
    a = corners(Fraction(1, 2), Fraction(1, 2), Fraction(1), Fraction(0))
    b = corners(Fraction(3, 2), Fraction(3, 2), Fraction(1), Fraction(0))
    pushed = corners(Fraction(3, 2) - TINY, Fraction(3, 2) - TINY, Fraction(1), Fraction(0))
    assert not overlaps(a, b)
    assert overlaps(a, pushed)


def test_every_control_reaches_its_required_outcome_on_the_grid() -> None:
    decision = decide(Fraction(2), GRID, measure=True)
    assert all(controls(Fraction(2), GRID, decision).values())


def test_a_control_that_cannot_refuse_is_reported() -> None:
    # One square alone has no pair to push, so the pair controls cannot run.
    lone: tuple[Pose, ...] = (GRID[0], (Fraction(9, 2), Fraction(9, 2), Fraction(0)))
    decision = decide(Fraction(5), lone, measure=True)
    with pytest.raises(AreaRouteError):
        controls(Fraction(5), lone, decision)


def test_all_fifteen_certificates_are_admitted_from_their_packets() -> None:
    found = [(case.entry, case.n) for case in route.cases()]
    assert found == [
        *(("T-128", n) for n in (105, 108, 127, 131, 155, 180, 228, 306)),
        *(("T-130", n) for n in (84, 86, 105, 175, 270)),
        ("T-131", 132),
        ("T-128", 155),
    ]


def test_smallest_certificate_agrees_with_its_receipt_and_claim_to_every_digit() -> None:
    case = next(case for case in route.cases() if (case.entry, case.n) == ("T-130", 84))
    row = route.decide_case(case)
    maintained = route.maintained_positives()[case.packet, 84]
    assert row["passed"]
    assert row["wall_clearance"] == "1/200000000000000000000"
    assert all(row["controls"].values())
    assert route.compare(row, maintained, route.register_claims()["T-130"][84]) == []


def test_a_claim_off_by_one_unit_in_its_last_place_is_reported() -> None:
    case = next(case for case in route.cases() if (case.entry, case.n) == ("T-130", 84))
    side, poses = parse_certificate(case.text, 84)
    row = {
        "entry": "T-130",
        "packet": case.packet,
        "n": 84,
        "side": str(side),
        "poses": [[str(value) for value in pose] for pose in poses],
        "passed": True,
        "wall_clearance": "1/200000000000000000000",
        "least_distance_squared": "1",
        "controls": {"all": True},
    }
    maintained = route.maintained_positives()[case.packet, 84]
    problems = route.compare(row, maintained, side - Fraction(1, 10**30))
    assert problems == [
        f"T-130 n=84 ({case.packet}): the register claim's decimal is not the exact side"
    ]


def test_register_claims_print_every_count_once() -> None:
    claims = route.register_claims()
    assert sorted(claims["T-128"]) == [105, 108, 127, 131, 155, 180, 228, 306]
    assert sorted(claims["T-130"]) == [84, 86, 105, 175, 270]
    assert sorted(claims["T-131"]) == [132]
