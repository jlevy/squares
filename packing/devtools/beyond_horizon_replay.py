"""Decide the beyond-horizon rows of a report exactly, from its retained packet.

A report beyond the ``n <= 324`` corpus is recorded as dated beyond-horizon rows of its
source, at assurance ``reported``, once its certificates are retained and replayed here.
Issues #678 and #715 each had a module of their own (`devtools.couzo_678_replay`,
`devtools.couzo_715_replay`); this one takes the same filtered decision and declares each
report it decides as a `Release`, so a further report of the same kind is a declaration and
not a module. `RELEASES` holds 30, each decided within a window of counts
(`Release.decided_above`, `Release.decided_through`), every one of them today from the
corpus to ``FROZEN_THROUGH = 1024``: the seven issues below, #732's later release, the
publication #763's index makes beside it, the sides the same push published at the
notebook rows' counts (nine releases, one a holder at a commit), Couzo's later 43f666c,
and 11 publications in watched repositories that no issue reports (**Publications no
issue reports**, `WATCHED`):

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
- **#732's comment of 23 October**, the release ``#732 comment 6374211504``: the 138
  certificates ``f1ceee4c`` rewrites at 328 to 989, held to ``certified_bounds.json``, the
  index it keeps current, and all retained, since its walk records every one (**f1ceee4**).
- **#763**, Francisco Couzo: certificates ``certificates/best/nN.cert`` at ``964ee2bd``,
  whose issue has no table, so its claims are re-derived from the source's indexes
  (`CLAIM_MAP`, `Release.claim_map`); its 184 rows are those its walk records, and the 10
  rows of the index that the issue's selection rule leaves out are the publication
  ``franciscouzo/square-packing@964ee2b`` (**Issue #763**).
- **The push of 23:38:42Z** at the counts of the 99 sides 964ee2b's index credits to the
  authors of seven Kaggle notebooks, which no issue reports: the 185 sides its walk records
  from the push's three commits, ``efef7d1``, ``fa6237e`` and ``964ee2b``, read commit by
  commit, each certificate ``certificates/best/nN.cert`` or the copy 964ee2b keeps under
  ``certificates/parents/`` or the root, the 12 notebook recipes' own included; a release
  is a holder at a commit, a notebook run or Couzo's own, each a coverage source (**The push
  of 23:38:42Z**).

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
the corpus, each walk to its own reach (`Walk.reaches`), to one chain in report order
(`chain_problems`): the start, then
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

**f1ceee4.** ``campaign/issue-intake/upper-bounds-issue732-f1ceee4-20261024`` walks the 138
counts the comment reports from starts frozen at ``main`` 0bbb0a2c4 (#754's merge) on 24
October, so each start holds Göbel's construction beside the row. The release is dated by
the comment (`Release.comment`), its claims are the certificates its commit changes
(``changed_only``), and the three commits after it are reports of their own from their
pushes (``later_reads``): ``later-commits`` reads each one's certificate files and index
bounds into ``receipts/later-commits.json``, and the walk takes, at those counts in the
corpus, the earlier reports the retained ledgers walked where the start alone does not order
a later claim (`ledger_reports`, `WALK_PENDING_REPORTS`). ``decide-later`` decides exactly,
against a case's algebraic side, each comparison of a later claim the prints leave
undecided (`decide_later`), and ``pose-identity`` measures the counts the author asks sole
credit at against what they supersede (`pose_identity`), deciding nothing.

**Issue #763.** ``campaign/issue-intake/upper-bounds-issue763-20261024`` walks the counts
to 1024 that #763 claims, and the index's unrequested rows there, from starts frozen at
``main`` e5c1c64e3 (#756's merge), the first ``main`` that holds f1ceee4's rows and T-239.
``release-sources`` transcribes its ``sources.yaml`` from the packet's claim map
(`claim_map_walk_sources`): the issue's claims dated by the issue, the unrequested rows by
the push of 23:38:42Z that made 964ee2b public (`PUSHED_LATER`), and every earlier
publication strictly below the start, from the history scan, Polkovskyi's repository
through f1ceee4 and the commits after it, #715's re-certifications and, in the corpus, the
retained ledgers. The walk holds the issue's deletion bound at 683 (`_HELD_763`) and the
history walk's holds it records (`_HELD_IN_763`). It held the issue's 13 L-border recipes
until a maintained construction checker existed; 43f666c's import decides each from its
recipe and its replayed parent (`RECIPES`, think-g2qy), so each is a declared row with its
recipe, dated by the first commit whose index states it (`recipe_first_commits`). A count
in the corpus is the register's: no declared row holds 268 or 303 (`declared_rows`).

**The push of 23:38:42Z.** The walk
``campaign/issue-intake/upper-bounds-couzo-964ee2b-notebooks-20261024`` reads the counts of
the 99 sides credited to the authors of Kaggle notebooks that the push published in
964ee2b's index (the claim map's ``others``, think-lyf9), from starts frozen at ``main``
2ec489d1e (#789's merge). Each certificate in a watched repository is a report from its
first commit, so the push is read commit by commit (#795's review A, A1):
``push-publications`` writes ``receipts/push/push-publications.json``, every side efef7d1,
fa6237e and 964ee2b first state at those counts and each commit's least one below the start,
held by a certificate 964ee2b keeps, a notebook recipe's included (A2). The walk has three
reports, all dated by the push and taken in commit order (`intake_ledger.walk`): efef7d1
(40), fa6237e (90) and 964ee2b (60). Each holder at each commit is a release with its own
coverage source, record and receipts (`PUSH_RELEASES`): the seven notebook runs and Couzo's
own sides at efef7d1 and fa6237e. The releases of one commit share its label
(`_walk_groups`, `release_at`). ``release-sources`` transcribes its ``sources.yaml`` from
that receipt, every earlier publication cut at the push, and ``push-identity`` measures the
rows at `PUSH_IDENTITY` against the push's earlier sides there
(``receipts/push/pose-identity.json``), which the walk records as refinements where the
packing is the same (`PUSH_SAME_PACKING`). The walk holds the history walk's holds it
records (`_HELD_IN_NOTEBOOKS`).

**43f666c.** Couzo's commit 43f666c, pushed with 73eac5b and 1c17153 at 06:10:44Z on 24
October, lowers 964ee2b's certified bounds at 957 counts; no issue reports it, so it is a
publication of its own, dated by that push (think-gn29). Its claims are re-derived from its
packet's indexes (`devtools.couzo_43f666c_claims`, ``lowered``). The walk
``campaign/issue-intake/upper-bounds-couzo-43f666c-20261024`` reads its counts to 1024 from
starts frozen at ``main`` 2ed0ea740 (#795's merge), and, besides the earlier publications
every claim-map walk reads, two reports that come between those starts and it
(`ClaimMapWalk`): #763's claims with no row among the starts, its recipes decided here and
its deletion bound and restatements (`earlier_issue_claims`), whose rows the walk takes
from #763's source (``later``); and the push of 23:38:42Z read commit by commit at the
walk's counts (``earlier-push``, ``receipts/earlier-push.json``), whose best/ certificates
and recipes at #763's recipe counts #795's review A noted. Each of those is above or equal
to #763's earlier claim, or restates a row, so the walk records none of them. It settles
43f666c's deletion at 690 by the D6 answer (`deletion_holds`) and holds the history walk's
holds it records (`_HELD_IN_43F`).

**Above 1024.** The owner tracks every count, with no ceiling (D1, think-f2io), and a
records slice lifts a release's window in the same pull request as the receipts it
needs (think-llit). Its rows above 1024 are planned by the walk above 1024 it names
(`Release.walk_above`, `walk_of`), which lists both rulings with no top. Göbel's
construction there comes from the maintained module (`devtools.goebel_construction`), so
a window above 1024 writes the v2 Göbel receipt (`goebel_receipt`). A recipe row is
decided by the construction checker (`devtools.construction_checker`, D2), not the
filtered replay: ``recipe-decisions`` replays the parents that are not rows and decides
each recipe (`RECIPES`). An index's one-square deletion from the next count is an earlier
report by D6, and any other deletion, or one an issue claims, waits on think-kzme
(`deletion_holds`); the Kingbird catalogue's sides wait on N1 (`CATALOGUE`). A certificate
the packet pins and does not retain is read from hosted shards (`Release.hosted`,
`devtools.hosted_shards`), and the fast check reads its side and blob from the source
history without opening one.

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
    python -m devtools.beyond_horizon_replay source-history --issue 732 --clone CLONE [--walk W]
    python -m devtools.beyond_horizon_replay release-sources --issue 732 --read-on DATE \
        [--walk W]
    python -m devtools.beyond_horizon_replay recipe-decisions --issue 715 [--workers 2]
    python -m devtools.beyond_horizon_replay later-commits --issue LABEL --clone CLONE
    python -m devtools.beyond_horizon_replay push-publications --issue LABEL --clone CLONE
    python -m devtools.beyond_horizon_replay earlier-push --issue LABEL --clone CLONE \
        [--read-on DATE]
    python -m devtools.beyond_horizon_replay push-identity --issue LABEL
    python -m devtools.beyond_horizon_replay decide-later --issue LABEL
    python -m devtools.beyond_horizon_replay pose-identity --issue LABEL
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
from collections import Counter
from collections.abc import Callable, Iterable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any, NamedTuple, cast

from strif import atomic_output_file

from devtools import acquire_source, goebel_construction, hosted_shards
from devtools import construction_checker as checker
from devtools import couzo_678_replay as base
from devtools import couzo_715_replay as couzo_715
from devtools import couzo_763_claims as claims_763
from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools import upper_bound_reports as reports
from devtools.retained_data import read_retained_bytes, read_retained_text, retained_exists
from sqpack.retained_json import dumps as retained_dumps
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
WEB = ROOT / "resources/web"
#: The reach of the walks and releases frozen at 1024: the five walks and 20 releases on
#: ``main`` before the work above 1024 (think-llit), which keep it. It is no longer a
#: ceiling: a release decides the rows in its own window (`Release.decided_above`,
#: `Release.decided_through`) and a walk reaches the counts in its own (`Walk.reaches`), so
#: a release whose window a records slice lifts decides its rows above 1024 (D1, think-f2io).
FROZEN_THROUGH = 1024
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
#: The Göbel receipt of a window above 1024, from the maintained module (`goebel_receipt`).
GOEBEL_FORMAT_V2 = "beyond-horizon-goebel-comparison-v2"
GOEBEL_MODULE = "packing/devtools/goebel_construction.py"
#: Each recipe row's decision by the construction checker, and the recipe parents the
#: release replays that are not rows (`write_recipe_decisions`).
RECIPES = Path("receipts/recipe-decisions.json")
RECIPES_FORMAT = "beyond-horizon-recipe-decisions-v1"
EARLIER = Path("receipts/earlier-publications.json")
EARLIER_FORMAT = "beyond-horizon-earlier-publications-v1"
INTAKE = ROOT / "campaign/issue-intake"
COVERAGE = ROOT / "frontier/source-coverage.yaml"
#: The results register, which holds the corpus counts a walk records (`declaration_problems`).
RESULTS = ROOT / "frontier/results.yaml"
RECORDED, NOT_RECORDED, UNDECIDED = "recorded", "not recorded", "undecided"
#: How an issue prints a side: rounded up at 12 places, or as the binary64 value of the
#: exact side at 16 places, which may lie below it (#719).
UP, BINARY64 = "up", "binary64"
_START_ROW = re.compile(r"beyond-horizon row (\S+)")
_BEAD = re.compile(r"think-[a-z0-9]{4}")


class ReplayError(ValueError):
    """Refuse a row, a certificate or a receipt that does not hold."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ReplayError(message)


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
#: The Kingbird catalogue's sides beyond the corpus (N1): the walk above 1024 records them
#: and the chain passes over them, so only the verdicts that rest on them wait.
CATALOGUE = "catalogue"
#: Where the owner's open questions on the work above 1024 are kept, N1 among them.
N1_BEAD = "think-llit"
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
    CATALOGUE: (
        "a side the Kingbird catalogue states beyond the corpus with its minimal polynomial, "
        "which is no issue, comment, pull request or watched commit: whether the catalogue "
        "is an earlier report there waits on the owner (N1, think-llit), so no row may hold "
        "it until the owner answers"
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
    CATALOGUE: "catalogue sides",
}
HELD_NAME = {
    CONSEQUENCE: "index deletion bound",
    RECIPE: "construction with no certificate file",
    WITHDRAWN: "certificate its author withdrew from an issue",
    CATALOGUE: "catalogue side",
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

    ``above`` and ``through`` are the counts the walk plans rows for (`reaches`): every
    walk frozen at 1024 reaches every count it walks to `FROZEN_THROUGH`, the corpus
    counts a release claims included, and the walk above 1024 every count above 1024, with
    no top (``through`` None). A count it walks outside them, as the #719 walk's claims
    above 1024, plans no row there.
    """

    name: str
    later: Mapping[str, str]
    awaiting: Mapping[str, Awaiting]
    held: Mapping[str, tuple[Held, ...]] = field(default_factory=dict)
    resting: tuple[Resting, ...] = ()
    above: int = 0
    through: int | None = FROZEN_THROUGH

    def reaches(self, n: int) -> bool:
        """Whether the walk plans rows at ``n``: above ``above`` and at most ``through``."""
        return self.above < n and (self.through is None or n <= self.through)

    @property
    def reach(self) -> str:
        """The counts the walk reaches beyond the corpus, as its sources' notes say them."""
        if self.through is None:
            return f"above {self.above}"
        return f"at or below {self.through}"

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
#: The counts the history walk reaches: beyond the corpus to `FROZEN_THROUGH`.
HISTORY_COUNTS = range(reports.HORIZON + 1, FROZEN_THROUGH + 1)
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
#: The walk of #732's later release, f1ceee4, which the author's comment of 23 October
#: 2026 at 20:35:12Z reports, and of the three commits past it, from starts frozen at
#: ``main`` at #754's merge, the first ``main`` after #742 recorded #732's rows
#: (`ISSUE_732_F1_READ_AT_MAIN`).
ISSUE_732_F1 = "upper-bounds-issue732-f1ceee4-20261024"
ISSUE_732_F1_READ_AT_MAIN = "0bbb0a2c4bae92393e26e7272c73a8de4cda1793"
#: The walk of issue #763's claims at or below `FROZEN_THROUGH`, Couzo's 964ee2b, with the
#: index's unrequested rows there, from starts frozen at ``main`` at #756's merge, the first
#: ``main`` that holds f1ceee4's rows (#769) and T-239 at 303 (#757)
#: (`ISSUE_763_READ_AT_MAIN`).
ISSUE_763 = "upper-bounds-issue763-20261024"
ISSUE_763_READ_AT_MAIN = "e5c1c64e39caaff6386eaa6720bdbe932d19b415"
#: The walk of the notebook rows the push of 23:38:42Z published in 964ee2b's index at 325
#: to 1024, credited to the authors of seven Kaggle notebooks (the claim map's ``others``,
#: think-lyf9), from starts frozen at ``main`` at #789's merge, the first ``main`` that
#: holds #763's rows (`NOTEBOOKS_964_READ_AT_MAIN`).
NOTEBOOKS_964 = "upper-bounds-couzo-964ee2b-notebooks-20261024"
NOTEBOOKS_964_READ_AT_MAIN = "2ec489d1eede791bf0686ca1c524278c2bb80253"
#: The walk of the live records Couzo's 43f666c publishes at 325 to 1024 below 964ee2b's
#: index (think-gn29), with #763's claims that have no row on ``main`` and the push of
#: 23:38:42Z at its counts, from starts frozen at ``main`` at #795's merge, the first
#: ``main`` that holds the notebook rows (`COUZO_43F_READ_AT_MAIN`).
COUZO_43F = "upper-bounds-couzo-43f666c-20261024"
COUZO_43F_READ_AT_MAIN = "2ed0ea7409b0ea21c47881f8874ce92a9d2011e8"
#: Couzo's 43f666c, which no issue reports (think-gn29): its packet pins 1c17153, the head
#: of the push of 06:10:44Z that made it public with 73eac5b and 1c17153.
COUZO_43F_PACKET = "couzo-43f666c-2026-10-24"
COUZO_43F_COMMIT = "43f666c23933fbc5cc418fa4e851218268fed0ed"
COUZO_43F_PIN = "1c1715399709bc955e9b402947ab8b52bbacdfc3"
COUZO_43F_PUSHED = "2026-10-24T06:10:44Z"
#: The ``main`` each release walk's starts are frozen at (`release_walk_sources`).
WALK_READ_AT_MAIN = {
    ISSUE_732: ISSUE_732_READ_AT_MAIN,
    ISSUE_732_F1: ISSUE_732_F1_READ_AT_MAIN,
    ISSUE_763: ISSUE_763_READ_AT_MAIN,
    NOTEBOOKS_964: NOTEBOOKS_964_READ_AT_MAIN,
    COUZO_43F: COUZO_43F_READ_AT_MAIN,
}
#: The receipt of a packet whose issue carries no table and whose claims are re-derived
#: from the source's own indexes (`devtools.couzo_763_claims`, `Release.claim_map`).
CLAIM_MAP = Path("receipts/claim-map.json")
#: The ``claim_map`` of a release of one push read commit by commit (`push_publications`).
PUSH = "push"
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


def deletion_holds(
    bounds: Iterable[tuple[int, int, int]], *, claimed_by: str = ""
) -> tuple[Held, ...]:
    """How a walk holds a report's deletion bounds, each ``(n, parent, deleted)``: the
    certificate at ``parent`` less its last ``deleted`` squares, so ``parent - deleted`` is
    ``n``.

    A bound a publication states that deletes one square from the next count's certificate
    is an earlier report by the owner's D6 answer, settled with no row of its own
    (`DELETION_ANSWER`, think-f2io). A bound deleting two or more squares is outside that
    question's words and waits on think-kzme, as the history walk's 751, 752 and 927 do.
    Every bound an issue claims waits on think-kzme too, whatever it deletes, with the bead
    of the issue's import (``claimed_by``), as #763's 683 does: whether an issue's deletion
    bound gets a row is that question (think-llit's plan, Deletion Rows).
    """
    settled: set[int] = set()
    waiting: set[int] = set()
    for n, parent, deleted in bounds:
        _require(
            deleted > 0 and parent - deleted == n,
            f"n={n}: {parent} less {deleted} squares is not {n}",
        )
        (settled if deleted == 1 and not claimed_by else waiting).add(n)
    holds: list[Held] = []
    if settled:
        holds.append(
            Held(
                CONSEQUENCE,
                "think-f2io",
                frozenset(settled),
                note="each deleting one square from the next count's certificate",
                answer=DELETION_ANSWER,
            )
        )
    if waiting and claimed_by:
        holds.append(
            Held(
                CONSEQUENCE,
                claimed_by,
                frozenset(waiting),
                also=("think-kzme",),
                note="deletion bounds the issue claims",
            )
        )
    elif waiting:
        holds.append(
            Held(
                CONSEQUENCE,
                "think-kzme",
                frozenset(waiting),
                note="each deleting two or more squares, beyond the D6 answer's words",
            )
        )
    return tuple(holds)


def catalogue_hold(counts: Iterable[int]) -> Held:
    """The walk above 1024's hold of the Kingbird catalogue's sides there (`CATALOGUE`),
    until the owner answers N1: recorded, passed over by the chain, and no row."""
    return Held(
        CATALOGUE,
        N1_BEAD,
        frozenset(counts),
        note="the capture of 2026-08-22, each side with its minimal polynomial (N1)",
    )


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
#: The publications the f1ceee4 walk records that the history walk holds, at the counts the
#: walk records them (`HISTORY_HELD`).
_HELD_IN_732_F1: tuple[tuple[str, str], ...] = (("franciscouzo/square-packing@4e4c8ce", "985"),)
#: The f1ceee4 walk's verdicts decided only against publications it holds for a decision
#: still owed (`Resting`).
_RESTING_732_F1: tuple[Resting, ...] = ()
#: #763's claim the walk records and holds back from a row: 683, 684's certificate less one
#: square, which the issue claims, so it waits on think-kzme's question whether an
#: issue-claimed deletion bound gets a row (think-2z2n). The walk held the issue's 13 tiling
#: and L-border recipes (365 444 487 632 733 734 737 788 789 845 910 966 970) on a maintained
#: construction checker until 43f666c's import (think-g2qy): the checker decides each one
#: exactly (D2, think-f2io; `RECIPES`), so each is a row the walk records, as it did, and the
#: release declares it with its recipe (`declared_rows`). The fourteenth recipe, 909,
#: restates PR C's row and is not recorded.
_HELD_763 = (
    _held(
        CONSEQUENCE,
        "think-2z2n",
        "683",
        also=("think-kzme",),
        note="684's certificate less one square, which the issue claims",
    ),
)
#: #763's recipes, held until the construction checker decided them in 43f666c's import, a
#: day after the issue's certificates landed: rows of a coverage source of their own, dated
#: by the merge that adds them, with the bead that decided them (`Split`; #800's review A,
#: A1). `split_problems` holds them to the release's declared recipe rows.
RECIPES_763 = frozenset({365, 444, 487, 632, 733, 734, 737, 788, 789, 845, 910, 966, 970})
#: The coverage source of #763's recipe rows (`RECIPES_763`).
COUZO_763_RECIPES_SOURCE = "couzo-issue763-2026-10-23-recipes"
#: The publications the #763 walk records that the history walk holds, at the counts the
#: walk records them (`HISTORY_HELD`).
_HELD_IN_763: tuple[tuple[str, str], ...] = (
    (
        "franciscouzo/square-packing@23aff0c",
        "457 542 588 590 629 630 638 680 681 690 733 734 788 789 845 847 904 905 966",
    ),
    ("franciscouzo/square-packing@4e4c8ce", "629 638 680 733 788 845 904"),
)
#: The #763 walk's verdicts decided only against publications it holds for a decision
#: still owed (`Resting`): earlier publications below its starts that rest on 23aff0c's
#: recipes and deletions from Friedman's constructions, as in the #732 walk.
_RESTING_763 = (
    _resting(f"{MISHAPOLK_REPOSITORY}@1851c2c", NOT_RECORDED, CONSEQUENCE, "542 588 638 847"),
    _resting(
        f"{MISHAPOLK_REPOSITORY}@1851c2c",
        NOT_RECORDED,
        RECIPE,
        "457 590 629 630 680 681 690 733 734 788 789 845",
    ),
    _resting(f"{MISHAPOLK_REPOSITORY}@3285fac", NOT_RECORDED, CONSEQUENCE, "542 588 638 847"),
    _resting(f"{MISHAPOLK_REPOSITORY}@3285fac", NOT_RECORDED, RECIPE, "590 690"),
    _resting("franciscouzo/square-packing@5a299b4", NOT_RECORDED, CONSEQUENCE, "588 638"),
    _resting(
        "franciscouzo/square-packing@5a299b4",
        NOT_RECORDED,
        RECIPE,
        "457 590 629 630 680 681 690 733 734 788 789 845 904 905 966",
    ),
)


#: The three commits of the push of 23:38:42Z, as the push walk's ledger labels them, in
#: commit order: efef7d1 and fa6237e state Couzo's own sides at the notebook rows' counts,
#: fa6237e first holds Tymchishin's "CPU Alternating Reclosure" v3 and Lavrentev's "CUDA
#: Packing Search" v11 rows, and 964ee2b the other five notebooks'.
COUZO_EFEF7D1 = "efef7d1418d0cb629debc962c077740125ba7901"
COUZO_FA6237E = "fa6237e288cf3fc53b53fc43438c91f3f59c40e9"
NOTEBOOKS_EFEF7D1 = "franciscouzo/square-packing@efef7d1"
NOTEBOOKS_FA6237E = "franciscouzo/square-packing@fa6237e"
NOTEBOOKS_964EE2B = "franciscouzo/square-packing@964ee2b"
#: The publications the notebook walk records that the history walk holds, at the counts the
#: walk records them (`HISTORY_HELD`).
_HELD_IN_NOTEBOOKS: tuple[tuple[str, str], ...] = (
    ("franciscouzo/square-packing@487b058", "327"),
    ("franciscouzo/square-packing@4e4c8ce", "533 580 589 965"),
    (
        "franciscouzo/square-packing@23aff0c",
        "406 533 541 543 580 589 639 846 906 907 965 967 968 981 982",
    ),
)
#: The notebook walk's verdicts decided only against publications it holds for a decision
#: still owed (`Resting`): earlier publications below its starts that rest on 487b058's,
#: 4e4c8ce's and 23aff0c's recipes and deletion bounds, as in the #763 walk.
_RESTING_NOTEBOOKS = (
    _resting(f"{MISHAPOLK_REPOSITORY}@1851c2c", NOT_RECORDED, CONSEQUENCE, "406 541 589"),
    _resting(f"{MISHAPOLK_REPOSITORY}@1851c2c", NOT_RECORDED, RECIPE, "533 543 580 639 846"),
    _resting(f"{MISHAPOLK_REPOSITORY}@3285fac", NOT_RECORDED, CONSEQUENCE, "406 541 589"),
    _resting(f"{MISHAPOLK_REPOSITORY}@3285fac", NOT_RECORDED, RECIPE, "543 639"),
    _resting(f"{MISHAPOLK_REPOSITORY}@8a488a1", NOT_RECORDED, CONSEQUENCE, "906 907 967 968"),
    _resting("franciscouzo/square-packing@23aff0c", NOT_RECORDED, RECIPE, "327"),
    _resting("franciscouzo/square-packing@4e4c8ce", NOT_RECORDED, RECIPE, "327"),
    _resting(
        "franciscouzo/square-packing@5a299b4",
        NOT_RECORDED,
        CONSEQUENCE,
        "406 589 906 907 967 968",
    ),
    _resting(
        "franciscouzo/square-packing@5a299b4",
        NOT_RECORDED,
        RECIPE,
        "327 533 580 639 846 965 981 982",
    ),
)


#: The publications the 43f666c walk records that the history walk holds, at the counts the
#: walk records them (`HISTORY_HELD`).
_HELD_IN_43F: tuple[tuple[str, str], ...] = (
    ("franciscouzo/square-packing@23aff0c", "367 733 734 788 789 845 966"),
    ("franciscouzo/square-packing@4e4c8ce", "733 788 845"),
)
#: The 43f666c walk's verdicts decided only against publications it holds for a decision
#: still owed (`Resting`): earlier publications below its starts that rest on 23aff0c's and
#: 4e4c8ce's recipes and deletions from Friedman's constructions, as in the #763 walk; the
#: push of 23:38:42Z's sides at 683, which rest on #763's deletion bound there (think-2z2n,
#: think-kzme); and 43f666c's own 367, an L-border of 330's certificate 3.83e-12 above
#: 23aff0c's deletion from Friedman's construction at 368 (think-zkxy).
_RESTING_43F = (
    _resting(f"{MISHAPOLK_REPOSITORY}@1851c2c", NOT_RECORDED, CONSEQUENCE, "367"),
    _resting(f"{MISHAPOLK_REPOSITORY}@1851c2c", NOT_RECORDED, RECIPE, "733 734 788 789 845"),
    _resting(f"{MISHAPOLK_REPOSITORY}@3285fac", NOT_RECORDED, CONSEQUENCE, "367"),
    _resting("franciscouzo/square-packing@43f666c", NOT_RECORDED, CONSEQUENCE, "367"),
    _resting(
        "franciscouzo/square-packing@5a299b4", NOT_RECORDED, RECIPE, "733 734 788 789 845 966"
    ),
    _resting("franciscouzo/square-packing@964ee2b", NOT_RECORDED, CONSEQUENCE, "683"),
    _resting("franciscouzo/square-packing@efef7d1", NOT_RECORDED, CONSEQUENCE, "683"),
    _resting("franciscouzo/square-packing@fa6237e", NOT_RECORDED, CONSEQUENCE, "683"),
)


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
    # f1ceee4's walk records the history walk's held publications where they stand below
    # the starts frozen after #754 (`_HELD_IN_732_F1`), and declares the verdicts resting on
    # them (`_RESTING_732_F1`).
    ISSUE_732_F1: Walk(
        ISSUE_732_F1,
        later={},
        awaiting={},
        held={report: _held_from_history(report, counts) for report, counts in _HELD_IN_732_F1},
        resting=_RESTING_732_F1,
    ),
    # #763's walk holds the issue's deletion bound at 683 (`_HELD_763`), and the history
    # walk's held publications where they stand below its starts (`_HELD_IN_763`). Its 13
    # recipes, held until the construction checker decided them, are rows (think-g2qy).
    ISSUE_763: Walk(
        ISSUE_763,
        later={},
        awaiting={},
        held={
            "#763": _HELD_763,
            **{report: _held_from_history(report, counts) for report, counts in _HELD_IN_763},
        },
        resting=_RESTING_763,
    ),
    # The push walk holds the history walk's held publications where they stand below its
    # starts (`_HELD_IN_NOTEBOOKS`). It holds no recipe: each of the notebooks' 12 has a
    # certificate at exactly its side (#795's review A, A2).
    NOTEBOOKS_964: Walk(
        NOTEBOOKS_964,
        later={},
        awaiting={},
        held={
            report: _held_from_history(report, counts) for report, counts in _HELD_IN_NOTEBOOKS
        },
        resting=_RESTING_NOTEBOOKS,
    ),
    # 43f666c's walk settles its deletion bound at 690, one square below 691's certificate,
    # by the owner's D6 answer (`deletion_holds`), holds #763's 683 as #763's walk does, and
    # holds the history walk's held publications where they stand below its starts
    # (`_HELD_IN_43F`).
    COUZO_43F: Walk(
        COUZO_43F,
        later={"#763": "couzo-issue763-2026-10-23"},
        awaiting={},
        held={
            f"franciscouzo/square-packing@{COUZO_43F_COMMIT[:7]}": deletion_holds(
                [(690, 691, 1)]
            ),
            "#763": _HELD_763,
            **{report: _held_from_history(report, counts) for report, counts in _HELD_IN_43F},
        },
        resting=_RESTING_43F,
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


def ruling_entries(
    *awaiting: Mapping[str, Any], through: int | None = FROZEN_THROUGH
) -> list[dict[str, Any]]:
    """The owner's rulings of 23 October 2026 as a walk's ``sources.yaml`` names them
    (`devtools.intake_ledger.Ruling`), with the claims the restatement ruling leaves to the
    owner. A walk frozen at 1024 lists both through `FROZEN_THROUGH`; the walk above 1024
    lists them with no ``through`` (``through`` None, `devtools.intake_ledger.NO_LIMIT`), so
    they reach its top count, as `devtools.intake_ledger.answer_problems` requires."""
    reach = {} if through is None else {"through": through}
    restatement: dict[str, Any] = {
        "ruling": "restatement",
        "decided": "2026-10-23",
        "bead": "think-fwa9",
        **reach,
    }
    if awaiting:
        restatement["awaiting_owner"] = [dict(item) for item in awaiting]
    classical = {
        "ruling": "classical-constructions",
        "decided": "2026-10-23",
        "bead": "think-8krd",
        **reach,
    }
    return [restatement, classical]


#: The owner's rulings each walk applies (`devtools.intake_ledger.RULINGS`). The walks
#: frozen at 1024 apply them through `FROZEN_THROUGH`; the walk above 1024 applies the same
#: answers with no top (`ruling_entries`, ``through`` None). The backlog walk applies none:
#: it was read on 22 October, and no step of it is in either's words.
WALK_RULINGS: dict[str, list[dict[str, Any]]] = {
    ISSUE_719: ruling_entries(_AWAITING_719_631),
    HISTORY: ruling_entries(_AWAITING_719_631),
    ISSUE_732: ruling_entries(),
    ISSUE_732_F1: ruling_entries(),
    ISSUE_763: ruling_entries(),
    NOTEBOOKS_964: ruling_entries(),
    COUZO_43F: ruling_entries(),
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


# --------------------------------------------------------------------------- the releases


@dataclass(frozen=True, slots=True)
class Claim:
    """One row of an issue's table: the count, the print, and the certificate it reads.

    A deletion row reads its parent's certificate, ``certificate_n``, less ``deleted``
    squares. A recipe row (``recipe``, as its packet declares it) has no certificate file
    of its own: ``path`` is its parent's, and the construction checker decides it
    (`write_recipe_decisions`, D2).
    """

    n: int
    prior: str
    printed: str
    path: str
    certificate_n: int
    deleted: int
    recipe: Mapping[str, Any] | None = None


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
class Split:
    """A release's rows that reach `main` in a later merge than its others, recorded as a
    coverage source of their own (#800's review A, A1).

    A source carries one landing day, the day `main` first held any of its rows
    (`devtools.stamp_landed`), and the home page's Recently Added lists all of a source's
    rows under it. Rows a later merge adds to a landed release therefore go under a source
    of their own, ``source_id``, with the bead that decided them, ``bead``, and a claims
    record of their own in the packet, ``record``, holding exactly them, while the release's
    record keeps the rest. ``counts`` are the rows the split holds: each must be a declared
    row of the release that its walk records (`split_problems`). #763's 13 L-border recipes,
    held until the construction checker decided them in 43f666c's import (think-g2qy) a day
    after the issue's certificates landed, are the one split (`RECIPES_763`).
    """

    counts: frozenset[int]
    source_id: str
    bead: str
    record: Path


@dataclass(frozen=True, slots=True)
class Release:
    """One report, as this module reads it from its packet.

    ``pin`` is the commit the issue links, ``retained`` the one the packet holds (the same
    but for #666), and ``first_commit`` the first commit of ``retained``'s history that holds
    every certificate a row reads, committed at ``committed``, but for the counts
    ``later_commits`` names with their own commit and time: what ``first-commits`` measures
    and the claims record states. ``rows`` counts the issue's table and ``decided`` the rows
    in the release's window (`decided_claims`); ``sampled`` names the counts the all-pairs
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

    **A later release reported in a comment** on its issue, as #732's ``f1ceee4``, names the
    comment (``comment``): the ledger labels it ``#N comment ID`` and dates it by the comment.
    Its source history is held to the index the release keeps current (``index``, whose
    ``index_key`` maps each count to its certificate path, SHA-256 and exact bound), and
    with ``changed_only`` its walk's claims are the certificates the pinned commit adds or
    changes, not every certificate the commit holds. ``later_reads`` names the commits past
    the pin, each with the time a push made it public, whose publications at any count the
    walk reaches the walk takes as reports of their own (`later_commits`).

    **An issue whose claims are re-derived** from its source's indexes, as #763's, names the
    list of its packet's claim map (`CLAIM_MAP`, written by `devtools.couzo_763_claims`) its
    claims are (``claim_map``): ``claims`` for the issue's, ``unrequested`` for the rows the
    index publishes that its selection rule leaves out, a publication of their own. Its walk's
    sources are transcribed from that map (`claim_map_walk_sources`), and its declared rows
    read each certificate from it (`declared_rows`).

    **Several sources in one report.** A commit's publications that credit several authors,
    as each commit of the push that made 964ee2b public (think-lyf9), are one report of the
    ledger, labelled by the commit, with a release a coverage source: ``name`` keys the
    release in `RELEASES` where its label is shared, and ``notebook_run`` takes from the
    push's receipt the claims of one notebook run at the release's commit, or 0 the
    publisher's own (`PUSH`, `push_publications`). The walk reads the releases of one label
    as one report (`_walk_groups`), and a count's source is the release that claims it there
    (`release_at`).

    **The window.** A release decides its rows from ``decided_above`` (exclusive, the
    corpus by default) to ``decided_through`` (inclusive; None for no top): every release
    on ``main`` before the work above 1024 decides to `FROZEN_THROUGH`, and its rows above
    wait (`held_claims`) until the records slice that lifts its window, in the same pull
    request as the receipts that window needs (think-llit). Its rows to 1024 are planned by
    ``walk``, and those above 1024 by ``walk_above``, the walk above 1024 that records them
    (`walk_of`). ``hosted`` names the hosted-data manifest of the certificates the packet
    pins and does not retain, read through `sqpack.hosted_data.require` (`hosted_bytes`).

    **Rows a later merge adds.** ``split`` names the release's rows that reach `main` after
    its others, with a coverage source, bead and claims record of their own (`Split`);
    `source_at` and `bead_at` give each row's.
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
    comment: int | None = None
    index: str = "certificates/manifest.json"
    index_key: str = "witnesses"
    changed_only: bool = False
    later_reads: tuple[tuple[str, str], ...] = ()
    claim_map: str = ""
    name: str = ""
    notebook_run: int = 0
    decided_above: int = reports.HORIZON
    decided_through: int | None = FROZEN_THROUGH
    walk_above: str = ""
    hosted: Path | None = None
    split: Split | None = None

    def decides(self, n: int) -> bool:
        """Whether ``n`` is in the release's window (`decided_claims`)."""
        return self.decided_above < n and (
            self.decided_through is None or n <= self.decided_through
        )

    @property
    def frozen(self) -> bool:
        """Whether the release's window ends at or below `FROZEN_THROUGH`, so its Göbel
        receipt keeps the retained program (`goebel_receipt`)."""
        return self.decided_through is not None and self.decided_through <= FROZEN_THROUGH

    @property
    def directory(self) -> Path:
        return WEB / self.packet

    @property
    def push_holder(self) -> str:
        """Whose claims a push release takes (`PUSH`): its notebook run, else the
        publisher's (`PUBLISHER`)."""
        return str(self.notebook_run) if self.notebook_run else PUBLISHER

    @property
    def key(self) -> str:
        """How `RELEASES` and the commands name the release: its ``name`` where its label is
        shared with another release, else its label."""
        return self.name or self.label

    @property
    def label(self) -> str:
        """How the ledger names the report: ``#N``, ``#N comment ID`` for a release a comment
        reports, or ``owner/name@commit`` (seven hex)."""
        if self.issue is not None and self.comment is not None:
            return f"#{self.issue} comment {self.comment}"
        if self.issue is not None:
            return f"#{self.issue}"
        return f"{repository_of(self.source_url)}@{self.pin[:7]}"

    @property
    def described(self) -> str:
        """The report in a sentence: ``issue #N``, its comment, or the publication's label."""
        if self.issue is not None and self.comment is not None:
            return f"issue #{self.issue}'s comment {self.comment}"
        if self.name:
            return f"{self.label}, the {self.name} rows"
        return f"issue #{self.issue}" if self.issue is not None else self.label

    @property
    def source(self) -> str:
        """The coverage source whose dated rows record this report, but for the rows its
        split holds (`source_at`)."""
        return self.source_id or self.packet

    @property
    def sources(self) -> tuple[str, ...]:
        """Every coverage source whose rows record this report: its own, then its split's."""
        return (self.source,) + ((self.split.source_id,) if self.split is not None else ())

    def source_at(self, n: int) -> str:
        """The coverage source whose row records this report at ``n``: the split's at a
        count it holds (`Split`), else the release's."""
        if self.split is not None and n in self.split.counts:
            return self.split.source_id
        return self.source

    def bead_at(self, n: int) -> str:
        """The bead a row at ``n`` names: the split's at a count it holds, else the
        release's."""
        if self.split is not None and n in self.split.counts:
            return self.split.bead
        return self.bead

    @property
    def records(self) -> tuple[Path, ...]:
        """Every claims record of the release in its packet: its own, then its split's."""
        own = self.path(RECORD)
        return (own,) + ((self.directory / self.split.record,) if self.split else ())

    @property
    def issue_url(self) -> str:
        """The report's address: the issue or its comment, or the publication's tree at
        its commit."""
        if self.issue is not None and self.comment is not None:
            return (
                f"https://github.com/jlevy/squares/issues/{self.issue}"
                f"#issuecomment-{self.comment}"
            )
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
        """The commit that first holds the certificate a row at ``n`` reads, and its time.

        A recipe row has no file of its own, and its parent's file may be older than the
        recipe: it is dated by the first commit whose index states its recipe (#793's review
        A, A8), which `first_commits` reads (`recipe_first_commits`).
        """
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
    up at 12 places, all of the publication's commit, and for a deletion the squares it
    deletes from that certificate (``deleted``), and for a recipe its parent's certificate
    and the recipe (``recipe``); `declare_rows` writes them. A row's ``certificate_n`` is
    the count its certificate's header states: n plus the squares a deletion deletes, and
    a recipe's parent count, ``source_n`` (#793's review A, A8)."""
    declared = json.loads(body)
    _require(declared.get("format") == WATCHED_FORMAT, f"{release.label}: not {WATCHED_FORMAT}")
    _require(
        declared.get("commit") == release.pin
        and declared.get("publication") == release.issue_url
        and declared.get("walk") == release.walk,
        f"{release.label}: the declaration names another commit or walk",
    )
    return [
        Claim(
            int(row["n"]),
            "",
            str(row["printed"]),
            str(row["certificate"]),
            int(row["recipe"]["source_n"])
            if row.get("recipe")
            else int(row["n"]) + int(row.get("deleted", 0)),
            int(row.get("deleted", 0)),
            row.get("recipe"),
        )
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
#: Issue #763's packet and pin, Couzo's 964ee2b, and the push that made it public.
COUZO_763_PACKET = "couzo-issue763-2026-10-23"
COUZO_763_PIN = "964ee2bdf301d0c8912d956d4010f478dcbbd5ea"
COUZO_763_PUSHED = "2026-10-23T23:38:42Z"
#: The counts whose certificate 964ee2b's parents first committed, efef7d1 and fa6237e,
#: each with its commit and committer time, and the recipes efef7d1's index first states,
#: 365 and 970 (`recipe_first_commits`); the push of 23:38:42Z made all three public.
_COUZO_763_EARLIER: dict[int, tuple[str, str]] = {
    **dict.fromkeys(
        (328, 344, 365, 420, 452, 490, 803, 850, 935, 970, 1486, 1647, 1648, 1765, 1898, 2263),
        ("efef7d1418d0cb629debc962c077740125ba7901", "2026-10-23T18:16:49Z"),
    ),
    **dict.fromkeys(
        (413, 498, 592, 747, 752, 794, 870, 931),
        ("fa6237e288cf3fc53b53fc43438c91f3f59c40e9", "2026-10-23T18:59:39Z"),
    ),
}


class PushRelease(NamedTuple):
    """One holder's claims at one commit of the push of 23:38:42Z that made 964ee2b public,
    as `push_publications` reads them (think-lyf9; #795's review A, A1): the holder, a
    Kaggle notebook run or the publisher's own sides (0), the receipts' tag, the coverage
    source and release name of its rows, its holder as the source credits it, the commit and
    its committer time, its certificate rows, and the counts the all-pairs sample decides."""

    run: int
    tag: str
    source: str
    holders: str
    commit: str
    committed: str
    rows: int
    sampled: tuple[int, ...] = ()


#: The push's releases, one coverage source each (the coordinator's decisions of 24 October
#: 2026 on think-lyf9): the seven notebook runs, Kirill Tymchishin's and Vladislav
#: Lavrentev's named by the source and three credited only by their Kaggle handles, and
#: Couzo's own sides at the push's first two commits, which its last replaced.
PUSH_RELEASES: tuple[PushRelease, ...] = (
    PushRelease(
        0,
        "couzo-efef7d1",
        "couzo-efef7d1-2026-10-23",
        "Francisco Couzo",
        COUZO_EFEF7D1,
        "2026-10-23T18:16:49Z",
        35,
    ),
    PushRelease(
        0,
        "couzo-fa6237e",
        "couzo-fa6237e-2026-10-23",
        "Francisco Couzo",
        COUZO_FA6237E,
        "2026-10-23T18:59:39Z",
        37,
    ),
    PushRelease(
        361239073,
        "361239073",
        "tymchishin-reclosure-v3-2026-10-23",
        "Kirill Tymchishin",
        COUZO_FA6237E,
        "2026-10-23T18:59:39Z",
        42,
        (975,),
    ),
    PushRelease(
        361263594,
        "361263594",
        "lavrentev-cuda-v11-2026-10-23",
        "Vladislav Lavrentev",
        COUZO_FA6237E,
        "2026-10-23T18:59:39Z",
        11,
    ),
    PushRelease(
        361576574,
        "361576574",
        "tymchishin-22-3662-2026-10-23",
        "Kirill Tymchishin",
        COUZO_763_PIN,
        "2026-10-23T22:38:09Z",
        15,
    ),
    PushRelease(
        361592092,
        "361592092",
        "kyleluecke-inos-2026-10-23",
        "kyleluecke",
        COUZO_763_PIN,
        "2026-10-23T22:38:09Z",
        18,
    ),
    PushRelease(
        361412241,
        "361412241",
        "alexchilton-fault-line-2026-10-23",
        "alexchilton",
        COUZO_763_PIN,
        "2026-10-23T22:38:09Z",
        11,
    ),
    PushRelease(
        361516058,
        "361516058",
        "aqibrazadev-blending-2026-10-23",
        "aqibrazadev",
        COUZO_763_PIN,
        "2026-10-23T22:38:09Z",
        9,
        (994,),
    ),
    PushRelease(
        361589987,
        "361589987",
        "lavrentev-cuda-run-361589987-2026-10-23",
        "Vladislav Lavrentev",
        COUZO_763_PIN,
        "2026-10-23T22:38:09Z",
        7,
    ),
)

RELEASES: dict[str, Release] = {
    release.key: release
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
        # The author's comment on #732 of 2026-10-23T20:35:12Z (issuecomment-6374211504)
        # reports f1ceee4, which rewrites 138 certificates at 328 to 989 and the two bound
        # indexes, and leaves certificates/manifest.json as 7b6366f wrote it: the release's
        # current index is certified_bounds.json. The three commits after it, pushed at
        # 21:28:42Z (34e59f3 and c0bf150, in one push) and 21:42:38Z (7e82c64) as the
        # repository's activity log records, change only counts in the corpus.
        Release(
            issue=732,
            comment=6374211504,
            packet="mishapolk-issue732-f1ceee4-2026-10-23",
            holders="Mykhailo Polkovskyi",
            source_url=MISHAPOLK_URL,
            pin="f1ceee4c1dd69f97d8e50e6ddaf1a14084dceda7",
            retained="f1ceee4c1dd69f97d8e50e6ddaf1a14084dceda7",
            first_commit="f1ceee4c1dd69f97d8e50e6ddaf1a14084dceda7",
            committed="2026-10-23T20:34:13Z",
            rows=138,
            decided=138,
            sampled=(335, 747, 989),
            bead="think-e3im",
            read=read_declared_rows,
            walk=ISSUE_732_F1,
            declared=Path("acquisition/declared-rows.json"),
            index="certified_bounds.json",
            index_key="entries",
            changed_only=True,
            later_reads=(
                ("34e59f349318ce55ad611fec577f89048c83c769", "2026-10-23T21:28:42Z"),
                ("c0bf1501d031f2c802cec3eec0846e63ee548021", "2026-10-23T21:28:42Z"),
                ("7e82c6408937c9a6fe2e11054ed716bba67922f0", "2026-10-23T21:42:38Z"),
            ),
        ),
        # Issue #763 (2026-10-23T23:35:51Z) names 964ee2b and carries no table: its claims
        # are re-derived from the source's indexes by the README's rule (`CLAIM_MAP`), and
        # its rows are those its walk records in its window, to `FROZEN_THROUGH`
        # (`declared_rows`). Its 13 recipes, decided in 43f666c's import, are rows of a
        # source of their own (`Split`, `RECIPES_763`).
        Release(
            issue=763,
            packet=COUZO_763_PACKET,
            holders="Francisco Couzo",
            source_url=COUZO_URL,
            pin=COUZO_763_PIN,
            retained=COUZO_763_PIN,
            first_commit=COUZO_763_PIN,
            committed="2026-10-23T22:38:09Z",
            rows=197,
            decided=197,
            sampled=(333, 684, 997),
            bead="think-ptkk",
            read=read_declared_rows,
            walk=ISSUE_763,
            declared=Path("acquisition/declared-rows.json"),
            later_commits=_COUZO_763_EARLIER,
            index="certified_bounds.json",
            index_key="entries",
            claim_map="claims",
            split=Split(
                RECIPES_763,
                COUZO_763_RECIPES_SOURCE,
                "think-g2qy",
                Path("acquisition/beyond-horizon-rows-recipes.json"),
            ),
        ),
        # The rows certified_bounds.json publishes at 964ee2b to `FROZEN_THROUGH` that the
        # issue's selection rule leaves out (`CLAIM_MAP`'s ``unrequested``): a publication
        # of the watched repository from the push that made it public, 2 min 51 s after the
        # issue, and an import of its own in the same packet (result-import.md, stage 1).
        Release(
            issue=None,
            packet=COUZO_763_PACKET,
            holders="Francisco Couzo",
            source_url=COUZO_URL,
            pin=COUZO_763_PIN,
            retained=COUZO_763_PIN,
            first_commit=COUZO_763_PIN,
            committed="2026-10-23T22:38:09Z",
            rows=10,
            decided=10,
            sampled=(998,),
            bead="think-ptkk",
            read=read_declared_rows,
            walk=ISSUE_763,
            later_commits=_COUZO_763_EARLIER,
            published=COUZO_763_PUSHED,
            source_id="couzo-964ee2b-2026-10-23",
            record=Path("acquisition/beyond-horizon-rows-964ee2b.json"),
            receipts=Path("receipts/964ee2b"),
            declared=Path("acquisition/watched-release-964ee2b.json"),
            index="certified_bounds.json",
            index_key="entries",
            claim_map="unrequested",
        ),
        # The notebook rows the same push published, and Couzo's own sides its first two
        # commits published at those counts, read commit by commit (`push_publications`): a
        # release a holder and a commit, each its own coverage source, and one report of
        # their walk a commit, efef7d1, fa6237e or 964ee2b (`PUSH_RELEASES`, think-lyf9).
        *(
            Release(
                issue=None,
                packet=COUZO_763_PACKET,
                holders=item.holders,
                source_url=COUZO_URL,
                pin=item.commit,
                retained=COUZO_763_PIN,
                first_commit=item.commit,
                committed=item.committed,
                rows=item.rows,
                decided=item.rows,
                sampled=item.sampled,
                bead="think-lyf9",
                read=read_declared_rows,
                walk=NOTEBOOKS_964,
                published=COUZO_763_PUSHED,
                source_id=item.source,
                record=Path(f"acquisition/beyond-horizon-rows-push-{item.tag}.json"),
                receipts=Path(f"receipts/push/{item.tag}"),
                declared=Path(f"acquisition/watched-release-push-{item.tag}.json"),
                index="certified_bounds.json",
                index_key="entries",
                claim_map=PUSH,
                name=item.source,
                notebook_run=item.run,
            )
            for item in PUSH_RELEASES
        ),
        # Couzo's 43f666c, which no issue reports: the counts at 325 to 1024 where its
        # certified_bounds.json lowers 964ee2b's bound (devtools.couzo_43f666c_claims,
        # ``lowered``), a watched repository's publication dated by the push of 06:10:44Z
        # that made it public, and an import of its own (think-gn29). Its packet pins the
        # push's head, 1c17153, whose two commits change no bound.
        Release(
            issue=None,
            packet=COUZO_43F_PACKET,
            holders="Francisco Couzo",
            source_url=COUZO_URL,
            pin=COUZO_43F_COMMIT,
            retained=COUZO_43F_PIN,
            first_commit=COUZO_43F_COMMIT,
            committed="2026-10-24T00:55:44Z",
            rows=122,
            decided=122,
            sampled=(330, 691, 997),
            bead="think-gn29",
            read=read_declared_rows,
            walk=COUZO_43F,
            published=COUZO_43F_PUSHED,
            source_id="couzo-43f666c-2026-10-24",
            index="certified_bounds.json",
            index_key="entries",
            claim_map="lowered",
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
    issue reports (its label, ``owner/name@commit``, or the ``name`` of one release of a
    label several share, `Release.key`)."""
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


def mapped_path(chosen: Release) -> Path:
    """Where a re-derived release's claims are listed: its packet's claim map, or, for a
    release of one push read commit by commit (`PUSH`), the push's receipt."""
    return chosen.directory / (PUSH_PUBLICATIONS if chosen.claim_map == PUSH else CLAIM_MAP)


def mapped_claims(chosen: Release) -> list[dict[str, Any]]:
    """A release's claims as its packet's claim map lists them (`Release.claim_map`), or a
    push release's, its holder's claims at its commit in the push's receipt."""
    _require(bool(chosen.claim_map), f"{chosen.label}: its claims are not re-derived")
    if chosen.claim_map == PUSH:
        return [
            item
            for item in _read(mapped_path(chosen))["claims"]
            if item["commit"] == chosen.pin and item["holder"] == chosen.push_holder
        ]
    return list(_read(chosen.directory / CLAIM_MAP)[chosen.claim_map])


def declares_rows(chosen: Release) -> bool:
    """Whether a release's packet declares its rows from its walk (`declared_rows`): every
    publication no issue reports, and an issue with no table of rows, as #732."""
    return chosen.read is read_declared_rows


def window(chosen: Release) -> str:
    """A release's window in words, as a refusal names it."""
    top = "" if chosen.decided_through is None else f" to {chosen.decided_through}"
    return f"above {chosen.decided_above}{top}"


def decided_claims(chosen: Release) -> list[Claim]:
    """The rows in the release's window (`Release.decides`), which this module decides,
    refused unless they are as many as the release declares: a release asked to decide a
    claim outside the window it was recorded with no longer matches its count."""
    rows = [row for row in claims(chosen) if chosen.decides(row.n)]
    _require(
        len(rows) == chosen.decided,
        f"{chosen.label}: {len(rows)} rows {window(chosen)}, not {chosen.decided}",
    )
    return rows


def held_claims(chosen: Release) -> list[Claim]:
    """The rows above the release's window, retained or pinned and not decided: they wait
    on the records slice that lifts it (think-llit)."""
    top = chosen.decided_through
    return [] if top is None else [row for row in claims(chosen) if row.n > top]


def replayed_claims(chosen: Release) -> list[Claim]:
    """The decided rows the filtered replay decides: every one but a recipe row."""
    return [row for row in decided_claims(chosen) if row.recipe is None]


def recipe_claims(chosen: Release) -> list[Claim]:
    """The decided rows the construction checker decides (`write_recipe_decisions`)."""
    return [row for row in decided_claims(chosen) if row.recipe is not None]


def manifest(chosen: Release) -> dict[str, str]:
    """The packet's upstream digests, by upstream path."""
    return acquire_source.read_manifest(chosen.directory / acquire_source.MANIFEST)


def hosted_pins(chosen: Release, root: Path | None = None) -> dict[str, str]:
    """The certificates a release's hosted shards hold: every file the packet pins and
    does not retain under ``root`` (its `archive`), whose path names a count above
    `FROZEN_THROUGH` (`named_count`), with the SHA-256 the packet pins for it."""
    root = root or archive(chosen)
    return {
        path: digest
        for path, digest in manifest(chosen).items()
        if (n := named_count(path)) is not None
        and n > FROZEN_THROUGH
        and not retained_exists(root / path)
    }


class Hosting:
    """A release's hosted certificates as one call reads them (#793's reviews A, A3, and
    B, B3): the packet's pins for the files its shards hold (`hosted_pins`), read once; the
    source-history receipts' entries for them (`index_entries`), read once when first
    asked; one reader of the shards (`devtools.hosted_shards.Hosted`); and the packet's
    retained root (`archive`), read once. A call that reads many rows builds one and passes
    it to each, so a check over thousands of rows parses the acquisition record, the
    manifest and each receipt once. A release with no hosted manifest hosts nothing, and
    reads neither the manifest nor a receipt."""

    def __init__(self, chosen: Release) -> None:
        self.chosen = chosen
        self.archive = archive(chosen)
        self.pins: Mapping[str, str] = (
            hosted_pins(chosen, self.archive) if chosen.hosted else {}
        )
        self._entries: Mapping[str, Mapping[str, Any]] | None = None
        self._reader: hosted_shards.Hosted | None = None

    def hosts(self, path: str) -> bool:
        """Whether ``path`` is read from the shards: one of `hosted_pins`."""
        return path in self.pins

    @property
    def entries(self) -> Mapping[str, Mapping[str, Any]]:
        """The source-history entries (`index_entries`), read on first use."""
        if self._entries is None:
            self._entries = index_entries(self.chosen)
        return self._entries

    def entry(self, path: str, n: int, where: str) -> Mapping[str, Any]:
        """A hosted certificate's source-history entry, held to the packet's pin and to
        the count ``n``: the one place the fast check reads a hosted side or blob from."""
        found = self.entries.get(path)
        _require(found is not None, f"{where}: hosted, and no source-history receipt lists it")
        assert found is not None
        _require(
            found["sha256"] == self.pins[path] and found["n"] == n,
            f"{where}: the source history's digest or count is not the packet's",
        )
        return found

    def read(self, path: str) -> bytes:
        """A hosted certificate's bytes from the shards, held to its pin."""
        chosen = self.chosen
        assert chosen.hosted is not None
        try:
            if self._reader is None:
                self._reader = hosted_shards.hosted(REPO / chosen.hosted, self.pins, REPO)
            return self._reader.read(path)
        except hosted_shards.ShardError as error:
            raise ReplayError(f"{chosen.label}: {error}") from error


def is_hosted(chosen: Release, path: str, hosting: Hosting | None = None) -> bool:
    """Whether a certificate is read from the release's hosted shards, not its packet: it
    is one of `hosted_pins`, the same predicate (#793's review B, B3)."""
    return (hosting or Hosting(chosen)).hosts(path)


def certificate_bytes(chosen: Release, path: str, hosting: Hosting | None = None) -> bytes:
    """A certificate's bytes: retained in the packet, or, for one it pins and does not
    retain, read from the release's hosted shards through `sqpack.hosted_data.require`
    and held to the packet's pin (`devtools.hosted_shards`)."""
    hosting = hosting or Hosting(chosen)
    if not hosting.hosts(path):
        return read_retained_bytes(hosting.archive / path)
    return hosting.read(path)


def index_entries(chosen: Release) -> dict[str, Mapping[str, Any]]:
    """Each certificate the release's source-history receipts list at the retained
    commit, by path: its Git blob, SHA-256 and exact side, each held to the release's index
    when the receipt was written (`source_history`). The fast check reads a hosted row's
    side and blob from here, so it opens no shard."""
    found: dict[str, Mapping[str, Any]] = {}
    for walk in walks_of(chosen):
        path = source_history_path(chosen, walk)
        if path.is_file():
            found |= {row["certificate"]: row for row in _read(path)["at_commit"]}
    return found


def certificate_side(
    chosen: Release, path: str, n: int, where: str, hosting: Hosting | None = None
) -> Fraction:
    """A certificate's exact side: its header line (`header_side`), or for a hosted one
    the side its source-history receipt states, held to the digest the packet pins
    (`Hosting.entry`)."""
    hosting = hosting or Hosting(chosen)
    if not hosting.hosts(path):
        return header_side(read_retained_bytes(hosting.archive / path), n, where)
    return Fraction(str(hosting.entry(path, n, where)["side"]))


def blob_of(chosen: Release, path: str, n: int, hosting: Hosting | None = None) -> str:
    """A certificate's Git blob: from its retained bytes, or for a hosted one from its
    source-history receipt, which held it to the clone's tree, the entry held to the
    packet's pin and the count ``n`` as for its side (`Hosting.entry`, #793's review B,
    B3)."""
    hosting = hosting or Hosting(chosen)
    if not hosting.hosts(path):
        return git_blob(read_retained_bytes(hosting.archive / path))
    return str(hosting.entry(path, n, f"{chosen.label} {path}")["blob"])


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
        raw = certificate_bytes(chosen, row.path)
        parsed = legacy.parse(raw.decode("utf-8"), expected_n=row.certificate_n)
    if row.deleted:
        parsed = legacy.Certificate(row.n, parsed.side, parsed.poses[: row.n])
    return parsed


def header_side(raw: bytes, expected_n: int, where: str) -> Fraction:
    """A certificate's side from its header line alone, ``n S``, the first line that is
    neither blank nor a comment, read by the rule `devtools.evand_exact_certificates.parse`
    applies to it (`devtools.evand_exact_certificates.header`, #793's review A, A12); the
    count must be ``expected_n``. The squares are not read: their parse is what the replay
    decides, and the receipts hold."""
    start = 0
    while start <= len(raw):
        end = raw.find(b"\n", start)
        end = len(raw) if end < 0 else end
        line = raw[start:end].decode("utf-8").strip()
        start = end + 1
        if not line or line.startswith("#"):
            continue
        try:
            return legacy.header(line.split(), expected_n=expected_n)[1]
        except legacy.CertificateError as error:
            raise ReplayError(f"{where}: {error}") from error
    raise ReplayError(f"{where}: no header")


def decided_sides(chosen: Release) -> dict[int, Fraction]:
    """Each decided row's exact side: a retained certificate's header line alone
    (`header_side`), or, for a derived packet, the side its frozen claim record states
    (`devtools.upper_bound_reports`), which that importer's ``check`` holds to the facts and
    ``check --replay`` here decides again from them. The fast check reads it once a release
    (`release_problems`): parsing every square, as the replay does, was three quarters of
    that check's time (think-llit, Gate Cost)."""
    rows = decided_claims(chosen)
    if not chosen.derived:
        hosting = Hosting(chosen)
        return {
            row.n: claim_side(
                row,
                certificate_side(
                    chosen,
                    row.path,
                    row.certificate_n,
                    f"{chosen.label} n={row.n} {row.path}",
                    hosting,
                ),
            )
            for row in rows
        }
    stated = {
        item["n"]: Fraction(item["exact_side"])
        for item in _read(chosen.directory / reports.CLAIMS)["results"]
    }
    _require(
        all(row.certificate_n in stated for row in rows),
        f"{chosen.label}: the claim record does not state every decided side",
    )
    return {row.n: stated[row.certificate_n] for row in rows}


def claim_side(row: Claim, parent: Fraction) -> Fraction:
    """A row's exact side from its certificate's: a recipe row's is the parent's times
    the tiles, plus the layers (the construction checker holds the recipe's stated bound
    to it); any other row's is its certificate's, a deletion's too. `decided_sides` and
    `release_sides` both read a row's side by this rule (#793's review B, B2)."""
    if row.recipe is None:
        return parent
    return int(row.recipe["tiles_per_side"]) * parent + int(row.recipe["layers"])


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
    row = next(row for row in replayed_claims(chosen) if row.n == job[1])
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
        (row.certificate_n, item.key, row.n) for item in chosen for row in replayed_claims(item)
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
        results = [decided[item.key, row.n] for row in replayed_claims(item)]
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
            "run_releases": [other.key for other in chosen],
            "workers": workers,
            "rows": results,
            "summary": base.summary(results),
        }
        _write(item.path(FILTERED), receipt)
        receipts[item.key] = receipt
    return receipts


# --------------------------------------------------------------------------- recipe rows


def recipe_of(chosen: Release, row: Claim) -> checker.Recipe:
    """A recipe row as the construction checker reads it: the recipe its packet declares
    (``kind``, ``source_n``, ``tiles_per_side``, ``layers``, the ``capacity`` and exact
    ``bound`` the index states and the parent's ``sha256``), on the parent ``row.path``."""
    recipe = row.recipe
    _require(recipe is not None, f"{chosen.label} n={row.n}: not a recipe row")
    assert recipe is not None
    return checker.Recipe(
        n=row.n,
        kind=str(recipe["kind"]),
        source_n=int(recipe["source_n"]),
        parent=row.path,
        parent_sha256=str(recipe["sha256"]),
        bound=Fraction(str(recipe["bound"])),
        tiles_per_side=int(recipe["tiles_per_side"]),
        layers=int(recipe["layers"]),
        deleted=row.deleted,
        capacity=None if recipe.get("capacity") is None else int(recipe["capacity"]),
        parts=tuple(str(part) for part in recipe.get("parts") or ()),
    )


def decide_parent(job: tuple[str, str, int]) -> dict[str, Any]:
    """A recipe parent that is not a row, ``(release key, path, count)``, decided as
    `decide_row` decides a row: both routes, and its six controls."""
    chosen = release(job[0])
    path, n = job[1], job[2]
    raw = certificate_bytes(chosen, path)
    cert = legacy.parse(raw.decode("utf-8"), expected_n=n)
    started = time.monotonic()
    result = base.decide(base.geometry(cert))
    return {
        "n": n,
        "certificate": path,
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "exact_side": legacy.literal(cert.side),
        "verified": result["passed"],
        "decision": result,
        "controls": base.decide_controls(cert),
        "wall_seconds": round(time.monotonic() - started, 3),
    }


def _replayed_parents(chosen: Release) -> dict[str, Mapping[str, Any]]:
    """The release's filtered receipt's rows that read a certificate whole, by path: the
    parents a recipe row may build on without a replay of their own."""
    path = chosen.path(FILTERED)
    if not path.is_file():
        return {}
    return {
        row["certificate"]: row for row in _read(path)["rows"] if not row["deleted_squares"]
    }


def recipe_decisions(
    chosen: Release, parents: Mapping[str, Mapping[str, Any]]
) -> list[dict[str, Any]]:
    """Each recipe row decided by the construction checker against its parent's replay
    (``parents``, by path), with the recipe's controls; a row it refuses keeps the reason."""
    found = []
    for row in recipe_claims(chosen):
        recipe = recipe_of(chosen, row)
        replayed = parents.get(row.path)
        # A parent with no replay is refused as not replayed, whatever its side.
        parent = (
            checker.parent_from_replay(replayed)
            if replayed is not None
            else checker.Parent(recipe.source_n, Fraction(0), row.path, recipe.parent_sha256)
        )
        try:
            decision = checker.decide(recipe, parent)
        except checker.RecipeRefusedError as error:
            found.append({"n": row.n, "verdict": "refused", "reason": str(error)})
            continue
        found.append(decision | {"controls": checker.controls(recipe, parent)})
    return found


def write_recipe_decisions(issues: Sequence[int | str], workers: int) -> dict[str, int]:
    """Write each chosen release's recipe decisions (`RECIPES`): every recipe parent that
    is not a replayed row of the release decided on both routes with its six controls
    (`decide_parent`), then every recipe row decided from its recipe (`recipe_decisions`).
    Returns each release's decided rows."""
    written: dict[str, int] = {}
    for chosen in [release(issue) for issue in issues]:
        custody(chosen)
        rows = recipe_claims(chosen)
        _require(rows, f"{chosen.label}: no recipe row in its window")
        replayed = _replayed_parents(chosen)
        needed = sorted(
            {(row.path, int((row.recipe or {})["source_n"])) for row in rows}
            - {(path, int(row["n"])) for path, row in replayed.items()}
        )
        with ProcessPoolExecutor(max_workers=workers) as pool:
            parents = list(pool.map(decide_parent, [(chosen.key, *job) for job in needed]))
        decisions = recipe_decisions(
            chosen, {**replayed, **{item["certificate"]: item for item in parents}}
        )
        _write(
            chosen.path(RECIPES),
            {
                "format": RECIPES_FORMAT,
                chosen.report_key: chosen.issue_url,
                "checker": "packing/devtools/construction_checker.py",
                "lemma": checker.LEMMA,
                "controls": list(checker.CONTROLS),
                "parents": parents,
                "rows": decisions,
            },
        )
        written[chosen.key] = sum(1 for item in decisions if item["verdict"] == "decided")
    return written


def recipe_problems(chosen: Release, *, replay: bool, workers: int) -> list[str]:
    """Where a release's recipe rows are not decided as its receipt says (`RECIPES`):
    each derived again from the stored parent replays, each decided with every control
    refused, and each parent replayed on both routes with its six controls refused; with
    ``replay`` the parents that are not rows are decided again."""
    rows = recipe_claims(chosen)
    path = chosen.path(RECIPES)
    if not rows:
        return (
            [f"{chosen.label}: recipe decisions with no recipe row"] if path.is_file() else []
        )
    if not path.is_file():
        return [f"{chosen.label}: {len(rows)} recipe rows and no recipe decisions"]
    receipt = _read(path)
    parents = {item["certificate"]: item for item in receipt["parents"]}
    problems = [
        f"{chosen.label}: the recipe parent {item['certificate']} is not verified with its "
        "six controls refused by both routes"
        for item in receipt["parents"]
        if not item["verified"]
        or len(item["controls"]) != len(base.CONTROLS)
        or not all(
            c["refused_by_sqpack"] and c["refused_by_independent"] for c in item["controls"]
        )
    ]
    problems += recipe_pin_problems(chosen, rows, receipt["parents"])
    if receipt["rows"] != recipe_decisions(chosen, {**_replayed_parents(chosen), **parents}):
        problems.append(f"{chosen.label}: the recipe decisions differ from their derivation")
    problems.extend(
        f"{chosen.label} n={item['n']}: the recipe is {item['verdict']}"
        + (f", {item['reason']}" if item.get("reason") else "")
        for item in receipt["rows"]
        if item["verdict"] != checker.DECIDED
        or not all(control["refused"] for control in item["controls"])
    )
    if replay and receipt["parents"]:
        jobs = [
            (chosen.key, item["certificate"], int(item["n"])) for item in receipt["parents"]
        ]
        with ProcessPoolExecutor(max_workers=workers) as pool:
            again = list(pool.map(decide_parent, jobs))
        problems.extend(
            f"{chosen.label}: the replay of the recipe parent {kept['certificate']} differs"
            for kept, fresh in zip(receipt["parents"], again, strict=True)
            if _stable(fresh) != _stable(kept)
        )
    return problems


def recipe_pin_problems(
    chosen: Release, rows: Sequence[Claim], parents: Sequence[Mapping[str, Any]]
) -> list[str]:
    """Where a recipe is not bound to the bytes the packet pins (#793's review A, A6): each
    declared recipe's parent digest must be the packet's pin for its parent, and each stored
    parent replay must have that pin and its certificate's header side (`certificate_side`),
    so a stale parent that agrees with its recipe is refused without ``--replay``."""
    pins = manifest(chosen)
    hosting = Hosting(chosen)
    problems = [
        f"{chosen.label} n={row.n}: the recipe's parent digest is not the packet's pin for "
        f"{row.path}"
        for row in rows
        if (row.recipe or {}).get("sha256") != pins.get(row.path)
    ]
    for item in parents:
        where = f"{chosen.label}: the recipe parent {item['certificate']}"
        if item["certificate_sha256"] != pins.get(item["certificate"]):
            problems.append(f"{where} is not the certificate the packet pins")
            continue
        try:
            side = certificate_side(chosen, item["certificate"], int(item["n"]), where, hosting)
        except ReplayError as error:
            problems.append(str(error))
            continue
        if Fraction(str(item["exact_side"])) != side:
            problems.append(f"{where}: its side is not its certificate's header's")
    return problems


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
    listed = [*decided_claims(chosen), *held_claims(chosen)]
    stated = recipe_first_commits(
        chosen, clone, [row for row in listed if row.recipe is not None]
    )
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
    hosting = Hosting(chosen)
    for row in listed:
        blob = (
            _pinned_blob(chosen, row, clone)
            if chosen.derived
            else blob_of(chosen, row.path, row.certificate_n, hosting)
        )
        commit = first[blob] if row.recipe is None else stated[row.n]
        item = {
            "n": row.n,
            "certificate": row.path,
            "blob": blob,
            "first_commit": commit,
            "committed": _utc(dates[commit]),
        }
        if row.recipe is not None:
            item["dated_by"] = chosen.index
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


def states_recipe(entry: object, row: Claim) -> bool:
    """Whether an index entry states a recipe row's recipe: a construction of the same kind,
    parent count, tiles, layers and capacity, on the parent the row declares by SHA-256, at
    the same exact bound, deleting as many squares."""
    recipe = row.recipe or {}
    if not isinstance(entry, Mapping) or entry.get("kind") != "construction":
        return False
    construction = entry.get("construction") or {}
    return (
        all(
            construction.get(key) == recipe.get(key)
            for key in ("kind", "source_n", "tiles_per_side", "layers", "capacity")
        )
        and entry.get("certificate_sha256") == recipe.get("sha256")
        and Fraction(str(entry.get("bound"))) == Fraction(str(recipe.get("bound")))
        and int(entry.get("deleted_squares") or 0) == row.deleted
    )


def recipe_first_commits(chosen: Release, clone: Path, rows: Sequence[Claim]) -> dict[int, str]:
    """The first commit of the retained commit's history whose index (`Release.index`)
    states each recipe row's recipe at its count (`states_recipe`). A recipe row has no
    file of its own, and its parent's file may be older than the recipe, so it is dated by
    its index (#793's review A, A8). Only the commits that change the index are read, oldest
    first, each version of it once."""
    if not rows:
        return {}
    commits = _git(
        clone, "log", "--reverse", "--format=%H", chosen.retained, "--", chosen.index
    ).split()
    found: dict[int, str] = {}
    for commit in commits:
        pending = [row for row in rows if row.n not in found]
        if not pending:
            break
        entries = json.loads(_git(clone, "show", f"{commit}:{chosen.index}"))[chosen.index_key]
        found |= {
            row.n: commit for row in pending if states_recipe(entries.get(str(row.n)), row)
        }
    missing = [row.n for row in rows if row.n not in found]
    _require(not missing, f"{chosen.label}: no commit's index states the recipe at {missing}")
    return found


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
    row = next(row for row in replayed_claims(chosen) if row.n == job[1])
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
    decided = {row.n for row in replayed_claims(chosen)}
    for n in counts:
        _require(n in decided, f"{chosen.label} n={n}: not a decided row")
    started = datetime.now(UTC)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(exhaustive_row, [(chosen.key, n) for n in counts]))
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


@functools.cache
def _goebel_program() -> Any:
    """The 15 October packet's exact Göbel comparison, loaded from its retained path."""
    spec = importlib.util.spec_from_file_location("goebel_beyond_horizon", base.GOEBEL_PROGRAM)
    if spec is None or spec.loader is None:
        raise ReplayError("the Göbel program is missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def goebel_receipt(chosen: Release, sides: Mapping[int, Fraction]) -> dict[str, Any]:
    """A release's decided sides against Göbel's classical constructions, exactly.

    A window frozen at 1024 (`Release.frozen`) keeps the 15 October packet's retained
    ``goebel_beyond_horizon.py``, read from its path unchanged, whose ``LIMIT`` of 1100
    covers it, so its receipt and its ``program`` field stay as written (#791's review A,
    A11). A window above reads the maintained module (`devtools.goebel_construction`),
    which proves every side it gives final, and writes `GOEBEL_FORMAT_V2`, naming it.
    """
    rows = [(row.n, sides[row.n], row.path) for row in decided_claims(chosen)]
    label = f"{chosen.described} at {chosen.pin[:8]}"
    if chosen.frozen:
        program = _goebel_program()
        _require(
            (chosen.decided_through or 0) <= program.LIMIT,
            "the Göbel program stops below the decided counts",
        )
        return {
            "format": GOEBEL_FORMAT,
            "program": base.GOEBEL_PROGRAM.relative_to(REPO).as_posix(),
            "families": (
                "Göbel squares, Göbel strips and corner-touching strips, with deletion"
            ),
            "comparison": program.compare(label, rows, program.families(program.LIMIT)),
        }
    try:
        comparison = goebel_construction.compare(label, rows)
    except goebel_construction.GoebelError as error:
        raise ReplayError(f"{chosen.label}: {error}") from error
    return {
        "format": GOEBEL_FORMAT_V2,
        "program": GOEBEL_MODULE,
        "families": goebel_construction.FAMILIES,
        "proof": (
            "each side is the least member at the count or above of a build the module "
            "proves final by the area bound, S^2 < B + 1 for a build to B"
        ),
        "comparison": comparison,
    }


def goebel() -> dict[str, dict[str, Any]]:
    """Write every release's Göbel receipt (`goebel_receipt`); return its tallies."""
    tallies: dict[str, dict[str, Any]] = {}
    for chosen in RELEASES.values():
        custody(chosen)
        receipt = goebel_receipt(chosen, decided_sides(chosen))
        _write(chosen.path(GOEBEL), receipt)
        result = receipt["comparison"]
        tallies[chosen.key] = {"rows": result["rows"], "tally": result["tally"]}
    return tallies


# --------------------------------------------------------------------------- claims record


def beyond_horizon_rows(
    chosen: Release, sides: Mapping[int, Fraction] | None = None
) -> dict[str, Any]:
    """The decided rows as the coverage register reads them, rebuilt; ``sides`` are the
    decided sides where the caller has read them (`decided_sides`).

    Each keeps the side the row records as ``offered_side``, the value a dated
    beyond-horizon row holds byte for byte: an `UP` release's print; for a `BINARY64`
    release, the side rounded up at 16 places, with the issue's print beside it
    (`recorded_side`). Each also keeps its certificate's exact header side and when the
    certificate was first committed. A decided row the walk does not record, as #719's 366,
    is no row, so the record leaves it out; the filtered receipt keeps its decision. The
    record's ``limit`` is the release's window's top, None where it has none, and a window
    that starts above the corpus says where (``decided_above``).
    """
    if sides is None:
        custody(chosen)
        sides = decided_sides(chosen)
    results = []
    unrecorded = {n for n, source in unrecorded_rows() if source in chosen.sources}
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
        if row.recipe is not None:
            result["recipe"] = dict(row.recipe)
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
        "limit": chosen.decided_through,
        "results": results,
    }
    if chosen.decided_above != reports.HORIZON:
        record["decided_above"] = chosen.decided_above
    if chosen.rounding != UP:
        record["issue_rounding"] = chosen.rounding
    if chosen.issue is None:
        record["published"] = chosen.reported
    return record


def split_records(chosen: Release, record: Mapping[str, Any]) -> dict[Path, dict[str, Any]]:
    """A release's beyond-horizon record as its claims records hold it, by path: the one
    record, or, for a release with a split (`Split`), the rows the split does not hold under
    the release's record and those it holds under the split's, each with the same header,
    so each coverage source's claims record prints exactly its rows."""
    if chosen.split is None:
        return {chosen.path(RECORD): dict(record)}
    held = chosen.split.counts
    own, split = chosen.records
    results = record["results"]
    return {
        own: {**record, "results": [row for row in results if row["n"] not in held]},
        split: {**record, "results": [row for row in results if row["n"] in held]},
    }


def claims_record() -> dict[str, int]:
    """Write each packet's beyond-horizon records and return each release's row count."""
    written: dict[str, int] = {}
    for chosen in RELEASES.values():
        record = beyond_horizon_rows(chosen)
        for path, part in split_records(chosen, record).items():
            _write(path, part)
        written[chosen.key] = len(record["results"])
    return written


# --------------------------------------------------------------------------- earlier reports


class Push(NamedTuple):
    """A push that made a watched repository's commits public after their committer time:
    every commit not reachable from ``before``, the public head until then, reached GitHub
    at ``pushed`` or later, in the push that moved the branch to ``head``. ``evidence`` says
    where the push is recorded."""

    before: str
    head: str
    pushed: str
    evidence: str


#: Watched repositories whose commits reached GitHub later than their committer times, each
#: push oldest first. A commit is a report from the push that made it public, not from its
#: commit (`publication_times`). Couzo's three commits after 7b6c87e were pushed at
#: 2026-10-21T22:56:37Z (`devtools.couzo_715_replay`). efef7d1 and fa6237e, committed at
#: 18:16:49Z and 18:59:39Z on 23 October, before Polkovskyi's f1ceee4 (20:34:13Z, reported
#: at 20:35:12Z), and 964ee2b were pushed at 23:38:42Z, after it (#769's review A, A7).
PUSHED_LATER: dict[str, tuple[Push, ...]] = {
    "franciscouzo/square-packing": (
        Push(
            "7b6c87e129cf80b5ff9847b90b47fd30b4563c54",
            "6b7391de820fd01f3ff6984e4a081e8c86845588",
            "2026-10-21T22:56:37Z",
            "GitHub's activity API (repos/franciscouzo/square-packing/activity): the push to "
            "refs/heads/master by franciscouzo at 2026-10-21T22:56:37Z, from 7b6c87e to "
            "6b7391d; devtools.couzo_715_replay",
        ),
        Push(
            "6b7391de820fd01f3ff6984e4a081e8c86845588",
            "964ee2bdf301d0c8912d956d4010f478dcbbd5ea",
            "2026-10-23T23:38:42Z",
            "GitHub's activity API (repos/franciscouzo/square-packing/activity), read "
            "2026-10-24: the push to refs/heads/master by franciscouzo at "
            "2026-10-23T23:38:42Z, from 6b7391d to 964ee2b, carrying efef7d1, fa6237e and "
            "964ee2b, 2 min 51 s after issue #763 (think-cnn7)",
        ),
        Push(
            "964ee2bdf301d0c8912d956d4010f478dcbbd5ea",
            "1c1715399709bc955e9b402947ab8b52bbacdfc3",
            "2026-10-24T06:10:44Z",
            "GitHub's activity API (repos/franciscouzo/square-packing/activity), read "
            "2026-10-24: the push to refs/heads/master by franciscouzo at "
            "2026-10-24T06:10:44Z, from 964ee2b to 1c17153, carrying 43f666c, 73eac5b and "
            "1c17153 (think-cncq)",
        ),
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


def publication_times(
    name: str, times: Mapping[str, str], reachable: Callable[[str], set[str]]
) -> dict[str, str]:
    """Each commit's publication time, from its committer time in ``times``: for each push
    `PUSHED_LATER` records for the repository ``name``, oldest first, a commit not reachable
    from the push's ``before`` (``reachable(before)``, every commit its history holds) is
    dated no earlier than the push. A commit is so dated by the first push that made it
    public, and one public before every recorded push keeps its committer time."""
    published = dict(times)
    for push in PUSHED_LATER.get(name, ()):
        public = reachable(push.before)
        published = {
            commit: (when if commit in public else max(when, push.pushed))
            for commit, when in published.items()
        }
    return published


def pushed_later_record() -> dict[str, list[dict[str, str]]]:
    """`PUSHED_LATER` as a receipt states it: each repository's pushes, oldest first."""
    return {
        name: [
            {"public_head": push.before, "head": push.head, "pushed": push.pushed}
            for push in pushes
        ]
        for name, pushes in PUSHED_LATER.items()
    }


def _dated_commits(name: str, clone: Path, until: str) -> list[tuple[str, str]]:
    """Every commit of a clone's ``HEAD`` history oldest first, each with the time it was
    published (`publication_times`): its committer time, or the later push `PUSHED_LATER`
    records; only those published before ``until``."""
    chain = _git(clone, "rev-list", "--reverse", "--topo-order", "HEAD").split()
    times = {
        commit: _utc(stamp)
        for commit, stamp in (
            line.split(" ", 1)
            for line in _git(clone, "log", "--format=%H %cI", "HEAD").splitlines()
        )
    }
    times = publication_times(
        name, times, lambda head: set(_git(clone, "rev-list", head).split())
    )
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
    ``counts`` the record has no result for, one above the window that no record holds
    yet, stands at the grid. Beyond the horizon a record read from
    `devtools.intake_ledger.GOEBEL_FROM` takes Göbel's construction too, from the
    maintained module, and refuses only a count whose side no build proves final."""
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
    the packet does not derive (above its window), from the release's hosted shard where it
    is hosted, else from the header of the file a clone of the source holds at the retained
    commit, refused unless it has the digest the packet pins."""
    record = _read(chosen.directory / reports.CLAIMS)
    stated = {item["n"]: Fraction(item["exact_side"]) for item in record["results"]}
    sides: dict[int, Fraction] = {}
    hosting = Hosting(chosen)
    for row in claims(chosen):
        if row.n in stated:
            sides[row.n] = stated[row.n]
            continue
        # Both branches read the certificate's header at its own count by one rule
        # (`header_side`, #793's review D, D6), and take the row's side from it as
        # `decided_sides` does (`claim_side`, review B, B2).
        where = f"{chosen.label} n={row.n}"
        if hosting.hosts(row.path):
            raw = hosting.read(row.path)
        else:
            _require(clone is not None, f"{where}: no clone to read it from")
            assert clone is not None
            blob = _pinned_blob(chosen, row, clone)
            raw = _blobs(clone, [blob])[blob]
        sides[row.n] = claim_side(row, header_side(raw, row.certificate_n, where))
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
        "pushed_later": pushed_later_record(),
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
    which the walk decides as restatements (think-fwa9), and above `FROZEN_THROUGH`, and
    #666's above it, which wait on their own walk (D1). A claim the start already holds is
    not walked again. The walk's rulings are `WALK_RULINGS`'. It transcribes the #719
    walk, frozen at 1024 (`tests/test_beyond_horizon_replay.py` holds the file to it).
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
        # By the constant, not #666's window, which a records slice lifts (#793's review
        # B, B1): this frozen walk read #666's claims above 1024.
        for row in claims(de_winter)
        if row.n > FROZEN_THROUGH and row.n in counts
    ]
    own = []
    for row in claims(chosen):
        side = Fraction(by_n[row.n]["release_side"])
        where = (
            f"facts/n-{row.n:03d}.yaml.gz in the {chosen.packet} packet, derived from "
            f"{row.path} at {chosen.retained[:8]} (its header)"
            if row.n <= FROZEN_THROUGH
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
    exact sides its packet's filtered receipt states, and its rows above `FROZEN_THROUGH`,
    at the side of the publication the earlier-publications receipt found its print to round
    up."""
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
        elif n > FROZEN_THROUGH and n in printed:
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
        "pushed_later": pushed_later_record(),
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


def source_history_path(chosen: Release, walk: Walk | None = None) -> Path:
    """Where a release's source-history receipt for ``walk`` is kept: `SOURCE_HISTORY` for
    its own walk, and ``receipts/source-history-WALK.json`` for the walk above 1024."""
    if walk is None or walk.name == chosen.walk:
        return chosen.path(SOURCE_HISTORY)
    return chosen.path(SOURCE_HISTORY.with_name(f"source-history-{walk.name}.json"))


def source_history(issue: int | str, clone: Path, walk: Walk | None = None) -> dict[str, Any]:
    """Every side a release's own repository published in a certificate file at the counts
    beyond the corpus a walk reaches, from a clone: its own walk by default, which reaches
    `HISTORY_COUNTS`.

    The repository is watched, so each certificate there is a publication from the first
    commit of the retained commit's history that holds its side. Only certificate files
    whose paths name a count the walk reaches are read (`_COUNT_NAMED`), so a blobless clone
    fetches no certificate outside it, and each file's header must state the
    count its path names. At the retained commit each count's certificate is listed with
    its Git blob, SHA-256 and exact side, the first commit that holds its side and the first
    that holds its blob, and is held to the release's index (``Release.index``, by default the
    source's manifest, `SOURCE_MANIFEST`): the path, digest and exact bound the index states
    for the count must be the file's. f1ceee4 left the manifest as the commit before it wrote
    it, so its release is held to ``certified_bounds.json``, the index it rewrote.

    Above 1024, where a release's certificates are hosted (`Release.hosted`), the files at
    the retained commit are read from the shards, each held to the Git blob the clone's tree
    names, so a blobless clone fetches only the earlier blobs at those paths; the first
    commits come from the clone's trees.

    The source's decimal poses and its own indexes are not read. At #732's source no
    ``verified`` or certified bound either index states at 325 to 1024, the lanes the history
    scan reads of an index (`INDEXES`), is below the start and every side walked there, at
    any commit that holds it; only ``3285fac``'s ``reported`` lane is, where it restates the
    Kingbird catalogue's 14-place prints (the packet README).
    """
    chosen = release(issue)
    walk = walk or walk_of(chosen)

    def wanted(n: int | None) -> bool:
        return n is not None and n > reports.HORIZON and walk.reaches(n)

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
            if n is None or not wanted(n):
                continue
            blob = meta.split()[2]
            first.setdefault((blob, path), commit)
            if commit == chosen.retained:
                at_pin.setdefault(n, []).append((path, blob))
    hosting = Hosting(chosen)
    hosted = {
        blob: path for items in at_pin.values() for path, blob in items if hosting.hosts(path)
    }
    texts = _blobs(clone, sorted({blob for blob, _ in first} - set(hosted)))
    for blob, path in hosted.items():
        raw = hosting.read(path)
        _require(git_blob(raw) == blob, f"{path}: the hosted bytes are not the clone's blob")
        texts[blob] = raw
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
    (listed,) = _git(clone, "ls-tree", chosen.retained, "--", chosen.index).splitlines()
    manifest_blob = listed.split("\t", 1)[0].split()[2]
    manifest_raw = _blobs(clone, [manifest_blob])[manifest_blob]
    stated = {
        key: entry
        for key, entry in json.loads(manifest_raw)[chosen.index_key].items()
        if isinstance(entry, Mapping) and entry.get("certificate")
    }
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
            f"n={n}: {path} is not the certificate, digest and bound {chosen.index} states",
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
    in_range = sorted(int(key) for key in stated if wanted(int(key)))
    _require(
        in_range == sorted(at_pin),
        f"{chosen.index} states other counts {walk.reach} than the commit holds",
    )
    return {
        "format": SOURCE_HISTORY_FORMAT,
        "source": chosen.source_url,
        "retained_commit": chosen.retained,
        "history_commits": len(chain),
        "counts": [max(walk.above, reports.HORIZON) + 1, walk.through],
        "manifest": chosen.index,
        "manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "at_commit": pin_rows,
        "publications": [
            {"n": n, "side": legacy.literal(side), **item}
            for (n, side), item in sorted(
                published.items(), key=lambda pair: (pair[0][0], pair[1]["published"])
            )
        ],
    }


def write_source_history(
    issue: int | str, clone: Path, walk: Walk | None = None
) -> dict[str, int]:
    """Write a release's source-history receipt for a walk (`source_history_path`); return
    its counts at the commit and its publications."""
    record = source_history(issue, clone, walk)
    _write(source_history_path(release(issue), walk), record)
    return {"at_commit": len(record["at_commit"]), "publications": len(record["publications"])}


def _least_highs(starts: Mapping[int, Sequence[Any]]) -> dict[int, Fraction]:
    """The least high end of a member of each count's start (`_start_sides`).

    A side at or above that end is at or above a member of the start, every number of which
    it is at least, so the walk never records it and it never joins the standing side; only
    a side strictly below it can change a verdict. A start of one member, as every walk's
    before 23 October 2026, has the same end either way; one read from that day may hold
    Göbel's construction beside the row (`devtools.intake_ledger.GOEBEL_FROM`)."""
    return {n: min(member.span.high for member in members) for n, members in starts.items()}


def _start_sides(
    walk: Walk, read_at_main: str, counts: Iterable[int], read_on: str = ""
) -> dict[int, list[Any]]:
    """Each count's start in ``walk`` as the ledger's sides (`devtools.intake_ledger.Side`):
    from its frozen ``starts.yaml``, or, before ``gather`` has frozen one, from the
    checkout's records for a ledger read on ``read_on``, which must then be those of
    ``read_at_main`` (`devtools.intake_ledger.tree_members`)."""
    from devtools import intake_ledger  # noqa: PLC0415

    wanted = sorted(set(counts))
    if (walk.directory / intake_ledger.STARTS).is_file():
        starts = intake_ledger.load_starts(walk.directory, read_at_main)
        missing = [n for n in wanted if n not in starts]
        _require(not missing, f"{walk.name}: the frozen starts have no count {missing[:5]}")
        return {n: list(starts[n]) for n in wanted}
    members = intake_ledger.tree_members(wanted, read_on=read_on)
    return {n: [intake_ledger.side_of(member) for member in members[n]] for n in wanted}


#: Who holds the #732 source's own publications, as the ledgers print it.
MISHAPOLK_HOLDER = "Mykhailo Polkovskyi"


def release_walk_sources(
    issue: int | str, read_on: str, walk: Walk | None = None
) -> dict[str, Any]:
    """The ``sources.yaml`` of a release whose walk reads its own source's history (#732).

    ``walk`` is the release's own walk by default (`walk_of`). The reports, at each count the
    release claims that the walk reaches (`Walk.reaches`):

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
    (`_least_highs`): at or above it, it could never be recorded or change a verdict. The
    start is frozen at the walk's ``read_at_main`` (`WALK_READ_AT_MAIN`).

    A later release a comment reports (`Release.comment`) is dated by that comment, and with
    ``changed_only`` its claims are only the certificates its commit adds or changes. Where
    it names ``later_reads``, each of those commits is a report of its own, dated by its
    push, at every count it publishes a side (`later_commits`, ``receipts/later-commits.json``);
    at those counts in the corpus the earlier reports the retained ledgers walked, and those
    whose import has not reached ``main`` (`WALK_PENDING_REPORTS`), are walked where they are
    strictly below the start (`ledger_reports`).
    """
    chosen = release(issue)
    walk = walk or walk_of(chosen)
    read_at_main = WALK_READ_AT_MAIN[walk.name]
    history = _read(source_history_path(chosen, walk))
    own = {
        row["n"]: row
        for row in history["at_commit"]
        if walk.reaches(row["n"])
        and (not chosen.changed_only or row["blob_first_commit"] == chosen.retained)
    }
    later = later_publications(chosen, walk)
    starts = _start_sides(walk, read_at_main, [*own, *later], read_on)
    highs = _least_highs(starts)
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
    if chosen.comment is None:
        what = (
            f"The {len(claims)} certificates the source holds at "
            f"{chosen.retained[:8]} beyond the corpus {walk.reach}, which its "
            f"manifest ({SOURCE_MANIFEST}, pinned by the SHA-256 the issue states) lists "
            "as the issue's claims there, each at its header's exact side and dated by "
            "the issue; first_committed is the first commit of the source's history "
            "that published the side."
        )
    else:
        what = (
            f"The {len(claims)} certificates {chosen.retained[:8]} adds or changes beyond "
            f"the corpus {walk.reach}, which the comment reports, each held to the "
            f"path, SHA-256 and exact bound the release's index ({chosen.index}) states and "
            "read at its header's exact side, dated by the comment; first_committed is the "
            "first commit of the source's history that published the side."
        )
    head: dict[str, Any] = {"report": chosen.label, "issue": chosen.issue}
    if chosen.comment is not None:
        head["comment"] = chosen.comment
    reports_list: list[dict[str, Any]] = [
        head
        | {
            "holders": chosen.holders,
            "bead": chosen.bead,
            "claims": claims,
            "note": what + held_sentence(walk, chosen.label),
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
    after = later_reports(chosen, later, walk)
    reports_list += after
    if later:
        inside = {n: highs[n] for n in _open_against(after, starts) if n <= reports.HORIZON}
        prints = {
            n: {read for member in starts[n] for read in member.record_prints} for n in inside
        }
        before = min(pushed for _, pushed in chosen.later_reads)
        reports_list += ledger_reports(walk, inside, before, prints)
    labels = [item["report"] for item in reports_list + publications]
    twice = sorted({label for label in labels if labels.count(label) > 1})
    _require(not twice, f"{walk.name}: two reports share a label: {twice}")
    return {
        "format": "intake-ledger-sources-v1",
        "read_at_main": read_at_main,
        "read_on": read_on,
        "rule": RULE,
        "lanes": [],
        "reports": reports_list + publications,
        "rulings": WALK_RULINGS[walk.name],
    }


LATER_COMMITS = Path("receipts/later-commits.json")
LATER_COMMITS_FORMAT = "beyond-horizon-later-commits-v1"


def later_commits(issue: int | str, clone: Path) -> dict[str, Any]:
    """Every side the commits a release names past its pin (``later_reads``) publish at a
    count its walk reaches (`Walk.reaches`; to 1024 for every walk frozen there, so
    f1ceee4's receipt keeps its ``"limit": 1024``), from a clone: each certificate file whose
    path names a count
    (`_COUNT_NAMED`) that the commit adds or changes, at its header's side, and each bound an
    index (`INDEXES`) states at a count where the commit changes it.

    Each commit must be the next of the release's history: the pin's child, then each the
    child of the one before. Each keeps its committer time and the push the release declares
    for it, which dates it as a report; only the files the commit changes are read.
    """
    chosen = release(issue)
    _require(chosen.later_reads, f"{chosen.label}: declares no later commits")
    walk = walk_of(chosen)
    parent = chosen.retained
    commits = []
    for commit, pushed in chosen.later_reads:
        (line,) = _git(clone, "log", "-1", "--format=%P %cI %s", commit).splitlines()
        parents, stamp, subject = line.split(" ", 2)
        _require(parents == parent, f"{commit[:8]}: not the child of {parent[:8]}")
        changed = _git(clone, "diff-tree", "-r", "--no-commit-id", parent, commit).splitlines()
        wanted: list[tuple[int, str, str, str]] = []
        indexes: dict[str, tuple[str, str]] = {}
        for entry in changed:
            meta, _, path = entry.partition("\t")
            _old_mode, _new_mode, old, new, status = meta.lstrip(":").split()
            n = named_count(path)
            if n is not None and walk.reaches(n) and status in ("A", "M"):
                wanted.append((n, path, new, "certificate"))
            elif path in INDEXES and status == "M":
                indexes[path] = (old, new)
        texts = _blobs(
            clone,
            sorted(
                {blob for _, _, blob, _ in wanted}
                | {b for pair in indexes.values() for b in pair}
            ),
        )
        found = []
        for n, path, blob, _kind in sorted(wanted):
            header = _header(texts[blob])
            _require(
                header is not None and header[0] == n,
                f"{path} ({blob[:8]}): its header does not state the count its name gives",
            )
            assert header is not None
            found.append(
                {
                    "n": n,
                    "kind": "certificate",
                    "path": path,
                    "blob": blob,
                    "sha256": hashlib.sha256(texts[blob]).hexdigest(),
                    "side": legacy.literal(header[1]),
                }
            )
        for path, (old, new) in sorted(indexes.items()):
            before = json.loads(texts[old]).get("entries") or {}
            after = json.loads(texts[new]).get("entries") or {}

            def bound(entries: Mapping[str, Any], key: str, keys: tuple[str, ...]) -> Any:
                value: Any = entries.get(key)
                for part in keys:
                    value = value.get(part) if isinstance(value, dict) else None
                return value

            for key in sorted(after, key=lambda item: int(item) if item.isdigit() else 0):
                if not key.isdigit() or not walk.reaches(int(key)):
                    continue
                stated = bound(after, key, INDEXES[path])
                if stated is None or stated == bound(before, key, INDEXES[path]):
                    continue
                found.append(
                    {
                        "n": int(key),
                        "kind": "index",
                        "path": path,
                        "blob": new,
                        "side": legacy.literal(Fraction(str(stated))),
                    }
                )
        commits.append(
            {
                "commit": commit,
                "parent": parent,
                "committed": _utc(stamp),
                "pushed": pushed,
                "subject": subject,
                "changed_paths": len(changed),
                "publications": sorted(found, key=lambda item: (item["n"], item["path"])),
            }
        )
        parent = commit
    return {
        "format": LATER_COMMITS_FORMAT,
        "source": chosen.source_url,
        "retained_commit": chosen.retained,
        "limit": walk.through,
        "indexes": {path: ".".join(keys) for path, keys in INDEXES.items()},
        "commits": commits,
    }


def write_later_commits(issue: int | str, clone: Path) -> dict[str, int]:
    """Write a release's later-commits receipt; return each commit's publications."""
    record = later_commits(issue, clone)
    _write(release(issue).path(LATER_COMMITS), record)
    return {item["commit"][:7]: len(item["publications"]) for item in record["commits"]}


# --------------------------------------------------------------------------- one push


#: A walk whose releases read one push commit by commit (#795's review A, A1): every
#: certificate header and index bound the push's commits add or change at the walk's counts,
#: and each commit's least new side at each count below the frozen start, its claim there.
PUSH_PUBLICATIONS = Path("receipts/push/push-publications.json")
PUSH_FORMAT = "beyond-horizon-push-publications-v1"
#: The holder of a push claim the index credits to the publisher: his own side.
PUBLISHER = "publisher"
#: The holder of a push claim the index credits to neither the publisher nor a notebook
#: run: another author's side, which no release of the push holds, so the walk refuses to
#: record it (`release_at`, `chain_problems`) and may only rule it out (#795's review B, B3).
OTHER_AUTHOR = "other"
#: The claims of the push's commits at the notebook rows' counts, as #795's review A counted
#: them (A1): its 99 rows, the 86 sides of efef7d1 and fa6237e the walk records before them,
#: and 5 of efef7d1's that restate earlier publications.
PUSH_CONTROLS = {"efef7d1": 40, "fa6237e": 90, "964ee2b": 60}
#: How a certificate path names its count in Couzo's repository.
_PUSH_NAMED = re.compile(r"certificates/(?:best/|extended/)?n([1-9][0-9]*)\.cert")


def _cert_headers(clone: Path, blobs: Sequence[str]) -> dict[str, tuple[int, Fraction] | None]:
    """Each certificate blob's count and side (`_header`), streamed through one
    ``git cat-file --batch`` so that no file is kept whole."""
    found: dict[str, tuple[int, Fraction] | None] = {}
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
            found[blob] = _header(process.stdout.read(size))
            process.stdout.read(1)
        process.stdin.close()
    return found


def _push_of(chosen: Release) -> Push:
    """The recorded push (`PUSHED_LATER`) that made a release's retained commit public."""
    pushes = PUSHED_LATER.get(repository_of(chosen.source_url), ())
    found = [push for push in pushes if push.head == chosen.retained]
    _require(
        len(found) == 1, f"{chosen.label}: no recorded push made {chosen.retained[:8]} public"
    )
    return found[0]


def _push_counts(chosen: Release) -> list[int]:
    """The counts a push walk reads: those its packet's claim map lists as ``others``."""
    return sorted(int(item["n"]) for item in _read(chosen.directory / CLAIM_MAP)["others"])


def _notebook_runs(chosen: Release) -> dict[str, dict[str, Any]]:
    """Each notebook credit the claim map's ``others`` state, with its notebook: how a push
    claim's credit names its notebook run."""
    found: dict[str, dict[str, Any]] = {}
    for item in _read(chosen.directory / CLAIM_MAP)["others"]:
        known = found.setdefault(str(item["credit"]), dict(item["notebook"]))
        _require(known["run"] == item["notebook"]["run"], f"{item['credit']}: two runs")
    return found


def _push_holder(credit: str, notebook: Mapping[str, Any] | None) -> str:
    """Whose a push claim is, by the credit the index states at its commit: the notebook
    run it names, the publisher where it names him (`couzo_763_claims.is_own`), else
    another author (`OTHER_AUTHOR`)."""
    if notebook:
        return str(notebook["run"])
    return PUBLISHER if claims_763.is_own(credit) else OTHER_AUTHOR


def _push_statements(
    clone: Path,
    push: Push,
    *,
    retained: str,
    counts: Sequence[int],
    highs: Mapping[int, Fraction],
    earlier: frozenset[tuple[int, Fraction]],
) -> tuple[list[dict[str, Any]], list[tuple[int, str, int, Fraction, list[dict[str, Any]]]]]:
    """A push read commit by commit at ``counts`` (#795's review A, A1): each commit's
    statements, and each commit's least new side at each count strictly below ``highs``.

    A commit's statements are what it adds or changes: each certificate file's header at a
    walked count, wherever it lies (``best/``, ``parents/``, a root certificate), and each
    bound an index (`INDEXES`) states at a walked count where the commit changes it, as
    `first_publications` reads a history and `later_commits` a commit. A side is the
    publication of the first commit of the push that states it, and none ``earlier`` holds
    is one. The push's commits must be a chain, each the child of the one before, ending at
    ``retained``; the clone must hold their blobs (a blobless clone fetches each). Returns
    each commit's record and, in commit order, ``(order, commit, n, side, statements)`` for
    each commit's least new side at each count, with the statements that give it."""
    commits = _git(
        clone, "rev-list", "--reverse", "--topo-order", f"{push.before}..{push.head}"
    )
    chain = commits.split()
    _require(chain and chain[-1] == retained, "the push does not end at the retained commit")
    parent = push.before
    read: list[dict[str, Any]] = []
    statements: list[tuple[int, int, Fraction, dict[str, Any]]] = []
    for order, commit in enumerate(chain):
        (line,) = _git(clone, "log", "-1", "--format=%P %cI %s", commit).splitlines()
        parents, stamp, subject = line.split(" ", 2)
        _require(parents == parent, f"{commit[:8]}: not the child of {parent[:8]}")
        changed = _git(
            clone, "diff-tree", "-r", "--no-commit-id", "--no-renames", parent, commit
        ).splitlines()
        certs: list[tuple[str, str]] = []
        indexes: dict[str, tuple[str, str]] = {}
        for entry in changed:
            meta, _, path = entry.partition("\t")
            _old_mode, _new_mode, old, new, status = meta.lstrip(":").split()
            if status in ("A", "M") and path.endswith(".cert"):
                certs.append((path, new))
            elif path in INDEXES and status == "M":
                indexes[path] = (old, new)
        headers = _cert_headers(clone, sorted({blob for _, blob in certs}))
        found: list[dict[str, Any]] = []
        for path, blob in sorted(certs):
            header = headers[blob]
            if header is None or header[0] not in highs:
                continue
            named = _PUSH_NAMED.fullmatch(path)
            _require(
                named is None or int(named[1]) == header[0],
                f"{path} ({blob[:8]}): its header does not state the count its name gives",
            )
            found.append(
                {"n": header[0], "kind": "certificate", "path": path, "blob": blob}
                | {"side": legacy.literal(header[1])}
            )
        texts = _blobs(clone, sorted({blob for pair in indexes.values() for blob in pair}))
        for path, (old, new) in sorted(indexes.items()):
            before = json.loads(texts[old]).get("entries") or {}
            after = json.loads(texts[new]).get("entries") or {}
            for n in counts:
                stated, was = after.get(str(n)), before.get(str(n))
                for part in INDEXES[path]:
                    stated = stated.get(part) if isinstance(stated, dict) else None
                    was = was.get(part) if isinstance(was, dict) else None
                if stated is None or stated == was:
                    continue
                item = {"n": n, "kind": "index", "path": path, "blob": new}
                item["side"] = legacy.literal(Fraction(str(stated)))
                if path == "certified_bounds.json":
                    entry = after[str(n)]
                    item |= {
                        "index_kind": entry.get("kind", ""),
                        "credit": entry.get("credit", ""),
                    }
                found.append(item)
        statements.extend(
            (order, item["n"], Fraction(item["side"]), item | {"commit": commit})
            for item in found
        )
        read.append(
            {
                "commit": commit,
                "parent": parent,
                "committed": _utc(stamp),
                "subject": subject,
                "changed_paths": len(changed),
                "publications": sorted(found, key=lambda item: (item["n"], item["path"])),
            }
        )
        parent = commit
    first: dict[tuple[int, Fraction], int] = {}
    for order, n, side, _ in statements:
        first[n, side] = min(order, first.get((n, side), order))
    least: list[tuple[int, str, int, Fraction, list[dict[str, Any]]]] = []
    for order, commit in enumerate(chain):
        mine = [
            (n, side, item)
            for at, n, side, item in statements
            if at == order
            and first[n, side] == order
            and (n, side) not in earlier
            and side < highs[n]
        ]
        for n in sorted({n for n, _, _ in mine}):
            side = min(side for m, side, _ in mine if m == n)
            items = [item for m, s, item in mine if m == n and s == side]
            least.append((order, commit, n, side, items))
    return read, least


def _pin_files(clone: Path, retained: str) -> dict[str, list[str]]:
    """Every certificate path the retained commit holds, by its Git blob."""
    at_pin: dict[str, list[str]] = {}
    for line in _git(clone, "ls-tree", "-r", retained, "certificates").splitlines():
        at_pin.setdefault(line.split()[2], []).append(line.partition("\t")[2])
    return at_pin


def _files_of(items: Sequence[Mapping[str, Any]], at_pin: Mapping[str, list[str]]) -> list[str]:
    """The retained commit's certificates that hold a statement's blob, ``best/`` first."""
    return sorted(
        {
            path
            for item in items
            if item["kind"] == "certificate"
            for path in at_pin.get(item["blob"], ())
        },
        key=lambda path: (not path.startswith("certificates/best/"), path),
    )


def push_publications(issue: int | str, clone: Path) -> dict[str, Any]:
    """Every side the push that made a release's retained commit public states at its walk's
    counts, commit by commit, and each commit's claim at each count (#795's review A, A1).

    The push is read by `_push_statements` at the counts of the claim map's ``others``. A
    commit's claim at a count is its least new side strictly below the count's frozen
    start, one claim a report (#722's review A, A2), read from a certificate the retained
    commit holds at exactly that blob, under the same path or another (``parents/`` keeps
    every certificate a later commit replaced). Its credit is the one
    ``certified_bounds.json`` states there at that commit, and its holder by that credit
    (`_push_holder`): the notebook run it names in the claim map's ``others``, the publisher
    where it names him, else another author, whom no release holds (#795's review B, B3).
    """
    chosen = release(issue)
    walk = walk_of(chosen)
    push = _push_of(chosen)
    counts = _push_counts(chosen)
    highs = _least_highs(_start_sides(walk, WALK_READ_AT_MAIN[walk.name], counts))
    runs = _notebook_runs(chosen)
    read, least = _push_statements(
        clone,
        push,
        retained=chosen.retained,
        counts=counts,
        highs=highs,
        earlier=claims_763.earlier_sides(),
    )
    at_pin = _pin_files(clone, chosen.retained)
    claims: list[dict[str, Any]] = []
    for _order, commit, n, side, items in least:
        files = _files_of(items, at_pin)
        _require(
            bool(files),
            f"{commit[:8]} n={n}: no certificate the retained commit holds states its side",
        )
        stated = next((item for item in items if item.get("credit") is not None), None)
        credit = str(stated["credit"]) if stated else ""
        notebook = runs.get(credit)
        claims.append(
            {
                "n": n,
                "commit": commit,
                "kind": "certificate",
                "certificate": files[0],
                "exact": legacy.literal(side),
                "deleted_squares": 0,
                "index_kind": str(stated["index_kind"]) if stated else "",
                "credit": credit,
                "holder": _push_holder(credit, notebook),
            }
            | ({"notebook": notebook} if notebook else {})
        )
    found_counts = Counter(item["commit"][:7] for item in claims)
    _require(
        dict(found_counts) == PUSH_CONTROLS,
        f"the push's claims are {dict(found_counts)}, not {PUSH_CONTROLS}",
    )
    # The push's last claim at each count is the claim map's row there (`couzo_763_claims`).
    last = {item["n"]: item for item in claims}
    for item in _read(chosen.directory / CLAIM_MAP)["others"]:
        own = last[int(item["n"])]
        _require(
            Fraction(own["exact"]) == Fraction(item["exact"])
            and own["certificate"] == item.get("recipe_certificate", item["certificate"]),
            f"n={item['n']}: the push's last claim is not the claim map's row",
        )
    return {
        "format": PUSH_FORMAT,
        "source": chosen.source_url,
        "retained_commit": chosen.retained,
        "push": {"before": push.before, "head": push.head, "pushed": push.pushed},
        "walk": walk.name,
        "starts_read_at_main": WALK_READ_AT_MAIN[walk.name],
        "counts": counts,
        "indexes": {path: ".".join(keys) for path, keys in INDEXES.items()},
        "commits": read,
        "claims": claims,
    }


def write_push_publications(issue: int | str, clone: Path) -> dict[str, int]:
    """Write a push walk's receipt (`push_publications`); return each commit's claims."""
    record = push_publications(issue, clone)
    _write(release(issue).directory / PUSH_PUBLICATIONS, record)
    return dict(Counter(item["commit"][:7] for item in record["claims"]))


def later_publications(
    chosen: Release, walk: Walk | None = None
) -> dict[int, list[dict[str, Any]]]:
    """A release's later commits' publications (`later_commits`), by count, each with its
    commit and push; none for a release that names no later commits. The receipt must
    cover every count ``walk`` reaches (its own walk by default): one written to 1024 is
    refused for a walk above it, rather than passing over every later publication there
    (#793's review B, B4)."""
    if not chosen.later_reads:
        return {}
    walk = walk or walk_of(chosen)
    record = _read(chosen.path(LATER_COMMITS))
    _require(
        [(item["commit"], item["pushed"]) for item in record["commits"]]
        == list(chosen.later_reads),
        f"{chosen.label}: the later-commits receipt names other commits",
    )
    _require("limit" in record, f"{chosen.label}: the later-commits receipt states no limit")
    limit = record["limit"]
    _require(
        limit is None or (walk.through is not None and limit >= walk.through),
        f"{chosen.label}: the later-commits receipt reads to {limit}, and {walk.name} "
        f"reaches {walk.reach}",
    )
    repository = repository_of(chosen.source_url)
    found: dict[int, list[dict[str, Any]]] = {}
    for item in record["commits"]:
        for publication in item["publications"]:
            found.setdefault(int(publication["n"]), []).append(
                publication
                | {
                    "repository": repository,
                    "commit": item["commit"],
                    "published": item["pushed"],
                }
            )
    return found


def later_reports(
    chosen: Release, later: Mapping[int, Sequence[Mapping[str, Any]]], walk: Walk
) -> list[dict[str, Any]]:
    """Each later commit's publications as a report of its own, dated by its push, at the
    least side it states at each count (#722's review A, A2)."""
    by_commit: dict[str, list[Mapping[str, Any]]] = {}
    for items in later.values():
        for item in items:
            by_commit.setdefault(str(item["commit"]), []).append(item)
    repository = repository_of(chosen.source_url)
    decided = later_relations(walk)
    found = []
    for commit, pushed in chosen.later_reads:
        items = by_commit.get(commit, [])
        if not items:
            continue
        label = f"{repository}@{commit[:7]}"
        claims = _least_claims(items)
        for claim in claims:
            relations = decided.get((label, int(claim["n"])))
            if relations:
                claim["record_relations"] = relations
        found.append(
            {
                "report": label,
                "url": f"{chosen.source_url}/tree/{commit}",
                "reported_at": pushed,
                "holders": chosen.holders,
                "bead": chosen.bead,
                "claims": claims,
                "note": (
                    f"A commit of the {chosen.label} source after the commit the comment "
                    "reports, which no issue reports: the repository is watched, so it is a "
                    "report from the push that made it public, which the repository's "
                    "activity log dates. Transcribed from the "
                    f"{chosen.packet} packet's {LATER_COMMITS.as_posix()} at every count "
                    f"{_to(walk)} where it adds or changes a certificate or an index's bound, "
                    "at the least side it states there." + held_sentence(walk, label)
                ),
            }
        )
    return found


def _to(walk: Walk) -> str:
    """The counts a walk reaches as a later commit's note says them: ``to 1024``."""
    return f"above {walk.above}" if walk.through is None else f"to {walk.through}"


def _open_against(
    after: Sequence[Mapping[str, Any]], starts: Mapping[int, Sequence[Any]]
) -> set[int]:
    """The counts where the start alone does not decide a later commit's claim against the
    record: at no member is it above or equal, under the record relations its decided
    comparisons give it (`later_relations`). Only there can an earlier report change its
    verdict, so only there are the earlier reports walked (`ledger_reports`)."""
    from devtools import intake_ledger  # noqa: PLC0415

    found: set[int] = set()
    for report in after:
        entry = cast("Any", {**report, "kind": "publication"})
        for claim in report["claims"]:
            side = intake_ledger.entry_side(entry, claim)
            relations = {
                intake_ledger.compare(side, member) for member in starts[int(claim["n"])]
            }
            if not relations & {intake_ledger.ABOVE, intake_ledger.EQUAL}:
                found.add(int(claim["n"]))
    return found


#: Reports a release walk takes whose own import has not reached ``main``, so that no
#: retained ledger walked them: #755, Amund Kristiansen's s(303), which pull request #757
#: imports (think-tqb5), reported before 7e82c64's 303.
WALK_PENDING_REPORTS: dict[str, tuple[dict[str, Any], ...]] = {
    ISSUE_732_F1: (
        {
            "report": "#755",
            "issue": 755,
            "holders": "Amund Kristiansen",
            "bead": "think-tqb5",
            "claims": [
                {
                    "n": 303,
                    "printed": "17.909762327476",
                    "rounding": "up",
                    "exact": "223872029093440709529093216833/12500000000000000000000000000",
                    "exact_from": (
                        "the certificate side issue 755's table states for s303_amund.cert "
                        "(gist amundsk/78f9f0e7b4669f2f509a281845081768 at 511f56bf, SHA-256 "
                        "9ec01059b35cc983cb28a1bb33bd215a2717228f7efd182e1724de6b22dc511b), "
                        "whose import, pull request 757 (think-tqb5), is not on main"
                    ),
                }
            ],
            "note": (
                "Issue 755's one claim, transcribed from the issue's table: its import has "
                "not reached main, so no retained ledger walks it, and it was reported before "
                "the later commit's 303."
            ),
        },
    ),
}
#: The fields of an earlier ledger's claim a release walk keeps (`ledger_reports`), beside
#: the record relations that still read a member of the walk's start.
_LEDGER_CLAIM_FIELDS = (
    "n",
    "printed",
    "rounding",
    "exact",
    "exact_from",
    "first_committed",
    "reported_at",
)


def ledger_reports(
    walk: Walk,
    highs: Mapping[int, Fraction],
    before: str,
    prints: Mapping[int, set[tuple[str, str, str]]],
) -> list[dict[str, Any]]:
    """The earlier reports at counts in the corpus a release walk takes beside its later
    commits: every report a retained report-order ledger walked at one of ``highs``'s counts
    before ``before``, with each claim strictly below the count's start (``highs``, as
    `_least_highs` reads it), and the walk's reports whose import has not reached ``main``
    (`WALK_PENDING_REPORTS`). Where two ledgers transcribe a report at a count, the one
    read last stands. A claim keeps its print, rounding, exact side and times
    (`_LEDGER_CLAIM_FIELDS`), and those of the record relations its ledger froze that still
    read a lane or entry of the start as the case records print it now (``prints``, each
    member's `devtools.intake_ledger.Side.record_prints`); the others read another
    ``main``'s lanes and would decide nothing."""
    from devtools import intake_ledger  # noqa: PLC0415

    def low(claim: Mapping[str, Any]) -> Fraction:
        if claim.get("exact"):
            return intake_ledger.number(str(claim["exact"]))
        return intake_ledger.printed_side(str(claim["printed"]), str(claim["rounding"])).low

    chosen: dict[
        tuple[str, int], tuple[tuple[str, str], Mapping[str, Any], dict[str, Any]]
    ] = {}
    for directory in sorted(INTAKE.glob("upper-bounds-*")):
        path = directory / intake_ledger.LEDGER
        if directory.name == walk.name or not path.is_file():
            continue
        ledger = safe_load(path.read_text(encoding="utf-8"))
        order = (str(ledger["read_on"]), directory.name)
        for report in ledger["reports"]:
            if str(report["reported_at"]) >= before:
                continue
            for claim in report["claims"]:
                n = int(claim["n"])
                if n not in highs or low(claim) >= highs[n]:
                    continue
                kept = {key: claim[key] for key in _LEDGER_CLAIM_FIELDS if key in claim}
                relations = [
                    dict(relation)
                    for relation in claim.get("record_relations") or []
                    if (relation["lane"], relation["value"], relation["exact_form"])
                    in prints.get(n, set())
                ]
                if relations:
                    kept["record_relations"] = relations
                key = (str(report["report"]), n)
                if key not in chosen or order > chosen[key][0]:
                    chosen[key] = (order, report, kept)
    grouped: dict[str, list[tuple[tuple[str, str], Mapping[str, Any], dict[str, Any]]]] = {}
    for (label, _n), item in sorted(chosen.items()):
        grouped.setdefault(label, []).append(item)
    found: list[dict[str, Any]] = []
    for label, items in sorted(
        grouped.items(), key=lambda pair: (str(pair[1][0][1]["reported_at"]), pair[0])
    ):
        report = max(items, key=lambda item: item[0])[1]
        url = str(report["url"])
        entry: dict[str, Any] = {"report": label}
        if report["kind"] == "pull-request":
            entry["pull"] = int(url.rstrip("/").rsplit("/", 1)[1])
        elif report["kind"] in ("issue", "comment"):
            match = re.fullmatch(
                r"https://github\.com/jlevy/squares/issues/(\d+)(?:#issuecomment-(\d+))?", url
            )
            _require(match is not None, f"{label}: {url} is not an issue or its comment")
            assert match is not None
            entry["issue"] = int(match[1])
            if report["kind"] == "comment":
                entry["comment"] = int(match[2])
        else:
            entry |= {"url": url, "reported_at": report["reported_at"]}
        ledgers = sorted({order[1] for order, _, _ in items})
        entry |= {
            "holders": report["holders"],
            "bead": report.get("bead", ""),
            "claims": [claim for _, _, claim in sorted(items, key=lambda item: item[2]["n"])],
            "note": (
                "An earlier report at counts in the corpus where a later commit of the source "
                "publishes a side, transcribed from the report-order "
                + ("ledger " if len(ledgers) == 1 else "ledgers ")
                + _listing([f"campaign/issue-intake/{name}" for name in ledgers])
                + " at each count where its claim is strictly below the start, with its print, "
                "rounding, exact side and times, and those of the record relations that "
                "ledger froze that still read a lane of the start as the case records print "
                "it. "
                "It is walked here only to order the later commit's claims: its own verdicts "
                "and records stand as its own import made them."
            ),
        }
        found.append(entry)
    for pending in WALK_PENDING_REPORTS.get(walk.name, ()):
        claims = [
            dict(claim)
            for claim in pending["claims"]
            if claim["n"] in highs and low(claim) < highs[claim["n"]]
        ]
        if claims:
            found.append({**pending, "claims": claims})
    return found


#: The later commits' comparisons a release walk's prints leave undecided, decided exactly
#: (`decide_later`), in the walk's directory as the 14 October ledger keeps its own.
LATER_RESOLVED = "undecided-resolved.json"
LATER_RESOLVED_FORMAT = "undecided-comparisons-resolved/v1"


def decide_later(issue: int | str) -> dict[str, Any]:
    """Decide exactly each comparison of a later commit's claim (`later_reports`) with a
    member of its count's frozen start that the two spans leave undecided: a case's reported
    lane whose record holds only a print and a minimal polynomial, or a register entry
    pending adoption whose root interval the catalogue retains.

    The standing side is read by `devtools.decide_undecided_comparisons.record_side`, as
    the root of its polynomial in the print's window of one unit either side or in the
    retained interval, and the claim's rational side is placed against it by one sign
    (`decide_undecided_comparisons.decide_rational`), with the margin's rigorous bounds. A
    member the record gives no exact side for is refused, never guessed.
    """
    from devtools import decide_undecided_comparisons as exact  # noqa: PLC0415
    from devtools import intake_ledger  # noqa: PLC0415

    chosen = release(issue)
    walk = walk_of(chosen)
    _require(
        (walk.directory / intake_ledger.STARTS).is_file(),
        f"{walk.name}: gather has frozen no starts to decide against",
    )
    later = later_publications(chosen)
    starts = _start_sides(walk, WALK_READ_AT_MAIN[walk.name], later)
    rows = []
    gated = []
    for item in later_reports(chosen, later, walk):
        for claim in item["claims"]:
            n, side = int(claim["n"]), Fraction(str(claim["exact"]))
            own = reports.exact_span(side)
            for member in starts[n]:
                if reports.below(own, member.span) or reports.below(member.span, own):
                    continue
                if member.exact:
                    continue
                try:
                    record, standing = exact.record_side(n)
                except exact.DecisionError as error:
                    gated.append(
                        {"n": n, "report": item["report"], "against": member.label}
                        | {"needs": str(error)}
                    )
                    continue
                expected = (
                    f"register {exact.REGISTER[n]}, pending adoption"
                    if n in exact.REGISTER
                    else exact.KINGBIRD
                )
                _require(
                    member.label == expected and isinstance(standing, exact.Root),
                    f"n={n}: {member.label} is not a side this decision reads",
                )
                assert isinstance(standing, exact.Root)
                (read,) = member.record_prints
                rows.append(
                    {
                        "n": n,
                        "report": item["report"],
                        "against": member.label,
                        "lane": read[0],
                        "value": read[1],
                        "exact_form": read[2],
                        **exact.decide_rational(side, standing),
                        "method": (
                            "the rational's position in the root's isolating interval, by one "
                            "sign"
                        ),
                        "side": claim["exact"],
                        "standing_side": {k: v for k, v in record.items() if k != "polynomial"},
                    }
                )
    return {
        "schema": LATER_RESOLVED_FORMAT,
        "tool": "devtools.beyond_horizon_replay decide-later",
        "walk": f"campaign/issue-intake/{walk.name}",
        "relation": (
            "the later commit's side against the standing one: margin is the later side minus "
            "the standing side, with rigorous bounds rounded outward"
        ),
        "counts": {
            name: sum(1 for row in rows if row["relation"] == name)
            for name in ("below", "equal", "above")
        },
        "rows": rows,
        "gated": gated,
    }


def write_decide_later(issue: int | str) -> dict[str, int]:
    """Write a release walk's decided comparisons (`decide_later`); return their counts."""
    record = decide_later(issue)
    _write(walk_of(release(issue)).directory / LATER_RESOLVED, record)
    return record["counts"]


def later_relations(walk: Walk) -> dict[tuple[str, int], list[dict[str, Any]]]:
    """The record relations a release walk's decided comparisons give its later commits'
    claims (`decide_later`), by report and count; none before the receipt is written."""
    path = walk.directory / LATER_RESOLVED
    if not path.is_file():
        return {}
    found: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for row in _read(path)["rows"]:
        found.setdefault((str(row["report"]), int(row["n"])), []).append(
            {
                "lane": row["lane"],
                "relation": row["relation"],
                "value": row["value"],
                "exact_form": row["exact_form"],
                "read_from": (
                    f"packing/campaign/issue-intake/{walk.name}/{LATER_RESOLVED} rows[n = "
                    f"{row['n']}], by devtools.beyond_horizon_replay decide-later"
                ),
                "margin": row["margin"],
            }
        )
    return found


#: When issue #763 was opened, which dates its claims (`claim_map_walk_sources`).
ISSUE_763_REPORTED = "2026-10-23T23:35:51Z"
#: The f1ceee4 packet: its source history holds every side Polkovskyi's repository
#: published at 325 to 1024 through f1ceee4, and its later-commits receipt the three
#: commits after it (`claim_map_walk_sources`).
_F1CEEE4 = WEB / "mishapolk-issue732-f1ceee4-2026-10-23"


class ClaimMapWalk(NamedTuple):
    """What the walk of a release whose claims are re-derived (`Release.claim_map`) reads
    beyond its releases (`claim_map_walk_sources`), by the walk: a second such release
    declares its own rather than borrowing #763's (#789's review A, A9)."""

    #: When the issue was opened: its claims' date, and the cutoff of every earlier
    #: publication the walk reads (the history scan's, Polkovskyi's and the ledgers').
    reported: str
    #: How the issue's note names the push that made its commits public.
    pushed: str
    #: The packet whose receipts hold Polkovskyi's repository's publications.
    polkovskyi: Path
    #: An earlier issue whose claims at the walk's counts have no row among its starts,
    #: walked as a report of its own (`earlier_issue_claims`): #763's at the 43f666c walk,
    #: the only issue the reading supports (`EARLIER_ISSUE`).
    earlier_issue: int | None = None
    #: The bead that owns the earlier issue's rows the walk records (`earlier_issue_claims`).
    earlier_bead: str = ""
    #: Whether the walk reads the push that made the earlier issue's pin public, commit by
    #: commit at its counts (`earlier_push`, `EARLIER_PUSH`).
    earlier_push: bool = False


CLAIM_MAP_WALKS = {
    ISSUE_763: ClaimMapWalk(
        reported=ISSUE_763_REPORTED,
        pushed="the push of 23:38:42Z made efef7d1, fa6237e and 964ee2b public together, after "
        "the issue",
        polkovskyi=_F1CEEE4,
    ),
    # The notebook rows are dated by the push itself, so every earlier publication is cut
    # there: issue #763, 2 min 51 s before it, claims none of their counts.
    NOTEBOOKS_964: ClaimMapWalk(
        reported=COUZO_763_PUSHED,
        pushed="the push of 23:38:42Z made efef7d1, fa6237e and 964ee2b public together",
        polkovskyi=_F1CEEE4,
    ),
    # 43f666c is dated by its push, so every earlier publication is cut there. Its starts are
    # frozen after #795, which hold #763's certificate rows and the push of 23:38:42Z at the
    # notebook rows' counts; #763's claims with no row there (its recipes, decided here,
    # think-g2qy) and that push at the walk's other counts are walked as reports.
    COUZO_43F: ClaimMapWalk(
        reported=COUZO_43F_PUSHED,
        pushed="the push of 06:10:44Z made 43f666c, 73eac5b and 1c17153 public together",
        polkovskyi=_F1CEEE4,
        earlier_issue=763,
        earlier_bead="think-g2qy",
        earlier_push=True,
    ),
}


def _claim_map_claim(chosen: Release, item: Mapping[str, Any]) -> dict[str, Any]:
    """One claim of a re-derived release (`Release.claim_map`) as its walk transcribes it:
    the exact bound the index states, the file or recipe it comes from, and, for a
    certificate, the time the commit that first holds its file was committed."""
    n = int(item["n"])
    index = (
        f"certified_bounds.json at {chosen.retained[:8]}, retained in the {chosen.packet} "
        f"packet ({CLAIM_MAP.as_posix()})"
    )
    if chosen.claim_map == PUSH:
        where = (
            f"{item['certificate']} at {chosen.retained[:8]} (its header), retained in the "
            f"{chosen.packet} packet: a side {chosen.pin[:7]} first states "
            f"({PUSH_PUBLICATIONS.as_posix()})"
            + (
                ", the certificate of the construction its index states there"
                if item.get("index_kind") == "construction"
                else ""
            )
        )
    elif item["kind"] == "certificate":
        where = (
            f"{item['certificate']} at {chosen.retained[:8]} (its header), retained in the "
            f"{chosen.packet} packet: the bound {index} states"
        )
    elif item["kind"] == "deletion":
        squares = int(item["deleted_squares"])
        where = (
            f"{item['certificate']} at {chosen.retained[:8]} less its last "
            f"{'square' if squares == 1 else f'{squares} squares'}: the bound {index} "
            "states, with no certificate file at this count"
        )
    else:
        recipe = item["construction"]
        where = (
            f"the bound {index} states for its {recipe['kind']} recipe of the "
            f"n{recipe['source_n']} certificate ({item['certificate']}; "
            f"{recipe['tiles_per_side']} a side, {recipe['layers']} L-border "
            f"{'layer' if recipe['layers'] == 1 else 'layers'}"
            + (f", less {item['deleted_squares']}" if int(item["deleted_squares"]) else "")
            + "), with no certificate file at this count"
        )
    claim = _claim(n, Fraction(str(item["exact"])), where)
    if item["kind"] == "certificate":
        claim["first_committed"] = chosen.first_commit_of(n)[1]
    if chosen.claim_map == PUSH:
        claim |= _push_identity_parts(chosen, n)
    return claim


def _push_identity_parts(chosen: Release, n: int) -> dict[str, Any]:
    """What a push release's claim at a count of `PUSH_IDENTITY` carries into its walk: the
    measurement against the push's earlier side there (``measured``), which the manifest of
    ``certificates/best/`` names as the row's ``previous_source``. That field names the
    record the source's catalogue held at the count before the row, not the packing a
    notebook or search started from: at 303 at fa6237e it names Evan Daniel's record where
    the entry's own ``seed_credit`` names Lavrentev, and of the 182 entries of that manifest
    that carry both seed fields, the two differ in all 182 and name another person in 178
    (M-1 of the 24 October review of T-241 and T-242, which corrects #795's review B, B1).
    At 964ee2b, which this walk reads, 11 of the 202 such entries differ, among them 794 and
    910, whose own seed is Tymchishin's v3 and whose previous record is Goebel's family
    formula; the other 191 are Couzo's refinements of his own previous records (review A,
    A4, of #803). So the field is no lineage, and the
    measurement alone decides what the walk says: where the squares pair one to one with
    none beyond `PUSH_SAME_PACKING`, the row refines that packing (``refines``) and is
    credited after its finder; otherwise it is another arrangement, a new packing
    (``new_packing``) with no ``continues``, since no source states where its search
    started, and it is credited to its finder alone."""
    if n not in PUSH_IDENTITY:
        return {}
    receipt = _read(chosen.directory / PUSH_IDENTITY_RECEIPT)
    found = [
        row
        for row in receipt["rows"]
        if row["n"] == n and row["commit"] == chosen.pin and row["holder"] == chosen.push_holder
    ]
    if not found:
        return {}
    (row,) = found
    nearest = min(row["against"], key=lambda item: abs(float(item["side_difference"])))
    other = _push_release(chosen, nearest["commit"], nearest["holder"])
    source = PUSH_IDENTITY_RECEIPT.as_posix()
    witness = claims_763.read_witnesses().get(str(n)) or {}
    previous = (witness.get("provenance") or {}).get("previous_source") or {}
    _require(
        previous.get("certificate") == nearest["certificate"],
        f"n={n}: the manifest's previous_source is not the push's earlier side measured",
    )
    stated = (
        f"964ee2b's manifest names {other.holders}'s {other.pin[:7]} certificate "
        f"({nearest['certificate']}) as the row's previous_source, the record its catalogue "
        "held at the count before, not a seed (M-1 of the 24 October review of T-241 and "
        "T-242)"
    )
    parts: dict[str, Any] = {
        "measured": {
            "against": other.label,
            "finding": _identity_finding(nearest, n),
            "source": f"packing/resources/web/{chosen.packet}/{source}",
        }
    }
    if nearest["one_to_one"] and not nearest["beyond"][PUSH_SAME_PACKING]:
        parts["refines"] = {
            "packing_of": other.holders,
            "entry": other.label,
            "source": (
                f"{stated}, and the measurement pairs every square one to one within "
                f"{PUSH_SAME_PACKING} ({source})"
            ),
        }
    else:
        parts["new_packing"] = {
            "source": (
                f"{stated}; the index credits the row to the notebook run and defers earlier "
                "credits to a provenance that states no seed of the row's own (\"earlier seed "
                'and construction credits retained in provenance"), and the measurement does '
                "not pair them one to one "
                f"({nearest['beyond'][PUSH_SAME_PACKING]} squares beyond {PUSH_SAME_PACKING}"
                f", {source}): another arrangement, whose search start no source states"
            ),
        }
    return parts


def _push_release(chosen: Release, commit: str, holder: str) -> Release:
    """The release of a push walk that holds ``holder``'s claims at ``commit``."""
    found = [
        item
        for item in RELEASES.values()
        if item.walk == chosen.walk
        and item.claim_map == PUSH
        and item.pin == commit
        and item.push_holder == holder
    ]
    _require(len(found) == 1, f"{commit[:8]} {holder}: {len(found)} releases of the push")
    return found[0]


def _identity_finding(item: Mapping[str, Any], n: int) -> str:
    """A pose measurement (`measured_identity`) in a sentence."""
    beyond = item["beyond"]
    pairing = (
        "every square pairs one to one"
        if item["one_to_one"]
        else f"the pairing is not one to one ({item['paired']} of {n} squares matched)"
    )
    moved = (
        f"none moves beyond 1e-6 (largest {item['largest_centre_distance']})"
        if not beyond["1e-6"]
        else f"{beyond['1e-6']} move beyond 1e-6, {beyond['1e-3']} beyond 1e-3 and "
        f"{beyond['1e-1']} beyond 0.1 (largest {item['largest_centre_distance']})"
    )
    below = item["side_difference"].lstrip("-")
    return (
        f"under the best of the box's eight symmetries {pairing}; {moved}, largest turn "
        f"{item['largest_rotation_difference_degrees']} degrees; the side is {below} below"
    )


def _grouped_publications(
    items: Iterable[Mapping[str, Any]], bead: Callable[[str], str], note: str, walk: Walk
) -> list[dict[str, Any]]:
    """Publications of watched repositories, one report a commit, dated by the item's
    ``published``, at the least side the commit states at each count (#722's review A,
    A2); a table row keeps its print at the table's places (`TABLES`)."""
    groups: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    for item in items:
        groups.setdefault((str(item["repository"]), str(item["commit"])), []).append(item)
    found = []
    for (name, commit), stated in sorted(
        groups.items(), key=lambda pair: (str(pair[1][0]["published"]), pair[0])
    ):
        claims = []
        for claim in _least_claims(stated):
            least = next(
                item
                for item in stated
                if item["n"] == claim["n"]
                and Fraction(str(item["side"])) == Fraction(claim["exact"])
            )
            if least.get("kind") == "table":
                places = TABLES[str(least["path"]).split(":", 1)[0]]
                printed = {key: value for key, value in claim.items() if key != "exact"}
                claims.append(printed | {"printed": ceiling(Fraction(claim["exact"]), places)})
            else:
                claims.append(claim)
        label = f"{name}@{commit[:7]}"
        holders = stated[0].get("holders")
        if holders is None:
            # Only a watched repository's publication is a report; an unknown name is
            # refused, not credited (#789's review B, B3).
            _require(name in WATCHED_HOLDERS, f"{label}: {name} is not a watched repository")
            holders = WATCHED_HOLDERS[name]
        found.append(
            {
                "report": label,
                "url": f"https://github.com/{name}/tree/{commit}",
                "reported_at": stated[0]["published"],
                "holders": holders,
                "bead": bead(label),
                "claims": claims,
                "note": note + held_sentence(walk, label),
            }
        )
    return found


def _notebook_phrase(chosen: Release, count: int) -> str:
    """A push release in the walk's note: its holder, the notebook as the source's manifest
    names it, its version where stated and its run, and how many sides it gives; or the
    publisher's own sides."""
    if not chosen.notebook_run:
        return f"{chosen.holders}'s own ({count})"
    stated = mapped_claims(chosen)[0]["notebook"]
    slug = str(stated["notebook"]).rstrip("/").rsplit("/", 1)[-1]
    version = f" v{stated['notebook_version']}" if stated.get("notebook_version") else ""
    return f'{chosen.holders}\'s "{slug}"{version}, run {stated["run"]} ({count})'


def _other_authors(item: Release, walk: Walk) -> list[dict[str, Any]]:
    """The claims of a push release's commit that the index credits to another author
    (`OTHER_AUTHOR`), which no release holds: the walk takes them as the commit's report
    and may only rule them out (`release_at`)."""
    if item.claim_map != PUSH:
        return []
    return [
        claim
        for claim in _read(mapped_path(item))["claims"]
        if claim["commit"] == item.pin
        and claim["holder"] == OTHER_AUTHOR
        and walk.reaches(int(claim["n"]))
    ]


def _other_phrase(claims: Sequence[Mapping[str, Any]]) -> list[str]:
    """Another author's sides of a push commit in the walk's note, by the credit's name."""
    names = Counter(str(claim["credit"]).split(";", 1)[0].strip() for claim in claims)
    return [
        f"{count} credited to {name}, which no release of the push holds"
        for name, count in sorted(names.items())
    ]


#: The one earlier issue a claim-map walk may read (`ClaimMapWalk.earlier_issue`). What the
#: reading excludes (`devtools.couzo_763_claims.earlier_sides`, in `earlier_push`) and the
#: notes it writes (`_earlier_issue_report`, `_earlier_push_reports`) are #763's and the push
#: of 23:38:42Z's, so another issue is refused until it declares its own (#800's review A,
#: A5).
EARLIER_ISSUE = 763


def _earlier_issue(walk: Walk, declared: ClaimMapWalk) -> int:
    """The earlier issue ``walk`` names, which must be `EARLIER_ISSUE`."""
    _require(
        declared.earlier_issue == EARLIER_ISSUE,
        f"{walk.name}: reads issue #{declared.earlier_issue} as an earlier issue; the "
        f"reading's exclusions and notes are #{EARLIER_ISSUE}'s alone",
    )
    return EARLIER_ISSUE


def earlier_issue_claims(walk: Walk) -> tuple[Release | None, list[dict[str, Any]]]:
    """The claims a claim-map walk reads of #763, the earlier issue it may name
    (`ClaimMapWalk.earlier_issue`, `EARLIER_ISSUE`), as a report of their own: each claim
    beyond the corpus the walk reaches that its release's filtered receipt does not hold, so
    that no row of it is among the walk's starts (a recipe, a deletion, or a claim its own
    walk does not record). At the 43f666c walk these are #763's 13 recipes, which its walk
    held until this walk's import decided them (think-g2qy), its deletion bound at 683, and
    328, 850 and 909, which restate f1ceee4's rows; the push of 23:38:42Z, which follows the
    issue, is walked against them."""
    declared = CLAIM_MAP_WALKS.get(walk.name)
    if declared is None or declared.earlier_issue is None:
        return None, []
    chosen = release(_earlier_issue(walk, declared))
    replayed = {int(row["n"]) for row in _read(chosen.path(FILTERED))["rows"]}
    return chosen, [
        claim
        for claim in mapped_claims(chosen)
        if int(claim["n"]) > reports.HORIZON
        and walk.reaches(int(claim["n"]))
        and int(claim["n"]) not in replayed
    ]


def _earlier_issue_report(
    walk: Walk,
    declared: ClaimMapWalk,
    chosen: Release,
    earlier: Release,
    claims: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """#763's claims (`earlier_issue_claims`) as a report of the walk; the note names the
    push of 23:38:42Z, so it is #763's alone (`EARLIER_ISSUE`)."""
    kinds = Counter(str(claim["kind"]) for claim in claims)
    described = _listing(
        [f"{count} {kind}{'' if count == 1 else 's'}" for kind, count in sorted(kinds.items())]
    )
    return {
        "report": earlier.label,
        "issue": earlier.issue,
        "holders": earlier.holders,
        "bead": declared.earlier_bead or earlier.bead,
        "claims": [_claim_map_claim(earlier, claim) for claim in claims],
        "note": (
            f"Issue {earlier.issue}'s {len(claims)} claims at the counts {chosen.label} "
            f"claims or that its walk ({earlier.walk}) records with no row of its own on main "
            f"({described}), re-derived from the source's indexes at {earlier.retained[:8]} "
            f"({earlier.packet} packet, {CLAIM_MAP.as_posix()}) and dated by the issue: "
            "each claim its release's filtered receipt does not hold, so no row of it is "
            "among this walk's starts. The construction checker decides its recipes "
            f"(devtools.construction_checker, {earlier.packet} packet, "
            f"{RECIPES.as_posix()}), which its walk held until this import "
            f"({declared.earlier_bead or earlier.bead}). Walking them here orders the push "
            "of 23:38:42Z, which made 964ee2b public 2 min 51 s after the issue, against "
            "them; first_committed is the committer time of the commit that first holds the "
            "certificate." + held_sentence(walk, earlier.label)
        ),
    }


#: The 43f666c walk's reading of the push that made #763's pin public, commit by commit at
#: the walk's counts (`earlier_push`).
EARLIER_PUSH = Path("receipts/earlier-push.json")
EARLIER_PUSH_FORMAT = "beyond-horizon-earlier-push-v1"


def _credited_name(credit: str, repository: str) -> str:
    """Who an index credit names first, by name; the repository's holder where it names
    none, or names him by his handle."""
    name = re.split(r" \(|,", credit.split(";", 1)[0], maxsplit=1)[0].strip()
    if not name or name == repository.split("/", 1)[0]:
        return WATCHED_HOLDERS[repository]
    return name


def walk_counts(walk: Walk) -> list[int]:
    """The counts a claim-map walk reads (`claim_map_walk_sources`): each count a release
    of the walk claims that the walk reaches, and the earlier issue's
    (`earlier_issue_claims`)."""
    found = {
        int(claim["n"])
        for items in _walk_groups(walk).values()
        for item in items
        if item.claim_map
        for claim in [*mapped_claims(item), *_other_authors(item, walk)]
        if walk.reaches(int(claim["n"]))
    }
    return sorted(found | {int(claim["n"]) for claim in earlier_issue_claims(walk)[1]})


def earlier_push(issue: int | str, clone: Path, read_on: str = "") -> dict[str, Any]:
    """The push that made #763's pin public, the earlier issue a claim-map walk may name
    (`ClaimMapWalk.earlier_issue`, `EARLIER_ISSUE`), read commit by commit at the walk's
    counts (`_push_statements`, #795's review
    A, A1): each commit's least new side at each count strictly below the frozen start, and
    none an earlier publication holds (`devtools.couzo_763_claims.earlier_sides`). A side
    a certificate the pin holds states names that certificate; a side only an index states,
    a recipe or a deletion bound, names the index. Each keeps the credit the index states
    at its count at that commit. At the 43f666c walk this is the push of 23:38:42Z, whose
    best/ certificates at #763's recipe counts #795's review A noted, read at the walk's
    counts after #763's issue. Its starts are the walk's frozen ones, or, before ``gather``
    freezes them, those the checkout's records give for a ledger read on ``read_on``
    (`_start_sides`)."""
    chosen = release(issue)
    walk = walk_of(chosen)
    declared = CLAIM_MAP_WALKS[walk.name]
    _require(declared.earlier_push, f"{walk.name}: reads no earlier push")
    _require(declared.earlier_issue is not None, f"{walk.name}: names no earlier issue")
    earlier = release(_earlier_issue(walk, declared))
    push = _push_of(earlier)
    counts = walk_counts(walk)
    highs = _least_highs(_start_sides(walk, WALK_READ_AT_MAIN[walk.name], counts, read_on))
    read, least = _push_statements(
        clone,
        push,
        retained=earlier.retained,
        counts=counts,
        highs=highs,
        earlier=claims_763.earlier_sides(),
    )
    at_pin = _pin_files(clone, earlier.retained)
    claims: list[dict[str, Any]] = []
    for _order, commit, n, side, items in least:
        files = _files_of(items, at_pin)
        stated = next((item for item in items if item.get("credit") is not None), None)
        index = next((item for item in items if item["kind"] == "index"), None)
        claims.append(
            {
                "n": n,
                "commit": commit,
                "kind": "certificate" if files else "index",
                "path": files[0] if files else str((index or {}).get("path", "")),
                "exact": legacy.literal(side),
                "index_kind": str(stated["index_kind"]) if stated else "",
                "credit": str(stated["credit"]) if stated else "",
            }
        )
    return {
        "format": EARLIER_PUSH_FORMAT,
        "source": earlier.source_url,
        "retained_commit": earlier.retained,
        "push": {"before": push.before, "head": push.head, "pushed": push.pushed},
        "walk": walk.name,
        "starts_read_at_main": WALK_READ_AT_MAIN[walk.name],
        "counts": counts,
        "indexes": {path: ".".join(keys) for path, keys in INDEXES.items()},
        "commits": read,
        "claims": claims,
    }


def write_earlier_push(issue: int | str, clone: Path, read_on: str = "") -> dict[str, int]:
    """Write a claim-map walk's earlier-push receipt (`earlier_push`); return each commit's
    claims."""
    record = earlier_push(issue, clone, read_on)
    _write(release(issue).directory / EARLIER_PUSH, record)
    return dict(Counter(item["commit"][:7] for item in record["claims"]))


def _earlier_push_reports(
    walk: Walk, chosen: Release, counts: Sequence[int]
) -> list[dict[str, Any]]:
    """The push of 23:38:42Z's claims (`earlier_push`) as reports of the walk, one a commit,
    each dated by the push and ordered by its commit's time (`devtools.intake_ledger.walk`);
    the notes are #763's alone (`EARLIER_ISSUE`)."""
    receipt = _read(chosen.directory / EARLIER_PUSH)
    _require(
        receipt["counts"] == list(counts),
        f"{walk.name}: the earlier push was read at other counts than the walk's",
    )
    repository = repository_of(str(receipt["source"]))
    pushed = str(receipt["push"]["pushed"])
    found: list[dict[str, Any]] = []
    for record in receipt["commits"]:
        commit = str(record["commit"])
        mine = [claim for claim in receipt["claims"] if claim["commit"] == commit]
        if not mine:
            continue
        label = f"{repository}@{commit[:7]}"
        claims = []
        for claim in mine:
            if claim["kind"] == "certificate":
                where = (
                    f"{claim['path']} at {str(receipt['retained_commit'])[:8]} (its header): "
                    f"a side {commit[:7]} first states ({chosen.packet} packet, "
                    f"{EARLIER_PUSH.as_posix()})"
                )
            else:
                where = (
                    f"the bound {claim['path']} states at {commit[:7]} for its "
                    f"{claim['index_kind'] or 'entry'}, with no certificate the pin holds at "
                    f"that side: a side {commit[:7]} first states ({chosen.packet} packet, "
                    f"{EARLIER_PUSH.as_posix()})"
                )
            claims.append(
                _claim(int(claim["n"]), Fraction(str(claim["exact"])), where)
                | {"first_committed": record["committed"]}
            )
        names = list(
            dict.fromkeys(_credited_name(str(claim["credit"]), repository) for claim in mine)
        )
        found.append(
            {
                "report": label,
                "url": f"https://github.com/{repository}/tree/{commit}",
                "reported_at": pushed,
                "holders": _listing(names),
                "bead": chosen.bead,
                "claims": claims,
                "note": (
                    f"The sides {commit[:7]} first states at the walk's counts below the "
                    "start, its least at each (devtools.beyond_horizon_replay earlier-push, "
                    f"{chosen.packet} packet, {EARLIER_PUSH.as_posix()}), read commit by "
                    "commit through the push of 23:38:42Z that made efef7d1, fa6237e and "
                    "964ee2b public together after issue 763, as the first-commit rule reads "
                    "a history (#795's review A, A1); each holder as the index credits the "
                    "side at that commit. No issue reports them, and #763's claims, which "
                    "come first, and the record's starts are what they are walked against. "
                    f"first_committed is the committer time of {commit[:7]}."
                    + held_sentence(walk, label)
                ),
            }
        )
    return found


def claim_map_walk_sources(
    issue: int | str, read_on: str, walk: Walk | None = None
) -> dict[str, Any]:
    """The ``sources.yaml`` of a release whose claims are re-derived from its source's
    indexes (#763, `Release.claim_map`), with every other release of its walk.

    ``walk`` is the release's own walk by default (`walk_of`). The reports, at each count
    those releases claim that the walk reaches (`Walk.reaches`):

    - the issue's claims, dated by the issue, each at the exact bound the index states:
      a certificate's header, a deletion's or a recipe's bound; and the index's
      unrequested rows, the watched repository's publication, dated by the push that made
      it public (`PUSHED_LATER`);
    - every earlier publication strictly below the count's start (`_least_highs`): the
      history scan's (`HISTORY_PUBLICATIONS`, to 6b7391d and the other watched
      repositories' heads before the issue), Polkovskyi's repository through f1ceee4 and the
      three commits after it, from the f1ceee4 packet's receipts, and #715's
      re-certifications below the print, which the walk decides as restatements
      (think-fwa9);
    - in the corpus, every earlier report a retained ledger walked strictly below the start
      before the issue (`ledger_reports`).

    Every earlier publication is cut at the issue (`CLAIM_MAP_WALKS`). The claims a walk
    frozen at 1024 does not reach are the walk above 1024's (D1, think-llit).
    """
    chosen = release(issue)
    walk = walk or walk_of(chosen)
    _require(
        walk.name in CLAIM_MAP_WALKS,
        f"{walk.name}: no claim-map walk declared (CLAIM_MAP_WALKS)",
    )
    declared = CLAIM_MAP_WALKS[walk.name]
    cutoff = declared.reported
    # The notes name the releases whose counts the walk reads.
    claimant = "the notebook rows" if chosen.claim_map == PUSH else chosen.label
    read_at_main = WALK_READ_AT_MAIN[walk.name]
    groups = {
        label: [item for item in items if item.claim_map]
        for label, items in _walk_groups(walk).items()
    }
    groups = {label: items for label, items in groups.items() if items}
    own = {
        item.key: [claim for claim in mapped_claims(item) if walk.reaches(int(claim["n"]))]
        for items in groups.values()
        for item in items
    }
    # A count is one release's among the releases sharing a claim map; a push read commit
    # by commit (`PUSH`) claims it at most once a commit.
    others = {label: _other_authors(items[0], walk) for label, items in groups.items()}
    claimed = Counter(
        (label if item.claim_map == PUSH else "", int(claim["n"]))
        for label, items in groups.items()
        for item in items
        for claim in own[item.key]
    ) + Counter(
        (label, int(claim["n"])) for label, claims in others.items() for claim in claims
    )
    twice = sorted(n for (_, n), times in claimed.items() if times > 1)
    _require(not twice, f"{walk.name}: the releases sharing a claim map both claim {twice}")
    earlier_release, earlier_claims = earlier_issue_claims(walk)
    counts = sorted({n for _, n in claimed} | {int(claim["n"]) for claim in earlier_claims})
    starts = _start_sides(walk, read_at_main, counts, read_on)
    highs = _least_highs(starts)
    reports_list: list[dict[str, Any]] = []
    for label, items in groups.items():
        item = items[0]
        pairs = sorted(
            [
                *((part, claim) for part in items for claim in own[part.key]),
                *((item, claim) for claim in others[label]),
            ],
            key=lambda pair: int(pair[1]["n"]),
        )
        claims = [_claim_map_claim(part, claim) for part, claim in pairs]
        kinds = Counter(str(claim["kind"]) for _, claim in pairs)
        described = _listing(
            [
                f"{count} {kind}{'' if count == 1 else 's'}"
                for kind, count in sorted(kinds.items())
            ]
        )
        if item.claim_map == PUSH:
            head = {
                "report": label,
                "url": f"{item.source_url}/tree/{item.pin}",
                "reported_at": item.reported,
            }
            what = (
                f"The {len(claims)} sides {item.pin[:7]} first states at the counts of the "
                f"notebook rows ({described}), each its least new side there below the start, "
                "commit by commit through the push (devtools.beyond_horizon_replay "
                f"push-publications, {item.packet} packet, {PUSH_PUBLICATIONS.as_posix()}): "
                + _listing(
                    [_notebook_phrase(part, len(own[part.key])) for part in items]
                    + _other_phrase(others[label])
                )
                + ". No issue reports them. The push of 23:38:42Z made efef7d1, fa6237e and "
                f"964ee2b public together (PUSHED_LATER), so each commit is a report from it, "
                "taken in commit order, and an import of their own (think-lyf9; #795's review "
                "A, A1), each holder's rows a coverage source of their own. first_committed is "
                f"the committer time of {item.pin[:7]}."
            )
        elif item.issue is not None:
            head: dict[str, Any] = {"report": item.label, "issue": item.issue}
            what = (
                f"The issue's {len(claims)} claims {walk.reach} ({described}), "
                f"re-derived from the source's indexes at {item.retained[:8]} by its README's "
                f"rule ({item.packet} packet, {CLAIM_MAP.as_posix()}), since the issue carries "
                "no table; each at the exact bound certified_bounds.json states, dated by the "
                "issue. first_committed is the committer time of the commit that first holds "
                f"the certificate; {declared.pushed}."
                + (
                    f" Its claims above {walk.through} are not walked here (think-llit)."
                    if walk.through is not None
                    else f" Its claims at or below {walk.above} are walked by {item.walk}."
                )
            )
        else:
            head = {
                "report": item.label,
                "url": f"{item.source_url}/tree/{item.pin}",
                "reported_at": item.reported,
            }
            what = (
                f"The {len(claims)} rows certified_bounds.json publishes at "
                f"{item.retained[:8]} {walk.reach} ({described}) that the issue's "
                "selection rule leaves out: each is below the comparison's 12-place print, "
                "but by 1e-10 or less where the comparison is another author's. No issue "
                "reports them, so they are the watched repository's publication, dated by the "
                f"push that made {item.pin[:7]} public (PUSHED_LATER), and an import of their "
                f"own ({item.packet} packet, {CLAIM_MAP.as_posix()}, unrequested)."
            )
        reports_list.append(
            head
            | {
                "holders": _listing(list(dict.fromkeys(part.holders for part in items))),
                "bead": item.bead,
                "claims": claims,
                "note": what + held_sentence(walk, label),
            }
        )
    if earlier_release is not None and earlier_claims:
        reports_list.append(
            _earlier_issue_report(walk, declared, chosen, earlier_release, earlier_claims)
        )
    if declared.earlier_push:
        reports_list += _earlier_push_reports(walk, chosen, counts)
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
        for n in sorted(held_715 & set(counts))
        if Fraction(replayed[n]["exact_side"]) < highs[n]
    ]
    by_side = {(claim["n"], Fraction(claim["exact"])) for claim in couzo}
    history = [
        item
        for item in _read(HISTORY_PUBLICATIONS)["publications"]
        if item["n"] in highs
        and Fraction(item["side"]) < highs[item["n"]]
        and (item["n"], Fraction(item["side"])) not in by_side
        and item["published"] < cutoff
    ]
    reports_list += _grouped_publications(
        history,
        lambda label: _publication_bead(label) or chosen.bead,
        "A publication in a watched repository that no issue reports, dated by its commit, "
        "or by the later push that made it public; transcribed from the history scan "
        f"({HISTORY_PUBLICATIONS.relative_to(ROOT).as_posix()}) at each count {claimant} "
        "claims where it states a side strictly below the start, at the least side the "
        "commit states there.",
        walk,
    )
    # Polkovskyi's publications carry their holder, and are cut at the issue as the
    # history scan's are (#789's review B, B3 and B4).
    mishapolk = [
        item
        | {
            "repository": MISHAPOLK_REPOSITORY,
            "kind": "certificate",
            "holders": MISHAPOLK_HOLDER,
        }
        for item in _read(declared.polkovskyi / SOURCE_HISTORY)["publications"]
        if item["n"] in highs
        and Fraction(item["side"]) < highs[item["n"]]
        and item["published"] < cutoff
    ] + [
        publication
        | {
            "repository": MISHAPOLK_REPOSITORY,
            "commit": later["commit"],
            "published": later["pushed"],
            "holders": MISHAPOLK_HOLDER,
        }
        for later in _read(declared.polkovskyi / LATER_COMMITS)["commits"]
        if later["pushed"] < cutoff
        for publication in later["publications"]
        if publication["n"] in highs and Fraction(publication["side"]) < highs[publication["n"]]
    ]
    reports_list += _grouped_publications(
        mishapolk,
        lambda label: RELEASES[label].bead if label in RELEASES else chosen.bead,
        "A publication in Mykhailo Polkovskyi's watched repository, dated by its commit, or "
        "by the push that made it public; transcribed from the "
        f"{declared.polkovskyi.name} packet's receipts (source-history.json through f1ceee4 "
        f"and later-commits.json after it) at each count {claimant} claims where it states "
        "a side strictly below the start, at the least side the commit states there.",
        walk,
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
                    "Issue 715's re-certifications of the 4e4c8ce certificates below the "
                    f"12-place print at the counts {claimant} claims, strictly below the "
                    "start, at the exact sides its packet's filtered receipt states; each "
                    "restates the certificate it re-certifies, by the owner's answer of 23 "
                    "October 2026 (think-fwa9)." + held_sentence(walk, "#715")
                ),
            }
        )
    inside = {n: highs[n] for n in counts if n <= reports.HORIZON}
    prints = {
        n: {read for member in starts[n] for read in member.record_prints} for n in inside
    }
    reports_list += ledger_reports(walk, inside, cutoff, prints)
    labels = [item["report"] for item in reports_list]
    twice = sorted({label for label in labels if labels.count(label) > 1})
    _require(not twice, f"{walk.name}: two reports share a label: {twice}")
    return {
        "format": "intake-ledger-sources-v1",
        "read_at_main": read_at_main,
        "read_on": read_on,
        "rule": RULE,
        "lanes": [],
        "reports": reports_list,
        "rulings": WALK_RULINGS[walk.name],
    }


def write_release_walk_sources(issue: int | str, read_on: str, walk: Walk | None = None) -> int:
    """Write a release walk's ``sources.yaml`` (`release_walk_sources`, or
    `claim_map_walk_sources` for a release whose claims are re-derived), for its own walk
    or ``walk``; return how many reports it holds."""
    import yaml  # noqa: PLC0415

    chosen = release(issue)
    document = (claim_map_walk_sources if chosen.claim_map else release_walk_sources)(
        issue, read_on, walk
    )
    target = (walk or walk_of(chosen)).directory / "sources.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(target) as temporary:
        temporary.write_text(
            yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=100),
            encoding="utf-8",
        )
    return len(document["reports"])


def declared_rows(chosen: Release) -> dict[str, Any]:
    """A release's rows as its walk records them (`declaration_problems`): at each count
    beyond the corpus the walk records it and does not hold it, the certificate the history
    scan found at the publication's least side there, or, for an issue with no table of rows
    (#732), the certificate its source holds at the retained commit (`source_history`), or,
    for one whose claims are re-derived from its source's indexes (#763), the certificate
    its packet's claim map names (`Release.claim_map`), with that side rounded up at 12
    places. A count in the corpus is the register's, not a row's. Each walk of the release
    (`walks_of`) declares the counts it reaches. A deletion the walk records and does not
    hold is a row at its parent's side, declaring the parent's certificate and the squares
    it deletes (``deleted``), which the replay decides as the parent's first ``n`` poses;
    whether an issue's deletion bound gets a row is think-kzme's, so a walk holds it until
    the owner answers. A recipe the walk records and does not hold is a row by the owner's
    D2 answer, declaring its parent's certificate and the recipe the construction checker
    decides (`write_recipe_decisions`)."""
    commit = chosen.pin
    if chosen.claim_map:
        found = {
            item["n"]: {
                "kind": item["kind"],
                "path": item["certificate"],
                "side": item["exact"],
                "deleted": int(item.get("deleted_squares") or 0),
                **({"recipe": declared_recipe(item)} if item.get("construction") else {}),
            }
            for item in mapped_claims(chosen)
        }
    elif chosen.issue is not None:
        found = {
            row["n"]: {"kind": "certificate", "path": row["certificate"], "side": row["side"]}
            for walk in walks_of(chosen)
            if source_history_path(chosen, walk).is_file()
            for row in _read(source_history_path(chosen, walk))["at_commit"]
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
    walked = {
        n: (walk, count)
        for walk in walks_of(chosen)
        for n, count in _walked(walk).items()
        if walk.reaches(n)
    }
    for n, (walk, count) in sorted(walked.items()):
        if n <= reports.HORIZON or walk.holds(chosen.label, n) is not None:
            continue
        if not any(
            step["report"] == chosen.label and step["verdict"] == RECORDED
            for step in count["steps"]
        ):
            continue
        if release_at(walk, chosen.label, n) is not chosen:
            continue
        item = found[n]
        deleted = int(item.get("deleted") or 0)
        _require(
            item["kind"] == "certificate"
            or (item["kind"] == "deletion" and deleted > 0)
            or "recipe" in item,
            f"{chosen.label} n={n}: no certificate file and no recipe",
        )
        row = {"n": n, "certificate": item["path"], "printed": ceiling(Fraction(item["side"]))}
        row |= {"deleted": deleted} if deleted else {}
        rows.append(row | ({"recipe": item["recipe"]} if "recipe" in item else {}))
    declared: dict[str, Any] = {
        "format": WATCHED_FORMAT,
        "publication": chosen.issue_url,
        "commit": chosen.pin,
        "committed": chosen.committed,
    }
    if chosen.issue is None:
        declared["published"] = chosen.reported
    return declared | {"walk": chosen.walk, "rows": rows}


def declared_recipe(item: Mapping[str, Any]) -> dict[str, Any]:
    """A claim map's recipe as a declared row carries it (`recipe_of` reads it back): the
    construction, the exact bound the index states and the parent's SHA-256."""
    recipe = checker.recipe_from_index(item)
    return {
        "kind": recipe.kind,
        "source_n": recipe.source_n,
        "tiles_per_side": recipe.tiles_per_side,
        "layers": recipe.layers,
        "capacity": recipe.capacity,
        "bound": legacy.literal(recipe.bound),
        "sha256": recipe.parent_sha256,
    }


def declare_rows() -> dict[str, int]:
    """Write each release's declared rows (`declared_rows`); return their counts."""
    written: dict[str, int] = {}
    for chosen in RELEASES.values():
        if declares_rows(chosen):
            document = declared_rows(chosen)
            path = chosen.directory / chosen.declared
            path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
            written[chosen.key] = len(document["rows"])
    return written


# --------------------------------------------------------------------------- pose identity


POSE_IDENTITY = Path("receipts/pose-identity.json")
POSE_IDENTITY_FORMAT = "beyond-horizon-pose-identity-v1"
#: Where a retained packet keeps its certificate at a count, for the packets a release's
#: rows are measured against (`pose_identity`).
POSE_REFERENCES = {
    "couzo-issue715-2026-10-21": ("#715", "certificates/n{n}.cert"),
    "mishapolk-issue732-2026-10-22": ("#732", "certificates/0000-0999/n{n}.cert"),
}
#: The counts a release's author asks sole credit at, which `pose_identity` measures: the
#: author's comment on #732 of 23 October 2026 (issuecomment-6374211504, section 3A).
SOLE_CREDIT = {
    "#732 comment 6374211504": (463, 645, 646, 651, 696, 702, 747, 756, 809, 813, 989),
}
#: The distances `pose_identity` counts squares beyond.
POSE_THRESHOLDS = ("1e-9", "1e-6", "1e-3", "1e-1")


def _pose_floats(cert: legacy.Certificate) -> list[tuple[float, float, float]]:
    """Each square's centre and its rotation in degrees modulo 90, in binary64."""
    import math  # noqa: PLC0415

    found = []
    for pose in cert.poses:
        theta = math.degrees(2 * math.atan(float(pose.t))) % 90.0
        found.append((float(pose.x), float(pose.y), theta))
    return found


def _image(
    point: tuple[float, float, float], k: int, side: float
) -> tuple[float, float, float]:
    """A square under the ``k``-th of the box's eight symmetries: ``k % 4`` quarter turns,
    then a reflection in the vertical axis for ``k >= 4``."""
    x, y, theta = point
    for _ in range(k % 4):
        x, y = side - y, x
    if k >= 4:
        x, theta = side - x, (-theta) % 90.0
    return x, y, theta


def measured_identity(ours: legacy.Certificate, other: legacy.Certificate) -> dict[str, Any]:
    """How closely one packing pairs with another, square by square, in binary64.

    Under each of the box's eight symmetries every square of ``ours`` is paired with the
    nearest centre of ``other``; the symmetry kept pairs one to one if any does, then has the
    least largest distance. The record is that distance, how many squares lie beyond each of
    `POSE_THRESHOLDS`, and the largest difference of the paired rotations modulo 90 degrees.
    A measurement, not a decision: it is recorded beside what the source says.
    """
    import math  # noqa: PLC0415

    mine, theirs = _pose_floats(ours), _pose_floats(other)
    side = float(ours.side)
    grid: dict[tuple[int, int], list[int]] = {}
    for index, (x, y, _) in enumerate(theirs):
        grid.setdefault((math.floor(x), math.floor(y)), []).append(index)

    def nearest(x: float, y: float) -> tuple[int, float]:
        best, distance, reach = -1, math.inf, 1
        while best < 0 or reach <= 2:
            cx, cy = math.floor(x), math.floor(y)
            for i in range(cx - reach, cx + reach + 1):
                for j in range(cy - reach, cy + reach + 1):
                    for index in grid.get((i, j), ()):
                        found = math.dist((x, y), theirs[index][:2])
                        if found < distance:
                            best, distance = index, found
            reach += 1
        return best, distance

    kept: tuple[Any, ...] | None = None
    for k in range(8):
        pairs = [(point, *nearest(*point[:2])) for point in (_image(p, k, side) for p in mine)]
        used = {index for _, index, _ in pairs}
        largest = max(distance for _, _, distance in pairs)
        score = (len(used) == len(theirs) == len(mine), -largest)
        if kept is None or score > kept[0]:
            kept = (score, k, pairs, len(used))
    assert kept is not None
    _, k, pairs, used = kept
    turns = [
        min(abs(point[2] - theirs[index][2]), 90.0 - abs(point[2] - theirs[index][2]))
        for point, index, _ in pairs
    ]
    return {
        "symmetry": k,
        "one_to_one": used == len(mine) == len(theirs),
        "paired": used,
        "largest_centre_distance": f"{max(d for _, _, d in pairs):.3e}",
        "beyond": {
            limit: sum(1 for _, _, d in pairs if d > float(limit)) for limit in POSE_THRESHOLDS
        },
        "largest_rotation_difference_degrees": f"{max(turns):.3e}",
        "side_difference": f"{float(ours.side - other.side):+.3e}",
    }


def pose_identity(issue: int | str) -> dict[str, Any]:
    """A release's certificates at the counts its author asks sole credit at (`SOLE_CREDIT`),
    each measured against the row its walk records it over and against every other packet
    of `POSE_REFERENCES` that retains a certificate at the count (`measured_identity`)."""
    chosen = release(issue)
    custody(chosen)
    walk = walk_of(chosen)
    walked = _walked(walk)
    rows = {row.n: row for row in decided_claims(chosen)}
    results = []
    for n in SOLE_CREDIT[chosen.label]:
        ours = certificate(chosen, rows[n])
        start = _start_source(walked[n])
        against = []
        for packet, (label, pattern) in POSE_REFERENCES.items():
            path = pattern.format(n=n)
            source = WEB / packet / "source" / path
            if not source.exists():
                continue
            other = legacy.parse(read_retained_text(source), expected_n=n)
            against.append(
                {
                    "report": label,
                    "packet": packet,
                    "certificate": path,
                    "superseded_row": packet == start,
                    **measured_identity(ours, other),
                }
            )
        _require(
            any(item["superseded_row"] for item in against),
            f"{chosen.label} n={n}: no retained certificate of the row it supersedes ({start})",
        )
        results.append({"n": n, "certificate": rows[n].path, "against": against})
    return {
        "format": POSE_IDENTITY_FORMAT,
        "release": chosen.issue_url,
        "measure": (
            "binary64: under each of the box's eight symmetries, each square paired with the "
            "nearest centre of the other packing; the symmetry kept pairs one to one if any "
            "does, then has the least largest distance. Decides nothing."
        ),
        "rows": results,
    }


def write_pose_identity(issue: int | str) -> dict[int, list[str]]:
    """Write a release's pose-identity receipt; return each count's largest distances."""
    record = pose_identity(issue)
    _write(release(issue).path(POSE_IDENTITY), record)
    return {
        row["n"]: [
            f"{item['report']} {item['largest_centre_distance']}" for item in row["against"]
        ]
        for row in record["rows"]
    }


#: The counts where a notebook row is within 1.1e-7 of a side an earlier commit of the same
#: push states (#795's review A, A1): measured to settle refinement and credit.
PUSH_IDENTITY = (364, 378, 405, 450, 874)
PUSH_IDENTITY_RECEIPT = Path("receipts/push/pose-identity.json")
#: Where the push walk takes a row as the same packing as an earlier one of the push: its
#: squares pair one to one under a symmetry and none moves beyond this.
PUSH_SAME_PACKING = "1e-3"


def push_identity(issue: int | str) -> dict[str, Any]:
    """Each count of `PUSH_IDENTITY`: the certificate of the push's last claim there,
    measured against the certificate of every earlier claim of the push there
    (`measured_identity`), each read from the packet. A measurement: it decides nothing, and
    the walk's notes say what it is taken to show (`PUSH_SAME_PACKING`)."""
    chosen = release(issue)
    _require(chosen.claim_map == PUSH, f"{chosen.label}: not a release of one push")
    custody(chosen)
    receipt = _read(chosen.directory / PUSH_PUBLICATIONS)
    order = {item["commit"]: index for index, item in enumerate(receipt["commits"])}
    root = archive(chosen)
    rows = []
    for n in PUSH_IDENTITY:
        stated = sorted(
            (item for item in receipt["claims"] if item["n"] == n),
            key=lambda item: order[item["commit"]],
        )
        _require(len(stated) > 1, f"n={n}: the push states one side there")
        last, earlier = stated[-1], stated[:-1]
        ours = legacy.parse(read_retained_text(root / last["certificate"]), expected_n=n)
        against = []
        for item in earlier:
            other = legacy.parse(read_retained_text(root / item["certificate"]), expected_n=n)
            against.append(
                {key: item[key] for key in ("commit", "holder", "credit", "certificate")}
                | measured_identity(ours, other)
            )
        rows.append(
            {key: last[key] for key in ("n", "commit", "holder", "credit", "certificate")}
            | {"against": against}
        )
    return {
        "format": POSE_IDENTITY_FORMAT,
        "release": f"{chosen.source_url}/tree/{chosen.retained}",
        "measure": (
            "binary64: under each of the box's eight symmetries, each square paired with the "
            "nearest centre of the other packing; the symmetry kept pairs one to one if any "
            "does, then has the least largest distance. Decides nothing."
        ),
        "rows": rows,
    }


def write_push_identity(issue: int | str) -> dict[int, list[str]]:
    """Write a push walk's pose-identity receipt; return each count's largest distances."""
    record = push_identity(issue)
    _write(release(issue).directory / PUSH_IDENTITY_RECEIPT, record)
    return {
        row["n"]: [
            f"{item['commit'][:7]} {item['largest_centre_distance']}" for item in row["against"]
        ]
        for row in record["rows"]
    }


# --------------------------------------------------------------------------- coverage plan


def walk_of(chosen: Release, n: int | None = None) -> Walk:
    """The ledger walk that plans a release's row at ``n``: its own walk where that walk
    reaches ``n``, as every row to 1024 and every count by default; above it, the walk
    above 1024 that records the release there (`Release.walk_above`), which must reach it."""
    own = WALKS[chosen.walk]
    if n is None or own.reaches(n):
        return own
    _require(
        bool(chosen.walk_above) and chosen.walk_above in WALKS,
        f"{chosen.label} n={n}: no walk reaches it ({own.name} reaches {own.reach})",
    )
    above = WALKS[chosen.walk_above]
    _require(above.reaches(n), f"{chosen.label} n={n}: {above.name} does not reach it")
    return above


def walks_of(chosen: Release) -> list[Walk]:
    """Every walk that plans a release's rows: its own, then the walk above 1024."""
    own = [WALKS[chosen.walk]]
    return own + ([WALKS[chosen.walk_above]] if chosen.walk_above else [])


def _walk_groups(walk: Walk) -> dict[str, tuple[Release, ...]]:
    """The releases a walk plans, by the report label the ledger gives each, those it is the
    own walk of and those whose rows above 1024 it records (`Release.walk_above`): one a
    label, or several where one commit's publications are several sources
    (`Release.notebook_run`)."""
    groups: dict[str, list[Release]] = {}
    for item in RELEASES.values():
        if walk.name in (item.walk, item.walk_above):
            groups.setdefault(item.label, []).append(item)
    return {label: tuple(items) for label, items in groups.items()}


@functools.cache
def _mapped_counts(key: str, _modified: int) -> frozenset[int]:
    """The counts a release whose claims are re-derived claims, held ones included, read once
    while its claim map is unchanged."""
    return frozenset(int(item["n"]) for item in mapped_claims(release(key)))


def release_at(walk: Walk, report: str, n: int) -> Release | None:
    """The release of ``walk`` whose rows record ``report`` at ``n``: the label's one release,
    or, where several share it or it is a push's (`PUSH`), the one whose claims hold ``n``;
    None for a report no release of the walk is, and for another author's side of a push
    (`OTHER_AUTHOR`), which no release holds, so the walk may not record it
    (`chain_problems`)."""
    group = _walk_groups(walk).get(report, ())
    if len(group) <= 1 and not any(item.claim_map == PUSH for item in group):
        return group[0] if group else None
    found = [
        item
        for item in group
        if item.claim_map
        and n in _mapped_counts(item.key, mapped_path(item).stat().st_mtime_ns)
    ]
    if not found and all(item.claim_map == PUSH for item in group):
        return None
    _require(len(found) == 1, f"{report} n={n}: {len(found)} of its releases claim it")
    return found[0]


def _awaits(walk: Walk, report: str, n: int) -> bool:
    """Whether a report the walk records at ``n`` has no row: its import is pending
    (`Awaiting`), or its publication there waits on an owner decision (`Held`)."""
    awaiting = walk.awaiting.get(report)
    pending = awaiting is not None and (awaiting.counts is None or n in awaiting.counts)
    return pending or walk.holds(report, n) is not None


def _source_of(walk: Walk, report: str, n: int) -> str:
    """The coverage source whose rows record a report the walk records at ``n``."""
    source = _report_source(walk, report, n)
    _require(source is not None, f"{report}: the ledger walks a report no source records")
    assert source is not None
    return source


def _report_source(walk: Walk, report: str, n: int) -> str | None:
    """The coverage source of a report ``walk`` walks at ``n``: its release's there
    (`Release.source_at`), or, for a report no release of the walk is, the source the walk
    names for it (`Walk.later`), which is a split's at a count the split holds (`Split`);
    None where neither is."""
    ours = release_at(walk, report, n)
    if ours is not None:
        return ours.source_at(n)
    source = walk.later.get(report)
    owners = [item for item in RELEASES.values() if item.source == source]
    return owners[0].source_at(n) if len(owners) == 1 else source


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
        printed = {
            row["n"]: row["offered_side"]
            for record in chosen.records
            for row in _read(record)["results"]
        }
        for row in decided_claims(chosen):
            walk = walk_of(chosen, row.n)
            walked = _walked(walk)
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
                "source_id": chosen.source_at(row.n),
                "claim": "upper-bound",
                "value": printed[row.n],
                "assurance": "reported",
                "disposition": "superseded" if later else "tracked-outside-case-corpus",
            }
            if later:
                planned["superseded_by"] = _source_of(walk, later[0], row.n)
            planned["bead"] = chosen.bead_at(row.n)
            rows.append(planned)
    return rows


def unrecorded_rows() -> list[tuple[int, str]]:
    """The decided rows each walk does not record, ``(n, source)``: no row may hold them."""
    found: list[tuple[int, str]] = []
    for chosen in RELEASES.values():
        for row in decided_claims(chosen):
            steps = _walked(walk_of(chosen, row.n)).get(row.n, {"steps": []})["steps"]
            if any(
                step["report"] == chosen.label and step["verdict"] == NOT_RECORDED
                for step in steps
            ):
                found.append((row.n, chosen.source_at(row.n)))
    return found


def _start_source(count: Mapping[str, Any]) -> str | None:
    """The source of a walked count's start, where a member of the start is a beyond-horizon
    row (a count the grid, a case or a register entry held has none). A start read from 23
    October 2026 may hold Göbel's construction beside the row, and a count in the corpus
    both case lanes; at most one member is a row."""
    found = [
        match[1]
        for start in count["start"]
        if (match := _START_ROW.fullmatch(start["label"])) is not None
    ]
    _require(len(found) <= 1, f"n={count['n']}: the start holds {len(found)} rows")
    return found[0] if found else None


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
        for count in _counts(walk):
            recorded = recorded_reports(walk, count)
            start = _start_source(count)
            ours = release_at(walk, recorded[0], count["n"]) if recorded else None
            if start is not None and ours is not None:
                flips.append((walk, count["n"], start, ours.source_at(count["n"])))
    return flips


def held_problems(register: Mapping[str, Any]) -> list[str]:
    """Where a walk's declared holds (`Held`) do not hold: each names a known class and a
    bead, holds each count once, and holds only a publication the walk records there, which
    no register row and no declared row of the report may then hold."""
    rows = {(row["n"], row["source_id"]) for row in register["beyond_horizon_claims"]}
    problems: list[str] = []
    for walk in WALKS.values():
        walked = _walked(walk)
        groups = _walk_groups(walk)
        for report, items in walk.held.items():
            declared = {
                row.n for item in groups.get(report, ()) for row in decided_claims(item)
            }
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
                    source = _report_source(walk, report, n)
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


def registered_corpus_counts(packet: str) -> set[int]:
    """The corpus counts the results register holds from a packet: the scope of every entry
    that names one of the packet's files among its artifacts."""
    prefix = f"packing/resources/web/{packet}/"
    entries = safe_load(RESULTS.read_text(encoding="utf-8"))["results"]
    return {
        int(n)
        for entry in entries
        if any(str(path).startswith(prefix) for path in entry.get("artifacts") or ())
        for n in (entry.get("scope") or {}).get("n_values") or ()
        if int(n) <= reports.HORIZON
    }


def declaration_problems() -> list[str]:
    """Where a release that declares its rows (`declares_rows`) declares other rows than its
    walk makes: every claim the walk records of it beyond the corpus, and does not hold, is a
    declared row, and no other. A count in the corpus the walk records and does not hold is
    no row: a registered result must hold it from the release's packet
    (`registered_corpus_counts`), as T-240 holds #763's 268 and 303 (#789's review B, B2)."""
    problems: list[str] = []
    for chosen in RELEASES.values():
        if not declares_rows(chosen):
            continue
        walked = {
            n
            for walk in walks_of(chosen)
            for n, count in _walked(walk).items()
            if walk.reaches(n)
            for step in count["steps"]
            if step["report"] == chosen.label
            and step["verdict"] == RECORDED
            and walk.holds(chosen.label, n) is None
            and release_at(walk, chosen.label, n) is chosen
        }
        recorded = {n for n in walked if n > reports.HORIZON}
        corpus = walked - recorded
        if corpus:
            registered = registered_corpus_counts(chosen.packet)
            problems.extend(
                f"{chosen.label} n={n}: the walk records a count in the corpus, and no "
                f"registered result holds it from the {chosen.packet} packet"
                for n in sorted(corpus - registered)
            )
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
    current, or superseded by a report the walk does not reach. Each walk is held at the
    counts it reaches (`Walk.reaches`): a count it walks beyond them, as the #719 walk's
    claims above 1024, is another walk's. Where two walks reach a count, a
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
            if n <= reports.HORIZON or not walk.reaches(n):
                continue
            start = _start_source(count)
            chain = ([start] if start is not None else []) + [
                _source_of(walk, report, n) for report in recorded_reports(walk, count)
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
        reached.add(_report_source(walk, report, n))
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
    """Where a register row beyond the corpus is not marked as the owner's answer of 23
    October 2026 on #613 requires (think-8krd): a row at or above Göbel's construction at its
    count, as `devtools.intake_ledger.goebel_form` reads the maintained module at any count,
    is marked ``above-classical-construction`` with that construction, and a row
    so marked is above it. A row is read at its exact side where its source's claims
    record states one, else as low as its print allows."""
    from devtools import check_source_coverage as coverage_check  # noqa: PLC0415
    from devtools import intake_ledger  # noqa: PLC0415

    sources = {str(source["id"]): source for source in register["sources"]}
    problems: list[str] = []
    for row in register["beyond_horizon_claims"]:
        n, value = int(row["n"]), str(row["value"])
        if n <= reports.HORIZON:
            continue
        where = f"n={n} from {row['source_id']}"
        marked = row.get("disposition") == coverage_check.ABOVE_CONSTRUCTION
        try:
            form = intake_ledger.goebel_form(n)
        except intake_ledger.LedgerError as error:
            problems.append(f"{where}: {error}")
            continue
        assert form is not None
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
    releases = {source: item for item in RELEASES.values() for source in item.sources}
    problems = []
    for row in planned_rows():
        held = rows.get((row["n"], row["source_id"]))
        walk = walk_of(releases[row["source_id"]], row["n"])
        if held != row and not (
            held is not None and _superseded_after(row, held, walk, register)
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


def split_problems(chosen: Release) -> list[str]:
    """Where a release's split (`Split`) does not hold: it names a source, bead and claims
    record of its own, and each count it holds is a decided row of the release that its
    walk records, so the split's source holds exactly the rows it names."""
    split = chosen.split
    if split is None:
        return []
    where = f"{chosen.label}: the split {split.source_id}"
    problems = [
        f"{where} {problem}"
        for problem, failed in (
            ("is the release's own source", split.source_id == chosen.source),
            ("names the release's claims record", split.record == chosen.record),
            ("holds no count", not split.counts),
            ("names no decision's bead", not _BEAD.fullmatch(split.bead)),
        )
        if failed
    ]
    decided = {row.n for row in decided_claims(chosen)}
    unrecorded = {n for n, source in unrecorded_rows() if source in chosen.sources}
    problems.extend(
        f"{where} holds n={n}, which is not a row of the release its walk records"
        for n in sorted(split.counts)
        if n not in decided or n in unrecorded
    )
    return problems


def release_problems(chosen: Release, *, replay: bool, workers: int) -> list[str]:
    """Problems with one packet's receipts and record; empty when they hold."""
    custody(chosen)
    decided = decided_claims(chosen)
    rows = [row for row in decided if row.recipe is None]
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
            again = list(pool.map(decide_row, [(chosen.key, row.n) for row in rows]))
        problems.extend(
            f"{chosen.label} n={row.n}: the replay differs from the receipt"
            for row, kept, fresh in zip(rows, stored, again, strict=True)
            if _stable(fresh) != _stable(kept)
        )
    problems += recipe_problems(chosen, replay=replay, workers=workers)
    for record, part in split_records(chosen, beyond_horizon_rows(chosen, sides)).items():
        rebuilt = retained_dumps(part, sort_keys=True)
        if not record.is_file() or record.read_text(encoding="utf-8") != rebuilt:
            which = f" {record.name}" if chosen.split is not None else ""
            problems.append(
                f"{chosen.label}: the beyond-horizon record{which} differs from its rebuild"
            )
    return problems + split_problems(chosen) + _cross_check_problems(chosen, decided, sides)


def _cross_check_problems(
    chosen: Release, rows: Sequence[Claim], decided: Mapping[int, Fraction]
) -> list[str]:
    """The first commits', the all-pairs sample's and the Göbel receipt's outcomes; the
    Göbel receipt must also be its rebuild byte for byte (`goebel_receipt`).

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
        expected = retained_blobs(chosen, held)
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
    unrecorded = {n for n, source in unrecorded_rows() if source in chosen.sources}
    sides = [(row.n, decided[row.n]) for row in rows]
    if [(n, side) for n, side, _ in compared] != sides or any(
        relation != "below" for n, _, relation in compared if n not in unrecorded
    ):
        problems.append(f"{chosen.label}: a decided side is not below Göbel's construction")
    rebuilt = retained_dumps(goebel_receipt(chosen, decided), sort_keys=True)
    if chosen.path(GOEBEL).read_text(encoding="utf-8") != rebuilt:
        problems.append(f"{chosen.label}: the Göbel receipt differs from its rebuild")
    return problems


def retained_blobs(chosen: Release, rows: Sequence[Claim]) -> list[tuple[int, str, str]]:
    """Each row's count, certificate and Git blob, as the first-commits receipt lists
    them, from one `Hosting` for the whole list (#793's review A, A3)."""
    hosting = Hosting(chosen)
    return [
        (row.n, row.path, blob_of(chosen, row.path, row.certificate_n, hosting)) for row in rows
    ]


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


#: How a command names a release: an issue's number, or a ledger label.
KEY_HELP = (
    "an issue's number, a comment's label '#N comment ID', or a publication's label "
    "owner/name@commit"
)


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
    own_history.add_argument("--walk", default="", help="a walk of WALKS; the release's own")
    one_push = commands.add_parser("push-publications")
    one_push.add_argument("--issue", required=True, help=KEY_HELP)
    one_push.add_argument("--clone", type=Path, required=True)
    before_push = commands.add_parser("earlier-push")
    before_push.add_argument("--issue", required=True, help=KEY_HELP)
    before_push.add_argument("--clone", type=Path, required=True)
    before_push.add_argument("--read-on", default="", help="before gather freezes the starts")
    push_pose = commands.add_parser("push-identity")
    push_pose.add_argument("--issue", required=True, help=KEY_HELP)
    after_pin = commands.add_parser("later-commits")
    after_pin.add_argument("--issue", required=True, help=KEY_HELP)
    after_pin.add_argument("--clone", type=Path, required=True)
    decide_after = commands.add_parser("decide-later")
    decide_after.add_argument("--issue", required=True, help=KEY_HELP)
    identity = commands.add_parser("pose-identity")
    identity.add_argument("--issue", required=True, help=KEY_HELP)
    transcribe_release = commands.add_parser("release-sources")
    transcribe_release.add_argument("--issue", required=True, help=KEY_HELP)
    transcribe_release.add_argument("--read-on", required=True)
    transcribe_release.add_argument("--walk", default="", help="a walk of WALKS")
    decide_recipes = commands.add_parser("recipe-decisions")
    decide_recipes.add_argument("--issue", nargs="+", required=True, help=KEY_HELP)
    decide_recipes.add_argument("--workers", type=int, default=2)
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
        "source-history": lambda: write_source_history(
            args.issue, args.clone, WALKS[args.walk] if args.walk else None
        ),
        "later-commits": lambda: write_later_commits(args.issue, args.clone),
        "push-publications": lambda: write_push_publications(args.issue, args.clone),
        "earlier-push": lambda: write_earlier_push(args.issue, args.clone, args.read_on),
        "push-identity": lambda: write_push_identity(args.issue),
        "decide-later": lambda: write_decide_later(args.issue),
        "pose-identity": lambda: write_pose_identity(args.issue),
        "release-sources": lambda: write_release_walk_sources(
            args.issue, args.read_on, WALKS[args.walk] if args.walk else None
        ),
        "recipe-decisions": lambda: write_recipe_decisions(args.issue, args.workers),
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
        named = ", ".join(item.key for item in chosen)
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
