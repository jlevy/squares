"""Decide the beyond-horizon rows of a report exactly, from its retained packet.

A report beyond the ``n <= 324`` corpus is recorded as dated beyond-horizon rows of its
source, at assurance ``reported``, once its certificates are retained and replayed here.
Issues #678 and #715 each had a module of their own (`devtools.couzo_678_replay`,
`devtools.couzo_715_replay`); this one takes the same filtered decision and declares each
report it decides as a `Release`, so a further report of the same kind is a declaration and
not a module. `RELEASES` holds 17, each decided at or below ``LIMIT = 1024``: the six
issues below, and 11 publications in watched repositories that no issue reports
(**Publications no issue reports**, `WATCHED`):

- **#666**, Joost de Winter: 19 certificates ``square-packing-above-324/nNNNN.cert`` in
  JoostdeWinter/joostdewinter.github.io. The issue pins ``b3152f52``, which no branch
  reaches since the site's history was rewritten; ``b9cdc16b``, with the same commit time,
  holds the identical folder, and the packet retains it from ``643dc9a``, which adds the
  folder's MIT licence and changes no certificate. Its 11 rows at or below 1024 are decided;
  the 8 above wait on the owner (think-f2io), retained and not decided.
- **#670**, **#672** and **#675**, Francisco Couzo: the rows beyond the corpus of the three
  issues whose in-corpus rows T-226 to T-228 register, from the same packets and pins
  (``23aff0c6``, ``af8cb795``, ``c6da0fc7``). #670 and #672 link root
  ``certificates/nN.cert``; #675 links ``certificates/best/nN.cert``, and its rows 992 and
  995 delete one square from the 993 and 996 certificates.
- **#719**, Mykhailo Polkovskyi: 122 certificates ``certificates/n-N.cert`` in
  Mishapolk/square-packing-records at ``12fc4667``, whose table names each file and its
  SHA-256. The source states no licence, so the packet keeps no upstream byte: each
  certificate is the exact Witness/v2 fact `devtools.upper_bound_reports` derived from a
  checkout at the pin (``derived``), held there to the digest the packet pins. Its 112 rows
  beyond the corpus at or below 1024 are decided; 105 and 204 are in the corpus, and the 8
  above 1024 wait on the owner.
- **#732**, Mykhailo Polkovskyi: 5,468 certificates ``certificates/NNNN-NNNN/nN.cert`` in the
  same repository, indexed by ``certificates/manifest.json``, whose SHA-256 the issue states;
  the packet pins ``17cc2201``, which adds only an MIT licence to the commit the issue
  describes. The issue has no table of rows, so its packet declares the rows its own walk
  records (``declare-rows``, `declares_rows`), 77 of the 390 at or below 1024, and retains
  those certificates; the 5,078 above 1024 wait on the owner (**Issue #732**).

Each certificate is ``n S``, then ``n`` rows ``x y t`` (centre and ``t = tan(theta/2)``),
and lines that begin with ``#`` are comments; the header is authoritative. The Couzo and
de Winter issues print ``S`` rounded up at 12 places. #719 prints ``S``'s binary64 value at
16 places (``rounding = "binary64"``), which lies below ``S`` at 76 of its rows, so its
rows record ``S`` rounded up at 16 places instead.

**The decision** is `devtools.couzo_678_replay`'s, reused unchanged: route ``sqpack``
through ``sqpack.witness`` and ``sqpack.verify``'s predicates, route ``independent``
through ``devtools.check_rational_witness_independent``'s, over every wall and every pair
whose centres are closer than ``sqrt 2`` by exact comparison, with its six controls on each
certificate a row reads whole. That module's docstring states the filter's lemma and the
controls. A deletion row is decided as its certificate's first ``n`` poses at the
certificate's side, since removing squares from a packing leaves a packing; the controls
are decided on the certificate's own row, which ``check`` requires the release to read
whole.

**The records.** Each packet keeps, under ``receipts/``, the filtered replay
(``filtered-exact-replay.json``), the first commit holding each certificate
(``first-commits.json``, from a clone of the source), an all-pairs sample
(``exhaustive-sample.json``, the maintained kernel of `devtools.evand_arrangement_reports`
on chosen rows) and the comparison with Göbel's classical constructions
(``goebel-comparison.json``, the 15 October packet's retained program). ``claims-record``
writes ``acquisition/beyond-horizon-rows.json``, the record ``check_source_coverage``
reads the source's beyond-horizon rows from: each row's print, its exact side and that
side rounded up at 16 places. The Couzo packets are also `devtools.upper_bound_reports`
packets, whose importer owns ``acquisition/beyond-horizon-claims.json`` for the counts its
declaration requests, and those requests stop at the corpus; so this module's record
has a name of its own, the same in all four packets. ``check`` reads every receipt and
the record back against the packet and the issue, and ``check --replay`` decides every
row and control again.

**The rows.** ``coverage-plan`` reads each row's disposition from its release's
report-order ledger (`Walk`; `planned_rows`): recorded at its count, it is superseded by the
next report the walk records there, or it is the count's current row; a row the walk does
not record, as #719's 366, plans no row. The four reports of 17 and 18 October are walked
by ``campaign/issue-intake/upper-bounds-backlog-20261022``, and #719 by
``campaign/issue-intake/upper-bounds-issue719-20261022``. Where a release's row is the
first report the walk records at a count, the count's start names that release as its
successor (`planned_supersessions`), whether the release's row is current or a later
report's row supersedes it in turn: the four came before #678, #686 and #715, so a start
those later reports had superseded on ``main`` names the backlog report that beat it
first. A report the walk records whose own import has not yet landed (`Awaiting`) has no
row, so the chain passes over it until that import writes one: Couzo's 4e4c8ce and 5a299b4
publications awaited theirs that way until the history walk recorded them, and the #719
walk now names their sources. #715's re-certifications of them below the 12-place print
restate them, by the owner's answer of 23 October (think-fwa9), so neither walk records
them. ``check`` holds
``frontier/source-coverage.yaml`` to that plan, and holds every count a walk reaches beyond
the corpus to ``LIMIT`` to one chain in report order (`chain_problems`): the start, then
each recorded report's row, each superseded by the next, the last current or superseded by
a report the walk does not reach. A planned current row the register shows superseded by
such a later report holds the plan too (`coverage_problems`).

**Publications no issue reports.** A watched repository's commit is a report from the
time it reached GitHub, as the owner ruled on 14 October, and a `Release` with no issue:
its packet declares the rows its walk records (``declare-rows``, `read_declared_rows`), and
a second report retained in one packet has its own source, record and receipts. A walk
holds back a publication that waits on an owner decision rather than an import (`Held`):
a construction with no certificate file, or an index bound deleting squares from one
(`HELD_CLASSES`). Two holds are settled by the owner's answers of 23 October
(`Held.answer`): a certificate its author withdrew from an issue is kept out of the record
(think-8m4k), and an index bound deleting a square from the next count's published
certificate is an earlier report (D6, think-f2io), so a later equal side, as #732's 985,
is not recorded; that it has no row of its own is D6's recommendation, which the owner has
not confirmed (think-kzme). A verdict the walk decides
only against held publications rests on them (`Resting`): an answer that leaves a hold
out reruns the walk, and ``held-dependents`` says what each such answer would reopen
(`refusal_flips`). ``check`` holds every hold, every resting verdict and every declaration
to the walk.

**The owner's rulings.** The history, #719 and #732 walks apply two answers of the owner
of 23 October 2026 as rules of the walk (`WALK_RULINGS`, `devtools.intake_ledger.RULINGS`):
a side below an earlier report by less than one unit in the 12th place, at the same
12-place print, restates it and is not recorded (think-fwa9); and Göbel's classical
construction at each count is an earlier report, so a side at or above it is not
recorded (think-8krd, #613). A register row at or above Göbel's construction stays listed
as its source printed it, marked ``above-classical-construction`` with the construction it
is above, and holds no count (`construction_problems`). #719's 631, another holder's
re-certification #722 recorded, is in the first answer's words and waits on the owner
(think-oqjd), so the walks record it as before.

**The history walk.** ``campaign/issue-intake/upper-bounds-couzo-history-20261022`` walks
every count from 325 to 1024 from starts frozen at ``main`` a97b712b9 (#479's merge, whose
only beyond-horizon rows are the two 8 October sources): every row source since, at its
rows' exact sides, and every side a watched repository published below the start, each at
the first commit of any of them that stated it. ``history-publications`` scans clones of
the repositories into the 4e4c8ce packet's ``receipts/history-publications.json`` and
freezes the starts from the coverage register of a checkout of that ``main``, read by its
path; ``history-sources`` transcribes the walk's ``sources.yaml`` from the scan and the
register. Where an earlier walk's starts were frozen later and it lacks a publication the
history walk inserts between two of its reports, the register may lead from one to the
other through that publication's row (`bridged`).

**Issue #732.** ``campaign/issue-intake/upper-bounds-issue732-20261023`` walks the 390 counts
#732 claims from starts frozen at ``main`` fcf2f96a5 (#730's merge), which read each row at
the exact side its source's claims record states (`devtools.intake_ledger.beyond_member`).
``source-history`` reads a clone of the author's repository, only the certificates whose
paths name a count from 325 to 1024, and writes the packet's
``receipts/source-history.json``: every certificate at the pin, held to the manifest's path,
digest and exact bound, and every side the repository published there with the first commit
that held it. The repository is watched, so ``release-sources`` transcribes the walk's
``sources.yaml`` from that receipt, the history scan and #715's held re-certifications: the
issue's claims, dated by the issue with the first commit of each side, the author's own
earlier sides, and every watched publication, each where it is strictly below the start
(`release_walk_sources`). The walk holds what #730's walk holds, and keeps out the author's
own files at the nine counts #719's edit withdrew (`WITHDRAWN`, think-8m4k); 499, below
#719's row by 8.66e-13 at the same print, restates it (think-fwa9).

**Earlier publications.** ``earlier`` reads clones of the watched repositories and writes
``receipts/earlier-publications.json`` for a release: at each of its counts, every
certificate and index bound published before the release's row, strictly below the record's
standing side there, with the commit that first held it. The release's ledger transcribes
them as reports (``ledger-sources``).

From ``packing/``, with the project interpreter::

    python -m devtools.beyond_horizon_replay filtered [--issue N|LABEL ...] [--workers 2]
    python -m devtools.beyond_horizon_replay first-commits --issue N --clone CLONE
    python -m devtools.beyond_horizon_replay exhaustive --issue N --n 922 [--workers 2]
    python -m devtools.beyond_horizon_replay goebel
    python -m devtools.beyond_horizon_replay claims-record
    python -m devtools.beyond_horizon_replay earlier --issue 719 --couzo CLONE
    python -m devtools.beyond_horizon_replay ledger-sources --issue 719
    python -m devtools.beyond_horizon_replay history-publications \
        --start-coverage CHECKOUT/packing/frontier/source-coverage.yaml \
        --clone franciscouzo/square-packing=CLONE evand/square-packing=CLONE ...
    python -m devtools.beyond_horizon_replay history-sources --read-on DATE
    python -m devtools.beyond_horizon_replay source-history --issue 732 --clone CLONE
    python -m devtools.beyond_horizon_replay release-sources --issue 732 --read-on DATE
    python -m devtools.beyond_horizon_replay declare-rows
    python -m devtools.beyond_horizon_replay coverage-plan
    python -m devtools.beyond_horizon_replay held-dependents
    python -m devtools.beyond_horizon_replay check [--replay [--workers 2]]

A command's ``--issue`` takes an issue's number or a publication's label,
``owner/name@commit``.

A finite packing certifies an upper bound and nothing more: novelty, rigidity and
optimality are not decided here, and neither are the sources' credit and lineage
statements, which the receipt copies from the per-count metadata where a packet retains it.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import importlib.util
import json
import platform
import re
import subprocess
import time
from collections.abc import Callable, Iterable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any, NamedTuple

from strif import atomic_output_file

from devtools import acquire_source
from devtools import couzo_678_replay as base
from devtools import couzo_715_replay as couzo_715
from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools import upper_bound_reports as reports
from devtools.retained_data import read_retained_bytes, read_retained_text
from sqpack.retained_json import dumps as retained_dumps
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
WEB = ROOT / "resources/web"
#: The largest count this module decides; above it every row waits on the owner (D1).
LIMIT = 1024
PLACES = 12
ISSUE = Path("acquisition/issue.json")
RECORD = Path("acquisition/beyond-horizon-rows.json")
RECEIPTS = Path("receipts")
#: A publication no issue reports declares its rows here (`Release`, `declare_rows`).
DECLARED = Path("acquisition/watched-release.json")
WATCHED_FORMAT = "beyond-horizon-watched-release-v1"
FILTERED = Path("receipts/filtered-exact-replay.json")
FIRST_COMMITS = Path("receipts/first-commits.json")
EXHAUSTIVE = Path("receipts/exhaustive-sample.json")
GOEBEL = Path("receipts/goebel-comparison.json")
FILTERED_FORMAT = "beyond-horizon-filtered-exact-replay-v1"
FIRST_COMMITS_FORMAT = "beyond-horizon-first-commits-v1"
EXHAUSTIVE_FORMAT = "beyond-horizon-exhaustive-sample-v1"
GOEBEL_FORMAT = "beyond-horizon-goebel-comparison-v1"
EARLIER = Path("receipts/earlier-publications.json")
EARLIER_FORMAT = "beyond-horizon-earlier-publications-v1"
INTAKE = ROOT / "campaign/issue-intake"
COVERAGE = ROOT / "frontier/source-coverage.yaml"
RECORDED, NOT_RECORDED, UNDECIDED = "recorded", "not recorded", "undecided"
#: How an issue prints a side: rounded up at 12 places, or as the binary64 value of the
#: exact side at 16 places, which may lie below it (#719).
UP, BINARY64 = "up", "binary64"
_START_ROW = re.compile(r"beyond-horizon row (\S+)")
_BEAD = re.compile(r"think-[a-z0-9]{4}")


@dataclass(frozen=True, slots=True)
class Awaiting:
    """A report a walk records whose rows are its own import's and not yet in the register.

    ``counts`` limits it to those counts (None: every count); ``bead`` owns the import. The
    chain at such a count passes over the report until that import lands, when the walk's
    declaration names its source instead.
    """

    bead: str
    counts: frozenset[int] | None = None


#: Why a walk holds a report's publication back from a row: each class waits on an owner
#: decision, which its `Held` names by bead, or is settled by the owner's answer, which it
#: states (`HELD_CLASSES`, `Held.answer`). The owner answered two classes on 23 October
#: 2026 as rules of the walk itself (`devtools.intake_ledger.RULINGS`), so they are no
#: longer holds: a re-certification below the 12-place print restates the report it beats
#: (think-fwa9), and a side above Göbel's classical construction is above an earlier
#: report (think-8krd).
CONSEQUENCE, RECIPE, WITHDRAWN = "consequence", "recipe", "withdrawn"
HELD_CLASSES = {
    CONSEQUENCE: (
        "an index bound that deletes squares from a larger count's certificate or from a "
        "construction the index states, with no certificate file at its own count; one "
        "deleting a square from the next count's published certificate is an earlier report, "
        "as the owner answered on 23 October 2026 (D6, think-f2io)"
    ),
    RECIPE: (
        "a construction an index or table states with no certificate file of its own: an "
        "L-border, tiling or composite bound, or a classical construction (Göbel's squares, "
        "Friedman's off-centre family) or an L-border extension of one"
    ),
    WITHDRAWN: (
        "a certificate in the reporter's own watched repository that his issue withdrew, at a "
        "count where his later release claims a lower side: not a report, as the owner "
        "answered on 23 October 2026 (think-8m4k)"
    ),
}
#: The owner's answer that settles the withdrawn class (`Held.answer`).
WITHDRAWN_ANSWER = (
    "the owner's answer of 23 October 2026 (think-8m4k): a watched certificate its author "
    "withdrew from an issue, claiming a lower file later, is not a report, so the walk "
    "keeps it out of the record"
)
#: The owner's answer that settles an index bound deleting one square from the next
#: count's published certificate (`Held.answer`; D6 on think-f2io). The owner selected
#: the option labelled "Yes, an earlier report (Recommended)". The rest is the question
#: the coordinator asked, not the owner's words: whether a side obtained by deleting a
#: square from a neighbour's certificate, Couzo's 985 from his 986, is an earlier report,
#: with that option described as "A published deletion bound counts like any stated
#: bound; a later equal or higher side is not recorded". The walk records it and the chain
#: passes over it; that it has no row of its own is the decision's recommendation, which
#: the owner has not confirmed (think-kzme). A bound deleting more squares, or from a
#: farther count, is outside the question's words and stays held.
DELETION_ANSWER = (
    "the owner's answer of 23 October 2026 on D6 (think-f2io), the option labelled "
    '"Yes, an earlier report (Recommended)" in the question the coordinator asked, whether '
    "a side obtained by deleting a square from a neighbour's certificate is an earlier "
    "report; so a later equal or higher side is not recorded, and on the decision's "
    "recommendation, which the owner has not confirmed (think-kzme), it has no row of its own"
)
#: What a hold's class is called where a sentence counts holds (`held_sentence`).
HELD_NAMES = {
    CONSEQUENCE: "index deletion bounds",
    RECIPE: "constructions with no certificate file",
    WITHDRAWN: "certificates their author withdrew from an issue",
}
HELD_NAME = {
    CONSEQUENCE: "index deletion bound",
    RECIPE: "construction with no certificate file",
    WITHDRAWN: "certificate its author withdrew from an issue",
}


@dataclass(frozen=True, slots=True)
class Held:
    """A report's publications a walk records that wait on an owner decision, or that an
    answer has settled out of the record.

    ``kind`` is the class (`HELD_CLASSES`), ``bead`` the decision's bead and ``counts`` the
    counts held; ``also`` names any further decision the hold waits on, and ``note`` says
    what the publications are where the class alone does not. Unlike `Awaiting`, nothing is
    pending but the decision: the walk records the publication, so it stands at its count,
    and no row may hold it until the owner answers, when the walk's declaration drops it
    and a row is written. The chain passes over it as over a report awaiting its import.
    ``answer`` states the owner's answer where it settles the publication's disposition for
    good: a certificate its author withdrew is kept out of the record (`WITHDRAWN_ANSWER`),
    and an index deletion bound from a published certificate is an earlier report with no
    row of its own (`DELETION_ANSWER`). The hold is then the settled disposition, nothing
    waits, and a verdict decided against it rests on nothing (`resting_on_holds`).

    A later report the walk decides only against held publications rests on them
    (`Resting`, `resting_on_holds`). An answer that leaves a hold out of the record takes
    the publication out of the walk too, so the walk is run again and those verdicts are
    decided afresh (`refusal_flips` says which would then be recorded).
    """

    kind: str
    bead: str
    counts: frozenset[int]
    also: tuple[str, ...] = ()
    note: str = ""
    answer: str = ""


@dataclass(frozen=True, slots=True)
class Resting:
    """A report's verdicts a walk decided only against publications it holds (`Held`).

    At each of ``counts`` the report's ``verdict`` (not recorded, or undecided) names only
    held publications, all of the classes ``kinds``. Each stands while its holds stand: an
    answer that leaves one of them out reruns the walk (`refusal_flips`).
    """

    report: str
    verdict: str
    kinds: tuple[str, ...]
    counts: frozenset[int]


@dataclass(frozen=True, slots=True)
class Walk:
    """A report-order ledger, ``campaign/issue-intake/<name>/``, whose verdicts plan rows.

    ``later`` maps each report the walk records after its releases to the source whose
    dated rows record it; ``awaiting`` names the reports it records that have no rows yet,
    ``held`` the publications it records that wait on an owner decision (`Held`), and
    ``resting`` the verdicts it decided only against those (`Resting`), which ``check``
    holds to the ledger (`resting_problems`).
    """

    name: str
    later: Mapping[str, str]
    awaiting: Mapping[str, Awaiting]
    held: Mapping[str, tuple[Held, ...]] = field(default_factory=dict)
    resting: tuple[Resting, ...] = ()

    @property
    def directory(self) -> Path:
        return INTAKE / self.name

    @property
    def ledger(self) -> Path:
        return self.directory / "ledger.json"

    def holds(self, report: str, n: int) -> Held | None:
        """The decision a report's publication at ``n`` waits on, if the walk holds it."""
        return next((item for item in self.held.get(report, ()) if n in item.counts), None)


def _held_715() -> frozenset[int]:
    """#715's re-certifications of Couzo's 4e4c8ce certificates below the print, which the
    22 October ledger left to a decision, as #715's committed receipt sets them: the owner's
    answer of 23 October (think-fwa9) makes each a restatement, which the walks decide."""
    return frozenset(couzo_715.counts_in(couzo_715.HELD))


