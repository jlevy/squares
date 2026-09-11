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
from collections.abc import Iterable, Sequence
from functools import cache
from pathlib import Path

from strif import atomic_output_file

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "site" / "index.html"
OUTPUT = ROOT / "site" / "t-018-explainer.pdf"

#: The reviewed publication pagination. Unlike PDF bytes, this is portable across the
#: pinned Linux and macOS Chromium builds. A one-line metric change once moved Figure 1
#: and expanded the paper from 17 pages to 18 while every other check stayed green.
#: The theorem-first introduction and complete T-025/T-026 derivation deliberately bring
#: the reviewed v0.4.0 edition to 21.
EXPECTED_PAGE_COUNT = 21

#: The two fields Chromium stamps from the clock, and the only two that move between
#: renders of one page. Normalised rather than removed: the length has to stay put or
#: every cross-reference offset after them shifts.
_DATES = re.compile(rb"/(CreationDate|ModDate) \(D:[^)]{0,32}\)")

#: What the page tells us it is ready. `math-ready` is set by the page's own script once
#: KaTeX has typeset; `document.fonts.ready` settles when the inlined faces are applied.
READY = "html.math-ready"

#: Media changes and ResizeObserver callbacks can start asynchronous math renders.
#: Let layout dispatch them, then await those renders and the faces they request.
SETTLED = """async () => {
  void document.documentElement.offsetHeight;
  await new Promise(done => requestAnimationFrame(() => requestAnimationFrame(done)));
  await globalThis.squaresMath?.settled();
  await document.fonts.ready;
  await new Promise(done => requestAnimationFrame(done));
  await globalThis.squaresMath?.settled();
}"""

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


#: The family and weight properties KPress's `@page` margin boxes read, and a
#: sample every face answers with its `unicode-range` so `document.fonts.load` actually
#: fetches it. Read as the root's resolved values rather than as literal stacks, which
#: is what covers a host that redirects the tokens.
_MARGIN_BOX_TOKENS = (
    ("--kpress-font-sans", "--kpress-font-weight-sans-regular"),
    ("--kpress-font-prose", "--_kpress-font-weight-prose"),
)
_MARGIN_BOX_SAMPLE = "Aa Gg 0123"

