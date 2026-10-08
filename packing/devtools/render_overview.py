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
  `overview_sections.PAPERS`. The three parts of the n = 11 series, in reading order
  (`PAPERS`): the lower-bounds explainer (`papers/n11-lower-bounds-explainer.html`,
  `render_n11_lower_bounds_explainer`), the threshold-bound review
  (`papers/n11-threshold-bound-review.html`, `render_n11_threshold_bound_review`) and the
  optimality review (`papers/n11-optimality-review.html`, `render_n11_optimality_review`),
  then the tutorial, are the section's papers, and the bar's Papers entry is current on
  all five;
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
import json
import re
import sys
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime
from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, NamedTuple
from urllib.parse import quote

from devtools import repo_links
from devtools.repo_links import repo_url
from sqpack.release import PUBLICATION_EDITION, PUBLICATION_HISTORY

if TYPE_CHECKING:
    from kpress.format.assets import AssetRef

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
#: The atlas's two views and three sizes of tile, and the move between layouts. The
#: drawing tabs' own script, `atlas-layer.js`, went with them on 2026-10-04 (think-k8x9).
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
    "The project's papers on packing unit squares in the smallest square: a series of "
    "three on n = 11, read in order, with proofs written out in full."
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
#: `render_n11_lower_bounds_explainer`, `render_n11_threshold_bound_review`,
#: `render_n11_optimality_review`. Every renderer imports this module, so the slugs are
#: written once, here.
N11_LOWER_BOUNDS_EXPLAINER = "n11-lower-bounds-explainer"
N11_THRESHOLD_BOUND_REVIEW = "n11-threshold-bound-review"
N11_OPTIMALITY_REVIEW = "n11-optimality-review"
#: From a paper's page back up to the site's root, which is where the bar's links, the
#: other pages and the atlas's files are.
PAPERS_ROOT = "../"


class PaperRecord(NamedTuple):
    """One of the site's papers, as every tool that has to know the papers reads it: its
    slug, the renderer module that writes it, the label its cards carry, its part in the
    series, and its title as its page sets it, in title case and plain text."""

    slug: str
    module: str
    label: str
    part: int
    title: str


#: The site's papers, in reading order: the one list a new paper is entered in. They are
#: one series on n = 11, read I, II, III (the plan of 2026-10-05,
#: `docs/project/specs/active/plan-2026-10-05-n11-explainer-series.md`): the project's
#: own lower bounds, the review of Kleddamag's s(11) > 31/8, and the review of the
#: optimality proof. `SITE_PAGES`, the cards (`overview_sections.PAPERS`), each paper's
#: series strip (`paper_front.series`), the structure audit (`paper_structure`), the
#: Pages scope (`pages_scope`), the preview build (`preview_site`) and the deployed-site
#: check (`check_published_site`) read it, so a new paper is one entry here and its
#: renderer. Each title is its renderer's `TITLE`, which `tests/test_overview.py` holds
#: it to; the renderers import this module, so the title is written here rather than read
#: from them.
PAPERS: tuple[PaperRecord, ...] = (
    PaperRecord(
        slug=N11_LOWER_BOUNDS_EXPLAINER,
        module="devtools.render_n11_lower_bounds_explainer",
        label="Part I",
        part=1,
        title="New Lower Bounds for Square Packing for n = 11",
    ),
    PaperRecord(
        slug=N11_THRESHOLD_BOUND_REVIEW,
        module="devtools.render_n11_threshold_bound_review",
        label="Part II",
        part=2,
        title="A Review of the Certified Lower Bound s(11) > 31/8 for 11 Squares",
    ),
    PaperRecord(
        slug=N11_OPTIMALITY_REVIEW,
        module="devtools.render_n11_optimality_review",
        label="Part III",
        part=3,
        title="A Review of the Optimality Proof of the Trump Packing of 11 Squares",
    ),
)


