"""Decide issue #678's 85 claimed upper bounds exactly, from the retained packet.

Francisco Couzo's issue #678 links 83 rational certificates at
franciscouzo/square-packing ``7b6c87e``, each ``n S`` then ``n`` rows ``x y t`` (centre and
``t = tan(theta/2)``), and claims ``s(n) <= P`` with ``P`` the header side rounded up at
12 places. Two rows, 545 and 641, delete one square from the 546 and 642 certificates.
The packet ``resources/web/couzo-issue678-2026-10-18`` retains the 83 files; this module
reads them from it once `acquire_source --check` holds the packet, and decides every row:

- **the side.** The header side ``S`` is the claim's exact side. The printed ``P`` must be
  its upward rounding at 12 places, ``P - 10^-12 < S <= P``, decided over ``Q``.
- **the geometry, by two exact routes over Q.** Route ``sqpack`` materializes the
  certificate through ``sqpack.witness`` and decides with ``sqpack.verify``'s predicates
  (`check_unit_squares`, `separated`); route ``independent`` builds corners with the
  kernel's half-angle conversion and decides with
  ``devtools.check_rational_witness_independent``'s ``square_failures`` and ``pair_gap``.
  Both check every corner against all four walls.
- **an exactly justified pair filter.** Only pairs whose centres are closer than
  ``sqrt 2`` are decided, chosen by exact rational comparison ``dx^2 + dy^2 < 2``. A unit
  square's interior lies inside the open disc of radius ``sqrt(2)/2`` about its centre, so
  two squares whose centres are at least ``sqrt 2`` apart have disjoint interiors; no pair
  that could overlap is skipped. The lemma needs each square to be a unit square about the
  centre the filter read, so both routes also check that every square is a unit square and
  that the mean of its corners is that centre, exactly.
- **the deletion rows.** 545 and 641 are the 546 and 642 certificates with their last
  square removed, at the same side, and are decided as such. Removing squares from a
  packing leaves a packing, so any choice of square gives the same bound.
- **controls.** For each of the 83 certificates, five mutants are decided by both routes,
  each with its known answer: square 2 replaced by square 1 (overlap); square 1 moved
  ``S + 2`` to the right (wall); the side lowered by the least top or right clearance plus
  ``10^-18`` (wall, by ``10^-18``); square 1 enlarged by ``10^-12`` about its centre (not a
  unit square); and the candidate pair with the least ``|dy|``, at most ``1/2``, given equal
  ``x`` (one coordinate changed), so the centres are within ``1/2`` and the inscribed open
  discs of radius ``1/2`` share a point (overlap). Every mutant must be refused by both.

``claims-record`` writes ``acquisition/beyond-horizon-claims.json``, the record of the 83
rows beyond the case corpus (``n > 324``) that ``check_source_coverage`` reads the
``couzo-issue678-2026-10-18`` source's beyond-horizon rows from: each row's print, its
exact side and that side rounded up at 16 places, rebuilt from the issue and the
retained certificates, which ``check`` holds it to.

``exhaustive`` runs the maintained two-route kernel of ``devtools.evand_arrangement_reports``
(every pair, no filter) on chosen counts, as a cross-check of the filtered decision and a
price for the complete all-pairs replay. ``source-checker`` runs the source's own checker,
``verify_bound_certificate.py``, unchanged from its retained copy in a ``python -I`` child
process, on the 83 certificates, the two derived packings and the four controls the
certificate format can state. ``check`` reads the receipts back against the packet and the
issue, and ``check --replay`` decides every filtered row again.

From ``packing/``, with the project interpreter::

    python -m devtools.couzo_678_replay filtered [--pinned CHECKOUT] [--workers 2]
    python -m devtools.couzo_678_replay exhaustive --n 204 546 ... [--workers 2]
    python -m devtools.couzo_678_replay source-checker --scratch DIR
    python -m devtools.couzo_678_replay claims-record
    python -m devtools.couzo_678_replay check [--replay]

``--pinned`` names a checkout of the source at the pin; the source's ``manifest.json``,
which the packet pins by digest only, is then read from it, held to that digest, and its
stated bound and certificate digest compared with each row. A finite packing certifies an
upper bound and nothing more: novelty, rigidity and optimality are not decided here.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import re
import subprocess
import sys
import time
from collections.abc import Callable, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import acquire_source
from devtools import check_rational_witness_independent as independent
from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools.retained_data import read_retained_bytes
from sqpack.retained_json import dumps as retained_dumps
from sqpack.verify import check_unit_squares, separated
from sqpack.witness import materialize_exact_witness

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PACKET = ROOT / "resources/web/couzo-issue678-2026-10-18"
SOURCE = PACKET / "source"
MANIFEST = PACKET / "acquisition/upstream-subtree.sha256"
ISSUE = ROOT / "campaign/issue-intake/intake-20261019/issue-678.json"
CHECKER = SOURCE / "verify_bound_certificate.py"
RECEIPTS = PACKET / "receipts"
FILTERED = RECEIPTS / "filtered-exact-replay.json"
EXHAUSTIVE = RECEIPTS / "exhaustive-sample.json"
SOURCE_RECEIPT = RECEIPTS / "source-checker-replay.json"
GOEBEL = RECEIPTS / "goebel-comparison.json"
GOEBEL_PROGRAM = ROOT / (
    "resources/web/couzo-verified-bounds-2026-10-14/review/goebel_beyond_horizon.py"
)
GOEBEL_FORMAT = "couzo-678-goebel-comparison-v1"
BEYOND = PACKET / "acquisition/beyond-horizon-claims.json"
#: The format ``check_source_coverage.load_claims`` reads a beyond-horizon record in.
BEYOND_FORMAT = "upper-bound-beyond-horizon-claims-v1"
ISSUE_URL = "https://github.com/jlevy/squares/issues/678"
SOURCE_URL = "https://github.com/franciscouzo/square-packing"
#: The pin's commit time, when every certificate the issue links was first committed.
COMMITTED = "2026-10-18T23:19:02Z"
#: The last count of the case corpus; a row above it is a beyond-horizon row.
HORIZON = 324
#: The places the record's ``ceiling`` rounds each exact side up to.
CEILING_PLACES = 16
PIN = "7b6c87e129cf80b5ff9847b90b47fd30b4563c54"
ROWS = 85
CERTIFICATES = 83
DELETIONS = {545: 546, 641: 642}
PLACES = 12
FILTERED_FORMAT = "couzo-678-filtered-exact-replay-v1"
EXHAUSTIVE_FORMAT = "couzo-678-exhaustive-sample-v1"
SOURCE_FORMAT = "couzo-678-source-checker-replay-v1"
#: The square of the centre distance at and beyond which two unit squares cannot overlap.
FILTER_RADIUS_SQUARED = Fraction(2)
WALL_SLACK = Fraction(1, 10**18)
ENLARGEMENT = Fraction(1, 10**12)
CONTROLS = (
    "duplicate-square",
    "square-outside-container",
    "side-below-least-clearance",
    "square-enlarged",
    "one-coordinate-overlap",
)
#: The controls the certificate format states, which the source's checker is given.
SOURCE_CONTROLS = (
    "duplicate-square",
    "square-outside-container",
    "side-below-least-clearance",
    "one-coordinate-overlap",
)
FILTER_LEMMA = (
    "A unit square lies in the closed disc of radius sqrt(2)/2 about its centre and its "
    "interior in the open disc, so squares whose centres are at least sqrt(2) apart have "
    "disjoint interiors. Pairs are kept for decision when dx^2 + dy^2 < 2, compared "
    "exactly over Q from the certificate's centres; both routes check that every square "
    "is a unit square whose corner mean is that centre."
)
_ROW = re.compile(
    r"\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*\[certificate( \(delete (\d+)\))?\]"
    r"\(https://github\.com/franciscouzo/square-packing/blob/([0-9a-f]{40})/"
    r"(certificates/best/n(\d+)\.cert)\)"
)

type Point = tuple[Fraction, Fraction]
type Corners = list[Point]


class ReplayError(ValueError):
    """Refuse a row, a certificate or a receipt that does not hold."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ReplayError(message)


