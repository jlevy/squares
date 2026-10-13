"""Audit and replay Hosono's linear certificates: points, segments and rectangles.

wand125/square-packing-bounds adds two certificates of a kind its superseded
``s(50) >= 147/20`` rung, ``mixed_n50_L735``, first used: a nonnegative measure of point
masses, uniform segments and uniform rectangles, each primitive standing for its eight
D4 images, with exact rational geometry and a total mass of ``n - 1/100000``, such that
every closed core of side ``9977/10000`` at each of 201 net half-angles of step
``83/40000`` has measure at least 1. They are

- ``certificates/mixed_n101_L1028`` (at ``af1db07``, unchanged at ``0c35d90``):
  ``s(101) >= 257/25`` from 333 point, 897 segment and 4 rectangle orbits;
- ``certificates/mixed_n83_L935`` (at ``0c35d90``): ``s(83) >= 187/20`` from 86 point,
  222 segment and 774 rectangle orbits; and
- ``certificates/mixed_n82_L932`` (at ``58f153f``, pinned at ``b00fc70`` in its own
  packet): ``s(82) >= 233/25`` from 86 point, 222 segment and 774 rectangle orbits.

All three are decided by ``code/unified_linear_verify.cpp`` (SHA-256 ``0249726a...``)
through its Python driver, which re-exports each angle's input from the candidate and
requires the checker to return the stored record. The checker is byte for byte the one in
the ``mixed_n50_L735`` bundle the 2026-09-28 packet pins, and every file of each
directory's ``code/`` is byte for byte the same. The 2026-10-02 linear packet retains the
seven files of ``code/`` that no other packet holds; the other six are the retained
``mixed_n50_L740/code/`` copies. `LINEAR` names each certificate with its packet and
statement.

``linear-audit`` recomputes from the packet's retained bytes, importing no source code,
every premise that is plain arithmetic: the pinned digests, the schema, the stated count,
side, core and orbit counts, each primitive inside the container and nondegenerate with a
nonnegative mass, the exact total ``n - 1/100000``, the D4 expansion and its invariance,
the candidate digest by the source's rule, the net's containment, a positive centre domain
at all 201 angles, the checker's and the code's identity, a replay record for each angle,
and the source audit's certificate and tarball digests. It decides no coverage.

``linear-fetch`` obtains the pinned tarball, refuses it unless its SHA-256 and size are the
pinned ones, unpacks it afresh, binds every file of the bundle to the packet, assembles
the shipped ``code/`` from the retained copies, repeats the driver's preconditions, and
binds every angle's input to the candidate by an independent enclosure check.
``linear-replay`` does that for a range of angles and then replays each with the shipped
``replay_angle`` and the checker the shipped ``compile_verifier`` builds, writing receipts
as each angle finishes; it is the mixed range driver
(`devtools.audit_wand125_point_and_mixed.replay_directions`), so ``linear-merge`` is
``mixed_merge`` and a certificate can be split across sessions. ``linear-plan`` splits the
angles by recorded node counts, ``linear-price`` estimates each replay from timed single
angles, and ``linear-control`` is stage 4 of ``campaign/result-import.md``: the original
and two mutations on one net direction, each mutation provably uncovered at an exact
witness centre, the original accepted and both refused.

Usage, from ``packing/`` with the project interpreter::

    .venv/bin/python3 -m devtools.audit_wand125_linear linear-audit [--packet PACKET] \\
        [--check] [--tarball TARBALL ...]
    .venv/bin/python3 -m devtools.audit_wand125_linear linear-fetch n101 --work W --out F
    .venv/bin/python3 -m devtools.audit_wand125_linear linear-replay n101 \\
        --range 0-100 --work W --workers 4 [--stop-after-hours H] [--via auto|url|git]
    .venv/bin/python3 -m devtools.audit_wand125_linear linear-merge n101 [--check]
    .venv/bin/python3 -m devtools.audit_wand125_linear linear-plan n83 --parts 4
    .venv/bin/python3 -m devtools.audit_wand125_linear linear-price
    .venv/bin/python3 -m devtools.audit_wand125_linear linear-control n101 --work W
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import resource
import shutil
import subprocess
import sys
import time
from collections import Counter
from collections.abc import Iterable, Mapping
from concurrent.futures import Future, ProcessPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import audit_wand125_point_and_mixed as mixed
from devtools.audit_wand125_rectangles import (
    CONTROL_FACTOR,
    coverage_exact,
    heaviest,
    net_rotation,
)
from devtools.retained_data import read_retained_bytes

LINEAR_REVISION = "0c35d909764997ead04dfd90081c9fe9af8d07f2"
LINEAR_PACKET = mixed.WEB / "wand125-linear-certificates-2026-10-02"
N82_REVISION = "b00fc70f1904e9b1b567afee056d347f911209e8"
N82_PACKET = mixed.WEB / "wand125-linear-n82-2026-10-02"
LINEAR_SCHEMA = "point_line_rectangle_v1"
#: ``unified_linear_verify.cpp``, the checker every linear certificate names.
LINEAR_CHECKER_SHA256 = "0249726ab1e67dc481e0c53f43b524902a48f95d051b1b08865a3cf3ef89a06d"
LINEAR_STATUS = "ALL_LINEAR_ANGLES_VERIFIED_AND_REPLAYED"
LINEAR_REPLAYED = "LINEAR_ANGLE_REPLAYED"
#: The retained copies of the files of ``code/`` that only the linear certificates ship.
LINEAR_CODE = LINEAR_PACKET / "square-packing-bounds/certificates/mixed_n101_L1028/code"
STEP = mixed.N50_STEP
LAST = mixed.N50_LAST
#: Every module of ``code/`` a replay may import, dropped before the bundle's are loaded.
SHIPPED = (
    "score",
    "mixed_density_check",
    "mixed_net_audit",
    "mixed_rotated_verify",
    "unified_measure",
    "unified_linear_verify",
    "unified_linear_full_verify",
    "radial_measure",
    "trimmed_core",
    "endpoint_cells",
)
#: How many coordinates each primitive kind has.
SIZES = {"point": 2, "segment": 4, "rectangle": 4}
KINDS = ("rectangle", "point", "segment")


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass(frozen=True, slots=True)
class LinearCertificate(mixed.MixedCertificate):
    """One linear ``certificates/mixed_n*`` directory, as the source states it.

    ``rectangles`` counts rectangle orbits, as ``points`` and ``segments`` count theirs;
    the rest is the mixed certificate's pin, so the tarball fetch, the range driver and
    the merge are the mixed ones.
    """

    points: int
    segments: int


#: Each row is the packet, the pinned revision, n, the side as the directory names it, the
#: side, and the point, segment and rectangle orbit counts and candidate digest the source
#: states.
_LINEAR_ROWS: tuple[tuple[Path, str, int, str, Fraction, int, int, int, str], ...] = (
    (
        LINEAR_PACKET,
        LINEAR_REVISION,
        101,
        "10.28",
        Fraction(257, 25),
        333,
        897,
        4,
        "933aa46895a8cdfda1e3d0017b394a4de5d585d507a65472b2c4fe0165d0f79b",
    ),
    (
        LINEAR_PACKET,
        LINEAR_REVISION,
        83,
        "9.35",
        Fraction(187, 20),
        86,
        222,
        774,
        "159f4c9ec8342d70d3bbf509c21edd95e9d344f3d25b8f2250e8d558cc76d0b5",
    ),
    (
        N82_PACKET,
        N82_REVISION,
        82,
        "9.32",
        Fraction(233, 25),
        86,
        222,
        774,
        "5ddb7ed328ca3250e8d0ffaab577a68acd8a2debfa600a43500e05e5ee019606",
    ),
)
LINEAR: dict[str, LinearCertificate] = {
    f"n{n}": LinearCertificate(
        name=f"n{n}",
        packet=packet,
        revision=revision,
        directory=Path(f"certificates/mixed_n{n}_L{label.replace('.', '')}"),
        n=n,
        side=side,
        rectangles=rectangles,
        candidate_digest=digest,
        tarball=f"n{n}-L{label}-proof-bundle.tar.gz",
        source_audit=True,
        points=points,
        segments=segments,
    )
    for packet, revision, n, label, side, points, segments, rectangles, digest in _LINEAR_ROWS
}


# --------------------------------------------------------------------------- the measure

Geometry = tuple[Fraction, ...]
Image = tuple[str, Geometry, Fraction]


@dataclass(frozen=True, slots=True)
class LinearMeasure:
    """A linear candidate read here: orbit representatives and their D4 images.

    ``images`` holds, per kind, every image in the source's export order with its own
    weight, one eighth of its orbit's mass; a rectangle's weight is its mass, not its
    density.
    """

    n: int
    side: Fraction
    core: Fraction
    primitives: list[Image]
    images: dict[str, list[tuple[Geometry, Fraction]]]
    total: Fraction


def _orbit(kind: str, geometry: Geometry, side: Fraction) -> list[Geometry]:
    """The eight D4 images of one primitive, in the source's order (swap, then signs)."""
    corners = [geometry] if kind == "point" else [geometry[:2], geometry[2:]]
    images: list[Geometry] = []
    for swap in (False, True):
        for flip_x, flip_y in ((False, False), (False, True), (True, False), (True, True)):
            moved = []
            for x, y in corners:
                u, v = (y, x) if swap else (x, y)
                moved.append((side - u if flip_x else u, side - v if flip_y else v))
            if kind == "point":
                images.append(moved[0])
            elif kind == "rectangle":
                (a, b), (c, d) = moved
                images.append((min(a, c), min(b, d), max(a, c), max(b, d)))
            else:
                images.append((*moved[0], *moved[1]))
    return images


