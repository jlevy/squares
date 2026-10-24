"""`upper_bound_reports sharp-controls`: the sharp controls every import copied, once.

The controls (`devtools.upper_bound_sharp_controls`) take a certificate to exact contact
and 1e-30 past it on both maintained exact routes. Negative controls first: the command
refuses counts outside the roster, a receipt another program wrote, and a check with
nothing to check, and the helpers refuse what they do not know. Then each control's
verdict on small packings whose answer is known, and the flip: removing each control's
perturbation turns its verdict, or the failure it makes, back. Last, the retained receipt
of the mishapolk-n204-2026-10-22 packet, which its own program wrote, reproduced route for
route on its certificate; that one decides eleven controls over 20,706 pairs on two routes,
80 to 135 s on a shared host, so it runs in the deep surface.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

EPSILON = sharp.EPSILON
PROFILE = {
    "witness_prefix": kernel.WITNESS_PREFIX,
    "claim_limitations": kernel.CLAIM_LIMITATIONS,
}
#: Three unit squares with room between them and the walls, one turned by
#: tan(theta/2) = 1/3, so every control can close its one pair or wall alone.
ROOMY = legacy.parse("3 4\n1 1 0\n23/10 6/5 1/3\n3/2 3 1/7\n")
#: Two unit squares filling a 2 by 1 strip of a box of side 2: they touch each other and
#: three walls exactly, so no enlargement can close one pair or wall alone.
TOUCHING = legacy.parse("2 2\n1/2 1/2 0\n3/2 1/2 0\n")
N204 = "mishapolk-n204-2026-10-22"
TRANSLATIONS = (sharp.SIDE_LOWERED, sharp.TIGHTEST_PAIR, sharp.NEAR_WALL)
ENLARGEMENTS = (sharp.ENLARGED_PAIR, sharp.ENLARGED_WALL)


@pytest.fixture(scope="module")
def roomy() -> dict[tuple[str, str], dict[str, Any]]:
    return {(row["control"], row["where"]): row for row in sharp.control_rows(ROOMY, PROFILE)}


@pytest.fixture(scope="module")
def touching() -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (row["control"], row["where"]): row for row in sharp.control_rows(TOUCHING, PROFILE)
    }


# --------------------------------------------------------------------------- refusals


def test_the_command_refuses_counts_outside_the_replayed_roster() -> None:
    with pytest.raises(reports.ReportError, match="outside the replayed roster"):
        sharp.run(reports.packet_path(N204), [205], check=False)


def test_the_command_leaves_a_receipt_another_program_wrote() -> None:
    """mishapolk-n204-2026-10-22's receipts/sharp-controls.json is bound to the packet's
    own receipts/sharp_controls.py; the command neither overwrites nor checks it."""
    for check in (False, True):
        with pytest.raises(reports.ReportError, match="another program's receipt"):
            sharp.run(reports.packet_path(N204), None, check=check)
    with pytest.raises(reports.ReportError, match="another program's receipt"):
        reports.main([N204, "sharp-controls"])


def test_a_check_with_no_retained_receipt_is_refused() -> None:
    with pytest.raises(reports.ReportError, match=r"no retained sharp-controls\.json"):
        sharp.run(reports.packet_path("evand-n303-2026-10-22"), None, check=True)


def test_the_helpers_refuse_what_they_do_not_know() -> None:
    with pytest.raises(reports.ReportError, match="no known kind"):
        sharp.failure_kinds("independent", ["the moon is square"])
    with pytest.raises(reports.ReportError, match="no known kind"):
        sharp.failure_kinds("exact_verify", [("tolerance", "close enough")])
    with pytest.raises(reports.ReportError, match="unknown margin rule"):
        sharp.margin_met(Fraction(0), Fraction(0), "near", Fraction(1))


def test_the_window_holds_a_margin_between_epsilon_and_epsilon_times_the_edge() -> None:
    edge = 1 + 2 * Fraction(1, 10**12)
    assert sharp.window(-EPSILON, edge)
    assert sharp.window(-EPSILON * edge, edge)
    assert not sharp.window(-EPSILON * edge - Fraction(1, 10**60), edge)
    assert not sharp.window(-EPSILON + Fraction(1, 10**60), edge)
    assert not sharp.window(Fraction(0), edge)


def test_receipts_are_named_for_a_roster_of_one_count_or_by_count() -> None:
    packet = Path("p")
    assert sharp.receipt_path(packet, [204], 204) == packet / "receipts/sharp-controls.json"
    assert (
        sharp.receipt_path(packet, [68, 268], 68)
        == packet / "receipts/sharp-controls-n068.json"
    )


# --------------------------------------------------------------------------- known answers


def test_every_control_on_a_roomy_packing_is_as_expected(
    roomy: dict[tuple[str, str], dict[str, Any]],
) -> None:
    assert len(roomy) == 2 * (len(TRANSLATIONS) + len(ENLARGEMENTS)) + 1
    for row in roomy.values():
        assert row["as_expected"] is True, row["control"]
        assert set(row["routes"]) == set(kernel.ROUTES)
    for control in ENLARGEMENTS:
        assert roomy[control, "at-contact"]["detail"]["clean"] is True


@pytest.mark.parametrize("control", TRANSLATIONS)
def test_a_translation_is_accepted_at_contact_and_refused_1e30_past_it(
    roomy: dict[tuple[str, str], dict[str, Any]], control: str
) -> None:
    """Removing the 1e-30 flips the verdict: both routes accept at contact with the margin
    exactly 0 and refuse past it at exactly -1e-30, naming the one failure the control
    makes."""
    at, past = roomy[control, "at-contact"], roomy[control, "past-contact"]
    margin = at["margin"]
    for route in kernel.ROUTES:
        assert at["routes"][route]["passed"] is True
        assert at["routes"][route]["failures"] == []
        assert Fraction(at["routes"][route][margin]) == 0
        assert past["routes"][route]["passed"] is False
        assert past["routes"][route]["failures"] == past["expected_failures"]
        assert Fraction(past["routes"][route][margin]) == -EPSILON


@pytest.mark.parametrize(
    ("control", "kind"), [(sharp.ENLARGED_PAIR, "overlap"), (sharp.ENLARGED_WALL, "container")]
)
def test_an_enlargement_meets_contact_for_its_shape_alone_and_crosses_it_1e30_past(
    roomy: dict[tuple[str, str], dict[str, Any]], control: str, kind: str
) -> None:
    """An enlarged square is no unit square, so both routes refuse it at contact for its
    shape alone, with the margin exactly 0; removing the 1e-30 removes the overlap or the
    wall, and removing the enlargement leaves the certificate, which both accept."""
    at, past = roomy[control, "at-contact"], roomy[control, "past-contact"]
    margin = at["margin"]
    for route in kernel.ROUTES:
        assert at["routes"][route]["failures"] == ["shape"]
        assert Fraction(at["routes"][route][margin]) == 0
        assert past["routes"][route]["failures"] == sorted({"shape", kind})
        assert Fraction(past["routes"][route][margin]) <= -EPSILON
    unperturbed = sharp.decide(ROOMY, PROFILE)
    for route in kernel.ROUTES:
        assert unperturbed[route]["passed"] is True
        assert unperturbed[route]["failures"] == []


def test_the_duplicate_square_is_refused_and_the_certificate_without_it_accepted(
    roomy: dict[tuple[str, str], dict[str, Any]],
) -> None:
    row = roomy[sharp.DUPLICATE, "gross"]
    for route in kernel.ROUTES:
        assert row["routes"][route]["passed"] is False
        assert row["routes"][route]["failures"] == ["overlap"]
        assert Fraction(row["routes"][route]["gap"]) == -1
        assert sharp.decide(ROOMY, PROFILE)[route]["passed"] is True


def test_an_enlargement_of_a_square_that_touches_exactly_is_predicted_and_met(
    touching: dict[tuple[str, str], dict[str, Any]],
) -> None:
    """In a certificate whose squares touch exactly no enlargement closes one pair or wall
    alone, and the tightest pair's square, or the square nearest a wall, is grown anyway.
    Its gap is 0, so at contact it is the certificate itself, which both routes accept;
    past contact it crosses the walls and its partner at once, as predicted."""
    for row in touching.values():
        assert row["as_expected"] is True, (row["control"], row["where"])
    for control in ENLARGEMENTS:
        at, past = touching[control, "at-contact"], touching[control, "past-contact"]
        assert at["detail"]["clean"] is False
        assert Fraction(at["detail"]["half_edge_grown_by"]) == 0
        assert at["expected"] == "accepted"
        assert past["expected_failures"] == ["container", "overlap", "shape"]
    pair = touching[sharp.ENLARGED_PAIR, "past-contact"]
    assert pair["margin_rule"] == sharp.AT_MOST
    wall = touching[sharp.ENLARGED_WALL, "past-contact"]
    assert (wall["margin_rule"], wall["expected_margin"]) == (
        sharp.EQUAL,
        legacy.literal(-EPSILON),
    )


def test_an_enlargement_closes_its_pair_at_exactly_the_growth_it_names() -> None:
    """`contact_enlargement` is exact: grown by it, the pair's gap is 0, and grown past
    it, -1e-30 on unit normals."""
    found = sharp.enlarged_pair(ROOMY)
    square, partner = found["square"], found["partner"]
    other = legacy.corner_squares(ROOMY)[partner]
    grown = sharp.enlarge(ROOMY.poses[square], found["at"])
    assert legacy.independent.pair_gap(grown, other) == 0
    past = sharp.enlarge(ROOMY.poses[square], found["past"])
    assert sharp.window(legacy.independent.pair_gap(past, other), 1 + 2 * found["past"])


# --------------------------------------------------------------------------- the command


def test_the_command_writes_a_receipt_and_checks_it_again(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Writing and checking, with the deciding replaced by a record of the roomy packing's
    controls and the receipt kept in scratch space: a check holds every field but the
    times, and refuses a receipt that differs."""
    record = {"format": sharp.FORMAT, "controls": sharp.control_rows(ROOMY, PROFILE)}
    path = tmp_path / "sharp-controls.json"
    monkeypatch.setattr(sharp, "receipt_path", lambda _packet, _roster, _n: path)
    monkeypatch.setattr(sharp.reports, "ensure_private", lambda _path: None)
    monkeypatch.setattr(
        sharp, "sharp_controls", lambda _packet, _n: {**record, "all_as_expected": True}
    )
    packet = reports.packet_path(N204)
    assert sharp.run(packet, None, check=False) == {204: True}
    written = json.loads(path.read_text("utf-8"))
    assert written["format"] == sharp.FORMAT
    for row in written["controls"]:
        row["cpu_seconds"] = 0.0
    path.write_text(json.dumps(written), encoding="utf-8")
    assert sharp.run(packet, None, check=True) == {204: True}
    written["controls"][0]["routes"]["independent"]["passed"] = False
    path.write_text(json.dumps(written), encoding="utf-8")
    with pytest.raises(reports.ReportError, match="differs"):
        sharp.run(packet, None, check=True)


# --------------------------------------------------------------------------- the receipt


@pytest.mark.slow
def test_it_reproduces_the_retained_204_receipt_route_for_route() -> None:
    """mishapolk-n204-2026-10-22's receipts/sharp-controls.json, written by the packet's
    own program: its six rows, three controls at contact and past it, reproduced exactly
    on both routes, verdict, wall and gap; and the five rows the program did not write as
    expected too."""
    packet = reports.packet_path(N204)
    retained = json.loads((packet / "receipts/sharp-controls.json").read_text("utf-8"))
    record = sharp.sharp_controls(packet, 204)
    assert record["all_as_expected"] is True
    assert (record["side"], record["epsilon"]) == (retained["side"], retained["epsilon"])
    rows = {(row["control"], row["where"]): row for row in record["controls"]}
    assert len(retained["controls"]) == 6
    for row in retained["controls"]:
        mine = rows[row["control"], row["where"]]
        for route, verdict in row["routes"].items():
            for key in ("passed", "wall", "gap"):
                assert mine["routes"][route][key] == verdict[key], (row["control"], route, key)
