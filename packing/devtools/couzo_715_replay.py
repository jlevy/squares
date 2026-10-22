"""Decide issue #715's upper bounds at or below n = 1024 exactly, from the retained packet.

Francisco Couzo's issue #715 reports 1285 upper bounds for n = 328 to 9913 at
franciscouzo/square-packing ``6b7391de``, each the exact side of the source's certificate or
construction rounded up at 12 places. At each of the 173 counts at or below 1024 the pin
holds an explicit certificate, ``certificates/nN.cert``: ``n S``, then ``n`` rows ``x y t``
(centre and ``t = tan(theta/2)``), whose header side is the claim's exact side. The source's
index, ``certified_bounds.json``, calls 59 of those counts L-border constructions and 11
deletions of another count's certificate; at each, the explicit file writes the packing
out in full, as the parent's poses followed by the border's axis-aligned unit squares, or
as the parent's first ``n`` poses.

**Which counts are new.** The source's ``master`` stood at ``PUBLIC_HEAD`` (``7b6c87e``,
issue #678's pin) from 2026-10-18T23:23:42Z, when GitHub recorded its push, until
2026-10-21T22:56:37Z, when the three commits after it (``d09edd7``, ``5a299b4`` and the pin)
were pushed together, two hours after the issue was filed at 20:55:57Z. So every certificate
reachable from ``PUBLIC_HEAD`` was public before the issue, and every other one reached this
repository first through the issue. ``publications`` reads the source's history from a clone
(blobless is enough) and, at each claimed count, holds the pin's certificate to every
certificate of that count reachable from ``PUBLIC_HEAD``, and to the bound the public index
at ``PUBLIC_HEAD`` states there, exactly. Each count falls in one set:

- **recorded**: the pin's side is below every earlier public side by more than the issue's
  print resolves, so the print alone decides it (109 counts). These are the issue's own
  reports, and ``claims-record`` writes them as the packet's beyond-horizon claims.
- **held**: the pin's side is below the least earlier public side, but both round up to the
  same 12-place print (30 counts, by 2.4e-23 to 3.2e-23): the issue re-certifies an earlier
  publication of its own packing a little tighter. Whether such a row is new is not decided
  here; it waits on the owner, and nothing is recorded for it.
- **restated**: the pin's side equals an earlier public side (34 counts): an earlier report,
  which the issue restates and which its own import records.

**The replay.** The packet ``resources/web/couzo-issue715-2026-10-21`` retains the 139
certificates of the first two sets; this module reads them from it once
``acquire_source --check`` holds the packet, and decides each with the filtered two-route
decision and the six controls of ``devtools.couzo_678_replay``, reused unchanged: route
``sqpack`` through ``sqpack.witness`` and ``sqpack.verify``'s predicates, route
``independent`` through ``devtools.check_rational_witness_independent``'s, over every wall
and every pair whose centres are closer than ``sqrt 2`` by exact comparison. That module's
docstring states the filter's lemma and the controls. Each printed side must be its header
side rounded up at 12 places. With ``--pinned CHECKOUT``, a checkout at the pin, each row's
index entry, manifest credit and, where the index names a parent, the parent's relation to
the explicit file are read from the source's files, each held to the digest the packet pins
or the index states, and recorded beside the decision.

``exhaustive`` runs the maintained all-pairs kernel of ``devtools.evand_arrangement_reports``
(every pair, no filter) on chosen counts beside the filtered decision, and ``goebel`` holds
every decided side to Göbel's classical constructions with the 15 October packet's retained
program. ``check`` reads the receipts and the claims record back against the packet and the
issue, and ``check --replay`` decides every row and control again.

From ``packing/``, with the project interpreter::

    python -m devtools.couzo_715_replay publications --history CLONE
    python -m devtools.couzo_715_replay filtered [--pinned CHECKOUT] [--workers 2]
    python -m devtools.couzo_715_replay exhaustive --n 343 996 [--workers 2]
    python -m devtools.couzo_715_replay goebel
    python -m devtools.couzo_715_replay claims-record
    python -m devtools.couzo_715_replay check [--replay [--workers 2]]

A finite packing certifies an upper bound and nothing more: novelty, rigidity and optimality
are not decided here, and neither are the source's credit and lineage statements.
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
from collections.abc import Set as AbstractSet
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
from devtools.retained_data import read_retained_bytes
from sqpack.retained_json import dumps as retained_dumps

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PACKET = ROOT / "resources/web/couzo-issue715-2026-10-21"
SOURCE = PACKET / "source"
MANIFEST = PACKET / "acquisition/upstream-subtree.sha256"
ISSUE = PACKET / "acquisition/issue.json"
BEYOND = PACKET / "acquisition/beyond-horizon-claims.json"
RECEIPTS = PACKET / "receipts"
FILTERED = RECEIPTS / "filtered-exact-replay.json"
PUBLICATIONS = RECEIPTS / "earlier-publications.json"
EXHAUSTIVE = RECEIPTS / "exhaustive-sample.json"
GOEBEL = RECEIPTS / "goebel-comparison.json"
ISSUE_URL = "https://github.com/jlevy/squares/issues/715"
SOURCE_URL = "https://github.com/franciscouzo/square-packing"
PIN = "6b7391de820fd01f3ff6984e4a081e8c86845588"
#: The source's public head while the issue was written (see the module docstring).
PUBLIC_HEAD = "7b6c87e129cf80b5ff9847b90b47fd30b4563c54"
#: The issue's rows, and those at or below this count, which this module decides.
ROWS = 1285
LIMIT = 1024
DECIDED = 173
RECORDED, HELD, RESTATED = "recorded", "held", "restated"
#: How many counts each set holds, as `publications` found them.
SET_SIZES = {RECORDED: 109, HELD: 30, RESTATED: 34}
PLACES = 12
FILTERED_FORMAT = "couzo-715-filtered-exact-replay-v1"
PUBLICATIONS_FORMAT = "couzo-715-earlier-publications-v1"
EXHAUSTIVE_FORMAT = "couzo-715-exhaustive-sample-v1"
GOEBEL_FORMAT = "couzo-715-goebel-comparison-v1"
INDEX = "certified_bounds.json"
SOURCE_MANIFEST = "certificates/best/manifest.json"
_ROW = re.compile(r"\|(\d+)\|([\d.]+)\|([\d.]+)\|")


class ReplayError(ValueError):
    """Refuse a row, a certificate or a receipt that does not hold."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ReplayError(message)


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


