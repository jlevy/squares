"""Import a report of rational upper-bound certificates by another author, from its packet.

Every upper-bound import since #432 wrote its own report module around the same steps.
This module does them for any packet under ``packing/resources/web/`` that carries an
import declaration, ``acquisition/report.json`` (`Declaration`), beside the custody
declaration ``devtools.acquire_source`` writes the packet from:

- **custody.** ``read_facts`` admits nothing until ``acquire_source.check`` passes, so
  every certificate it reads is a retained file bound to its upstream blob;
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
  ``receipts/exact-certification.json.xz``; ``check`` admits the receipt, and ``check
  --replay`` decides it again;
- **registration.** ``register-plan`` prints, and writes nowhere, the register, evidence,
  coverage, bibliography and resources entries the ``requested`` counts need. A
  certificate the issue does not name is an import of its own (``result-import.md``, stage
  1), compared here and registered by none of these entries.

No source program runs. A finite construction certifies an upper bound and nothing more:
no KKT, local-minimum, rigidity, novelty or optimality statement is replayed here.

From ``packing/``, with the project interpreter::

    python -m devtools.upper_bound_reports PACKET check-claims [--write]
    python -m devtools.upper_bound_reports PACKET certify --jobs-dir SCRATCH/jobs --workers 2
    python -m devtools.upper_bound_reports PACKET check [--n N ...] [--replay]
    python -m devtools.upper_bound_reports PACKET register-plan

**Adding a format.** An adapter is a function ``(raw, n, options) -> Certificate`` (the
`Adapter` type) that reads one retained file's bytes for count ``n`` and returns the
exact certificate, centres in ``[0, S]^2`` and ``t = tan(theta/2)``. ``options`` is the
row's declared ``options`` as a mapping of strings, and an adapter refuses any it does not
read. Add it to `ADAPTERS` under a new name and declare that name as a row's ``format``;
nothing else changes. A declared-dilation reader of decimal poses (#470) is such an
adapter: it takes its dilation and its rationalisation as options, and the side it
returns, like any other, is admitted only if it rounds up to the side the report prints.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from collections.abc import Callable, Mapping
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from fractions import Fraction
from pathlib import Path, PurePosixPath
from typing import Any, NamedTuple, NotRequired, TypedDict, cast

import yaml
from strif import atomic_output_file

from devtools import acquire_source
from devtools import check_source_coverage as coverage_check
from devtools import couzo_followup_reports as couzo_followup
from devtools import couzo_refinement_reports as couzo_451
from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools import evand_hunt_reports as evand_hunt
from devtools import gupta_refinement_reports as gupta
from devtools import refinement_packets as rehwaldt
from devtools import ryxu_arrangement_reports as ryxu
from devtools import squish_followup_packets as squish_update
from devtools import squish_second_update_packets as squish_second
from devtools import squish_upper_bound_packets as squish_first
from devtools.retained_data import read_retained_bytes
from sqpack.yamlio import safe_load

MODULE = "devtools.upper_bound_reports"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
WEB = ROOT / "resources/web"
DECLARATION = Path("acquisition/report.json")
CLAIMS = Path("acquisition/claims.json")
BEYOND = Path("acquisition/beyond-horizon-claims.json")
RECEIPT = Path("receipts/exact-certification.json.xz")
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
MAX_SOURCE_BYTES = 1_000_000
MAX_LITERAL_CHARS = 1024
#: How a printed side was rounded: up, as the report states, or not stated.
ROUNDINGS = ("up", "unstated")
THIS = "this certificate"
_PRINTED = re.compile(r"[0-9]+\.[0-9]+")
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


class SamePacking(TypedDict):
    """Another retained file of the same count, which must state the identical packing."""

    path: str
    format: str


class CertificateRow(TypedDict):
    """One certificate the issue reports.

    - ``path``: its upstream path under the packet's archived directory.
    - ``format``: the adapter that reads it (`ADAPTERS`).
    - ``offered``: the side the issue prints, as printed.
    - ``printed_in`` (optional): where ``offered`` is printed, for a certificate the issue
      does not name; its source's own table.
    - ``first_committed``: the UTC time of the first commit holding these bytes, which
      dates the claim (``attribution.published``).
    - ``options`` (optional): what the adapter reads besides the bytes.
    - ``same_packing`` (optional): other retained files that state the same packing.
    """

    n: int
    path: str
    format: str
    offered: str
    first_committed: str
    printed_in: NotRequired[str]
    options: NotRequired[list[Option]]
    same_packing: NotRequired[list[SamePacking]]


class House(TypedDict):
    """The case record's upper bound at an in-horizon count, as it stood when read.

    - ``reader``: the `HOUSES` key that rebuilds its exact side from its own packet.
    - ``source_key``, ``holders``, ``result`` (optional): its source key, its credit as
      the case prints it, and the register entry that holds it.
    - ``reported_value``, ``verified_value``: the two lanes' values as printed.
    - ``evidence``: the verified lane's evidence.
    """

    n: int
    reader: str
    source_key: str
    holders: str
    result: NotRequired[str]
    reported_value: str
    verified_value: str
    evidence: list[str]


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
    for row in declaration["certificates"]:
        _require(row["format"] in ADAPTERS, f"n={row['n']}: unknown format {row['format']}")
        _require(_PRINTED.fullmatch(row["offered"]), f"n={row['n']}: offered side")
        _require(_UTC.fullmatch(row["first_committed"]), f"n={row['n']}: first_committed")
        for other in row.get("same_packing", []):
            _require(other["format"] in ADAPTERS, f"n={row['n']}: unknown format")
    _require(
        [house["n"] for house in declaration["houses"]] == [n for n in counts if n <= HORIZON],
        "the houses must be exactly the in-horizon counts, in order",
    )
    for house in declaration["houses"]:
        _require(house["reader"] in HOUSES, f"n={house['n']}: no reader {house['reader']}")
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
    rows = []
    for index, square in enumerate(squares, start=1):
        _require(type(square) is list and len(square) == 3, f"n={n} square {index}: x y t")
        x, y, t = (_literal(item, f"n={n} square {index}") for item in square)
        rows.append((x, y, t))
    return _certificate(n, _literal(value["s_exact"], f"n={n} side"), rows)


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


#: Every certificate format a declaration may name. The module docstring says how to add one.
ADAPTERS: dict[str, Adapter] = {
    "evand-cert": evand_cert,
    "squish-json": squish_json,
    "centred-json": centred_json,
}


def parse_certificate(
    raw: bytes, n: int, form: str, options: Mapping[str, str] | None = None
) -> legacy.Certificate:
    """One retained file through its declared adapter."""
    _require(form in ADAPTERS, f"unknown certificate format {form!r}")
    return ADAPTERS[form](raw, n, {} if options is None else options)


def admit(certificate: legacy.Certificate, offered: str) -> None:
    """Refuse a side that neither equals the printed side nor rounds up to it there."""
    _require(_PRINTED.fullmatch(offered), f"n={certificate.n}: offered side is not a decimal")
    places = len(offered.partition(".")[2])
    printed = Fraction(Decimal(offered))
    rounded = Fraction(Decimal(legacy.ceiling_decimal(certificate.side, places)))
    _require(
        printed in {certificate.side, rounded},
        f"n={certificate.n}: exact side {legacy.literal(certificate.side)} does not round up "
        f"to the printed {offered} at {places} places",
    )


def _options(row: CertificateRow) -> dict[str, str]:
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


def read_facts(packet: Path) -> dict[int, legacy.Certificate]:
    """Admit every declared certificate once the packet's custody check passes."""
    ensure_private(packet)
    declaration = load_declaration(packet)
    source = REPO / acquisition(packet)["archived_path"]
    certificates = {}
    for row in declaration["certificates"]:
        n = row["n"]
        raw = _read(source, row["path"])
        certificate = parse_certificate(raw, n, row["format"], _options(row))
        admit(certificate, row["offered"])
        for other in row.get("same_packing", []):
            copy = parse_certificate(_read(source, other["path"]), n, other["format"])
            _require(copy == certificate, f"n={n}: {other['path']} states another packing")
        certificates[n] = certificate
    return certificates


