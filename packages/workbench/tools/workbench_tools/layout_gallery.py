"""Photograph every workbench view at every review viewport, and compare two such sets.

A design review needs the same pictures before and after a change, taken the same way, so
this is a tool rather than a session's script. From `packing/`::

    uv run --frozen --all-extras --group dev python -m workbench_tools.layout_gallery \\
        capture --page site/workbench/index.html --out ../attic/design/after
    uv run --frozen --all-extras --group dev python -m workbench_tools.layout_gallery \\
        compare --before ../attic/design/before --after ../attic/design/after \\
        --out ../attic/design/compare.html

`capture` loads the page once per view in a reduced-motion window, drives it to the view with
the page's own controls, and writes `<view>/<width>x<height>.jpg` at each viewport. When the
controls scroll, a second picture, `<width>x<height>-end.jpg`, shows them scrolled to their
end. A view with a stage also gets `<view>/stage.png`, the stage alone in a 1920 x 1080
window, which is where a stroke a pixel or two wide can be judged: in capture preview, at the
stage's own size, where the catalogue owns the page, and with the controls showing in Pack,
whose page API has no capture preview. Beside the pictures it writes `metrics.json`: the
`design/layout-metrics` measurements of every view at every viewport, which is what
`check_layout` asserts over.

`compare` writes one self-contained HTML page with no script, grouping the two sets by view
and viewport and linking the pictures by relative path.
"""

from __future__ import annotations

import argparse
import html
import json
import os
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, Page, sync_playwright

from workbench_tools.browser_page import open_page
from workbench_tools.build_site import OUT
from workbench_tools.check_search_panel import run_plan
from workbench_tools.probes import probe

#: The review viewports, widest first: two laptops, a small laptop, a tablet and a phone.
VIEWPORTS: tuple[tuple[int, int], ...] = (
    (1440, 900),
    (1280, 800),
    (1024, 768),
    (768, 1024),
    (390, 844),
)

#: The stage's own size, the window `stage.png` is taken in.
STAGE = (1920, 1080)


def _api(page: Page, *calls: list[Any]) -> Any:
    return page.evaluate(probe("api/apply"), {"calls": list(calls)})


def _show_n(n: int) -> Callable[[Page], None]:
    """Animate paused at the end of the step into `n`, so the stage's panel describes `n`."""

    def drive(page: Page) -> None:
        duration = _api(page, ["pause"], ["setStepN", n], ["duration"])
        _api(page, ["seek", duration], ["pause"])

    return drive


def _box_moving(n: int) -> Callable[[Page], None]:
    """Animate paused in the step into `n` where its container has just finished growing.

    The catalogue's box is on its way there, drawn over the trace of where it was, so this is
    the one view that shows the box unlocked.
    """

    def drive(page: Page) -> None:
        schedule = _api(page, ["pause"], ["setStepN", n], ["schedule"])
        _api(page, ["seek", schedule["containerEnd"]], ["pause"])

    return drive


def _cited(n: int) -> Callable[[Page], None]:
    """Animate at `n` with the citations shown, which is off by default."""

    def drive(page: Page) -> None:
        duration = _api(page, ["pause"], ["setCitations", True], ["setStepN", n], ["duration"])
        _api(page, ["seek", duration], ["pause"])

    return drive


def _pack(page: Page) -> None:
    page.locator("#mode-pack").click()


def _pack_import(page: Page) -> None:
    _pack(page)
    page.locator("#pack-workspace details > summary").click()


def _search(page: Page) -> None:
    page.locator("#mode-search").click()


def _search_results(page: Page) -> None:
    _search(page)
    run_plan(page, n=5, seeds="0,1,2,3", steps=500, repair=False)


def _advanced(page: Page) -> None:
    page.locator("#motion-advanced > summary").click()


def _studio(page: Page) -> None:
    page.locator("#animation-example").click()


def _with_citations(n: int) -> Callable[[Page], None]:
    """Animate at the end of the step into `n` with the CITATION section on, by its control."""

    def drive(page: Page) -> None:
        _show_n(n)(page)
        page.locator("#citations-toggle").check()

    return drive


@dataclass(frozen=True)
class View:
    """One state a reader reaches by ordinary navigation."""

    name: str
    title: str
    drive: Callable[[Page], None]


