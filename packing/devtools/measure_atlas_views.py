#!/usr/bin/env python3
"""Measure the homepage's atlas in its two views and three sizes, and the move between
layouts.

The atlas is one set of tiles, a drawing of the best packing known for each case, that
the reader sets as a grid or as a triangle (`templates/paper-design.md`, Atlas views),
at a size of tile, Small, Medium or Large (`overview/atlas-view.js`). A tile carries its
centered case number. Selected derived
drawings are shown directly, without layer labels.
The triangle keeps each complete row of 2k - 1 cases, ending at k squared, aligned to
a common right edge. Its scroll frame pans wide rows at the same drawing scale as Grid.
This opens a built overview in Chromium and reports what the
browser made of that:

- `layout` reports each view at each width, with the first hundred cases and with all of
  them: the block's width, how many tiles a line holds, a tile's and a drawing's width,
  the size of a tile's number, how many lines the tiles take and how tall they stand, and
  the rows that wrap. With them it reports what a layout may not do (`layout_problems`):
  run past the window, set a tile outside the block or over another, break the order of
  the cases, cut a row into lines other than `row_lines` gives, or start any Triangle
  row away from the canvas's right edge. Each layout is read at each size (`SIZES`), and
  count centering is checked by `mark_problems`. The probe also records actual
  enclosing-outline and count-ink bounds; `ink_clearances` measures ordinary horizontal
  gaps and the deepest count's clearance above the next drawing. Obsolete stars and
  layer badges are still reported so tests can refuse them.
  `--markdown` prints one line a layout.
- `move` times each change of layout (`CHANGES`: to the triangle and back, with a hundred
  cases and with all, the expander's change in the triangle, and changes of size in each
  view), `--runs` times each:
  how long the script's handler ran, how many tiles moved, how long the move lasted, the
  animation frames the page was given and the ones the main thread missed, every long
  task, and Chromium's own counters over the change, the time in script, in layout and
  in style, and how many layouts it made (the DevTools protocol's
  `Performance.getMetrics`). The counters are the main thread's own processor time,
  not the clock's, so a busy machine does not lengthen them; the handler's time, the
  move's and the frames are the clock's and it does. `--markdown` prints one line a
  change, the median of the runs, or with `--stat best` the least of them, which is
  the nearest a busy machine comes to the change's own cost. Watching the frames makes
  the main thread produce one at every refresh and restyle every moving tile in it,
  work the compositor otherwise does alone; `--unwatched` asks for no frame, and the
  counters then show what a reader's browser does.
- `shots` writes pictures to `--out`: the atlas block in each view at each width, in the
  light theme and the dark, with a hundred cases and with all, at each size (the
  pictures at Medium and Large end `-medium` and `-large`); the two actions under a
  table and under the grid, "See all results" and the expander collapsed and expanded,
  at each width in both themes; and the window at five points of the move from the grid
  to the triangle (0, 25, 50, 75 and 100 percent).

`PAGE` is a built `index.html`, or a directory `preview_site` built. `--render` renders
the overview alone into `PAGE` first, which takes seconds where a whole site takes a
minute. Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python -m devtools.measure_atlas_views \
        layout PAGE --render --markdown
    uv run --frozen --all-extras --group dev python -m devtools.measure_atlas_views \
        move PAGE --width 1280 --runs 5 --markdown
    uv run --frozen --all-extras --group dev python -m devtools.measure_atlas_views \
        shots PAGE --out DIR

Set `SQPACK_CHROMIUM` to use a browser the environment supplies, as the other tools do.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import statistics
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from devtools.render_n11_lower_bounds_explainer_pdf import BROWSER_OVERRIDE
from sqpack.probes import probe

PROBES = Path(__file__).resolve().parent / "probes"
LAYOUT = probe(PROBES, "measure_atlas_views/layout")
MOVE = probe(PROBES, "measure_atlas_views/move")
HOLD = probe(PROBES, "measure_atlas_views/hold")
SETTLED = probe(PROBES, "measure_atlas_views/settled")
TOP = probe(PROBES, "measure_atlas_views/top")
QUIET = probe(PROBES, "measure_atlas_views/quiet")

MODES = ("layout", "move", "shots")
VIEWS = ("grid", "triangle")
#: The atlas's three sizes of tile, in tab order: the key `?size=` takes. The drawing
#: tabs, House and Regularized, that stood here as `LAYERS` went on 2026-10-04
#: (think-k8x9).
SIZES = ("small", "medium", "large")
#: The size a plain address opens at, which `?size=` does not name.
DEFAULT_SIZE = "small"
SCALES = ("fixed", "row", "global")
DEFAULT_SCALE = "fixed"
WIDTHS = (1280, 1024, 768, 390)
SCHEMES = ("light", "dark")
#: The points of a move a picture is taken at, as shares of its duration.
FRACTIONS = (0.0, 0.25, 0.5, 0.75, 1.0)
#: The windows the move is pictured in, each with the hundred and with every case: a
#: desktop tall enough to hold the whole triangle under its heading, and a phone.
FRAME_WINDOWS = ((1280, 1200), (390, 844))
#: How far two edges may differ and still be one edge, in CSS pixels.
EDGE = 0.75
EXPANDER = "[data-atlas-toggle]"
BLOCK = "[data-atlas-grid]"
#: How long the page must go without a long task before a change is timed, and the
#: longest that is waited for, in milliseconds (the `quiet` probe).
CALM_MS, CALM_MOST_MS = 1000, 30_000
#: Chromium's counters a change is read between, as `Performance.getMetrics` names them,
#: each with the name it is reported under: four times, in seconds, and two counts.
COUNTERS = {
    "ScriptDuration": "script_ms",
    "LayoutDuration": "layout_ms",
    "RecalcStyleDuration": "style_ms",
    "TaskDuration": "task_ms",
}
COUNTS = {"LayoutCount": "layouts", "RecalcStyleCount": "style_recalcs"}


def tab(view: str) -> str:
    """The selector of a view's tab."""
    if view not in VIEWS:
        raise ValueError(f"the atlas has no view {view!r}")
    return f'[data-atlas-tab="{view}"]'