def paper_record(slug: str) -> PaperRecord:
    """The site's paper `slug`; a slug that names no paper of the site is refused."""
    for paper in PAPERS:
        if paper.slug == slug:
            return paper
    raise ValueError(f"no paper of the site has the slug {slug!r}")


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
    *(paper_path(paper.slug) for paper in PAPERS),
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
#: What a forwarder that leads off the site calls the place it sends a reader, by that
#: place's address. A forwarder to a page of the site calls the page by the page's own
#: name, from the record the page writes its head from (`forwarded_metas`).
OFF_SITE_TITLES: dict[str, str] = {
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
    # The atlas's regularized layer: which cases have a view, and their drawings
    # (`overview_sections.atlas_regularized`, `render_frontier_page.packing_svg`).
    PACKING / "atlas" / "known-best" / "regularized" / "index.json",
    PACKING / "atlas" / "known-best" / "regularized" / "rendering",
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

#: The one place a site page fetches what it is drawn with: the site's shared assets
#: (`site_assets`), named by a relative path from wherever the page is served.
_ASSET_PATH = r"(?:\.\./)*assets/"
# A fetch a page may not make: a script with a source outside the shared assets, a
# `<link>` that is not the canonical link, a data URI, or a stylesheet or face preload
# from the shared assets, a CSS import, or a `url()` in the page's own text that is not a
# data URI or a fragment. A shared stylesheet's own `url()`s name the faces beside it.
_EXTERNAL_REFERENCE = re.compile(
    rf'<script(?![^>]*\ssrc="{_ASSET_PATH}js/)[^>]*\ssrc='
    r'|<link(?![^>]*\srel="canonical")(?![^>]*\shref="data:)'
    rf'(?![^>]*\srel="(?:stylesheet|preload)"[^>]*\shref="{_ASSET_PATH})[^>]*\shref='
    r"|@import\b"
    r"""|url\(\s*(?!["']?(?:data:|#))"""
)
#: A page a build writes is named here as if it stood at the site's root, as
#: `kpress_page` writes every address; a page under a directory is rebased after.
_FROM_ROOT = "index.html"


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
    structured_data: tuple[Mapping[str, Any], ...] = ()
    extra_meta: tuple[tuple[str, str], ...] = ()


#: The records the results page and the frontier atlas write their heads from, named
#: here because a forwarder to either previews it (`forwarded_metas`).
RESULTS_META = PageMeta("Every Result", RESULTS_DESCRIPTION, RESULTS_PAGE)
FRONTIER_META = PageMeta("The Frontier Survey", FRONTIER_DESCRIPTION, "frontier.html")


def breadcrumb_data(*items: tuple[str, str]) -> dict[str, Any]:
    """Structured breadcrumbs, with each address resolved from the site's root."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": position,
                "name": label,
                "item": canonical_url(path),
            }
            for position, (label, path) in enumerate(items, start=1)
        ],
    }


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
    title = page.name if page.kind == "article" else page_title(page.name)
    return "\n".join(
        (
            f"<title>{html.escape(title, quote=False)}</title>",
            meta("description", description),
            meta("robots", "max-image-preview:large"),
            *(
                (meta("google-site-verification", SEARCH_CONSOLE_VERIFICATION),)
                if SEARCH_CONSOLE_VERIFICATION
                else ()
            ),
            *(meta(key, value) for key, value in page.extra_meta),
            *(
                '<script type="application/ld+json">'
                + json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace(
                    "<", "\\u003c"
                )
                + "</script>"
                for data in page.structured_data
            ),
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
    The forwarders preview the papers from the papers' own records (`forwarded_metas`), so
    the files the explainer's sentence is read from are inputs too: its walkthrough's
    certificates, which name the case, and T-026's record with what it is checked against.
    """
    from devtools import overview_data  # noqa: PLC0415
    from devtools import render_n11_lower_bounds_explainer as explainer  # noqa: PLC0415
    from devtools.render_case_pages import CASES_INPUTS  # noqa: PLC0415
    from devtools.render_frontier_page import FRONTIER_INPUTS  # noqa: PLC0415

    return tuple(
        dict.fromkeys(
            (
                *RENDER_INPUTS,
                BROWSER / "favicon-48.png",
                BROWSER / "apple-touch-icon.png",
                *overview_data.INPUTS,
                *FRONTIER_INPUTS,
                *CASES_INPUTS,
                *explainer.WALKTHROUGH,
                explainer.THRESHOLD_CERTIFICATE,
                explainer.THRESHOLD_FINE_CERTIFICATE,
                explainer.CURRENT_BOUND_RECORD,
                explainer.THRESHOLD_PROOF,
            )
        )
    )


class Page(NamedTuple):
    """One rendered page: where it is served and its bytes."""

    name: str
    html: str


def page_assets() -> tuple[str, str]:
    """The shared assets every site page links, from the site's root: its head's face
    preloads and stylesheets, and the math pipeline's script.

    The stylesheets are the explainer's (`kpress_css`, `katex_css`, `relation_face_css`),
    with the same faces, so a reader moving between the explainer and these pages sees
    one design system; `paper-type.css`, the text tokens the explainer also carries,
    follows them, then the site's own. The script is the explainer's math pipeline,
    `render_n11_lower_bounds_explainer.katex_js`: KaTeX, kpress's metric tables and shared
    runtime, and the explainer's host adapter (`squaresMath`), without kpress's auto-render
    entry point and its whole-page synchronous pass. `overview/math.js`, which `kpress_page`
    places after it, drives the adapter over kpress's own math markup. The pipeline is described
    in `templates/paper-design.md`, under Math Loading. Each is a file of the site's
    `assets/` (`site_assets.shared`), fetched by a reader once for every page.
    """
    from devtools import site_assets  # noqa: PLC0415

    bundle = site_assets.shared()
    own = (PAPER_TYPE_CSS, SITE_NAV_CSS, SITE_CSS, SITE_RESULT_CSS)
    head = "\n".join(
        [
            bundle.head(_FROM_ROOT),
            *(
                site_assets.stylesheet_tag(bundle.assets.stylesheet_file(path), _FROM_ROOT)
                for path in own
            ),
        ]
    )
    return head, site_assets.script_tag(bundle.katex_js, _FROM_ROOT)


def assert_fetches_only_assets(name: str, page: str) -> None:
    """Refuse a page that would fetch anything to be drawn but the site's shared assets
    (`site_assets`): a script or stylesheet with another source, a CSS import, or a
    `url()` or `<link>` that is not a data URI or a fragment. What a reader opens
    afterwards is fetched then, from the site itself: a page a card's popover frames,
    and a result's overview (`result_fragments`)."""
    checked = re.sub(
        r'<link rel="(?:icon|apple-touch-icon)"[^>]*href="(?:\.\./)*'
        r'(?:favicon\.svg|favicon-48\.png|apple-touch-icon\.png)"[^>]*>',
        "",
        page,
    )
    hit = _EXTERNAL_REFERENCE.search(checked)
    if hit:
        excerpt = page[max(hit.start() - 60, 0) : hit.end() + 80]
        raise SystemExit(f"{name} fetches more than the site's assets: ...{excerpt}...")


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
def favicon_url() -> str:
    """The site's icon: case 11, Trump's packing of eleven squares, drawn small as a
    data URI, so it costs no fetch. It names its ink and paper, since a tab has no page
    colour to inherit."""
    from devtools.render_frontier_page import packing_svg  # noqa: PLC0415

    svg = packing_svg(11, units=200, ink="#17202a", paper="#ffffff", frame_px=FAVICON_PX)
    svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    return f"data:image/svg+xml,{quote(svg)}"


def favicon_html(*, inline: bool = False, root: str = "") -> str:
    """The site's icon as the link every page's head carries once: the site's pages, the
    two papers, the workbench, each case's record file and each forwarder to a page of
    the site (`check_published_site.head_problems`)."""
    if inline:
        return f'<link rel="icon" type="image/svg+xml" href="{favicon_url()}">'
    return "\n".join(
        (
            f'<link rel="icon" type="image/svg+xml" href="{root}favicon.svg">',
            f'<link rel="icon" type="image/png" sizes="48x48" href="{root}favicon-48.png">',
            (
                f'<link rel="apple-touch-icon" sizes="180x180" '
                f'href="{root}apple-touch-icon.png">'
            ),
        )
    )


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
    structured_data: tuple[Mapping[str, Any], ...] = (),
    extra_meta: tuple[tuple[str, str], ...] = (),
    prepare_math: bool = True,
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
    head, _math_scripts = page_assets()
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
    page = _site_head(
        name,
        rendered.html,
        PageMeta(
            title,
            description,
            name,
            kind,
            structured_data=structured_data,
            extra_meta=extra_meta,
        ),
    )
    prose = 'class="kpress-prose kpress-long-text'
    page = page.replace(prose + '"', prose + ' site-page"', 1)
    page = _document_scrolls(name, page)
    page = _KPRESS_CELL_LABELS.sub("", page)
    # Site pages have no model-driven widgets; TOC/history use their static DOM.
    page = re.sub(
        r'<script type="application/json" id="kpress-(?:page-model|diagnostics)">.*?</script>',
        "",
        page,
        flags=re.DOTALL,
    )
    if rewrite_body is not None:
        page = rewrite_body(page)
    from devtools import site_assets  # noqa: PLC0415

    assets = site_assets.shared().assets
    programs = "".join(
        f"\n{site_assets.script_tag(ref, _FROM_ROOT)}"
        for ref in (
            kpress_client_asset(),
            *(assets.script_file(path) for path in (THEME_SCRIPT, *page_scripts)),
        )
    )
    page = page.replace("</body>", f"{programs}\n</body>", 1)
    from devtools import site_math  # noqa: PLC0415

    if prepare_math:
        page = site_math.prepare(page)
    assert_fetches_only_assets(name, page)
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


def kpress_client_asset() -> AssetRef:
    """kpress's contents-rail and history modules as one classic script, a file of the
    site's shared assets.

    Flattened by the explainer's checked flattener, since kpress ships them as modules,
    which a page read from a file cannot load; see
    `render_n11_lower_bounds_explainer.kpress_client_js`.
    """
    from devtools import site_assets  # noqa: PLC0415
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
    return site_assets.shared().assets.script("kpress-behaviors.js", script)


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
        title="Square Packing: Bounds, Results and Best Packings",
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
        "EPISTEMICS_URL": "epistemics.html",
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
        name=RESULTS_META.path,
        current="results",
        title=RESULTS_META.name,
        description=RESULTS_META.description,
        toc=False,
        page_scripts=(TABLE_SCRIPT, POPOVER_SCRIPT, ROW_POPOVER_SCRIPT),
    )


