"""The case houses adopted on 11 October 2026 from the upper-bound reports of 8 to 11 October.

`devtools.select_houses` derives, count by count, the smallest confirmed and reviewed exact
side the register holds; `devtools.adopt_houses` moves each case record to it. This module
is the drawing's half of that adoption: the known-best witness of each adopted count,
`packing/witnesses/known-best/n-NNN.yaml`, the geometry the atlas draws, rebuilt from the
retained certificate and the complete native jobs that decided it, as the Gupta, Ry-Xu and
Daniel arrangement adoptions rebuild theirs (`gupta_house_links`, `ryxu_house_links`,
`evand_arrangement_houses`).

**Custody.** Each house is bound to private, ordinary repository files and to nothing
else: the packet's declaration and acquisition record, the one retained certificate or
derived fact of its count, bound to the digest the packet pins for its upstream file, and
the receipt that holds the count's three native jobs, a positive and its duplicate-square
and outside-container controls, each held to the certificate by
`evand_arrangement_reports.validate_job`. `private_input_paths` names exactly those files;
the negative controls copy them into every private worker (`COPY_SEPARATELY`), so a house
check that runs there reads its own inputs, never a link back into the primary checkout.
`T-128`'s packet carries its own reader and its custody was closed at its import;
`T-130`'s derived facts are read the way its own module reads them, one count at a time.

**No geometry runs in a check.** `check_houses` admits the inputs and compares the
retained witness with the one they rebuild; `build_witness`, which writes a house, also
decides it again with `sqpack`'s exact verifier and holds the result to the retained
native one.

Usage, from ``packing/`` with the project interpreter::

    python -m devtools.upper_bound_houses check [--n N ...]
    python -m devtools.upper_bound_houses inputs
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from pathlib import Path, PurePosixPath
from typing import Any, cast

from devtools import couzo_followup_reports as couzo_460
from devtools import couzo_refinement_reports as couzo_451
from devtools import evand_arrangement_reports as kernel
from devtools import retained_data
from devtools import squish_second_update_house_links as house
from devtools import upper_bound_reports as reports
from devtools.retained_data import read_retained_bytes
from sqpack.witness import WitnessError, validate_witness_document, witness_envelope
from sqpack.yamlio import load_yaml, safe_load

legacy = reports.legacy
ROOT = reports.ROOT
REPO = reports.REPO
WITNESSES = ROOT / "witnesses/known-best"
ADOPTED_ON = "2026-10-11"
COUZO = "Francisco Couzo"
NO_LICENCE = "no-licence-published"


class HouseError(kernel.ReportError):
    """A house, or an input it is rebuilt from, differs from what the record adopted."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise HouseError(message)


#: How the atlas's source index describes what a retained certificate keeps of upstream.
RAW_RETENTION = (
    "Complete source certificate retained losslessly and bound to the SHA-256 its packet "
    "pins upstream; no upstream program or prose is copied."
)
DERIVED_RETENTION = (
    "Exact certificate retained as a derived fact, bound to the SHA-256 its packet pins "
    "upstream; no upstream byte is copied."
)


@dataclass(frozen=True)
class Origin:
    """Where one count's certificate came from, as its witness's ``source`` states it.

    `author`, `licence_status`, `raw_asset_retained` and `retention_policy` are what the
    atlas's source index records of it (`build_known_best_atlas._source_index`); a raw
    asset is one whose retained file, or the container entry the url names, is the
    upstream file's exact bytes.
    """

    key: str
    path: Path
    url: str
    revision: str
    retrieved: str
    author: str
    licence_status: str
    raw_asset_retained: bool
    retention_policy: str


@dataclass(frozen=True)
class Source:
    """One adopted result's packet: how a count's certificate and jobs are read."""

    result: str
    key: str
    packet: Path
    certificate: Callable[[int], legacy.Certificate]
    jobs: Callable[[int, legacy.Certificate], Mapping[str, Any]]
    origin: Callable[[int], Origin]
    inputs: Callable[[Sequence[int]], tuple[Path, ...]]
    witness_prefix: str
    claim_limitations: str


