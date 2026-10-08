#!/usr/bin/env python3
"""Check a complete GitHub Pages tree and the deployed site's retained URL contract.

From packing/:

    uv run --frozen --group dev python -m devtools.check_published_site --commit <sha>

With no --commit, origin/main supplies the expected deployed revision. --site can name
an HTTP preview built from the same revision. Every registered non-asset address is
fetched: all content pages, cases, results, paper editions, historical forwarders,
file copies, tombstones, sitemap and 404. Page budgets and share-preview metadata are
checked alongside repository links, paper versions, PDF source receipts, record-link
coverage and workbench startup. Forwarder destinations agree in canonical metadata,
refresh, script and visible link; pinned-browser arrival preserves query and fragment.

--local DIR checks the closed-world registry, required physical outputs, HTML budgets,
heads and links between papers without fetching the network. --partial requires one
or more --producer names and checks every output of those producers; missing files
never select partial mode. --local DIR --inventory reports heads without validation.

The live deployment check is separate from the required source registry/history gate.
Tests cover the parsing and failure controls with fixtures.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import posixpath
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Mapping, Sequence
from html.parser import HTMLParser
from pathlib import Path
from typing import NamedTuple
from urllib.parse import urljoin, urlsplit

from playwright.sync_api import Browser, BrowserContext, sync_playwright
from playwright.sync_api import Error as PlaywrightError

from devtools import (
    overview_data,
    render_case_pages,
    render_overview,
    result_overview,
    site_urls,
    social_card,
)
from devtools.overview_sections import LOWER_BOUNDS_PAPER, OPTIMALITY_PAPER, result_fragment
from devtools.render_n11_lower_bounds_explainer import (
    COMPOSITE_ASSETS,
    PAGE_URL,
    REPO,
    SITE_URL,
)
from devtools.render_n11_lower_bounds_explainer_pdf import BROWSER_OVERRIDE, EXPECTED_PAGE_COUNT
from devtools.repo_links import (
    REPO_URL,
    RepositoryTree,
    branch_paths,
    hash_pinned_links,
    repository_tree,
)
from sqpack.probes import probe
from sqpack.release import (
    EXPLAINER_VERSION,
    OPTIMALITY_REVIEW_EDITION,
    PUBLICATION_EDITION,
    THRESHOLD_REVIEW_EDITION,
)

#: The JavaScript this runs in the deployed workbench, as files (`sqpack.probes`).
PROBES = Path(__file__).resolve().parent / "probes"

#: A link into this repository as GitHub spells one: the ref, then the path, under
#: `blob/` for a file and `tree/` for a directory.
REPOSITORY_LINK = re.compile(re.escape(REPO_URL) + r"/(blob|tree)/([^/\s\"<>)]+)/([^\s\"<>)]*)")
CANONICAL = re.compile(r'<link\s+rel="canonical"\s+href="([^"]*)"')
#: The fuller body a row's popover fetches, as its address beside the page, and how a
#: result's overview opens: the one block it is, naming its result.
ROW_SOURCE = re.compile(r'data-row-pop-src="([^"]+)"')
RESULT_OVERVIEW = re.compile(r'<div class="site-result" data-result-overview="(t-\d{3})">')
#: The record page's index, each case's link to its record file beside it, and the
#: record a record file holds (`render_case_pages`).
CASE_INDEX_LINK = re.compile(r'href="(\d+)\.html" data-case="(\d+)"')
CASE_RECORD = re.compile(r'<article class="site-case" data-case="(\d+)"')
#: The record files a deploy check fetches: the first and last cases indexed and the
#: settled n = 11. The record page and every case popover fetch these files, so a deploy
#: that wrote none shows every record as a failed fetch, which no page fetch reveals.
RECORD_FILE_SAMPLE = 11

#: The lower-bounds explainer's Markdown edition and its PDF, by path under the site's
#: root: beside the page, under the paper's slug.
LOWER_BOUNDS_MARKDOWN = f"{LOWER_BOUNDS_PAPER.removesuffix('.html')}.md"
LOWER_BOUNDS_PDF = f"{LOWER_BOUNDS_PAPER.removesuffix('.html')}.pdf"

#: The site's own pages, by served name, read from the renderer that owns them so a page
#: added there is checked here without an edit. `index.html` is fetched as the root.
SITE_PAGES = tuple(render_overview.PAGES)

#: The pages whose repository links are each asked of GitHub as well. The rest are
#: checked against the commit's tree alone, which is offline, as the reader documents'
#: links already are when they are rendered; asking GitHub would cost a request per link
#: on every deploy. The results page is one, since its records are the register's links
#: and were asked of GitHub when the table was on the overview.
LINK_CHECKED_PAGES = frozenset({"index.html", "frontier.html", render_overview.RESULTS_PAGE})

#: Each paper's own version, as its front prints it (`sqpack.release`), by slug: the
#: explainer's number, and each review's status and number (`Draft v0.1.4`). A test holds
#: its slugs to the site's papers (`render_overview.PAPERS`).
PAPER_VERSIONS: dict[str, str] = {
    render_overview.N11_LOWER_BOUNDS_EXPLAINER: EXPLAINER_VERSION,
    render_overview.N11_THRESHOLD_BOUND_REVIEW: THRESHOLD_REVIEW_EDITION,
    render_overview.N11_OPTIMALITY_REVIEW: OPTIMALITY_REVIEW_EDITION,
}
#: The reviews, every paper after the first, by the path each is served at, which is the
#: one its Papers card links: each built and served as the optimality review is.
REVIEW_PAPERS: tuple[str, ...] = tuple(
    render_overview.paper_path(paper.slug)
    for paper in render_overview.PAPERS
    if paper.slug != render_overview.N11_LOWER_BOUNDS_EXPLAINER
)


def paper_files(page: str) -> tuple[str, str]:
    """What is served with a paper's page, by path under the site's root: its Markdown
    and its PDF, beside it under its slug."""
    stem = page.removesuffix(".html")
    return f"{stem}.md", f"{stem}.pdf"


#: What is served with the optimality paper's page (`paper_files`).
OPTIMALITY_PAPER_MARKDOWN, _OPTIMALITY_PAPER_PDF = paper_files(OPTIMALITY_PAPER)
OPTIMALITY_PAPER_FILES = paper_files(OPTIMALITY_PAPER)
#: The bar's current entry on a paper's page, a level below the root.
PAPERS_CURRENT = '<a data-page="papers" aria-current="page" href="../papers.html">'

#: Every file the deploy serves with the lower-bounds explainer, by path under the site's
#: root: its Markdown and PDF beside it, and the atlas's files at the root.
SERVED = (
    LOWER_BOUNDS_MARKDOWN,
    LOWER_BOUNDS_PDF,
    *(asset.name for asset in COMPOSITE_ASSETS),
)

#: What a forwarder says about where its page is now: the address the script reads, the
#: refresh a reader without scripts follows, and the link.
MOVED_TO = re.compile(r'<html\b[^>]*\sdata-moved-to="([^"]*)"')
REFRESH = re.compile(r'<meta\s+http-equiv="refresh"\s+content="0;\s*url=([^"]*)"')
MOVED_LINK = re.compile(r'<p>[^<]*<a\s+href="([^"]*)"')
#: The query string and fragment a forwarder is visited with in the browser: the review
#: switch the explainer reads and a footnote, both of which a real old link carries.
FORWARDED_SUFFIX = "?review=fonts#fn-1"

USER_AGENT = "squares-check-published-site (+https://github.com/jlevy/squares)"
WORKBENCH_PATH = "workbench/"
#: The workbench as a file under the root, which is how its head names its own address
#: (`render_overview.canonical_url`).
WORKBENCH_PAGE = f"{WORKBENCH_PATH}index.html"
WORKBENCH_REVISION = re.compile(
    r'<meta\s+name="squares-workbench-revision"\s+content="([0-9a-f]{40})">'
)
WORKBENCH_HOME = re.compile(r'<a\s+href="([^"]+)">the overview</a>')


#: The results whose published overviews are held, link for link, to what the renderer
#: writes for them. Between them their records cite files under directories of
#: `packing/resources` and of `packing/campaign`, the two trees the Pages jobs' partial
#: checkouts leave out (`rendered_record_links` refuses a sample that stops doing so):
#: T-060's source packet, certificate and proof; T-043's, for another case and source; and
#: T-023, a result of this project whose proofs and receipts are in the campaign.
RECORD_LINK_SAMPLE = ("T-060", "T-043", "T-023")
#: The trees a partial checkout omits the directories of, as `pages.yml` writes them.
OMITTED_TREES = ("packing/resources/", "packing/campaign/")
#: The pages with a table of results, whose rows' popovers each carry their result's
#: record links.
RECORD_LINK_PAGES = ("index.html", render_overview.RESULTS_PAGE)
#: A result row's popover from its opening tag on, named by its result
#: (`overview_sections.result_row`), and the line of record links its short form ends
#: with (`overview_sections._detail`).
_RESULT_POPOVER = re.compile(r'site-row-pop" id="pop-result-(t-\d{3})"')
_ROW_RECORDS = re.compile(r'<div class="site-records">(.*?)</div>', re.DOTALL)


#: Every `<meta>` a page's head carries exactly once, by its `name` or `property`: the
#: set `render_overview.head_tags` writes. The title and the canonical link are the
#: other two, read as their own elements.
REQUIRED_META = (
    "description",
    "og:type",
    "og:site_name",
    "og:locale",
    "og:title",
    "og:description",
    "og:url",
    "og:image",
    "og:image:type",
    "og:image:width",
    "og:image:height",
    "og:image:alt",
    "twitter:card",
    "twitter:title",
    "twitter:description",
    "twitter:image",
    "twitter:image:alt",
)
#: A paper's dates, which a head may carry once each and only as an article.
ARTICLE_META = ("article:published_time", "article:modified_time")
_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
#: How much of a page is handed to the parser at a time. A head ends within the first
#: response; the reader stops as soon as that head closes.
_HEAD_CHUNK = 1 << 16


class PageHead(NamedTuple):
    """What a page's `<head>` says of it, as a browser or a crawler reads it."""

    lang: str | None
    """The root element's `lang`."""
    titles: tuple[str, ...]
    metas: tuple[tuple[str, str], ...]
    """Each `<meta>` with a `name`, a `property` or an `http-equiv`, as that key and its
    `content`, in the head's order."""
    links: tuple[tuple[str, str], ...]
    """Each `<link>`, as its `rel` and its `href`."""

    def meta(self, key: str) -> list[str]:
        """Every value the head gives `key`: one, for a tag written once."""
        return [content for name, content in self.metas if name == key]

    def link(self, rel: str) -> list[str]:
        return [href for name, href in self.links if name == rel]


