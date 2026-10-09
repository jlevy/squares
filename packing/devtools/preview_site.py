#!/usr/bin/env python3
"""Build the whole published site into one directory, serve it, and screenshot it.

The Pages workflow assembles the site from five builds on five runners: the three papers
under `papers/`, each by its slug (`render_overview.PAPERS`: `n11-lower-bounds-explainer`,
with the atlas's files it shares with the overview at the root,
`n11-threshold-bound-review` and `n11-optimality-review`), the site pages from
`devtools.render_overview`, with a forwarder at each address a paper used to have, and
the workbench. This puts the same five side by side on one machine, so the site can
be looked at, and its navigation followed, before anything is deployed. It never deploys
and never writes into `packing/site/`.

A file that moved and cannot forward, a paper's Markdown or PDF, is served at its old
address as a copy, as the workflow's `publish` job leaves it (`copy_moved_files`). The
lower-bounds explainer's PDF is drawn by its own Pages job from `packing/site/`, which a
preview never writes, so a preview has that PDF only if one is put there.

With the pages it draws the card every page's link preview names
(`devtools.social_card`), at the site's root as the deploy serves it, and after every
build it holds each page's head to the site's identity and card tags and the card to its
size (`check_published_site.local_head_checks`, the checks the deployed site gets).

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.preview_site
    uv run --frozen --all-extras --group dev python -m devtools.preview_site --serve
    uv run --frozen --all-extras --group dev python -m devtools.preview_site --shots DIR
    uv run --frozen --all-extras --group dev python -m devtools.preview_site --shots DIR \
        --scheme light --scheme dark --page index.html
    uv run --frozen --all-extras --group dev python -m devtools.preview_site --clips

`--skip` leaves a slow build out, by its name: a paper's slug
(`n11-lower-bounds-explainer`, `n11-threshold-bound-review`, `n11-optimality-review`),
`pages` or `workbench`. A link to it then points at a missing page, which
the link check reports rather than fails on, and a build already in `--output` stays.
`--page` shoots only the pages it
names, each with any fragment (`frontier.html#n-11` is one case's row), and `--press`
names an element to press on each page that has one (a card, an atlas cell), so what it
opens is checked and shot too: its math, its wide blocks, and its words, none of which
may be broken across lines inside the word (`split_problem`). Every page is also laid
out at `CLIP_WIDTHS`, with and without a scrollbar's width taken from the layout, and
fails where a table, a filter bar, a count or any other wide block runs past an ancestor
that clips or scrolls sideways. Set `SQPACK_CHROMIUM` to use a browser the environment
supplies, as the explainer's own tools do.
"""

from __future__ import annotations

import argparse
import contextlib
import functools
import gzip
import hashlib
import itertools
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import Sequence
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

from devtools import check_published_site, render_overview, site_urls, social_card

if TYPE_CHECKING:
    from playwright.sync_api import Browser, Page, Playwright