BACKLOG = "upper-bounds-backlog-20261022"
ISSUE_719 = "upper-bounds-issue719-20261022"
#: The walk of every count from 325 to 1024 since ``main`` a97b712b9, Couzo's watched history
#: and every row source since then in report order.
HISTORY = "upper-bounds-couzo-history-20261022"
#: The history walk's starts: ``main`` at #479's merge, 2026-10-10T00:28:19Z, the last
#: ``main`` whose only beyond-horizon rows are the two 8 October sources.
HISTORY_READ_AT_MAIN = "a97b712b94a138ebe9998070dd08d0ba0f320e09"
#: The counts the history walk reaches: beyond the corpus to ``LIMIT``.
HISTORY_COUNTS = range(reports.HORIZON + 1, LIMIT + 1)
#: The sources whose rows are the history walk's starts, and so are not walked.
HISTORY_START_SOURCES = (
    "couzo-extended-range-reports-2026-10-08",
    "couzo-extended-range-updates-2026-10-08",
)
#: The row sources an issue reported: the walk dates their claims by the issue, as the
#: backlog and #719 ledgers do, and records where a watched repository published a side a
#: little earlier (``first_committed``). Every other row source is a watched repository's
#: publication, dated by the first commit that published each side.
HISTORY_ISSUES: dict[str, tuple[int, str, str]] = {
    "de-winter-issue666-2026-10-17": (666, "Joost de Winter", "think-3m10"),
    "couzo-issue670-2026-10-17": (670, "Francisco Couzo", "think-f28n"),
    "couzo-issue672-2026-10-17": (672, "Francisco Couzo", "think-2vjc"),
    "couzo-issue675-2026-10-18": (675, "Francisco Couzo", "think-pvav"),
    "couzo-issue678-2026-10-18": (678, "Francisco Couzo", "think-xu4d"),
    "muglich-issue686-2026-10-19": (686, "Darius Muglich", "think-9vjn"),
    "evand-n343-sweep-2026-10-20": (702, "Evan Daniel", "think-wuxt"),
    "couzo-issue715-2026-10-21": (715, "Francisco Couzo", "think-cyal"),
    "mishapolk-issue719-2026-10-22": (719, "Mykhailo Polkovskyi", "think-xyhn"),
}


#: The walk of issue #732's claims at 325 to 1024, from starts frozen at ``main`` at #730's
#: merge, the first ``main`` that holds Couzo's history (`ISSUE_732_READ_AT_MAIN`).
ISSUE_732 = "upper-bounds-issue732-20261023"
ISSUE_732_READ_AT_MAIN = "fcf2f96a5213bb6cc076bcba90e353a661db773a"
MISHAPOLK_REPOSITORY = "Mishapolk/square-packing-records"
MISHAPOLK_URL = f"https://github.com/{MISHAPOLK_REPOSITORY}"


def history_label(source: str) -> str:
    """How the history walk names a row source's report: its issue, else its source id."""
    issue = HISTORY_ISSUES.get(source)
    return f"#{issue[0]}" if issue is not None else source


#: The row sources the history walk takes after its starts, each the report of its rows.
HISTORY_SOURCES = (
    "fang-two-wedge-certificates-2026-10-10",
    "evand-record-hunt3-2026-10-10",
    "couzo-certificates-2026-10-11",
    "couzo-certificates-2026-10-12",
    "fang-direct-certificates-2026-10-13",
    "fang-excess-theorem-2026-10-13",
    "couzo-issue583-2026-10-13",
    "evand-compositions-2026-10-13",
    "couzo-certificates-2026-10-13",
    "evand-fresh-compositions-2026-10-14",
    "couzo-verified-bounds-2026-10-14",
    "couzo-certificates-2026-10-14",
    "de-winter-issue666-2026-10-17",
    "couzo-issue670-2026-10-17",
    "couzo-issue672-2026-10-17",
    "couzo-issue675-2026-10-18",
    "couzo-issue678-2026-10-18",
    "muglich-issue686-2026-10-19",
    "evand-n343-sweep-2026-10-20",
    "couzo-issue715-2026-10-21",
    "mishapolk-issue719-2026-10-22",
)


def _held(
    kind: str,
    bead: str,
    counts: str,
    *,
    also: tuple[str, ...] = (),
    note: str = "",
    answer: str = "",
) -> Held:
    """A `Held` whose counts are written out, separated by spaces."""
    return Held(kind, bead, frozenset(int(n) for n in counts.split()), also, note, answer)


def _resting(report: str, verdict: str, kinds: str, counts: str) -> Resting:
    """A `Resting` whose classes and counts are written out, separated by spaces."""
    return Resting(
        report, verdict, tuple(kinds.split()), frozenset(int(n) for n in counts.split())
    )


#: 23aff0c's index states the constructions it holds back (``upper_bounds.json`` at the
#: pin, pinned by digest in the couzo-issue670-2026-10-17 packet): Göbel's squares (27,
#: credited "Frits Göbel; family formulas generalized by David Ellsworth") and Friedman's
#: off-centre family (19, citing this repository's ``packing/cases/gobel_offcentre``), 41
#: of the 46 as L-border extensions and 368, 543, 626, 752 and 849 bare; and 15 bounds
#: that delete one or two squares from Friedman's constructions at 368, 407, 448, 543,
#: 590, 639, 752, 849, 908 and 969. #613's answer (think-8krd) makes Göbel's own
#: constructions earlier reports, and every one of these is below Göbel's construction at
#: its count, so they wait on D2 and D6 (think-f2io) and on whether Friedman's
#: constructions count as Göbel's do (think-zkxy).
_CLASSICAL_23AFF0C = "Göbel's squares and Friedman's off-centre family"


#: What the history walk records and holds back from a row, by report and class: index
#: deletion bounds and constructions with no certificate file, waiting on D2 (think-f2io);
#: 23aff0c's extend Friedman's constructions (`_CLASSICAL_23AFF0C`), so they wait on
#: think-zkxy too. 36 of 4e4c8ce's 39 deletion bounds each delete one square from the next
#: count's certificate and are settled by the owner's D6 answer (`DELETION_ANSWER`); the
#: other three delete two or three squares and wait on think-kzme. ``check`` holds each to
#: the walk.
HISTORY_HELD: dict[str, tuple[Held, ...]] = {
    "TheSnakeFang/squarepack-certs@bef5c42": (
        _held(
            RECIPE,
            "think-f2io",
            "420 462 506 552 600 650 702 756 757 812 813 870 871 930 931 992 993",
        ),
    ),
    "franciscouzo/square-packing@487b058": (_held(RECIPE, "think-f2io", "327"),),
    "franciscouzo/square-packing@4e4c8ce": (
        _held(
            CONSEQUENCE,
            "think-f2io",
            "505 533 549 551 580 583 589 593 595 598 629 632 638 642 680 683 693 700 "
            "733 743 753 788 798 805 807 845 855 864 869 904 923 928 965 979 985 989",
            note="each deleting one square from the next count's 4e4c8ce certificate",
            answer=DELETION_ANSWER,
        ),
        _held(
            CONSEQUENCE,
            "think-kzme",
            "751 752 927",
            note=(
                "deleting three squares from 754's certificate, two from 754's and two from "
                "929's (certified_bounds.json at 4e4c8ce), beyond the D6 answer's words"
            ),
        ),
    ),
    "franciscouzo/square-packing@23aff0c": (
        _held(
            CONSEQUENCE,
            "think-f2io",
            "367 406 447 541 542 588 589 638 751 847 848 906 907 967 968",
            also=("think-zkxy",),
            note=(
                "deletions from Friedman's off-centre constructions, which no certificate "
                "file states, so D6's answer on deletions from certificates does not reach "
                "them"
            ),
        ),
        _held(
            RECIPE,
            "think-f2io",
            "368 407 448 457 491 500 533 534 543 545 580 581 590 592 626 629 630 639 "
            "641 677 680 681 690 730 733 734 741 752 785 788 789 796 842 845 846 849 "
            "901 904 905 908 962 965 966 969 981 982",
            also=("think-zkxy",),
            note=f"{_CLASSICAL_23AFF0C}, 41 of them as L-border extensions",
        ),
    ),
}
#: The history walk's verdicts decided only against publications it holds for a decision
#: still owed (`Resting`), by report, verdict and the classes they rest on: recipes, and
#: 23aff0c's deletions from Friedman's constructions. ``refusal_flips`` says which would be
#: recorded if an answer left those out. ``check`` holds the list to the ledger.
HISTORY_RESTING = (
    _resting("TheSnakeFang/squarepack-certs@5f3bdbf", NOT_RECORDED, RECIPE, "757 813 871"),
    _resting("franciscouzo/square-packing@23aff0c", NOT_RECORDED, RECIPE, "327"),
    _resting("franciscouzo/square-packing@43ac7d2", UNDECIDED, RECIPE, "812 930 931 992 993"),
    _resting("franciscouzo/square-packing@487b058", NOT_RECORDED, RECIPE, "812 930"),
    _resting("franciscouzo/square-packing@4e4c8ce", NOT_RECORDED, RECIPE, "327"),
    _resting(
        "franciscouzo/square-packing@5a299b4",
        NOT_RECORDED,
        CONSEQUENCE,
        "406 447 588 589 638 906 907 967 968",
    ),
    _resting(
        "franciscouzo/square-packing@5a299b4",
        NOT_RECORDED,
        RECIPE,
        "327 407 448 457 491 533 534 580 581 590 629 630 639 677 680 681 690 730 733 734 "
        "741 785 788 789 796 842 845 846 901 904 905 908 962 965 966 969 981 982",
    ),
)
#: The publications the #732 walk records that the history walk holds, at the counts the
#: walk records them: the history walk's holds there (`HISTORY_HELD`).
_HELD_IN_732 = (
    (
        "franciscouzo/square-packing@23aff0c",
        (
            "367 368 406 407 448 457 491 533 534 541 542 543 580 581 588 589 590 626 629 630 "
            "638 639 677 680 681 690 730 733 734 741 785 788 789 796 842 845 846 847 848 849 "
            "901 904 905 906 907 908 962 965 966 967 968 969 981 982"
        ),
    ),
    (
        "franciscouzo/square-packing@4e4c8ce",
        "533 580 583 589 629 632 638 680 683 733 788 845 855 904 965 985",
    ),
)
#: The #732 walk's verdicts decided only against publications it holds for a decision
#: still owed (`Resting`): those on recipes and on 23aff0c's deletions from Friedman's
#: constructions are reopened by `held-dependents`. None rests on a settled hold: the
#: withdrawn files (think-8m4k), or 4e4c8ce's deletion bounds, earlier reports by the D6
#: answer, against which #732's 985 is not recorded.
_RESTING_732 = (
    _resting(
        "#732",
        NOT_RECORDED,
        CONSEQUENCE,
        "367 406 541 542 588 589 638 847 848 906 907 967 968",
    ),
    _resting(
        "#732",
        NOT_RECORDED,
        RECIPE,
        "368 407 448 457 491 533 534 543 580 581 590 626 629 630 639 677 680 681 690 "
        "730 733 734 741 785 788 789 796 842 845 846 849 901 904 905 908 962 965 966 "
        "969 981 982",
    ),
    _resting(
        f"{MISHAPOLK_REPOSITORY}@1851c2c",
        NOT_RECORDED,
        CONSEQUENCE,
        "367 406 541 542 588 589 638 847",
    ),
    _resting(
        f"{MISHAPOLK_REPOSITORY}@1851c2c",
        NOT_RECORDED,
        RECIPE,
        "368 407 448 457 491 533 534 543 580 581 590 626 629 630 639 677 680 681 690 "
        "730 733 734 741 785 788 789 796 842 845 846",
    ),
    _resting(f"{MISHAPOLK_REPOSITORY}@8a488a1", NOT_RECORDED, CONSEQUENCE, "848"),
    _resting(f"{MISHAPOLK_REPOSITORY}@8a488a1", NOT_RECORDED, RECIPE, "849"),
    _resting(
        "franciscouzo/square-packing@5a299b4",
        NOT_RECORDED,
        CONSEQUENCE,
        "406 588 589 638 906 907 967 968",
    ),
    _resting(
        "franciscouzo/square-packing@5a299b4",
        NOT_RECORDED,
        RECIPE,
        "407 448 457 491 533 534 580 581 590 629 630 639 677 680 681 690 730 733 734 "
        "741 785 788 789 796 842 845 846 901 904 905 908 962 965 966 969 981 982",
    ),
)
#: Mykhailo Polkovskyi's 1851c2c files at the nine counts #719's 06:05Z edit withdrew where
#: #732 claims a lower side; at 539 the 1851c2c file is #732's own claim.
_WITHDRAWN_1851C2C = "411 451 494 495 540 583 587 632 683"


def _held_from_history(report: str, counts: str) -> tuple[Held, ...]:
    """The history walk's holds of a report (`HISTORY_HELD`), at ``counts`` only."""
    wanted = frozenset(int(n) for n in counts.split())
    return tuple(
        Held(item.kind, item.bead, item.counts & wanted, item.also, item.note, item.answer)
        for item in HISTORY_HELD[report]
        if item.counts & wanted
    )


#: The walk of each ledger these releases' rows are planned from. The backlog ledger's
#: starts were frozen at the 18 October ledger's ``main``; #719's at ``main`` after #720.
#: The history, #719 and #732 walks apply the owner's rulings of 23 October 2026
#: (`devtools.intake_ledger.RULINGS`): the re-certifications below the 12-place print they
#: held for think-fwa9 restate the reports they beat, and the publications above Göbel's
#: construction they held for think-8krd are above an earlier report, so neither is held.
WALKS: dict[str, Walk] = {
    BACKLOG: Walk(
        BACKLOG,
        later={
            "#678": "couzo-issue678-2026-10-18",
            "#686": "muglich-issue686-2026-10-19",
            "#715": "couzo-issue715-2026-10-21",
        },
        awaiting={},
    ),
    ISSUE_719: Walk(
        ISSUE_719,
        later={
            "franciscouzo/square-packing@4e4c8ce": "couzo-index-2026-10-15",
            "franciscouzo/square-packing@23aff0c": "couzo-23aff0c-2026-10-17",
            "franciscouzo/square-packing@5a299b4": "couzo-reconcile-2026-10-20",
        },
        awaiting={},
        held={
            report: tuple(
                Held(
                    item.kind,
                    item.bead,
                    item.counts & counts,
                    item.also,
                    item.note,
                    item.answer,
                )
                for item in HISTORY_HELD[report]
                if item.counts & counts
            )
            for report, counts in (
                ("franciscouzo/square-packing@4e4c8ce", frozenset({743, 798})),
                ("franciscouzo/square-packing@23aff0c", frozenset({447})),
            )
        },
        resting=(
            _resting("franciscouzo/square-packing@5a299b4", NOT_RECORDED, CONSEQUENCE, "447"),
        ),
    ),
    HISTORY: Walk(
        HISTORY,
        later={history_label(source): source for source in HISTORY_SOURCES},
        awaiting={},
        held=HISTORY_HELD,
        resting=HISTORY_RESTING,
    ),
    # #732's walk records the history walk's held publications where they stand below the
    # starts frozen after #730, and the 1851c2c files #719 withdrew, which the owner's answer
    # keeps out of the record (think-8m4k). Its verdicts resting on holds are declared so
    # that an answer names what it reopens (`held-dependents`).
    ISSUE_732: Walk(
        ISSUE_732,
        later={},
        awaiting={},
        held={
            **{report: _held_from_history(report, counts) for report, counts in _HELD_IN_732},
            f"{MISHAPOLK_REPOSITORY}@1851c2c": (
                _held(WITHDRAWN, "think-8m4k", _WITHDRAWN_1851C2C, answer=WITHDRAWN_ANSWER),
            ),
        },
        resting=_RESTING_732,
    ),
}
#: #719's 631: 2.73e-13 below Couzo's 4e4c8ce certificate (and 2.57e-23 below #715's
#: re-certification of it), all three rounding up to 25.656854249519. It is in the
#: restatement ruling's words, but the answer named the re-certifications the walks held,
#: and #722 recorded this one, another holder's, which its source states at 16 places: it
#: waits on the owner (think-oqjd), and the walks record it as before.
_AWAITING_719_631 = {
    "n": 631,
    "report": "#719",
    "bead": "think-oqjd",
    "reason": (
        "Another holder's re-certification of Couzo's 4e4c8ce certificate, 2.73e-13 below it "
        "at the same 12-place print, which #722 recorded and the owner's answer did not name"
    ),
}


def _rulings(*awaiting: Mapping[str, Any]) -> list[dict[str, Any]]:
    """The owner's rulings of 23 October 2026 as a walk's ``sources.yaml`` names them
    (`devtools.intake_ledger.Ruling`), with the claims the restatement ruling leaves to the
    owner."""
    restatement: dict[str, Any] = {
        "ruling": "restatement",
        "decided": "2026-10-23",
        "bead": "think-fwa9",
        "through": LIMIT,
    }
    if awaiting:
        restatement["awaiting_owner"] = [dict(item) for item in awaiting]
    classical = {
        "ruling": "classical-constructions",
        "decided": "2026-10-23",
        "bead": "think-8krd",
        "through": LIMIT,
    }
    return [restatement, classical]


#: The owner's rulings each walk applies (`devtools.intake_ledger.RULINGS`), through
#: ``LIMIT``: the counts above it wait on their own work (D1, think-llit), which applies the
#: same answers there. The backlog walk applies none: it was read on 22 October, and no
#: step of it is in either's words.
WALK_RULINGS: dict[str, list[dict[str, Any]]] = {
    ISSUE_719: _rulings(_AWAITING_719_631),
    HISTORY: _rulings(_AWAITING_719_631),
    ISSUE_732: _rulings(),
}
#: A Couzo row: the count, the prior and new prints, the deletion and the link.
_COUZO_ROW = re.compile(
    r"\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*\[certificate( \(delete (\d+)\))?\]"
    r"\(https://github\.com/franciscouzo/square-packing/blob/([0-9a-f]{40})/"
    r"(certificates/(?:best/)?n(\d+)\.cert)\)"
)
#: A de Winter row: the count, the print and the record it names.
_DE_WINTER_ROW = re.compile(r"\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|\s*([^|]+?)\s*\|")
_DE_WINTER_LINK = (
    "https://github.com/JoostdeWinter/joostdewinter.github.io/tree/"
    "b3152f526f23bc3ae450e51b6e906841233086d1/square-packing-above-324"
)
#: A #719 row: the count, the 16-place print and the baseline the issue cites; and the
#: count's file and its SHA-256, in the issue's second table.
_MISHAPOLK_ROW = re.compile(
    r"\|\s*\*\*(\d+)\*\*\s*\|\s*([0-9]+\.[0-9]{16})\s*\|\s*([0-9]+\.[0-9]+)\s*\|[^|]*\|[^|]*\|"
)
_MISHAPOLK_FILE = re.compile(
    r"\|\s*\*\*(\d+)\*\*\s*\|\s*`(certificates/n-\d+\.cert)`\s*\|\s*`([0-9a-f]{64})`\s*\|"
)


class ReplayError(ValueError):
    """Refuse a row, a certificate or a receipt that does not hold."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ReplayError(message)


# --------------------------------------------------------------------------- the releases


@dataclass(frozen=True, slots=True)
class Claim:
    """One row of an issue's table: the count, the print, and the certificate it reads."""

    n: int
    prior: str
    printed: str
    path: str
    certificate_n: int
    deleted: int


@dataclass(frozen=True, slots=True)
class SameCommitLeast:
    """Another file of a release's commit at a count, with a smaller side than the row's.

    ``path`` is its upstream path, ``packet`` the packet that retains it and whose import
    declaration reads its exact side (`upper_bound_reports.import_side`), ``claimed`` the
    comment in which the author claimed it, after the issue had named the row's file, and
    ``note`` the sentence the ledger's note on the report adds for the count.
    At #719's 204 the commit 1851c2c published both `certificates/n-204.cert`, which the
    issue names and T-229 registers, and `certificates/n204.cert`, 1.48e-11 lower, which
    the author claimed on 22 October and T-231 registers (think-h01y).
    """

    path: str
    packet: str
    claimed: str
    note: str