VIEWS: tuple[View, ...] = (
    View("animate", "Animate, as the page opens", lambda _page: None),
    View("animate-star", "Animate at n = 17, a new result", _show_n(17)),
    View("animate-open-none", "Animate at n = 16, nothing open", _show_n(16)),
    # The stage both ways (the owner, 2026-09-21): n = 17 again, with its citations on.
    View("animate-citations", "Animate at n = 17 with citations", _with_citations(17)),
    View("animate-11", "Animate at n = 11", _show_n(11)),
    View("animate-cited-17", "Animate at n = 17, citations shown", _cited(17)),
    View("animate-cited-29", "Animate at n = 29, a reported upper bound cited", _cited(29)),
    View("animate-moving", "Animate into n = 11, the box on its way", _box_moving(11)),
    View("animate-advanced", "Animate with Advanced motion open", _advanced),
    View("studio", "Animate with an illustration in the studio", _studio),
    View("pack", "Pack", _pack),
    View("pack-import", "Pack with the import form open", _pack_import),
    View("search", "Search", _search),
    View("search-results", "Search after a run", _search_results),
)


def _slug(size: tuple[int, int]) -> str:
    return f"{size[0]}x{size[1]}"


def _open(
    browser: Browser, page_path: Path, size: tuple[int, int], view: View, scale: float = 1
) -> Page:
    """A fresh reduced-motion page at `size` and device `scale`, driven to `view`."""
    context = browser.new_context(
        reduced_motion="reduce",
        viewport={"width": size[0], "height": size[1]},
        device_scale_factor=scale,
    )
    page = context.new_page()
    open_page(page, page_path)
    page.wait_for_function(probe("benchmark/page-api-ready"))
    page.evaluate(probe("capture/fonts-ready"))
    view.drive(page)
    return page


def _stage_still(browser: Browser, page_path: Path, view: View, path: Path) -> None:
    """Photograph the stage alone, from a page opened at the stage's own size.

    A page of its own rather than the one the viewports were taken in: Chromium keeps drawing
    the gap bar's SVG text at the size it was last laid out at when the stage's scale grows
    under it, so a page narrowed to 390 px and widened again draws those numbers at about half
    their size, while its DOM reports the right one.
    """
    page = _open(browser, page_path, STAGE, view)
    try:
        if page.locator("#stage").is_visible():
            if _api(page, ["mode"]) == "animate":
                _api(page, ["setCapture", True])
            page.evaluate(probe("design/frames"))
            page.locator("#stage").screenshot(path=path)
    finally:
        page.context.close()


#: The device scale the legend close-up is photographed at. Its type is 22 stage px, so at 1x a
#: baseline a pixel off is one pixel of a small word, which is the size of offset the owner kept
#: seeing and a stage still cannot show; at 3x it is three.
LEGEND_SCALE = 3

#: How much of the sentence either side of a formula its close-up keeps, in stage px.
LEGEND_CONTEXT_PX = 90


def _legend_still(browser: Browser, page_path: Path, view: View, path: Path) -> None:
    """Photograph the stage's legend alone, close up, where it is shown."""
    page = _open(browser, page_path, STAGE, view, scale=LEGEND_SCALE)
    try:
        legend = page.locator("#stage-note")
        if legend.is_visible():
            # In capture the stage is drawn at its own size; with the controls showing it is
            # scaled to fit beside them, and the close-up would be of a legend half as big.
            if _api(page, ["mode"]) == "animate":
                _api(page, ["setCapture", True])
            page.evaluate(probe("design/frames"))
            legend.screenshot(path=path)
            # Each formula with the words either side of it, small enough to be seen at full
            # size: a baseline is judged against the letters beside it, not across the column.
            line = page.locator("#stage-note .note-sentence").bounding_box()
            for index, formula in enumerate(page.locator("#stage-note .note-math").all()):
                box = formula.bounding_box()
                if box is None or line is None:
                    continue
                left = max(0.0, box["x"] - LEGEND_CONTEXT_PX)
                page.screenshot(
                    path=path.with_name(f"{path.stem}-math-{index + 1}.png"),
                    clip={
                        "x": left,
                        "y": line["y"],
                        "width": box["x"] + box["width"] + LEGEND_CONTEXT_PX - left,
                        "height": line["height"],
                    },
                )
    finally:
        page.context.close()