from devtools.render_n11_lower_bounds_explainer_pdf import BROWSER_OVERRIDE
from sqpack.probes import probe

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
DEFAULT_OUTPUT = Path(tempfile.gettempdir()) / "squares-site-preview"
#: The builds, in the order they run, each by its name: the first paper, whose page the
#: site's pages share the atlas's files with, the site's own pages, the workbench, then
#: every other paper of the site in reading order (`render_overview.PAPERS`), each by its
#: slug.
#: The papers built as the reviews are (`build_paper`): every paper but the first.
OTHER_PAPERS = tuple(
    paper.slug
    for paper in render_overview.PAPERS
    if paper.slug != render_overview.N11_LOWER_BOUNDS_EXPLAINER
)
BUILDS = (render_overview.N11_LOWER_BOUNDS_EXPLAINER, "pages", "workbench", *OTHER_PAPERS)
WIDTHS = (1280, 390)
PROBES = PACKING / "devtools" / "probes"
_OVERFLOW = probe(PROBES, "preview_site/overflow")
_MATH_PENDING = probe(PROBES, "preview_site/math_pending")
MATH_FACE = probe(PROBES, "preview_site/math_face")
_SCROLL_TOP = probe(PROBES, "preview_site/scroll_top")
_AT_FOOT = probe(PROBES, "preview_site/at_foot")
_CARDS = probe(PROBES, "measure_site_pages/cards")
CLIPPED = probe(PROBES, "preview_site/clipped")
HEADER = probe(PROBES, "preview_site/header")
BASELINES = probe(PROBES, "preview_site/baselines")
SPLIT_WORDS = probe(PROBES, "preview_site/split_words")
#: A run of this many characters with no space in it is a token, not a word: an evidence
#: identifier, an address, an exact decimal. One that is wider than the line it is set on
#: has to break somewhere; anything shorter fits every column the site sets text in, so a
#: column that breaks it is too narrow.
LONG_TOKEN = 24
#: What a line may end on inside a name without cutting a word: a hyphen or a dash.
HYPHENS = "-\u2010\u2011\u2013\u2014"
#: The widths every page is laid out at to look for a clipped wide block, beside the
#: two it is shot at: a tablet upright and on its side, where a narrow page clips at the
#: document's edge and a wide block has no room to spare.
CLIP_WIDTHS = (1024, 768)
#: A classic scrollbar's width, taken from the layout but not from the window: `100vw`
#: and a media query still see the whole window, which is what a block sized from the
#: window gets wrong. A headless browser draws its scrollbar over the page, so the check
#: narrows the page by this much itself.
SCROLLBAR_PX = 15
#: How far, in CSS pixels, a row of cards may sit off the centre of its line.
CENTRE_TOLERANCE = 1.0
#: How far apart, in CSS pixels, two labels of the header that share a line may stand.
BASELINE_TOLERANCE = 0.5
#: How long a page may take to typeset all its math before it is shot as it stands. The
#: site typesets the formulas near the viewport first and the rest in idle time
#: (`overview/math.js`); the synopsis's 1,357 took 40 to 50 seconds of scrolling in all.
MATH_WAIT_MS = 60_000
#: How long the pictures a page loads as it is scrolled may take to arrive.
LAZY_WAIT_MS = 5_000
#: How long what a press opens may take to typeset its math.
PRESS_WAIT_MS = 5_000
HREF = re.compile(r'<nav class="site-nav".*?</nav>', re.DOTALL)
#: Every address a built page links or frames.
HREF_ATTRIBUTE = re.compile(r'\s(?:href|src)="([^"]*)"')
#: The motion preference a tool opens a page that starts a film under: a reader's who
#: asks for reduced motion. The Visualize page starts its film on a visit unless the
#: reader asks that (`overview/film.js`), and the film is a 216 MB release download a page
#: would wait on and a shot would catch mid-frame; under this it stands at its poster and
#: nothing is fetched.
REDUCED_MOTION: Literal["reduce"] = "reduce"
#: The pages that start a film on a visit. Only they are opened under reduced motion:
#: every other page is opened as any reader's, since under reduced motion the overview's
#: formulas in closed popovers, which are typeset in idle time, were still untypeset when
#: `settle_math`'s wait ran out (229 of them at 1280 pixels, against none in ten seconds).
FILM_PAGES = ("visualize.html",)


def motion_for(name: str) -> Literal["reduce", "no-preference"]:
    """The motion preference a tool opens the page `name` under (`FILM_PAGES`)."""
    return REDUCED_MOTION if name.partition("#")[0] in FILM_PAGES else "no-preference"


def _run(*args: str) -> None:
    print("+", " ".join(args), flush=True)
    subprocess.run([sys.executable, "-m", *args], cwd=PACKING, check=True)


def build_lower_bounds_explainer(output: Path) -> None:
    """The lower-bounds explainer as its `prepare` job leaves it: the page and its
    Markdown under `papers/`, and the atlas's files it shows at the site's root."""
    _run("devtools.render_n11_lower_bounds_explainer", "--prepare-math", "--site", str(output))
    _run("devtools.render_n11_lower_bounds_explainer_pdf", "--site", str(output), "--update")


def build_workbench(output: Path) -> None:
    _run("workbench_tools.build_site", "--out", str(output / "workbench"))


def build_paper(slug: str, output: Path) -> None:
    """Build a paper's declared web and download editions as its Pages job does."""
    paper = render_overview.paper_record(slug)
    arguments = [paper.module, "--site", str(output)]
    if paper.has_pdf:
        arguments.append("--pdf")
    _run(*arguments)


