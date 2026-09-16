"""The Animate view's standing contract: the assertions of the retired legacy checkers.

`check_workbench.py`, `check_legend.py` and `check_revision7.py` held the catalogue view's
behaviour record and ran nowhere once the page opened on Pack. What of them is still true
of the view the page shows is here, as sections of `check_animate_view`, driven through
probe files: the range and chooser, the drawn controls, the gap bar, colours, timing and
physics, the hand and its keys, the layout, the force law, the relationship graph and the
drawn graph. What was dropped, and why, is in the retirement commit.

Every section reads the settings it found, changes what it needs, and puts them back,
requiring that it did; a section that leaves the view changed fails there rather than in
whichever section runs next.
"""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Callable
from itertools import pairwise
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from workbench_tools.check_animate_view import Session

# ---------------------------------------------------------------- settings a section puts back

LAW_KEYS = ("rigidity", "repulsion", "attraction", "range")


def settings(session: Session) -> dict[str, Any]:
    """Every setting a section here may change, read so that it can be put back."""
    state = session.api(("state",))
    law = session.api(("law",))
    chosen = session.api(("range",))
    return {
        **{
            key: state[key]
            for key in (
                "style",
                "anneal",
                "speed",
                "desaturate",
                "snap",
                "blind",
                "capture",
                "links",
                "phase",
                "timing",
                "pair",
            )
        },
        "scheme": session.api(("colorScheme",)),
        "standardize": session.api(("animateStandardize",)),
        "chroma": session.api(("stageChroma",)),
        "law": {key: law[key] for key in LAW_KEYS},
        "relationship": session.api(("relationship",))["kind"],
        "target": session.api(("targetSource",)),
        "drawing": session.api(("drawing",)),
        "edges": session.api(("edges",)),
        "range": [chosen["from"], chosen["to"]],
    }


def restore(session: Session, found: dict[str, Any], section: str) -> None:
    """Put back what `settings` read, paused at the start of the step, and require it held."""
    session.api(
        ("pause",),
        ("stopAll",),
        ("release",),
        ("linkCancel",),
        ("seek", 0),
        ("setCapture", found["capture"]),
        ("setDrawing", found["drawing"]),
        ("setStyle", found["style"]),
        ("setAnneal", found["anneal"]),
        ("setSpeed", found["speed"]),
        ("setDesaturate", found["desaturate"]),
        ("setSnap", found["snap"]),
        ("setBlind", found["blind"]),
        ("setPhase", found["phase"]),
        ("setOverlay", found["links"]),
        ("setTiming", found["timing"]),
        ("setColorScheme", found["scheme"]),
        ("setAnimateStandardize", found["standardize"]),
        ("setStageChroma", found["chroma"]),
        ("setLaw", found["law"]),
        ("setRelationship", found["relationship"]),
        ("setTargetGraph", None),
        ("setTargetSource", found["target"]),
        ("setRange", *found["range"]),
        ("select", found["pair"]),
        ("seek", 0),
    )
    now = settings(session)
    changed = {key: (found[key], now[key]) for key in found if now[key] != found[key]}
    session.require(changed == {}, f"{section} did not put the view back: {changed}")


def pair_index(session: Session, n: int) -> int:
    """The pair that steps into n; a size the page does not carry is a failure, not a skip."""
    index = session.look("pairs/index-of-n", n=n)
    if index < 0:
        raise ValueError(f"the page carries no step into n = {n}")
    return index


def other(values: list[Any], current: Any) -> Any:
    """A value of the list that is not the one in force, so a round trip cannot pass idly."""
    return next(value for value in values if value != current)


# ---------------------------------------------------------------- colour measurement


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


def lab_distance(x: str, y: str) -> float:
    """Euclidean distance between two hex colours in OkLab."""
    points = []
    for lightness, chroma, hue in (oklab(x), oklab(y)):
        angle = math.radians(hue)
        points.append((lightness, chroma * math.cos(angle), chroma * math.sin(angle)))
    return math.dist(*points)


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


# ---------------------------------------------------------------- the force law, written out
# The law from its formula rather than read off the page, so `lawForce` is checked against
# something independent of itself. `steep` is derived from the rigidity: zero at a rigidity of
# 0.15 and above, eight at none.
LAW_TOL0, LAW_STEEP_MAX = 0.15, 8


def law_steep(law: dict[str, float]) -> float:
    """The slope multiplier past the knee."""
    return LAW_STEEP_MAX * max(0.0, 1 - law["rigidity"] / LAW_TOL0)


def law_force(law: dict[str, float], d: float) -> float:
    """The force at a signed gap `d`: positive pushes apart, negative pulls together."""
    if d <= 0:
        p, tol = -d, law["rigidity"]
        return law["repulsion"] * (min(p, tol) + law_steep(law) * max(0.0, p - tol))
    if not (law["attraction"] > 0 and law["range"] > 0) or d >= law["range"]:
        return 0.0
    u = d / law["range"]
    return -law["attraction"] * 4 * u * (1 - u)


def law_samples(law: dict[str, float]) -> list[float]:
    """Signed gaps worth asking a law about: a dense sweep, every breakpoint sampled exactly."""
    ds = [-0.6 + 1.2 * i / 240 for i in range(241)]
    tol = law["rigidity"]
    ds += [-tol, -tol - 1e-6, -tol + 1e-6, 0.0, 1e-12, -1e-12, 1e-9, -1e-9]
    if law["range"] > 0:
        r = law["range"]
        ds += [r, r - 1e-6, r + 1e-6, r / 2, r / 4, r * 3 / 4, r * 2]
    return sorted(set(ds))


def four(law: dict[str, Any]) -> dict[str, float]:
    """A law's four parameters, without what the page reports alongside them."""
    return {key: law[key] for key in LAW_KEYS}


def collinear(points: list[tuple[float, float]], tolerance: float) -> bool:
    """Whether every point lies on the line through the first two, to within `tolerance`."""
    (x0, y0), (x1, y1) = points[0], points[1]
    slope = (y1 - y0) / (x1 - x0)
    return all(abs(y0 + slope * (x - x0) - y) <= tolerance for x, y in points[2:])


# ---------------------------------------------------------------- the sections