class _HeadReader(HTMLParser):
    """Reads the head and stops at its end. A real parser, since a head's inline scripts
    and styles are megabytes that may spell a tag in a comment or a string."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang: str | None = None
        self.titles: list[str] = []
        self.metas: list[tuple[str, str]] = []
        self.links: list[tuple[str, str]] = []
        self.done = False
        #: Whether the text opens a document: a doctype, an `<html>` or a `<head>`.
        self.document = False
        self._title: list[str] | None = None

    def handle_decl(self, decl: str) -> None:
        if decl.lower().startswith("doctype"):
            self.document = True

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.done:
            return
        values = dict(attrs)
        if tag in ("html", "head"):
            self.document = True
        if tag == "html":
            self.lang = values.get("lang")
        elif tag == "title":
            self._title = []
        elif tag == "meta":
            key = values.get("property") or values.get("name") or values.get("http-equiv")
            if key:
                self.metas.append((key, values.get("content") or ""))
        elif tag == "link":
            self.links.append((values.get("rel") or "", values.get("href") or ""))
        elif tag == "body":
            self.done = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self._title is not None:
            self.titles.append("".join(self._title))
            self._title = None
        elif tag == "head":
            self.done = True

    def handle_data(self, data: str) -> None:
        if self._title is not None:
            self._title.append(data)


def is_document(text: str) -> bool:
    """Whether `text` is a page rather than a fragment: it has a doctype, an `<html>` or a
    `<head>`, whatever its head then carries. A result's overview, a block fetched into a
    popover, has none of them. What a head says is no test, since a page with no `lang`,
    no title and no named `<meta>` says nothing and is a page all the same."""
    reader = _HeadReader()
    for start in range(0, len(text), _HEAD_CHUNK):
        reader.feed(text[start : start + _HEAD_CHUNK])
        if reader.document or reader.done:
            break
    return reader.document


def read_head(text: str) -> PageHead:
    """A page's head: its language, titles, `<meta>` tags and `<link>`s. A file with no
    head, as a result's overview is, has none of them."""
    reader = _HeadReader()
    for start in range(0, len(text), _HEAD_CHUNK):
        reader.feed(text[start : start + _HEAD_CHUNK])
        if reader.done:
            break
    return PageHead(reader.lang, tuple(reader.titles), tuple(reader.metas), tuple(reader.links))


def head_problems(
    text: str,
    canonical: str,
    *,
    allow_inline_favicon: bool = False,
    page_url: str | None = None,
) -> list[str]:
    """What is wrong with a page's head as the site writes one, for the page served at
    `canonical`; empty when it is clean.

    Each tag of `render_overview.head_tags` is there exactly once, and they agree with
    each other and with the site: the canonical link and `og:url` are `canonical`, in
    full under the published root; the title is the page's own name and then the
    project's formal name, and the preview's title is that name alone; the site's name
    is the formal name; the description is one sentence or two of at most
    `DESCRIPTION_LIMIT` characters, the same in all three places; the image is the
    site's one card, at the size it is drawn at; and the icon is the site's. What cannot
    be read off one page, that no other page says the same thing, is
    `shared_descriptions`, and that the card is served, the card's own check.
    """
    head = read_head(text)
    problems: list[str] = []

    def single(found: Sequence[str], what: str) -> str | None:
        if len(found) != 1:
            problems.append(f"{len(found)} {what}, not one")
            return None
        return found[0]

    def require(what: str, found: str | None, expected: str) -> None:
        if found is not None and found != expected:
            problems.append(f"{what} is {found!r}, not {expected!r}")

    if head.lang != "en":
        problems.append(f"lang is {head.lang!r}, not 'en'")
    title = single(head.titles, "<title>")
    declared = single(head.link("canonical"), "canonical links")
    tags = {key: single(head.meta(key), f"{key} tags") for key in REQUIRED_META}

    if not canonical.startswith(render_overview.SITE_URL):
        problems.append(f"{canonical!r} is not under {render_overview.SITE_URL}")
    require("the canonical link", declared, canonical)
    require("og:url", tags["og:url"], canonical)

    project = render_overview.PROJECT_NAME
    suffix = render_overview.TITLE_SEPARATOR + project
    if title is not None:
        if title.endswith(suffix) and title != suffix:
            require("og:title", tags["og:title"], title.removesuffix(suffix))
        elif title == project:
            require("og:title", tags["og:title"], project)
        elif title != tags["og:title"]:
            problems.append(f"the title {title!r} does not end in {suffix!r} or match og:title")
    require("twitter:title", tags["twitter:title"], tags["og:title"] or "")
    require("og:site_name", tags["og:site_name"], project)
    require("og:locale", tags["og:locale"], render_overview.SITE_LOCALE)

    description = tags["description"]
    if description is not None:
        limit = render_overview.DESCRIPTION_LIMIT
        if not description.strip():
            problems.append("the description is empty")
        elif len(description) > limit:
            problems.append(f"the description is {len(description)} characters, over {limit}")
        require("og:description", tags["og:description"], description)
        require("twitter:description", tags["twitter:description"], description)

    kind = tags["og:type"]
    if kind is not None and kind not in ("website", "article"):
        problems.append(f"og:type is {kind!r}")
    for key in ARTICLE_META:
        moments = head.meta(key)
        if len(moments) > 1 or (moments and kind != "article"):
            problems.append(f"{len(moments)} {key} tags on a page whose og:type is {kind!r}")
        problems += [
            f"{key} is {moment!r}, not an ISO date"
            for moment in moments
            if not _ISO_DATE.fullmatch(moment)
        ]

    image = render_overview.social_card_url()
    require("og:image", tags["og:image"], image)
    require("twitter:image", tags["twitter:image"], image)
    require("og:image:type", tags["og:image:type"], "image/png")
    require("og:image:width", tags["og:image:width"], str(render_overview.SOCIAL_CARD_WIDTH))
    require("og:image:height", tags["og:image:height"], str(render_overview.SOCIAL_CARD_HEIGHT))
    alt = tags["og:image:alt"]
    if alt is not None and not alt.strip():
        problems.append("og:image:alt is empty")
    require("twitter:image:alt", tags["twitter:image:alt"], alt or "")
    require("twitter:card", tags["twitter:card"], "summary_large_image")
    # Stable SVG/PNG icons are resolved from each page's address. The standalone
    # workbench artifact keeps its approved inline SVG under its isolated CSP.
    icons = head.link("icon")
    expected_icons = {
        render_overview.SITE_URL + "favicon.svg",
        render_overview.SITE_URL + "favicon-48.png",
    }
    resolved = [urljoin(page_url or canonical, icon) for icon in icons]
    inline_workbench = (
        (allow_inline_favicon or canonical == render_overview.canonical_url(WORKBENCH_PAGE))
        and len(icons) == 1
        and icons[0] == render_overview.favicon_url()
    )
    if not inline_workbench:
        if len(icons) != 2:
            problems.append(f"{len(icons)} icon links, expected the SVG/PNG pair")
        elif set(resolved) != expected_icons:
            problems.append("the icon is not the site's SVG/PNG pair")
        apple = [urljoin(page_url or canonical, icon) for icon in head.link("apple-touch-icon")]
        if apple != [render_overview.SITE_URL + "apple-touch-icon.png"]:
            problems.append("the apple-touch icon is missing or not the site's")
    return problems