# --------------------------------------------------------------------------- houses


def grid_side(n: int) -> Fraction:
    """The trivial bound ``ceil(sqrt(n))``: a grid of that side holds ``n`` squares."""
    _require(type(n) is int and n >= 1, "count must be positive")
    return Fraction(math.isqrt(n - 1) + 1)


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
    "[Couzo exact refinements 2026-10-08]": lambda n: couzo_451.read_facts()[n].side,
    "[Gupta rational refinements 2026-10-08]": lambda n: gupta.read_fact(n).side,
    "[SQUISH second update 2026-10-07]": lambda n: Fraction(squish_second.read_fact(n)["side"]),
    "[SQUISH ten packings 2026-10-07]": lambda n: Fraction(squish_first.read_fact(n)["side"]),
    "[ry-xu square packing 2026]": lambda n: ryxu.read_fact(n).side,
    "[Daniel new arrangements 2026-10-07]": lambda n: kernel.read_fact(n).side,
    "[Daniel record hunt 2026-10-09]": lambda n: evand_hunt.read_facts()[n].side,
    "[Couzo follow-up refinements 2026-10-08]": lambda n: couzo_followup.read_facts()[n].side,
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

    ``u`` is one unit in the last printed place.
    """
    _require(_PRINTED.fullmatch(printed) and rounding in ROUNDINGS, "printed side, rounding")
    value = Fraction(Decimal(printed))
    unit = Fraction(1, 10 ** len(printed.partition(".")[2]))
    if rounding == "up":
        return Span(value - unit, value, open_low=True, open_high=False)
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
        for lane in ("reported_value", "verified_value"):
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
    current = coverage_check.current_beyond_horizon(coverage)
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


# --------------------------------------------------------------------------- replay


def replayed_facts(packet: Path) -> tuple[Declaration, dict[int, legacy.Certificate]]:
    """The declaration and the admitted certificates of its ``replayed`` roster, in order."""
    certificates = read_facts(packet)
    declaration = load_declaration(packet)
    return declaration, {n: certificates[n] for n in declaration["replayed"]}


def check_certification(
    packet: Path, numbers: list[int] | None = None, *, replay: bool = False
) -> dict[int, Any]:
    """Admit the retained receipt; with ``replay``, decide the selected counts again."""
    declaration, facts = replayed_facts(packet)
    selected = list(facts) if numbers is None else numbers
    _require(
        selected
        and all(type(n) is int for n in selected)
        and len(set(selected)) == len(selected)
        and not set(selected) - set(facts),
        "empty, repeated or unknown replay selection",
    )
    ensure_private(packet / RECEIPT)
    record = kernel.read_xz(packet / RECEIPT)
    profile = _profile(declaration)
    positives = kernel.validate_receipt(
        record, facts, receipt_format=declaration["receipt_format"], **profile
    )
    if replay:
        kernel.replay_receipt(record, facts, selected, **profile)
    return positives


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


def certify(
    packet: Path, directory: Path, *, workers: int = MAX_WORKERS, timeout: int = JOB_TIMEOUT
) -> dict[int, Any]:
    """Run every job of every count in a fresh directory; write the receipt once all pass."""
    _require(
        type(workers) is int
        and 1 <= workers <= MAX_WORKERS
        and type(timeout) is int
        and 1 <= timeout <= JOB_TIMEOUT,
        "invalid bounded worker/deadline selection",
    )
    ensure_private(packet / RECEIPT)
    declaration, facts = replayed_facts(packet)
    _require(not directory.exists(), "native job directory must be a fresh attempt")
    directory.mkdir(parents=True)
    jobs = [(n, control) for n in facts for control in JOBS]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(run_job, packet, job, directory, timeout) for job in jobs]
        rows = [future.result() for future in futures]
    record = {"format": declaration["receipt_format"], "routes": list(ROUTES), "cases": rows}
    positives = kernel.validate_receipt(
        record, facts, receipt_format=declaration["receipt_format"], **_profile(declaration)
    )
    kernel.save_xz(packet / RECEIPT, record)
    return positives


def decide_job(packet: Path, n: int, control: str, output: Path) -> None:
    """The child's side of `run_job`: decide one job and write its validated row."""
    declaration, facts = replayed_facts(packet)
    _require(n in facts and control in JOBS, "job outside the declared roster")
    _require(not output.exists(), "refusing to overwrite a deciding job")
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


