"""Francisco Couzo's registration witnesses at 43ac7d2: issue #607's 23 certificates.

The issue asks for 14 campaign bounds of the author's own, one inside the case corpus at
237 and 13 beyond it, seven of Kevin Fang's composites, which the author replayed and
credits to Fang, and two precision refinements beyond the corpus. The records lane of 15
October declares requested the 16 counts the per-count rule records as the author's: the
seven composites tie Fang's earlier rows, so they stay in the claim record as replayed
certificates and out of the beyond-horizon record, whose rows are this source's. These
tests hold what is particular to the packet, and the general importer's checks on it,
reading the retained packets only.
"""

from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import check_source_coverage as coverage_check
from devtools import check_standing
from devtools import evand_exact_certificates as legacy
from devtools import upper_bound_reports as reports
from devtools.retained_data import read_retained_bytes

PACKET = "couzo-certificates-2026-10-14"
FANG = "fang-excess-theorem-2026-10-13"
#: The first commit holding the 23 certificates, which dates every claim.
FIRST = "2026-10-14T19:15:09Z"
#: Each count's side as the issue prints it, rounded up at 12 places.
PRINTED = {
    237: "15.902603638284",
    339: "18.915818555470",
    342: "18.964706723173",
    382: "19.987621154241",
    409: "20.767428349966",
    419: "20.959997582079",
    450: "21.767428350587",
    461: "21.973183753375",
    542: "23.828427124774",
    552: "23.968034845503",
    599: "24.968034846127",
    648: "25.968034846328",
    649: "25.976974088403",
    651: "25.984515068279",
    703: "26.999256308447",
    757: "27.991000865994",
    804: "28.920398747577",
    812: "28.988287236851",
    930: "30.988287236851",
    931: "30.994048655032",
    992: "31.997220361783",
    993: "31.991327887692",
    994: "31.999256308447",
}
#: Kevin Fang's composite table rows the seven composite certificates are, by count.
COMPOSITES = {
    703: "L1_n27_703_r17x16_n0257+n-110",
    812: "L1_n29_812_r21x20_n0401+n-71",
    930: "L1_n31_930_r21x20_n0401+n-109",
    931: "L1_n31_931_r19x18_n0325+n-156",
    992: "L1_n32_992_r22x21_n0442+n-109",
    993: "L1_n32_993_r21x20_n0401+n-132",
    994: "L1_n32_994_r17x16_n0257+n-241",
}
#: The two of them Fang ships, as the files the excess-theorem packet pins by digest.
SHIPPED = {703: "composites/n027_j1_703.cert", 994: "composites/n032_j2_994.cert"}
#: The author's own parent commit, whose certificates at these counts no issue reports,
#: labelled by the source row that records them (T-188's).
PARENT = "couzo-verified-bounds-2026-10-14"
#: When each other report at a count reached the record: an issue or pull request at its
#: filing, a register entry at the issue it registered, a source-register row at the report
#: or commit it holds, and a watched repository's result at its first commit.
REACHED = {
    # T-056's 237: the source commit holding its printed side (2083b05), before #227's import.
    "T-056": "2026-09-26T22:21:57Z",
    "T-098 (#375)": "2026-10-05T21:40:49Z",
    "T-115 (#401)": "2026-10-07T02:49:31Z",
    "T-127 (#438)": "2026-10-08T03:08:01Z",
    "couzo-extended-range-reports-2026-10-08": "2026-10-08T15:17:05Z",
    "#470": "2026-10-09T07:11:15Z",
    "#476": "2026-10-09T20:38:53Z",
    "T-134 (#476)": "2026-10-09T20:38:53Z",
    "T-136 (#481)": "2026-10-09T21:59:29Z",
    # T-140's 237, the house until #614 adopted T-183 there.
    "#488": "2026-10-10T14:08:32Z",
    "#505": "2026-10-11T14:24:18Z",
    "#506": "2026-10-11T18:06:50Z",
    "#561": "2026-10-12T18:55:03Z",
    "#573": "2026-10-12T23:58:50Z",
    # Fang's direct certificates: e646c47 at 651, and c284cd0, this time, at 382.
    "fang-direct-certificates-2026-10-13": "2026-10-13T00:05:31Z",
    "PR #574": "2026-10-13T00:13:11Z",
    "#583": "2026-10-13T14:11:17Z",
    "#584": "2026-10-13T14:31:16Z",
    "#586": "2026-10-13T17:37:01Z",
    "couzo-certificates-2026-10-13": "2026-10-13T17:37:01Z",
    "#593": "2026-10-14T01:40:32Z",
    PARENT: "2026-10-14T17:45:39Z",
}
#: Fang's composite table, first committed in bef5c42 and unchanged at 078789a.
COMPOSITES_COMMITTED = "2026-10-12T19:13:41Z"
#: Fang's theorem certificates, held at 078789a, committed then or earlier.
THEOREM_COMMITTED = "2026-10-13T06:57:58Z"


