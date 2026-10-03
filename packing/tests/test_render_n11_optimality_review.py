"""The separate T-060 paper remains complete when opened from a local file."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Literal

import pytest

from devtools import (
    check_published_site,
    paper_front,
    render_n11_lower_bounds_explainer,
    render_overview,
)
from devtools import measure_site_pages as measure
from devtools import n11_optimality_mechanism_figures as mechanism
from devtools import n11_optimality_overview_figures as overview
from devtools import render_n11_optimality_review as paper
from devtools.render_n11_lower_bounds_explainer import assert_self_contained
from devtools.render_n11_optimality_review import TYPESET_ALL
from sqpack import release
from sqpack.probes import probe

ARTICLE = paper.TEMPLATES / "n11-optimality-review-article.md"
PROBES = Path(__file__).with_name("probes")
REVISION = "a" * 40
SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2 2">'
    '<title>Exact diagram</title><rect width="2" height="2"/></svg>'
)
FIGURES: dict[str, str] = dict.fromkeys(paper.FIGURE_KEYS, SVG)
SOURCE = """{{FRONT_MATTER}}

An exact formula is $x^2$.[^proof] See the
[review](../../../docs/project/reviews/review-2026-09-29-n11-optimality.md)
and the [record][register].

<figure>
{{WITNESS_SVG}}
<figcaption>See the
<a href="../../cases/trump11/verify_exact.py">exact witness check</a>.</figcaption>
</figure>

{{COVER_SVG}}

{{CAPTURE_SVG}}

{{MASK_SVG}}

[^proof]: The claim has a retained proof.

