"""Score an n17 capture pilot against its review's falsifier and the local-radius target.

`devtools.pilot_n17_capture` writes a JSON line to stderr for every certified step and for
every complete round, and with `--output` it rewrites `<output>.partial.json` after every
round with the round summaries in full. This tool reads a run back from those files and
reports, round by round:

* each contracting owner's widest-row-to-extent ratio, or, from the logs alone, only the
  largest of them, which is all the stderr round line carries;
* each position coordinate's two-sided extent and its fall from the start box (round 0);
* the state of the after-pilot review's falsifier, MET, CLEARED or UNDECIDED, with the
  reason in words;
* with a target, each coordinate's remaining contraction factor against its local radius.

For the run it also reports the rows each owner would need to bring its ratio under a
twentieth (and under a tenth), and what a round would cost at that row cap, scaled from
the logs.

The falsifier. Section 5 of
`docs/project/reviews/review-2026-10-02-n17-capture-after-pilot.md`: if, for three
consecutive rounds, every contracting owner's widest live row is under a twentieth of its
position extent and no owner's two-sided position extent falls by ten percent, the
architecture is wrong. The terms are the pilot's, and so are the constants, imported from
it. An owner's ratio is its widest live row, in radians of turn, over its largest
two-sided position extent; a coordinate's two-sided extent is the high side less the low
side of the owner's residual union around the endpoint, slide coordinates left out. A
round is *fine* when every contracting owner's ratio is under `FINE_ROWS`, and *flat* when
no contracting owner's two-sided extent in any position coordinate is below `EXTENT_DROP`
of the previous round's. The states:

* MET: `FALSIFIER_ROUNDS` consecutive complete rounds were fine and flat.
* CLEARED: not met, and positions have started to contract, the review's alternative: the
  worst owner's two-sided position extent fell by a tenth in one round (the pilot's
  `contraction_start`). This is read as of the last round. Three fine and flat rounds
  after it would still meet the falsifier, and MET takes precedence.
* UNDECIDED: neither; the reason names the condition that is missing.

The target. `--target` reads the radius vector of a `check_n17_local_radius` receipt
(`radii`, or `radii_over_floor` times `floor`), such as the L1 composition's
`ratio-composition-1216.json`: 45 coordinates named `xi`, `eta`, `u` and `omega` with the
square's label. The pilot's coordinates map onto them by label: `x` to `xi`, `y` to `eta`,
`u` to `u`, and the owner's turn range to `omega`. The slide coordinates (`a`, `b`, `z`)
and square 6 have no radius. Each coordinate gets two factors: its extent over the
target's extent `2 r`, and its larger side over `r`. Capture must bring the second under
one, since the local theorem takes a coordinate inside `[-r, r]`.

Sources. Logs are read in the order given, as one run. A log that starts at round `R`
supersedes what the earlier logs hold from round `R` on, since a resumed run repeats the
round its predecessor was stopped in, and the steps after the last log's last round line
are a round in progress. Lines that are not JSON are skipped. Per-owner and per-coordinate
figures come from `--rounds`: a partial or final pilot receipt (`rounds` at the top
level), or a checkpoint (`checkpoint-round-NNN.json.gz`). A checkpoint is inflated only up
to the end of its `rounds` member: `write_checkpoint` sorts its keys, so the rows, seed
and steps that make up nearly all of a late checkpoint come after it. A checkpoint whose
members before `rounds`, or whose `rounds` member itself, run past
`CHECKPOINT_PREFIX_LIMIT` characters is refused rather than read. Where a round has both
sources, the logged aggregates are checked against the exact summary and any disagreement
is reported.

Rows needed. Rows are bisected in the half-angle chart `t = tan(turn / 2)`, where a row of
chart width `dt` at `t` turns by about `2 dt / (1 + t^2)`. An owner whose ratio is `q`
needs `h` more levels, the least with `q / 2^h` under the threshold. Three estimates hold
the live measure and the position extent fixed. The continuous one is the rows if each
could be cut to exactly the threshold width. The dyadic one is the live chart width over
the widest row's, times `2^h`: the rows if every live row went down all `h` levels. The
chart count walks the owner's live turn range, placed at its endpoint turn from the pilot,
in the coarsest aligned dyadic rows that pass, and scales by the live share of the range.
Where the range lies in the chart decides how many levels each part needs, which the
widest row alone does not show, so the cap is read from the chart count when there is one.
A run whose rows need more than its cap may still get there as the live ranges narrow, so
each owner's narrowing over the last `NARROWING_ROUNDS` rounds is extrapolated to the round
its rows would fit the most rows any owner has held; that is a trend, not a bound.

Cost. A round's wall time is read from the step lines: the last step's `seconds` less the
previous round's in the same process. Within each log, `wall = c * live^alpha` is fitted
by least squares on logarithms over the complete rounds in the top three octaves of that
log's live rows. The fit over the widest such range scales the latest complete round to a
projected live-row count, either every contracting owner at a uniform cap or each owner at
the rows it needs and no fewer than it has. `--rss-mb` scales a resident size measured at
the latest round in proportion to live rows; that proportion is an assumption, and the
output says so.
"""

from __future__ import annotations

import argparse
import gzip
import itertools
import json
import math
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import IO, Any

from devtools import pilot_n17_capture as pilot

SCHEMA = "n17-capture-score/v1"
CHECKPOINT_PREFIX_LIMIT = 64 * 2**20
CHUNK = 2**20
FIT_OCTAVES = 3
FIT_MIN_RANGE = 2.0
FIT_MIN_ROUNDS = 3
NARROWING_ROUNDS = 3
COORDINATE_NAMES = {"x": "xi", "y": "eta", "u": "u", "turn": "omega"}


# ---------------------------------------------------------------------------
# Reading the logs
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Step:
    """One certified step's progress line."""

    round: int
    step: int
    cell: str
    live_rows: int
    splits: int
    seconds: float
    work: float