#: The added faces, settled -- both the ones the document tree asks for and the ones
#: only an `@page` margin box does.
#:
#: `document.fonts.ready` had already resolved once, on a document these faces were not
#: in; a set that has not begun loading them reports itself ready again straight away.
#: So layout is forced and two frames are let through first, and the faces the new rules
#: bring into use are loading before the wait -- the same device `check_print_layout`
#: uses after it switches media.
#:
#: That covers the document tree and stops there, which is the gap this second half
#: closes: a margin box is not in the tree, so a face used only there never enters
#: `document.fonts.ready` and its first request lands inside `page.pdf()`, after the
#: page it belongs to is drawn. The families are therefore asked for by name and waited
#: on again. Nothing on this page is currently set in a margin box in a weight nothing
#: else uses, so the step changes no byte today; it is here so that restoring kpress's
#: sans footer does not silently print it in the fallback, where `sans_instances --check`
#: cannot see it either.
#:
#: This mirrors kpress's `_await_print_fonts` (`kpress/format/pdf.py`) rather than
#: calling it, and the reason is the underscore: the helper, the tokens, the sample and
#: the page protocol it takes are all private to that module, so importing them would
#: be this repository reaching past kpress's public surface. `think-y15p` asks kpress to
#: export it, and this block goes when it does. No timeout race, which is the one thing
#: dropped: kpress races one because a host page can name a face it fetches, while every
#: face here is already a data URI in a document loaded from `file://`, and Playwright's
#: own evaluate timeout is the backstop.
_FACES_APPLIED = """async ([tokens, sample]) => {
  void document.documentElement.offsetHeight;
  await new Promise((frame) => requestAnimationFrame(() => requestAnimationFrame(frame)));
  await document.fonts.ready;
  const root = getComputedStyle(document.documentElement);
  const stacks = tokens
    .map(([familyToken, weightToken]) => ({
      family: root.getPropertyValue(familyToken).trim(),
      weight: root.getPropertyValue(weightToken).trim() || root.fontWeight || '400',
    }))
    .filter((stack) => stack.family.length > 0);
  await Promise.all(stacks.map(
    (stack) => document.fonts.load(`${stack.weight} 1rem ${stack.family}`, sample)
      .catch(() => undefined),
  ));
  await document.fonts.ready;
  void document.documentElement.offsetHeight;
  return document.fonts.status;
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
            page.evaluate(_FACES_APPLIED, [list(_MARGIN_BOX_TOKENS), _MARGIN_BOX_SAMPLE])
            page.evaluate(SETTLED)
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

#: What tells a descriptor that carries the face from one that only names it. `/FontFile`
#: is Type1, `/FontFile2` TrueType, `/FontFile3` the compact forms; a descriptor with
#: none of them describes a font the reader is expected to already have.
_FONT_FILE = re.compile(rb"/FontFile[23]?\b")

#: The `/Type` a descriptor declares, which is how a real object is told from the same
#: bytes appearing inside a compressed stream.
_IS_DESCRIPTOR = re.compile(rb"/Type\s*/FontDescriptor\b")

#: One object's body, from its header to its own `endobj`. Anchored at a line start,
#: which is where the writer puts a header and where stream bytes only land by accident.
_OBJECT_BODY = re.compile(rb"(?ms)^\d+\s+0\s+obj\b(.*?)endobj")

#: The faces this page carries that are named the same whatever kpress calls its print
#: instances. `SourceSans3` is the variable face the screen reads in, and it is on the
#: list precisely because a Type3 font under that name is the defect the instances were
#: written to remove, coming back: a print run that missed them fell back to the
#: variable font. Prefixes, because an instanced or subsetted face is named from its
#: family with the axis or the style appended.
#:
#: `KPressQuotes` is the six-glyph face kpress now ships for the quotation marks and the
#: apostrophe, leading the prose stack through `--kpress-font-punctuation`. It replaces
#: `LocalPunct`, which was `local("Georgia")` and drew those marks from whatever the
#: reader's machine had -- the reason `Georgia` was on `EXPECTED_HOST_FONTS` and the
#: reason the shell overrode the prose stack for print. Both are gone; `LocalPunct` stays
#: on this list only until a kpress that still declares it can no longer be checked out.
#:
#: `PlanetaireMonoText` is kpress's mono face, which the page declares in all four styles
#: through `render_explainer.MONO_WEIGHTS`. Only the regular reaches the export -- the
#: page has no highlighted code and no bold or italic code span -- but the family is what
#: is listed, because which of a family's styles a run of code needs is the document's to
#: change and not the guard's to police.
_FIXED_FACES = (
    "PTSerif",
    "SourceSans3",
    "KaTeX_",
    "LocalPunct",
    "KPressMathText",
    "KPressQuotes",
    "PlanetaireMonoText",
)


@cache
def owned_faces() -> tuple[str, ...]:
    """The faces this page answers for, by the PostScript name Chromium writes them under.

    These are the ones the project chose, ships inside the document, and owes a proper
    embedding to: if one of them is drawn as outline paths that is a defect here.

    The static print instances are among them, and their name is not written down here.
    kpress derives it from the family it declares them under -- `KPress Print Sans`
    becomes `KPressPrintSans-410` -- and `devtools.sans_instances` derives the prefix
    the same way from the same source, so a rename upstream moves this scan with it
    instead of quietly narrowing it to faces the file no longer contains.

    Imported inside the function because `sans_instances` imports this module.
    """
    from devtools.sans_instances import postscript_prefix  # noqa: PLC0415

    return (*_FIXED_FACES, postscript_prefix())


#: What a Type3 font is called when its descriptor cannot be read. Counted as ours: an
#: outline font this scan cannot attribute is not one to wave through.
UNNAMED = "unnamed"

#: The one glyph source in this export that comes from the machine that drew it, with the
#: bead that records it. The 100-best atlas figure on page 3 is an SVG written by
#: `build_known_best_atlas.py`, which sets 468 labels in `font-family="Helvetica, Arial,
#: sans-serif"`; the export carries nine subsets of whatever that resolved to -- nine
#: `Helvetica-Bold` and `Helvetica-BoldOblique` subsets on this Mac. So the page's own
#: text has no host font in it and the figure inside it does, and both halves of that
#: sentence have to be said together.
#:
#: Accepted rather than pending, by the owner's decision (2026-09-07): the figure is
#: generated by its own pipeline, is published on its own, and stays as it is. `think-czt4`
#: is the record of the exception rather than a request to change the figure, and it is
#: here because an exception without a bead is a defect nobody wrote down -- the rule
#: `EXPECTED_HOST_FONTS` below states, and the last host family this file excused left
#: with its bead when the bead closed.
#:
#: Two names and not the figure's whole fallback chain, for the reason that mapping gives:
#: a name here is a face the guard stops looking at, so it holds what the figure has been
#: measured drawing with and nothing plausible beside it. Helvetica is this Mac; Liberation
#: Sans is the Linux runner that gates the export, where fontconfig aliases both Helvetica
#: and Arial to the metric-compatible substitute. `Arial` itself was listed once and is
#: not: no machine that draws this figure has been seen to answer with it, and a run that
#: did -- a Windows host, or a Linux one whose fontconfig stopped substituting -- is a
#: third face in the figure's labels, which is a finding to be looked at and then listed,
#: not a silence.
ATLAS_FACES: dict[str, str] = {"Helvetica": "think-czt4", "LiberationSans": "think-czt4"}


@cache
def allowed_families() -> tuple[str, ...]:
    """Every family this document is allowed to draw a glyph from.

    The rule behind it, the owner's on 2026-09-07: the explainer resolves every text run
    to a face the page ships. A family outside this list is a glyph the reader's own
    machine supplied, which is a different glyph for every reader and, when that
    machine's face is variable, outline paths instead of a font.

    A function rather than a tuple because `owned_faces` is one: the print instances'
    name is kpress's, and the guard follows it there rather than keeping a copy that a
    rename upstream would leave pointing at nothing.
    """
    return (*owned_faces(), *ATLAS_FACES)


#: The host families the page still leans on, each with the bead that removes it. Empty
#: since 2026-09-08, which is the state the rule asks for of the document's own text:
#: every run of it resolves to a face the page ships. It is not the whole export -- the
#: atlas figure's labels are still the drawing machine's, which is `ATLAS_FACES` and not
#: this, and the difference between the two mappings is whether anyone intends to close
#: the bead.
#:
#: The mapping is kept rather than deleted with its last entry, because it is the shape
#: an exception takes here and the shape is the point: an entry passes `--check` and is
#: reported as pending, so a guard can land before the fix it waits on and the file says
#: what it waits for. A family added without a bead is not an exception, it is a defect
#: nobody wrote down.
#:
#: Two entries are the roles and two are the same roles on another machine. The names are
#: the host's, so they are the host's names: macOS answers `ui-monospace` with Menlo and
#: `local("Georgia")` with Georgia, and the Linux runner that gates this answers the same
#: two with DejaVu Sans Mono and Liberation Serif.
#:
#: Measured rather than anticipated, and that is the rule for adding to it. A name here
#: is a face the guard stops looking at, so a plausible substitute nobody has seen is a
#: hole rather than insurance -- the generic Linux sans was listed once, and it is the
#: exact face a relation face that stopped loading would come back as on the runner. An
#: unlisted substitute on some other machine fails the check and names itself, which is
#: how the two below were found (`pages.yml`, run 34174661935).
#:
#: `Georgia` and its Linux substitute `LiberationSerif` came off on 2026-09-08, when
#: `kpr-2tmj` and `kpr-asj4` landed and the gitlink moved to them: the list marker is
#: drawn in CSS now instead of set as U+25AA, and the quotation marks come from the
#: shipped `KPress Quotes` rather than from `local("Georgia")`. Neither family appears in
#: the export any more, so listing them would only widen the guard.
#:
#: `Menlo` and its Linux substitute `DejaVuSansMono` came off the same day, when
#: `kpr-v731` landed Planetaire Mono Text and the page took it. They were `ui-monospace`
#: resolved on two machines, the last two glyph sources in this export the project did
#: not ship, and the reason this mapping existed.
EXPECTED_HOST_FONTS: dict[str, str] = {}


def family_of(base_font: str) -> str:
    """A `/BaseFont` without Chromium's six-character subset tag.

    `ABCDEF+PTSerif-Regular` is one subset of PT Serif; the tag distinguishes two subsets
    of one face and says nothing about which face it is, which is what provenance asks.
    """
    return base_font.rsplit("+", maxsplit=1)[-1]


def _listed(family: str, names: Iterable[str]) -> str | None:
    """The listed name this family is a face of, or `None`. Longest match wins."""
    matches = [name for name in names if _is_face_of(family, name)]
    return max(matches, key=len) if matches else None


def _is_face_of(family: str, name: str) -> bool:
    """Whether `family` is `name` itself, or a face of it, and by which of two rules.

    A name the page owns is a prefix, because the page owns everything under it and the
    names that come back are not one shape. Chromium writes a PostScript face into the
    PDF (`PTSerif-Italic`, `KPressPrintSans-410Italic`) and Blink answers the screen
    probe with the instance a variable face is at (`Source Sans 3 ExtraLight`, which is
    `SourceSans3` at 275). Neither is a family name, and both are ours.

    Every other name here is a host family -- the atlas figure's two and the pending
    substitutes -- and there a longer name is a different font, so it matches only
    itself and its `-` styles. Bare `startswith` gave each one a family tree of fonts a
    real machine has: `Helvetica` admitted `HelveticaNeue`, `LiberationSans` admitted
    `LiberationSansNarrow`, `Arial` admitted `ArialUnicodeMS` while it was listed, and
    `DejaVuSansMono` had to be read before `DejaVuSans` to land on the right bead.
    """
    if not family.startswith(name):
        return False
    if name in owned_faces():
        return True
    remainder = family[len(name) :]
    return not remainder or remainder.startswith("-")


def host_font_bead(family: str) -> str | None:
    """The bead a host family is waiting on, or `None` if nothing here expects it.

    Spaces are dropped before matching, so one mapping serves both sides of the guard:
    a PDF names a face `Menlo-Regular` and a browser names the same platform font
    `Menlo`, and a Linux runner names its mono `DejaVu Sans Mono` where the PDF would
    write `DejaVuSansMono`.
    """
    listed = _listed(family.replace(" ", ""), EXPECTED_HOST_FONTS)
    return EXPECTED_HOST_FONTS[listed] if listed else None


def shipped(family: str) -> bool:
    """Whether a family is one the page carries, or the atlas figure's exception."""
    return _listed(family.replace(" ", ""), allowed_families()) is not None


