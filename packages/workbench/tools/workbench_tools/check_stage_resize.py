"""Drag, key, reload and reset the separator between the stage and the controls."""

from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, sync_playwright

from workbench_tools.build_site import build
from workbench_tools.probes import probe

KEY = "squares.workbench.stageShare"
FIXTURE = Path(__file__).resolve().parents[2] / "tests/fixtures/packing-animation-v1.json"


def check(page_path: Path) -> str:
    """Drive the separator by pointer and keyboard on the built page in a 1440 x 1000 window."""
    errors: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True, executable_path=os.environ.get("SQUARES_BROWSER_EXECUTABLE")
        )
        page = browser.new_page(
            reduced_motion="reduce", viewport={"width": 1440, "height": 1000}
        )
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(page_path.resolve().as_uri())
        handle = page.locator("#stage-resize")

        def require(condition: bool, message: str) -> None:  # noqa: FBT001
            if not condition:
                raise ValueError(message)

        def layout(view: Page) -> dict[str, Any]:
            return view.evaluate(probe("layout/separator"), {"key": KEY})

        def stage_height(view: Page) -> float:
            return float(layout(view)["stageHeight"])

        def fits(view: Page) -> bool:
            return bool(layout(view)["controlsFit"])

        require(handle.get_attribute("role") == "separator", "the handle is not a separator")
        require(
            handle.get_attribute("aria-orientation") == "horizontal"
            and handle.get_attribute("tabindex") == "0",
            "the separator does not name its orientation or take the focus",
        )
        automatic = stage_height(page)
        # The window-splitter pattern: `aria-controls` names the primary pane, the one whose
        # size the separator's value reports, and that is the stage.
        controlled = handle.get_attribute("aria-controls") or ""
        pane = page.locator(f"#{controlled}").bounding_box() if controlled else None
        require(
            controlled == "stage-wrap" and pane is not None,
            f"the separator controls {controlled!r}, not the stage whose height it reports",
        )
        require(
            pane is not None
            and abs(float(handle.get_attribute("aria-valuenow") or "nan") - pane["height"]) <= 1
            and abs(pane["height"] - automatic) <= 1,
            "the separator's value is not the height of the pane it controls",
        )

        box = handle.bounding_box()
        if box is None:
            raise ValueError("the separator is not drawn")
        x, y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
        page.mouse.move(x, y)
        page.mouse.down()
        page.mouse.move(x, y + 80, steps=8)
        page.mouse.up()
        dragged = stage_height(page)
        require(
            abs(dragged - (automatic + 80)) <= 2,
            f"dragging 80 px down moved the stage from {automatic} to {dragged}",
        )
        require(fits(page), "the controls overflow the window after a drag")
        require(
            not layout(page)["resizing"], "the page is still marked as resizing after the drag"
        )

        def call(*calls: list[Any]) -> Any:
            return page.evaluate(probe("api/apply"), {"calls": list(calls)})

        def playhead() -> tuple[int, float]:
            state = call(["state"])
            return state["pair"], state["t"]

        # The separator's keys move the separator and nothing else: with the playhead part-way
        # through 10 -> 11, the page's own Home and End would rewind or finish the step.
        call(["pause"], ["select", 9], ["seek", 1.0])
        before = playhead()
        handle.focus()
        page.keyboard.press("ArrowUp")
        keyed = stage_height(page)
        require(abs(keyed - (dragged - 16)) <= 2, f"ArrowUp moved {dragged} to {keyed}")
        page.keyboard.press("Home")
        require(
            abs(stage_height(page) - 120) <= 2, "Home did not raise the stage to its minimum"
        )
        page.keyboard.press("End")
        require(fits(page), "End pushed the controls out of the window")
        page.keyboard.press("Shift+ArrowUp")
        shifted = stage_height(page)
        require(
            playhead() == before,
            f"the separator's keys moved the playhead from {before} to {playhead()}",
        )
        # And with an imported animation on the stage, whose own Home and End seek it.
        call(["importAnimation", FIXTURE.read_text(encoding="utf-8")], ["seekAnimation", 0.5])
        handle.focus()
        page.keyboard.press("Home")
        page.keyboard.press("End")
        page.keyboard.press("Shift+ArrowUp")
        traced = call(["animationState"])
        require(
            traced["active"] and traced["time"] == 0.5,
            f"the separator's keys seeked the imported animation: {traced}",
        )
        page.locator("#mode-pack").click()
        page.locator("#mode-animate").click()
        shifted = stage_height(page)

        page.reload()
        restored = stage_height(page)
        require(
            abs(restored - shifted) <= 2,
            f"a reload did not keep the stage at {shifted}, it came back at {restored}",
        )

        # A chosen share is re-clamped whenever the window changes, and kept. End stores the
        # largest share, 944 of 1000 px; in a 600 px window that share would leave the controls
        # 34 px, so the stage stops at 600 - 56 = 544, and the separator reports the new range.
        # Back at 1000 px the stored share, not the clamped height, comes back.
        handle.focus()
        page.keyboard.press("End")
        tallest = layout(page)
        page.set_viewport_size({"width": 1440, "height": 600})
        page.wait_for_timeout(200)
        short = layout(page)
        require(
            abs(short["stageHeight"] - 544) <= 2
            and short["controlsFit"]
            and short["valueMax"] == 544
            and abs(short["valueNow"] - short["stageHeight"]) <= 1,
            f"a 600 px window did not re-clamp the stage to 544: {short}",
        )
        page.set_viewport_size({"width": 1440, "height": 1000})
        page.wait_for_timeout(200)
        again = layout(page)
        require(
            abs(again["stageHeight"] - tallest["stageHeight"]) <= 2
            and again["stored"] == tallest["stored"],
            f"the clamp overwrote the chosen share: {tallest} then {again}",
        )
        page.locator("#stage-resize").dblclick()
        reset = stage_height(page)
        require(
            abs(reset - automatic) <= 2,
            f"double-click did not return to the automatic {automatic}: {reset}",
        )
        require(layout(page)["stored"] is None, "double-click did not forget the stored share")
        page.locator("#mode-search").click()
        require(not handle.is_visible(), "the separator shows over Search")
        page.locator("#mode-animate").click()
        require(handle.is_visible(), "the separator did not come back with Animate")
        require(not errors, "page errors: " + "; ".join(errors))
        browser.close()
    return (
        "stage separator drag, arrows, Home and End with the step and an imported animation "
        "left where they were, reload persistence, re-clamping in a shorter window, "
        "double-click reset and Search hiding"
    )


def main() -> int:
    """Check a supplied page, or build one first."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page", type=Path, help="reuse this built index.html")
    args = parser.parse_args()
    if args.page is not None:
        print(f"OK: {check(args.page)}")
        return 0
    with tempfile.TemporaryDirectory(prefix="squares-workbench-resize-") as scratch:
        page = Path(scratch) / "workbench" / "index.html"
        build(page.parent)
        print(f"OK: {check(page)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