def size_tab(size: str) -> str:
    """The selector of a size's tab."""
    if size not in SIZES:
        raise ValueError(f"the atlas has no size {size!r}")
    return f'[data-atlas-size-tab="{size}"]'


#: The presses `move` makes on one page, in order: what the change is called, how many
#: cases show once it is made, and the control pressed. A change with no name is made
#: and not timed: it only sets the page up for the next. The first two are such a pair,
#: to the triangle and back. A first change of view brings the sections under the atlas
#: nearer the window, and the page then typesets their math and loads the pages its
#: cards frame, once, on the same thread; that is the page's work and not the move's,
#: so it is done before anything is timed. A change of size is timed in each view, from
#: Medium to Large and on to Small, and the page is put back at Medium after.
CHANGES: tuple[tuple[str | None, int, str], ...] = (
    (None, 100, tab("triangle")),
    (None, 100, tab("grid")),
    ("grid to triangle", 100, tab("triangle")),
    ("triangle to grid", 100, tab("grid")),
    ("grid, medium to large", 100, size_tab("large")),
    ("grid, large to small", 100, size_tab("small")),
    (None, 100, size_tab("medium")),
    (None, 324, EXPANDER),
    ("grid to triangle", 324, tab("triangle")),
    ("triangle to grid", 324, tab("grid")),
    (None, 100, EXPANDER),
    (None, 100, tab("triangle")),
    ("triangle, 100 to 324", 324, EXPANDER),
    ("triangle, medium to large", 324, size_tab("large")),
    ("triangle, large to small", 324, size_tab("small")),
    (None, 324, size_tab("medium")),
)


def row_of(n: int) -> int:
    """The triangle's row for case `n`: the k with (k - 1)^2 < n <= k^2."""
    if n < 1:
        raise ValueError(f"no case n = {n}")
    return math.isqrt(n - 1) + 1


