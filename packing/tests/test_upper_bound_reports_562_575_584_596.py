"""Issues #562, #575, #584 and #596: two Ostashev releases and Evan Daniel's compositions.

Daniil Ostashev's #562 names fe43a64 and #575 names b909e1b of the same repository; each
packet retains the certificates its issue names and pins the rest. Evan Daniel's #584
and #596 each request three counts beyond the case corpus and nothing inside it, so their
register plans hold beyond-horizon rows and no register entry. The general importer's
checks run on all four through ``test_upper_bound_reports``; these hold what is
particular to them. Every test reads retained packets only.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import PurePosixPath
from typing import Any

import pytest

from devtools import check_source_coverage as coverage_check
from devtools import upper_bound_reports as reports

OSTASHEV_501 = "dostashev-records-2026-10-11"
OSTASHEV_562 = "dostashev-compositions-2026-10-12"
OSTASHEV_575 = "dostashev-merged-bands-2026-10-13"
EVAND_584 = "evand-compositions-2026-10-13"
EVAND_596 = "evand-fresh-compositions-2026-10-14"

#: The SHA-256 each issue prints for the files it names.
ISSUE_DIGESTS = {
    OSTASHEV_562: {
        "records/n0129.sqpk": (
            "fd79773bd5168dbb72846510b76522dc0e177f38f5e030353116b73608a999c4"
        ),
        "records/n0129.sqcert": (
            "6ee26567f49a700822840807ea97947647bcdbf110e656041c0e2fe970624e72"
        ),
        "records/n0204.sqpk": (
            "64f804cd98f3cfcf113582b14dce0a00d162c527097c4ff89b8ca790f9a60b01"
        ),
        "records/n0204.sqcert": (
            "9d6261e7bbd83ddb8aee29e6f713c403e07d07e3e436f51ec09037b3c241ffa0"
        ),
        "records/n0303.sqpk": (
            "9df683c6a24db53b91fa4ecf9f5bab1bf529a9aba99278574bbaa370dfd8ef59"
        ),
        "records/n0303.sqcert": (
            "f8c22f3c00cf40bab8e6edd33ccd58f99f4837d5ccad717bbb1ef964986c3f58"
        ),
    },
    OSTASHEV_575: {
        "records/n0176.sqpk": (
            "2b79553855e03f613130b6e88ccf788e1df5d0dbaed70e441f77fde3b5facadc"
        ),
        "records/n0176.sqcert": (
            "f70f484dfeb7057fd23c57859eac8d77bc4554e3d6aa6df1425ae5cdd2e9ef39"
        ),
        "records/n0211.sqpk": (
            "0fac3226cd3e2ebbe1465c1fba2d9761e3e70b34dc174775cc0dfd856e0e0628"
        ),
        "records/n0211.sqcert": (
            "7d35edaac371fd7b2a32517bd52dd0fd8b58d9ae9642008112496f80b58bf310"
        ),
        "records/n0241.sqpk": (
            "bf99eee479060a868b8e7d063265a20ccc51bebc7e12cf7af0c6987a869ed950"
        ),
        "records/n0241.sqcert": (
            "8d67da52a9445c38f28f5cea24169bcd3a421c39db581a5a5bf779c0d4cdf962"
        ),
        "records/n0304.sqpk": (
            "534e5679d6253254bfe109db698ff997623272c644946455f5bb631c46de67cc"
        ),
        "records/n0304.sqcert": (
            "b87d0c9df7336872a2e0c26b761a1d7030b8850c2cf385bec43126f62c270c71"
        ),
    },
    EVAND_584: {
        "search/packer/candidates/comp2_n339.cert": (
            "c09a12a5242f7ac759a4ef30c1d64fb813cef4419344c3c9459af30cf2a7801c"
        ),
        "search/packer/candidates/comp2_n364.cert": (
            "f79b2d23b730d3b118b14d7995607410068a6b5b3db6929e2f0cfda8e522bf4a"
        ),
        "search/packer/candidates/comp2_n375.cert": (
            "06438617618f35e202eff4f9d295076e9838df05b76a38ee04d763d9052d097e"
        ),
    },
    EVAND_596: {
        "search/packer/candidates/fresh_n365.cert": (
            "2d03e6bfd6993488adbf5d851d5b77feb0cd9a5dbe722f690932abe096d1e8ed"
        ),
        "search/packer/candidates/fresh_n370.cert": (
            "7cfb9102add6ccce5575176e2012178733db6393f969091d2d5acdb20f31a69b"
        ),
        "search/packer/candidates/fresh_n460.cert": (
            "3b2c3916e21079ba171cead7b7de2d65535e74b4560d48dc1e5c058c3a894d6d"
        ),
    },
}
#: The beyond-horizon sides #584 prints, each its certificate's side rounded up at 12 places.
ISSUE_584 = {339: "18.926898900357", 364: "19.583782203951", 375: "19.882451030482"}
#: The same for #596.
ISSUE_596 = {365: "19.621320343560", 370: "19.767730746255", 460: "21.959969683021"}


def _source(name: str) -> dict[str, Any]:
    record = json.loads(
        (reports.packet_path(name) / "acquisition/sources.json").read_text("utf-8")
    )
    (source,) = record["sources"]
    return source


def _rows(name: str) -> dict[int, dict[str, Any]]:
    claims = reports.check_claims(reports.packet_path(name))["results"]
    return {row["n"]: row for row in claims}


def _others(row: dict[str, Any]) -> dict[str, str]:
    return {other["report"]: other["relation"] for other in row["pending"]}


def test_each_retained_file_is_the_one_its_issue_names() -> None:
    for name, digests in ISSUE_DIGESTS.items():
        archive = reports.REPO / _source(name)["archived_path"]
        for path, digest in digests.items():
            assert hashlib.sha256((archive / path).read_bytes()).hexdigest() == digest


def test_each_ostashev_packet_retains_its_issues_records_and_pins_the_rest() -> None:
    retained = {
        OSTASHEV_562: [129, 176, 204, 303],
        OSTASHEV_575: [176, 211, 241, 304],
    }
    for name, counts in retained.items():
        source = _source(name)
        archive = reports.REPO / source["archived_path"]
        kept = sorted({int(path.name[1:5]) for path in (archive / "records").iterdir()})
        assert kept == counts
        twins = {
            item["path"]: item["identical_to"]
            for item in source["pinned_only"]
            if "identical_to" in item
        }
        prior = f"packing/resources/web/{OSTASHEV_501}/source"
        assert all(twin.startswith(prior) for twin in twins.values())
        assert all(twin.endswith(path) for path, twin in twins.items())
        unchanged = {int(path[9:13]) for path in twins if path.startswith("records/")}
        assert unchanged == ({155, 156, 211} if name == OSTASHEV_562 else {155, 156})
        digest_only = {
            int(PurePosixPath(item["path"]).name[1:5])
            for item in source["pinned_only"]
            if "identical_to" not in item
        }
        assert digest_only == (
            {175, 232, 264} if name == OSTASHEV_562 else {129, 175, 204, 232, 264, 303}
        )


def _header(text: str, label: str) -> str:
    (value,) = [line.split()[2] for line in text.splitlines() if line.startswith(f"# {label}:")]
    return value


def test_each_ostashev_side_is_its_labelled_optimum_dilated_by_its_labelled_delta() -> None:
    """Each side is ``claimed_s`` times ``1 + delta``, both read from its own header.

    The issues say every certificate is dilated by 1 + 1e-60. All are but one: the 304
    header, and its side, say 1 + 1e-59, from a 59-digit optimum.
    """
    deltas = {}
    for name in (OSTASHEV_562, OSTASHEV_575):
        packet = reports.packet_path(name)
        archive = reports.REPO / reports.acquisition(packet)["archived_path"]
        for n, certificate in reports.read_facts(packet).items():
            text = (archive / f"records/n{n:04d}.sqcert").read_text(encoding="utf-8")
            delta = Fraction(_header(text, "delta"))
            assert certificate.side == Fraction(_header(text, "claimed_s")) * (1 + delta)
            deltas[name, n] = delta
    assert {key for key, delta in deltas.items() if delta != Fraction(1, 10**60)} == {
        (OSTASHEV_575, 304)
    }
    assert deltas[OSTASHEV_575, 304] == Fraction(1, 10**59)


def test_the_562_sides_are_below_593_and_its_unrequested_176_is_superseded() -> None:
    """Read at their exact sides, PR 574's refinements are smaller by about 1e-19 at all
    three counts, and #593's are larger (review A1 of #602)."""
    rows = _rows(OSTASHEV_562)
    assert [n for n, row in rows.items() if row["requested"]] == [129, 204, 303]
    for n in (129, 204, 303):
        assert (rows[n]["smallest"], rows[n]["case"]["relation"]) == ("PR #574", "below")
        assert _others(rows[n]) == {
            "#593": "below",
            "PR #574": "above",
            **({"#573": "below"} if n == 303 else {}),
        }
    assert [rows[n]["case"]["result"] for n in (129, 204, 303)] == ["T-146", "T-101", "T-146"]
    # The README's 176 is compared and not replayed: the author's own #575 and Couzo's
    # #561, which started from it, are both smaller.
    assert not rows[176]["replayed"]
    assert rows[176]["case"]["relation"] == "below"
    assert _others(rows[176]) == {
        "#561": "above",
        "#575": "above",
        "#593": "above",
        "PR #574": "above",
        "#586": "above",
    }