# --------------------------------------------------------------------- generic packets


@cache
def _declaration(packet: Path) -> reports.Declaration:
    return reports.load_declaration(packet)


@cache
def _record(packet: Path) -> Mapping[str, Any]:
    path = packet / reports.acquire_source.RECORD
    reports.ensure_private(path)
    record = json.loads(path.read_text(encoding="utf-8"))
    _require(len(record["sources"]) == 1, f"{packet.name}: one acquisition source")
    return cast("Mapping[str, Any]", record)


@cache
def _manifest(packet: Path) -> Mapping[str, str]:
    """The packet's pinned digest of every upstream file in its scope, by upstream path."""
    source = _record(packet)["sources"][0]
    path = REPO / source["subtree_manifest"]
    reports.ensure_private(path)
    digests = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, _, name = line.partition("  ")
        digests[name.removeprefix("./")] = digest
    return digests


def _row(packet: Path, n: int) -> reports.CertificateRow:
    rows = [row for row in _declaration(packet)["certificates"] if row["n"] == n]
    _require(len(rows) == 1, f"n={n}: {packet.name} declares no certificate at this count")
    return rows[0]


def _stored(packet: Path, n: int) -> Path:
    """The one retained file the count's certificate is read from."""
    row = _row(packet, n)
    if "fact" in row:
        return retained_data.compressed_path(packet / row["fact"])
    source = REPO / _record(packet)["sources"][0]["archived_path"]
    plain = source / row["path"]
    return plain if plain.is_file() else retained_data.compressed_path(plain)


def _packet_certificate(packet: Path, n: int) -> legacy.Certificate:
    """The count's certificate, bound to its pinned upstream digest, through its adapter."""
    declaration, row = _declaration(packet), _row(packet, n)
    if "fact" in row:
        certificate = reports.read_fact(packet, declaration, row)
    else:
        stored = _stored(packet, n)
        reports.ensure_private(stored)
        digest = _manifest(packet).get(row["path"])
        raw = stored.read_bytes() if stored.name == PurePosixPath(row["path"]).name else b""
        decoded = read_retained_bytes(stored, limit=reports.MAX_SOURCE_BYTES)
        pinned = hashlib.sha256(raw or decoded).hexdigest()
        _require(
            digest == pinned, f"n={n}: retained certificate differs from its pinned digest"
        )
        certificate = reports.parse_certificate(
            decoded,
            n,
            row["format"],
            reports.row_options(row),
        )
    reports.admit(certificate, row["offered"])
    return certificate


def _receipt(packet: Path, n: int) -> Path:
    shard = packet / reports.shard(n)
    return shard if shard.is_file() else packet / reports.RECEIPT


@cache
def receipt_cases(path: Path, receipt_format: str) -> tuple[Mapping[str, Any], ...]:
    reports.ensure_private(path)
    record = kernel.read_xz(path)
    _require(
        type(record) is dict
        and set(record) == {"format", "routes", "cases"}
        and record["format"] == receipt_format
        and record["routes"] == list(kernel.ROUTES)
        and type(record["cases"]) is list,
        f"{path.name}: incomplete receipt envelope",
    )
    return tuple(cast("list[Mapping[str, Any]]", record["cases"]))


def _validated_jobs(
    rows: Sequence[Mapping[str, Any]],
    certificate: legacy.Certificate,
    *,
    witness_prefix: str,
    claim_limitations: str,
) -> dict[str, Any]:
    """The count's three native jobs, each held to the certificate it decided."""
    found = {str(row.get("control")): row for row in rows if row.get("n") == certificate.n}
    _require(
        set(found) == set(kernel.JOBS)
        and sum(row.get("n") == certificate.n for row in rows) == len(kernel.JOBS),
        f"n={certificate.n}: the receipt does not hold exactly the count's three jobs",
    )
    for control in kernel.JOBS:
        kernel.validate_job(
            found[control],
            certificate,
            control,
            witness_prefix=witness_prefix,
            claim_limitations=claim_limitations,
        )
    return found


