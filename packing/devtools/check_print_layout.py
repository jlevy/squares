#!/usr/bin/env python3
"""Measure the explainer's print layout in the browser, and refuse what reads wrong.

Every other check this repository runs looks at the page on screen. The PDF is drawn
from the same document under `media: print`, and that block changes the inputs the rest
of the stylesheet computes from -- the base font size, the page margin -- and adds rules
that override the screen ones. So a print-only defect is invisible to every check we
have, and the three we shipped were all found by a human reading the finished PDF:

  * a colophon that came out left-aligned, because the print block's
    `.kpress p { text-align: left !important }` (0,2,0) beats the restatement meant to
    exempt it, `.colophon { text-align: center !important }` (0,1,0);
  * a list bullet sitting at the baseline, because its `top` is a multiple of
    `--kpress-font-size-base`, which the print block redefines;
  * a footnote reference wrapping onto a line of its own.

None of the three is a divergence between Chromium and CSS. Chromium applied exactly the
cascade we wrote; we had just never looked at what that cascade computes under `print`.
This looks.

The waiting is the PDF exporter's, deliberately: a check that measures a differently
settled page than the one that gets drawn is measuring a document nobody reads.
The same browser also exercises Figure 5 after those measurements, including its
certificate controls, feedback, field cache, and layout at desktop and phone widths.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import NotRequired, TypedDict

from playwright.sync_api import CDPSession, Locator, Page, ViewportSize

from devtools.check_math_loading import MATH_LIBRARY
from devtools.render_explainer import WALKTHROUGH
from devtools.render_explainer_pdf import BROWSER_OVERRIDE, FONTS_READY, PAGE, READY, SETTLED
from sqpack.probes import probe as load_probe

#: The probes this module hands the page, one file each under `probes/`.
PROBES = Path(__file__).resolve().parent / "probes"


class Centred(TypedDict):
    """One element's alignment, in one medium. `index` and `parent` line the two up."""

    index: int
    parent: int
    path: str
    align: str
    declared: bool
    shown: bool


class Marker(TypedDict):
    """A list marker's box against the line box it belongs to."""

    path: str
    markerCentre: float
    lineCentre: float
    fontSize: float
    baseFontSize: float
    lineHeight: float
    width: float
    height: float
    painted: bool


class Bullet(TypedDict):
    """A drawn unordered-list marker, including one whose CSS no longer paints it."""

    path: str
    width: float
    height: float
    painted: bool


class Footnote(TypedDict):
    """How much of a footnote reference's own line lies in front of it."""

    path: str
    text: str
    leadIn: float
    fontSize: float


class Boxed(TypedDict):
    """Text against the box drawn around it, for a control that is a box and a label."""

    path: str
    text: str
    offset: float


class Overflow(TypedDict):
    """A block reaching past the measure, where the paper will clip rather than wrap."""

    path: str
    over: float
    text: str


class Probe(TypedDict):
    """Everything one pass measures, plus the column it measured at."""

    centred: list[Centred]
    markers: list[Marker]
    bullets: list[Bullet]
    footnotes: list[Footnote]
    boxed: list[Boxed]
    overflow: list[Overflow]
    #: How far the document's layout reaches past the page, and the run that reaches
    #: farthest. Not clipped: Chromium scales the whole document to fit it.
    pageOverflow: float
    widest: Overflow | None
    measure: float
    viewport: float


class Measured(TypedDict):
    """The two passes, taken from one browser and one load of the page."""

    screen: Probe
    print: Probe
    controls: NotRequired[list[str]]


#: One CSS pixel, which at the print body size is six percent of an em: well under what
#: reads as misaligned, well over the rounding in a font's own metrics. The bullet defect
#: was 1.9px, so this catches it with room to spare. Not tighter, because the two sides of
#: the comparison are built differently -- a marker box against a line box -- and half a
#: pixel is finer than that construction is self-consistent to.
TOLERANCE_PX = 1.0

#: The requested optical adjustment below the geometric line centre. Keep the
#: existing one-pixel tolerance around that target, rather than relaxing it to
#: accommodate the adjustment. Numbered markers retain the geometric target.
MARKER_OPTICAL_OFFSET_EM = 0.04

