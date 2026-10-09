"""Check the catalogue Animate view on a built, deployable workbench page.

Animate still runs on the retained controller in `application.js`, driven here through
`window.atlasTransitions`, real keys and a real mouse. Pack and Search have their own
contracts (`check_pack_panel.py`, `check_search_panel.py`); this file holds what is true of
the page's own view, and of the page's global handlers while another panel owns it.

The checks are sections, each a function taking a `Session` and returning the phrase the
summary line reports. A new contract is a new function appended to `SECTIONS`: sections share
one browser page, run in order, and must leave the view paused on the default style.

Every browser assertion is a probe file under `probes/`, loaded by `probes.probe` and given
its values as its one argument; nothing here writes JavaScript.

Usage, from ``packing/``::

    uv run --frozen --all-extras --group dev python -m workbench_tools.check_animate_view
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import os
import tempfile
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image
from playwright.sync_api import Page, sync_playwright

from workbench_tools import animate_view_contract
from workbench_tools.browser_page import open_page
from workbench_tools.build_candidate import CITATIONS, stage_spelling
from workbench_tools.build_site import build
from workbench_tools.probes import probe


@dataclass
class Session:
    """One page, the citation file it was built from, and the failures collected against it."""

    page: Page
    failures: list[str] = field(default_factory=list)
    citations: Path = CITATIONS

    def look(self, name: str, /, **argument: Any) -> Any:
        """Evaluate one probe, with its argument."""
        return self.page.evaluate(probe(name), argument or None)

    def api(self, *calls: tuple[Any, ...]) -> Any:
        """Several calls on the Animate API in one turn; the last one's answer comes back."""
        return self.look("api/apply", calls=[list(call) for call in calls])

    def require(self, condition: bool, message: str) -> None:  # noqa: FBT001 - the assertion
        if not condition:
            self.failures.append(message)

    def enter_animate(self) -> None:
        """Enter Animate by its tab; if a failed section hid the tab, by the API, and say so."""
        tab = self.page.locator("#mode-animate")
        if tab.is_visible():
            tab.click()
        else:
            self.failures.append("the Animate tab is hidden")
            self.api(("setMode", "animate"), ("setCapture", False))
        self.require(self.api(("mode",)) == "animate", "the Animate tab did not enter Animate")


def keyboard_ownership(session: Session) -> str:
    """The page's global shortcuts act only while the Animate view owns the page.

    The page opens on Animate (#171), so from load a shortcut letter is the catalogue's; once
    Pack is chosen it is Pack's business. The same guard behind Search is
    `check_search_panel`'s keyboard case.
    """
    page = session.page
    session.require(
        session.api(("mode",)) == "animate", "the page does not open on the Animate view"
    )
    page.locator("#mode-pack").click()
    page.locator("#pack-count").focus()
    page.locator("#pack-count").blur()
    page.keyboard.press("c")
    owner = session.look("animate/input-owner")
    session.require(
        not owner["capture"] and owner["transport"] == "Play",
        f"a bare `c` acted behind Pack: {owner}",
    )
    return "the page opens on Animate, and shortcuts yield to Pack"


def gap_bar_through_dwell(session: Session) -> str:
    """Through the dwell the bar measures only the squares drawn, against their own record."""
    for n in (17, 26):
        for sample in session.look("animate/gap-through-dwell", n=n):
            label = f"step into {n} at t = {sample['t']:.3f}"
            session.require(
                sample["n"] == n - 1, f"{label}: the bar describes n = {sample['n']}"
            )
            session.require(
                sample["valid"] is True,
                f"{label}: the bar calls n - 1's own record not a packing: {sample}",
            )
            session.require(
                math.isclose(sample["side"], sample["record"], rel_tol=1e-6),
                f"{label}: the side {sample['side']} is not n - 1's record {sample['record']}",
            )
    for n in (17, 26):
        session.api(("pause",), ("setStepN", n), ("seek", 0))
        dwell = session.look("stage/visible-count")
        session.api(("seek", session.api(("duration",))))
        rest = session.look("stage/visible-count")
        session.require(
            (dwell, rest) == (n - 1, n),
            f"step into {n}: the stage draws {dwell} squares in the dwell and {rest} at rest",
        )
    session.api(("seek", 0))
    return "the dwell's bar measures only the squares drawn"


def colours_by_instant(session: Session) -> str:
    """A frame's colours are a function of its instant, not of the seeks before it."""
    for n in (26, 110, 272):
        for walk in (6, 24):
            fills = session.look("animate/seek-fills", n=n, at=0.6, walk=walk)
            direct = fills["direct"]
            for route in ("walked", "again"):
                differ = sum(1 for a, b in zip(direct, fills[route], strict=True) if a != b)
                session.require(
                    len(direct) == n and differ == 0,
                    f"step into {n}: the {route} seek ({walk} steps) paints {differ} of "
                    f"{len(direct)} fills differently from a direct seek to the same instant",
                )
    return "direct, walked and revisited seeks paint alike"


def seeks_anywhere(session: Session) -> str:
    """Every instant of a step can be drawn, the ends included, under every style."""
    swept = session.look(
        "animate/seek-grid",
        ns=[10, 17, 26],
        styles=["tween", "physics", "bodies"],
        levels=[0, 3, 10],
        k=48,
    )
    session.require(
        swept["seeks"] == 3 * 3 * 3 * 49 and not swept["failures"],
        f"{len(swept['failures'])} of {swept['seeks']} seeks threw: {swept['failures'][:4]}",
    )
    return f"{swept['seeks']} seeks drawn"


