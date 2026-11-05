"""The #890 and #910 dilations' retained premise audits, #890's replay comparison and
#910's native receipt archive audit, held to their packets.

`devtools.audit_dilated_measure` recomputes each receipt from the retained bytes; these
tests ask that the committed receipts are what it recomputes, that they say what the
register relies on, and that its checks refuse the mutations they exist to catch.
"""

from __future__ import annotations

import copy
import dataclasses
import functools
import gzip
import json
import shutil
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_dilated_measure as audit
from devtools.check_sqverify_fast import mixed_mutant

PACKET = "ozden-s94-lower-bound-2026-11-03"
DILATION = audit.DILATIONS[PACKET]
PACKET_910 = "ozden-s94-lower-bound-9972-2026-11-05"
DILATION_910 = audit.DILATIONS[PACKET_910]


def stored(packet: str, command: str) -> dict[str, Any]:
    value: dict[str, Any] = json.loads(
        audit.receipt_path(packet, command).read_text(encoding="utf-8")
    )
    return value


@functools.cache
def candidate_910() -> dict[str, Any]:
    raw = (audit.WEB / PACKET_910 / DILATION_910.candidate).read_bytes()
    data: dict[str, Any] = json.loads(gzip.decompress(raw), parse_float=str)
    return data


def candidate() -> dict[str, Any]:
    raw = (audit.WEB / PACKET / DILATION.candidate).read_bytes()
    data: dict[str, Any] = json.loads(gzip.decompress(raw), parse_float=str)
    return data


def base() -> dict[str, Any]:
    raw = (audit.WEB / DILATION.base).read_bytes()
    data: dict[str, Any] = json.loads(gzip.decompress(raw), parse_float=str)
    return data


def test_the_audit_receipt_is_what_the_tool_recomputes() -> None:
    assert audit.main(["audit", PACKET, "--check"]) == 0


def test_the_audit_holds_every_premise_the_register_states() -> None:
    receipt = json.loads(audit.receipt_path(PACKET, "audit").read_text(encoding="utf-8"))
    assert receipt["status"] == "PREMISES_HOLD"
    net = receipt["lemma_n0"]
    assert net["angle_count"] == 600
    assert net["b_shrink"] == "2387749705363/2388000000000"
    assert net["net_last_tangent"] == "49717/120000"
    assert receipt["file"]["total_mass"] == "9399999/100000"
    assert receipt["dilation"]["lambda"] == "1993/1990"
    observed = receipt["observations"]
    assert observed["axis_domain_growth_in_base_coordinates"] == "3/3986"
    assert observed["route_ceiling"] == "99500/9977"
    assert observed["base_step"] == "83/40000"
    assert observed["base_net_admits_dilated_core"] is False
    assert receipt["dilation"]["regenerated_text_is_the_certificate"] is True
    digests = receipt["digests"]
    # The source's stated digests, which stage 2 checked once and the receipt records.
    assert digests["text_sha256"] == digests["text_sha256_stated"]
    assert digests["base_text_sha256"] == digests["base_text_sha256_stated"]
    assert digests["regenerated_text_sha256"] == DILATION.text_sha256
    assert digests["candidate_sha256"] == (
        "116c83425959a943196287a910ad799b2fe1bb9dec433085ea222bd62d5a16f8"
    )


def test_the_replay_comparison_is_what_the_tool_recomputes() -> None:
    assert audit.main(["compare", PACKET, "--check"]) == 0


def test_every_direction_of_the_capture_equals_both_producer_receipts() -> None:
    receipt = json.loads(audit.receipt_path(PACKET, "compare").read_text(encoding="utf-8"))
    assert receipt["verdict"] == "EVERY_DIRECTION_AGREES"
    assert receipt["status"] == "VERIFIED"
    assert receipt["directions"] == 600
    for item in receipt["receipts"]:
        assert item["identical_directions"] == 600
        assert item["differing"] == {}
        assert all(item["summary_equal"].values())


