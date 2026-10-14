"""replay4d's source hashes re-derive from the packets, and the calibration inputs bind.

``devtools.audit_wand125_closed_form`` reads three packets of wand125's closed form
through their acquisition records. These tests check its hash rule on a known answer,
the covered files it reads from each revision's ``main.rs``, the retained receipt
against a fresh derivation, and the parsers and control writer the calibration uses.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from devtools import audit_wand125_closed_form as audit


def test_source_hash_is_names_nul_lengths_and_bytes() -> None:
    files = [("a.rs", b"xy"), ("../b", b"")]
    blob = b"a.rs\0" + (2).to_bytes(8, "big") + b"xy" + b"../b\0" + (0).to_bytes(8, "big")
    assert audit.source_hash(files) == hashlib.sha256(blob).hexdigest()
    assert audit.source_hash(reversed(files)) != audit.source_hash(files)


@pytest.mark.parametrize(
    ("revision", "count", "covers_b3d_sort"),
    [
        (audit.REVISIONS[0], 10, False),
        (audit.REVISIONS[1], 10, False),
        (audit.REVISIONS[2], 11, True),
    ],
)
def test_each_revisions_main_rs_names_its_covered_files(
    revision: audit.Revision,
    count: int,
    covers_b3d_sort: bool,  # noqa: FBT001
) -> None:
    tree = audit.PacketTree(audit.WEB / revision.packet)
    order = audit.source_order(tree.read(audit.MAIN_RS).decode())
    assert len(order) == count
    assert order[0] == ("Cargo.toml", f"{audit.CHECKER}/replay4d/Cargo.toml")
    assert order[3] == ("src/main.rs", audit.MAIN_RS)
    assert (audit.B3D_SORT in {path for _, path in order}) is covers_b3d_sort


def test_source_order_refuses_a_name_that_is_not_the_included_file() -> None:
    text = (
        'fn source_hash()->String { ("Cargo.toml",include_bytes!("../../Cargo.toml")) '
        "sha256::digest(&bytes) }"
    )
    with pytest.raises(ValueError, match="different files"):
        audit.source_order(text)


def test_recomputed_hashes_equal_the_stated_and_b3d_sort_enters_at_0_1_1() -> None:
    receipt = audit.hashes_receipt()
    assert receipt["all_equal_to_stated"]
    assert [r["source_sha256"][:8] for r in receipt["revisions"]] == [
        "92002e0e",
        "92002e0e",
        "f8cafeab",
    ]
    b3d_sort, b3d = receipt["controls"]
    assert [b3d_sort[c]["hash_changes"] for c in ("9a28a84", "746e2c5", "1c661b7")] == [
        False,
        False,
        True,
    ]
    assert all(b3d[c]["hash_changes"] for c in ("9a28a84", "746e2c5", "1c661b7"))
    assert all(row["byte_identical"] for row in receipt["unchanged_files"])
    assert receipt["b3d_sort_equals_stated"]
    assert receipt["structure_receipt"]["fields_that_differ"] == ["validate_family_sha256"]
    names = [r["structure_receipt_names_published_script"] for r in receipt["revisions"]]
    assert names == [False, False, True]


def test_the_retained_hashes_receipt_is_current() -> None:
    text = json.dumps(audit.hashes_receipt(), indent=1, ensure_ascii=False) + "\n"
    assert audit.HASHES_RECEIPT.read_text(encoding="utf-8") == text


def test_a_path_outside_the_packets_scope_is_refused() -> None:
    tree = audit.PacketTree(audit.PACKET_1C661B7)
    with pytest.raises(KeyError, match="not in the manifest"):
        tree.read("problems/closed-form/no-such-file.rs")


def test_region_plan_names_the_smallest_record() -> None:
    plan = audit.region_plan(26, "top")
    assert (plan["roots"], plan["leaves"], plan["source_cpu_hours"]) == (4158, 32828, 0.27)
    assert plan["bounds"] == ["167/100", "301/100", "272/100", "38/10"]
    assert plan["record_sha256"].startswith("c3a19d70")


def test_parse_receipt_log_reads_header_footer_and_last_line() -> None:
    text = (
        "# command: ./replay4d f.json r.rec\n# cwd: run\n# python3: not used by this command\n"
        "# host: 4 cores; load 1.00 2.00 3.00; started 2026-10-14T17:00:00Z\n"
        "roots 2 leaf kinds {}\ncpu 1.0s wall 1.0s\nREPLAY OK\n"
        "# finished 2026-10-14T17:00:01Z; exit 0; wall 1.250 s; CPU 1.1 s "
        "(user 1.000 + sys 0.125); load 1.00 2.00 3.00\n"
    )
    log = audit.parse_receipt_log(text)
    assert (log["exit"], log["wall_seconds"], log["cpu_seconds"]) == (0, 1.25, 1.125)
    assert (log["cores"], log["last_line"]) == (4, "REPLAY OK")
    with pytest.raises(ValueError, match="not a replay_receipt log"):
        audit.parse_receipt_log("REPLAY OK\n")


def test_write_controls_truncates_and_relabels_one_leaf(tmp_path: Path) -> None:
    box = ["0", "1", "0", "1", "0", "1", "0", "1"]
    lines = [
        {"root": box, "leaves": [[box, "CORE"], [box, "B3D"]], "uncert": []},
        {"root": box, "leaves": [[box, "EDGE"]], "uncert": []},
        {"root": box, "leaves": [[box, "CORE"]], "uncert": []},
    ]
    record = tmp_path / "top.rec"
    record.write_text("".join(json.dumps(line) + "\n" for line in lines))
    manifest = audit.write_controls(record, tmp_path / "out", roots=2)
    assert (tmp_path / "out/truncated.rec").read_text().count("\n") == 2
    leaves = [json.loads(x) for x in (tmp_path / "out/leaves.jsonl").read_text().splitlines()]
    relabelled = [
        json.loads(x) for x in (tmp_path / "out/relabelled.jsonl").read_text().splitlines()
    ]
    assert [leaf[1] for leaf in leaves] == ["CORE", "B3D", "EDGE"]
    assert [leaf[1] for leaf in relabelled] == ["CORE", "CORE", "EDGE"]
    assert manifest["relabelled"] == {
        "leaf": 1,
        "from": "B3D",
        "to": "CORE",
        "note": "the same leaves with this one relabelled, run with --leaves",
    }


def test_binary_digests_are_read_from_a_sha256sum_receipt(tmp_path: Path) -> None:
    log = tmp_path / "binaries.log"
    log.write_text(
        "# command: sha256sum replay4d-0.1.0\n"
        + "a" * 64
        + "  replay4d-0.1.0\nnot a digest line\n"
    )
    assert audit.binary_digests(log) == {"replay4d-0.1.0": "a" * 64}


def test_the_retained_calibration_receipt_is_current() -> None:
    receipt = audit.calibration_receipt()
    text = json.dumps(receipt, indent=1, ensure_ascii=False) + "\n"
    assert audit.CALIBRATION_RECEIPT.read_text(encoding="utf-8") == text
    assert receipt["all_as_expected"]
    timed = [run for run in receipt["runs"] if "plan" in run]
    assert [(run["plan"]["interval"], run["plan"]["region"]) for run in timed] == [
        (26, "top"),
        (14, "top"),
    ]
    assert all(all(run["binds"].values()) for run in timed)
    tests = [build["tests"] for build in receipt["builds"].values() if "tests" in build]
    assert tests == [{"passed": 28, "failed": 0, "all_ok": True}] * 2
    hashes = {
        run["summary"]["version"]: run["summary"]["source_sha256"] for run in receipt["runs"]
    }
    assert hashes["0.1.0"].startswith("92002e0e")
    assert hashes["0.1.1"].startswith("f8cafeab")