def test_the_575_sides_are_below_each_case_and_above_couzos_continuations() -> None:
    rows = _rows(OSTASHEV_575)
    assert all(row["case"]["relation"] == "below" for row in rows.values())
    # At 211 the case is the author's own T-149, a different packing this one replaces.
    assert rows[211]["case"]["result"] == "T-149"
    assert rows[211]["case"]["source_key"] == "[Ostashev records 2026-10-11]"
    for n in (211, 241):
        assert _others(rows[n]) == {
            "#583": "above",
            "#586": "above",
            "#593": "above",
            "PR #574": "below",
        }
        # Read exactly, #593's sides here are #586's (review A1 of #602).
        assert rows[n]["tied"] == ["#586", "#593"]
    assert _others(rows[176])["#561"] == "below"
    assert _others(rows[176])["fe43a64 (#562, not requested)"] == "below"


@pytest.mark.parametrize(("name", "printed"), [(EVAND_584, ISSUE_584), (EVAND_596, ISSUE_596)])
def test_a_beyond_horizon_plan_registers_no_entry_and_one_row_a_count(
    name: str, printed: dict[int, str]
) -> None:
    plan = reports.register_plan(reports.packet_path(name))
    assert "results.yaml" not in plan
    assert plan["evidence.yaml"]["scope"]["n_values"] == list(printed)
    coverage = plan["source-coverage.yaml"]
    (source,) = coverage["sources"]
    assert source["represented_by"][0] == f"resources/web/{name}/README.md"
    assert "no register entry" in source["notes"]
    assert "T-NNN" not in source["notes"] + plan["resources/README.md"]
    assert {row["n"]: row["value"] for row in coverage["beyond_horizon_claims"]} == printed
    claims = coverage_check.load_claims(reports.ROOT / source["claims_record"])
    assert claims == printed


