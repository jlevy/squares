"""The layout check's rules, without a browser.

`check_layout.check_open` measures the built page in Chromium inside `check_frontend`. What is
tested here is what decides the verdict: one well-formed page passes, and each rule refuses a
page that breaks it in exactly the way it names. Each negative control changes one measurement.
"""

from __future__ import annotations

import copy
from collections.abc import Callable
from typing import Any

import numpy as np
import pytest

from workbench_tools.check_layout import (
    LEGEND_INK_SLACK,
    attribution_findings,
    citation_findings,
    facts_findings,
    findings,
    frames_findings,
    ink_bottoms,
    legend_findings,
    legend_ink_findings,
    widest_cited,
)

TYPE = {"family": '"Source Sans 3", sans-serif', "size": "28px", "weight": "500"}
#: Computed colors for status labels, ordinary case numbers, and recent case numbers.
GREY = "rgb(71, 82, 95)"
INK = "rgb(17, 21, 25)"
SCARLET = "rgb(163, 18, 63)"
LABEL = {**TYPE, "color": GREY}
#: The frames' three colours: `--scene-frame`, `--scene-frame-locked`, `--scene-trace`.
FRAME = "rgb(125, 133, 144)"
LOCKED = "rgb(23, 121, 74)"
TRACE = "rgb(223, 227, 231)"
#: A section head's type, as PROVEN, CITATION and OPEN are all set (measured on the page).
HEAD = {
    "family": '"Source Sans 3", sans-serif',
    "size": "28px",
    "weight": "500",
    "spacing": "4.48px",
    "transform": "uppercase",
    "color": "rgb(138, 147, 158)",
}


def _panel(name: str, left: float, right: float, top: float, bottom: float) -> dict[str, Any]:
    return {"name": name, "left": left, "right": right, "top": top, "bottom": bottom}


def _page() -> dict[str, Any]:
    """A 1024-wide page that keeps every rule: a 16 px gutter, 8 px gaps, 28 px controls."""
    law = _panel("#law-box", 16, 700, 120, 250)
    walls = _panel("#wall-box", 708, 1008, 120, 250)
    return {
        "viewport": {"width": 1024, "height": 768},
        "documentWidth": 1024,
        "controls": {
            "left": 0,
            "top": 400,
            "right": 1024,
            "bottom": 768,
            "clientWidth": 1024,
            "scrollWidth": 1024,
            "clientHeight": 368,
            "scrollHeight": 600,
            "paddingLeft": 16,
            "paddingRight": 16,
            "borderLeft": 0,
        },
        "tokens": {"gutter": "16px", "stack": "8px", "control": "28px", "tab": "32px"},
        "blocks": [
            _panel("#mode-subpanel", 16, 1008, 8, 112),
            {**_panel("div.panel-row", 16, 1008, 120, 250)},
            _panel("#animation-editor", 16, 1008, 258, 400),
        ],
        "panels": [
            _panel("#mode-subpanel", 16, 1008, 8, 112),
            law,
            walls,
            _panel("#animation-editor", 16, 1008, 258, 400),
        ],
        "rows": [{**_panel("div.panel-row", 16, 1008, 120, 250), "panels": [law, walls]}],
        "controlsFound": [
            {"kind": "tab", "name": "#mode-animate", "height": 32},
            {"kind": "button", "name": "#play", "height": 28},
            {"kind": "select", "name": "#style-select", "height": 28},
            {"kind": "input-number", "name": "#range-from", "height": 28},
            {"kind": "segment", "name": "button.on", "height": 26},
            {"kind": "segment", "name": "button", "height": 26},
            {"kind": "segmented", "name": "#initial-seg", "height": 28},
            {"kind": "segmented", "name": "#phase-seg", "height": 54},
        ],
        "facts": None,
    }


def _layer(*, recent: bool, open_items: int) -> dict[str, Any]:
    badges = [{"icon": "badge badge-solid", "text": "exact", **LABEL}]
    heads = ["Proven", "Open"] if open_items else ["Proven"]
    return {
        "heads": heads,
        "headTypes": [{"text": head, **HEAD} for head in heads],
        "citations": None,
        "openItems": open_items,
        "colours": {"recent": SCARLET, "ink": INK, "label": GREY},
        "numeral": {
            "recent": recent,
            "color": SCARLET if recent else INK,
            "title": "Recent result" if recent else None,
        },
        "recencyMarks": 0,
        "badges": badges,
    }


