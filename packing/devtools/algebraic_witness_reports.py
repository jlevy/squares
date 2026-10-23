"""Replay a packet's algebraic-number-field witnesses on sqpack's exact route.

`devtools.upper_bound_reports` imports rational certificates and decides each on the two
maintained exact routes over Q. PR #574 also states certificates whose coordinates lie in
real algebraic number fields, of degree 2 to 8. One maintained route reads them:
`sqpack.witness.exact_verify`, which builds every square in its witness's field
(`sqpack.field`) and decides each unit-square identity, wall and pair by exact signs. The
independent rational corner checker reads rational corners only, and no second route over
a number field is maintained here, so every receipt this module writes records one route
and says so.

The packet declares the witnesses in ``acquisition/algebraic.json`` (`Declaration`):

- ``derive`` reads each witness from its release asset through the manifest the packet
  pins, as `upper_bound_reports.derive` does, holds it to the witness schema, its count and
  its declared field degree, and writes the derived fact ``facts/alg-n-NNN.yaml.gz``: the
  witness's field, side and squares exactly, under this packet's id, claim and source
  record. No upstream byte is retained; ``--check`` compares the facts again;
- ``derive-forms`` does the same for a witness the packet declares as an exact form in
  another format, retained in its archived source and bound to the digest its subtree
  manifest pins (`FORMS`): Evan Daniel's ``n-N.minpoly.json.gz`` of issue 639 (T-193),
  whose squares are a centre in the field and a half-angle tangent `u`, written here as
  the centre and the basis ``((1 - u^2)/(1 + u^2), 2u/(1 + u^2))`` turned by the form's
  quarter turns, computed exactly in the field;
- ``compare`` builds ``acquisition/algebraic-claims.json``: each side, enclosed exactly,
  against the case record's verified and reported upper bounds held exactly
  (`regularize_evand`) and against each pending report the declaration names;
- ``certify`` decides a positive, a duplicate-square and an outside-container job for each
  count of the ``replayed`` roster, each in its own child process, and writes one receipt
  per count, ``receipts/algebraic-route1-nNNN.json.xz``;
- ``check`` admits the receipts, and ``check --replay`` decides the jobs again and requires
  the same outcomes.

A finite construction certifies an upper bound and nothing more. From ``packing/``::

    python -m devtools.algebraic_witness_reports PACKET derive --checkout C --assets D [--check]
    python -m devtools.algebraic_witness_reports PACKET derive-forms [--check]
    python -m devtools.algebraic_witness_reports PACKET compare [--write]
    python -m devtools.algebraic_witness_reports PACKET certify --jobs-dir DIR [--n N ...]
    python -m devtools.algebraic_witness_reports PACKET check [--n N ...] [--replay]
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import re
import subprocess
import sys
import time
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Any, NotRequired, TypedDict, cast

import yaml
from strif import atomic_output_file

from devtools import acquire_source, retained_data
from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from devtools.retained_data import read_retained_bytes
from sqpack.field import FieldElement, NumberField
from sqpack.witness import (
    WitnessError,
    exact_verify,
    materialize_exact_witness,
    validate_witness_document,
    witness_document,
    witness_envelope,
)
from sqpack.yamlio import load_yaml

if TYPE_CHECKING:
    from devtools.regularize_evand import VerifiedBound

MODULE = "devtools.algebraic_witness_reports"
REPO = reports.REPO
DECLARATION = Path("acquisition/algebraic.json")
CLAIMS = Path("acquisition/algebraic-claims.json")
DECLARATION_FORMAT = "algebraic-witness-declaration-v1"
CLAIMS_FORMAT = "algebraic-witness-claims-v1"
FACT_SCHEMA = reports.FACT_SCHEMA
WITNESS_SCHEMA = reports.WITNESS_SCHEMA
JOBS = kernel.JOBS
ROUTE = "exact_verify"
#: The digits each side is enclosed to before it is compared, and the most tried.
DIGITS = (60, 120, 240)
DISPLAY_PLACES = 40
_FRACTION = re.compile(r"[1-9][0-9]*/[1-9][0-9]*")
_RATIONAL_SIDE = re.compile(r"[0-9]+(?:/[1-9][0-9]*)?")
_DECIMAL_SIDE = re.compile(r"[0-9]+\.[0-9]+")
_UTC = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d(:\d\d)?Z")


class ReportError(reports.ReportError):
    """Refuse incomplete custody, an unadmitted witness, a changed claim or receipt."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ReportError(message)


class Witness(TypedDict):
    """One algebraic witness of the release, in one of two places.

    - ``path``: the witness's path inside its release asset, as ``archive.member`` names it,
      or the upstream path of a retained exact form, as the subtree manifest names it.
    - ``archive``: where a Witness/v2 is (`upper_bound_reports.ArchiveMember`); or
    - ``form``: the format of an exact form the packet retains at ``path`` under its
      archived source, read by `FORMS`.
    - ``fact``: the packet-relative derived fact, ``facts/alg-n-NNN.yaml``.
    - ``degree``: the degree of the witness's field, which its minimal polynomial must have.
    - ``first_committed``: the UTC time of the first pinned commit that binds the asset.
    """

    n: int
    path: str
    archive: NotRequired[reports.ArchiveMember]
    form: NotRequired[str]
    fact: str
    degree: int
    first_committed: str


