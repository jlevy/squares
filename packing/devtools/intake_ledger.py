"""Evaluate every reported upper bound per count, in the order the reports arrived.

The owner's rule (2026-10-14): reports of ``s(n) <= v`` are taken per count ``n`` in the
order they reached this repository, and each one is recorded as a result while it is
stronger than the last; one that is not stronger than an earlier report is not recorded,
unless the owner names a key reason it should be. This module applies that rule to an
intake directory such as ``campaign/issue-intake/upper-bounds-20261014/``:

- **the start.** At ``n <= 324`` the standing side starts at the case record's reported
  upper bound on the tree (``packing/frontier/n-NNN.md``): its ``exact_form`` where that
  is a rational, else its ``value`` as a printed side within one unit of its last place.
  A register entry pending adoption that states a smaller upper bound
  (``check_standing.improvements``) lowers it. Above the horizon the start is the current
  beyond-horizon row of ``frontier/source-coverage.yaml``, else the grid ``ceil(sqrt n)``;
- **the walk.** The claims at ``n`` are sorted by ``reported_at`` (issue, comment or pull
  request creation; a claim added later by an edit or a commit carries its own time; a
  publication in a watched repository is dated by its first commit). A claim is
  *recorded* when every number it may be is below every number the standing side may be
  (`upper_bound_reports.below`), and it becomes the standing side; one equal to it (a
  tie) or above it is *not recorded*, and the verdict names what holds the count; one
  that print precision cannot order is *undecided*, never guessed, and stays beside the
  standing side until something decidably below both arrives;
- **exceptions** come only from the input's ``exceptions`` list, each with a count, a
  report and the owner's reason; such a claim is shown as recorded by exception and
  moves nothing;
- **owner decisions** the render lists without deciding: exact ties between different
  holders, a not-recorded claim whose certificate was first committed before the report
  that holds the count, every undecided comparison with what would decide it, claims
  whose time is unknown (kept out of the walk), and every count where a verdict changes
  when publications in watched repositories are not counted as reports.

Printed sides carry a rounding (`ROUNDINGS`), ``u`` being one unit in the last printed
place: ``up`` lies in ``(p - u, p]``; ``nearest`` within ``u/2`` of ``p`` and ``unstated``
within ``u``; ``binary64``, a double printed at more places than it determines, within one
ulp of ``float(p)`` plus ``u``, as the lanes read #593's 16-place prints; ``cut`` (decimals
followed by an ellipsis) in ``[p, p + u)``; and ``exact`` is the number printed. A
claim's ``exact`` side, where a lane's frozen claim record or the certificate itself
states it, replaces the print in every comparison. A claim's ``record_relations``, each
an exact comparison with a case lane or a pending register entry that a lane's claim
record or a decision's receipt states (`RecordRelation`), decide those comparisons while
the record still prints what they read. ``restates`` says, for the README,
that a claim's certificate is another holder's packing; it changes no verdict. A
recorded claim is classified only where a source says what it is: ``refines`` (the same
configuration with a tighter certificate, naming the packing's finder and the entry that
holds it, which the register credits as a regularization) or ``new_packing`` (with
``continues`` where a continued search started from another arrangement); the render
lists every count where two or more refinements of one packing are each recorded.

The directory holds ``sources.yaml`` (what ``gather`` reads: the reports, their GitHub
coordinates, the lane claim records, and the printed sides transcribed from the reports),
``github-issues.json`` (the GitHub snapshot), ``ledger.yaml`` (the input of the rule) and
the rendered ``ledger.json`` and ``README.md``.

From ``packing/``, with the project interpreter::

    python -m devtools.intake_ledger gather [DIR] [--snapshot] [--refresh-starts]
    python -m devtools.intake_ledger render [DIR] [--write | --check]
    python -m devtools.intake_ledger check [DIR] [--tree]

``gather`` reads GitHub through ``gh`` (``--snapshot`` reuses ``github-issues.json``) and
each lane's claim record by path: the packet's ``acquisition/`` record where the checkout
holds it, else the copy retained under ``lane-claims/<lane>/<packet>/`` in the intake
directory, whose README gives each copy's branch, commit and path. A lane's commit is
provenance only; nothing reads it. ``gather`` may need the network and runs in no
validation tier. It keeps a ``starts.yaml`` already frozen at ``read_at_main`` and reads
the starts from the checkout only when there is none or ``--refresh-starts`` asks, which
is run from a checkout of ``read_at_main`` (``check --tree`` reports where the checkout's
records give other starts). ``render`` and ``check`` are offline. Both refuse a
``starts.yaml`` member whose span its stored lanes, stated bound or print do not give, so
a start edited by hand fails, and a record relation that reads no member of its count's
start, since it would decide nothing; ``render --check`` also fails when either rendered
file would change.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any, NotRequired, TypedDict, TypeIs, cast

import mpmath as mp
import yaml
from mpmath.libmp import to_rational
from strif import atomic_output_file

from devtools import check_source_coverage as coverage_check
from devtools import check_standing
from devtools import render_recent_results as view
from devtools.upper_bound_reports import Span, below, exact_span, grid_side, printed_span
from sqpack.retained_json import dumps as retained_dumps
from sqpack.yamlio import safe_load

MODULE = "devtools.intake_ledger"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FRONTIER = ROOT / "frontier"
DEFAULT_DIRECTORY = ROOT / "campaign/issue-intake/upper-bounds-20261014"
SOURCES = "sources.yaml"
SNAPSHOT = "github-issues.json"
LEDGER = "ledger.yaml"
STARTS = "starts.yaml"
#: Where the lanes' claim records the checkout does not hold are retained (`lane_record`).
LANE_CLAIMS = "lane-claims"
VERDICTS = "ledger.json"
README = "README.md"
LEDGER_FORMAT = "intake-ledger-v1"
SOURCES_FORMAT = "intake-ledger-sources-v1"
SNAPSHOT_FORMAT = "intake-ledger-github-v1"
VERDICTS_FORMAT = "intake-ledger-verdicts-v1"
STARTS_FORMAT = "intake-ledger-starts-v2"
GITHUB_REPOSITORY = "jlevy/squares"
#: The case corpus is ``n = 1..324``; above it the start is a beyond-horizon row or the grid.
HORIZON = 324
#: How a printed side was rounded; see the module docstring.
ROUNDINGS = ("up", "binary64", "nearest", "unstated", "cut", "exact")
KINDS = ("issue", "comment", "pull-request", "publication")
UNKNOWN = "unknown"
RECORDED = "recorded"
NOT_RECORDED = "not recorded"
UNDECIDED = "undecided"
BY_EXCEPTION = "recorded by exception"
#: What a recorded claim's certificate is, where a source says: a refinement of a standing
#: packing, a new packing, or neither stated (`Refines`, `NewPacking`).
REFINEMENT, NEW, UNCLASSIFIED = "refinement", "new packing", "unclassified"
BELOW, ABOVE, EQUAL = "below", "above", "equal"
SHOWN_PLACES = 12
#: The common-doc footer every durable document carries (`check_documentation`).
FOOTER = (
    "<!-- This document follows common-doc-guidelines.md.",
    "See github.com/jlevy/practical-prose and review guidelines before editing.",
    "-->",
)
_UTC = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ")
_DATE = re.compile(r"\d{4}-\d\d-\d\d")
_COMMIT = re.compile(r"[0-9a-f]{40}")
_DECIMAL = re.compile(r"[0-9]+(?:\.[0-9]+)?")
_FRACTION = re.compile(r"[0-9]+/[1-9][0-9]*")
_BEAD = re.compile(r"think-[a-z0-9]{4}")
_ENTRY = re.compile(r"T-\d+")
_MARGIN = re.compile(r"-?[0-9]+(?:\.[0-9]+)?(?:e[-+]?[0-9]+)?")
_MARGIN_SIGN = {BELOW: -1, EQUAL: 0, ABOVE: 1}


class LedgerError(ValueError):
    """Refuse a malformed ledger, a claim outside its own print, or an unknown reference."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise LedgerError(message)


# --------------------------------------------------------------------------- the input


class RecordRelation(TypedDict):
    """An exact comparison of a claim's side with one case lane, as a lane's claim record
    or a decision's receipt states it, or with a register entry pending adoption.

    ``relation`` holds only while that lane still prints ``value`` and ``exact_form``, or,
    where ``lane`` names a register entry (``T-NNN``), while the entry states ``value``
    (`pending_member`; ``exact_form`` is then empty). ``margin``, where the decision gives
    it, is the claim's side minus the other's, and the render shows it as the difference.
    """

    lane: str
    relation: str
    value: str
    exact_form: str
    read_from: str
    margin: NotRequired[str]


class Refines(TypedDict):
    """Whose packing a claim's certificate tightens, as a source states it.

    A refinement is the same configuration with a tighter certificate: a padding
    reduction, an exact-contact refinement, an exact attainment. ``entry`` is the register
    entry or the report that holds the packing; ``source`` is where this is stated.
    """

    packing_of: str
    entry: str
    source: str


class NewPacking(TypedDict):
    """A claim its source states is a new packing, not a tighter certificate of one.

    ``continues`` names the arrangement a continued search started from, where the
    source says the packing continues one.
    """

    source: str
    continues: NotRequired[str]


class Measured(TypedDict):
    """A geometric measurement of a claim's certificate against another packing.

    It is recorded beside the source's word and decides nothing.
    """

    against: str
    finding: str
    source: str


class Claim(TypedDict):
    """One ``s(n) <= v`` a report states; see the module docstring for the fields."""

    n: int
    printed: str
    rounding: str
    exact: NotRequired[str]
    exact_from: NotRequired[str]
    first_committed: NotRequired[str]
    reported_at: NotRequired[str]
    record_relations: NotRequired[list[RecordRelation]]
    measured: NotRequired[Measured]
    restates: NotRequired[str]
    refines: NotRequired[Refines]
    new_packing: NotRequired[NewPacking]
    note: NotRequired[str]


class Lane(TypedDict):
    """A lane's branch and the commit its frozen claim records were taken at, as
    provenance: the records are read by path (`lane_record`), never at the commit."""

    name: str
    branch: str
    commit: str
    note: NotRequired[str]


class Report(TypedDict):
    """One report: an issue, a comment, a pull request, or a watched-repository publication."""

    report: str
    url: str
    kind: str
    holders: str
    reported_at: str
    bead: str
    claims: list[Claim]
    note: NotRequired[str]


class OwnerException(TypedDict):
    """The owner's key reason to record a claim the rule does not record."""

    n: int
    report: str
    reason: str


class OtherItem(TypedDict):
    """An intake item that states no new upper bound, with its bead's disposition."""

    issue: str
    url: str
    holders: str
    kind: str
    bead: str
    disposition: str


class KeyReason(TypedDict):
    """A claim someone argues has a key reason to be recorded, which the rule does not
    apply: the render shows it beside the rule's verdict and among the owner's decisions."""

    n: int
    report: str
    argument: str
    proposed_as: NotRequired[str]


class Ledger(TypedDict):
    format: str
    read_at_main: str
    read_on: str
    rule: str
    lanes: list[Lane]
    reports: list[Report]
    exceptions: list[OwnerException]
    key_reason_candidates: NotRequired[list[KeyReason]]
    cross_check: NotRequired[list[str]]
    other_items: list[OtherItem]


def _is_count(value: object) -> TypeIs[int]:
    """A positive integer count; a bool is not one."""
    return isinstance(value, int) and not isinstance(value, bool) and value >= 1


def number(text: str) -> Fraction:
    """A decimal, an integer or a fraction ``p/q``, exactly."""
    _require(_DECIMAL.fullmatch(text) or _FRACTION.fullmatch(text), f"not a number: {text!r}")
    return Fraction(text) if "/" in text else Fraction(Decimal(text))


def unit(printed: str) -> Fraction:
    """One unit in the last printed place."""
    return Fraction(1, 10 ** len(printed.partition(".")[2]))


def printed_side(printed: str, rounding: str) -> Span:
    """The numbers a printed side may be, by its rounding (`ROUNDINGS`)."""
    _require(rounding in ROUNDINGS, f"unknown rounding {rounding!r}")
    if rounding == "exact":
        return exact_span(number(printed))
    _require(_DECIMAL.fullmatch(printed) and "." in printed, f"not a decimal: {printed!r}")
    if rounding == "up":
        return printed_span(printed, "up")
    if rounding == "cut":
        value = number(printed)
        return Span(value, value + unit(printed), open_low=False, open_high=True)
    if rounding == "binary64":
        # The double nearest the side, rendered at more places than a double of that size
        # determines: the side lies within one ulp of the double plus one printed unit, as
        # the lanes read #593's 16-place prints (an exact side lies 1.2e-15 from them).
        value = number(printed)
        slack = Fraction(math.ulp(float(value))) + unit(printed)
        return Span(value - slack, value + slack, open_low=False, open_high=False)
    if rounding == "nearest":
        value, half = number(printed), unit(printed) / 2
        return Span(value - half, value + half, open_low=False, open_high=False)
    return printed_span(printed, "unstated")


