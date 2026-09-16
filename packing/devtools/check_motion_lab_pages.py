"""Drive both Motion Lab pages in Chromium and report what their controls draw.

The labs had no browser check: their tests read the rendered HTML and run the models in
Node, so nothing proved that a page's scripts run in a page. That mattered when the
scripts became module scripts (think-6o9n), which changes how a browser runs them. This
loads each page from a file, works its controls through Playwright's own input and locator
calls, and fails on an uncaught error, a console error, or a readout the page script never
wrote. `--report` writes every observation as JSON, so two builds of a page can be compared
value for value.

The general lab's numerical run needs its loopback service, so only its editor is driven
here: selection, keyboard moves and rotations, snapping, and reset, all of which go through
the editor model the page script reads from `globalThis.MotionLabEditor`.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.check_motion_lab_pages
    uv run --frozen --all-extras --group dev python -m devtools.check_motion_lab_pages \\
        --exact EXACT.html --general GENERAL.html --report REPORT.json
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

from playwright.sync_api import ConsoleMessage, Error, Page, sync_playwright

from devtools.render_general_motion_lab import (
    DEFAULT_SEED,
    DEFAULT_SIDE,
    DEFAULT_SQUARE_COUNT,
    render_general_motion_lab,
)
from devtools.render_packing_motion_lab import render_motion_lab

#: The exact lab's readouts, each written by the page script's first update.
EXACT_READOUTS = (
    "scene-value",
    "parameter-name",
    "parameter-value",
    "evidence-value",
    "source-value",
    "claim-value",
    "angle-value",
    "contacts-value",
    "stage-description",
    "motion-note",
    "live-region",
)
EXACT_TOGGLES = ("ids-toggle", "contacts-toggle", "trails-toggle", "tangent-toggle")
#: Readouts the exact lab's markup leaves empty, so an empty one after load means the page
#: script did not run.
EXACT_WRITTEN = ("scene-value", "parameter-value", "angle-value", "stage-description")

#: The general lab's setup readouts, written by `renderSetup` through the editor model.
GENERAL_READOUTS = (
    "run-readout-title",
    "mode-value",
    "groups-value",
    "diagnostics-value",
    "selection-value",
    "event-value",
    "live-region",
)

State = dict[str, Any]


def _exact_state(page: Page, step: str) -> State:
    return {
        "step": step,
        "readouts": {name: page.locator(f"#{name}").text_content() for name in EXACT_READOUTS},
        "valuetext": page.locator("#parameter-input").get_attribute("aria-valuetext"),
        "plane": page.locator("#math-plane").inner_html(),
        "labels": page.locator("#label-layer").inner_html(),
        "branch_hidden": page.locator("#branch-panel").is_hidden(),
        "owner_disabled": page.locator("#owner-select").is_disabled(),
    }


def _options(page: Page, select: str) -> list[str]:
    return [
        option.get_attribute("value") or ""
        for option in page.locator(f"#{select} option").all()
    ]


def drive_exact(page: Page) -> list[State]:
    """Every motion and stratum at three path positions, every owner, the overlays on."""
    states = [_exact_state(page, "opened")]
    for toggle in EXACT_TOGGLES:
        page.locator(f"#{toggle}").check()
    states.append(_exact_state(page, "overlays on"))
    for motion in _options(page, "motion-select"):
        page.locator("#motion-select").select_option(motion)
        for stratum in _options(page, "stratum-select"):
            page.locator("#stratum-select").select_option(stratum)
            for position in ("0", "500", "1000"):
                page.locator("#parameter-input").fill(position)
                states.append(_exact_state(page, f"{motion} {stratum} at {position}"))
            if not page.locator("#owner-select").is_disabled():
                for owner in _options(page, "owner-select"):
                    page.locator("#owner-select").select_option(owner)
                    states.append(_exact_state(page, f"{motion} {stratum} owner {owner}"))
    page.locator("#restart-button").click()
    states.append(_exact_state(page, "restarted"))
    return states


def _general_state(page: Page, step: str) -> State:
    return {
        "step": step,
        "readouts": {
            name: page.locator(f"#{name}").text_content() for name in GENERAL_READOUTS
        },
        "accepted": page.locator("#accepted-layer").inner_html(),
        "labels": page.locator("#free-label-layer").inner_html(),
        "rotate_disabled": page.locator("#rotate-left-button").is_disabled(),
    }


def drive_general(page: Page) -> list[State]:
    """Select a square, move and rotate it by keyboard and button, then snap and reset."""
    states = [_general_state(page, "opened")]
    stage = page.locator("#free-stage")
    # The square drawn last is the one on top, so a click at its centre reaches it.
    page.locator("#accepted-layer [data-square-id]").last.click()
    states.append(_general_state(page, "top square clicked"))
    # A key pressed on a square selects it: the stage's handler reads the event's target.
    square = page.locator('#accepted-layer [data-square-id="0"]').first
    for key in ("ArrowRight", "ArrowRight", "Shift+ArrowUp", "q", "e", "e"):
        square.press(key)
        states.append(_general_state(page, f"pressed {key} on square 0"))
    page.locator("#rotate-left-button").click()
    states.append(_general_state(page, "rotated left"))
    page.locator("#snapping-toggle").uncheck()
    for key in ("ArrowLeft", "ArrowDown"):
        stage.press(key)
        states.append(_general_state(page, f"unsnapped, pressed {key}"))
    page.locator("#reset-button").click()
    states.append(_general_state(page, "reset"))
    return states


def run_page(path: Path, drive: Callable[[Page], list[State]]) -> tuple[list[State], list[str]]:
    """Load one page from its file, drive it, and return its states and its errors."""
    errors: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 1280, "height": 900})

            def on_console(message: ConsoleMessage) -> None:
                if message.type == "error":
                    errors.append(f"console: {message.text}")

            def on_error(error: Error) -> None:
                errors.append(f"uncaught: {error.message}")

            page.on("console", on_console)
            page.on("pageerror", on_error)
            page.goto(path.resolve().as_uri(), wait_until="load")
            states = drive(page)
        finally:
            browser.close()
    return states, errors


def faults(exact: list[State], general: list[State], errors: list[str]) -> list[str]:
    """What says a page script did not run, or ran and failed."""
    found = list(errors)
    opened = exact[0]["readouts"]
    found.extend(
        f"exact lab: #{name} was never written" for name in EXACT_WRITTEN if not opened[name]
    )
    if len({state["plane"] for state in exact}) < 2:
        found.append("exact lab: no control changed the drawing")
    if general[0]["readouts"]["diagnostics-value"] in {None, "", "Checking…"}:
        found.append("general lab: the setup diagnostics were never written")
    if len({state["accepted"] for state in general}) < 2:
        found.append("general lab: no edit changed the drawing")
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--exact", type=Path, help="the exact n=5 lab; rendered fresh if omitted"
    )
    parser.add_argument(
        "--general", type=Path, help="the general lab; rendered fresh if omitted"
    )
    parser.add_argument("--report", type=Path, help="write every observation here as JSON")
    arguments = parser.parse_args(argv)
    with tempfile.TemporaryDirectory(prefix="squares-motion-lab-") as scratch:
        exact_page = arguments.exact
        if exact_page is None:
            exact_page = Path(scratch) / "exact.html"
            exact_page.write_text(render_motion_lab(), encoding="utf-8")
        general_page = arguments.general
        if general_page is None:
            general_page = Path(scratch) / "general.html"
            general_page.write_text(
                render_general_motion_lab(
                    n=DEFAULT_SQUARE_COUNT, seed=DEFAULT_SEED, side=DEFAULT_SIDE
                ),
                encoding="utf-8",
            )
        exact, exact_errors = run_page(exact_page, drive_exact)
        general, general_errors = run_page(general_page, drive_general)
    report = {"exact": exact, "general": general}
    if arguments.report is not None:
        arguments.report.write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
    problems = faults(
        exact,
        general,
        [f"exact lab {error}" for error in exact_errors]
        + [f"general lab {error}" for error in general_errors],
    )
    if problems:
        print("FAIL:\n  " + "\n  ".join(problems), file=sys.stderr)
        return 1
    print(
        f"OK: exact lab drove {len(exact)} states and the general lab {len(general)}, "
        "with no page error and every readout written"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
