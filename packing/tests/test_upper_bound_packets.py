"""The September 2026 parallel upper-bound packets, their certificates and their records."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from fractions import Fraction

import pytest

from devtools import apply_exact_optima as exact_optima
from devtools import apply_upper_bound_packets as apply
from devtools import upper_bound_packets as packets
from devtools.check_case_prose import Reading
from devtools.source_supersession import superseded_counts
from sqpack.assurance import bounds_agree_at_declared_precision
from sqpack.witness import witness_document
from sqpack.yamlio import safe_load

#: Where the certified ceiling sits above the printed side: n = 206, 259 and 305, measured
#: on 2026-09-29, and n = 306 at Couzo's revision of 3 October, measured on 2026-10-05.
TRAILING = {206, 259, 305, 306}


def test_the_verified_value_is_the_larger_of_the_printed_and_certified_sides() -> None:
    assert packets.verified_value("1.25", Fraction(5, 4)) == "1.25"
    assert packets.verified_value("1.25", Fraction(124, 100)) == "1.25"
    assert packets.verified_value("1.25", Fraction(1250000001, 10**9)) == "1.26"
    assert packets.units_above("1.25", Fraction(1250000001, 10**9)) == 1
    assert packets.units_above("1.25", Fraction(124, 100)) == 0
    assert packets.derived("1.25", Fraction(124, 100)) == {
        "units_above_printed": 0,
        "verified_value": "1.25",
        "exact_form": "5/4",
    }
    assert packets.exact_form("1.26") == "63/50"


def test_a_franciscouzo_file_is_read_by_its_header_and_rows() -> None:
    text = "# n = 2\n# s = 2.0\n# x y theta(rad)\n0.5 0.5 0\n1.5 0.5 0\n"
    assert packets.parse_couzo(text) == (2, "2.0", [("0.5", "0.5", "0"), ("1.5", "0.5", "0")])
    with pytest.raises(ValueError, match="rows"):
        packets.parse_couzo(text + "1.5 1.5 0\n")
    with pytest.raises(ValueError, match="franciscouzo"):
        packets.parse_couzo("# n = 2\n" + text)


def _two_squares() -> str:
    """Two unit squares side by side in a 2 x 1 box, as an exact rational witness."""
    squares = [
        {"id": 1, "corners": [["0", "0"], ["1", "0"], ["1", "1"], ["0", "1"]]},
        {"id": 2, "corners": [["1", "0"], ["2", "0"], ["2", "1"], ["1", "1"]]},
    ]
    witness = {
        "id": "W-control",
        "n": 2,
        "side": "2",
        "square_size": "1",
        "representation": "corners",
        "scalar": {"kind": "rational"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": squares,
        "claim": {
            "coordinate_provenance": "verified",
            "method": "exact-algebraic",
            "limitations": "control",
        },
        "source": {"path": "control"},
    }
    return witness_document(witness)


def test_the_negative_controls_fail_both_ways_on_a_packing_that_passes() -> None:
    text = _two_squares()
    assert packets.independent_check(text)["verification_passed"]
    shrunk = packets.independent_check(packets.shrink_side(text))
    assert not shrunk["verification_passed"]
    assert "container penetration" in shrunk["failures"][0]
    moved = packets.independent_check(packets.shift_square(text, 1, Fraction(1, 10**6)))
    assert not moved["verification_passed"]
    assert "overlapping" in moved["failures"][0]


@pytest.mark.parametrize("source", packets.SOURCES, ids=lambda source: source.id)
def test_each_retained_packet_is_consistent_with_its_receipts(source: packets.Source) -> None:
    assert packets.fast_problems(source) == []


def test_every_certificate_verifies_and_the_trailing_cases_are_the_measured_four() -> None:
    trailing = set()
    for source in packets.CERTIFIED:
        for n, row in packets.certification(source).items():
            assert row["independent"]["verification_passed"], n
            assert row["center_dilation"] == "1", n
            increase = Fraction(row["certified_side"]) - Fraction(row["printed_side"])
            assert abs(increase) < Fraction(22, 10**16) or source is packets.DE_WINTER, n
            if row["units_above_printed"] > 1:
                trailing.add(n)
    assert trailing == TRAILING


def test_the_casson_packings_are_each_larger_than_couzos() -> None:
    couzo = packets.cases(packets.FRANCISCOUZO)
    casson = packets.cases(packets.CASSON)
    assert len(casson) == 39
    assert set(casson) <= set(couzo)
    for n, case in casson.items():
        assert Decimal(case["side"]) > Decimal(couzo[n]["side"]), n


def test_the_records_are_what_the_apply_tool_writes() -> None:
    assert apply.main(["--check"]) == 0


def _historical_body(plan: apply.Plan) -> str:
    """Audit this frozen packet's attributed prose independently of later selections."""
    earlier = apply.earlier_reports()[plan.n]
    return apply.packing_section(
        plan,
        "## The packing\n\nThe retained earlier construction.",
        earlier["kingbird"],
        earlier.get("unitsquare"),
    )