def is_square(n: int) -> bool:
    """Whether `n` is a perfect square, the last case of its row."""
    return n >= 1 and math.isqrt(n) ** 2 == n


def row_lines(k: int, per: int, _first_grid: int | None = None) -> tuple[int, ...]:
    """One complete bound row, independent of viewport capacity and grid threshold."""
    if k < 1 or per < 1:
        raise ValueError(f"no row {k} at {per} a line")
    return (2 * k - 1,)


def _lines(tiles: Sequence[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    """The tiles by line, top to bottom, each line left to right."""
    lines: dict[float, list[dict[str, Any]]] = {}
    for tile in tiles:
        top = next((top for top in lines if abs(top - tile["top"]) <= EDGE), tile["top"])
        lines.setdefault(top, []).append(tile)
    return [sorted(lines[top], key=lambda tile: tile["left"]) for top in sorted(lines)]


def layout_problems(report: dict[str, Any]) -> list[str]:
    """What is wrong with a settled layout, in either view: the page runs past the
    window, a tile stands outside the block or over another, or the cases are out of
    order reading left to right and top to bottom. In the triangle also: a row cut into
    lines other than `row_lines` gives, a row off the right edge of the pannable canvas,
    or a segment separator unlike half a drawing."""
    problems: list[str] = []
    tiles: list[dict[str, Any]] = report["tiles"]
    if not tiles:
        return ["no tile shows"]
    if report["moving"]:
        problems.append(f"{report['moving']} tiles are still in a move")
    if report["overflow"] > 0:
        problems.append(f"the page runs {report['overflow']}px past the window")
    cells = (
        report.get("canvas", report["cells"])
        if report["view"] == "triangle"
        else report["cells"]
    )
    outside = [
        tile["n"]
        for tile in tiles
        if tile["left"] < cells["left"] - EDGE or tile["right"] > cells["right"] + EDGE
    ]
    if outside:
        problems.append(f"tiles outside the block: {outside[:8]}")
    lines = _lines(tiles)
    for line in lines:
        for left, right in itertools.pairwise(line):
            if left["right"] > right["left"] + EDGE:
                problems.append(f"n = {left['n']} runs over n = {right['n']}")
    for upper, lower in itertools.pairwise(lines):
        if max(tile["bottom"] for tile in upper) > min(tile["top"] for tile in lower) + EDGE:
            problems.append(f"the line of n = {upper[0]['n']} runs over the next")
    reading = [tile["n"] for line in lines for tile in line]
    if reading != sorted(reading):
        problems.append("the cases are out of order")
    problems.extend(mark_problems(report))
    if report["view"] != "triangle":
        return problems
    per = report["per_line"]
    if not per:
        return [*problems, "the triangle has no tiles to a line"]
    last = max(reading)
    starts = {row_of(tile["n"]): tile["n"] for tile in tiles if tile.get("grid_from")}
    by_row: dict[int, list[list[int]]] = {}
    for line in lines:
        k = row_of(line[0]["n"])
        by_row.setdefault(k, []).append([tile["n"] for tile in line])
        if len({row_of(tile["n"]) for tile in line}) > 1:
            problems.append(f"the line of n = {line[0]['n']} holds two rows")
        if abs(line[-1]["right"] - cells["right"]) > EDGE:
            problems.append(f"row {k}'s line of n = {line[0]['n']} misses the right edge")
    for k, found in sorted(by_row.items()):
        if k * k > last:
            continue
        sizes = tuple(len(line) for line in found)
        expected = row_lines(k, per, starts.get(k))
        if sizes != expected:
            problems.append(f"row {k} is set {sizes}, not {expected}")
    if "gap_px" in report:
        for line in lines:
            for left, right in itertools.pairwise(line):
                expected_gap = report["gap_px"]
                if right.get("grid_from"):
                    expected_gap += (
                        right.get("drawing_slot_width", right["drawing"]["width"]) / 2
                    )
                gap = right["left"] - left["right"]
                if abs(gap - expected_gap) > EDGE:
                    problems.append(
                        f"the gap before n = {right['n']} is {gap}px, not {expected_gap}px"
                    )
    return problems


#: A tile's two marks, by the key the layout probe reports each under: the new-result
#: star, hung past the number's end, and the regularized layer's badge, hung before its
#: start. The badge hung past the end, alone, until the star took that side on 2026-10-04.
MARKS = {"star": ("star", "after"), "mark": ("badge", "before")}


def mark_problems(report: dict[str, Any]) -> list[str]:
    """What is wrong with the marks a settled layout's tiles carry: a star that runs
    over its number or stands outside its tile, a badge that does either, a mark with no
    size, and a number off its tile's centre, where the marks would have pushed it. A
    tile reported with no number's box, as from a page older than its marks, has none of
    these to check. Which tiles carry which marks is the page's record, not the layout's
    (`test_site_atlas_views` holds it to the case records)."""
    problems: list[str] = []
    for tile in report["tiles"]:
        n, number = tile["n"], tile.get("number_box")
        if number is None:
            continue
        for key, (name, side) in MARKS.items():
            mark = tile.get(key)
            if mark is None:
                continue
            if mark["width"] <= 0 or mark["height"] <= 0:
                problems.append(f"n = {n}'s {name} has no size")
                continue
            over = (
                mark["left"] < number["right"] - EDGE
                if side == "after"
                else mark["right"] > number["left"] + EDGE
            )
            if over:
                problems.append(f"n = {n}'s {name} runs over its number")
            if (
                mark["left"] < tile["left"] - EDGE
                or mark["right"] > tile["right"] + EDGE
                or mark["top"] < tile["top"] - EDGE
                or mark["bottom"] > tile["bottom"] + EDGE
            ):
                problems.append(f"n = {n}'s {name} stands outside its tile")
        centre = (number["left"] + number["right"]) / 2
        if abs(centre - (tile["left"] + tile["right"]) / 2) > 2 * EDGE:
            problems.append(f"n = {n}'s number is off its tile's centre")
    return problems


def ink_clearances(report: dict[str, Any]) -> dict[str, tuple[float, float]]:
    """Measured outline gaps and deepest count-ink gaps, excluding grid separators."""
    lines = _lines(report["tiles"])
    horizontal = [
        after["outline"]["left"] - before["outline"]["right"]
        for line in lines
        for before, after in itertools.pairwise(line)
        if before.get("outline")
        and after.get("outline")
        and not (report["view"] == "triangle" and after.get("grid_from"))
    ]
    vertical = [
        min(tile["outline"]["top"] for tile in after)
        - max(tile["number_ink"]["bottom"] for tile in before)
        for before, after in itertools.pairwise(lines)
        if all(tile.get("number_ink") for tile in before)
        and all(tile.get("outline") for tile in after)
    ]
    return {
        name: (min(gaps), max(gaps))
        for name, gaps in (("horizontal", horizontal), ("vertical", vertical))
        if gaps
    }


def summary(report: dict[str, Any]) -> dict[str, Any]:
    """One layout in a line: its sizes, its lines and the rows that wrap."""
    tiles: list[dict[str, Any]] = report["tiles"]
    lines = _lines(tiles)
    rows: dict[int, int] = {}
    for line in lines:
        rows[row_of(line[0]["n"])] = rows.get(row_of(line[0]["n"]), 0) + 1
    wrapped = [k for k, count in sorted(rows.items()) if count > 1]
    widths = sorted({round(tile["width"], 1) for tile in tiles})
    drawings = sorted({round(tile["drawing"]["width"], 1) for tile in tiles if tile["drawing"]})
    return {
        "view": report["view"],
        "size": report.get("size"),
        "scale": report.get("scale", DEFAULT_SCALE),
        "shown": len(tiles),
        "starred": sum(tile.get("star") is not None for tile in tiles),
        "ink_clearances": ink_clearances(report),
        "badged": sum(tile.get("mark") is not None for tile in tiles),
        "block": report["cells"]["width"],
        "per_line": report["per_line"] if report["view"] == "triangle" else len(lines[0]),
        "tile": widths[0] if len(widths) == 1 else f"{widths[0]}-{widths[-1]}",
        "drawing": drawings[0] if len(drawings) == 1 else f"{drawings[0]}-{drawings[-1]}",
        "number_px": min(tile["number_px"] for tile in tiles),
        "lines": len(lines),
        "height": report["cells"]["height"],
        "wrapped": wrapped if report["view"] == "triangle" else [],
        "problems": layout_problems(report),
    }


def launch(driver: Any) -> Any:
    return driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))