#: Half of that, for a label against the box drawn around it. Tighter because the
#: measurement is tighter: both sides are rects from one layout, with none of the
#: marker check's mismatch between a marker box and a line box. It has to be tighter to
#: be worth having -- the chips shipped 0.65px off and a reader saw it, which a
#: one-pixel tolerance would have called clean.
BOXED_TOLERANCE_PX = 0.5

#: The two dimensions use the same CSS length, so only subpixel rounding can
#: distinguish them. A line-height override once turned a 3.7px square into a 27px bar.
BULLET_TOLERANCE_PX = 0.05

#: The measure the PDF actually has, in CSS pixels. `emulate_media` switches which media
#: queries match; it does not paginate and it does not apply the `@page` box. So the
#: default 1280px viewport leaves the column at whatever `--kpress-measure` caps it to --
#: 720px here -- and every horizontal question is asked of a page 25% wider than the one
#: that gets printed. Letter is 816 x 1056px at 96dpi; the stylesheet's margin is 1.25in,
#: so the column is 816 - 2 * 120.
PRINT_VIEWPORT: ViewportSize = {"width": 816 - 2 * 120, "height": 1056 - 2 * 120}

#: What each media's probe returns. One probe for both passes, so the two cannot drift
#: apart: the whole point is comparing like with like across `emulateMedia`.
_PROBE = load_probe(PROBES, "check_print_layout/layout")

#: How the layout probe names an element and rounds a measurement (`sig` and `round`), and
#: the helpers it is composed from: the bullet box, the first line box and the culprit scan.
#: Handed to it through handles, so the Node tests run the same helpers on their own.
_NAMING = load_probe(PROBES, "check_print_layout/naming")
_LAYOUT_HELPERS = load_probe(PROBES, "check_print_layout/layout_helpers")


def _layout(page: Page) -> Probe:
    """One pass of the layout probe over the page as it now stands."""
    naming = page.evaluate_handle(_NAMING)
    helpers = page.evaluate_handle(_LAYOUT_HELPERS, naming)
    measured: Probe = page.evaluate(_PROBE, {"naming": naming, "helpers": helpers})
    return measured


#: What `--self-check` puts in front of the gate, and what it holds the gate to naming.
#: 42px is the overflow the display equation shipped with, and the number the reviewer
#: reproduced this defect at: in a 576px print column it is a 618px block, and Chromium
#: would print the whole document at 93.2%.
SELF_CHECK_PX = 42.0
SELF_CHECK_CLASS = "print-layout-self-check"
SELF_CHECK_BULLET_CLASS = f"{SELF_CHECK_CLASS}-bullet"

#: Figure 5's layout at one screen width, from geometry and computed type sizes.
_PROVER_LAYOUT = load_probe(PROBES, "check_print_layout/prover_layout")


#: The text of the matched nodes in the active saved-font profile, chosen from metadata.
_ACTIVE_MATH_TEXT = load_probe(PROBES, "check_print_layout/active_math_text")


#: A typeset readout's text in the active profile, read from its text nodes.
_READOUT_TEXT = load_probe(PROBES, "check_print_layout/readout_text")

#: The distinct certificates the page's figures carry, and whether the one named is
#: selected consistently and holds focus.
_CERTIFICATE_SLUGS = load_probe(PROBES, "check_print_layout/certificate_slugs")
_CERTIFICATE_SELECTION = load_probe(PROBES, "check_print_layout/certificate_selection")
_CERTIFICATE_FOCUS = load_probe(PROBES, "check_print_layout/certificate_focus")

#: Figure 5's controls as a person cannot drive them: a canvas read back, a slider value set
#: without its event, and a restored field compared with the one rebuilt at its direction.
_CANVAS_BITMAP = load_probe(PROBES, "check_print_layout/canvas_bitmap")
_SET_VALUE = load_probe(PROBES, "check_print_layout/set_value")
_LONG_HALF_TANGENT_DIRECTION = load_probe(
    PROBES, "check_print_layout/long_half_tangent_direction"
)
_FIELD_REPLAYS = load_probe(PROBES, "check_print_layout/field_replays")


