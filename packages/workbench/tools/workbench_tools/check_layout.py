"""Hold every workbench view to one page structure, measured in Chromium.

The stylesheet's tokens say what the layout should be; this measures what it is. At each
declared viewport, in each view a reader reaches by ordinary navigation -- Animate on a bound
that is a recent result, Animate with nothing open, the animation studio, Pack and Search -- the
`design/layout-metrics` probe reads the page's boxes, and `findings` requires:

- **no horizontal overflow**, of the document or of the controls' column;
- **one gutter**: the column's inline padding on both sides is `--layout-gutter`;
- **shared edges**: every top-level block in the column starts at the column's left content
  edge and ends at its right one, whatever the mode;
- **one stack gap**: consecutive blocks, and consecutive panels on one line of a row of
  panels, are `--layout-stack-gap` apart, no block is drawn empty (which would double the gap
  around it), and the last panel on each line ends at the row's right edge;
- **one control height per kind**: every button, select, number and text field and chip is
  `--control-height`, every tab is `--tab-height`, every segment of a group has one height, and
  a segmented group is one control tall -- or, where a narrow window wraps it, a whole number of
  segments tall inside its border;
- **no overlapping panels**;
- on the stage, **OPEN only when something is open**, **one head type** for PROVEN, CITATION
  and OPEN, and **one badge type**: every badge label, `new result` included, in the same
  family, size and weight, each in the colour its badge calls for -- the star's scarlet for
  `new result`, the label grey for every other (the owner, 2026-09-17);
- on the stage, **the CITATION section** only while its setting is on, headed only where it has
  a line and naming the n's frontier record on the head's line, its lower bound's source on the
  first line and its upper bound's on the second, each labeled in its bound's colour on the
  bound line, inside the column's two edges within `CITATION_SLACK`, and ending above OPEN and
  the legend below it (the owner, 2026-09-21 and 2026-09-22);
- on the stage, **one frame**: the catalogue's box, the trace of where it just was and the
  container Pack and the animation studio draw are all `--scene-frame-width` wide, and each is
  drawn in the colour its state calls for -- the best known side's green where the box locks
  there, the frames' grey where it does not and for the container, the lightest grey for the
  trace (the owner, 2026-09-17);
- on the stage, **the attribution** starts at the legend's left edge, within
  `ATTRIBUTION_SLACK` stage pixels (the owner, 2026-09-21), and stands one legend line under it:
  its baseline is as far below the legend's last row's as that is below the row before (the
  owner, 2026-09-22); **the shared version** stands on the same baseline, in the same type, and
  ends at the column's right edge (the owner, 2026-09-22); and both are drawn over nothing,
  including in Pack and the studio, which do not show the legend and center their drawing.
- on the stage, **the legend's math on its sentence's line**: each formula stands on the
  sentence's baseline within `LEGEND_BASELINE_SLACK`, and its letters' ink ends where the
  sentence's does within `LEGEND_INK_SLACK`, read at `LEGEND_INK_SCALE` (the owner asked for
  this four times, and each fix was judged by eye).

`findings`, `facts_findings`, `citation_findings`, `frames_findings` and `attribution_findings`
are pure functions of the probe's output, so `tests/test_check_layout.py` proves each rule
refuses a page that breaks it without a browser. One rule cannot be: `_painted` reads the
pixels once, at the narrowest viewport, because an overlay Chromium has left unpainted still
reports every box correctly.

`check_open` runs the views in a page a caller already has open, which is how `check_frontend`
adds this to a browser session it has already paid for; `check` opens its own. From `packing/`::

    uv run --frozen --all-extras --group dev python -m workbench_tools.check_layout \\
        [--page PAGE]
"""

from __future__ import annotations

import argparse
import io
import itertools
import os
import re
import tempfile
import time
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any, NamedTuple

import numpy as np
from PIL import Image
from playwright.sync_api import FloatRect, Page, sync_playwright

from workbench_tools.browser_page import open_page
from workbench_tools.build_site import build
from workbench_tools.probes import probe

#: The viewports every view is held at: a laptop, a small laptop and a phone.
VIEWPORTS: tuple[tuple[int, int], ...] = ((1440, 900), (1024, 768), (390, 844))

#: Rounding slack, in CSS pixels: boxes land on device-pixel fractions.
SLACK = 0.6

#: Control kinds held to `--control-height`; tabs are held to `--tab-height`.
AT_CONTROL_HEIGHT = frozenset({"button", "select", "input-number", "input-text", "chip"})

#: A recent result (n = 18) and an n with nothing open (n = 16).
#: It was n = 17 until T-032 adopted an external certificate there, which is exactly the
#: fact the star reports; the six that still qualify are n = 11, 12, 18, 19, 20 and 21.
STAR_N = 18
OPEN_NONE_N = 16
#: The step the one moving view is paused in. At rest the box is locked at the best known side
#: and drawn green, so a step on its way is the only place the frames' grey is drawn.
MOVING_N = 11
NEW_RESULT = "new result"

