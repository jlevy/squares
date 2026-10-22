"""Decide the beyond-horizon rows of a report exactly, from its retained packet.

A report beyond the ``n <= 324`` corpus is recorded as dated beyond-horizon rows of its
source, at assurance ``reported``, once its certificates are retained and replayed here.
Issues #678 and #715 each had a module of their own (`devtools.couzo_678_replay`,
`devtools.couzo_715_replay`); this one takes the same filtered decision and declares each
report it decides as a `Release`, so a further report of the same kind is a declaration and
not a module. `RELEASES` holds five, each decided at or below ``LIMIT = 1024``:

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
first. A report the walk records whose own import has not yet landed (`Awaiting`: Couzo's
4e4c8ce and 5a299b4 publications, and #715's re-certifications held on think-fwa9) has no
row, so the chain passes over it until that import writes one. ``check`` holds
``frontier/source-coverage.yaml`` to that plan, and holds every count a walk reaches beyond
the corpus to ``LIMIT`` to one chain in report order (`chain_problems`): the start, then
each recorded report's row, each superseded by the next, the last current or superseded by
a report the walk does not reach. A planned current row the register shows superseded by
such a later report holds the plan too (`coverage_problems`).

**Earlier publications.** ``earlier`` reads clones of the watched repositories and writes
``receipts/earlier-publications.json`` for a release: at each of its counts, every
certificate and index bound published before the release's row, strictly below the record's
standing side there, with the commit that first held it. The release's ledger transcribes
them as reports (``ledger-sources``).

From ``packing/``, with the project interpreter::

    python -m devtools.beyond_horizon_replay filtered [--issue N ...] [--workers 2]
    python -m devtools.beyond_horizon_replay first-commits --issue N --clone CLONE
    python -m devtools.beyond_horizon_replay exhaustive --issue N --n 922 [--workers 2]
    python -m devtools.beyond_horizon_replay goebel
    python -m devtools.beyond_horizon_replay claims-record
    python -m devtools.beyond_horizon_replay earlier --issue 719 --couzo CLONE
    python -m devtools.beyond_horizon_replay ledger-sources --issue 719
    python -m devtools.beyond_horizon_replay coverage-plan
    python -m devtools.beyond_horizon_replay check [--replay [--workers 2]]

A finite packing certifies an upper bound and nothing more: novelty, rigidity and
optimality are not decided here, and neither are the sources' credit and lineage
statements, which the receipt copies from the per-count metadata where a packet retains it.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import re
import subprocess
import time
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

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
RECORDED, NOT_RECORDED = "recorded", "not recorded"
#: How an issue prints a side: rounded up at 12 places, or as the binary64 value of the
#: exact side at 16 places, which may lie below it (#719).
UP, BINARY64 = "up", "binary64"
_START_ROW = re.compile(r"beyond-horizon row (\S+)")


@dataclass(frozen=True, slots=True)
class Awaiting:
    """A report a walk records whose rows are its own import's and not yet in the register.

    ``counts`` limits it to those counts (None: every count); ``bead`` owns the import. The
    chain at such a count passes over the report until that import lands, when the walk's
    declaration names its source instead.
    """

    bead: str
    counts: frozenset[int] | None = None


@dataclass(frozen=True, slots=True)
class Walk:
    """A report-order ledger, ``campaign/issue-intake/<name>/``, whose verdicts plan rows.

    ``later`` maps each report the walk records after its releases to the source whose
    dated rows record it; ``awaiting`` names the reports it records that have no rows yet.
    """

    name: str
    later: Mapping[str, str]
    awaiting: Mapping[str, Awaiting]

    @property
    def directory(self) -> Path:
        return INTAKE / self.name

    @property
    def ledger(self) -> Path:
        return self.directory / "ledger.json"


def _held_715() -> frozenset[int]:
    """#715's re-certifications of Couzo's 4e4c8ce certificates below the print, which the
    22 October ledger left to a decision (think-fwa9), as #715's committed receipt sets them."""
    return frozenset(couzo_715.counts_in(couzo_715.HELD))