# --------------------------------------------------------------------------- the claims


@dataclass(frozen=True, slots=True)
class Claim:
    """One row of the issue's table: the count, its printed sides and its certificate."""

    n: int
    prior: str
    printed: str
    path: str
    certificate_n: int
    deleted: int


def claims() -> list[Claim]:
    """The issue's 85 rows, read from its retained body, refused unless all are there."""
    body = json.loads(ISSUE.read_text(encoding="utf-8"))["body"]
    rows: list[Claim] = []
    for line in body.splitlines():
        match = _ROW.match(line)
        if match is None:
            continue
        _require(match[6] == PIN, f"n={match[1]}: the link names another commit")
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
    _require(len(rows) == ROWS, f"{len(rows)} rows, not {ROWS}")
    _require([row.n for row in rows] == sorted({row.n for row in rows}), "rows out of order")
    _require(len({row.path for row in rows}) == CERTIFICATES, "not 83 distinct certificates")
    for row in rows:
        expected = DELETIONS.get(row.n, row.n)
        _require(
            row.certificate_n == expected and row.deleted == row.certificate_n - row.n,
            f"n={row.n}: the link and the deletion do not agree",
        )
    return rows


def manifest() -> dict[str, str]:
    """The packet's upstream digests, by upstream path."""
    digests: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, path = line.split("  ./", 1)
        digests[path] = digest
    return digests