def _packet_jobs(packet: Path, n: int, certificate: legacy.Certificate) -> Mapping[str, Any]:
    declaration = _declaration(packet)
    return _validated_jobs(
        receipt_cases(_receipt(packet, n), declaration["receipt_format"]),
        certificate,
        witness_prefix=declaration["witness_prefix"],
        claim_limitations=declaration["claim_limitations"],
    )


def _packet_origin(packet: Path, n: int) -> Origin:
    record = _record(packet)
    source = record["sources"][0]
    raw = "fact" not in _row(packet, n)
    return Origin(
        key=_declaration(packet)["source_key"],
        path=_stored(packet, n),
        url=f"{source['source_url']}/blob/{source['source_commit']}/{_row(packet, n)['path']}",
        revision=source["source_commit"],
        retrieved=str(record["retrieved_at_utc"])[:10],
        author=_declaration(packet)["author"],
        licence_status="MIT" if str(source["license"]).startswith("MIT") else NO_LICENCE,
        raw_asset_retained=raw,
        retention_policy=RAW_RETENTION if raw else DERIVED_RETENTION,
    )


def _packet_inputs(packet: Path, numbers: Sequence[int]) -> tuple[Path, ...]:
    paths = [packet / reports.DECLARATION, packet / reports.acquire_source.RECORD]
    if any("fact" not in _row(packet, n) for n in numbers):
        paths.append(REPO / _record(packet)["sources"][0]["subtree_manifest"])
    paths.extend(_stored(packet, n) for n in numbers)
    paths.extend(dict.fromkeys(_receipt(packet, n) for n in numbers))
    return tuple(paths)


def packet_source(result: str, name: str) -> Source:
    packet = reports.packet_path(name)
    declaration = _declaration(packet)
    return Source(
        result=result,
        key=declaration["source_key"],
        packet=packet,
        certificate=lambda n: _packet_certificate(packet, n),
        jobs=lambda n, certificate: _packet_jobs(packet, n, certificate),
        origin=lambda n: _packet_origin(packet, n),
        inputs=lambda numbers: _packet_inputs(packet, numbers),
        witness_prefix=declaration["witness_prefix"],
        claim_limitations=declaration["claim_limitations"],
    )


# --------------------------------------------------------------------- T-128 and T-130


@cache
def _couzo_451() -> dict[int, legacy.Certificate]:
    """All eight originals, each held to the digest its acquisition roster pins."""
    return couzo_451.read_facts()


def _couzo_451_jobs(_n: int, certificate: legacy.Certificate) -> Mapping[str, Any]:
    return _validated_jobs(
        receipt_cases(couzo_451.receipt_path(), couzo_451.RECEIPT_FORMAT),
        certificate,
        witness_prefix=couzo_451.WITNESS_PREFIX,
        claim_limitations=couzo_451.CLAIM_LIMITATIONS,
    )


def _couzo_451_origin(n: int) -> Origin:
    path = couzo_451.source_pins()[n]["certificate"]["path"]
    # The packet's fact container keeps each certificate's upstream text whole, as
    # ry-xu's does: the entry the url names is the upstream file, byte for byte.
    return Origin(
        key=couzo_451.SOURCE_KEY,
        path=couzo_451.fact_path(),
        url=f"{couzo_451.SOURCE}/blob/{couzo_451.REVISION}/{path}",
        revision=couzo_451.REVISION,
        retrieved="2026-10-08",
        author=COUZO,
        licence_status=NO_LICENCE,
        raw_asset_retained=True,
        retention_policy=RAW_RETENTION,
    )


def _couzo_460_case(n: int) -> Mapping[str, Any]:
    source = couzo_460.read_record(couzo_460.sources_path())
    rows = [row for row in source["cases"] if type(row) is dict and row.get("n") == n]
    _require(len(rows) == 1, f"n={n}: T-130 acquisition holds no row at this count")
    return rows[0]


