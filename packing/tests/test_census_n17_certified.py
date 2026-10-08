"""Controls for the n17 certified census: what it refuses, what it counts, and its data.

Every fixture lives in a temporary directory that is not a Git checkout: the census reads
no history (OR-18). Hosted certificate objects are listed in a fabricated manifest in the
hosted-data contract (`sqpack.hosted_data`) and, where a test needs them in place, written
at their paths.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from devtools.census_n17_certified import (
    BB_CERTIFIED,
    BB_SCHEMA,
    CENSUS,
    DEFAULT_LEDGER,
    DEFAULT_SELECTOR_RECEIPTS,
    DESIGN,
    KERNEL_FRAME,
    LEDGER_SCHEMA,
    PILOTS,
    REPO,
    VERIFICATION_SCHEMA,
    RefusedError,
    census,
    class_mask,
    cover_context,
    flagged_classes,
    hosted_files,
    main,
)
from devtools.select_n17_sub_patterns import SCHEMA as SELECTOR_SCHEMA
from sqpack.hosted_data import CONTRACT, fetch_command
from sqpack.yamlio import load_yaml

W7 = ["corner-SW", "side-N0", "side-W0", "side-W1", "side-W2", "interior-SW", "interior-W"]
A = ["interior-SW", "interior-NW", "interior-W", "interior-S", "interior-N", "interior-SE"]
VERIFIERS = {"kernel": "tools/verify_kernel.py", "branch-and-bound": "tools/verify_bb.py"}
LISTINGS = {"kernel": "kernel-v1", "branch-and-bound": "bb-v1"}
MANIFEST = "hosted.yaml"
HOSTED_HEAD = {
    "softschema": {
        "contract": CONTRACT,
        "schema": "hosted-data.schema.yaml",
        "status": "enforced",
    },
    "repository": "jlevy/squares",
    "tag": "data/census-fixture-v1",
}
EXP250_CENSUS = (
    REPO
    / "packing/campaign/series/series-000-smoke-and-calibration/results"
    / "exp-250-n17-standing-verifier-admissions/census.json"
)
RECHECK = f"{PILOTS}/receipts/selector-recheck-90-seed1.json"
EARLIER_FLAGS = (
    f"{PILOTS}/receipts/selector-arity7-seed1.json",
    f"{PILOTS}/receipts/selector-arity8-seed1-restricted.json",
)
EXP250_ADMITTED = {"W7", "A", "SW9", "N1"}


def ids(name: str) -> dict[str, str]:
    """The content ids of entry `name`'s fabricated certificate objects."""
    return {
        kind: hashlib.sha256(f"{kind} {name}".encode()).hexdigest()
        for kind in ("seed", "node", "manifest")
    }


def write_json(root: Path, name: str, document: dict[str, Any]) -> str:
    """A fabricated receipt under the root: its relative path."""
    path = root / "receipts" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    _ = path.write_text(json.dumps(document), encoding="utf-8")
    return f"receipts/{name}"


def kernel_receipt(cells: list[str], name: str = "W7") -> dict[str, Any]:
    return {
        "status": "PASS_SAVED_CLOSED",
        "cells": cells,
        "frame": KERNEL_FRAME,
        "seed_sha256": ids(name)["seed"],
        "node_sha256": ids(name)["node"],
    }


def bb_receipt(cells: list[str], name: str = "A", **extra: Any) -> dict[str, Any]:
    return {
        "schema": BB_SCHEMA,
        "design": DESIGN,
        "pattern": cells,
        "verdict": BB_CERTIFIED,
        "control": False,
        "certificate_manifest": ids(name)["manifest"],
        **extra,
    }


def object_files(name: str, certifier: str) -> list[str]:
    named = ids(name)
    if certifier == "kernel":
        return [f"seed-{named['seed']}.json.gz", f"node-{named['node']}.json.gz"]
    return [f"{named['manifest']}.json.gz"]


def bare_directory(root: Path, directory: str) -> str:
    """A certificate directory holding only its small files."""
    path = root / "certificates" / directory
    path.mkdir(parents=True, exist_ok=True)
    _ = (path / "README.txt").write_text("objects hosted elsewhere\n", encoding="utf-8")
    return f"certificates/{directory}"


def payload(file_name: str) -> bytes:
    """The fabricated bytes of a hosted object."""
    return f"object {file_name}\n".encode()


