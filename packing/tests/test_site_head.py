"""What every page says of itself in its head, and the one card they all name.

`render_overview.head_tags` writes a page's title, description, canonical link and link
preview from a small record, for every page kind: the site's own pages, the papers
and the workbench. These hold the function, the pages it is rendered into here, the
checks the deployed site gets from `check_published_site`, and the card
`devtools.social_card` draws. The papers' and the workbench's own heads are held in
their modules' tests (`test_n11_lower_bounds_explainer`, `test_render_n11_optimality_review`,
`packages/workbench/tests/test_site_nav.py`).
"""

from __future__ import annotations

import html
import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

from devtools import (
    check_published_site,
    overview_sections,
    render_overview,
    rung_scale,
    site_documents,
    site_urls,
    social_card,
)
from devtools.check_published_site import (
    REQUIRED_META,
    forwarder_problems,
    head_checks,
    head_problems,
    local_head_checks,
    read_head,
    shared_descriptions,
)
from devtools.render_frontier_page import packing_svg
from devtools.render_overview import (
    DESCRIPTION_LIMIT,
    PROJECT_NAME,
    SITE_URL,
    SOCIAL_CARD,
    SOCIAL_CARD_HEIGHT,
    SOCIAL_CARD_WIDTH,
    PageMeta,
    canonical_url,
    favicon_html,
    head_tags,
    page_title,
)
from sqpack.probes import probe
from tests import site_renders
from tests.site_renders import prepared_forwarders

pytestmark = pytest.mark.usefixtures(prepared_forwarders.__name__)

RESULTS = PageMeta(
    name="Every Result",
    description="Every reviewed result, with its claim, its credit and its ratings.",
    path="all-results.html",
)


def document(head: str) -> str:
    """A page around a head and the site's icon, as the reader meets one."""
    return (
        f'<!doctype html><html lang="en"><head>{head}{favicon_html()}</head>'
        "<body><p>Text</p></body></html>"
    )


@pytest.fixture(scope="module")
def pages() -> dict[str, str]:
    """Every page `render_overview` builds, from the process's one render of each."""
    return site_renders.pages()


@pytest.fixture(scope="module")
def card() -> bytes:
    return social_card.card_png()


def test_head_tags_writes_each_tag_once_from_a_page_record() -> None:
    """One record gives the whole set: the title, the description, the canonical link,
    Open Graph and Twitter, each once, the addresses in full under the published root."""
    head = read_head(document(head_tags(RESULTS)))
    url = SITE_URL + "all-results.html"
    assert head.titles == ("Every Result · The Squares Project",)
    assert head.link("canonical") == [url]
    assert [key for key, _ in head.metas] == ["description", "robots", *REQUIRED_META[1:]]
    assert dict(head.metas) == {
        "description": RESULTS.description,
        "robots": "max-image-preview:large",
        "og:type": "website",
        "og:site_name": "The Squares Project",
        "og:locale": "en_US",
        "og:title": "Every Result",
        "og:description": RESULTS.description,
        "og:url": url,
        "og:image": SITE_URL + "social-card.png",
        "og:image:type": "image/png",
        "og:image:width": "1200",
        "og:image:height": "630",
        "og:image:alt": render_overview.social_card_alt(),
        "twitter:card": "summary_large_image",
        "twitter:title": "Every Result",
        "twitter:description": RESULTS.description,
        "twitter:image": SITE_URL + "social-card.png",
        "twitter:image:alt": render_overview.social_card_alt(),
    }
    assert head_problems(document(head_tags(RESULTS)), url) == []
    # Open Graph's tags are `property` and the rest are `name`, which consumers require.
    tags = head_tags(RESULTS)
    assert '<meta property="og:title" content="Every Result">' in tags
    assert '<meta name="twitter:title" content="Every Result">' in tags
    assert 'name="og:' not in tags
    assert 'property="twitter:' not in tags


def test_the_title_helper_does_not_repeat_the_formal_project_name() -> None:
    """Website titles add the project name once, including when it is the page's name."""
    assert page_title("Papers") == "Papers · The Squares Project"
    assert page_title(PROJECT_NAME) == PROJECT_NAME == "The Squares Project"
    head = read_head(
        document(head_tags(PageMeta(PROJECT_NAME, "The front door.", "index.html")))
    )
    assert head.titles == (PROJECT_NAME,)
    assert head.meta("og:title") == head.meta("og:site_name") == [PROJECT_NAME]
    assert head.link("canonical") == head.meta("og:url") == [SITE_URL]


def test_a_page_is_canonical_at_the_address_it_is_served_at() -> None:
    """A directory's `index.html` is served as the directory: the overview at the root,
    the workbench at `workbench/`. Every other page is served under its own name."""
    assert canonical_url("index.html") == SITE_URL == "https://jlevy.github.io/squares/"
    assert canonical_url("workbench/index.html") == SITE_URL + "workbench/"
    assert canonical_url("papers.html") == SITE_URL + "papers.html"
    nested = "papers/n11-optimality-review.html"
    assert canonical_url(nested) == SITE_URL + nested
    # A directory that only forwards is canonical nowhere: its forwarder names the paper.
    assert canonical_url("n11-optimality/index.html") == SITE_URL + "n11-optimality/"


def test_what_a_record_says_is_escaped_and_read_back_whole() -> None:
    """A description with a quote, an ampersand and an angle bracket is one attribute."""
    said = 'Squares & "bounds" for n < 12, the project\'s own.'
    head = read_head(document(head_tags(RESULTS._replace(name="A & B", description=said))))
    assert head.meta("description") == head.meta("og:description") == [said]
    assert head.titles == ("A & B · The Squares Project",)
    assert head.meta("og:title") == ["A & B"]


