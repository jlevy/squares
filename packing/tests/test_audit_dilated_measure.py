"""The #890 dilation's retained premise audit and replay comparison, held to their packet.

`devtools.audit_dilated_measure` recomputes both receipts from the retained bytes; these
tests ask that the committed receipts are what it recomputes, that they say what the
register relies on, and that its checks refuse the mutations they exist to catch.
"""

from __future__ import annotations

import copy
import gzip
import json
from fractions import Fraction
from typing import Any

import pytest

from devtools import audit_dilated_measure as audit

PACKET = "ozden-s94-lower-bound-2026-11-03"
DILATION = audit.DILATIONS[PACKET]


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
    assert receipt["dilation"]["axis_domain_growth_in_base_coordinates"] == "3/3986"
    assert receipt["dilation"]["route_ceiling"] == "99500/9977"
    digests = receipt["digests"]
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
    assert audit.dilation_checks(candidate(), base())["base_net_refuses_dilated_core"] is True


@pytest.mark.parametrize("extra", ["net", "certificate"])
def test_a_second_net_declaration_is_refused(extra: str) -> None:
    data = candidate()
    data[extra] = {"D": "83/40000"}
    checks = audit.file_checks(data, DILATION)
    assert checks["keys_known"] is False