@dataclass
class Segment:
    """One log file: its step lines and its round lines by round."""

    path: str
    steps: list[Step] = field(default_factory=list)
    lines: dict[int, dict[str, Any]] = field(default_factory=dict)

    def first_round(self) -> int | None:
        rounds = [step.round for step in self.steps] + list(self.lines)
        return min(rounds, default=None)


@dataclass(frozen=True)
class LogRound:
    """A complete round as the logs show it."""

    round: int
    line: dict[str, Any]
    segment: int
    steps: int
    wall: float
    work: float

    @property
    def live(self) -> int:
        return int(self.line["live"])


@dataclass
class Run:
    """The logs of one run, merged in order."""

    segments: list[dict[str, Any]]
    rounds: dict[int, LogRound]
    in_progress: dict[str, Any] | None
    cap_seen: int
    missing: list[int]


def parse_log(text: str, path: str = "") -> Segment:
    """The step and round lines of one log; anything that is not one is skipped."""
    segment = Segment(path)
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("{"):
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(record, dict) or "round" not in record:
            continue
        if "step" in record:
            segment.steps.append(
                Step(
                    round=int(record["round"]),
                    step=int(record["step"]),
                    cell=str(record["cell"]),
                    live_rows=int(record["live_rows"]),
                    splits=int(record["splits"]),
                    seconds=float(record["seconds"]),
                    work=float(record["producer"]) + float(record["checker"]),
                )
            )
        elif "worst" in record:
            segment.lines[int(record["round"])] = record
    return segment


def round_wall(steps: Sequence[Step], number: int) -> tuple[float, float, int]:
    """Wall seconds, step seconds and step count of one round within one process."""
    own = [step for step in steps if step.round == number]
    before = [step for step in steps if step.round == number - 1]
    start = before[-1].seconds if before else 0.0
    return own[-1].seconds - start, sum(step.work for step in own), len(own)


def merge(segments: Sequence[Segment]) -> Run:
    """One run from logs in order: a later log supersedes earlier ones from its first round."""
    kept: list[Segment] = []
    notes: list[dict[str, Any]] = []
    for segment in segments:
        start = segment.first_round()
        if start is not None:
            for earlier, note in zip(kept, notes, strict=True):
                dropped = [step for step in earlier.steps if step.round >= start]
                lines = sorted(number for number in earlier.lines if number >= start)
                if dropped or lines:
                    note["superseded"] = {
                        "by": segment.path,
                        "from_round": start,
                        "steps": len(dropped),
                        "round_lines": lines,
                    }
                    earlier.steps = [step for step in earlier.steps if step.round < start]
                    for number in lines:
                        del earlier.lines[number]
        kept.append(Segment(segment.path, list(segment.steps), dict(segment.lines)))
        notes.append({"path": segment.path, "superseded": None})
    rounds: dict[int, LogRound] = {}
    for index, segment in enumerate(kept):
        for number, line in sorted(segment.lines.items()):
            wall, work, count = round_wall(segment.steps, number)
            rounds[number] = LogRound(number, line, index, count, wall, work)
        notes[index]["rounds"] = sorted(segment.lines)
    in_progress = None
    if kept:
        last = kept[-1]
        done = max(last.lines, default=-1)
        trailing = [step for step in last.steps if step.round > done]
        if trailing:
            number = trailing[0].round
            own = [step for step in trailing if step.round == number]
            before = [step for step in last.steps if step.round == number - 1]
            start = before[-1].seconds if before else 0.0
            in_progress = {
                "round": number,
                "steps": len(own),
                "cells": [step.cell for step in own],
                "wall_so_far": own[-1].seconds - start,
            }
    numbers = sorted(rounds)
    missing = sorted(set(range(numbers[0], numbers[-1] + 1)) - set(numbers)) if numbers else []
    cap = max((step.live_rows for segment in kept for step in segment.steps), default=0)
    return Run(notes, rounds, in_progress, cap, missing)


def read_logs(paths: Sequence[Path]) -> Run:
    return merge([parse_log(path.read_text(encoding="utf-8"), str(path)) for path in paths])


# ---------------------------------------------------------------------------
# Reading round summaries: receipts, partials and checkpoints
# ---------------------------------------------------------------------------


class _Prefix:
    """A growing window on an inflating text stream, refused past a limit."""

    def __init__(self, stream: IO[str], limit: int) -> None:
        self.stream = stream
        self.limit = limit
        self.text = ""
        self.done = False

    def more(self) -> None:
        if self.done:
            raise ValueError("the checkpoint ends before its rounds member")
        chunk = self.stream.read(CHUNK)
        if not chunk:
            self.done = True
            return
        self.text += chunk
        if len(self.text) > self.limit:
            raise ValueError(
                f"the checkpoint's members before `rounds` exceed {self.limit} characters; "
                "read the run's partial receipt instead"
            )

    def skip(self, index: int) -> int:
        while True:
            while index < len(self.text) and self.text[index] in " \t\r\n":
                index += 1
            if index < len(self.text) or self.done:
                return index
            self.more()

    def char(self, index: int) -> str:
        index = self.skip(index)
        return self.text[index] if index < len(self.text) else ""

    def decode(self, decoder: json.JSONDecoder, index: int) -> tuple[Any, int]:
        """One JSON value from `index`, read further until it provably ends."""
        while True:
            try:
                value, end = decoder.raw_decode(self.text, index)
            except json.JSONDecodeError:
                if self.done:
                    raise
                self.more()
                continue
            # A number at the end of the window may continue past it.
            if end < len(self.text) or self.done:
                return value, end
            self.more()

    def drop(self, index: int) -> int:
        self.text = self.text[index:]
        return 0