def test_an_article_states_its_dates_and_a_page_of_the_site_does_not() -> None:
    paper = RESULTS._replace(kind="article", published="2026-09-05", modified="2026-09-28")
    head = read_head(document(head_tags(paper)))
    assert head.meta("og:type") == ["article"]
    assert head.meta("article:published_time") == ["2026-09-05"]
    assert head.meta("article:modified_time") == ["2026-09-28"]
    assert head_problems(document(head_tags(paper)), SITE_URL + paper.path) == []
    assert "article:" not in head_tags(RESULTS)
    with pytest.raises(SystemExit, match="only an article"):
        head_tags(RESULTS._replace(published="2026-09-05"))
    with pytest.raises(SystemExit, match="not an ISO date"):
        head_tags(paper._replace(modified="September 28, 2026"))


@pytest.mark.parametrize(
    "description",
    ["", "   ", "x" * (DESCRIPTION_LIMIT + 1), "One line.\nAnd another."],
    ids=["empty", "blank", "too long", "two lines"],
)
def test_a_description_that_would_break_a_preview_is_refused(description: str) -> None:
    with pytest.raises(SystemExit, match="a description is one line"):
        head_tags(RESULTS._replace(description=description))
    head_tags(RESULTS._replace(description="x" * DESCRIPTION_LIMIT))


def test_every_page_of_the_site_carries_the_set_once_at_its_own_address(
    pages: dict[str, str],
) -> None:
    """Each page the renderer builds passes the deployed site's own check: one of each
    tag, canonical and `og:url` at the served address, a topical article title or named
    website title, the formal project name, and the site's card."""
    assert set(pages) == set(render_overview.PAGES)
    for name, page in pages.items():
        assert head_problems(page, canonical_url(name)) == [], name
        head = read_head(page)
        assert head.lang == "en", name
        (title,) = head.titles
        (shown,) = head.meta("og:title")
        assert title == (shown if head.meta("og:type") == ["article"] else page_title(shown)), (
            name
        )
        assert "Square Packing Project" not in title, name
        # kpress's own four tags are gone, not added to.
        assert len(head.meta("og:type")) == len(head.meta("twitter:card")) == 1, name
    assert read_head(pages["index.html"]).titles == (
        "Square Packing: Bounds, Results and Best Packings · The Squares Project",
    )
    assert read_head(pages["tutorial.html"]).meta("og:type") == ["article"]
    kinds = {name: read_head(page).meta("og:type") for name, page in pages.items()}
    assert [name for name, kind in kinds.items() if kind != ["website"]] == ["tutorial.html"]


def test_every_page_has_a_description_of_its_own(pages: dict[str, str]) -> None:
    """No two pages say the same thing of themselves, the workbench and the reviews
    among them, and none is the site-wide sentence under another page's name."""
    import importlib  # noqa: PLC0415

    from workbench_tools import build_site  # noqa: PLC0415

    assert shared_descriptions(pages) == []
    described = {name: read_head(page).meta("description")[0] for name, page in pages.items()}
    described["workbench/index.html"] = build_site.PAGE.description
    for record in render_overview.PAPERS[1:]:
        review = importlib.import_module(record.module)
        described[review.SITE_PATH] = review.DESCRIPTION
    assert len(set(described.values())) == len(described)
    for name, description in described.items():
        assert 20 <= len(description) <= DESCRIPTION_LIMIT, (name, len(description))
        assert description.endswith("."), name
    assert described["index.html"] == render_overview.OVERVIEW_DESCRIPTION
    assert described["frontier.html"] == render_overview.FRONTIER_DESCRIPTION
    assert described[render_overview.RESULTS_PAGE] == render_overview.RESULTS_DESCRIPTION
    assert described["papers.html"] == render_overview.PAPERS_DESCRIPTION
    assert described["visualize.html"] == render_overview.VISUALIZE_DESCRIPTION


def test_document_cards_and_expanded_descriptions_name_the_same_documents(
    pages: dict[str, str],
) -> None:
    """Short card notes and richer search descriptions belong to the same documents."""
    notes = [note for _, _, note in overview_sections.DOCUMENTS]
    described = [
        read_head(pages[name]).meta("description")[0] for name in render_overview.DOCUMENT_PAGES
    ]
    documents = {doc.name: doc for doc in site_documents.DOCUMENTS}
    assert described == [documents[name].description for name in render_overview.DOCUMENT_PAGES]
    assert [source for source, _, _ in overview_sections.DOCUMENTS] == [
        documents[name].source.relative_to(site_documents.REPO).as_posix()
        for name in render_overview.DOCUMENT_PAGES
    ]
    assert all(
        20 <= len(note) < len(description) <= DESCRIPTION_LIMIT
        for note, description in zip(notes, described, strict=True)
    )


def broken(change: tuple[str, str]) -> str:
    """The results page's head with one string replaced."""
    old, new = change
    tags = head_tags(RESULTS)
    assert old in tags, old
    return document(tags.replace(old, new, 1))


OG_TITLE = '<meta property="og:title" content="Every Result">'