def _frames(*, locked: bool = True, catalogue: bool = True) -> dict[str, Any]:
    """The stage's three outer container borders as the catalogue or as Pack draws them."""
    return {
        "container": {
            "shown": not catalogue,
            "stroke": FRAME,
            "strokeWidth": "4px",
            "locked": False,
        },
        "box": {
            "shown": catalogue,
            "stroke": LOCKED if locked else FRAME,
            "strokeWidth": "4px",
            "locked": locked,
        },
        "trace": {"shown": catalogue, "stroke": TRACE, "strokeWidth": "4px", "locked": False},
        "tokens": {"width": "4px", "frame": FRAME, "locked": LOCKED, "trace": TRACE},
    }


def _attribution() -> dict[str, Any]:
    """The address one legend line under the legend at its left edge, and the version on its
    baseline at the column's right edge, over nothing. The numbers are the page's, measured."""
    legend = {"left": 1116.0, "right": 1884.0, "top": 906.0, "bottom": 997.52}
    return {
        "placed": True,
        "shown": True,
        "left": 1116.0,
        "baseline": 1018.52,
        "legend": legend,
        "rows": [929.0, 959.14, 988.83],
        "column": dict(legend),
        "version": {
            "text": "v0.4.1-f5e113",
            "right": 1884.0,
            "baseline": 1018.52,
            "ink": {"left": 1762.04, "top": 995.66, "right": 1884.0, "bottom": 1027.09},
            "screen": {"x": 1300.0, "y": 352.5, "width": 50.0, "height": 13.0},
            "family": '"Source Sans 3", sans-serif',
            "size": "22px",
            "weight": "400",
            "fill": FRAME,
            "shown": True,
        },
        "ink": {"left": 1116.0, "right": 1351.13, "top": 995.66, "bottom": 1027.09},
        "frame": {"left": 0.0, "top": 0.0, "right": 1920.0, "bottom": 1080.0},
        "screen": {"x": 932.9, "y": 352.5, "width": 97.2, "height": 13.0},
        "family": '"Source Sans 3", sans-serif',
        "size": "22px",
        "weight": "400",
        "fill": FRAME,
        "obstacles": [
            {"name": "#packing-svg", "left": 60, "right": 1060, "top": 12, "bottom": 983},
            {"name": "div.numeral", "left": 476, "right": 680.8, "top": 973, "bottom": 1074},
            {"name": "#site-note", "left": 0, "right": 1860, "top": 2500, "bottom": 2560},
        ],
    }


def test_a_page_that_keeps_every_rule_passes() -> None:
    assert findings(_page()) == []
    assert facts_findings(_layer(recent=True, open_items=2), recent=True) == []
    assert facts_findings(_layer(recent=False, open_items=0), recent=False) == []
    assert frames_findings(_frames()) == []
    assert frames_findings(_frames(locked=False)) == []
    assert frames_findings(_frames(catalogue=False)) == []
    assert attribution_findings(_attribution(), aligned=True) == []
    assert attribution_findings(_attribution(), aligned=False) == []


def _set(path: str, value: Any) -> Callable[[dict[str, Any]], None]:
    def change(page: dict[str, Any]) -> None:
        *parents, leaf = path.split(".")
        node: Any = page
        for key in parents:
            node = node[int(key)] if key.isdigit() else node[key]
        node[int(leaf) if leaf.isdigit() else leaf] = value

    return change