def saved_certificate(
    root: Path, directory: str, name: str | None = None, certifier: str = "kernel"
) -> str:
    """A certificate directory whose objects the root's hosted-data manifest lists; the
    objects are not placed."""
    declared = bare_directory(root, directory)
    manifest = root / MANIFEST
    document = (
        json.loads(manifest.read_text(encoding="utf-8"))
        if manifest.exists()
        else {**HOSTED_HEAD, "objects": []}
    )
    listed = {item["path"] for item in document["objects"]}
    for file_name in object_files(name or directory, certifier):
        if f"{declared}/{file_name}" in listed:
            continue
        document["objects"].append(
            {
                "path": f"{declared}/{file_name}",
                "asset": file_name,
                "size": len(payload(file_name)),
                "sha256": hashlib.sha256(payload(file_name)).hexdigest(),
            }
        )
    _ = manifest.write_text(json.dumps(document), encoding="utf-8")  # JSON is YAML
    return declared


def verification(
    root: Path, directory: str, certifier: str, cells: list[str], **extra: Any
) -> dict[str, Any]:
    """A fabricated full, passing verification receipt from the listed verifier, of the
    objects `saved_certificate` lists for the entry named by the directory's first part,
    recording that it ran in that directory; the entry's `verification` field."""
    named = ids(directory.split("-", maxsplit=1)[0])
    kernel = certifier == "kernel"
    objects = (
        {"seed_sha256": named["seed"], "node_sha256": named["node"]}
        if kernel
        else {"manifest_sha256": named["manifest"]}
    )
    document = {
        "schema": VERIFICATION_SCHEMA,
        "verifier": certifier,
        "provenance": {"revision": "r1", "dirty": False, "files": {VERIFIERS[certifier]: "0"}},
        "directory": f"certificates/{directory}",
        "certificate": objects,
        "status": "PASS",
        "mode": "full",
        "cells" if kernel else "pattern": cells,
        **extra,
    }
    receipt = write_json(root, f"verify-{directory}-{certifier}.json", document)
    return {"receipt": receipt, "verifier": LISTINGS[certifier]}


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


def default_listings() -> list[dict[str, Any]]:
    return [
        {
            "id": LISTINGS[certifier],
            "certifier": certifier,
            "path": path,
            "version": "1",
            "review": "review.md",
        }
        for certifier, path in VERIFIERS.items()
    ]


def run_census(
    root: Path,
    entries: list[dict[str, Any]],
    listings: list[dict[str, Any]] | None = None,
    **options: Any,
) -> dict[str, Any]:
    """The census of the entries under the listings (by default one per certifier), with
    the root's manifest when one was written."""
    for path in VERIFIERS.values():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        _ = (root / path).write_text("the reviewed verifier\n", encoding="utf-8")
    _ = (root / "review.md").write_text("admits the verifiers\n", encoding="utf-8")
    ledger = root / "ledger.yaml"
    document: dict[str, Any] = {
        "schema": LEDGER_SCHEMA,
        "design": DESIGN,
        "verifiers": default_listings() if listings is None else listings,
        "entries": entries,
    }
    if (root / MANIFEST).exists():
        document["data_manifest"] = MANIFEST
    _ = ledger.write_text(json.dumps(document), encoding="utf-8")  # JSON is YAML
    return census(ledger, root=root, selector_receipts=(), **options)


def admitted_w7(root: Path, checked: dict[str, Any] | None = None) -> dict[str, Any]:
    return entry(
        "W7",
        W7,
        write_json(root, "w7.json", kernel_receipt(W7)),
        status="admitted",
        evidence="review.md",
        certificate=saved_certificate(root, "W7"),
        verification=checked or verification(root, "W7", "kernel", W7),
    )


def admitted_a(root: Path) -> dict[str, Any]:
    return entry(
        "A",
        A,
        write_json(root, "a.json", bb_receipt(A)),
        certifier="branch-and-bound",
        status="admitted",
        evidence="review.md",
        certificate=saved_certificate(root, "A", certifier="branch-and-bound"),
        verification=verification(root, "A", "branch-and-bound", A),
    )


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


def test_only_admitted_entries_are_counted_and_need_no_hosted_bytes(tmp_path: Path) -> None:
    a = write_json(tmp_path, "a.json", bb_receipt(A))
    entries = [admitted_w7(tmp_path), entry("A", A, a, certifier="branch-and-bound")]
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
    # The count rests on the receipts; the objects are hosted and not in place.
    assert record["entries"][0]["certificate_data"]["local"] == "absent"
    assert record["data"]["certificates_not_in_place"] == 1
    assert record["data"]["full_recheck"] == (
        f"run {fetch_command(tmp_path / MANIFEST)} from packing/"
    )
    assert "python -m devtools.hosted_data fetch --manifest " in record["data"]["full_recheck"]
    receipt = entries[0]["receipt"]
    with pytest.raises(RefusedError, match="evidence"):
        _ = run_census(tmp_path, [entry("W7", W7, receipt, status="admitted")])


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


