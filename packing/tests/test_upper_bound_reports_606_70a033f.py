"""Issue #606 and Mishapolk's 70a033f: the evening intake of 14 October 2026.

Evan Daniel's s(146) (#606) is retained under the MIT licence at e006ce6 and read by the
`evand-cert` adapter. Mykhailo Polkovskyi's 24 certificates at 70a033f, which no issue
reports, are kept as derived facts, since the source states no licence, and admitted at
the census's exact fractions. At 153, 207 and 302 PR #574's sides are algebraic, and the
comparison reads them exactly from that packet's derived field witnesses (`algebraic`
pending reports). Francisco Couzo's unnamed 175 of #506, which he asked the same day to
import, has a hand-written register plan in its packet. The general importer's checks run
on both packets through ``test_upper_bound_reports``; these hold what is particular to
them. Every test reads retained packets only; none needs the network.
"""

from __future__ import annotations

import json
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
import yaml

from devtools import check_standing
from devtools import upper_bound_reports as reports
from sqpack.field import NumberField

DANIEL_606 = "evand-n146-2026-10-14"
MISHAPOLK_70A = "mishapolk-kkt-refinements-2026-10-14"
COUZO_506 = "couzo-certificates-2026-10-11"
CANDIDATES = "search/packer/candidates"
#: The seven files e006ce6 adds for 146.
SEVEN = (
    "tt2_n146.cert",
    "tt2_n146.exact.txt",
    "tt2_n146.input.txt",
    "tt2_n146.json",
    "tt2_n146_regularized.cert",
    "tt2_n146_regularized.json",
    "tt2_n146_vs505.json",
)
ISSUE_399 = "packing/resources/web/evand-new-arrangements-2026-10-07/source/s12/search/exact"
#: The counts where 70a033f's certificate is below every earlier report, in report order.
RECORDED = (129, 154, 156, 175, 176, 204, 232, 264, 271, 302, 303, 304)
#: The other twelve certificates the commit replaces, PR #574 (T-174) smaller at each.
NOT_RECORDED = (153, 155, 181, 207, 209, 267, 270, 272, 305, 306, 307, 308)


def _rows(name: str) -> dict[int, dict[str, Any]]:
    return {row["n"]: row for row in reports.check_claims(reports.packet_path(name))["results"]}


def _source(name: str) -> Path:
    return reports.REPO / reports.acquisition(reports.packet_path(name))["archived_path"]


# --------------------------------------------------------------------------- #606


def test_the_606_packet_retains_the_seven_n146_files_and_pins_the_checkers_to_399() -> None:
    retained = sorted(path.name for path in (_source(DANIEL_606) / CANDIDATES).iterdir())
    assert retained == sorted(SEVEN)
    record = json.loads(
        (reports.packet_path(DANIEL_606) / "acquisition/sources.json").read_text("utf-8")
    )
    (source,) = record["sources"]
    assert source["source_commit"] == "e006ce6230f2240457b083199755a3a5d287692c"
    assert source["committed_utc"] == "2026-10-14T21:50:35Z"
    pinned = {item["path"]: item for item in source["pinned_only"]}
    assert set(pinned) == {
        "search/exact/verify_cert.py",
        "search/exact/verify_cert2.py",
        "search/packer/PACKER.md",
    }
    for name in ("verify_cert.py", "verify_cert2.py"):
        assert pinned[f"search/exact/{name}"]["identical_to"] == f"{ISSUE_399}/{name}"


def test_the_606_side_is_the_kkt_point_scaled_by_1e20_and_rounded_up_at_30_places() -> None:
    (certificate,) = reports.read_facts(reports.packet_path(DANIEL_606)).values()
    folder = _source(DANIEL_606) / CANDIDATES
    count, kkt = (folder / "tt2_n146.exact.txt").read_text("utf-8").split("\n")[0].split()
    assert int(count) == 146
    scaled = Fraction(Decimal(kkt)) * (1 + Fraction(1, 10**20))
    assert certificate.side - Fraction(1, 10**30) < scaled <= certificate.side
    assert certificate.side == Fraction(12583782190151860342292508597077, 10**30)
    regular = reports.evand_cert((folder / "tt2_n146_regularized.cert").read_bytes(), 146, {})
    assert regular.side == certificate.side