[register]: ../../frontier/results.yaml
"""

SOURCE += "\n" + "\n".join(
    "{{" + key + "}}" for key in paper.FIGURE_KEYS if "{{" + key + "}}" not in SOURCE
)


@pytest.fixture(scope="module")
def rendered() -> tuple[str, str]:
    return paper.render(SOURCE, figures=FIGURES, revision=REVISION, article=ARTICLE)


def test_rendered_page_is_offline_and_contains_proof_figures(rendered: tuple[str, str]) -> None:
    html, markdown = rendered
    assert_self_contained(html)
    assert html.count("<title>Exact diagram</title>") == len(paper.FIGURE_KEYS)
    assert '<span class="kpress-math kpress-math-inline"' in html
    assert 'class="kpress-footnotes"' in html
    assert "{{" not in markdown
    for name in ("MD", "PDF", "GITHUB"):
        assert f">{name}</a>" in html
    assert '<div class="doc-links screen-only">' in html
    assert 'href="https://github.com/jlevy/squares"' in html


def test_the_papers_head_is_the_sites_set_at_the_papers_own_address(
    rendered: tuple[str, str],
) -> None:
    """The paper's head carried a title and a description and nothing else, so a shared
    link to it previewed as a line of text. It is the site's one set now
    (`render_overview.head_tags`), written from the paper's record: an article, at the
    address its own path constant gives, with the day the article says it was revised."""
    html, _ = rendered
    url = render_overview.canonical_url(paper.SITE_PATH)
    assert url == render_overview.SITE_URL + paper.SITE_PATH
    assert check_published_site.head_problems(html, url) == []
    head = check_published_site.read_head(html)
    assert head.titles == (f"{paper.TITLE} · {render_overview.PROJECT_NAME}",)
    assert head.meta("og:title") == [paper.TITLE]
    assert head.meta("og:type") == ["article"]
    assert head.meta("description") == [paper.DESCRIPTION]
    assert not paper.DESCRIPTION.startswith(paper.TITLE)
    # The head says what the front says: the day the review was last revised, from the
    # release module, and no first publication, which the review does not record.
    meta = paper.page_meta()
    assert meta.modified == render_n11_lower_bounds_explainer.iso_date(
        release.OPTIMALITY_REVIEW_REVISED
    )
    assert head.meta("article:modified_time") == [meta.modified]
    assert meta.published == ""
    assert (meta.kind, meta.path) == ("article", paper.SITE_PATH)
    assert paper_front.revised(paper.FRONT) == release.OPTIMALITY_REVIEW_REVISED


def test_the_paper_ends_with_the_sites_closing_credit_without_its_version(
    rendered: tuple[str, str],
) -> None:
    """The paper's closing paragraph holds the two lines every page's footer is made of,
    the project and its repository, then the credit to the two tools, with no version
    between them: the paper's own version is in its credits, and the site's edition and
    the data hash go nowhere on a paper (the owner, 2026-10-01). The paper's version and
    dates are declared in `release.py`, which is therefore one of its declared inputs."""
    from devtools import render_overview  # noqa: PLC0415
    from sqpack.release import (  # noqa: PLC0415
        DATA_REVISION,
        DATA_REVISION_LENGTH,
        PUBLICATION_EDITION,
    )

    html, markdown = rendered
    footer = f'<p class="col colophon centred">{render_overview.colophon_lines(edition="")}</p>'
    assert html.count(footer) == 1
    assert html.count('class="site-colophon-line"') == 2
    assert footer.count('class="site-colophon-part"') == 3
    assert "Formatted and typeset with" in footer
    assert PUBLICATION_EDITION not in footer
    assert PUBLICATION_EDITION not in html
    assert PUBLICATION_EDITION not in markdown
    assert DATA_REVISION[:DATA_REVISION_LENGTH] not in markdown
    assert paper.PACKING / "src" / "sqpack" / "release.py" in paper.RENDER_INPUTS


def test_the_page_carries_the_sites_bar_with_papers_current(rendered: tuple[str, str]) -> None:
    """The paper is one of the site's papers, so it carries the site's navigation bar as
    the explainer does, through the shared helper: Papers is the current entry, the
    bar's links climb to the site's root from the directory the paper is served in, the
    gear's program and the embed script ride with it, and print hides the bar."""
    from devtools import render_overview  # noqa: PLC0415

    html, _ = rendered
    assert paper.SLUG == "n11-optimality-review"
    assert paper.SITE_PATH == "papers/n11-optimality-review.html"
    assert paper.SITE_PATH in render_overview.SITE_PAGES
    assert paper.SITE_PATH.count("/") == paper.SITE_ROOT.count("../") == 1
    assert render_overview.nav_html("papers", root="../") in html
    assert '<a data-page="papers" aria-current="page" href="../papers.html">Papers</a>' in html
    # One link is current, the bar's entry: the format chips link the other formats.
    assert len(re.findall(r'<a\b[^>]*\saria-current="page"', html)) == 1
    main = html.split('<main class="kpress-page-main kpress-viewport">', 1)[1]
    assert main.lstrip().startswith('<nav class="site-nav"')
    nav_css = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    assert nav_css in html
    # The shared text tokens come first, then the bar, then the publication layer both
    # papers share, which reads both, then this paper's own diagram rules.
    type_css = render_overview.PAPER_TYPE_CSS.read_text(encoding="utf-8")
    publication_css = paper.render_n11_lower_bounds_explainer.PUBLICATION_STYLE.read_text(
        encoding="utf-8"
    )
    paper_css = paper.STYLE.read_text(encoding="utf-8")
    order = [html.index(sheet) for sheet in (type_css, nav_css, publication_css, paper_css)]
    assert order == sorted(order)
    assert (
        "@media print {\n  .site-nav,\n  .kpress-site-header {\n    display: none;" in nav_css
    )
    for script in (render_overview.THEME_SCRIPT, render_overview.EMBED_SCRIPT):
        assert script.read_text(encoding="utf-8") in html, script.name
    for needed in (
        render_overview.PAPER_TYPE_CSS,
        render_overview.SITE_NAV,
        render_overview.SITE_NAV_CSS,
        render_overview.THEME_SCRIPT,
        render_overview.EMBED_SCRIPT,
    ):
        assert needed in paper.RENDER_INPUTS, needed.name
    # The page's hero starts the site's one space below the bar's rule, by the rule the
    # first paper's hero uses; this paper declares no top space of its own.
    assert "    padding-block-start: var(--site-page-top);\n" in publication_css
    assert "--site-page-top" not in paper_css