@pytest.mark.parametrize(
    ("change", "finding"),
    [
        ((OG_TITLE, OG_TITLE * 2), "2 og:title tags"),
        ((OG_TITLE, ""), "0 og:title tags"),
        (
            ('content="Every Result">', 'content="Every Result · Square Packing">'),
            "og:title is",
        ),
        (("<title>Every Result · The", "<title>Every Result · A"), "does not end in"),
        (
            ("<title>Every Result · The Squares Project", "<title>Squares"),
            "does not end",
        ),
        (
            (
                'og:site_name" content="The Squares Project',
                'og:site_name" content="Squares',
            ),
            "og:site_name is 'Squares'",
        ),
        (
            (
                'og:url" content="https://jlevy.github.io/squares/all-results.html',
                'og:url" content="https://jlevy.github.io/squares/results.html',
            ),
            "og:url is",
        ),
        (
            (
                'rel="canonical" href="https://jlevy.github.io/squares/',
                'rel="canonical" href="',
            ),
            "the canonical link is 'all-results.html'",
        ),
        (
            ('og:image" content="https://jlevy.github.io/squares/', 'og:image" content="'),
            "og:image is 'social-card.png'",
        ),
        (('og:image:width" content="1200', 'og:image:width" content="2400'), "og:image:width"),
        (
            ('twitter:card" content="summary_large_image', 'twitter:card" content="summary'),
            "twitter:card is 'summary'",
        ),
        (
            (
                '<meta name="description" content="Every',
                '<meta name="description" content="Each',
            ),
            "og:description is",
        ),
        (('og:type" content="website', 'og:type" content="page'), "og:type is 'page'"),
        (('og:locale" content="en_US', 'og:locale" content="en'), "og:locale is 'en'"),
        (("</title>", "</title><title>Another</title>"), "2 <title>"),
    ],
    ids=lambda value: value if isinstance(value, str) else None,
)
def test_a_head_that_would_show_a_worse_preview_is_named(
    change: tuple[str, str], finding: str
) -> None:
    """Each way the heads were wrong before, and each way one could drift, is a finding:
    a tag twice or missing, the site's name after the preview's title, the old names, an
    address that is not the page's or not in full, a size the card is not."""
    problems = head_problems(broken(change), SITE_URL + RESULTS.path)
    assert any(finding in problem for problem in problems), problems


def test_a_head_is_read_by_a_parser_and_only_to_its_end() -> None:
    """A tag spelt in a stylesheet's comment or in the body is not the head's."""
    page = (
        '<!doctype html><html lang="en"><head>'
        "<style>/* <title>Not this</title> <meta name=description content=no> */"
        f"</style>{head_tags(RESULTS)}{favicon_html()}</head><body>"
        "<svg><title>A figure</title></svg>"
        '<meta property="og:title" content="Body"></body></html>'
    )
    head = read_head(page)
    assert head.titles == ("Every Result · The Squares Project",)
    assert head.meta("og:title") == ["Every Result"]
    assert head_problems(page, SITE_URL + RESULTS.path) == []
    assert read_head(
        "<div class='site-result'>A fragment</div>"
    ) == check_published_site.PageHead(None, (), (), ())


@pytest.mark.parametrize("boundary", [0, (1 << 16) - 3])
def test_head_markers_in_raw_text_and_attributes_do_not_end_the_head(boundary: int) -> None:
    """Only the parser's real head boundary ends metadata, including across chunks."""
    prefix = '<!doctype html><html lang="en"><head>'
    padding = " " * max(0, boundary - len(prefix))
    marker = probe(Path(__file__).with_name("probes"), "check_published_site/head_marker")
    page = (
        prefix
        + padding
        + f"<script>{marker}</script>"
        + "<style>/* </head><title>Not this</title> */</style>"
        + "<!-- </head><title>Not this either</title> -->"
        + '<meta data-note="</head>" name="extra" content="whole">'
        + head_tags(RESULTS)
        + favicon_html()
        + '</head><body><meta property="og:title" content="Body"></body></html>'
    )
    head = read_head(page)
    assert head.titles == ("Every Result · The Squares Project",)
    assert head.meta("extra") == ["whole"]
    assert head_problems(page, SITE_URL + RESULTS.path) == []


@pytest.mark.parametrize("boundary", [0, (1 << 16) - 3])
def test_head_reader_does_not_parse_the_math_body(
    monkeypatch: pytest.MonkeyPatch, boundary: int
) -> None:
    """A metadata pass ends at the real boundary, before tokenizing dense body markup."""
    prefix = '<!doctype html><html lang="en"><head>'
    padding = " " * max(0, boundary - len(prefix) - len(head_tags(RESULTS)))
    scanned: list[str] = []
    original = HTMLParser.parse_starttag

    def observe(reader: HTMLParser, position: int) -> int:
        tag = re.match(r"<([a-z]+)", reader.rawdata[position:])
        assert tag is not None
        scanned.append(tag.group(1))
        return original(reader, position)

    monkeypatch.setattr(HTMLParser, "parse_starttag", observe)
    page = (
        prefix
        + head_tags(RESULTS)
        + padding
        + "</head><body>"
        + ("<math><mrow><mi>x</mi><mo>+</mo><mn>1</mn></mrow></math>" * 800)
        + "</body></html>"
    )
    assert read_head(page).titles == ("Every Result · The Squares Project",)
    assert "body" not in scanned
    assert "math" not in scanned