def test_the_606_certificate_is_below_every_report_at_146() -> None:
    row = _rows(DANIEL_606)[146]
    assert (row["smallest"], row["case"]["result"], row["case"]["relation"]) == (
        reports.THIS,
        "T-150",
        "below",
    )
    margin = Fraction(row["case"]["difference"])
    assert Fraction(1379, 10**11) < margin < Fraction(1381, 10**11)
    others = {other["report"]: other for other in row["pending"]}
    assert set(others) == {
        "T-101 (#375)",
        "T-125 (#432)",
        "T-146 (no issue)",
        "T-168 (#566)",
        "T-174 (PR #574)",
        "#593",
    }
    assert {other["relation"] for other in others.values()} == {"below"}
    # The smallest earlier report, PingYou Ltd's PR #574, is 1.38e-8 above this side too.
    closest = Fraction(others["T-174 (PR #574)"]["difference"])
    assert Fraction(1379, 10**11) < closest < Fraction(1380, 10**11)


def test_the_house_readers_rebuild_the_new_sides() -> None:
    (certificate,) = reports.read_facts(reports.packet_path(DANIEL_606)).values()
    assert reports.house_side("[Daniel n146 2026-10-14]", 146) == certificate.side
    facts = reports.read_facts(reports.packet_path(MISHAPOLK_70A), {129, 302})
    for n, fact in facts.items():
        assert reports.house_side("[Mishapolk KKT refinements 2026-10-14]", n) == fact.side


def test_the_606_replay_clears_every_wall_by_5e_21_and_every_pair_by_just_under_1e_20() -> None:
    positives = reports.check_certification(reports.packet_path(DANIEL_606))
    (margins,) = reports.margins(positives).values()
    for route in ("exact_verify", "independent"):
        assert Fraction(margins[f"{route}_containment_clearance"]) == Fraction(1, 2 * 10**20)
        gap = Fraction(margins[f"{route}_best_pair_gap"])
        assert Fraction(999, 10**23) < gap < Fraction(1, 10**20)


# --------------------------------------------------------------------------- 70a033f


def test_the_70a033f_certificates_are_admitted_at_the_census_fractions() -> None:
    packet = reports.packet_path(MISHAPOLK_70A)
    declaration = reports.load_declaration(packet)
    assert declaration["issue"] == "(no issue)"
    rows = declaration["certificates"]
    assert [row["n"] for row in rows] == sorted(RECORDED + NOT_RECORDED)
    assert {row["first_committed"] for row in rows} == {"2026-10-14T16:11:31Z"}
    facts = reports.read_facts(packet)
    for row in rows:
        assert facts[row["n"]].side == Fraction(row["offered"])
    assert declaration["requested"] == list(RECORDED)


def test_70a033f_is_smallest_exactly_at_the_twelve_recorded_counts() -> None:
    rows = _rows(MISHAPOLK_70A)
    assert sorted(n for n, row in rows.items() if row["smallest"] == reports.THIS) == list(
        RECORDED
    )
    for n in NOT_RECORDED:
        assert rows[n]["smallest"] == "T-174 (PR #574)", n


def test_207_is_decided_exactly_against_pr_574s_degree_5_side() -> None:
    """PR #574's 40-place print left 207 undecided; its field witness decides it."""
    row = _rows(MISHAPOLK_70A)[207]
    (pr574,) = [other for other in row["pending"] if other["report"] == "T-174 (PR #574)"]
    assert pr574["algebraic"] == "pingyou-pr574-certificates-2026-10-13"
    assert pr574["relation"] == "above"
    low, high = (Fraction(value) for value in pr574["difference_bounds"])
    # PR #574's side is below this certificate's by 1.488e-99.
    assert -Fraction(1489, 10**102) < low <= high < -Fraction(1487, 10**102)
    assert low <= Fraction(pr574["difference"]) <= high