def seeds(session: Session) -> str:
    """One seed replays, another differs, and a new seed stops a run it would orphan."""
    runs = session.look("animate/seed-poses", n=26, at=0.55, seeds=[7, 8, 7])
    session.require([run["seed"] for run in runs] == [7, 8, 7], f"setSeed did not take: {runs}")
    session.require(runs[0]["poses"] == runs[2]["poses"], "seed 7 does not replay its poses")
    session.require(runs[0]["poses"] != runs[1]["poses"], "seeds 7 and 8 draw the same poses")
    run = session.look("animate/seed-during-run", n=17)
    session.require(
        run["before"]["playing"] and run["before"]["optimizing"],
        f"the hand's run did not start, so the seed check tested nothing: {run}",
    )
    session.require(
        not run["after"]["playing"] and not run["after"]["optimizing"],
        f"a new seed left the page playing with no run behind it: {run['after']}",
    )
    return "seeds replay and a new seed ends the run"


def scope(session: Session) -> str:
    """Pair-moving calls keep the stage inside the range, and a run ends where one starts."""
    steps = session.look(
        "animate/scope",
        calls=[
            ["pause"],
            ["setRange", 17, 17],
            ["goTo", 26],
            ["setRange", 20, 30],
            ["goTo", 99],
            ["seekSequence", 0],
            ["seekSequence", 1e9],
            ["setRange", 17, 17],
            ["grab", 0],
            ["release"],
            ["play"],
            ["playAll"],
            ["stopAll"],
        ],
    )
    for step in steps:
        session.require(
            step["inside"], f"`{step['call']}` left the stage outside the range: {step}"
        )
    one_step = steps[2]
    session.require(
        (one_step["from"], one_step["to"], one_step["n"]) == (27, 27, 27),
        f"goTo on a one-step range did not carry the range with it: {one_step}",
    )
    session.require(
        (steps[4]["n"], steps[5]["n"], steps[6]["n"]) == (30, 20, 30),
        f"goTo and seekSequence did not hold a wide range's ends: {steps[4:7]}",
    )
    session.require(
        steps[10]["optimizing"] and not steps[11]["optimizing"],
        f"playAll ran continuous play on top of the hand's run: {steps[10:12]}",
    )
    return "goTo, seekSequence and playAll keep to the range"


def transport_loop(session: Session) -> str:
    """Play pressed in the frame a step ended starts one loop, not a second."""
    loops = session.look("animate/tick-loops", n=17, frames=30)
    session.require(loops["replayed"], f"the step never ended inside a frame: {loops}")
    session.require(
        loops["ticks"] <= loops["frames"] + 2,
        f"{loops['ticks']} tick requests in {loops['frames']} frames: two loops are running",
    )
    return "one playback loop"


def plays_across_steps(session: Session) -> str:
    """Play carries on from one step into the next, in real time, through the range.

    Every other section seeks, and a seek draws one instant: none of them could see play stop
    at the end of a step, which is how a regression that halted playback after the first step
    reached the owner (2026-09-21). This plays from the grid fill into 6 for 3.5 s and requires
    the stage to have shown at least three n in turn: 5, 6 and 7 on the page as it stands.
    """
    played = session.look("animate/plays-on", **{"from": 6, "to": 10, "seconds": 3.5})
    session.require(not played["errors"], f"a frame threw while playing: {played['errors']}")
    # Stopped after its first step, the stage shows that step's n and n + 1 and nothing more.
    # Carrying on, it shows at least one n past that, each in turn.
    seen = played["seen"]
    session.require(
        len(seen) >= 3 and seen == list(range(seen[0], seen[0] + len(seen))),
        f"play did not carry on from step to step: the stage showed n = {seen}",
    )
    return f"play carried the stage through n = {played['seen'][0]} to {played['seen'][-1]}"


def drag_ends(session: Session) -> str:
    """A key that ends the run mid-drag does not leave the page marked as dragging."""
    page = session.page
    session.look("animate/rest-poses", n=17)
    x, y = session.look("stage/screen-of", index=0)
    page.mouse.move(x, y)
    page.mouse.down()
    page.mouse.move(x + 5, y)
    session.require(
        session.look("animate/hand")["dragging"],
        "a press on a square did not start a drag, so the check tested nothing",
    )
    page.keyboard.press("Home")
    page.mouse.up()
    session.require(
        not session.look("animate/hand")["dragging"],
        "a key that ended the run mid-drag left `body.dragging` behind",
    )
    session.api(("pause",), ("seek", 0))
    return "a drag always ends"


def drag_past_walls(session: Session) -> str:
    """A square dragged past the walls with a real mouse stays under the cursor."""
    page = session.page
    poses = session.look("animate/rest-poses", n=17)
    index = max(range(len(poses)), key=lambda i: poses[i][0])
    x, y = session.look("stage/screen-of", index=index)
    page.mouse.move(x, y)
    page.mouse.down()
    for k in range(1, 11):
        page.mouse.move(x + 15 * k, y)
    for k in range(10):
        page.mouse.move(x + 150 + (1 if k % 2 == 0 else 0), y)
    held = session.look("stage/screen-of", index=index)
    away = math.dist(held, (x + 150, y))
    session.require(
        session.look("animate/hand")["held"] == index,
        f"the drag did not hold square {index}, so the check tested nothing",
    )
    session.require(
        away < 3, f"a square dragged past the wall is {away:.1f} px from the cursor"
    )
    page.mouse.up()
    session.require(
        session.look("animate/hand") == {"held": -1, "dragging": False},
        f"release did not end the drag: {session.look('animate/hand')}",
    )
    session.api(("pause",), ("seek", 0))
    return "a dragged square stays under the cursor"


#: How close an opacity must be to the value it is asserted to have.
OPACITY_TOLERANCE = 1e-6