@pytest.mark.parametrize(
    ("change", "expected"),
    [
        (_set("documentWidth", 1100), "the page is 1100 px wide"),
        (_set("controls.scrollWidth", 1200), "the controls scroll sideways"),
        (_set("controls.paddingRight", 12), "the column's gutters differ"),
        (_set("tokens.gutter", "12px"), "not the 12.0 px gutter"),
        (_set("tokens.stack", None), "declares no pixel --layout-gutter"),
        # The search workspace, centred at 1100 px inside a wider column.
        (_set("blocks.2.left", 170), "#animation-editor spans 170..1008"),
        # The mode tabs' panel, as wide as its tabs.
        (_set("blocks.0.right", 246), "#mode-subpanel spans 16..246"),
        (_set("blocks.2.top", 272), "are 22.00 apart, not 8.00"),
        # Pack's step-animation row, emptied by hiding its one panel: 8 + 0 + 8 between blocks.
        (_set("blocks.1.bottom", 120), "div.panel-row is drawn empty"),
        (
            _set("rows.0.panels.1.left", 718),
            "#law-box and #wall-box in div.panel-row are 18.00 apart",
        ),
        (_set("rows.0.panels.1.right", 900), "line ends at 900"),
        (_set("controlsFound.1.height", 24.5), "button #play is 24.5 tall, not 28.0"),
        (_set("controlsFound.3.height", 30), "input-number #range-from is 30 tall"),
        (_set("controlsFound.0.height", 36), "tab #mode-animate is 36 tall, not 32.0"),
        (_set("controlsFound.5.height", 48), "segment controls come in 2 heights"),
        (_set("controlsFound.7.height", 40), "segmented #phase-seg is 40 tall"),
        (_set("tokens.control", None), "declares no pixel --control-height"),
        (_set("panels.2.left", 690), "#law-box and #wall-box overlap by 10.0 x 130.0"),
    ],
)
def test_each_layout_rule_refuses_the_page_that_breaks_it(
    change: Callable[[dict[str, Any]], None], expected: str
) -> None:
    page = copy.deepcopy(_page())
    change(page)
    found = findings(page)
    assert any(expected in item for item in found), found


def test_heights_without_tokens_still_have_to_agree() -> None:
    """A page with no control token is still refused for mixing control heights."""
    page = _page()
    page["tokens"]["control"] = None
    page["controlsFound"][2]["height"] = 30
    assert any("not one height" in item for item in findings(page))


def test_a_nested_panel_is_not_an_overlap() -> None:
    page = _page()
    page["panels"].append(_panel("fieldset", 30, 990, 270, 390))
    assert findings(page) == []


def test_open_is_headed_only_when_something_is_open() -> None:
    headed_over_nothing = _layer(recent=False, open_items=0)
    headed_over_nothing["heads"] = ["Proven", "Open"]
    assert facts_findings(headed_over_nothing) == ["OPEN is headed with 0 open items"]
    unheaded_items = _layer(recent=False, open_items=2)
    unheaded_items["heads"] = ["Proven"]
    assert facts_findings(unheaded_items) == ["OPEN is not headed with 2 open items"]


def test_recent_case_numbers_use_red_and_an_accessible_title() -> None:
    layer = _layer(recent=True, open_items=2)
    layer["numeral"]["color"] = INK
    assert facts_findings(layer, recent=True) == [f"the case number is {INK}, not {SCARLET}"]
    layer["numeral"]["color"] = SCARLET
    layer["numeral"]["title"] = None
    assert facts_findings(layer, recent=True) == [
        "the recent case number has no Recent result title"
    ]
    assert facts_findings(layer, recent=False) == [
        "the case number's recency does not match False"
    ]
    layer["recencyMarks"] = 1
    assert "the facts panel still draws a recency symbol" in facts_findings(layer)


def test_status_badges_keep_one_type_and_label_color() -> None:
    layer = _layer(recent=True, open_items=2)
    layer["badges"].append({"icon": "badge badge-solid", "text": "rigid", **LABEL})
    layer["badges"][0]["family"] = '"PT Serif", serif'
    assert any("2 different types" in item for item in facts_findings(layer))
    layer["badges"][0]["color"] = SCARLET
    assert f"the `exact` label is {SCARLET}, not the label grey {GREY}" in facts_findings(layer)