def checkpoint_rounds(path: Path, limit: int = CHECKPOINT_PREFIX_LIMIT) -> list[dict[str, Any]]:
    """The `rounds` member of a gzipped pilot checkpoint, inflating nothing after it."""
    decoder = json.JSONDecoder()
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        window = _Prefix(stream, limit)
        index = window.skip(0)
        if window.char(index) != "{":
            raise ValueError(f"{path} is not a JSON object")
        index = window.skip(index) + 1
        while True:
            index = window.skip(index)
            if window.char(index) in {"}", ""}:
                raise ValueError(f"{path} has no rounds member")
            key, index = window.decode(decoder, index)
            index = window.skip(index)
            if window.char(index) != ":":
                raise ValueError(f"{path} is not a checkpoint object")
            index = window.skip(index + 1)
            value, index = window.decode(decoder, index)
            if key == "rounds":
                if not isinstance(value, list):
                    raise ValueError(f"{path}: rounds is not a list")
                return value
            index = window.skip(index)
            if window.char(index) == ",":
                index += 1
            index = window.drop(index)


def load_rounds(paths: Sequence[Path]) -> dict[int, dict[str, Any]]:
    """Round summaries by round from receipts and checkpoints; later files win."""
    rounds: dict[int, dict[str, Any]] = {}
    for path in paths:
        if path.name.endswith(".gz"):
            entries = checkpoint_rounds(path)
        else:
            document = json.loads(path.read_text(encoding="utf-8"))
            entries = document["rounds"]
        for entry in entries:
            rounds[int(entry["round"])] = entry
    return rounds


def read_target(path: Path) -> dict[str, Fraction]:
    """A radius vector from a `check_n17_local_radius` ratio or shape receipt."""
    document = json.loads(path.read_text(encoding="utf-8"))
    if "radii_over_floor" in document:
        base = Fraction(document["floor"])
        return {
            name: base * Fraction(value) for name, value in document["radii_over_floor"].items()
        }
    return {name: Fraction(value) for name, value in document["radii"].items()}


def n17_owners() -> tuple[dict[str, int], dict[str, float]]:
    """Each n17 owner cell's square label and endpoint turn, from the pilot's endpoint."""
    endpoint = pilot.load_endpoint(pilot.capture_frame(None))
    return (
        {target.cell: target.label for target in endpoint.targets},
        {target.cell: target.turn for target in endpoint.targets},
    )


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def _argmax(values: Mapping[str, float]) -> str | None:
    return max(values, key=values.__getitem__) if values else None


def least_fall(entry: Mapping[str, Any]) -> tuple[float | None, str | None]:
    """The least two-sided extent ratio to the previous round, and where it is."""
    best: tuple[float | None, str | None] = (None, None)
    for cell, ratios in entry.get("g_extent", {}).items():
        for key, value in ratios.items():
            if value is not None and (best[0] is None or value < best[0]):
                best = (value, f"{cell} {key}")
    return best


def round_score(
    number: int, logged: LogRound | None, entry: Mapping[str, Any] | None
) -> dict[str, Any]:
    """One round's falsifier inputs, from the exact summary when there is one."""
    score: dict[str, Any] = {"round": number, "source": "rounds" if entry else "log"}
    if logged is not None:
        score |= {
            "live": logged.live,
            "wall_seconds": logged.wall,
            "step_seconds": logged.work,
            "steps": logged.steps,
            "segment": logged.segment,
        }
    if entry is not None:
        ratios: dict[str, float] = entry["row_to_extent"]
        least, where = least_fall(entry)
        score |= {
            "complete": entry.get("complete", True),
            "max_ratio": entry["max_row_to_extent"],
            "binding": _argmax(ratios),
            "under_tenth": sum(1 for value in ratios.values() if value < pilot.MODEL_THRESHOLD),
            "under_twentieth": sum(1 for value in ratios.values() if value < pilot.FINE_ROWS),
            "owners": len(ratios),
            "worst_position_extent": entry["worst_position_extent"],
            "min_g_extent": least,
            "min_g_where": where,
            "fine": bool(entry["rows_fine"]),
            "flat": bool(entry["no_extent_drop"]),
        }
        score.setdefault("live", sum(entry["live_rows"].values()))
        if logged is not None:
            score["disagreements"] = disagreements(logged.line, entry)
        return score
    assert logged is not None
    line = logged.line
    least = line.get("min_g_extent")
    ratio = float(line["row_to_extent"])
    score |= {
        "complete": True,
        "max_ratio": ratio,
        "binding": line.get("binding"),
        "worst_position_extent": float(line["extent"]),
        "min_g_extent": least,
        "min_g_where": None,
        "fine": bool(line["fine"]) if "fine" in line else ratio < pilot.FINE_ROWS,
        "flat": (
            bool(line["flat"])
            if "flat" in line
            else least is not None and least >= pilot.EXTENT_DROP
        ),
    }
    return score


def disagreements(line: Mapping[str, Any], entry: Mapping[str, Any]) -> list[str]:
    """Where a round line differs from the exact summary of the same round."""
    found = []
    if round(entry["max_row_to_extent"], 4) != line["row_to_extent"]:
        found.append(f"ratio {line['row_to_extent']} != {entry['max_row_to_extent']}")
    if line.get("min_g_extent") != entry["min_g_extent"]:
        found.append(f"min g {line.get('min_g_extent')} != {entry['min_g_extent']}")
    if f"{entry['worst_position_extent']:.4e}" != line["extent"]:
        found.append(f"extent {line['extent']} != {entry['worst_position_extent']}")
    if sum(entry["live_rows"].values()) != line["live"]:
        found.append(f"live {line['live']} != {sum(entry['live_rows'].values())}")
    return found


