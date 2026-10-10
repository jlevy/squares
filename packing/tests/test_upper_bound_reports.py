"""The declaration-driven importer of rational upper-bound reports, on its two packets.

Every test reads retained packets only; none needs the network.
"""

from __future__ import annotations

import functools
import gzip
import json
import os
import shutil
import subprocess
from collections.abc import Callable, Mapping
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_source_coverage as coverage_check
from devtools import check_standing
from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools import upper_bound_reports as reports

COUZO = "couzo-exact-certificates-2026-10-09"
FANG = "fang-two-wedge-certificates-2026-10-10"
PACKETS = (COUZO, FANG)
SQUISH_481 = "squish-481-third-request-2026-10-09"
DELEEUW = "ebdeleeuw-n70-refinement-2026-10-10"
DERIVED = (SQUISH_481, DELEEUW)
MISHAPOLK = "mishapolk-decimal-poses-2026-10-09"
#: Issues #488 and #489, two retained Evan Daniel format releases of the same afternoon.
COUZO_488 = "couzo-certificates-2026-10-10"
HUNT3 = "evand-record-hunt3-2026-10-10"
EVERY = (*PACKETS, *DERIVED, MISHAPOLK, COUZO_488, HUNT3)


def _packet(name: str) -> Path:
    return reports.packet_path(name)


