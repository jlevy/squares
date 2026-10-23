#!/usr/bin/env python3
"""Decide Evan Daniel's exact square-packing certificates with this repository's geometry.

``evand/square-packing`` at ``13ee36e`` (5 October 2026) publishes, under
``s12/search/exact/batch/certs/``, one certificate ``n-N.cert`` of ``s(n) <= S'`` for 321
of the register's 324 counts: ``n`` unit squares, each a rational centre ``(x, y)`` and a
rational ``t = tan(theta/2)``, so that ``(c, s) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))``
satisfies ``c^2 + s^2 = 1`` exactly, inside a box of rational side ``S'``. At 48 counts
``S'`` lies below the side the register reports, by 3e-13 to 5e-11; issue #375 asks for
those to be registered. The source checks each certificate with two exact checkers of its
own (``verify_cert.py`` and ``verify_cert2.py``).

No checker here read that form, so this module converts it exactly and decides it with
the two exact checkers this repository already runs in its ``exact verification`` step:

- the certificate becomes a rational ``center-basis`` Witness/v2, ``(x, y)`` and ``(c, s)``
  as fractions, which ``sqpack.witness.exact_verify`` materializes and decides over Q;
- the same squares as rational corners, computed here from ``(x, y, c, s)``, go to
  ``devtools.check_rational_witness_independent``, which shares no geometry or
  verification code with ``sqpack``.

The parse and the map from ``t`` to ``(c, s)`` are this module's own and are the common
mode of the two decisions; the corners built here go to the independent checker alone,
which checks their shape itself. The source's checkers are not imported by any code here:
``source-replay`` runs them as separate processes, and ``controls`` copies them, unchanged,
into a scratch tree to run the source's ``verify_all.sh``.

**What its author read.** The format as the source's README states it, and the source's
``verify_cert.py`` and ``verify_cert2.py``, read before this module was written to
confirm that the corners it builds from ``(x, y, t)`` are the squares those checkers
decide. Nothing of theirs, nor of the source's solver, is imported, but two expressions
are theirs, transcribed (RF-1 of the 22 October 2026 review of issue #728): the reader's
line filter in `parse`, which skips blank lines and lines beginning with ``#``, is the
filter of both checkers, and `Pose.corners`, from which the independent checker decides,
is ``verify_cert2.py``'s ``corners`` term for term. The corner construction is the
format's definition, and a clean-room checker derived it without reading theirs. The two
deciders predate this import: ``sqpack.witness`` is this repository's own, and
``devtools.check_rational_witness_independent`` was written to share no geometry or
verification code with it.

Subcommands, from ``packing/``:

``check [--certs DIR] [--n N ...] [--workers K] [--receipt PATH]``
    Parse, convert and decide every certificate, and write a receipt of each verdict,
    its exact side and its least clearances. Without ``--certs`` it reads the packet's
    retained certificates and writes ``receipts/first-party-check.json``; that receipt is
    what ``--check`` holds the retained certificates to.

``check --check``
    The retained certificates' digests and sides against the committed receipt, and
    each case record of an improving count against it. Fast and offline; the tests run
    it.

``source-replay --checkers DIR --certs DIR [--receipt PATH]``
    Run the source's own ``verify_cert.py`` and ``verify_cert2.py``, as retained, on
    each certificate with this project's interpreter, and record each exit status and
    verdict line.

``compare``
    Each improving certificate's side against the register's reported and verified
    upper bounds, and its pose against the register's known-best witness: the largest
    centre displacement and rotation difference over the squares, matched by nearest
    centre. Writes ``receipts/register-comparison.json``.

``controls``
    For each improving certificate, three altered copies: one square moved just past
    touching its tightest neighbour, the box shrunk past its least wall clearance by one
    unit of the side's denominator, and the box shrunk by that one unit alone, which is
    still a valid certificate when its clearance exceeds the unit. Every checker must
    refuse the first two. Writes ``receipts/negative-controls.json``.

The count ``n = 17`` is held by the owner for the n = 17 work on other branches
(think-x4v4): no subcommand reads, replays or records its certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import resource
import subprocess
import sys
import time
from collections.abc import Callable, Iterable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from decimal import ROUND_CEILING, ROUND_FLOOR, Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import check_rational_witness_independent as independent
from devtools.retained_data import read_retained_text
from sqpack import retained_json
from sqpack.witness import exact_verify
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
PACKET = ROOT / "resources/web/evand-square-packing-2026-10-05"
BATCH = PACKET / "square-packing/s12/search/exact/batch"
EXACT = BATCH.parent
CERTS = BATCH / "certs"
RECEIPTS = PACKET / "receipts"
FIRST_PARTY_RECEIPT = RECEIPTS / "first-party-check.json"
SOURCE_REPLAY_RECEIPT = RECEIPTS / "source-replay.json"
COMPARISON_RECEIPT = RECEIPTS / "register-comparison.json"
CONTROLS_RECEIPT = RECEIPTS / "negative-controls.json"
MANIFEST = PACKET / "acquisition/upstream-subtree.sha256"
UPSTREAM_CERTS = "s12/search/exact/batch/certs"
#: The reproduction sample: the smallest count, a squeezed input, de Winter's two
#: packings (one the source reports as a certified bound only) and the largest gap.
REPRODUCED = (68, 102, 126, 211, 270)
REPRODUCTION_RECEIPT = RECEIPTS / "reproduction-sample.json"
REPRODUCE_TIMEOUT = 3600
FRONTIER = ROOT / "frontier"
KNOWN_BEST = ROOT / "witnesses/known-best"

SOURCE = "https://github.com/evand/square-packing"
REVISION = "13ee36e5807727d12a5da36b9b90a96bdba272bf"
#: Held by the owner for the n = 17 work on other branches (think-x4v4).
HELD = frozenset({17})
#: The counts whose certified side lies below the register's, as issue #375 lists them.
IMPROVING = (
    68, 102, 103, 106, 110, 123, 126, 131, 132, 152, 154, 155, 156, 172, 177, 180, 181,
    182, 199, 206, 207, 208, 209, 210, 211, 228, 236, 237, 238, 239, 240, 241, 259, 263,
    268, 269, 270, 271, 272, 273, 297, 301, 302, 303, 304, 305, 306, 307,
)  # fmt: skip
#: The counts whose certificate, above the printed side, carries the verified upper lane
#: below the ceiling it held before (T-101): every count at which the
#: certified side rounded up at the printed precision lies below the record's earlier
#: verified upper bound. `devtools.apply_exact_ceilings survey` derives them from the
#: records and the receipts, and its `--check` holds this list to that derivation.
CEILINGS = (
    28, 37, 39, 41, 50, 51, 53, 54, 55, 69, 70, 71, 83, 87, 88, 101, 104, 107, 108, 109,
    122, 124, 125, 127, 128, 129, 145, 146, 147, 148, 149, 150, 151, 153, 170, 171, 173,
    174, 175, 176, 178, 179, 197, 198, 200, 201, 202, 203, 204, 205, 226, 227, 229, 230,
    231, 232, 233, 234, 235, 257, 258, 260, 261, 262, 264, 265, 266, 267, 290, 291, 293,
    294, 295, 296, 298, 299, 300,
)  # fmt: skip
#: The certificates the packet retains, each one cited by a case record.
RETAINED = tuple(sorted(IMPROVING + CEILINGS))
#: The ceiling counts' controls, made as the improving counts' are.
CEILING_CONTROLS_RECEIPT = RECEIPTS / "negative-controls-ceilings.json"
CONTROL_KINDS = (
    "tightest-pair-overlapped",
    "side-shrunk-past-clearance",
    "side-shrunk-one-unit",
)
#: How far the source's checkers may run per certificate before the replay calls it hung.
SOURCE_TIMEOUT = 600
FORMAT = "evand-exact-certificate-receipt-v1"
#: A square whose centre moved further than this, or whose rotation differs by more
#: radians, has moved beyond the binary64 slack of the witness it was solved from.
MOVED = 1e-8
#: The source's per-count numerical report, which lists each certificate's free squares.
RESULTS_JSON = BATCH / "results.json"

_RATIONAL = re.compile(r"-?\d+(?:/[1-9]\d*|\.\d+)?")
_COUNT = re.compile(r"[1-9]\d*")
_NAME = re.compile(r"n-([1-9]\d*)\.cert")


class CertificateError(ValueError):
    """A certificate this module refuses to read."""


@dataclass(frozen=True, slots=True)
class Pose:
    """One square: its exact centre and the exact tangent of half its rotation."""

    x: Fraction
    y: Fraction
    t: Fraction

    @property
    def basis(self) -> tuple[Fraction, Fraction]:
        """``(cos theta, sin theta)`` from ``t = tan(theta/2)``, exactly."""
        denominator = 1 + self.t * self.t
        return (1 - self.t * self.t) / denominator, 2 * self.t / denominator

    def corners(self) -> list[tuple[Fraction, Fraction]]:
        """The four corners, counter-clockwise: the centre plus the rotated half-diagonals."""
        c, s = self.basis
        half = Fraction(1, 2)
        return [
            (self.x + c * a - s * b, self.y + s * a + c * b)
            for a, b in ((half, half), (-half, half), (-half, -half), (half, -half))
        ]


@dataclass(frozen=True, slots=True)
class Certificate:
    n: int
    side: Fraction
    poses: tuple[Pose, ...]


def _rational(text: str, where: str) -> Fraction:
    """A literal the certificate format allows: an integer, ``p/q`` or a plain decimal.

    Python's `Fraction` also reads exponents, underscores and surrounding blanks, none of
    which the format names, so a literal is matched in full before it is converted.
    """
    if _RATIONAL.fullmatch(text) is None:
        raise CertificateError(f"{where}: {text!r} is not a rational literal")
    return Fraction(text)


def parse(text: str, *, expected_n: int | None = None) -> Certificate:
    """Read a certificate, refusing anything the format does not state.

    The header is ``n S``; then exactly ``n`` rows ``x y t``, and no further data rows.
    Lines that are blank or begin with ``#`` are comments. The source's checkers read the
    first ``n`` rows and ignore the rest; this reader refuses extra rows, so a certificate
    it accepts means the same thing to both.
    """
    rows = [
        line.split()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not rows or len(rows[0]) != 2 or _COUNT.fullmatch(rows[0][0]) is None:
        raise CertificateError("the header must be `n S` with n a positive integer")
    n = int(rows[0][0])
    if expected_n is not None and n != expected_n:
        raise CertificateError(f"the header says n = {n}, the file name says {expected_n}")
    side = _rational(rows[0][1], "side")
    if side <= 0:
        raise CertificateError("the side must be positive")
    body = rows[1:]
    if len(body) != n:
        raise CertificateError(f"{len(body)} square rows for n = {n}")
    poses: list[Pose] = []
    for index, row in enumerate(body, start=1):
        if len(row) != 3:
            raise CertificateError(f"square {index}: {len(row)} fields, not `x y t`")
        x, y, t = (_rational(value, f"square {index}") for value in row)
        poses.append(Pose(x, y, t))
    return Certificate(n, side, tuple(poses))


def literal(value: Fraction) -> str:
    """The witness format's rational literal."""
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def basis_witness(certificate: Certificate) -> dict[str, Any]:
    """The certificate as a rational ``center-basis`` Witness/v2, read by `exact_verify`."""
    return {
        "id": f"W-evand-exact-n{certificate.n:03d}",
        "n": certificate.n,
        "side": literal(certificate.side),
        "square_size": "1",
        "representation": "center-basis",
        "scalar": {"kind": "rational"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": [
            {
                "id": index,
                "center": [literal(pose.x), literal(pose.y)],
                "basis": [literal(value) for value in pose.basis],
            }
            for index, pose in enumerate(certificate.poses, start=1)
        ],
        "claim": {
            "coordinate_provenance": "reported",
            "method": "exact-algebraic",
            "limitations": (
                "Evan Daniel's rational certificate converted exactly; the conversion "
                "decides nothing, exact_verify does."
            ),
        },
    }