BACKLOG = "upper-bounds-backlog-20261022"
ISSUE_719 = "upper-bounds-issue719-20261022"
#: The walk of each ledger these releases' rows are planned from. The backlog ledger's
#: starts were frozen at the 18 October ledger's ``main``; #719's at ``main`` after #720.
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
        later={},
        awaiting={
            "franciscouzo/square-packing@4e4c8ce": Awaiting("think-yfoo"),
            "franciscouzo/square-packing@23aff0c": Awaiting("think-tmwt"),
            "franciscouzo/square-packing@5a299b4": Awaiting("think-tmwt"),
            "#715": Awaiting("think-fwa9", _held_715()),
        },
    ),
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
    time rather than the issue's opening (#722's review A, A4).
    """

    issue: int
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

    @property
    def directory(self) -> Path:
        return WEB / self.packet

    @property
    def issue_url(self) -> str:
        return f"https://github.com/jlevy/squares/issues/{self.issue}"

    def first_commit_of(self, n: int) -> tuple[str, str]:
        """The commit that first holds the certificate a row at ``n`` reads, and its time."""
        later = self.later_commits or {}
        return later.get(n, (self.first_commit, self.committed))


def _couzo_rows(body: str, release: Release) -> list[Claim]:
    rows: list[Claim] = []
    for line in body.splitlines():
        match = _COUZO_ROW.match(line.strip())
        if match is None:
            continue
        _require(
            match[6] == release.pin, f"#{release.issue} n={match[1]}: links another commit"
        )
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
            f"#{release.issue} n={row.n}: the link and the deletion do not agree",
        )
    return rows


def _de_winter_rows(body: str, release: Release) -> list[Claim]:
    _require(_DE_WINTER_LINK in body, f"#{release.issue}: the issue links another folder")
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
        f"#{release.issue}: the issue links another commit",
    )
    printed: dict[int, tuple[str, str]] = {}
    files: dict[int, tuple[str, str]] = {}
    for line in body.splitlines():
        if match := _MISHAPOLK_ROW.fullmatch(line.strip()):
            printed[int(match[1])] = (match[2], match[3])
        elif match := _MISHAPOLK_FILE.fullmatch(line.strip()):
            files[int(match[1])] = (match[2], match[3])
    _require(printed.keys() == files.keys(), f"#{release.issue}: the two tables differ")
    pinned = manifest(release)
    rows: list[Claim] = []
    for n in printed:
        path, digest = files[n]
        _require(pinned.get(path) == digest, f"#{release.issue} n={n}: not the pinned digest")
        rows.append(Claim(n, printed[n][1], printed[n][0], path, n, 0))
    return rows


COUZO_URL = "https://github.com/franciscouzo/square-packing"
RELEASES: dict[int, Release] = {
    release.issue: release
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
        ),
    )
}


def release(issue: int) -> Release:
    """The declared release of an issue."""
    _require(issue in RELEASES, f"#{issue}: no declared release")
    return RELEASES[issue]


def claims(chosen: Release) -> list[Claim]:
    """Every row of the issue's table, read from its retained body, refused unless all are."""
    body = json.loads((chosen.directory / ISSUE).read_text(encoding="utf-8"))["body"]
    rows = chosen.read(body, chosen)
    _require(len(rows) == chosen.rows, f"#{chosen.issue}: {len(rows)} rows, not {chosen.rows}")
    counts = [row.n for row in rows]
    _require(counts == sorted(set(counts)), f"#{chosen.issue}: rows out of order")
    return rows


