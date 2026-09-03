#!/usr/bin/env python3
"""One place that knows how a result's significance is read and ranked.

`results.yaml` is the record, `epistemics.md` owns the vocabulary, and
`devtools/check_results.py` grants the rungs. Two surfaces now display them --
the synopsis headline block and the pull-request description -- and before this
module existed neither did. Agenda 016 registered `T-014`, `T-015` and `T-016`,
scored all three at `S3`, rendered them into `RESULTS.md`, and then published a
synopsis whose first mention of a significance score was 400 lines in and a
pull request that carried no score for two of the three at all. The record was
complete and the presentation was not, which is the failure this module is here
to make structurally impossible: both surfaces read their rows and their rubric
wording from here, so a result cannot be registered and go unpresented.

The anchors are parsed from `epistemics.md` rather than copied, because a rubric
restated in code is a rubric that drifts from the policy it claims to quote --
the same shape as `D-010`, `D-017` and `D-022`, three hand-maintained views that
drifted from their sources in one week.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
#: The reader-facing policy lives at the repository root, not under `packing/`.
REPO = ROOT.parent
RESULTS = ROOT / "frontier" / "results.yaml"
EPISTEMICS = REPO / "epistemics.md"

#: `| `S3` | A substantive case result or machine audit |`, the rubric's own row shape.
_ANCHOR_ROW = re.compile(r"^\|\s*`S(\d)`\s*\|\s*(.+?)\s*\|\s*$", re.MULTILINE)


def anchors() -> dict[int, str]:
    """The significance rubric, read from `epistemics.md` at the moment of use."""
    text = EPISTEMICS.read_text(encoding="utf-8")
    found = {int(score): anchor for score, anchor in _ANCHOR_ROW.findall(text)}
    if not found:
        raise SystemExit(f"{EPISTEMICS}: no significance anchors found; the rubric moved")
    return found


def anchor_for(score: int) -> str:
    """The rubric's own words for one score, or a refusal naming the gap."""
    found = anchors()
    if score not in found:
        raise SystemExit(f"epistemics.md defines no anchor for S{score}")
    return found[score]


def load() -> list[dict]:
    """Every registered result, as recorded."""
    return safe_load(RESULTS.read_text(encoding="utf-8"))["results"]


def scope_label(record: dict) -> str:
    """The `n` a result speaks about, in the register's own two shapes."""
    scope = record["scope"]
    if "n_values" in scope:
        return ", ".join(str(n) for n in scope["n_values"])
    return f"{scope['n_min']}-{scope['n_max']}"


def by_significance(results: list[dict]) -> list[dict]:
    """Significance descending, then confirmation, then id.

    The same order `RESULTS.md` uses. Reading order is the whole purpose of the
    score, so the two prioritized surfaces must not disagree about it.
    """
    return sorted(
        results,
        key=lambda record: (
            -record["significance"]["score"],
            -int(record["confirmation"][1:]),
            record["id"],
        ),
    )


def scored_within(results: list[dict], start: date, end: date) -> list[dict]:
    """Results whose current significance assessment was made in `[start, end]`.

    `scored` dates the assessment rather than the registration, which is the
    field that answers "what did this run establish": a result re-scored inside
    the window is news to the reader even when its id is older, and one
    registered earlier and untouched is not.
    """
    inside = []
    for record in results:
        scored = record["significance"].get("scored")
        if scored is None:
            continue
        when = scored if isinstance(scored, date) else date.fromisoformat(str(scored))
        if start <= when <= end:
            inside.append(record)
    return by_significance(inside)


def headline(record: dict) -> str:
    """The first sentence of a claim, for a table cell that must stay one line."""
    claim = " ".join(record["claim"].split())
    sentence, _, _ = claim.partition(". ")
    return sentence.rstrip(".") + "."