def atlas_face_bead(family: str) -> str | None:
    """The bead recording this family as the atlas figure's, or `None`.

    The same lookup as `host_font_bead` over the other mapping, so `--fonts` can name the
    export's one host-drawn family and the bead that records it instead of passing it in
    silence. A pending face is on its way out and an accepted one is not, which is the
    whole difference between the two mappings; both are reported, neither is hidden.
    """
    listed = _listed(family.replace(" ", ""), ATLAS_FACES)
    return ATLAS_FACES[listed] if listed else None


def _families_in(pdf: bytes) -> set[str]:
    """Every family the file draws from, whichever kind of font dictionary carries it."""
    families = {family_of(name) for name in embedded_fonts(pdf)}
    return families | {name for name in outline_fonts(pdf) if name != UNNAMED}


def atlas_faces_present(pdf: bytes) -> dict[str, str]:
    """The atlas figure's host families this file really carries, family to bead.

    Reported by `--check` and `--fonts` rather than left to a code comment, because the
    claim the guard is read as making -- no text run in this export comes from the
    machine that drew it -- is true of the document and not of the figure inside it. A
    reader of the output should not have to open this file to learn that.
    """
    found = {family: atlas_face_bead(family) for family in sorted(_families_in(pdf))}
    return {family: bead for family, bead in found.items() if bead is not None}