def papers_page() -> Page:
    """The Papers section's page: a short introduction and one large card per paper,
    each the link to its paper, which is a full page of the site. It has no popover,
    so it carries no popover script. The introduction's links to the three parts of the
    series are the cards' own addresses, filled from the one constant each."""
    from devtools import overview_sections  # noqa: PLC0415

    values = {
        "PAPER_CARDS": overview_sections.paper_cards(),
        "LOWER_BOUNDS_PAPER": overview_sections.LOWER_BOUNDS_PAPER,
        "THRESHOLD_BOUND_PAPER": overview_sections.THRESHOLD_BOUND_PAPER,
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
        name=FRONTIER_META.path,
        current="frontier",
        title=FRONTIER_META.name,
        description=FRONTIER_META.description,
        structured_data=(
            {
                "@context": "https://schema.org",
                "@type": "Dataset",
                "name": "Square packing frontier register",
                "description": FRONTIER_DESCRIPTION,
                "url": canonical_url("frontier.html"),
                "license": repo_url("LICENSE"),
                "creator": {"@type": "Organization", "name": PROJECT_NAME},
            },
        ),
        toc=False,
        rewrite_body=_case_links,
        page_scripts=(TABLE_SCRIPT, POPOVER_SCRIPT, CASE_POPOVER_SCRIPT),
    )