@dataclass(frozen=True, slots=True)
class Release:
    """One report, as this module reads it from its packet.

    ``pin`` is the commit the issue links, ``retained`` the one the packet holds (the same
    but for #666), and ``first_commit`` the first commit of ``retained``'s history that holds
    every certificate a row reads, committed at ``committed``, but for the counts
    ``later_commits`` names with their own commit and time: what ``first-commits`` measures
    and the claims record states. ``rows`` counts the issue's table and ``decided`` the rows
    beyond the corpus at or below ``LIMIT``; ``sampled`` names the counts the all-pairs
    sample decides, which the packet README and the atom state. ``walk`` names the ledger
    that plans its rows, ``rounding`` how the issue prints a side (`UP`, `BINARY64`), and
    ``derived`` that the packet keeps derived facts and no upstream byte. ``claimed_at``
    dates the counts an edit of the issue first claimed, which the ledger walks at that
    time rather than the issue's opening (#722's review A, A4). ``same_commit_least`` names
    the counts where the commit that first holds a row's certificate also states a smaller
    side in another file the issue does not name (`SameCommitLeast`): the ledger keeps one
    claim of a report per count, the least side its commit states there (#722's review A,
    A2), so the row is transcribed at that file's side (`same_commit_claim`).

    **A publication no issue reports** (``issue`` None) is a watched repository's commit,
    ``pin``, reported from the time it reached GitHub, ``published``: its committer time,
    or the later push `PUSHED_LATER` records. Its rows are not read from an issue body but
    declared in its packet, ``declared`` (`WATCHED_FORMAT`), from its walk's verdicts
    (`declare_rows`). Its label is the ledger's, ``owner/name@commit``. ``source`` names the
    coverage source that records its rows, the packet by default; a second report retained
    in one packet, as Couzo's ``23aff0c`` beside issue #670, has a source of its own, with
    its own claims record (``record``) and receipts directory (``receipts``).
    """

    issue: int | None
    packet: str
    holders: str
    source_url: str
    pin: str
    retained: str
    first_commit: str
    committed: str
    rows: int
    decided: int
    sampled: tuple[int, ...]
    bead: str
    read: Callable[[str, Release], list[Claim]]
    walk: str = BACKLOG
    rounding: str = UP
    derived: bool = False
    later_commits: Mapping[int, tuple[str, str]] | None = None
    claimed_at: Mapping[int, str] | None = None
    same_commit_least: Mapping[int, SameCommitLeast] | None = None
    published: str | None = None
    source_id: str | None = None
    record: Path = RECORD
    receipts: Path = RECEIPTS
    declared: Path = DECLARED

    @property
    def directory(self) -> Path:
        return WEB / self.packet

    @property
    def label(self) -> str:
        """How the ledger names the report: ``#N``, or ``owner/name@commit`` (seven hex)."""
        if self.issue is not None:
            return f"#{self.issue}"
        return f"{repository_of(self.source_url)}@{self.pin[:7]}"

    @property
    def described(self) -> str:
        """The report in a sentence: ``issue #N``, or the publication's label."""
        return f"issue #{self.issue}" if self.issue is not None else self.label

    @property
    def source(self) -> str:
        """The coverage source whose dated rows record this report."""
        return self.source_id or self.packet

    @property
    def issue_url(self) -> str:
        """The report's address: the issue, or the publication's tree at its commit."""
        if self.issue is not None:
            return f"https://github.com/jlevy/squares/issues/{self.issue}"
        return f"{self.source_url}/tree/{self.pin}"

    @property
    def report_key(self) -> str:
        """The key under which a receipt or record names the report."""
        return "issue" if self.issue is not None else "publication"

    @property
    def reported(self) -> str:
        """When a publication no issue reports reached GitHub (`published`, else
        `committed`); an issue's time is its own and is read from GitHub by the ledger."""
        return self.published or self.committed

    def path(self, kind: Path) -> Path:
        """A receipt's or the claims record's path in the packet: ``receipts/NAME`` under
        this release's own receipts directory, and the record at ``record``."""
        if kind == RECORD:
            return self.directory / self.record
        if kind.parent == RECEIPTS:
            return self.directory / self.receipts / kind.name
        return self.directory / kind

    def first_commit_of(self, n: int) -> tuple[str, str]:
        """The commit that first holds the certificate a row at ``n`` reads, and its time."""
        later = self.later_commits or {}
        return later.get(n, (self.first_commit, self.committed))


def repository_of(url: str) -> str:
    """``owner/name`` of a GitHub repository's address."""
    match = re.fullmatch(r"https://github\.com/([^/]+/[^/]+?)/?", url)
    _require(match is not None, f"{url}: not a GitHub repository")
    assert match is not None
    return match[1]


def _couzo_rows(body: str, release: Release) -> list[Claim]:
    rows: list[Claim] = []
    for line in body.splitlines():
        match = _COUZO_ROW.match(line.strip())
        if match is None:
            continue
        _require(match[6] == release.pin, f"{release.label} n={match[1]}: links another commit")
        rows.append(
            Claim(
                n=int(match[1]),
                prior=match[2],
                printed=match[3],
                path=match[7],
                certificate_n=int(match[8]),
                deleted=int(match[5] or 0),
            )
        )
    for row in rows:
        _require(
            row.deleted == row.certificate_n - row.n,
            f"{release.label} n={row.n}: the link and the deletion do not agree",
        )
    return rows


def _de_winter_rows(body: str, release: Release) -> list[Claim]:
    _require(_DE_WINTER_LINK in body, f"{release.label}: the issue links another folder")
    rows: list[Claim] = []
    for line in body.splitlines():
        match = _DE_WINTER_ROW.fullmatch(line.strip())
        if match is None:
            continue
        n = int(match[1])
        path = f"square-packing-above-324/n{n:04d}.cert"
        rows.append(Claim(n, match[3], match[2], path, n, 0))
    return rows


def _mishapolk_rows(body: str, release: Release) -> list[Claim]:
    """#719's two tables: each count's 16-place print and baseline, then the file the count
    reads and its SHA-256, which must be the digest the packet pins for that file."""
    _require(
        f"square-packing-records/tree/{release.pin}/certificates" in body,
        f"{release.label}: the issue links another commit",
    )
    printed: dict[int, tuple[str, str]] = {}
    files: dict[int, tuple[str, str]] = {}
    for line in body.splitlines():
        if match := _MISHAPOLK_ROW.fullmatch(line.strip()):
            printed[int(match[1])] = (match[2], match[3])
        elif match := _MISHAPOLK_FILE.fullmatch(line.strip()):
            files[int(match[1])] = (match[2], match[3])
    _require(printed.keys() == files.keys(), f"{release.label}: the two tables differ")
    pinned = manifest(release)
    rows: list[Claim] = []
    for n in printed:
        path, digest = files[n]
        _require(pinned.get(path) == digest, f"{release.label} n={n}: not the pinned digest")
        rows.append(Claim(n, printed[n][1], printed[n][0], path, n, 0))
    return rows


def read_declared_rows(body: str, release: Release) -> list[Claim]:
    """The rows a publication no issue reports declares in its packet (`WATCHED_FORMAT`):
    each count, the certificate the walk records there and its exact header side rounded
    up at 12 places, all of the publication's commit; `declare_rows` writes them."""
    declared = json.loads(body)
    _require(declared.get("format") == WATCHED_FORMAT, f"{release.label}: not {WATCHED_FORMAT}")
    _require(
        declared.get("commit") == release.pin
        and declared.get("publication") == release.issue_url
        and declared.get("walk") == release.walk,
        f"{release.label}: the declaration names another commit or walk",
    )
    return [
        Claim(int(row["n"]), "", str(row["printed"]), str(row["certificate"]), int(row["n"]), 0)
        for row in declared["rows"]
    ]


COUZO_URL = "https://github.com/franciscouzo/square-packing"
EVAND_URL = "https://github.com/evand/square-packing"
FANG_URL = "https://github.com/TheSnakeFang/squarepack-certs"
#: The publications no issue reports whose rows the history walk records, each with its
#: packet, holder, repository, commit and committer time, its row count, the counts its
#: all-pairs sample decides, its bead, and where it differs from the defaults: the push
#: that made it public (`PUSHED_LATER`), and the source, record and receipts of a second
#: report in one packet.
WATCHED: tuple[
    tuple[str, str, str, str, str, int, tuple[int, ...], str, dict[str, Any]], ...
] = (
    (
        "couzo-exact-certificates-2026-10-09",
        "Francisco Couzo",
        COUZO_URL,
        "02f969075f79d5e13fa21e09e381a44e8647b452",
        "2026-10-09T20:28:52Z",
        12,
        (),
        "think-a4wq",
        {"source_id": "couzo-02f9690-2026-10-09"},
    ),
    (
        "evand-hunt3-first-hour-2026-10-10",
        "Evan Daniel",
        EVAND_URL,
        "f7a2325df1e396f46ee373c6d00a880795b749b7",
        "2026-10-10T09:15:50Z",
        1,
        (),
        "think-xm4h",
        {},
    ),
    (
        "couzo-certificates-2026-10-10",
        "Francisco Couzo",
        COUZO_URL,
        "3ef76349025bf4bfa99c9c3600bcc273f4c33e02",
        "2026-10-10T13:52:27Z",
        2,
        (),
        "think-1545",
        {"source_id": "couzo-3ef7634-2026-10-10"},
    ),
    (
        "couzo-extended-certificates-2026-10-11",
        "Francisco Couzo",
        COUZO_URL,
        "f311f08901c24b2a6c5f720710a45adec23e926a",
        "2026-10-11T03:39:54Z",
        4,
        (),
        "think-om5l",
        {},
    ),
    (
        "couzo-updates-2026-10-12",
        "Francisco Couzo",
        COUZO_URL,
        "a7067d7b92b1e0208499b26d93e898648f0e8667",
        "2026-10-12T17:55:52Z",
        1,
        (),
        "think-rfce",
        {},
    ),
    (
        "fang-composites-2026-10-12",
        "Kevin Fang",
        FANG_URL,
        "bef5c42d58257fe38ed010a5d1ff9b8fc608df57",
        "2026-10-12T19:13:41Z",
        2,
        (),
        "think-qik6",
        {},
    ),
    (
        "couzo-retained-certificates-2026-10-12",
        "Francisco Couzo",
        COUZO_URL,
        "93570ef79474fd8c35d1293addf095f9eee6a658",
        "2026-10-12T21:31:43Z",
        2,
        (),
        "think-rfce",
        {},
    ),
    (
        "couzo-issue583-2026-10-13",
        "Francisco Couzo",
        COUZO_URL,
        "45966700cf15d3f42e064fd6da51fcb9a5def2be",
        "2026-10-13T13:53:57Z",
        1,
        (),
        "think-rfce",
        {"source_id": "couzo-4596670-2026-10-13"},
    ),
    (
        "couzo-index-2026-10-15",
        "Francisco Couzo",
        COUZO_URL,
        "4e4c8ce23cb5e87f033021687010992c40575480",
        "2026-10-15T00:31:53Z",
        253,
        (366, 703),
        "think-yfoo",
        {},
    ),
    (
        "couzo-issue670-2026-10-17",
        "Francisco Couzo",
        COUZO_URL,
        "23aff0c6f992271e1ad13a148d44f392c4b386c0",
        "2026-10-17T18:00:09Z",
        21,
        (),
        "think-tmwt",
        {
            "source_id": "couzo-23aff0c-2026-10-17",
            "record": Path("acquisition/beyond-horizon-rows-23aff0c.json"),
            "receipts": Path("receipts/23aff0c"),
            "declared": Path("acquisition/watched-release-23aff0c.json"),
        },
    ),
    (
        "couzo-reconcile-2026-10-20",
        "Francisco Couzo",
        COUZO_URL,
        "5a299b4708ab1ae4870d0fc1ab155738144f6ab8",
        "2026-10-20T22:35:41Z",
        20,
        (903,),
        "think-tmwt",
        {"published": "2026-10-21T22:56:37Z"},
    ),
)
RELEASES: dict[str, Release] = {
    release.label: release
    for release in (
        Release(
            issue=666,
            packet="de-winter-issue666-2026-10-17",
            holders="Joost de Winter",
            source_url="https://github.com/JoostdeWinter/joostdewinter.github.io",
            pin="b3152f526f23bc3ae450e51b6e906841233086d1",
            retained="643dc9ad4d3dbd71a9a05558c7f6116b809ba930",
            first_commit="b9cdc16bc20fedfbd4f5aa142dd7039b22f757f2",
            committed="2026-10-17T07:03:15Z",
            rows=19,
            decided=11,
            sampled=(464,),
            bead="think-3m10",
            read=_de_winter_rows,
        ),
        Release(
            issue=670,
            packet="couzo-issue670-2026-10-17",
            holders="Francisco Couzo",
            source_url=COUZO_URL,
            pin="23aff0c6f992271e1ad13a148d44f392c4b386c0",
            retained="23aff0c6f992271e1ad13a148d44f392c4b386c0",
            first_commit="23aff0c6f992271e1ad13a148d44f392c4b386c0",
            committed="2026-10-17T18:00:09Z",
            rows=73,
            decided=72,
            sampled=(922,),
            bead="think-f28n",
            read=_couzo_rows,
        ),
        Release(
            issue=672,
            packet="couzo-issue672-2026-10-17",
            holders="Francisco Couzo",
            source_url=COUZO_URL,
            pin="af8cb7959aead318c0cf5e9f873de3caa763f77a",
            retained="af8cb7959aead318c0cf5e9f873de3caa763f77a",
            first_commit="af8cb7959aead318c0cf5e9f873de3caa763f77a",
            committed="2026-10-17T20:44:59Z",
            rows=46,
            decided=44,
            sampled=(996,),
            bead="think-2vjc",
            read=_couzo_rows,
        ),
        Release(
            issue=675,
            packet="couzo-issue675-2026-10-18",
            holders="Francisco Couzo",
            source_url=COUZO_URL,
            pin="c6da0fc7524d667bf3d224559724ba9b60762e60",
            retained="c6da0fc7524d667bf3d224559724ba9b60762e60",
            first_commit="c6da0fc7524d667bf3d224559724ba9b60762e60",
            committed="2026-10-18T05:46:00Z",
            rows=79,
            decided=78,
            sampled=(998,),
            bead="think-pvav",
            read=_couzo_rows,
        ),
        Release(
            issue=719,
            packet="mishapolk-issue719-2026-10-22",
            holders="Mykhailo Polkovskyi",
            source_url="https://github.com/Mishapolk/square-packing-records",
            pin="12fc46678fa8eefa3f156ff37dfffd84c8f3a580",
            retained="12fc46678fa8eefa3f156ff37dfffd84c8f3a580",
            first_commit="1851c2c70a77085f2deb87978f10d40e0f0e86a6",
            committed="2026-10-22T05:29:48Z",
            rows=122,
            decided=112,
            sampled=(447, 652, 997),
            bead="think-xyhn",
            read=_mishapolk_rows,
            walk=ISSUE_719,
            rounding=BINARY64,
            derived=True,
            # The pin replaced 447's certificate, which 1851c2c had first committed.
            later_commits={
                447: ("12fc46678fa8eefa3f156ff37dfffd84c8f3a580", "2026-10-22T06:05:07Z")
            },
            # The issue's 06:05:31Z edit added 366 and 447 to the table it opened with.
            claimed_at={366: "2026-10-22T06:05:31Z", 447: "2026-10-22T06:05:31Z"},
            # 1851c2c also published certificates/n204.cert, 1.48e-11 below n-204.cert, the
            # file the issue names; the author claimed it on 22 October (think-h01y, T-231).
            # Of the 122 claimed counts, the trees of 1851c2c and 12fc466 hold a second file
            # (nN.cert beside n-N.cert, the same blobs in both) at seven: 105, 204, 753, 754
            # and 790 to 792. Read from their headers on 23 October 2026, only 204's is
            # lower; 105's is 4.64e-12 above, and the other five state the same side, so
            # 204 is the one count this rule moves (#753's review A, A10).
            same_commit_least={
                204: SameCommitLeast(
                    path="certificates/n204.cert",
                    packet="mishapolk-n204-2026-10-22",
                    claimed=(
                        "https://github.com/jlevy/squares/issues/719#issuecomment-6350348588"
                    ),
                    note=(
                        "At 204 the claim is the least side 1851c2c states there, "
                        "certificates/n204.cert, since a report keeps one claim a count "
                        "(#722's review A, A2); this ledger was re-gathered on 23 October "
                        "2026 to read it (think-h01y). The issue names "
                        "certificates/n-204.cert, which T-229 registered before the author "
                        "claimed the lower file on 22 October at 20:15:57Z, and which the "
                        "case adopted on 23 October; T-229 stands as registered, and T-231 "
                        "registers the lower file, by the same author and from the same "
                        "commit, and supersedes T-229 at 204. Of the 122 claimed counts, "
                        "1851c2c holds a second file only at 105, 204, 753, 754 and 790 to "
                        "792, and only 204's is lower. 105 is untouched."
                    ),
                )
            },
        ),
        Release(
            issue=732,
            packet="mishapolk-issue732-2026-10-22",
            holders="Mykhailo Polkovskyi",
            source_url=MISHAPOLK_URL,
            pin="17cc220131360ef290750eb845a3544c30ccb389",
            retained="17cc220131360ef290750eb845a3544c30ccb389",
            first_commit="8a488a10e994f13c706b651ddaaa9727600c96e5",
            committed="2026-10-22T19:08:59Z",
            rows=77,
            decided=77,
            sampled=(645, 752, 995),
            bead="think-0gp6",
            read=read_declared_rows,
            walk=ISSUE_732,
            declared=Path("acquisition/declared-rows.json"),
        ),
        *(
            Release(
                issue=None,
                packet=packet,
                holders=holders,
                source_url=url,
                pin=commit,
                retained=commit,
                first_commit=commit,
                committed=committed,
                rows=rows,
                decided=rows,
                sampled=sampled,
                bead=bead,
                read=read_declared_rows,
                walk=HISTORY,
                **extra,
            )
            for packet, holders, url, commit, committed, rows, sampled, bead, extra in WATCHED
        ),
    )
}


def release(key: int | str) -> Release:
    """The declared release of an issue (its number, or ``#N``) or of a publication no
    issue reports (its label, ``owner/name@commit``)."""
    label = f"#{key}" if isinstance(key, int) or str(key).isdigit() else str(key)
    _require(label in RELEASES, f"{label}: no declared release")
    return RELEASES[label]


def claims(chosen: Release) -> list[Claim]:
    """Every row of the issue's table, read from its retained body, or every row a
    release's packet declares (`declares_rows`), refused unless all are."""
    if declares_rows(chosen):
        body = (chosen.directory / chosen.declared).read_text(encoding="utf-8")
    else:
        body = json.loads((chosen.directory / ISSUE).read_text(encoding="utf-8"))["body"]
    rows = chosen.read(body, chosen)
    _require(len(rows) == chosen.rows, f"{chosen.label}: {len(rows)} rows, not {chosen.rows}")
    counts = [row.n for row in rows]
    _require(counts == sorted(set(counts)), f"{chosen.label}: rows out of order")
    return rows


def declares_rows(chosen: Release) -> bool:
    """Whether a release's packet declares its rows from its walk (`declared_rows`): every
    publication no issue reports, and an issue with no table of rows, as #732."""
    return chosen.read is read_declared_rows


def decided_claims(chosen: Release) -> list[Claim]:
    """The rows beyond the corpus at or below ``LIMIT``, which this module decides."""
    rows = [row for row in claims(chosen) if reports.HORIZON < row.n <= LIMIT]
    _require(
        len(rows) == chosen.decided,
        f"{chosen.label}: {len(rows)} rows beyond the corpus to {LIMIT}, not {chosen.decided}",
    )
    return rows


def held_claims(chosen: Release) -> list[Claim]:
    """The rows above ``LIMIT``, retained and not decided: they wait on the owner."""
    return [row for row in claims(chosen) if row.n > LIMIT]


def manifest(chosen: Release) -> dict[str, str]:
    """The packet's upstream digests, by upstream path."""
    return acquire_source.read_manifest(chosen.directory / acquire_source.MANIFEST)


def archive(chosen: Release) -> Path:
    """The directory holding the packet's retained upstream files."""
    record = json.loads((chosen.directory / acquire_source.RECORD).read_text(encoding="utf-8"))
    return REPO / record["sources"][0]["archived_path"]


def custody(chosen: Release) -> None:
    """Refuse to read the packet unless ``acquire_source --check`` holds for it."""
    problems = acquire_source.check(chosen.directory, REPO)
    _require(not problems, f"{chosen.packet} custody: " + "; ".join(problems))


def certificate(chosen: Release, row: Claim) -> legacy.Certificate:
    """The packing a row claims: its retained certificate, less the squares it deletes.

    A derived packet's certificate is its exact fact, which `devtools.upper_bound_reports`
    admits only once the packet's custody holds and the fact rebuilds itself from the
    digest the packet pins for ``row.path``.
    """
    if chosen.derived:
        facts = reports.read_facts(chosen.directory, {row.certificate_n})
        _require(row.certificate_n in facts, f"{chosen.label} n={row.n}: no derived fact")
        declared = {
            item["n"]: item["path"]
            for item in reports.load_declaration(chosen.directory)["certificates"]
        }
        _require(
            declared[row.certificate_n] == row.path,
            f"{chosen.label} n={row.n}: the fact is not of the issue's file",
        )
        parsed = facts[row.certificate_n]
    else:
        raw = read_retained_bytes(archive(chosen) / row.path)
        parsed = legacy.parse(raw.decode("utf-8"), expected_n=row.certificate_n)
    if row.deleted:
        parsed = legacy.Certificate(row.n, parsed.side, parsed.poses[: row.n])
    return parsed


def decided_sides(chosen: Release) -> dict[int, Fraction]:
    """Each decided row's exact side: a retained certificate's header, or, for a derived
    packet, the side its frozen claim record states (`devtools.upper_bound_reports`), which
    that importer's ``check`` holds to the facts and ``check --replay`` here decides again
    from them. Admitting a fact validates the whole witness, a fraction of a second each, so
    the sides alone are read from the record."""
    rows = decided_claims(chosen)
    if not chosen.derived:
        return {row.n: certificate(chosen, row).side for row in rows}
    stated = {
        item["n"]: Fraction(item["exact_side"])
        for item in _read(chosen.directory / reports.CLAIMS)["results"]
    }
    _require(
        all(row.certificate_n in stated for row in rows),
        f"{chosen.label}: the claim record does not state every decided side",
    )
    return {row.n: stated[row.certificate_n] for row in rows}


def ceiling(side: Fraction, places: int = PLACES) -> str:
    """``side`` rounded up at ``places`` decimal places."""
    return legacy.ceiling_decimal(side, places)


def print_holds(chosen: Release, side: Fraction, printed: str) -> bool:
    """Whether the issue's print is what its rounding makes of ``side``: rounded up at 12
    places, or ``side``'s binary64 value printed at 16 (`BINARY64`)."""
    if chosen.rounding == BINARY64:
        return f"{float(side):.16f}" == printed
    return base.rounds_up_to(side, printed)


def recorded_side(chosen: Release, side: Fraction, printed: str) -> str:
    """The side a row records: an `UP` release's print; for a `BINARY64` release, the
    side rounded up at 16 places, the places a binary64 print shows, at every row."""
    return ceiling(side, 16) if chosen.rounding == BINARY64 else printed