#: What a forwarder's preview says of the page it leads to, which the page's own head
#: says too: its name, its kind and its sentence. The rest of the set either follows from
#: these (`twitter:title`, the descriptions) or is the site's, which `head_problems` holds.
PREVIEWED = ("og:title", "og:type", "og:description")


def forwarder_problems(
    text: str,
    canonical: str,
    destination: str | None = None,
    *,
    allow_inline_favicon: bool = False,
    page_url: str | None = None,
) -> list[str]:
    """What is wrong with the head of a page that only sends a reader on to `canonical`,
    by the rule `render_overview.forwarder_head` writes it to.

    To a page of the site, it previews that page: the whole set a page's head carries,
    held as one is (`head_problems`), at `canonical`, so its canonical link and `og:url`
    are where it leads. `destination` is that page's text where the check has it, and
    then the forwarder's name, kind and description (`PREVIEWED`) are the ones the page's
    own head gives, so a shared old address does not preview the page under another
    name. Off the site, it names `canonical`, in full and once, and carries no preview,
    since the site does not write the page it would describe.
    """
    if canonical.startswith(render_overview.SITE_URL):
        problems = head_problems(
            text, canonical, allow_inline_favicon=allow_inline_favicon, page_url=page_url
        )
        if destination is not None:
            # A tag the page does not give once is the page's own failure, named there.
            head, page = read_head(text), read_head(destination)
            problems += [
                f"its {key} is {head.meta(key)}, and the page's own is {own}"
                for key in PREVIEWED
                if len(own := page.meta(key)) == 1 and head.meta(key) != own
            ]
        return problems
    head = read_head(text)
    found = head.link("canonical")
    problems = []
    if found != [canonical]:
        problems.append(f"its canonical links are {found}, not [{canonical!r}]")
    if not canonical.startswith("https://"):
        problems.append(f"{canonical!r} is not an address in full")
    cards = sorted({key for key, _ in head.metas if key.startswith(("og:", "twitter:"))})
    if cards:
        problems.append(f"it carries card tags: {cards}")
    return problems


def shared_descriptions(pages: Mapping[str, str]) -> list[str]:
    """Every description two or more of `pages` (text by name) carry, with the pages that
    do: a preview that says the same of two pages says nothing of either."""
    by_description: dict[str, list[str]] = {}
    for name, text in pages.items():
        for description in read_head(text).meta("description"):
            by_description.setdefault(description, []).append(name)
    return [
        f"{', '.join(names)}: {description!r}"
        for description, names in by_description.items()
        if len(names) > 1
    ]


#: How many of the case records whose heads are wrong one line names; the count says how
#: many there are in all.
RECORD_PROBLEMS_SHOWN = 3


def head_checks(
    pages: Mapping[str, str],
    forwarders: Mapping[str, tuple[str, str]],
    card: bytes | None,
    records: Mapping[str, str] | None = None,
) -> list[tuple[bool, str]]:
    """The identity and link-preview checks as (passed, line), on text already in hand.

    `pages` is each page that can be shared, by the path it is served at under the root
    (`index.html`, `workbench/index.html`); `records` is each case's record file, by its
    path (`cases/11.html`), held as a page is and reported in one line, since there are
    hundreds; `forwarders` is each page that only sends a reader on, as its text and the
    canonical address it should name, held to the head of the page at that address when
    `pages` has it (`forwarder_problems`); `card` is the bytes served as the site's card, or
    `None` when nothing was. The deployed site and a directory a preview built are both
    read through this.
    """
    records = records or {}
    results: list[tuple[bool, str]] = []
    for name, text in pages.items():
        problems = head_problems(text, render_overview.canonical_url(name))
        line = (
            f"{name}: head: {'; '.join(problems)}"
            if problems
            else f"{name}: one of each identity and card tag, agreeing with its address"
        )
        results.append((not problems, line))
    if records:
        wrong = {
            name: problems
            for name, text in records.items()
            if (problems := head_problems(text, render_overview.canonical_url(name)))
        }
        shown = list(wrong.items())[:RECORD_PROBLEMS_SHOWN]
        results.append(
            (
                not wrong,
                f"case records: {len(wrong)} of {len(records)} heads wrong: "
                + " | ".join(f"{name}: {'; '.join(problems)}" for name, problems in shown)
                if wrong
                else f"case records: each of {len(records)} carries one of each identity and "
                "card tag, agreeing with its address",
            )
        )
    described = {**pages, **records}
    shared = shared_descriptions(described)
    results.append(
        (
            not shared,
            f"descriptions shared between pages: {'; '.join(shared)}"
            if shared
            else f"each of {len(described)} pages has a description of its own",
        )
    )
    # A forwarder to a page of the site is held to that page's own head where it is here.
    by_address = {render_overview.canonical_url(name): text for name, text in pages.items()}
    for name, (text, canonical) in forwarders.items():
        destination = by_address.get(canonical)
        problems = forwarder_problems(
            text, canonical, destination, page_url=render_overview.SITE_URL + name
        )
        within = canonical.startswith(render_overview.SITE_URL)
        line = (
            f"forwarder {name}: head: {'; '.join(problems)}"
            if problems
            else f"forwarder {name}: names {canonical} as canonical, and carries no card"
            if not within
            else f"forwarder {name}: previews {canonical} as that page's own head does"
            if destination is not None
            else f"forwarder {name}: previews {canonical}, whose page is not here to compare"
        )
        results.append((not problems, line))
    address = render_overview.SOCIAL_CARD
    if card is None:
        results.append((False, f"card {address}: not served"))
    else:
        problems = social_card.card_problems(card)
        size = social_card.png_dimensions(card) or (0, 0)
        line = (
            f"card {address}: {'; '.join(problems)}"
            if problems
            else f"card {address}: a PNG of {size[0]}x{size[1]}, {len(card)} bytes"
        )
        results.append((not problems, line))
    return results


def forwarder_canonicals() -> dict[str, str]:
    """Each forwarder the site serves, by its path, and the canonical address it names:
    the renderer's (`render_overview.forwarder_pages`), each naming where its page went.
    The address the optimality paper's directory once had, `n11-optimality/`, is one of
    them, naming the paper where it is served now."""
    named: dict[str, str] = {}
    for forwarder in render_overview.forwarder_pages():
        found = read_head(forwarder.html).link("canonical")
        named[forwarder.name] = found[0] if found else ""
    return named


def shared_pages() -> tuple[str, ...]:
    """Every page of the site that can be shared, by the path it is served at: the
    renderer's own pages, every paper and the workbench."""
    return (*SITE_PAGES, LOWER_BOUNDS_PAPER, *REVIEW_PAPERS, WORKBENCH_PAGE)


#: A link from one paper's page to another's, as `devtools.paper_links` fills it on the
#: page: the target's page beside it, with a heading's anchor or none.
_PAPER_PAGE_LINK = re.compile(r'href="(?P<slug>[a-z0-9-]+)\.html(?:#(?P<anchor>[^"]*))?"')
#: The same link in a Markdown edition: the target's page at the site's address.
_PAPER_MARKDOWN_LINK = re.compile(
    r"\]\("
    + re.escape(render_overview.SITE_URL + render_overview.PAPERS_DIR + "/")
    + r"(?P<slug>[a-z0-9-]+)\.html(?:#(?P<anchor>[^)\s]*))?\)"
)
#: A heading's id, which is what a link between papers may name.
_HEADING_ID = re.compile(r'<h[1-6]\b[^>]*\sid="([^"]+)"')


