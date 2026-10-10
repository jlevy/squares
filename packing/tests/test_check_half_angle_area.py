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


# --------------------------------------------------------------------------- #470 and trio126

#: tan(15 degrees) = 2 - sqrt 3 and tan(30 degrees) = 1/sqrt 3, rounded down at 32 places,
#: from their known expansions 0.26794919243112270647255365849412763... and
#: 0.57735026918962576450914878050195745...
TAN_15 = Fraction(26794919243112270647255365849412, 10**32)
TAN_30 = Fraction(57735026918962576450914878050195, 10**32)
#: Two squares of Ellsworth's decimal text, centres in [-s/2, s/2]^2 and angles in degrees.
POSE_TEXT = "s: 2.15\n\nSquare 1: x=-0.5, y=-0.5, deg=0.0\nSquare 2: x=0.55, y=0.5, deg=30.0\n"


def test_the_decimal_pose_reader_reads_every_digit_exactly() -> None:
    printed, squares = route.read_decimal_pose(POSE_TEXT.encode(), 2)
    assert printed == "2.15"
    assert squares == (
        (Fraction(-1, 2), Fraction(-1, 2), Fraction(0)),
        (Fraction(11, 20), Fraction(1, 2), Fraction(30)),
    )


@pytest.mark.parametrize(
    "text",
    [
        POSE_TEXT.replace("Square 2", "Square 3"),
        POSE_TEXT.replace("deg=30.0", "deg=3e1"),
        POSE_TEXT.replace("s: 2.15", "side: 2.15"),
        POSE_TEXT + "Square 3: x=0.0, y=0.0, deg=0.0\n",
        POSE_TEXT.replace("x=0.55, y=0.5", "y=0.5, x=0.55"),
    ],
)
def test_the_decimal_pose_reader_refuses_any_other_form(text: str) -> None:
    with pytest.raises(AreaRouteError):
        route.read_decimal_pose(text.encode(), 2)


@pytest.mark.parametrize(
    ("degrees", "expected"),
    [
        (Fraction(0), Fraction(0)),
        (Fraction(90), Fraction(1)),
        (Fraction(-90), Fraction(-1)),
        (Fraction(450), Fraction(1)),
        (Fraction(30), TAN_15),
        (Fraction(60), TAN_30),
        (Fraction(-60), -TAN_30 - Fraction(1, 10**32)),
        (Fraction(-300), TAN_30),
    ],
)
def test_the_half_angle_floor_is_the_tangent_rounded_down(
    degrees: Fraction, expected: Fraction
) -> None:
    assert route.half_angle_floor(degrees, 32) == expected


def test_the_half_angle_floor_refuses_a_half_turn() -> None:
    with pytest.raises(AreaRouteError):
        route.half_angle_floor(Fraction(180), 32)


@pytest.mark.parametrize(
    "degrees",
    ["0.0000000000000268", "-0.0000000000000032", "28.0172114106334327", "-89.9999", "179.9"],
)
def test_the_half_angle_floor_agrees_with_the_importers_interval_floor(degrees: str) -> None:
    angle = literal(degrees)
    assert route.half_angle_floor(angle, 32) == upper.half_angle_tangent(angle, 32)


#: The #470 declaration row the two squares of `POSE_TEXT` would carry: 2.15 rounded up
#: at one place is 2.2, so the dilation is 2.2/2.15 = 44/43.
POSE_ROW: dict[str, Any] = {
    "n": 2,
    "path": "certificates/square-2.txt",
    "format": "decimal-dilation",
    "offered": "2.2",
    "options": [
        {"name": "dilation", "value": "44/43"},
        {"name": "half_angle_places", "value": "32"},
    ],
    "fact": "facts/n-002.yaml",
}


def _pose_witness() -> tuple[Fraction, tuple[route.Placed, ...]]:
    lam, half = Fraction(44, 43), Fraction(11, 10)
    return Fraction(11, 5), (
        (-lam / 2 + half, -lam / 2 + half, Fraction(1), Fraction(0)),
        (lam * Fraction(11, 20) + half, lam / 2 + half, *rotation(TAN_15)),
    )


def test_a_decimal_pose_is_derived_as_the_importers_adapter_derives_it() -> None:
    raw = POSE_TEXT.encode()
    assert route.derive_decimal_pose(raw, POSE_ROW) == _pose_witness()
    options = {option["name"]: option["value"] for option in POSE_ROW["options"]}
    certificate = upper.decimal_dilation(raw, 2, options)
    derived = (certificate.side, tuple((p.x, p.y, *p.basis) for p in certificate.poses))
    assert derived == _pose_witness()


