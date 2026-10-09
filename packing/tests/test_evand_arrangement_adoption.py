"""Complete new-pose adoption, preserved history and exact private atlas custody."""

from __future__ import annotations

import copy
import json
import lzma
import shutil
import subprocess
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from devtools import build_known_best_atlas as atlas
from devtools import check_results
from devtools import evand_arrangement_houses as houses
from devtools import evand_arrangement_reports as reports
from devtools import register_evand_arrangements as adoption
from devtools import run_negative_controls as controls
from sqpack.witness import witness_document
from sqpack.yamlio import safe_load
from tests.test_negative_controls import index_fixture_source

SOURCE = reports.REPO


@pytest.fixture
def private(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    tree = tmp_path / "private"
    packet = tree / reports.PACKET.relative_to(SOURCE)
    for path in houses.private_input_paths():
        target = tree / path.relative_to(SOURCE)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    for n in reports.NUMBERS:
        target = tree / houses.house_path(n).relative_to(SOURCE)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(houses.house_path(n))
    monkeypatch.setattr(reports, "REPO", tree)
    monkeypatch.setattr(reports, "PACKET", packet)
    monkeypatch.setattr(houses, "REPO", tree)
    return tree


@pytest.mark.parametrize("n", reports.NUMBERS)
def test_exact_new_pose_adoption_preserves_historical_case_and_is_idempotent(n: int) -> None:
    prior = reports.read_xz(reports.PACKET / "acquisition/prior-state.json.xz")
    original = next(row["complete_case"] for row in prior if row["n"] == n)
    adopted = adoption.adopt_case(n, original)
    case = safe_load(adopted.split("---\n", 2)[1])["packing"]
    old = safe_load(original.split("---\n", 2)[1])["packing"]
    assert Decimal(case["verified_upper_bound"]["value"]) < Decimal(
        old["verified_upper_bound"]["value"]
    )
    assert case["reported_upper_bound"]["exact_form"] == reports.legacy.literal(
        reports.read_fact(n).side
    )
    assert case["reported_lower_bound"] == old["reported_lower_bound"]
    assert case["verified_lower_bound"] == old["verified_lower_bound"]
    assert case["rigidity"] is None
    assert case["conjectured_optimum"] is None
    assert set(old["evidence"]) <= set(case["evidence"])
    assert all(resource in case["resources"] for resource in old["resources"])
    assert old["reported_upper_bound"]["value"] in str(case["priority_notes"])
    assert adoption.adopt_case(n, adopted) == adopted
    assert "earlier #375" in adopted


def test_generator_preserves_new_geometry_and_adopts_ordinary_lower_lane() -> None:
    n = 266
    existing = (SOURCE / "packing/frontier/n-266.md").read_text()
    document = safe_load(existing.split("---\n", 2)[1])
    document["packing"]["verified_lower_bound"] = {
        "value": "16",
        "exact_form": "16",
        "evidence": ["E-area-lower"],
    }
    generated = (
        "---\n" + adoption.registry.dump(document) + "---\n" + existing.split("---\n", 2)[2]
    )
    result = adoption.adopt_case(n, existing, generated)
    case = safe_load(result.split("---\n", 2)[1])["packing"]
    assert case["verified_lower_bound"]["value"] == "16"
    assert case["reported_upper_bound"]["exact_form"] == reports.legacy.literal(
        reports.read_fact(n).side
    )
    assert case["verified_upper_bound"] == reports.confirmed_bound(n)


def test_actual_houses_bind_every_complete_input_and_native_field(private: Path) -> None:
    assert private == reports.REPO
    houses.check_houses()
    row = reports.check_certification()[266]
    expected = houses.expected_house(reports.read_fact(266), row)
    assert len(expected["squares"]) == 266
    assert expected["certificate"]["result"]["pairs_tested"] == 35245
    assert expected["source"]["path"].startswith("packing/")
    assert (
        houses.linked_house_problem(
            "packing/witnesses/known-best/n-266.yaml", repository=private
        )
        is None
    )
    assert (
        houses.linked_house_problem(
            "packing/witnesses/known-best/n-267.yaml", repository=private
        )
        is not None
    )


@pytest.mark.parametrize(
    "change", ["last-pose", "side", "source", "claim", "native-minimum", "native-limitations"]
)
def test_individual_linked_leaf_mutation_is_refused(
    private: Path, tmp_path: Path, change: str
) -> None:
    assert private == reports.REPO
    witness = houses.house.bounded_house(houses.house_path(266))
    if change == "last-pose":
        witness["squares"][-1]["corners"][0][0] = "0"
    elif change == "side":
        witness["side"] = "17"
    elif change == "source":
        witness["source"]["key"] = "[wrong]"
    elif change == "claim":
        witness["claim"]["limitations"] = "Globally optimal."
    elif change == "native-minimum":
        witness["certificate"]["result"]["minimum_best_pair_gap"] = "1"
    else:
        witness["certificate"]["result"]["limitations"] = "Globally optimal."
    changed = tmp_path / "changed.yaml"
    changed.write_text(witness_document(witness, schema="../witness.schema.yaml"))
    houses.house_path(266).unlink()
    houses.house_path(266).symlink_to(changed)
    houses.check_houses([270])
    with pytest.raises(reports.ReportError, match="geometry or metadata"):
        houses.check_houses([266])


def test_each_standalone_call_rereads_private_receipt_and_full_facts(private: Path) -> None:
    assert private == reports.REPO
    houses.check_houses([266])
    record = reports.read_xz(reports.receipt_path())
    changed = copy.deepcopy(record)
    changed["cases"][-1]["checker_input"]["poses"][-1][2] = "1"
    reports.save_xz(reports.receipt_path(), changed)
    with pytest.raises(reports.ReportError):
        houses.check_houses([266])
    reports.save_xz(reports.receipt_path(), record)
    houses.check_houses([266])
    facts = reports.read_xz(reports.fact_path())
    facts["cases"][-1]["source_certificate"] += "\n1 1 0\n"
    reports.save_xz(reports.fact_path(), facts)
    with pytest.raises(reports.ReportError):
        houses.check_houses([266])


def test_all_house_producers_refuse_before_writing(private: Path) -> None:
    assert private == reports.REPO
    before = houses.house_path(266).read_bytes()
    for producer in (
        lambda: houses.guard_house_outputs([266]),
        lambda: atlas.update_selected([266]),
        atlas.update,
    ):
        with pytest.raises(ValueError, match="escapes"):
            producer()
        assert houses.house_path(266).read_bytes() == before


def test_unrelated_private_root_rejects_lexical_house_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(check_results, "REPO", tmp_path)
    for n in reports.NUMBERS:
        problem = check_results.linked_repository_file_problem(
            f"packing/witnesses/known-best/n-{n:03d}.yaml"
        )
        assert problem is not None
        assert problem == "linked house requires its complete private selected frontier"


def test_actual_snapshot_preserves_separate_alias_destinations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source"
    packing = source / "packing"
    packing.mkdir(parents=True)
    first, alias = packing / "first", packing / "alias"
    first.write_bytes(b"complete source bytes")
    alias.symlink_to(first)
    index_fixture_source(source)
    monkeypatch.setattr(controls, "REPO", source)
    monkeypatch.setattr(controls, "ROOT", packing)
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", ())
    monkeypatch.setattr(controls, "COPY_SEPARATELY", (first, alias))
    monkeypatch.setattr(controls, "PRUNE", frozenset({first, alias}))
    monkeypatch.setattr(controls, "root_files", lambda: ())
    monkeypatch.setattr(controls, "snapshot_pruned_targets", lambda: [first, alias])
    monkeypatch.setattr(controls, "linked_pruned_directories", list)
    monkeypatch.setattr(controls, "LINK_BACK", ())
    monkeypatch.setattr(
        controls, "_clone_into", lambda _source, target: target.mkdir(parents=True)
    )
    before = first.read_bytes()
    assert controls.snapshot_source_bytes() == 2 * len(before)
    assert controls.snapshot_duplicate_copy_bytes() == 2 * len(before)
    tree = tmp_path / "private"
    controls.clone_tree(tree)
    copied_first, copied_alias = tree / "packing/first", tree / "packing/alias"
    assert copied_first.read_bytes() == before
    assert copied_alias.read_bytes() == before
    assert not copied_alias.is_symlink()
    copied_alias.write_bytes(b"private mutation")
    assert copied_first.read_bytes() == before
    assert first.read_bytes() == before


def test_snapshot_deduplicates_only_identical_declared_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    first, alias, rescued = (tmp_path / name for name in ("first", "alias", "rescued"))
    monkeypatch.setattr(controls, "COPY_SEPARATELY", (first, alias))
    monkeypatch.setattr(controls, "root_files", lambda: (first,))
    monkeypatch.setattr(controls, "snapshot_pruned_targets", lambda: [rescued, alias])
    assert controls.snapshot_copy_targets() == (first, alias, rescued)
    monkeypatch.setattr(
        controls, "snapshot_pruned_targets", lambda: [rescued, tmp_path / "new"]
    )
    assert controls.snapshot_copy_targets() == (first, alias, rescued, tmp_path / "new")


@pytest.mark.slow
def test_production_clone_copies_every_scientific_input_and_admits_exact_links(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert set(houses.private_input_paths()) <= set(controls.COPY_SEPARATELY)
    assert controls.snapshot_source_bytes() <= controls.SNAPSHOT_MAX_BYTES
    tree = tmp_path / "worker"
    scientific = houses.private_input_paths()
    copied_sources: list[Path] = []
    original_copy = controls.shutil.copy2

    def counted_copy(source: Any, destination: Any, **kwargs: Any) -> Any:
        path = Path(source)
        if path in scientific:
            copied_sources.append(path)
        return original_copy(source, destination, **kwargs)

    monkeypatch.setattr(controls.shutil, "copy2", counted_copy)
    controls.clone_tree(tree)
    assert all(copied_sources.count(path) == 1 for path in scientific)
    for path in houses.private_input_paths():
        copied = tree / path.relative_to(SOURCE)
        assert copied.is_file()
        assert not copied.is_symlink()
        assert copied.read_bytes() == path.read_bytes()
    env = controls.control_environment(tree, tmp_path / "pycache")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from devtools.evand_arrangement_houses import check_houses; check_houses()",
        ],
        cwd=tree / controls.HERE,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=45,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    leaf = tree / houses.house_path(266).relative_to(SOURCE)
    before = leaf.read_bytes()
    refused = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "from devtools.evand_arrangement_houses import guard_house_outputs; "
                "guard_house_outputs([266])"
            ),
        ],
        cwd=tree / controls.HERE,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert refused.returncode != 0
    assert "escapes" in refused.stderr
    assert leaf.read_bytes() == before
    child_receipt = tree / reports.receipt_path().relative_to(SOURCE)
    record: Any = reports.read_xz(child_receipt)
    record["cases"][0]["exact_verify"]["pairs_tested"] -= 1
    child_receipt.write_bytes(lzma.compress(json.dumps(record).encode()))
    rejected = subprocess.run(
        [
            sys.executable,
            "-c",
            "from devtools.evand_arrangement_houses import check_houses; check_houses()",
        ],
        cwd=tree / controls.HERE,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=45,
    )
    assert rejected.returncode != 0
    assert "native exact route" in rejected.stderr


