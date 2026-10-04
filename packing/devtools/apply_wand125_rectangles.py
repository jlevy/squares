#!/usr/bin/env python3
# ruff: noqa: RUF001 -- this module writes register prose, whose typography uses curly
# apostrophes and the corpus's other non-ASCII marks.
"""Carry wand125's rectangle-density bounds into the Frontier records.

Each retained packet of the source (`devtools.audit_wand125_rectangles.PACKETS`) is one
`Registration`: its source key and its three evidence entries. The newest registration
any case record cites is the registered one, and a run without ``--packet`` repeats it.
A later packet is registered by naming it; an earlier one is refused, because the later
one raised its bounds and writing it again would lower them.

The reported lane takes every standing certificate at the chosen packet's revision, and
its monotone consequences, wherever it beats the case's current report. A certificate
byte-identical to one an earlier packet retains belongs to that packet's registration,
which already wrote it, so a later registration writes only the counts its own new or
raised certificates carry. The verified lane takes only certificates whose complete
coverage replay is in a retained receipt, ``receipts/replay/audit.json`` of this packet
or an earlier one, again with monotone consequences. Replays are expensive (hours each),
so they arrive in batches: rerun this after each batch and it promotes exactly what the
receipts now cover. It is idempotent, and it never lowers a bound.

What it writes: each affected case's ``reported_lower_bound``, ``verified_lower_bound``,
top-level ``evidence`` and ``resources`` entries, ``source_reviewed`` (never moved
earlier), and one intake paragraph under the title, ending in wand125's AI-assistance
statement as ``devtools.state_ai_assistance`` words it, and it retires the claims an
earlier registration's paragraph makes once they stop being current. In ``evidence.yaml``
it inserts the registration's report entries when they are missing, keeps every wand125
rectangle entry's scope equal to the cases that cite it, and keeps each replay entry's
command. Other prose in a promoted
case can still describe the superseded bound, which ``check_case_prose`` reports, and is
edited by hand.

``--frontier`` points every read and write at a copy of the Frontier directory, for a
dry run. ``--plan`` prints the per-count decision table without writing, and
``--replay-plan`` the standing certificates whose replay would raise a verified bound,
largest rise first, with the upstream per-angle CPU time as the cost.

Usage, from ``packing/``:
    uv run --frozen --all-extras --group dev python -m devtools.apply_wand125_rectangles
    uv run --frozen --all-extras --group dev python -m devtools.apply_wand125_rectangles --check
    uv run --frozen --all-extras --group dev python -m devtools.apply_wand125_rectangles \\
        --packet 2026-09-28 --frontier /tmp/frontier-copy
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml
from strif import atomic_write_text

from devtools.audit_wand125_rectangles import (
    OCTOBER_1,
    OCTOBER_2,
    PACKETS,
    SEPTEMBER_27,
    SEPTEMBER_28,
    SOURCE_URL,
    Packet,
    monotone_bounds,
)
from devtools.generate_frontier_case import display_gap
from devtools.migrate_math import markdown_math
from devtools.retained_data import read_retained_text, retained_exists
from devtools.state_ai_assistance import WAND125
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
SCOPE = "Unrestricted square packing with independent rotations and disjoint interiors."


@dataclass(frozen=True, slots=True, eq=False)
class Registration:
    """How one packet's certificates are cited in the Frontier records."""

    packet: Packet
    source_key: str
    report: str
    monotone_report: str
    replay: str
    #: Counts where a stronger bound from another source is registered separately, so
    #: this packet's certificate there is a superseded prior and moves neither lane.
    #: `plans` skips such a count outright, so a replay of its certificate would not
    #: reach the verified lane either: a count belongs here only once the other bound
    #: holds both lanes. Where the stronger bound is only reported, `plans` already
    #: leaves the reported field to it, and a replay still raises the verified one.
    superseded_priors: Mapping[int, str]
    #: The report entries to insert into ``evidence.yaml`` when missing; ``{scope}`` is
    #: filled with the cases that cite each one, and ``{certificate}`` with the packet's
    #: certificate directory. Empty for a registration whose entries were written by hand.
    entries: Mapping[str, str]

    @property
    def date(self) -> str:
        return self.packet.date

    @property
    def intake(self) -> str:
        return f"**External intake, {self.date}.**"

    @property
    def link(self) -> str:
        return f"../resources/web/{self.packet.directory.name}/README.md"

    @property
    def head(self) -> str:
        """How the paragraph this registration writes begins, and so how it is found.

        The date alone is not enough: other sources' intakes of the same day open with the
        same bold label, and a paragraph this tool did not write is never touched.
        """
        return f"{self.intake} wand125’s [rectangle-density source]({self.link})"

    def wrote(self, paragraph: str) -> bool:
        """Whether ``paragraph`` is this registration's, however Flowmark wrapped it."""
        return " ".join(paragraph.split()).startswith(self.head)

    @property
    def ids(self) -> frozenset[str]:
        return frozenset({self.report, self.monotone_report, self.replay})

    @property
    def resource(self) -> dict[str, Any]:
        return {
            "key": self.source_key,
            "role": "lower-bound-proof",
            "local": f"web/{self.packet.directory.name}/wand125-rectangles",
            "url": SOURCE_URL,
            "retrieved": True,
        }

    @property
    def replay_audit(self) -> Path:
        return self.packet.directory / "receipts/replay/audit.json"

    @property
    def preflight_audit(self) -> Path:
        return self.packet.directory / "receipts/preflight/audit.json"


