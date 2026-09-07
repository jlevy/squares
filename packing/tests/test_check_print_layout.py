"""`findings` reports what it is for, on measurements built to trip each check.

The checker's own value is that it fails. It shipped once with the `--all` gate above the
marker, footnote and overflow checks instead of below them, so a default run -- which is
the run CI makes -- evaluated only the `.centred` declaration and reported a clean layout
for a document nobody had measured. It read "print layout clean" while doing a third of
its job, which is the failure mode a check that has only ever passed cannot distinguish
itself from.

So each check is exercised here against a measurement built to trip it, and against one
built not to. The first-line probe and the overflow culprit scan also run in Node against
retained browser rectangle measurements, so the grouping in the one and the exclusions in
the other are tested without requiring a browser installation. Only the browser can
establish that the retained rectangles are still what the page lays out, and
`check_print_layout --self-check` is where that is asked.
"""

from __future__ import annotations

import json
import re
from textwrap import dedent

import pytest
from nodejs_wheel import node

from devtools.check_print_layout import (
    _PROBE,  # pyright: ignore[reportPrivateUsage]
    BOXED_TOLERANCE_PX,
    TOLERANCE_PX,
    Boxed,
    Centred,
    Footnote,
    Marker,
    Measured,
    Overflow,
    Probe,
    findings,
)


def block(**over: object) -> Centred:
    row: Centred = {
        "index": 0,
        "parent": -1,
        "path": "p.colophon.centred[0]",
        "align": "center",
        "declared": True,
        "shown": True,
    }
    return {**row, **over}  # pyright: ignore[reportReturnType]


def marker(**over: object) -> Marker:
    row: Marker = {
        "path": "ul[0] > li[0]",
        "markerCentre": 100.0,
        "lineCentre": 100.0,
        "fontSize": 13.2,
        "lineHeight": 20.5,
    }
    return {**row, **over}  # pyright: ignore[reportReturnType]


def footnote(**over: object) -> Footnote:
    row: Footnote = {
        "path": "sup.kpress-footnote-ref[1]",
        "text": "Trump's 1979 packing shows",
        "leadIn": 300.0,
        "fontSize": 16.0,
    }
    return {**row, **over}  # pyright: ignore[reportReturnType]


def probe(**over: object) -> Probe:
    row: Probe = {
        "centred": [],
        "markers": [],
        "footnotes": [],
        "boxed": [],
        "overflow": [],
        "pageOverflow": 0,
        "widest": None,
        "measure": 576.0,
        "viewport": 576.0,
    }
    return {**row, **over}  # pyright: ignore[reportReturnType]


def both(**over: object) -> Measured:
    """The same measurement in each medium, so a finding names the medium it came from."""
    return {"screen": probe(**over), "print": probe(**over)}


def test_a_declared_centred_block_that_is_not_centred_is_a_finding() -> None:
    """The colophon's defect: the page declares it centred and the cascade disagrees."""
    assert not findings(both(centred=[block()]))
    for wrong in ("left", "justify", "start", "right"):
        found = findings(both(centred=[block(align=wrong)]))
        assert len(found) == 2, f"{wrong} should be reported in each medium"
        assert f"is `{wrong}`, not centred" in found[0]
        assert found[0].startswith("screen:")
        assert found[1].startswith("print:")


def test_a_block_the_page_does_not_declare_centred_is_not_held_to_it() -> None:
    """Figure captions are left-aligned in print on purpose and must not be findings."""
    assert not findings(both(centred=[block(declared=False, align="left")]))


def test_a_block_that_does_not_print_is_not_measured() -> None:
    """`screen-only` blocks are `display: none` and still report an inherited alignment."""
    assert not findings(both(centred=[block(shown=False, align="left")]))


@pytest.mark.parametrize("off", [-3.6, -1.9, 1.9, 2.45])
def test_a_marker_off_the_line_centre_is_a_finding(off: float) -> None:
    """The measured before-values of the bullet defect, in both directions."""
    found = findings(both(markers=[marker(markerCentre=100.0 + off)]))
    assert len(found) == 2
    assert f"{off:+.2f}px" in found[0]


@pytest.mark.parametrize("off", [0.0, -0.09, -0.01, 0.5])
def test_a_marker_within_tolerance_is_not(off: float) -> None:
    """The measured after-values. The tolerance is what separates the two lists."""
    assert abs(off) <= TOLERANCE_PX
    assert not findings(both(markers=[marker(markerCentre=100.0 + off)]))


