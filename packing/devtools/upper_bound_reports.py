"""Import a report of rational upper-bound certificates by another author, from its packet.

Every upper-bound import since #432 wrote its own report module around the same steps.
This module does them for any packet under ``packing/resources/web/`` that carries an
import declaration, ``acquisition/report.json`` (`Declaration`), beside the custody
declaration ``devtools.acquire_source`` writes the packet from:

- **custody.** ``read_facts`` admits nothing until ``acquire_source.check`` passes, so
  every certificate it reads is a retained file bound to its upstream blob. Where the
  source states no licence and the packet retains no upstream byte, a row names a derived
  ``fact`` instead: the certificate as an exact rational Witness/v2, which ``derive``
  writes from a checkout once ``acquire_source.acquire`` shows the checkout yields this
  packet's own acquisition record, so its bytes have the digests the packet pins. The
  fact names those digests, and ``read_facts`` holds it to its own rebuild. A pinned file
  the row names as stating the same packing, such as the source's own Witness/v2, is
  compared with the certificate by ``derive``, from the same checkout. Where the source
  keeps its geometry in release assets and pins them by digest in a manifest of its tree,
  as PR #574 does, a row names the asset member (`ArchiveMember`), and ``derive`` reads it
  from a local copy of the asset that has the manifest's size and digest;
- **format.** Each certificate is read by the adapter its row names (`ADAPTERS`) into the
  kernel's exact centre/half-angle certificate, with centres in ``[0, S]^2``;
- **admission.** A certificate is admitted only where its exact side equals, or rounds up
  to, the side the issue prints, at the places it prints; a certificate of the release that
  the issue does not name is held to the side its source prints (``printed_in``);
- **comparison.** ``compare`` rebuilds ``acquisition/claims.json``: each certificate of the
  release against the case record's ceiling as the declaration read it, rebuilt from the
  holding source's own packet (`HOUSES`), and against every other pending report at that
  count, exactly where its side is retained and by its printed decimals otherwise. A count
  beyond the ``n <= 324`` horizon has no case record and is compared with the grid; a
  requested one is also written to ``acquisition/beyond-horizon-claims.json``, the record
  ``check_source_coverage`` reads a beyond-horizon row against;
- **replay.** ``certify`` runs a positive, a duplicate-square and an outside-container job
  for every count of the declared ``replayed`` roster, each in its own child process,
  through the two exact routes of ``devtools.evand_arrangement_reports``, and writes
  ``receipts/exact-certification.json.xz``, or one ``receipts/exact-certification-nNNN.json.xz``
  per count where the whole would exceed the kernel's ceiling on uncompressed evidence;
  ``check`` admits the receipt, and ``check --replay`` decides it again;
- **registration.** ``register-plan`` prints, and writes nowhere, the register, evidence,
  coverage, bibliography and resources entries the ``requested`` counts need. A release
  whose requested counts all lie beyond the horizon, as #584's do, plans no register
  entry, only its evidence, its source row and its beyond-horizon rows. A
  certificate the issue does not name is an import of its own (``result-import.md``, stage
  1), compared here and registered by none of these entries.

No source program runs. A finite construction certifies an upper bound and nothing more:
no KKT, local-minimum, rigidity, novelty or optimality statement is replayed here.

From ``packing/``, with the project interpreter::

    python -m devtools.upper_bound_reports PACKET derive --checkout CHECKOUT [--check] \\
        [--assets DIR]
    python -m devtools.upper_bound_reports PACKET check-claims [--write]
    python -m devtools.upper_bound_reports PACKET certify --jobs-dir SCRATCH/jobs --workers 2
    python -m devtools.upper_bound_reports PACKET check [--n N ...] [--replay]
    python -m devtools.upper_bound_reports PACKET register-plan

**Adding a format.** An adapter is a function ``(raw, n, options) -> Certificate`` (the
`Adapter` type) that reads one retained file's bytes for count ``n`` and returns the
exact certificate, centres in ``[0, S]^2`` and ``t = tan(theta/2)``. ``options`` is the
row's declared ``options`` as a mapping of strings, and an adapter refuses any it does not
read. Add it to `ADAPTERS` under a new name and declare that name as a row's ``format``;
nothing else changes. `decimal_dilation`, the reader of #470's decimal poses, is such an
adapter: it takes its dilation and its rounding of each half-angle tangent as options,
and the side it returns, like any other, is admitted only if it rounds up to the side the
report prints.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import io
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
import zlib
from collections.abc import Callable, Collection, Mapping
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from fractions import Fraction
from pathlib import Path, PurePosixPath
from typing import Any, NamedTuple, NotRequired, TypedDict, cast

import mpmath as mp
import yaml
from mpmath.libmp import to_rational
from strif import atomic_output_file

from devtools import acquire_source, retained_data
from devtools import check_source_coverage as coverage_check
from devtools import couzo_followup_reports as couzo_followup
from devtools import couzo_refinement_reports as couzo_451
from devtools import decimal_pose_margins as decimal_poses
from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools import evand_hunt_reports as evand_hunt
from devtools import gupta_refinement_reports as gupta
from devtools import refinement_packets as rehwaldt
from devtools import register_regularized_bounds as regularized
from devtools import ryxu_arrangement_reports as ryxu
from devtools import squish_followup_packets as squish_update
from devtools import squish_second_update_packets as squish_second
from devtools import squish_upper_bound_packets as squish_first
from devtools.retained_data import read_retained_bytes
from sqpack.witness import (
    WitnessError,
    validate_witness_document,
    witness_document,
    witness_envelope,
)
from sqpack.yamlio import load_yaml, safe_load

MODULE = "devtools.upper_bound_reports"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
WEB = ROOT / "resources/web"
DECLARATION = Path("acquisition/report.json")
CLAIMS = Path("acquisition/claims.json")
BEYOND = Path("acquisition/beyond-horizon-claims.json")
RECEIPT = Path("receipts/exact-certification.json.xz")


def shard(n: int) -> Path:
    """The receipt of one count, where the roster's receipt would exceed the ceiling."""
    return Path(f"receipts/exact-certification-n{n:03d}.json.xz")


FACTS = "facts"
#: The witness schema, as a fact under ``packing/resources/web/PACKET/facts/`` names it.
FACT_SCHEMA = "../../../../witnesses/witness.schema.yaml"
WITNESS_SCHEMA = ROOT / "witnesses/witness.schema.yaml"
DECLARATION_FORMAT = "upper-bound-report-declaration-v1"
CLAIMS_FORMAT = "upper-bound-report-claims-v1"
BEYOND_FORMAT = "upper-bound-beyond-horizon-claims-v1"
#: The case corpus is ``n = 1..324``; a count above it has no case record.
HORIZON = 324
DISPLAY_PLACES = 16
#: A terminating side with more places than this is stated as a fraction in a claim.
CLAIM_PLACES = 40
JOBS = kernel.JOBS
ROUTES = kernel.ROUTES
JOB_TIMEOUT = kernel.JOB_TIMEOUT
MAX_WORKERS = 2
#: The largest file an adapter reads. #567's n261 release pins a 1,076,936-byte certificate
#: and a 4,842,525-byte corners witness of the same packing.
MAX_SOURCE_BYTES = 6_000_000
#: The longest rational literal an adapter reads, the longest a receipt row may state:
#: that witness has corner literals of 2,522 characters, and PR #574's n146 witness has
#: rotation literals of 6,023 characters.
MAX_LITERAL_CHARS = kernel.MAX_RATIONAL_CHARS
#: The longest integer part a literal may have: Python's default limit on converting
#: between integers and decimal strings, which every writer downstream shares (the
#: kernel's `to_witness` and `_rational`, and any printed side), so a literal past it is
#: refused when it is read rather than failing where it is written. The longest integer
#: part any retained packet states, in PR #574's n146 receipt, has 3,011 digits.
MAX_INTEGER_DIGITS = kernel.MAX_INTEGER_DIGITS
#: How a printed side was rounded: up, as the report states; not stated; or ``binary64``,
#: a decimal rendering of the IEEE double nearest the side, as #593 prints its sides at 16
#: places, whose last places a double of that size does not determine (`printed_span`).
ROUNDINGS = ("up", "unstated", "binary64")
THIS = "this certificate"
_PRINTED = re.compile(r"[0-9]+\.[0-9]+")
_FRACTION = re.compile(r"[1-9][0-9]*/[1-9][0-9]*")
_LITERAL = re.compile(r"-?[0-9]+(?:/[1-9][0-9]*)?")
_DATE = re.compile(r"\d{4}-\d\d-\d\d")
_UTC = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d(:\d\d)?Z")
_COMMIT = re.compile(r"[0-9a-f]{40}")
_PACKET = re.compile(r"[a-z0-9][a-z0-9.-]*-\d{4}-\d\d-\d\d")


class ReportError(kernel.ReportError):
    """Refuse incomplete custody, an unadmitted certificate, a changed claim or receipt."""


# --------------------------------------------------------------------------- the contract


class Option(TypedDict):
    """One option an adapter reads, by name; every value is a string."""

    name: str
    value: str


class ArchiveMember(TypedDict):
    """A file inside a release asset that a pinned manifest binds, not a file of the tree.

    PR #574 keeps its geometry outside Git: its pinned commit adds HostedData manifests
    (``packing.squares:HostedData/v1``) that name each release asset of the source's
    repository by size and SHA-256, and the certificates are members of those zip assets.

    - ``manifest``: the pinned upstream path of the HostedData manifest.
    - ``repository``, ``tag``: the release the manifest names, which it must state.
    - ``asset``: the asset's file name, one of the manifest's ``objects``.
    - ``member``: the file's path inside the zip asset.
    - ``sha256``: the member's SHA-256, which a derived fact names as its digest.
    """

    manifest: str
    repository: str
    tag: str
    asset: str
    member: str
    sha256: str


class SamePacking(TypedDict):
    """Another file of the same count, which must state the identical packing.

    Beside a retained certificate it is a retained file, compared whenever the
    certificate is read. Beside a derived fact it is a file the packet pins and does not
    retain, so ``derive`` compares it, from the same checkout, when it writes or checks
    the fact. Beside a fact read from a release asset it may be another asset's member
    (``archive``), compared by ``derive`` from the same assets directory.
    """

    path: str
    format: str
    archive: NotRequired[ArchiveMember]


class CertificateRow(TypedDict):
    """One certificate the issue reports.

    - ``path``: its upstream path under the packet's archived directory.
    - ``format``: the adapter that reads it (`ADAPTERS`).
    - ``offered``: the side the issue prints, as printed: decimals, which the exact side
      must equal or round up to there, or an exact fraction, which it must equal.
    - ``printed_in`` (optional): where ``offered`` is printed, for a certificate the issue
      does not name; its source's own table.
    - ``first_committed``: the UTC time of the first commit holding these bytes, which
      dates the claim (``attribution.published``).
    - ``options`` (optional): what the adapter reads besides the bytes.
    - ``same_packing`` (optional): other retained files that state the same packing.
    - ``fact`` (optional): the packet-relative derived fact, ``facts/n-NNN.yaml``, read in
      place of ``path`` where no upstream byte is retained (``derive``).
    - ``archive`` (optional, with ``fact``): where ``path`` is a member of a release asset
      that a pinned manifest binds rather than a file of the pinned tree (`ArchiveMember`);
      ``path`` is then the member's path.
    """

    n: int
    path: str
    format: str
    offered: str
    first_committed: str
    printed_in: NotRequired[str]
    options: NotRequired[list[Option]]
    same_packing: NotRequired[list[SamePacking]]
    fact: NotRequired[str]
    archive: NotRequired[ArchiveMember]


class House(TypedDict):
    """The case record's upper bound at an in-horizon count, as it stood when read.

    - ``reader``: the `HOUSES` key that rebuilds its exact side from its own packet.
    - ``source_key``, ``holders``, ``result`` (optional): its source key, its credit as
      the case prints it, and the register entry that holds it.
    - ``reported_value``, ``verified_value``: the two lanes' values as printed.
    - ``evidence``: the verified lane's evidence.
    - ``reported_rounding`` (optional): where the reported lane is another source's print
      and not the house's side, how it was rounded (`ROUNDINGS`); it is compared as a
      printed side. A catalogue print below a rational ceiling is such a lane.
    """

    n: int
    reader: str
    source_key: str
    holders: str
    result: NotRequired[str]
    reported_value: str
    verified_value: str
    evidence: list[str]
    reported_rounding: NotRequired[str]


