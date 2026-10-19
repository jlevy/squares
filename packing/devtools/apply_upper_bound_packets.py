#!/usr/bin/env python3
# ruff: noqa: RUF001 -- this module writes register prose, whose typography uses curly
# apostrophes, the multiplication sign and the corpus's other non-ASCII marks.
"""Carry the September 2026 parallel upper bounds into the Frontier records.

`devtools.upper_bound_packets` retains Francisco Couzo's 49 packings, Joost de Winter's
``s(211)`` packing and Griffin Casson's 39 packings, and certifies the first two here;
it also retains the seven packings Couzo lowered on 3 October (T-092), which take those
counts from his earlier ones (T-056).
This tool writes what those packets establish into the records, and is idempotent: a
second run writes nothing, and ``--check`` reports any record that differs from what it
would write.

For each certified case it sets ``reported_upper_bound`` to the source's printed side,
``verified_upper_bound`` to the receipt's verified value with its exact fraction, and
``conjectured_optimum`` to null (neither source conjectures optimality). It drops the
upper-bound blocker the earlier report carried, and where the certified ceiling trails
the printed side it records a ``replay-failure`` conflict and a ``mathematics`` blocker
instead. It adds the evidence, resources and, at the counts both repositories report,
priority notes stating Casson's and Couzo's dates and values, and never inferring that
either packing derives from the other; at ``n = 103``, which issue #227 named before
Casson's commit, the body also gives the issue's date. In the body it points the opening
sentence at the new side, removes or rewrites the ceiling section, and rewrites the
packing section, keeping the earlier packing's paragraph under a heading of its own.

In ``source-coverage.yaml`` it keeps the certified sources' ``selected_overrides`` and
the ``superseded_reports`` they displace (UnitSquare's at five counts, and all of
Casson's) equal to the packets.

Usage, from ``packing/``:
    uv run --frozen --all-extras --group dev python -m devtools.apply_upper_bound_packets
    uv run --frozen --all-extras --group dev python -m \
        devtools.apply_upper_bound_packets --check
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

import yaml
from strif import atomic_write_text

from devtools import upper_bound_packets as packets
from devtools.check_source_coverage import parse_kingbird
from devtools.generate_frontier_case import (
    MONTH_NAMES,
    display_first_party_upper,
    display_gap,
    load_unitsquare_release,
)
from devtools.migrate_math import markdown_math
from devtools.state_ai_assistance import state
from sqpack.assurance import bounds_agree_at_declared_precision
from sqpack.kingbird_catalogue import INTAKE_CATALOGUE_HTML
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
COVERAGE = FRONTIER / "source-coverage.yaml"
EVIDENCE = FRONTIER / "evidence.yaml"
#: The capture this intake read, not whichever one is current: the sides it records as
#: replaced are the ones the records held on 2026-09-29, and a later capture of the page
#: must not rewrite them.
CATALOGUE = ROOT / INTAKE_CATALOGUE_HTML
INTAKE = "2026-09-29"
ISSUE = "https://github.com/jlevy/squares/issues/227"
#: The counts issue #227 names, in its author's words "the 102 and 103 problems".
ISSUE_COUNTS = frozenset({102, 103})

FRANCISCOUZO, DE_WINTER, CASSON = packets.FRANCISCOUZO, packets.DE_WINTER, packets.CASSON


@dataclass(frozen=True, slots=True)
class Registration:
    """How one certified source is cited in the records."""

    source: packets.Source
    coverage_id: str
    report: str
    replay: str
    result: str
    #: How the body names the author and the repository.
    author: str
    repository: str
    #: The method-distinct second route, the source's printed pose decided by intervals.
    interval_replay: str
    #: The day this intake read its packet into the records.
    intake: str = INTAKE


REGISTRATIONS = (
    Registration(
        source=FRANCISCOUZO,
        coverage_id="franciscouzo-square-packing-2026",
        report="E-franciscouzo-2026-09-27-report",
        replay="E-franciscouzo-2026-09-27-exact-replay",
        result="T-056",
        author="Francisco Couzo",
        repository="square-packing",
        interval_replay="E-franciscouzo-2026-09-27-interval-replay",
    ),
    Registration(
        source=DE_WINTER,
        coverage_id="de-winter-square-packing-211-2026",
        report="E-n211-de-winter-report",
        replay="E-n211-de-winter-exact-replay",
        result="T-057",
        author="Joost de Winter",
        repository="square-packing-211",
        interval_replay="E-n211-de-winter-interval-replay",
    ),
    # Couzo's next revision, at the seven counts whose side it lowered. A registration
    # listed later takes a count from an earlier one, which stays its previous packing.
    Registration(
        source=packets.FRANCISCOUZO_2026_10_03,
        coverage_id="franciscouzo-square-packing-2026-10-03",
        report="E-franciscouzo-2026-10-03-report",
        replay="E-franciscouzo-2026-10-03-exact-replay",
        result="T-092",
        author="Francisco Couzo",
        repository="square-packing",
        interval_replay="E-franciscouzo-2026-10-03-interval-replay",
        intake="2026-10-05",
    ),
)
CASSON_COVERAGE_ID = "casson-square-packing-2026"
CASSON_REPORT = "E-casson-2026-09-23-report"
UNITSQUARE_COVERAGE_ID = "unitsquare-release1"
#: The evidence an earlier reported upper bound cited; a blocker citing one of these is
#: the gap blocker that bound carried, and goes when the new certificate closes the gap.
EARLIER_UPPER = frozenset(
    {
        "E-kingbird-upper-register",
        "E-kingbird-grid-completeness",
        "E-unitsquare-release1-report",
    }
)
PREVIOUS_HEADING = "### The previous best known packing"
CEILING_HEADING = "## The verified upper bound is a ceiling"


@dataclass(frozen=True, slots=True)
class Plan:
    """Everything one case record takes from the packets."""

    n: int
    registration: Registration
    case: Mapping[str, Any]
    receipt: Mapping[str, Any]
    casson: Mapping[str, Any] | None
    #: The earlier registration's plan at this count, which this one replaces.
    previous: Plan | None = None

    @property
    def chain(self) -> list[Plan]:
        """Every plan at this count, earliest first, ending with this one."""
        return [*(self.previous.chain if self.previous else []), self]

    @property
    def side(self) -> str:
        return str(self.case["side"])

    @property
    def verified(self) -> str:
        return str(self.receipt["verified_value"])

    @property
    def trailing(self) -> bool:
        """Whether the verified value does not agree with the printed side by the record's
        own rule, which allows one unit of the last place and no more."""
        return not bounds_agree_at_declared_precision(
            {"value": self.side, "exact_form": None},
            {"value": self.verified, "exact_form": str(self.receipt["exact_form"])},
        )


def plans() -> list[Plan]:
    """One plan per certified count, the latest registration's, by `n`.

    Where a later registration reports a count an earlier one did, its plan keeps the
    earlier one as `previous`, and `apply_case` writes that one first.
    """
    casson = packets.cases(CASSON)
    latest: dict[int, Plan] = {}
    for registration in REGISTRATIONS:
        receipts = packets.certification(registration.source)
        for n, case in sorted(packets.cases(registration.source).items()):
            latest[n] = Plan(n, registration, case, receipts[n], casson.get(n), latest.get(n))
    return [latest[n] for n in sorted(latest)]


# --------------------------------------------------------------------------------------
# Words
# --------------------------------------------------------------------------------------


def _when(timestamp: str) -> datetime:
    return datetime.fromisoformat(timestamp)


def day(timestamp: str) -> str:
    """``2026-09-26T22:21:57Z`` as ``26 September 2026``."""
    moment = _when(timestamp)
    return f"{moment.day} {MONTH_NAMES[moment.month - 1]} {moment.year}"


def _decimal(value: Fraction, places: int) -> str:
    """``value`` to ``places`` decimals, marked with an ellipsis unless that is exact."""
    with localcontext() as context:
        context.prec = 80
        exact = Decimal(value.numerator) / Decimal(value.denominator)
        shown = exact.quantize(Decimal(1).scaleb(-places))
    if Fraction(shown) == value:
        return format(shown.normalize(), "f")
    return f"{shown:f}…"


def difference(larger: str, smaller: str) -> str:
    """``larger - smaller`` at 28 digits, a small one in the receipts' lowercase ``e`` form.

    Decimal writes ``2E-15``; the receipts beside it write ``1.124e-15``.
    """
    with localcontext() as context:
        context.prec = 28
        return str(Decimal(larger) - Decimal(smaller)).replace("E", "e")


def _link(source: packets.Source) -> str:
    return f"../resources/web/{source.directory}/README.md"


# --------------------------------------------------------------------------------------
# Front matter
# --------------------------------------------------------------------------------------


def _block(name: str, value: object) -> str:
    dumped = yaml.safe_dump({name: value}, allow_unicode=True, sort_keys=False, width=100)
    return "".join("  " + line + "\n" for line in dumped.splitlines())


def set_block(front: str, name: str, value: object) -> str:
    """Replace one top-level ``packing`` key, however its value is laid out."""
    pattern = re.compile(rf"^  {name}:.*\n(?:(?:    |  - ).*\n)*", re.MULTILINE)
    if not pattern.search(front):
        raise ValueError(f"no {name} in the front matter")
    return pattern.sub(lambda _match: _block(name, value), front, count=1)


def reported_upper(plan: Plan, current: Mapping[str, Any]) -> dict[str, Any]:
    registration = plan.registration
    return {
        "value": plan.side,
        "exact_form": None,
        "algebraic_degree": None,
        "minimal_polynomial": None,
        "analytically_optimized": None,
        # The catalogue never described this packing, so it states nothing about its
        # rigidity. At all 50 counts it states nothing about its own packing either, which
        # is what check_source_coverage holds the field to.
        "catalogue_rigid": "not-stated",
        "construction_method": "unknown",
        "tilt_angles_deg": None,
        "found_by": [registration.author],
        "found_year": 2026,
        "improved_by": [],
        "catalogue_pictured": current["catalogue_pictured"],
        "source_key": registration.source.key,
        "source_date": plan.case["current_since_authored_utc"][:10],
        "retrieved_date": registration.source.retrieved,
        "witnesses": [f"W-known-best-n{plan.n:03d}"],
        "evidence": [registration.report],
    }


def conflict(plan: Plan) -> dict[str, Any]:
    registration = plan.registration
    certified = str(plan.receipt["certified_side_decimal"])[: len(plan.side) + 5]
    return {
        "kind": "replay-failure",
        "detail": (
            f"The exact rational replay of the source's pose certifies s({plan.n}) <= "
            f"{plan.verified} (the certificate's side is {certified}...), "
            f"{plan.receipt['units_above_printed']} units of the fifteenth decimal above the "
            f"printed side {plan.side}, so the printed side is not certified here. The "
            "interval replay of the printed pose, with each angle's true cosine and sine, "
            "finds the pose's own extent above the printed side as well, so the gap is the "
            "source's pose and not the rounding."
        ),
        "evidence": [registration.replay, registration.interval_replay, registration.report],
    }


def blocker(plan: Plan) -> dict[str, Any]:
    registration = plan.registration
    return {
        "kind": "mathematics",
        "detail": (
            f"verified_upper_bound is {registration.replay}'s certified side rounded up, "
            f"{plan.verified}, which trails the report {plan.side} by "
            f"{difference(plan.verified, plan.side)}, more than the one unit of the last "
            "place bounds_agree_at_declared_precision allows. Closing it needs a pose "
            "refined beyond the source's binary64 digits, for example by Newton's method "
            "on the active contacts, or coordinates the source prints at higher precision."
        ),
        "evidence": [registration.report],
    }


def priority_notes(plan: Plan) -> list[dict[str, Any]]:
    """Casson's and Couzo's first claims at a count both report, with their dates."""
    if plan.casson is None:
        return []
    first = plan.case["history"][0]
    casson = plan.casson
    return [
        {
            "claim": (
                f"s({plan.n}) <= {casson['side']}, Griffin Casson's packing, larger than "
                "the reported side"
            ),
            "claimed_by": ["Griffin Casson"],
            "published": (
                f"griffcass/square-packing {CASSON.revision[:7]}, committed "
                f"{casson['first_authored_utc']} (2026-09-23 22:45 UTC-6)"
            ),
            "year": 2026,
        },
        {
            "claim": (
                f"s({plan.n}) <= {first['side']}, the first of Francisco Couzo's packings "
                "for this count"
            ),
            "claimed_by": ["Francisco Couzo"],
            "published": (
                f"franciscouzo/square-packing {first['commit'][:7]}, authored "
                f"{first['authored_utc']}, committed {first['committed_utc']}"
            ),
            "year": 2026,
        },
    ]


def _ours(item: Mapping[str, Any], ours: set[str]) -> bool:
    return bool(set(item.get("evidence") or []) & ours)


def resource(source: packets.Source) -> dict[str, Any]:
    local = f"web/{source.directory}"
    if source.retain_raw:
        local += f"/{packets.CASSON_TREE}"
    return {
        "key": source.key,
        "role": "upper-bound-report",
        "local": local,
        "url": source.url,
        "retrieved": True,
    }


def front_matter(plan: Plan, front: str) -> str:
    payload = safe_load(front)["packing"]
    registration = plan.registration
    # A conflict or blocker an earlier registration at this count wrote is about the
    # packing this one replaces, so it goes with it.
    ours = {
        evidence
        for step in plan.chain
        for evidence in (
            step.registration.report,
            step.registration.replay,
            step.registration.interval_replay,
        )
    } | {CASSON_REPORT}
    # Never earlier than a later intake's review, the rule
    # `devtools.apply_wand125_rectangles` keeps from the other side: its 1 October
    # registration reviewed n = 68 after this intake did. ISO dates order as text.
    reviewed = max(str(payload.get("source_reviewed") or ""), registration.intake)
    front = re.sub(
        r"^  source_reviewed: .*$",
        f"  source_reviewed: '{reviewed}'",
        front,
        count=1,
        flags=re.MULTILINE,
    )
    front = set_block(
        front, "reported_upper_bound", reported_upper(plan, payload["reported_upper_bound"])
    )
    front = set_block(
        front,
        "verified_upper_bound",
        {
            "value": plan.verified,
            "exact_form": str(plan.receipt["exact_form"]),
            "evidence": [registration.replay, registration.interval_replay],
        },
    )
    front = set_block(front, "conjectured_optimum", None)
    notes = [
        note
        for note in payload.get("priority_notes") or []
        if not {"Griffin Casson", "Francisco Couzo"} & set(note.get("claimed_by") or [])
    ]
    front = set_block(front, "priority_notes", notes + priority_notes(plan))
    wanted = [registration.report, registration.replay, registration.interval_replay]
    if plan.casson is not None:
        wanted.append(CASSON_REPORT)
    # This intake's entries lead a draft. On a record that already carries them they keep
    # their places, since a later intake may have put its own ahead of them, as wand125's
    # rectangle registrations did at n = 68.
    evidence = list(payload["evidence"])
    front = set_block(
        front, "evidence", [item for item in wanted if item not in evidence] + evidence
    )
    conflicts = [item for item in payload["conflicts"] if not _ours(item, ours)]
    front = set_block(
        front, "conflicts", conflicts + ([conflict(plan)] if plan.trailing else [])
    )
    blockers = [
        item for item in payload["blockers"] if not _ours(item, ours | set(EARLIER_UPPER))
    ]
    front = set_block(front, "blockers", blockers + ([blocker(plan)] if plan.trailing else []))
    added = [resource(registration.source)]
    if plan.casson is not None:
        added.append(resource(CASSON))
    # And its resources likewise: written over in place where present, ahead otherwise.
    ours_by_key = {item["key"]: item for item in added}
    kept = [ours_by_key.get(item["key"]) or item for item in payload["resources"]]
    present = {item["key"] for item in kept}
    return set_block(
        front, "resources", [item for item in added if item["key"] not in present] + kept
    )


# --------------------------------------------------------------------------------------
# Body
# --------------------------------------------------------------------------------------


def _section(body: str, heading: str) -> tuple[int, int] | None:
    """The span of one ``##`` section, heading included, up to the next ``##``."""
    start = body.find(f"{heading}\n")
    if start < 0:
        return None
    end = body.find("\n## ", start + len(heading))
    return start, (len(body) if end < 0 else end + 1)