def _replay(positives: dict[int, Any], record: Mapping[str, Any]) -> str:
    summary = receipt_summary(record)
    found = margins(positives).values()
    wall = min(Fraction(row["exact_verify_containment_clearance"]) for row in found)
    gap = min(Fraction(row["exact_verify_best_pair_gap"]) for row in found)
    return (
        f"A separate complete repository replay is retained for n = "
        f"{_and([str(n) for n in positives])}: {len(positives)} positives and "
        f"{2 * len(positives)} duplicate-square and outside-container controls passed their "
        f"required outcomes on both routes, {summary['pair_decisions']} pair decisions; summed "
        f"over the {summary['jobs']} jobs, the receipt records {summary['route_cpu_seconds']} "
        f"route CPU seconds and {summary['job_wall_seconds']} job wall seconds, the longest "
        f"job {summary['longest_job_seconds']} seconds. Every positive clears every wall by "
        f"at least {_sci(wall)} and every pair by at least {_sci(gap)}."
    )


def _comparison(row: Mapping[str, Any]) -> str:
    """One count's frozen comparison, as a sentence of the register's notes."""
    if row["case"] is None:
        grid = Fraction(row["grid_side"]) - Fraction(row["exact_side"])
        parts = [f"beyond the horizon, with no case record, and {_sci(grid)} below the grid"]
    else:
        case = row["case"]
        held = f"{case['holders']}, {case['result']}" if "result" in case else case["holders"]
        parts = [
            f"{case['relation']} the case's ceiling ({held}) by {_sci(case['difference'])}"
        ]
    for other in row["pending"]:
        decided = other["relation"] in {"below", "above"}
        by = f" by {_sci(abs(Fraction(other['difference'])))}" if decided else ""
        parts.append(f"{other['relation']} {other['report']} ({other['holders']}){by}")
    if row["smallest"]:
        parts.append(f"smallest: {row['smallest']}")
    else:
        parts.append("no report is decidably smallest of " + _and(row["undecided_among"]))
    return f"At n = {row['n']} the certificate is " + "; ".join(parts) + "."


