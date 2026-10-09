"""The overview page: every register entry shown, every count read from the record."""

from __future__ import annotations

import dataclasses
import functools
import html
import html.parser
import re
import struct
import textwrap
from collections import Counter
from collections.abc import Callable
from datetime import date
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path
from typing import cast
from urllib.parse import urlsplit

import pytest

from devtools import (
    check_results,
    overview_data,
    overview_sections,
    render_case_pages,
    render_overview,
    render_recent_results,
    result_overview,
    result_status,
    site_assets,
    site_urls,
)
from devtools.check_results import scope_values
from devtools.render_n11_lower_bounds_explainer import COMPOSITE_ASSETS, OVERVIEW_FILM_POSTER
from devtools.render_n11_lower_bounds_explainer import MARKDOWN as EXPLAINER_ARTICLE
from devtools.render_n11_lower_bounds_explainer import PUBLICATION_STYLE as EXPLAINER_STYLE
from devtools.render_n11_lower_bounds_explainer import TEMPLATE as EXPLAINER_SHELL
from devtools.repo_links import (
    DEFAULT_BRANCH,
    REPO_URL,
    branch_file,
    hash_pinned_links,
    repo_url,
)
from devtools.result_credit import OTHERS, source_lineage
from sqpack.yamlio import safe_load
from tests import site_renders

ID = re.compile(r'\sid="([^"]+)"')
#: A results-table row: its id, whose result it is, and its confirmation rung's level.
ROW = re.compile(
    r'<tr id="(t-\d{3})" data-source="(ours|others)" data-v="\d" data-c="(\d)"[^>]*>'
)


@pytest.fixture(scope="module")
def page() -> str:
    return site_renders.html("index.html")


@pytest.fixture(scope="module")
def results() -> str:
    return site_renders.html(render_overview.RESULTS_PAGE)


@pytest.fixture(scope="module")
def result_bodies() -> dict[str, str]:
    """Render complete result bodies during setup, before per-test monkeypatches.

    Each preview still renders afresh; its complete context comes from the same
    shared overview. Rendering all bodies in call time took 12.92 s on run 37785086481.
    """
    return site_renders.result_bodies()


@pytest.fixture(scope="module")
def register() -> list[dict]:
    return safe_load(overview_data.RESULTS.read_text(encoding="utf-8"))["results"]


@pytest.fixture(scope="module")
def case_pages() -> dict[str, str]:
    """Every case record by served name, from the one render the test process shares
    (`tests.site_renders.case_records`). The 324 records take about fifteen seconds to
    render, so they are rendered here, during setup, as the pages are: a check that reads
    them carries no render in its own call time, which the pull-request surface caps."""
    return site_renders.case_records()


@pytest.fixture(scope="module")
def rendered() -> Callable[[str], str]:
    """Any site page by name, from the one render of each the test process shares
    (`tests.site_renders`). Every page is rendered here, during setup, the case record
    page among them, so no check carries a render in its own call time."""
    site_renders.pages()
    return site_renders.html


@pytest.fixture(scope="module")
def served() -> Callable[[str], str]:
    """Any site page by name as a reader's browser assembles it, with every shared asset
    it links put back in it (`tests.site_renders.served`): for a check of what a page
    carries, its programs' and stylesheets' text among it, rather than of how it names
    them. Every page is assembled here, during setup, as `rendered` renders them."""
    assembled = {name: site_renders.served(name) for name in render_overview.PAGES}
    return assembled.__getitem__


def _asset_tag(path: Path, name: str = "index.html") -> str:
    """The element by which the page `name` loads `path`, a stylesheet or a page program
    of the repository's: a file of the site's shared assets named by its content
    (`site_assets`), so a page holding the element loads this text and no other."""
    assets = site_assets.shared().assets
    if path.suffix == ".css":
        return site_assets.stylesheet_tag(assets.stylesheet_file(path), name)
    return site_assets.script_tag(assets.script_file(path), name)


def test_every_register_entry_is_one_row(results: str, register: list[dict]) -> None:
    rows = ROW.findall(results)
    assert sorted(row_id for row_id, _, _ in rows) == sorted(r["id"].lower() for r in register)
    declared = {r["id"].lower(): r for r in register}
    for row_id, source, confirmation in rows:
        record = declared[row_id]
        assert source == ("others" if record.get("attribution") else "ours"), row_id
        assert f"C{confirmation}" == record["confirmation"], row_id


def test_counts_are_the_declared_rungs(register: list[dict]) -> None:
    stats = overview_data.stats(overview_data.load())
    ours = [r for r in register if not r.get("attribution")]
    others = [r for r in register if r.get("attribution")]
    assert (stats.total, stats.ours, stats.others) == (len(register), len(ours), len(others))
    assert stats.verification == Counter(r["verification"] for r in register)
    assert stats.confirmation_ours == Counter(r["confirmation"] for r in ours)
    assert stats.confirmation_others == Counter(r["confirmation"] for r in others)
    assert stats.cases_1_100_proved + stats.cases_1_100_open == 100


@pytest.fixture
def shared_html(request: pytest.FixtureRequest) -> str:
    """Resolve the shared page during setup, before its independent fresh render.

    Resolving it in the assertion rendered a cold overview twice in call time
    (12.49 s on run 37777128452). The fresh render remains uncached.
    """
    return cast(str, request.getfixturevalue(request.param))


@pytest.mark.parametrize(
    ("render", "shared_html"),
    [(render_overview.overview_page, "page"), (render_overview.results_page, "results")],
    ids=["overview", "results"],
    indirect=["shared_html"],
)
def test_the_render_is_deterministic(
    render: Callable[[], render_overview.Page], shared_html: str
) -> None:
    """A fresh render of each page is the shared one, byte for byte, which is what lets
    every other check read the shared render. One page per node: the two fresh renders
    together held one node past the per-test ceiling (12.25 s on run 37372707772)."""
    assert render().html == shared_html


def test_the_results_table_has_its_own_page_and_the_overview_points_to_it(
    page: str, results: str, served: Callable[[str], str]
) -> None:
    """The table is on `all-results.html`, marked current in the bar, with its sorting
    and filters; the overview keeps no row of it, only a pointer under the recent table."""
    assert render_overview.RESULTS_PAGE == "all-results.html"
    assert "all-results.html" in render_overview.SITE_PAGES
    # `results.html` was `RESULTS.md` as a page, and now forwards to the table.
    assert "results.html" not in render_overview.SITE_PAGES
    assert dict(render_overview.MOVED_PAGES)["results.html"] == "all-results.html"
    assert 'aria-current="page" href="all-results.html">Results</a>' in results
    assert "data-site-table" in results
    assert results.count(_asset_tag(render_overview.TABLE_SCRIPT)) == 1
    table = render_overview.TABLE_SCRIPT.read_text(encoding="utf-8")
    assert table in served(render_overview.RESULTS_PAGE)
    assert '<h1 id="every-result">' in results
    assert not ROW.findall(page)
    assert 'id="every-result"' not in page
    recent = page.split('id="recent-results"', 1)[1].split("<h2", 1)[0]
    # The one action under the table: the site's action button, a link with the arrow.
    assert (
        '<p class="site-action-row site-more"><a class="site-action" href="all-results.html">'
        f"See all results{overview_sections.arrow_icon('right')}</a></p>"
    ) in recent


def test_every_link_to_a_result_goes_to_its_row(
    page: str, results: str, case_pages: dict[str, str]
) -> None:
    """The overview's recent table and replay table, and the case records, link a
    result at its row on the results page, never at a fragment of their own page."""
    rows = {row_id for row_id, _, _ in ROW.findall(results)}
    linked = re.findall(r'href="all-results\.html#([^"]+)"', page)
    assert linked
    # The one link to the results page that is not a row: the Verification Ladders
    # section under its table, since 2026-10-02.
    assert set(linked) - rows == {"verification-ladders"}
    assert 'id="verification-ladders"' in results
    assert not re.search(r'href="#t-\d+"', page)
    for record in case_pages.values():
        assert set(re.findall(r'href="\.\./all-results\.html#([^"]+)"', record)) <= rows
        assert 'href="index.html#t-' not in record
        assert 'href="../index.html#t-' not in record


def test_every_moved_fragment_is_one_the_forwarder_sends_on(page: str, results: str) -> None:
    """`forward.js` sends `#every-result` and a row's id from the overview to the results
    page (`tests/node/overview_forward` runs it): every row id is of the form it
    recognises, the section's lands on the page's title, and no id the overview keeps is."""
    forward = render_overview.FORWARD_SCRIPT.read_text(encoding="utf-8")
    for sent in (
        'id === "every-result"',
        'id === "verification-ladders"',
        'id === "verification-at-a-glance"',
        "/^t-\\d+$/.test(id)",
    ):
        assert sent in forward, sent
    assert f'"{render_overview.RESULTS_PAGE}"' in forward
    # Every other fragment goes to the explainer where it is served now, not through the
    # forwarder at its old address.
    assert f'"{overview_sections.LOWER_BOUNDS_PAPER}"' in forward
    assert '"explainer.html"' not in forward
    moved = re.compile(r"every-result|verification-ladders|verification-at-a-glance|t-\d+")
    assert all(moved.fullmatch(row_id) for row_id, _, _ in ROW.findall(results))
    for landing in ("every-result", "verification-ladders", "verification-at-a-glance"):
        assert f'id="{landing}"' in results, landing
    assert not [i for i in ID.findall(page) if moved.fullmatch(i)]


def test_the_page_fetches_only_the_shared_assets(page: str) -> None:
    """The page fetches what it is drawn with from the site's shared assets and nowhere
    else, and every file it names is one the build writes beside it. The same page with
    one program or one stylesheet named from anywhere else is refused."""
    render_overview.assert_fetches_only_assets("index.html", page)
    assert site_assets.shared().assets.referenced([page])
    for shared, elsewhere in (
        ('<script src="assets/js/', '<script src="js/'),
        ('<link rel="stylesheet" href="assets/css/', '<link rel="stylesheet" href="css/'),
        (
            '<link data-site-font-preload href="assets/fonts/',
            '<link data-site-font-preload href="https://example.com/fonts/',
        ),
    ):
        moved = page.replace(shared, elsewhere, 1)
        assert moved != page, shared
        with pytest.raises(SystemExit):
            render_overview.assert_fetches_only_assets("index.html", moved)


def test_the_bar_leads_with_case_11_beside_the_name(page: str) -> None:
    """The bar's home link carries case 11, the tab's icon, in the bar's own ink."""
    link = page.split('<a class="site-name"', 1)[1].split("</a>", 1)[0]
    assert '<svg class="site-logo" ' in link
    assert 'aria-hidden="true"' in link.split("<svg", 1)[1].split(">", 1)[0]
    assert '<span class="site-name-text">Square Packing</span>' in link
    assert render_overview.site_logo() in link


def test_the_site_icons_have_stable_same_origin_addresses(page: str) -> None:
    icon = render_overview.favicon_html()
    assert page.count(icon) == 1
    assert 'type="image/svg+xml" href="favicon.svg"' in icon
    assert 'sizes="48x48" href="favicon-48.png"' in icon
    assert 'rel="apple-touch-icon"' in icon
    assert 'href="../favicon.svg"' in render_overview.favicon_html(root="../")
    assert "data:image/svg+xml," in render_overview.favicon_html(inline=True)
    render_overview.assert_fetches_only_assets("index.html", icon)


def test_the_hero_draws_its_case_and_links_to_its_row(page: str) -> None:
    n = overview_sections.HERO_CASE
    hero = page.split('class="site-hero-figure', 1)[1].split("</figure>", 1)[0]
    assert f'href="frontier.html#n-{n}"' in hero
    assert hero.count("<svg ") == 1


def _atlas_cards(page: str) -> list[tuple[str, str]]:
    """The atlas's direct cards, the PDFs and Videos section's: each href and body."""
    section = page.split('id="pdfs-and-videos"', 1)[1].split("<h2", 1)[0]
    frame = section.split('class="site-cards-frame', 1)[1]
    return re.findall(
        r'<a class="site-card site-card-link" href="([^"]+)"(.*?)</a>', frame, re.DOTALL
    )


def test_the_posters_and_the_film_have_a_section_of_their_own_under_the_atlas(
    page: str,
) -> None:
    """The Atlas of Square Packings keeps the grid and its expander, and holds no card.
    The two posters and the film follow under an ordinary section heading, PDFs and
    Videos, after Recent Results since the atlas moved above it on 2026-10-04, with its
    own id and its entry in the page's contents, and their note, the star, the shorter
    film, the release and the SVGs, goes with them."""
    heading = '<h2 id="pdfs-and-videos">PDFs and Videos</h2>'
    assert page.count(heading) == 1
    atlas = page.split('id="the-atlas-of-square-packings"', 1)[1].split("<h2", 1)[0]
    assert "data-atlas-grid" in atlas
    assert 'class="site-cards-frame' not in atlas
    assert 'class="site-card ' not in atlas
    # The grid's own note under the expander went on 2026-10-02 (think-l38m); the
    # posters' note is the PDFs and Videos section's.
    assert atlas.count('class="site-atlas-note"') == 0
    assert 'class="site-wide site-atlas-note"' not in atlas
    assert page.index('id="the-atlas-of-square-packings"') < page.index(heading)
    section = page.split(heading, 1)[1].split("<h2", 1)[0]
    assert section.lstrip().startswith('<div class="site-cards-frame')
    assert section.count('<a class="site-card site-card-link"') == len(
        overview_sections.ATLAS_CARDS
    )
    note = section.split('<p class="site-wide site-atlas-note">', 1)[1].split("</p>", 1)[0]
    # The star is keyed once on the page, in the legend under the recent table
    # (`rung_legend`); the note links that table and says it no second time.
    assert note.startswith(
        'On the posters, each star marks a <a href="#recent-results">new result</a>.'
    )
    assert "22 August" not in note
    assert section.index('class="site-cards-frame') < section.index("site-atlas-note")
    for linked in ("ascent-n1-100-1080p60-citations.mp4", "known-best-1-324.svg"):
        assert linked in note, linked
    assert 'id="kpress-page-model"' not in page


def test_the_atlas_section_is_named_for_its_packings_and_the_sections_run_in_order(
    page: str,
) -> None:
    """The homepage's atlas section is The Atlas of Square Packings, and it was The Atlas
    until 2026-10-01: an empty anchor in the heading keeps `#the-atlas` landing on it.
    The sections run in the owner's order: the problem, the project with its page cards,
    the atlas, the recent results, then the posters and film, the other projects and the
    documents. The atlas stood after the recent results until 2026-10-04. Verification
    Ladders stood between the recent results and the atlas until 2026-10-02, and is the
    results page's since; The Frontier Survey stood after the atlas until the same day,
    and its card is a page card since."""
    heading = (
        '<h2 id="the-atlas-of-square-packings">The Atlas of Square Packings'
        '<a id="the-atlas"></a></h2>'
    )
    assert page.count(heading) == 1
    assert 'href="#the-atlas"' not in page
    assert '<h1 id="the-problem"' in page
    assert re.findall(r'<h2 id="([^"]+)"', page) == [
        "the-squares-project",
        "the-atlas-of-square-packings",
        "recent-results",
        "pdfs-and-videos",
        "other-square-packing-projects",
        "squares-project-documentation",
    ]


def test_the_atlas_posters_are_hero_cards_each_opening_its_pdf(page: str) -> None:
    """Each poster is a card headed by its picture that is itself the link to its PDF,
    typed as PDF and never marked for download, so the browser opens it in place."""
    cards = dict(_atlas_cards(page))
    for stem, hero in (
        ("known-best-1-100", "known-best-1-100-card.png"),
        ("known-best-1-324", "known-best-1-324.png"),
    ):
        body = cards[f"{stem}.pdf"]
        assert body.startswith(' type="application/pdf"'), stem
        assert f'<span class="site-card-hero"><img src="{hero}" alt=""' in body, stem
        assert (COMPOSITE_ASSETS[0].parent / hero).is_file(), hero
    assert re.search(r"<a\b[^>]*\sdownload\b", page) is None


def test_every_lazy_atlas_card_reserves_its_source_image_dimensions(page: str) -> None:
    """A delayed thumbnail fetch cannot change its intrinsic aspect ratio."""
    cards = dict(_atlas_cards(page))
    for href, hero, *_ in overview_sections.ATLAS_CARDS:
        source = next(path for path in COMPOSITE_ASSETS if path.name == hero)
        width, height = struct.unpack(">II", source.read_bytes()[16:24])
        image = re.search(rf'<img\b[^>]*\ssrc="{re.escape(hero)}"[^>]*>', cards[href])
        assert image is not None
        assert f'width="{width}"' in image[0]
        assert f'height="{height}"' in image[0]
        assert 'loading="lazy"' in image[0]


def test_the_atlas_film_is_a_hero_card_opening_the_visualize_page(page: str) -> None:
    """The film is no longer embedded here: its card, headed by a frame of the film served
    beside the page, opens the Visualize page, which shows the film alone."""
    cards = _atlas_cards(page)
    assert [href for href, _ in cards] == [
        "known-best-1-100.pdf",
        "known-best-1-324.pdf",
        overview_sections.VISUALIZE_PAGE,
    ]
    body = dict(cards)[overview_sections.VISUALIZE_PAGE]
    assert f'<img src="{OVERVIEW_FILM_POSTER.name}" alt=""' in body
    # Under a heading that says PDFs and Videos, each label says which its card is.
    assert '<span class="site-card-label">Film \u00b7 Video</span>' in body
    labels = [
        re.findall(r'<span class="site-card-label">([^<]*)</span>', body) for _, body in cards
    ]
    assert labels == [["Poster \u00b7 PDF"], ["Poster \u00b7 PDF"], ["Film \u00b7 Video"]]
    assert OVERVIEW_FILM_POSTER in COMPOSITE_ASSETS
    assert OVERVIEW_FILM_POSTER.is_file()
    assert "<video" not in page


def _page_cards(page: str) -> list[tuple[str, str, str]]:
    """The overview's page cards, its first card section: each card's address, the rest
    of its opening tag, and its body."""
    frame = page.split('<div class="site-cards-frame', 1)[1].split("</div></div>", 1)[0]
    cards = re.findall(
        r'<a class="site-card site-card-link" href="([^"]+)"([^>]*)>(.*?)</a>', frame, re.DOTALL
    )
    assert frame.count("site-card-label") == len(cards), "a page card that is not a link"
    return cards


def _page_card_parts(page: str, href: str) -> tuple[str, str]:
    """A page card's value and note: on the overview, or a paper's card on the Papers
    page, whose cards are its first card section too."""
    (body,) = [body for address, _, body in _page_cards(page) if address == href]
    value, note = body.split('class="site-card-value">', 1)[1].split(
        '<span class="site-card-note">'
    )
    return value, note


def test_each_page_card_is_a_plain_link_to_its_page(page: str) -> None:
    """The overview's seven page cards lead to full pages the site serves, so each card
    is the link itself and goes there in the same tab: an `<a href>` with the page icon
    (`data-go="page"`), no popover, no framed preview and no new tab. Each keeps its
    label, headline, note and size. The three parts of the n = 11 series stand together
    in reading order, as on the Papers page: each card carries its Papers card's label,
    title and line, Part III's within what T-060's rungs allow, and an address a
    directory below the site's root."""
    cards = _page_cards(page)
    pages = overview_sections.PAGES
    assert [href for href, _, _ in cards] == [href for href, *_ in pages]
    # The Frontier page's card is first, alone on its line, up from The Frontier Survey's
    # section since 2026-10-02 (think-ec5k, think-ns3d;
    # `test_the_frontier_survey_is_the_frontier_pages_and_its_card_is_a_page_card`).
    assert [href for href, *_ in pages] == [
        "frontier.html",
        "papers/n11-lower-bounds-explainer.html",
        "papers/n11-threshold-bound-review.html",
        "papers/n11-optimality-review.html",
        "papers/square-packing-methods-survey.html",
        "tutorial.html",
        "workbench/",
    ]
    for card, paper in zip(pages[1:4], overview_sections.PAPERS[:3], strict=True):
        assert card == (paper.href, paper.label, paper.title, paper.description)
    assert [card[1] for card in pages[1:4]] == ["Part I", "Part II", "Part III"]
    assert overview_sections.OPTIMALITY is overview_sections.PAPERS[2]
    note = pages[3][3]
    assert note.startswith(
        "Explains Queuingtheorydotcom\u2019s proof that Trump\u2019s packing"
    )
    assert "(T-060)" in note
    assert "formal" not in note.lower()
    served = {*render_overview.SITE_PAGES, "workbench/"}
    size = overview_sections.SECTION_CARD_SIZES["pages"]
    for (href, tag, body), (_, label, title, note) in zip(cards, pages, strict=True):
        assert href in served, href
        assert tag == f' data-go="page" data-card-size="{size}"', href
        assert "popovertarget" not in tag, href
        assert 'target="_blank"' not in tag, href
        assert "<button" not in body, href
        assert f'<span class="site-card-label">{label}</span>' in body, href
        value, shown = _page_card_parts(page, href)
        assert card_text(value) == title, href
        # A bound's relation and ellipsis are set inside its formula, which reads back as
        # TeX.
        assert card_text(shown) == note.replace("\u2026", r"\ldots").replace(
            " >= ", r" \ge "
        ), href
        assert f'src="{overview_sections.embed_url(href)}"' not in page, href
    assert "pop-page-" not in page
    frame = page.split('<div class="site-cards-frame', 1)[1].split("</div></div>", 1)[0]
    for popover in ("popover", "<iframe", "<button"):
        assert popover not in frame, popover


def test_a_same_tab_link_card_leads_only_to_a_page_of_the_site() -> None:
    """`link_card` opens a new tab unless told otherwise; told otherwise, it emits no
    `target`, and refuses anything but a page the site serves (`is_site_page`): an
    address off the site, which never replaces this page, and a file beside the page,
    which is not one."""
    made = overview_sections.link_card("frontier.html", "Label", "Headline", "A note.")
    assert ' target="_blank" rel="noopener noreferrer">' in made
    same = overview_sections.link_card(
        "frontier.html", "Label", "Headline", "A note.", new_tab=False
    )
    assert same.startswith(
        '<a class="site-card site-card-link" href="frontier.html" data-go="page" '
        'data-card-size="small">'
    )
    assert "target=" not in same
    assert "rel=" not in same
    assert same.split(">", 1)[1] == made.split(">", 1)[1]
    for address in ("https://github.com/jlevy/squares", "known-best-1-100.pdf"):
        with pytest.raises(SystemExit, match="only a page of this site"):
            overview_sections.link_card(address, "Label", "Headline", "A note.", new_tab=False)


def test_a_site_page_is_a_page_the_site_serves() -> None:
    """`is_site_page` is the one rule for which cards navigate in the same tab: every
    page the site serves (`render_overview.SITE_PAGES`), the papers under `papers/`
    among them, and a directory served by its `index.html`, as `workbench/` is, with or
    without a query or fragment. Every page card's address and every paper's is one;
    nothing else is, and not an address a paper used to have, which serves a forwarder."""
    is_site_page = overview_sections.is_site_page
    for name in render_overview.SITE_PAGES:
        assert is_site_page(name), name
    assert overview_sections.OPTIMALITY_PAPER in render_overview.SITE_PAGES
    for address in (
        "workbench/",
        overview_sections.OPTIMALITY_PAPER,
        "frontier.html?recent=true",
        "cases/",
        "cases/#n-11",
        overview_sections.result_url("T-060"),
        *(href for href, *_ in overview_sections.PAGES),
        *(paper.href for paper in overview_sections.PAPERS),
    ):
        assert is_site_page(address), address
    for address in (
        "",
        "#recent-results",
        "https://github.com/jlevy/squares",
        "known-best-1-100.pdf",
        "nowhere.html",
        "papers/",
        "workbench",
        *(old for old, _ in render_overview.MOVED_PAGES),
        *(old.removesuffix("index.html") for old, _ in render_overview.MOVED_PAGES),
    ):
        assert not is_site_page(address), address


def test_every_other_direct_card_opens_in_a_new_tab(page: str) -> None:
    """A card that is itself the link, other than a page card, opens its target in a new
    tab, on the site or off it, and never hands the new tab a way back to this one: a
    poster's PDF, the film, another project."""
    direct = re.findall(r'<a class="site-card[^"]*"[^>]*>', page)
    same_tab = len(overview_sections.PAGES)
    assert len(direct) == same_tab + len(overview_sections.project_urls()) + len(
        overview_sections.ATLAS_CARDS
    )
    for tag in direct[:same_tab]:
        assert 'target="_blank"' not in tag, tag
    for tag in direct[same_tab:]:
        assert 'target="_blank"' in tag, tag
        assert 'rel="noopener noreferrer"' in tag, tag


def test_a_card_hero_is_served_beside_the_page_never_fetched() -> None:
    hero = overview_sections.card_hero("known-best-1-100-card.png")
    assert hero.startswith('<span class="site-card-hero"><img ')
    assert 'loading="lazy"' in hero
    for address in ("https://example.org/x.png", "//example.org/x.png"):
        with pytest.raises(SystemExit):
            overview_sections.card_hero(address)
    button = overview_sections.card(
        "pop-x",
        "Label",
        "Value",
        "Note",
        href="#x",
        action="Go",
        hero="known-best-1-100-card.png",
    )
    assert button.index('class="site-card-hero"') < button.index('class="site-card-label"')


def test_the_atlas_grid_arrives_with_static_sized_drawing_images(
    page: str, served: Callable[[str], str]
) -> None:
    """All tiles exist in static HTML; each external drawing reserves its box."""
    first, rest = _atlas_template(page, "first"), _atlas_template(page, "rest")
    for content, expected in ((first, range(1, 101)), (rest, range(101, 325))):
        found = re.findall(r'data-atlas-n="(\d+)"', content)
        assert [int(n) for n in found] == list(expected)
        assert content.count("<img ") == len(found)
        assert content.count('width="400" height="400"') == len(found)
    assert "<template data-atlas-" not in page
    script = render_overview.ATLAS_GRID_SCRIPT.read_text(encoding="utf-8")
    assert "IntersectionObserver" not in script
    assert "cloneNode" not in script
    assert script in served("index.html")


def test_the_atlas_grid_expands_from_100_to_324_with_one_button() -> None:
    """Under the grid one centred button, the site's action under a table or grid, reads
    "Show More" with the double chevron down, names what it does and how many cases that
    is, controls the box of tiles, and says it is collapsed; its row ships hidden, since
    only the script makes it act. The script places the rest on the first expand, flips
    the label to "Show Less", the chevron to up, the name and `aria-expanded`, and
    expands the grid when the popover steps past the last case shown."""
    grid = overview_sections.atlas_grid()
    (row,) = re.findall(r'<p class="site-action-row site-atlas-toggle-row">(.*?)</p>', grid)
    assert row == (
        '<button type="button" class="site-action site-atlas-toggle" '
        'data-atlas-toggle aria-expanded="false" aria-controls="atlas-cells" '
        'aria-label="Show more: all 324 cases" data-label-more="Show More" '
        'data-label-less="Show Less" data-name-more="Show more: all 324 cases" '
        'data-name-less="Show less: the first 100">'
        "<span data-atlas-label>Show More</span>"
        f"{overview_sections.arrow_icon('double-down')}</button>"
    )
    # The expander's row ends the grid's block: no note follows it since 2026-10-02.
    assert 'class="site-atlas-note"' not in grid
    script = render_overview.ATLAS_GRID_SCRIPT.read_text(encoding="utf-8")
    assert 'toggle.setAttribute("aria-expanded", String(open))' in script
    assert "toggle.dataset.nameLess : toggle.dataset.nameMore" in script
    assert "toggle.dataset.labelLess : toggle.dataset.labelMore" in script
    assert 'toggleChevron.dataset.arrow = open ? "double-up" : "double-down"' in script
    assert "toggle.textContent" not in script
    assert "rest.hidden = !open;" in script


def test_the_atlas_expander_reuses_the_action_button_and_tokens() -> None:
    """The expander takes the site's one action button's rule, shared with the popover's
    action and widened to a <button>, not a style of its own; its row is the action row,
    whose space under the tiles is the grid's token, and the placed rest is one box the
    grid lays out as its cells, hidden when collapsed."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert (
        ".kpress :is(.site-popover a, button).site-popover-action,\n"
        ".kpress :is(a, button).site-action {"
    ) in css
    assert ".kpress button:is(.site-popover-action, .site-action) {" in css
    assert ".site-atlas-toggle {" not in css
    row = css[css.index(".site-atlas-grid .site-atlas-toggle-row {") :]
    row = row[: row.index("}")]
    assert "--site-action-space: var(--site-atlas-toggle-space);" in row
    action_row = _rule(css, ".kpress .site-action-row")
    # A table's own space below it since 2026-10-02 (think-0o9u), so text that follows
    # a button stands as clear of it as of a table.
    assert "margin-block: var(--site-action-space) var(--site-table-space);" in action_row
    assert "text-align: center;" in action_row
    grid = css[css.index(".site-page .site-atlas-grid {") :]
    assert "--site-atlas-toggle-space:" in grid[: grid.index("}")]
    rest = css[css.index(".site-atlas-rest {") :]
    assert "display: contents;" in rest[: rest.index("}")]
    assert ".site-atlas-rest[hidden] {\n  display: none;" in css


def test_the_atlas_is_rendered_as_the_grid_under_tabs_that_ship_hidden(
    page: str, served: Callable[[str], str]
) -> None:
    """The page is rendered in the grid view, the default, with the two view tabs over
    the tiles: a tablist of buttons, Grid selected and the one stop in the tab order,
    each controlling the box of tiles the script places. The strip ships `hidden`, since
    without the script it would do nothing, as the expander's row does. Both scripts are
    linked, the views' first: the grid's calls it. `test_site_atlas_views` reads the
    two views in a browser."""
    block = re.findall(r'<div class="site-wide site-atlas-grid" ([^>]*)>', page)
    assert block == ['data-atlas-view="grid" data-atlas-size="medium" data-atlas-grid']
    tabs = overview_sections.atlas_view_tabs()
    assert tabs == (
        '<div class="site-tabs site-atlas-views" role="tablist" aria-label="Atlas layout" '
        'data-atlas-views data-atlas-panel="atlas-cells">'
        '<button type="button" role="tab" id="atlas-view-grid" data-atlas-tab="grid" '
        'aria-selected="true" aria-controls="atlas-cells">Grid</button>'
        '<button type="button" role="tab" id="atlas-view-triangle" data-atlas-tab="triangle" '
        'aria-selected="false" aria-controls="atlas-cells" tabindex="-1">Triangle</button>'
        "</div>"
    )
    assert page.count(tabs) == 1
    assert page.count('class="site-tabs site-atlas-views"') == 1
    atlas = page.split('id="the-atlas-of-square-packings"', 1)[1].split("<h2", 1)[0]
    order = [
        atlas.index(mark)
        for mark in (
            "data-atlas-views",
            '<div class="site-atlas-cells" id="atlas-cells">',
            "data-atlas-toggle",
        )
    ]
    assert order == sorted(order)
    # The triangle's key and the line under the expander are gone since 2026-10-02
    # (the owner, think-l38m): the expander's row ends the block.
    assert "site-atlas-key" not in atlas
    assert 'class="site-atlas-note"' not in atlas
    toggle_end = atlas.index("</button></p>", atlas.index("data-atlas-toggle")) + len(
        "</button></p>"
    )
    assert atlas[toggle_end:].startswith("</div>")
    assert not hasattr(overview_sections, "ATLAS_TRIANGLE_KEY")
    for gone in ("Each row ends at a perfect square", "is also in the frontier survey"):
        assert gone not in _seen(page), gone
    assert [key for key, _ in overview_sections.ATLAS_VIEWS] == ["grid", "triangle"]
    view = render_overview.ATLAS_VIEW_SCRIPT.read_text(encoding="utf-8")
    grid = render_overview.ATLAS_GRID_SCRIPT.read_text(encoding="utf-8")
    view_tag = _asset_tag(render_overview.ATLAS_VIEW_SCRIPT)
    grid_tag = _asset_tag(render_overview.ATLAS_GRID_SCRIPT)
    assert page.index(view_tag) < page.index(grid_tag)
    whole = served("index.html")
    assert whole.index(view) < whole.index(grid)
    assert "SiteAtlasView.mount({" in grid
    assert "cells.append" not in grid
    # No tile is written twice, for a second view or a second drawing: one tile a case.
    tiles = re.findall(r'<a class="site-atlas-cell" [^>]*data-atlas-n="(\d+)"', page)
    assert [int(n) for n in tiles] == list(range(1, 325))


def test_the_atlas_marks_each_perfect_square_and_nothing_else_on_a_tile(page: str) -> None:
    """A perfect square ends its row of the triangle, and its tile says so; that mark is
    all the triangle adds to a tile's markup. Where a tile stands is the script's to
    write, since it follows from the window's width."""
    grid = page.split("data-atlas-grid>", 1)[1].split('<p class="site-action-row', 1)[0]
    squares = re.findall(r'data-atlas-n="(\d+)" data-atlas-square ', grid)
    assert [int(n) for n in squares] == [k * k for k in range(1, 19)]
    assert grid.count("data-atlas-square") == 18
    assert 'style="--r:1;--c:0;--o:0"' in _atlas_template(page, "first")
    assert 'class="site-atlas-key"' not in page


def _regularized_index() -> dict:
    import json  # noqa: PLC0415

    from devtools import render_frontier_page  # noqa: PLC0415

    return json.loads(render_frontier_page.REGULARIZED_INDEX.read_text(encoding="utf-8"))


def _atlas_template(page: str, which: str) -> str:
    """The static first or remaining tile run in the atlas block."""
    grid = page.split("data-atlas-grid>", 1)[1].split('<p class="site-action-row', 1)[0]
    if which == "first":
        return grid.split('<div class="site-atlas-cells" id="atlas-cells">', 1)[1].split(
            '<div class="site-atlas-rest" data-atlas-rest hidden>', 1
        )[0]
    return grid.split('<div class="site-atlas-rest" data-atlas-rest hidden>', 1)[1].rsplit(
        "</div></div>", 1
    )[0]


def test_the_atlas_offers_three_sizes_under_tabs_beside_the_views(
    page: str, served: Callable[[str], str]
) -> None:
    """Beside the view tabs, in one row over the tiles, three more choose the size of
    the tiles (think-ht8t): Small, Medium, the default and the size the page is rendered
    at, and Large. The strip is the view tabs' own, a tablist of buttons controlling the
    box of tiles, and ships `hidden` as they do; the key to a tile's marks follows them
    in the same box. The House and Regularized tabs that stood there went on 2026-10-04
    (think-k8x9), with their script: the views' script mounts the sizes, and the page
    links the views' and the grid's alone."""
    assert [key for key, _ in overview_sections.ATLAS_SIZES] == ["small", "medium", "large"]
    assert overview_sections.ATLAS_SIZE == "medium"
    tabs = overview_sections.atlas_size_tabs()
    assert tabs == (
        '<div class="site-tabs site-atlas-sizes" role="tablist" aria-label="Atlas tile size" '
        "data-atlas-sizes>"
        '<button type="button" role="tab" id="atlas-size-small" data-atlas-size-tab="small" '
        'aria-selected="false" aria-controls="atlas-cells" tabindex="-1">Small</button>'
        '<button type="button" role="tab" id="atlas-size-medium" data-atlas-size-tab="medium" '
        'aria-selected="true" aria-controls="atlas-cells">Medium</button>'
        '<button type="button" role="tab" id="atlas-size-large" data-atlas-size-tab="large" '
        'aria-selected="false" aria-controls="atlas-cells" tabindex="-1">Large</button>'
        "</div>"
    )
    assert page.count(tabs) == 1
    # The key closes the box; the page's renderer gives its link to GitHub a new tab.
    controls = (
        '<div class="site-atlas-controls" data-atlas-controls>'
        f'{overview_sections.atlas_view_tabs()}{tabs}<p class="site-atlas-legend" '
    )
    assert page.count(controls) == 1
    key = page.split(controls, 1)[1].split("</p>", 1)[0]
    assert key.endswith("regularized view</a></span>")
    following = page.split(controls, 1)[1].split("</p>", 1)[1]
    assert following.startswith('</div><div class="site-atlas-cells"')
    atlas = page.split('id="the-atlas-of-square-packings"', 1)[1].split("<h2", 1)[0]
    cells = '<div class="site-atlas-cells" id="atlas-cells">'
    assert atlas.index(controls) < atlas.index(cells)
    for gone in ("data-atlas-layers", "data-atlas-layer-tab", "atlas-layer-house", "House"):
        assert gone not in atlas, gone
    assert not hasattr(overview_sections, "ATLAS_LAYERS")
    assert not hasattr(render_overview, "ATLAS_LAYER_SCRIPT")
    assert not (render_overview.BROWSER / "atlas-layer.js").exists()
    whole = served("index.html")
    assert "SiteAtlasLayer" not in whole
    view = render_overview.ATLAS_VIEW_SCRIPT.read_text(encoding="utf-8")
    grid = render_overview.ATLAS_GRID_SCRIPT.read_text(encoding="utf-8")
    # The size the address names is set before any tile is placed, as the view is, and a
    # change of size is a change of layout, moved as a change of view is. Read by
    # pattern, not quoted as JavaScript.
    assert re.search(r'\bSIZE_PARAM = "size";', view)
    mount = view[view.index("function mount(") :]
    assert "dataset.siteAtlasSize" in mount
    assert "priorWidth" in mount
    select_size = view.split("selectSize", 1)[1].split("};", 1)[0]
    assert re.search(r"\bchange\(.*\bmarkSize\(next\)\);", select_size)
    assert "readdress(searchForSize(location.search, next));" in select_size
    assert "history.replaceState(history.state" in view
    assert '"--site-atlas-scale"' in view
    assert '"--site-atlas-tile-max"' in view
    assert "cells.append" not in grid


