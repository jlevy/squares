"""The instrument behind the release-assets plan measures what it says it measures.

`devtools.measure_release_assets` is where the numbers in
`plan-2026-10-01-release-assets-on-demand.md` come from: what each build costs, and what
the re-pin commits cost git. The second is a claim about history -- of thirty re-pins in
a row, none changed a card -- so the reading it rests on is held here on a scratch
repository where the answer is known.
"""

from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest

from devtools import build_known_best_atlas as atlas
from devtools import measure_release_assets as measure
from devtools import render_composite_pdf
from sqpack.known_best import CompositeSpec

SCRATCH_GIT = (
    "-c",
    "user.name=measure test",
    "-c",
    "user.email=measure-test@example.invalid",
    "-c",
    "commit.gpgsign=false",
    "-c",
    "core.hooksPath=/dev/null",
)
SVG = (
    '<svg>\n  <text data-feature="release-stamp" x="1">{stamp}</text>\n'
    '  <g data-feature="packing-card" data-n="11"><text>{bound}</text></g>\n</svg>\n'
)
POSTER = "packing/atlas/known-best/known-best-1-100.svg"
RASTER = "packing/atlas/known-best/known-best-1-100@2x.png"


def _git(repo: Path, *arguments: str) -> str:
    done = subprocess.run(
        ("git", "-C", str(repo), *SCRATCH_GIT, *arguments),
        capture_output=True,
        text=True,
        check=True,
    )
    return done.stdout.strip()


def _commit(repo: Path, subject: str, files: dict[str, bytes]) -> str:
    for path, content in files.items():
        target = repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        _git(repo, "add", path)
    _git(repo, "commit", "--quiet", "-m", subject)
    return _git(repo, "rev-parse", "HEAD")


def test_a_drawing_that_differs_only_in_its_stamp_reads_as_unchanged() -> None:
    first = SVG.format(stamp="v0.4.2-aaaaaa", bound="3.87")
    assert measure.without_stamp(first) == measure.without_stamp(
        SVG.format(stamp="v0.4.2-bbbbbb", bound="3.87")
    )
    assert measure.without_stamp(first) != measure.without_stamp(
        SVG.format(stamp="v0.4.2-aaaaaa", bound="3.875")
    )
    assert "v0.4.2" not in measure.without_stamp(first)