def _packet() -> Path:
    return reports.packet_path(PACKET)


def _source() -> dict[str, Any]:
    record = json.loads((_packet() / "acquisition/sources.json").read_text("utf-8"))
    (source,) = record["sources"]
    return source


def _archive() -> Path:
    return reports.REPO / _source()["archived_path"]


def _rows() -> dict[int, dict[str, Any]]:
    return {row["n"]: row for row in reports.check_claims(_packet())["results"]}


def _reached(report: str) -> str:
    if report.startswith("Fang theorem/"):
        return THEOREM_COMMITTED
    if report.startswith("Fang "):
        return COMPOSITES_COMMITTED
    return REACHED[report]


def test_custody_admits_each_certificate_at_its_printed_side() -> None:
    declaration = reports.load_declaration(_packet())
    certificates = reports.read_facts(_packet())
    assert [house["n"] for house in declaration["houses"]] == [237]
    assert declaration["replayed"] == list(PRINTED)
    assert declaration["requested"] == [n for n in PRINTED if n not in COMPOSITES]
    assert list(certificates) == list(PRINTED)
    for row in declaration["certificates"]:
        n = row["n"]
        assert row["path"] == f"submissions/2026-10-14/certificates/n{n}.cert"
        assert (row["offered"], row["first_committed"]) == (PRINTED[n], FIRST)
        assert len(certificates[n].poses) == n
        assert legacy.ceiling_decimal(certificates[n].side, 12) == PRINTED[n]


def test_the_scope_is_the_submission_and_retains_only_its_certificates() -> None:
    source = _source()
    assert source["subtree_scope"] == [
        "README.md",
        "submissions/2026-10-14",
        "upper_bounds.json",
    ]
    retained = sorted(
        path.relative_to(_archive()).as_posix()
        for path in _archive().rglob("*")
        if path.is_file()
    )
    assert retained == [
        f"submissions/2026-10-14/certificates/n{n}.cert" for n in sorted(PRINTED, key=str)
    ]
    pinned = {item["path"] for item in source["pinned_only"]}
    assert len(pinned) == 29
    assert {"README.md", "upper_bounds.json", "submissions/2026-10-14/manifest.json"} <= pinned