def opener(body: str, plan: Plan, verified_lower: str) -> str:
    """Point the case's opening sentence at the new side and its gap.

    The sentence is read in either form the records hold it in, code or the math
    `devtools.migrate_math` made of it, and written as code for `apply_case` to convert.
    """
    who = f"{plan.registration.author}’s ({plan.registration.result})"
    shown = display_first_party_upper(plan.side)
    body, count = re.subn(
        rf"The\s+best\s+known\s+(?:published\s+)?packing(?:,\s+[^`$]*?,)?\s+gives\s+"
        rf"(?:`s\({plan.n}\)\s+≤\s+[^`]+`|\$s\({plan.n}\)\s+\\le\s+[^$]+\$)",
        f"The best known published packing, {who}, gives `s({plan.n}) ≤ {shown}`",
        body,
        count=1,
    )
    if count != 1:
        raise ValueError(f"n={plan.n}: no opening sentence names the best known packing")
    return re.sub(
        r"leaving\s+a\s+gap\s+of\s+(?:`[0-9.]+`|\$[0-9.]+\$)",
        f"leaving a gap of `{display_gap(plan.side, verified_lower)}`",
        body,
        count=1,
    )


def ceiling_section(plan: Plan) -> str:
    registration = plan.registration
    certified = str(plan.receipt["certified_side_decimal"])[: len(plan.side) + 5]
    first = (
        f"`verified_upper_bound` for this case is `{plan.verified}`, proved by the exact "
        f"rational certificate of {registration.author}’s packing "
        f"(`{registration.replay}`). It is **larger** than the best known `{plan.side}` two "
        f"fields above it, by `{difference(plan.verified, plan.side)}`."
    )
    second = (
        f"It is not the value of `s({plan.n})` and not a different packing: it is the "
        f"certificate’s own side, `{certified}…`, rounded up at the fifteen decimals the "
        "source prints. The source writes each coordinate as a binary64 value, and rounded "
        "to rationals those poses close only at a side "
        f"{plan.receipt['units_above_printed']} units of the last place above the printed "
        "one, so the printed side itself is not certified here. The `replay-failure` "
        "conflict and the `mathematics` blocker in the frontmatter record the difference. "
        "Read `reported_upper_bound` for the best known side length."
    )
    return f"{CEILING_HEADING}\n\n{first}\n\n{second}\n\n"