def read_falsifier(scores: list[dict[str, Any]]) -> dict[str, Any]:
    """The review's falsifier over the complete rounds; each score gets its state."""
    run = best = 0
    met: list[int] | None = None
    start: dict[str, Any] | None = None
    previous: dict[str, Any] | None = None
    window: list[int] = []
    complete = [score for score in scores if score.get("complete", True)]
    for score in complete:
        if score["round"] >= 1:
            run = run + 1 if score["fine"] and score["flat"] else 0
            window = [*window, score["round"]][-run:] if run else []
            best = max(best, run)
            if met is None and run >= pilot.FALSIFIER_ROUNDS:
                met = window[-pilot.FALSIFIER_ROUNDS :]
        if (
            start is None
            and previous is not None
            and score["worst_position_extent"]
            <= pilot.EXTENT_DROP * previous["worst_position_extent"]
        ):
            start = {
                "round": score["round"],
                "worst_position_extent_before": previous["worst_position_extent"],
                "worst_position_extent": score["worst_position_extent"],
                "max_ratio_before": previous["max_ratio"],
            }
        score["run"] = run
        score["state"] = "MET" if met else "CLEARED" if start else "UNDECIDED"
        previous = score
    after = [
        score["worst_position_extent"]
        for score in complete
        if start is not None and score["round"] >= start["round"] - 1
    ]
    g_after = [current / before for before, current in itertools.pairwise(after)]
    return {
        "state": "MET" if met else "CLEARED" if start else "UNDECIDED",
        "met_rounds": met,
        "longest_fine_and_flat_run": best,
        "contraction_start": start,
        "g_worst_extent_from_start": g_after,
        "first_round_under_tenth": next(
            (
                score["round"]
                for score in complete
                if score["round"] >= 1 and score["max_ratio"] < pilot.MODEL_THRESHOLD
            ),
            None,
        ),
        "first_round_under_twentieth": next(
            (score["round"] for score in complete if score["round"] >= 1 and score["fine"]),
            None,
        ),
    }


def falsifier_reason(
    reading: Mapping[str, Any],
    scores: Sequence[Mapping[str, Any]],
    needed: Mapping[str, Any] | None,
    cap_seen: int,
) -> str:
    """The falsifier's state in words, citing the numbers that decide it."""
    complete = [
        score for score in scores if score.get("complete", True) and score["round"] >= 1
    ]
    if not complete:
        return "no complete round after the seed: nothing to read"
    last = complete[-1]
    if reading["state"] == "MET":
        rounds = [score for score in complete if score["round"] in reading["met_rounds"]]
        ratio = max(score["max_ratio"] for score in rounds)
        least = min(
            (score["min_g_extent"] for score in rounds if score["min_g_extent"] is not None),
            default=None,
        )
        return (
            f"rounds {rounds[0]['round']}-{rounds[-1]['round']}: every contracting owner's "
            f"widest live row is under 1/20 of its position extent (largest {ratio:.4f}) and "
            f"no two-sided position extent fell below 0.9 of the round before (least "
            f"{_number(least)}): by the review's rule the architecture is wrong"
        )
    if reading["state"] == "CLEARED":
        start = reading["contraction_start"]
        g = start["worst_position_extent"] / start["worst_position_extent_before"]
        return (
            "positions contract: the worst two-sided position extent fell from "
            f"{start['worst_position_extent_before']:.4e} to "
            f"{start['worst_position_extent']:.4e} "
            f"in round {start['round']} (g = {g:.3f}), with the widest-row ratio at "
            f"{start['max_ratio_before']:.4f} the round before"
        )
    if not last["fine"]:
        owner = last.get("binding") or "the binding owner"
        trend = [score["max_ratio"] for score in complete[-3:]]
        own = needed["owners"].get(owner) if needed is not None else None
        # An owner holding more than half the cap can no longer bisect every live row.
        capped = own is not None and 2 * own["live_rows"] > cap_seen
        text = (
            f"ratio {last['max_ratio']:.4f} > 1/20 at {owner} in round {last['round']}: the "
            "falsifier's precondition is not reached" + (" at this row cap" if capped else "")
        )
        if len(trend) > 1:
            text += (
                f" (largest ratio over the last rounds: {', '.join(f'{v:.4f}' for v in trend)})"
            )
        if own is not None:
            text += (
                f"; {owner} holds {own['live_rows']} live rows, the most any owner held is "
                f"{cap_seen}, and it needs {own['halvings_twentieth']} more bisection levels, "
                f"about {own['need_twentieth']} rows, to pass 1/20"
            )
            rate, fit = own.get("narrowing"), own.get("rounds_to_fit_cap")
            if capped and rate is not None:
                text += (
                    f"; its live range narrows to {rate:.3f} a round, at which those rows "
                    + (
                        f"would fit {cap_seen} after about {fit} more rounds"
                        if fit is not None
                        else f"never fit {cap_seen}"
                    )
                )
        return text
    if not last["flat"]:
        where = last.get("min_g_where") or "a coordinate"
        return (
            f"every owner's rows are under 1/20 in round {last['round']}, but {where} fell to "
            f"{_number(last['min_g_extent'])} of the round before, so the round is not flat, "
            "and the worst position extent has not fallen by a tenth"
        )
    return (
        f"fine and flat for {last['run']} consecutive round(s) up to round {last['round']}; "
        f"{pilot.FALSIFIER_ROUNDS} are needed"
    )


def _number(value: float | None) -> str:
    return "none" if value is None else f"{value:.4f}"


# ---------------------------------------------------------------------------
# Coordinates, the target and the rows needed
# ---------------------------------------------------------------------------


def coordinate_table(
    entry: Mapping[str, Any], start: Mapping[str, Any] | None
) -> dict[str, dict[str, dict[str, float | None]]]:
    """Per contracting owner, each position coordinate's sides, extent and fall, and its
    turn range; the fall is the extent over the start round's."""
    table: dict[str, dict[str, dict[str, float | None]]] = {}
    for cell in entry["row_to_extent"]:
        rows: dict[str, dict[str, float | None]] = {}
        for key, extent in entry["extent"][cell].items():
            low, high = entry["range"][cell][key]
            before = start["extent"][cell].get(key) if start is not None else None
            rows[key] = {
                "low": low,
                "high": high,
                "extent": extent,
                "start": before,
                "fall": extent / before if before else None,
                "g": entry["g_extent"][cell].get(key),
            }
        low, high = entry["turn_range"][cell]
        before_turn = None
        if start is not None:
            first, last = start["turn_range"][cell]
            before_turn = last - first
        rows["turn"] = {
            "low": low,
            "high": high,
            "extent": high - low,
            "start": before_turn,
            "fall": (high - low) / before_turn if before_turn else None,
            "g": None,
        }
        table[cell] = rows
    return table