def copy_moved_files(output: Path) -> list[str]:
    """Serve each file that moved and cannot forward at its old address too, as a copy of
    the file at its new one (`render_overview.MOVED_FILES`), which is what the
    workflow's `publish` job does. Returns the old addresses written; a file the build
    lacks, such as a PDF a skipped build would have drawn, has no copy."""
    copied = []
    for old, new in render_overview.MOVED_FILES:
        source = output / new
        if source.is_file():
            target = output / old
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            copied.append(old)
    return copied


def build(output: Path, skip: set[str]) -> None:
    output.mkdir(parents=True, exist_ok=True)
    if render_overview.N11_LOWER_BOUNDS_EXPLAINER not in skip:
        build_lower_bounds_explainer(output)
    if "pages" not in skip:
        pages = render_overview.render_all()
        fragments = render_overview.result_fragments()
        records = render_overview.case_records()
        forwarders = render_overview.forwarder_pages()
        render_overview.write_site(output, [*pages, *fragments, *records, *forwarders])
        for page in pages:
            print(f"wrote {output / page.name}")
        print(f"wrote {len(fragments)} result overviews beside them")
        print(f"wrote {len(records)} case record files under {output / 'cases'}")
        for forwarder in forwarders:
            print(f"wrote {output / forwarder.name}, a forwarder")
        print(f"wrote {social_card.write(output)}, the link preview's card")
    if "workbench" not in skip:
        build_workbench(output)
    for slug in OTHER_PAPERS:
        if slug not in skip:
            build_paper(slug, output)
    if "pages" not in skip:
        site_urls.write_crawl_files(output)
    for old in copy_moved_files(output):
        print(f"copied {output / old}, the address a file had before it moved")


def missing_links(output: Path) -> list[str]:
    """Every nav link on every built page that names a page this build lacks."""
    missing = []
    for name in render_overview.SITE_PAGES:
        path = output / name
        if not path.is_file():
            continue
        nav = HREF.search(path.read_text(encoding="utf-8"))
        if nav is None:
            missing.append(f"{name}: no site nav")
            continue
        base = path.parent
        for href in re.findall(r'href="([^"#?]+)', nav.group(0)):
            if href.startswith("https://"):
                continue
            target = (base / href).resolve()
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                missing.append(f"{name}: {href}")
    return missing


def moved_links(output: Path) -> list[str]:
    """Every link in the built site to an address that is now a forwarder
    (`render_overview.MOVED_PAGES`) or the old address of a file that moved
    (`MOVED_FILES`), as `page: href`. A forwarder keeps an old link working; a page of
    the site names where the reader is going. A directory is linked as its index, as
    `n11-optimality/` was."""
    forwarders = {old for old, _ in render_overview.MOVED_PAGES}
    moved = forwarders | {old for old, _ in render_overview.MOVED_FILES}
    found = []
    for path in sorted(output.rglob("*.html")):
        name = path.relative_to(output).as_posix()
        if name in forwarders:
            continue
        for href in sorted(set(HREF_ATTRIBUTE.findall(path.read_text(encoding="utf-8")))):
            if href.startswith(("https://", "http://", "#", "data:", "mailto:")):
                continue
            target = (path.parent / href.partition("#")[0].partition("?")[0]).resolve()
            if not target.is_relative_to(output):
                continue
            address = target.relative_to(output).as_posix()
            if address in moved or f"{address}/index.html" in moved:
                found.append(f"{name}: {href}")
    return found


class _Handler(SimpleHTTPRequestHandler):
    """A quiet static server. `/favicon.ico` gets an empty answer: no page declares an
    icon, so a browser's automatic request would otherwise log a 404 as a page error."""

    def do_GET(self) -> None:
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        super().do_GET()

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        pass


#: What GitHub Pages compresses, by suffix, and the freshness it gives every file: a
#: browser reuses a file it fetched in the last ten minutes without asking again.
PAGES_COMPRESSED = frozenset({".html", ".css", ".js", ".mjs", ".json", ".svg", ".md", ".txt"})
PAGES_CACHE_CONTROL = "max-age=600"