def contains(span: Span, value: Fraction) -> bool:
    """Whether ``value`` is one of the numbers ``span`` may be."""
    above_low = value > span.low or (value == span.low and not span.open_low)
    below_high = value < span.high or (value == span.high and not span.open_high)
    return above_low and below_high


def claim_span(claim: Claim) -> Span:
    """The exact side where one is known, else the print."""
    if "exact" in claim:
        return exact_span(number(claim["exact"]))
    return printed_side(claim["printed"], claim["rounding"])


def load_yaml(path: Path) -> Any:
    return safe_load(path.read_text(encoding="utf-8"))


#: The top-level keys every ledger states (`Ledger`), and the fields every report does.
LEDGER_KEYS = (
    "format",
    "read_at_main",
    "read_on",
    "rule",
    "lanes",
    "reports",
    "exceptions",
    "other_items",
)
REPORT_KEYS = ("report", "url", "kind", "holders", "reported_at", "bead")
#: The parts of a claim that are themselves mappings, and the fields each must name.
CLAIM_PARTS: Mapping[str, tuple[str, ...]] = {
    "refines": ("packing_of", "entry", "source"),
    "new_packing": ("source",),
    "measured": ("against", "finding", "source"),
}


def _problems_of_claim(where: str, claim: Mapping[str, Any], reported_at: str) -> list[str]:
    problems: list[str] = []
    allowed = set(Claim.__annotations__)
    if set(claim) - allowed:
        problems.append(f"{where}: unknown fields {sorted(set(claim) - allowed)}")
    if not _is_count(claim.get("n")):
        return [*problems, f"{where}: n is not a positive count"]
    try:
        span = printed_side(str(claim.get("printed")), str(claim.get("rounding")))
    except LedgerError as error:
        return [*problems, f"{where}: {error}"]
    if "exact" in claim:
        try:
            exact = number(str(claim["exact"]))
        except LedgerError as error:
            return [*problems, f"{where}: {error}"]
        if not contains(span, exact):
            problems.append(
                f"{where}: the exact side {claim['exact']} lies outside its own print "
                f"{claim['printed']} ({claim['rounding']})"
            )
    problems.extend(
        f"{where}: {key} is not a UTC time"
        for key in ("first_committed", "reported_at")
        if key in claim and not _UTC.fullmatch(str(claim[key]))
    )
    own = str(claim.get("reported_at") or "")
    if own and reported_at != UNKNOWN and _UTC.fullmatch(own) and own < reported_at:
        problems.append(f"{where}: a claim cannot arrive before its report")
    problems.extend(
        f"{where}: {key} is not a string"
        for key in ("restates", "note", "exact_from")
        if key in claim and not isinstance(claim[key], str)
    )
    parts = {key: claim.get(key) for key in CLAIM_PARTS if claim.get(key) is not None}
    for key, part in parts.items():
        if not isinstance(part, Mapping):
            problems.append(f"{where}: {key} is not a mapping")
        elif not all(str(part.get(name) or "").strip() for name in CLAIM_PARTS[key]):
            problems.append(f"{where}: {key} names {', '.join(CLAIM_PARTS[key])}")
    if "refines" in parts and "new_packing" in parts:
        problems.append(f"{where}: a claim is a refinement or a new packing, not both")
    relations = claim.get("record_relations") or []
    if not isinstance(relations, list):
        return [*problems, f"{where}: record_relations is not a list"]
    read: set[tuple[str, str, str]] = set()
    for relation in relations:
        if not isinstance(relation, Mapping):
            problems.append(f"{where}: a record relation is not a mapping")
            continue
        problems.extend(f"{where}: {problem}" for problem in _relation_problems(relation))
        lane, value = str(relation.get("lane")), str(relation.get("value"))
        key = (lane, value, str(relation.get("exact_form")))
        if key in read:
            problems.append(f"{where}: two record relations read {lane} at {value}")
        read.add(key)
    return problems


def _relation_problems(relation: Mapping[str, Any]) -> list[str]:
    """Every way one record relation breaks its contract (`RecordRelation`)."""
    problems: list[str] = []
    if relation.get("relation") not in (BELOW, ABOVE, EQUAL):
        problems.append("a record relation is below, above or equal")
    lane = str(relation.get("lane"))
    if lane not in ("reported", "verified") and not _ENTRY.fullmatch(lane):
        problems.append(
            "a record relation names the reported or verified lane or a register entry"
        )
    if not all(isinstance(relation.get(key), str) for key in ("value", "exact_form")):
        problems.append("a record relation states the value and form it read")
    if "margin" in relation:
        margin = str(relation["margin"])
        if not _MARGIN.fullmatch(margin):
            problems.append(f"a record relation's margin {margin!r} is not a number")
        elif (Decimal(margin) > 0) - (Decimal(margin) < 0) != _MARGIN_SIGN.get(
            str(relation.get("relation")), 2
        ):
            problems.append(
                f"a record relation {relation.get('relation')} has the margin {margin}"
            )
    return problems


def _mappings(found: list[str], items: Any, what: str) -> list[Mapping[str, Any]]:
    """The mappings of a list the ledger holds, each other item named in ``found``."""
    if items is None:
        return []
    if not isinstance(items, list):
        found.append(f"{what} is not a list")
        return []
    kept = [item for item in items if isinstance(item, Mapping)]
    found.extend(
        f"{what}: {str(item)[:60]!r} is not a mapping"
        for item in items
        if not isinstance(item, Mapping)
    )
    return kept


def _named(item: Mapping[str, Any]) -> tuple[str, int]:
    """The (report, count) an exception or a key-reason candidate names; 0 for no count."""
    n = item.get("n")
    return str(item.get("report")), n if _is_count(n) else 0


def problems(ledger: Mapping[str, Any]) -> list[str]:
    """Every way the input breaks its contract; empty when it holds."""
    missing = [key for key in LEDGER_KEYS if key not in ledger]
    if missing:
        return [f"the ledger is missing {missing}"]
    found: list[str] = []
    if ledger.get("format") != LEDGER_FORMAT:
        found.append(f"format is not {LEDGER_FORMAT}")
    if not _COMMIT.fullmatch(str(ledger.get("read_at_main"))):
        found.append("read_at_main is not a commit")
    if not _DATE.fullmatch(str(ledger.get("read_on"))):
        found.append("read_on is not a date")
    if not str(ledger.get("rule") or "").strip():
        found.append("the rule is not quoted")
    found.extend(
        f"lane {lane.get('name')}: a branch and a full commit"
        for lane in _mappings(found, ledger["lanes"], "lanes")
        if not _COMMIT.fullmatch(str(lane.get("commit"))) or not lane.get("branch")
    )
    labels: set[str] = set()
    claimed: set[tuple[str, int]] = set()
    arrivals: dict[int, dict[str, list[str]]] = {}
    for report in _mappings(found, ledger["reports"], "reports"):
        label = str(report.get("report"))
        absent = [key for key in (*REPORT_KEYS, "claims") if key not in report]
        if absent:
            found.append(f"{label}: missing {absent}")
            continue
        mistyped = [key for key in REPORT_KEYS if not isinstance(report[key], str)]
        if mistyped:
            found.append(f"{label}: {mistyped} are not strings")
            continue
        if label in labels:
            found.append(f"{label}: the report is listed twice")
        labels.add(label)
        if report["kind"] not in KINDS:
            found.append(f"{label}: unknown kind {report['kind']!r}")
        when = report["reported_at"]
        if when != UNKNOWN and not _UTC.fullmatch(when):
            found.append(f"{label}: reported_at is neither a UTC time nor {UNKNOWN}")
        if report["bead"] and not _BEAD.fullmatch(report["bead"]):
            found.append(f"{label}: bead is not a think-xxxx id")
        claims = _mappings(found, report["claims"], f"{label} claims")
        if not report["claims"]:
            found.append(f"{label}: no claims")
        for claim in claims:
            where = f"{label} n={claim.get('n')}"
            found.extend(_problems_of_claim(where, claim, when))
            n = claim.get("n")
            if not _is_count(n):
                continue
            key = (label, n)
            if key in claimed:
                found.append(f"{where}: the claim is listed twice")
            claimed.add(key)
            arrived = str(claim.get("reported_at") or when)
            if arrived != UNKNOWN:
                arrivals.setdefault(key[1], {}).setdefault(arrived, []).append(label)
    found.extend(
        f"n={n}: {' and '.join(sorted(tied))} arrive at {arrived}, so only their labels "
        "would order them; give each claim its own reported_at"
        for n, times in sorted(arrivals.items())
        for arrived, tied in times.items()
        if len(tied) > 1
    )
    for exception in _mappings(found, ledger["exceptions"], "exceptions"):
        key = _named(exception)
        if key not in claimed:
            found.append(f"exception {key}: names no claim of the ledger")
        if not str(exception.get("reason") or "").strip():
            found.append(f"exception {key}: states no reason")
    candidates = ledger.get("key_reason_candidates")
    for candidate in _mappings(found, candidates, "key_reason_candidates"):
        key = _named(candidate)
        if key not in claimed:
            found.append(f"key-reason candidate {key}: names no claim of the ledger")
        if not str(candidate.get("argument") or "").strip():
            found.append(f"key-reason candidate {key}: states no argument")
    for item in _mappings(found, ledger["other_items"], "other_items"):
        absent = set(OtherItem.__annotations__) - set(item)
        if absent:
            found.append(f"other item {item.get('issue')}: missing {sorted(absent)}")
    if not isinstance(ledger.get("cross_check", []), list):
        found.append("cross_check is not a list")
    return found


def load_ledger(directory: Path) -> Ledger:
    value = load_yaml(directory / LEDGER)
    _require(isinstance(value, dict), f"{LEDGER} is not a mapping")
    found = problems(value)
    _require(not found, "; ".join(found))
    return cast("Ledger", value)


# --------------------------------------------------------------------------- the start


#: Digits of the interval arithmetic that encloses a case record's closed form, and of the
#: root finder whose result an exact sign change then confirms.
INTERVAL_DIGITS = 90
#: mpmath's interval context, untyped: its stubs know neither its arithmetic nor its precision.
IV: Any = mp.iv


class StartMember(TypedDict):
    """One member of a count's start as ``gather`` froze it in ``starts.yaml``.

    ``low`` and ``high`` bound the side (exact fractions; ``open_*`` say whether the bound
    is excluded). ``lanes`` are the case lanes it stands for, each as its name, the value
    and exact form the case record printed, which a lane's frozen relation must match, and
    the polynomial it was read with (`lane_polynomials`). ``stated`` is a pending register
    entry's stated value and slack. ``check`` recomputes the span from these
    (`starts_problems`), so a span edited by hand is refused.
    """

    label: str
    kind: str
    holders: str
    model: str
    low: str
    high: str
    open_low: bool
    open_high: bool
    shown: str
    decide: str
    lanes: list[list[str]]
    stated: NotRequired[list[str]]


@dataclass(frozen=True)
class Side:
    """One side in the walk: a member of the record's start, or one report's claim."""

    label: str
    holders: str
    span: Span
    shown: str
    value: Fraction
    kind: str
    reported_at: str = ""
    first_committed: str = ""
    exact: bool = False
    relations: tuple[RecordRelation, ...] = ()
    record_prints: tuple[tuple[str, str, str], ...] = ()
    decide: str = ""
    restates: str = ""
    refines: Refines | None = None
    new_packing: NewPacking | None = None
    measured: Measured | None = None


def shown(value: Fraction) -> str:
    """``value`` rounded up at `SHOWN_PLACES` places."""
    scaled = value * 10**SHOWN_PLACES
    whole = math.ceil(scaled)
    text = str(whole).rjust(SHOWN_PLACES + 1, "0")
    return f"{text[:-SHOWN_PLACES]}.{text[-SHOWN_PLACES:]}"


def scientific(value: Fraction) -> str:
    return f"{float(value):.2e}"


def _record_holders(bound: Mapping[str, Any], names: Mapping[str, str]) -> str:
    """A case lane's credit: its finders, then its improvers, each by the display name
    ``names`` gives it (`display_names`), else as the record writes it."""
    found = [names.get(str(name), str(name)) for name in bound.get("found_by") or []]
    improved = [names.get(str(name), str(name)) for name in bound.get("improved_by") or []]
    text = ", ".join(found) or str(bound.get("source_key") or "")
    return f"{text}, improved by {', '.join(improved)}" if improved else text


_TOKEN = re.compile(r"\s*(?:([0-9]+(?:\.[0-9]+)?)|(sqrt)|([-+*/()]))")