#: Steps whose facts handover is sampled. The step into 18 keeps `4.59 <= s(1` and the `4.` of
#: its upper bound, and the step into 111 keeps two digits of `s(11`: each holds a digit of a
#: number that changes.
HANDOVER_STEPS = (18, 26, 100, 111)

#: How much of each other two parts' boxes must cover for them to be drawn in the same place.
SAME_PLACE = 0.5

#: What two DIFFERENT strings drawn in the same place may both be seen at, at once.
#:
#: Measured on 2026-09-22 with the citations on: at the midpoint of the step into 18 the panel
#: drew `Guzhou0806 & Mira 2026, GitHub (confirmed,` and `This project 2026, result T-030` at
#: the same x, each at 0.5, and the same for the upper line. Every opacity rule above held --
#: the two sum to one, nothing is blank, the words `lower` and `upper` hold -- because they are
#: about one part at a time, and none of them can see that the two parts are different sentences
#: on top of each other. That is what the owner saw as a flicker (`think-0few`): for the middle
#: of every roll, two citations are legible as neither.
#:
#: So a changed part leaves before its replacement arrives, rather than dissolving through it.
#: Where they are drawn in the same place, the fainter of the two stays under this, which is low
#: enough that a reader sees one sentence and the ghost of another, not two sentences.
SUPERIMPOSED_LIMIT = 0.2


def handover_instants(session: Session, n: int) -> tuple[dict[str, Any], list[float]]:
    """The step's schedule, and instants every 10 ms across its handover, ends included."""
    schedule = session.api(("pause",), ("setStepN", n), ("schedule",))
    arrive, roll, end = schedule["arrive"], schedule["roll"], schedule["end"]
    start = max(0.0, arrive - 0.1)
    count = round((roll + 0.2) / 0.01)
    at = [0.0, *(start + k * 0.01 for k in range(count + 1)), end]
    return schedule, at


#: The shares of the roll over which changed text leaves and arrives, as the page declares them
#: in `TEXT_HANDOVER`. Written here too rather than read from the bundle, so the check states
#: the contract it holds the page to and a change to either side has to be made on purpose.
TEXT_HANDOVER = {"outStart": 0.36, "outEnd": 0.52, "inStart": 0.48, "inEnd": 0.64}

#: How long a slot may be under half ink while its parts trade, in seconds.
#:
#: A slot where every part changes -- the badge row, a citation line -- has nothing holding it
#: up through the handover, so it dips. The rule here used to be that no slot is ever under half
#: ink, which a crossfade satisfies by drawing both the old and the new at once; that is exactly
#: what `SUPERIMPOSED_LIMIT` refuses. Both cannot hold, so this one asks the honest question
#: instead: not whether the panel dips, but for how long. Three frames at 60 is a trade; a fifth
#: of a second is the blink the owner asked us to stop.
BLANK_DIP_SECONDS = 0.07


def require_handover_curves(
    session: Session,
    label: str,
    schedule: dict[str, Any],
    at: list[float],
    *,
    enter: list[float],
    leave: list[float],
) -> None:
    """Changed text leaves over its window and arrives over its own, each whole within the roll.

    The two are no longer one curve and its complement: what leaves goes before what arrives
    comes, so that two different strings in the same place are never both legible
    (`SUPERIMPOSED_LIMIT`). Each is checked on its own window -- settled outside it, partial
    somewhere within -- and the windows are the page's, which is what makes this a contract
    rather than a description.
    """
    arrive, roll = schedule["arrive"], schedule["roll"]
    session.require(
        len(enter) == len(at) and len(leave) == len(at),
        f"{label}: {len(enter)} arriving and {len(leave)} leaving samples of {len(at)}",
    )
    for name, seen, first, last, settled in (
        ("arriving", enter, TEXT_HANDOVER["inStart"], TEXT_HANDOVER["inEnd"], (0.0, 1.0)),
        ("leaving", leave, TEXT_HANDOVER["outStart"], TEXT_HANDOVER["outEnd"], (1.0, 0.0)),
    ):
        lo, hi = arrive + first * roll, arrive + last * roll
        partial = [t for t, v in zip(at, seen, strict=True) if 1e-9 < v < 1 - 1e-9]
        session.require(
            bool(partial) and lo - 0.011 <= min(partial) and max(partial) <= hi + 0.011,
            f"{label}: the {name} text moves over {partial[:1]}..{partial[-1:]}, outside its "
            f"window [{lo:.3f}, {hi:.3f}]",
        )
        for t, v in zip(at, seen, strict=True):
            q = (t - arrive) / roll if roll > 0 else float(t >= arrive)
            if q < first or q > last:
                want = settled[0] if q < first else settled[1]
                session.require(
                    abs(v - want) <= OPACITY_TOLERANCE,
                    f"{label} at t = {t:.3f}: the {name} text is at {v}, not {want}",
                )


def facts_handover(session: Session) -> str:
    """Unchanged text never fades; changed text leaves before its replacement arrives."""
    held_digits = handover(session, HANDOVER_STEPS)
    session.require(
        held_digits > 0,
        "no step held a digit of a number it kept (a KaTeX number is one span unless split)",
    )
    return f"the facts hand over part by part, {held_digits} kept digits held"


def _placed(key: str) -> tuple[str, tuple[float, float, float, float]]:
    """A probe key split into what is drawn and the box it is drawn in.

    The probe writes `<what>@<left>,<top>,<width>,<height>`, the box in half pixels, and `what`
    is `tag:text` for text and the bare markup for an SVG. Split at the LAST `@`, since markup
    may carry one of its own.
    """
    what, _, box = key.rpartition("@")
    left, top, width, height = (float(value) for value in box.split(","))
    return what, (left, top, width, height)