def target_factors(
    table: Mapping[str, Mapping[str, Mapping[str, float | None]]],
    labels: Mapping[str, int],
    radii: Mapping[str, Fraction],
) -> dict[str, Any]:
    """Each coordinate's remaining contraction against its radius `r`: extent over `2 r`
    and the larger side over `r`."""
    rows: list[dict[str, Any]] = []
    for cell, coordinates in table.items():
        label = labels[cell]
        for key, values in coordinates.items():
            if key not in COORDINATE_NAMES:
                continue
            name = f"{COORDINATE_NAMES[key]}{label}"
            if name not in radii:
                continue
            radius = float(radii[name])
            low, high, extent = values["low"], values["high"], values["extent"]
            if low is None or high is None or extent is None:
                continue
            rows.append(
                {
                    "name": name,
                    "cell": cell,
                    "low": low,
                    "high": high,
                    "extent": extent,
                    "radius": str(radii[name]),
                    "extent_factor": extent / (2 * radius),
                    "side_factor": max(abs(low), abs(high)) / radius,
                }
            )
    rows.sort(key=lambda row: -row["side_factor"])
    named = {row["name"] for row in rows}
    return {
        "coordinates": rows,
        "unmatched_radii": sorted(set(radii) - named),
        "inside": sum(1 for row in rows if row["side_factor"] <= 1),
    }


def halvings(ratio: float, threshold: float) -> int | None:
    """Bisection levels until `ratio / 2^h` is under the threshold."""
    if not math.isfinite(ratio):
        return None
    levels = 0
    while ratio / 2**levels >= threshold:
        levels += 1
    return levels


def chart_pieces(turn: float, low: float, high: float) -> list[tuple[float, float]]:
    """The turns `turn + [low, high]` as intervals of `[0, pi/2]`, split where they wrap."""
    first, last = turn + low, turn + high
    if first < 0:
        return [(0.0, last), (pilot.QUARTER + first, pilot.QUARTER)]
    if last > pilot.QUARTER:
        return [(first, pilot.QUARTER), (0.0, last - pilot.QUARTER)]
    return [(first, last)]


def _row_turn(start: float, size: float) -> float:
    return pilot.chart_turn(start + size) - pilot.chart_turn(start)


def chart_rows(pieces: Sequence[tuple[float, float]], width: float) -> int:
    """Rows of a dyadic partition of the half-angle chart over the pieces (turns), each
    the coarsest aligned row whose turn width is under `width`."""
    count = 0
    for first, last in pieces:
        start, end = math.tan(first / 2), math.tan(last / 2)
        size = 1.0
        while _row_turn(start, size) >= width:
            size /= 2
        start = math.floor(start / size) * size
        while start < end:
            size = 1.0
            while start % size or _row_turn(start, size) >= width:
                size /= 2
            count += 1
            start += size
    return count


def rows_needed(
    entry: Mapping[str, Any], turns: Mapping[str, float] | None = None
) -> dict[str, Any]:
    """Each owner's rows for a twentieth and a tenth, at its live measure and extent:
    `rows_*` is the dyadic estimate, `rows_*_continuous` the continuous one, and, with the
    owners' endpoint turns, `rows_*_chart` the chart count (see the module's docstring);
    `need_*` is the chart count when there is one."""
    owners: dict[str, dict[str, Any]] = {}
    for cell, ratio in entry["row_to_extent"].items():
        live = int(entry["live_rows"][cell])
        width = float(entry["live_width"][cell])
        widest = float(entry["widest_live_row"][cell])
        extent = max(entry["extent"][cell].values())
        own: dict[str, Any] = {"live_rows": live, "ratio": ratio}
        pieces = None
        if turns is not None and cell in turns:
            pieces = chart_pieces(turns[cell], *entry["turn_range"][cell])
            span = sum(math.tan(last / 2) - math.tan(first / 2) for first, last in pieces)
            own["live_share"] = min(1.0, width / span) if span > 0 else None
        for suffix, threshold in (
            ("twentieth", pilot.FINE_ROWS),
            ("tenth", pilot.MODEL_THRESHOLD),
        ):
            levels = halvings(ratio, threshold)
            own[f"halvings_{suffix}"] = levels
            own[f"rows_{suffix}_chart"] = None
            if levels is None or widest <= 0:
                own[f"rows_{suffix}"] = None
                own[f"rows_{suffix}_continuous"] = None
                continue
            if levels == 0:
                own[f"rows_{suffix}"] = own[f"rows_{suffix}_continuous"] = live
                own[f"rows_{suffix}_chart"] = live if pieces is not None else None
                continue
            own[f"rows_{suffix}"] = math.ceil(width / widest * 2**levels)
            own[f"rows_{suffix}_continuous"] = math.ceil(width / widest * ratio / threshold)
            if pieces is not None and own["live_share"] is not None:
                rows = chart_rows(pieces, threshold * extent)
                own[f"rows_{suffix}_chart"] = math.ceil(rows * own["live_share"])
        owners[cell] = own
    coarse = sum(int(value) for cell, value in entry["live_rows"].items() if cell not in owners)

    def cap(suffix: str) -> int:
        return max(
            (
                own[f"rows_{suffix}_chart"] or own[f"rows_{suffix}"] or 0
                for own in owners.values()
            ),
            default=0,
        )

    for own in owners.values():
        for suffix in ("twentieth", "tenth"):
            own[f"need_{suffix}"] = own[f"rows_{suffix}_chart"] or own[f"rows_{suffix}"]
    return {
        "round": entry["round"],
        "owners": owners,
        "coarse_live_rows": coarse,
        "cap_twentieth": cap("twentieth"),
        "cap_tenth": cap("tenth"),
    }


# ---------------------------------------------------------------------------
# Cost
# ---------------------------------------------------------------------------