def git_blob(raw: bytes) -> str:
    """The Git blob id of a file's bytes."""
    return hashlib.sha1(b"blob %d\0" % len(raw) + raw, usedforsecurity=False).hexdigest()


def seed_credit(chosen: Release, row: Claim) -> dict[str, Any] | None:
    """The per-count metadata's seed credit, where the packet retains it, and whether the
    metadata describes the row's certificate (a #675 row reads ``best/``, the metadata the
    root certificate of its count)."""
    if chosen.derived:
        return None
    try:
        metadata = json.loads(
            read_retained_text(archive(chosen) / f"certificates/n{row.n}.json")
        )
    except FileNotFoundError:
        return None
    return {
        "metadata": f"certificates/n{row.n}.json",
        "seed_credit": (metadata.get("origin") or {}).get("seed_credit", ""),
        "kind": metadata.get("kind", ""),
        "describes_this_certificate": metadata.get("certificate_sha256")
        == manifest(chosen)[row.path],
    }


# --------------------------------------------------------------------------- the replay


def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_text(retained_dumps(value, sort_keys=True), encoding="utf-8")


def _environment() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "machine": platform.machine(),
    }


def decide_row(job: tuple[str, int]) -> dict[str, Any]:
    """One row: the side against the print, both routes, and the certificate's controls."""
    chosen = release(job[0])
    row = next(row for row in decided_claims(chosen) if row.n == job[1])
    cert = certificate(chosen, row)
    started = time.monotonic()
    result = base.decide(base.geometry(cert))
    holds = print_holds(chosen, cert.side, row.printed)
    key = (
        "printed_is_binary64_of_side"
        if chosen.rounding == BINARY64
        else "printed_is_upward_rounding"
    )
    record: dict[str, Any] = {
        "n": row.n,
        "certificate": row.path,
        "certificate_sha256": manifest(chosen)[row.path],
        "deleted_squares": row.deleted,
        "printed": row.printed,
        "issue_prior": row.prior,
        "exact_side": legacy.literal(cert.side),
        "side_ceiling_16": ceiling(cert.side, 16),
        key: holds,
        "verified": result["passed"] and holds,
        "decision": result,
    }
    if row.deleted == 0:
        record["controls"] = base.decide_controls(cert)
    credit = seed_credit(chosen, row)
    if credit is not None:
        record["source_metadata"] = credit
    record["wall_seconds"] = round(time.monotonic() - started, 3)
    return record


def _jobs(chosen: Sequence[Release]) -> list[tuple[str, int]]:
    """Every decided row of the chosen releases, the largest certificates first: a
    certificate's work grows with its count, which the issue row names, so no file is read
    to order the jobs."""
    jobs = [
        (row.certificate_n, item.label, row.n)
        for item in chosen
        for row in decided_claims(item)
    ]
    return [(issue, n) for _, issue, n in sorted(jobs, key=lambda job: -job[0])]


def filtered(issues: Sequence[int | str], workers: int) -> dict[str, dict[str, Any]]:
    """Decide every decided row and control of the chosen releases, one receipt a packet."""
    chosen = [release(issue) for issue in issues]
    for item in chosen:
        custody(item)
    started = datetime.now(UTC)
    wall = time.monotonic()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        decided = dict(zip(_jobs(chosen), pool.map(decide_row, _jobs(chosen)), strict=True))
    elapsed = round(time.monotonic() - wall, 1)
    receipts: dict[str, dict[str, Any]] = {}
    for item in chosen:
        results = [decided[item.label, row.n] for row in decided_claims(item)]
        receipt: dict[str, Any] = {
            "format": FILTERED_FORMAT,
            item.report_key: item.issue_url,
            "source_commit": item.retained,
            "issue_pin": item.pin,
            "packet": item.directory.relative_to(REPO).as_posix(),
            "program": "packing/devtools/beyond_horizon_replay.py",
            "decision": "packing/devtools/couzo_678_replay.py",
            "filter_lemma": base.FILTER_LEMMA,
            "controls": list(base.CONTROLS),
            "environment": _environment(),
            "started_utc": started.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "run_wall_seconds": elapsed,
            "run_releases": [other.label for other in chosen],
            "workers": workers,
            "rows": results,
            "summary": base.summary(results),
        }
        _write(item.path(FILTERED), receipt)
        receipts[item.label] = receipt
    return receipts


# --------------------------------------------------------------------------- first commits


def _git(clone: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(clone), *args], capture_output=True, text=True, check=True
    ).stdout


def first_commits(issue: int | str, clone: Path) -> dict[str, Any]:
    """The first commit of the retained commit's history that holds each certificate.

    ``clone`` is a clone of the source holding the retained commit and its history; a
    blobless clone serves, since only trees are read. Each certificate the decided and held
    rows read is found by its Git blob at the retained commit, under any path. A derived
    packet retains no byte to hash, so each blob is read from the clone's tree at the
    retained commit, and its bytes must have the SHA-256 the packet pins (`_pinned_blob`).
    """
    chosen = release(issue)
    custody(chosen)
    chain = _git(clone, "rev-list", "--reverse", chosen.retained).split()
    _require(chain and chain[-1] == chosen.retained, "the clone does not hold the commit")
    dates = dict(
        line.split(" ", 1)
        for line in _git(clone, "log", "--format=%H %cI", chosen.retained).splitlines()
    )
    first: dict[str, str] = {}
    for commit in chain:
        for line in _git(clone, "ls-tree", "-r", commit).splitlines():
            meta, _, _path = line.partition("\t")
            first.setdefault(meta.split()[2], commit)
    rows = []
    for row in [*decided_claims(chosen), *held_claims(chosen)]:
        if chosen.derived:
            blob = _pinned_blob(chosen, row, clone)
        else:
            blob = git_blob(read_retained_bytes(archive(chosen) / row.path))
        commit = first[blob]
        item = {
            "n": row.n,
            "certificate": row.path,
            "blob": blob,
            "first_commit": commit,
            "committed": _utc(dates[commit]),
        }
        if chosen.derived:
            item["sha256"] = manifest(chosen)[row.path]
        rows.append(item)
    receipt = {
        "format": FIRST_COMMITS_FORMAT,
        "source": chosen.source_url,
        "retained_commit": chosen.retained,
        "history_commits": len(chain),
        "rows": rows,
    }
    _write(chosen.path(FIRST_COMMITS), receipt)
    return receipt


def _pinned_blob(chosen: Release, row: Claim, clone: Path) -> str:
    """A derived packet's certificate's Git blob at the retained commit, read from a clone
    and refused unless its bytes have the SHA-256 the packet pins."""
    (line,) = _git(clone, "ls-tree", chosen.retained, "--", row.path).splitlines()
    blob = line.split("\t", 1)[0].split()[2]
    raw = subprocess.run(
        ["git", "-C", str(clone), "cat-file", "blob", blob], capture_output=True, check=True
    ).stdout
    _require(
        hashlib.sha256(raw).hexdigest() == manifest(chosen)[row.path] and git_blob(raw) == blob,
        f"{chosen.label} n={row.n}: the clone's file is not the pinned one",
    )
    return blob


def _utc(stamp: str) -> str:
    return datetime.fromisoformat(stamp).astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------- cross-checks


def exhaustive_row(job: tuple[str, int]) -> dict[str, Any]:
    """The maintained all-pairs kernel on one row, beside the filtered decision of it."""
    chosen = release(job[0])
    row = next(row for row in decided_claims(chosen) if row.n == job[1])
    cert = certificate(chosen, row)
    wall = time.monotonic()
    case = kernel.run_case(cert, "positive")
    elapsed = time.monotonic() - wall
    first, second = case["exact_verify"], case["independent"]
    narrow = base.decide(base.geometry(cert))["independent"]
    return {
        "n": row.n,
        "exact_verify_passed": first["verification_passed"],
        "independent_passed": second["verification_passed"],
        "pairs_tested": first["pairs_tested"],
        "least_pair_gap": second["minimum_best_pair_gap"],
        "least_wall_clearance": second["minimum_containment_clearance"],
        "routes_agree_on_least_gap": Fraction(first["minimum_best_pair_gap"])
        == Fraction(second["minimum_best_pair_gap"]),
        "equals_filtered_least_gap": Fraction(second["minimum_best_pair_gap"])
        == Fraction(narrow["least_pair_gap"]),
        "equals_filtered_least_wall": Fraction(second["minimum_containment_clearance"])
        == Fraction(narrow["least_wall_clearance"]),
        "cpu_seconds": case["cpu_seconds"],
        "wall_seconds": round(elapsed, 1),
    }


def exhaustive(issue: int | str, counts: Sequence[int], workers: int) -> dict[str, Any]:
    """The all-pairs kernel on chosen rows of one release, each against the filtered one."""
    chosen = release(issue)
    custody(chosen)
    decided = {row.n for row in decided_claims(chosen)}
    for n in counts:
        _require(n in decided, f"{chosen.label} n={n}: not a decided row")
    started = datetime.now(UTC)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(exhaustive_row, [(chosen.label, n) for n in counts]))
    receipt = {
        "format": EXHAUSTIVE_FORMAT,
        "kernel": "devtools.evand_arrangement_reports.run_case, positive job, every pair",
        "environment": _environment(),
        "started_utc": started.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "workers": workers,
        "rows": results,
        "sample_pairs": sum(row["pairs_tested"] for row in results),
        "sample_cpu_seconds": round(
            sum(sum(row["cpu_seconds"].values()) for row in results), 1
        ),
    }
    _write(chosen.path(EXHAUSTIVE), receipt)
    return receipt