class _PagesHandler(_Handler):
    """`_Handler` answering as GitHub Pages does where a load's cost depends on it: a
    text file gzipped for a client that accepts it, every file fresh for ten minutes
    with an `ETag`, and a matching `If-None-Match` answered 304. So a measured load
    moves the bytes and reuses the cache a reader's browser would."""

    def do_GET(self) -> None:
        path = Path(self.translate_path(self.path))
        if path.is_dir():
            path = path / "index.html"
        if self.path == "/favicon.ico" or not path.is_file():
            super().do_GET()
            return
        data = path.read_bytes()
        tag = f'"{hashlib.sha256(data).hexdigest()[:16]}"'
        if self.headers.get("If-None-Match") == tag:
            self.send_response(304)
            self.send_header("ETag", tag)
            self.send_header("Cache-Control", PAGES_CACHE_CONTROL)
            self.end_headers()
            return
        compress = path.suffix in PAGES_COMPRESSED and "gzip" in self.headers.get(
            "Accept-Encoding", ""
        )
        body = gzip.compress(data, compresslevel=6, mtime=0) if compress else data
        self.send_response(200)
        self.send_header("Content-Type", self.guess_type(str(path)))
        self.send_header("Content-Length", str(len(body)))
        self.send_header("ETag", tag)
        self.send_header("Cache-Control", PAGES_CACHE_CONTROL)
        if compress:
            self.send_header("Content-Encoding", "gzip")
            self.send_header("Vary", "Accept-Encoding")
        self.end_headers()
        self.wfile.write(body)


def serve(output: Path, port: int, *, as_pages: bool = False) -> ThreadingHTTPServer:
    """Serve `output` on `port` in a thread. `as_pages` answers as GitHub Pages does,
    gzipped and cacheable (`_PagesHandler`), for a measurement of what a load costs."""
    handler = functools.partial(_PagesHandler if as_pages else _Handler, directory=str(output))
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def shot_stem(name: str) -> str:
    """A page's screenshot name, less its width: `workbench/index.html` is `workbench`,
    `frontier.html#n-11` is `frontier-n-11`, `cases/index.html#n-11` is `cases-n-11`, and
    a page in a directory keeps the directory's name, so every shot lands in the one
    folder."""
    stem = name.replace("/index.html", "").replace(".html", "")
    return stem.replace("#", "-").replace("/", "-")


def off_centre(sections: list[dict[str, Any]]) -> list[str]:
    """Every row of cards, in a `measure_site_pages cards` report of one page, that does
    not sit centred on its line: its slack at the start and at the end differ."""
    return [
        f"a row of {row['cards']} cards in {section['section'] or 'the page'} is off centre: "
        f"{row['start']}px before it, {row['end']}px after"
        for section in sections
        for row in section["rows"]
        if abs(row["start"] - row["end"]) > CENTRE_TOLERANCE
    ]


def tabs_problems(found: dict[str, Any]) -> list[str]:
    """What is wrong with where a page's section tabs stand, in a `preview_site/header`
    report. From the top a page of a section reads bar, rule, tabs, content: the tabs
    start at or below the foot of the rule under the navigation bar, and the content
    starts at or below the foot of the tabs. A page with no tabs has nothing to say."""
    tabs, rule, first = found["tabs"], found["rule"], found["first"]
    if tabs is None:
        return []
    if rule is None:
        return ["the section tabs have no rule over them, under the navigation bar"]
    problems: list[str] = []
    if tabs["top"] < rule["bottom"]:
        problems.append(
            f"the section tabs start {rule['bottom'] - tabs['top']:g}px above the foot of "
            f"the rule under the navigation bar, which is on {rule['on']}"
        )
    if first is not None and first["top"] < tabs["bottom"]:
        problems.append(
            f"{first['block']} starts {tabs['bottom'] - first['top']:g}px above the foot of "
            "the section tabs"
        )
    return problems


def baseline_problems(found: dict[str, Any]) -> list[str]:
    """What is wrong with the header's text baselines, in a `preview_site/baselines`
    report: the site's name, where its text is shown, stands on the baseline of the links
    of the bar's first line; the links of each line of the bar stand on one baseline; and
    the section tabs stand on one. Each is held to `BASELINE_TOLERANCE`, and the mark is
    held to the middle of the name's line by the same measure."""
    problems: list[str] = []
    lines: dict[int, list[dict[str, Any]]] = {}
    for link in found["links"]:
        lines.setdefault(link["top"], []).append(link)
    for group, what in ((list(lines.values()), "link"), ([found["tabs"]], "section tab")):
        for labels in group:
            if not labels:
                continue
            first = labels[0]
            for label in labels[1:]:
                offset = label["baseline"] - first["baseline"]
                if abs(offset) > BASELINE_TOLERANCE:
                    problems.append(
                        f"the {what} {label['label']} stands {offset:+g}px off the "
                        f"baseline of {first['label']}, beside it"
                    )
    if found["name"] is not None and lines:
        first = lines[min(lines)][0]
        offset = found["name"] - first["baseline"]
        if abs(offset) > BASELINE_TOLERANCE:
            problems.append(
                f"the site's name stands {offset:+g}px off the baseline of the bar's links"
            )
        text, logo = found["name_text"], found["logo"]
        if text is not None and logo is not None:
            lift = (logo["top"] + logo["bottom"] - text["top"] - text["bottom"]) / 2
            if abs(lift) > BASELINE_TOLERANCE:
                problems.append(
                    f"the site's mark is centred {lift:+g}px off the middle of its name's line"
                )
    return problems


