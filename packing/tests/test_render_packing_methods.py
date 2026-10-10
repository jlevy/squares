"""The methods tutorial is a standalone native paper, including its printed edition."""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path

import pytest

from devtools import (
    artifact_dates,
    check_published_site,
    paper_front,
    paper_structure,
    render_n11_optimality_review,
    render_overview,
    site_assets,
    site_math,
)
from devtools import render_packing_methods as paper
from devtools.render_n11_lower_bounds_explainer import assert_self_contained
from devtools.render_n11_lower_bounds_explainer_pdf import date_problem
from sqpack import release

REVISION = "a" * 40
FIGURES: dict[str, str] = dict.fromkeys(
    paper.FIGURE_KEYS, '<svg xmlns="http://www.w3.org/2000/svg"></svg>'
)
SOURCE = r"""{{FRONT_MATTER}}

## From a Candidate to an Upper Bound

A verified packing in a container of side $L$ establishes $s(n) \le L$.
See the [paper front](../paper_front.py) and the
[lower-bound paper]({{PAPER:n11-lower-bounds-explainer}}).

<figure>
{{HAND_CONSTRUCTION_SVG}}
<figcaption><strong>Figure 1.</strong> Example packing.</figcaption>
</figure>

<figure>
{{ANNEALING_SVG}}
<figcaption><strong>Figure 2.</strong> Example packing.</figcaption>
</figure>

<figure>
{{ANNEALING_SLP_SVG}}
<figcaption><strong>Figure 3.</strong> Example packing.</figcaption>
</figure>

<figure>
{{SURGERY_SVG}}
<figcaption><strong>Figure 4.</strong> Example packing.</figcaption>
</figure>

<figure>
{{ALGEBRAIC_WITNESS_SVG}}
<figcaption><strong>Figure 5.</strong> Example packing.</figcaption>
</figure>

## Version History

{{VERSION_HISTORY}}
"""


@pytest.fixture(scope="module")
def rendered() -> tuple[str, str]:
    return paper.render(SOURCE, figures=FIGURES, facts={}, revision=REVISION)


def test_the_tutorial_uses_the_shared_paper_front_and_its_own_identity(
    rendered: tuple[str, str],
) -> None:
    html, markdown = rendered
    assert_self_contained(html)
    assert paper.FRONT.series is None
    assert paper.FRONT.source is None
    assert paper.SLUG == "square-packing-methods-survey"
    assert paper.SITE_PATH == "papers/square-packing-methods-survey.html"
    assert (paper.ARTICLE.name, paper.SHELL.name, paper.STYLE.name) == (
        "packing-methods-article.md",
        "packing-methods-shell.html",
        "packing-methods.css",
    )
    assert paper.FRONT.history == "version-history"
    assert paper.FRONT.version == release.PACKING_METHODS_EDITION == "v0.2.0"
    assert paper_front.revised(paper.FRONT) == release.PACKING_METHODS_REVISED
    assert "Part IV" not in html
    assert "the n = 11 series" not in markdown
    structure = paper_structure.read(paper.SLUG, html, markdown)
    assert [line.kind for line in structure.credits] == [
        "oversight",
        "agents",
        "version",
        "dates",
    ]
    assert [chip.href for chip in structure.chips] == [
        "square-packing-methods-survey.md",
        "square-packing-methods-survey.pdf",
        "https://github.com/jlevy/squares",
    ]
    version = next(line for line in structure.credits if line.kind == "version")
    assert version.text == "v0.2.0 (version history)"
    assert version.links == (("version history", "#version-history"),)
    assert version.bold == ()
    assert structure.h1 == ("How Record Square Packings Are Found",)
    assert structure.title == paper.TITLE
    assert structure.published == "2026-10-08"
    assert structure.modified == "2026-10-10"
    assert next(line.text for line in structure.credits if line.kind == "dates") == (
        "First published October 8, 2026 · Last revised October 10, 2026"
    )
    assert "- First published October 8, 2026 · Last revised October 10, 2026" in markdown
    assert structure.pdf == {}
    assert release.PUBLICATION_EDITION not in html
    assert release.PUBLICATION_EDITION not in markdown
    canonical = render_overview.SITE_URL + paper.SITE_PATH
    assert check_published_site.head_problems(html, canonical, allow_inline_favicon=True) == []
    assert '<a data-page="papers" aria-current="page" href="../papers.html">' in html
    assert "{{" not in markdown


def test_the_editions_pin_repository_citations_and_link_sibling_papers(
    rendered: tuple[str, str],
) -> None:
    html, markdown = rendered
    source = f"https://github.com/jlevy/squares/blob/{REVISION}/packing/devtools/paper_front.py"
    assert source in html
    assert source in markdown
    assert 'href="n11-lower-bounds-explainer.html"' in html
    assert (
        "(https://jlevy.github.io/squares/papers/n11-lower-bounds-explainer.html)" in markdown
    )
    assert markdown.startswith("# How Record Square Packings Are Found\n")
    assert "[PDF]" not in markdown