def decided_claims(chosen: Release) -> list[Claim]:
    """The rows beyond the corpus at or below ``LIMIT``, which this module decides."""
    rows = [row for row in claims(chosen) if reports.HORIZON < row.n <= LIMIT]
    _require(
        len(rows) == chosen.decided,
        f"#{chosen.issue}: {len(rows)} rows beyond the corpus to {LIMIT}, not {chosen.decided}",
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
        _require(row.certificate_n in facts, f"#{chosen.issue} n={row.n}: no derived fact")
        declared = {
            item["n"]: item["path"]
            for item in reports.load_declaration(chosen.directory)["certificates"]
        }
        _require(
            declared[row.certificate_n] == row.path,
            f"#{chosen.issue} n={row.n}: the fact is not of the issue's file",
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
        f"#{chosen.issue}: the claim record does not state every decided side",
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


def decide_row(job: tuple[int, int]) -> dict[str, Any]:
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


def _jobs(chosen: Sequence[Release]) -> list[tuple[int, int]]:
    """Every decided row of the chosen releases, the largest certificates first: a
    certificate's work grows with its count, which the issue row names, so no file is read
    to order the jobs."""
    jobs = [
        (row.certificate_n, item.issue, row.n)
        for item in chosen
        for row in decided_claims(item)
    ]
    return [(issue, n) for _, issue, n in sorted(jobs, key=lambda job: -job[0])]


def filtered(issues: Sequence[int], workers: int) -> dict[int, dict[str, Any]]:
    """Decide every decided row and control of the chosen releases, one receipt a packet."""
    chosen = [release(issue) for issue in issues]
    for item in chosen:
        custody(item)
    started = datetime.now(UTC)
    wall = time.monotonic()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        decided = dict(zip(_jobs(chosen), pool.map(decide_row, _jobs(chosen)), strict=True))
    elapsed = round(time.monotonic() - wall, 1)
    receipts: dict[int, dict[str, Any]] = {}
    for item in chosen:
        results = [decided[item.issue, row.n] for row in decided_claims(item)]
        receipt: dict[str, Any] = {
            "format": FILTERED_FORMAT,
            "issue": item.issue_url,
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
            "run_releases": [other.issue for other in chosen],
            "workers": workers,
            "rows": results,
            "summary": base.summary(results),
        }
        _write(item.directory / FILTERED, receipt)
        receipts[item.issue] = receipt
    return receipts


# --------------------------------------------------------------------------- first commits


def _git(clone: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(clone), *args], capture_output=True, text=True, check=True
    ).stdout


def first_commits(issue: int, clone: Path) -> dict[str, Any]:
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
    _write(chosen.directory / FIRST_COMMITS, receipt)
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
        f"#{chosen.issue} n={row.n}: the clone's file is not the pinned one",
    )
    return blob


def _utc(stamp: str) -> str:
    return datetime.fromisoformat(stamp).astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------- cross-checks


def exhaustive_row(job: tuple[int, int]) -> dict[str, Any]:
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


def exhaustive(issue: int, counts: Sequence[int], workers: int) -> dict[str, Any]:
    """The all-pairs kernel on chosen rows of one release, each against the filtered one."""
    chosen = release(issue)
    custody(chosen)
    decided = {row.n for row in decided_claims(chosen)}
    for n in counts:
        _require(n in decided, f"#{issue} n={n}: not a decided row")
    started = datetime.now(UTC)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(exhaustive_row, [(issue, n) for n in counts]))
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
    _write(chosen.directory / EXHAUSTIVE, receipt)
    return receipt