def custody() -> None:
    """Refuse to read the packet unless ``acquire_source --check`` holds for it.

    That check holds every retained file to the digest the packet's manifest pinned at
    acquisition; the files themselves are then read from Git and compared with nothing.
    """
    problems = acquire_source.check(PACKET, REPO)
    _require(not problems, "packet custody: " + "; ".join(problems))


def certificate_bytes(path: str, digests: dict[str, str]) -> bytes:
    """A retained certificate's bytes; ``digests`` names the files the packet pins."""
    _require(path in digests, f"{path}: not in the packet's manifest")
    return read_retained_bytes(SOURCE / path)


def certificate(row: Claim, digests: dict[str, str]) -> legacy.Certificate:
    """The packing a row claims: its certificate, less the squares the row deletes."""
    parsed = legacy.parse(
        certificate_bytes(row.path, digests).decode("utf-8"), expected_n=row.certificate_n
    )
    if row.deleted:
        parsed = legacy.Certificate(row.n, parsed.side, parsed.poses[: row.n])
    return parsed


def rounds_up_to(side: Fraction, printed: str) -> bool:
    """``printed - 10^-PLACES < side <= printed``: ``printed`` is ``side`` rounded up."""
    _require(re.fullmatch(rf"[0-9]+\.[0-9]{{{PLACES}}}", printed), f"{printed}: not 12 places")
    value = Fraction(printed)
    return value - Fraction(1, 10**PLACES) < side <= value


# --------------------------------------------------------------------------- geometry


@dataclass(frozen=True, slots=True)
class Geometry:
    """One packing as both routes read it: the side, the centres and both corner lists."""

    n: int
    side: Fraction
    centres: tuple[Point, ...]
    sqpack_squares: tuple[tuple[Point, ...], ...]
    independent_squares: tuple[tuple[Point, ...], ...]


def geometry(cert: legacy.Certificate) -> Geometry:
    """Both routes' exact corners of a certificate, each from its own conversion."""
    squares, side = materialize_exact_witness(legacy.basis_witness(cert))
    _require(side == cert.side, "the sqpack side differs from the header")
    return Geometry(
        n=cert.n,
        side=cert.side,
        centres=tuple((pose.x, pose.y) for pose in cert.poses),
        sqpack_squares=tuple(
            tuple((Fraction(x), Fraction(y)) for x, y in sq) for sq in squares
        ),
        independent_squares=tuple(tuple(corners) for corners in legacy.corner_squares(cert)),
    )


def candidate_pairs(centres: Sequence[Point]) -> list[tuple[int, int]]:
    """Every pair whose centres are closer than ``sqrt 2``, by exact comparison.

    The indices are sorted by ``x``; for each square the scan stops at the first later one
    whose ``x`` is at least ``sqrt 2`` further, since every square after it is too.
    """
    order = sorted(range(len(centres)), key=lambda index: centres[index][0])
    pairs: list[tuple[int, int]] = []
    for position, left in enumerate(order):
        lx, ly = centres[left]
        for right in order[position + 1 :]:
            rx, ry = centres[right]
            dx = rx - lx
            if dx * dx >= FILTER_RADIUS_SQUARED:
                break
            dy = ry - ly
            if dx * dx + dy * dy < FILTER_RADIUS_SQUARED:
                pairs.append((min(left, right), max(left, right)))
    return sorted(pairs)


