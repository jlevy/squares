#!/usr/bin/env python3
"""Build the package workbench as a standalone page under `site/workbench/`.

GitHub Pages serves `packing/site` whole, so a subdirectory is a URL: this puts the
workbench at `/workbench/` beside the overview at `/` and the explainer, touching neither.
That separation is the point -- both are already published and may be linked from
elsewhere, so nothing here moves `site/index.html`.

The candidate generator produces a self-contained offline page. Publication extracts its
corpus, stylesheets, fonts and scripts into content-addressed files beside `index.html`.
A small loader validates the fetched corpus before starting the application, and displays
HTTP or decoding failures in the page. The policy permits resources from the same origin;
its inline favicon keeps this artifact independent of the site's root files.

The page no longer carries a banner calling itself unchecked, because it is checked. It
carries one quiet line saying what a reader does have to know -- that the animation model is
still moving, so a number it draws is not evidence -- and that line goes when the model
settles, which is a different question from where the code lives.

`--check` is the page's determinism contract: two independent full builds, compared byte for
byte. **The two run at once**, the published one into `--out` and its twin into a temporary
directory, so they never write one file, and the check costs one build's wall time rather
than two. A build is almost entirely child processes -- `build_candidate`, then the Node
corpus check -- so the threads waiting on them do not contend for the GIL.

Concurrency drops one thing the sequential form exercised: a second build that started after
the first had finished, and could read whatever the first left behind. Nothing is left
behind that a build reads (2026-09-15, from the code and from one watched run):
`build_candidate` and the Node tools it runs write only into their own temporary directories,
Node's compile cache is not enabled, and esbuild's build API keeps no disk cache; the run left
nothing in the checkout but CPython's `__pycache__` bytecode, which is derived from the source
rather than an input to the page. A future build that filled a cache and then read it would
show both twins the same cold cache, so `--check` would not see a cold build and a warm one
diverge. In exchange, a build that wrote to a fixed path now collides with its twin rather
than passing.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m workbench_tools.build_site
    uv run --frozen --all-extras --group dev python -m workbench_tools.build_site --check
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from functools import cache
from html import escape
from pathlib import Path

from kpress.format.assets import content_hash

from devtools import site_assets
from devtools.render_overview import (
    PageMeta,
    favicon_html,
    head_tags,
    nav_shell,
    visualize_tabs,
)
from workbench_tools.self_contained import assert_self_contained_html

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
REPO = PACKAGE_ROOT.parents[1]
ROOT = REPO / "packing"
WORKBENCH_PACKAGE = PACKAGE_ROOT
OUT = ROOT / "site/workbench"

ASSET_NAMESPACES = ("workbench/assets/css", "workbench/assets/js", "workbench/assets/fonts")
DATA_NAMESPACE = "workbench/data"

RENDER_INPUTS = (
    Path(__file__),
    ROOT / "devtools/render_n11_lower_bounds_explainer.py",
    ROOT / "devtools/site_assets.py",
    ROOT / "devtools/probes/site_assets/preload_fonts.js",
    ROOT / "src/sqpack/render",
    ROOT / "pyproject.toml",
    ROOT / "uv.lock",
    Path(__file__).with_name("build_candidate.py"),
    Path(__file__).with_name("self_contained.py"),
    WORKBENCH_PACKAGE / "assets/template.html",
    WORKBENCH_PACKAGE / "assets/workbench.css",
    WORKBENCH_PACKAGE / "src/application.js",
    ROOT / "witnesses/known-best",
    ROOT / "atlas/known-best/rendering",
    ROOT / "atlas/known-best/manifest.json",
    ROOT / "atlas/known-best/composite-figure.json",
    ROOT / "atlas/known-best/bound-citations.json",
    # The stage prints the shared version, which is pinned here, so a re-pin redraws the page.
    ROOT / "src/sqpack/release.py",
    # The site's navigation bar, gear and theme, from the partial, stylesheet and program
    # every page of the site carries (`render_overview.nav_shell`).
    ROOT / "devtools/render_overview.py",
    ROOT / "devtools/templates/site-nav.html",
    ROOT / "devtools/templates/site-nav.css",
    ROOT / "devtools/templates/paper-type.css",
    ROOT / "devtools/overview/theme.js",
    REPO / "vendor/kpress",
    REPO / "package.json",
    REPO / "package-lock.json",
    REPO / ".node-version",
    WORKBENCH_PACKAGE / "package.json",
    WORKBENCH_PACKAGE / "src",
    WORKBENCH_PACKAGE / "tools/bundle-browser.ts",
    WORKBENCH_PACKAGE / "tools/build-assets.ts",
    WORKBENCH_PACKAGE / "tools/check-candidate-corpus.ts",
    WORKBENCH_PACKAGE / "tools/render-katex.ts",
    WORKBENCH_PACKAGE / "probes/bench-annealing.ts",
)
"""Everything the page is built from. The Pages workflow's path filter has to cover this
list, and `test_the_pages_filter_covers_every_render_input` is what says so -- which is what
stops a published page going stale when the data under it moves. The list is written by
hand, so `test_build_site_inputs.py` derives what this module and `build_candidate` name --
imports, modules run, paths joined, Node tools and their imports -- and requires this list
to cover it."""

NOTE = """<div id="site-note">
The animation model is still moving, so a number here is not evidence
&mdash; <a href="../">the overview</a> and the explainer beside it are the published work.
</div>"""
"""The one thing a reader of the published page has to know, said once and quietly.