W7_IDS = ids("W7")


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"verification": None}, "verification must name"),
        ({"status": "FAIL"}, "did not pass"),
        ({"mode": "sample"}, "sample"),
        ({"verifier": "branch-and-bound"}, "not a kernel verification"),
        ({"listing": None}, "names no listed verifier"),
        ({"listing": "kernel-v9"}, "names no listed verifier"),
        ({"listing": "bb-v1"}, "checks branch-and-bound"),
        (
            {
                "provenance": {
                    "revision": "r1",
                    "dirty": True,
                    "files": {VERIFIERS["kernel"]: "1"},
                }
            },
            "uncommitted",
        ),
        (
            {"provenance": {"revision": "r1", "dirty": False, "files": {"tools/x.py": "1"}}},
            r"ran tools/x\.py, not tools/verify_kernel\.py",
        ),
        (
            {"certificate": {"seed_sha256": "d" * 64, "node_sha256": W7_IDS["node"]}},
            "other objects",
        ),
        ({"certificate": {"seed_sha256": W7_IDS["seed"]}}, "other objects"),
        ({"certificate": None}, "other objects"),
        ({"checked_cells": A}, "another class"),
        ({"certificate_path": None}, "saved certificate"),
        ({"unlisted": True}, "lists no seed-"),
    ],
)
def test_an_admitted_entry_needs_its_full_passing_reviewed_verification(
    tmp_path: Path, change: dict[str, Any], message: str
) -> None:
    receipt = write_json(tmp_path, "w7.json", kernel_receipt(W7))
    special = {"verification", "listing", "checked_cells", "certificate_path", "unlisted"}
    fields = {k: v for k, v in change.items() if k not in special}
    directory = bare_directory(tmp_path, "W7") if change.get("unlisted") else None
    certificate = change.get("certificate_path", directory or saved_certificate(tmp_path, "W7"))
    checked: Any = verification(
        tmp_path, "W7", "kernel", change.get("checked_cells", W7), **fields
    )
    if "listing" in change:
        checked["verifier"] = change["listing"]
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
    record = run_census(tmp_path, [admitted_a(tmp_path)])
    assert record["certified"]["admitted"] == 1
    assert record["certified"]["surviving_states"] == 346104 - 110448
    assert record["certified"]["orbits"] == 43593 - 13897
    assert record["entries"][0]["verification"]["verifier"] == {
        "id": "bb-v1",
        "path": VERIFIERS["branch-and-bound"],
        "version": "1",
        "review": "review.md",
    }
    assert record["entries"][0]["verification"]["ran_at"] == "r1"


def test_a_verification_counts_under_the_listing_its_entry_names(tmp_path: Path) -> None:
    """The listing is named, not looked up in history: a receipt without provenance counts
    under the listing its entry names; one whose provenance names another file than the
    listing's is refused; listings need distinct ids, a known certifier and files that
    exist. None of it needs Git."""
    assert not (tmp_path / ".git").exists()
    legacy = verification(tmp_path, "W7", "kernel", W7, provenance=None)
    record = run_census(tmp_path, [admitted_w7(tmp_path, legacy)])
    assert record["entries"][0]["verification"]["ran_at"] is None
    assert record["entries"][0]["verification"]["verifier"]["id"] == "kernel-v1"
    second = {**default_listings()[0], "id": "kernel-v2", "path": "tools/verify_kernel_2.py"}
    (tmp_path / second["path"]).write_text("the rewritten verifier\n", encoding="utf-8")
    moved = {**verification(tmp_path, "W7", "kernel", W7), "verifier": "kernel-v2"}
    with pytest.raises(RefusedError, match=r"ran tools/verify_kernel\.py, not"):
        _ = run_census(tmp_path, [admitted_w7(tmp_path, moved)], [*default_listings(), second])
    for broken, message in (
        ({**second, "id": "kernel-v1"}, "distinct"),
        ({**second, "certifier": "lattice"}, "certifier"),
        ({**second, "path": "tools/missing.py"}, "does not exist"),
        ({**second, "revision": "abc"}, "verifiers must be a list"),
    ):
        with pytest.raises(RefusedError, match=message):
            _ = run_census(tmp_path, [], [*default_listings(), broken])