_REPORT_2026_09_28 = """\
  - id: E-wand125-rectangle-2026-09-28-report
    claim: lower-bound
    scope: {scope}
    assurance: reported
    reported_method: interval-certified
    performed_by: source-author
    relationship_to_generator: same-implementation
    origin: external
    novelty: previously-published
    source_key: '[wand125 rectangle bounds 2026-09-28]'
    certificate: {certificate}
    replay_status: not-attempted
    verifiers: [V-tokoharu-verify-cpp]
    limitations: >-
      Source 39d8ecc74d651b54ec977c331c8f2015b442a6c4, pushed between 2026-09-27 and
      2026-09-28 (UTC), reports one standing rectangle-density certificate in Tokoharu's
      format for each listed count, each new or raised since ad43d29, accepted there by
      Tokoharu's unchanged interval checker (verify.cpp SHA-256
      a75140df1b484ad104a214d2e8de87afda9fca5929341ec40121afde0c1af602). The listed
      sides run from 399/80 at n21 to 49209/5000 at n95; the complete list is the
      CASES_2026_09_28 table of devtools/audit_wand125_rectangles.py and the source's own
      README. The twelve standing certificates the revision left unchanged, at n18, 19,
      20, 26, 27, 30, 32, 40, 45, 61, 75 and 78, are byte-identical to those
      E-wand125-rectangle-report records, and their cases stay on that entry. Each
      certificate's weights were multiplied by one exact rational factor, between
      1.00021 and 1.02697, to bring its mass to n - 1/100 (n - 1/1000 at n21) before the
      recorded run, which checked the scaled data. The source's direct n77 claim,
      891/100, is weaker than the n76 transfer recorded separately. Lower rungs,
      matching certificates, the point certificates and the point-only and mixed-measure
      bundles at the same revision are pinned by digest only. This is the public-claim
      entry, not a local verification receipt. At n21 the claim 399/80 is a superseded
      prior: the bound registered there separately, Evan Daniel's s(21) >= 5000/1001 when
      this entry was written, is stronger, so the case record does not cite this entry.
    source_reviewed: '2026-09-28'
"""
_MONOTONE_2026_09_28 = """\
  - id: E-wand125-rectangle-2026-09-28-monotone-report
    claim: lower-bound
    scope: {scope}
    assurance: reported
    reported_method: interval-certified
    performed_by: repository
    relationship_to_generator: not-applicable
    origin: audited-here
    novelty: previously-published
    source_key: '[wand125 rectangle bounds 2026-09-28]'
    replay_status: not-attempted
    verifiers: [V-tokoharu-verify-cpp]
    limitations: >-
      Reported-lane transfer at 39d8ecc: a certificate whose exact mass is below k
      refutes k squares as well, and deleting squares proves monotonicity, so each listed
      count takes the strongest smaller-count certificate below whose mass it lies. The
      n76 certificate at 223/25, of mass 7599/100, gives s(77) >= 223/25, above the
      direct n77 claim 891/100; the n89 certificate at 191/20, of mass 8899/100, gives
      s(90) >= 191/20; the source README marks the n76 and n89 lines "(also n = 77)" and
      "(also n = 90)". The listed counts are those where the transfer beats every other
      registered report. This derivation does not strengthen the assurance of its
      source premise or substitute for its complete replay.
    source_reviewed: '2026-09-28'
"""
_REPORT_2026_10_01 = """\
  - id: E-wand125-rectangle-2026-10-01-report
    claim: lower-bound
    scope: {scope}
    assurance: reported
    reported_method: interval-certified
    performed_by: source-author
    relationship_to_generator: same-implementation
    origin: external
    novelty: previously-published
    source_key: '[wand125 rectangle bounds 2026-10-01]'
    certificate: {certificate}
    replay_status: not-attempted
    verifiers: [V-tokoharu-verify-cpp]
    limitations: >-
      Source 1a25a5ed745fdd905a52f48fcc48150a0669032d, committed 2026-10-01 (UTC),
      reports one standing rectangle-density certificate in Tokoharu's format for each
      listed count, each new or raised since 39d8ecc and first committed between
      2026-09-29 and 2026-10-01 (UTC), accepted there by Tokoharu's unchanged interval
      checker (verify.cpp SHA-256
      a75140df1b484ad104a214d2e8de87afda9fca5929341ec40121afde0c1af602). The listed
      sides run from 1927/400 at n19 to 49259/5000 at n95; the complete list is the
      CASES_2026_10_01 table of devtools/audit_wand125_rectangles.py and the source's own
      README. Registration was requested in jlevy/squares#281, which lists 34 of the 37
      and leaves out n59, n77 and n78. The sixteen standing certificates the revision
      left unchanged, at n18, 21, 32, 37, 45, 51, 52, 57, 58, 60, 61, 67, 71, 72, 73 and
      91, are byte-identical to those E-wand125-rectangle-report and
      E-wand125-rectangle-2026-09-28-report record, and their cases stay on those
      entries. Each certificate's weights were multiplied by one exact rational factor,
      between 1.00004 and 1.04329, to bring its mass to n - 1/100 before the recorded
      run, which checked the scaled data. The n31 certificate, of mass 3099/100, also
      gives s(32) >= 2381/400, above the unchanged direct n32 claim 119/20 and below
      Evan Daniel's s(32) = 6. Lower rungs, matching certificates, the point
      certificates and the point-only, exact-cover and mixed-measure bundles at the same
      revision are pinned by digest only. This is the public-claim entry, not a local
      verification receipt. At n59, n66, n77, n78 and n90 a stronger bound was
      registered separately when this entry was written, so those five case records do
      not cite this entry: the source's own exact covers s(59) = 8 and s(77) = 9, Evan
      Daniel's s(78) = 9, and the source's mixed rectangle-measure certificates 421/50
      at n66 and 48/5 at n90.
    source_reviewed: '2026-10-01'
"""
_MONOTONE_2026_10_01 = """\
  - id: E-wand125-rectangle-2026-10-01-monotone-report
    claim: lower-bound
    scope: {scope}
    assurance: reported
    reported_method: interval-certified
    performed_by: repository
    relationship_to_generator: not-applicable
    origin: audited-here
    novelty: previously-published
    source_key: '[wand125 rectangle bounds 2026-10-01]'
    replay_status: not-attempted
    verifiers: [V-tokoharu-verify-cpp]
    limitations: >-
      Reported-lane transfer at 1a25a5e: a certificate whose exact mass is below k
      refutes k squares as well, and deleting squares proves monotonicity, so each listed
      count takes the strongest smaller-count certificate below whose mass it lies. Two
      certificates new at this revision are the strongest below counts they do not
      name: the n31 certificate at 2381/400, of mass 3099/100, passes the unchanged
      direct n32 claim 119/20 and carries to n32 through n36, and the n78 certificate at
      1793/200, of mass 7799/100, carries to n79 through n85. The direct n77 claim,
      3573/400, now exceeds the n76 transfer 357/40, and n87 and n90 have certificates of
      their own. The listed counts are those where the transfer beats every other
      registered report. This derivation does not strengthen the assurance of its
      source premise or substitute for its complete replay.
    source_reviewed: '2026-10-01'
"""
_REPORT_2026_10_02 = """\
  - id: E-wand125-rectangle-2026-10-02-report
    claim: lower-bound
    scope: {scope}
    assurance: reported
    reported_method: interval-certified
    performed_by: source-author
    relationship_to_generator: same-implementation
    origin: external
    novelty: previously-published
    source_key: '[wand125 rectangle bounds 2026-10-02]'
    certificate: {certificate}
    replay_status: not-attempted
    limitations: >-
      Source b00fc70f1904e9b1b567afee056d347f911209e8, committed 2026-10-02 (UTC),
      reports one standing rectangle-density certificate in Tokoharu's format for each
      listed count, each raised since 1a25a5e by three commits of 2026-10-02 (UTC),
      06eeb40, 7d77022 and 4318bdf, and accepted there by Tokoharu's unchanged interval
      checker (verify.cpp SHA-256
      a75140df1b484ad104a214d2e8de87afda9fca5929341ec40121afde0c1af602). The seven sides
      are 49/10 at n20, 2731/400 at n42, 127/16 at n59, 3451/400 at n70, 447/50 at n77,
      3859/400 at n91 and 1947/200 at n93; the complete standing list is the
      CASES_2026_10_02 table of devtools/audit_wand125_rectangles.py. No issue requests
      them; the import of 2 October took them in from the source's own commits. The 46
      standing certificates the revision left unchanged are byte-identical to those the
      earlier rectangle entries record, and their cases stay on those entries. Each
      certificate's weights were multiplied by one exact rational factor, between
      1.00009 and 1.03993, to bring its mass to n - 1/100 before the recorded run, which
      checked the scaled data. Lower rungs, matching certificates, the point
      certificates and the point-only, exact-cover, mixed and linear bundles at the same
      revision are pinned by digest only. This is the public-claim entry, not a local
      verification receipt. At n59 and n77 a stronger bound was registered separately
      when this entry was written, the source's own exact covers s(59) = 8 and
      s(77) = 9, so those case records do not cite this entry; at n91 and n93 the same
      revision's mixed rectangle-measure certificates, 97/10 at n91 and 39/4 at n92,
      which carries to n93, are stronger wherever they are registered.
    source_reviewed: '2026-10-02'
"""
_MONOTONE_2026_10_02 = """\
  - id: E-wand125-rectangle-2026-10-02-monotone-report
    claim: lower-bound
    scope: {scope}
    assurance: reported
    reported_method: interval-certified
    performed_by: repository
    relationship_to_generator: not-applicable
    origin: audited-here
    novelty: previously-published
    source_key: '[wand125 rectangle bounds 2026-10-02]'
    replay_status: not-attempted
    limitations: >-
      Reported-lane transfer at b00fc70: a certificate whose exact mass is below k
      refutes k squares as well, and deleting squares proves monotonicity, so each listed
      count takes the strongest smaller-count certificate below whose mass it lies. The
      one transfer new at this revision is the n91 certificate at 3859/400, of mass
      9099/100, to n92, where the source's mixed certificates hold more. The listed
      counts are those where the transfer beats every other registered report. This
      derivation does not strengthen the assurance of its source premise or substitute
      for its complete replay.
    source_reviewed: '2026-10-02'
"""