def _readout_text(readout: Locator) -> str:
    """Read a typeset readout by its text, not by Chromium's rendered-text collection.

    `inner_text` is the wrong instrument for KaTeX markup. Measured on ubuntu-latest,
    seven times across 72 runs of this check: the direction readout answers `""` from
    `innerText` -- on the first read, on a retry, and after a forced reflow -- while its
    `textContent` carries all 134 characters, every element from the readout up to
    `<html>` is displayed, visible, opaque, unanimated and has a client rect, and
    `_PROVER_LAYOUT` goes on to find that subtree's fraction digits laid out at full
    size. The document's own `innerText` is short by exactly those characters. Nothing
    is wrong with the page; the collection returns nothing for it. Recorded in
    think-kdkq.

    Read glyph and raw fallback text from the active font profile. Dormant prepared
    variants and the clipped MathML annotation cannot supply an expected value when
    the displayed formula is wrong. This uses the same profile selection as the
    semantic fraction check above, without depending on rendered-text collection.
    """
    return readout.evaluate(_READOUT_TEXT, {"math": readout.page.evaluate_handle(MATH_LIBRARY)})


def prover_findings(page: Page) -> list[str]:
    """Exercise Figure 5 through its public controls in the already open browser.

    A bitmap comparison follows two paths to the same state: restore a field after
    changing direction while it was hidden, then rebuild it at that direction. A
    stale cache differs. Neither path reads the page's private geometric variables.
    These checks run after the print measurements, so their interaction cannot change
    the state whose print layout is being inspected.
    """
    page.emulate_media(media="screen", reduced_motion="reduce")
    page.set_viewport_size({"width": 1280, "height": 900})
    page.evaluate(SETTLED)
    slugs: list[str] = page.locator(".cert-figure").evaluate_all(_CERTIFICATE_SLUGS)
    if not slugs:
        return ["Figure 5: no certificate figures were found"]
    records = (json.loads(path.read_text("utf-8")) for path in WALKTHROUGH)
    known_minima = {
        record["outer_side"].replace("/", "-"): Fraction(record["least_cell_mass"])
        for record in records
    }
    found: list[str] = []
    for slug in slugs:
        prefix = f"Figure 5 ({slug}): "
        page.locator(
            f'figure[data-figure="5"] .cert-toggle button[data-cert="{slug}"]:visible'
        ).click()
        selection: bool = page.evaluate(_CERTIFICATE_SELECTION, slug)
        if not selection:
            found.append(prefix + "certificate visibility, selection, and URL disagree")
        focused: bool = page.evaluate(_CERTIFICATE_FOCUS, slug)
        if not focused:
            found.append(prefix + "certificate switching leaves focus on a hidden control")
        figure = page.locator(f'.cert-figure[data-cert="{slug}"] figure[data-figure="5"]')
        if figure.count() != 1 or not figure.is_visible():
            found.append(prefix + "the selected certificate has no visible prover")
            continue
        reset = figure.locator(f"#btn-tight-{slug}")
        scan = figure.locator(f"#btn-scan-{slug}")
        field = figure.locator(f"#btn-heat-{slug}")
        slider = figure.locator(f"#kslider-{slug}")
        status = figure.locator(f"#status-{slug}")
        hint = figure.locator(f"#hint-{slug}")
        canvas = figure.locator("canvas")
        verdict = figure.locator(f"#vd-{slug}")
        instruction = hint.inner_text()
        initial_bitmap: str = canvas.evaluate(_CANVAS_BITMAP)
        if slider.input_value() == "0" or _control_angle(slider, prover=True) == 0:
            found.append(prefix + "the opening pose is axis-aligned")
        if verdict.is_visible() or "off the net" in (
            slider.get_attribute("aria-valuetext") or ""
        ):
            found.append(prefix + "the opening pose is not an admissible net placement")
        reset.click()
        page.evaluate(SETTLED)
        if not status.is_visible() or not status.inner_text().strip():
            found.append(prefix + "reset gives no status feedback")
        if slider.input_value() != "0":
            found.append(prefix + "reset does not restore direction zero")
        if verdict.is_visible():
            found.append(prefix + "the ordinary on-net minimum shows a stale verdict")
        if canvas.evaluate(_CANVAS_BITMAP) == initial_bitmap:
            found.append(prefix + "the minimum button does not change the opening pose")
        terms = figure.locator(f"#mv-{slug} .katex-mathml mfrac mn").evaluate_all(
            _ACTIVE_MATH_TEXT, {"math": page.evaluate_handle(MATH_LIBRARY)}
        )
        minimum_mass = Fraction(int(terms[0]), int(terms[1])) if len(terms) == 2 else None
        if slug in known_minima and minimum_mass != known_minima[slug]:
            found.append(prefix + "the minimum button disagrees with the retained certificate")
        minimum = _readout_text(figure.locator(f"#mv-{slug}"))
        canvas.click(position={"x": 20, "y": 20})
        if status.is_visible() and status.inner_text().strip():
            found.append(prefix + "moving the square leaves reset feedback visible")
        if not verdict.is_visible():
            found.append(prefix + "an outside-domain placement has no verdict")
        reset.click()
        page.evaluate(SETTLED)
        if _readout_text(figure.locator(f"#mv-{slug}")) != minimum:
            found.append(prefix + "reset does not restore the certificate's minimum mass")
        scan.click()
        if not status.is_visible() or not status.inner_text().strip():
            found.append(prefix + "the raster scan gives no status feedback")
        slider.evaluate(_SET_VALUE, slider.get_attribute("max"))
        slider.dispatch_event("input")
        if status.is_visible() and status.inner_text().strip():
            found.append(prefix + "changing direction leaves scan feedback visible")
        field.check()
        visible_bitmap: str = canvas.evaluate(_CANVAS_BITMAP)
        field.uncheck()
        if canvas.evaluate(_CANVAS_BITMAP) == visible_bitmap:
            found.append(prefix + "unchecking mass shading leaves the field unchanged")
        slider.evaluate(_SET_VALUE, "0")
        slider.dispatch_event("input")
        field.check()
        replays: bool = figure.evaluate(_FIELD_REPLAYS)
        if not replays:
            found.append(prefix + "restoring the field uses a stale direction bitmap")
        if hint.inner_text() != instruction:
            found.append(prefix + "an action overwrites the permanent instructions")
        # This is the reported long half-tangent, 12219313/45000000, rather than
        # only the much shorter zero readout which cannot expose the wrap defect.
        slider.evaluate(_LONG_HALF_TANGENT_DIRECTION)
        slider.dispatch_event("input")
        page.evaluate(SETTLED)
        if slider.get_attribute("max") == "180":
            direction = _readout_text(figure.locator(f"#kval-{slug}"))
            if not all(value in direction for value in ("12219313", "45000000", "30.3836")):
                found.append(
                    prefix + f"direction 118 has the wrong half-tangent or angle: {direction!r}"
                )
        for width in (1280, 375):
            page.set_viewport_size({"width": width, "height": 900})
            page.evaluate(SETTLED)
            layout: list[str] = page.evaluate(
                _PROVER_LAYOUT, {"math": page.evaluate_handle(MATH_LIBRARY)}
            )
            found.extend(prefix + f"{width}px: {failure}" for failure in layout)
        page.set_viewport_size({"width": 1280, "height": 900})
        slider.evaluate(_SET_VALUE, "0")
        slider.dispatch_event("input")
        box = canvas.bounding_box()
        if box is not None:
            # Center the square, then drag the visible top handle into the reflected
            # angle range. These are pointer locations in the displayed instrument;
            # they do not call or expose its private geometry functions.
            canvas.click(position={"x": box["width"] / 2, "y": box["height"] / 2})
            box = canvas.bounding_box()
            assert box is not None
            handle = figure.locator(f"#prove-rotate-{slug}")
            target = handle.bounding_box() if handle.count() else None
            if target is None:
                found.append(prefix + "the rotation handle is missing")
                continue
            page.mouse.move(
                target["x"] + target["width"] / 2, target["y"] + target["height"] / 2
            )
            page.mouse.down()
            page.mouse.move(box["x"] + box["width"] * 0.3, box["y"] + box["height"] * 0.4)
            page.mouse.up()
            if "off the net" not in (slider.get_attribute("aria-valuetext") or ""):
                found.append(prefix + "free rotation does not report an off-net direction")
            for width in (1280, 375):
                page.set_viewport_size({"width": width, "height": 900})
                page.evaluate(SETTLED)
                layout = page.evaluate(
                    _PROVER_LAYOUT, {"math": page.evaluate_handle(MATH_LIBRARY)}
                )
                found.extend(prefix + f"off-net {width}px: {failure}" for failure in layout)
        page.set_viewport_size({"width": 1280, "height": 900})
    return found


