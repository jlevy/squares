"""The four rules that decide which faces the explainer ships, and at what cost.

`tests/test_explainer.py` renders the page and asserts that nothing in it is a
reference outside it. That is the property, and it is the wrong instrument for these
four seams: a page that inlines every face in the distribution passes it, and so does
a page that drops the half of a composite slot the other half depends on. The first
costs 40 KB a face; the second is worse than either alternative, because the reading
face's metric tables would still be installed and KaTeX would lay out digits it is not
drawing -- the exact mismatch the math text face exists to prevent.

So the four are exercised directly, on inputs small enough to read:

- `inline_font_urls` over the four `url()` shapes the distribution actually carries,
  and over the two refusals it owes a build: a face that names a file that is not
  there, and a kept face that still names a source the rewrite did not reach.
- `_font_face_reachable` over both prunes, the KaTeX one and the composite one, in the
  keeping and the dropping direction. The composite's reading-face blocks name no KaTeX
  file at all, so their reachability is their slot partner's, and `KaTeX_Math-BoldItalic`
  is the partner this page cannot reach.
- `katex_js`'s ordering guard, which is what keeps kpress's metric tables from being
  loaded before the bundle they patch.
- `_print_sans_face`, the prune that keeps kpress's static print instances out of the
  page. They are at kpress's weight tokens and this page prints at its own, so they
  would answer nothing while costing 20 KB of base64 a face in every copy served; the
  PDF pass injects this page's own set into the loaded document instead.

One test does read the real static tree, and it is the one that has to: that registering
`print-fonts.css` upstream leaves the rendered page byte for byte where it was. Nothing
else here reads a real font -- `tmp_path` holds two stand-in files of a few bytes -- and
the whole file still runs in well under a second, so it belongs in the quick lane and
carries no marker.
"""

# `_font_face_reachable` and `_print_sans_face` are the prunes, and they are private
# because nothing outside the renderer should decide what a page ships. Testing them
# directly rather than through `katex_css` is what keeps all but one test here off the
# real static tree, and every one of them off a 1.4 MB page.
# pyright: reportPrivateUsage=false
from __future__ import annotations

import base64
import io
import json
import re
from pathlib import Path
from textwrap import dedent

import pytest
from kpress.format import assets as kpress_assets
from nodejs_wheel import node

from devtools import render_explainer
from devtools.render_explainer import (
    FONT_FACE_BLOCK,
    RELATION_FACES,
    RELATION_FAMILIES,
    RELATION_POINTS,
    RELATION_SIZE_ADJUST,
    _composite_slot,
    _declares_nothing,
    _face_family,
    _font_face_reachable,
    _print_sans_face,
    inline_font_urls,
    katex_css,
    katex_js,
    kpress_css,
    kpress_static,
    relation_face_css,
)
from devtools.sans_instances import SCREEN_SANS, print_family

#: kpress's generated print-face stylesheet, registered in `DEFAULT_CSS_ASSETS`.
PRINT_FONTS = "css/print-fonts.css"

#: The second composite, which draws the letters and digits of mathematics from Source
#: Sans wherever the words around them are sans. Its name has the first composite's as a
#: prefix, which is the whole reason the prune and its staleness guard match a family
#: exactly rather than searching for one.
SANS_COMPOSITE = "KPress Math Text Sans"

#: Stand-ins for the two faces the shapes below reference. Any bytes will do: the
#: rewrite reads a file and base64s it, and nothing in this file parses a font.
PROSE_BYTES = b"pt-serif-regular-stand-in"
MATH_BYTES = b"katex-main-regular-stand-in"


def _data_uri(payload: bytes) -> str:
    return f"data:font/woff2;base64,{base64.b64encode(payload).decode()}"


PROSE_URI = _data_uri(PROSE_BYTES)
MATH_URI = _data_uri(MATH_BYTES)