def test_one_tile_a_case_is_drawn_from_its_regularized_view_where_it_has_one() -> None:
    """Each case with a regularized view has one tile, drawn from that view: the
    regularized rendering reduced by `packing_svg`, the code that reduces a house
    rendering, so it differs from the house drawing only where the view moved a square
    or changed a square's shade. At tile resolution, subpixel moves can round to the
    same drawing; the audited equality set is pinned below. Its name says
    it is the regularized view and its number carries the layer's badge before it. Every
    other case is drawn from its house rendering, unbadged. Read from the generator's own
    markup, before the page's renderer normalizes it."""
    from devtools import render_frontier_page as frontier  # noqa: PLC0415

    page = overview_sections.atlas_grid()
    regularized = overview_sections.atlas_regularized()
    tiles = _atlas_template(page, "first") + _atlas_template(page, "rest")
    tile = re.compile(r'(<a class="site-atlas-cell" [^>]*>)(<img [^>]*>)(<span class=.*?)</a>')
    drawn = {
        int(re.findall(r'data-atlas-n="(\d+)"', a)[0]): (a, d, n)
        for a, d, n in tile.findall(tiles)
    }
    assert list(drawn) == list(range(1, 325))
    mark = overview_sections.atlas_layer_mark()
    for n, (open_tag, drawing, number) in drawn.items():
        is_regularized = n in regularized
        assert drawing == frontier.drawing_img(n, regularized=is_regularized, size=400)
        assert (", regularized view, " in open_tag) == is_regularized
        assert (mark in number) == is_regularized
        assert 'width="400" height="400"' in drawing
        assert frontier.drawing_path(n, regularized=is_regularized) in frontier.drawing_paths()

    identical_thumbnails: set[int] = set()
    for n in regularized:
        assert (frontier.REGULARIZED_RENDERINGS / f"n-{n:03d}.svg").read_bytes() != (
            frontier.RENDERINGS / f"n-{n:03d}.svg"
        ).read_bytes(), n
        if frontier.packing_svg(
            n, units=overview_sections.ATLAS_UNITS, root=frontier.REGULARIZED_RENDERINGS
        ) == frontier.packing_svg(n, units=overview_sections.ATLAS_UNITS):
            identical_thumbnails.add(n)
    # The exact #432 houses and n155's 337 sub-picometre snaps have unchanged
    # tile-scale shades; 400-unit rounding hides moves visible in the full SVG.
    assert identical_thumbnails == {
        129,
        131,
        261,
        70,
        103,
        295,
        105,
        267,
        108,
        155,
        146,
        84,
        86,
        123,
        126,
        127,
    }
    assert "data-atlas-layer" not in tiles


def test_a_case_with_a_new_result_carries_the_star_by_the_frontier_tables_rule() -> None:
    """A case's tile carries the star after its number exactly where the frontier
    table's Recent column stars its row (`render_frontier_page.recent_lower_bounds`, its
    verified lower bound a recent result), and its name ends "new result", as a starred
    row's name does in a table of results (think-wwtt). The star is the site's one star,
    `.site-star`, hidden from assistive technology since the name says it."""
    from devtools import render_frontier_page as frontier  # noqa: PLC0415

    star = overview_sections.atlas_star()
    assert star == '<span class="site-star" aria-hidden="true">★</span>'
    assert overview_sections.STAR in star
    page = overview_sections.atlas_grid()
    tiles = _atlas_template(page, "first") + _atlas_template(page, "rest")
    found = re.findall(
        r'<a class="site-atlas-cell" [^>]*data-atlas-n="(\d+)"[^>]*aria-label="([^"]+)"[^>]*>'
        r'<img [^>]*><span class="site-atlas-n">(.*?)</span></a>',
        tiles,
    )
    assert [int(n) for n, _, _ in found] == list(range(1, 325))
    recent = frontier.recent_lower_bounds()
    frontier_page = site_renders.html("frontier.html")
    rows = dict(re.findall(r'<tr id="n-(\d+)"[^>]*data-recent="(true|false)"', frontier_page))
    assert sorted(int(n) for n in rows) == list(range(1, 325))
    for n, name, number in found:
        starred = recent.get(int(n), False)
        assert starred == (rows[n] == "true"), n
        assert number.endswith(star) == starred, n
        assert number.count(star) == (1 if starred else 0), n
        assert name.endswith(f", {overview_sections.NEW_RESULT}") == starred, n
    assert sum(recent.values()) == len(
        [1 for _, name, _ in found if name.endswith("new result")]
    )
    # A case without a new result: n = 1, the unit square, and n = 25, a perfect square.
    assert not recent[1]
    assert not recent[25]


def test_the_atlas_key_names_the_star_and_the_badge_and_ships_hidden() -> None:
    """The key under the tabs names a tile's two marks in words, each mark beside its
    words as on the tiles: the star, "new result", and the regularized badge,
    "regularized view", linked to the atlas README's section on the layer. Without a
    regularized drawing on the page it names the star alone. It ships `hidden`, with the
    tabs; `atlas-grid.js` shows it as it places the tiles."""
    key = overview_sections.atlas_legend(regularized=True)
    readme = branch_file(overview_sections.ATLAS_REGULARIZED_README, "#the-regularized-views")
    assert key == (
        '<p class="site-atlas-legend" role="note" aria-label="What a tile\u2019s marks mean" '
        "data-atlas-legend>"
        f'<span class="site-atlas-legend-item">{overview_sections.atlas_star()} '
        "<span>new result</span></span> "
        f'<span class="site-atlas-legend-item">{overview_sections.atlas_layer_mark()}'
        f'<a href="{readme}">regularized view</a></span></p>'
    )
    assert readme.endswith("packing/atlas/known-best/README.md#the-regularized-views")
    readme_text = overview_sections.ATLAS_REGULARIZED_README.read_text(encoding="utf-8")
    assert "\n## The regularized views\n" in readme_text
    alone = overview_sections.atlas_legend(regularized=False)
    assert "regularized" not in alone
    assert overview_sections.atlas_star() in alone
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    legend = _rule(css, ".kpress .site-atlas-grid .site-atlas-legend")
    for declaration in (
        "color: var(--site-support-color);",
        "font-size: var(--site-font-size-note);",
        "flex-basis: 100%;",
        "justify-content: center;",
    ):
        assert declaration in legend, declaration


def test_the_sizes_scale_a_tile_by_one_token_in_either_view() -> None:
    """Medium is a scale of 1, the atlas as it was; Small two thirds and Large half as
    wide again, set on the block by its `data-atlas-size`. The grid's least cell is the
    scale times 6.4rem, 4.6rem on a phone, as it was at Medium; the triangle's tile is its
    line's share, scaled down at Small, and no wider than the most a tile may be, scaled,
    never under the least tile."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    block = _rule(css, ".site-page .site-atlas-grid")
    assert "--site-atlas-scale: 1;" in block
    assert "--site-atlas-cell-min: 6.4rem;" in block
    assert "--site-atlas-scale: 0.667;" in _rule(
        css, '.site-page .site-atlas-grid[data-atlas-size="small"]'
    )
    assert "--site-atlas-scale: 1.5;" in _rule(
        css, '.site-page .site-atlas-grid[data-atlas-size="large"]'
    )
    plain = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    assert re.search(
        r"@media \(max-width: 40rem\) \{\s*"
        r"\.site-page \.site-atlas-grid \{\s*--site-atlas-cell-min: 4\.6rem;\s*\}",
        plain,
    )
    shared = _rule(css, ".site-atlas-cells")
    for declaration in (
        "--site-atlas-fit: calc(100cqi / var(--site-atlas-per-line, 1));",
        "--site-atlas-share: calc(var(--site-atlas-fit) * min(1, var(--site-atlas-scale)));",
        "--site-atlas-most: calc(var(--site-atlas-tile-max) * var(--site-atlas-scale));",
        (
            "--site-atlas-tile: clamp(\n"
            "    var(--site-atlas-tile-min),\n"
            "    var(--site-atlas-share),\n"
            "    var(--site-atlas-most)\n"
            "  );"
        ),
        "--site-atlas-cell: calc(var(--site-atlas-cell-min) * var(--site-atlas-scale));",
        "grid-template-columns: repeat(auto-fill, minmax(var(--site-atlas-cell), 1fr));",
    ):
        assert declaration in shared, declaration
    # The size tabs are drawn as the view tabs are, and hidden until the tiles are placed.
    assert "display: none;" in _rule(
        css,
        ".site-atlas-grid .site-atlas-views[hidden],\n"
        ".site-atlas-grid .site-atlas-sizes[hidden],\n"
        ".site-atlas-grid .site-atlas-legend[hidden]",
    )


def test_the_regularized_set_is_the_layer_index_and_refuses_a_stale_drawing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The cases are the ones the layer's index lists as regularized, never a list kept
    here, so a view the layer gains joins the atlas at the next render. A drawing the
    index does not ask for, or one it asks for that is missing, refuses the page; so
    does an index that labels its drawings with another word than the badge's."""
    import json  # noqa: PLC0415

    from devtools import render_frontier_page as frontier  # noqa: PLC0415

    index = _regularized_index()
    listed = tuple(entry["n"] for entry in index["entries"] if entry["status"] == "regularized")
    assert overview_sections.atlas_regularized() == listed
    assert listed, "the atlas has no regularized view to offer"
    drawings = tmp_path / "rendering"
    drawings.mkdir()
    for n in listed[:2]:
        (drawings / f"n-{n:03d}.svg").write_text("", encoding="utf-8")
    copy = tmp_path / "index.json"
    copy.write_text(json.dumps(index), encoding="utf-8")
    monkeypatch.setattr(frontier, "REGULARIZED_INDEX", copy)
    monkeypatch.setattr(frontier, "REGULARIZED_RENDERINGS", drawings)
    with pytest.raises(SystemExit, match=r"stale \(missing \["):
        overview_sections.atlas_regularized()
    for n in listed[2:]:
        (drawings / f"n-{n:03d}.svg").write_text("", encoding="utf-8")
    assert overview_sections.atlas_regularized() == listed
    (drawings / "n-001.svg").write_text("", encoding="utf-8")
    with pytest.raises(SystemExit, match=r"unexpected \[1\]"):
        overview_sections.atlas_regularized()
    (drawings / "n-001.svg").unlink()
    copy.write_text(json.dumps({**index, "label": "tidied"}), encoding="utf-8")
    with pytest.raises(SystemExit, match="labels its drawings 'tidied'"):
        overview_sections.atlas_regularized()


def test_the_marks_hang_either_side_of_a_number_that_stays_centred() -> None:
    """The badge is one dot in the accent, sized in the text it stands with; the star is
    the site's one star in its warm ink. Every number's box is shrunk to the number and
    centred, and on a tile each mark is out of the flow beside it, the badge before its
    start and the star past its end, so a marked number stands where an unmarked one
    does (`devtools.measure_atlas_views.mark_problems` holds the boxes in a browser)."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    dot = _rule(css, ".site-atlas-layer-mark")
    for declaration in (
        "background: var(--kpress-doc-accent);",
        "block-size: 0.5em;",
        "inline-size: 0.5em;",
        "border-radius: 50%;",
    ):
        assert declaration in dot, declaration
    assert "color: var(--site-new-result);" in _rule(css, ".site-star")
    number = _rule(css, ".site-atlas-n")
    for declaration in (
        "inline-size: fit-content;",
        "margin-inline: auto;",
        "position: relative;",
    ):
        assert declaration in number, declaration
    hung = _rule(css, ".site-atlas-n > .site-atlas-layer-mark")
    for declaration in ("position: absolute;", "inset-inline-end: calc(100% + 0.3em);"):
        assert declaration in hung, declaration
    star = _rule(css, ".site-atlas-n > .site-star")
    for declaration in ("position: absolute;", "inset-inline-start: calc(100% + 0.12em);"):
        assert declaration in star, declaration
    assert '[data-atlas-layer="regularized"]' not in css


def test_the_view_tabs_are_the_section_tabs_strip() -> None:
    """A tab that switches a view in place is drawn by the rules that draw a section's
    link tabs, each selector widened to the button: one look, in the one stylesheet
    every page carries. site.css only places the strip over the tiles, on the bar's
    line, and hides it while it is `hidden`."""
    nav = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    for selector in (
        'nav.site-tabs a,\n.site-tabs [role="tab"] {',
        'nav.site-tabs a + a,\n.site-tabs [role="tab"] + [role="tab"] {',
        (
            "nav.site-tabs a:is(:hover, :focus-visible),\n"
            '.site-tabs [role="tab"]:is(:hover, :focus-visible) {'
        ),
        (
            'nav.site-tabs a[aria-current="page"],\n'
            '.site-tabs [role="tab"][aria-selected="true"] {'
        ),
    ):
        assert selector in nav, selector
    button = _rule(nav, '.site-tabs [role="tab"]')
    for declaration in (
        "background: none;",
        "border: 0;",
        "font: inherit;",
        "cursor: pointer;",
    ):
        assert declaration in button
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    placed = _rule(
        css, ".site-atlas-grid .site-atlas-views,\n.site-atlas-grid .site-atlas-sizes"
    )
    assert "line-height: var(--site-nav-line);" in placed
    assert "margin: 0;" in placed
    hidden = (
        ".site-atlas-grid .site-atlas-views[hidden],\n"
        ".site-atlas-grid .site-atlas-sizes[hidden],\n"
        ".site-atlas-grid .site-atlas-legend[hidden]"
    )
    assert "display: none;" in _rule(css, hidden)
    assert "font-size" not in placed
    # The two strips are one row over the tiles, centred, that wraps on a narrow block.
    row = _rule(css, ".site-atlas-grid .site-atlas-controls")
    for declaration in (
        "display: flex;",
        "flex-wrap: wrap;",
        "justify-content: center;",
        "margin-block-end: var(--site-atlas-toggle-space);",
    ):
        assert declaration in row, declaration


def test_the_triangle_is_sized_and_timed_by_tokens_the_script_reads() -> None:
    """The triangle's least and greatest tile and the move's duration and easing are
    tokens of the atlas block. The script reads the least tile, in rem, to say how many
    a line holds, and the two timing tokens to move the tiles; reduced motion sets the
    duration to 0ms, which is no move. A tile's size is the stylesheet's, from the block's
    width and the tiles a line holds, and nothing in the sheet transitions or animates a
    tile's place."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    block = _rule(css, ".site-page .site-atlas-grid")
    for declaration in (
        "--site-atlas-tile-min: 1.625rem;",
        "--site-atlas-tile-max: 4.5rem;",
        "--site-atlas-move-duration: 360ms;",
        "--site-atlas-move-easing: cubic-bezier(0.2, 0, 0, 1);",
        "container-type: inline-size;",
    ):
        assert declaration in block, declaration
    plain = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    assert re.search(
        r"@media \(max-width: 40rem\), \(pointer: coarse\) \{\s*"
        r"\.site-page \.site-atlas-grid \{\s*--site-atlas-tile-min: 2\.5rem;\s*\}",
        plain,
    )
    assert re.search(
        r"@media \(prefers-reduced-motion: reduce\) \{\s*"
        r"\.site-page \.site-atlas-grid \{\s*--site-atlas-move-duration: 0ms;\s*\}",
        plain,
    )
    assert css.count("--site-atlas-move-duration:") == 2
    # The tile's width is declared in the rule both views share, so a change of view
    # restyles no drawing; the triangle's rule reads it. At Medium, a scale of 1, it is
    # the line's share no wider than the most a tile may be, as it was before the sizes
    # (`test_the_sizes_scale_a_tile_by_one_token_in_either_view`).
    shared = _rule(css, ".site-atlas-cells")
    assert "--site-atlas-tile: clamp(" in shared
    assert re.search(r"0\.12\s*\+\s*0\.28\s*\*\s*clamp\(", shared)
    assert "--site-atlas-row-space: 0.4;" in _rule(css, ".site-atlas-cells[data-atlas-wrapped]")
    assert "transform-origin: 0 0;" in _rule(css, ".kpress .site-atlas-cell")
    cells = _rule(css, '.site-atlas-grid[data-atlas-view="triangle"] .site-atlas-cells')
    assert "--site-atlas-tile:" not in cells
    assert (
        "grid-template-columns: repeat(var(--site-atlas-per-line, 1), var(--site-atlas-tile));"
        in cells
    )
    tile = _rule(css, '.kpress .site-atlas-grid[data-atlas-view="triangle"] .site-atlas-cell')
    assert "var(--site-atlas-line, var(--site-atlas-initial-line)) /" in tile
    for rule in (cells, tile):
        assert "transition" not in rule
        assert "animation" not in rule
    # Nor does anything in the block transition its place by another sheet's rule: KPress
    # gives every classed element a 0.01ms transition of every property under reduced
    # motion, which laid the triangle out for a frame with the grid's gaps.
    still = _rule(css, ".site-atlas-cells,\n.site-atlas-cell :is(svg, img),\n.site-atlas-n")
    assert "transition: none;" in still
    script = render_overview.ATLAS_VIEW_SCRIPT.read_text(encoding="utf-8")
    for token in (
        "--site-atlas-tile-min",
        "--site-atlas-tile-max",
        "--site-atlas-scale",
        "--site-atlas-move-duration",
        "--site-atlas-move-easing",
        "--site-atlas-per-line",
    ):
        assert f'"{token}"' in script, token
    for written in ("--site-atlas-line: ", "--site-atlas-column: ", "--site-atlas-opens: "):
        assert written in script, written
    # The script moves with transforms and opacity alone, and never sets a size.
    assert "transform: `translate(" in script
    for sized in ("style.width", "style.height", "style.left", "style.top"):
        assert sized not in script


def test_a_cases_visual_summary_carries_what_the_film_shows() -> None:
    """A case's visual summary, which opens its record (`render_case_pages.
    visual_summary`), is the film's panel for the case: for n = 11, settled by T-060,
    the exact value, its star and badges and both bounds' sources with this project's
    notes; for n = 17, still open, the film's chained bound and what is open; all read
    from the atlas figure and `bound-citations.json` (`atlas_film_facts`)."""
    facts = result_overview.film_facts()
    assert sorted(facts) == list(range(1, 325))
    eleven = facts[11]
    assert eleven["exact"] is True
    assert (eleven["lower"], eleven["upper"]) == (None, "3.877084")
    assert eleven["star"] is True
    assert [label for _, _, label in eleven["badges"]] == ["optimal", "exact", "rigid"]
    assert eleven["open"] == []
    assert eleven["record"] == "n-011"
    assert eleven["cite"]["lower"] == {
        "text": "Queuingtheorydotcom after Levy et al. 2026, Web",
        "corrects": None,
        "note": "(confirmed T-060)",
    }
    assert eleven["cite"]["upper"] == {
        "text": "Trump 1979, Squares in Squares",
        "corrects": None,
        "note": "(confirmed T-011)",
    }
    seventeen = facts[17]
    assert seventeen["exact"] is False
    assert (seventeen["lower"], seventeen["upper"]) == ("4.660442", "4.675531")
    assert seventeen["open"] == ["optimality"]
    assert seventeen["cite"]["lower"]["note"] == "(confirmed T-093)"
    # A floor that stands in for Nagamochi 2005's withdrawn bound names the work it corrects.
    assert facts[150]["cite"]["lower"]["corrects"] == "corrects Nagamochi 2005"
    assert facts[150]["cite"]["upper"]["corrects"] is None
    # The summary draws it between the reference and the note, as the frontier does.
    summary = result_overview.film_facts_html(facts[150])
    tag = '<span class="site-corrects">corrects Nagamochi 2005</span>'
    assert summary.count(tag) == 1
    assert "site-corrects" not in result_overview.film_facts_html(eleven)
    assert facts[1] == {**facts[1], "exact": True, "upper": "1", "lower": None, "open": []}


def test_the_atlas_grid_opens_each_case_in_the_case_popover(
    page: str, served: Callable[[str], str]
) -> None:
    """A cell opens the page's one case popover, which fetches the case's record file
    and shows its record as its own page does (think-t21m). The atlas popover the
    script filled from a JSON of the film's facts, until 2026-10-03, is gone with its
    JSON; its button is the case popover's, to the record's own address."""
    assert page.count('id="pop-case" popover') == 1
    assert 'id="pop-atlas"' not in page
    assert "data-atlas-facts" not in page
    popover = render_case_pages.case_popover()
    assert popover in page
    (action,) = re.findall(r'<a class="site-popover-action"[^>]*>([^<]*)</a>', popover)
    assert action == "Open the Case Record"
    script = render_overview.ATLAS_GRID_SCRIPT.read_text(encoding="utf-8")
    assert "data-atlas-popover" not in script
    assert "data-atlas-facts" not in script
    # Nor in the page as it is served, its stylesheets and programs with it.
    assert "site-atlas-tip" not in served("index.html")


def test_the_document_is_kpress_viewport_with_its_contents_behaviours(
    page: str, served: Callable[[str], str]
) -> None:
    """A site page scrolls the document, so the document is the element kpress watches:
    with `<main>` marked instead, the contents rail's scroll-spy observed a pane that
    never scrolls. kpress's contents-rail and history modules ride on every page, since
    without them nothing marks the section in view: one shared file, which the page
    links."""
    assert page.count("<html data-kpress-viewport ") == 1
    assert '<main class="kpress-page-main kpress-viewport">' in page
    behaviors = site_assets.script_tag(render_overview.kpress_client_asset(), "index.html")
    assert page.count(behaviors) == 1
    whole = served("index.html")
    for module in render_overview.KPRESS_CLIENT_MODULES:
        assert f"/* kpress: js/{module} */" in whole, module


def test_the_big_tables_have_no_outer_border(
    page: str, results: str, rendered: Callable[[str], str]
) -> None:
    """The site's tables, Recent Results, the Results page's table and the frontier
    table, have no frame (the owner, 2026-10-02, `think-wadm`): KPress draws a border
    round every `.kpress-table`, and the site's rule takes it off every `.site-table`,
    keeping the rule under the header and the light rule under each row."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert ".kpress .site-table {\n  border: 0;\n}" in css
    rows = css[css.index(".kpress .site-table tbody tr {") :]
    assert "border-block-end: 1px solid var(--kpress-doc-border);" in rows[: rows.index("}")]
    for name, html_page in (
        ("index.html", page),
        ("all-results.html", results),
        ("frontier.html", rendered("frontier.html")),
    ):
        tables = re.findall(r'<table class="([^"]*)"', html_page)
        assert tables, name
        assert all("site-table" in classes.split() for classes in tables), (name, tables)


def test_every_card_grid_sits_in_a_frame_it_can_measure(page: str) -> None:
    """A card is as wide as a column of the grid its frame fits, which it can know only by
    asking the frame, so every card section is a `.site-cards-frame` holding its grid
    and nothing else: one grid, or for a section set in lines of its own
    (`SECTION_CARD_LINES`) one grid per line, each directly after the one before."""
    grids = re.findall(r'(<div class="[^"]*">|</div>)<div class="site-cards[" ]', page)
    every = re.findall(r'<div class="site-cards[" ]', page)
    assert len(grids) == len(every), "a card grid outside a frame"
    opened = [before for before in grids if before != "</div>"]
    assert all(before == '<div class="site-cards-frame site-wide">' for before in opened)
    assert len(grids) - len(opened) == sum(
        len(lines) - 1 for lines in overview_sections.SECTION_CARD_LINES.values()
    )
    assert "site-cards-dimensions" not in page, "the rating ladders are no card grid"


def test_the_page_cards_keep_the_series_together_at_one_column_width(
    page: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The seven page cards stand in three lines: the Frontier page alone at the top, then
    the three parts of the n = 11 series in reading order, one card per paper, then the
    methods tutorial, first-principles tutorial and workbench (the series plan,
    2026-10-05; one, two and two while the
    site had two papers, the owner, 2026-10-02, `think-ns3d`). A section set in lines of
    its own (`SECTION_CARD_LINES`) is one frame holding a grid per line, a gap apart,
    each marked with its longest line's count, which the stylesheet caps a line of its
    size at, so the lines share one column width and each centres in it. Lines that do
    not count the section's cards are refused."""
    assert overview_sections.SECTION_CARD_LINES == {"pages": (1, 3, 3)}
    assert len(overview_sections.PAGES) == 7
    frame = page.split('<div class="site-cards-frame site-wide">', 1)[1]
    rows = re.findall(r'<div class="site-cards" data-cards-most="3">(.*?)</div>', frame)
    assert [
        re.findall(r'class="site-card site-card-link" href="([^"]+)"', row) for row in rows
    ] == [
        ["frontier.html"],
        [
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-optimality-review.html",
        ],
        ["papers/square-packing-methods-survey.html", "tutorial.html", "workbench/"],
    ]
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    gap = css[css.index(".site-cards + .site-cards {") :]
    assert "margin-block-start: var(--site-card-gap);" in gap[: gap.index("}")]
    screen = _screen_card_rules()
    for section, lines in overview_sections.SECTION_CARD_LINES.items():
        most, size = max(lines), overview_sections.SECTION_CARD_SIZES[section]
        rule = screen[screen.index(f'.site-cards[data-cards-most="{most}"] > .site-card {{') :]
        assert (
            f"--site-cards-line: min(var(--site-cards-{size}), {most});"
            in rule[: rule.index("}")]
        ), section
    monkeypatch.setitem(overview_sections.SECTION_CARD_LINES, "pages", (2, 2))
    with pytest.raises(SystemExit, match="pages: 7 cards in lines of"):
        overview_sections.page_cards()


#: A container query naming how many cards of one size its frame fits to a line from a
#: given width.
_CARDS_TO_A_LINE = re.compile(
    r"@container \(width >= ([\d.]+)rem\) \{\s*\.site-cards \{\s*"
    r"--site-cards-(small|medium|large): (\d+);\s*\}\s*\}"
)
#: Each card size's minimum column, in rem, and the most to a line the stylesheet steps
#: to: `paper-design.md`, Cards.
#: Each size's minimum column in rem and the most cards it sets to a line: four at most for
#: every size (the owner, 2026-10-05).
CARD_COLUMNS = {"small": (12, 4), "medium": (16, 4), "large": (21, 4)}


def _screen_card_rules() -> str:
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    screen = css[css.index("@media screen {\n  .site-cards {") :]
    return screen[: screen.index("\n}\n")]


def test_every_card_line_centres_on_its_line() -> None:
    """On screen the cards are one wrapping row that centres every line it does not fill,
    four cards on a wide screen and the last line of a long section alike, and a medium
    card keeps the width of a column of the grid the frame fits: n 16rem columns and
    n - 1 1rem gaps. Print keeps that grid, filled from the left."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    base = css[css.index(".site-cards {") :]
    base = base[: base.index("}")]
    assert "--site-card-gap: 1rem;" in base
    assert "grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr));" in base
    screen = _screen_card_rules()
    row = screen[: screen.index("}")]
    for declaration in ("display: flex;", "flex-wrap: wrap;", "justify-content: center;"):
        assert declaration in row
    card = screen[screen.index(".site-cards > .site-card {") :]
    card = card[: card.index("}")]
    assert "--site-cards-line: var(--site-cards-medium);" in card
    assert "calc((var(--site-cards-line) - 1) * var(--site-card-gap));" in card
    assert "flex: 0 0 calc((100% - var(--site-cards-gaps)) / var(--site-cards-line));" in card
    assert "min-inline-size: 0;" in card
    cards = css[css.index("/* ---------- Cards") : css.index(".kpress .site-card {")]
    assert ":has(" not in cards, "a card line centres without counting its cards"


def test_each_card_size_is_a_column_of_its_own_grid() -> None:
    """A card of each size is as wide as a column of the grid of that size's columns the
    frame fits: n columns of minimum m rem and n - 1 1rem gaps need (m + 1)n - 1 rem, so
    each size's count steps at exactly those widths, and a card that names no size is
    medium."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    steps: dict[str, list[tuple[float, int]]] = {size: [] for size in CARD_COLUMNS}
    for width, size, count in _CARDS_TO_A_LINE.findall(css):
        steps[size].append((float(width), int(count)))
    assert tuple(steps) == overview_sections.CARD_SIZES
    for size, (minimum, most) in CARD_COLUMNS.items():
        assert [count for _, count in steps[size]] == list(range(2, most + 1)), size
        assert all(width == (minimum + 1) * count - 1 for width, count in steps[size]), size
    base = css[css.index(".site-cards {") :]
    base = base[: base.index("}")]
    screen = _screen_card_rules()
    for size in CARD_COLUMNS:
        assert f"--site-cards-{size}: 1;" in base
        if size != "medium":
            rule = screen[
                screen.index(f'.site-cards > .site-card[data-card-size="{size}"] {{') :
            ]
            assert f"--site-cards-line: var(--site-cards-{size});" in rule[: rule.index("}")]
    assert '[data-card-size="medium"]' not in css


#: A card, as its opening tag's size and everything after its caps label: the headline,
#: the note and a direct card's address.
_CARD_ELEMENT = re.compile(
    r'<(button|a|div)\b[^>]*class="site-card[ "][^>]*data-card-size="([^"]*)"[^>]*>'
    r'.*?<span class="site-card-value">(.*?)</(?:button|a)>',
    re.DOTALL,
)


def _card_sections(page: str) -> dict[str, list[tuple[str, str]]]:
    """Each card section of the overview, in page order, as its cards' (size, text)."""
    frames = page.split('<div class="site-cards-frame')[1:]
    assert len(frames) == len(overview_sections.SECTION_CARD_SIZES)
    return {
        name: [(size, text) for _, size, text in _CARD_ELEMENT.findall(frame)]
        for name, frame in zip(overview_sections.SECTION_CARD_SIZES, frames, strict=True)
    }


def test_every_card_names_one_of_three_sizes(page: str) -> None:
    """Every card says its size in `data-card-size`, small, medium or large, and a
    section's cards are all the size the section declares, so its lines are one grid."""
    assert overview_sections.CARD_SIZES == ("small", "medium", "large")
    sections = _card_sections(page)
    assert sum(len(cards) for cards in sections.values()) == len(
        re.findall(r'<(?:button|a|div)\b[^>]*class="site-card[ "]', page)
    ), "a card with no size"
    assert [len(cards) for cards in sections.values()] == [
        len(overview_sections.PAGES),
        len(overview_sections.ATLAS_CARDS),
        len(overview_sections.project_urls()),
        len(overview_sections.DOCUMENTS),
    ]
    for name, cards in sections.items():
        declared = overview_sections.SECTION_CARD_SIZES[name]
        assert {size for size, _ in cards} == {declared}, name
    assert overview_sections.SECTION_CARD_SIZES == {
        "pages": "medium",
        "atlas": "medium",
        "projects": "medium",
        "documents": "small",
    }


def test_no_card_leaves_its_math_as_plain_text(page: str) -> None:
    """A card's headline and note are prose whose mathematical runs are set as math
    (`n = 21`, a bound on `s(11)`), so on a card, which is sans, they are sans math
    rather than upright words: nothing `overview_data.MATH` would match is left outside
    a formula on any card."""
    cards = [text for section in _card_sections(page).values() for _, text in section]
    assert len(cards) > len(overview_sections.OTHER_PROJECTS)
    typeset = 0
    for text in cards:
        left = overview_data.MATH.findall(overview_sections.words(text))
        assert not left, (left, overview_sections.reading_text(text))
        typeset += overview_sections.formulas(text)
    assert typeset >= 9


def test_each_sections_size_is_what_its_typical_card_asks_for(page: str) -> None:
    """A section's declared size is the size its median card's text takes by default, so
    the sizes follow the text: a section whose cards grow or shrink past a threshold
    fails here until its size is declared again. The median of an even count is the
    mean of its two middle lengths, as a median is: the four page cards, two short and
    two long, are 71, 103, 171 and 206 characters since the Frontier card left the row
    on 2026-10-02, and their typical card is the 137 of a medium card, not the 171 of a
    large one that the upper middle value alone would say."""
    for name, cards in _card_sections(page).items():
        lengths = sorted(len(overview_sections.reading_text(text)) for _, text in cards)
        middle = len(lengths) // 2
        typical = (
            lengths[middle]
            if len(lengths) % 2
            else (lengths[middle - 1] + lengths[middle]) // 2
        )
        assert (
            overview_sections.size_for_length(typical)
            == overview_sections.SECTION_CARD_SIZES[name]
        ), (name, lengths)


def test_a_card_without_a_declared_size_takes_its_texts() -> None:
    """The default size counts a card's headline and note as they read, a formula once,
    and is small under 80 characters, large from 160 and medium between; a declared size
    wins, and a size that is not one of the three is refused."""
    assert (overview_sections.CARD_SMALL_BELOW, overview_sections.CARD_LARGE_FROM) == (80, 160)
    formula = overview_data.math_html("n = 11")
    assert overview_sections.reading_text(f"Earlier {formula} lower  bounds") == (
        "Earlier n=11 lower bounds"
    )
    assert [overview_sections.size_for_length(n) for n in (0, 79, 80, 159, 160, 400)] == [
        "small",
        "small",
        "medium",
        "medium",
        "large",
        "large",
    ]
    assert overview_sections.card_size("x" * 30, "y" * 49) == "small"
    assert overview_sections.card_size("x" * 30, "y" * 50) == "medium"
    assert overview_sections.card_size("x" * 30, "y" * 130) == "large"

    def built(note: str, size: str | None = None) -> str:
        made = overview_sections.card(
            "pop-x",
            "Label",
            "Headline",
            note,
            href="#recent-results",
            action="Go",
            size=cast("overview_sections.CardSize | None", size),
        )
        return made.split(">", 1)[0]

    assert built("A short note.").endswith('data-card-size="small"')
    assert built("y" * 200).endswith('data-card-size="large"')
    assert built("y" * 200, size="small").endswith('data-card-size="small"')
    link = overview_sections.link_card("frontier.html", "Label", "Headline", "A short note.")
    assert ' data-card-size="small" ' in link.split(">", 1)[0]
    with pytest.raises(SystemExit, match="not a card size"):
        built("A short note.", size="huge")


#: A cell of the rating-ladder diagram: the ladder it belongs to, then, where it holds a
#: rung, the chip's title, scale, level and label, and the description. Nothing follows
#: the description, so a cell with a tally in it is no match.
_LADDER_CELL_RE = re.compile(
    r'<div class="site-ladders-cell(?P<empty> site-ladders-empty)?" role="cell" '
    r'data-ladder="(?P<ladder>[SVC])">'
    r'(?:<div class="site-ladders-rung">'
    r'(?:<span class="site-chip site-rung-fill" title="(?P<title>[^"]*)" '
    r'data-rung="(?P<scale>[VC])" data-level="(?P<level>\d)">(?P<label>[VC]\d)</span>'
    r'|<span class="site-significance" data-level="(?P<s_level>\d)" role="img" '
    r'aria-label="Significance S(?P=s_level) of 5" title="(?P<s_title>[^"]*)">'
    r'<span class="site-significance-label" aria-hidden="true">(?P<s_label>S\d)</span>'
    r'<span class="site-significance-bars" aria-hidden="true">'
    r'(?P<bars>(?:<span class="site-significance-bar"></span>)*)</span></span>)'
    r'<span class="site-ladders-meaning">(?P<meaning>[^<]*)</span></div>)?</div>'
)


class _LADDER_CELL:  # noqa: N801
    """The ladder diagram's cells, a chip's (V and C) and a significance mark's (S) read
    alike: `ladder`, `label`, `scale`, `level`, `title` and `meaning`, and for a mark
    the bars it draws, one per level."""

    @staticmethod
    def finditer(text: str) -> list[dict[str, str | None]]:
        cells = []
        for match in _LADDER_CELL_RE.finditer(text):
            cell = match.groupdict()
            if cell["s_label"]:
                bars = (cell["bars"] or "").count("site-significance-bar")
                assert bars == int(cell["s_level"] or 0), cell
                cell |= {
                    "label": cell["s_label"],
                    "scale": "S",
                    "level": cell["s_level"],
                    "title": cell["s_title"],
                }
            cells.append(cell)
        return cells


def _seen(page: str) -> str:
    """A page's text as a reader sees it: without its inlined styles and programs, its
    comments, and its tags."""
    bare = re.sub(r"<(script|style)\b.*?</\1>", "", page, flags=re.DOTALL)
    bare = re.sub(r"<!--.*?-->", "", bare, flags=re.DOTALL)
    return re.sub(r"<[^>]+>", "", bare)


def _ladders(results: str) -> str:
    """The Verification Ladders section's diagram on the results page, the one block
    between the section's lead and the prose under it."""
    section = results.split('id="verification-ladders"', 1)[1].split("<h2", 1)[0]
    assert section.count('class="site-ladders"') == 1
    return section.split('<div class="site-ladders-frame site-wide">', 1)[1].split("<p", 1)[0]


