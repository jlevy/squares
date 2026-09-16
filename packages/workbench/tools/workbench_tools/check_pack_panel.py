"""Exercise the independent Pack panel on a built, deployable workbench page."""

from __future__ import annotations

import argparse
import json
import math
import os
import tempfile
from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, Page, sync_playwright

from workbench_tools.build_site import build
from workbench_tools.probes import probe

#: Chords that belong to the browser or the system, pressed with a square focused. Each
#: names a key the Pack map does handle bare, so a missing guard shows as a change.
SQUARE_CHORDS = (
    "Alt+ArrowLeft",
    "Control+ArrowLeft",
    "Meta+ArrowRight",
    "Alt+ArrowUp",
    "Control+KeyQ",
    "Meta+KeyE",
    "Meta+BracketRight",
    "Meta+BracketLeft",
    "Control+PageDown",
    "Control+PageUp",
    "Alt+Escape",
)

#: The same, pressed with the stage itself focused, where Enter and Space are Pack's.
STAGE_CHORDS = ("Control+Enter", "Meta+Enter", "Alt+Enter", "Control+Space", "Alt+Space")

#: Mutations of live regions allowed across a second of Run: the Run press itself may be
#: announced, a frame may not. At 60 frames a second a per-frame write is far above it.
LIVE_MUTATION_LIMIT = 3


def _require(condition: bool, message: str) -> None:  # noqa: FBT001
    if not condition:
        raise ValueError(message)


def _look(page: Page, name: str, /, **argument: Any) -> Any:
    """Evaluate one checked probe, passing values through Playwright's data channel."""
    return page.evaluate(probe(name), argument or None)


def _seeded_run(page: Page, index: int) -> dict[str, Any]:
    """Restore the default grid start and advance it, so a reset of the run is visible."""
    page.locator("#pack-reset").click()
    _look(page, "pack/apply", calls=[["step", 25]])
    run = _look(page, "pack/run", index=index)
    _require(
        run["latest"] and run["steps"] == 25 and run["startControl"] == "grid",
        f"Pack did not reach a 25-step seeded run to test against: {run}",
    )
    return run


def _unfocused(run: dict[str, Any]) -> dict[str, Any]:
    return {**run, "focus": None}


def _check_modifier_chords(page: Page) -> None:
    """A Pack shortcut is a bare key: Ctrl, Meta and Alt chords leave the run alone."""
    before = _seeded_run(page, 0)
    page.locator("#stage").focus()
    page.keyboard.press("Enter")
    focused = _look(page, "pack/run", index=0)
    _require(
        focused["focus"] == "0" and _unfocused(focused) == _unfocused(before),
        f"Enter did not focus Pack square 1 and leave the run alone: {focused}",
    )
    for chord in SQUARE_CHORDS:
        page.keyboard.press(chord)
        after = _look(page, "pack/run", index=0)
        _require(
            after == focused,
            f"{chord} with a square focused was taken as a Pack shortcut: "
            f"{focused} became {after}",
        )
    # The positive control, and the capital case the square's label promises.
    page.keyboard.press("Shift+KeyE")
    rotated = _look(page, "pack/run", index=0)
    _require(
        abs(rotated["angle"] - focused["angle"] - math.pi / 36) < 1e-12
        and rotated["startControl"] == "given",
        f"Shift+E did not rotate the focused square by five degrees: {rotated}",
    )
    page.keyboard.press("Escape")
    at_stage = _look(page, "pack/run", index=0)
    _require(at_stage["focus"] == "stage", f"Escape did not return to the stage: {at_stage}")
    for chord in STAGE_CHORDS:
        page.keyboard.press(chord)
        after = _look(page, "pack/run", index=0)
        _require(
            after == at_stage,
            f"{chord} on the stage was taken as a Pack shortcut: {at_stage} became {after}",
        )


def _check_click_keeps_run(page: Page) -> None:
    """Pressing a square without moving it keeps the run; a drag still edits it."""
    before = _seeded_run(page, 3)
    centre = _look(page, "pack/square-centre", index=3)
    page.mouse.click(centre["x"], centre["y"])
    clicked = _look(page, "pack/run", index=3)
    _require(
        _unfocused(clicked) == _unfocused(before),
        f"a click without a drag changed the Pack run: {before} became {clicked}",
    )
    page.mouse.move(centre["x"], centre["y"])
    page.mouse.down()
    page.mouse.move(centre["x"] + 40, centre["y"], steps=4)
    page.mouse.up()
    dragged = _look(page, "pack/run", index=3)
    _require(
        dragged["x"] > clicked["x"]
        and not dragged["latest"]
        and dragged["startControl"] == "given",
        f"a drag did not commit its edit: {clicked} became {dragged}",
    )


