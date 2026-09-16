"""`findings` reports what it is for, on measurements built to trip each check.

The checker's own value is that it fails. It shipped once with the `--all` gate above the
marker, footnote and overflow checks instead of below them, so a default run -- which is
the run CI makes -- evaluated only the `.centred` declaration and reported a clean layout
for a document nobody had measured. It read "print layout clean" while doing a third of
its job, which is the failure mode a check that has only ever passed cannot distinguish
itself from.

So each check is exercised here against a measurement built to trip it, and against one
built not to. The first-line probe and the overflow culprit scan also run in Node against
retained browser rectangle measurements (`tests/node/check_print_layout/`), so the grouping
in the one and the exclusions in the other are tested without requiring a browser
installation. Only the browser can establish that the retained rectangles are still what
the page lays out, and `check_print_layout --self-check` is where that is asked.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from nodejs_wheel import node

from devtools.check_print_layout import (
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

#: The Node scripts that run this module's probes against stand-ins.
NODE = Path(__file__).resolve().parent / "node" / "check_print_layout"


def test_layout_settlement_waits_for_pending_math() -> None:
    """Two animation frames cannot finish a readout still waiting for its font."""
    completed = node(
        [str(NODE / "settlement-waits-for-math.mjs")],
        return_completed_process=True,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr


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
        "baseFontSize": 16.0,
        "lineHeight": 20.5,
        "width": 3.25,
        "height": 3.25,
        "painted": False,
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
        "bullets": [],
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


def test_numbered_markers_do_not_have_to_be_square() -> None:
    assert not findings(both(markers=[marker(height=22, width=10, painted=False)]))


@pytest.mark.parametrize("base_size", [16.0, 18.0])
def test_painted_markers_use_the_requested_optical_offset(base_size: float) -> None:
    adjusted = marker(markerCentre=100 + base_size * 0.04, baseFontSize=base_size, painted=True)
    assert not findings(both(markers=[adjusted]))
    for displacement in (-1.01, 1.01):
        wrong = {**adjusted, "markerCentre": adjusted["markerCentre"] + displacement}
        found = findings(both(markers=[wrong]))
        assert len(found) == 2
        assert all("optical centre" in message for message in found)


def test_centered_bullets_must_still_be_visible_squares() -> None:
    """The glyph-centering override stretched drawn squares into centered vertical bars."""
    square = {"path": "ul[0] > li[0]", "width": 3.3, "height": 3.3, "painted": True}
    assert not findings(both(markers=[marker()], bullets=[square]))
    for change in (
        {"height": 25.0},
        {"height": 3.36},
        {"height": 0.0},
        {"width": 0.0},
        {"painted": False},
    ):
        found = findings(both(markers=[marker()], bullets=[{**square, **change}]))
        assert len(found) == 2
        assert found[0].startswith("screen: list bullet")
        assert found[1].startswith("print: list bullet")
        assert all("ul[0] > li[0]" in line for line in found)


def run_node(script: str, *arguments: str) -> str | bytes:
    """What one of the `NODE` scripts printed, or its stderr as the failure."""
    completed = node(
        [str(NODE / script), *arguments],
        return_completed_process=True,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    return completed.stdout


def first_line_box(script: str, *arguments: str) -> dict[str, float]:
    """Run the shipped probe against retained Range geometry, without browser setup."""
    return json.loads(run_node(script, *arguments))


def test_bullet_probe_measures_boxes_and_keeps_missing_markers() -> None:
    """A missing pseudo-element must reach the guard; ordered and hidden items must not."""
    result = json.loads(run_node("bullet-box.mjs"))
    assert result["ordered"] is None
    assert result["hidden"] is None
    square, *broken = result["boxes"]
    assert square == {"path": "ul[0] > li[0]", "width": 3.3, "height": 3.3, "painted": True}
    assert not findings(both(bullets=[square]))
    for bullet in broken:
        assert bullet is not None
        found = findings(both(bullets=[bullet]))
        assert len(found) == 2
        assert all("list bullet" in line for line in found)


def test_mixed_inline_boxes_share_one_line_and_real_marker_offsets_still_fail() -> None:
    """The printed mass-condition bullets have inline tops at -1, 0, 2 and 3px."""
    line = first_line_box("mixed-inline-boxes.mjs")
    assert line == {"top": -1, "bottom": 22.390625}
    normal = marker(markerCentre=22.390625 / 2, lineCentre=(line["top"] + line["bottom"]) / 2)
    assert not findings(both(markers=[normal]))
    displaced = {**normal, "markerCentre": normal["markerCentre"] + 4}
    found = findings(both(markers=[displaced]))
    assert len(found) == 2
    assert all("+4.50px" in finding for finding in found)


def test_zero_line_height_footnote_ink_does_not_move_the_marker_line() -> None:
    """Chrome print rectangles from Further Reading, relative to the list item's top."""
    line = first_line_box("zero-line-height-footnote.mjs", "0px")
    assert line == {"top": 0, "bottom": 20}
    normal = marker(markerCentre=10.63, lineCentre=(line["top"] + line["bottom"]) / 2)
    assert not findings(both(markers=[normal]))
    displaced = {**normal, "markerCentre": normal["markerCentre"] + 4}
    found = findings(both(markers=[displaced]))
    assert len(found) == 2
    assert all("+4.63px" in finding for finding in found)
    # Only zero-height references are overlays; a normal inline must still contribute.
    contributing = first_line_box("zero-line-height-footnote.mjs", "22px")
    assert contributing == {"top": -8.515625, "bottom": 20}