def fit_wall(rounds: Sequence[LogRound]) -> dict[str, Any] | None:
    """`wall = c * live^alpha` over one log's rounds in the top octaves of its live rows."""
    points = [
        (item.live, item.wall, item.round) for item in rounds if item.live > 0 and item.wall > 0
    ]
    if not points:
        return None
    top = max(live for live, _, _ in points)
    used = [point for point in points if point[0] >= top / 2**FIT_OCTAVES]
    span = top / min(live for live, _, _ in used)
    fit: dict[str, Any] = {
        "rounds": [number for _, _, number in used],
        "live_range": [min(live for live, _, _ in used), top],
        "usable": len(used) >= FIT_MIN_ROUNDS and span >= FIT_MIN_RANGE,
        "alpha": None,
    }
    if fit["usable"]:
        xs = [math.log(live) for live, _, _ in used]
        ys = [math.log(wall) for _, wall, _ in used]
        mean_x, mean_y = sum(xs) / len(xs), sum(ys) / len(ys)
        slope = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys, strict=True)) / sum(
            (x - mean_x) ** 2 for x in xs
        )
        fit["alpha"] = slope
    return fit


def cost(
    run: Run,
    needed: Mapping[str, Any] | None,
    caps: Sequence[int],
    rss_mb: float | None,
) -> dict[str, Any]:
    """Per-log fits, and the latest round's wall scaled to projected live-row counts."""
    fits = []
    for index, note in enumerate(run.segments):
        rounds = [item for item in run.rounds.values() if item.segment == index]
        fit = fit_wall(sorted(rounds, key=lambda item: item.round))
        if fit is not None:
            fits.append({"path": note["path"], **fit})
    usable = [fit for fit in fits if fit["usable"]]
    chosen = max(
        usable, key=lambda fit: fit["live_range"][1] / fit["live_range"][0], default=None
    )
    result: dict[str, Any] = {"fits": fits, "alpha_from": None, "projections": []}
    if not run.rounds or chosen is None:
        return result
    reference = run.rounds[max(run.rounds)]
    alpha = float(chosen["alpha"])
    result["alpha_from"] = chosen["path"]
    result["alpha"] = alpha
    result["reference"] = {
        "round": reference.round,
        "live": reference.live,
        "wall_seconds": reference.wall,
        "rss_mb": rss_mb,
    }

    def project(label: str, live: int, fill: int | None) -> dict[str, Any]:
        scale = live / reference.live
        wall = reference.wall * scale**alpha
        return {
            "projection": label,
            "live": live,
            "wall_seconds": wall,
            "rss_mb_if_proportional": None if rss_mb is None else rss_mb * scale,
            "rounds_to_fill": fill,
            "hours_to_fill_and_three": (
                None if fill is None else wall * (fill + pilot.FALSIFIER_ROUNDS) / 3600
            ),
        }

    if needed is None:
        # From the logs alone: one step per contracting owner per round, no coarse rows.
        for cap in sorted(set(caps)):
            result["projections"].append(
                project(f"uniform cap {cap}", reference.steps * cap, None)
            )
        return result
    owners = needed["owners"]
    coarse = needed["coarse_live_rows"]
    for cap in sorted({needed["cap_twentieth"], needed["cap_tenth"], *caps}):
        fill = max(
            (
                _doublings(own["live_rows"], min(own["need_twentieth"] or 0, cap))
                for own in owners.values()
            ),
            default=0,
        )
        result["projections"].append(
            project(f"uniform cap {cap}", len(owners) * cap + coarse, fill)
        )
    for suffix, denominator in (("twentieth", 20), ("tenth", 10)):
        rows = [max(own["live_rows"], own[f"need_{suffix}"] or 0) for own in owners.values()]
        fill = max(
            (
                _doublings(own["live_rows"], own[f"need_{suffix}"] or 0)
                for own in owners.values()
            ),
            default=0,
        )
        result["projections"].append(
            project(f"per-owner rows for 1/{denominator}", sum(rows) + coarse, fill)
        )
    return result


def narrowing(entries: Sequence[Mapping[str, Any]], cell: str) -> float | None:
    """The owner's live chart width, round over round, as a geometric mean over the last
    `NARROWING_ROUNDS` rounds."""
    widths = [
        float(entry["live_width"][cell])
        for entry in entries[-(NARROWING_ROUNDS + 1) :]
        if cell in entry["live_width"]
    ]
    if len(widths) < 2 or widths[0] <= 0:
        return None
    return (widths[-1] / widths[0]) ** (1 / (len(widths) - 1))


def rounds_to_fit(need: int | None, cap: int, rate: float | None) -> int | None:
    """Rounds until `need` rows, shrinking with the live range at `rate`, fit the cap."""
    if need is None or need <= cap:
        return 0
    if rate is None or rate >= 1:
        return None
    return math.ceil(math.log(cap / need) / math.log(rate))


def _doublings(live: int, target: int) -> int:
    """Rounds of bisecting every live row to grow from `live` rows to `target`."""
    return max(0, math.ceil(math.log2(target / live))) if live > 0 and target > live else 0


# ---------------------------------------------------------------------------
# The score
# ---------------------------------------------------------------------------