def _tokens(form: str) -> list[tuple[str, str]] | None:
    """The tokens of a closed form, with the implicit products of ``(1/2)sqrt(2)`` made
    explicit; None where the text has anything else, such as ``root(``."""
    tokens: list[tuple[str, str]] = []
    position = 0
    while position < len(form):
        match = _TOKEN.match(form, position)
        if match is None:
            return None if form[position:].strip() else tokens
        position = match.end()
        if match.group(1):
            token = ("number", match.group(1))
        elif match.group(2):
            token = ("sqrt", "sqrt")
        else:
            token = ("operator", match.group(3))
        previous = tokens[-1] if tokens else None
        implicit = previous is not None and (
            previous[0] == "number" or previous == ("operator", ")")
        )
        if implicit and (token[0] in ("number", "sqrt") or token == ("operator", "(")):
            tokens.append(("operator", "*"))
        tokens.append(token)
    return tokens


class _ClosedForm:
    """A recursive-descent reader of a closed form over the rationals and ``sqrt``.

    It evaluates exactly while it can and in `INTERVAL_DIGITS`-digit interval arithmetic
    once a square root appears, so the result is an exact `Fraction` or a rigorous
    enclosure.
    """

    def __init__(self, tokens: list[tuple[str, str]]) -> None:
        self.tokens = tokens
        self.position = 0

    def peek(self) -> tuple[str, str] | None:
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def take(self) -> tuple[str, str]:
        _require(self.position < len(self.tokens), "a closed form ended early")
        token = self.tokens[self.position]
        self.position += 1
        return token

    def expression(self) -> Any:
        value = self.term()
        while self.peek() in (("operator", "+"), ("operator", "-")):
            operator = self.take()[1]
            other = self.term()
            value = _combine(value, other, operator)
        return value

    def term(self) -> Any:
        value = self.factor()
        while self.peek() in (("operator", "*"), ("operator", "/")):
            operator = self.take()[1]
            other = self.factor()
            value = _combine(value, other, operator)
        return value

    def factor(self) -> Any:
        token = self.take()
        if token == ("operator", "-"):
            return -self.factor()
        if token == ("operator", "("):
            value = self.expression()
            _require(self.take() == ("operator", ")"), "an unclosed parenthesis")
            return value
        if token[0] == "sqrt":
            _require(self.take() == ("operator", "("), "sqrt without its argument")
            value = self.expression()
            _require(self.take() == ("operator", ")"), "an unclosed sqrt")
            return IV.sqrt(_interval(value))
        _require(token[0] == "number", f"an unexpected {token[1]!r}")
        return Fraction(Decimal(token[1]))


def _interval(value: Any) -> Any:
    """A rigorous interval for an exact `Fraction`, or the interval itself."""
    if isinstance(value, Fraction):
        return IV.mpf(value.numerator) / IV.mpf(value.denominator)
    return value


_ARITHMETIC: Mapping[str, Callable[[Any, Any], Any]] = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}


def _combine(value: Any, other: Any, operator: str) -> Any:
    """Exact while both operands are, in interval arithmetic once either is an interval."""
    if isinstance(value, Fraction) and isinstance(other, Fraction):
        return _ARITHMETIC[operator](value, other)
    return _ARITHMETIC[operator](_interval(value), _interval(other))


def _fraction(raw: Any) -> Fraction:
    """A raw mpmath number (an ``_mpf_`` tuple) as the exact rational it is."""
    numerator, denominator = to_rational(raw)
    return Fraction(int(numerator), int(denominator))


@contextmanager
def _interval_digits(digits: int) -> Iterator[None]:
    """Interval arithmetic at ``digits`` decimal digits, restored afterwards."""
    saved = IV.prec
    IV.dps = digits
    try:
        yield
    finally:
        IV.prec = saved


def closed_form_span(form: str) -> Span | None:
    """A closed form of integers, decimals, ``+ - * /``, parentheses and ``sqrt``, as one
    exact number or a rigorous enclosure; None for any other form, such as a root."""
    tokens = _tokens(form) if form else None
    if not tokens:
        return None
    with _interval_digits(INTERVAL_DIGITS):
        reader = _ClosedForm(tokens)
        try:
            value = reader.expression()
        except LedgerError, ZeroDivisionError:
            return None
        if reader.position != len(tokens):
            return None
        if isinstance(value, Fraction):
            return exact_span(value)
        low, high = value._mpi_
        return Span(_fraction(low), _fraction(high), open_low=False, open_high=False)


_MONOMIAL = re.compile(r"([+-]?)([0-9]*)(s(?:\^\{?([0-9]+)\}?)?)?")


def polynomial(text: str) -> list[int]:
    """The integer coefficients, highest degree first, of a polynomial in ``s`` written as
    ``s^8 - 20s^7 + ... - 6865 = 0`` or ``4775s^{18} - 190430s^{17} + ...``."""
    written = text.split("=", 1)[0].replace(" ", "")
    coefficients: dict[int, int] = {}
    position = 0
    while position < len(written):
        match = _MONOMIAL.match(written, position)
        _require(match is not None and match.end() > position, f"not a polynomial: {text!r}")
        assert match is not None
        sign = -1 if match.group(1) == "-" else 1
        if match.group(3):
            degree = int(match.group(4) or 1)
            coefficient = int(match.group(2) or 1)
        else:
            _require(match.group(2), f"not a polynomial: {text!r}")
            degree, coefficient = 0, int(match.group(2))
        coefficients[degree] = coefficients.get(degree, 0) + sign * coefficient
        position = match.end()
    _require(coefficients, f"not a polynomial: {text!r}")
    return [coefficients.get(degree, 0) for degree in range(max(coefficients), -1, -1)]


def _evaluate_at(coefficients: Sequence[int], point: Fraction) -> Fraction:
    total = Fraction(0)
    for coefficient in coefficients:
        total = total * point + coefficient
    return total


def root_span(coefficients: Sequence[int], near: str) -> Span:
    """A rigorous enclosure of the root of an integer polynomial nearest ``near``: a
    high-precision root, then rational endpoints where the polynomial changes sign.

    The enclosure must lie inside ``near`` read as an unstated print, within one unit of
    its last place; a polynomial whose root there is another number is refused.
    """
    with mp.workdps(INTERVAL_DIGITS + 30):
        root = mp.findroot(lambda s: mp.polyval(list(coefficients), s), mp.mpf(near))
        centre = _fraction(mp.mpf(root)._mpf_)
    printed = printed_side(near, "unstated")
    for places in range(INTERVAL_DIGITS + 30, 20, -5):
        epsilon = Fraction(1, 10**places)
        low, high = centre - epsilon, centre + epsilon
        if _evaluate_at(coefficients, low) * _evaluate_at(coefficients, high) < 0:
            _require(
                contains(printed, low) and contains(printed, high),
                f"the polynomial's root nearest {near} is {float(centre)!r}, outside that "
                "print: the lane's form names another polynomial",
            )
            return Span(low, high, open_low=False, open_high=False)
    raise LedgerError(f"no sign change of the polynomial around {near}")


def _member(
    label: str,
    kind: str,
    holders: str,
    *,
    model: str,
    span: Span,
    display: str,
    decide: str,
    lanes: list[list[str]],
) -> StartMember:
    return {
        "label": label,
        "kind": kind,
        "holders": holders,
        "model": model,
        "low": str(span.low),
        "high": str(span.high),
        "open_low": span.open_low,
        "open_high": span.open_high,
        "shown": display,
        "decide": decide,
        "lanes": lanes,
    }


def lane_member(
    n: int,
    lane: str,
    bound: Mapping[str, Any],
    entries: Iterable[str],
    polynomial_text: str = "",
    *,
    names: Mapping[str, str] | None = None,
) -> StartMember:
    """One case lane's upper bound: its exact form where that is rational, a rigorous
    interval where it is a closed form with ``sqrt``, an enclosure of the root a ``root(``
    form names where the case states the polynomial, else its print within one unit.
    ``names`` credits a holder by the display name the intake gives it (`display_names`)."""
    named = ", ".join(sorted(entries)) or str(bound.get("source_key") or "")
    label = f"record {named}"
    holders = _record_holders(bound, names or {}) or ", ".join(sorted(entries))
    value = str(bound["value"])
    form = str(bound.get("exact_form") or "")
    lanes = [[lane, value, form, polynomial_text]]
    span = closed_form_span(form) if form else None
    if span is not None and span.low == span.high:
        return _member(
            label,
            "record",
            holders,
            model="exact",
            span=span,
            display=shown(span.low),
            decide="",
            lanes=lanes,
        )
    if span is not None:
        decide = f"an exact comparison with the {lane} lane's closed form {form}"
        return _member(
            label,
            "record",
            holders,
            model="closed form",
            span=span,
            display=value,
            decide=decide,
            lanes=lanes,
        )
    if form.startswith("root(") and polynomial_text:
        enclosure = root_span(polynomial(polynomial_text), value)
        decide = f"an exact comparison with the {lane} lane's {form.partition(',')[0]})"
        return _member(
            label,
            "record",
            holders,
            model="root",
            span=enclosure,
            display=value,
            decide=decide,
            lanes=lanes,
        )
    if "." not in value:
        exact = exact_span(number(value))
        return _member(
            label,
            "record",
            holders,
            model="exact",
            span=exact,
            display=value,
            decide="",
            lanes=lanes,
        )
    degree = bound.get("algebraic_degree")
    if bound.get("minimal_polynomial"):
        decide = (
            f"the root of the {lane} lane's degree-{degree} minimal polynomial at its print "
            f"{value} (n = {n})"
        )
    else:
        decide = f"the exact side behind the {lane} lane's print {value} (n = {n})"
    span = printed_side(value, "unstated")
    return _member(
        label,
        "record",
        holders,
        model="print",
        span=span,
        display=value,
        decide=decide,
        lanes=lanes,
    )


def merged_lanes(reported: StartMember, verified: StartMember) -> list[StartMember]:
    """The two lanes, as one member where they are the same side and separate otherwise."""
    same = all(
        reported[key] == verified[key] for key in ("low", "high", "open_low", "open_high")
    )
    if same and reported["model"] == verified["model"]:
        names = dict.fromkeys(
            [
                reported["label"].removeprefix("record "),
                verified["label"].removeprefix("record "),
            ]
        )
        return [
            {
                **reported,
                "label": f"record {', '.join(names)}",
                "lanes": reported["lanes"] + verified["lanes"],
            }
        ]
    return [
        {**reported, "label": f"{reported['label']} (reported lane)"},
        {**verified, "label": f"{verified['label']} (verified lane)"},
    ]


def pending_member(record: Mapping[str, Any], stated: check_standing.Stated) -> StartMember:
    """A register entry pending adoption, at the bound its words state."""
    if stated.slack:
        span = Span(stated.value, stated.value + stated.slack, open_low=False, open_high=True)
    else:
        span = exact_span(stated.value)
    entry = str(record["id"])
    keys = (record.get("attribution") or {}).get("source_keys") or []
    holders = ", ".join(str(key) for key in keys) or entry
    model = "print" if stated.slack else "exact"
    decide = f"{entry}'s exact side" if stated.slack else ""
    label = f"register {entry}, pending adoption"
    member = _member(
        label,
        "register",
        holders,
        model=model,
        span=span,
        display=shown(stated.value),
        decide=decide,
        lanes=[],
    )
    member["stated"] = [str(stated.value), str(stated.slack)]
    return member


def beyond_member(n: int, rows: Mapping[int, Mapping[str, Any]]) -> StartMember:
    """Above the horizon: the current beyond-horizon row, read within one unit of its
    print, else the grid."""
    row = rows.get(n)
    if row is None:
        grid = exact_span(grid_side(n))
        return _member(
            "the grid",
            "record",
            "ceil(sqrt n)",
            model="exact",
            span=grid,
            display=str(grid.low),
            decide="",
            lanes=[],
        )
    value = str(row["value"])
    decide = f"the exact side of the beyond-horizon row {row['source_id']} at n = {n}"
    return _member(
        f"beyond-horizon row {row['source_id']}",
        "record",
        str(row["source_id"]),
        model="print",
        span=printed_side(value, "unstated"),
        display=value,
        decide=decide,
        lanes=[],
    )


def lane_polynomials(
    reported: Mapping[str, Any], verified: Mapping[str, Any]
) -> tuple[str, str]:
    """The polynomial each case lane is read with: the lane's own ``minimal_polynomial``.

    The verified lane's schema has no such field, so a ``root(`` form there names the
    reported lane's, the one polynomial a case states (n = 11's ``P_trump11``).
    `root_span` refuses an enclosure outside the lane's own print, so a form that names
    some other polynomial is refused rather than read as this one.
    """
    stated = str(reported.get("minimal_polynomial") or "")
    own = str(verified.get("minimal_polynomial") or "")
    named = str(verified.get("exact_form") or "").startswith("root(")
    return stated, own or (stated if named else "")


def display_names(sources: Mapping[str, Any]) -> dict[str, str]:
    """How the intake credits a case record's finder or improver where the owner asked for
    a name other than the one the record writes: ``sources.yaml``'s ``display_names``."""
    names = sources.get("display_names") or {}
    _require(
        isinstance(names, Mapping)
        and all(
            isinstance(key, str) and isinstance(value, str) for key, value in names.items()
        ),
        f"{SOURCES}: display_names maps a name the record writes to the name credited",
    )
    return dict(names)


