"""`devtools.check_half_angle_area`: the third exact route for the 2026-10-10 reviews."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_half_angle_area as route
from devtools import upper_bound_reports as upper
from devtools.check_half_angle_area import (
    AreaRouteError,
    Pose,
    admitted,
    controls,
    corners,
    decide,
    decide_placed,
    literal,
    overlaps,
    parse_certificate,
    placed,
    read_centred_json,
    read_fact,
    read_squish_json,
    rotation,
    unit_basis,
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


# --------------------------------------------------------------------------- the imports

#: Two unit squares in the box of side 12/5, the right one turned to c = 3/5 and touching
#: the left one with a vertex, as in the rotated-contact test above.
PAIR_JSON: dict[str, Any] = {
    "n": 2,
    "s_exact": "12/5",
    "squares": [["1/2", "3/5", "0"], ["17/10", "7/10", "1/2"]],
}


def test_a_stated_basis_must_be_a_rotation() -> None:
    assert unit_basis(Fraction(3, 5), Fraction(-4, 5)) == (Fraction(3, 5), Fraction(-4, 5))
    with pytest.raises(AreaRouteError):
        unit_basis(Fraction(1), Fraction(1, 2))
    with pytest.raises(AreaRouteError):
        decide_placed(Fraction(2), [(Fraction(1), Fraction(1), Fraction(1), Fraction(1, 2))])


def test_a_placed_decision_is_the_half_angle_one_and_counts_wall_contacts() -> None:
    assert decide(Fraction(2), GRID, measure=True) == decide_placed(
        Fraction(2), placed(GRID), measure=True
    )
    # Each grid square touches two walls of the closed box; nothing touches at side 3.
    assert decide(Fraction(2), GRID).wall_contacts == 8
    assert (
        decide(Fraction(3), [(Fraction(3, 2), Fraction(3, 2), Fraction(0))]).wall_contacts == 0
    )


def test_the_squish_and_centred_readers_read_one_packing_alike() -> None:
    squish = read_squish_json(json.dumps(PAIR_JSON).encode(), 2)
    shifted = [
        {"x": str(literal(x) - Fraction(6, 5)), "y": str(literal(y) - Fraction(6, 5)), "t": t}
        for x, y, t in PAIR_JSON["squares"]
    ]
    centred = {"n": 2, "coordinate_system": "centered", "side": "12/5", "squares": shifted}
    assert read_centred_json(json.dumps(centred).encode(), 2) == squish
    assert squish == parse_certificate("2 12/5\n1/2 3/5 0\n17/10 7/10 1/2\n", 2)


@pytest.mark.parametrize(
    "text",
    [
        '{"n": 2, "n": 2, "s_exact": "12/5", "squares": []}',
        '{"n": 3, "s_exact": "12/5", "squares": [["1", "1", "0"], ["2", "1", "0"]]}',
        '{"n": 2, "s_exact": "12/5", "squares": [["1", "1"], ["2", "1", "0"]]}',
        '{"n": 2, "s_exact": 2.4, "squares": [["1", "1", "0"], ["2", "1", "0"]]}',
        '{"n": 2, "s_exact": "1e3", "squares": [["1", "1", "0"], ["2", "1", "0"]]}',
    ],
)
def test_the_squish_reader_refuses_what_its_format_does_not_state(text: str) -> None:
    with pytest.raises(AreaRouteError):
        read_squish_json(text.encode(), 2)


def test_the_centred_reader_refuses_another_coordinate_system() -> None:
    square = {"x": "0", "y": "0", "t": "0"}
    value = {"n": 1, "coordinate_system": "lower-left", "side": "2", "squares": [square]}
    centred = json.dumps({**value, "coordinate_system": "centered"}).encode()
    assert read_centred_json(centred, 1) == (
        Fraction(2),
        ((Fraction(1), Fraction(1), Fraction(0)),),
    )
    with pytest.raises(AreaRouteError):
        read_centred_json(json.dumps(value).encode(), 1)


def test_the_n70_fact_reads_as_its_bases_state_and_as_the_kernel_reads_it() -> None:
    packet = route.WEB / route.IMPORTS["#483"]
    certificate = upper.read_facts(packet)[70]
    text = route.packet_bytes(packet / "facts/n-070.yaml").decode()
    side, placements = read_fact(text, 70)
    assert side == certificate.side
    assert placements == tuple((p.x, p.y, *p.basis) for p in certificate.poses)
    # One basis off the unit circle, by one unit in a numerator, is refused.
    tampered = text.replace("- -60000000000000000/", "- -60000000000000001/", 1)
    assert tampered != text
    with pytest.raises(AreaRouteError):
        read_fact(tampered, 70)


@pytest.mark.parametrize(
    ("side", "offered"),
    [
        (Fraction(3, 7), "3/7"),
        (Fraction(3, 7), "6/14"),
        (Fraction(3, 7), "0.429"),
        (Fraction(1, 8), "0.125"),
        (Fraction(1, 8), "0.13"),
    ],
)
def test_admission_takes_the_printed_side_or_its_rounding_up(
    side: Fraction, offered: str
) -> None:
    assert admitted(side, offered)


@pytest.mark.parametrize("offered", ["0.428", "0.430", "4/7", "0.4285714285714285"])
def test_admission_refuses_a_print_below_the_side_or_above_its_rounding_up(
    offered: str,
) -> None:
    assert not admitted(Fraction(3, 7), offered)


SQUISH_481 = (
    131,
    153,
    154,
    207,
    209,
    232,
    236,
    237,
    259,
    263,
    269,
    270,
    292,
    302,
    303,
    305,
    307,
)


def test_the_import_roster_is_every_certificate_the_entries_would_cite() -> None:
    found = [(case.issue, case.n) for case in route.import_cases()]
    assert found == [
        *(("#476", n) for n in (132, 237, 263, 267, 270, 303)),
        *(("#481", n) for n in SQUISH_481),
        ("#483", 70),
        *(("#484", n) for n in (308, 343, 344)),
    ]


def test_the_n70_import_agrees_with_its_receipt_plan_and_print_to_every_digit() -> None:
    case = next(case for case in route.import_cases() if case.issue == "#483")
    row = route.decide_import(case)
    packet = route.WEB / case.packet
    maintained = upper.check_certification(packet)[70]
    claim = route.PLAN_CLAIM.findall(upper.register_plan(packet)["results.yaml"]["claim"])
    frozen = upper.check_claims(packet)["results"][0]
    assert row["passed"]
    assert row["wall_contacts"] == 0
    assert all(row["controls"].values())
    assert (
        route.compare_import(
            row, maintained, literal(claim[0][1]), frozen, "8.88096037156625096037155737"
        )
        == []
    )
    assert route.compare_import(
        row, maintained, literal(claim[0][1]), frozen, "8.880960371566"
    ) == [
        f"#483 n=70 ({case.packet}): the frozen claim record states another side",
        (
            f"#483 n=70 ({case.packet}): the side is neither the printed 8.880960371566 nor "
            "rounds up to it"
        ),
    ]


@pytest.fixture
def mock_packet(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    """A derived-fact packet of two squares and its upstream files at a pinned commit."""
    monkeypatch.setattr(route, "REPO", tmp_path)
    commit = "0" * 40
    upstream = tmp_path / "upstream"
    (upstream / "run").mkdir(parents=True)
    centred = {
        "n": 2,
        "coordinate_system": "centered",
        "side": "12/5",
        "squares": [
            {"x": "-7/10", "y": "-3/5", "t": "0"},
            {"x": "1/2", "y": "-1/2", "t": "1/2"},
        ],
    }
    (upstream / "run/cert.json").write_text(json.dumps(centred), encoding="utf-8")
    (upstream / "run/summary.csv").write_text("n,exact\n2,12/5\n", encoding="utf-8")
    packet = tmp_path / "packet"
    (packet / "acquisition").mkdir(parents=True)
    (packet / "facts").mkdir()
    pinned = [
        {"path": path, "sha256": hashlib.sha256((upstream / path).read_bytes()).hexdigest()}
        for path in ("run/cert.json", "run/summary.csv")
    ]
    record = {"sources": [{"source_commit": commit, "pinned_only": pinned}]}
    (packet / "acquisition/sources.json").write_text(json.dumps(record), encoding="utf-8")
    row = {
        "n": 2,
        "path": "run/cert.json",
        "format": "centred-json",
        "offered": "12/5",
        "printed_in": f"https://github.com/someone/repo/blob/{commit}/run/summary.csv",
        "fact": "facts/n-002.yaml",
    }
    declaration = {"certificates": [row], "requested": [2]}
    (packet / "acquisition/report.json").write_text(json.dumps(declaration), encoding="utf-8")
    fact = (
        "witness:\n  n: 2\n  side: 12/5\n  square_size: '1'\n"
        "  representation: center-basis\n  scalar:\n    kind: rational\n"
        "  coordinates:\n    origin: lower-left\n    axes: x-right-y-up\n  squares:\n"
        "  - id: 1\n    center: [1/2, 3/5]\n    basis: ['1', '0']\n"
        "  - id: 2\n    center: [17/10, 7/10]\n    basis: [3/5, 4/5]\n"
    )
    (packet / "facts/n-002.yaml").write_text(fact, encoding="utf-8")
    return packet, upstream


def test_a_fact_is_held_to_its_pinned_upstream_file_and_printed_side(
    mock_packet: tuple[Path, Path],
) -> None:
    packet, upstream = mock_packet
    assert route.upstream_problems(packet, upstream) == (2, [])


def test_an_upstream_file_off_its_pin_or_another_packing_is_reported(
    mock_packet: tuple[Path, Path],
) -> None:
    packet, upstream = mock_packet
    path = upstream / "run/summary.csv"
    path.write_text("n,exact\n2,13/5\n", encoding="utf-8")
    assert route.upstream_problems(packet, upstream) == (
        1,
        ["packet: run/summary.csv is not the file the packet pins"],
    )
    fact = packet / "facts/n-002.yaml"
    fact.write_text(fact.read_text().replace("[17/10, 7/10]", "[9/5, 7/10]"), encoding="utf-8")
    _held, problems = route.upstream_problems(packet, upstream)
    assert "packet n=2: the fact is not the packing run/cert.json states" in problems