def corner_squares(certificate: Certificate) -> list[list[tuple[Fraction, Fraction]]]:
    """The certificate's squares as exact corners, for the independent checker."""
    return [pose.corners() for pose in certificate.poses]


def _float(value: Fraction | str) -> float:
    return float(Fraction(value))


def decide(certificate: Certificate) -> dict[str, Any]:
    """Both exact decisions of one certificate, with their least clearances."""
    started = time.process_time()
    result, _report = exact_verify(basis_witness(certificate))
    sqpack_seconds = time.process_time() - started
    started = time.process_time()
    second = independent.check_squares(corner_squares(certificate), certificate.side)
    independent_seconds = time.process_time() - started
    return {
        "n": certificate.n,
        "side": literal(certificate.side),
        "side_decimal": _decimal(certificate.side, 40),
        "exact_verify": {
            "passed": bool(result["verification_passed"]),
            "pairs_tested": result["pairs_tested"],
            "minimum_containment_clearance": _float(result["minimum_containment_clearance"]),
            "minimum_best_pair_gap": _float(result["minimum_best_pair_gap"]),
            "failures": [list(failure) for failure in result["failures"]],
            "cpu_seconds": round(sqpack_seconds, 3),
        },
        "independent": {
            "passed": bool(second["verification_passed"]),
            "pairs_tested": second["pairs_tested"],
            "minimum_containment_clearance": _float(second["minimum_containment_clearance"]),
            "minimum_best_pair_gap": _float(second["minimum_best_pair_gap"]),
            "failures": second["failures"],
            "cpu_seconds": round(independent_seconds, 3),
        },
    }


def _decimal(value: Fraction, digits: int, rounding: str = ROUND_FLOOR) -> str:
    """``value`` to ``digits`` significant digits, rounded in the stated direction."""
    with localcontext() as context:
        context.prec = digits
        context.rounding = rounding
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def ceiling_decimal(value: Fraction, places: int) -> str:
    """``value`` rounded up to ``places`` decimal places, as a plain decimal string."""
    scaled = math.ceil(value * 10**places)
    with localcontext() as context:
        context.prec = 200
        context.rounding = ROUND_CEILING
        return str(Decimal(scaled).scaleb(-places))


def terminating_decimal(value: Fraction) -> str | None:
    """``value`` written out in full when its decimal expansion ends, else None."""
    denominator = value.denominator
    twos = fives = 0
    while denominator % 2 == 0:
        denominator //= 2
        twos += 1
    while denominator % 5 == 0:
        denominator //= 5
        fives += 1
    if denominator != 1:
        return None
    places = max(twos, fives)
    scaled = value * 10**places
    with localcontext() as context:
        context.prec = 400
        return str(Decimal(scaled.numerator).scaleb(-places))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_decided(path: Path, n: int) -> bool:
    """Whether the certificate at ``path`` is, byte for byte, the one the first-party
    receipt decided at ``n``: the download boundary, a source's file against the digest
    this packet pinned and decided."""
    rows = json.loads(read_retained_text(FIRST_PARTY_RECEIPT))["rows"]
    decided = {int(row["n"]): str(row["sha256"]) for row in rows}
    return n in decided and sha256(path) == decided[n]


