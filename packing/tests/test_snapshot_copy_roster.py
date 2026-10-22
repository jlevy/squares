"""Count and copy the full private roster without repeated destination writes."""

import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from devtools import run_negative_controls as controls
from sqpack.contributor_occurrences import dependency_paths
from sqpack.contributors import PEOPLE_DIR, SCHEMA_PATH, load_contributors
from sqpack.yamlio import load_yaml
from tests.test_negative_controls import index_fixture_source


@pytest.fixture
def source_roster(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    repo = tmp_path / "source"
    root = repo / "packing"
    archive = root / "resources"
    archive.mkdir(parents=True)
    first, alias = archive / "first.json", archive / "alias.json"
    first.write_bytes(b'{"exact":1}')
    alias.write_bytes(first.read_bytes())
    index_fixture_source(repo)
    monkeypatch.setattr(controls, "REPO", repo)
    monkeypatch.setattr(controls, "ROOT", root)
    monkeypatch.setattr(controls, "HERE", Path("packing"))
    monkeypatch.setattr(controls, "PRUNE", frozenset({archive}))
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", ())
    monkeypatch.setattr(controls, "LINK_BACK", ())
    monkeypatch.setattr(controls, "COPY_SEPARATELY", (first, alias, first))
    monkeypatch.setattr(controls, "root_files", lambda: (first,))
    monkeypatch.setattr(controls, "snapshot_pruned_targets", lambda: [alias, first])
    monkeypatch.setattr(controls, "linked_pruned_directories", list)
    return first, alias


def test_named_duplicates_count_once_and_aliases_remain(
    source_roster: tuple[Path, Path],
) -> None:
    first, alias = source_roster
    assert controls.snapshot_copy_targets() == (first, alias)
    assert controls.snapshot_source_bytes() == first.stat().st_size + alias.stat().st_size
    assert controls.snapshot_duplicate_copy_bytes() == 4 * first.stat().st_size


def test_clone_carries_both_mutable_aliases_independently(
    source_roster: tuple[Path, Path], tmp_path: Path
) -> None:
    first, alias = source_roster
    destination = tmp_path / "worker"
    controls.clone_tree(destination)
    private_first = destination / first.relative_to(controls.REPO)
    private_alias = destination / alias.relative_to(controls.REPO)
    assert private_first.read_bytes() == first.read_bytes()
    assert private_alias.read_bytes() == alias.read_bytes()
    private_first.write_bytes(b"invalid witness")
    assert private_alias.read_bytes() == alias.read_bytes()
    assert first.read_bytes() == alias.read_bytes()


def test_roster_is_rebuilt_after_new_input_declaration(
    source_roster: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    first, alias = source_roster
    assert controls.snapshot_copy_targets() == (first, alias)
    extra = first.with_name("new-receipt.json")
    extra.write_bytes(b"new deciding receipt")
    monkeypatch.setattr(controls, "COPY_SEPARATELY", (first, alias, extra))
    assert controls.snapshot_copy_targets() == (first, alias, extra)
    assert controls.snapshot_source_bytes() == sum(
        p.stat().st_size for p in (first, alias, extra)
    )


def test_contributor_seed_evidence_survives_archive_pruning() -> None:
    registry = load_contributors(controls.ROOT / PEOPLE_DIR, repo=controls.REPO)
    declared = {
        (controls.REPO / source.archive_path).resolve()
        for contributor in registry.by_id.values()
        for source in contributor.sources
        if source.archive_path is not None
    }
    declared.update(
        path.resolve()
        for path in dependency_paths(
            controls.ROOT / "contributors/occurrences.yaml", repo=controls.REPO
        )
        if controls.in_pruned_roots(path, frozenset(controls.LINKED_PRUNE_ROOTS))
    )
    assert set(controls.contributor_pruned_targets()) == {
        path
        for path in declared
        if controls.in_pruned_roots(path, frozenset(controls.LINKED_PRUNE_ROOTS))
    }
    # Unpruned dependencies arrive through the ordinary tree walk; only archive
    # dependencies need the separate rescue roster asserted above.
    assert declared <= set(controls.snapshot_source_paths())
    assert any(path.name == "LICENSE" for path in declared)
    assert any(path.name == "CITATION.cff" for path in declared)
    assert controls.ROOT / "resources" not in controls.snapshot_copy_targets()


def test_snapshot_copies_only_declared_contributor_evidence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = controls.ROOT / PEOPLE_DIR
    repo = tmp_path / "source"
    root = repo / "packing"
    directory = root / "contributors"
    (directory / "people").mkdir(parents=True)
    (directory / "schemas").mkdir()
    shutil.copyfile(original / SCHEMA_PATH, directory / "people" / SCHEMA_PATH)
    archive = root / "resources"
    archive.mkdir()
    cited = archive / "CITATION.cff"
    cited.write_text("authors:\n  - name: Mira\n")
    unrelated = archive / "unrelated.bin"
    unrelated.write_bytes(b"not a deciding input")
    origin = archive / "origin.yaml"
    origin.write_text("credit: Mira\n")
    inspected = archive / "inspected.txt"
    inspected.write_text("public byline")
    pending = archive / "pending.pdf"
    pending.write_bytes(b"pending archive bytes")
    manifest = {
        "occurrences": [{"origin": {"path": "packing/resources/origin.yaml"}}],
        "inspections": [
            {"path": "packing/resources/inspected.txt", "status": "inspected"},
            {"path": "packing/resources/pending.pdf", "status": "pending"},
        ],
    }
    (directory / "occurrences.yaml").write_text(yaml.dump(manifest))
    document = load_yaml((original / "mira.md").read_text().split("---\n")[1])
    document["contributor"]["sources"][0]["archive_path"] = "packing/resources/CITATION.cff"
    header = yaml.dump(document, sort_keys=False)
    footer = (original / "mira.md").read_text().split("---\n")[2]
    (directory / "people" / "mira.md").write_text(f"---\n{header}---\n{footer}")
    register = root / "frontier/results.yaml"
    register.parent.mkdir()
    register.write_text("results: []\n")
    monkeypatch.setattr(controls, "REPO", repo)
    monkeypatch.setattr(controls, "ROOT", root)
    monkeypatch.setattr(controls, "HERE", Path("packing"))
    monkeypatch.setattr(controls, "PRUNE", frozenset({archive}))
    monkeypatch.setattr(controls, "LINKED_PRUNE_ROOTS", (archive,))
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", ())
    monkeypatch.setattr(controls, "COPY_SEPARATELY", ())
    monkeypatch.setattr(controls, "LINK_BACK", ())
    monkeypatch.setattr(controls, "root_files", tuple)
    assert set(controls.snapshot_pruned_targets()) == {cited, origin, inspected}
    index_fixture_source(repo)
    worker = tmp_path / "worker"
    controls.clone_tree(worker)
    assert (worker / cited.relative_to(repo)).read_bytes() == cited.read_bytes()
    assert not (worker / unrelated.relative_to(repo)).exists()
    assert (worker / origin.relative_to(repo)).read_bytes() == origin.read_bytes()
    assert (worker / inspected.relative_to(repo)).read_bytes() == inspected.read_bytes()
    assert not (worker / pending.relative_to(repo)).exists()
    assert (
        load_contributors(worker / "packing" / PEOPLE_DIR, repo=worker).by_id["mira"].id
        == "mira"
    )
    tree = subprocess.run(
        ["git", "-C", str(repo), "write-tree"],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout.strip()
    assert controls.snapshot_git_source_bytes(tree) == controls.snapshot_source_bytes()