def score_run(
    run: Run,
    exact: Mapping[int, Mapping[str, Any]],
    *,
    labels: Mapping[str, int] | None = None,
    turns: Mapping[str, float] | None = None,
    radii: Mapping[str, Fraction] | None = None,
    caps: Sequence[int] = (),
    rss_mb: float | None = None,
) -> dict[str, Any]:
    """The whole score: rounds, falsifier, coordinates, target, rows needed and cost."""
    numbers = sorted(set(run.rounds) | set(exact))
    scores = [
        round_score(number, run.rounds.get(number), exact.get(number)) for number in numbers
    ]
    reading = read_falsifier(scores)
    start = exact[min(exact)] if exact else None
    coordinates: dict[str, Any] = {}
    for number in numbers:
        if number in exact:
            coordinates[str(number)] = coordinate_table(exact[number], start)
    scored = max((number for number in numbers if number in exact), default=None)
    needed = rows_needed(exact[scored], turns) if scored is not None else None
    if needed is not None:
        history = [exact[number] for number in sorted(exact) if number <= needed["round"]]
        needed["cap"] = run.cap_seen
        for cell, own in needed["owners"].items():
            own["narrowing"] = narrowing(history, cell)
            own["rounds_to_fit_cap"] = rounds_to_fit(
                own["need_twentieth"], run.cap_seen, own["narrowing"]
            )
            own["rounds_to_fit_cap_tenth"] = rounds_to_fit(
                own["need_tenth"], run.cap_seen, own["narrowing"]
            )
    target = None
    if radii is not None and labels is not None and scored is not None:
        target = {"round": scored, **target_factors(coordinates[str(scored)], labels, radii)}
        for score in scores:
            if str(score["round"]) in coordinates:
                factors = target_factors(coordinates[str(score["round"])], labels, radii)
                worst = factors["coordinates"][0] if factors["coordinates"] else None
                score["inside_target"] = factors["inside"]
                score["worst_side_factor"] = None if worst is None else worst["side_factor"]
                score["worst_side_name"] = None if worst is None else worst["name"]
    reading["reason"] = falsifier_reason(reading, scores, needed, run.cap_seen)
    return {
        "schema": SCHEMA,
        "segments": run.segments,
        "missing_rounds": run.missing,
        "in_progress": run.in_progress,
        "cap_seen": run.cap_seen,
        "start_round": None if start is None else start["round"],
        "rounds": scores,
        "falsifier": reading,
        "ratios": {
            str(number): dict(exact[number]["row_to_extent"])
            for number in numbers
            if number in exact
        },
        "coordinates": coordinates,
        "target": target,
        "rows_needed": needed,
        "cost": cost(run, needed, caps, rss_mb),
    }


# ---------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------


def _cell(value: float | None, digits: int = 3) -> str:
    return "-" if value is None else f"{value:.{digits}g}"


def render(score: Mapping[str, Any]) -> str:
    """The score as plain tables."""
    out: list[str] = []
    say: Callable[[str], None] = out.append
    for note in score["segments"]:
        rounds = note.get("rounds") or []
        span = f"rounds {rounds[0]}-{rounds[-1]}" if rounds else "no complete round"
        say(f"log {note['path']}: {span}")
        if note["superseded"]:
            gone = note["superseded"]
            say(
                f"  superseded from round {gone['from_round']} by {gone['by']}: "
                f"{gone['steps']} steps, round lines {gone['round_lines']}"
            )
    if score["missing_rounds"]:
        say(f"missing rounds: {score['missing_rounds']}")
    if score["in_progress"]:
        going = score["in_progress"]
        say(
            f"round {going['round']} in progress: {going['steps']} steps, "
            f"{going['wall_so_far']:.0f} s so far"
        )
    _render_rounds(score, say)
    _render_ratios(score, say)
    _render_falls(score, say)
    _render_target(score, say)
    _render_needed(score, say)
    _render_cost(score, say)
    reading = score["falsifier"]
    say("")
    say(f"falsifier: {reading['state']}")
    say(f"  {reading['reason']}")
    say(
        f"  first round with every ratio under 1/10: {reading['first_round_under_tenth']}; "
        f"under 1/20: {reading['first_round_under_twentieth']}; "
        f"longest fine and flat run: {reading['longest_fine_and_flat_run']}"
    )
    return "\n".join(out) + "\n"


def _render_rounds(score: Mapping[str, Any], say: Callable[[str], None]) -> None:
    target = score["target"] is not None
    say("")
    say(
        f"{'round':>5} {'live':>5} {'wall s':>7} {'max ratio':>9}  {'binding':<10}"
        f" {'<1/10':>5} {'<1/20':>5} {'worst ext':>9} {'min g':>6}  {'where':<14}"
        f" {'fine':>4} {'flat':>4} {'run':>3}"
        + (f" {'in r':>4} {'side/r':>6}" if target else "")
        + "  state"
    )
    for row in score["rounds"]:
        factors = ""
        if target:
            factors = (
                f" {row.get('inside_target', '-'):>4} {_cell(row.get('worst_side_factor')):>6}"
            )
        say(
            f"{row['round']:>5} {row.get('live', '-'):>5}"
            f" {_cell(row.get('wall_seconds'), 4):>7}"
            f" {row['max_ratio']:>9.4f}  {row.get('binding') or '-':<10}"
            f" {row.get('under_tenth', '-'):>5} {row.get('under_twentieth', '-'):>5}"
            f" {row['worst_position_extent']:>9.3e} {_cell(row['min_g_extent']):>6}"
            f"  {row.get('min_g_where') or '-':<14} {'y' if row['fine'] else 'n':>4}"
            f" {'y' if row['flat'] else 'n':>4} {row.get('run', 0):>3}{factors}"
            f"  {row.get('state', '-')}"
        )
        for problem in row.get("disagreements", []):
            say(f"      log and rounds file disagree: {problem}")


def _render_ratios(score: Mapping[str, Any], say: Callable[[str], None]) -> None:
    ratios: Mapping[str, Mapping[str, float]] = score["ratios"]
    say("")
    if not ratios:
        say("per-owner ratios: the logs carry only the largest; pass --rounds for the rest")
        return
    numbers = sorted(ratios, key=int)
    cells = sorted({cell for row in ratios.values() for cell in row})
    say("widest live row over position extent, per owner (columns are rounds)")
    say(f"{'owner':<11}" + "".join(f"{number:>8}" for number in numbers))
    for cell in cells:
        say(f"{cell:<11}" + "".join(f"{_cell(ratios[n].get(cell)):>8}" for n in numbers))