def probe_function(name: str) -> str:
    """One helper's shipped source, so what runs here is what runs in the browser."""
    source = re.search(rf"  function {name}\([^)]*\) \{{.*?\n  \}}", _PROBE, re.DOTALL)
    assert source is not None, f"{name} is no longer a helper of its own in the probe"
    return source.group() + "\n"


def run_node(script: str) -> str | bytes:
    """What the script printed, or its stderr as the failure."""
    completed = node(
        ["-"], return_completed_process=True, input=script, capture_output=True, text=True
    )
    assert completed.returncode == 0, completed.stderr
    return completed.stdout


def first_line_box(setup: str) -> dict[str, float]:
    """Run the shipped probe against retained Range geometry, without browser setup."""
    script = (
        dedent(setup)
        + probe_function("firstLineBox")
        + "\nconsole.log(JSON.stringify(firstLineBox(el)));\n"
    )
    return json.loads(run_node(script))


def test_mixed_inline_boxes_share_one_line_and_real_marker_offsets_still_fail() -> None:
    """The printed mass-condition bullets have inline tops at -1, 0, 2 and 3px."""
    line = first_line_box("""
            const rects = [
              {top: 0, bottom: 22, height: 22, width: 100},
              {top: 0, bottom: 22.390625, height: 22.390625, width: 20},
              {top: -1, bottom: 19, height: 20, width: 10},
              {top: 2, bottom: 22, height: 20, width: 10},
              {top: 3, bottom: 21, height: 18, width: 10},
              {top: 22.390625, bottom: 44.390625, height: 22, width: 100},
            ];
            const document = {createRange: () => ({
              selectNodeContents() {}, getClientRects: () => rects,
            })};
            const el = {querySelectorAll: () => []};
        """)
    assert line == {"top": -1, "bottom": 22.390625}
    normal = marker(markerCentre=22.390625 / 2, lineCentre=(line["top"] + line["bottom"]) / 2)
    assert not findings(both(markers=[normal]))
    displaced = {**normal, "markerCentre": normal["markerCentre"] + 4}
    found = findings(both(markers=[displaced]))
    assert len(found) == 2
    assert all("+4.50px" in finding for finding in found)


def test_zero_line_height_footnote_ink_does_not_move_the_marker_line() -> None:
    """Chrome print rectangles from Further Reading, relative to the list item's top."""
    setup = """
        const reference = {lineHeight: '0px', rects: [
          {top: -8.515625, bottom: 13.484375, height: 22, width: 10.390625,
           left: 519.625, right: 530.015625},
          {top: -8.515625, bottom: 13.484375, height: 22, width: 6.40625,
           left: 520.421875, right: 526.828125},
        ]};
        const el = {querySelectorAll: () => [reference], rects: [
          {top: 0, bottom: 20, height: 20, width: 462.03125,
           left: 57.59375, right: 519.625},
          ...reference.rects,
          {top: 21.25, bottom: 41.25, height: 20, width: 200,
           left: 57.59375, right: 257.59375},
        ]};
        const getComputedStyle = el => ({lineHeight: el.lineHeight});
        const document = {createRange: () => {
          let selected;
          return {
            selectNodeContents(el) { selected = el; },
            selectNode(el) { selected = el; },
            getClientRects: () => selected.rects,
          };
        }};
        """
    line = first_line_box(setup)
    assert line == {"top": 0, "bottom": 20}
    normal = marker(markerCentre=10.63, lineCentre=(line["top"] + line["bottom"]) / 2)
    assert not findings(both(markers=[normal]))
    displaced = {**normal, "markerCentre": normal["markerCentre"] + 4}
    found = findings(both(markers=[displaced]))
    assert len(found) == 2
    assert all("+4.63px" in finding for finding in found)
    # Only zero-height references are overlays; a normal inline must still contribute.
    contributing = first_line_box(setup.replace("lineHeight: '0px'", "lineHeight: '22px'"))
    assert contributing == {"top": -8.515625, "bottom": 20}