def linear_measure(data: Mapping[str, Any]) -> LinearMeasure:
    """Read a linear candidate exactly, refusing anything the source's schema refuses."""
    _require(data.get("schema") == LINEAR_SCHEMA, "not a point_line_rectangle_v1 measure")
    n = data["n"]
    side, core = Fraction(data["L"]), Fraction(data["B"])
    _require(
        isinstance(n, int) and not isinstance(n, bool) and n >= 1 and 0 < core < 1 < side,
        "invalid count, side or core",
    )
    primitives: list[Image] = []
    images: dict[str, list[tuple[Geometry, Fraction]]] = {kind: [] for kind in KINDS}
    for item in data["primitives"]:
        _require(set(item) == {"kind", "geometry", "mass"}, "a primitive has other fields")
        kind = item["kind"]
        _require(kind in SIZES, f"unknown primitive kind: {kind}")
        geometry = tuple(Fraction(value) for value in item["geometry"])
        mass = Fraction(item["mass"])
        _require(len(geometry) == SIZES[kind], f"a {kind} with {len(geometry)} coordinates")
        _require(mass >= 0, "negative mass")
        _require(all(0 <= value <= side for value in geometry), "a primitive outside the box")
        if kind == "rectangle":
            _require(geometry[0] < geometry[2] and geometry[1] < geometry[3], "empty rectangle")
        if kind == "segment":
            _require(geometry[:2] != geometry[2:], "a segment of length zero")
        primitives.append((kind, geometry, mass))
        if mass:
            images[kind].extend((image, mass / 8) for image in _orbit(kind, geometry, side))
    total = sum((mass for _, _, mass in primitives), Fraction())
    return LinearMeasure(n, side, core, primitives, images, total)


def _normal(kind: str, geometry: Geometry) -> Geometry:
    """One spelling per set: a segment's endpoints in order, anything else as it is."""
    if kind == "segment" and geometry[2:] < geometry[:2]:
        return (*geometry[2:], *geometry[:2])
    return geometry


def d4_invariant(
    images: Mapping[str, Iterable[tuple[Geometry, Fraction]]], side: Fraction
) -> bool:
    """Whether the weighted images are carried onto themselves by both D4 generators.

    The generators are the diagonal reflection and the reflection ``x -> L - x``; the
    measure is compared as a multiset of (kind, set, weight).
    """
    found: Counter[tuple[str, Geometry, Fraction]] = Counter()
    for kind, rows in images.items():
        for geometry, weight in rows:
            found[(kind, _normal(kind, geometry), weight)] += 1

    def moved(kind: str, geometry: Geometry, *, swap: bool) -> Geometry:
        corners = [geometry] if kind == "point" else [geometry[:2], geometry[2:]]
        mapped = [(y, x) if swap else (side - x, y) for x, y in corners]
        if kind == "point":
            return mapped[0]
        if kind == "rectangle":
            (a, b), (c, d) = mapped
            return (min(a, c), min(b, d), max(a, c), max(b, d))
        return _normal(kind, (*mapped[0], *mapped[1]))

    for swap in (False, True):
        image: Counter[tuple[str, Geometry, Fraction]] = Counter()
        for (kind, geometry, weight), count in found.items():
            image[(kind, moved(kind, geometry, swap=swap), weight)] += count
        if image != found:
            return False
    return True


def semantic_digest(data: Mapping[str, Any]) -> str:
    """The candidate digest by the source's rule: its seven semantic fields, canonical JSON."""
    fields = ("schema", "n", "L", "B", "primitives", "total_mass", "net")
    semantic = {key: data[key] for key in fields}
    return _sha256(json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode())


def centre_half_widths(side: Fraction, core: Fraction) -> list[Fraction]:
    """``E = (L - B(c + s))/2`` at each net angle: the centre domain is ``L/2 +- E``."""
    widths = []
    for index in range(LAST + 1):
        c, s = net_rotation(index * STEP)
        widths.append((side - core * (c + s)) / 2)
    return widths


# --------------------------------------------------------------------------- the audit


def linear_retained(certificate: LinearCertificate) -> dict[str, bytes]:
    """The retained small files of one certificate directory, decompressed."""
    return {
        name: read_retained_bytes(certificate.source / certificate.directory / name)
        for name in mixed.MIXED_FILES
    }


def code_sources(certificate: LinearCertificate, tree: Mapping[Path, str]) -> dict[str, Path]:
    """Where this repository retains each file of the directory's ``code/``.

    The seven linear files are retained in this packet under n = 101; the other six are
    the 2026-09-28 packet's ``mixed_n50_L740/code/``. Each must have the pinned digest.
    """
    listed = {
        path.name: digest
        for path, digest in tree.items()
        if path.parent == certificate.directory / "code"
    }
    found: dict[str, Path] = {}
    for name, digest in sorted(listed.items()):
        copies = [folder / name for folder in (LINEAR_CODE, mixed.MIXED_CODE)]
        held = [path for path in copies if path.is_file()]
        _require(len(held) == 1, f"code/{name} is retained {len(held)} times, not once")
        _require(_sha256(held[0].read_bytes()) == digest, f"code/{name} is not the pinned file")
        found[name] = held[0]
    _require(
        listed.get("unified_linear_verify.cpp") == LINEAR_CHECKER_SHA256,
        "code/unified_linear_verify.cpp is not the named checker",
    )
    return found


def _records(certificate: dict[str, Any]) -> dict[str, Any]:
    """The 201 replay records a certificate carries, each in the shipped record's shape."""
    results = certificate["results"]
    _require(
        set(results) == {str(index) for index in range(LAST + 1)},
        "the certificate does not carry exactly the 201 net angles",
    )
    nodes = []
    for index in range(LAST + 1):
        record = results[str(index)]
        _require(
            list(record) == ["index", "status", "input_sha256", "nodes"]
            and record["index"] == index
            and record["status"] == LINEAR_REPLAYED
            and isinstance(record["input_sha256"], str)
            and len(record["input_sha256"]) == 64
            and isinstance(record["nodes"], int)
            and record["nodes"] > 0,
            f"angle {index} is not a replayed record",
        )
        nodes.append(record["nodes"])
    return {
        "nodes": sum(nodes),
        "most_nodes": max(nodes),
        "most_nodes_at": nodes.index(max(nodes)),
        "axis_nodes": nodes[0],
    }


def _counts(measure: LinearMeasure) -> dict[str, int]:
    return {kind: sum(1 for k, _, _ in measure.primitives if k == kind) for kind in KINDS}