def settle(page: Any) -> None:
    """Wait until the tiles are placed and none is in a move."""
    page.wait_for_function(SETTLED)


def query_for(view: str, size: str = DEFAULT_SIZE, scale: str = DEFAULT_SCALE) -> str:
    """The query string that asks for `view` and `size`: nothing for Triangle at Small,
    the defaults."""
    if view not in VIEWS:
        raise ValueError(f"the atlas has no view {view!r}")
    if size not in SIZES:
        raise ValueError(f"the atlas has no size {size!r}")
    if scale not in SCALES:
        raise ValueError(f"the atlas has no scale {scale!r}")
    params = [
        *(["atlas=grid"] if view == "grid" else []),
        *([f"size={size}"] if size != DEFAULT_SIZE else []),
        *([f"scale={scale}"] if scale != DEFAULT_SCALE else []),
    ]
    return f"?{'&'.join(params)}" if params else ""


def open_atlas(
    browser: Any,
    address: str,
    *,
    width: int,
    view: str = "triangle",
    size: str = DEFAULT_SIZE,
    scale: str = DEFAULT_SCALE,
    query: str | None = None,
    scheme: str = "light",
    height: int = 900,
    reduced_motion: str | None = None,
    init_script: str | None = None,
) -> Any:
    """A page showing the atlas in `view` at `size`, asked for in the address, with its
    tiles placed and the block in the window. `query` is the whole of what follows the page's
    name instead, a query string and any fragment, for an address that says more, and
    `init_script` a script the page runs before any of its own."""
    page = browser.new_page(
        viewport={"width": width, "height": height},
        color_scheme=scheme,
        reduced_motion=reduced_motion,
    )
    if init_script is not None:
        page.add_init_script(init_script)
    page.goto(
        address + (query_for(view, size, scale) if query is None else query), wait_until="load"
    )
    page.locator(BLOCK).scroll_into_view_if_needed()
    settle(page)
    return page


