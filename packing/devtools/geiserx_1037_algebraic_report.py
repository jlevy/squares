"""Read the two reviewed quadratic certificates in issue 1037's attachment.

The original mathematical members supply every center, basis and side. Derived facts
must rebuild from those members, and per-count native receipts must preserve the
original six-job record. This reader does not decide geometric feasibility or register
an upper bound. Registration remains absent until the coordinator assigns its result.
"""

from __future__ import annotations

import copy
import gzip
import hashlib
import io
import json
import re
import zlib
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import algebraic_witness_reports as fields
from devtools import evand_arrangement_reports as kernel
from devtools import exact_sides, retained_data
from devtools import upper_bound_reports as reports
from sqpack.field import FieldElement
from sqpack.witness import validate_witness_document, witness_document, witness_envelope
from sqpack.yamlio import load_yaml

PACKET_NAME = "geiserx-exact-1037-2026-11-22"
SOURCE_KEY = "[GeiserX issue 1037 2026-11-18]"
COUNTS = (202, 263)
CUSTODY = Path("acquisition/sources.json")
NATIVE_RECEIPT = Path("receipts/native-quadratic-202-263.json.xz")
REGISTRATION = Path("acquisition/registration.json")
ISSUE = "https://github.com/jlevy/squares/issues/1037"
ARCHIVE_URL = "https://github.com/user-attachments/files/35051652/GeiserX_exact.zip"
ARCHIVE_SHA256 = "19c069b42d6a6fbe87dd419d358e7b046eadbba20dbaadd7f519faab1152c5e9"
WITNESS_PREFIX = "W-geiserx-1037-quadratic-n"
RECEIPT_FORMAT = "geiserx-1037-algebraic-route1-v1"
MEMBERS = {
    202: (57568, "f588cdc40027ff01c4b49f8ad1dbadacb50449b4941133a242e70974be908ffc"),
    263: (71063, "092d7599ff0b3ead6d5281cd7bd3ffaef4b4a950eda22118e151b18b183b200e"),
}
LIMITATIONS = (
    "Finite feasibility of the submitted 202- and 263-square quadratic configurations. "
    "Construction credited to Sergio Fernández Rubio (GeiserX), refined and certified "
    "by Joost de Winter. No optimality, rigidity or stationarity claim. The 202-square "
    "restriction of the 263 witness is not the standalone quadratic 202 witness."
)


def packet_path() -> Path:
    return reports.packet_path(PACKET_NAME)


def accepts(packet: Path) -> bool:
    return packet.name == PACKET_NAME


def require_count(n: int) -> None:
    if type(n) is not int or n not in COUNTS:
        raise fields.ReportError(
            f"issue 1037's quadratic reader admits only 202 and 263, not {n}"
        )


def source_path(n: int) -> Path:
    require_count(n)
    return Path(f"source/algebraic/n{n}.minpoly.json.gz")


def fact_path(n: int) -> Path:
    require_count(n)
    return Path(f"facts/alg-n-{n}.yaml")


def declaration(*, read_on: str, read_at_main: str) -> fields.Declaration:
    return {
        "format": fields.DECLARATION_FORMAT,
        "issue": ISSUE,
        "author": "Sergio Fernández Rubio (GeiserX); quadratic certificates by Joost de Winter",
        "source_key": SOURCE_KEY,
        "receipt_format": RECEIPT_FORMAT,
        "witness_prefix": WITNESS_PREFIX,
        "claim_limitations": LIMITATIONS,
        "read_on": read_on,
        "read_at_main": read_at_main,
        "witnesses": [
            {
                "n": n,
                "path": source_path(n).as_posix(),
                "form": "evand-exact-minpoly-v1",
                "fact": fact_path(n).as_posix(),
                "degree": 2,
                # The source issue's publication time, not a certificate Git commit.
                "first_committed": "2026-11-18T20:06:25Z",
            }
            for n in COUNTS
        ],
        "replayed": list(COUNTS),
        "pending": [],
    }


def _checked_declaration(packet: Path) -> fields.Declaration:
    if not accepts(packet):
        raise fields.ReportError("not the issue 1037 attachment packet")
    actual = fields.load_declaration(packet)
    expected = declaration(read_on=actual["read_on"], read_at_main=actual["read_at_main"])
    if actual != expected:
        raise fields.ReportError("issue 1037 declaration changes the accepted source or scope")
    return actual