@pytest.fixture
def stylesheet_dir(tmp_path: Path) -> Path:
    """kpress's static tree in miniature, and the directory a stylesheet is served from.

    `katex/` beside `fonts/`, which is the only structure the three relative shapes
    depend on: `../fonts/` climbs to the reading faces, a bare `fonts/` stays inside
    `katex/`, and the composite's `../katex/fonts/` climbs and comes back to the same
    place. Resolving from the stylesheet's own directory is what makes all three work
    without a special case, so the fixture returns that directory rather than the root.
    """
    (tmp_path / "katex" / "fonts").mkdir(parents=True)
    (tmp_path / "katex" / "fonts" / "KaTeX_Main-Regular.woff2").write_bytes(MATH_BYTES)
    (tmp_path / "fonts").mkdir()
    (tmp_path / "fonts" / "pt-serif-latin-400-normal.woff2").write_bytes(PROSE_BYTES)
    return tmp_path / "katex"


def _kpress_block(source: str) -> str:
    """kpress's own shape: pretty-printed, quoted, with a `format()` clause after it."""
    return (
        '@font-face {\n  font-family: "PT Serif";\n  font-style: normal;\n'
        f'  src: url("{source}") format("woff2");\n}}'
    )


def _katex_block(source: str) -> str:
    """KaTeX's, out of the minified bundle: one line, and the bare form is unquoted."""
    return (
        "@font-face{font-display:swap;font-family:KaTeX_Main;font-style:normal;"
        f"font-weight:400;src:url({source})}}"
    )


def _composite_block(source: str) -> str:
    """The composite's Greek half, which reaches sideways out of `katex/` and back in."""
    return (
        '@font-face {\n  font-family: "KPress Math Text";\n  size-adjust: 102.5%;\n'
        f'  src: url("{source}") format("woff2");\n'
        "  unicode-range: U+0391-03A9;\n}"
    )


#: The four `@font-face` shapes the distribution carries, each with what it must become.
#: kpress writes its own pretty-printed with a `format()` clause; the minified KaTeX
#: bundle writes a bare, unquoted, relative `url()`; the composite reaches sideways into
#: `../katex/fonts/`; and a stylesheet inlined once already must survive being inlined
#: again unchanged, since `kpress_css` and `katex_css` both run this over whole files.
FONT_FACE_SHAPES: list[tuple[str, str, str]] = [
    (
        "kpress-quoted-relative",
        _kpress_block("../fonts/pt-serif-latin-400-normal.woff2"),
        _kpress_block(PROSE_URI),
    ),
    (
        "katex-bare-relative",
        _katex_block("fonts/KaTeX_Main-Regular.woff2"),
        _katex_block(f'"{MATH_URI}"'),
    ),
    (
        "composite-sideways",
        _composite_block("../katex/fonts/KaTeX_Main-Regular.woff2"),
        _composite_block(MATH_URI),
    ),
    (
        "already-inlined",
        _kpress_block(PROSE_URI),
        _kpress_block(PROSE_URI),
    ),
]


@pytest.mark.parametrize(
    ("css", "expected"),
    [pytest.param(css, expected, id=name) for name, css, expected in FONT_FACE_SHAPES],
)
def test_every_font_face_shape_becomes_a_data_uri(
    css: str, expected: str, stylesheet_dir: Path
) -> None:
    """Each shape is resolved from the stylesheet's directory, and nothing else moves."""
    assert inline_font_urls(css, stylesheet_dir) == expected


def test_a_face_the_stylesheet_names_but_does_not_ship_fails_the_render(
    stylesheet_dir: Path,
) -> None:
    """An unresolved reference is a build error, not a face left to the reader's machine.

    Falling back would be silent and would look almost right: the page would draw
    mathematics in whatever the reader has, laid out from metrics for a face that never
    arrived.
    """
    css = '@font-face { font-family: "Gone"; src: url("../fonts/gone.woff2"); }'
    with pytest.raises(SystemExit, match="which is not there"):
        inline_font_urls(css, stylesheet_dir)