class Pending(TypedDict):
    """Another report at the same count that no case record holds.

    Either ``reader`` names the retained packet whose exact side it is, for a register
    entry pending adoption, or ``printed`` is the side it prints, with ``rounding``
    (`ROUNDINGS`).
    """

    n: int
    report: str
    url: str
    holders: str
    result: NotRequired[str]
    reader: NotRequired[str]
    printed: NotRequired[str]
    rounding: NotRequired[str]


class Bibliography(TypedDict):
    """The source's bibliography entry, read from its own attribution files."""

    authors: list[str]
    lineage: str
    credit: str
    short_credit: str
    note: str


class Register(TypedDict):
    """The prose a register plan cannot derive: the source's own words and the next step."""

    title: str
    headline: str
    significance: int
    source_checks: str
    credit: str
    next_rung: str
    bead: str
    bibliography: Bibliography


class Declaration(TypedDict):
    """``acquisition/report.json``: what the import is, written by the importing lane.

    ``certificates`` is every certificate of the release, ``requested`` the counts the
    issue reports and ``replayed`` the counts the receipt covers.
    """

    format: str
    issue: str
    author: str
    source_key: str
    report_evidence: str
    receipt_format: str
    witness_prefix: str
    claim_limitations: str
    read_on: str
    read_at_main: str
    certificates: list[CertificateRow]
    requested: list[int]
    replayed: list[int]
    houses: list[House]
    pending: list[Pending]
    register: Register


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ReportError(message)


def ensure_private(path: Path) -> None:
    if path.is_symlink() or not path.resolve().is_relative_to(REPO.resolve()):
        raise ReportError(f"{path}: retained evidence must be a private repository file")


def packet_path(name: str) -> Path:
    _require(_PACKET.fullmatch(name), f"not a dated packet name: {name!r}")
    return WEB / name


def _profile(declaration: Declaration) -> dict[str, str]:
    return {
        "witness_prefix": declaration["witness_prefix"],
        "claim_limitations": declaration["claim_limitations"],
    }


_ASSET = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_REPOSITORY = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9._-]+")
_TAG = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/-]*")
_SHA256 = re.compile(r"[0-9a-f]{64}")


def _plain_path(path: str) -> bool:
    relative = PurePosixPath(path)
    return (
        bool(path)
        and not relative.is_absolute()
        and ".." not in relative.parts
        and relative.as_posix() == path
    )


def archive_spec(spec: ArchiveMember, path: str, where: str) -> None:
    """Refuse a release-asset member that is not named plainly and bound by a digest."""
    _require(spec["member"] == path, f"{where}: the row's path is not its asset member")
    _require(
        _plain_path(spec["member"])
        and _plain_path(spec["manifest"])
        and _ASSET.fullmatch(spec["asset"])
        and _REPOSITORY.fullmatch(spec["repository"])
        and _TAG.fullmatch(spec["tag"])
        and ".." not in spec["tag"]
        and _SHA256.fullmatch(spec["sha256"]),
        f"{where}: a release-asset member names its manifest, release, asset, path and digest",
    )


def load_declaration(packet: Path) -> Declaration:
    """The packet's import declaration, refused unless every part of it is well formed."""
    ensure_private(packet / DECLARATION)
    value: object = json.loads(
        (packet / DECLARATION).read_text(encoding="utf-8"),
        object_pairs_hook=kernel.unique_object,
    )
    # The custody contract's shape check reads any TypedDict; its signature names its own.
    shape: Any = Declaration
    problems = acquire_source.shape_problems(value, shape, DECLARATION.as_posix())
    _require(not problems, "; ".join(problems))
    declaration = cast("Declaration", value)
    _require(declaration["format"] == DECLARATION_FORMAT, "unknown import declaration format")
    _require(_DATE.fullmatch(declaration["read_on"]), "read_on is not a date")
    _require(_COMMIT.fullmatch(declaration["read_at_main"]), "read_at_main is not a commit")
    counts = [row["n"] for row in declaration["certificates"]]
    _require(counts and counts == sorted(set(counts)), "counts must be unique and ascending")
    for roster in ("requested", "replayed"):
        chosen = declaration[roster]
        _require(
            chosen and chosen == sorted(set(chosen)) and not set(chosen) - set(counts),
            f"{roster} must be ascending, unique declared counts",
        )
    # A declaration may request only counts beyond the horizon, as #584 does: the register
    # plan then has no in-horizon side to register and plans beyond-horizon rows alone.
    for row in declaration["certificates"]:
        _require(row["format"] in ADAPTERS, f"n={row['n']}: unknown format {row['format']}")
        _require(
            _PRINTED.fullmatch(row["offered"])
            or (_FRACTION.fullmatch(row["offered"]) and row["n"] <= HORIZON),
            f"n={row['n']}: offered side is no plain decimal or, in the corpus, fraction",
        )
        if "fact" in row:
            fact = PurePosixPath(row["fact"])
            _require(
                fact.parent.as_posix() == FACTS and fact.name == f"n-{row['n']:03d}.yaml",
                f"n={row['n']}: a derived fact is facts/n-NNN.yaml",
            )
        if "archive" in row:
            _require("fact" in row, f"n={row['n']}: a release-asset certificate is a fact")
            archive_spec(row["archive"], row["path"], f"n={row['n']}")
        _require(_UTC.fullmatch(row["first_committed"]), f"n={row['n']}: first_committed")
        for other in row.get("same_packing", []):
            _require(other["format"] in ADAPTERS, f"n={row['n']}: unknown format")
            if "archive" in other:
                _require("archive" in row, f"n={row['n']}: an asset member beside a tree file")
                archive_spec(other["archive"], other["path"], f"n={row['n']} same packing")
    _require(
        [house["n"] for house in declaration["houses"]] == [n for n in counts if n <= HORIZON],
        "the houses must be exactly the in-horizon counts, in order",
    )
    for house in declaration["houses"]:
        _require(house["reader"] in HOUSES, f"n={house['n']}: no reader {house['reader']}")
        _require(
            house.get("reported_rounding", "up") in ROUNDINGS,
            f"n={house['n']}: unknown reported rounding",
        )
    labels = [(pending["n"], pending["report"]) for pending in declaration["pending"]]
    _require(len(labels) == len(set(labels)), "a pending report is named twice at one count")
    for pending in declaration["pending"]:
        where = f"n={pending['n']} {pending['report']}"
        _require(pending["n"] in counts, f"{where}: a pending report at an undeclared count")
        if "reader" in pending:
            _require(
                pending["reader"] in HOUSES and not {"printed", "rounding"} & set(pending),
                f"{where}: a known reader, and no printed side beside it",
            )
        else:
            _require(
                _PRINTED.fullmatch(pending.get("printed", ""))
                and pending.get("rounding") in ROUNDINGS,
                f"{where}: a printed side and its rounding",
            )
    # The kernel holds a witness prefix and limitations to its profile when it builds a
    # witness, so building one square's refuses a bad profile before any job runs.
    kernel.to_witness(
        legacy.Certificate(
            1, Fraction(2), (legacy.Pose(Fraction(1), Fraction(1), Fraction(0)),)
        ),
        **_profile(declaration),
    )
    return declaration


def acquisition(packet: Path) -> acquire_source.Source:
    """The packet's one acquisition record, after its custody check."""
    if problems := acquire_source.check(packet, REPO):
        raise ReportError("packet custody: " + "; ".join(problems))
    record = json.loads((packet / acquire_source.RECORD).read_text(encoding="utf-8"))
    return cast("acquire_source.Source", record["sources"][0])


# --------------------------------------------------------------------------- adapters

type Adapter = Callable[[bytes, int, Mapping[str, str]], legacy.Certificate]


def _no_options(options: Mapping[str, str], name: str) -> None:
    _require(not options, f"{name} reads no options: {sorted(options)}")


def _text(raw: bytes) -> str:
    _require(len(raw) <= MAX_SOURCE_BYTES, "certificate exceeds its byte ceiling")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ReportError("certificate is not UTF-8") from error


def _literal(value: object, where: str) -> Fraction:
    """A rational the JSON formats allow: a string integer or ``p/q``, never a number."""
    if (
        type(value) is not str
        or len(value) > MAX_LITERAL_CHARS
        or _LITERAL.fullmatch(value) is None
    ):
        raise ReportError(f"{where}: not a bounded rational string")
    _require(
        kernel.integer_parts_bounded(value),
        f"{where}: an integer part longer than {MAX_INTEGER_DIGITS} digits",
    )
    return Fraction(value)


def _json(raw: bytes) -> Any:
    try:
        return json.loads(_text(raw), object_pairs_hook=kernel.unique_object)
    except (json.JSONDecodeError, kernel.ReportError) as error:
        raise ReportError(f"invalid certificate JSON: {error}") from error


def _certificate(
    n: int, side: Fraction, rows: list[tuple[Fraction, Fraction, Fraction]]
) -> legacy.Certificate:
    _require(side > 0, f"n={n}: the side must be positive")
    _require(len(rows) == n, f"{len(rows)} squares for n = {n}")
    return legacy.Certificate(n, side, tuple(legacy.Pose(x, y, t) for x, y, t in rows))


def _squares(value: Any, n: int) -> list[Any]:
    _require(type(value) is dict, f"n={n}: a certificate must be a JSON object")
    _require(type(value.get("n")) is int and value["n"] == n, f"n={n}: count differs")
    _require(type(value.get("squares")) is list, f"n={n}: squares must be a list")
    return value["squares"]


def evand_cert(raw: bytes, n: int, options: Mapping[str, str]) -> legacy.Certificate:
    """Evan Daniel's text format: ``n S``, then ``x y t`` per square, centres in [0, S]^2."""
    _no_options(options, "evand-cert")
    try:
        return legacy.parse(_text(raw), expected_n=n)
    except legacy.CertificateError as error:
        raise ReportError(f"n={n}: {error}") from error


def _triples(squares: list[Any], n: int) -> list[tuple[Fraction, Fraction, Fraction]]:
    """Each square's ``[x, y, t]`` row of rational strings."""
    rows = []
    for index, square in enumerate(squares, start=1):
        _require(type(square) is list and len(square) == 3, f"n={n} square {index}: x y t")
        x, y, t = (_literal(item, f"n={n} square {index}") for item in square)
        rows.append((x, y, t))
    return rows


def squish_json(raw: bytes, n: int, options: Mapping[str, str]) -> legacy.Certificate:
    """SQUISH's JSON: ``s_exact`` and ``squares`` as ``[x, y, t]`` strings in [0, S]^2.

    ``s_decimal`` and ``note`` are the source's display and prose, read and not believed;
    ``phase`` and ``squeezed`` are its optional search metadata.
    """
    _no_options(options, "squish-json")
    value = _json(raw)
    squares = _squares(value, n)
    required = {"n", "s_exact", "s_decimal", "note", "squares"}
    _require(
        required <= set(value) <= required | {"phase", "squeezed"}
        and type(value["s_decimal"]) is str
        and type(value["note"]) is str,
        f"n={n}: SQUISH certificate has missing, unknown or mistyped fields",
    )
    return _certificate(n, _literal(value["s_exact"], f"n={n} side"), _triples(squares, n))


#: The fields PingYou's JSON may add to its side and squares, with the JSON types allowed.
PINGYOU_METADATA: dict[str, tuple[type, ...]] = {
    "note": (str,),
    "dilation_exact": (str,),
    "raw_side": (int, float),
    "provenance": (dict,),
    # PR #574's construction records at n = 50, 171 and 230: the source's account of how
    # the poses were made, which the exact routes do not read.
    "construction": (str,),
    "source_ids": (list,),
    "rules": (list,),
    "reflection_center": (list,),
    "boundary_word": (dict,),
    "registration": (list,),
}


def pingyou_json(raw: bytes, n: int, options: Mapping[str, str]) -> legacy.Certificate:
    """PingYou Ltd's JSON (#503, #504, #564, #566-#569): ``s_exact`` and ``[x, y, t]`` squares.

    The rows are SQUISH's. ``note``, ``dilation_exact``, ``raw_side`` and ``provenance``
    are the source's prose, its guard dilation, its undilated floating-point side and its
    construction record, read and not believed: the side is ``s_exact``, and only the
    exact routes decide whether the poses pack.
    """
    _no_options(options, "pingyou-json")
    value = _json(raw)
    squares = _squares(value, n)
    required = {"n", "s_exact", "squares"}
    _require(
        required <= set(value) <= required | set(PINGYOU_METADATA)
        and all(
            type(value[key]) in kinds for key, kinds in PINGYOU_METADATA.items() if key in value
        ),
        f"n={n}: PingYou certificate has missing, unknown or mistyped fields",
    )
    return _certificate(n, _literal(value["s_exact"], f"n={n} side"), _triples(squares, n))


