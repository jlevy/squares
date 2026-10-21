"""Joost de Winter's issue #668: three rational centre-basis witnesses at 227, 229 and 260.

The packet retains each witness as the author's exact JSON, read by the
`center-basis-json` adapter, and its `records.json`, which states the exact side and the
decimal the issue prints. The general importer's checks run on the packet through
``test_upper_bound_reports``; these hold what is particular to it: that the adapter reads
the side each record states, that each print is that side rounded up at twelve places,
where each side stands against the case and the other reports at its count, and the
margins the replay found. Every test reads the retained packet only; none needs the
network.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from typing import Any

import pytest

from devtools import upper_bound_reports as reports

DE_WINTER = "de-winter-upper-bounds-227-229-260-2026-10-17"
SOURCE_KEY = "[de Winter upper bounds 2026-10-17]"
COUNTS = (227, 229, 260)
#: Where each side stands: against the case, and against each other report at its count.
#: At 227 and 260 it is below the case and above a later Couzo report; at 229 it is above
#: the house best packing, Evan Daniel's T-199, and above his T-198 and Couzo's #672 as well.
RELATIONS = {
    227: ("below", {"#672": "above"}),
    229: ("above", {"#672": "above", "T-198 (#674)": "above"}),
    260: ("below", {"#678": "above"}),
}


def _records(n: int) -> dict[str, Any]:
    packet = reports.packet_path(DE_WINTER)
    text = (packet / "source" / f"n{n}" / "records.json").read_text(encoding="utf-8")
    (row,) = (row for row in json.loads(text)["records"] if row["n"] == n)
    return row


def _row(n: int) -> dict[str, Any]:
    (row,) = (
        row
        for row in reports.check_claims(reports.packet_path(DE_WINTER))["results"]
        if row["n"] == n
    )
    return row


@pytest.mark.parametrize("n", COUNTS)
def test_each_witness_states_the_side_its_record_states_and_the_reader_rebuilds_it(
    n: int,
) -> None:
    certificate = reports.read_facts(reports.packet_path(DE_WINTER))[n]
    assert certificate.n == n
    assert certificate.side == Fraction(_records(n)["certified_side_exact"])
    assert reports.house_side(SOURCE_KEY, n) == certificate.side


@pytest.mark.parametrize("n", COUNTS)
def test_each_print_is_its_side_rounded_up_at_twelve_places(n: int) -> None:
    side = reports.read_facts(reports.packet_path(DE_WINTER))[n].side
    printed = Fraction(_records(n)["decimal_upper_bound"])
    assert printed == Fraction(math.ceil(side * 10**12), 10**12)
    assert side < printed


@pytest.mark.parametrize("n", COUNTS)
def test_each_side_stands_where_the_frozen_comparison_says(n: int) -> None:
    row = _row(n)
    case, others = RELATIONS[n]
    assert row["case"]["relation"] == case
    assert {other["report"]: other["relation"] for other in row["pending"]} == others
    assert row["smallest"] != reports.THIS


def test_the_replay_clears_every_wall_and_pair_by_a_billionth() -> None:
    positives = reports.check_certification(reports.packet_path(DE_WINTER))
    margins = reports.margins(positives)
    assert sorted(margins) == list(COUNTS)
    for row in margins.values():
        for route in ("exact_verify", "independent"):
            assert Fraction(row[f"{route}_containment_clearance"]) == Fraction(1, 10**9)
            assert Fraction(1, 10**9) < Fraction(row[f"{route}_best_pair_gap"])