def _goebel_program() -> Any:
    """The 15 October packet's exact Göbel comparison, loaded from its retained path."""
    spec = importlib.util.spec_from_file_location("goebel_beyond_horizon", base.GOEBEL_PROGRAM)
    if spec is None or spec.loader is None:
        raise ReplayError("the Göbel program is missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def goebel() -> dict[str, dict[str, Any]]:
    """Every decided side against Göbel's classical constructions, exactly.

    The families, their deletion to smaller counts and the sign test are those of the 15
    October packet's retained ``goebel_beyond_horizon.py``, read from its path unchanged;
    its ``LIMIT`` of 1100 covers every count decided here.
    """
    program = _goebel_program()
    _require(program.LIMIT >= LIMIT, "the Göbel program stops below the decided counts")
    forms = program.families(program.LIMIT)
    tallies: dict[str, dict[str, Any]] = {}
    for chosen in RELEASES.values():
        custody(chosen)
        sides = decided_sides(chosen)
        rows = [(row.n, sides[row.n], row.path) for row in decided_claims(chosen)]
        result = program.compare(f"{chosen.described} at {chosen.pin[:8]}", rows, forms)
        _write(
            chosen.path(GOEBEL),
            {
                "format": GOEBEL_FORMAT,
                "program": base.GOEBEL_PROGRAM.relative_to(REPO).as_posix(),
                "families": (
                    "Göbel squares, Göbel strips and corner-touching strips, with deletion"
                ),
                "comparison": result,
            },
        )
        tallies[chosen.label] = {"rows": result["rows"], "tally": result["tally"]}
    return tallies


# --------------------------------------------------------------------------- claims record


def beyond_horizon_rows(chosen: Release) -> dict[str, Any]:
    """The decided rows as the coverage register reads them, rebuilt.

    Each keeps the side the row records as ``offered_side``, the value a dated
    beyond-horizon row holds byte for byte: an `UP` release's print; for a `BINARY64`
    release, the side rounded up at 16 places, with the issue's print beside it
    (`recorded_side`). Each also keeps its certificate's exact header side and when the
    certificate was first committed. A decided row the walk does not record, as #719's 366,
    is no row, so the record leaves it out; the filtered receipt keeps its decision.
    """
    custody(chosen)
    results = []
    sides = decided_sides(chosen)
    unrecorded = {n for n, source in unrecorded_rows() if source == chosen.source}
    for row in decided_claims(chosen):
        if row.n in unrecorded:
            continue
        side = sides[row.n]
        _require(
            print_holds(chosen, side, row.printed),
            f"{chosen.label} n={row.n}: the print is not the side's {chosen.rounding} print",
        )
        result: dict[str, Any] = {
            "n": row.n,
            "offered_side": recorded_side(chosen, side, row.printed),
            "exact_side": legacy.literal(side),
            "ceiling": ceiling(side, reports.DISPLAY_PLACES),
            "certificate": row.path,
            "deleted": row.deleted,
            "first_committed": chosen.first_commit_of(row.n)[1],
        }
        if chosen.rounding != UP:
            result["issue_print"] = row.printed
        results.append(result)
    record = {
        "format": reports.BEYOND_FORMAT,
        chosen.report_key: chosen.issue_url,
        "source": chosen.source_url,
        "revision": chosen.retained,
        "issue_pin": chosen.pin,
        "horizon": reports.HORIZON,
        "limit": LIMIT,
        "results": results,
    }
    if chosen.rounding != UP:
        record["issue_rounding"] = chosen.rounding
    if chosen.issue is None:
        record["published"] = chosen.reported
    return record


def claims_record() -> dict[str, int]:
    """Write each packet's beyond-horizon record and return its row counts."""
    written: dict[str, int] = {}
    for chosen in RELEASES.values():
        record = beyond_horizon_rows(chosen)
        _write(chosen.path(RECORD), record)
        written[chosen.label] = len(record["results"])
    return written


# --------------------------------------------------------------------------- earlier reports


#: Watched repositories whose commits after a public head reached GitHub later, in one push:
#: Couzo's three commits after 7b6c87e were pushed at 2026-10-21T22:56:37Z
#: (`devtools.couzo_715_replay`), so each is dated by that push, not by its committer time.
PUSHED_LATER: dict[str, tuple[str, str]] = {
    "franciscouzo/square-packing": (
        "7b6c87e129cf80b5ff9847b90b47fd30b4563c54",
        "2026-10-21T22:56:37Z",
    ),
}
#: The index files whose stated bounds are publications too: each count's verified bound.
INDEXES = {"upper_bounds.json": ("verified", "bound"), "certified_bounds.json": ("bound",)}
_HEADER = re.compile(rb"\s*([1-9][0-9]*)\s+([0-9]+(?:/[1-9][0-9]*)?)\s*")


def _header(raw: bytes) -> tuple[int, Fraction] | None:
    """A certificate's count and side, from its first line that is not a comment."""
    for line in raw.splitlines()[:8]:
        if not line.strip() or line.lstrip().startswith(b"#"):
            continue
        match = _HEADER.fullmatch(line)
        return None if match is None else (int(match[1]), Fraction(match[2].decode()))
    return None


def _dated_commits(name: str, clone: Path, until: str) -> list[tuple[str, str]]:
    """Every commit of a clone's ``HEAD`` history oldest first, each with the time it was
    published: its committer time, or the later push `PUSHED_LATER` records; only those
    published before ``until``."""
    chain = _git(clone, "rev-list", "--reverse", "--topo-order", "HEAD").split()
    times = {
        commit: _utc(stamp)
        for commit, stamp in (
            line.split(" ", 1)
            for line in _git(clone, "log", "--format=%H %cI", "HEAD").splitlines()
        )
    }
    if name in PUSHED_LATER:
        head, pushed = PUSHED_LATER[name]
        public = set(_git(clone, "rev-list", head).split())
        times = {c: (t if c in public else max(t, pushed)) for c, t in times.items()}
    return [(commit, times[commit]) for commit in chain if times[commit] < until]


def _blobs(clone: Path, blobs: Sequence[str]) -> dict[str, bytes]:
    """Each blob's bytes, read in one ``git cat-file --batch``."""
    found: dict[str, bytes] = {}
    with subprocess.Popen(
        ["git", "-C", str(clone), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    ) as process:
        assert process.stdin is not None
        assert process.stdout is not None
        for blob in blobs:
            process.stdin.write(blob.encode() + b"\n")
            process.stdin.flush()
            size = int(process.stdout.readline().split()[2])
            found[blob] = process.stdout.read(size)
            process.stdout.read(1)
        process.stdin.close()
    return found


def _stated_side(source: Mapping[str, Any], n: int) -> Fraction | None:
    """The exact side a row's source states at ``n``, read as the ledger's starts read it
    (`devtools.intake_ledger.stated_exact_side`), or None for a record that states none."""
    from devtools import intake_ledger  # noqa: PLC0415

    try:
        return intake_ledger.stated_exact_side(source, n)
    except intake_ledger.LedgerError as error:
        raise ReplayError(str(error)) from error


def row_side(source: Mapping[str, Any], n: int, printed: str) -> Fraction:
    """A beyond-horizon row's side: the exact side its source's claims record states, or,
    where that record states none at any count, the row's print (`_stated_side`)."""
    side = _stated_side(source, n)
    return Fraction(printed) if side is None else side


class Standing(NamedTuple):
    """A claimed count's standing side as a packet's frozen claim record read the record
    (`standing_sides`): the least of the case, or of the rows that stood there and the
    grid (``side``), and, for a record read from `devtools.intake_ledger.GOEBEL_FROM`, an
    enclosure of Göbel's construction there (``construction``, of the closed form
    ``form``), as the importer reads it (`reports.goebel_construction`)."""

    side: Fraction
    construction: reports.Span | None = None
    form: str = ""

    def covers(self, value: Fraction) -> bool:
        """``value`` is at or above the standing side: no publication strictly below it. A
        rational side the construction's enclosure cannot separate from it is refused."""
        if value >= self.side:
            return True
        if self.construction is None:
            return False
        own = reports.exact_span(value)
        if reports.below(own, self.construction):
            return False
        _require(
            reports.below(self.construction, own),
            f"{value} does not separate from the enclosure of Göbel's construction",
        )
        return True


def standing_sides(
    record: Mapping[str, Any], counts: Iterable[int], sources: Mapping[str, Mapping[str, Any]]
) -> dict[int, Standing]:
    """Each claimed count's standing side as the frozen claim ``record`` read the record:
    the case's exact side in the corpus, else the exact side of the row that stood there,
    read from its source's claims record (``sources``, by id), or the grid; a count of
    ``counts`` the record has no result for, one above ``LIMIT`` that no record holds yet,
    stands at the grid. Beyond the horizon a record read from
    `devtools.intake_ledger.GOEBEL_FROM` takes Göbel's construction too, and refuses a
    count above the retained program's reach of 1073."""
    read_on = str(record.get("read_on", ""))

    def beyond(n: int, side: Fraction) -> Standing:
        try:
            construction = reports.goebel_construction(n, read_on)
        except reports.ReportError as error:
            raise ReplayError(str(error)) from error
        if construction is None:
            return Standing(side)
        _, form, span = construction
        return Standing(side, span, form)

    standing = {n: beyond(n, reports.grid_side(n)) for n in counts}
    for row in record["results"]:
        n = row["n"]
        if row["case"] is not None:
            standing[n] = Standing(Fraction(row["case"]["exact_side"]))
            continue
        rows = [
            row_side(sources[item["report"]], n, item["printed"])
            for item in row["pending"]
            if "printed" in item
        ]
        standing[n] = beyond(n, min([*rows, Fraction(row["grid_side"])]))
    return standing


def _standing(chosen: Release) -> dict[int, Standing]:
    """Each claimed count's standing side as the packet's frozen claim record read the
    record (`standing_sides`)."""
    record = _read(chosen.directory / reports.CLAIMS)
    coverage = safe_load(COVERAGE.read_text(encoding="utf-8"))
    sources = {source["id"]: source for source in coverage["sources"]}
    return standing_sides(record, [row.n for row in claims(chosen)], sources)


def release_sides(chosen: Release, clone: Path | None) -> dict[int, Fraction]:
    """Each claimed row's exact side: from the packet's frozen claim record, and for a row
    the packet does not derive (above ``LIMIT``), from the header of the file a clone of the
    source holds at the retained commit, refused unless it has the digest the packet pins."""
    record = _read(chosen.directory / reports.CLAIMS)
    stated = {item["n"]: Fraction(item["exact_side"]) for item in record["results"]}
    sides: dict[int, Fraction] = {}
    for row in claims(chosen):
        if row.n in stated:
            sides[row.n] = stated[row.n]
            continue
        _require(clone is not None, f"{chosen.label} n={row.n}: no clone to read it from")
        assert clone is not None
        blob = _pinned_blob(chosen, row, clone)
        header = _header(_blobs(clone, [blob])[blob])
        _require(header is not None and header[0] == row.n, f"n={row.n}: no header")
        assert header is not None
        sides[row.n] = header[1]
    return sides


def earlier_publications(
    issue: int | str, clones: Mapping[str, Path], source: Path | None = None
) -> dict[str, Any]:
    """Every side a watched repository published at a release's claimed counts before the
    release's row, strictly below the record's standing side there (a tie is the start's own).

    ``clones`` maps each repository (``owner/name``) to a clone holding its history. Every
    certificate (``*.cert`` under any path, header ``n S``) and every bound an index file
    states (`INDEXES`) is a publication from the first commit that holds it, dated as
    `_dated_commits` says. At each count each distinct side keeps its first publication.
    ``source`` is a clone of the release's own repository, read for the sides of rows the
    packet does not derive (`release_sides`).
    """
    chosen = release(issue)
    custody(chosen)
    standing = _standing(chosen)
    claimed = {row.n: row for row in claims(chosen)}
    until = max(chosen.first_commit_of(n)[1] for n in claimed)
    rows: dict[int, dict[Fraction, dict[str, Any]]] = {n: {} for n in claimed}
    scanned = {}
    for name, clone in sorted(clones.items()):
        commits = _dated_commits(name, clone, until)
        first: dict[str, tuple[str, str, str]] = {}
        index_blobs: list[tuple[str, str, str, str]] = []
        for commit, when in commits:
            for line in _git(clone, "ls-tree", "-r", commit).splitlines():
                meta, _, path = line.partition("\t")
                blob = meta.split()[2]
                if path.endswith(".cert"):
                    first.setdefault(blob, (commit, when, path))
                elif path in INDEXES:
                    index_blobs.append((blob, commit, when, path))
        headers = {blob: _header(raw) for blob, raw in _blobs(clone, sorted(first)).items()}
        for blob, (commit, when, path) in first.items():
            header = headers[blob]
            if header is None or header[0] not in claimed:
                continue
            n, side = header
            if when >= chosen.first_commit_of(n)[1] or standing[n].covers(side):
                continue
            item = {
                "repository": name,
                "commit": commit,
                "published": when,
                "kind": "certificate",
                "path": path,
                "blob": blob,
            }
            kept = rows[n].get(side)
            if kept is None or when < kept["published"]:
                rows[n][side] = item
        seen: set[tuple[str, str]] = set()
        texts = _blobs(clone, sorted({blob for blob, *_ in index_blobs}))
        for blob, commit, when, path in index_blobs:
            if (blob, path) in seen:
                continue
            seen.add((blob, path))
            entries = json.loads(texts[blob])["entries"]
            for n in claimed:
                entry = entries.get(str(n))
                for key in INDEXES[path]:
                    entry = entry.get(key) if isinstance(entry, dict) else None
                if entry is None:
                    continue
                side = Fraction(str(entry))
                if when >= chosen.first_commit_of(n)[1] or standing[n].covers(side):
                    continue
                item = {
                    "repository": name,
                    "commit": commit,
                    "published": when,
                    "kind": "index",
                    "path": path,
                    "blob": blob,
                }
                kept = rows[n].get(side)
                if kept is None or when < kept["published"]:
                    rows[n][side] = item
        scanned[name] = {
            "head": _git(clone, "rev-parse", "HEAD").strip(),
            "commits": len(commits),
        }
    sides = release_sides(chosen, source)
    result = []
    for n in sorted(claimed):
        own = sides[n]
        result.append(
            {
                "n": n,
                "standing": legacy.literal(standing[n].side),
                **(
                    {"standing_construction": standing[n].form}
                    if standing[n].construction is not None
                    else {}
                ),
                "release_side": legacy.literal(own),
                "publications": [
                    {
                        **item,
                        "side": legacy.literal(side),
                        "ceiling_12": ceiling(side),
                        "release_below_by": legacy.literal(side - own),
                    }
                    for side, item in sorted(
                        rows[n].items(), key=lambda pair: pair[1]["published"]
                    )
                ],
            }
        )
    return {
        "format": EARLIER_FORMAT,
        "issue": chosen.issue_url,
        "until": until,
        "repositories": scanned,
        "pushed_later": {
            name: {"public_head": head, "pushed": time}
            for name, (head, time) in PUSHED_LATER.items()
        },
        "indexes": {path: ".".join(keys) for path, keys in INDEXES.items()},
        "rows": result,
    }


def write_earlier(
    issue: int | str, clones: Mapping[str, Path], source: Path | None
) -> dict[int, int]:
    """Write a release's earlier-publications receipt; return each count's publications."""
    record = earlier_publications(issue, clones, source)
    _write(release(issue).path(EARLIER), record)
    return {row["n"]: len(row["publications"]) for row in record["rows"] if row["publications"]}


#: The holders the ledgers print for each watched repository's publications.
HOLDERS = {
    "franciscouzo/square-packing": "Francisco Couzo",
    "evand/square-packing": "Evan Daniel (evand)",
}
RULE = (
    "If they are reported in order, then each one should be recorded as a result, as long "
    "as each one is stronger than the last. If a stronger result is reported first, then the "
    "other one should not be recorded since it is weaker after that, unless there is some key "
    "reason it should be recorded."
)


def _claim(n: int, side: Fraction, exact_from: str) -> dict[str, Any]:
    return {
        "n": n,
        "printed": ceiling(side),
        "rounding": "up",
        "exact": legacy.literal(side),
        "exact_from": exact_from,
    }


def _least_claims(items: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """One claim per count for a commit's publications: the least side it states there,
    naming the files and bounds it also states at that count (#722's review A, A2). The
    ledger keeps one claim of a report per count, so a commit that states two sides at
    a count is its least."""
    by_n: dict[int, list[Mapping[str, Any]]] = {}
    for item in items:
        by_n.setdefault(int(item["n"]), []).append(item)
    found = []
    for n, stated in sorted(by_n.items()):
        ranked = sorted(stated, key=lambda item: (Fraction(item["side"]), item["path"]))
        least = ranked[0]
        what = "its header" if least["kind"] == "certificate" else "the bound it states"
        where = f"{least['path']} at {least['repository']}@{least['commit']} ({what})"
        others = [item["path"] for item in ranked[1:]]
        if others:
            where += (
                f"; the least of the {len(ranked)} sides the commit states at this count, "
                f"beside {', '.join(others)}"
            )
        found.append(_claim(n, Fraction(least["side"]), where))
    return found


def same_commit_claim(
    chosen: Release, row: Claim, named: Fraction, lower: SameCommitLeast
) -> dict[str, Any]:
    """A row's claim at the least side its commit states at the count (#722's review A,
    A2): the side of the other file `lower` names, read from the packet that retains it,
    which must be below the side of the file the issue names. The claim says which file
    it is, that the issue named the other, and where the author claimed this one."""
    side = reports.import_side(lower.packet, row.n)
    _require(side < named, f"n={row.n}: {lower.path} is not below the file the issue names")
    where = (
        f"{lower.path} at {chosen.retained[:8]} (its header), retained in the "
        f"{lower.packet} packet: the least of the 2 sides the commit states at this count, "
        f"beside {row.path}, the file the issue names (facts/n-{row.n:03d}.yaml.gz in the "
        f"{chosen.packet} packet), which the record registered before the author claimed "
        f"this one ({lower.claimed})"
    )
    return _claim(row.n, side, where)


def _earlier_bead(walk: Walk, label: str, chosen: Release) -> str:
    """The bead that owned an earlier publication when ``walk`` was made: its pending
    import's, its own import's once it is a release here, else the walk's."""
    if label in walk.awaiting:
        return walk.awaiting[label].bead
    if label in RELEASES:
        return RELEASES[label].bead
    return chosen.bead


def ledger_sources(issue: int | str, read_at_main: str, read_on: str) -> dict[str, Any]:
    """The ``sources.yaml`` a release's walk reads, transcribed from the packets' receipts
    (`devtools.intake_ledger` gathers it).

    The reports are the release's own rows, at their exact sides, and every earlier report
    at its counts no row holds: each publication the release's earlier-publications receipt
    lists, at its exact side; #715's rows at the counts it re-certified below the print,
    which the walk decides as restatements (think-fwa9), and above ``LIMIT``, and #666's
    above ``LIMIT``, which wait on the owner (D1). A claim the start already holds is not
    walked again. The walk's rulings are `WALK_RULINGS`'.
    """
    chosen = release(issue)
    walk = walk_of(chosen)
    earlier = _read(chosen.path(EARLIER))
    by_n = {row["n"]: row for row in earlier["rows"]}
    counts = set(by_n)
    groups: dict[tuple[str, str], dict[str, Any]] = {}
    for row in earlier["rows"]:
        for item in row["publications"]:
            key = (item["repository"], item["commit"])
            label = f"{item['repository']}@{item['commit'][:7]}"
            group = groups.setdefault(
                key,
                {
                    "report": label,
                    "url": f"https://github.com/{item['repository']}/tree/{item['commit']}",
                    "reported_at": item["published"],
                    "holders": HOLDERS[item["repository"]],
                    "bead": _earlier_bead(walk, label, chosen),
                    "claims": [],
                },
            )
            group["claims"].append(item | {"n": row["n"]})
    publications = sorted(groups.values(), key=lambda group: group["reported_at"])
    for group in publications:
        group["claims"] = _least_claims(group["claims"])
        group["note"] = (
            "A publication in a watched repository with no issue, dated by its first commit, "
            "or by the later push that made it public; transcribed from the "
            f"{chosen.packet} packet's receipts/earlier-publications.json at each count "
            f"{chosen.label} claims where it is strictly below the record's standing side. "
            f"Its rows are its own import's ({group['bead']}); none is recorded by this pass."
        )
    couzo = release_715_claims(counts, by_n)
    de_winter = release(666)
    held_666 = [
        _claim(
            row.n,
            certificate(de_winter, row).side,
            f"{row.path} (its header), retained in the {de_winter.packet} packet",
        )
        | {"printed": row.printed}
        for row in held_claims(de_winter)
        if row.n in counts
    ]
    own = []
    for row in claims(chosen):
        side = Fraction(by_n[row.n]["release_side"])
        where = (
            f"facts/n-{row.n:03d}.yaml.gz in the {chosen.packet} packet, derived from "
            f"{row.path} at {chosen.retained[:8]} (its header)"
            if row.n <= LIMIT
            else f"{row.path} at {chosen.retained[:8]} (its header), pinned by digest in the "
            f"{chosen.packet} packet and read from a clone; not derived until the owner's D1"
        )
        claim = {
            "n": row.n,
            "printed": row.printed,
            "rounding": BINARY64 if chosen.rounding == BINARY64 else "up",
            "exact": legacy.literal(side),
            "exact_from": where,
        }
        if (lower := (chosen.same_commit_least or {}).get(row.n)) is not None:
            claim = same_commit_claim(chosen, row, side, lower)
        if row.n in (chosen.claimed_at or {}):
            claim["reported_at"] = (chosen.claimed_at or {})[row.n]
        own.append(claim)
    reports_list: list[dict[str, Any]] = [
        {
            "report": "#666",
            "issue": 666,
            "holders": de_winter.holders,
            "bead": "think-3m10",
            "claims": held_666,
            "note": (
                "Issue-table prints at the counts above 1024 that issue 719 also claims, each "
                f"with its certificate's exact header side from the {de_winter.packet} packet. "
                "Whether the record tracks counts above 1024 waits on the owner (think-f2io); "
                "none is recorded by this pass."
            ),
        },
        *publications,
        {
            "report": "#715",
            "issue": 715,
            "holders": "Francisco Couzo",
            "bead": "think-cyal",
            "claims": couzo,
            "note": (
                "Issue 715's rows at the counts issue 719 also claims that no row of the "
                "couzo-issue715-2026-10-21 source holds: its re-certifications of the "
                "4e4c8ce certificates below the 12-place print, at their exact sides from "
                "that packet's filtered replay, which restate those certificates by the "
                "owner's answer of 23 October 2026 (think-fwa9), and its rows above 1024, at "
                "the exact sides of the certificates the issue links, which wait on the owner "
                "(think-f2io). None is recorded by this pass. "
                "Its other rows at these counts, at 410, 413, 454, 490, 498, 544, 584, 596, "
                "637, 644, 689, 692, 699, 736, 743, 744, 746, 792 and 800, state the 4e4c8ce "
                "certificates' sides exactly, the same holder's, so they are not walked: each "
                "would be an exact tie, not recorded, and move nothing."
            ),
        },
        {
            "report": chosen.label,
            "issue": chosen.issue,
            "holders": chosen.holders,
            "bead": chosen.bead,
            "rounding": chosen.rounding,
            "claims": own,
            "note": (
                "Issue-table prints at all 122 counts: each is the binary64 value of the "
                "certificate's exact header side printed at 16 places, which lies below that "
                "side at 76 rows, so each claim carries the exact side and is compared by it. "
                "121 certificates were first committed at 1851c2c (05:29:48Z), a minute before "
                "the issue, and 447's at the pin (06:05:07Z). 366 and 447 are dated by the "
                "06:05:31Z edit that first claimed them; the issue opened with the other 120. "
                "No other report reached the repository at these counts between those times."
                + "".join(
                    f" {lower.note}"
                    for _, lower in sorted((chosen.same_commit_least or {}).items())
                )
            ),
        },
    ]
    document: dict[str, Any] = {
        "format": "intake-ledger-sources-v1",
        "read_at_main": read_at_main,
        "read_on": read_on,
        "rule": RULE,
        "lanes": [],
        "reports": [report for report in reports_list if report["claims"]],
    }
    if walk.name in WALK_RULINGS:
        document["rulings"] = WALK_RULINGS[walk.name]
    return document


def release_715_claims(
    counts: set[int], by_n: Mapping[int, Mapping[str, Any]]
) -> list[dict[str, Any]]:
    """#715's claims at ``counts`` that no row holds: its held re-certifications, at the
    exact sides its packet's filtered receipt states, and its rows above ``LIMIT``, at the
    side of the publication the earlier-publications receipt found its print to round up."""
    packet = WEB / "couzo-issue715-2026-10-21"
    held = _held_715()
    replayed = {
        row["n"]: row for row in _read(packet / "receipts/filtered-exact-replay.json")["rows"]
    }
    printed = {row.n: (row.printed, row.path) for row in couzo_715.claims()}
    found = []
    for n in sorted(counts):
        if n in held and n in replayed:
            row = replayed[n]
            found.append(
                _claim(
                    n,
                    Fraction(row["exact_side"]),
                    f"{row['certificate']} (its header) at "
                    "franciscouzo/square-packing@6b7391de, retained and replayed in the "
                    "couzo-issue715-2026-10-21 packet",
                )
                | {"printed": row["printed"]}
            )
        elif n > LIMIT and n in printed:
            sides = [
                Fraction(item["side"])
                for item in by_n[n]["publications"]
                if item["kind"] == "certificate" and item["ceiling_12"] == printed[n][0]
            ]
            _require(
                len(set(sides)) == 1, f"#715 n={n}: no one certificate its print rounds up"
            )
            found.append(
                _claim(
                    n,
                    sides[0],
                    f"{printed[n][1]} (its header) at franciscouzo/square-packing@6b7391de, "
                    "the certificate the issue links, read from a clone; not retained "
                    "(think-f2io)",
                )
                | {"printed": printed[n][0]}
            )
    return found


def write_ledger_sources(issue: int | str, read_at_main: str, read_on: str) -> int:
    """Write the release's walk's ``sources.yaml``; return how many reports it holds."""
    import yaml  # noqa: PLC0415

    document = ledger_sources(issue, read_at_main, read_on)
    target = walk_of(release(issue)).directory / "sources.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(target) as temporary:
        temporary.write_text(
            yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=100),
            encoding="utf-8",
        )
    return len(document["reports"])


# --------------------------------------------------------------------------- the history walk


#: Where the history walk's scan of the watched repositories is kept: beside the 4e4c8ce
#: packet's receipts, since the scan is the history of that index's author.
HISTORY_PUBLICATIONS = WEB / "couzo-index-2026-10-15/receipts/history-publications.json"
HISTORY_FORMAT = "beyond-horizon-history-publications-v1"
#: Tables whose rows state composite sides rounded up at the places given.
TABLES = {"composites/table.csv": 15}
WATCHED_HOLDERS = {
    "franciscouzo/square-packing": "Francisco Couzo",
    "evand/square-packing": "Evan Daniel",
    "TheSnakeFang/squarepack-certs": "Kevin Fang",
    "JoostdeWinter/joostdewinter.github.io": "Joost de Winter",
    "JoostdeWinter/square-packing": "Joost de Winter",
}


def history_start_highs(coverage: Mapping[str, Any]) -> dict[int, Fraction]:
    """Each count's frozen start as `devtools.intake_ledger` reads it from ``coverage``, the
    register at `HISTORY_READ_AT_MAIN`: the high end of the side it may be."""
    from devtools import intake_ledger  # noqa: PLC0415

    rows = coverage_current(coverage)
    return {
        n: intake_ledger.side_of(intake_ledger.beyond_member(n, rows)).span.high
        for n in HISTORY_COUNTS
    }


def coverage_current(coverage: Mapping[str, Any]) -> dict[int, Mapping[str, Any]]:
    from devtools import check_source_coverage as coverage_check  # noqa: PLC0415

    return coverage_check.current_beyond_horizon(coverage)


def write_history_starts(start_coverage: Path, counts: Sequence[int]) -> int:
    """Freeze the history walk's starts at ``counts`` from ``start_coverage``, the coverage
    register of a checkout of `HISTORY_READ_AT_MAIN` (read by path, never from Git)."""
    import yaml  # noqa: PLC0415

    from devtools import intake_ledger  # noqa: PLC0415

    rows = coverage_current(safe_load(start_coverage.read_text(encoding="utf-8")))
    members = {n: [intake_ledger.beyond_member(n, rows)] for n in sorted(counts)}
    document = intake_ledger.starts_document(HISTORY_READ_AT_MAIN, members)
    target = INTAKE / HISTORY / intake_ledger.STARTS
    target.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(target) as temporary:
        temporary.write_text(
            yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=88),
            encoding="utf-8",
        )
    return len(members)


def _table_sides(raw: bytes, places: int) -> list[tuple[int, Fraction, str]]:
    """A composites table's rows: the count, the side its print rounds up to at ``places``,
    and the row's id."""
    import csv  # noqa: PLC0415
    import io  # noqa: PLC0415

    found = []
    for row in csv.DictReader(io.StringIO(raw.decode("utf-8"))):
        printed = row[f"side_rounded_up_{places}"]
        found.append((int(row["count"]), Fraction(printed), str(row["id"])))
    return found


def first_publications(name: str, clone: Path) -> list[dict[str, Any]]:
    """Every side a repository published at `HISTORY_COUNTS`, each at the first commit that
    stated it, by publication time and then history order (`_dated_commits`): a
    certificate's header, a bound an index states (`INDEXES`), or a table row (`TABLES`)."""
    commits = _dated_commits(name, clone, "9999-12-31T23:59:59Z")
    rank = {commit: index for index, (commit, _) in enumerate(commits)}
    files: dict[tuple[str, str], tuple[str, str]] = {}
    for commit, when in commits:
        for line in _git(clone, "ls-tree", "-r", commit).splitlines():
            meta, _, path = line.partition("\t")
            if path.endswith(".cert") or path in INDEXES or path in TABLES:
                key = (meta.split()[2], path)
                kept = files.get(key)
                if kept is None or (when, rank[commit]) < (kept[1], rank[kept[0]]):
                    files[key] = (commit, when)
    texts = _blobs(clone, sorted({blob for blob, _ in files}))
    stated: list[tuple[int, Fraction, dict[str, Any]]] = []
    for (blob, path), (commit, when) in files.items():
        item = {"repository": name, "commit": commit, "published": when, "path": path}
        if path.endswith(".cert"):
            header = _header(texts[blob])
            if header is not None:
                stated.append((*header, item | {"kind": "certificate", "blob": blob}))
        elif path in TABLES:
            for n, side, ident in _table_sides(texts[blob], TABLES[path]):
                where = f"{path}:{ident}"
                stated.append((n, side, item | {"kind": "table", "path": where, "blob": blob}))
        else:
            entries = json.loads(texts[blob]).get("entries") or {}
            for key, entry in entries.items():
                bound: Any = entry
                for part in INDEXES[path]:
                    bound = bound.get(part) if isinstance(bound, dict) else None
                if bound is not None and str(key).isdigit():
                    side = Fraction(str(bound))
                    stated.append((int(key), side, item | {"kind": "index", "blob": blob}))
    first: dict[tuple[int, Fraction], dict[str, Any]] = {}
    for n, side, item in stated:
        if n not in HISTORY_COUNTS:
            continue
        kept = first.get((n, side))
        order = (item["published"], rank[item["commit"]], item["path"])
        if kept is None or order < (kept["published"], rank[kept["commit"]], kept["path"]):
            first[n, side] = item
    return [
        item | {"n": n, "side": legacy.literal(side)}
        for (n, side), item in sorted(first.items(), key=lambda pair: (pair[0][0], pair[0][1]))
    ]


def history_publications(clones: Mapping[str, Path], start_coverage: Path) -> dict[str, Any]:
    """The history walk's scan of the watched repositories: at each count, every side a
    repository published strictly below the high end of the count's frozen start, at the
    first commit of any of them that stated it, a copy in a later commit or another
    repository being no report of its own; a side at or above the start could never be
    recorded.

    Each publication keeps its kind, path and Git blob; a table row is a print rounded up
    at its places, every other side exact. ``start_coverage`` is the register of a checkout
    of `HISTORY_READ_AT_MAIN`, which freezes the starts (`write_history_starts`)."""
    highs = history_start_highs(safe_load(start_coverage.read_text(encoding="utf-8")))
    scanned: dict[str, Any] = {}
    first: dict[tuple[int, Fraction], dict[str, Any]] = {}
    for name, clone in sorted(clones.items()):
        items = [
            item
            for item in first_publications(name, clone)
            if Fraction(item["side"]) < highs[item["n"]]
        ]
        for item in items:
            key = (item["n"], Fraction(item["side"]))
            if key not in first or item["published"] < first[key]["published"]:
                first[key] = item
        scanned[name] = {
            "head": _git(clone, "rev-parse", "HEAD").strip(),
            "commits": len(_git(clone, "rev-list", "HEAD").split()),
        }
    found = list(first.values())
    for name, record in scanned.items():
        record["publications"] = sum(1 for item in found if item["repository"] == name)
    return {
        "format": HISTORY_FORMAT,
        "read_at_main": HISTORY_READ_AT_MAIN,
        "counts": [HISTORY_COUNTS.start, HISTORY_COUNTS.stop - 1],
        "repositories": scanned,
        "pushed_later": {
            name: {"public_head": head, "pushed": time}
            for name, (head, time) in PUSHED_LATER.items()
        },
        "indexes": {path: ".".join(keys) for path, keys in INDEXES.items()},
        "tables": {path: f"rounded up at {places} places" for path, places in TABLES.items()},
        "publications": sorted(
            found, key=lambda item: (item["n"], item["published"], item["repository"])
        ),
    }


def write_history_publications(clones: Mapping[str, Path], start_coverage: Path) -> int:
    """Write the scan (`history_publications`) and freeze the starts at every count it, or
    a row of the register, reaches; return the publications found."""
    record = history_publications(clones, start_coverage)
    _write(HISTORY_PUBLICATIONS, record)
    coverage = safe_load(COVERAGE.read_text(encoding="utf-8"))
    counts = {item["n"] for item in record["publications"]} | {
        row["n"] for row in coverage["beyond_horizon_claims"] if row["n"] in HISTORY_COUNTS
    }
    write_history_starts(start_coverage, sorted(counts))
    return len(record["publications"])


def _source_times(source: Mapping[str, Any]) -> str:
    """When a row source's packet pin was committed, from its acquisition record."""
    local = source.get("local", "")
    record = ROOT / local.removeprefix("/") / "acquisition/sources.json"
    commit = re.search(r"/tree/([0-9a-f]{40})", source.get("url", ""))
    _require(record.is_file() and commit is not None, f"{source['id']}: no pinned commit")
    assert commit is not None
    for item in json.loads(record.read_text(encoding="utf-8"))["sources"]:
        if item["source_commit"] == commit[1]:
            return str(item["committed_utc"])
    raise ReplayError(f"{source['id']}: the acquisition record does not pin {commit[1]}")


def exact_row_side(source: Mapping[str, Any], n: int) -> Fraction:
    """A row's exact side, from its source's claims record (`_stated_side`); the history
    walk compares sides exactly, so a row whose record keeps only a print is refused."""
    side = _stated_side(source, n)
    _require(
        side is not None, f"{source['id']} n={n}: its claims record states no one exact side"
    )
    assert side is not None
    return side


def _history_rows(coverage: Mapping[str, Any]) -> dict[str, list[tuple[int, Fraction, str]]]:
    """Every row source's rows the history walk takes, by source: each count, exact side
    (from its claims record) and the value the row records. The walk takes the row sources
    it declares (`HISTORY_SOURCES`); a later source, as #732's, is walked by its own walk.
    The starts' sources are the walk's starts, and a release of the walk is walked as its
    publication instead."""
    ours = {item.source for item in RELEASES.values() if item.walk == HISTORY}
    sources = {source["id"]: source for source in coverage["sources"]}
    found: dict[str, list[tuple[int, Fraction, str]]] = {}
    for row in coverage["beyond_horizon_claims"]:
        source = row["source_id"]
        if row["n"] not in HISTORY_COUNTS or source not in HISTORY_SOURCES or source in ours:
            continue
        side = exact_row_side(sources[source], row["n"])
        found.setdefault(source, []).append((row["n"], side, str(row["value"])))
    return {source: sorted(rows) for source, rows in found.items()}


def _counted(total: int) -> str:
    return "1 count" if total == 1 else f"{total} counts"


def _compress_counts(counts: Iterable[int]) -> str:
    """Counts written out in order, separated by commas and a final "and"."""
    return _listing([str(n) for n in sorted(counts)])


def _listing(parts: Sequence[str]) -> str:
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]