#: The only frame and the only schema name a corner witness may state for `witness_corners`.
CORNER_FRAME = {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "not-applicable"}
CORNER_SCHEMA = "witness.schema.yaml"
#: Corners as ``sqpack.witness`` materializes a centre and basis, in half-diagonal units.
CORNER_ORDER = ((-1, -1), (1, -1), (1, 1), (-1, 1))


def pose_corners(pose: legacy.Pose) -> list[tuple[Fraction, Fraction]]:
    """A pose's four corners, counter-clockwise from the corner at its frame's (-1/2, -1/2)."""
    c, s = pose.basis
    return [
        (pose.x + (a * c - b * s) / 2, pose.y + (a * s + b * c) / 2) for a, b in CORNER_ORDER
    ]


def witness_corners(raw: bytes, n: int, options: Mapping[str, str]) -> legacy.Certificate:
    """A rational ``corners`` Witness/v2, read back exactly to centres and half-angles.

    The document must name the witness schema by its file name, which is read from this
    repository, pass it and its semantic checks, state ``n`` unit squares numbered 1 to
    ``n`` in order in the lower-left frame, and list each square's corners in the order
    `pose_corners` writes them. A pose is recovered as the corners' mean and
    ``t = s / (1 + c)`` from the first edge ``(c, s)``, and the four corners must be
    exactly that pose's, which holds only for a unit square in that order. Corners listed
    from another vertex draw the same square at another ``t``, and a comparison of poses
    reads them as another packing.
    """
    _no_options(options, "witness-corners")
    try:
        document = load_yaml(_text(raw))
    except yaml.YAMLError as error:
        raise ReportError(f"n={n}: invalid witness YAML: {error}") from error
    metadata = document.get("softschema") if type(document) is dict else None
    _require(
        type(metadata) is dict and metadata.get("schema") == CORNER_SCHEMA,
        f"n={n}: a corner witness names {CORNER_SCHEMA} as its schema",
    )
    try:
        witness = validate_witness_document(
            document, path=WITNESS_SCHEMA, fallback_schema=WITNESS_SCHEMA
        )
    except WitnessError as error:
        raise ReportError(f"n={n}: not a valid witness: {error}") from error
    _require(
        witness["n"] == n
        and witness["representation"] == "corners"
        and witness["scalar"] == {"kind": "rational"}
        and witness["square_size"] == "1"
        and witness["coordinates"] == CORNER_FRAME,
        f"n={n}: not a rational corner witness of {n} unit squares in the lower-left frame",
    )
    rows = []
    for index, square in enumerate(witness["squares"], start=1):
        where = f"n={n} square {index}"
        _require(square["id"] == index, f"{where}: squares are not numbered 1..n in order")
        corners = [(_literal(x, where), _literal(y, where)) for x, y in square["corners"]]
        c, s = corners[1][0] - corners[0][0], corners[1][1] - corners[0][1]
        _require(c != -1, f"{where}: no finite half-angle")
        x = sum((x for x, _ in corners), Fraction(0)) / 4
        y = sum((y for _, y in corners), Fraction(0)) / 4
        pose = legacy.Pose(x, y, s / (1 + c))
        _require(
            pose_corners(pose) == corners,
            f"{where}: the corners are not a unit square's in the order pose_corners writes",
        )
        rows.append((pose.x, pose.y, pose.t))
    return _certificate(n, _literal(witness["side"], f"n={n} side"), rows)


def witness_center_basis(raw: bytes, n: int, options: Mapping[str, str]) -> legacy.Certificate:
    """A rational ``center-basis`` Witness/v2 (PR #574's n146 and n261), read exactly.

    The document is held to this repository's witness schema and semantic checks whatever
    schema path it names, since a packet's upstream file is read where it was found and
    the path it names is the source's. It must state ``n`` unit squares with distinct ids
    in the lower-left frame. Each pose is the centre and ``t = s / (1 + c)`` from the basis
    ``(c, s)``, and the basis must be exactly the rotation that ``t`` gives, which holds only
    where ``c^2 + s^2 = 1``.
    """
    _no_options(options, "witness-center-basis")
    try:
        document = load_yaml(_text(raw))
    except yaml.YAMLError as error:
        raise ReportError(f"n={n}: invalid witness YAML: {error}") from error
    metadata = document.get("softschema") if type(document) is dict else None
    _require(type(metadata) is dict, f"n={n}: not a witness document")
    fields = cast("dict[str, Any]", document)
    try:
        witness = validate_witness_document(
            {
                **fields,
                "softschema": {**cast("dict[str, Any]", metadata), "schema": CORNER_SCHEMA},
            },
            path=WITNESS_SCHEMA,
            fallback_schema=WITNESS_SCHEMA,
        )
    except WitnessError as error:
        raise ReportError(f"n={n}: not a valid witness: {error}") from error
    _require(
        witness["n"] == n
        and witness["representation"] == "center-basis"
        and witness["scalar"] == {"kind": "rational"}
        and witness["square_size"] == "1"
        and witness["coordinates"] == CORNER_FRAME,
        f"n={n}: not a rational centre-basis witness of {n} unit squares in the lower-left "
        "frame",
    )
    ids = [square["id"] for square in witness["squares"]]
    _require(len(ids) == len(set(ids)) == n, f"n={n}: square ids are not {n} distinct ids")
    rows = []
    for index, square in enumerate(witness["squares"], start=1):
        where = f"n={n} square {index}"
        x, y = (_literal(value, where) for value in square["center"])
        c, s = (_literal(value, where) for value in square["basis"])
        _require(c != -1, f"{where}: no finite half-angle")
        pose = legacy.Pose(x, y, s / (1 + c))
        _require(pose.basis == (c, s), f"{where}: the basis is no rotation")
        rows.append((pose.x, pose.y, pose.t))
    return _certificate(n, _literal(witness["side"], f"n={n} side"), rows)


def centred_json(raw: bytes, n: int, options: Mapping[str, str]) -> legacy.Certificate:
    """Centred JSON (#483): ``side`` and ``{x, y, t}`` squares in [-S/2, S/2]^2.

    Each centre is translated by ``S/2``, exactly, into the kernel's [0, S]^2.
    ``schema``, ``parent_side`` and ``dilation`` are the source's labels, read and not
    believed.
    """
    _no_options(options, "centred-json")
    value = _json(raw)
    squares = _squares(value, n)
    required = {"schema", "n", "coordinate_system", "side", "squares"}
    _require(
        required <= set(value) <= required | {"parent_side", "dilation"}
        and value["coordinate_system"] == "centered"
        and all(
            type(value.get(key, "")) is str for key in ("schema", "parent_side", "dilation")
        ),
        f"n={n}: not a centred certificate with only the known fields",
    )
    side = _literal(value["side"], f"n={n} side")
    rows = []
    for index, square in enumerate(squares, start=1):
        _require(
            type(square) is dict and set(square) == {"x", "y", "t"},
            f"n={n} square {index}: exactly x, y and t",
        )
        x, y, t = (_literal(square[key], f"n={n} square {index}") for key in ("x", "y", "t"))
        rows.append((x + side / 2, y + side / 2, t))
    return _certificate(n, side, rows)