#: How far the attribution may sit from what it is set against, in stage pixels. The stage is a
#: 1920 x 1080 poster drawn at `--stage-scale`, so this is one pixel of the poster at every
#: window size rather than one device pixel at some.
ATTRIBUTION_SLACK = 1.0

#: How far a CITATION line may reach past the column's edges, and the section's foot into what
#: is set below it, in stage pixels: one pixel of the poster, as for the attribution.
CITATION_SLACK = 1.0

#: The word a citation line ends with where the register reports a bound without certifying it.
#: One aside after a reference, as `build_bound_citations.note` composes it.
NOTE = re.compile(
    r"\((reported|confirmed T-\d{3}(, T-\d{3})*|reported; confirmed T-\d{3}(, T-\d{3})*)\)"
)


def drawn_line(citation: Mapping[str, Any]) -> str:
    """A citation as the stage sets it: the reference, then its note where there is one."""
    return " ".join(part for part in (citation["text"], citation["note"]) if part)


#: What a section head's type is: all of it, since the three heads are one style.
HEAD_TYPE = ("family", "size", "weight", "spacing", "transform", "color")

#: The frontier record on the CITATION head's line: the word and the case record's name.
RECORD_LINE = re.compile(r"recordn-\d{3}")

#: How far a formula in the legend's sentence may stand from the sentence's own baseline, in
#: stage pixels: half a pixel of the poster, which is less than any offset the eye can see and
#: more than a marker's sub-pixel placement.
LEGEND_BASELINE_SLACK = 0.5

Metrics = Mapping[str, Any]


def _px(value: str | None) -> float | None:
    if value is None or not value.endswith("px"):
        return None
    return float(value[:-2])


def _near(a: float, b: float) -> bool:
    return abs(a - b) <= SLACK


def _overflow(m: Metrics) -> list[str]:
    found = []
    if m["documentWidth"] > m["viewport"]["width"] + SLACK:
        found.append(
            f"the page is {m['documentWidth']} px wide in a {m['viewport']['width']} window"
        )
    controls = m["controls"]
    if controls["scrollWidth"] > controls["clientWidth"] + SLACK:
        found.append(
            f"the controls scroll sideways: {controls['scrollWidth']} px of content in "
            f"{controls['clientWidth']}"
        )
    return found


def _edges(m: Metrics) -> list[str]:
    found = []
    controls, tokens = m["controls"], m["tokens"]
    gutter, stack = _px(tokens.get("gutter")), _px(tokens.get("stack"))
    if gutter is None or stack is None:
        found.append(
            f"the page declares no pixel --layout-gutter or --layout-stack-gap: {tokens}"
        )
    if not _near(controls["paddingLeft"], controls["paddingRight"]):
        found.append(
            f"the column's gutters differ: {controls['paddingLeft']} left, "
            f"{controls['paddingRight']} right"
        )
    found.extend(
        f"the column's {side} is {controls[side]}, not the {gutter} px gutter"
        for side in ("paddingLeft", "paddingRight")
        if gutter is not None and not _near(controls[side], gutter)
    )
    left = controls["left"] + controls["borderLeft"] + controls["paddingLeft"]
    right = controls["left"] + controls["borderLeft"] + controls["clientWidth"]
    right -= controls["paddingRight"]
    found.extend(
        f"{block['name']} spans {block['left']}..{block['right']}, not the column's "
        f"{left:.2f}..{right:.2f}"
        for block in m["blocks"]
        if not (_near(block["left"], left) and _near(block["right"], right))
    )
    # An empty block is still a flex item, so it doubles the gap around it without a gap of its
    # own ever reading wrong.
    found.extend(
        f"{block['name']} is drawn empty, and doubles the stack gap around it"
        for block in m["blocks"]
        if block["bottom"] - block["top"] <= SLACK
    )
    gaps: list[tuple[str, float]] = [
        (f"{above['name']} and {below['name']}", below["top"] - above["bottom"])
        for above, below in itertools.pairwise(m["blocks"])
    ]
    for row in m["rows"]:
        lines: dict[float, list[Mapping[str, Any]]] = {}
        for panel in row["panels"]:
            lines.setdefault(round(panel["top"]), []).append(panel)
        for line in lines.values():
            ordered = sorted(line, key=lambda panel: panel["left"])
            gaps.extend(
                (
                    f"{before['name']} and {after['name']} in {row['name']}",
                    after["left"] - before["right"],
                )
                for before, after in itertools.pairwise(ordered)
            )
            last = ordered[-1] if ordered else None
            if last is not None and not _near(last["right"], row["right"]):
                found.append(
                    f"{row['name']}'s line ends at {last['right']} ({last['name']}), "
                    f"short of the row's edge at {row['right']}"
                )
    wanted = stack if stack is not None else (gaps[0][1] if gaps else None)
    found.extend(
        f"{between} are {gap:.2f} apart, not {wanted:.2f}"
        for between, gap in gaps
        if wanted is not None and not _near(gap, wanted)
    )
    return found


