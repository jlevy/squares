"""Fast reconciliation and adverse controls for the retained complete native run.

These checks do not replay interval coverage. In particular, agreement between a
receipt and its journal cannot authenticate coordinated invented observations.
"""

from __future__ import annotations

import copy
import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from devtools.audit_kleddamag_n11_native import (
    PROOF_COMMIT,
    RECONCILIATION,
    ReceiptContext,
    check_proof_code,
    prepare_context,
    read_documents,
    reconcile,
)


@pytest.fixture(scope="module")
def context() -> ReceiptContext:
    return prepare_context()


@pytest.fixture(scope="module")
def documents() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    return read_documents()


def test_complete_retained_run_reconciles_in_normal_ci(
    context: ReceiptContext, documents: tuple[dict[str, Any], list[dict[str, Any]]]
) -> None:
    result = reconcile(*documents, context)
    assert result["status"] == "RECONCILED_RECEIPT_NOT_COVERAGE_REPLAY"
    assert result["proof_commit"] == PROOF_COMMIT
    assert result["rows_reconciled"] == 12028
    assert result["minimum_recorded_lower_units"] == 999962528
    assert result["total_recorded_boxes"] == 136081500
    assert result["counting_gap"] == "13483/125000000"
    assert result["coverage_replayed"] is False
    assert result["additional_confirmation_method"] is False
    assert json.loads(json.dumps(result)) == json.loads(RECONCILIATION.read_text())


@pytest.mark.parametrize(
    ("path", "value", "message"),
    [
        (("status",), "PASS_PARTIAL", "not PASS_COMPLETE"),
        (("accepted",), False, "not accepted"),
        (("complete",), 1, "not accepted"),
        (("provenance", "git_commit"), "0" * 40, "unexpected proof commit"),
        (("provenance", "dirty"), True, "source was dirty"),
        (("provenance", "certificate_sha256"), "0" * 64, "wrong source identity"),
        (("provenance", "python"), "", "interpreter disagrees"),
        (("minimum_charge",), "1", "minimum_charge disagrees"),
        (("parent_side",), "1", "parent_side disagrees"),
        (("budget",), "11", "budget disagrees"),
        (("batch", "workers"), 3, "batch disagrees"),
        (("rows", 0, "index"), False, "row index must be"),
        (("rows", 1, "index"), 0, "wrong row order or identity"),
        (("rows", 11962, "label"), "11963", "wrong row label"),
        (("rows", 11962, "lower"), 999962527, "below Gamma"),
        (("rows", 11962, "lower"), 999962528.0, "lower bound must be"),
        (("rows", 12027, "stalled"), 1, "has stalls"),
        (("rows", 12027, "budget_exhausted"), True, "exhausted its budget"),
        (("rows", 12027, "status"), "undecided", "is not certified"),
    ],
)
def test_claim_and_outcome_mutations_are_refused(
    context: ReceiptContext,
    documents: tuple[dict[str, Any], list[dict[str, Any]]],
    path: tuple[str | int, ...],
    value: object,
    message: str,
) -> None:
    receipt, journal = copy.deepcopy(documents)
    item: Any = receipt
    for key in path[:-1]:
        item = item[key]
    item[path[-1]] = value
    with pytest.raises(ValueError, match=message):
        reconcile(receipt, journal, context)


def test_missing_final_row_cannot_be_hidden_by_complete_flags(
    context: ReceiptContext, documents: tuple[dict[str, Any], list[dict[str, Any]]]
) -> None:
    receipt, journal = copy.deepcopy(documents)
    receipt["rows"].pop()
    journal.pop()
    with pytest.raises(ValueError, match="incomplete row inventory"):
        reconcile(receipt, journal, context)


def test_journal_must_agree_with_final_receipt(
    context: ReceiptContext, documents: tuple[dict[str, Any], list[dict[str, Any]]]
) -> None:
    receipt, journal = copy.deepcopy(documents)
    journal[-1]["boxes"] += 1
    with pytest.raises(ValueError, match="journal rows differ"):
        reconcile(receipt, journal, context)


def test_reconciliation_does_not_authenticate_coordinated_invented_data(
    context: ReceiptContext, documents: tuple[dict[str, Any], list[dict[str, Any]]]
) -> None:
    receipt, journal = copy.deepcopy(documents)
    receipt["rows"][0]["seconds"] = 123456.0
    journal[1]["seconds"] = 123456.0
    result = reconcile(receipt, journal, context)
    assert result["coverage_replayed"] is False
    assert "cannot authenticate coordinated invented data" in result["limitations"][0]


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ('{"accepted":false,"accepted":true}', "duplicate receipt key"),
        ('{"seconds":NaN}', "non-finite JSON number"),
        ('{"seconds":Infinity}', "non-finite JSON number"),
    ],
)
def test_json_reader_rejects_ambiguous_or_nonfinite_values(
    tmp_path: Path, text: str, message: str
) -> None:
    receipt = tmp_path / "receipt.json"
    journal = tmp_path / "journal.jsonl"
    receipt.write_text(text)
    journal.write_text("{}\n")
    with pytest.raises(ValueError, match=message):
        read_documents(receipt, journal)


def _git(repository: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments], cwd=repository, check=True, capture_output=True, text=True
    ).stdout.strip()


def test_git_reuse_boundary_binds_transitive_code_and_lock_not_unrelated_docs(
    tmp_path: Path,
) -> None:
    _git(tmp_path, "init", "--quiet")
    paths = ("dependency.py", "uv.lock")
    (tmp_path / paths[0]).write_text("EXACT = True\n")
    (tmp_path / paths[1]).write_text("version = 1\n")
    _git(tmp_path, "add", ".")
    _git(
        tmp_path,
        "-c",
        "core.hooksPath=/dev/null",
        "-c",
        "user.name=Receipt test",
        "-c",
        "user.email=receipt-test@example.invalid",
        "commit",
        "--quiet",
        "-m",
        "Frozen proof fixture",
    )
    revision = _git(tmp_path, "rev-parse", "HEAD")
    manifest = check_proof_code(tmp_path, revision=revision, paths=paths)
    assert {entry["path"] for entry in manifest} == set(paths)
    (tmp_path / "notes.md").write_text("A documentation-only continuation.\n")
    assert check_proof_code(tmp_path, revision=revision, paths=paths) == manifest
    for relative in paths:
        target = tmp_path / relative
        frozen = target.read_text()
        target.write_text(frozen + "# changed\n")
        with pytest.raises(ValueError, match="proof input differs from frozen Git blob"):
            check_proof_code(tmp_path, revision=revision, paths=paths)
        target.write_text(frozen)


def test_reader_accepts_original_json_semantics(tmp_path: Path) -> None:
    receipt = tmp_path / "receipt.json"
    journal = tmp_path / "journal.jsonl"
    receipt.write_text(json.dumps({"exact": 999962528}))
    journal.write_text('{"index": 0}\n')
    assert read_documents(receipt, journal) == ({"exact": 999962528}, [{"index": 0}])