def sqcert(raw: bytes, n: int, options: Mapping[str, str]) -> legacy.Certificate:
    """Daniil Ostashev's ``.sqcert`` (#501): ``n N``, ``s S``, then ``x y t`` per square.

    As in Evan Daniel's format, centres lie in [0, S]^2 and ``t = tan(theta/2)``, and blank
    lines and lines that begin with ``#`` are comments, so the ``# claimed_s`` and
    ``# delta`` headers are the source's labels, read and not believed. The source's own
    reader also takes ``n`` and ``s`` in either order and decimals beside ``p/q``; this one
    takes the order and the integer and ``p/q`` literals every retained file uses, and
    refuses the rest.
    """
    _no_options(options, "sqcert")
    rows = [
        line.split()
        for line in _text(raw).splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    _require(
        len(rows) >= 2
        and len(rows[0]) == 2
        and rows[0][0] == "n"
        and re.fullmatch(r"[1-9][0-9]*", rows[0][1]) is not None
        and int(rows[0][1]) == n,
        f"n={n}: the first data line must be `n {n}`",
    )
    _require(
        len(rows[1]) == 2 and rows[1][0] == "s", f"n={n}: the second data line must be `s S`"
    )
    poses = []
    for index, row in enumerate(rows[2:], start=1):
        _require(len(row) == 3, f"n={n} square {index}: {len(row)} fields, not `x y t`")
        x, y, t = (_literal(value, f"n={n} square {index}") for value in row)
        poses.append((x, y, t))
    return _certificate(n, _literal(rows[1][1], f"n={n} side"), poses)


#: The two options `decimal_dilation` reads, and the bounds on the places it rounds at.
DILATION = "dilation"
HALF_ANGLE_PLACES = "half_angle_places"
MIN_HALF_ANGLE_PLACES = 30
MAX_HALF_ANGLE_PLACES = 100
#: Working digits beyond the rounding place, tried in turn until an enclosure decides it.
GUARD_DIGITS = (20, 60, 200)
#: The angles, reduced to [-180, 180) degrees, whose half-angle tangent is rational.
EXACT_TANGENTS = {
    Fraction(0): Fraction(0),
    Fraction(90): Fraction(1),
    Fraction(-90): Fraction(-1),
}
_POSITIVE = re.compile(r"[1-9][0-9]*(?:/[1-9][0-9]*)?")
_PLACES = re.compile(r"[1-9][0-9]{0,2}")


def _exact_endpoint(value: Any) -> Fraction | None:
    """An enclosure's endpoint as the exact dyadic it is, or None where it is infinite."""
    number = mp.mpf(value)
    if not mp.isfinite(number):
        return None
    numerator, denominator = to_rational(number._mpf_)
    return Fraction(int(numerator), int(denominator))


def half_angle_tangent(degrees: Fraction, places: int) -> Fraction:
    """``tan(theta/2)`` for an angle in degrees, rounded down at ``places`` decimals.

    The angle is reduced exactly to [-180, 180). There the tangent is rational only at
    0 and +-90 degrees, where it is 0 or +-1 and is returned exactly; at every other
    rational angle it is irrational, so an outward-rounded enclosure narrow enough puts
    both its endpoints on one side of every rounding point, and the working precision
    rises until it does. The floor is therefore proved, whatever precision decided it,
    and a floor no enclosure decides is refused. At 180 degrees no finite tangent exists.
    """
    turn = (degrees + 180) % 360 - 180
    _require(turn != -180, f"an angle of {degrees} degrees has no finite half-angle tangent")
    if turn in EXACT_TANGENTS:
        return EXACT_TANGENTS[turn]
    return _tangent_floor(
        lambda: decimal_poses.enclose(turn) * mp.iv.pi / 360,
        places,
        f"tan({degrees}/2 degrees)",
    )


def half_angle_tangent_radians(radians: Fraction, places: int) -> Fraction:
    """``tan(theta/2)`` for an angle in radians, rounded down at ``places`` decimals.

    At 0 the tangent is 0, returned exactly. At every other rational angle it is
    irrational (the tangent of a nonzero algebraic number is transcendental), so, as in
    `half_angle_tangent`, an outward-rounded enclosure narrow enough decides the floor and
    the working precision rises until it does; a floor no enclosure decides is refused,
    as is an enclosure that meets a pole of the tangent.
    """
    if radians == 0:
        return Fraction(0)
    return _tangent_floor(
        lambda: decimal_poses.enclose(radians) / 2, places, f"tan({radians}/2 radians)"
    )


def _tangent_floor(half_angle: Callable[[], Any], places: int, label: str) -> Fraction:
    """The tangent of an enclosed half-angle, rounded down at ``places``, once decided.

    ``half_angle`` builds the enclosure at the working precision it is called under.
    """
    scale = 10**places
    for guard in GUARD_DIGITS:
        with decimal_poses.working_precision(places + guard):
            enclosure = mp.iv.tan(half_angle())
            low, high = (_exact_endpoint(end) for end in (enclosure.a, enclosure.b))
        if low is not None and high is not None:
            floor = math.floor(low * scale)
            if floor == math.floor(high * scale):
                return Fraction(floor, scale)
    raise ReportError(f"no enclosure decides {label} at {places} places")


def _dilation_options(options: Mapping[str, str]) -> tuple[Fraction, int]:
    _require(
        set(options) == {DILATION, HALF_ANGLE_PLACES},
        f"decimal-dilation reads exactly {DILATION} and {HALF_ANGLE_PLACES}, not "
        f"{sorted(options)}",
    )
    value, places = options[DILATION], options[HALF_ANGLE_PLACES]
    _require(
        len(value) <= MAX_LITERAL_CHARS
        and _POSITIVE.fullmatch(value)
        and kernel.integer_parts_bounded(value),
        f"{DILATION} is no positive integer or p/q: {value[:80]!r}",
    )
    dilation = Fraction(value)
    _require(dilation >= 1, f"a {DILATION} moves centres apart; {value} is below 1")
    _require(
        _PLACES.fullmatch(places)
        and MIN_HALF_ANGLE_PLACES <= int(places) <= MAX_HALF_ANGLE_PLACES,
        f"{HALF_ANGLE_PLACES} is an integer from {MIN_HALF_ANGLE_PLACES} to "
        f"{MAX_HALF_ANGLE_PLACES}, not {places[:80]!r}",
    )
    return dilation, int(places)


def decimal_dilation(raw: bytes, n: int, options: Mapping[str, str]) -> legacy.Certificate:
    """David Ellsworth's decimal centre-angle text (#470), made exact by a declared dilation.

    The file states ``s: SIDE``, then ``Square K: x=X, y=Y, deg=D`` for ``K = 1..n`` in
    order, in the box ``[-s/2, s/2]^2`` (`devtools.decimal_pose_margins.parse_pose` reads
    it). Its digits are rounded, so it is no exact certificate. Two declared options make
    one, and nothing else is read:

    - ``dilation``, a rational ``p/q >= 1``: every centre is scaled by it about the box
      centre, and the side is ``dilation * s``;
    - ``half_angle_places``, an integer from 30 to 100: each square's
      ``t = tan(theta/2)`` is the exact tangent rounded down at that many decimals
      (`half_angle_tangent`).

    The centres are then translated by half the side into ``[0, S]^2``. Like any other,
    the side is admitted only where it rounds up to the side the report prints, and only
    the exact routes decide whether the result packs.
    """
    dilation, places = _dilation_options(options)
    try:
        pose = decimal_poses.parse_pose(_text(raw))
    except decimal_poses.PoseError as error:
        raise ReportError(f"n={n}: {error}") from error
    labels = [square.label for square in pose.squares]
    _require(labels == list(range(1, len(labels) + 1)), f"n={n}: squares are not 1..n in order")
    side = dilation * pose.side
    half = side / 2
    rows = [
        (
            dilation * square.x + half,
            dilation * square.y + half,
            half_angle_tangent(square.degrees, places),
        )
        for square in pose.squares
    ]
    return _certificate(n, side, rows)


_CALLE_COUNT = re.compile(r"# n = ([1-9][0-9]*)")
_CALLE_SIDE = re.compile(r"# s = ([0-9]+\.[0-9]+)")
_CALLE_NUMBER = re.compile(r"-?[0-9]+\.[0-9]+(?:e[-+][0-9]{1,3})?")
#: The longest number `calle_txt` reads; the source prints 18 significant digits.
MAX_CALLE_CHARS = 64


def _calle_number(text: str, where: str) -> Fraction:
    _require(
        len(text) <= MAX_CALLE_CHARS and _CALLE_NUMBER.fullmatch(text) is not None,
        f"{where}: not a plain or scientific decimal: {text[:80]!r}",
    )
    return Fraction(Decimal(text))


def calle_txt(raw: bytes, n: int, options: Mapping[str, str]) -> legacy.Certificate:
    """Rio Calle's decimal text (#529), made exact by rounding each half-angle tangent.

    The file states ``# n = N`` and ``# s = S`` as comment lines, then ``x y theta`` for
    each square: its centre in ``[0, S]^2`` and its rotation about that centre in
    radians, every number a decimal, in scientific notation or not. Other comment lines
    are prose, read and not believed, and blank lines are skipped. Every decimal is read
    exactly as printed; the side is the printed ``S``, and no dilation is applied. Each
    square's ``t = tan(theta/2)`` is the exact tangent rounded down at the declared
    ``half_angle_places``, from 30 to 100 (`half_angle_tangent_radians`), the one option
    read. The file is no exact certificate, and only the exact routes decide whether the
    result packs.
    """
    _require(
        set(options) == {HALF_ANGLE_PLACES},
        f"calle-txt reads exactly {HALF_ANGLE_PLACES}, not {sorted(options)}",
    )
    places = options[HALF_ANGLE_PLACES]
    _require(
        _PLACES.fullmatch(places)
        and MIN_HALF_ANGLE_PLACES <= int(places) <= MAX_HALF_ANGLE_PLACES,
        f"{HALF_ANGLE_PLACES} is an integer from {MIN_HALF_ANGLE_PLACES} to "
        f"{MAX_HALF_ANGLE_PLACES}, not {places[:80]!r}",
    )
    lines = [line.strip() for line in _text(raw).splitlines() if line.strip()]
    comments = [line for line in lines if line.startswith("#")]
    counts = [match for line in comments if (match := _CALLE_COUNT.fullmatch(line))]
    sides = [match for line in comments if (match := _CALLE_SIDE.fullmatch(line))]
    _require(
        len(counts) == 1 and int(counts[0].group(1)) == n,
        f"n={n}: the file must state `# n = {n}` once",
    )
    _require(len(sides) == 1, f"n={n}: the file must state `# s = S` once")
    rows = []
    data = [line for line in lines if not line.startswith("#")]
    for index, line in enumerate(data, start=1):
        where = f"n={n} square {index}"
        fields = line.split()
        _require(len(fields) == 3, f"{where}: {len(fields)} fields, not `x y theta`")
        x, y, theta = (_calle_number(field, where) for field in fields)
        rows.append((x, y, half_angle_tangent_radians(theta, int(places))))
    return _certificate(n, Fraction(Decimal(sides[0].group(1))), rows)


#: Every certificate format a declaration may name. The module docstring says how to add one.
ADAPTERS: dict[str, Adapter] = {
    "evand-cert": evand_cert,
    "squish-json": squish_json,
    "pingyou-json": pingyou_json,
    "witness-corners": witness_corners,
    "witness-center-basis": witness_center_basis,
    "centred-json": centred_json,
    "decimal-dilation": decimal_dilation,
    "sqcert": sqcert,
    "calle-txt": calle_txt,
}


def parse_certificate(
    raw: bytes, n: int, form: str, options: Mapping[str, str] | None = None
) -> legacy.Certificate:
    """One retained file through its declared adapter."""
    _require(form in ADAPTERS, f"unknown certificate format {form!r}")
    return ADAPTERS[form](raw, n, {} if options is None else options)


def admit(certificate: legacy.Certificate, offered: str) -> None:
    """Refuse a side that neither equals the printed side nor rounds up to it there."""
    if _FRACTION.fullmatch(offered):
        _require(
            certificate.side == Fraction(offered),
            f"n={certificate.n}: exact side {legacy.literal(certificate.side)} is not the "
            f"printed {offered}",
        )
        return
    _require(_PRINTED.fullmatch(offered), f"n={certificate.n}: offered side is not a decimal")
    places = len(offered.partition(".")[2])
    printed = Fraction(Decimal(offered))
    rounded = Fraction(Decimal(legacy.ceiling_decimal(certificate.side, places)))
    _require(
        printed in {certificate.side, rounded},
        f"n={certificate.n}: exact side {legacy.literal(certificate.side)} does not round up "
        f"to the printed {offered} at {places} places",
    )


def row_options(row: CertificateRow) -> dict[str, str]:
    """The options a certificate row declares for its format's reader, by name."""
    options = row.get("options", [])
    names = [option["name"] for option in options]
    _require(len(names) == len(set(names)), f"n={row['n']}: an option is declared twice")
    return {option["name"]: option["value"] for option in options}


def _read(source: Path, path: str) -> bytes:
    relative = PurePosixPath(path)
    _require(
        not relative.is_absolute()
        and ".." not in relative.parts
        and relative.as_posix() == path,
        f"not a plain upstream path: {path}",
    )
    target = source / path
    ensure_private(target if target.exists() else target.with_name(target.name + ".gz"))
    try:
        return read_retained_bytes(target, limit=MAX_SOURCE_BYTES)
    except (OSError, ValueError) as error:
        raise ReportError(f"{path}: {error}") from error


def _record(packet: Path) -> acquire_source.Record:
    value = json.loads((packet / acquire_source.RECORD).read_text(encoding="utf-8"))
    return cast("acquire_source.Record", value)


def fact_witness(
    packet: Path, declaration: Declaration, row: CertificateRow, certificate: legacy.Certificate
) -> dict[str, Any]:
    """A derived fact: the positive job's deciding witness, with the pinned file it is from.

    ``revision_sha256`` is the digest the packet's acquisition record pins for the file,
    which is not retained; ``derive`` writes the fact only from bytes that have it. For a
    member of a release asset it is the member's own digest, the file the manifest pinned
    at ``revision`` binds through the asset's, and the address is the asset's, with the
    member as its fragment.
    """
    record = _record(packet)
    source = record["sources"][0]
    pinned = {item["path"]: item for item in source["pinned_only"]}
    archive = row.get("archive")
    bound = row["path"] if archive is None else archive["manifest"]
    _require(bound in pinned, f"n={row['n']}: a fact for a file the packet does not pin")
    witness = kernel.to_witness(certificate, **_profile(declaration))
    if archive is None:
        url = f"{source['source_url']}/blob/{source['source_commit']}/{row['path']}"
        digest = pinned[row["path"]]["sha256"]
    else:
        url = (
            f"https://github.com/{archive['repository']}/releases/download/{archive['tag']}/"
            f"{archive['asset']}#{archive['member']}"
        )
        digest = archive["sha256"]
    witness["source"] = {
        "key": declaration["source_key"],
        "path": (packet / acquire_source.RECORD).relative_to(REPO).as_posix(),
        "url": url,
        "retrieved": record["retrieved_at_utc"][:10],
        "revision": source["source_commit"],
        "revision_sha256": digest,
    }
    return witness


def certificate_from_witness(witness: Mapping[str, Any], n: int) -> legacy.Certificate:
    """Recover every centre and half-angle exactly; refuse a basis that is no rotation."""
    squares = witness.get("squares")
    _require(
        witness.get("n") == n
        and witness.get("representation") == "center-basis"
        and witness.get("scalar") == {"kind": "rational"}
        and type(squares) is list,
        f"n={n}: a derived fact is a complete rational centre-basis witness",
    )
    rows = []
    for index, entry in enumerate(cast("list[Any]", squares), start=1):
        where = f"n={n} square {index}"
        square = cast("dict[str, list[Any]]", entry) if type(entry) is dict else {}
        _require(
            set(square) == {"id", "center", "basis"}
            and square["id"] == index
            and len(square["center"]) == len(square["basis"]) == 2,
            f"{where}: incomplete exact pose",
        )
        x, y = (_literal(value, where) for value in square["center"])
        c, s = (_literal(value, where) for value in square["basis"])
        _require(c != -1, f"{where}: no finite half-angle")
        t = s / (1 + c)
        _require(legacy.Pose(x, y, t).basis == (c, s), f"{where}: the basis is no rotation")
        rows.append((x, y, t))
    return _certificate(n, _literal(witness.get("side"), f"n={n} side"), rows)


def read_fact(
    packet: Path, declaration: Declaration, row: CertificateRow
) -> legacy.Certificate:
    """Admit one derived fact: a valid witness that rebuilds itself from its certificate."""
    path = packet / row.get("fact", "")
    ensure_private(retained_data.compressed_path(path))
    try:
        raw = read_retained_bytes(path, limit=4 * MAX_SOURCE_BYTES)
        document = load_yaml(raw.decode("utf-8"))
        witness = validate_witness_document(document, path=path, fallback_schema=WITNESS_SCHEMA)
    except (OSError, ValueError, yaml.YAMLError, WitnessError) as error:
        raise ReportError(
            f"n={row['n']}: derived fact is not a valid witness: {error}"
        ) from error
    certificate = certificate_from_witness(witness, row["n"])
    rebuilt = witness_envelope(
        fact_witness(packet, declaration, row, certificate), schema=FACT_SCHEMA
    )
    _require(document == rebuilt, f"n={row['n']}: derived fact differs from its own rebuild")
    return certificate


def read_facts(
    packet: Path, numbers: Collection[int] | None = None
) -> dict[int, legacy.Certificate]:
    """Admit every declared certificate once the packet's custody check passes.

    With ``numbers``, only those counts' certificates are read: a deciding child needs its
    own, and PR #574's 85 facts take longer to admit than most of its jobs take to decide.
    """
    ensure_private(packet)
    declaration = load_declaration(packet)
    source = REPO / acquisition(packet)["archived_path"]
    certificates = {}
    for row in declaration["certificates"]:
        n = row["n"]
        if numbers is not None and n not in numbers:
            continue
        if "fact" in row:
            certificate = read_fact(packet, declaration, row)
        else:
            raw = _read(source, row["path"])
            certificate = parse_certificate(raw, n, row["format"], row_options(row))
        admit(certificate, row["offered"])
        # Beside a derived fact the other files are not retained; ``derive`` compares them.
        for other in [] if "fact" in row else row.get("same_packing", []):
            copy = parse_certificate(_read(source, other["path"]), n, other["format"])
            _require(copy == certificate, f"n={n}: {other['path']} states another packing")
        certificates[n] = certificate
    return certificates


# --------------------------------------------------------------------------- houses


def grid_side(n: int) -> Fraction:
    """The trivial bound ``ceil(sqrt(n))``: a grid of that side holds ``n`` squares."""
    _require(type(n) is int and n >= 1, "count must be positive")
    return Fraction(math.isqrt(n - 1) + 1)


@functools.cache
def _sides(loader: Callable[[], Mapping[int, legacy.Certificate]]) -> dict[int, Fraction]:
    """Every side of one retained house packet, read once: those packets never change."""
    return {n: certificate.side for n, certificate in loader().items()}


@functools.cache
def _import_sides(packet: Path) -> dict[int, Fraction]:
    """Every exact side of one packet this module imports, read once after its custody check.

    Keyed on the packet's path, so a private copy is read as itself.
    """
    return {n: certificate.side for n, certificate in read_facts(packet).items()}


def import_side(name: str, n: int) -> Fraction:
    """One exact side of the import packet named ``name``, its directory name."""
    return _import_sides(packet_path(name))[n]


def _import(name: str) -> Callable[[int], Fraction]:
    """The reader of one import packet's exact sides, by the packet's directory name; the
    packet is the reader's ``args[0]``."""
    return functools.partial(import_side, name)


def _evand_optima(n: int) -> Fraction:
    path = legacy.certificate_path(legacy.CERTS, n)
    return legacy.parse(path.read_text(encoding="utf-8"), expected_n=n).side


#: How each holding source's exact side is rebuilt from its own retained packet, keyed by
#: source key, so a comparison stays what it was however the case records later move.
HOUSES: dict[str, Callable[[int], Fraction]] = {
    "grid": grid_side,
    "[evand exact optima 2026-10-05]": _evand_optima,
    "[Rehwaldt n68 refinement 2026-10-07]": lambda n: Fraction(
        rehwaldt.read_fact(rehwaldt.N68, n)["side"]
    ),
    "[Rehwaldt Couzo refinements 2026-10-07]": lambda n: Fraction(
        rehwaldt.read_fact(rehwaldt.COUZO, n)["side"]
    ),
    "[SQUISH update 2026-10-07]": lambda n: Fraction(squish_update.read_fact(n)["side"]),
    "[Couzo exact refinements 2026-10-08]": lambda n: _sides(couzo_451.read_facts)[n],
    "[Gupta rational refinements 2026-10-08]": lambda n: _sides(gupta.read_facts)[n],
    "[SQUISH second update 2026-10-07]": lambda n: Fraction(squish_second.read_fact(n)["side"]),
    "[SQUISH ten packings 2026-10-07]": lambda n: Fraction(squish_first.read_fact(n)["side"]),
    "[ry-xu square packing 2026]": lambda n: _sides(ryxu.read_facts)[n],
    "[Daniel new arrangements 2026-10-07]": lambda n: _sides(kernel.read_facts)[n],
    "[Daniel record hunt 2026-10-09]": lambda n: _sides(evand_hunt.read_facts)[n],
    "[Couzo follow-up refinements 2026-10-08]": lambda n: _sides(couzo_followup.read_facts)[n],
    "[Couzo exact certificates 2026-10-09]": _import("couzo-exact-certificates-2026-10-09"),
    "[SQUISH third request 2026-10-09]": _import("squish-481-third-request-2026-10-09"),
    "[Fang two-wedge certificates 2026-10-10]": _import(
        "fang-two-wedge-certificates-2026-10-10"
    ),
    "[Couzo certificates 2026-10-10]": _import("couzo-certificates-2026-10-10"),
    "[Daniel record hunt 3 2026-10-10]": _import("evand-record-hunt3-2026-10-10"),
    "[Deleeuw n70 refinement 2026-10-10]": _import("ebdeleeuw-n70-refinement-2026-10-10"),
    "[Mishapolk decimal poses 2026-10-09]": _import("mishapolk-decimal-poses-2026-10-09"),
    "[Daniel regularized lists 2026-10-10]": _import("evand-regularized-2026-10-10"),
    "[Daniel trio126 2026-10-09]": _import("evand-trio126-2026-10-09"),
    "[PingYou n207 certificate 2026-10-11]": _import("pingyou-n207-certificate-2026-10-11"),
    "[PingYou n153 certificate 2026-10-11]": _import("pingyou-n153-certificate-2026-10-11"),
    "[Ostashev records 2026-10-11]": _import("dostashev-records-2026-10-11"),
    "[Barnett refinements 2026-10-11]": _import("barnett-refinements-2026-10-11"),
    "[SQUISH fourth request 2026-10-11]": _import("squish-500-fourth-request-2026-10-11"),
    "[Couzo certificates 2026-10-11]": _import("couzo-certificates-2026-10-11"),
    "[PingYou n302 certificate 2026-10-12]": _import("pingyou-n302-certificate-2026-10-12"),
    "[PingYou n153 refinement 2026-10-12]": _import("pingyou-n153-refinement-2026-10-12"),
    "[PingYou n207 refinement 2026-10-12]": _import("pingyou-n207-refinement-2026-10-12"),
    "[PingYou n146 refinement 2026-10-12]": _import("pingyou-n146-refinement-2026-10-12"),
    "[PingYou n261 refinement 2026-10-12]": _import("pingyou-n261-refinement-2026-10-12"),
    "[PingYou n105 refinement 2026-10-12]": _import("pingyou-n105-refinement-2026-10-12"),
    "[PingYou n272 refinement 2026-10-12]": _import("pingyou-n272-refinement-2026-10-12"),
    "[Couzo certificates 2026-10-12]": _import("couzo-certificates-2026-10-12"),
    "[Couzo certificates 2026-10-13]": _import("couzo-certificates-2026-10-13"),
    "[Mishapolk exact certificates 2026-10-12]": _import(
        "mishapolk-exact-certificates-2026-10-12"
    ),
    "[Mishapolk records 2026-10-14]": _import("mishapolk-records-2026-10-14"),
    "[Ostashev compositions 2026-10-12]": _import("dostashev-compositions-2026-10-12"),
    "[Ostashev merged bands 2026-10-13]": _import("dostashev-merged-bands-2026-10-13"),
    "[Daniel compositions 2026-10-13]": _import("evand-compositions-2026-10-13"),
    "[Daniel fresh compositions 2026-10-14]": _import("evand-fresh-compositions-2026-10-14"),
    "[Ostashev records 2026-10-12]": _import("dostashev-records-2026-10-12"),
    "[Calle n102 2026-10-12]": _import("riocalle-n102-2026-10-12"),
    "[Daniel n154 2026-10-12]": _import("evand-n154-2026-10-12"),
    "[Couzo issue-583 certificates 2026-10-13]": _import("couzo-issue583-2026-10-13"),
    "[PingYou PR 574 certificates 2026-10-13]": _import(
        "pingyou-pr574-certificates-2026-10-13"
    ),
    # T-155: the side of the retained view of Evan Daniel's regularizer at each count.
    "[Daniel regularizer 2026-10-11]": regularized.view_side,
}


def house_side(reader: str, n: int) -> Fraction:
    _require(reader in HOUSES, f"no reader for {reader}")
    try:
        return HOUSES[reader](n)
    except (OSError, ValueError, KeyError) as error:
        raise ReportError(f"n={n}: {reader} does not rebuild: {error}") from error


# --------------------------------------------------------------------------- comparison


class Span(NamedTuple):
    """The numbers a side may be: one exact number, or a printed decimal's range."""

    low: Fraction
    high: Fraction
    open_low: bool
    open_high: bool


def exact_span(value: Fraction) -> Span:
    return Span(value, value, open_low=False, open_high=False)


def printed_span(printed: str, rounding: str) -> Span:
    """A side printed rounded up lies in ``(p - u, p]``, otherwise within ``u`` of ``p``.

    ``u`` is one unit in the last printed place. A ``binary64`` print renders the double
    nearest the side, which is within half an ulp of the side, to within half a unit of
    that double; the side then lies within one ulp of the double ``p`` reads as, plus
    ``u``. Read as ``unstated``, #593's 16-place prints at 271 and 302 exclude their own
    certificates' exact sides, which lie 1.2e-15 from them.
    """
    _require(_PRINTED.fullmatch(printed) and rounding in ROUNDINGS, "printed side, rounding")
    value = Fraction(Decimal(printed))
    unit = Fraction(1, 10 ** len(printed.partition(".")[2]))
    if rounding == "up":
        return Span(value - unit, value, open_low=True, open_high=False)
    if rounding == "binary64":
        slack = Fraction(math.ulp(float(value))) + unit
        return Span(value - slack, value + slack, open_low=False, open_high=False)
    return Span(value - unit, value + unit, open_low=False, open_high=False)


def below(first: Span, second: Span) -> bool:
    """Every number the first may be is smaller than every number the second may be."""
    return first.high < second.low or (
        first.high == second.low and (first.open_high or second.open_low)
    )


def relation(side: Fraction, other: Span) -> str:
    """Where the certificate stands against another side: below, equal, above, undecided."""
    own = exact_span(side)
    if below(own, other):
        return "below"
    if below(other, own):
        return "above"
    return "equal" if other == own else "undecided"


def smallest(candidates: list[tuple[str, Span]]) -> dict[str, Any]:
    """The one report below every other; else those nothing is below, tied or undecided.

    Reports nothing is decidably below are ``tied`` when each is one exact number and all
    are the same number, and ``undecided_among`` otherwise.
    """
    winners = [
        label
        for label, span in candidates
        if all(below(span, other) for name, other in candidates if name != label)
    ]
    if winners:
        return {"smallest": winners[0]}
    unbeaten = [
        (label, span)
        for label, span in candidates
        if not any(below(other, span) for name, other in candidates if name != label)
    ]
    labels = [label for label, _ in unbeaten]
    if len({span for _, span in unbeaten}) == 1 and unbeaten[0][1].low == unbeaten[0][1].high:
        return {"smallest": None, "tied": labels}
    return {"smallest": None, "undecided_among": labels}


def _row(
    row: CertificateRow,
    certificate: legacy.Certificate,
    declaration: Declaration,
) -> dict[str, Any]:
    n, side = row["n"], certificate.side
    houses = {house["n"]: house for house in declaration["houses"]}
    pending = [report for report in declaration["pending"] if report["n"] == n]
    result: dict[str, Any] = {
        "n": n,
        "certificate": row["path"],
        "format": row["format"],
        "requested": n in declaration["requested"],
        "replayed": n in declaration["replayed"],
        "offered_side": row["offered"],
        "printed_in": row.get("printed_in", declaration["issue"]),
        "exact_side": legacy.literal(side),
        "ceiling": legacy.ceiling_decimal(side, DISPLAY_PLACES),
        "first_committed": row["first_committed"],
        "grid_side": legacy.literal(grid_side(n)),
    }
    candidates: list[tuple[str, Span]] = [(THIS, exact_span(side))]
    if n <= HORIZON:
        house = houses[n]
        prior = house_side(house["reader"], n)
        printed_lane = "reported_rounding" in house
        lanes = ("verified_value",) if printed_lane else ("reported_value", "verified_value")
        for lane in lanes:
            shown = Fraction(Decimal(house[lane]))
            unit = Fraction(1, 10 ** len(house[lane].partition(".")[2]))
            _require(
                shown == prior or prior < shown <= prior + unit,
                f"n={n}: the case's {lane} is not its house's side, exact or rounded up",
            )
        result["case"] = {
            **{key: value for key, value in house.items() if key not in {"n", "reader"}},
            "exact_side": legacy.literal(prior),
            "relation": relation(side, exact_span(prior)),
            "difference": legacy.literal(prior - side),
        }
        candidates.append((f"case: {house['holders']}", exact_span(prior)))
        if printed_lane:
            span = printed_span(house["reported_value"], house.get("reported_rounding", ""))
            result["case"]["reported_relation"] = relation(side, span)
            candidates.append((f"case reported: {house['source_key']}", span))
    else:
        result["case"] = None
        candidates.append(("grid", exact_span(grid_side(n))))
    others = []
    for report in pending:
        entry: dict[str, Any] = {
            key: value for key, value in report.items() if key not in {"n", "reader"}
        }
        if "reader" in report:
            value = house_side(report["reader"], n)
            span = exact_span(value)
            entry["exact_side"] = legacy.literal(value)
        else:
            printed, rounding = report.get("printed", ""), report.get("rounding", "")
            value = Fraction(Decimal(printed))
            span = printed_span(printed, rounding)
        entry["relation"] = relation(side, span)
        # The other side less the certificate's, exactly or at its printed value.
        entry["difference"] = legacy.literal(value - side)
        others.append(entry)
        candidates.append((report["report"], span))
    result["pending"] = others
    result.update(smallest(candidates))
    return result


def compare(
    packet: Path, certificates: dict[int, legacy.Certificate] | None = None
) -> dict[str, Any]:
    """The frozen claim record, rebuilt from the certificates and the retained houses."""
    certificates = read_facts(packet) if certificates is None else certificates
    declaration = load_declaration(packet)
    source = acquisition(packet)
    rows = [
        _row(row, certificates[row["n"]], declaration) for row in declaration["certificates"]
    ]
    return {
        "format": CLAIMS_FORMAT,
        "issue": declaration["issue"],
        "source": source["source_url"],
        "revision": source["source_commit"],
        "read_on": declaration["read_on"],
        "read_at_main": declaration["read_at_main"],
        "horizon": HORIZON,
        "results": rows,
    }


def beyond_horizon_claims(claims: Mapping[str, Any]) -> dict[str, Any] | None:
    """The requested claims beyond the horizon: the record a beyond-horizon row is read from."""
    rows = [row for row in claims["results"] if row["n"] > HORIZON and row["requested"]]
    if not rows:
        return None
    return {
        "format": BEYOND_FORMAT,
        "issue": claims["issue"],
        "source": claims["source"],
        "revision": claims["revision"],
        "horizon": HORIZON,
        "results": [
            {key: row[key] for key in ("n", "offered_side", "exact_side", "ceiling")}
            for row in rows
        ],
    }


def live_problems(packet: Path) -> list[str]:
    """Where the declaration's reading differs from the records as they stand now.

    Asked only when the claim record is written: the frozen record keeps what was read,
    however the case records and the coverage register later move.
    """
    declaration = load_declaration(packet)
    problems = []
    for house in declaration["houses"]:
        n = house["n"]
        case = coverage_check.parse_case(ROOT / f"frontier/n-{n:03d}.md")
        reported, verified = case["reported_upper_bound"], case["verified_upper_bound"]
        found = [
            reported["source_key"],
            str(reported["value"]),
            str(verified["value"]),
            [str(item) for item in verified["evidence"]],
        ]
        expected = [
            house["source_key"],
            house["reported_value"],
            house["verified_value"],
            house["evidence"],
        ]
        if found != expected:
            problems.append(f"n={n}: the case record reads {found}, not {expected}")
    register = safe_load((ROOT / "frontier/results.yaml").read_text(encoding="utf-8"))
    entries = {entry["id"] for entry in register["results"]}
    problems.extend(
        f"n={item['n']}: no register entry {item['result']}"
        for item in [*declaration["houses"], *declaration["pending"]]
        if "result" in item and item["result"] not in entries
    )
    coverage = safe_load(coverage_check.COVERAGE.read_text(encoding="utf-8"))
    # A count's current row may be this packet's own, which is no other report to declare.
    current = {
        n: row
        for n, row in coverage_check.current_beyond_horizon(coverage).items()
        if row["source_id"] != packet.name
    }
    declared = {(p["n"], p["report"]): p.get("printed") for p in declaration["pending"]}
    problems.extend(
        f"n={row['n']}: declare the current beyond-horizon row of "
        f"{current[row['n']]['source_id']}, {current[row['n']]['value']}, as a pending report"
        for row in declaration["certificates"]
        if row["n"] in current
        and declared.get((row["n"], current[row["n"]]["source_id"]))
        != current[row["n"]]["value"]
    )
    return problems


def _json_text(value: Any) -> str:
    return json.dumps(value, indent=2, allow_nan=False, ensure_ascii=False) + "\n"


def _record_text(value: Mapping[str, Any]) -> str:
    """A claim record with one result per line, so a large release stays a short file."""
    head = [
        f"  {json.dumps(key)}: {json.dumps(item, ensure_ascii=False)}"
        for key, item in value.items()
        if key != "results"
    ]
    rows = [
        "    " + json.dumps(row, allow_nan=False, ensure_ascii=False)
        for row in value["results"]
    ]
    return (
        "{\n" + ",\n".join([*head, '  "results": [\n' + ",\n".join(rows) + "\n  ]"]) + "\n}\n"
    )


def _stored(path: Path) -> Any:
    ensure_private(path)
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=kernel.unique_object)