def checked_source(packet: Path, n: int) -> bytes:
    """Read bounded gzip bytes whose decoded content is the original attachment member."""
    require_count(n)
    if not accepts(packet):
        raise fields.ReportError("not the issue 1037 attachment packet")
    path = packet / source_path(n)
    reports.ensure_private(packet / CUSTODY)
    reports.ensure_private(path)
    record = json.loads(
        (packet / CUSTODY).read_text(encoding="utf-8"),
        object_pairs_hook=kernel.unique_object,
    )
    if type(record) is not dict or type(record.get("attachment")) is not dict:
        raise fields.ReportError("issue 1037 attachment custody is not an object")
    attachment = record["attachment"]
    if (
        record.get("format") != "issue-attachment-sources-v1"
        or record.get("issue") != ISSUE
        or record.get("published") != "2026-11-18T20:06:25Z"
        or attachment.get("url") != ARCHIVE_URL
        or attachment.get("sha256") != ARCHIVE_SHA256
        or attachment.get("bytes") != 1989212
    ):
        raise fields.ReportError("issue 1037 attachment custody identity differs")
    member = f"GeiserX_exact/algebraic/n{n}.minpoly.json"
    size, digest = MEMBERS[n]
    members = record.get("members")
    if type(members) is not list or any(type(row) is not dict for row in members):
        raise fields.ReportError("issue 1037 member custody is not a row list")
    matches = [row for row in members if row.get("path") == member]
    expected = {
        "path": member,
        "bytes": size,
        "sha256": digest,
        "retained_at": source_path(n).as_posix(),
        "storage": "deterministic-gzip",
        "role": "numerical-source",
    }
    if len(matches) != 1 or any(
        matches[0].get(key) != value for key, value in expected.items()
    ):
        raise fields.ReportError(f"n={n}: issue 1037 mathematical member custody differs")
    # A malformed replacement must not decompress without a bound before it is refused.
    with path.open("rb") as handle:
        raw = handle.read(65537)
    if len(raw) > 65536:
        raise fields.ReportError(f"n={n}: issue 1037 gzip exceeds the retained-member limit")
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(raw)) as handle:
            decoded = handle.read(size + 1)
    except (OSError, EOFError, zlib.error) as error:
        raise fields.ReportError(
            f"n={n}: issue 1037 mathematical gzip is unreadable"
        ) from error
    if len(decoded) != size or hashlib.sha256(decoded).hexdigest() != digest:
        raise fields.ReportError(f"n={n}: issue 1037 mathematical attachment member differs")
    return raw


def build_witness(packet: Path, n: int) -> dict[str, Any]:
    admitted = _checked_declaration(packet)
    raw = checked_source(packet, n)
    row = next(row for row in admitted["witnesses"] if row["n"] == n)
    geometry = fields.evand_minpoly_geometry(raw, row)
    return {
        "id": f"{WITNESS_PREFIX}{n}",
        "n": n,
        "side": geometry["side"],
        "square_size": "1",
        "representation": geometry["representation"],
        "scalar": geometry["scalar"],
        "coordinates": dict(reports.CORNER_FRAME),
        "squares": geometry["squares"],
        "claim": {
            "coordinate_provenance": "reported",
            "method": "exact-algebraic",
            "limitations": LIMITATIONS,
        },
        "source": {
            "key": SOURCE_KEY,
            "path": f"packing/resources/web/{PACKET_NAME}/{source_path(n).as_posix()}",
            "url": f"{ARCHIVE_URL}#GeiserX_exact/algebraic/n{n}.minpoly.json",
            "retrieved": "2026-11-22",
            "revision": f"attachment-sha256:{ARCHIVE_SHA256}",
            "revision_sha256": MEMBERS[n][1],
        },
    }


def check_receipt_copy(packet: Path, n: int) -> None:
    """A per-count wrapper preserves every row of the accepted combined native receipt."""
    require_count(n)
    original_path = packet / NATIVE_RECEIPT
    wrapper_path = fields.receipt_path(packet, n)
    reports.ensure_private(original_path)
    reports.ensure_private(wrapper_path)
    original = kernel.read_xz(original_path)
    if (
        type(original) is not dict
        or type(original.get("cases")) is not list
        or any(type(row) is not dict for row in original["cases"])
        or original.get("format") != "geiserx-1037-native-quadratic-v1"
        or original.get("route") != fields.ROUTE
        or [(row.get("n"), row.get("control")) for row in original.get("cases", [])]
        != [(count, control) for count in COUNTS for control in fields.JOBS]
    ):
        raise fields.ReportError("issue 1037 original native receipt has a different scope")
    expected = {
        "format": RECEIPT_FORMAT,
        "routes": [fields.ROUTE],
        "cases": [row for row in original["cases"] if row["n"] == n],
    }
    if kernel.read_xz(wrapper_path) != expected:
        raise fields.ReportError(f"n={n}: issue 1037 wrapped native receipt differs")