def linear_certificate(
    certificate: LinearCertificate,
    files: Mapping[str, bytes] | None = None,
    tree: Mapping[Path, str] | None = None,
) -> dict[str, Any]:
    """Exact premises of one linear certificate from its retained files; coverage is not.

    Every retained file must have its pinned digest. The candidate must be the stated
    count, side and core ``9977/10000`` with the stated orbit counts, every primitive
    inside the container, nondegenerate and of nonnegative mass, and total exactly
    ``n - 1/100000``; its D4 images must be invariant under both generators; its digest,
    recomputed by the source's rule, must be the one the statement, the manifest, the
    certificate and the source's audit name. The net must be the 201-node net whose
    containment is recomputed here, with a positive centre domain at every angle; the
    checker must be ``0249726a...`` and ``code/`` the retained copies. The certificate
    must carry a replay record for every angle, and the source's audit must bind the
    certificate's and the tarball's digests.
    """
    tree = tree if tree is not None else mixed.read_subtree_manifest(certificate.subtree)
    files = files if files is not None else linear_retained(certificate)
    directory = certificate.directory
    for name in mixed.MIXED_FILES:
        _require(
            _sha256(files[name]) == tree[directory / name], f"{name} is not the pinned file"
        )
    data = json.loads(files["candidate.json"])
    manifest = json.loads(files["manifest.json"])
    replay = json.loads(files["certificate.json"])
    audit = json.loads(files["completion-audit.json"])
    measure = linear_measure(data)
    n, side, core, total = certificate.n, measure.side, measure.core, measure.total
    _require(
        measure.n == n and side == certificate.side and core == mixed.MIXED_CORE,
        "count, side or core differs from the statement",
    )
    counts = _counts(measure)
    stated = {
        "rectangle": certificate.rectangles,
        "point": certificate.points,
        "segment": certificate.segments,
    }
    _require(counts == stated, f"orbit counts {counts} differ from the statement {stated}")
    _require(total == Fraction(data["total_mass"]) == n - mixed.MIXED_GAP, "total mass differs")
    _require(d4_invariant(measure.images, side), "the D4 images are not invariant")
    digest = semantic_digest(data)
    _require(
        digest
        == certificate.candidate_digest
        == manifest["candidate_digest"]
        == replay["candidate_digest"]
        == audit["candidate_digest"],
        "recomputed candidate digest differs",
    )
    _require(
        data["net"] == {"step": str(STEP), "last": LAST}, "the candidate names another net"
    )
    end = STEP * LAST
    _require(
        end <= Fraction(1, 2) and (1 + end) ** 2 >= 2 and core * (1 + STEP) < 1,
        "the net does not strictly inscribe every angle",
    )
    _require(manifest["net"] == replay["net"], "the manifest and certificate nets differ")
    net = mixed.net_facts(manifest["net"], core)
    widths = centre_half_widths(side, core)
    narrowest = min(range(LAST + 1), key=lambda index: widths[index])
    _require(widths[narrowest] > 0, "a net angle has an empty centre domain")
    _require(
        manifest["n"] == n
        and Fraction(manifest["L"]) == side
        and Fraction(manifest["B"]) == core
        and Fraction(manifest["mass"]) == total
        and manifest["angle_count"] == LAST + 1
        and manifest["source_sha256"] == LINEAR_CHECKER_SHA256,
        "the manifest states another measure or checker",
    )
    code = code_sources(certificate, tree)
    _require(
        replay["status"] == LINEAR_STATUS
        and replay["n"] == n
        and Fraction(replay["L"]) == side
        and Fraction(replay["B"]) == core
        and Fraction(replay["total_mass"]) == total
        and Fraction(replay["budget_gap"]) == n - total
        and replay["angle_count"] == LAST + 1
        and replay["source_sha256"] == LINEAR_CHECKER_SHA256,
        "the certificate states another run",
    )
    records = _records(replay)
    archive = tree[certificate.upstream_tarball]
    _require(
        audit["status"] == "AUDITED_AND_PACKAGED"
        and audit["n"] == n
        and Fraction(audit["L"]) == side
        and Fraction(audit["total_mass"]) == total
        and audit["all_angles"] == LAST + 1
        and audit["bundle"] in (certificate.bundle, certificate.tarball)
        and audit["verifier_source_sha256"] == LINEAR_CHECKER_SHA256,
        "the source's audit states another measure",
    )
    _require(
        audit["certificate_sha256"] == _sha256(files["certificate.json"]),
        "the source's audit binds another certificate",
    )
    _require(audit["archive_sha256"] == archive, "the source's audit binds another tarball")
    _require(archive in files["README.md"].decode(), "the README states another tarball")
    # The n = 82 audit compares with the upper end of its own enclosure of Green's value.
    field = "green_upper" if "green_upper" in audit else "compared_with"
    compared = Fraction(audit[field])
    _require(
        field == "compared_with" or Fraction(audit["green_interval"][1]) == compared,
        "the source's Green upper bound is not its interval's upper end",
    )
    improvement = Fraction(audit["improvement_lower"])
    _require(improvement == side - compared > 0, "the source's improvement is not L - value")
    return {
        "directory": directory.as_posix(),
        "side": str(side),
        "side_float": float(side),
        "core": str(core),
        "orbits": counts,
        "images": {kind: len(rows) for kind, rows in measure.images.items()},
        "d4_invariant": True,
        "total_mass": str(total),
        "budget_gap": str(n - total),
        "candidate_digest": digest,
        "checker_sha256": LINEAR_CHECKER_SHA256,
        "code_files": len(code),
        "code_retained_in": sorted(
            {path.parent.relative_to(mixed.REPO).as_posix() for path in code.values()}
        ),
        "net": net,
        "centre_half_width_least": str(widths[narrowest]),
        "centre_half_width_least_at": narrowest,
        "certificate_status": replay["status"],
        **records,
        "tarball": certificate.upstream_tarball.as_posix(),
        "tarball_sha256": archive,
        "source_audit": {
            "status": audit["status"],
            "certificate_sha256_matches": True,
            "archive_sha256_matches": True,
            **({} if field == "compared_with" else {"compared_field": field}),
            "compared_with": str(compared),
            "compared_note": audit.get("compared_note"),
            "improvement_lower": str(improvement),
        },
        "comparison": mixed.green_facts(n, side, compared),
        "coverage_decided_here": False,
    }


def linear_audit(packet: Path = LINEAR_PACKET) -> dict[str, Any]:
    """`linear_certificate` for every linear certificate a packet retains."""
    chosen = [c for c in LINEAR.values() if c.packet == packet]
    _require(bool(chosen), f"no linear certificate is registered for {packet.name}")
    revision = json.loads(chosen[0].record.read_text())["sources"][0]["source_commit"]
    _require(all(c.revision == revision for c in chosen), "the packet pins another revision")
    return {
        "kind": "wand125-linear-certificate-audit/v1",
        "packet": packet.name,
        "source_revision": revision,
        "certificates": {c.name: linear_certificate(c) for c in chosen},
        "scope": (
            "Exact premises only, from the retained files: pinned digests, the measure's "
            "count, side, core, orbit counts, containment, nonnegativity and total "
            "n - 1/100000, its D4 invariance, the candidate digest by the source's rule, "
            "the net containment and centre domains, the checker and code identity, a "
            "replay record for each of the 201 angles, and the source audit's certificate "
            "and tarball digests. Coverage is decided by the source's checker, whose "
            "replay is recorded separately."
        ),
    }


# --------------------------------------------------------------------------- the bundle