def _controls(m: Metrics) -> list[str]:
    found = []
    control, tab = _px(m["tokens"].get("control")), _px(m["tokens"].get("tab"))
    if control is None or tab is None:
        found.append(
            f"the page declares no pixel --control-height or --tab-height: {m['tokens']}"
        )
    heights: dict[str, set[float]] = {}
    for item in m["controlsFound"]:
        heights.setdefault(item["kind"], set()).add(round(item["height"], 1))
        wanted = (
            control
            if item["kind"] in AT_CONTROL_HEIGHT
            else tab
            if item["kind"] == "tab"
            else None
        )
        if wanted is not None and not _near(item["height"], wanted):
            found.append(
                f"{item['kind']} {item['name']} is {item['height']} tall, not {wanted}"
            )
    found.extend(
        f"{kind} controls come in {len(values)} heights: {sorted(values)}"
        for kind, values in sorted(heights.items())
        if kind != "segmented" and max(values) - min(values) > SLACK
    )
    same = {
        kind: min(values)
        for kind, values in heights.items()
        if kind in AT_CONTROL_HEIGHT and max(values) - min(values) <= SLACK
    }
    if control is None and len(set(map(round, same.values()))) > 1:
        found.append(
            f"buttons, fields and chips are not one height: {dict(sorted(same.items()))}"
        )
    segments = heights.get("segment", set())
    height = control if control is not None else same.get("button")
    if segments and height is not None and max(segments) - min(segments) <= SLACK:
        segment = min(segments)
        border = (height - segment) / 2
        for item in m["controlsFound"]:
            if item["kind"] != "segmented":
                continue
            lines = (item["height"] - 2 * border) / segment
            if round(lines) < 1 or not _near(
                round(lines) * segment + 2 * border, item["height"]
            ):
                found.append(
                    f"segmented {item['name']} is {item['height']} tall, not a whole number of "
                    f"{segment} px segments inside a {height} px control"
                )
    return found


def _overlaps(m: Metrics) -> list[str]:
    found = []
    for a, b in itertools.combinations(m["panels"], 2):
        width = min(a["right"], b["right"]) - max(a["left"], b["left"])
        height = min(a["bottom"], b["bottom"]) - max(a["top"], b["top"])
        nested = all(
            (a[k] <= b[k] if k in ("left", "top") else a[k] >= b[k])
            for k in ("left", "top", "right", "bottom")
        ) or all(
            (b[k] <= a[k] if k in ("left", "top") else b[k] >= a[k])
            for k in ("left", "top", "right", "bottom")
        )
        if width > SLACK and height > SLACK and not nested:
            found.append(f"{a['name']} and {b['name']} overlap by {width:.1f} x {height:.1f}")
    return found


def facts_findings(layer: Metrics, *, star: bool | None = None) -> list[str]:
    """The stage panel's rules for one facts layer; `star` says whether `new result` is due."""
    found = []
    heads = [head.strip().lower() for head in layer["heads"]]
    if ("open" in heads) != (layer["openItems"] > 0):
        found.append(
            f"OPEN is {'headed' if 'open' in heads else 'not headed'} with "
            f"{layer['openItems']} open items"
        )
    head_types = {tuple(head[key] for key in HEAD_TYPE) for head in layer["headTypes"]}
    if len(head_types) > 1:
        named = {
            head["text"]: tuple(head[key] for key in HEAD_TYPE) for head in layer["headTypes"]
        }
        found.append(f"the section heads are set in {len(head_types)} different types: {named}")
    badges = layer["badges"]
    types = {(b["family"], b["size"], b["weight"]) for b in badges}
    if len(types) > 1:
        found.append(
            f"the badge labels are set in {len(types)} different types: {sorted(types)}"
        )
    # One type, two colours: `new result` is the star's scarlet and every other badge the label
    # grey, which is the one thing that tells the row's one new claim from its standing ones.
    colours = layer["colours"]
    for badge in badges:
        starred = badge["text"] == NEW_RESULT
        wanted = colours["starred"] if starred else colours["label"]
        if badge["color"] != wanted:
            role = "the star's scarlet" if starred else "the label grey"
            found.append(
                f"the `{badge['text']}` label is {badge['color']}, not {role} {wanted}"
            )
    new = [b for b in badges if b["text"] == NEW_RESULT]
    if star is True and not (len(new) == 1 and "badge-star" in (new[0]["icon"] or "").split()):
        found.append(f"a recent result has no `{NEW_RESULT}` star badge: {badges}")
    if star is False and new:
        found.append(f"`{NEW_RESULT}` is drawn where no bound is a recent result: {badges}")
    return found