def tree_members(
    counts: Iterable[int], *, names: Mapping[str, str] | None = None
) -> dict[int, list[StartMember]]:
    """Each count's start members, read from the records on the tree: both case lanes and
    any register entry pending adoption that states a smaller bound, or above the horizon
    the beyond-horizon row or the grid. A lane's holders are credited by ``names``."""
    wanted = sorted(set(counts))
    members: dict[int, list[StartMember]] = {}
    inside = [n for n in wanted if n <= HORIZON]
    if inside:
        records = view.load_records()
        pending: dict[int, list[StartMember]] = {}
        for record in records.register.results:
            if view.standing(record, records) != view.PENDING_ADOPTION:
                continue
            for finding in check_standing.improvements(record, records):
                if finding.direction == check_standing.UPPER:
                    pending.setdefault(finding.n, []).append(
                        pending_member(record, finding.stated)
                    )
        for n in inside:
            case = coverage_check.parse_case(FRONTIER / f"n-{n:03d}.md")
            reported, verified = case["reported_upper_bound"], case["verified_upper_bound"]
            reported_text, verified_text = lane_polynomials(reported, verified)
            lanes = merged_lanes(
                lane_member(
                    n,
                    "reported",
                    reported,
                    view.lane_holders(n, records, "upper", ("reported",)),
                    reported_text,
                    names=names,
                ),
                lane_member(
                    n,
                    "verified",
                    verified,
                    view.lane_holders(n, records, "upper", ("verified",)),
                    verified_text,
                    names=names,
                ),
            )
            members[n] = [*lanes, *pending.get(n, [])]
    outside = [n for n in wanted if n > HORIZON]
    if outside:
        coverage = load_yaml(coverage_check.COVERAGE)
        rows = coverage_check.current_beyond_horizon(coverage)
        for n in outside:
            members[n] = [beyond_member(n, rows)]
    return members


def side_of(member: StartMember) -> Side:
    """A start member as a side of the walk."""
    span = Span(
        number(member["low"]),
        number(member["high"]),
        open_low=member["open_low"],
        open_high=member["open_high"],
    )
    exact = member["model"] == "exact"
    value = (
        span.low if exact else (number(member["shown"]) if "." in member["shown"] else span.low)
    )
    prints = tuple((lane[0], lane[1], lane[2]) for lane in member["lanes"])
    stated = member.get("stated")
    if member["kind"] == "register" and stated:
        # A pending entry is read as its id and the value its words state (`RecordRelation`).
        entry = member["label"].removeprefix("register ").removesuffix(", pending adoption")
        prints = ((entry, str(stated[0]), ""),)
    return Side(
        member["label"],
        member["holders"],
        span,
        member["shown"],
        value,
        member["kind"],
        exact=exact,
        record_prints=prints,
        decide=member["decide"],
    )


def record_side(
    n: int, bound: Mapping[str, Any], entries: Iterable[str], lane: str = "reported"
) -> Side:
    """One case lane as a side (`lane_member`)."""
    return side_of(
        lane_member(n, lane, bound, entries, str(bound.get("minimal_polynomial") or ""))
    )


def pending_side(record: Mapping[str, Any], stated: check_standing.Stated) -> Side:
    return side_of(pending_member(record, stated))


def beyond_side(n: int, rows: Mapping[int, Mapping[str, Any]]) -> Side:
    return side_of(beyond_member(n, rows))


def minimal(sides: Sequence[Side]) -> list[Side]:
    """The members nothing else is decidably below: the start the walk is seeded with.

    A pending register bound below a case lane removes that lane; two pending bounds that
    overlap each other both stay, and a claim must be below both to be recorded.
    """
    return [
        side
        for side in sides
        if not any(below(other.span, side.span) for other in sides if other is not side)
    ]


_SPAN = ("model", "low", "high", "open_low", "open_high")
_MEMBER_TYPES: Mapping[str, type] = {
    **dict.fromkeys(
        ("label", "kind", "holders", "model", "low", "high", "shown", "decide"), str
    ),
    "open_low": bool,
    "open_high": bool,
    "lanes": list,
}


def recomputed(n: int, member: Mapping[str, Any]) -> list[dict[str, Any]]:
    """The span each of a frozen member's stored inputs gives: every case lane it stands
    for (`lane_member`), a pending entry's stated bound, a beyond-horizon print, or the
    grid. Each must equal the member's own."""
    if member["lanes"]:
        found = []
        for lane in member["lanes"]:
            _require(
                isinstance(lane, list)
                and len(lane) == 4
                and all(isinstance(x, str) for x in lane),
                "a lane is [name, value, exact form, polynomial]",
            )
            name, value, form, text = lane
            bound = {"value": value, "exact_form": form, "minimal_polynomial": text}
            found.append(lane_member(n, name, bound, [], text))
    elif member["kind"] == "register":
        stated = member.get("stated")
        stated = stated if isinstance(stated, list) else []
        _require(len(stated) == 2, "a pending entry states [value, slack]")
        value, slack = (number(str(item)) for item in stated)
        found = [pending_member({"id": "-"}, check_standing.Stated(value, slack))]
    elif member["label"] == "the grid":
        found = [beyond_member(n, {})]
    else:
        source = str(member["label"]).removeprefix("beyond-horizon row ")
        found = [beyond_member(n, {n: {"value": member["shown"], "source_id": source}})]
    return [{key: item[key] for key in _SPAN} for item in found]


def starts_problems(value: Any, read_at_main: str) -> list[str]:
    """Every way a frozen ``starts.yaml`` breaks its contract: its header, its shape, an
    empty start, and any member whose span is not the one its stored inputs give."""
    if not isinstance(value, Mapping) or value.get("format") != STARTS_FORMAT:
        return [f"{STARTS} is not a mapping of format {STARTS_FORMAT}"]
    if value.get("read_at_main") != read_at_main:
        return [
            f"{STARTS} was read at {value.get('read_at_main')}, the ledger at {read_at_main}"
        ]
    counts = value.get("counts")
    if not isinstance(counts, list):
        return [f"{STARTS}: counts is not a list"]
    found: list[str] = []
    seen: set[int] = set()
    for count in counts:
        if not isinstance(count, Mapping) or not _is_count(count.get("n")):
            found.append(f"{STARTS}: a count without a positive n: {str(count)[:80]}")
            continue
        n = count["n"]
        if n in seen:
            found.append(f"{STARTS} n = {n}: listed twice")
        seen.add(n)
        members = count.get("members")
        if not isinstance(members, list) or not members:
            found.append(f"{STARTS} n = {n}: no members; a start is never empty")
            continue
        for member in members:
            found.extend(_member_problems(n, member))
    return found


def _member_problems(n: int, member: Any) -> list[str]:
    where = f"{STARTS} n = {n}"
    if not isinstance(member, Mapping):
        return [f"{where}: a member is not a mapping"]
    wrong = sorted(
        key for key, kind in _MEMBER_TYPES.items() if not isinstance(member.get(key), kind)
    )
    if wrong:
        return [f"{where} {member.get('label')}: missing or mistyped {wrong}"]
    where = f"{where} {member['label']}"
    try:
        frozen = {key: member[key] for key in _SPAN}
        spans = recomputed(n, member)
    except LedgerError as error:
        return [f"{where}: {error}"]
    return [
        f"{where}: frozen {frozen}, but its stored inputs give {span}"
        for span in spans
        if span != frozen
    ]


def load_starts(directory: Path, read_at_main: str) -> dict[int, list[Side]]:
    """The starts ``gather`` froze, refused unless they were read at ``read_at_main`` and
    every member's span is the one its stored inputs give (`starts_problems`)."""
    value = load_yaml(directory / STARTS)
    found = starts_problems(value, read_at_main)
    _require(not found, "; ".join(found))
    return {
        int(count["n"]): [side_of(cast("StartMember", member)) for member in count["members"]]
        for count in value["counts"]
    }


def starts_document(
    read_at_main: str, members: Mapping[int, list[StartMember]]
) -> dict[str, Any]:
    return {
        "format": STARTS_FORMAT,
        "read_at_main": read_at_main,
        "counts": [{"n": n, "members": members[n]} for n in sorted(members)],
    }


def tree_drift(directory: Path) -> list[str]:
    """Where the records on the tree now give a start other than the frozen one."""
    frozen = load_yaml(directory / STARTS)
    counts = [int(count["n"]) for count in frozen["counts"]]
    now = tree_members(counts, names=display_names(load_yaml(directory / SOURCES)))
    drift = []
    for count in frozen["counts"]:
        n = int(count["n"])
        if count["members"] != now[n]:
            before = "; ".join(f"{m['label']} {m['shown']}" for m in count["members"])
            after = "; ".join(f"{m['label']} {m['shown']}" for m in now[n])
            drift.append(f"n = {n}: frozen {before}; on the tree {after}")
    return drift


# --------------------------------------------------------------------------- the walk


def entry_side(report: Report, claim: Claim) -> Side:
    span = claim_span(claim)
    exact = "exact" in claim or claim["rounding"] == "exact"
    value = number(claim.get("exact", claim["printed"]))
    decide = "" if exact else f"the exact side of {report['report']} at n = {claim['n']}"
    if exact:
        display = shown(value)
    elif len(claim["printed"].partition(".")[2]) > SHOWN_PLACES:
        display = shown(span.high)
    else:
        display = claim["printed"]
    return Side(
        report["report"],
        report["holders"],
        span,
        display,
        value,
        report["kind"],
        reported_at=claim.get("reported_at", report["reported_at"]),
        first_committed=claim.get("first_committed", ""),
        exact=exact,
        relations=tuple(claim.get("record_relations", [])),
        decide=decide,
        restates=claim.get("restates", ""),
        refines=claim.get("refines"),
        new_packing=claim.get("new_packing"),
        measured=claim.get("measured"),
    )


_INVERSE = {BELOW: ABOVE, ABOVE: BELOW, EQUAL: EQUAL}


def _frozen_relation(side: Side, other: Side) -> RecordRelation | None:
    """The frozen relation of ``side`` to the case lane or pending entry ``other`` stands
    for, while the record still prints the value and form the relation read."""
    for relation in side.relations:
        read = (relation["lane"], relation["value"], relation["exact_form"])
        if read in other.record_prints:
            return relation
    return None


def _frozen(side: Side, other: Side) -> str | None:
    relation = _frozen_relation(side, other)
    return None if relation is None else relation["relation"]


def _frozen_margin(side: Side, other: Side) -> Fraction | None:
    """How far apart a frozen relation that states a margin puts the two, read in either
    order."""
    relation = _frozen_relation(side, other) or _frozen_relation(other, side)
    if relation is None or "margin" not in relation:
        return None
    return abs(Fraction(Decimal(relation["margin"])))


def _frozen_either(side: Side, other: Side) -> str | None:
    """A frozen relation of ``side`` to ``other``, read in either order."""
    frozen = _frozen(side, other)
    if frozen is not None:
        return frozen
    inverse = _frozen(other, side)
    return None if inverse is None else _INVERSE[inverse]


def compare(side: Side, other: Side) -> str:
    """Where ``side`` stands against ``other``: below, above, equal or undecided.

    A lane's frozen relation between an algebraic side and a case lane replaces the spans,
    read in either order.
    """
    frozen = _frozen_either(side, other)
    if frozen is not None:
        return frozen
    if below(side.span, other.span):
        return BELOW
    if below(other.span, side.span):
        return ABOVE
    if side.exact and other.exact and side.span == other.span:
        return EQUAL
    return UNDECIDED


@dataclass
class Step:
    """One claim's verdict in the walk at one count."""

    side: Side
    verdict: str
    reason: str
    holders: list[Side]
    against: list[Side] = field(default_factory=list)
    exception: str = ""


@dataclass
class Walk:
    n: int
    start: list[Side]
    steps: list[Step]
    standing: list[Side]


def clamped(side: Side, members: Iterable[Side]) -> Side:
    """``side`` with its span ended below each member a frozen relation puts it below.

    The relation compares the side with the member's exact value, which lies in the
    member's span, so the side is below the member's ``high``: a claim recorded through a
    frozen relation, or joining the standing side through one, keeps that once the member
    leaves the set, and a later claim above the member is above it too. For an exact
    member that bound is the member itself.
    """
    span = side.span
    for member in members:
        if _frozen_either(side, member) != BELOW:
            continue
        if member.span.high < span.high or (
            member.span.high == span.high and not span.open_high
        ):
            span = Span(span.low, member.span.high, open_low=span.open_low, open_high=True)
    return side if span == side.span else replace(side, span=span)


def decider(side: Side, others: Sequence[Side]) -> str:
    needed = [item.decide for item in (side, *others) if item.decide]
    return "; ".join(dict.fromkeys(needed)) or "an exact comparison of the two sides"