SEPTEMBER_27_REGISTRATION = Registration(
    packet=SEPTEMBER_27,
    source_key="[wand125 rectangle bounds 2026]",
    report="E-wand125-rectangle-report",
    monotone_report="E-wand125-rectangle-monotone-report",
    replay="E-wand125-rectangle-source-replay",
    # evand's reviewed s(21) >= 5000/1001 and s(32) = 6 (coordinator, 2026-09-27).
    superseded_priors={
        21: "evand/square-packing s(21) >= 5000/1001 supersedes 997/200",
        32: "evand/square-packing s(32) = 6 supersedes 119/20",
    },
    entries={},
)
SEPTEMBER_28_REGISTRATION = Registration(
    packet=SEPTEMBER_28,
    source_key="[wand125 rectangle bounds 2026-09-28]",
    report="E-wand125-rectangle-2026-09-28-report",
    monotone_report="E-wand125-rectangle-2026-09-28-monotone-report",
    replay="E-wand125-rectangle-2026-09-28-source-replay",
    # evand's s(21) and s(32) as before, and s(45) = 7, which the 2026-09-28 intake
    # takes in separately; the n32 and n45 certificates are unchanged since ad43d29.
    superseded_priors={
        21: "evand/square-packing s(21) >= 5000/1001 supersedes 399/80",
        32: "evand/square-packing s(32) = 6 supersedes 119/20",
        45: "evand/square-packing s(45) = 7 supersedes 1391/200",
    },
    entries={
        "E-wand125-rectangle-2026-09-28-report": _REPORT_2026_09_28,
        "E-wand125-rectangle-2026-09-28-monotone-report": _MONOTONE_2026_09_28,
    },
)
OCTOBER_1_REGISTRATION = Registration(
    packet=OCTOBER_1,
    source_key="[wand125 rectangle bounds 2026-10-01]",
    report="E-wand125-rectangle-2026-10-01-report",
    monotone_report="E-wand125-rectangle-2026-10-01-monotone-report",
    replay="E-wand125-rectangle-2026-10-01-source-replay",
    # The three counts where another source's bound holds both lanes, so no replay of the
    # rectangle certificate could move either; all three certificates are unchanged since
    # 39d8ecc. The counts whose stronger bound is only reported are deliberately absent:
    # wand125's exact covers s(59) = 8 and s(77) = 9, evand's s(60) = s(61) = 8 and
    # s(78) = 9, and wand125's mixed certificates at n37, n66 and n90 (n65 and n92 have no
    # rectangle certificate). `plans` leaves their reported fields alone because the
    # record holds more, and a replayed rectangle certificate still raises their
    # verified lane, which sat at Nagamochi's bound until one of those claims was replayed
    # (at Karakus's weaker bound since 2026-10-02, when Nagamochi's Lemma 1 proved false).
    superseded_priors={
        21: "evand/square-packing s(21) = 5 supersedes 399/80",
        32: "evand/square-packing s(32) = 6 supersedes 119/20 and the n31 transfer 2381/400",
        45: "evand/square-packing s(45) = 7 supersedes 1391/200",
    },
    entries={
        "E-wand125-rectangle-2026-10-01-report": _REPORT_2026_10_01,
        "E-wand125-rectangle-2026-10-01-monotone-report": _MONOTONE_2026_10_01,
    },
)
OCTOBER_2_REGISTRATION = Registration(
    packet=OCTOBER_2,
    source_key="[wand125 rectangle bounds 2026-10-02]",
    report="E-wand125-rectangle-2026-10-02-report",
    monotone_report="E-wand125-rectangle-2026-10-02-monotone-report",
    replay="E-wand125-rectangle-2026-10-02-source-replay",
    # The same three counts as at 1a25a5e, whose certificates are unchanged since 39d8ecc.
    # The exact covers at n59 and n77 and the mixed certificates at n91 and n92 are only
    # reported, so they are left to the comparison with the record, as before.
    superseded_priors={
        21: "evand/square-packing s(21) = 5 supersedes 399/80",
        32: "evand/square-packing s(32) = 6 supersedes 119/20 and the n31 transfer 2381/400",
        45: "evand/square-packing s(45) = 7 supersedes 1391/200",
    },
    entries={
        "E-wand125-rectangle-2026-10-02-report": _REPORT_2026_10_02,
        "E-wand125-rectangle-2026-10-02-monotone-report": _MONOTONE_2026_10_02,
    },
)
#: Oldest first; the order is the order of the packets' pins.
REGISTRATIONS = (
    SEPTEMBER_27_REGISTRATION,
    SEPTEMBER_28_REGISTRATION,
    OCTOBER_1_REGISTRATION,
    OCTOBER_2_REGISTRATION,
)
BY_DATE = {registration.date: registration for registration in REGISTRATIONS}
OURS = frozenset().union(*(registration.ids for registration in REGISTRATIONS))
if set(BY_DATE) != set(PACKETS):
    raise RuntimeError("every retained packet needs exactly one registration")