def _couzo_460_certificate(n: int) -> legacy.Certificate:
    """One derived fact, rebuilt to the pinned certificate bytes its acquisition records.

    The checks are `couzo_followup_reports.read_facts`'s for one count: the witness is
    valid, rebuilds itself, and renders exactly the certificate whose size and digest the
    acquisition row records; its exact side is the row's.
    """
    row = _couzo_460_case(n)
    path = couzo_460.fact_path(n)
    couzo_460.ensure_private(path)
    raw = path.read_bytes()
    _require(len(raw) <= couzo_460.MAX_SOURCE_BYTES, f"n={n}: derived fact exceeds its ceiling")
    try:
        document = load_yaml(raw.decode("utf-8"))
        witness = validate_witness_document(
            document, path=path, fallback_schema=ROOT / "witnesses/witness.schema.yaml"
        )
    except (UnicodeDecodeError, ValueError, WitnessError) as error:
        raise HouseError(
            f"n={n}: T-130 derived fact is not a valid witness: {error}"
        ) from error
    certificate = couzo_460.certificate_from_fact(n, witness)
    text = couzo_460.render(certificate).encode()
    _require(
        document == witness_envelope(couzo_460.fact(certificate), schema=couzo_460.SCHEMA)
        and row["derived_fact"] == f"facts/n-{n:03d}.yaml"
        and row["size"] == len(text)
        and row["sha256"] == hashlib.sha256(text).hexdigest()
        and row["side"] == legacy.literal(certificate.side),
        f"n={n}: T-130 derived fact does not rebuild its pinned certificate",
    )
    return certificate


def _couzo_460_jobs(_n: int, certificate: legacy.Certificate) -> Mapping[str, Any]:
    return _validated_jobs(
        receipt_cases(couzo_460.receipt_path(), couzo_460.RECEIPT_FORMAT),
        certificate,
        witness_prefix=couzo_460.WITNESS_PREFIX,
        claim_limitations=couzo_460.CLAIM_LIMITATIONS,
    )


def _couzo_460_origin(n: int) -> Origin:
    return Origin(
        key=couzo_460.SOURCE_KEY,
        path=couzo_460.fact_path(n),
        url=f"{couzo_460.SOURCE}/blob/{couzo_460.REVISION}/{couzo_460.certificate_path(n)}",
        revision=couzo_460.REVISION,
        retrieved=couzo_460.RETRIEVED,
        author=COUZO,
        licence_status=NO_LICENCE,
        raw_asset_retained=False,
        retention_policy=DERIVED_RETENTION,
    )


def _sources() -> dict[str, Source]:
    sources = [
        Source(
            result="T-128",
            key=couzo_451.SOURCE_KEY,
            packet=couzo_451.PACKET,
            certificate=lambda n: _couzo_451()[n],
            jobs=_couzo_451_jobs,
            origin=_couzo_451_origin,
            inputs=lambda _numbers: couzo_451.private_input_paths(),
            witness_prefix=couzo_451.WITNESS_PREFIX,
            claim_limitations=couzo_451.CLAIM_LIMITATIONS,
        ),
        Source(
            result="T-130",
            key=couzo_460.SOURCE_KEY,
            packet=couzo_460.PACKET,
            certificate=_couzo_460_certificate,
            jobs=_couzo_460_jobs,
            origin=_couzo_460_origin,
            inputs=lambda numbers: (
                couzo_460.sources_path(),
                *(couzo_460.fact_path(n) for n in numbers),
                couzo_460.receipt_path(),
            ),
            witness_prefix=couzo_460.WITNESS_PREFIX,
            claim_limitations=couzo_460.CLAIM_LIMITATIONS,
        ),
        packet_source("T-134", "couzo-exact-certificates-2026-10-09"),
        packet_source("T-136", "squish-481-third-request-2026-10-09"),
        packet_source("T-139", "evand-trio126-2026-10-09"),
        packet_source("T-140", "couzo-certificates-2026-10-10"),
        packet_source("T-141", "evand-record-hunt3-2026-10-10"),
        packet_source("T-146", "evand-regularized-2026-10-10"),
        packet_source("T-147", "pingyou-n207-certificate-2026-10-11"),
        packet_source("T-148", "pingyou-n153-certificate-2026-10-11"),
        packet_source("T-149", "dostashev-records-2026-10-11"),
        packet_source("T-150", "barnett-refinements-2026-10-11"),
        packet_source("T-151", "squish-500-fourth-request-2026-10-11"),
        packet_source("T-152", "couzo-certificates-2026-10-11"),
        packet_source("T-158", "dostashev-records-2026-10-12"),
        packet_source("T-160", "evand-n154-2026-10-12"),
    ]
    return {source.key: source for source in sources}


