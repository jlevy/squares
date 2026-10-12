"""`devtools.check_half_angle_area`: the third exact route for the 2026-10-10 reviews."""

from __future__ import annotations

import gzip
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
    read_pingyou_json,
    read_squish_json,
    read_witness_corners,
    rotation,
    unit_basis,
)
from sqpack.yamlio import load_yaml

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


def test_a_printed_side_whose_file_was_not_fetched_is_reported(
    mock_packet: tuple[Path, Path],
) -> None:
    packet, upstream = mock_packet
    (upstream / "run/summary.csv").unlink()
    assert route.upstream_problems(packet, upstream) == (
        1,
        [f"packet: no upstream run/summary.csv in {upstream}"],
    )


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


def test_the_488_and_489_rosters_are_the_counts_their_entries_cite() -> None:
    found = [(case.issue, case.n) for case in route.import_cases(("#488", "#489"))]
    assert found == [
        *(("#488", n) for n in (132, 175, 209, 237, 270, 305)),
        *(("#489", n) for n in (132, 308, 343, 344)),
    ]


REGULARIZED = (70, 102, 103, 123, 129, 146, 153, 236, 258, 263, 269, 292, 295, 302, 303)


def test_the_regularized_roster_is_its_fifteen_gzipped_certificates_read_alike() -> None:
    """Each original gzip is decompressed here and read by this route's own parser."""
    found = route.import_cases(("regularized",))
    assert [(case.issue, case.n) for case in found] == [("regularized", n) for n in REGULARIZED]
    admitted_sides = upper.read_facts(route.WEB / route.ALL_IMPORTS["regularized"])
    for case in found:
        assert case.read == f"source/search/regularize/lists/certs/n-{case.n:03d}.cert.gz"
        assert case.side == admitted_sides[case.n].side
        assert len(case.placements) == case.n
    # Each count is measured against the packing T-146's `regularizations` credit, read
    # from the register: Ryan Xu's alone at 70, Mishapolk's refinements at 103 and 258.
    assert {n: route.credited("regularized", n) for n in (70, 103, 258, 303)} == {
        70: ("T-125",),
        103: ("T-138",),
        258: ("T-138",),
        303: ("T-136",),
    }


def test_each_regularized_count_is_measured_against_the_packing_the_register_credits() -> None:
    """The register's `regularizations` replace a hand-kept map: every count T-146 states
    is credited to the result its item names, and that result has a reader here."""
    register = load_yaml(route.RESULTS.read_text(encoding="utf-8"))
    (t146,) = (result for result in register["results"] if result["id"] == "T-146")
    named = {item["n"]: (item["of"],) for item in t146["regularizations"]}
    assert sorted(named) == list(REGULARIZED)
    assert {n: route.credited("regularized", n) for n in REGULARIZED} == named
    assert {of for (of,) in named.values()} <= set(route.CREDITED_READERS)
    # The fixed pairs of the earlier imports are not regularizations and stay as they were.
    assert route.credited("trio126", 126) == ("T-125",)
    assert route.credited("#470", 258) == ("T-115",)
    assert route.credited("#476", 263) == ()


def _gzip(text: str) -> bytes:
    """Deterministic gzip of ``text``, as an upstream list might store a certificate."""
    return gzip.compress(text.encode("utf-8"), mtime=0)