def citation_findings(citations: Metrics | None, *, shown: bool) -> list[str]:
    """Every way one facts layer's CITATION section sits wrong; `shown` is the setting.

    The section is built only while the setting is on, as three fixed slots: the head, drawn
    only where a line is, then the lower bound's source and the upper bound's, each empty where
    that bound has nothing to cite. A drawn line is labeled with its bound in that bound's
    colour on the bound line, stays inside the column's two edges, and the section ends above
    what is set below it: OPEN, and the legend at the column's foot.
    """
    if not shown:
        return [] if citations is None else ["a CITATION section is built with the setting off"]
    if citations is None:
        return ["the citation setting is on and no CITATION section is built"]
    found = []
    lines = citations["lines"]
    slots = [line["slot"] for line in lines]
    if slots != ["lower", "upper"]:
        found.append(f"the section's lines are {slots}, not the lower bound's then the upper's")
    drawn = [line for line in lines if line["text"]]
    head = citations["head"]
    headed = head is not None and head["drawn"]
    if headed != bool(drawn):
        found.append(
            f"CITATION is {'headed' if headed else 'not headed'} over {len(drawn)} drawn lines"
        )
    column = citations["column"]
    # The frontier record on the head's line, once, wherever the section is headed.
    record = citations["record"]
    if headed != (record is not None) or (
        record is not None and RECORD_LINE.fullmatch(record["text"]) is None
    ):
        found.append(f"the head's line names the record {record} where it is headed: {headed}")
    elif record is not None and column is not None and record["right"] > column["right"]:
        found.append(
            f"the record {record['text']!r} ends past the column at {record['right']:.1f}"
        )
    for line in drawn:
        label = f"the {line['slot']} citation {line['text']!r}"
        if line["bound"] != line["slot"]:
            found.append(f"{label} is labeled {line['bound']!r}")
        wanted = citations["colours"][line["slot"]]
        if line["color"] != wanted:
            found.append(f"{label} is labeled in {line['color']}, not its bound's {wanted}")
        if line["note"] is not None and not NOTE.fullmatch(line["note"]):
            found.append(f"{label} carries the note {line['note']!r}, which is not one aside")
        if column is None:
            found.append(f"{label} has no column to be measured against")
        elif (
            line["left"] < column["left"] - CITATION_SLACK
            or line["right"] > column["right"] + CITATION_SLACK
        ):
            found.append(
                f"{label} spans {line['left']:.1f}..{line['right']:.1f}, outside the column's "
                f"{column['left']:.1f}..{column['right']:.1f}"
            )
        if headed and head is not None and line["top"] < head["bottom"] - CITATION_SLACK:
            found.append(f"{label} starts at {line['top']:.1f}, inside its head")
    for above, below in itertools.pairwise(drawn):
        if below["top"] < above["bottom"] - CITATION_SLACK:
            found.append(
                f"the {above['slot']} and {below['slot']} citations overlap by "
                f"{above['bottom'] - below['top']:.1f}"
            )
    parts = [*([head] if headed and head is not None else []), *drawn]
    if parts:
        foot = max(part["bottom"] for part in parts)
        under = [*citations["below"], *([{"name": "#stage-note", **column}] if column else [])]
        found.extend(
            f"the CITATION section ends at {foot:.1f}, {foot - other['top']:.1f} stage px into "
            f"{other['name']} below it"
            for other in under
            if other["top"] < foot - CITATION_SLACK
        )
    return found


def frames_findings(frames: Metrics) -> list[str]:
    """Every way the stage's outer container borders break the one-frame rule.

    Three elements draw one: the catalogue's box, the trace of where it just was under it, and
    the container Pack and the animation studio draw. All three are one width, and the colour
    is the only thing that changes -- the box is the best known side's green where it locks
    there and the frames' grey on its way, the trace is the lightest grey the page draws a line
    in, and the container is the frames' grey. Widths are read on all three whether or not they
    are drawn, because a hidden element still computes one; colours only where they are drawn.
    """
    found = []
    tokens = frames["tokens"]
    width = _px(tokens.get("width"))
    if width is None:
        found.append(f"the page declares no pixel --scene-frame-width: {tokens}")
    parts = {name: frames[name] for name in ("container", "box", "trace")}
    for name, part in parts.items():
        measured = _px(part["strokeWidth"])
        if width is None or measured is None or not _near(measured, width):
            found.append(f"the {name} frame is {part['strokeWidth']} wide, not {width} px")
    box = parts["box"]
    if box["shown"]:
        wanted = tokens["locked"] if box["locked"] else tokens["frame"]
        role = "the best known side's green" if box["locked"] else "the frames' grey"
        if box["stroke"] != wanted:
            found.append(f"the box is {box['stroke']}, not {role} {wanted}")
    if parts["trace"]["shown"] and parts["trace"]["stroke"] != tokens["trace"]:
        found.append(
            f"the trace is {parts['trace']['stroke']}, not the lightest grey {tokens['trace']}"
        )
    if parts["container"]["shown"] and parts["container"]["stroke"] != tokens["frame"]:
        found.append(
            f"the container is {parts['container']['stroke']}, not the frames' grey "
            f"{tokens['frame']}"
        )
    return found