def test_a_verification_matches_its_certificate_by_object_ids_not_by_directory(
    tmp_path: Path,
) -> None:
    """A certificate whose verification ran in another directory still counts, for either
    certifier, because the receipt names the same seed and node (or manifest) ids; a
    verification of other objects is refused wherever it ran."""
    w7 = write_json(tmp_path, "w7.json", kernel_receipt(W7))
    a = write_json(tmp_path, "a.json", bb_receipt(A))
    checked = {
        "W7": verification(tmp_path, "W7-pending", "kernel", W7),
        "A": verification(tmp_path, "A-pending", "branch-and-bound", A),
    }
    renamed = [
        entry(
            "W7",
            W7,
            w7,
            status="admitted",
            evidence="review.md",
            certificate=saved_certificate(tmp_path, "W7"),
            verification=checked["W7"],
        ),
        entry(
            "A",
            A,
            a,
            certifier="branch-and-bound",
            status="admitted",
            evidence="review.md",
            certificate=saved_certificate(tmp_path, "A", certifier="branch-and-bound"),
            verification=checked["A"],
        ),
    ]
    record = run_census(tmp_path, renamed)
    assert record["certified"]["admitted"] == 2
    assert [row["verification"]["certificate"] for row in record["entries"]] == [
        "certificates/W7",
        "certificates/A",
    ]
    other = {"seed_sha256": W7_IDS["seed"], "node_sha256": "e" * 64}
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
    verified under it is refused, and the new entry counts once verified under a listing
    without `admits`."""
    base = default_listings()[0]
    old = {**base, "id": "kernel-old", "admits": ["W7"]}
    fixed = {**base, "id": "kernel-fixed"}
    listings = [old, fixed]
    first = admitted_w7(
        tmp_path, {**verification(tmp_path, "W7", "kernel", W7), "verifier": "kernel-old"}
    )
    late = entry(
        "A",
        A,
        write_json(tmp_path, "a-kernel.json", kernel_receipt(A, "A")),
        status="admitted",
        evidence="review.md",
        certificate=saved_certificate(tmp_path, "A"),
        verification={**verification(tmp_path, "A", "kernel", A), "verifier": "kernel-old"},
    )
    assert run_census(tmp_path, [first], listings)["certified"]["admitted"] == 1
    with pytest.raises(RefusedError, match=r"'A'.*reviewed only for other entries.*admits W7"):
        _ = run_census(tmp_path, [first, late], listings)
    late["verification"] = {**late["verification"], "verifier": "kernel-fixed"}
    both = run_census(tmp_path, [first, late], listings)
    assert both["certified"]["admitted"] == 2
    assert [row["verification"]["verifier"]["id"] for row in both["entries"]] == [
        "kernel-old",
        "kernel-fixed",
    ]
    closed = [{**old, "admits": []}, fixed]
    with pytest.raises(RefusedError, match=r"'W7'.*admits no entry"):
        _ = run_census(tmp_path, [first], closed)
    for malformed in ("W7", [None], None):
        with pytest.raises(RefusedError, match="admits must be a list"):
            _ = run_census(tmp_path, [first], [{**old, "admits": malformed}, fixed])


def test_objects_in_place_are_reported_and_one_of_another_size_is_refused(
    tmp_path: Path,
) -> None:
    """The census never downloads: objects written at their paths read as in place, the
    count is the same either way, and a file whose size is not the manifest's is refused
    before anything counts."""
    entries = [admitted_w7(tmp_path), admitted_a(tmp_path)]
    before = run_census(tmp_path, entries)
    assert before["data"]["certificates_not_in_place"] == 2
    for item in json.loads((tmp_path / MANIFEST).read_text(encoding="utf-8"))["objects"]:
        _ = (tmp_path / item["path"]).write_bytes(payload(item["asset"]))
    after = run_census(tmp_path, entries)
    assert after["data"]["full_recheck"] == "the hosted files are in place"
    assert {row["certificate_data"]["local"] for row in after["entries"]} == {"present"}
    assert after["certified"] == before["certified"]
    placed = tmp_path / "certificates/W7" / object_files("W7", "kernel")[0]
    _ = placed.write_bytes(b"truncated")
    with pytest.raises(RefusedError, match="differs from its manifest"):
        _ = run_census(tmp_path, entries)
    _ = placed.write_bytes(b"x" * len(payload(placed.name)))  # the size, other bytes
    with pytest.raises(RefusedError, match=r"differs from its manifest \(sha256"):
        _ = run_census(tmp_path, entries)
    placed.unlink()
    partial = run_census(tmp_path, entries)
    assert partial["entries"][0]["certificate_data"]["local"] == "partial"


def test_the_cli_names_the_fetch_command_when_objects_are_absent(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _ = run_census(tmp_path, [admitted_w7(tmp_path)])
    flags = {"schema": SELECTOR_SCHEMA, "design": DESIGN, "flagged": []}
    receipt = write_json(tmp_path, "f.json", flags)
    command = ["--root", str(tmp_path), "--selector-receipt", receipt]
    assert main([*command, "--ledger", "ledger.yaml"]) == 0
    captured = capsys.readouterr()
    assert json.loads(captured.out)["certified"]["admitted"] == 1
    assert fetch_command(tmp_path / MANIFEST) in captured.err
    assert main([*command, "--ledger", "missing.yaml"]) == 2
    assert "does not exist" in json.loads(capsys.readouterr().out)["refused"]


def test_the_manifest_is_refused_unless_it_meets_the_hosted_data_contract(
    tmp_path: Path,
) -> None:
    """The census reads its manifest through `sqpack.hosted_data`, so a manifest outside
    the contract refuses the count, as does an object listed twice."""
    good = {
        "path": "certificates/W7/x.json.gz",
        "asset": "x.json.gz",
        "size": 1,
        "sha256": "a" * 64,
        "description": "optional",
    }
    ledger = {"data_manifest": MANIFEST}
    bare = {key: value for key, value in HOSTED_HEAD.items() if key != "softschema"}
    for document, message in (
        ({**HOSTED_HEAD, "objects": [{**good, "size": -1}]}, "minimum"),
        ({**HOSTED_HEAD, "objects": [{**good, "sha256": "A" * 64}]}, "does not match"),
        ({**HOSTED_HEAD, "objects": [{**good, "path": "/abs/x.json.gz"}]}, "does not match"),
        ({**HOSTED_HEAD, "objects": [{**good, "url": "https://x"}]}, "url"),
        ({**HOSTED_HEAD, "objects": [good, good]}, "listed twice"),
        ({**HOSTED_HEAD, "tag": "data-test-v1", "objects": [good]}, "does not match"),
        ({**bare, "objects": [good]}, "softschema.contract missing"),
        ({**HOSTED_HEAD, "objects": {}}, "array"),
    ):
        _ = (tmp_path / MANIFEST).write_text(json.dumps(document), encoding="utf-8")
        with pytest.raises(RefusedError, match=f"data_manifest {MANIFEST}: .*{message}"):
            _ = hosted_files(tmp_path, ledger)
    _ = (tmp_path / MANIFEST).write_text(
        json.dumps({**HOSTED_HEAD, "objects": [good]}), encoding="utf-8"
    )
    hosted = hosted_files(tmp_path, ledger)
    assert hosted.manifest == tmp_path / MANIFEST
    assert hosted.objects["certificates/W7/x.json.gz"].size == 1
    assert hosted_files(tmp_path, {}).objects == {}


@pytest.fixture(scope="module")
def committed_census_without_flags() -> dict[str, Any]:
    """The bare committed census shared by its two read-only consumers."""
    return census(REPO / DEFAULT_LEDGER, selector_receipts=())


def test_the_committed_ledger_counts_its_four_admitted_entries_without_the_dumps(
    committed_census_without_flags: dict[str, Any],
) -> None:
    """W7, A, SW9 and N1 count from the committed receipts whether or not the hosted
    certificate objects are in place, to exp-250's census."""
    record = committed_census_without_flags
    admitted = {row["name"] for row in record["entries"] if row["status"] == "admitted"}
    assert {"W7", "A", "SW9", "N1"} <= admitted
    assert record["certified"]["admitted"] == len(admitted)
    assert record["certified"]["endpoint_survives"]
    retained = json.loads(EXP250_CENSUS.read_text(encoding="utf-8"))
    if admitted == {"W7", "A", "SW9", "N1"}:
        assert record["certified"] == retained["certified"]
    # Session 182 staged the seeds and nodes of its admitted certificates (exp-251,
    # exp-252): 92 files and 112,285,110 bytes before them.
    assert record["data"]["files"] == 200
    assert record["data"]["bytes"] == 2_135_600_454