def register_plan(packet: Path) -> dict[str, Any]:
    """The entries the coordinator will need, derived from the packet; written nowhere.

    ``T-NNN`` is a placeholder: an id is its row's position, taken in the registering commit.
    """
    declaration = load_declaration(packet)
    register = declaration["register"]
    every = check_claims(packet, read_facts(packet))["results"]
    rows = [row for row in every if row["requested"]]
    others = [row["n"] for row in every if not row["requested"]]
    positives = check_certification(packet)
    record = kernel.read_xz(packet / RECEIPT)
    source = acquisition(packet)
    inside = [row for row in rows if row["n"] <= HORIZON]
    beyond = [row for row in rows if row["n"] > HORIZON]
    dated = {row["n"]: row["first_committed"][:10] for row in declaration["certificates"]}
    replay = _replay(positives, record)

    def states(group: list[dict[str, Any]]) -> str:
        return _and([f"s({r['n']}) <= {claim_value(Fraction(r['exact_side']))}" for r in group])

    claim = (
        f"{len(inside)} complete rational source certificates report finite upper-bound "
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
            f" The same release states {states(beyond)}, beyond the case corpus; the source "
            "register tracks those as beyond-horizon rows."
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
            "rationale": (
                f"Smaller finite construction sides at n = "
                f"{_and([str(row['n']) for row in inside])}, {_sci(min(below_by))} to "
                f"{_sci(max(below_by))} below the case ceilings; no lower bound or optimum."
            ),
            "scored": declaration["read_on"],
            "by": f"{register['bead']} {declaration['author']} import",
        },
        "novelty": "previously-published",
        "attribution": {
            "source_keys": [declaration["source_key"]],
            "published": max(dated[row["n"]] for row in inside),
        },
        "evidence": [declaration["report_evidence"]],
        "artifacts": [
            f"{packet_path}/README.md",
            f"{packet_path}/{CLAIMS.as_posix()}",
            *(f"{source['archived_path']}/{row['certificate']}" for row in inside),
            f"{packet_path}/{RECEIPT.as_posix()}",
            "packing/devtools/upper_bound_reports.py",
        ],
        "controls": ["packing/tests/test_upper_bound_reports.py"],
        "notes": (
            f"{replay}\n\n"
            + " ".join(_comparison(row) for row in rows)
            + (
                f"\n\nThe same commit holds {len(others)} further certificates the issue does "
                f"not name, at n = {_and([str(n) for n in others])}; the packet's claim "
                "record compares each with its case, and each is an import of its own."
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
        "certificate": f"{(PurePosixPath(source['archived_path']) / folder).as_posix()}/",
        "replay_status": "not-attempted",
        "verifiers": [],
        "source_reviewed": declaration["read_on"],
        "limitations": (
            f"This atom records the source author's report of {len(rows)} exact rational "
            f"certificates at {source['source_commit'][:7]}. {replay} Independent review and "
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
        "represented_by": ["frontier/results.yaml", f"{local}/{CLAIMS.as_posix()}"],
        "evidence": [declaration["report_evidence"]],
        "notes": (
            f"All {len(rows)} complete certificates are retained, each admitted only where "
            "its exact side rounds up to the side the issue prints. T-NNN records the "
            f"in-horizon report. All {len(record['cases'])} native jobs have full outcomes. "
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
        f"certificates for n = {_and([str(row['n']) for row in rows])}, pinned at "
        f"`{source['source_commit']}`; [packet](web/{packet.name}/README.md). Both project "
        f"exact routes accept every certificate and refuse all {2 * len(rows)} controls. "
        "T-NNN records the in-horizon sides at V0/C0, pending independent review and adoption."
    )
    if beyond:
        readme += (
            f" The n = {_and([str(row['n']) for row in beyond])} sides lie beyond the case "
            "corpus and are tracked as beyond-horizon rows."
        )
    return {
        "results.yaml": result,
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
    claims = sub.add_parser("check-claims")
    claims.add_argument("--write", action="store_true")
    campaign = sub.add_parser("certify")
    campaign.add_argument("--jobs-dir", type=Path, required=True)
    campaign.add_argument("--workers", type=int, default=MAX_WORKERS)
    campaign.add_argument("--timeout", type=int, default=JOB_TIMEOUT)
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
    if args.action == "check-claims":
        if args.write:
            write_claims(packet)
        print(_json_text(check_claims(packet)), end="")
    elif args.action == "certify":
        positives = certify(packet, args.jobs_dir, workers=args.workers, timeout=args.timeout)
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