def test_a_kept_face_that_still_names_a_file_fails_the_render(stylesheet_dir: Path) -> None:
    """The self-containment check covers every source, not only the woff2 ones.

    The rewrite recognises `.woff2`, because that is all the pinned distribution
    carries. A `woff` or `truetype` fallback added upstream would pass straight through
    it and ship as a relative path beside a file that has no such neighbour, so a kept
    block naming any non-`data:` source stops the build instead.
    """
    css = (
        '@font-face { font-family: "PT Serif";\n'
        '  src: url("../fonts/pt-serif-latin-400-normal.woff2") format("woff2"),\n'
        '       url("../fonts/pt-serif-latin-400-normal.woff") format("woff"); }'
    )
    with pytest.raises(SystemExit, match="still fetches"):
        inline_font_urls(css, stylesheet_dir)


def _katex_font_block(face: str) -> str:
    """A KaTeX `@font-face`, judged on the file it names."""
    return (
        f"@font-face{{font-display:swap;font-family:{face.partition('-')[0]};"
        f"font-style:normal;font-weight:400;src:url(fonts/{face}.woff2)}}"
    )


def _composite_slot_block(
    style: str, weight: str, source: str, family: str = "KPress Math Text"
) -> str:
    """A composite slot's reading half, which names no KaTeX file for the prune to read."""
    return (
        f'@font-face {{\n  font-family: "{family}";\n  font-style: {style};\n'
        f"  font-weight: {weight};\n  font-display: swap;\n"
        f'  src: url("../fonts/{source}") format("woff2");\n'
        "  unicode-range: U+0041-005A, U+0061-007A;\n}"
    )


def _sans_composite_greek(style: str, weight: str, face: str) -> str:
    """A sans composite slot's Greek half, which does name a KaTeX file.

    The shape matters to the prune's ORDER: this block names `KaTeX_Main-Bold.woff2`, a
    face the page draws elsewhere, so a rule that read the file before the family would
    keep it while its Source Sans partner was being dropped.
    """
    return (
        f'@font-face {{\n  font-family: "KPress Math Text Sans";\n  font-style: {style};\n'
        f"  font-weight: {weight};\n  font-display: block;\n  size-adjust: 95.2%;\n"
        f'  src: url("../katex/fonts/{face}.woff2") format("woff2");\n'
        "  unicode-range: U+0391-03A9;\n}"
    )


#: The prunes, in both directions. The first two blocks name a KaTeX file and are judged
#: on it; the composite blocks are judged on the family they declare, then on the slot.
REACHABILITY_CASES: list[tuple[str, str, bool]] = [
    ("katex-face-the-page-draws", _katex_font_block("KaTeX_Main-Regular"), True),
    ("katex-face-the-page-cannot-reach", _katex_font_block("KaTeX_Fraktur-Regular"), False),
    (
        "composite-slot-with-a-reachable-partner",
        _composite_slot_block("italic", "400", "pt-serif-latin-400-italic.woff2"),
        True,
    ),
    (
        "composite-slot-whose-partner-is-dropped",
        _composite_slot_block("italic", "700", "pt-serif-latin-700-italic.woff2"),
        False,
    ),
    (
        "sans-slot-the-page-draws",
        _composite_slot_block(
            "italic", "400", "source-sans-3-latin-wght-italic.woff2", SANS_COMPOSITE
        ),
        True,
    ),
    (
        "sans-bold-slot-the-reader-preference-can-reach",
        _composite_slot_block(
            "normal", "650", "source-sans-3-latin-wght-normal.woff2", SANS_COMPOSITE
        ),
        True,
    ),
    (
        "sans-print-instance-under-a-drawn-slot",
        _composite_slot_block(
            "normal", "400", "kpress-print-sans-latin-400-normal.woff2", SANS_COMPOSITE
        ),
        True,
    ),
    (
        "sans-print-instance-under-a-pruned-slot",
        _composite_slot_block(
            "italic", "650", "kpress-print-sans-latin-650-italic.woff2", SANS_COMPOSITE
        ),
        False,
    ),
    (
        "sans-greek-half-of-the-reader-preferences-bold-slot",
        _sans_composite_greek("normal", "650", "KaTeX_Main-Bold"),
        True,
    ),
    (
        "sans-greek-half-of-a-drawn-slot",
        _sans_composite_greek("normal", "400", "KaTeX_Main-Regular"),
        True,
    ),
]