def write_claims(packet: Path) -> None:
    """Freeze the comparison, after holding the declaration to the live records."""
    if problems := live_problems(packet):
        raise ReportError("the declaration does not read the records: " + "; ".join(problems))
    claims = compare(packet)
    for path, value in (
        (packet / CLAIMS, claims),
        (packet / BEYOND, beyond_horizon_claims(claims)),
    ):
        ensure_private(path.parent)
        if value is None:
            path.unlink(missing_ok=True)
            continue
        with atomic_output_file(path) as temporary:
            temporary.write_text(_record_text(value), encoding="utf-8")


def check_claims(
    packet: Path, certificates: dict[int, legacy.Certificate] | None = None
) -> dict[str, Any]:
    """Hold the frozen record, and its beyond-horizon part, to their rebuild."""
    rebuilt = compare(packet, certificates)
    if _stored(packet / CLAIMS) != rebuilt:
        raise ReportError("frozen claim record differs from its rebuild")
    beyond = beyond_horizon_claims(rebuilt)
    if beyond is None:
        _require(not (packet / BEYOND).exists(), "a beyond-horizon record without such claims")
    elif not (packet / BEYOND).is_file() or _stored(packet / BEYOND) != beyond:
        raise ReportError("frozen beyond-horizon claim record differs from its rebuild")
    return rebuilt


