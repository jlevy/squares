"""Controls for Hosono's point-only s(21), s(45) and mixed-rectangle s(50) certificates.

The packet under ``resources/web/wand125-point-and-mixed-2026-09-28/`` holds the source's
bytes at ``39d8ecc`` and this repository's replay receipts. These tests are the fast part
that has to stay true: every retained file is the pinned upstream file, the exact audit
recomputes to the receipt, each measure is nonnegative with the stated exact total below
its count, the point measures are exactly D4-invariant, and the n = 50 sides exceed
Green's reported bound. Coverage is not decided here; it is the source checkers' sweep,
replayed in the packet's receipts.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import audit_wand125_point_and_mixed as audit
from devtools.retained_data import candidates, check_packet, read_retained_bytes


@pytest.fixture(scope="module")
def exact() -> dict:
    return audit.exact_audit()


def test_exact_audit_recomputes_to_the_receipt(exact: dict) -> None:
    assert audit.EXACT_RECEIPT.read_text(encoding="utf-8") == json.dumps(exact, indent=2) + "\n"


def test_every_retained_file_is_the_pinned_upstream_file(exact: dict) -> None:
    record = json.loads(audit.MANIFEST.read_text())["sources"][0]
    assert record["source_commit"] == audit.REVISION
    assert exact["provenance"]["retained_files"] == record["retained_file_count"] == 64
    assert exact["provenance"]["subtree_files"] == record["subtree_file_count"] == 517


def test_compressed_files_match_their_table_rows() -> None:
    assert check_packet(audit.PACKET) == []
    assert candidates(audit.PACKET) == []


def test_the_three_claims_carry_their_exact_data(exact: dict) -> None:
    assert Fraction(exact["n45"]["total"]) == Fraction(12666371418707823, 2**48) < 45
    assert exact["n45"]["distinct_points"] == 12645
    assert exact["n21"]["strict_gap"] == "999979/125000000000"
    assert exact["n21"]["positive_entries"] == 4520
    assert {name: row["side"] for name, row in exact["n50"].items()} == {
        "L740": "37/5",
        "L735": "147/20",
        "L7318": "3659/500",
    }
    assert all(row["total_mass"] == "4999999/100000" for row in exact["n50"].values())
    assert exact["n50"]["L740"]["recorded_minimum_at"] == "150"


def _swap_one_weight(data: bytes) -> bytes:
    lines = data.decode().splitlines()
    x, y, w = lines[5].split()
    lines[5] = f"{x} {y} {int(w) + 1}"
    return ("\n".join(lines) + "\n").encode()


def test_a_changed_n45_weight_is_refused() -> None:
    data = read_retained_bytes(audit.SOURCE / audit.N45 / "cover.txt")
    provenance = json.loads(read_retained_bytes(audit.SOURCE / audit.N45 / "provenance.json"))
    with pytest.raises(ValueError, match="SHA-256"):
        audit.n45_cover(_swap_one_weight(data), provenance)


def test_green_comparison_is_exact() -> None:
    low, high = audit.green_bounds()
    assert low < high < low + Fraction(1, 10**29)
    assert audit.exceeds_green(high)
    assert not audit.exceeds_green(low)
    assert audit.exceeds_green(Fraction(3659, 500))
    assert not audit.exceeds_green(Fraction(7317, 1000))


def _write_run(run_dir: Path, *, uncertified: int) -> None:
    run_dir.mkdir()
    rows = [
        f"ROOT {k} pass 0 root r{k} boxes 2 cert 1 empty 0 "
        f"uncert {uncertified if k == 3 else 0} maxdepth 1 capped 0 ms 1"
        for k in range(4)
    ]
    (run_dir / "roots.log").write_text("\n".join(rows) + "\n", encoding="ascii")
    (run_dir / "run.log").write_text("VERIFIED-D4: toy\n", encoding="utf-8")


def test_n45_comparison_flags_an_uncertified_root(tmp_path: Path) -> None:
    reference = {"roots": 4, "uncertified": 0, "capped": 0, "boxes": 8, "max_depth": 1}
    _write_run(tmp_path / "good", uncertified=0)
    _write_run(tmp_path / "bad", uncertified=1)
    good = audit.n45_compare(tmp_path / "good", {"reference_run": reference})
    bad = audit.n45_compare(tmp_path / "bad", {"reference_run": reference})
    assert good["status"] == "MATCHES_SOURCE_REFERENCE"
    assert bad["status"] == "DIFFERS"
    assert not bad["agreement"]["uncertified"]


def test_n45_receipt_recomputes_from_the_retained_run_logs() -> None:
    receipts = audit.PACKET / "receipts" / "n45"
    provenance = json.loads(read_retained_bytes(audit.SOURCE / audit.N45 / "provenance.json"))
    recorded = json.loads((receipts / "comparison.json").read_text())
    assert audit.n45_compare(receipts, provenance) == recorded
    assert recorded["status"] == "MATCHES_SOURCE_REFERENCE"
    assert recorded["replay"]["boxes"] == 1295460


def test_d4_expansion_preserves_mass_and_closes_under_the_group() -> None:
    side = Fraction(7)
    item = (Fraction(1), Fraction(2), Fraction(3, 2), Fraction(4), Fraction(5, 3))
    images = audit.d4_images(side, [item])
    assert len(images) == 8
    assert sum(rho * (v - u) * (z - w) for u, w, v, z, rho in images) == item[4]
    corners = {(u, w, v, z) for u, w, v, z, _ in images}
    assert {(side - v, w, side - u, z) for u, w, v, z in corners} == corners
    assert {(w, u, z, v) for u, w, v, z in corners} == corners


def test_an_interval_must_enclose_its_datum() -> None:
    point = f"{(0.1).hex()} {(0.1).hex()}"
    assert audit.encloses(point, Fraction(0.1))
    assert not audit.encloses(point, Fraction(1, 10))
    wider = "0x1.9999999999999p-4 0x1.999999999999ap-4"
    assert audit.encloses(wider, Fraction(1, 10))


def test_n21_finished_stages_reproduce_every_proof_file_of_the_m1_run() -> None:
    record = json.loads((audit.PACKET / "receipts/n21/stage_comparison.json").read_text())
    for stage, parents in (("root", 5000), ("sieve", 8758)):
        row = record["stages"][stage]
        assert row["identical"] == parents
        assert row["files_here"] == row["files_m1"] == parents + 4
        assert not row["only_here"]
        assert not row["only_m1"]
        assert row["differing"] == [
            f"{stage}/{name}"
            for name in ("inputs.json", "portable-reads.json", "progress.json", "result.json")
        ]


def test_n21_complete_replay_matches_the_m1_record_output_for_output() -> None:
    receipts = audit.PACKET / "receipts" / "n21"
    recorded = json.loads((receipts / "comparison.json").read_text())
    assert recorded["status"] == "MATCHES_SOURCE_M1_RECORD"
    assert all(recorded["agreement"].values())
    outputs = recorded["outputs_against_m1"]
    assert outputs["outputs_here"] == outputs["outputs_m1"] == 45446
    assert outputs["identical"] == 45436
    assert not outputs["only_here"]
    assert not outputs["only_m1"]
    assert outputs["differing_names"] == [
        "inputs.json",
        "portable-reads.json",
        "progress.json",
        "result.json",
    ]
    # The run's linkage.json is not retained, so its digest is the one result.json states.
    fresh = audit.n21_compare(receipts)
    linkage = json.loads((receipts / "result.json").read_text())["linkage_sha256"]
    assert fresh["agreement"] == recorded["agreement"]
    assert fresh["reference"] == recorded["reference"]
    assert fresh["replay"] | {"linkage_sha256": linkage} == recorded["replay"]


def test_n21_collect_takes_a_receipts_path_relative_to_the_working_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    out = tmp_path / "out"
    out.mkdir()
    (out / "result.json").write_text("{}")
    (out / "run-inputs.json").write_text("{}")
    exit_record = {"stage": "root", "shard": None, "exit_code": 0, "seconds": 1}
    (out / "root-exit.json").write_text(json.dumps(exit_record))
    (out / "root.log").write_text("".join(f"{k}\n" for k in range(audit.LINE_THRESHOLD + 1)))
    monkeypatch.setattr(audit, "PACKET", tmp_path / "packet")
    monkeypatch.chdir(tmp_path)
    result = audit.n21_collect(out, Path("packet/receipts/n21"), None)
    assert result["status"] == "DIFFERS"
    stored = ["result.json", "run-inputs.json", "root-exit.json", "root.log.gz"]
    assert result["stored"] == stored
    row = result["compressed_file_rows"][0]
    assert row.startswith("| `receipts/n21/root.log.gz` | receipt |")


def test_n50_complete_replay_returns_every_shipped_record() -> None:
    full = audit.PACKET / "receipts" / "n50" / "full"
    retained = audit.SOURCE / audit.N50["L740"] / "certificate.json"
    shipped = json.loads(read_retained_bytes(retained))
    fresh_bytes = read_retained_bytes(full / "proof" / "certificate.json")
    fresh = json.loads(fresh_bytes)
    assert fresh["status"] == "ALL_ANGLES_VERIFIED_AND_REPLAYED"
    assert fresh == shipped
    progress = json.loads((full / "proof" / "replay-progress.json").read_text())
    assert progress == {"done": audit.N50_LAST + 1, "total": audit.N50_LAST + 1}
    axis = json.loads((full / "proof" / "axis" / "replayed.json").read_text())
    assert axis == shipped["results"]["0"]
    for index in range(1, audit.N50_LAST + 1):
        replayed = full / "proof" / f"net{index:03}" / "replayed.json"
        assert json.loads(replayed.read_text()) == shipped["results"][str(index)]
    recorded = json.loads((full / "compare.json").read_text())
    assert recorded["status"] == "FULL_REPLAY_MATCHES_SHIPPED"
    assert recorded["oblique_angles_matching"] == audit.N50_LAST
    assert recorded["certificate_sha256"] == hashlib.sha256(fresh_bytes).hexdigest()