#: Whether a rotation handle is a usable touch target beside a canvas that still scrolls.
_ROTATION_TARGET = load_probe(PROBES, "check_print_layout/rotation_target")

#: Scrolling: an element brought to the middle of the viewport, and how far the reader is
#: scrolled in kpress's viewport or the document.
_SCROLL_INTO_CENTRE = load_probe(PROBES, "check_print_layout/scroll_into_centre")
_SCROLL_TOP = load_probe(PROBES, "check_print_layout/scroll_top")


def _touch_gesture(
    page: Page,
    session: CDPSession,
    start: tuple[float, float],
    end: tuple[float, float] | None = None,
) -> None:
    """Send real browser touch input, paced by animation frames rather than sleeps."""
    session.send(
        "Input.dispatchTouchEvent",
        {"type": "touchStart", "touchPoints": [{"x": start[0], "y": start[1], "id": 1}]},
    )
    if end is not None:
        for step in range(1, 7):
            x = start[0] + (end[0] - start[0]) * step / 6
            y = start[1] + (end[1] - start[1]) * step / 6
            session.send(
                "Input.dispatchTouchEvent",
                {"type": "touchMove", "touchPoints": [{"x": x, "y": y, "id": 1}]},
            )
            page.evaluate(SETTLED)
    session.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
    page.evaluate(SETTLED)


