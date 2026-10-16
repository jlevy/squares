"""PR #622: PingYou Ltd's N29 certificate, whose geometry is in a release asset.

The pull request's pinned commit 3115557 adds a HostedData manifest binding one release
asset of BuddenPing/square-packing-certificates by size and SHA-256, and the certificate is
a member of that zip. The packet keeps it as a derived exact fact, held there to the
source's own corners Witness/v2. The general importer's checks run on it through
``test_upper_bound_reports``; these hold what is particular to it: the digests the pull
request states, the exact margins below T-155 and below PR #574's N29 certificate, the
undecided comparison with the reported lane's catalogue print, the two refused controls on
both maintained routes, and the verified print that n-029.md keeps above its own exact
form (think-gzrw). Nothing here needs Git or the network.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
from test_upper_bound_reports_574 import private

from devtools import upper_bound_reports as reports
from sqpack.yamlio import safe_load

__all__ = ["private"]

PACKET = "pingyou-pr622-certificate-2026-10-15"
N = 29
#: The digests the pull request's claims.json and HostedData manifest state.
CERTIFICATE_SHA256 = "a01428c51875679fbe78c11a803742b8d99f44b916a660ab6801bb0fcf76951b"
NATIVE_SHA256 = "0eff5b4d2a9701e30fe8912fd634c5a7124384366197533c18a5bcc26dfe4a39"
ASSET_SHA256 = "0dc9bcd1cf5f2806a4d2e0c4c1c07e4903d91bbea611b8b938bda770b9782537"
#: T-155's exact side at 29, the exact form of n-029.md's verified lane.
T155 = Fraction("296691673133846459484473030817600957/50000000000000000000000000000000000")
#: The 14 October ledger's transcription of PR #574's N29 side, from that pull request's
#: claims.json at 4c319c2: a v2 row T-174 does not register.
LEDGER_1014 = reports.ROOT / "campaign/issue-intake/upper-bounds-20261014/sources.yaml"


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _packet() -> Path:
    return reports.packet_path(PACKET)


def _row() -> dict[str, Any]:
    (row,) = reports.check_claims(_packet())["results"]
    return row


def _side() -> Fraction:
    return reports.read_facts(_packet())[N].side


def _pr574_side() -> Fraction:
    sources = safe_load(LEDGER_1014.read_text(encoding="utf-8"))
    (report,) = [item for item in sources["reports"] if item["report"] == "PR #574"]
    (claim,) = [item for item in report["claims"] if item["n"] == N]
    return Fraction(claim["exact"])


def test_the_packet_pins_its_release_and_retains_no_upstream_byte() -> None:
    (source,) = _json(_packet() / "acquisition/sources.json")["sources"]
    assert (source["retained_file_count"], source["retained_total_bytes"]) == (0, 0)
    assert source["source_commit"] == "31155575ce1e6b461f77bfc9f3e201adf101115b"
    (declared,) = reports.load_declaration(_packet())["certificates"]
    # Read as a plain mapping: the row's `fact`, `archive` and `same_packing` are optional
    # in its contract, and this packet states all three.
    row: dict[str, Any] = dict(declared)
    assert row["fact"] == "facts/n-029.yaml"
    assert row["archive"]["sha256"] == CERTIFICATE_SHA256
    assert row["archive"]["tag"] == "data/pingyou-n29-certificate-2026-10-15-v1"
    (native,) = row["same_packing"]
    assert native["format"] == "witness-corners"
    assert native["archive"]["sha256"] == NATIVE_SHA256
    pinned = {item["path"]: item for item in source["pinned_only"]}
    manifest = pinned["packing/hosted/pingyou-n29-certificate-2026-10-15.yaml"]
    assert manifest["sha256"]
    declaration = reports.load_declaration(_packet())
    fact = reports.read_fact(_packet(), declaration, declared)
    assert fact.side == Fraction(row["offered"])


def test_the_side_is_below_t155_and_pr574_by_the_margins_the_pull_request_states() -> None:
    side = _side()
    case = _row()["case"]
    assert case["result"] == "T-155"
    assert case["relation"] == "below"
    assert Fraction(case["exact_side"]) == T155
    assert Fraction(case["difference"]) == T155 - side
    # The pull request prints both margins rounded at 15 significant digits.
    assert abs((T155 - side) / Fraction("1.56616581892211e-36") - 1) < Fraction(1, 10**14)
    margin = _pr574_side() - side
    assert margin > 0
    assert abs(margin / Fraction("7.32482673606514e-90") - 1) < Fraction(1, 10**14)


def test_the_catalogue_print_and_pr574s_print_leave_the_comparison_undecided() -> None:
    row = _row()
    assert row["case"]["reported_relation"] == "undecided"
    (pr574,) = row["pending"]
    assert (pr574["report"], pr574["relation"]) == ("PR #574", "undecided")
    assert row["smallest"] is None
    # The catalogue's 5.93383346267692 is below the side, within one unit of its last place.
    printed = Fraction("5.93383346267692")
    assert printed < _side() < printed + Fraction(1, 10**14)


def test_the_receipt_holds_both_controls_refused_on_both_routes() -> None:
    reports.check_certification(_packet())
    _declaration, facts = reports.replayed_facts(_packet())
    (part, _), *rest = reports.receipt_parts(_packet(), facts)
    assert not rest
    cases = {row["control"]: row for row in part["cases"]}
    assert set(cases) == set(reports.JOBS)
    for control, row in cases.items():
        positive = control == "positive"
        for route in ("exact_verify", "independent"):
            assert row[route]["verification_passed"] is positive, (control, route)
            assert row[route]["pairs_tested"] == N * (N - 1) // 2
    margins = reports.margins({N: cases["positive"]})[N]
    assert set(margins.values()) == {"0"}


def test_the_case_keeps_a_verified_print_above_its_exact_form(
    private: Callable[[str], Path],
) -> None:
    """n-029.md prints T-155's verified lane at the decimal it printed before (think-gzrw).

    The declaration states the exact form the case states, and the house's side must be it
    exactly; a print below it, or another exact form, is refused.
    """
    packet = private(PACKET)
    (declared,) = reports.load_declaration(packet)["houses"]
    house: dict[str, Any] = dict(declared)
    assert Fraction(house["verified_value"]) - T155 > Fraction(5, 10**20)
    assert Fraction(house["verified_exact_form"]) == T155
    reports.compare(packet)
    path = packet / reports.DECLARATION
    other_form = T155 + Fraction(1, 25 * 10**33)
    for change in (
        {"verified_exact_form": f"{other_form.numerator}/{other_form.denominator}"},
        {"verified_value": "5.93383346267692918968946061635201913"},
    ):
        value = _json(path)
        value["houses"][0].update(change)
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        with pytest.raises(reports.ReportError, match="verified exact form"):
            reports.compare(packet)
    value = _json(path)
    del value["houses"][0]["verified_exact_form"]
    value["houses"][0]["verified_value"] = house["verified_value"]
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    with pytest.raises(reports.ReportError, match="exact or rounded up"):
        reports.compare(packet)


def test_the_packet_is_a_house_reader_of_its_own_side() -> None:
    declaration = reports.load_declaration(_packet())
    assert reports.house_side(declaration["source_key"], N) == _side()


def test_the_ledger_leaves_both_reports_undecided_and_names_the_key_reason() -> None:
    """The per-count ledger of this pass: PR #574's row and PR #622 in report order."""
    from devtools import intake_ledger as ledger  # noqa: PLC0415

    directory = ledger.ROOT / "campaign/issue-intake/upper-bounds-n29-20261016"
    assert ledger.problems(ledger.load_yaml(directory / ledger.LEDGER)) == []
    assert ledger.render(directory, check=True) == []
    verdicts = json.loads((directory / ledger.VERDICTS).read_text("utf-8"))
    (count,) = verdicts["counts"]
    assert count["n"] == N
    assert [(step["report"], step["verdict"]) for step in count["steps"]] == [
        ("PR #574", ledger.UNDECIDED),
        ("PR #622", ledger.UNDECIDED),
    ]
    (found,) = ledger.load_ledger(directory).get("key_reason_candidates") or []
    candidate: dict[str, Any] = dict(found)
    assert (candidate["n"], candidate["report"]) == (N, "PR #622")
    assert candidate["proposed_as"].startswith("T-195")