def attribution_findings(attribution: Metrics, *, aligned: bool) -> list[str]:
    """Every way the stage's attribution and version sit wrong; `aligned` says what they are set
    against.

    The repository's address starts at the legend's left edge, and in every mode stands one
    legend line under the legend's last row, at the legend's own pitch, all read off what is
    drawn. The shared version stands on the same baseline in the same type and ends at the
    column's right edge. Pack and the animation studio do not show the legend, so there
    `aligned` is false and where the address starts is not checked, only that it is drawn and
    what it clears.
    """
    found = []
    if not (attribution["placed"] and attribution["shown"]):
        return ["the stage's attribution is not drawn"]
    # The start above is read in the overlay's own units, which are stage pixels only because
    # it is a 1920 x 1080 box over a 1920 x 1080 viewBox. That is measured, not assumed.
    poster = attribution["frame"]
    if not (
        _near(poster["left"], 0)
        and _near(poster["top"], 0)
        and _near(poster["right"], 1920)
        and _near(poster["bottom"], 1080)
    ):
        found.append(f"the attribution's overlay is not the stage's own box: {poster}")
    legend = attribution["legend"]
    ink = attribution["ink"]
    baseline = attribution["baseline"]
    if aligned:
        start = attribution["left"]
        if legend is None or start is None:
            found.append(
                f"the attribution cannot be measured against the legend: starts at {start}, "
                f"legend {legend}"
            )
        elif abs(start - legend["left"]) > ATTRIBUTION_SLACK:
            found.append(
                f"the attribution starts at {start:.2f}, {abs(start - legend['left']):.2f} "
                f"stage px from the legend's left edge at {legend['left']:.2f}"
            )
    rows = attribution["rows"]
    if len(rows) < 2 or baseline is None:
        found.append(
            f"the attribution's line cannot be measured against the legend's rows: baseline "
            f"{baseline}, rows {rows}"
        )
    else:
        pitch = rows[-1] - rows[-2]
        under = baseline - rows[-1]
        if abs(under - pitch) > ATTRIBUTION_SLACK:
            found.append(
                f"the attribution's baseline is {under:.2f} stage px under the legend's last "
                f"row, not one legend line ({pitch:.2f})"
            )
    inks = [("the attribution", ink)]
    version = attribution["version"]
    if version is None or not version["shown"] or not version["text"]:
        found.append("the shared version is not drawn on the stage")
    else:
        inks.append(("the version", version["ink"]))
        if baseline is not None and abs(version["baseline"] - baseline) > ATTRIBUTION_SLACK:
            found.append(
                f"the version stands on {version['baseline']:.2f}, not the attribution's "
                f"baseline at {baseline:.2f}"
            )
        column = attribution["column"]
        if column is None or abs(version["right"] - column["right"]) > ATTRIBUTION_SLACK:
            edge = None if column is None else column["right"]
            found.append(
                f"the version ends at {version['right']:.2f}, not the column's right edge at "
                f"{edge}"
            )
        found.extend(
            f"the version's {key} is {version[key]}, not the attribution's {attribution[key]}"
            for key in ("family", "size", "weight", "fill")
            if version[key] != attribution[key]
        )
    # What each is drawn over, and the version over the address: in the modes that center their
    # drawing the two share a line, and at a narrow enough column they would meet.
    pairs = [(what, drawn, other) for what, drawn in inks for other in attribution["obstacles"]]
    if len(inks) == 2:
        pairs.append(("the version", inks[1][1], {"name": "the attribution", **ink}))
    for what, drawn, other in pairs:
        width = min(drawn["right"], other["right"]) - max(drawn["left"], other["left"])
        height = min(drawn["bottom"], other["bottom"]) - max(drawn["top"], other["top"])
        if width > SLACK and height > SLACK:
            found.append(f"{what} is drawn over {other['name']} by {width:.1f} x {height:.1f}")
    return found


def legend_findings(legend: Metrics) -> list[str]:
    """Every formula in the legend's sentence that does not stand on the sentence's baseline.

    The owner asked four times for `s(n)` to sit on the line its sentence is set on, and each
    fix was judged by eye. This is the measurement instead: the probe reads both baselines off
    the page, and a formula more than `LEGEND_BASELINE_SLACK` off is a finding.
    """
    found = []
    if not legend["math"]:
        found.append("the legend's sentence sets no math to measure")
    for formula in legend["math"]:
        off = formula["baseline"] - legend["text"]
        if abs(off) > LEGEND_BASELINE_SLACK:
            found.append(
                f"the legend's {formula['source']} stands {off:+.2f} stage px from its "
                f"sentence's baseline at {legend['text']:.2f}"
            )
    return found


#: The device scale the legend's ink is read at. Its type is 22 stage px, so at 4x a letter's
#: lowest inked row is placed to a quarter of a poster pixel.
LEGEND_INK_SCALE = 4

#: How far a formula's letters may end from the sentence's, in stage px. Round letters dip
#: below the baseline by design, by about one and a half per cent of their size, which is a
#: third of a poster pixel here; a formula off by more than this is off by something else.
LEGEND_INK_SLACK = 0.6


def ink_bottoms(
    image: np.ndarray, glyphs: Sequence[Metrics], origin: float, scale: float
) -> list[float | None]:
    """The lowest inked row under each glyph, in image rows, or None where it drew nothing.

    A pixel is ink where it is darker than halfway from the paper to the darkest pixel in the
    picture, so the row found is where a letter's edge is half covered: the same point for a
    grey face and a black one. Only the middle of each advance box is read, because italic
    letters lean into their neighbours' columns.
    """
    darkness = image.astype(int).sum(axis=2)
    paper = int(darkness.max())
    ink = darkness < (paper + int(darkness.min())) / 2
    found: list[float | None] = []
    for glyph in glyphs:
        left = (float(glyph["left"]) - origin) * scale
        right = (float(glyph["right"]) - origin) * scale
        inset = (right - left) * 0.2
        columns = ink[:, max(0, round(left + inset)) : max(0, round(right - inset))]
        rows = np.flatnonzero(columns.any(axis=1))
        found.append(float(rows[-1] + 1) if rows.size else None)
    return found