def _control_angle(control: Locator, *, prover: bool) -> float:
    if not prover:
        return float(control.input_value()) / 10
    text = control.get_attribute("aria-valuetext") or ""
    match = re.search(r"([0-9]+(?:\.[0-9]+)?) degrees", text)
    if match is None:
        raise ValueError(f"net direction control has no readable angle: {text!r}")
    return float(match.group(1))


def touch_findings(page: Page) -> list[str]:
    """Tap, drag, keyboard, and ordinary swipes on both figures and certificates."""
    session = page.context.new_cdp_session(page)
    slugs: list[str] = page.locator(".cert-figure").evaluate_all(_CERTIFICATE_SLUGS)
    found: list[str] = []
    try:
        for slug in slugs:
            page.locator(f'.cert-toggle button[data-cert="{slug}"]:visible').first.tap()
            for number, name, control_name in ((5, "prove", "kslider"), (6, "shrink", "phi")):
                prefix = f"Figure {number} touch ({slug}): "
                canvas = page.locator(f"#{name}-{slug}")
                handle = page.locator(f"#{name}-rotate-{slug}")
                if not handle.count() or not handle.is_visible():
                    found.append(prefix + "no visible rotation button before the first touch")
                    continue
                canvas.evaluate(_SCROLL_INTO_CENTRE)
                page.evaluate(SETTLED)
                control = page.locator(f"#{control_name}-{slug}")
                if number == 5:
                    control.evaluate(_SET_VALUE, "0")
                    control.dispatch_event("input")
                    box = canvas.bounding_box()
                    assert box is not None
                    _touch_gesture(
                        page,
                        session,
                        (box["x"] + box["width"] / 2, box["y"] + box["height"] / 2),
                    )
                target_findings: list[str] = handle.evaluate(_ROTATION_TARGET)
                found.extend(prefix + failure for failure in target_findings)
                before = _control_angle(control, prover=number == 5)
                # Native taps wait for a stable, hittable target after scrolling.
                handle.tap()
                page.evaluate(SETTLED)
                if _control_angle(control, prover=number == 5) == before:
                    found.append(
                        prefix + "tapping the rotation button does not turn the square"
                    )
                before = _control_angle(control, prover=number == 5)
                target, box = handle.bounding_box(), canvas.bounding_box()
                assert target is not None
                assert box is not None
                _touch_gesture(
                    page,
                    session,
                    (target["x"] + target["width"] / 2, target["y"] + target["height"] / 2),
                    (box["x"] + box["width"] * 0.3, box["y"] + box["height"] * 0.4),
                )
                if abs(_control_angle(control, prover=number == 5) - before) < 0.5:
                    found.append(
                        prefix + "touch dragging the handle does not rotate the square"
                    )
                before = _control_angle(control, prover=number == 5)
                handle.press("ArrowRight")
                if _control_angle(control, prover=number == 5) == before:
                    found.append(prefix + "the rotation button does not support arrow keys")
                canvas.evaluate(_SCROLL_INTO_CENTRE)
                page.evaluate(SETTLED)
                box = canvas.bounding_box()
                assert box is not None
                prior_scroll: float = page.evaluate(_SCROLL_TOP)
                _touch_gesture(
                    page,
                    session,
                    (box["x"] + box["width"] * 0.8, box["y"] + box["height"] * 0.8),
                    (box["x"] + box["width"] * 0.8, box["y"] + box["height"] * 0.2),
                )
                if page.evaluate(_SCROLL_TOP) - prior_scroll < 20:
                    found.append(prefix + "an ordinary canvas swipe does not scroll the page")
    finally:
        session.detach()
    return found