def _check_non_packings_labelled(page: Page) -> None:
    """An import that is not a packing is never shown as one, in the status or on the stage."""
    touching = [{"x": 0.5, "y": 0.5, "angle": 0}, {"x": 1.5, "y": 0.5, "angle": 0}]
    cases = (
        (
            "half-size squares",
            {
                "squareSide": 0.5,
                "container": {"originX": 0, "originY": 0, "side": 1},
                "poses": [
                    {"x": 0.25, "y": 0.25, "angle": 0},
                    {"x": 0.75, "y": 0.25, "angle": 0},
                ],
            },
            "not unit squares",
        ),
        (
            "a 5e-9 overlap",
            {
                "squareSide": 1,
                "container": {"originX": 0, "originY": 0, "side": 2},
                "poses": [touching[0], {"x": 1.5 - 5e-9, "y": 0.5, "angle": 0}],
            },
            "pair overlap",
        ),
        (
            "two touching unit squares",
            {
                "squareSide": 1,
                "container": {"originX": 0, "originY": 0, "side": 2},
                "poses": touching,
            },
            None,
        ),
    )
    page.locator("#pack-json").fill("")
    for label, snapshot, refusal in cases:
        page.locator("#pack-json").fill(json.dumps(snapshot))
        page.locator("#pack-load").click()
        status = page.locator("#pack-status").inner_text()
        facts = page.locator("#pack-stage-facts").inner_text()
        if refusal is None:
            _require(
                "valid unit packing" in status
                and "Valid unit packing" in facts
                and "Required side 2.000000" in facts,
                f"{label} is not shown as a packing: {status!r}; {facts!r}",
            )
            continue
        _require(
            refusal in status
            and "valid unit packing" not in status
            and "bounding side" in status
            and "Not a packing" in facts
            and "Bounding side" in facts
            and "Required side" not in facts
            and "Valid unit packing" not in facts,
            f"{label} is shown as a packing, or unlabelled: {status!r}; {facts!r}",
        )


def _check_quiet_live_regions(browser: Browser, page_path: Path, errors: list[str]) -> None:
    """A second of animated Run rewrites the stage text but announces no frame."""
    page = browser.new_page(
        reduced_motion="no-preference", viewport={"width": 1440, "height": 1000}
    )
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(page_path.resolve().as_uri())
    page.locator("#mode-pack").click()
    facts = page.locator("#pack-stage-facts")
    _require(facts.is_visible(), "the Pack stage facts are hidden after choosing Pack")
    regions = _look(page, "pack/live-watch")
    _require(bool(regions), "the page has no live region to watch")
    first = facts.inner_text()
    page.locator("#pack-run").click()
    page.wait_for_timeout(1000)
    counts = _look(page, "pack/live-count")
    running = _look(page, "pack/run", index=0)
    shown = facts.inner_text()
    page.locator("#pack-pause").click()
    _require(
        running["playing"] and running["steps"] >= 20,
        f"Pack did not animate for a second: {running}",
    )
    _require(
        shown != first and "running" in shown,
        f"the stage facts did not follow the run: {first!r} then {shown!r}",
    )
    _require(
        sum(counts.values()) <= LIVE_MUTATION_LIMIT,
        f"live regions changed per frame during a second of Run: {counts} "
        f"(regions watched: {regions})",
    )
    page.close()