def held_sentence(walk: Walk, report: str) -> str:
    """What ``walk`` holds of a report and what of its verdicts rests on holds, for the
    report's note in the walk's ``sources.yaml``: the ledger says it beside the verdicts.
    The history walk declares its holds as `HISTORY_HELD` and `HISTORY_RESTING`, every
    other walk in `WALKS`."""
    text = ""
    history = walk.name == HISTORY
    held_name = "HISTORY_HELD" if history else f"WALKS[{walk.name!r}].held"
    resting_name = "HISTORY_RESTING" if history else f"WALKS[{walk.name!r}].resting"
    items = [item for item in walk.held.get(report, ()) if not item.answer]
    if items:
        parts = [
            f"{len(item.counts)} "
            + (HELD_NAMES if len(item.counts) > 1 else HELD_NAME)[item.kind]
            + (f", {item.note}" if item.note else "")
            + f" ({', '.join((item.bead, *item.also))})"
            for item in items
        ]
        total = sum(len(item.counts) for item in items)
        text += (
            f" The walk holds its publications at {_counted(total)} back from a row, each "
            f"waiting on an owner decision (beyond_horizon_replay.{held_name}): "
            f"{_listing(parts)}."
        )
    for item in walk.held.get(report, ()):
        if item.answer:
            text += (
                f" Its {len(item.counts)} "
                + (HELD_NAMES if len(item.counts) > 1 else HELD_NAME)[item.kind]
                + (f", {item.note}" if item.note else "")
                + f", at {_compress_counts(item.counts)}, have no row by {item.answer} "
                f"(beyond_horizon_replay.{held_name})."
            )
    resting = [item for item in walk.resting if item.report == report]
    if resting:
        parts = [
            f"{len(item.counts)} against "
            + " and ".join(HELD_NAMES[kind] for kind in item.kinds)
            + ("" if item.verdict == NOT_RECORDED else f", {item.verdict}")
            for item in resting
        ]
        total = sum(len(item.counts) for item in resting)
        text += (
            f" Its verdicts at {_counted(total)} are decided only against held publications "
            f"(beyond_horizon_replay.{resting_name}): {_listing(parts)}. An answer that "
            "leaves a hold out reruns this walk."
        )
    return text


def history_sources(read_on: str) -> dict[str, Any]:
    """The history walk's ``sources.yaml``, transcribed from the register and the scan.

    The reports are every row source since `HISTORY_READ_AT_MAIN` at its rows' exact sides,
    and every publication the scan found (`history_publications`) that no row holds, one
    report a commit, at the least side the commit states at each count (#722's review A,
    A2). A publication of a row's side is that row's report; where it came before the issue
    that reported the row, the claim says when (``first_committed``). #715's
    re-certifications below the print are #715's claims, at the exact sides its packet's
    filtered receipt states, which the walk decides as restatements (think-fwa9). A row
    source an issue did not report is dated, side by side, by the first publication of the
    side, else its packet's pinned commit. The walk's rulings are `WALK_RULINGS`'.
    """
    coverage = safe_load(COVERAGE.read_text(encoding="utf-8"))
    sources = {source["id"]: source for source in coverage["sources"]}
    scan = _read(HISTORY_PUBLICATIONS)
    rows = _history_rows(coverage)
    packet_715 = WEB / "couzo-issue715-2026-10-21"
    held_715 = _held_715()
    replayed = {
        row["n"]: row
        for row in _read(packet_715 / "receipts/filtered-exact-replay.json")["rows"]
    }
    rows.setdefault("couzo-issue715-2026-10-21", []).extend(
        (n, Fraction(replayed[n]["exact_side"]), str(replayed[n]["printed"]))
        for n in sorted(held_715)
        if n in HISTORY_COUNTS
    )
    by_side: dict[tuple[int, Fraction], str] = {
        (n, side): source for source, items in rows.items() for n, side, _ in items
    }
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for item in scan["publications"]:
        groups.setdefault((item["repository"], item["commit"]), []).append(item)
    attached: dict[tuple[int, Fraction], dict[str, Any]] = {}
    publications = []
    for (repository, commit), items in sorted(
        groups.items(), key=lambda pair: (pair[1][0]["published"], pair[0])
    ):
        claims = []
        for claim in _least_claims(items):
            side = Fraction(claim["exact"])
            least = next(
                item
                for item in items
                if item["n"] == claim["n"] and Fraction(item["side"]) == side
            )
            if (claim["n"], side) in by_side:
                attached[claim["n"], side] = least
                continue
            if least["kind"] == "table":
                places = TABLES[least["path"].split(":", 1)[0]]
                printed = {key: value for key, value in claim.items() if key != "exact"}
                claims.append(printed | {"printed": ceiling(side, places)})
            else:
                claims.append(claim)
        if claims:
            publications.append(
                {
                    "report": f"{repository}@{commit[:7]}",
                    "url": f"https://github.com/{repository}/tree/{commit}",
                    "reported_at": items[0]["published"],
                    "holders": WATCHED_HOLDERS[repository],
                    "bead": _publication_bead(f"{repository}@{commit[:7]}"),
                    "claims": claims,
                    "note": (
                        "A publication in a watched repository that no issue reports, dated "
                        "by its commit, or by the later push that made it public; "
                        "transcribed from the history scan "
                        f"({HISTORY_PUBLICATIONS.relative_to(ROOT).as_posix()}) at each "
                        "count where it states a side strictly below the frozen start "
                        "that no row holds, at the least side the commit states there."
                        + held_sentence(WALKS[HISTORY], f"{repository}@{commit[:7]}")
                    ),
                }
            )
    reports_list: list[dict[str, Any]] = []
    for source, items in sorted(rows.items()):
        label = history_label(source)
        claims = []
        for n, side, _ in items:
            claim: dict[str, Any] = _claim(n, side, _history_where(sources[source], n))
            first = attached.get((n, side))
            if label.startswith("#"):
                if first is not None:
                    claim["first_committed"] = first["published"]
            else:
                pinned = _source_times(sources[source])
                when = min(pinned, first["published"]) if first is not None else pinned
                claim["reported_at"] = when
            claims.append(claim)
        issue = HISTORY_ISSUES.get(source)
        report: dict[str, Any] = {
            "report": label,
            "holders": issue[1] if issue else WATCHED_HOLDERS[_repository(sources[source])],
            "bead": issue[2] if issue else _row_bead(coverage, source),
            "claims": claims,
            "note": _history_note(source, label) + held_sentence(WALKS[HISTORY], label),
        }
        if issue is not None:
            report["issue"] = issue[0]
        else:
            earliest = min(claim["reported_at"] for claim in claims)
            for claim in claims:
                if claim["reported_at"] == earliest:
                    claim.pop("reported_at")
            report |= {"url": sources[source]["url"], "reported_at": earliest}
        reports_list.append(report)
    return {
        "format": "intake-ledger-sources-v1",
        "read_at_main": HISTORY_READ_AT_MAIN,
        "read_on": read_on,
        "rule": RULE,
        "lanes": [],
        "reports": reports_list + publications,
        "rulings": WALK_RULINGS[HISTORY],
    }


def _repository(source: Mapping[str, Any]) -> str:
    match = re.match(r"https://github\.com/([^/]+/[^/]+)/tree/", str(source.get("url", "")))
    _require(match is not None, f"{source['id']}: not a watched repository's tree")
    assert match is not None
    return match[1]


def _row_bead(coverage: Mapping[str, Any], source: str) -> str:
    """The bead most of a source's rows name."""
    from collections import Counter  # noqa: PLC0415

    beads = Counter(
        str(row.get("bead") or "")
        for row in coverage["beyond_horizon_claims"]
        if row["source_id"] == source
    )
    return beads.most_common(1)[0][0] if beads else ""


def _publication_bead(label: str) -> str:
    """The bead a watched publication's claims wait on: its release's, else its holds'."""
    chosen = RELEASES.get(label)
    if chosen is not None:
        return chosen.bead
    held = WALKS[HISTORY].held.get(label, ()) if HISTORY in WALKS else ()
    return held[0].bead if held else ""


def _history_where(source: Mapping[str, Any], n: int) -> str:
    return f"the exact side at n = {n} in the source's claims record, {source['claims_record']}"


def _history_note(source: str, label: str) -> str:
    if source == "couzo-issue715-2026-10-21":
        return (
            "Issue 715's rows, at the exact sides its source's claims record states, and its "
            "30 re-certifications of the 4e4c8ce certificates below the 12-place print, at "
            "the exact sides of the certificates its packet's filtered receipt states, which "
            "restate those certificates by the owner's answer of 23 October 2026 "
            "(think-fwa9). Its other restatements of earlier certificates tie them exactly "
            "and are not walked."
        )
    if label.startswith("#"):
        return (
            f"The {source} source's dated beyond-horizon rows at these counts, at the exact "
            "sides its claims record states, dated by the issue; where a watched repository "
            "published a side first, the claim says when (first_committed)."
        )
    return (
        f"The {source} source's dated beyond-horizon rows at these counts, at the exact sides "
        "its claims record states, a watched repository's publication that no issue reports: "
        "each dated by the first commit that published its side, else by the commit its "
        "packet pins."
    )


def write_history_sources(read_on: str) -> int:
    """Write the history walk's ``sources.yaml``; return how many reports it holds."""
    import yaml  # noqa: PLC0415

    document = history_sources(read_on)
    target = INTAKE / HISTORY / "sources.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(target) as temporary:
        temporary.write_text(
            yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=100),
            encoding="utf-8",
        )
    return len(document["reports"])


# --------------------------------------------------------------------------- issue #732


#: A certificate file's path that names its count, under every layout of certificate
#: files the #732 source has used: ``certificates/nN.cert``, ``certificates/n-N.cert`` and
#: its suffixed variants (``n-N_tight.cert``), ``certificates/square-N.cert``, and the
#: thousands folders ``certificates/NNNN-NNNN/nN.cert``. Nothing else names a side to it.
#: The source's decimal poses, ``certificates/square-N.txt`` (343 to 360 in the band, since
#: ``2b76e6f`` of 9 October and still at the pin), are not certificates; every one is above
#: the grid's 19 (``mishapolk-decimal-poses-2026-10-09``). Its indexes, ``upper_bounds.json``
#: and ``certified_bounds.json``, are not read either (#742's review A, A4).
_COUNT_NAMED = re.compile(
    r"certificates/(?:[0-9]{4}-[0-9]{4}/)?(?:n-?|square-)([1-9][0-9]*)[^/]*\.cert"
)
SOURCE_HISTORY = Path("receipts/source-history.json")
SOURCE_HISTORY_FORMAT = "beyond-horizon-source-history-v1"
#: The #732 source's index of its certificates beyond the corpus, which the issue pins by
#: digest: each count's certificate path, SHA-256 and exact bound.
SOURCE_MANIFEST = "certificates/manifest.json"


def named_count(path: str) -> int | None:
    """The count a certificate's path names (`_COUNT_NAMED`), or None for any other path."""
    match = _COUNT_NAMED.fullmatch(path)
    return None if match is None else int(match[1])


def source_history(issue: int | str, clone: Path) -> dict[str, Any]:
    """Every side a release's own repository published in a certificate file at
    `HISTORY_COUNTS`, from a clone.

    The repository is watched, so each certificate there is a publication from the first
    commit of the retained commit's history that holds its side. Only certificate files
    whose paths name a count in `HISTORY_COUNTS` are read (`_COUNT_NAMED`), so a blobless
    clone fetches no certificate above ``LIMIT``, and each file's header must state the
    count its path names. At the retained commit each count's certificate is listed with
    its Git blob, SHA-256 and exact side, the first commit that holds its side and the first
    that holds its blob, and is held to the source's manifest (`SOURCE_MANIFEST`): the path,
    digest and exact bound the manifest states for the count must be the file's.

    The source's decimal poses and its own indexes are not read. At #732's source no
    ``verified`` or certified bound either index states at 325 to 1024, the lanes the history
    scan reads of an index (`INDEXES`), is below the start and every side walked there, at
    any commit that holds it; only ``3285fac``'s ``reported`` lane is, where it restates the
    Kingbird catalogue's 14-place prints (the packet README).
    """
    chosen = release(issue)
    chain = _git(clone, "rev-list", "--reverse", "--topo-order", chosen.retained).split()
    _require(chain and chain[-1] == chosen.retained, "the clone does not hold the commit")
    times = {
        commit: _utc(stamp)
        for commit, stamp in (
            line.split(" ", 1)
            for line in _git(clone, "log", "--format=%H %cI", chosen.retained).splitlines()
        )
    }
    rank = {commit: index for index, commit in enumerate(chain)}
    first: dict[tuple[str, str], str] = {}
    at_pin: dict[int, list[tuple[str, str]]] = {}
    for commit in chain:
        for line in _git(clone, "ls-tree", "-r", commit).splitlines():
            meta, _, path = line.partition("\t")
            n = named_count(path)
            if n is None or n not in HISTORY_COUNTS:
                continue
            blob = meta.split()[2]
            first.setdefault((blob, path), commit)
            if commit == chosen.retained:
                at_pin.setdefault(n, []).append((path, blob))
    texts = _blobs(clone, sorted({blob for blob, _ in first}))
    sides: dict[str, Fraction] = {}
    for (blob, path), _commit in sorted(first.items()):
        header = _header(texts[blob])
        _require(
            header is not None and header[0] == named_count(path),
            f"{path} ({blob[:8]}): its header does not state the count its name gives",
        )
        assert header is not None
        sides[blob] = header[1]
    published: dict[tuple[int, Fraction], dict[str, Any]] = {}
    blob_first: dict[str, str] = {}
    for (blob, path), commit in first.items():
        n, side = int(named_count(path) or 0), sides[blob]
        kept = blob_first.get(blob)
        if kept is None or rank[commit] < rank[kept]:
            blob_first[blob] = commit
        item = {"commit": commit, "published": times[commit], "path": path, "blob": blob}
        order = (rank[commit], path)
        held = published.get((n, side))
        if held is None or order < (rank[held["commit"]], held["path"]):
            published[n, side] = item
    (listed,) = _git(clone, "ls-tree", chosen.retained, "--", SOURCE_MANIFEST).splitlines()
    manifest_blob = listed.split("\t", 1)[0].split()[2]
    manifest_raw = _blobs(clone, [manifest_blob])[manifest_blob]
    stated = json.loads(manifest_raw)["witnesses"]
    pin_rows = []
    for n in sorted(at_pin):
        _require(len(at_pin[n]) == 1, f"n={n}: the commit holds {len(at_pin[n])} files")
        ((path, blob),) = at_pin[n]
        raw = texts[blob]
        side = sides[blob]
        entry = stated.get(str(n))
        digest = hashlib.sha256(raw).hexdigest()
        _require(
            entry is not None
            and entry["certificate"] == path
            and entry["certificate_sha256"] == digest
            and Fraction(entry["bound"]) == side,
            f"n={n}: {path} is not the certificate, digest and bound {SOURCE_MANIFEST} states",
        )
        origin = published[n, side]
        pin_rows.append(
            {
                "n": n,
                "certificate": path,
                "blob": blob,
                "sha256": digest,
                "side": legacy.literal(side),
                "ceiling_12": ceiling(side),
                "side_first_commit": origin["commit"],
                "side_first_published": origin["published"],
                "side_first_path": origin["path"],
                "blob_first_commit": blob_first[blob],
                "blob_first_published": times[blob_first[blob]],
            }
        )
    in_range = sorted(int(key) for key in stated if int(key) in HISTORY_COUNTS)
    _require(
        in_range == sorted(at_pin),
        f"{SOURCE_MANIFEST} states other counts at or below {LIMIT} than the commit holds",
    )
    return {
        "format": SOURCE_HISTORY_FORMAT,
        "source": chosen.source_url,
        "retained_commit": chosen.retained,
        "history_commits": len(chain),
        "counts": [HISTORY_COUNTS.start, HISTORY_COUNTS.stop - 1],
        "manifest": SOURCE_MANIFEST,
        "manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "at_commit": pin_rows,
        "publications": [
            {"n": n, "side": legacy.literal(side), **item}
            for (n, side), item in sorted(
                published.items(), key=lambda pair: (pair[0][0], pair[1]["published"])
            )
        ],
    }


def write_source_history(issue: int | str, clone: Path) -> dict[str, int]:
    """Write a release's source-history receipt; return its counts at the commit and its
    publications."""
    record = source_history(issue, clone)
    _write(release(issue).path(SOURCE_HISTORY), record)
    return {"at_commit": len(record["at_commit"]), "publications": len(record["publications"])}


def _start_highs(walk: Walk, read_at_main: str, counts: Iterable[int]) -> dict[int, Fraction]:
    """The high end of each count's start in ``walk``: from its frozen ``starts.yaml``, or,
    before ``gather`` has frozen one, from the checkout's records, which must then be
    those of ``read_at_main`` (`devtools.intake_ledger.tree_members`)."""
    from devtools import intake_ledger  # noqa: PLC0415

    wanted = sorted(set(counts))
    if (walk.directory / intake_ledger.STARTS).is_file():
        starts = intake_ledger.load_starts(walk.directory, read_at_main)
        missing = [n for n in wanted if n not in starts]
        _require(not missing, f"{walk.name}: the frozen starts have no count {missing[:5]}")
        return {n: max(member.span.high for member in starts[n]) for n in wanted}
    members = intake_ledger.tree_members(wanted)
    return {
        n: max(intake_ledger.side_of(member).span.high for member in members[n]) for n in wanted
    }


#: Who holds the #732 source's own publications, as the ledgers print it.
MISHAPOLK_HOLDER = "Mykhailo Polkovskyi"