def bundle_bindings(
    certificate: LinearCertificate, bundle: Path, tree: Mapping[Path, str] | None = None
) -> dict[str, Any]:
    """An unpacked linear bundle against the packet, before any of its code is run.

    The bundle has no file list of its own, so its whole shape is checked: exactly the
    top-level candidate, certificate, manifest, summary, progress record and
    ``verify.cpp``, and four files in each of the 201 angle folders. Its candidate,
    certificate and manifest must be the retained files; every ``verify.cpp`` the pinned
    checker; every angle's ``candidate.json`` the top-level one; and its summary must
    record all 201 angles verified on the stated candidate.
    """
    tree = tree if tree is not None else mixed.read_subtree_manifest(certificate.subtree)
    top = {
        "candidate.json",
        "certificate.json",
        "manifest.json",
        "replay-progress.json",
        "summary.json",
        "verify.cpp",
    }
    leaves = ("candidate.json", "input.txt", "result.json", "verify.cpp")
    expected = top | {f"net{i:03}/{leaf}" for i in range(LAST + 1) for leaf in leaves}
    present = {
        path.relative_to(bundle).as_posix() for path in bundle.rglob("*") if path.is_file()
    }
    _require(
        present == expected, f"the bundle's files differ: {sorted(present ^ expected)[:5]}"
    )
    for name in ("candidate.json", "certificate.json", "manifest.json"):
        _require(
            _sha256((bundle / name).read_bytes()) == tree[certificate.directory / name],
            f"the bundle's {name} is not the retained file",
        )
    checker = tree[certificate.directory / "code/unified_linear_verify.cpp"]
    candidate = (bundle / "candidate.json").read_bytes()
    for index in range(LAST + 1):
        folder = bundle / f"net{index:03}"
        _require(
            (folder / "candidate.json").read_bytes() == candidate,
            f"angle {index} carries another candidate",
        )
    copies = [bundle / "verify.cpp", *(bundle.glob("net*/verify.cpp"))]
    _require(
        all(_sha256(path.read_bytes()) == checker == LINEAR_CHECKER_SHA256 for path in copies),
        "a verify.cpp in the bundle is not the pinned checker",
    )
    summary = json.loads((bundle / "summary.json").read_text())
    records = summary["records"]
    _require(
        summary["status"] == LINEAR_STATUS
        and summary["globally_verified"] is True
        and summary["candidate_digest"] == certificate.candidate_digest
        and summary["complete_angles"] == summary["verified_angles"] == LAST + 1
        and set(records) == {str(index) for index in range(LAST + 1)}
        and all(record["status"] == "ANGLE_VERIFIED" for record in records.values()),
        "the bundle's summary does not record every angle verified",
    )
    progress = json.loads((bundle / "replay-progress.json").read_text())
    _require(progress == {"done": LAST + 1, "total": LAST + 1}, "the replay progress differs")
    return {
        "status": "BUNDLE_BOUND_TO_PACKET",
        "files": len(present),
        "checker_copies": len(copies),
        "upstream_seconds": round(sum(record["seconds"] for record in records.values()), 1),
    }


def assemble_code(certificate: LinearCertificate, into: Path, tree: Mapping[Path, str]) -> Path:
    """The shipped ``code/`` rebuilt afresh from the retained copies, each at its pin."""
    if into.exists():
        shutil.rmtree(into)
    into.mkdir(parents=True)
    for name, path in code_sources(certificate, tree).items():
        shutil.copyfile(path, into / name)
    return into


@dataclass(frozen=True, slots=True)
class Preconditions:
    """What ``replay_linear_bundle.main`` establishes before it replays any angle."""

    root: Path
    code: str
    digest: str
    count: int
    mass: Fraction
    verifier: Any

    def facts(self) -> dict[str, Any]:
        return {
            "status": "DRIVER_PRECONDITIONS_HOLD",
            "candidate_digest": self.digest,
            "angles": self.count,
            "total_mass": str(self.mass),
            "checker_sha256": _sha256(Path(self.verifier.SOURCE).read_bytes()),
        }


def driver_preconditions(bundle: Path, code: Path) -> Preconditions:
    """Repeat ``replay_linear_bundle.main``'s assertions, in its order, on its own code.

    The driver has no range mode, so a split replay calls its per-angle function after
    this: the candidate's validation and net, the certificate's status, digest, mass,
    net and angle count against the manifest, and the checker source's digest.
    """
    root, folder = bundle.resolve(), str(code.resolve())
    for name in SHIPPED:
        sys.modules.pop(name, None)
    if folder in sys.path:
        sys.path.remove(folder)
    sys.path.insert(0, folder)
    measure = importlib.import_module("unified_measure")
    verifier = importlib.import_module("unified_linear_verify")
    net_audit = importlib.import_module("mixed_net_audit")
    _require(
        Path(verifier.SOURCE).resolve().parent == Path(folder),
        "the imported checker is not the assembled code's",
    )
    certificate = json.loads((root / "certificate.json").read_text())
    manifest = json.loads((root / "manifest.json").read_text())
    data = json.loads((root / "candidate.json").read_text())
    _, core, n, _, mass, digest = measure.validate(data)
    step, last = measure.net_check(data)
    count = last + 1
    _require(
        certificate["status"] == LINEAR_STATUS
        and certificate["candidate_digest"] == digest == manifest["candidate_digest"],
        "the certificate's status or digest",
    )
    _require(
        0 < mass < n
        and str(mass) == certificate["total_mass"]
        and certificate["net"] == manifest["net"] == net_audit.net_certificate(core, step, last)
        and certificate["angle_count"] == count,
        "the certificate's mass, net or angle count",
    )
    source = _sha256(Path(verifier.SOURCE).read_bytes())
    _require(
        source == manifest["source_sha256"] == certificate["source_sha256"],
        "verifier source differs from the certificate",
    )
    return Preconditions(root, folder, digest, count, mass, verifier)


def _interval(text: str) -> tuple[Fraction, Fraction]:
    low, high = (Fraction(float.fromhex(token)) for token in text.split())
    return low, high


def _encloses(tokens: list[str], values: Iterable[Fraction]) -> bool:
    exact = list(values)
    if len(tokens) != 2 * len(exact):
        return False
    pairs = (_interval(f"{tokens[2 * k]} {tokens[2 * k + 1]}") for k in range(len(exact)))
    return all(low <= value <= high for (low, high), value in zip(pairs, exact, strict=True))


def check_inputs(
    root: Path, candidate_sha256: str, indices: Iterable[int], shipped: Mapping[str, Any]
) -> dict[str, Any]:
    """Bind each angle's input to the exact candidate, independently of the source's code.

    The input must hash to the digest its ``result.json`` and the certificate's record
    name; its header must enclose ``L``, ``B``, ``E``, ``c``, ``s`` and exactly ``1``; and
    its rectangle, point and segment lines must enclose, in the source's order, every D4
    image recomputed here (a rectangle's density, a point's and a segment's weight). The
    stored result must be the verified one the shipped replay requires.
    """
    candidate = (root / "candidate.json").read_bytes()
    _require(_sha256(candidate) == candidate_sha256, "the bundle's candidate differs")
    data = json.loads(candidate)
    measure = linear_measure(data)
    digest = semantic_digest(data)
    rows: dict[str, list[tuple[Fraction, ...]]] = {
        "rectangle": [
            (*g, w / ((g[2] - g[0]) * (g[3] - g[1]))) for g, w in measure.images["rectangle"]
        ],
        "point": [(*g, w) for g, w in measure.images["point"]],
        "segment": [(*g, w) for g, w in measure.images["segment"]],
    }
    checked = 0
    for index in indices:
        _require(0 <= index <= LAST, f"not a net index: {index}")
        folder = root / f"net{index:03}"
        raw = (folder / "input.txt").read_bytes()
        result = json.loads((folder / "result.json").read_text())
        spec = result["manifest"]
        _require(
            _sha256(raw) == spec["input_sha256"] == shipped[str(index)]["input_sha256"],
            f"input {index} is not the recorded one",
        )
        _require(
            result["status"] == "ANGLE_VERIFIED"
            and result["frontier"] == []
            and not result["exact_witnesses"]
            and result["nodes"] == shipped[str(index)]["nodes"],
            f"angle {index}'s stored result is not the verified one",
        )
        t = index * STEP
        c, s = net_rotation(t)
        width = (measure.side - measure.core * (c + s)) / 2
        _require(
            spec["index"] == index
            and Fraction(spec["t"]) == t
            and Fraction(spec["E"]) == width
            and Fraction(spec["L"]) == measure.side
            and Fraction(spec["B"]) == measure.core
            and spec["gamma"] == "1"
            and Fraction(spec["mass"]) == measure.total
            and spec["candidate_digest"] == digest
            and spec["source_sha256"] == LINEAR_CHECKER_SHA256,
            f"angle {index}'s specification differs",
        )
        lines = raw.decode("ascii").splitlines()
        header = (measure.side, measure.core, width, c, s, Fraction(1))
        for line, exact in zip(lines[:6], header, strict=True):
            _require(_encloses(line.split(), [exact]), f"input {index} header differs")
        _require(_interval(lines[5]) == (1, 1), f"input {index}: gamma is not exactly one")
        at = 6
        for kind in KINDS:
            _require(int(lines[at]) == len(rows[kind]), f"input {index}: {kind} count")
            for line, exact in zip(
                lines[at + 1 : at + 1 + len(rows[kind])], rows[kind], strict=True
            ):
                _require(_encloses(line.split(), exact), f"input {index}: a {kind} differs")
            at += 1 + len(rows[kind])
        _require(at == len(lines), f"input {index} has extra lines")
        checked += 1
    return {
        "status": "ALL_INPUTS_ENCLOSE_THE_CANDIDATE",
        "inputs": checked,
        "images": {kind: len(rows[kind]) for kind in KINDS},
        "gamma": "1",
        "scope": (
            "Each input hashes to its recorded digest and every interval encloses the exact "
            "datum recomputed from the candidate; coverage is not decided here."
        ),
    }