def test_a_retained_upstream_gzip_is_held_to_its_stored_bytes_and_its_json_print(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(route, "REPO", tmp_path)
    packet = tmp_path / "packet"
    (packet / "acquisition").mkdir(parents=True)
    (packet / "source/certs").mkdir(parents=True)
    certificate = _gzip("2 2\n1/2 1/2 0\n3/2 1/2 0\n")
    printed = _gzip(json.dumps({"n": 2, "S_cert": "2", "S_exact": "2"}))
    (packet / "source/certs/n-002.cert.gz").write_bytes(certificate)
    (packet / "source/certs/n-002.json.gz").write_bytes(printed)
    pin = "2" * 40
    source = {"source_commit": pin, "pinned_only": [], "archived_path": "packet/source"}
    (packet / "acquisition/sources.json").write_text(
        json.dumps({"sources": [source]}), encoding="utf-8"
    )
    row = {
        "n": 2,
        "path": "certs/n-002.cert.gz",
        "format": "evand-cert",
        "offered": "2",
        "printed_in": f"https://github.com/a/b/blob/{pin}/certs/n-002.json.gz",
    }
    declaration = {"certificates": [row], "requested": [2]}
    (packet / "acquisition/report.json").write_text(json.dumps(declaration), encoding="utf-8")
    assert route.packet_bytes(packet / "source/certs/n-002.cert.gz").startswith(b"2 2\n")
    upstream = tmp_path / "upstream"
    (upstream / "certs").mkdir(parents=True)
    (upstream / "certs/n-002.cert.gz").write_bytes(certificate)
    (upstream / "certs/n-002.json.gz").write_bytes(printed)
    assert route.upstream_problems(packet, upstream) == (2, [])
    # The same content in another gzip header is other stored bytes.
    other = gzip.compress(b"2 2\n1/2 1/2 0\n3/2 1/2 0\n", mtime=1)
    (upstream / "certs/n-002.cert.gz").write_bytes(other)
    assert route.upstream_problems(packet, upstream) == (
        2,
        ["packet n=2: the retained certs/n-002.cert.gz differs"],
    )
    (upstream / "certs/n-002.cert.gz").write_bytes(certificate)
    elsewhere = _gzip(json.dumps({"n": 2, "S_cert": "21/10"}))
    (packet / "source/certs/n-002.json.gz").write_bytes(elsewhere)
    (upstream / "certs/n-002.json.gz").write_bytes(elsewhere)
    assert route.upstream_problems(packet, upstream) == (
        1,
        ["packet n=2: certs/n-002.json.gz prints another side than the row offers"],
    )
    (upstream / "certs/n-002.json.gz").write_bytes(printed)
    assert route.upstream_problems(packet, upstream) == (
        1,
        ["packet n=2: the retained certs/n-002.json.gz differs"],
    )


def test_a_regularized_slide_too_far_to_match_is_recorded_not_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A gap no symmetry decides is kept with its side difference, and the run goes on."""
    side = Fraction(2)
    grid = tuple(placed(GRID))
    case = route.Imported("regularized", "packet", 4, "certs/n-004.cert.gz", side, grid)
    monkeypatch.setitem(route.CREDITED, ("regularized", 4), ("T-998", "T-999"))
    monkeypatch.setitem(route.CREDITED_READERS, "T-998", lambda _n: (side, grid))
    # Two squares stacked where the grid has two: nearest centres cannot be one to one.
    stacked = (grid[0], grid[0], grid[2], grid[3])
    monkeypatch.setitem(route.CREDITED_READERS, "T-999", lambda _n: (side + TINY, stacked))
    gaps = route.credited_gaps([case])
    assert gaps["regularized n=4 against T-998"]["moved_beyond"]["1e-9"] == 0
    assert gaps["regularized n=4 against T-999"] == {
        "unmatched": "no symmetry matches the two packings square for square",
        "side_difference": "-1/1000000000000000000000000000000",
    }


@pytest.mark.slow
def test_the_489_certificate_at_305_has_488s_side_in_a_quarter_turned_arrangement() -> None:
    """Hunt 3's unnamed n305 certificate states exactly the side #488 reports there.

    No entry cites it, so no roster reads it; this route's own parser reads both files
    after their packets' custody, and `route.arrangement_gap` measures them, for credit.
    """
    packings = []
    for issue, path in (
        ("#489", "search/packer/candidates/hunt3_n305.cert"),
        ("#488", "certificates/n305.cert"),
    ):
        packet = route.WEB / route.ALL_IMPORTS[issue]
        upper.read_facts(packet)
        source = route.REPO / upper.acquisition(packet)["archived_path"]
        side, poses = parse_certificate(route.packet_bytes(source / path).decode("utf-8"), 305)
        packings.append((side, tuple(placed(poses))))
    (hunt_side, _), (couzo_side, _) = packings
    assert hunt_side == couzo_side == Fraction(8975569886103498772971256586313, 5 * 10**29)
    gap = route.arrangement_gap(packings[0], packings[1])
    assert (gap["symmetry"], gap["side_difference"]) == (1, "0")
    assert gap["moved_beyond"] == {"1e-9": 34, "1e-6": 33, "1e-3": 19, "1e-2": 2, "1e-1": 0}
    assert gap["largest_displacement"] == "1.765499e-2"
    assert gap["turned_beyond_1e-6"] == 3


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


# --------------------------------------------------------------------------- #503 and #504

#: PingYou Ltd's JSON: SQUISH's rows with the four fields its reader leaves unread.
PINGYOU_JSON: dict[str, Any] = {
    **PAIR_JSON,
    "note": "rational centers and t=tan(theta/2)",
    "dilation_exact": "5000000000001/5000000000000",
    "raw_side": 2.4,
    "provenance": {"construction": "two squares", "angle": 53.13},
}
PAIR_SIDE = Fraction(12, 5)
PAIR = tuple(
    placed(
        (
            (Fraction(1, 2), Fraction(3, 5), Fraction(0)),
            (Fraction(17, 10), Fraction(7, 10), HALF_TURN),
        )
    )
)


def test_the_503_and_504_rosters_are_one_derived_fact_each() -> None:
    found = route.import_cases(("#503", "#504"))
    assert [(case.issue, case.n, case.read) for case in found] == [
        ("#503", 207, "facts/n-207.yaml"),
        ("#504", 153, "facts/n-153.yaml"),
    ]
    assert found[0].side == Fraction(148809603730436756319360591381170501178639, 10**40)
    assert found[1].side == Fraction(6435006925203522001385040447, 5 * 10**26)


def test_the_pingyou_reader_reads_squish_rows_and_leaves_its_metadata_unread() -> None:
    assert read_pingyou_json(json.dumps(PINGYOU_JSON).encode(), 2) == read_squish_json(
        json.dumps(PAIR_JSON).encode(), 2
    )
    # A field the reader does not know is refused, whatever it holds; so is another count.
    with pytest.raises(AreaRouteError):
        read_pingyou_json(json.dumps({**PINGYOU_JSON, "s_decimal": "2.4"}).encode(), 2)
    with pytest.raises(AreaRouteError):
        read_pingyou_json(json.dumps(PINGYOU_JSON).encode(), 3)


def _corner_witness(
    side: Fraction,
    placements: tuple[route.Placed, ...],
    *,
    start: int = 0,
    frame: dict[str, str] | None = None,
    representation: str = "corners",
) -> str:
    """A corners Witness/v2 in JSON syntax, each square's corners from its ``start``-th."""
    squares = []
    for index, (x, y, c, s) in enumerate(placements, start=1):
        points = [
            [str(x + (a * c - b * s) / 2), str(y + (a * s + b * c) / 2)]
            for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))
        ]
        squares.append({"id": index, "corners": points[start:] + points[:start]})
    witness = {
        "n": len(placements),
        "side": str(side),
        "square_size": "1",
        "representation": representation,
        "scalar": {"kind": "rational"},
        "coordinates": dict(route.CORNER_FRAME) if frame is None else frame,
        "squares": squares,
    }
    return json.dumps({"softschema": {"schema": "witness.schema.yaml"}, "witness": witness})