def heading_ids(page: str) -> frozenset[str]:
    """The ids of a paper's headings: the anchors a link from another paper may name."""
    return frozenset(_HEADING_ID.findall(page))


def cross_paper_link_checks(
    pages: Mapping[str, str], markdowns: Mapping[str, str]
) -> list[tuple[bool, str]]:
    """Every link from one paper to another, on each page in `pages` and in each Markdown
    edition in `markdowns` (each by the path it is served at), against the target: a
    paper of the site whose page is among `pages`, and, where the link names an anchor,
    one of that page's headings (`devtools.paper_links`). A link to a paper whose page
    is not there is reported and not failed, as a build that skipped it would otherwise
    always fail; one to a page the site does not serve fails. One line per source."""
    slugs = {
        paper.slug: render_overview.paper_path(paper.slug) for paper in render_overview.PAPERS
    }
    ids = {path: heading_ids(text) for path, text in pages.items()}
    results: list[tuple[bool, str]] = []
    sources = [(path, text, _PAPER_PAGE_LINK) for path, text in pages.items()]
    sources += [(path, text, _PAPER_MARKDOWN_LINK) for path, text in markdowns.items()]
    for source, text, pattern in sources:
        found = [
            (match["slug"], match["anchor"])
            for match in pattern.finditer(text)
            if pattern is _PAPER_MARKDOWN_LINK or match["slug"] in slugs
        ]
        if not found:
            continue
        broken: list[str] = []
        unbuilt: set[str] = set()
        for slug, anchor in found:
            target = slugs.get(slug)
            if target is None:
                broken.append(f"{slug}.html, no paper of the site")
            elif target not in ids:
                unbuilt.add(target)
            elif anchor and anchor not in ids[target]:
                broken.append(f"{target}#{anchor}, no heading of that paper")
        line = f"{source}: {len(found)} links to other papers"
        if broken:
            line += f", {len(broken)} broken: {broken[:5]}"
        elif unbuilt:
            line += f", to {sorted(unbuilt)} not in this build, so not checked"
        else:
            line += ", each to a paper served here and a heading it has"
        results.append((not broken, line))
    return results


#: A case's record file, by its path under the site's root.
_RECORD_FILE = re.compile(rf"{re.escape(render_case_pages.CASES_DIR)}/\d+\.html")


#: A shared asset as a page names it (`site_assets`), from wherever the page is served;
#: a face as a shared stylesheet names it, from beside it; and a shared file's name, which
#: carries the first sixteen hex digits of its bytes' SHA-256 (`content_hash`).
_ASSET_REFERENCE = re.compile(r'(?:href|src)="((?:\.\./)*assets/[^"#?]+)"')
_FACE_REFERENCE = re.compile(r'url\("(\.\./fonts/[^"]+)"\)')
_HASHED_NAME = re.compile(r"\.([0-9a-f]{16})\.[a-z0-9]+$")


def asset_checks(
    pages: Mapping[str, str], read: Callable[[str], bytes | None]
) -> list[tuple[bool, str]]:
    """Every shared asset `pages` name, and every face a named stylesheet names, is
    served with the bytes its name was given for. `pages` are by their path from the
    site's root, and `read` gives a file's bytes by its path from there, or `None`
    where nothing is served. One line, since a site's pages name the same few dozen."""
    named: dict[str, str] = {}
    for name, text in pages.items():
        for href in _ASSET_REFERENCE.findall(text):
            named.setdefault(
                posixpath.normpath(posixpath.join(posixpath.dirname(name), href)), name
            )
    if not named:
        return [(True, "shared assets: no page here names one")]
    problems: list[str] = []
    served = 0
    pending = sorted(named)
    seen: set[str] = set()
    while pending:
        path = pending.pop()
        if path in seen:
            continue
        seen.add(path)
        data = read(path)
        if data is None:
            problems.append(f"{path}, named by {named[path]}, is not served")
            continue
        stamp = _HASHED_NAME.search(path)
        if stamp is None or hashlib.sha256(data).hexdigest()[:16] != stamp.group(1):
            problems.append(f"{path} is not the bytes its name was given for")
            continue
        served += 1
        if path.endswith(".css"):
            for face in _FACE_REFERENCE.findall(data.decode("utf-8", errors="replace")):
                target = posixpath.normpath(posixpath.join(posixpath.dirname(path), face))
                named.setdefault(target, path)
                pending.append(target)
    if problems:
        return [(False, f"shared assets: {'; '.join(problems[:5])}")]
    return [(True, f"shared assets: each of {served} files the pages name is served whole")]


def local_head_checks(directory: Path) -> list[tuple[bool, str]]:
    """`head_checks` on a site built into `directory`, as `devtools.preview_site` leaves
    one. A page a build left out is reported and not failed, as a preview that skipped
    a slow build would otherwise always fail; the card is required wherever a file that
    names it is there, a page, a record or a forwarder to a page of the site.

    Every HTML file there that is a document (`is_document`) is held, not only the pages
    this module names: a forwarder by its rule, a case's record file as a page, and any
    other file as the page it is, at the address it is served at, so a page a build adds
    later fails here until it carries the set, however little its head says. A file that
    is no document, a result's overview, is a fragment.
    """

    def text(name: str) -> str | None:
        path = directory / name
        return path.read_text(encoding="utf-8") if path.is_file() else None

    withdrawn = (
        {row.path for row in site_urls.load_registry() if row.status == "withdrawn"}
        if site_urls.REGISTRY.is_file()
        else set()
    )
    pages = {name: text(name) for name in shared_pages() if name not in withdrawn}
    forwarders = {
        name: (text(name), canonical) for name, canonical in forwarder_canonicals().items()
    }
    card = directory / render_overview.SOCIAL_CARD
    built = {name: found for name, found in pages.items() if found is not None}
    records: dict[str, str] = {}
    for path in sorted(directory.rglob("*.html")):
        name = path.relative_to(directory).as_posix()
        if name == "404.html" or name in withdrawn:
            continue
        if name in pages or name in forwarders:
            continue
        found = path.read_text(encoding="utf-8")
        if not is_document(found):
            continue
        (records if _RECORD_FILE.fullmatch(name) else built)[name] = found
    present = {
        name: (found, to) for name, (found, to) in forwarders.items() if found is not None
    }
    results = head_checks(
        built, present, card.read_bytes() if card.is_file() else None, records
    )
    # The card is written with the site's own pages. A build that has none of them, no
    # record and no forwarder to a page of the site names no card, so it misses none.
    carded = any(to.startswith(render_overview.SITE_URL) for _, to in present.values())
    if not built and not records and not carded and not card.is_file():
        results[-1] = (True, f"card {render_overview.SOCIAL_CARD}: not in this build")
    absent = [name for name, found in pages.items() if found is None]
    absent += [name for name, (found, _) in forwarders.items() if found is None]
    results += [(True, f"{name}: not in this build, so not checked") for name in absent]
    papers = (LOWER_BOUNDS_PAPER, *REVIEW_PAPERS)
    markdowns = {paper_files(paper)[0]: text(paper_files(paper)[0]) for paper in papers}
    results += cross_paper_link_checks(
        {paper: found for paper in papers if (found := pages[paper]) is not None},
        {name: found for name, found in markdowns.items() if found is not None},
    )

    def served(path: str) -> bytes | None:
        found = directory / path
        return found.read_bytes() if found.is_file() else None

    if missing_page := text("404.html"):
        built["404.html"] = missing_page.replace(
            urlsplit(render_overview.SITE_URL).path + "assets/", "assets/"
        )
    return results + asset_checks(built, served)


