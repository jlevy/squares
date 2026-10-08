"""The explainer renders, and what it renders fetches nothing.

`devtools.render_n11_lower_bounds_explainer` was exercised only by the Pages workflow, on the
pull requests whose paths its filters name; nothing in the suite rendered the page. A full
render is under a second, so it runs here, and the two properties the workflow used to grep for
are asserted on the string the renderer returns: no placeholder survived substitution, and
nothing in the page is a reference outside it.
"""

from __future__ import annotations

import posixpath
import re
from dataclasses import replace
from fnmatch import fnmatchcase
from fractions import Fraction
from pathlib import Path
from urllib.parse import urljoin

import pytest
import tinycss2

from devtools import (
    check_published_site,
    paper_links,
    render_n11_lower_bounds_explainer,
    render_overview,
)
from devtools.render_n11_lower_bounds_explainer import (
    ATLAS,
    BEST_RENDERING,
    CASE,
    COMPOSITE_ASSETS,
    COMPOSITE_CARD,
    COMPOSITE_PNG,
    GENERATOR,
    MARKDOWN_OUTPUT,
    OUTPUT,
    PAGE_URL,
    RENDER_INPUTS,
    REPO,
    RESULT_ID,
    SITE,
    SITE_PATH,
    SITE_ROOT,
    SITE_URL,
    SLUG,
    THIRDPARTY,
    VERIFIER,
    WALKTHROUGH,
    assert_self_contained,
    current_bound_facts,
    png_size,
    render,
)
from devtools.render_n11_lower_bounds_explainer import load_certificate as load
from devtools.render_n11_lower_bounds_explainer_pdf import OUTPUT as PDF_OUTPUT
from devtools.render_overview import PAPERS_DIR, SITE_PAGES
from devtools.repo_links import REPO_URL
from sqpack.release import (
    DATA_REVISION,
    DATA_REVISION_LENGTH,
    EXPLAINER_FIRST_PUBLISHED,
    EXPLAINER_HISTORY,
    EXPLAINER_REVISED,
    EXPLAINER_VERSION,
    PUBLICATION_EDITION,
    PUBLICATION_HISTORY,
    PUBLICATION_STAMP,
    PUBLICATION_VERSION,
    edition_at,
)
from sqpack.yamlio import safe_load
from workbench_tools.build_site import NOTE as WORKBENCH_NOTE
from workbench_tools.build_site import RENDER_INPUTS as WORKBENCH_INPUTS
from workbench_tools.build_site import build_metadata as workbench_build_metadata


@pytest.fixture(scope="module")
def rendered():
    return render(WALKTHROUGH)


@pytest.fixture(scope="module")
def page(rendered) -> str:
    return rendered.page


@pytest.fixture(scope="module")
def document(rendered) -> str:
    return rendered.markdown


def test_the_page_renders_every_walkthrough_certificate(page: str) -> None:
    """Each certificate's slug is in the page: its switch button and its figure copies."""

    for path in WALKTHROUGH:
        certificate, _ = load(path)
        fragment = f"{certificate.outer_side.numerator}-{certificate.outer_side.denominator}"
        assert f'data-cert="{fragment}"' in page, fragment


def test_default_figures_reserve_their_place_before_any_script_runs(page: str) -> None:
    """All-hidden source markup used to insert thousands of pixels after first paint."""
    wrappers = re.findall(r'<div class="cert-figure" data-cert="([^"]+)"([^>]*)>', page)
    assert wrappers
    default = render_n11_lower_bounds_explainer.slug(
        render_n11_lower_bounds_explainer.derive(WALKTHROUGH[0])
    )
    assert any(cert == default for cert, _attrs in wrappers)
    for cert, attrs in wrappers:
        assert ("hidden" not in attrs) is (cert == default)


def test_no_placeholder_survives_substitution(page: str) -> None:
    assert re.findall(r"\{\{[A-Z_]+\}\}", page) == []


def test_the_explainer_ends_with_the_sites_closing_credit_without_its_version(
    page: str,
) -> None:
    """The explainer's closing paragraph holds the two lines every page's footer is made
    of (`render_overview.colophon_lines`): the project and its repository, then the
    credit to Flowmark and KPress, with no version between them. The paper's own version
    is in its credits, and the site's edition goes on no paper (the owner, 2026-10-01).
    The paragraph keeps the paper's own class, and so its type and its print rules."""
    footer = f'<p class="col colophon centred">{render_overview.colophon_lines(edition="")}</p>'
    assert page.count(footer) == 1
    assert page.count('class="site-colophon-line"') == 2
    assert footer.count('class="site-colophon-part"') == 3
    assert '<a href="https://github.com/jlevy/squares">github.com/jlevy/squares</a>' in footer
    assert "Formatted and typeset with" in footer
    assert PUBLICATION_EDITION not in footer
    assert re.search(r"v\d+\.\d+\.\d+", footer) is None


def test_the_bar_marks_papers_current_on_the_explainer(page: str) -> None:
    """The explainer is one of the site's papers: the bar has no entry of its own for it,
    Papers is the one marked current, and the page is served under `papers/` by its slug,
    so the bar's links climb one level to the site's root. The bar is the site's one
    partial, so its entries stand in the order every other page has them."""
    assert page.count(render_overview.nav_html("papers", root=SITE_ROOT)) == 1
    assert re.findall(r'<a data-page="(\w+)" aria-current="page"', page) == ["papers"]
    assert '<a data-page="papers" aria-current="page" href="../papers.html">Papers</a>' in page
    assert 'data-page="explainer"' not in page
    assert SLUG == "n11-lower-bounds-explainer"
    assert f"papers/{SLUG}.html" == SITE_PATH
    assert f"{SITE_URL}{SITE_PATH}" == PAGE_URL
    assert OUTPUT == SITE / SITE_PATH
    assert {"papers.html", SITE_PATH} <= set(SITE_PAGES)
    assert "explainer.html" not in SITE_PAGES


def test_title_block_names_the_result_without_a_subtitle(page: str, document: str) -> None:
    """The title stands alone; the exact theorem is typeset in the opening section. Its
    `n = 11` is a math run, so the hero's caps leave the variable lowercase, and the run
    never breaks after its relation, as it did at phone width."""
    heading = re.search(r"<h1\b.*?</h1>", page, re.DOTALL)
    assert heading is not None
    assert re.sub(r"<[^>]+>", "", heading.group(0)) == render_n11_lower_bounds_explainer.TITLE
    assert '<span class="tex">n = 11</span></h1>' in heading.group(0)
    rule = (
        ".hero h1 .tex,\n.hero h1 .kpress-math {\n  letter-spacing: 0;\n"
        "  text-transform: none;\n  white-space: nowrap;\n}"
    )
    assert rule in page
    assert '<p class="subtitle centred">' not in page
    assert "Weighted Certificates for Square Packing" not in page
    current = current_bound_facts()
    theorem = (
        "$$\ns(11) \\;\\ge\\; L = "
        f"{current.bounded_side_tex} = {current.bounded_side_decimal}.\n$$"
    )
    assert theorem in document