def _history_sentence(plan: Plan) -> str:
    history = plan.case.get("history") or []
    first = history[0] if history else None
    if first is None or first["side"] == plan.side:
        return ""
    return (
        f" Its first packing for this count, of side `{first['side']}`, is dated "
        f"{day(first['authored_utc'])}."
    )


def _certificate_paragraph(plan: Plan) -> str:
    registration = plan.registration
    receipt = plan.receipt
    certified = Fraction(str(receipt["certified_side"]))
    relation = (
        "no larger than the printed side"
        if int(receipt["units_above_printed"]) <= 0
        else f"`{receipt['side_increase']}` above the printed side"
    )
    receipts = f"../resources/web/{registration.source.directory}/README.md#certified-here"
    interval = f"../resources/web/{registration.source.directory}/README.md#interval-route"
    return (
        "This repository certifies it exactly. The retained decimal pose rounds to an "
        "exact rational packing at centre dilation 1, of side "
        f"`{_decimal(certified, len(plan.side.split('.')[1]) + 4)}`, {relation}, and every "
        "pair and every wall is decided over `ℚ` twice, by the promotion’s exact "
        "separating-axis test and by an independent checker that shares no code with it "
        f"([receipt]({receipts})). That proves `s({plan.n}) ≤ {plan.verified}`, the "
        "verified upper bound; it says nothing about optimality. Interval arithmetic on "
        "the printed pose itself, with each angle’s true cosine and sine and no rational "
        "rounding, decides every pair and wall again and gives the same verified upper "
        f"bound ([interval route]({interval}))."
    )


