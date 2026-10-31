"""Hyukdong Kim's exact configurations for T-244 (issue 804): custody, side, both routes.

`devtools.configuration_fact_replay` reads the two configurations the
``hyukdongkim-t244-configurations-2026-10-25`` packet keeps as derived facts. This holds
each fact to the member digest the comment states, each side to T-244's, the route-1
receipts to the witness rebuilt from each fact, and the route-2 receipt to the checker
that ran and to its controls; and refuses a fact that no longer rebuilds the author's file.
"""

from __future__ import annotations

import copy
import json

import pytest

from devtools import configuration_fact_replay as replay


def test_each_fact_rebuilds_the_certificate_the_comment_pins() -> None:
    rows = replay.custody()
    assert [row["n"] for row in rows] == [172, 263]
    assert [row["field_degree"] for row in rows] == [24, 17]
    assert [row["rebuilt_bytes"] for row in rows] == [197519, 269624]


def test_each_rebuilt_file_is_the_file_the_comment_pins() -> None:
    """The custody claim the records make: each fact rebuilds the author's file, whose
    SHA-256 the comment states, and a changed configuration does not."""
    for row in replay.custody():
        assert row["rebuilt_sha256"] == row["member_sha256"]
    fact = replay.load(263)
    changed = copy.deepcopy(fact)
    changed["configuration"]["squares"][0]["x"][0] = "1/3"
    assert replay.sha256(replay.certificate_bytes(changed)) != fact["source"]["member_sha256"]


def test_route_two_ran_on_the_rebuilt_files() -> None:
    receipt = json.loads(replay.ROUTE2_RECEIPT.read_text(encoding="utf-8"))
    stated = {row["n"]: row["member_sha256"] for row in replay.custody()}
    for row in receipt["rows"]:
        assert row["positive"]["input_sha256"] == stated[row["n"]]


def test_each_side_is_t244s_and_the_receipt_says_so() -> None:
    record = replay.side_check()
    assert record["agrees"] is True
    stored = json.loads(replay.SIDE_RECEIPT.read_text(encoding="utf-8"))
    assert stored == record


def test_the_controls_mutate_what_they_name() -> None:
    data = replay.load(172)["configuration"]
    for kind in replay.CONTROLS:
        mutated, what = replay.mutate(data, kind)
        assert mutated != data
        assert what
    with pytest.raises(replay.ReplayError):
        replay.mutate(data, "unknown")


def test_route_one_receipts_hold_each_rebuilt_witness() -> None:
    for n in replay.COUNTS:
        record = replay.check_route1(n)
        assert record["cases"][0]["exact_verify"]["verification_passed"] is True


def test_route_two_accepts_both_files_and_refuses_every_control() -> None:
    summary = replay.check_route2()
    assert summary == {"positives_valid": 2, "controls_refused": 8, "controls": 8}