def range_and_chooser(session: Session) -> str:
    """Animate opens on the corpus; n and the range are chosen, clamped and scoped."""
    page = session.page
    # W-step2-2 is about the first entry, so the page is loaded again for it.
    page.reload()
    session.enter_animate()
    corpus = session.api(("pairs",))
    first, last = corpus[0]["n"] + 1, corpus[-1]["n"] + 1
    opened = session.api(("range",))
    session.require(
        (opened["from"], opened["to"]) == (first, last),
        f"Animate does not open on the whole corpus {first}..{last}: {opened}",
    )
    found = settings(session)

    session.api(("setRange", 17, 17))
    label = session.look("dom/text", id="step-label")
    session.require(
        "16" in label and "17" in label, f"the step label does not name both ends: {label!r}"
    )
    for want in (5, 29, 272):
        got = session.api(("setStepN", want))
        chosen = session.api(("range",))
        session.require(
            got == want
            and session.api(("state",))["n"] == want - 1
            and (chosen["from"], chosen["to"]) == (want, want),
            f"setStepN({want}) landed on {got} with the range {chosen}",
        )
    chips = session.look("chips/numbers")
    session.require(len(chips) > 0, "the chooser carries no quick-pick chips")
    chip = other(chips, session.api(("stepN",)))
    clicked = session.look("chips/click", n=chip)
    session.require(
        (clicked["from"], clicked["to"]) == (chip, chip),
        f"the chip for {chip} does not set both ends: {clicked}",
    )
    low, high = session.api(("setStepN", -40)), session.api(("setStepN", 100000))
    session.require(
        (low, high) == (first, last),
        f"setStepN clamps to {low} and {high}, not {first}, {last}",
    )

    page.locator("#range-all").click()
    widened = session.api(("range",))
    session.require(
        (widened["from"], widened["to"], widened["steps"]) == (first, last, len(corpus))
        and widened["duration"] > 60,
        f"the corpus button does not widen to every pair the page carries: {widened}",
    )
    clamped = session.api(("setRange", -10, 100000))
    session.require(
        (clamped["from"], clamped["to"]) == (first, last),
        f"the range does not clamp to what the page carries: {clamped}",
    )
    crossed = session.api(("setRange", 80, 20))
    session.require(crossed["from"] <= crossed["to"], f"the range allows from > to: {crossed}")
    one = session.api(("setRange", 17, 17))
    session.require(
        (one["steps"], one["from"], one["to"], session.api(("state",))["n"]) == (1, 17, 17, 16),
        f"17 to 17 is not the one step 16 -> 17: {one}",
    )
    session.require(
        session.look("dom/text", id="range-position").strip() == "",
        "the position readout is drawn for a one-step range",
    )
    session.require(
        session.api(("progress",))["n"] in {16, 17},
        "a one-step range does not put the step 16 -> 17 on the stage",
    )
    lo, hi = first, first + 98
    wide = session.api(("setRange", lo, hi))
    session.require(
        (wide["steps"], wide["from"], wide["to"]) == (99, lo, hi),
        f"{lo}..{hi} is not 99 steps: {wide}",
    )
    session.api(("playRange",), ("pause",))
    position = session.look("dom/text", id="range-position")
    priced = session.look("dom/text", id="range-duration")
    session.require(
        session.api(("state",))["n"] == lo - 1 and session.api(("range",))["step"] == 1,
        f"playRange does not start at the range's first step: {session.api(('range',))}",
    )
    session.require(
        "1" in position and "99" in position and "99 steps" in priced,
        f"the readouts do not say step 1 of 99 steps: {position!r}, {priced!r}",
    )
    session.api(("goTo", hi - 1))
    session.require(
        session.api(("range",))["step"] == 99, f"the last step of {lo}..{hi} is not step 99"
    )
    end = session.look("range/last-step", lo=2, hi=4, step=3)
    session.require(
        (end["n"], end["last"]) == (3, 4), f"a run carries past the range's last pair: {end}"
    )
    session.api(("stopAll",))

    # A visit to the Pack panel, by its own tabs, keeps the range and every shared setting.
    session.api(("setRange", 30, 90))
    page.locator("#mode-pack").click()
    session.enter_animate()
    kept = session.api(("range",))
    session.require(
        (kept["from"], kept["to"]) == (30, 90),
        f"Animate did not come back on the range it was left on: {kept}",
    )
    anneal = session.api(("anneal",))
    want = {
        # The tween is not a solver and Pack drops it, so a physical style is carried over.
        "style": other(["bodies", "physics"], found["style"]),
        "anneal": other([anneal["max"], anneal["min"]], found["anneal"]),
        "speed": other([0.5, 1.5], found["speed"]),
        "desaturate": not found["desaturate"],
    }
    session.api(
        ("setStyle", want["style"]),
        ("setAnneal", want["anneal"]),
        ("setSpeed", want["speed"]),
        ("setDesaturate", want["desaturate"]),
        ("setRange", 30, 60),
    )
    page.locator("#mode-pack").click()
    session.enter_animate()
    state = session.api(("state",))
    kept = session.api(("range",))
    session.require(
        {key: state[key] for key in want} == want and (kept["from"], kept["to"]) == (30, 60),
        f"a Pack visit lost a setting: wanted {want} on 30..60, found {state} on {kept}",
    )
    restore(session, found, "range_and_chooser")
    return (
        "Animate opens on the corpus; the chooser and the range clamp, scope and survive Pack"
    )


def single_view(session: Session) -> str:
    """One Animate view: its API, its drawn controls, its solvers and its timing group."""
    found = settings(session)
    names = set(session.look("page/api-names"))
    wanted = (
        "setStepN",
        "stepN",
        "setRange",
        "range",
        "playRange",
        "gapBar",
        "refreshGap",
        "seek",
        "setAnneal",
        "anneal",
    )
    missing = [name for name in wanted if name not in names]
    session.require(missing == [], f"the API lacks {missing}")

    controls = [
        "panel",
        "mode-tabs",
        "range-from",
        "range-sep",
        "range-to",
        "range-all",
        "range-duration",
        "range-position",
        "play",
        "restart",
        "clock",
        "style-select",
        "anneal",
    ]
    # `#step-chips` is left out: the page marks it hidden outside Pack, but `.chips` sets its
    # display after `[hidden]` does, so Animate draws it. Which of the two is intended is an
    # owner decision (think-bead named in the retirement commit), not a checker's.
    drawn = session.look("dom/drawn", ids=controls)
    session.require(len(drawn) == len(controls), f"asked for {len(controls)}: {drawn}")
    undrawn = [ident for ident, shown, _hidden in drawn if not shown]
    session.require(undrawn == [], f"the Animate view does not draw {undrawn}")

    offered = session.look("controls/solvers-offered")
    session.require(
        offered["shown"] == offered["solvers"] == offered["styles"]
        and set(offered["styles"]) == {"tween", "physics", "bodies"},
        f"Animate does not offer every solver: {offered}",
    )
    select = session.page.locator("#style-select")
    for style in offered["shown"]:
        select.select_option(style)
        chosen = session.look("controls/solvers-offered")
        session.require(
            chosen["style"] == style and chosen["note"].strip() == "",
            f"choosing {style} gave {chosen['style']} with the note {chosen['note']!r}",
        )

    timing = [
        "t-dwell",
        "t-move",
        "t-correct",
        "t-settle",
        "phase-seg",
        "fullbeat-toggle",
        "fastsimple-toggle",
    ]
    outside = session.look("dom/contains", parent="step-anim-box", ids=timing)
    session.require(outside == [], f"the timing group does not hold {outside}")
    shown = session.look("dom/drawn", ids=["step-anim-box", *timing])
    hidden = [ident for ident, visible, _ in shown if not visible]
    session.require(
        len(shown) == len(timing) + 1 and hidden == [],
        f"Animate does not draw its timing group: {hidden}",
    )
    restore(session, found, "single_view")
    return "one view, its controls and timing group drawn, every solver offered"