def test_clipped_mathml_does_not_move_the_marker_line_but_visible_fallback_does() -> None:
    """Retained mass-condition geometry: hidden MathML rises above the real line."""
    line = first_line_box("clipped-mathml-line.mjs", "absolute")
    assert line == {"top": 1, "bottom": 26.1875}
    unchanged = marker(
        markerCentre=14.217525,
        lineCentre=(line["top"] + line["bottom"]) / 2,
        baseFontSize=18,
        painted=True,
    )
    assert not findings(both(markers=[unchanged]))
    shifted = {**unchanged, "markerCentre": unchanged["markerCentre"] + 4}
    assert len(findings(both(markers=[shifted]))) == 2
    visible = first_line_box("clipped-mathml-line.mjs", "static")
    assert visible == {"top": -3.6875, "bottom": 26.1875}


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


def test_prover_failures_are_reported_without_the_optional_layout_sweep() -> None:
    measured = both()
    measured["controls"] = [
        "Figure 5 (19-5): restoring the field uses a stale direction bitmap"
    ]
    assert findings(measured) == measured["controls"]
    assert findings(measured, every=True) == measured["controls"]


@pytest.mark.parametrize("broken", [False, True], ids=["valid", "known-defects"])
def test_prover_layout_probe_accepts_valid_boxes_and_rejects_known_defects(
    *, broken: bool
) -> None:
    """Run the browser's own predicate on contrasting geometry and font measurements.

    The Pages job supplies real DOM geometry; these controls prove that the predicate
    refuses the earlier side panel, small fraction, broken math, and ignored hidden
    attribute without requiring every pytest host to install a browser.
    """
    measured: list[str] = json.loads(run_node("prover-layout.mjs", json.dumps(broken)))
    if not broken:
        assert measured == []
        return
    assert set(measured) == {
        "control panel is beside the graphic",
        "a direction item permits an internal line break",
        "a direction item overflows the control panel",
        "the mass fraction has reduced-size numerator or denominator",
        "the half-tangent fraction has reduced-size numerator or denominator",
        "a hidden status or verdict still occupies a visible box",
    }


def test_minimum_mass_reads_only_the_selected_semantic_fraction() -> None:
    """Clipped active MathML survives; inactive font variants cannot add extra terms."""
    run_node("minimum-mass-terms.mjs")


def test_readout_text_excludes_dormant_variants_and_semantics_but_keeps_fallback() -> None:
    """Hidden expected values cannot mask a wrong active readout or replace its glyphs."""
    run_node("readout-text.mjs")


@pytest.mark.parametrize("broken", [False, True], ids=["usable", "known-touch-defects"])
def test_rotation_target_probe_requires_a_large_named_unobstructed_touch_target(
    *, broken: bool
) -> None:
    measured: list[str] = json.loads(run_node("rotation-target.mjs", json.dumps(broken)))
    if not broken:
        assert measured == []
        return
    assert set(measured) == {
        "rotation target is smaller than 44px",
        "rotation target is not a named native button",
        "rotation target is covered by another element",
        "rotation target allows the browser to cancel its touch drag",
        "the canvas no longer permits vertical touch scrolling",
    }


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


def widest_run(scene: str, style: dict[str, str]) -> dict[str, object] | None:
    """Run the shipped culprit scan over retained geometry, without browser setup.

    `scene` is one of `widest-run.mjs`'s element chains, and `style` the computed style of
    the ancestor whose clipping decides the answer: `.katex-mathml` in `mathml`, and the
    clipping block in `escaping`.
    """
    return json.loads(run_node("widest-run.mjs", scene, json.dumps(style)))


#: `.katex-mathml` as the rendered explainer lays it out under print: absolutely positioned,
#: 1px wide with `overflow: hidden`, and clipped to a pixel.
CLIPPED_MATHML = {
    "position": "absolute",
    "overflowX": "hidden",
    "clip": "rect(1px, 1px, 1px, 1px)",
}


def test_the_named_culprit_is_the_block_that_widens_the_page_not_a_clipped_one() -> None:
    """S114-R2: the scan named clipped MathML, pointing the author at the wrong formula.

    The gate had the overflow and the scale right and the culprit wrong, which is the
    worse half to get wrong: a reader acts on the name. Measured on the rendered page,
    the tau* equation's `mrow` overhangs by 236.77px while the document's scroll width
    equals the page's -- it is 1px of ink inside `.katex-mathml` and cannot widen
    anything -- and it outbid a genuinely overflowing block by nearly six to one.
    """
    widest = widest_run("mathml", CLIPPED_MATHML)
    assert widest is not None
    assert widest["path"] == "div.print-layout-self-check"
    assert widest["over"] == 42


def test_the_culprit_scan_excludes_by_what_clips_and_not_by_what_the_element_is() -> None:
    """The same MathML, with the wrapper's clipping removed, is named again.

    Which pins the criterion rather than the outcome: nothing here knows about KaTeX,
    and a figure given its own scroll is excluded by the same rule that excludes this.
    """
    unclipped = {"position": "absolute", "clip": "auto"}
    widest = widest_run("mathml", unclipped)
    assert widest is not None
    assert widest["path"] == "mrow"
    assert widest["over"] == 236.77


#: A clipping block with a box absolutely positioned inside it, in `escaping`.
CLIPPER = {"overflowX": "hidden"}


def test_a_box_that_escapes_the_clipping_ancestor_is_still_named() -> None:
    """Only ancestors that are laid out around a box get to cut it back."""
    widest = widest_run("escaping", CLIPPER)
    assert widest is not None
    assert widest["path"] == "div.escapee"
    assert widest["over"] == 42
    # The same clipper, positioned, is the escapee's containing block and does clip it.
    containing = {**CLIPPER, "position": "relative"}
    assert widest_run("escaping", containing) is None