@cache
def _issue_opened() -> str:
    """When issue #227 was opened, as the Couzo packet's acquisition record keeps it."""
    return str(packets.acquisition(FRANCISCOUZO)["ai_statement"]["opened_utc"])


def _issue_sentence(plan: Plan, casson_time: str) -> str:
    """At a count issue #227 names before Casson's commit, the issue as evidence of when.

    The issue is dated by GitHub rather than by either author's clock, so it bears on
    priority where the rewritten history cannot; it gives no side, so it dates a claim at
    the count and not any one packing. The comparison is of the full timestamps; the
    sentence gives the plain date, and the acquisition record keeps the time.
    """
    opened = _issue_opened()
    if plan.n not in ISSUE_COUNTS or _when(opened) >= _when(casson_time):
        return ""
    return (
        f" [Issue #227]({ISSUE}), opened on {day(opened)}, already linked Couzo’s "
        "repository and named this count, so a claim of his at this count predates "
        "Casson’s commit on evidence independent of either repository’s history; the "
        "issue gives no side."
    )


def _casson_paragraph(plan: Plan) -> str | None:
    """Casson's packing at a count both report, and which of the two is the earlier.

    The order is decided on the full timestamps, which `priority_notes` writes into the
    front matter; the sentences give each packing's plain date and point there. Couzo's
    history carries two: the date his first packing was authored, and the date the
    history now public was committed. Where the first precedes Casson's commit and the
    second follows it, the paragraph says both, since "earlier" on the authored date
    alone would state the order more firmly than the record does.
    """
    casson = plan.casson
    if casson is None:
        return None
    first = plan.case["history"][0]
    casson_time = str(casson["first_authored_utc"])
    earlier = _when(first["authored_utc"]) < _when(casson_time)
    recommitted = _when(first["committed_utc"]) > _when(casson_time)
    kept = "by the timestamps this record’s priority notes keep"
    caveat = (
        f"; the history now public was committed on {day(first['committed_utc'])}, after it"
        if recommitted
        else ""
    )
    ordering = (
        f"Couzo’s first packing for this count, of side `{first['side']}`, is dated "
        f"{day(first['authored_utc'])}, before Casson’s{caveat}. The priority notes keep "
        "the timestamps"
        if earlier
        else f"Casson’s is the earlier of the two {kept}: Couzo’s first packing for this "
        f"count, of side `{first['side']}`, is dated {day(first['authored_utc'])}"
    )
    gap = difference(str(casson["side"]), plan.side)
    return (
        f"Griffin Casson’s [`square-packing`]({_link(CASSON)}), dated 23 September 2026 "
        "and made with the help of Claude as its README says, reports a packing of side "
        f"`{casson['side']}` for this count, larger than Couzo’s by `{gap}`. {ordering}."
        f"{_issue_sentence(plan, casson_time)} The record states both dates and infers "
        "nothing about whether either packing derives from the other."
    )