def test_the_corner_witness_reader_recovers_each_pose_from_its_corners() -> None:
    assert read_witness_corners(_corner_witness(PAIR_SIDE, PAIR).encode(), 2) == (
        PAIR_SIDE,
        PAIR,
    )
    # Corners from the next vertex are the same squares a quarter turn around, read so.
    turned = read_witness_corners(_corner_witness(PAIR_SIDE, PAIR, start=1).encode(), 2)
    assert turned == (PAIR_SIDE, tuple((x, y, -s, c) for x, y, c, s in PAIR))


def _clockwise() -> str:
    """The first pair square alone, its corners listed clockwise."""
    document = json.loads(_corner_witness(PAIR_SIDE, PAIR[:1]))
    document["witness"]["squares"][0]["corners"].reverse()
    return json.dumps(document)


@pytest.mark.parametrize(
    ("text", "n"),
    [
        # Square 1's corners (0, 1/10) and (1, 1/10) moved up: no longer a unit square.
        (_corner_witness(PAIR_SIDE, PAIR).replace('"1/10"', '"1/9"'), 2),
        (_corner_witness(PAIR_SIDE, PAIR).replace('"id": 2', '"id": 3'), 2),
        (
            _corner_witness(
                PAIR_SIDE, PAIR, frame={"origin": "lower-left", "axes": "x-right-y-up"}
            ),
            2,
        ),
        (_corner_witness(PAIR_SIDE, PAIR, representation="center-basis"), 2),
        (_corner_witness(PAIR_SIDE, PAIR).replace('"side": "12/5"', '"side": "0"'), 2),
        (_corner_witness(PAIR_SIDE, PAIR), 3),
        (_clockwise(), 1),
    ],
)
def test_the_corner_witness_reader_refuses_what_is_not_one_unit_square_in_order(
    text: str, n: int
) -> None:
    """A moved corner, an id out of order, another frame, another representation, a
    side that is not positive, another count and corners listed clockwise are refused."""
    assert text != _corner_witness(PAIR_SIDE, PAIR) or n != 2
    with pytest.raises(AreaRouteError):
        read_witness_corners(text.encode(), n)


