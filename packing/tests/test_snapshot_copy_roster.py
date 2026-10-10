"""Count and copy the full private roster without repeated destination writes."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

from devtools import run_negative_controls as controls
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


def test_historical_replay_inputs_survive_an_ancestor_prune(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The production custody roster rescues leaves even without inline links."""
    repo = tmp_path / "source"
    inputs = tuple(
        repo / path.relative_to(controls.REPO)
        for path in sorted(controls.HISTORICAL_REPLAY_INPUTS)
    )
    carried = tuple(
        repo / path.relative_to(controls.REPO)
        for path in controls.COPY_SEPARATELY
        if path in controls.HISTORICAL_REPLAY_INPUTS
    )
    agenda = inputs[0].parent
    agenda.mkdir(parents=True)
    for source in inputs:
        source.write_bytes(source.name.encode())
    bulk = agenda / "unconsumed-profile.json"
    bulk.write_bytes(b"unrelated generated output")
    index_fixture_source(repo)
    monkeypatch.setattr(controls, "REPO", repo)
    monkeypatch.setattr(controls, "ROOT", repo / "packing")
    monkeypatch.setattr(controls, "HERE", Path("packing"))
    monkeypatch.setattr(controls, "PRUNE", frozenset({agenda}))
    monkeypatch.setattr(controls, "DESCEND", frozenset(agenda.parents))
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", ())
    monkeypatch.setattr(controls, "LINK_BACK", ())
    monkeypatch.setattr(controls, "COPY_SEPARATELY", carried)
    monkeypatch.setattr(controls, "root_files", tuple)
    monkeypatch.setattr(controls, "snapshot_pruned_targets", lambda: [inputs[0]])
    monkeypatch.setattr(controls, "linked_pruned_directories", list)

    paths = controls.snapshot_source_paths()
    assert sorted(paths) == list(inputs)
    assert controls.snapshot_source_bytes() == sum(p.stat().st_size for p in inputs)
    destination = tmp_path / "worker"
    controls.clone_tree(destination)
    for source in inputs:
        assert (destination / source.relative_to(repo)).read_bytes() == source.read_bytes()
    assert not (destination / bulk.relative_to(repo)).exists()


def test_schema_overlap_aligns_copier_live_and_git_rosters(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Named, rescued and bulk selections share one path; equal-byte aliases remain."""
    for name in tuple(os.environ):
        if name.startswith("GIT_"):
            monkeypatch.delenv(name)

    repo = tmp_path / "source"
    packing = repo / "packing"
    schema = packing / "witnesses/witness.schema.yaml"
    schema.parent.mkdir(parents=True)
    schema.write_bytes(b"type: object\n")
    alias = schema.with_name("independent.schema.yaml")
    alias.write_bytes(schema.read_bytes())
    document = repo / "README.md"
    document.write_text("[schema](packing/witnesses/witness.schema.yaml)\n")
    register = packing / "frontier/results.yaml"
    register.parent.mkdir()
    register.write_text("results:\n- artifacts: [packing/witnesses/witness.schema.yaml]\n")
    index_fixture_source(repo)
    tree = subprocess.run(
        ["git", "-C", str(repo), "write-tree"],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout.strip()
    monkeypatch.setattr(controls, "REPO", repo)
    monkeypatch.setattr(controls, "ROOT", packing)
    monkeypatch.setattr(controls, "HERE", Path("packing"))
    monkeypatch.setattr(controls, "PRUNE", frozenset())
    monkeypatch.setattr(controls, "LINKED_PRUNE_ROOTS", (schema.parent,))
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", (document,))
    monkeypatch.setattr(controls, "COPY_SEPARATELY", (schema, alias, schema))
    monkeypatch.setattr(controls, "LINK_BACK", ())
    monkeypatch.setattr(controls, "root_files", tuple)
    monkeypatch.setattr(controls, "_linked_documents", lambda: [document])
    monkeypatch.setattr(controls, "index_tree", lambda _tree: None)
    assert controls.snapshot_pruned_targets() == [schema]
    selected = {schema, alias, document, register}
    live_paths = controls.snapshot_source_paths()
    assert live_paths == sorted(selected)
    inventory = controls.snapshot_git_source_inventory(tree)
    assert inventory == {path: path.stat().st_size for path in selected}
    assert inventory[schema] == inventory[alias] == len(b"type: object\n")
    assert controls.snapshot_source_bytes() == sum(inventory.values())
    assert controls.snapshot_git_source_bytes(tree) == sum(inventory.values())
    copied: list[Path] = []
    copy = shutil.copy2

    def counted_copy(source_path: str | Path, landing: str | Path) -> str | Path:
        copied.append(Path(source_path))
        return copy(source_path, landing)

    monkeypatch.setattr(shutil, "copy2", counted_copy)
    destination = tmp_path / "worker"
    controls.clone_tree(destination)
    # The bulk clone already carried both schemas; named/rescued routes add no write.
    assert schema not in copied
    assert alias not in copied
    actual = {
        path.relative_to(destination): path.stat().st_size
        for path in destination.rglob("*")
        if path.is_file()
    }
    assert actual == {path.relative_to(repo): size for path, size in inventory.items()}
    private = destination / schema.relative_to(repo)
    assert not private.is_symlink()
    private.write_bytes(b"invalid schema")
    assert schema.read_bytes() == alias.read_bytes() == b"type: object\n"
    assert (destination / alias.relative_to(repo)).read_bytes() == alias.read_bytes()
