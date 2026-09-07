"""`findings` reports what it is for, on measurements built to trip each check.

The checker's own value is that it fails. It shipped once with the `--all` gate above the
marker, footnote and overflow checks instead of below them, so a default run -- which is
the run CI makes -- evaluated only the `.centred` declaration and reported a clean layout
for a document nobody had measured. It read "print layout clean" while doing a third of
its job, which is the failure mode a check that has only ever passed cannot distinguish
itself from.

So each check is exercised here against a measurement built to trip it, and against one
built not to. The first-line probe also runs in Node against retained browser rectangle
measurements, so its grouping is tested without requiring a browser installation.
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


def test_mixed_inline_boxes_share_one_line_and_real_marker_offsets_still_fail() -> None:
    """The printed mass-condition bullets have inline tops at -1, 0, 2 and 3px."""
    function = re.search(r"  function firstLineBox\(el\) \{.*?\n  \}", _PROBE, re.DOTALL)
    assert function is not None
    script = (
        dedent("""
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
        """)
        + function.group()
        + "\nconsole.log(JSON.stringify(firstLineBox({})));\n"
    )
    completed = node(
        ["-"], return_completed_process=True, input=script, capture_output=True, text=True
    )
    assert completed.returncode == 0, completed.stderr
    line = json.loads(completed.stdout)
    assert line == {"top": -1, "bottom": 22.390625}
    normal = marker(markerCentre=22.390625 / 2, lineCentre=(line["top"] + line["bottom"]) / 2)
    assert not findings(both(markers=[normal]))
    displaced = {**normal, "markerCentre": normal["markerCentre"] + 4}
    found = findings(both(markers=[displaced]))
    assert len(found) == 2
    assert all("+4.50px" in finding for finding in found)


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