@pytest.mark.parametrize(
    ("block", "reachable"),
    [pytest.param(block, reachable, id=name) for name, block, reachable in REACHABILITY_CASES],
)
def test_only_the_faces_the_page_can_draw_are_kept(block: str, *, reachable: bool) -> None:
    """Both halves of a composite slot are kept or dropped together.

    The serif composite's bold-italic slot is the first case that matters: the page sets
    nothing in bold italic, so `KaTeX_Math-BoldItalic` is outside `KATEX_FACES` and its
    PT Serif partner goes with it. Keeping the reading half alone would be a slot the CSS
    calls one contract, split -- 40 KB shipped for a range whose Greek is gone.

    The sans composite adds a second rule and a third half. Its upright bold slot stays
    because the reader can choose sans prose, while bold italic is still unused. Both
    slots keep or drop their Source Sans half, Greek half, and static print instance
    together.
    """
    assert _font_face_reachable(block) is reachable


def test_reader_sans_preference_keeps_bold_faces_in_both_media() -> None:
    """The emitted CSS must cover the bold D in prose when the reader chooses sans.

    Keeping only the normal 400 face makes CSS synthesize bold while KaTeX uses the
    real 650 metrics. All three pieces must survive: the screen Latin face, Greek, and
    the print instance. The unused italic 650 slot remains pruned.
    """
    css = katex_css(kpress_static())
    faces = [
        block for block in FONT_FACE_BLOCK.findall(css) if _face_family(block) == SANS_COMPOSITE
    ]
    slots = [_composite_slot(block) for block in faces]
    assert slots.count(("normal", "650")) == 3
    assert ("italic", "650") not in slots
    assert "@media print" in css


def test_a_composite_the_renderer_does_not_know_fails_the_render() -> None:
    """A third composite is 20-40 KB a face, inlined unread, and it is refused instead.

    The families are matched exactly for the same reason. `KPress Math Text` is a prefix
    of `KPress Math Text Sans`, and the guard that counted faces by substring saw twenty
    of one composite when the second landed and refused the render before anything could
    say what had actually changed (kpress #57 senior review, K57-R2).
    """
    with pytest.raises(SystemExit, match="does not know how to prune"):
        _font_face_reachable(
            _composite_slot_block(
                "normal", "400", "pt-serif-latin-400-normal.woff2", "KPress Math Text Mono"
            )
        )


def test_a_composite_that_gains_a_slot_upstream_fails_the_render(tmp_path: Path) -> None:
    """The slot tables here are a copy of kpress's, so they are checked against it.

    A slot added upstream would otherwise be inlined unread. The check is per family and
    on the exact name, which is what the substring form got wrong.
    """
    static = tmp_path / "katex"
    static.mkdir(parents=True)
    stylesheet = static / "katex.min.css"
    stylesheet.write_text(
        "\n".join(
            _composite_slot_block(style, weight, "pt-serif-latin-400-normal.woff2")
            for style, weight in (("normal", "400"), ("italic", "400"))
        ),
        encoding="utf-8",
    )
    monkey = pytest.MonkeyPatch()
    monkey.setattr(kpress_assets, "KATEX_CSS_ASSETS", ["katex/katex.min.css"])
    try:
        with pytest.raises(SystemExit, match="declares 2 faces of KPress Math Text"):
            katex_css(tmp_path)
    finally:
        monkey.undo()