def type_problems(found: dict[str, Any]) -> list[str]:
    """What is wrong with the size of the bar's type, in a `preview_site/header` report,
    held against the body's and never against a pixel value. A link in the bar, and a
    section tab, is one step below the body on the paper's scale and no more: smaller
    than the prose base, and no smaller than the largest step of the scale under it. The
    two are one size. The site's name is at least the body's size. A page with no bar has
    nothing to say, and nor does one that does not carry the paper's scale, the
    optimality paper, whose body is its own."""
    sizes = found["type"]
    if sizes["link"] is None or sizes["scale"] is None:
        return []
    body = sizes["scale"]["prose"]
    below = max(step for step in sizes["scale"].values() if step < body)
    problems: list[str] = []
    for part in ("link", "tab"):
        size = sizes[part]
        if size is None:
            continue
        if not below <= size < body:
            problems.append(
                f"a {part} in the header is {size:g}px: it should be under the body's "
                f"{body:g}px and no smaller than the step below it, {below:g}px"
            )
    if sizes["tab"] is not None and sizes["tab"] != sizes["link"]:
        problems.append(
            f"a section tab is {sizes['tab']:g}px and a link in the bar {sizes['link']:g}px"
        )
    if sizes["name"] is not None and sizes["name"] < body:
        problems.append(f"the site's name is {sizes['name']:g}px, under the body's {body:g}px")
    return problems


def clipped(page: Page) -> list[str]:
    """Every wide block on the page as it stands that runs past an ancestor which clips
    or scrolls sideways, as laid out now and again with a scrollbar's width taken from
    the layout; each named once, with how far it runs past either side."""
    problems: list[str] = []
    for scrollbar in (0, SCROLLBAR_PX):
        for found in page.evaluate(CLIPPED, {"scrollbar": scrollbar}):
            problem = clip_problem(found, scrollbar=scrollbar)
            if problem not in problems:
                problems.append(problem)
    return problems


def clip_problem(found: dict[str, Any], *, scrollbar: int = 0) -> str:
    """One clipped block, as the probe reports it, in words."""
    sides = " and ".join(
        f"{found[side]:g}px past its {side} edge" for side in ("left", "right") if found[side]
    )
    under = f", with a {scrollbar}px scrollbar" if scrollbar else ""
    return f"{found['block']} runs {sides} of {found['frame']}, which clips it{under}"