def _same_place(
    one: tuple[float, float, float, float], two: tuple[float, float, float, float]
) -> bool:
    """Whether two boxes cover enough of each other to be read as one place on the panel."""
    (left, top, width, height), (l2, t2, w2, h2) = one, two
    across = min(left + width, l2 + w2) - max(left, l2)
    down = min(top + height, t2 + h2) - max(top, t2)
    if across <= 0 or down <= 0:
        return False
    smaller = min(width * height, w2 * h2)
    return smaller > 0 and (across * down) / smaller >= SAME_PLACE


def _longest_run(instants: list[float], apart: float = 0.011) -> float:
    """The longest stretch of consecutive sampled instants, counting each sample's own 10 ms."""
    longest = 0.0
    start = previous = instants[0]
    for moment in instants[1:]:
        if moment - previous > apart:
            longest = max(longest, previous - start)
            start = moment
        previous = moment
    return max(longest, previous - start) + 0.01


def handover(session: Session, steps: tuple[int, ...], note: str = "") -> int:
    """The facts panel's handover over each step into n, part by part; returns the digits held.

    Every part a slot draws in both layers is held at full ink and swapped at the midpoint;
    every other part leaves over its window and its replacement arrives over its own, and a slot
    is never blank. Two DIFFERENT strings drawn in the same place are never both legible at
    once (`SUPERIMPOSED_LIMIT`). `note` names the setting the steps were run under.
    """
    held_digits = 0
    for n in steps:
        schedule, at = handover_instants(session, n)
        read = session.look("facts/crossfade", n=n, at=at)
        enter, leaving = read["enter"], read["leave"]
        require_handover_curves(
            session, f"facts, step into {n}", schedule, at, enter=enter, leave=leaving
        )
        changed = 0
        for slot in read["slots"]:
            keys_a, keys_b = slot["keys"]
            shared = Counter(keys_a) & Counter(keys_b)
            pairs = []
            for key, times in shared.items():
                ia = [i for i, k in enumerate(keys_a) if k == key]
                ib = [i for i, k in enumerate(keys_b) if k == key]
                pairs.extend(zip(ia[:times], ib[:times], strict=True))
            held_a = {i for i, _ in pairs}
            held_b = {j for _, j in pairs}
            # A digit held although the number it belongs to changed: the `1` of 17 and 18.
            numbers_a, numbers_b = slot["numbers"]
            held_digits += sum(
                1 for i, j in pairs if numbers_a[i] is not None and numbers_a[i] != numbers_b[j]
            )
            going = [i for i in range(len(keys_a)) if i not in held_a]
            coming = [j for j in range(len(keys_b)) if j not in held_b]
            changed += bool(going or coming)
            label = f"step into {n}{note}, slot {slot['name']!r}"
            # The changed parts that a reader would see on top of each other: drawn in the same
            # place and saying different things. Paired here, off the boxes, rather than per
            # instant, since neither what nor where changes across the handover.
            over = [
                (i, j, what_a)
                for i in going
                for j in coming
                for what_a, box_a in [_placed(keys_a[i])]
                for what_b, box_b in [_placed(keys_b[j])]
                if what_a != what_b and _same_place(box_a, box_b)
            ]
            dim: list[float] = []
            for k, (seen_a, seen_b) in enumerate(slot["seen"]):
                t = at[k]
                for i, j in pairs:
                    total = seen_a[i] + seen_b[j]
                    session.require(
                        abs(total - 1) <= OPACITY_TOLERANCE
                        and max(seen_a[i], seen_b[j]) >= 1 - OPACITY_TOLERANCE,
                        f"{label} at t = {t:.3f}: unchanged {keys_a[i]!r} is seen at "
                        f"{seen_a[i]:.3f} + {seen_b[j]:.3f}",
                    )
                for i in going:
                    session.require(
                        abs(seen_a[i] - leaving[k]) <= OPACITY_TOLERANCE,
                        f"{label} at t = {t:.3f}: leaving {keys_a[i]!r} at {seen_a[i]:.3f}, "
                        f"not {leaving[k]:.3f}",
                    )
                for j in coming:
                    session.require(
                        abs(seen_b[j] - enter[k]) <= OPACITY_TOLERANCE,
                        f"{label} at t = {t:.3f}: arriving {keys_b[j]!r} at {seen_b[j]:.3f}, "
                        f"not {enter[k]:.3f}",
                    )
                for i, j, what in over:
                    session.require(
                        min(seen_a[i], seen_b[j]) <= SUPERIMPOSED_LIMIT + OPACITY_TOLERANCE,
                        f"{label} at t = {t:.3f}: {what!r} and what replaces it are drawn in "
                        f"the same place and seen at {seen_a[i]:.3f} and {seen_b[j]:.3f}, so "
                        f"both are legible at once",
                    )
                if keys_a and keys_b and max([*seen_a, *seen_b]) < 0.5 - OPACITY_TOLERANCE:
                    dim.append(t)
            # How long the slot was under half ink, as the longest unbroken run of instants that
            # were: a slot that dips twice is two dips, not one long one. The instants are 10 ms
            # apart, so a run of one covers 10 ms.
            if dim:
                longest = _longest_run(dim)
                session.require(
                    longest <= BLANK_DIP_SECONDS + 1e-9,
                    f"{label}: the slot is under half ink for {longest:.3f} s, longer than "
                    f"the {BLANK_DIP_SECONDS:.3f} s a trade may take",
                )
        session.require(
            changed > 0, f"step into {n}{note} changed no slot, so it tested nothing"
        )
    return held_digits


def citation_file(session: Session) -> tuple[dict[str, Any] | None, str | None]:
    """The citation file's entries by n and its digest, or None and None where it is absent."""
    path = session.citations
    if not path.is_file():
        return None, None
    raw = path.read_bytes()
    entries = json.loads(raw)["citations"]["entries"]
    return {str(entry["n"]): entry for entry in entries}, hashlib.sha256(raw).hexdigest()


