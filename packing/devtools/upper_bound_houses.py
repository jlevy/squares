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
Every house's packet is read through its declaration (`packet_source`): the adoption of
17 October 2026 moved the last counts of `T-128` and `T-130`, whose packets carried
readers of their own, to `T-174`. Issue 678's packet (`T-223`) carries no import
declaration: its replay module reads it, and `couzo_678_source` reads its two counts of
the case corpus through that module, the certificate bound to its pinned digest and the
kernel's three jobs kept in the packet's own receipt (`couzo_678_replay house-jobs`).

**No geometry runs in a check.** `check_houses` admits the inputs and compares the
retained witness with the one they rebuild; `build_witness`, which writes a house, also
decides it again with `sqpack`'s exact verifier and holds the result to the retained
native one.

Usage, from ``packing/`` with the project interpreter::

    python -m devtools.upper_bound_houses check [--n N ...]
    python -m devtools.upper_bound_houses inputs
    python -m devtools.upper_bound_houses sizes [--n N ...]

**Sizes.** `sizes` measures the witnesses an adoption would write, before it writes them:
each staged count's (`select_houses.PENDING_ADOPTION`) house rebuilt as this module
builds one, in bytes in a checkout and as Git stores the blob, beside the witness it
replaces, with the set's totals and its largest. That is OR-18's unit, the sum of the
blobs a clone downloads (`stored_size`), by which the house rule decides whether a house's
witnesses go into Git or a hosted data release (packing/campaign/result-import.md, "The
House Rule"; review C9 of #660).
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import zlib
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from pathlib import Path, PurePosixPath
from typing import Any, NamedTuple, cast

from devtools import couzo_678_replay as couzo_678
from devtools import evand_arrangement_reports as kernel
from devtools import retained_data
from devtools import squish_second_update_house_links as house
from devtools import upper_bound_reports as reports
from devtools.retained_data import read_retained_bytes
from sqpack.witness import witness_document
from sqpack.yamlio import safe_load

legacy = reports.legacy
ROOT = reports.ROOT
REPO = reports.REPO
WITNESSES = ROOT / "witnesses/known-best"
ADOPTED_ON = "2026-10-11"
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
    #: The one retained file a count's certificate is read from, and the receipt of its
    #: three jobs, which the custody check mutates (`_mutants`).
    stored: Callable[[int], Path]
    receipt: Callable[[int], Path]


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
        stored=lambda n: _stored(packet, n),
        receipt=lambda n: _receipt(packet, n),
    )


def _couzo_678_path(n: int) -> Path:
    _require(n in couzo_678.HOUSE_COUNTS, f"n={n}: issue 678 houses only 204 and 260")
    return couzo_678.SOURCE / couzo_678.house_path(n)


def _couzo_678_origin(n: int) -> Origin:
    path = couzo_678.PACKET / reports.acquire_source.RECORD
    reports.ensure_private(path)
    record = json.loads(path.read_text(encoding="utf-8"))
    stored = _couzo_678_path(n)
    return Origin(
        key=couzo_678.SOURCE_KEY,
        path=stored,
        url=(
            f"{couzo_678.SOURCE_URL}/blob/{couzo_678.PIN}/"
            f"{stored.relative_to(couzo_678.SOURCE).as_posix()}"
        ),
        revision=couzo_678.PIN,
        retrieved=str(record["retrieved_at_utc"])[:10],
        author="Francisco Couzo",
        licence_status=NO_LICENCE,
        raw_asset_retained=True,
        retention_policy=RAW_RETENTION,
    )


def _couzo_678_jobs(n: int, certificate: legacy.Certificate) -> Mapping[str, Any]:
    _require(n == certificate.n, f"n={n}: the certificate is another count's")
    return _validated_jobs(
        receipt_cases(couzo_678.HOUSE_JOBS, couzo_678.HOUSE_FORMAT),
        certificate,
        witness_prefix=couzo_678.WITNESS_PREFIX,
        claim_limitations=couzo_678.CLAIM_LIMITATIONS,
    )