def clip_check(
    output: Path, port: int, pages: Sequence[str], widths: Sequence[int] = CLIP_WIDTHS
) -> list[str]:
    """Every clipped wide block on every built page at each of `widths`. A page is only
    laid out here, not walked or shot, since a block's box does not wait on its math."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    errors: list[str] = []
    server = serve(output, port)
    try:
        with sync_playwright() as driver:
            browser = launch_chromium(driver)
            for name in pages:
                if not (output / name.partition("#")[0]).is_file():
                    continue
                for width in widths:
                    page = browser.new_page(
                        viewport={"width": width, "height": 900},
                        reduced_motion=motion_for(name),
                    )
                    page.goto(f"http://127.0.0.1:{port}/{name}", wait_until="load")
                    page.wait_for_timeout(200)
                    errors.extend(f"{name} @{width}: {problem}" for problem in clipped(page))
                    page.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    return errors


def split_problem(found: dict[str, Any]) -> str | None:
    """One word set across lines, as the probe reports it, in words; nothing when every
    break in it is one a reader expects.

    A break is inside the word when it falls between two letters or digits: `low` over
    `er`, which only `overflow-wrap: anywhere` or `word-break` does, in a column squeezed
    narrower than the word. It is inside a name when the name is set as code or as a chip
    in a popover or a block the site builds and the line ends on one of its hyphens:
    `E-nagamochi-` over `lower` reads as two things. Any other break is ordinary: after
    the slash of a path, at a bracket or an ellipsis, after the hyphen of a compound in
    running text, and after a name's hyphen in a document's own prose, which KPress sets
    as it sets every report.

    One exception: a token of `LONG_TOKEN` characters or more that is wider than its line
    has to break somewhere.
    """
    word, pieces = found["word"], found["pieces"]
    name = found["code"] and not found["prose"]
    inside = any(
        (before[-1].isalnum() and after[0].isalnum()) or (name and before[-1] in HYPHENS)
        for before, after in itertools.pairwise(pieces)
    )
    if not inside or (len(word) >= LONG_TOKEN and found["width"] > found["line"]):
        return None
    where = found["host"]
    if found["block"] != where:
        where += f" in {found['block']}"
    framed = f", framed in {found['frame']}" if found["frame"] else ""
    return (
        f'"{" | ".join(pieces)}" is one word on {len(pieces)} lines in {where}{framed}: '
        f"{found['width']:g}px wide on a {found['line']:g}px line"
    )


#: What the headless shell is told about hinting. Its default is `HINTING_FULL`
#: (`headless/public/headless_browser.h`), under which Linux rounds every glyph's advance
#: to a whole pixel and a page measures wider than on macOS by up to a pixel a glyph: the
#: overview's 24ch measure read 232 px against 224.8, 9 px a digit against 8.7, and the
#: frontier table 1210.8 px in its 1200 px track (run 36943941580, D-513). `none` is the
#: value that lifts it (`headless/lib/browser/command_line_handler.cc`); on macOS, where
#: CoreText hints nothing, both tables measure the same with it as without.
FONT_RENDER_HINTING = "--font-render-hinting=none"


def launch_chromium(driver: Playwright, **options: Any) -> Browser:
    """The Chromium the site is measured in: the pinned one, or the one `SQPACK_CHROMIUM`
    names, with its text unhinted, so that a Linux reading is a macOS reading."""
    arguments = [FONT_RENDER_HINTING, *options.pop("args", ())]
    return driver.chromium.launch(
        executable_path=os.environ.get(BROWSER_OVERRIDE), args=arguments, **options
    )


def split_words(page: Page, root: str | None = None) -> list[str]:
    """Every word broken across lines, in what the page has open or in `root`, that
    `split_problem` calls a fault; each named once."""
    found = page.evaluate(SPLIT_WORDS, {"root": root} if root else None)
    return list(dict.fromkeys(filter(None, map(split_problem, found))))


def settle_math(page: Page) -> int:
    """Scroll the page through once, a screen at a time, to its foot, and on until every
    formula is typeset, then return to the top; returns how many were still untypeset
    when the wait ran out. Reaching the foot is what places whatever a page lays out or
    loads only as it nears the window, the atlas grid and a card's picture among them,
    even on a page whose math was done at once; what that starts loading is given
    `LAZY_WAIT_MS` to arrive, and a page that keeps the network busy is shot as it
    stands. The return is instant and waited for: the wheel's own scroll animates, and a
    screenshot taken during it was drawn offset."""
    from playwright.sync_api import TimeoutError as PlaywrightTimeout  # noqa: PLC0415

    deadline = time.monotonic() + MATH_WAIT_MS / 1000
    while time.monotonic() < deadline:
        if not page.evaluate(_MATH_PENDING) and page.evaluate(_AT_FOOT):
            break
        page.mouse.wheel(0, 800)
        page.wait_for_timeout(100)
    pending = page.evaluate(_MATH_PENDING)
    with contextlib.suppress(PlaywrightTimeout):
        page.wait_for_load_state("networkidle", timeout=LAZY_WAIT_MS)
    page.wait_for_timeout(200)
    page.wait_for_function(_SCROLL_TOP)
    return pending


def _pending(page: Page) -> int:
    """The math not yet typeset on the page and in every page it frames in view; a frame
    still loading counts as one."""
    from playwright.sync_api import Error as PlaywrightError  # noqa: PLC0415

    pending = 0
    for frame in page.frames:
        try:
            if frame is not page.main_frame and not frame.frame_element().is_visible():
                continue
            pending += frame.evaluate(_MATH_PENDING) if frame.url != "about:blank" else 1
        except PlaywrightError:
            pending += 1
    return pending


def press(page: Page, selector: str) -> list[str]:
    """Press the first element `selector` matches and wait for what it opens to typeset
    its math, a page it frames included (a card's popover frames its page); returns
    the formulas then set in the wrong face. A popover's math is only typeset once it
    opens, so the page's own check cannot see it."""
    page.locator(selector).first.click()
    page.wait_for_timeout(100)
    deadline = time.monotonic() + PRESS_WAIT_MS / 1000
    while _pending(page) and time.monotonic() < deadline:
        page.wait_for_timeout(100)
    page.wait_for_timeout(300)
    return page.evaluate(MATH_FACE)


#: A colour scheme a page is shot in, as Playwright names the two the site styles.
Scheme = Literal["light", "dark"]
#: The colour schemes a page is shot in: light alone unless `--scheme` asks for dark too.
SCHEMES: tuple[Scheme, ...] = ("light", "dark")


def shot_name(name: str, width: int, scheme: Scheme = "light", press: int = 0) -> str:
    """A screenshot's file name: the page's stem (`shot_stem`) and its width, `-dark`
    when it is shot in the dark scheme, and `-press<n>` for what the n-th selector
    pressed on it opened: `index-1280.png`, `index-390-dark.png`,
    `frontier-1280-dark-press1.png`."""
    dark = "-dark" if scheme == "dark" else ""
    pressed = f"-press{press}" if press else ""
    return f"{shot_stem(name)}-{width}{dark}{pressed}.png"


def screenshots(
    output: Path,
    shots: Path,
    port: int,
    pages: Sequence[str] = render_overview.SITE_PAGES,
    presses: Sequence[str] = (),
    *,
    schemes: Sequence[Scheme] = SCHEMES[:1],
) -> list[str]:
    """A full-page screenshot of every built page at each width, in each of `schemes`
    (light alone by default; a dark shot is named `-dark`, `shot_name`), with what went
    wrong:
    console errors, math left untypeset or set in the other face from its text, a row of
    cards off the centre of its line, any page wider than its viewport, section tabs
    that do not stand under the bar's rule (`tabs_problems`), a bar whose type is not
    one step under the body's (`type_problems`), a site name or a link off the bar's
    baseline (`baseline_problems`), and any wide block that
    runs past an ancestor which clips it (`clipped`). Each selector in
    `presses` is then pressed on every page that has a match, its math and its blocks
    checked the same way and its words for one broken across lines (`split_words`), and
    the window shot as `<page>-<width>-press<n>.png`. A page that starts a film is opened
    as for a reader who asks for reduced motion (`motion_for`), so the Visualize page's
    film is shot at its poster and its download never starts."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    shots.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    server = serve(output, port)
    try:
        with sync_playwright() as driver:
            browser = launch_chromium(driver)
            for name in pages:
                if not (output / name.partition("#")[0]).is_file():
                    continue
                for width, scheme in itertools.product(WIDTHS, schemes):
                    where = f"{name} @{width}" + (" dark" if scheme == "dark" else "")
                    page = browser.new_page(
                        viewport={"width": width, "height": 900},
                        reduced_motion=motion_for(name),
                        color_scheme=scheme,
                    )
                    page.on(
                        "console",
                        lambda message, where=where: (
                            errors.append(f"{where}: {message.text}")
                            if message.type == "error"
                            else None
                        ),
                    )
                    page.goto(f"http://127.0.0.1:{port}/{name}", wait_until="networkidle")
                    pending = settle_math(page)
                    if pending:
                        errors.append(f"{where}: {pending} math spans never typeset")
                    faces: list[str] = page.evaluate(MATH_FACE)
                    errors.extend(f"{where}: {mismatch}" for mismatch in faces)
                    errors.extend(
                        f"{where}: {problem}" for problem in off_centre(page.evaluate(_CARDS))
                    )
                    overflow = page.evaluate(_OVERFLOW)
                    if overflow > 0:
                        errors.append(f"{where}: {overflow}px wider than the viewport")
                    header = page.evaluate(HEADER)
                    errors.extend(
                        f"{where}: {problem}"
                        for problem in (
                            *tabs_problems(header),
                            *type_problems(header),
                            *baseline_problems(page.evaluate(BASELINES)),
                        )
                    )
                    cut = clipped(page)
                    errors.extend(f"{where}: {problem}" for problem in cut)
                    target = shots / shot_name(name, width, scheme)
                    page.screenshot(path=str(target), full_page=True)
                    print(f"shot {target}")
                    for index, selector in enumerate(presses, start=1):
                        if not page.locator(selector).count():
                            continue
                        errors.extend(
                            f"{where}, {selector} pressed: {mismatch}"
                            for mismatch in press(page, selector)
                            if mismatch not in faces
                        )
                        errors.extend(
                            f"{where}, {selector} pressed: {problem}"
                            for problem in clipped(page)
                            if problem not in cut
                        )
                        errors.extend(
                            f"{where}, {selector} pressed: {problem}"
                            for problem in split_words(page)
                        )
                        target = shots / shot_name(name, width, scheme, index)
                        page.screenshot(path=str(target))
                        print(f"shot {target}")
                        page.keyboard.press("Escape")
                    page.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    return errors


def _site_page(name: str) -> str:
    """A `--page` value: a page the site serves, with any fragment."""
    published = {row.path for row in site_urls.load_registry() if row.path.endswith(".html")}
    if name.partition("#")[0] not in published:
        served = ", ".join(sorted(published))
        raise argparse.ArgumentTypeError(f"{name} is not a page the site serves: {served}")
    return name


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--skip", action="append", choices=BUILDS, default=[])
    parser.add_argument("--shots", type=Path, help="write screenshots of every page here")
    parser.add_argument(
        "--page",
        action="append",
        type=_site_page,
        metavar="PAGE",
        help="with --shots or --clips: only this page, with any #fragment; repeatable",
    )
    parser.add_argument(
        "--press",
        action="append",
        default=[],
        metavar="SELECTOR",
        help="with --shots: press the first element this CSS selector matches on each page "
        "that has one, then check and shoot what it opens; repeatable",
    )
    parser.add_argument(
        "--scheme",
        action="append",
        choices=SCHEMES,
        metavar="SCHEME",
        help="with --shots: a colour scheme to shoot each page in, light or dark; "
        "repeatable, light alone by default, and a dark shot is named -dark",
    )
    parser.add_argument(
        "--clips",
        action="store_true",
        help="lay every page out at 1024, 768 and 390 pixels and report each wide block an "
        "ancestor clips, without shooting anything; --page narrows it",
    )
    parser.add_argument("--serve", action="store_true", help="serve the site until stopped")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args(argv)
    output = args.output.resolve()
    if output == (PACKING / "site").resolve():
        parser.error("the preview never writes into packing/site/")

    build(output, set(args.skip))
    status = 0
    for problem in missing_links(output):
        print(f"missing: {problem}", file=sys.stderr)
    for problem in moved_links(output):
        print(f"problem: a link to a page that moved: {problem}", file=sys.stderr)
        status = 1
    producers = tuple(
        "overview"
        if name == "pages"
        else "workbench"
        if name == "workbench"
        else f"paper:{name}"
        for name in BUILDS
        if name not in args.skip
    )
    for passed, line in check_published_site.local_site_checks(
        output, partial=bool(args.skip), producers=producers if args.skip else ()
    ):
        if not passed:
            print(f"problem: {line}", file=sys.stderr)
            status = 1
    if args.shots:
        pages = tuple(args.page or render_overview.SITE_PAGES)
        problems = screenshots(
            output,
            args.shots.resolve(),
            args.port,
            pages,
            args.press,
            # Each scheme asked for, once, in `SCHEMES`' order: light before dark.
            schemes=tuple(s for s in SCHEMES if s in (args.scheme or SCHEMES[:1])),
        )
        problems += clip_check(output, args.port, pages)
        for error in problems:
            print(f"problem: {error}", file=sys.stderr)
            status = 1
    if args.clips:
        pages = tuple(args.page or render_overview.SITE_PAGES)
        for error in clip_check(output, args.port, pages, (*CLIP_WIDTHS, WIDTHS[-1])):
            print(f"problem: {error}", file=sys.stderr)
            status = 1
    if args.serve:
        server = serve(output, args.port)
        print(f"serving {output} at http://127.0.0.1:{args.port}/ (Ctrl-C to stop)")
        try:
            threading.Event().wait()
        except KeyboardInterrupt:
            server.shutdown()
    return status


if __name__ == "__main__":
    raise SystemExit(main())