def _couzo_paragraph(plan: Plan) -> str:
    registration = plan.registration
    if plan.previous is None:
        dated = (
            f"dated {day(plan.case['current_since_authored_utc'])} and unchanged when this "
            f"record retained the repository on 27 September 2026 ({registration.result})."
        )
    else:
        previous = plan.previous
        current = (
            "the revision this record retained"
            if plan.case["current_since_commit"] == registration.source.revision
            else "and unchanged at the revision this record retained"
        )
        dated = (
            f"dated {day(plan.case['current_since_authored_utc'])}, {current} "
            f"({registration.result}). It replaces his packing of side `{previous.side}`, "
            f"dated {day(previous.case['current_since_authored_utc'])} "
            f"({previous.registration.result})."
        )
    return (
        f"Francisco Couzo’s [`square-packing`]({_link(registration.source)}) reports a "
        f"packing of side `{plan.side}` for this count, "
        f"{dated}{_history_sentence(plan)} The repository names no method "
        "and no tolerance, and itself states no AI assistance; its author said on "
        f"[issue #227]({ISSUE}) that he found the 102 and 103 packings “with the help of "
        "Claude”."
    )


def _de_winter_paragraph(plan: Plan) -> str:
    registration = plan.registration
    return (
        f"Joost de Winter’s [`square-packing-211`]({_link(registration.source)}) reports "
        f"211 unit squares in a square of side `{plan.side}`, dated "
        f"{day(plan.case['current_since_authored_utc'])} ({registration.result}): the first "
        "packing on record that beats the `15 × 15` grid. Its record names a previous side "
        f"of `{plan.case['previous_verified_s']}` and describes its method as "
        f"“{plan.case['method']}” It reports an outward interval check at 80 digits but "
        "publishes no boxes or checker, and it says nothing about AI assistance. With the "
        "catalogue’s packings at `n = 241, 273, 307`, found by Arslanov, Mustafin and "
        "Shangitbayev in 2019, it shows `s(k² − k + 1) < k` for `k = 15` as well as `16`, "
        "`17` and `18`. The records at `n = 31, 43, …, 183` (`k = 6…14`) still hold the "
        "grid, so on the catalogue and this record the smallest `k` shown to satisfy it "
        "moves from 16 to 15."
    )


