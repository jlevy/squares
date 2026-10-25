"""The counts the statement audit of the Lean proof that s(12) = 4 cites, and their receipt.

``devtools.audit_n12_lean`` reads every module a ``devtools.lean_closure`` receipt names
by its Git blob and counts tokens, instance classes, declarations of the statement's
names and the declarations that hold each ``native_decide``, against the source's run
evidence. The 5,377-module closure is not retained here, so these tests run the tool on a
small synthetic project in a scratch Git repository, and hold the retained receipt to
the packet's own bytes (the statement closure and the run evidence) and to the review
that cites it.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from devtools import audit_n12_lean as audit
from devtools import lean_closure

REVIEW = (
    audit.REPO
    / "docs/project/reviews/review-2026-10-25-n12-lean-formalization-statement-audit.md"
)
SCRATCH_GIT = (
    "-c",
    "user.name=n12 audit test",
    "-c",
    "user.email=n12-audit-test@example.invalid",
    "-c",
    "commit.gpgsign=false",
    "-c",
    "core.hooksPath=/dev/null",
)
FILES: dict[str, str] = {
    "lean/lean-toolchain": "leanprover/lean4:v4.35.0\n",
    "lean/lakefile.toml": (
        'name = "pkg"\n\n[[lean_lib]]\nname = "S12"\n\n[[lean_lib]]\nname = "Compact"\n'
    ),
    "lean/S12/Diagonal.lean": (
        "import Mathlib\n\nnamespace S12Pilot\n"
        "-- an axiom named in a comment is not code\n"
        "def InBands (a u : Nat) : Prop := a < u\n"
        "structure OpenSquare where\n  side : Nat\n"
        "def OpenSquare.Inside (q : OpenSquare) (x : Nat) : Prop := x < q.side\n"
        "instance (a u : Nat) : Decidable (InBands a u) := Nat.decLt a u\n"
        "end S12Pilot\n"
    ),
    "lean/S12/PackingConstant.lean": (
        "import S12.Diagonal\n\nnamespace S12\nopen S12Pilot\n"
        "def packingConstant12 : Nat := 4\n"
        "set_option maxHeartbeats 0 in\n"
        "theorem used_checked : 2 + 2 = 4 := by native_decide\n"
        "theorem twice_checked : 1 = 1 ∧ 2 = 2 := ⟨by native_decide, by native_decide⟩\n"
        "theorem unused_count : 3 = 3 := by native_decide\n"
        'def note : String := "native_decide in a string"\n'
        "end S12\n"
    ),
    "lean/Compact/Final.lean": (
        "import S12.PackingConstant\nimport Lean\n\nnamespace N12Compact.Final\n"
        'syntax (name := checked) "checked " ident : command\n'
        "inductive Variant | a\n"
        "instance : Fintype Variant := sorry_free\n"
        "theorem optimality : S12.packingConstant12 = 4 := rfl\n"
        "end N12Compact.Final\n"
    ),
}
AXIOMS = [
    "propext",
    "Classical.choice",
    "Quot.sound",
    "S12.used_checked._native.native_decide.ax_1",
    "S12.twice_checked._native.native_decide.ax_1",
    "S12.twice_checked._native.native_decide.ax_2",
]


def _git(checkout: Path, *arguments: str) -> str:
    done = subprocess.run(
        ("git", "-C", str(checkout), *SCRATCH_GIT, *arguments),
        capture_output=True,
        text=True,
        check=True,
        env={
            "PATH": "/usr/bin:/bin",
            "GIT_AUTHOR_DATE": "2026-01-01T00:00:00Z",
            "GIT_COMMITTER_DATE": "2026-01-01T00:00:00Z",
        },
    )
    return done.stdout.strip()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@pytest.fixture
def project(tmp_path: Path) -> dict[str, Path]:
    """A checkout at a commit, its closure receipt, a run directory and a provenance
    record, with every digest the run's own."""
    checkout = tmp_path / "upstream"
    checkout.mkdir()
    _git(checkout, "init", "--quiet")
    for name, text in FILES.items():
        path = checkout / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    _git(checkout, "add", "-A")
    _git(checkout, "commit", "--quiet", "-m", "pin")
    commit = _git(checkout, "rev-parse", "HEAD")
    # The working tree is never read: the receipt names blobs at the commit.
    (checkout / "lean/S12/Diagonal.lean").write_text("axiom bad : False\n", encoding="utf-8")
    report = lean_closure.closure(
        lean_closure.Source(checkout, commit),
        "lean",
        ["Compact.Final"],
        "https://example.invalid/pkg",
    )
    closure = tmp_path / "lean-closure.json.gz"
    closure.write_bytes(gzip.compress(json.dumps(report).encode(), mtime=0))
    run = tmp_path / "run"
    run.mkdir()
    listed = ",\n ".join(AXIOMS)
    log = f"'N12Compact.Final.optimality' depends on axioms: [{listed}]\n"
    (run / "global-type-axiom-audit.log").write_text(log, encoding="utf-8")
    (run / "global-native-axiom-audit.json").write_text(
        json.dumps({"final_axioms": sorted(AXIOMS)}), encoding="utf-8"
    )
    manifest = {
        "source_commit": "upstream",
        "root_module": "Compact.Final",
        "modules": [
            {
                "module": module["module"],
                "path": module["path"],
                "sha256": _sha256(FILES[module["path"]].encode()),
            }
            for module in report["modules"]
        ],
    }
    (run / "verified-source-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    provenance = tmp_path / "SOURCE-PROVENANCE.json"
    provenance.write_text(
        json.dumps(
            {
                "final_audit_log_sha256": _sha256(log.encode()),
                "source_manifest_sha256": _sha256(json.dumps(manifest).encode()),
            }
        ),
        encoding="utf-8",
    )
    return {"checkout": checkout, "closure": closure, "run": run, "provenance": provenance}


def _scan(paths: dict[str, Path]) -> dict:
    closure = audit.load_closure(paths["closure"])
    return audit.audit(
        audit.read_checkout(paths["checkout"], closure),
        closure,
        closure_path=paths["closure"],
        run=paths["run"],
        provenance=paths["provenance"],
    )


def test_the_instance_class_is_the_word_after_the_last_top_level_colon() -> None:
    assert audit.instance_class("instance (a : Nat) : Decidable (P a)") == "Decidable"
    assert audit.instance_class("instance : DecidableRel (fun (a b : Nat) ↦ a < b)") == (
        "DecidableRel"
    )
    assert audit.instance_class("instance foo") == "?"


def test_the_scan_counts_code_tokens_owners_and_names(project: dict[str, Path]) -> None:
    receipt = _scan(project)
    whole, statement = receipt["closure"], receipt["statement"]
    assert whole["modules"] == 3
    assert statement["modules"] == 2
    assert receipt["statement_targets"] == ["S12.PackingConstant"]
    native = whole["tokens"]["native_decide"]
    assert (native["occurrences_code"], native["occurrences_raw"]) == (4, 5)
    assert native["hits_code"][0] == "lean/S12/PackingConstant.lean:7"
    assert whole["tokens"]["axiom_word"]["occurrences_code"] == 0
    assert whole["tokens"]["axiom_word"]["occurrences_raw"] == 1
    assert whole["tokens"]["macro"]["files_code"] == 1
    assert statement["tokens"]["macro"]["occurrences_code"] == 0
    assert whole["tokens"]["import_Lean"]["occurrences_code"] == 1
    assert whole["set_option"] == {"maxHeartbeats": 1}
    assert whole["instances"] == {"Decidable": 1, "Fintype": 1}
    assert whole["instances_not_decidable"] == ["lean/Compact/Final.lean:7: Fintype"]
    assert statement["instances"] == {"Decidable": 1}
    declared = receipt["shadowing"]["declarations"]
    assert declared["packingConstant12"] == [
        "def S12.packingConstant12 lean/S12/PackingConstant.lean:5"
    ]
    assert declared["Inside"] == ["def S12Pilot.OpenSquare.Inside lean/S12/Diagonal.lean:8"]
    assert declared["optimality"] == [
        "theorem N12Compact.Final.optimality lean/Compact/Final.lean:8"
    ]
    assert receipt["shadowing"]["nested_namespaces"] == []


def test_every_native_axiom_is_matched_to_the_calls_of_its_owner(
    project: dict[str, Path],
) -> None:
    native = _scan(project)["native"]
    assert native["calls"] == 4
    assert native["declarations"] == 3
    assert native["native_axioms"] == 3
    assert native["native_owners"] == 2
    assert native["owners_without_a_site"] == []
    assert native["owners_whose_axioms_are_not_their_calls"] == []
    assert (native["on_path"]["declarations"], native["on_path"]["calls"]) == (2, 3)
    off = native["off_path"]["by_module"]
    assert off == {
        "lean/S12/PackingConstant.lean": {
            "declarations": 1,
            "calls": 1,
            "names": ["S12.unused_count"],
        }
    }


def test_an_axiom_without_its_calls_is_reported(project: dict[str, Path]) -> None:
    log = project["run"] / "global-type-axiom-audit.log"
    log.write_text(
        log.read_text(encoding="utf-8").replace(
            "Quot.sound,", "Quot.sound,\n S12.used_checked._native.native_decide.ax_2,"
        ),
        encoding="utf-8",
    )
    native = _scan(project)["native"]
    assert native["owners_whose_axioms_are_not_their_calls"] == [
        "S12.used_checked: 2 axioms, 1 calls"
    ]


def test_the_run_evidence_is_held_to_the_bytes_read(project: dict[str, Path]) -> None:
    receipt = _scan(project)
    manifest, log = receipt["manifest"], receipt["axiom_log"]
    assert manifest["same_modules_as_closure"]
    assert manifest["sha256_mismatches"] == []
    assert manifest["sha256"] == manifest["provenance_sha256"]
    assert log["equals_native_audit_final_axioms"]
    assert log["standard_axioms"] == ["Classical.choice", "Quot.sound", "propext"]
    assert log["sha256"] == log["provenance_sha256"]
    path = project["run"] / "verified-source-manifest.json"
    tampered = json.loads(path.read_text(encoding="utf-8"))
    tampered["modules"][0]["sha256"] = "0" * 64
    path.write_text(json.dumps(tampered), encoding="utf-8")
    assert _scan(project)["manifest"]["sha256_mismatches"] == [tampered["modules"][0]["module"]]


def test_a_receipt_naming_other_bytes_is_refused(project: dict[str, Path]) -> None:
    closure = audit.load_closure(project["closure"])
    closure["modules"][0]["blob"] = "0" * 40
    with pytest.raises(SystemExit, match="is not blob"):
        audit.read_checkout(project["checkout"], closure)


def test_the_retained_receipt_agrees_with_the_packet() -> None:
    # The statement closure and the run evidence are retained, so every part of the
    # receipt they decide is recomputed from the packet's bytes.
    assert audit.check() == []


def test_the_receipt_holds_what_the_review_cites() -> None:
    receipt = json.loads(audit.RECEIPT.read_text(encoding="utf-8"))
    native, whole = receipt["native"], receipt["closure"]
    assert receipt["commit"] == "d0caf4532a7ead68be1389ef87387b126fc2e0ab"
    assert (whole["modules"], receipt["statement"]["modules"]) == (5377, 109)
    assert native["standard_axioms"] == ["Classical.choice", "Quot.sound", "propext"]
    assert (native["native_axioms"], native["native_owners"]) == (1624, 1525)
    assert (native["calls"], native["declarations"]) == (2572, 2274)
    assert (native["off_path"]["calls"], native["off_path"]["declarations"]) == (948, 749)
    assert native["owners_without_a_site"] == []
    assert native["owners_whose_axioms_are_not_their_calls"] == []
    assert receipt["manifest"]["modules_compared"] == 5377
    assert receipt["manifest"]["sha256_mismatches"] == []
    review = REVIEW.read_text(encoding="utf-8")
    assert "devtools/audit_n12_lean.py" in review
    assert "receipts/statement-audit.json" in review
    for figure in ("1,624", "1,525", "2,572", "2,274", "948", "749", "15,166"):
        assert figure in review, figure