def couzo_678_source() -> Source:
    """Issue 678's certificates at 204 and 260 (T-223), read through its replay module.

    The packet carries no import declaration. Each certificate is read once its bytes
    equal the digest the packet's manifest pins (`couzo_678_replay.house_certificate`),
    and its jobs from the packet's own receipt of the kernel's three jobs.
    """
    return Source(
        result="T-223",
        key=couzo_678.SOURCE_KEY,
        packet=couzo_678.PACKET,
        certificate=couzo_678.house_certificate,
        jobs=_couzo_678_jobs,
        origin=_couzo_678_origin,
        inputs=lambda numbers: (
            couzo_678.PACKET / reports.acquire_source.RECORD,
            couzo_678.MANIFEST,
            *(_couzo_678_path(n) for n in numbers),
            couzo_678.HOUSE_JOBS,
        ),
        witness_prefix=couzo_678.WITNESS_PREFIX,
        claim_limitations=couzo_678.CLAIM_LIMITATIONS,
        stored=_couzo_678_path,
        receipt=lambda _n: couzo_678.HOUSE_JOBS,
    )


def _sources() -> dict[str, Source]:
    sources = [
        packet_source("T-134", "couzo-exact-certificates-2026-10-09"),
        packet_source("T-136", "squish-481-third-request-2026-10-09"),
        packet_source("T-139", "evand-trio126-2026-10-09"),
        packet_source("T-146", "evand-regularized-2026-10-10"),
        packet_source("T-173", "mishapolk-exact-certificates-2026-10-12"),
        packet_source("T-174", "pingyou-pr574-certificates-2026-10-13"),
        packet_source("T-182", "couzo-certificates-2026-10-13"),
        packet_source("T-186", "mishapolk-kkt-refinements-2026-10-14"),
        packet_source("T-187", "evand-n146-2026-10-14"),
        packet_source("T-188", "couzo-verified-bounds-2026-10-14"),
        packet_source("T-190", "couzo-n237-2026-10-15"),
        packet_source("T-195", "pingyou-pr622-certificate-2026-10-15"),
        packet_source("T-196", "de-winter-upper-bounds-227-229-260-2026-10-17"),
        packet_source("T-197", "evand-n155-explorer-2026-10-17"),
        packet_source("T-199", "evand-n229-dilation-update-2026-10-18"),
        packet_source("T-218", "evand-n236-2026-10-16"),
        packet_source("T-219", "evand-n271-2026-10-17"),
        packet_source("T-220", "evand-n183-subgrid-2026-10-19"),
        packet_source("T-221", "evand-n308-2026-10-19"),
        packet_source("T-222", "evand-n154-sweep-2026-10-20"),
        couzo_678_source(),
        packet_source("T-224", "evand-n270-sweep-2026-10-20"),
        packet_source("T-225", "evand-regularized-2026-10-20"),
    ]
    found = {source.result: source for source in sources}
    # Two results may read one packet (T-181 and T-182 both read issue 586's), so the
    # sources are keyed by result, not by source key.
    _require(len(found) == len(sources), "one house source per result")
    return found