def test_document_detection_stops_at_the_first_document_marker(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Detecting a document does not parse its metadata or the prepared math body."""

    def refuse_head(*_args: object) -> None:
        raise AssertionError("document detection reached the head")

    monkeypatch.setattr(HTMLParser, "parse_starttag", refuse_head)
    assert check_published_site.is_document(
        "<!doctype html><html><head><title>Page</title></head><body></body></html>"
    )


def test_a_long_or_missing_description_is_a_finding() -> None:
    long = "x" * (DESCRIPTION_LIMIT + 1)
    tags = head_tags(RESULTS).replace(RESULTS.description, long)
    assert any("over 160" in p for p in head_problems(document(tags), SITE_URL + RESULTS.path))
    tags = head_tags(RESULTS).replace(f'content="{RESULTS.description}"', 'content=""')
    assert any("empty" in p for p in head_problems(document(tags), SITE_URL + RESULTS.path))


def test_two_pages_with_one_description_are_named() -> None:
    first = document(head_tags(RESULTS))
    second = document(head_tags(RESULTS._replace(name="Papers", path="papers.html")))
    third = document(head_tags(RESULTS._replace(description="Another sentence.")))
    (shared,) = shared_descriptions({"a.html": first, "b.html": second, "c.html": third})
    assert shared.startswith("a.html, b.html: ")
    assert shared_descriptions({"a.html": first, "c.html": third}) == []


def test_a_forwarder_previews_the_page_it_leads_to_and_one_off_the_site_carries_none(
    pages: dict[str, str],
) -> None:
    """An old address is still shared, and a crawler drawing a preview runs no script and
    does not reliably follow a refresh. So a forwarder to a page of the site
    carries the whole set, at that page's address: its canonical link and `og:url` are
    where it leads, the card and the icon are the site's (think-esmk), and its name, its
    kind and its description are the ones the page's own head gives. Those are read here
    from the rendered page, not from the record the forwarder is written from: the
    forwarder from `status.html` named the frontier atlas by a name the page no longer
    had. The papers are other builds' pages, so their forwarders are held to the
    rendered papers in those modules' tests. The one forwarder that leads off the site,
    the defect log's, names that address and carries no card. Every forwarder is the
    renderer's, the papers' old addresses among them: the optimality paper's page, the
    directory it was served from, and the explainer's."""
    from devtools import render_n11_lower_bounds_explainer as explainer  # noqa: PLC0415
    from devtools import render_n11_optimality_review as paper  # noqa: PLC0415

    named = check_published_site.forwarder_canonicals()
    forwarders = {page.name: page.html for page in render_overview.forwarder_pages()}
    assert set(named) == set(forwarders)
    moved = dict(render_overview.MOVED_PAGES)
    within = {name for name, url in named.items() if url.startswith(SITE_URL)}
    assert set(named) - within == {"defects.html"}
    papers = {explainer.SITE_PATH, paper.SITE_PATH}
    assert {moved[name] for name in within} - set(pages) == papers
    for name, page in forwarders.items():
        assert named[name].startswith("https://"), name
        head = read_head(page)
        if name not in within:
            assert forwarder_problems(page, named[name], page_url=SITE_URL + name) == [], name
            assert head.link("canonical") == [moved[name]] == [named[name]]
            assert not [key for key, _ in head.metas if key.startswith(("og:", "twitter:"))]
            continue
        assert named[name] == canonical_url(moved[name]), name
        assert head.meta("og:url") == head.link("canonical") == [named[name]], name
        assert head.meta("og:image") == [render_overview.social_card_url()], name
        if moved[name] in papers:
            assert forwarder_problems(page, named[name], page_url=SITE_URL + name) == [], name
            continue
        destination = pages[moved[name]]
        assert (
            forwarder_problems(page, named[name], destination, page_url=SITE_URL + name) == []
        ), name
        own = read_head(destination)
        assert head.titles == own.titles, name
        for key in ("og:title", "og:type", "og:description", "description", "twitter:title"):
            assert head.meta(key) == own.meta(key), (name, key)
    landing = forwarders["n11-optimality/index.html"]
    target = canonical_url(paper.SITE_PATH)
    assert target == SITE_URL + "papers/n11-optimality-review.html"
    assert named["n11-optimality/index.html"] == target
    assert named["n11-optimality/t-060-explainer.html"] == target
    assert named["explainer.html"] == canonical_url(explainer.SITE_PATH) == explainer.PAGE_URL
    assert explainer.PAGE_URL == SITE_URL + "papers/n11-lower-bounds-explainer.html"
    assert (
        forwarder_problems(landing, target, page_url=SITE_URL + "n11-optimality/index.html")
        == []
    )
    # The landing address named the paper by its file name alone until 2026-10-01.
    relative = landing.replace(
        f'rel="canonical" href="{target}"',
        'rel="canonical" href="../papers/n11-optimality-review.html"',
    )
    assert any(
        "the canonical link is" in p
        for p in forwarder_problems(
            relative, target, page_url=SITE_URL + "n11-optimality/index.html"
        )
    )
    assert any("not an address in full" in p for p in forwarder_problems(relative, "a.html"))


#: The forwarder at the optimality paper's old address, and the address it leads to.
LANDING = "n11-optimality/t-060-explainer.html"


def _landing() -> tuple[str, str]:
    forwarders = {page.name: page.html for page in render_overview.forwarder_pages()}
    return forwarders[LANDING], canonical_url("papers/n11-optimality-review.html")


@pytest.mark.parametrize(
    ("tag", "finding"),
    [
        ('<meta property="og:image" content="', "0 og:image tags, not one"),
        ('<meta name="twitter:card" content="', "0 twitter:card tags, not one"),
        ('<meta name="description" content="', "0 description tags, not one"),
        ('<meta property="og:url" content="', "0 og:url tags, not one"),
        ('<link rel="icon" ', "1 icon links, expected the SVG/PNG pair"),
    ],
    ids=["og:image", "twitter:card", "description", "og:url", "icon"],
)
def test_a_forwarder_to_a_page_of_the_site_that_drops_a_tag_is_named(
    tag: str, finding: str
) -> None:
    """The negative controls of the forwarders' rule: each tag a preview is drawn from,
    taken out of a forwarder that leads to a paper, is a finding."""
    page, target = _landing()
    assert forwarder_problems(page, target, page_url=SITE_URL + LANDING) == []
    start = page.index(tag)
    dropped = page[:start] + page[page.index(">", start) + 1 :]
    assert finding in forwarder_problems(dropped, target, page_url=SITE_URL + LANDING)


def test_a_forwarder_previewing_its_page_by_another_name_kind_or_sentence_is_named() -> None:
    """A forwarder's preview is the page's own, so a name, a kind or a description the
    page's own head does not give is a finding wherever the check has that head, however
    whole and consistent the forwarder's own set is: the frontier atlas's forwarder named
    it "The Frontier Atlas" and the papers' took their cards' sentence-case titles as
    websites. Without the page's head there is nothing to hold it to. A forwarder off the
    site with a card is a finding too."""
    forwarder = next(
        moved.html
        for moved in render_overview.forwarder_pages()
        if moved.name == "results.html"
    )
    target = canonical_url(render_overview.RESULTS_PAGE)
    destination = document(head_tags(render_overview.RESULTS_META))
    assert forwarder_problems(forwarder, target, destination) == []
    said = html.escape(render_overview.RESULTS_DESCRIPTION, quote=True)
    assert said in forwarder
    for old, new, finding in (
        (
            "Every Result",
            "All Results",
            "its og:title is ['All Results'], and the page's own is ['Every Result']",
        ),
        (
            'og:type" content="website"',
            'og:type" content="article"',
            "its og:type is ['article'], and the page's own is ['website']",
        ),
        (said, "This page has moved.", "its og:description is ['This page has moved.']"),
    ):
        changed = forwarder.replace(old, new)
        assert head_problems(changed, target) == [], old
        problems = forwarder_problems(changed, target, destination)
        assert len(problems) == 1, problems
        assert problems[0].startswith(finding), problems
        assert forwarder_problems(changed, target) == [], old
    defects = next(
        forwarder.html
        for forwarder in render_overview.forwarder_pages()
        if forwarder.name == "defects.html"
    )
    away = dict(render_overview.MOVED_PAGES)["defects.html"]
    assert forwarder_problems(defects, away) == []
    carded = defects.replace("<title>", f"{OG_TITLE}<title>", 1)
    assert any("card tags" in problem for problem in forwarder_problems(carded, away))


@pytest.mark.parametrize(
    ("icons", "finding"),
    [
        ("", "0 icon links, expected the SVG/PNG pair"),
        ("{icon}{icon}", "4 icon links, expected the SVG/PNG pair"),
        (
            '<link rel="icon" href="data:image/png;base64,AAAA">',
            "1 icon links, expected the SVG/PNG pair",
        ),
        (
            favicon_html().replace("favicon.svg", "other.svg"),
            "the icon is not the site's SVG/PNG pair",
        ),
    ],
    ids=["missing", "twice", "inline-substitute", "wrong-pair-member"],
)
def test_a_page_without_the_sites_exact_icon_pair_is_named(icons: str, finding: str) -> None:
    """Missing, duplicate and substituted stable icons fail the complete head check."""
    page = document(head_tags(RESULTS)).replace(
        favicon_html(), icons.format(icon=favicon_html()), 1
    )
    problems = head_problems(page, SITE_URL + RESULTS.path)
    assert any(finding in problem for problem in problems), problems
    head = read_head(document(head_tags(RESULTS)))
    assert head.link("icon") == ["favicon.svg", "favicon-48.png"]
    assert head.link("apple-touch-icon") == ["apple-touch-icon.png"]


@pytest.mark.parametrize("complete", [False, True])
def test_only_the_complete_exact_archive_accepts_its_self_contained_icon(
    *,
    complete: bool,
) -> None:
    slug = render_overview.EXACT_SIDE_VALUES + ("-complete" if complete else "")
    page = PageMeta(
        name="Exact archive icon control",
        description="A control for the self-contained archive icon policy.",
        path=render_overview.paper_path(slug),
    )
    text = document(head_tags(page)).replace(favicon_html(), favicon_html(inline=True))
    problems = head_problems(text, canonical_url(page.path))
    if complete:
        assert problems == []
        changed = text.replace(render_overview.favicon_url(), "data:image/svg+xml,bad", 1)
        assert head_problems(changed, canonical_url(page.path))
    else:
        assert any("expected the SVG/PNG pair" in problem for problem in problems)


@pytest.fixture(scope="module")
def result_pages() -> dict[str, str]:
    return {page.name: page.html for page in site_renders.result_pages()}


@pytest.fixture(scope="module")
def records() -> dict[str, str]:
    return site_renders.case_records()


def test_result_overviews_are_complete_canonical_documents(
    result_pages: dict[str, str],
) -> None:
    """The canonical document's article can also be fetched into a reader's popover."""
    assert result_pages
    for path, page in result_pages.items():
        assert check_published_site.is_document(page), path
        assert head_problems(page, canonical_url(path)) == [], path
        assert len(re.findall(r"<h1\b", page)) == 1, path
        assert '<article class="site-result"' in page, path
        assert "<main" in page, path
        assert 'class="site-nav"' in page, path


def test_the_card_is_the_heros_drawing_on_the_pages_background() -> None:
    """The card is the homepage's hero and no second drawing: the same case at the same
    resolution through the same function, so its squares, colours and line weights are
    the page's, in the light theme's ink on its background, with the project's name."""
    hero = overview_sections.hero()
    case = overview_sections.HERO_CASE
    assert case == 53
    assert f"The best packing known for {case} squares" in hero
    assert packing_svg(case, units=social_card.HERO_UNITS) in hero
    light = rung_scale.page_colours()["light"]
    ink, paper = rung_scale.hex_colour(light["text"]), rung_scale.hex_colour(light["bg"])
    assert social_card.page_colours() == (ink, paper) == ("#111827", "#ffffff")
    drawing = packing_svg(case, units=social_card.HERO_UNITS, ink=ink)
    svg = social_card.card_svg()
    body = drawing.split(">", 1)[1]
    assert svg.count(body) == 1, "the hero's drawing, in the page's ink, is in the card whole"
    assert svg.startswith(
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" '
        'viewBox="0 0 1200 630"><rect width="1200" height="630" fill="#ffffff"/>'
    )
    # The packing and the name sit inside the square at the card's centre, which is what
    # a consumer that shows a square thumbnail keeps.
    placed = re.search(r'<svg x="([\d.]+)" y="([\d.]+)" width="(\d+)" height="(\d+)"', svg)
    assert placed is not None
    x, y, width, height = (float(part) for part in placed.groups())
    assert width == height == social_card.PACKING_SIDE
    assert x == (SOCIAL_CARD_WIDTH - width) / 2
    margin = (SOCIAL_CARD_WIDTH - SOCIAL_CARD_HEIGHT) / 2
    outline, name_width, cap_height = social_card.name_outline(
        PROJECT_NAME.upper(), social_card.NAME_SIZE
    )
    assert outline in svg
    assert margin < (SOCIAL_CARD_WIDTH - name_width) / 2
    foot = y + height + social_card.NAME_GAP + cap_height
    assert y == pytest.approx(SOCIAL_CARD_HEIGHT - foot, abs=0.01), "equal margins"
    assert y >= 40
    # Without the name the drawing is the whole card, larger and centred.
    plain = social_card.card_svg(named=False)
    assert outline not in plain
    assert plain.count(body) == 1
    assert f'width="{social_card.PLAIN_PACKING_SIDE}"' in plain


def test_the_cards_name_is_set_as_the_bar_sets_the_sites() -> None:
    """The name under the packing is the bar's: the bar's sans at its weight and letter
    spacing, in capitals. The values are the bar's rule's, read from the stylesheet."""
    css = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    rule = re.search(r"\.site-nav \.site-name \{([^}]*font-weight[^}]*)\}", css)
    assert rule is not None
    assert f"font-weight: {social_card.NAME_WEIGHT};" in rule.group(1)
    assert f"letter-spacing: {social_card.NAME_TRACKING}em;" in rule.group(1)
    assert "text-transform: uppercase;" in rule.group(1)
    face = render_overview.nav_shell("visualize", root="../").head
    assert '"Source Sans 3 Variable"' in face
    assert social_card.SANS_FACE.startswith("source-sans-3-")
    # Outlines, not text: a rasteriser would set text in a face the machine happens to have.
    svg = social_card.card_svg()
    assert "<text" not in svg
    assert "font-family" not in svg
    outline, width, cap_height = social_card.name_outline("THE", 34)
    assert outline.startswith("M")
    assert 40 < width < 80
    assert 20 < cap_height < 26


def test_the_card_is_a_png_of_the_declared_size_under_the_ceiling(card: bytes) -> None:
    """The bytes are what every head declares: a PNG, 1200 by 630, and light enough that
    no consumer refuses it. Two drawings agree, which is what the Pages job compares."""
    assert social_card.png_dimensions(card) == (SOCIAL_CARD_WIDTH, SOCIAL_CARD_HEIGHT)
    assert (SOCIAL_CARD_WIDTH, SOCIAL_CARD_HEIGHT) == (1200, 630)
    assert social_card.card_problems(card) == []
    assert 10_000 < len(card) <= social_card.BYTE_CEILING == 300_000
    assert social_card.card_png() == card
    assert social_card.card_png(named=False) != card


def test_bytes_that_are_not_the_card_are_named(card: bytes) -> None:
    import cairosvg  # noqa: PLC0415

    assert social_card.card_problems(b"<html>404</html>") == ["it is not a PNG"]
    assert social_card.png_dimensions(b"") is None
    wide = cairosvg.svg2png(
        bytestring=social_card.card_svg().encode(), output_width=2400, output_height=1260
    )
    assert isinstance(wide, bytes)
    (problem,) = social_card.card_problems(wide)
    assert problem == "it is 2400x1260, and every page declares 1200x630"
    heavy = card + b"\0" * social_card.BYTE_CEILING
    assert social_card.card_problems(heavy) == [
        f"it is {len(heavy)} bytes, over the 300000-byte ceiling"
    ]


def test_the_tool_writes_the_card_under_its_served_name_and_checks_it(
    tmp_path: Path, card: bytes, capsys: pytest.CaptureFixture[str]
) -> None:
    assert social_card.main(["--output-dir", str(tmp_path), "--check"]) == 1
    assert "stale or missing" in capsys.readouterr().err
    assert social_card.main(["--output-dir", str(tmp_path)]) == 0
    assert sorted(path.name for path in tmp_path.iterdir()) == [SOCIAL_CARD]
    assert (tmp_path / SOCIAL_CARD).read_bytes() == card
    assert "1200x630" in capsys.readouterr().out
    assert social_card.main(["--output-dir", str(tmp_path), "--check"]) == 0
    (tmp_path / SOCIAL_CARD).write_bytes(social_card.card_png(named=False))
    assert social_card.main(["--output-dir", str(tmp_path), "--check"]) == 1
    assert social_card.main(["--output-dir", str(tmp_path), "--plain", "--check"]) == 0


def test_a_head_only_build_checks_metadata_but_is_not_complete_publication(
    tmp_path: Path, pages: dict[str, str], card: bytes, capsys: pytest.CaptureFixture[str]
) -> None:
    """The local mode reads a directory as the deploy check reads the site: every page
    there, every forwarder there and the card, with what a build left out reported and
    not failed, and a card that is missing or the wrong picture failed. A forwarder to a
    page of the site names the card as a page does."""
    # A build with none of the site's pages names no card, so it misses none.
    assert all(passed for passed, _ in local_head_checks(tmp_path))
    forwarders = {
        forwarder.name: forwarder.html for forwarder in render_overview.forwarder_pages()
    }
    (tmp_path / "status.html").write_text(forwarders["status.html"], encoding="utf-8")
    assert [line for passed, line in local_head_checks(tmp_path) if not passed] == [
        f"card {SOCIAL_CARD}: not served"
    ]
    (tmp_path / "status.html").unlink()
    # Each page with the shared assets it names, which the check holds too.
    site_renders.write(tmp_path, "index.html", "papers.html")
    for forwarder in render_overview.forwarder_pages():
        # A forwarder stands where its page was, which for a paper was a directory down.
        (tmp_path / forwarder.name).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / forwarder.name).write_text(forwarder.html, encoding="utf-8")
    results = local_head_checks(tmp_path)
    assert [line for passed, line in results if not passed] == [
        f"card {SOCIAL_CARD}: not served"
    ]
    (tmp_path / SOCIAL_CARD).write_bytes(card)
    results = local_head_checks(tmp_path)
    assert all(passed for passed, _ in results), results
    lines = [line for _, line in results]
    assert "index.html: one of each identity and card tag, agreeing with its address" in lines
    assert "each of 2 pages has a description of its own" in lines
    assert f"card {SOCIAL_CARD}: a PNG of 1200x630, {len(card)} bytes" in lines
    assert "papers/n11-lower-bounds-explainer.html: not in this build, so not checked" in lines
    assert "papers/n11-threshold-bound-review.html: not in this build, so not checked" in lines
    assert "papers/n11-optimality-review.html: not in this build, so not checked" in lines
    assert "workbench/index.html: not in this build, so not checked" in lines
    # A metadata-only fixture is not the complete registered publication tree.
    assert check_published_site.main(["--local", str(tmp_path)]) == 1
    assert "site cases/11.html: required overview output missing" in capsys.readouterr().out
    # A page under another's head, and a card that is not the card.
    (tmp_path / "papers.html").write_text(pages["index.html"], encoding="utf-8")
    (tmp_path / SOCIAL_CARD).write_bytes(b"not a picture")
    failed = [line for passed, line in local_head_checks(tmp_path) if not passed]
    assert len(failed) == 3
    assert failed[0].startswith("papers.html: head: the canonical link is")
    assert failed[1].startswith("descriptions shared between pages: index.html, papers.html")
    assert failed[2] == f"card {SOCIAL_CARD}: it is not a PNG"
    assert check_published_site.main(["--local", str(tmp_path)]) == 1


