"""The audit of the 11SquaresFormalized Lean proof of s(11) = T, and its retained receipts.

``devtools.audit_n11_lean`` extracts the axiom receipt from the source's final audit,
scans the commit's archive for kernel escapes, and stages the statement closure. The
final audit and the archive are not retained here, so these tests run the scanner and the
extractor on small synthetic inputs, stage the closure from the packet, and hold the
retained receipts to each other and to what the records say of them.
"""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import tarfile
from pathlib import Path

import pytest

from devtools import audit_n11_lean as audit

LEAN = audit.RECEIPTS / "lean"


def test_comments_and_strings_do_not_count() -> None:
    text = (
        "/- a /- nested native_decide -/ sorry -/\ntheorem t : True := trivial -- sorry\n"
        'def s : String := "implemented_by unsafe"\n'
    )
    counts = audit.token_counts(text)
    assert counts["sorry"] == 0
    assert counts["native_decide"] == 0
    assert counts["implemented_by"] == 0
    assert counts["unsafe"] == 0
    assert "theorem t : True := trivial" in audit.strip_code(text)
    assert len(audit.strip_code(text)) == len(text)


def test_char_literals_and_raw_strings_do_not_open_strings() -> None:
    text = 'def q := \'"\'\ntheorem x : False := sorry\ndef r := r#"axiom "no" sorry"#\n'
    counts = audit.token_counts(text)
    assert counts["sorry"] == 1
    hits = audit.token_hits(text)["sorry"]
    assert hits == [(2, True), (3, False)]
    primed = "theorem h' : True := trivial\ntheorem g : False := sorry\n"
    assert audit.token_counts(primed)["sorry"] == 1


ESCAPES = [
    (line, token)
    for token, _, line in (
        row.partition("\t")
        for row in (Path(__file__).parent / "fixtures/n11-lean/escapes.tsv")
        .read_text(encoding="utf-8")
        .splitlines()
        if row and not row.startswith("#")
    )
]


@pytest.mark.parametrize(("line", "token"), ESCAPES)
def test_each_escape_is_found_in_code(line: str, token: str) -> None:
    assert audit.token_counts(line + "\n")[token] == 1


def _gz(payload: dict[str, object]) -> bytes:
    return gzip.compress(json.dumps(payload).encode(), mtime=0)


def test_the_axiom_receipt_separates_native_from_standard_axioms() -> None:
    native = [f"A.d{i}._native.native_decide.ax_1_{j}" for i in range(3) for j in (1, 2)]
    payload: dict[str, object] = {
        "status": "OPTIMALITY_PROVED_WITH_NATIVE_CERTIFICATES",
        "trust_model": "lean_kernel_and_native_compiler",
        "global_optimality_proved": True,
        "checked_modules": 2,
        "lean_toolchain": "leanprover/lean4:v4.34.1",
        "mathlib_revision": "d13f23b7",
        "explicit_native_admissions": 0,
        "native_certificate_axioms": native,
        "axioms": {
            "ElevenSquare.optimality": ["propext", "Quot.sound", "Classical.choice", *native],
            "ElevenSquare.Pending.prior_certificate_exists": ["propext", native[0]],
        },
    }
    raw = _gz(payload)
    receipt = audit.axiom_receipt(payload, raw)
    top = receipt["public_theorems"]["ElevenSquare.optimality"]
    assert top["non_native_axioms"] == ["Classical.choice", "Quot.sound", "propext"]
    assert top["native_decide_axioms"] == 6
    assert top["native_decide_owner_declarations"] == 3
    assert top["native_set_equals_audit_native_list"]
    assert not top["sorryAx"]
    prior = receipt["public_theorems"]["ElevenSquare.Pending.prior_certificate_exists"]
    assert prior["native_subset_of_audit_native_list"]
    assert not prior["native_set_equals_audit_native_list"]
    assert receipt["public_theorems"]["ElevenSquare.optimal_side_lower_bound"] is None
    assert receipt["final_audit_sha256"] == hashlib.sha256(gzip.decompress(raw)).hexdigest()


def test_an_audit_with_other_bytes_is_refused(tmp_path: Path) -> None:
    path = tmp_path / "final-audit.json.gz"
    path.write_bytes(_gz({"status": "forged"}))
    with pytest.raises(SystemExit, match="not the final audit the packet pins"):
        audit.load_final_audit(path)