def test_the_584_sides_are_smallest_at_364_and_375_and_couzos_586_at_339() -> None:
    rows = _rows(EVAND_584)
    # At 339 issue 586's certificate is the source register's current row, read as that row.
    assert {n: row["smallest"] for n, row in rows.items()} == {
        339: "couzo-certificates-2026-10-13",
        364: reports.THIS,
        375: reports.THIS,
    }
    assert all(row["case"] is None for row in rows.values())
    assert _others(rows[339]) == {
        "couzo-certificates-2026-10-11": "below",
        "#583": "below",
        "couzo-certificates-2026-10-13": "above",
    }
    assert set(_others(rows[375]).values()) == {"below"}
    # A later import reads these sides exactly, by the packet's source key.
    for key, name in (
        ("[Daniel compositions 2026-10-13]", EVAND_584),
        ("[Daniel fresh compositions 2026-10-14]", EVAND_596),
        ("[Ostashev compositions 2026-10-12]", OSTASHEV_562),
        ("[Ostashev merged bands 2026-10-13]", OSTASHEV_575),
    ):
        for n, row in _rows(name).items():
            assert reports.house_side(key, n) == Fraction(row["exact_side"])


def test_the_596_sides_meet_no_tracked_row_or_other_report() -> None:
    """Nothing the record tracks names 365, 370 or 460; each side is below the grid."""
    rows = _rows(EVAND_596)
    assert list(rows) == list(ISSUE_596)
    for row in rows.values():
        assert (row["case"], row["pending"], row["smallest"]) == (None, [], reports.THIS)
        assert Fraction(row["exact_side"]) < Fraction(row["grid_side"])
    # 365 is s(26) + 14 = 14 + 7/2 + 3/sqrt(2), the issue says, and the certificate's
    # rational side lies above that irrational sum by less than its 1 + 1e-20 scaling.
    side = Fraction(rows[365]["exact_side"])
    above = side - Fraction(35, 2)
    assert above > 0
    assert Fraction(9, 2) < above**2 < Fraction(9, 2) * (1 + Fraction(1, 10**18))