def cited_lines(entry: dict[str, Any] | None) -> dict[str, tuple[str, str | None, str | None]]:
    """What the file says an n's section draws: per bound, its reference, the published work
    it corrects where it corrects one, and its note, in the stage's spelling."""
    if entry is None:
        return {}
    return {
        bound: (
            stage_spelling(cited["text"]),
            None
            if cited.get("corrects") is None
            else f"corrects {stage_spelling(cited['corrects']['credit'])}",
            cited["note"],
        )
        for bound in ("lower", "upper")
        if (cited := entry.get(bound)) is not None
    }


def citations_drawn(session: Session) -> str:
    """The CITATION section is drawn exactly where the citation file has a line, at every n.

    With the setting off no n builds any of it. With it on, each n draws its lower bound's
    reference on the first line and its upper bound's on the second, labeled with the bound,
    `reported` exactly where the file says the register has not certified the bound, headed
    only where it draws a line, with the file's frontier record for the n on the head's line,
    and every line inside the column. The file is the one the page
    was built from, by digest; a page built without one draws nothing at any n.
    """
    entries, digest = citation_file(session)
    carried = session.look("page/citations")
    session.require(
        carried["sha256"] == digest,
        f"the page was built from citations {carried['sha256']}, not {session.citations} "
        f"({digest})",
    )
    off = session.look("facts/citation-sweep", on=False)
    built_off = [row["n"] for row in off["drawn"] if row["built"]]
    session.require(
        not built_off, f"with the setting off, n = {built_off[:12]} build citations"
    )
    on = session.look("facts/citation-sweep", on=True)
    column = on["column"]
    wrong: list[str] = []
    drawn_lines = noted = corrected = 0
    for row in on["drawn"]:
        n = row["n"]
        want = cited_lines(None if entries is None else entries.get(str(n)))
        got = {
            line["slot"]: (line["text"], line["corrects"], line["note"])
            for line in row["lines"]
        }
        drawn_lines += len(got)
        noted += sum(1 for _, _, aside in got.values() if aside)
        corrected += sum(1 for _, tag, _ in got.values() if tag)
        if got != want:
            wrong.append(f"n = {n} draws {got}, and the file has {want}")
        if row["built"] != 3:
            wrong.append(f"n = {n} builds {row['built']} citation slots, not the fixed 3")
        if (row["head"] is not None) != bool(want):
            wrong.append(f"n = {n} is {'headed' if row['head'] else 'not headed'} over {want}")
        record = entries[str(n)]["record"] if want and entries is not None else None
        if row["record"] != record:
            wrong.append(f"n = {n} names the record {row['record']}, and the file {record}")
        if row["recordRight"] is not None and row["recordRight"] > column["right"] + 1:
            wrong.append(
                f"n = {n}: the record ends at {row['recordRight']:.1f}, past the column"
            )
        for line in row["lines"]:
            if line["bound"] != line["slot"]:
                wrong.append(f"n = {n}: the {line['slot']} line is labeled {line}")
            if line["left"] < column["left"] - 1 or line["right"] > column["right"] + 1:
                wrong.append(
                    f"n = {n}: the {line['slot']} line {line['text']!r} spans "
                    f"{line['left']:.1f}..{line['right']:.1f}, past the column's "
                    f"{column['left']:.1f}..{column['right']:.1f} by "
                    f"{line['right'] - column['right']:.1f}"
                )
    session.failures.extend(wrong[:12])
    session.require(len(wrong) <= 12, f"and {len(wrong) - 12} more citation findings")
    if entries is None:
        return f"no citation file, and no n of {len(on['drawn'])} draws a citation"
    session.require(drawn_lines > 0, "the citation file cites nothing the page drew")
    return (
        f"the citations are drawn at exactly the file's {drawn_lines} lines over "
        f"{len(on['drawn'])} n, {noted} of them carrying this project's aside and "
        f"{corrected} naming the published work they correct, inside the column, and "
        f"nowhere with the setting off"
    )


def citation_steps(entries: dict[str, Any], last: int) -> tuple[int, ...]:
    """Steps into n where the section changes in each way it can: a reference, a note, a
    bound gaining or losing its line, and the section appearing or going. The first of each."""
    kinds: dict[str, int] = {}
    for n in range(2, last + 1):
        before, after = cited_lines(entries.get(str(n - 1))), cited_lines(entries.get(str(n)))
        for bound in ("lower", "upper"):
            a, b = before.get(bound), after.get(bound)
            if (a is None) != (b is None):
                kinds.setdefault(f"{bound} line", n)
            elif a is not None and b is not None and a[0] != b[0]:
                kinds.setdefault(f"{bound} reference", n)
            elif a is not None and b is not None and a[1] != b[1]:
                kinds.setdefault("note", n)
        if bool(before) != bool(after):
            kinds.setdefault("section", n)
    return tuple(sorted(set(kinds.values())))


def citations_handover(session: Session) -> str:
    """With the citations on, the section hands over between n as the rest of the panel does."""
    entries, _ = citation_file(session)
    if entries is None:
        return "no citation file, so no citation handover to sample"
    last = max(int(pair["n"]) for pair in session.api(("pairs",))) + 1
    steps = citation_steps(entries, last)
    session.require(bool(steps), "the citation file changes the section at no step")
    session.api(("setCitations", True))
    try:
        handover(session, steps, " with citations")
    finally:
        session.api(("setCitations", False), ("pause",), ("seek", 0))
    return f"the citations hand over part by part at the steps into {list(steps)}"


def _near(a: list[float] | None, b: list[float] | None, within: float = 0.5) -> bool:
    return (
        a is not None
        and b is not None
        and all(abs(x - y) <= within for x, y in zip(a, b, strict=True))
    )