#: What kpress's list must not become. The tables patch the bundle's own metrics through
#: `katex.__setFontMetrics`, so a list that loads them first would install them into
#: nothing and leave the page drawing PT Serif from Computer Modern's measurements.
BAD_ASSET_LISTS: list[tuple[str, list[str], str]] = [
    (
        "tables-before-the-bundle",
        [
            "katex/katex-text-metrics.js",
            "katex/katex.min.js",
            "katex/katex-math-runtime.js",
            "katex/katex-init.js",
        ],
        "which cannot be right",
    ),
    (
        "tables-gone",
        ["katex/katex.min.js", "katex/auto-render.min.js", "katex/katex-init.js"],
        "no longer lists",
    ),
]


@pytest.mark.parametrize(
    ("listed", "complaint"),
    [pytest.param(listed, complaint, id=name) for name, listed, complaint in BAD_ASSET_LISTS],
)
def test_the_metric_tables_must_follow_the_bundle_they_patch(
    listed: list[str], complaint: str, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Both refusals fire before a byte is read, so the static tree is not needed."""
    monkeypatch.setattr(kpress_assets, "KATEX_JS_ASSETS", listed)
    with pytest.raises(SystemExit, match=complaint):
        katex_js(tmp_path)


def test_host_context_and_kerning_reach_the_shared_math_renderer() -> None:
    """The host contributes its custom wrappers and TeX spacing to the shared API.

    Figure readouts are custom sans components, while native math wrappers reset the
    font to prose. The context callback must look through those wrappers without
    changing ordinary prose or detached nodes into sans mathematics.
    """
    setup = dedent(r"""
        const assert = require('node:assert/strict');
        const calls = [];
        let finish;
        const sans = {nodeType: 1, parentElement: null, matches: () => false,
          fontFamily: '"Source Sans 3 Variable", sans-serif'};
        const prose = {...sans, fontFamily: '"PT Serif", serif'};
        const wrapper = parent => ({nodeType: 1, parentElement: parent,
          matches: () => true, dataset: {}});
        const nodes = [wrapper(wrapper(sans)), wrapper(prose), wrapper(null)];
        nodes[0].dataset.kpressMathPrepared = 'true';
        const document = {querySelectorAll: () => nodes};
        const getComputedStyle = el => ({fontFamily: el.fontFamily,
          getPropertyValue: () => '"Source Sans 3 Variable", sans-serif'});
        globalThis.kpressMathText = {
          render(source, target, options, context) {
            calls.push({source, display: options.displayMode,
              sans: context.isSansContext(target)});
            if (target === nodes[1]) return new Promise(resolve => { finish = resolve; });
            return Promise.resolve();
          },
          hydrate(source, target, options, context) {
            calls.push({hydrate: true});
            return globalThis.kpressMathText.render(source, target, options, context);
          },
        };
    """)
    exercise = dedent(r"""
        (async () => {
          assert.deepEqual(nodes.map(squaresMath.context.isSansContext), [true, false, false]);
          await squaresMath.render(nodes[0], 's(11) + cos(x)', true);
          const delayed = squaresMath.render(nodes[1], 'n(2)', false);
          assert.equal(nodes[0].dataset.squaresMathReady, 'true');
          assert.equal(nodes[1].dataset.squaresMathReady, undefined,
            'an unrelated pending formula does not hide the completed one');
          let completed = false;
          const settled = squaresMath.settled().then(() => { completed = true; });
          await Promise.resolve();
          assert.equal(completed, false, 'initial readouts are still being rendered');
          finish();
          await delayed;
          await settled;
          assert.equal(completed, true);
          assert.equal(nodes[1].dataset.squaresMathReady, 'true');
          process.stdout.write(JSON.stringify(calls));
        })();
    """)
    completed = node(
        ["-"],
        return_completed_process=True,
        input=setup + render_explainer.host_math_init() + exercise,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout) == [
        {"hydrate": True},
        {"source": r"s\mkern1mu(11) + cos(x)", "display": True, "sans": True},
        {"source": r"n\mkern1mu(2)", "display": False, "sans": False},
    ]


def test_heat_map_waits_for_math_and_cancels_a_hidden_certificates_queued_draw() -> None:
    """Expensive canvas work starts after the required math settles and a paint occurs."""
    source = render_explainer.TEMPLATE.read_text()
    start = source.index("function scheduleHeat() {")
    function = source[start : source.index("\nfunction toWorld(", start)]
    setup = dedent("""
        const assert = require('node:assert/strict');
        let finish, heatQueued = false, heat = null, showHeat = true, hidden = false;
        let draws = 0, builds = 0, settlements = 0;
        const frames = [], tasks = [];
        const pending = new Promise(resolve => { finish = resolve; });
        const squaresMath = {settled: () => { settlements++; return pending; }};
        const pv = {closest: () => ({hidden})};
        const requestAnimationFrame = callback => frames.push(callback);
        const setTimeout = callback => tasks.push(callback);
        const buildHeat = () => { heat = {}; builds++; };
        const drawProver = () => { draws++; };
    """)
    exercise = dedent("""
        (async () => {
          scheduleHeat(); scheduleHeat();
          assert.equal(settlements, 1, 'only one heat-map task may be pending');
          assert.equal(frames.length, 0, 'pending math has not yet reached a paint');
          finish(); await Promise.resolve();
          assert.equal(frames.length, 1);
          assert.equal(builds, 0);
          frames.shift()();
          assert.equal(builds, 0, 'the animation-frame callback still lets a paint through');
          hidden = true; tasks.shift()();
          assert.equal(builds, 0, 'a certificate hidden since scheduling is not drawn');
          hidden = false; scheduleHeat(); await Promise.resolve();
          frames.shift()(); tasks.shift()();
          assert.equal(builds, 1); assert.equal(draws, 1);
          scheduleHeat();
          assert.equal(frames.length, 0, 'a completed heat map is reused');
        })();
    """)
    completed = node(
        ["-"],
        return_completed_process=True,
        input=setup + function + exercise,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr


def _sans_face(family: str, weight: int) -> str:
    """One of kpress's generated print instances, in the shape its generator writes."""
    return (
        f'  @font-face {{\n    font-family: "{family}";\n    font-style: normal;\n'
        f"    font-display: swap;\n    font-weight: {weight};\n"
        f'    src: url("../fonts/kpress-print-sans-latin-{weight}-normal.woff2")'
        ' format("woff2");\n'
        "  }\n"
    )


#: The prune, in both directions. Only the static print family goes: it is the one this
#: page overrides, and it is asked of kpress rather than spelled here, so a rename
#: upstream moves the case with the rule. `Source Sans 3 Variable` is a different family
#: and a different string, and the page's screen face; the rest are what the document is
#: set in.
PRINT_SANS_CASES: list[tuple[str, str, bool]] = [
    ("the static print instance", _sans_face(print_family(), 550), True),
    ("the variable face the screen uses", _sans_face(SCREEN_SANS, 400), False),
    ("the reading face", _kpress_block("../fonts/pt-serif-latin-400-normal.woff2"), False),
    ("the composite", _composite_block("../katex/fonts/KaTeX_Main-Regular.woff2"), False),
    ("a KaTeX face", _katex_block("fonts/KaTeX_Main-Regular.woff2"), False),
]


@pytest.mark.parametrize(
    ("block", "dropped"),
    [pytest.param(block, dropped, id=name) for name, block, dropped in PRINT_SANS_CASES],
)
def test_only_kpress_own_print_instances_are_pruned(block: str, *, dropped: bool) -> None:
    """Judged on the family alone, so the rule survives kpress reshaping the stylesheet.

    The variable face is the case that matters: it is what the screen reads in, and
    dropping it would leave the page with no sans at all. It was also the near miss the
    whole-string comparison was written for -- while the instances were declared under
    `"Source Sans 3"`, `"Source Sans 3 Variable"` shared its first eleven characters.
    kpress's rename put the two families further apart than that; the comparison is
    still whole, because the next family it declares may not be.
    """
    assert _print_sans_face(block) is dropped


#: What a stylesheet is once its faces are gone, and what is not empty. The `@media`
#: wrapper is kpress's: the instances are declared inside one so a screen never fetches
#: them, and pruning the faces out of it leaves the wrapper behind.
EMPTINESS_CASES: list[tuple[str, str, bool]] = [
    ("a comment and an emptied media block", "/* generated */\n\n@media print {\n}\n", True),
    ("nested empty blocks", "@media print {\n  @supports (x: y) {\n  }\n}\n", True),
    ("whitespace", "\n\n  \n", True),
    ("one real rule left in the block", "@media print {\n  body { margin: 0 }\n}\n", False),
    ("a rule outside any block", "/* c */\n:root { --x: 1 }\n", False),
]


@pytest.mark.parametrize(
    ("css", "empty"),
    [pytest.param(css, empty, id=name) for name, css, empty in EMPTINESS_CASES],
)
def test_a_stylesheet_with_nothing_left_in_it_does_not_enter_the_page(
    css: str, *, empty: bool
) -> None:
    """Not even as its own comment marker, which is what keeps the page's bytes still."""
    assert _declares_nothing(css) is empty


def test_registering_the_print_faces_upstream_does_not_move_the_page(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """kpress's print stylesheet arrives, and the served page is byte for byte where it was.

    The one test here that reads the real static tree, because the claim is about that
    tree: twelve faces at kpress's weights, about 250 KB of base64, land in
    `DEFAULT_CSS_ASSETS` and none of it reaches a reader. The PDF pass supplies this
    page's own instances at this page's weights, to the loaded document only.
    """
    static = kpress_static()
    if not (static / PRINT_FONTS).is_file():
        pytest.skip(f"kpress ships no {PRINT_FONTS} at this gitlink")
    listed = [name for name in kpress_assets.DEFAULT_CSS_ASSETS if name != PRINT_FONTS]
    monkeypatch.setattr(kpress_assets, "DEFAULT_CSS_ASSETS", listed)
    without = kpress_css(static)
    monkeypatch.setattr(kpress_assets, "DEFAULT_CSS_ASSETS", [*listed, PRINT_FONTS])
    assert kpress_css(static) == without
    assert f'font-family: "{SCREEN_SANS}"' in without


def test_the_relation_face_joins_the_screen_sans_at_the_sans_weight_range() -> None:
    """The three characters the page sets in a sans run and no text face it ships carries.

    Four properties, and every one of them was a defect before it was a rule.

    The weight range has to match the family's own faces exactly. Blink picks one face per
    family for a weight before it looks at which face has the character; among faces that
    match the weight equally the coverage decides, but a face that matches it better wins
    outright and the search moves on to the next family when it turns out to have no glyph.
    At `100 900` this face beat Source Sans 3's `200 900` at every weight and every upright
    sans run on the page came from the reader's machine.

    One family, and not the print stack's `KPress Print Sans` beside it, which is the same
    lesson from the other side. `render_explainer_pdf` injects this page's static instances
    into that family at 410, 550 and 680; a relation face declared there over `200 900` did
    not lose an exact 410 cleanly, and the sans came back out of the export as Type3
    outline paths with 127 KB on the file. The instances carry kpress's Latin
    `unicode-range`, so they leave these three code points to the next family, which is
    this one.

    The `unicode-range` is what keeps the face to those three characters and out of the way
    of everything else. And the source is inline, because the page is opened from a
    `file://` URL with nothing to fetch from.
    """
    static = kpress_static()
    css = relation_face_css(static)
    assert css.count("@font-face") == len(RELATION_FACES) * len(RELATION_FAMILIES)
    for family in RELATION_FAMILIES:
        assert f'font-family: "{family}";' in css
    assert css.count("font-weight: 200 900;") == len(RELATION_FAMILIES)
    assert css.count("unicode-range: U+2192, U+2248, U+2265;") == len(RELATION_FAMILIES)
    assert css.count(f"size-adjust: {RELATION_SIZE_ADJUST}%;") == len(RELATION_FAMILIES)
    assert css.count('url("data:font/woff2;base64,') == len(RELATION_FAMILIES)
    assert '.woff2")' not in css


def test_a_family_kpress_no_longer_declares_fails_the_render(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`RELATION_FAMILIES` is a copy of kpress's name, so it is checked against kpress.

    The failure it prevents is silent in every other instrument: a renamed family leaves
    `relation_face_css` declaring a face nothing on the page can reach, the render still
    reproduces byte for byte, the assertions above still hold -- they read the emitted
    CSS, which is where the stale name is -- and the three relation characters go back to
    the reader's own machine. kpress has renamed a sans family here once already.

    A synthetic stylesheet rather than kpress's, because the rename is the input: the
    same two lines with one name changed are the before and the after.
    """
    static = kpress_static()

    def kpress_declares(names: tuple[str, ...]) -> None:
        css = "\n".join(
            f'@font-face {{ font-family: "{name}"; src: url("sans.woff2"); }}' for name in names
        )

        def stylesheet(_static: Path, text: str = css) -> str:
            return text

        monkeypatch.setattr(render_explainer, "kpress_css", stylesheet)

    kpress_declares(RELATION_FAMILIES)
    faces = relation_face_css(static).count("@font-face")
    assert faces == len(RELATION_FACES) * len(RELATION_FAMILIES)

    kpress_declares(tuple(f"{name} Next" for name in RELATION_FAMILIES))
    with pytest.raises(SystemExit, match="RELATION_FAMILIES is stale"):
        relation_face_css(static)


def test_the_relation_subset_carries_the_three_glyphs_and_its_own_name() -> None:
    """A few hundred bytes of the 26 KB face, and it has to still say what face it is.

    The name table stays for a reason that cost a render to find: Chromium's font
    sanitiser renames a face with no name table to `OTS-derived-font`, the PDF embeds it
    under that name, and the provenance guard cannot tell it from a face off the reader's
    machine. The hinting programs are what goes instead -- 1.8 KB of the 2.5 KB a hinted
    three-glyph subset weighs, written for a whole face rather than for these three.
    """
    from fontTools.ttLib import TTFont  # noqa: PLC0415

    css = relation_face_css(kpress_static())
    encoded = re.search(r'base64,([A-Za-z0-9+/=]+)"', css)
    assert encoded is not None
    face = TTFont(io.BytesIO(base64.b64decode(encoded.group(1))))
    assert set(RELATION_POINTS) <= set(face.getBestCmap() or {})
    assert "KaTeX_Main-Bold" in (face["name"].getDebugName(6) or "")
    assert not {"fpgm", "prep", "cvt "} & set(face.keys())
    assert len(base64.b64decode(encoded.group(1))) < 2000


def test_the_shared_math_runtime_is_embedded_without_rewriting_its_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Runtime changes upstream reach the host without another JavaScript implementation."""
    scripts = {
        "katex/katex.min.js": "/* vendor bundle */",
        "katex/katex-text-metrics.js": "/* profile tables */",
        "katex/katex-math-runtime.js": (
            "/* shared runtime */\nconst changedShape = {\n  ready: true,\n};"
        ),
        "katex/katex-init.js": "/* native auto-render loop */",
    }
    monkeypatch.setattr(kpress_assets, "KATEX_JS_ASSETS", list(scripts))
    for name, source in scripts.items():
        asset = tmp_path / name
        asset.parent.mkdir(exist_ok=True)
        asset.write_text(source, encoding="utf-8")
    assert katex_js(tmp_path) == "\n".join(
        [*list(scripts.values())[:-1], render_explainer.host_math_init()]
    )
