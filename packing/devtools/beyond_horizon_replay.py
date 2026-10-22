"""Decide the beyond-horizon rows of a report exactly, from its retained packet.

A report beyond the ``n <= 324`` corpus is recorded as dated beyond-horizon rows of its
source, at assurance ``reported``, once its certificates are retained and replayed here.
Issues #678 and #715 each had a module of their own (`devtools.couzo_678_replay`,
`devtools.couzo_715_replay`); this one takes the same filtered decision and declares each
report it decides as a `Release`, so a further report of the same kind is a declaration and
not a module. `RELEASES` holds four, each at or below ``LIMIT = 1024``:

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

Each certificate is ``n S``, then ``n`` rows ``x y t`` (centre and ``t = tan(theta/2)``),
and lines that begin with ``#`` are comments; the issue prints ``S`` rounded up at 12
places, and the header is authoritative.

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

**The rows.** ``coverage-plan`` reads each row's disposition from the report-order ledger
of ``campaign/issue-intake/upper-bounds-backlog-20261022`` (`planned_rows`): recorded at
its count, it is superseded by the next report the walk records there, or it is the
count's current row. Where a release's row is the first report the walk records at a count,
the count's start names that release as its successor (`planned_supersessions`), whether
the release's row is current or a later report's row supersedes it in turn: the four
reports came before #678, #686 and #715, so a start those later reports had superseded on
``main`` now names the backlog report that beat it first. ``check`` holds
``frontier/source-coverage.yaml`` to that plan, and holds every count the ledger walks
beyond the corpus to one chain in report order (`chain_problems`): the start, then each
recorded report's row, each superseded by the next, the last current or superseded by a
report the walk does not reach.

From ``packing/``, with the project interpreter::

    python -m devtools.beyond_horizon_replay filtered [--issue N ...] [--workers 2]
    python -m devtools.beyond_horizon_replay first-commits --issue N --clone CLONE
    python -m devtools.beyond_horizon_replay exhaustive --issue N --n 922 [--workers 2]
    python -m devtools.beyond_horizon_replay goebel
    python -m devtools.beyond_horizon_replay claims-record
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
#: The report-order walk at every count these reports claim, starts frozen at the 18
#: October ledger's ``main``; `planned_rows` reads each row's disposition from it.
LEDGER = ROOT / "campaign/issue-intake/upper-bounds-backlog-20261022/ledger.json"
COVERAGE = ROOT / "frontier/source-coverage.yaml"
#: The source whose dated rows record each later report the ledger walks beyond the corpus.
LATER_SOURCES = {
    "#678": "couzo-issue678-2026-10-18",
    "#686": "muglich-issue686-2026-10-19",
    "#715": "couzo-issue715-2026-10-21",
}
_START_ROW = re.compile(r"beyond-horizon row (\S+)")
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
    every certificate a row reads, committed at ``committed``: what ``first-commits``
    measures and the claims record states. ``rows`` counts the issue's table and ``decided``
    the rows beyond the corpus at or below ``LIMIT``; ``sampled`` names the counts the
    all-pairs sample decides, which the packet README and the atom state.
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

    @property
    def directory(self) -> Path:
        return WEB / self.packet

    @property
    def issue_url(self) -> str:
        return f"https://github.com/jlevy/squares/issues/{self.issue}"


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
    """The packing a row claims: its retained certificate, less the squares it deletes."""
    raw = read_retained_bytes(archive(chosen) / row.path)
    parsed = legacy.parse(raw.decode("utf-8"), expected_n=row.certificate_n)
    if row.deleted:
        parsed = legacy.Certificate(row.n, parsed.side, parsed.poses[: row.n])
    return parsed


def ceiling(side: Fraction, places: int = PLACES) -> str:
    """``side`` rounded up at ``places`` decimal places."""
    return legacy.ceiling_decimal(side, places)


def git_blob(raw: bytes) -> str:
    """The Git blob id of a file's bytes."""
    return hashlib.sha1(b"blob %d\0" % len(raw) + raw, usedforsecurity=False).hexdigest()