@dataclass(frozen=True, slots=True)
class Prepared:
    """A bundle fetched, bound and checked up to its first angle."""

    tarball: dict[str, Any]
    bindings: dict[str, Any]
    driver: Preconditions
    bundle: Path


def prepare(
    certificate: LinearCertificate, work: Path, supplied: Path | None, via: str
) -> Prepared:
    """The tarball at its pin, unpacked afresh, bound, with code and preconditions."""
    tree = mixed.read_subtree_manifest(certificate.subtree)
    tarball = mixed.fetch_tarball(certificate, work, supplied, via)
    bundle = mixed.unpack_bundle(certificate, work / certificate.tarball, work / "unpacked")
    bindings = bundle_bindings(certificate, bundle, tree)
    code = assemble_code(certificate, work / "code", tree)
    driver = driver_preconditions(bundle, code)
    _require(driver.digest == certificate.candidate_digest, "the bundle's candidate differs")
    return Prepared(tarball, bindings, driver, bundle)


def linear_fetch(
    certificate: LinearCertificate, work: Path, supplied: Path | None = None, via: str = "auto"
) -> dict[str, Any]:
    """Every check a replay makes before its first angle, over all 201, and nothing run."""
    runtime = mixed.replay_runtime()
    prepared = prepare(certificate, work, supplied, via)
    tree = mixed.read_subtree_manifest(certificate.subtree)
    shipped = mixed.shipped_results(certificate)
    inputs = check_inputs(
        prepared.driver.root,
        tree[certificate.directory / "candidate.json"],
        range(LAST + 1),
        shipped,
    )
    return {
        "status": "BUNDLE_READY",
        "certificate": certificate.name,
        "environment": runtime,
        "tarball": prepared.tarball,
        "bindings": prepared.bindings,
        "preconditions": prepared.driver.facts(),
        "inputs": inputs,
        "bundle": str(prepared.bundle),
    }


# --------------------------------------------------------------------------- the replay


def _replay_direction(job: tuple[str, str, int, str]) -> dict[str, Any]:
    """Replay one net angle with the shipped ``replay_angle``, unchanged (worker).

    The shipped function writes no file, so the row's ``replayed_sha256`` is the digest of
    the record it returned, serialized as the mixed rows' ``replayed.json`` is; a row
    passes only when that record is the certificate's own. A refusal by the shipped checks
    is returned as ``FAILED`` with its message, never swallowed.
    """
    code, root, index, binary = job
    sys.dont_write_bytecode = True
    if code not in sys.path:
        sys.path.insert(0, code)
    folder = Path(root) / f"net{index:03}"
    candidate = Path(root) / "candidate.json"
    started = _utc()
    clock = time.monotonic()
    own = resource.getrusage(resource.RUSAGE_SELF)
    children = resource.getrusage(resource.RUSAGE_CHILDREN)
    report: dict[str, Any] | None = None
    error: str | None = None
    try:
        module = importlib.import_module("unified_linear_full_verify")
        report = module.replay_angle((str(candidate), str(folder), binary))
    except (AssertionError, KeyError, ValueError, OSError, subprocess.CalledProcessError) as e:
        error = f"{type(e).__name__}: {e}"
    own_after = resource.getrusage(resource.RUSAGE_SELF)
    children_after = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu = sum(
        after - before
        for after, before in (
            (own_after.ru_utime, own.ru_utime),
            (own_after.ru_stime, own.ru_stime),
            (children_after.ru_utime, children.ru_utime),
            (children_after.ru_stime, children.ru_stime),
        )
    )
    return {
        "index": index,
        "status": "FAILED" if report is None else "REPLAYED",
        "report": report,
        "error": error,
        "replayed_sha256": None
        if report is None
        else _sha256(json.dumps(report, indent=2).encode()),
        "started": started,
        "finished": _utc(),
        "wall_seconds": round(time.monotonic() - clock, 3),
        "cpu_seconds": round(cpu, 3),
        "load": os.getloadavg(),
    }


def linear_replay(
    certificate: LinearCertificate,
    work: Path,
    first: int,
    last: int,
    *,
    workers: int,
    receipts: Path,
    supplied: Path | None = None,
    via: str = "auto",
    stop_after_hours: float | None = None,
) -> dict[str, Any]:
    """Replay the net angles ``first..last`` of one certificate and write their receipts.

    The steps are the source's complete replay restricted to a range: the tarball at its
    pin, unpacked afresh and bound to the packet, the shipped code assembled from the
    retained copies, the driver's preconditions, each input of the range bound to the
    candidate independently, the checker compiled by the shipped ``compile_verifier``, and
    then each angle replayed by the shipped ``replay_angle`` through the mixed range
    driver, which appends and syncs each receipt as the angle finishes. Run again, it
    replays only the angles with no passing row.
    """
    runtime = mixed.replay_runtime()
    _require(0 <= first <= last <= LAST, f"range outside 0..{LAST}: {first}-{last}")
    _require(
        1 <= workers <= mixed.MAX_REPLAY_WORKERS,
        f"workers must be 1 to {mixed.MAX_REPLAY_WORKERS}",
    )
    clock = time.monotonic()
    folder = receipts / mixed.range_name(first, last)
    folder.mkdir(parents=True, exist_ok=True)
    torn = sum(
        mixed.drop_torn_line(folder / name) for name in ("runs.jsonl", "directions.jsonl")
    )
    shipped = mixed.shipped_results(certificate)
    todo = mixed.pending_directions(folder, shipped, first, last)
    if not todo:
        summary = mixed.range_summary(certificate, folder, first, last, shipped)
        atomic_write_text(folder / "summary.json", json.dumps(summary, indent=2) + "\n")
        return summary
    tree = mixed.read_subtree_manifest(certificate.subtree)
    prepared = prepare(certificate, work, supplied, via)
    driver = prepared.driver
    inputs = check_inputs(
        driver.root, tree[certificate.directory / "candidate.json"], todo, shipped
    )
    binary = work / "replay-verify"
    driver.verifier.compile_verifier(binary)
    run = {
        "run": f"{_utc()}-{os.getpid()}",
        "certificate": certificate.name,
        "range": [first, last],
        "todo": len(todo),
        "torn_bytes_dropped": torn,
        "argv": sys.argv,
        "load": os.getloadavg(),
        "environment": runtime,
        "host": mixed.host_facts(),
        "tarball": prepared.tarball,
        "bindings": prepared.bindings,
        "preconditions": driver.facts(),
        "inputs": {key: inputs[key] for key in ("status", "inputs", "images")},
        "binary_sha256": _sha256(binary.read_bytes()),
        "compile": "the shipped compile_verifier: c++ -O2 -std=c++17 -ffp-contract=off "
        "-fno-fast-math",
    }
    with (folder / "runs.jsonl").open("a", encoding="utf-8") as out:
        out.write(json.dumps(run, default=str) + "\n")
        out.flush()
        os.fsync(out.fileno())
    print(
        json.dumps({"run": run["run"], "range": [first, last], "todo": len(todo)}), flush=True
    )
    deadline = None if stop_after_hours is None else clock + 3600 * stop_after_hours
    with ProcessPoolExecutor(max_workers=workers) as pool:

        def submit(index: int) -> Future[dict[str, Any]]:
            job = (driver.code, str(driver.root), index, str(binary))
            return pool.submit(_replay_direction, job)

        return mixed.replay_directions(
            certificate,
            folder,
            (first, last),
            todo,
            submit,
            workers=workers,
            run=run["run"],
            shipped=shipped,
            deadline=deadline,
        )