def test_the_seven_composites_are_fangs_certificates_byte_for_byte() -> None:
    """Each has the SHA-256 Fang's table lists for its row, his smallest at its count."""
    table = reports.REPO / "packing/resources/web" / FANG / "source/composites/table.csv"
    with table.open(encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    fang = json.loads(
        (reports.packet_path(FANG) / "acquisition/sources.json").read_text("utf-8")
    )
    pinned = {item["path"]: item["sha256"] for item in fang["sources"][0]["pinned_only"]}
    for n, ident in COMPOSITES.items():
        data = read_retained_bytes(
            _archive() / f"submissions/2026-10-14/certificates/n{n}.cert"
        )
        digest = hashlib.sha256(data).hexdigest()
        (row,) = [row for row in rows if row["id"] == ident]
        assert row["sha256"] == digest
        smallest = min(
            (r for r in rows if r["count"] == str(n)),
            key=lambda r: Fraction(r["side_rounded_up_15"]),
        )
        assert smallest["id"] == ident
        assert (row["status"] == "shipped") is (n in SHIPPED)
        if n in SHIPPED:
            assert pinned[SHIPPED[n]] == digest
    # The 16 campaign and precision certificates are the author's own, none Fang's.
    digests = {row["sha256"] for row in rows}
    for n in set(PRINTED) - set(COMPOSITES):
        data = read_retained_bytes(
            _archive() / f"submissions/2026-10-14/certificates/n{n}.cert"
        )
        assert hashlib.sha256(data).hexdigest() not in digests


def test_the_claims_put_237_below_t183_and_every_other_report() -> None:
    """#614 adopted #593's certificate (T-183) as the house at 237, so the case is #593's
    and T-140 (#488), the house before it, is an earlier report (PR #627 review A1)."""
    row = _rows()[237]
    assert row["case"]["result"] == "T-183"
    assert row["case"]["relation"] == "below"
    assert row["smallest"] == reports.THIS
    relations = {p["report"]: p["relation"] for p in row["pending"]}
    assert set(relations.values()) == {"below"}
    assert "#593" not in relations
    (t140,) = [p for p in row["pending"] if p.get("result") == "T-140"]
    assert t140["report"] == "#488"
    gap = Fraction(row["case"]["difference"])
    assert Fraction(1014, 10**7) < gap < Fraction(1015, 10**7)
    assert min(Fraction(p["difference"]) for p in row["pending"]) > gap


def test_beyond_the_corpus_the_campaign_bounds_are_smallest_and_the_composites_tie() -> None:
    rows = _rows()
    for n, row in rows.items():
        if n <= reports.HORIZON:
            continue
        assert row["case"] is None
        assert (row["requested"], row["replayed"]) == (n not in COMPOSITES, True)
        assert Fraction(row["exact_side"]) < Fraction(row["grid_side"])
        if n in COMPOSITES:
            # Fang's print is at 15 places; the digests, not the prints, decide the tie.
            (fang,) = [p for p in row["pending"] if COMPOSITES[n] in p["report"]]
            assert fang["relation"] == "undecided"
            assert abs(Fraction(fang["difference"])) < Fraction(1, 10**15)
            assert row["smallest"] is None
            assert row["undecided_among"] == [reports.THIS, fang["report"]]
            others = [p for p in row["pending"] if p is not fang]
            assert all(p["relation"] == "below" for p in others)
        else:
            assert row["smallest"] == reports.THIS
            assert {p["relation"] for p in row["pending"]} == {"below"}
    # The author's own 487b058 certificate is the nearest earlier report at 16 counts.
    parent = {
        n: Fraction(p["difference"])
        for n, row in rows.items()
        for p in row["pending"]
        if p["report"] == PARENT
    }
    assert sorted(parent) == [
        339,
        382,
        409,
        419,
        450,
        461,
        542,
        552,
        599,
        648,
        649,
        651,
        757,
        804,
        812,
        930,
    ]
    assert Fraction(1, 10**9) < parent[542] < Fraction(2, 10**9)
    assert Fraction(1, 10**7) < parent[382] < Fraction(2, 10**7)


def test_in_report_order_16_counts_are_recorded_and_the_7_composites_are_fangs() -> None:
    """A watched repository's result is reported at its first commit (think-abi1).

    Every report at a campaign count reached the record before 43ac7d2 and is above its
    certificate, so it is recorded. At each composite count the certificate is the file
    Fang's row names, published two days earlier: a tie the earlier holder keeps.
    """
    rows = _rows()
    for n, row in rows.items():
        assert row["first_committed"] == FIRST
        assert all(_reached(p["report"]) < FIRST for p in row["pending"])
        recorded = all(p["relation"] == "below" for p in row["pending"])
        assert recorded is (n not in COMPOSITES)


def test_the_beyond_horizon_record_holds_every_requested_count_past_324() -> None:
    claims = coverage_check.load_claims(_packet() / reports.BEYOND)
    assert claims == {
        n: side for n, side in PRINTED.items() if n > reports.HORIZON and n not in COMPOSITES
    }


def test_the_receipt_admits_every_job_of_every_count_on_both_routes() -> None:
    packet = _packet()
    positives = reports.check_certification(packet)
    assert list(positives) == list(PRINTED)
    _declaration, facts = reports.replayed_facts(packet)
    parts = reports.receipt_parts(packet, facts)
    record = {"cases": [row for part, _ in parts for row in part["cases"]]}
    assert [(row["n"], row["control"]) for row in record["cases"]] == [
        (n, control) for n in PRINTED for control in reports.JOBS
    ]
    summary = reports.receipt_summary(record)
    assert summary["pair_decisions"] == sum(3 * n * (n - 1) for n in PRINTED)
    for margins in reports.margins(positives).values():
        for field in ("containment_clearance", "best_pair_gap"):
            assert margins[f"exact_verify_{field}"] == margins[f"independent_{field}"]
        assert Fraction(margins["exact_verify_best_pair_gap"]) > 0
        assert Fraction(margins["exact_verify_containment_clearance"]) > 0


def test_the_plan_states_the_237_bound_as_check_standing_reads_it() -> None:
    plan = reports.register_plan(_packet())
    result = plan["results.yaml"]
    assert result["scope"]["n_values"] == [237]
    assert result["attribution"]["published"] == "2026-10-14"
    stated = check_standing.statements(" ".join(result["claim"].split()), [237])
    assert {n: bound.value for (n, _), bound in stated.items()} == {
        237: Fraction(_rows()[237]["exact_side"])
    }
    coverage = plan["source-coverage.yaml"]
    assert [row["n"] for row in coverage["beyond_horizon_claims"]] == [
        n for n in PRINTED if n > reports.HORIZON and n not in COMPOSITES
    ]
    assert plan["bibliography.yaml"]["dated"] == "2026-10-14"
    assert "T-NNN" not in coverage["sources"][0]["notes"].replace("T-NNN records", "")