def expand(page: Any) -> None:
    """Show every case, as the reader does: press the expander and let the move end."""
    page.locator(EXPANDER).click()
    settle(page)


def top(page: Any) -> int | None:
    """Scroll the page so The Atlas, its heading, starts at the window's top edge, as a
    reader who has just reached the section has it; returns where the heading then
    stands (the `top` probe)."""
    return page.evaluate(TOP)


def layout(page: Any) -> dict[str, Any]:
    """The atlas as the page lays it out now (the `layout` probe)."""
    report = page.evaluate(LAYOUT)
    if report is None:
        raise SystemExit("the page has no atlas with its tiles placed")
    return report


def measure_layout(
    address: str, widths: Sequence[int], sizes: Sequence[str] = SIZES
) -> list[dict[str, Any]]:
    """Each view at each width at each size, with a hundred cases and with all."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    rows: list[dict[str, Any]] = []
    with sync_playwright() as driver:
        browser = launch(driver)
        for width in widths:
            for view in VIEWS:
                for size in sizes:
                    page = open_atlas(browser, address, width=width, view=view, size=size)
                    rows.append({"width": width, **summary(layout(page))})
                    expand(page)
                    rows.append({"width": width, **summary(layout(page))})
                    page.close()
        browser.close()
    return rows


def _counters(client: Any) -> dict[str, float]:
    metrics = client.send("Performance.getMetrics")["metrics"]
    found = {metric["name"]: metric["value"] for metric in metrics}
    return {name: found[name] for name in (*COUNTERS, *COUNTS)}


def timed(page: Any, client: Any, press: str, *, frames: bool = True) -> dict[str, Any]:
    """One change made by pressing `press`, with the page's own report (the `move`
    probe) and Chromium's counters over it, the times in milliseconds. With `frames`
    false the probe asks for no animation frame while the tiles move, so the counters
    are the main thread's work when nothing watches it."""
    before = _counters(client)
    report = page.evaluate(MOVE, {"press": press, "frames": frames})
    if report is None:
        raise SystemExit(f"the page has no {press}")
    after = _counters(client)
    for name, label in COUNTERS.items():
        report[label] = round((after[name] - before[name]) * 1000, 2)
    for name, label in COUNTS.items():
        report[label] = round(after[name] - before[name])
    return report