def head_inventory(directory: Path) -> list[str]:
    """What every HTML file of a built site carries in its head, one file to a block:
    its language, title, canonical link and every `<meta>` a tab, a search engine or a
    link preview reads, in the head's order. The table a change to the heads is read
    against, before and after; the result overviews, sixty-one files with no head, are
    one line."""
    lines: list[str] = []
    fragments = 0
    for path in sorted(directory.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        if not is_document(text):
            fragments += 1
            continue
        head = read_head(text)
        lines.append(f"{path.relative_to(directory).as_posix()}  lang={head.lang!r}")
        lines += [f"  title: {title}" for title in head.titles]
        lines += [
            f"  link {rel}: {href if len(href) <= 100 else href[:60] + '…'}"
            for rel, href in head.links
        ]
        lines += [
            f"  {key}: {content}"
            for key, content in head.metas
            if key not in {"viewport", "color-scheme", "generator", "Content-Security-Policy"}
        ]
    lines.append(f"{fragments} files with no head (fragments fetched into a popover)")
    return lines


class RecordLinks(NamedTuple):
    """What the renderer writes from the register, for the deployed pages to be held to."""

    rows: dict[str, str]
    """Each result's record links as a table row carries them (`Result.records`), by the
    row's name (`t-060`): their addresses, one to a line."""
    overviews: dict[str, str]
    """The rendered overview of each result of `RECORD_LINK_SAMPLE`, by its address
    beside the pages (`result/t-060.html`)."""


def rendered_record_links() -> RecordLinks:
    """The record links as the renderer writes them from this checkout's register.

    These are the functions the pages are rendered with, `overview_data.load` for a row's
    records and `result_overview.result_popover_html` for an overview, so what is
    expected of the deploy is what a render of the same commit produces, and nothing is
    restated here. They resolve a cited path against the commit (`repo_links.path_kind`),
    so the answer does not depend on whether this checkout is partial. The sample has to
    cite something under a directory of each omitted tree, or it would pass a deploy
    that dropped those links again; a register that no longer does that fails here.
    """
    overview = overview_data.load()
    results = {result.id: result for result in overview.results}
    unknown = [result for result in RECORD_LINK_SAMPLE if result not in results]
    if unknown:
        raise SystemExit(f"the register has no {', '.join(unknown)} to sample")
    overviews = {
        result_fragment(result): result_overview.result_popover_html(results[result], overview)
        for result in RECORD_LINK_SAMPLE
    }
    cited = {path for body in overviews.values() for _, path in branch_paths(body)}
    for tree in OMITTED_TREES:
        # A file directly under the tree is in every checkout; one a directory down is not.
        if not any(path.startswith(tree) and "/" in path.removeprefix(tree) for path in cited):
            raise SystemExit(
                f"the overviews of {', '.join(RECORD_LINK_SAMPLE)} cite nothing under a "
                f"directory of {tree}: sample a result that does"
            )
    rows = {
        result.id.lower(): "\n".join(link.url for link in result.records)
        for result in overview.results
    }
    return RecordLinks(rows, overviews)


def absent_links(rendered: str, published: str) -> list[str]:
    """Every repository path `rendered` links on `main` that `published` does not, as
    `kind/path`: what a deploy dropped."""
    return sorted(
        f"{kind}/{path}" for kind, path in branch_paths(rendered) - branch_paths(published)
    )


def row_records(page: str) -> dict[str, str]:
    """The line of record links each result row of a page's table of results opens to,
    in the short form of the row's popover, by the result's name. A popover is read from
    its own opening tag to the next popover's, so one that lost its line is not given
    its neighbour's. The rows carried the line in a Details cell until 2026-10-04."""
    found: dict[str, str] = {}
    for popover in page.split('<div class="site-popover ')[1:]:
        named = _RESULT_POPOVER.match(popover)
        records = _ROW_RECORDS.search(popover)
        if named is not None and records is not None:
            found[named.group(1)] = records.group(1)
    return found


def checkout_commit() -> str | None:
    """The commit this checkout is at, which is the register the expectation is read from."""
    found = subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=REPO, capture_output=True, text=True, check=False
    )
    return found.stdout.strip() if found.returncode == 0 else None


def record_link_checks(
    expected: RecordLinks,
    pages: Mapping[str, str],
    overviews: Mapping[str, str],
    *,
    rendered_at: str = "",
) -> list[tuple[bool, str]]:
    """The record-link checks as (passed, line): each page of `pages`, a served page with a
    table of results by name, and each sampled overview of `overviews`, the served
    overviews by address, against what the renderer writes. `rendered_at` ends a failing
    line where the expectation was not rendered at the deployed commit, since a failure
    may then be the checkout's and not the deploy's."""
    results: list[tuple[bool, str]] = []
    for name, text in pages.items():
        served = row_records(text)
        lacking = {
            row: absent
            for row, records in expected.rows.items()
            if (absent := absent_links(records, served.get(row, "")))
        }
        total = sum(len(branch_paths(records)) for records in expected.rows.values())
        if lacking:
            shown = "; ".join(
                f"{row} lacks {absent[:3]}" for row, absent in list(lacking.items())[:3]
            )
            line = (
                f"{name}: {len(lacking)} of {len(expected.rows)} result rows lack record "
                f"links the renderer writes: {shown}{rendered_at}"
            )
        else:
            line = (
                f"{name}: each of {len(expected.rows)} result rows carries its record "
                f"links, {total} in all"
            )
        results.append((not lacking, line))
    for address, rendered in expected.overviews.items():
        count = len(branch_paths(rendered))
        if address not in overviews:
            results.append(
                (
                    False,
                    f"result overview {address}: sampled for its record links and not served",
                )
            )
            continue
        absent = absent_links(rendered, overviews[address])
        line = (
            f"result overview {address}: lacks {len(absent)} of the {count} repository links "
            f"the renderer writes for it: {absent[:5]}{rendered_at}"
            if absent
            else f"result overview {address}: carries the {count} repository links the "
            "renderer writes for it"
        )
        results.append((not absent, line))
    return results


def repository_links(text: str) -> set[tuple[str, str, str]]:
    """Every (kind, ref, path) the text links into the repository, scripts and styles aside."""
    markup = re.sub(r"<(script|style)\b.*?</\1>", "", text, flags=re.DOTALL | re.IGNORECASE)
    return {
        (kind, ref, path.rstrip("/")) for kind, ref, path in REPOSITORY_LINK.findall(markup)
    }


def paper_citations(text: str, commit: str) -> tuple[set[tuple[str, str]], list[str]]:
    """The optimality paper's repository links: each (kind, path) it cites at `commit`,
    without any query or anchor, and every link that names another ref, `main` among
    them, as `kind/ref/path`. The paper pins its citations to the commit it was built
    from (`render_n11_optimality_review.link_revision`), and the deploy builds it
    from the commit it deploys."""
    cited: set[tuple[str, str]] = set()
    strays: list[str] = []
    for kind, ref, path in sorted(repository_links(text)):
        if ref == commit:
            cited.add((kind, re.split(r"[?#]", path, maxsplit=1)[0].rstrip("/")))
        else:
            strays.append(f"{kind}/{ref}/{path}")
    return cited, strays


def pdf_pages(data: bytes) -> int:
    """The number of page objects a PDF declares; 0 when the bytes are not a PDF."""
    if not data.startswith(b"%PDF"):
        return 0
    return len(re.findall(rb"/Type\s*/Page(?![s])", data))


def pdf_source_matches(data: bytes, page: bytes) -> bool:
    """Whether the PDF's unique trailing source receipt names the exact fetched HTML."""
    receipt = re.search(rb"\n%sqpack-source-html-sha256: ([0-9a-f]{64})\n\Z", data)
    return (
        receipt is not None
        and data.count(b"%sqpack-source-html-sha256:") == 1
        and receipt[1] == hashlib.sha256(page).hexdigest().encode()
    )


#: The pauses, in seconds, before each retry of a transient answer. This runs straight after
#: a deploy reports success, when Pages can still answer 404 or 5xx for a short while, so a
#: single fetch failed a good deploy on timing alone (#160 R26). Thirty seconds in all.
RETRY_DELAYS = (2.0, 4.0, 8.0, 16.0)
#: Answers worth asking again: unreachable (0), not yet there, throttled, or a server error.
TRANSIENT_STATUSES = frozenset({0, 404, 408, 429, 500, 502, 503, 504})


#: A site this machine serves, as `devtools.preview_site --serve` does: the one kind of
#: address that is not https and is still asked, so a build can be checked before it is
#: deployed. GitHub is always asked over https.
LOCAL_SITE = re.compile(r"http://(?:127\.0\.0\.1|localhost)(?::\d+)?/")