def exp250_ledger(tmp_path: Path) -> Path:
    """The committed ledger cut to the four entries exp-250 admitted, so that a later
    admission does not move the projection pinned here."""
    document = load_yaml((REPO / DEFAULT_LEDGER).read_text(encoding="utf-8"))
    document["entries"] = [e for e in document["entries"] if e["name"] in EXP250_ADMITTED]
    ledger = tmp_path / "ledger.yaml"
    _ = ledger.write_text(json.dumps(document), encoding="utf-8")  # JSON is YAML
    return ledger


def test_the_census_projects_the_recheck_flags_by_default(tmp_path: Path) -> None:
    """The recheck leaves 89 classes flagged, two of which the ledger admits: 87 projected
    flags, whose certification would leave 17,168 states in 2,197 orbits with the
    endpoint's state among them. The certified line stays exp-250's."""
    assert DEFAULT_SELECTOR_RECEIPTS == (RECHECK,)
    record = census(exp250_ledger(tmp_path))
    admitted = {row["name"] for row in record["entries"] if row["status"] == "admitted"}
    assert admitted == EXP250_ADMITTED
    flagged = record["flagged_uncertified"]
    assert flagged["selector_receipts"] == [RECHECK]
    assert len(flagged["classes"]) == 87
    assert {row["selector_receipt"] for row in flagged["classes"]} == {RECHECK}
    assert flagged["all_certified_projection"] == {
        "surviving_states": 17168,
        "orbits": 2197,
        "endpoint_survives": True,
    }
    retained = json.loads(EXP250_CENSUS.read_text(encoding="utf-8"))
    assert record["certified"] == retained["certified"]
    assert record["certified"]["endpoint_survives"]


