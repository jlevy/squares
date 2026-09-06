#!/usr/bin/env python3
"""Export the rendered explainer to a print-quality PDF, from the page beside it.

The page has always had a PDF chip, and until now it opened the browser's print
dialog: the reader's own margins, the reader's own header and footer, and whatever
their browser had finished laying out when they pressed it. Printing still works --
the chip's handler is untouched -- but the artifact this writes is the one the project
owns and can hold to a standard.

What makes the output reproducible is the waiting, and it is worth stating because the
obvious recipe is wrong. `networkidle` fires on this page before KaTeX has typeset and
before the faces are applied: two renders taken that way differed by 440 KB, one of
them a partly-drawn document. Waiting on the page's own `html.math-ready` and on
`document.fonts.ready` closes that, and reduced motion closes the rest -- without it a
CSS transition is caught mid-flight and the graphics state differs in the fourth
decimal of an alpha. With all three, ten consecutive renders agreed byte for byte
except for `/CreationDate` and `/ModDate`.

That is a stronger guarantee than the composite PDF beside it manages: cairo assigns
font-subset tags per process, so two runs of `render_composite_pdf` differ. It is still
not a portable one, and the difference matters for what `--check` can mean. These bytes
are a function of the Chromium build, of which binary variant ran -- the headless shell
and full Chrome differ in about 99% of the output -- and of the fonts the host has. So
`--check` compares two renders taken here, now, in one browser, which is exactly the
guarantee `pages.yml` already asks of the HTML: a second render has to match the first.
It does not compare against a recorded digest. A check that fails on the next pin bump,
or on a contributor's laptop, is the check-that-can-never-pass this repository has been
bitten by before, and the lesson is written into the macOS job.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from collections.abc import Sequence
from pathlib import Path

from strif import atomic_output_file

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "site" / "index.html"
OUTPUT = ROOT / "site" / "t-018-explainer.pdf"

#: The two fields Chromium stamps from the clock, and the only two that move between
#: renders of one page. Normalised rather than removed: the length has to stay put or
#: every cross-reference offset after them shifts.
_DATES = re.compile(rb"/(CreationDate|ModDate) \(D:[^)]{0,32}\)")

#: What the page tells us it is ready. `math-ready` is set by the page's own script once
#: KaTeX has typeset; `document.fonts.ready` settles when the inlined faces are applied.
_READY = "html.math-ready"

#: A browser the environment supplies, for hosts that have one and cannot run
#: `playwright install` -- a sandbox with a preloaded cache, a distribution package, a CI
#: image that pins its own. Left unset, the driver finds the build its own pin names,
#: which is the reproducible path and what CI takes.
#:
#: Setting it is a statement that you want the tool to run, not that you want these
#: exact bytes: a different build writes a different file, and the difference is not
#: small. `--check` is unaffected either way, because it compares two renders from
#: whichever browser it just used rather than against a recorded digest.
_BROWSER_OVERRIDE = "SQPACK_CHROMIUM"

#: Where the page lives, so a link in the PDF points there rather than at whoever built
#: it. Kept in step with `render_explainer.SITE_URL` by the test beside this module.
SITE_URL = "https://jlevy.github.io/squares/"

#: The page is drawn from a `file://` URL, which is what keeps the render offline and
#: reproducible, and which turns every relative `href` into a link to the build
#: machine's disk. Two of them shipped that way -- one covering the whole atlas figure
#: -- pointing at `file:///home/.../known-best-1-100.pdf`: dead for every reader, and
#: the build path published along with them.
#:
#: Rewritten in the loaded page rather than fixed with a `<base>` tag, because a `<base>`
#: would also send the composite the figure shows to the network, and a render that
#: fetches is a render that can differ. Anchors only; `img` and `link` keep resolving
#: beside the file.
_ABSOLUTE_LINKS = """(site) => {
  for (const a of document.querySelectorAll('a[href]')) {
    const href = a.getAttribute('href');
    if (!href || /^[a-z][a-z0-9+.-]*:/i.test(href) || href.startsWith('#')) continue;
    a.setAttribute('href', new URL(href, site).href);
  }
}"""


def _normalised(pdf: bytes) -> bytes:
    """The document without its clock, for comparing one render against another."""
    return _DATES.sub(rb"/\1 (D:00000000000000+00'00')", pdf)


def render_pdf_bytes() -> bytes:
    """Draw the page as a PDF, waiting for it to be finished rather than for the network.

    `preferCSSPageSize` is what makes the stylesheet's `@page` rule decide the paper,
    and it is not optional here. The page declares `@page { size: Letter }`; without the
    flag Chromium centres that box on the API's paper and leaves dead bands around it.
    The margin is a stylesheet decision for a blunter reason: a `@page { margin }` in the
    document beats `page.pdf({margin})` outright, so the API argument is inert on this
    document and passing one only looks like it did something.

    `tagged` gives the file a structure tree, a language and headings, which is the
    difference between a document and a glyph soup for anyone reading it aloud. Measured
    at 5.5% more bytes for bit-identical layout. `outline` is a no-op without it --
    Chromium builds the bookmarks from the accessibility tree -- so the two are set
    together or not at all.
    """
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    with sync_playwright() as driver:
        # The default launch is the headless shell, and it stays the default on purpose:
        # `channel="chromium"` runs full Chrome in new-headless mode and rewrites about
        # 99% of the bytes for the same page and the same options.
        browser = driver.chromium.launch(executable_path=os.environ.get(_BROWSER_OVERRIDE))
        try:
            page = browser.new_page()
            page.emulate_media(media="print", reduced_motion="reduce")
            page.goto(PAGE.as_uri(), wait_until="load")
            page.wait_for_selector(_READY, timeout=60_000)
            page.evaluate("document.fonts.ready")
            page.evaluate(_ABSOLUTE_LINKS, SITE_URL)
            return page.pdf(
                print_background=True,
                prefer_css_page_size=True,
                tagged=True,
                outline=True,
            )
        finally:
            browser.close()


def _with_receipt(pdf: bytes, source: bytes) -> bytes:
    """Name the page these bytes were drawn from, after `%%EOF`.

    The same device the composite PDF and the atlas rasters use, for the same reason: a
    staleness link rather than a tamper check. Trailing bytes after `%%EOF` are ignored
    by readers and the cross-reference offsets are untouched, so appending is safe.
    """
    digest = hashlib.sha256(source).hexdigest()
    return pdf + f"\n%sqpack-source-html-sha256: {digest}\n".encode()


def update() -> None:
    written = _with_receipt(render_pdf_bytes(), PAGE.read_bytes())
    with atomic_output_file(OUTPUT, make_parents=True) as temporary:
        temporary.write_bytes(written)
    print(f"explainer PDF updated: {OUTPUT.name} ({len(written)} bytes)")


def check() -> None:
    """Two renders, one browser, one moment: the second has to match the first.

    Not a comparison against the committed file, because there is no committed file --
    the PDF is built in the Pages job and deployed, never checked in. What this catches
    is the failure that would actually reach a reader: a canvas race, a face that had
    not applied, an animation still running, anything that makes the page draw
    differently twice. Those are the defects that produced a 440 KB spread before the
    waiting was right.
    """
    first = _normalised(render_pdf_bytes())
    second = _normalised(render_pdf_bytes())
    if first != second:
        raise SystemExit(
            f"explainer PDF does not reproduce itself: {len(first)} then {len(second)} "
            "bytes, normalised. The page draws differently twice, which means something "
            "it draws is not finished when it is captured."
        )
    pages = first.count(b"/Type /Page\n") or first.count(b"/Type/Page")
    print(f"explainer PDF check passed: two renders agree, {len(first)} bytes, {pages} pages")


def main(argv: Sequence[str] | None = None) -> int:
    command = argparse.ArgumentParser(description=__doc__)
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true", help="write the PDF")
    mode.add_argument("--check", action="store_true", help="render twice and compare")
    arguments = command.parse_args(argv)
    if not PAGE.is_file():
        raise SystemExit(f"{PAGE.relative_to(ROOT)} is missing; render the page first")
    if arguments.update:
        update()
    else:
        check()
    return 0


if __name__ == "__main__":
    sys.exit(main())
