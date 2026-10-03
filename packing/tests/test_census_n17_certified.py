"""Controls for the n17 certified census: what it refuses and what it counts."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from devtools.census_n17_certified import (
    BB_CERTIFIED,
    BB_SCHEMA,
    CENSUS,
    DEFAULT_LEDGER,
    DESIGN,
    KERNEL_FRAME,
    LEDGER_SCHEMA,
    REPO,
    VERIFICATION_SCHEMA,
    RefusedError,
    census,
    cover_context,
)

W7 = ["corner-SW", "side-N0", "side-W0", "side-W1", "side-W2", "interior-SW", "interior-W"]
A = ["interior-SW", "interior-NW", "interior-W", "interior-S", "interior-N", "interior-SE"]
SEED, NODE, MANIFEST = "a" * 64, "b" * 64, "c" * 64
VERIFIERS = {"kernel": "tools/verify_kernel.py", "branch-and-bound": "tools/verify_bb.py"}


def git(root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), *arguments], capture_output=True, text=True, check=True
    )
    return completed.stdout.strip()


def commit_verifiers(root: Path, text: str) -> str:
    """The two fabricated verifiers committed under the root with this text; the revision."""
    if not (root / ".git").exists():
        _ = git(root, "init", "-q")
        _ = git(root, "config", "user.email", "census@example.invalid")
        _ = git(root, "config", "user.name", "census")
    for path in VERIFIERS.values():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        _ = (root / path).write_text(text, encoding="utf-8")
    _ = (root / "review.md").write_text("admits the verifiers\n", encoding="utf-8")
    _ = git(root, "add", "-A")
    _ = git(root, "commit", "-qm", text, "--no-verify", "--allow-empty")
    return git(root, "rev-parse", "HEAD")


def write_json(root: Path, name: str, document: dict[str, Any]) -> str:
    """A fabricated receipt under the root: its relative path."""
    path = root / "receipts" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    _ = path.write_text(json.dumps(document), encoding="utf-8")
    return f"receipts/{name}"


def kernel_receipt(cells: list[str]) -> dict[str, Any]:
    return {
        "status": "PASS_SAVED_CLOSED",
        "cells": cells,
        "frame": KERNEL_FRAME,
        "seed_sha256": SEED,
        "node_sha256": NODE,
    }


def bb_receipt(cells: list[str], **extra: Any) -> dict[str, Any]:
    return {
        "schema": BB_SCHEMA,
        "design": DESIGN,
        "pattern": cells,
        "verdict": BB_CERTIFIED,
        "control": False,
        "certificate_manifest": MANIFEST,
        **extra,
    }


def saved_certificate(root: Path, name: str) -> str:
    """A certificate directory holding files with the names the receipts give."""
    directory = root / "certificates" / name
    directory.mkdir(parents=True, exist_ok=True)
    for object_name in (f"seed-{SEED}", f"node-{NODE}", MANIFEST):
        _ = (directory / f"{object_name}.json.gz").write_bytes(b"")
    return f"certificates/{name}"


def verification(root: Path, name: str, certifier: str, cells: list[str], **extra: Any) -> Any:
    """A fabricated full, passing verification receipt from the committed verifier, run on
    unedited bytes at the root's current revision, of the objects `saved_certificate`
    writes, in the directory of that name."""
    kernel = certifier == "kernel"
    objects = (
        {"seed_sha256": SEED, "node_sha256": NODE} if kernel else {"manifest_sha256": MANIFEST}
    )
    document = {
        "schema": VERIFICATION_SCHEMA,
        "verifier": certifier,
        "provenance": {
            "revision": git(root, "rev-parse", "HEAD"),
            "dirty": False,
            "files": {VERIFIERS[certifier]: "0" * 40},
        },
        "directory": f"certificates/{name}",
        "certificate": objects,
        "status": "PASS",
        "mode": "full",
        "cells" if kernel else "pattern": cells,
        **extra,
    }
    return {"receipt": write_json(root, f"verify-{name}.json", document)}


def entry(name: str, cells: list[str], receipt: str, **fields: Any) -> dict[str, Any]:
    return {
        "name": name,
        "cells": cells,
        "certifier": "kernel",
        "receipt": receipt,
        "certificate": None,
        "status": "pending",
        "evidence": None,
        **fields,
    }


def run_census(
    root: Path,
    entries: list[dict[str, Any]],
    revisions: list[str] | None = None,
    listings: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """The census of the entries, with each verifier listed at the given revisions (by
    default the root's first commit, made here when the root has none), or with the given
    listings in place of those."""
    if revisions is None:
        revisions = [
            git(root, "rev-list", "--max-parents=0", "HEAD")
            if (root / ".git").exists()
            else commit_verifiers(root, "the reviewed verifier\n")
        ]
    ledger = root / "ledger.yaml"
    document = {
        "schema": LEDGER_SCHEMA,
        "design": DESIGN,
        "verifiers": listings
        if listings is not None
        else [
            {"path": path, "revision": revision, "review": "review.md"}
            for path in VERIFIERS.values()
            for revision in revisions
        ],
        "entries": entries,
    }
    _ = ledger.write_text(json.dumps(document), encoding="utf-8")  # JSON is YAML
    return census(ledger, root=root, selector_receipts=())


def image_names(cells: list[str], element: int) -> list[str]:
    """The cell names of one D4 image of a pattern."""
    geometry = cover_context().geometry
    permutation = geometry.group[element]
    return [geometry.names[permutation[geometry.names.index(name)]] for name in cells]


def test_an_empty_ledger_reproduces_the_h266_census(tmp_path: Path) -> None:
    record = run_census(tmp_path, [])
    assert record["census"]["surviving_states"] == CENSUS["states"] == 346104
    assert record["census"]["orbits"] == CENSUS["orbits"] == 43593
    for line in ("certified", "pending_verified_projection", "pending_all_projection"):
        assert record[line]["surviving_states"] == 346104
        assert record[line]["orbits"] == 43593
        assert record[line]["endpoint_survives"]


def test_a_missing_receipt_is_refused(tmp_path: Path) -> None:
    with pytest.raises(RefusedError, match="does not exist"):
        _ = run_census(tmp_path, [entry("W7", W7, "receipts/w7.json")])


def test_cells_that_disagree_with_the_receipt_are_refused(tmp_path: Path) -> None:
    receipt = write_json(tmp_path, "w7.json", kernel_receipt(W7))
    other = [*W7[:-1], "interior-NW"]
    with pytest.raises(RefusedError, match="another class"):
        _ = run_census(tmp_path, [entry("W7", other, receipt)])
    # The comparison is by D4 class: an image of the receipt's cells is the same claim.
    turned = run_census(tmp_path, [entry("W7", image_names(W7, 1), receipt)])
    assert turned["entries"][0]["verified"]


def test_an_entry_excluding_the_endpoint_state_is_refused(tmp_path: Path) -> None:
    context = cover_context()
    inside = [
        name for k, name in enumerate(context.geometry.names) if context.endpoint_state >> k & 1
    ]
    cells = inside[:3]
    receipt = write_json(tmp_path, "endpoint.json", kernel_receipt(cells))
    with pytest.raises(RefusedError, match="endpoint"):
        _ = run_census(tmp_path, [entry("E", cells, receipt)])


def test_only_admitted_entries_are_counted(tmp_path: Path) -> None:
    _ = commit_verifiers(tmp_path, "the reviewed verifier\n")
    w7 = write_json(tmp_path, "w7.json", kernel_receipt(W7))
    a = write_json(tmp_path, "a.json", bb_receipt(A))
    review = tmp_path / "review.md"
    _ = review.write_text("admits W7\n", encoding="utf-8")
    entries = [
        entry(
            "W7",
            W7,
            w7,
            status="admitted",
            evidence="review.md",
            certificate=saved_certificate(tmp_path, "W7"),
            verification=verification(tmp_path, "W7", "kernel", W7),
        ),
        entry("A", A, a, certifier="branch-and-bound"),
    ]
    record = run_census(tmp_path, entries)
    # W7 excludes 133,152 states in 16,701 orbits, as its kernel receipt says.
    assert record["certified"]["surviving_states"] == 346104 - 133152
    assert record["certified"]["orbits"] == 43593 - 16701
    assert record["entries"][0]["marginal"] == record["entries"][0]["alone"]
    both = record["pending_verified_projection"]
    assert both["surviving_states"] < record["certified"]["surviving_states"]
    assert both["surviving_states"] == (
        record["certified"]["surviving_states"] - record["entries"][1]["marginal"]["states"]
    )
    with pytest.raises(RefusedError, match="evidence"):
        _ = run_census(tmp_path, [entry("W7", W7, w7, status="admitted")])


def test_uncertified_or_control_receipts_are_refused(tmp_path: Path) -> None:
    stall = write_json(
        tmp_path, "stall.json", {**kernel_receipt(W7), "status": "PASS_SAVED_STALL"}
    )
    with pytest.raises(RefusedError, match="closure"):
        _ = run_census(tmp_path, [entry("W7", W7, stall)])
    control = write_json(tmp_path, "control.json", bb_receipt(A, control=True))
    with pytest.raises(RefusedError, match="control"):
        _ = run_census(tmp_path, [entry("A", A, control, certifier="branch-and-bound")])
    budget = write_json(tmp_path, "budget.json", bb_receipt(A, verdict="unresolved-at-budget"))
    with pytest.raises(RefusedError, match="not certified"):
        _ = run_census(tmp_path, [entry("A", A, budget, certifier="branch-and-bound")])


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"verification": None}, "verification must name"),
        ({"status": "FAIL"}, "did not pass"),
        ({"mode": "sample"}, "sample"),
        ({"verifier": "branch-and-bound"}, "not a kernel verification"),
        ({"provenance": None}, "needs the entry's verifier"),
        (
            {"provenance": {"revision": "0" * 40, "dirty": True, "files": {"x.py": "1"}}},
            "uncommitted",
        ),
        ({"certificate": {"seed_sha256": "d" * 64, "node_sha256": NODE}}, "other objects"),
        ({"certificate": {"seed_sha256": SEED}}, "other objects"),
        ({"certificate": None}, "other objects"),
        ({"checked_cells": A}, "another class"),
        ({"certificate_path": None}, "saved certificate"),
    ],
)
def test_an_admitted_entry_needs_its_full_passing_reviewed_verification(
    tmp_path: Path, change: dict[str, Any], message: str
) -> None:
    _ = commit_verifiers(tmp_path, "the reviewed verifier\n")
    receipt = write_json(tmp_path, "w7.json", kernel_receipt(W7))
    fields = {k: v for k, v in change.items() if k != "verification"}
    certificate = fields.pop("certificate_path", saved_certificate(tmp_path, "W7"))
    cells = fields.pop("checked_cells", W7)
    checked = verification(tmp_path, "W7", "kernel", cells, **fields)
    if "verification" in change:
        checked = change["verification"]
    admitted = entry(
        "W7",
        W7,
        receipt,
        status="admitted",
        evidence="review.md",
        certificate=certificate,
        verification=checked,
    )
    with pytest.raises(RefusedError, match=message):
        _ = run_census(tmp_path, [admitted])


def test_an_admitted_branch_and_bound_entry_counts_with_its_verification(
    tmp_path: Path,
) -> None:
    reviewed = commit_verifiers(tmp_path, "the reviewed verifier\n")
    receipt = write_json(tmp_path, "a.json", bb_receipt(A))
    admitted = entry(
        "A",
        A,
        receipt,
        certifier="branch-and-bound",
        status="admitted",
        evidence="review.md",
        certificate=saved_certificate(tmp_path, "A"),
        verification=verification(tmp_path, "A", "branch-and-bound", A),
    )
    record = run_census(tmp_path, [admitted])
    assert record["certified"]["admitted"] == 1
    assert record["certified"]["surviving_states"] == 346104 - 110448
    assert record["certified"]["orbits"] == 43593 - 13897
    assert record["entries"][0]["verification"]["verifier"] == {
        "path": VERIFIERS["branch-and-bound"],
        "revision": reviewed,
        "review": "review.md",
    }


def admitted_w7(root: Path, checked: dict[str, Any]) -> dict[str, Any]:
    return entry(
        "W7",
        W7,
        write_json(root, "w7.json", kernel_receipt(W7)),
        status="admitted",
        evidence="review.md",
        certificate=saved_certificate(root, "W7"),
        verification=checked,
    )


def test_a_verification_counts_at_a_revision_whose_verifier_is_the_reviewed_one(
    tmp_path: Path,
) -> None:
    """A later revision with the verifier's file unchanged counts; an edited verifier does
    not until its revision is listed; a receipt that predates provenance counts by the
    revision the entry names for it, and only such a receipt may name one."""
    reviewed = commit_verifiers(tmp_path, "the reviewed verifier\n")
    _ = commit_verifiers(tmp_path, "the reviewed verifier\n")
    later = admitted_w7(tmp_path, verification(tmp_path, "W7", "kernel", W7))
    assert run_census(tmp_path, [later], [reviewed])["certified"]["admitted"] == 1
    edited = commit_verifiers(tmp_path, "the verifier, edited\n")
    unreviewed = admitted_w7(tmp_path, verification(tmp_path, "W7", "kernel", W7))
    with pytest.raises(RefusedError, match="not a reviewed verifier"):
        _ = run_census(tmp_path, [unreviewed], [reviewed])
    assert run_census(tmp_path, [unreviewed], [reviewed, edited])["certified"]["admitted"] == 1
    named = {"path": VERIFIERS["kernel"], "revision": reviewed}
    legacy = verification(tmp_path, "W7", "kernel", W7, provenance=None)
    record = run_census(tmp_path, [admitted_w7(tmp_path, {**legacy, "verifier": named})])
    assert record["entries"][0]["verification"]["verifier"]["revision"] == reviewed
    both = {**verification(tmp_path, "W7", "kernel", W7), "verifier": named}
    with pytest.raises(RefusedError, match="names none"):
        _ = run_census(tmp_path, [admitted_w7(tmp_path, both)], [reviewed, edited])
    with pytest.raises(RefusedError, match="holds no such file"):
        _ = run_census(tmp_path, [], ["0" * 40])


def test_a_verification_matches_its_certificate_by_object_ids_not_by_directory(
    tmp_path: Path,
) -> None:
    """A certificate directory renamed after its verification still counts, for either
    certifier, because the receipt names the same seed and node (or manifest) ids; a
    verification of other objects is refused wherever it ran."""
    _ = commit_verifiers(tmp_path, "the reviewed verifier\n")
    w7 = write_json(tmp_path, "w7.json", kernel_receipt(W7))
    a = write_json(tmp_path, "a.json", bb_receipt(A))
    checked = {
        "W7": verification(tmp_path, "W7-pending", "kernel", W7),
        "A": verification(tmp_path, "A-pending", "branch-and-bound", A),
    }
    for name in ("W7", "A"):
        _ = saved_certificate(tmp_path, f"{name}-pending")
        (tmp_path / "certificates" / f"{name}-pending").rename(tmp_path / "certificates" / name)
    renamed = [
        entry(
            "W7",
            W7,
            w7,
            status="admitted",
            evidence="review.md",
            certificate="certificates/W7",
            verification=checked["W7"],
        ),
        entry(
            "A",
            A,
            a,
            certifier="branch-and-bound",
            status="admitted",
            evidence="review.md",
            certificate="certificates/A",
            verification=checked["A"],
        ),
    ]
    record = run_census(tmp_path, renamed)
    assert record["certified"]["admitted"] == 2
    assert [row["verification"]["certificate"] for row in record["entries"]] == [
        "certificates/W7",
        "certificates/A",
    ]
    other = {"seed_sha256": SEED, "node_sha256": "e" * 64}
    swapped = {
        **renamed[0],
        "verification": verification(tmp_path, "W7", "kernel", W7, certificate=other),
    }
    with pytest.raises(RefusedError, match="other objects"):
        _ = run_census(tmp_path, [swapped])
    elsewhere = {
        **renamed[1],
        "verification": verification(
            tmp_path, "A", "branch-and-bound", A, certificate={"manifest_sha256": "f" * 64}
        ),
    }
    with pytest.raises(RefusedError, match="other objects"):
        _ = run_census(tmp_path, [elsewhere])


def test_a_listing_with_admits_verifies_only_the_entries_it_names(tmp_path: Path) -> None:
    """An older verifier listing kept to the receipts it already wrote, as the kernel
    listings before the closed-cover fix are: its own entry still counts, a new entry
    verified at it is refused, and the new entry counts once verified at a listing
    without `admits`."""
    kernel = VERIFIERS["kernel"]
    old = commit_verifiers(tmp_path, "the verifier with the zero-area branch\n")
    first = admitted_w7(tmp_path, verification(tmp_path, "W7", "kernel", W7))
    late = entry(
        "A",
        A,
        write_json(tmp_path, "a-kernel.json", kernel_receipt(A)),
        status="admitted",
        evidence="review.md",
        certificate=saved_certificate(tmp_path, "A"),
        verification=verification(tmp_path, "A", "kernel", A),
    )
    fixed = commit_verifiers(tmp_path, "the verifier with exact closed covers\n")
    listings = [
        {"path": kernel, "revision": old, "review": "review.md", "admits": ["W7"]},
        {"path": kernel, "revision": fixed, "review": "review.md"},
    ]
    assert run_census(tmp_path, [first], listings=listings)["certified"]["admitted"] == 1
    with pytest.raises(RefusedError, match=r"'A'.*reviewed only for other entries.*admits W7"):
        _ = run_census(tmp_path, [first, late], listings=listings)
    late["verification"] = verification(tmp_path, "A", "kernel", A)
    both = run_census(tmp_path, [first, late], listings=listings)
    assert both["certified"]["admitted"] == 2
    assert [row["verification"]["verifier"]["revision"] for row in both["entries"]] == [
        old,
        fixed,
    ]
    closed = [{**listings[0], "admits": []}, listings[1]]
    with pytest.raises(RefusedError, match=r"'W7'.*admits no entry"):
        _ = run_census(tmp_path, [first], listings=closed)
    for malformed in ("W7", [None], None):
        with pytest.raises(RefusedError, match="admits must be a list"):
            _ = run_census(tmp_path, [first], listings=[{**listings[0], "admits": malformed}])
    with pytest.raises(RefusedError, match="verifiers must be a list"):
        _ = run_census(tmp_path, [first], listings=[{**listings[0], "scope": ["W7"]}])


def test_the_committed_ledger_still_counts_its_four_admitted_entries() -> None:
    """W7, A, SW9 and N1 still count once the kernel listings before the closed-cover fix
    admit only them. Reads the repository's history, as the census does."""
    record = census(REPO / DEFAULT_LEDGER, selector_receipts=())
    admitted = {row["name"] for row in record["entries"] if row["status"] == "admitted"}
    assert {"W7", "A", "SW9", "N1"} <= admitted
    assert record["certified"]["admitted"] == len(admitted)
    assert record["certified"]["endpoint_survives"]