@pytest.mark.parametrize(
    ("change", "expected"),
    [
        (_set("box.strokeWidth", "1.5px"), "the box frame is 1.5px wide, not 4.0 px"),
        (_set("trace.strokeWidth", "1.5px"), "the trace frame is 1.5px wide, not 4.0 px"),
        (_set("container.strokeWidth", "2px"), "the container frame is 2px wide, not 4.0 px"),
        (_set("tokens.width", None), "declares no pixel --scene-frame-width"),
        (_set("box.stroke", "rgb(0, 0, 0)"), "the box is rgb(0, 0, 0), not the best known"),
        (_set("trace.stroke", "rgb(0, 0, 0)"), "the trace is rgb(0, 0, 0), not the lightest"),
    ],
)
def test_each_frame_rule_refuses_the_stage_that_breaks_it(
    change: Callable[[dict[str, Any]], None], expected: str
) -> None:
    frames = copy.deepcopy(_frames())
    change(frames)
    found = frames_findings(frames)
    assert any(expected in item for item in found), found


def test_the_box_is_grey_on_its_way_and_green_only_where_it_locks() -> None:
    """One width, and the lock is the only colour change (the owner, 2026-09-17)."""
    green_on_its_way = _frames(locked=False)
    green_on_its_way["box"]["stroke"] = LOCKED
    assert frames_findings(green_on_its_way) == [
        f"the box is {LOCKED}, not the frames' grey {FRAME}"
    ]
    grey_at_rest = _frames()
    grey_at_rest["box"]["stroke"] = FRAME
    assert frames_findings(grey_at_rest) == [
        f"the box is {FRAME}, not the best known side's green {LOCKED}"
    ]
    black_container = _frames(catalogue=False)
    black_container["container"]["stroke"] = "rgb(0, 0, 0)"
    assert frames_findings(black_container) == [
        f"the container is rgb(0, 0, 0), not the frames' grey {FRAME}"
    ]


@pytest.mark.parametrize(
    ("change", "expected"),
    [
        (_set("left", 1110.0), "starts at 1110.00, 6.00 stage px from the legend's left edge"),
        # Where it stood before the owner asked for the legend's own spacing: 30 under the
        # legend's box is 38 under its last row, against the rows' 30. And closer than a line.
        (_set("baseline", 1027.52), "is 38.69 stage px under the legend's last row, not one"),
        (_set("baseline", 1008.0), "is 19.17 stage px under the legend's last row, not one"),
        (_set("rows", [929.0]), "cannot be measured against the legend's rows"),
        (_set("legend", None), "cannot be measured against the legend"),
        (_set("left", None), "cannot be measured against the legend"),
        # The overlay's units are stage pixels only because its box is the stage's; a box that
        # is not makes the two numbers above mean something else.
        (_set("frame.right", 1024.0), "overlay is not the stage's own box"),
    ],
)
def test_each_attribution_anchor_refuses_the_stage_that_breaks_it(
    change: Callable[[dict[str, Any]], None], expected: str
) -> None:
    attribution = copy.deepcopy(_attribution())
    change(attribution)
    found = attribution_findings(attribution, aligned=True)
    assert any(expected in item for item in found), found


@pytest.mark.parametrize(
    ("change", "expected"),
    [
        (_set("version", None), "the shared version is not drawn"),
        (_set("version.text", ""), "the shared version is not drawn"),
        (lambda a: a["version"].update(shown=False), "the shared version is not drawn"),
        # On its own line rather than the attribution's, and short of the column's edge.
        (_set("version.baseline", 1022.0), "stands on 1022.00, not the attribution's baseline"),
        (_set("version.right", 1876.0), "ends at 1876.00, not the column's right edge at 1884"),
        (_set("column", None), "not the column's right edge at None"),
        # Styled to match it (the owner, 2026-09-22): one family, size, weight and colour.
        (
            _set("version.size", "18px"),
            "the version's size is 18px, not the attribution's 22px",
        ),
        (_set("version.weight", "600"), "the version's weight is 600"),
        (_set("version.fill", GREY), f"the version's fill is {GREY}"),
        (_set("version.family", "serif"), "the version's family is serif"),
        # A mode that set both texts on the right would put the one over the other.
        (_set("ink.right", 1800.0), "the version is drawn over the attribution"),
    ],
)
def test_each_version_rule_refuses_the_stage_that_breaks_it(
    change: Callable[[dict[str, Any]], None], expected: str
) -> None:
    attribution = copy.deepcopy(_attribution())
    change(attribution)
    found = attribution_findings(attribution, aligned=True)
    assert any(expected in item for item in found), found