def walk(
    n: int,
    start: Side | Sequence[Side],
    entries: Sequence[Side],
    exceptions: Mapping[tuple[int, str], str] | None = None,
) -> Walk:
    """The owner's rule at one count: each claim in report order against the standing side.

    The standing side is a set: the minimal members of the start (`minimal`), then each
    recorded claim, together with any undecided claim nothing has since been decidably
    below. A claim is recorded only when it is below every member; it is not recorded when
    it is above or exactly equal to one; otherwise it is undecided and joins the set. A
    claim recorded, or joining, through a lane's frozen relation below a member carries
    that relation in its span (`clamped`).
    """
    exceptions = exceptions or {}
    seeds = minimal([start] if isinstance(start, Side) else list(start))
    standing = list(seeds)
    steps: list[Step] = []
    for side in sorted(entries, key=lambda item: (item.reported_at, item.label)):
        relations = [(member, compare(side, member)) for member in standing]
        above = [member for member, relation in relations if relation == ABOVE]
        equal = [member for member, relation in relations if relation == EQUAL]
        unsure = [member for member, relation in relations if relation == UNDECIDED]
        if all(relation == BELOW for _, relation in relations):
            step = Step(side, RECORDED, BELOW, [member for member, _ in relations])
            standing = [clamped(side, standing)]
        elif above or equal:
            reason = ABOVE if above else EQUAL
            step = Step(side, NOT_RECORDED, reason, above or equal)
        else:
            step = Step(side, UNDECIDED, UNDECIDED, unsure, against=unsure)
            joining = clamped(side, standing)
            standing = [member for member in standing if compare(member, side) != ABOVE]
            standing.append(joining)
        reason = exceptions.get((n, side.label))
        if reason and step.verdict != RECORDED:
            step.verdict, step.exception = BY_EXCEPTION, reason
        steps.append(step)
    return Walk(n, seeds, steps, standing)


# --------------------------------------------------------------------------- the render


def _when(text: str) -> str:
    return text.replace("T", " ").removesuffix("Z") + "Z" if _UTC.fullmatch(text) else text


def held_by(step: Step) -> str:
    return ", ".join(member.label for member in step.holders)


def _difference(step: Step) -> str:
    """The claim against what it was decided by, as a distance and a direction."""
    if step.reason == EQUAL:
        return "equal"
    if step.reason == UNDECIDED or not step.holders:
        return ""
    word = "below" if step.reason == BELOW else "above"
    gaps = [_gap(step.side, member, step.reason) for member in step.holders]
    gap, how = min(gaps, key=lambda item: item[0])
    return f"{word} by {how}{scientific(gap)}"


def _gap(side: Side, member: Side, reason: str) -> tuple[Fraction, str]:
    """How far apart two decided sides are: exactly where both are exact or a frozen
    relation states its margin, else the least separation of the numbers each may be; a
    lane's exact relation where the spans meet."""
    if side.exact and member.exact:
        return abs(member.value - side.value), ""
    margin = _frozen_margin(side, member)
    if margin is not None:
        return margin, ""
    if reason == BELOW:
        separation = member.span.low - side.span.high
    else:
        separation = side.span.low - member.span.high
    if separation > 0:
        return separation, "at least "
    return abs(member.value - side.value), "about "


def step_record(step: Step) -> dict[str, Any]:
    side = step.side
    record: dict[str, Any] = {
        "report": side.label,
        "kind": side.kind,
        "reported_at": side.reported_at,
        "side": side.shown,
        "exact": side.exact,
        "verdict": step.verdict,
        "reason": step.reason,
        "decided_against": [member.label for member in step.holders],
        "difference": _difference(step),
    }
    if side.first_committed:
        record["first_committed"] = side.first_committed
    if UNDECIDED in (step.verdict, step.reason):
        record["decide_by"] = decider(side, step.against)
    if step.exception:
        record["exception"] = step.exception
    if side.restates:
        record["restates"] = side.restates
    if side.measured is not None:
        record["measured"] = side.measured["finding"]
    if side.refines is not None:
        record["packing"] = {
            "kind": REFINEMENT,
            "packing_of": side.refines["packing_of"],
            "entry": side.refines["entry"],
        }
    elif side.new_packing is not None:
        record["packing"] = {
            "kind": NEW,
            **{key: value for key, value in side.new_packing.items() if key == "continues"},
        }
    return record


def side_record(side: Side) -> dict[str, Any]:
    return {
        "label": side.label,
        "holders": side.holders,
        "side": side.shown,
        "exact": side.exact,
    }


def _entries(ledger: Ledger, *, publications: bool) -> tuple[dict[int, list[Side]], list[Any]]:
    by_count: dict[int, list[Side]] = {}
    unknown: list[Any] = []
    for report in ledger["reports"]:
        if report["kind"] == "publication" and not publications:
            continue
        for claim in report["claims"]:
            side = entry_side(report, claim)
            if side.reported_at == UNKNOWN:
                unknown.append({"n": claim["n"], "report": report["report"]})
                continue
            by_count.setdefault(claim["n"], []).append(side)
    return by_count, unknown


def counts_of(ledger: Ledger) -> list[int]:
    return sorted({claim["n"] for report in ledger["reports"] for claim in report["claims"]})


def evaluate(ledger: Ledger, starts: Mapping[int, Sequence[Side]]) -> dict[str, Any]:
    """Every verdict, the owner decisions and the per-report summary, as ``ledger.json``."""
    exceptions = {
        (item["n"], item["report"]): item["reason"] for item in ledger.get("exceptions", [])
    }
    entries, unknown = _entries(ledger, publications=True)
    alternative_entries, _ = _entries(ledger, publications=False)
    walks = [walk(n, starts[n], entries.get(n, []), exceptions) for n in counts_of(ledger)]
    alternative = {
        n: walk(n, starts[n], alternative_entries.get(n, []), exceptions)
        for n in counts_of(ledger)
    }
    candidates = {
        (item["n"], item["report"]): item["argument"]
        for item in ledger.get("key_reason_candidates", [])
    }
    counts = []
    for result in walks:
        steps = [step_record(step) for step in result.steps]
        for record in steps:
            argument = candidates.get((result.n, record["report"]))
            if argument:
                record["key_reason_candidate"] = argument
        changed = publication_changes(result, alternative[result.n])
        counts.append(
            {
                "n": result.n,
                "start": [side_record(side) for side in result.start],
                "steps": steps,
                "best_now": [side_record(side) for side in result.standing],
                "publication_dependent": changed,
            }
        )
        if changed:
            counts[-1]["best_now_without_publications"] = [
                side_record(side) for side in alternative[result.n].standing
            ]
    return {
        "format": VERDICTS_FORMAT,
        "read_at_main": ledger["read_at_main"],
        "read_on": ledger["read_on"],
        "counts": counts,
        "summary": tally(walks),
        "cross_check": ledger.get("cross_check", []),
        "reports": report_summaries(ledger, walks),
        "owner_decisions": {
            **owner_decisions(ledger, walks, unknown, counts),
            "refinement_chains": refinement_chains(walks),
            "key_reason_candidates": key_reasons(ledger, walks),
            "measured_identity": measured_identity(walks),
        },
        "other_items": ledger.get("other_items", []),
    }


NOT_IN_WALK = "not in the walk"


def publication_changes(default: Walk, without: Walk) -> list[dict[str, Any]]:
    """The verdicts at one count that differ when publications are not counted as reports.

    A publication the default walk records or leaves undecided drops out of the other walk;
    any other report is listed where its verdict differs.
    """
    other = {step.side.label: step for step in without.steps}
    changed = []
    for step in default.steps:
        alternative = other.get(step.side.label)
        if alternative is None:
            if step.verdict == NOT_RECORDED:
                continue
            verdict, held = NOT_IN_WALK, ""
        elif alternative.verdict == step.verdict:
            continue
        else:
            verdict, held = alternative.verdict, held_by(alternative)
        changed.append(
            {
                "report": step.side.label,
                "with_publications": step.verdict,
                "held_by_with": held_by(step),
                "without_publications": verdict,
                "held_by_without": held,
            }
        )
    return changed


def key_reasons(ledger: Ledger, walks: Sequence[Walk]) -> list[dict[str, Any]]:
    """Each key-reason candidate beside the verdict the rule gives its claim."""
    steps = {(result.n, step.side.label): step for result in walks for step in result.steps}
    found = []
    for candidate in ledger.get("key_reason_candidates", []):
        step = steps[(candidate["n"], candidate["report"])]
        found.append(
            {
                **candidate,
                "verdict": step.verdict,
                "reason": step.reason,
                "decided_against": held_by(step),
                "difference": _difference(step),
            }
        )
    return found


def measured_identity(walks: Sequence[Walk]) -> list[dict[str, Any]]:
    """Each claim whose certificate a measurement compares with another packing, beside
    what its source says it is; the measurement decides nothing."""
    found = []
    for result in walks:
        for step in result.steps:
            measured = step.side.measured
            if measured is None:
                continue
            says = (
                f"a refinement of {step.side.refines['packing_of']}'s packing "
                f"({step.side.refines['entry']})"
                if step.side.refines is not None
                else "a new packing"
                if step.side.new_packing is not None
                else "nothing stated"
            )
            found.append(
                {
                    "n": result.n,
                    "report": step.side.label,
                    "verdict": step.verdict,
                    "source_says": says,
                    **measured,
                }
            )
    return found


def kind_of(step: Step) -> str:
    """What a claim's certificate is, where its source says (`REFINEMENT`, `NEW`)."""
    if step.side.refines is not None:
        return REFINEMENT
    return NEW if step.side.new_packing is not None else UNCLASSIFIED


def _refined(step: Step) -> dict[str, str]:
    refines = step.side.refines
    return (
        {}
        if refines is None
        else {"packing_of": refines["packing_of"], "entry": refines["entry"]}
    )


def tally(walks: Sequence[Walk]) -> dict[str, int]:
    """The verdicts over every count, recorded claims split by what they are."""
    steps = [step for result in walks for step in result.steps]
    recorded = [step for step in steps if step.verdict == RECORDED]
    return {
        "counts": len(walks),
        "claims": len(steps),
        "recorded_new": sum(kind_of(step) == NEW for step in recorded),
        "recorded_new_continuing": sum(
            kind_of(step) == NEW and "continues" in (step.side.new_packing or {})
            for step in recorded
        ),
        "recorded_refinement": sum(kind_of(step) == REFINEMENT for step in recorded),
        "recorded_unclassified": sum(kind_of(step) == UNCLASSIFIED for step in recorded),
        "recorded_by_exception": sum(step.verdict == BY_EXCEPTION for step in steps),
        "not_recorded": sum(step.verdict == NOT_RECORDED for step in steps),
        "undecided": sum(step.verdict == UNDECIDED for step in steps),
    }


def _chain_root(
    step: Step, recorded: Mapping[str, Step], seen: frozenset[str] = frozenset()
) -> str:
    """The packing a recorded claim belongs to: itself, or what its refinement tightens."""
    refines = step.side.refines
    if refines is None:
        return step.side.label
    earlier = recorded.get(refines["entry"])
    if earlier is None or refines["entry"] in seen:
        return refines["entry"]
    return _chain_root(earlier, recorded, seen | {step.side.label})


def refinement_chains(walks: Sequence[Walk]) -> list[dict[str, Any]]:
    """Counts where two or more recorded refinements tighten one packing, with margins.

    A refinement's ``entry`` that names a report recorded at the same count is followed
    to that report's own packing, so a refinement of a refinement joins its chain.
    """
    chains = []
    for result in walks:
        recorded = {step.side.label: step for step in result.steps if step.verdict == RECORDED}

        groups: dict[str, list[Step]] = {}
        for step in recorded.values():
            if step.side.refines is not None:
                groups.setdefault(_chain_root(step, recorded), []).append(step)
        chains.extend(
            {
                "n": result.n,
                "packing": packing,
                "packing_of": group[0].side.refines["packing_of"]
                if group[0].side.refines
                else "",
                "refinements": [
                    {
                        "report": step.side.label,
                        "difference": _difference(step),
                        "decided_against": held_by(step),
                    }
                    for step in group
                ],
            }
            for packing, group in groups.items()
            if len(group) >= 2
        )
    return chains