def provenance(pdf: bytes) -> tuple[list[str], dict[str, str]]:
    """Every family in the file that the page did not ship, split by whether it is known.

    The first list is the failure: a family that is neither one of this page's own, nor
    the atlas figure's accepted host sans, nor one of the host faces a named bead is on
    its way to removing. The mapping is those pending ones, family to bead, for reporting.

    Both kinds of font dictionary are read. An embedded host face and a host face drawn
    as outline paths are the same defect seen from two sides -- the reader's machine
    supplied a glyph -- and which of the two happens depends only on whether that
    machine's face is variable.
    """
    families = _families_in(pdf)
    unexpected: list[str] = []
    pending: dict[str, str] = {}
    for family in sorted(families):
        if shipped(family):
            continue
        bead = host_font_bead(family)
        if bead is None:
            unexpected.append(family)
        else:
            pending[family] = bead
    return unexpected, pending


def embedded_fonts(pdf: bytes) -> list[str]:
    """Every font whose program the file carries, by its `/BaseFont`, deduplicated.

    A `/BaseFont` names a face; it does not say the face travels with the document. A
    font dictionary whose descriptor has no `/FontFile*` is a reference to a font the
    reader is expected to own, and counting it here would have `--check` announce as
    embedded something this page does not ship -- the one reading this scan must never
    give, since shipping the faces is the whole claim. So a name is taken only once its
    descriptor is found to carry the program.

    For a Type0 font that descriptor hangs off the descendant CIDFont, which repeats the
    same `/BaseFont`; the Type0 parent has no descriptor of its own and contributes
    nothing the descendant does not.

    The six-character subset tag Chromium prefixes (`ABCDEF+PTSerif-Regular`) is kept:
    it is what distinguishes two subsets of one face, and dropping it would report one
    font where the file carries two.
    """
    seen: dict[str, None] = {}
    for body in _OBJECT_BODY.findall(pdf):
        name = _BASE_FONT.search(body)
        reference = _DESCRIPTOR_REF.search(body)
        if name is None or reference is None:
            continue
        if _FONT_FILE.search(_descriptor(pdf, int(reference.group(1)))):
            seen[name.group(1).decode("latin-1")] = None
    return sorted(seen)


