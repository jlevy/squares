"""Exercise import, editing, replay, export and mode return in the built animation studio."""

from __future__ import annotations

import argparse
import json
import math
import os
import tempfile
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright

from workbench_tools.browser_page import open_page
from workbench_tools.build_site import build
from workbench_tools.probes import probe

FIXTURE = Path(__file__).resolve().parents[2] / "tests/fixtures/packing-animation-v1.json"
#: Within what the box's side counts as the best known side the gap bar shows: the catalogue's
#: declared stored precision (`CATALOGUE_PRECISION.penetrationTolerance`), because the bar's
#: record is the six-decimal fact and the box's side the frame's nine-decimal side.
CATALOGUE_TOLERANCE = 4e-6


def check(page_path: Path, screenshots: Path | None = None) -> str:
    """Run against the delivered page, including the public API and actual DOM controls."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True, executable_path=os.environ.get("SQUARES_BROWSER_EXECUTABLE")
        )
        page = browser.new_page(
            reduced_motion="reduce", viewport={"width": 1440, "height": 1000}
        )
        errors: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        open_page(page, page_path)
        tabs = page.evaluate(probe("modes/tabs"))
        if [tab[0] for tab in tabs] != ["animate", "pack", "search"] or tabs[0][2] != "true":
            raise ValueError(f"tabs are not Animate, Pack, Search with Animate open: {tabs}")
        if not page.locator("#animation-editor").is_visible() or errors:
            raise ValueError(f"Animate is not what the page opens on: {errors}")
        page.locator("#mode-animate").click()

        def call(name: str, *arguments: Any) -> Any:
            return page.evaluate(probe("api/apply"), {"calls": [[name, *arguments]]})

        def require(condition: bool, message: str) -> None:  # noqa: FBT001
            if not condition:
                raise ValueError(message)

        # The owner's defaults of 2026-09-13, as the page reports them before anything moves.
        law = call("law")
        require(
            {key: law[key] for key in ("rigidity", "repulsion", "attraction", "range")}
            == {"rigidity": 0.35, "repulsion": 950, "attraction": 80, "range": 0.15},
            f"the pair law does not start at the owner's defaults: {law}",
        )
        dial = call("anneal")
        require(
            (dial["level"], dial["min"], dial["max"], dial["dflt"]) == (9, 0, 20, 9),
            f"the annealing dial does not start at 9 of 0..20: {dial}",
        )
        require(
            page.locator("#anneal").get_attribute("max") == "20",
            "the dial's slider stops short",
        )
        # Drained all the way to grey by default (the owner, 2026-09-21).
        require(call("desatFloor") == 0, "the desaturation floor is not 0")
        beat = call("continuous")
        require(
            (beat["dwell"], beat["move"], beat["settle"]) == (0.6, 0.4, 0.3),
            f"the continuous beat is not 0.6 + 0.4 + 0.3: {beat}",
        )
        shown = [
            page.locator(f"#t-{key}").input_value()
            for key in ("dwell", "move", "correct", "settle")
        ]
        require(
            shown == ["0.6", "0.4", "0.2", "0.3"],
            f"the timing inputs do not show the 0.6 / 0.4 / 0.2 / 0.3 beat: {shown}",
        )

        # 6 -> 7 fills the last row of a 3 x 3 grid; 4 -> 5 tilts its squares.
        into = {pair["n"] + 1: index for index, pair in enumerate(call("pairs"))}
        simple_index, moving_index = into[7], into[5]
        toggle = page.locator("#fastsimple-toggle")
        require(toggle.is_checked(), "simple transitions are not sped up by default")

        # The census, observed as the steps whose duration shrinks by the page's speed-up. A
        # simple step lies inside k^2 - k .. k^2 - 1 for k = ceil(sqrt(n + 1)), and that range
        # holds 170 steps of the corpus; twelve of them change the container, because their best
        # packing is tilted, and play at full length. So 158 play sped up, and the page's own
        # count agrees. The twelfth is 211 -> 212 since the #227 intake: de Winter's tilted
        # n = 211 at side 14.998 replaced the 15 x 15 grid, so the grid resumes at 212.
        def grid_fill_range(n: int) -> bool:
            k = math.isqrt(n) + 1  # ceil(sqrt(n + 1))
            return k * k - k <= n <= k * k - 1

        census = page.evaluate(probe("animate/sped-pairs"))
        sped = {row["n"] for row in census if row["sped"]}
        in_range = {row["n"] for row in census if grid_fill_range(row["n"])}
        full_length = {110, 132, 156, 182, 210, 211, 240, 241, 272, 273, 306, 307}
        require(
            call("continuous")["simplePairs"] == len(sped) == 158
            and sped == in_range - full_length,
            f"the simple steps are not the 158 grid fills: page count "
            f"{call('continuous')['simplePairs']}, sped up {len(sped)}, outside the range "
            f"{sorted(sped - in_range)}, missing {sorted(in_range - full_length - sped)}",
        )
        # The speed-up is a setting, not a constant (the owner, 2026-09-22). Four by default,
        # over a control the page also declares the ends of, so the input and the API cannot
        # drift apart about what may be asked for.
        speeds = call("continuous")
        speed = speeds["simpleSpeed"]
        require(speed > 1, f"the simple-transition speed-up is not a speed-up: {speed}")
        require(
            (
                speed,
                speeds["simpleSpeedDefault"],
                speeds["simpleSpeedMin"],
                speeds["simpleSpeedMax"],
            )
            == (4, 4, 1, 8),
            f"the grid-fill speed-up does not start at 4 of 1..8: {speeds}",
        )
        speed_input = page.locator("#simple-speed")
        shown = [
            speed_input.input_value(),
            *(speed_input.get_attribute(name) for name in ("min", "max", "step")),
        ]
        require(
            shown == ["4", "1", "8", "0.5"],
            f"the grid-fill speed control does not show 4 over 1..8 in halves: {shown}",
        )
        fast = [call("duration", simple_index), call("duration", moving_index)]
        toggle.click()
        playback = call("continuous")
        require(not playback["fastSimple"], "unchecking did not turn the speed-up off")
        full = [call("duration", simple_index), call("duration", moving_index)]
        require(
            abs(full[0] - speed * fast[0]) < 1e-9,
            f"the grid fill does not play at {speed}x: {fast[0]} s against {full[0]} s",
        )
        require(
            abs(full[1] - fast[1]) < 1e-9,
            f"a step with motion changed speed: {fast[1]} s against {full[1]} s",
        )
        toggle.click()
        require(call("continuous")["fastSimple"], "checking did not turn the speed-up back on")
        # The speed-up is presentation only: a simple transition simulates as many physics steps
        # sped up as at full length, so `physics()`, and the annealing benchmark that
        # calls it, do the same work whatever the clock plays.
        work = page.evaluate(
            probe("physics/steps-by-speed"),
            {"indices": [simple_index, moving_index], "style": "physics", "mode": "blind"},
        )
        by_speed = {(row["index"], row["fastSimple"]): row for row in work}
        require(
            abs(
                speed * by_speed[simple_index, True]["duration"]
                - by_speed[simple_index, False]["duration"]
            )
            < 1e-9,
            f"the grid fill is not sped up where its physics work is compared: {work}",
        )
        require(
            all(
                by_speed[index, True]["steps"] == by_speed[index, False]["steps"]
                for index in (simple_index, moving_index)
            ),
            f"the simple-transition speed-up changed the physics work: {work}",
        )

        # The factor round-trips through the setter, and the control follows it: what the census
        # above measures is whatever the page is set to, not a number written here. Two is far
        # enough from four that a page ignoring the setter cannot pass by accident.
        moved = call("setSimpleSpeed", 2)
        require(
            moved["simpleSpeed"] == 2 and speed_input.input_value() == "2",
            f"setting the grid-fill speed-up to 2 gave {moved['simpleSpeed']} "
            f"with the control on {speed_input.input_value()}",
        )
        at_two = call("duration", simple_index)
        require(
            abs(full[0] - 2 * at_two) < 1e-9,
            f"the grid fill does not play at 2x once asked: {at_two} s against {full[0]} s",
        )
        # The census measures something different now -- every grid fill is twice the length it
        # was -- and still finds the same 158 steps, because it reads the page's factor rather
        # than assuming one. A census that assumed four would find none of them here.
        recensus = page.evaluate(probe("animate/sped-pairs"))
        require(
            {row["n"] for row in recensus if row["sped"]} == sped,
            "the census does not follow the page's factor: at 2x it reads "
            f"{len({row['n'] for row in recensus if row['sped']})} sped steps, not {len(sped)}",
        )
        # Out of range the page takes the nearest factor it can play rather than the one asked
        # for, so nothing is ever drawn on a clock the control cannot show.
        require(
            [call("setSimpleSpeed", value)["simpleSpeed"] for value in (0.25, 50, 3.7)]
            == [1, 8, 3.5],
            "the grid-fill speed-up is not clamped to 1..8 and snapped to halves",
        )
        restored = call("setSimpleSpeed", speeds["simpleSpeedDefault"])
        require(
            restored["simpleSpeed"] == speed,
            f"the grid-fill speed-up did not go back to {speed}: {restored['simpleSpeed']}",
        )

        # The CITATION section is optional and its checkbox says so (think-nzs4): off on
        # arrival, like the correspondence overlay, and driven from the box rather than only
        # from `setCitations`, so the stage can be seen both ways without a console.
        cites = page.locator("#citations-toggle")
        facts = page.locator("#facts")
        require(
            not cites.is_checked() and call("citations") is False,
            "the citation section is not off when the page opens",
        )
        cites.click()
        require(
            call("citations") is True
            and "shows-citations" in (facts.get_attribute("class") or ""),
            "checking the citations box did not turn the CITATION section on",
        )
        cites.click()
        require(
            call("citations") is False
            and "shows-citations" not in (facts.get_attribute("class") or ""),
            "unchecking the citations box did not turn the CITATION section off",
        )

        # The box on the stage: the frames' grey on its way, green once locked at the best known
        # side, with the room n + 1 needs drawn in the lightest grey and a triangle over the gap
        # bar at its side (the owner, 2026-09-17: every frame one width, and only the lock is a
        # colour change). Both colours are the stylesheet's `--scene-frame-*`, which the probe
        # compares the drawn stroke with, so this asks for the token rather than for a hex.
        #
        # **The box never animates growing** (the owner, 2026-09-21). On 10 -> 11 it rests green
        # at 3.707 while the room 11 needs, 4, fades in around it in light grey over the dwell.
        # When the move opens the box takes that room at once with no ink and darkens into it in
        # place, so the only motion the container ever shows is shrinking: the new square shows
        # once the arrival delay has passed, and the box shrinks to settle at 3.877 inside the
        # room. 6 -> 7 is a grid fill, where the box never changes size. That the box only ever
        # shrinks, frame by frame, is the transition contract's to hold (`check_transitions`).
        def at(seconds: float) -> tuple[float, float, float, float]:
            call("seek", seconds)
            drawn = page.evaluate(probe("stage/box-state"))
            return drawn["trace"], drawn["box"], drawn["traceOpacity"], drawn["boxInk"]

        def locked() -> tuple[bool, bool]:
            drawn = page.evaluate(probe("stage/box-state"))
            return drawn["green"], drawn["pointerLocked"]

        require(
            page.evaluate(probe("stage/box-state"))["boxOverTrace"],
            "the box is not drawn over its trace",
        )
        call("select", into[11])
        step = call("schedule")
        rest = at(0)
        require(
            abs(rest[0] - 4) < 1e-9 and abs(rest[1] - 3.707106781) < 1e-6 and rest[2] == 0,
            f"n = 10 does not rest at 3.707 with the room 11 needs not yet shown: {rest}",
        )
        require(locked() == (True, True), f"n = 10 at rest is not locked green: {locked()}")
        shown = at(step["moveStart"])
        require(
            abs(shown[1] - 3.707106781) < 1e-6 and shown[2] == 1,
            f"the room 11 needs has not faded in by the end of the dwell: {shown}",
        )

        def arriving() -> float:
            return float(
                page.locator('#squares g[data-identity="11"]').get_attribute("opacity") or "nan"
            )

        require(
            step["containerStart"] == step["moveStart"]
            and step["containerEnd"] < step["arrive"],
            f"the box resize does not open the move ahead of the new square: {step}",
        )
        # Half way through the resize the box already has the room, part inked, and nothing has
        # arrived: it darkens into 4, it does not grow to it.
        opening = at((step["containerStart"] + step["containerEnd"]) / 2)
        require(
            abs(opening[1] - 4) < 1e-9 and 0 < opening[3] < 1 and arriving() == 0,
            f"the box is not darkening in place, alone, half way through its resize: "
            f"{opening}, new square at {arriving()}, {step}",
        )
        grown = at(step["containerEnd"])
        require(
            abs(grown[0] - 4) < 1e-9
            and abs(grown[1] - 4) < 1e-9
            and grown[3] == 1
            and arriving() == 0,
            f"the box did not darken into the room before the new square showed: {grown}, "
            f"new square at {arriving()}",
        )
        waiting = at((step["containerEnd"] + step["arrive"]) / 2)
        require(
            abs(waiting[1] - grown[1]) < 1e-9 and arriving() == 0,
            f"the new square shows during the arrival delay: {waiting}, {arriving()}",
        )
        at((step["arrive"] + step["arrived"]) / 2)
        require(
            0 < arriving() < 1,
            f"the new square is not fading in after the delay: {arriving()}, {step}",
        )
        moving = page.evaluate(probe("stage/box-state"))
        require(
            locked() == (False, False) and moving["grey"],
            f"the moving box or its pointer is not the frames' grey: {locked()}, "
            f"{moving['boxStroke']}",
        )
        settled = at(call("duration", into[11]))
        require(
            abs(settled[0] - 4) < 1e-9
            and abs(settled[1] - 3.87708359) < 1e-6
            and settled[2] == 1,
            f"n = 11 does not settle at 3.877 inside a trace at 4: {settled}",
        )
        require(locked() == (True, True), f"n = 11 settled is not locked green: {locked()}")
        drawn = page.evaluate(probe("stage/box-state"))
        require(
            drawn["pointerX"] is not None and abs(drawn["pointerX"] - drawn["recordX"]) < 0.02,
            f"the pointer is not over the best known side: {drawn}",
        )
        call("select", simple_index)
        fill = at(call("duration", simple_index))
        require(fill[0] == fill[1] == 3, f"a grid fill changed the box: {fill}")

        # Green means one thing. The box locks, and its pointer with it, only where it rests at
        # the best known side of the n the gap bar describes, within the validity contract's
        # tolerance, and never while it is on its way: through a move only a step whose box
        # does not change size stays green. Every step rests locked in its dwell and at its end.
        # Swept over every step under the tween, and under physics at the steps into 6 and 12,
        # where the moving container breathes past the record.
        sweeps = [
            ("tween", None, [0.1, 0.21, 0.25, 0.5, 0.9]),
            ("physics", [into[6], into[12]], [0.25, 0.5, 0.9]),
        ]
        misread: list[str] = []
        sampled = 0
        for style, indices, fractions in sweeps:
            rows = page.evaluate(
                probe("stage/box-locks"),
                {"indices": indices, "style": style, "fractions": fractions},
            )
            steps: dict[int, list[dict[str, Any]]] = {}
            for row in rows:
                steps.setdefault(row["index"], []).append(row)
            for step_rows in steps.values():
                resting = all(row["side"] == step_rows[0]["side"] for row in step_rows)
                for row in step_rows:
                    sampled += 1
                    at_record = abs(row["side"] - row["record"]) <= CATALOGUE_TOLERANCE
                    label = (
                        f"{style} {row['n']} -> {row['n'] + 1} {row['phase']} t={row['t']:.3f}"
                    )
                    if row["green"] != row["pointer"]:
                        misread.append(
                            f"{label}: box green {row['green']}, pointer {row['pointer']}"
                        )
                    elif row["phase"] != "move" and not row["green"]:
                        misread.append(f"{label}: not locked at rest ({row})")
                    elif row["green"] and not (
                        at_record and (row["phase"] != "move" or resting)
                    ):
                        misread.append(f"{label}: locked on its way or off the record ({row})")
        require(
            not misread,
            f"the box or its pointer misreads its lock in {len(misread)} of {sampled} samples: "
            + "; ".join(misread[:6]),
        )

        initial = call("importAnimation", FIXTURE.read_text(encoding="utf-8"))
        require(initial["active"] and initial["n"] == 2, "import did not activate n = 2")
        require(not initial["guided"], "an earlier free frame inherited later guidance")
        require(page.locator("#animation-editor").is_visible(), "animation editor is hidden")
        require(
            page.locator("#animation-squares > g").count() == 2, "stage lost square identities"
        )
        # The studio draws no box: the catalogue's box and trace are hidden, and the imported
        # animation's container is drawn at its own side, 2.
        drawn = page.evaluate(probe("stage/bounds"))
        require(
            drawn["container"]["shown"]
            and drawn["container"]["stroke"] not in {"none", ""}
            and drawn["container"]["width"] == 2
            and not drawn["box"]["shown"]
            and not drawn["trace"]["shown"],
            f"the animation studio does not draw its container, or keeps the catalogue's box: "
            f"{drawn}",
        )
        if screenshots is not None:
            screenshots.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshots / "animation-desktop.png"), full_page=True)
        page.set_viewport_size({"width": 390, "height": 844})
        dimensions = page.evaluate(probe("layout/document-size"))
        require(
            dimensions["width"] <= dimensions["viewport"],
            f"animation editor overflows the mobile viewport: {dimensions}",
        )
        if screenshots is not None:
            page.screenshot(path=str(screenshots / "animation-mobile.png"), full_page=True)
        page.set_viewport_size({"width": 1440, "height": 1000})
        middle = call("seekAnimation", 0.5)
        require(
            middle["guided"] and middle["valid"] is False,
            "claimed feasibility bypassed geometry",
        )
        interpolated = call("seekAnimation", 0.25)
        require(
            interpolated["interpolated"] and interpolated["valid"] is None,
            "interpolation reused feasibility",
        )

        page.locator("#animation-loaded details summary").click()
        page.locator("#animation-frame").select_option("1")
        page.locator("#animation-poses").fill("[[0.5,0.5,0],[1.5,0.5,0]]")
        page.locator("#animation-save-frame").click()
        edited = json.loads(call("exportAnimation"))
        require("feasible" not in edited["frames"][1], "editing retained a feasibility claim")
        require(edited["frames"][2]["guided"], "editing laundered later guidance")
        require("<svg" in call("exportAnimationSvg"), "SVG export did not produce a drawing")

        page.locator("#animation-duration").fill("0.05")
        page.locator("#animation-duration").press("Tab")
        call("seekAnimation", 0)
        expected_first = call("exportAnimationSvg")
        with page.expect_download() as captured:
            page.locator("#animation-frames-export").click()
        capture_path = captured.value.path()
        require(capture_path is not None, "capture did not download its frame receipt")
        payload = json.loads(Path(str(capture_path)).read_text(encoding="utf-8"))
        receipt = payload["receipt"]
        require(receipt["status"] == "completed", "frame capture did not complete")
        require(receipt["scheduledFrames"] == 3, "frame capture lost its endpoint")
        require(
            receipt["frames"][0]["svg"] == expected_first, "capture differs from visible seek"
        )
        require(len(receipt["source"]["commit"]) == 40, "capture lost source identity")
        require(payload["animation"]["frames"][2]["guided"], "capture lost guidance ancestry")

        page.locator("#animation-play").click()
        played = call("animationState")
        require(
            played["time"] == 1 and not played["playing"],
            "reduced motion did not seek to the end",
        )
        # A rejected replacement must leave the checked document in place.
        page.locator("#animation-editor > details summary").click()
        page.locator("#animation-json").fill('{"contract":"unsupported"}')
        page.locator("#animation-load").click()
        require(
            call("animationState")["n"] == 2, "invalid import replaced the checked document"
        )
        require(
            "contract" in (page.locator("#animation-status").text_content() or ""),
            "invalid import has no useful error",
        )

        page.locator("#mode-pack").click()
        require(
            not page.locator("#animation-editor").is_visible(),
            "Pack did not relinquish the trace scene",
        )
        require(page.locator("#pack-squares").is_visible(), "Pack scene remained hidden")
        require(page.locator("#pack-workspace").is_visible(), "Pack controls remained hidden")
        page.locator("#mode-animate").click()
        drawn = page.evaluate(probe("stage/bounds"))
        require(
            drawn["box"]["shown"] and drawn["container"]["stroke"] == "none",
            f"back in Animate the catalogue does not draw its box over an undrawn container: "
            f"{drawn}",
        )
        require(not errors, "page errors: " + "; ".join(errors))
        browser.close()
    return (
        "arrival on Animate, first of Animate, Pack and Search; the owner's law, dial, beat "
        "and desaturation defaults, the box, its trace, its lock "
        "and its gap-bar pointer through a step, sped-up simple "
        "transitions with their checkbox and their settable factor, "
        "the citation section off on arrival and driven from its box, "
        "animation import drawn in its own container with no "
        "catalogue box, geometry/guidance, frame edits, replay, "
        "SVG/JSON/frame capture, Pack return, and the box back in Animate"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page", type=Path)
    parser.add_argument(
        "--screenshots", type=Path, help="also save desktop and mobile UI views"
    )
    options = parser.parse_args()
    if options.page is None:
        with tempfile.TemporaryDirectory(prefix="squares-animation-editor-") as directory:
            page = Path(directory) / "index.html"
            build(page.parent)
            result = check(page, options.screenshots)
    else:
        result = check(options.page, options.screenshots)
    print(f"OK: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