# --------------------------------------------------------------------------- derivation


def checkout_problems(packet: Path, checkout: Path) -> list[str]:
    """Where a checkout fails to yield this packet's acquisition record and manifest.

    ``acquire_source.acquire`` writes a scratch copy of the packet from the checkout: it
    refuses a checkout at another commit and binds every file to its Git blob there. Equal
    records and manifests then mean every pinned file has the digest the packet records.
    """
    with tempfile.TemporaryDirectory() as scratch:
        root = Path(scratch)
        copy = root / packet.relative_to(REPO)
        (copy / acquire_source.DECLARATION).parent.mkdir(parents=True)
        shutil.copyfile(packet / acquire_source.DECLARATION, copy / acquire_source.DECLARATION)
        try:
            acquire_source.acquire(copy, checkout.resolve(), root)
        except (OSError, ValueError, subprocess.CalledProcessError) as error:
            return [f"the checkout does not yield this packet: {error}"]
        problems = []
        if _record(copy) != _record(packet):
            problems.append("the checkout does not yield this packet's acquisition record")
        fresh = acquire_source.read_manifest(copy / acquire_source.MANIFEST)
        if fresh != acquire_source.read_manifest(packet / acquire_source.MANIFEST):
            problems.append("the checkout does not yield this packet's manifest")
        return problems


def _checkout_bytes(packet: Path, checkout: Path, path: str) -> bytes:
    """A file the packet pins, read from a checkout that `checkout_problems` admitted."""
    pinned = {item["path"] for item in _record(packet)["sources"][0]["pinned_only"]}
    _require(path in pinned, f"{path}: not a file this packet pins")
    upstream = checkout / path
    _require(
        not upstream.is_symlink() and upstream.resolve().is_relative_to(checkout.resolve()),
        f"{path}: not a plain file of the checkout",
    )
    with upstream.open("rb") as stream:
        return stream.read(MAX_SOURCE_BYTES + 1)


#: The largest release asset `_asset_bytes` reads: PR #574's native-witness archive is
#: 21,737,024 bytes.
MAX_ASSET_BYTES = 64_000_000


class ReleaseAssets:
    """Release assets read from a local directory, each held to the pinned manifest once.

    An asset is admitted only where a manifest the checkout pins, read from that admitted
    checkout, names its repository and tag and lists it by name with exactly its size and
    SHA-256. A member is then read from the admitted bytes, and must have the digest the
    declaration states.
    """

    def __init__(self, packet: Path, checkout: Path, directory: Path | None) -> None:
        self.packet, self.checkout, self.directory = packet, checkout, directory
        self.admitted: dict[tuple[str, str], bytes] = {}

    def asset(self, spec: ArchiveMember) -> bytes:
        key = (spec["manifest"], spec["asset"])
        if key in self.admitted:
            return self.admitted[key]
        _require(self.directory is not None, "a release-asset member needs --assets")
        directory = cast("Path", self.directory)
        raw = _checkout_bytes(self.packet, self.checkout, spec["manifest"])
        try:
            loaded: object = safe_load(raw.decode("utf-8"))
        except (UnicodeDecodeError, yaml.YAMLError) as error:
            raise ReportError(f"{spec['manifest']}: not a YAML manifest: {error}") from error
        _require(type(loaded) is dict, f"{spec['manifest']}: not a manifest")
        manifest = cast("dict[str, Any]", loaded)
        _require(
            manifest.get("repository") == spec["repository"]
            and manifest.get("tag") == spec["tag"],
            f"{spec['manifest']}: does not name {spec['repository']} at {spec['tag']}",
        )
        objects = [
            item
            for item in manifest.get("objects") or []
            if type(item) is dict and item.get("asset") == spec["asset"]
        ]
        _require(len(objects) == 1, f"{spec['manifest']}: does not list {spec['asset']} once")
        size, digest = objects[0].get("size"), objects[0].get("sha256")
        path = directory / spec["asset"]
        _require(
            path.is_file() and not path.is_symlink() and path.stat().st_size == size,
            f"{spec['asset']}: no local file of the manifest's {size} bytes",
        )
        _require(type(size) is int and size <= MAX_ASSET_BYTES, f"{spec['asset']}: too large")
        data = path.read_bytes()
        _require(
            len(data) == size and hashlib.sha256(data).hexdigest() == digest,
            f"{spec['asset']}: the local file is not the asset the manifest pins",
        )
        self.admitted[key] = data
        return data

    def member(self, spec: ArchiveMember) -> bytes:
        try:
            with zipfile.ZipFile(io.BytesIO(self.asset(spec))) as archive:
                info = archive.getinfo(spec["member"])
                _require(
                    info.file_size <= MAX_SOURCE_BYTES, f"{spec['member']}: exceeds its ceiling"
                )
                data = archive.read(info)
        except (
            KeyError,
            zipfile.BadZipFile,
            RuntimeError,
            NotImplementedError,
            EOFError,
            zlib.error,
        ) as error:
            raise ReportError(
                f"{spec['asset']}: no member {spec['member']}: {error}"
            ) from error
        _require(
            hashlib.sha256(data).hexdigest() == spec["sha256"],
            f"{spec['member']}: the member is not the bytes the declaration names",
        )
        return data


def derive(
    packet: Path, checkout: Path, *, check: bool = False, assets: Path | None = None
) -> list[retained_data.Row]:
    """Write, or with ``check`` compare, each derived fact from a checkout at the pin.

    A fact is stored as ``facts/n-NNN.yaml.gz``, deterministic gzip by the archive's rule,
    and its row belongs in the packet README's Compressed Files table, origin ``receipt``.
    Each ``same_packing`` file of a fact's row is read from the same checkout and must
    state the certificate's packing exactly, or the fact is refused. A row read from a
    release asset (``archive``) is read from ``assets``, a directory holding the assets
    by name, through a manifest the checkout pins (`ReleaseAssets`).
    """
    ensure_private(packet)
    declaration = load_declaration(packet)
    acquisition(packet)
    if problems := checkout_problems(packet, checkout):
        raise ReportError("; ".join(problems))
    store = ReleaseAssets(packet, checkout, assets)

    def read(item: CertificateRow | SamePacking) -> bytes:
        if "archive" in item:
            return store.member(item["archive"])
        return _checkout_bytes(packet, checkout, item["path"])

    written = []
    for row in declaration["certificates"]:
        if "fact" not in row:
            continue
        n = row["n"]
        raw = read(row)
        certificate = parse_certificate(raw, n, row["format"], row_options(row))
        admit(certificate, row["offered"])
        for other in row.get("same_packing", []):
            raw = read(other)
            copy = parse_certificate(raw, n, other["format"])
            _require(copy == certificate, f"n={n}: {other['path']} states another packing")
        witness = fact_witness(packet, declaration, row, certificate)
        text = witness_document(witness, schema=FACT_SCHEMA)
        target = packet / row["fact"]
        stored = retained_data.compressed_path(target)
        validate_witness_document(load_yaml(text), path=target, fallback_schema=WITNESS_SCHEMA)
        if check:
            ensure_private(stored)
            _require(
                stored.is_file() and read_retained_bytes(stored) == text.encode(),
                f"n={row['n']}: the retained fact is not what the checkout derives",
            )
        else:
            ensure_private(target.parent if target.parent.exists() else packet)
            target.parent.mkdir(exist_ok=True)
            stored.unlink(missing_ok=True)
            with atomic_output_file(target) as temporary:
                temporary.write_text(text, encoding="utf-8")
            retained_data.compress(target)
        written.append(retained_data.describe(packet, stored, "receipt"))
    return written