# --------------------------------------------------------------------------- price, plan

#: Single angles replayed one at a time (``linear-replay --range I-I --workers 1``) to price
#: the replays, as (certificate, net index, CPU seconds here, the source's seconds for the
#: same angle in its bundle's ``summary.json``): 2026-10-02 on a 4-core KVM guest (Intel
#: Xeon at 2.10 GHz) with its other cores busy, checker built by the shipped
#: ``compile_verifier``. The receipts are in the 2026-10-02 linear packet.
PRICE_SAMPLES: tuple[tuple[str, int, float, float], ...] = (
    ("n101", 150, 123.841, 133.350),
    ("n83", 50, 273.307, 249.558),
)

#: The source's own seconds for each complete run, summed over its bundle's 201 records.
#: n = 82's run was resumed and finished on other machines (its ``completion-audit.json``),
#: and has no sampled angle here.
UPSTREAM_SECONDS = {"n101": 31303.5, "n83": 75685.9, "n82": 118941.6}


def linear_costs(certificate: LinearCertificate) -> list[float]:
    """Each net angle's cost in checker nodes, the certificate's own counts."""
    shipped = mixed.shipped_results(certificate)
    return [float(shipped[str(index)]["nodes"]) for index in range(LAST + 1)]


def linear_price() -> dict[str, Any]:
    """Each linear replay's estimated CPU-hours, from `PRICE_SAMPLES`.

    A node's cost depends on the measure's mix of points, segments and rectangles and on
    the angle, so each certificate is priced from its own samples: the source's seconds
    for the whole run, scaled by the ratio of this host's CPU seconds to the source's on
    the sampled angles. The nodes-only estimate is given beside it.
    """
    rows: dict[str, Any] = {}
    for name, certificate in sorted(LINEAR.items(), key=lambda item: item[1].n):
        samples = [sample for sample in PRICE_SAMPLES if sample[0] == name]
        nodes = sum(linear_costs(certificate))
        row: dict[str, Any] = {
            "nodes": int(nodes),
            "upstream_cpu_hours": round(UPSTREAM_SECONDS[name] / 3600, 2),
        }
        if samples:
            shipped = mixed.shipped_results(certificate)
            ratio = sum(here for _, _, here, _ in samples) / sum(up for *_, up in samples)
            per_node = sum(here for _, _, here, _ in samples) / sum(
                shipped[str(index)]["nodes"] for _, index, _, _ in samples
            )
            hours = ratio * UPSTREAM_SECONDS[name] / 3600
            row |= {
                "samples": [
                    {"index": index, "cpu_seconds": here, "upstream_seconds": up}
                    for _, index, here, up in samples
                ],
                "host_over_upstream": round(ratio, 3),
                "cpu_hours": round(hours, 1),
                "cpu_hours_by_nodes_only": round(per_node * nodes / 3600, 1),
                "wall_hours_at_4_workers": round(hours / mixed.MAX_REPLAY_WORKERS, 1),
            }
        rows[name] = row
    return {
        "certificates": rows,
        "scope": (
            "An estimate: the source's seconds per run, scaled by this host's single-"
            "threaded seconds on the sampled angles over the source's for the same angles. "
            "On a guest with busier neighbours the mixed replays ran up to twice their "
            "estimates; budget wall time accordingly."
        ),
    }


def linear_plan(certificate: LinearCertificate, parts: int) -> dict[str, Any]:
    """Split the 201 angles into ``parts`` contiguous ranges of about equal node count."""
    costs = linear_costs(certificate)
    total = sum(costs)
    rows = []
    for first, stop in mixed.balanced_ranges(costs, parts):
        command = (
            "uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_linear "
            f"linear-replay {certificate.name} --range {first}-{stop - 1} "
            f"--work /tmp/wand125-{certificate.name} --workers 4 --via git"
        )
        rows.append(
            {
                "range": [first, stop - 1],
                "angles": stop - first,
                "node_share": round(sum(costs[first:stop]) / total, 4),
                "command": command,
            }
        )
    return {
        "certificate": certificate.name,
        "nodes": int(total),
        "parts": rows,
        "merge": (
            "uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_linear "
            f"linear-merge {certificate.name}"
        ),
    }


# --------------------------------------------------------------------------- controls

LINEAR_CONTROL_KIND = "wand125-linear-control/v1"
LINEAR_MUTATIONS = ("scale-masses", "drop-top-contributor")
LINEAR_CONTROL_TIMEOUT = 3600


def coverage_at(
    measure: LinearMeasure, centre: tuple[Fraction, Fraction], c: Fraction, s: Fraction
) -> dict[str, Fraction]:
    """The exact mass each kind puts in the closed core at ``centre``, turned by ``(c, s)``.

    A point counts when it is in the closed core; a segment by the fraction of its length
    inside; a rectangle by the area inside, by `coverage_exact`.
    """
    x, y = centre
    half = measure.core / 2

    def local(px: Fraction, py: Fraction) -> tuple[Fraction, Fraction]:
        dx, dy = px - x, py - y
        return c * dx + s * dy, -s * dx + c * dy

    points = Fraction()
    for (px, py), weight in measure.images["point"]:
        u, v = local(px, py)
        if abs(u) <= half and abs(v) <= half:
            points += weight
    segments = Fraction()
    for (x0, y0, x1, y1), weight in measure.images["segment"]:
        start, stop = local(x0, y0), local(x1, y1)
        low, high = Fraction(0), Fraction(1)
        for a, b in zip(start, stop, strict=True):
            slope = b - a
            if not slope:
                if abs(a) > half:
                    low, high = Fraction(1), Fraction(0)
                continue
            p, q = (-half - a) / slope, (half - a) / slope
            low, high = max(low, min(p, q)), min(high, max(p, q))
        segments += weight * max(Fraction(0), high - low)
    rects = [
        (x0, y0, x1, y1, w / ((x1 - x0) * (y1 - y0)))
        for (x0, y0, x1, y1), w in measure.images["rectangle"]
    ]
    rectangles = coverage_exact(rects, centre, c, s, measure.core)
    return {"point": points, "segment": segments, "rectangle": rectangles}