#: The house this adoption gave each count, by the register result whose certificate it is.
#: `devtools.select_houses` derived it from the register on 11 October 2026; `check`
#: holds every case record named here to it, so an adoption that moves a count again
#: changes or removes its row in the same change, as the second pass of that day did at
#: 146, 153, 155 and 207, the third, for issues 500 and 506, at 270 and 305, the
#: fourth, for issue 528, at 175 and 232, the fifth, for issue 552, at 154, and the
#: pass of 15 October 2026, for issues 573, 575, 583, 586 and 593, at 153, 154, 207,
#: 211, 237, 241, 302 and 304, and, for the next candidates where PR 574's (T-174) were
#: held for the owner (the hold the house rule lifted, `select_houses.LIFTED`), at 105,
#: 129, 146, 156, 176, 204, 261, 271, 272 and 303, and the pass of 16 October 2026, for
#: the 16 October review of issues 506 to 607, at 129, 146, 154, 156, 175, 176, 204, 211,
#: 232, 237, 264, 271, 302, 303 and 304, and the pass of 17 October 2026, the house rule's
#: adoption of PingYou Ltd's PR 574 (T-174), at 37 of its rational counts, 68, 84, 86, 103,
#: 105, 108, 110, 127, 130 to 132, 155, 172, 179 to 182, 206, 208 to 210, 228, 238 to 240,
#: 261, 263, 268 to 270, 272, 273, 297 and 305 to 308. The same day adopted PR 622's
#: certificate (T-195) at 29. The pass of 19 October 2026 adopted Evan Daniel's
#: certificates of issues 669 (T-197), 674 (T-199), 659 (T-218), 664 (T-219) and 680
#: (T-220) at 155, 229, 236, 271 and 183, and the pass of 20 October 2026 his certificates
#: of issues 694 (T-222) and 689 (T-221) at 154 and 308, Francisco Couzo's certificate of
#: issue 678 (T-223) at 204 and Joost de Winter's certificates of issue 668 (T-196) at 227
#: and 260. The pass of 21 October 2026 adopted Evan Daniel's certificate of issue 703
#: (T-224) at 270 and Couzo's of issue 678 (T-223) at 260, which replaced T-196 there. The
#: pass of 22 October 2026 adopted Evan Daniel's regularized views of 20 October (T-225) at
#: 204 and 260 from T-223, at 227 from T-196, once Francisco Couzo's #672 was registered
#: as T-227 and T-225's item there named it, and at 229 from T-199.
ADOPTED: dict[int, str] = {
    29: "T-195",
    68: "T-174",
    70: "T-146",
    84: "T-174",
    86: "T-174",
    102: "T-146",
    103: "T-174",
    105: "T-174",
    108: "T-174",
    110: "T-174",
    123: "T-146",
    126: "T-139",
    127: "T-174",
    129: "T-186",
    130: "T-174",
    131: "T-174",
    132: "T-174",
    146: "T-187",
    153: "T-173",
    154: "T-222",
    155: "T-197",
    156: "T-186",
    172: "T-174",
    175: "T-186",
    176: "T-186",
    179: "T-174",
    180: "T-174",
    181: "T-174",
    182: "T-174",
    183: "T-220",
    204: "T-225",
    206: "T-174",
    207: "T-173",
    208: "T-174",
    209: "T-174",
    210: "T-174",
    211: "T-188",
    227: "T-225",
    228: "T-174",
    229: "T-225",
    232: "T-186",
    236: "T-218",
    237: "T-190",
    238: "T-174",
    239: "T-174",
    240: "T-174",
    241: "T-182",
    258: "T-146",
    259: "T-136",
    260: "T-225",
    261: "T-174",
    263: "T-174",
    264: "T-186",
    267: "T-134",
    268: "T-174",
    269: "T-174",
    270: "T-224",
    271: "T-219",
    272: "T-174",
    273: "T-174",
    292: "T-146",
    295: "T-146",
    297: "T-174",
    302: "T-186",
    303: "T-186",
    304: "T-186",
    305: "T-174",
    306: "T-174",
    307: "T-174",
    308: "T-221",
}
NUMBERS = tuple(sorted(ADOPTED))
#: The counts a later pass adopted, by the day it did; every other count of `ADOPTED` was
#: adopted on `ADOPTED_ON`. The passes of 12 October 2026 adopted issues 500 and 506
#: (T-151, T-152), the second of them reviewed that day, moving 270 and 305 from T-140,
#: issue 528 (T-158), reviewed that day, moving 175 from T-140 and 232 from T-136, and
#: issue 552 (T-160), reviewed that day, moving 154 from T-136, which the first pass of
#: 11 October had adopted there. The pass of 15 October 2026 adopted the 14 October
#: reviews of issues 573, 575, 583, 586 and 593: issue 573 (T-173) at 153 and 207 from
#: PingYou Ltd's T-148 and T-147, issue 586 (T-182) at 154 from T-160, at 211 from T-149
#: and at 241, first adopted here, from Evan Daniel's exact optimum (T-098), issue 593
#: (T-183) at 237 from T-140, issue 583's 302 (T-181) from T-146, and issue 575 (T-175)
#: at 304 from T-152. The same day, once a hold skipped only the held entry (reviews A
#: and B of PR 614), it adopted the next candidates where PR 574's (T-174) are held:
#: issue 562 (T-162) at 129 and 303 from T-146 and at 204, first adopted here, from the
#: Kingbird catalogue; issue 561 (T-161) at 156 from T-149 and at 271 from T-151; T-165
#: at 176 from T-151; and PingYou Ltd's re-solves (T-168 to T-171) at 146 and 261 from
#: T-150, at 105 from T-130 and at 272 from T-151. The pass of 16 October 2026 adopted the
#: 16 October review of issues 506 to 607: Mykhailo Polkovskyi's KKT refinements (T-186)
#: at 129, 204 and 303 from T-162, at 154 from T-182, at 156 and 271 from T-161, at 175,
#: 232 and 264 from T-158, at 176 from T-165, at 302 from T-181 and at 304 from T-175;
#: issue 606 (T-187) at 146 from T-168; Francisco Couzo's 211 (T-188) from T-182; and his
#: 237 of 15 October (T-190) from T-183. The pass of 17 October 2026, the first under the
#: owner's house rule, adopted PR 574 (T-174) at 37 of its rational counts, from the
#: houses of T-128, T-130, T-136, T-140, T-141, T-146, T-149, T-151, T-152, T-169, T-170
#: and T-171 and, at the 13 counts it first adopts (68, 110, 130, 172, 179, 182, 206, 208,
#: 210, 240, 268, 273 and 297), from the case records' own. Twelve of its other rational
#: counts are below it by issue 639's algebraic sides (T-193, #658), which wait for the
#: writer, and 236 by Evan Daniel's issue 659, whose import adopts it. The same day
#: adopted PR 622's certificate (T-195) at 29 from T-155, the case's replay of the
#: Kingbird catalogue's packing, which no pass had adopted before. The pass of 19 October
#: 2026 adopted Evan Daniel's certificates after the 19 October review: issue 669 (T-197)
#: at 155 from T-174, issue 674's update (T-199) at 229, first adopted here, from the case
#: record's own (the Kingbird catalogue's packing, verified by T-155's exact ceiling),
#: issue 659 (T-218) at 236 from T-146, which takes 236 off T-174's staged adoption,
#: issue 664 (T-219) at 271 from T-186, and his original certificate of issue 680 (T-220)
#: at 183 from the case's trivial 14 x 14 grid, which no pass had adopted before. The pass
#: of 20 October 2026 adopted Evan Daniel's certificates after the 20 October review: issue
#: 694 (T-222) at 154 from T-186, continuing Francisco Couzo's #586 arrangement, and issue
#: 689 (T-221) at 308 from T-174, another arrangement of the two-wedge design; after their
#: own reviews of that day, Couzo's certificate of issue 678 (T-223) at 204 from T-186,
#: below T-193's algebraic side as well, and Joost de Winter's certificates of issue 668
#: (T-196) at 227 and 260 from the case records' own (the Kingbird catalogue's packings,
#: verified by T-155's exact ceilings), which no pass had adopted before; at 229 T-199
#: stays. The pass of 21 October 2026 adopted Evan Daniel's certificate of issue 703
#: (T-224) after the 21 October review, at 270 from T-174: another arrangement of the
#: design of Nate Chaoweeraprasit's #500 packing, which T-174 refines, found from that
#: packing; and, once #704 had landed, Couzo's certificate of issue 678 (T-223) at 260
#: from T-196, 2.56e-05 below it, so that 260 moved twice in two days. The pass of 22
#: October 2026 adopted Evan Daniel's regularized views of 20 October (T-225) after the 21
#: October review of them: his solved views of Couzo's issue-678 packings at 204 and 260,
#: 1.39e-09 and 2.51e-11 below T-223, and of his own issue-674 packing at 229, 1.91e-11
#: below T-199; and, once Couzo's #672 was registered (T-227) and T-225's item there named
#: it, his solved view of #672's packing at 227, 1.71e-04 below de Winter's T-196.
#: A count a pass names keeps its place in the earlier passes' sets, which their archives
#: hold; it was adopted on the latest day that names it.
LATER_PASSES: dict[str, frozenset[int]] = {
    "2026-10-12": frozenset({154, 175, 176, 181, 232, 238, 239, 264, 270, 271, 272, 304, 305}),
    "2026-10-15": frozenset(
        {
            105,
            129,
            146,
            153,
            154,
            156,
            176,
            204,
            207,
            211,
            237,
            241,
            261,
            271,
            272,
            302,
            303,
            304,
        }
    ),
    "2026-10-16": frozenset(
        {129, 146, 154, 156, 175, 176, 204, 211, 232, 237, 264, 271, 302, 303, 304}
    ),
    "2026-10-17": frozenset(
        {
            29,
            68,
            84,
            86,
            103,
            105,
            108,
            110,
            127,
            130,
            131,
            132,
            155,
            172,
            179,
            180,
            181,
            182,
            206,
            208,
            209,
            210,
            228,
            238,
            239,
            240,
            261,
            263,
            268,
            269,
            270,
            272,
            273,
            297,
            305,
            306,
            307,
            308,
        }
    ),
    "2026-10-19": frozenset({155, 183, 229, 236, 271}),
    "2026-10-20": frozenset({154, 204, 227, 260, 308}),
    "2026-10-21": frozenset({260, 270}),
    "2026-10-22": frozenset({204, 227, 229, 260}),
}