def measure_move(
    address: str, widths: Sequence[int], runs: int, *, frames: bool = True
) -> list[dict[str, Any]]:
    """Every named change of `CHANGES`, `runs` times at each width, each run on a page
    of its own opened in the grid with The Atlas at the top of the window. `frames`
    false watches no animation frame (`timed`)."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    rows: list[dict[str, Any]] = []
    with sync_playwright() as driver:
        browser = launch(driver)
        for width in widths:
            for run in range(runs):
                page = open_atlas(browser, address, width=width, view="grid", size="medium")
                top(page)
                client = page.context.new_cdp_session(page)
                client.send("Performance.enable", {"timeDomain": "threadTicks"})
                for change, shown, press in CHANGES:
                    if change is None:
                        page.locator(press).click()
                        settle(page)
                        continue
                    # What the page loads and typesets as it scrolls shares this
                    # thread: let it finish, so a move is timed alone.
                    page.evaluate(QUIET, {"calm": CALM_MS, "most": CALM_MOST_MS})
                    # The control is in the window when a reader presses it: the tabs
                    # with the section's heading at the top, the expander wherever it is.
                    if press == EXPANDER:
                        page.locator(press).scroll_into_view_if_needed()
                    else:
                        top(page)
                    report = timed(page, client, press, frames=frames)
                    rows.append(
                        {"width": width, "change": change, "shown": shown, "run": run, **report}
                    )
                page.close()
        browser.close()
    return rows


def medians(rows: Sequence[dict[str, Any]], *, best: bool = False) -> list[dict[str, Any]]:
    """The runs of each change at each width as one line: the median of every number,
    or with `best` the least, and the most long tasks any run had."""
    pick = min if best else statistics.median
    groups: dict[tuple[int, str, int], list[dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault((row["width"], row["change"], row["shown"]), []).append(row)
    lines: list[dict[str, Any]] = []
    for (width, change, shown), group in groups.items():
        line: dict[str, Any] = {
            "width": width,
            "change": change,
            "shown": shown,
            "runs": len(group),
        }
        for name, value in group[0].items():
            if isinstance(value, (int, float)) and name not in {"width", "shown", "run"}:
                line[name] = round(pick(row[name] for row in group), 2)
        line["long_tasks"] = max(len(row["long_tasks"]) for row in group)
        lines.append(line)
    return lines


#: The two actions under a table and under the grid, as `shots` pictures them: the row
#: of "See all results", and the expander's row, collapsed and expanded.
ACTIONS = (("see-all", ".site-more"), ("expander", ".site-atlas-toggle-row"))


def shots(address: str, out: Path, widths: Sequence[int]) -> list[Path]:
    """The atlas block in each view at each width, light and dark, with a hundred cases
    and with all, at each size; the two actions (`ACTIONS`) at each width in both
    themes, the expander collapsed and expanded; then the window at each of `FRACTIONS`
    of the move to the triangle."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    out.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    with sync_playwright() as driver:
        browser = launch(driver)
        for scheme in SCHEMES:
            for width in widths:
                for view in VIEWS:
                    for size in (size for size in SIZES if size != DEFAULT_SIZE):
                        page = open_atlas(
                            browser, address, width=width, view=view, size=size, scheme=scheme
                        )
                        for shown in (100, 324):
                            if shown == 324:
                                expand(page)
                            target = out / f"atlas-{view}-{shown}-{width}-{scheme}-{size}.png"
                            page.locator(BLOCK).screenshot(path=str(target))
                            written.append(target)
                        page.close()
                    page = open_atlas(browser, address, width=width, view=view, scheme=scheme)
                    for shown in (100, 324):
                        if shown == 324:
                            expand(page)
                        target = out / f"atlas-{view}-{shown}-{width}-{scheme}.png"
                        page.locator(BLOCK).screenshot(path=str(target))
                        written.append(target)
                        if view != "grid":
                            continue
                        for name, selector in ACTIONS:
                            if name == "see-all" and shown == 324:
                                continue
                            state = (
                                ""
                                if name == "see-all"
                                else ("-less" if shown == 324 else "-more")
                            )
                            target = out / f"action-{name}{state}-{width}-{scheme}.png"
                            page.locator(selector).screenshot(path=str(target))
                            written.append(target)
                    page.close()
        for width, height in FRAME_WINDOWS:
            for shown in (100, 324):
                page = open_atlas(browser, address, width=width, height=height, view="grid")
                if shown == 324:
                    expand(page)
                top(page)
                page.locator(tab("triangle")).click()
                for fraction in FRACTIONS:
                    page.evaluate(HOLD, {"fraction": fraction})
                    target = out / f"move-{shown}-{width}-{round(fraction * 100):03d}.png"
                    page.screenshot(path=str(target))
                    written.append(target)
                page.close()
        browser.close()
    return written