@pytest.mark.parametrize(
    "change",
    [
        {"offered": "2.3"},
        {"offered": "2.15000000000001"},
        {"options": [{"name": "dilation", "value": "43/42"}, POSE_ROW["options"][1]]},
        {"options": POSE_ROW["options"][:1]},
    ],
)
def test_a_decimal_pose_off_its_ceiling_or_dilation_is_refused(change: dict[str, Any]) -> None:
    with pytest.raises(AreaRouteError):
        route.derive_decimal_pose(POSE_TEXT.encode(), {**POSE_ROW, **change})


def test_a_markdown_table_row_is_read_by_its_cells() -> None:
    table = b"# Records\n\n| n | S |\n|---:|---|\n| 132 | 11.986956226066 | note |\n"
    assert route.printed_rows(table, "README.md")[-1] == ["132", "11.986956226066", "note"]
    assert route.printed_rows(b"n,exact\n2,12/5\n", "summary.csv") == [
        ["n", "exact"],
        ["2", "12/5"],
    ]


def _fact_text(side: Fraction, placements: tuple[route.Placed, ...]) -> str:
    squares = "".join(
        f"  - id: {index}\n    center: ['{x}', '{y}']\n    basis: ['{c}', '{s}']\n"
        for index, (x, y, c, s) in enumerate(placements, start=1)
    )
    return (
        f"witness:\n  n: {len(placements)}\n  side: '{side}'\n  square_size: '1'\n"
        "  representation: center-basis\n  scalar:\n    kind: rational\n"
        "  coordinates:\n    origin: lower-left\n    axes: x-right-y-up\n  squares:\n" + squares
    )