def _descriptor(pdf: bytes, number: int) -> bytes:
    """The body of one numbered font descriptor, or nothing where the file has no such object.

    Three guards, one per way this could read the wrong bytes. The header is matched at
    a line start and the body ends at its own `endobj`, so what comes back is an object
    rather than a span. The body has to declare `/Type /FontDescriptor`, which is what
    separates a real object from the same byte sequence occurring inside a Flate stream
    -- compressed content can hold anything, a plausible object header included. And the
    last qualifying definition wins, because a file written in increments carries the
    superseded object first and the current one after it.
    """
    body = b""
    for match in re.finditer(rb"(?m)^%d\s+0\s+obj\b" % number, pdf):
        end = pdf.find(b"endobj", match.end())
        candidate = pdf[match.end() : end if end != -1 else len(pdf)]
        if _IS_DESCRIPTOR.search(candidate):
            body = candidate
    return body


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
        name = _FONT_NAME.search(_descriptor(pdf, int(ref.group(1)))) if ref else None
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

    Scoped to `owned_faces` rather than to every Type3 font, and that limit is the
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
    findings: list[str] = []
    ours = sorted({n for n in outlined if n == UNNAMED or n.startswith(owned_faces())})
    if ours:
        # One is the common case -- a single weight falling back is what a stylesheet
        # edit produces -- so the sentence agrees with the count rather than reading
        # like a template that was never run on the failure it exists for.
        findings.append(
            f"{len(ours)} of the faces this page ships "
            f"{'is' if len(ours) == 1 else 'are'} drawn as Type3 outline "
            f"paths rather than embedded: {', '.join(ours)}. A viewer that smooths "
            "embedded text leaves them thin. Check that `sans_instances` has "
            "written the instances the page asks for and that the print stack "
            "names them."
        )
    unexpected, _ = provenance(pdf)
    if unexpected:
        findings.append(
            f"{len(unexpected)} font families in this file are not the page's: "
            f"{', '.join(unexpected)}. Every text run has to resolve to a face the page "
            "ships, so a family from the reader's machine is a glyph nobody here chose. "
            "Give the characters to a shipped face; or, if a kpress fix is on its way, "
            "add the family to EXPECTED_HOST_FONTS with the bead it waits on; or, if it "
            "is the atlas figure's own label face, to ATLAS_FACES with the bead that "
            "records it."
        )
    return findings


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
    if pages != EXPECTED_PAGE_COUNT:
        raise SystemExit(
            f"explainer PDF has {pages} pages; expected {EXPECTED_PAGE_COUNT}. "
            "A layout change crossed a page boundary."
        )
    embedded = embedded_fonts(first)
    host = sorted(set(outline_fonts(first)))
    fallbacks = ", ".join(host)
    trailer = f"; drawn as outlines from the host's own fonts: {fallbacks}" if host else ""
    print(
        f"explainer PDF check passed: two renders agree, {len(first)} bytes, "
        f"{pages} pages, {len(embedded)} embedded fonts, none of them this page's "
        f"in outline paths{trailer}"
    )
    _, pending = provenance(first)
    for family, bead in sorted(pending.items()):
        print(f"pending: {family} still comes from the host, waiting on {bead}")
    for family, bead in atlas_faces_present(first).items():
        print(
            f"accepted: {family} is the atlas figure's own, drawn by whichever machine "
            f"exported it, and stays; recorded in {bead}"
        )


def fonts() -> None:
    """One render, and what it set its glyphs in. For reading, not for gating."""
    pdf = render_pdf_bytes()
    unexpected, pending = provenance(pdf)
    for name in embedded_fonts(pdf):
        print(f"embedded  {name}")
    for name in sorted(set(outline_fonts(pdf))):
        print(f"outlines  {name}")
    for family, bead in atlas_faces_present(pdf).items():
        print(f"accepted  {family}, the atlas figure's, from the host and recorded in {bead}")
    for family, bead in sorted(pending.items()):
        print(f"pending   {family}, from the host, waiting on {bead}")
    for family in unexpected:
        print(f"unlisted  {family}, from the host and on no bead")
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
