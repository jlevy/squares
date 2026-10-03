"""Fast reconciliation and adverse controls for the retained complete native run.

These checks do not replay interval coverage. In particular, agreement between a
receipt and its journal cannot authenticate coordinated invented observations.

The run is bound to the revision that produced it. Nothing here depends on the
working tree matching that revision: the reconciliation context is prepared from a
directory holding only the certificate, with no Git history and no environment file,
and drift since the run is reported, never refused. That the current verifier still
decides as the run did is tested on one retained row, not by freezing files.
"""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
from dataclasses import asdict
from math import ceil
from pathlib import Path
from typing import Any

import pytest

from devtools.audit_kleddamag_n11_native import (
    PROOF_COMMIT,
    PROOF_INPUTS,
    RECONCILIATION,
    ReceiptContext,
    drift_line,
    prepare_context,
    proof_input_drift,
    read_documents,
    reconcile,
)
from devtools.verify_kleddamag_n11_native import REPO, REVIEWED_SHA256, SOURCE
from sqpack.fractional.parent_core import load_kleddamag_parent_core
from sqpack.fractional.parent_core_interval import parent_core_search
from sqpack.fractional.threshold_interval import ThresholdAtomData

#: What the reconciliation says about the receipt. The v1 document retained on
#: 2026-09-22 also lists the proof inputs' Git blobs and a limitation saying Git
#: identity froze them; those stay there as history and are not recomputed.
RECONCILED_FIELDS = (
    "status",
    "coverage_replayed",
    "additional_confirmation_method",
    "proof_commit",
    "certificate_sha256",
    "rows_reconciled",
    "minimum_recorded_lower_units",
    "threshold_units",
    "total_recorded_boxes",
    "counting_gap",
    "exact_premises",
)

#: The cheapest row of the retained run: under a second, where the run took 6,197 s.
DETERMINISM_ROW = 4795


@pytest.fixture(scope="module")
def context(tmp_path_factory: pytest.TempPathFactory) -> ReceiptContext:
    bare = tmp_path_factory.mktemp("certificate-only")
    target = bare / SOURCE.relative_to(REPO)
    target.parent.mkdir(parents=True)
    shutil.copyfile(SOURCE, target)
    return prepare_context(bare)


@pytest.fixture(scope="module")
def documents() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    return read_documents()


def test_complete_retained_run_reconciles_in_normal_ci(
    context: ReceiptContext, documents: tuple[dict[str, Any], list[dict[str, Any]]]
) -> None:
    result = json.loads(json.dumps(reconcile(*documents, context)))
    assert result["status"] == "RECONCILED_RECEIPT_NOT_COVERAGE_REPLAY"
    assert result["proof_commit"] == PROOF_COMMIT
    assert result["rows_reconciled"] == 12028
    assert result["minimum_recorded_lower_units"] == 999962528
    assert result["total_recorded_boxes"] == 136081500
    assert result["counting_gap"] == "13483/125000000"
    assert result["coverage_replayed"] is False
    assert result["additional_confirmation_method"] is False
    assert set(result) == {"schema", "limitations", *RECONCILED_FIELDS}
    retained = json.loads(RECONCILIATION.read_text())
    assert {field: result[field] for field in RECONCILED_FIELDS} == {
        field: retained[field] for field in RECONCILED_FIELDS
    }


def test_current_verifier_decides_a_retained_row_as_the_run_did(
    documents: tuple[dict[str, Any], list[dict[str, Any]]],
) -> None:
    """The retained run is never executed again; one of its rows is, by today's code.

    Agreement on the row's whole outcome -- bounds, box count and witness -- is what says
    the verifier still decides as it did at `PROOF_COMMIT`, whatever has changed in the
    code, the dependencies or the interpreter since. If an intended change to the search
    moves this row, pin the new outcome here as a literal and say why; the retained run
    stays bound to its revision and is not re-run.
    """
    receipt, _journal = documents
    certificate = load_kleddamag_parent_core(SOURCE, expected_sha256=REVIEWED_SHA256)
    data = ThresholdAtomData.of(certificate, batch_size=receipt["batch"]["boxes"])
    threshold = ceil(certificate.minimum_charge * data.scale)
    assert threshold == receipt["threshold_units"]
    outcome = parent_core_search(certificate, data, DETERMINISM_ROW).search(prune_at=threshold)
    retained = {
        key: value
        for key, value in receipt["rows"][DETERMINISM_ROW].items()
        if key not in ("index", "seconds")
    }
    assert json.loads(json.dumps(asdict(outcome))) == retained


