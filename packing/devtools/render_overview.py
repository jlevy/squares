#!/usr/bin/env python3
"""Render the site's own pages: the overview, the frontier atlas and the tutorial.

The published site used to have one top-level page, the n = 11 explainer. This renderer
adds the front door and the pages around it, as the plan in
`docs/project/specs/active/plan-2026-09-29-github-pages-overview.md` lays out:

- `index.html`, the overview: the problem, the headline and recent results and the
  verification statistics, generated from the register;
- `all-results.html`, every registered result in one table, which the overview's cards
  and recent list point into by row (`#t-018`);
- `frontier.html`, the frontier atlas: one row for every case, from its
  `SquarePackingCase/v2` record;
- `cases/index.html`, the record page: the index of every case and the reader that shows
  one case's record file, `cases/N.html`, which this module writes beside it
  (`case_records`) and the atlas grid and the frontier table both open in their case
  popover (`render_case_pages`); `cases.html`, where every record was until 2026-10-03,
  is a forwarder to it;
- `papers.html`, the Papers section's page: one large card per paper, from the one list
  `overview_sections.PAPERS`. The optimality review (`papers/n11-optimality-review.html`,
  `render_n11_optimality_review`), the lower-bounds explainer
  (`papers/n11-lower-bounds-explainer.html`, `render_n11_lower_bounds_explainer`) and the
  tutorial are the section's papers, and the bar's Papers entry is current on all four;
- a forwarder at each address a page used to have (`MOVED_PAGES`), the papers' old
  addresses among them, so an old link still arrives, query and fragment kept
  (`forwarder_pages`);
- `tutorial.html`, the tutorial rendered as a page;
- a forwarder at each address a page used to have (`MOVED_PAGES`), so an old link still
  arrives, query and fragment kept (`forwarder_pages`);
- `visualize.html`, the Visualize section's first tab: the n = 1 to 324 film at full
  size. Its second tab is the workbench at `workbench/`, which
  `workbench_tools.build_site` builds and gives the same tab bar (`visualize_tabs`).

Every page is a kpress standalone page with its assets inlined, so it opens the same
way from a file, from GitHub Pages and from an artifact host. The explainer's paper
typography and accent are carried by `templates/site.css`, and one navigation partial,
`templates/site-nav.html`, joins the pages. No value on a page is typed into a template:
bounds, rungs, credits and counts are read from the record at render time.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.render_overview
    uv run --frozen --all-extras --group dev python -m devtools.render_overview --check
    uv run --frozen --all-extras --group dev python -m devtools.render_overview --output DIR
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from collections.abc import Callable, Sequence
from datetime import datetime
from functools import cache
from pathlib import Path
from typing import Literal, NamedTuple
from urllib.parse import quote

from devtools import repo_links
from devtools.repo_links import repo_url
from sqpack.release import PUBLICATION_EDITION, PUBLICATION_HISTORY

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
TEMPLATES = PACKING / "devtools" / "templates"
SITE_CSS = TEMPLATES / "site.css"
#: The result overview's styles, the popover body a result's row opens
#: (`devtools.result_overview`), kept apart from `site.css` and inlined after it.
SITE_RESULT_CSS = TEMPLATES / "site-result.css"
SITE_NAV = TEMPLATES / "site-nav.html"
SITE_NAV_CSS = TEMPLATES / "site-nav.css"
#: The text tokens every page shares with the explainer: its type base, reading measure,
#: heading scale and pinned faces. The explainer's shell inlines the same file.
PAPER_TYPE_CSS = TEMPLATES / "paper-type.css"
OVERVIEW_ARTICLE = TEMPLATES / "overview-article.md"
RESULTS_ARTICLE = TEMPLATES / "all-results-article.md"
VISUALIZE_ARTICLE = TEMPLATES / "visualize-article.md"
PAPERS_ARTICLE = TEMPLATES / "papers-article.md"
BROWSER = PACKING / "devtools" / "overview"
FORWARD_SCRIPT = BROWSER / "forward.js"
TABLE_SCRIPT = BROWSER / "table.js"
MATH_SCRIPT = BROWSER / "math.js"
POPOVER_SCRIPT = BROWSER / "popover.js"
ROW_POPOVER_SCRIPT = BROWSER / "row-popover.js"
ATLAS_VIEW_SCRIPT = BROWSER / "atlas-view.js"
ATLAS_GRID_SCRIPT = BROWSER / "atlas-grid.js"
EMBED_SCRIPT = BROWSER / "embed.js"
CASE_POPOVER_SCRIPT = BROWSER / "case-popover.js"
#: What starts the Visualize page's film when the page is visited.
FILM_SCRIPT = BROWSER / "film.js"
THEME_SCRIPT = BROWSER / "theme.js"
#: The frame the site's flattened kpress client modules are placed in.
KPRESS_CLIENT_FRAME = BROWSER / "kpress-client.js"
#: kpress's client modules a site page carries, in dependency order: the contents rail's
#: scroll-spy and drawer (`toc.js`) and hash-navigation history (`history.js`), with
#: the helpers they import.
KPRESS_CLIENT_MODULES = ("viewport.js", "overlay.js", "runtime.js", "toc.js", "history.js")
KPRESS_CLIENT_API = {"runtime.js": "behaviors", "toc.js": "initKpressToc"}
OUTPUT = PACKING / "site"

#: Where the deploy serves the site: the one statement of the published root. Every
#: canonical URL and every address in a link preview is built from it (`canonical_url`,
#: `head_tags`), and `render_n11_lower_bounds_explainer.SITE_URL` is this constant.
SITE_URL = "https://jlevy.github.io/squares/"
SITE_NAME = "Square Packing"
#: The project's formal name (the owner, 2026-10-01). The name in the bar stays the
#: shorter `SITE_NAME`; a page's title and its link preview carry the formal name
#: (`page_title`, `head_tags`; think-3w07).
PROJECT_NAME = "The Squares Project"
#: What stands between a page's own name and the project's in `<title>`.
TITLE_SEPARATOR = " \u00b7 "
#: The picture a shared link to any page of the site shows: the homepage's hero, the
#: best packing known of `overview_sections.HERO_CASE` squares, on the page's light
#: background with the project's name under it. `devtools.social_card` draws it when
#: the site is built, at this size, and it is served under this name at the site's
#: root; it is not checked in. 1200 by 630 is the large card every consumer shows
#: uncropped, 1.905 to 1.
SOCIAL_CARD = "social-card.png"
SOCIAL_CARD_WIDTH = 1200
SOCIAL_CARD_HEIGHT = 630
#: The locale Open Graph names the site's language by; every page is `lang="en"`.
SITE_LOCALE = "en_US"
#: The longest description a page may carry. A search result and a link preview both cut
#: a longer one mid-sentence, at about this length.
DESCRIPTION_LIMIT = 160
#: The two tools the closing line credits, at the addresses the repository already uses:
#: README links Flowmark there, and KPress is the `vendor/kpress` submodule's origin.
FLOWMARK_URL = "https://github.com/jlevy/flowmark"
KPRESS_URL = "https://github.com/jlevy/kpress"
#: Where a reader reports a result the site does not have yet: a new issue on the
#: repository, which the overview's own statement links.
NEW_ISSUE_URL = f"{repo_links.REPO_URL}/issues/new"
OVERVIEW_DESCRIPTION = (
    "Packing unit squares in the smallest square: the problem, every current result, "
    "and how each one is verified."
)
RESULTS_DESCRIPTION = (
    "Every reviewed result on packing unit squares in the smallest square, this project's "
    "and others': its claim, credit, date and ratings, with its records."
)
PAPERS_DESCRIPTION = (
    "The project's papers on packing unit squares in the smallest square: its "
    "explanations and proofs, written out in full."
)
VISUALIZE_DESCRIPTION = (
    "The best packings known of n unit squares, n = 1 to 324, built one square at a "
    "time in an eight-minute film, and a workbench to move the squares yourself."
)
#: The release the films are published on, and the two films on it.
FILM_RELEASE = "v0.4.2"
FILM_RELEASE_URL = f"https://github.com/jlevy/squares/releases/tag/{FILM_RELEASE}"
FILM_URL = (
    f"https://github.com/jlevy/squares/releases/download/{FILM_RELEASE}/"
    "ascent-n1-324-1080p60-citations.mp4"
)
SHORT_FILM_URL = FILM_URL.replace("n1-324", "n1-100")


def film_release_date() -> str:
    """The day `FILM_RELEASE` was first published, as the site writes a date without
    its year: 28 September. The films show the record as it stood that day."""
    entry = next(entry for entry in PUBLICATION_HISTORY if entry.version == FILM_RELEASE)
    day = datetime.strptime(entry.first_published, "%B %d, %Y").date()  # noqa: DTZ007
    return f"{day.day} {day:%B}"


#: The Visualize section's tabs, each its own page: its key, where it is served from the
#: site's root, and its label. The film is the section's first tab and the bar's target.
VISUALIZE_TABS: tuple[tuple[str, str, str], ...] = (
    ("film", "visualize.html", "Film"),
    ("workbench", "workbench/", "Workbench"),
)
FRONTIER_DESCRIPTION = (
    "Every tracked case of packing n unit squares in the smallest square, n = 1 to 324: "
    "the best known packing, the reported and verified bounds, and their records."
)

#: The results table's page; its row ids are the results' (`#t-018`). `results.html` was
#: `RESULTS.md` rendered as a reader document until 2026-10-01, and is now a forwarder
#: to this page (`MOVED_PAGES`).
RESULTS_PAGE = "all-results.html"

#: The repository documents served as pages outside the navigation, reached from the
#: overview's cards, in the cards' order; `site_documents` renders them. README and
#: `epistemics.md` lead, then the synopsis and the two reference documents.
DOCUMENT_PAGES: tuple[str, ...] = (
    "readme.html",
    "epistemics.html",
    "synopsis.html",
    "conventions.html",
    "development.html",
)
#: The directory the site's papers are served from, under its root.
PAPERS_DIR = "papers"
#: The papers' slugs, each naming its case, its subject and its kind of paper. A paper is
#: `papers/<slug>.html`, with its Markdown and its PDF beside it under the same slug
#: (`paper_path`), and its renderer, templates and tests carry the slug in their names:
#: `render_n11_optimality_review`, `render_n11_lower_bounds_explainer`. Both renderers
#: import this module, so the slugs are written once, here.
N11_OPTIMALITY_REVIEW = "n11-optimality-review"
N11_LOWER_BOUNDS_EXPLAINER = "n11-lower-bounds-explainer"
#: From a paper's page back up to the site's root, which is where the bar's links, the
#: other pages and the atlas's files are.
PAPERS_ROOT = "../"


def paper_path(slug: str, suffix: str = ".html") -> str:
    """Where a paper is served, by path under the site's root: its page, or with
    `suffix` its Markdown (`.md`) or its PDF (`.pdf`)."""
    return f"{PAPERS_DIR}/{slug}{suffix}"


#: Every page the published site serves, by path under the site root, whichever build
#: writes it. The navigation bar links only to these, and tests hold it to that.
SITE_PAGES: tuple[str, ...] = (
    "index.html",
    "frontier.html",
    RESULTS_PAGE,
    "cases/index.html",
    "papers.html",
    paper_path(N11_OPTIMALITY_REVIEW),
    paper_path(N11_LOWER_BOUNDS_EXPLAINER),
    "tutorial.html",
    "visualize.html",
    "workbench/index.html",
    *DOCUMENT_PAGES,
)

#: Every page that moved or was withdrawn, by the path it was served at and where a
#: visit to it is sent now: a path under the site's root, or the address of a file on
#: `main`. Three generated views of the record were served as reader documents until
#: 2026-10-01 (think-bk2e). The results register's page gave way to the results table
#: and the status table's to the frontier atlas, each built from the same record; the
#: defect log is internal to the repository, so its old address opens the file on
#: GitHub. The papers moved to `papers/<slug>.html` the same day (think-cmz6): the
#: explainer from `explainer.html`, where it had been since the overview took the root,
#: and the optimality paper from `n11-optimality/t-060-explainer.html`, with the landing
#: address its directory had. Each old path is still served, as a forwarder
#: (`forwarder_pages`), so a link written before the change arrives with its query and
#: its fragment. Nothing on the site links an old path; a test holds every page to that.
MOVED_PAGES: tuple[tuple[str, str], ...] = (
    ("results.html", RESULTS_PAGE),
    ("status.html", "frontier.html"),
    ("defects.html", repo_url(repo_links.DEFECTS, kind="blob")),
    ("explainer.html", paper_path(N11_LOWER_BOUNDS_EXPLAINER)),
    ("n11-optimality/t-060-explainer.html", paper_path(N11_OPTIMALITY_REVIEW)),
    ("n11-optimality/index.html", paper_path(N11_OPTIMALITY_REVIEW)),
    # Every record was one page, each at its fragment, until 2026-10-03 (think-bnw2): the
    # record page takes `#n-11` and shows that case's record file, `cases/11.html`.
    ("cases.html", "cases/index.html"),
)
#: What a forwarder calls the place it sends a reader, by that place's address. A paper
#: is called by its title, which its card has (`overview_sections.PAPERS`).
FORWARDER_TITLES: dict[str, str] = {
    RESULTS_PAGE: "Every Result",
    "frontier.html": "The Frontier Atlas",
    "cases/index.html": "Case Records",
    repo_url(repo_links.DEFECTS, kind="blob"): "defects.md on GitHub",
}
#: Every file that moved and is not a page, the same way: the papers' Markdown and PDF,
#: which a script cannot forward. Each old path is served as a copy of the new one, made
#: when the site is assembled, since the files come from other builds than this one: by
#: the Pages workflow's `publish` job, and by `preview_site.copy_moved_files` on one
#: machine. The first paper's had been linked since September, a dated review among the
#: links; the optimality paper's PDF was linked from the README.
MOVED_FILES: tuple[tuple[str, str], ...] = (
    ("t-018-explainer.md", paper_path(N11_LOWER_BOUNDS_EXPLAINER, ".md")),
    ("t-018-explainer.pdf", paper_path(N11_LOWER_BOUNDS_EXPLAINER, ".pdf")),
    ("n11-optimality/t-060-explainer.md", paper_path(N11_OPTIMALITY_REVIEW, ".md")),
    ("n11-optimality/t-060-explainer.pdf", paper_path(N11_OPTIMALITY_REVIEW, ".pdf")),
)
FORWARDER = TEMPLATES / "site-forwarder.html"

#: Every file a render reads beside the record `overview_data.INPUTS` names; `inputs()`
#: is the two together. The Pages workflow's deploy filter and the scope tool are checked
#: against that, so a page cannot go stale because an input moved unseen. The record is
#: read through `sqpack`'s loaders and the pages are kpress pages, so the package, the
#: vendored kpress and the locked environment are inputs, as they are the explainer's.
RENDER_INPUTS: tuple[Path, ...] = (
    Path(__file__).resolve(),
    SITE_CSS,
    SITE_RESULT_CSS,
    SITE_NAV,
    SITE_NAV_CSS,
    PAPER_TYPE_CSS,
    OVERVIEW_ARTICLE,
    RESULTS_ARTICLE,
    VISUALIZE_ARTICLE,
    PAPERS_ARTICLE,
    FORWARDER,
    BROWSER,
    PACKING / "src" / "sqpack",
    PACKING / "devtools" / "site_documents.py",
    PACKING / "devtools" / "result_overview.py",
    # The card every page's head names is drawn beside the pages, in the page's colours.
    PACKING / "devtools" / "social_card.py",
    PACKING / "devtools" / "rung_scale.py",
    REPO / repo_links.TUTORIAL,
    REPO / repo_links.README,
    REPO / repo_links.SYNOPSIS,
    REPO / repo_links.CONVENTIONS,
    REPO / repo_links.DEVELOPMENT,
    PACKING / "devtools" / "repo_links.py",
    REPO / "vendor" / "kpress",
    PACKING / "pyproject.toml",
    PACKING / "uv.lock",
)

# The same refusal the explainer makes: a script or stylesheet with a source, a CSS
# import, or a url() or `<link>` that is not a data URI or a fragment is a fetch.
_EXTERNAL_REFERENCE = re.compile(
    r"<script[^>]*\ssrc="
    r'|<link(?![^>]*\srel="canonical")(?![^>]*\shref="data:)[^>]*\shref='
    r"|@import\b"
    r"""|url\(\s*(?!["']?(?:data:|#))"""
)


def canonical_url(name: str) -> str:
    """A served page's canonical URL, from its path under the site's root: the address it
    is served at. A directory's `index.html` is served as the directory, so the overview
    is the root and the workbench is `workbench/`."""
    if name == "index.html" or name.endswith("/index.html"):
        return SITE_URL + name.removesuffix("index.html")
    return SITE_URL + name


#: What a page is to Open Graph: a page of the site, or a paper.
PageKind = Literal["website", "article"]
_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


class PageMeta(NamedTuple):
    """What a page says of itself in its `<head>`: to a tab, to a search engine and to
    whatever draws a preview of a shared link (`head_tags`)."""

    name: str
    """The page's own name, with no site name after it: `Every Result`. The overview's is
    the project's name."""
    description: str
    """One or two plain sentences on this page and no other, `DESCRIPTION_LIMIT`
    characters at most."""
    path: str
    """Where the page is served, under the site's root: `all-results.html`,
    `workbench/index.html`. Its canonical URL is read from this (`canonical_url`)."""
    kind: PageKind = "website"
    """`article` for a paper, `website` for every other page."""
    published: str = ""
    """For a paper that states them, the day it was first published and the day it was
    last revised, as ISO dates (`2026-09-05`)."""
    modified: str = ""


def page_title(name: str) -> str:
    """A page's `<title>`: its own name, then the project's. The overview's name is the
    project's, written once."""
    return name if name == PROJECT_NAME else f"{name}{TITLE_SEPARATOR}{PROJECT_NAME}"


def social_card_url() -> str:
    """The card image's address on the deployed site, which every page names in full."""
    return SITE_URL + SOCIAL_CARD


def social_card_alt() -> str:
    """What the card is a picture of, for a reader who cannot see it."""
    from devtools.overview_sections import HERO_CASE  # noqa: PLC0415

    return (
        f"The best packing known of {HERO_CASE} unit squares in a square: rows of upright "
        "squares around a diagonal band of tilted ones. Under it, the name "
        f"{PROJECT_NAME}."
    )


def head_tags(page: PageMeta) -> str:
    """A page's identity and its link preview, the one definition every page's head is
    written from: the site's own pages (`kpress_page`), the two papers and the workbench.

    One tag to a line: the title, the description, the canonical link, the Open Graph set
    and the Twitter set. The preview's title is the page's own name, since `og:site_name`
    already says whose page it is, and its description is the page's own. Every address
    is absolute, built from `SITE_URL`, because a crawler reads these off the markup with
    no base to resolve against: the canonical URL and `og:url` are one address, the one
    the page is served at, and the image is the site's one card (`SOCIAL_CARD`), with the
    size `devtools.social_card` draws it at so a consumer can reserve its box. None of
    them is a load: no browser fetches any of them to draw the page.

    The description is refused if it is empty, runs over `DESCRIPTION_LIMIT` or breaks
    across lines, and a paper's dates if they are not ISO dates, so a page that would
    carry a broken tag does not render. `check_published_site.head_problems` holds a
    rendered page to this set.
    """
    description = page.description.strip()
    if not description or "\n" in description or len(description) > DESCRIPTION_LIMIT:
        raise SystemExit(
            f"{page.path}: a description is one line of at most {DESCRIPTION_LIMIT} "
            f"characters, and this is {len(description)}: {description!r}"
        )
    if not page.name.strip():
        raise SystemExit(f"{page.path}: a page has a name")
    for moment in (page.published, page.modified):
        if moment and not _ISO_DATE.fullmatch(moment):
            raise SystemExit(f"{page.path}: {moment!r} is not an ISO date")
    if (page.published or page.modified) and page.kind != "article":
        raise SystemExit(f"{page.path}: only an article states when it was published")

    def attribute(value: str) -> str:
        return html.escape(value, quote=True)

    def meta(key: str, value: str) -> str:
        # Open Graph's tags are `property`; the description and Twitter's are `name`.
        named = "property" if key.startswith(("og:", "article:")) else "name"
        return f'<meta {named}="{key}" content="{attribute(value)}">'

    url = canonical_url(page.path)
    image = social_card_url()
    alt = social_card_alt()
    article = [
        meta(f"article:{key}_time", moment)
        for key, moment in (("published", page.published), ("modified", page.modified))
        if moment
    ]
    return "\n".join(
        (
            f"<title>{html.escape(page_title(page.name), quote=False)}</title>",
            meta("description", description),
            f'<link rel="canonical" href="{attribute(url)}">',
            meta("og:type", page.kind),
            meta("og:site_name", PROJECT_NAME),
            meta("og:locale", SITE_LOCALE),
            meta("og:title", page.name),
            meta("og:description", description),
            meta("og:url", url),
            meta("og:image", image),
            meta("og:image:type", "image/png"),
            meta("og:image:width", str(SOCIAL_CARD_WIDTH)),
            meta("og:image:height", str(SOCIAL_CARD_HEIGHT)),
            meta("og:image:alt", alt),
            *article,
            meta("twitter:card", "summary_large_image"),
            meta("twitter:title", page.name),
            meta("twitter:description", description),
            meta("twitter:image", image),
            meta("twitter:image:alt", alt),
        )
    )


def inputs() -> tuple[Path, ...]:
    """Every file any page this module renders reads: its own inputs and the record's.

    The page modules are imported here rather than at the top because
    `render_frontier_page` reads `render_n11_lower_bounds_explainer`, which imports this module.
    """
    from devtools import overview_data  # noqa: PLC0415
    from devtools.render_case_pages import CASES_INPUTS  # noqa: PLC0415
    from devtools.render_frontier_page import FRONTIER_INPUTS  # noqa: PLC0415

    return tuple(
        dict.fromkeys(
            (
                *RENDER_INPUTS,
                *overview_data.INPUTS,
                *FRONTIER_INPUTS,
                *CASES_INPUTS,
            )
        )
    )


class Page(NamedTuple):
    """One rendered page: where it is served and its bytes."""

    name: str
    html: str


def page_assets() -> tuple[str, str]:
    """The explainer's own inlined assets: head styles and the math pipeline.

    The stylesheets are the explainer's (`kpress_css`, `katex_css`, `relation_face_css`),
    faces already inlined as data URIs, so a reader moving between the explainer and
    these pages sees one design system; `paper-type.css`, the text tokens the explainer
    also carries, follows them. The script is the explainer's math pipeline,
    `render_n11_lower_bounds_explainer.katex_js`: KaTeX, kpress's metric tables and shared
    runtime, and the explainer's host adapter (`squaresMath`), without kpress's auto-render
    entry point and its whole-page synchronous pass. `overview/math.js`, which `kpress_page`
    places after it, drives the adapter over kpress's own math markup. The pipeline is described
    in `templates/paper-design.md`, under Math Loading.
    """
    from devtools.render_n11_lower_bounds_explainer import (  # noqa: PLC0415
        katex_css,
        katex_js,
        kpress_css,
        kpress_static,
        relation_face_css,
    )

    static = kpress_static()
    head = (
        f"<style>{kpress_css(static)}{katex_css(static)}</style>\n"
        f"<style>{relation_face_css(static)}</style>\n"
        f"<style>{PAPER_TYPE_CSS.read_text(encoding='utf-8')}</style>\n"
        f"<style>{SITE_NAV_CSS.read_text(encoding='utf-8')}</style>\n"
        f"<style>{SITE_CSS.read_text(encoding='utf-8')}</style>\n"
        f"<style>{SITE_RESULT_CSS.read_text(encoding='utf-8')}</style>"
    )
    return head, f"<script>{katex_js(static)}</script>"


def assert_self_contained(name: str, page: str) -> None:
    """Refuse a page that would fetch anything to be drawn: a script or stylesheet with
    a source, a CSS import, or a `url()` or `<link>` that is not a data URI or a
    fragment. What a reader opens afterwards is fetched then, from the site itself: a
    page a card's popover frames, and a result's overview (`result_fragments`)."""
    hit = _EXTERNAL_REFERENCE.search(page)
    if hit:
        excerpt = page[max(hit.start() - 60, 0) : hit.end() + 80]
        raise SystemExit(f"{name} is not self-contained: ...{excerpt}...")


def nav_html(current: str, *, root: str = "") -> str:
    """The navigation bar, with the current page marked."""
    nav = SITE_NAV.read_text(encoding="utf-8")
    nav = nav.replace("{{ROOT}}", root).replace("{{LOGO}}", site_logo())
    marker = f'data-page="{current}"'
    if marker not in nav:
        raise SystemExit(f"site-nav.html has no entry for {current!r}")
    return nav.replace(marker, f'{marker} aria-current="page"')


class NavShell(NamedTuple):
    """The navigation bar for a page kpress does not render, in the three places it goes.

    `head` opens the page's `<head>`: kpress's pre-paint theme bootstrap, kpress's design
    tokens with the one face the bar is set in, the text tokens every page shares
    (`paper-type.css`), and `site-nav.css`. `header` is the bar
    in the shell `site-nav.css` gives an application page, for the start of `<body>`,
    with the page's section tabs after the bar when it has them.
    `script` is the gear's program, `overview/theme.js`, for the end of `<body>`.
    """

    head: str
    header: str
    script: str


#: The face the bar is set in, the one `@font-face` of kpress's tokens an application page
#: needs: `--kpress-font-sans` leads with it.
_NAV_FACE = re.compile(r'font-family:\s*"Source Sans 3 Variable";\s*font-style:\s*normal;')


def nav_shell(current: str, *, root: str, tabs: str = "") -> NavShell:
    """The site's navigation bar, gear included, for an application page: the workbench.

    The same partial, stylesheet and theme program every kpress page carries, with the
    theme bootstrap kpress's standalone page runs before first paint, so the bar sits
    where it does on every page and one stored choice, `kpress.theme`, drives the theme
    on all of them. kpress's tokens come whole but for their faces, of which only the
    bar's own is kept and inlined; the page's own stylesheet, placed after them, keeps
    any of its own custom properties the tokens also name. `tabs`, a section's tab bar
    (`visualize_tabs`), follows the bar in the header, as on a kpress page.
    """
    from devtools.render_n11_lower_bounds_explainer import (  # noqa: PLC0415
        FONT_FACE_BLOCK,
        inline_font_urls,
        kpress_static,
        theme_bootstrap,
    )

    static = kpress_static()
    tokens = (static / "css" / "style-tokens.css").read_text(encoding="utf-8")
    tokens = FONT_FACE_BLOCK.sub(
        lambda match: match.group(0) if _NAV_FACE.search(match.group(0)) else "", tokens
    )
    if not _NAV_FACE.search(tokens):
        raise SystemExit("kpress's style-tokens.css no longer declares the bar's face")
    tokens = inline_font_urls(tokens, static / "css")
    head = (
        f"{favicon_html()}\n"
        f"<script>{theme_bootstrap(static)}</script>\n"
        f"<style>{tokens}</style>\n"
        f"<style>{PAPER_TYPE_CSS.read_text(encoding='utf-8')}</style>\n"
        f"<style>{SITE_NAV_CSS.read_text(encoding='utf-8')}</style>"
    )
    header = (
        '<div class="site-app-shell">\n<header class="kpress-site-header">\n'
        f"{nav_html(current, root=root)}{tabs}</header>\n</div>"
    )
    return NavShell(head, header, f"<script>{_script_text(THEME_SCRIPT)}</script>")


def visualize_tabs(current: str, *, root: str = "") -> str:
    """The Visualize section's tab bar, with the current tab marked.

    Each tab is a real link to its own page, so the bar needs no script and a tab can be
    opened, bookmarked and shared. Its look is `.site-tabs` in `site-nav.css`, the one
    stylesheet both the film's page and the workbench carry, which also draws the rule
    under the navigation bar over the tabs: they follow the bar in the header slot, and
    the bar, not the slot, carries the rule on a page that has them.
    """
    if current not in {key for key, _, _ in VISUALIZE_TABS}:
        raise SystemExit(f"the Visualize section has no tab {current!r}")
    links = "".join(
        f'<a data-tab="{key}"{' aria-current="page"' if key == current else ""} '
        f'href="{root}{href}">{html.escape(label)}</a>'
        for key, href, label in VISUALIZE_TABS
    )
    return f'<nav class="site-tabs" aria-label="Visualize">{links}</nav>'


#: The logo's size in the bar and the icon's in a tab, in CSS pixels: whole pixels, so
#: each drawing's one-pixel frame (`packing_svg(frame_px=)`) lands on the pixel grid.
#: `site-nav.css` sets the logo to the same size.
SITE_LOGO_PX = 18
FAVICON_PX = 16


@cache
def site_logo() -> str:
    """The site's mark beside its name in the bar: case 11, the drawing the tab's icon
    is, in the bar's own ink so it turns over with the theme."""
    from devtools.render_frontier_page import packing_svg  # noqa: PLC0415

    svg = packing_svg(11, units=200, frame_px=SITE_LOGO_PX)
    return svg.replace("<svg ", '<svg class="site-logo" ', 1)


@cache
def favicon_html() -> str:
    """The site's icon: case 11, Trump's packing of eleven squares, drawn small as a
    data URI, so it costs no fetch. It names its ink and paper, since a tab has no page
    colour to inherit."""
    from devtools.render_frontier_page import packing_svg  # noqa: PLC0415

    svg = packing_svg(11, units=200, ink="#17202a", paper="#ffffff", frame_px=FAVICON_PX)
    svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    return f'<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,{quote(svg)}">'


def colophon_lines(*, edition: str = PUBLICATION_EDITION) -> str:
    """The closing credit's two lines, the one definition every page's footer is made of:
    the site's pages (`colophon_html`), the explainer and the optimality paper, whose
    shells set it in their own closing paragraph.

    The first line is the project's formal name and its repository, shown without its
    scheme and linked. The second is `edition`, then the credit to the two tools. On the
    site's pages the edition is `sqpack.release.PUBLICATION_EDITION` taken whole, the
    stamp the atlas footer and the film carry (`v0.4.2-8ac5de`, with the edition's
    status ahead of it while it has one), so it follows a re-pin and a new edition with
    no edit here; a build that prints it names `release.py` among its inputs. A paper
    passes none: its own version is in its credits, and the site's version and the data
    hash go nowhere on a paper (the owner, 2026-10-01), so its second line is the credit
    to the tools alone.

    A line is a block, so there are two at every width, and each part beside a middle
    dot is an inline block, so a line too long for a phone breaks at its dot before it
    breaks inside a part (`site-nav.css`, which every page carries).
    """

    def part(markup: str) -> str:
        return f'<span class="site-colophon-part">{markup}</span>'

    def line(*parts: str) -> str:
        shown = [part(markup) for markup in parts if markup]
        return f'<span class="site-colophon-line">{" · ".join(shown)}</span>'

    repository = repo_links.REPO_URL
    return line(
        html.escape(PROJECT_NAME),
        f'<a href="{repository}">{html.escape(repository.removeprefix("https://"))}</a>',
    ) + line(
        html.escape(edition),
        f'Formatted and typeset with <a href="{FLOWMARK_URL}">Flowmark</a> '
        f'and <a href="{KPRESS_URL}">KPress</a>',
    )


def colophon_html() -> str:
    """The closing credit every site page carries, in KPress's footer slot: the two lines
    every page shares (`colophon_lines`), as the explainer's are."""
    return f'<p class="site-colophon">{colophon_lines()}</p>'


def kpress_page(
    markdown: str,
    *,
    name: str,
    current: str,
    title: str,
    description: str,
    toc: bool | Literal["auto"],
    rewrite_body: Callable[[str], str] | None = None,
    page_scripts: Sequence[Path] = (),
    trust_mode: Literal["trusted", "sanitized"] = "trusted",
    strict_anchors: bool = False,
    tabs: str = "",
    kind: PageKind = "website",
) -> Page:
    """One standalone kpress page with the site's layer, nav and colophon.

    `title` is the page's own name, with no site name after it, and `description` its
    own sentence: its `<title>`, description, canonical link and link preview are the
    site's one set (`head_tags`), in place of the tags kpress's shell writes. `kind` is
    `article` for a paper.

    `tabs`, a section's tab bar (`visualize_tabs`), follows the navigation bar in the
    header slot, where the workbench's shell also puts it, so it sits in one place on
    every page of its section.

    `page_scripts` are page programs in checked `.js` files, each placed in its own
    script element after the math scripts and the navigation bar's theme control
    (`overview/theme.js`); no script text is written here.
    `strict_anchors` raises kpress's `broken_anchor` warning, an in-page `#…` link
    with no target, to a failure; the reader documents are rendered that way.
    """
    from kpress.format.model import DocumentInput, RenderOptions  # noqa: PLC0415
    from kpress.format.render import render_page  # noqa: PLC0415

    document = DocumentInput(
        title=page_title(title),
        source_text=markdown,
        source_path=name,
        body_markdown=markdown,
        trust_mode=trust_mode,
    )
    head, math_scripts = page_assets()
    options = RenderOptions(
        asset_mode="inline",
        asset_policy="none",
        content_card=False,
        show_doc_header=False,
        include_toc="auto" if toc == "auto" else "on" if toc else "off",
        head_extra_html=(
            f"{favicon_html()}{head}<script>{_script_text(EMBED_SCRIPT)}</script>"
        ),
        header_html=nav_html(current) + tabs,
        footer_html=colophon_html(),
    )
    rendered = render_page(document, options)
    errors = [
        d
        for d in rendered.diagnostics
        if d.get("severity") == "error" or (strict_anchors and d.get("type") == "broken_anchor")
    ]
    if errors:
        raise SystemExit(f"{name}: kpress reported errors: {errors[:3]}")
    page = _site_head(name, rendered.html, PageMeta(title, description, name, kind))
    prose = 'class="kpress-prose kpress-long-text'
    page = page.replace(prose + '"', prose + ' site-page"', 1)
    page = _document_scrolls(name, page)
    page = _KPRESS_CELL_LABELS.sub("", page)
    if rewrite_body is not None:
        page = rewrite_body(page)
    programs = f"\n{kpress_client_script()}" + "".join(
        f"\n<script>{_script_text(path)}</script>"
        for path in (THEME_SCRIPT, MATH_SCRIPT, *page_scripts)
    )
    page = page.replace("</body>", f"{math_scripts}{programs}\n</body>", 1)
    assert_self_contained(name, page)
    return Page(name, page)


#: The column label and position kpress writes on every table cell, `data-col` and
#: `data-col-index`, hooks for a downstream decorator (`kpress.contract`) that nothing on
#: the site reads: about 128 KB of the frontier page, whose size has a ceiling, and a
#: little of every page with a table. Every page drops them (`think-k8xp`).
_KPRESS_CELL_LABELS = re.compile(r' data-col="[^"]*" data-col-index="\d+"')


#: What kpress's standalone shell writes of a page's identity: its own link-preview tags,
#: then the title. The site writes the whole set itself (`head_tags`), so this goes.
_KPRESS_IDENTITY = re.compile(
    r'(?:<(?:meta (?:property="og:|name="twitter:)|link rel="canonical")[^>]*>\s*)*'
    r"<title>[^<]*</title>"
)


def _site_head(name: str, page: str, meta: PageMeta) -> str:
    """Put the site's identity tags (`head_tags`) where kpress's shell wrote its own.

    kpress writes four link-preview tags on every page whatever it is told, with
    `og:type` always `website` and the preview's title the tab's, so they are taken out
    with the title they precede rather than added to: a head with two `og:title` is read
    differently by each consumer. A shell that stops writing them there fails here.
    """
    found = _KPRESS_IDENTITY.search(page)
    body = page.find("<body")
    if found is None or body < 0 or found.start() > body:
        raise SystemExit(f"{name}: kpress's shell no longer writes a title in its head")
    page = page[: found.start()] + head_tags(meta) + page[found.end() :]
    head = page[: page.find("<body")]
    stray = [
        tag
        for tag in ("<title>", 'property="og:title"', 'name="twitter:card"', 'rel="canonical"')
        if head.count(tag) != 1
    ]
    if stray:
        raise SystemExit(f"{name}: the head does not carry exactly one of {stray}")
    return page


#: kpress's standalone shell marks `<main>` as the pane the document scrolls in.
_MAIN_VIEWPORT = '<main class="kpress-page-main kpress-viewport" data-kpress-viewport>'


def _document_scrolls(name: str, page: str) -> str:
    """Name the document as kpress's viewport, as the explainer's shell does.

    `site.css` lets a site page scroll the document rather than `<main>`, so the
    navigation bar can stick, and kpress has to be told: its scroll-spy observes and
    listens on the element marked `data-kpress-viewport`, and with `<main>` still marked
    it watched a pane that never scrolls and the contents rail never followed the
    reader. Its popovers place themselves against the same element.
    """
    if page.count(_MAIN_VIEWPORT) != 1 or page.count("<html ") != 1:
        raise SystemExit(f"{name}: kpress's shell no longer marks <main> as its viewport")
    page = page.replace(
        _MAIN_VIEWPORT, _MAIN_VIEWPORT.removesuffix(" data-kpress-viewport>") + ">"
    )
    return page.replace("<html ", "<html data-kpress-viewport ", 1)


def kpress_client_script() -> str:
    """kpress's contents-rail and history modules as one classic script element.

    Flattened by the explainer's checked flattener, since an inline module would fetch
    its siblings at view time; see `render_n11_lower_bounds_explainer.kpress_client_js`.
    """
    from devtools.render_n11_lower_bounds_explainer import (  # noqa: PLC0415
        kpress_client_js,
        kpress_static,
    )

    script = kpress_client_js(
        kpress_static(),
        modules=KPRESS_CLIENT_MODULES,
        api=KPRESS_CLIENT_API,
        frame=KPRESS_CLIENT_FRAME,
    )
    return f"<script>{script}</script>"


def _script_text(path: Path) -> str:
    """A page program's text, refused if it would close its own script element early."""
    script = path.read_text(encoding="utf-8")
    if "</script" in script.lower():
        raise SystemExit(f"{path.name} contains a closing script tag")
    return script


def fill(template: str, values: dict[str, str], *, where: str) -> str:
    """Substitute every `{{NAME}}`; a placeholder left over or a value unused fails."""
    unused = [key for key in values if "{{" + key + "}}" not in template]
    if unused:
        raise SystemExit(f"{where}: values with no placeholder: {', '.join(unused)}")
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    left = re.findall(r"\{\{[A-Z_]+\}\}", template)
    if left:
        raise SystemExit(f"{where}: unfilled placeholders: {', '.join(sorted(set(left)))}")
    return template


def overview_page() -> Page:
    """The front door: prose from its template, every fact from the record.

    Its first section, The Square Packing Problem, opens with README's two opening
    paragraphs, read from README's `project-intro` block with their links rewritten for
    the site (`site_documents`). Recent Results is one paragraph of the template's own
    before its table; README keeps its fuller account of the same progress.
    """
    from devtools import overview_data, overview_sections, site_documents  # noqa: PLC0415

    overview = overview_data.load()
    values = {
        "HERO": overview_sections.hero(),
        "README_INTRO": site_documents.overview_intro(),
        "NEW_ISSUE_URL": NEW_ISSUE_URL,
        "DOCUMENT_CARDS": overview_sections.document_cards(),
        "OTHER_PROJECTS": overview_sections.other_project_cards(overview),
        "ATLAS_GRID": overview_sections.atlas_grid(),
        "ATLAS_CARDS": overview_sections.atlas_cards(),
        "PAGE_CARDS": overview_sections.page_cards(),
        "RECENT": overview_sections.recent_table(overview),
        "ARROW_RIGHT": overview_sections.arrow_icon("right"),
    }
    markdown = fill(
        OVERVIEW_ARTICLE.read_text(encoding="utf-8"), values, where=OVERVIEW_ARTICLE.name
    )
    # The prose names a repository file as `repo:PATH`, which becomes its link on `main`
    # through the one helper every page links the repository with (`repo_links`).
    markdown = re.sub(
        r'(\]\(|href=")repo:([^)"\s#]+)',
        lambda match: match[1] + repo_url(match[2]),
        markdown,
    )
    return kpress_page(
        markdown,
        name="index.html",
        current="overview",
        title=PROJECT_NAME,
        description=OVERVIEW_DESCRIPTION,
        toc=False,
        rewrite_body=lambda text: _case_links(site_documents.rewrite_overview_blocks(text)),
        page_scripts=(
            FORWARD_SCRIPT,
            TABLE_SCRIPT,
            POPOVER_SCRIPT,
            ROW_POPOVER_SCRIPT,
            ATLAS_VIEW_SCRIPT,
            ATLAS_GRID_SCRIPT,
            CASE_POPOVER_SCRIPT,
        ),
    )


def results_page() -> Page:
    """Every registered result, one row each at its own id, sortable and filterable."""
    from devtools import overview_data, overview_sections  # noqa: PLC0415

    overview = overview_data.load()
    values = {
        "EPISTEMICS_URL": repo_url(repo_links.EPISTEMICS),
        "RESULTS_TABLE": overview_sections.results_table(overview),
        "STAR_LEGEND": overview_sections.star_legend(),
        "STATUS_COUNTS": overview_sections.status_counts(overview),
        # The rating ladders, the homepage's Verification Ladders until 2026-10-02.
        "VERIFICATION": overview_sections.verification_block(),
    }
    markdown = fill(
        RESULTS_ARTICLE.read_text(encoding="utf-8"), values, where=RESULTS_ARTICLE.name
    )
    return kpress_page(
        markdown,
        name=RESULTS_PAGE,
        current="results",
        title="Every Result",
        description=RESULTS_DESCRIPTION,
        toc=False,
        page_scripts=(TABLE_SCRIPT, POPOVER_SCRIPT, ROW_POPOVER_SCRIPT),
    )


def papers_page() -> Page:
    """The Papers section's page: a short introduction and one large card per paper,
    each the link to its paper, which is a full page of the site. It has no popover,
    so it carries no popover script. The introduction's link to the optimality paper is
    the card's own address, filled from the one constant."""
    from devtools import overview_sections  # noqa: PLC0415

    values = {
        "PAPER_CARDS": overview_sections.paper_cards(),
        "OPTIMALITY_PAPER": overview_sections.OPTIMALITY_PAPER,
    }
    markdown = fill(
        PAPERS_ARTICLE.read_text(encoding="utf-8"), values, where=PAPERS_ARTICLE.name
    )
    return kpress_page(
        markdown,
        name="papers.html",
        current="papers",
        title="Papers",
        description=PAPERS_DESCRIPTION,
        toc=False,
    )


def tutorial_page() -> Page:
    """`TUTORIAL.md` as a page; `site_documents` rewrites and checks its links."""
    from devtools.site_documents import tutorial_page as build  # noqa: PLC0415

    return build()


def frontier_page() -> Page:
    """The frontier atlas: one row per case, from its `SquarePackingCase/v2` record."""
    from devtools.render_frontier_page import frontier_markdown  # noqa: PLC0415

    return kpress_page(
        frontier_markdown(fill),
        name="frontier.html",
        current="frontier",
        title="The Frontier Survey",
        description=FRONTIER_DESCRIPTION,
        toc=False,
        rewrite_body=_case_links,
        page_scripts=(TABLE_SCRIPT, POPOVER_SCRIPT, CASE_POPOVER_SCRIPT),
    )


def _case_links(page: str) -> str:
    """A page's links to case records, its prose's among them, marked for its case
    popover (`render_case_pages.mark_case_links`)."""
    from devtools.render_case_pages import mark_case_links  # noqa: PLC0415

    return mark_case_links(page)


def cases_page() -> Page:
    """The record page, `cases/`: the index of every case and the reader that shows one
    case's record file (`render_case_pages.cases_page`)."""
    from devtools.render_case_pages import cases_page as build  # noqa: PLC0415

    return build()


def case_records() -> list[Page]:
    """Each case's record file, `cases/11.html`, beside the record page: the record
    alone, which the record page and every case popover fetch
    (`render_case_pages.case_records`). Like a result's overview, a record file is not
    among `PAGES`."""
    from devtools.render_case_pages import case_records as build  # noqa: PLC0415

    return build()


def visualize_page() -> Page:
    """The Visualize section's first tab: the film of the ascent at full size.

    The film starts when the page is visited: its markup mutes it and marks it
    `data-autoplay`, and `overview/film.js` starts it unless the reader asks for reduced
    motion or the page is framed in a popover. No other page carries that script, so no
    other film on the site starts unasked."""
    values = {
        "FILM_URL": FILM_URL,
        "SHORT_FILM_URL": SHORT_FILM_URL,
        "RELEASE_URL": FILM_RELEASE_URL,
        "RELEASE": FILM_RELEASE,
        "RELEASE_DATE": film_release_date(),
    }
    markdown = fill(
        VISUALIZE_ARTICLE.read_text(encoding="utf-8"), values, where=VISUALIZE_ARTICLE.name
    )
    return kpress_page(
        markdown,
        name="visualize.html",
        current="visualize",
        title="Visualize",
        description=VISUALIZE_DESCRIPTION,
        toc=False,
        page_scripts=(FILM_SCRIPT,),
        tabs=visualize_tabs("film"),
    )


def _document_page(name: str) -> Callable[[], Page]:
    def build() -> Page:
        from devtools.site_documents import document_page  # noqa: PLC0415

        return document_page(name)

    return build


#: The pages this renderer owns, by served name.
PAGES: dict[str, Callable[[], Page]] = {
    "index.html": overview_page,
    "frontier.html": frontier_page,
    RESULTS_PAGE: results_page,
    "cases/index.html": cases_page,
    "papers.html": papers_page,
    "tutorial.html": tutorial_page,
    "visualize.html": visualize_page,
    **{name: _document_page(name) for name in DOCUMENT_PAGES},
}


def render_all() -> list[Page]:
    """Every page, in a fixed order."""
    return [build() for build in PAGES.values()]


def result_fragments() -> list[Page]:
    """Each registered result's overview, in the register's order, as the file its row's
    popover fetches (`overview_sections.result_fragment`).

    A fragment is not a page: it is one `.site-result` block and nothing else, with no
    shell, styles or scripts of its own, placed by `overview/row-popover.js` into the
    popover of a page that has them. The overviews are 2.8 MB between them and two pages
    list every result, so they are written once, here, rather than into either page.
    """
    from devtools import overview_data, overview_sections  # noqa: PLC0415

    overview = overview_data.load()
    return [
        Page(
            overview_sections.result_fragment(result.id),
            overview_sections.result_row_popover_body(result, overview) + "\n",
        )
        for result in overview.results
    ]


def forwarder_pages() -> list[Page]:
    """A forwarder at each address a page used to have (`MOVED_PAGES`), so no link written
    before the change breaks.

    A forwarder is a few lines and no page of the site: `overview/forward.js`, the script
    the overview already forwards its own old fragments with, reads where the reader is
    sent from the root element and sends them there with the query string and the
    fragment they came with. For a reader without scripts it carries a refresh and a
    link, and for a crawler the canonical address of the place it stands for. It has no
    bar, no stamp and no styles, and is not among `PAGES`. A target is written as the
    old path's reader must follow it: relative for a page of the site, climbing out of
    the old path's directory where it has one, and whole for an address off it.
    """
    import posixpath  # noqa: PLC0415

    from devtools.overview_sections import PAPERS  # noqa: PLC0415

    titles = FORWARDER_TITLES | {paper.href: paper.title for paper in PAPERS}
    template = FORWARDER.read_text(encoding="utf-8")
    pages = []
    for old, new in MOVED_PAGES:
        external = new.startswith("https://")
        target = new if external else posixpath.relpath(new, posixpath.dirname(old))
        values = {
            "TARGET": html.escape(target, quote=True),
            "TITLE": html.escape(titles[new]),
            "CANONICAL_URL": html.escape(new if external else canonical_url(new), quote=True),
            "FORWARD_SCRIPT": _script_text(FORWARD_SCRIPT),
        }
        page = fill(template, values, where=FORWARDER.name)
        assert_self_contained(old, page)
        pages.append(Page(old, page))
    return pages


def render_site() -> list[Page]:
    """Every file this module writes: the pages, the result fragments, the case record
    files, and a forwarder at each address a page used to have."""
    return [*render_all(), *result_fragments(), *case_records(), *forwarder_pages()]


def write_site(output: Path, files: Sequence[Page]) -> None:
    """Write `files` under `output`, and drop any result fragment or case record file
    already there that is not among them, so a directory built before a result was
    withdrawn, or a case dropped, does not keep serving it."""
    from devtools.overview_sections import RESULT_FRAGMENTS  # noqa: PLC0415
    from devtools.render_case_pages import CASES_DIR  # noqa: PLC0415

    output.mkdir(parents=True, exist_ok=True)
    kept = {output / file.name for file in files}
    for directory in (RESULT_FRAGMENTS, CASES_DIR):
        for stale in sorted((output / directory).glob("*.html")):
            if stale not in kept:
                stale.unlink()
    for file in files:
        target = output / file.name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(file.html, encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero if a file on disk differs from a fresh render",
    )
    args = parser.parse_args(argv)
    output = args.output.resolve()
    pages = render_all()
    fragments = result_fragments()
    records = case_records()
    forwarders = forwarder_pages()
    if args.check:
        stale = [
            p.name
            for p in (*pages, *fragments, *records, *forwarders)
            if not (output / p.name).is_file()
            or (output / p.name).read_text(encoding="utf-8") != p.html
        ]
        # A file left in a directory this module writes whole, a result withdrawn or a
        # case dropped since, is stale too: `write_site` would remove it.
        from devtools.overview_sections import RESULT_FRAGMENTS  # noqa: PLC0415
        from devtools.render_case_pages import CASES_DIR  # noqa: PLC0415

        written = {p.name for p in (*pages, *fragments, *records)}
        stale += [
            path.relative_to(output).as_posix()
            for directory in (RESULT_FRAGMENTS, CASES_DIR)
            for path in sorted((output / directory).glob("*.html"))
            if path.relative_to(output).as_posix() not in written
        ]
        if stale:
            print(f"stale or missing: {', '.join(stale)}", file=sys.stderr)
            return 1
        print(
            f"{len(pages)} pages, {len(fragments)} result overviews, {len(records)} case "
            f"records and {len(forwarders)} forwarders match a fresh render"
        )
        return 0
    write_site(output, [*pages, *fragments, *records, *forwarders])
    for page in pages:
        print(f"wrote {output / page.name} ({len(page.html) // 1024} KB)")
    for forwarder in forwarders:
        print(f"wrote {output / forwarder.name}, a forwarder")
    total = sum(len(fragment.html.encode("utf-8")) for fragment in fragments)
    places = sorted({(output / fragment.name).parent for fragment in fragments})
    print(
        f"wrote {len(fragments)} result overviews under "
        f"{', '.join(f'{place}/' for place in places)} ({total // 1024} KB in all)"
    )
    kept = sum(len(record.html.encode("utf-8")) for record in records)
    print(
        f"wrote {len(records)} case records under {output / 'cases'}/ "
        f"({kept // 1024} KB in all)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