#: A block the print column cannot contain and a stretched list bullet, put on the page.
_SELF_CHECK_DEFECTS = load_probe(PROBES, "check_print_layout/self_check_defects")


#: A prose bullet's box against its first visible run's baseline, and the math beside it.
_MARKER_OPTICAL_GEOMETRY = load_probe(PROBES, "check_print_layout/marker_optical_geometry")


def save_marker_preview(
    page: Page,
    directory: Path,
    medium: str,
    *,
    selector: str = ".cert-page.kpress-prose ul > li",
) -> None:
    """Keep a prose bullet's ink and measured optical alignment together."""
    directory.mkdir(parents=True, exist_ok=True)
    item = page.locator(selector).first
    item.scroll_into_view_if_needed()
    measured: dict[str, object] = page.evaluate(_MARKER_OPTICAL_GEOMETRY, selector)
    if measured["initialText"] != measured["sampledText"]:
        raise AssertionError("the baseline probe changed the text's layout")
    box = item.bounding_box()
    assert box is not None
    page.screenshot(
        path=directory / f"marker-{medium}.png",
        clip={
            "x": max(0, box["x"] - 25),
            "y": max(0, box["y"] - 8),
            "width": box["width"] + 35,
            "height": box["height"] + 16,
        },
    )
    (directory / f"marker-{medium}.json").write_text(json.dumps(measured, indent=2) + "\n")


def measure(
    page_url: str,
    *,
    inject: str | None = None,
    spec: object = None,
    marker_artifacts: Path | None = None,
) -> Measured:
    """The probe's answer under each medium, from one browser and one load.

    `inject` runs in the print pass, after the media switch and the viewport change and
    before the probe, which is the only place a deliberate print-layout defect can be put
    where the print measurement will see it. Nothing but `--self-check` passes one.
    """
    import os  # noqa: PLC0415

    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        try:
            page = browser.new_page(device_scale_factor=3 if marker_artifacts else 1)
            page.emulate_media(media="screen", reduced_motion="reduce")
            page.goto(page_url, wait_until="load")
            page.wait_for_selector(READY, timeout=60_000)
            page.evaluate(FONTS_READY)
            screen = _layout(page)
            if marker_artifacts is not None:
                save_marker_preview(page, marker_artifacts, "screen")
            page.emulate_media(media="print", reduced_motion="reduce")
            page.set_viewport_size(PRINT_VIEWPORT)
            page.evaluate(FONTS_READY)
            if inject is not None:
                page.evaluate(inject, spec)
            page.evaluate(SETTLED)
            printed = _layout(page)
            if marker_artifacts is not None:
                save_marker_preview(page, marker_artifacts, "print")
            controls = prover_findings(page)
            mobile = browser.new_page(
                viewport={"width": 375, "height": 812},
                is_mobile=True,
                has_touch=True,
                reduced_motion="reduce",
            )
            mobile.goto(page_url, wait_until="load")
            mobile.wait_for_selector(READY, timeout=60_000)
            mobile.evaluate(FONTS_READY)
            controls.extend(touch_findings(mobile))
            return {"screen": screen, "print": printed, "controls": controls}
        finally:
            browser.close()