def _later_counts() -> set[int]:
    coverage = safe_load(apply.COVERAGE.read_text())
    return superseded_counts(
        coverage,
        {exact_optima.COVERAGE_ID}
        | {registration.coverage_id for registration in apply.REGISTRATIONS},
    )


def test_a_case_trails_its_report_exactly_where_the_certificate_does() -> None:
    """Where a packet's certificate trails its printed side the record says so, except at
    the counts whose packing Evan Daniel solved exactly (T-098), which every trailing
    count is: there both lanes hold the exact optimum, and the trailing goes with the
    printed side it was about."""
    exact = set(exact_optima.certificates.IMPROVING)
    assert exact >= TRAILING
    for plan in apply.plans():
        case = safe_load(
            (apply.FRONTIER / f"n-{plan.n:03d}.md")
            .read_text(encoding="utf-8")
            .split("---\n")[1]
        )["packing"]
        if plan.n in _later_counts():
            # The newer report is separately reviewed; retain this packet's receipts
            # and evidence without pretending its geometry is still the best known.
            assert plan.registration.report in case["evidence"], plan.n
            assert plan.registration.replay in case["evidence"], plan.n
            continue
        agrees = bounds_agree_at_declared_precision(
            case["reported_upper_bound"], case["verified_upper_bound"]
        )
        kinds = {conflict["kind"] for conflict in case["conflicts"]}
        if plan.n in exact:
            assert agrees, plan.n
            assert case["verified_upper_bound"]["evidence"] == [
                exact_optima.EXACT_REPLAY,
                exact_optima.SOURCE_REPLAY,
            ]
            assert "replay-failure" not in kinds, plan.n
            continue
        assert agrees == (plan.n not in TRAILING), plan.n
        assert case["verified_upper_bound"]["evidence"] == [
            plan.registration.replay,
            plan.registration.interval_replay,
        ]
        assert ("replay-failure" in kinds) == (plan.n in TRAILING), plan.n


def test_shared_counts_state_both_sources_dates_and_values() -> None:
    for plan in apply.plans():
        if plan.casson is None:
            continue
        body = _historical_body(plan)
        # The sides are math; read back, each is the code span it was written as.
        flat = " ".join(Reading.of(body).text.split())
        assert f"`{plan.casson['side']}`" in flat, plan.n
        assert f"`{plan.case['history'][0]['side']}`" in flat, plan.n
        first = apply.day(plan.case["history"][0]["authored_utc"])
        assert "dated 23 September 2026 and made with the help of Claude" in flat, plan.n
        assert f"`{plan.case['history'][0]['side']}`, is dated {first}" in flat, plan.n
        assert "infers nothing about whether either packing derives" in flat, plan.n
        # Which is the earlier is said only as firmly as the timestamps allow. Where
        # Couzo's packing was authored before Casson's commit and the history now public
        # was committed after it, the body says both.
        casson_time = datetime.fromisoformat(str(plan.casson["first_authored_utc"]))
        history = plan.case["history"][0]
        if datetime.fromisoformat(history["authored_utc"]) < casson_time:
            assert f"is dated {first}, before Casson\u2019s" in flat, plan.n
            assert "The priority notes keep the timestamps." in flat, plan.n
            recommitted = datetime.fromisoformat(history["committed_utc"]) > casson_time
            caveat = (
                f"the history now public was committed on {apply.day(history['committed_utc'])}"
                ", after it"
            )
            assert (caveat in flat) == recommitted, plan.n
        else:
            assert "Casson\u2019s is the earlier of the two by the timestamps" in flat, plan.n
            assert "before Casson\u2019s" not in flat, plan.n