def _centre_failures(squares: Sequence[Sequence[Point]], centres: Sequence[Point]) -> list[str]:
    return [
        f"square {index}: corner mean is not the filter's centre"
        for index, (square, centre) in enumerate(zip(squares, centres, strict=True), start=1)
        if (sum(x for x, _ in square) / 4, sum(y for _, y in square) / 4) != centre
    ]


def _rational_sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def route_sqpack(shape: Geometry, pairs: Sequence[tuple[int, int]]) -> dict[str, Any]:
    """``sqpack.verify``'s exact predicates on the candidate pairs and every wall."""
    squares = [list(square) for square in shape.sqpack_squares]
    failures = [
        f"{kind}: {detail}" for kind, detail in check_unit_squares(squares, _rational_sign)
    ]
    failures += _centre_failures(squares, shape.centres)
    contacts = 0
    for index, square in enumerate(squares, start=1):
        for x, y in square:
            for value in (x, y, shape.side - x, shape.side - y):
                if value < 0:
                    failures.append(f"square {index} crosses a wall")
                elif value == 0:
                    contacts += 1
    touching = strict = 0
    for left, right in pairs:
        verdict = separated(squares[left], squares[right], _rational_sign)
        if verdict is None:
            failures.append(f"squares {left + 1} and {right + 1} overlap")
        elif verdict == 0:
            touching += 1
        else:
            strict += 1
    return {
        "passed": not failures,
        "pairs_decided": len(pairs),
        "touching_pairs": touching,
        "strict_pairs": strict,
        "container_contacts": contacts,
        "failures": failures[:20],
        "failure_count": len(failures),
    }


def route_independent(shape: Geometry, pairs: Sequence[tuple[int, int]]) -> dict[str, Any]:
    """The independent checker's exact predicates on the candidate pairs and every wall."""
    squares = [list(square) for square in shape.independent_squares]
    failures = [
        failure
        for index, square in enumerate(squares, start=1)
        for failure in independent.square_failures(square, index)
    ]
    failures += _centre_failures(squares, shape.centres)
    clearances = [
        value
        for square in squares
        for x, y in square
        for value in (x, y, shape.side - x, shape.side - y)
    ]
    least_wall = min(clearances)
    if least_wall < 0:
        failures.append(f"container penetration {least_wall}")
    gaps = [
        (independent.pair_gap(squares[left], squares[right]), left, right)
        for left, right in pairs
    ]
    overlaps = [(gap, left, right) for gap, left, right in gaps if gap < 0]
    if overlaps:
        gap, left, right = min(overlaps)
        failures.append(
            f"{len(overlaps)} overlapping pairs; worst {gap} at {left + 1}, {right + 1}"
        )
    least = min(gaps) if gaps else None
    return {
        "passed": not failures,
        "pairs_decided": len(pairs),
        "least_wall_clearance": str(least_wall),
        "least_pair_gap": None if least is None else str(least[0]),
        "least_pair": None if least is None else [least[1] + 1, least[2] + 1],
        "failures": failures[:20],
        "failure_count": len(failures),
    }


def decide(shape: Geometry) -> dict[str, Any]:
    """Both routes on one packing, with the filter's counts."""
    started = time.process_time()
    pairs = candidate_pairs(shape.centres)
    filtered = time.process_time()
    first = route_sqpack(shape, pairs)
    middle = time.process_time()
    second = route_independent(shape, pairs)
    ended = time.process_time()
    return {
        "n": shape.n,
        "side": legacy.literal(shape.side),
        "all_pairs": shape.n * (shape.n - 1) // 2,
        "candidate_pairs": len(pairs),
        "passed": first["passed"] and second["passed"],
        "sqpack": first,
        "independent": second,
        "cpu_seconds": {
            "filter": round(filtered - started, 3),
            "sqpack": round(middle - filtered, 3),
            "independent": round(ended - middle, 3),
        },
    }


# --------------------------------------------------------------------------- controls


def _scaled(square: Sequence[Point], centre: Point, factor: Fraction) -> tuple[Point, ...]:
    cx, cy = centre
    return tuple((cx + (x - cx) * factor, cy + (y - cy) * factor) for x, y in square)


def _least_top_right(shape: Geometry) -> Fraction:
    return min(
        min(shape.side - x, shape.side - y)
        for square in shape.independent_squares
        for x, y in square
    )


