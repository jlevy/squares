"""The revision-9 checks: one view, the chooser for n, the range spine, the gap bar.

Everything here is a property of the built page, driven through `window.atlasTransitions` in the
pinned headless shell. It complements `check_revision6.py` (desaturation, snap, blind, continuous
play) and `check_revision7.py` (the bar scale, the annealing dial, the live gap) rather than
repeating them. The workbench needs pairs the 25-pair demo does not carry, so it defaults to the
all-pairs build.

Revision 9 folded revision 8's two tabs into one view: the range is the spine, its two ends are
values of n stepped *into*, and setting them equal is the old Single step tab. So the tab checks
below became checks that the tabs are *gone* and that `setTab` / `tab` survive as no-ops.

Revision 11 took the choice out of the colouring: hue is a function of the angle and shade is the
square's full-side contact count, always, with no rule to pick. Step 9 is that property, driven
through `colour()` (what the frame was painted from) and `fillsFor` (the same map as a pure
function, needing nothing on the stage).

Revision 11 also made the contact force one editable law of the signed gap (step 10) and put a
relationship graph beside it saying which pairs the law's attraction reaches (step 11). The two are
orthogonal, and the asymmetry is the property step 11 exists to hold down: repulsion always applies
to every pair, attraction only to the pairs the graph relates.

The JavaScript this drives the page with lives in `probes/`, one expression to a file, and
reaches the page through `probes.probe`. Nothing below formats a Python value into a probe:
a probe that needs a number takes it as its one argument. See `probes.py` for why.

    packing/.venv/bin/python3 check_workbench.py [workbench.html]
"""

import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright
from probes import probe

HERE = Path(__file__).resolve().parent

#: What one trajectory may cost to build. Measured on this machine at n = 324: 27 ms and 1.3 MB
#: under `physics`, 31 ms under `bodies`. The ceilings are about thirteen times the time and three
#: times the memory, which is loose enough that wall clock on a loaded machine does not trip it and
#: tight enough that an algorithm going quadratic does.
TRAJECTORY_MS_CEILING = 400.0
TRAJECTORY_BYTE_CEILING = 4_000_000


def oklab(hex_colour: str) -> tuple[float, float, float]:
    """(lightness, chroma, hue in degrees) of an sRGB hex colour in OkLab / OkLCh."""

    def linear(channel: int) -> float:
        c = channel / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (linear(int(hex_colour[i : i + 2], 16)) for i in (1, 3, 5))
    l_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m_ = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s_ = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    lightness = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return lightness, math.hypot(a, bb), (math.degrees(math.atan2(bb, a)) + 360) % 360


def hue_gap(a: float, b: float) -> float:
    """The shorter way round the OkLCh hue circle, in degrees."""
    return abs((a - b + 180) % 360 - 180)


def fold_angle(a: float) -> float:
    """A tilt modulo a quarter turn, as the page folds it."""
    return ((a % 90) + 90) % 90


def angle_gap(a: float, b: float) -> float:
    """How far apart two tilts are, seam included, as the page measures it."""
    d = abs(fold_angle(a) - fold_angle(b))
    return min(90 - d, d)


# ---------------------------------------------------------------- the force law, reimplemented
# The revision-11 law written out from the formula rather than read off the page, so `lawForce` is
# checked against something independent of itself. `steep` is derived from the rigidity, not a fifth
# parameter, which is what makes the shipped defaults reproduce the old hard-coded law exactly.
LAW_KEYS = ("rigidity", "repulsion", "attraction", "range")
LAW_TOL0, LAW_STEEP_MAX = 0.15, 8
LAW_DEFAULT = {"rigidity": 0.15, "repulsion": 2500, "attraction": 0, "range": 0}
LAW_BOUNDS = {
    "rigidity": [0.002, 0.4],
    "repulsion": [200, 8000],
    "attraction": [0, 400],
    "range": [0, 0.5],
}
LAW_PRESETS = {
    "rigid": {"rigidity": 0.01, "repulsion": 4000, "attraction": 0, "range": 0},
    "soft": {"rigidity": 0.35, "repulsion": 400, "attraction": 0, "range": 0},
    "sticky": {"rigidity": 0.08, "repulsion": 2500, "attraction": 120, "range": 0.25},
}


def law_steep(law: dict) -> float:
    """The slope multiplier past the knee: zero at the shipped rigidity, eight at a fifteenth of it."""
    return LAW_STEEP_MAX * max(0.0, 1 - law["rigidity"] / LAW_TOL0)


def law_force(law: dict, d: float) -> float:
    """The force at a signed gap `d`: positive pushes apart, negative pulls together."""
    if d <= 0:
        p, tol = -d, law["rigidity"]
        return law["repulsion"] * (min(p, tol) + law_steep(law) * max(0.0, p - tol))
    if not (law["attraction"] > 0 and law["range"] > 0) or d >= law["range"]:
        return 0.0
    u = d / law["range"]
    return -law["attraction"] * 4 * u * (1 - u)


def law_samples(law: dict) -> list[float]:
    """Signed gaps worth asking a law about: a dense sweep, with every breakpoint sampled exactly."""
    ds = [-0.6 + 1.2 * i / 240 for i in range(241)]
    ds += [
        -law["rigidity"],
        -law["rigidity"] - 1e-6,
        -law["rigidity"] + 1e-6,
        0.0,
        1e-12,
        -1e-12,
        1e-9,
        -1e-9,
    ]
    if law["range"] > 0:
        r = law["range"]
        ds += [r, r - 1e-6, r + 1e-6, r / 2, r / 4, r * 3 / 4, r * 2]
    return sorted(set(ds))


# ---------------------------------------------------------------- the plot's own geometry
# The two half-axes of `#law-plot`: the gap runs across the whole editable domain so a handle can
# never be dragged off the plot, the push climbs a ladder chosen to keep the current peak in the
# box, and the pull hangs below the zero line on the attraction's own fixed bound.
LP = {
    "w": 300,
    "zero": 88,
    "pullSpan": 44,
    "dLo": -0.42,
    "dHi": 0.52,
    "ladder": [200, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000],
}


def lp_x(d: float) -> float:
    return ((d - LP["dLo"]) / (LP["dHi"] - LP["dLo"])) * LP["w"]


def lp_top(law: dict) -> int:
    peak = max(law_force(law, LP["dLo"]), law["repulsion"] * law["rigidity"], 1)
    for v in LP["ladder"]:
        if peak <= v:
            return v
    return LP["ladder"][-1]


def lp_knee(law: dict) -> tuple[float, float]:
    """Where the knee handle belongs: at -rigidity across, at repulsion x rigidity up."""
    push = law["repulsion"] * law["rigidity"]
    return lp_x(-law["rigidity"]), LP["zero"] - min(1.0, max(0.0, push / lp_top(law))) * LP[
        "zero"
    ]


def lp_pull(law: dict) -> tuple[float, float]:
    """Where the pull handle belongs: at half the range across, at the attraction down."""
    depth = min(1.0, max(0.0, law["attraction"] / LAW_BOUNDS["attraction"][1]))
    return lp_x(law["range"] / 2), LP["zero"] + depth * LP["pullSpan"]