@pytest.mark.parametrize(
    ("paths", "comparison", "pinned_check"),
    [
        (WALKTHROUGH[:1], False, False),
        (WALKTHROUGH, True, True),
        (WALKTHROUGH[::-1], False, True),
        (WALKTHROUGH[1:], False, True),
    ],
    ids=["single", "both", "headline-first", "headline-only"],
)
def test_certificate_comparisons_match_the_rendered_certificates(
    paths: tuple[Path, ...], *, comparison: bool, pinned_check: bool
) -> None:
    rendered = render(paths)
    document = " ".join(rendered.markdown.split())
    assert ("simpler certificate for the weaker bound" in document) is comparison
    assert ("It checks the simpler point example at $19/5$." in document) is comparison
    assert ("The figures below illustrate this certificate." in document) is not comparison
    assert "the theorem written out, the 19/5 certificate as plain data" in document
    assert ("one-file checker" in document) is pinned_check
    assert ("T-022" in document) is pinned_check
    assert "gap left by the certificates explained here" in document
    assert "what remains unknown about" not in document
    assert "A certificate written by a wrong program" not in document
    assert (
        "The verifier rejects a point certificate that fails the conditions, "
        "regardless of how it was generated."
    ) in document
    assert "{{" not in rendered.markdown
    if len(paths) != 1:
        return
    facts = render_n11_lower_bounds_explainer.derive(paths[0])
    assert f"{len(facts.atoms):,} rationally weighted points" in document
    assert f"{facts.steps + 1} rationally parameterized" in document
    assert (
        f"weighted points reach ${render_n11_lower_bounds_explainer.decimal(facts.outer_side)}$"
        in document
    )


def test_the_explainer_carries_the_site_theme_control(page: str) -> None:
    """The explainer's nav ends in the same gear as every other page, and its script
    runs after the nav is drawn."""
    script = render_n11_lower_bounds_explainer.INLINE_SCRIPT_ASSETS["SITE_THEME"].read_text(
        encoding="utf-8"
    )
    assert page.count('class="site-theme-button"') == 1
    assert page.index('class="site-theme-button"') < page.index(script)
    assert 'stored("kpress.theme")' in page


def test_the_page_is_self_contained(page: str) -> None:
    """The renderer's own check passes on its own output; the workflow relies on this.

    The page carries exactly two `<link>`s: the canonical URL and the site icon as a
    data URI. Neither is a fetch -- a browser reads the one and carries the other's bytes
    -- but each could become one, so they are counted rather than merely permitted: a
    third `<link>` arriving here is a stylesheet, an icon at an address or a preload,
    and the count fails before the refusal has to.
    """

    assert_self_contained(page)
    assert re.findall(r"<link[^>]*>", page) == [
        f'<link rel="canonical" href="{PAGE_URL}">',
        render_overview.favicon_html(inline=True),
    ]
    assert re.search(r"<script[^>]*\ssrc=", page) is None


@pytest.mark.parametrize(
    "fragment",
    [
        '<script src="https://cdn.example/x.js"></script>',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=X">',
        "<style>@import url(https://example.org/a.css);</style>",
        "<style>body { background: url(https://example.org/a.png) }</style>",
        "<style>body { background: url('//example.org/a.png') }</style>",
        # The canonical exemption is the exact quoted form the shell emits and nothing
        # wider: every other rel is still a fetch, and a rel that merely contains the
        # word does not buy its way past.
        '<link rel="preload" as="font" href="https://example.org/a.woff2">',
        '<link rel="icon" href="https://example.org/favicon.png">',
        '<link rel="canonical stylesheet" href="https://example.org/a.css">',
        "<link rel=canonical href=https://example.org/>",
    ],
)
def test_an_external_reference_is_refused(fragment: str) -> None:
    with pytest.raises(SystemExit, match="not self-contained"):
        assert_self_contained(f"<html><body>{fragment}</body></html>")


@pytest.mark.parametrize(
    "fragment",
    [
        "<style>@font-face { src: url(data:font/woff2;base64,AAAA) }</style>",
        "<style>.a { fill: url(#gradient) }</style>",
        '<style>.b { background: url("data:image/svg+xml,%3Csvg%3E") }</style>',
        # Metadata for a crawler, read off the markup and never requested to display
        # the page. Both forms are outward addresses on purpose: a preview consumer
        # resolves them on its own machine and drops a relative one.
        '<link rel="canonical" href="https://jlevy.github.io/squares/">',
        '<meta property="og:image" content="https://jlevy.github.io/squares/a.png">',
    ],
)
def test_a_data_uri_or_fragment_is_not_a_fetch(fragment: str) -> None:
    assert_self_contained(f"<html><body>{fragment}</body></html>")


def test_the_published_document_is_markdown_and_not_the_template(document: str) -> None:
    """The chip offers this file, so it has to be the article rather than its source.

    The template states no bound: every number in it is a `{{PLACEHOLDER}}`, and the
    chip used to link to it. What is published is the same document with the
    certificate's own values in place, and it has to survive being read as text.
    """
    assert "{{" not in document
    assert "3.81" in document
    assert "1,121" in document
    assert "181" in document
    assert document.startswith("# New Lower Bounds for Square Packing for $n = 11$\n")


def test_the_three_stage_guide_wraps_each_print_grid_item_in_a_paragraph(page: str) -> None:
    """KPress's print list grid needs one element child for each item's prose.

    A tight Markdown list leaves the text after its opening ``strong`` as an anonymous
    grid item. Chromium then auto-places that text in the 2.5rem number column, producing
    several pages of nearly one-character-wide lines. A loose list wraps each complete
    item in one paragraph, which the print stylesheet explicitly places in column two.
    """

    guide = re.search(
        r"We explain the proof in three stages:</p>\s*<ol>(.*?)</ol>", page, re.DOTALL
    )
    assert guide is not None
    items = re.findall(r"<li>(.*?)</li>", guide.group(1), re.DOTALL)
    assert len(items) == 3
    for item in items:
        assert re.fullmatch(r"\s*<p>.*</p>\s*", item, re.DOTALL)


def test_the_published_document_carries_no_html(document: str) -> None:
    """A canvas, a control panel and a drawn diagram are apparatus, not prose.

    None of them means anything in a text file, and together they were seventy per cent
    of the bytes. What a figure says is in its caption, so a figure here is its caption.
    """
    assert not re.search(r"</?[a-zA-Z][^>]*>", document)
    for number in (1, 3):
        assert f"**Figure {number}." in document


def test_the_published_document_states_each_figure_once(document: str) -> None:
    """The page carries a copy per certificate and switches between them; text cannot.

    Stating the same figure twice, once per certificate, reads as a duplication rather
    than as a choice, so only the certificate the page opens on is kept.
    """
    # A caption's bold lead carries the figure's own subtitle, so it is matched by
    # its number rather than by an exact string.
    for number in range(1, 8):
        assert document.count(f"**Figure {number}.") == 1, number


def test_figure_two_counts_stars_in_its_own_composite(monkeypatch: pytest.MonkeyPatch) -> None:
    """Stars beyond the first hundred must not enter Figure 2's caption."""
    whole_corpus = {"lower_bound_recent_result": 23, "lower_bound_first_proved_here": 5}
    record = {
        "totals": whole_corpus,
        "composites": [
            {
                "stem": render_n11_lower_bounds_explainer.POSTER_STEM.name,
                "totals": whole_corpus,
            },
            {
                "stem": render_n11_lower_bounds_explainer.COMPOSITE_STEM.name,
                "totals": {"lower_bound_recent_result": 7, "lower_bound_first_proved_here": 2},
            },
        ],
    }
    monkeypatch.setattr(render_n11_lower_bounds_explainer, "load_figure_record", lambda: record)

    document = " ".join(render(WALKTHROUGH).markdown.split())
    assert "7 of the hundred, 2 of them here" in document
    assert "23 of the hundred" not in document
    assert "includes 2 new lower bounds proved here" in document


