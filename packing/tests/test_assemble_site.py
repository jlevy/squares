"""Producer assembly shares identical assets and refuses partial collision writes."""

from pathlib import Path

import pytest

from devtools.assemble_site import assemble


def test_shared_assets_are_merged_and_conflicts_preflight_before_writes(tmp_path: Path) -> None:
    site, left, right = (tmp_path / part for part in ("site", "left", "right"))
    for root in (left, right):
        (root / "assets").mkdir(parents=True)
        (root / "assets" / "same.css").write_text("shared")
    (left / "index.html").write_text("overview")
    (right / "paper.html").write_text("paper")
    assert assemble(site, (left, right)) == 3
    assert (site / "assets" / "same.css").read_text() == "shared"
    assert assemble(site, (left, right)) == 0
    (right / "a-new.html").write_text("new")
    (right / "index.html").write_text("collision")
    with pytest.raises(ValueError, match="collision"):
        assemble(site, (right,))
    assert not (site / "a-new.html").exists()
    assert (site / "index.html").read_text() == "overview"


def test_symlinks_and_empty_producers_are_refused(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    with pytest.raises(ValueError, match="empty"):
        assemble(tmp_path / "site", (source,))
    (source / "outside").symlink_to(tmp_path / "outside")
    with pytest.raises(ValueError, match="symlink"):
        assemble(tmp_path / "site", (source,))


@pytest.mark.parametrize("reverse", [False, True])
def test_file_directory_conflict_between_producers_fails_before_writing(
    tmp_path: Path, *, reverse: bool
) -> None:
    left, right, site = (tmp_path / name for name in ("left", "right", "site"))
    left.mkdir()
    (left / "a-new.html").write_text("new")
    (left / "item").write_text("file")
    (right / "item").mkdir(parents=True)
    (right / "item" / "page.html").write_text("page")
    sources = (right, left) if reverse else (left, right)
    with pytest.raises(ValueError, match="file/directory collision"):
        assemble(site, sources)
    assert not site.exists()


def test_destination_symlink_is_refused(tmp_path: Path) -> None:
    source, real, link = (tmp_path / name for name in ("source", "real", "link"))
    source.mkdir()
    real.mkdir()
    (source / "index.html").write_text("page")
    link.symlink_to(real, target_is_directory=True)
    with pytest.raises(ValueError, match="symlink"):
        assemble(link, (source,))
    assert not (real / "index.html").exists()