def static_content_page(body: str, *, meta: PageMeta, current: str) -> Page:
    """A complete styled page around an already rendered article."""
    from devtools import site_assets, site_math  # noqa: PLC0415
    from devtools.render_case_pages import rebase_links  # noqa: PLC0415
    from devtools.render_n11_lower_bounds_explainer import (  # noqa: PLC0415
        kpress_static,
        theme_bootstrap,
    )

    head, _math_scripts = page_assets()
    programs = "\n".join(
        site_assets.script_tag(site_assets.shared().assets.script_file(path), _FROM_ROOT)
        for path in (THEME_SCRIPT,)
    )
    page = fill(
        (TEMPLATES / "case-record.html").read_text(encoding="utf-8"),
        {
            "HEAD": head_tags(meta) + "\n" + favicon_html() + head,
            "BOOTSTRAP": theme_bootstrap(kpress_static()) + "\n" + _script_text(EMBED_SCRIPT),
            "NAV": nav_html(current),
            "RECORD": body,
            "FOOTER": colophon_html(),
            "PROGRAMS": programs,
        },
        where="case-record.html",
    )
    page = site_math.prepare(page)
    directory = str(Path(meta.path).parent)
    if directory != ".":
        page = rebase_links(page, directory)
    assert_fetches_only_assets(meta.path, page)
    return Page(meta.path, page)


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
    from devtools.site_documents import chapter_pages  # noqa: PLC0415

    return [*[build() for build in PAGES.values()], *chapter_pages()]