def test_a_row_not_dilated_is_refused() -> None:
    data = candidate()
    row = data["rectangles"][17]["rectangle"]
    row[0] = str(Fraction(row[0]) + Fraction(1, 10**12))
    checks = audit.dilation_checks(data, base())
    assert checks["every_rectangle_lambda_times_base"] is False


def test_a_changed_mass_is_refused() -> None:
    data = candidate()
    data["rectangles"][3]["mass"] = str(Fraction(data["rectangles"][3]["mass"]) * 2)
    checks = audit.dilation_checks(data, base())
    assert checks["every_mass_equal"] is False
    assert audit.file_checks(data, DILATION)["total_mass_equals_stated"] is False


def test_the_base_net_does_not_admit_the_dilated_core() -> None:
    data = copy.deepcopy(candidate())
    data["proof_net"] = {"step": "83/40000", "last": 200}
    net = audit.lemma_n0(data)
    assert net["b_shrink_below_one"] is False
    observed = audit.dilation_observations(candidate(), base())
    assert observed["base_net_admits_dilated_core"] is False


def test_an_observation_is_required_of_nothing() -> None:
    """The status reads the premises, the dilation and the regeneration, never what the
    dilation does not carry: a base on a declared net fine enough for the dilated core
    changes the observation and not the checks, and the observation is read on the
    base's own step."""
    fine = base()
    fine["proof_net"] = {"step": "1/1000000", "last": 414214}
    observed = audit.dilation_observations(candidate(), fine)
    assert observed["base_step"] == "1/1000000"
    assert observed["base_net_admits_dilated_core"] is True
    checks = audit.dilation_checks(candidate(), fine)
    assert all(value is True for value in checks.values() if isinstance(value, bool))


def test_a_row_of_the_wrong_shape_is_refused() -> None:
    for change in ("coordinates", "key"):
        data = candidate()
        if change == "coordinates":
            data["rectangles"][5]["rectangle"] = data["rectangles"][5]["rectangle"][:3]
        else:
            data["rectangles"][5]["weight"] = "1"
        checks = audit.file_checks(data, DILATION)
        assert checks["every_row_a_rectangle_of_four_and_a_mass"] is False
        assert checks["every_rectangle_inside"] is False


def test_a_capture_with_a_stray_line_or_a_second_summary_is_refused(tmp_path: Path) -> None:
    capture = audit.CENSUS / PACKET / f"{DILATION.name}.jsonl.gz"
    lines = gzip.decompress(capture.read_bytes()).decode().splitlines()
    stray = tmp_path / "stray.jsonl"
    stray.write_text("\n".join([*lines[:3], '{"note": 1}', *lines[3:]]), encoding="utf-8")
    with pytest.raises(SystemExit, match="neither a direction row nor the summary"):
        audit.read_rows(stray)
    twice = tmp_path / "twice.jsonl"
    twice.write_text("\n".join([*lines, lines[-1]]), encoding="utf-8")
    with pytest.raises(SystemExit, match="a second summary"):
        audit.read_rows(twice)