def findings(measured: Measured, *, every: bool = False) -> list[str]:
    """Everything the two passes say is wrong, as lines a reader can act on."""
    screen = measured["screen"]
    printed = measured["print"]
    found: list[str] = list(measured.get("controls", []))

    # `.centred` is the page's declaration that a block is centred in every medium, so
    # it is the thing to hold it to. Everything here runs in both media: a defect that is
    # wrong on screen too is still a defect, and two of these were.
    for medium, probe in (("screen", screen), ("print", printed)):
        found.extend(
            f"{medium}: `.centred` block is `{row['align']}`, not centred ({row['path']})"
            for row in probe["centred"]
            if row["declared"] and row["shown"] and row["align"] != "center"
        )
        for row in probe["markers"]:
            optical = row["baseFontSize"] * MARKER_OPTICAL_OFFSET_EM if row["painted"] else 0
            offset = row["markerCentre"] - row["lineCentre"] - optical
            if abs(offset) > TOLERANCE_PX:
                target = "optical centre" if row["painted"] else "line's centre"
                found.append(
                    f"{medium}: list marker off the {target} by {offset:+.2f}px "
                    f"({row['path']}, {row['fontSize']}px on a {row['lineHeight']}px line)"
                )
        for bullet in probe["bullets"]:
            if not bullet["painted"] or min(bullet["width"], bullet["height"]) <= 0:
                found.append(f"{medium}: list bullet is missing ({bullet['path']})")
            elif abs(bullet["width"] - bullet["height"]) > BULLET_TOLERANCE_PX:
                found.append(
                    f"{medium}: list bullet is {bullet['width']:.2f} by "
                    f"{bullet['height']:.2f}px instead of square ({bullet['path']})"
                )
        # Under one em there is no word in front of the reference, only stray punctuation
        # that wrapped down with it, and it reads as opening the line.
        found.extend(
            f"{medium}: footnote reference opens its line, with only "
            f"{row['leadIn']:.2f}px in front of it ({row['path']}: {row['text']!r})"
            for row in probe["footnotes"]
            if row["leadIn"] < row["fontSize"]
        )
        found.extend(
            f"{medium}: label sits {row['offset']:+.2f}px off the centre of its own box "
            f"({row['path']}: {row['text']!r})"
            for row in probe["boxed"]
            if abs(row["offset"]) > BOXED_TOLERANCE_PX
        )
        found.extend(
            f"{medium}: {row['path']} runs {row['over']:.2f}px past the measure "
            f"({row['text']!r})"
            for row in probe["overflow"]
        )

    # The page as a whole, in print only: on screen a wide run scrolls, on paper it
    # shrinks the document. Reported with the scale Chromium would apply, which is the
    # number a reader of the PDF would otherwise have to infer from the type size.
    if printed["pageOverflow"] > TOLERANCE_PX:
        scale = printed["viewport"] / (printed["viewport"] + printed["pageOverflow"])
        widest = printed["widest"]
        where = f"; the widest run is {widest['path']} ({widest['text']!r})" if widest else ""
        found.append(
            f"print: the document is {printed['pageOverflow']:.0f}px wider than the page, "
            f"so Chromium prints every page scaled to {scale:.1%}{where}"
        )

    if not every:
        return found

    # The sweep, for exploring, and not a failure: the print block left-aligns figure
    # captions on purpose, so every caption in the document answers to it. This is how
    # the colophon was found, before there was a class to check.
    was = {row["index"]: row["align"] for row in screen["centred"]}
    lost = {
        row["index"]
        for row in printed["centred"]
        if row["shown"] and was.get(row["index"]) == "center" and row["align"] != "center"
    }
    # Only where the change starts. An element under one that also lost centring
    # inherited the loss and is a symptom of the same rule, not a second finding.
    found.extend(
        f"centring lost in print: {row['path']} is `center` on screen "
        f"and `{row['align']}` in print"
        for row in printed["centred"]
        if row["index"] in lost and row["parent"] not in lost
    )

    return found