def test_a_commits_cost_is_its_new_blobs_and_whether_a_drawing_changed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A re-stamp and a redraw, told apart, with the bytes each added.

    The family is the composite files and nothing else: a re-pin's line of `release.py`
    counts toward the commit and not toward the family.
    """
    repo = tmp_path / "origin"
    repo.mkdir()
    _git(repo, "init", "--quiet")
    monkeypatch.setattr(measure, "REPO", repo)
    first_svg = SVG.format(stamp="v0.4.2-aaaaaa", bound="3.87").encode()
    _commit(
        repo,
        "atlas: first drawing",
        {POSTER: first_svg, RASTER: b"png one", "packing/src/sqpack/release.py": b"pin a\n"},
    )
    restamped_svg = SVG.format(stamp="v0.4.2-bbbbbb", bound="3.87").encode()
    restamp = _commit(
        repo,
        "release: re-pin DATA_REVISION to bbbbbbbb and re-stamp the atlas",
        {
            POSTER: restamped_svg,
            RASTER: b"png two!",
            "packing/src/sqpack/release.py": b"pin b\n",
        },
    )
    redrawn_svg = SVG.format(stamp="v0.4.2-cccccc", bound="3.875").encode()
    redraw = _commit(
        repo,
        "release: re-pin DATA_REVISION to cccccccc and re-stamp the atlas",
        {POSTER: redrawn_svg, RASTER: b"png three"},
    )

    cost = measure.commit_cost(restamp)
    assert (cost.files, cost.family_files, cost.redrawn) == (3, 2, ())
    assert (cost.reframed, cost.drawing) == ((), "stamp only")
    assert cost.family_blob_bytes == len(restamped_svg) + len(b"png two!")
    assert cost.blob_bytes == cost.family_blob_bytes + len(b"pin b\n")
    assert 0 < cost.family_packed_bytes <= cost.packed_bytes

    cost = measure.commit_cost(redraw)
    assert (cost.files, cost.family_files) == (2, 2)
    assert cost.redrawn == ("known-best-1-100.svg",)
    assert cost.drawing == "cards: known-best-1-100.svg"

    # A footer sentence reworded, and no card: what the project's renaming did four times.
    reworded = _commit(
        repo,
        "release: re-pin DATA_REVISION to dddddddd and re-stamp the atlas",
        {POSTER: redrawn_svg.replace(b"<svg>", b"<svg>\n  <text>the Squares Project</text>")},
    )
    cost = measure.commit_cost(reworded)
    assert (cost.redrawn, cost.reframed) == ((), ("known-best-1-100.svg",))
    assert cost.drawing == "frame, no card: known-best-1-100.svg"

    assert measure.history("HEAD", measure.DEFAULT_GREP, 30, [], None) == 0
    assert measure.history("HEAD", "", 30, [POSTER], None) == 0
    with pytest.raises(SystemExit, match="no commit on HEAD matches"):
        measure.history("HEAD", "no such subject", 30, [], None)


def test_release_cost_counts_legacy_and_dated_pdf_exports(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo = tmp_path / "origin"
    repo.mkdir()
    _git(repo, "init", "--quiet")
    monkeypatch.setattr(measure, "REPO", repo)
    _commit(repo, "baseline", {"README.md": b"baseline\n"})
    pdfs = {
        "packing/atlas/known-best/known-best-1-324.pdf": b"legacy PDF",
        "packing/atlas/known-best/square-packings-100-20261008.pdf": b"dated hundred PDF",
        "packing/atlas/known-best/square-packings-324-20261008.pdf": b"dated poster PDF",
    }
    changed = _commit(repo, "PDF edition", {**pdfs, "papers/other.pdf": b"other PDF"})
    cost = measure.commit_cost(changed)
    assert cost.files == 4
    assert cost.family_files == 3
    assert cost.family_blob_bytes == sum(len(content) for content in pdfs.values())
    assert cost.blob_bytes == cost.family_blob_bytes + len(b"other PDF")
    assert (cost.redrawn, cost.reframed) == ((), ())
    for path in (
        "papers/square-packings-324-20261008.pdf",
        "packing/atlas/known-best/square-packings-324-20261008.svg",
        "packing/atlas/known-best/square-packings-324-latest.pdf",
        "packing/atlas/known-best/square-packings-324-20261008.pdf.bak",
    ):
        assert measure.COMPOSITE_FAMILY.search(path) is None


def test_pdf_timing_reports_the_published_download_names(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(render_composite_pdf, "render_pdf_bytes", lambda _stem: b"PDF")
    measure._atlas_pdfs()  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    report = capsys.readouterr().out
    assert "square-packings-100-20261008.pdf: 3 bytes" in report
    assert "square-packings-324-20261008.pdf: 3 bytes" in report


def test_raster_timing_uses_resolved_production_dimensions_without_rendering(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    custom = atlas.CompositeCanvas(CompositeSpec(1, 4, 2, "synthetic", raster_scales=(1,)))
    monkeypatch.setattr(atlas, "COMPOSITES", (*atlas.COMPOSITES, custom))
    monkeypatch.setattr(atlas, "ATLAS_ROOT", tmp_path)
    for canvas in atlas.COMPOSITES:
        canvas.svg_path.write_text(f"source for {canvas.spec.stem}", encoding="utf-8")
    requested: list[tuple[str, int, int]] = []

    def capture(export: atlas.RasterExport, svg_text: str) -> bytes:
        assert svg_text.startswith("source for ")
        requested.append((export.path.name, export.width, export.height))
        return b"PNG"

    monkeypatch.setattr(atlas, "png_export_bytes", capture)
    measure._atlas_rasters()  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert requested == [
        ("known-best-1-100.png", 2260, 3995),
        ("known-best-1-100@2x.png", 4520, 7990),
        ("known-best-1-100-card.png", 2260, 1256),
        ("known-best-1-324.png", 7871, 5701),
        ("synthetic.png", 576, 880),
    ]
    assert capsys.readouterr().out.count(": 3 bytes,") == len(requested)


def test_the_phases_are_commands_that_exist_and_groups_select_them() -> None:
    """Each phase is a module's own command or a function named here, never a script."""
    for phase in measure.PHASES:
        module = phase.command[0]
        assert importlib.util.find_spec(module) is not None, phase.name
        if module == measure.MODULE:
            assert phase.command[1:3] == ("--run", phase.command[2])
            assert phase.command[2] in measure.INTERNAL, phase.name
    assert len({phase.name for phase in measure.PHASES}) == len(measure.PHASES)
    assert measure.selected([]) == measure.PHASES
    atlas = measure.selected(["atlas"])
    assert atlas
    assert all(phase.group == "atlas" or "atlas" in phase.name for phase in atlas)
    assert [phase.name for phase in measure.selected(["re-pin"])] == ["re-pin"]
    with pytest.raises(SystemExit, match="names no phase"):
        measure.selected(["no such build"])
