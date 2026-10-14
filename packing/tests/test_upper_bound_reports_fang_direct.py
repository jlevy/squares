"""Kevin Fang's direct certificates at 078789a: fourteen counts beyond the case corpus.

TheSnakeFang/squarepack-certs added eight direct packings in e646c47 and six in c284cd0,
each a folder ``nNNNN/`` with the certificate in Evan Daniel's text format and in
SQUISH's JSON layout. No issue asked. Every count lies beyond the ``n <= 324`` corpus, so
the declaration requests nothing inside it and the register plan holds beyond-horizon
rows and no register entry. These tests hold what is particular to the packet, and the
general importer's checks on it, reading the retained packet only.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import check_source_coverage as coverage_check
from devtools import evand_exact_certificates as legacy
from devtools import upper_bound_reports as reports
from devtools.retained_data import read_retained_bytes

PACKET = "fang-direct-certificates-2026-10-13"
FIRST = "2026-10-12T19:06:24Z"
SECOND = "2026-10-13T00:05:31Z"
#: Each count's side as the source's README table and the folder's NOTES.md print it,
#: rounded up at 15 places, with the commit that first held the folder.
PRINTED = {
    380: ("19.976775433974195", FIRST),
    381: ("19.976969740405508", FIRST),
    382: ("19.989479729399675", SECOND),
    421: ("20.986150316947159", FIRST),
    422: ("20.988436524095744", SECOND),
    463: ("21.986880406196935", FIRST),
    464: ("21.991709536768996", SECOND),
    507: ("22.997807183348823", FIRST),
    508: ("22.994733849702143", SECOND),
    553: ("23.998811020144984", FIRST),
    601: ("24.998914572427130", FIRST),
    651: ("25.991547815274380", FIRST),
    758: ("27.996346242823117", SECOND),
    814: ("28.999873603982716", SECOND),
}
#: The counts the receipt covers: all fourteen, each kept as its own receipt shard.
REPLAYED = list(PRINTED)
#: When each other report at 380, 381 and 382 reached the record: the standing rows from
#: issue #506, then Miles Gray's #582 and Francisco Couzo's #583 and #586.
REACHED = {
    "couzo-certificates-2026-10-11": "2026-10-11T18:06:50Z",
    "#582": "2026-10-13T11:38:11Z",
    "#583": "2026-10-13T14:11:17Z",
    "#586": "2026-10-13T17:37:01Z",
    # Issue 586's packet, read as the source register's current row at 380 to 382.
    "couzo-certificates-2026-10-13": "2026-10-13T17:37:01Z",
}


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


def test_custody_admits_each_certificate_at_its_printed_side_in_both_formats() -> None:
    declaration = reports.load_declaration(_packet())
    certificates = reports.read_facts(_packet())
    assert declaration["houses"] == []
    assert declaration["requested"] == list(PRINTED)
    assert declaration["replayed"] == REPLAYED
    assert list(certificates) == list(PRINTED)
    for row in declaration["certificates"]:
        n = row["n"]
        offered, committed = PRINTED[n]
        assert (row["offered"], row["first_committed"]) == (offered, committed)
        assert len(certificates[n].poses) == n
        assert legacy.ceiling_decimal(certificates[n].side, 15) == offered
        # read_facts admits a count only where the .cert.json states the same packing.
        assert row.get("same_packing") == [
            {"path": f"n{n:04d}/n{n:04d}.cert.json", "format": "squish-json"}
        ]


def test_the_source_prints_each_side_in_its_table_and_in_the_folders_notes() -> None:
    readme = (_archive() / "README.md").read_text("utf-8")
    for n, (offered, _committed) in PRINTED.items():
        assert f"| `n{n:04d}/` | {n} |" in readme
        assert readme.count(offered) == 1
        notes = (_archive() / f"n{n:04d}/NOTES.md").read_text("utf-8")
        assert notes.startswith(f"n = {n}")
        assert f"S = {offered} (rounded up" in notes


def test_each_folders_own_checksums_match_the_retained_and_pinned_bytes() -> None:
    manifest = {
        line.split("  ", 1)[1].removeprefix("./"): line.split("  ", 1)[0]
        for line in (_packet() / "acquisition/upstream-subtree.sha256")
        .read_text("utf-8")
        .splitlines()
    }
    pinned = {item["path"] for item in _source()["pinned_only"]}
    for n in PRINTED:
        folder = f"n{n:04d}"
        sums = (_archive() / folder / "SHA256SUMS").read_text("utf-8").splitlines()
        assert len(sums) == 7
        for line in sums:
            digest, name = line.split("  ", 1)
            path = f"{folder}/{name}"
            assert manifest[path] == digest
            if path in pinned:
                assert name.endswith((".svg", ".txt"))
                continue
            data = read_retained_bytes(_archive() / path)
            assert hashlib.sha256(data).hexdigest() == digest


def test_the_scope_leaves_the_earlier_folders_and_the_theorem_bundle_to_other_packets() -> None:
    scope = _source()["subtree_scope"]
    assert not {"n0308", "n0343", "n0344"} & set(scope)
    assert not [item for item in scope if item.split("/")[0] in {"theorem", "composites"}]
    assert not [item for item in scope if item.split("/")[0] in {"rectangles", "third_party"}]
    assert "tools/glue.py" not in scope
    twins = {item["path"]: item.get("identical_to") for item in _source()["pinned_only"]}
    assert twins["tools/verify_cert_daniel.py"] == (
        "packing/resources/web/evand-new-arrangements-2026-10-07/source/s12/search/exact/"
        "verify_cert.py"
    )


def test_the_claims_name_couzos_later_reports_smallest_at_380_381_and_382() -> None:
    rows = _rows()
    assert all(row["case"] is None and row["requested"] for row in rows.values())
    assert [n for n, row in rows.items() if row["replayed"]] == REPLAYED
    # Issue 586's certificates are the source register's current rows at 380 to 382, and at
    # 381 issue 583's is the same certificate; each is read as that row (review A1 of #602).
    current = "couzo-certificates-2026-10-13"
    assert {n: row["smallest"] for n, row in rows.items() if n <= 382} == dict.fromkeys(
        (380, 381, 382), current
    )
    relations = {n: {p["report"]: p["relation"] for p in rows[n]["pending"]} for n in rows}
    assert relations[380] == {
        "couzo-certificates-2026-10-11": "below",
        "#583": "above",
        current: "above",
    }
    assert relations[381] == {
        "couzo-certificates-2026-10-11": "below",
        "#582": "below",
        current: "above",
    }
    assert relations[382] == {"#583": "above", current: "above"}
    # Nothing the record tracks, and no other report, names the other eleven counts.
    for n in set(rows) - {380, 381, 382}:
        assert (rows[n]["pending"], rows[n]["smallest"]) == ([], reports.THIS)
    for row in rows.values():
        assert Fraction(row["exact_side"]) < Fraction(row["grid_side"])


def test_in_report_order_each_certificate_at_380_to_382_is_below_every_earlier_report() -> None:
    """A watched repository's result is reported at its first commit (think-abi1).

    Each certificate is below every report that reached the record before it, so it is
    recorded; at 381 Miles Gray's later #582 is above it, so it is not recorded, and
    Couzo's #583 and #586 are below it, so each is recorded after it.
    """
    rows = _rows()
    for n in (380, 381, 382):
        committed = rows[n]["first_committed"]
        earlier = [p for p in rows[n]["pending"] if REACHED[p["report"]] < committed]
        later = [p for p in rows[n]["pending"] if REACHED[p["report"]] > committed]
        assert len(earlier) + len(later) == len(rows[n]["pending"])
        assert all(p["relation"] == "below" for p in earlier)
        assert {p["report"] for p in earlier} == (
            set() if n == 382 else {"couzo-certificates-2026-10-11"}
        )
        assert {p["report"] for p in later if p["relation"] == "above"} == (
            {"couzo-certificates-2026-10-13"}
            if n == 381
            else {"#583", "couzo-certificates-2026-10-13"}
        )


def test_the_508_side_bounds_s507_below_the_507_certificate() -> None:
    """s(507) <= s(508): dropping one square of the 508 packing packs 507 squares.

    The consequence settles no case and registers nothing of its own (result-import.md,
    stage 1); the 507 row keeps its own certificate's side.
    """
    sides = {n: certificate.side for n, certificate in reports.read_facts(_packet()).items()}
    gap = sides[507] - sides[508]
    assert Fraction(307, 10**5) < gap < Fraction(308, 10**5)
    others = [n for n in sides if n + 1 in sides and sides[n + 1] < sides[n]]
    assert others == [507]


def test_the_plan_registers_no_entry_and_one_beyond_horizon_row_a_count() -> None:
    plan = reports.register_plan(_packet())
    assert "results.yaml" not in plan
    assert plan["evidence.yaml"]["scope"]["n_values"] == list(PRINTED)
    assert plan["evidence.yaml"]["replay_status"] == "not-attempted"
    coverage = plan["source-coverage.yaml"]
    (source,) = coverage["sources"]
    assert source["represented_by"][0] == f"resources/web/{PACKET}/README.md"
    assert source["source_date"] == "2026-10-13"
    assert "T-NNN" not in source["notes"] + plan["resources/README.md"]
    printed = {n: offered for n, (offered, _committed) in PRINTED.items()}
    assert {row["n"]: row["value"] for row in coverage["beyond_horizon_claims"]} == printed
    assert {row["bead"] for row in coverage["beyond_horizon_claims"]} == {"think-7bw3"}
    assert coverage_check.load_claims(reports.ROOT / source["claims_record"]) == printed
    assert plan["bibliography.yaml"]["dated"] == "2026-10-13"


def test_the_receipt_admits_every_job_of_every_count_on_both_routes() -> None:
    packet = _packet()
    positives = reports.check_certification(packet)
    assert list(positives) == REPLAYED
    # The whole would exceed the kernel's evidence ceiling, so each count has its shard.
    assert not (packet / reports.RECEIPT).exists()
    assert all((packet / reports.shard(n)).is_file() for n in REPLAYED)
    _declaration, facts = reports.replayed_facts(packet)
    parts = reports.receipt_parts(packet, facts)
    record = {"cases": [row for part, _ in parts for row in part["cases"]]}
    assert [(row["n"], row["control"]) for row in record["cases"]] == [
        (n, control) for n in REPLAYED for control in reports.JOBS
    ]
    summary = reports.receipt_summary(record)
    assert summary["pair_decisions"] == sum(3 * n * (n - 1) for n in REPLAYED)
    for margins in reports.margins(positives).values():
        for field in ("containment_clearance", "best_pair_gap"):
            assert margins[f"exact_verify_{field}"] == margins[f"independent_{field}"]
        assert Fraction(margins["exact_verify_best_pair_gap"]) > 0
        assert Fraction(margins["exact_verify_containment_clearance"]) > 0