def self_check(page_url: str) -> int:
    """Put an overflow and a stretched bullet in front of the gate and require both.

    A check that has only ever passed cannot tell itself apart from one that cannot fail,
    and this one has a second way to be useless: it can fail loudly at the right size and
    still name the wrong element, which sends the author to shrink a formula that is not
    the cause. That is what it shipped doing. So the control checks all three of what the
    finding says -- the overflow, the scale, and the culprit -- against an overflow this
    puts there itself.

    A browser is the only place this can be established: what makes the reported culprit
    wrong is real layout, a MathML subtree at its natural width inside a 1px clipping
    wrapper, and no retained measurement can be trusted to still be what the page does.
    The unit tests beside this run the scan over rectangles retained from here.
    """
    measured = measure(
        page_url,
        inject=_SELF_CHECK_DEFECTS,
        spec={
            "over": SELF_CHECK_PX,
            "name": SELF_CHECK_CLASS,
            "bullet": SELF_CHECK_BULLET_CLASS,
        },
    )
    printed = measured["print"]
    column = printed["viewport"]
    print(
        f"self-check: a {column + SELF_CHECK_PX:.0f}px block in a {column:.0f}px print column, "
        f"expected to overflow the page by {SELF_CHECK_PX:.0f}px"
    )
    found = findings(measured)
    for line in found:
        print(f"self-check: {line}")

    widest = printed["widest"]
    scale = f"{column / (column + SELF_CHECK_PX):.1%}"
    wrong: list[str] = []
    if abs(printed["pageOverflow"] - SELF_CHECK_PX) > TOLERANCE_PX:
        wrong.append(
            f"the page overflows by {printed['pageOverflow']:.2f}px, not {SELF_CHECK_PX:.0f}px"
        )
    if not any(line.startswith("print: the document is") for line in found):
        wrong.append("the gate did not report the document as wider than the page")
    if not any(f"scaled to {scale}" in line for line in found):
        wrong.append(f"the gate did not report the print scale as {scale}")
    if widest is None:
        wrong.append("the gate named no culprit at all")
    elif SELF_CHECK_CLASS not in widest["path"]:
        wrong.append(
            f"the gate named {widest['path']} ({widest['over']:.2f}px over) rather than the "
            f"block it was handed; a clipped subtree cannot widen the page"
        )
    elif abs(widest["over"] - SELF_CHECK_PX) > TOLERANCE_PX:
        wrong.append(
            f"the named culprit overhangs by {widest['over']:.2f}px, not {SELF_CHECK_PX}"
        )
    if not any(
        line.startswith("print: list bullet")
        and "instead of square" in line
        and SELF_CHECK_BULLET_CLASS in line
        for line in found
    ):
        wrong.append("the gate did not report the stretched unordered-list bullet")

    for line in wrong:
        print(f"self-check failed: {line}")
    if wrong:
        return 1
    print(
        f"self-check passed: the gate fails on a {SELF_CHECK_PX:.0f}px overflow, reports the "
        f"{scale} scale, names the block that caused it, and rejects the stretched bullet"
    )
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page", type=Path, default=PAGE, help="the rendered page to measure")
    parser.add_argument("--json", action="store_true", help="print the raw measurements")
    parser.add_argument(
        "--marker-artifacts",
        type=Path,
        help="Save screen/print bullet images and baseline measurements",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="also report every block centred on screen and not in print",
    )
    parser.add_argument(
        "--self-check",
        action="store_true",
        help="inject an overflow and a stretched bullet, and check the gate names both",
    )
    args = parser.parse_args(argv)

    if not args.page.is_file():
        raise SystemExit(f"{args.page}: no rendered page; run `render_explainer` first")

    if args.self_check:
        return self_check(args.page.resolve().as_uri())

    measured = measure(args.page.resolve().as_uri(), marker_artifacts=args.marker_artifacts)
    if args.json:
        print(json.dumps(measured, indent=2, sort_keys=True))
        return 0

    found = findings(measured, every=args.all)
    for line in found:
        print(line)
    counts = measured["print"]
    declared = sum(1 for row in counts["centred"] if row["declared"])
    print(
        f"measured {len(counts['centred'])} blocks ({declared} declared `.centred`), "
        f"{len(counts['markers'])} list markers, {len(counts['footnotes'])} footnote "
        f"references and {len(measured['screen']['boxed'])} boxed labels in each medium; "
        f"print column {counts['measure']:.0f}px in a {counts['viewport']:.0f}px page"
    )
    if found:
        print(f"{len(found)} print-layout findings")
        return 1
    print("print layout clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