def result_fragments() -> list[Page]:
    """Every result as a complete page; row overlays extract its article on input."""
    from devtools import overview_data, overview_sections  # noqa: PLC0415

    overview = overview_data.load()
    pages = []
    for result in overview.results:
        path = overview_sections.result_fragment(result.id)
        summary = overview_sections.plain_text(result.summary)
        description = f"{result.id}: {summary}. {result.credit}; {result.status}."
        if len(description) > DESCRIPTION_LIMIT:
            description = description[: DESCRIPTION_LIMIT - 1].rsplit(" ", 1)[0] + "."
        meta = PageMeta(
            f"{result.id}: {summary[:90]}",
            description,
            path,
            structured_data=(
                breadcrumb_data(
                    ("Home", "index.html"), ("Every Result", RESULTS_PAGE), (result.id, path)
                ),
            ),
        )
        body = overview_sections.result_row_popover_body(result, overview)
        body = body.replace('<div class="site-result"', '<article class="site-result"', 1)
        body = body.removesuffix("</div>") + "</article>"
        heading = (
            f'<h1 id="{result.id.lower()}">{html.escape(result.id)}: '
            f"{overview_sections.tex_bounds(result.summary)}</h1>"
        )
        body = body.replace(">", ">" + heading, 1)
        pages.append(static_content_page(body, meta=meta, current="results"))
    return pages


def forwarded_metas() -> dict[str, PageMeta]:
    """Each page of the site a forwarder leads to (`MOVED_PAGES`), by its path, with the
    record that page writes its own head from: the results page's and the frontier
    atlas's (`RESULTS_META`, `FRONTIER_META`), the record page's
    (`render_case_pages.cases_meta`), and each paper's `page_meta`, the explainer's as the
    site publishes it. They are read from the pages' own records and not restated, so a
    forwarder cannot preview a page by another name, kind or description than the
    page's own head gives it.

    The renderers are imported here rather than at the top, as in `inputs`, since each of
    them imports this module."""
    from devtools import render_case_pages, render_n11_optimality_review  # noqa: PLC0415
    from devtools import render_n11_lower_bounds_explainer as explainer  # noqa: PLC0415

    metas = (
        RESULTS_META,
        FRONTIER_META,
        render_case_pages.cases_meta(),
        explainer.published_page_meta(),
        render_n11_optimality_review.page_meta(),
    )
    return {meta.path: meta for meta in metas}


