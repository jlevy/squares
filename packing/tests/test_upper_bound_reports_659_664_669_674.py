"""Evan Daniel's issues #659, #664, #669 and #674: the evand lane of 19 October 2026.

Five certificates in the author's own text format, each retained under the MIT licence
and read by the `evand-cert` adapter: s(155) of #669 (T-197), s(229) of #674's opening
post and of its update (T-198, T-199), s(236) of #659 and s(271) of #664. The general
importer's checks run on all five packets through ``test_upper_bound_reports``; these hold
what is particular to them, as the stage 4 review of 19 October asked (RV-1 of
docs/project/reviews/review-2026-10-19-upper-bound-imports-659-664-669-674.md): how each
side was made, that each is below every report at its count, and that the house readers
rebuild them. Every test reads retained packets only; none needs the network.
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
DANIEL_669 = "evand-n155-explorer-2026-10-17"
DANIEL_674 = "evand-n229-dilation-2026-10-17"
DANIEL_674_UPDATE = "evand-n229-dilation-update-2026-10-18"
DANIEL_659 = "evand-n236-2026-10-16"
DANIEL_664 = "evand-n271-2026-10-17"
#: Packet, count, source key and the certificate's exact side.
SIDES = (
    (
        DANIEL_669,
        155,
        "[Daniel n155 explorer 2026-10-17]",
        Fraction(2590452188930112807053435932173, 2 * 10**29),
    ),
    (
        DANIEL_674,
        229,
        "[Daniel n229 dilation 2026-10-17]",
        Fraction(7825081627429265081627421439843, 5 * 10**29),
    ),
    (
        DANIEL_674_UPDATE,
        229,
        "[Daniel n229 dilation update 2026-10-18]",
        Fraction(7825080756947776580756939951343, 5 * 10**29),
    ),
    (
        DANIEL_659,
        236,
        "[Daniel n236 2026-10-16]",
        Fraction(7930967195303679308621899285697, 5 * 10**29),
    ),
    (
        DANIEL_664,
        271,
        "[Daniel n271 2026-10-17]",
        Fraction(16948947733713657510723401112423, 10**30),
    ),
)
#: The KKT point the certificate scales by 1 + 10^-20, for the three solved certificates.
KKT = {DANIEL_669: "s155_ex2", DANIEL_659: "s236_bm3c", DANIEL_664: "s271_ex1"}
#: The binary64 input the certificate dilates, for the two dilation certificates.
DILATED = {DANIEL_674: "s229", DANIEL_674_UPDATE: "s229_v2"}
#: The dilation's delta as `dilate_cert.py` reads it: the double nearest 10^-12.
DELTA = Fraction(1e-12)


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


@pytest.mark.parametrize(("name", "n", "key", "side"), SIDES)
def test_each_certificate_states_its_side_and_the_house_reader_rebuilds_it(
    name: str, n: int, key: str, side: Fraction
) -> None:
    (certificate,) = reports.read_facts(reports.packet_path(name)).values()
    assert (certificate.n, certificate.side) == (n, side)
    assert reports.house_side(key, n) == side


@pytest.mark.parametrize("name", sorted(KKT))
def test_a_solved_side_is_its_kkt_point_scaled_by_1e20_and_rounded_up_at_30_places(
    name: str,
) -> None:
    (certificate,) = reports.read_facts(reports.packet_path(name)).values()
    head = (_folder(name) / f"{KKT[name]}.exact.txt").read_text("utf-8").split("\n")[0]
    count, kkt = head.split()
    assert int(count) == certificate.n
    assert certificate.side == _ceil_at(Fraction(Decimal(kkt)) * (1 + Fraction(1, 10**20)), 30)
    regularized = (_folder(name) / f"{KKT[name]}_regularized.cert").read_bytes()
    assert reports.evand_cert(regularized, certificate.n, {}).side == certificate.side


@pytest.mark.parametrize("name", sorted(DILATED))
def test_a_dilation_side_is_its_input_side_times_1_plus_delta_rounded_up_at_30_places(
    name: str,
) -> None:
    (certificate,) = reports.read_facts(reports.packet_path(name)).values()
    text = (_folder(name) / f"{DILATED[name]}.input.txt").read_text("utf-8")
    count, side = text.split("\n")[0].split()
    assert int(count) == certificate.n == 229
    assert Fraction(1, 10**12) != DELTA
    assert certificate.side == _ceil_at(Fraction(Decimal(side)) * (1 + DELTA), 30)


@pytest.mark.parametrize(("name", "n"), [(name, n) for name, n, _key, _side in SIDES])
def test_each_certificate_is_below_its_case_and_every_report_it_names(
    name: str, n: int
) -> None:
    row = _row(name, n)
    assert row["smallest"] == reports.THIS
    assert row["case"]["relation"] == "below"
    assert {other["relation"] for other in row["pending"]} == {"below"}


def test_the_update_is_below_the_opening_by_1_74e_6() -> None:
    row = _row(DANIEL_674_UPDATE, 229)
    (opening,) = (other for other in row["pending"] if other.get("result") == "T-198")
    margin = Fraction(opening["difference"])
    assert Fraction(1740, 10**9) < margin < Fraction(1742, 10**9)


@pytest.mark.parametrize(
    ("name", "wall", "pair"),
    [
        (DANIEL_669, Fraction(1, 2 * 10**20), Fraction(999, 10**23)),
        (DANIEL_659, Fraction(1, 2 * 10**20), Fraction(999, 10**23)),
        (DANIEL_664, Fraction(1, 2 * 10**20), Fraction(999, 10**23)),
        (DANIEL_674, Fraction(5, 10**13), Fraction(999, 10**15)),
        (DANIEL_674_UPDATE, Fraction(6, 10**13), Fraction(12, 10**13)),
    ],
)
def test_the_replay_clears_walls_and_pairs_by_the_margins_its_construction_gives(
    name: str, wall: Fraction, pair: Fraction
) -> None:
    positives = reports.check_certification(reports.packet_path(name))
    (margins,) = reports.margins(positives).values()
    for route in ("exact_verify", "independent"):
        assert Fraction(margins[f"{route}_containment_clearance"]) >= wall
        assert Fraction(margins[f"{route}_best_pair_gap"]) >= pair