def test_the_attribution_is_drawn_and_clears_what_the_stage_draws() -> None:
    hidden = _attribution()
    hidden["placed"] = False
    assert attribution_findings(hidden, aligned=True) == [
        "the stage's attribution is not drawn"
    ]
    # A stage laid out so that the packing reaches into the address's corner.
    over_the_packing = copy.deepcopy(_attribution())
    over_the_packing["obstacles"][0]["right"] = 1600
    over_the_packing["obstacles"][0]["bottom"] = 1050
    assert any(
        "drawn over #packing-svg" in item
        for item in attribution_findings(over_the_packing, aligned=True)
    )
    # The legend is not shown in Pack and the studio, so where the address starts is not checked
    # there, but what it is drawn over still is: those modes center the packing, and at the
    # legend's left edge the address sat across it.
    clear = copy.deepcopy(_attribution())
    clear["legend"] = None
    # Where Pack and the studio set the address: mirroring the version, at the stage's bottom
    # left, 36 stage px in from its edge as the version is from the right one.
    clear["ink"] = {"left": 36.0, "right": 271.13, "top": 995.66, "bottom": 1027.09}
    clear["obstacles"][0] = {
        "name": "#packing-svg",
        "left": 460,
        "right": 1516,
        "top": 12,
        "bottom": 1068,
    }
    assert attribution_findings(clear, aligned=False) == []
    across = copy.deepcopy(clear)
    across["ink"] = _attribution()["ink"]
    assert any(
        "drawn over #packing-svg" in item
        for item in attribution_findings(across, aligned=False)
    )
    # The version and the address both at the right, as the address stood there before the
    # version: 379 stage px of text in the 368 right of Pack's drawing.
    both_right = copy.deepcopy(clear)
    both_right["ink"] = {"left": 1505.0, "right": 1740.0, "top": 995.66, "bottom": 1027.09}
    assert any(
        "the attribution is drawn over #packing-svg by 11.0" in item
        for item in attribution_findings(both_right, aligned=False)
    )
    version_over = copy.deepcopy(clear)
    version_over["version"]["ink"] = {
        "left": 1400.0,
        "right": 1522.0,
        "top": 995.66,
        "bottom": 1027.09,
    }
    assert any(
        "the version is drawn over #packing-svg" in item
        for item in attribution_findings(version_over, aligned=False)
    )


# -------------------------------------------------------------------------------- the legend


def test_the_legends_math_must_stand_on_its_sentences_baseline() -> None:
    # Measured on the page: the sentence and both formulas at 929.5.
    aligned = {"text": 929.5, "math": [{"source": "s(n)", "baseline": 929.5}]}
    assert legend_findings(aligned) == []
    low = {"text": 929.5, "math": [{"source": "s(n)", "baseline": 930.5}]}
    [finding] = legend_findings(low)
    assert "s(n) stands +1.00 stage px" in finding
    assert legend_findings({"text": 929.5, "math": []}) == [
        "the legend's sentence sets no math to measure"
    ]


def _letters(bottoms: dict[int, int], height: int = 40, width: int = 60) -> np.ndarray:
    """White paper with a black block per letter, each ten columns wide, ending at its row."""
    image = np.full((height, width, 3), 255, dtype=np.uint8)
    for start, bottom in bottoms.items():
        image[bottom - 12 : bottom, start : start + 10] = 0
    return image


def test_ink_is_read_where_each_letter_ends_and_nowhere_else() -> None:
    image = _letters({0: 30, 20: 30, 40: 34})
    glyphs = [
        {"char": "i", "math": False, "left": 0, "right": 10},
        {"char": "s", "math": False, "left": 20, "right": 30},
        {"char": "n", "math": True, "left": 40, "right": 50},
    ]
    assert ink_bottoms(image, glyphs, origin=0, scale=1) == [30.0, 30.0, 34.0]
    # An empty advance box drew nothing, which is its own finding rather than a zero.
    blank = [{"char": "x", "math": True, "left": 52, "right": 60}]
    assert ink_bottoms(image, blank, origin=0, scale=1) == [None]