def test_the_paper_takes_the_publication_layer_and_the_sites_math_pipeline(
    rendered: tuple[str, str],
) -> None:
    """The paper draws its text and its mathematics as the explainer and every site page
    do, from the same sources. The publication layer is the stylesheet and the head
    script its math rule reads the platform from, both from
    `render_n11_lower_bounds_explainer.publication_layer` and both in the head: the paper once
    inlined the stylesheet alone, and on macOS every formula was drawn a sixth lighter than the
    explainer's (think-jc3w). The math pipeline is the explainer's, driven by the site pages'
    own script, and not KPress's auto-render entry points, which neither kern a function's name
    nor wait for a formula's faces."""
    from devtools import render_overview  # noqa: PLC0415

    html, _ = rendered
    head, body = html.split("</head>", 1)
    layer = paper.render_n11_lower_bounds_explainer.publication_layer()
    assert set(layer) == {"PUBLICATION_CSS", "NATIVE_MATH_METRICS"}
    for name, value in layer.items():
        assert head.count(value) == 1, name
    assert f"<script>{layer['NATIVE_MATH_METRICS']}</script>" in head
    static = paper.render_n11_lower_bounds_explainer.kpress_static()
    scripts = paper.math_scripts(static)
    assert scripts["KATEX_JS"] == paper.render_n11_lower_bounds_explainer.katex_js(static)
    assert scripts["SITE_MATH"] == render_overview.MATH_SCRIPT.read_text(encoding="utf-8")
    assert body.index(scripts["KATEX_JS"]) < body.index(scripts["SITE_MATH"])
    assert "squaresMath" in scripts["KATEX_JS"]
    for stock in ("katex/auto-render.min.js", "katex/katex-init.js"):
        assert (static / stock).read_text(encoding="utf-8") not in html, stock
    for needed in (
        render_overview.MATH_SCRIPT,
        paper.render_n11_lower_bounds_explainer.INLINE_SCRIPT_ASSETS["NATIVE_MATH_METRICS"],
        paper.render_n11_lower_bounds_explainer.PROBES
        / "render_n11_lower_bounds_explainer"
        / "host_math_init.js",
        paper.render_n11_lower_bounds_explainer.PROBES
        / "render_n11_optimality_review"
        / "typeset_all.js",
    ):
        assert needed.is_file()
        assert needed in paper.RENDER_INPUTS, needed.name


@pytest.mark.parametrize(
    "dropped",
    ["<script>{{NATIVE_MATH_METRICS}}</script>\n", "<script>{{SITE_MATH}}</script>\n"],
)
def test_a_shell_that_drops_half_of_a_shared_layer_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, dropped: str
) -> None:
    """A value the shell has no place for fails the render, so the stylesheet cannot be
    inlined without its head script, nor the math pipeline without its driver."""
    shell = paper.SHELL.read_text(encoding="utf-8")
    assert shell.count(dropped) == 1
    broken = tmp_path / paper.SHELL.name
    broken.write_text(shell.replace(dropped, ""), encoding="utf-8")
    monkeypatch.setattr(paper, "SHELL", broken)
    with pytest.raises(ValueError, match="values with no placeholder"):
        paper.render(SOURCE, figures=FIGURES, revision=REVISION, article=ARTICLE)


def test_a_caption_fact_the_article_does_not_use_is_refused() -> None:
    """The captions' facts are the article's list and the figure modules' alike: one the
    article does not name is refused, and one it names with no value is a leftover
    slot."""
    with pytest.raises(ValueError, match="caption facts unused"):
        paper.render(
            SOURCE, figures=FIGURES, revision=REVISION, article=ARTICLE, facts={"A": "1"}
        )
    used = SOURCE.replace("exact witness check</a>.", "exact witness check</a>, {{ROWS}} rows.")
    html, markdown = paper.render(
        used, figures=FIGURES, revision=REVISION, article=ARTICLE, facts={"ROWS": "32"}
    )
    assert "exact witness check</a>, 32 rows." in html
    assert "32 rows." in markdown
    with pytest.raises(ValueError, match="unresolved placeholders"):
        paper.render(used, figures=FIGURES, revision=REVISION, article=ARTICLE)


def test_a_captions_formula_is_typeset_and_kept_as_latex_in_the_markdown() -> None:
    source = SOURCE.replace(
        "exact witness check</a>.", "exact witness check</a>, $t_i \\le 1$."
    )
    html, markdown = paper.render(source, figures=FIGURES, revision=REVISION, article=ARTICLE)
    caption = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", html, re.DOTALL)
    assert caption is not None
    assert "$" not in caption.group(1)
    assert '<span class="kpress-math-render" aria-hidden="true">\\(t_i \\le 1\\)</span>' in (
        caption.group(1)
    )
    assert "exact witness check</a>, $t_i \\le 1$." in markdown