class Pending(TypedDict):
    """Another report at the same count: its printed side and how it was rounded, or its
    exact rational side where that is retained (``exact``, a fraction)."""

    n: int
    report: str
    url: str
    holders: str
    printed: NotRequired[str]
    rounding: NotRequired[str]
    exact: NotRequired[str]


class Declaration(TypedDict):
    """``acquisition/algebraic.json``: the algebraic witnesses, the roster and the reports."""

    format: str
    issue: str
    author: str
    source_key: str
    receipt_format: str
    witness_prefix: str
    claim_limitations: str
    read_on: str
    read_at_main: str
    witnesses: list[Witness]
    replayed: list[int]
    pending: list[Pending]


def load_declaration(packet: Path) -> Declaration:
    """The packet's algebraic declaration, refused unless every part is well formed."""
    path = packet / DECLARATION
    reports.ensure_private(path)
    value: object = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=kernel.unique_object
    )
    shape: Any = Declaration
    problems = acquire_source.shape_problems(value, shape, DECLARATION.as_posix())
    _require(not problems, "; ".join(problems))
    declaration = cast("Declaration", value)
    _require(
        declaration["format"] == DECLARATION_FORMAT, "unknown algebraic declaration format"
    )
    counts = [row["n"] for row in declaration["witnesses"]]
    _require(counts and counts == sorted(set(counts)), "counts must be unique and ascending")
    roster = declaration["replayed"]
    _require(
        roster == sorted(set(roster)) and not set(roster) - set(counts),
        "replayed must be ascending, unique declared counts",
    )
    for row in declaration["witnesses"]:
        where = f"n={row['n']}"
        _require(
            ("archive" in row) != ("form" in row),
            f"{where}: a witness is a release-asset member or a retained exact form, not both",
        )
        if "archive" in row:
            reports.archive_spec(row["archive"], row["path"], where)
        else:
            _require(
                row.get("form") in FORMS and _plain(row["path"]),
                f"{where}: a retained exact form names a known format and a plain path",
            )
        fact = PurePosixPath(row["fact"])
        _require(
            fact.parent.as_posix() == reports.FACTS
            and fact.name == f"alg-n-{row['n']:03d}.yaml",
            f"{where}: an algebraic fact is facts/alg-n-NNN.yaml",
        )
        _require(type(row["degree"]) is int and row["degree"] >= 2, f"{where}: degree >= 2")
        _require(
            _UTC.fullmatch(row["first_committed"]) is not None,
            f"{where}: first_committed is a UTC time, YYYY-MM-DDTHH:MM[:SS]Z",
        )
    for item in declaration["pending"]:
        where = f"n={item['n']} {item['report']}"
        _require(item["n"] in counts, f"{where}: a pending report at an undeclared count")
        if "exact" in item:
            _require(
                _FRACTION.fullmatch(item.get("exact", "")) and "printed" not in item,
                f"{where}: an exact side is a fraction, alone",
            )
        else:
            reports.printed_span(item.get("printed", ""), item.get("rounding", ""))
    return declaration


# --------------------------------------------------------------------------- facts


def _validated(document: object, n: int) -> dict[str, Any]:
    """A witness held to this repository's schema whatever schema path it names."""
    _require(type(document) is dict, f"n={n}: not a witness document")
    metadata = cast("dict[str, Any]", document).get("softschema")
    _require(type(metadata) is dict, f"n={n}: not a witness document")
    try:
        return validate_witness_document(
            {
                **cast("dict[str, Any]", document),
                "softschema": {
                    **cast("dict[str, Any]", metadata),
                    "schema": "witness.schema.yaml",
                },
            },
            path=WITNESS_SCHEMA,
            fallback_schema=WITNESS_SCHEMA,
        )
    except WitnessError as error:
        raise ReportError(f"n={n}: not a valid witness: {error}") from error


def _geometry(witness: dict[str, Any], row: Witness) -> dict[str, Any]:
    """The witness's exact content, refused unless it is the declared count's field."""
    n = row["n"]
    scalar = witness["scalar"]
    _require(
        witness["n"] == n
        and witness["square_size"] == "1"
        and witness["coordinates"] == reports.CORNER_FRAME
        and witness["representation"] in {"center-basis", "corners"}
        and scalar.get("kind") == "algebraic-number-field"
        and len(scalar.get("minimal_polynomial", [])) == row["degree"] + 1,
        f"n={n}: not a degree-{row['degree']} field witness of {n} unit squares in the "
        "lower-left frame",
    )
    keys = ("center", "basis") if witness["representation"] == "center-basis" else ("corners",)
    return {
        "side": witness["side"],
        "representation": witness["representation"],
        "scalar": {
            "kind": "algebraic-number-field",
            "minimal_polynomial": scalar["minimal_polynomial"],
            "isolating_interval": scalar["isolating_interval"],
        },
        "squares": [
            {"id": index, **{key: square[key] for key in keys}}
            for index, square in enumerate(witness["squares"], start=1)
        ],
    }