def certificate_path(directory: Path, n: int) -> Path:
    return directory / f"n-{n}.cert"


def certificate_counts(directory: Path) -> list[int]:
    """The counts a directory holds certificates for, the held ones left out."""
    counts: list[int] = []
    for path in directory.glob("n-*.cert"):
        match = _NAME.fullmatch(path.name)
        if match is None:
            raise CertificateError(f"unexpected certificate name {path.name}")
        n = int(match.group(1))
        if n not in HELD:
            counts.append(n)
    return sorted(counts)


def check_one(path_text: str) -> dict[str, Any]:
    path = Path(path_text)
    match = _NAME.fullmatch(path.name)
    if match is None:
        raise CertificateError(f"unexpected certificate name {path.name}")
    n = int(match.group(1))
    if n in HELD:
        raise CertificateError(f"n = {n} is held (think-x4v4) and is not read here")
    certificate = parse(path.read_text(encoding="utf-8"), expected_n=n)
    row = decide(certificate)
    row["sha256"] = sha256(path)
    return row


def _map(function: Callable[[str], dict[str, Any]], items: Sequence[str], workers: int):
    if workers <= 1:
        return [function(item) for item in items]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(function, items))


def _write_json(path: Path, value: object) -> None:
    """A receipt in the retained layout, a row to a line (`sqpack.retained_json`)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_text(retained_json.dumps(value, sort_keys=True), "utf-8")


def write_receipt(path: Path, value: object) -> None:
    """A receipt of another tool over this packet, in the same layout."""
    _write_json(path, value)


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.name


def run_check(directory: Path, counts: Iterable[int], workers: int) -> dict[str, Any]:
    paths = [str(certificate_path(directory, n)) for n in counts]
    started = time.monotonic()
    rows = _map(check_one, paths, workers)
    wall = time.monotonic() - started
    cpu = sum(
        row["exact_verify"]["cpu_seconds"] + row["independent"]["cpu_seconds"] for row in rows
    )
    return {
        "format": FORMAT,
        "tool": "python -m devtools.evand_exact_certificates check",
        "source": f"{SOURCE}/tree/{REVISION}/s12/search/exact/batch/certs",
        "read_from": (
            _relative(directory)
            if directory.resolve() == CERTS.resolve()
            else "a checkout of the source at the pinned revision"
        ),
        "held": sorted(HELD),
        "deciders": [
            "sqpack.witness.exact_verify",
            "devtools.check_rational_witness_independent",
        ],
        "workers": workers,
        "wall_seconds": round(wall, 1),
        "cpu_seconds": round(cpu, 1),
        "all_passed": all(
            row["exact_verify"]["passed"] and row["independent"]["passed"] for row in rows
        ),
        "rows": rows,
    }


def case_record(n: int) -> dict[str, Any]:
    """The `packing` payload of frontier case ``n``."""
    text = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    return safe_load(text.split("---\n", 2)[1])["packing"]


def _witness_poses(n: int) -> tuple[list[tuple[float, float, float]], str, str]:
    """The known-best witness's squares as ``(x, y, theta)`` about the lower-left corner,
    with its side and its source key."""
    document = safe_load((KNOWN_BEST / f"n-{n:03d}.yaml").read_text(encoding="utf-8"))
    witness = document["witness"]
    if witness["representation"] != "center-angle":
        raise CertificateError(f"n = {n}: the known-best witness is not center-angle")
    shift = (
        float(Fraction(witness["side"])) / 2
        if witness["coordinates"]["origin"] == "container-center"
        else 0.0
    )
    degrees = witness["coordinates"]["angle_unit"] == "degrees"
    poses = [
        (
            float(Fraction(square["center"][0])) + shift,
            float(Fraction(square["center"][1])) + shift,
            math.radians(float(Fraction(square["angle"])))
            if degrees
            else float(Fraction(square["angle"])),
        )
        for square in witness["squares"]
    ]
    return poses, str(witness["side"]), str(witness.get("source", {}).get("key", ""))


def round_up(value: float, digits: int = 4) -> float:
    """``value`` rounded up to ``digits`` significant digits, for a stated upper bound."""
    if value <= 0:
        return 0.0
    exponent = math.floor(math.log10(value)) - digits + 1
    scaled = math.ceil(Decimal(repr(value)).scaleb(-exponent))
    return float(Decimal(scaled).scaleb(exponent))


def _turn(left: float, right: float) -> float:
    """The least rotation taking one square's orientation to the other's, modulo 90 degrees."""
    quarter = math.pi / 2
    difference = (left - right) % quarter
    return min(difference, quarter - difference)


def pose_match(certificate: Certificate, free: Sequence[int] | None = None) -> dict[str, Any]:
    """How far the certificate's squares lie from the register's known-best witness.

    Each certificate square is matched to the witness square with the nearest centre; the
    match must be one to one. A square is *moved* when its centre is displaced by more
    than `MOVED` or its rotation differs by more than `MOVED` radians, modulo 90 degrees;
    the rest are the slack the source says it removes. Reported: the moved squares by
    their 0-based place in the certificate, those of them the source's report does not
    list as free (carrying no force, `free`), and the largest displacement and rotation
    difference over all squares, over the moved squares not listed free, and over the
    squares that did not move. Each is a list of scalars, so a receipt stays a row to a
    line. Binary64 is
    ample for differences far above 1e-16.
    """
    poses, side, source_key = _witness_poses(certificate.n)
    taken: set[int] = set()
    moved: dict[str, list[int]] = {"squares": [], "nonfree_squares": []}
    still_shift = still_turn = largest_shift = largest_turn = 0.0
    nonfree_shift = nonfree_turn = 0.0
    for place, pose in enumerate(certificate.poses):
        x, y = float(pose.x), float(pose.y)
        theta = 2 * math.atan(float(pose.t))
        index = min(range(len(poses)), key=lambda k: math.dist((x, y), poses[k][:2]))
        if index in taken:
            raise CertificateError(
                f"n = {certificate.n}: two squares match witness square {index + 1}"
            )
        taken.add(index)
        shift = math.dist((x, y), poses[index][:2])
        turn = _turn(theta, poses[index][2])
        largest_shift, largest_turn = max(largest_shift, shift), max(largest_turn, turn)
        if shift > MOVED or turn > MOVED:
            moved["squares"].append(place)
            if free is not None and place not in free:
                moved["nonfree_squares"].append(place)
                nonfree_shift, nonfree_turn = max(nonfree_shift, shift), max(nonfree_turn, turn)
        else:
            still_shift, still_turn = max(still_shift, shift), max(still_turn, turn)
    return {
        "witness": f"witnesses/known-best/n-{certificate.n:03d}.yaml",
        "witness_side": side,
        "witness_source_key": source_key,
        "matched_one_to_one": len(taken) == certificate.n,
        "moved": moved,
        "moved_count": len(moved["squares"]),
        "moved_listed_free": len(moved["squares"]) - len(moved["nonfree_squares"]),
        "largest_centre_displacement": round_up(largest_shift),
        "largest_rotation_difference_radians": round_up(largest_turn),
        "nonfree_moved_largest_centre_displacement": round_up(nonfree_shift),
        "nonfree_moved_largest_rotation_difference_radians": round_up(nonfree_turn),
        "unmoved_largest_centre_displacement": round_up(still_shift),
        "unmoved_largest_rotation_difference_radians": round_up(still_turn),
    }


@dataclass(frozen=True, slots=True)
class Earlier:
    """The bounds the register held at an improving count before this import."""

    side: str
    verified: str
    result: str | None
    source_key: str
    author: str


def earlier_holders() -> dict[int, Earlier]:
    """What each improving count's record held before this import, read from the sources
    that held it and not from the case records, which this import changes.

    Where a certified packet held the count, its latest one
    (`devtools.apply_upper_bound_packets.plans`), with the printed side and the verified
    value its receipt derives. Otherwise the count's side is the Kingbird catalogue's
    (n = 126, Joost de Winter's packing of 14 August 2026), and its verified ceiling was
    the integer grid.
    """
    from devtools.apply_upper_bound_packets import plans  # noqa: PLC0415 -- heavy import
    from devtools.check_source_coverage import parse_kingbird  # noqa: PLC0415

    held = {
        plan.n: Earlier(
            plan.side,
            plan.verified,
            plan.registration.result,
            plan.registration.source.key,
            plan.registration.author,
        )
        for plan in plans()
        if plan.n in IMPROVING
    }
    catalogue = parse_kingbird(ROOT / "resources/web/kingbird-squares-in-squares.html", 1, 324)
    for n in IMPROVING:
        if n not in held:
            held[n] = Earlier(
                catalogue[n], str(math.isqrt(n - 1) + 1), None, "[Kingbird]", "Joost de Winter"
            )
    return held


def reported_free(path: Path = RESULTS_JSON) -> dict[int, list[int]]:
    """The free squares the source's report lists for each count, 0-based."""
    from devtools.retained_data import read_retained_text  # noqa: PLC0415

    rows = json.loads(read_retained_text(path))
    return {int(row["n"]): list(row["free"]) for row in rows if row.get("free") is not None}


def compare_one(
    n: int, earlier: Earlier, directory: Path = CERTS, free: Sequence[int] | None = None
) -> dict[str, Any]:
    """One improving certificate against the bounds the register held and its witness."""
    certificate = parse(
        certificate_path(directory, n).read_text(encoding="utf-8"), expected_n=n
    )
    printed = Fraction(Decimal(earlier.side))
    verified = Fraction(Decimal(earlier.verified))
    return {
        "n": n,
        "certified_side": literal(certificate.side),
        "certified_side_decimal": _decimal(certificate.side, 40),
        "earlier_result": earlier.result,
        "earlier_source_key": earlier.source_key,
        "earlier_author": earlier.author,
        "earlier_printed_side": earlier.side,
        "earlier_verified_value": earlier.verified,
        "below_printed_side_by": float(f"{float(printed - certificate.side):.4e}"),
        "below_earlier_verified_by": float(f"{float(verified - certificate.side):.4e}"),
        "pose": pose_match(certificate, free),
    }


def run_compare(directory: Path = CERTS) -> dict[str, Any]:
    holders = earlier_holders()
    missing = sorted(set(IMPROVING) - set(holders))
    if missing:
        raise CertificateError(f"no earlier certified packet at n = {missing}")
    free = reported_free()
    rows = [compare_one(n, holders[n], directory, free.get(n)) for n in IMPROVING]
    poses = [row["pose"] for row in rows]
    below = [row["below_printed_side_by"] for row in rows]
    return {
        "format": FORMAT,
        "tool": "python -m devtools.evand_exact_certificates compare",
        "what": (
            "Each improving certificate's exact side against the printed side and the "
            "verified value of the certified packet the register held at that count before "
            "this import, and its pose against the register's known-best witness of that "
            "packet."
        ),
        "all_below_printed_side": all(value > 0 for value in below),
        "all_below_earlier_verified": all(row["below_earlier_verified_by"] > 0 for row in rows),
        "all_matched_one_to_one": all(row["pose"]["matched_one_to_one"] for row in rows),
        "least_below_printed_side": min(below),
        "most_below_printed_side": max(below),
        "largest_centre_displacement": max(
            row["pose"]["largest_centre_displacement"] for row in rows
        ),
        "largest_rotation_difference_radians": max(
            row["pose"]["largest_rotation_difference_radians"] for row in rows
        ),
        "moved_squares": sum(pose["moved_count"] for pose in poses),
        "moved_squares_listed_free": sum(pose["moved_listed_free"] for pose in poses),
        "nonfree_moved_largest_centre_displacement": max(
            pose["nonfree_moved_largest_centre_displacement"] for pose in poses
        ),
        "nonfree_moved_largest_rotation_difference_radians": max(
            pose["nonfree_moved_largest_rotation_difference_radians"] for pose in poses
        ),
        "unmoved_largest_centre_displacement": max(
            row["pose"]["unmoved_largest_centre_displacement"] for row in rows
        ),
        "unmoved_largest_rotation_difference_radians": max(
            row["pose"]["unmoved_largest_rotation_difference_radians"] for row in rows
        ),
        "rows": rows,
    }


def _children_cpu() -> float:
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    return usage.ru_utime + usage.ru_stime


def _run_checker(script: Path, certificate: Path) -> dict[str, Any]:
    """One run of one of the source's checkers, as a separate process."""
    before = _children_cpu()
    completed = subprocess.run(
        [sys.executable, str(script), str(certificate)],
        capture_output=True,
        text=True,
        timeout=SOURCE_TIMEOUT,
        check=False,
    )
    lines = [line.strip() for line in completed.stdout.strip().splitlines()]
    return {
        "exit_status": completed.returncode,
        "last_line": lines[-1] if lines else "",
        "output": lines[:-1][:4],
        "stderr": completed.stderr.strip()[-400:],
        "cpu_seconds": round(_children_cpu() - before, 3),
    }


def _source_one(job: tuple[str, str, str]) -> dict[str, Any]:
    checkers, directory, name = (Path(job[0]), Path(job[1]), job[2])
    match = _NAME.fullmatch(name)
    if match is None or int(match.group(1)) in HELD:
        raise CertificateError(f"{name} is not a certificate this replay reads")
    path = directory / name
    return {
        "n": int(match.group(1)),
        "sha256": sha256(path),
        "verify_cert": _run_checker(checkers / "verify_cert.py", path),
        "verify_cert2": _run_checker(checkers / "verify_cert2.py", path),
    }


def _source_passed(row: Mapping[str, Any]) -> bool:
    """Both checkers exited 0, and each printed its own word for a valid certificate.

    `verify_all.sh` takes ``grep -q VALID`` on verify_cert.py's last line, which also
    matches ``INVALID``; here each checker is held to its exit status and to a last line
    that begins with ``VALID``.
    """
    first, second = row["verify_cert"], row["verify_cert2"]
    return (
        first["exit_status"] == 0
        and first["last_line"].startswith("VALID: s(n) <=")
        and second["exit_status"] == 0
        and second["last_line"].startswith("VALID:")
    )


def run_source_replay(
    checkers: Path, directory: Path, counts: Iterable[int], workers: int
) -> dict[str, Any]:
    scripts = {name: sha256(checkers / name) for name in ("verify_cert.py", "verify_cert2.py")}
    jobs = [(str(checkers), str(directory), f"n-{n}.cert") for n in counts]
    started = time.monotonic()
    if workers <= 1:
        rows = [_source_one(job) for job in jobs]
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            rows = list(pool.map(_source_one, jobs))
    wall = time.monotonic() - started
    for row in rows:
        row["passed"] = _source_passed(row)
    return {
        "format": FORMAT,
        "tool": "python -m devtools.evand_exact_certificates source-replay",
        "source": f"{SOURCE}/tree/{REVISION}/s12/search/exact",
        "checkers": {
            "read_from": _relative(checkers),
            "sha256": scripts,
            "interpreter": f"CPython {sys.version.split()[0]}",
        },
        "read_from": (
            _relative(directory)
            if directory.resolve() == CERTS.resolve()
            else "a checkout of the source at the pinned revision"
        ),
        "held": sorted(HELD),
        "workers": workers,
        "wall_seconds": round(wall, 1),
        "cpu_seconds": round(
            sum(
                row["verify_cert"]["cpu_seconds"] + row["verify_cert2"]["cpu_seconds"]
                for row in rows
            ),
            1,
        ),
        "all_passed": all(row["passed"] for row in rows),
        "rows": rows,
    }


def serialize(certificate: Certificate) -> str:
    """A certificate in the source's format, for the source's own checkers."""
    rows = [f"{certificate.n} {literal(certificate.side)}"]
    rows.extend(
        f"{literal(pose.x)} {literal(pose.y)} {literal(pose.t)}" for pose in certificate.poses
    )
    return "\n".join(rows) + "\n"


def _axes(square: Sequence[tuple[Fraction, Fraction]]) -> list[tuple[Fraction, Fraction]]:
    return [
        (-(square[1][1] - square[0][1]), square[1][0] - square[0][0]),
        (-(square[2][1] - square[1][1]), square[2][0] - square[1][0]),
    ]


def _extent(
    square: Sequence[tuple[Fraction, Fraction]], axis: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    values = [x * axis[0] + y * axis[1] for x, y in square]
    return min(values), max(values)


def tightest_pair(
    certificate: Certificate,
) -> tuple[int, int, Fraction, tuple[Fraction, Fraction]]:
    """The pair with the least exact separating gap, and the direction that closes it.

    For each pair whose centres lie within the circumscribed discs' reach, the gap is the
    largest over the four face normals of the distance between the two projections
    (`devtools.check_rational_witness_independent.pair_gap`). Returned: the pair, its gap
    and the unit normal along which moving the second square by the gap closes it.
    """
    squares = corner_squares(certificate)
    best: tuple[int, int, Fraction, tuple[Fraction, Fraction]] | None = None
    for left in range(certificate.n):
        a = certificate.poses[left]
        for right in range(left + 1, certificate.n):
            b = certificate.poses[right]
            if (a.x - b.x) ** 2 + (a.y - b.y) ** 2 > 2:
                continue
            gap: Fraction | None = None
            direction: tuple[Fraction, Fraction] = (Fraction(0), Fraction(0))
            for axis in (*_axes(squares[left]), *_axes(squares[right])):
                left_lo, left_hi = _extent(squares[left], axis)
                right_lo, right_hi = _extent(squares[right], axis)
                for value, sign in ((right_lo - left_hi, -1), (left_lo - right_hi, 1)):
                    if gap is None or value > gap:
                        gap, direction = value, (sign * axis[0], sign * axis[1])
            if gap is not None and (best is None or gap < best[2]):
                best = (left, right, gap, direction)
    if best is None:
        raise CertificateError("no pair lies close enough to touch")
    return best


def _moved(certificate: Certificate, index: int, dx: Fraction, dy: Fraction) -> Certificate:
    poses = list(certificate.poses)
    pose = poses[index]
    poses[index] = Pose(pose.x + dx, pose.y + dy, pose.t)
    return Certificate(certificate.n, certificate.side, tuple(poses))


def overlap_control(certificate: Certificate) -> tuple[Certificate, dict[str, Any]]:
    """Move one square of the tightest pair along the pair's best separating face axis by
    that axis's gap plus one unit of the side's denominator, doubling the excess until the
    pair overlaps. The overlap is judged by the independent checker's own pair gap, so its
    refusal of the mutant is circular; the mutant is invalid regardless, since its squares
    have rational unit edge normals and a negative gap on every face axis means, by the
    separating-axis theorem, that their interiors meet."""
    left, right, gap, (nx, ny) = tightest_pair(certificate)
    unit = Fraction(1, certificate.side.denominator)
    excess = unit
    for _ in range(200):
        step = gap + excess
        moved = _moved(certificate, right, step * nx, step * ny)
        squares = corner_squares(moved)
        if independent.pair_gap(squares[left], squares[right]) < 0:
            return moved, {
                "control": "tightest-pair-overlapped",
                "squares": [left, right],
                "exact_gap": float(gap),
                "moved_by_gap_plus": float(excess),
                "unit": float(unit),
                "moved_square_wall_clearance": float(
                    min(
                        clearance
                        for x, y in squares[right]
                        for clearance in (x, y, moved.side - x, moved.side - y)
                    )
                ),
            }
        excess *= 2
    raise CertificateError(f"n = {certificate.n}: no small move overlaps the tightest pair")


def top_clearance(certificate: Certificate) -> Fraction:
    """The least exact distance from a corner to the box's top or right side."""
    return min(
        certificate.side - coordinate
        for square in corner_squares(certificate)
        for point in square
        for coordinate in point
    )


def shrink_controls(certificate: Certificate) -> list[tuple[Certificate, dict[str, Any]]]:
    """The box shrunk past its least top or right clearance by one unit of the side's
    denominator, which must be refused, and by that one unit alone, which is a valid
    certificate wherever the clearance exceeds the unit."""
    unit = Fraction(1, certificate.side.denominator)
    clearance = top_clearance(certificate)
    past = Certificate(certificate.n, certificate.side - clearance - unit, certificate.poses)
    one = Certificate(certificate.n, certificate.side - unit, certificate.poses)
    return [
        (
            past,
            {
                "control": "side-shrunk-past-clearance",
                "clearance": float(clearance),
                "unit": float(unit),
                "expect": "refused",
            },
        ),
        (
            one,
            {
                "control": "side-shrunk-one-unit",
                "clearance": float(clearance),
                "unit": float(unit),
                "expect": "accepted" if clearance > unit else "refused",
            },
        ),
    ]


def _all_checkers(certificate: Certificate, checkers: Path, scratch: Path) -> dict[str, bool]:
    """Each checker's verdict on one certificate: this repository's two and the source's."""
    path = scratch / f"n-{certificate.n}.cert"
    path.write_text(serialize(certificate), encoding="utf-8")
    first, _ = exact_verify(basis_witness(certificate))
    second = independent.check_squares(corner_squares(certificate), certificate.side)
    source = {
        "verify_cert": _run_checker(checkers / "verify_cert.py", path),
        "verify_cert2": _run_checker(checkers / "verify_cert2.py", path),
    }
    return {
        "exact_verify": bool(first["verification_passed"]),
        "independent": bool(second["verification_passed"]),
        "verify_cert": source["verify_cert"]["exit_status"] == 0,
        "verify_cert2": source["verify_cert2"]["exit_status"] == 0,
        "verify_cert_last_line": source["verify_cert"]["last_line"],
    }


def _controls_one(job: tuple[str, str, int]) -> list[dict[str, Any]]:
    import tempfile  # noqa: PLC0415

    checkers, directory, n = Path(job[0]), Path(job[1]), job[2]
    certificate = parse(
        certificate_path(directory, n).read_text(encoding="utf-8"), expected_n=n
    )
    rows: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory() as scratch:
        mutants = [overlap_control(certificate), *shrink_controls(certificate)]
        for mutant, row in mutants:
            row.setdefault("expect", "refused")
            verdicts = _all_checkers(mutant, checkers, Path(scratch))
            accepted = [
                name
                for name in ("exact_verify", "independent", "verify_cert", "verify_cert2")
                if verdicts[name]
            ]
            row.update(
                {
                    "n": n,
                    "sha256": hashlib.sha256(serialize(mutant).encode()).hexdigest(),
                    "verdicts": verdicts,
                    "as_expected": (
                        not accepted if row["expect"] == "refused" else len(accepted) == 4
                    ),
                }
            )
            rows.append(row)
    return rows


def verify_all_vacuity(checkers: Path, mutant: Certificate) -> dict[str, Any]:
    """Run the source's `verify_all.sh`, as retained, on one refused certificate.

    The script calls ``python3``; a directory holding a ``python3`` link to this
    project's interpreter goes first on its ``PATH``. Its first leg pipes
    verify_cert.py's last line to ``grep -q VALID``, which ``INVALID`` also matches, so
    only its second leg can report the failure.
    """
    import os  # noqa: PLC0415
    import shutil  # noqa: PLC0415
    import tempfile  # noqa: PLC0415

    with tempfile.TemporaryDirectory() as scratch:
        root = Path(scratch)
        (root / "bin").mkdir()
        (root / "bin/python3").symlink_to(sys.executable)
        exact = root / "exact"
        (exact / "batch/certs").mkdir(parents=True)
        for name in ("verify_cert.py", "verify_cert2.py"):
            shutil.copyfile(checkers / name, exact / name)
        shutil.copyfile(checkers / "batch/verify_all.sh", exact / "batch/verify_all.sh")
        (exact / f"batch/certs/n-{mutant.n}.cert").write_text(serialize(mutant), "utf-8")
        completed = subprocess.run(
            ["bash", str(exact / "batch/verify_all.sh")],
            capture_output=True,
            text=True,
            timeout=SOURCE_TIMEOUT,
            check=False,
            env={**os.environ, "PATH": f"{root / 'bin'}:{os.environ.get('PATH', '')}"},
        )
    lines = completed.stdout.strip().splitlines()
    return {
        "script": "s12/search/exact/batch/verify_all.sh",
        "sha256": sha256(checkers / "batch/verify_all.sh"),
        "certificate_sha256": hashlib.sha256(serialize(mutant).encode()).hexdigest(),
        "exit_status": completed.returncode,
        "output": [line.replace(scratch, "<scratch>") for line in lines],
        "first_leg_reported_the_failure": any("verify_cert FAIL" in line for line in lines),
        "second_leg_reported_the_failure": any("verify_cert2 FAIL" in line for line in lines),
    }


def annotate_controls(path: Path = CONTROLS_RECEIPT) -> dict[str, Any]:
    """Add each overlap control's moved-square wall clearance to a committed receipt.

    The control is regenerated from its retained certificate, which is deterministic, and
    must have the digest the receipt recorded; nothing is decided again. Where the moved
    square stays strictly inside the box, every checker's refusal can only be for a pair,
    since the original certificate passed and only that square moved.
    """
    receipt = json.loads(read_retained_text(path))
    for row in receipt["rows"]:
        if row["control"] != "tightest-pair-overlapped":
            continue
        n = int(row["n"])
        certificate = parse(
            certificate_path(CERTS, n).read_text(encoding="utf-8"), expected_n=n
        )
        mutant, fresh = overlap_control(certificate)
        if hashlib.sha256(serialize(mutant).encode()).hexdigest() != row["sha256"]:
            raise CertificateError(f"n = {n}: the overlap control does not regenerate")
        row["moved_square_wall_clearance"] = fresh["moved_square_wall_clearance"]
    overlaps = [row for row in receipt["rows"] if row["control"] == "tightest-pair-overlapped"]
    receipt["overlap_controls_inside_the_box"] = all(
        row["moved_square_wall_clearance"] > 0 for row in overlaps
    )
    return receipt


def run_controls(
    checkers: Path, directory: Path, workers: int, counts: Sequence[int] = IMPROVING
) -> dict[str, Any]:
    """Three controls at each of ``counts``, the improving counts unless told otherwise.

    A receipt for other counts lists them and the workers that ran them. It records no CPU
    time: the pool's workers are the forkserver's children, not this process's, so
    ``RUSAGE_CHILDREN`` here does not see them (the first ceiling run recorded 0.2 s that
    way, and that field was taken out of its receipt).
    """
    held = sorted(set(counts) & HELD)
    if held:
        raise CertificateError(f"n = {held} is held (think-x4v4)")
    jobs = [(str(checkers), str(directory), n) for n in counts]
    started = time.monotonic()
    if workers <= 1:
        groups = [_controls_one(job) for job in jobs]
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            groups = list(pool.map(_controls_one, jobs))
    rows = [row for group in groups for row in group]
    smallest = parse(certificate_path(directory, min(counts)).read_text("utf-8"))
    vacuity = verify_all_vacuity(checkers, overlap_control(smallest)[0])
    improving = tuple(counts) == IMPROVING
    which = "improving certificate" if improving else "certificate this receipt lists"
    extra: dict[str, Any] = {} if improving else {"counts": list(counts), "workers": workers}
    return {
        "format": FORMAT,
        "tool": "python -m devtools.evand_exact_certificates controls",
        **extra,
        "what": (
            f"Three altered copies of each {which}, decided by this "
            "repository's two exact checkers and by the source's two, as retained: the "
            "tightest pair overlapped by moving one square along its closing normal by the "
            "exact gap plus one unit of the side's denominator (doubled until it overlaps), "
            "and the box shrunk past its least top or right clearance by that unit, both of "
            "which every checker must refuse; and the box shrunk by the unit alone, which "
            "is still a valid certificate where the clearance exceeds it."
        ),
        "wall_seconds": round(time.monotonic() - started, 1),
        "all_as_expected": all(row["as_expected"] for row in rows),
        "overlap_controls_inside_the_box": all(
            row["moved_square_wall_clearance"] > 0
            for row in rows
            if row["control"] == "tightest-pair-overlapped"
        ),
        "verify_all_vacuity": vacuity,
        "rows": rows,
    }


def manifest_digests() -> dict[str, str]:
    """The packet's subtree manifest, upstream path to SHA-256."""
    digests: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, _, name = line.partition("  ")
        digests[name.removeprefix("./")] = digest
    return digests


def _reproduce_one(job: tuple[str, int]) -> dict[str, Any]:
    """Solve one pinned input again with the source's retained solver, and compare."""
    import os  # noqa: PLC0415
    import tempfile  # noqa: PLC0415

    inputs, n = Path(job[0]), job[1]
    if n in HELD:
        raise CertificateError(f"n = {n} is held (think-x4v4)")
    source = inputs / f"n-{n}.txt"
    pinned = manifest_digests()[f"s12/search/exact/batch/inputs/n-{n}.txt"]
    if sha256(source) != pinned:
        raise CertificateError(f"n = {n}: the input is not the one the packet pins")
    with tempfile.TemporaryDirectory() as scratch:
        before = _children_cpu()
        started = time.monotonic()
        completed = subprocess.run(
            [sys.executable, str(EXACT / "exactsolve.py"), str(source), "--out", scratch, "-q"],
            capture_output=True,
            text=True,
            timeout=REPRODUCE_TIMEOUT,
            check=False,
            env={**os.environ, "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1"},
        )
        produced = Path(scratch) / f"n-{n}.cert"
        retained = certificate_path(CERTS, n)
        row: dict[str, Any] = {
            "n": n,
            "input_sha256": pinned,
            "exit_status": completed.returncode,
            "cpu_seconds": round(_children_cpu() - before, 1),
            "wall_seconds": round(time.monotonic() - started, 1),
            "produced": produced.is_file(),
        }
        if produced.is_file():
            row["byte_identical"] = produced.read_bytes() == retained.read_bytes()
            row["produced_sha256"] = sha256(produced)
            ours = parse(produced.read_text(encoding="utf-8"), expected_n=n)
            theirs = parse(retained.read_text(encoding="utf-8"), expected_n=n)
            row["same_side"] = ours.side == theirs.side
            row["squares_differing"] = sum(
                mine != kept for mine, kept in zip(ours.poses, theirs.poses, strict=True)
            )
            row["largest_tangent_difference"] = float(
                f"{
                    max(
                        (
                            float(abs(mine.t - kept.t))
                            for mine, kept in zip(ours.poses, theirs.poses, strict=True)
                        ),
                        default=0.0,
                    ):.3e}"
            )
            row["largest_coordinate_difference"] = float(
                f"{
                    max(
                        (
                            float(max(abs(mine.x - kept.x), abs(mine.y - kept.y)))
                            for mine, kept in zip(ours.poses, theirs.poses, strict=True)
                        ),
                        default=0.0,
                    ):.3e}"
            )
            decided = decide(ours)
            row["produced_decided_valid"] = (
                decided["exact_verify"]["passed"] and decided["independent"]["passed"]
            )
    return row