@pytest.mark.parametrize(
    ("source", "figures", "facts", "refusal"),
    [
        (SOURCE, {"WITNESS_SVG": "<svg></svg>"}, {}, "exactly the declared"),
        (SOURCE, FIGURES, {"L": "1"}, "no fact"),
        (SOURCE + "\n{{UNDECLARED}}", FIGURES, {}, "unresolved placeholders"),
        (SOURCE.replace("{{FRONT_MATTER}}", ""), FIGURES, {}, "exactly once"),
        (SOURCE.replace("{{HAND_CONSTRUCTION_SVG}}", ""), FIGURES, {}, "every declared"),
        (SOURCE + "{{HAND_CONSTRUCTION_SVG}}", FIGURES, {}, "exactly once"),
        (
            SOURCE,
            {**FIGURES, "HAND_CONSTRUCTION_SVG": "<svg><script/></svg>"},
            {},
            "active or remote",
        ),
        (SOURCE, {**FIGURES, "HAND_CONSTRUCTION_SVG": "<svg"}, {}, "complete SVG"),
        (
            SOURCE,
            {
                **FIGURES,
                "HAND_CONSTRUCTION_SVG": (
                    '<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"></svg>'
                ),
            },
            {},
            "unsafe SVG attribute",
        ),
        (
            SOURCE,
            {
                **FIGURES,
                "HAND_CONSTRUCTION_SVG": '<svg xmlns="http://www.w3.org/2000/svg"><image href = "https://example.invalid/asset.png"/></svg>',
            },
            {},
            "unsupported SVG element",
        ),
        (
            SOURCE,
            {
                **FIGURES,
                "HAND_CONSTRUCTION_SVG": '<svg xmlns="http://www.w3.org/2000/svg"><g></svg>',
            },
            {},
            "complete SVG",
        ),
    ],
)
def test_undeclared_inputs_and_unfilled_slots_are_refused(
    source: str, figures: dict[str, str], facts: dict[str, str], refusal: str
) -> None:
    with pytest.raises(ValueError, match=refusal):
        paper.render(source, figures=figures, facts=facts, revision=REVISION)


def test_the_canonical_manuscript_renders_through_the_registered_interface() -> None:
    html, markdown = paper.render(
        paper.ARTICLE.read_text(encoding="utf-8"),
        figures=paper.render_all_figures(),
        facts=paper.render_all_facts(),
        revision=REVISION,
    )
    assert_self_contained(html)
    assert markdown.startswith(f"# {paper.TITLE}\n")
    assert "{{" not in markdown
    assert 'class="kpress-math' in html
    assert html.count('class="methods-diagram ') == 5
    assert html.count("<figcaption") == 5
    assert markdown.count('class="methods-diagram ') == 5
    assert "square-packing-methods-survey.pdf" in html
    assert 'id="version-history"' in html
    history = markdown.partition("## Version History\n")[2]
    assert history
    assert release.PACKING_METHODS_HISTORY[0].version == "v0.2.0"
    for entry in release.PACKING_METHODS_HISTORY:
        assert (
            f"- **{entry.version} — {entry.first_published}.** {entry.result_scope}" in history
        )


def test_cli_checks_the_same_files_and_assets_it_publishes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    article = tmp_path / "article.md"
    article.write_text(
        SOURCE.replace("[paper front](../paper_front.py)", "paper front"), encoding="utf-8"
    )
    monkeypatch.setattr(paper, "ARTICLE", article)
    monkeypatch.setattr(site_math, "prepare", lambda html, **_kwargs: html)
    args = ["--site", str(tmp_path / "site"), "--revision", REVISION]
    assert paper.main(args) == 0
    page = tmp_path / "site" / paper.SITE_PATH
    markdown = tmp_path / "site" / render_overview.paper_path(paper.SLUG, ".md")
    assert page.is_file()
    assert markdown.is_file()
    assert paper.main([*args, "--check"]) == 0
    page.write_text(page.read_text(encoding="utf-8") + "stale", encoding="utf-8")
    with pytest.raises(SystemExit, match="stale square-packing-methods-survey output"):
        paper.main([*args, "--check"])
    with pytest.raises(SystemExit) as refusal:
        paper.main([*args, "--check", "--pdf"])
    assert refusal.value.code == 2


@pytest.mark.skipif(
    os.environ.get("SQPACK_PACKING_METHODS_BROWSER") != "1",
    reason="the dedicated methods-paper Pages producer sets SQPACK_PACKING_METHODS_BROWSER=1",
)
def test_printed_paper_has_its_own_title_dates_and_absolute_links(
    tmp_path: Path, rendered: tuple[str, str]
) -> None:
    html = site_math.prepare(rendered[0], page_path=paper.SITE_PATH)
    html, assets = site_assets.link_inline_assets(html, paper.SITE_PATH)
    site_assets.write_assets(tmp_path, assets)
    page = tmp_path / paper.SITE_PATH
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(html, encoding="utf-8")
    pdf = page.with_suffix(".pdf")
    revised = date(2026, 10, 10)
    paper.print_pdf(page, pdf, revised=revised, site_path=paper.SITE_PATH)
    data = pdf.read_bytes()
    assert date_problem(data, revised) is None
    structure = paper_structure.read(paper.SLUG, html, rendered[1], data)
    assert structure.pdf["title"] == paper.TITLE
    assert int(structure.pdf["pages"]) >= 1
    assert b"https://jlevy.github.io/squares/papers/n11-lower-bounds-explainer.html" in data
    # The shared print stylesheet hides the screen-only format chips.
    assert b"file://" not in data
    assert artifact_dates.main(["--pdf", str(pdf), "--revised", "packing-methods"]) == 0


@pytest.mark.skipif(
    os.environ.get("SQPACK_PACKING_METHODS_BROWSER") != "1",
    reason="the dedicated methods-paper Pages producer sets SQPACK_PACKING_METHODS_BROWSER=1",
)
def test_unrendered_math_never_publishes_a_pdf(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    page = tmp_path / "unrendered.html"
    page.write_text('<html><span class="kpress-math">raw TeX</span></html>', encoding="utf-8")
    pdf = page.with_suffix(".pdf")
    monkeypatch.setattr(render_n11_optimality_review, "MATH_WAIT_MS", 200)
    with pytest.raises(ValueError, match="unrendered math"):
        paper.print_pdf(page, pdf, revised=date(2026, 10, 8), site_path=paper.SITE_PATH)
    assert not pdf.exists()