# --------------------------------------------------------------------------- replay


def replayed_facts(
    packet: Path, certificates: Mapping[int, legacy.Certificate] | None = None
) -> tuple[Declaration, dict[int, legacy.Certificate]]:
    """The declaration and the admitted certificates of its ``replayed`` roster, in order."""
    certificates = read_facts(packet) if certificates is None else certificates
    declaration = load_declaration(packet)
    return declaration, {n: certificates[n] for n in declaration["replayed"]}


def check_certification(
    packet: Path,
    numbers: list[int] | None = None,
    *,
    replay: bool = False,
    certificates: Mapping[int, legacy.Certificate] | None = None,
) -> dict[int, Any]:
    """Admit the retained receipt; with ``replay``, decide the selected counts again."""
    declaration, facts = replayed_facts(packet, certificates)
    selected = list(facts) if numbers is None else numbers
    _require(
        selected
        and all(type(n) is int for n in selected)
        and len(set(selected)) == len(selected)
        and not set(selected) - set(facts),
        "empty, repeated or unknown replay selection",
    )
    profile = _profile(declaration)
    positives: dict[int, Any] = {}
    for record, part in receipt_parts(packet, facts):
        positives |= kernel.validate_receipt(
            record, part, receipt_format=declaration["receipt_format"], **profile
        )
        if replay and set(part) & set(selected):
            kernel.replay_receipt(record, part, selected, **profile)
    return positives


def evidence_bytes(value: Any) -> int:
    """The size of the kernel's serialization of a record, which its ceiling bounds."""
    text = json.dumps(value, separators=(",", ":"), allow_nan=False, sort_keys=True)
    return len(text.encode()) + 1


def receipt_parts(
    packet: Path, facts: Mapping[int, legacy.Certificate]
) -> list[tuple[dict[str, Any], dict[int, legacy.Certificate]]]:
    """The retained receipt, whole or by count, each with the certificates it decides."""
    whole = packet / RECEIPT
    parts = {n: packet / shard(n) for n in facts}
    stray = {
        path
        for path in (packet / "receipts").glob("exact-certification-n*.json.xz")
        if path not in parts.values()
    }
    present = [path for path in parts.values() if path.exists()]
    _require(not stray, f"receipts for counts outside the replayed roster: {sorted(stray)}")
    _require(
        whole.exists() != bool(present) and len(present) in {0, len(parts)},
        "a receipt is the roster's whole receipt or one per replayed count, not both",
    )
    if whole.exists():
        ensure_private(whole)
        return [(kernel.read_xz(whole), dict(facts))]
    result = []
    for n, path in parts.items():
        ensure_private(path)
        result.append((kernel.read_xz(path), {n: facts[n]}))
    return result


def save_receipt(
    packet: Path, declaration: Declaration, facts: Mapping[int, Any], rows: list[Any]
) -> None:
    """Write the roster's receipt, split by count where the whole exceeds the ceiling."""
    head = {"format": declaration["receipt_format"], "routes": list(ROUTES)}
    record = {**head, "cases": rows}
    for path in [packet / RECEIPT, *(packet / shard(n) for n in facts)]:
        ensure_private(path)
        path.unlink(missing_ok=True)
    if evidence_bytes(record) <= kernel.MAX_BYTES:
        kernel.save_xz(packet / RECEIPT, record)
        return
    for n in facts:
        cases = [row for row in rows if row["n"] == n]
        kernel.save_xz(packet / shard(n), {**head, "cases": cases})


def run_job(
    packet: Path, job: tuple[int, str], directory: Path, timeout: int
) -> dict[str, Any]:
    """Run one job as ``python -m devtools.upper_bound_reports PACKET decide-job``.

    The kernel's own runner names no packet. As there, the child's stdout and stderr are
    kept beside its output whatever happens, and a timeout leaves a failure record.
    """
    n, control = job
    path = directory / f"n{n}-{control}.json"
    command = [sys.executable, "-m", MODULE, packet.name, "decide-job"]
    command += ["--n", str(n), "--control", control, "--output", str(path)]
    try:
        completed = subprocess.run(command, capture_output=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as error:
        path.with_suffix(".stdout.log").write_bytes(error.stdout or b"")
        path.with_suffix(".stderr.log").write_bytes(error.stderr or b"")
        failure = {"n": n, "control": control, "status": "timeout", "timeout_seconds": timeout}
        path.with_suffix(".failure.json").write_text(_json_text(failure), encoding="utf-8")
        raise ReportError(f"n={n} {control}: deciding child exceeded {timeout}s") from error
    path.with_suffix(".stdout.log").write_bytes(completed.stdout)
    path.with_suffix(".stderr.log").write_bytes(completed.stderr)
    _require(completed.returncode == 0, f"n={n} {control}: child exited {completed.returncode}")
    with path.open("rb") as stream:
        data = stream.read(kernel.MAX_BYTES + 1)
    _require(len(data) <= kernel.MAX_BYTES, "native child receipt exceeds its ceiling")
    return json.loads(data, object_pairs_hook=kernel.unique_object)


def read_job(path: Path) -> dict[str, Any]:
    """One finished job's row, as its child process wrote it."""
    with path.open("rb") as stream:
        data = stream.read(kernel.MAX_BYTES + 1)
    _require(len(data) <= kernel.MAX_BYTES, "native child receipt exceeds its ceiling")
    return json.loads(data, object_pairs_hook=kernel.unique_object)


def certify(
    packet: Path,
    directory: Path,
    *,
    workers: int = MAX_WORKERS,
    timeout: int = JOB_TIMEOUT,
    finished: bool = False,
) -> dict[int, Any]:
    """Run every job of every count in a fresh directory; write the receipt once all pass.

    With ``finished``, the directory instead holds every job's output from an earlier run
    of this command, and the receipt is assembled from those rows, admitted as any is.
    """
    _require(
        type(workers) is int
        and 1 <= workers <= MAX_WORKERS
        and type(timeout) is int
        and 1 <= timeout <= JOB_TIMEOUT,
        "invalid bounded worker/deadline selection",
    )
    declaration, facts = replayed_facts(packet)
    jobs = [(n, control) for n in facts for control in JOBS]
    if finished:
        _require(directory.is_dir(), "no finished job directory")
        rows = [read_job(directory / f"n{n}-{control}.json") for n, control in jobs]
    else:
        _require(not directory.exists(), "native job directory must be a fresh attempt")
        directory.mkdir(parents=True)
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(run_job, packet, job, directory, timeout) for job in jobs]
            rows = [future.result() for future in futures]
    record = {"format": declaration["receipt_format"], "routes": list(ROUTES), "cases": rows}
    positives = kernel.validate_receipt(
        record, facts, receipt_format=declaration["receipt_format"], **_profile(declaration)
    )
    save_receipt(packet, declaration, facts, rows)
    return positives


def decide_job(packet: Path, n: int, control: str, output: Path) -> None:
    """The child's side of `run_job`: decide one job and write its validated row."""
    declaration = load_declaration(packet)
    _require(
        n in declaration["replayed"] and control in JOBS, "job outside the declared roster"
    )
    _require(not output.exists(), "refusing to overwrite a deciding job")
    facts = read_facts(packet, {n})
    kernel.decide_job(facts[n], control, output, **_profile(declaration))


def margins(positives: dict[int, Any]) -> dict[int, dict[str, str]]:
    """The least wall and pair clearance each route found in each positive job."""
    return {
        n: {
            f"{route}_{field}": row[route][f"minimum_{field}"]
            for route in ROUTES
            for field in ("containment_clearance", "best_pair_gap")
        }
        for n, row in positives.items()
    }


def receipt_summary(record: Mapping[str, Any]) -> dict[str, Any]:
    """What the receipt's jobs cost and decided, summed over every job and route."""
    rows = record["cases"]
    return {
        "jobs": len(rows),
        "pair_decisions": sum(row[route]["pairs_tested"] for row in rows for route in ROUTES),
        "route_cpu_seconds": round(sum(sum(row["cpu_seconds"].values()) for row in rows), 2),
        "job_wall_seconds": round(sum(row["wall_seconds"] for row in rows), 2),
        "longest_job_seconds": round(max(row["wall_seconds"] for row in rows), 2),
    }


# --------------------------------------------------------------------------- register plan


def claim_value(side: Fraction) -> str:
    """The side as a claim states it: decimals where they end soon, a fraction otherwise."""
    written = legacy.terminating_decimal(side)
    if written is not None and len(written.partition(".")[2]) <= CLAIM_PLACES:
        return written
    return legacy.literal(side)


def _and(items: list[str]) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + f" and {items[-1]}"


def _sci(value: str | Fraction) -> str:
    return f"{float(Fraction(value)):.2e}"


def _floor_sci(value: Fraction) -> str:
    """Three significant digits rounded down, so a bound stated as "at least" holds."""
    if value <= 0:
        return "0"
    # Seeded from the digit counts, which a float's range never limits; the loops correct it.
    exponent = len(str(value.numerator)) - len(str(value.denominator))
    while Fraction(10) ** exponent > value:
        exponent -= 1
    while Fraction(10) ** (exponent + 1) <= value:
        exponent += 1
    mantissa = math.floor(value / Fraction(10) ** exponent * 100)
    return f"{mantissa / 100:.2f}e{exponent:+03d}"


_WORDS = [
    "Zero",
    "One",
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Eleven",
    "Twelve",
    "Thirteen",
    "Fourteen",
    "Fifteen",
    "Sixteen",
    "Seventeen",
    "Eighteen",
    "Nineteen",
    "Twenty",
]


def _many(count: int, noun: str) -> str:
    """``count`` and ``noun``, made plural with an ``s`` unless the count is one."""
    return f"{count} {noun}" if count == 1 else f"{count} {noun}s"


def _count_word(n: int) -> str:
    return _WORDS[n] if n < len(_WORDS) else str(n)


def _replay(positives: dict[int, Any], record: Mapping[str, Any]) -> str:
    summary = receipt_summary(record)
    found = margins(positives).values()
    wall = min(Fraction(row["exact_verify_containment_clearance"]) for row in found)
    gap = min(Fraction(row["exact_verify_best_pair_gap"]) for row in found)
    return (
        f"A separate complete repository replay is retained for n = "
        f"{_and([str(n) for n in positives])}: {_many(len(positives), 'positive')} and "
        f"{2 * len(positives)} duplicate-square and outside-container controls passed their "
        f"required outcomes on both routes, {summary['pair_decisions']} pair decisions; summed "
        f"over the {summary['jobs']} jobs, the receipt records {summary['route_cpu_seconds']} "
        f"route CPU seconds and {summary['job_wall_seconds']} job wall seconds, the longest "
        f"job {summary['longest_job_seconds']} seconds. "
        + (
            f"Every positive clears every wall by at least {_floor_sci(wall)} and every pair "
            f"by at least {_floor_sci(gap)}."
            if wall
            else "In every positive squares touch the box, a least wall clearance of exactly "
            f"0, and every pair clears by at least {_floor_sci(gap)}."
        )
    )


def comparison(row: Mapping[str, Any]) -> str:
    """One count's frozen comparison, as a sentence of the register's notes.

    Every difference is printed as a distance, the relation saying which side is larger.
    Where no report is decidably smallest, `smallest` either found the unbeaten reports
    to be one exact side (``tied``) or could not order them (``undecided_among``).
    """
    if row["case"] is None:
        grid = Fraction(row["grid_side"]) - Fraction(row["exact_side"])
        parts = [f"beyond the horizon, with no case record, and {_sci(grid)} below the grid"]
    else:
        case = row["case"]
        held = f"{case['holders']}, {case['result']}" if "result" in case else case["holders"]
        decided = case["relation"] in {"below", "above"}
        by = f" by {_sci(abs(Fraction(case['difference'])))}" if decided else ""
        parts = [f"{case['relation']} the case's ceiling ({held}){by}"]
    for other in row["pending"]:
        decided = other["relation"] in {"below", "above"}
        by = f" by {_sci(abs(Fraction(other['difference'])))}" if decided else ""
        parts.append(f"{other['relation']} {other['report']} ({other['holders']}){by}")
    if row["smallest"]:
        parts.append(f"smallest: {row['smallest']}")
    elif "tied" in row:
        parts.append(
            "no report is smallest, since " + _and(row["tied"]) + " are one exact side"
        )
    else:
        parts.append("no report is decidably smallest of " + _and(row["undecided_among"]))
    return f"At n = {row['n']} the certificate is " + "; ".join(parts) + "."