def _legend(served: str) -> str:
    """The legend under a page's table of results (`rung_legend`)."""
    return served.split('<div class="site-rung-legend"', 1)[1].split("</div>", 1)[0]


def test_a_table_of_results_has_a_legend_of_every_rungs_mark_under_it(
    page: str, results: str
) -> None:
    """Under each table of results stands a legend of three short lines in a box of its
    own (the owner, 2026-10-03, `think-42dx`; it stood between the bar and the table
    until 2026-10-04): every significance mark, S1 to S5;
    every verification and confirmation chip, V0 to C5, each titled with the rubric's
    meaning; and the star, a new result, with a link to the Verification Ladders that
    define each rung in full. It took the place of the key of the ladders' whole grid
    the homepage set under its table."""
    assert not hasattr(overview_sections, "rung_key")
    meanings = overview_sections.rung_meanings()
    expected = [
        f"{scale}{level}"
        for scale in "SVC"
        for level, _ in sorted(overview_sections.rubric_levels()[scale])
    ]
    for served, href in (
        (page, "all-results.html#verification-ladders"),
        (results, "#verification-ladders"),
    ):
        assert served.count('<div class="site-rung-legend"') == 1
        bar = (
            served.index('<div class="site-table-tools')
            if served is results
            else served.index('class="site-recent-scope"')
        )
        at = served.index('<div class="site-rung-legend"')
        assert bar < served.index('<table class="kpress-table site-table site-results"')
        # The legend follows the table's wrap directly, before the rows' popovers.
        follows = re.search(r'</table>(?:</div>)+<div class="site-rung-legend"', served)
        assert follows is not None
        assert follows.end() - len('<div class="site-rung-legend"') == at
        legend = _legend(served)
        assert legend.count("<p>") == 3
        assert RUNG_CHIP.findall(legend) == expected
        for label in expected:
            assert f'title="{html.escape(meanings[label], quote=True)}"' in legend, label
        assert f'<a href="{href}">What each rung means</a>' in legend
        # The star's words are a span of their own, so the face they are drawn in is
        # measured apart from the star's, which no shipped face carries.
        words = f"<span>{overview_sections.NEW_RESULT}</span>"
        assert f"{overview_sections.STAR}</span> {words}" in legend
    assert "site-ladders-key" not in page


def test_the_ladders_are_the_results_pages_and_the_overview_points_to_them(
    page: str, results: str
) -> None:
    """Verification Ladders left the overview for the results page on 2026-10-02 (the
    owner, think-hqb3): the section stands under the table there, headed as it was, with
    the empty anchor of its older fragment; the overview has no ladders section, and the
    legend under its table links the section (think-42dx), its account of the ratings and
    its key of every rung gone since 2026-10-03. The results page's
    opening paragraph points at the section, so a reader meets the table first and the
    account of the ratings is written once, as the section's lead."""
    heading = (
        '<h2 id="verification-ladders">Verification Ladders'
        '<a id="verification-at-a-glance"></a></h2>'
    )
    assert results.count(heading) == 1
    assert "Verification at a Glance" not in results
    assert 'href="#verification-at-a-glance"' not in results
    assert results.index("</table>") < results.index(heading)
    section = results.split(heading, 1)[1].split("<h2", 1)[0]
    lead = _rendered_text(section.split('<div class="site-ladders-frame', 1)[0])
    assert lead.startswith("The three ratings on every row are rungs of three ladders")
    assert "S, how significant the result is; V, how it was originally verified" in lead
    assert "C, how it has been confirmed, what this repository has checked itself" in lead
    assert "under the policy epistemics.md states" in lead
    # The diagram holds no paragraph, so the first `<p>` after its frame opens the prose
    # under it.
    frame_on = section.split('<div class="site-ladders-frame', 1)[1]
    after = _rendered_text(frame_on[frame_on.index("<p>") :])
    assert after.startswith("The ladders grade a result; the evidence under it carries")
    assert "Finite precision is not enough where squares touch exactly." in after
    assert "T-004 and T-008 check Bentz" in after
    intro = _rendered_text(
        results.split("</h1>", 1)[1].split('<div class="site-table-tools', 1)[0]
    )
    assert "the rungs of the Verification Ladders under the table" in intro
    assert '<a href="#verification-ladders">Verification Ladders</a>' in results
    # The ratings are defined once, in the section's lead, and the intro no longer
    # defines them.
    assert "how much the result matters" not in intro
    assert "the strongest verification its evidence supports" not in intro
    # The section and its diagram are gone; its grid is the key's, once.
    for gone in (
        'id="verification-ladders"',
        'id="verification-at-a-glance"',
        '<span class="site-ladders-question">',
        '<a class="site-ladders-name"',
    ):
        assert gone not in page, gone
    assert 'class="site-ladders"' not in page
    # The overview names the ladders nowhere a reader sees: its legend links them.
    assert _seen(page).count("Verification Ladders") == 0
    assert '<a href="all-results.html#verification-ladders">' in _legend(page)
    for scale, _, _, question in overview_sections.DIMENSIONS:
        assert question in results, scale


def test_the_frontier_survey_is_the_frontier_pages_and_its_card_is_a_page_card(
    page: str, rendered: Callable[[str], str]
) -> None:
    """The homepage had a section headed The Frontier Survey, one paragraph and two cards
    to the Frontier page, until the owner dropped it on 2026-10-02 (`think-ec5k`): its
    account is the Frontier page's own prose, and its card to every case is the first of
    the page cards under The Squares Project, alone on its line (`think-ns3d`); the card
    to the recent cases went with it.
    The section's two fragments, `#the-frontier-survey` and the older `#the-survey`, name
    nothing on the homepage, so `forward.js` sends them to the Frontier page, whose title
    carries the first. One vocabulary holds in what a reader sees: the page and its bar
    entry are Frontier, what the page holds is the frontier survey, and "atlas" is the
    grid of packings, never the table of cases, so no page calls the Frontier page an
    atlas."""
    for gone in ('id="the-frontier-survey"', 'id="the-survey"', 'href="#the-survey"'):
        assert gone not in page, gone
    assert '"href": "#the-frontier-survey"' not in page
    assert "The frontier survey is the record the atlas" not in _seen(page)
    assert "frontier.html?recent=true" not in page
    assert '<a data-page="frontier" href="frontier.html">Frontier</a>' in page
    href, tag, body = _page_cards(page)[0]
    assert (href, tag) == ("frontier.html", ' data-go="page" data-card-size="medium"')
    assert '<span class="site-card-label">Frontier survey</span>' in body
    frontier = rendered("frontier.html")
    assert "<title>The Frontier Survey · The Squares Project</title>" in frontier
    assert re.search(r'<h1 id="the-frontier-survey"[^>]*>The Frontier Survey</h1>', frontier)
    for name in (
        "index.html",
        "frontier.html",
        render_case_pages.CASES_PAGE,
        render_overview.RESULTS_PAGE,
    ):
        # What a reader sees or hears: the page without its inlined styles and programs.
        text = re.sub(r"<(script|style)\b.*?</\1>", "", rendered(name), flags=re.DOTALL)
        assert "frontier atlas" not in text.lower(), name


def test_the_frontier_page_opens_with_the_surveys_account(
    rendered: Callable[[str], str], overview: overview_data.Overview
) -> None:
    """The Frontier page's prose, before its table, carries what the homepage's survey
    section carried until 2026-10-02, refined, the survey's account first and the key to
    the table's columns last, beside the table: what the survey records with the case
    counts; the audit of its sources, with the $s(7) = 3$ example and the archive and
    inventory links; the star and the survey's four counts, every number from the record
    and the date written once; the seven authors' seventeen-square bounds before this
    project, replayed as T-015 and T-016; then the columns, with the external
    certificate's rule where the verified columns are defined. The run-in heads are the
    page's own device, so the account groups without a sub-heading. The star's count
    over every case is not written beside the starred cases' count among the first
    hundred, since the two were the one number, 27, on 2026-10-02, and read as a
    stutter."""
    from devtools.render_frontier_page import (  # noqa: PLC0415
        ARCHIVE_README,
        EVIDENCE_INVENTORY,
        recent_lower_bounds,
        since_prose,
        survey_counts,
    )

    page = rendered("frontier.html")
    prose = page.split("</h1>", 1)[1].split('<div class="site-table-tools', 1)[0]
    text = _rendered_text(prose)
    heads = re.findall(r"<p><strong>([^<]+)</strong>", prose)
    assert heads == [
        "Audited sources.",
        "Recent results.",
        "Seventeen squares.",
        "Reported and verified.",
        "The other columns.",
        "A row\u2019s details.",
    ]
    assert text.endswith("Click a column heading to sort; the filters narrow the rows.")
    assert "An external certificate counts once it is replayed here in full" in text
    assert "The survey audits what it records." in text
    assert (
        _markdown_text(
            "The earliest published proof of $s(7) = 3$ carries four recorded defects"
        )
        in text
    )
    assert 'href="cases/7.html" data-case="7"' in prose
    # Each repository document is linked on `main`, in a new tab as every link off the
    # site opens.
    for path, words in (
        (ARCHIVE_README, "literature archive"),
        (EVIDENCE_INVENTORY, "evidence inventory"),
    ):
        assert (
            f'<a href="{repo_url(path)}" target="_blank" rel="noopener noreferrer">{words}</a>'
        ) in prose, words
    # The star's date is written once, and the counts run "since then".
    assert since_prose() == "22 August 2026"
    assert text.count("22 August 2026") == 1
    assert (
        "A star marks a recent verified lower bound, one proved since 22 August 2026, "
        "when this project\u2019s work began."
    ) in text
    assert "Recent holds the star." in text
    counts = render_recent_results.recent_counts(render_recent_results.recent_rows())
    assert overview.counts == counts
    sentence = survey_counts(counts)
    for number in counts:
        assert f" {number} " in sentence, number
    assert sentence.startswith(
        f"Of the first hundred cases, {counts.cases} have a lower bound published or "
        "proved since then"
    )
    assert f"{counts.verified} of those have a recent verified one, the starred cases" in text
    assert sentence in text
    starred = sum(recent_lower_bounds().values())
    assert f"one of the {starred} verified" not in text
    assert "Before this project\u2019s work began, seven authors had published" in text
    for author in ("Brandwijk", "Burns", "MacIver", "Mira", "Fort", "Massaccesi"):
        assert author in text, author
    assert 'href="all-results.html#t-015">T-015</a>' in prose
    assert 'href="all-results.html#t-016">T-016</a>' in prose
    assert 'href="cases/17.html" data-case="17">seventeen-square record</a>' in prose
    # Neither other page says any of this a second time: the Results page points to the
    # policy for results by others and does not restate when a certificate counts. Each
    # page's prose is read without its rows' popovers, whose detail may say a result
    # was replayed here in full, which is that result's own account.
    overview_page = rendered("index.html")
    results_page = rendered(render_overview.RESULTS_PAGE)
    for stated in ("audits what it records", "Brandwijk", "four recorded defects"):
        assert stated not in overview_page, stated
        assert stated not in results_page, stated
    results_prose = results_page.split("</h1>", 1)[1].split('<div class="site-table-tools', 1)[
        0
    ]
    overview_prose = _outside_row_popovers(
        re.sub(r"<table.*?</table>", "", overview_page, flags=re.DOTALL)
    )
    for served in (overview_prose, results_prose):
        assert "certificate is replayed here in full" not in served
        assert "certificate counts once" not in served
        assert "assumptions are discharged" not in served
    results_text = _rendered_text(results_prose)
    # The policy pointer stands in the Verification Ladders' lead, under the table,
    # since 2026-10-02 (think-hqb3), where V and C are defined.
    ladders_lead = _rendered_text(
        results_page.split('id="verification-ladders"', 1)[1].split(
            '<div class="site-ladders-frame', 1
        )[0]
    )
    assert (
        "are this repository\u2019s own verification of it, under the policy epistemics.md "
        "states."
    ) in ladders_lead
    assert "under the policy" not in results_text
    assert (
        "A result by others is dated by its publication, and this project\u2019s by the day "
        "it was established."
    ) in results_text
    assert "dated by its publication" not in _rendered_text(overview_page)


def test_verification_ladders_is_one_ladder_diagram_significance_first(results: str) -> None:
    """The section is one diagram, not three cards: a column a dimension in the order
    Significance, Verification, Confirmation, each headed by its name and question with
    no caps label, and a row a level, the highest first, so the rungs line up. It is a
    grid with table roles, never a `<table>`, which kpress would wrap and restyle and
    `overview/table.js` would look for; on the results page, which has a table, that
    is what keeps the diagram out of the script's hands."""
    assert [scale for scale, *_ in overview_sections.DIMENSIONS] == ["S", "V", "C"]
    diagram = _ladders(results)
    for foreign in ("<table", "site-table", "site-card", "popovertarget"):
        assert foreign not in diagram, foreign
    assert "pop-dimension-" not in results
    assert diagram.startswith(
        '<div class="site-ladders" role="table" aria-label="Verification ladders by level: '
        'significance, verification, confirmation">'
    )
    heads = re.findall(
        r'<div class="site-ladders-head" role="columnheader" data-ladder="([SVC])">'
        r'<a class="site-ladders-name" href="([^"]+)">([^<]+)</a> '
        r'<span class="site-ladders-question">([^<]+)</span></div>',
        diagram,
    )
    assert heads == [
        (scale, f"epistemics.html#{section}", name, html.escape(question, quote=True))
        for scale, name, section, question in overview_sections.DIMENSIONS
    ]
    rows = diagram.split('<div class="site-ladders-row" role="row"')[1:]
    assert len(rows) == diagram.count('role="row"')
    assert rows[0].count('role="columnheader"') == 1 + len(heads)
    levels = [re.match(r' data-level="(\d)">', row) for row in rows[1:]]
    assert [int(level.group(1)) for level in levels if level] == [5, 4, 3, 2, 1, 0]
    for level, row in zip(range(5, -1, -1), rows[1:], strict=True):
        assert f'<span class="site-ladders-level" role="rowheader">Level {level}</span>' in row
        cells = list(_LADDER_CELL.finditer(row))
        assert row.count('role="cell"') == len(cells) == len(heads), level
        assert [cell["ladder"] for cell in cells] == ["S", "V", "C"], level
        held = [cell["label"] for cell in cells if cell["label"]]
        # Significance has no level 0, so its cell there is empty and holds its place.
        assert held == ([f"{scale}{level}" for scale in "SVC"] if level else ["V0", "C0"])
        assert [bool(cell["empty"]) for cell in cells] == [not cell["label"] for cell in cells]


def test_the_ladder_diagram_says_what_the_rubric_says(results: str) -> None:
    """Every rung of `epistemics.md` is a cell: its chip, titled with the rubric's own
    meaning, and its description, which is that meaning unless the rung has a short
    form."""
    levels = overview_sections.rubric_levels()
    assert [len(levels[scale]) for scale in "VCS"] == [6, 6, 5]
    meanings = {
        f"{scale}{level}": meaning
        for scale, rungs in levels.items()
        for level, meaning in rungs
    }
    assert overview_sections.rung_meanings() == meanings
    short = overview_sections.rung_short_meanings()
    assert set(short) == set(meanings)
    # A description differs from the rubric's meaning only where a short form is written:
    # the `Short` column of the V and C tables, or `RUNG_SHORT_MEANINGS` for S.
    written = {
        **overview_sections.rubric_short_forms(),
        **overview_sections.RUNG_SHORT_MEANINGS,
    }
    assert {label for label in short if short[label] != meanings[label]} == {
        label for label, form in written.items() if form != meanings[label]
    }
    cells = {
        cell["label"]: cell
        for cell in _LADDER_CELL.finditer(_ladders(results))
        if cell["label"]
    }
    assert set(cells) == set(meanings)
    for label, cell in cells.items():
        assert (cell["ladder"], cell["scale"], cell["level"]) == (label[0], label[0], label[1])
        assert html.unescape(cell["title"] or "") == meanings[label], label
        assert html.unescape(cell["meaning"] or "") == short[label], label