def test_figure_three_marks_the_verified_lower_bound_beside_the_packing(
    page: str, document: str
) -> None:
    """T-060's exact endpoint joins Trump's tick; older certificates keep their band."""
    header = (REPO / "packing/frontier/n-011.md").read_text(encoding="utf-8").split("---", 2)
    packing = safe_load(header[1])["packing"]
    recorded = packing["verified_lower_bound"]
    verified = render_n11_lower_bounds_explainer.verified_lower_bound(11)
    assert verified.value == Fraction(recorded["value"])
    assert recorded["exact_form"] == packing["verified_upper_bound"]["exact_form"]
    assert render_n11_lower_bounds_explainer.n11_solved(verified)
    assert verified.display == "3.8770835…"
    assert verified.credit == "Queuingtheorydotcom after Levy et al. 2026"

    best_x = round(
        render_n11_lower_bounds_explainer.line_x(
            float(render_n11_lower_bounds_explainer.BEST_PACKING)
        )
    )
    assert f'<line x1="{best_x}" y1="24" x2="{best_x}" y2="76"' in page
    assert f'<line x1="{best_x}" y1="56"' not in page
    assert "one exact optimum endpoint shared by the T-060 lower proof" in page
    figure = page.split('<div class="line-fig kpress-diagram">', 1)[1].split("</div>", 1)[0]
    assert "<pre" not in figure
    assert "<code" not in figure
    assert '<line x1="356" y1="76.0"' in figure

    caption = " ".join(document.split())
    assert (
        "T-060, by Queuingtheorydotcom after Levy et al. 2026, closes the remaining gap"
        in caption
    )
    assert "the exact algebraic side $T$" in caption
    assert "a truncated decimal display of $T$" in caption
    assert "leaves a gap of $0.0000000" not in caption