def adopted_on(n: int) -> str:
    """The day the count's house was adopted, as an ISO date."""
    _require(type(n) is int and n in ADOPTED, f"n={n}: not a count this adoption houses")
    return max((day for day, counts in LATER_PASSES.items() if n in counts), default=ADOPTED_ON)


@cache
def sources() -> dict[str, Source]:
    """Each adopted result's source, by result, built once."""
    return _sources()


def source_for(n: int) -> Source:
    _require(type(n) is int and n in ADOPTED, f"n={n}: not a count this adoption houses")
    found = sources().get(ADOPTED[n])
    _require(found is not None, f"n={n}: {ADOPTED[n]} has no house source")
    return cast("Source", found)


def source_keys() -> frozenset[str]:
    return frozenset(source.key for source in sources().values())


def numbers_for(key: str) -> tuple[int, ...]:
    return tuple(n for n in NUMBERS if source_for(n).key == key)


def numbers_of(result: str) -> tuple[int, ...]:
    """The counts one adopted result houses."""
    return tuple(n for n in NUMBERS if ADOPTED[n] == result)


def house_path(n: int) -> Path:
    _require(type(n) is int and n in ADOPTED, f"n={n}: not a count this adoption houses")
    return WITNESSES / f"n-{n:03d}.yaml"