@pytest.fixture
def original_cases(
    private: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[dict[int, str], Path]:
    original_packet = SOURCE / reports.PACKET.relative_to(reports.REPO)
    prior = reports.read_xz(original_packet / "acquisition/prior-state.json.xz")
    frontier = private / "packing/frontier"
    frontier.mkdir(parents=True, exist_ok=True)
    originals = {row["n"]: row["complete_case"] for row in prior}
    for n, text in originals.items():
        (frontier / f"n-{n:03d}.md").write_text(text)
    monkeypatch.setattr(adoption, "FRONTIER", frontier)
    monkeypatch.setattr(adoption.registry.packets, "REPO", private)
    history = reports.PACKET / "acquisition/prior-state.json.xz"
    assert not history.exists()
    return originals, history


def test_later_case_preflight_refuses_without_mutation_and_restoration_succeeds(
    original_cases: tuple[dict[int, str], Path],
) -> None:
    originals, history = original_cases
    later = adoption.FRONTIER / "n-270.md"
    changed = originals[270].splitlines(keepends=True)
    later.write_text("".join(line for line in changed if not line.startswith("# ")))
    before = {n: (adoption.FRONTIER / f"n-{n:03d}.md").read_bytes() for n in originals}
    with pytest.raises(reports.ReportError, match="existing title"):
        adoption.record_cases()
    assert not history.exists()
    assert {n: (adoption.FRONTIER / f"n-{n:03d}.md").read_bytes() for n in originals} == before
    later.write_text(originals[270])
    adoption.record_cases()
    assert {row["n"]: row["complete_case"] for row in reports.read_xz(history)} == originals
    for n in originals:
        current = (adoption.FRONTIER / f"n-{n:03d}.md").read_text()
        assert (
            safe_load(current.split("---\n", 2)[1])["packing"]["reported_upper_bound"][
                "source_key"
            ]
            == reports.SOURCE_KEY
        )


def test_interrupted_write_preserves_complete_history_and_retry_is_idempotent(
    original_cases: tuple[dict[int, str], Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    originals, history = original_cases
    original_save = adoption.registry.save

    def interrupted(path: Path, text: str) -> None:
        assert {row["n"]: row["complete_case"] for row in reports.read_xz(history)} == originals
        if path.name == "n-270.md":
            raise OSError("injected second case write failure")
        original_save(path, text)

    monkeypatch.setattr(adoption.registry, "save", interrupted)
    with pytest.raises(OSError, match="second case write"):
        adoption.record_cases()
    preserved = history.read_bytes()
    assert (adoption.FRONTIER / "n-266.md").read_text() != originals[266]
    assert (adoption.FRONTIER / "n-270.md").read_text() == originals[270]
    monkeypatch.setattr(adoption.registry, "save", original_save)
    adoption.record_cases()
    assert history.read_bytes() == preserved
    final = {n: (adoption.FRONTIER / f"n-{n:03d}.md").read_bytes() for n in originals}
    adoption.record_cases()
    assert history.read_bytes() == preserved
    assert {n: (adoption.FRONTIER / f"n-{n:03d}.md").read_bytes() for n in originals} == final


@pytest.mark.parametrize(
    "changed", ["incomplete", "duplicate", "wrong-count", "changed-original"]
)
def test_existing_history_must_be_complete_and_match_unadopted_originals(
    original_cases: tuple[dict[int, str], Path],
    changed: str,
) -> None:
    originals, history = original_cases
    rows = [{"n": n, "complete_case": text} for n, text in originals.items()]
    if changed == "incomplete":
        rows.pop()
    elif changed == "duplicate":
        rows[-1] = copy.deepcopy(rows[0])
    elif changed == "wrong-count":
        rows[-1]["complete_case"] = rows[-1]["complete_case"].replace("  n: 272", "  n: 271", 1)
    else:
        rows[-1]["complete_case"] += "\nAn unrelated source mutation.\n"
    reports.save_xz(history, rows)
    saved = history.read_bytes()
    before = {n: (adoption.FRONTIER / f"n-{n:03d}.md").read_bytes() for n in originals}
    with pytest.raises(
        reports.ReportError, match=r"roster|original pre-adoption|changed historical"
    ):
        adoption.record_cases()
    assert history.read_bytes() == saved
    assert {n: (adoption.FRONTIER / f"n-{n:03d}.md").read_bytes() for n in originals} == before


def test_adopted_prefix_without_history_cannot_replace_the_original_roster(
    original_cases: tuple[dict[int, str], Path],
) -> None:
    originals, history = original_cases
    first = adoption.FRONTIER / "n-266.md"
    first.write_text(adoption.adopt_case(266, originals[266]))
    before = {n: (adoption.FRONTIER / f"n-{n:03d}.md").read_bytes() for n in originals}
    with pytest.raises(reports.ReportError, match="lacks complete original history"):
        adoption.record_cases()
    assert not history.exists()
    assert {n: (adoption.FRONTIER / f"n-{n:03d}.md").read_bytes() for n in originals} == before