def _goebel_program() -> Any:
    """The 15 October packet's exact Göbel comparison, loaded from its retained path."""
    spec = importlib.util.spec_from_file_location("goebel_beyond_horizon", base.GOEBEL_PROGRAM)
    if spec is None or spec.loader is None:
        raise ReplayError("the Göbel program is missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def goebel() -> dict[int, dict[str, Any]]:
    """Every decided side against Göbel's classical constructions, exactly.

    The families, their deletion to smaller counts and the sign test are those of the 15
    October packet's retained ``goebel_beyond_horizon.py``, read from its path unchanged;
    its ``LIMIT`` of 1100 covers every count decided here.
    """
    program = _goebel_program()
    _require(program.LIMIT >= LIMIT, "the Göbel program stops below the decided counts")
    forms = program.families(program.LIMIT)
    tallies: dict[int, dict[str, Any]] = {}
    for chosen in RELEASES.values():
        custody(chosen)
        sides = decided_sides(chosen)
        rows = [(row.n, sides[row.n], row.path) for row in decided_claims(chosen)]
        result = program.compare(f"issue #{chosen.issue} at {chosen.pin[:8]}", rows, forms)
        _write(
            chosen.directory / GOEBEL,
            {
                "format": GOEBEL_FORMAT,
                "program": base.GOEBEL_PROGRAM.relative_to(REPO).as_posix(),
                "families": (
                    "Göbel squares, Göbel strips and corner-touching strips, with deletion"
                ),
                "comparison": result,
            },
        )
        tallies[chosen.issue] = {"rows": result["rows"], "tally": result["tally"]}
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
    unrecorded = {n for n, source in unrecorded_rows() if source == chosen.packet}
    for row in decided_claims(chosen):
        if row.n in unrecorded:
            continue
        side = sides[row.n]
        _require(
            print_holds(chosen, side, row.printed),
            f"#{chosen.issue} n={row.n}: the print is not the side's {chosen.rounding} print",
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
        "issue": chosen.issue_url,
        "source": chosen.source_url,
        "revision": chosen.retained,
        "issue_pin": chosen.pin,
        "horizon": reports.HORIZON,
        "limit": LIMIT,
        "results": results,
    }
    if chosen.rounding != UP:
        record["issue_rounding"] = chosen.rounding
    return record


def claims_record() -> dict[int, int]:
    """Write each packet's beyond-horizon record and return its row counts."""
    written: dict[int, int] = {}
    for chosen in RELEASES.values():
        record = beyond_horizon_rows(chosen)
        _write(chosen.directory / RECORD, record)
        written[chosen.issue] = len(record["results"])
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


def _row_side(source: Mapping[str, Any], n: int, printed: str) -> Fraction:
    """A beyond-horizon row's side: the exact side its source's claims record states, or,
    where that record keeps none, the row's print."""
    record = json.loads(read_retained_text(ROOT / source["claims_record"]))
    found = [item for item in record.get("results", []) if int(item["n"]) == n]
    if found and "exact_side" in found[0]:
        return Fraction(found[0]["exact_side"])
    return Fraction(printed)


def _standing(chosen: Release) -> dict[int, Fraction]:
    """Each claimed count's standing side as the packet's frozen claim record read the
    record: the case's exact side in the corpus, else the exact side of the row that stood
    there, read from its source's claims record, or the grid; a count above ``LIMIT``, which
    no record holds yet, stands at the grid."""
    record = _read(chosen.directory / reports.CLAIMS)
    coverage = safe_load(COVERAGE.read_text(encoding="utf-8"))
    sources = {source["id"]: source for source in coverage["sources"]}
    standing = {row.n: reports.grid_side(row.n) for row in claims(chosen)}
    for row in record["results"]:
        n = row["n"]
        if row["case"] is not None:
            standing[n] = Fraction(row["case"]["exact_side"])
            continue
        rows = [
            _row_side(sources[item["report"]], n, item["printed"])
            for item in row["pending"]
            if "printed" in item
        ]
        standing[n] = min([*rows, Fraction(row["grid_side"])])
    return standing


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
        _require(clone is not None, f"#{chosen.issue} n={row.n}: no clone to read it from")
        assert clone is not None
        blob = _pinned_blob(chosen, row, clone)
        header = _header(_blobs(clone, [blob])[blob])
        _require(header is not None and header[0] == row.n, f"n={row.n}: no header")
        assert header is not None
        sides[row.n] = header[1]
    return sides


def earlier_publications(
    issue: int, clones: Mapping[str, Path], source: Path | None = None
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
            if when >= chosen.first_commit_of(n)[1] or side >= standing[n]:
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
                if when >= chosen.first_commit_of(n)[1] or side >= standing[n]:
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
                "standing": legacy.literal(standing[n]),
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
    issue: int, clones: Mapping[str, Path], source: Path | None
) -> dict[int, int]:
    """Write a release's earlier-publications receipt; return each count's publications."""
    record = earlier_publications(issue, clones, source)
    _write(release(issue).directory / EARLIER, record)
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


def ledger_sources(issue: int, read_at_main: str, read_on: str) -> dict[str, Any]:
    """The ``sources.yaml`` a release's walk reads, transcribed from the packets' receipts
    (`devtools.intake_ledger` gathers it).

    The reports are the release's own rows, at their exact sides, and every earlier report
    at its counts no row holds: each publication the release's earlier-publications receipt
    lists, at its exact side; #715's rows at the counts it re-certified below the print
    (think-fwa9) and above ``LIMIT``, and #666's above ``LIMIT``, which wait on the owner
    (D1). A claim the start already holds is not walked again.
    """
    chosen = release(issue)
    walk = walk_of(chosen)
    earlier = _read(chosen.directory / EARLIER)
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
                    "bead": walk.awaiting[label].bead
                    if label in walk.awaiting
                    else chosen.bead,
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
            f"#{issue} claims where it is strictly below the record's standing side. Its rows "
            f"are its own import's ({group['bead']}); none is recorded by this pass."
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
                "that packet's filtered replay, which wait on a decision (think-fwa9), and "
                "its rows above 1024, at the exact sides of the certificates the issue "
                "links, which wait on the owner (think-f2io). None is recorded by this pass. "
                "Its other rows at these counts, at 410, 413, 454, 490, 498, 544, 584, 596, "
                "637, 644, 689, 692, 699, 736, 743, 744, 746, 792 and 800, state the 4e4c8ce "
                "certificates' sides exactly, the same holder's, so they are not walked: each "
                "would be an exact tie, not recorded, and move nothing."
            ),
        },
        {
            "report": f"#{issue}",
            "issue": issue,
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
            ),
        },
    ]
    return {
        "format": "intake-ledger-sources-v1",
        "read_at_main": read_at_main,
        "read_on": read_on,
        "rule": RULE,
        "lanes": [],
        "reports": [report for report in reports_list if report["claims"]],
    }