def _plain(path: str) -> bool:
    relative = PurePosixPath(path)
    return (
        bool(path)
        and not relative.is_absolute()
        and ".." not in relative.parts
        and relative.as_posix() == path
    )


def _pinned_digest(packet: Path, path: str) -> str:
    """The SHA-256 the packet's subtree manifest pins for the upstream file at `path`."""
    source = json.loads((packet / acquire_source.RECORD).read_text(encoding="utf-8"))
    manifest = REPO / source["sources"][0]["subtree_manifest"]
    reports.ensure_private(manifest)
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, _, name = line.partition("  ")
        if name.removeprefix("./") == path:
            return digest
    raise ReportError(f"{path}: the packet's manifest pins no such upstream file")


def source_url(packet: Path, row: Witness) -> tuple[str, str]:
    """Where the row's witness is upstream, and the digest that binds it there."""
    record = json.loads((packet / acquire_source.RECORD).read_text(encoding="utf-8"))
    source = record["sources"][0]
    if "archive" not in row:
        url = f"{source['source_url']}/blob/{source['source_commit']}/{row['path']}"
        return url, _pinned_digest(packet, row["path"])
    pinned = {item["path"] for item in source["pinned_only"]}
    archive = row["archive"]
    _require(archive["manifest"] in pinned, f"n={row['n']}: the manifest is not pinned")
    url = (
        f"https://github.com/{archive['repository']}/releases/download/"
        f"{archive['tag']}/{archive['asset']}#{archive['member']}"
    )
    return url, archive["sha256"]


def fact_witness(
    packet: Path, declaration: Declaration, row: Witness, geometry: dict[str, Any]
) -> dict[str, Any]:
    """The derived fact: the geometry exactly, under this packet's id, claim and source."""
    record = json.loads((packet / acquire_source.RECORD).read_text(encoding="utf-8"))
    source = record["sources"][0]
    url, digest = source_url(packet, row)
    return {
        "id": f"{declaration['witness_prefix']}{row['n']:03d}",
        "n": row["n"],
        "side": geometry["side"],
        "square_size": "1",
        "representation": geometry["representation"],
        "scalar": geometry["scalar"],
        "coordinates": dict(reports.CORNER_FRAME),
        "squares": geometry["squares"],
        "claim": {
            "coordinate_provenance": "reported",
            "method": "exact-algebraic",
            "limitations": declaration["claim_limitations"],
        },
        "source": {
            "key": declaration["source_key"],
            "path": (packet / acquire_source.RECORD).relative_to(REPO).as_posix(),
            "url": url,
            "retrieved": record["retrieved_at_utc"][:10],
            "revision": source["source_commit"],
            "revision_sha256": digest,
        },
    }


def _write_fact(
    packet: Path,
    declaration: Declaration,
    row: Witness,
    geometry: dict[str, Any],
    *,
    check: bool,
) -> retained_data.Row:
    """Write, or with ``check`` compare, the row's derived fact from its geometry."""
    text = witness_document(
        fact_witness(packet, declaration, row, geometry), schema=FACT_SCHEMA
    )
    target = packet / row["fact"]
    stored = retained_data.compressed_path(target)
    _validated(load_yaml(text), row["n"])
    if check:
        reports.ensure_private(stored)
        _require(
            stored.is_file() and read_retained_bytes(stored) == text.encode(),
            f"n={row['n']}: the retained fact is not what its source derives",
        )
    else:
        target.parent.mkdir(exist_ok=True)
        stored.unlink(missing_ok=True)
        with atomic_output_file(target) as temporary:
            temporary.write_text(text, encoding="utf-8")
        retained_data.compress(target)
    return retained_data.describe(packet, stored, "receipt")


def derive(
    packet: Path, checkout: Path, assets: Path, *, check: bool = False
) -> list[retained_data.Row]:
    """Write, or with ``check`` compare, each algebraic fact from the pinned assets."""
    reports.ensure_private(packet)
    declaration = load_declaration(packet)
    reports.acquisition(packet)
    if problems := reports.checkout_problems(packet, checkout):
        raise ReportError("; ".join(problems))
    store = reports.ReleaseAssets(packet, checkout, assets)
    written = []
    for row in declaration["witnesses"]:
        if "archive" not in row:
            continue
        raw = store.member(row["archive"])
        try:
            document = load_yaml(raw.decode("utf-8"))
        except (UnicodeDecodeError, yaml.YAMLError) as error:
            raise ReportError(f"n={row['n']}: invalid witness YAML: {error}") from error
        geometry = _geometry(_validated(document, row["n"]), row)
        written.append(_write_fact(packet, declaration, row, geometry, check=check))
    return written