def overlap_pair(cert: legacy.Certificate) -> tuple[int, int]:
    """The candidate pair with the least ``|dy|``, which must be at most 1/2."""
    centres = [(pose.x, pose.y) for pose in cert.poses]
    pairs = candidate_pairs(centres)
    left, right = min(
        pairs, key=lambda pair: (abs(centres[pair[1]][1] - centres[pair[0]][1]), pair)
    )
    _require(
        abs(centres[right][1] - centres[left][1]) <= Fraction(1, 2), "no pair with |dy| <= 1/2"
    )
    return left, right


def mutant_certificate(cert: legacy.Certificate, control: str) -> legacy.Certificate:
    """The control as a certificate, for the four the ``n S`` / ``x y t`` format states."""
    poses = list(cert.poses)
    if control == "duplicate-square":
        poses[1] = poses[0]
    elif control == "square-outside-container":
        poses[0] = replace(poses[0], x=poses[0].x + cert.side + 2)
    elif control == "side-below-least-clearance":
        shape = geometry(cert)
        return replace(cert, side=cert.side - _least_top_right(shape) - WALL_SLACK)
    elif control == "one-coordinate-overlap":
        left, right = overlap_pair(cert)
        poses[right] = replace(poses[right], x=poses[left].x)
    else:
        raise ReplayError(f"{control}: not a certificate control")
    return replace(cert, poses=tuple(poses))


def control_geometry(cert: legacy.Certificate, control: str) -> Geometry:
    """The control's geometry as both routes read it."""
    if control == "square-enlarged":
        shape = geometry(cert)
        factor = 1 + ENLARGEMENT
        return replace(
            shape,
            sqpack_squares=(
                _scaled(shape.sqpack_squares[0], shape.centres[0], factor),
                *shape.sqpack_squares[1:],
            ),
            independent_squares=(
                _scaled(shape.independent_squares[0], shape.centres[0], factor),
                *shape.independent_squares[1:],
            ),
        )
    return geometry(mutant_certificate(cert, control))


def decide_controls(cert: legacy.Certificate) -> list[dict[str, Any]]:
    """Every control of one certificate, decided by both routes; each must be refused."""
    rows = []
    for control in CONTROLS:
        result = decide(control_geometry(cert, control))
        rows.append(
            {
                "control": control,
                "refused_by_sqpack": not result["sqpack"]["passed"],
                "refused_by_independent": not result["independent"]["passed"],
                "candidate_pairs": result["candidate_pairs"],
                "sqpack_failures": result["sqpack"]["failures"][:3],
                "independent_failures": result["independent"]["failures"][:3],
            }
        )
    return rows


# --------------------------------------------------------------------------- the replay


def decide_row(row: Claim) -> dict[str, Any]:
    """One row: custody, the side against the print, both routes, and its controls."""
    digests = manifest()
    cert = certificate(row, digests)
    started = time.monotonic()
    result = decide(geometry(cert))
    record: dict[str, Any] = {
        "n": row.n,
        "certificate": row.path,
        "certificate_sha256": digests[row.path],
        "deleted_squares": row.deleted,
        "printed": row.printed,
        "issue_prior": row.prior,
        "exact_side": legacy.literal(cert.side),
        "side_ceiling_16": legacy.ceiling_decimal(cert.side, 16),
        "printed_is_upward_rounding": rounds_up_to(cert.side, row.printed),
        "verified": result["passed"] and rounds_up_to(cert.side, row.printed),
        "decision": result,
    }
    if row.deleted == 0:
        record["controls"] = decide_controls(cert)
    record["wall_seconds"] = round(time.monotonic() - started, 3)
    return record


def source_manifest_rows(checkout: Path, rows: Sequence[Claim]) -> dict[str, Any]:
    """The source manifest's bound and digest for each row, read from a pinned checkout."""
    digests = manifest()
    path = "certificates/best/manifest.json"
    raw = (checkout / path).read_bytes()
    _require(hashlib.sha256(raw).hexdigest() == digests[path], "manifest.json differs from pin")
    witnesses = json.loads(raw)["witnesses"]
    results = []
    for row in rows:
        entry = witnesses[str(row.n)]
        header = certificate(row, digests).side
        own = entry["certificate"]
        own_side = Fraction(entry["bound"])
        results.append(
            {
                "n": row.n,
                "manifest_certificate": own,
                "manifest_bound_equals_claim_side": own_side == header,
                "manifest_digest_matches": entry["certificate_sha256"] == digests.get(own),
                "manifest_bound_ceiling_12": legacy.ceiling_decimal(own_side, PLACES),
                "credit": entry.get("credit", ""),
                "source_strict_valid": entry.get("strict_verification", {}).get("valid"),
            }
        )
    return {"manifest_sha256": digests[path], "rows": results}


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