@dataclass(frozen=True, slots=True)
class Bound:
    """A side, the count whose certificate proves it, and the registration citing it."""

    side: Fraction
    source: int
    registration: Registration


@dataclass(frozen=True, slots=True)
class Plan:
    n: int
    reported: Bound | None
    verified: Bound | None


def _index(registration: Registration) -> int:
    return REGISTRATIONS.index(registration)


def owner(name: str) -> Registration:
    """The registration of the first packet that retains this certificate."""
    for registration in REGISTRATIONS:
        if any(name == held for held, _side in registration.packet.cases.values()):
            return registration
    raise KeyError(name)


def _loose(phrase: str) -> str:
    """A regex for ``phrase`` however Flowmark wrapped it, and with its escaped ``)``."""
    return r"\s+".join(re.escape(word).replace(r"\)", r"\\?\)") for word in phrase.split())


#: A figure as the bodies quote it: a code span, or the math `devtools.migrate_math` made
#: of one. The two delimiters are not paired; no body writes a span that mixes them.
_QUOTED = r"[`$]{figure}[`$]"

#: The two sentences the Nagamochi-form bodies use to name their verified lower bound.
#: Once this source holds that field, both describe history, so they are rewritten.
_NAGAMOCHI_SUMMARY = re.compile(
    _loose("Open. The best known packing gives")
    + r"\s+"
    + _QUOTED.format(figure=r"s\(\d+\)\s+(?:≤|\\le)\s+(?P<upper>[0-9.]+)")
    + r",\s+"
    + _loose("and the strongest lower bound independently verified here is")
    + r"\s+"
    + _QUOTED.format(figure="[0-9.]+")
    + r"\s+"
    + _loose("from Nagamochi’s general theorem, leaving a gap of")
    + r"\s+"
    + _QUOTED.format(figure="[0-9.]+")
    + r"\.\s+"
    + _loose(
        "General closed form: s(N) >= min(ceil(sqrt(N)), sqrt(N - 2*floor(sqrt(N)) + 1) + 1)."
    )
)
_NAGAMOCHI_SECTION = re.compile(
    _loose(
        "The strongest lower bound independently verified in this record is Nagamochi’s "
        "general closed form, which applies to every"
    )
    + r"\s+(?:`N ≥ 4`|\$N \\ge 4\$):"
)