def test_the_archive_scan_compares_hashes_and_counts_escapes() -> None:
    files = {
        "ElevenSquare/A.lean": b"theorem a : True := trivial -- sorry\n",
        "ElevenSquare/B.lean": b"theorem b : 1 = 1 := by native_decide\n",
        "README.md": b"sorry\n",
    }
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        for name, data in files.items():
            info = tarfile.TarInfo(f"top-abc/{name}")
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    expected = {
        "ElevenSquare.A": hashlib.sha256(files["ElevenSquare/A.lean"]).hexdigest(),
        "ElevenSquare.B": "0" * 64,
        "ElevenSquare.C": "1" * 64,
    }
    buffer.seek(0)
    report = audit.scan_archive(buffer, expected)
    assert report["lean_files"] == 2
    assert report["all_files"] == 3
    assert report["sha256_match"] == 1
    assert report["sha256_mismatch"] == ["ElevenSquare.B"]
    assert report["in_audit_not_in_tree"] == ["ElevenSquare.C"]
    tokens = report["tokens"]
    assert {k for k, v in tokens.items() if v["files_code"]} == {"native_decide"}
    assert tokens["sorry"]["files_raw"] == 1
    assert tokens["sorry"]["raw_hits"] == [
        {"path": "ElevenSquare/A.lean", "line": 1, "in_code": False}
    ]
    assert tokens["axiom_decl"]["occurrences_raw"] == 0


def test_the_statement_closure_stages_from_the_packet(tmp_path: Path) -> None:
    written = audit.stage(tmp_path)
    assert len(written) == len(audit.CLOSURE) + len(audit.PINS) + 1
    staged = {p.stem for p in (tmp_path / "ElevenSquare").glob("*.lean")}
    assert staged == set(audit.CLOSURE)
    # The closure is closed: every local import of a staged module is staged.
    for path in (tmp_path / "ElevenSquare").glob("*.lean"):
        assert audit.local_imports(path.read_text(encoding="utf-8")) <= staged
    assert (tmp_path / "lean-toolchain").read_text().strip() == "leanprover/lean4:v4.34.1"
    assert "IsLeast" in (tmp_path / "AuditN11Statement.lean").read_text(encoding="utf-8")


def test_the_retained_receipts_agree_with_each_other() -> None:
    receipt = json.loads((LEAN / "axioms-public-theorems.json").read_text(encoding="utf-8"))
    assert receipt["final_audit_matches_summary"]
    assert receipt["final_audit_gz_sha256"] == audit.pinned_sha256(audit.FINAL_AUDIT)
    assert receipt["non_native_axioms_anywhere"] == sorted(audit.STANDARD_AXIOMS)
    native = gzip.decompress((LEAN / "native-axioms.txt.gz").read_bytes()).decode().split()
    assert len(native) == receipt["native_decide_axioms_in_audit"] == 13308
    assert all(audit.NATIVE_MARK in name for name in native)
    top = receipt["public_theorems"]["ElevenSquare.optimality"]
    assert top["native_decide_axioms"] == 13308
    assert top["non_native_axioms"] == sorted(audit.STANDARD_AXIOMS)
    scan = json.loads((audit.RECEIPTS / "tree-scan.json").read_text(encoding="utf-8"))
    assert scan["sha256_match"] == scan["final_audit_modules"] == 7920
    assert not scan["sha256_mismatch"]
    assert not scan["in_audit_not_in_tree"]
    tokens = scan["tokens"]
    assert set(tokens) == set(audit.TOKENS)
    assert all(tokens[name]["pattern"] == pattern for name, pattern in audit.TOKENS.items())
    assert tokens["native_decide"]["occurrences_code"] == 10464
    assert tokens["native_decide"]["files_code"] == 1839
    for name in ("sorry", "admit", "axiom_decl", "implemented_by", "extern", "unsafe"):
        assert tokens[name]["occurrences_code"] == 0, name
        hits = tokens[name]["raw_hits"]
        assert isinstance(hits, list)
        assert not any(hit["in_code"] for hit in hits), name


def test_the_statement_probe_printed_only_standard_axioms() -> None:
    log = (LEAN / "build-statement-closure.log").read_text(encoding="utf-8")
    assert "error" not in log.lower()
    lines = [line for line in log.splitlines() if "depends on axioms" in line]
    assert len(lines) == 6
    assert all(line.endswith("[propext, Classical.choice, Quot.sound]") for line in lines)
    assert any("construction_packable" in line for line in lines)
    exits = [line for line in log.splitlines() if line.startswith("# exit ")]
    assert exits
    assert all(line.startswith("# exit 0;") for line in exits)
    built = {
        line.removeprefix("# command: lake build ElevenSquare.")
        for line in log.splitlines()
        if line.startswith("# command: lake build ElevenSquare.")
    }
    assert built == set(audit.CLOSURE)
    assert "Built Mathlib" not in log