def fetch_once(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
    """The status and body of a GET (or the status alone of a HEAD); 0 when unreachable."""
    if not (url.startswith("https://") or LOCAL_SITE.match(url)):
        raise ValueError(f"refusing to fetch a URL that is neither https nor local: {url}")
    request = urllib.request.Request(
        url, method="HEAD" if head else "GET", headers={"User-Agent": USER_AGENT}
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, b"" if head else response.read()
    except urllib.error.HTTPError as error:
        return error.code, b""
    except urllib.error.URLError:
        return 0, b""


def fetch(
    url: str,
    *,
    head: bool = False,
    timeout: float = 30.0,
    delays: Sequence[float] = RETRY_DELAYS,
    sleep: Callable[[float], object] = time.sleep,
) -> tuple[int, bytes]:
    """`fetch_once`, asked again after each delay while the answer is transient.

    The last answer is returned whatever it is, so a page that stays missing still fails
    its check, only later.
    """
    answer = fetch_once(url, head=head, timeout=timeout)
    for delay in delays:
        if answer[0] not in TRANSIENT_STATUSES:
            break
        sleep(delay)
        answer = fetch_once(url, head=head, timeout=timeout)
    return answer


def expected_commit() -> str:
    """`origin/main` as the checkout knows it, which is what the last deploy built from."""
    found = subprocess.run(
        ("git", "rev-parse", "origin/main"),
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    if found.returncode != 0:
        raise SystemExit("no --commit given and origin/main cannot be resolved here")
    return found.stdout.strip()


def workbench_startup(url: str, project_root: str, *, timeout: float) -> tuple[bool, str]:
    """Start the deployed page and require its public API and project-root navigation."""
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            try:
                page = browser.new_page()
                page.goto(url, wait_until="load", timeout=timeout * 1000)
                page.wait_for_function(
                    probe(PROBES, "check_published_site/api-ready"),
                    timeout=timeout * 1000,
                )
                observed = page.evaluate(probe(PROBES, "check_published_site/startup"))
            finally:
                browser.close()
    except PlaywrightError as error:
        return False, f"workbench startup failed: {error}"
    pairs = observed.get("pairs") if isinstance(observed, dict) else None
    home = observed.get("home") if isinstance(observed, dict) else None
    passed = isinstance(pairs, int) and pairs > 0 and home == project_root
    return passed, f"workbench API started with {pairs!r} pairs; home resolved to {home!r}"


def forwarder_says(text: str) -> dict[str, str | None]:
    """Where a forwarder says its page is now, in each of the four places it says it:
    its canonical URL, the address its script reads, its refresh, and its link."""
    places = (
        ("canonical", CANONICAL),
        ("script", MOVED_TO),
        ("refresh", REFRESH),
        ("link", MOVED_LINK),
    )
    found = {name: pattern.search(text) for name, pattern in places}
    return {
        name: match.group(1) if match is not None else None for name, match in found.items()
    }


def forwarder_expected(old: str, new: str) -> dict[str, str | None]:
    """What `forwarder_says` has to answer for the page that moved from `old` to `new`:
    the new address in full as the canonical URL, and relative to the old one elsewhere.
    An address off the site, as the defect log's on GitHub is, is whole in all four."""
    new = site_urls.canonical_path(new)
    external = new.startswith("https://")
    target = new if external else posixpath.relpath(new, posixpath.dirname(old))
    if not external and new.endswith("/"):
        target += "/"
    return {
        "canonical": new if external else render_overview.canonical_url(new),
        "script": target,
        "refresh": target,
        "link": target,
    }


def visited_address(old: str) -> str:
    """The address a reader has for a page that moved: a directory's `index.html` is
    linked as its directory."""
    return old.removesuffix("index.html")


def forwarder_arrivals(
    browser: Browser | BrowserContext, site: str, *, timeout: float
) -> list[tuple[bool, str]]:
    """Visit each address a page used to have in `browser`, with a query string and a
    fragment, and require it to arrive where the page is now with both: a page of the
    site, or for a page that left it the address off the site it is sent to. The arrival
    is the address the browser commits to, so a slow page at the far end is not waited
    for."""
    results: list[tuple[bool, str]] = []
    for old, new in render_overview.MOVED_PAGES:
        start = site + visited_address(old) + FORWARDED_SUFFIX
        arrival = (
            new if new.startswith("https://") else site + site_urls.canonical_path(new)
        ) + FORWARDED_SUFFIX
        page = browser.new_page()
        try:
            page.goto(start, wait_until="load", timeout=timeout * 1000)
            page.wait_for_url(arrival, wait_until="commit", timeout=timeout * 1000)
        except PlaywrightError:
            pass  # Where the visit is now says what went wrong.
        landed = page.url
        page.close()
        results.append(
            (landed == arrival, f"visiting {start} arrives at {landed!r}, expected {arrival!r}")
        )
    return results


def forwarders_followed(site: str, *, timeout: float) -> list[tuple[bool, str]]:
    """`forwarder_arrivals` in the pinned browser. `SQPACK_CHROMIUM` names a browser the
    environment supplies, as the other browser tools read it."""
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                executable_path=os.environ.get(BROWSER_OVERRIDE)
            )
            try:
                return forwarder_arrivals(browser, site, timeout=timeout)
            finally:
                browser.close()
    except PlaywrightError as error:
        return [(False, f"the forwarders could not be visited: {error}")]


def deployed_registry_checks(
    site: str,
    read: Callable[..., tuple[int, bytes]],
    *,
    timeout: float,
    rows: Sequence[site_urls.SiteURL] | None = None,
) -> list[tuple[bool, str]]:
    """Fetch every retained non-asset URL, including all cases and result pages.

    The registry owns the complete walk. The specialized paper/citation checks below
    share its response cache and retain their stronger content assurance.
    """
    rows = list(rows) if rows is not None else site_urls.load_registry()
    results = site_urls.validate_registry(rows)
    site = site.rstrip("/") + "/"
    pages: dict[str, str] = {}
    forwarded: dict[str, tuple[str, str]] = {}
    records: dict[str, str] = {}
    for row in rows:
        if row.pattern or row.kind == "asset-file":
            continue
        status, body = read(site + row.path, timeout=timeout)
        results.append(
            (status == 200, f"registered {row.path}: HTTP {status}, {len(body)} bytes")
        )
        if status != 200:
            continue
        if row.kind == "copy":
            target_status, target_body = read(site + row.target, timeout=timeout)
            results.append(
                (
                    target_status == 200 and body == target_body,
                    f"registered copy {row.path}: same bytes as {row.target}",
                )
            )
        if not row.path.endswith(".html"):
            continue
        budget = site_urls.page_budget(row)
        results.append(
            (
                len(body) <= min(budget, site_urls.HARD_HTML_LIMIT),
                f"registered HTML {row.path}: {len(body)} bytes, budget {budget}",
            )
        )
        text = body.decode("utf-8", errors="replace")
        if row.status == "withdrawn" or row.path == "404.html":
            results.append(
                (
                    bool(read_head(text).meta("robots"))
                    and "noindex" in read_head(text).meta("robots")[0]
                    and "<main>" in text
                    and "<h1>" in text,
                    f"registered {row.path}: complete noindex disposition page",
                )
            )
            continue
        canonical = (
            row.canonical
            if row.canonical.startswith("https://")
            else render_overview.SITE_URL + row.canonical
        )
        if row.status == "forwarded":
            forwarded[row.path] = (text, canonical)
            declared = forwarder_says(text)
            expected = forwarder_expected(row.path, row.target)
            results.append(
                (
                    declared == expected,
                    f"registered forwarder {row.path}: all redirect targets agree",
                )
            )
            if not row.target.startswith("https://"):
                target_status, _ = read(site + row.target, timeout=timeout)
                results.append(
                    (
                        target_status == 200,
                        f"registered forwarder {row.path}: target served HTTP {target_status}",
                    )
                )
        elif row.kind == "record":
            records[row.path] = text
        else:
            pages[row.path] = text
    card_status, card = read(site + render_overview.SOCIAL_CARD, timeout=timeout)
    results += head_checks(pages, forwarded, card if card_status == 200 else None, records)
    return results


def local_site_checks(
    directory: Path, *, partial: bool = False, producers: Sequence[str] = ()
) -> list[tuple[bool, str]]:
    """Explicit producer contract, then every present page's head and linked assets."""
    from devtools.check_site_scripts import inventory  # noqa: PLC0415

    scripts, script_failures = inventory(directory)
    script_checks = [(False, error) for error in script_failures] or [
        (True, f"script inventory: {len(scripts)} reviewed declarations")
    ]
    return (
        site_urls.check_site(directory, partial=partial, producers=producers)
        + local_head_checks(directory)
        + script_checks
    )


def check(
    site: str,
    commit: str,
    *,
    timeout: float,
    browser: bool = True,
) -> list[tuple[bool, str]]:
    """Every check as (passed, line), in the order they are printed."""
    cache: dict[tuple[str, bool], tuple[int, bytes]] = {}

    def read(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
        key = (url, head)
        if head and (url, False) in cache:
            return cache[(url, False)]
        if key not in cache:
            cache[key] = fetch(url, head=head, timeout=timeout)
        return cache[key]

    results = deployed_registry_checks(site, read, timeout=timeout)
    site = site.rstrip("/") + "/"

    def served_page(
        name: str, url: str, canonical: str, *, version: str = PUBLICATION_EDITION
    ) -> tuple[bytes, str]:
        """Fetch one page and check it is served, stamped and canonical; its bytes and text.

        `version` is what the page must print: the site's edition on a site page, and a
        paper's own version on a paper, which must then not carry the site's edition
        (the owner, 2026-10-01: papers are individually versioned).
        """
        status, body = read(url, timeout=timeout)
        text = body.decode("utf-8", errors="replace")
        results.append((status == 200, f"page {url}: HTTP {status}, {len(body)} bytes"))
        # The shared version (think-qsuu), pinned in release.py: a site page names the
        # data it was drawn from, as the atlas and the videos do, whatever commit built
        # it. The commit is still what the workbench's source revision must name.
        stamped = version in text
        where = f"{'' if stamped else 'not '}on {name}"
        results.append((stamped, f"version {version!r} is {where}"))
        if version != PUBLICATION_EDITION:
            absent = PUBLICATION_EDITION not in text
            results.append(
                (
                    absent,
                    (
                        f"the site's edition {PUBLICATION_EDITION!r} is "
                        f"{'not ' if absent else ''}on {name}, which carries its own version"
                    ),
                )
            )
        found = CANONICAL.search(text)
        declared = found.group(1) if found is not None else None
        results.append(
            (
                declared == canonical,
                f"{name} names canonical URL {declared!r} against expected {canonical!r}",
            )
        )
        return body, text

    try:
        tree: RepositoryTree | None = repository_tree(commit)
    except SystemExit as error:
        tree = None
        results.append((False, f"the tree of {commit} cannot be read here: {error}"))

    def links_main(name: str, text: str) -> None:
        """No link names a commit, and every path linked on `main` is in the tree."""
        pinned = hash_pinned_links(text)
        results.append(
            (
                not pinned,
                f"{name}: {len(pinned)} repository links pinned to a commit: {pinned[:5]}"
                if pinned
                else f"{name}: no repository link is pinned to a commit",
            )
        )
        if tree is None:
            return
        missing = tree.missing(branch_paths(text))
        results.append(
            (
                not missing,
                f"{name}: linked on main but not in {commit[:12]}: {missing[:5]}"
                if missing
                else f"{name}: every path linked on main is in {commit[:12]}",
            )
        )

    checked_links: set[tuple[str, str, str]] = set()
    overviews: list[str] = []
    tables: dict[str, str] = {}
    # Every page that can be shared and every forwarder, as served, for the head checks
    # at the end: they are read from the text fetched here and cost no request.
    heads: dict[str, str] = {}
    record_heads: dict[str, str] = {}
    forwarded: dict[str, tuple[str, str]] = {}
    canonicals = forwarder_canonicals()
    indexed: list[int] = []
    for name in SITE_PAGES:
        url = site if name == "index.html" else site + name
        _, text = served_page(name, url, render_overview.canonical_url(name))
        heads[name] = text
        links_main(name, text)
        if name in LINK_CHECKED_PAGES:
            checked_links |= repository_links(text)
        if name in RECORD_LINK_PAGES:
            tables[name] = text
        if name == render_overview.RESULTS_PAGE:
            overviews = sorted(set(ROW_SOURCE.findall(text)))
        if name == render_case_pages.CASES_PAGE:
            indexed = [int(n) for n, case in CASE_INDEX_LINK.findall(text) if n == case]

    # The result overviews are files beside the pages, fetched when a row is opened: a
    # deploy that lost one would show only as a popover that keeps its short detail.
    results.append(
        (
            bool(overviews),
            f"{render_overview.RESULTS_PAGE} names {len(overviews)} result overviews",
        )
    )
    bodies = []
    for address in overviews:
        status, body = read(site + address, timeout=timeout)
        fragment = body.decode("utf-8", errors="replace")
        found = RESULT_OVERVIEW.search(fragment)
        holds = None if found is None else result_fragment(found.group(1))
        results.append(
            (
                status == 200 and holds == address,
                f"result overview {address}: HTTP {status}, {len(body)} bytes"
                + ("" if holds == address else f", but it is {holds!r}"),
            )
        )
        bodies.append(fragment)
    if bodies:
        links_main("the result overviews", "\n".join(bodies))

    # The case records are files beside the record page, which it and every case popover
    # fetch: the index names each in order, and a sample of them is fetched.
    results.append(
        (
            bool(indexed) and indexed == list(range(1, len(indexed) + 1)),
            f"{render_case_pages.CASES_PAGE} indexes {len(indexed)} case records in order",
        )
    )
    sample = (
        sorted({indexed[0], RECORD_FILE_SAMPLE, indexed[-1]} & set(indexed)) if indexed else []
    )
    records: list[str] = []
    for n in sample:
        address = render_case_pages.case_url(n)
        status, body = read(site + address, timeout=timeout)
        record = body.decode("utf-8", errors="replace")
        found = CASE_RECORD.search(record)
        holds = None if found is None else int(found.group(1))
        results.append(
            (
                status == 200 and holds == n,
                f"case record {address}: HTTP {status}, {len(body)} bytes"
                + ("" if holds == n else f", but it holds {holds!r}"),
            )
        )
        if status == 200:
            # A record file is a page a reader shares: its head is held as a page's is,
            # and its links to the repository as the pages' are.
            record_heads[address] = record
            records.append(record)
    if records:
        links_main("the case records", "\n".join(records))

    # Every link above resolves; whether every link is there is asked of the renderer.
    try:
        expected = rendered_record_links()
    except SystemExit as error:
        results.append(
            (False, f"the record links cannot be rendered in this checkout: {error}")
        )
    else:
        head = checkout_commit()
        rendered_at = (
            ""
            if head == commit
            else f" (expected as rendered at {(head or 'no commit')[:12]}, not {commit[:12]})"
        )
        results.extend(
            record_link_checks(
                expected,
                tables,
                dict(zip(overviews, bodies, strict=True)),
                rendered_at=rendered_at,
            )
        )

    # The explainer's bytes are what the PDF's source receipt names, so they are kept whole.
    page, text = served_page(
        LOWER_BOUNDS_PAPER, site + LOWER_BOUNDS_PAPER, PAGE_URL, version=EXPLAINER_VERSION
    )
    current = PAPERS_CURRENT in text
    marked = f"Papers is {'' if current else 'not '}the bar's current entry"
    results.append((current, f"{LOWER_BOUNDS_PAPER}: {marked}, linked from a level below"))
    heads[LOWER_BOUNDS_PAPER] = text

    status, markdown = read(site + LOWER_BOUNDS_MARKDOWN, timeout=timeout)
    results.append(
        (
            status == 200,
            f"Markdown edition {LOWER_BOUNDS_MARKDOWN}: HTTP {status}, {len(markdown)} bytes",
        )
    )

    markdown_text = markdown.decode("utf-8", errors="replace")
    links_main(LOWER_BOUNDS_PAPER, text)
    links_main(LOWER_BOUNDS_MARKDOWN, markdown_text)
    checked_links |= repository_links(text) | repository_links(markdown_text)
    # This loop is where the check's time goes: one request to github.com for each distinct
    # link, in turn. On 2026-10-01 it was 614 of 783 checks and nearly all of a 14 m 47 s
    # run from a laptop, at 1.3 to 3.8 s a request (the deploy job's whole run took
    # 4 m 35 s). 558 of the 614 name `packing/frontier`, among them the 324 case files
    # and 170 line anchors into `results.yaml` and `evidence.yaml`, each anchor asked as an
    # address of its own though the files are two. The record-link checks above add no
    # request.
    for kind, ref, path in sorted(checked_links):
        url = f"{REPO_URL}/{kind}/{ref}/{path}"
        status, _ = read(url, head=True, timeout=timeout)
        results.append((status == 200, f"link HTTP {status}: {url}"))

    for name in SERVED:
        if name == LOWER_BOUNDS_MARKDOWN:
            continue
        head_only = name != LOWER_BOUNDS_PDF
        status, body = read(site + name, head=head_only, timeout=timeout)
        line = f"served {name}: HTTP {status}"
        ok = status == 200
        if name == LOWER_BOUNDS_PDF:
            pages = pdf_pages(body)
            source_matches = pdf_source_matches(body, page)
            ok = ok and pages == EXPECTED_PAGE_COUNT and source_matches
            line += f", {len(body)} bytes, {pages} pages (expected {EXPECTED_PAGE_COUNT})"
            line += ", source HTML receipt " + (
                "matches fetched page"
                if source_matches
                else "missing, malformed, or mismatched"
            )
        results.append((ok, line))

    def cites_commit(name: str, text: str) -> None:
        """The paper's rule, where every other page's is `links_main`: each repository
        link names the expected commit, and every path cited there is in its tree."""
        cited, strays = paper_citations(text, commit)
        results.append(
            (
                bool(cited) and not strays,
                f"{name}: {len(strays)} repository links not pinned to {commit[:12]}: "
                f"{strays[:5]}"
                if strays
                else f"{name}: {len(cited)} citations, each pinned to {commit[:12]}",
            )
        )
        if tree is None:
            return
        missing = tree.missing(cited)
        results.append(
            (
                not missing,
                f"{name}: cited at {commit[:12]} but not in its tree: {missing[:5]}"
                if missing
                else f"{name}: every cited path is in {commit[:12]}",
            )
        )

    # Every review, each as the optimality review has been checked since it was served:
    # its page with Papers current in its bar, its own version and not the site's, its
    # citations pinned to the commit, and its Markdown and PDF beside it.
    paper_pages = {LOWER_BOUNDS_PAPER: text}
    paper_markdowns = {LOWER_BOUNDS_MARKDOWN: markdown_text}
    for review in REVIEW_PAPERS:
        record = render_overview.paper_record(
            review.removeprefix("papers/").removesuffix(".html")
        )
        version = PAPER_VERSIONS[record.slug]
        status, paper = read(site + review, timeout=timeout)
        paper_text = paper.decode("utf-8", errors="replace")
        current = PAPERS_CURRENT in paper_text
        marked = f"Papers is {'' if current else 'not '}the bar's current entry"
        line = f"{record.label} {review}: HTTP {status}, {len(paper)} bytes, {marked}"
        results.append((status == 200 and current, line))
        if status == 200:
            # A review carries its own version and not the site's, as the explainer does.
            versioned = version in paper_text
            results.append(
                (versioned, f"version {version!r} is {'' if versioned else 'not '}on {review}")
            )
            unstamped = PUBLICATION_EDITION not in paper_text
            results.append(
                (
                    unstamped,
                    (
                        f"the site's edition {PUBLICATION_EDITION!r} is "
                        f"{'not ' if unstamped else ''}on {review}, which carries its "
                        "own version"
                    ),
                )
            )
            cites_commit(review, paper_text)
            paper_pages[review] = paper_text
        heads[review] = paper_text
        review_markdown, _ = paper_files(review)
        for name in paper_files(review):
            cited_here = name == review_markdown
            status, body = read(site + name, head=not cited_here, timeout=timeout)
            results.append((status == 200, f"served {name}: HTTP {status}"))
            if cited_here and status == 200:
                found = body.decode("utf-8", errors="replace")
                cites_commit(name, found)
                paper_markdowns[name] = found
    results.extend(cross_paper_link_checks(paper_pages, paper_markdowns))

    # No link written before a page moved or was withdrawn breaks: a page's old address
    # forwards, and a file's old address serves the same bytes. A deploy that dropped a
    # forwarder would 404 every link written before the change.
    for old, new in render_overview.MOVED_PAGES:
        status, body = read(site + old, timeout=timeout)
        moved_text = body.decode("utf-8", errors="replace")
        # Its head is read with the other pages' below, by the forwarders' rule.
        forwarded[old] = (moved_text, canonicals[old])
        says = forwarder_says(moved_text)
        expected = forwarder_expected(old, new)
        results.append(
            (
                status == 200 and says == expected,
                f"forwarder {old}: HTTP {status}, leads to {new}"
                if says == expected
                else f"forwarder {old}: HTTP {status}, says {says} against expected {expected}",
            )
        )
    for old, new in render_overview.MOVED_FILES:
        old_status, old_body = read(site + old, timeout=timeout)
        new_status, new_body = read(site + new, timeout=timeout)
        same = old_status == 200 and new_status == 200 and old_body == new_body
        verdict = "the same bytes as" if same else "not the bytes of"
        line = (
            f"moved file {old}: HTTP {old_status}, {len(old_body)} bytes, {verdict} {new} "
            f"(HTTP {new_status}, {len(new_body)} bytes)"
        )
        results.append((same, line))
    if browser:
        results.extend(forwarders_followed(site, timeout=timeout))

    workbench_url = site + WORKBENCH_PATH
    status, workbench = read(workbench_url, timeout=timeout)
    workbench_text = workbench.decode("utf-8", errors="replace")
    results.append(
        (
            status == 200,
            f"workbench {workbench_url}: HTTP {status}, {len(workbench)} bytes",
        )
    )
    stamped = WORKBENCH_REVISION.search(workbench_text)
    observed_revision = stamped.group(1) if stamped is not None else None
    results.append(
        (
            observed_revision == commit,
            f"workbench source revision {observed_revision!r} against expected {commit}",
        )
    )
    home = WORKBENCH_HOME.search(workbench_text)
    home_href = home.group(1) if home is not None else ""
    resolved_home = urljoin(workbench_url, home_href) if home_href else None
    results.append(
        (
            resolved_home == site,
            f"workbench home resolves to {resolved_home!r} against project root {site!r}",
        )
    )
    if browser:
        results.append(workbench_startup(workbench_url, site, timeout=timeout))

    # What every page says of itself to a tab, a search engine and a link preview, and
    # the one image they all name, which is served at the root of the site under test.
    heads[WORKBENCH_PAGE] = workbench_text
    status, card = read(site + render_overview.SOCIAL_CARD, timeout=timeout)
    results.extend(head_checks(heads, forwarded, card if status == 200 else None, record_heads))

    def served(path: str) -> bytes | None:
        status, body = read(site + path, timeout=timeout)
        return body if status == 200 else None

    return results + asset_checks(heads, served)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument(
        "--site", default=SITE_URL, help=f"the deployed site (default {SITE_URL})"
    )
    parser.add_argument("--commit", help="the full commit the deploy should have built from")
    parser.add_argument("--timeout", type=float, default=30.0, help="seconds per request")
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="skip the checks that open a browser, the workbench's API startup and the "
        "forwarders' arrival (HTTP identity checks still run)",
    )
    parser.add_argument(
        "--local",
        type=Path,
        metavar="DIR",
        help="check only the heads and the card of a site built into DIR; fetches nothing",
    )
    parser.add_argument(
        "--partial", action="store_true", help="with --local: selected producers only"
    )
    parser.add_argument(
        "--producer",
        action="append",
        default=[],
        help="selected producer (overview, workbench, paper:slug); requires --partial",
    )
    parser.add_argument(
        "--inventory",
        action="store_true",
        help="with --local: print what every file's head carries, and check nothing",
    )
    args = parser.parse_args(argv)
    if (args.partial or args.producer) and args.local is None:
        parser.error("--partial/--producer require --local")
    if args.inventory:
        if args.local is None:
            parser.error("--inventory reads a built site: give --local DIR")
        print("\n".join(head_inventory(args.local.resolve())))
        return 0
    if args.local is not None:
        try:
            results = local_site_checks(
                args.local.resolve(), partial=args.partial, producers=args.producer
            )
        except ValueError as error:
            parser.error(str(error))
    else:
        commit = args.commit or expected_commit()
        results = check(args.site, commit, timeout=args.timeout, browser=not args.no_browser)
    failed = 0
    for passed, line in results:
        print(f"{'ok  ' if passed else 'FAIL'} {line}", flush=True)
        failed += not passed
    print(f"{len(results) - failed} of {len(results)} checks passed", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