def test_every_rung_has_a_description_that_fits_two_lines(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A cell's description is a box of exactly two lines, so every rung's text wraps to
    at most two lines of the narrowest cell, `SHORT_MEANING_LINE` characters each, and
    none is cut with an ellipsis. One that does not fit stops the build and asks for a
    short form, as does a short form for a rung the rubric does not have.
    `test_site_ladders` measures the same lines in a browser."""
    short = overview_sections.rung_short_meanings()
    for label, text in short.items():
        lines = textwrap.wrap(text, overview_sections.SHORT_MEANING_LINE)
        assert 1 <= len(lines) <= 2, (label, lines)
        assert not re.search(r"…|\.\.\.", text), label
    long_form = "A reusable technique, bound family, or resolved disputed value"
    assert overview_sections.rung_meanings()["S4"] == long_form
    try:
        monkeypatch.setattr(overview_sections, "RUNG_SHORT_MEANINGS", {})
        overview_sections.rung_short_meanings.cache_clear()
        with pytest.raises(SystemExit, match=r"S4's description.*does not fit two lines"):
            overview_sections.rung_short_meanings()
        monkeypatch.setattr(overview_sections, "RUNG_SHORT_MEANINGS", {"S0": "No such rung"})
        overview_sections.rung_short_meanings.cache_clear()
        with pytest.raises(SystemExit, match=r"names no rung of epistemics\.md: S0"):
            overview_sections.rung_short_meanings()
    finally:
        monkeypatch.undo()
        overview_sections.rung_short_meanings.cache_clear()
    assert overview_sections.rung_short_meanings() == short


def test_every_v_and_c_rung_has_a_short_form_in_the_rubric() -> None:
    """The V and C rungs' two-line descriptions are the `Short` column of their tables in
    `epistemics.md`, one place beside the full meaning the chip's title keeps: every rung
    has one, each at most 60 characters, and the diagram prints exactly those."""
    forms = overview_sections.rubric_short_forms()
    meanings = overview_sections.rung_meanings()
    assert set(forms) == {label for label in meanings if label[0] in "VC"}
    for label, form in forms.items():
        assert form, label
        assert len(form) <= 60, (label, form)
        assert "|" not in form
        assert "`" not in form
    assert forms["V3"] == "Checkable; review record pending"
    assert forms["C5"] == "Formal, replayed here, open, two experts"
    short = overview_sections.rung_short_meanings()
    assert all(short[label] == form for label, form in forms.items())


def test_the_diagram_carries_no_tally_and_keeps_the_rungs_no_result_stands_at(
    results: str, register: list[dict]
) -> None:
    """The diagram says what each rung means and counts nothing: a cell is a chip and a
    description, with no "7 results" and no "no result yet", and the helpers that counted
    are gone. A rung is a cell whether or not a result stands at it, so V5 and C5, which
    the 2026-09-30 ladder reserves for formal, expert-reviewed work and no result has
    reached, are drawn like the rest."""
    diagram = _ladders(results)
    assert "site-ladders-count" not in diagram
    assert not re.search(r"\d+ results?\b|no result yet", diagram)
    for retired in ("rung_counts", "count_label"):
        assert not hasattr(overview_sections, retired), retired
    assert not any(r["verification"] == "V5" or r["confirmation"] == "C5" for r in register)
    cells = {cell["label"] for cell in _LADDER_CELL.finditer(diagram) if cell["label"]}
    assert {"V5", "C5"} <= cells
    rungs = diagram.count('<div class="site-ladders-rung">')
    assert rungs == len(cells) == len(overview_sections.rung_meanings())


def test_every_rung_chip_in_the_diagram_is_titled_with_the_rubrics_meaning(
    results: str,
) -> None:
    """The diagram's wording is `epistemics.md`'s, not a second hand-written copy: every
    `S`, `V` and `C` chip in the ladder diagram carries its rung's full meaning as its
    title, the 2026-09-30 meanings included, and the tables' chips stay bare."""
    meanings = overview_sections.rung_meanings()
    titled = {
        cell["label"]: html.unescape(cell["title"] or "")
        for cell in _LADDER_CELL.finditer(_ladders(results))
        if cell["label"]
    }
    assert set(titled) == set(meanings)
    assert titled == meanings
    assert titled["V3"].startswith("Checkable: a published or audited proof")
    assert titled["C5"].startswith("Formal confirmation: replayed here, open")
    assert re.search(
        r'<span class="site-chip site-rung-fill" data-rung="V" data-level="3">', results
    )


def test_the_ladder_diagram_is_its_own_component_on_the_shared_tokens() -> None:
    """The diagram's rules are its own (`.site-ladders`), and its measures agree with one
    another: the description's box is two lines and is never clipped; a rung sets its
    description beside the rail only where the cell holds the widest rail, the gap and
    the least description; and three columns stand only where each still holds that
    least. It
    stands the tables' space clear of the text. Its one rule is under the column heads:
    no cell and no row carries a border, and the rows are kept apart by space alone."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    for retired in (".site-level", "site-cards-dimensions", "site-ladders-count"):
        assert retired not in css, retired
    rules = css.split("/* ---------- The rating ladders ----------", 1)[1]
    rules = rules.split("/* The atlas grid:", 1)[0]
    assert "margin-block: var(--site-table-space);" in rules
    boxes = re.findall(r"\.site-ladders-meaning \{([^}]*)\}", rules)
    assert "block-size: calc(2 * var(--site-ladders-line));" in boxes[0]
    assert not any("overflow" in box or "clamp" in box for box in boxes)
    assert not re.search(r"text-overflow|line-clamp", rules)

    def rem(token: str) -> float:
        found = re.search(rf"--site-ladders-{token}: ([\d.]+)rem;", rules)
        assert found, token
        return float(found.group(1))

    rail, gap, least, inset = rem("rail"), rem("gap"), rem("meaning-min"), rem("inset")
    # Significance's marks take a wider rail than the chips, and every cell turns at the
    # one width, so the widest rail sets it.
    widest = max(rail, rem("significance-rail"))
    assert widest > rail
    beside = re.search(r"@container \(inline-size >= ([\d.]+)rem\)", rules)
    columns = re.search(r"@container site-ladders \(inline-size < ([\d.]+)rem\)", rules)
    assert beside, "no query sets a description beside its rail"
    assert columns, "no query stacks the ladders"
    assert float(beside.group(1)) == pytest.approx(widest + gap + least)
    assert float(columns.group(1)) / len(overview_sections.DIMENSIONS) - inset >= least

    def body(selector: str) -> str:
        found = re.search(rf"^{re.escape(selector)} \{{([^}}]*)\}}", rules, re.MULTILINE)
        assert found, selector
        return found.group(1)

    # The rail is the chip's own width, now that no count stands under the chip.
    assert "min-inline-size: var(--site-ladders-rail);" in body(".site-ladders-rung .site-chip")
    # The rail is never narrower than what stands in it, so a wider face's mark pushes the
    # description along rather than running into it.
    assert "minmax(var(--site-ladders-rail), max-content)" in rules
    bordered = re.findall(r"([^{}]+)\{[^{}]*\bborder[\w-]*:[^{}]*\}", rules)
    assert [selector.strip() for selector in bordered] == [".site-ladders-head"]
    assert "border-block-end: 1px solid var(--kpress-doc-text);" in body(".site-ladders-head")
    assert "padding-block: var(--site-ladders-row-space);" in body(".site-ladders-cell")
    # Enough to part two rungs that no rule divides, and little enough that they read
    # as one ladder (the owner, 2026-10-01: the rows were too far apart at 0.75rem).
    assert 0.3 <= rem("row-space") <= 0.5


def test_no_placeholder_or_raw_math_is_left(page: str) -> None:
    article = re.sub(r"<script.*?</script>", "", page, flags=re.DOTALL).split("<article", 1)[1]
    assert not re.search(r"\{\{[A-Z0-9_]+\}\}", page)
    assert not re.search(r"\bs\(\d+\) *[<>]=", article)
    assert not re.search(r"(?<![\w\\])\$[^$\s][^$<]*\$", article)


def test_every_record_link_is_on_main_or_a_site_page(overview: overview_data.Overview) -> None:
    for result in overview.results:
        for link in result.records:
            assert (
                link.url.startswith(f"{REPO_URL}/blob/{DEFAULT_BRANCH}/")
                or link.url == "frontier.html"
                or re.fullmatch(r"cases/\d+\.html", link.url)
            ), (result.id, link)


def test_every_repository_link_on_the_page_names_main(page: str) -> None:
    """The deployed-site check refuses a repository link pinned to a commit: every one
    names `main`, the prose's `repo:` links and the "On GitHub" links alike."""
    from devtools.check_published_site import repository_links  # noqa: PLC0415

    assert not hash_pinned_links(page)
    links = repository_links(page)
    assert links
    assert {ref for _, ref, _ in links} == {DEFAULT_BRANCH}


def test_on_github_links_open_the_latest_version(page: str) -> None:
    """Each document card has an "On GitHub" link on `main`."""
    branch = f"{REPO_URL}/blob/{DEFAULT_BRANCH}/"
    also = re.findall(r'<a class="site-popover-also" href="([^"]+)"[^>]*>On GitHub</a>', page)
    assert len(also) == len(overview_sections.DOCUMENTS)
    assert all(url.startswith(branch) for url in also)


def test_the_document_cards_lead_with_readme_and_epistemics(
    page: str, rendered: Callable[[str], str]
) -> None:
    """The documentation section's cards are the reader documents the site renders, in
    the order of `DOCUMENT_PAGES`: README and `epistemics.md` first. The results
    register, the status table and the defect log have no card and no page; the prose
    of the overview links none of them (think-bk2e)."""
    assert re.findall(r'<div class="site-popover" id="pop-doc-([a-z]+)" popover', page) == [
        "readme",
        "epistemics",
        "synopsis",
        "conventions",
        "development",
    ]
    assert re.findall(r">Expand ([A-Za-z.]+)<", page) == [
        "README.md",
        "epistemics.md",
        "SYNOPSIS.md",
        "conventions.md",
        "development.md",
    ]
    for name in ("results.html", "status.html", "defects.html"):
        assert f'"{name}' not in page, name
    for gone in ("RESULTS.md", "STATUS.md", "defects.md"):
        assert f">Expand {gone}<" not in page, gone
    # The survey's two case records are the site's own, not the files on GitHub; they
    # are linked from the Frontier page's prose since 2026-10-02. The files are linked
    # where a record is shown, the Records column and a result's popover, and from no
    # prose of either page.
    frontier = rendered("frontier.html")
    assert '<a href="cases/17.html" data-case="17">seventeen-square record</a>' in frontier
    assert '<a href="cases/7.html" data-case="7">record for seven squares</a>' in frontier
    frontier_prose = frontier.split("</h1>", 1)[1].split('<div class="site-table-tools', 1)[0]
    overview_prose = re.sub(
        r'<div class="site-popover.*?</div>\s*</div>', "", page, flags=re.DOTALL
    )
    overview_prose = re.sub(r"<table.*?</table>", "", overview_prose, flags=re.DOTALL)
    for served in (overview_prose, frontier_prose):
        assert 'packing/frontier/n-007.md"' not in served
        assert 'packing/frontier/n-017.md"' not in served


def test_other_projects_include_every_source_repository_the_record_reviews() -> None:
    coverage = safe_load(
        (overview_data.REPO / "packing/frontier/source-coverage.yaml").read_text(
            encoding="utf-8"
        )
    )
    reviewed = {
        re.sub(r"/tree/.*", "", source["url"])
        for source in coverage["sources"]
        if source["role"] == "source-repository" and "github.com" in source["url"]
    }
    listed = [url for url, _, _ in overview_sections.OTHER_PROJECTS]
    assert reviewed <= set(listed)
    assert len(set(listed)) == len(listed)
    assert not any("jlevy/squares" in url for url in listed)
    assert all(url.startswith("https://github.com/") for url in listed)


def test_every_source_the_coverage_register_reviews_has_a_card() -> None:
    """Every source the source-coverage register reviews, on GitHub or off it, has a card
    in Other Square Packing Projects: a repository's (a revision or a directory of it
    names the repository), the catalogue's, a release's or a record's on Zenodo. No
    address is listed twice."""
    coverage = safe_load(overview_sections.SOURCE_COVERAGE.read_text(encoding="utf-8"))
    listed = [
        overview_sections.source_repository(url) for url in overview_sections.project_urls()
    ]
    reviewed = {
        overview_sections.source_repository(source["url"]) for source in coverage["sources"]
    }
    assert reviewed <= set(listed), sorted(reviewed - set(listed))
    assert len(set(listed)) == len(listed)


#: The record's files a website's card must find its address in: the source-coverage
#: register, the bibliography, the case records, and the retained captures of sources
#: with their packets' READMEs. A capture counts because the address of Friedman's
#: original page is the one the catalogue's own header links, as retained.
CITING_FILES = (
    "packing/frontier/source-coverage.yaml",
    "packing/resources/bibliography.yaml",
    "packing/frontier/n-*.md",
    "packing/resources/web/*.md",
    "packing/resources/web/*/README.md",
)


def test_every_website_card_opens_a_place_the_record_cites(
    page: str, overview: overview_data.Overview
) -> None:
    """Each website's card, a catalogue's or another site's, opens an address the record
    itself cites (`CITING_FILES`), whole, so the list says no more than the record does.
    David Ellsworth's catalogue, the record's `[Kingbird]`, is there and leads the
    section, ahead of Friedman's original page and Evan Daniel's atlas, and its card
    counts exactly the results the register files under the catalogue's venue. No
    GitHub website is an issue or discussion rather than a repository, and every address
    `PROJECT_EXTRA_KEYS` and `SOURCE_VENUES`
    name is listed."""
    texts = [
        path.read_text(encoding="utf-8")
        for pattern in CITING_FILES
        for path in sorted(overview_data.REPO.glob(pattern))
    ]
    assert len(texts) > 300
    sites = [*overview_sections.CATALOGUE_SITES, *overview_sections.OTHER_SITES]
    for url, name, author, note in sites:
        whole = re.compile(re.escape(url) + r"""(?=[\s)\]>"'`|]|$)""", re.MULTILINE)
        assert any(whole.search(text) for text in texts), url
        parsed = urlsplit(url)
        if parsed.hostname == "github.com":
            assert re.fullmatch(r"/[^/]+/[^/]+/(?:issues|discussions)/[0-9]+", parsed.path), url
        assert all((name, author, note)), url
    assert [urlsplit(url).hostname for url, _, _, _ in overview_sections.CATALOGUE_SITES] == [
        "kingbird.myphotos.cc",
        "web.archive.org",
        "evand.github.io",
    ]
    assert overview_sections.CATALOGUE_SITES[0][0] == overview_sections.KINGBIRD
    (first, tally), *_ = overview_sections.listed_projects(overview)
    assert first == overview_sections.KINGBIRD
    bibliography = safe_load(overview_data.BIBLIOGRAPHY.read_text(encoding="utf-8"))
    filed = {
        entry["key"]
        for entry in bibliography["sources"]
        if entry.get("venue") == overview_sections.SOURCE_VENUES[overview_sections.KINGBIRD]
    }
    assert filed <= overview_sections.project_source_keys()[overview_sections.KINGBIRD]
    own = sorted(
        result.id
        for result in overview.results
        if filed & set((result.record.get("attribution") or {}).get("source_keys") or ())
    )
    assert own
    assert sorted(tally.results) == own
    section = page.split('id="other-square-packing-projects"', 1)[1].split("<h2", 1)[0]
    assert section.index(f'href="{overview_sections.KINGBIRD}"') == min(
        section.index(f'href="{url}"') for url in overview_sections.project_urls()
    )
    named = {*overview_sections.PROJECT_EXTRA_KEYS, *overview_sections.SOURCE_VENUES}
    assert named <= set(overview_sections.project_urls())


def test_other_project_cards_are_links_showing_their_address(
    page: str, overview: overview_data.Overview
) -> None:
    """Each other project's card links the project, with no popover, and shows its
    address beside GitHub's mark, or for a website the host's saved favicon or, where
    none is saved, the globe. A card with a tally of results is a box around that link
    and the tally; one with none is the link itself
    (`tests/test_site_project_tallies.py` holds the order, the tallies and their links)."""
    section = page.split('id="other-square-packing-projects"', 1)[1].split("<h2", 1)[0]
    cards = re.findall(
        r'<a class="site-card(?: site-card-link|-link site-card-main)" href="([^"]+)"(.*?)</a>',
        section,
    )
    assert [url for url, _ in cards] == [
        url for url, _ in overview_sections.listed_projects(overview)
    ]
    assert sorted(url for url, _ in cards) == sorted(overview_sections.project_urls())

    def closed(markup: str) -> str:
        """`markup` with each empty element closed as kpress writes it, `<path … />`."""
        return re.sub(r"\s*/>", " />", markup)

    for url, body in cards:
        address = url.removeprefix("https://").rstrip("/")
        assert html.escape(address) in body.replace("<wbr>", ""), url
        assert closed(overview_sections.link_icon(url)) in closed(body), url
    assert closed(overview_sections.GITHUB_MARK) in closed(section)
    assert closed(overview_sections.WEB_MARK) in closed(section)
    assert "popovertarget" not in section
    assert "pop-project-" not in page


def test_record_line_links_point_at_their_entry(overview: overview_data.Overview) -> None:
    lines = overview_data.RESULTS.read_text(encoding="utf-8").splitlines()
    for result in overview.results:
        (register,) = (link for link in result.records if link.label == "register")
        line = int(register.url.rsplit("#L", 1)[1])
        assert lines[line - 1].strip() == f"- id: {result.id}", result.id


def _slug(heading: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")


def test_overview_ids_never_shadow_an_explainer_anchor(page: str, results: str) -> None:
    """`forward.js` sends a fragment the overview lacks to the explainer, so an old
    explainer deep link lands on the overview only if the overview has the same id."""
    explainer = EXPLAINER_ARTICLE.read_text(encoding="utf-8")
    explainer_ids = set(ID.findall(explainer + EXPLAINER_SHELL.read_text(encoding="utf-8")))
    explainer_ids |= {
        _slug(h) for h in re.findall(r"^#{1,4} (.+)$", explainer, flags=re.MULTILINE)
    }
    ours = {i for i in ID.findall(page) if not i.startswith("kpress-")}
    assert not ours & explainer_ids
    moved = {i for i in ID.findall(results) if i.startswith("t-")}
    assert moved
    assert not moved & explainer_ids


def test_the_nav_links_only_to_served_pages() -> None:
    nav = render_overview.nav_html("overview")
    served = {"./", *render_overview.SITE_PAGES, "workbench/"}
    for href in re.findall(r'href="([^"]+)"', nav):
        assert href.startswith("https://") or href in served, href
    assert nav.count('aria-current="page"') == 1


#: The bar's entries, in order: each one's key, where it leads and its label.
NAV_ENTRIES = [
    ("overview", "./", "Overview"),
    ("results", "all-results.html", "Results"),
    ("papers", "papers.html", "Papers"),
    ("frontier", "frontier.html", "Frontier"),
    ("visualize", "visualize.html", "Visualize"),
    ("github", "https://github.com/jlevy/squares", "GitHub"),
]
#: The pages the bar's Papers entry is current on, of those this renderer owns; the
#: explainer, the third, is rendered by its own module and held there
#: (`test_n11_lower_bounds_explainer`).
PAPERS_SECTION = {"papers.html", "tutorial.html"}


def test_the_nav_has_one_papers_entry_for_the_explainer_and_the_tutorial() -> None:
    """The explainer and the tutorial have no entry of their own: Papers leads to the page
    that holds them both, and neither old key can be marked current."""
    nav = render_overview.nav_html("papers")
    entries = re.findall(
        r'<a data-page="(\w+)"(?: aria-current="page")? href="([^"]+)">([^<]+)</a>', nav
    )
    assert entries == NAV_ENTRIES
    assert '<a data-page="papers" aria-current="page" href="papers.html">Papers</a>' in nav
    assert "papers.html" in render_overview.SITE_PAGES
    assert "papers.html" in render_overview.PAGES
    for gone in ("explainer", "tutorial"):
        with pytest.raises(SystemExit):
            render_overview.nav_html(gone)


@pytest.mark.parametrize("name", sorted(render_overview.PAGES))
def test_papers_is_current_on_the_papers_page_and_the_tutorial_alone(
    name: str, rendered: Callable[[str], str]
) -> None:
    """Papers is the current entry on `papers.html` and on the tutorial, which keeps its
    own address, and on no other page this renderer owns."""
    current = re.findall(r'<a data-page="(\w+)" aria-current="page"', rendered(name))
    assert len(current) == 1
    assert (current == ["papers"]) is (name in PAPERS_SECTION), current
    assert set(render_overview.PAGES) >= PAPERS_SECTION


@pytest.mark.parametrize(
    ("prose", "tex"),
    [
        ("s(11) >= 2 + 4/sqrt(5) by a repair", [r"s(11) \ge 2 + 4/\sqrt{5}"]),
        ("s(17), s(18), s(19) >= 459/100 by", [r"s(17), s(18), s(19) \ge 459/100"]),
        ("a bound on s(N) for every 4 <= N <= 100", ["s(N)", r"4 \le N \le 100"]),
        ("s(46) = 7 from the 7 x 7 grid", ["s(46) = 7", r"7 \times 7"]),
        ("need side >= 3.8770835..., equal", [r"\ge 3.8770835\ldots"]),
        ("s(11) > 31/8 by a certificate", ["s(11) > 31/8"]),
        ("Goebel's n = 5 packing", ["n = 5"]),
    ],
)
def test_register_prose_math_is_found_and_set_in_tex(prose: str, tex: list[str]) -> None:
    runs = [match.group(0) for match in overview_data.MATH.finditer(prose)]
    assert [overview_data.prose_tex(run) for run in runs] == tex
    assert overview_data.tex_bounds(prose).count("data-kpress-math") >= len(tex)


@pytest.mark.parametrize("name", sorted(render_overview.PAGES))
def test_every_site_page_has_prepared_math_without_a_runtime_renderer(
    name: str, rendered: Callable[[str], str], served: Callable[[str], str]
) -> None:
    """Prepared mathematics is readable without a post-load geometry change."""
    page = rendered(name)
    assert site_assets.script_tag(site_assets.shared().katex_js, name) not in page
    assert _asset_tag(render_overview.MATH_SCRIPT, name) not in page
    whole = served(name)
    assert render_overview.MATH_SCRIPT.read_text(encoding="utf-8") not in whole
    if 'data-kpress-math="' in page:
        assert 'data-kpress-math-rendered="true"' in page
        assert "<math " in page


@pytest.mark.parametrize("name", ["index.html", "tutorial.html"])
def test_every_site_page_carries_the_explainers_text_tokens(
    name: str, rendered: Callable[[str], str], served: Callable[[str], str]
) -> None:
    """The type base, measure and heading scale come from the one file the explainer
    carries too, after kpress's stylesheets so they win at kpress's own scopes."""
    page = rendered(name)
    links = [
        site_assets.stylesheet_tag(site_assets.shared().kpress_css, name),
        _asset_tag(render_overview.PAPER_TYPE_CSS, name),
        _asset_tag(render_overview.SITE_CSS, name),
    ]
    assert [page.count(link) for link in links] == [1, 1, 1]
    assert [page.index(link) for link in links] == sorted(page.index(link) for link in links)
    whole = served(name)
    tokens = render_overview.PAPER_TYPE_CSS.read_text(encoding="utf-8")
    assert tokens in whole
    assert whole.index(tokens) > whole.index("/* kpress: css/style-tokens.css */")
    assert whole.index(tokens) < whole.index(
        render_overview.SITE_CSS.read_text(encoding="utf-8")
    )


def test_the_text_tokens_are_declared_in_one_place() -> None:
    """No page layer re-declares what `paper-type.css` owns, so no page can drift."""
    owned = (
        "--kpress-host-font-size-base:",
        "--kpress-measure:",
        "--kpress-font-size-h2:",
        "--kpress-host-font-sans:",
    )
    tokens = render_overview.PAPER_TYPE_CSS.read_text(encoding="utf-8")
    for name in owned:
        assert name in tokens, name
    for layer in (
        EXPLAINER_SHELL,
        EXPLAINER_STYLE,
        render_overview.SITE_CSS,
        render_overview.SITE_NAV_CSS,
    ):
        text = layer.read_text(encoding="utf-8")
        for name in owned:
            assert name not in text, f"{layer.name} re-declares {name}"
    assert "{{PAPER_TYPE_CSS}}" in EXPLAINER_SHELL.read_text(encoding="utf-8")


def test_the_shared_stylesheet_states_the_provers_two_palette_colours() -> None:
    """The first paper's stylesheet was a block of its shell, where the renderer filled
    in the two colours the prover's canvases also draw with. As a file of its own it
    states them, so they are held to the renderer's here and cannot drift apart."""
    from devtools import render_n11_lower_bounds_explainer  # noqa: PLC0415

    css = EXPLAINER_STYLE.read_text(encoding="utf-8")
    assert f"  --cert-below: {render_n11_lower_bounds_explainer.BELOW_ONE};\n" in css
    assert f"  --cert-near: {render_n11_lower_bounds_explainer.NEAR_LIMIT};\n" in css
    assert "{{" not in css


def test_the_nav_ends_in_an_accessible_theme_control() -> None:
    """The gear is a named button that opens a menu of three radio items, System, Light
    and Dark, and it is the bar's last item."""
    nav = render_overview.nav_html("overview")
    gear = re.search(r'<button type="button" class="site-theme-button"[^>]*>', nav)
    assert gear, "the nav has no theme gear"
    for attribute in (
        'aria-label="Color theme"',
        'aria-haspopup="menu"',
        'aria-expanded="false"',
        'popovertarget="site-theme-menu"',
    ):
        assert attribute in gear[0], attribute
    assert '<div class="site-theme-menu" id="site-theme-menu" popover role="menu"' in nav
    choices = re.findall(
        r'<button type="button" role="menuitemradio" aria-checked="false" tabindex="-1" '
        r'data-theme-choice="(\w+)">.*?<span>(\w+)</span>',
        nav,
    )
    assert choices == [("system", "System"), ("light", "Light"), ("dark", "Dark")]
    assert nav.index("site-theme") > nav.rindex('data-page="')


@pytest.mark.parametrize("name", sorted(render_overview.PAGES))
def test_every_site_page_carries_the_theme_control(
    name: str, rendered: Callable[[str], str], served: Callable[[str], str]
) -> None:
    page = rendered(name)
    script = render_overview.THEME_SCRIPT.read_text(encoding="utf-8")
    assert page.count('class="site-theme-button"') == 1
    assert page.count(_asset_tag(render_overview.THEME_SCRIPT, name)) == 1
    assert script in served(name)
    # kpress's own bootstrap, in the page itself, applies the stored choice before first
    # paint, and the control stores into the key that bootstrap reads.
    assert 'stored("kpress.theme")' in page
    assert 'storageKey = "kpress.theme"' in script


#: The closing credit as a page carries it: a line a block, a part beside each middle dot.
COLOPHON_LINE = re.compile(
    r'<span class="site-colophon-line">(.*?)</span>(?=<span class="site-colophon-line">|$)'
)
COLOPHON_PART = re.compile(r'<span class="site-colophon-part">(.*?)</span>(?= · |$)')


def test_the_closing_credit_is_two_lines_the_project_and_the_version() -> None:
    """Every footer is made of one definition, `colophon_lines`: the project's formal
    name and its repository, linked, on the first line, and on the second the version
    every artifact prints and the credit to the two tools, each linked where README
    links it. The parts of a line stand either side of a middle dot with a space each
    side. The version is the release's own edition stamp at the pinned data revision, so
    a re-pin or a new edition changes it here with no edit. An atlas poster's footer is
    the same spelling at the data commit the poster was drawn from (`release.edition_at`),
    which a re-pin does not move."""
    from sqpack import release  # noqa: PLC0415

    lines = COLOPHON_LINE.findall(render_overview.colophon_lines())
    assert len(lines) == 2
    first, second = (COLOPHON_PART.findall(line) for line in lines)
    assert first == [
        "The Squares Project",
        '<a href="https://github.com/jlevy/squares">github.com/jlevy/squares</a>',
    ]
    assert second == [
        release.PUBLICATION_EDITION,
        (
            "Formatted and typeset with "
            '<a href="https://github.com/jlevy/flowmark">Flowmark</a> '
            'and <a href="https://github.com/jlevy/kpress">KPress</a>'
        ),
    ]
    for line, parts in zip(lines, (first, second), strict=True):
        assert line == " · ".join(f'<span class="site-colophon-part">{p}</span>' for p in parts)
    assert release.PUBLICATION_EDITION.endswith(release.PUBLICATION_STAMP)
    assert re.fullmatch(r"v\d+\.\d+\.\d+-[0-9a-f]{6}", release.PUBLICATION_STAMP)
    revision = release.DATA_REVISION[: release.DATA_REVISION_LENGTH]
    assert f"{release.PUBLICATION_VERSION}-{revision}" == release.PUBLICATION_STAMP
    assert second[0] == release.PUBLICATION_EDITION == release.edition_at(release.DATA_REVISION)
    # The tools' addresses are the repository's own: README links Flowmark there, and
    # KPress is the submodule this site is rendered with.
    readme = (render_overview.REPO / "README.md").read_text(encoding="utf-8")
    assert f"({render_overview.FLOWMARK_URL})" in readme
    modules = (render_overview.REPO / ".gitmodules").read_text(encoding="utf-8")
    assert f"url = {render_overview.KPRESS_URL}" in modules
    nav_css = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    assert ".site-colophon-line {\n  display: block;\n}" in nav_css
    part = ".site-colophon-part {\n  display: inline-block;\n  text-wrap: balance;\n}"
    assert part in nav_css


@pytest.mark.parametrize("name", sorted(render_overview.PAGES))
def test_every_site_page_ends_with_the_closing_credit(
    name: str, rendered: Callable[[str], str]
) -> None:
    """Each KPress page carries the two lines once, in its footer slot."""
    footer = f'<p class="site-colophon">{render_overview.colophon_lines()}</p>'
    page = rendered(name)
    assert page.count(footer) == 1
    assert page.count('class="site-colophon-line"') == 2


SITE_NAV_BLOCK = re.compile(r'<nav class="site-nav" aria-label="Site">.*?</nav>', re.DOTALL)


def _the_bar(page: str, *, root: str) -> str:
    """The page's one navigation bar with its current mark and its root prefix taken out."""
    bars = SITE_NAV_BLOCK.findall(page)
    assert len(bars) == 1, "a page carries exactly one navigation bar"
    assert bars[0].count(' aria-current="page"') == 1, "the bar marks one page current"
    bar = bars[0].replace(' aria-current="page"', "")
    if root:
        # A link to the root itself, written from below it, is the root's directory,
        # `../`, where the partial writes `{{ROOT}}./`.
        bar = bar.replace(f'href="{root}"', 'href="./"')
    return bar.replace(f'href="{root}', 'href="')


def _workbench_page() -> str:
    """The workbench page as `build_site` gives it the bar, on its own template."""
    from workbench_tools import build_site  # noqa: PLC0415

    template = build_site.WORKBENCH_PACKAGE / "assets" / "template.html"
    return build_site.with_nav(template.read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", [*sorted(render_overview.PAGES), "workbench/index.html"])
def test_every_site_page_carries_the_same_bar(
    name: str, rendered: Callable[[str], str]
) -> None:
    """Every page the Python build renders carries the bar byte for byte as the partial
    writes it, but for which item is current and the prefix that reaches the site's root."""
    assert name in render_overview.SITE_PAGES
    if name == "workbench/index.html":
        page, root = _workbench_page(), "../"
    else:
        # A page in a directory of its own, the case records', reaches the root from it.
        page, root = rendered(name), "../" * name.count("/")
    partial = (
        render_overview.SITE_NAV.read_text(encoding="utf-8")
        .replace("{{ROOT}}", "")
        .replace("{{LOGO}}", render_overview.site_logo())
    )
    assert _the_bar(page, root=root) == SITE_NAV_BLOCK.findall(partial)[0]


def test_the_visualize_section_is_marked_current_on_both_its_pages(
    rendered: Callable[[str], str],
) -> None:
    """The bar's Visualize entry leads to the film and is current on the film's page and
    on the workbench, which share one tab bar with their own tab current."""
    nav = render_overview.nav_html("overview")
    assert '<a data-page="visualize" href="visualize.html">Visualize</a>' in nav
    assert "Visualizer" not in nav
    film = rendered("visualize.html")
    for page, root, tab in ((film, "", "film"), (_workbench_page(), "../", "workbench")):
        assert re.findall(r'<a data-page="(\w+)" aria-current="page"', page) == ["visualize"]
        tabs = render_overview.visualize_tabs(tab, root=root)
        assert page.count('class="site-tabs"') == 1
        assert tabs in page
        assert re.findall(r'<a data-tab="(\w+)" aria-current="page"', tabs) == [tab]
        # In the header slot, directly after the bar, on both pages alike: the bar's
        # stylesheet draws the rule between the two (the next test).
        header = page.split('class="kpress-site-header"', 1)[1].split("</header>", 1)[0]
        assert header.index('class="site-nav"') < header.index(tabs)
        assert re.search(r'</nav>\s*<nav class="site-tabs"', header)
    with pytest.raises(SystemExit):
        render_overview.visualize_tabs("stills")


def test_the_bars_type_is_set_from_the_papers_scale() -> None:
    """The bar's links and a section's tabs take one token, the note step of the paper's
    scale, which is the first size under the body's prose; the site's name takes the sans
    base. Both come from the host base and the scale's own tokens, so no rule holds a
    size in pixels or rem, and the bar is one size on every page. Each token names the
    paper's value as its fallback, for the one page that carries the bar without
    `paper-type.css`, and the fallbacks are that file's values. `test_site_wide_blocks`
    holds the computed sizes to the body's in a browser."""
    css = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    tokens = dict(re.findall(r"\n  (--site-nav-[a-z-]+): ([^;]+);", css))
    assert {name: " ".join(value.split()) for name, value in tokens.items()} == {
        "--site-nav-name-size": (
            "calc( var(--kpress-host-font-size-base, 18px) "
            "* var(--paper-font-scale-sans, calc(19 / 18)) )"
        ),
        "--site-nav-font-size": (
            "calc(var(--site-nav-name-size) * var(--paper-note-scale, 0.92))"
        ),
        # The line the bar's items are set on (`test_the_bars_name_is_aligned_by_its_text`).
        "--site-nav-line": "calc(var(--site-nav-font-size) * 1.43)",
    }
    for selector, token in (
        (".site-nav {", "--site-nav-font-size"),
        (".site-nav .site-name {", "--site-nav-name-size"),
        (".site-tabs {", "--site-nav-font-size"),
    ):
        rule = css[css.index(f"\n{selector}") :]
        rule = rule[: rule.index("}")]
        assert re.findall(r"font-size: ([^;]+);", rule) == [f"var({token})"], selector
    paper = render_overview.PAPER_TYPE_CSS.read_text(encoding="utf-8")
    for declaration in (
        "  --kpress-host-font-size-base: 18px;\n",
        "  --paper-font-scale-sans: calc(19 / 18);\n",
        "  --paper-note-scale: 0.92;\n",
    ):
        assert declaration in paper, declaration


def test_the_bars_name_is_aligned_by_its_text() -> None:
    """The bar aligns its items by their baselines, and the name's row, a mark and the
    text, takes its baseline from the text, not from the mark that leads it, so the name
    stands on the links' baseline at any size of either. Every item is set on one line,
    a length, so the larger name is no taller than a link. `test_site_wide_blocks`
    measures the baselines in a browser."""
    css = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    inner = css[css.index("\n.site-nav-inner {") :]
    assert "  align-items: baseline;\n" in inner[: inner.index("}")]
    assert ".site-nav .site-name-text {\n  align-self: baseline;\n}" in css
    assert "  --site-nav-line: calc(var(--site-nav-font-size) * 1.43);\n" in css
    links = css[css.index("\n.site-nav a {") :]
    assert "  line-height: var(--site-nav-line);\n" in links[: links.index("}")]
    name = css[css.index("\n.site-nav .site-name {\n  align-items: center;") :]
    name = name[: name.index("}")]
    assert "display: inline-flex;" in name
    for nudge in ("translate", "position: relative", "margin-block", "vertical-align"):
        assert nudge not in name, nudge


def test_the_section_tabs_sit_below_the_bars_rule() -> None:
    """The tabs are in the header slot, whose lower border is the rule under the bar, so
    they would stand over it. A header that holds tabs gives up its border and the bar
    draws the rule at its own foot, over the tabs, on a kpress page and in the
    application shell alike. The tabs stand one space under the rule and keep it below
    them only in the shell, where the application starts at the shell's edge; on a kpress
    page the first block starts `--site-page-top` under them. Print hides all three.
    `test_site_wide_blocks` measures the same in a browser."""
    css = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    shell_rule = ".site-app-shell .kpress-site-header {\n  border-block-end: 1px solid"
    handed = ".kpress-site-header:has(> .site-tabs) {\n  border-block-end: 0;\n}"
    drawn = (
        ".kpress-site-header > .site-nav:has(+ .site-tabs) {\n"
        "  border-block-end: 1px solid var(--kpress-doc-border);\n}"
    )
    # After the shell's own rule, which it has the same specificity as.
    assert css.index(shell_rule) < css.index(handed) < css.index(drawn)
    tabs = css[css.index("\n.site-tabs {") :]
    tabs = tabs[: tabs.index("}")]
    assert "--site-tabs-space: 0.7rem;" in tabs
    assert "margin: var(--site-tabs-space) auto 0;" in tabs
    assert (
        ".site-app-shell .site-tabs {\n  margin-block-end: var(--site-tabs-space);\n}"
    ) in css
    assert css.count("--site-tabs-space: ") == 1
    assert "@media print {\n  .site-tabs {\n    display: none;\n  }\n}" in css
    assert "@media print {\n  .site-nav,\n  .kpress-site-header {\n    display: none;" in css


def test_the_film_page_embeds_the_film_at_its_own_proportions(
    rendered: Callable[[str], str],
) -> None:
    """The film is inline with its controls, fetches nothing until it is started, and
    shows a poster at the video's own 16:9, so starting playback moves nothing."""
    page = rendered("visualize.html")
    video = re.search(r"<video [^>]*>", page)
    assert video is not None
    for attribute in (
        'class="site-film"',
        "controls",
        'preload="none"',
        "playsinline",
        'width="1920" height="1080"',
        'poster="ascent-n1-324-poster.png"',
    ):
        assert attribute in video[0], attribute
    assert f'<source src="{render_overview.FILM_URL}" type="video/mp4' in page
    assert page.index('class="site-tabs"') < page.index("<h1") < page.index("<video")


def test_the_film_starts_on_a_visit_to_its_page_and_nowhere_else(
    rendered: Callable[[str], str], served: Callable[[str], str]
) -> None:
    """Visiting the Visualize page starts its film. The markup mutes it, which a browser
    requires of a film it starts unasked, keeps its controls and its inline playback, and
    marks it `data-autoplay`; `overview/film.js`, which only this page carries, starts it
    unless the reader asks for reduced motion or the page is framed in a popover
    (`tests/node/overview_film` runs it). The markup itself has no `autoplay`, so a
    reader the script leaves alone fetches nothing (`preload="none"`), and no `loop`.
    No other page carries the script, and the explainer's film is not marked."""
    page = rendered("visualize.html")
    videos = re.findall(r"<video [^>]*>", page)
    assert len(videos) == 1
    attributes = videos[0].removeprefix("<video ").removesuffix(">").split()
    for attribute in ("controls", "muted", "playsinline", "data-autoplay", 'preload="none"'):
        assert attribute in attributes, attribute
    assert not {"autoplay", "loop"} & {name.partition("=")[0] for name in attributes}
    script = render_overview.FILM_SCRIPT.read_text(encoding="utf-8")
    link = _asset_tag(render_overview.FILM_SCRIPT, "visualize.html")
    assert page.count(link) == 1
    assert page.index("</video>") < page.index(link)
    assert served("visualize.html").count(script) == 1
    for name in render_overview.PAGES:
        if name != "visualize.html":
            # The page as it is served, with every program it links.
            other = served(name)
            assert script not in other, name
            assert "data-autoplay" not in other, name
            assert not re.search(r"<video\b[^>]*\sautoplay\b", other), name
    explainer = re.findall(r"<video [^>]*>", EXPLAINER_ARTICLE.read_text(encoding="utf-8"))
    assert len(explainer) == 1
    assert 'preload="none"' in explainer[0]
    for absent in ("autoplay", "muted", "loop"):
        assert absent not in explainer[0], absent


def test_the_film_page_shows_no_title_and_keeps_one_for_a_screen_reader(
    rendered: Callable[[str], str],
) -> None:
    """The Visualize page shows the bar, the section tabs and the film: no page title and
    no subtitle. It keeps its document title and one `h1`, for a screen reader alone, and
    the film, the first block a reader sees, brings no margin of its own."""
    page = rendered("visualize.html")
    assert "<title>Visualize · The Squares Project</title>" in page
    assert re.findall(r"<h1\b[^>]*>.*?</h1>", page, re.DOTALL) == [
        '<h1 class="site-visually-hidden" id="visualize">Visualize</h1>'
    ]
    article = page.split('class="kpress-prose kpress-long-text site-page">', 1)[1]
    assert article.lstrip().startswith('<h1 class="site-visually-hidden"')
    assert re.search(r'</h1>\s*<figure class="site-film-frame', article)
    for gone in ('class="site-hero"', 'class="subtitle"', "The ascent"):
        assert gone not in article, gone
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    hidden = css[css.index("\n.site-visually-hidden {") :]
    hidden = hidden[: hidden.index("}")]
    for declaration in (
        "block-size: 1px;",
        "clip-path: inset(50%);",
        "inline-size: 1px;",
        "overflow: hidden;",
        "position: absolute;",
    ):
        assert declaration in hidden, declaration
    assert "display: none" not in hidden
    assert "visibility" not in hidden
    assert (
        "@media screen {\n"
        "  .site-page .site-visually-hidden:first-child + .site-film-frame {\n"
        "    margin-block-start: 0;\n  }\n}"
    ) in css


def test_no_site_stylesheet_keys_on_the_system_theme_alone() -> None:
    """An explicit Light or Dark choice must win over the system theme, so the site's
    styles key on kpress's resolved theme, never on `prefers-color-scheme`."""
    for sheet in (
        render_overview.SITE_CSS,
        render_overview.SITE_NAV_CSS,
        EXPLAINER_SHELL,
        EXPLAINER_STYLE,
    ):
        assert "prefers-color-scheme" not in sheet.read_text(encoding="utf-8"), sheet.name


CARD = re.compile(
    r'<button type="button" class="site-card" popovertarget="([^"]+)" '
    r'data-go="(scroll|external|page)" data-card-size="(?:small|medium|large)">'
)
ACTION = re.compile(
    r'<a class="site-popover-action" href="([^"]+)" data-go="(scroll|external|page)"'
)


def test_every_card_shows_where_it_goes_and_gets_there(page: str, results: str) -> None:
    """Every card opens a popover that shows its target and ends in one button that goes
    there. Another page is rendered in a frame, in its embedded view, and the button
    expands it; a place on this page, or another site, is previewed, and the button goes
    there; a row on another page, such as a result's on the results page, is previewed
    too, and the button goes to that page. The card's icon and the button's agree, and
    every target on the site exists.
    The exceptions are the cards that are the link itself, with no popover: the page
    cards, the atlas's and the other projects' (their own tests above)."""
    cards = CARD.findall(page)
    assert "page" in {kind for _, kind in cards} <= {"scroll", "page", "external"}
    assert page.count('class="site-card"') == len(cards)
    ids = set(ID.findall(page))
    rows = set(ID.findall(results))
    served = {*render_overview.SITE_PAGES, "workbench/"}
    for target, kind in cards:
        start = page.index(f'<div class="site-popover" id="{target}" popover')
        # A card's panel ends where the next card begins, or the next popover: a table
        # row's popover, with a button of its own, can follow the section's last card.
        panel = re.split(
            r'<button type="button" class="site-card"|<div class="site-popover[ "]',
            page[start + 1 :],
            maxsplit=1,
        )[0]
        (action,) = ACTION.findall(panel)
        href, action_kind = action
        assert action_kind == kind == overview_sections.card_kind(href), target
        if kind == "scroll":
            assert 'class="site-popover-preview"' in panel, target
            assert href[1:] in ids, href
        elif kind == "external":
            assert 'class="site-popover-preview"' in panel, target
        elif 'class="site-popover-preview"' in panel:
            base, _, row = href.partition("#")
            assert base == render_overview.RESULTS_PAGE, href
            assert row in rows, href
            assert "<iframe" not in panel, target
        else:
            assert re.split(r"[?#]", href, maxsplit=1)[0] in served, href
            found = re.search(r'<iframe [^>]*src="([^"]+)"', panel)
            assert found is not None, target
            frame = html.unescape(found.group(1))
            assert frame == overview_sections.embed_url(href), target
            assert "view=embed" in frame, target


def test_an_embedded_page_keeps_its_query_and_fragment() -> None:
    embed = overview_sections.embed_url
    assert embed("papers.html") == "papers.html?view=embed"
    assert embed("frontier.html?recent=true") == "frontier.html?recent=true&view=embed"
    assert embed("frontier.html#n-21") == "frontier.html?view=embed#n-21"
    assert embed("workbench/") == "workbench/?view=embed"


CHIP = re.compile(r'<span class="site-chip( site-rung-fill)?"([^>]*)>([^<]+)</span>')


@pytest.mark.parametrize("name", ["index.html", "frontier.html", "all-results.html"])
def test_every_small_label_is_one_chip(name: str, rendered: Callable[[str], str]) -> None:
    """Rungs and case statuses share one chip; a rung chip carries its scale and level,
    which the stylesheet colours, and names the rung it shows."""
    html = rendered(name)
    chips = CHIP.findall(html)
    assert chips, name
    for fill, attributes, label in chips:
        if fill:
            assert f'data-rung="{label[0]}" data-level="{label[1:]}"' in attributes, label
    assert "site-rung " not in html
    assert "site-status-proved" not in html


#: A rung chip, and what may stand between two chips of one run: white space.
#: A rung as the site draws it, its label the one group: a V or C chip, or the
#: significance mark, S1 to S5 with its bars (`overview_sections.significance_mark`).
RUNG_CHIP = re.compile(
    r'<span class="(?:site-chip site-rung-fill"(?: title="[^"]*")? data-rung="[VC]" '
    r'data-level="\d'
    r'|site-significance" data-level="\d" role="img" aria-label="[^"]*"(?: title="[^"]*")?>'
    r'<span class="site-significance-label" aria-hidden="true)">([SVC]\d)</span>'
    r'(?:<span class="site-significance-bars" aria-hidden="true">'
    r'(?:<span class="site-significance-bar"></span>)*</span></span>)?'
)
#: The order the site lists a result's rungs in: significance first (think-ucon).
RUNG_ORDER = "SVC"


def _rung_runs(html: str) -> list[list[str]]:
    """Every run of rung chips with only white space between them, as their labels."""
    runs: list[list[str]] = []
    end = None
    for match in RUNG_CHIP.finditer(html):
        if end is not None and not html[end : match.start()].strip():
            runs[-1].append(match.group(1))
        else:
            runs.append([match.group(1)])
        end = match.end()
    return runs


def test_a_results_rungs_run_significance_first(overview: overview_data.Overview) -> None:
    """`rung_chips` is the one place the order is set: S, then V, then C. The status
    cell and a result overview's head open with it (`status_chips`)."""
    assert overview.results
    for result in overview.results:
        record = result.record
        rungs = overview_sections.result_rungs(result)
        assert rungs == (
            f"S{record['significance']['score']}",
            record["verification"],
            record["confirmation"],
        )
        chips = overview_sections.rung_chips(result)
        assert RUNG_CHIP.findall(chips) == list(rungs)
        assert overview_sections.status_chips(result).startswith(chips)


@pytest.mark.parametrize(
    "name", ["index.html", render_overview.RESULTS_PAGE, "cases/11.html", "frontier.html"]
)
def test_every_page_lists_significance_first(
    name: str, rendered: Callable[[str], str], case_pages: dict[str, str]
) -> None:
    """Wherever rungs sit side by side, on any page, they run S, V, C: a case record's
    three, and the V and C of a table's row, whose significance is a column of its own
    before them (`test_each_results_row_shows_its_rungs_significance_first`). No run
    repeats a scale or puts a later one first."""
    shown = case_pages[name] if name.startswith("cases/") else rendered(name)
    # The legend under a table of results lists every mark of a ladder in a row, by
    # design, and is no result's rungs
    # (`test_a_table_of_results_has_a_legend_of_every_rungs_mark_under_it`).
    shown = re.sub(r'<div class="site-rung-legend".*?</div>', "", shown, flags=re.DOTALL)
    runs = [run for run in _rung_runs(shown) if len(run) > 1]
    if name.startswith("cases/"):
        assert any(len(run) == len(RUNG_ORDER) for run in runs), name
    for run in runs:
        places = [RUNG_ORDER.index(label[0]) for label in run]
        assert places == sorted(set(places)), (name, run)


def test_each_results_row_shows_its_rungs_significance_first(
    page: str, results: str, overview: overview_data.Overview
) -> None:
    """A row of the results table and of Recent Results shows the result's significance
    in its own column, the second, and its V and C chips open its Rungs cell, so its
    rungs still read S, V, C across the row (`think-m3m4`)."""
    recent = {result.id for result in _recent_entries(overview)}
    assert recent
    table = _recent_table(page)

    def cell(row: str, column: str) -> str:
        """A row's cell of this class, from the end of its opening tag."""
        found = re.search(rf'<td class="{column}"[^>]*>', row)
        assert found, column
        return row[found.end() :]

    for result in overview.results:
        chips = overview_sections.ladder_chips(result)
        level = overview_sections.significance(result)
        mark = overview_sections.significance_mark(
            level, overview_sections.rung_meanings()[f"S{level}"]
        )
        rows = [_row(results, result.id)]
        if result.id in recent:
            rows.append(_recent_row(table, result.id))
        for row in rows:
            assert cell(row, "site-rungs").startswith(chips), result.id
            assert cell(row, "site-col-s").startswith(mark), result.id
            assert row.index('class="site-col-s"') < row.index('class="site-rungs"')
            assert RUNG_CHIP.findall(row) == list(overview_sections.result_rungs(result))
    for title in re.findall(
        r'<th[^>]* title="([^"]*whether a case bound[^"]*)"', page + results
    ):
        assert title.startswith("Significance, verification and confirmation, then "), title


def test_the_prose_links_repository_files_on_main(page: str) -> None:
    """Every `repo:` link in the template becomes a link on `main` to a file that exists."""
    from devtools.render_n11_lower_bounds_explainer import REPO  # noqa: PLC0415

    article = render_overview.OVERVIEW_ARTICLE.read_text(encoding="utf-8")
    paths = re.findall(r'(?:\]\(|href=")repo:([^)"\s#]+)', article)
    assert paths
    assert 'href="repo:' not in page
    for path in paths:
        assert (REPO / path).exists(), path
        assert f'href="{repo_url(path)}"' in page, path


# ---------- What the page shares with the register's views (think-o0om) ----------


@pytest.fixture(scope="module")
def overview() -> overview_data.Overview:
    return site_renders.overview()


@pytest.fixture(scope="module")
def records() -> render_recent_results.Records:
    return render_recent_results.load_records()


def _row(page: str, result_id: str) -> str:
    match = re.search(rf'<tr id="{result_id.lower()}"[^>]*>.*?</tr>', page, re.DOTALL)
    assert match, result_id
    return match.group(0)


_DIV = re.compile(r"<(/?)div\b")


def _row_popover(page: str, target: str) -> str:
    """A row's popover, from its opening tag to the `</div>` that closes it."""
    start = page.index(f'<div class="site-popover site-row-pop" id="{target}" popover')
    depth = 0
    for match in _DIV.finditer(page, start):
        depth += -1 if match.group(1) else 1
        if depth == 0:
            return page[start : match.end() + 1]
    raise AssertionError(f"{target}: its popover never closes")


def _outside_row_popovers(page: str) -> str:
    """A page's text with every row popover cut out of it, each one whole."""
    opening = '<div class="site-popover site-row-pop" id="'
    while opening in page:
        target = page[page.index(opening) + len(opening) :].split('"', 1)[0]
        page = page.replace(_row_popover(page, target), "", 1)
    return page


def test_every_result_shows_its_status_and_its_place_on_the_frontier(
    page: str,
    results: str,
    overview: overview_data.Overview,
    records: render_recent_results.Records,
) -> None:
    """A row's status line is derived, never restated. Its first chip is the status,
    which every row draws (`result_status.status`) and carries as an attribute, for the
    filter. After it comes `superseded`, on a bound that no case bound rests on now
    (`render_recent_results.superseded`), and that is all a row shows of a standing.
    That a bound is only reported is the status `recorded` and no chip of its own; a
    second proof of a held value says so by its kind; and a result that is no bound is
    marked only where its entry declares a later result that implies it
    (`superseded_by`), whatever its evidence makes its standing. Each mark names the
    results that supersede it, as links to their rows (think-6zg1), and a mark of a
    result superseded in part is the same `superseded` chip, its standing kept as
    `superseded-in-part`, with `in part` after it (think-kmi4). Every chip is the one
    plain chip (think-ai94)."""
    held = render_recent_results.HOLDS
    recent = _recent_table(page)
    status = re.compile(r'<span class="site-chip" data-status="([^"]*)"[^>]*>([^<]+)</span>')
    standing = re.compile(r'<span class="site-chip" data-standing="([^"]*)">([^<]+)</span>')
    evidence = records.register.evidence
    for result in overview.results:
        expected = render_recent_results.standing(result.record, records)
        assert result.standing == expected, result.id
        assert result.status == result_status.status(result.record, evidence), result.id
        found = render_recent_results.supersessions(result.record, expected, records)
        assert result.supersessions == tuple(found), result.id
        marks = [mark.mark for mark in found]
        assert overview_sections.is_superseded(result) is (
            render_recent_results.SUPERSEDED in marks
        ), result.id
        for row in _result_rows(results, recent, result.id):
            tag = row.split(">", 1)[0]
            assert f'data-status="{result.status}"' in tag, result.id
            assert "data-standing=" not in tag, result.id
            assert status.findall(row) == [(result.status, result.status)], result.id
            # Each mark's chip says `superseded` and carries its own standing.
            assert standing.findall(row) == [
                (overview_sections.standing_key(mark), render_recent_results.SUPERSEDED)
                for mark in marks
            ], result.id
            line = row.split('<span class="site-standing">', 1)[1]
            assert line.startswith(overview_sections.status_chip(result.status)), result.id
            # The status line is a column of its own since 2026-10-02 (think-ybt5),
            # sorted on the status word, and the rungs' cell holds no part of it.
            # As a page serves it, KPress has labelled the cell, after its own attributes.
            shown = re.escape(overview_sections.status_marks(result))
            cell = re.compile(
                rf'<td class="site-col-status" data-value="{result.status}"[^>]*>'
                rf'<span class="site-standing">{shown}</span></td>'
            )
            assert len(cell.findall(row)) == 1, result.id
            rungs = row.split('<td class="site-rungs"', 1)[1].split("</td>", 1)[0]
            assert "data-status=" not in rungs, result.id
            for word in (">current best<", ">reported<", ">second certificate<"):
                assert word not in row, (result.id, word)
    assert {result.status for result in overview.results} <= set(result_status.STATUSES)
    assert any(result.standing == held for result in overview.results)
    # A method's limit cites the bound it measures and derives `superseded`; it is no
    # bound, and declares no later result that implies it, so its row is not marked.
    by_id = {result.id: result for result in overview.results}
    assert by_id["T-003"].standing == render_recent_results.SUPERSEDED
    assert not overview_sections.is_superseded(by_id["T-003"])
    assert overview_sections.is_superseded(by_id["T-037"])
    # A superseded bound names the result its case's bound rests on now, as a link to
    # that result's row; a result of another kind that a later one implies in part
    # names it the same way, and stays current (think-6zg1, think-7df0).
    t060 = f'by <a href="{overview_sections.result_url("T-060")}">T-060</a>'
    assert t060 in _row(results, "T-037")
    assert not overview_sections.is_superseded(by_id["T-036"])
    in_part = render_recent_results.SUPERSEDED_IN_PART
    # Since 2026-10-06 T-112, the uniqueness corollary of T-060, implies its equality
    # clause, so its mark names both.
    assert by_id["T-036"].supersessions == (
        render_recent_results.Supersession(in_part, ("T-060", "T-112")),
    )
    assert t060 in _row(results, "T-036")
    # A superseding result that no replay has confirmed is named as a report, in the
    # register's words (`Supersession.words`). T-044's mark named T-082, at C1, as
    # "T-082 (reported)" until T-082's replays raised it to C3 on 6 October; since then it
    # names it as a confirmed result, and the words of a report are held on the same mark
    # with T-082 put back among the reports.
    t082 = f'<a href="{overview_sections.result_url("T-082")}">T-082</a>'
    assert t082 in _row(results, "T-044")
    assert f"{t082} (reported)" not in _row(results, "T-044")
    (mark,) = by_id["T-044"].supersessions
    shown = overview_sections.supersession_marks(by_id["T-044"])
    assert html.unescape(re.sub(r"<[^>]+>", "", shown)) == mark.words()
    reported = mark._replace(reported=frozenset({"T-082"}))
    before = dataclasses.replace(by_id["T-044"], supersessions=(reported,))
    shown = overview_sections.supersession_marks(before)
    assert f"{t082} (reported)" in shown
    assert html.unescape(re.sub(r"<[^>]+>", "", shown)) == reported.words()
    for second in ("T-054", "T-055"):
        assert by_id[second].record["kind"] == "simplification"
        assert "second certificate" not in _row(results, second), second
    for other in render_recent_results.STANDINGS:
        assert "data-tone" not in overview_sections.standing_chip(other), other
    for other in result_status.STATUSES:
        assert "data-tone" not in overview_sections.status_chip(other), other


def test_an_activity_is_a_chip_beside_the_status_and_only_where_recorded(
    overview: overview_data.Overview,
) -> None:
    """Who has the next move is drawn where the register records an `activity`, straight
    after the status: `in analysis` for work under way here, `waiting on source` for a
    request with another party, its title what is in hand and since when. A result with
    none recorded draws nothing for it."""
    for result in overview.results:
        chip = overview_sections.activity_chip(result)
        activity = result.record.get("activity")
        marks = overview_sections.status_marks(result)
        if not activity:
            assert chip == "", result.id
            assert "data-activity=" not in marks, result.id
            continue
        assert result.activity == result_status.activity_label(activity), result.id
        assert f'data-activity="{activity["state"]}"' in chip, result.id
        assert f">{html.escape(result.activity)}</span>" in chip, result.id
        assert f"Since {activity['since']}." in html.unescape(chip), result.id
        status = overview_sections.status_chip(result.status)
        assert marks.startswith(f"{status} {chip}"), result.id
    doing = overview_data.Result(
        {"activity": {"state": "in-analysis", "what": "a <b> replay", "since": "2026-09-29"}},
        group="",
        credit="",
        ours=False,
        status="recorded",
    )
    assert overview_sections.activity_chip(doing) == (
        '<span class="site-chip" data-activity="in-analysis" '
        'title="a &lt;b&gt; replay Since 2026-09-29.">in analysis</span>'
    )
    waiting = overview_data.Result(
        {
            "activity": {
                "state": "waiting",
                "party": "third-party",
                "what": "the boxes",
                "since": "2026-09-30",
            }
        },
        group="",
        credit="",
        ours=False,
        status="confirmed",
    )
    assert ">waiting on third party</span>" in overview_sections.activity_chip(waiting)


def test_every_result_shows_its_kind(
    page: str,
    results: str,
    overview: overview_data.Overview,
) -> None:
    """A result's kind is the register's `kind`, never restated: every row of both
    tables carries it as `data-kind`, for the Kind filter, and draws it as one plain
    chip in the rubric's words, on a line of its own under its rungs, the last thing in
    their cell: the status line has a column of its own since 2026-10-02 (`think-ybt5`).
    A result with no standing is of a kind that is no bound."""
    recent = _recent_table(page)
    for result in overview.results:
        kind = result.record["kind"]
        chip = overview_sections.kind_chip(result)
        label = check_results.kind_label(kind)
        assert chip == f'<span class="site-chip" data-kind="{kind}">{label}</span>'
        assert "data-tone" not in chip
        marks = overview_sections.status_marks(result)
        under = f'{overview_sections.ladder_chips(result)}<span class="site-kind">{chip}</span>'
        for row in _result_rows(results, recent, result.id):
            assert f' data-kind="{kind}" ' in row.split(">", 1)[0], result.id
            assert f">{under}</td>" in row, result.id
            assert row.count(chip) == 1, result.id
        if result.standing == render_recent_results.NO_STANDING:
            assert kind not in check_results.BOUND_KINDS, result.id
        if kind not in check_results.BOUND_KINDS:
            # Superseded only where the entry declares a later result that implies the
            # whole of it (`superseded_by`, think-nlo0).
            declared = result.record.get("superseded_by") or []
            whole = any(item["extent"] == "whole" for item in declared)
            assert overview_sections.is_superseded(result) is whole, result.id
            assert ('data-standing="superseded">' in marks) is whole, result.id
    assert ">not a bound<" not in results + recent
    assert 'data-standing="not-a-bound"' not in results + recent
    # The popover's head and a chain's step show the kind beside the rungs, then the
    # status line.
    t036 = next(result for result in overview.results if result.id == "T-036")
    assert overview_sections.status_chips(t036) == (
        f"{overview_sections.rung_chips(t036)} {overview_sections.kind_chip(t036)} "
        f"{overview_sections.status_marks(t036)}"
    )
    assert overview_sections.kind_and_status(t036) == (
        f"{overview_sections.kind_chip(t036)} {overview_sections.status_chip('confirmed')} "
        f"{overview_sections.supersession_marks(t036)}"
    )
    # Its partial mark's chip says `superseded`, as the whole mark's does, and keeps its
    # own standing; `in part` leads the quiet text after it, so the line reads as the
    # register's does, and the status column is no wider than `superseded` (think-kmi4).
    t060 = f'<a href="{overview_sections.result_url("T-060")}">T-060</a>'
    t112 = f'<a href="{overview_sections.result_url("T-112")}">T-112</a>'
    marks = overview_sections.supersession_marks(t036)
    assert marks == (
        '<span class="site-superseded"><span class="site-chip" '
        'data-standing="superseded-in-part">superseded</span> '
        f'<span class="site-cell-quiet">in part by {t060} and {t112}</span></span>'
    )
    (in_part,) = t036.supersessions
    assert html.unescape(re.sub(r"<[^>]+>", "", marks)) == in_part.words()
    from devtools import result_overview  # noqa: PLC0415

    assert ">restricted optimality</span>" in result_overview.result_popover_html(
        t036, overview
    )


def _recent_entries(overview: overview_data.Overview) -> list[overview_data.Result]:
    reference = overview_sections.reference_date(overview)
    return [
        result
        for result in overview_sections.recent_results(overview)
        if overview_sections.shown_by_default(
            result, overview_sections.RECENT_DEFAULTS, reference
        )
    ]


def _result_rows(table: str, recent: str, result_id: str) -> list[str]:
    rows = [_row(table, result_id)]
    if f'data-result="{result_id.lower()}"' in recent:
        rows.append(_recent_row(recent, result_id))
    return rows


def _recent_row(table: str, result_id: str) -> str:
    match = re.search(rf'<tr data-result="{result_id.lower()}"[^>]*>.*?</tr>', table, re.DOTALL)
    assert match, result_id
    return match.group(0)


def _recent_table(page: str) -> str:
    """The recent table as the page carries it, after kpress has wrapped it and labelled
    its cells, from its opening tag to its close."""
    match = re.search(
        r'<table class="kpress-table site-table site-results"[^>]*>'
        r".*?</table>",
        page,
        re.DOTALL,
    )
    assert match
    return match.group(0)


def test_recent_results_is_one_table_not_cards_or_a_list(
    page: str, overview: overview_data.Overview
) -> None:
    """The section is one `.site-table` of the recent results, one row each, with the
    columns every table of results has; a row links across to the results page only
    where its status names the results that supersede it, no card or list is left in
    it, and its only popovers are its rows' own. What a row's popover
    holds is the popover's own business, so the section is read without them."""
    section = page.split('id="recent-results"', 1)[1].split("<h2", 1)[0]
    recent = _recent_table(page)
    assert recent in section
    assert set(re.findall(r'<div class="(site-popover(?: [^"]*)?)"', section)) == {
        "site-popover site-row-pop"
    }
    section = _outside_row_popovers(section)
    assert "site-popover" not in section
    assert not re.search(r'class="site-card[ "]', section)
    assert "<li>" not in section
    # The recent table and no other: a reported bound is a row of it (think-d04u).
    assert section.count("<table") == 1
    assert "<details" not in section
    assert 'class="kpress-table site-table site-results"' in recent
    assert "site-recent-table" not in page
    # The script that sorts and filters the results page's table wires this one too.
    assert "data-site-table" in recent
    heads = re.findall(r"<th[^>]*>([^<]+)</th>", recent.split("</thead>", 1)[0])
    assert heads == ["Date", "S", "Result", "n", "Credit", "Rungs", "Status", "ID"]
    newest = _recent_entries(overview)
    assert re.findall(r'<tr data-result="(t-\d+)"', recent) == [r.id.lower() for r in newest]
    for result in newest:
        row = _recent_row(recent, result.id)
        # The row is the result's own here too, so nothing in it leads to its row on
        # the results page: the summary is plain, as it is there. A superseded result
        # links the rows of the results that supersede it, and only those.
        assert overview_sections.result_url(result.id) not in row, result.id
        linked = re.findall(r'href="all-results\.html#(t-\d+)"', row)
        named = {other.lower() for mark in result.supersessions for other in mark.by}
        assert set(linked) == named, result.id
        # The id, in its own cell, is the row's native trigger, which opens its popover
        # unscripted; the result's cell holds the result and no id.
        assert (
            f'<a class="site-row-open" href="result/{result.id.lower()}.html">'
            f"{result.id}</a></td>"
        ) in row
        assert row.count(f">{result.id}<") == 1
        cell = row.split('<td class="site-col-result"', 1)[1].split("</td>", 1)[0]
        assert "site-row-open" not in cell
        assert "<br" not in row
    # Evan Daniel's three exact values, the closures the exact-value cards used to show, and
    # every closure since: each is a case some row lists. Until 2026-10-02 each was its
    # row's first case; s(78) = 9, proved that day by the s(77) cover's total being below
    # 78, is the second case of T-067's row, which lists 77 and 78. Since 2026-10-02 the
    # k^2-1 and k^2-2 families count too, whose exact values rest on 2026 results (T-084,
    # T-086) that each cover a whole family rather than one case.
    exact = {n for n in overview.recent_lower if overview.cases[n]["status"] == "proved"}
    shown = {n for r in newest for n in scope_values(dict(r.record["scope"]))}
    assert exact <= shown


def test_the_recent_table_contains_the_advertised_static_subset(
    page: str, overview: overview_data.Overview
) -> None:
    """Older and superseded entries remain reachable through the complete table."""
    listed = re.findall(r'<tr data-result="(t-\d+)"', _recent_table(page))
    expected = _recent_entries(overview)
    assert listed == [result.id.lower() for result in expected]
    assert 0 < len(listed) < len(overview.results)
    section = page.split('id="recent-results"', 1)[1].split("<h2", 1)[0]
    assert "data-filter=" not in section
    assert 'href="all-results.html" data-all-results' in section
    assert "last 180 days" in _seen(section)
    assert "excluding superseded results" in _seen(section)


def test_the_html_measures_an_age_from_the_register_and_never_from_the_clock(
    overview: overview_data.Overview, register: list[dict]
) -> None:
    """The rows a render starts `hidden`, and the count beside them, are measured from
    the newest `registered` date in the register, so two renders of one tree are the
    same bytes whatever day they run on. The script measures again from the reader's
    day (`tests/node/overview_table/`), by the same reckoning: a row dated exactly the
    maximum age ago still shows."""
    reference = overview_sections.reference_date(overview)
    assert reference == max(date.fromisoformat(str(r["registered"])) for r in register)
    source = Path(overview_sections.__file__).read_text(encoding="utf-8")
    for clock in ("today()", "now()", "time.time"):
        assert clock not in source, clock
    # The same answer `overview/table.js` gives (`ageCutoff`), which its Node test pins.
    assert overview_sections.age_cutoff(date(2026, 9, 30), 180) == "2026-04-03"
    assert overview_sections.age_cutoff(date(2026, 10, 1), 0) == "2026-10-01"
    assert overview_sections.age_cutoff(date(2024, 3, 1), 1) == "2024-02-29"

    def result(
        dated: str, score: int, standing: str = "current best", kind: str = "lower-bound"
    ) -> overview_data.Result:
        record = {
            "id": "T-900",
            "kind": kind,
            "scope": {"n_values": [11]},
            "established": dated,
            "registered": "2026-09-30",
            "significance": {"score": score},
        }
        return overview_data.Result(record, group="", credit="", ours=True, standing=standing)

    shows = overview_sections.shown_by_default
    recent = overview_sections.RECENT_DEFAULTS
    every = overview_sections.RESULTS_DEFAULTS
    assert every == overview_sections.FilterDefaults(significance=None, max_age=None)
    day = date(2026, 9, 30)
    assert shows(result("2026-04-03", 3), recent, day)
    assert not shows(result("2026-04-02", 5), recent, day)
    assert not shows(result("2026-09-29", 2), recent, day)
    assert not shows(result("1979", 5), recent, day)
    # A result dated after the reference is no older than any age.
    assert shows(result("2026-10-15", 4), recent, day)
    # The same row a day later is a day older.
    assert not shows(result("2026-04-03", 4), recent, date(2026, 10, 1))
    for dated, score in (("1979", 2), ("2026-04-02", 3), ("2026-09-29", 5)):
        assert shows(result(dated, score), every, day), dated
    assert shows(result("1979", 4), overview_sections.FilterDefaults(significance=4), day)
    assert not shows(result("1979", 2), overview_sections.FilterDefaults(max_age=30), day)
    # Hide superseded hides a bound of the one standing, and keeps every other.
    hiding = overview_sections.FilterDefaults(hide_superseded=True)
    for standing in render_recent_results.STANDINGS:
        current = standing != "superseded"
        bound = result("1979", 2, standing)
        assert overview_sections.is_superseded(bound) == (not current), standing
        assert shows(bound, hiding, day) == current, standing
        assert shows(result("2026-09-29", 5, standing), recent, day) == current, standing
        assert shows(bound, every, day), standing
    # A result that is no bound is not superseded by its standing, whatever its
    # evidence gives it: no later bound supersedes the limit of a method. Only a
    # declared later result does (`superseded_by`).
    for kind in sorted(set(check_results.KINDS) - check_results.BOUND_KINDS):
        other = result("1979", 2, "superseded", kind)
        assert not overview_sections.is_superseded(other), kind
        assert shows(other, hiding, day), kind


def test_a_credit_splits_at_what_it_builds_on_and_a_standing_into_its_chips() -> None:
    # A credit is set whole, whatever the register's credit line says: the finder, then
    # what the result builds on, quiet.
    credit = overview_sections.credit_cell("wand125 after Daniel, Tokoharu, Levy, Stromquist")
    assert credit == (
        'wand125 <span class="site-cell-quiet">after Daniel, Tokoharu, Levy, Stromquist</span>'
    )
    assert overview_sections.credit_cell("Levy") == "Levy"
    assert overview_sections.credit_cell("Levy after Burns, Massaccesi") == (
        'Levy <span class="site-cell-quiet">after Burns, Massaccesi</span>'
    )
    assert overview_sections.credit_cell("A & B") == "A &amp; B"
    # Of a standing a table draws one chip, `superseded`, the plain one; the partial
    # mark's says the same word and keeps its own standing (think-kmi4).
    assert overview_sections.standing_chip("superseded") == (
        '<span class="site-chip" data-standing="superseded">superseded</span>'
    )
    assert overview_sections.standing_chip("superseded in part", "superseded") == (
        '<span class="site-chip" data-standing="superseded-in-part">superseded</span>'
    )
    assert not hasattr(overview_sections, "standing_chips")


def test_only_t060_of_the_s5_results_still_holds(overview: overview_data.Overview) -> None:
    s5 = [r for r in overview.results if r.record["significance"]["score"] >= 5]
    holding = {r.id for r in s5 if r.standing == render_recent_results.HOLDS}
    # The audit's reading of the record; update it when the record moves on. T-060's
    # exact n = 11 value superseded T-037's 31/8.
    assert holding == {"T-060"}


def test_recent_results_has_no_lead_line(page: str) -> None:
    """Nothing stands between the section's heading and its filter bar, since its prose
    follows the table (think-tgjv): the generated "Lead result" line the owner dropped
    on 2026-10-01 is gone, from the page, the template and the module that wrote it."""
    section = page.split('id="recent-results"', 1)[1].split("<h2", 1)[0]
    assert "site-recent-lead" not in section
    assert "Lead result" not in section
    assert 'class="site-recent-scope"' in section
    assert "data-filter=" not in section
    template = render_overview.OVERVIEW_ARTICLE.read_text(encoding="utf-8")
    assert "RECENT_LEAD" not in template
    assert not hasattr(overview_sections, "recent_lead")
    assert not hasattr(overview_sections, "lead_result")


def _shared(page: str, name: str) -> str:
    """One shared block of README as the overview renders it: the run between its
    markers."""
    from devtools import site_documents  # noqa: PLC0415

    (block,) = (b for b in site_documents.SHARED_BLOCKS if b.name == name)
    assert page.count(block.opened) == page.count(block.closed) == 1
    return page.split(block.opened, 1)[1].split(block.closed, 1)[0]


def _intro(page: str) -> str:
    """README's two opening paragraphs as the overview's first section renders them."""
    return _shared(page, "project-intro")


def _recent_prose(page: str) -> str:
    """Recent Results' paragraph, the markup under its table's action, the comments
    after it set aside."""
    section = page.split('id="recent-results"', 1)[1].split("<h2", 1)[0]
    after = section.split('<p class="site-action-row site-more">', 1)[1].split("</p>", 1)[1]
    return re.sub(r"<!--.*?-->", "", after, flags=re.DOTALL).strip()


#: One formula as kpress writes it: the TeX for KaTeX, then its MathML.
_KPRESS_MATH = re.compile(
    r'<span class="kpress-math [^>]*><span class="kpress-math-render"[^>]*>'
    r"\\\((.*?)\\\)</span>.*?</math></span></span>",
    re.DOTALL,
)


def _rendered_text(markup: str) -> str:
    """Rendered prose as its words, with each formula's semantic source once."""

    class Prose(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.words: list[str] = []
            self.formula: list[str] = []
            self.math_depth = 0
            self.semantic_depth = 0

        def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
            found = dict(attrs)
            if tag == "span" and "kpress-math" in (found.get("class") or "").split():
                self.math_depth = 1
                self.formula = []
            elif tag == "span" and self.math_depth:
                self.math_depth += 1
            if tag == "span" and "kpress-math-semantic" in (found.get("class") or "").split():
                self.semantic_depth = self.math_depth

        def handle_endtag(self, tag: str) -> None:
            if tag == "span" and self.math_depth:
                if self.semantic_depth == self.math_depth:
                    self.semantic_depth = 0
                self.math_depth -= 1
                if not self.math_depth:
                    self.words.append("$" + "".join(self.formula) + "$")

        def handle_data(self, data: str) -> None:
            if self.semantic_depth:
                self.formula.append(data)
            elif not self.math_depth:
                self.words.append(data)

    parser = Prose()
    parser.feed(markup)
    return " ".join("".join(parser.words).split())


def _markdown_text(markdown: str) -> str:
    """Markdown's prose and formula semantics, comparable with prepared HTML."""
    from kpress.format.markdown import parse_markdown  # noqa: PLC0415

    return _rendered_text(parse_markdown(markdown, title="Expected prose").html)


def _template_paragraphs(section: str) -> list[str]:
    """A section of the overview's template after its heading, as its paragraphs."""
    prose = re.sub(r"<!--.*?-->", "", section, flags=re.DOTALL)
    return [" ".join(part.split()) for part in prose.split("\n\n") if part.strip()]


#: README's `project-intro` block, the owner's words of 2026-10-03 (`think-8lyq`): the
#: question after a colon, the lower bound glossed as a size below which no packing can
#: exist, and an example of each bound at $n = 29$, the case's current bounds as the
#: record reports them (the owner, 2026-10-03: "make the examples current"), each
#: written as the record writes it, with $\le$ and $\ge$. The lower is called reported,
#: the field `test_the_intros_examples_are_the_records` compares it with: when this was
#: written wand125's certificate was not yet replayed here and stood at V0/C0, so "proved"
#: alone would have put a reported bound in a verified one's place. Its 6 October
#: certificate (T-108) is replayed here at V3/C3, so both lanes now hold 5.81, and the
#: word stays the owner's.
PROBLEM_STATEMENT = (
    (
        "The square packing problem is a simple and long-standing problem in geometry: "
        "what is the size of the smallest square that can hold $n$ unit squares, where "
        "the squares are free to rotate but cannot overlap? The side length of that "
        "smallest square is written $s(n)$."
    ),
    (
        "The question of the value of $s(n)$ is simple, but the answer is an open problem "
        "for most $n$. In many cases, $s(n)$ is known only to lie between an upper bound "
        "(the size of the enclosing square for the tightest packing ever discovered, such "
        "as $s(29) \\le 5.934$) and a lower bound (a size below which it is proved that no "
        "packing can exist, such as the reported $s(29) \\ge 5.81$)."
    ),
)


def test_the_intros_examples_are_the_records() -> None:
    """The introduction's two examples are case 29's current bounds: its lower example
    is the reported lower bound, wand125's 5.79 of 2026-09-28 when this was written,
    its 2319/400 = 5.7975 of 1 October (T-074) after it, and its 581/100 = 5.81 of 6
    October (T-108) since, and its upper example is the reported upper bound rounded
    up, which also stands at or above the verified ceiling, so it is itself a proved
    ceiling. A new bound at $n = 29$ that leaves an example stale fails here rather
    than on the page."""
    from devtools import overview_data, site_documents  # noqa: PLC0415

    block = site_documents.intro_block(site_documents.README.read_text(encoding="utf-8"))
    upper = Decimal(re.findall(r"\$s\(29\) \\le ([\d.]+)\$", block)[0])
    lower = Decimal(re.findall(r"\$s\(29\) \\ge ([\d.]+)\$", block)[0])
    case = overview_data.load().cases[29]
    reported_upper = Decimal(case["reported_upper_bound"]["value"])
    ceiling = Decimal(case["verified_upper_bound"]["value"])
    assert max(reported_upper, ceiling) <= upper < reported_upper + Decimal("0.001")
    assert lower == Decimal(case["reported_lower_bound"]["value"])


def test_the_overviews_first_section_is_readmes_one_block(page: str) -> None:
    """The overview says what README's opening says, word for word and formula for
    formula, in one place: the first section opens with README's `project-intro` block,
    the problem and its bounds, which names $s(n)$ and writes it thrice. README's next
    two paragraphs, what the project covers and its newest major result, were a second
    shared block that opened Recent Results until 2026-10-02; they are README's own
    since, unmarked, and no other block is shared. The template holds a placeholder
    where the block goes, names no registered result of its own in the first section,
    and opens Recent Results with a paragraph of its own."""
    from devtools import site_documents  # noqa: PLC0415

    readme = site_documents.README.read_text(encoding="utf-8")
    blocks = site_documents.shared_blocks(readme)
    assert list(blocks) == ["project-intro"]
    assert site_documents.SHARED_BLOCKS == (site_documents.INTRO,)
    assert blocks["project-intro"] == site_documents.intro_block(readme)
    assert _rendered_text(_intro(page)) == _markdown_text(blocks["project-intro"])
    assert len(re.findall(r"<p>", _intro(page))) == 2
    problem, bounds = (
        _markdown_text(paragraph) for paragraph in blocks["project-intro"].split("\n\n")
    )
    assert problem == _markdown_text(PROBLEM_STATEMENT[0])
    assert bounds == _markdown_text(PROBLEM_STATEMENT[1])
    assert blocks["project-intro"].count("$s(n)$") == 3
    assert not re.search(r"^#", blocks["project-intro"], re.MULTILINE)
    assert "<!--" not in blocks["project-intro"]
    # README keeps its account of recent progress, unmarked, right after the block.
    assert "recent-progress" not in readme
    after_block = readme.split(site_documents.INTRO.end, 1)[1]
    assert after_block.lstrip().startswith("The project covers the problem at every $n$.")
    assert "A recent major result settles eleven squares" in after_block
    assert "README recent-progress" not in page

    template = render_overview.OVERVIEW_ARTICLE.read_text(encoding="utf-8")
    section = template.split('id="the-problem"', 1)[1].split("{{PAGE_CARDS}}", 1)[0]
    paragraphs = _template_paragraphs(section.split("</h1>", 1)[1])
    assert paragraphs[0] == "{{README_INTRO}}"
    own = " ".join(paragraphs[1:])
    assert not re.search(r"\bT-\d{3}\b", own)
    assert "eleven" not in own.lower()
    recent = template.split("## Recent Results", 1)[1].split("\n## ", 1)[0]
    assert "README_PROGRESS" not in template
    # The table and its action come first since 2026-10-02 (think-tgjv), then the prose.
    prose = [part for part in _template_paragraphs(recent) if not part.startswith(("{{", "<p"))]
    assert prose[0].startswith("Eleven squares is settled:")


def test_recent_results_opens_with_its_table_and_says_what_it_shows_under_it(
    page: str,
) -> None:
    """Recent Results opens with its table, its legend under it, and under the table's one
    action stands one short paragraph (the owner, 2026-10-02, `think-tgjv`; one
    paragraph stood between the heading and the filter bar until then): the headline of
    recent progress and where the filters start. The paragraph on what the ratings mean,
    the star's sentence and the key of every rung went on 2026-10-03 (`think-42dx`): the
    legend shows every mark, and the Results page explains them. What stood there before
    2026-10-02, README's two paragraphs and a paragraph on the table, is gone from the
    page: the rungs, review, packet and defects of T-060 are its row's, and the kinds and
    statuses the Results page's."""
    problem = page.split('id="the-problem"', 1)[1].split('id="recent-results"', 1)[0]
    section = page.split('id="recent-results"', 1)[1].split("<h2", 1)[0]
    head = section.split("</h2>", 1)[1]
    # The table first: nothing a reader sees stands between the heading and its bar,
    # which opens the table's wide block.
    before = re.sub(
        r"<!--.*?-->", "", head.split('<p class="site-recent-scope"', 1)[0], flags=re.DOTALL
    )
    assert before.strip() == '<div class="site-wide">'
    lead = _recent_prose(page)
    paragraphs = re.findall(r"<p>(.*?)</p>", lead, re.DOTALL)
    assert len(paragraphs) == 1
    first = _rendered_text(paragraphs[0])
    assert first.startswith(
        _markdown_text("Eleven squares is settled: $s(11) = 3.8770835\\ldots$")
    )
    assert first.endswith("The complete table includes older results and offers all filters.")
    assert 40 <= len(first.split()) <= 100, len(first.split())
    for gone in ("Each row carries three ratings", "marks a new result", "S1 to S5"):
        assert gone not in _seen(section), gone
    assert "site-ladders" not in section
    # The bar, the table, the legend, its action, then the paragraph.
    order = [
        section.index('<p class="site-recent-scope"'),
        section.index(_recent_table(page)),
        section.index('<div class="site-rung-legend"'),
        section.index('<p class="site-action-row site-more">'),
        section.index(lead),
    ]
    assert order == sorted(order)
    text = first
    # The section's prose is the lead; its bar and rows name sources and credits of
    # their own (Guzhou0806 is a Source option, Kleddamag a credit), so they are read
    # out of the lead and the sections before it only.
    for gone in (
        "The project covers the problem at every",
        "settles eleven squares",
        "V3/C3/S5",
        "retained packet",
        "reproducibility defects",
        "clear Hide superseded",
        "The table lists every result",
        "results register",
        "Guzhou0806",
        "Kleddamag",
    ):
        assert gone not in text, gone
        # Part II's card, above, names the proof it reviews by its author.
        if gone != "Kleddamag":
            assert gone not in _rendered_text(problem), gone
    for gone in ("The project covers the problem at every", "retained packet", "clear Hide"):
        assert gone not in _rendered_text(section), gone
    assert "These are the recent results this project tracks" not in _rendered_text(section)
    for defined_there in ("reviewed", "incomplete", "replayed here in full"):
        assert defined_there not in text, defined_there
    assert "epistemics" not in lead


def test_recent_results_names_the_headline_results_at_their_rows(
    page: str, results: str, case_pages: dict[str, str]
) -> None:
    """The paragraph names the results that settle eleven squares, bracket seventeen and
    give the new exact values, each id at its row on the Results page and each case at
    its record, and the template is in the reader tier, so the gate refuses a result
    it names that the register does not hold. README is held the same way for its own
    account."""
    from devtools import check_results, site_documents  # noqa: PLC0415

    lead = _recent_prose(page)
    text = _rendered_text(lead)
    assert "the exact side of Trump\u2019s 1979 packing" in text
    assert "Seventeen squares is bracketed by machine-checked bounds, T-093 below" in text
    assert "new exact values" in text
    for result in ("t-060", "t-093", "t-065"):
        assert f'<a href="all-results.html#{result}">{result.upper()}</a>' in lead, result
        assert f'id="{result}"' in results, result
    assert re.findall(r"\bT-\d{3}\b", text) == ["T-060", "T-093", "T-065"]
    records = case_pages
    for n in (21, 32, 45):
        assert f'<a href="{render_case_pages.case_url(n)}" data-case="{n}">' in lead, n
        assert render_case_pages.case_url(n) in records, n
    hrefs = re.findall(r'href="([^"]+)"', lead)
    for href in hrefs:
        page_name = href.partition("#")[0]
        assert page_name in render_overview.SITE_PAGES or page_name in records, href
    assert site_documents.README in check_results.READER_TIER
    assert render_overview.OVERVIEW_ARTICLE in check_results.READER_TIER
    template = render_overview.OVERVIEW_ARTICLE.read_text(encoding="utf-8")
    for result in ("T-060", "T-093", "T-065"):
        assert result in template, result
    # The register's own values, as the rows state them: the exact values the
    # paragraph says are new, and the eleven-square side it writes.
    by_id = {r.id: r for r in overview_data.load().results}
    assert by_id["T-060"].record["kind"] == "optimality"
    assert [by_id[t].record["scope"]["n_values"] for t in ("T-093", "T-065")] == [[17], [17]]
    assert by_id["T-093"].record["kind"] == "lower-bound"
    assert by_id["T-065"].record["kind"] == "upper-bound"
    assert "3.8770835" in by_id["T-060"].record["claim"]
    exact = {
        r.first_n
        for r in overview_data.load().results
        if r.record["kind"] == "optimality" and r.first_n in (21, 32, 45)
    }
    assert exact == {21, 32, 45}


#: The site's own statement, the owner's words of 2026-10-03 (`think-a7oa`), with the
#: name the owner left blank filled from the register (T-060 is Queuingtheorydotcom's),
#: the project's start put as the record has it (its explorations obtained the lower
#: bounds, from 2026-08-31, after it began on 2026-08-22), and one phrase narrowed to
#: what the register holds: the project tabulates every known new result and verifies
#: the proofs behind them, without claiming every one is checked, since some registered
#: results are recorded and not yet replayed here. The sentence after Queuingtheorydotcom's
#: is the owner's of the same day (`think-nlyc`): the top-line results by others, Evan
#: Daniel's family T-064 and his exact values T-052, T-051 and T-053, in a sentence of
#: their own because the bibliography files them as independent of this project, and
#: without a significance score, since they are S4 and only n = 11's results are S5.
SITE_STATEMENT = (
    (
        "Work on the square packing problem has exploded in the summer of 2026 thanks to "
        "AI-powered research efforts. This Squares Project was begun by Joshua Levy in "
        "August 2026 with some initial explorations that obtained new lower bounds for "
        "$n = 11, 17, 18, 19, 20$ and other low values. Now several others have obtained "
        "results building on this work, including Kleddamag"
        "\N{RIGHT SINGLE QUOTATION MARK}s certified lower bound of 31/8 and a landmark "
        "new proof by Queuingtheorydotcom of the optimality of the famous case of 11 "
        "squares. "
        "Separately, Evan Daniel has proved the optimality of a whole infinite family, "
        "$s(k^2 - 3) = k$ for every $k \\ge 6$, along with exact values at 21, 32 and 45 "
        "squares. This project now independently tabulates all known new results and "
        "does AI-assisted verification of the proofs and certificates behind them, to "
        "encourage open collaboration on open questions and formalizations of current "
        "proofs."
    ),
    (
        "If you have new results or know of newer results, please file an issue to "
        "report them, and we will gladly incorporate them and cite your work. We also "
        "have a group chat. Contact ojoshe if you wish to join."
    ),
)


def test_the_sites_own_statement_follows_readmes_introduction(
    page: str, results: str, case_pages: dict[str, str]
) -> None:
    """After README's introduction the section has two paragraphs of its own (the
    owner, 2026-10-03): how the project began and what it does now, and where to
    report a result it lacks and how to join its chat. The first links the project's
    founder, the explainer that holds its first lower bounds (Part I), Parts II and
    III of the series at Kleddamag's bound and the optimality proof, the case record of
    $n = 11$, Evan Daniel's family $s(k^2 - 3) = k$ at its row on the Results page and
    his exact values at the case records of 21, 32 and 45, and the ladders that show how
    far each result is checked, and does not claim every proof is; the second opens a
    new issue on the repository and links the founder's account on X. Each result the
    first names is the register's, with the credit it gives: T-060 Queuingtheorydotcom's
    and building on this project, T-064, T-052, T-051 and T-053 Daniel's and independent
    of it, which is why his results stand in a sentence of their own; each is an
    optimality result at V3/C3 or above, so "proved" holds. No significance score is
    named, since only n = 11's results are S5 (the owner, 2026-10-03, think-nlyc)."""
    from devtools import site_documents  # noqa: PLC0415

    problem = page.split('id="the-problem"', 1)[1].split('id="recent-results"', 1)[0]
    own = problem.split(site_documents.OVERVIEW_INTRO_CLOSE, 1)[1].split("<div", 1)[0]
    paragraphs = re.findall(r"<p>(.*?)</p>", own, re.DOTALL)
    assert [_rendered_text(paragraph) for paragraph in paragraphs] == [
        _markdown_text(text) for text in SITE_STATEMENT
    ]
    # An external link opens in a new tab, so its anchor carries more than its address.
    founder = '<a href="https://x.com/ojoshe" target="_blank" rel="noopener noreferrer">'
    for link in (
        f"{founder}Joshua Levy</a>",
        '<a href="papers/n11-lower-bounds-explainer.html">new lower bounds</a>',
        '<a href="papers/n11-threshold-bound-review.html">certified lower bound of 31/8</a>',
        '<a href="papers/n11-optimality-review.html">landmark new proof</a>',
        f'<a href="{render_case_pages.case_url(11)}" data-case="11">case of 11 squares</a>',
        '<a href="all-results.html#t-064">a whole infinite family</a>',
        *(
            f'<a href="{render_case_pages.case_url(n)}" data-case="{n}">{n}</a>'
            for n in (21, 32, 45)
        ),
        '<a href="all-results.html#verification-ladders">AI-assisted verification</a>',
    ):
        assert link in paragraphs[0], link
    # Every link lands: a case at its record, a result at its row on the Results page.
    for n in (11, 21, 32, 45):
        assert render_case_pages.case_url(n) in case_pages, n
    assert 'id="t-064"' in results
    # The register's own facts, as the sentences state them.
    by_id = {r.id: r for r in overview_data.load().results}
    groups = dict(OTHERS)
    assert by_id["T-060"].credit.startswith("Queuingtheorydotcom after Levy")
    assert by_id["T-060"].group == groups["builds-on-project"]
    assert by_id["T-037"].credit.startswith("Kleddamag")
    assert by_id["T-037"].group == groups["builds-on-project"]
    exact = {"T-064": None, "T-052": [21], "T-051": [32], "T-053": [45]}
    for result, n_values in exact.items():
        record = by_id[result].record
        assert by_id[result].credit.startswith("Daniel"), result
        assert by_id[result].group == groups["independent"], result
        assert record["kind"] == "optimality", result
        assert int(record["verification"][1:]) >= 3, result
        assert int(record["confirmation"][1:]) >= 3, result
        assert n_values is None or record["scope"]["n_values"] == n_values, result
    assert "s(k^2 - 3) = k for every integer k >= 6" in by_id["T-064"].record["claim"]
    assert "Evan Daniel" in by_id["T-064"].record["claim"]
    for score in ("S4", "S5"):
        assert score not in " ".join(SITE_STATEMENT), score
    assert "all proofs" not in " ".join(SITE_STATEMENT)
    assert 'id="verification-ladders"' not in page
    assert render_overview.NEW_ISSUE_URL == "https://github.com/jlevy/squares/issues/new"
    assert re.search(
        rf'<a href="{re.escape(render_overview.NEW_ISSUE_URL)}"[^>]*>file an issue</a>',
        paragraphs[1],
    )
    assert f"{founder}ojoshe</a>" in paragraphs[1]
    # Formal proofs are invited, not claimed.
    assert "formally" not in " ".join(SITE_STATEMENT).lower()


def test_the_sites_statement_stands_under_its_own_section_heading(page: str) -> None:
    """README's two paragraphs stay under the page's first heading, and the site's own
    statement has a section heading of its own, The Squares Project: an ordinary
    `h2` with its own id and its entry in the page's contents, directly after README's
    block and directly above the paragraph on how the project began. It is no
    page title, so it takes the two section spaces every `h2` takes
    (`test_section_headings_share_one_space_above_and_one_below`)."""
    from devtools import site_documents  # noqa: PLC0415

    heading = '<h2 id="the-squares-project">The Squares Project</h2>'
    assert page.count(heading) == 1
    problem = page.split('id="the-problem"', 1)[1].split('id="recent-results"', 1)[0]
    after_intro = problem.split(site_documents.OVERVIEW_INTRO_CLOSE, 1)[1]
    assert after_intro.lstrip().startswith(heading)
    following = after_intro.split(heading, 1)[1].lstrip()
    assert following.startswith("<p>Work on the square packing problem")
    assert heading not in problem.split(site_documents.OVERVIEW_INTRO_CLOSE, 1)[0]
    template = render_overview.OVERVIEW_ARTICLE.read_text(encoding="utf-8")
    assert (
        "{{README_INTRO}}\n\n## The Squares Project\n\nWork on the square packing "
        "problem" in template
    )


def test_the_project_is_named_the_squares_project_wherever_it_is_named(
    page: str, rendered: Callable[[str], str]
) -> None:
    """The project's formal name is The Squares Project (the owner, 2026-10-01, in place
    of The Square Packing Project of earlier that day), and no page of the site calls it
    anything else in its own words: the README's title and its card, the closing
    section's heading, which carries its own fragment, and the sentence under it. Other
    Square Packing Projects, the plural, names other people's projects, and The Square
    Packing Problem the subject; neither is this project's name."""
    from devtools import site_documents  # noqa: PLC0415

    heading = '<h2 id="squares-project-documentation">Squares Project Documentation</h2>'
    assert page.count(heading) == 1
    section = page.split(heading, 1)[1]
    assert "live in the Squares Project\u2019s" in _rendered_text(section)
    readme = site_documents.README.read_text(encoding="utf-8")
    assert readme.startswith("# The Squares Project\n")
    # README's page is named for the file in its tab, since the project's name follows
    # it there as it does every page's name, and the overview's title is that name alone.
    assert "<title>README · The Squares Project</title>" in rendered("readme.html")
    assert (
        "<title>Square Packing: Bounds, Results and Best Packings · The Squares Project</title>"
        in page
    )
    labels = [label for _, label, _ in overview_sections.DOCUMENTS]
    assert labels[0] == "The Squares Project"
    for name in ("index.html", "papers.html", "frontier.html", "readme.html", "visualize.html"):
        text = re.sub(r"<(script|style)\b.*?</\1>", "", rendered(name), flags=re.DOTALL)
        text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
        assert not re.search(r"square packing project(?!s)", text, flags=re.IGNORECASE), name


def _the_central_case() -> re.Pattern[str]:
    """The framing the owner refused on 2026-09-30, as `site_documents` holds README's
    shared blocks to it: eleven squares is a central case, never the central one."""
    from devtools import site_documents  # noqa: PLC0415

    return site_documents.THE_CENTRAL_CASE


@pytest.mark.parametrize(
    "path",
    [
        render_overview.REPO / "README.md",
        render_overview.OVERVIEW_ARTICLE,
        render_overview.TEMPLATES / "paper-design.md",
        render_overview.PACKING / "devtools" / "render_overview.py",
    ],
    ids=lambda path: path.name,
)
def test_no_case_is_called_the_central_one(path: Path) -> None:
    """The project covers square packing at every n. "A central case" may be said of
    eleven squares; "the central case", "its central case" and "the central open case"
    may not, in README, the overview's template, the design notes or this renderer."""
    pattern = _the_central_case()
    found = pattern.findall(path.read_text(encoding="utf-8"))
    assert not found, f"{path.name}: {found}"
    assert not pattern.search("a central case, and a central open case")
    for phrase in ("the central case", "Its central\ncase", "the central open case"):
        assert pattern.search(phrase), phrase


def card_text(fragment: str) -> str:
    """A card's semantic text, with mathematical operators in the source's notation."""
    text = _rendered_text(fragment).replace("$", "")
    text = re.sub(r"\s*([=<>])\s*", r" \1 ", text)
    return text.replace("≥", r" \ge ").replace("≤", r" \le ").replace("…", r"\ldots")


EXPLAINER_TITLE = "New lower bounds for square packing for n = 11"
EXPLAINER_NOTE = (
    "How weighted points and 2-of-3 threshold atoms prove T-018, T-025 and T-026, "
    "s(11) \\ge 3.8264\\ldots, with interactive figures."
)


def papers_article(papers: str) -> str:
    """The Papers page's article: its introduction and its cards."""
    return papers.split("<article", 1)[1].split("</article>", 1)[0]


def test_the_explainer_card_says_what_the_explainer_now_is(
    page: str, results: str, rendered: Callable[[str], str]
) -> None:
    """The explainer proves the earlier, simpler lower bounds, so its card is titled as
    the owner put it and described in the series plan's line for Part I, `n = 11` and
    the bound set as math. On the overview and on the Papers page the card is the link to
    the explainer, so it holds no other; T-060, the optimality proof since registered, is
    linked from the Papers page's introduction. The wording stays within T-060's rungs:
    proved, never formally."""
    value, note = _page_card_parts(page, overview_sections.LOWER_BOUNDS_PAPER)
    article = papers_article(rendered("papers.html"))
    assert card_text(value) == EXPLAINER_TITLE
    assert card_text(note) == EXPLAINER_NOTE
    assert "kpress-math" in value
    assert "kpress-math" in note
    assert "formal" not in card_text(value + note).lower()
    assert '<a href="all-results.html#t-060">T-060</a>' in article
    assert 'id="t-060"' in results


#: What a popover card and its popover are made of, none of which the Papers page's
#: article holds: its cards are plain same-tab links.
POPOVER_MARKUP = (
    "pop-paper-",
    "popovertarget",
    " popover",
    "site-popover",
    "<iframe",
    "view=embed",
    "<button",
    'target="_blank"',
)


def test_the_papers_page_holds_one_large_card_for_each_paper(
    rendered: Callable[[str], str], served: Callable[[str], str]
) -> None:
    """`papers.html` is one large card per paper and nothing else in cards, in the order of
    the one list that defines them (`overview_sections.PAPERS`), so a new paper is one
    entry there. A paper is a full page the site serves, so its card is the link itself
    and goes there in the same tab, as the overview's page cards do: an `<a href>` with
    the page icon (`data-go="page"`), no popover, no framed preview and no new tab.
    The page has no popover, so it carries no popover script."""
    page = rendered("papers.html")
    papers = overview_sections.PAPERS
    assert [paper.href for paper in papers] == [
        "papers/n11-lower-bounds-explainer.html",
        "papers/n11-threshold-bound-review.html",
        "papers/n11-optimality-review.html",
        "papers/square-packing-methods-survey.html",
        "tutorial.html",
    ]
    assert [paper.label for paper in papers] == [
        "Part I",
        "Part II",
        "Part III",
        "Methods tutorial",
        "Tutorial",
    ]
    assert [paper.href for paper in papers[:-1]] == [
        render_overview.paper_path(record.slug) for record in render_overview.PAPERS
    ]
    assert {paper.size for paper in papers} == {"large"}
    cards = _page_cards(page)
    assert [href for href, _, _ in cards] == [paper.href for paper in papers]
    assert len(re.findall(r'class="site-card[ "]', page)) == len(cards)
    for (href, tag, body), paper in zip(cards, papers, strict=True):
        assert href in render_overview.SITE_PAGES, href
        assert tag == ' data-go="page" data-card-size="large"', href
        assert f'<span class="site-card-label">{paper.label}</span>' in body, href
        value, note = _page_card_parts(page, href)
        assert card_text(value) == paper.title, href
        # A formula in a description reads here as its TeX, so its opening words are held.
        assert card_text(note).startswith(paper.description[:32]), href
    article = papers_article(page)
    for markup in POPOVER_MARKUP:
        assert markup not in article, markup
    popover = render_overview.POPOVER_SCRIPT.read_text(encoding="utf-8")
    assert popover not in served("papers.html")


def test_a_papers_card_holds_no_link_so_the_introduction_links_what_it_names(
    rendered: Callable[[str], str],
) -> None:
    """A paper's card is the link to its paper, and a link holds no other. What the
    descriptions name, the three parts of the series and the rows of T-037 and T-060, is
    linked from the page's introduction instead, above the cards. A paper's entry is its
    address, label, title, description and size, with no links of its own."""
    assert overview_sections.Paper._fields == (
        "href",
        "label",
        "title",
        "description",
        "size",
    )
    explainer = overview_sections.EXPLAINER
    assert explainer is overview_sections.PAPERS[0]
    assert explainer.href == overview_sections.LOWER_BOUNDS_PAPER
    assert overview_sections.THRESHOLD_REVIEW is overview_sections.PAPERS[1]
    article = papers_article(rendered("papers.html"))
    introduction, cards = article.split('<div class="site-cards-frame', 1)
    assert re.findall(r'<a href="([^"]+)">([^<]+)</a>', introduction) == [
        (overview_sections.LOWER_BOUNDS_PAPER, "Part I"),
        (overview_sections.THRESHOLD_BOUND_PAPER, "Part II"),
        ("all-results.html#t-037", "T-037"),
        (overview_sections.OPTIMALITY_PAPER, "Part III"),
        ("all-results.html#t-060", "T-060"),
        ("tutorial.html", "square-packing tutorial"),
        ("papers/square-packing-methods-survey.html", "How Record Square Packings Are Found"),
    ]
    for body in re.findall(r"<a\b[^>]*>(.*?)</a>", cards, re.DOTALL):
        assert "<a" not in body


def test_the_papers_page_says_what_each_paper_is(
    page: str, rendered: Callable[[str], str]
) -> None:
    """The explainer's card is its card on the overview, word for word; the tutorial's is
    `TUTORIAL.md`'s own opening, whom it is for and what it covers. The overview keeps a
    card for the explainer and the tutorial."""
    papers = rendered("papers.html")
    explainer = overview_sections.LOWER_BOUNDS_PAPER
    value, note = _page_card_parts(papers, explainer)
    assert card_text(value) == EXPLAINER_TITLE
    assert card_text(note) == EXPLAINER_NOTE
    assert (value, note) == _page_card_parts(page, explainer)

    value, note = _page_card_parts(papers, "tutorial.html")
    assert card_text(value) == "Square packing from first principles"
    opening = (overview_data.REPO / "TUTORIAL.md").read_text(encoding="utf-8")
    opening = " ".join(opening.split("## Contents", 1)[0].split())
    assert "Square Packing from First Principles" in opening
    assert "anyone new to the problem" in card_text(note)
    for phrase in (
        "what the objects are",
        "why the approach is shaped the way it is",
        "what the research has and has not established",
        "linear programming",
        "is first needed",
    ):
        assert phrase in card_text(note), phrase
        assert phrase in opening, phrase
    assert {explainer, "tutorial.html"} <= {href for href, _, _ in _page_cards(page)}


def test_the_optimality_papers_card_says_what_t060s_rungs_allow(
    register: list[dict], rendered: Callable[[str], str]
) -> None:
    """The optimality paper is Part III, the third card: served where its renderer writes
    it, titled as its renderer titles it, in sentence case, and described as explaining
    the proof of T-060 in the words T-060's rungs allow, V3 and C3: a proof, never a
    formal one. The card is the link to the paper, in the same tab."""
    from devtools import render_n11_optimality_review as renderer  # noqa: PLC0415

    paper = overview_sections.PAPERS[2]
    assert paper.href == overview_sections.OPTIMALITY_PAPER == renderer.SITE_PATH
    assert paper.href in render_overview.SITE_PAGES
    assert paper.title.lower() == renderer.TITLE.lower()
    assert paper.title == "A review of the optimality proof of the Trump packing of 11 squares"
    papers = rendered("papers.html")
    assert _page_cards(papers)[2][0] == paper.href
    value, note = _page_card_parts(papers, paper.href)
    assert card_text(value) == paper.title
    text = card_text(note)
    assert text.startswith(
        "Explains Queuingtheorydotcom\u2019s proof that Trump\u2019s packing"
    )
    assert "(T-060)" in text
    assert "is optimal" in text
    assert "s(11) = 3.8770835" in text
    assert "kpress-math" in note
    assert "formal" not in text.lower()
    t060 = next(r for r in register if r["id"] == "T-060")
    assert (t060["verification"], t060["confirmation"]) == ("V3", "C3")


def test_the_papers_page_introduces_the_papers_within_t060s_rungs(
    register: list[dict], rendered: Callable[[str], str]
) -> None:
    """The introduction presents the three parts of the n = 11 series in reading order,
    each linked, and names T-060 with a link to its row, in the words its rungs allow,
    V3 and C3: proved optimal, machine-checked and reviewed with its review record
    pending, never formally. It keeps T-060's standing in one sentence: T-060 settles
    the case, and Part III explains it (the series plan, Owner Decisions). Its template
    is in the reader tier, so the gate refuses a result it names that the register does
    not hold."""
    from devtools import check_results  # noqa: PLC0415

    article = papers_article(rendered("papers.html"))
    text = card_text(article)
    assert re.search(r"<h1\b[^>]*>Papers</h1>", article)
    assert '<a href="all-results.html#t-060">T-060</a>' in article
    assert f'<a href="{overview_sections.OPTIMALITY_PAPER}">Part III</a>' in article
    assert "proved optimal" in text
    assert "machine-checked and reviewed here" in text
    assert "review record pending" in text
    assert "one series on n = 11, read in order" in " ".join(text.split())
    assert "T-060 settles the case; Part III explains it." in " ".join(text.split())
    assert "formal" not in text.lower()
    t060 = next(r for r in register if r["id"] == "T-060")
    assert (t060["verification"], t060["confirmation"]) == ("V3", "C3")
    assert render_overview.PAPERS_ARTICLE in check_results.READER_TIER
    assert render_overview.PAPERS_ARTICLE in render_overview.RENDER_INPUTS


def test_the_film_note_says_the_films_predate_t060(
    register: list[dict], rendered: Callable[[str], str]
) -> None:
    """The films were cut before T-060, so the film page says what they show at n = 11,
    dated from the release; a film cut after T-060 fails here until the note goes."""
    from datetime import datetime  # noqa: PLC0415

    from sqpack.release import PUBLICATION_HISTORY  # noqa: PLC0415

    page = rendered("visualize.html")
    assert render_overview.film_release_date() == "28 September"
    text = re.sub(r"<[^>]+>", "", page)
    assert (
        "Both predate T-060, so at n = 11 they show the lower bound of 28 September, "
        "not the proved value." in text
    )
    assert '<a href="all-results.html#t-060">T-060</a>' in page
    release = next(e for e in PUBLICATION_HISTORY if e.version == render_overview.FILM_RELEASE)
    released = datetime.strptime(release.first_published, "%B %d, %Y").date()  # noqa: DTZ007
    t060 = next(r for r in register if r["id"] == "T-060")
    assert released.isoformat() < str(t060["registered"])


def test_the_status_filter_offers_each_status_a_result_has(
    results: str, overview: overview_data.Overview
) -> None:
    """Status offers All, then each status some result has, in the workflow's order,
    each under its own word. Superseded is no status: the checkbox beside it asks that."""
    tools = re.search(r'<select data-filter="status">(.*?)</select>', results, re.DOTALL)
    assert tools
    offered = re.findall(r'<option value="([^"]*)"[^>]*>([^<]+)</option>', tools.group(1))
    present = {result.status for result in overview.results}
    assert offered[0] == ("", "All")
    assert offered[1:] == [
        (status, status) for status in result_status.STATUSES if status in present
    ]
    assert "superseded" not in dict(offered)
    assert '<select data-filter="standing">' not in results


def test_the_survey_counts_are_the_frontier_pages(page: str) -> None:
    """The survey's four counts are the Frontier page's since 2026-10-02
    (`test_the_frontier_page_opens_with_the_surveys_account`); the homepage states no
    count of cases and names no sentence of them."""
    assert not hasattr(overview_sections, "survey_counts")
    text = re.sub(r"<[^>]+>", "", page)
    assert "have a lower bound published or proved since" not in text
    assert "SURVEY_COUNTS" not in render_overview.OVERVIEW_ARTICLE.read_text(encoding="utf-8")


def test_a_reported_bound_is_a_row_of_the_results_table_and_no_block_of_its_own(
    page: str, results: str, overview: overview_data.Overview
) -> None:
    """Every recent case whose reported lower bound says more than its verified one is
    carried by register entries, and each of those is a row of both tables with its
    status. The overview lists no case of them on its own; the results page, where the
    statuses are defined, says how many results are not yet confirmed, each count the
    link to those rows (think-d04u; on the results page since 2026-10-02)."""
    waiting = [row for row in overview.recent if row.shows_reported]
    assert waiting
    carrying = {
        entry for row in waiting for entry in re.findall(r"T-\d{3}", row.reported.results)
    }
    assert carrying
    recent = _recent_table(page)
    by_id = {result.id: result for result in overview.results}
    for entry in sorted(carrying):
        chip = overview_sections.status_chip(by_id[entry].status)
        assert chip in _row(results, entry), entry
        if f'data-result="{entry.lower()}"' in recent:
            assert chip in _recent_row(recent, entry), entry
    # n = 11 reports T-060 rounded, and T-060 is verified: nothing awaits (think-pd2g).
    assert 11 not in [row.n for row in waiting]
    for gone in ("site-replay", "awaiting replay", 'id="replay-n-', "pop-replay-n-"):
        assert gone not in page, gone
    assert not hasattr(overview, "awaiting_replay")
    assert not hasattr(overview_sections, "awaiting_replay")
    sentence = overview_sections.status_counts(overview)
    held = Counter(result.status for result in overview.results)
    opening = f"Of the {len(overview.results)} results, {held['confirmed']} are confirmed"
    assert opening in sentence
    assert sentence.endswith(".")
    assert "this table shows" not in sentence
    for status, count in held.items():
        link = f"[{count} {status}](all-results.html?status={status})"
        assert (link in sentence) is (status != "confirmed"), status
        if status != "confirmed":
            linked = f'<a href="all-results.html?status={status}">{count} {status}</a>'
            assert linked in results
            assert linked not in page
    # It stands where the statuses are defined, between their definitions and the rule
    # that the status is never set by hand.
    prose = results.split("</h1>", 1)[1].split('<div class="site-table-tools', 1)[0]
    text = _rendered_text(prose)
    assert text.index("a defect found in it still open.") < text.index(opening)
    assert text.index(opening) < text.index("The status follows the confirmation rung")
    assert opening not in _rendered_text(page)


def test_results_by_others_show_their_publication_date(
    results: str, overview: overview_data.Overview
) -> None:
    for result in overview.results:
        row = _row(results, result.id)
        attribution = result.record.get("attribution")
        if attribution:
            published = str(attribution["published"])
            assert result.dated == ("published", published)
            assert f'{published} <span class="site-date-kind">published</span></td>' in row
        else:
            assert result.dated[0] == "established"
    recent = overview_sections.recent_table(overview)
    dates = re.findall(r'([\d-]+) <span class="site-date-kind">(\w+)</span></td>', recent)
    assert dates
    assert [d for d, _ in dates] == sorted((d for d, _ in dates), reverse=True)
    assert max(r.dated[1] for r in overview.results) == dates[0][0]


def test_both_tables_of_results_have_the_same_columns(
    page: str, results: str, overview: overview_data.Overview
) -> None:
    """Both tables use the same row schema and ordinary links to complete result pages."""
    table = overview_sections.results_table(overview)
    recent = overview_sections.recent_table(overview)
    head = overview_sections.result_head()
    assert table.count(head) == recent.count(head) == 1
    classes = re.compile(r'<td class="([^"]+)"')
    placed = re.compile(r'^<tr (?:id|data-result)="(t-\d+)"([^>]*?)(?: hidden)?>')
    for result in _recent_entries(overview):
        here = _row(table, result.id)
        there = _recent_row(recent, result.id)
        assert classes.findall(here) == classes.findall(there)
        assert placed.sub(r'<tr key="\1"\2>', here) == placed.sub(r'<tr key="\1"\2>', there)
        assert f'href="result/{result.id.lower()}.html"' in here
        target = f"pop-result-{result.id.lower()}"
        assert _row_popover(table, target) == _row_popover(recent, target)
        assert "data-row-pop-src=" in _row_popover(table, target)
        assert "<dt>" not in _row_popover(table, target)
    assert re.findall(
        r"<th[^>]*>([^<]+)</th>", _recent_table(page).split("</thead>", 1)[0]
    ) == re.findall(r"<th[^>]*>([^<]+)</th>", results.split("</thead>", 1)[0])


def test_both_tables_of_results_end_with_the_same_id_column(
    overview: overview_data.Overview,
) -> None:
    """The id is a column of its own, the last since 2026-10-02 (`think-t090`; it was the
    first), in the results table and in Recent Results alike: one cell, written by one
    helper, holding the row's trigger and nothing else. On a phone it still opens each
    card, in both tables, which place their cells by class."""
    table = overview_sections.results_table(overview)
    recent = overview_sections.recent_table(overview)
    last = re.compile(r"<th([^>]*)>([^<]+)</th></tr></thead>")
    for html_table in (table, recent):
        head = last.search(html_table)
        assert head
        assert head.group(2) == "ID"
        assert 'class="site-col-id"' in head.group(1)
    for result in overview.results:
        trigger = (
            f'<a class="site-row-open" href="result/{result.id.lower()}.html">{result.id}</a>'
        )
        cell = f'<td class="site-col-id" data-value="{result.id}">{trigger}</td>'
        for row in _result_rows(table, recent, result.id):
            # The row's last cell, straight before the row's end.
            assert row.endswith(f"{cell}</tr>"), result.id
            assert row.count("site-row-open") == 1, result.id
            assert row.count(f">{result.id}<") == 1, result.id
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    # As narrow as an id, below the floor KPress keeps a cell to.
    assert "  .site-table .site-col-id {\n    min-width: 0;\n  }" in css
    # On a phone the id opens the card, in both tables, and the date, the row's first
    # cell, still follows the credit there.
    assert "  .site-results .site-col-id {\n    font-weight: 650;\n    grid-area: 1 / 1;" in css
    assert "    grid-column: 1 / -1;\n    order: 2;\n    text-align: end;" in css


def test_a_date_cell_leads_with_the_date_and_then_says_what_it_dates(
    overview: overview_data.Overview,
) -> None:
    """In both tables of results the date cell reads `2026-09-29 published`: the date,
    then the quiet word for what it dates, and nothing before the date. Both tables sort
    on the date alone, the cell's `data-value`, and filter on the row's `data-date`."""
    table = overview_sections.results_table(overview)
    recent = overview_sections.recent_table(overview)
    for result in overview.results:
        kind, dated = result.dated
        assert kind in {"published", "established"}
        cell = f'{dated} <span class="site-date-kind">{kind}</span>'
        assert overview_sections.date_cell(result) == cell
        row = _row(table, result.id)
        assert f'<td class="site-col-date" data-value="{dated}">{cell}</td>' in row, result.id
        if f'data-result="{result.id.lower()}"' in recent:
            row = _recent_row(recent, result.id)
            assert f'<td class="site-col-date" data-value="{dated}">{cell}</td>' in row, (
                result.id
            )
        assert f'data-date="{overview_sections.first_day(dated)}"' in row, result.id
    assert '<th data-sort="text" title="Published, for a result by others;' in table
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    # On a wide table the word sits under the date; on a phone, beside it.
    assert ".site-table .site-date-kind {\n  color: var(--site-support-color);\n" in css
    assert ".site-results .site-date-kind {\n    display: inline;" in css


#: A new result's star as a row carries it, straight after the result's text: an image
#: whose name and tooltip are one label.
ROW_STAR = re.compile(
    '<span class="site-star" role="img" aria-label="([^"]+)" title="([^"]+)">\u2605</span>'
)


def test_a_new_result_is_starred_in_both_tables_by_the_atlas_rule(
    page: str, results: str, overview: overview_data.Overview
) -> None:
    """A row is starred where the atlas stars its case: the result holds a case's
    verified lower bound now, and that bound is recent (`starred_results`). The starred
    cases are the ones a case's visual summary and the film call a new result, each starred
    result is a current best in scope, and the star is read as well as seen: it has a
    label, the row's name says so, and the prose above each table says what it marks."""
    atlas = {n for n, fact in result_overview.film_facts().items() if fact["star"]}
    assert atlas == set(overview.recent_lower)
    starred = overview.starred
    assert {n for cases in starred.values() for n in cases} == atlas
    by_id = {result.id: result for result in overview.results}
    for result_id, cases in starred.items():
        result = by_id[result_id]
        assert result.standing == render_recent_results.HOLDS, result_id
        assert set(cases) <= set(scope_values(dict(result.record["scope"]))), result_id
    # T-060 settles n = 11 and T-093 holds n = 17 (T-043 until 2026-10-05). T-037 is as
    # new and is superseded, T-007 holds its cases and is from 2005, and T-057 is a new
    # upper bound, which the atlas does not star.
    assert starred["T-060"] == (11,)
    assert starred["T-093"] == (17,)
    assert not {"T-037", "T-007", "T-057", "T-043"} & set(starred)

    table = overview_sections.results_table(overview)
    recent = overview_sections.recent_table(overview)
    for result in overview.results:
        # Each row, and where its star stands: after the result's own text, the last
        # thing in its cell, since its records are a Details column (think-e4o3).
        # The star follows the significance mark, in the significance cell, since
        # 2026-10-03 (`think-m3m4`); the result's cell holds its text alone.
        level = overview_sections.significance(result)
        mark = overview_sections.significance_mark(
            level, overview_sections.rung_meanings()[f"S{level}"]
        )
        placed_here = mark + "{star}</td>"
        rows = [(row, placed_here) for row in _result_rows(table, recent, result.id)]
        for row, placed in rows:
            name = re.search(r' aria-label="([^"]*)"', row)
            assert name
            if result.id not in starred:
                assert "site-star" not in row, result.id
                assert not name.group(1).endswith("new result"), result.id
                continue
            label = html.escape(overview_sections.new_result_label(result, overview))
            assert label.startswith("New result: holds the verified lower bound for n = ")
            star = ROW_STAR.search(row)
            assert star, result.id
            assert star.groups() == (label, label), result.id
            assert row.count("site-star") == 1, result.id
            assert placed.replace("{star}", star.group(0)) in row, result.id
            assert name.group(1).endswith(", new result"), result.id
    assert overview_sections.new_result_label(by_id["T-060"], overview).endswith("n = 11")

    recent_starred = set(starred) & {r.id for r in _recent_entries(overview)}
    assert len(ROW_STAR.findall(recent)) == len(recent_starred)
    assert len(ROW_STAR.findall(table)) == len(starred)
    # Each page carries every row's star, and says in its prose what the star marks.
    legend = re.sub(r"<[^>]+>", "", overview_sections.star_legend())
    assert legend == (
        "A star (\u2605) marks a new result, as the atlas does: the verified lower bound of a "
        "case rests on it now, and it was proved or published on or after 22 August 2026."
    )
    for served, expected in ((page, recent_starred), (results, starred)):
        assert len(ROW_STAR.findall(served)) == len(expected)
        # The legend under each table says what the star marks, in two words.
        words = f"<span>{overview_sections.NEW_RESULT}</span>"
        assert f"{overview_sections.STAR}</span> {words}" in _legend(served)
    # The results page says it in full before its table; the overview says no more than
    # its legend since 2026-10-03 (think-42dx).
    assert legend in re.sub(r"<[^>]+>", "", results)
    assert results.index("marks a new result") < results.index('<div class="site-table-tools')
    assert legend not in re.sub(r"<[^>]+>", "", page)
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    # The star's colour is a token (`think-zhlc`), and it sits after the significance
    # mark's bars in the significance cell, no longer hung after the result's text.
    assert ".site-star {\n  color: var(--site-new-result);\n}" in css
    assert ".site-results .site-col-s .site-star {" in css
    assert ".site-col-result .site-star" not in css
    assert "td.site-col-result:has(.site-star)" not in css
    assert "\u00a0" not in table + recent


def test_a_table_of_results_is_one_flat_list_newest_first(
    page: str, results: str, overview: overview_data.Overview
) -> None:
    """Neither table of results has a heading row among its rows: every row is a
    result's, in one order on both pages, newest first by the date the table shows and
    then by id. The lineage the headings said is read from each row's credit, which is
    the register's credit line set whole, and the Source filter still narrows the table
    to this project's results or to others'."""
    table = overview_sections.results_table(overview)
    recent = overview_sections.recent_table(overview)
    order = [result.id.lower() for result in overview_sections.recent_results(overview)]
    assert re.findall(r'<tr id="(t-\d+)"', table) == order
    assert re.findall(r'<tr data-result="(t-\d+)"', recent) == [
        r.id.lower() for r in _recent_entries(overview)
    ]
    dates = [overview_sections.first_day(r.dated[1]) for r in overview.results]
    assert sorted(dates, reverse=True) == [
        overview_sections.first_day(r.dated[1])
        for r in overview_sections.recent_results(overview)
    ]
    for served in (table, recent, results, _recent_table(page)):
        assert 'class="site-group-row"' not in served
        assert "data-group=" not in served
        assert 'scope="colgroup"' not in served
    assert table.count("<tr ") == len(overview.results)
    assert recent.count("<tr ") == len(_recent_entries(overview))
    for title, _ in overview.groups:
        assert html.escape(title) not in results, title
    assert len(overview.groups) > 1
    # Each row's credit is the register's, whole: the finder, then what it builds on.
    for result in overview.results:
        cell = (
            f'<td class="site-col-credit" data-value="{html.escape(result.credit)}">'
            f"{overview_sections.credit_cell(result.credit)}</td>"
        )
        assert cell in _row(table, result.id), result.id
        if f'data-result="{result.id.lower()}"' in recent:
            assert cell in _recent_row(recent, result.id), result.id
        source = "ours" if result.ours else "others"
        assert f'data-source="{source}"' in _row(table, result.id), result.id
    assert {result.ours for result in overview.results} == {True, False}
    bar = _filter_bar(results)
    assert '<label>Source <select data-filter="source">' in bar
    assert ">This project</option>" in bar
    assert ">Others</option>" in bar
    # The script has no heading logic left, and the stylesheet none for a results table.
    script = render_overview.TABLE_SCRIPT.read_text(encoding="utf-8")
    assert "site-group-row" not in script
    assert "rowsShown" not in script
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert ".site-results tr.site-group-row" not in css
    assert ".site-results tbody tr.site-group-row" not in css


def test_grouping_agrees_with_readmes_relation(
    overview: overview_data.Overview, records: render_recent_results.Records
) -> None:
    """The register's groups, which `RESULTS.md` prints and no page of the site does, are
    `source_lineage`'s, the lineage `render_recent_results.relation` names, so wand125's
    T-048, T-054 and T-055 read as crediting this project second-hand in both."""
    titles = dict(OTHERS)
    for title, members in overview.groups[1:]:
        for result in members:
            lineage = source_lineage(result.record, records.sources)
            assert titles[lineage] == title, result.id
            if render_recent_results.is_recent_by_others(result.record):
                relation = render_recent_results.relation(result.record, records)
                assert render_recent_results.LINEAGES[str(lineage)] == relation, result.id
    group = {r.id: title for title, members in overview.groups for r in members}
    for result_id in ("T-048", "T-054", "T-055"):
        assert group[result_id] == "Crediting this project second-hand", result_id
        relation = render_recent_results.relation(records.results[result_id], records)
        assert relation == "credits second-hand", result_id


def test_each_row_detail_names_its_novelty_label(
    results: str, overview: overview_data.Overview, result_bodies: dict[str, str]
) -> None:
    """The complete result page carries the novelty; the table's panel links to it.

    The bodies are the module's `result_bodies`, rendered in setup: rendering them in
    this call, as the first test of the module to ask, took 12.08 s on run 37877186650."""
    for result in overview.results:
        body = result_bodies[result.id]
        assert f'data-novelty="{result.novelty}"' in body
        panel = _row_popover(results, f"pop-result-{result.id.lower()}")
        assert f'href="result/{result.id.lower()}.html"' in panel
        assert "<dt>" not in panel
        assert "<dt>" not in _row(results, result.id)


def test_the_page_title_style_is_upright() -> None:
    """KPress sets `h2` in italic; the title style, which the homepage's first `h2` takes
    through `site-title`, overrides it, so it reads as the frontier atlas's `h1` does."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    rule = css[css.index(".site-hero h1,\n.kpress .site-title {") :]
    assert "font-style: normal;" in rule[: rule.index("}")]


def test_card_headlines_take_the_page_titles_sans_face_and_weight() -> None:
    """A card's headline, and its popover's repeat of it, is set in the sans face at the
    medium weight by the same two tokens the page title uses, which KPress's sans `h3`
    resolves to as well; no value of its own."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    title = css[css.index(".site-hero h1,\n.kpress .site-title {") :]
    headline = css[
        css.index(".kpress .site-card .site-card-value,\n.site-popover .site-popover-value {") :
    ]
    for rule in (title[: title.index("}")], headline[: headline.index("}")]):
        assert "font-family: var(--kpress-font-sans);" in rule
        assert "font-weight: var(--site-font-weight-sans-medium);" in rule
    assert "--site-font-weight-sans-medium: var(--paper-font-weight-sans-medium);" in css
    text = render_overview.PAPER_TYPE_CSS.read_text(encoding="utf-8")
    assert "--paper-font-weight-sans-medium: 550;" in text


def test_every_heading_and_headline_shares_one_leading() -> None:
    """One line height, 1.15, for every heading on screen: the text layer every page
    carries sets it on `h1` to `h6`, and the site's stylesheet reads the same token for a
    card's headline, a popover's, a case record's title, a page's subtitle and a column's
    name in the rating ladders. Print is left to KPress, and a formula in any of them
    takes no line of its own."""
    text = render_overview.PAPER_TYPE_CSS.read_text(encoding="utf-8")
    assert text.count("--paper-heading-leading: 1.15;") == 1
    assert (
        "@media screen {\n  .kpress-prose :is(h1, h2, h3, h4, h5, h6) {\n"
        "    line-height: var(--paper-heading-leading);\n  }\n}"
    ) in text
    assert text.count("var(--paper-heading-leading)") == 1
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    for selector in (
        ".kpress .site-card .site-card-value,\n.site-popover .site-popover-value {",
        ".kpress .site-case-title {",
        ".kpress .site-hero .subtitle {",
        ".kpress .site-ladders .site-ladders-name {",
    ):
        rule = css[css.index(selector) :]
        assert "line-height: var(--paper-heading-leading);" in rule[: rule.index("}")], selector
    assert css.count("var(--paper-heading-leading)") == 4
    assert "--paper-heading-leading:" not in css
    math = css[css.index(".site-page :is(h1, h2, h3, h4) :is(.kpress-math, .katex),\n") :]
    math = math[: math.index("}")]
    assert ":is(.site-card-value, .site-popover-value, .site-case-title," in math
    assert "  :is(.kpress-math, .katex) {\n" in math
    assert "line-height: 0;" in math
    # The explainer's hero title keeps KPress's own leading, which its math is fitted to.
    paper = EXPLAINER_STYLE.read_text(encoding="utf-8")
    assert "paper-heading-leading" not in paper
    assert "paper-heading-leading" not in EXPLAINER_SHELL.read_text(encoding="utf-8")
    assert "height: 1.05em !important;" in paper


def test_the_bar_sits_close_to_the_top_of_every_page() -> None:
    """The space above the bar is kpress's page top margin, narrowed once in the stylesheet
    every page carries, so the explainer, the KPress pages and the workbench all agree."""
    css = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    assert "--kpress-page-margin-block-start: 1rem;" in css


def test_the_gear_sits_level_with_the_tab_text() -> None:
    """The gear's centre is set at the middle of the tab text's capitals by one token, on
    every page and at every width, rather than at the middle of the bar's row."""
    css = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    assert "--site-gear-drop: 0.11em;" in css
    assert "translate: 0 var(--site-gear-drop);" in css


def test_every_page_starts_one_shared_space_below_the_bar() -> None:
    """The space from the bar's rule to a page's first block is one token, declared in the
    stylesheet every page carries and read by the site's column and the explainer's hero."""
    nav = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    assert "--site-page-top: 4rem;" in nav
    assert "padding-block-start: var(--site-page-top);" in render_overview.SITE_CSS.read_text(
        encoding="utf-8"
    )
    assert "padding-block-start: var(--site-page-top);" in EXPLAINER_STYLE.read_text(
        encoding="utf-8"
    )


def test_an_opening_picture_sits_one_token_nearer_the_bar() -> None:
    """The homepage's packing opens the page a token nearer the bar than a title does."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert "--site-hero-lift: 0.5rem;" in css
    assert "margin-block-start: calc(-1 * var(--site-hero-lift));" in css


def test_section_headings_share_one_space_above_and_one_below() -> None:
    """The space above an `h2` and the space below it are two tokens in the text layer
    both the site and the explainer read. Each has a screen value and, under print, the
    paper's own, so the explainer's PDF paginates as it did."""
    text = render_overview.PAPER_TYPE_CSS.read_text(encoding="utf-8")
    start = "@media print {\n  .kpress {\n    --paper-section-space"
    screen, _, printed = text.partition(start)
    assert "  --paper-section-space: calc(var(--kpress-font-size-base) * 2.7);\n" in screen
    assert "  --paper-section-space-below: 1.7rem;\n" in screen
    assert printed.startswith(": calc(var(--kpress-font-size-base) * 2.8);\n")
    assert "    --paper-section-space-below: 1.3rem;\n  }\n}" in printed[:120]
    paper = EXPLAINER_STYLE.read_text(encoding="utf-8")
    for css in (render_overview.SITE_CSS.read_text(encoding="utf-8"), paper):
        assert (
            "margin-block: var(--paper-section-space) var(--paper-section-space-below);" in css
        )
        assert "var(--paper-section-space) 1.3rem" not in css


def test_a_page_title_stands_one_space_above_what_follows_it() -> None:
    """The space under a page's title is one token: around its subtitle, and under a title
    that has none, a document's own `h1` among them, on screen. A hero title with a
    subtitle hands the space to the subtitle."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert css.count("--site-subtitle-space: 1.5rem;") == 1
    assert "  margin-block: var(--site-subtitle-space);\n" in css
    assert (
        "@media screen {\n  .site-page h1 {\n"
        "    margin-block-end: var(--site-subtitle-space);\n  }\n}\n"
        ".kpress .site-hero:has(.subtitle) h1 {\n  margin-block-end: 0;\n}"
    ) in css
    paper = EXPLAINER_STYLE.read_text(encoding="utf-8")
    assert "  .cert-page .hero .credits {\n    margin-block-start: 2.25rem;\n  }\n}" in paper
    assert "  margin-block: 2rem 2.2rem;\n" in paper


def test_a_tables_filter_bar_is_set_a_step_under_its_tables_text() -> None:
    """A table's filter bar, its controls, their labels and its count, is set at the
    control size, 0.8 of the sans base, a step under the table's own note-size text,
    so it reads as the table's tools (the owner, 2026-10-02, `think-gwcu`; it was the
    support size). On a touch screen a field keeps 16 pixels at least, under which a
    phone's browser zooms the page into it on focus."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert "--site-font-size-control: calc(var(--site-font-size-sans-base) * 0.8);" in css
    bar = css[css.index("\n.site-table-tools {") :]
    bar = bar[: bar.index("}")]
    assert "font-size: var(--site-font-size-control);" in bar
    assert "gap: 0.4rem 0.9rem;" in bar
    fields = css[css.index(".site-table-tools :is(select, input) {") :]
    assert "padding: 0.05rem 0.3rem;" in fields[: fields.index("}")]
    coarse = css[css.index("@media (pointer: coarse) {") :]
    assert (
        '.site-table-tools :is(select, input:not([type="checkbox"])) {\n'
        "    font-size: max(16px, 1em);"
    ) in coarse[: coarse.index("\n}\n")]


def test_a_filter_at_its_default_is_gray_and_one_that_filters_is_the_text_colour(
    page: str, results: str, rendered: Callable[[str], str]
) -> None:
    """A control at its no-filter value is gray and a control that filters is the text
    colour, so the bar says what narrows the table (the owner, 2026-10-02,
    `think-pcei`): a select showing its empty-valued "All", an empty field's placeholder
    and an unchecked checkbox's words are gray, and the count is the text colour. Every
    select in every bar has its no-filter choice as the empty value the rule reads."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    for rule, colour in (
        ('.site-table-tools select:has(option[value=""]:checked) {', "--site-support-color"),
        (".site-table-tools select option {", "--kpress-doc-text"),
        (".site-table-tools input::placeholder {", "--site-support-color"),
        ('.site-table-tools label:has(input[type="checkbox"]:checked) {', "--kpress-doc-text"),
        (".site-table-tools .site-count {", "--kpress-doc-text"),
    ):
        block = css[css.index(rule) :]
        assert f"color: var({colour});" in block[: block.index("}")], rule
    assert 'class="site-table-tools' not in page
    for name, html_page in (
        ("all-results.html", results),
        ("frontier.html", rendered("frontier.html")),
    ):
        bar = html_page.split('<div class="site-table-tools', 1)[1].split("</div>", 1)[0]
        selects = re.findall(r"<select[^>]*>(.*?)</select>", bar, re.DOTALL)
        assert selects, name
        for options in selects:
            assert options.startswith('<option value=""'), (name, options[:60])


def test_every_table_stands_one_shared_space_from_the_text_around_it() -> None:
    """The space above and below a table is one token: above the filter bar of a table
    that has one, below every table's wrap, and around a document's own table, which
    KPress wraps. The rules that read it are for
    the screen alone, so print keeps KPress's spacing; the bar is not printed at all."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert css.count("--site-table-space: 2rem;") == 1
    bar = css[css.index("\n.site-table-tools {") :]
    assert "margin-block: var(--site-table-space) 0.5rem;" in bar[: bar.index("}")]
    start = css.index("@media screen {\n  .kpress-table-wrap,")
    screen = css[start : css.index("\n}\n", start)]
    assert (
        "  .kpress-table-wrap,\n  .site-table-wrap {\n"
        "    margin-block: var(--site-table-space);\n  }"
    ) in screen
    # The bar keeps its own gap to its table.
    assert (
        "  .site-table-tools + .site-table-wrap {\n    margin-block-start: 0;\n  }"
    ) in screen
    assert "site-replay" not in css
    # The rating ladders, which are no table, stand the same space clear of the text.
    ladders = css[css.index("@media screen {\n  .site-ladders-frame {") :]
    assert "margin-block: var(--site-table-space);" in ladders[: ladders.index("}")]
    # A table of results' legend stands close under its table and takes the table's
    # space below itself (the owner, 2026-10-04).
    assert (
        "  .site-table-wrap:has(+ .site-rung-legend) {\n    margin-block-end: 0.75rem;\n  }"
    ) in screen
    assert (
        "  .site-rung-legend {\n    margin-block-end: var(--site-table-space);\n  }"
    ) in screen
    # The action row under a table or grid takes it below itself too (think-0o9u).
    assert css.count("var(--site-table-space)") == 5
    assert "@media print {\n  .site-nav,\n  .site-table-tools {\n    display: none;" in css
    design = (render_overview.TEMPLATES / "paper-design.md").read_text(encoding="utf-8")
    assert "| Above and below a table | `--site-table-space` | 2rem, 32px |" in design


def test_the_icon_frame_is_one_pixel_at_icon_size() -> None:
    """The logo and the favicon draw case 11's container as one whole pixel at the size
    each is shown, with its outer edge on the drawing's edge: (200 + w) / px = w."""
    from devtools.render_frontier_page import packing_svg  # noqa: PLC0415

    for px in (render_overview.SITE_LOGO_PX, render_overview.FAVICON_PX):
        svg = packing_svg(11, units=200, frame_px=px)
        view = re.search(r'viewBox="([^"]+)"', svg)
        stroke = re.search(r'<rect [^>]*stroke-width="([\d.]+)"', svg)
        assert view is not None
        assert stroke is not None
        box = [float(v) for v in view.group(1).split()]
        width = float(stroke.group(1))
        assert box[2] / px == pytest.approx(width, abs=1e-3)
        assert box[0] == pytest.approx(-width / 2, abs=1e-3)
        assert 'shape-rendering="crispEdges"' in svg
        lines = re.search(r'<g stroke="[^"]+" stroke-width="([\d.]+)"', svg)
        assert lines is not None
        assert float(lines.group(1)) == pytest.approx(width / 2, abs=1e-3)
    assert "block-size: 18px;" in render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    assert render_overview.SITE_LOGO_PX == 18


def test_page_subtitles_share_one_size() -> None:
    """Every hero's subtitle (the case records' "Every tracked case, n = 1 to 324, one
    record each"; the Results, Papers and Frontier pages carried one until 2026-10-02) is
    set from one scale of
    the sans base, a small step above it."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert "--site-subtitle-scale: 1.1;" in css
    rule = css[css.index(".kpress .site-hero .subtitle {") :]
    assert "var(--site-subtitle-scale)" in rule[: rule.index("}")]


def test_the_frontier_results_and_papers_pages_carry_no_subtitle(
    rendered: Callable[[str], str],
) -> None:
    """The three section pages' titles stand over their first paragraph with no subtitle
    between, since 2026-10-02 (the owner, think-wz9d): the lines "A survey of everything
    known for cases n = 1, …, 324", "A survey of all reviewed results" and "Papers and
    interactive explanations for specific results" are gone from the pages, the
    templates and the Frontier renderer's values, with no empty element left in the
    hero. The page descriptions are their own constants and stay. The case records'
    page keeps its subtitle, which the owner did not name."""
    from devtools.render_frontier_page import FRONTIER_ARTICLE  # noqa: PLC0415

    gone = (
        "A survey of everything known",
        "A survey of all reviewed results",
        "Papers and interactive explanations for specific results",
    )
    for name in ("frontier.html", render_overview.RESULTS_PAGE, "papers.html"):
        page = rendered(name)
        assert 'class="subtitle"' not in page, name
        hero = page.split('<div class="site-hero">', 1)[1].split("</div>", 1)[0]
        assert re.fullmatch(r"\s*<h1[^>]*>[^<]+</h1>\s*", hero), name
        # The templates' comments record the dropped lines, and the stylesheet's comment
        # quotes one; a reader sees none of them.
        seen = _seen(page)
        for line in gone:
            assert line not in seen, (name, line)
        assert '<meta name="description" content="' in page, name
    assert "{{CASE_RANGE}}" not in FRONTIER_ARTICLE.read_text(encoding="utf-8")
    assert "{{COUNT}}" not in render_overview.RESULTS_ARTICLE.read_text(encoding="utf-8")
    assert render_overview.RESULTS_DESCRIPTION
    assert render_overview.PAPERS_DESCRIPTION
    assert render_overview.FRONTIER_DESCRIPTION
    cases = rendered(render_case_pages.CASES_PAGE)
    assert cases.count('<p class="subtitle">') == 1


def test_wrapped_chips_never_touch() -> None:
    """Chips wrap like words; every chip carries a block margin, so a wrapped row keeps a
    gap from the row above wherever chips sit."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    rule = css[css.index(".site-chip {") :]
    assert "margin-block: 0.15rem;" in rule[: rule.index("}")]


#: Every arrow a typed character could draw, as characters and as CSS or HTML escapes.
ARROW_CHARACTERS = re.compile(
    r"[\u2190-\u21ff\u27f0-\u27ff\u2b00-\u2b0d\u2b60-\u2bff]"
    r"|\\21[9a-f][0-9a-f]|\\u21[9a-f][0-9a-f]|&(?:[lrudh]arr|nearr|varr);|&#x?21[9a-f]",
    re.IGNORECASE,
)


class _VisibleText(html.parser.HTMLParser):
    """Prose text, excluding math, code and explicitly hidden drawing content."""

    SKIP = frozenset({"style", "script", "math", "code", "pre", "svg"})
    VOID = frozenset(
        {
            "area",
            "base",
            "br",
            "col",
            "embed",
            "hr",
            "img",
            "input",
            "link",
            "meta",
            "param",
            "source",
            "track",
            "wbr",
        }
    )

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[tuple[str, bool]] = []
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in self.VOID:
            hidden = (
                bool(self.stack and self.stack[-1][1])
                or tag in self.SKIP
                or dict(attrs).get("aria-hidden") == "true"
            )
            self.stack.append((tag, hidden))

    def handle_endtag(self, tag: str) -> None:
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data: str) -> None:
        if not self.stack or not self.stack[-1][1]:
            self.parts.append(data)


def _visible_text(page: str) -> str:
    parser = _VisibleText()
    parser.feed(page)
    return "".join(parser.parts)


@pytest.mark.parametrize("name", sorted(render_overview.PAGES))
def test_no_arrow_on_a_site_page_is_a_typed_character(
    name: str, rendered: Callable[[str], str]
) -> None:
    """Every arrow a site page shows is the one drawn icon set. The one exception is a
    repository document's own prose, where its author writes an arrow as notation
    (`experiment → series` in conventions.md): its article may show no more arrows than
    its Markdown source has, and the page around the article none."""
    from devtools.site_documents import DOCUMENTS  # noqa: PLC0415

    page = rendered(name)
    sources = {doc.name: doc.source for doc in DOCUMENTS}
    if name in sources:
        body = re.search(r"<article\b.*?</article>", page, re.DOTALL)
        assert body is not None, name
        written = len(ARROW_CHARACTERS.findall(sources[name].read_text(encoding="utf-8")))
        assert len(ARROW_CHARACTERS.findall(_visible_text(body.group(0)))) <= written, name
        page = page.replace(body.group(0), "")
    assert not ARROW_CHARACTERS.findall(_visible_text(page)), name


@pytest.mark.parametrize("name", sorted(render_overview.PAGES))
def test_every_arrow_icon_comes_from_the_one_set(
    name: str, rendered: Callable[[str], str]
) -> None:
    """Every inline arrow is `arrow_icon`'s markup, hidden from assistive technology, and
    no page draws an arrow of its own."""
    page = rendered(name)
    icons = re.findall(r"<span class=\"site-icon-arrow\"[^>]*></span>", page)
    allowed = {overview_sections.arrow_icon(d) for d in overview_sections.ARROW_DIRECTIONS}
    assert set(icons) <= allowed, name
    assert 'class="site-arrow' not in page


def test_the_icon_set_is_one_drawing_in_the_stylesheet() -> None:
    """The stylesheet draws every arrow from `--site-arrow` (and the sort pair), declared
    once, and no generated content or site script is an arrow character."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    nav = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    assert css.count("--site-arrow: url(") == 1
    assert css.count("--site-arrow-sort: url(") == 1
    assert css.count("--site-arrow-double: url(") == 1
    assert "--site-arrow" not in nav
    for content in re.findall(r"content:\s*([^;]+);", css):
        assert not ARROW_CHARACTERS.search(content), content
    for mask in re.findall(r"mask(?:-image)?:\s*([^;]+);", css):
        assert re.match(r"var\(--site-arrow(?:-sort|-double)?\)", mask), mask
    # The double chevron is the arrow's head twice, in the arrow's own box and stroke.
    head = "stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'"
    double = re.search(r"--site-arrow-double: url\(\"([^\"]+)\"\);", css)
    assert double is not None
    assert head in double.group(1)
    assert "d='M3.5 3 8 7.5 12.5 3M3.5 8 8 12.5 12.5 8'" in double.group(1)
    scripts = (render_overview.PACKING / "devtools" / "overview").glob("*.js")
    for script in scripts:
        assert not ARROW_CHARACTERS.search(script.read_text(encoding="utf-8")), script.name
    assert not ARROW_CHARACTERS.search(
        render_overview.OVERVIEW_ARTICLE.read_text(encoding="utf-8")
    )
    with pytest.raises(ValueError, match="unknown arrow direction"):
        overview_sections.arrow_icon("sideways")


# The one hover transition and every hover's use of it are held by
# `tests/test_site_hover_motion.py`.


def test_every_popover_shares_one_margin_and_close_target() -> None:
    """Popover margins are one token on all four sides, and the close cross is one square
    tap target set in from the corner by another."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    popover = css[css.index(".site-popover {") :]
    assert "padding: var(--site-popover-pad);" in popover[: popover.index("}")]
    close = css[css.index(".site-popover .site-popover-close {") :]
    close = close[: close.index("}")]
    for token in ("--site-popover-close)", "--site-popover-close-inset)"):
        assert f"var({token}" in close


def test_a_popover_is_as_tall_as_the_window_allows() -> None:
    """A popover's height has one limit, read from one token: the window's height less a
    margin above and below, so a taller window shows more of a long panel. A card's and
    a row's popover, the case popover and a result overview may be that tall, and a
    framed page is that tall. No rule stops a popover at a
    fixed height, and none declares `max-height`, which is the same property as
    `max-block-size` and would override it. A phone keeps the heights it had."""
    css = re.sub(
        r"/\*.*?\*/", "", render_overview.SITE_CSS.read_text(encoding="utf-8"), flags=re.DOTALL
    )
    assert css.count("--site-popover-window-margin: clamp(1rem, 4dvh, 3rem);") == 1
    assert (
        css.count(
            "--site-popover-max-block: calc(100dvh - 2 * var(--site-popover-window-margin));"
        )
        == 1
    )
    limit = "max-block-size: var(--site-popover-max-block);"
    assert limit in _rule(css, ".site-popover")
    assert limit in _rule(css, ".site-popover.site-case-pop:popover-open")
    framed = _rule(css, '.site-popover[data-go="page"]:popover-open')
    assert "block-size: var(--site-popover-max-block);" in framed
    assert "max-block-size: none;" in framed
    result = render_overview.SITE_RESULT_CSS.read_text(encoding="utf-8")
    assert limit in _rule(
        result, ".site-popover:has(.site-result, [data-row-pop-src]):popover-open"
    )
    for sheet in (css, result):
        popovers = [
            body
            for selector, body in re.findall(r"([^{}]+){([^{}]*)}", sheet)
            if ".site-popover" in selector or ".site-atlas-pop" in selector
        ]
        assert popovers
        assert not any("max-height" in body for body in popovers)
    # The phone's own heights, each restated under the phone's media query.
    phone = css.split("@media (max-width: 40rem) {")[1:]
    assert any(
        "  .site-popover {\n    max-block-size: min(80vh, 40rem);" in block for block in phone
    )
    assert any("    block-size: min(88vh, 56rem);" in block for block in phone)
    assert any(
        "  .site-popover.site-case-pop:popover-open {\n    max-block-size: calc(100dvh - 1rem);"
        in block
        for block in phone
    )


def _rule(css: str, selector: str) -> str:
    """Declarations of the first rule containing the requested selector."""
    rules = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    wanted = " ".join(selector.split())
    for found in re.finditer(r"([^{}]+)\{([^{}]*)\}", rules):
        choices = " ".join(found[1].split())
        if wanted == choices or wanted in [part.strip() for part in choices.split(",")]:
            return found[2]
    raise AssertionError(selector)


def test_no_site_text_breaks_inside_a_word() -> None:
    """KPress's `overflow-wrap: break-word` cuts a run only when it is longer than a whole
    line. `anywhere` also lets a column shrink to one character, so the site puts it on
    the two things that are long runs by nature, an exact decimal and a repository path,
    and nowhere else; and no sheet breaks words with `word-break` or hyphenates them."""
    sheets = {
        sheet.name: re.sub(r"/\*.*?\*/", "", sheet.read_text(encoding="utf-8"), flags=re.DOTALL)
        for sheet in (
            render_overview.SITE_CSS,
            render_overview.SITE_RESULT_CSS,
            render_overview.SITE_NAV_CSS,
            render_overview.PAPER_TYPE_CSS,
        )
    }
    anywhere = {
        (name, selector.strip())
        for name, rules in sheets.items()
        for selector, body in re.findall(r"([^{}]+){([^{}]*)}", rules)
        if "overflow-wrap: anywhere" in body
    }
    assert anywhere == {
        ("site.css", ".site-case-decimal"),
        ("site-result.css", ".site-result-links code"),
    }
    for name, rules in sheets.items():
        assert set(re.findall(r"word-break: ([a-z-]+)", rules)) <= {"normal"}, name
        assert "hyphens:" not in rules, name


def test_a_label_column_is_as_wide_as_its_labels() -> None:
    """No label column has a width of its own. The film panel's citation rows, in a
    case's visual summary, are table rows, so their label cell is as wide as "lower" or
    "upper" is drawn; and a name set as code is one box that a line breaks before, never
    inside. The frontier row's pairs, labels in a `max-content` column, went with its
    popover on 2026-10-03."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert ".site-pairs" not in css
    cite = _rule(css, ".site-atlas-pop .site-atlas-pop-cite")
    assert "display: table-row;" in cite
    assert "padding-inline-start" not in cite
    assert "text-indent" not in cite
    which = _rule(css, ".site-atlas-pop-which")
    assert "display: table-cell;" in which
    assert "white-space: nowrap;" in which
    assert "inline-size" not in which
    name = _rule(css, ".site-name")
    assert "display: inline-block;" in name
    assert "max-inline-size: 100%;" in name
    assert "minmax(min(100%, 17rem), 1fr)" in _rule(css, ".site-case-bounds")
    link = _rule(
        render_overview.SITE_RESULT_CSS.read_text(encoding="utf-8"),
        ".site-result-links a:has(> code)",
    )
    assert "display: inline-block;" in link
    assert "max-inline-size: 100%;" in link


def test_a_headline_that_is_all_math_sets_it_serif(page: str) -> None:
    """A headline that is mathematics standing alone, such as `n = 11`, is marked for
    serif mathematics, on a card and in its popover; a headline with words in it carries
    no mark, so its math follows the words into the sans. No popover forces sans
    mathematics on everything inside it."""
    formula = overview_data.math_html("n = 11")
    assert overview_sections.is_all_math(formula)
    assert overview_sections.is_all_math(f" {formula} {formula}\n")
    for mixed in (f"Earlier {formula} lower bounds", f"{formula}.", "Results", ""):
        assert not overview_sections.is_all_math(mixed), mixed
    assert overview_sections.SERIF_MATH == 'data-math-face="serif"'

    def built(value: str) -> str:
        return overview_sections.card(
            "pop-x", "Case", value, "A note.", href="#recent-results", action="Go"
        )

    alone = built(formula)
    assert f'<span class="site-card-value" data-math-face="serif">{formula}</span>' in alone
    assert f'<p class="site-popover-value" data-math-face="serif">{formula}</p>' in alone
    assert "data-math-face" not in built(f"Earlier {formula} lower bounds")
    link = overview_sections.link_card("frontier.html", "Case", formula, "A note.")
    assert f'<span class="site-card-value" data-math-face="serif">{formula}</span>' in link
    assert "data-math-face" not in overview_sections.link_card(
        "frontier.html", "Case", f"{formula} to 100", "A note."
    )

    headlines = re.findall(
        r'<span class="site-card-value"([^>]*)>(.*?)</span><span class="site-card-note">', page
    ) + re.findall(r'<p class="site-popover-value"([^>]*)>(.*?)</p>', page)
    assert len(headlines) > len(overview_sections.DOCUMENTS)
    for attributes, value in headlines:
        marked = overview_sections.SERIF_MATH in attributes
        assert marked == overview_sections.is_all_math(value), value
    shell = (
        render_overview.PACKING
        / "devtools"
        / "probes"
        / "render_n11_lower_bounds_explainer"
        / "host_math_init.js"
    ).read_text(encoding="utf-8")
    assert "closest('[data-math-face=\"serif\"]')" in shell


TABLE_BLEED = ".site-page .site-wide:is(.site-table-wrap, :has(> .site-table-wrap)) {"


def test_data_tables_bleed_like_the_atlas_only_above_1280_pixels() -> None:
    """A data table's wide track is one rule on shared tokens. It stops at its own
    maximum, short of the atlas grid's, and its growth term is zero at or below
    `--site-table-bleed-from` (80rem), so a table at 1280 pixels or narrower keeps the
    plain wide track."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert "--site-bleed-max: 140rem;" in css
    assert "--site-table-bleed-from: 80rem;" in css
    grid = css[css.index(".site-page .site-atlas-grid {") :]
    assert "--site-wide: var(--site-bleed-max);" in grid[: grid.index("}")]
    rule = css[css.index(TABLE_BLEED) :]
    rule = rule[: rule.index("\n}")]
    assert "--site-table-max: 100rem;" in css
    assert "var(--site-table-max)," in rule
    assert "--site-table-grow: max(0px, 100vw - var(--site-table-bleed-from));" in rule
    assert "calc(var(--site-wide) + var(--site-table-grow))" in rule
    assert "max-width: var(--site-table-wide);" in rule


def test_a_wide_block_keeps_one_gutter_inside_the_pages_content_area() -> None:
    """A table and its filter bar, a row of cards, the atlas grid and the film stop one
    token short of the page's content area on either side. That area is KPress's page
    container, `100cqw`, never the window: `100vw` counts a scrollbar the layout does
    not, and a narrow page clips at the document's edge. A wide track, a table's bleed
    and the film all read the one room; a document's own table keeps to its column in
    KPress's own narrow band, a phone's row cards are padded, and a result overview's
    bounds scroll inside their own box."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert css.count("--site-wide-gutter: 0.5rem;") == 1
    assert css.count("--site-wide-gutter:") == 1
    wide = css[css.index(".site-page .site-wide {") :]
    wide = wide[: wide.index("}")]
    assert "--site-wide-room: calc(100cqw - 2 * var(--site-wide-gutter));" in wide
    assert "max-width: min(var(--site-wide), var(--site-wide-room));" in wide
    rule = css[css.index(TABLE_BLEED) :]
    assert "    var(--site-wide-room),\n" in rule[: rule.index("\n}")]
    film = css[css.index(".site-page .site-film-frame {") :]
    assert "min(100cqw - 2 * var(--site-wide-gutter), " in film[: film.index("}")]
    # No block in the page's flow is sized from the window: only a popover, which is
    # laid out in the window's own top layer, and a table's growth above 1280 pixels,
    # which the room still caps.
    sized = [
        line.strip()
        for line in css.splitlines()
        if "100vw" in line and re.match(r"\s*[\w-]+:\s", line)
    ]
    assert sized == [
        "--site-table-grow: max(0px, 100vw - var(--site-table-bleed-from));",
        "max-width: min(36rem, 100vw - 2rem);",
        "inline-size: min(46rem, 100vw - 2rem);",
        "inline-size: min(62rem, 100vw - 2rem);",
        "inline-size: calc(100vw - 1rem);",
    ]
    assert (
        "@container kpress-doc (max-width: 47.99rem) {\n"
        "  .kpress .site-page .kpress-table-wrap {\n    max-inline-size: 100%;\n  }\n}"
    ) in css
    row = css[css.index("  .site-results tr {") :]
    assert "padding: 0.7rem 0.5rem;" in row[: row.index("}")]
    result = render_overview.SITE_RESULT_CSS.read_text(encoding="utf-8")
    bounds = result[result.index(".site-result-bounds {") :]
    bounds = bounds[: bounds.index("}")]
    assert "max-inline-size: 100%;" in bounds
    assert "overflow-x: auto;" in bounds


class _TableAncestry(HTMLParser):
    """Each `<table>`'s own classes and the classes of the elements around it."""

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[tuple[str, str]] = []
        self.tables: list[tuple[str, list[str]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = dict(attrs).get("class") or ""
        if tag == "table":
            # KPress's own table wrap, where it adds one, is not the site's.
            around = [c for _, c in reversed(self.stack) if c != "kpress-table-wrap"]
            self.tables.append((classes, around))
        if tag in {"div", "details", "section", "table"}:
            self.stack.append((tag, classes))

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break


def test_every_data_table_is_the_shared_component(page: str, results: str) -> None:
    """Every `.site-table` on the overview, the results page and the frontier atlas is a
    KPress table directly in a `.site-table-wrap`, and every one that fills its track is
    in a `.site-wide` the bleed rule takes (the wrap itself, or its parent). Only the
    compact replay table keeps to its content, and it is the rule's one exclusion."""
    from devtools.render_frontier_page import frontier_cases, table_html  # noqa: PLC0415

    seen = 0
    for text in (page, results, table_html(frontier_cases())):
        parser = _TableAncestry()
        parser.feed(text)
        for classes, around in parser.tables:
            if "site-table" not in classes.split():
                continue
            seen += 1
            assert "kpress-table" in classes.split()
            wrap = around[0].split()
            parent = around[1].split() if len(around) > 1 else []
            assert "site-table-wrap" in wrap, classes
            assert "site-wide" in wrap or "site-wide" in parent, classes
    assert seen >= 3


# ---------- Row popovers: the row is the unit (think-br9e) ----------

#: The pages whose tables have rows with detail. The frontier table's rows open the
#: case popover instead, since 2026-10-03 (`test_case_pages`).
ROW_PAGES = ("index.html", "all-results.html")


class _RowWiring(HTMLParser):
    """What ties a page's table rows to their popovers: every body row of a `.site-table`
    that is not a group heading, with the triggers in its cells; every row popover, with
    whether it sits inside a table; how many cells the page has and how many `<details>`
    sit inside one; and how often each id occurs.
    """

    def __init__(self) -> None:
        super().__init__()
        self.rows: list[tuple[dict[str, str | None], list[str | None]]] = []
        self.popovers: dict[str, dict[str, str | None]] = {}
        self.inside_tables: list[str] = []
        self.cells = 0
        self.cell_details = 0
        self.ids: Counter[str] = Counter()
        self.closers: Counter[str] = Counter()
        self._depth = {"table": 0, "tbody": 0, "td": 0, "th": 0}
        self._site_table = False
        self._row: list[str | None] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        found = dict(attrs)
        classes = (found.get("class") or "").split()
        if found.get("id"):
            self.ids[str(found["id"])] += 1
        if tag in self._depth:
            self._depth[tag] += 1
        if tag == "table":
            self._site_table = "site-table" in classes
        elif tag in {"td", "th"}:
            self.cells += 1
        elif tag == "tr":
            self._row = None
            if self._site_table and self._depth["tbody"]:
                self._row = []
                self.rows.append((found, self._row))
        elif tag == "a" and "site-row-open" in classes and self._row is not None:
            path = (found.get("href") or "").rsplit("/", 1)[-1].removesuffix(".html")
            self._row.append(f"pop-result-{path}")
        elif tag == "button" and "site-popover-close" in classes:
            hides = found.get("popovertargetaction") == "hide"
            self.closers[str(found.get("popovertarget"))] += int(hides)
        elif tag == "details" and (self._depth["td"] or self._depth["th"]):
            self.cell_details += 1
        elif tag == "div" and "site-row-pop" in classes:
            self.popovers[str(found.get("id"))] = found
            if self._depth["table"]:
                self.inside_tables.append(str(found.get("id")))

    def handle_endtag(self, tag: str) -> None:
        if tag in self._depth:
            self._depth[tag] -= 1
        if tag == "tr":
            self._row = None
        elif tag == "table":
            self._site_table = False


@functools.cache
def _row_wiring(name: str) -> _RowWiring:
    parser = _RowWiring()
    parser.feed(site_renders.html(name))
    return parser


@pytest.mark.parametrize("name", ROW_PAGES)
def test_no_table_cell_expands_on_its_own(name: str) -> None:
    """No `<td>` or `<th>` on a page with a site table holds a `<details>`: a row's
    detail is its popover. The replay table's own disclosure wraps the whole table."""
    wiring = _row_wiring(name)
    assert wiring.rows, name
    assert wiring.cells > len(wiring.rows), name
    assert wiring.cell_details == 0, name


@pytest.mark.parametrize("name", ROW_PAGES)
def test_every_row_with_detail_is_wired_to_one_popover(name: str) -> None:
    """Every body row of every site table names one popover, has an accessible name, and
    carries exactly one native trigger for that popover, so it opens without scripts.
    The popover is on the page once, outside every table, a dialog labelled by its own
    headline, with a close cross of its own; no popover is left without a row.
    A row carries no `tabindex`: `row-popover.js` makes it focusable when it takes the
    trigger out of the tab order, so without scripts the trigger is the one stop."""
    wiring = _row_wiring(name)
    targets = []
    for attributes, triggers in wiring.rows:
        target = attributes.get("data-row-popover")
        assert target, attributes
        assert attributes.get("aria-label"), target
        assert "tabindex" not in attributes, target
        assert triggers == [target], target
        targets.append(target)
    assert len(targets) == len(set(targets)), name
    assert set(targets) == set(wiring.popovers), name
    assert not wiring.inside_tables, name
    for target, popover in wiring.popovers.items():
        assert wiring.ids[target] == 1, target
        assert "popover" in popover, target
        assert (popover.get("class") or "").split()[0] == "site-popover", target
        assert popover.get("role") == "dialog", target
        assert popover.get("aria-labelledby") == f"{target}-title", target
        assert wiring.ids[f"{target}-title"] == 1, target
        assert wiring.closers[target] == 1, target


def test_the_tables_with_row_detail_are_the_ones_named(
    overview: overview_data.Overview,
) -> None:
    """The recent table on the overview and the results table on its page: each row's
    popover is its own, by its key. The frontier table's rows open their case's record
    in the one case popover instead (think-necq)."""
    recent = {f"pop-result-{r.id.lower()}" for r in _recent_entries(overview)}
    assert recent
    assert set(_row_wiring("index.html").popovers) == recent
    assert set(_row_wiring("all-results.html").popovers) == {
        f"pop-result-{r.id.lower()}" for r in overview.results
    }
    assert not _row_wiring("frontier.html").popovers


@pytest.mark.parametrize("name", ROW_PAGES)
def test_a_page_with_row_detail_carries_the_row_and_popover_scripts(
    name: str, rendered: Callable[[str], str], served: Callable[[str], str]
) -> None:
    """The row script makes the row the control, and the popover script typesets a
    popover's math when it opens and closes it when a link inside is followed."""
    page = rendered(name)
    whole = served(name)
    for script in (
        render_overview.ROW_POPOVER_SCRIPT,
        render_overview.POPOVER_SCRIPT,
        render_overview.TABLE_SCRIPT,
    ):
        assert page.count(_asset_tag(script, name)) == 1, script.name
        assert script.read_text(encoding="utf-8") in whole, script.name


def test_a_result_rows_popover_body_comes_from_one_function(
    overview: overview_data.Overview, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`result_row_popover_body` is the one source of what a result's row opens to, on
    the overview's recent table and on the results page alike: the result's whole
    overview. It is written once, as the result's fragment beside the pages; a row's
    popover names that fragment and holds the short detail, and no cell repeats either."""
    from devtools import result_overview  # noqa: PLC0415

    result = overview_sections.recent_results(overview)[0]
    body = overview_sections.result_row_popover_body(result, overview)
    assert body == result_overview.result_popover_html(result, overview)
    assert body.startswith(
        f'<div class="site-result" data-result-overview="{result.id.lower()}">'
    )

    def marked(
        result: overview_data.Result, _: overview_data.Overview, **_metadata: object
    ) -> str:
        return f"<p>BODY OF {result.id}</p>"

    monkeypatch.setattr(overview_sections, "result_row_popover_body", marked)
    fragments = render_overview.result_fragments()
    assert [file.name for file in fragments] == [
        f"result/{row.id.lower()}.html" for row in overview.results
    ]
    for file, row in zip(fragments, overview.results, strict=True):
        assert f"BODY OF {row.id}" in file.html
        assert "<main " in file.html
        assert "<h1 " in file.html
        assert 'aria-label="Neighboring results"' in file.html
        for neighbor in re.findall(r'rel="(?:prev|next)" href="([^"]+)"', file.html):
            assert f"result/{neighbor}" in {page.name for page in fragments}
    for table, listed in (
        (overview_sections.results_table(overview), overview.results),
        (overview_sections.recent_table(overview), _recent_entries(overview)),
    ):
        assert "BODY OF" not in table
        for row in listed:
            panel = _row_popover(table, f"pop-result-{row.id.lower()}")
            assert f'data-row-pop-src="result/{row.id.lower()}.html"' in panel
            assert "Read the complete result record" in panel
            assert "<dl" not in panel


def test_result_preview_keeps_claim_scope_and_links_with_full_context_in_fragment(
    overview: overview_data.Overview, result_bodies: dict[str, str]
) -> None:
    """Table previews link to complete records retaining each claim and its context."""
    for result in overview.results:
        preview = overview_sections.result_row(result, trigger="row").popover
        full = result_bodies[result.id]
        assert f'href="{overview_sections.result_fragment(result.id)}"' in preview, result.id
        assert "Read the complete result record" in preview, result.id
        assert (
            overview_sections.prose_html(
                result.record["claim"], between='</p><p class="site-result-claim">'
            )
            in full
        ), result.id
        assert (
            overview_sections.prose_html(result.record["significance"]["rationale"]) in full
        ), result.id
        for link in result.records:
            assert f'href="{html.escape(link.url, quote=True)}"' in full, result.id
            label = html.escape(link.label)
            if link.url == "frontier.html":
                label = "The frontier survey"
            elif match := re.fullmatch(r"cases/(\d+)\.html", link.url):
                label = "Case record, " + overview_data.math_html(f"n = {match.group(1)}")
            elif match := re.fullmatch(r"evidence (\d+)", link.label):
                evidence = result.record["evidence"][int(match.group(1)) - 1]
                label = f"<code>{html.escape(evidence)}</code>"
            assert f">{label}</a>" in full, result.id
        assert f'data-novelty="{result.novelty}"' in full, result.id
        for key, label in (("composition", "Composition"), ("next_rung", "Next rung")):
            assert f"<dt>{label}</dt>" not in preview, result.id
            if result.record.get(key):
                assert f"<dt>{label}</dt>" in full, result.id
                assert overview_sections.prose_html(result.record[key]) in full, result.id


#: What the two pages that list results may weigh. The result overviews are 4.9 MB
#: between them; a page that carried them, as both once would have, crosses its ceiling.
#: The results page was 2.77 MB with 81 results on 3 October 2026, and its significance
#: column and legend added 43 KB that day (`think-m3m4`, `think-42dx`), which took it
#: past 2.8. The shell every page carried then, its faces and math, about 1.8 MB of each,
#: became the site's shared assets on 4 October 2026 (`site_assets`), which a page links
#: rather than carries, and each ceiling came down by as much, keeping the room it had:
#: the overview measured 2.32 MB that day and the results page 1.01 MB.
#: index.html's ceiling was 4,300,000 before that, and PR 305 raised it to 4,700,000 on
#: 2026-10-03 for the 51 regularized atlas drawings it inlines (285,963 bytes): its merge
#: with main then rendered the page at 4,448,100 bytes. Lowered by the same 1.8 MB, that
#: is 2,900,000 here; the merge of main into PR 305 on 2026-10-04 rendered the page at
#: 2,670,052 bytes, over 2,500,000 by less than the drawings weigh. The owner dropped the
#: choice of drawing that day (think-k8x9): a regularized case is drawn once, from its
#: view, and its house drawing no longer ships, which rendered the page at 2,404,813
#: bytes with the new-result stars, and the ceiling is 2,500,000 again, without the
#: fetch think-yozo planned for the second drawings. The results' short rows took both
#: past it on 6 October: 2,548,891 and 1,200,769 bytes with the six results of that
#: morning, and 2,680,770 and 1,332,411 with wand125's ten check2 results after them,
#: about 13 KB a result on each page. Each ceiling keeps about a hundred kilobytes above
#: the second measurement. Merged with main's T-101 the same day, as T-102 to T-111, they
#: measured 2,727,614 and 1,379,239 bytes, above both earlier ceilings and about 70 KB
#: under these.
PAGE_CEILINGS = {"index.html": 600_000, render_overview.RESULTS_PAGE: 800_000}


def test_no_page_carries_a_result_overview(
    page: str, results: str, overview: overview_data.Overview
) -> None:
    """A result's overview is fetched when its row is opened, never written into a page:
    the two pages that list results hold only each row's short detail and the address
    of its overview, and stay under their ceilings. The overviews are served from one
    directory that no page's address shadows."""
    for name, html_text in (("index.html", page), (render_overview.RESULTS_PAGE, results)):
        assert "data-result-overview=" not in html_text, name
        assert 'class="site-result"' not in html_text, name
        size = len(html_text.encode("utf-8"))
        print(f"{name}: {size:,} source bytes / {PAGE_CEILINGS[name]:,} ceiling")
        assert size < PAGE_CEILINGS[name], f"{name} is {size:,} bytes"
    sources = re.findall(r'data-row-pop-src="([^"]+)"', results)
    assert sources == [
        overview_sections.result_fragment(result.id)
        for result in overview_sections.recent_results(overview)
    ]
    assert set(re.findall(r'data-row-pop-src="([^"]+)"', page)) == {
        overview_sections.result_fragment(result.id) for result in _recent_entries(overview)
    }
    directory = overview_sections.RESULT_FRAGMENTS
    assert directory == "result"
    served = {
        name.split("/", 1)[0].removesuffix(".html") for name in render_overview.SITE_PAGES
    }
    assert directory not in served
    assert render_overview.ROW_POPOVER_SCRIPT.read_text(encoding="utf-8").count(
        "data-row-pop-src"
    )


def test_the_site_writes_each_result_overview_once_and_drops_a_withdrawn_one(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`write_site` writes the pages at the root and the fragments in their directory,
    and removes a fragment a directory built earlier still holds for a result the
    register no longer has; nothing else in the directory is touched."""
    files = [
        render_overview.Page("index.html", "<p>page</p>"),
        render_overview.Page("result/t-001.html", "<p>one</p>\n"),
    ]
    (tmp_path / "result").mkdir()
    (tmp_path / "result" / "t-999.html").write_text("withdrawn", encoding="utf-8")
    paper = tmp_path / overview_sections.LOWER_BOUNDS_PAPER
    paper.parent.mkdir()
    paper.write_text("another build's", encoding="utf-8")
    render_overview.write_site(tmp_path, files)
    assert sorted(
        path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*.html")
    ) == sorted(
        [
            "404.html",
            "index.html",
            "papers/n11-lower-bounds-explainer.html",
            "result/t-001.html",
            *(row.path for row in site_urls.load_registry() if row.status == "withdrawn"),
        ]
    )
    assert (tmp_path / "result" / "t-001.html").read_text(encoding="utf-8") == "<p>one</p>\n"
    monkeypatch.setattr(render_overview, "render_all", lambda: files[:1])
    monkeypatch.setattr(render_overview, "result_fragments", lambda: files[1:])
    monkeypatch.setattr(render_overview, "case_records", list)
    forwarder = render_overview.Page("old.html", "<p>moved</p>")
    monkeypatch.setattr(render_overview, "forwarder_pages", lambda: [forwarder])
    assert [file.name for file in render_overview.render_site()] == [
        "index.html",
        "result/t-001.html",
        "old.html",
    ]
    # A forwarder is one of the files a render writes, so a build without it is stale.
    assert render_overview.main(["--output", str(tmp_path), "--check"]) == 1
    render_overview.write_site(tmp_path, [*files, forwarder])
    assert render_overview.main(["--output", str(tmp_path), "--check"]) == 0
    (tmp_path / "result" / "t-001.html").write_text("changed", encoding="utf-8")
    assert render_overview.main(["--output", str(tmp_path), "--check"]) == 1


def test_check_finds_a_record_file_or_overview_left_from_another_build(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`--check` holds the directories the site writes whole, `result/` and `cases/`, to
    a fresh render: a file a later build would remove, a case dropped or a result
    withdrawn since, makes the build stale, as a missing or changed one does."""
    files = [
        render_overview.Page("index.html", "<p>page</p>"),
        render_overview.Page("cases/index.html", "<p>records</p>"),
    ]
    records = [render_overview.Page("cases/11.html", "<p>eleven</p>")]
    monkeypatch.setattr(render_overview, "render_all", lambda: files)
    monkeypatch.setattr(render_overview, "result_fragments", list)
    monkeypatch.setattr(render_overview, "case_records", lambda: records)
    monkeypatch.setattr(render_overview, "forwarder_pages", list)
    assert render_overview.main(["--output", str(tmp_path)]) == 0
    assert render_overview.main(["--output", str(tmp_path), "--check"]) == 0
    (tmp_path / "cases" / "325.html").write_text("a dropped case", encoding="utf-8")
    assert render_overview.main(["--output", str(tmp_path), "--check"]) == 1
    render_overview.write_site(tmp_path, [*files, *records])
    assert not (tmp_path / "cases" / "325.html").exists()
    assert render_overview.main(["--output", str(tmp_path), "--check"]) == 0


def test_a_result_row_popover_is_the_same_panel_in_both_tables(
    overview: overview_data.Overview,
) -> None:
    """A result's popover is the same panel on both pages, a card's: the id as its caps
    label and the summary as its headline. Every statically selected recent row opens
    the same complete-record link, close control and panel in both tables."""
    entries = _recent_entries(overview)
    assert entries
    recent_table = overview_sections.recent_table(overview)
    results_table = overview_sections.results_table(overview)
    for result in entries:
        target = f"pop-result-{result.id.lower()}"
        away = _row_popover(recent_table, target)
        here = _row_popover(results_table, target)
        face = overview_sections.headline_math_face(
            overview_sections.tex_bounds(result.summary)
        )
        for panel in (away, here):
            assert f'<span class="site-card-label">{result.id}</span>' in panel
            assert f'<p class="site-popover-value"{face} id="{target}-title">' in panel
            assert 'popovertargetaction="hide" aria-label="Close">' in panel
        assert ACTION.findall(away)
        assert ACTION.findall(here)
        assert "in the results table" not in away
        assert away == here


def test_a_row_detail_escapes_its_words_and_keeps_its_html() -> None:
    """`row_detail` is the component: the row's attributes, its native trigger and its
    popover. The name, the label and the action's words are escaped; the trigger, the
    headline and the body are HTML and pass through."""
    detail = overview_sections.row_detail(
        "pop-x",
        name='a < b & "c"',
        trigger="<b>key</b>",
        label="A & B",
        title="<i>title</i>",
        body="<p>body</p>",
        action=("other.html#x", "Go <there>"),
    )
    assert detail.attributes == (
        'data-row-popover="pop-x" aria-label="a &lt; b &amp; &quot;c&quot;"'
    )
    assert detail.trigger == (
        '<button type="button" class="site-row-open" popovertarget="pop-x"><b>key</b></button>'
    )
    assert detail.popover.startswith(
        '<div class="site-popover site-row-pop" id="pop-x" popover role="dialog" '
        'aria-labelledby="pop-x-title">'
    )
    assert '<span class="site-card-label">A &amp; B</span>' in detail.popover
    assert 'id="pop-x-title"><i>title</i></p>' in detail.popover
    assert '<div class="site-row-pop-body"><p>body</p></div>' in detail.popover
    assert (
        '<a class="site-popover-action" href="other.html#x" data-go="page">Go &lt;there&gt;</a>'
    ) in detail.popover
    plain = overview_sections.row_detail(
        "pop-y", name="n", trigger="k", label="l", title="t", body="b"
    )
    assert "site-popover-actions" not in plain.popover
    assert "<template" not in plain.popover
    assert "data-row-pop-src" not in plain.popover
    assert overview_sections.plain_text("`s(11) >= 3`,  reported") == "s(11) >= 3, reported"


def test_a_deferred_row_body_waits_in_a_template_with_a_fallback_for_no_scripts(
    overview: overview_data.Overview,
) -> None:
    """A body too heavy to render once per row at load is held in a `<template>`, which
    `row-popover.js` places when the popover first opens (`tests/node/overview_rows`),
    with a `<noscript>` beside it for a reader whose template would stay inert. A body
    too heavy to carry at all is named instead (`source`), with the short form in its
    place for the script to replace; a body is one or the other. The result rows take
    the second way, on both tables, so neither holds a template."""
    held = overview_sections.row_detail(
        "pop-z",
        name="n",
        trigger="k",
        label="l",
        title="t",
        body="<p>long</p>",
        deferred=True,
        fallback="<p>short</p>",
    )
    assert (
        '<div class="site-row-pop-body"><template data-row-pop-body><p>long</p></template>'
        "<noscript><p>short</p></noscript></div>"
    ) in held.popover
    bare = overview_sections.row_detail(
        "pop-z", name="n", trigger="k", label="l", title="t", body="<p>long</p>", deferred=True
    )
    assert "<noscript>" not in bare.popover
    named = overview_sections.row_detail(
        "pop-z",
        name="n",
        trigger="k",
        label="l",
        title="t",
        body="<p>short</p>",
        source="beside/z.html?a=1&b=2",
    )
    assert (
        '<div class="site-row-pop-body" data-row-pop-src="beside/z.html?a=1&amp;b=2">'
        "<p>short</p></div>"
    ) in named.popover
    with pytest.raises(SystemExit, match="in a template or is fetched, not both"):
        overview_sections.row_detail(
            "pop-z",
            name="n",
            trigger="k",
            label="l",
            title="t",
            body="b",
            deferred=True,
            source="z",
        )
    for table in (
        overview_sections.results_table(overview),
        overview_sections.recent_table(overview),
    ):
        assert "<template" not in table
        assert table.count("data-row-pop-src=") == table.count(
            '<div class="site-popover site-row-pop"'
        )


def test_a_row_with_detail_takes_the_shared_wash_and_no_disclosure_style() -> None:
    """The row's hover wash is the shared table rule's; a row with detail, and a
    frontier row, which opens its case's record (think-necq), keeps it on keyboard
    focus, with a ring, and while its popover is open, and shows the pointer once its
    script has made it the control. No rule styles a `<details>` in a table."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    hover = css[css.index(".kpress .site-table tbody tr:hover {") :]
    assert "background: var(--site-wash);" in hover[: hover.index("}")]
    held = _rule(
        css,
        ".kpress\n  .site-table\n  tbody\n  tr:is([data-row-popover], [data-case-row])"
        ':is(:focus-visible, [aria-expanded="true"])',
    )
    assert "background: var(--site-wash);" in held
    ring = _rule(
        css,
        ".kpress .site-table tbody tr:is([data-row-popover], [data-case-row]):focus-visible",
    )
    assert "outline: 2px solid var(--kpress-doc-accent);" in ring
    ready = _rule(
        css, ".kpress .site-table tbody tr:is([data-row-ready], [data-case-row][aria-controls])"
    )
    assert "cursor: pointer;" in ready
    trigger = css[css.index(".kpress .site-table .site-row-open {") :]
    for declaration in ("background: none;", "border: 0;", "color: inherit;", "font: inherit;"):
        assert declaration in trigger[: trigger.index("}")], declaration
    assert not re.search(r"\.site-(?:table|frontier)[^{}]*\b(?:details|summary)\b[^{}]*\{", css)


# ---------- Result filters: one bar on both tables of results (think-3pi5) ----------

#: The bar's controls, in its order: the row attribute each filters and how.
RESULT_FILTERS = [
    ("s", "min"),
    ("v", "min"),
    ("c", "min"),
    ("kind", ""),
    ("status", ""),
    ("current", ""),
    ("source", ""),
    ("n", "covers"),
    ("date", "age"),
    # The two preset-only controls, out of the bar until a link sets them: the listed
    # project a row is attributed to, and its significance exactly.
    ("project", "has"),
    ("s", ""),
]

#: The bar's one checkbox, as `result_filters` writes it: its own label, after Status.
HIDE_SUPERSEDED = (
    '<label><input type="checkbox" data-filter="current"{checked}> Hide superseded</label>'
)

_COUNT = re.compile(r'(<span class="site-count"[^>]*>)[^<]*</span>')
_SELECTED = re.compile(
    r'<select data-filter="([a-z]+)"(?![^>]*data-preset)[^>]*>'
    r'(?:<option value="[^"]*">[^<]*</option>)*<option value="([^"]*)" selected>'
)


def _filter_bar(page: str) -> str:
    """A results table's tools bar as the page carries it, from its tag to its close."""
    match = re.search(
        r'<div class="site-table-tools site-result-filters">.*?</div>', page, re.DOTALL
    )
    assert match
    return match.group(0)


def _controls(bar: str) -> list[tuple[str, str]]:
    """Each control's row attribute and bound, in the bar's order."""
    found = []
    for attributes in re.findall(r"<(?:select|input)\b([^>]*)>", bar):
        key = re.search(r'data-filter="([^"]+)"', attributes)
        bound = re.search(r'data-bound="([^"]+)"', attributes)
        assert key, attributes
        found.append((key[1], bound[1] if bound else ""))
    return found


def _without_defaults(bar: str) -> str:
    """A bar less what is a table's own: its count, which option each select starts at,
    the value an input starts with and whether its checkbox starts checked."""
    bar = _COUNT.sub(r"\1</span>", bar).replace(" selected>", ">").replace(" checked>", ">")
    return re.sub(r'(<input\b[^>]*?) value="[^"]*"', r"\1", bar)


def test_both_tables_of_results_carry_the_identical_filter_set(page: str, results: str) -> None:
    """The complete table exposes every filter while the static subset links to it."""
    assert "data-filter=" not in page.split('id="recent-results"', 1)[1].split("<h2", 1)[0]
    assert 'href="all-results.html" data-all-results' in page
    bar = _filter_bar(results)
    assert _controls(bar) == RESULT_FILTERS
    assert dict(_SELECTED.findall(bar)) == {
        "s": "",
        "v": "",
        "c": "",
        "kind": "",
        "status": "",
        "source": "",
    }
    assert HIDE_SUPERSEDED.format(checked="") in bar
    assert bar.count(" selected>") == bar.count("<select ") == 8
    assert bar.count("<input ") == 3


def test_the_filter_bar_is_one_helpers_and_reads_the_whole_register(
    overview: overview_data.Overview,
) -> None:
    """`result_filters` writes the bar for both tables, each passing where its own
    starts. Its choices come from the whole register, so a table that lists fewer
    results offers the same ones; only its count is the table's. Each rung select offers
    the rubric's levels above the lowest as floors, the top one bare."""
    recent = overview_sections.recent_results(overview)
    assert sorted(r.id for r in recent) == sorted(r.id for r in overview.results)
    assert [r.id for r in recent] == [
        r.id
        for r in sorted(
            overview.results,
            key=lambda r: (overview_sections.first_day(r.dated[1]), r.id),
            reverse=True,
        )
    ]
    every = overview_sections.RESULTS_DEFAULTS
    full = overview_sections.result_filters(overview, overview.results, every)
    part = overview_sections.result_filters(overview, recent, overview_sections.RECENT_DEFAULTS)
    few = overview_sections.result_filters(overview, recent[:3], every)
    assert full in overview_sections.results_table(overview)
    assert part not in overview_sections.recent_table(overview)
    assert "data-filter=" not in overview_sections.recent_table(overview)
    assert few.endswith(">3 results</span></div>")
    assert _COUNT.sub("", full) == _COUNT.sub("", few)
    assert _without_defaults(full) == _without_defaults(part)
    for defaults in (every, overview_sections.RECENT_DEFAULTS):
        assert overview_sections.result_filters(overview, [], defaults).endswith(
            ">0 results</span></div>"
        )
    assert overview_sections.rung_options("S") == [
        ("", "All"),
        ("2", "S2 and up"),
        ("3", "S3 and up"),
        ("4", "S4 and up"),
        ("5", "S5"),
    ]
    for scale in "VC":
        choices = overview_sections.rung_options(scale)
        assert choices[0] == ("", "All")
        assert choices[1] == ("1", f"{scale}1 and up")
        assert choices[-1] == ("5", f"{scale}5")
    statuses = re.search(r'<select data-filter="status">(.*?)</select>', full)
    assert statuses
    assert set(re.findall(r'<option value="([^"]+)"', statuses[1])) == {
        result.status for result in overview.results
    }
    # Kind offers the kinds the register holds, in the rubric's order and words.
    kinds = re.search(r'<label>Kind <select data-filter="kind">(.*?)</select>', full)
    assert kinds
    held = {result.record["kind"] for result in overview.results}
    assert re.findall(r'<option value="([^"]*)"[^>]*>([^<]*)</option>', kinds[1]) == [
        ("", "All"),
        *(
            (kind, check_results.kind_label(kind))
            for kind in check_results.KINDS
            if kind in held
        ),
    ]
    assert f' min="1" max="{max(overview.cases)}" ' in full
    assert 'data-bound="age" min="0" placeholder="any"> days</label>' in full
    assert 'data-bound="age" min="0" placeholder="any" value="180"> days</label>' in part
    assert overview_sections.count_text(3, 3) == "3 results"
    assert overview_sections.count_text(2, 3) == "2 of 3 results"


def _facets(tag: str) -> dict[str, str]:
    """A row's `data-*` attributes but for the two that name it and its popover."""
    found = dict(re.findall(r'\sdata-([a-z-]+)="([^"]*)"', tag))
    return {key: value for key, value in found.items() if key not in {"result", "row-popover"}}


def test_every_facet_a_result_row_carries_has_a_filter_and_every_filter_a_facet(
    page: str, results: str, overview: overview_data.Overview
) -> None:
    """A row of either table carries the same facets, each from the register: whose
    result it is, its V, C and S levels, its kind, the listed projects it is attributed
    to, its status, whether it is current, which is to say not superseded, its cases and
    its date. The bar has a control for each and no control without one."""
    filtered = {key for key, _ in RESULT_FILTERS}
    recent = _recent_table(page)
    listed = {r.id for r in _recent_entries(overview)}
    for result in overview.results:
        record = result.record
        expected = {
            "source": "ours" if result.ours else "others",
            "v": record["verification"][1:],
            "c": record["confirmation"][1:],
            "s": str(record["significance"]["score"]),
            "kind": record["kind"],
            "project": " ".join(overview_sections.result_projects(result)),
            "status": result.status,
            "current": "false" if overview_sections.is_superseded(result) else "true",
            "n": overview_sections.result_cases(result),
            "date": overview_sections.first_day(result.dated[1]),
        }
        assert set(expected) == filtered
        tags = [_row(results, result.id).split(">", 1)[0]]
        if result.id in listed:
            tags.append(_recent_row(recent, result.id).split(">", 1)[0])
        for tag in tags:
            assert _facets(html.unescape(tag)) == expected, result.id
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", expected["date"]), result.id
        assert re.fullmatch(r"\d+(?:-\d+)?(?: \d+(?:-\d+)?)*", expected["n"]), result.id


def test_a_results_cases_and_date_are_written_for_the_filters() -> None:
    """A result's cases are a list of counts and ranges, and a date the register gives
    to the year or the month is the first day of it, so both order as the script reads
    them."""

    def cases(scope: dict) -> str:
        record = {"id": "T-900", "scope": scope}
        result = overview_data.Result(record, group="", credit="", ours=True)
        return overview_sections.result_cases(result)

    assert cases({"n_values": [11]}) == "11"
    assert cases({"n_values": [17, 18]}) == "17 18"
    assert cases({"n_values": [26, 18, 19, 20, 21]}) == "18-21 26"
    assert cases({"n_min": 1, "n_max": 100}) == "1-100"
    assert overview_sections.first_day("1979") == "1979-01-01"
    assert overview_sections.first_day("2005-03") == "2005-03-01"
    assert overview_sections.first_day("2026-09-04") == "2026-09-04"


def test_the_results_page_starts_with_every_result_showing(
    results: str, overview: overview_data.Overview
) -> None:
    """The results page's bar starts with Significance at All, no maximum age and
    Hide superseded clear, so no row is `hidden` in its HTML and its count is the whole
    register's."""
    for result in overview.results:
        tag = _row(results, result.id).split(">", 1)[0] + ">"
        assert not tag.endswith(" hidden>"), result.id
    assert f">{len(overview.results)} results</span>" in _filter_bar(results)
    assert HIDE_SUPERSEDED.format(checked="") in _filter_bar(results)
    text = " ".join(re.sub(r"<[^>]+>", "", results).split())
    assert "The table starts with every result showing, newest first." in text
    assert "case and age, and they combine." in text
    assert "starts filtered" not in text


def test_hide_superseded_starts_checked_on_the_overview_and_clear_on_the_results_page(
    page: str, results: str, overview: overview_data.Overview
) -> None:
    """Superseded entries are omitted from the recent subset and retained in the full table."""
    assert overview_sections.RECENT_DEFAULTS.hide_superseded is True
    assert overview_sections.RESULTS_DEFAULTS.hide_superseded is False
    assert HIDE_SUPERSEDED.format(checked="") in _filter_bar(results)
    recent = _recent_table(page)
    for result in overview.results:
        superseded = overview_sections.is_superseded(result)
        flag = f'data-current="{"false" if superseded else "true"}"'
        assert flag in _row(results, result.id).split(">", 1)[0]
        if f'data-result="{result.id.lower()}"' in recent:
            assert not superseded
            assert flag in _recent_row(recent, result.id).split(">", 1)[0]
    assert len(_recent_entries(overview)) < len(overview.results)


def test_rows_outside_a_tables_defaults_are_hidden_in_the_html_and_stay_in_it(
    overview: overview_data.Overview,
) -> None:
    """Under defaults that hide rows, as the overview's are, a row outside them is
    `hidden` in the HTML, never left out of it, and the count is written for the rows
    left, so the first paint is the filtered table. Both tables are the one table, so
    the results page's is rendered here under the overview's defaults."""
    defaults = overview_sections.RECENT_DEFAULTS
    reference = overview_sections.reference_date(overview)
    table = overview_sections.results_table(overview, defaults)
    shown = 0
    for result in overview.results:
        tag = _row(table, result.id).split(">", 1)[0] + ">"
        keeps = overview_sections.shown_by_default(result, defaults, reference)
        assert tag.endswith(" hidden>") == (not keeps), result.id
        shown += keeps
    assert 0 < shown < len(overview.results)
    assert f"{shown} of {len(overview.results)} results</span>" in _filter_bar(table)
    assert table.count("<tr ") == len(overview.results)


def test_a_row_named_by_the_address_shows_whatever_the_filters_hide() -> None:
    """A link to a result's row (`all-results.html#t-048`) must land on the row even
    when the default filter hides it. With scripts `table.js` keeps the row the fragment
    names, which `tests/node/overview_table/filters.test.mjs` runs; without them one
    rule shows a hidden row that is the target, as a table row and, on a phone, as the
    card a results row is there. A targeted row takes the wash in every site table."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    hidden = css[css.index("\n.site-table tr[hidden] {") :]
    assert "display: none;" in hidden[: hidden.index("}")]
    target = css[css.index("\n.site-table tr[hidden]:target {") :]
    assert "display: table-row;" in target[: target.index("}")]
    assert css.index("\n.site-table tr[hidden] {") < css.index(
        "\n.site-table tr[hidden]:target {"
    )
    phone = css[css.index("  .site-results tr[hidden]:target {") :]
    assert "display: grid;" in phone[: phone.index("}")]
    wash = css[css.index("\n.kpress .site-table tbody tr:target {") :]
    assert "background: var(--site-wash);" in wash[: wash.index("}")]


def test_without_scripts_no_row_stays_filtered() -> None:
    """A reader without scripts cannot change a filter, so the default must not hide
    anything from them: under `scripting: none` every row shows, as a table row or, on a
    phone, as the results table's card, and the bar, which would do nothing, is not
    shown."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    block = css[css.index("\n@media (scripting: none) {") :]
    block = block[: block.index("\n}\n")]
    assert ".site-result-filters {\n    display: none;" in block
    assert ".site-table tbody tr[hidden] {\n    display: table-row;" in block
    phone = css[css.index("\n@media (scripting: none) and (width < 40rem) {") :]
    phone = phone[: phone.index("\n}\n")]
    assert ".site-results tbody tr[hidden] {\n    display: grid;" in phone


def test_secondary_cell_content_is_quiet(results: str) -> None:
    """What a credit builds on, in a table of results, and a finder under a frontier
    bound take the one quiet style: the support colour in the sans face."""
    from devtools.render_frontier_page import frontier_cases, table_html  # noqa: PLC0415

    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    rule = css[css.index("\n.site-cell-quiet {") :]
    rule = rule[: rule.index("}")]
    assert "color: var(--site-support-color);" in rule
    assert "font-family: var(--kpress-font-sans);" in rule
    assert '<span class="site-cell-quiet">after ' in results
    assert "site-col-credit site-cell-quiet" not in results
    assert 'class="site-frontier-note site-cell-quiet"' in table_html(frontier_cases())


def _old_addresses() -> set[str]:
    """Every address a paper used to have, in every form a link may take: its path under
    the site's root, its directory where it was a directory's index, and either as an
    address on the deployed site."""
    old = {
        *(old for old, _ in render_overview.MOVED_PAGES),
        *(old.removesuffix("index.html") for old, _ in render_overview.MOVED_PAGES),
        *(old for old, _ in render_overview.MOVED_FILES),
    }
    return old | {render_overview.SITE_URL + address for address in old}


def test_a_paper_is_named_by_its_slug_in_the_source_and_on_the_site() -> None:
    """`conventions.md`: a paper has one name, its slug, which says the case, the subject
    and the kind of paper. The site serves it at `papers/<slug>.html`; the registry
    connects that address to its renderer, templates, tests and Pages scope. The methods
    survey retains its private packing_methods module and packing-methods templates."""
    import importlib  # noqa: PLC0415

    from devtools.pages_scope import BUILDER_INPUTS, load_workflow  # noqa: PLC0415

    slugs = tuple(paper.slug for paper in render_overview.PAPERS)
    assert slugs == (
        "n11-lower-bounds-explainer",
        "n11-threshold-bound-review",
        "n11-optimality-review",
        "square-packing-methods-survey",
    )
    packing = overview_data.REPO / "packing"
    jobs = load_workflow()["jobs"]
    skip_notices = next(
        step["run"]
        for step in jobs["scope"]["steps"]
        if step.get("name") == "Say why each skipped page is not built"
    )
    for slug in slugs:
        name = slug.replace("-", "_")
        private_name = "packing_methods" if slug == render_overview.PACKING_METHODS else name
        assert render_overview.paper_record(slug).module == f"devtools.render_{private_name}"
        renderer = importlib.import_module(render_overview.paper_record(slug).module)
        assert render_overview.paper_record(slug).title == renderer.TITLE
        assert slug == renderer.SLUG
        assert renderer.SITE_PATH == render_overview.paper_path(slug) == f"papers/{slug}.html"
        assert renderer.SITE_PATH in render_overview.SITE_PAGES
        assert renderer.SITE_ROOT == render_overview.PAPERS_ROOT == "../"
        assert renderer.SITE_PATH in {paper.href for paper in overview_sections.PAPERS}
        template_name = private_name.replace("_", "-")
        for template in (f"{template_name}-article.md", f"{template_name}-shell.html"):
            assert (render_overview.TEMPLATES / template).is_file(), template
        tests = packing / "tests"
        assert (tests / f"test_render_{private_name}.py").is_file() or (
            tests / f"test_{private_name}.py"
        ).is_file(), slug
        assert name in BUILDER_INPUTS, slug
        assert name in {line.split(" ", 1)[0] for line in skip_notices.splitlines()}, slug
    assert render_overview.paper_path("a-b", ".pdf") == "papers/a-b.pdf"


def test_each_address_a_paper_had_serves_a_forwarder_to_where_it_is() -> None:
    """A page that moved leaves a forwarder at its old address (`MOVED_PAGES`), so no
    link written before the move breaks. The forwarder names where the page is now four
    times, and they agree: as its canonical URL, in full; to the forwarding script, on
    the root element; in a refresh for a reader without scripts, inside `<noscript>` so
    it cannot outrun the script and drop the fragment; and in a link. It carries the
    overview's own forwarding script whole, the paper's preview by the paper's own title
    (`render_overview.forwarder_head`), and nothing else of a site page: no bar, no
    stamp, no stylesheet. `check_published_site` reads a deployed one the same way."""
    from devtools import check_published_site  # noqa: PLC0415
    from devtools import render_n11_lower_bounds_explainer as explainer  # noqa: PLC0415
    from devtools import render_n11_optimality_review as review  # noqa: PLC0415

    forwarders = {
        forwarder.name: forwarder.html for forwarder in render_overview.forwarder_pages()
    }
    assert list(forwarders) == [old for old, _ in render_overview.MOVED_PAGES]
    papers = {
        old: new
        for old, new in render_overview.MOVED_PAGES
        if new.startswith(f"{render_overview.PAPERS_DIR}/")
    }
    assert papers == {
        "explainer.html": "papers/n11-lower-bounds-explainer.html",
        "n11-optimality/t-060-explainer.html": "papers/n11-optimality-review.html",
        "n11-optimality/index.html": "papers/n11-optimality-review.html",
    }
    script = render_overview.FORWARD_SCRIPT.read_text(encoding="utf-8")
    titles = {explainer.SITE_PATH: explainer.TITLE, review.SITE_PATH: review.TITLE}
    for old, new in papers.items():
        page = forwarders[old]
        assert new in render_overview.SITE_PAGES, new
        assert old not in render_overview.SITE_PAGES, old
        assert old not in render_overview.PAGES, old
        says = check_published_site.forwarder_says(page)
        assert says == check_published_site.forwarder_expected(old, new), old
        assert says["canonical"] == render_overview.SITE_URL + new
        climbs = "../" * old.count("/")
        assert says["script"] == f"{climbs}{new}"
        assert page.count(f"<script>{script}</script>") == 1
        assert page.count("<script") == 3  # The executable forwarder plus two JSON-LD records.
        refresh = (
            f'<noscript><meta http-equiv="refresh" content="0; url={climbs}{new}"></noscript>'
        )
        assert refresh in page
        title = titles[new]
        assert f"<title>{html.escape(title, quote=False)}</title>" in page
        assert f'<meta property="og:title" content="{html.escape(titles[new])}">' in page
        assert f">{html.escape(titles[new])}</a>.</p>" in page
        assert "site-nav" not in page
        assert "<style" not in page
        assert len(page) < 10_000, "a forwarder and metadata remain small"
        # It fetches nothing, not even the shared assets a site page links.
        render_overview.assert_fetches_only_assets(old, page)
        assert f"{site_assets.ASSETS_DIR}/" not in page, old
    # The script reads the root element's `data-moved-to`.
    assert "movedTo" in script


def test_each_file_that_moved_is_a_papers_markdown_or_pdf_under_its_slug() -> None:
    """A file that moved and cannot forward is served at its old address as a copy
    (`MOVED_FILES`): each paper's Markdown and PDF, which now sit beside the page under
    its slug. The copies are made when the site is assembled, by the workflow's
    `publish` job and by `preview_site.copy_moved_files`."""
    assert dict(render_overview.MOVED_FILES) == {
        "t-018-explainer.md": "papers/n11-lower-bounds-explainer.md",
        "t-018-explainer.pdf": "papers/n11-lower-bounds-explainer.pdf",
        "n11-optimality/t-060-explainer.md": "papers/n11-optimality-review.md",
        "n11-optimality/t-060-explainer.pdf": "papers/n11-optimality-review.pdf",
    }
    pages = {new for _, new in render_overview.MOVED_PAGES}
    for old, new in render_overview.MOVED_FILES:
        assert Path(old).suffix == Path(new).suffix in {".md", ".pdf"}
        assert str(Path(new).with_suffix(".html")) in pages, new


def test_no_page_links_an_address_a_paper_used_to_have(
    rendered: Callable[[str], str], result_bodies: dict[str, str]
) -> None:
    """Every link on the site goes to a paper where it is served, never through a
    forwarder: the bar, the cards, the Papers introduction, a result's overview, and
    the reader documents, whose links to the site are written in full. A link to the
    directory the optimality paper was in, to an old Markdown or PDF, and to the
    deployed site's own old address are all found, which a pattern over the pages' paths
    alone (`test_site_documents`) does not read."""
    old = _old_addresses()
    assert "explainer.html" in old
    assert "n11-optimality/" in old
    assert "https://jlevy.github.io/squares/n11-optimality/t-060-explainer.pdf" in old
    bodies = {name: rendered(name) for name in render_overview.PAGES}
    bodies |= {f"the overview of {result}": body for result, body in result_bodies.items()}
    for name, body in bodies.items():
        links = {
            html.unescape(link).partition("#")[0].partition("?")[0]
            for link in re.findall(r'\b(?:href|src|data-pop-src|poster)="([^"]+)"', body)
        }
        assert not links & old, (name, sorted(links & old))
    # The papers are linked, where they are served, from the pages that card them.
    for name in ("index.html", "papers.html"):
        for paper in (overview_sections.OPTIMALITY_PAPER, overview_sections.LOWER_BOUNDS_PAPER):
            assert f'href="{paper}"' in bodies[name], (name, paper)


def test_the_site_writes_its_forwarders_and_checks_them(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`render_overview` writes the forwarders with the pages, each in the directory its
    old address was in, and `--check` holds them to a fresh render as it holds a page."""
    page = render_overview.Page("index.html", "<p>page</p>")
    monkeypatch.setattr(render_overview, "render_all", lambda: [page])
    monkeypatch.setattr(render_overview, "result_fragments", list)
    monkeypatch.setattr(render_overview, "case_records", list)
    moved = [old for old, _ in render_overview.MOVED_PAGES]
    assert [file.name for file in render_overview.render_site()] == ["index.html", *moved]
    assert {"explainer.html", "n11-optimality/index.html"} < set(moved)
    assert render_overview.main(["--output", str(tmp_path)]) == 0
    crawl, crawl_assets = site_urls.crawl_files()
    assert set(crawl) == {
        "404.html",
        "sitemap.xml",
        *(row.path for row in site_urls.load_registry() if row.status == "withdrawn"),
    }
    assert sorted(
        path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*") if path.is_file()
    ) == sorted(
        [
            "index.html",
            *moved,
            *render_overview.support_files(),
            *crawl,
            *(f"{site_assets.ASSETS_DIR}/{name}" for name in crawl_assets),
        ]
    )
    assert render_overview.main(["--output", str(tmp_path), "--check"]) == 0
    (tmp_path / "explainer.html").write_text("an old page", encoding="utf-8")
    assert render_overview.main(["--output", str(tmp_path), "--check"]) == 1
    (tmp_path / "explainer.html").unlink()
    assert render_overview.main(["--output", str(tmp_path), "--check"]) == 1


def test_a_cases_status_is_one_chip_wherever_it_is_drawn(
    rendered: Callable[[str], str], overview: overview_data.Overview, case_pages: dict[str, str]
) -> None:
    """A case's status, `proved` or `open`, is one chip (`case_status_chip`) on every page
    that draws it, the frontier table and the case records alike, and its fill is the
    status's own (the owner, 2026-10-02, `think-c19o`): no page marks a case with the
    accent tone it had before."""
    statuses = {case["status"] for case in overview.cases.values()}
    assert statuses == {"proved", "open"}
    records = case_pages
    shown = {
        "frontier.html": rendered("frontier.html"),
        # A record draws its own case's status: one solved case and one open one.
        "case records": records["cases/11.html"] + records["cases/29.html"],
    }
    for name, page in shown.items():
        assert 'data-tone="accent"' not in page, name
        drawn = re.findall(
            r'<span class="site-chip" data-case-status="(\w+)">(\w+)</span>', page
        )
        assert drawn, name
        assert all(attribute == word for attribute, word in drawn), name
        assert {word for _, word in drawn} == statuses, name
        for status in statuses:
            assert page.count(overview_sections.case_status_chip(status)) >= 1, (name, status)


def test_an_indexed_line_anchor_is_the_line_a_line_by_line_search_finds() -> None:
    """`LineIndex` searches a file once rather than line by line, and must land where the
    line-by-line search did for every id an overview links, so no anchor moves."""
    for path, key in ((overview_data.RESULTS, "results"), (overview_data.EVIDENCE, "evidence")):
        ids = [entry["id"] for entry in safe_load(path.read_text(encoding="utf-8"))[key]]
        lines = path.read_text(encoding="utf-8").splitlines()
        index = overview_data.LineIndex.read(path)
        assert ids
        for entry in ids:
            whole = re.compile(re.escape(f"id: {entry}") + r"(?![\w-])")
            expected = next(n for n, line in enumerate(lines, start=1) if whole.search(line))
            assert index.line_of(f"id: {entry}") == expected, (path.name, entry)
    with pytest.raises(SystemExit, match="has no line containing"):
        index.line_of("id: E-no-such-entry")


def test_a_line_link_finds_an_id_whole_and_not_as_the_start_of_a_longer_one() -> None:
    """`overview_data.line_link` anchors the first line naming an id whole: T-020's first
    evidence entry, `E-n020-fractional-certificate`, comes after the entry whose id it
    begins, `E-n020-fractional-certificate-97-20`, and its link pointed there until
    2026-10-04 (`think-46fw`)."""
    lines = overview_data.EVIDENCE.read_text(encoding="utf-8").splitlines()
    for entry in ("E-n020-fractional-certificate", "E-n020-fractional-certificate-97-20"):
        own = lines.index(f"  - id: {entry}") + 1
        assert overview_data.line_link(overview_data.EVIDENCE, f"id: {entry}").endswith(
            f"#L{own}"
        ), entry
    longer = lines.index("  - id: E-n020-fractional-certificate-97-20")
    assert longer < lines.index("  - id: E-n020-fractional-certificate")