@pytest.fixture(scope="module")
def published(
    tmp_path_factory: pytest.TempPathFactory,
    pages: dict[str, str],
    card: bytes,
    result_pages: dict[str, str],
    records: dict[str, str],
) -> Path:
    """Everything the overview's Pages job publishes, as it writes it: the site's pages,
    every case's record file, every forwarder and the card, with a result's overview
    beside them as complete documents. The papers and the workbench are other jobs'
    pages, held to the same `head_problems` in their own modules' tests."""
    root = tmp_path_factory.mktemp("published")
    files = [
        *(render_overview.Page(name, text) for name, text in pages.items()),
        *(render_overview.Page(name, text) for name, text in records.items()),
        *render_overview.forwarder_pages(),
        *(render_overview.Page(name, text) for name, text in result_pages.items()),
        *site_documents.chapter_pages(),
    ]
    render_overview.write_site(root, files)
    (root / SOCIAL_CARD).write_bytes(card)
    return root


def test_every_page_the_site_publishes_carries_its_preview_by_its_kind(
    published: Path, result_pages: dict[str, str], records: dict[str, str]
) -> None:
    """The metadata contract, over every HTML file the overview's build publishes: each
    page and each case's record file carries the whole set at its own address, with the
    site's icons; each forwarder carries what its rule says; results and synopsis chapters
    carry complete heads. The exhaustive output inventory also includes crawl HTML;
    the not-found and withdrawn pages are excluded from live preview counts."""
    results = local_head_checks(published)
    assert [line for passed, line in results if not passed] == []
    lines = [line for _, line in results]
    assert len(records) == 324
    assert (
        f"case records: each of {len(records)} carries one of each identity and card tag, "
        "agreeing with its address"
    ) in lines
    chapters = site_documents.chapter_names()
    for name in (*render_overview.PAGES, *result_pages, *chapters):
        assert f"{name}: one of each identity and card tag, agreeing with its address" in lines
    pages = len(render_overview.PAGES) + len(records) + len(result_pages) + len(chapters)
    assert f"each of {pages} pages has a description of its own" in lines
    # A forwarder to a page this build writes is held to that page's head; the papers'
    # are other builds' pages, held to theirs where the site is assembled.
    for old, new in render_overview.MOVED_PAGES:
        rule = (
            f"forwarder {old}: names {new} as canonical, and carries no card"
            if new.startswith("https://")
            else f"forwarder {old}: previews {canonical_url(new)} as that page's own head does"
            if new in render_overview.PAGES
            else f"forwarder {old}: previews {canonical_url(new)}, whose page is not here to "
            "compare"
        )
        assert rule in lines, old
    crawl_html = {
        "404.html",
        *(row.path for row in site_urls.load_registry() if row.status == "withdrawn"),
    }
    held = {
        *render_overview.PAGES,
        *records,
        *(old for old, _ in render_overview.MOVED_PAGES),
        *result_pages,
        *chapters,
        *(name for name in crawl_html if name.endswith(".html")),
    }
    assert {
        path.relative_to(published).as_posix() for path in published.rglob("*.html")
    } == held
    for record in records.values():
        assert record.count(favicon_html(root="../")) == 1