def _previous(plan: Plan, old: str, kingbird: str, unitsquare: str | None) -> str:
    """The earlier packing's paragraph, put in the past where it spoke of the present."""
    if plan.n == 211:
        return (
            "Before this intake the best known packing was the trivial `15 × 15` grid: the "
            "Kingbird catalogue as retained here does not picture `n = 211`, and its live "
            "page of 29 September 2026 still does not."
        )
    old = re.sub(
        r"We\s+therefore\s+record\s+the\s+value\s+as\s+reported\.",
        "This repository recorded the value as reported.",
        old,
    )
    old = re.sub(
        r"The\s+formal\s+lane\s+retains\s+the\s+exact\s+"
        r"(?:`(?P<a>\d+)\s+×\s+(?P<b>\d+)`|\$(?P<c>\d+)\s+\\times\s+(?P<d>\d+)\$)"
        r"\s+grid\s+construction\.",
        lambda match: (
            f"The formal lane held the exact `{match['a'] or match['c']} × "
            f"{match['b'] or match['d']}` grid construction until this intake."
        ),
        old,
    )
    lead = (
        f"Before this intake the best known packing was the UnitSquare Project’s, of side "
        f"`{unitsquare}`, below the Kingbird catalogue’s `{kingbird}`."
        if unitsquare is not None
        else f"Before this intake the best known packing was the Kingbird catalogue’s, of "
        f"side `{kingbird}`."
    )
    return f"{lead}\n\n{old.strip()}"


def _replaced_marker(plan: Plan) -> str:
    """How the paragraph on the packing a later registration replaced begins."""
    assert plan.previous is not None
    return f"{plan.previous.registration.author}’s earlier packing for this count"


def _replaced(plan: Plan, previous: str) -> str:
    """The previous-packing text of a count a later registration took from an earlier one.

    It leads with the packing replaced, certified here under the earlier registration,
    and keeps what that registration kept, its opening put in the past. Written over its
    own output it changes nothing, since the paragraph it leads with is replaced, not added.
    """
    earlier = plan.previous
    assert earlier is not None
    marker = _replaced_marker(plan)
    if previous.startswith(marker):
        previous = previous.split("\n\n", 1)[1] if "\n\n" in previous else ""
    previous = re.sub(r"^Before\s+this\s+intake\b", "Before that intake", previous)
    receipts = f"{_link(earlier.registration.source)}#certified-here"
    paragraph = (
        f"{marker}, of side `{earlier.side}`, dated "
        f"{day(earlier.case['current_since_authored_utc'])}, was the best known from this "
        f"record’s intake of {day(earlier.registration.intake)} until this one "
        f"({earlier.registration.result}), and this repository certified "
        f"`s({plan.n}) ≤ {earlier.verified}` from it ([receipt]({receipts}))."
    )
    return f"{paragraph}\n\n{previous}".rstrip("\n")


def packing_section(plan: Plan, old: str, kingbird: str, unitsquare: str | None) -> str:
    """The rewritten ``## The packing`` section, keeping the earlier paragraph."""
    content = old.split("\n", 1)[1].strip("\n")
    if PREVIOUS_HEADING in content:
        previous = content.split(PREVIOUS_HEADING, 1)[1].strip("\n")
    else:
        previous = _previous(plan, content, kingbird, unitsquare)
    if plan.previous is not None:
        previous = _replaced(plan, previous)
    lead = (
        _couzo_paragraph(plan)
        if plan.registration.source.layout == "couzo"
        else _de_winter_paragraph(plan)
    )
    parts = [lead, _certificate_paragraph(plan)]
    casson = _casson_paragraph(plan)
    if casson is not None:
        parts.append(casson)
    return "\n\n".join(["## The packing", *parts, PREVIOUS_HEADING, previous]) + "\n"