def certificate(n: int) -> legacy.Certificate:
    return source_for(n).certificate(n)


def expected_house(n: int) -> dict[str, Any]:
    """The count's house: its certificate as a witness, with its full native result."""
    return _house_witness(n, source_for(n))


def _house_witness(n: int, source: Source) -> dict[str, Any]:
    """The witness `source` makes the house at `n`: its certificate, with its native result."""
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


#: The schema reference a house witness carries, as the atlas writes the file.
WITNESS_SCHEMA_REFERENCE = "../witness.schema.yaml"


def stored_size(data: bytes) -> int:
    """The bytes Git keeps for a file: its blob object, the header ``blob <size>`` and a NUL
    then the content, compressed by zlib at its default level, as Git compresses an object
    in a pack (`core.compression`) before any delta. A loose object, as `git hash-object -w`
    first writes it, is compressed at Git's default loose level, a little larger."""
    return len(zlib.compress(b"blob %d\x00" % len(data) + data, zlib.Z_DEFAULT_COMPRESSION))


class Sizes(NamedTuple):
    """One staged count's witness, as the adoption would write it and as it is now."""

    n: int
    house: str
    checkout: int
    stored: int
    now_checkout: int
    now_stored: int


def staged_sizes(numbers: Sequence[int] | None = None) -> tuple[list[Sizes], list[str]]:
    """The witness each staged count's adoption would write, measured, and the counts it
    cannot build: an algebraic house, which no writer here takes yet (think-ot5c)."""
    from devtools import select_houses  # noqa: PLC0415

    staged = select_houses.PENDING_ADOPTION
    selected = sorted(staged) if numbers is None else list(numbers)
    _require(
        all(n in staged for n in selected),
        "only counts staged in select_houses.PENDING_ADOPTION are measured",
    )
    # Only the staged results are read: `select_houses --check` holds each staging to the
    # selection, and this measures what the staged house's adoption would write.
    names = {staged[n].house for n in selected}
    results = [entry for entry in select_houses.load_results() if str(entry["id"]) in names]
    found = select_houses.candidates(results, select_houses.load_evidence())
    measured: list[Sizes] = []
    skipped: list[str] = []
    for n in selected:
        house = next((c for c in found.get(n, ()) if c.result == staged[n].house), None)
        _require(house is not None, f"n={n}: {staged[n].house} is no candidate there")
        assert house is not None
        packet = reports.import_packet(house.source_key)
        if house.algebraic or packet is None:
            skipped.append(f"n={n}: {house.result}'s side is algebraic; no writer takes it yet")
            continue
        witness = _house_witness(n, packet_source(house.result, packet.name))
        data = witness_document(witness, schema=WITNESS_SCHEMA_REFERENCE).encode("utf-8")
        current = (WITNESSES / f"n-{n:03d}.yaml").read_bytes()
        measured.append(
            Sizes(
                n,
                house.result,
                len(data),
                stored_size(data),
                len(current),
                stored_size(current),
            )
        )
    return measured, skipped