def release_walk_sources(issue: int | str, read_on: str) -> dict[str, Any]:
    """The ``sources.yaml`` of a release whose walk reads its own source's history (#732).

    The reports, at each count the release claims at or below ``LIMIT``:

    - the release's claims, every certificate its source holds at the retained commit, at
      the exact sides the source-history receipt states (`source_history`), dated by the
      issue, each with the first commit that published its side (``first_committed``);
    - the source's own earlier publications of other sides at those counts, one report a
      commit, dated by the commit: the repository is watched;
    - every publication of the watched repositories the history scan found
      (`HISTORY_PUBLICATIONS`), one report a commit, at the least side the commit states
      at each count (#722's review A, A2), and #715's re-certifications below the print,
      at the exact sides its packet's filtered receipt states, which the walk decides as
      restatements (think-fwa9); a publication of a side #715 re-certified is #715's report.

    Every earlier publication is walked only where it is strictly below the count's start
    (`_start_highs`): at or above it, it could never be recorded or change a verdict. The
    start is frozen at the walk's ``read_at_main``.
    """
    chosen = release(issue)
    walk = walk_of(chosen)
    history = _read(chosen.path(SOURCE_HISTORY))
    own = {row["n"]: row for row in history["at_commit"] if row["n"] <= LIMIT}
    highs = _start_highs(walk, ISSUE_732_READ_AT_MAIN, own)
    claims = []
    for n, row in sorted(own.items()):
        side = Fraction(row["side"])
        claim = _claim(
            n,
            side,
            f"{row['certificate']} at {chosen.retained[:8]} (its header), pinned by digest "
            f"in the {chosen.packet} packet (receipts/source-history.json)",
        )
        claim["first_committed"] = row["side_first_published"]
        claims.append(claim)
    reports_list: list[dict[str, Any]] = [
        {
            "report": chosen.label,
            "issue": chosen.issue,
            "holders": chosen.holders,
            "bead": chosen.bead,
            "claims": claims,
            "note": (
                f"The {len(claims)} certificates the source holds at "
                f"{chosen.retained[:8]} beyond the corpus at or below {LIMIT}, which its "
                f"manifest ({SOURCE_MANIFEST}, pinned by the SHA-256 the issue states) lists "
                "as the issue's claims there, each at its header's exact side and dated by "
                "the issue; first_committed is the first commit of the source's history "
                "that published the side." + held_sentence(walk, chosen.label)
            ),
        }
    ]
    repository = repository_of(chosen.source_url)
    earlier: dict[str, list[dict[str, Any]]] = {}
    for item in history["publications"]:
        n, side = item["n"], Fraction(item["side"])
        mine = own.get(n)
        if mine is None or side == Fraction(mine["side"]) or side >= highs[n]:
            continue
        earlier.setdefault(item["commit"], []).append(
            {**item, "repository": repository, "kind": "certificate"}
        )
    for commit, items in sorted(earlier.items(), key=lambda pair: pair[1][0]["published"]):
        label = f"{repository}@{commit[:7]}"
        reports_list.append(
            {
                "report": label,
                "url": f"{chosen.source_url}/tree/{commit}",
                "reported_at": items[0]["published"],
                "holders": MISHAPOLK_HOLDER,
                "bead": chosen.bead,
                "claims": _least_claims(items),
                "note": (
                    f"The {chosen.label} source's own publications, dated by the commit: the "
                    "repository is watched, so each certificate there is a report from the "
                    "first commit that holds its side. Transcribed from the "
                    f"{chosen.packet} packet's receipts/source-history.json at each count "
                    f"{chosen.label} claims where the commit states a side other than the "
                    "one the issue claims, strictly below the start."
                    + held_sentence(walk, label)
                ),
            }
        )
    held_715 = _held_715()
    replayed = {
        row["n"]: row
        for row in _read(WEB / "couzo-issue715-2026-10-21/receipts/filtered-exact-replay.json")[
            "rows"
        ]
    }
    couzo = [
        _claim(
            n,
            Fraction(replayed[n]["exact_side"]),
            f"{replayed[n]['certificate']} (its header) at "
            "franciscouzo/square-packing@6b7391de, retained and replayed in the "
            "couzo-issue715-2026-10-21 packet",
        )
        | {"printed": replayed[n]["printed"]}
        for n in sorted(held_715 & set(own))
        if Fraction(replayed[n]["exact_side"]) < highs[n]
    ]
    by_side = {(claim["n"], Fraction(claim["exact"])) for claim in couzo}
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for item in _read(HISTORY_PUBLICATIONS)["publications"]:
        n, side = item["n"], Fraction(item["side"])
        if n not in own or side >= highs[n] or (n, side) in by_side:
            continue
        groups.setdefault((item["repository"], item["commit"]), []).append(item)
    publications = []
    for (name, commit), items in sorted(
        groups.items(), key=lambda pair: (pair[1][0]["published"], pair[0])
    ):
        found = []
        for claim in _least_claims(items):
            least = next(
                item
                for item in items
                if item["n"] == claim["n"]
                and Fraction(item["side"]) == Fraction(claim["exact"])
            )
            if least["kind"] == "table":
                places = TABLES[least["path"].split(":", 1)[0]]
                printed = {key: value for key, value in claim.items() if key != "exact"}
                found.append(printed | {"printed": ceiling(Fraction(claim["exact"]), places)})
            else:
                found.append(claim)
        label = f"{name}@{commit[:7]}"
        publications.append(
            {
                "report": label,
                "url": f"https://github.com/{name}/tree/{commit}",
                "reported_at": items[0]["published"],
                "holders": WATCHED_HOLDERS[name],
                "bead": _publication_bead(label),
                "claims": found,
                "note": (
                    "A publication in a watched repository that no issue reports, dated by "
                    "its commit, or by the later push that made it public; transcribed from "
                    f"the history scan ({HISTORY_PUBLICATIONS.relative_to(ROOT).as_posix()}) "
                    f"at each count {chosen.label} claims where it states a side strictly "
                    "below the start, at the least side the commit states there."
                    + held_sentence(walk, label)
                ),
            }
        )
    if couzo:
        reports_list.append(
            {
                "report": "#715",
                "issue": 715,
                "holders": "Francisco Couzo",
                "bead": "think-cyal",
                "claims": couzo,
                "note": (
                    f"Issue 715's re-certifications of the 4e4c8ce certificates below the "
                    f"12-place print at the counts {chosen.label} claims, strictly below the "
                    "start, at the exact sides its packet's filtered receipt states; each "
                    "restates the certificate it re-certifies, by the owner's answer of 23 "
                    "October 2026 (think-fwa9)." + held_sentence(walk, "#715")
                ),
            }
        )
    return {
        "format": "intake-ledger-sources-v1",
        "read_at_main": ISSUE_732_READ_AT_MAIN,
        "read_on": read_on,
        "rule": RULE,
        "lanes": [],
        "reports": reports_list + publications,
        "rulings": WALK_RULINGS[walk.name],
    }


def write_release_walk_sources(issue: int | str, read_on: str) -> int:
    """Write a release walk's ``sources.yaml`` (`release_walk_sources`); return how many
    reports it holds."""
    import yaml  # noqa: PLC0415

    document = release_walk_sources(issue, read_on)
    target = walk_of(release(issue)).directory / "sources.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(target) as temporary:
        temporary.write_text(
            yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=100),
            encoding="utf-8",
        )
    return len(document["reports"])


def declared_rows(chosen: Release) -> dict[str, Any]:
    """A release's rows as its walk records them (`declaration_problems`): at each count
    the walk records it and does not hold it, the certificate the history scan found at the
    publication's least side there, or, for an issue with no table of rows (#732), the
    certificate its source holds at the retained commit (`source_history`), with that side
    rounded up at 12 places."""
    walk = walk_of(chosen)
    commit = chosen.pin
    if chosen.issue is not None:
        found = {
            row["n"]: {"kind": "certificate", "path": row["certificate"], "side": row["side"]}
            for row in _read(chosen.path(SOURCE_HISTORY))["at_commit"]
        }
    else:
        found = {
            item["n"]: item
            for item in sorted(
                (
                    item
                    for item in _read(HISTORY_PUBLICATIONS)["publications"]
                    if item["commit"] == commit
                ),
                key=lambda item: (Fraction(item["side"]), item["path"]),
                reverse=True,
            )
        }
    rows = []
    for n, count in sorted(_walked(walk).items()):
        if walk.holds(chosen.label, n) is not None:
            continue
        if not any(
            step["report"] == chosen.label and step["verdict"] == RECORDED
            for step in count["steps"]
        ):
            continue
        item = found[n]
        _require(item["kind"] == "certificate", f"{chosen.label} n={n}: no certificate file")
        rows.append(
            {"n": n, "certificate": item["path"], "printed": ceiling(Fraction(item["side"]))}
        )
    declared: dict[str, Any] = {
        "format": WATCHED_FORMAT,
        "publication": chosen.issue_url,
        "commit": chosen.pin,
        "committed": chosen.committed,
    }
    if chosen.issue is None:
        declared["published"] = chosen.reported
    return declared | {"walk": chosen.walk, "rows": rows}


def declare_rows() -> dict[str, int]:
    """Write each release's declared rows (`declared_rows`); return their counts."""
    written: dict[str, int] = {}
    for chosen in RELEASES.values():
        if declares_rows(chosen):
            document = declared_rows(chosen)
            path = chosen.directory / chosen.declared
            path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
            written[chosen.label] = len(document["rows"])
    return written


# --------------------------------------------------------------------------- coverage plan


def walk_of(chosen: Release) -> Walk:
    """The ledger walk that plans a release's rows."""
    return WALKS[chosen.walk]


def _releases(walk: Walk) -> dict[str, Release]:
    """The releases a walk plans, by the report label the ledger gives each."""
    return {item.label: item for item in RELEASES.values() if item.walk == walk.name}


def _awaits(walk: Walk, report: str, n: int) -> bool:
    """Whether a report the walk records at ``n`` has no row: its import is pending
    (`Awaiting`), or its publication there waits on an owner decision (`Held`)."""
    awaiting = walk.awaiting.get(report)
    pending = awaiting is not None and (awaiting.counts is None or n in awaiting.counts)
    return pending or walk.holds(report, n) is not None


def _source_of(walk: Walk, report: str) -> str:
    """The coverage source whose rows record a report the walk records."""
    ours = {label: item.source for label, item in _releases(walk).items()}
    source = ours.get(report) or walk.later.get(report)
    _require(source is not None, f"{report}: the ledger walks a report no source records")
    assert source is not None
    return source


def _counts(walk: Walk) -> list[dict[str, Any]]:
    ledger = walk.ledger
    return _ledger_counts(str(ledger), ledger.stat().st_mtime_ns)


def _walked(walk: Walk) -> dict[int, dict[str, Any]]:
    """A walk's counts by ``n``."""
    ledger = walk.ledger
    return _ledger_index(str(ledger), ledger.stat().st_mtime_ns)


@functools.cache
def _ledger_index(path: str, modified: int) -> dict[int, dict[str, Any]]:
    return {count["n"]: count for count in _ledger_counts(path, modified)}


@functools.cache
def _ledger_counts(path: str, _modified: int) -> list[dict[str, Any]]:
    """A ledger's counts, read once while the file is unchanged: the checks read each walk
    many times, and a walk may reach every count to 1024."""
    return _read(Path(path))["counts"]


def recorded_reports(walk: Walk, count: Mapping[str, Any]) -> list[str]:
    """The reports the walk records at a count that hold a row, in report order: a report
    whose own import is pending (`Awaiting`) is passed over."""
    return [
        step["report"]
        for step in count["steps"]
        if step["verdict"] == RECORDED and not _awaits(walk, step["report"], count["n"])
    ]


def planned_rows() -> list[dict[str, Any]]:
    """Each decided row as a dated beyond-horizon row, in report order at its count.

    Each release's walk takes every report at each count from the start frozen at its
    ledger's ``main``; a release's row the walk records is superseded by the next report
    the walk records there with a row, or is the count's current row. A row the walk does
    not record (equal to or above an earlier report) plans no row. A row the walk leaves
    undecided, or a count it does not walk, is refused: it is a records decision this plan
    does not make.
    """
    rows: list[dict[str, Any]] = []
    for chosen in RELEASES.values():
        walk = walk_of(chosen)
        walked = {count["n"]: count for count in _counts(walk)}
        printed = {
            row["n"]: row["offered_side"] for row in _read(chosen.path(RECORD))["results"]
        }
        for row in decided_claims(chosen):
            _require(row.n in walked, f"{chosen.label} n={row.n}: the ledger does not walk it")
            steps = walked[row.n]["steps"]
            (mine,) = [i for i, step in enumerate(steps) if step["report"] == chosen.label]
            if steps[mine]["verdict"] == NOT_RECORDED:
                continue
            _require(
                steps[mine]["verdict"] == RECORDED,
                f"{chosen.label} n={row.n}: the ledger does not record it",
            )
            later = [
                step["report"]
                for step in steps[mine + 1 :]
                if step["verdict"] == RECORDED and not _awaits(walk, step["report"], row.n)
            ]
            planned: dict[str, Any] = {
                "n": row.n,
                "source_id": chosen.source,
                "claim": "upper-bound",
                "value": printed[row.n],
                "assurance": "reported",
                "disposition": "superseded" if later else "tracked-outside-case-corpus",
            }
            if later:
                planned["superseded_by"] = _source_of(walk, later[0])
            planned["bead"] = chosen.bead
            rows.append(planned)
    return rows


def unrecorded_rows() -> list[tuple[int, str]]:
    """The decided rows each walk does not record, ``(n, source)``: no row may hold them."""
    found: list[tuple[int, str]] = []
    for chosen in RELEASES.values():
        walked = {count["n"]: count for count in _counts(walk_of(chosen))}
        for row in decided_claims(chosen):
            steps = walked.get(row.n, {"steps": []})["steps"]
            if any(
                step["report"] == chosen.label and step["verdict"] == NOT_RECORDED
                for step in steps
            ):
                found.append((row.n, chosen.source))
    return found


def _start_source(count: Mapping[str, Any]) -> str | None:
    """The source of a walked count's start, where the start is a beyond-horizon row (a
    count the grid or a register entry held has none)."""
    (start,) = count["start"]
    match = _START_ROW.fullmatch(start["label"])
    return None if match is None else match[1]


def planned_supersessions() -> list[tuple[int, str, str]]:
    """Where a release's row is the first report a walk records at its count with a row,
    the start it supersedes: ``(n, the start's source, the release's source)``.

    The start is the count's beyond-horizon row frozen in the ledger's starts. The release's
    row may itself be superseded by a later report; the start still names the release, the
    first report to beat it in report order, so each count is one chain. A report the walk
    records before it whose import is pending has no row to name (`Awaiting`).
    """
    return sorted({(n, start, source) for _, n, start, source in _planned_supersessions()})


def _planned_supersessions() -> list[tuple[Walk, int, str, str]]:
    """`planned_supersessions` with the walk that plans each."""
    flips: list[tuple[Walk, int, str, str]] = []
    for walk in WALKS.values():
        ours = {label: item.source for label, item in _releases(walk).items()}
        for count in _counts(walk):
            recorded = recorded_reports(walk, count)
            start = _start_source(count)
            if start is not None and recorded and recorded[0] in ours:
                flips.append((walk, count["n"], start, ours[recorded[0]]))
    return flips


def held_problems(register: Mapping[str, Any]) -> list[str]:
    """Where a walk's declared holds (`Held`) do not hold: each names a known class and a
    bead, holds each count once, and holds only a publication the walk records there, which
    no register row and no declared row of the report may then hold."""
    rows = {(row["n"], row["source_id"]) for row in register["beyond_horizon_claims"]}
    problems: list[str] = []
    for walk in WALKS.values():
        walked = _walked(walk)
        releases = _releases(walk)
        for report, items in walk.held.items():
            source = releases[report].source if report in releases else walk.later.get(report)
            declared = (
                {row.n for row in decided_claims(releases[report])}
                if report in releases
                else set()
            )
            seen: set[int] = set()
            for item in items:
                where = f"{walk.name}: {report}"
                if item.kind not in HELD_CLASSES:
                    problems.append(f"{where}: no such class of hold, {item.kind!r}")
                problems.extend(
                    f"{where}: {bead!r} is not a decision's bead"
                    for bead in (item.bead, *item.also)
                    if not _BEAD.fullmatch(bead)
                )
                if seen & item.counts:
                    problems.append(f"{where}: holds n={sorted(seen & item.counts)} twice")
                seen |= item.counts
                for n in sorted(item.counts):
                    steps = walked.get(n, {"steps": []})["steps"]
                    if not any(
                        step["report"] == report and step["verdict"] == RECORDED
                        for step in steps
                    ):
                        problems.append(
                            f"{where} n={n}: the walk does not record it, so it holds nothing"
                        )
                    if source is not None and (n, source) in rows:
                        problems.append(
                            f"{where} n={n}: held for {item.bead}, yet {source} has a row there"
                        )
                    if n in declared:
                        problems.append(f"{where} n={n}: held and declared as a row")
    return problems


def held_plan() -> list[dict[str, Any]]:
    """Every publication a walk holds back from a row, with its class and decision's bead."""
    return [
        {
            "walk": walk.name,
            "report": report,
            "n": n,
            "class": item.kind,
            "bead": item.bead,
        }
        | ({"also": list(item.also)} if item.also else {})
        | ({"settled": True} if item.answer else {})
        for walk in WALKS.values()
        for report, items in walk.held.items()
        for item in items
        for n in sorted(item.counts)
    ]


def resting_on_holds(walk: Walk) -> tuple[Resting, ...]:
    """The verdicts ``walk`` decided only against publications it holds for a decision still
    owed, from its ledger: a step not recorded, or undecided, every report of whose
    ``decided_against`` the walk holds at that count with no answer settling it
    (`Held.answer`), grouped by report, verdict and the holds' classes."""
    groups: dict[tuple[str, str, tuple[str, ...]], set[int]] = {}
    for count in _counts(walk):
        n = count["n"]
        for step in count["steps"]:
            against = step.get("decided_against") or []
            if step["verdict"] == RECORDED or not against:
                continue
            holds = [walk.holds(report, n) for report in against]
            if all(item is not None and not item.answer for item in holds):
                kinds = tuple(sorted({item.kind for item in holds if item is not None}))
                groups.setdefault((step["report"], step["verdict"], kinds), set()).add(n)
    return tuple(
        Resting(report, verdict, kinds, frozenset(counts))
        for (report, verdict, kinds), counts in sorted(groups.items())
    )


def resting_problems() -> list[str]:
    """Where a walk's declared `Resting` verdicts are not the ones its ledger rests on its
    holds (`resting_on_holds`): each is named, so an answer that leaves a hold out names
    every verdict it reopens."""
    problems: list[str] = []
    for walk in WALKS.values():

        def key(item: Resting) -> tuple[str, str, tuple[str, ...]]:
            return (item.report, item.verdict, item.kinds)

        declared = {key(item): item.counts for item in walk.resting}
        found = {key(item): item.counts for item in resting_on_holds(walk)}
        for group in sorted(declared.keys() | found.keys()):
            have, want = declared.get(group, frozenset()), found.get(group, frozenset())
            where = f"{walk.name}: {group[0]} {group[1]} on {'/'.join(group[2])} holds"
            if want - have:
                problems.append(f"{where}: rests at n={sorted(want - have)}, undeclared")
            if have - want:
                problems.append(
                    f"{where}: declared at n={sorted(have - want)}, not in the ledger"
                )
    return problems


#: What a step a rerun walk records would be (`refusal_flips`): a record, which needs a row.
NEW_RECORD = "record"


def refusal_flips(walk: Walk, kinds: Iterable[str]) -> list[tuple[int, str, str]]:
    """The steps ``walk`` would record if the owner left its holds of ``kinds`` out of the
    record, each with what it would then be. A hold an answer has settled stays.

    The walk is run again by `devtools.intake_ledger`'s rule from its frozen starts without
    those publications, under the ledger's own exceptions and rulings, and each step that
    was not recorded and now is is named: a new record (`NEW_RECORD`). The rulings decide
    in the rerun as in the walk, so a side above Göbel's construction or a restatement of
    the report it beats is not recorded there either.
    """
    from devtools import intake_ledger  # noqa: PLC0415

    refused = set(kinds)
    ledger = intake_ledger.load_ledger(walk.directory)
    starts = intake_ledger.load_starts(walk.directory, ledger["read_at_main"])
    exceptions = {(item["n"], item["report"]): item["reason"] for item in ledger["exceptions"]}
    rulings = intake_ledger.rulings_of(ledger)
    entries: dict[int, list[Any]] = {}
    for report in ledger["reports"]:
        for claim in report["claims"]:
            held = walk.holds(report["report"], claim["n"])
            if held is None or held.kind not in refused or held.answer:
                entries.setdefault(claim["n"], []).append(
                    intake_ledger.entry_side(report, claim)
                )
    before = {
        (count["n"], step["report"]): step["verdict"]
        for count in _counts(walk)
        for step in count["steps"]
    }
    flips: list[tuple[int, str, str]] = []
    for n, sides in sorted(entries.items()):
        for step in intake_ledger.walk(n, starts[n], sides, exceptions, rulings).steps:
            if step.verdict != RECORDED or before.get((n, step.side.label)) == RECORDED:
                continue
            flips.append((n, step.side.label, NEW_RECORD))
    return flips