def check(page_path: Path) -> str:
    """Drive Pack through its public controls and inspect the rendered stage."""
    errors: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True, executable_path=os.environ.get("SQUARES_BROWSER_EXECUTABLE")
        )
        # No `bypass_csp`: the page runs under its published policy, as the public loads it.
        page = browser.new_page(
            reduced_motion="reduce", viewport={"width": 1440, "height": 1000}
        )
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(page_path.resolve().as_uri())
        page.locator("#mode-pack").click()
        panel = page.locator("#pack-workspace")
        squares = page.locator("#pack-squares > g")

        def require(condition: bool, message: str) -> None:  # noqa: FBT001
            if not condition:
                raise ValueError(message)

        require(
            panel.is_visible(),
            "Pack panel is hidden after choosing Pack: " + "; ".join(errors),
        )
        require(squares.count() == 17, "Pack did not draw all 17 starting squares")
        require(not page.locator("#squares").is_visible(), "catalogue scene still owns Pack")
        # Pack draws no box: the catalogue's box and trace are hidden, and Pack's container,
        # side 5 for 17 squares from a grid, is drawn.
        drawn = _look(page, "stage/bounds")
        require(
            drawn["container"]["shown"]
            and drawn["container"]["stroke"] not in {"none", ""}
            and drawn["container"]["width"] == 5
            and not drawn["box"]["shown"]
            and not drawn["trace"]["shown"],
            f"Pack does not draw its container, or keeps the catalogue's box: {drawn}",
        )
        require("n = 17" in page.locator("#pack-status").inner_text(), "Pack status lost n")

        page.locator("#pack-count").fill("7")
        page.locator("#pack-seed").fill("42")
        page.locator("#pack-start").select_option("random")
        page.locator("#pack-apply").click()
        require(
            squares.count() == 7,
            f"Pack count did not reach 7: {squares.count()} nodes; "
            f"{page.locator('#pack-status').inner_text()}",
        )
        random_poses = squares.evaluate_all(probe("dom/transforms"))
        stepped = _look(page, "pack/apply", calls=[["step", 1]])
        require(stepped["latest"]["work"]["baseSteps"] == 1, "Pack API step did not advance")
        scene_match = _look(page, "pack/scene-matches-snapshot")
        require(scene_match, "Pack API snapshot does not match the visible square transforms")
        hidden_legacy = _look(page, "api/refusal", calls=[["optimizeStep", 1]])
        require(
            isinstance(hidden_legacy, str) and "packWorkbench" in hidden_legacy,
            f"legacy optimizer advanced behind the Pack scene: {hidden_legacy}",
        )
        page.locator("#pack-apply").click()
        require(
            random_poses == squares.evaluate_all(probe("dom/transforms")),
            "the same random seed does not reproduce its starting arrangement",
        )
        page.locator("#pack-run").click()
        require("1 steps" in page.locator("#pack-status").inner_text(), "Run did not advance")
        page.locator("#pack-restart").click()
        require(
            "0 steps" in page.locator("#pack-status").inner_text(), "Restart did not rewind"
        )
        require(
            random_poses == squares.evaluate_all(probe("dom/transforms")),
            "Restart did not recover the same start",
        )

        imported = {
            "squareSide": 1,
            "container": {"originX": 0, "originY": 0, "side": 2},
            "poses": [{"x": 0.5, "y": 0.5, "angle": 0}],
        }
        page.locator("#pack-workspace details summary").click()
        page.locator("#pack-json").fill(json.dumps(imported))
        page.locator("#pack-load").click()
        require(squares.count() == 1, "import did not draw its one square")
        require("n = 1" in page.locator("#pack-status").inner_text(), "import did not set n")
        require(
            page.locator("#pack-start").input_value() == "given",
            "import did not identify its given arrangement",
        )
        with page.expect_download() as download:
            page.locator("#pack-export").click()
        export_path = download.value.path()
        require(export_path is not None, "Pack export did not download a snapshot")
        exported = json.loads(Path(str(export_path)).read_text(encoding="utf-8"))
        require(exported == imported, "Pack snapshot export differs from its imported geometry")

        page.locator("#pack-json").fill('{"poses":[]}')
        page.locator("#pack-load").click()
        require(squares.count() == 1, "a rejected import replaced the checked arrangement")
        require(
            "snapshot" in page.locator("#pack-status").inner_text().lower(),
            "a rejected import has no useful error",
        )
        page.locator("#pack-resolve").click()
        require(
            "Resolve" in page.locator("#pack-repair-status").inner_text(),
            "Resolve did not expose its receipt",
        )

        page.locator("#mode-animate").click()
        require(not panel.is_visible(), "Pack panel remains visible in Animate")
        page.locator("#mode-pack").click()
        require(
            panel.is_visible() and squares.count() == 1, "Pack lost its arrangement on return"
        )
        _check_modifier_chords(page)
        _check_click_keeps_run(page)
        _check_non_packings_labelled(page)
        page.set_viewport_size({"width": 390, "height": 844})
        # Chromium delivers the resize event after set_viewport_size returns. Wait for
        # the stage's JS scale to reflect the new viewport before testing overflow.
        page.wait_for_function(probe("pack/stage-fits-viewport"))
        width = _look(page, "layout/scroll-width")
        require(width <= 390, f"Pack overflows the mobile viewport: {width}px")
        _check_quiet_live_regions(browser, page_path, errors)
        require(not errors, "page errors: " + "; ".join(errors))
        browser.close()
    return (
        "Pack's own container with no catalogue box, count, seeded starts, transport, "
        "import/export, Resolve, "
        "mode return, bare-key shortcuts, click without drag, non-packings labelled, "
        "quiet live regions "
        "and mobile fit"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page", type=Path)
    options = parser.parse_args()
    if options.page is None:
        with tempfile.TemporaryDirectory(prefix="squares-pack-panel-") as directory:
            page = Path(directory) / "index.html"
            build(page.parent)
            result = check(page)
    else:
        result = check(options.page)
    print(f"OK: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