def gap_bar(session: Session) -> str:
    """The gap bar reads the panel's n, spans its scale, and draws a hand only on a packing."""
    found = settings(session)
    session.api(
        ("pause",),
        ("setStyle", "tween"),
        ("setSnap", True),
        ("setBlind", False),
        ("setStepN", 17),
        ("seek", 0),
    )
    dwell, shown = session.api(("gapBar",)), session.api(("progress",))["n"]
    session.require(
        dwell["n"] == shown,
        f"through the dwell the bar is on {dwell['n']}, the panel on {shown}",
    )
    session.look("page/seek-to-end", calls=[])
    bar, facts = session.api(("gapBar",)), session.look("atlas/facts", n=17)
    session.require(
        bar["n"] == session.api(("progress",))["n"] == 17
        and abs(bar["record"] - float(facts["side"])) < 1e-9
        and abs(bar["lower"] - float(facts["lower"])) < 1e-9
        and bar["lo"] <= bar["lower"] + 1e-9
        and bar["hi"] > bar["record"],
        f"at rest the bar does not read the panel's own bounds for 17: {bar} against {facts}",
    )
    session.require(
        bar["met"] and abs(bar["excess"]) < 0.05,
        f"the tween does not reach the record by the end of the step: {bar}",
    )

    scaled = []
    for size in (16, 17, 324):
        landed = session.api(("setStepN", size))
        session.look("page/seek-to-end", calls=[])
        scale = session.api(("gapBar",))
        root = math.sqrt(size)
        scaled.append(size)
        session.require(
            landed == size
            and abs(scale["lo"] - (math.ceil(root) - 1)) < 1e-9
            and abs(scale["hi"] - scale["lo"] - 2.0) < 1e-9
            and scale["lo"] <= root <= root + 1 <= scale["hi"],
            f"the bar at n = {size} does not run two units from ceil(sqrt n) - 1 "
            f"around sqrt n and sqrt n + 1: {scale}",
        )
    session.require(len(scaled) == 3, f"the scale was read at {scaled}")

    swept = 0
    for style, n in (("physics", 17), ("bodies", 11), ("tween", 110)):
        rows = session.look("gapbar/validity-through-step", n=n, style=style)
        swept += len(rows)
        for t, valid, overlap, opacity, reason, tolerance, precision in rows:
            # Valid is the validity contract: no failing clause, penetration within the
            # tolerance applied, the contract's 1e-9 unless the frame draws a stored record.
            session.require(
                valid is (reason is None)
                and (not valid or overlap <= tolerance)
                and tolerance == (4e-6 if precision == "catalogue-precision" else 1e-9)
                and opacity == (1 if valid else 0),
                f"{style} {n} at t = {t:.3f}: valid {valid}, reason {reason}, overlap "
                f"{overlap:.2e} at {precision} tolerance {tolerance}, hand opacity {opacity}",
            )
        session.require(
            len(rows) == 6 and rows[-1][1] and not all(row[1] for row in rows),
            f"{style} {n}: the sweep saw no rest packing or no move that is not one: {rows}",
        )
    session.require(swept == 18, f"the validity sweep read {swept} instants, not 18")

    session.api(("setStyle", "tween"), ("setStepN", 17))
    session.look("page/seek-to-end", calls=[])
    met_stroke = session.look("dom/computed", id="gapbar-hand", property="stroke")
    session.look("page/seek-to-end", calls=[["setStyle", "bodies"], ["setSnap", False]])
    free = session.api(("gapBar",))
    free_stroke = session.look("dom/computed", id="gapbar-hand", property="stroke")
    session.require(
        not free["met"] and free_stroke != met_stroke and 0 <= free["x"] <= 1,
        f"a free run's hand is {free_stroke} against {met_stroke} on the record: {free}",
    )
    session.look("page/seek-to-end", calls=[["setBlind", True]])
    blind = session.api(("gapBar",))
    session.require(
        blind["side"] > 0 and 0 <= blind["x"] <= 1, f"blind mode loses the hand: {blind}"
    )

    for size, marks in ((17, 5), (16, 3)):
        session.look(
            "page/seek-to-end",
            calls=[
                ["setBlind", False],
                ["setSnap", True],
                ["setStyle", "tween"],
                ["setStepN", size],
            ],
        )
        parts = session.look("gapbar/parts")
        integers = [value for value in parts["refNums"] if "." not in value]
        session.require(
            parts["refTicks"] == marks == len(parts["refNums"]) and len(integers) == 3,
            f"n = {size}: {parts['refTicks']} marks labelled {parts['refNums']}, expected "
            f"{marks} with three integers",
        )
    session.look("page/seek-to-end", calls=[["setStepN", 17]])
    parts = session.look("gapbar/parts")
    low_mid = (parts["low"]["l"] + parts["low"]["r"]) / 2
    rec_mid = (parts["rec"]["l"] + parts["rec"]["r"]) / 2
    session.require(
        parts["open"]["t"] >= parts["track"]["t"] - 0.5
        and parts["open"]["b"] <= parts["track"]["b"] + 0.5
        and abs(parts["open"]["l"] - low_mid) < 3
        and abs(parts["open"]["r"] - rec_mid) < 3,
        f"the open span is not a band from the lower bound to the record: {parts}",
    )
    low_label, rec_label = parts["lowLabel"], parts["recLabel"]
    session.require(
        low_label["r"] < rec_label["l"] - 0.5
        or rec_label["r"] < low_label["l"] - 0.5
        or low_label["t"] > rec_label["b"] - 0.5
        or rec_label["t"] > low_label["b"] - 0.5,
        f"the bar's two numbers overlap: {low_label} and {rec_label}",
    )
    room = session.look("gapbar/clearance")
    session.require(
        room["shown"]
        and room["headTop"] >= room["packBottom"] - 0.5
        and room["headBottom"] <= room["stageBottom"] + 0.5
        and room["right"] <= room["panelRight"] + 0.5,
        f"the bar or the headline is out of its room: {room}",
    )

    index = pair_index(session, 100)
    snapped = session.api(("physics", index, "physics", "snap"))["miss"]
    blinded = session.api(("physics", index, "physics", "blind"))["miss"]
    session.require(
        snapped["centre"] < 1e-9 and blinded["excess"] > -0.001,
        f"a snapped run misses the record by {snapped} or a blind one beats it: {blinded}",
    )
    for style in session.api(("styles",)):
        reads = {}
        reads["dwell"] = session.api(
            ("stopAll",),
            ("select", index),
            ("setStyle", style),
            ("setSnap", True),
            ("setBlind", False),
            ("seek", 0),
            ("gapBar",),
        )
        session.look("page/seek-to-end", calls=[])
        reads["rest"] = session.api(("gapBar",))
        session.look("page/seek-to-end", calls=[["setSnap", False]])
        reads["free"] = session.api(("gapBar",))
        free = reads["free"]
        session.require(
            reads["dwell"]["met"]
            and reads["rest"]["met"]
            and (style == "tween" or not free["met"] or free["side"] >= free["record"] - 1e-9),
            f"{style} at n = 100: the dwell, snapped rest or free run misreads: {reads}",
        )
    agree = session.look("revision7/gap_agrees", index=index)
    session.require(
        abs(agree[0] - agree[1]) < 5e-3,
        f"the bar says {agree[0]} where the trajectory says {agree[1]}",
    )
    session.api(("setStepN", 101), ("setStyle", "bodies"), ("setSnap", False))
    span = session.api(("duration",))
    held = session.look("gapbar/refresh-on-demand", before=span * 0.5, after=span * 0.9)
    session.require(
        abs(held["demand"] - held["after"]) < 1e-9
        and abs(held["before"] - held["after"]) > 1e-6,
        f"refreshGap does not read the current frame: {held}",
    )
    restore(session, found, "gap_bar")
    return "the gap bar reads the panel's bounds and draws its hand only on a packing"


def gap_bar_holds_through_motion(session: Session) -> str:
    """Played for real, the hand holds through the move and catches up when it settles."""
    found = settings(session)
    # n = 101: 99 -> 100 is a grid prefix where nothing moves, so the bar would have nothing to
    # hold through. The beat is shortened to 1.4 s of real play; the snap makes the rest a
    # packing, so the hand has somewhere to catch up to.
    session.api(
        ("pause",),
        ("setStepN", 101),
        ("setStyle", "bodies"),
        ("setSnap", True),
        ("setTiming", {"dwell": 0.2, "move": 0.8, "correct": 0.2, "settle": 0.2}),
    )
    schedule = session.api(("schedule",))
    session.look("gapbar/sample-run")
    page = session.page
    for _ in range(40):
        page.wait_for_timeout(100)
        if not session.api(("state",))["playing"]:
            break
    samples = session.look("gapbar/samples")
    inside = (schedule["moveStart"] + 0.1, schedule["moveEnd"] - 0.05)
    mid = [row for row in samples if inside[0] < row[0] < inside[1]]
    hands = {round(row[1], 9) for row in mid}
    overlaps = {row[2] for row in mid}
    session.require(
        not session.api(("state",))["playing"] and len(mid) >= 8,
        f"the run gave {len(mid)} samples inside the move {schedule}",
    )
    session.require(len(hands) == 1, f"the hand moved {len(hands)} times through the move")
    session.require(
        len(overlaps) >= 5,
        f"the frame's own overlap took {len(overlaps)} values over {len(mid)} samples",
    )
    settled = session.api(("gapBar",))["x"]
    session.require(
        len(mid) > 0 and abs(settled - mid[0][1]) > 1e-6,
        "the hand never caught up once the motion settled",
    )
    restore(session, found, "gap_bar_holds_through_motion")
    return f"the hand holds over {len(mid)} samples of a real move and catches up"