@pytest.fixture
def private(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Callable[[str], Path]:
    """Copy a packet into a private repository root and point the importer at it."""
    repo = tmp_path / "private"
    web = repo / reports.WEB.relative_to(reports.REPO)
    monkeypatch.setattr(reports, "REPO", repo)
    monkeypatch.setattr(reports, "WEB", web)
    monkeypatch.setattr(kernel, "REPO", repo)

    def copy(name: str) -> Path:
        target = web / name
        shutil.copytree(reports.ROOT / "resources/web" / name, target)
        return target

    return copy


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- custody


@pytest.mark.parametrize("name", PACKETS)
def test_custody_admits_every_declared_certificate_at_its_printed_side(name: str) -> None:
    packet = _packet(name)
    declaration = reports.load_declaration(packet)
    certificates = reports.read_facts(packet)
    assert list(certificates) == [row["n"] for row in declaration["certificates"]]
    for row in declaration["certificates"]:
        certificate = certificates[row["n"]]
        assert len(certificate.poses) == row["n"]
        places = len(row["offered"].partition(".")[2])
        assert legacy.ceiling_decimal(certificate.side, places) == row["offered"]


def test_the_couzo_sides_are_the_exact_fractions_the_source_states() -> None:
    certificates = reports.read_facts(_packet(COUZO))
    assert certificates[132].side == Fraction(11986954193640392741450366579623, 10**30)
    assert certificates[263].side == Fraction(
        7488939206954142477014939239, 447356905819500000000000000
    )


def test_each_fang_count_states_one_packing_in_both_retained_formats() -> None:
    packet = _packet(FANG)
    source = reports.REPO / reports.acquisition(packet)["archived_path"]
    certificates = reports.read_facts(packet)
    for n, certificate in certificates.items():
        raw = gzip.decompress((source / f"n{n:04d}/n{n:04d}.cert.json.gz").read_bytes())
        assert reports.parse_certificate(raw, n, "squish-json") == certificate


def test_a_same_packing_file_that_differs_is_refused(
    private: Callable[[str], Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    packet = private(FANG)
    # Custody would refuse the changed file first; the same-packing rule is checked apart.
    monkeypatch.setattr(reports.acquire_source, "check", lambda *_: [])
    stored = packet / "source/n0308/n0308.cert.json.gz"
    value = json.loads(gzip.decompress(stored.read_bytes()))
    value["squares"][5][2] = "1/1000"
    stored.unlink()
    _write_json(stored.with_suffix(""), value)
    with pytest.raises(reports.ReportError, match="states another packing"):
        reports.read_facts(packet)


@pytest.mark.parametrize("mutation", ["certificate-byte", "extra-pose", "licence"])
def test_custody_refuses_a_changed_retained_file(
    private: Callable[[str], Path], mutation: str
) -> None:
    packet = private(COUZO if mutation != "licence" else FANG)
    source = packet / "source"
    if mutation == "certificate-byte":
        path = source / "certificates/n267.cert"
        path.write_text(path.read_text().replace("1", "2", 3))
    elif mutation == "extra-pose":
        path = source / "certificates/n132.cert"
        path.write_text(path.read_text() + "1/2 1/2 0\n")
    else:
        (source / "LICENSE").write_text("All rights reserved.\n")
    with pytest.raises(reports.ReportError, match="packet custody"):
        reports.read_facts(packet)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("format", "import declaration format"),
        ("house-missing", "in-horizon counts"),
        ("reader-and-print", "no printed side beside it"),
        ("unknown-adapter", "unknown format"),
        ("witness-prefix", "witness namespace"),
        ("descending", "unique and ascending"),
        ("replayed-undeclared", "replayed must be"),
        ("requested-empty", "requested must be"),
    ],
)
def test_the_declaration_refuses_what_it_does_not_describe(
    private: Callable[[str], Path], mutation: str, message: str
) -> None:
    packet = private(COUZO)
    path = packet / reports.DECLARATION
    value = _json(path)
    if mutation == "format":
        value["format"] = "upper-bound-report-declaration-v0"
    elif mutation == "house-missing":
        value["houses"].pop(2)
    elif mutation == "reader-and-print":
        value["pending"][0]["printed"] = "11.9"
    elif mutation == "unknown-adapter":
        value["certificates"][0]["format"] = "no-such-format"
    elif mutation == "witness-prefix":
        value["witness_prefix"] = "W_couzo"
    elif mutation == "replayed-undeclared":
        value["replayed"].append(400)
    elif mutation == "requested-empty":
        value["requested"] = []
    else:
        value["certificates"].reverse()
    _write_json(path, value)
    with pytest.raises(kernel.ReportError, match=message):
        reports.load_declaration(packet)


# --------------------------------------------------------------------------- adapters


EVAND = b"# comment\n2 3\n1 1 0\n2 2 1/3\n"
SQUISH = {
    "n": 2,
    "s_exact": "3",
    "s_decimal": "3.0",
    "note": "centre and t",
    "squares": [["1", "1", "0"], ["2", "2", "1/3"]],
}
CENTRED = {
    "schema": "sqpack-rational-v1",
    "n": 2,
    "coordinate_system": "centered",
    "side": "3",
    "squares": [{"x": "-1/2", "y": "-1/2", "t": "0"}, {"x": "1/2", "y": "1/2", "t": "1/3"}],
    "parent_side": "3.0",
    "dilation": "0",
}


def _bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(value).encode()


def test_the_three_adapters_read_one_packing_alike() -> None:
    expected = legacy.parse(EVAND.decode(), expected_n=2)
    assert reports.parse_certificate(EVAND, 2, "evand-cert") == expected
    assert reports.parse_certificate(_bytes(SQUISH), 2, "squish-json") == expected
    # The centred certificate's centres move by S/2 = 3/2, exactly.
    assert reports.parse_certificate(_bytes(CENTRED), 2, "centred-json") == expected


@pytest.mark.parametrize(
    ("form", "value", "message"),
    [
        ("squish-json", {**SQUISH, "squares": [[1, "1", "0"], ["2", "2", "0"]]}, "rational"),
        ("squish-json", {**SQUISH, "extra": "x"}, "unknown"),
        ("squish-json", {**SQUISH, "n": 3}, "count differs"),
        ("squish-json", {**SQUISH, "squares": [["1", "1"], ["2", "2", "0"]]}, "x y t"),
        ("squish-json", {**SQUISH, "s_exact": "1.5"}, "rational"),
        ("centred-json", {**CENTRED, "coordinate_system": "lower-left"}, "not a centred"),
        ("centred-json", {**CENTRED, "origin": "centre"}, "not a centred"),
        ("centred-json", {**CENTRED, "squares": [{"x": "0", "y": "0"}] * 2}, "x, y and t"),
        ("centred-json", {**CENTRED, "side": "-3"}, "positive"),
    ],
)
def test_the_json_adapters_refuse_what_their_formats_do_not_state(
    form: str, value: Mapping[str, Any], message: str
) -> None:
    with pytest.raises(reports.ReportError, match=message):
        reports.parse_certificate(_bytes(value), 2, form)


def test_an_adapter_refuses_options_and_unknown_formats_are_refused() -> None:
    with pytest.raises(reports.ReportError, match="reads no options"):
        reports.parse_certificate(EVAND, 2, "evand-cert", {"dilation": "1"})
    with pytest.raises(reports.ReportError, match="unknown certificate format"):
        reports.parse_certificate(EVAND, 2, "no-such-format")
    with pytest.raises(reports.ReportError, match="square rows"):
        reports.parse_certificate(EVAND + b"0 0 0\n", 2, "evand-cert")
    with pytest.raises(reports.ReportError, match="duplicate JSON key"):
        reports.parse_certificate(b'{"n": 2, "n": 2}', 2, "squish-json")


def test_a_new_adapter_needs_only_its_entry_and_receives_its_declared_options(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen: list[Mapping[str, str]] = []

    def dilated(raw: bytes, n: int, options: Mapping[str, str]) -> legacy.Certificate:
        seen.append(options)
        certificate = reports.evand_cert(raw, n, {})
        return reports.legacy.Certificate(
            n, certificate.side * Fraction(options["dilation"]), certificate.poses
        )

    monkeypatch.setitem(reports.ADAPTERS, "dilated-cert", dilated)
    certificate = reports.parse_certificate(EVAND, 2, "dilated-cert", {"dilation": "2"})
    assert seen == [{"dilation": "2"}]
    assert certificate.side == 6


# --------------------------------------------------------------------------- decimal poses

#: Ellsworth's text: a side, then centres and degrees in the box centred at the origin.
POSE = b"s: 2.5\n\nSquare 1: x=-0.5, y=-0.5, deg=0.0000\nSquare 2: x=0.75, y=0.5, deg=-90\n"
DILATED = {"dilation": "2", "half_angle_places": "30"}


def test_a_decimal_pose_is_dilated_about_its_centre_into_the_kernels_box() -> None:
    # Side 2 * 2.5; each centre doubled, then moved by half the side; t = tan(theta/2).
    expected = legacy.Certificate(
        2,
        Fraction(5),
        (
            legacy.Pose(Fraction(3, 2), Fraction(3, 2), Fraction(0)),
            legacy.Pose(Fraction(4), Fraction(7, 2), Fraction(-1)),
        ),
    )
    assert reports.parse_certificate(POSE, 2, "decimal-dilation", DILATED) == expected
    undilated = {**DILATED, "dilation": "1"}
    centred = reports.parse_certificate(POSE, 2, "decimal-dilation", undilated)
    assert centred.side == Fraction(5, 2)
    assert (centred.poses[1].x, centred.poses[1].y) == (Fraction(2), Fraction(7, 4))


def _below(square: Callable[[Fraction], Fraction], t: Fraction, places: int) -> bool:
    """Whether ``t <= tangent < t + 10^-places``, for a tangent ``square`` is increasing in."""
    unit = Fraction(1, 10**places)
    return square(t) <= 0 < square(t + unit)


@pytest.mark.parametrize("places", [30, 32, 100])
@pytest.mark.parametrize(
    ("degrees", "square"),
    [
        # tan(22.5) = sqrt(2) - 1, a root of (t + 1)^2 - 2.
        (Fraction(45), lambda t: (t + 1) ** 2 - 2),
        (Fraction(405), lambda t: (t + 1) ** 2 - 2),
        (Fraction(-315), lambda t: (t + 1) ** 2 - 2),
        # tan(-22.5) = 1 - sqrt(2), a root of 2 - (1 - t)^2 below 1.
        (Fraction(-45), lambda t: 2 - (1 - t) ** 2),
        # tan(30) = 1/sqrt(3) and tan(60) = sqrt(3).
        (Fraction(60), lambda t: 3 * t * t - 1),
        (Fraction(120), lambda t: t * t - 3),
    ],
)
def test_a_half_angle_tangent_is_its_exact_value_rounded_down(
    degrees: Fraction, square: Callable[[Fraction], Fraction], places: int
) -> None:
    t = reports.half_angle_tangent(degrees, places)
    assert (t * 10**places).denominator == 1
    assert _below(square, t, places)


def test_a_half_angle_tangent_near_zero_keeps_its_places() -> None:
    # 2.68e-14 degrees, the size of the source's near-axis angles: t is about 2.34e-16.
    t = reports.half_angle_tangent(Fraction("0.0000000000000268"), 32)
    assert (t * 10**32).denominator == 1
    assert Fraction(233874119767, 10**27) < t < Fraction(233874119768, 10**27)


@pytest.mark.parametrize(
    ("degrees", "tangent"),
    [(0, 0), (-0, 0), (90, 1), (-90, -1), (270, -1), (360, 0), (450, 1), (-270, 1)],
)
def test_the_rational_half_angle_tangents_are_exact(degrees: int, tangent: int) -> None:
    assert reports.half_angle_tangent(Fraction(degrees), 30) == tangent


@pytest.mark.parametrize("degrees", [180, -180, 540])
def test_a_half_turn_has_no_half_angle_tangent(degrees: int) -> None:
    with pytest.raises(reports.ReportError, match="no finite half-angle tangent"):
        reports.half_angle_tangent(Fraction(degrees), 30)


@pytest.mark.parametrize(
    ("options", "message"),
    [
        ({}, "reads exactly"),
        ({"dilation": "2"}, "reads exactly"),
        ({**DILATED, "side": "5"}, "reads exactly"),
        ({**DILATED, "dilation": "0"}, "positive integer or p/q"),
        ({**DILATED, "dilation": "1.5"}, "positive integer or p/q"),
        ({**DILATED, "dilation": "-2"}, "positive integer or p/q"),
        ({**DILATED, "dilation": "3/0"}, "positive integer or p/q"),
        ({**DILATED, "dilation": "1" * 1025}, "positive integer or p/q"),
        ({**DILATED, "dilation": "1/2"}, "below 1"),
        ({**DILATED, "half_angle_places": "29"}, "integer from 30 to 100"),
        ({**DILATED, "half_angle_places": "101"}, "integer from 30 to 100"),
        ({**DILATED, "half_angle_places": "032"}, "integer from 30 to 100"),
        ({**DILATED, "half_angle_places": "3e1"}, "integer from 30 to 100"),
    ],
)
def test_the_decimal_adapter_reads_exactly_its_two_declared_options(
    options: Mapping[str, str], message: str
) -> None:
    with pytest.raises(reports.ReportError, match=message):
        reports.parse_certificate(POSE, 2, "decimal-dilation", options)


@pytest.mark.parametrize(
    ("raw", "n", "message"),
    [
        (POSE.replace(b"Square 1", b"Square 3"), 2, r"1\.\.n in order"),
        (POSE, 3, "2 squares for n = 3"),
        (POSE + b"Square 3: x=0, y=0\n", 3, "neither the side nor a square"),
        (POSE.replace(b"s: 2.5", b""), 2, "states no side"),
        (POSE + b"s: 3\n", 2, "second side line"),
        (POSE.replace(b"2.5", b"\xff"), 2, "not UTF-8"),
        (POSE.replace(b"deg=-90", b"deg=180"), 2, "no finite half-angle tangent"),
    ],
)
def test_the_decimal_adapter_refuses_what_the_format_does_not_state(
    raw: bytes, n: int, message: str
) -> None:
    with pytest.raises(reports.ReportError, match=message):
        reports.parse_certificate(raw, n, "decimal-dilation", DILATED)


# --------------------------------------------------------------------------- admission


@pytest.mark.parametrize(
    ("side", "offered"),
    [
        (Fraction(31, 10), "3.1"),
        (Fraction(31, 10), "3.10"),
        (Fraction(3101, 1000), "3.11"),
        (Fraction(10, 3), "3.334"),
    ],
)
def test_admission_takes_a_side_equal_to_its_print_or_rounding_up_to_it(
    side: Fraction, offered: str
) -> None:
    reports.admit(legacy.Certificate(1, side, ()), offered)


@pytest.mark.parametrize(
    ("side", "offered"),
    [
        (Fraction(3101, 1000), "3.10"),
        (Fraction(3101, 1000), "3.12"),
        (Fraction(10, 3), "3.333"),
    ],
)
def test_admission_refuses_a_print_below_the_side_or_above_its_rounding_up(
    side: Fraction, offered: str
) -> None:
    with pytest.raises(reports.ReportError, match="does not round up"):
        reports.admit(legacy.Certificate(1, side, ()), offered)


def test_admission_refuses_a_print_that_is_no_plain_decimal() -> None:
    with pytest.raises(reports.ReportError, match="not a decimal"):
        reports.admit(legacy.Certificate(1, Fraction(3), ()), "3")


# --------------------------------------------------------------------------- comparison


def test_a_printed_side_stands_for_the_numbers_its_rounding_allows() -> None:
    up = reports.printed_span("1.25", "up")
    assert (up.low, up.high, up.open_low, up.open_high) == (
        Fraction(124, 100),
        Fraction(125, 100),
        True,
        False,
    )
    either = reports.printed_span("1.25", "unstated")
    assert (either.low, either.high) == (Fraction(124, 100), Fraction(126, 100))
    assert reports.relation(Fraction(124, 100), up) == "below"
    assert reports.relation(Fraction(124, 100), either) == "undecided"
    assert reports.relation(Fraction(127, 100), either) == "above"
    assert reports.relation(Fraction(5, 4), reports.exact_span(Fraction(5, 4))) == "equal"


def test_smallest_names_one_report_only_when_it_is_decidably_below_every_other() -> None:
    exact = reports.exact_span
    assert reports.smallest([("a", exact(Fraction(1))), ("b", exact(Fraction(2)))]) == {
        "smallest": "a"
    }
    near = reports.printed_span("1.0", "unstated")
    assert reports.smallest(
        [("a", exact(Fraction(1))), ("b", near), ("c", exact(Fraction(3)))]
    ) == {"smallest": None, "undecided_among": ["a", "b"]}
    assert reports.smallest(
        [("a", exact(Fraction(1))), ("b", exact(Fraction(1))), ("c", exact(Fraction(3)))]
    ) == {"smallest": None, "tied": ["a", "b"]}


@functools.cache
def _rows(name: str) -> dict[int, dict[str, Any]]:
    """A retained packet's frozen comparison, rebuilt once: the tests only read it."""
    return {row["n"]: row for row in reports.check_claims(_packet(name))["results"]}


def test_the_couzo_claims_rebuild_and_name_the_smallest_report_at_each_count() -> None:
    every = _rows(COUZO)
    assert len(every) == 65
    rows = {n: row for n, row in every.items() if row["requested"]}
    assert {n: row["smallest"] for n, row in rows.items()} == {
        132: reports.THIS,
        237: "#481",
        263: "#481",
        267: reports.THIS,
        270: "#481",
        303: "#481",
    }
    for row in rows.values():
        side = Fraction(row["exact_side"])
        assert row["case"]["relation"] == "below"
        assert Fraction(row["case"]["exact_side"]) - side == Fraction(row["case"]["difference"])
    assert [row["case"]["result"] for row in rows.values()] == [
        "T-098",
        "T-127",
        "T-116",
        "T-125",
        "T-119",
        "T-113",
    ]
    pending = {
        (n, other["report"]): other for n, row in rows.items() for other in row["pending"]
    }
    assert pending[132, "T-131 (#465)"]["exact_side"] == (
        "2397419866449012645435948575487/200000000000000000000000000000"
    )
    assert pending[270, "T-130 (#460)"]["relation"] == "below"
    assert {key for key, other in pending.items() if other["relation"] == "above"} == {
        (237, "#481"),
        (263, "#481"),
        (270, "#481"),
        (303, "#481"),
    }
    assert 2.0e-6 < float(Fraction(pending[132, "#470"]["difference"])) < 2.1e-6


def test_the_couzo_claims_compare_the_certificates_the_issue_does_not_name() -> None:
    rows = _rows(COUZO)
    unnamed = [n for n, row in rows.items() if not row["requested"]]
    assert len(unnamed) == 59
    assert all(rows[n]["printed_in"].endswith("/certificates/README.md") for n in unnamed)
    # Byte-identical to issue #451's certificate, and so tied with T-128.
    assert rows[155]["tied"] == [reports.THIS, "T-128 (#451)"]
    # The exact optimum Evan Daniel solved for Couzo's packing, tied with the case.
    assert rows[106]["case"]["relation"] == "equal"
    above = {n for n, row in rows.items() if row["case"] and row["case"]["relation"] == "above"}
    assert above == {68, 102, 103, 272, 292}
    assert [rows[n]["pending"][0]["relation"] for n in (375, 378)] == ["below", "below"]
    assert rows[327]["smallest"] == "couzo-extended-range-reports-2026-10-08"
    assert not (_packet(COUZO) / reports.BEYOND).exists()


def test_the_fang_claims_compare_the_beyond_horizon_counts_with_the_grid() -> None:
    rows = _rows(FANG)
    assert rows[308]["case"]["holders"] == "the grid"
    assert rows[308]["case"]["exact_side"] == "18"
    for n in (343, 344):
        assert rows[n]["case"] is None
        assert rows[n]["grid_side"] == "19"
        assert rows[n]["smallest"] == reports.THIS
        assert [other["relation"] for other in rows[n]["pending"]] == ["below"]
    beyond = _json(_packet(FANG) / reports.BEYOND)
    assert [row["n"] for row in beyond["results"]] == [343, 344]
    assert not (_packet(COUZO) / reports.BEYOND).exists()


def test_the_beyond_horizon_record_is_what_the_coverage_check_reparses() -> None:
    claims = coverage_check.load_claims(_packet(FANG) / reports.BEYOND)
    assert claims == {343: "18.994903529220497", 344: "18.995489275430816"}


@pytest.mark.parametrize(
    "mutation", ["house-side", "pending-relation", "dropped-row", "beyond-removed"]
)
def test_the_claims_refuse_a_tampered_frozen_comparison(
    private: Callable[[str], Path], mutation: str
) -> None:
    packet = private(FANG)
    path = packet / reports.CLAIMS
    claims = _json(path)
    if mutation == "house-side":
        claims["results"][0]["case"]["exact_side"] = "17"
    elif mutation == "pending-relation":
        claims["results"][1]["pending"][0]["relation"] = "above"
    elif mutation == "dropped-row":
        claims["results"].pop()
    else:
        (packet / reports.BEYOND).unlink()
    _write_json(path, claims)
    with pytest.raises(reports.ReportError, match="differs from its rebuild"):
        reports.check_claims(packet)


def test_writing_the_claims_refuses_a_declaration_the_case_records_no_longer_bear_out(
    private: Callable[[str], Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    packet = private(FANG)
    before = (packet / reports.CLAIMS).read_bytes()
    original = coverage_check.parse_case

    def moved(path: Path) -> dict[str, Any]:
        case = original(path)
        case["reported_upper_bound"]["source_key"] = "[Fang two-wedge certificates 2026-10-10]"
        return case

    monkeypatch.setattr(reports.coverage_check, "parse_case", moved)
    with pytest.raises(reports.ReportError, match="does not read the records"):
        reports.write_claims(packet)
    assert (packet / reports.CLAIMS).read_bytes() == before


def test_a_case_value_that_is_not_its_house_rounded_up_is_refused(
    private: Callable[[str], Path],
) -> None:
    packet = private(COUZO)
    path = packet / reports.DECLARATION
    value = _json(path)
    value["houses"][0]["verified_value"] = "11.9913278876915014"
    _write_json(path, value)
    with pytest.raises(reports.ReportError, match="exact or rounded up"):
        reports.compare(packet)


# --------------------------------------------------------------------------- receipts


@pytest.mark.parametrize("name", EVERY)
def test_the_receipt_admits_every_job_on_both_routes(name: str) -> None:
    packet = _packet(name)
    positives = reports.check_certification(packet)
    _declaration, facts = reports.replayed_facts(packet)
    parts = reports.receipt_parts(packet, facts)
    record = {"cases": [row for part, _ in parts for row in part["cases"]]}
    assert [(row["n"], row["control"]) for row in record["cases"]] == [
        (n, control) for n in positives for control in reports.JOBS
    ]
    assert list(positives) == reports.load_declaration(packet)["replayed"]
    summary = reports.receipt_summary(record)
    assert summary["pair_decisions"] == sum(3 * n * (n - 1) for n in positives)
    for margins in reports.margins(positives).values():
        for field in ("containment_clearance", "best_pair_gap"):
            assert margins[f"exact_verify_{field}"] == margins[f"independent_{field}"]
        assert Fraction(margins["exact_verify_best_pair_gap"]) > 0
        assert Fraction(margins["exact_verify_containment_clearance"]) >= 0
    # SQUISH's squares touch the box; every other source's clear it.
    walls = {
        Fraction(m["exact_verify_containment_clearance"])
        for m in reports.margins(positives).values()
    }
    assert (walls == {0}) is (name == SQUISH_481)


def _jobs_from_receipt(packet: Path, directory: Path) -> None:
    """Write a retained receipt's rows back out as a finished job directory."""
    _declaration, facts = reports.replayed_facts(packet)
    directory.mkdir()
    for part, _ in reports.receipt_parts(packet, facts):
        for row in part["cases"]:
            _write_json(directory / f"n{row['n']}-{row['control']}.json", row)


def test_a_receipt_over_the_ceiling_is_kept_by_count_and_admitted_alike(
    private: Callable[[str], Path], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet = private(FANG)
    _jobs_from_receipt(packet, tmp_path / "jobs")
    whole = kernel.read_xz(packet / reports.RECEIPT)
    sizes = [
        reports.evidence_bytes({**whole, "cases": [r for r in whole["cases"] if r["n"] == n]})
        for n in (308, 343, 344)
    ]
    ceiling = kernel.MAX_BYTES
    monkeypatch.setattr(kernel, "MAX_BYTES", max(sizes))
    assert reports.evidence_bytes(whole) > kernel.MAX_BYTES
    reports.certify(packet, tmp_path / "jobs", finished=True)
    assert not (packet / reports.RECEIPT).exists()
    assert [path.name for path in sorted((packet / "receipts").iterdir())] == [
        f"exact-certification-n{n}.json.xz" for n in (308, 343, 344)
    ]
    assert list(reports.check_certification(packet)) == [308, 343, 344]
    monkeypatch.setattr(kernel, "MAX_BYTES", ceiling)
    kernel.save_xz(packet / reports.RECEIPT, whole)
    with pytest.raises(reports.ReportError, match="not both"):
        reports.check_certification(packet)


def test_assembling_a_receipt_refuses_a_missing_or_altered_job(
    private: Callable[[str], Path], tmp_path: Path
) -> None:
    packet = private(DELEEUW)
    jobs = tmp_path / "jobs"
    _jobs_from_receipt(packet, jobs)
    before = (packet / reports.RECEIPT).read_bytes()
    row = _json(jobs / "n70-positive.json")
    row["checker_input"]["side"] = "9"
    _write_json(jobs / "n70-positive.json", row)
    with pytest.raises(kernel.ReportError):
        reports.certify(packet, jobs, finished=True)
    (jobs / "n70-positive.json").unlink()
    with pytest.raises(FileNotFoundError):
        reports.certify(packet, jobs, finished=True)
    assert (packet / reports.RECEIPT).read_bytes() == before


@pytest.mark.parametrize("kind", ["flipped-control", "moved-input", "reordered", "format"])
def test_receipt_mutations_refuse(private: Callable[[str], Path], kind: str) -> None:
    packet = private(COUZO)
    record = kernel.read_xz(packet / reports.RECEIPT)
    cases = record["cases"]
    if kind == "flipped-control":
        cases[1]["independent"]["verification_passed"] = True
    elif kind == "moved-input":
        cases[0]["checker_input"]["poses"][0][0] = "1/3"
    elif kind == "reordered":
        cases[0], cases[3] = cases[3], cases[0]
    else:
        record["format"] = "evand-465-record-hunt-exact-replay-v1"
    kernel.save_xz(packet / reports.RECEIPT, record)
    with pytest.raises(kernel.ReportError):
        reports.check_certification(packet)


@pytest.mark.parametrize("selection", [[], [132, 132], [True], [132, 133]])
def test_replay_selection_refuses_unknown_and_repeated_counts(selection: list[int]) -> None:
    with pytest.raises(reports.ReportError, match="replay selection"):
        reports.check_certification(_packet(COUZO), selection)


def test_certify_refuses_an_invalid_allocation_or_a_reused_directory(tmp_path: Path) -> None:
    with pytest.raises(reports.ReportError, match="worker/deadline"):
        reports.certify(_packet(COUZO), tmp_path / "jobs", workers=3)
    with pytest.raises(reports.ReportError, match="fresh attempt"):
        reports.certify(_packet(COUZO), tmp_path)


def _fake_runner(
    monkeypatch: pytest.MonkeyPatch, outcome: Callable[[list[str]], bytes | None]
) -> list[list[str]]:
    """Replace the child process; ``outcome`` writes the output, or None times out."""
    commands: list[list[str]] = []

    def run(command: list[str], **options: Any) -> subprocess.CompletedProcess[bytes]:
        commands.append(command)
        payload = outcome(command)
        if payload is None:
            raise subprocess.TimeoutExpired(
                command, options["timeout"], output=b"partial out", stderr=b"partial err"
            )
        Path(command[-1]).write_bytes(payload)
        return subprocess.CompletedProcess(command, 0, b"native stdout", b"native stderr")

    monkeypatch.setattr(reports.subprocess, "run", run)
    return commands


def test_the_driver_names_the_packet_and_keeps_a_timeout_failure_record(
    private: Callable[[str], Path], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet = private(COUZO)
    commands = _fake_runner(monkeypatch, lambda _command: None)
    before = (packet / reports.RECEIPT).read_bytes()
    with pytest.raises(reports.ReportError, match="exceeded 45s"):
        reports.certify(packet, tmp_path / "jobs", workers=1, timeout=45)
    command = commands[0]
    assert command[2:5] == [reports.MODULE, COUZO, "decide-job"]
    assert command[command.index("--n") + 1] == "68"
    assert command[command.index("--control") + 1] == "positive"
    stem = tmp_path / "jobs" / "n68-positive"
    assert stem.with_suffix(".stdout.log").read_bytes() == b"partial out"
    assert stem.with_suffix(".stderr.log").read_bytes() == b"partial err"
    assert _json(stem.with_suffix(".failure.json")) == {
        "n": 68,
        "control": "positive",
        "status": "timeout",
        "timeout_seconds": 45,
    }
    assert (packet / reports.RECEIPT).read_bytes() == before


@pytest.mark.parametrize("payload", [b'{"n":132,"n":237}', b"[]", b'{"n": 132}'])
def test_the_driver_refuses_duplicate_keys_and_incomplete_rows(
    private: Callable[[str], Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    payload: bytes,
) -> None:
    packet = private(COUZO)
    _fake_runner(monkeypatch, lambda _command: payload)
    before = (packet / reports.RECEIPT).read_bytes()
    with pytest.raises(kernel.ReportError):
        reports.certify(packet, tmp_path / "jobs", workers=1, timeout=45)
    assert (tmp_path / "jobs" / "n68-positive.stdout.log").read_bytes() == b"native stdout"
    assert (packet / reports.RECEIPT).read_bytes() == before


# --------------------------------------------------------------------------- register plan


@pytest.mark.parametrize("name", EVERY)
def test_the_register_plan_states_each_bound_as_check_standing_reads_it(name: str) -> None:
    plan = reports.register_plan(_packet(name))
    result = plan["results.yaml"]
    assert result["id"] == "T-NNN"
    assert (result["verification"], result["confirmation"]) == ("V0", "C0")
    claims = reports.check_claims(_packet(name))["results"]
    rows = {row["n"]: row for row in claims if row["requested"]}
    scope = result["scope"]["n_values"]
    assert scope == [n for n in rows if n <= reports.HORIZON]
    stated = check_standing.statements(" ".join(result["claim"].split()), scope)
    assert {n: bound.value for (n, _), bound in stated.items()} == {
        n: Fraction(rows[n]["exact_side"]) for n in scope
    }
    assert not check_standing.statements(result["headline"], scope)
    published = {
        COUZO: "2026-10-09",
        FANG: "2026-10-10",
        SQUISH_481: "2026-10-09",
        MISHAPOLK: "2026-10-09",
    }
    assert result["attribution"]["published"] == published.get(name, "2026-10-10")
    evidence = plan["evidence.yaml"]
    assert evidence["scope"]["n_values"] == list(rows)
    assert evidence["assurance"] == "reported"


def test_the_fang_plan_records_the_beyond_horizon_counts_as_dated_rows() -> None:
    coverage = reports.register_plan(_packet(FANG))["source-coverage.yaml"]
    (source,) = coverage["sources"]
    assert (
        source["claims_record"]
        == f"resources/web/{FANG}/acquisition/beyond-horizon-claims.json"
    )
    assert [
        (row["n"], row["value"], row["disposition"])
        for row in coverage["beyond_horizon_claims"]
    ] == [
        (343, "18.994903529220497", "tracked-outside-case-corpus"),
        (344, "18.995489275430816", "tracked-outside-case-corpus"),
    ]
    claims = coverage_check.load_claims(reports.ROOT / source["claims_record"])
    assert {row["n"]: row["value"] for row in coverage["beyond_horizon_claims"]} == claims


def test_a_claim_states_a_short_terminating_side_in_decimals_and_others_as_fractions() -> None:
    assert reports.claim_value(Fraction(3975917726395155753617729398543, 25 * 10**28)) == (
        "15.903670905580623014470917594172"
    )
    assert reports.claim_value(Fraction(10, 3)) == "10/3"
    assert reports.claim_value(Fraction(1, 2**200)).count("/") == 1


# --------------------------------------------------------------------------- derived facts

SYNTHETIC = "synthetic-derived-2026-10-10"
DATE = "2026-10-10T00:00:00Z"


def _git(directory: Path, *arguments: str) -> str:
    environment = {**os.environ, "GIT_AUTHOR_DATE": DATE, "GIT_COMMITTER_DATE": DATE}
    identity = ["-c", "user.name=Test", "-c", "user.email=test@example.invalid"]
    completed = subprocess.run(
        ["git", *identity, "-C", str(directory), *arguments],
        capture_output=True,
        text=True,
        check=True,
        env=environment,
    )
    return completed.stdout.strip()


def _upstream(tmp_path: Path, certificate: Mapping[str, Any]) -> tuple[Path, str]:
    """A one-commit upstream repository holding one centred certificate, unlicensed."""
    upstream = tmp_path / "upstream"
    upstream.mkdir()
    _git(upstream, "init", "--quiet")
    (upstream / "certificate.json").write_text(json.dumps(certificate, indent=2) + "\n")
    _git(upstream, "add", "certificate.json")
    _git(upstream, "commit", "--quiet", "-m", "certificate")
    return upstream, _git(upstream, "rev-parse", "HEAD")


def _readme(packet: Path, rows: list[Any]) -> None:
    table = "\n".join(row.markdown() for row in rows)
    (packet / "README.md").write_text(
        "# Synthetic\n\n## Compressed Files\n\n"
        "| Stored File | Origin | Git Blob of Original | SHA-256 of Original |\n"
        f"| --- | --- | --- | --- |\n{table}\n"
    )


@pytest.fixture
def derived(private: Callable[[str], Path], tmp_path: Path) -> tuple[Path, Path]:
    """A derived-only packet written from a synthetic checkout, and the checkout."""
    upstream, commit = _upstream(tmp_path, CENTRED)
    packet = reports.WEB / SYNTHETIC
    (packet / "acquisition").mkdir(parents=True)
    _write_json(
        packet / "acquisition/declaration.json",
        {
            "format": "external-source-declaration-v1",
            "id": "synthetic",
            "source_url": "https://example.invalid/synthetic",
            "source_ref": "main",
            "source_commit": commit,
            "retrieved_at_utc": "2026-10-10T00:00Z",
            "git_scope": "The one file of a synthetic one-commit repository.",
            "archived_dir": "source",
            "license": "None stated: derived-only custody.",
            "claims": ["s(2) <= 3, a synthetic centred certificate."],
            "scope": ["certificate.json"],
            "pinned_only": [{"match": "certificate.json", "reason": "Derived-only custody."}],
        },
    )
    reports.acquire_source.acquire(packet, upstream, reports.REPO)
    declaration = _json(private(DELEEUW) / reports.DECLARATION)
    declaration.update(
        {
            "issue": "https://example.invalid/issue",
            "certificates": [
                {
                    "n": 2,
                    "path": "certificate.json",
                    "format": "centred-json",
                    "offered": "3.0",
                    "first_committed": DATE,
                    "fact": "facts/n-002.yaml",
                }
            ],
            "requested": [2],
            "replayed": [2],
            "houses": [
                {
                    "n": 2,
                    "reader": "grid",
                    "source_key": "[Kingbird]",
                    "holders": "the grid",
                    "reported_value": "2",
                    "verified_value": "2",
                    "evidence": ["E-basic-grid-upper"],
                }
            ],
            "pending": [],
        }
    )
    _write_json(packet / reports.DECLARATION, declaration)
    _readme(packet, [])
    _readme(packet, reports.derive(packet, upstream))
    return packet, upstream


def test_a_derived_fact_reads_offline_as_the_certificate_it_was_derived_from(
    derived: tuple[Path, Path],
) -> None:
    packet, upstream = derived
    assert not (packet / "source").exists() or not any((packet / "source").iterdir())
    raw = (upstream / "certificate.json").read_bytes()
    expected = reports.parse_certificate(raw, 2, "centred-json")
    assert reports.read_facts(packet) == {2: expected}
    assert [row.stored for row in reports.derive(packet, upstream, check=True)] == [
        "facts/n-002.yaml.gz"
    ]
    fact = gzip.decompress((packet / "facts/n-002.yaml.gz").read_bytes()).decode()
    assert "revision_sha256:" in fact


def test_derivation_refuses_a_checkout_that_does_not_yield_the_packet(
    derived: tuple[Path, Path],
) -> None:
    packet, upstream = derived
    changed = {**CENTRED, "side": "4"}
    (upstream / "certificate.json").write_text(json.dumps(changed, indent=2) + "\n")
    with pytest.raises(reports.ReportError, match="does not yield this packet"):
        reports.derive(packet, upstream, check=True)
    _git(upstream, "commit", "--quiet", "-am", "a later revision")
    with pytest.raises(reports.ReportError, match="does not yield this packet"):
        reports.derive(packet, upstream, check=True)


def test_a_derived_fact_that_names_other_bytes_is_refused(derived: tuple[Path, Path]) -> None:
    packet, _upstream = derived
    stored = packet / "facts/n-002.yaml.gz"
    text = gzip.decompress(stored.read_bytes()).decode()
    marker = "revision_sha256: "
    start = text.index(marker) + len(marker)
    text = text[:start] + "a" * 64 + text[start + 64 :]
    stored.write_bytes(gzip.compress(text.encode(), mtime=0))
    _readme(packet, [reports.retained_data.describe(packet, stored, "receipt")])
    with pytest.raises(reports.ReportError, match="differs from its own rebuild"):
        reports.read_facts(packet)


def test_a_derived_fact_names_its_file_and_admits_no_second_format(
    private: Callable[[str], Path],
) -> None:
    packet = private(DELEEUW)
    path = packet / reports.DECLARATION
    value = _json(path)
    value["certificates"][0]["fact"] = "facts/n-70.yaml"
    _write_json(path, value)
    with pytest.raises(reports.ReportError, match=r"facts/n-NNN\.yaml"):
        reports.load_declaration(packet)


@pytest.mark.parametrize("name", DERIVED)
def test_the_derived_packets_admit_every_certificate_at_its_printed_exact_side(
    name: str,
) -> None:
    packet = _packet(name)
    declaration = reports.load_declaration(packet)
    certificates = reports.read_facts(packet)
    assert list(certificates) == [row["n"] for row in declaration["certificates"]]
    for row in declaration["certificates"]:
        assert certificates[row["n"]].side == Fraction(row["offered"])
    rows = _rows(name)
    assert all(row["smallest"] == reports.THIS for row in rows.values())
    assert all(row["case"]["relation"] == "below" for row in rows.values())


def test_the_n232_case_reports_a_catalogue_print_under_its_verified_ceiling() -> None:
    row = _rows(SQUISH_481)[232]
    assert row["case"]["reported_relation"] == "below"
    # The verified lane prints Evan Daniel's certificate side rounded up at 14 places; the
    # comparison is with the certificate's exact side, rebuilt from its packet.
    exact = Fraction(row["case"]["exact_side"])
    assert exact == Fraction(3944543648263005692141767432271, 250000000000000000000000000000)
    assert exact < Fraction(row["case"]["verified_value"]) < exact + Fraction(1, 10**14)
    assert Fraction(row["case"]["reported_value"]) < exact
    assert row["case"]["result"] == "T-101"


def test_the_481_claims_compare_issue_476_from_its_own_packet() -> None:
    rows = _rows(SQUISH_481)
    for n in (237, 263, 270, 303):
        (couzo,) = [other for other in rows[n]["pending"] if other["report"] == "#476"]
        assert couzo["relation"] == "below"
        assert Fraction(couzo["exact_side"]) == reports.read_facts(_packet(COUZO))[n].side


# --------------------------------------------------------------------------- decimal packet

MARGINS = "receipts/decimal-pose-margins.json"
#: Where the issue's ceiling is below the case's verified ceiling.
BELOW_CASE = (84, 86, 103, 105, 108, 127, 131, 132, 175, 180, 258, 267, 270, 302, 303, 306)


def test_each_decimal_fact_is_the_issue_ceiling_by_the_dilation_the_margins_measured() -> None:
    packet = _packet(MISHAPOLK)
    measured = {row["n"]: row for row in _json(packet / MARGINS)["files"]}
    record = _json(packet / reports.acquire_source.RECORD)
    pinned = {item["path"]: item["sha256"] for item in record["sources"][0]["pinned_only"]}
    certificates = reports.read_facts(packet)
    assert list(certificates) == list(measured)
    for row in reports.load_declaration(packet)["certificates"]:
        n, certificate = row["n"], certificates[row["n"]]
        options = {option["name"]: option["value"] for option in row.get("options", [])}
        assert (row["format"], options["half_angle_places"]) == ("decimal-dilation", "32")
        # The measured file, at the digest the packet pins, with the dilation it measured.
        assert measured[n]["path"] == row["path"]
        assert measured[n]["sha256"] == pinned[row["path"]]
        assert Fraction(options["dilation"]) == Fraction(measured[n]["dilation"])
        printed = Fraction(measured[n]["printed_side"])
        assert certificate.side == Fraction(options["dilation"]) * printed
        # The side is the issue's ceiling exactly, which the interval route proved packs.
        assert certificate.side == Fraction(row["offered"])
        assert measured[n]["target_side"] == row["offered"]
        assert measured[n]["at_target_side"]["verdict"] == "packing"
        assert all((pose.t * 10**32).denominator == 1 for pose in certificate.poses)


def test_the_decimal_claims_find_the_ceiling_smallest_only_at_103_and_258() -> None:
    rows = _rows(MISHAPOLK)
    assert [n for n, row in rows.items() if row["smallest"] == reports.THIS] == [103, 258]
    assert [n for n, row in rows.items() if not row["requested"]] == [132, 267]
    below = tuple(n for n, row in rows.items() if row["case"]["relation"] == "below")
    assert below == BELOW_CASE
    assert all(row["case"]["relation"] == "above" for n, row in rows.items() if n not in below)
    earlier = {
        n
        for n, row in rows.items()
        for other in row["pending"]
        if other["report"].startswith(("T-128", "T-130")) and other["relation"] == "above"
    }
    assert earlier == {84, 86, 105, 108, 127, 131, 175, 180, 270, 306}
    assert {n: rows[n]["smallest"] for n in (132, 267, 302, 303)} == {
        132: "#476",
        267: "#476",
        302: "#481",
        303: "#481",
    }