def report_summaries(ledger: Ledger, walks: Sequence[Walk]) -> list[dict[str, Any]]:
    steps: dict[str, list[tuple[int, Step]]] = {}
    for result in walks:
        for step in result.steps:
            steps.setdefault(step.side.label, []).append((result.n, step))
    summaries = []
    for report in sorted(
        ledger["reports"], key=lambda item: (item["reported_at"], item["report"])
    ):
        own = steps.get(report["report"], [])
        summaries.append(
            {
                "report": report["report"],
                "url": report["url"],
                "kind": report["kind"],
                "holders": report["holders"],
                "reported_at": report["reported_at"],
                "bead": report["bead"],
                "counts": sorted(claim["n"] for claim in report["claims"]),
                "recorded": [n for n, step in own if step.verdict == RECORDED],
                "recorded_new": [
                    n for n, step in own if step.verdict == RECORDED and kind_of(step) == NEW
                ],
                "recorded_refinement": [
                    {"n": n, **_refined(step)}
                    for n, step in own
                    if step.verdict == RECORDED and kind_of(step) == REFINEMENT
                ],
                "recorded_unclassified": [
                    n
                    for n, step in own
                    if step.verdict == RECORDED and kind_of(step) == UNCLASSIFIED
                ],
                "recorded_by_exception": [n for n, step in own if step.verdict == BY_EXCEPTION],
                "not_recorded": [
                    {"n": n, "reason": step.reason, "held_by": held_by(step)}
                    for n, step in own
                    if step.verdict == NOT_RECORDED
                ],
                "undecided": [
                    {"n": n, "against": held_by(step)}
                    for n, step in own
                    if step.verdict == UNDECIDED
                ],
            }
        )
    return summaries


def _names(holders: str) -> set[str]:
    """The people or groups a credit names, without logins in parentheses."""
    plain = re.sub(r"\([^)]*\)", "", holders).replace("improved by", ",").replace(" and ", ",")
    return {name.strip().lower() for name in plain.split(",") if name.strip()}


def same_holder(first: str, second: str) -> bool:
    """Whether two credits share a holder: a tie between them is no owner decision."""
    return bool(_names(first) & _names(second))


def owner_decisions(
    ledger: Ledger, walks: Sequence[Walk], unknown: list[Any], counts: Sequence[Any]
) -> dict[str, Any]:
    holders = {report["report"]: report["holders"] for report in ledger["reports"]}
    ties: list[dict[str, Any]] = []
    early: list[dict[str, Any]] = []
    undecided: list[dict[str, Any]] = []
    for result in walks:
        for step in result.steps:
            side = step.side
            if step.reason == EQUAL:
                ties.extend(
                    {
                        "n": result.n,
                        "report": side.label,
                        "holders": side.holders,
                        "tied_with": member.label,
                        "tied_holders": member.holders,
                    }
                    for member in step.holders
                    if not same_holder(member.holders, side.holders)
                )
            if step.verdict == NOT_RECORDED and side.first_committed:
                early.extend(
                    {
                        "n": result.n,
                        "report": side.label,
                        "first_committed": side.first_committed,
                        "reported_at": side.reported_at,
                        "held_by": member.label,
                        "held_by_reported_at": member.reported_at,
                        "reason": step.reason,
                    }
                    for member in step.holders
                    if member.reported_at and side.first_committed < member.reported_at
                )
            if step.verdict == UNDECIDED:
                undecided.append(
                    {
                        "n": result.n,
                        "report": side.label,
                        "against": held_by(step),
                        "decide_by": decider(side, step.against),
                    }
                )
    dependent = [
        {
            "n": count["n"],
            **change,
            "best_now_without": " or ".join(
                f"{side['label']} {side['side']}"
                for side in count["best_now_without_publications"]
            ),
        }
        for count in counts
        for change in count["publication_dependent"]
    ]
    return {
        "exact_ties": ties,
        "first_commit_before_report": early,
        "undecided": undecided,
        "publication_dependent": dependent,
        "unknown_times": [{**item, "holders": holders[item["report"]]} for item in unknown],
    }


def _compress(counts: Iterable[int]) -> str:
    return check_standing.compress(sorted(counts)).replace(check_standing.EN_DASH, "-") or "-"


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def _report_link(label: str, url: str) -> str:
    return f"[{_cell(label)}]({url})"