def body_text(
    plan: Plan, body: str, payload: Mapping[str, Any], earlier: Mapping[str, str]
) -> str:
    body = opener(body, plan, str(payload["verified_lower_bound"]["value"]))
    span = _section(body, CEILING_HEADING)
    if span is not None:
        start, end = span
        body = body[:start] + (ceiling_section(plan) if plan.trailing else "") + body[end:]
    elif plan.trailing:
        start, _end = _section(body, "## The packing") or (len(body), len(body))
        body = body[:start] + ceiling_section(plan) + "\n" + body[start:]
    span = _section(body, "## The packing")
    if span is None:
        raise ValueError(f"n={plan.n}: no packing section")
    start, end = span
    section = packing_section(
        plan, body[start:end], earlier["kingbird"], earlier.get("unitsquare")
    )
    return body[:start] + section + "\n" + body[end:].lstrip("\n")


# --------------------------------------------------------------------------------------
# Source coverage
# --------------------------------------------------------------------------------------


def _override(plan: Plan, earlier: Mapping[str, str]) -> dict[str, Any]:
    beaten = "the UnitSquare release and " if earlier.get("unitsquare") else ""
    if plan.previous is not None:
        beaten = (
            f"{plan.previous.registration.author}'s earlier side "
            f"({plan.previous.registration.result}) and " + beaten
        )
    return {
        "n": plan.n,
        "source_id": plan.registration.coverage_id,
        "value": plan.side,
        "evidence": plan.registration.report,
        "reason": (
            f"Newer reported upper bound, certified here ({plan.registration.result}), "
            f"below {beaten}the Kingbird baseline."
        ),
    }


def _entries(name: str, entries: Sequence[Mapping[str, Any]]) -> str:
    if not entries:
        return f"{name}: []\n"
    lines = [f"{name}:\n"]
    for entry in entries:
        dumped = yaml.safe_dump(dict(entry), allow_unicode=True, sort_keys=False, width=88)
        for index, line in enumerate(dumped.splitlines()):
            lines.append(("  - " if index == 0 else "    ") + line + "\n")
    return "".join(lines)


def coverage_text(
    text: str, selected: list[Plan], earliest: Mapping[int, Mapping[str, str]]
) -> str:
    original = text
    coverage = safe_load(text)
    ours = {registration.coverage_id for registration in REGISTRATIONS}
    from devtools.source_supersession import (  # noqa: PLC0415
        coverage_list_span,
        preserve_other_coverage,
        replace_coverage_list,
        superseded_counts,
    )

    later = superseded_counts(coverage, ours)
    selected = [plan for plan in selected if plan.n not in later]
    by_n = {plan.n: plan for plan in selected}
    overrides = [
        entry
        for entry in coverage["selected_overrides"]
        if entry["source_id"] not in ours and entry["n"] not in by_n
    ]
    overrides += [_override(plan, earliest[plan.n]) for plan in selected]
    overrides.sort(key=lambda entry: entry["n"])
    superseded = [
        entry
        for entry in coverage.get("superseded_reports") or []
        if entry["n"] not in by_n
        or entry["source_id"] not in {UNITSQUARE_COVERAGE_ID, CASSON_COVERAGE_ID} | ours
    ]
    for plan in selected:
        unitsquare = earliest[plan.n].get("unitsquare")
        first = plan.chain[0].registration
        if unitsquare is not None:
            superseded.append(
                {
                    "n": plan.n,
                    "source_id": UNITSQUARE_COVERAGE_ID,
                    "value": unitsquare,
                    "superseded_by": plan.registration.coverage_id,
                    "reason": (
                        f"Superseded on {first.intake} by Francisco Couzo's smaller certified "
                        "side."
                    ),
                }
            )
        superseded.extend(
            {
                "n": plan.n,
                "source_id": step.registration.coverage_id,
                "value": step.side,
                "superseded_by": plan.registration.coverage_id,
                "reason": (
                    f"Superseded on {plan.registration.intake} by "
                    f"{plan.registration.author}'s own later and smaller certified side "
                    f"({plan.registration.result})."
                ),
            }
            for step in plan.chain[:-1]
        )
        if plan.casson is not None:
            superseded.append(
                {
                    "n": plan.n,
                    "source_id": CASSON_COVERAGE_ID,
                    "value": str(plan.casson["side"]),
                    "superseded_by": plan.registration.coverage_id,
                    "reason": (
                        "Larger than Francisco Couzo's side at this count; the case record "
                        "states both sources' dates and values."
                    ),
                }
            )
    superseded.sort(key=lambda entry: (entry["n"], entry["source_id"]))
    text = replace_coverage_list(
        text, "selected_overrides", _entries("selected_overrides", overrides)
    )
    block = _entries("superseded_reports", superseded)
    if coverage_list_span(text, "superseded_reports") is not None:
        rendered = replace_coverage_list(text, "superseded_reports", block)
    else:
        rendered = text.replace("beyond_horizon_claims:", block + "beyond_horizon_claims:", 1)
    return preserve_other_coverage(original, rendered, set(by_n))