#: The house this adoption gave each count, by the register result whose certificate it is.
#: `devtools.select_houses` derived it from the register on 11 October 2026; `check`
#: holds every case record named here to it, so an adoption that moves a count again
#: changes or removes its row in the same change, as the second pass of that day did at
#: 146, 153, 155 and 207, the third, for issues 500 and 506, at 270 and 305, the
#: fourth, for issue 528, at 175 and 232, and the fifth, for issue 552, at 154.
ADOPTED: dict[int, str] = {
    70: "T-146",
    84: "T-130",
    86: "T-130",
    102: "T-146",
    103: "T-146",
    105: "T-130",
    108: "T-128",
    123: "T-146",
    126: "T-139",
    127: "T-128",
    129: "T-146",
    131: "T-136",
    132: "T-141",
    146: "T-150",
    153: "T-148",
    154: "T-160",
    155: "T-149",
    156: "T-149",
    175: "T-158",
    176: "T-151",
    180: "T-128",
    181: "T-151",
    207: "T-147",
    209: "T-140",
    211: "T-149",
    228: "T-128",
    232: "T-158",
    236: "T-146",
    237: "T-140",
    238: "T-151",
    239: "T-151",
    258: "T-146",
    259: "T-136",
    261: "T-150",
    263: "T-146",
    264: "T-158",
    267: "T-134",
    269: "T-146",
    270: "T-151",
    271: "T-151",
    272: "T-151",
    292: "T-146",
    295: "T-146",
    302: "T-146",
    303: "T-146",
    304: "T-152",
    305: "T-152",
    306: "T-128",
    307: "T-136",
    308: "T-141",
}
NUMBERS = tuple(sorted(ADOPTED))
#: The counts a later pass adopted, by the day it did; every other count of `ADOPTED` was
#: adopted on `ADOPTED_ON`. The passes of 12 October 2026 adopted issues 500 and 506
#: (T-151, T-152), the second of them reviewed that day, moving 270 and 305 from T-140,
#: issue 528 (T-158), reviewed that day, moving 175 from T-140 and 232 from T-136, and
#: issue 552 (T-160), reviewed that day, moving 154 from T-136, which the first pass of
#: 11 October had adopted there.
LATER_PASSES: dict[str, frozenset[int]] = {
    "2026-10-12": frozenset({154, 175, 176, 181, 232, 238, 239, 264, 270, 271, 272, 304, 305}),
}


def adopted_on(n: int) -> str:
    """The day the count's house was adopted, as an ISO date."""
    _require(type(n) is int and n in ADOPTED, f"n={n}: not a count this adoption houses")
    return next((day for day, counts in LATER_PASSES.items() if n in counts), ADOPTED_ON)


@cache
def sources() -> dict[str, Source]:
    """Each adopted result's source, by source key, built once."""
    return _sources()


def source_for(n: int) -> Source:
    _require(type(n) is int and n in ADOPTED, f"n={n}: not a count this adoption houses")
    found = [source for source in sources().values() if source.result == ADOPTED[n]]
    _require(len(found) == 1, f"n={n}: {ADOPTED[n]} has no house source")
    return found[0]


def source_keys() -> frozenset[str]:
    return frozenset(source.key for source in sources().values())


def numbers_for(key: str) -> tuple[int, ...]:
    return tuple(n for n in NUMBERS if source_for(n).key == key)


def house_path(n: int) -> Path:
    _require(type(n) is int and n in ADOPTED, f"n={n}: not a count this adoption houses")
    return WITNESSES / f"n-{n:03d}.yaml"


def certificate(n: int) -> legacy.Certificate:
    return source_for(n).certificate(n)