def seed_credit(chosen: Release, row: Claim) -> dict[str, Any] | None:
    """The per-count metadata's seed credit, where the packet retains it, and whether the
    metadata describes the row's certificate (a #675 row reads ``best/``, the metadata the
    root certificate of its count)."""
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
    upward = base.rounds_up_to(cert.side, row.printed)
    record: dict[str, Any] = {
        "n": row.n,
        "certificate": row.path,
        "certificate_sha256": manifest(chosen)[row.path],
        "deleted_squares": row.deleted,
        "printed": row.printed,
        "issue_prior": row.prior,
        "exact_side": legacy.literal(cert.side),
        "side_ceiling_16": ceiling(cert.side, 16),
        "printed_is_upward_rounding": upward,
        "verified": result["passed"] and upward,
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
    rows read is found by its Git blob at the retained commit, under any path.
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
        blob = git_blob(read_retained_bytes(archive(chosen) / row.path))
        commit = first[blob]
        rows.append(
            {
                "n": row.n,
                "certificate": row.path,
                "blob": blob,
                "first_commit": commit,
                "committed": _utc(dates[commit]),
            }
        )
    receipt = {
        "format": FIRST_COMMITS_FORMAT,
        "source": chosen.source_url,
        "retained_commit": chosen.retained,
        "history_commits": len(chain),
        "rows": rows,
    }
    _write(chosen.directory / FIRST_COMMITS, receipt)
    return receipt


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
        rows = [
            (row.n, certificate(chosen, row).side, row.path) for row in decided_claims(chosen)
        ]
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

    Each keeps the issue's print as ``offered_side``, the value a dated beyond-horizon row
    holds byte for byte, its certificate's exact header side, and when the certificate was
    first committed.
    """
    custody(chosen)
    results = []
    for row in decided_claims(chosen):
        side = certificate(chosen, row).side
        _require(
            base.rounds_up_to(side, row.printed),
            f"#{chosen.issue} n={row.n}: the print does not round up",
        )
        results.append(
            {
                "n": row.n,
                "offered_side": row.printed,
                "exact_side": legacy.literal(side),
                "ceiling": ceiling(side, reports.DISPLAY_PLACES),
                "certificate": row.path,
                "deleted": row.deleted,
                "first_committed": chosen.committed,
            }
        )
    return {
        "format": reports.BEYOND_FORMAT,
        "issue": chosen.issue_url,
        "source": chosen.source_url,
        "revision": chosen.retained,
        "issue_pin": chosen.pin,
        "horizon": reports.HORIZON,
        "limit": LIMIT,
        "results": results,
    }


def claims_record() -> dict[int, int]:
    """Write each packet's beyond-horizon record and return its row counts."""
    written: dict[int, int] = {}
    for chosen in RELEASES.values():
        record = beyond_horizon_rows(chosen)
        _write(chosen.directory / RECORD, record)
        written[chosen.issue] = len(record["results"])
    return written


# --------------------------------------------------------------------------- coverage plan


def _source_of(report: str) -> str:
    """The coverage source whose rows record a report the ledger walks."""
    ours = {f"#{issue}": item.packet for issue, item in RELEASES.items()}
    source = ours.get(report) or LATER_SOURCES.get(report)
    _require(source is not None, f"{report}: the ledger walks a report no source records")
    assert source is not None
    return source


def planned_rows() -> list[dict[str, Any]]:
    """Each decided row as a dated beyond-horizon row, in report order at its count.

    The backlog ledger walks every report at each count from the start frozen at the 18
    October ledger's ``main``; a row of these releases is recorded, and is superseded by
    the next report the walk records at its count, or is the count's current row. A row
    the walk does not record, or a count the ledger does not walk, is refused: it is a
    records decision this plan does not make.
    """
    walked = {count["n"]: count for count in _read(LEDGER)["counts"]}
    rows: list[dict[str, Any]] = []
    for chosen in RELEASES.values():
        printed = {
            row["n"]: row["offered_side"] for row in _read(chosen.directory / RECORD)["results"]
        }
        for row in decided_claims(chosen):
            _require(row.n in walked, f"#{chosen.issue} n={row.n}: the ledger does not walk it")
            steps = walked[row.n]["steps"]
            (mine,) = [
                i for i, step in enumerate(steps) if step["report"] == f"#{chosen.issue}"
            ]
            _require(
                steps[mine]["verdict"] == "recorded",
                f"#{chosen.issue} n={row.n}: the ledger does not record it",
            )
            later = [step for step in steps[mine + 1 :] if step["verdict"] == "recorded"]
            planned: dict[str, Any] = {
                "n": row.n,
                "source_id": chosen.packet,
                "claim": "upper-bound",
                "value": printed[row.n],
                "assurance": "reported",
                "disposition": "superseded" if later else "tracked-outside-case-corpus",
            }
            if later:
                planned["superseded_by"] = _source_of(later[0]["report"])
            planned["bead"] = chosen.bead
            rows.append(planned)
    return rows


def _start_source(count: Mapping[str, Any]) -> str | None:
    """The source of a walked count's start, where the start is a beyond-horizon row (a
    count the grid or a register entry held has none)."""
    (start,) = count["start"]
    match = _START_ROW.fullmatch(start["label"])
    return None if match is None else match[1]


def planned_supersessions() -> list[tuple[int, str, str]]:
    """Where a release's row is the first report the walk records at its count, the start
    it supersedes: ``(n, the start's source, the release's source)``, in count order.

    The start is the count's beyond-horizon row frozen in the ledger's starts. The release's
    row may itself be superseded by a later report; the start still names the release, the
    first report to beat it in report order, so each count is one chain.
    """
    ours = {f"#{issue}": item.packet for issue, item in RELEASES.items()}
    flips: list[tuple[int, str, str]] = []
    for count in _read(LEDGER)["counts"]:
        recorded = [step["report"] for step in count["steps"] if step["verdict"] == "recorded"]
        start = _start_source(count)
        if start is not None and recorded and recorded[0] in ours:
            flips.append((count["n"], start, ours[recorded[0]]))
    return flips


def chain_problems(coverage: Mapping[str, Any]) -> list[str]:
    """Where a count the ledger walks beyond the corpus is not one chain in report order.

    The chain is the count's start, where it is a beyond-horizon row, then the row of each
    report the walk records, in report order. Each must be in the register and superseded by
    the next; the last is current, or superseded by a report the walk does not reach.
    """
    rows = {(row["n"], row["source_id"]): row for row in coverage["beyond_horizon_claims"]}
    problems: list[str] = []
    for count in _read(LEDGER)["counts"]:
        n = count["n"]
        if n <= reports.HORIZON:
            continue
        start = _start_source(count)
        chain = ([start] if start is not None else []) + [
            _source_of(step["report"])
            for step in count["steps"]
            if step["verdict"] == "recorded"
        ]
        for earlier, later in zip(chain, [*chain[1:], None], strict=True):
            held = rows.get((n, earlier))
            if held is None:
                problems.append(f"n={n}: the register has no row from {earlier}")
                continue
            successor = held.get("superseded_by")
            if later is not None and (held.get("disposition"), successor) != (
                "superseded",
                later,
            ):
                problems.append(f"n={n} from {earlier}: names {successor}, not {later}")
            elif later is None and successor in chain:
                problems.append(
                    f"n={n} from {earlier}: names {successor}, earlier in the chain"
                )
    return problems


def coverage_problems() -> list[str]:
    """Where the coverage register differs from the plan: each planned row, as written,
    each start a release's row beat first naming the release's source as its successor, and
    each walked count one chain in report order."""
    coverage = safe_load(COVERAGE.read_text(encoding="utf-8"))
    rows = {(row["n"], row["source_id"]): row for row in coverage["beyond_horizon_claims"]}
    problems = [
        f"n={row['n']} from {row['source_id']}: the register's row is not the plan's"
        for row in planned_rows()
        if rows.get((row["n"], row["source_id"])) != row
    ]
    for n, earlier, successor in planned_supersessions():
        held = rows.get((n, earlier)) or {}
        if (held.get("disposition"), held.get("superseded_by")) != ("superseded", successor):
            problems.append(f"n={n} from {earlier}: not superseded by {successor}")
    return problems + chain_problems(coverage)


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
    for row, kept in zip(rows, stored, strict=True):
        problems.extend(row_problems(chosen, row, kept))
        if Fraction(kept["exact_side"]) != certificate(chosen, row).side:
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
    """The first commits', the all-pairs sample's and the Göbel receipt's outcomes."""
    problems: list[str] = []
    commits = _read(chosen.directory / FIRST_COMMITS)
    expected = [
        (row.n, row.path, git_blob(read_retained_bytes(archive(chosen) / row.path)))
        for row in [*rows, *held_claims(chosen)]
    ]
    if [(item["n"], item["certificate"], item["blob"]) for item in commits["rows"]] != expected:
        problems.append(
            f"#{chosen.issue}: the first commits are not the retained certificates'"
        )
    problems.extend(
        f"#{chosen.issue} n={item['n']}: first committed at {item['first_commit'][:8]}, "
        f"not {chosen.first_commit[:8]} as the record states"
        for item in commits["rows"]
        if (item["first_commit"], item["committed"]) != (chosen.first_commit, chosen.committed)
    )
    problems.extend(sample_problems(chosen, rows, _read(chosen.directory / EXHAUSTIVE)["rows"]))
    comparison = _read(chosen.directory / GOEBEL)["comparison"]
    compared = [
        (item["n"], Fraction(item["side"]), item["relation"]) for item in comparison["detail"]
    ]
    if compared != [(row.n, certificate(chosen, row).side, "below") for row in rows]:
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