def test_link_revision_is_the_commit_the_paper_is_built_from(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The paper's citations name the checkout's `HEAD`, in full, and where git names no
    commit the renderer says so rather than writing a link no one can follow."""
    assert re.fullmatch(r"[0-9a-f]{40}", paper.link_revision())
    monkeypatch.setattr(paper, "REPO", tmp_path)
    with pytest.raises(SystemExit, match="give --revision"):
        paper.link_revision()


def test_local_citation_is_pinned(rendered: tuple[str, str]) -> None:
    html, markdown = rendered
    url = (
        "https://github.com/jlevy/squares/blob/"
        + REVISION
        + "/docs/project/reviews/review-2026-09-29-n11-optimality.md"
    )
    assert url in html
    assert url in markdown
    register_url = (
        "https://github.com/jlevy/squares/blob/" + REVISION + "/packing/frontier/results.yaml"
    )
    assert f"[register]: {register_url}" in markdown
    assert f'href="{register_url}"' in html
    witness_url = (
        "https://github.com/jlevy/squares/blob/"
        + REVISION
        + "/packing/cases/trump11/verify_exact.py"
    )
    assert f'<a href="{witness_url}"' in html
    assert ">exact witness check</a>" in html
    assert "[exact witness check](" not in html


@pytest.mark.parametrize(
    ("source", "figures"),
    [
        (SOURCE.replace("{{MASK_SVG}}", ""), FIGURES),
        (SOURCE + "\n{{MASK_SVG}}\n", FIGURES),
        (SOURCE, {**FIGURES, "EXTRA_SVG": SVG}),
        (SOURCE, {**FIGURES, "MASK_SVG": "<svg><script>bad</script></svg>"}),
    ],
)
def test_incomplete_or_active_figure_input_refuses(
    source: str, figures: dict[str, str]
) -> None:
    with pytest.raises(ValueError, match=r"figure|article|SVG"):
        paper.expanded_markdown(source, figures=figures, article=ARTICLE, revision=REVISION)


def test_relative_link_must_resolve_to_a_repo_file() -> None:
    unsafe = SOURCE.replace(
        "../../../docs/project/reviews/review-2026-09-29-n11-optimality.md",
        "../../../../etc/passwd",
    )
    with pytest.raises(ValueError, match="escapes repository"):
        paper.expanded_markdown(unsafe, figures=FIGURES, article=ARTICLE, revision=REVISION)


def test_missing_reference_target_refuses() -> None:
    missing = SOURCE.replace("../../frontier/results.yaml", "../../frontier/not-a-file.yaml")
    with pytest.raises(ValueError, match="does not exist"):
        paper.expanded_markdown(missing, figures=FIGURES, article=ARTICLE, revision=REVISION)


def test_the_paper_is_written_under_papers_by_its_slug(
    tmp_path: Path, rendered: tuple[str, str]
) -> None:
    """Given the site's root, a render writes the page and its Markdown under `papers/`,
    beside each other under the paper's slug, and the format chips name the Markdown and
    the PDF by that slug, so each is a file beside the page. It writes no landing page:
    the directory the paper used to be served from is the overview build's to forward
    (`render_overview.MOVED_PAGES`)."""
    from devtools import render_overview  # noqa: PLC0415

    html, markdown = rendered
    outputs = paper.output_files(tmp_path, html, markdown)
    assert {path.relative_to(tmp_path).as_posix(): text for path, text in outputs.items()} == {
        "papers/n11-optimality-review.html": html,
        "papers/n11-optimality-review.md": markdown,
    }
    assert 'href="n11-optimality-review.md"' in html
    assert 'href="n11-optimality-review.pdf"' in html
    assert "t-060-explainer" not in html
    moved = dict(render_overview.MOVED_PAGES)
    assert moved["n11-optimality/t-060-explainer.html"] == paper.SITE_PATH
    assert moved["n11-optimality/index.html"] == paper.SITE_PATH


def test_actual_article_renders_all_retained_figures_and_pinned_sources() -> None:
    html, markdown = paper.render(
        paper.ARTICLE.read_text(encoding="utf-8"),
        figures=paper.render_all_figures(),
        facts=paper.render_all_facts(),
        revision=REVISION,
    )
    assert "A Review of the Optimality Proof of the Trump Packing of 11 Squares" in html
    assert len(re.findall(r"<figure\b", html)) == 11
    assert len(re.findall(r"<figcaption\b", html)) == 11
    assert (
        html.count("<svg") >= len(paper.FIGURE_KEYS) + 1
    )  # article figures and KPress icon sprite
    captions = re.findall(r"<figcaption[^>]*>(.*?)</figcaption>", html, re.DOTALL)
    assert len(captions) == 11
    assert all("$" not in caption for caption in captions)
    # A caption's formulas are KPress math, typeset by the page as the prose's are, and
    # the Markdown edition keeps them as LaTeX; none is written as text any more.
    assert (
        sum(caption.count('class="kpress-math kpress-math-inline"') for caption in captions)
        >= 12
    )
    written = re.findall(r"<figcaption>(.*?)</figcaption>", markdown, re.DOTALL)
    assert sum(caption.count("$") for caption in written) >= 24
    assert not UNICODE_MATH.search("".join(written))
    # Each count a caption states is the figure module's, from its receipt.
    facts = paper.render_all_facts()
    assert set(facts) == {
        "CAPACITY_CELL",
        "LOCAL_BRANCHES",
        "LOCAL_MARGINS",
        "ROW_UPDATE_ROWS",
        "ROW_CASE_UPDATES",
        "D4_BAN_REGIONS",
        "D4_REGIONS",
        "D4_BANS",
        "LOCAL_RADII_TABLE",
        "ROLE_MAP_TABLE",
        "COVER_SITES_TABLE",
    }
    said = " ".join(" ".join(caption.split()) for caption in written)
    for phrase in (
        f"cell {facts['CAPACITY_CELL']}, comes from the exact cover",
        f"one of {facts['ROW_UPDATE_ROWS']} in its update",
        f"{facts['ROW_CASE_UPDATES']} complete updates exclude case 2095",
        f"overlay regions {facts['D4_BAN_REGIONS']} is below 1",
        f"over {facts['D4_REGIONS']} closed regions and {facts['D4_BANS']} bans",
        f"{facts['LOCAL_MARGINS']} exact margins over {facts['LOCAL_BRANCHES']} branches",
    ):
        assert phrase in said, phrase
    # The first figure is set as the first paper sets its own: the drawing alone in a
    # centred stage, linked to the rendering it is cut from, its caption under it.
    first = html.split("<figure", 2)[1]
    assert '<div class="stage trump"><a href="https://github.com/jlevy/squares/blob/' in first
    assert f"/blob/{REVISION}/packing/atlas/rendering/trump11-overview.svg" in first
    assert "<text" not in first
    assert "<pre><code><svg" not in html
    assert "kpress-math-render" in html
    assert "{{" not in markdown
    assert not re.search(r"[\ue000-\uf8ff]", html + markdown)
    assert "../../resources/" not in markdown
    assert f"/blob/{REVISION}/packing/resources/" in markdown
    assert markdown.count(f"/blob/{REVISION}/") >= 39


def test_a_diagram_drawn_in_fixed_ink_keeps_a_light_ground_on_the_dark_theme() -> None:
    """The page carries the site's theme control, so a diagram is read on the dark theme
    too. One drawn in the theme's tokens follows it; one painted in fixed colours, its
    labels and its dark strokes among them, needs a light ground there, or it is dark on
    dark. The stylesheet's list of diagrams that take that ground is exactly the diagrams
    that carry a fixed colour, and it keys on KPress's resolved theme, as every site
    stylesheet does."""
    fixed, themed = set(), set()
    for svg in paper.render_all_figures().values():
        found = re.match(r'<svg\b[^>]*\bclass="n11-diagram (n11-[a-z-]+)"', svg)
        if found is None:
            continue  # Figure 1, the atlas's rendering, which carries no lettering.
        ink = re.findall(r'\b(?:fill|stroke)="(#[0-9a-fA-F]{3,6})"', svg)
        (fixed if ink else themed).add(found.group(1))
    assert fixed, "no diagram carries fixed ink: the ground rule has nothing to hold"
    assert themed, "no diagram follows the theme: the rule would apply to every diagram"
    css = paper.STYLE.read_text(encoding="utf-8")
    # The ground is a token, as every colour is (`devtools.check_colour_tokens`,
    # 2026-10-03), and the token is white.
    assert "--n11-diagram-ground: oklch(100% 0 0);" in css
    rule = re.search(
        r':root\[data-kpress-resolved-theme="dark"\]\s+\.n11-paper\s+:is\(([^)]*)\)\s*'
        r"\{\s*background: var\(--n11-diagram-ground\);\s*\}",
        css,
    )
    assert rule is not None
    listed = {name.strip().removeprefix(".") for name in rule.group(1).split(",")}
    assert listed == fixed
    assert "prefers-color-scheme" not in css


def test_the_front_is_the_shared_components_in_the_owners_form(
    rendered: tuple[str, str],
) -> None:
    """The article carries one slot for its front, and the page and the Markdown edition
    take it from `paper_front`, written from this paper's record: the original proof
    first, by its author's name in bold and then its address as a plain link; this
    review's own credits a line's space below, names in bold; the draft's version not
    bold, with no history to link; then the dates. The credits' column and the space
    before a paper's own credits are the publication layer's, so the paper's own sheet
    says nothing about them."""
    article = paper.ARTICLE.read_text(encoding="utf-8")
    assert article.count("{{FRONT_MATTER}}") == 1
    assert '<div class="credits' not in article
    assert "doc-links" not in article
    assert "doc-links" not in paper.SHELL.read_text(encoding="utf-8")
    assert ".credits" not in paper.STYLE.read_text(encoding="utf-8")
    html, markdown = rendered
    address = "github.com/Queuingtheorydotcom/11SquaresOptimal"
    oversight = '<a href="https://x.com/ojoshe" target="_blank" rel="noopener noreferrer">'
    block = html.split('<div class="credits centred">', 1)[1].split("</div>", 1)[0]
    assert [line.strip() for line in block.strip().splitlines()] == [
        (
            '<span class="credits-source">From the original proof by '
            "<strong>Queuingtheorydotcom</strong></span>"
        ),
        (
            f'<span class="credits-source"><a href="https://{address}" target="_blank" '
            f'rel="noopener noreferrer">{address}</a></span>'
        ),
        (
            f'<span class="credits-own">Human oversight: {oversight}'
            "<strong>Joshua Levy</strong></a></span>"
        ),
        "<span>Agents: <strong>GPT-6 Astra</strong> and <strong>GPT-6 Sol</strong></span>",
        (
            f'<span class="edition">{release.OPTIMALITY_REVIEW_EDITION} '
            '(<a href="#version-history">version history</a>)</span>'
        ),
        (
            '<span class="publication-date">'
            f"Original proof {release.OPTIMALITY_PROOF_PUBLISHED} · "
            f"Last revised {release.OPTIMALITY_REVIEW_REVISED}</span>"
        ),
    ]
    assert html.index('<div class="doc-links screen-only">') < html.index('<div class="hero">')
    shared = paper.render_n11_lower_bounds_explainer.PUBLICATION_STYLE.read_text(
        encoding="utf-8"
    )
    assert "  grid-template-columns: minmax(0, 1fr);\n" in shared
    assert ".credits a {\n  overflow-wrap: anywhere;\n}" in shared
    assert (
        ".credits .credits-source + .credits-own,\n.credits .publication-date {\n"
        "  margin-block-start: 1lh;\n}"
    ) in shared
    assert markdown.startswith(
        f"# {paper.TITLE}\n\n- From the original proof by **Queuingtheorydotcom**\n"
        f"- [{address}](https://{address})\n"
        "- Human oversight: [**Joshua Levy**](https://x.com/ojoshe)\n"
        "- Agents: **GPT-6 Astra** and **GPT-6 Sol**\n"
        f"- {release.OPTIMALITY_REVIEW_EDITION} ([version history](#version-history))\n"
        f"- Original proof {release.OPTIMALITY_PROOF_PUBLISHED} · "
        f"Last revised {release.OPTIMALITY_REVIEW_REVISED}\n\n"
    )
    assert "doc-links" not in markdown
    assert '<div class="hero">' not in markdown


def test_a_table_keeps_to_the_column_and_scrolls_inside_its_wrap() -> None:
    """The shared column rule caps a block at the measure, which outranks KPress's cap on
    a table's wrap, so on a phone the wrap ran past the article that clips it. The
    paper's own rule caps the wrap at the column too, later in the page and at a higher
    specificity than the shared rule, and the page has tables for it to hold.
    `preview_site --clips` measures the result in the browser."""
    css = paper.STYLE.read_text(encoding="utf-8")
    cap = "max-width: min(100%, calc(var(--kpress-measure) + 2 * var(--kpress-column-inset)));"
    assert f".cert-page.n11-paper > .kpress-table-wrap {{\n  {cap}\n}}" in css
    shared = paper.render_n11_lower_bounds_explainer.PUBLICATION_STYLE.read_text(
        encoding="utf-8"
    )
    assert ".cert-page > :not(figure, .cert-figure, .kpress-figure),\n.col {" in shared
    html, _ = paper.render(
        paper.ARTICLE.read_text(encoding="utf-8"),
        figures=paper.render_all_figures(),
        facts=paper.render_all_facts(),
        revision=REVISION,
    )
    assert html.index(shared) < html.index(css)
    article = html.split('<article class="kpress kpress-doc kpress-prose cert-page n11-paper">')
    assert len(article) == 2
    # The branch table, the frame legend, the role map, the two tables of Appendix C
    # and the version history: each is wrapped, and the wrap is what the rule caps.
    assert len(re.findall(r'<div class="kpress-table-wrap"><table\b', article[1])) == 6


@pytest.mark.skipif(
    os.environ.get("SQPACK_N11_OPTIMALITY_REVIEW_BROWSER") != "1",
    reason="the dedicated T-060 Pages job sets SQPACK_N11_OPTIMALITY_REVIEW_BROWSER=1",
)
def test_pdf_refuses_a_math_host_without_rendered_katex(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    html = tmp_path / "unrendered.html"
    html.write_text('<html><body><span class="kpress-math">raw TeX</span></body></html>')
    pdf = tmp_path / "unrendered.pdf"
    monkeypatch.setattr(paper, "MATH_WAIT_MS", 200)
    with pytest.raises(ValueError, match="unrendered math"):
        paper._print_pdf(html, pdf)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    assert not pdf.exists()


@pytest.mark.skipif(
    os.environ.get("SQPACK_N11_OPTIMALITY_REVIEW_BROWSER") != "1",
    reason="the dedicated T-060 Pages job sets SQPACK_N11_OPTIMALITY_REVIEW_BROWSER=1",
)
def test_a_print_can_ask_for_every_formula_at_once(tmp_path: Path) -> None:
    """The site's math driver typesets the formulas near the window and leaves the rest
    to the browser's idle time, after the page and its fonts have loaded. A print does
    not wait for that: asked through the probe `_print_pdf` evaluates, the driver
    typesets every formula, three hundred paragraphs down included, before it answers.
    The page is read as soon as its markup is parsed, when the far formulas are still
    waiting, so the answer is the probe's doing."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    far = "\n\n".join(f"Paragraph {index} holds $z_{{{index}}}^9$." for index in range(300))
    html, _ = paper.render(
        SOURCE + "\n\n" + far + "\n", figures=FIGURES, revision=REVISION, article=ARTICLE
    )
    page_path = tmp_path / "far.html"
    page_path.write_text(html, encoding="utf-8")
    untypeset = ".kpress-math:not([data-kpress-math-rendered])"
    with sync_playwright() as driver:
        browser = driver.chromium.launch()
        try:
            page = browser.new_page()
            page.goto(page_path.as_uri(), wait_until="domcontentloaded")
            assert page.locator(untypeset).count() > 0
            page.evaluate(TYPESET_ALL)
            assert page.locator(untypeset).count() == 0
        finally:
            browser.close()


@pytest.mark.skipif(
    os.environ.get("SQPACK_N11_OPTIMALITY_REVIEW_BROWSER") != "1",
    reason="the dedicated T-060 Pages job sets SQPACK_N11_OPTIMALITY_REVIEW_BROWSER=1",
)
def test_radical_svg_has_print_geometry(tmp_path: Path) -> None:
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    with sync_playwright() as driver:
        html, _ = paper.render(
            SOURCE.replace("$x^2$", r"$\sqrt2$"),
            figures=FIGURES,
            revision=REVISION,
            article=ARTICLE,
        )
        page_path = tmp_path / "radical.html"
        page_path.write_text(html, encoding="utf-8")
        browser = driver.chromium.launch()
        try:
            page = browser.new_page()
            page.goto(page_path.as_uri(), wait_until="networkidle")
            page.emulate_media(media="print")
            radical = page.locator(".katex .sqrt svg").first
            radical.wait_for(state="visible")
            box = radical.bounding_box()
            assert box is not None
            assert box["width"] > 1
            assert box["height"] > 1
        finally:
            browser.close()


#: The diagrams that keep their width on a phone and scroll inside their figure: their
#: lettering, shrunk to the column, would not read (think-wzc1).
SCROLLED_ON_A_PHONE = {"n11-diagram n11-capture", "n11-diagram n11-mechanism-charge"}


@pytest.mark.skipif(
    os.environ.get("SQPACK_N11_OPTIMALITY_REVIEW_BROWSER") != "1",
    reason="the dedicated T-060 Pages job sets SQPACK_N11_OPTIMALITY_REVIEW_BROWSER=1",
)
def test_diagram_labels_keep_publication_sizes_through_viewbox_scale(tmp_path: Path) -> None:
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    html, _ = paper.render(
        paper.ARTICLE.read_text(encoding="utf-8"),
        figures=paper.render_all_figures(),
        facts=paper.render_all_facts(),
        revision=REVISION,
    )
    page_path = tmp_path / "diagram-roles.html"
    page_path.write_text(html, encoding="utf-8")
    measure = probe(PROBES, "render_n11_optimality_review/diagram_roles")
    with sync_playwright() as driver:
        browser = driver.chromium.launch()
        try:
            views: tuple[tuple[int, Literal["screen", "print"]], ...] = (
                (1280, "screen"),
                (390, "screen"),
                (1280, "print"),
            )
            for width, media in views:
                page = browser.new_page(viewport={"width": width, "height": 900})
                page.goto(page_path.as_uri(), wait_until="networkidle")
                page.emulate_media(media=media)
                page.wait_for_function(measure, arg={"readyOnly": True})
                roles = page.evaluate(measure, {"readyOnly": False})
                # Every diagram that carries a label: the construction and the capacity
                # drawing carry none.
                assert len(roles) == len(paper.FIGURE_KEYS) - 2
                for role in roles:
                    assert not role["overflowingLabels"], (width, media, role)
                    assert abs(role["label"] - role["support"]) < 0.1, (width, media, role)
                    if role["note"] is not None:
                        assert role["caption"] is not None
                        assert abs(role["note"] - role["caption"]) < 0.1, (
                            width,
                            media,
                            role,
                        )
                # On a phone a diagram takes the column where it reasonably can, its
                # labels shrunk with it, and the two whose lettering would not read so
                # keep their width and scroll (the owner, 2026-10-03, think-wzc1).
                scrolled = {
                    role["name"] for role in roles if role["scrollWidth"] > role["clientWidth"]
                }
                if width == 390:
                    assert scrolled == SCROLLED_ON_A_PHONE, (width, media, scrolled)
                    for role in roles:
                        fitted = role["name"] not in SCROLLED_ON_A_PHONE
                        assert (role["shrink"] < 1) == fitted, (width, media, role)
                else:
                    assert not scrolled, (width, media, scrolled)
                    assert all(role["shrink"] == 1 for role in roles)
                page.close()
        finally:
            browser.close()


#: Mathematics written as text, which a caption once had to be: the relations, Greek
#: letters, subscripts and minus sign the sans face does not carry.
UNICODE_MATH = re.compile("[\u2264\u2265\u03c4\u03b8\u1d62\u1d67\u2081\u2085\u00b2\u2212]")
#: The article's `s(11)=T` as the site's pipeline typesets it.
KERNED = r"s\mkern1mu(11)=T"
#: Mathematics on each surface the paper sets it on: prose, a sans heading, a table's
#: cells, a display, and a footnote. `s(11)` is a function's name before a bracket,
#: which the site's pipeline kerns by one mu.
MATH_SURFACES = """

### A sans heading with $n = 11$

The side is $s(11)=T$.[^side]

| Branch | Verdict |
| --- | --- |
| $y_{15}\\le5/4$ | $u^2<1$ |

$$
\\left\\|\\lambda^{\\top}A-\\sigma e_j^{\\top}\\right\\|_1\\le\\epsilon_j.
$$

[^side]: Where $T$ is the side of the construction.
"""


@pytest.mark.skipif(
    os.environ.get("SQPACK_N11_OPTIMALITY_REVIEW_BROWSER") != "1",
    reason="the dedicated T-060 Pages job sets SQPACK_N11_OPTIMALITY_REVIEW_BROWSER=1",
)
def test_formulas_are_drawn_as_their_text_is_on_macos_and_linearly_elsewhere(
    tmp_path: Path,
) -> None:
    """The paper told it is on macOS and told it is not, on whatever machine this runs:
    on macOS the head script stamps the root and every formula is rasterised as the text
    around it; elsewhere it keeps the publication layer's linear advances. On both,
    every formula is typeset, at its text's size, colour and weight, in the face its
    text is in, from faces the page ships, with the function's name kerned."""
    html, _ = paper.render(
        SOURCE + MATH_SURFACES, figures=FIGURES, revision=REVISION, article=ARTICLE
    )
    (tmp_path / "paper.html").write_text(html, encoding="utf-8")
    for platform, flag, rendering in (
        ("MacIntel", "true", "auto"),
        ("Linux x86_64", None, "geometricprecision"),
    ):
        (found,) = measure.measure_glyphs(
            tmp_path.as_uri(),
            ("paper.html",),
            widths=(1280,),
            platform=platform,
            tex=(KERNED,),
            every_ink=False,
        )
        assert found["platform"] == platform
        assert found["root"].get(measure.NATIVE_METRICS) == flag, platform
        assert measure.glyph_problems(found, katex=measure.shipped_katex()) == [], platform
        formulas = {(row["surface"], row["layout"]): row for row in found["math"]}
        assert set(formulas) == {
            ("prose", "inline"),
            ("prose", "display"),
            ("heading", "inline"),
            ("table cell", "inline"),
            ("footnote", "inline"),
        }
        assert {row["text_rendering"] for row in found["math"]} == {rendering}, platform
        sans = {
            surface
            for (surface, _), row in formulas.items()
            if row["math"] == measure.SANS_MATH
        }
        assert sans == {"heading", "table cell", "footnote"}
        assert [row["example"] for row in found["math"] if row["compared"]] == [KERNED]


def test_new_figure_dependencies_are_declared_to_publication_scope() -> None:
    for source in (*mechanism.RENDER_INPUTS, *overview.RENDER_INPUTS):
        assert any(
            source == declared or (declared.is_dir() and source.is_relative_to(declared))
            for declared in paper.RENDER_INPUTS
        ), source