def test_recorded_runtime_is_history_not_a_condition(
    context: ReceiptContext, documents: tuple[dict[str, Any], list[dict[str, Any]]]
) -> None:
    receipt, journal = copy.deepcopy(documents)
    for provenance in (receipt["provenance"], journal[0]["provenance"]):
        provenance["python"] = "3.15.0 (another interpreter)"
        provenance["platform"] = "another host"
    assert reconcile(receipt, journal, context)["rows_reconciled"] == 12028


@pytest.mark.parametrize(
    ("path", "value", "message"),
    [
        (("status",), "PASS_PARTIAL", "not PASS_COMPLETE"),
        (("accepted",), False, "not accepted"),
        (("complete",), 1, "not accepted"),
        (("provenance", "git_commit"), "0" * 40, "unexpected proof commit"),
        (("provenance", "dirty"), True, "source was dirty"),
        (("provenance", "certificate_sha256"), "0" * 64, "wrong source identity"),
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


def _commit(repository: Path, message: str) -> str:
    _git(repository, "add", ".")
    _git(
        repository,
        "-c",
        "core.hooksPath=/dev/null",
        "-c",
        "user.name=Receipt test",
        "-c",
        "user.email=receipt-test@example.invalid",
        "commit",
        "--quiet",
        "-m",
        message,
    )
    return _git(repository, "rev-parse", "HEAD")


def test_proof_input_drift_is_reported_and_never_refused(tmp_path: Path) -> None:
    """A run at an older proof commit is read at a later HEAD with its drift listed."""
    _git(tmp_path, "init", "--quiet")
    paths = ("verifier.py", "kernel.py")
    (tmp_path / "verifier.py").write_text("EXACT = True\n")
    (tmp_path / "kernel.py").write_text("STEP = 1\n")
    (tmp_path / "uv.lock").write_text("version = 1\n")
    proof = _commit(tmp_path, "Proof commit")
    assert proof_input_drift(tmp_path, revision=proof, paths=paths) == ()
    (tmp_path / "uv.lock").write_text("version = 1\n# a new pinned dependency\n")
    (tmp_path / "notes.md").write_text("A documentation-only continuation.\n")
    _commit(tmp_path, "A dependency and a note")
    assert proof_input_drift(tmp_path, revision=proof, paths=paths) == ()
    (tmp_path / "kernel.py").write_text("STEP = 1  # faster, same answers\n")
    _commit(tmp_path, "A kernel change")
    (tmp_path / "verifier.py").write_text("EXACT = True  # uncommitted\n")
    drift = proof_input_drift(tmp_path, revision=proof, paths=paths)
    assert drift == ("kernel.py", "verifier.py")
    assert "informational" in drift_line(drift, proof)
    assert proof_input_drift(tmp_path, revision="0" * 40, paths=paths) is None
    assert "unknown" in drift_line(None, proof)


def test_environment_declarations_are_not_proof_inputs() -> None:
    assert not {
        "packing/pyproject.toml",
        "packing/uv.lock",
        "packing/.python-version",
    } & set(PROOF_INPUTS)


def test_reader_accepts_original_json_semantics(tmp_path: Path) -> None:
    receipt = tmp_path / "receipt.json"
    journal = tmp_path / "journal.jsonl"
    receipt.write_text(json.dumps({"exact": 999962528}))
    journal.write_text('{"index": 0}\n')
    assert read_documents(receipt, journal) == ({"exact": 999962528}, [{"index": 0}])
