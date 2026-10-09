"""Count and copy the full private roster without repeated destination writes."""

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