def _float_coverage(
    images: list[tuple[str, tuple[float, ...], float]],
    centre: tuple[float, float],
    rotation: tuple[float, float],
    core: float,
) -> float:
    """`coverage_at` in binary64, with a bounding-box filter: for a search, never a claim."""
    x, y = centre
    c, s = rotation
    half = core / 2
    reach = half * (abs(c) + abs(s))
    total = 0.0
    for kind, g, weight in images:
        if kind == "point":
            if abs(g[0] - x) > reach or abs(g[1] - y) > reach:
                continue
            dx, dy = g[0] - x, g[1] - y
            if abs(c * dx + s * dy) <= half and abs(-s * dx + c * dy) <= half:
                total += weight
            continue
        if min(g[0], g[2]) > x + reach or max(g[0], g[2]) < x - reach:
            continue
        if min(g[1], g[3]) > y + reach or max(g[1], g[3]) < y - reach:
            continue
        if kind == "segment":
            a = (c * (g[0] - x) + s * (g[1] - y), -s * (g[0] - x) + c * (g[1] - y))
            b = (c * (g[2] - x) + s * (g[3] - y), -s * (g[2] - x) + c * (g[3] - y))
            low, high = 0.0, 1.0
            for start, stop in zip(a, b, strict=True):
                slope = stop - start
                if slope == 0:
                    if abs(start) > half:
                        low, high = 1.0, 0.0
                    continue
                p, q = (-half - start) / slope, (half - start) / slope
                low, high = max(low, min(p, q)), min(high, max(p, q))
            total += weight * max(0.0, high - low)
            continue
        polygon = [
            (x + core * (c * u - s * v) / 2, y + core * (s * u + c * v) / 2)
            for u, v in ((-1, -1), (1, -1), (1, 1), (-1, 1))
        ]
        for axis, edge, sign in ((0, g[0], 1), (0, g[2], -1), (1, g[1], 1), (1, g[3], -1)):
            clipped: list[tuple[float, float]] = []
            if not polygon:
                break
            previous = polygon[-1]
            before = sign * (previous[axis] - edge)
            for current in polygon:
                depth = sign * (current[axis] - edge)
                if (depth >= 0) != (before >= 0):
                    ratio = before / (before - depth)
                    clipped.append(
                        (
                            previous[0] + ratio * (current[0] - previous[0]),
                            previous[1] + ratio * (current[1] - previous[1]),
                        )
                    )
                if depth >= 0:
                    clipped.append(current)
                previous, before = current, depth
            polygon = clipped
        pairs = zip(polygon, polygon[1:] + polygon[:1], strict=True)
        area = abs(sum(p[0] * q[1] - p[1] * q[0] for p, q in pairs)) / 2
        total += weight * area / ((g[2] - g[0]) * (g[3] - g[1]))
    return total


def least_covered(
    measure: LinearMeasure,
    rotation: tuple[Fraction, Fraction],
    domain: tuple[Fraction, Fraction],
    *,
    grid: int = 33,
    rounds: int = 12,
) -> tuple[Fraction, Fraction]:
    """A centre in ``domain`` squared where the coverage at one angle is low.

    A binary64 grid, then a pattern search around its least point, rounded to a rational
    in the domain. It is only a candidate: a control evaluates it exactly.
    """
    images = [
        (kind, tuple(float(v) for v in g), float(w))
        for kind in KINDS
        for g, w in measure.images[kind]
    ]
    floats = (float(rotation[0]), float(rotation[1]))
    core = float(measure.core)
    low, high = float(domain[0]), float(domain[1])

    def value(point: tuple[float, float]) -> float:
        return _float_coverage(images, point, floats, core)

    step = (high - low) / (grid - 1)
    best = min(
        ((low + i * step, low + j * step) for i in range(grid) for j in range(grid)), key=value
    )
    for _ in range(rounds):
        step /= 2
        best = min(
            (
                (
                    min(high, max(low, best[0] + i * step)),
                    min(high, max(low, best[1] + j * step)),
                )
                for i in range(-2, 3)
                for j in range(-2, 3)
            ),
            key=value,
        )
    x, y = (min(domain[1], max(domain[0], Fraction(v).limit_denominator(10**6))) for v in best)
    return x, y


def mutate_linear(data: Mapping[str, Any], kind: str, row: int) -> dict[str, Any]:
    """A copy of a linear candidate with every mass scaled, or one primitive deleted.

    The total is restated exactly, as the shipped ``validate`` requires. A primitive is one
    orbit of eight images, so deleting it keeps the D4 symmetry built into the schema.
    """
    mutated = dict(data)
    if kind == "scale-masses":
        mutated["primitives"] = [
            item | {"mass": str(Fraction(item["mass"]) * CONTROL_FACTOR)}
            for item in data["primitives"]
        ]
    elif kind == "drop-top-contributor":
        mutated["primitives"] = [
            item for index, item in enumerate(data["primitives"]) if index != row
        ]
    else:
        raise ValueError(f"unknown mutation: {kind}")
    masses = (Fraction(item["mass"]) for item in mutated["primitives"])
    mutated["total_mass"] = str(sum(masses, Fraction()))
    return mutated


def orbit_contributions(
    data: Mapping[str, Any], centre: tuple[Fraction, Fraction], c: Fraction, s: Fraction
) -> dict[int, Fraction]:
    """Each primitive's exact share of the coverage at ``centre``, for those with any."""
    found: dict[int, Fraction] = {}
    for row, item in enumerate(data["primitives"]):
        alone = dict(data) | {"primitives": [item], "total_mass": item["mass"]}
        share = sum(coverage_at(linear_measure(alone), centre, c, s).values(), Fraction())
        if share:
            found[row] = share
    return found


def linear_control(
    certificate: LinearCertificate,
    work: Path,
    supplied: Path | None = None,
    via: str = "auto",
    index: int | None = None,
) -> dict[str, Any]:
    """Run one linear certificate and two mutations on one net direction: the receipt.

    The bundle is fetched, bound and checked as for a replay. The direction defaults to the
    oblique one with the fewest recorded nodes, so that the three runs are short. A witness
    centre is found in the checker's quadrant at that angle (`least_covered`) and evaluated
    exactly; ``scale-masses`` multiplies every mass by `CONTROL_FACTOR`, and
    ``drop-top-contributor`` deletes the primitive contributing most there. Each mutation
    must leave the witness covered below 1, so it is provably invalid at that angle. Each
    variant is exported by the shipped ``export`` and run by the checker the shipped
    ``compile_verifier`` builds, with the shipped record's node count as the limit, which
    is what the shipped replay passes; the original must return the stored result, and
    both mutations must stop unresolved.
    """
    runtime = mixed.replay_runtime()
    prepared = prepare(certificate, work, supplied, via)
    driver = prepared.driver
    shipped = mixed.shipped_results(certificate)
    oblique = {i: shipped[str(i)] for i in range(1, LAST + 1)}
    chosen = min(oblique, key=lambda i: (oblique[i]["nodes"], i)) if index is None else index
    _require(chosen in oblique, "a control runs one oblique net direction")
    tree = mixed.read_subtree_manifest(certificate.subtree)
    check_inputs(driver.root, tree[certificate.directory / "candidate.json"], [chosen], shipped)
    stored = json.loads((driver.root / f"net{chosen:03}" / "result.json").read_text())
    spec = stored["manifest"]
    data = json.loads((driver.root / "candidate.json").read_text())
    measure = linear_measure(data)
    c, s = net_rotation(Fraction(spec["t"]))
    width = Fraction(spec["E"])
    domain = (measure.side / 2, measure.side / 2 + width)
    centre = least_covered(measure, (c, s), domain)
    contributions = orbit_contributions(data, centre, c, s)
    top = heaviest(contributions)
    variants = {"original": data} | {
        kind: mutate_linear(data, kind, top) for kind in LINEAR_MUTATIONS
    }
    binary = work / "control-verify"
    driver.verifier.compile_verifier(binary)
    shipped_input = (driver.root / f"net{chosen:03}" / "input.txt").read_bytes()
    runs: list[dict[str, Any]] = []
    for label, variant in variants.items():
        folder = work / "control" / label
        shutil.rmtree(folder, ignore_errors=True)
        folder.mkdir(parents=True)
        atomic_write_text(folder / "candidate.json", json.dumps(variant, indent=2) + "\n")
        manifest = driver.verifier.export(variant, chosen, folder / "input.txt")
        at_witness = sum(
            coverage_at(linear_measure(variant), centre, c, s).values(), Fraction()
        )
        item: dict[str, Any] = {
            "name": label,
            "candidate_digest": manifest["candidate_digest"],
            "input_sha256": manifest["input_sha256"],
            "total_mass": manifest["mass"],
            "primitives": len(variant["primitives"]),
            "witness_coverage_exact": str(at_witness),
            "witness_coverage": float(at_witness),
        }
        if label == "original":
            _require(
                manifest == spec and (folder / "input.txt").read_bytes() == shipped_input,
                "the original's export is not the shipped proof's",
            )
        else:
            _require(at_witness < 1, f"{label} leaves the witness covered")
        if label == "drop-top-contributor":
            item["mutation"] = {
                "row": top,
                "primitive": data["primitives"][top],
                "contribution_at_witness_exact": str(contributions[top]),
            }
        elif label == "scale-masses":
            item["mutation"] = {"factor": str(CONTROL_FACTOR)}
        run = mixed.control_direction(binary, folder, stored["nodes"], LINEAR_CONTROL_TIMEOUT)
        output = run.get("output") or {}
        if label == "original":
            matches = run.get("returncode") == 0 and run.get("frontier_boxes") == 0
            matches = matches and all(
                output.get(key) == stored[key] for key in ("status", "nodes", "leaves", "lower")
            )
            run["verdict"] = "ACCEPTED" if matches else "NOT_ACCEPTED"
        elif "verdict" not in run:
            unresolved = output.get("status") == "ANGLE_UNRESOLVED" and run["frontier_boxes"]
            run["verdict"] = "REFUSED" if unresolved else "ACCEPTED"
        runs.append(item | {"run": run})
        print(json.dumps({"name": label, "verdict": run["verdict"]}), flush=True)
    original, *mutations = runs
    passed = original["run"]["verdict"] == "ACCEPTED"
    refused = all(item["run"]["verdict"] == "REFUSED" for item in mutations)
    return {
        "kind": LINEAR_CONTROL_KIND,
        "status": "CONTROLS_REFUSED" if passed and refused else "CONTROL_FAILED",
        "certificate": certificate.name,
        "directory": certificate.directory.as_posix(),
        "revision": certificate.revision,
        "n": certificate.n,
        "side": str(certificate.side),
        "index": chosen,
        "index_choice": "the fewest recorded nodes among the oblique angles"
        if index is None
        else "given",
        "shipped_record": {key: stored[key] for key in ("status", "nodes", "leaves", "lower")},
        "checker": {
            "source_sha256": spec["source_sha256"],
            "compile": "the shipped compile_verifier: c++ -O2 -std=c++17 -ffp-contract=off "
            "-fno-fast-math",
            "binary_sha256": _sha256(binary.read_bytes()),
            "argv": ["verify", "input.txt", str(stored["nodes"])],
        },
        "witness": {
            "centre": [str(v) for v in centre],
            "t": spec["t"],
            "cos": str(c),
            "sin": str(s),
            "side": str(measure.core),
            "domain": [str(v) for v in domain],
            "coverage_exact": str(sum(contributions.values(), Fraction())),
        },
        "runs": runs,
        "tarball": prepared.tarball,
        "bindings": prepared.bindings,
        "preconditions": driver.facts(),
        "environment": runtime,
        "host": mixed.host_facts(),
        "scope": (
            "Stage-4 negative controls: the shipped export and the C++ checker its "
            "compile_verifier builds, on one net direction with the shipped replay's node "
            "limit. Each mutation leaves an exact witness centre covered below 1 at that "
            "angle, so the checker must not verify it."
        ),
    }


