"""Exact-nine generated atlas reads, with private semantic custody and no write escape.

This proposal links only eight leaves: n263's existing private/index consumer survives.
It does not grant a generic witness-reader or mutation-target escape.
"""

from __future__ import annotations

import copy
import lzma
import os
from pathlib import Path, PurePosixPath
from typing import Any

from devtools import squish_second_update_confirmation as confirmation
from sqpack.witness import validate_witness_document, witness_envelope
from sqpack.yamlio import safe_load

shared = confirmation.shared
original = confirmation.original
LINK_NUMBERS = tuple(n for n in confirmation.NUMBERS if n != 263)
LIMITATIONS = (
    "Exact rational corners derived from retained SQUISH center/half-angle facts, "
    "checked with exact predicates at the source's exact rational side. The SVG "
    "rounds only for visualization. Verifies this upper-bound construction, not "
    "optimality or confirmation of the imported result in the frontier register. "
    "The source publishes no licence, so only derived geometry and attributed "
    "metadata are retained; this conservative retention policy is not a legal "
    "conclusion."
)


def house_path(n: int) -> Path:
    confirmation.reported.source_url(n)
    return confirmation.REPO / "packing/witnesses/known-best" / f"n-{n:03d}.yaml"


def metadata_path() -> Path:
    return confirmation.PACKET / "receipts/house-atlas-metadata.json.xz"


def bounded_house(path: Path) -> dict[str, Any]:
    with path.open("rb") as stream:
        data = stream.read(original.MAX_RECEIPT_BYTES + 1)
    if len(data) > original.MAX_RECEIPT_BYTES:
        raise original.PacketError("house witness exceeds existing witness ceiling")
    document = safe_load(data.decode())
    softschema = witness_envelope({}, schema="../witness.schema.yaml")["softschema"]
    if document.get("softschema") != softschema:
        raise original.PacketError("house schema contract differs from canonical envelope")
    return dict(
        validate_witness_document(
            witness_envelope(document["witness"], schema=confirmation.SCHEMA.as_posix()),
            path=path,
            fallback_schema=confirmation.SCHEMA,
        )
    )


def validate_metadata(n: int, value: Any, positive: dict[str, Any]) -> None:
    fact = confirmation.read_fact(n)
    identifier = f"W-known-best-n{n:03d}"
    expected_claim = original.to_witness(fact)["claim"]
    expected_claim["limitations"] = LIMITATIONS
    if (
        type(value) is not dict
        or set(value) != {"id", "claim", "source", "certificate"}
        or value["id"] != identifier
        or value["claim"] != expected_claim
        or value["source"]
        != {
            "key": confirmation.reported.SOURCE_KEY,
            "path": confirmation.fact_path(n)
            .relative_to(confirmation.REPO / "packing")
            .as_posix(),
            "url": confirmation.reported.source_url(n),
            "retrieved": confirmation.reported.RETRIEVED,
            "revision": confirmation.REVISION,
        }
        or set(value["certificate"]) != {"kind", "replay", "result"}
        or value["certificate"]["kind"] != "exact-rational-sat"
        or value["certificate"]["replay"]
        != (f"uv run --frozen packing-witness verify witnesses/known-best/n-{n:03d}.yaml")
    ):
        raise original.PacketError("house identity/source/claim/replay metadata mismatch")
    result = value["certificate"]["result"]
    shared.validate_verdict(result, n, passed=True)
    if (
        set(result)
        != {
            "operation",
            "id",
            "coordinate_provenance",
            "method",
            "verification_passed",
            "n",
            "side",
            "pairs_tested",
            "minimum_containment_clearance",
            "minimum_best_pair_gap",
            "field_certificate",
            "failures",
            "limitations",
        }
        or result["operation"] != "verify"
        or result["id"] != identifier
        or result["coordinate_provenance"] != "verified"
        or result["method"] != "exact-algebraic"
        or result["side"] != fact["side"]
        or result["field_certificate"]
        != {"field": "Q", "preconditions": "degree-one rational field"}
        or result["limitations"]
        != ("Verifies witness feasibility and its upper bound, not global optimality.")
        or {key: result[key] for key in positive} != positive
        or type(result["minimum_best_pair_gap"]) is not str
        or shared.clearance(result["minimum_best_pair_gap"]) < 0
    ):
        raise original.PacketError("house retained native result differs from complete replay")