def filtered(pinned: Path | None, workers: int) -> dict[str, Any]:
    """Decide all 85 rows and every control, and write the filtered receipt."""
    custody()
    rows = claims()
    started = datetime.now(UTC)
    wall = time.monotonic()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(decide_row, rows))
    receipt: dict[str, Any] = {
        "format": FILTERED_FORMAT,
        "issue": "https://github.com/jlevy/squares/issues/678",
        "source_commit": PIN,
        "packet": PACKET.relative_to(REPO).as_posix(),
        "program": "packing/devtools/couzo_678_replay.py",
        "filter_lemma": FILTER_LEMMA,
        "controls": list(CONTROLS),
        "environment": _environment(),
        "started_utc": started.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "wall_seconds": round(time.monotonic() - wall, 1),
        "workers": workers,
        "rows": results,
        "summary": summary(results),
    }
    if pinned is not None:
        receipt["source_manifest"] = source_manifest_rows(pinned, rows)
    _write(FILTERED, receipt)
    return receipt


def summary(results: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """Counts and totals over the rows."""
    controls = [control for row in results for control in row.get("controls", [])]
    decisions = [row["decision"] for row in results]
    return {
        "rows": len(results),
        "verified": sum(1 for row in results if row["verified"]),
        "refused": [row["n"] for row in results if not row["verified"]],
        "controls": len(controls),
        "controls_refused_by_both": sum(
            1 for c in controls if c["refused_by_sqpack"] and c["refused_by_independent"]
        ),
        "all_pairs": sum(d["all_pairs"] for d in decisions),
        "candidate_pairs": sum(d["candidate_pairs"] for d in decisions),
        "positive_cpu_seconds": round(
            sum(sum(d["cpu_seconds"].values()) for d in decisions), 1
        ),
    }


# --------------------------------------------------------------------------- cross-checks


def exhaustive_row(row: Claim) -> dict[str, Any]:
    """The maintained all-pairs kernel on one row, beside the filtered decision of it."""
    cert = certificate(row, manifest())
    wall = time.monotonic()
    case = kernel.run_case(cert, "positive")
    elapsed = time.monotonic() - wall
    first, second = case["exact_verify"], case["independent"]
    narrow = decide(geometry(cert))["independent"]
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
    """The maintained all-pairs kernel on chosen rows, each against the filtered decision."""
    custody()
    rows = {row.n: row for row in claims()}
    for n in counts:
        _require(n in rows, f"n={n}: not a claimed row")
    started = datetime.now(UTC)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(exhaustive_row, [rows[n] for n in counts]))
    receipt = {
        "format": EXHAUSTIVE_FORMAT,
        "kernel": "devtools.evand_arrangement_reports.run_case, positive job, every pair",
        "environment": _environment(),
        "started_utc": started.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "workers": workers,
        "rows": results,
        "price": price(results),
    }
    _write(EXHAUSTIVE, receipt)
    return receipt