def expected_house(n: int) -> dict[str, Any]:
    """The count's house: its certificate as a witness, with its full native result."""
    source = source_for(n)
    exact = source.certificate(n)
    positive = source.jobs(n, exact)["positive"]
    witness = kernel.to_witness(
        exact,
        witness_prefix=source.witness_prefix,
        claim_limitations=source.claim_limitations,
    )
    identifier = f"W-known-best-n{n:03d}"
    witness["id"] = identifier
    witness["claim"]["coordinate_provenance"] = "verified"
    origin = source.origin(n)
    witness["source"] = {
        "key": origin.key,
        "path": origin.path.relative_to(ROOT).as_posix(),
        "url": origin.url,
        "revision": origin.revision,
        "retrieved": origin.retrieved,
    }
    native = copy.deepcopy(positive["exact_verify"])
    native["id"] = identifier
    witness["certificate"] = {
        "kind": "exact-rational-sat",
        "replay": f"uv run --frozen packing-witness verify witnesses/known-best/n-{n:03d}.yaml",
        "result": native,
    }
    return witness


def build_witness(n: int) -> dict[str, Any]:
    """The house, decided again by `sqpack`'s exact verifier and held to the native result."""
    witness = expected_house(n)
    native, verification = legacy.exact_verify(witness)
    _require(
        verification.valid and native == witness["certificate"]["result"],
        f"n={n}: the house's exact decision differs from its retained native job",
    )
    return witness


def side(n: int) -> Fraction:
    return certificate(n).side


def check_houses(numbers: Sequence[int] | None = None) -> None:
    """Hold each retained house to the witness its private inputs rebuild."""
    selected = list(NUMBERS) if numbers is None else list(numbers)
    _require(
        selected
        and len(set(selected)) == len(selected)
        and all(type(n) is int and n in ADOPTED for n in selected),
        "a unique roster of adopted counts is required",
    )
    for n in selected:
        path = house_path(n)
        _require(
            not path.parent.is_symlink()
            and path.parent.resolve().is_relative_to(REPO.resolve()),
            "the house directory escapes the private checkout",
        )
        if path.is_symlink():
            _require(
                not (path.parent / path.readlink()).is_symlink(),
                "a house leaf must be a direct read-only link",
            )
        _require(
            house.bounded_house(path) == expected_house(n),
            f"n={n}: the house geometry or metadata differs from its certificate",
        )


def guard_house_outputs(numbers: Sequence[int]) -> None:
    for n in NUMBERS:
        if n in numbers and not house_path(n).resolve().is_relative_to(REPO.resolve()):
            raise ValueError(f"n={n}: house output escapes the private checkout")


def snapshot_house_links() -> tuple[Path, ...]:
    controls = safe_load((ROOT / "devtools/controls.yaml").read_text(encoding="utf-8"))
    private = {(ROOT / row["file"]).resolve() for row in controls["controls"]}
    return tuple(house_path(n) for n in NUMBERS if house_path(n).resolve() not in private)


def private_input_paths() -> tuple[Path, ...]:
    """Every ordinary file a house check reads, for every adopted count, once each."""
    paths: list[Path] = []
    for source in sources().values():
        counts = [n for n in NUMBERS if ADOPTED[n] == source.result]
        paths.extend(source.inputs(counts))
    return tuple(dict.fromkeys(paths))


def linked_house_problem(path: str, *, repository: Path) -> str | None:
    allowed = {house_path(n).relative_to(REPO).as_posix(): n for n in NUMBERS}
    if repository.resolve() != REPO.resolve() or path not in allowed:
        return "artifact escapes the repository checkout"
    if not house_path(allowed[path]).is_symlink():
        return "artifact is not an admitted house leaf"
    try:
        check_houses([allowed[path]])
    except (ValueError, KeyError, TypeError, OSError) as error:
        return f"house source/custody mismatch: {error}"
    return None


# --------------------------------------------------------------------- custody