# --------------------------------------------------------------------- retained forms

#: The most bytes a retained exact form may decompress to: the largest form issue 639
#: retains, n = 172, is 1,404,617 bytes of JSON.
MAX_FORM_BYTES = 8_000_000


def _retained_form(packet: Path, source: acquire_source.Source, row: Witness) -> bytes:
    """The upstream bytes of a retained exact form, bound to the digest the manifest pins,
    from the packet's acquisition record `source` once its custody is checked."""
    path = REPO / source["archived_path"] / row["path"]
    reports.ensure_private(path)
    _require(path.is_file(), f"n={row['n']}: the exact form is not retained in the packet")
    raw = path.read_bytes()
    _require(
        hashlib.sha256(raw).hexdigest() == _pinned_digest(packet, row["path"]),
        f"n={row['n']}: the retained exact form differs from its pinned digest",
    )
    return raw


def _ratio(value: object, where: str) -> Fraction:
    _require(type(value) in (int, str), f"{where}: not a rational literal")
    try:
        return Fraction(cast("int | str", value))
    except (ValueError, ZeroDivisionError) as error:
        raise ReportError(f"{where}: not a rational literal: {error}") from error


def _coefficients(value: object, degree: int, where: str) -> list[Fraction]:
    """A field element's coefficients in the power basis, low degree first."""
    _require(
        type(value) is list and 1 <= len(cast("list[Any]", value)) <= degree,
        f"{where}: not an element of the degree-{degree} field",
    )
    return [_ratio(item, where) for item in cast("list[Any]", value)]


def evand_minpoly_geometry(raw: bytes, row: Witness) -> dict[str, Any]:
    """The exact geometry of one of Evan Daniel's ``n-N.minpoly.json.gz`` forms (issue 639).

    The form states a number field ``K = Q[t]/f``, ``f`` low degree first, with a rational
    interval about its root; every square's centre ``(x, y)`` and angle parameter ``u`` in
    ``K``, low degree first in the power basis, and a quarter-turn count ``m``; and the
    side ``S`` in ``K`` (``S.in_K``). Its checker reads the square's basis as ``R^m ((1 -
    u^2)/(1 + u^2), 2u/(1 + u^2))``, ``R`` the turn by 90 degrees, a unit square about the
    centre in the box ``[0, S]^2`` (``verify_exact.py``). This computes that basis exactly
    in the field and states each square by its centre and basis, as a centre-basis
    Witness/v2 does; a quarter turn draws the same square, and is applied all the same.
    """
    n = row["n"]
    try:
        text = gzip.decompress(raw)
        _require(len(text) <= MAX_FORM_BYTES, f"n={n}: the exact form is over its size limit")
        data = json.loads(text)
    except (OSError, EOFError, ValueError) as error:
        raise ReportError(f"n={n}: the exact form does not read: {error}") from error
    _require(type(data) is dict and data.get("n") == n, f"n={n}: the form is not this count's")
    form = cast("dict[str, Any]", data)
    _require(
        type(form.get("field")) is dict
        and type(form.get("S")) is dict
        and type(form.get("squares")) is list,
        f"n={n}: the form has no field, side or squares",
    )
    field_spec = cast("dict[str, Any]", form["field"])
    side_spec = cast("dict[str, Any]", form["S"])
    squares = cast("list[Any]", form["squares"])
    low_to_high = [int(_ratio(value, f"n={n} f")) for value in field_spec.get("f", [])]
    degree = len(low_to_high) - 1
    _require(
        degree == row["degree"], f"n={n}: the form's field is not of degree {row['degree']}"
    )
    interval = [
        _ratio(value, f"n={n} t_interval") for value in field_spec.get("t_interval", [])
    ]
    _require(len(interval) == 2 and interval[0] < interval[1], f"n={n}: no isolating interval")
    _require(len(squares) == n, f"n={n}: the form lists {len(squares)} squares")
    polynomial = list(reversed(low_to_high))
    field = NumberField(polynomial, (interval[0], interval[1]))
    one = field.rational(Fraction(1))

    def scalar(element: FieldElement) -> Any:
        return _scalar_text([Fraction(value) for value in element.coeffs])

    stated = []
    for index, square in enumerate(squares, start=1):
        where = f"n={n} square {index}"
        _require(type(square) is dict, f"{where}: not a square")
        pose = cast("dict[str, Any]", square)
        x, y, u = (field.element(_coefficients(pose.get(key), degree, where)) for key in "xyu")
        turns = pose.get("m")
        _require(type(turns) is int and 0 <= turns <= 3, f"{where}: m is a quarter-turn count")
        denominator = one + u * u
        cosine, sine = (one - u * u) / denominator, (u + u) / denominator
        for _turn in range(cast("int", turns)):
            cosine, sine = -sine, cosine
        stated.append(
            {
                "id": index,
                "center": [scalar(x), scalar(y)],
                "basis": [scalar(cosine), scalar(sine)],
            }
        )
    side = field.element(_coefficients(side_spec.get("in_K"), degree, f"n={n} S"))
    return {
        "side": scalar(side),
        "representation": "center-basis",
        "scalar": {
            "kind": "algebraic-number-field",
            "minimal_polynomial": [str(value) for value in polynomial],
            "isolating_interval": [str(end) for end in interval],
        },
        "squares": stated,
    }