def colours(session: Session) -> str:
    """The angle map and the identity greens, on retained frames and through steps."""
    found = settings(session)
    schemes = session.api(("colorSchemes",))
    session.require(
        schemes == ["identity", "angle-stable", "angle-continuous"]
        and found["scheme"] == schemes[0],
        f"the view is on {found['scheme']} of the schemes {schemes}, not identity",
    )
    session.require(found["standardize"] is True, "the Animate standardising is not on")
    session.api(
        ("pause",),
        ("setStyle", "tween"),
        ("setSnap", True),
        ("setBlind", False),
        ("setDesaturate", False),
        ("setStageChroma", 1),
        ("setColorScheme", "angle-stable"),
    )
    book = session.api(("colour",))
    palette, shades, tol = book["palette"], book["shades"], book["tolerance"]
    family = {
        hexed: (slot, j) for slot, fam in enumerate(shades) for j, hexed in enumerate(fam)
    }
    session.require(
        len(shades) == len(palette) > 2
        and all(len(fam) == 5 for fam in shades)
        and len(family) == 5 * len(palette),
        f"the map is not distinct five-shade families: {len(family)} hexes in {len(palette)}",
    )
    band = 90 / (len(palette) - 2)

    frames: dict[int, dict[str, Any]] = {}
    for n in (17, 29, 100, 110, 272):
        session.require(session.api(("setStepN", n)) == n, f"the page does not carry n = {n}")
        session.look("page/seek-to-end", calls=[])
        frames[n] = session.api(("colour",))
    session.require(len(frames) == 5, f"read {len(frames)} retained frames")
    for n, c in frames.items():
        slots, sizes, centres = c["slots"], c["sizes"], c["centres"]
        session.require(
            len(c["fills"]) == len(c["contacts"]) == n
            and len(slots) == len(sizes) == len(centres) == c["classes"]
            and sum(sizes) == n,
            f"n = {n}: {len(c['fills'])} fills, {len(c['contacts'])} contacts and classes "
            f"{len(slots)} / {len(sizes)} / {len(centres)} of {c['classes']}",
        )
        stray = [fill for fill in c["fills"] if fill not in family]
        session.require(stray == [], f"n = {n} painted {stray[:3]}, in no family")
        want_family: Counter[int] = Counter()
        for slot, size in zip(slots, sizes, strict=True):
            want_family[slot] += size
        drawn_family = Counter(family[f][0] for f in c["fills"] if f in family)
        drawn_shade = Counter(family[f][1] for f in c["fills"] if f in family)
        want_shade = Counter(4 - max(0, min(4, k)) for k in c["contacts"])
        session.require(
            drawn_family == want_family and drawn_shade == want_shade,
            f"n = {n} is not painted as colour() says: families {dict(drawn_family)} against "
            f"{dict(want_family)}, shades {dict(drawn_shade)} against {dict(want_shade)}",
        )
        alone = session.look("colour/fills-for-angles", angles=centres)
        wrong = [
            (centre, slot, hexed)
            for centre, slot, hexed in zip(centres, slots, alone, strict=True)
            if hexed != shades[slot][4]
        ]
        session.require(wrong == [], f"n = {n}: a class's slot is not its angle alone: {wrong}")

    def shared_angles(sizes: tuple[int, ...]) -> list[tuple[int, float, int, int, float, int]]:
        found_pairs = []
        for i, a in enumerate(sizes):
            for b in sizes[i + 1 :]:
                fa, fb = frames[a], frames[b]
                for ca, sa in zip(fa["centres"], fa["slots"], strict=True):
                    for cb, sb in zip(fb["centres"], fb["slots"], strict=True):
                        if angle_gap(ca, cb) <= tol:
                            found_pairs.append((a, ca, sa, b, cb, sb))
        return found_pairs

    core = shared_angles((17, 29, 100, 272))
    split = [pair for pair in core if pair[2] != pair[5]]
    session.require(
        len(core) >= 6 and split == [],
        f"the four frames share {len(core)} angles, {len(split)} in two slots: {split[:3]}",
    )
    both = session.look("colour/fills-for-pairs", pairs=[[pair[1], pair[4]] for pair in core])
    session.require(
        len(both) == len(core) and all(x == y for rows in both for x, y in rows),
        f"a shared angle is painted differently at some contact count: {both[:2]}",
    )
    wide = shared_angles(tuple(frames))
    straddles = [pair for pair in wide if pair[2] != pair[5]]
    for a, ca, sa, b, cb, sb in straddles:
        edge = min(fold_angle(ca) % band, band - fold_angle(ca) % band)
        session.require(
            int(fold_angle(ca) // band) != int(fold_angle(cb) // band)
            and abs(sa - sb) == 1
            and edge <= tol,
            f"n = {a}'s {ca:.4f} (slot {sa}) and n = {b}'s {cb:.4f} (slot {sb}) disagree "
            "without a band edge between them",
        )
    session.require(
        len(wide) - len(straddles) >= 10 and len(straddles) <= 2,
        f"{len(wide) - len(straddles)} shared angles agree and {len(straddles)} straddle",
    )
    sweep = [0.0, 0.4, 0.6, 12.3, 23.4513, 44.4, 44.6, 45.0, 45.3, 64.9387, 65.1299, 89.7]
    tables = []
    for n in frames:
        session.look("page/seek-to-end", calls=[["setStepN", n]])
        tables.append(session.look("colour/fills-table", angles=sweep))
    session.require(
        len(tables) == 5 and all(table == tables[0] for table in tables),
        "fillsFor answers differently with another n on the stage",
    )
    pinned = session.look("colour/fills-for-angles", angles=[0.0, 0.4, 0.6, 44.4, 44.6, 45.0])
    session.require(
        [family.get(hexed, (None,))[0] for hexed in pinned] == [0, 0, 2, 10, 1, 1],
        f"the half-degree tolerance and five-degree bands are not where they belong: {pinned}",
    )

    for slot in range(len(palette)):
        theta = 0.0 if slot == 0 else 45.0 if slot == 1 else band * (slot - 2) + band / 2
        ramp = session.look("colour/shade-ramp", angle=theta)
        lit = [oklab(hexed)[0] for hexed in ramp]
        hues = [oklab(hexed)[2] for hexed in ramp]
        allowed = 1.0 if slot < 2 else 7.0
        session.require(
            [family.get(hexed) for hexed in ramp] == [(slot, 4 - k) for k in range(5)]
            and all(x > y for x, y in pairwise(lit))
            and max(hue_gap(h, hues[0]) for h in hues) <= allowed
            and max(hue_gap(h, oklab(palette[slot])[2]) for h in hues) <= allowed,
            f"slot {slot} at {theta} degrees does not darken at a held hue: {ramp}",
        )

    session.api(("setStepN", 110), ("seek", 0))
    span = session.api(("duration",))
    snaps = []
    for fraction in (0.0, 0.15, 0.35, 0.5, 0.62, 0.75, 0.88, 1.0):
        session.api(("seek", span * fraction))
        rows = session.look("stage/drawn")
        pure = session.look("colour/fills-for-drawn", angles=[row[1] for row in rows])
        session.require(len(pure) == len(rows), f"{len(pure)} mapped fills for {len(rows)}")
        snaps.append(
            {row[0]: (row[1], row[2], mapped) for row, mapped in zip(rows, pure, strict=True)}
        )
    session.require(
        len(snaps) == 8 and all(len(snap) == 110 for snap in snaps[1:]),
        f"the step into 110 drew {[len(snap) for snap in snaps]} squares",
    )
    turned = sum(
        1
        for k, v in snaps[0].items()
        if k in snaps[-1] and angle_gap(v[0], snaps[-1][k][0]) > tol
    )
    held, moved_hue = 0, []
    for i, early in enumerate(snaps):
        for late in snaps[i + 1 :]:
            for ident, (angle, fill, mapped) in early.items():
                if ident == 110 or ident not in late:
                    continue
                angle2, fill2, mapped2 = late[ident]
                if angle_gap(angle, angle2) > tol:
                    continue
                held += 1
                drawn = (family.get(fill, (None,))[0], family.get(fill2, (None,))[0])
                if (
                    drawn[0] is None
                    or drawn[0] != drawn[1]
                    or family[mapped][0] != family[mapped2][0]
                ):
                    moved_hue.append((ident, angle, fill, angle2, fill2))
    session.require(
        turned > 0 and held >= 500 and moved_hue == [],
        f"over the step into 110, {turned} turned, {held} held their angle, and these changed "
        f"hue: {moved_hue[:3]}",
    )

    session.api(("setColorScheme", "identity"))
    greens = session.api(("colour",))["greens"]
    session.require(
        len(greens) > 1 and len(set(greens)) == len(greens), f"greens repeat: {greens}"
    )
    for hexed in greens:
        _, chroma, hue = oklab(hexed)
        session.require(
            105.0 <= hue <= 179.0
            and chroma > 0.04
            and hexed.lower() not in {"#a3123f", "#17794a"},
            f"{hexed} is not an identity green: hue {hue:.1f}, chroma {chroma:.3f}",
        )
    period = len(greens)
    closest = min(
        lab_distance(greens[i], greens[j]) for i in range(period) for j in range(i + 1, period)
    )
    by_identity = session.api(("identityFills", 3 * period))
    neighbours = min(lab_distance(x, y) for x, y in pairwise(by_identity))
    session.require(
        len(by_identity) == 3 * period
        and by_identity[period : 2 * period] == by_identity[:period]
        and sorted(by_identity[:period]) == sorted(greens)
        and neighbours > 2 * closest,
        f"the identities do not walk the {period} greens once a period with neighbours set "
        f"apart: neighbours {neighbours:.4f}, closest pair {closest:.4f}",
    )

    session.api(
        ("setAnimateStandardize", False),
        ("setStepN", 110),
        ("setStyle", "bodies"),
        ("setSnap", False),
        ("seek", 0),
    )
    span = session.api(("duration",))
    settle = []
    for fraction in (0.0, 0.3, 0.6, 1.0):
        session.api(("seek", span * fraction))
        settle.append({row[0]: (row[1], row[2]) for row in session.look("stage/drawn")})
    moved = sum(
        1
        for k, v in settle[0].items()
        if k in settle[-1] and angle_gap(v[0], settle[-1][k][0]) > 0.5
    )
    repainted = [
        (k, settle[0][k][1], snap[k][1])
        for snap in settle[1:]
        for k in settle[0]
        if k in snap and k != 110 and settle[0][k][1] != snap[k][1]
    ]
    session.require(
        len(settle) == 4 and moved >= 5 and repainted == [],
        f"over a settle at 110, {moved} squares turned and these repainted: {repainted[:3]}",
    )
    session.look(
        "page/seek-to-end", calls=[["setStepN", 29], ["setStyle", "tween"], ["setSnap", True]]
    )
    frame = {row[0]: row[2] for row in session.look("stage/drawn")}
    pure = session.api(("identityFills", 29))
    wrong = [(k, frame[k], pure[k - 1]) for k in sorted(frame) if frame[k] != pure[k - 1]]
    session.require(
        len(frame) == 29 and wrong == [],
        f"a drawn fill is not its identity's green: {wrong[:3]}",
    )

    session.api(("setAnimateStandardize", True), ("setRange", 29, 29))
    span = session.api(("duration",))
    rest = session.api(("seek", span), ("colour",))
    moving = session.api(("seek", span * 0.55), ("colour",))
    unstandard = session.api(("setAnimateStandardize", False), ("seek", span), ("colour",))
    session.require(
        (rest["painted"], rest["scheme"], moving["painted"], unstandard["painted"])
        == ("angle-atlas", "identity", "identity", "identity"),
        f"Animate paints its rest frame {rest['painted']} under {rest['scheme']}, a moving "
        f"frame {moving['painted']}, and a rest frame unstandardised {unstandard['painted']}",
    )
    restore(session, found, "colours")
    return (
        f"five retained frames painted as colour() says, {len(core)} angles shared by four and "
        f"{len(wide) - len(straddles)} agreeing over five ({len(straddles)} straddling a band "
        f"edge); {held} held square-instants keep their hue; greens hold through a settle"
    )


def timing_transport_physics(session: Session) -> str:
    """Progress, restart, the annealing cache, trajectory cost and the settled side."""
    found = settings(session)
    session.look("revision7/set_full_range")
    walk = session.look("revision7/walk")
    session.require(
        len(walk) == 9
        and abs(walk[0]) < 1e-9
        and abs(walk[-1] - 1) < 1e-9
        and all(b >= a - 1e-12 for a, b in pairwise(walk)),
        f"progress does not run 0 to 1 without going back: {walk}",
    )
    index = pair_index(session, 100)
    anneal = session.api(("anneal",))
    reproduced = session.look(
        "physics/anneal-reproduces", index=index, levels=[anneal["max"], anneal["min"]]
    )
    session.require(
        reproduced["first"] == reproduced["again"]
        and reproduced["first"] != reproduced["other"]
        and reproduced["level"] == anneal["level"],
        f"a level does not reproduce its trajectory after another ran: {reproduced}",
    )

    session.require("restart" in session.look("page/api-names"), "the API lacks restart")
    seat = session.look("controls/restart-seat")
    session.require(
        seat["i"] == seat["j"] + 1
        and seat["sameRow"]
        and 0 <= seat["gap"] < 40
        and seat["glyph"]
        and seat["name"] in {"Restart", "Back to the start"},
        f"restart is not a glyph beside play: {seat}",
    )
    span = session.api(("setRange", 16, 40), ("goTo", 28), ("duration",))
    restarted = session.look("transport/restart-in-animate", lo=16, hi=40, at=28, t=span * 0.6)
    session.require(
        restarted["before"]["n"] > 16 and restarted["before"]["t"] > 0,
        f"the run was not away from its first step: {restarted}",
    )
    session.require(
        restarted["after"]["n"] == 16
        and restarted["after"]["t"] == 0
        and restarted["pair"] == restarted["first"],
        f"restart did not go to the start of the range's first step: {restarted}",
    )

    built = []
    for n in (11, 100, 324):
        at = pair_index(session, n)
        for style in ("physics", "bodies"):
            cost = session.look("physics/build", index=at, style=style)
            built.append((n, style, cost["ms"], cost["bytes"]))
    slow = [row for row in built if not (row[2] < 400.0 and row[3] < 4_000_000)]
    session.require(
        len(built) == 6 and slow == [], f"a trajectory costs over 400 ms or 4 MB: {slow}"
    )

    settled = []
    session.api(("setStyle", "tween"), ("setSnap", True))
    for n in (17, 29, 110, 272):
        session.require(session.api(("setStepN", n)) == n, f"the page does not carry n = {n}")
        session.look("page/seek-to-end", calls=[])
        relationship = session.api(("relationship",))
        settled.append(n)
        session.require(
            abs(relationship["side"] - relationship["record"]) < 1e-9,
            f"the settled frame at n = {n} is {relationship['side']}, not the record's "
            f"{relationship['record']}",
        )
    session.require(len(settled) == 4, f"the settled side was read at {settled}")
    snap = session.look("controls/snap-toggle")
    session.require(
        snap["flipped"] is not snap["was"]
        and snap["back"] is snap["was"]
        and snap["shown"] is snap["was"],
        f"the snap box does not drive and read back state().snap: {snap}",
    )
    restore(session, found, "timing_transport_physics")
    slowest = max(row[2] for row in built)
    return (
        f"progress, restart and the settled side hold; the dearest trajectory {slowest:.0f} ms"
    )


def hand_and_keys(session: Session) -> str:
    """The hand grabs from the timeline and a real pointer; the bare keys still work."""
    found = settings(session)
    page = session.page
    session.api(
        ("pause",), ("setStyle", "tween"), ("setSnap", True), ("setStepN", 17), ("seek", 0)
    )
    x, y, _ = session.api(("poseOf", 0))
    grabbed = session.look("hand/grab-from-timeline", x=x, y=y)
    session.require(
        grabbed["i"] >= 0
        and grabbed["g"] == grabbed["i"]
        and not grabbed["before"]
        and grabbed["optimizing"]
        and grabbed["edited"]
        and session.api(("optimizeState",))["edited"] is True,
        f"a grab from the timeline did not start a hand-edited run: {grabbed}",
    )
    before = session.api(("gapBar",))["side"]
    after = session.api(("dragTo", x + 4, y, False), ("gapBar",))["side"]
    session.require(abs(after - before) > 1e-9, f"the side did not follow a drag: {before}")
    session.api(("release",), ("seek", 0))

    session.api(("play",))
    picked = session.api(("pickAt", x, y))
    held = session.api(("grab", picked, x, y), ("hand",))["held"]
    state = session.api(("state",))
    session.require(
        held >= 0 and state["playing"] and state["optimizing"],
        f"a grab during playback did not carry on running: held {held}, {state}",
    )
    session.api(("release",), ("pause",), ("setStepN", 17), ("seek", 0))

    session.look("dom/blur")
    page.keyboard.press("ArrowRight")
    right = session.api(("stepN",))
    page.keyboard.press("ArrowLeft")
    session.require(
        (right, session.api(("stepN",))) == (18, 17), f"the arrows step n to {right} and back"
    )
    styles = session.api(("styles",))
    start = session.api(("state",))["style"]
    page.keyboard.press("p")
    cycled = session.api(("state",))["style"]
    for _ in styles[1:]:
        page.keyboard.press("p")
    session.require(
        cycled == styles[(styles.index(start) + 1) % len(styles)]
        and session.api(("state",))["style"] == start,
        f"p does not cycle {styles} from {start}: went to {cycled}",
    )
    page.keyboard.press(" ")
    playing = session.api(("state",))["playing"]
    page.keyboard.press(" ")
    session.require(
        playing and not session.api(("state",))["playing"], "space does not play and pause"
    )
    keys = ("capture", "snap", "style", "blind", "playing")
    before_keys = {key: session.api(("state",))[key] for key in keys}
    for combo in ("Meta+c", "Control+c", "Meta+s", "Meta+p", "Alt+b"):
        page.keyboard.press(combo)
        after_keys = {key: session.api(("state",))[key] for key in keys}
        session.require(after_keys == before_keys, f"{combo} acted as a shortcut: {after_keys}")
    page.keyboard.press("c")
    captured = session.api(("state",))["capture"]
    page.keyboard.press("Escape")
    session.require(
        captured and not session.api(("state",))["capture"],
        "a bare c does not enter capture or Escape does not leave it",
    )

    session.look(
        "page/seek-to-end",
        calls=[["setStepN", 11], ["setDrawing", True], ["clearEdges"]],
    )
    ax, ay = session.look("stage/screen-of", index=0)
    page.mouse.move(ax, ay)
    page.mouse.down()
    page.mouse.move(ax + 40, ay + 40, steps=3)
    drawing_held = session.api(("hand",))["held"]
    page.mouse.up()
    session.api(("setDrawing", False), ("clearEdges",))
    page.mouse.move(ax, ay)
    page.mouse.down()
    page.mouse.move(ax + 40, ay + 40, steps=3)
    dragged = session.api(("hand",))["held"]
    page.mouse.up()
    hand = session.api(("hand",))
    session.require(
        drawing_held < 0
        and dragged == 0
        and hand["edited"] is True
        and session.api(("edges",)) == [],
        f"a pointer press held {drawing_held} with drawing on and {dragged} with it off "
        f"({hand}, edges {session.api(('edges',))})",
    )
    session.api(("seek", 0), ("clearEdges",))
    restore(session, found, "hand_and_keys")
    return "grabs start hand-edited runs, a real drag holds its square, the keys still act"


def stage_layout(session: Session) -> str:
    """The stage fits the window, and nothing clicked moves while the view changes."""
    found = settings(session)
    fits = session.look("stage/fits-window")
    session.require(
        fits["top"] >= -0.5 and fits["bottom"] <= fits["h"] + 0.5,
        f"the stage does not fit the window: {fits}",
    )

    def unmoved(before: list[list[Any]], label: str) -> None:
        after = session.look("controls/button-boxes")
        moved = (
            [(a, b) for a, b in zip(before, after, strict=True) if a != b]
            if len(before) == len(after)
            else ["the button count changed"]
        )
        session.require(moved == [], f"{label} moved a control: {moved[:3]}")

    span = session.api(("setRange", 16, 30), ("playRange",), ("pause",), ("duration",))
    session.api(("seek", span * 0.2))
    early = session.look("controls/button-boxes")
    early_label = session.look("dom/text", id="step-label")
    session.require(len(early) >= 20, f"only {len(early)} buttons in the controls")
    session.api(("goTo", 28), ("seek", span * 0.8))
    session.require(
        session.look("dom/text", id="step-label") != early_label,
        "the step label did not change across the pairs, so the check has no teeth",
    )
    unmoved(early, "a range run across a pair boundary")

    session.api(("stopAll",), ("setStepN", 17), ("seek", 0))
    base = session.look("controls/button-boxes")
    anneal = session.api(("anneal",))
    presets = session.api(("lawPresets",))
    for label, call in (
        ("the style", ("setStyle", other(session.api(("styles",)), found["style"]))),
        (
            "the annealing dial",
            ("setAnneal", other([anneal["max"], anneal["min"]], found["anneal"])),
        ),
        ("the law preset", ("setLawPreset", presets[-1])),
        ("the graph", ("setRelationship", "contact")),
        (
            "the colour scheme",
            ("setColorScheme", other(session.api(("colorSchemes",)), found["scheme"])),
        ),
        ("the size", ("setStepN", 324)),
        ("the size again", ("setStepN", 5)),
    ):
        session.api(call)
        unmoved(base, f"changing {label}")

    ids = [
        "clock",
        "speed-info",
        "range-duration",
        "range-position",
        "step-label",
        "step-note",
        "law-info",
        "rel-info",
        "anneal-info",
        "continuous-info",
    ]
    slots = session.look("controls/readout-slots", ids=ids)
    loose = [
        (ident, is_readout, width, overflow)
        for ident, is_readout, width, overflow, _ in slots
        if not (
            is_readout
            and overflow == "hidden"
            and width.endswith("px")
            and float(width[:-2]) > 0
        )
    ]
    session.require(
        len(slots) == len(ids) and loose == [],
        f"a live readout is not in a fixed slot: {loose}",
    )
    session.require(
        sum(1 for *_, full_line in slots if full_line) >= 4,
        "fewer than four readouts take a line of their own",
    )
    restore(session, found, "stage_layout")
    return "the stage fits; no control moves across a pair boundary or a setting"


def force_law(session: Session) -> str:
    """The law is its written formula, clamps, keys runs, and its plot and presets follow it."""
    found = settings(session)
    shipped = session.api(("law",))
    bounds = shipped["bounds"]
    presets = session.api(("lawPresets",))
    session.require(len(presets) >= 2, f"the law offers the presets {presets}")
    custom = {"rigidity": 0.05, "repulsion": 1000, "attraction": 200, "range": 0.3}
    laws: dict[str, dict[str, float]] = {}
    for name in ["default", *presets]:
        got = session.api(("setLawPreset", name))
        laws[name] = four(got)
        session.require(
            abs(got["steep"] - law_steep(laws[name])) < 1e-12,
            f"the {name} law's steep is {got['steep']}, not {law_steep(laws[name])}",
        )
    session.require(laws["default"] == four(shipped["defaults"]), "default is not the defaults")
    session.require(
        four(session.api(("setLaw", custom))) == custom, "a law inside the bounds is not taken"
    )
    laws["custom"] = custom
    for name, law in laws.items():
        session.api(("setLaw", law))
        ds = law_samples(law)
        fs = session.look("law/forces-at", gaps=ds)
        session.require(len(fs) == len(ds), f"{len(fs)} forces for {len(ds)} gaps")
        off = [
            (d, f, law_force(law, d))
            for d, f in zip(ds, fs, strict=True)
            if abs(f - law_force(law, d)) > 1e-9 * max(1.0, abs(law_force(law, d)))
        ]
        at = dict(zip(ds, fs, strict=True))
        reach = law["range"] if law["attraction"] > 0 else 0.0
        beyond = [f for d, f in at.items() if d >= reach > 0 or (reach == 0 and d > 0)]
        tol, rep = law["rigidity"], law["repulsion"]
        inside = session.look("law/forces-at", gaps=[-tol * 0.75, -tol * 0.25])
        past = session.look("law/forces-at", gaps=[-tol - 0.15, -tol - 0.05])
        steeper = rep * law_steep(law)
        session.require(
            off == []
            and at[0.0] == 0
            and abs(at[1e-12]) < 1e-6
            and abs(at[-1e-12]) < 1e-6
            and len(beyond) >= 20
            and all(f == 0 for f in beyond)
            and abs(at[-tol] - rep * tol) < 1e-9
            and abs((inside[0] - inside[1]) / (tol * 0.5) - rep) < 1e-6 * rep
            and abs((past[0] - past[1]) / 0.1 - steeper) <= 1e-6 * max(steeper, rep),
            f"the {name} law departs from its formula: {off[:3]} (knee {at[-tol]}, "
            f"zero tail {len(beyond)})",
        )
        if law["attraction"] > 0:
            session.require(
                at[law["range"] / 2] == -law["attraction"] == min(fs),
                f"the {name} law's pull does not peak at half its range: {min(fs)}",
            )
    session.require(
        any(law["attraction"] > 0 for law in laws.values()), "no law sampled here pulls"
    )

    grid = [
        dict(zip(LAW_KEYS, values, strict=True))
        for values in _grid(
            [[lo, (lo + hi) / 2, hi] for lo, hi in (bounds[k] for k in LAW_KEYS)]
        )
    ]
    grid += list(laws.values())
    pulls = session.look("law/never-pulls", laws=grid)
    session.require(
        len(grid) == 81 + len(presets) + 2 and pulls == [],
        f"the law pulls at a penetration over {len(grid)} settings: {pulls[:3]}",
    )

    middle = {"rigidity": 0.123, "repulsion": 3333, "attraction": 250, "range": 0.375}
    session.require(
        all(bounds[k][0] < middle[k] < bounds[k][1] for k in LAW_KEYS),
        f"the round-trip law is outside the bounds {bounds}",
    )
    moved = session.look(
        "law/clamps-and-round-trips",
        low={k: bounds[k][0] - 9 for k in LAW_KEYS},
        high={k: bounds[k][1] * 10 + 9 for k in LAW_KEYS},
        middle=middle,
    )
    segment = [part for part in moved["stray"].split("|") if part.startswith("pair:")]
    session.require(
        moved["lo"] == {k: bounds[k][0] for k in LAW_KEYS}
        and moved["hi"] == {k: bounds[k][1] for k in LAW_KEYS}
        and moved["mid"] == moved["back"] == moved["junk"] == moved["none"] == middle
        and segment == ["pair:0.123:3333:250:0.375"],
        f"the law does not clamp, round-trip and ignore junk: {moved}",
    )
    keyed = session.look(
        "law/cache-key",
        n=17,
        presets={"a": "default", "b": presets[0], "c": "default", "d": presets[1]},
    )
    session.require(
        len({keyed["a"], keyed["b"], keyed["d"]}) == 3 and keyed["a"] == keyed["c"],
        f"the law is not what the trajectory cache is keyed by: {keyed}",
    )

    curves = [session.look("dom/attribute", id="lp-curve", name="d")]
    session.api(("setLawPreset", "default"))
    for nudge in (
        {"rigidity": 0.2},
        {"repulsion": 3000},
        {"attraction": 200, "range": 0.3},
        {"range": 0.45},
    ):
        session.api(("setLaw", nudge))
        curves.append(session.look("dom/attribute", id="lp-curve", name="d"))
    session.require(
        len(set(curves)) == 5 and all(curve.startswith("M") for curve in curves),
        f"a parameter changed without redrawing the curve: {len(set(curves))} of 5 distinct",
    )
    # The plot's geometry as properties rather than its pixel constants: the knee, the touching
    # mark and the pull handle share one gap axis across, and the push and the pull hang from
    # one zero line down. Handles are placed to a hundredth of a pixel, so 0.05 is the slack.
    low, high = bounds["rigidity"]
    knees, pushes = [], []
    for rigidity in (low, (low + high) / 2, high):
        session.api(("setLaw", {"rigidity": rigidity, "repulsion": 1000, "attraction": 0}))
        handles = session.look("law/plot-handles")
        knees.append((-rigidity, handles["knee"][0]))
        session.require(
            not handles["shown"] and handles["top"] >= session.api(("law",))["pushAtKnee"],
            f"with no pull the plot draws a pull handle or tops out under the knee: {handles}",
        )
    tops = set()
    for repulsion in (300, 500, 600):
        law = session.api(
            ("setLaw", {"rigidity": 0.3, "repulsion": repulsion, "attraction": 0})
        )
        handles = session.look("law/plot-handles")
        tops.add(handles["top"])
        pushes.append((law["pushAtKnee"], handles["knee"][1]))
    pulls = []
    for attraction in (100, 200, 300):
        session.api(("setLaw", {"attraction": attraction, "range": 0.3}))
        handles = session.look("law/plot-handles")
        pulls.append((attraction, handles["pull"][1]))
    (d0, x0), (d1, x1) = knees[0], knees[1]
    gap_x = (x1 - x0) / (d1 - d0)
    (p0, y0), (p1, y1) = pushes[0], pushes[1]
    zero = y0 - p0 * (y1 - y0) / (p1 - p0)
    (a0, v0), (a1, v1) = pulls[0], pulls[1]
    session.require(
        gap_x > 0
        and collinear(knees, 0.05)
        and len(tops) == 1
        and y1 < y0
        and collinear(pushes, 0.05)
        and v1 > v0
        and collinear(pulls, 0.05)
        and abs(v0 - a0 * (v1 - v0) / (a1 - a0) - zero) < 0.05,
        f"the knee and pull handles are not placed on one gap axis and one zero line: knees "
        f"{knees}, pushes {pushes} under tops {tops}, pulls {pulls}",
    )
    handles = session.look("law/plot-handles")
    session.require(
        handles["shown"]
        and abs(handles["cross"] - (x0 - gap_x * d0)) < 0.05
        and abs(handles["pull"][0] - (x0 + gap_x * (0.15 - d0))) < 0.05,
        f"the touching mark or the pull handle is off the knee's gap axis: {handles}, {knees}",
    )
    for name in ["default", *presets]:
        law = session.api(("setLawPreset", name))
        attracts = law["attraction"] > 0 and law["range"] > 0
        session.require(
            session.look("law/plot-handles")["shown"] == attracts,
            f"the {name} law's pull handle is drawn {not attracts}",
        )
    base = four(session.api(("setLawPreset", "default")))
    knee = session.look("law/drag-handle", handle="knee", d=-0.1, f=300)
    pull = session.look("law/drag-handle", handle="pull", d=0.1, f=-200)
    want_knee = {**base, "rigidity": 0.1, "repulsion": 3000}
    want_pull = {**want_knee, "attraction": 200, "range": 0.2}
    session.require(
        knee["law"] == want_knee
        and [float(v) for v in knee["sliders"]] == [want_knee[k] for k in LAW_KEYS]
        and pull["law"] == want_pull
        and [float(v) for v in pull["sliders"]] == [want_pull[k] for k in LAW_KEYS]
        and pull["shown"],
        f"dragging the handles did not move the law and its sliders together: {knee}, {pull}",
    )
    pulling = max(presets, key=lambda name: laws[name]["attraction"])
    sampled = session.look("law/curve-samples", preset=pulling, samples=40)
    ends = [-2 * laws[pulling]["rigidity"], laws[pulling]["range"]]
    session.require(
        sampled["n"] == 41
        and sampled["rising"]
        and sampled["off"] == 0
        and all(abs(a - b) < 1e-12 for a, b in zip(sampled["ends"], ends, strict=True)),
        f"lawCurve(40) under {pulling} is not 41 rising samples over {ends}: {sampled}",
    )
    for name in presets:
        lit = session.look("law/press-preset", name=name)
        session.require(
            lit["law"] == laws[name] and lit["on"] == [name],
            f"the {name} button set {lit['law']} and lit {lit['on']}",
        )
    session.api(("setLawPreset", "default"))
    session.require(
        session.look("dom/count", selector="#law-preset-seg button.on") == 0,
        "a preset is still lit with the default law in use",
    )
    restore(session, found, "force_law")
    return (
        f"the law matches its formula under {len(laws)} laws and never pulls over {len(grid)}"
    )


def _grid(axes: list[list[float]]) -> list[list[float]]:
    """Every combination of one value from each axis."""
    combinations: list[list[float]] = [[]]
    for axis in axes:
        combinations = [[*prefix, value] for prefix in combinations for value in axis]
    return combinations


def relationship_graph(session: Session) -> str:
    """Who attracts whom: three graphs, the groups mask, the target as drawn, and the bias."""
    found = settings(session)
    kinds = session.api(("relationships",))
    session.require(kinds == ["general", "groups", "contact"], f"the graphs are {kinds}")
    for kind in kinds:
        reported = session.api(("setRelationship", kind))["kind"]
        session.require(
            reported == kind == session.api(("relationship",))["kind"],
            f"setRelationship({kind!r}) reported {reported}",
        )
    session.require(
        session.api(("setRelationship", "nonesuch"))["kind"] == "general",
        "an unknown graph does not fall back to general",
    )

    counted = []
    session.api(("setStyle", "tween"), ("setSnap", True))
    for n in (11, 17, 29, 110):
        session.require(session.api(("setStepN", n)) == n, f"the page does not carry n = {n}")
        session.api(("setRelationship", "groups"))
        mask = session.look("relationship/groups-mask-cliques")
        counted.append(mask["maskEdges"])
        session.require(
            mask["maskEdges"] == mask["byOf"] == mask["byBlocks"] and mask["maskEdges"] < 60000,
            f"the groups mask at n = {n} is not the blocks' cliques: {mask}",
        )
    session.require(
        len(counted) == 4 and sum(counted) > 0, f"the groups masks counted {counted} pairs"
    )

    session.api(("setRelationship", "general"), ("setStepN", 17))
    swapped = session.look("relationship/target-swap", graph=[[0, 1], [1, 2]])
    session.require(
        swapped["from"] == swapped["target"] == "record"
        and swapped["given"] == {"graph": [0, 1, 1, 2], "target": "given", "edges": 2}
        and swapped["after"] == swapped["before"],
        f"setTargetGraph does not replace the target and go back: {swapped}",
    )

    presets = session.api(("lawPresets",))
    pulls = {name: session.api(("setLawPreset", name))["attraction"] for name in presets}
    pulling = max(presets, key=lambda name: pulls[name])
    session.require(pulls[pulling] > 0, f"no preset pulls: {pulls}")
    session.look(
        "page/seek-to-end",
        calls=[
            ["setLawPreset", pulling],
            ["setStepN", 29],
            ["setOverlay", False],
            ["setTargetSource", "record"],
        ],
    )
    drawn = {}
    for kind in kinds:
        session.api(("setRelationship", kind))
        drawn[kind] = session.look("mask/links")
    relationship = session.api(("relationship",))
    contact = drawn["contact"]
    session.require(
        drawn["general"]["drawn"] == 0
        and drawn["groups"]["drawn"] == 0
        and contact["shown"]
        and contact["drawn"] == relationship["edges"] > 0
        and contact["met"] == relationship["met"] == relationship["edges"]
        and contact["unmet"] == 0,
        f"with the overlay off only the contact target is drawn, all met at rest: {drawn}, "
        f"{relationship}",
    )
    session.api(("seek", 0))
    dwell = session.look("mask/links")
    styles = session.look("mask/link-styles")
    session.require(
        dwell["met"] + dwell["unmet"] == dwell["drawn"] and dwell["unmet"] > 0,
        f"the dwell, which does not realise the target, draws no unmet edge: {dwell}",
    )
    session.require(
        styles["met"] is not None
        and styles["unmet"] is not None
        and styles["met"] != styles["unmet"],
        f"met and unmet edges are not drawn apart: {styles}",
    )
    session.look(
        "page/seek-to-end", calls=[["setRelationship", "groups"], ["setOverlay", True]]
    )
    grouped = session.look("mask/links")
    related = session.api(("relationship",))["maskEdges"]
    session.api(("setOverlay", False))
    session.require(
        grouped["shown"]
        and 0 < grouped["drawn"] < related
        and session.look("mask/links")["drawn"] == 0,
        f"the groups mask draws {grouped} of {related} pairs, or outlives the overlay",
    )
    boxes = session.look("controls/checkbox-ids")
    session.require(
        [box for box in boxes if "mask" in box or "overlay" in box] == [],
        f"the mask added an overlay control of its own: {boxes}",
    )
    rode = session.look("mask/rides-overlay")
    session.require(
        rode["on"] and rode["off"] and rode["links"] is False,
        f"the groups mask does not ride the overlay's own control: {rode}",
    )

    session.api(
        ("setStepN", 17),
        ("setRelationship", "general"),
        ("setLaw", {"attraction": 0, "range": 0}),
    )
    biased = session.look("controls/bias-toggle")
    session.require(
        biased["before"] == 0
        and biased["on"]["attraction"] > 0
        and biased["on"]["range"] > 0
        and biased["on"]["kind"] == "contact"
        and biased["on"]["checked"]
        and biased["off"]["kind"] == "general"
        and not biased["off"]["checked"],
        f"the bias does not bring the contact graph and a pull, and go back: {biased}",
    )
    session.api(("setLawPreset", pulling), ("setRelationship", "general"))
    again = session.look("controls/bias-toggle-with-pull")
    session.require(
        again["on"] == {"kind": "contact", "attraction": pulls[pulling]}
        and again["kind"] == "general",
        f"from a law that pulls, the bias touches more than the graph: {again}",
    )
    session.api(("setLaw", {"attraction": 0, "range": 0}), ("setRelationship", "general"))
    alone = session.look("relationship/set-touches-law", kind="contact")
    session.require(
        alone["before"] == alone["after"] and alone["kind"] == "contact",
        f"setRelationship touched the law: {alone}",
    )
    session.api(("setLawPreset", pulling))
    graphed = session.look(
        "relationship/cache-key", n=17, kinds=["general", "contact", "groups", "general"]
    )
    session.require(
        len({runs[0] for runs in graphed.values()}) == 3
        and len(graphed["general"]) == 2
        and graphed["general"][0] == graphed["general"][1],
        f"the graph is not what the trajectory cache is keyed by: {graphed}",
    )
    restore(session, found, "relationship_graph")
    return "three graphs, the groups mask as cliques, the target drawn met and unmet, the bias"


def drawn_graph(session: Session) -> str:
    """A contact graph drawn by a real pointer is the same object the record's graph is."""
    found = settings(session)
    page = session.page
    session.look(
        "page/seek-to-end",
        calls=[
            ["setStyle", "tween"],
            ["setSnap", True],
            ["setStepN", 11],
            ["setDrawing", False],
            ["clearEdges"],
            ["setTargetSource", "record"],
            ["setRelationship", "contact"],
        ],
    )
    record_edges = session.api(("relationship",))["edges"]
    session.api(("setRelationship", "general"))
    session.require(
        record_edges > 0
        and session.api(("targetSources",)) == ["record", "drawn"]
        and session.api(("targetSource",)) == "record"
        and session.api(("edges",)) == [],
        f"n = 11 does not start on the record's graph of {record_edges} edges, none drawn",
    )
    session.require(
        session.api(("setDrawing", True)) is True and session.api(("targetSource",)) == "drawn",
        "turning drawing on did not point the target at the drawn graph",
    )
    ax, ay = session.look("stage/screen-of", index=0)
    bx, by = session.look("stage/screen-of", index=3)
    page.mouse.move(ax, ay)
    page.mouse.down()
    page.mouse.move((ax + bx) / 2, (ay + by) / 2, steps=4)
    pending = session.look("draw/pending-edge")
    page.mouse.move(bx, by, steps=4)
    page.mouse.up()
    added = session.api(("edges",))
    line = session.look("dom/display", id="draw-line")
    page.mouse.move(bx, by)
    page.mouse.down()
    page.mouse.move(ax, ay, steps=4)
    page.mouse.up()
    removed = session.api(("edges",))
    page.mouse.move(ax, ay)
    page.mouse.down()
    page.mouse.move(4, 4, steps=3)
    page.mouse.up()
    session.require(
        pending["shown"]
        and pending["x1"] != pending["x2"]
        and added == [[0, 3]]
        and line == "none"
        and removed == []
        and session.api(("edges",)) == [],
        f"the gesture drew {pending}, added {added} (line {line!r}), took it away to "
        f"{removed}, and on paper left {session.api(('edges',))}",
    )
    session.require(
        session.look("draw/self-link", index=2) is False, "a square can be joined to itself"
    )
    session.api(("linkCancel",), ("setDrawing", False))

    graph = [[0, 1], [1, 2], [2, 3], [0, 3], [4, 5]]
    session.require(
        session.api(("setEdges", graph)) == graph, "setEdges did not take the graph"
    )
    relationship = session.api(("setRelationship", "contact"))
    session.require(
        session.api(("targetSource",)) == "drawn"
        and (relationship["edges"], relationship["drawn"], relationship["target"])
        == (5, 5, "drawn")
        and relationship["maskEdges"] == 5
        and session.api(("targetGraph",)) == [0, 1, 1, 2, 2, 3, 0, 3, 4, 5],
        f"the relationship and its mask do not read the drawn graph: {relationship}",
    )
    normalised = session.api(("setEdges", [[1, 0], [0, 1], [2, 2], [3, 900], [-1, 4], [5, 4]]))
    session.api(("setStepN", 5))
    at_five = session.api(("edges",))
    session.api(("setEdges", [[0, 2]]), ("setStepN", 11))
    back = session.api(("edges",))
    recorded = session.api(("setTargetSource", "record"), ("relationship",))
    session.require(
        normalised == [[0, 1], [4, 5]] and at_five == [] and back == [[0, 1], [4, 5]],
        f"the drawn graph is not normalised and held per n: {normalised}, {at_five}, {back}",
    )
    session.require(
        (recorded["target"], recorded["edges"], recorded["drawn"])
        == ("record", record_edges, 2),
        f"the record's graph is not what the target goes back to: {recorded}",
    )
    session.require(session.api(("clearEdges",)) == [], "clearEdges left something behind")
    session.api(("setStepN", 5), ("clearEdges",))

    presets = session.api(("lawPresets",))
    pulling = max(presets, key=lambda name: session.api(("setLawPreset", name))["attraction"])
    session.api(
        ("setLawPreset", pulling),
        ("setStepN", 17),
        ("setRelationship", "contact"),
        ("setTargetSource", "record"),
    )
    recorded_graph = session.api(("targetGraph",))
    keyed = session.look(
        "draw/graph-cache-key",
        walk=[
            ["record", None],
            ["two", [[0, 1], [2, 3]]],
            ["three", [[0, 1], [2, 3], [4, 5]]],
            ["twoAgain", [[0, 1], [2, 3]]],
            ["recordAgain", None],
        ],
    )
    session.require(
        len({keyed[k]["key"] for k in ("record", "two", "three")}) == 3
        and keyed["two"] == keyed["twoAgain"]
        and keyed["record"] == keyed["recordAgain"],
        f"a drawn graph does not key its own run: {keyed}",
    )
    same = session.look("draw/record-graph-by-hand", graph=recorded_graph)
    session.require(
        same["fromRecord"] == same["fromHand"],
        f"the record's graph drawn by hand drives a different run: {same}",
    )
    session.api(("clearEdges",), ("setTargetSource", "record"))
    restore(session, found, "drawn_graph")
    return "a pointer draws and removes an edge; the drawn graph is normalised, per n and keyed"


SECTIONS: tuple[Callable[[Session], str], ...] = (
    range_and_chooser,
    single_view,
    gap_bar,
    gap_bar_holds_through_motion,
    colours,
    timing_transport_physics,
    hand_and_keys,
    stage_layout,
    force_law,
    relationship_graph,
    drawn_graph,
)
