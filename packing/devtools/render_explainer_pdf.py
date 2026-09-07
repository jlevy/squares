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
READY = "html.math-ready"

#: A browser the environment supplies, for hosts that have one and cannot run
#: `playwright install` -- a sandbox with a preloaded cache, a distribution package, a CI
#: image that pins its own. Left unset, the driver finds the build its own pin names,
#: which is the reproducible path and what CI takes.
#:
#: Setting it is a statement that you want the tool to run, not that you want these
#: exact bytes: a different build writes a different file, and the difference is not
#: small. `--check` is unaffected either way, because it compares two renders from
#: whichever browser it just used rather than against a recorded digest.
BROWSER_OVERRIDE = "SQPACK_CHROMIUM"

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


#: The added faces, settled. `document.fonts.ready` had already resolved once, on a
#: document these faces were not in; a set that has not begun loading them reports
#: itself ready again straight away. Layout is forced and two frames are let through
#: first, so the faces the new rules bring into use are loading before the wait, which
#: is the same device `check_print_layout` uses after it switches media.
_FACES_APPLIED = """() => new Promise((done) => {
  void document.documentElement.offsetHeight;
  requestAnimationFrame(() => requestAnimationFrame(
    () => { document.fonts.ready.then(() => done(document.fonts.status)); },
  ));
})"""


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

    The last thing added to the page is a block of `@font-face` rules carrying static
    Source Sans 3 instances at the weights this page prints in. Chromium embeds a
    variable font only at its default position, so without them every sans glyph is a
    Type3 outline path, which viewers that smooth embedded text leave alone; the sans
    then reads a step lighter than the serif and the mathematics beside it.
    `devtools.sans_instances` is where the set is declared and checked, and injecting
    the faces here rather than rendering them into the page is what keeps the served
    `index.html` and the screen on the variable font.
    """
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    from devtools.sans_instances import print_face_css  # noqa: PLC0415

    with sync_playwright() as driver:
        # The default launch is the headless shell, and it stays the default on purpose:
        # `channel="chromium"` runs full Chrome in new-headless mode and rewrites about
        # 99% of the bytes for the same page and the same options.
        browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        try:
            page = browser.new_page()
            page.emulate_media(media="print", reduced_motion="reduce")
            page.goto(PAGE.as_uri(), wait_until="load")
            page.wait_for_selector(READY, timeout=60_000)
            page.evaluate("document.fonts.ready")
            page.evaluate(_ABSOLUTE_LINKS, SITE_URL)
            page.add_style_tag(content=print_face_css())
            page.evaluate(_FACES_APPLIED)
            return page.pdf(
                print_background=True,
                prefer_css_page_size=True,
                tagged=True,
                outline=True,
            )
        finally:
            browser.close()


#: Font dictionaries, read out of the file with a byte scan rather than a PDF parser.
#: That works because Chromium's Skia writer emits them uncompressed: it puts the page
#: content and the structure tree in streams, and leaves the font, descriptor and
#: encoding dictionaries as plain objects. So the scan needs no dependency, and the
#: cost of that shortcut is stated in `font_findings`: if the writer ever compresses
#: them the scan sees nothing at all, which is a failure rather than a pass.
_TYPE0 = re.compile(rb"/Subtype\s*/Type0\b")
_TYPE3 = re.compile(rb"/Subtype\s*/Type3\b")
_BASE_FONT = re.compile(rb"/BaseFont\s*/([^\s/<>\[\]()]+)")
_DESCRIPTOR_REF = re.compile(rb"/FontDescriptor\s+(\d+)\s+0\s+R")
_FONT_NAME = re.compile(rb"/FontName\s*/([^\s/<>\[\]()]+)")

#: The faces this page carries, by the PostScript name Chromium writes them under, with
#: the subset tag off. These are the ones the project answers for: it chose them, it
#: ships them inside the document, and if one of them is drawn as outline paths that is
#: a defect here. Prefixes, because an instanced or subsetted face is named from its
#: family with the axis or the style appended.
OWNED_FACES = ("PTSerif", "SourceSans3", "KaTeX_", "LocalPunct", "KPressMathText")

#: What a Type3 font is called when its descriptor cannot be read. Counted as ours: an
#: outline font this scan cannot attribute is not one to wave through.
UNNAMED = "unnamed"


def embedded_fonts(pdf: bytes) -> list[str]:
    """Every font the file names, by its `/BaseFont`, deduplicated and sorted.

    The six-character subset tag Chromium prefixes (`ABCDEF+PTSerif-Regular`) is kept:
    it is what distinguishes two subsets of one face, and dropping it would report one
    font where the file carries two.
    """
    seen = dict.fromkeys(name.decode("latin-1") for name in _BASE_FONT.findall(pdf))
    return sorted(seen)


def _indirect(pdf: bytes, number: int) -> bytes:
    """The body of one numbered object. Enough for the small dictionaries read here."""
    match = re.search(rb"(?m)^%d 0 obj\b" % number, pdf)
    if match is None:
        return b""
    end = pdf.find(b"endobj", match.end())
    return pdf[match.end() : end if end != -1 else len(pdf)]


def outline_fonts(pdf: bytes) -> list[str]:
    """The face behind every Type3 font in the file, in the order the file lists them.

    A Type3 font carries no `/BaseFont`; what it has is a `/FontDescriptor`, and the
    descriptor's `/FontName` is the face Chromium laid the run out in before it gave up
    on embedding it. The reference is resolved rather than assumed adjacent, and the
    Type3 dictionary is read only as far as its own `endobj`, so a second font later in
    the file cannot be mistaken for this one's descriptor.
    """
    found: list[str] = []
    for match in _TYPE3.finditer(pdf):
        end = pdf.find(b"endobj", match.end())
        body = pdf[match.end() : end if end != -1 else len(pdf)]
        ref = _DESCRIPTOR_REF.search(body)
        name = _FONT_NAME.search(_indirect(pdf, int(ref.group(1)))) if ref else None
        found.append(name.group(1).decode("latin-1").split("+")[-1] if name else UNNAMED)
    return found


def font_findings(pdf: bytes) -> list[str]:
    """Whether the faces this document ships are set in fonts, or drawn as paths.

    A Type3 font is not a font: it is a dictionary of drawing procedures, one per
    glyph, and Chromium writes one whenever it cannot embed the face a run was laid out
    in -- which for a variable font is any position but its default. The outlines carry
    the right weight, so nothing looks broken until the file is read in a viewer that
    smooths embedded text and leaves paths alone. Preview does, and the sans came out a
    step lighter than the serif beside it. `devtools.sans_instances` is the fix; this is
    the guard that says whether it took.

    Scoped to `OWNED_FACES` rather than to every Type3 font, and that limit is the
    honest one. Three characters on this page -- the relations and the arrow in the sans
    line -- are in no face the document carries, so the browser draws them from the
    host's own sans, and on macOS that is a variable font too. Failing on those would
    make the check pass on Linux and fail on a Mac for a glyph nobody here chose, which
    is the check-that-can-never-pass this module's own header warns about. They are
    reported instead, by `check`, so a fallback that grew is visible.

    Seeing no font dictionary of either kind is a failure and not a clean file. The
    scan reads the bytes directly, so a writer that started compressing them would
    report a document with no Type3 fonts in it and no fonts at all, and that reading
    has to be louder than a pass.
    """
    outlined = outline_fonts(pdf)
    if not _TYPE0.search(pdf) and not outlined:
        return [
            (
                "cannot see font dictionaries; the writer changed. The scan reads "
                "`/Subtype /Type0` and `/Subtype /Type3` out of the uncompressed "
                "objects Chromium writes, and this file has neither."
            )
        ]
    ours = sorted({n for n in outlined if n == UNNAMED or n.startswith(OWNED_FACES)})
    if ours:
        return [
            (
                f"{len(ours)} of the faces this page ships are drawn as Type3 outline "
                f"paths rather than embedded: {', '.join(ours)}. A viewer that smooths "
                "embedded text leaves them thin. Check that `sans_instances` has "
                "written the instances the page asks for and that the print stack "
                "names them."
            )
        ]
    return []


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

    The second question is about one render rather than about two, and no amount of
    self-agreement would answer it: whether the glyphs are set in fonts. A page that
    draws its sans as outline paths draws it that way every time.
    """
    first = _normalised(render_pdf_bytes())
    second = _normalised(render_pdf_bytes())
    if first != second:
        raise SystemExit(
            f"explainer PDF does not reproduce itself: {len(first)} then {len(second)} "
            "bytes, normalised. The page draws differently twice, which means something "
            "it draws is not finished when it is captured."
        )
    findings = font_findings(first)
    if findings:
        raise SystemExit("\n".join(findings))
    pages = first.count(b"/Type /Page\n") or first.count(b"/Type/Page")
    embedded = embedded_fonts(first)
    host = sorted(set(outline_fonts(first)))
    fallbacks = ", ".join(host)
    trailer = f"; drawn as outlines from the host's own fonts: {fallbacks}" if host else ""
    print(
        f"explainer PDF check passed: two renders agree, {len(first)} bytes, "
        f"{pages} pages, {len(embedded)} embedded fonts, none of them this page's "
        f"in outline paths{trailer}"
    )


def fonts() -> None:
    """One render, and what it set its glyphs in. For reading, not for gating."""
    pdf = render_pdf_bytes()
    for name in embedded_fonts(pdf):
        print(f"embedded  {name}")
    for name in sorted(set(outline_fonts(pdf))):
        print(f"outlines  {name}")
    for line in font_findings(pdf):
        print(line, file=sys.stderr)


def main(argv: Sequence[str] | None = None) -> int:
    command = argparse.ArgumentParser(description=__doc__)
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true", help="write the PDF")
    mode.add_argument("--check", action="store_true", help="render twice and compare")
    mode.add_argument("--fonts", action="store_true", help="list the fonts the PDF embeds")
    arguments = command.parse_args(argv)
    if not PAGE.is_file():
        raise SystemExit(f"{PAGE.relative_to(ROOT)} is missing; render the page first")
    if arguments.update:
        update()
    elif arguments.fonts:
        fonts()
    else:
        check()
    return 0


if __name__ == "__main__":
    sys.exit(main())