def register_plan(packet: Path) -> dict[str, Any]:
    """The entries the coordinator will need, derived from the packet; written nowhere.

    ``T-NNN`` is a placeholder: an id is its row's position, taken in the registering commit.
    """
    declaration = load_declaration(packet)
    register = declaration["register"]
    certificates = read_facts(packet)
    every = check_claims(packet, certificates)["results"]
    rows = [row for row in every if row["requested"]]
    others = [row["n"] for row in every if not row["requested"]]
    positives = check_certification(packet, certificates=certificates)
    _declaration, facts = replayed_facts(packet, certificates)
    parts = receipt_parts(packet, facts)
    record = {"cases": [row for part, _ in parts for row in part["cases"]]}
    receipts = [packet / RECEIPT] if len(parts) == 1 else [packet / shard(n) for n in facts]
    source = acquisition(packet)
    derived = {row["n"]: row["fact"] for row in declaration["certificates"] if "fact" in row}
    kept = (
        "kept as derived exact facts, no upstream byte retained"
        if derived
        else "retained as the source wrote them"
    )
    inside = [row for row in rows if row["n"] <= HORIZON]
    beyond = [row for row in rows if row["n"] > HORIZON]
    dated = {row["n"]: row["first_committed"][:10] for row in declaration["certificates"]}
    replay = _replay(positives, record)

    def states(group: list[dict[str, Any]]) -> str:
        return _and([f"s({r['n']}) <= {claim_value(Fraction(r['exact_side']))}" for r in group])

    # A release that requests only counts beyond the horizon has no in-horizon side, so no
    # register entry: its plan is the evidence, the source row and the beyond-horizon rows.
    claim = ""
    if inside:
        claim = (
            f"{_count_word(len(inside))} complete rational source certificates report finite "
            "upper-bound "
            f"improvements at the exact sides they state: {states(inside)}. Complete native "
            "feasibility outcomes are retained separately; the selected standing cases are "
            "unchanged pending independent review and record review."
        )
        if len(inside) == 1:
            claim = (
                "One complete rational source certificate reports a finite upper-bound "
                f"improvement at the exact side it states: {states(inside)}. Complete native "
                "feasibility outcomes are retained separately; the selected standing case is "
                "unchanged pending independent review and record review."
            )
        if beyond:
            claim += (
                f" The same release states {states(beyond)}, beyond the case corpus; the "
                "source register tracks those as beyond-horizon rows."
            )
        claim += f"\n\n{register['source_checks']}\n\n{register['credit']}"
    below_by = [Fraction(row["case"]["difference"]) for row in inside]
    packet_path = packet.relative_to(REPO).as_posix()
    local = packet.relative_to(ROOT).as_posix()
    parents = {PurePosixPath(row["path"]).parent for row in declaration["certificates"]}
    folder = parents.pop() if len(parents) == 1 else PurePosixPath()
    shared = (
        "The two maintained routes, the sqpack rational witness verifier and the independent "
        "rational corner checker, share certificate parsing, half-angle conversion, Fraction "
        "arithmetic and the separating-axis method. No two independent methods, human "
        "oversight or optimality is claimed."
    )
    rationale = ""
    if inside:
        rationale = (
            f"A smaller finite construction side at n = {inside[0]['n']}, "
            f"{_sci(below_by[0])} below the case ceiling"
            if len(inside) == 1
            else f"Smaller finite construction sides at n = "
            f"{_and([str(row['n']) for row in inside])}, {_sci(min(below_by))} to "
            f"{_sci(max(below_by))} below the case ceilings"
        ) + "; no lower bound or optimum."
    result = {
        "id": "T-NNN",
        "kind": "upper-bound",
        "registered": declaration["read_on"],
        "headline": register["headline"],
        "claim": claim,
        "scope": {"n_values": [row["n"] for row in inside]},
        "verification": "V0",
        "confirmation": "C0",
        "significance": {
            "score": register["significance"],
            "rationale": rationale,
            "scored": declaration["read_on"],
            "by": f"{register['bead']} {declaration['author']} import",
        },
        "novelty": "previously-published",
        "attribution": {
            "source_keys": [declaration["source_key"]],
            "published": max((dated[row["n"]] for row in inside), default=""),
        },
        "evidence": [declaration["report_evidence"]],
        "artifacts": [
            f"{packet_path}/README.md",
            f"{packet_path}/{CLAIMS.as_posix()}",
            *(
                f"{packet_path}/{derived[row['n']]}.gz"
                if row["n"] in derived
                else f"{source['archived_path']}/{row['certificate']}"
                for row in inside
            ),
            *(path.relative_to(REPO).as_posix() for path in receipts),
            "packing/devtools/upper_bound_reports.py",
        ],
        "controls": ["packing/tests/test_upper_bound_reports.py"],
        "notes": (
            f"{replay}\n\n"
            + " ".join(comparison(row) for row in rows)
            + (
                f"\n\nThe same commit holds {_many(len(others), 'further certificate')} the "
                f"issue does not name, at n = {_and([str(n) for n in others])}; the packet's "
                "claim record compares "
                + (
                    "it with its case, and it is an import of its own."
                    if len(others) == 1
                    else "each with its case, and each is an import of its own."
                )
                if others
                else ""
            )
            + f"\n\nThe source's own checkers were not run here. {shared}"
        ),
        "next_rung": register["next_rung"],
    }
    evidence = {
        "id": declaration["report_evidence"],
        "claim": "upper-bound",
        "scope": {"n_values": [row["n"] for row in rows]},
        "assurance": "reported",
        "reported_method": "exact-algebraic",
        "performed_by": "source-author",
        "relationship_to_generator": "same-implementation",
        "origin": "external",
        "novelty": "previously-published",
        "source_key": declaration["source_key"],
        "certificate": (
            f"{packet_path}/{FACTS}/"
            if derived
            else f"{(PurePosixPath(source['archived_path']) / folder).as_posix()}/"
        ),
        "replay_status": "not-attempted",
        "verifiers": [],
        "source_reviewed": declaration["read_on"],
        "limitations": (
            "This atom records the source author's report of "
            f"{_many(len(rows), 'exact rational certificate')} at "
            f"{source['source_commit'][:7]}. {replay} Independent review and "
            "confirmation remain pending. The source's own checkers were not run here. "
            f"{shared}"
        ),
    }
    coverage: dict[str, Any] = {
        "id": packet.name,
        "title": register["title"],
        "role": "source-repository",
        "url": f"{source['source_url']}/tree/{source['source_commit']}",
        "local": f"{local}/",
        "source_key": declaration["source_key"],
        "scope": {"n_values": [row["n"] for row in rows]},
        "reviewed": declaration["read_on"],
        "source_date": max(dated.values()),
        "disposition": "current-report",
        "replay_disposition": "case-specific",
        "represented_by": [
            "frontier/results.yaml" if inside else f"{local}/README.md",
            f"{local}/{CLAIMS.as_posix()}",
        ],
        "evidence": [declaration["report_evidence"]],
        "notes": (
            f"{'The' if len(rows) == 1 else 'All'} {_many(len(rows), 'complete certificate')} "
            f"{'is' if len(rows) == 1 else 'are'} {kept}, "
            f"{'admitted' if len(rows) == 1 else 'each admitted'} only where its "
            "exact side equals, or rounds up to, the side its source prints. "
            + (
                "T-NNN records the in-horizon report. "
                if inside
                else "Every requested count lies beyond the case corpus, so no register entry "
                "records them; each is a beyond-horizon row. "
            )
            + f"All {len(record['cases'])} native jobs have full outcomes. "
            "No selected override or superseded claim is created at this source-only stage; "
            "current cases and earlier source ownership remain unchanged."
        ),
    }
    if beyond:
        coverage["claims_record"] = f"{local}/{BEYOND.as_posix()}"
    bibliography = {
        "key": declaration["source_key"],
        "authors": register["bibliography"]["authors"],
        "year": int(source["committed_utc"][:4]),
        "venue": "GitHub",
        "dated": source["committed_utc"][:10],
        "lineage": register["bibliography"]["lineage"],
        "credit": register["bibliography"]["credit"],
        "short_credit": register["bibliography"]["short_credit"],
        "note": register["bibliography"]["note"],
    }
    readme = (
        f"**{declaration['source_key']}**: {declaration['author']}'s exact rational "
        f"{'certificate' if len(rows) == 1 else 'certificates'} for n = "
        f"{_and([str(row['n']) for row in rows])}, pinned at "
        f"`{source['source_commit']}`, {kept}; [packet](web/{packet.name}/README.md). Both "
        "project "
        f"exact routes accept {'the' if len(positives) == 1 else 'all'} "
        f"{_many(len(positives), 'replayed certificate')} and refuse "
        f"{'both' if len(positives) == 1 else f'all {2 * len(positives)}'} controls."
    )
    if inside:
        readme += (
            " T-NNN records the in-horizon "
            f"{'side' if len(inside) == 1 else 'sides'} at V0/C0, "
            "pending independent review and adoption."
        )
    if beyond:
        readme += (
            f" The n = {_and([str(row['n']) for row in beyond])} sides lie beyond the case "
            "corpus and are tracked as beyond-horizon rows."
        )
    plan: dict[str, Any] = {"results.yaml": result} if inside else {}
    return plan | {
        "evidence.yaml": evidence,
        "source-coverage.yaml": {
            "sources": [coverage],
            "beyond_horizon_claims": [
                {
                    "n": row["n"],
                    "source_id": packet.name,
                    "claim": "upper-bound",
                    "value": row["offered_side"],
                    "assurance": "reported",
                    "disposition": "tracked-outside-case-corpus",
                    "bead": register["bead"],
                }
                for row in beyond
            ],
        },
        "bibliography.yaml": bibliography,
        "resources/README.md": readme,
    }


# --------------------------------------------------------------------------- command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("packet", help="the packet's directory name under resources/web/")
    sub = parser.add_subparsers(dest="action", required=True)
    derivation = sub.add_parser("derive")
    derivation.add_argument("--checkout", type=Path, required=True)
    derivation.add_argument("--check", action="store_true")
    derivation.add_argument("--assets", type=Path)
    claims = sub.add_parser("check-claims")
    claims.add_argument("--write", action="store_true")
    campaign = sub.add_parser("certify")
    campaign.add_argument("--jobs-dir", type=Path, required=True)
    campaign.add_argument("--workers", type=int, default=MAX_WORKERS)
    campaign.add_argument("--timeout", type=int, default=JOB_TIMEOUT)
    campaign.add_argument("--finished", action="store_true")
    check = sub.add_parser("check")
    check.add_argument("--n", type=int, nargs="+")
    check.add_argument("--replay", action="store_true")
    sub.add_parser("register-plan")
    job = sub.add_parser("decide-job")
    job.add_argument("--n", type=int, required=True)
    job.add_argument("--control", choices=JOBS, required=True)
    job.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    packet = packet_path(args.packet)
    if args.action == "derive":
        rows = derive(packet, args.checkout, check=args.check, assets=args.assets)
        verb = "match the checkout" if args.check else "written"
        print(f"{len(rows)} derived facts {verb}; their Compressed Files rows:")
        for row in rows:
            print(row.markdown())
    elif args.action == "check-claims":
        if args.write:
            write_claims(packet)
        print(_json_text(check_claims(packet)), end="")
    elif args.action == "certify":
        positives = certify(
            packet,
            args.jobs_dir,
            workers=args.workers,
            timeout=args.timeout,
            finished=args.finished,
        )
        print(_json_text(margins(positives)), end="")
    elif args.action == "check":
        positives = check_certification(packet, args.n, replay=args.replay)
        print(_json_text(margins(positives)), end="")
        print(f"{len(positives)} certificates and {len(positives) * len(JOBS)} jobs admitted")
    elif args.action == "register-plan":
        plan = register_plan(packet)
        print(yaml.safe_dump(plan, sort_keys=False, allow_unicode=True, width=100), end="")
    else:
        decide_job(packet, args.n, args.control, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