#: The formats a retained exact form may be declared in, each with its reader.
FORMS: dict[str, Callable[[bytes, Witness], dict[str, Any]]] = {
    "evand-exact-minpoly-v1": evand_minpoly_geometry,
}


def derive_forms(packet: Path, *, check: bool = False) -> list[retained_data.Row]:
    """Write, or with ``check`` compare, each fact the packet declares as a retained form."""
    reports.ensure_private(packet)
    declaration = load_declaration(packet)
    # Custody is checked once, before any fact is written: a fact this writes is not yet
    # in the README's table of compressed files, which the check holds every one to.
    source = reports.acquisition(packet)
    written = []
    for row in declaration["witnesses"]:
        if "form" not in row:
            continue
        geometry = FORMS[row["form"]](_retained_form(packet, source, row), row)
        written.append(_write_fact(packet, declaration, row, geometry, check=check))
    return written


def read_fact(packet: Path, declaration: Declaration, row: Witness) -> dict[str, Any]:
    """Admit one algebraic fact: a valid witness that rebuilds itself from its geometry."""
    path = packet / row["fact"]
    reports.ensure_private(retained_data.compressed_path(path))
    try:
        raw = read_retained_bytes(path, limit=4 * reports.MAX_SOURCE_BYTES)
        document = load_yaml(raw.decode("utf-8"))
    except (OSError, ValueError, yaml.YAMLError) as error:
        raise ReportError(f"n={row['n']}: derived fact is unreadable: {error}") from error
    witness = _validated(document, row["n"])
    rebuilt = witness_envelope(
        fact_witness(packet, declaration, row, _geometry(witness, row)), schema=FACT_SCHEMA
    )
    _require(document == rebuilt, f"n={row['n']}: derived fact differs from its own rebuild")
    return witness


def read_facts(packet: Path, numbers: set[int] | None = None) -> dict[int, dict[str, Any]]:
    """Admit the declared witnesses, or those of ``numbers``, after the custody check."""
    reports.ensure_private(packet)
    declaration = load_declaration(packet)
    reports.acquisition(packet)
    return {
        row["n"]: read_fact(packet, declaration, row)
        for row in declaration["witnesses"]
        if numbers is None or row["n"] in numbers
    }


# --------------------------------------------------------------------------- comparison


def _scalar_coefficients(value: Any) -> list[Fraction]:
    return [Fraction(value)] if isinstance(value, str) else [Fraction(item) for item in value]


def _scalar_text(coefficients: list[Fraction]) -> Any:
    while len(coefficients) > 1 and coefficients[-1] == 0:
        coefficients.pop()
    texts = [str(item) for item in coefficients]
    return texts[0] if len(texts) == 1 else texts


def side_of(witness: dict[str, Any]) -> Any:
    """The witness's exact side: a field element, or a Fraction where it is rational."""
    _squares, side = materialize_exact_witness(witness)
    return side


def enclosure(value: Any, digits: int) -> tuple[Fraction, Fraction]:
    if isinstance(value, FieldElement):
        value.field.refine_to(digits)
        return value.field.enclose(value)
    return value, value


def against(value: Any, span: reports.Span) -> str:
    """Below, above or undecided, with the side enclosed ever more tightly."""
    for digits in DIGITS:
        low, high = enclosure(value, digits)
        own = reports.Span(low, high, open_low=False, open_high=False)
        if reports.below(own, span):
            return "below"
        if reports.below(span, own):
            return "above"
    return "equal" if span.low == span.high == value else "undecided"


def _is_root(polynomial: tuple[int, ...], value: Any) -> bool:
    total: Any = value.field.zero if isinstance(value, FieldElement) else Fraction(0)
    for coefficient in polynomial:
        total = total * value + coefficient
    return total.is_zero() if isinstance(total, FieldElement) else total == 0


def against_bound(value: Any, bound: VerifiedBound | None) -> str:
    """The side against a case bound held exactly, including equality to a closed form.

    A closed form is its minimal polynomial's one root in its isolating interval, so a side
    that is a root of that polynomial and lies inside the interval is that number.
    """
    if bound is None:
        return "none"
    if bound.rational is not None:
        return against(value, reports.exact_span(bound.rational))
    if bound.interval is None:
        return "undecided"
    low, high = bound.interval
    root = _is_root(bound.polynomial, value)
    relation = "undecided"
    for digits in DIGITS:
        lo, hi = enclosure(value, digits)
        if root and low < lo and hi < high:
            relation = "equal"
        elif hi < low:
            relation = "below"
        elif lo > high:
            relation = "above"
        if relation != "undecided":
            break
    return relation