def headline_roll(session: Session) -> str:
    """`n =` holds still at full ink while only the number hands over, in place."""
    equals_at: list[float] | None = None
    for n in (10, 100, 101):
        schedule, at = handover_instants(session, n)
        samples = session.look("headline/roll", n=n, at=at)
        require_handover_curves(
            session,
            f"headline, step into {n}",
            schedule,
            at,
            enter=[s["arriving"]["seen"] for s in samples],
            leave=[s["leaving"]["seen"] for s in samples],
        )
        first = samples[0]
        for sample in samples:
            label = f"headline, step into {n} at t = {sample['t']:.3f}"
            still, leaving, arriving = sample["still"], sample["leaving"], sample["arriving"]
            # The two numbers stand in the same place, so one goes before the other comes
            # (`TEXT_HANDOVER`): they used to sum to one, which drew both at once.
            session.require(
                min(leaving["seen"], arriving["seen"])
                <= SUPERIMPOSED_LIMIT + OPACITY_TOLERANCE,
                f"{label}: the numbers are both legible, at "
                f"{leaving['seen']:.3f} and {arriving['seen']:.3f}",
            )
            session.require(
                abs(still["seen"] - 1) <= OPACITY_TOLERANCE
                and still["equalsShown"]
                and not still["digitsShown"],
                f"{label}: the still `n =` is not `n =` alone at full ink: {still}",
            )
            session.require(
                leaving["digitsShown"]
                and arriving["digitsShown"]
                and not leaving["equalsShown"]
                and not arriving["equalsShown"],
                f"{label}: a rolling copy draws `n =` or hides its number: "
                f"{leaving}, {arriving}",
            )
            session.require(
                (leaving["digits"], arriving["digits"]) == (str(n - 1), str(n)),
                f"{label}: the numbers read {leaving['digits']} and {arriving['digits']}",
            )
            equals_at = equals_at or still["equalsAt"]
            session.require(
                _near(still["equalsAt"], equals_at),
                f"{label}: `=` moved from {equals_at} to {still['equalsAt']}",
            )
            session.require(
                _near(leaving["digitsAt"], first["leaving"]["digitsAt"])
                and _near(arriving["digitsAt"], first["arriving"]["digitsAt"])
                and _near(leaving["digitsAt"], still["digitsAt"])
                and _near(arriving["digitsAt"], still["digitsAt"]),
                f"{label}: a rolling number is not where the still copy leaves room for it: "
                f"{leaving['digitsAt']}, {arriving['digitsAt']} against {still['digitsAt']}",
            )
    return "`n =` holds while the number crossfades in place"


#: The elements whose text the stage may draw: the gap bar, the facts panel and its
#: headings,
#: the headline, the composite's legend at the column's foot (the owner, 2026-09-21), and the
#: repository's address in the stage's bottom right (the owner, 2026-09-17). The last two are on
#: the stage in every mode so that a captured frame carries them: both explain the
#: PICTURE, which
#: is why they survive capture preview while everything explaining the page does not.
DRAWN_TEXT_OWNERS = (
    "gapbar",
    "facts",
    "facts-a",
    "facts-b",
    "numeral-static",
    "numeral-a",
    "numeral-b",
    "stage-note",
    "stage-attribution",
    # The shared version on the attribution's line (the owner, 2026-09-22), so every captured
    # frame names the data it was drawn from.
    "stage-version",
)


def stage_says_only_facts(session: Session) -> str:
    """No caption, legend, step header or closed-form line: the stage draws only its facts."""
    states = 0
    style_before = session.api(("state",))["style"]
    for capture in (False, True):
        for style in ("tween", "physics"):
            for n in (17, 110):
                for at in (0.0, 0.5, 1.0):
                    session.api(
                        ("pause",),
                        ("setCapture", capture),
                        ("setStyle", style),
                        ("setStepN", n),
                    )
                    session.api(("seek", session.api(("duration",)) * at))
                    states += 1
                    label = (
                        f"{style} step into {n} at {at:.0%}{' in capture' if capture else ''}"
                    )
                    strays = [
                        d
                        for d in session.look("stage/text-owners")
                        if not str(d["owner"]).startswith(DRAWN_TEXT_OWNERS)
                    ]
                    session.require(
                        not strays, f"{label}: the stage draws other text: {strays[:4]}"
                    )
                    # Three slots a layer at the least -- PROVEN's head, the bound and the
                    # badges -- and two more where anything is open, so n = 16 (nothing open)
                    # beside 17 draws eight.
                    lines = session.look("facts/slot-lines")
                    session.require(
                        len(lines) >= 6 and all(slot["lines"] <= 1 for slot in lines),
                        f"{label}: a facts slot draws more than one line: "
                        f"{[slot for slot in lines if slot['lines'] > 1]}",
                    )
    session.api(("setCapture", False), ("setStyle", style_before), ("seek", 0))
    return f"the stage draws only its facts in {states} states"


def container_ink(session: Session) -> tuple[float, float] | None:
    """The settled box's drawn top and floor, in stage units.

    Read from a capture-mode screenshot of the frame on the stage rather than from element
    boxes,
    because a box is not where the ink is: the SVG's own box carries the view's padding and the
    drawn container ends well above it.

    It used to return the headline's inked rows as well, because the headline hung under the
    packing and two checks measured against them. The headline heads the facts column now, so
    what is left to say about the picture is where its own two edges are.
    """
    page = session.page
    session.look("animate/clear-selection")
    page.wait_for_timeout(300)
    boxes = session.look("layout/stage-boxes")
    left, top, width, _ = boxes["stage"]
    scale = width / 1920
    svg_floor = boxes["svg"][1] + boxes["svg"][3] - top
    image = np.asarray(Image.open(io.BytesIO(page.screenshot())).convert("RGB")).astype(int)
    paper = image[int(top + 1076 * scale), int(left + 1900 * scale)]
    band = image[
        int(top) : int(top + 1080 * scale),
        int(left + PACKING_LEFT * scale) : int(left + PACKING_RIGHT * scale),
    ]
    inked = np.abs(band - paper).sum(axis=2) > 60
    wide = np.where(inked.mean(axis=1) > 0.5)[0]
    wide = wide[wide < svg_floor]
    if wide.size == 0:
        return None
    return float(wide.min() / scale), float((wide.max() + 1) / scale)