def legend_ink_findings(
    glyphs: Sequence[Metrics], bottoms: Sequence[float | None]
) -> list[str]:
    """Every formula letter whose ink ends off the line the sentence's letters end on.

    The line is the median of the text letters' bottoms, which no single letter's overshoot
    moves. `bottoms` are in stage px.
    """
    text = [b for g, b in zip(glyphs, bottoms, strict=True) if not g["math"] and b is not None]
    if not text:
        return ["the legend's sentence has no letters to read its line from"]
    line = float(np.median(text))
    found = []
    for glyph, bottom in zip(glyphs, bottoms, strict=True):
        if not glyph["math"]:
            continue
        if bottom is None:
            found.append(f"the legend's math {glyph['char']!r} drew no ink to read")
        elif abs(bottom - line) > LEGEND_INK_SLACK:
            found.append(
                f"the legend's math {glyph['char']!r} ends {bottom - line:+.2f} stage px from "
                f"the line its sentence's letters end on"
            )
    return found


def legend_ink(page: Page) -> tuple[list[str], float]:
    """Read the legend's ink in a capture of the stage at its own size, `LEGEND_INK_SCALE` up.

    Returns the findings and the furthest a formula letter ended from the sentence's line.
    A page of its own: with the controls showing, the stage is scaled to fit beside them and
    the legend's letters are a few device pixels tall.
    """
    browser = page.context.browser
    if browser is None:
        return ["no browser to read the legend's ink in"], float("nan")
    context = browser.new_context(
        reduced_motion="reduce",
        viewport={"width": 1920, "height": 1080},
        device_scale_factor=LEGEND_INK_SCALE,
    )
    try:
        still = context.new_page()
        still.goto(page.url)
        still.wait_for_function(probe("benchmark/page-api-ready"))
        still.evaluate(probe("capture/fonts-ready"))
        still.evaluate(probe("api/apply"), {"calls": [["setCapture", True]]})
        still.evaluate(probe("design/frames"))
        read = still.evaluate(probe("design/legend-glyphs"))
        if read is None:
            return ["the legend is not drawn to read its ink"], float("nan")
        line = read["line"]
        clip: FloatRect = {
            "x": float(line["left"]),
            "y": float(line["top"]),
            "width": float(line["right"]) - float(line["left"]),
            "height": float(line["bottom"]) - float(line["top"]),
        }
        image = np.asarray(Image.open(io.BytesIO(still.screenshot(clip=clip))).convert("RGB"))
        rows = ink_bottoms(image, read["glyphs"], float(line["left"]), LEGEND_INK_SCALE)
        bottoms = [None if r is None else r / LEGEND_INK_SCALE for r in rows]
        found = legend_ink_findings(read["glyphs"], bottoms)
        text = [b for g, b in zip(read["glyphs"], bottoms, strict=True) if not g["math"] and b]
        math = [b for g, b in zip(read["glyphs"], bottoms, strict=True) if g["math"] and b]
        furthest = (
            max(abs(b - float(np.median(text))) for b in math)
            if text and math
            else float("nan")
        )
        return found, furthest
    finally:
        context.close()


#: The sum of an RGB pixel's channels under which it counts as ink rather than paper. White is
#: 765 and the attribution is set in the scene's ink, far darker, so a region of paper alone
#: never reaches it.
INK = 720


def _painted(page: Page, attribution: Metrics, what: str = "the attribution") -> list[str]:
    """The attribution, or the version on its line, is painted, not merely laid out.

    Chromium leaves this nested SVG unpainted when the transform above it changes: narrowed
    through the review viewports to 390 px, the text vanished from the picture while every box
    it reports stayed right (measured 2026-09-17). The page answers by rewriting the attributes
    both texts are placed by whenever the stage's scale moves, and nothing in the DOM shows the
    difference, so this reads the pixels instead, once, at the narrowest viewport a sweep ends
    on. `attribution` is either text's measurement: each has its own `screen` box.
    """
    screen = attribution["screen"]
    if screen["width"] <= 0 or screen["height"] <= 0:
        return [f"{what} has no box to photograph: {screen}"]
    clip: FloatRect = {
        "x": max(0.0, float(screen["x"]) - 2),
        "y": max(0.0, float(screen["y"]) - 2),
        "width": float(screen["width"]) + 4,
        "height": float(screen["height"]) + 4,
    }
    image = np.asarray(Image.open(io.BytesIO(page.screenshot(clip=clip))).convert("RGB"))
    darkest = int(image.astype(int).sum(axis=2).min())
    if darkest > INK:
        return [
            (
                f"{what} is laid out at {clip} but nothing is painted there "
                f"(darkest pixel {darkest} of 765)"
            )
        ]
    return []