def run_reproduce(inputs: Path, counts: Sequence[int], workers: int) -> dict[str, Any]:
    jobs = [(str(inputs), n) for n in counts]
    if workers <= 1:
        rows = [_reproduce_one(job) for job in jobs]
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            rows = list(pool.map(_reproduce_one, jobs))
    import numpy as np  # noqa: PLC0415
    import scipy  # noqa: PLC0415

    return {
        "format": FORMAT,
        "tool": "python -m devtools.evand_exact_certificates reproduce",
        "what": (
            "The source's solver, exactsolve.py as retained, run here on the pinned input "
            "of each sampled count with one BLAS thread, and its certificate compared with "
            "the retained one byte for byte, as the source's reproduce.sh does; where the "
            "bytes differ, the sides and the squares are compared, and the regenerated "
            "certificate is decided by this repository's two exact checkers."
        ),
        "environment": {
            "interpreter": f"CPython {sys.version.split()[0]}",
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "solver_sha256": sha256(EXACT / "exactsolve.py"),
        "workers": workers,
        "cpu_seconds": round(sum(row["cpu_seconds"] for row in rows), 1),
        "rows": rows,
    }


def manifest_certificates() -> dict[int, str]:
    """The SHA-256 the packet's subtree manifest pins for each certificate, by count."""
    pinned: dict[int, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, _, name = line.partition("  ")
        directory, _, file = name.removeprefix("./").rpartition("/")
        match = _NAME.fullmatch(file)
        if directory == UPSTREAM_CERTS and match is not None:
            pinned[int(match.group(1))] = digest
    return pinned


def receipt_problems() -> list[str]:
    """Every committed receipt against the packet: fast, offline, deciding nothing again.

    Each replay receipt must cover every certificate the manifest pins, at its pinned
    digest, and pass; the retained certificates must be the 48 improving counts and the 77
    ceiling counts, each with its row's digest and side; the comparison must cover the 48
    at their certified sides; and every control, three at each of the 125, must have come
    out as expected.
    """
    problems: list[str] = []
    pinned = manifest_certificates()
    if set(pinned) & HELD:
        problems.append(f"the manifest pins a held count: {sorted(set(pinned) & HELD)}")
    retained = {n: certificate_path(CERTS, n) for n in certificate_counts(CERTS)}
    if tuple(sorted(retained)) != RETAINED:
        problems.append("the retained certificates are not the improving and ceiling counts")
    for path, label in (
        (FIRST_PARTY_RECEIPT, "first-party check"),
        (SOURCE_REPLAY_RECEIPT, "source replay"),
    ):
        receipt = json.loads(path.read_text(encoding="utf-8"))
        rows = {int(row["n"]): row for row in receipt["rows"]}
        if not receipt["all_passed"]:
            problems.append(f"{label}: not every certificate passed")
        if set(rows) != set(pinned):
            problems.append(f"{label}: rows differ from the pinned certificates")
        problems.extend(
            f"{label} n={n}: digest is not the pinned one"
            for n, row in rows.items()
            if pinned.get(n) != row["sha256"]
        )
        for n, file in retained.items():
            row = rows.get(n)
            if row is None or sha256(file) != row["sha256"]:
                problems.append(
                    f"{label} n={n}: the retained certificate is not the one decided"
                )
    first = json.loads(FIRST_PARTY_RECEIPT.read_text(encoding="utf-8"))
    for row in first["rows"]:
        if row["n"] in retained:
            side = parse(
                retained[row["n"]].read_text(encoding="utf-8"), expected_n=row["n"]
            ).side
            if literal(side) != row["side"]:
                problems.append(
                    f"first-party check n={row['n']}: side differs from the certificate"
                )
    comparison = json.loads(COMPARISON_RECEIPT.read_text(encoding="utf-8"))
    compared = {int(row["n"]): row for row in comparison["rows"]}
    if sorted(compared) != sorted(IMPROVING):
        problems.append("comparison: rows are not the 48 improving counts")
    if not (comparison["all_below_printed_side"] and comparison["all_matched_one_to_one"]):
        problems.append(
            "comparison: a side is not below its printed side or a pose did not match"
        )
    for n, row in compared.items():
        if n in retained:
            side = parse(retained[n].read_text(encoding="utf-8"), expected_n=n).side
            if literal(side) != row["certified_side"]:
                problems.append(f"comparison n={n}: side differs from the certificate")
    for path, counts, label in (
        (CONTROLS_RECEIPT, IMPROVING, "controls"),
        (CEILING_CONTROLS_RECEIPT, CEILINGS, "ceiling controls"),
    ):
        controls = json.loads(path.read_text(encoding="utf-8"))
        if not (controls["all_as_expected"] and controls["overlap_controls_inside_the_box"]):
            problems.append(f"{label}: not every control came out as expected")
        kinds = {(int(row["n"]), row["control"]) for row in controls["rows"]}
        if kinds != {(n, kind) for n in counts for kind in CONTROL_KINDS}:
            problems.append(f"{label}: rows are not three controls at each of its counts")
        for row in controls["rows"]:
            if int(row["n"]) in retained and int(row["n"]) in counts:
                continue
            problems.append(f"{label} n={row['n']}: the controlled certificate is not retained")
    return problems


def table() -> str:
    """The packet README's table of the 48 counts, from the committed receipts."""
    from devtools.generate_frontier_case import display_first_party_upper  # noqa: PLC0415

    statuses = {
        int(row["n"]): str(row.get("status"))
        for row in json.loads(read_retained_text(RESULTS_JSON))
    }
    header = (
        "| n | Finder | Printed side | Certified side `S'` | Below by | Source's report "
        "| Moved squares |"
    )
    lines = [header, "| --- | --- | --- | --- | --- | --- | --- |"]
    comparison = json.loads(read_retained_text(COMPARISON_RECEIPT))
    for row in comparison["rows"]:
        n, pose = int(row["n"]), row["pose"]
        side = parse(certificate_path(CERTS, n).read_text(encoding="utf-8"), expected_n=n).side
        held = row["earlier_result"] or "catalogue"
        count, free = pose["moved_count"], pose["moved_listed_free"]
        moved = f"{count} ({free} free)" if count else "0"
        lines.append(
            f"| {n} | {row['earlier_author']} ({held}) | `{row['earlier_printed_side']}` "
            f"| `{display_first_party_upper(terminating_decimal(side) or literal(side))}` "
            f"| `{row['below_printed_side_by']:.2e}` | {statuses.get(n)} | {moved} |"
        )
    return "\n".join(lines) + "\n"


def _command_check(args: argparse.Namespace) -> int:
    if args.check:
        problems = receipt_problems()
        for problem in problems:
            print(f"FAIL {problem}", file=sys.stderr)
        if not problems:
            print(
                f"receipts agree with the packet: {len(manifest_certificates())} pinned "
                f"certificates, {len(RETAINED)} retained, held {sorted(HELD)}"
            )
        return 1 if problems else 0
    counts = args.n or certificate_counts(args.certs)
    held = sorted(set(counts) & HELD)
    if held:
        print(f"n = {held} is held (think-x4v4)", file=sys.stderr)
        return 2
    receipt = run_check(args.certs, counts, args.workers)
    if args.receipt:
        _write_json(args.receipt, receipt)
    for row in receipt["rows"]:
        seconds = row["exact_verify"]["cpu_seconds"] + row["independent"]["cpu_seconds"]
        print(
            f"n={row['n']}: exact_verify "
            f"{'VALID' if row['exact_verify']['passed'] else 'INVALID'}, independent "
            f"{'VALID' if row['independent']['passed'] else 'INVALID'}, {seconds:.1f}s"
        )
    print(
        f"{len(receipt['rows'])} certificates, all passed: {receipt['all_passed']}, "
        f"{receipt['cpu_seconds']} CPU seconds"
    )
    return 0 if receipt["all_passed"] else 1


def _command_source_replay(args: argparse.Namespace) -> int:
    counts = certificate_counts(args.certs)
    receipt = run_source_replay(args.checkers, args.certs, counts, args.workers)
    if args.receipt:
        _write_json(args.receipt, receipt)
    failed = [row["n"] for row in receipt["rows"] if not row["passed"]]
    print(
        f"{len(receipt['rows'])} certificates, both source checkers accept "
        f"{len(receipt['rows']) - len(failed)}; refused {failed}; "
        f"{receipt['cpu_seconds']} CPU seconds, {receipt['wall_seconds']} s wall"
    )
    return 0 if receipt["all_passed"] else 1


def _command_compare(args: argparse.Namespace) -> int:
    receipt = run_compare()
    _write_json(args.receipt, receipt)
    for row in receipt["rows"]:
        holder = row["earlier_result"] or row["earlier_source_key"]
        pose = row["pose"]
        print(
            f"n={row['n']}: {row['below_printed_side_by']:.3e} below {holder}'s printed "
            f"side, pose within {pose['largest_centre_displacement']:.1e} and "
            f"{pose['largest_rotation_difference_radians']:.1e} rad"
        )
    print(
        f"all below the printed side: {receipt['all_below_printed_side']}, by "
        f"{receipt['least_below_printed_side']:.2e} to "
        f"{receipt['most_below_printed_side']:.2e}; matched one to one: "
        f"{receipt['all_matched_one_to_one']}"
    )
    return 0


def _command_reproduce(args: argparse.Namespace) -> int:
    receipt = run_reproduce(args.inputs, args.n or REPRODUCED, args.workers)
    _write_json(args.receipt, receipt)
    for row in receipt["rows"]:
        print(
            f"n={row['n']}: exit {row['exit_status']}, byte-identical "
            f"{row.get('byte_identical')}, {row['cpu_seconds']} CPU s"
        )
    return 0


def _command_controls(args: argparse.Namespace) -> int:
    receipt = annotate_controls(args.receipt or CONTROLS_RECEIPT) if args.annotate else None
    if receipt is not None:
        _write_json(args.receipt or CONTROLS_RECEIPT, receipt)
        print(f"overlap controls inside the box: {receipt['overlap_controls_inside_the_box']}")
        return 0 if receipt["overlap_controls_inside_the_box"] else 1
    counts = CEILINGS if args.ceilings else IMPROVING
    path = args.receipt or (CEILING_CONTROLS_RECEIPT if args.ceilings else CONTROLS_RECEIPT)
    receipt = run_controls(EXACT, args.certs, args.workers, counts)
    _write_json(path, receipt)
    unexpected = [
        (row["n"], row["control"]) for row in receipt["rows"] if not row["as_expected"]
    ]
    vacuity = receipt["verify_all_vacuity"]
    print(
        f"{len(receipt['rows'])} controls, all as expected: {receipt['all_as_expected']}; "
        f"unexpected {unexpected}; verify_all.sh first leg reported the failure: "
        f"{vacuity['first_leg_reported_the_failure']}, second leg: "
        f"{vacuity['second_leg_reported_the_failure']}"
    )
    return 0 if receipt["all_as_expected"] else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check")
    check.add_argument("--certs", type=Path, default=CERTS)
    check.add_argument("--n", type=int, nargs="*")
    check.add_argument("--workers", type=int, default=1)
    check.add_argument("--receipt", type=Path)
    check.add_argument(
        "--check",
        action="store_true",
        help="hold the committed receipts to the packet without deciding anything again",
    )
    check.set_defaults(run=_command_check)
    replay = commands.add_parser("source-replay")
    replay.add_argument("--checkers", type=Path, default=EXACT)
    replay.add_argument("--certs", type=Path, default=CERTS)
    replay.add_argument("--workers", type=int, default=1)
    replay.add_argument("--receipt", type=Path)
    replay.set_defaults(run=_command_source_replay)
    compare = commands.add_parser("compare")
    compare.add_argument("--receipt", type=Path, default=COMPARISON_RECEIPT)
    compare.set_defaults(run=_command_compare)
    reproduce = commands.add_parser("reproduce")
    reproduce.add_argument("--inputs", type=Path, required=True)
    reproduce.add_argument("--n", type=int, nargs="*")
    reproduce.add_argument("--workers", type=int, default=1)
    reproduce.add_argument("--receipt", type=Path, default=REPRODUCTION_RECEIPT)
    reproduce.set_defaults(run=_command_reproduce)
    commands.add_parser("table").set_defaults(run=lambda _args: print(table(), end="") or 0)
    controls = commands.add_parser("controls")
    controls.add_argument("--workers", type=int, default=1)
    controls.add_argument("--certs", type=Path, default=CERTS)
    controls.add_argument(
        "--ceilings",
        action="store_true",
        help="control the ceiling counts' certificates (T-101), not the improving ones",
    )
    controls.add_argument("--receipt", type=Path)
    controls.add_argument(
        "--annotate",
        action="store_true",
        help="add the overlap controls' wall clearances to the committed receipt",
    )
    controls.set_defaults(run=_command_controls)
    args = parser.parse_args(argv)
    return int(args.run(args))


if __name__ == "__main__":
    raise SystemExit(main())