def headline_space(session: Session) -> str:
    """The picture is centred in the height it has, at every n.

    This used to measure the headline's ink against the box's floor, because the headline hung
    under the packing. It heads the facts column now (the owner, 2026-09-21) and the box grew
    into the room it left, so what is worth measuring is the room itself: the drawn container
    should sit with the same space above it as below, or the picture is off-centre on the stage
    and every captured frame carries it. `gapbar/clearance` checks where the headline went.
    """
    session.api(("pause",), ("setCapture", True))
    for n in (2, 17, 100):
        session.api(("setStepN", n), ("seek", 0))
        measured = container_ink(session)
        session.require(measured is not None, f"no drawn container to measure at n = {n}")
        if measured is None:
            continue
        ceiling, floor = measured
        above, under = ceiling, 1080 - floor
        session.require(
            abs(above - under) <= CONTAINER_CENTRING,
            f"the picture at n = {n} is not centred in its space: {above:.1f} above its "
            f"drawn top, {under:.1f} below its floor",
        )
    session.api(("setCapture", False), ("seek", 0))
    return "the picture is centred in the height it has"


#: How far from centred the drawn container may sit on the stage, in stage px. Two: the box is
#: drawn on a scale that does not land on whole pixels at every n, and a tolerance tighter than
#: the rounding would fail on arithmetic rather than on layout.
CONTAINER_CENTRING = 2

#: The packing SVG's own left and right edges on the stage, in stage px: the band the
#: container's
#: floor is looked for in. Sampling the whole stage would find the facts column's ink instead.
PACKING_LEFT = 30
PACKING_RIGHT = 1086

#: How far above the stage's own floor the lowest drawn point of a moving frame must stay,
#: in
#: stage px. It used to be measured against the headline's ink, which sat under the
#: packing; with
#: the headline moved to the facts column the floor is the stage's own, and the clearance
#: is what
#: keeps a swinging square from drawing to the very edge of the frame.
STAGE_FLOOR_CLEARANCE = 5


def stage_clearance(session: Session) -> str:
    """What a moving drawing draws stays inside the stage, where it reaches deepest.

    The box grows toward the next record's side and squares tilt, so a moving drawing reaches
    below the settled floor. `stage/lowest-drawn` counts only what the SVG draws, cut at the
    SVG's floor where the SVG clips, because an element's box is not what is drawn: at the
    step into 293 under the bodies style a square's box reads 15 px below a floor that nothing
    is drawn under. The four steps are the corpus's deepest under each physical style.

    The thing being cleared used to be the headline's ink. With the headline at the head of the
    facts column the hazard is the frame's own edge, so that is what this measures.
    """
    style = session.api(("state",))["style"]
    session.api(("pause",), ("setCapture", True), ("setStepN", 17), ("seek", 0))
    limit = 1080 - STAGE_FLOOR_CLEARANCE
    for solver, n in (("physics", 6), ("physics", 5), ("bodies", 293), ("bodies", 302)):
        drawn = session.look("stage/lowest-drawn", n=n, style=solver)
        session.require(
            drawn["deepest"] <= limit,
            f"the drawing reaches {drawn['deepest']:.1f} in the step into n = {n} under "
            f"{solver}, within {STAGE_FLOOR_CLEARANCE} of the stage's floor at 1080 "
            f"(the SVG's floor is {drawn['floor']:.1f}, clipping: {drawn['clips']})",
        )
    session.api(("setCapture", False), ("setStyle", style), ("setStepN", 17), ("seek", 0))
    return f"what a moving drawing draws stays above {limit:.0f}"


def capture_baseline(session: Session) -> str:
    """The capture tools' shared baseline starts from any view and lands on the catalogue."""
    session.page.locator("#mode-pack").click()
    try:
        prepared = session.look(
            "capture/control", prepare=True, capture=False, read=["state", "duration"]
        )
    except Exception as error:  # noqa: BLE001 - the refusal is the finding
        session.failures.append(f"the capture baseline cannot start from Pack: {error}")
        session.enter_animate()
        return "capture baseline refused"
    state = prepared["state"]
    session.require(
        (state["aspect"], state["n"] + 1, state["t"], state["playing"], state["capture"])
        == ("animate", 17, 0, False, False),
        f"the capture baseline is not Animate at the step into 17, paused at 0: {state}",
    )
    session.require(
        session.page.locator("#mode-animate").get_attribute("aria-pressed") == "true",
        "the capture baseline did not show the Animate tab as the page's view",
    )
    return "the capture baseline reaches Animate from Pack"


#: What on the stage is text a pointer could select: the legend's sentence, the headline and
#: the facts column's first rows. A selection in any of them was painted through the animation.
SELECTABLE_LOOKING = ("#stage-note .note-sentence", "#headline", "#gapbar")