def held_dependents() -> dict[str, Any]:
    """For each walk, the verdicts resting on its holds; for each class of hold an answer
    might leave out, the steps a rerun walk would then record, by what each would be
    (`refusal_flips`); and the holds an answer has settled (`Held.answer`)."""
    return {
        walk.name: {
            "settled": [
                {
                    "report": report,
                    "class": item.kind,
                    "counts": sorted(item.counts),
                    "answer": item.answer,
                }
                for report, items in walk.held.items()
                for item in items
                if item.answer
            ],
            "resting": [
                {
                    "report": item.report,
                    "verdict": item.verdict,
                    "kinds": list(item.kinds),
                    "counts": sorted(item.counts),
                }
                for item in walk.resting
            ],
            "recorded_if_left_out": {
                kind: {
                    falls: [f"{report} n={n}" for n, report, how in flips if how == falls]
                    for falls in sorted({how for _, _, how in flips})
                }
                for kind in sorted(
                    {
                        item.kind
                        for items in walk.held.values()
                        for item in items
                        if not item.answer
                    }
                )
                for flips in [refusal_flips(walk, (kind,))]
            },
        }
        for walk in WALKS.values()
        if walk.held
    }


def declaration_problems() -> list[str]:
    """Where a release that declares its rows (`declares_rows`) declares other rows than its
    walk makes: every claim the walk records of it, and does not hold, is a declared row, and
    no other."""
    problems: list[str] = []
    for chosen in RELEASES.values():
        if not declares_rows(chosen):
            continue
        walk = walk_of(chosen)
        recorded = {
            n
            for n, count in _walked(walk).items()
            for step in count["steps"]
            if step["report"] == chosen.label
            and step["verdict"] == RECORDED
            and walk.holds(chosen.label, n) is None
        }
        declared = {row.n for row in decided_claims(chosen)}
        problems.extend(
            f"{chosen.label} n={n}: the walk records it, and the packet declares no row"
            for n in sorted(recorded - declared)
        )
        problems.extend(
            f"{chosen.label} n={n}: declared as a row the walk does not record"
            for n in sorted(declared - recorded)
        )
    return problems


def chain_problems(coverage: Mapping[str, Any]) -> list[str]:
    """Where a count a walk reaches beyond the corpus is not one chain in report order.

    The chain is the count's start, where it is a beyond-horizon row, then the row of each
    report the walk records, in report order, passing over a report whose import is pending
    (`Awaiting`). Each must be in the register and superseded by the next; the last is
    current, or superseded by a report the walk does not reach. Counts above ``LIMIT``
    have no rows yet (the owner's D1) and are not held. Where two walks reach a count, a
    later walk may insert between two of an earlier walk's reports a report the earlier
    walk does not reach, as the history walk inserts Couzo's 4e4c8ce between a start and
    #670; the register may then lead from one to the other through it (`bridged`), and
    the later walk holds that stretch to its own chain. A problem two walks find is named
    once.
    """
    rows = {(row["n"], row["source_id"]): row for row in coverage["beyond_horizon_claims"]}
    problems: list[str] = []
    for walk in WALKS.values():
        for count in _counts(walk):
            n = count["n"]
            if not reports.HORIZON < n <= LIMIT:
                continue
            start = _start_source(count)
            chain = ([start] if start is not None else []) + [
                _source_of(walk, report) for report in recorded_reports(walk, count)
            ]
            # At 366 the grid stands and only publications awaiting their imports are
            # recorded, so the chain is empty until one lands.
            for earlier, later in zip(chain, [*chain[1:], None][: len(chain)], strict=True):
                held = rows.get((n, earlier))
                if held is None:
                    problems.append(f"n={n}: the register has no row from {earlier}")
                    continue
                disposition, successor = held.get("disposition"), held.get("superseded_by")
                if (
                    later is not None
                    and (disposition, successor) != ("superseded", later)
                    and not bridged(rows, n, earlier, later, walk)
                ):
                    problems.append(
                        f"n={n} from {earlier}: {disposition} naming {successor}, "
                        f"not superseded by {later}"
                    )
                elif later is None and successor in chain:
                    problems.append(
                        f"n={n} from {earlier}: names {successor}, earlier in the chain"
                    )
    return list(dict.fromkeys(problems))


def _reached(walk: Walk, n: int) -> set[str]:
    """Every source a walk reaches at ``n``: its start's and each walked report's."""
    count = _walked(walk).get(n)
    if count is None:
        return set()
    reached = {_start_source(count)}
    for step in count["steps"]:
        report = step["report"]
        source = {label: item.source for label, item in _releases(walk).items()}.get(report)
        reached.add(source or walk.later.get(report))
    return {source for source in reached if source is not None}


def bridged(
    rows: Mapping[tuple[int, str], Mapping[str, Any]],
    n: int,
    earlier: str,
    later: str,
    walk: Walk,
) -> bool:
    """Whether the register leads from ``earlier`` to ``later`` at ``n`` through one or more
    rows of sources ``walk`` does not reach there, each of which another walk reaches at
    ``n``, so that walk orders it in its own chain (`chain_problems`)."""
    mine = _reached(walk, n)
    others: set[str] = set()
    for other in WALKS.values():
        if other is not walk:
            others |= _reached(other, n)
    current, seen = earlier, {earlier}
    while True:
        held = rows.get((n, current)) or {}
        successor = held.get("superseded_by")
        if held.get("disposition") != "superseded" or successor is None:
            return False
        if successor == later:
            return current != earlier
        if successor in mine or successor not in others or successor in seen:
            return False
        seen.add(successor)
        current = successor


def _superseded_after(
    plan: Mapping[str, Any], held: Mapping[str, Any], walk: Walk, register: Mapping[str, Any]
) -> bool:
    """Whether a row the plan calls current is held superseded by a report its walk does
    not reach: a later import's row, as `chain_problems` allows (#720's review B, B1). The
    held row must be the plan's but for its disposition and successor, and the successor
    must hold a row at the count of the same claim strictly below it, from a source dated
    no earlier than the row's own, so the plan does not rest on `check_source_coverage`
    (#722's review A, A5, and review B, B3). A successor dated the same day is not ordered
    by the day, as that gate does not. A source the walk reaches is never the successor,
    whatever its row: the walk already ordered it."""
    if "superseded_by" in plan or held.get("disposition") != "superseded":
        return False
    successor = held.get("superseded_by")
    if (
        successor is None
        or successor in _reached(walk, plan["n"])
        or {**plan, "disposition": "superseded", "superseded_by": successor} != dict(held)
    ):
        return False
    dated = {str(item["id"]): str(item.get("source_date", "")) for item in register["sources"]}
    later = [
        row
        for row in register["beyond_horizon_claims"]
        if row["n"] == plan["n"]
        and row["source_id"] == successor
        and row["claim"] == plan["claim"]
    ]
    own = dated.get(str(plan["source_id"]), "")
    return (
        len(later) == 1
        and bool(own)
        and dated.get(str(successor), "") >= own
        and Fraction(str(later[0]["value"])) < Fraction(str(plan["value"]))
    )


def construction_problems(register: Mapping[str, Any]) -> list[str]:
    """Where a register row beyond the corpus to ``LIMIT`` is not marked as the owner's
    answer of 23 October 2026 on #613 requires (think-8krd): a row at or above Göbel's
    construction at its count, as `devtools.intake_ledger.goebel_form` reads the retained
    program, is marked ``above-classical-construction`` with that construction, and a row
    so marked is above it. A row is read at its exact side where its source's claims
    record states one, else as low as its print allows."""
    from devtools import check_source_coverage as coverage_check  # noqa: PLC0415
    from devtools import intake_ledger  # noqa: PLC0415

    sources = {str(source["id"]): source for source in register["sources"]}
    problems: list[str] = []
    for row in register["beyond_horizon_claims"]:
        n, value = int(row["n"]), str(row["value"])
        if not reports.HORIZON < n <= LIMIT:
            continue
        where = f"n={n} from {row['source_id']}"
        marked = row.get("disposition") == coverage_check.ABOVE_CONSTRUCTION
        form = intake_ledger.goebel_form(n)
        exact = _stated_side(sources[str(row["source_id"])], n)
        low = exact if exact is not None else Fraction(value) - intake_ledger.unit(value)
        above = coverage_check.construction_sign(low, form.text()) == 1
        below = coverage_check.construction_sign(exact or Fraction(value), form.text()) == -1
        if not (above or below):
            problems.append(f"{where}: its print does not decide it against {form.text()}")
        elif above and not marked:
            problems.append(
                f"{where}: above Göbel's construction {form.text()}, and not marked "
                f"{coverage_check.ABOVE_CONSTRUCTION}"
            )
        elif marked and not above:
            problems.append(f"{where}: marked, and not above Göbel's {form.text()}")
        elif marked and row.get("construction") != form.text():
            problems.append(
                f"{where}: names {row.get('construction')!r}, not Göbel's {form.text()}"
            )
    return problems


def coverage_problems(coverage: Mapping[str, Any] | None = None) -> list[str]:
    """Where the coverage register differs from the plan: each planned row, as written, or
    superseded by a report its walk does not reach where the plan calls it current; no row
    for a decided row its walk does not record; each start a release's row beat first naming
    the release's source as its successor; each walked count one chain in report order; and
    each row above Göbel's construction marked so (`construction_problems`).
    ``coverage`` is the register as `safe_load` reads it, by default the checkout's."""
    register: Mapping[str, Any] = (
        safe_load(COVERAGE.read_text(encoding="utf-8")) if coverage is None else coverage
    )
    rows = {(row["n"], row["source_id"]): row for row in register["beyond_horizon_claims"]}
    walks = {item.source: walk_of(item) for item in RELEASES.values()}
    problems = []
    for row in planned_rows():
        held = rows.get((row["n"], row["source_id"]))
        if held != row and not (
            held is not None and _superseded_after(row, held, walks[row["source_id"]], register)
        ):
            problems.append(
                f"n={row['n']} from {row['source_id']}: the register's row is not the plan's"
            )
    problems.extend(
        f"n={n} from {source}: the ledger does not record it, so no row may hold it"
        for n, source in unrecorded_rows()
        if (n, source) in rows
    )
    for walk, n, earlier, successor in _planned_supersessions():
        held = rows.get((n, earlier)) or {}
        if (held.get("disposition"), held.get("superseded_by")) != (
            "superseded",
            successor,
        ) and not bridged(rows, n, earlier, successor, walk):
            problems.append(f"n={n} from {earlier}: not superseded by {successor}")
    return (
        problems
        + held_problems(register)
        + resting_problems()
        + declaration_problems()
        + chain_problems(register)
        + construction_problems(register)
    )


# --------------------------------------------------------------------------- check


def _stable(row: Mapping[str, Any]) -> dict[str, Any]:
    """A row without its timings."""
    copy = json.loads(json.dumps(row))
    copy.pop("wall_seconds", None)
    copy["decision"].pop("cpu_seconds", None)
    return copy


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def row_problems(chosen: Release, row: Claim, kept: Mapping[str, Any]) -> list[str]:
    """Where one receipt row fails its issue row or its controls."""
    where = f"{chosen.label} n={row.n}"
    problems: list[str] = []
    if (kept["certificate"], kept["printed"], kept["deleted_squares"]) != (
        row.path,
        row.printed,
        row.deleted,
    ):
        problems.append(f"{where}: receipt row differs from the issue")
    if not kept["verified"]:
        problems.append(f"{where}: not verified")
    controls = kept.get("controls", [])
    if [control["control"] for control in controls] != (
        [] if row.deleted else list(base.CONTROLS)
    ):
        problems.append(f"{where}: the controls are not the declared six")
    problems.extend(
        f"{where}: {control['control']} was accepted"
        for control in controls
        if not (control["refused_by_sqpack"] and control["refused_by_independent"])
    )
    return problems


def deletion_problems(chosen: Release, rows: Sequence[Claim]) -> list[str]:
    """A deletion row whose certificate no row of the release reads whole: its controls are
    decided on that row (`decide_row`), so without it the certificate would have none."""
    whole = {row.n: row.path for row in rows if not row.deleted}
    return [
        f"{chosen.label} n={row.n}: deletes from n{row.certificate_n}, which no row of the "
        "release reads whole, so no control decides its certificate"
        for row in rows
        if row.deleted and whole.get(row.certificate_n) != row.path
    ]


def sample_problems(
    chosen: Release, rows: Sequence[Claim], sample: Sequence[Mapping[str, Any]]
) -> list[str]:
    """Where the all-pairs sample is not the declared counts, or disagrees with the
    filtered decision at one of them."""
    problems: list[str] = []
    if [item["n"] for item in sample] != list(chosen.sampled):
        problems.append(
            f"{chosen.label}: the all-pairs sample decides "
            f"{[item['n'] for item in sample]}, not the declared {list(chosen.sampled)}"
        )
    decided = {row.n for row in rows}
    problems.extend(
        f"{chosen.label} n={item['n']}: the all-pairs sample disagrees with the filtered one"
        for item in sample
        if item["n"] not in decided
        or not all(
            item[key]
            for key in (
                "exact_verify_passed",
                "independent_passed",
                "routes_agree_on_least_gap",
                "equals_filtered_least_gap",
                "equals_filtered_least_wall",
            )
        )
    )
    return problems


def release_problems(chosen: Release, *, replay: bool, workers: int) -> list[str]:
    """Problems with one packet's receipts and record; empty when they hold."""
    custody(chosen)
    rows = decided_claims(chosen)
    receipt = _read(chosen.path(FILTERED))
    stored = receipt["rows"]
    if [row["n"] for row in stored] != [row.n for row in rows]:
        return [f"{chosen.label}: the filtered receipt's rows are not the issue's"]
    problems = deletion_problems(chosen, rows)
    sides = decided_sides(chosen)
    for row, kept in zip(rows, stored, strict=True):
        problems.extend(row_problems(chosen, row, kept))
        if Fraction(kept["exact_side"]) != sides[row.n]:
            problems.append(f"{chosen.label} n={row.n}: the receipt's side is not the header's")
    if receipt["summary"] != base.summary(stored):
        problems.append(f"{chosen.label}: the summary does not match the rows")
    if replay:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            again = list(pool.map(decide_row, [(chosen.label, row.n) for row in rows]))
        problems.extend(
            f"{chosen.label} n={row.n}: the replay differs from the receipt"
            for row, kept, fresh in zip(rows, stored, again, strict=True)
            if _stable(fresh) != _stable(kept)
        )
    record = chosen.path(RECORD)
    if not record.is_file() or _read(record) != beyond_horizon_rows(chosen):
        problems.append(f"{chosen.label}: the beyond-horizon record differs from its rebuild")
    return problems + _cross_check_problems(chosen, rows)


def _cross_check_problems(chosen: Release, rows: Sequence[Claim]) -> list[str]:
    """The first commits', the all-pairs sample's and the Göbel receipt's outcomes.

    A retained certificate's Git blob is rebuilt from its bytes; a derived packet keeps
    none, so its receipt's SHA-256 must be the one the packet pins. Every side the walk
    records must be below Göbel's construction; a side it does not record, as #719's 366,
    is held to the receipt as compared.
    """
    problems: list[str] = []
    commits = _read(chosen.path(FIRST_COMMITS))
    held = [*rows, *held_claims(chosen)]
    if chosen.derived:
        pinned = manifest(chosen)
        expected = [(row.n, row.path, pinned[row.path]) for row in held]
        found = [(item["n"], item["certificate"], item["sha256"]) for item in commits["rows"]]
    else:
        expected = [
            (row.n, row.path, git_blob(read_retained_bytes(archive(chosen) / row.path)))
            for row in held
        ]
        found = [(item["n"], item["certificate"], item["blob"]) for item in commits["rows"]]
    if found != expected:
        problems.append(f"{chosen.label}: the first commits are not the retained certificates'")
    problems.extend(
        f"{chosen.label} n={item['n']}: first committed at {item['first_commit'][:8]}, "
        f"not {chosen.first_commit_of(item['n'])[0][:8]} as the record states"
        for item in commits["rows"]
        if (item["first_commit"], item["committed"]) != chosen.first_commit_of(item["n"])
    )
    sample = chosen.path(EXHAUSTIVE)
    if chosen.sampled or sample.is_file():
        problems.extend(sample_problems(chosen, rows, _read(sample)["rows"]))
    comparison = _read(chosen.path(GOEBEL))["comparison"]
    compared = [
        (item["n"], Fraction(item["side"]), item["relation"]) for item in comparison["detail"]
    ]
    unrecorded = {n for n, source in unrecorded_rows() if source == chosen.source}
    decided = decided_sides(chosen)
    sides = [(row.n, decided[row.n]) for row in rows]
    if [(n, side) for n, side, _ in compared] != sides or any(
        relation != "below" for n, _, relation in compared if n not in unrecorded
    ):
        problems.append(f"{chosen.label}: a decided side is not below Göbel's construction")
    return problems


def check(*, replay: bool, workers: int = 1, issues: Sequence[int | str] = ()) -> list[str]:
    """Problems with every chosen packet's receipts and record; empty when they hold.

    With ``replay`` every decided row and its controls are decided again, on ``workers``
    processes, and each must equal its receipt row apart from timings.
    """
    chosen = [release(issue) for issue in issues] if issues else list(RELEASES.values())
    return [
        problem
        for item in chosen
        for problem in release_problems(item, replay=replay, workers=workers)
    ] + coverage_problems()


def _clone(text: str) -> tuple[str, Path]:
    name, _, path = text.partition("=")
    _require(bool(path) and name in WATCHED_HOLDERS, f"{text}: give owner/name=PATH")
    return name, Path(path)


#: How a command names a release: an issue's number, or a publication's ledger label.
KEY_HELP = "an issue's number, or a publication's label owner/name@commit"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n", 1)[0])
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("filtered")
    run.add_argument("--issue", nargs="+", default=list(RELEASES), help=KEY_HELP)
    run.add_argument("--workers", type=int, default=2)
    history = commands.add_parser("first-commits")
    history.add_argument("--issue", required=True, help=KEY_HELP)
    history.add_argument("--clone", type=Path, required=True)
    sample = commands.add_parser("exhaustive")
    sample.add_argument("--issue", required=True, help=KEY_HELP)
    sample.add_argument("--n", type=int, nargs="+", required=True)
    sample.add_argument("--workers", type=int, default=2)
    commands.add_parser("goebel")
    commands.add_parser("claims-record")
    scan = commands.add_parser("earlier")
    scan.add_argument("--issue", required=True, help=KEY_HELP)
    scan.add_argument("--couzo", type=Path, required=True, help="franciscouzo/square-packing")
    scan.add_argument("--evand", type=Path, required=True, help="evand/square-packing")
    scan.add_argument("--source", type=Path, help="the release's own repository")
    transcribe = commands.add_parser("ledger-sources")
    transcribe.add_argument("--issue", required=True, help=KEY_HELP)
    transcribe.add_argument("--read-at-main", required=True)
    transcribe.add_argument("--read-on", required=True)
    scan_history = commands.add_parser("history-publications")
    scan_history.add_argument(
        "--clone",
        nargs="+",
        required=True,
        help="owner/name=PATH, a clone of each watched repository",
    )
    scan_history.add_argument(
        "--start-coverage",
        type=Path,
        required=True,
        help="frontier/source-coverage.yaml of a checkout of HISTORY_READ_AT_MAIN",
    )
    transcribe_history = commands.add_parser("history-sources")
    transcribe_history.add_argument("--read-on", required=True)
    own_history = commands.add_parser("source-history")
    own_history.add_argument("--issue", required=True, help=KEY_HELP)
    own_history.add_argument("--clone", type=Path, required=True)
    transcribe_release = commands.add_parser("release-sources")
    transcribe_release.add_argument("--issue", required=True, help=KEY_HELP)
    transcribe_release.add_argument("--read-on", required=True)
    commands.add_parser("declare-rows")
    commands.add_parser("coverage-plan")
    commands.add_parser("held-dependents")
    audit = commands.add_parser("check")
    audit.add_argument("--issue", nargs="+", default=[], help=KEY_HELP)
    audit.add_argument("--replay", action="store_true")
    audit.add_argument("--workers", type=int, default=1)
    args = parser.parse_args(argv)
    actions: dict[str, Callable[[], Any]] = {
        "filtered": lambda: {
            issue: receipt["summary"]
            for issue, receipt in filtered(args.issue, args.workers).items()
        },
        "first-commits": lambda: len(first_commits(args.issue, args.clone)["rows"]),
        "exhaustive": lambda: exhaustive(args.issue, args.n, args.workers)["rows"],
        "goebel": goebel,
        "claims-record": claims_record,
        "earlier": lambda: write_earlier(
            args.issue,
            {"franciscouzo/square-packing": args.couzo, "evand/square-packing": args.evand},
            args.source,
        ),
        "ledger-sources": lambda: write_ledger_sources(
            args.issue, args.read_at_main, args.read_on
        ),
        "history-publications": lambda: write_history_publications(
            dict(_clone(item) for item in args.clone), args.start_coverage
        ),
        "history-sources": lambda: write_history_sources(args.read_on),
        "source-history": lambda: write_source_history(args.issue, args.clone),
        "release-sources": lambda: write_release_walk_sources(args.issue, args.read_on),
        "declare-rows": declare_rows,
        "coverage-plan": lambda: {
            "rows": planned_rows(),
            "supersessions": planned_supersessions(),
            "held": held_plan(),
        },
        "held-dependents": held_dependents,
    }
    if args.command == "check":
        problems = check(replay=args.replay, workers=args.workers, issues=args.issue)
        for problem in problems:
            print(problem)
        chosen = [release(issue) for issue in args.issue] or list(RELEASES.values())
        decided = sum(item.decided for item in chosen)
        named = ", ".join(item.label for item in chosen)
        print(
            "FAILED"
            if problems
            else f"OK: {decided} rows of {named} verified, controls refused; "
            "the coverage plan and report order hold"
        )
        return 1 if problems else 0
    print(json.dumps(actions[args.command](), indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