def readme(ledger: Ledger, verdicts: Mapping[str, Any]) -> str:
    """The human tables: the rule, per report, per count, owner decisions, other items."""
    lines = [
        "# Upper-Bound Reports, Count by Count, in Report Order",
        "",
        f"<!-- GENERATED by {MODULE} render from ledger.yaml. Do not edit. -->",
        "",
        (
            f"Read against `main` at `{ledger['read_at_main']}` on {ledger['read_on']}. "
            f"Rendered by `python -m {MODULE} render` from [ledger.yaml](ledger.yaml), which "
            f"`gather` writes from [sources.yaml](sources.yaml), "
            f"[github-issues.json](github-issues.json) and the lanes' frozen claim records; "
            f"the verdicts are also in [ledger.json](ledger.json)."
        ),
        "",
        "## The Rule",
        "",
        "The owner's rule: “" + " ".join(ledger["rule"].split()) + "”",
        "",
        (
            "At each count the standing side starts at the record on `main`, frozen by "
            "`gather` in [starts.yaml](starts.yaml) and never read from the working tree. For "
            "n ≤ 324 it is the set of both upper lanes of the case record "
            "(`packing/frontier/n-NNN.md`): each lane's exact form where that is rational, a "
            "rigorous 90-digit interval where it is a closed form with square roots, an "
            "enclosure by exact sign change of the root a `root(...)` form names, else its "
            "printed value within one unit of its last place; with any register entry pending "
            "adoption that states a smaller bound, and only the members nothing else is "
            "decidably below. Above 324 it is the current beyond-horizon row of "
            "`frontier/source-coverage.yaml`, else the grid ⌈√n⌉. The claims are then taken in "
            "the order they reached this repository: issue, comment or pull-request creation, "
            "the update comment for a claim added to an issue later, the commit for a claim "
            "added to a pull request later, and the first commit for a publication in a "
            "watched repository that no issue reports. A claim is recorded when every number "
            "it may be is below every number every member of the standing side may be, and it "
            "becomes the standing side. A claim equal to a member (a tie: the earlier holder "
            "keeps it) or above one is not recorded, and the table names what holds the count. "
            "A comparison the printed precision cannot decide is undecided; the undecided "
            "claim stays beside the standing side until a claim is decidably below both. Exact "
            "sides come from the lanes' frozen claim records or, where `ledger.yaml` says so, "
            "from the certificate at its pinned commit; this ledger compares sides and "
            "verifies no certificate. Where a lane's claim record or an exact decision's "
            "receipt states how a claim compares with a record lane or a pending register "
            "entry, that relation decides in place of the prints while the record still "
            "prints what it read (`record_relations` in `ledger.yaml`, each naming where it "
            "was read). Sides are shown rounded up at 12 places where exact, as printed "
            "otherwise."
        ),
        "",
        "## Counts",
        "",
        *_count_lines(verdicts["summary"]),
        "",
        "## Lane Records Read",
        "",
        (
            "Exact sides marked as a lane's come from its `acquisition/claims.json` (and "
            "`algebraic-claims.json`) records, read by path from the checkout or, for a "
            "packet the tree does not hold, from the copy in "
            "[lane-claims/](lane-claims/README.md). Each commit is where the lane froze "
            "them, given as provenance; nothing reads it."
        ),
        "",
        "| Lane | Branch | Commit | Note |",
        "| --- | --- | --- | --- |",
        *[
            f"| {lane['name']} | `{lane['branch']}` | `{lane['commit']}` "
            f"| {lane.get('note', '')} |"
            for lane in ledger["lanes"]
        ],
        "",
        "## Per Report",
        "",
        (
            "| Report | Holder | Reported | Counts claimed | Recorded: new packing "
            "| Recorded: refinement (whose packing) | Recorded: unclassified "
            "| Not recorded (held by) | Undecided | Bead |"
        ),
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for summary in verdicts["reports"]:
        held: dict[str, list[int]] = {}
        for item in summary["not_recorded"]:
            held.setdefault(item["held_by"], []).append(item["n"])
        not_recorded = "; ".join(f"{_compress(ns)} ({who})" for who, ns in held.items()) or "-"
        undecided = _compress(item["n"] for item in summary["undecided"])
        whose: dict[str, list[int]] = {}
        for item in summary["recorded_refinement"]:
            whose.setdefault(f"{item['entry']}: {item['packing_of']}", []).append(item["n"])
        refined = "; ".join(f"{_compress(ns)} ({who})" for who, ns in whose.items()) or "-"
        unclassified = _compress(summary["recorded_unclassified"])
        if summary["recorded_by_exception"]:
            unclassified += f"; by exception {_compress(summary['recorded_by_exception'])}"
        lines.append(
            f"| {_report_link(summary['report'], summary['url'])} "
            f"| {_cell(summary['holders'])} | {_when(summary['reported_at'])} "
            f"| {_compress(summary['counts'])} | {_compress(summary['recorded_new'])} "
            f"| {_cell(refined)} | {unclassified} "
            f"| {_cell(not_recorded)} | {undecided} | {summary['bead'] or '-'} |"
        )
    lines += [
        "",
        "## Per Count",
        "",
        (
            "Each report at the count in report order, with its side and verdict; a verdict "
            "names what decided it and by how much."
        ),
        "",
        "| n | Record on main | Reports in order | Best now |",
        "| ---: | --- | --- | --- |",
    ]
    for count in verdicts["counts"]:
        record = "; ".join(
            f"{member['side']} ({_cell(member['label'])}; {_cell(member['holders'])})"
            for member in count["start"]
        )
        steps = []
        for step in count["steps"]:
            verdict = recorded_text(step)
            detail = step["difference"]
            if step["verdict"] != RECORDED and step["decided_against"]:
                detail = f"{detail} {', '.join(step['decided_against'])}".strip()
            if step.get("exception"):
                detail += f"; exception: {step['exception']}"
            if step.get("restates"):
                detail = f"{detail}; {step['restates']}".lstrip("; ")
            if step.get("measured"):
                detail = f"{detail}; measured: {step['measured']}".lstrip("; ")
            if step.get("key_reason_candidate"):
                detail = f"{detail}; key-reason candidate (owner decision)".lstrip("; ")
            steps.append(
                f"{_cell(step['report'])} {step['side']}: {verdict}"
                + (f" ({_cell(detail)})" if detail else "")
            )
        best = " or ".join(
            f"{_cell(side['label'])} {side['side']}" for side in count["best_now"]
        )
        if len(count["best_now"]) > 1:
            best = f"undecided: {best}"
        lines.append(f"| {count['n']} | {record} | {'; '.join(steps)} | {best} |")
    lines += _decision_lines(verdicts["owner_decisions"])
    lines += _note_lines(ledger)
    lines += [
        "",
        "## Lane Cross-Check",
        "",
        (
            "Where a lane's claim record reads another report's side in a way this ledger's "
            "claim contradicts, as `gather` found it."
        ),
        "",
        *([f"- {_cell(warning)}" for warning in verdicts["cross_check"]] or ["None."]),
    ]
    lines += [
        "",
        "## Other Items (No New Upper Bound)",
        "",
        "| Issue | Holder | Kind | Bead | Disposition |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in verdicts["other_items"]:
        lines.append(
            f"| {_report_link(item['issue'], item['url'])} | {_cell(item['holders'])} "
            f"| {_cell(item['kind'])} | {item['bead']} | {_cell(item['disposition'])} |"
        )
    lines += ["", *FOOTER]
    return "\n".join(lines) + "\n"


def _decision_lines(decisions: Mapping[str, Any]) -> list[str]:
    lines = [
        "",
        "## Owner Decisions Needed",
        "",
        "Nothing here is decided by the rule; each list is what the owner may want to rule on.",
        "",
        "### Publication in a Watched Repository",
        "",
        (
            "By default a certificate published in a watched repository, with no issue, "
            "competes as a report from its first commit. These are the counts where a verdict "
            "changes if such publications are not counted: each publication drops out of the "
            "walk, and a later report may then be recorded in its place."
        ),
        "",
    ]
    if decisions["publication_dependent"]:
        lines += [
            (
                "| n | Report | Default verdict (decided against) | Without publications "
                "(decided against) | Best now without publications |"
            ),
            "| ---: | --- | --- | --- | --- |",
        ]
        for item in decisions["publication_dependent"]:
            against = f" ({_cell(item['held_by_without'])})" if item["held_by_without"] else ""
            lines.append(
                f"| {item['n']} | {_cell(item['report'])} | {item['with_publications']} "
                f"({_cell(item['held_by_with']) or '-'}) | {item['without_publications']}"
                f"{against} | {_cell(item['best_now_without'])} |"
            )
    else:
        lines.append("None.")
    lines += [
        "",
        "### Key-Reason Candidates",
        "",
        (
            "Claims an argument says have a key reason to be recorded. The rule does not "
            "apply it: the verdict is the rule's, and the owner decides."
        ),
        "",
        *_key_reason_lines(decisions["key_reason_candidates"]),
        "",
        "### Measured Identity Against the Source's Word",
        "",
        (
            "Claims whose certificate a measurement compares with another packing. The "
            "measurement is recorded beside what the source says and decides nothing; the "
            "owner decides the credit."
        ),
        "",
        *_measured_lines(decisions["measured_identity"]),
        "",
        "### Refinement Chains",
        "",
        (
            "Counts where two or more refinements of one packing are each recorded, in "
            "report order; the rule records each, and each margin is against the side it "
            "was decided against."
        ),
        "",
        *_chain_lines(decisions["refinement_chains"]),
        "",
        "### Exact Ties Between Different Holders",
        "",
        "Not recorded by the rule, since the earlier holder keeps a tie.",
        "",
    ]
    if decisions["exact_ties"]:
        lines += [
            "| Report (holder) | Tied with | Counts | Tied holders |",
            "| --- | --- | --- | --- |",
        ]
        groups: dict[tuple[str, str, str], list[Any]] = {}
        for item in decisions["exact_ties"]:
            key = (item["report"], item["holders"], item["tied_with"])
            groups.setdefault(key, []).append(item)
        for (report, holders, tied), items in groups.items():
            names = ", ".join(dict.fromkeys(item["tied_holders"] for item in items))
            lines.append(
                f"| {_cell(report)} ({_cell(holders)}) | {_cell(tied)} "
                f"| {_compress(item['n'] for item in items)} | {_cell(names)} |"
            )
    else:
        lines.append("None.")
    lines += [
        "",
        "### Certificate Committed Before the Report That Holds the Count",
        "",
        (
            "A claim not recorded whose certificate's first commit precedes the time the "
            "holding report reached this repository."
        ),
        "",
    ]
    if decisions["first_commit_before_report"]:
        lines += [
            (
                "| n | Report | First committed | Reported | Held by | Held by, reported "
                "| Reason |"
            ),
            "| ---: | --- | --- | --- | --- | --- | --- |",
        ]
        for item in decisions["first_commit_before_report"]:
            lines.append(
                f"| {item['n']} | {_cell(item['report'])} | {_when(item['first_committed'])} "
                f"| {_when(item['reported_at'])} | {_cell(item['held_by'])} "
                f"| {_when(item['held_by_reported_at'])} | {item['reason']} |"
            )
    else:
        lines.append("None.")
    lines += ["", "### Undecided Comparisons", ""]
    if decisions["undecided"]:
        lines += [
            "| n | Report | Against | What would decide it |",
            "| ---: | --- | --- | --- |",
        ]
        for item in decisions["undecided"]:
            lines.append(
                f"| {item['n']} | {_cell(item['report'])} | {_cell(item['against'])} "
                f"| {_cell(item['decide_by'])} |"
            )
    else:
        lines.append("None.")
    lines += ["", "### Claims of Unknown Time", "", "Kept out of the walk.", ""]
    if decisions["unknown_times"]:
        lines += ["| n | Report | Holder |", "| ---: | --- | --- |"]
        for item in decisions["unknown_times"]:
            lines.append(
                f"| {item['n']} | {_cell(item['report'])} | {_cell(item['holders'])} |"
            )
    else:
        lines.append("None.")
    return lines


def _key_reason_lines(items: Sequence[Mapping[str, Any]]) -> list[str]:
    if not items:
        return ["None."]
    lines = [
        "| n | Report | Rule's verdict | Argument | Proposed as |",
        "| ---: | --- | --- | --- | --- |",
    ]
    for item in items:
        verdict = f"{item['verdict']} ({item['difference']} {item['decided_against']})".strip()
        lines.append(
            f"| {item['n']} | {_cell(item['report'])} | {_cell(verdict)} "
            f"| {_cell(item['argument'])} | {_cell(item.get('proposed_as', '-'))} |"
        )
    return lines


def _measured_lines(items: Sequence[Mapping[str, Any]]) -> list[str]:
    if not items:
        return ["None."]
    lines = [
        "| n | Report | Verdict | The source says | Measured against | Finding | Measured by |",
        "| ---: | --- | --- | --- | --- | --- | --- |",
    ]
    lines.extend(
        f"| {item['n']} | {_cell(item['report'])} | {item['verdict']} "
        f"| {_cell(item['source_says'])} | {_cell(item['against'])} "
        f"| {_cell(item['finding'])} | {_cell(item['source'])} |"
        for item in items
    )
    return lines


def _chain_lines(chains: Sequence[Mapping[str, Any]]) -> list[str]:
    if not chains:
        return ["None."]
    lines = ["| n | Packing | Refinements in order |", "| ---: | --- | --- |"]
    for chain in chains:
        steps = "; ".join(
            f"{item['report']} {item['difference']} {item['decided_against']}".strip()
            for item in chain["refinements"]
        )
        packing = f"{chain['packing']} ({chain['packing_of']})" if chain["packing_of"] else ""
        lines.append(
            f"| {chain['n']} | {_cell(packing or chain['packing'])} | {_cell(steps)} |"
        )
    return lines


def _count_lines(summary: Mapping[str, int]) -> list[str]:
    continuing = summary["recorded_new_continuing"]
    return [
        (
            f"{summary['claims']} claims at {summary['counts']} counts. Recorded: "
            f"{summary['recorded_new']} new packings (of which {continuing} continue another "
            f"holder's or the reporter's own arrangement), {summary['recorded_refinement']} "
            f"refinements of a standing packing, {summary['recorded_unclassified']} that no "
            f"source classifies; {summary['recorded_by_exception']} recorded by exception; "
            f"{summary['not_recorded']} not recorded; {summary['undecided']} undecided."
        ),
        "",
        (
            "A refinement is the same configuration with a tighter certificate (a padding "
            "reduction, an exact-contact refinement, an exact attainment), as a source says; "
            "a new packing is one its source says is new, including one a continued search "
            "found from another arrangement. The rule records both; the register credits a "
            "refinement as a regularization of the packing it tightens."
        ),
    ]


def recorded_text(step: Mapping[str, Any]) -> str:
    """A recorded verdict, with what the certificate is where a source says."""
    packing = step.get("packing")
    if step["verdict"] != RECORDED or packing is None:
        return str(step["verdict"])
    if packing["kind"] == REFINEMENT:
        return (
            f"recorded, a refinement of {packing['packing_of']}'s packing ({packing['entry']})"
        )
    if "continues" in packing:
        return f"recorded (new packing, continuing {packing['continues']})"
    return "recorded (new packing)"


def _note_lines(ledger: Ledger) -> list[str]:
    """Each report's note and its claims' notes, one row per note."""
    lines = [
        "",
        "## Notes on Reports and Claims",
        "",
        "From `ledger.yaml`; a note that several claims share is one row.",
        "",
        "| Report | Counts | Note |",
        "| --- | --- | --- |",
    ]
    for report in ledger["reports"]:
        note = report.get("note")
        if note:
            lines.append(f"| {_cell(report['report'])} | all | {_cell(note)} |")
        notes: dict[str, list[int]] = {}
        for claim in report["claims"]:
            text = claim.get("note")
            if text:
                notes.setdefault(text, []).append(claim["n"])
        for note, ns in notes.items():
            lines.append(f"| {_cell(report['report'])} | {_compress(ns)} | {_cell(note)} |")
    return lines


def json_text(value: Any) -> str:
    """JSON in the retained layout (`sqpack.retained_json`), non-ASCII kept."""
    return retained_dumps(value, ensure_ascii=False)


def inert_relations(ledger: Ledger, starts: Mapping[int, Sequence[Side]]) -> list[str]:
    """Every record relation that reads no member of its count's start: a lane, value or
    form the starts never froze, or a register entry they do not hold. Such a relation
    decides nothing (`_frozen_relation`), so it is refused rather than kept."""
    found: list[str] = []
    for report in ledger["reports"]:
        for claim in report["claims"]:
            prints = {
                read for member in starts.get(claim["n"], ()) for read in member.record_prints
            }
            found.extend(
                f"{report['report']} n = {claim['n']}: the record relation to "
                f"{relation['lane']} at {relation['value']!r} reads no member of the start"
                for relation in claim.get("record_relations", [])
                if (relation["lane"], relation["value"], relation["exact_form"]) not in prints
            )
    return found


def load_walk(directory: Path) -> tuple[Ledger, dict[int, list[Side]]]:
    """The ledger and the starts ``gather`` froze, refused when a count has no start or a
    record relation reads no member of its start (`inert_relations`)."""
    ledger = load_ledger(directory)
    starts = load_starts(directory, ledger["read_at_main"])
    missing = sorted(set(counts_of(ledger)) - set(starts))
    _require(not missing, f"{STARTS} has no start at n = {missing}")
    inert = inert_relations(ledger, starts)
    _require(not inert, "; ".join(inert))
    return ledger, starts


def rendered(directory: Path) -> dict[str, str]:
    """The two rendered files' text, from the ledger and the starts ``gather`` froze; the
    records on the tree are not read (`tree_drift` compares them)."""
    ledger, starts = load_walk(directory)
    verdicts = evaluate(ledger, starts)
    return {VERDICTS: json_text(verdicts), README: readme(ledger, verdicts)}


def render(directory: Path, *, check: bool = False) -> list[str]:
    """Write the rendered files, or with ``check`` name those that would change."""
    changed = []
    for name, text in rendered(directory).items():
        path = directory / name
        if path.exists() and path.read_text(encoding="utf-8") == text:
            continue
        changed.append(name)
        if not check:
            with atomic_output_file(path) as temporary:
                Path(temporary).write_text(text, encoding="utf-8")
    return changed


# --------------------------------------------------------------------------- gather


Fetch = Callable[[str], Any]


def _gh_api(path: str) -> Any:
    shown_ = subprocess.run(("gh", "api", path), capture_output=True, text=True, check=True)
    return json.loads(shown_.stdout)


def github_item(source: Mapping[str, Any], api: Fetch) -> dict[str, Any]:
    """One report's GitHub coordinates: number, author, creation time, state, title.

    A comment carries its own author and time, and its issue's state and title.
    """
    base = f"repos/{GITHUB_REPOSITORY}"
    if "comment" in source:
        item = api(f"{base}/issues/comments/{source['comment']}")
        parent = api(f"{base}/issues/{source['issue']}")
        return {
            "report": source["report"],
            "kind": "comment",
            "number": int(source["issue"]),
            "comment_id": int(source["comment"]),
            "url": item["html_url"],
            "author": item["user"]["login"],
            "created_at": item["created_at"],
            "issue_state": parent["state"],
            "issue_closed_at": parent.get("closed_at"),
            "issue_title": parent["title"],
        }
    kind, path = ("pull-request", "pulls") if "pull" in source else ("issue", "issues")
    number_ = int(source.get("pull", source.get("issue", 0)))
    item = api(f"{base}/{path}/{number_}")
    return {
        "report": source["report"],
        "kind": kind,
        "number": number_,
        "url": item["html_url"],
        "author": item["user"]["login"],
        "created_at": item["created_at"],
        "state": item["state"],
        "closed_at": item.get("closed_at"),
        "title": item["title"],
    }


def record_path(mapping: Mapping[str, Any]) -> str:
    """A lane record's repository-relative path in its packet."""
    return f"packing/resources/web/{mapping['packet']}/acquisition/{mapping['record']}"


def lane_record(directory: Path, mapping: Mapping[str, Any]) -> Any:
    """A lane's claim record, by path: the packet's in the checkout where it is there, else
    the copy retained under ``directory``'s `LANE_CLAIMS`. No commit is read (OR-18)."""
    on_tree = REPO / record_path(mapping)
    retained = directory / LANE_CLAIMS / mapping["lane"] / mapping["packet"] / mapping["record"]
    path = on_tree if on_tree.is_file() else retained
    _require(
        path.is_file(),
        f"{record_path(mapping)} is in neither the checkout nor {LANE_CLAIMS}/: retain a "
        "copy with its provenance in that directory's README",
    )
    return json.loads(path.read_text(encoding="utf-8"))


def _lane_claim(
    row: Mapping[str, Any], mapping: Mapping[str, Any], where: str, rounding: str, url: str
) -> Claim:
    if "side_decimal" in row:
        case = row.get("case") or {}
        claim: Claim = {
            "n": int(row["n"]),
            "printed": str(row["side_decimal"]),
            "rounding": "unstated",
            "first_committed": str(row["first_committed"]),
            "note": f"algebraic side of degree {row['degree']}; the print is the lane's",
        }
        relations: list[RecordRelation] = [
            {
                "lane": lane,
                "relation": str(case[f"{lane}_relation"]),
                "value": str(case[f"{lane}_value"]),
                "exact_form": str(case.get(f"{lane}_exact_form") or ""),
                "read_from": where,
            }
            for lane in ("reported", "verified")
            if case.get(f"{lane}_relation") in (BELOW, ABOVE, EQUAL)
        ]
        if relations:
            claim["record_relations"] = relations
        return claim
    offered = str(row["offered_side"])
    claim = {
        "n": int(row["n"]),
        "printed": offered,
        "rounding": "exact" if "/" in offered else rounding,
        "exact": str(row["exact_side"]),
        "exact_from": where,
        "first_committed": str(row["first_committed"]),
    }
    if mapping.get("printed_in_note") and row.get("printed_in") not in (None, "", url):
        claim["note"] = f"printed in {row['printed_in']}"
    return claim


def record_key(mapping: Mapping[str, Any]) -> str:
    return f"{mapping['lane']}:{mapping['packet']}/{mapping['record']}"


def lane_claims(
    directory: Path,
    mapping: Mapping[str, Any],
    lanes: Mapping[str, Mapping[str, Any]],
    url: str,
    rounding: str,
    *,
    taken: dict[str, set[int]] | None = None,
) -> list[Claim]:
    """The claims one lane record gives a report: its rows printed in it, or those named.

    ``taken`` collects every row of every record read, and the rows some report took, so
    ``gather`` can refuse a row no report claims (`unclaimed_rows`). The lane's branch and
    commit are written beside each claim as provenance.
    """
    lane = lanes[mapping["lane"]]
    path = record_path(mapping)
    record = lane_record(directory, mapping)
    where = f"{path} at {lane['branch']}@{lane['commit']}"
    wanted = {int(n) for n in mapping.get("counts") or []}
    rows = [row for row in record["results"] if _selected(row, mapping, wanted, url)]
    if wanted:
        found = {int(row["n"]) for row in rows}
        _require(found == wanted, f"{path}: no rows for {sorted(wanted - found)}")
    if taken is not None:
        key = record_key(mapping)
        taken.setdefault(f"{key} rows", set()).update(
            int(row["n"]) for row in record["results"]
        )
        taken.setdefault(key, set()).update(int(row["n"]) for row in rows)
        taken[key].update(int(n) for n in mapping.get("not_ours") or [])
    return [_lane_claim(row, mapping, where, rounding, url) for row in rows]


def unclaimed_rows(taken: Mapping[str, set[int]]) -> list[str]:
    """Each lane record's rows that no report took and no mapping names as ``not_ours``."""
    return [
        f"{key}: rows {sorted(rows - taken.get(key, set()))} are claimed by no report; "
        "map them to one or list them in a mapping's not_ours"
        for key, rows in sorted(
            (name.removesuffix(" rows"), rows)
            for name, rows in taken.items()
            if name.endswith(" rows")
        )
        if rows - taken.get(key, set())
    ]


def _selected(
    row: Mapping[str, Any], mapping: Mapping[str, Any], wanted: set[int], url: str
) -> bool:
    """A lane row a report takes: every row, the counts named, or the rows printed in it."""
    if mapping.get("all"):
        return True
    if wanted:
        return int(row["n"]) in wanted
    return str(row.get("printed_in", "")) == url


def _merge(transcribed: Sequence[Claim], from_lanes: Sequence[Claim]) -> list[Claim]:
    """Transcribed fields win; a lane adds the exact side and the commit time. Record
    relations are kept from both, the lane's first."""
    merged: dict[int, Claim] = {claim["n"]: cast("Claim", dict(claim)) for claim in from_lanes}
    for claim in transcribed:
        lane = merged.get(claim["n"])
        if lane is None:
            merged[claim["n"]] = claim
            continue
        both = [*lane.get("record_relations", []), *claim.get("record_relations", [])]
        merged[claim["n"]] = cast("Claim", {**lane, **claim})
        if both:
            merged[claim["n"]]["record_relations"] = both
    return [merged[n] for n in sorted(merged)]


def _later(claim: Claim, reported_at: str) -> Claim:
    """A pull request's claim committed after it was opened arrived with that commit."""
    committed = claim.get("first_committed", "")
    if committed > reported_at and "reported_at" not in claim:
        claim = cast("Claim", {**claim, "reported_at": committed})
    return claim


def gather(
    directory: Path,
    *,
    snapshot: bool = False,
    refresh_starts: bool = False,
    api: Fetch = _gh_api,
) -> list[str]:
    """Write ``github-issues.json`` and ``ledger.yaml``, and ``starts.yaml`` when there is
    none or ``refresh_starts`` asks; return the cross-check warnings, which ``ledger.yaml``
    keeps too.

    A ``starts.yaml`` already frozen at ``read_at_main`` is kept as it is, so that reading a
    lane again never moves a start, and a ledger with a count it holds no start for is
    refused. Writing the starts reads the checkout's records, so it is run from a checkout
    of ``read_at_main``; nothing here resolves that commit (OR-18), and ``check --tree``
    reports where the checkout's records give other starts.
    """
    sources = load_yaml(directory / SOURCES)
    _require(sources.get("format") == SOURCES_FORMAT, f"{SOURCES} format")
    read_at_main = str(sources["read_at_main"])
    keep = (directory / STARTS).is_file() and not refresh_starts
    lanes = {lane["name"]: lane for lane in sources["lanes"]}
    if snapshot:
        github = json.loads((directory / SNAPSHOT).read_text(encoding="utf-8"))["items"]
    else:
        github = [
            github_item(source, api)
            for source in sources["reports"]
            if "issue" in source or "pull" in source
        ]
    by_report = {item["report"]: item for item in github}
    reports: list[Report] = []
    taken: dict[str, set[int]] = {}
    for source in sources["reports"]:
        item = by_report.get(source["report"])
        if item is not None:
            kind, url, reported_at = item["kind"], item["url"], item["created_at"]
        else:
            kind, url, reported_at = "publication", source["url"], source["reported_at"]
        rounding = str(source.get("rounding", "up"))
        from_lanes = [
            claim
            for mapping in source.get("lanes", [])
            for claim in lane_claims(directory, mapping, lanes, url, rounding, taken=taken)
        ]
        claims = _merge(source.get("claims", []), from_lanes)
        if kind == "pull-request":
            claims = [_later(claim, reported_at) for claim in claims]
        report: Report = {
            "report": source["report"],
            "url": url,
            "kind": kind,
            "holders": source["holders"],
            "reported_at": reported_at,
            "bead": source.get("bead", ""),
            "claims": claims,
        }
        if source.get("note"):
            report["note"] = source["note"]
        reports.append(report)
    unclaimed = unclaimed_rows(taken)
    _require(not unclaimed, "; ".join(unclaimed))
    ledger: Ledger = {
        "format": LEDGER_FORMAT,
        "read_at_main": read_at_main,
        "read_on": sources["read_on"],
        "rule": sources["rule"],
        "lanes": sources["lanes"],
        "reports": reports,
        "exceptions": sources.get("exceptions", []),
        "key_reason_candidates": sources.get("key_reason_candidates", []),
        "other_items": sources.get("other_items", []),
    }
    warnings = cross_check(directory, ledger, sources)
    ledger["cross_check"] = warnings
    found = problems(ledger)
    _require(not found, "; ".join(found))
    texts = [
        (SNAPSHOT, json_text({"format": SNAPSHOT_FORMAT, "items": github})),
        (LEDGER, yaml.safe_dump(ledger, sort_keys=False, allow_unicode=True, width=88)),
    ]
    if keep:
        missing = sorted(set(counts_of(ledger)) - set(load_starts(directory, read_at_main)))
        _require(
            not missing,
            f"{STARTS} has no start at n = {missing}: gather --refresh-starts from a checkout "
            f"of read_at_main {read_at_main[:12]}",
        )
    else:
        members = tree_members(counts_of(ledger), names=display_names(sources))
        starts = starts_document(read_at_main, members)
        texts.append(
            (STARTS, yaml.safe_dump(starts, sort_keys=False, allow_unicode=True, width=88))
        )
    for name, text in texts:
        with atomic_output_file(directory / name) as temporary:
            Path(temporary).write_text(text, encoding="utf-8")
    return warnings


def _pending_owner(
    pending: Mapping[str, Any],
    n: int,
    claims: Mapping[tuple[str, int], Claim],
    reports: Sequence[Report],
) -> Report | None:
    """The ledger report a lane's ``pending`` row names at count ``n``, by its address.

    A register entry (``T-NNN``) is part of the record, not of the ledger, and names none.
    """
    url = str(pending.get("url", ""))
    label = str(pending.get("report", ""))
    if label.startswith("T-") or not url.startswith("https://github.com/"):
        return None
    for report in reports:
        if report["url"] == url and report["kind"] != "comment":
            return report
    for report in reports:
        commented = report["kind"] == "comment" and report["url"].split("#")[0] == url
        if commented and ("comment" in label or "refinement" in label):
            return report
    for report in reports:
        repository = report["url"].split("/tree/")[0] + "/"
        published = report["kind"] == "publication" and url.startswith(repository)
        if published and (report["report"], n) in claims:
            return report
    return None


def cross_check(directory: Path, ledger: Ledger, sources: Mapping[str, Any]) -> list[str]:
    """Where a lane read another report's side in a way this ledger's claim contradicts."""
    claims = {
        (report["report"], claim["n"]): claim
        for report in ledger["reports"]
        for claim in report["claims"]
    }
    warnings: list[str] = []
    seen: set[str] = set()
    for source in sources["reports"]:
        for mapping in source.get("lanes", []):
            key = f"{mapping['lane']}/{mapping['packet']}/{mapping['record']}"
            if key in seen:
                continue
            seen.add(key)
            for row in lane_record(directory, mapping)["results"]:
                n = int(row["n"])
                for pending in row.get("pending", []):
                    owner = _pending_owner(pending, n, claims, ledger["reports"])
                    if owner is not None:
                        claim = claims.get((owner["report"], n))
                        warnings.extend(_disagreement(key, n, owner, claim, pending))
    return warnings


def _disagreement(
    key: str, n: int, owner: Report, claim: Claim | None, pending: Mapping[str, Any]
) -> list[str]:
    """A lane's reading of ``owner`` at ``n`` that the ledger's claim cannot both satisfy."""
    where = f"{key} n={n} reads {pending.get('report')}"
    if claim is None:
        return [f"{where}, which this ledger does not list at n = {n}"]
    ours = claim_span(claim)
    if "exact_side" in pending:
        theirs = exact_span(number(str(pending["exact_side"])))
        lane = f"exactly {pending['exact_side']}"
    else:
        theirs = printed_side(
            str(pending.get("printed")), lane_rounding(str(pending.get("rounding")))
        )
        lane = f"{pending.get('printed')} ({pending.get('rounding')})"
    if below(ours, theirs) or below(theirs, ours):
        shown_ = claim.get("exact", claim["printed"])
        held = f"{shown_} ({claim['rounding']}) for {owner['report']}"
        return [f"{where} as {lane}; this ledger has {held}"]
    return []


def lane_rounding(rounding: str) -> str:
    """A lane's printed rounding, refused unless it is one of `ROUNDINGS`."""
    _require(rounding in ROUNDINGS, f"a lane reads a print with unknown rounding {rounding!r}")
    return rounding


# --------------------------------------------------------------------------- command


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="action", required=True)
    for name in ("gather", "render", "check"):
        command = sub.add_parser(name)
        command.add_argument("directory", type=Path, nargs="?", default=DEFAULT_DIRECTORY)
        if name == "gather":
            command.add_argument("--snapshot", action="store_true")
            command.add_argument(
                "--refresh-starts",
                action="store_true",
                help=f"read the starts from the checkout again, replacing {STARTS}",
            )
        if name == "check":
            command.add_argument(
                "--tree",
                action="store_true",
                help="also report where today's records give other starts (never fails)",
            )
        if name == "render":
            mode = command.add_mutually_exclusive_group()
            mode.add_argument(
                "--check", action="store_true", help="fail if a file would change"
            )
            mode.add_argument("--write", action="store_true", help="write them (the default)")
    args = parser.parse_args(argv)
    try:
        return _run(args)
    except LedgerError as error:
        message = " ".join(str(error).split())
        print(f"FAIL  {args.action}: {message}", file=sys.stderr)
        return 1


def _run(args: argparse.Namespace) -> int:
    directory = cast("Path", args.directory).resolve()
    if args.action == "gather":
        kept = (directory / STARTS).is_file() and not args.refresh_starts
        warnings = gather(directory, snapshot=args.snapshot, refresh_starts=args.refresh_starts)
        for warning in warnings:
            print(f"WARN  {warning}")
        wrote = (
            f"wrote {SNAPSHOT} and {LEDGER}, kept {STARTS}"
            if kept
            else f"wrote {SNAPSHOT}, {LEDGER} and {STARTS}"
        )
        print(f"{wrote}; {len(warnings)} cross-check warnings")
        return 0
    if args.action == "check":
        ledger, starts = load_walk(directory)
        claims = sum(len(report["claims"]) for report in ledger["reports"])
        print(
            f"OK: {len(ledger['reports'])} reports, {claims} claims, {len(starts)} starts, "
            "each member's span recomputed from its stored inputs, each record relation "
            "read against its start"
        )
        if args.tree:
            drift = tree_drift(directory)
            for line in drift:
                print(f"DRIFT  {line}")
            print(f"{len(drift)} counts where today's records give another start (not a gate)")
        return 0
    changed = render(directory, check=args.check)
    if args.check and changed:
        print(f"FAIL  would change: {', '.join(changed)}", file=sys.stderr)
        return 1
    print("up to date" if not changed else f"wrote {', '.join(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