# --------------------------------------------------------------------------- command line


def linear_audit_supplements(
    tarballs: Iterable[Path] = (), packet: Path = LINEAR_PACKET
) -> dict[str, Any]:
    """Tarballs checked against the pin and replay receipts merged, out of the receipt."""
    chosen = {c.tarball: c for c in LINEAR.values() if c.packet == packet}
    checked: dict[str, Any] = {}
    for path in tarballs:
        certificate = chosen.get(path.name)
        if certificate is None:
            raise ValueError(f"{path.name} is not a tarball {packet.name} pins")
        checked[certificate.name] = mixed.check_tarball(certificate, path)
    replays = {c.name: mixed.replay_receipts(c) for c in chosen.values()}
    return {
        "tarballs": checked,
        "replays": {name: state for name, state in replays.items() if state is not None},
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    names = sorted(LINEAR, key=lambda name: int(name[1:]))
    auditing = commands.add_parser("linear-audit", help="exact premises of the linear certs")
    auditing.add_argument(
        "--packet",
        default=LINEAR_PACKET.name,
        choices=sorted({c.packet.name for c in LINEAR.values()}),
        help="the packet's directory name under resources/web/",
    )
    auditing.add_argument("--out", type=Path, help="default: PACKET/receipts/linear-audit.json")
    auditing.add_argument(
        "--check", action="store_true", help="compare with --out, write nothing"
    )
    auditing.add_argument("--tarball", type=Path, action="append", default=[])
    for name, text in (
        ("linear-fetch", "fetch, pin-check, unpack, bind and check every input"),
        ("linear-replay", "replay a range of net angles"),
        ("linear-control", "refuse two mutations (stage 4)"),
    ):
        command = commands.add_parser(name, help=text)
        command.add_argument("certificate", choices=names)
        command.add_argument("--work", type=Path, required=True, help="a scratch directory")
        command.add_argument(
            "--tarball", type=Path, help="use this file instead of downloading"
        )
        command.add_argument("--via", choices=mixed.TRANSPORTS, default="auto")
        if name == "linear-replay":
            command.add_argument("--range", required=True, help="A-B, inclusive")
            command.add_argument("--workers", type=int, default=3)
            command.add_argument("--receipts", type=Path, help="default: PACKET/receipts/NAME")
            command.add_argument("--stop-after-hours", type=float)
        else:
            command.add_argument("--out", type=Path, help="default: PACKET/receipts/NAME/")
        if name == "linear-control":
            command.add_argument("--index", type=int, help="default: the fewest nodes'")
    merging = commands.add_parser("linear-merge", help="merge range receipts into a verdict")
    merging.add_argument("certificate", choices=names)
    merging.add_argument("--receipts", type=Path, help="default: PACKET/receipts/NAME")
    merging.add_argument("--out", type=Path, help="default: RECEIPTS/merged.json")
    merging.add_argument(
        "--check", action="store_true", help="compare with --out, write nothing"
    )
    planning = commands.add_parser("linear-plan", help="split a replay into balanced ranges")
    planning.add_argument("certificate", choices=names)
    planning.add_argument("--parts", type=int, default=1)
    commands.add_parser("linear-price", help="estimate each replay's CPU-hours")
    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.command == "linear-audit":
        packet = mixed.WEB / args.packet
        out = args.out or packet / "receipts/linear-audit.json"
        status = mixed.write_or_check(out, linear_audit(packet), check=args.check)
        print(json.dumps(linear_audit_supplements(args.tarball, packet), indent=2))
        return status
    if args.command == "linear-price":
        print(json.dumps(linear_price(), indent=2))
        return 0
    return _run_certificate_command(args)


def _run_certificate_command(args: argparse.Namespace) -> int:
    """One command on one certificate: plan, merge, replay, control or fetch."""
    certificate = LINEAR[args.certificate]
    if args.command == "linear-plan":
        print(json.dumps(linear_plan(certificate, args.parts), indent=2))
        return 0
    if args.command == "linear-merge":
        receipts = args.receipts or certificate.receipts
        result = mixed.mixed_merge(certificate, receipts)
        status = mixed.write_or_check(
            args.out or receipts / "merged.json", result, check=args.check
        )
        return status or int(result["status"] != "FULL_REPLAY_MATCHES_SHIPPED")
    work = args.work.resolve()
    if args.command == "linear-replay":
        first, last = mixed.parse_range(args.range)
        outcome = linear_replay(
            certificate,
            work,
            first,
            last,
            workers=args.workers,
            receipts=(args.receipts or certificate.receipts).resolve(),
            supplied=args.tarball,
            via=args.via,
            stop_after_hours=args.stop_after_hours,
        )
        print(json.dumps(outcome, indent=2, default=str))
        if outcome["status"] == "INCOMPLETE":
            return mixed.RESUMABLE
        return 0 if outcome["status"] == "RANGE_REPLAYED" else 1
    if args.command == "linear-control":
        outcome = linear_control(certificate, work, args.tarball, args.via, index=args.index)
        out = args.out or certificate.receipts / "control.json"
    else:
        outcome = linear_fetch(certificate, work, args.tarball, args.via)
        out = args.out or work / "fetch.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(outcome, indent=2, default=str) + "\n"
    atomic_write_text(out, text, encoding="utf-8")
    print(text, end="")
    return 0 if outcome["status"] in mixed.PASSING else 1


if __name__ == "__main__":
    raise SystemExit(main())