def markdown_table(rows: Sequence[dict[str, Any]]) -> str:
    """The rows as a Markdown table, one column a key."""
    if not rows:
        return ""
    names = list(rows[0])
    lines = ["| " + " | ".join(names) + " |", "|" + " --- |" * len(names)]
    for row in rows:
        cells = (
            ", ".join(str(item) for item in row[name]) or "none"
            if isinstance(row[name], list)
            else str(row[name])
            for name in names
        )
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def page_address(target: Path, *, render: bool) -> str:
    """The address of the overview at `target`, a built `index.html` or the directory
    that holds one; with `render`, the overview is rendered there first."""
    path = target / "index.html" if target.is_dir() or target.suffix != ".html" else target
    if render:
        from devtools import render_overview  # noqa: PLC0415

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_overview.PAGES["index.html"]().html, encoding="utf-8")
    if not path.is_file():
        raise SystemExit(f"no built overview at {path}; pass --render to write one")
    return path.resolve().as_uri()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("mode", choices=MODES)
    parser.add_argument("page", type=Path, help="a built index.html, or its directory")
    parser.add_argument("--render", action="store_true", help="render the overview there first")
    parser.add_argument("--width", type=int, action="append", help="window width; repeatable")
    parser.add_argument("--runs", type=int, default=5, help="move: how many times each change")
    parser.add_argument(
        "--unwatched",
        action="store_true",
        help="move: ask for no animation frame while the tiles move, so the counters "
        "show the main thread's work when nothing watches it; the frame numbers are zero",
    )
    parser.add_argument(
        "--stat",
        choices=("median", "best"),
        default="median",
        help="move, with --markdown: the median of the runs, or the least",
    )
    parser.add_argument("--out", type=Path, help="shots: where the pictures go")
    parser.add_argument("--markdown", action="store_true", help="print a table, not JSON")
    args = parser.parse_args(argv)
    address = page_address(args.page, render=args.render)
    widths = tuple(args.width or WIDTHS)
    if args.mode == "shots":
        if args.out is None:
            parser.error("shots needs --out")
        for target in shots(address, args.out.resolve(), widths):
            print(f"shot {target}")
        return 0
    if args.mode == "move":
        rows = measure_move(address, widths, args.runs, frames=not args.unwatched)
        report = medians(rows, best=args.stat == "best") if args.markdown else rows
    else:
        report = measure_layout(address, widths)
    print(markdown_table(report) if args.markdown else json.dumps(report, indent=2))
    failed = [row for row in report if row.get("problems")]
    for row in failed:
        where = f"{row['width']}, {row['view']}, {row.get('size')}, {row['shown']}"
        print(f"problem at {where}: {row['problems']}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
