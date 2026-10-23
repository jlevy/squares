"""Controls for the document sweep behind the inline-SVG ownership check.

The check asks a question about this repository's own prose: does every SVG a document
embeds resolve to an artifact this repository builds and retains? The question only makes
sense over documents this repository is answerable for, and the sweep is what decides
that set. Widen it by accident and the check indicts files nobody here wrote.

That is not hypothetical. `vendor/kpress` is an upstream repository checked out as a
submodule, and its own test fixtures embed two SVGs of their own. The sweep excluded
`resources`, `node_modules` and dot-prefixed directories but not `vendor`, so the moment
the submodule landed the check began failing on `main` -- reporting, correctly by its own
lights and uselessly by ours, that an upstream project's fixture is not one of our
artifacts (D-455).

So what is pinned here is the boundary, not the check: the sweep must reach our
documents and must not reach a vendored one. The check's own controls run in the
validation gate; these run in the fast suite, where a regression is cheap to see.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from devtools import check_svg_rendering as tool
from devtools.check_svg_rendering import (
    FOREIGN_DIRECTORY_NAMES,
    REPO,
    repository_documents,
)
from devtools.repo_scope import vendored_directories

#: A Markdown file inside the vendored submodule that embeds an SVG of its own. Named
#: rather than discovered: a test that searches for its own subject passes when the
#: subject is gone, which is the failure mode this test exists to catch.
VENDORED_DOCUMENT = REPO / "vendor/kpress/tests/e2e/docs/index.md"


def test_the_sweep_reaches_this_repositorys_own_documents() -> None:
    """A sweep that excluded everything would satisfy every other test here."""
    documents = set(repository_documents())
    assert REPO / "README.md" in documents
    assert REPO / "AGENTS.md" in documents


@pytest.mark.skipif(
    not VENDORED_DOCUMENT.is_file(),
    reason="vendor/kpress is not checked out, so there is no vendored document to exclude",
)
def test_the_sweep_does_not_reach_a_vendored_document() -> None:
    """The regression that turned `main` red: upstream fixtures are not our prose."""
    assert VENDORED_DOCUMENT not in set(repository_documents())


@pytest.mark.skipif(
    not (REPO / "vendor").is_dir(),
    reason="vendor/ is not checked out",
)
def test_no_swept_document_lies_under_a_foreign_directory() -> None:
    """Stated over the whole result, so a second vendored tree cannot slip in."""
    trespassers = [
        document.relative_to(REPO).as_posix()
        for document in repository_documents()
        if FOREIGN_DIRECTORY_NAMES & set(document.relative_to(REPO).parts)
    ]
    assert trespassers == []


def test_a_generated_document_under_site_is_not_swept() -> None:
    """The render output is this repository's, but it is not this repository's prose.

    `packing/site/` is written fresh by every explainer render: the page, the published
    Markdown, and copies of the composite placed beside them. The published document
    embeds its neighbouring copy of the atlas, which is not one of the atlas's owned
    artifacts and never will be, so sweeping that directory makes the ownership control
    report a finding about a file the renderer is already responsible for.

    Being gitignored is not what excludes it. This sweep walks files git does not track,
    which is exactly the blind spot D-455 was about; the exclusion has to be stated.
    """
    swept = {document.relative_to(REPO).as_posix() for document in repository_documents()}
    assert not [path for path in swept if path.startswith("packing/site/")]
    assert "site" in FOREIGN_DIRECTORY_NAMES


def test_the_exclusion_set_is_the_one_the_formatter_uses() -> None:
    """`.flowmarkignore` excludes every vendored tree, for the same reason.

    The two lists are maintained by hand in different languages, and the vendored entry
    is the one that has drifted before. It is no longer hand-typed on this side --
    `devtools.repo_scope` reads `.gitmodules` -- so what is checked here is the
    formatter's list against the declaration, which covers a second submodule the day it
    is added rather than the day someone remembers.
    """
    ignore = (REPO / ".flowmarkignore").read_text(encoding="utf-8")
    declared = vendored_directories()
    assert declared, "no submodule is declared; the exclusion would be vacuous"
    for path in sorted(declared):
        top = path.split("/")[0]
        assert f"{top}/" in ignore, f"{top}/ is vendored but the formatter does not skip it"
    assert "vendor" not in FOREIGN_DIRECTORY_NAMES, "vendored trees come from .gitmodules"


def test_a_document_in_a_vendored_tree_is_not_swept() -> None:
    """The sweep skips submodules by declaration, not by a name someone typed.

    D-455 was the vendored tree being swept at all. What replaced the fix is a weaker
    thing to get wrong -- a second submodule under a different name -- so the property
    checked is the general one: nothing under any declared submodule path is swept.
    """
    swept = {document.relative_to(REPO).as_posix() for document in repository_documents()}
    for path in sorted(vendored_directories()):
        assert not [seen for seen in swept if seen.startswith(f"{path}/")], path


def test_svg_images_are_semantic_in_markdown_and_html(tmp_path: Path) -> None:
    document = tmp_path / "examples.md"
    document.write_text(
        '![Packing](first.svg "Caption")\n\n'
        '<figure><img alt="Second packing"\n src="second.svg"></figure>\n\n'
        "![Third packing][third]\n\n[third]: third.svg\n\n"
        '`<img src="inline-code.svg" alt="not an image">`\n\n'
        '```html\n<img src="fenced-code.svg" alt="not an image">\n```\n\n'
        '<!-- <img src="comment.svg" alt="not an image"> -->\n'
    )
    assert tool.svg_image_targets(document) == (
        ((tmp_path / "first.svg").resolve(), "Packing"),
        ((tmp_path / "second.svg").resolve(), "Second packing"),
        ((tmp_path / "third.svg").resolve(), "Third packing"),
    )


@pytest.mark.parametrize("damage", ["missing", "unowned", "comparison", "comparison-no-alt"])
def test_gallery_controls_reject_html_image_boundary_violations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, damage: str
) -> None:
    target = tmp_path / "not-a-retained-artifact.svg"
    if damage == "unowned":
        target.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
    elif damage.startswith("comparison"):
        target = tool.ROOT / "atlas/rendering/gobel10-source-return-comparison.svg"
    document = tmp_path / "unexpected-embed.md"
    alt = "" if damage == "comparison-no-alt" else 'alt="Packing" '
    document.write_text(f'<figure><img {alt}src="{target}"></figure>')
    gallery = tool.ROOT / "atlas/rendering/README.md"
    virtual = tool.REPO / "unexpected-image-fixture.md"
    extract = tool.svg_image_targets

    def images(path: Path) -> tuple[tuple[Path | None, str], ...]:
        return extract(document if path == virtual else path)

    monkeypatch.setattr(tool, "svg_image_targets", images)
    monkeypatch.setattr(tool, "repository_documents", lambda: iter((gallery, virtual)))
    controls = tool.run_gallery_controls()
    if damage == "missing":
        assert not controls["all_inline_svg_targets_exist"]
        assert not controls["all_inline_svg_targets_are_owned_artifacts"]
    elif damage == "unowned":
        assert controls["all_inline_svg_targets_exist"]
        assert not controls["all_inline_svg_targets_are_owned_artifacts"]
    else:
        assert controls["all_inline_svg_targets_exist"]
        assert controls["all_inline_svg_targets_are_owned_artifacts"]
        assert not controls["comparison_is_embedded_only_in_focused_gallery"]


def test_an_html_tutorial_image_with_the_wrong_owned_source_is_rejected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document = tmp_path / "wrong-example.md"
    wrong_source = tool.ROOT / "atlas/rendering/kingbird29-overview.svg"
    document.write_text(f'<figure><img alt="Packing" src="{wrong_source}"></figure>')
    extract = tool.svg_image_targets

    def images(path: Path) -> tuple[tuple[Path | None, str], ...]:
        return extract(document if path == tool.REPO / "TUTORIAL.md" else path)

    monkeypatch.setattr(tool, "svg_image_targets", images)
    assert not tool.run_gallery_controls()["exposition_surfaces_embed_expected_examples"]


def test_only_the_explainer_template_resolves_the_known_composite_placeholder(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(tool, "REPO", tmp_path)
    document = tmp_path / "packing/devtools/templates/n11-lower-bounds-explainer-article.md"
    document.parent.mkdir(parents=True)
    document.write_text(
        '<img alt="Composite" src="{{SITE_ROOT}}known-best-1-100.svg">\n'
        '<img alt="Wrong source" src="{{SITE_ROOT}}missing.svg">'
    )
    known, unknown = tool.svg_image_targets(document)
    assert known[0] == (tool.ROOT / "atlas/known-best/known-best-1-100.svg").resolve()
    assert known[0] is not None
    assert known[0].is_file()
    assert unknown[0] is not None
    assert not unknown[0].is_file()
    other = tmp_path / "other.md"
    other.write_text('<img alt="Composite" src="{{SITE_ROOT}}known-best-1-100.svg">')
    assert tool.svg_image_targets(other)[0][0] != known[0]