def test_check_fails_on_a_receipt_that_does_not_pass(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """`--check` also requires the passing status, so an unchanged failing receipt fails."""
    stored = json.loads(audit.receipt_path(PACKET, "audit").read_text(encoding="utf-8"))
    failing = {**stored, "status": "PREMISES_FAIL"}
    kept = tmp_path / "dilation-audit.json"
    kept.write_text(json.dumps(failing), encoding="utf-8")
    monkeypatch.setattr(audit, "audit", lambda _packet: failing)
    monkeypatch.setattr(audit, "receipt_path", lambda _packet, _command: kept)
    assert audit.main(["audit", PACKET, "--check"]) == 1


@pytest.mark.parametrize("extra", ["net", "certificate"])
def test_a_second_net_declaration_is_refused(extra: str) -> None:
    data = candidate()
    data[extra] = {"D": "83/40000"}
    checks = audit.file_checks(data, DILATION)
    assert checks["keys_known"] is False


def test_the_890_shared_node_growth_is_the_stage_4_reviews() -> None:
    """F5 of the 3 November review measured the growth at the nodes the 600-direction net
    shares with Hosono's, 6.55e-5 to 1.062e-3, and the source counts 400 new directions;
    the observation, written apart from that review, finds the same."""
    growth = stored(PACKET, "audit")["observations"]["shared_node_growth_in_base_coordinates"]
    assert (growth["shared_nodes"], growth["new_nodes"]) == (200, 400)
    assert f"{growth['least_approx']:.3g}" == "6.55e-05"
    assert f"{growth['most_approx']:.4g}" == "0.001062"


def test_the_910_audit_receipt_is_what_the_tool_recomputes() -> None:
    assert audit.main(["audit", PACKET_910, "--check"]) == 0


def test_the_910_audit_holds_every_premise_the_register_states() -> None:
    receipt = stored(PACKET_910, "audit")
    assert receipt["status"] == "PREMISES_HOLD"
    net = receipt["lemma_n0"]
    assert net["angle_count"] == 4972
    assert net["D"] == "1/12000"
    assert net["B"] == "24872661/24875000"
    assert net["b_shrink"] == "99498934887/99500000000"
    assert net["net_last_tangent"] == "1657/4000"
    # The last tangent covers the endpoint tan(pi/8): t^2 + 2t - 1 > 0.
    assert net["c_endpoint"] == "1649/16000000"
    assert receipt["file"]["total_mass"] == "9399999/100000"
    assert receipt["file"]["rows"] == 853
    scaled = receipt["dilation"]
    assert scaled["lambda"] == "4986/4975"
    assert all(scaled[key] is True for key in scaled if key != "lambda")
    observed = receipt["observations"]
    assert observed["regenerated_gzip_is_the_stored_file"] is True
    assert observed["base_net_admits_dilated_core"] is False
    assert observed["axis_domain_growth_in_base_coordinates"] == "11/9972"
    growth = observed["shared_node_growth_in_base_coordinates"]
    assert (growth["shared_nodes"], growth["new_nodes"]) == (20, 4952)
    assert observed["route_ceiling"] == "99500/9977"
    assert observed["side_below_ceiling"] is True
    digests = receipt["digests"]
    # The issue's stated digests, which stage 2 checked once and the receipt records.
    assert digests["candidate_sha256"] == digests["candidate_sha256_stated"]
    assert digests["text_sha256"] == digests["text_sha256_stated"]
    assert digests["base_text_sha256"] == digests["base_text_sha256_stated"]
    assert digests["base_stored_sha256"] == digests["base_stored_sha256_stated"]
    assert digests["regenerated_text_sha256"] == DILATION_910.text_sha256


def test_the_two_rescale_rules_are_not_one() -> None:
    """#910's script writes canonical JSON with its own label: #890's rule, applied to the
    same base and net, does not give its text."""
    base_text = gzip.decompress((audit.WEB / DILATION_910.base).read_bytes())
    text = gzip.decompress((audit.WEB / PACKET_910 / DILATION_910.candidate).read_bytes())
    step, last = Fraction(1, 12000), 4971
    plain = audit.rescaled_text(base_text, DILATION_910.side, step, last)
    assert plain != text
    canonical = audit.rescaled_text(
        base_text,
        DILATION_910.side,
        step,
        last,
        canonical=True,
        derived_from=DILATION_910.derived_from,
    )
    assert canonical == text


def test_the_910_receipt_archive_audit_is_what_the_tool_recomputes() -> None:
    assert audit.main(["receipts", PACKET_910, "--check"]) == 0


def test_every_910_direction_has_one_verified_native_line_of_reviewed_source() -> None:
    receipt = stored(PACKET_910, "receipts")
    assert receipt["status"] == "RECEIPTS_HOLD"
    coverage = receipt["coverage"]
    assert coverage["directions"] == coverage["net_directions"] == 4972
    assert coverage["every_index_once"] is True
    assert coverage["selected_lines_equal_their_source"] == 4972
    assert coverage["least_certified_bound"] == 1.0000000000003892
    assert coverage["least_bound_direction"] == 3663
    assert coverage["selected_by_stream"] == {
        "A": 2486,
        "B": 801,
        "C": 800,
        "D": 800,
        "E": 84,
        "F": 1,
    }
    assert coverage["merged_sha256"] == coverage["merged_sha256_stated"]
    assert coverage["merged_text_sha256"] == coverage["merged_text_sha256_stated"]
    candidate_sha256 = receipt["candidate_sha256"]
    assert candidate_sha256 == DILATION_910.stored_sha256
    for stream in receipt["streams"]:
        assert all(stream[key] is True for key in audit.STREAM_CHECKS), stream["id"]
        # The streams are bound to the retained certificate by the digest they state.
        assert stream["input_sha256"] == candidate_sha256, stream["id"]
        assert stream["archive_sha256"] == stream["archive_sha256_stated"], stream["id"]
        assert stream["uncompressed_sha256"] == stream["uncompressed_sha256_stated"]
        assert stream["reviewed_source_commit"] == "910b6b12c"
    crate = receipt["crate"]
    assert crate["copy_is_reviewed_source_for_declared_nets"] is True
    assert crate["copy_source_sha256"] == (
        "d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88"
    )
    assert receipt["nodes"]["selected_nodes"] == 2462923881
    assert receipt["nodes"]["selected_oblique_rows_of_unknown_nodes"] == 0


def test_the_910_control_witness_at_1198_is_recomputed_exactly() -> None:
    control = stored(PACKET_910, "receipts")["control"]
    assert control["passes"] is True
    assert control["directions"] == [0, 1198]
    assert control["every_mass_times_factor"] is True
    (producer,) = (
        item for item in control["witnesses"] if item["kind"].startswith("the producer")
    )
    assert producer["r"] == 1198
    assert (producer["x"], producer["y"]) == (
        "3477717289/625000000",
        "7444849783253/1000000000000",
    )
    assert producer["capture_equals_stated"] is True
    assert f"{producer['capture_approx']:.15f}" == "0.991109005346039"
    assert producer["in_searched_quadrant"] is True
    assert producer["original_capture_at_least_one"] is True
    assert control["scope"].endswith("not the whole net")


def copied_packet(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """#910's packet copied to a scratch tree the tool is pointed at."""
    project = tmp_path / "packing"
    web = project / "resources/web"
    shutil.copytree(audit.WEB / PACKET_910, web / PACKET_910)
    monkeypatch.setattr(audit, "PROJECT", project)
    monkeypatch.setattr(audit, "WEB", web)
    return web / PACKET_910


def test_a_merged_line_not_its_source_or_below_one_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    folder = copied_packet(tmp_path, monkeypatch)
    merged = folder / "source/receipts/directions.jsonl.gz"
    lines = gzip.decompress(merged.read_bytes()).decode().splitlines()
    row = json.loads(lines[17])
    row["min_certified_lower_bound"] = 0.9999
    lines[17] = json.dumps(row, separators=(",", ":"), sort_keys=True)
    merged.write_bytes(gzip.compress(("\n".join(lines) + "\n").encode(), mtime=0))
    receipt = audit.receipts(PACKET_910)
    assert receipt["status"] == "RECEIPTS_FAIL"
    assert receipt["coverage"]["every_selected_line_is_its_source_line"] is False
    assert receipt["coverage"]["every_bound_finite_and_at_least_one"] is False


def test_a_stream_row_outside_its_scope_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    folder = copied_packet(tmp_path, monkeypatch)
    stream = folder / "source/receipts/native/F.jsonl.gz"
    lines = gzip.decompress(stream.read_bytes()).decode().splitlines()
    row = json.loads(lines[0])
    row["r"] = 7
    lines[0] = json.dumps(row, separators=(",", ":"), sort_keys=True)
    stream.write_bytes(gzip.compress(("\n".join(lines) + "\n").encode(), mtime=0))
    receipt = audit.receipts(PACKET_910)
    assert receipt["status"] == "RECEIPTS_FAIL"
    (report,) = (item for item in receipt["streams"] if item["id"] == "F")
    assert report["rows_are_the_scope"] is False


def test_a_direction_twice_in_a_stream_or_the_selection_is_refused(tmp_path: Path) -> None:
    line = '{"r":3,"verdict":"verified"}'
    with pytest.raises(SystemExit, match="direction 3 twice"):
        audit.direction_lines(f"{line}\n{line}\n".encode(), "stream")
    selection = tmp_path / "selection.csv"
    selection.write_text("r,source\n0,A\n1,B\n0,C\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="direction 0 twice"):
        audit.read_selection(selection)


def test_a_mutant_that_is_not_every_mass_times_its_factor_is_refused() -> None:
    data = candidate_910()
    mutant = mixed_mutant(data, factor=Fraction(99, 100))
    assert audit.mutant_checks(data, mutant, Fraction(99, 100))["every_mass_times_factor"]
    mutant["rectangles"][40]["mass"] = data["rectangles"][40]["mass"]
    checks = audit.mutant_checks(data, mutant, Fraction(99, 100))
    assert checks["every_mass_times_factor"] is False
    moved = mixed_mutant(data, factor=Fraction(99, 100))
    moved["rectangles"][2]["rectangle"][0] = "0"
    assert audit.mutant_checks(data, moved, Fraction(99, 100))["geometry_unchanged"] is False


def test_compare_refuses_a_dilation_with_neither_an_archive_nor_a_complete_receipt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Without the lab's archive or a complete producer receipt, compare would hold
    vacuously over nothing; it refuses instead."""
    bare = dataclasses.replace(DILATION_910, archive=None)
    monkeypatch.setitem(audit.DILATIONS, PACKET_910, bare)
    with pytest.raises(SystemExit, match="no complete producer receipt"):
        audit.compare(PACKET_910)


def test_the_910_replay_comparison_is_what_the_tool_recomputes() -> None:
    assert audit.main(["compare", PACKET_910, "--check"]) == 0


def test_every_910_direction_of_the_census_equals_the_labs_selected_line() -> None:
    """The census capture against the lab's merged archive: every field each selected
    line keeps, timings aside, at all 4,972 directions, and the node totals equal."""
    receipt = stored(PACKET_910, "compare")
    assert receipt["verdict"] == "EVERY_DIRECTION_AGREES"
    assert receipt["status"] == "VERIFIED"
    assert receipt["directions"] == receipt["archive_directions"] == 4972
    assert receipt["identical_on_archive_fields"] == 4972
    assert receipt["differing"] == {}
    assert receipt["nodes"] == receipt["archive_selected_nodes"] == 2462923881
    assert receipt["least_certified_bound"] == 1.0000000000003892


def test_a_capture_that_differs_from_an_archive_line_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    folder = copied_packet(tmp_path, monkeypatch)
    census = tmp_path / "packing/benchmarks/measure-verifier/census-mixed"
    (census / PACKET_910).mkdir(parents=True)
    capture = f"{PACKET_910}/{DILATION_910.name}.jsonl.gz"
    shutil.copy(audit.CENSUS / capture, census / capture)
    shutil.copy(audit.CENSUS / "census.json", census / "census.json")
    monkeypatch.setattr(audit, "CENSUS", census)
    merged = folder / "source/receipts/directions.jsonl.gz"
    lines = gzip.decompress(merged.read_bytes()).decode().splitlines()
    row = json.loads(lines[17])
    row["min_certified_lower_bound"] = 1.5
    lines[17] = json.dumps(row, separators=(",", ":"), sort_keys=True)
    merged.write_bytes(gzip.compress(("\n".join(lines) + "\n").encode(), mtime=0))
    receipt = audit.compare(PACKET_910)
    assert receipt["verdict"] == "DIRECTIONS_DIFFER"
    assert receipt["differing"] == {str(row["r"]): ["min_certified_lower_bound"]}