def retain_metadata(source_repository: Path) -> None:
    rows = confirmation.admit_certification()
    admitted = []
    for n in confirmation.NUMBERS:
        witness = bounded_house(
            source_repository / house_path(n).relative_to(confirmation.REPO)
        )
        if original.checker_input(witness) != original.checker_input(
            confirmation.to_witness(confirmation.read_fact(n))
        ):
            raise original.PacketError("house complete geometry differs from reviewed facts")
        metadata = confirmation.metadata(witness)
        validate_metadata(
            n, metadata, rows[n]["case"]["historical_actual_receipts"][0]["exact_verify"]
        )
        admitted.append({"n": n, "metadata": metadata})
    confirmation.save(
        metadata_path(),
        lzma.compress(
            shared.json_bytes(
                {
                    "format": "squish-422-private-house-metadata-v1",
                    "source_commit": confirmation.REVISION,
                    "producer_checker_replayed": False,
                    "cases": admitted,
                }
            )
        ),
    )


def admitted_metadata(rows: dict[int, Any]) -> dict[int, Any]:
    path = metadata_path()
    if not path.resolve().is_relative_to(confirmation.REPO.resolve()):
        raise original.PacketError("house custody input must remain private")
    record = shared.read_xz_receipt(path)
    if (
        record["format"] != "squish-422-private-house-metadata-v1"
        or record["source_commit"] != confirmation.REVISION
        or record["producer_checker_replayed"] is not False
    ):
        raise original.PacketError("private house metadata custody mismatch")
    metadata = shared.roster(record["cases"], confirmation.NUMBERS)
    for n, row in metadata.items():
        validate_metadata(
            n,
            row["metadata"],
            rows[n]["case"]["historical_actual_receipts"][0]["exact_verify"],
        )
    return metadata


def check_houses(numbers: list[int] | None = None) -> dict[int, Any]:
    """One complete custody admission for a selected set of exact-nine house reads."""
    selected = list(confirmation.NUMBERS) if numbers is None else numbers
    if (
        not selected
        or len(set(selected)) != len(selected)
        or any(type(n) is not int or n not in confirmation.NUMBERS for n in selected)
    ):
        raise original.PacketError("invalid scoped house read roster")
    rows = confirmation.admit_certification()
    metadata = admitted_metadata(rows)
    result = {}
    for n in selected:
        path = house_path(n)
        parent = path.parent
        if (
            not parent.resolve().is_relative_to(confirmation.REPO.resolve())
            or parent.is_symlink()
        ):
            raise original.PacketError("house parent must remain inside the private checkout")
        if path.is_symlink() and (
            n not in LINK_NUMBERS or (path.parent / path.readlink()).is_symlink()
        ):
            raise original.PacketError("house leaf is not an admitted direct readonly link")
        expected = original.to_witness(confirmation.read_fact(n))
        expected.update(copy.deepcopy(metadata[n]["metadata"]))
        actual = bounded_house(path)
        if shared.json_bytes(actual) != shared.json_bytes(expected):
            raise original.PacketError(
                "house full geometry or private metadata custody mismatch"
            )
        result[n] = actual
    return result


def check_house(n: int) -> dict[str, Any]:
    return check_houses([n])[n]


def linked_house_problem(path: str, *, repository: Path) -> str | None:
    allowed = {house_path(n).relative_to(confirmation.REPO).as_posix(): n for n in LINK_NUMBERS}
    if repository.resolve() != confirmation.REPO.resolve() or path not in allowed:
        return "artifact escapes the repository checkout"
    candidate = house_path(allowed[path])
    if not candidate.is_symlink():
        return "artifact is not an exact admitted house leaf link"
    try:
        check_house(allowed[path])
    except (ValueError, KeyError, TypeError, OSError, StopIteration) as error:
        return f"linked house source/custody mismatch: {error}"
    return None


def guard_house_outputs(numbers: tuple[int, ...] | list[int]) -> None:
    """Producer preflight before figure metadata writes, geometry builds or mkdir."""
    for n in confirmation.NUMBERS:
        if n in numbers:
            confirmation.guard_output(house_path(n))


def snapshot_house_links() -> tuple[Path, ...]:
    """Exact candidates, excluding all declared mutation targets before pruning/indexing.

    Ordinary document/result dependency rescue remains the harness's existing API;
    a rescued file must be copied/indexed and must never be replaced by a link.
    """
    controls = safe_load((confirmation.REPO / "packing/devtools/controls.yaml").read_text())
    private = set()
    for control in controls["controls"]:
        raw = control["file"]
        pure = PurePosixPath(raw)
        if pure.is_absolute() or pure.as_posix() != raw:
            raise original.PacketError("registered mutation target is not normalized")
        target = Path(os.path.normpath(confirmation.REPO / "packing" / pure))
        if not target.is_relative_to(confirmation.REPO):
            raise original.PacketError("registered mutation target escapes the checkout")
        private.add(target)
    return tuple(house_path(n) for n in LINK_NUMBERS if house_path(n) not in private)