@pytest.fixture
def pingyou_packet(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    """A derived-fact packet of PingYou's shape: the JSON certificate and the source's
    own corner witness, both pinned and neither retained, and the fact derived from it."""
    monkeypatch.setattr(route, "REPO", tmp_path)
    upstream = tmp_path / "upstream"
    upstream.mkdir()
    (upstream / "n2.cert.json").write_text(json.dumps(PINGYOU_JSON), encoding="utf-8")
    (upstream / "n2-rational.yaml").write_text(
        _corner_witness(PAIR_SIDE, PAIR), encoding="utf-8"
    )
    packet = tmp_path / "packet"
    (packet / "acquisition").mkdir(parents=True)
    (packet / "facts").mkdir()
    _pin(packet, upstream)
    row = {
        "n": 2,
        "path": "n2.cert.json",
        "format": "pingyou-json",
        "offered": "12/5",
        "printed_in": "https://github.com/jlevy/squares/issues/0",
        "same_packing": [{"path": "n2-rational.yaml", "format": "witness-corners"}],
        "fact": "facts/n-002.yaml",
    }
    declaration = {"certificates": [row], "requested": [2]}
    (packet / "acquisition/report.json").write_text(json.dumps(declaration), encoding="utf-8")
    (packet / "facts/n-002.yaml").write_text(_fact_text(PAIR_SIDE, PAIR), encoding="utf-8")
    return packet, upstream


def _pin(packet: Path, upstream: Path) -> None:
    """Write the packet's acquisition record pinning both upstream files as they are."""
    pinned = [
        {"path": path, "sha256": hashlib.sha256((upstream / path).read_bytes()).hexdigest()}
        for path in ("n2.cert.json", "n2-rational.yaml")
    ]
    record = {"sources": [{"source_commit": "5" * 40, "pinned_only": pinned}]}
    (packet / "acquisition/sources.json").write_text(json.dumps(record), encoding="utf-8")


def test_a_facts_same_packing_witness_is_held_to_its_pin_and_its_packing(
    pingyou_packet: tuple[Path, Path],
) -> None:
    packet, upstream = pingyou_packet
    assert route.upstream_problems(packet, upstream) == (2, [])
    witness = upstream / "n2-rational.yaml"
    witness.write_bytes(witness.read_bytes() + b"\n")
    assert route.upstream_problems(packet, upstream) == (
        1,
        ["packet: n2-rational.yaml is not the file the packet pins"],
    )
    # Re-pinned at a witness of another packing, one square moved far below binary64.
    x, y, c, s = PAIR[1]
    moved = (PAIR[0], (x + TINY, y, c, s))
    witness.write_text(_corner_witness(PAIR_SIDE, moved), encoding="utf-8")
    _pin(packet, upstream)
    assert route.upstream_problems(packet, upstream) == (
        2,
        ["packet n=2: n2-rational.yaml is not the packing the fact states"],
    )
    # A same-packing format this route has no reader for is reported, not skipped.
    report = packet / "acquisition/report.json"
    report.write_text(report.read_text().replace("witness-corners", "corners-csv"))
    assert route.upstream_problems(packet, upstream) == (
        1,
        ["packet n=2: no reader for corners-csv"],
    )


@pytest.mark.parametrize(
    ("issue", "n", "clearance", "least_distance"),
    [
        ("#504", 153, "1/10000000000000", "1.885826e-13"),
        pytest.param("#503", 207, "1/20000000000", "1.000000e-10", marks=pytest.mark.slow),
    ],
)
def test_the_pingyou_imports_agree_with_their_receipts_plans_and_prints_to_every_digit(
    issue: str, n: int, clearance: str, least_distance: str
) -> None:
    case = route.import_cases((issue,))[0]
    row = route.decide_import(case)
    packet = route.WEB / case.packet
    maintained = upper.check_certification(packet)[n]
    claim = route.PLAN_CLAIM.findall(upper.register_plan(packet)["results.yaml"]["claim"])
    frozen = upper.check_claims(packet)["results"][0]
    assert row["passed"]
    assert row["wall_contacts"] == 0
    assert row["wall_clearance"] == clearance
    assert row["least_distance"] == least_distance
    assert all(row["controls"].values())
    assert (
        route.compare_import(
            row, maintained, literal(claim[0][1]), frozen, frozen["offered_side"]
        )
        == []
    )


def test_lineage_finds_a_placed_dilated_copy_of_a_packing_and_counts_a_turned_square() -> None:
    side = Fraction(2)
    parent = tuple(placed(GRID))
    dilation = Fraction(10000000001, 10000000000)
    child = tuple((dilation * (x + 1), dilation * y, c, s) for x, y, c, s in parent)
    found = route.patch_lineage((2 * side, child), (side, parent), dilation)
    assert found[0] == {
        "symmetry": 0,
        "translation": ["1", "0"],
        "squares": 4,
        "turned_beyond_1e-6": 0,
        "exact": 4,
    }
    x, y, _c, _s = child[3]
    turned = (*child[:3], (x, y, *rotation(Fraction(1, 1000))))
    found = route.patch_lineage((2 * side, turned), (side, parent), dilation)
    assert (found[0]["squares"], found[0]["turned_beyond_1e-6"], found[0]["exact"]) == (4, 1, 3)
    # A square whose basis is written a quarter turn around is the same square, exactly.
    quarter = (*child[:3], (x, y, Fraction(0), Fraction(1)))
    assert route.patch_lineage((2 * side, quarter), (side, parent), dilation)[0]["exact"] == 4
    # Nothing of the parent in a child placed far away: no placement reaches the floor.
    apart = tuple((x + 10, y + 10, c, s) for x, y, c, s in parent[:2])
    assert route.patch_lineage((Fraction(20), apart), (side, parent), Fraction(1)) == []


@pytest.mark.slow
def test_the_n207_certificate_is_two_placed_patches_of_the_n70_and_the_n153_is_not() -> None:
    """#503's 207 holds Evan Daniel's n70 twice, 60 squares at the identity and all 69
    of the second patch under the box's anti-diagonal reflection moved by (6, 6), as its
    provenance states; #504's 153 is reclosed at a new angle and no placement of the n70
    lands more than 31 of its squares within 10^-9, one of them exactly."""
    lineage = route.lineage_gaps(route.import_cases(("#503", "#504")))
    n207 = lineage["#503 n=207 from regularized n=70"]
    assert n207[0] == {
        "symmetry": 0,
        "translation": ["0", "0"],
        "squares": 69,
        "turned_beyond_1e-6": 0,
        "exact": 60,
    }
    assert n207[1] == {
        "symmetry": 5,
        "translation": ["6", "6"],
        "squares": 69,
        "turned_beyond_1e-6": 0,
        "exact": 69,
    }
    n153 = lineage["#504 n=153 from regularized n=70"]
    assert max(patch["squares"] for patch in n153) == 31
    assert max(patch["exact"] for patch in n153) == 1


# --------------------------------------------------------------------------- #505 and #501

#: The pair packing in Daniil Ostashev's sqcert format: his header labels as comments.
SQCERT_TEXT = (
    "# sqcert v1\n# generated-by: sqverify --certify\n# claimed_s: 2.4\n"
    "# delta: 1e-60 (centres and side multiplied by 1 + delta)\n"
    "n 2\ns 12/5\n# x y t\n1/2 3/5 0\n17/10 7/10 1/2\n"
)
BARNETT_146 = (
    "116279649124311595126849961042493265136092670741573762928668277775998122712863"
    "472766532671969348798419026610394581005669/9240437194455113887096299456817024243"
    "377978045957194209468060456305894240222303442118770000000000000000000000000000000"
)
BARNETT_261 = (
    "281511998443714605777671262552678001053511713995864784318453182156213791529093"
    "472577894719178723409384395264262601/168784527733880048005353512381558168574000"
    "40173477095354881922318666694517637251382500000000000000000000000000000"
)
OSTASHEV = {
    155: Fraction(
        64762127034792280678268012662770039849775757530809316735783064762127034792280678268012662770039849775757530809316735783,
        5 * 10**117,
    ),
    156: Fraction(
        8111982883527766297069290937797918339306619994848173142743008111982883527766297069290937797918339306619994848173142743,
        625 * 10**114,
    ),
    211: Fraction(
        74981683606681578473292015533873289965462274509366086287257074981683606681578473292015533873289965462274509366086287257,
        5 * 10**117,
    ),
}


def test_the_505_and_501_rosters_are_the_counts_their_issues_request() -> None:
    """#505's five superseded certificates are replayed by the importer and not read here."""
    found = route.import_cases(("#505", "#501"))
    assert [(case.issue, case.n, case.read) for case in found] == [
        ("#505", 146, "facts/n-146.yaml"),
        ("#505", 261, "facts/n-261.yaml"),
        ("#501", 155, "source/records/n0155.sqcert"),
        ("#501", 156, "source/records/n0156.sqcert"),
        ("#501", 211, "source/records/n0211.sqcert"),
    ]
    sides = {(case.issue, case.n): case.side for case in found}
    assert sides["#505", 146] == literal(BARNETT_146)
    assert sides["#505", 261] == literal(BARNETT_261)
    for n, side in OSTASHEV.items():
        assert sides["#501", n] == side
    report = route.WEB / route.ALL_IMPORTS["#505"] / "acquisition/report.json"
    declaration = json.loads(report.read_text(encoding="utf-8"))
    assert declaration["replayed"] == [70, 103, 123, 146, 237, 261, 295]
    assert route.roster("#505", declaration) == [146, 261]


def test_the_sqcert_reader_reads_the_split_header_and_skips_the_labels() -> None:
    assert route.parse_sqcert(SQCERT_TEXT, 2) == parse_certificate(
        "2 12/5\n1/2 3/5 0\n17/10 7/10 1/2\n", 2
    )
    readers = route.RETAINED_READERS
    assert readers == {"evand-cert": parse_certificate, "sqcert": route.parse_sqcert}


@pytest.mark.parametrize(
    ("text", "n"),
    [
        (SQCERT_TEXT, 3),
        (SQCERT_TEXT.replace("n 2\ns 12/5", "s 12/5\nn 2"), 2),
        (SQCERT_TEXT.replace("n 2\ns 12/5", "2 12/5"), 2),
        (SQCERT_TEXT.replace("n 2\ns 12/5", "n 2"), 2),
        (SQCERT_TEXT.replace("n 2\n", "N 2\n"), 2),
        (SQCERT_TEXT.replace("n 2\n", "n 02\n"), 2),
        (SQCERT_TEXT.replace("s 12/5", "s 0"), 2),
        (SQCERT_TEXT.replace("s 12/5", "s 12/5 1"), 2),
        (SQCERT_TEXT.replace("17/10 7/10 1/2", "17/10 7/10 1/2 0"), 2),
        (SQCERT_TEXT + "1/2 3/2 0\n", 2),
        (SQCERT_TEXT.replace("1/2 3/5 0\n", ""), 2),
    ],
)
def test_the_sqcert_reader_refuses_what_its_format_does_not_state(text: str, n: int) -> None:
    """Another count, the labels swapped or joined, a missing or extra field or row, a
    label in another case or a padded count, and a side that is not positive."""
    with pytest.raises(AreaRouteError):
        route.parse_sqcert(text, n)


def test_the_evand_cert_upstream_reader_is_the_text_reader() -> None:
    raw = b"# a comment\n2 2\n1/2 1/2 0\n3/2 1/2 0\n"
    assert route.read_evand_cert(raw, 2) == parse_certificate(raw.decode(), 2)
    assert route.UPSTREAM_READERS["evand-cert"] is route.read_evand_cert
    with pytest.raises(AreaRouteError):
        route.read_evand_cert(raw, 3)


def test_a_retained_certificates_table_print_is_held_to_its_pinned_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The README a retained certificate's side is printed in must be fetched at the pin,
    be the packet's own copy and print the side in the count's row."""
    monkeypatch.setattr(route, "REPO", tmp_path)
    packet = tmp_path / "packet"
    (packet / "acquisition").mkdir(parents=True)
    (packet / "source/records").mkdir(parents=True)
    certificate = SQCERT_TEXT.encode()
    readme = b"# Records\n\n| n | side |\n|---:|---|\n| 2 | 2.4 |\n"
    (packet / "source/records/n0002.sqcert").write_bytes(certificate)
    (packet / "source/README.md").write_bytes(readme)
    pin = "7" * 40
    source = {"source_commit": pin, "pinned_only": [], "archived_path": "packet/source"}
    (packet / "acquisition/sources.json").write_text(
        json.dumps({"sources": [source]}), encoding="utf-8"
    )
    row = {
        "n": 2,
        "path": "records/n0002.sqcert",
        "format": "sqcert",
        "offered": "2.4",
        "printed_in": f"https://github.com/a/b/blob/{pin}/README.md",
    }
    declaration = {"certificates": [row], "requested": [2]}
    report = packet / "acquisition/report.json"
    report.write_text(json.dumps(declaration), encoding="utf-8")
    upstream = tmp_path / "upstream"
    (upstream / "records").mkdir(parents=True)
    (upstream / "records/n0002.sqcert").write_bytes(certificate)
    (upstream / "README.md").write_bytes(readme)
    assert route.upstream_problems(packet, upstream) == (2, [])
    where = "packet n=2"
    (upstream / "README.md").write_bytes(readme + b"\n")
    assert route.upstream_problems(packet, upstream) == (
        1,
        [f"{where}: the retained README.md differs"],
    )
    (upstream / "README.md").unlink()
    assert route.upstream_problems(packet, upstream) == (
        1,
        [f"{where}: no upstream README.md in {upstream}"],
    )
    elsewhere = readme.replace(b"| 2 | 2.4 |", b"| 3 | 2.4 |")
    (upstream / "README.md").write_bytes(elsewhere)
    (packet / "source/README.md").write_bytes(elsewhere)
    assert route.upstream_problems(packet, upstream) == (
        1,
        [f"{where}: README.md does not print the side"],
    )
    report.write_text(json.dumps(declaration).replace(pin, "8" * 40), encoding="utf-8")
    assert route.upstream_problems(packet, upstream) == (
        1,
        [f"{where}: the side is printed at another commit"],
    )
    # A README the packet pins without retaining is held to its digest instead.
    report.write_text(json.dumps(declaration), encoding="utf-8")
    (packet / "source/README.md").unlink()
    (upstream / "README.md").write_bytes(readme)
    digest = hashlib.sha256(readme).hexdigest()
    source["pinned_only"] = [{"path": "README.md", "sha256": digest}]
    (packet / "acquisition/sources.json").write_text(
        json.dumps({"sources": [source]}), encoding="utf-8"
    )
    assert route.upstream_problems(packet, upstream) == (2, [])
    (upstream / "README.md").write_bytes(readme + b"\n")
    assert route.upstream_problems(packet, upstream) == (
        1,
        [f"{where}: README.md is neither retained nor the file the packet pins"],
    )


def test_the_houses_505_and_501_are_measured_against_are_read_as_their_entries_state() -> None:
    """T-146's regularized view at 146, Couzo's refinement at 155 (T-128) and Evan Daniel's
    exact optima at 156 and 211 (T-098), each read by this route after its packet's custody."""
    side, placements = route.CREDITED_READERS["T-146"](146)
    assert side == Fraction(6291891138707538440974154877957, 5 * 10**29)
    assert len(placements) == 146
    side, placements = route.couzo_refinement_packing(155)
    assert side == Fraction(647624947200700369098292528347, 5 * 10**28)
    assert len(placements) == 155
    side, placements = route.evand_optimum_packing(156)
    assert side == Fraction(3245520674629223275519207125509, 25 * 10**28)
    assert len(placements) == 156
    side, placements = route.evand_optimum_packing(211)
    assert side == Fraction(7498980352483680782590502239189, 5 * 10**29)
    assert len(placements) == 211
    measured = {
        (key, n): route.credited(key, n) for key, n in route.CREDITED if key in {"#505", "#501"}
    }
    assert measured == {
        ("#505", 146): ("T-125", "T-146"),
        ("#505", 261): ("T-125",),
        ("#501", 155): ("T-115", "T-128"),
        ("#501", 156): ("T-098",),
        ("#501", 211): ("T-098",),
    }
    with pytest.raises(AreaRouteError):
        route.evand_optimum_packing(17)


#: #501's least wall clearance at 155 and 156, a corner square's: half of the 1 + 1e-20
#: scaling of the load-bearing squares the source describes, carried through the
#: 1 + 1e-60 dilation; at 211 a tilted square is nearest and its clearance is a longer
#: rational of the same size.
OSTASHEV_WALL = (
    "1000000000000000000000000000000000000000100000000000000000001/" + "2" + "0" * 80
)


@pytest.mark.parametrize(
    ("issue", "n", "clearance", "least_distance"),
    [
        ("#505", 146, "3.925867e-14", "1.206274e-16"),
        pytest.param("#505", 261, "4.688122e-14", "1.206060e-16", marks=pytest.mark.slow),
        ("#501", 155, "5.000000e-21", "5.000000e-21"),
        ("#501", 156, "5.000000e-21", "5.000000e-21"),
        pytest.param("#501", 211, "5.000000e-21", "5.000000e-21", marks=pytest.mark.slow),
    ],
)
def test_the_505_and_501_imports_agree_with_their_receipts_plans_and_prints_to_every_digit(
    issue: str, n: int, clearance: str, least_distance: str
) -> None:
    case = next(case for case in route.import_cases((issue,)) if case.n == n)
    row = route.decide_import(case)
    packet = route.WEB / case.packet
    maintained = upper.check_certification(packet)[n]
    claims = dict(
        route.PLAN_CLAIM.findall(upper.register_plan(packet)["results.yaml"]["claim"])
    )
    frozen = next(r for r in upper.check_claims(packet)["results"] if r["n"] == n)
    assert row["passed"]
    assert row["wall_contacts"] == 0
    assert f"{float(literal(row['wall_clearance'])):.6e}" == clearance
    assert row["least_distance"] == least_distance
    assert all(row["controls"].values())
    if issue == "#501" and n != 211:
        assert row["wall_clearance"] == row["far_wall_clearance"] == OSTASHEV_WALL
    assert (
        route.compare_import(
            row, maintained, literal(claims[str(n)]), frozen, frozen["offered_side"]
        )
        == []
    )


@pytest.mark.slow
def test_barnetts_refinements_are_ryan_xus_packings_moved_and_ostashevs_are_not() -> None:
    """#505's 146 and 261 match Ryan Xu's certificates square for square at the identity,
    261 moved by at most 9.1e-6 and 146 by at most 5.0e-2 (nearer than Evan Daniel's
    regularized view, 0.12); #501's 155 pairs with SQUISH's and Couzo's packings only
    through the aligned corner blocks every packing of this family shares, 50 squares
    turned by up to 27 degrees, and 156 and 211 match the exact optima under no symmetry."""
    gaps = route.credited_gaps(route.import_cases(("#505", "#501")))
    xu146 = gaps["#505 n=146 against T-125"]
    assert (xu146["symmetry"], xu146["largest_displacement"]) == (0, "5.023183e-2")
    assert xu146["moved_beyond"] == {"1e-9": 145, "1e-6": 79, "1e-3": 51, "1e-2": 31, "1e-1": 0}
    assert xu146["turned_beyond_1e-6"] == 24
    daniel146 = gaps["#505 n=146 against T-146"]
    assert (daniel146["symmetry"], daniel146["largest_displacement"]) == (0, "1.224465e-1")
    assert daniel146["moved_beyond"]["1e-1"] == 3
    xu261 = gaps["#505 n=261 against T-125"]
    assert (xu261["symmetry"], xu261["largest_displacement"]) == (0, "9.146345e-6")
    assert xu261["largest_orientation_sine"] == "2.441757e-06"
    assert xu261["moved_beyond"] == {"1e-9": 82, "1e-6": 52, "1e-3": 0, "1e-2": 0, "1e-1": 0}
    for house, beyond_tenth in (("T-115", 13), ("T-128", 14)):
        gap = gaps[f"#501 n=155 against {house}"]
        assert gap["symmetry"] == 0
        assert gap["largest_displacement"].startswith("2.25")
        assert gap["largest_orientation_sine"].startswith("4.57")
        assert gap["moved_beyond"]["1e-1"] == beyond_tenth
        assert gap["turned_beyond_1e-6"] == 50
    for n in (156, 211):
        assert gaps[f"#501 n={n} against T-098"]["unmatched"] == (
            "no symmetry matches the two packings square for square"
        )