def test_the_body_gives_plain_dates_and_the_priority_notes_keep_the_timestamps() -> None:
    """A sentence dates a packing by its day; the time of day and the revision that order
    two claims made on one day are the front matter's `priority_notes`."""
    for plan in apply.plans():
        text = (apply.FRONTIER / f"n-{plan.n:03d}.md").read_text(encoding="utf-8")
        _, front, body = text.split("---\n", 2)
        assert "UTC" not in body, plan.n
        assert "clock" not in body, plan.n
        assert plan.registration.source.revision[:7] not in body, plan.n
        if plan.casson is None:
            continue
        first = plan.case["history"][0]
        kept = [note["published"] for note in safe_load(front)["packing"]["priority_notes"]]
        cassons, couzos = (note["published"] for note in apply.priority_notes(plan))
        assert cassons in kept, plan.n
        assert couzos in kept, plan.n
        assert f"committed {plan.casson['first_authored_utc']}" in cassons, plan.n
        assert "(2026-09-23 22:45 UTC-6)" in cassons, plan.n
        assert f"authored {first['authored_utc']}" in couzos, plan.n
        assert f"committed {first['committed_utc']}" in couzos, plan.n


def test_issue_227_dates_a_claim_only_at_the_shared_count_it_names() -> None:
    """The issue names 102 and 103; Casson reports only 103, so only 103 cites its date."""
    for plan in apply.plans():
        body = (apply.FRONTIER / f"n-{plan.n:03d}.md").read_text(encoding="utf-8")
        flat = " ".join(body.split())
        cited = "opened on 23 September 2026, already linked Couzo\u2019s repository" in flat
        assert cited == (plan.n == 103), plan.n


def test_couzos_ai_statement_is_quoted_for_the_counts_it_names() -> None:
    """Issue #227 speaks of the 102 and 103 packings, never of all 49."""
    for plan in apply.plans():
        if plan.registration.source.layout != "couzo":
            continue
        body = _historical_body(plan)
        flat = " ".join(body.split())
        quoted = "found the 102 and 103 packings \u201cwith the help of Claude\u201d"
        assert quoted in flat, plan.n
        assert "itself states no AI assistance" in flat, plan.n
        assert "found the packings" not in flat, plan.n


def test_the_october_packet_keeps_exactly_the_sides_couzo_lowered() -> None:
    """The 3 October packet follows the 27 September one and keeps each count whose side
    changed, each below the side it replaces, and no other."""
    later = packets.FRANCISCOUZO_2026_10_03
    assert later.supersedes == packets.FRANCISCOUZO.id
    earlier = packets.cases(packets.FRANCISCOUZO)
    kept = packets.cases(later)
    assert sorted(kept) == [208, 209, 228, 263, 272, 303, 306]
    for n, case in kept.items():
        assert Decimal(case["side"]) < Decimal(earlier[n]["side"]), n
        assert [entry["side"] for entry in case["history"]][-2:] == [
            earlier[n]["side"],
            case["side"],
        ], n
    pinned = {entry["path"] for entry in packets.acquisition(later)["files"]}
    first = packets.acquisition(packets.FRANCISCOUZO)["files"]
    assert pinned == {entry["path"] for entry in first}


def test_a_later_registration_takes_a_count_and_keeps_the_earlier_packing() -> None:
    """At each count the October packet lowered, the record reports and verifies its side,
    still cites the September evidence, and states the packing it replaced."""
    taken = [plan for plan in apply.plans() if plan.previous is not None]
    assert sorted(plan.n for plan in taken) == [208, 209, 228, 263, 272, 303, 306]
    for plan in taken:
        earlier = plan.previous
        assert earlier is not None
        assert earlier.registration.result == "T-056"
        assert plan.registration.result == "T-092"
        text = (apply.FRONTIER / f"n-{plan.n:03d}.md").read_text(encoding="utf-8")
        _, front, _body = text.split("---\n", 2)
        case = safe_load(front)["packing"]
        # All seven are among Evan Daniel's exact optima (T-098), so both lanes hold
        # that side; the October packing stays the one the body describes.
        if plan.n not in _later_counts():
            assert case["reported_upper_bound"]["value"] == exact_optima.side_text(plan.n)
            assert case["verified_upper_bound"]["value"] == exact_optima.side_text(plan.n)
        assert plan.registration.replay in case["evidence"], plan.n
        assert earlier.registration.replay in case["evidence"], plan.n
        flat = " ".join(Reading.of(_historical_body(plan)).text.split())
        assert f"It replaces his packing of side `{earlier.side}`" in flat, plan.n
        assert flat.count("earlier packing for this count") == 1, plan.n
        assert f"certified `s({plan.n}) ≤ {earlier.verified}` from it" in flat, plan.n
        assert "Before that intake" in flat, plan.n
        assert "Before this intake" not in flat, plan.n
