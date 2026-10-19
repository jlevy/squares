"""Issue #552: Evan Daniel's s(154) certificate, imported by declaration.

The certificate is in Evan Daniel's text format, retained under the MIT licence at
597e660 with the regularized drawing of the same packing beside it, and read by the
`evand-cert` adapter. The general importer's checks run on the packet through
``test_upper_bound_reports``; these hold what is particular to it. Every test reads
retained packets only; none needs the network.
"""

from __future__ import annotations

import json
from decimal import Decimal
from fractions import Fraction
from typing import Any

from devtools import upper_bound_reports as reports

DANIEL_552 = "evand-n154-2026-10-12"
SOURCE_KEY = "[Daniel n154 2026-10-12]"
CANDIDATES = "search/packer/candidates"
#: The six files 597e660 adds for 154: the certificate, its KKT point, the binary64
#: input, the solver's report, and the regularized drawing with its report.
SIX = (
    "tt_n154.cert",
    "tt_n154.exact.txt",
    "tt_n154.input.txt",
    "tt_n154.json",
    "tt_n154_regularized.cert",
    "tt_n154_regularized.json",
)
ISSUE_399 = "packing/resources/web/evand-new-arrangements-2026-10-07/source/s12/search/exact"


def _packet() -> Any:
    return reports.packet_path(DANIEL_552)


def _source() -> Any:
    return reports.REPO / reports.acquisition(_packet())["archived_path"]


def _row() -> dict[str, Any]:
    (row,) = reports.check_claims(_packet())["results"]
    return row


def test_the_packet_retains_the_six_n154_files_and_pins_the_checkers_to_399() -> None:
    retained = sorted(path.name for path in (_source() / CANDIDATES).iterdir())
    assert retained == sorted(SIX)
    record = json.loads((_packet() / "acquisition/sources.json").read_text("utf-8"))
    (source,) = record["sources"]
    assert source["source_commit"] == "597e660c9a078a552991ab893cda3ab693cb5ac8"
    pinned = {item["path"]: item for item in source["pinned_only"]}
    assert set(pinned) == {
        "search/exact/verify_cert.py",
        "search/exact/verify_cert2.py",
        "search/packer/PACKER.md",
        "search/packer/timetravel.py",
    }
    for name in ("verify_cert.py", "verify_cert2.py"):
        assert pinned[f"search/exact/{name}"]["identical_to"] == f"{ISSUE_399}/{name}"


def test_the_side_is_the_kkt_point_scaled_by_1e20_and_rounded_up_at_30_places() -> None:
    (certificate,) = reports.read_facts(_packet()).values()
    first = (_source() / CANDIDATES / "tt_n154.exact.txt").read_text("utf-8").split("\n")[0]
    count, kkt = first.split()
    assert int(count) == 154
    scaled = Fraction(Decimal(kkt)) * (1 + Fraction(1, 10**20))
    unit = Fraction(1, 10**30)
    assert certificate.side - unit < scaled <= certificate.side
    assert certificate.side == Fraction(12922566401934059503377267965457, 10**30)


def test_the_certificate_is_smallest_at_154_and_below_t136_by_5_04e_4() -> None:
    row = _row()
    assert (row["smallest"], row["case"]["result"], row["case"]["relation"]) == (
        reports.THIS,
        "T-136",
        "below",
    )
    margin = Fraction(row["case"]["difference"])
    assert Fraction(5037, 10**7) < margin < Fraction(5039, 10**7)
    others = {other["report"]: other for other in row["pending"]}
    assert set(others) == {
        "T-127 (#438)",
        "#470",
        "T-115 (#401)",
        "T-113 (#401)",
        "T-098 (#375)",
        "T-056",
    }
    assert {other["relation"] for other in others.values()} == {"below"}
    # The case on main still held T-127, Gupta's refinement, 3.996e-3 above this side.
    gupta = Fraction(others["T-127 (#438)"]["difference"])
    assert Fraction(3995, 10**6) < gupta < Fraction(3997, 10**6)


def test_the_house_reader_rebuilds_the_552_side() -> None:
    (certificate,) = reports.read_facts(_packet()).values()
    assert reports.house_side(SOURCE_KEY, 154) == certificate.side


def test_the_regularized_drawing_has_the_same_side_and_moves_only_flat_squares() -> None:
    folder = _source() / CANDIDATES
    original = reports.evand_cert((folder / "tt_n154.cert").read_bytes(), 154, {})
    regular = reports.evand_cert((folder / "tt_n154_regularized.cert").read_bytes(), 154, {})
    assert regular.side == original.side
    differ = [
        index
        for index, (a, b) in enumerate(zip(original.poses, regular.poses, strict=True))
        if a != b
    ]
    assert len(differ) == 42
    report = json.loads((folder / "tt_n154.json").read_text("utf-8"))
    flat = set(report["second_order"]["flat_squares"]) | set(report["free_squares"])
    assert set(differ) <= flat
    # Only the eight rattlers turn; every load-bearing square keeps its half-angle.
    turned = {i for i in differ if original.poses[i].t != regular.poses[i].t}
    assert turned <= set(report["free_squares"])


def test_the_replay_clears_every_wall_by_5e_21_and_every_pair_by_just_under_1e_20() -> None:
    positives = reports.check_certification(_packet())
    (margins,) = reports.margins(positives).values()
    for route in ("exact_verify", "independent"):
        assert Fraction(margins[f"{route}_containment_clearance"]) == Fraction(1, 2 * 10**20)
        gap = Fraction(margins[f"{route}_best_pair_gap"])
        assert Fraction(999, 10**23) < gap < Fraction(1, 10**20)