def test_a_page_added_later_or_a_record_that_loses_a_tag_fails_the_check(
    tmp_path: Path, pages: dict[str, str], card: bytes, records: dict[str, str]
) -> None:
    """The negative controls: a page no list names that ships with a head and no preview,
    one whose head says nothing at all, a record file that loses its image, one without
    the icon, a forwarder to a page of the site that carries only its canonical link, as
    every forwarder did before 2026-10-03, and one that previews the page beside it by
    another name than the page's own are each a failure of the check the overview's job
    runs."""
    record = records["cases/11.html"]
    good = {
        "index.html": pages["index.html"],
        "cases/11.html": record,
        "cases/12.html": records["cases/12.html"],
    }
    render_overview.write_site(tmp_path, [render_overview.Page(n, t) for n, t in good.items()])
    (tmp_path / SOCIAL_CARD).write_bytes(card)
    assert all(passed for passed, _ in local_head_checks(tmp_path))

    added = '<!doctype html><html lang="en"><head><title>New</title></head><body></body></html>'
    (tmp_path / "new.html").write_text(added, encoding="utf-8")
    (failure,) = [line for passed, line in local_head_checks(tmp_path) if not passed]
    assert failure.startswith("new.html: head: 0 canonical links, not one")
    assert "0 og:image tags, not one" in failure
    # A page whose head names nothing is a page all the same, not a fragment.
    bare = (
        '<!doctype html><html><head><meta charset="utf-8"><style>p{margin:0}</style>'
        "</head><body><p>New</p></body></html>"
    )
    assert read_head(bare) == check_published_site.PageHead(None, (), (), ())
    assert check_published_site.is_document(bare)
    assert check_published_site.is_document("<!doctype html><title>New</title><p>New")
    assert not check_published_site.is_document('<div class="site-result"><p>A</p></div>')
    (tmp_path / "new.html").write_text(bare, encoding="utf-8")
    (failure,) = [line for passed, line in local_head_checks(tmp_path) if not passed]
    assert failure.startswith("new.html: head: lang is None, not 'en'; 0 <title>, not one")
    (tmp_path / "new.html").unlink()

    image = f'<meta property="og:image" content="{render_overview.social_card_url()}">'
    assert image in record
    (tmp_path / "cases/11.html").write_text(record.replace(image, ""), encoding="utf-8")
    (tmp_path / "cases/12.html").write_text(
        good["cases/12.html"].replace(favicon_html(root="../"), ""), encoding="utf-8"
    )
    (failure,) = [line for passed, line in local_head_checks(tmp_path) if not passed]
    assert failure.startswith("case records: 2 of 2 heads wrong: cases/11.html: ")
    assert "cases/11.html: 0 og:image tags, not one" in failure
    assert "cases/12.html: 0 icon links, expected the SVG/PNG pair" in failure

    (tmp_path / "cases/11.html").write_text(record, encoding="utf-8")
    (tmp_path / "cases/12.html").write_text(good["cases/12.html"], encoding="utf-8")
    target = canonical_url(render_overview.RESULTS_PAGE)
    bare = (
        '<!doctype html><html lang="en" data-moved-to="all-results.html"><head>'
        f'<title>Every Result</title><link rel="canonical" href="{target}"></head></html>'
    )
    (tmp_path / "results.html").write_text(bare, encoding="utf-8")
    (failure,) = [line for passed, line in local_head_checks(tmp_path) if not passed]
    assert failure.startswith("forwarder results.html: head: ")
    assert "0 og:url tags, not one" in failure
    assert "0 twitter:card tags, not one" in failure
    (tmp_path / "results.html").unlink()

    # The frontier atlas beside a forwarder that names it as the forwarder from
    # `status.html` did, by a name the page no longer had.
    site_renders.write(tmp_path, "frontier.html")
    forwarder = next(
        moved.html for moved in render_overview.forwarder_pages() if moved.name == "status.html"
    )
    (tmp_path / "status.html").write_text(forwarder, encoding="utf-8")
    assert all(passed for passed, _ in local_head_checks(tmp_path))
    renamed = forwarder.replace("The Frontier Survey", "The Frontier Atlas")
    (tmp_path / "status.html").write_text(renamed, encoding="utf-8")
    (failure,) = [line for passed, line in local_head_checks(tmp_path) if not passed]
    assert failure == (
        "forwarder status.html: head: its og:title is ['The Frontier Atlas'], and the "
        "page's own is ['The Frontier Survey']"
    )


def test_head_checks_report_one_line_a_page_a_forwarder_and_the_card(card: bytes) -> None:
    page = document(head_tags(render_overview.RESULTS_META))
    target = SITE_URL + "all-results.html"
    forwarder = next(
        moved.html
        for moved in render_overview.forwarder_pages()
        if moved.name == "results.html"
    )
    results = head_checks(
        {"all-results.html": page}, {"results.html": (forwarder, target)}, card
    )
    assert [passed for passed, _ in results] == [True, True, True, True]
    assert (
        results[2][1]
        == f"forwarder results.html: previews {target} as that page's own head does"
    )
    # The same forwarder under another name fails beside the page, and passes alone.
    renamed = forwarder.replace("Every Result", "All Results")
    results = head_checks({"all-results.html": page}, {"results.html": (renamed, target)}, card)
    assert [passed for passed, _ in results] == [True, True, False, True]
    results = head_checks({}, {"results.html": (renamed, target)}, card)
    assert results[1] == (
        True,
        f"forwarder results.html: previews {target}, whose page is not here to compare",
    )
    results = head_checks({"papers.html": page}, {"results.html": (forwarder, "x")}, None)
    assert [passed for passed, _ in results] == [False, True, False, False]
