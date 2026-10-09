"""Historical browser output needs a worker consumer before link rescue copies it."""

import subprocess
from pathlib import Path

import pytest

from devtools import run_negative_controls as controls
from tests.test_negative_controls import index_fixture_source


def test_operational_links_preserve_checked_consumers_and_scientific_custody(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "source"
    packing = repo / "packing"
    runs = packing / "benchmarks/math-startup/runs"
    output = runs / "historical/reference.pdf"
    output.parent.mkdir(parents=True)
    output.write_bytes(b"retained browser observation")
    archive = packing / "resources"
    scientific_input = archive / "certificate.json"
    archive.mkdir()
    scientific_input.write_bytes(b"deciding scientific input")
    review = repo / "docs/review.md"
    review.parent.mkdir()
    review.write_text(
        "[observation](../packing/benchmarks/math-startup/runs/historical/reference.pdf)\n"
        "[scientific input](../packing/resources/certificate.json)\n"
    )
    readme, synopsis = repo / "README.md", repo / "SYNOPSIS.md"
    readme.write_text("[review](docs/review.md)\n")
    synopsis.write_text("Synopsis\n")
    campaign = packing / "campaign/record.md"
    campaign.parent.mkdir()
    campaign.write_text("Campaign\n")
    register = packing / "frontier/results.yaml"
    register.parent.mkdir()
    register.write_text("results: []\n")
    monkeypatch.setattr(controls, "REPO", repo)
    monkeypatch.setattr(controls, "ROOT", packing)
    monkeypatch.setattr(controls, "HERE", Path("packing"))
    monkeypatch.setattr(controls, "PRUNE", frozenset({runs, archive}))
    monkeypatch.setattr(
        controls,
        "DESCEND",
        frozenset({packing / "benchmarks", packing / "benchmarks/math-startup"}),
    )
    monkeypatch.setattr(controls, "LINKED_PRUNE_ROOTS", (runs, archive))
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", (readme, synopsis, review.parent))
    monkeypatch.setattr(controls, "COPY_SEPARATELY", ())
    monkeypatch.setattr(controls, "LINK_BACK", ())

    # A checked link to the review checks that document, not its outgoing links.
    assert controls.snapshot_pruned_targets() == [scientific_input]
    index_fixture_source(repo)
    tree = tmp_path / "worker"
    controls.clone_tree(tree)
    assert not (tree / output.relative_to(repo)).exists()
    copied_input = tree / scientific_input.relative_to(repo)
    assert copied_input.read_bytes() == scientific_input.read_bytes()
    git_tree = subprocess.run(
        ["git", "-C", str(repo), "write-tree"],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout.strip()
    assert controls.snapshot_git_source_bytes(git_tree) == controls.snapshot_source_bytes()

    for document, relative in (
        (readme, "packing/benchmarks/math-startup/runs/historical/reference.pdf"),
        (synopsis, "packing/benchmarks/math-startup/runs/historical/reference.pdf"),
        (campaign, "../benchmarks/math-startup/runs/historical/reference.pdf"),
    ):
        original = document.read_text()
        document.write_text(original + f"[observed input]({relative})\n")
        assert controls.snapshot_pruned_targets() == [output, scientific_input]
        document.write_text(original)

    # Structural result registration and explicit custody remain independent of prose.
    for field in ("artifacts", "controls", "reviews"):
        declaration = (
            "reviews: [{path: packing/benchmarks/math-startup/runs/historical/reference.pdf}]"
            if field == "reviews"
            else f"{field}: [packing/benchmarks/math-startup/runs/historical/reference.pdf]"
        )
        register.write_text(f"results:\n- {declaration}\n")
        assert controls.snapshot_pruned_targets() == [output, scientific_input]
    register.write_text("results: []\n")
    monkeypatch.setattr(controls, "COPY_SEPARATELY", (output,))
    assert output in controls.snapshot_copy_targets()

    # Rescued evidence remains a private mutable copy, never a link into custody.
    readme.write_text(
        "[observed input](packing/benchmarks/math-startup/runs/historical/reference.pdf)\n"
    )
    index_fixture_source(repo)
    rescued_tree = tmp_path / "rescued-worker"
    controls.clone_tree(rescued_tree)
    copied = rescued_tree / output.relative_to(repo)
    assert not copied.is_symlink()
    assert copied.read_bytes() == output.read_bytes()
    copied.write_bytes(b"corrupted observation")
    assert output.read_bytes() == b"retained browser observation"