def _goebel_program() -> Any:
    """The 15 October packet's exact Göbel comparison, loaded from its retained path."""
    spec = importlib.util.spec_from_file_location("goebel_beyond_horizon", base.GOEBEL_PROGRAM)
    if spec is None or spec.loader is None:
        raise ReplayError("the Göbel program is missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------- the claims


@dataclass(frozen=True, slots=True)
class Claim:
    """One row of the issue's table: the count, the author's prior column and the print."""

    n: int
    prior: str
    printed: str

    @property
    def path(self) -> str:
        """The upstream path of the count's explicit certificate."""
        return f"certificates/n{self.n}.cert"


def claims() -> list[Claim]:
    """The issue's 1285 rows, read from its retained body, refused unless all are there."""
    body = json.loads(ISSUE.read_text(encoding="utf-8"))["body"]
    rows = [
        Claim(int(match[1]), match[2], match[3])
        for line in body.splitlines()
        if (match := _ROW.fullmatch(line.strip())) is not None
    ]
    _require(len(rows) == ROWS, f"{len(rows)} rows, not {ROWS}")
    _require([row.n for row in rows] == sorted({row.n for row in rows}), "rows out of order")
    return rows


def decided_claims() -> list[Claim]:
    """The rows at or below ``LIMIT``, which this module decides."""
    rows = [row for row in claims() if row.n <= LIMIT]
    _require(len(rows) == DECIDED, f"{len(rows)} rows at or below {LIMIT}, not {DECIDED}")
    return rows


def manifest() -> dict[str, str]:
    """The packet's upstream digests, by upstream path."""
    return acquire_source.read_manifest(MANIFEST)


def custody() -> None:
    """Refuse to read the packet unless ``acquire_source --check`` holds for it."""
    problems = acquire_source.check(PACKET, REPO)
    _require(not problems, "packet custody: " + "; ".join(problems))


def retained(n: int) -> bool:
    """Whether the packet retains the count's certificate, not only its digest."""
    return (SOURCE / f"certificates/n{n}.cert").is_file()


def certificate(row: Claim) -> legacy.Certificate:
    """A row's retained explicit certificate, its count checked against the row's."""
    _require(retained(row.n), f"n={row.n}: the packet does not retain its certificate")
    return legacy.parse(
        read_retained_bytes(SOURCE / row.path).decode("utf-8"), expected_n=row.n
    )


def ceiling(side: Fraction, places: int = PLACES) -> str:
    """``side`` rounded up at ``places`` decimal places."""
    return legacy.ceiling_decimal(side, places)


# --------------------------------------------------------------------------- publications


def _git(clone: Path, *args: str, text: bool = True) -> Any:
    return subprocess.run(
        ["git", "-C", str(clone), *args], capture_output=True, text=text, check=True
    ).stdout


def _header(raw: bytes) -> tuple[int, Fraction]:
    rows = [
        line.split()
        for line in raw.decode("utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    _require(rows and len(rows[0]) == 2, "a certificate without an `n S` header")
    return int(rows[0][0]), Fraction(rows[0][1])


def _trees(clone: Path, commits: Sequence[str]) -> dict[str, dict[str, str]]:
    """Each commit's certificate files, path to blob, from the tree alone."""
    trees: dict[str, dict[str, str]] = {}
    for commit in commits:
        listing = _git(clone, "ls-tree", "-r", commit)
        trees[commit] = {
            path: meta.split()[2]
            for meta, _, path in (line.partition("\t") for line in listing.splitlines())
            if path.endswith(".cert")
        }
    return trees


def _headers(clone: Path, blobs: Sequence[str]) -> dict[str, tuple[int, Fraction]]:
    """Each blob's ``n S`` header, read in one ``git cat-file --batch``.

    A blob the clone lacks is fetched from its promisor remote first, by ``--batch-check``,
    so a blobless clone serves; ``--batch`` then reads only local objects.
    """
    listed = "".join(f"{blob}\n" for blob in blobs).encode()
    subprocess.run(
        ["git", "-C", str(clone), "cat-file", "--batch-check"],
        input=listed,
        capture_output=True,
        check=True,
    )
    shown = subprocess.run(
        ["git", "-C", str(clone), "cat-file", "--batch"],
        input=listed,
        capture_output=True,
        check=True,
    ).stdout
    headers: dict[str, tuple[int, Fraction]] = {}
    offset = 0
    for blob in blobs:
        end = shown.index(b"\n", offset)
        name, kind, size = shown[offset:end].decode().split()
        _require(name == blob and kind == "blob", f"{blob}: not a blob")
        start = end + 1
        headers[blob] = _header(shown[start : start + int(size)])
        offset = start + int(size) + 1
    return headers


def earlier_publications(clone: Path) -> dict[str, Any]:
    """Each claimed count's certificate at the pin against every earlier public side.

    ``clone`` is a clone of the source holding its history to the pin. Every certificate
    file (``*.cert``, under any directory and name) of every commit reachable from
    ``PUBLIC_HEAD`` is read, and its header's count and side kept; the public index at
    ``PUBLIC_HEAD`` adds the bound it states where it names a certificate, which at a
    deletion is another count's. Each side is compared exactly with the pin's certificate.
    """
    _require(_git(clone, "rev-parse", "HEAD").strip() == PIN, "the clone is not at the pin")
    chain = _git(clone, "rev-list", "--reverse", PIN).split()
    public = set(_git(clone, "rev-list", PUBLIC_HEAD).split())
    dates = dict(
        line.split(" ", 1) for line in _git(clone, "log", "--format=%H %cI", PIN).splitlines()
    )
    trees = _trees(clone, chain)
    first_holding: dict[str, tuple[str, str]] = {}
    for commit in chain:
        for path, blob in trees[commit].items():
            first_holding.setdefault(blob, (commit, path))
    published = sorted({blob for c in chain if c in public for blob in trees[c].values()})
    rows_at_pin = [trees[PIN][row.path] for row in decided_claims()]
    headers = _headers(clone, sorted(set(published) | set(rows_at_pin)))
    by_count: dict[int, list[str]] = {}
    for blob in published:
        by_count.setdefault(headers[blob][0], []).append(blob)
    index = json.loads(_git(clone, "show", f"{PUBLIC_HEAD}:{INDEX}"))["entries"]
    rows = []
    for row, blob in zip(decided_claims(), rows_at_pin, strict=True):
        n, side = headers[blob]
        _require(n == row.n, f"n={row.n}: the pin's certificate counts {n}")
        candidates: list[dict[str, Any]] = [
            {
                "kind": "certificate",
                "path": first_holding[other][1],
                "blob": other,
                "commit": first_holding[other][0],
                "side": headers[other][1],
            }
            for other in by_count.get(row.n, [])
        ]
        entry = index.get(str(row.n))
        if entry is not None and entry["kind"] == "certificate":
            parent = trees[PUBLIC_HEAD][entry["certificate"]]
            candidates.append(
                {
                    "kind": "index",
                    "path": entry["certificate"],
                    "blob": parent,
                    "commit": first_holding[parent][0],
                    "side": Fraction(entry["bound"]),
                    "deleted_squares": entry["deleted_squares"],
                }
            )
        _require(candidates, f"n={row.n}: no earlier public side")
        least = min(candidates, key=lambda item: (item["side"], dates[item["commit"]]))
        rows.append(
            publication_row(
                row,
                blob,
                side,
                first=first_holding[blob][0],
                least=least,
                dates=dates,
                public=public,
            )
        )
    return {
        "format": PUBLICATIONS_FORMAT,
        "issue": ISSUE_URL,
        "source": SOURCE_URL,
        "revision": PIN,
        "public_head": PUBLIC_HEAD,
        "public_until": "2026-10-21T22:56:37Z",
        "issue_filed": "2026-10-21T20:55:57Z",
        "rows": rows,
        "sets": {name: [r["n"] for r in rows if r["set"] == name] for name in SET_SIZES},
    }


def classify(side: Fraction, printed: str, earlier: Fraction) -> str:
    """The set a count falls in, from its exact side, its print and the least earlier side."""
    _require(base.rounds_up_to(side, printed), f"{printed} is not {side} rounded up")
    _require(side <= earlier, f"{printed}: above an earlier public side")
    if side == earlier:
        return RESTATED
    return HELD if ceiling(earlier) == printed else RECORDED


def publication_row(
    row: Claim,
    blob: str,
    side: Fraction,
    *,
    first: str,
    least: Mapping[str, Any],
    dates: Mapping[str, str],
    public: AbstractSet[str],
) -> dict[str, Any]:
    """One count's record: its certificate, when first committed and whether that commit was
    public before the issue (reachable from ``PUBLIC_HEAD``), and the least earlier side."""
    earlier = least["side"]
    _require(least["commit"] in public, f"n={row.n}: an earlier side not public before")
    kept = {
        "kind": least["kind"],
        "path": least["path"],
        "blob": least["blob"],
        "commit": least["commit"],
        "committed": dates[least["commit"]],
        "exact_side": legacy.literal(earlier),
        "ceiling_12": ceiling(earlier),
    }
    if "deleted_squares" in least:
        kept["deleted_squares"] = least["deleted_squares"]
    return {
        "n": row.n,
        "printed": row.printed,
        "blob": blob,
        "first_commit": first,
        "first_committed": dates[first],
        "first_commit_public": first in public,
        "exact_side": legacy.literal(side),
        "earlier": kept,
        "below_earlier_by": legacy.literal(earlier - side),
        "set": classify(side, row.printed, earlier),
    }


def write_publications(clone: Path) -> dict[str, list[int]]:
    """Write the publications receipt and return its sets."""
    record = earlier_publications(clone)
    _write(PUBLICATIONS, record)
    return record["sets"]


def publications() -> dict[str, Any]:
    """The committed publications receipt."""
    return json.loads(PUBLICATIONS.read_text(encoding="utf-8"))


def counts_in(name: str) -> list[int]:
    """The counts of one set, as the committed publications receipt states them."""
    return [row["n"] for row in publications()["rows"] if row["set"] == name]


# --------------------------------------------------------------------------- the replay


def _pinned_bytes(checkout: Path, path: str, digest: str) -> bytes:
    raw = (checkout / path).read_bytes()
    _require(hashlib.sha256(raw).hexdigest() == digest, f"{path}: differs from its digest")
    return raw


def source_facts(checkout: Path) -> dict[str, Any]:
    """The index and the manifest, read from a pinned checkout and held to their digests."""
    digests = manifest()
    index = json.loads(_pinned_bytes(checkout, INDEX, digests[INDEX]))["entries"]
    witnesses = json.loads(_pinned_bytes(checkout, SOURCE_MANIFEST, digests[SOURCE_MANIFEST]))[
        "witnesses"
    ]
    return {"index": index, "witnesses": witnesses, "checkout": str(checkout)}


def index_relation(
    row: Claim, cert: legacy.Certificate, facts: Mapping[str, Any]
) -> dict[str, Any]:
    """The index's entry at the count, and how the explicit file relates to its parent.

    For a construction or a deletion the index names a parent certificate and its digest;
    the parent is read from the checkout and held to that digest. A deletion's file must be
    the parent's first ``n`` poses at the parent's side; an L-border's, the parent's poses
    followed by axis-aligned squares (``t = 0``), at the parent's side plus its layers.
    """
    entry = facts["index"][str(row.n)]
    recipe = entry.get("construction") or {}
    parent_n = recipe.get("source_n", entry["source_n"])
    provenance = (facts["witnesses"].get(str(parent_n)) or {}).get("provenance") or {}
    relation: dict[str, Any] = {
        "kind": entry["kind"],
        "bound_equals_header": Fraction(entry["bound"]) == cert.side,
        "source_n": parent_n,
        "deleted_squares": entry["deleted_squares"],
        "credit": entry.get("credit", ""),
        "prior_source_credit": provenance.get("prior_source_credit", ""),
    }
    if entry["kind"] == "certificate" and not entry["deleted_squares"]:
        return relation
    parent_path = entry["certificate"]
    raw = _pinned_bytes(Path(facts["checkout"]), parent_path, entry["certificate_sha256"])
    parent = legacy.parse(raw.decode("utf-8"))
    layers = recipe.get("layers", 0)
    tiles = recipe.get("tiles_per_side", 1)
    shared = min(len(parent.poses), cert.n)
    relation.update(
        {
            "parent": parent_path,
            "parent_n": parent.n,
            "layers": layers,
            "tiles_per_side": tiles,
            "parent_poses_lead": cert.poses[:shared] == parent.poses[:shared],
            "added_squares_axis_aligned": all(pose.t == 0 for pose in cert.poses[parent.n :]),
            "side_is_parent_side_plus_layers": cert.side == tiles * parent.side + layers,
        }
    )
    return relation


def decide_row(row: Claim) -> dict[str, Any]:
    """One row: custody, the side against the print, both routes, and the six controls."""
    cert = certificate(row)
    started = time.monotonic()
    result = base.decide(base.geometry(cert))
    upward = base.rounds_up_to(cert.side, row.printed)
    record: dict[str, Any] = {
        "n": row.n,
        "certificate": row.path,
        "certificate_sha256": manifest()[row.path],
        "printed": row.printed,
        "issue_prior": row.prior,
        "exact_side": legacy.literal(cert.side),
        "side_ceiling_16": ceiling(cert.side, 16),
        "printed_is_upward_rounding": upward,
        "verified": result["passed"] and upward,
        "decision": result,
        "controls": base.decide_controls(cert),
    }
    record["wall_seconds"] = round(time.monotonic() - started, 3)
    return record


def replayed_claims() -> list[Claim]:
    """The rows whose certificates the packet retains: the recorded and the held."""
    keep = set(counts_in(RECORDED)) | set(counts_in(HELD))
    return [row for row in decided_claims() if row.n in keep]


def filtered(pinned: Path | None, workers: int) -> dict[str, Any]:
    """Decide every retained certificate and its controls, and write the receipt."""
    custody()
    rows = replayed_claims()
    facts = None if pinned is None else source_facts(pinned)
    started = datetime.now(UTC)
    wall = time.monotonic()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(decide_row, rows))
    if facts is not None:
        for row, result in zip(rows, results, strict=True):
            result["source_index"] = index_relation(row, certificate(row), facts)
    receipt: dict[str, Any] = {
        "format": FILTERED_FORMAT,
        "issue": ISSUE_URL,
        "source_commit": PIN,
        "packet": PACKET.relative_to(REPO).as_posix(),
        "program": "packing/devtools/couzo_715_replay.py",
        "decision": "packing/devtools/couzo_678_replay.py",
        "filter_lemma": base.FILTER_LEMMA,
        "controls": list(base.CONTROLS),
        "environment": _environment(),
        "started_utc": started.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "wall_seconds": round(time.monotonic() - wall, 1),
        "workers": workers,
        "rows": results,
        "summary": base.summary(results),
    }
    _write(FILTERED, receipt)
    return receipt


# --------------------------------------------------------------------------- cross-checks


def exhaustive_row(row: Claim) -> dict[str, Any]:
    """The maintained all-pairs kernel on one row, beside the filtered decision of it."""
    cert = certificate(row)
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


def exhaustive(counts: Sequence[int], workers: int) -> dict[str, Any]:
    """The all-pairs kernel on chosen rows, each against the filtered decision."""
    custody()
    rows = {row.n: row for row in replayed_claims()}
    for n in counts:
        _require(n in rows, f"n={n}: not a replayed row")
    started = datetime.now(UTC)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(exhaustive_row, [rows[n] for n in counts]))
    pairs = sum(row["pairs_tested"] for row in results)
    seconds = sum(sum(row["cpu_seconds"].values()) for row in results)
    receipt = {
        "format": EXHAUSTIVE_FORMAT,
        "kernel": "devtools.evand_arrangement_reports.run_case, positive job, every pair",
        "environment": _environment(),
        "started_utc": started.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "workers": workers,
        "rows": results,
        "sample_pairs": pairs,
        "sample_cpu_seconds": round(seconds, 1),
    }
    _write(EXHAUSTIVE, receipt)
    return receipt


def goebel() -> dict[str, Any]:
    """Every replayed side against Göbel's classical constructions, exactly.

    The families, their deletion to smaller counts and the sign test are those of the 15
    October packet's retained ``goebel_beyond_horizon.py``, read from its path unchanged;
    its ``LIMIT`` of 1100 covers every count decided here.
    """
    custody()
    program = _goebel_program()
    _require(program.LIMIT >= LIMIT, "the Göbel program stops below the decided counts")
    forms = program.families(program.LIMIT)
    rows = [(row.n, certificate(row).side, row.path) for row in replayed_claims()]
    result = program.compare("issue #715 at 6b7391de", rows, forms)
    receipt = {
        "format": GOEBEL_FORMAT,
        "program": base.GOEBEL_PROGRAM.relative_to(REPO).as_posix(),
        "families": "Göbel squares, Göbel strips and corner-touching strips, with deletion",
        "comparison": result,
    }
    _write(GOEBEL, receipt)
    return {"rows": result["rows"], "tally": result["tally"], "above": result["above"]}


# --------------------------------------------------------------------------- claims record


def beyond_horizon_claims() -> dict[str, Any]:
    """The recorded rows as the coverage register reads them, rebuilt.

    Each keeps the issue's print as ``offered_side``, the value a dated beyond-horizon row
    holds byte for byte, its certificate's exact header side, and when the certificate was
    first committed; every one reached this repository first through the issue.
    """
    custody()
    first = {row["n"]: row["first_committed"] for row in publications()["rows"]}
    keep = set(counts_in(RECORDED))
    results = []
    for row in decided_claims():
        if row.n not in keep:
            continue
        side = certificate(row).side
        _require(
            base.rounds_up_to(side, row.printed), f"n={row.n}: the print does not round up"
        )
        results.append(
            {
                "n": row.n,
                "offered_side": row.printed,
                "exact_side": legacy.literal(side),
                "ceiling": ceiling(side, reports.DISPLAY_PLACES),
                "certificate": row.path,
                "first_committed": _utc(first[row.n]),
            }
        )
    return {
        "format": reports.BEYOND_FORMAT,
        "issue": ISSUE_URL,
        "source": SOURCE_URL,
        "revision": PIN,
        "horizon": reports.HORIZON,
        "results": results,
    }


def _utc(stamp: str) -> str:
    return datetime.fromisoformat(stamp).astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def claims_record() -> int:
    """Write the beyond-horizon claims record and return its row count."""
    record = beyond_horizon_claims()
    _write(BEYOND, record)
    return len(record["results"])


# --------------------------------------------------------------------------- check


def _stable(row: Mapping[str, Any]) -> dict[str, Any]:
    """A row without its timings or the pinned checkout's facts."""
    copy = json.loads(json.dumps(row))
    copy.pop("wall_seconds", None)
    copy.pop("source_index", None)
    copy["decision"].pop("cpu_seconds", None)
    return copy


def publication_problems() -> list[str]:
    """The publications receipt against the issue, the packet and its own arithmetic."""
    record = publications()
    rows = record["rows"]
    problems: list[str] = []
    if [row["n"] for row in rows] != [row.n for row in decided_claims()]:
        return ["the publications receipt's counts are not the issue's at or below 1024"]
    digests = manifest()
    by_n = {row.n: row for row in decided_claims()}
    for row in rows:
        claim = by_n[row["n"]]
        side = Fraction(row["exact_side"])
        earlier = Fraction(row["earlier"]["exact_side"])
        if row["printed"] != claim.printed:
            problems.append(f"n={row['n']}: the receipt's print is not the issue's")
        if Fraction(row["below_earlier_by"]) != earlier - side:
            problems.append(f"n={row['n']}: the margin is not the sides' difference")
        try:
            kept = classify(side, claim.printed, earlier)
        except ReplayError as error:
            problems.append(f"n={row['n']}: {error}")
            continue
        if kept != row["set"]:
            problems.append(f"n={row['n']}: the set is {kept}, not {row['set']}")
        if (row["set"] == RESTATED) == retained(row["n"]):
            problems.append(f"n={row['n']}: retention does not follow the set")
        if retained(row["n"]) and certificate(claim).side != side:
            problems.append(f"n={row['n']}: the retained certificate's side differs")
        if not retained(row["n"]) and claim.path not in digests:
            problems.append(f"n={row['n']}: the restated certificate is not pinned")
        if row["set"] != RESTATED and row["first_commit_public"]:
            problems.append(f"n={row['n']}: first committed while public, yet new")
    sizes = {name: len(record["sets"][name]) for name in SET_SIZES}
    if sizes != SET_SIZES:
        problems.append(f"the sets are {sizes}, not {SET_SIZES}")
    return problems


def check(*, replay: bool, workers: int = 1) -> list[str]:
    """Problems with the receipts against the packet and the issue; empty when they hold.

    With ``replay`` every retained row and its controls are decided again, on ``workers``
    processes, and each must equal its receipt row apart from timings.
    """
    custody()
    problems = publication_problems()
    rows = replayed_claims()
    receipt = json.loads(FILTERED.read_text(encoding="utf-8"))
    stored = receipt["rows"]
    if [row["n"] for row in stored] != [row.n for row in rows]:
        return [*problems, "the filtered receipt's rows are not the retained certificates"]
    again: list[dict[str, Any]] = []
    if replay:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            again = list(pool.map(decide_row, rows))
    for position, (row, kept) in enumerate(zip(rows, stored, strict=True)):
        if kept["certificate"] != row.path or kept["printed"] != row.printed:
            problems.append(f"n={row.n}: receipt row differs from the issue")
        if not kept["verified"]:
            problems.append(f"n={row.n}: not verified")
        if [control["control"] for control in kept["controls"]] != list(base.CONTROLS):
            problems.append(f"n={row.n}: the controls are not the declared six")
        problems.extend(
            f"n={row.n}: {control['control']} was accepted"
            for control in kept["controls"]
            if not (control["refused_by_sqpack"] and control["refused_by_independent"])
        )
        index = kept.get("source_index")
        if index is not None and not all(
            index.get(key, True)
            for key in (
                "bound_equals_header",
                "parent_poses_lead",
                "added_squares_axis_aligned",
                "side_is_parent_side_plus_layers",
            )
        ):
            problems.append(f"n={row.n}: the file does not realize the index's entry")
        if again and _stable(again[position]) != _stable(kept):
            problems.append(f"n={row.n}: the replay differs from the receipt")
    if receipt["summary"] != base.summary(stored):
        problems.append("the summary does not match the rows")
    if not BEYOND.is_file() or json.loads(BEYOND.read_text(encoding="utf-8")) != (
        beyond_horizon_claims()
    ):
        problems.append("the beyond-horizon claims record differs from its rebuild")
    return problems + _cross_check_problems(rows)


def _cross_check_problems(rows: Sequence[Claim]) -> list[str]:
    """The all-pairs sample's and the Göbel receipt's outcomes."""
    problems: list[str] = []
    sample = json.loads(EXHAUSTIVE.read_text(encoding="utf-8"))["rows"]
    problems.extend(
        f"n={row['n']}: the all-pairs sample disagrees with the filtered decision"
        for row in sample
        if not all(
            row[key]
            for key in (
                "exact_verify_passed",
                "independent_passed",
                "routes_agree_on_least_gap",
                "equals_filtered_least_gap",
                "equals_filtered_least_wall",
            )
        )
    )
    comparison = json.loads(GOEBEL.read_text(encoding="utf-8"))["comparison"]
    if comparison["rows"] != len(rows) or comparison["tally"]["below"] != len(rows):
        problems.append("a replayed side is not below Göbel's construction at its count")
    compared = [
        (item["n"], Fraction(item["side"]), item["relation"]) for item in comparison["detail"]
    ]
    if compared != [(row.n, certificate(row).side, "below") for row in rows]:
        problems.append("the Göbel receipt's rows are not the retained certificates' sides")
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n", 1)[0])
    commands = parser.add_subparsers(dest="command", required=True)
    history = commands.add_parser("publications")
    history.add_argument("--history", type=Path, required=True)
    run = commands.add_parser("filtered")
    run.add_argument("--pinned", type=Path)
    run.add_argument("--workers", type=int, default=2)
    sample = commands.add_parser("exhaustive")
    sample.add_argument("--n", type=int, nargs="+", required=True)
    sample.add_argument("--workers", type=int, default=2)
    commands.add_parser("goebel")
    commands.add_parser("claims-record")
    audit = commands.add_parser("check")
    audit.add_argument("--replay", action="store_true")
    audit.add_argument("--workers", type=int, default=1)
    args = parser.parse_args(argv)
    actions: dict[str, Callable[[], Any]] = {
        "publications": lambda: write_publications(args.history),
        "filtered": lambda: filtered(args.pinned, args.workers)["summary"],
        "exhaustive": lambda: exhaustive(args.n, args.workers)["rows"],
        "goebel": goebel,
        "claims-record": claims_record,
    }
    if args.command == "check":
        problems = check(replay=args.replay, workers=args.workers)
        for problem in problems:
            print(problem)
        recorded, held = len(counts_in(RECORDED)), len(counts_in(HELD))
        print(
            "FAILED"
            if problems
            else f"OK: {recorded} recorded and {held} held rows verified, every control refused"
        )
        return 1 if problems else 0
    print(json.dumps(actions[args.command](), indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