def test_a_footnote_reference_that_opens_its_line_is_a_finding() -> None:
    """Under one em in front of it, there is no word there -- only wrapped punctuation."""
    assert not findings(both(footnotes=[footnote(leadIn=300.0)]))
    assert not findings(both(footnotes=[footnote(leadIn=16.0)]))
    found = findings(both(footnotes=[footnote(leadIn=4.2)]))
    assert len(found) == 2
    assert "opens its line, with only 4.20px" in found[0]


def test_a_block_past_the_measure_is_a_finding() -> None:
    """Anything the probe reports here is over its threshold already."""
    over: Overflow = {"path": "p[3]", "over": 12.5, "text": "a very long token"}
    found = findings(both(overflow=[over]))
    assert len(found) == 2
    assert "runs 12.50px past the measure" in found[0]


def test_the_sweep_is_reported_only_when_asked_and_only_where_a_loss_starts() -> None:
    """`--all` adds the screen-to-print diff, deduplicated to the element that changed.

    `text-align` inherits, so one lost centring is otherwise reported once for the block
    and again for every span, link and KaTeX node beneath it.
    """
    parent = block(index=0, parent=-1, declared=False, path="figcaption[1]")
    child = block(index=1, parent=0, declared=False, path="figcaption[1] > a[0]")
    measured: Measured = {
        "screen": probe(centred=[parent, child]),
        "print": probe(
            centred=[
                block(index=0, parent=-1, declared=False, align="left", path="figcaption[1]"),
                block(
                    index=1, parent=0, declared=False, align="left", path="figcaption[1] > a[0]"
                ),
            ]
        ),
    }
    assert not findings(measured), "the sweep is not a failure by default"
    swept = findings(measured, every=True)
    assert swept == [
        "centring lost in print: figcaption[1] is `center` on screen and `left` in print"
    ]


def boxed(**over: object) -> Boxed:
    row: Boxed = {"path": "a.chip[1]", "text": "PDF", "offset": 0.0}
    return {**row, **over}  # pyright: ignore[reportReturnType]


@pytest.mark.parametrize("off", [-0.65, 0.65, -2.0])
def test_a_label_off_the_centre_of_its_own_box_is_a_finding(off: float) -> None:
    """-0.65 is what the chips shipped at, and is the reason this tolerance is not 1px."""
    assert abs(off) > BOXED_TOLERANCE_PX
    found = findings(both(boxed=[boxed(offset=off)]))
    assert len(found) == 2
    assert f"{off:+.2f}px off the centre of its own box" in found[0]


@pytest.mark.parametrize("off", [0.0, 0.02, -0.5])
def test_a_label_within_tolerance_is_not(off: float) -> None:
    assert not findings(both(boxed=[boxed(offset=off)]))


def test_a_document_wider_than_the_page_is_reported_with_the_scale_chromium_applies() -> None:
    """An unclipped run past the page box shrinks every page, silently, in the PDF."""
    measured = both()
    measured["print"]["pageOverflow"] = 42
    measured["print"]["viewport"] = 576
    measured["print"]["widest"] = {
        "path": "span.base[3]",
        "over": 42,
        "text": "1 for every placement Q,",
    }
    found = findings(measured)
    assert len(found) == 1
    assert "42px wider than the page" in found[0]
    assert "scaled to 93.2%" in found[0]
    assert "span.base[3]" in found[0]


def test_screen_overflow_alone_is_not_a_page_finding() -> None:
    """On screen a wide run scrolls; only the print pass decides the paper."""
    measured = both()
    measured["screen"]["pageOverflow"] = 200
    assert findings(measured) == []


#: Enough of a DOM for the culprit scan to walk: a rectangle, a parent, and the computed
#: properties `inkRight` reads. `sig` and `round` are stubbed rather than taken from the
#: probe, the shipped `sig` wanting a real `classList` and `children`; the scan itself is
#: the shipped one. Geometry goes in as rectangles retained from the browser.
_DOM = """
const plain = {position: 'static', overflowX: 'visible', clip: 'auto', clipPath: 'none'};
const el = (name, left, right, style) => ({
  name, textContent: name, closest: () => null, parentElement: null,
  style: {...plain, ...style},
  getBoundingClientRect: () => ({left, right, width: right - left}),
});
const stack = (...nodes) => {
  for (let i = 0; i < nodes.length - 1; i++) nodes[i].parentElement = nodes[i + 1];
  return nodes[0];
};
const root = {clientWidth: 576};
const getComputedStyle = (node) => node.style;
const sig = (node) => node.name;
const round = (v) => Math.round((v || 0) * 100) / 100;
"""