def _decimal(value: Any) -> str:
    """The side rounded down at ``DISPLAY_PLACES``, from an enclosure 20 places tighter."""
    low, _high = enclosure(value, DISPLAY_PLACES + 20)
    scale = 10**DISPLAY_PLACES
    floor = low.numerator * scale // low.denominator
    whole, part = divmod(floor, scale)
    return f"{whole}.{part:0{DISPLAY_PLACES}d}"


def _closed(form: Any) -> VerifiedBound | None:
    # The layer's driver, loaded where a comparison needs it: a house check reads this
    # module's facts and receipts in a worker that prunes the driver (`upper_bound_houses`).
    from devtools import regularize_evand as regularized  # noqa: PLC0415

    if not form:
        return None
    text = str(form)
    try:
        return regularized.VerifiedBound(text, rational=Fraction(text.replace(" ", "")))
    except ValueError:
        return regularized.verified_bound(
            {"verified_upper_bound": text, "exact_form": text.replace(" sqrt", "*sqrt")}
        )


def compare(packet: Path) -> dict[str, Any]:
    """Each side against the case record's two lanes and every pending report, exactly."""
    from devtools import regularize_evand as regularized  # noqa: PLC0415 -- as `_closed`

    declaration = load_declaration(packet)
    witnesses = read_facts(packet)
    source = reports.acquisition(packet)
    results = []
    for row in declaration["witnesses"]:
        n = row["n"]
        side = side_of(witnesses[n])
        facts = regularized.case_facts(n)
        case_text = (regularized.FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
        front = load_yaml(case_text.split("---\n", 2)[1])["packing"]["reported_upper_bound"]
        try:
            verified = regularized.verified_bound(facts)
            reported_form = _closed(front.get("exact_form"))
        except ValueError as error:
            raise ReportError(
                f"n={n}: the case's bounds do not read exactly: {error}"
            ) from error
        others = []
        for item in declaration["pending"]:
            if item["n"] != n:
                continue
            span = (
                reports.exact_span(Fraction(item.get("exact", "")))
                if "exact" in item
                else reports.printed_span(item.get("printed", ""), item.get("rounding", ""))
            )
            entry = {key: value for key, value in item.items() if key != "n"}
            entry["relation"] = against(side, span)
            others.append(entry)
        relations = [entry["relation"] for entry in others]
        verified_relation = against_bound(side, verified)
        reported_relation = (
            against_bound(side, reported_form)
            if reported_form is not None
            else against(side, reports.printed_span(str(front["value"]), "unstated"))
        )
        everything = [verified_relation, reported_relation, *relations]
        results.append(
            {
                "n": n,
                "certificate": row["path"],
                "degree": row["degree"],
                "minimal_polynomial": witnesses[n]["scalar"]["minimal_polynomial"],
                "side": witnesses[n]["side"],
                "side_decimal": _decimal(side),
                "first_committed": row["first_committed"],
                "replayed": n in declaration["replayed"],
                "case": {
                    "verified_value": str(facts["verified_upper_bound"]),
                    "verified_exact_form": facts["exact_form"],
                    "verified_relation": verified_relation,
                    "reported_value": str(front["value"]),
                    "reported_exact_form": front.get("exact_form"),
                    "reported_source_key": front.get("source_key"),
                    "reported_relation": reported_relation,
                },
                "pending": others,
                "below_every_other": all(item == "below" for item in everything),
            }
        )
    return {
        "format": CLAIMS_FORMAT,
        "issue": declaration["issue"],
        "source": source["source_url"],
        "revision": source["source_commit"],
        "read_on": declaration["read_on"],
        "read_at_main": declaration["read_at_main"],
        "results": results,
    }


def _record_text(value: dict[str, Any]) -> str:
    """A claim record with one result per line, as the importer writes its own."""
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


def write_claims(packet: Path) -> dict[str, Any]:
    claims = compare(packet)
    path = packet / CLAIMS
    reports.ensure_private(path.parent)
    with atomic_output_file(path) as temporary:
        temporary.write_text(_record_text(claims), encoding="utf-8")
    return claims


def check_claims(packet: Path) -> dict[str, Any]:
    rebuilt = compare(packet)
    path = packet / CLAIMS
    reports.ensure_private(path)
    stored = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=kernel.unique_object
    )
    _require(stored == rebuilt, "frozen algebraic claim record differs from its rebuild")
    return rebuilt


# --------------------------------------------------------------------------- replay