def release_715_claims(
    counts: set[int], by_n: Mapping[int, Mapping[str, Any]]
) -> list[dict[str, Any]]:
    """#715's claims at ``counts`` that no row holds: its held re-certifications, at the
    exact sides its packet's filtered receipt states, and its rows above ``LIMIT``, at the
    side of the publication the earlier-publications receipt found its print to round up."""
    packet = WEB / "couzo-issue715-2026-10-21"
    held = WALKS[ISSUE_719].awaiting["#715"].counts or frozenset()
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


def write_ledger_sources(issue: int, read_at_main: str, read_on: str) -> int:
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


# --------------------------------------------------------------------------- coverage plan


def walk_of(chosen: Release) -> Walk:
    """The ledger walk that plans a release's rows."""
    return WALKS[chosen.walk]


def _releases(walk: Walk) -> dict[str, Release]:
    """The releases a walk plans, by the report label the ledger gives each."""
    return {f"#{issue}": item for issue, item in RELEASES.items() if item.walk == walk.name}


def _awaits(walk: Walk, report: str, n: int) -> bool:
    """Whether a report the walk records at ``n`` has no row yet: its import is pending."""
    awaiting = walk.awaiting.get(report)
    return awaiting is not None and (awaiting.counts is None or n in awaiting.counts)


def _source_of(walk: Walk, report: str) -> str:
    """The coverage source whose rows record a report the walk records."""
    ours = {label: item.packet for label, item in _releases(walk).items()}
    source = ours.get(report) or walk.later.get(report)
    _require(source is not None, f"{report}: the ledger walks a report no source records")
    assert source is not None
    return source


def _counts(walk: Walk) -> list[dict[str, Any]]:
    return _read(walk.ledger)["counts"]


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
            row["n"]: row["offered_side"] for row in _read(chosen.directory / RECORD)["results"]
        }
        for row in decided_claims(chosen):
            _require(row.n in walked, f"#{chosen.issue} n={row.n}: the ledger does not walk it")
            steps = walked[row.n]["steps"]
            (mine,) = [
                i for i, step in enumerate(steps) if step["report"] == f"#{chosen.issue}"
            ]
            if steps[mine]["verdict"] == NOT_RECORDED:
                continue
            _require(
                steps[mine]["verdict"] == RECORDED,
                f"#{chosen.issue} n={row.n}: the ledger does not record it",
            )
            later = [
                step["report"]
                for step in steps[mine + 1 :]
                if step["verdict"] == RECORDED and not _awaits(walk, step["report"], row.n)
            ]
            planned: dict[str, Any] = {
                "n": row.n,
                "source_id": chosen.packet,
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
                step["report"] == f"#{chosen.issue}" and step["verdict"] == NOT_RECORDED
                for step in steps
            ):
                found.append((row.n, chosen.packet))
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
    flips: list[tuple[int, str, str]] = []
    for walk in WALKS.values():
        ours = {label: item.packet for label, item in _releases(walk).items()}
        for count in _counts(walk):
            recorded = recorded_reports(walk, count)
            start = _start_source(count)
            if start is not None and recorded and recorded[0] in ours:
                flips.append((count["n"], start, ours[recorded[0]]))
    return sorted(flips)