def test_a_formula_whose_ink_ends_off_the_sentences_line_is_a_finding() -> None:
    glyphs = [
        {"char": "i", "math": False},
        {"char": "s", "math": False},
        {"char": "e", "math": False},
        {"char": "n", "math": True},
    ]
    # The line is the median of the text letters, so one letter's overshoot does not move it.
    on_line = [929.25, 929.5, 929.5, 929.5 + LEGEND_INK_SLACK / 2]
    assert legend_ink_findings(glyphs, on_line) == []
    [finding] = legend_ink_findings(glyphs, [929.25, 929.5, 929.5, 930.5])
    assert "'n' ends +1.00 stage px" in finding
    assert legend_ink_findings(glyphs, [929.5, 929.5, 929.5, None]) == [
        "the legend's math 'n' drew no ink to read"
    ]


# ------------------------------------------------------------------------------ the citations

#: The bound line's two colours, which a citation line's label takes.
LOWER_INK = SCARLET
UPPER_INK = LOCKED


def _section(*, lower: bool = True, upper: bool = True, noted: bool = True) -> dict[str, Any]:
    """A CITATION section as the page draws it at n = 17, with OPEN moved below it."""

    def line(
        slot: str, top: float, right: float, *, drawn: bool, marked: bool
    ) -> dict[str, Any]:
        return {
            "slot": slot,
            "bound": slot if drawn else None,
            "text": f"the {slot} bound's source" if drawn else None,
            "note": "(reported)" if drawn and marked else None,
            "color": (LOWER_INK if slot == "lower" else UPPER_INK) if drawn else None,
            "left": 1116.0,
            "top": top,
            "right": right if drawn else 1116.0,
            "bottom": top + 30,
        }

    drawn = lower or upper
    return {
        "head": {
            "text": "Citation" if drawn else "",
            "drawn": drawn,
            "left": 1116.0,
            "top": 618.0,
            "right": 1263.09 if drawn else 1116.0,
            "bottom": 652.0,
        },
        "record": (
            {
                "text": "recordn-017",
                "left": 1278.6,
                "top": 624.5,
                "right": 1395.2,
                "bottom": 654.2,
            }
            if drawn
            else None
        ),
        "lines": [
            line("lower", 658.0, 1461.06, drawn=lower, marked=False),
            line("upper", 688.0, 1814.38, drawn=upper, marked=noted),
        ],
        "below": [
            {
                "name": "div.section-head.head-open",
                "left": 1116,
                "top": 746,
                "right": 1202,
                "bottom": 780,
            },
            {"name": "div.open-items", "left": 1116, "top": 786, "right": 1280, "bottom": 826},
        ],
        "column": {"left": 1116.0, "top": 906.0, "right": 1884.0, "bottom": 997.52},
        "colours": {"lower": LOWER_INK, "upper": UPPER_INK},
    }


def test_a_citation_section_that_keeps_every_rule_passes() -> None:
    assert citation_findings(_section(), shown=True) == []
    assert citation_findings(_section(noted=False), shown=True) == []
    # One bound cited: the other line is an empty slot, and the section is still headed.
    assert citation_findings(_section(lower=False), shown=True) == []
    assert citation_findings(_section(upper=False), shown=True) == []
    # Nothing cited: the slots are built and empty, and the head is not drawn.
    assert citation_findings(_section(lower=False, upper=False), shown=True) == []
    assert citation_findings(None, shown=False) == []