def test_the_committed_ledger_projects_the_recheck_flags_it_has_not_admitted(
    committed_census_without_flags: dict[str, Any],
) -> None:
    """At the committed ledger, the projected flags are the recheck's 89 less those the
    ledger admits, the flags leave the certified line as the census gives it without
    them, and the endpoint survives. While every admitted class beyond exp-250's four is
    a flag, certifying all flags still leaves 17,168 states in 2,197 orbits. With lane
    K's s182-k1 admitted (exp-251) that is 86 flags over 102,124 certified states in
    12,929 orbits."""
    record = census(REPO / DEFAULT_LEDGER)
    bare = committed_census_without_flags
    assert record["certified"] == bare["certified"]
    assert record["certified"]["endpoint_survives"]
    cover = cover_context()
    flags = set(flagged_classes(cover, REPO, (RECHECK,)))
    admitted = {
        row["name"]: class_mask(cover, row["cells"], row["name"])
        for row in record["entries"]
        if row["status"] == "admitted"
    }
    projected = record["flagged_uncertified"]
    assert (
        len(projected["classes"])
        == len(flags - set(admitted.values()))
        == 89 - len({mask for mask in admitted.values() if mask in flags})
    )
    if {name for name, mask in admitted.items() if mask not in flags} <= EXP250_ADMITTED:
        assert projected["all_certified_projection"] == {
            "surviving_states": 17168,
            "orbits": 2197,
            "endpoint_survives": True,
        }
    if set(admitted) == {*EXP250_ADMITTED, "s182-k1"}:
        assert record["certified"] == {
            "admitted": 5,
            "surviving_states": 102124,
            "orbits": 12929,
            "endpoint_survives": True,
        }
        assert len(projected["classes"]) == 86


def test_a_recheck_withdraws_the_class_it_placed_from_earlier_flags(tmp_path: Path) -> None:
    """The earlier sweeps flagged 90 classes; the recheck placed one arity-8 class, and read
    after them it withdraws that class, leaving its own 89. Any other schema is refused."""
    cover = cover_context()
    earlier = flagged_classes(cover, REPO, EARLIER_FLAGS)
    rechecked = flagged_classes(cover, REPO, (RECHECK,))
    both = flagged_classes(cover, REPO, (*EARLIER_FLAGS, RECHECK))
    assert (len(earlier), len(rechecked)) == (90, 89)
    assert set(both) == set(rechecked) < set(earlier)
    (placed,) = set(earlier) - set(rechecked)
    assert placed.bit_count() == 8
    assert {row["selector_receipt"] for row in both.values()} == {RECHECK}
    other = write_json(tmp_path, "other.json", {"schema": "other/v1", "design": DESIGN})
    with pytest.raises(RefusedError, match="not a selector or recheck receipt"):
        _ = flagged_classes(cover, tmp_path, [other])