def _megabytes(size: int) -> str:
    return f"{size / 1e6:.2f} MB"


def print_sizes(numbers: Sequence[int] | None = None) -> int:
    measured, skipped = staged_sizes(numbers)
    heading = ("n", "house", "checkout", "stored", "now", "now stored")
    print("{:>4}  {:6}  {:>10}  {:>9}  {:>9}  {:>10}".format(*heading))
    for row in measured:
        print(
            f"{row.n:>4}  {row.house:6}  {row.checkout:>10}  {row.stored:>9}  "
            f"{row.now_checkout:>9}  {row.now_stored:>10}"
        )
    for line in skipped:
        print(f"skipped {line}")
    if not measured:
        return 0
    checkout = sum(row.checkout for row in measured)
    stored = sum(row.stored for row in measured)
    now_checkout = sum(row.now_checkout for row in measured)
    now_stored = sum(row.now_stored for row in measured)
    largest = max(measured, key=lambda row: row.checkout)
    # History keeps every blob: the witnesses replaced stay in it, so an adoption adds its
    # new blobs' whole size to what a clone downloads, and the tree's difference is only
    # what a checkout grows by (review D3 of #660).
    print(
        f"{len(measured)} witness{'' if len(measured) == 1 else 'es'}: "
        f"{_megabytes(checkout)} in a checkout and "
        f"{_megabytes(stored)} as Git stores them, which history keeps, the replaced "
        f"witnesses staying in it; in the tree they replace {_megabytes(now_checkout)} and "
        f"{_megabytes(now_stored)}, so a checkout grows by "
        f"{_megabytes(checkout - now_checkout)} and the tree's blobs by "
        f"{_megabytes(stored - now_stored)}; the largest, n = "
        f"{largest.n}, {_megabytes(largest.checkout)} and {_megabytes(largest.stored)}"
    )
    return 0


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
#: The worker's deadline: it admits all 70 house best packings and refuses 44 mutations,
#: two for each of the twenty-two results (22.8 s in the worker on 21 October 2026, with
#: 9.78 s of setup at a load average of about six, after the merge of main 970e89de8 and
#: the adoption at 260 that day; 23.84 s for 69 on this branch after the merge of main
#: 51ac9d7ee, at a load average of about six; 23.33 s for 70 on #704's branch after the
#: merge of main 7eeab1f5e, at about four; 21.69 s there after the merge of main 51ac9d7ee,
#: at about one; 23.62 s on main after the adoption at 270, at about four; 25.76 s on 20
#: October 2026, after the adoptions at 154 and 308 and at 227 and 260, at about nine;
#: 32.08 s that day after the adoption at 204 and 260 on this branch, at about seventeen;
#: 20.55 s after the adoption at 154 and 308 alone, with 7.76 s of setup, and 24.0 s after
#: the merge with main that morning, with 14.25 s; earlier readings: 59.18 s for 67 of them
#: on 19 October at a load average of about seven, 28.36 s for 65 on 17 October at about
#: five, and 48.95 s for 52 on 16 October at about ten).
CUSTODY_TIMEOUT = 120


def clear_caches() -> None:
    """Forget every input read, so a check reads the files as they are now."""
    for function in (_declaration, _record, _manifest, receipt_cases, sources):
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

    return [
        ("outside-control verdict", receipt_of(n), verdict),
        ("certificate bytes", source.stored(n), lambda raw: raw + b"\n"),
    ]


def receipt_of(n: int) -> Path:
    return source_for(n).receipt(n)


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
    for n in sorted({min(numbers_of(result)) for result in sources()}):
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
    sizes = sub.add_parser(
        "sizes",
        help="measure the witnesses the staged adoptions would write, as Git stores them",
    )
    sizes.add_argument("--n", type=int, nargs="+", help="only these staged counts")
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
    if arguments.command == "sizes":
        return print_sizes(arguments.n)
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
