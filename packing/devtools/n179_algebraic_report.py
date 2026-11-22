"""Read issue 959's attachment without inventing repository-commit custody.

Only n179 is admitted. The retained mathematical file is bound to its attachment member;
its exact geometry is rebuilt by the maintained minpoly reader and compared with the
retained fact. The independently frozen review decides the original data separately.
This adapter checks premises and does not itself decide geometric feasibility.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from devtools import algebraic_witness_reports as fields
from devtools import exact_sides, retained_data
from devtools import upper_bound_reports as reports
from sqpack.field import FieldElement
from sqpack.witness import validate_witness_document, witness_envelope
from sqpack.yamlio import load_yaml

PACKET_NAME = "de-winter-959-followup-2026-11-20"
SOURCE_KEY = "[de Winter n179 algebraic certificate 2026-11-20]"
SOURCE = Path("source/n179.minpoly.json.gz")
CUSTODY = Path("acquisition/sources.json")
FACT = Path("facts/alg-n-179.yaml")
SOURCE_SHA256 = "28edf9561e87037b5c681e4ff0051a1bd1b8e5401c1a8376fe2e66c2c18663d1"
ARCHIVE_SHA256 = "143e9298eaf8c96e0e36bd7346a41b765e1d8e77dc1be10c76e17846ce73c3c8"
COMMENT = "https://github.com/jlevy/squares/issues/959#issuecomment-7050119161"
ARCHIVE_URL = "https://github.com/user-attachments/files/35184249/n179-exact-construction.zip"
MEMBER = "algebraic/n179/n179.minpoly.json.gz"
WITNESS_PREFIX = "W-de-winter-959-alg-n"
LIMITATIONS = (
    "Finite feasibility of 179 unit squares at the exact algebraic side L70+5=L207-1. "
    "Construction credited to Doğa Özden after Ryan Xu and Evan Daniel; algebraic "
    "certificate credited to Joost de Winter. The reported GeiserX starting file and "
    "its identity remain unresolved. No optimality, stationarity or historical-priority claim."
)


def packet_path() -> Path:
    return reports.packet_path(PACKET_NAME)


def accepts(packet: Path) -> bool:
    return packet.name == PACKET_NAME


def require_count(n: int) -> None:
    if type(n) is not int or n != 179:
        raise fields.ReportError(f"the issue 959 attachment states only n=179, not {n}")


def declaration(*, read_on: str, read_at_main: str) -> fields.Declaration:
    return {
        "format": fields.DECLARATION_FORMAT,
        "issue": COMMENT,
        "author": "Doğa Özden; algebraic reconstruction by Joost de Winter",
        "source_key": SOURCE_KEY,
        "receipt_format": "de-winter-959-n179-algebraic-route1-v1",
        "witness_prefix": WITNESS_PREFIX,
        "claim_limitations": LIMITATIONS,
        "read_on": read_on,
        "read_at_main": read_at_main,
        "witnesses": [
            {
                "n": 179,
                "path": SOURCE.as_posix(),
                "form": "evand-exact-minpoly-v1",
                "fact": FACT.as_posix(),
                "degree": 5,
                # This is the attachment publication time, not a fabricated Git commit.
                "first_committed": "2026-11-20T20:41:05Z",
            }
        ],
        "replayed": [179],
        "pending": [],
    }


def checked_source(packet: Path) -> bytes:
    """Bind the mathematical input to the retained attachment custody record."""
    if not accepts(packet):
        raise fields.ReportError("not the n179 attachment packet")
    reports.ensure_private(packet / CUSTODY)
    reports.ensure_private(packet / SOURCE)
    record = json.loads((packet / CUSTODY).read_text(encoding="utf-8"))
    expected = {
        "source_comment": COMMENT,
        "source_url": ARCHIVE_URL,
        "archive_sha256": ARCHIVE_SHA256,
        "member": MEMBER,
        "member_sha256": SOURCE_SHA256,
        "retained_member": SOURCE.as_posix(),
        "retained_bytes_unchanged": True,
    }
    if any(record.get(key) != value for key, value in expected.items()):
        raise fields.ReportError("n179 attachment custody identity differs")
    raw = (packet / SOURCE).read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise fields.ReportError("n179 mathematical attachment member differs")
    return raw


def build_witness(packet: Path) -> dict[str, Any]:
    raw = checked_source(packet)
    row = declaration(read_on="2026-11-21", read_at_main="context-only")["witnesses"][0]
    geometry = fields.evand_minpoly_geometry(raw, row)
    return {
        "id": f"{WITNESS_PREFIX}179",
        "n": 179,
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
            "path": f"packing/resources/web/{PACKET_NAME}/{SOURCE.as_posix()}",
            "url": f"{ARCHIVE_URL}#{MEMBER}",
            "retrieved": "2026-11-21",
            "revision": f"attachment-sha256:{ARCHIVE_SHA256}",
            "revision_sha256": SOURCE_SHA256,
        },
    }


def read_witness(packet: Path, n: int) -> dict[str, Any]:
    """Refuse a changed or detached derived fact before any house uses it."""
    require_count(n)
    actual = fields.load_declaration(packet)
    expected_declaration = declaration(
        read_on=actual["read_on"], read_at_main=actual["read_at_main"]
    )
    if actual != expected_declaration:
        raise fields.ReportError(
            "n179 algebraic declaration changes the accepted source or scope"
        )
    expected = build_witness(packet)
    path = retained_data.compressed_path(packet / FACT)
    reports.ensure_private(path)
    reports.ensure_private(packet / FACT)
    document = load_yaml(retained_data.read_retained_bytes(packet / FACT).decode("utf-8"))
    witness = validate_witness_document(
        document, path=path, fallback_schema=fields.WITNESS_SCHEMA
    )
    if witness != expected or document != witness_envelope(expected, schema=fields.FACT_SCHEMA):
        raise fields.ReportError("n179 derived fact does not rebuild from the original source")
    return copy.deepcopy(witness)


def read_facts(packet: Path, numbers: set[int] | None = None) -> dict[int, dict[str, Any]]:
    if numbers is not None and numbers - {179}:
        raise fields.ReportError("n179 attachment reader received an undeclared count")
    return {179: read_witness(packet, 179)} if numbers is None or 179 in numbers else {}


def exact_side(n: int) -> exact_sides.Side:
    require_count(n)
    value = fields.side_of(read_witness(packet_path(), n))
    if not isinstance(value, FieldElement):
        raise fields.ReportError("n179 side must be an algebraic field element")
    return exact_sides.of_field_element(value)


def inputs(packet: Path) -> tuple[Path, ...]:
    paths = (
        packet / fields.DECLARATION,
        packet / CUSTODY,
        packet / SOURCE,
        retained_data.compressed_path(packet / FACT),
        fields.receipt_path(packet, 179),
    )
    registration = packet / "acquisition/registration.json"
    return (*paths, registration) if registration.is_file() else paths


def registered_result() -> str | None:
    """The coordinator-assigned result; absent until the registration is installed."""
    path = packet_path() / "acquisition/registration.json"
    if not path.is_file():
        return None
    reports.ensure_private(path)
    record = json.loads(path.read_text(encoding="utf-8"))
    result = record.get("result")
    if type(result) is not str or re.fullmatch(r"T-[0-9]{3,}", result) is None:
        raise fields.ReportError("n179 registration has no assigned T identifier")
    if record.get("n") != 179 or record.get("source_key") != SOURCE_KEY:
        raise fields.ReportError("n179 registration identifies a different source")
    return result