def findings(m: Metrics) -> list[str]:
    """Every way one measured page breaks the layout rules."""
    return [*_overflow(m), *_edges(m), *_controls(m), *_overlaps(m)]


def _api(page: Page, *calls: list[Any]) -> Any:
    return page.evaluate(probe("api/apply"), {"calls": list(calls)})


def _stage_n(n: int) -> Callable[[Page], None]:
    """Animate paused at the start of the step into n + 1, so the first facts layer is n's."""

    def drive(page: Page) -> None:
        if _api(page, ["mode"]) != "animate":
            page.locator("#mode-animate").click()
        _api(page, ["pause"], ["setStepN", n + 1], ["seek", 0])

    return drive


def _moving(n: int) -> Callable[[Page], None]:
    """Animate paused in the step into n where the container has just finished growing.

    The box is on its way rather than resting at the best known side, so this is the one view
    that draws it in the frames' grey; everywhere else it is locked and green.
    """

    def drive(page: Page) -> None:
        if _api(page, ["mode"]) != "animate":
            page.locator("#mode-animate").click()
        schedule = _api(page, ["pause"], ["setStepN", n], ["schedule"])
        _api(page, ["seek", schedule["containerEnd"]], ["pause"])

    return drive


def _studio(page: Page) -> None:
    _stage_n(STAR_N)(page)
    page.locator("#animation-example").click()


def _leave_studio(page: Page) -> None:
    page.locator("#animation-catalogue").click()


def _cited(n: int) -> Callable[[Page], None]:
    """Animate at the step into n + 1 with the citations on, turned on by their own control."""

    def drive(page: Page) -> None:
        _stage_n(n)(page)
        page.locator("#citations-toggle").check()

    return drive


def _uncited(page: Page) -> None:
    page.locator("#citations-toggle").uncheck()


class View(NamedTuple):
    """A view the sweep measures: how to reach and leave it, the facts it must show, whether it
    shows the legend the attribution is set against, and whether its citations are on."""

    label: str
    enter: Callable[[Page], None]
    leave: Callable[[Page], None] | None
    star: bool | None
    aligned: bool
    cited: bool = False


VIEWS: tuple[View, ...] = (
    View(f"animate at n = {STAR_N}", _stage_n(STAR_N), None, star=True, aligned=True),
    View(
        f"animate at n = {OPEN_NONE_N}", _stage_n(OPEN_NONE_N), None, star=False, aligned=True
    ),
    View(f"animate mid-step into n = {MOVING_N}", _moving(MOVING_N), None, None, aligned=True),
    View("the animation studio", _studio, _leave_studio, None, aligned=False),
    View("pack", lambda page: page.locator("#mode-pack").click(), None, None, aligned=False),
    View(
        "search", lambda page: page.locator("#mode-search").click(), None, None, aligned=False
    ),
)


def widest_cited(entries: Mapping[str, Any], last: int) -> int | None:
    """The n up to `last` whose CITATION section is hardest to fit: both bounds cited, then a
    noted one, then the longest line, the reference and its note together as they are drawn."""

    def cost(n: str) -> tuple[int, int, int]:
        lines = [entries[n][bound] for bound in ("lower", "upper") if entries[n][bound]]
        noted = any(line["note"] for line in lines)
        longest = max(len(drawn_line(line)) for line in lines)
        return (len(lines), noted, longest)

    candidates = [n for n in entries if int(n) <= last]
    return int(max(candidates, key=lambda n: (*cost(n), -int(n)))) if candidates else None


def citation_views(page: Page) -> tuple[list[View], str]:
    """The citations' view, at the page's hardest n to fit, and how the summary names it.

    None where the page was built without a citation file: then the section has nothing to draw,
    and the summary says it went unmeasured rather than that it passed.
    """
    cited = page.evaluate(probe("page/citations"))
    if cited is None or cited["sha256"] is None:
        return [], "no citations in this page, so the CITATION section went unmeasured"
    if _api(page, ["mode"]) != "animate":
        page.locator("#mode-animate").click()
    last = max(int(pair["n"]) for pair in _api(page, ["pairs"]))
    n = widest_cited(cited["entries"], last)
    if n is None:
        return [], "the page's citations cite nothing it can show"
    view = View(
        f"animate at n = {n} with citations",
        _cited(n),
        _uncited,
        None,
        aligned=True,
        cited=True,
    )
    return [view], f"the CITATION section at n = {n}, its hardest to fit,"