# --------------------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------------------


def earlier_reports() -> dict[int, dict[str, str]]:
    """The best known sides this intake replaces, from the retained sources."""
    kingbird = parse_kingbird(CATALOGUE, 1, 324)
    release = load_unitsquare_release()
    result: dict[int, dict[str, str]] = {}
    for registration in REGISTRATIONS:
        for n in packets.cases(registration.source):
            result[n] = {"kingbird": kingbird[n]}
            if n in release:
                result[n]["unitsquare"] = release[n].offered_side
    return result


def evidence_problems(selected: Sequence[Plan]) -> list[str]:
    """The registrations' evidence entries must cover exactly the cases that cite them."""
    entries = {entry["id"]: entry for entry in safe_load(EVIDENCE.read_text())["evidence"]}
    problems = []
    for registration in REGISTRATIONS:
        # A case a later registration took still cites the earlier one's evidence.
        wanted = sorted(
            plan.n
            for plan in selected
            if any(step.registration is registration for step in plan.chain)
        )
        for identifier in (
            registration.report,
            registration.replay,
            registration.interval_replay,
        ):
            scope = entries.get(identifier, {}).get("scope", {}).get("n_values")
            if scope != wanted:
                problems.append(f"{identifier}: scope is not {wanted}")
    casson = sorted(packets.cases(CASSON))
    if entries.get(CASSON_REPORT, {}).get("scope", {}).get("n_values") != casson:
        problems.append(f"{CASSON_REPORT}: scope is not Casson's {len(casson)} counts")
    return problems


def apply_case(plan: Plan, text: str, earlier: Mapping[str, str]) -> str:
    """One case record with this intake written over it: its front matter and its body.

    ``devtools.generate_frontier_case`` applies it to its own draft of a certified count,
    since the record is that draft with this intake applied.
    """
    from devtools.source_supersession import preserve_selected_case  # noqa: PLC0415

    if preserve_selected_case(plan.n, text, {plan.registration.coverage_id}):
        return text
    if plan.previous is not None:
        text = apply_case(plan.previous, text, earlier)
    _, front, body = text.split("---\n", 2)
    payload = safe_load(front)["packing"]
    # What this writes is prose with code spans; its mathematics becomes math by the
    # rules `devtools.migrate_math` applied to the rest of the body, which is left as is.
    written = markdown_math(body_text(plan, body, payload, earlier))
    # A rewritten paragraph describing a source keeps the AI-assistance statement
    # `devtools.state_ai_assistance` owes it there, as Casson's does at his 39 counts.
    return state(f"---\n{front_matter(plan, front)}---\n{written}")


#: The backslash the formatter puts before a character that would open a list item, a
#: heading or a quotation at the start of a wrapped line, as in `\+ 1).`: formatting,
#: like the line break it follows.
_WRAP_ESCAPE = re.compile(r"^([ \t]*)\\([-+*#>])", re.MULTILINE)


def normalized(text: str) -> str:
    """The text with its whitespace collapsed: the formatter rewraps what this writes."""
    return " ".join(_WRAP_ESCAPE.sub(r"\1\2", text).split())


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    args = parser.parse_args(argv)
    # Evan Daniel's exact optima (T-098) are a layer over this intake at 47 of its counts,
    # imported here and not at the top, since that tool reads this one's helpers.
    from devtools import apply_exact_optima  # noqa: PLC0415

    selected = plans()
    earlier = earlier_reports()
    problems = evidence_problems(selected)
    drift: list[Path] = []
    for plan in selected:
        path = FRONTIER / f"n-{plan.n:03d}.md"
        text = path.read_text(encoding="utf-8")
        rendered = apply_exact_optima.apply_case(
            plan.n, apply_case(plan, text, earlier[plan.n])
        )
        if normalized(rendered) != normalized(text):
            drift.append(path)
            if not args.check:
                atomic_write_text(path, rendered)
    text = COVERAGE.read_text(encoding="utf-8")
    updated = apply_exact_optima.coverage_text(coverage_text(text, selected, earlier))
    if updated != text:
        drift.append(COVERAGE)
        if not args.check:
            atomic_write_text(COVERAGE, updated)
    for problem in problems:
        print(f"FAIL {problem}", file=sys.stderr)
    for path in drift:
        print(("drift: " if args.check else "wrote: ") + str(path.relative_to(ROOT)))
    return 1 if problems or (args.check and drift) else 0


if __name__ == "__main__":
    sys.exit(main())