def widest_run(setup: str) -> dict[str, object] | None:
    """Run the shipped culprit scan over retained geometry, without browser setup."""
    script = (
        _DOM
        + dedent(setup)
        + probe_function("widestRun")
        + probe_function("inkRight")
        + "\nconsole.log(JSON.stringify(widestRun(root) ?? null));\n"
    )
    return json.loads(run_node(script))


#: The tau* equation's MathML chain and `--self-check`'s injected block, as the rendered
#: explainer lays them out under `emulateMedia('print')` in a 576px column. KaTeX puts a
#: MathML transcription of every formula in a `.katex-mathml` span that is 1px wide with
#: `overflow: hidden`, and the boxes inside it keep their natural width: the `mrow` ends
#: at 812.77px, 236.77px past a page that its ink never reaches.
_CLIPPED_MATHML = """
const html = el('html.math-ready', 0, 576);
const body = el('body.kpress-frame', 0, 576);
const main = el('main.kpress-viewport', 0, 576, {position: 'relative'});
const column = el('div.kpress', 0, 576);
const render = el('div.kpress-math-render', 0, 576);
const display = el('span.katex-display', 0, 576);
const katex = el('span.katex', 0, 576, {position: 'relative'});
const mathml = el('span.katex-mathml', 288, 289,
  {position: 'absolute', overflowX: 'hidden', clip: 'rect(1px, 1px, 1px, 1px)'});
const math = el('math', 288, 289);
const semantics = el('semantics', 288, 289);
const mrow = el('mrow', 288, 812.765625);
const injected = el('div.print-layout-self-check', 0, 618);
stack(mrow, semantics, math, mathml, katex, display, render, column, main, body, html);
stack(injected, column);
const document = {querySelectorAll: () => [mrow, semantics, math, mathml, injected]};
"""


def test_the_named_culprit_is_the_block_that_widens_the_page_not_a_clipped_one() -> None:
    """S114-R2: the scan named clipped MathML, pointing the author at the wrong formula.

    The gate had the overflow and the scale right and the culprit wrong, which is the
    worse half to get wrong: a reader acts on the name. Measured on the rendered page,
    the tau* equation's `mrow` overhangs by 236.77px while the document's scroll width
    equals the page's -- it is 1px of ink inside `.katex-mathml` and cannot widen
    anything -- and it outbid a genuinely overflowing block by nearly six to one.
    """
    widest = widest_run(_CLIPPED_MATHML)
    assert widest is not None
    assert widest["path"] == "div.print-layout-self-check"
    assert widest["over"] == 42


def test_the_culprit_scan_excludes_by_what_clips_and_not_by_what_the_element_is() -> None:
    """The same MathML, with the wrapper's clipping removed, is named again.

    Which pins the criterion rather than the outcome: nothing here knows about KaTeX,
    and a figure given its own scroll is excluded by the same rule that excludes this.
    """
    unclipped = _CLIPPED_MATHML.replace("overflowX: 'hidden',", "").replace(
        "clip: 'rect(1px, 1px, 1px, 1px)'", "clip: 'auto'"
    )
    widest = widest_run(unclipped)
    assert widest is not None
    assert widest["path"] == "mrow"
    assert widest["over"] == 236.77


#: Synthesized rather than retained: this page has no such box. An absolutely positioned
#: element is laid out in its containing block, so a clipping ancestor below that block
#: does not cut it, and it really does widen the document.
_ESCAPING = """
const html = el('html', 0, 576);
const body = el('body', 0, 576);
const clipper = el('div.clipper', 0, 576, {overflowX: 'hidden'});
const escapee = el('div.escapee', 0, 618, {position: 'absolute'});
stack(escapee, clipper, body, html);
const document = {querySelectorAll: () => [escapee]};
"""


def test_a_box_that_escapes_the_clipping_ancestor_is_still_named() -> None:
    """Only ancestors that are laid out around a box get to cut it back."""
    widest = widest_run(_ESCAPING)
    assert widest is not None
    assert widest["path"] == "div.escapee"
    assert widest["over"] == 42
    # The same clipper, positioned, is the escapee's containing block and does clip it.
    containing = _ESCAPING.replace(
        "{overflowX: 'hidden'}", "{overflowX: 'hidden', position: 'relative'}"
    )
    assert widest_run(containing) is None