#: Where the custody run's receipt is kept: one record for every adopted packet.
CUSTODY_RECEIPT = ROOT / "devtools/house-custody-2026-10-11.json"
CUSTODY_FORMAT = "AdoptedHouseCustody/v1"
#: The worker's deadline: it admits all 50 houses and refuses 32 mutations, two for each
#: of the sixteen packets.
CUSTODY_TIMEOUT = 120


def clear_caches() -> None:
    """Forget every input read, so a check reads the files as they are now."""
    for function in (_declaration, _record, _manifest, receipt_cases, _couzo_451, sources):
        function.cache_clear()


def _forbidden(*_args: object, **_kwargs: object) -> None:
    raise AssertionError("a custody check must not run a geometric decision")


def _mutants(n: int) -> list[tuple[str, Path, Callable[[bytes], bytes]]]:
    """Two late mutations of one count's inputs, each of which a check must refuse."""
    source = source_for(n)

    def verdict(_raw: bytes) -> bytes:
        path = receipt_of(n)
        record = kernel.read_xz(path)
        rows = [
            row for row in record["cases"] if row["n"] == n and row["control"] == kernel.JOBS[2]
        ]
        rows[0]["exact_verify"]["verification_passed"] = True
        kernel.save_xz(path, record)
        return path.read_bytes()

    def original(_raw: bytes) -> bytes:
        """T-128's facts hold each original certificate's text, bound to its digest."""
        path = couzo_451.fact_path()
        value = kernel.read_xz(path)
        row = next(row for row in value["cases"] if row["n"] == n)
        row["source_certificate"] += "\n"
        kernel.save_xz(path, value)
        return path.read_bytes()

    def side(raw: bytes) -> bytes:
        """T-130's derived fact parses to the same witness with any trailing byte added."""
        text = raw.decode("utf-8")
        return text.replace("  side: ", "  side: 1", 1).encode("utf-8")

    if source.result == "T-128":
        certificate, mutate = couzo_451.fact_path(), original
    elif source.result == "T-130":
        certificate, mutate = couzo_460.fact_path(n), side
    else:
        certificate, mutate = _stored(source.packet, n), lambda raw: raw + b"\n"
    return [
        ("outside-control verdict", receipt_of(n), verdict),
        ("certificate bytes", certificate, mutate),
    ]


def receipt_of(n: int) -> Path:
    source = source_for(n)
    if source.result == "T-128":
        return couzo_451.receipt_path()
    if source.result == "T-130":
        return couzo_460.receipt_path()
    return _receipt(source.packet, n)


def worker_custody() -> dict[str, Any]:
    """Run inside a private worker: admit every house, refuse late mutations, restore.

    No geometric decider may run. Each mutation is written in the worker's own copy of
    an input and restored byte for byte, and the check must refuse it and then pass again.
    """
    legacy.exact_verify = _forbidden
    kernel.run_case = _forbidden
    legacy.independent.check_squares = _forbidden
    inputs = private_input_paths()
    for path in inputs:
        _require(path.is_file() and not path.is_symlink(), f"{path}: not an ordinary file")
    check_houses()
    refused = []
    for n in sorted({min(numbers_for(key)) for key in source_keys()}):
        for name, path, mutate in _mutants(n):
            original = path.read_bytes()
            try:
                changed = mutate(original)
                _require(changed != original, f"n={n}: the {name} mutation changed nothing")
                path.write_bytes(changed)
                clear_caches()
                try:
                    check_houses([n])
                except Exception:  # noqa: BLE001 -- any refusal is the outcome required
                    refused.append(f"{source_for(n).result} n={n}: {name}")
                else:
                    raise AssertionError(f"n={n}: a late {name} mutation was admitted")
            finally:
                path.write_bytes(original)
                clear_caches()
            check_houses([n])
    return {"houses": len(NUMBERS), "inputs": len(inputs), "refused": refused}


