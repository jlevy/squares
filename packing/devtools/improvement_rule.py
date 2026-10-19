"""The regularization policy's improvement rule: its one statement, and the judgement it
states.

The owner, 13 October 2026: "tie is fine on exactness or regularity as long as it is
making some improvement wrt our regularity or heuristic goals", and "that should be
codified in our regularization standards doc". So the rule is written once, in section 11
of the regularization policy (`POLICY`), between the two markers below, and everything
that applies it reads it from there: question 14 of the policy points to it,
`devtools.regularize_select` prints it in its rule (`regularize_select.rule`), and
`devtools.default_drawings` prints it with its check. Nothing else restates it.

The marked statement is two sentences of rule and a list of its goals, one line each,
`- <goal>: <direction>`. The sentences say what `judge` decides: a view improves on a
drawing when it is worse on none of the goals and better on at least one; ties on the
others are fine, and a tie on every goal is no improvement. They are printed, not parsed.
The goal list is parsed exactly (`stated_goals`) and compared both ways with what the code
judges (`problems`), name by name (`GOAL_NAMES`) and direction by direction
(`DIRECTIONS`): a goal the policy adds that the code does not judge, a goal the code
judges that the policy drops, a line that does not parse, and a direction that differs
from the code's each fail the check. The goals are

- **regularity**, the seven measures (`MEASURES`): five from the house renderer's
  colouring of a drawing (`census_drawing_regularity.regularity`), fewer being better
  (`FEWER_IS_BETTER`, which `compare` reads) -- light, uneven and near-axis squares,
  distinct angle classes and hues -- and the house and stage totals of full shared sides
  (`regularize_evand.contact_partners`), more being better;
- **the side**: a smaller exact side is better and a larger one worse;
- **exactness**: an exactly verified view is better than a numerically checked witness.
  Every view the layer draws is exactly verified, so exactness is never worse.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
POLICY_DOCUMENT = "docs/project/policies/regularization-policy.md"
POLICY = REPO / POLICY_DOCUMENT
#: Where the statement stands, as a link from the repository's root.
SECTION = f"{POLICY_DOCUMENT}#11-the-improvement-rule"
BEGIN = "<!-- BEGIN RULE: improvement (devtools.improvement_rule) -->"
END = "<!-- END RULE: improvement -->"

#: The house renderer's colouring of a drawing, fewer being better.
DRAWING_MEASURES = ("light_axis", "uneven_axis", "near_axis", "classes", "hues")
#: Full shared sides under the house and stage rules, more being better.
CONTACT_MEASURES = ("house_total", "stage_total")
MEASURES = DRAWING_MEASURES + CONTACT_MEASURES
FEWER_IS_BETTER = frozenset(DRAWING_MEASURES)
#: The two goals beside the measures.
SIDE = "side"
EXACTNESS = "exactness"
GOALS = (*MEASURES, SIDE, EXACTNESS)
#: Each goal's name in the policy's list.
GOAL_NAMES = {
    "light_axis": "light squares",
    "uneven_axis": "uneven squares",
    "near_axis": "near-axis squares",
    "classes": "angle classes",
    "hues": "hues",
    "house_total": "house total of full shared sides",
    "stage_total": "stage total of full shared sides",
    SIDE: "exact side",
    EXACTNESS: "exactness",
}
FEWER = "fewer is better"
MORE = "more is better"
SMALLER = "smaller is better"
EXACT = "exactly verified is better than numerically checked"
#: Each goal's direction as the code judges it: the measures' from `FEWER_IS_BETTER`,
#: which `compare` reads, and the side's and exactness's from `judge`.
DIRECTIONS = {
    **{key: FEWER if key in FEWER_IS_BETTER else MORE for key in MEASURES},
    SIDE: SMALLER,
    EXACTNESS: EXACT,
}
_GOAL_LINE = re.compile(r"- (?P<name>[^:]+): (?P<direction>.+)")


def _marked(policy: Path) -> str:
    """The text between the markers, refused unless it is there once and not empty."""
    text = policy.read_text(encoding="utf-8")
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise ValueError(f"{POLICY_DOCUMENT} must state the improvement rule once, marked")
    start, end = text.index(BEGIN) + len(BEGIN), text.index(END)
    if end < start:
        raise ValueError(f"{POLICY_DOCUMENT} closes the improvement rule before opening it")
    marked = text[start:end].strip()
    if not marked:
        raise ValueError(f"{POLICY_DOCUMENT} marks an empty improvement rule")
    return marked


def _parts(policy: Path) -> tuple[str, list[str]]:
    """The marked statement's sentences, on one line, and its goal lines, each joined
    with any lines a formatter wrapped it onto."""
    sentences: list[str] = []
    goals: list[str] = []
    for line in _marked(policy).splitlines():
        if line.startswith("- "):
            goals.append(line.strip())
        elif line.startswith(" ") and goals and line.strip():
            goals[-1] = f"{goals[-1]} {line.strip()}"
        elif line.strip():
            sentences.append(line.strip())
    return " ".join(" ".join(sentences).split()), [" ".join(goal.split()) for goal in goals]


@cache
def statement(policy: Path = POLICY) -> str:
    """The rule as the policy states it, on one line: its sentences, then its goals."""
    sentences, goals = _parts(policy)
    listed = "; ".join(goal.removeprefix("- ") for goal in goals)
    return f"{sentences} The goals: {listed}." if goals else sentences


def stated_goals(policy: Path = POLICY) -> tuple[dict[str, str], list[str]]:
    """The policy's goals, each name with its stated direction, and every goal line that
    does not parse or names a goal twice."""
    found: dict[str, str] = {}
    unread: list[str] = []
    for line in _parts(policy)[1]:
        match = _GOAL_LINE.fullmatch(line)
        if match is None or match["name"] in found:
            unread.append(line)
            continue
        found[match["name"]] = match["direction"].rstrip(".;")
    return found, unread


def problems(policy: Path = POLICY) -> list[str]:
    """Every way the policy's goals and the code's differ: a goal on one side only, a
    direction stated otherwise than the code judges it, or a goal line that does not
    parse."""
    try:
        statement(policy)
        stated, unread = stated_goals(policy)
    except (OSError, ValueError) as error:
        return [str(error)]
    where = f"the improvement rule in {POLICY_DOCUMENT}"
    judged = {GOAL_NAMES[key]: DIRECTIONS[key] for key in GOALS}
    found = [f"{where} has a goal line that does not parse: {line!r}" for line in unread]
    found.extend(
        f"{where} names the goal {name!r}, which the code does not judge"
        for name in stated
        if name not in judged
    )
    found.extend(
        f"{where} does not name the goal {name!r} ({direction})"
        for name, direction in judged.items()
        if name not in stated
    )
    found.extend(
        f"{where} states {name!r} as {stated[name]!r}; the code judges {direction!r}"
        for name, direction in judged.items()
        if name in stated and stated[name] != direction
    )
    if not stated and not unread:
        found.append(f"{where} lists no goals")
    return found


def compare(
    view: Mapping[str, int | None], drawing: Mapping[str, int | None]
) -> tuple[list[str], list[str]]:
    """The measures on which a view is better and worse than a drawing; a measure either
    side lacks is not compared."""
    gains: list[str] = []
    worse: list[str] = []
    for key in MEASURES:
        mine, theirs = view.get(key), drawing.get(key)
        if mine is None or theirs is None or mine == theirs:
            continue
        better = mine < theirs if key in FEWER_IS_BETTER else mine > theirs
        (gains if better else worse).append(key)
    return gains, worse


@dataclass(frozen=True)
class Judgement:
    """A view against a drawing, goal by goal."""

    better: tuple[str, ...]
    worse: tuple[str, ...]

    @property
    def improves(self) -> bool:
        """The rule: worse on no goal and better on one."""
        return bool(self.better) and not self.worse

    @property
    def reason(self) -> str:
        """Why it is no improvement, in words; empty when it is one."""
        if self.worse:
            return f"worse on {', '.join(self.worse)}"
        return "" if self.better else "no gain"


def judge(
    gains: Sequence[str],
    worse: Sequence[str],
    *,
    smaller: bool,
    larger: bool,
    exact_gain: bool,
) -> Judgement:
    """The rule over every goal, from the measures' comparison (`compare`), whether the
    view's exact side is smaller or larger than the drawing's, and whether it replaces a
    numerically checked witness with an exactly verified view."""
    unknown = sorted((set(gains) | set(worse)) - set(MEASURES))
    if unknown:
        raise ValueError(f"not measures of the rule: {unknown}")
    return Judgement(
        better=(*gains, *((SIDE,) if smaller else ()), *((EXACTNESS,) if exact_gain else ())),
        worse=(*worse, *((SIDE,) if larger else ())),
    )