def forwarder_head(new: str, meta: PageMeta | None, *, old: str = "") -> str:
    """A forwarder's identity, by the rule for where it leads (`forwarder_pages`).

    To a page of the site, the identity that page's own head carries: the site's whole
    set, written from `meta`, the page's own record (`forwarded_metas`), and the site's
    icon. Its canonical link and `og:url` are the page's, so a consumer that keys a
    preview by `og:url` files the share under the page, and its name, its kind, its
    description and, for a paper, its dates are the page's, so a shared old address
    previews the page as a share of the page would. It is held as any page's head is
    (`check_published_site.head_problems`), and against the page's own head wherever the
    check has that too (`check_published_site.forwarder_problems`).

    Off the site, where `meta` is None, its title (`OFF_SITE_TITLES`) and a canonical
    link to that address and nothing else: the site does not write the page it leads
    to, so a preview could not say what it shows.
    """
    if meta is None:
        return (
            f"<title>{html.escape(OFF_SITE_TITLES[new], quote=False)}</title>\n"
            f'<link rel="canonical" href="{html.escape(new, quote=True)}">'
        )
    return f"{head_tags(meta)}\n{favicon_html(root='../' * old.count('/'))}"


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

    A forwarder to a page of the site also carries a link preview of that page
    (`forwarder_head`), since an old address is still shared: GitHub Pages cannot answer
    one with a redirect a crawler follows, and the crawlers that draw link previews run
    no script and do not reliably follow a refresh, so a forwarder with a title and a
    canonical link alone previewed as a bare title or as nothing (think-esmk,
    2026-10-03). Its preview is the page's own, at the page's address, with the site's
    card. The one forwarder off the site, the defect log's, carries no preview.
    """
    import posixpath  # noqa: PLC0415

    metas = forwarded_metas()
    template = FORWARDER.read_text(encoding="utf-8")
    pages = []
    for old, new in MOVED_PAGES:
        external = new.startswith("https://")
        target = new if external else posixpath.relpath(new, posixpath.dirname(old))
        if old == "cases.html":
            target = "cases/"
        meta = None if external else metas.get(new)
        if not external and meta is None:
            raise SystemExit(f"{old} forwards to {new}, which `forwarded_metas` does not name")
        values = {
            "TARGET": html.escape(target, quote=True),
            "TITLE": html.escape(OFF_SITE_TITLES[new] if meta is None else meta.name),
            "HEAD": forwarder_head(new, meta, old=old),
            "FORWARD_SCRIPT": _script_text(FORWARD_SCRIPT),
        }
        page = fill(template, values, where=FORWARDER.name)
        if old == "cases.html":
            from devtools.render_frontier_page import frontier_cases  # noqa: PLC0415

            known = ",".join(str(case["n"]) for case in frontier_cases())
            page = page.replace("<html ", f'<html data-case-numbers="{known}" ', 1)
        assert_fetches_only_assets(old, page)
        pages.append(Page(old, page))
    return pages


def render_site() -> list[Page]:
    """Every file this module writes: the pages, the result fragments, the case record
    files, and a forwarder at each address a page used to have."""
    return [*render_all(), *result_fragments(), *case_records(), *forwarder_pages()]


def asset_files(files: Sequence[Page]) -> dict[str, bytes]:
    """The shared assets `files` name, by path under the site's `assets/`
    (`site_assets.SiteAssets.referenced`)."""
    from devtools import site_assets  # noqa: PLC0415

    return site_assets.shared().assets.referenced(file.html for file in files)


FAVICON_FILES = ("favicon.svg", "favicon-48.png", "apple-touch-icon.png")
SEARCH_CONSOLE_VERIFICATION = ""


def support_file_paths() -> tuple[str, ...]:
    """Lightweight declarations of stable files written beside overview pages."""
    from devtools.render_frontier_page import drawing_paths  # noqa: PLC0415

    return (*FAVICON_FILES, *drawing_paths())


@cache
def support_files() -> dict[str, bytes]:
    """Stable icons and standalone atlas drawings."""
    from devtools.render_frontier_page import drawing_files, packing_svg  # noqa: PLC0415
    from devtools.site_documents import document_files  # noqa: PLC0415

    svg = packing_svg(11, units=200, ink="#17202a", paper="#ffffff", frame_px=48)
    svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    data = svg.encode("utf-8")
    files = {"favicon.svg": data, **drawing_files(), **document_files()}
    for name in FAVICON_FILES[1:]:
        files[name] = (BROWSER / name).read_bytes()

    return files


def write_site(output: Path, files: Sequence[Page]) -> None:
    """Write `files` under `output`, with the shared assets they name under `assets/`,
    and drop any result fragment, case record file or asset already there that is not
    among them, so a directory built before a result was withdrawn, a case dropped or
    an asset changed does not keep serving it."""
    from devtools import site_assets  # noqa: PLC0415
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
    site_assets.write_assets(output, asset_files(files))
    for name, data in support_files().items():
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    # The registry lane adds crawl files after all declared producer outputs.


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
        from devtools import site_assets  # noqa: PLC0415

        stale += site_assets.stale_assets(
            output, asset_files([*pages, *fragments, *records, *forwarders])
        )
        stale += [
            name
            for name, data in support_files().items()
            if not (output / name).is_file() or (output / name).read_bytes() != data
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
    shared = asset_files([*pages, *fragments, *records, *forwarders])
    print(
        f"wrote {len(shared)} shared assets under {output / 'assets'}/ "
        f"({sum(len(data) for data in shared.values()) // 1024} KB in all)"
    )
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