def price(results: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """The measured all-pairs rate, applied to every distinct certificate of the issue."""
    pairs = sum(row["pairs_tested"] for row in results)
    seconds = sum(sum(row["cpu_seconds"].values()) for row in results)
    distinct = {row.certificate_n for row in claims()}
    total_pairs = sum(n * (n - 1) // 2 for n in distinct)
    positive = seconds / pairs * total_pairs
    return {
        "sample_pairs": pairs,
        "sample_cpu_seconds": round(seconds, 1),
        "seconds_per_pair_both_routes": seconds / pairs,
        "all_pairs_of_83_certificates": total_pairs,
        "positive_cpu_hours": round(positive / 3600, 2),
        "certify_three_jobs_cpu_hours": round(3 * positive / 3600, 2),
        "certify_and_replay_cpu_hours": round(6 * positive / 3600, 2),
    }


def _write_certificate(cert: legacy.Certificate, path: Path) -> None:
    path.write_text(legacy.serialize(cert), encoding="utf-8")


def source_run(path: Path) -> dict[str, Any]:
    shown = subprocess.run(
        (sys.executable, "-I", str(CHECKER), str(path)),
        capture_output=True,
        text=True,
        check=False,
        timeout=600,
    )
    lines = shown.stdout.strip().splitlines()
    result = json.loads(lines[-1]) if lines else {}
    return {
        "exit": shown.returncode,
        "valid": result.get("valid"),
        "strict_valid": result.get("strict_valid"),
        "candidate_pairs": result.get("candidate_pairs"),
        "near_pairs": result.get("near_pairs"),
        "side": result.get("side"),
    }


def source(scratch: Path) -> dict[str, Any]:
    """The source's checker, from its retained copy, on every packing and four controls."""
    scratch.mkdir(parents=True, exist_ok=True)
    digests = manifest()
    custody()
    checker_digest = digests["verify_bound_certificate.py"]
    results = []
    for row in claims():
        cert = certificate(row, digests)
        if row.deleted:
            path = scratch / f"derived-n{row.n}.cert"
            _write_certificate(cert, path)
        else:
            path = SOURCE / row.path
        record: dict[str, Any] = {"n": row.n, "positive": source_run(path)}
        if not row.deleted:
            record["controls"] = {}
            for control in SOURCE_CONTROLS:
                mutant = scratch / f"n{row.n}-{control}.cert"
                _write_certificate(mutant_certificate(cert, control), mutant)
                record["controls"][control] = source_run(mutant)
                mutant.unlink()
        results.append(record)
    receipt = {
        "format": SOURCE_FORMAT,
        "checker": "source/verify_bound_certificate.py",
        "checker_sha256": checker_digest,
        "environment": _environment(),
        "started_utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "rows": results,
    }
    _write(SOURCE_RECEIPT, receipt)
    return receipt


def _goebel_program() -> Any:
    """The 15 October packet's exact Göbel comparison, loaded from its retained path."""
    spec = importlib.util.spec_from_file_location("goebel_beyond_horizon", GOEBEL_PROGRAM)
    if spec is None or spec.loader is None:
        raise ReplayError("the Göbel program is missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def goebel() -> dict[str, Any]:
    """Every claimed exact side against Göbel's classical constructions, exactly.

    The families, their deletion to smaller counts and the exact sign test are those of
    ``couzo-verified-bounds-2026-10-14/review/goebel_beyond_horizon.py``, which this reads
    from its retained path and does not change.
    """
    custody()
    program = _goebel_program()
    forms = program.families(program.LIMIT)
    digests = manifest()
    rows = [(row.n, certificate(row, digests).side, row.path) for row in claims()]
    result = program.compare("issue #678 at 7b6c87e", rows, forms)
    receipt = {
        "format": GOEBEL_FORMAT,
        "program": GOEBEL_PROGRAM.relative_to(REPO).as_posix(),
        "families": "Göbel squares, Göbel strips and corner-touching strips, with deletion",
        "comparison": result,
    }
    _write(GOEBEL, receipt)
    return {"rows": result["rows"], "tally": result["tally"], "above": result["above"]}


# --------------------------------------------------------------------------- claims record


def beyond_horizon_claims() -> dict[str, Any]:
    """The rows beyond the corpus as the coverage register reads them, rebuilt.

    Each row keeps the issue's print as ``offered_side``, the side ``check_source_coverage``
    holds a dated beyond-horizon row to byte for byte; the exact side is the certificate's
    header side, which a deletion row shares with the certificate it deletes from.
    """
    custody()
    digests = manifest()
    results = []
    for row in claims():
        if row.n <= HORIZON:
            continue
        side = certificate(row, digests).side
        _require(rounds_up_to(side, row.printed), f"n={row.n}: the print does not round up")
        results.append(
            {
                "n": row.n,
                "offered_side": row.printed,
                "exact_side": legacy.literal(side),
                "ceiling": legacy.ceiling_decimal(side, CEILING_PLACES),
                "certificate": row.path,
                "deleted": row.deleted,
                "first_committed": COMMITTED,
            }
        )
    return {
        "format": BEYOND_FORMAT,
        "issue": ISSUE_URL,
        "source": SOURCE_URL,
        "revision": PIN,
        "horizon": HORIZON,
        "results": results,
    }


def claims_record() -> int:
    """Write the beyond-horizon claims record and return its row count."""
    record = beyond_horizon_claims()
    _write(BEYOND, record)
    return len(record["results"])


# --------------------------------------------------------------------------- check


def _stable(row: dict[str, Any]) -> dict[str, Any]:
    """A row without its timings."""
    copy = json.loads(json.dumps(row))
    copy.pop("wall_seconds", None)
    copy["decision"].pop("cpu_seconds", None)
    return copy


def check(*, replay: bool) -> list[str]:
    """Problems with the receipts against the packet and the issue; empty when they hold."""
    custody()
    problems: list[str] = []
    rows = claims()
    receipt = json.loads(FILTERED.read_text(encoding="utf-8"))
    stored = receipt["rows"]
    if [row["n"] for row in stored] != [row.n for row in rows]:
        return ["the filtered receipt's rows are not the issue's"]
    for row, kept in zip(rows, stored, strict=True):
        if kept["certificate"] != row.path or kept["printed"] != row.printed:
            problems.append(f"n={row.n}: receipt row differs from the issue")
        if not kept["verified"]:
            problems.append(f"n={row.n}: not verified")
        if [control["control"] for control in kept.get("controls", [])] != (
            [] if row.deleted else list(CONTROLS)
        ):
            problems.append(f"n={row.n}: the controls are not the declared five")
        problems.extend(
            f"n={row.n}: {control['control']} was accepted"
            for control in kept.get("controls", [])
            if not (control["refused_by_sqpack"] and control["refused_by_independent"])
        )
        if replay and _stable(decide_row(row)) != _stable(kept):
            problems.append(f"n={row.n}: the replay differs from the receipt")
    if receipt["summary"] != summary(stored):
        problems.append("the summary does not match the rows")
    if not BEYOND.is_file() or json.loads(BEYOND.read_text(encoding="utf-8")) != (
        beyond_horizon_claims()
    ):
        problems.append("the beyond-horizon claims record differs from its rebuild")
    return problems + _cross_check_problems(rows)


def _cross_check_problems(rows: Sequence[Claim]) -> list[str]:
    """The source checker's, the all-pairs sample's and the Göbel receipts' outcomes."""
    problems: list[str] = []
    counts = [row.n for row in rows]
    runs = json.loads(SOURCE_RECEIPT.read_text(encoding="utf-8"))["rows"]
    if [run["n"] for run in runs] != counts:
        problems.append("the source checker's rows are not the issue's")
    for run in runs:
        if not (run["positive"]["exit"] == 0 and run["positive"]["valid"] is True):
            problems.append(f"n={run['n']}: the source checker did not accept the packing")
        problems.extend(
            f"n={run['n']}: the source checker accepted {name}"
            for name, outcome in run.get("controls", {}).items()
            if outcome["exit"] == 0 or outcome["valid"] is not False
        )
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
    goebel_rows = json.loads(GOEBEL.read_text(encoding="utf-8"))["comparison"]
    if goebel_rows["rows"] != len(rows) or goebel_rows["tally"]["below"] != len(rows):
        problems.append("a claimed side is not below Göbel's construction at its count")
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n", 1)[0])
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("filtered")
    run.add_argument("--pinned", type=Path)
    run.add_argument("--workers", type=int, default=2)
    sample = commands.add_parser("exhaustive")
    sample.add_argument("--n", type=int, nargs="+", required=True)
    sample.add_argument("--workers", type=int, default=2)
    own = commands.add_parser("source-checker")
    own.add_argument("--scratch", type=Path, required=True)
    commands.add_parser("goebel")
    commands.add_parser("claims-record")
    audit = commands.add_parser("check")
    audit.add_argument("--replay", action="store_true")
    args = parser.parse_args(argv)
    actions: dict[str, Callable[[], Any]] = {
        "filtered": lambda: filtered(args.pinned, args.workers)["summary"],
        "exhaustive": lambda: exhaustive(args.n, args.workers)["price"],
        "source-checker": lambda: len(source(args.scratch)["rows"]),
        "goebel": goebel,
        "claims-record": claims_record,
    }
    if args.command == "check":
        problems = check(replay=args.replay)
        for problem in problems:
            print(problem)
        print("FAILED" if problems else "OK: 85 rows verified, every control refused")
        return 1 if problems else 0
    print(json.dumps(actions[args.command](), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