def _decimal(side: Fraction) -> str:
    text = format(Decimal(side.numerator) / Decimal(side.denominator), "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def replayed(registration: Registration) -> dict[int, Fraction]:
    """Cases whose complete coverage replay this packet's receipt records as passed."""
    if not retained_exists(registration.replay_audit):
        return {}
    cases = registration.packet.cases
    record = json.loads(read_retained_text(registration.replay_audit))
    result: dict[int, Fraction] = {}
    for case in record.get("cases", []):
        replay = case.get("replay") or {}
        summary = replay.get("summary") or {}
        n = case["n"]
        if (
            case.get("status") == "PASS"
            and replay.get("status") == "PASS"
            and summary.get("status") == "VERIFIED"
            and summary.get("angle_cases") == 201
            and n in cases
            and Fraction(case["L"]) == cases[n][1]
        ):
            result[n] = cases[n][1]
    return result


def replays(registration: Registration) -> dict[int, tuple[Fraction, Registration]]:
    """The strongest replayed side at each count over this and every earlier packet."""
    best: dict[int, tuple[Fraction, Registration]] = {}
    for earlier in REGISTRATIONS[: _index(registration) + 1]:
        for n, side in replayed(earlier).items():
            if n not in best or side > best[n][0]:
                best[n] = (side, earlier)
    return best


def _case_path(frontier: Path, n: int) -> Path:
    return frontier / f"n-{n:03d}.md"


def _front(frontier: Path, n: int) -> tuple[str, dict[str, Any], str]:
    text = _case_path(frontier, n).read_text(encoding="utf-8")
    _, front, body = text.split("---\n", 2)
    return front, safe_load(front)["packing"], body


def registered(frontier: Path = FRONTIER) -> Registration:
    """The newest registration whose evidence any case record cites."""
    texts = [path.read_text(encoding="utf-8") for path in frontier.glob("n-*.md")]
    held = [
        registration
        for registration in REGISTRATIONS
        if any(f"- {item}\n" in text for text in texts for item in registration.ids)
    ]
    return held[-1] if held else REGISTRATIONS[0]


def _held_by_us(field: Mapping[str, Any] | None) -> bool:
    return bool(field) and bool(set(field.get("evidence") or []) & OURS)


def _superseded_by_record(field: Mapping[str, Any] | None, candidate: Fraction) -> bool:
    """Whether the field already holds a bound this one must not replace.

    Another source's bound at least as high stays; so does any higher wand125 bound, so
    a registration never lowers what a later one wrote.
    """
    if field is None:
        return False
    value = Fraction(Decimal(str(field["value"])))
    return value > candidate if _held_by_us(field) else value >= candidate


def plans(registration: Registration, frontier: Path = FRONTIER) -> list[Plan]:
    current = registered(frontier)
    if _index(registration) < _index(current):
        raise ValueError(
            f"the records hold the {current.date} registration; the {registration.date} "
            "one is older, and writing it would lower bounds"
        )
    cases = registration.packet.cases
    reported = monotone_bounds({n: side for n, (_name, side) in cases.items()})
    proofs = replays(registration)
    verified = (
        monotone_bounds({n: side for n, (side, _) in proofs.items()}, upto=max(cases))
        if proofs
        else {}
    )
    result = []
    for n in sorted(reported):
        if n in registration.superseded_priors:
            continue
        _front_text, payload, _body = _front(frontier, n)
        side, source = reported[n]
        report: Bound | None = Bound(side, source, owner(cases[source][0]))
        if owner(cases[source][0]) is not registration or _superseded_by_record(
            payload.get("reported_lower_bound"), side
        ):
            report = None
        proof: Bound | None = None
        if n in verified:
            side, source = verified[n]
            proof = Bound(side, source, proofs[source][1])
            if _superseded_by_record(payload.get("verified_lower_bound"), side):
                proof = None
        if report is not None or (
            proof is not None
            and (
                proof.registration is registration
                or not _written(payload.get("verified_lower_bound"), proof)
            )
        ):
            result.append(Plan(n, report, proof))
    return result


def _written(field: Mapping[str, Any] | None, proof: Bound) -> bool:
    """Whether the verified field already records exactly this replayed bound."""
    return (
        field is not None
        and field.get("exact_form") == str(proof.side)
        and field.get("evidence") == [proof.registration.replay]
    )


def _block(name: str, value: dict[str, Any]) -> str:
    dumped = yaml.safe_dump({name: value}, allow_unicode=True, sort_keys=False, width=100)
    return "".join("  " + line + "\n" for line in dumped.splitlines())


def _replace_block(front: str, name: str, block: str) -> str:
    pattern = re.compile(rf"^  {name}:\n(?:^    .*\n)*", re.MULTILINE)
    if not pattern.search(front):
        raise ValueError(f"no {name} block")
    return pattern.sub(lambda _match: block, front, count=1)


def _prepend_list(front: str, name: str, items: list[str]) -> str:
    """Insert raw list items at the head of a top-level ``packing`` list."""
    marker = f"\n  {name}:\n"
    index = front.index(marker) + len(marker)
    return front[:index] + "".join(items) + front[index:]


def reported_field(n: int, bound: Bound) -> dict[str, Any]:
    registration = bound.registration
    direct = bound.source == n
    note = (
        "Rectangle-density certificate in Tokoharu's format, reported in the retained source "
        "and accepted there by Tokoharu's unchanged interval checker. The verified lane "
        "records the local replay separately."
        if direct
        else f"wand125's n={bound.source} rectangle-density certificate has mass below {n}, "
        f"so monotonicity carries its bound to n={n}. The verified lane records the local "
        "replay separately."
    )
    return {
        "value": _decimal(bound.side),
        "exact_form": str(bound.side),
        "kind": "counting" if direct else "monotonicity",
        "proved_by": ["wand125"],
        "proved_year": 2026,
        "source_key": registration.source_key,
        "note": note,
        "scope": SCOPE,
        "evidence": [registration.report if direct else registration.monotone_report],
    }


def _mass(registration: Registration, n: int) -> Fraction:
    record = json.loads(read_retained_text(registration.preflight_audit))
    return next(Fraction(case["mass_exact"]) for case in record["cases"] if case["n"] == n)


def _verified_sentence(plan: Plan, registration: Registration) -> str | None:
    n, proof = plan.n, plan.verified
    cases = registration.packet.cases
    if proof is None:
        if n in cases:
            return (
                "This repository’s exact audit checks that the regenerated checker input "
                "is the published one, and checks the mass and net premises; the complete "
                "coverage replay has not yet run here, so the verified lower bound is "
                "unchanged."
            )
        if plan.reported is None:
            return None
        return (
            f"The n{plan.reported.source} certificate’s complete coverage replay has not yet "
            "run here, so the verified lower bound is unchanged."
        )
    claim = f"`s({n}) >= {proof.side} = {_decimal(proof.side)}`"
    if proof.source != n:
        return (
            f"The replayed n{proof.source} certificate carries {claim} here by monotonicity, "
            "which is the verified lower bound."
        )
    if proof.side == cases[n][1]:
        return (
            "The complete 201-direction coverage replay here accepted it again, after "
            "this repository’s exact audit checked that the regenerated checker input is "
            "the published one and checked the mass and net premises, so it is also "
            "verified."
        )
    return (
        "Its complete coverage replay has not yet run here; the verified lower bound is "
        f"{claim}, from the source’s certificate for this count in the "
        f"{proof.registration.date} intake, whose complete 201-direction replay passed here."
    )


def _field_side(field: Mapping[str, Any] | None) -> Fraction | None:
    return None if not field else Fraction(Decimal(str(field["value"])))


def intake(plan: Plan, registration: Registration, payload: Mapping[str, Any]) -> str:
    """The registration's paragraph for one case, whose fields are ``payload`` before it.

    A certificate's own side is written as a bound on ``s(n)`` only when it is what the
    reported or verified field holds once the plan is applied, since `check_case_prose`
    holds that form to the fields; otherwise it is "a direct certificate", and the
    stronger bound another source registered keeps the field and its own paragraph.
    """
    n = plan.n
    cases = registration.packet.cases
    head = registration.head
    sentences: list[str] = []
    monotone = plan.reported is not None and plan.reported.source != n
    if n in cases:
        side = cases[n][1]
        mass = _mass(registration, n)
        fields = (
            plan.reported.side
            if plan.reported is not None
            else _field_side(payload.get("reported_lower_bound")),
            plan.verified.side
            if plan.verified is not None
            else _field_side(payload.get("verified_lower_bound")),
        )
        claim = f"`s({n}) >= {side} = {_decimal(side)}`"
        if monotone or side not in fields:
            claim = f"a direct `{side} = {_decimal(side)}` certificate for this case"
        sentences.append(
            f"{head} reports {claim}, with total mass "
            f"`{mass} = {_decimal(mass)} < {n}`, accepted by Tokoharu’s unchanged interval "
            "checker."
        )
    else:
        sentences.append(f"{head} has no certificate at `n = {n}`.")
    if plan.reported is not None and monotone:
        side, source = plan.reported.side, plan.reported.source
        stronger = "the stronger " if n in cases else ""
        sentences.append(
            f"Its n{source} certificate, of mass `{_mass(registration, source)} < {n}`, gives "
            f"{stronger}`s({n}) >= {side} = {_decimal(side)}` by monotonicity, the reported "
            "lower bound."
        )
    verified = _verified_sentence(plan, registration)
    if verified is not None:
        sentences.append(verified)
    # The first paragraph describing wand125 is where `devtools.state_ai_assistance` says
    # what wand125's README says of AI assistance; this paragraph is that one.
    sentences.append(WAND125.sentence)
    return " ".join(sentences)


_SELECTED_REPORT = re.compile(_loose("The selected external report, ["))
_REPORTED_ONLY = re.compile(
    _loose(
        "This changes the reported source field only; the independently verified lower "
        "bound remains"
    )
    + r"\s+(?P<verified>`[^`]+`|\$[^$]+\$)\."
)


def _retire_selected_report(rest: str, plan: Plan) -> str:
    """The generator's DS7 paragraph calls its report the selected one; it no longer is."""
    rest = _SELECTED_REPORT.sub("The earlier external report, [", rest, count=1)

    def reported_only(match: re.Match[str]) -> str:
        if plan.verified is not None:
            return (
                "wand125’s rectangle-density certificate above has since replaced it in both "
                "the reported and the verified field."
            )
        return (
            "wand125’s rectangle-density certificate above has since replaced it in the "
            "reported field; the independently verified lower bound remains "
            f"{match['verified']}."
        )

    return _REPORTED_ONLY.sub(reported_only, rest, count=1)


def _retire_nagamochi_prose(rest: str, plan: Plan, upper: str) -> str:
    """Point a Nagamochi-form body's summary at the promoted verified lower bound."""
    assert plan.verified is not None
    side, source = plan.verified.side, plan.verified.source
    origin = (
        "wand125’s rectangle-density certificate"
        if source == plan.n
        else f"wand125’s n{source} rectangle-density certificate by monotonicity"
    )

    def summary(match: re.Match[str]) -> str:
        return (
            f"Open. The best known packing gives `s({plan.n}) ≤ {match['upper']}`, and the "
            f"verified lower bound is `s({plan.n}) ≥ {side} = {_decimal(side)}`, "
            f"from {origin}, "
            f"leaving a gap of `{display_gap(upper, _decimal(side))}`."
        )

    rest = _NAGAMOCHI_SUMMARY.sub(summary, rest, count=1)
    return _NAGAMOCHI_SECTION.sub(
        "Nagamochi’s general closed form, the verified lower bound before this certificate, "
        "applies to every `N ≥ 4`:",
        rest,
        count=1,
    )


_FIGURE = r"`s\({n}\)\s+>=\s+(?P<exact>\d+/\d+)\s+=\s+(?P<decimal>[0-9.]+)`"


def _retire_earlier_intake(paragraph: str, plan: Plan, registration: Registration) -> str:
    """Put an earlier registration's intake claims in the past once this one moves them.

    Only claims this plan makes stale are touched: the reported ones when it writes the
    reported field, the verified ones when its own packet's replay raises that field.
    Each rewrite drops the ``s(n) >=`` form, which ``check_case_prose`` holds to the
    current fields, and the rewritten sentence no longer matches, so a rerun is a no-op.
    """
    n, later = plan.n, f"the {registration.date} intake above"
    figure = _FIGURE.format(n=n)
    if plan.reported is not None:
        paragraph = re.sub(
            r"reports\s+" + figure + r",\s+with\s+total\s+mass",
            lambda match: (
                f"reports a direct `{match['exact']} = {match['decimal']}` certificate for "
                f"this case, whose reported bound {later} raises, with total mass"
            ),
            paragraph,
            count=1,
        )
        paragraph = re.sub(
            r"Its\s+n(?P<source>\d+)\s+certificate,\s+of\s+mass\s+(?P<mass>`[^`]+`|\$[^$]+\$),\s+"
            r"gives\s+(?:the\s+stronger\s+)?"
            + figure
            + r"\s+by\s+monotonicity,\s+the\s+reported\s+lower\s+bound\.",
            lambda match: (
                f"Its n{match['source']} certificate, of mass {match['mass']}, gave "
                f"`{match['exact']} = {match['decimal']}` by monotonicity, the reported "
                f"lower bound until {later}."
            ),
            paragraph,
            count=1,
        )
    if plan.verified is not None and plan.verified.registration is registration:
        paragraph = re.sub(
            _loose("so it is also verified."),
            f"so it was also the verified lower bound until {later}.",
            paragraph,
            count=1,
        )
        paragraph = re.sub(
            r"The\s+replayed\s+n(?P<source>\d+)\s+certificate\s+carries\s+"
            + figure
            + r"\s+here\s+by\s+monotonicity,\s+which\s+is\s+the\s+verified\s+lower\s+bound\.",
            lambda match: (
                f"The replayed n{match['source']} certificate carried "
                f"`{match['exact']} = {match['decimal']}` here by monotonicity, the verified "
                f"lower bound until {later}."
            ),
            paragraph,
            count=1,
        )
        paragraph = re.sub(
            r"the\s+verified\s+lower\s+bound\s+is\s+" + figure + r",\s+from",
            lambda match: (
                f"the verified lower bound was `{match['exact']} = {match['decimal']}` "
                f"until {later}, from"
            ),
            paragraph,
            count=1,
        )
    return paragraph


def apply_case(plan: Plan, registration: Registration, frontier: Path = FRONTIER) -> str:
    front, payload, body = _front(frontier, plan.n)
    if plan.reported is not None:
        front = _replace_block(
            front,
            "reported_lower_bound",
            _block("reported_lower_bound", reported_field(plan.n, plan.reported)),
        )
    if plan.verified is not None:
        side = plan.verified.side
        front = _replace_block(
            front,
            "verified_lower_bound",
            _block(
                "verified_lower_bound",
                {
                    "value": _decimal(side),
                    "exact_form": str(side),
                    "evidence": [plan.verified.registration.replay],
                },
            ),
        )
    # Never earlier than a later intake's review: `devtools.apply_upper_bound_packets`
    # reviewed n = 68 on 2026-09-29, after this registration's 2026-09-28. ISO dates
    # order as text.
    reviewed = max(str(payload.get("source_reviewed") or ""), registration.date)
    front = re.sub(
        r"^  source_reviewed: .*$",
        f"  source_reviewed: '{reviewed}'",
        front,
        count=1,
        flags=re.MULTILINE,
    )
    cases = registration.packet.cases
    wanted: list[str] = []
    cited: list[Registration] = []
    if plan.reported is not None:
        cited.append(plan.reported.registration)
        if plan.reported.source == plan.n:
            wanted.append(plan.reported.registration.report)
        else:
            wanted.append(plan.reported.registration.monotone_report)
            if plan.n in cases:
                direct = owner(cases[plan.n][0])
                wanted.append(direct.report)
                cited.append(direct)
    if plan.verified is not None:
        wanted.append(plan.verified.registration.replay)
        cited.append(plan.verified.registration)
    existing = payload.get("evidence") or []
    front = _prepend_list(
        front,
        "evidence",
        [f"  - {item}\n" for item in dict.fromkeys(wanted) if item not in existing],
    )
    keys = {resource.get("key") for resource in payload.get("resources") or []}
    missing = [item.resource for item in dict.fromkeys(cited) if item.source_key not in keys]
    for resource in reversed(missing):
        dumped = yaml.safe_dump([resource], allow_unicode=True, sort_keys=False, width=100)
        front = _prepend_list(
            front, "resources", ["".join("  " + line + "\n" for line in dumped.splitlines())]
        )
    # The intake is written with code spans, and its mathematics made math by the rules
    # `devtools.migrate_math` applied to the rest of the body.
    paragraph = markdown_math(intake(plan, registration, payload))
    title, _, rest = body.partition("\n\n")
    # This registration's paragraph is found by its source and packet, wherever it is;
    # a new one goes under the title. Every other paragraph is someone else's or an
    # earlier registration's, and only the latter's claims are ever retired.
    parts = rest.split("\n\n")
    mine = [index for index, part in enumerate(parts) if registration.wrote(part)]
    if len(mine) > 1:
        raise ValueError(f"n = {plan.n} holds {len(mine)} {registration.date} paragraphs")
    place = mine[0] if mine else 0
    if mine:
        existing_paragraph = parts.pop(place)
        # Flowmark rewraps the paragraph at commit; the same words are the same paragraph.
        if " ".join(existing_paragraph.split()) == paragraph:
            paragraph = existing_paragraph
    earlier = REGISTRATIONS[: _index(registration)]
    rest = "\n\n".join(
        _retire_earlier_intake(part, plan, registration)
        if any(item.wrote(part) for item in earlier)
        else part
        for part in parts
    )
    if plan.reported is not None:
        rest = _retire_selected_report(rest, plan)
    if plan.verified is not None:
        rest = _retire_nagamochi_prose(
            rest, plan, str(payload["reported_upper_bound"]["value"])
        )
    others = rest.split("\n\n")
    if len(others) != len(parts):
        raise ValueError(f"n = {plan.n}: rewriting the body changed its paragraphs")
    # Only what a retirement wrote is still code: the rest is migrated already, and a
    # paragraph no retirement changed is left exactly as it is.
    others = [
        markdown_math(new) if new != old else old
        for new, old in zip(others, parts, strict=True)
    ]
    others.insert(place, paragraph)
    return f"---\n{front}---\n{title}\n\n" + "\n\n".join(others)


def _entry_span(text: str, identifier: str) -> tuple[int, int] | None:
    start = text.find(f"  - id: {identifier}\n")
    if start < 0:
        return None
    end = text.find("\n  - id: ", start + 1)
    return start, len(text) if end < 0 else end


def _scope(values: list[int]) -> str:
    return "{n_values: [" + ", ".join(str(n) for n in sorted(values)) + "]}"


def _set_scope(text: str, identifier: str, values: list[int]) -> str:
    span = _entry_span(text, identifier)
    assert span is not None
    start, end = span
    entry = re.sub(
        r"^    scope: .*$",
        f"    scope: {_scope(values)}",
        text[start:end],
        count=1,
        flags=re.MULTILINE,
    )
    return text[:start] + entry + text[end:]


def _replay_command(text: str, registration: Registration, sources: list[int]) -> str:
    span = _entry_span(text, registration.replay)
    assert span is not None
    start, end = span
    packet = "" if registration.packet is SEPTEMBER_27 else f"--packet {registration.date} "
    direct = " ".join(f"--n {n}" for n in sorted(sources))
    command = (
        "    replay: >-\n"
        '      wand125_replay_output="$(mktemp -d '
        '"${TMPDIR:-/tmp}/wand125-rectangle-replay.XXXXXX")" &&\n'
        "      .venv/bin/python3 -m devtools.audit_wand125_rectangles "
        f'{packet}--out "$wand125_replay_output"\n'
        f"      --replay --workers 2 {direct}\n"
    )
    entry = re.sub(
        r"^    replay: >-\n(?:^      .*\n)+",
        command,
        text[start:end],
        count=1,
        flags=re.MULTILINE,
    )
    return text[:start] + entry + text[end:]


def _citing(texts: Mapping[int, str], identifier: str) -> list[int]:
    """The cases whose front matter cites ``identifier`` anywhere.

    A case keeps an entry in its top-level evidence list after a field stops citing it,
    and every entry a case lists must cover it, so the scope is every such case.
    """
    return sorted(
        n for n, text in texts.items() if f"- {identifier}\n" in text.split("---\n", 2)[1]
    )


def update_evidence(text: str, registration: Registration, texts: Mapping[int, str]) -> str:
    """Insert the registration's missing entries, and keep each scope and replay command."""
    for item in REGISTRATIONS[: _index(registration) + 1]:
        citing = _citing(texts, item.replay)
        if _entry_span(text, item.replay) is None:
            if citing:
                raise ValueError(
                    f"add {item.replay} to evidence.yaml before promoting {citing}"
                )
            continue
        own = replayed(item)
        if not citing or not own:
            continue
        carried = monotone_bounds(own, upto=max(registration.packet.cases))
        sources = sorted({carried[n][1] for n in citing if n in carried})
        text = _replay_command(_set_scope(text, item.replay, citing), item, sources)
    owned = [
        n
        for n, (name, _side) in registration.packet.cases.items()
        if owner(name) is registration
    ]
    wanted = {
        registration.report: sorted(set(owned) | set(_citing(texts, registration.report))),
        registration.monotone_report: _citing(texts, registration.monotone_report),
    }
    for identifier, values in wanted.items():
        if _entry_span(text, identifier) is not None:
            text = _set_scope(text, identifier, values) if values else text
            continue
        if not values:
            continue
        if identifier not in registration.entries:
            raise ValueError(f"add {identifier} to evidence.yaml")
        anchors = [
            span
            for earlier in REGISTRATIONS
            for item in (*sorted(earlier.ids), *earlier.entries)
            if (span := _entry_span(text, item)) is not None
        ]
        end = max(anchors, key=lambda span: span[0])[1]
        entry = (
            registration.entries[identifier]
            .replace("{scope}", _scope(values))
            .replace(
                "{certificate}",
                f"{registration.packet.relative.relative_to('packing')}"
                "/wand125-rectangles/certificates",
            )
        )
        text = text[:end] + "\n" + entry + text[end:]
    return text


def _field(payload: Mapping[str, Any], name: str) -> str:
    field = payload.get(name) or {}
    exact = field.get("exact_form")
    source = field.get("source_key") or ",".join(field.get("evidence") or [])
    shown = f"{field.get('value')}" + (f" ({exact})" if exact else "")
    return f"{shown} {source}".strip()


def decision_table(registration: Registration, frontier: Path) -> str:
    """Every count this packet's certificates reach, and what the registration does there."""
    selected = {plan.n: plan for plan in plans(registration, frontier)}
    cases = registration.packet.cases
    reported = monotone_bounds({n: side for n, (_name, side) in cases.items()})
    rows = [
        "| n | current reported | current verified | certificate bound | decision |",
        "| --- | --- | --- | --- | --- |",
    ]
    for n, (side, source) in sorted(reported.items()):
        _front_text, payload, _body = _front(frontier, n)
        name = cases[source][0]
        via = f"`{name}`" + ("" if source == n else f" by mass, n{source}")
        plan = selected.get(n)
        field = payload.get("reported_lower_bound")
        held = Fraction(Decimal(str(field["value"]))) if field else None
        if plan is not None and plan.reported is not None:
            decision = "write reported"
        elif n in registration.superseded_priors:
            decision = f"superseded prior: {registration.superseded_priors[n]}"
        elif held is not None and not _held_by_us(field) and held >= side:
            decision = f"current reported stronger by {_decimal(held - side)}"
        elif owner(name) is not registration:
            decision = f"held by the {owner(name).date} registration, certificate unchanged"
        else:
            decision = "current reported at least as strong"
        if plan is not None and plan.verified is not None:
            decision += f"; verified {plan.verified.side} ({plan.verified.registration.date})"
        rows.append(
            f"| {n} | {_field(payload, 'reported_lower_bound')} | "
            f"{_field(payload, 'verified_lower_bound')} | "
            f"`{side} = {_decimal(side)}` {via} | {decision} |"
        )
    return "\n".join(rows) + "\n"


def _cpu_hours(registration: Registration, name: str) -> float:
    path = registration.packet.locate(Path("certificates") / name / "verified_angles.jsonl")
    if path is None:
        raise ValueError(f"no packet retains {name}")
    rows = [json.loads(line) for line in read_retained_text(path).splitlines()]
    return sum(float(row["seconds"]) for row in rows) / 3600


def replay_plan(registration: Registration, frontier: Path) -> str:
    """Standing certificates not yet replayed, by how far a replay raises the verified lane.

    Each is replayed into the packet that retains it, so a certificate unchanged since an
    earlier packet is promoted under that packet's replay entry.
    """
    cases = registration.packet.cases
    done = replays(registration)
    verified: dict[int, Fraction] = {}
    for n in range(min(cases), max(cases) + 1):
        field = _front(frontier, n)[1].get("verified_lower_bound")
        verified[n] = Fraction(Decimal(str(field["value"]))) if field else Fraction(0)
    rows = []
    for n, (name, side) in cases.items():
        if n in done and done[n][0] >= side:
            continue
        carried = [m for m in range(n + 1, max(cases) + 1) if verified[m] < side]
        own = side - verified[n]
        if own <= 0 and not carried:
            continue
        home = owner(name)
        rows.append((own, n, name, side, carried, _cpu_hours(home, name), home))
    rows.sort(key=lambda row: (-row[0], row[5]))
    lines = [
        (
            "| order | n | certificate | packet | side | current verified | rise at n | "
            "also raises | upstream CPU-h | cumulative CPU-h | note |"
        ),
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    total = 0.0
    for order, (own, n, name, side, carried, hours, home) in enumerate(rows, 1):
        total += hours
        others = ", ".join(f"n{m} +{float(side - verified[m]):.4f}" for m in carried)
        note = registration.superseded_priors.get(n, "")
        lines.append(
            f"| {order} | {n} | `{name}` | {home.date} | `{side} = {_decimal(side)}` | "
            f"{float(verified[n]):.6f} | {float(own):+.4f} | {others} | {hours:.2f} | "
            f"{total:.1f} | {note} |"
        )
    lines.extend(
        ["", "Replay commands, from `packing/`, one `--n` per count, in the order above:", ""]
    )
    for home in dict.fromkeys(row[6] for row in rows):
        counts = " ".join(f"--n {row[1]}" for row in rows if row[6] is home)
        lines.append(
            f"    .venv/bin/python3 -m devtools.audit_wand125_rectangles --packet {home.date} "
            f"--out resources/web/{home.packet.directory.name}/receipts/replay "
            f"--resume --replay --workers 2 {counts}"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    parser.add_argument(
        "--packet", choices=tuple(BY_DATE), help="default: the registration the records hold"
    )
    parser.add_argument("--frontier", type=Path, default=FRONTIER, help="for a dry run")
    parser.add_argument("--plan", action="store_true", help="print the decision table")
    parser.add_argument("--replay-plan", action="store_true", help="print the replay order")
    args = parser.parse_args()
    frontier: Path = args.frontier
    registration = registered(frontier) if args.packet is None else BY_DATE[args.packet]
    if args.plan or args.replay_plan:
        print(
            decision_table(registration, frontier)
            if args.plan
            else replay_plan(registration, frontier)
        )
        return 0
    drift: list[str] = []
    selected = plans(registration, frontier)
    texts = {
        int(path.stem.removeprefix("n-")): path.read_text(encoding="utf-8")
        for path in frontier.glob("n-*.md")
    }
    for plan in selected:
        path = _case_path(frontier, plan.n)
        rendered = apply_case(plan, registration, frontier)
        texts[plan.n] = rendered
        if rendered != path.read_text(encoding="utf-8"):
            drift.append(str(path))
            if not args.check:
                atomic_write_text(path, rendered)
    evidence = frontier / "evidence.yaml"
    text = evidence.read_text(encoding="utf-8")
    updated = update_evidence(text, registration, texts)
    if updated != text:
        drift.append(str(evidence))
        if not args.check:
            atomic_write_text(evidence, updated)
    for item in drift:
        shown = Path(item).relative_to(ROOT) if Path(item).is_relative_to(ROOT) else item
        print(("drift: " if args.check else "wrote: ") + str(shown))
    return 1 if args.check and drift else 0


if __name__ == "__main__":
    sys.exit(main())