def chain_problems(coverage: Mapping[str, Any]) -> list[str]:
    """Where a count a walk reaches beyond the corpus is not one chain in report order.

    The chain is the count's start, where it is a beyond-horizon row, then the row of each
    report the walk records, in report order, passing over a report whose import is pending
    (`Awaiting`). Each must be in the register and superseded by the next; the last is
    current, or superseded by a report the walk does not reach. Counts above ``LIMIT``
    have no rows yet (the owner's D1) and are not held.
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
                if later is not None and (disposition, successor) != ("superseded", later):
                    problems.append(
                        f"n={n} from {earlier}: {disposition} naming {successor}, "
                        f"not superseded by {later}"
                    )
                elif later is None and successor in chain:
                    problems.append(
                        f"n={n} from {earlier}: names {successor}, earlier in the chain"
                    )
    return problems


def _reached(walk: Walk, n: int) -> set[str]:
    """Every source a walk reaches at ``n``: its start's and each walked report's."""
    count = next((item for item in _counts(walk) if item["n"] == n), None)
    if count is None:
        return set()
    reached = {_start_source(count)}
    for step in count["steps"]:
        report = step["report"]
        source = {label: item.packet for label, item in _releases(walk).items()}.get(report)
        reached.add(source or walk.later.get(report))
    return {source for source in reached if source is not None}


def _superseded_after(
    plan: Mapping[str, Any], held: Mapping[str, Any], walk: Walk, register: Mapping[str, Any]
) -> bool:
    """Whether a row the plan calls current is held superseded by a report its walk does
    not reach: a later import's row, as `chain_problems` allows (#720's review B, B1). The
    held row must be the plan's but for its disposition and successor, and the successor
    must hold a row at the count strictly below it, from a source dated no earlier than the
    row's own, so the plan does not rest on `check_source_coverage` (#722's review A, A5).
    A successor dated the same day is not ordered by the day, as that gate does not."""
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
        if row["n"] == plan["n"] and row["source_id"] == successor
    ]
    own = dated.get(str(plan["source_id"]), "")
    return (
        len(later) == 1
        and bool(own)
        and dated.get(str(successor), "") >= own
        and Fraction(str(later[0]["value"])) < Fraction(str(plan["value"]))
    )


def coverage_problems(coverage: Mapping[str, Any] | None = None) -> list[str]:
    """Where the coverage register differs from the plan: each planned row, as written, or
    superseded by a report its walk does not reach where the plan calls it current; no row
    for a decided row its walk does not record; each start a release's row beat first naming
    the release's source as its successor; and each walked count one chain in report order.
    ``coverage`` is the register as `safe_load` reads it, by default the checkout's."""
    register: Mapping[str, Any] = (
        safe_load(COVERAGE.read_text(encoding="utf-8")) if coverage is None else coverage
    )
    rows = {(row["n"], row["source_id"]): row for row in register["beyond_horizon_claims"]}
    walks = {item.packet: walk_of(item) for item in RELEASES.values()}
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
    for n, earlier, successor in planned_supersessions():
        held = rows.get((n, earlier)) or {}
        if (held.get("disposition"), held.get("superseded_by")) != ("superseded", successor):
            problems.append(f"n={n} from {earlier}: not superseded by {successor}")
    return problems + chain_problems(register)


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
    where = f"#{chosen.issue} n={row.n}"
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
        f"#{chosen.issue} n={row.n}: deletes from n{row.certificate_n}, which no row of the "
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
            f"#{chosen.issue}: the all-pairs sample decides "
            f"{[item['n'] for item in sample]}, not the declared {list(chosen.sampled)}"
        )
    decided = {row.n for row in rows}
    problems.extend(
        f"#{chosen.issue} n={item['n']}: the all-pairs sample disagrees with the filtered one"
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
    receipt = _read(chosen.directory / FILTERED)
    stored = receipt["rows"]
    if [row["n"] for row in stored] != [row.n for row in rows]:
        return [f"#{chosen.issue}: the filtered receipt's rows are not the issue's"]
    problems = deletion_problems(chosen, rows)
    sides = decided_sides(chosen)
    for row, kept in zip(rows, stored, strict=True):
        problems.extend(row_problems(chosen, row, kept))
        if Fraction(kept["exact_side"]) != sides[row.n]:
            problems.append(
                f"#{chosen.issue} n={row.n}: the receipt's side is not the header's"
            )
    if receipt["summary"] != base.summary(stored):
        problems.append(f"#{chosen.issue}: the summary does not match the rows")
    if replay:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            again = list(pool.map(decide_row, [(chosen.issue, row.n) for row in rows]))
        problems.extend(
            f"#{chosen.issue} n={row.n}: the replay differs from the receipt"
            for row, kept, fresh in zip(rows, stored, again, strict=True)
            if _stable(fresh) != _stable(kept)
        )
    record = chosen.directory / RECORD
    if not record.is_file() or _read(record) != beyond_horizon_rows(chosen):
        problems.append(f"#{chosen.issue}: the beyond-horizon record differs from its rebuild")
    return problems + _cross_check_problems(chosen, rows)


def _cross_check_problems(chosen: Release, rows: Sequence[Claim]) -> list[str]:
    """The first commits', the all-pairs sample's and the Göbel receipt's outcomes.

    A retained certificate's Git blob is rebuilt from its bytes; a derived packet keeps
    none, so its receipt's SHA-256 must be the one the packet pins. Every side the walk
    records must be below Göbel's construction; a side it does not record, as #719's 366,
    is held to the receipt as compared.
    """
    problems: list[str] = []
    commits = _read(chosen.directory / FIRST_COMMITS)
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
        problems.append(
            f"#{chosen.issue}: the first commits are not the retained certificates'"
        )
    problems.extend(
        f"#{chosen.issue} n={item['n']}: first committed at {item['first_commit'][:8]}, "
        f"not {chosen.first_commit_of(item['n'])[0][:8]} as the record states"
        for item in commits["rows"]
        if (item["first_commit"], item["committed"]) != chosen.first_commit_of(item["n"])
    )
    problems.extend(sample_problems(chosen, rows, _read(chosen.directory / EXHAUSTIVE)["rows"]))
    comparison = _read(chosen.directory / GOEBEL)["comparison"]
    compared = [
        (item["n"], Fraction(item["side"]), item["relation"]) for item in comparison["detail"]
    ]
    unrecorded = {n for n, source in unrecorded_rows() if source == chosen.packet}
    decided = decided_sides(chosen)
    sides = [(row.n, decided[row.n]) for row in rows]
    if [(n, side) for n, side, _ in compared] != sides or any(
        relation != "below" for n, _, relation in compared if n not in unrecorded
    ):
        problems.append(f"#{chosen.issue}: a decided side is not below Göbel's construction")
    return problems


def check(*, replay: bool, workers: int = 1, issues: Sequence[int] = ()) -> list[str]:
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


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n", 1)[0])
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("filtered")
    run.add_argument("--issue", type=int, nargs="+", default=sorted(RELEASES))
    run.add_argument("--workers", type=int, default=2)
    history = commands.add_parser("first-commits")
    history.add_argument("--issue", type=int, required=True)
    history.add_argument("--clone", type=Path, required=True)
    sample = commands.add_parser("exhaustive")
    sample.add_argument("--issue", type=int, required=True)
    sample.add_argument("--n", type=int, nargs="+", required=True)
    sample.add_argument("--workers", type=int, default=2)
    commands.add_parser("goebel")
    commands.add_parser("claims-record")
    scan = commands.add_parser("earlier")
    scan.add_argument("--issue", type=int, required=True)
    scan.add_argument("--couzo", type=Path, required=True, help="franciscouzo/square-packing")
    scan.add_argument("--evand", type=Path, required=True, help="evand/square-packing")
    scan.add_argument("--source", type=Path, help="the release's own repository")
    transcribe = commands.add_parser("ledger-sources")
    transcribe.add_argument("--issue", type=int, required=True)
    transcribe.add_argument("--read-at-main", required=True)
    transcribe.add_argument("--read-on", required=True)
    commands.add_parser("coverage-plan")
    audit = commands.add_parser("check")
    audit.add_argument("--issue", type=int, nargs="+", default=[])
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
        "coverage-plan": lambda: {
            "rows": planned_rows(),
            "supersessions": planned_supersessions(),
        },
    }
    if args.command == "check":
        problems = check(replay=args.replay, workers=args.workers, issues=args.issue)
        for problem in problems:
            print(problem)
        chosen = [release(issue) for issue in args.issue] or list(RELEASES.values())
        decided = sum(item.decided for item in chosen)
        named = ", ".join(f"#{item.issue}" for item in chosen)
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