@pytest.mark.parametrize(
    ("change", "expected"),
    [
        # Too long for the column at the stage's small type: the fixture's 65-character
        # noted line measured 1912 against the column's 1884.
        (
            _set("lines.1.right", 1912.4),
            "spans 1116.0..1912.4, outside the column's 1116.0..1884.0",
        ),
        (_set("lines.0.left", 1100.0), "spans 1100.0..1461.1, outside the column's"),
        (_set("column", None), "has no column to be measured against"),
        # OPEN left where it stands with the setting off, across the section.
        (
            _set("below.0.top", 618.0),
            "ends at 718.0, 100.0 stage px into div.section-head.head-open",
        ),
        (_set("column.top", 700.0), "18.0 stage px into #stage-note below it"),
        (lambda c: c["head"].update(drawn=False), "CITATION is not headed over 2 drawn lines"),
        (_set("lines.0.color", GREY), f"is labeled in {GREY}, not its bound's {LOWER_INK}"),
        (
            _set("lines.1.color", LOWER_INK),
            f"is labeled in {LOWER_INK}, not its bound's {UPPER_INK}",
        ),
        (_set("lines.0.bound", "upper"), "source\" is labeled 'upper'"),
        # An aside the record would never compose: the check reads the words, not a flag.
        (
            _set("lines.1.note", "(unverified)"),
            "carries the note '(unverified)', which is not one aside",
        ),
        (_set("lines.1.top", 670.0), "the lower and upper citations overlap by 18.0"),
        (_set("lines.0.top", 640.0), "starts at 640.0, inside its head"),
        (
            _set("lines", []),
            "the section's lines are [], not the lower bound's then the upper's",
        ),
        # The frontier record, once per n on the head's line (the owner, 2026-09-22).
        (
            _set("record", None),
            "the head's line names the record None where it is headed: True",
        ),
        (_set("record.text", "recordN-017"), "names the record"),
        (_set("record.text", "n-017"), "names the record"),
        (
            _set("record.right", 1900.0),
            "the record 'recordn-017' ends past the column at 1900.0",
        ),
    ],
)
def test_each_citation_rule_refuses_the_section_that_breaks_it(
    change: Callable[[dict[str, Any]], None], expected: str
) -> None:
    section = copy.deepcopy(_section())
    change(section)
    found = citation_findings(section, shown=True)
    assert any(expected in item for item in found), found


def test_the_citation_section_is_built_exactly_while_its_setting_is_on() -> None:
    assert citation_findings(_section(), shown=False) == [
        "a CITATION section is built with the setting off"
    ]
    assert citation_findings(None, shown=True) == [
        "the citation setting is on and no CITATION section is built"
    ]
    headed_over_nothing = _section(lower=False, upper=False)
    headed_over_nothing["head"]["drawn"] = True
    assert citation_findings(headed_over_nothing, shown=True) == [
        "CITATION is headed over 0 drawn lines",
        "the head's line names the record None where it is headed: True",
    ]
    # A record named over nothing: the empty head's slot names no record either.
    unheaded_record = _section(lower=False, upper=False)
    unheaded_record["record"] = _section()["record"]
    assert any(
        "names the record" in item for item in citation_findings(unheaded_record, shown=True)
    )


def test_the_citation_head_is_set_in_the_heads_type() -> None:
    layer = _layer(recent=False, open_items=2)
    layer["headTypes"].insert(1, {"text": "Citation", **HEAD})
    assert facts_findings(layer) == []
    for key, value in (
        ("size", "22px"),
        ("spacing", "0px"),
        ("transform", "none"),
        ("color", GREY),
    ):
        off = copy.deepcopy(layer)
        off["headTypes"][1][key] = value
        assert any("heads are set in 2 different types" in item for item in facts_findings(off))


def test_the_sweep_measures_the_citation_section_where_it_is_hardest_to_fit() -> None:
    def cite(text: str, note: str | None = None) -> dict[str, str | None]:
        return {"text": text, "note": note, "basis": "external", "assurance": "verified"}

    entries = {
        "5": {"lower": cite("x" * 60), "upper": None},
        "17": {"lower": cite("short"), "upper": cite("y" * 50, "(reported)")},
        "18": {"lower": cite("short"), "upper": cite("z" * 55)},
        "324": {"lower": cite("w" * 66), "upper": cite("v" * 66, "(reported)")},
    }
    # Both bounds cited beats one; a noted line beats none; 324 has no step into it drawn.
    assert widest_cited(entries, last=323) == 17
    assert widest_cited(entries, last=324) == 324
    assert widest_cited({}, last=323) is None