def stage_takes_no_selection(session: Session) -> str:
    """A double-click or a drag across the stage's text selects nothing.

    The owner saw the facts' text painted with a grey background through the animation
    (2026-09-21): a click, drag or double-click on the stage left a browser selection, which is
    repainted on every frame after it and is grey while the window is unfocused. The stage is a
    poster and refuses selection, and this makes the gestures that caused it.
    """
    page = session.page
    session.api(("pause",), ("setStepN", 11), ("seek", 0))
    gestures = 0
    for selector in SELECTABLE_LOOKING:
        box = page.locator(selector).first.bounding_box()
        session.require(box is not None, f"{selector} is not drawn to try selecting")
        if box is None:
            continue
        x, y = box["x"] + box["width"] / 3, box["y"] + box["height"] / 2
        page.mouse.dblclick(x, y)
        page.mouse.move(x, y)
        page.mouse.down()
        page.mouse.move(box["x"] + box["width"] * 0.9, y, steps=6)
        page.mouse.up()
        gestures += 2
        selected = session.look("stage/selection", clear=True)
        session.require(
            selected == "",
            f"a double-click and a drag on {selector} selected {selected!r}",
        )
    session.api(("pause",), ("seek", 0))
    return f"{gestures} double-clicks and drags across the stage's text select nothing"


def readouts_claim_only_packings(session: Session) -> str:
    """No readout calls a non-packing valid, on the record, or gives it an excess or a side."""

    def read(label: str, *calls: tuple[Any, ...]) -> dict[str, Any]:
        out = session.look("animate/readouts", calls=[list(call) for call in calls])
        out["label"] = label
        return out

    def require_record(out: dict[str, Any]) -> None:
        session.require(
            out["valid"]
            and out["met"]
            and out["hand"] == 1
            and out["precision"] == "catalogue-precision",
            f"{out['label']}: a retained record drawn as stored is not a packing: {out}",
        )

    def require_refused(out: dict[str, Any], reason: str) -> None:
        session.require(
            not out["valid"]
            and not out["met"]
            and out["excess"] is None
            and out["reason"] == reason
            and out["precision"] == "packing"
            and out["tolerance"] == 1e-9
            and out["hand"] == 0
            and not out["growthPacking"]
            and out["growthExcess"] is None
            and out["runPacking"] is False
            and out["runExcess"] is None,
            f"{out['label']}: a readout claims a packing for {reason}: {out}",
        )

    session.api(("setStyle", "physics"))
    require_record(read("dwell of the step into 16", ("pause",), ("setStepN", 16), ("seek", 0)))
    require_record(read("rest of the step into 16", ("seek", session.api(("duration",)))))
    pair = session.look("animate/touching-pair", n=16)
    session.require(pair is not None, "the record of 16 has no touching pair to press together")
    if pair is None:
        return "no touching pair"
    left, _neighbour = pair
    x, y, _ = session.api(("poseOf", left))
    # 5e-9 of overlap: under the catalogue's stored precision, over the contract's 1e-9.
    pressed = read(
        "a square pressed 5e-9 into its neighbour",
        ("grab", left, x, y),
        ("dragTo", x + 5e-9, y, False),
        ("release",),
    )
    require_refused(pressed, "pair-overlap")
    shrunk = read(
        "the hand's run at half size",
        ("dragTo", x, y, False),
        ("setGrowth", {"on": True, "size": 0.5}),
    )
    require_refused(shrunk, "unit-size")
    session.require(
        shrunk["growInfo"].endswith("not a packing"),
        f"the growth readout compares a non-packing with the record: {shrunk['growInfo']!r}",
    )
    session.api(
        ("setGrowth", {"on": False, "size": 1}),
        ("setStyle", "tween"),
        ("pause",),
        ("seek", 0),
    )
    return "no readout claims a packing for a 5e-9 overlap or half-size squares"


SECTIONS: tuple[Callable[[Session], str], ...] = (
    keyboard_ownership,
    gap_bar_through_dwell,
    colours_by_instant,
    seeks_anywhere,
    seeds,
    scope,
    transport_loop,
    plays_across_steps,
    drag_ends,
    drag_past_walls,
    facts_handover,
    citations_drawn,
    citations_handover,
    headline_roll,
    headline_space,
    stage_clearance,
    stage_says_only_facts,
    stage_takes_no_selection,
    readouts_claim_only_packings,
    *animate_view_contract.SECTIONS,
    capture_baseline,
)


def check(page_path: Path, citations: Path = CITATIONS) -> str:
    """Run every section against one page; raise with every failure if any section failed.

    `citations` is the file the page was built from, which the citation sections hold what it
    draws to.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True, executable_path=os.environ.get("SQUARES_BROWSER_EXECUTABLE")
        )
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        session = Session(page, citations=citations)
        page.on("pageerror", lambda error: session.failures.append(f"pageerror: {error}"))
        page.on(
            "console",
            lambda event: (
                session.failures.append(f"console.{event.type}: {event.text}")
                if event.type == "error"
                else None
            ),
        )
        open_page(page, page_path)
        page.wait_for_timeout(500)
        done = []
        for section in SECTIONS:
            if section is not keyboard_ownership and session.api(("mode",)) != "animate":
                session.enter_animate()
            try:
                done.append(section(session))
            except Exception as error:  # noqa: BLE001 - one broken section must not hide the rest
                session.failures.append(f"{section.__name__} stopped: {error}")
        browser.close()
    if session.failures:
        raise ValueError("Animate view:\n  " + "\n  ".join(session.failures))
    return "; ".join(done)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page", type=Path)
    parser.add_argument(
        "--citations",
        type=Path,
        default=CITATIONS,
        help="the citation file the page is built from",
    )
    options = parser.parse_args()
    if options.page is None:
        with tempfile.TemporaryDirectory(prefix="squares-animate-view-") as directory:
            page = Path(directory) / "index.html"
            build(page.parent, citations=options.citations)
            result = check(page, options.citations)
    else:
        result = check(options.page, options.citations)
    print(f"OK: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