def test_equal_display_digits_cannot_admit_solved_figure_without_t060(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    verified = render_n11_lower_bounds_explainer.verified_lower_bound(11)
    with pytest.raises(SystemExit, match="matching exact T-060"):
        render_n11_lower_bounds_explainer.n11_solved(replace(verified, confirmed_by=()))
    changed = render_n11_lower_bounds_explainer.FRONTIER_N11.read_text(
        encoding="utf-8"
    ).replace(
        "root(P_trump11, 3.87708359002281417730789706010096)",
        "root(P_other, 3.87708359002281417730789706010096)",
        1,
    )
    case = tmp_path / "n-011.md"
    case.write_text(changed, encoding="utf-8")
    monkeypatch.setattr(render_n11_lower_bounds_explainer, "FRONTIER_N11", case)
    with pytest.raises(SystemExit, match="matching exact T-060"):
        render_n11_lower_bounds_explainer.n11_solved(verified)


def test_omitting_the_solved_tick_does_not_split_the_svg_html_block(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An empty replacement turns the following indented SVG into Markdown code."""
    original = render_n11_lower_bounds_explainer.shared_substitutions

    def blank_tick(
        facts: list[render_n11_lower_bounds_explainer.Facts],
        headline: render_n11_lower_bounds_explainer.Facts,
        default: render_n11_lower_bounds_explainer.Facts,
    ) -> dict[str, str]:
        values = original(facts, headline, default)
        values["VERIFIED_MARK"] = ""
        return values

    monkeypatch.setattr(render_n11_lower_bounds_explainer, "shared_substitutions", blank_tick)
    broken = render(WALKTHROUGH).page
    figure = broken.split('<div class="line-fig kpress-diagram">', 1)[1].split("</div>", 1)[0]
    assert "<pre" in figure
    assert "<code" in figure


def test_historical_open_bracket_keeps_its_separate_tick_and_gap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    old = render_n11_lower_bounds_explainer.VerifiedLowerBound(
        value=Fraction(31, 8),
        display="3.875",
        credit="Kleddamag after Levy et al. 2026",
        confirmed_by=("T-037",),
    )
    monkeypatch.setattr(
        render_n11_lower_bounds_explainer, "verified_lower_bound", lambda _n: old
    )
    monkeypatch.setattr(render_n11_lower_bounds_explainer, "n11_solved", lambda _bound: False)
    historical = render(WALKTHROUGH)
    x = round(render_n11_lower_bounds_explainer.line_x(float(old.value)))
    assert f'<line x1="{x}" y1="56" x2="{x}" y2="76"' in historical.page
    assert "September 22, 2026" in historical.markdown
    assert "leaves a gap of $0.0020835\\ldots$" in historical.markdown
    assert "T-060 closes the remaining gap" not in historical.markdown


def test_the_published_document_sets_mathematics_without_typesetting_kerns(
    document: str,
) -> None:
    """`\\mkern1mu` is how KaTeX is told not to set `s` against `(`, and nothing more.

    It is a fact about typesetting, not about the mathematics, and a reader or a model
    taking this file should see `s(11)`.
    """
    assert "mkern" not in document
    assert "$s(11)$" in document or "s(11)" in document


def test_the_link_preview_is_the_sites_and_its_urls_are_absolute(page: str) -> None:
    """A shared link previews as every page of the site does, or it previews with nothing.

    The page shipped with four `<meta>` tags, a title and a description and no card at
    all, so every unfurl of it -- X, Slack, Discord, Facebook, iMessage -- was a line of
    text on a blank rectangle. What makes a card is the set together rather than any one
    tag: a consumer that finds `og:image` and no `twitter:card` falls back to a
    thumbnail, and one that finds a relative `og:image` drops the image outright,
    because a crawler resolves it on its own machine and has no base to resolve
    against. The set was this page's own until 2026-10-01 and is now the site's, written
    by `render_overview.head_tags` from this page's record, so it is held here to the
    same check the deployed site gets: one of each tag, each address in full, and the
    canonical link and `og:url` both the page's own address.
    """
    assert check_published_site.head_problems(page, PAGE_URL, allow_inline_favicon=True) == []
    head = check_published_site.read_head(page)
    assert head.link("canonical") == head.meta("og:url") == [PAGE_URL]
    assert render_overview.canonical_url(PAGE_URL.removeprefix(SITE_URL)) == PAGE_URL
    assert head.meta("og:type") == ["article"]


def test_the_card_image_is_the_sites_one_card_at_the_size_it_is_drawn(page: str) -> None:
    """The card names the image every page names, at the size it is drawn at.

    Two ways a card breaks without the page changing at all. The image URL can name
    something the deploy does not serve, which is a 404 a consumer answers by showing no
    image; and the declared width and height can drift from the file, which reflows the
    preview or loses it. The image is the site's one card, drawn when the site is built
    (`devtools.social_card`) and not beside this page, so what is held here is that the
    head names it by the renderer's constants; `tests/test_site_head.py` holds the
    drawing to those constants, and the deployed bytes are read by
    `check_published_site`.
    """
    head = check_published_site.read_head(page)
    card = SITE_URL + render_overview.SOCIAL_CARD
    assert head.meta("og:image") == head.meta("twitter:image") == [card]
    assert head.meta("og:image:width") == [str(render_overview.SOCIAL_CARD_WIDTH)]
    assert head.meta("og:image:height") == [str(render_overview.SOCIAL_CARD_HEIGHT)]
    assert head.meta("og:image:alt") == head.meta("twitter:image:alt")
    assert head.meta("og:image:alt") == [render_overview.social_card_alt()]


def test_the_composite_card_is_the_landscape_crop_and_not_the_portrait_canvas() -> None:
    """The composite's card, which the overview's atlas card shows and which was this
    page's link preview until the site took one card for every page, stays a card.

    A portrait card is cropped by the platform, and it crops away the title.

    X and Facebook show a landscape card and take a band from the middle of whatever
    they are handed, so the full 150:181 canvas arrives as four rows out of the middle
    of the grid with the title, the date and the repository line gone. The atlas builder
    writes the top of the same drawing at 1.91:1 instead, which is the ratio those
    platforms want, so they crop nothing.

    What is pinned is the property rather than the number: landscape, and within a
    pixel of the ratio the croppers use. A future canvas can change the crop height as
    long as the card stays a card.
    """
    width, height = png_size(COMPOSITE_CARD)
    assert width > height, "a card cropped by the platform is a card without its title"
    assert abs(width / height - 1.91) < 0.01, (width, height, width / height)
    # The crop is of the composite, not a second drawing: same width, less height.
    full_width, full_height = png_size(COMPOSITE_PNG)
    assert width == full_width
    assert height < full_height


def test_the_card_and_the_page_say_the_same_thing(page: str) -> None:
    """A preview that disagrees with the page it opens is worse than no preview.

    The title and the sentence are in the page's record once (`page_meta`) and written
    from it into `<title>`, `<meta name="description">` and both card vocabularies, so
    there is one string and not four. This is what would catch a later edit that retyped
    one of them in the template instead.
    """
    head = check_published_site.read_head(page)
    current = current_bound_facts()
    (title,) = head.titles
    # The preview's title is the page's own, bound-free: T-060 has settled the case, and
    # one bound after a title about several would read as its current one. The tab's
    # title names the project after it, as every page's does.
    assert (
        head.meta("og:title")
        == head.meta("twitter:title")
        == [render_n11_lower_bounds_explainer.TITLE]
    )
    assert (
        render_n11_lower_bounds_explainer.TITLE
        == "New Lower Bounds for Square Packing for n = 11"
    )
    assert title == render_n11_lower_bounds_explainer.TITLE
    (description,) = head.meta("description")
    assert head.meta("og:description") == head.meta("twitter:description") == [description]
    assert current.bounded_side_decimal in description
    assert len(description) <= render_overview.DESCRIPTION_LIMIT
    # The two dates the hero prints, as a crawler reads a date.
    assert head.meta("article:published_time") == [
        render_n11_lower_bounds_explainer.iso_date(EXPLAINER_FIRST_PUBLISHED)
    ]
    assert head.meta("article:modified_time") == [
        render_n11_lower_bounds_explainer.iso_date(EXPLAINER_REVISED)
    ]
    assert render_n11_lower_bounds_explainer.iso_date("September 5, 2026") == "2026-09-05"
    assert "s(11)" not in title
    assert "s(11)" in description
    assert "T-026's historical bound" in description


def test_the_forwarder_at_the_old_address_previews_the_page_as_the_page_does(
    page: str,
) -> None:
    """A link to `explainer.html`, where the page was served until 2026-10-01, is still
    shared, and the forwarder there previews the page (`render_overview.forwarder_pages`):
    by the page's own title, kind, sentence and dates, read here from the rendered page,
    and at its address. The card's sentence-case title and `website`, which it carried
    first, previewed the paper as something else; `check_published_site` holds the
    deployed forwarder to the deployed page the same way."""
    forwarder = next(
        moved.html
        for moved in render_overview.forwarder_pages()
        if moved.name == "explainer.html"
    )
    assert dict(render_overview.MOVED_PAGES)["explainer.html"] == SITE_PATH
    assert (
        check_published_site.forwarder_problems(
            forwarder,
            PAGE_URL,
            page,
            allow_inline_favicon=True,
            page_url=SITE_URL + "explainer.html",
        )
        == []
    )
    head = check_published_site.read_head(forwarder)
    own = check_published_site.read_head(page)
    assert head.titles == own.titles
    assert head.link("canonical") == own.link("canonical") == [PAGE_URL]
    for key in (
        *check_published_site.PREVIEWED,
        "description",
        "twitter:title",
        "article:published_time",
        "article:modified_time",
    ):
        assert head.meta(key) == own.meta(key), key
    assert head.meta("og:type") == ["article"]


def test_advanced_section_derives_the_current_lower_bound(document: str) -> None:
    current = current_bound_facts()
    prose = " ".join(document.split())
    assert "## Proof of the New Lower Bound" in document
    assert "The numerical $3.81$ result is not a premise of T-026" in prose
    assert "Keeping T-018 in full also serves as an assurance bridge" in prose
    assert "does not verify the threshold certificates" in prose
    assert "t-025-verifiable-claim-191-50.md" in prose
    assert "t-026-verifiable-claim-dilation-limit.md" in prose
    assert "call this selected square a **core**" in prose
    assert "Its **trace** on a core $P$ is the subset $P\\cap S$" in prose
    assert "T-025 proves $s(11)\\ge 191/50=3.82$ directly" in prose
    assert (
        f"$D={render_n11_lower_bounds_explainer.frac_inline_tex(current.fine_half_gap)}$"
        in prose
    )
    assert "\\frac{qB(1+D)}{\\sqrt{1+D^2}}" in document
    assert "both atom families closed under the eight symmetries of the container" in prose
    assert current.bounded_side_decimal in prose
    assert "exact exclusions include rational sides above $3.82$" in prose
    assert "the exact lower bound $s(11)\\ge L$" in prose
    assert "choose a rational $q<c$" in prose
    assert "fit unchanged in that larger container" in prose
    assert "Each point-certificate bound shown in the interactive figures" in prose
    assert "T-025 claim document" in prose
    assert "standard-library exact verifier" in prose
    assert "the same verifier, and the exact dilation record" in prose
    assert "weak limit" not in prose.lower()


def test_the_published_document_is_named_by_the_papers_slug(document: str) -> None:
    """A paper's Markdown is served beside its page under the same slug.

    It was `explainer.md`, then `t-018-explainer.md`, named for the result the way a
    case-local document is. A paper is named by its slug, which says the case, the
    subject and the kind of paper, and its page, Markdown and PDF share it
    (`conventions.md`); the case-local documents keep the result's id, which is written
    once in the renderer and every such name is derived from it.
    """
    assert OUTPUT.with_suffix(".md") == MARKDOWN_OUTPUT
    assert MARKDOWN_OUTPUT.name == "n11-lower-bounds-explainer.md"
    claims = sorted(CASE.glob("*-verifiable-claim-*.md"))
    assert claims, "the case carries no claim document to share an id with"
    for claim in claims:
        assert claim.name.startswith(f"{RESULT_ID}-"), claim.name
    # The document is what it is named after: the article, not the template.
    assert document.startswith("# New Lower Bounds for Square Packing for $n = 11$\n")


def test_the_md_chip_offers_the_document_by_its_published_name(page: str) -> None:
    """The chip is a relative link, so it resolves to a file that has to be beside it.

    `SOURCE_URL` is the published document's own filename, so a rename moves both ends
    at once. A chip left pointing at the old name is a 404 on the deployed site and
    nothing in the render notices, which is why it is checked against the constant the
    writer uses rather than against a name spelled out here.
    """
    assert f'href="{MARKDOWN_OUTPUT.name}"' in page


def pages_filters() -> dict[str, list[str]]:
    """The `paths:` filter of each event the Pages workflow triggers on."""
    workflow = safe_load((REPO / ".github" / "workflows" / "pages.yml").read_text("utf-8"))
    triggers = workflow["on" if "on" in workflow else True]
    return {
        event: settings["paths"]
        for event, settings in triggers.items()
        if isinstance(settings, dict) and "paths" in settings
    }


def test_pages_selects_the_validation_node_runtime_before_rendering() -> None:
    workflow = safe_load((REPO / ".github" / "workflows" / "pages.yml").read_text("utf-8"))
    setup_node = "actions/setup-node@48b55a011bda9f5d6aeb4c2d9c7362e8dae4041e"
    for job_name in ("prepare", "workbench"):
        steps = workflow["jobs"][job_name]["steps"]
        selected = [step for step in steps if step.get("uses") == setup_node]
        assert len(selected) == 1, f"{job_name} must select one pinned Node runtime"
        assert selected[0]["with"]["node-version"] == "24.18.0"


def test_pages_installs_the_locked_package_before_building_the_workbench() -> None:
    workflow = safe_load((REPO / ".github" / "workflows" / "pages.yml").read_text("utf-8"))
    steps = workflow["jobs"]["workbench"]["steps"]
    node = next(
        i
        for i, step in enumerate(steps)
        if step.get("uses", "").startswith("actions/setup-node@")
    )
    install = next(
        i for i, step in enumerate(steps) if step.get("run") == "npm ci --ignore-scripts"
    )
    build = next(
        i
        for i, step in enumerate(steps)
        if "python -m workbench_tools.build_site" in step.get("run", "")
    )
    assert node < install < build
    assert steps[install]["working-directory"] == "."


def test_workbench_navigation_resolves_to_the_pages_project_root() -> None:
    href = re.search(r'<a href="([^"]+)">the overview</a>', WORKBENCH_NOTE)
    assert href is not None
    workbench = "https://jlevy.github.io/squares/workbench/"
    assert urljoin(workbench, href.group(1)) == "https://jlevy.github.io/squares/"
    assert href.group(1) == "../"


def test_workbench_build_identity_requires_an_exact_commit() -> None:
    revision = "0123456789abcdef0123456789abcdef01234567"
    assert workbench_build_metadata(revision) == (
        f'<meta name="squares-workbench-revision" content="{revision}">'
    )
    for invalid in ("main", revision[:8], f"{revision}0", "g" * 40):
        with pytest.raises(ValueError, match="invalid workbench source revision"):
            workbench_build_metadata(invalid)


def covered(path: Path, patterns: list[str]) -> bool:
    """Whether a GitHub `paths:` filter republishes on a change under `path`.

    A filter entry is matched against files, not directories, so a declared input that
    is a directory is covered by a pattern that would match a file inside it. `**` and a
    bare directory name both do that; the comparison below is deliberately the strict
    one, so an entry that covers the directory only by accident does not pass.
    """
    relative = path.relative_to(REPO).as_posix()
    return any(
        pattern == relative
        or fnmatchcase(relative, pattern)
        or (path.is_dir() and fnmatchcase(f"{relative}/__render_input__", pattern))
        or pattern.rstrip("/*") == relative.rstrip("/")
        for pattern in patterns
    )


def test_the_pages_filter_covers_every_render_input() -> None:
    """A render input outside the filter is a page that goes stale with the gate green.

    The workflow's `paths:` list and the renderer's imports are written in two languages
    and maintained by hand, so nothing but this comparison stops them drifting. They had
    drifted: the filter named the composite PNG and PDF but not the SVG the figure
    actually shows, and named neither the frontier register the opening counts nor the
    figure record the drawing is built from (think-bl0n). Any of those four could have
    changed on main and left the deployed page showing the previous render, with every
    check passing, which is the shape of D-455 rather than a new one.

    Only the deploy's filter is a list. A pull request that builds the page is the only
    review a render change gets, and it has no filter since 2026-09-15: the scope job
    reads `RENDER_INPUTS` itself, and `test_pages_scope` holds it to this declaration --
    so the gap seen from the pull request's side is closed by construction rather than by
    a second comparison here.
    """
    filters = pages_filters()
    assert set(filters) == {"push"}, sorted(filters)
    for event, patterns in filters.items():
        missing = [
            declared.relative_to(REPO).as_posix()
            for declared in RENDER_INPUTS
            if not covered(declared, patterns)
        ]
        assert not missing, f"{event}: RENDER_INPUTS not covered by paths: {missing}"


def test_the_pages_filter_covers_every_workbench_input() -> None:
    """The workbench is published by the same workflow, so it needs the same guard.

    `packing/site` is uploaded whole and the workbench is a subdirectory of it, which is
    what gives it its own URL -- and also what makes a stale workbench invisible: the
    explainer would rebuild, the artifact would upload, and `/workbench/` would keep
    serving the previous build with every check green. The comparison is the explainer's,
    asked of the other page's declared inputs.
    """
    filters = pages_filters()
    for event, patterns in filters.items():
        missing = [
            declared.relative_to(REPO).as_posix()
            for declared in WORKBENCH_INPUTS
            if not covered(declared, patterns)
        ]
        assert not missing, f"{event}: workbench inputs not covered by paths: {missing}"


def test_the_workbench_input_guard_detects_an_omitted_input_class() -> None:
    """The filter comparison must fail when one whole source class is absent.

    The old declaration omitted every witness while its builder read all 324. Removing the
    witness pattern from the real filter recreates that failure and proves the comparison sees
    the directory as an input, rather than only comparing two mutually incomplete file lists.
    """
    witnesses = REPO / "packing/witnesses/known-best"
    for event, patterns in pages_filters().items():
        without_witnesses = [
            pattern for pattern in patterns if "witnesses/known-best" not in pattern
        ]
        missing = [
            declared
            for declared in WORKBENCH_INPUTS
            if not covered(declared, without_witnesses)
        ]
        assert witnesses in missing, f"{event}: omitted witnesses were not detected"


def test_every_declared_workbench_input_exists() -> None:
    """The other half, for the workbench: a filter entry naming a file that is gone."""
    for declared in WORKBENCH_INPUTS:
        assert declared.exists(), declared.relative_to(REPO).as_posix()


def test_the_pages_filter_covers_every_overview_input() -> None:
    """The site's own pages are the third build the workflow publishes; the same guard.

    `render_overview.inputs()` is its declaration: the renderer's own `RENDER_INPUTS` and
    the record `overview_data.INPUTS` reads. A register entry, a case record, the
    bibliography or `TUTORIAL.md` changed on `main` outside this filter would leave `/`
    and the pages beside it showing the previous render with every check green.
    """
    declared = render_overview.inputs()
    assert REPO / "TUTORIAL.md" in declared
    assert REPO / "packing/frontier/evidence.yaml" in declared
    for event, patterns in pages_filters().items():
        missing = [
            path.relative_to(REPO).as_posix()
            for path in declared
            if not covered(path, patterns)
        ]
        assert not missing, f"{event}: overview inputs not covered by paths: {missing}"
        without_documents = [p for p in patterns if p != "TUTORIAL.md"]
        exposed = [path for path in declared if not covered(path, without_documents)]
        assert exposed == [REPO / "TUTORIAL.md"], event


def test_every_declared_overview_input_exists() -> None:
    for declared in render_overview.inputs():
        assert declared.exists(), declared.relative_to(REPO).as_posix()


def test_generated_workbench_palette_declares_its_renderer_source() -> None:
    assert REPO / "packing/src/sqpack/render" in WORKBENCH_INPUTS


def test_every_declared_render_input_exists() -> None:
    """A path filter naming a file that is gone republishes on nothing, silently.

    The check above compares two lists to each other, which both of them can satisfy
    while naming a file the repository no longer has. This is the other half: every
    declared input resolves, so a rename cannot leave a matched pair of dead entries.
    """
    for declared in RENDER_INPUTS:
        assert declared.exists(), declared.relative_to(REPO).as_posix()


def test_no_screen_only_prose_survives_into_the_published_document(document: str) -> None:
    """A multi-line `screen-only` span used to leak, and reads as ordinary prose when it does.

    `_SCREEN_ONLY` is compiled `re.DOTALL` so it can span lines, but it was applied one
    line at a time, so a span opening on one line and closing on the next matched
    nothing; `_SIMPLE_TAG` then stripped the bare tags and the sentence shipped. "The
    chooser under each figure switches every figure between the two at once" reached a
    published edition that has no chooser in it, and nothing objected, because the leak
    is well-formed Markdown in a well-formed document.

    Checked on the words rather than on the markup, for the same reason the publisher's
    own guard is: an edition that tells its reader to hover or tap is wrong however it
    got that way, and the markup is exactly what is missing by the time it is wrong.
    """
    for word in ("chooser", "hover", "tap", "drag", "click", "slider"):
        assert word not in document.lower(), f"{word!r} addresses a reader who has the page"


def test_the_published_document_says_what_it_is_and_where_the_figures_are(
    document: str,
) -> None:
    """Six of the seven figures are captions here, and a reader cannot tell that alone.

    Figure 2 carries its image; the rest are drawn by the page, so they arrive as
    captions with nothing above them -- readable, and describing something the reader
    cannot see. Without a word of explanation that reads as images that failed to load,
    and the chip row that would have pointed at the real page is one of the things this
    edition drops.
    """
    assert "Markdown edition" in document
    assert SITE_URL in document


def test_the_published_document_names_the_sites_files_where_the_site_serves_them(
    document: str,
) -> None:
    """The page reaches the atlas's files a level up, which resolves only from where the
    page is served. The document is read wherever it is taken, and is also served at the
    address it had before the papers moved (`render_overview.MOVED_FILES`), so it names
    each of those files by its address on the site, and links nothing relatively."""
    assert f"]({SITE_ROOT}" not in document
    assert f"]({SITE_URL}known-best-1-100.svg)" in document
    assert f"]({SITE_URL}known-best-1-100.pdf)" in document
    assert f"]({SITE_URL}known-best-1-324.pdf)" in document
    relative = re.findall(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)", document)
    assert relative == []


def _style_blocks(page: str) -> list[str]:
    return re.findall(r"<style>(.*?)</style>", page, re.DOTALL)


def _figure_blocks(page: str) -> dict[int, tuple[str, str]]:
    figures: dict[int, tuple[str, str]] = {}
    for attributes, body in re.findall(r"<figure\b([^>]*)>(.*?)</figure>", page, re.DOTALL):
        number = re.search(r"<strong>Figure (\d+)\.</strong>", body)
        if number:
            figures[int(number.group(1))] = (attributes, body)
    return figures


def test_only_composite_apparatus_has_the_panel_hairline(page: str) -> None:
    """The three panelled figures are framed; packing drawings and charts stay open."""
    figures = _figure_blocks(page)
    assert figures.keys() == set(range(1, 8))
    for number, (attributes, body) in figures.items():
        framed = bool(re.search(r'\bclass="[^"]*\bapparatus\b', attributes))
        assert framed is (number in {4, 5, 6}), number
        assert ('class="panel"' in body) is framed, number

    css = "\n".join(_style_blocks(page))
    assert re.search(r"\.cert-page \.kpress-figure\s*\{\s*border:\s*0;\s*}", css)
    assert re.search(
        r"\.cert-page \.kpress-figure\.apparatus\s*\{\s*"
        r"border:\s*1px solid var\(--kpress-doc-border\);\s*}",
        css,
    )


def test_only_the_figure_number_prefix_is_bold_in_every_caption(page: str) -> None:
    figures = _figure_blocks(page)
    for number, (_attributes, body) in figures.items():
        caption = re.search(r"<figcaption\b[^>]*>(.*?)</figcaption>", body, re.DOTALL)
        assert caption, number
        strong = re.findall(r"<strong>(.*?)</strong>", caption.group(1), re.DOTALL)
        assert strong == [f"Figure {number}."], number


def test_print_removes_only_inline_code_chip_decoration(page: str) -> None:
    css = "\n".join(_style_blocks(page))
    assert re.search(
        r"@media print\s*\{.*?\.cert-page code:not\(pre code\)\s*\{\s*"
        r"background:\s*transparent;\s*border:\s*0;\s*}",
        css,
        re.DOTALL,
    )


def test_the_page_stylesheet_has_no_orphaned_comment_delimiter(page: str) -> None:
    """A comment that ends early turns the prose after it into CSS, silently.

    This shipped. A block comment was extended with a second paragraph, but the original
    `*/` was left in place above it, so eleven lines of English became two invalid
    qualified rules -- and the second one's prelude ran on until it swallowed the `{
    text-align: left !important; }` underneath, which is a real rule the printed document
    depends on. CSS error recovery is silent by specification: the browser dropped both,
    printed prose reverted to the vendor's justification, and every render, every
    reproducibility check and every screenshot still passed.

    Checked on the delimiters rather than by parsing, so it needs no CSS parser: strip
    the balanced comments and nothing that opens or closes one may remain.
    """
    for index, css in enumerate(_style_blocks(page)):
        stripped = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
        for orphan in ("*/", "/*"):
            assert orphan not in stripped, (
                f"style block {index}: an unbalanced {orphan} leaves prose outside a comment"
            )


def _selector_list(prelude: str) -> list[str]:
    """Split only top-level commas; functions, strings and escapes stay in one selector."""
    selectors = [""]
    for token in tinycss2.parse_component_value_list(prelude):
        if token == ",":
            selectors.append("")
        else:
            selectors[-1] += token.serialize()
    return [selector.strip() for selector in selectors]


def _assert_no_prose_selectors(page: str) -> None:
    for index, css in enumerate(_style_blocks(page)):
        stripped = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
        # Preludes only: what stands between the end of one rule and the `{` of the next.
        for prelude in re.findall(r"(?:^|[}])([^{}]*)\{", stripped):
            text = prelude.strip()
            assert ";" not in text, f"style block {index}: selector holds a `;`: {text[:80]!r}"
            assert "important" not in text, (
                f"style block {index}: selector holds `important`: {text[:80]!r}"
            )
            for selector in _selector_list(text):
                assert len(selector) < 400, (
                    f"style block {index}: selector is prose: {selector[:80]!r}"
                )


def test_no_rule_in_the_page_stylesheet_has_prose_for_a_selector(page: str) -> None:
    """Catch prose that silent CSS error recovery would discard along with the next rule.

    An unbalanced comment is one way to get there and a stray `}` is another. Our
    selectors contain neither a semicolon nor `important`, and each is under 400
    characters. A valid selector list can exceed that bound, as the four saved-font
    contexts do, so apply it to each top-level entry rather than the entire prelude.
    """
    _assert_no_prose_selectors(page)


def test_selector_list_keeps_nested_quoted_and_escaped_commas() -> None:
    selectors = [":is(.a, :not(.b, .c))", '[data-label="a,b"]', r".a\,b"]
    assert _selector_list(", ".join(selectors)) == selectors


@pytest.mark.parametrize(
    "prelude",
    [
        "text-align: left; .prose",
        "text-align: left !important .prose",
        "A sentence outside its comment " * 20,
        ":is(" + ", ".join("a" * 100 for _ in range(5)) + ")",
    ],
)
def test_prose_selector_guard_rejects_bad_preludes(prelude: str) -> None:
    with pytest.raises(AssertionError, match=r"selector (holds|is prose)"):
        _assert_no_prose_selectors(f"<style>{prelude} {{ color: red; }}</style>")


def test_every_relative_link_in_the_page_names_a_file_the_deploy_serves(page: str) -> None:
    """A chip that 404s on the deployed site is invisible to every other check here.

    The page is served from a directory, so each relative `href` and `src` resolves
    against whatever the Pages artifact happens to contain. The MD chip is checked above
    against the constant the writer uses; this asks the same question of all of them at
    once, which is what the PDF chip needed -- its file is written by a different module
    from the one that writes the page, so nothing else relates the two.

    Two links already shipped as `file:///home/.../known-best-1-100.pdf`, absolute paths
    to the machine that built them, and the atlas figure was one of them.
    """
    # By path under the site's root: the paper's own files under `papers/`, and at the
    # root the atlas's files and the site's other pages, which the navigation bar links
    # to. A directory index is linked as its directory.
    served = {
        SITE_PATH,
        f"{PAPERS_DIR}/{MARKDOWN_OUTPUT.name}",
        f"{PAPERS_DIR}/{PDF_OUTPUT.name}",
        *(asset.name for asset in COMPOSITE_ASSETS),
        *SITE_PAGES,
        *(page.removesuffix("index.html") or "./" for page in SITE_PAGES),
        # The series' other papers, which the page links (`devtools.paper_links`).
        *(render_overview.paper_path(slug) for slug in paper_links.PAPER_SLUGS),
    }
    # Markup only. The page inlines KaTeX and kpress's client, and a minified
    # `'+a(this.src)+'` in one of them reads as an attribute to a regex that does not
    # know where the script ends.
    markup = re.sub(r"<(script|style)\b.*?</\1>", "", page, flags=re.DOTALL | re.IGNORECASE)
    links = {
        match.group(2)
        for match in re.finditer(r'\b(href|src)="([^"]+)"', markup)
        if not re.match(r"[a-z][a-z0-9+.-]*:|#|//", match.group(2), re.IGNORECASE)
    }
    # Each link is resolved from where the page is served, a level below the root.
    resolved = {
        link: posixpath.normpath(posixpath.join(PAPERS_DIR, link.split("#")[0].split("?")[0]))
        for link in links
    }
    assert all(not path.startswith("..") for path in resolved.values()), resolved
    missing = sorted(
        link for link, path in resolved.items() if (path if path != "." else "./") not in served
    )
    assert not missing, f"relative links to files the deploy does not serve: {missing}"
    # The atlas's files are at the root, where the overview links them and a link
    # preview names the card: the page reaches each a level up.
    assert f'src="{SITE_ROOT}known-best-1-100.svg"' in page
    assert f'poster="{SITE_ROOT}ascent-n1-100-poster.png"' in page
    assert SITE_ROOT == "../"


def test_the_pdf_chip_offers_the_pdf_the_exporter_writes(page: str) -> None:
    """Named against the exporter's own constant, so a rename moves both ends at once."""
    assert f'href="{PDF_OUTPUT.name}"' in page
    assert PDF_OUTPUT.parent == OUTPUT.parent, "the PDF must land beside the page it links from"


#: A link into this repository as GitHub spells one: the ref, then the path, under
#: `blob/` for a file and `tree/` for a directory.
REPOSITORY_LINK = re.compile(
    re.escape(REPO_URL) + r"/(?:blob|tree)/([^/\s\"<>)]+)/([^\s\"<>?#)]*)"
)


def repository_links(text: str) -> set[tuple[str, str]]:
    """Repository (ref, path) pairs, excluding fragments, queries, scripts and styles."""
    markup = re.sub(r"<(script|style)\b.*?</\1>", "", text, flags=re.DOTALL | re.IGNORECASE)
    return {(ref, path.rstrip("/")) for ref, path in REPOSITORY_LINK.findall(markup)}


def test_every_repository_link_names_main_and_exists_there(page: str, document: str) -> None:
    """Each link into the repository names `main`, and each linked path is in `HEAD`.

    The page used to link the commit it was built from, so that a link identified the
    verifier, the generator and the exposition a reported run used (review of
    2026-09-05, Finding 8). Those permalinks 404ed once a squash merge left the build
    commit on no branch, so the page now links `main`, where it deploys from, and the
    committed claim documents are what pin a run's verifier at the edition's revision.
    Every piece of evidence the page walks through is still linked, and every linked
    path is asked of git at `HEAD`, the tree `main` holds when the page deploys.
    """
    from devtools.repo_links import (  # noqa: PLC0415
        DEFAULT_BRANCH,
        hash_pinned_links,
        repository_tree,
    )

    assert not hash_pinned_links(page)
    assert not hash_pinned_links(document)
    links = repository_links(page) | repository_links(document)
    assert links, "the page links nothing in the repository"
    elsewhere = sorted(f"{ref}/{path}" for ref, path in links if ref != DEFAULT_BRANCH)
    assert not elsewhere, f"repository links not on {DEFAULT_BRANCH}: {elsewhere}"
    linked = {path for _, path in links}
    evidence = (
        VERIFIER,
        GENERATOR,
        THIRDPARTY,
        BEST_RENDERING,
        ATLAS,
        Path(render_n11_lower_bounds_explainer.__file__),
        *WALKTHROUGH,
        render_n11_lower_bounds_explainer.THRESHOLD_CERTIFICATE,
        render_n11_lower_bounds_explainer.THRESHOLD_FINE_CERTIFICATE,
        render_n11_lower_bounds_explainer.CURRENT_BOUND_RECORD,
        *sorted(CASE.glob("*-verifiable-claim-*.md")),
    )
    for path in evidence:
        assert path.resolve().relative_to(REPO).as_posix() in linked, path.name
    tree = repository_tree()
    missing = sorted(path for path in linked if path not in tree.files | tree.directories)
    assert not missing, f"linked on {DEFAULT_BRANCH} but not in HEAD: {missing}"


def test_the_atlas_figure_carries_the_shared_version_at_its_own_data_commit() -> None:
    """A poster names the data it was drawn from, in the site's one spelling at its own
    data commit, and is not re-stamped when the pin moves (`sqpack.release`, rule 4):
    the posters agree with the site's edition in the version and may differ in the six
    characters after it. The posters are the site's assets, so they keep the site's
    version; the paper that shows them does not."""
    for composite in (path for path in COMPOSITE_ASSETS if path.suffix == ".svg"):
        text = composite.read_text()
        footer = re.search(r'<text data-feature="release-stamp"[^>]*>([^<]*)</text>', text)
        assert footer is not None, composite.name
        drawn_from = re.search(r'name="data-revision">([0-9a-f]{40})</sqpack:value>', text)
        assert drawn_from is not None, composite.name
        assert footer.group(1) == edition_at(drawn_from.group(1)), composite.name
        assert footer.group(1).rsplit("-", 1)[0] == PUBLICATION_EDITION.rsplit("-", 1)[0]


def test_the_credits_print_the_papers_own_version_and_not_the_sites(
    page: str, document: str
) -> None:
    """The top names which version of the paper is being read, the paper's own, linking
    the full list rather than repeating it (the owner, 2026-09-22), then when the paper
    was first published and when it was last revised, in the two papers' one credits
    form (the owner, 2026-10-01: the version line, plain, before the dates). The first
    date is the paper's oldest edition's; the second is the day the article last
    changed, which `test_artifact_dates` holds to git. The front is `paper_front`'s,
    from this paper's record, and the article carries one slot for it.
    """
    dates = f"First published {EXPLAINER_FIRST_PUBLISHED} · Last revised {EXPLAINER_REVISED}"
    edition = f'{EXPLAINER_VERSION} (<a href="#version-history">version history</a>)'
    assert f'<span class="edition">{edition}</span>' in page
    assert f'<span class="publication-date">{dates}</span>' in page
    assert page.index('class="edition"') < page.index('class="publication-date"')
    assert EXPLAINER_FIRST_PUBLISHED != EXPLAINER_REVISED
    compact = " ".join(document.split())
    assert dates in compact
    assert f"{EXPLAINER_VERSION} ([version history](#version-history))" in compact
    assert 'id="version-history"' in page
    article = render_n11_lower_bounds_explainer.MARKDOWN.read_text(encoding="utf-8")
    assert article.count("{{FRONT_MATTER}}") == 1
    assert '<div class="credits' not in article
    assert "doc-links" not in article
    # The explainer explains the project's own proofs, so it credits no source and its
    # credits begin at its own; the project's repository is the footer's and the GitHub
    # chip's, in the credits of neither paper (think-2cqu).
    assert render_n11_lower_bounds_explainer.FRONT.source is None
    block = page.split('<div class="credits centred">', 1)[1].split("</div>", 1)[0]
    # Four lines of credits, then the series strip (`paper_front.series`).
    assert block.count("<span") - block.count('<span class="series">') == 4
    assert block.count('<span class="series">') == 3
    assert "github.com/jlevy/squares" not in block
    assert block.lstrip().startswith('<span class="credits-own">Human oversight: ')
    # The version line is the paper's own, plain: no status, no data hash.
    assert re.fullmatch(r"v\d+\.\d+\.\d+", EXPLAINER_VERSION)
    assert render_n11_lower_bounds_explainer.FRONT.version == EXPLAINER_VERSION


def _visible_text(page: str) -> str:
    """The page's words: what a reader, or `pdftotext`, sees, with the inlined scripts,
    stylesheets and base64 faces out of the way. A six-character hash occurs by chance
    in a megabyte of base64, so the hash is held out of the words, not the bytes."""
    stripped = re.sub(r"<(script|style)\b.*?</\1>", " ", page, flags=re.DOTALL | re.IGNORECASE)
    stripped = re.sub(r"<[^>]+>", " ", stripped)
    return " ".join(stripped.split())


def test_no_site_version_or_data_hash_reaches_the_paper(page: str, document: str) -> None:
    """The site's edition and the data hash are on no paper page, in no Markdown edition
    and in no PDF (the owner, 2026-10-01: the repository's version does not go on the
    papers). The PDF is drawn from this page and its receipt holds it to these bytes
    (`render_n11_lower_bounds_explainer_pdf`), so what is not in the page's words is not
    in the PDF's. The hash is held out of the words rather than the bytes: the page
    inlines its faces as base64, where six hex characters occur by chance.
    """
    words = _visible_text(page)
    for forbidden in (PUBLICATION_EDITION, PUBLICATION_STAMP):
        assert forbidden not in page
        assert forbidden not in document
    assert DATA_REVISION[:DATA_REVISION_LENGTH] not in words
    assert DATA_REVISION[:DATA_REVISION_LENGTH] not in document
    assert DATA_REVISION not in page
    # Every version on the page is the paper's own or the release the films are on;
    # the site's edition is neither.
    allowed = {EXPLAINER_VERSION, render_overview.FILM_RELEASE} | {
        entry.version for entry in EXPLAINER_HISTORY
    }
    for found in set(re.findall(r"v\d+\.\d+\.\d+(?:-[0-9a-f]{6})?", words)):
        assert found in allowed, found
    for found in set(re.findall(r"v\d+\.\d+\.\d+(?:-[0-9a-f]{6})?", document)):
        assert found in allowed, found


def test_version_history_lists_the_papers_own_editions_and_no_others(
    page: str, document: str
) -> None:
    """The page's history is `release.EXPLAINER_HISTORY`, exactly: the editions in which
    the paper changed, each with the day it was first published, and none of the site's
    editions under which it did not (the owner, 2026-10-01: the version history on a
    paper reflects versions of the paper, not of the website)."""
    match = re.search(
        r"^## Version History\n\n(?P<history>.*?)(?=\n\[\^|\Z)",
        document,
        re.MULTILINE | re.DOTALL,
    )
    assert match is not None
    assert document.index("## Version History") > document.index("## Further Reading")
    history = match.group("history")
    listed = re.findall(r"^- \*\*(v\d+\.\d+\.\d+) — ", history, re.MULTILINE)
    assert listed == [entry.version for entry in EXPLAINER_HISTORY]
    compact_history = " ".join(history.split())
    for entry in EXPLAINER_HISTORY:
        expected = f"- **{entry.version} — {entry.first_published}.** {entry.result_scope}"
        assert " ".join(expected.split()) in compact_history
        assert entry.version in page
        assert entry.first_published in page
    site_only = {e.version for e in PUBLICATION_HISTORY} - set(listed)
    assert site_only, "the site has had editions in which the paper did not change"
    for version in site_only:
        assert f"**{version} — " not in history


def test_reader_facing_version_references_follow_release_metadata() -> None:
    """Nearby entry points name the right version: the README the site's edition, where
    it speaks of the site and the posters, and the tutorial the explainer's own, where it
    points at the paper; neither retains a previous number."""
    readme = (REPO / "README.md").read_text()
    assert PUBLICATION_VERSION in readme
    assert "its papers and the atlas posters are at edition" not in readme
    tutorial = (REPO / "TUTORIAL.md").read_text()
    assert f"the standalone {EXPLAINER_VERSION} explainer" in tutorial
    if PUBLICATION_VERSION != EXPLAINER_VERSION:
        assert PUBLICATION_VERSION not in tutorial
    development = (REPO / "development.md").read_text()
    assert "PUBLICATION_HISTORY" in development
    assert "EXPLAINER_HISTORY" in development