def test_an_algebraic_side_is_decided_by_one_exact_sign() -> None:
    root2 = NumberField([1, 0, -2], (Fraction(1), Fraction(2))).alpha
    # A certificate side of 1.4142 is below sqrt(2), and its enclosure excludes that side.
    verdict, span, low, high = reports.algebraic_against(root2, Fraction(14142, 10**4))
    assert verdict == "below"
    assert span.low > Fraction(14142, 10**4)
    assert 0 < low <= high
    assert (high - low) * 10**6 <= low
    verdict, _span, low, high = reports.algebraic_against(root2, Fraction(14143, 10**4))
    assert verdict == "above"
    assert low <= high < 0
    assert reports.algebraic_against(Fraction(3, 2), Fraction(3, 2))[0] == "equal"


def test_an_algebraic_comparison_refines_to_its_ceiling_and_refuses_past_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Review A10 of #612: the last refinement is to the stated ceiling itself, and a side
    that does not separate there is refused rather than guessed."""
    root2 = NumberField([1, 0, -2], (Fraction(1), Fraction(2))).alpha
    # sqrt(2) rounded down at 80 places: about 1e-80 below it, so the enclosure needs about
    # 87 places to exclude it to one part in a million.
    side = Fraction(math.isqrt(2 * 10**160), 10**80)
    # Doubling from 60 would stop at 60, short of 90; the loop refines to 90 itself.
    monkeypatch.setattr(reports, "ALGEBRAIC_PLACES", (60, 90))
    verdict, _span, low, high = reports.algebraic_against(root2, side)
    assert verdict == "below"
    assert 0 < low <= high < Fraction(1, 10**79)
    root2 = NumberField([1, 0, -2], (Fraction(1), Fraction(2))).alpha
    monkeypatch.setattr(reports, "ALGEBRAIC_PLACES", (60, 60))
    with pytest.raises(reports.ReportError, match=r"does not separate .* at 60 places"):
        reports.algebraic_against(root2, side)


@pytest.mark.parametrize(
    ("extra", "message"),
    [
        ({"printed": "1.5", "rounding": "up"}, "no printed side"),
        ({"reader": "grid"}, "nor an algebraic one"),
    ],
)
def test_the_declaration_refuses_an_algebraic_side_beside_another(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, extra: dict[str, str], message: str
) -> None:
    source = reports.packet_path(MISHAPOLK_70A) / reports.DECLARATION
    declaration = json.loads(source.read_text("utf-8"))
    (pending,) = [p for p in declaration["pending"] if p["n"] == 207 and "algebraic" in p]
    pending.update(extra)
    packet = tmp_path / "private" / "packing/resources/web" / MISHAPOLK_70A
    (packet / "acquisition").mkdir(parents=True)
    (packet / reports.DECLARATION).write_text(json.dumps(declaration), "utf-8")
    monkeypatch.setattr(reports, "REPO", tmp_path / "private")
    with pytest.raises(reports.ReportError, match=message):
        reports.load_declaration(packet)


def test_the_175_plan_states_couzos_side_superseded_by_t158() -> None:
    """Couzo's unnamed 175 at 337078c, which he asked on #506 to import (14 October)."""
    plan = yaml.safe_load(
        (reports.packet_path(COUZO_506) / "register-plan-n175.yaml").read_text("utf-8")
    )
    claim = " ".join(plan["results.yaml"]["claim"].split())
    ((key, bound),) = check_standing.statements(claim, [175]).items()
    couzo = reports.house_side("[Couzo certificates 2026-10-11]", 175)
    assert (key[0], bound.value) == (175, couzo)
    # Below T-140, the standing report when it was published, by 1.70e-6; T-158 (#528),
    # reported the next day, is below it by 2.94e-3 and supersedes it.
    t140 = reports.house_side("[Couzo certificates 2026-10-10]", 175)
    t158 = reports.house_side("[Ostashev records 2026-10-12]", 175)
    assert Fraction(169, 10**8) < t140 - couzo < Fraction(171, 10**8)
    assert Fraction(294, 10**5) < couzo - t158 < Fraction(295, 10**5)


def test_the_70a033f_replay_admits_every_count_on_both_routes() -> None:
    positives = reports.check_certification(reports.packet_path(MISHAPOLK_70A))
    assert sorted(positives) == sorted(RECORDED + NOT_RECORDED)
    for margins in reports.margins(positives).values():
        for route in ("exact_verify", "independent"):
            assert Fraction(margins[f"{route}_containment_clearance"]) >= 0
            assert Fraction(margins[f"{route}_best_pair_gap"]) > 0