def _render_falls(score: Mapping[str, Any], say: Callable[[str], None]) -> None:
    coordinates: Mapping[str, Mapping[str, Mapping[str, Mapping[str, float | None]]]] = score[
        "coordinates"
    ]
    if not coordinates:
        return
    numbers = sorted(coordinates, key=int)
    say("")
    say(
        f"two-sided extent over round {score['start_round']}'s, per coordinate "
        "(columns are rounds; turn is the live turn range)"
    )
    say(f"{'owner':<11} {'coord':<5} {'start':>9}" + "".join(f"{n:>8}" for n in numbers))
    last = coordinates[numbers[-1]]
    for cell in sorted(last):
        for key in last[cell]:
            start = last[cell][key]["start"]
            cells = "".join(
                f"{_cell(coordinates[n].get(cell, {}).get(key, {}).get('fall')):>8}"
                for n in numbers
            )
            say(f"{cell:<11} {key:<5} {_cell(start):>9}{cells}")


def _render_target(score: Mapping[str, Any], say: Callable[[str], None]) -> None:
    target = score["target"]
    if target is None:
        return
    say("")
    say(
        f"target at round {target['round']}: {target['inside']} of "
        f"{len(target['coordinates'])} coordinates inside [-r, r]; ext/2r is the extent "
        "over the target's, side/r the larger side over r"
    )
    say(
        f"{'name':<8} {'owner':<11} {'low':>10} {'high':>10} {'r':>10}"
        f" {'ext/2r':>7} {'side/r':>7}"
    )
    for row in target["coordinates"]:
        say(
            f"{row['name']:<8} {row['cell']:<11} {row['low']:>10.3e} {row['high']:>10.3e}"
            f" {float(Fraction(row['radius'])):>10.3e} {row['extent_factor']:>7.3g}"
            f" {row['side_factor']:>7.3g}"
        )
    if target["unmatched_radii"]:
        say(f"radii with no pilot coordinate: {', '.join(target['unmatched_radii'])}")


def _render_needed(score: Mapping[str, Any], say: Callable[[str], None]) -> None:
    needed = score["rows_needed"]
    if needed is None:
        return
    say("")
    say(
        f"rows needed at round {needed['round']}, live measure and extent held fixed: "
        "bisection levels, then rows by the chart, dyadic and continuous estimates"
    )
    say(
        f"{'owner':<11} {'live':>5} {'ratio':>7} {'share':>6}"
        f" | {'1/20':>4} {'chart':>6} {'dyadic':>6} {'cont':>5}"
        f" | {'1/10':>4} {'chart':>6} {'dyadic':>6} {'cont':>5}"
        f" | {'narrow':>6} {'fit':>4} {'1/10':>4}"
    )
    for cell, own in sorted(needed["owners"].items(), key=lambda item: -item[1]["ratio"]):
        say(
            f"{cell:<11} {own['live_rows']:>5} {own['ratio']:>7.4f}"
            f" {_cell(own.get('live_share')):>6}"
            f" | {own['halvings_twentieth']!s:>4} {own['rows_twentieth_chart']!s:>6}"
            f" {own['rows_twentieth']!s:>6} {own['rows_twentieth_continuous']!s:>5}"
            f" | {own['halvings_tenth']!s:>4} {own['rows_tenth_chart']!s:>6}"
            f" {own['rows_tenth']!s:>6} {own['rows_tenth_continuous']!s:>5}"
            f" | {_cell(own.get('narrowing')):>6} {own.get('rounds_to_fit_cap')!s:>4}"
            f" {own.get('rounds_to_fit_cap_tenth')!s:>4}"
        )
    say(
        f"cap for 1/20: {needed['cap_twentieth']}; for 1/10: {needed['cap_tenth']}; "
        f"narrow is the live chart width's ratio a round over the last {NARROWING_ROUNDS}, "
        f"and fit the rounds at that rate until the 1/20 (and 1/10) rows fit "
        f"{needed.get('cap')}"
    )


def _render_cost(score: Mapping[str, Any], say: Callable[[str], None]) -> None:
    result = score["cost"]
    say("")
    say("round wall against live rows, wall = c * live^alpha, per log")
    for fit in result["fits"]:
        say(
            f"  {fit['path']}: rounds {fit['rounds']}, live {fit['live_range']}, "
            f"alpha {_cell(fit['alpha'])}"
            + ("" if fit["usable"] else " (not used: range too narrow)")
        )
    if result["alpha_from"] is None:
        say("  no log spans enough live rows to scale from")
        return
    reference = result["reference"]
    say(
        f"  scaling round {reference['round']} ({reference['live']} live, "
        f"{reference['wall_seconds']:.0f} s) with alpha {result['alpha']:.2f} "
        f"from {result['alpha_from']}"
    )
    for item in result["projections"]:
        rss = item["rss_mb_if_proportional"]
        hours = item["hours_to_fill_and_three"]
        say(
            f"  {item['projection']:<24} live {item['live']:>6}:"
            f" {item['wall_seconds'] / 60:>4.0f} min a round"
            + ("" if rss is None else f", RSS {rss / 1024:.1f} GB if proportional")
            + (
                ""
                if hours is None
                else f"; {item['rounds_to_fill']} rounds to fill, then 3: {hours:.1f} h"
            )
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logs", nargs="+", type=Path, help="pilot stderr logs, in run order")
    parser.add_argument(
        "--rounds",
        type=Path,
        action="append",
        default=[],
        help="a partial or final pilot receipt, or a checkpoint .json.gz (repeatable)",
    )
    parser.add_argument("--target", type=Path, help="a check_n17_local_radius receipt")
    parser.add_argument(
        "--cap", type=int, action="append", default=[], help="also project at this row cap"
    )
    parser.add_argument("--rss-mb", type=float, help="resident size at the latest round")
    parser.add_argument("--json", type=Path, help="write the full score here")
    args = parser.parse_args(argv)
    run = read_logs(args.logs)
    exact = load_rounds(args.rounds)
    radii = None if args.target is None else read_target(args.target)
    labels, turns = n17_owners() if exact else (None, None)
    score = score_run(
        run, exact, labels=labels, turns=turns, radii=radii, caps=args.cap, rss_mb=args.rss_mb
    )
    if args.json is not None:
        args.json.write_text(
            json.dumps(score, indent=1, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(render(score), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