def check_open(page: Page, viewports: Sequence[tuple[int, int]] = VIEWPORTS) -> str:
    """Measure every view at every viewport in an open page; raise with every finding.

    Leaves the page in Animate at its starting viewport.
    """
    started = time.perf_counter()
    original = page.viewport_size
    failures: list[str] = []
    measured = 0
    #: Whether the box was seen locked and seen on its way. Its two colours are one rule, and a
    #: sweep that only ever saw it at rest would pass without the frames' grey being drawn once.
    locks: set[bool] = set()
    #: Every formula offset the legend rule measured, so the summary says what it saw and not
    #: only that nothing failed: a rule that read nothing would also report nothing.
    offsets: list[float] = []
    #: Every CITATION line the sweep measured, so a sweep that turned the section on and drew
    #: nothing says so rather than passing.
    cited_lines = 0
    extra, citations_said = citation_views(page)
    for label, enter, leave, star, aligned, cited in (*VIEWS, *extra):
        enter(page)
        for width, height in viewports:
            page.set_viewport_size({"width": width, "height": height})
            page.evaluate(probe("design/frames"))
            metrics = page.evaluate(probe("design/layout-metrics"))
            measured += 1
            found = findings(metrics)
            if star is not None or cited:
                if metrics["facts"] is None:
                    found.append("the stage's facts panel is not drawn")
                else:
                    found.extend(facts_findings(metrics["facts"]["facts-a"], star=star))
            if metrics["facts"] is not None:
                for layer in ("facts-a", "facts-b"):
                    section = metrics["facts"][layer]["citations"]
                    found.extend(
                        f"{layer}: {item}" for item in citation_findings(section, shown=cited)
                    )
                    if cited and section is not None:
                        cited_lines += sum(1 for line in section["lines"] if line["text"])
            if metrics["frames"] is not None:
                found.extend(frames_findings(metrics["frames"]))
                if metrics["frames"]["box"]["shown"]:
                    locks.add(bool(metrics["frames"]["box"]["locked"]))
            if metrics["attribution"] is not None:
                found.extend(attribution_findings(metrics["attribution"], aligned=aligned))
            if metrics["legend"] is not None:
                found.extend(legend_findings(metrics["legend"]))
                offsets.extend(
                    abs(formula["baseline"] - metrics["legend"]["text"])
                    for formula in metrics["legend"]["math"]
                )
            failures.extend(f"{label} at {width} x {height}: {item}" for item in found)
        if leave is not None:
            leave(page)
    if not offsets:
        failures.append(
            "the sweep never measured the legend's math, so its baseline went unchecked"
        )
    if extra and cited_lines == 0:
        failures.append("the sweep turned the citations on and measured no CITATION line")
    if locks != {True, False}:
        failures.append(
            f"the sweep never saw the box both locked and on its way, so only one of its two "
            f"colours was measured: locked states seen {sorted(locks)}"
        )
    page.locator("#mode-animate").click()
    # The stage at its smallest, having been resized through every viewport above, which is the
    # state the overlay was found unpainted in.
    narrowest = min(viewports, key=lambda size: size[0])
    page.set_viewport_size({"width": narrowest[0], "height": narrowest[1]})
    page.evaluate(probe("design/frames"))
    smallest = page.evaluate(probe("design/layout-metrics"))["attribution"]
    if smallest is None:
        failures.append(f"no stage at {narrowest[0]} x {narrowest[1]} to photograph")
    else:
        painted = _painted(page, smallest)
        if smallest["version"] is not None:
            painted += _painted(page, smallest["version"], "the version")
        failures.extend(
            f"animate at {narrowest[0]} x {narrowest[1]}: {item}" for item in painted
        )
    ink_found, ink_furthest = legend_ink(page)
    failures.extend(
        f"the legend at 1920 x 1080, {LEGEND_INK_SCALE}x: {item}" for item in ink_found
    )
    if original is not None:
        page.set_viewport_size(original)
    if failures:
        raise ValueError("workbench layout:\n  " + "\n  ".join(failures))
    return (
        f"one gutter, edge, stack gap and control height across {len(VIEWS) + len(extra)} "
        f"views at {len(viewports)} viewports ({measured} measurements, "
        f"{time.perf_counter() - started:.1f}s), OPEN only when open, one head type, one badge "
        f"type with `{NEW_RESULT}` alone in the star's scarlet, "
        + (
            f"{citations_said} inside its column and above OPEN ({cited_lines} lines), "
            if extra
            else f"{citations_said}, "
        )
        + f"one frame width in its three colours, the attribution one legend line under the "
        f"legend at its left edge with the version on its baseline at the column's right edge, "
        f"and the legend's math on its sentence's baseline ({len(offsets)} formulas measured, "
        f"the furthest {max(offsets, default=float('nan')):.2f} stage px off; its letters' ink "
        f"{ink_furthest:.2f} stage px from the sentence's)"
    )


def check(page_path: Path) -> str:
    """Open the page in its own browser and run `check_open`."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True, executable_path=os.environ.get("SQUARES_BROWSER_EXECUTABLE")
        )
        try:
            page = browser.new_page(
                reduced_motion="reduce",
                viewport={"width": VIEWPORTS[0][0], "height": VIEWPORTS[0][1]},
            )
            open_page(page, page_path)
            page.wait_for_function(probe("benchmark/page-api-ready"))
            page.evaluate(probe("capture/fonts-ready"))
            return check_open(page)
        finally:
            browser.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("--page", type=Path, help="reuse this built index.html")
    options = parser.parse_args()
    if options.page is not None:
        print(f"OK: {check(options.page)}")
        return 0
    with tempfile.TemporaryDirectory(prefix="squares-workbench-layout-") as scratch:
        page = Path(scratch) / "workbench" / "index.html"
        build(page.parent)
        print(f"OK: {check(page)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