@pytest.fixture
def pose_packet(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    """A #470-style packet of two derived squares, with its pose file and README at a pin."""
    monkeypatch.setattr(route, "REPO", tmp_path)
    commit = "1" * 40
    upstream = tmp_path / "upstream"
    (upstream / "certificates").mkdir(parents=True)
    (upstream / POSE_ROW["path"]).write_text(POSE_TEXT, encoding="utf-8")
    readme = "| n | S |\n|---:|---|\n| 2 | 2.2 |\n"
    (upstream / "README.md").write_text(readme, encoding="utf-8")
    packet = tmp_path / "packet"
    (packet / "acquisition").mkdir(parents=True)
    (packet / "facts").mkdir()
    pinned = [
        {"path": path, "sha256": hashlib.sha256((upstream / path).read_bytes()).hexdigest()}
        for path in (POSE_ROW["path"], "README.md")
    ]
    record = {"sources": [{"source_commit": commit, "pinned_only": pinned}]}
    (packet / "acquisition/sources.json").write_text(json.dumps(record), encoding="utf-8")
    row = {**POSE_ROW, "printed_in": f"https://github.com/someone/repo/blob/{commit}/README.md"}
    declaration = {"certificates": [row], "requested": [], "replayed": [2]}
    (packet / "acquisition/report.json").write_text(json.dumps(declaration), encoding="utf-8")
    (packet / "facts/n-002.yaml").write_text(_fact_text(*_pose_witness()), encoding="utf-8")
    return packet, upstream


def test_a_derived_pose_fact_is_held_to_its_pinned_pose_and_readme(
    pose_packet: tuple[Path, Path],
) -> None:
    packet, upstream = pose_packet
    assert route.upstream_problems(packet, upstream, [2]) == (2, [])
    # The default roster is the requested counts, and this count is not requested.
    assert route.upstream_problems(packet, upstream) == (0, [])


def test_a_derived_pose_fact_off_its_rounding_or_print_is_reported(
    pose_packet: tuple[Path, Path],
) -> None:
    packet, upstream = pose_packet
    fact = packet / "facts/n-002.yaml"
    side, placements = _pose_witness()
    x, y, _c, _s = placements[1]
    moved = (placements[0], (x, y, *rotation(TAN_15 + Fraction(1, 10**32))))
    fact.write_text(_fact_text(side, moved), encoding="utf-8")
    assert route.upstream_problems(packet, upstream, [2]) == (
        2,
        ["packet n=2: the fact is not the packing certificates/square-2.txt states"],
    )
    (upstream / "README.md").write_text("| n | S |\n| 2 | 2.3 |\n", encoding="utf-8")
    _held, problems = route.upstream_problems(packet, upstream, [2])
    assert "packet: README.md is not the file the packet pins" in problems


def test_a_retained_certificate_is_held_to_its_upstream_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(route, "REPO", tmp_path)
    packet = tmp_path / "packet"
    (packet / "acquisition").mkdir(parents=True)
    (packet / "source/run").mkdir(parents=True)
    (packet / "source/run/n2.cert").write_text("2 2\n1/2 1/2 0\n3/2 1/2 0\n", encoding="utf-8")
    source = {"source_commit": "2" * 40, "pinned_only": [], "archived_path": "packet/source"}
    (packet / "acquisition/sources.json").write_text(
        json.dumps({"sources": [source]}), encoding="utf-8"
    )
    row = {"n": 2, "path": "run/n2.cert", "format": "evand-cert", "offered": "2"}
    declaration = {"certificates": [row], "requested": [2]}
    (packet / "acquisition/report.json").write_text(json.dumps(declaration), encoding="utf-8")
    upstream = tmp_path / "upstream"
    (upstream / "run").mkdir(parents=True)
    (upstream / "run/n2.cert").write_bytes((packet / "source/run/n2.cert").read_bytes())
    assert route.upstream_problems(packet, upstream) == (1, [])
    (upstream / "run/n2.cert").write_text("2 2\n1/2 1/2 0\n3/2 3/2 0\n", encoding="utf-8")
    assert route.upstream_problems(packet, upstream) == (
        1,
        ["packet n=2: the retained run/n2.cert differs"],
    )


MISHAPOLK_470 = (
    84, 86, 88, 103, 105, 108, 127, 130, 131, 132, 153, 154, 175, 179, 180,
    199, 207, 208, 209, 236, 237, 238, 239, 258, 263, 267, 270, 302, 303, 306,
)  # fmt: skip


def test_the_later_roster_is_all_thirty_of_470_and_the_n126_certificate() -> None:
    found = [(case.issue, case.n) for case in route.import_cases(("#470", "trio126"))]
    assert found == [*(("#470", n) for n in MISHAPOLK_470), ("trio126", 126)]


def test_the_488_roster_is_the_counts_its_entry_cites() -> None:
    found = [(case.issue, case.n) for case in route.import_cases(("#488",))]
    assert found == [
        *(("#488", n) for n in (132, 175, 209, 237, 270, 305)),
    ]


def test_the_n126_import_agrees_with_its_receipt_plan_and_print_to_every_digit() -> None:
    case = route.import_cases(("trio126",))[0]
    row = route.decide_import(case)
    packet = route.WEB / case.packet
    maintained = upper.check_certification(packet)[126]
    claim = route.PLAN_CLAIM.findall(upper.register_plan(packet)["results.yaml"]["claim"])
    frozen = upper.check_claims(packet)["results"][0]
    offered = "11742640687119285146522492579501/1000000000000000000000000000000"
    assert row["passed"]
    assert row["wall_clearance"] == "1/200000000000000000000"
    assert all(row["controls"].values())
    claimed = literal(claim[0][1])
    assert route.compare_import(row, maintained, claimed, frozen, offered) == []
    uncited = route.compare_import(row, maintained, claimed, frozen, offered, cited=False)
    where = f"trio126 n=126 ({case.packet})"
    assert uncited == [f"{where}: the register plan claims a count its entry does not cite"]


def test_an_arrangement_matches_its_own_symmetric_copy_and_counts_a_moved_square() -> None:
    side = Fraction(12, 5)
    pair = tuple(
        placed(
            (
                (Fraction(1, 2), Fraction(3, 5), Fraction(0)),
                (Fraction(17, 10), Fraction(7, 10), HALF_TURN),
            )
        )
    )
    mirrored = tuple(reversed([route.symmetric(side, square, 5) for square in pair]))
    gap = route.arrangement_gap((side, pair), (side, mirrored))
    assert gap["largest_squared"] == "0"
    assert gap["largest_orientation_sine"] == "0.000000e+00"
    assert gap["moved_beyond"] == dict.fromkeys(("1e-9", "1e-6", "1e-3", "1e-2", "1e-1"), 0)
    assert gap["turned_beyond_1e-6"] == 0
    x, y, c, s = pair[1]
    moved = (pair[0], (x + Fraction(1, 100) + TINY, y, c, s))
    found = route.arrangement_gap((side, pair), (side, moved))
    assert found["moved_beyond"] == {"1e-9": 1, "1e-6": 1, "1e-3": 1, "1e-2": 1, "1e-1": 0}
    turned = (pair[0], (x, y, *rotation(HALF_TURN + Fraction(1, 1000))))
    assert route.arrangement_gap((side, pair), (side, turned))["turned_beyond_1e-6"] == 1


def test_the_credited_certificates_are_read_as_their_entries_state_them() -> None:
    side, placements = route.ryxu_packing(126)
    assert side == Fraction(14678300859014678300859, 1250000000000000000000)
    assert len(placements) == 126
    side, placements = route.squish_update_packing(258)
    assert side == Fraction(582774517581285, 35184372088832)
    assert len(placements) == 258
    assert decide_placed(side, placements).passed


def test_the_470_witness_at_103_is_ryan_xus_packing_square_for_square() -> None:
    case = next(case for case in route.import_cases(("#470",)) if case.n == 103)
    gap = route.arrangement_gap((case.side, case.placements), route.ryxu_packing(103))
    assert gap["symmetry"] == 0
    assert gap["moved_beyond"]["1e-9"] == 0
    assert gap["turned_beyond_1e-6"] == 0