It is **injected here rather than written into the template** because it is a property of
the published page and not of the page. The relative link reaches the project root from
`/squares/workbench/`, from a local static server, and from any other deployment subpath.

Where it sits and how it looks are both deliberate, and both are corrections. It was a
full-width strip in warning yellow at the top of `<body>` -- which put it outside
`#viewport`, the absolutely-positioned element that covers the whole window, so it showed
through against the chrome rather than sitting above the page. Now it is fixed to the
bottom right in the page's muted text colour at the caption size, in the corner the timing
readout does not use, and `pointer-events` stay off everywhere but the link so it cannot
swallow a drag. `body.capture` hides it, because a note about the page does not belong in a
frame of the video.

Only the element is injected. How it looks is `#site-note` in `assets/workbench.css`, in the
page's design tokens like everything else, and the controls end `--site-note-clearance` above
the window's floor so their last row is never under it.
"""

#: The page's entry in the site's navigation bar, which marks it as the current page.
NAV_PAGE = "visualize"
#: The page's tab in the Visualize section, whose first tab is the film at
#: `visualize.html`: the bar under the navigation marks it current.
SECTION_TAB = "workbench"
#: Where the site's root is from the page: it is served at `workbench/index.html`.
NAV_ROOT = "../"


#: What the published page says of itself in its head: its name, its sentence and the
#: address it is served at, `workbench/` under the site's root.
PAGE = PageMeta(
    name="Workbench",
    description=(
        "An interactive workbench for packing unit squares in a square: animate the best "
        "packings known, or pack any number of squares and move them yourself."
    ),
    path="workbench/index.html",
)
TITLE = re.compile(r"<title>[^<]*</title>")


def with_head(page: str) -> str:
    """Give the page the site's identity tags in place of the template's bare title.

    The title, the description, the canonical link and the link preview are the site's
    one set (`render_overview.head_tags`), written from `PAGE`, so a shared link to the
    workbench previews as every other page of the site does. Like the bar, they are a
    property of the published page: the candidate the checkers open keeps its own title.
    Their absolute addresses identify the page without loading a resource.
    """
    head = page.find("</head>")
    found = TITLE.search(page)
    if found is None or head < 0 or found.start() > head:
        raise ValueError("could not place the site's head tags; the page has no title")
    return f"{page[: found.start()]}{head_tags(PAGE)}{page[found.end() :]}"


def with_nav(page: str) -> str:
    """Give the page the site's navigation bar, as every page of the site has it.

    The bar is the site's own, rendered from its one partial by `render_overview.nav_shell`
    rather than written again here, with Visualize marked current and its links reaching
    the site's root, and under it the Visualize section's tabs with Workbench current, so
    this page and the film's (`visualize.html`) read as one section and every existing
    `workbench/` link lands on its tab. Its stylesheet and kpress's theme bootstrap open
    the head, so the reader's stored theme is on the root before anything is drawn; the
    page's own stylesheet follows them. The bar opens the body, above `#viewport`, which
    `assets/workbench.css` then lays out below it, and the gear's program closes the body.
    Like the note, it is a property of the published page: `body.capture` hides it.
    """
    shell = nav_shell(NAV_PAGE, root=NAV_ROOT, tabs=visualize_tabs(SECTION_TAB, root=NAV_ROOT))
    shell = shell._replace(head=shell.head.replace(favicon_html(), favicon_html(inline=True)))
    head = HEAD.search(page)
    body = BODY.search(page)
    if head is None or body is None or "</body>" not in page:
        msg = "could not place the site's navigation bar; the page has no head or body"
        raise ValueError(msg)
    page = (
        f"{page[: head.end()]}\n{shell.head}{page[head.end() : body.end()]}\n"
        f"{shell.header}{page[body.end() :]}"
    )
    return page.replace("</body>", f"{shell.script}\n</body>", 1)


#: The published page loads scripts, fonts, styles and its corpus from its own origin.
#: Inline theme bootstraps and style attributes remain enabled; no evaluation of strings
#: or third-party resource source is permitted. The candidate stays self-contained.
#:
#: No `'unsafe-eval'`: the page does not evaluate strings, and the public page is not
#: loosened for test tooling. Playwright compiles an expression-string `wait_for_function`
#: predicate inside the page, which this policy refuses, so every checker's predicates are
#: probe functions and no checker opens the page with `bypass_csp`. `check_page_policy`
#: holds this policy to what the page needs.
CONTENT_SECURITY_POLICY = (
    "default-src 'none'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data: blob:; font-src 'self' data:; connect-src 'self'; "
    "base-uri 'none'; form-action 'none'"
)
POLICY_META = f'<meta http-equiv="Content-Security-Policy" content="{CONTENT_SECURITY_POLICY}">'
HEAD = re.compile(r"<head(?:\s[^>]*)?>", re.IGNORECASE)
BODY = re.compile(r"<body(?:\s[^>]*)?>", re.IGNORECASE)

REVISION = re.compile(r"[0-9a-f]{40}")


def with_policy(page: str) -> str:
    """Put the page's Content-Security-Policy first in `<head>`.

    A policy delivered by `<meta>` governs only what follows it, so it opens the head,
    before the inline style and script it has to cover.
    """
    head = HEAD.search(page)
    if head is None:
        raise ValueError("could not place the page's security policy; the page has no <head>")
    return f"{page[: head.end()]}\n{POLICY_META}{page[head.end() :]}"


def source_revision() -> str:
    """The exact checkout revision whose sources the page embeds."""
    found = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    revision = found.stdout.strip()
    if found.returncode != 0 or REVISION.fullmatch(revision) is None:
        raise ValueError("could not determine the workbench source revision")
    return revision


def source_dirty() -> bool:
    """Whether the checkout carries changes beyond its stamped commit."""
    found = subprocess.run(
        ("git", "status", "--porcelain", "--untracked-files=all"),
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    if found.returncode != 0:
        raise ValueError("could not determine whether the workbench source is dirty")
    return bool(found.stdout.strip())


def build_metadata(revision: str) -> str:
    """The machine-readable source identity checked after deployment."""
    if REVISION.fullmatch(revision) is None:
        raise ValueError(f"invalid workbench source revision: {revision!r}")
    return f'<meta name="squares-workbench-revision" content="{revision}">'


def dirty_metadata(*, dirty: bool) -> str:
    """The conservative source-state marker consumed by capture receipts."""
    return f'<meta name="squares-workbench-dirty" content="{str(dirty).lower()}">'


@cache
def published_script() -> str:
    """Build the data loader separately from the self-contained candidate application."""
    with tempfile.TemporaryDirectory(prefix="squares-workbench-loader-") as scratch:
        output = Path(scratch) / "published.js"
        subprocess.run(
            (
                "node",
                str(WORKBENCH_PACKAGE / "tools/bundle-browser.ts"),
                str(WORKBENCH_PACKAGE / "src/published.ts"),
                str(output),
            ),
            cwd=REPO,
            check=True,
            capture_output=True,
            text=True,
        )
        return output.read_text(encoding="utf-8")


_DATA_BLOCK = re.compile(
    r'<script id="atlas-data" type="application/json">(.*?)</script>', re.DOTALL
)
_APPLICATION_BLOCK = re.compile(
    r'(<script id="atlas-data"[^>]*>.*?</script>)\s*<script>(.*?)</script>', re.DOTALL
)


def publish_assets(page: str, out: Path) -> str:
    """Split the validated offline candidate into an HTML shell and hashed resources."""
    match = _APPLICATION_BLOCK.search(page)
    data_match = _DATA_BLOCK.search(page)
    if match is None or data_match is None:
        raise ValueError("the workbench has no unique data/application pair")
    data = json.dumps(
        json.loads(data_match.group(1)),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    data_path = f"data/corpus.{content_hash(data)}.json"
    assets = site_assets.SiteAssets()
    application = assets.script("workbench.js", match.group(2))
    loader = assets.script("published.js", published_script())
    island = (
        '<script id="atlas-data" type="application/json" '
        f'data-src="{data_path}" '
        f'data-application-src="{escape(site_assets.asset_href(application, "index.html"))}"'
        ">null</script>"
    )
    page = (
        page[: match.start()]
        + island
        + site_assets.script_tag(loader, "index.html")
        + page[match.end() :]
    )
    status = '<p id="workbench-startup" role="status">Loading packing data…</p>'
    page = page.replace('<div id="viewport">', status + '<div id="viewport">', 1)
    page, files = site_assets.link_inline_assets(page, "index.html", assets=assets)
    # The application is requested by the loader, not by a resource-bearing HTML tag.
    files.update(assets.files())
    site_assets.write_assets(out, files)
    destination = out / data_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    # This producer exclusively owns workbench/assets and workbench/data. Remove only
    # obsolete content-addressed files it previously emitted, never another namespace.
    wanted = {f"assets/{name}" for name in files} | {data_path}
    for folder in (out / "assets", out / "data"):
        for old in folder.rglob("*"):
            if (
                old.is_file()
                and re.fullmatch(r"[\w.-]+\.[0-9a-f]{16}\.(?:css|js|woff2|json)", old.name)
                and old.relative_to(out).as_posix() not in wanted
            ):
                old.unlink()
    if len(page.encode("utf-8")) > 600_000:
        raise ValueError("published workbench HTML exceeds its 600 KB budget")
    return page


def build(
    out: Path,
    *,
    revision: str | None = None,
    dirty: bool | None = None,
    citations: Path | None = None,
) -> str:
    """Validate an offline candidate, publish its assets, and return the HTML shell.

    `citations` stands in for the register's citation file, for a page built from a fixture.
    """
    extra = ["--citations", str(citations)] if citations is not None else []
    with tempfile.TemporaryDirectory() as scratch:
        # Captured so a working build stays quiet, but reported on failure: `check=True`
        # alone raises a CalledProcessError whose message is the exit status and the
        # argv, with the child's traceback sealed inside the exception object. A CI log
        # then says only "returned non-zero exit status 1", which is how a hard-coded
        # absolute path in the generator survived a whole run unnamed.
        built = subprocess.run(
            [
                sys.executable,
                "-m",
                "workbench_tools.build_candidate",
                "--out",
                scratch,
                "--all",
                *extra,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if built.returncode != 0:
            msg = (
                f"workbench_tools.build_candidate exited {built.returncode}\n"
                f"--- stderr ---\n{built.stderr.strip() or '(empty)'}\n"
                f"--- stdout ---\n{built.stdout.strip() or '(empty)'}"
            )
            raise ValueError(msg)
        candidate = Path(scratch) / "workbench.html"
        checked = subprocess.run(
            (
                "node",
                str(WORKBENCH_PACKAGE / "tools/check-candidate-corpus.ts"),
                str(candidate),
            ),
            cwd=REPO,
            check=False,
            capture_output=True,
            text=True,
        )
        if checked.returncode != 0:
            msg = (
                f"generated workbench corpus check exited {checked.returncode}\n"
                f"--- stderr ---\n{checked.stderr.strip() or '(empty)'}\n"
                f"--- stdout ---\n{checked.stdout.strip() or '(empty)'}"
            )
            raise ValueError(msg)
        page = candidate.read_text(encoding="utf-8")

    assert_self_contained_html(page)

    identity = "\n".join(
        (
            build_metadata(revision or source_revision()),
            dirty_metadata(dirty=source_dirty() if dirty is None else dirty),
        )
    )
    marked = with_policy(with_nav(with_head(page))).replace(
        "</head>", f"{identity}\n</head>", 1
    )
    if identity not in marked:
        raise ValueError("could not stamp the page; it has no </head> to close")

    # At the end of the body, so it is inside `#viewport`'s stacking context and after the
    # stylesheet that defines the custom properties it borrows.
    marked = marked.replace("</body>", f"{NOTE}</body>", 1)
    if NOTE not in marked:
        msg = "could not place the page's note; the page has no </body> to close"
        raise ValueError(msg)

    out.mkdir(parents=True, exist_ok=True)
    marked = publish_assets(marked, out)
    (out / "index.html").write_text(marked, encoding="utf-8")
    return marked


def check_builds(
    out: Path,
    *,
    revision: str,
    dirty: bool,
    citations: Path | None = None,
) -> tuple[str, str]:
    """Build the page twice at once and return both texts, the published one first.

    Each build has its own directory -- `out` for the published page, a temporary directory
    for its twin, removed on return -- so neither reads or overwrites the other's
    `index.html`, and `out` is the only place a page is kept. Both are given one `revision`
    and one `dirty`, looked up once by the caller, so the stamps cannot differ and any byte
    difference is the build's own.

    The builds' child processes used the same CPU either way on a local reading (37.6 s one
    after the other, 34.9 s at once), so running them together adds no work; the wall it
    saves is the Pages workflow's to measure, where the sequential pair cost about 48 s.
    """
    with (
        tempfile.TemporaryDirectory(prefix="squares-workbench-twin-") as scratch,
        ThreadPoolExecutor(max_workers=2) as pool,
    ):

        def one(into: Path) -> str:
            return build(into, revision=revision, dirty=dirty, citations=citations)

        published = pool.submit(one, out)
        twin = pool.submit(one, Path(scratch))
        first, second = published.result(), twin.result()

        def files(root: Path) -> dict[str, bytes]:
            return {
                path.relative_to(root).as_posix(): path.read_bytes()
                for path in sorted(root.rglob("*"))
                if path.is_file()
            }

        if files(out) != files(Path(scratch)):
            raise ValueError("the workbench did not reproduce itself: emitted files differ")
        return first, second


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument(
        "--check", action="store_true", help="build twice at once and require byte equality"
    )
    ap.add_argument("--revision", help="full source commit to stamp (default: checkout HEAD)")
    ap.add_argument(
        "--citations", type=Path, help="bound citations to draw (default: the register's)"
    )
    o = ap.parse_args(argv)

    revision = o.revision or source_revision()
    dirty = source_dirty()
    if o.check:
        first, again = check_builds(
            o.out, revision=revision, dirty=dirty, citations=o.citations
        )
        if again != first:
            msg = (
                "the workbench did not reproduce itself; a published page must be deterministic"
            )
            raise ValueError(msg)
        print(f"deterministic, linked assets, {len(first) / 1024 / 1024:.1f} MB")
        return 0

    first = build(o.out, revision=revision, dirty=dirty, citations=o.citations)
    print(f"{o.out / 'index.html'}: {len(first) / 1024 / 1024:.1f} MB, same-origin assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
