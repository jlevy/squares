#!/usr/bin/env python3
"""Instance Source Sans 3 at the weights this page prints at, so the PDF embeds a font.

Chromium's PDF writer embeds a variable font only at its default position. Every glyph
of Source Sans 3 Variable away from it is therefore written as a Type3 outline path
instead: five such fonts in the explainer PDF, against the Type0 subsets PT Serif and
the KaTeX faces get. The outlines carry the right weight, so the file is not wrong. It
reads wrong. Preview smooths text it draws through the font machinery -- 5 to 20 percent
more ink at 2 to 3 pixels per point -- and leaves outline paths alone, so the captions,
footnotes, hero and footer come out a step lighter than the serif and the mathematics
beside them. Measured on 2026-09-07: the export was 979,521 bytes with the sans in
outlines and 793,873 with it in fonts.

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
page under `media: print` at the printed column width, walks every text run, and records
the computed weight and style wherever the family stack starts with the sans. One request
is answered without an instance of its own, and it is 400: the `@page` margin-box footer
inherits it. It is not reachable any other way -- a margin box is not in the document
tree, so no probe can see it -- and CSS font matching sends a request in [400, 500]
ascending before descending, so it lands on the 410 instance, ten units away and below
what shows at 11pt.

`--weights` is the audit beside the gate. It lists every family, weight and style the
page draws in, under both media, with the run count, a few of the elements that ask, and
the declaration behind each -- read out of the cascade through CDP rather than out of
`getComputedStyle`, which resolves a token to a number before any script can see which
token it was. It is how a fourth sans weight is found: two were, on 2026-09-07, the
caption label at the medium where the title credits were bold, and kpress's literal 600
on the footnote controls.

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python -m devtools.sans_instances
    uv run --frozen --all-extras --group dev python -m devtools.sans_instances --check
    uv run --frozen --all-extras --group dev python -m devtools.sans_instances --weights
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
from collections.abc import Callable, Iterable, Mapping, Sequence
from functools import cache
from pathlib import Path
from typing import NotRequired, Protocol, TypedDict, cast

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
#: answer. One weight per role and no others: the paper profile's own three tokens,
#: light 410, medium 550 and bold 680, declared in `explainer-shell.html`. kpress's own
#: instances are at kpress's tokens -- 370, 400, 550, 600, 650, 700 -- a different set
#: for a different document, which is why this page instances its own.
#:
#: 600 was here until 2026-09-07, for kpress's literal on the footnote controls, which
#: the profile now maps to its medium: a fourth weight on this page's sans, two instanced
#: faces in the PDF, for thirty superscript figures and the arrows back from the sources.
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
    (680, "normal"),
    (680, "italic"),
)

#: The one request answered by a face that is not an exact match, and where it lands.
#: CSS Fonts 4 searches a desired weight in [400, 500] upward to 500 before it looks
#: down, so 400 takes the 410 instance rather than falling to 550. Ten units is under a
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

#: What the page asks for, taken from the page rather than read out of the stylesheet.
#: A run is counted when the first family in its computed stack is one of the two sans
#: names the probe is handed: the print family kpress declares its instances under, and
#: `SCREEN_SANS`. Runs the print stylesheet hides are skipped -- a `display: none` block
#: still reports a computed weight, and counting it would declare an instance for text
#: no reader ever sees.
_PROBE = r"""(families) => {
  const sans = new Set(families);
  const found = new Map();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let node = walker.nextNode(); node; node = walker.nextNode()) {
    if (!node.nodeValue || !node.nodeValue.trim()) continue;
    const el = node.parentElement;
    if (!el || !el.getClientRects().length) continue;
    const style = getComputedStyle(el);
    const family = style.fontFamily.split(',')[0].trim().replace(/^["']|["']$/g, '');
    if (!sans.has(family)) continue;
    const weight = parseInt(style.fontWeight, 10);
    const key = `${weight}/${style.fontStyle}`;
    if (!found.has(key)) {
      found.set(key, {weight, style: style.fontStyle, path: sig(el)});
    }
  }
  return [...found.values()].sort((a, b) =>
    a.weight - b.weight || a.style.localeCompare(b.style));
  {{SIG}}
}"""

#: A name for an element that is readable in a failure: the tag, its classes, and its
#: index among its siblings, up to the page wrapper. The same shape `check_print_layout`
#: reports its findings with, so two print findings about one element read alike.
#: Spliced into both probes here rather than written twice, so a path in the listing and
#: a path in a `--check` failure name the same element the same way.
_SIG = r"""
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
  }"""

#: Every distinct family, weight and style the page draws text in, with a run count and
#: the first few elements that ask for it, each stamped with a marker the matched-rule
#: walk finds it by. Not scoped to the sans: the question the listing answers is whether
#: one bold and one medium serve the whole design system, and the serif's own bold is
#: part of that answer. Hidden runs are skipped for the reason `_PROBE` skips them -- a
#: weight nobody sees is not a weight the design has to reconcile.
#:
#: Several elements per combination, not one, because one is the wrong number for the
#: question. `.doc-links .chip` and the caption's label are both the sans at 550, and a
#: listing that reported the first would say the medium had one source when it had two.
#: The markers are cleared first: the same page is probed under both media, and a marker
#: the screen pass left behind would be found instead of the element the print pass just
#: stamped, since `DOM.querySelector` answers with the first match in document order.
_WEIGHTS_PROBE = r"""({attribute, samples}) => {
  for (const stale of document.querySelectorAll(`[${attribute}]`))
    stale.removeAttribute(attribute);
  const found = new Map();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let next = 0;
  for (let node = walker.nextNode(); node; node = walker.nextNode()) {
    if (!node.nodeValue || !node.nodeValue.trim()) continue;
    const el = node.parentElement;
    if (!el || !el.getClientRects().length) continue;
    const style = getComputedStyle(el);
    const family = style.fontFamily.split(',')[0].trim().replace(/^["']|["']$/g, '');
    const weight = parseInt(style.fontWeight, 10);
    const key = `${family}/${weight}/${style.fontStyle}`;
    if (!found.has(key))
      found.set(key, {family, weight, style: style.fontStyle, runs: 0, seen: []});
    const row = found.get(key);
    row.runs++;
    if (row.seen.length < samples && !el.hasAttribute(attribute)) {
      el.setAttribute(attribute, String(next));
      row.seen.push({marker: next, path: sig(el)});
      next++;
    }
  }
  return [...found.values()].sort((a, b) =>
    a.family.localeCompare(b.family) || a.weight - b.weight
    || a.style.localeCompare(b.style));
  {{SIG}}
}"""


def _spliced(probe_source: str) -> str:
    """One probe with the shared element-path helper in it."""
    return probe_source.replace("{{SIG}}", _SIG)


_PROBE = _spliced(_PROBE)
_WEIGHTS_PROBE = _spliced(_WEIGHTS_PROBE)


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
            rows: list[Requested] = page.evaluate(_PROBE, [print_family(), SCREEN_SANS])
            return rows
        finally:
            browser.close()


class Sampled(TypedDict):
    """One element that asks for a combination, and the declaration that gave it one."""

    #: The attribute value the probe stamped on the element, so the matched-rule walk
    #: can find the node again through CDP's own `DOM.querySelector`.
    marker: int
    path: str
    #: The declaration that won, as `selector { value }`, with `inherited` appended when
    #: it came from an ancestor. `unset` when no rule names a weight at all. Written by
    #: `_attributed`; the probe cannot see it, which is the whole reason CDP is here.
    source: NotRequired[str]


class Declared(TypedDict):
    """One family, weight and style the page draws in, and what asked for it."""

    family: str
    weight: int
    style: str
    runs: int
    seen: list[Sampled]


#: The attribute `_WEIGHTS_PROBE` stamps and the matched-rule walk selects on. A `data-`
#: name, so it is inert; the page it is written into is a fresh load that is thrown away.
MARKER = "data-weight-probe"

#: How many elements per combination are stamped and attributed. Enough to show that one
#: weight has two sources, short enough that a table stays a table; the run count beside
#: it says how much of the page a combination covers, so the samples do not have to.
SAMPLES = 6

#: How much of a selector the listing shows. kpress's own selectors run past 200
#: characters (the `:not()` chain guarding the math text face is one), and a table whose
#: rows wrap three times is not a table.
SELECTOR_WIDTH = 58


def _weight_declarations(node_styles: Mapping[str, object]) -> list[tuple[str, str]]:
    """Every `font-weight` a node's own cascade sets, weakest origin first.

    The order is the cascade's: the presentation attribute an SVG label carries, then
    the matched rules, which CDP already returns by ascending specificity, then the
    inline style. So the last entry is the one that won. Disabled declarations are the
    ones a rule lost on `!important` or on shorthand expansion, and they are dropped
    rather than counted; CDP repeats the winner with `disabled` unset, which is why
    consecutive duplicates collapse.
    """
    found: list[tuple[str, str]] = []

    def collect(selector: str, style: object) -> None:
        if not isinstance(style, dict):
            return
        properties = style.get("cssProperties")
        if not isinstance(properties, list):
            return
        for entry in properties:
            if not isinstance(entry, dict) or entry.get("name") != "font-weight":
                continue
            if entry.get("disabled") is True:
                continue
            pair = (selector, str(entry.get("value", "")))
            if not found or found[-1] != pair:
                found.append(pair)

    collect("<presentation attribute>", node_styles.get("attributesStyle"))
    matched = node_styles.get("matchedCSSRules")
    if isinstance(matched, list):
        for match in matched:
            rule = match.get("rule") if isinstance(match, dict) else None
            if not isinstance(rule, dict):
                continue
            selectors = rule.get("selectorList")
            text = selectors.get("text") if isinstance(selectors, dict) else None
            collect(str(text) if text else "<rule>", rule.get("style"))
    collect("<inline style>", node_styles.get("inlineStyle"))
    return found


def _attribution(node_styles: Mapping[str, object]) -> str:
    """Where one element's weight came from, as a line a reader can act on.

    The element's own cascade first; failing that the nearest ancestor that names a
    weight, because `font-weight` inherits and most of this page's text is set by a
    token on a wrapper rather than on the run itself.
    """
    own = _weight_declarations(node_styles)
    if own:
        selector, value = own[-1]
        return f"{selector[:SELECTOR_WIDTH]} {{ {value} }}"
    inherited = node_styles.get("inherited")
    if isinstance(inherited, list):
        for level in inherited:
            if not isinstance(level, dict):
                continue
            from_ancestor = _weight_declarations(level)
            if from_ancestor:
                selector, value = from_ancestor[-1]
                return f"{selector[:SELECTOR_WIDTH]} {{ {value} }}  (inherited)"
    return "unset (the initial 400)"


def _attributed(page: object, rows: list[Declared]) -> list[Declared]:
    """Fill in each row's `source` by asking the browser which rules matched.

    `CSS.getMatchedStylesForNode` is the only way to see the declaration behind a
    computed weight: `getComputedStyle` resolves `var()` before anything can read it, so
    a page that sets every weight through a token and a page that writes 550 nine times
    look identical from script. The listing exists to tell those two apart.
    """
    from playwright.sync_api import Page  # noqa: PLC0415

    assert isinstance(page, Page)
    session = page.context.new_cdp_session(page)
    try:
        session.send("DOM.enable")
        session.send("CSS.enable")
        document = session.send("DOM.getDocument", {"depth": -1})
        root = int(document["root"]["nodeId"])
        for row in rows:
            for sample in row["seen"]:
                found = session.send(
                    "DOM.querySelector",
                    {"nodeId": root, "selector": f'[{MARKER}="{sample["marker"]}"]'},
                )
                node = int(found.get("nodeId") or 0)
                if not node:  # pragma: no cover - the probe stamped it a moment ago
                    sample["source"] = "the element could not be found again"
                    continue
                sample["source"] = _attribution(
                    session.send("CSS.getMatchedStylesForNode", {"nodeId": node})
                )
    finally:
        session.detach()
    return rows


def distinct_sources(row: Declared) -> list[Sampled]:
    """The sampled elements of one combination, one per declaration that produced it.

    Two elements set from the same rule say the same thing twice; two elements at one
    weight from two different rules are the finding the listing exists to surface.
    """
    kept: list[Sampled] = []
    for sample in row["seen"]:
        if sample.get("source") not in {other.get("source") for other in kept}:
            kept.append(sample)
    return kept


def weights(page_path: Path) -> dict[str, list[Declared]]:
    """Every family, weight and style the page draws in, per medium, with its source.

    Both media from one load, screen first, because switching to print is one call and
    reloading is fifteen seconds. What that costs is one line inside `_WEIGHTS_PROBE`,
    which clears its own markers before each pass for the reason recorded there: the
    numbering restarts at 0 every medium, so a marker the screen pass left behind is
    what `DOM.querySelector` answers with, being earlier in document order.
    """
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    from devtools.check_print_layout import PRINT_VIEWPORT  # noqa: PLC0415

    listed: dict[str, list[Declared]] = {}
    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        try:
            page = browser.new_page()
            page.emulate_media(reduced_motion="reduce")
            page.goto(page_path.resolve().as_uri(), wait_until="load")
            page.wait_for_selector(READY, timeout=60_000)
            for medium in ("screen", "print"):
                if medium == "print":
                    page.emulate_media(media="print")
                    page.set_viewport_size(PRINT_VIEWPORT)
                page.evaluate("document.fonts.ready")
                rows: list[Declared] = page.evaluate(
                    _WEIGHTS_PROBE, {"attribute": MARKER, "samples": SAMPLES}
                )
                listed[medium] = _attributed(page, rows)
            return listed
        finally:
            browser.close()


def list_weights(page_path: Path) -> int:
    """Print the weight table, one block per medium. For reading, not for gating."""
    for medium, rows in weights(page_path).items():
        print(f"\n{medium}: {len(rows)} distinct family, weight and style combinations")
        print(f"  {'weight':>6} {'style':<7} {'runs':>5}  family / set by / one element")
        for row in rows:
            print(f"  {row['weight']:>6} {row['style']:<7} {row['runs']:>5}  {row['family']}")
            for sample in distinct_sources(row):
                print(f"  {'':>21}   {sample.get('source', '(not attributed)')}")
                print(f"  {'':>21}     {sample['path']}")
    return 0


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
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        help="verify the instances and the weights the page asks for, instead of writing",
    )
    mode.add_argument(
        "--weights",
        action="store_true",
        help="list every family, weight and style the page draws in, and what set it",
    )
    parser.add_argument("--page", type=Path, default=PAGE, help="the rendered page to probe")
    arguments = parser.parse_args(argv)
    if not arguments.check and not arguments.weights:
        return write()
    if not arguments.page.is_file():
        raise SystemExit(f"{arguments.page}: no rendered page; run `render_explainer` first")
    if arguments.weights:
        return list_weights(arguments.page)
    return check(arguments.page)


if __name__ == "__main__":
    sys.exit(main())