def job_witness(witness: dict[str, Any], control: str) -> dict[str, Any]:
    """The positive witness, or a control: square 2 a copy of square 1, or square 1 moved
    right by the side and two more, wholly outside the box."""
    _require(control in JOBS, "unknown job")
    job = copy.deepcopy(witness)
    squares = job["squares"]
    if control == "duplicate-square-overlap":
        squares[1] = {**copy.deepcopy(squares[0]), "id": squares[1]["id"]}
    elif control == "square-translated-outside-container":
        shift = _scalar_coefficients(job["side"])
        shift[0] += 2
        first = squares[0]
        points = [first["center"]] if "center" in first else first["corners"]
        for point in points:
            moved = _scalar_coefficients(point[0])
            width = max(len(moved), len(shift))
            moved += [Fraction(0)] * (width - len(moved))
            padded = shift + [Fraction(0)] * (width - len(shift))
            point[0] = _scalar_text([a + b for a, b in zip(moved, padded, strict=True)])
    job["id"] = f"{witness['id']}-{control}"
    return job


def decide(witness: dict[str, Any], control: str) -> dict[str, Any]:
    """One job on the route, with its CPU and wall time."""
    started, cpu = time.monotonic(), time.process_time()
    result, _report = exact_verify(job_witness(witness, control))
    return {
        "n": witness["n"],
        "control": control,
        ROUTE: json.loads(json.dumps(result, default=str)),
        "cpu_seconds": time.process_time() - cpu,
        "wall_seconds": time.monotonic() - started,
    }


def side_agrees(printed: object, side: Any) -> bool:
    """A verdict's side is this side: exactly where it is a rational, and otherwise a
    decimal of certain digits whose one-unit span the side's enclosures do not leave."""
    if type(printed) is not str:
        return False
    if _RATIONAL_SIDE.fullmatch(printed):
        return not isinstance(side, FieldElement) and Fraction(printed) == side
    # A decimal side binds only at the route's own precision (review C9 of #602).
    if not _DECIMAL_SIDE.fullmatch(printed) or len(printed.partition(".")[2]) < DISPLAY_PLACES:
        return False
    return against(side, reports.printed_span(printed, "unstated")) not in {"below", "above"}


def validate_job(
    row: Any, witness: dict[str, Any], control: str, *, side: Any | None = None
) -> None:
    """A job row is its count's and this witness's, and has the outcome its control requires.

    The verdict must name the job `job_witness` builds from this witness and state this
    witness's side (`side_agrees`), so a receipt that decided another witness of the same
    count is refused. ``side`` is the witness's exact side, when the caller has it.
    """
    n = witness["n"]
    _require(type(row) is dict, f"n={n} {control}: wrong row")
    fields = cast("dict[str, Any]", row)
    _require(
        fields.get("n") == n and fields.get("control") == control, f"n={n} {control}: wrong row"
    )
    _require(type(fields.get(ROUTE)) is dict, f"n={n} {control}: no route verdict")
    verdict = cast("dict[str, Any]", fields[ROUTE])
    _require(
        verdict.get("id") == f"{witness['id']}-{control}",
        f"n={n} {control}: the verdict is not this witness's job",
    )
    _require(
        side_agrees(verdict.get("side"), side_of(witness) if side is None else side),
        f"n={n} {control}: the verdict's side is not this witness's",
    )
    passed = verdict.get("verification_passed")
    if control == "positive":
        _require(
            passed is True
            and verdict.get("pairs_tested") == n * (n - 1) // 2
            and verdict.get("failures") == []
            and verdict.get("n") == n,
            f"n={n}: the positive job does not pass with every pair decided",
        )
    else:
        kinds = {failure[0] for failure in verdict.get("failures", [])}
        expected = "overlap" if control == "duplicate-square-overlap" else "container"
        _require(passed is False and expected in kinds, f"n={n} {control}: not refused")
    for key in ("cpu_seconds", "wall_seconds"):
        value = fields.get(key)
        _require(type(value) in (int, float) and cast("float", value) >= 0, f"n={n}: bad time")


def receipt_path(packet: Path, n: int) -> Path:
    return packet / f"receipts/algebraic-route1-n{n:03d}.json.xz"


def run_job(packet: Path, n: int, control: str, directory: Path) -> dict[str, Any]:
    """One job in its own child process, its output kept whatever happens."""
    output = directory / f"n{n}-{control}.json"
    if output.exists():
        return json.loads(output.read_text(encoding="utf-8"))
    command = [sys.executable, "-m", MODULE, packet.name, "decide-job"]
    command += ["--n", str(n), "--control", control, "--output", str(output)]
    completed = subprocess.run(command, capture_output=True, check=False)
    output.with_suffix(".stdout.log").write_bytes(completed.stdout)
    output.with_suffix(".stderr.log").write_bytes(completed.stderr)
    _require(completed.returncode == 0, f"n={n} {control}: child exited {completed.returncode}")
    return json.loads(output.read_text(encoding="utf-8"))


