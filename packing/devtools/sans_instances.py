#!/usr/bin/env python3
"""Instance Source Sans 3 at the weights this page prints at, so the PDF embeds a font.

Chromium's PDF writer embeds a variable font only at its default position. Every glyph
of Source Sans 3 Variable away from it is therefore written as a Type3 outline path
instead: five such fonts in the explainer PDF, against the Type0 subsets PT Serif and
the KaTeX faces get. The outlines carry the right weight, so the file is not wrong. It
reads wrong. Preview smooths text it draws through the font machinery -- 5 to 20 percent
more ink at 2 to 3 pixels per point -- and leaves outline paths alone, so the captions,
footnotes, hero and footer come out a step lighter than the serif and the mathematics
beside them.

One pair of numbers, taken as one measurement: the same page, in one browser, at one
moment, with the instances injected and with them suppressed. At this branch's head, on
macOS with Playwright's pinned headless shell, the export is 1,024,108 bytes with the
sans in outlines and 830,153 with it in fonts, 17 pages either way, and the five
`SourceSans3-*` outline fonts drop out. Absolute figures from two hosts do not
subtract -- the bytes follow the Chromium build and the fonts the machine has -- which
is why the before and the after are always rendered together rather than quoted from
different days.

A static instance embeds like any other font. This tool writes one per face the print
pass asks for, into `templates/fonts/`, and hands them to `render_explainer_pdf` as
`@font-face` rules with the bytes inline (`print_face_css`). They are injected into the
loaded page immediately before it is printed, so the screen keeps the variable font and
the served `site/index.html` does not gain a byte. The instancer itself is kpress's
(`vendor/kpress/devtools/instance_sans.py`), loaded from the submodule by path: kpress
ships instances at its own weight tokens, and this page overrides them, which is the
case that file is written to serve.

The family those instances declare is kpress's too, and it is read off the loaded
module (`print_family`) rather than written down here. The instances are a modified
Source Sans 3, whose OFL reserves the name "Source", so kpress gives them a family of
their own; a second copy of that string in this repository is a rename away from
naming a family nothing declares, and the two would drift without a word of warning.

`PRINT_FACES` is the declared set, and `--check` holds it to what the page actually
requests rather than to what the stylesheet appears to say. The probe loads the rendered
page under `media: print` at the printed column width and records the computed weight
and style wherever the family stack starts with the sans. It reads two things, not one:
every text run, and the generated content of `::before`, `::after` and `::marker` on
every element with a box. The second half is not a precaution -- kpress numbers footnote
items with `li.kpress-footnote-item::before`, which is a real sans run this page prints
and which no tree walk reaches, so a walk over text alone would have let a weight
nothing instances back into the PDF as outlines.

What is left outside is the `@page` margin box, and it is outside by construction: a
margin box is not in the document tree, so no probe reaches it. `render_explainer_pdf`
covers that side instead, by loading the families the margin boxes name before it
prints. Two requests are answered without an instance of their own and both are 400:
`.rel` names it for the one fallback relation glyph, and the margin-box footer inherits
it. CSS font matching sends a request in [400, 500] ascending before descending, so
both land on the 410 instance, ten units away and below what shows at 11pt.

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python -m devtools.sans_instances
    uv run --frozen --all-extras --group dev python -m devtools.sans_instances --check
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
from collections.abc import Callable, Iterable, Sequence
from functools import cache
from pathlib import Path
from typing import Protocol, TypedDict, cast

from devtools.render_explainer import data_uri, kpress_static
from devtools.render_explainer_pdf import BROWSER_OVERRIDE, PAGE, READY

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent

#: Where the instances live: beside the template they are printed with, since they are
#: an input to this page's PDF and to nothing else. Generated files, not sources.
FONTS = PACKING / "devtools" / "templates" / "fonts"

#: kpress's instancer, in the submodule's `devtools/`, which is repository content
#: rather than part of the installed distribution -- so it is reached by path and not
#: by an import. The file is written to be loadable that way, with fontTools, already
#: pinned in this project's dev group, as its only dependency.
GENERATOR = REPO / "vendor" / "kpress" / "devtools" / "instance_sans.py"

#: A weight and a style, as CSS asks for them.
type Face = tuple[int, str]

#: The faces this page prints in, and `--check` refuses any request the set does not
#: answer. Three of the weights are the paper profile's own tokens
#: (`explainer-shell.html`: light 410, medium 550, bold 680); 600 is kpress's, on the
#: footnote reference control, which the profile does not override. kpress's own
#: instances are at kpress's tokens -- 370, 400, 550, 600, 650, 700 -- a different set
#: for a different document, which is why this page instances its own.
#:
#: Both styles of each, though the probe finds a request only for 410 italic: `font-style`
#: inherits, so any of these weights becomes italic the moment a word inside it is
#: emphasised, and a missing instance would put that run back on the variable font and
#: back into outlines. An instance nothing asks for costs 15 KB on disk and nothing in
#: the PDF, since a declared face that draws no glyph is not embedded.
PRINT_FACES: tuple[Face, ...] = (
    (410, "normal"),
    (410, "italic"),
    (550, "normal"),
    (550, "italic"),
    (600, "normal"),
    (600, "italic"),
    (680, "normal"),
    (680, "italic"),
)

#: The one request answered by a face that is not an exact match, and where it lands.
#: CSS Fonts 4 searches a desired weight in [400, 500] upward to 500 before it looks
#: down, so 400 takes the 410 instance rather than falling to 680. Ten units is under a
#: fifth of the gap to the next token and does not show at the size these run at.
SUBSTITUTED: dict[int, int] = {400: 410}


class Generator(Protocol):
    """The part of kpress's `instance_sans` this tool uses, so the loaded module has one.

    Declared as attributes rather than as methods because a module's functions are
    plain attributes. `generator` casts the loaded module to this, and nothing else in
    the file touches it untyped.
    """

    FAMILY: str
    instance_face: Callable[[Path, int], bytes]
    instance_name: Callable[[int, str], str]
    variable_face: Callable[[str, Path], Path]
    face_rule: Callable[[int, str, str], str]


@cache
def generator() -> Generator:
    """kpress's instancer, loaded from the submodule by path.

    Cached because loading it costs a module execution and every entry point here wants
    it. A missing file is a submodule that is not checked out at a commit carrying the
    generator, and it is said that way rather than as an import error.
    """
    if not GENERATOR.is_file():
        raise SystemExit(
            f"{GENERATOR.relative_to(REPO)} is missing; check out the kpress submodule "
            "at a commit that carries the instance generator"
        )
    spec = importlib.util.spec_from_file_location("kpress_instance_sans", GENERATOR)
    if spec is None or spec.loader is None:  # pragma: no cover - a stdlib failure
        raise SystemExit(f"{GENERATOR}: cannot be loaded as a module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return cast(Generator, module)


def print_family() -> str:
    """The family the instances declare, taken from the generator that writes them.

    Every consumer here asks for it through this function -- the probe that recognises
    the print stack, the prune in `render_explainer` that keeps kpress's own copies out
    of the served page, the PostScript prefix `render_explainer_pdf` scans the PDF for.
    One string, in kpress, where the faces are named; a literal on this side would be a
    second definition of the same thing and would survive the rename that moved it.
    """
    return generator().FAMILY


def postscript_prefix() -> str:
    """The PostScript name every instance's name table starts with.

    kpress builds it from the family by dropping the spaces -- `KPressPrintSans-410` --
    and Chromium writes the same name into the PDF, behind a subset tag. So the prefix
    is derived the same way rather than spelled out, and follows the family by itself.
    """
    return print_family().replace(" ", "")


class Requested(TypedDict):
    """One sans face the page asks for under print, and an element that asks for it."""

    weight: int
    style: str
    path: str


def covered(weight: int, style: str, faces: Sequence[Face] = PRINT_FACES) -> bool:
    """Whether the set draws this request at the weight it asked for.

    Exact, or through `SUBSTITUTED`, which is the 400 case and its reason. Anything
    else is a request the page makes and the PDF cannot honour: the browser would fall
    back to the variable font for it, and that run would be Type3 again.
    """
    if (weight, style) in faces:
        return True
    stand_in = SUBSTITUTED.get(weight)
    return stand_in is not None and (stand_in, style) in faces


def gaps(
    requested: Iterable[Requested], faces: Sequence[Face] = PRINT_FACES
) -> list[Requested]:
    """Every request the set does not answer, each with an element that makes it."""
    return [row for row in requested if not covered(row["weight"], row["style"], faces)]


#: The screen's sans, which is the variable face kpress's print stack now puts the
#: static family ahead of. Still in the probe's set beside it: a run whose computed
#: stack leads with this one under print is a run the injected instances do not reach,
#: and it has to be counted for `--check` to say so rather than pass in silence.
SCREEN_SANS = "Source Sans 3 Variable"

#: The pseudo-elements that can put type on the page without a text node behind it.
#: Passed in rather than written into the probe so the set is visible from Python and
#: the test that runs the shipped rule can name the same three.
PSEUDO_ELEMENTS: tuple[str, ...] = ("::before", "::after", "::marker")

#: What the page asks for, taken from the page rather than read out of the stylesheet.
#: A run is counted when the first family in its computed stack is one of the two sans
#: names the probe is handed: the print family kpress declares its instances under, and
#: `SCREEN_SANS`. Runs the print stylesheet hides are skipped -- a `display: none` block
#: still reports a computed weight, and counting it would declare an instance for text
#: no reader ever sees.
#:
#: Two passes, because a tree walk sees only half the type. Text nodes are the first;
#: generated content is the second, and it is not hypothetical here -- kpress numbers
#: footnote items with `li.kpress-footnote-item::before`, a real sans run in no text
#: node on the page.
_PROBE = r"""([families, pseudos]) => {
  const sans = new Set(families);
  const found = new Map();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let node = walker.nextNode(); node; node = walker.nextNode()) {
    if (!node.nodeValue || !node.nodeValue.trim()) continue;
    const el = node.parentElement;
    if (!el || !el.getClientRects().length) continue;
    record(getComputedStyle(el), sig(el));
  }
  for (const el of document.body.querySelectorAll('*')) {
    if (!el.getClientRects().length) continue;
    for (const pseudo of pseudos) {
      const style = getComputedStyle(el, pseudo);
      if (!draws(style.content)) continue;
      record(style, sig(el) + pseudo);
    }
  }
  return [...found.values()].sort((a, b) =>
    a.weight - b.weight || a.style.localeCompare(b.style));

  /* Whether a computed `content` puts glyphs on the page. `none` is no pseudo-element
     at all and `normal` is the default -- which for `::marker` is a bullet drawn in the
     list item's own font, already counted through its text. An empty string is a box
     with no type in it: a rule, a spacer, a clearfix. None of the four asks for a face. */
  function draws(content) {
    return Boolean(content) && !['none', 'normal', '""', "''"].includes(content);
  }

  /* One request, recorded once per weight and style. The first element to ask for a
     pair is the one a failure names, and the text pass runs first, so a run a reader
     can point at is preferred over generated content that says the same thing. */
  function record(style, path) {
    const family = style.fontFamily.split(',')[0].trim().replace(/^["']|["']$/g, '');
    if (!sans.has(family)) return;
    const weight = parseInt(style.fontWeight, 10);
    const key = `${weight}/${style.fontStyle}`;
    if (!found.has(key)) {
      found.set(key, {weight, style: style.fontStyle, path});
    }
  }

  /* A name for an element that is readable in a failure: the tag, its classes, and its
     index among its siblings, up to the page wrapper. The same shape `check_print_layout`
     reports its findings with, so two print findings about one element read alike. */
  function sig(el) {
    const steps = [];
    for (let node = el, depth = 0; node && depth < 3; node = node.parentElement, depth++) {
      const parent = node.parentElement;
      const nth = parent ? [...parent.children].indexOf(node) : 0;
      const cls = [...node.classList].join('.');
      steps.unshift(`${node.tagName.toLowerCase()}${cls ? '.' + cls : ''}[${nth}]`);
      if (node.classList.contains('kpress')) break;
    }
    return steps.join(' > ');
  }
}"""


def probe(page_path: Path) -> list[Requested]:
    """Every sans face the rendered page requests under print, from one browser load.

    The waiting and the viewport are the print checks' beside this one, deliberately:
    a set measured on a differently settled page, or at the screen's column, is a set
    for a document nobody prints.
    """
    # Deferred, both of them: `check_print_layout` imports playwright at module scope
    # and imports `render_explainer_pdf`, which reaches this module when it prints, so
    # importing either up here would put playwright behind every unit test that reads
    # the coverage rule.
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    from devtools.check_print_layout import PRINT_VIEWPORT  # noqa: PLC0415

    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        try:
            page = browser.new_page()
            page.emulate_media(media="print", reduced_motion="reduce")
            page.goto(page_path.resolve().as_uri(), wait_until="load")
            page.wait_for_selector(READY, timeout=60_000)
            page.set_viewport_size(PRINT_VIEWPORT)
            page.evaluate("document.fonts.ready")
            rows: list[Requested] = page.evaluate(
                _PROBE, [[print_family(), SCREEN_SANS], list(PSEUDO_ELEMENTS)]
            )
            return rows
        finally:
            browser.close()


def print_face_css(faces: Sequence[Face] = PRINT_FACES, fonts: Path = FONTS) -> str:
    """The instances as one `@media print` block, with every face's bytes inline.

    Injected into the loaded page rather than written into it: the PDF is the only
    artifact that needs a static instance, and the served page keeps the variable font
    it has always had, at the size it has always had.
    """
    generate = generator()
    rules: list[str] = []
    for weight, style in faces:
        face = fonts / generate.instance_name(weight, style)
        if not face.is_file():
            raise SystemExit(f"{face.name} is missing; run `python -m devtools.sans_instances`")
        rules.append(generate.face_rule(weight, style, data_uri(face)))
    return "@media print {\n" + "\n".join(rules) + "}\n"


def expected() -> dict[Path, bytes]:
    """Every instance with the bytes it should hold, built from the vendored variables."""
    generate = generator()
    sources = kpress_static() / "fonts"
    built: dict[Path, bytes] = {}
    for weight, style in PRINT_FACES:
        variable = generate.variable_face(style, sources)
        if not variable.is_file():
            raise SystemExit(f"{variable} is missing; kpress ships no {style} variable face")
        built[FONTS / generate.instance_name(weight, style)] = generate.instance_face(
            variable, weight
        )
    return built


def write() -> int:
    FONTS.mkdir(parents=True, exist_ok=True)
    for path, data in expected().items():
        path.write_bytes(data)
        print(f"wrote {path.relative_to(PACKING)} ({len(data):,} bytes)")
    return 0


def check(page_path: Path) -> int:
    """The instances against their inputs, then the declared set against the page.

    Two failures, and they are different failures. Stale bytes mean the vendored
    variable faces or the fontTools pin moved and the shipped instances no longer come
    from them. An uncovered request means the page asks for a weight nothing here
    draws, which the PDF would answer with the variable font and Type3 outlines: the
    defect this whole tool exists to remove, quietly reintroduced by one stylesheet
    edit.
    """
    stale = [
        path.relative_to(PACKING)
        for path, data in expected().items()
        if not path.is_file() or path.read_bytes() != data
    ]
    if stale:
        for path in stale:
            print(f"stale: {path}", file=sys.stderr)
        print("regenerate with `python -m devtools.sans_instances`", file=sys.stderr)
        return 1

    requested = probe(page_path)
    print(f"the page requests {len(requested)} sans faces under print:")
    for row in requested:
        print(f"  {row['weight']:>3} {row['style']:<7} {row['path']}")
    missing = gaps(requested)
    for row in missing:
        print(
            f"no instance draws {row['weight']} {row['style']}, which {row['path']} asks for",
            file=sys.stderr,
        )
    if missing:
        print(
            "add the face to PRINT_FACES and regenerate, or take the request out of "
            "the page's stylesheet",
            file=sys.stderr,
        )
        return 1
    print(f"print sans instances current: {len(PRINT_FACES)} faces cover every request")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the instances and the weights the page asks for, instead of writing",
    )
    parser.add_argument("--page", type=Path, default=PAGE, help="the rendered page to probe")
    arguments = parser.parse_args(argv)
    if not arguments.check:
        return write()
    if not arguments.page.is_file():
        raise SystemExit(f"{arguments.page}: no rendered page; run `render_explainer` first")
    return check(arguments.page)


if __name__ == "__main__":
    sys.exit(main())