def read_witness(packet: Path, n: int) -> dict[str, Any]:
    """Admit the fact only when its entire document rebuilds from the original source."""
    expected = build_witness(packet, n)
    plain = packet / fact_path(n)
    stored = retained_data.compressed_path(plain)
    reports.ensure_private(plain)
    reports.ensure_private(stored)
    document = load_yaml(retained_data.read_retained_bytes(plain).decode("utf-8"))
    actual = validate_witness_document(
        document, path=stored, fallback_schema=fields.WITNESS_SCHEMA
    )
    if actual != expected or document != witness_envelope(expected, schema=fields.FACT_SCHEMA):
        raise fields.ReportError(f"n={n}: issue 1037 fact does not rebuild from its source")
    check_receipt_copy(packet, n)
    return copy.deepcopy(actual)


def read_facts(packet: Path, numbers: set[int] | None = None) -> dict[int, dict[str, Any]]:
    selected = set(COUNTS) if numbers is None else numbers
    for n in selected:
        require_count(n)
    return {n: read_witness(packet, n) for n in COUNTS if n in selected}


def derive_facts(packet: Path, *, check: bool = False) -> list[retained_data.Row]:
    """Write the original geometry as compressed Witness/v2 facts, without a replay."""
    _checked_declaration(packet)
    rows = []
    for n in COUNTS:
        expected = build_witness(packet, n)
        text = witness_document(expected, schema=fields.FACT_SCHEMA)
        validate_witness_document(
            load_yaml(text), path=fields.WITNESS_SCHEMA, fallback_schema=fields.WITNESS_SCHEMA
        )
        target = packet / fact_path(n)
        stored = retained_data.compressed_path(target)
        reports.ensure_private(target)
        reports.ensure_private(stored)
        if check:
            if retained_data.read_retained_bytes(target) != text.encode("utf-8"):
                raise fields.ReportError(
                    f"n={n}: issue 1037 fact differs from the source rebuild"
                )
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            with atomic_output_file(target) as temporary:
                temporary.write_text(text, encoding="utf-8")
            # Keep the same compression convention as the maintained fact writer.
            stored.unlink(missing_ok=True)
            retained_data.compress(target)
        rows.append(retained_data.describe(packet, stored, "receipt"))
    return rows


def exact_side(n: int) -> exact_sides.Side:
    require_count(n)
    value = fields.side_of(read_witness(packet_path(), n))
    if not isinstance(value, FieldElement):
        raise fields.ReportError(f"n={n}: issue 1037 must state an algebraic side")
    return exact_sides.of_field_element(value)


def inputs(packet: Path, numbers: tuple[int, ...] = COUNTS) -> tuple[Path, ...]:
    for n in numbers:
        require_count(n)
    paths = [packet / fields.DECLARATION, packet / CUSTODY, packet / NATIVE_RECEIPT]
    for n in numbers:
        paths.extend(
            (
                packet / source_path(n),
                retained_data.compressed_path(packet / fact_path(n)),
                fields.receipt_path(packet, n),
            )
        )
    registration = packet / REGISTRATION
    if registration.is_file():
        paths.append(registration)
    return tuple(paths)


def registered_result() -> str | None:
    """Absent until the coordinator assigns a result for precisely these two counts."""
    path = packet_path() / REGISTRATION
    if not path.is_file():
        return None
    reports.ensure_private(path)
    record = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=kernel.unique_object
    )
    result = record.get("result")
    if type(result) is not str or re.fullmatch(r"T-[0-9]{3,}", result) is None:
        raise fields.ReportError("issue 1037 registration has no assigned T identifier")
    if record.get("n_values") != list(COUNTS) or record.get("source_key") != SOURCE_KEY:
        raise fields.ReportError(
            "issue 1037 registration identifies a different source or scope"
        )
    return result