def certify(packet: Path, directory: Path, numbers: list[int] | None = None) -> None:
    """Decide each roster count's three jobs, one at a time, and write its receipt.

    A job whose output is already in ``directory`` is not decided again, so an interrupted
    run resumes; every row is validated before a receipt is written.
    """
    declaration = load_declaration(packet)
    roster = declaration["replayed"] if numbers is None else numbers
    _require(not set(roster) - set(declaration["replayed"]), "a count outside the roster")
    directory.mkdir(parents=True, exist_ok=True)
    for n in roster:
        witness = read_facts(packet, {n})[n]
        side = side_of(witness)
        rows = [run_job(packet, n, control, directory) for control in JOBS]
        for row, control in zip(rows, JOBS, strict=True):
            validate_job(row, witness, control, side=side)
        kernel.save_xz(
            receipt_path(packet, n),
            {"format": declaration["receipt_format"], "routes": [ROUTE], "cases": rows},
        )


def decide_job(packet: Path, n: int, control: str, output: Path) -> None:
    declaration = load_declaration(packet)
    _require(n in declaration["replayed"] and control in JOBS, "job outside the roster")
    _require(not output.exists(), "refusing to overwrite a deciding job")
    witness = read_facts(packet, {n})[n]
    row = decide(witness, control)
    validate_job(row, witness, control)
    output.write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")


def check(
    packet: Path, numbers: list[int] | None = None, *, replay: bool = False
) -> dict[int, Any]:
    """Admit every roster count's receipt; with ``replay``, decide its jobs again."""
    declaration = load_declaration(packet)
    roster = declaration["replayed"] if numbers is None else numbers
    _require(not set(roster) - set(declaration["replayed"]), "a count outside the roster")
    stray = {
        path
        for path in (packet / "receipts").glob("algebraic-route1-n*.json.xz")
        if path not in {receipt_path(packet, n) for n in declaration["replayed"]}
    }
    _require(not stray, f"receipts for counts outside the roster: {sorted(stray)}")
    positives = {}
    for n in roster:
        witness = read_facts(packet, {n})[n]
        side = side_of(witness)
        record = kernel.read_xz(receipt_path(packet, n))
        _require(
            record.get("format") == declaration["receipt_format"]
            and record.get("routes") == [ROUTE]
            and len(record.get("cases", [])) == len(JOBS),
            f"n={n}: not this packet's receipt",
        )
        for row, control in zip(record["cases"], JOBS, strict=True):
            validate_job(row, witness, control, side=side)
            if replay:
                again = decide(witness, control)
                _require(again[ROUTE] == row[ROUTE], f"n={n} {control}: the replay differs")
        positives[n] = record["cases"][0][ROUTE]
    return positives


def summary(positives: dict[int, Any], packet: Path) -> dict[str, Any]:
    rows = [row for n in positives for row in kernel.read_xz(receipt_path(packet, n))["cases"]]
    return {
        "counts": len(positives),
        "jobs": len(rows),
        "pair_decisions": sum(row[ROUTE]["pairs_tested"] for row in rows),
        "route_cpu_seconds": round(sum(row["cpu_seconds"] for row in rows), 2),
        "job_wall_seconds": round(sum(row["wall_seconds"] for row in rows), 2),
        "longest_job_seconds": round(max(row["wall_seconds"] for row in rows), 2),
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
    derivation.add_argument("--assets", type=Path, required=True)
    derivation.add_argument("--check", action="store_true")
    forms = sub.add_parser("derive-forms")
    forms.add_argument("--check", action="store_true")
    claims = sub.add_parser("compare")
    claims.add_argument("--write", action="store_true")
    campaign = sub.add_parser("certify")
    campaign.add_argument("--jobs-dir", type=Path, required=True)
    campaign.add_argument("--n", type=int, nargs="+")
    checking = sub.add_parser("check")
    checking.add_argument("--n", type=int, nargs="+")
    checking.add_argument("--replay", action="store_true")
    job = sub.add_parser("decide-job")
    job.add_argument("--n", type=int, required=True)
    job.add_argument("--control", choices=JOBS, required=True)
    job.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    packet = reports.packet_path(args.packet)
    if args.action == "derive":
        rows = derive(packet, args.checkout, args.assets, check=args.check)
        verb = "match the assets" if args.check else "written"
        print(f"{len(rows)} algebraic facts {verb}; their Compressed Files rows:")
        for row in rows:
            print(row.markdown())
    elif args.action == "derive-forms":
        rows = derive_forms(packet, check=args.check)
        verb = "match the retained forms" if args.check else "written"
        print(f"{len(rows)} algebraic facts {verb}; their Compressed Files rows:")
        for row in rows:
            print(row.markdown())
    elif args.action == "compare":
        claims_record = write_claims(packet) if args.write else check_claims(packet)
        print(_record_text(claims_record), end="")
    elif args.action == "certify":
        certify(packet, args.jobs_dir, args.n)
        print(json.dumps(summary(check(packet, args.n), packet), indent=2))
    elif args.action == "check":
        positives = check(packet, args.n, replay=args.replay)
        print(json.dumps(summary(positives, packet), indent=2))
    else:
        decide_job(packet, args.n, args.control, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
