"""Evan Daniel's issues #689 and #694: the evand lane of 20 October 2026.

Two certificates in the author's own text format, each retained under the MIT licence and
read by the `evand-cert` adapter: s(308) of #689 at ``bc0708f`` and s(154) of #694 at
``1d2bb82``. The general importer's checks run on both packets through
``test_upper_bound_reports``; these hold what is particular to them, as the stage 4 review
of 19 October asked of the five before them (RV-1 of
docs/project/reviews/review-2026-10-19-upper-bound-imports-659-664-669-674.md): how each
side was made, that each is below every report at its count by the margin the records
state, and that the house readers rebuild them. Every test reads retained packets only;
none needs the network.
"""

from __future__ import annotations

import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import upper_bound_reports as reports

CANDIDATES = "search/packer/candidates"
DANIEL_689 = "evand-n308-2026-10-19"
DANIEL_694 = "evand-n154-sweep-2026-10-20"
#: Packet, count, source key, the certificate's file stem and its exact side.
SIDES = (
    (
        DANIEL_689,
        308,
        "[Daniel n308 2026-10-19]",
        "s308_d308",
        Fraction(3599429824254181747030632150463, 2 * 10**29),
    ),
    (
        DANIEL_694,
        154,
        "[Daniel n154 sweep 2026-10-20]",
        "s154_sw",
        Fraction(1615137617595210068732072760947, 125 * 10**27),
    ),
)
#: Each certificate's margin below the house it would replace, bracketed in units of
#: 10^-12: T-174 at 308 and T-186 at 154.
MARGINS = {
    DANIEL_689: ("T-174", 1_120_758_255, 1_120_758_256),
    DANIEL_694: ("T-186", 105_636_370, 105_636_371),
}


def _folder(name: str) -> Path:
    packet = reports.packet_path(name)
    return reports.REPO / reports.acquisition(packet)["archived_path"] / CANDIDATES


def _row(name: str, n: int) -> dict[str, Any]:
    (row,) = (
        row
        for row in reports.check_claims(reports.packet_path(name))["results"]
        if row["n"] == n
    )
    return row


def _ceil_at(value: Fraction, places: int) -> Fraction:
    return Fraction(math.ceil(value * 10**places), 10**places)


@pytest.mark.parametrize(("name", "n", "key", "stem", "side"), SIDES)
def test_each_certificate_states_its_side_and_the_house_reader_rebuilds_it(
    name: str, n: int, key: str, stem: str, side: Fraction
) -> None:
    (certificate,) = reports.read_facts(reports.packet_path(name)).values()
    assert (certificate.n, certificate.side) == (n, side)
    assert reports.house_side(key, n) == side
    (row,) = reports.load_declaration(reports.packet_path(name))["certificates"]
    assert row["path"] == f"{CANDIDATES}/{stem}.cert"


@pytest.mark.parametrize(("name", "n", "key", "stem", "side"), SIDES)
def test_each_side_is_its_kkt_point_scaled_by_1e20_and_rounded_up_at_30_places(
    name: str, n: int, key: str, stem: str, side: Fraction
) -> None:
    del key
    head = (_folder(name) / f"{stem}.exact.txt").read_text("utf-8").split("\n")[0]
    count, kkt = head.split()
    assert int(count) == n
    assert side == _ceil_at(Fraction(Decimal(kkt)) * (1 + Fraction(1, 10**20)), 30)
    regularized = (_folder(name) / f"{stem}_regularized.cert").read_bytes()
    assert reports.evand_cert(regularized, n, {}).side == side


@pytest.mark.parametrize(("name", "n"), [(name, n) for name, n, *_rest in SIDES])
def test_each_certificate_is_below_its_house_and_every_report_it_names(
    name: str, n: int
) -> None:
    row = _row(name, n)
    assert row["smallest"] == reports.THIS
    assert row["case"]["relation"] == "below"
    assert {other["relation"] for other in row["pending"]} == {"below"}
    house, low, high = MARGINS[name]
    assert row["case"]["result"] == house
    assert Fraction(low, 10**12) < Fraction(row["case"]["difference"]) < Fraction(high, 10**12)


@pytest.mark.parametrize("name", [DANIEL_689, DANIEL_694])
def test_the_replay_clears_walls_and_pairs_by_the_margins_its_construction_gives(
    name: str,
) -> None:
    positives = reports.check_certification(reports.packet_path(name))
    (margins,) = reports.margins(positives).values()
    for route in ("exact_verify", "independent"):
        assert Fraction(margins[f"{route}_containment_clearance"]) >= Fraction(1, 2 * 10**20)
        assert Fraction(margins[f"{route}_best_pair_gap"]) >= Fraction(999, 10**23)