def main() -> int:
    page_path = (HERE / sys.argv[1]) if len(sys.argv) > 1 else HERE / "workbench.html"
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.on(
            "console",
            lambda m: (
                failures.append(f"console.{m.type}: {m.text}") if m.type == "error" else None
            ),
        )
        page.on("pageerror", lambda e: failures.append(f"pageerror: {e}"))
        page.goto(f"file://{page_path}")
        page.wait_for_timeout(900)

        def look(probe_name: str, /, **argument: Any) -> Any:
            """Put one probe to the page, with its argument.

            The name is positional-only so that every keyword belongs to the probe: a probe
            asking for a field called `name` would otherwise collide with this one's.
            """
            return page.evaluate(probe(probe_name), argument or None)

        def drive(*calls: tuple[Any, ...]) -> Any:
            """Several calls on the page's API, in one turn, so no frame falls between them.

            Each call is `(method, *arguments)`; the last one's answer comes back. Driving a
            sequence as one probe matters: the page runs on a frame clock, and two settings
            applied in two turns are not the same thing as two settings applied in one.
            """
            return look("api/apply", calls=[list(call) for call in calls])

        def ask(method: str, *arguments: Any) -> Any:
            """One call on the page's API, with its answer."""
            return drive((method, *arguments))

        def text_of(ident: str) -> str:
            """The text of one element."""
            return look("dom/text", id=ident)

        def in_page(ident: str) -> bool:
            """Is there an element with this id?"""
            return look("dom/present", id=ident)

        def seek_to_end(*before: tuple[Any, ...]) -> None:
            """Seek to the last instant of whatever is on the stage.

            Any calls given are applied first and in the same turn, because the duration is
            what those calls leave behind rather than what stood before them.
            """
            look("page/seek-to-end", calls=[list(call) for call in before])

        # ---- step 1: one view, no tabs.
        api = set(look("page/api-names"))
        for name in (
            "setTab",
            "tab",
            "setStepN",
            "stepN",
            "setRange",
            "range",
            "playRange",
            "gapBar",
        ):
            check(name in api, f"the API lacks {name}")
        # The tab bar and the two tab panels are gone from the page; the API keeps the two calls.
        gone = look(
            "dom/present-ids",
            ids=["tabbar", "tab-single", "tab-sequence", "panel-single", "panel-sequence"],
        )
        check(gone == [], f"the tab machinery is still in the page: {gone}")
        check(
            look("dom/count", selector="[role=tab], [role=tablist], [role=tabpanel]") == 0,
            "the page still carries tab roles",
        )
        check(ask("tab") == "single", "tab() is not the 'single' no-op")
        check(ask("setTab", "sequence") == "single", "setTab is not a no-op")
        check(in_page("panel"), "there is no single control panel")
        # One control set: every setting is reachable without switching anything.
        for ident in (
            "range-from",
            "range-to",
            "range-all",
            "step-chips",
            "range-duration",
            "range-position",
            "play",
            "clock",
            "style-select",
            "anneal",
            "mode-tabs",
        ):
            check(in_page(ident), f"the one view lacks #{ident}")
        # Revision 10: the timeline scrubber is gone from the page, `seek` staying on the API.
        check(not in_page("scrub"), "the timeline scrubber is still in the page")
        # Every slider in the controls is named, which is how the scrubber's absence is checked
        # without counting: the speed dial, the annealing dial and the four physics-law dials, and
        # nothing whose id reads like a timeline. (This was a count of two when the scrubber went;
        # the law panel has since added four, so the ids say it instead.)
        sliders = look("controls/slider-ids")
        # Revision 16: the law sliders are generated from the page's own parameter table, so this
        # asks the page which ones that table implies rather than restating a list that has needed
        # editing every time a law or a parameter was added. What is actually being checked is
        # that nothing else is a slider -- that the timeline scrubber is gone and has not returned
        # under another name -- so only the handful outside the laws is written out here.
        derived = look("controls/law-slider-ids")
        # `desat-floor` joins them: the owner asked for the degree of desaturation to be settable,
        # so how much chroma a moving square keeps is a dial like the rest rather than a constant.
        check(
            sorted(sliders)
            == sorted(derived + ["anneal", "desat-floor", "grow-rate", "grow-size", "speed"]),
            f"the controls carry a slider that is none of the speed, drain, annealing and law dials: {sliders}",
        )
        check("seek" in api, "the API lost seek when the scrubber went")
        # The controls may not push the stage off the window.
        fits = look("stage/fits-window")
        check(
            fits["top"] >= -0.5 and fits["bottom"] <= fits["h"] + 0.5,
            f"the stage does not fit above the controls: {fits}",
        )

        # ---- step 2: the chooser for n, which is the range collapsed onto one value.
        check(ask("stepN") == 17, "the workbench does not open on n = 17")
        opened = ask("range")
        check(
            opened["from"] == 17 and opened["to"] == 17 and opened["steps"] == 1,
            f"the workbench does not open on the one-step range 17 to 17: {opened}",
        )
        st = ask("state")
        check(
            st["n"] == 16,
            f"n = 17 does not show the step 16 -> 17 (the pair starts at {st['n']})",
        )
        # Revision 10: the page opens in Pack, where the label names the size, not the step; Animate
        # keeps the step wording. Both are read here so the two modes cannot drift apart silently.
        label = text_of("step-label")
        check(
            "17" in label and "16" not in label,
            f"the Pack label does not name the size alone: {label!r}",
        )
        # Animate has never been entered on this page, so this is where it opens on the whole corpus.
        ask("setMode", "animate")
        opening = ask("range")
        pairs = ask("pairs")
        check(
            opening["from"] == pairs[0]["n"] + 1 and opening["to"] == pairs[-1]["n"] + 1,
            f"Animate does not open on the whole corpus the first time: {opening}",
        )
        ask("setRange", 17, 17)
        label = text_of("step-label")
        check(
            "16" in label and "17" in label,
            f"the Animate label does not name both ends: {label!r}",
        )
        ask("setMode", "pack")
        for want in (5, 10, 11, 26, 29, 100, 110, 272):
            got = ask("setStepN", want)
            check(got == want, f"setStepN({want}) landed on {got}")
            check(
                ask("state")["n"] == want - 1,
                f"n = {want} does not show the step {want - 1} -> {want}",
            )
            r = ask("range")
            check(
                r["from"] == want and r["to"] == want,
                f"choosing n = {want} did not set both ends of the range: {r}",
            )
        # A chip is the same thing through the DOM.
        clicked = look("chips/click", n=110)
        check(
            clicked["from"] == 110 and clicked["to"] == 110,
            f"a chip does not set both ends: {clicked}",
        )
        chips = look("chips/numbers")
        check(
            chips == [5, 10, 11, 17, 26, 29, 100, 110, 272], f"the quick-pick chips are {chips}"
        )
        lo = ask("setStepN", -40)
        hi = ask("setStepN", 100000)
        check(lo == ask("pairs")[0]["n"] + 1, f"the chooser does not clamp low (got {lo})")
        check(hi == ask("pairs")[-1]["n"] + 1, f"the chooser does not clamp high (got {hi})")
        ask("setStepN", 17)
        note = text_of("step-note")
        check(
            "whole-configuration" in note or "whole configuration" in note,
            f"the n = 17 note does not say what makes 17 worth playing with: {note!r}",
        )

        # ---- step 3: the range spine. Guarded so a page built before this feature reports the
        # missing calls above rather than dying on the first one.
        if not {"setRange", "range", "playRange"} <= api:
            browser.close()
            print("FAILED")
            for failure in dict.fromkeys(failures):
                print(" -", failure)
            print(" - the range and the gap bar were not driven: the API is not there yet")
            return 1
        corpus = ask("pairs")
        first, last = corpus[0]["n"] + 1, corpus[-1]["n"] + 1
        # One click widens the range to the whole corpus.
        look("dom/click", id="range-all")
        rng = ask("range")
        check(
            rng["from"] == first and rng["to"] == last,
            f"the corpus button does not widen to {first}..{last}: {rng}",
        )
        check(
            rng["steps"] == len(corpus),
            f"the corpus range is {rng['steps']} steps, not every pair the page carries",
        )
        check(
            rng["duration"] > 60,
            f"the corpus run's duration reads {rng['duration']}, which is not minutes",
        )
        # The span the range covers, read from the n it steps from through the n it steps into. It
        # used to be checked on the numerals of the progress scale along the bottom of the stage;
        # the owner found that distracting and it is gone, so the span is read from the range itself,
        # which is what the scale was drawing.
        check(
            rng["from"] == first and rng["to"] == last,
            f"the corpus range does not span {first}..{last}: {rng}",
        )
        # Clamped to what the page carries, and to from <= to.
        r = ask("setRange", -10, 100000)
        check(
            r["from"] == first and r["to"] == last,
            f"the range does not clamp to what the page carries: {r}",
        )
        r = ask("setRange", 80, 20)
        check(r["from"] <= r["to"], f"the range allows from > to: {r}")
        # A one-step range is the old Single step tab: the two readouts collapse with it.
        r = ask("setRange", 17, 17)
        check(
            r["steps"] == 1 and r["from"] == 17 and r["to"] == 17,
            f"17 to 17 is not one step: {r}",
        )
        check(ask("state")["n"] == 16, "17 to 17 does not show the step 16 -> 17")
        check(
            text_of("range-position").strip() == "",
            "the position readout is drawn for a one-step range",
        )
        check(
            ask("progress")["n"] in (16, 17),
            "a one-step range does not put the step 16 -> 17 on the stage",
        )
        # A range of more than one step: the run is scoped to it and both readouts come back.
        r = ask("setRange", 2, 100)
        check(r["steps"] == 99, f"2..100 is {r['steps']} steps, expected 99")
        check(r["from"] == 2 and r["to"] == 100, f"the range does not span 2..100: {r}")
        drive(("setStyle", "tween"), ("playRange",), ("pause",))
        check(ask("state")["n"] == 1, "playRange does not start at the range's first step")
        pos = ask("range")
        check(
            pos["step"] == 1,
            f"the position readout says step {pos['step']} at the start of the run",
        )
        readout = text_of("range-position")
        check(
            "1" in readout and "99" in readout,
            f"the position readout does not read as step k of 99: {readout!r}",
        )
        duration_readout = text_of("range-duration")
        check(
            "99 steps" in duration_readout,
            f"the duration readout does not price 99 steps: {duration_readout!r}",
        )
        ask("goTo", 99)
        check(ask("range")["step"] == 99, "the last step of 2..100 is not step 99")
        end = look("range/last-step", lo=2, hi=4, step=3)
        check(end["n"] == 3 and end["last"] == 4, f"the range's last step is not 3 -> 4: {end}")
        drive(("stopAll",), ("setRange", 17, 17))

        # ---- step 4: the gap bar. Guarded the same way as step 3.
        if "gapBar" not in api:
            browser.close()
            print("FAILED")
            for failure in dict.fromkeys(failures):
                print(" -", failure)
            print(" - the gap bar was not driven: gapBar is not on the API yet")
            return 1
        # **The bar is keyed to the n on the panel, so it is read where the panel says 17.** Through
        # the dwell the stage shows the packing of 16 and both say 16; the roll carries both to 17.
        # Read at t = 0 the bar used to describe 17 while the stage showed 16's packing, which is how
        # a 25-square packing came to sit eleven per cent "under the best known" at the step into 26.
        drive(("setStepN", 17), ("setStyle", "tween"))
        ask("seek", 0)
        dwell = ask("gapBar")
        shown = ask("progress")["n"]
        check(
            dwell["n"] == shown,
            f"through the dwell the bar describes n = {dwell['n']} and the panel n = {shown}",
        )
        seek_to_end()
        bar = ask("gapBar")
        check(
            bar["n"] == ask("progress")["n"] == 17,
            f"at rest the bar describes n = {bar['n']}, not the 17 the panel shows",
        )
        facts = look("atlas/facts", n=17)
        check(
            abs(bar["record"] - float(facts["side"])) < 1e-9,
            f"the bar's record {bar['record']} is not the panel's s(17) <= {facts['side']}",
        )
        check(
            abs(bar["lower"] - float(facts["lower"])) < 1e-9,
            f"the bar's lower bound {bar['lower']} is not the panel's s(17) >= {facts['lower']}",
        )
        check(
            bar["lo"] <= bar["lower"] + 1e-9,
            f"the bar's scale starts above the lower bound: {bar}",
        )
        check(
            bar["hi"] > bar["record"], f"the bar's scale does not reach past the record: {bar}"
        )
        # **The scale runs between whole integers, and the same width at every n.** It used to run
        # from the area bound `sqrt(n)` to one above, so both ends moved with every n and nothing
        # on the bar was ever twice in the same place. It now runs from `floor(sqrt(n))` to two
        # above, so it changes only when `floor(sqrt(n))` does -- once per perfect square -- and a
        # reader watching a sweep has something that holds still.
        #
        # `sqrt(n)` is still on the bar, as a mark rather than an end: it is the one bound here
        # that needs no citation, since n unit squares have area n. A constant span is still what
        # makes two bars comparable. Checked at both ends of the corpus, and at a perfect square,
        # where `sqrt(n)` IS the left end and the record sits hard against it.
        for size in (16, 17, 324):
            if ask("setStepN", size) != size:
                continue
            seek_to_end()
            scale = ask("gapBar")
            check(
                abs(scale["lo"] - math.floor(math.sqrt(size))) < 1e-9,
                f"the bar at n = {size} starts at {scale['lo']}, "
                f"not the integer below the area bound, {math.floor(math.sqrt(size))}",
            )
            check(
                abs((scale["hi"] - scale["lo"]) - 2.0) < 1e-9,
                f"the bar at n = {size} spans {scale['hi'] - scale['lo']}, not 2",
            )
            check(
                scale["lo"] <= math.sqrt(size) <= scale["hi"]
                and scale["lo"] <= math.sqrt(size) + 1 <= scale["hi"],
                f"the bar at n = {size} does not contain both sqrt(n) and sqrt(n) + 1: {scale}",
            )
        ask("setStepN", 17)
        # **The pointer is drawn only where the arrangement is a packing.** A bounding box reports a
        # number for any arrangement, including one whose squares are inside each other, and that
        # number is smaller than the record -- which is how a frame mid-move came to read as better
        # than the best known. Measured: a retained record scores 0 to 1.3e-5 of a unit side of
        # summed overlap, the float precision of the poses; the same step mid-move reaches 1.1 at
        # n = 11 and 12.4 at n = 110.
        seek_to_end(("setStyle", "physics"))
        rest = ask("gapBar")
        check(
            rest["valid"] and rest["overlap"] < 1e-4,
            f"the retained record does not read as a packing: overlap {rest['overlap']}",
        )
        check(
            look("dom/attribute-number", id="gapbar-hand", name="opacity") == 1,
            "the pointer is hidden on a valid packing",
        )
        sc = ask("schedule")
        ask("seek", (sc["moveStart"] + sc["moveEnd"]) / 2)
        moving = ask("gapBar")
        check(
            not moving["valid"] and moving["overlap"] > 1e-4,
            f"a frame mid-move reads as a packing: overlap {moving['overlap']}",
        )
        check(
            look("dom/attribute-number", id="gapbar-hand", name="opacity") == 0,
            "the pointer claims a side for an arrangement that is not a packing",
        )
        ask("setStyle", "tween")
        # Under style A the indicator sweeps to the record and the check turns green.
        seek_to_end()
        end_bar = ask("gapBar")
        check(
            end_bar["met"],
            f"style A does not reach the record by the end of the step: {end_bar}",
        )
        check(
            abs(end_bar["excess"]) < 0.05, f"the excess at rest is {end_bar['excess']} per cent"
        )

        # The HAND is what turns green on a hit. It was a tick box in a head row, then a triangle,
        # and is now a line through the track -- the bar's two arrows are the bounds and the hand is
        # the only mark that moves, so it does not need a shape to argue for it. The property has
        # survived all three: the mark that says where the arrangement is changes colour when the
        # arrangement is the record.
        def hand_colour() -> str:
            return look("dom/computed", id="gapbar-hand", property="stroke")

        tick_colour = hand_colour()
        drive(("setStyle", "bodies"), ("setSnap", False), ("seek", 2.0))
        mid = ask("gapBar")
        check(not mid["met"], f"the check reads met in the middle of a free run: {mid}")
        mid_colour = hand_colour()
        check(
            tick_colour != mid_colour,
            f"the hand does not change colour when the record is met ({tick_colour})",
        )
        check(0 <= mid["x"] <= 1, f"the indicator is off the bar: {mid}")
        # In blind mode the bar still means something: the side comparison is all it needs.
        drive(("setBlind", True), ("seek", 2.0))
        blind = ask("gapBar")
        check(
            blind["side"] > 0 and 0 <= blind["x"] <= 1,
            f"the bar loses its indicator in blind mode: {blind}",
        )
        drive(("setBlind", False), ("setSnap", True), ("setStyle", "tween"))
        # The headline left the panel: it sits centred under the packing it names, which gave the
        # panel back its room for the facts. So the clearance it needs is from the picture rather
        # than from the bar -- it must sit below the packing and inside the stage -- and the bar,
        # now the first thing in the column, must stay inside the panel's own width.
        geom = look("gapbar/clearance")
        # The bar's own geometry: the shaded open span is a band inside the track, from the lower
        # bound's tick to the record's, and the two numbers do not sit on each other. (The band was
        # 76 px tall on its first build: `height` is a CSS property on an SVG rect, and the class
        # name it had then was the panel's own `.open` slot.)
        parts = look("gapbar/parts")
        # The scale's reference marks: the three integers the bar spans, plus `sqrt(n)` and
        # `sqrt(n) + 1`. At a perfect square those two ARE integers and collapse onto the marks
        # already there, so the count is three; everywhere else it is five. Every mark carries
        # its value, so the two counts agree.
        perfect = math.isqrt(17) ** 2 == 17
        expected_marks = 3 if perfect else 5
        check(
            parts["refTicks"] == expected_marks and len(parts["refNums"]) == expected_marks,
            f"the scale carries {parts['refTicks']} marks and {len(parts['refNums'])} numbers "
            f"at n = 17, expected {expected_marks} of each",
        )
        # An exact integer is written as one. `5`, not `5.00`: the second says a measurement was
        # taken to two places when the value is four.
        integers = [value for value in parts["refNums"] if "." not in value]
        check(
            len(integers) == 3,
            f"the scale's three integer marks are not written as integers: {parts['refNums']}",
        )
        check(
            parts["open"]["t"] >= parts["track"]["t"] - 0.5
            and parts["open"]["b"] <= parts["track"]["b"] + 0.5,
            f"the shaded open span is not a band inside the track: {parts['open']} against {parts['track']}",
        )
        # The two bounds are bold vertical rules. A rule has width, so the span is compared
        # against their CENTRES rather than their edges -- which is also what makes the check
        # independent of how bold "bold" is.
        low_mid = (parts["low"]["l"] + parts["low"]["r"]) / 2
        rec_mid = (parts["rec"]["l"] + parts["rec"]["r"]) / 2
        check(
            abs(parts["open"]["l"] - low_mid) < 3 and abs(parts["open"]["r"] - rec_mid) < 3,
            f"the shaded span does not run from the lower bound to the record: {parts}",
        )
        # Both values share one line above the rail now, so they dodge each other sideways
        # rather than being separated by being on different sides of it. What must hold is the
        # same either way: they do not overlap.
        apart = (
            parts["lowLabel"]["r"] < parts["recLabel"]["l"] - 0.5
            or parts["recLabel"]["r"] < parts["lowLabel"]["l"] - 0.5
            or parts["lowLabel"]["t"] > parts["recLabel"]["b"] - 0.5
            or parts["recLabel"]["t"] > parts["lowLabel"]["b"] - 0.5
        )
        check(
            apart, f"the bar's two numbers overlap: {parts['lowLabel']} and {parts['recLabel']}"
        )
        check(geom["shown"], "the gap bar is not drawn")
        check(
            geom["headTop"] >= geom["packBottom"] - 0.5,
            f"the headline overlaps the packing: {geom}",
        )
        check(
            geom["headBottom"] <= geom["stageBottom"] + 0.5,
            f"the headline runs off the stage: {geom}",
        )
        check(
            geom["right"] <= geom["panelRight"] + 0.5,
            f"the gap bar runs past the panel: {geom}",
        )

        # ---- step 5 (revision 9): the bar stops animating. The sparkline is gone, the hand holds
        # still through the motion, and it catches up when the picture settles.
        check(not in_page("gap-spark"), "the per-frame sparkline is still in the page")
        check("refreshGap" in api, "the API lacks refreshGap")
        # n = 101, not 100: 99 -> 100 is a grid prefix where nothing moves, so the bar would be on the
        # record for the whole step and "it held still" would prove nothing.
        drive(
            ("setStepN", 101),
            ("setStyle", "bodies"),
            ("setSnap", False),
            ("setTiming", {"dwell": 0.4, "move": 2.5, "settle": 0.4}),
        )
        # The third sample used to be the live readout's text, which is gone with the readout. The
        # summed overlap replaces it and is a better witness for the same property: it is measured
        # from the poses of every frame, so it moves while the bar deliberately does not.
        look("gapbar/sample-run")
        page.wait_for_timeout(4500)
        samples = look("gapbar/samples")
        mid = [r for r in samples if 0.6 < r[0] < 2.6]
        check(len(mid) >= 10, f"the run gave only {len(mid)} samples in the middle of the move")
        hands = {round(r[1], 9) for r in mid}
        rows = {r[2] for r in mid}
        check(
            len(hands) == 1,
            f"the gap bar's hand moved {len(hands)} times mid-motion: it should hold still",
        )
        check(
            len(rows) > 5,
            f"the frame's own measurement froze with the bar ({len(rows)} distinct values over {len(mid)} samples)",
        )
        settled = ask("gapBar")["x"]
        check(
            abs(settled - mid[0][1]) > 1e-6, "the bar never caught up once the motion settled"
        )
        # On demand, mid-motion, with nothing else touched.
        held = look("gapbar/refresh-on-demand", before=1.2, after=2.2)
        check(
            abs(held["demand"] - held["after"]) < 1e-9,
            f"refreshGap does not read the current frame: {held}",
        )
        drive(
            ("setTiming", {"dwell": 1.0, "move": 1.4, "settle": 0.4}),
            ("setSnap", True),
            ("setStyle", "tween"),
            ("setStepN", 17),
        )

        # ---- step 6 (revision 9): initial conditions and the open-ended Optimize run.
        for name in (
            "setInitial",
            "initial",
            "optimize",
            "optimizeState",
            "optimizeStep",
            "setSpeed",
            "speed",
        ):
            check(name in api, f"the API lacks {name}")
        # Revision 16: `record` joined them, the retained packing of n itself. It is last because
        # it is the least common start and its use is diagnostic rather than exploratory: put a
        # known optimum on the stage and see whether the law holds it.
        check(
            ask("initials") == ["previous", "random", "grid", "record"],
            "the initial conditions are not previous / random / grid / record",
        )
        check(ask("initial") == "previous", "the default start is not the previous packing")
        # Revision 9 removed the snap checkbox because an open-ended run had nothing to snap to.
        # Revision 11 brings it back as one of the two chart options, beside the contact bias, and
        # the two are different claims: the snap ends on the record by construction, the bias only
        # says which pairs should touch. Both are on the page and both drive the API.
        snap_box = look("controls/chart-options")
        check(snap_box is not None, "the two chart options are not both on the page")
        check(
            snap_box == {"snap": ask("state")["snap"], "bias": False},
            f"the chart options do not agree with the state they drive: {snap_box}",
        )
        check(
            "setSnap" in api,
            "setSnap was removed from the API rather than only from the controls",
        )
        check(in_page("initial-seg"), "there is no initial-conditions chooser")
        check(in_page("optimize"), "there is no Optimize button")
        ask("setStepN", 17)
        record17 = look("atlas/record-side", n=17)
        starts = {}
        for kind in ("random", "grid", "previous"):
            look("optimize/arm-start", kind=kind)
            st = ask("optimizeState")
            starts[kind] = st
            check(
                st["on"] and st["initial"] == kind, f"the {kind} start did not arm a run: {st}"
            )
            check(st["n"] == 17, f"the {kind} start built {st['n']} squares, not 17")
            check(st["steps"] == 0, f"the {kind} start is already {st['steps']} steps in")
        # Random and grid have no correspondence to the record, so they run without target springs;
        # the previous packing with the blind box off does have one.
        check(
            not starts["random"]["springs"] and not starts["grid"]["springs"],
            "a random or grid start was given the record's poses to spring at",
        )
        check(starts["previous"]["springs"], "the previous start lost its target springs")
        # The grid start is the trivial grid: axis-aligned, in a box of side ceil(sqrt(n)).
        check(
            abs(starts["grid"]["side"] - 5) < 1e-9,
            f"the grid start's box is {starts['grid']['side']}, not 5 for n = 17",
        )
        check(
            starts["random"]["side"] > record17,
            "the random start's box is not larger than the record",
        )
        # Random is deterministic: the same n and the same kind give the same arrangement.
        again = look("optimize/random-repeatable")
        check(
            abs(again - starts["random"]["required"]) < 1e-12,
            f"the random start is not reproducible: {again} vs {starts['random']['required']}",
        )
        # An open-ended run advances state rather than reading a cache, and keeps going.
        run = look("optimize/accumulates", n=17, steps=1200)
        check(
            run["b"]["steps"] == 1200 and run["c"]["steps"] == 2400,
            f"the run does not accumulate steps: {run}",
        )
        check(
            run["c"]["time"] > run["b"]["time"] > 0, f"simulated time does not advance: {run}"
        )
        check(
            run["c"]["side"] < run["a"]["side"] - 1e-3,
            f"the walls never closed on the grid start: {run}",
        )
        check(
            run["c"]["required"] < run["a"]["required"] - 1e-3,
            f"the run made the arrangement no smaller: {run['a']['required']} -> {run['c']['required']}",
        )
        check(
            run["c"]["best"] is not None and run["c"]["bestPenetration"] is not None,
            f"the run reports no smallest box and no overlap beside it: {run['c']}",
        )
        # And it reports all four figures. They used to be read off the rows under the stage; the
        # owner had those dropped, so they are read from the API that filled them -- which is where
        # a number belongs, and is what `grade_motion.py` and the capture receipt read too.
        said = ask("optimizeState")
        for field in ("time", "steps", "best", "bestPenetration", "record"):
            check(said.get(field) is not None, f"the run does not report its {field}: {said}")
        # Play resumes and pause stops it where it stands.
        held = look("optimize/play-resumes", speed=1)
        page.wait_for_timeout(700)
        after = drive(("pause",), ("optimizeState",))
        check(held["playing"], "play did not resume the run")
        check(
            after["steps"] > held["steps"],
            f"the run did not advance while playing: {held} -> {after}",
        )
        page.wait_for_timeout(300)
        stopped = ask("optimizeState")
        check(
            stopped["steps"] == after["steps"],
            f"the run kept going after pause: {after['steps']} -> {stopped['steps']}",
        )
        # Seeking is how the timeline is come back to.
        ask("seek", 0)
        check(not ask("state")["optimizing"], "a seek did not leave the open-ended run")
        check(ask("state")["optimizing"] is False, "the run survived leaving it")
        drive(("setInitial", "previous"), ("setStepN", 17))

        # ---- step 7 (revision 9): the hand.
        for name in ("pickAt", "grab", "dragTo", "release", "hand"):
            check(name in api, f"the API lacks {name}")
        # Grabbing from the timeline hands the picture to an open-ended run seeded where it stood.
        drive(("setStepN", 17), ("setStyle", "tween"), ("seek", 0))
        grabbed = look("hand/grab-from-timeline", x=2.5, y=2.5)
        check(grabbed["i"] >= 0, "nothing was picked at the middle of the packing")
        check(
            grabbed["g"] == grabbed["i"] and not grabbed["before"] and grabbed["optimizing"],
            f"a grab from the timeline did not start an open-ended run: {grabbed}",
        )
        check(grabbed["edited"], "a dragged run is not marked hand-edited")
        check(
            ask("optimizeState")["edited"] is True,
            "the run does not report that it was hand-edited",
        )
        ask("release")
        # Pinned: the held square follows the cursor exactly and its neighbours are pushed aside.
        pin = look(
            "hand/pinned-drag",
            n=17,
            steps=400,
            settle=300,
            at=[0.5, 0.5],
            to=[1.2, 0.5],
            neighbour=[1.9, 0.5],
        )
        check(pin["held"] == pin["i"], f"the square was not held through the drag: {pin}")
        check(
            pin["stillThere"], "the held square did not stay exactly where the cursor left it"
        )
        check(pin["neighbourMoved"], "the run did not push the held square's neighbour aside")
        check(pin["after"] == -1, "the square was not dropped on release")
        # Shift turns it about its own centre.
        turn = look(
            "hand/shift-turns",
            n=17,
            at=[0.5, 0.5],
            grab=[1.0, 0.5],
            first=[1.0, 0.5],
            second=[0.5, 1.0],
        )
        check(
            abs(turn["a"]["angle"]) < 1e-6,
            f"the first shifted move already turned the square: {turn['a']}",
        )
        check(
            abs(turn["b"]["angle"] - 90) < 1e-6,
            f"a quarter turn of the cursor did not turn it 90 degrees: {turn['b']}",
        )
        check(
            abs(turn["b"]["x"] - turn["a"]["x"]) < 1e-9
            and abs(turn["b"]["y"] - turn["a"]["y"]) < 1e-9,
            f"a shifted drag moved the square's centre: {turn}",
        )
        # The readout follows the drag at once.
        moved = look("hand/readout-follows", n=17, at=[0.5, 0.5], to=[7.5, 0.5])
        check(
            abs(moved["before"] - moved["after"]) > 1e-9,
            f"the measured side did not follow the drag: {moved}",
        )
        # And a drag while a run is playing leaves it playing.
        live = look("hand/grab-while-playing", n=17, x=2.5, y=2.5)
        check(
            live["held"] >= 0 and live["playing"] and live["optimizing"],
            f"a grab during playback did not carry on running: {live}",
        )
        # No keyboard control regressed.
        drive(("setInitial", "previous"), ("setStepN", 17), ("seek", 0))
        page.keyboard.press("ArrowRight")
        check(ask("stepN") == 18, "the right arrow no longer steps n")
        page.keyboard.press("ArrowLeft")
        check(ask("stepN") == 17, "the left arrow no longer steps n")
        page.keyboard.press("p")
        check(ask("state")["style"] == "physics", "the p key no longer cycles the style")
        page.keyboard.press("p")
        page.keyboard.press("p")
        page.keyboard.press(" ")
        check(ask("state")["playing"], "the space bar no longer plays")
        page.keyboard.press(" ")
        check(not ask("state")["playing"], "the space bar no longer pauses")

        # ---- step 8 (revision 10): the two modes, and what each of them plays.
        if "setMode" not in api:
            browser.close()
            print("FAILED")
            for failure in dict.fromkeys(failures):
                print(" -", failure)
            print(" - the modes were not driven: setMode is not on the API yet")
            return 1
        drive(("setMode", "pack"), ("setStepN", 17))
        check(ask("mode") == "pack", "setMode('pack') did not select Pack")
        tabs = look("modes/tabs")
        check(
            [t[0] for t in tabs] == ["pack", "animate"],
            f"the sub-panel does not carry two modes: {tabs}",
        )
        check(
            tabs[0][2] == "true" and tabs[1][2] == "false",
            f"the pressed tab is not Pack: {tabs}",
        )
        # Pack is one number: the second box, the separator, the corpus button and the two figures
        # that price a fixed-length run are Animate's.
        chooser = [
            "range-to",
            "range-sep",
            "range-all",
            "range-duration",
            "range-position",
            "step-chips",
        ]
        packing = look("modes/chooser-hidden", ids=chooser)
        check(
            dict(packing)
            == {
                "range-to": True,
                "range-sep": True,
                "range-all": True,
                "range-duration": True,
                "range-position": True,
                "step-chips": False,
            },
            f"Pack shows the wrong pieces of the chooser: {packing}",
        )
        # In Pack the range's two ends stay equal whatever the chooser is asked for.
        for want in (11, 29, 100):
            ask("setStepN", want)
            r = ask("range")
            check(
                r["from"] == want and r["to"] == want,
                f"Pack let the range come apart at n = {want}: {r}",
            )
            check(ask("mode") == "pack", f"choosing n = {want} left Pack")
        # Pack's playback is the open-ended run: press play and it optimises until pause.
        drive(("setStepN", 17), ("setInitial", "grid"), ("setSpeed", 1))
        look("dom/click", id="play")
        page.wait_for_timeout(700)
        ran = look("optimize/state-then-pause")
        check(
            ran["on"] and ran["steps"] > 0,
            f"the transport in Pack did not start an open-ended run: {ran}",
        )
        # And the readout is a seconds counter with the step count beside it, not a t / duration.
        counter = text_of("clock")
        check(
            " s " in counter and "steps" in counter and "/" not in counter,
            f"Pack's readout is not a seconds counter with the step count: {counter!r}",
        )
        # Play again resumes the same run rather than restarting it.
        before = ask("optimizeState")["steps"]
        look("dom/click", id="play")
        page.wait_for_timeout(500)
        after = look("optimize/steps-then-pause")
        check(after > before, f"the transport did not resume the run: {before} -> {after}")
        # Animate: a range, always, and the pieces Pack hides come back. It comes back on the range it
        # was last left on rather than on whatever Pack collapsed to.
        drive(("setMode", "animate"), ("setRange", 30, 90))
        drive(("setMode", "pack"), ("setMode", "animate"))
        rng = ask("range")
        check(ask("mode") == "animate", "setMode('animate') did not select Animate")
        check(
            rng["from"] == 30 and rng["to"] == 90,
            f"Animate did not come back on the range it was left on: {rng}",
        )
        animating = look("modes/chooser-hidden", ids=chooser)
        check(
            dict(animating)
            == {
                "range-to": False,
                "range-sep": False,
                "range-all": False,
                "range-duration": False,
                "range-position": False,
                "step-chips": True,
            },
            f"Animate shows the wrong pieces of the chooser: {animating}",
        )
        # A shared strategy setting survives a switch in both directions, which is the whole point of
        # the modes being two aspects of one page rather than two pages.
        drive(
            ("setStyle", "bodies"),
            ("setAnneal", 7),
            ("setSpeed", 0.5),
            ("setInitial", "random"),
            ("setDesaturate", False),
            ("setRange", 30, 60),
        )
        kept = look("modes/shared-settings")
        check(
            kept["style"] == "bodies"
            and kept["anneal"] == 7
            and abs(kept["speed"] - 0.5) < 1e-9
            and kept["initial"] == "random"
            and kept["desaturate"] is False,
            f"a mode switch lost a shared setting: {kept}",
        )
        check(
            kept["range"]["from"] == 30 and kept["range"]["to"] == 60,
            f"Animate did not remember the range it was left on: {kept['range']}",
        )
        # `setRange` still works as it did; a range wider than one step names Animate, since Pack has
        # no way to show one.
        forced = look("modes/wide-range-from-pack", lo=40, hi=44)
        check(
            forced["mode"] == "animate" and forced["range"]["steps"] == 5,
            f"a wide range set from Pack did not put the page in Animate: {forced}",
        )
        drive(("setStyle", "tween"), ("setAnneal", 3), ("setSpeed", 1))
        drive(("setDesaturate", True), ("setInitial", "previous"))
        drive(("setMode", "pack"), ("setStepN", 17))

        # ---- step 9 (revision 11): the colouring is the angle map, and only that. Guarded like the
        # steps above so a page built before the revision reports the missing calls rather than
        # dying on the first one.
        if not {"colour", "fillsFor"} <= api:
            browser.close()
            print("FAILED")
            for failure in dict.fromkeys(failures):
                print(" -", failure)
            print(" - the colouring was not driven: colour / fillsFor are not on the API yet")
            return 1
        # The stage trims chroma to compensate for drawing one packing where the atlas draws a page
        # of them, so the fills on the stage are a step under the palette's by default. Every check
        # below is about the PALETTE -- which hue a class takes, which shade a contact count takes,
        # that a square keeps its fill through a turn -- so they are taken with the trim off, and
        # the trim gets one check of its own: that it is on by default, and that turning it off is
        # what puts the stage back on the atlas's own numbers.
        check(
            abs(ask("stageChroma") - 0.85) < 1e-9,
            f"the stage's chroma trim is {ask('stageChroma')}, not 0.85",
        )
        check(
            ask("setStageChroma", 1) == 1,
            "the stage's chroma trim does not go back to the atlas's own numbers",
        )
        # Revision 12 put three schemes where revision 11 had one, and made the square's *identity*
        # the default, so the angle map has to be selected before it can be checked. The default is
        # read here, before anything switches it, because "identity is the default" is the claim.
        check(
            ask("colorScheme") == "identity",
            f"the page does not open in the identity scheme: {ask('colorScheme')}",
        )
        check(
            ask("colorSchemes") == ["identity", "angle-stable", "angle-continuous"],
            f"the three schemes are {ask('colorSchemes')}",
        )
        # The desaturation is revision 6's and is a separate thing: it drains chroma out of the very
        # fills this step is reading, so it comes off for the whole step and goes back on at the end.
        drive(
            ("setMode", "pack"),
            ("setStyle", "tween"),
            ("setSnap", True),
            ("setDesaturate", False),
            ("setColorScheme", "angle-stable"),
        )
        check(ask("colorScheme") == "angle-stable", "the angle map could not be selected")
        book = ask("colour")
        palette, shades, tol = book["palette"], book["shades"], book["tolerance"]
        check(abs(tol - 0.5) < 1e-12, f"the angle tolerance is {tol}, not half a degree")
        check(
            abs(book["contactGap"] - 0.01) < 1e-12,
            f"the contact gap is {book['contactGap']}, not a hundredth of a side",
        )
        check(
            len(palette) == 20 and len(shades) == 20 and all(len(f) == 5 for f in shades),
            f"the map is not twenty hues of five shades: {len(palette)} hues, {[len(f) for f in shades]}",
        )
        check(
            palette[0] == "#1faa8e" and palette[1] == "#c3c45f",
            f"the two pinned slots are not the house teal and citron: {palette[:2]}",
        )
        # Every fill on the stage is looked up here, so the hundred hexes have to name one family and
        # one shade each; two families sharing a hex would make the readings below ambiguous.
        family = {h: (s, j) for s, fam in enumerate(shades) for j, h in enumerate(fam)}
        check(
            len(family) == 100,
            f"the twenty families are not a hundred distinct hexes ({len(family)})",
        )
        band = 90 / (len(palette) - 2)

        # 9a. The same angle takes the same fill in every retained packing that holds it. Each of
        # these is settled on its own retained frame first, which under style A with the snap on is
        # the record's own packing for n.
        frames = {}
        for want in (5, 11, 17, 26, 29, 100, 110, 172, 272, 324):
            if not (first <= want <= last):
                continue
            if ask("setStepN", want) != want:
                continue
            seek_to_end()
            frames[want] = ask("colour")
        check(
            {17, 29, 100, 272} <= set(frames),
            f"the four retained frames this step needs are not all on the page: {sorted(frames)}",
        )
        for n, c in frames.items():
            check(
                len(c["fills"]) == n and len(c["contacts"]) == n,
                f"n = {n} drew {len(c['fills'])} squares against {len(c['contacts'])} contact counts",
            )
            stray = [f for f in c["fills"] if f not in family]
            check(stray == [], f"n = {n} painted {stray[:3]}, which is in no palette family")
            # The whole frame, read back off the DOM and taken apart: the family histogram is the
            # classes' own slots weighted by their sizes (two classes may land on one slot, so they
            # are summed), and the shade histogram is 4 - contacts, square for square. Together
            # these say the picture is exactly what `colour()` claims it was painted from.
            drawn_family = Counter(family[f][0] for f in c["fills"] if f in family)
            want_family: Counter[int] = Counter()
            for slot, size in zip(c["slots"], c["sizes"]):
                want_family[slot] += size
            check(
                drawn_family == want_family,
                f"n = {n}'s families are {dict(drawn_family)}, not the classes' slots {dict(want_family)}",
            )
            drawn_shade = Counter(family[f][1] for f in c["fills"] if f in family)
            want_shade = Counter(4 - max(0, min(4, k)) for k in c["contacts"])
            check(
                drawn_shade == want_shade,
                f"n = {n}'s shades are {dict(drawn_shade)}, not 4 - contacts {dict(want_shade)}",
            )
            # And the slot a class took is the pure function of its own centre: asking `fillsFor`
            # for that one angle, with nothing else in the array, gives the same family back. This
            # is what kills the old house rule, under which a class's colour was its rank among the
            # frame's other classes and so moved when the frame did.
            alone = look("colour/fills-for-angles", angles=c["centres"])
            for centre, slot, hexed in zip(c["centres"], c["slots"], alone):
                check(
                    hexed == shades[slot][4],
                    f"n = {n}'s {centre:.4f} degree class took slot {slot}, but the angle alone gives {hexed}",
                )
        # The four the revision names, pairwise: a shared angle is a shared fill, at every contact
        # count, with no exception allowed.
        core = [n for n in (17, 29, 100, 272) if n in frames]
        shared = 0
        for i, a in enumerate(core):
            for b in core[i + 1 :]:
                for ca, sa in zip(frames[a]["centres"], frames[a]["slots"]):
                    for cb, sb in zip(frames[b]["centres"], frames[b]["slots"]):
                        if angle_gap(ca, cb) > tol:
                            continue
                        shared += 1
                        check(
                            sa == sb,
                            f"n = {a}'s {ca:.4f} degree class took slot {sa} while n = {b}'s {cb:.4f} took {sb}",
                        )
                        both = look("colour/fills-for-pair", angles=[ca, cb])
                        check(
                            all(x == y for x, y in both),
                            f"n = {a}'s {ca:.4f} and n = {b}'s {cb:.4f} are painted differently: {both}",
                        )
        check(
            shared >= 6,
            f"the four frames share only {shared} angles, so the check has no teeth",
        )
        # The wider sweep, where the one loophole in "hue is a function of the angle" shows up: the
        # slot is a step function with an edge every five degrees, and two classes within the half
        # degree that counts as the same tilt can still fall either side of one. Measured over the
        # ten frames above that happens exactly once — n = 29's 64.9387 degree class takes slot 14
        # and n = 110's 65.1299 takes slot 15 — so a disagreement is allowed only when the two
        # centres are in different bands, and then only to the neighbouring slot.
        agreed, straddles = 0, []
        wide = sorted(frames)
        for i, a in enumerate(wide):
            for b in wide[i + 1 :]:
                for ca, sa in zip(frames[a]["centres"], frames[a]["slots"]):
                    for cb, sb in zip(frames[b]["centres"], frames[b]["slots"]):
                        if angle_gap(ca, cb) > tol:
                            continue
                        if sa == sb:
                            agreed += 1
                        else:
                            straddles.append((a, ca, sa, b, cb, sb))
        check(agreed >= 40, f"the sweep found only {agreed} agreeing shared angles")
        for a, ca, sa, b, cb, sb in straddles:
            edge = min(fold_angle(ca) % band, band - fold_angle(ca) % band)
            check(
                int(fold_angle(ca) // band) != int(fold_angle(cb) // band)
                and abs(sa - sb) == 1
                and edge <= tol,
                f"n = {a}'s {ca:.4f} (slot {sa}) and n = {b}'s {cb:.4f} (slot {sb}) disagree without a band edge between them",
            )
        check(
            len(straddles) <= 2,
            f"{len(straddles)} shared angles fall either side of a band edge, not the one measured",
        )
        # `fillsFor` is the map with nothing on the stage, so its answer cannot depend on what is:
        # the same table comes back at every n, and it pins the tolerance and the five-degree band.
        sweep = [0.0, 0.4, 0.6, 12.3, 23.4513, 44.4, 44.6, 45.0, 45.3, 64.9387, 65.1299, 89.7]
        table = {}
        for n in wide:
            seek_to_end(("setStepN", n))
            table[n] = look("colour/fills-table", angles=sweep)
        for n in wide[1:]:
            check(
                table[n] == table[wide[0]],
                f"fillsFor answered differently with n = {n} on the stage",
            )
        pinned = look("colour/fills-for-angles", angles=[0.0, 0.4, 0.6, 44.4, 44.6, 45.0])
        check(
            [family[h][0] for h in pinned] == [0, 0, 2, 10, 1, 1],
            f"the half-degree pins and the five-degree bands are not where the revision puts them: {pinned}",
        )

        # 9b. A square whose angle does not move keeps its hue through a step. n = 110 carries twelve
        # angle classes and a real rotation, so the frame is not one colour throughout.
        # Revision 14: a step is Animate's, and it is asked for here. Pack has all n squares on the
        # stage from the first frame and never plays a transition, so scrubbing one there would find
        # a still arrangement and the check would prove nothing (measured: it found nothing turning).
        drive(("setMode", "animate"), ("setStepN", 110), ("setStyle", "tween"), ("seek", 0))
        span = ask("duration")
        snaps = []
        for fraction in (0.0, 0.15, 0.35, 0.5, 0.62, 0.75, 0.88, 1.0):
            ask("seek", span * fraction)
            rows = look("stage/drawn")
            # The map driven by the angles the frame actually drew, which is the same question the
            # painter asked, put to the pure function instead.
            pure = look("colour/fills-for-drawn", angles=[r[1] for r in rows])
            snaps.append({r[0]: (r[1], r[2], pure[i]) for i, r in enumerate(rows)})
        check(
            all(len(s) == 110 for s in snaps),
            f"the step did not draw 110 squares at every instant: {[len(s) for s in snaps]}",
        )
        turned = sum(
            1
            for k, v in snaps[0].items()
            if k in snaps[-1] and angle_gap(v[0], snaps[-1][k][0]) > tol
        )
        check(turned > 0, "no square turned over the step, so a held hue proves nothing")
        held, moved_hue = 0, []
        for i in range(len(snaps)):
            for j in range(i + 1, len(snaps)):
                for ident, (ang, fill, mapped) in snaps[i].items():
                    # The arriving square is tinted toward scarlet as it lands, which is the one
                    # fill this map does not have the last word on, so it is not read here.
                    if ident == 110 or ident not in snaps[j]:
                        continue
                    ang2, fill2, mapped2 = snaps[j][ident]
                    if angle_gap(ang, ang2) > tol:
                        continue
                    held += 1
                    drawn = (family.get(fill, (None,))[0], family.get(fill2, (None,))[0])
                    if (
                        drawn[0] is None
                        or drawn[0] != drawn[1]
                        or family[mapped][0] != family[mapped2][0]
                    ):
                        moved_hue.append((ident, ang, fill, ang2, fill2))
        check(held >= 500, f"only {held} square-instants held their angle over the step")
        check(moved_hue == [], f"a square kept its angle and changed hue: {moved_hue[:3]}")

        # 9c. A contact darkens without changing hue. First off the stage, where it is exact: the
        # five fills of one angle are one family, they run from the light end at no contacts to the
        # dark end at four, and the hue holds. The two pinned families ramp in OkLCh and hold to
        # within a degree; the eighteen free ones ramp in HSL, which drifts — 6.42 degrees at slot 6
        # is the worst of them — so they are held to seven.
        for slot in range(len(palette)):
            theta = 0.0 if slot == 0 else 45.0 if slot == 1 else band * (slot - 2) + band / 2
            ramp = look("colour/shade-ramp", angle=theta)
            check(
                [family.get(h, (None, None)) for h in ramp]
                == [(slot, 4), (slot, 3), (slot, 2), (slot, 1), (slot, 0)],
                f"{theta} degrees does not walk slot {slot} from its light end to its dark one: {ramp}",
            )
            lit = [oklab(h)[0] for h in ramp]
            check(
                all(lit[k] > lit[k + 1] for k in range(4)),
                f"slot {slot} does not darken as contacts rise: {[round(x, 4) for x in lit]}",
            )
            hues = [oklab(h)[2] for h in ramp]
            allowed = 1.0 if slot < 2 else 7.0
            spread = max(hue_gap(x, hues[0]) for x in hues)
            check(
                spread <= allowed,
                f"slot {slot}'s five shades span {spread:.2f} degrees of hue, over {allowed}",
            )
            check(
                max(hue_gap(x, oklab(palette[slot])[2]) for x in hues) <= allowed,
                f"slot {slot}'s shades are not the palette hue {palette[slot]}",
            )
        # Then on the stage. A grid start is every square upright, so the whole picture is one class
        # and one family, and the only thing left to tell the fills apart is the contact count.
        for n in (17, 26):
            drive(("setStepN", n), ("setInitial", "grid"))
            c = ask("colour")
            check(
                c["classes"] == 1
                and c["slots"] == [0]
                and angle_gap(c["centres"][0], 0) <= tol,
                f"the grid start at n = {n} is not one upright class: {c['classes']} classes at {c['centres']}",
            )
            hist = Counter(c["contacts"])
            check(
                len(hist) >= 3,
                f"the grid start at n = {n} has only the contact counts {sorted(hist)}",
            )
            check(
                Counter(c["fills"]) == Counter(shades[0][4 - k] for k in c["contacts"]),
                f"the grid start at n = {n} is not its own contact counts shaded: {sorted(Counter(c['fills']).items())}",
            )
            check(
                {family[f][0] for f in c["fills"]} == {0},
                f"an upright grid start at n = {n} painted more than the teal family",
            )
            counts = sorted(hist)
            lit = [oklab(shades[0][4 - k])[0] for k in counts]
            check(
                all(lit[i] > lit[i + 1] for i in range(len(lit) - 1)),
                f"the grid start's shades do not darken with contacts: {list(zip(counts, [round(x, 4) for x in lit]))}",
            )
        ask("setInitial", "previous")

        # 9d. The old rule switch is still gone. Revision 12's scheme chooser is not it: `rule-seg`
        # is not back, `setColorRule` is a no-op alias reporting the scheme in force, and the key
        # that used to cycle the rule still moves nothing.
        seek_to_end(("setStepN", 29))
        check(not in_page("rule-seg"), "the colour-rule chooser is still in the page")
        check(
            look("dom/count", selector="[data-rule]") == 0,
            "the page still carries a colour-rule control",
        )
        check(
            ask("state")["rule"] == "angle-stable",
            "state().rule does not report the scheme in force",
        )
        painted = ask("colour")["fills"]
        check(len(painted) == 29, f"the frame under test draws {len(painted)} squares, not 29")
        check(
            ask("setColorRule", "house") == "angle-stable",
            "setColorRule is not the no-op alias reporting the scheme",
        )
        check(ask("colour")["fills"] == painted, "setColorRule('house') repainted the stage")
        look("dom/blur")
        page.keyboard.press("k")
        page.wait_for_timeout(120)
        check(ask("colour")["fills"] == painted, "the k key repainted the stage")
        check(ask("state")["rule"] == "angle-stable", "the k key moved the scheme")

        # 9e (revision 12): colour is the square's identity, and that is the default. The claim is
        # stronger than the angle map's: a square's fill is a property of the square and of nothing
        # else, so it survives the square turning, its neighbours moving, and the frame being drawn
        # from a different start altogether.
        if "setColorScheme" not in api or "identityFills" not in api:
            browser.close()
            print("FAILED")
            for failure in dict.fromkeys(failures):
                print(" -", failure)
            print(" - the identity scheme was not driven: setColorScheme is not on the API yet")
            return 1
        ask("setColorScheme", "identity")
        greens = ask("colour")["greens"]
        check(
            len(greens) == 42,
            f"the identity ramp carries {len(greens)} greens, not the 42 measured",
        )
        check(
            len(set(greens)) == len(greens),
            "the identity ramp repeats a colour inside one period",
        )
        # Every one of them is a green: its OkLCh hue is inside the band the teal-to-citron ramp
        # spans, 109.4 to 174.6 degrees, and none is a colour the page reserves.
        for hexed in greens:
            _, chroma, hue = oklab(hexed)
            check(105.0 <= hue <= 179.0, f"{hexed} is at hue {hue:.1f}, outside the green band")
            check(
                chroma > 0.04,
                f"{hexed} has chroma {chroma:.3f} and is not a green so much as a grey",
            )
            check(
                hexed.lower() not in ("#a3123f", "#17794a"),
                f"an identity green is a colour the page reserves: {hexed}",
            )

        # The palette's own resolution, re-measured here rather than asserted: the closest two of the
        # 42 are 0.0237 apart in OkLab, and consecutive identities are five times further apart than
        # that, which is what the co-prime stride buys.
        def lab_dist(x: str, y: str) -> float:
            a, b = oklab(x), oklab(y)
            pa = (
                a[0],
                a[1] * math.cos(math.radians(a[2])),
                a[1] * math.sin(math.radians(a[2])),
            )
            pb = (
                b[0],
                b[1] * math.cos(math.radians(b[2])),
                b[1] * math.sin(math.radians(b[2])),
            )
            return math.dist(pa, pb)

        closest = min(
            lab_dist(greens[i], greens[j])
            for i in range(len(greens))
            for j in range(i + 1, len(greens))
        )
        check(
            closest >= 0.023,
            f"the two closest greens are {closest:.4f} apart, under the 0.0237 measured",
        )
        by_identity = ask("identityFills", 90)
        neighbours = min(
            lab_dist(by_identity[i], by_identity[i + 1]) for i in range(len(by_identity) - 1)
        )
        check(neighbours >= 0.10, f"neighbouring identities are only {neighbours:.4f} apart")
        check(
            by_identity[42:84] == by_identity[:42],
            "the ramp does not repeat with a period of 42",
        )
        check(
            sorted(by_identity[:42]) == sorted(greens),
            "the 42 identities do not use the 42 greens once each",
        )

        # A settle that turns the squares does not repaint them. n = 110 has a real rotation in it,
        # and the run is left free so the physics, not the record, decides where it lands.
        # Revision 14: a settle is a step's, so this is Animate's stage — with the standardising off,
        # because it is Animate that repaints a *resting* frame in the angle map and this check is
        # about the identity greens holding. 9f puts it back on and proves it fires.
        drive(
            ("setMode", "animate"),
            ("setAnimateStandardize", False),
            ("setStepN", 110),
            ("setStyle", "bodies"),
            ("setSnap", False),
            ("setDesaturate", False),
            ("seek", 0),
        )
        span = ask("duration")
        settle = []
        for fraction in (0.0, 0.3, 0.6, 1.0):
            ask("seek", span * fraction)
            settle.append({r[0]: (r[1], r[2]) for r in look("stage/drawn")})
        moved = sum(
            1
            for k, v in settle[0].items()
            if k in settle[-1] and angle_gap(v[0], settle[-1][k][0]) > 0.5
        )
        check(
            moved >= 5,
            f"only {moved} squares turned over the settle, so a held fill proves little",
        )
        repainted = [
            (k, settle[0][k][1], s[k][1])
            for s in settle[1:]
            for k in settle[0]
            # The arriving square — identity 110, the n the step lands on — leans toward scarlet as
            # it lands and settles to its own green, which is a mark and not a colouring.
            if k in s and k != 110 and settle[0][k][1] != s[k][1]
        ]
        check(repainted == [], f"a square changed colour while it turned: {repainted[:3]}")
        # And the same square is the same green in two different frames of the same n: the settled
        # step animation, and an open-ended run from the ordered fill, which shares nothing with it
        # but the labelling.
        seek_to_end(("setStepN", 29), ("setStyle", "tween"), ("setSnap", True))
        frame_one = {r[0]: r[2] for r in look("stage/drawn")}
        drive(
            ("setMode", "pack"), ("setStepN", 29), ("setInitial", "grid"), ("optimizeStep", 600)
        )
        frame_two = {r[0]: r[2] for r in look("stage/drawn")}
        check(
            len(frame_one) == 29 and len(frame_two) == 29,
            f"the two frames of n = 29 drew {len(frame_one)} and {len(frame_two)} squares",
        )
        differ = [k for k in frame_one if frame_one[k] != frame_two.get(k)]
        check(
            differ == [],
            f"two frames of n = 29 paint the same square differently: {differ[:5]}",
        )
        # And the fill a square is drawn with is its identity's own entry in the ramp, not merely
        # something stable: the pure function and the picture agree square by square.
        pure = ask("identityFills", 29)
        wrong = [
            (k, frame_one[k], pure[k - 1])
            for k in sorted(frame_one)
            if frame_one[k] != pure[k - 1]
        ]
        check(wrong == [], f"a drawn fill is not its identity's green: {wrong[:3]}")
        # Contacts do not shade the identity scheme, which is the decision revision 12 records: the
        # ordered fill at n = 17 carries three different contact counts and exactly seventeen
        # different greens, one a square, where the angle map would have painted it in three shades
        # of one hue.
        drive(("setStepN", 17), ("setInitial", "grid"), ("setColorScheme", "identity"))
        grid = ask("colour")
        check(
            len(set(grid["contacts"])) >= 3,
            f"the ordered fill at n = 17 has contacts {sorted(set(grid['contacts']))}",
        )
        check(
            len(set(grid["fills"])) == 17,
            f"identity painted the ordered fill in {len(set(grid['fills']))} colours, not 17",
        )
        ask("setColorScheme", "angle-stable")
        shaded = ask("colour")
        check(
            len(set(shaded["fills"])) == len(set(shaded["contacts"])),
            f"the angle map's ordered fill is {len(set(shaded['fills']))} fills for {len(set(shaded['contacts']))} contact counts",
        )

        # 9f (revision 12): the Animate exception, and it belongs to Animate alone. In Animate the resting
        # frame is repainted in the standard angle map while the motion stays identity-coloured; in
        # Pack nothing is repainted, whatever the setting says.
        drive(
            ("setInitial", "previous"),
            ("setColorScheme", "identity"),
            ("setMode", "animate"),
            ("setRange", 29, 29),
            ("setStyle", "tween"),
            ("setSnap", True),
            ("setAnimateStandardize", True),
        )
        check(
            ask("animateStandardize") is True, "the Animate standardising is not on by default"
        )
        span = ask("duration")
        ask("seek", span)
        rest = ask("colour")
        # `angle-atlas`, not `angle-stable`. The two group angles identically and differ in which
        # palette slot a class is given: the stable map gives a class the slot its own angle falls
        # in, so a square keeps its hue from frame to frame, while the atlas hands slots out from 2
        # by descending class size. A resting frame is a picture that is meant to match a rendering,
        # so it takes the atlas's answer -- measured before this changed, n = 17's tilted core came
        # out `#b9e53c`, the lightest fill in the ramp, against the rendering's `#dd87b8`.
        check(
            rest["painted"] == "angle-atlas" and rest["scheme"] == "identity",
            f"a resting Animate frame is painted {rest['painted']} with the scheme on {rest['scheme']}",
        )
        ask("seek", span * 0.55)
        mid = ask("colour")
        check(
            mid["painted"] == "identity",
            f"a moving Animate frame is painted {mid['painted']}, not in identity",
        )
        ask("setAnimateStandardize", False)
        ask("seek", span)
        check(
            ask("colour")["painted"] == "identity",
            "turning the Animate standardising off still repaints the resting frame",
        )
        seek_to_end(("setAnimateStandardize", True), ("setMode", "pack"), ("setStepN", 29))
        check(
            ask("colour")["painted"] == "identity",
            "Pack repaints its resting frame, which is Animate's setting and not Pack's",
        )
        check(
            look("dom/disabled", id="animate-standard-toggle") is True,
            "the Animate standardising box is live in Pack",
        )
        drive(("setDesaturate", True), ("setColorScheme", "identity"), ("setStepN", 17))

        # ---- step 10 (revision 11): one editable force law. Guarded like the steps above so a page
        # built before the revision reports the missing calls rather than dying on the first one.
        if (
            not {
                "setLaw",
                "law",
                "setLawPreset",
                "lawPresets",
                "lawCurve",
                "lawForce",
                "dragLaw",
            }
            <= api
        ):
            browser.close()
            print("FAILED")
            for failure in dict.fromkeys(failures):
                print(" -", failure)
            print(
                " - the law was not driven: setLaw / lawForce / dragLaw are not on the API yet"
            )
            return 1
        drive(
            ("setMode", "pack"),
            ("setStyle", "tween"),
            ("setStepN", 17),
            ("setLawPreset", "default"),
        )
        check(
            ask("lawPresets") == ["rigid", "soft", "sticky"],
            f"the three named laws are {ask('lawPresets')}",
        )
        shipped = ask("law")
        check(
            shipped["bounds"] == LAW_BOUNDS,
            f"the law's bounds are {shipped['bounds']}, not {LAW_BOUNDS}",
        )
        check(
            shipped["defaults"] == LAW_DEFAULT,
            f"the law's defaults are {shipped['defaults']}, not {LAW_DEFAULT}",
        )

        # 10a. The law's shape, against the formula written out at the top of this file rather than
        # against the page's own arithmetic. Four laws, and every breakpoint sampled exactly.
        for name in ("default", "rigid", "soft", "sticky"):
            want = LAW_DEFAULT if name == "default" else LAW_PRESETS[name]
            got = ask("setLawPreset", name)
            check(
                {k: got[k] for k in LAW_KEYS} == want,
                f"the {name} law is {[got[k] for k in LAW_KEYS]}, not {[want[k] for k in LAW_KEYS]}",
            )
            check(
                abs(got["steep"] - law_steep(want)) < 1e-12,
                f"the {name} law's steep is {got['steep']}, not the derived {law_steep(want)}",
            )
            ds = law_samples(want)
            fs = look("law/forces-at", gaps=ds)
            off = [
                (d, f, law_force(want, d))
                for d, f in zip(ds, fs)
                if abs(f - law_force(want, d)) > 1e-9 * max(1.0, abs(law_force(want, d)))
            ]
            check(off == [], f"the {name} law departs from the formula at {off[:3]}")
            at = dict(zip(ds, fs))
            # Continuous at zero: nothing at touching, and nothing either side of it in the limit.
            check(at[0.0] == 0, f"the {name} law is {at[0.0]} at touching, not zero")
            check(
                abs(at[1e-12]) < 1e-6 and abs(at[-1e-12]) < 1e-6,
                f"the {name} law is not continuous at zero: {at[-1e-12]} below, {at[1e-12]} above",
            )
            # Zero at and past the range — which for a law with no pull is everywhere past touching.
            reach = want["range"] if want["attraction"] > 0 else 0.0
            beyond = [
                (d, f) for d, f in zip(ds, fs) if d >= reach > 0 or (reach == 0 and d > 0)
            ]
            check(
                all(f == 0 for _, f in beyond),
                f"the {name} law pulls at or past its range: {[b for b in beyond if b[1]][:3]}",
            )
            check(
                len(beyond) >= 20,
                f"the {name} law's zero tail was sampled only {len(beyond)} times",
            )
            # The knee, and the two slopes either side of it, taken against the penetration the law
            # is written in: `repulsion` per unit of depth up to the knee, `repulsion * steep` past
            # it — which is flat wherever steep is zero, and that flat is the old law's cap.
            tol, rep = want["rigidity"], want["repulsion"]
            check(
                abs(at[-tol] - rep * tol) < 1e-9,
                f"the {name} law's knee is {at[-tol]}, not {rep * tol}",
            )
            inside = look("law/forces-at", gaps=[-tol * 0.75, -tol * 0.25])
            gentle = (inside[0] - inside[1]) / (tol * 0.5)
            check(
                abs(gentle - rep) < 1e-6 * rep,
                f"the {name} law's slope inside the knee is {gentle}, not {rep}",
            )
            past = look("law/forces-at", gaps=[-tol - 0.15, -tol - 0.05])
            steeper, sharp = rep * law_steep(want), (past[0] - past[1]) / 0.1
            check(
                abs(sharp - steeper) <= 1e-6 * max(steeper, rep),
                f"the {name} law's slope past the knee is {sharp}, not {steeper}",
            )
            # And the attraction hump, which peaks at half the range at exactly the attraction.
            if want["attraction"] > 0:
                deepest = min(fs)
                check(
                    at[want["range"] / 2] == -want["attraction"],
                    f"the {name} law's pull at half its range is {at[want['range'] / 2]}, not {-want['attraction']}",
                )
                check(
                    deepest == -want["attraction"] and deepest == at[want["range"] / 2],
                    f"the {name} law's deepest pull is {deepest}, not {-want['attraction']} at half the range",
                )

        # 10b. The attraction never overcomes the repulsion at contact. The two halves of the law do
        # not overlap by construction, so this holds whatever the four numbers are: over every preset
        # and a grid of 108 settings, the force at any penetration is a push and never a pull.
        grid = [
            {"rigidity": g, "repulsion": r, "attraction": a, "range": w}
            for g in (0.002, 0.05, 0.15, 0.4)
            for r in (200, 2500, 8000)
            for a in (0, 120, 400)
            for w in (0, 0.25, 0.5)
        ]
        grid += [LAW_DEFAULT] + [LAW_PRESETS[k] for k in ("rigid", "soft", "sticky")]
        pulls = look("law/never-pulls", laws=grid)
        check(pulls == [], f"the law pulls at a penetration under some setting: {pulls[:3]}")
        check(len(grid) == 112, f"the parameter grid is {len(grid)} settings")

        # 10c. The defaults reproduce today's behaviour to the bit: the old law was `contact *
        # min(p, contactCap)` with contact 2500 and cap 0.15, and steep is zero exactly there, so
        # every cached trajectory and every measurement of revisions 6 to 10 is unchanged.
        ask("setLawPreset", "default")
        check(ask("law")["steep"] == 0, "the shipped law's steep is not exactly zero")
        old_ps = [0.0, 1e-6, 0.001, 0.02, 0.075, 0.1499, 0.15, 0.1501, 0.2, 0.3, 0.42, 0.6]
        old = look("law/forces-at-penetration", penetrations=old_ps)
        drift = [
            (p, f, 2500 * min(p, 0.15)) for p, f in zip(old_ps, old) if f != 2500 * min(p, 0.15)
        ]
        check(
            drift == [],
            f"the shipped law is not the old hard-coded one to the bit: {drift[:3]}",
        )

        # 10d. Every parameter clamps to its bounds and round-trips, and a setter given nothing —
        # or something that is not a number — leaves the law alone rather than resetting it.
        moved = look(
            "law/clamps-and-round-trips",
            low={"rigidity": -9, "repulsion": -9, "attraction": -9, "range": -9},
            high={"rigidity": 99, "repulsion": 99999, "attraction": 9999, "range": 9},
            middle={"rigidity": 0.123, "repulsion": 3333, "attraction": 250, "range": 0.375},
        )
        check(
            moved["lo"] == {k: LAW_BOUNDS[k][0] for k in LAW_KEYS},
            f"the law does not clamp low: {moved['lo']}",
        )
        check(
            moved["hi"] == {k: LAW_BOUNDS[k][1] for k in LAW_KEYS},
            f"the law does not clamp high: {moved['hi']}",
        )
        check(
            moved["mid"]
            == {"rigidity": 0.123, "repulsion": 3333, "attraction": 250, "range": 0.375},
            f"a law inside the bounds is not taken as given: {moved['mid']}",
        )
        check(
            moved["back"] == moved["mid"], f"the law does not round-trip through law(): {moved}"
        )
        check(
            moved["junk"] == moved["mid"] and moved["none"] == moved["mid"],
            f"a setter given junk or nothing moved the law: {moved}",
        )
        # Revision 15: the cache key carries the walls' own law after a "|w", since a changed wall
        # law needs its run rebuilt too. The claim here is about the pair law, so it reads the
        # pair's segment rather than the whole key, which would fail on an unrelated change.
        pair_segment = next(s for s in moved["stray"].split("|") if s.startswith("pair:"))
        check(
            pair_segment == "pair:0.123:3333:250:0.375",
            f"an unknown preset is not a no-op: {moved['stray']}",
        )

        # 10e. The law is in the trajectory cache key. Two laws draw two trajectories, and the same
        # law set twice draws the same one byte for byte: the cache is keyed rather than cleared, so
        # coming back to a law already run is instant and gives what it gave before.
        keyed = look(
            "law/cache-key",
            n=17,
            presets={"a": "default", "b": "soft", "c": "default", "d": "rigid"},
        )
        check(
            keyed["a"] != keyed["b"] and keyed["b"] != keyed["d"] and keyed["a"] != keyed["d"],
            f"three laws drew the same free run: {keyed}",
        )
        check(
            keyed["a"] == keyed["c"],
            f"the same law drew two different runs: {keyed['a']} then {keyed['c']}",
        )

        # 10f. The plot. The curve is redrawn on every parameter, the two handles sit where the four
        # numbers put them, and the pull handle is not drawn when there is nothing to pull with.
        ask("setLawPreset", "default")

        def curve() -> str:
            return look("dom/attribute", id="lp-curve", name="d")

        curves = [curve()]
        for nudge in (
            {"rigidity": 0.2},
            {"repulsion": 3000},
            {"attraction": 200, "range": 0.3},
            {"range": 0.45},
        ):
            ask("setLaw", nudge)
            curves.append(curve())
        check(
            len(set(curves)) == len(curves),
            f"a parameter changed without redrawing the curve ({len(set(curves))} of {len(curves)} distinct)",
        )
        check(
            all(c.startswith("M") for c in curves),
            f"the curve is not a path: {curves[0][:40]!r}",
        )
        for name in ("default", "rigid", "soft", "sticky"):
            want = LAW_DEFAULT if name == "default" else LAW_PRESETS[name]
            ask("setLawPreset", name)
            handles = look("law/plot-handles")
            kx, ky = lp_knee(want)
            check(
                abs(handles["knee"][0] - kx) < 0.01 and abs(handles["knee"][1] - ky) < 0.01,
                f"the {name} law's knee is drawn at {handles['knee']}, not ({kx:.2f}, {ky:.2f})",
            )
            check(
                handles["top"] == lp_top(want),
                f"the {name} law's push axis tops out at {handles['top']}, not {lp_top(want)}",
            )
            check(
                abs(handles["cross"] - lp_x(0)) < 0.01,
                f"the plot's touching mark is at {handles['cross']}, not {lp_x(0):.2f}",
            )
            attracts = want["attraction"] > 0 and want["range"] > 0
            check(
                handles["shown"] == attracts,
                f"the {name} law's pull handle is {'drawn' if handles['shown'] else 'hidden'}",
            )
            if attracts:
                px, py = lp_pull(want)
                check(
                    abs(handles["pull"][0] - px) < 0.01 and abs(handles["pull"][1] - py) < 0.01,
                    f"the {name} law's pull handle is drawn at {handles['pull']}, not ({px:.2f}, {py:.2f})",
                )
        # Dragging a handle is the same setter the sliders write through, so neither can get ahead of
        # the other: the four numbers move and the four sliders follow.
        ask("setLawPreset", "default")
        dragged = look("law/drag-handle", handle="knee", d=-0.1, f=300)
        check(
            dragged["law"] == {"rigidity": 0.1, "repulsion": 3000, "attraction": 0, "range": 0},
            f"dragging the knee to a push of 300 at a tenth of a side gave {dragged['law']}",
        )
        check(
            dragged["sliders"] == ["0.1", "3000", "0", "0"],
            f"the sliders did not follow the knee: {dragged['sliders']}",
        )
        dragged = look("law/drag-handle", handle="pull", d=0.1, f=-200)
        check(
            dragged["law"]
            == {"rigidity": 0.1, "repulsion": 3000, "attraction": 200, "range": 0.2},
            f"dragging the pull to 200 at a fifth of a side gave {dragged['law']}",
        )
        check(
            dragged["sliders"] == ["0.1", "3000", "200", "0.2"],
            f"the sliders did not follow the pull: {dragged['sliders']}",
        )
        check(dragged["shown"], "the pull handle stayed hidden after a pull was dragged in")
        # `lawCurve` is the same law sampled, which is what the plot draws from.
        sampled = look("law/curve-samples", preset="sticky", samples=40)
        check(
            sampled["n"] == 41 and sampled["rising"],
            f"lawCurve(40) is not 41 rising samples: {sampled}",
        )
        check(
            sampled["off"] == 0,
            f"{sampled['off']} of lawCurve's samples are not what lawForce says",
        )
        check(
            abs(sampled["ends"][0] + 0.16) < 1e-12 and abs(sampled["ends"][1] - 0.25) < 1e-12,
            f"the sticky law's curve spans {sampled['ends']}, not twice its knee through its range",
        )

        # 10g. The three presets are reachable from the panel, and the pressed one is the one in use.
        for name in ("rigid", "soft", "sticky"):
            lit = look("law/press-preset", name=name)
            check(
                lit["law"] == LAW_PRESETS[name],
                f"the {name} button set {lit['law']}, not {LAW_PRESETS[name]}",
            )
            check(lit["on"] == [name], f"the {name} button did not light up alone: {lit['on']}")
        ask("setLawPreset", "default")
        check(
            look("dom/count", selector="#law-preset-seg button.on") == 0,
            "a preset is still lit with the shipped law in use",
        )

        # ---- step 11 (revision 11): the relationship graph. Orthogonal to the law: the law says
        # what the force is, the graph says between whom. Guarded like the steps above.
        if (
            not {
                "setRelationship",
                "relationship",
                "relationships",
                "setTargetGraph",
                "targetGraph",
                "contactGraph",
            }
            <= api
        ):
            browser.close()
            print("FAILED")
            for failure in dict.fromkeys(failures):
                print(" -", failure)
            print(
                " - the relationship graph was not driven: setRelationship is not on the API yet"
            )
            return 1
        drive(
            ("setMode", "pack"),
            ("setStyle", "tween"),
            ("setSnap", True),
            ("setLawPreset", "default"),
            ("setRelationship", "general"),
            ("setStepN", 17),
        )
        kinds = ["general", "groups", "contact"]
        check(ask("relationships") == kinds, f"the three graphs are {ask('relationships')}")
        check(ask("relationship")["kind"] == "general", "the default graph is not general")
        for kind in kinds:
            got = ask("setRelationship", kind)
            check(got["kind"] == kind, f"setRelationship({kind!r}) reported {got['kind']}")
            check(ask("relationship")["kind"] == kind, f"{kind} did not stick")
        check(
            ask("setRelationship", "nonesuch")["kind"] == "general",
            "an unknown graph does not fall back to general",
        )

        # 11a. Repulsion is never masked. Under every graph, with the sticky law's pull switched on,
        # an open-ended run from the grid start settles to the same shallow overlap: no relationship
        # lets two squares be pulled through each other, because the mask is never consulted on the
        # penetrating side of the law. Measured over 2,400 steps: at n = 17 the deepest overlap is
        # 0.0048 under general, 0.0052 under groups and 0.0056 under contact; at n = 29 it is 0.0048,
        # 0.0046 and 0.0054. All are thousandths of a side, and none runs away.
        overlaps: dict[tuple[int, str], float] = {}
        nears: dict[tuple[int, str], int] = {}
        for n in (17, 29):
            for kind in kinds:
                look("relationship/arm-run", n=n, kind=kind)
                ask("optimizeStep", 2400)
                st = ask("optimizeState")
                check(
                    st["steps"] == 2400 and st["n"] == n,
                    f"the n = {n} run under {kind} is {st['steps']} steps of {st['n']}",
                )
                overlaps[(n, kind)] = st["penetration"]
                nears[(n, kind)] = st["near"]
        for (n, kind), pen in overlaps.items():
            check(
                pen is not None and 0 < pen < 0.01,
                f"the deepest overlap at n = {n} under {kind} is {pen}, not a few thousandths of a side",
            )
            check(
                pen <= 2.5 * overlaps[(n, "general")],
                f"{kind} at n = {n} overlaps {pen}, against {overlaps[(n, 'general')]} under general",
            )

        # 11b. Attraction IS masked. The same runs, counted by how many pairs the pull was reaching
        # at the last step: at n = 17 that is 17 pairs under general against 0 under contact, and at
        # n = 29 it is 31 against 0. Groups falls in between (5 and 1), being a mask that still
        # relates whole blocks. The bands below are wide enough to survive a nudge to the physics
        # and narrow enough that a mask quietly doing nothing would show.
        for n, wide in ((17, 17), (29, 31)):
            general, contact = nears[(n, "general")], nears[(n, "contact")]
            check(
                general >= wide // 2,
                f"the pull reached only {general} pairs at n = {n} under general (measured {wide})",
            )
            check(
                contact <= 3,
                f"the pull reached {contact} pairs at n = {n} under contact, which is not a mask (measured 0)",
            )
            check(
                general >= 4 * max(contact, 1),
                f"n = {n}: {general} pairs under general against {contact} under contact",
            )
            check(
                nears[(n, "groups")] <= general,
                f"n = {n}: groups reached {nears[(n, 'groups')]} pairs, more than general's {general}",
            )
        # With no pull at all there is nothing to mask, whatever the graph says.
        drive(("setLawPreset", "default"), ("setRelationship", "general"))
        check(
            not ask("relationship")["attracting"],
            "the shipped law reports itself as attracting",
        )

        # 11c. The groups mask is exactly the blocks' own cliques. `blocks()` splits a block into
        # members and riders and the mask is built from `blockOf`, which carries both, so the count
        # is the sum of (members + riders) choose 2 — n = 17's blocks are 5, 4 + 1 and 3 + 3, which
        # is 10 + 10 + 15 = 35 pairs, not the 19 the member counts alone would give. The runs above
        # left the stage on an open-ended run from the grid; everything from here reads the timeline,
        # so the start goes back to the previous packing first.
        ask("setInitial", "previous")
        # The counts fell when the crossing repair landed, and they were meant to: a block that was
        # buying its coherence with two squares trading places across the packing is dissolved by
        # the repair, so there are fewer members to form cliques from -- and occasionally more, where
        # undoing one crossing lets a member join a block it was assigned away from. Measured before
        # and after: 11 was 4 and is 3, 17 was 35 and is 40, 26 was 59 and is 53, 29 was 46 and is
        # 42, 110 was 550 and is 365. What has not changed, and is the part that is a property rather
        # than a number, is the line below: the mask IS the blocks' cliques, counted either way round.
        for n, want_edges in ((11, 3), (17, 40), (26, 53), (29, 42), (110, 365)):
            if ask("setStepN", n) != n:
                continue
            ask("setRelationship", "groups")
            counted = look("relationship/groups-mask-cliques")
            check(
                counted["maskEdges"] == want_edges,
                f"the groups mask at n = {n} is {counted['maskEdges']} pairs, not the measured {want_edges}",
            )
            check(
                counted["maskEdges"] == counted["byOf"] == counted["byBlocks"],
                f"the groups mask at n = {n} is not the blocks' cliques: {counted}",
            )
            check(
                counted["maskEdges"] < 60000,
                f"the groups mask at n = {n} reaches the 60,000-pair cap",
            )
        # 11d. **What a trajectory costs to build.** Every physical style runs a simulation of
        # `bodies` squares over `steps` sub-steps, and the page builds one per pair on demand while
        # a viewer waits. None of the algorithms here is worse than linear in the body count today,
        # and this is what says so tomorrow: a change that made the broad phase quadratic, or that
        # dropped the grid, would still produce the right picture and take ten times as long. The
        # ceiling is loose on purpose -- thirteen times the measurement -- because this is wall
        # clock on whatever machine is running it, and a flaky performance gate is worse than none.
        # It is the shape of a regression this catches, not a tenth of a millisecond.
        costs = []
        for n in (11, 100, 324):
            if ask("setStepN", n) != n:
                continue
            index = look("pairs/index-of-n", n=n)
            if index < 0:
                continue
            for style in ("physics", "bodies"):
                built = look("physics/build", index=index, style=style)
                costs.append((n, style, built["bodies"], built["ms"], built["bytes"]))
                check(
                    built["ms"] < TRAJECTORY_MS_CEILING,
                    f"a {style} trajectory at n = {n} took {built['ms']:.0f} ms, "
                    f"over the {TRAJECTORY_MS_CEILING} ms ceiling",
                )
                check(
                    built["bytes"] < TRAJECTORY_BYTE_CEILING,
                    f"a {style} trajectory at n = {n} holds {built['bytes']} bytes, "
                    f"over the {TRAJECTORY_BYTE_CEILING} ceiling",
                )
        print(
            "trajectory build cost: "
            + "; ".join(
                f"n={n} {style} {bodies} bodies {ms:.0f} ms {bytes_ / 1e6:.1f} MB"
                for n, style, bodies, ms, bytes_ in costs
            )
        )

        # A general relationship has no mask to report, and the arriving square is in no block, so a
        # size whose blocks the record does not carry attracts nobody under groups.
        drive(("setStepN", 17), ("setRelationship", "general"))
        check(ask("relationship")["maskEdges"] is None, "a general relationship reports a mask")
        if ask("setStepN", 100) == 100:
            ask("setRelationship", "groups")
            check(
                ask("relationship")["maskEdges"] == 0 and len(ask("blocks")) == 0,
                "n = 100 carries no blocks, so its groups mask should be empty",
            )

        # 11d. The contact target is the retained packing's own contact graph, relabelled into the
        # run's square order. The counts are read off the record and pinned here.
        ask("setRelationship", "contact")
        for n, want_edges in (
            (17, 4),
            (29, 17),
            (100, 180),
            (110, 111),
            (272, 322),
            (324, 612),
        ):
            if ask("setStepN", n) != n:
                continue
            got = len(ask("targetGraph")) // 2
            check(
                got == want_edges,
                f"the target graph at n = {n} has {got} edges, not the record's {want_edges}",
            )
            check(
                ask("relationship")["edges"] == want_edges,
                f"the relationship at n = {n} does not report the target's {want_edges} edges",
            )
        # And settling on the retained frame realises that graph, by definition — bar one pair. The
        # full-side test builds its axes from the lower-indexed square of the pair, so a contact
        # right on the hundredth-of-a-side tolerance can read differently once the frame's order is
        # relabelled into the run's. Measured over eleven retained frames that happens exactly once:
        # n = 110's run-order pair 46-54 (the frame's squares 17 and 7, whose centres are 1.00415
        # apart at 63.93 and 64.22 degrees) is a contact in the frame's order and not in the run's.
        short = []
        ask("setMode", "animate")
        for n in (5, 10, 11, 17, 26, 29, 100, 110, 172, 272, 324):
            if ask("setStepN", n) != n:
                continue
            # Revision 14: the retained frame is what a step comes to rest on, so it is Animate's
            # settled stage that is read here. Pack's own stage is a starting arrangement.
            seek_to_end()
            rel = ask("relationship")
            check(
                abs(rel["side"] - rel["record"]) < 1e-9,
                f"the settled frame at n = {n} is a box of {rel['side']}, not the record's {rel['record']}",
            )
            if rel["met"] == rel["edges"]:
                check(
                    rel["edges"] == 0 or abs(rel["fraction"] - 1.0) < 1e-12,
                    f"n = {n} met every target contact but reports fraction {rel['fraction']}",
                )
            else:
                short.append((n, rel["edges"], rel["met"]))
        check(
            short == [(110, 111, 110)],
            f"the retained frames that do not realise their own contact graph are {short}, not the one measured",
        )

        # 11e. A graph from anywhere, and back to the record's.
        ask("setStepN", 17)
        swapped = look("relationship/target-swap", graph=[[0, 1], [1, 2]])
        check(
            swapped["from"] == "record" and swapped["target"] == "record",
            f"the target does not name where it came from: {swapped['from']} then {swapped['target']}",
        )
        check(
            swapped["given"]["graph"] == [0, 1, 1, 2]
            and swapped["given"]["target"] == "given"
            and swapped["given"]["edges"] == 2,
            f"setTargetGraph did not replace the target: {swapped['given']}",
        )
        check(
            swapped["after"] == swapped["before"],
            f"setTargetGraph(null) did not go back to the record's: {swapped['after']} against {swapped['before']}",
        )

        # 11f. What the graph looks like on the stage. Revision 12 splits it in two, and the split
        # is the point: a **contact** target is drawn whenever it is in force, overlay or no
        # overlay, because it is what the run is being asked to realise; the **groups** cliques
        # still ride the correspondence overlay and are still drawn only where the pull reaches,
        # a completely connected block being thousands of pairs that are not doing anything.
        seek_to_end(
            ("setMode", "animate"),
            ("setLawPreset", "sticky"),
            ("setStepN", 29),
            ("setOverlay", False),
            ("setTargetSource", "record"),
        )
        no_overlay = {}
        for kind in kinds:
            ask("setRelationship", kind)
            no_overlay[kind] = look("mask/links")
        check(
            no_overlay["general"]["drawn"] == 0,
            f"a general relationship draws a mask: {no_overlay['general']}",
        )
        check(
            no_overlay["groups"]["drawn"] == 0,
            f"the groups mask is drawn with the overlay off: {no_overlay['groups']}",
        )
        check(
            no_overlay["contact"]["shown"] and no_overlay["contact"]["drawn"] > 0,
            f"the contact graph is not drawn without the overlay: {no_overlay['contact']}",
        )
        # Every target edge is drawn, in one of two classes, and on the record's own settled frame
        # they are all met: n = 29's seventeen target contacts are seventeen solid lines.
        targeted = ask("relationship")["edges"]
        rel = ask("relationship")
        check(
            no_overlay["contact"]["drawn"] == targeted,
            f"the contact graph draws {no_overlay['contact']['drawn']} of its {targeted} edges",
        )
        check(
            no_overlay["contact"]["met"] == rel["met"]
            and no_overlay["contact"]["unmet"] == targeted - rel["met"],
            f"the two classes do not split the graph the way the count does: {no_overlay['contact']} against {rel}",
        )
        check(
            no_overlay["contact"]["met"] > 0 and no_overlay["contact"]["unmet"] == 0,
            f"the retained frame's own contact graph is not drawn as met: {no_overlay['contact']}",
        )
        # The two classes are drawn differently, which is what makes the difference readable.
        styles = look("mask/link-styles")
        drive(("setInitial", "grid"), ("optimizeStep", 300))
        mixed = look("mask/links")
        check(
            mixed["met"] + mixed["unmet"] == mixed["drawn"] and mixed["unmet"] > 0,
            f"an arrangement that does not realise the graph draws no unmet edges: {mixed}",
        )
        pair_styles = look("mask/link-styles")
        check(
            pair_styles["met"] is not None and pair_styles["unmet"] is not None,
            f"one of the two classes is not on the stage to compare: {pair_styles} (settled: {styles})",
        )
        check(
            pair_styles["met"] != pair_styles["unmet"],
            f"a met edge and an unmet one are drawn the same: {pair_styles}",
        )
        seek_to_end(("setInitial", "previous"), ("setStepN", 29))
        # The groups cliques, which still ride the overlay and are still reach-limited.
        drive(("setRelationship", "groups"), ("setOverlay", True))
        grouped = look("mask/links")
        related = ask("relationship")["maskEdges"]
        check(
            grouped["shown"] and 0 < grouped["drawn"] < related,
            f"the groups mask draws {grouped['drawn']} of {related} related pairs",
        )
        ask("setOverlay", False)
        check(
            look("mask/links")["drawn"] == 0, "the groups mask survives the overlay going off"
        )
        # And the correspondence overlay is still one control: the graph added no second checkbox
        # for itself, the drawing mode's toggle being a mode and not an overlay.
        controls = look("controls/checkbox-ids")
        check(
            [c for c in controls if "mask" in c or "overlay" in c] == [],
            f"the mask added an overlay control of its own: {controls}",
        )
        rode = look("mask/rides-overlay")
        check(
            rode["on"] and rode["off"] and rode["links"] is False,
            f"the groups mask does not ride the correspondence overlay's own control: {rode}",
        )

        # 11g. The two chart options. They are two claims, not one setting: the snap ends on the
        # record by construction, the bias only says which pairs should touch.
        drive(("setStepN", 17), ("setRelationship", "general"))
        snapped = look("controls/snap-toggle")
        check(
            snapped["flipped"] is not snapped["was"] and snapped["back"] is snapped["was"],
            f"the snap option does not drive state().snap: {snapped}",
        )
        check(
            snapped["shown"] is snapped["was"],
            f"the snap box does not read back the state it drives: {snapped}",
        )
        # The bias sets the graph, and brings a pull with it when the law has none — there being no
        # point masking a force that is not there. The two are one gesture, and the order they are
        # done in matters: `setLaw` runs `updateSegments`, which writes `bias-toggle.checked` back
        # from the relationship, so a handler that reads `ev.target.checked` again *after* calling
        # `setLaw` reads the value it has just been reset to. The two checks below are exactly that
        # reading, and they are the ones to look at first if this step goes red.
        drive(("setLawPreset", "default"), ("setRelationship", "general"))
        biased = look("controls/bias-toggle")
        check(
            biased["before"] == 0,
            f"the law already pulled before the bias was turned on: {biased['before']}",
        )
        check(
            biased["on"]["attraction"] > 0 and biased["on"]["range"] > 0,
            f"the bias masked a force that is not there: {biased['on']}",
        )
        check(
            biased["on"]["kind"] == "contact",
            "the bias did not set the contact graph from a law with no pull "
            f"(the pull arrived but the graph did not): {biased['on']}",
        )
        check(
            biased["on"]["checked"],
            f"the bias box unticked itself while turning the bias on: {biased['on']}",
        )
        check(
            biased["off"]["kind"] == "general" and not biased["off"]["checked"],
            f"turning the bias off did not go back to general: {biased['off']}",
        )
        # From a law that already pulls, the graph is all the bias touches.
        drive(("setLawPreset", "sticky"), ("setRelationship", "general"))
        again = look("controls/bias-toggle-with-pull")
        check(
            again["on"] == {"kind": "contact", "attraction": 120}
            and again["kind"] == "general",
            f"the bias does not toggle the graph from a law that already pulls: {again}",
        )
        # `setRelationship` on the API changes the graph and nothing else, which is what makes the
        # convenience above a property of the control rather than of the physics.
        drive(("setLawPreset", "default"), ("setRelationship", "general"))
        alone = look("relationship/set-touches-law", kind="contact")
        check(
            alone["before"] == alone["after"] and alone["kind"] == "contact",
            f"setRelationship touched the law: {alone}",
        )
        # The graph is in the trajectory cache key as well: three graphs, three free runs.
        ask("setLawPreset", "sticky")
        graphed = look(
            "relationship/cache-key", n=17, kinds=["general", "contact", "groups", "general"]
        )
        check(
            len({v[0] for v in graphed.values()}) == 3,
            f"three graphs drew fewer than three free runs: {graphed}",
        )
        check(
            graphed["general"][0] == graphed["general"][1],
            f"the same graph drew two different free runs: {graphed['general']}",
        )
        drive(
            ("setLawPreset", "default"),
            ("setRelationship", "general"),
            ("setOverlay", False),
            ("setInitial", "previous"),
            ("setSnap", True),
            ("setStepN", 17),
        )

        # ---- step 12 (revision 12): nothing the owner clicks moves while a run plays. The defect
        # this closes is a real one and it will come back: the live readouts sat inline with the
        # buttons, so a figure gaining a digit slid every control after it sideways under the
        # cursor. Every button's bounding box is captured at two instants of a run and compared,
        # for both of the page's playbacks — Pack's open-ended optimisation, whose clock, step
        # count, overlap and target fraction all move, and a Animate, which additionally crosses a
        # pair boundary and so redraws every readout in the panel rather than only the live ones.
        drive(
            ("setMode", "pack"),
            ("setStepN", 17),
            ("setInitial", "grid"),
            ("setLawPreset", "sticky"),
            ("setRelationship", "contact"),
            ("optimizeStep", 5),
        )
        early = look("controls/button-boxes")
        check(len(early) >= 20, f"only {len(early)} buttons found in the controls")
        ask("optimizeStep", 2400)
        late = look("controls/button-boxes")
        moved = [(a, b) for a, b in zip(early, late) if a != b]
        check(moved == [], f"a control moved while a Pack run played: {moved[:3]}")
        # And the two readouts that drive it really did change, so the comparison has teeth.
        drive(("setStepN", 17), ("setInitial", "grid"), ("optimizeStep", 5))
        first_clock = text_of("clock")
        ask("optimizeStep", 2400)
        check(
            first_clock != text_of("clock"),
            "the clock did not change over the run, so the no-reflow check proves nothing",
        )
        # The Animate half: a range played across a pair boundary, where the whole panel is rewritten.
        drive(
            ("setInitial", "previous"),
            ("setLawPreset", "default"),
            ("setRelationship", "general"),
            ("setMode", "animate"),
            ("setRange", 16, 30),
            ("playRange",),
            ("pause",),
            ("seek", 0.4),
        )
        early = look("controls/button-boxes")
        drive(("goTo", 28), ("seek", 1.9))
        late = look("controls/button-boxes")
        moved = [(a, b) for a, b in zip(early, late) if a != b]
        check(moved == [], f"a control moved while a Animate run played: {moved[:3]}")
        # And the same for the settings a press changes: switching the style, the size, the law
        # preset, the graph or growth rewrites the whole panel, and none of it may move a control.
        # (Pack and Animate are exempt: they deliberately show different controls.)
        drive(
            ("setMode", "pack"),
            ("setStepN", 17),
            ("setStyle", "tween"),
            ("setAnneal", 3),
            ("setLawPreset", "default"),
            ("setRelationship", "general"),
            ("setGrowth", {"on": False}),
        )
        base = look("controls/button-boxes")
        for label, call in (
            ("the style", ("setStyle", "bodies")),
            ("the annealing dial", ("setAnneal", 10)),
            ("the law preset", ("setLawPreset", "sticky")),
            ("the graph", ("setRelationship", "contact")),
            ("growth", ("setGrowth", {"on": True, "size": 0.3})),
            ("the size", ("setStepN", 324)),
            ("the size again", ("setStepN", 5)),
        ):
            drive(call)
            moved = [(a, b) for a, b in zip(base, look("controls/button-boxes")) if a != b]
            check(moved == [], f"changing {label} moved a control: {moved[:3]}")
        drive(
            ("setStyle", "tween"),
            ("setAnneal", 3),
            ("setLawPreset", "default"),
            ("setRelationship", "general"),
            ("setGrowth", {"on": False, "size": 1}),
            ("setStepN", 17),
        )
        # Every readout that changes at runtime is in a slot of its own: fixed width, or a full
        # line below the control it belongs to. This is the property, stated where it can be read.
        slots = look(
            "controls/readout-slots",
            ids=[
                "clock",
                "speed-info",
                "range-duration",
                "range-position",
                "step-label",
                "step-note",
                "law-info",
                "rel-info",
                "grow-info",
                "anneal-info",
                "continuous-info",
            ],
        )
        for ident, is_readout, width, overflow, _full_line in slots:
            check(is_readout, f"#{ident} changes at runtime and is not in a fixed slot")
            check(overflow == "hidden", f"#{ident} can overrun its slot (overflow: {overflow})")
            check(
                width.endswith("px") and float(width[:-2]) > 0,
                f"#{ident} has no width of its own: {width}",
            )
        check(
            sum(1 for *_, full_line in slots if full_line) >= 4,
            "no readout takes the owner's suggested form, a line of its own below the control",
        )
        drive(("stopAll",), ("setMode", "pack"), ("setStepN", 17), ("seek", 0))

        # ---- step 13 (revision 12): no position bar in Pack. Pack is one fixed n, so the bar that
        # carries the corpus's scale has nothing to say about it. Animate keeps it. The property that
        # matters alongside is that hiding it moves nothing else: the bar is absolutely positioned
        # inside the stage, so the stage, the panel and the controls are the same box either way.
        # Revision 16: the position bar and its scale along the bottom of the stage are gone --
        # the owner found them distracting, and the stage carries facts about the packing rather
        # than apparatus about the playback. What was checked here was that hiding the bar in Pack
        # moved nothing else; with no bar there is nothing to hide, and what remains worth holding
        # is the other half of that property: the two modes lay the stage out identically, so a
        # switch between them does not move the picture.
        drive(("setMode", "pack"), ("setStepN", 17))
        packed = look("layout/stage-boxes")
        check(packed["progress"], "the position bar is still in the page")
        drive(("setMode", "animate"), ("setRange", 2, 100))
        swept = look("layout/stage-boxes")
        for key in ("stage", "facts", "svg"):
            check(
                packed[key] == swept[key],
                f"the mode moved the {key}: {packed[key]} against {swept[key]}",
            )
        # The step header still goes with the mode: it describes a step, and Pack has none.
        drive(("setMode", "pack"), ("setStepN", 17))
        check(look("dom/hidden", id="kind-tag"), "Pack still draws the step header")
        drive(("setMode", "animate"), ("setInitial", "previous"), ("setStepN", 17), ("seek", 0))

        # ---- step 14 (revision 12): a contact graph drawn by hand. The owner: "it would be nice
        # if you can click and drag a link between any two boxes to add to their contact graph."
        # The property that matters is not the gesture but where the edges *go*: they are the same
        # object the record-derived graph is, they reach the mask by the same path, and nothing in
        # the physics is told which of the two it is looking at.
        if not {"edges", "setEdges", "clearEdges", "setDrawing", "linkStart", "linkEnd"} <= api:
            browser.close()
            print("FAILED")
            for failure in dict.fromkeys(failures):
                print(" -", failure)
            print(
                " - the drawn graph was not driven: setEdges / linkStart are not on the API yet"
            )
            return 1
        seek_to_end(
            ("setMode", "pack"),
            ("setStyle", "tween"),
            ("setStepN", 11),
            ("setSnap", True),
            ("setDrawing", False),
            ("clearEdges",),
            ("setTargetSource", "record"),
        )
        # What the record's own graph is at this n, read off the page before anything is drawn, so
        # the check that the target goes back to it compares against the record and not a constant.
        ask("setRelationship", "contact")
        record_edges = ask("relationship")["edges"]
        check(
            record_edges > 0,
            f"n = 11 carries no record contact graph to go back to ({record_edges})",
        )
        ask("setRelationship", "general")
        check(
            ask("targetSources") == ["record", "drawn"],
            f"the two target sources are {ask('targetSources')}",
        )
        check(
            ask("targetSource") == "record", "the target does not start on the record's graph"
        )
        check(ask("edges") == [], "the drawn graph does not start empty")

        # 14a. The gesture, driven as a real pointer press, drag and release on the stage. World
        # coordinates go through the same matrix the page's own handler uses, so this is the
        # gesture and not a call dressed up as one.
        def screen_of(index: int) -> tuple[float, float]:
            return tuple(look("stage/screen-of", index=index))

        ask("setDrawing", True)
        check(ask("drawing") is True, "the drawing mode did not come on")
        check(
            ask("targetSource") == "drawn",
            "turning drawing on did not point the target at the drawn graph",
        )
        ax, ay = screen_of(0)
        bx, by = screen_of(3)
        page.mouse.move(ax, ay)
        page.mouse.down()
        page.mouse.move((ax + bx) / 2, (ay + by) / 2, steps=4)
        pending = look("draw/pending-edge")
        check(pending["shown"], "the pending edge is not drawn while the gesture is being made")
        check(
            pending["x1"] != pending["x2"],
            f"the pending edge does not follow the cursor: {pending}",
        )
        page.mouse.move(bx, by, steps=4)
        page.mouse.up()
        check(
            ask("edges") == [[0, 3]],
            f"a drag between two squares did not add the edge: {ask('edges')}",
        )
        check(
            look("dom/display", id="draw-line") == "none",
            "the pending edge is still drawn after the release",
        )
        # The same gesture again takes it away.
        page.mouse.move(bx, by)
        page.mouse.down()
        page.mouse.move(ax, ay, steps=4)
        page.mouse.up()
        check(
            ask("edges") == [], f"the same drag again did not remove the edge: {ask('edges')}"
        )
        # A release on empty paper is not an edge, and neither is a square joined to itself.
        page.mouse.move(ax, ay)
        page.mouse.down()
        page.mouse.move(4, 4, steps=3)
        page.mouse.up()
        check(ask("edges") == [], "a release off the packing made an edge out of nothing")
        check(look("draw/self-link", index=2) is False, "a square can be joined to itself")
        ask("linkCancel")

        # 14b. The square drag still works, and the two gestures are kept apart by the toggle
        # alone: with drawing on nothing is ever picked up, with it off nothing is ever drawn.
        ask("setDrawing", True)
        page.mouse.move(ax, ay)
        page.mouse.down()
        page.mouse.move(ax + 40, ay + 40, steps=3)
        drawing_held = ask("hand")["held"]
        page.mouse.up()
        check(drawing_held < 0, f"a press picked square {drawing_held} up while drawing was on")
        drive(("setDrawing", False), ("clearEdges",))
        page.mouse.move(ax, ay)
        page.mouse.down()
        page.mouse.move(ax + 40, ay + 40, steps=3)
        dragged = ask("hand")["held"]
        page.mouse.up()
        check(dragged == 0, f"the square drag stopped working: the hand holds {dragged}")
        check(ask("edges") == [], "a square drag drew an edge with the drawing mode off")
        check(
            ask("hand")["edited"] is True,
            "the drag did not mark the run hand-edited, so it did not happen",
        )

        # 14c. The drawn graph is the same object the record's is. It reaches the mask by the one
        # path, it is what the readout counts, and it is held per n because an index is a different
        # square at a different n.
        seek_to_end(
            ("setInitial", "previous"),
            ("setStepN", 11),
            ("setStyle", "tween"),
            ("setSnap", True),
        )
        ask("setEdges", [[0, 1], [1, 2], [2, 3], [0, 3], [4, 5]])
        check(
            ask("edges") == [[0, 1], [1, 2], [2, 3], [0, 3], [4, 5]],
            f"setEdges did not take the graph: {ask('edges')}",
        )
        check(
            ask("targetSource") == "drawn",
            "setEdges did not point the target at the drawn graph",
        )
        ask("setRelationship", "contact")
        rel = ask("relationship")
        check(
            rel["edges"] == 5 and rel["drawn"] == 5 and rel["target"] == "drawn",
            f"the relationship does not read the drawn graph: {rel}",
        )
        check(
            ask("targetGraph") == [0, 1, 1, 2, 2, 3, 0, 3, 4, 5],
            f"the target graph is not the drawn one: {ask('targetGraph')}",
        )
        # The mask the physics consults is the drawn graph's own edge count.
        check(
            rel["maskEdges"] == 5, f"the mask is {rel['maskEdges']} pairs, not the drawn five"
        )
        # Duplicates, self-loops, reversed pairs and out-of-range indices are all folded away.
        ask("setEdges", [[1, 0], [0, 1], [2, 2], [3, 900], [-1, 4], [5, 4]])
        check(ask("edges") == [[0, 1], [4, 5]], f"the graph is not normalised: {ask('edges')}")
        # Per n: a graph drawn at 11 is not a graph at 5, and going back finds it again.
        ask("setStepN", 5)
        check(
            ask("edges") == [],
            f"the graph drawn at n = 11 followed the page to n = 5: {ask('edges')}",
        )
        ask("setEdges", [[0, 2]])
        ask("setStepN", 11)
        check(
            ask("edges") == [[0, 1], [4, 5]],
            f"the graph drawn at n = 11 was lost: {ask('edges')}",
        )
        # And back to the record's, which is still there and still the record's.
        ask("setTargetSource", "record")
        recorded = ask("relationship")
        check(
            recorded["target"] == "record"
            and recorded["edges"] == record_edges
            and recorded["drawn"] == 2,
            f"the record's graph is not what the target goes back to (its {record_edges} edges): {recorded}",
        )
        check(ask("clearEdges") == [], "clearEdges left something behind")
        drive(("setStepN", 5), ("clearEdges",), ("setStepN", 11))

        # 14d. A drawn graph drives a run. The trajectory cache is keyed by it, so two graphs draw
        # two runs and the same graph twice draws the same one; and the physics never learns which
        # source it came from, so a drawn copy of the record's graph drives the record's run.
        drive(
            ("setLawPreset", "sticky"),
            ("setStepN", 17),
            ("setRelationship", "contact"),
            ("setTargetSource", "record"),
        )
        recorded_graph = ask("targetGraph")
        keyed = look(
            "draw/graph-cache-key",
            walk=[
                ["record", None],
                ["two", [[0, 1], [2, 3]]],
                ["three", [[0, 1], [2, 3], [4, 5]]],
                ["twoAgain", [[0, 1], [2, 3]]],
                ["recordAgain", None],
            ],
        )
        # The key is what the trajectory cache is keyed by, so this is the property directly: three
        # graphs are three keys, and one graph reached twice is one key both times. The *outcome*
        # is the weaker test — two masks the pull never reaches can settle to the same arrangement,
        # which is revision 11's own measured finding about the contact bias — so the run is only
        # asserted to be stable, never to differ.
        check(
            len({keyed[k]["key"] for k in ("record", "two", "three")}) == 3,
            f"three graphs share a cache key: {[keyed[k]['key'] for k in ('record', 'two', 'three')]}",
        )
        check(
            keyed["two"]["key"] == keyed["twoAgain"]["key"],
            f"the same drawn graph keys two runs: {keyed['two']['key']} against {keyed['twoAgain']['key']}",
        )
        check(
            keyed["two"]["miss"] == keyed["twoAgain"]["miss"],
            f"the same drawn graph drew two different runs: {keyed['two']} against {keyed['twoAgain']}",
        )
        check(
            keyed["record"] == keyed["recordAgain"],
            f"going back to the record's graph did not go back to its run: {keyed['record']} against {keyed['recordAgain']}",
        )
        # The record's own graph, drawn by hand, is the record's own run: the physics is told
        # nothing about where the edges came from.
        same = look("draw/record-graph-by-hand", graph=recorded_graph)
        check(
            same["fromRecord"] == same["fromHand"],
            f"the record's graph drawn by hand drives a different run: {same}",
        )

        # 14e. The readout says how much of the target is realised, out of how much, and the side
        # the arrangement is in — and it says it whether or not anything is simulating, because it
        # is a measurement of the picture rather than of a run.
        seek_to_end(
            ("setStepN", 11),
            ("clearEdges",),
            ("setStyle", "tween"),
            ("setSnap", True),
            ("setInitial", "previous"),
            ("setRelationship", "contact"),
            ("setTargetSource", "record"),
        )
        # The row that carried this under the stage is gone with the rest of the readout, so what is
        # checked is the measurement itself: how much of the target graph is realised, out of how
        # much, and the side the arrangement is in. It is a measurement of the picture rather than of
        # a run, which is why it holds with nothing simulating.
        state_rel = ask("relationship")
        check(
            state_rel["edges"] > 0 and 0 <= state_rel["met"] <= state_rel["edges"],
            f"the contact target reports no fraction: {state_rel}",
        )
        check(state_rel["side"] > 0, f"the relationship readout carries no side: {state_rel}")
        drive(
            ("setRelationship", "general"),
            ("setTargetSource", "record"),
            ("setLawPreset", "default"),
            ("setDrawing", False),
            ("setStepN", 17),
            ("seek", 0),
        )

        # ---- step 15 (revision 13): the starting size redraws the arrangement. The owner: "when we
        # change size in Pack mode it should change the size of the boxes in the initial arrangement
        # right?" It did not. `setGrowth({size: 0.5})` stored the value and `growth().size` read it
        # back, but every drawn square stayed at full width until a run was started — because the
        # previous-packing start, which is the default, has no arrangement of its own on the stage,
        # only the step animation, and the size was written into a run that did not exist.
        #
        # The property, stated as geometry rather than as a transform string: **the drawn width of
        # the squares is proportional to the size setting**, at once, in Pack, under every one of the
        # three starts, with growth off as well as on, and with no run started. Reading the rendered
        # box rather than the `scale()` in the transform is deliberate — it is the picture the owner
        # is looking at, and it catches a scale that is written but not applied.
        def widths() -> list[float]:
            return look("stage/square-widths")

        def staged() -> dict:
            """The whole drawn frame: every square's transform, and the container it sits in."""
            return look("stage/frame")

        drive(
            ("stopAll",),
            ("setMode", "pack"),
            ("setStepN", 17),
            ("setStyle", "tween"),
            ("setGrowth", {"on": False, "size": 1}),
        )
        for start in ("previous", "random", "grid"):
            for grow_on in (False, True):
                drive(("setInitial", start), ("setGrowth", {"on": grow_on, "size": 1}))
                # Half size, then a third of it again, both from a stage that has not been run: the
                # ratio of the drawn widths must be the ratio of the sizes, square for square.
                ask("setGrowth", {"size": 0.9})
                check(
                    (ask("optimizeState")["steps"] or 0) == 0,
                    f"the {start} stage had already stepped, so the size check proves nothing",
                )
                big = widths()
                ask("setGrowth", {"size": 0.45})
                small = widths()
                where = f"{start} start, grow {'on' if grow_on else 'off'}"
                check(
                    len(big) == len(small) and len(big) > 1,
                    f"{where}: the stage drew {len(big)} squares then {len(small)}",
                )
                check(all(w > 0 for w in big), f"{where}: a square drew at no width at all")
                worst = max(
                    (abs(s / b - 0.5) for b, s in zip(big, small) if b > 0), default=1.0
                )
                check(
                    worst < 2e-3,
                    f"{where}: halving the size did not halve the drawn width "
                    f"(worst ratio error {worst:.4f}; {big[:2]} against {small[:2]})",
                )
                # And it is the setting that did it, not a run: nothing was played.
                check(not ask("state")["playing"], f"{where}: the size change started a run")
        # A size below one is not a picture of nothing: it is the frame a run started at that instant
        # would begin from, container and all. That is what makes the small squares mean something,
        # and it is checked against a real run rather than asserted.
        drive(("setInitial", "previous"), ("setGrowth", {"on": True, "size": 0.4}))
        paused = staged()
        drive(("optimize", True), ("pause",))
        started = staged()
        check(
            paused == started,
            f"the staged arrangement is not the frame a run starts from: {paused} against {started}",
        )
        check(
            float(started["box"]) > 1,
            f"the run starts in no container at all: {started['box']}",
        )
        # The container is the run's own starting box and the size does not move it: while the
        # squares are growing the walls hold (measured in revision 11 — the `clean` rule deadlocked
        # at 0.76 when they did not), so a reduced size is small squares in a full-size frame.
        boxes = {}
        for size in (0.3, 0.6, 0.9):
            drive(("setInitial", "previous"), ("setGrowth", {"size": size}))
            boxes[size] = staged()["box"]
        check(
            len(set(boxes.values())) == 1,
            f"the starting container moved with the size, which no growth run does: {boxes}",
        )
        # Revision 14 drops the condition revision 13 put on that staging: Pack shows its n squares
        # from the first frame at every size, so a full size leaves the arrangement on the stage
        # rather than uncovering the timeline underneath it. Leaving Pack is what gives the timeline
        # back, and that is the reversibility that matters.
        ask("setGrowth", {"size": 1})
        check(
            ask("optimizeState")["on"] is True,
            "a full starting size unstaged Pack, which no longer shows all n squares",
        )
        ask("setMode", "animate")
        check(
            ask("optimizeState")["on"] is False,
            "leaving Pack did not give the step animation back",
        )
        drive(("setMode", "pack"), ("setStepN", 17))
        check(
            ask("optimizeState")["on"] is True,
            "entering Pack did not stage the arrangement again",
        )
        # The three starting-arrangement buttons have the same duty and are checked the same way:
        # each takes effect on the drawing at once, with nothing played.
        drive(("setGrowth", {"on": False, "size": 1}), ("setStepN", 17), ("seek", 0))
        drawn = {}
        for start in ("previous", "random", "grid", "previous"):
            ask("setInitial", start)
            check(not ask("state")["playing"], f"choosing the {start} start started a run")
            drawn.setdefault(start, []).append(staged())
        check(
            len({tuple(v[0]["squares"]) for v in drawn.values()}) == 3,
            "two of the three starting arrangements draw the same picture, so a button did nothing",
        )
        check(
            drawn["previous"][0] == drawn["previous"][1],
            "going back to the previous-packing start did not go back to its arrangement",
        )
        drive(
            ("setInitial", "previous"),
            ("setGrowth", {"on": False, "size": 1}),
            ("setStepN", 17),
            ("seek", 0),
        )

        # ---- step 16 (revision 14): in Pack, n squares are on the stage from the first frame. The
        # owner: "if 17 is set below in pack mode why does the diagram show 16 to begin with". They
        # did: the pool held seventeen and sixteen were drawn, because Pack opened on the timeline,
        # which stages the seventeenth square's *arrival* — a transition model in a mode that has no
        # transitions. The property is counted rather than argued: what is drawn, at rest and after a
        # restart, under every start.
        drive(
            ("stopAll",),
            ("setMode", "pack"),
            ("setGrowth", {"on": False, "size": 1}),
            ("setStyle", "bodies"),
        )
        starts = ask("initials")
        counted = {}
        for n in (5, 11, 17, 29, 100):
            if ask("setStepN", n) != n:
                continue
            for kind in starts:
                ask("setInitial", kind)
                at_rest = look("stage/visible-count")
                check(
                    at_rest == n,
                    f"Pack at n = {n} from the {kind} start draws {at_rest} squares, not {n}",
                )
                if "restart" in api:
                    ask("restart")
                    after = look("stage/visible-count")
                    check(
                        after == n,
                        f"Pack at n = {n} from the {kind} start draws {after} squares after a restart, not {n}",
                    )
                    check(
                        not ask("state")["playing"],
                        f"a restart from a paused stage at n = {n} started the clock",
                    )
                counted[(n, kind)] = at_rest
        check(len(counted) >= 12, f"only {len(counted)} start-and-size pairs were counted")
        # And the step header goes with the step: `16 -> 17 · matched · max move …` describes a
        # transition, and Pack makes none. Animate keeps it, and hiding it moves nothing, the tag
        # being absolutely positioned on the stage.
        tag = look("modes/step-header", n=17)
        check(tag["packed"]["hidden"], "Pack still draws the step header")
        check(not tag["swept"]["hidden"], "Animate lost the step header as well")
        check(
            "→" in tag["swept"]["text"],
            f"the step header does not name a step: {tag['swept']['text']!r}",
        )
        check(
            tag["packed"]["stage"] == tag["swept"]["stage"],
            f"hiding the step header moved the stage: {tag['packed']['stage']} against {tag['swept']['stage']}",
        )

        # ---- step 17 (revision 14): restart, beside play and pause. The owner asked for it there,
        # and then for the thought behind it: "perhaps the restart makes more sense for Pack than
        # for Animate." One definition serves both — **back to the beginning of whatever play would
        # play** — so the transport keeps its shape across the modes. What is checked is that
        # definition, and that it is not the other reset: restart puts the picture back and keeps
        # every setting, where `reset` puts the parameters back and leaves the picture alone.
        check("restart" in api, "the API lacks restart")
        seat = look("controls/restart-seat")
        check(
            seat["i"] == seat["j"] + 1 and seat["sameRow"] and 0 <= seat["gap"] < 40,
            f"restart is not beside play and pause: {seat}",
        )
        # Revision 15: the owner's refinement -- the button does two things and should say which.
        # Paused it skips back to the start; running, what it actually does is restart the run, so
        # it swaps to a circling arrow and renames itself, exactly as play swaps to pause. The name
        # is therefore state-dependent and the check reads the paused one.
        check(
            seat["glyph"] and seat["name"] in ("Restart", "Back to the start"),
            f"restart is not drawn in the transport's own convention: {seat}",
        )
        packed_restart = look("transport/restart-in-pack", n=17, steps=600, anneal=7)
        check(
            packed_restart["before"]["steps"] >= 600,
            f"the Pack run did not run: {packed_restart['before']}",
        )
        check(
            packed_restart["after"]["steps"] == 0 and packed_restart["after"]["on"],
            f"restart in Pack did not go back to the start of the run: {packed_restart['after']}",
        )
        check(
            packed_restart["after"]["pull"] == packed_restart["before"]["pull"]
            and packed_restart["after"]["anneal"] == packed_restart["before"]["anneal"],
            f"restart in Pack changed a setting: {packed_restart}",
        )
        check(
            not packed_restart["after"]["playing"],
            "restart from a paused run started the clock",
        )
        # A run that was playing keeps playing, from the top: it is a transport control.
        ask("optimize", True)
        page.wait_for_timeout(350)
        rolling = look("transport/restart-while-playing")
        page.wait_for_timeout(300)
        check(
            rolling["was"] and rolling["playing"] and rolling["steps"] == 0,
            f"restart did not put a playing run back to the top and keep it rolling: {rolling}",
        )
        check(ask("optimizeState")["steps"] > 0, "the restarted run did not carry on")
        ask("pause")
        # In Animate the beginning is the first step of the range, not this step's own zero.
        animate_restart = look("transport/restart-in-animate", lo=16, hi=40, at=28, t=1.4)
        check(
            animate_restart["before"]["n"] == 29 and animate_restart["before"]["t"] > 1,
            f"the Animate run was not away from its first step: {animate_restart['before']}",
        )
        check(
            animate_restart["after"]["n"] == 16
            and animate_restart["after"]["t"] == 0
            and animate_restart["pair"] == animate_restart["first"],
            f"restart in Animate did not go to the first step of the range: {animate_restart}",
        )
        # And the two are different controls: reset puts the parameters back and leaves the picture,
        # restart puts the picture back and leaves the parameters.
        parted = look("transport/reset-against-restart", n=17, steps=400)
        check(
            parted["reset"]["pull"] == 0 and parted["before"]["pull"] > 0,
            f"reset did not put the law back: {parted}",
        )
        check(not parted["reset"]["playing"], "reset started the clock")
        drive(
            ("setLawPreset", "default"),
            ("setAnneal", 3),
            ("setInitial", "previous"),
            ("setStepN", 17),
        )

        # ---- step 18 (revision 14): every control sits with the axis it belongs to. A mode is a
        # choice on three independent axes — scope (one n, or a range), strategy (the law, the
        # graph, growth, annealing, and which solver runs) and presentation (colour, timing,
        # phasing, desaturation) — so a control belongs to an axis and not to the mode that
        # happened to introduce it. Three consequences are checked here.
        #
        # 18a. The solver choice is strategy: it left the step-animation group for the row that
        # carries the force law and the relationship graph.
        placed = look("controls/solver-placement")
        check(
            not placed["inStepGroup"],
            "the solver select is still inside the step-animation group",
        )
        # Revision 15: the law took a line of its own, so the solver's neighbours are the two
        # graphs rather than the law. What matters is the axis, not the adjacency: the solver is
        # strategy, so it sits among the strategy boxes and not in the step-animation group.
        # Asserting who it sat next to made a layout choice look like an invariant.
        check(
            "who attracts whom" in placed["siblings"] or "force law" in placed["siblings"],
            f"the solver select is not among the strategy boxes: {placed}",
        )
        check(
            placed["width"].endswith("px") and float(placed["width"][:-2]) > 0,
            f"the solver select has no width of its own, so hiding an option would resize it: {placed}",
        )
        # 18b. The tween is not a solver: it interpolates toward a known answer, and Pack has no
        # answer to interpolate toward. It is taken out of Pack's choices rather than left
        # selectable and inert, and a page arriving in Pack carrying it falls back and says so.
        offered = look("controls/solver-options", n=17)
        check(
            offered["animating"]["shown"] == ["tween", "physics", "bodies"]
            and offered["animating"]["solvers"] == ["tween", "physics", "bodies"],
            f"Animate does not offer all three solvers: {offered['animating']}",
        )
        check(
            offered["packing"]["shown"] == ["physics", "bodies"]
            and offered["packing"]["solvers"] == ["physics", "bodies"],
            f"Pack still offers the tween: {offered['packing']}",
        )
        check(
            offered["packing"]["style"] == "physics" and "tween" in offered["packing"]["note"],
            f"entering Pack on the tween did not fall back to the physics and say so: {offered['packing']}",
        )
        check(
            offered["chosen"]["note"] == "",
            f"the fallback note outlived the next choice: {offered['chosen']}",
        )
        check(
            offered["asked"]["style"] == "physics" and "tween" in offered["asked"]["note"],
            f"setStyle('tween') in Pack left the tween selected: {offered['asked']}",
        )
        check(
            offered["back"]["shown"] == ["tween", "physics", "bodies"]
            and offered["back"]["note"] == "",
            f"leaving Pack did not give the tween back: {offered['back']}",
        )
        # 18c. Timing and phasing are Animate's: dwell, move, settle, the motion phasing and the
        # full beat all describe a step, and Pack has none. The group is hidden there — and hidden
        # *in place*, because taking its box out of the wrapping row would rewrap the panel, shorten
        # the controls and resize the stage, which is the reflow rule revision 12 established.
        timing_group = look("controls/timing-group", n=17)
        check(
            timing_group["animating"]["holds"],
            "the timing and phasing controls are not all in the step-animation group",
        )
        check(
            timing_group["animating"]["visibility"] == "visible",
            "Animate hides its own timing group",
        )
        check(
            timing_group["packing"]["visibility"] == "hidden"
            or timing_group["packing"]["display"] == "none",
            f"Pack still shows the timing group: {timing_group['packing']}",
        )
        # Revision 15: this used to require `visibility: hidden` so the group kept its width and
        # the row could not rewrap. That reserved 1145 px of dead space in Pack and pushed the view
        # onto a line of its own, which is the ragged layout the owner reported. The group is a
        # whole row now, so removing it moves nothing beside it -- which is what the boxes below
        # actually assert. The hidden box's own geometry is deliberately not among them: a box
        # that is not drawn should not have any.
        # What must hold is that removing the group cannot reflow anything beside it, which is
        # guaranteed by it being the only panel in its row rather than by measuring neighbours.
        # The panel is deliberately shorter in Pack and the stage correspondingly larger: a mode
        # with fewer controls should give the packing more room, and pretending otherwise is what
        # reserved the dead space in the first place. So the law, which shares no row with it,
        # must not move; the shake, which follows it down the panel, is expected to rise.
        check(
            timing_group["packing"]["alone_in_row"],
            "the timing group shares its row, so hiding it would reflow its neighbours",
        )
        check(
            timing_group["packing"]["law"] == timing_group["animating"]["law"],
            f"hiding the timing group moved the law: "
            f"{timing_group['packing']['law']} against {timing_group['animating']['law']}",
        )
        drive(("setMode", "pack"), ("setStepN", 17), ("setStyle", "bodies"))

        browser.close()

    if failures:
        print("FAILED")
        for failure in dict.fromkeys(failures):
            print(" -", failure)
        return 1
    print(
        "OK: one view with no tab machinery left and setTab/tab surviving as no-ops, every control in "
        "one panel and the stage still fitting; the chooser opening on n = 17 as the one-step range 17 "
        "to 17, nine quick picks each setting both ends, clamped both ways; the range widening to the "
        "whole corpus in one click, clamped, collapsing to one step, and scoping the run and the bar's "
        "scale; the gap bar reading the panel's own s(n) bounds, sweeping to the record under style A, "
        "missing under a free run, alive in blind mode, and clear of the `n =` line and the panel edge; "
        "the bar holding still through the motion and catching up when it settles, with the per-frame "
        "sparkline gone and refreshGap redrawing it on demand; three initial conditions, the random "
        "one reproducible and the grid one the trivial grid, an open-ended run that accumulates "
        "steps, closes the walls, reports its box beside its overlap, and resumes and stops with the "
        "transport, with the two chart options on the page and setSnap still on the API; a "
        "hand that picks the topmost square, pins it against its neighbours, turns it on shift, "
        "moves the readout as it goes, marks the run hand-edited and regresses no key; and the two "
        "modes — Pack showing one n whose ends never come apart and whose transport is the "
        "open-ended run reported as a seconds counter, Animate showing a range and remembering it, "
        "with every shared setting surviving a switch either way and the scrubber gone; and the "
        "colouring being the angle map and nothing else — every retained frame from 5 to 324 "
        "painted exactly as colour() says, each class taking the slot its own centre alone gives, "
        "a shared angle taking the same fill across frames but for the one class pair that "
        "straddles a five-degree band edge, fillsFor answering the same table whatever is on the "
        "stage, a square that holds its angle holding its hue across a step, all twenty families "
        "darkening from no contacts to four at a held hue, an upright grid start painted in the "
        "teal family alone and shaded by its contacts, and no switch left: no rule control and "
        "neither setColorRule nor the k key moving a fill; and colour being the square's own "
        "identity by default — 42 greens inside the teal-to-citron band, all distinct, the "
        "closest two 0.0237 apart in OkLab and consecutive identities five times further, a "
        "square keeping its fill through a settle that turns it, two frames of one n painting "
        "a square the same, no contact shading under identity, and Animate alone repainting its "
        "resting frame in the angle map; "
        "one editable force law matching the written-out formula at every sampled gap under all "
        "four of default, rigid, soft and sticky — continuous at touching, flat at and past its "
        "range, its hump peaking at half the range at exactly the attraction, its knee at the "
        "rigidity with the stated slope either side — never pulling at any penetration over a "
        "112-setting grid, reproducing the old hard-coded 2500 * min(p, 0.15) to the bit at the "
        "shipped defaults with steep exactly zero, clamping and round-tripping every parameter, "
        "keying the trajectory cache so two laws draw two runs and one law drawn twice is "
        "byte-identical, and drawn as a plot whose curve redraws on every parameter, whose two "
        "handles sit where the four numbers put them, whose pull handle is hidden with no pull, "
        "and whose drags move the numbers and the sliders together, with the three presets "
        "reachable from the panel and lit when in use; and the relationship graph beside it, "
        "orthogonal to the law — three kinds settable and reported, repulsion never masked (the "
        "deepest overlap staying a few thousandths under every graph at n = 17 and n = 29) while "
        "attraction is (17 and 31 pairs in reach under general against none under contact), the "
        "groups mask exactly the blocks' cliques counted over members and riders, the contact "
        "target the record's own graph at 4, 17, 180, 111, 322 and 612 edges and realised by the "
        "retained frame itself bar n = 110's one tolerance-width pair, a target graph settable "
        "from outside and returnable to the record's, the mask drawn through the one overlay "
        "control on the pairs the pull is actually reaching and on none under general, and the "
        "two chart options driving the snap and the contact bias; "
        "no control moving while either playback runs or when the style, the dial, the preset, the "
        "graph, growth or n is changed, every live readout in a fixed slot or on a line of its own; "
        "no position bar in Pack, in a run or in a capture, Animate keeping it, and the stage, panel "
        "and controls the same box either way; and a contact graph drawn by hand — a real pointer "
        "press, drag and release adding an edge and the same gesture taking it away, the square "
        "drag untouched beside it, the graph normalised and held per n, reaching the mask by the "
        "one path the record's does, keyed into the trajectory cache by its own contents so the "
        "record's graph drawn by hand drives the record's run, and reported as a fraction and a "
        "container side; and the starting size redrawing the arrangement at once — the drawn width "
        "of every square proportional to the size under all three starts with growth off and on and "
        "nothing played, the staged frame identical to the one a run started at that instant begins "
        "from, the starting container the run's own and unmoved by the size, a full size restoring "
        "the timeline, and each of the three starting-arrangement buttons drawing its own picture "
        "the moment it is pressed."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