def custody(*, write: bool = True) -> dict[str, Any]:
    """Clone a private worker, run `worker_custody` in it, and keep the receipt."""
    import os  # noqa: PLC0415
    import platform  # noqa: PLC0415
    import subprocess  # noqa: PLC0415
    import tempfile  # noqa: PLC0415
    import time  # noqa: PLC0415

    from devtools import run_negative_controls as controls  # noqa: PLC0415
    from sqpack import retained_json  # noqa: PLC0415

    inputs = private_input_paths()
    _require(set(inputs) <= set(controls.COPY_SEPARATELY), "an input is not copied privately")
    originals = {path: path.read_bytes() for path in inputs}
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="house-custody-") as scratch:
        tree = Path(scratch) / "snapshot"
        controls.clone_tree(tree)
        setup = time.monotonic() - started
        for path, raw in originals.items():
            copied = tree / path.relative_to(REPO)
            _require(
                copied.is_file() and not copied.is_symlink() and copied.read_bytes() == raw,
                f"{path.relative_to(REPO)}: not an ordinary private copy in the worker",
            )
        call = time.monotonic()
        completed = subprocess.run(
            [sys.executable, "-m", "devtools.upper_bound_houses", "worker-custody"],
            cwd=tree / "packing",
            env=controls.control_environment(tree, Path(scratch) / "pycache"),
            capture_output=True,
            text=True,
            check=False,
            timeout=CUSTODY_TIMEOUT,
        )
        call = time.monotonic() - call
        _require(completed.returncode == 0, completed.stdout + completed.stderr)
        child = json.loads(completed.stdout.strip().splitlines()[-1])
        for path, raw in originals.items():
            _require(
                (tree / path.relative_to(REPO)).read_bytes() == raw,
                f"{path.relative_to(REPO)}: the worker did not restore it",
            )
    _require(all(path.read_bytes() == raw for path, raw in originals.items()), "inputs moved")
    receipt = {
        "format": CUSTODY_FORMAT,
        "outcome": "PASS",
        "adopted_on": ADOPTED_ON,
        "command": "python -m devtools.upper_bound_houses custody",
        "runtime": f"CPython {platform.python_version()}",
        "host": platform.node() or os.uname().nodename,
        "setup_seconds": round(setup, 2),
        "call_seconds": round(call, 2),
        "child_timeout_seconds": CUSTODY_TIMEOUT,
        "snapshot_cap_bytes": controls.SNAPSHOT_MAX_BYTES,
        "snapshot_source_bytes": controls.snapshot_source_bytes(),
        "fresh_geometric_deciders": False,
        "houses": {str(n): ADOPTED[n] for n in NUMBERS},
        "inputs": [
            {
                "path": path.relative_to(REPO).as_posix(),
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
            }
            for path, raw in originals.items()
        ],
        "mutations_refused_and_restored": child["refused"],
        "original_inputs_byte_equal": True,
        "restored_worker_inputs_byte_equal": True,
    }
    if write:
        CUSTODY_RECEIPT.write_text(
            retained_json.dumps(receipt, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    return receipt


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", 1)[0])
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="hold each retained house to its inputs")
    check.add_argument("--n", type=int, nargs="+", help="only these counts")
    sub.add_parser("inputs", help="print every private input and its size")
    sub.add_parser(
        "custody", help="run the custody check in a private worker; keep its receipt"
    )
    sub.add_parser("worker-custody", help="the worker side of custody, run by custody")
    arguments = parser.parse_args(argv)
    if arguments.command == "custody":
        receipt = custody()
        refused = len(receipt["mutations_refused_and_restored"])
        print(
            f"custody passed: {len(receipt['houses'])} houses, {len(receipt['inputs'])} "
            f"inputs, {refused} mutations refused and restored, {receipt['call_seconds']} s "
            f"in the worker; {CUSTODY_RECEIPT.relative_to(REPO)}"
        )
        return 0
    if arguments.command == "worker-custody":
        print(json.dumps(worker_custody()))
        return 0
    if arguments.command == "inputs":
        paths = private_input_paths()
        for path in paths:
            print(f"{path.stat().st_size:>9}  {path.relative_to(REPO).as_posix()}")
        print(f"{sum(path.stat().st_size for path in paths):>9}  {len(paths)} inputs")
        return 0
    selected = arguments.n or list(NUMBERS)
    check_houses(selected)
    print(f"OK: {len(selected)} adopted houses rebuild from their private inputs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