def capture(page_path: Path, out: Path, views: tuple[View, ...] = VIEWS) -> dict[str, Any]:
    """Write every view at every viewport under `out`; return the measurements.

    Measurements of views not captured this time are kept from an earlier `metrics.json`.
    """
    recorded = out / "metrics.json"
    metrics: dict[str, dict[str, Any]] = (
        json.loads(recorded.read_text(encoding="utf-8")) if recorded.is_file() else {}
    )
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True, executable_path=os.environ.get("SQUARES_BROWSER_EXECUTABLE")
        )
        try:
            for view in views:
                page = _open(browser, page_path, VIEWPORTS[0], view)
                folder = out / view.name
                folder.mkdir(parents=True, exist_ok=True)
                metrics[view.name] = {}
                for size in VIEWPORTS:
                    page.set_viewport_size({"width": size[0], "height": size[1]})
                    page.evaluate(probe("design/scroll-controls"), {"to": "top"})
                    page.evaluate(probe("design/frames"))
                    measured = page.evaluate(probe("design/layout-metrics"))
                    metrics[view.name][_slug(size)] = measured
                    page.screenshot(path=folder / f"{_slug(size)}.jpg", type="jpeg", quality=80)
                    scrolled = page.evaluate(probe("design/scroll-controls"), {"to": "end"})
                    if scrolled["scrolls"]:
                        page.evaluate(probe("design/frames"))
                        page.screenshot(
                            path=folder / f"{_slug(size)}-end.jpg", type="jpeg", quality=80
                        )
                page.context.close()
                _stage_still(browser, page_path, view, folder / "stage.png")
                _legend_still(browser, page_path, view, folder / "legend.png")
        finally:
            browser.close()
    out.mkdir(parents=True, exist_ok=True)
    recorded.write_text(json.dumps(metrics, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return metrics


_STYLE = """
body { margin: 0; padding: 16px; font: 14px/1.4 system-ui, sans-serif; color: #17202a;
  background: #f7f8fa; }
h1 { font-size: 20px; margin: 0 0 16px; }
h2 { font-size: 16px; margin: 32px 0 8px; }
h3 { font-size: 13px; margin: 16px 0 4px; color: #47525f; font-weight: 600; }
nav a { margin-right: 12px; }
.pair { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.pair figure { margin: 0; }
.pair figcaption { font-size: 12px; color: #47525f; }
.pair img { width: 100%; height: auto; border: 1px solid #c9cfd5; background: #fff; }
.missing { padding: 24px; border: 1px dashed #c9cfd5; color: #5c6673; }
@media (max-width: 700px) { .pair { grid-template-columns: 1fr; } }
"""


def _figure(root: Path, image: Path, label: str) -> str:
    if not image.is_file():
        return f'<figure><div class="missing">no {html.escape(label)} picture</div></figure>'
    relative = os.path.relpath(image, root).replace(os.sep, "/")
    link, text = html.escape(relative), html.escape(label)
    return (
        f'<figure><figcaption>{text}</figcaption><a href="{link}">'
        f'<img loading="lazy" src="{link}" alt="{text}"></a></figure>'
    )


def compare(before: Path, after: Path, out: Path) -> Path:
    """Write the side-by-side page to `out`, linking both sets relative to it."""
    root = out.parent
    parts = [
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>Workbench layout: before and after</title>",
        f"<style>{_STYLE}</style></head><body>",
        "<h1>Workbench layout: before and after</h1><nav>",
        *(f'<a href="#{view.name}">{html.escape(view.title)}</a>' for view in VIEWS),
        "</nav>",
    ]
    for view in VIEWS:
        parts.append(f'<h2 id="{view.name}">{html.escape(view.title)}</h2>')
        first, second = before / view.name / "stage.png", after / view.name / "stage.png"
        if first.is_file() or second.is_file():
            parts.append(f"<h3>the stage at {STAGE[0]} &times; {STAGE[1]}</h3><div class=pair>")
            parts.append(_figure(root, first, "before"))
            parts.append(_figure(root, second, "after"))
            parts.append("</div>")
        for size in VIEWPORTS:
            for suffix, label in (("", ""), ("-end", ", controls scrolled to the end")):
                name = f"{_slug(size)}{suffix}.jpg"
                first, second = before / view.name / name, after / view.name / name
                if suffix and not (first.is_file() or second.is_file()):
                    continue
                parts.append(f"<h3>{size[0]} &times; {size[1]}{label}</h3><div class=pair>")
                parts.append(_figure(root, first, "before"))
                parts.append(_figure(root, second, "after"))
                parts.append("</div>")
    parts.append("</body></html>\n")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(parts), encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)
    shoot = commands.add_parser("capture", help="photograph every view at every viewport")
    shoot.add_argument("--page", type=Path, default=OUT / "index.html")
    shoot.add_argument("--out", type=Path, required=True)
    shoot.add_argument("--view", action="append", help="only these views (repeatable)")
    side = commands.add_parser("compare", help="write the before-and-after page")
    side.add_argument("--before", type=Path, required=True)
    side.add_argument("--after", type=Path, required=True)
    side.add_argument("--out", type=Path, required=True)
    options = parser.parse_args()
    if options.command == "capture":
        chosen = VIEWS
        if options.view:
            chosen = tuple(view for view in VIEWS if view.name in set(options.view))
            unknown = set(options.view) - {view.name for view in chosen}
            if unknown:
                parser.error(f"unknown views: {sorted(unknown)}")
        capture(options.page, options.out, chosen)
        print(f"OK: {len(chosen)} views at {len(VIEWPORTS)} viewports in {options.out}")
    else:
        print(f"OK: {compare(options.before, options.after, options.out)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
