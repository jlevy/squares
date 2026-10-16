"""Audit and replay Hosono's point-only and mixed-rectangle certificates.

wand125/square-packing-bounds at ``39d8ecc`` adds three certificate families that are not
in Tokoharu's rectangle format:

- ``point_n45_L7``: a point measure proving ``s(45) = 7``, whose capture condition is
  decided by Evan Daniel's unmodified ``zmx2`` checker (``--d4 --pair-points``);
- ``point_n21_L5``: a point measure proving ``s(21) = 5`` with capture threshold
  ``249987/250000``, decided by the source's own rational replay of a 463 MB bundle; and
- ``certificates/mixed_n50_*``: rectangle-density measures proving ``s(50) >= 37/5`` (and
  the superseded ``147/20`` and ``3659/500``), decided by a research copy of Tokoharu's
  ``verify.cpp`` that accepts coverage ``>= 1``.

Later revisions add more ``certificates/mixed_n*`` directories of the same kind, with the
same code byte for byte: n = 37, 65, 66, 90 and 92 at ``1a25a5ed``, n = 84 and 85 at
``52af997``, n = 76 at ``7975030``, n = 83, 85, 87, 91, 92 and 96 at ``b00fc70``,
22 more at ``2aff207``, n = 51 to 96, five of them at counts already named, 16 more
at ``8aa6a10``, n = 42 to 95, nine of them at counts already named, 12 more at
``797bdf6``, n = 53 to 94, ten of them at counts already named, two more at
``a541afb``, n = 67 and 84, both at counts already named, and one more at ``d73ce20``,
pinned at ``43050ed``, n = 66, at a count already named. ``43050ed`` also adds
``mixed_n18_L470``, on a finer net with core 999/1000, which this tool does not audit:
its exact premises are `sqverify-fast`'s admission, and its replay is the bundle's own
driver run as its README says.
`MIXED` names each with its packet and the source's statement; a certificate at a count
an earlier one already names is ``n85-L946``, its count and side. Since ``150939e`` the
source's directories carry no ``completion-audit.json``, the source's own audit that
bound each certificate to its tarball, so a certificate pinned at or after it is bound to
its bundle by the tarball's digest at the pinned tree alone (`WITHOUT_SOURCE_AUDIT`); a
certificate pinned before it is still refused without that audit. The linear certificates
of ``af1db07``, ``0c35d90`` and ``b00fc70``, which another checker decides, are
`devtools.audit_wand125_linear`'s.

This tool is the first-party part. ``exact`` recomputes, from the 2026-09-28 packet's
retained bytes and without importing any source code, every premise that is plain
arithmetic: each measure's digest, format, nonnegativity, exact total and strict budget,
the point measures' D4 invariance, the ``s(21)`` threshold algebra and its support's link
to Daniel's certificate, the ``s(50)`` angle-net containment and the exact comparison
with Green's reported ``2√2 + 101/25 + 3√14/25``. ``mixed-audit`` does the same for every
mixed certificate a packet retains. Neither decides coverage.

The other commands work on the source's own runs. ``n45-compare``, ``n21-compare`` and
``n50-compare`` read a replay's outputs and compare them with the source's records (for
``s(21)``, output file by output file against the pinned M1 linkage, also for the
finished stages of a run in progress). ``n21-control`` is stage 4 of
``campaign/result-import.md`` for the ``s(21)`` replay: the source's ``verify_portable.py``
run on two mutated covers, each provably uncovered at an exact witness square, with the
bundle's records re-bound to the mutated cover by digest; each run must end in the
checker's own refusal. ``n50-bundle-check`` checks an unpacked bundle
against its ``files-sha256.json``; ``n50-inputs`` binds all 200 oblique inputs to the
exact candidate by an independent enclosure check; and ``n50-replay`` re-executes chosen
per-angle proofs by calling the shipped Python driver functions and C++ checker
unchanged. ``acquire`` rebuilds the 2026-09-28 packet's retained subset and digest list
from a checkout at the pinned revision, and ``host`` records the toolchain.

For any mixed certificate, ``mixed-fetch`` obtains the pinned tarball, refuses it unless
its SHA-256 and size are the pinned ones, unpacks it afresh, binds the bundle to the
packet and runs every check that precedes the first angle. ``mixed-replay`` does that and
then replays a range of the 201 net angles with the shipped functions, writing receipts
as each angle finishes, so that one certificate can be split across sessions;
``mixed-merge`` turns every range's receipts into the complete replay's verdict;
``mixed-plan`` splits the angles into ranges of equal estimated cost, and ``mixed-price``
estimates every replay's CPU-hours from timed single angles; and ``mixed-compare``
compares a complete run of the source's own driver. ``mixed-control`` is stage 4 of
``campaign/result-import.md`` for the mixed checker: one certificate and two mutations of
it, each provably uncovered at an exact witness centre, run on one net direction with the
shipped export, checker and node limit; the original must be accepted and both refused.
``mixed-audit`` also checks any tarball it is given against the pin, and any replay
receipts a certificate has.

A ``mixed-replay`` command is one batch: it downloads the tarball (from the raw-file
address, then by Git) and checks its digest before use, appends each angle's receipt as
the angle finishes, so the receipts can be committed and pushed at any moment, and, run
again after an interruption, replays only what has not passed. It exits 0 when its range
is complete, 3 when angles remain and none was refused, and 1 otherwise.

Usage, from ``packing/`` with the project interpreter::

    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed exact --check
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed acquire CHECKOUT
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed n45-compare RUN_DIR --out F
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed n21-compare OUT_DIR \\
        --m1-linkage M1 [--stage root --stage sieve | --collect RECEIPTS] --out F
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed n21-control \\
        drop-heaviest-point move-point --bundle BUNDLE --work W
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed n50-bundle-check BUNDLE --out F
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed n50-inputs BUNDLE --out F
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed n50-replay BUNDLE \\
        --index 0 --index 150 --workers 2 --out F
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed n50-compare BUNDLE --out F
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed mixed-audit PACKET [--check] \\
        [--tarball TARBALL ...]
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed mixed-fetch n84 --work W --out F
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed mixed-replay n84 \\
        --range 0-79 --work W --workers 4 [--stop-after-hours H] [--via auto|url|git]
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed mixed-merge n84 [--check]
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed mixed-plan n84 --parts 3
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed mixed-price
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed mixed-shard PACKET --runners 8
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed mixed-compare n84 BUNDLE --out F
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed mixed-control n37 --work W

Retained data files over 1,000 lines are stored as deterministic gzip, so every read goes
through `devtools.retained_data.read_retained_bytes` and every digest is the upstream one.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib
import importlib.metadata
import itertools
import json
import os
import platform
import re
import resource
import shutil
import subprocess
import sys
import tarfile
import time
import urllib.request
from collections import Counter, deque
from collections.abc import Callable, Iterable, Mapping
from concurrent.futures import FIRST_COMPLETED, Future, ProcessPoolExecutor, wait
from dataclasses import dataclass
from datetime import UTC, datetime
from fractions import Fraction
from math import isqrt
from pathlib import Path, PurePosixPath
from typing import Any, cast

from strif import atomic_write_text

from devtools import replay_receipt
from devtools.audit_wand125_rectangles import (
    CONTROL_FACTOR,
    coverage_exact,
    heaviest,
    least_covered,
    net_rotation,
    orbit_contributions,
)
from devtools.replay_evand_zmx2 import D4, d4_image
from devtools.retained_data import (
    GZIP_SUFFIX,
    LINE_THRESHOLD,
    compress,
    describe,
    git_blob,
    read_retained_bytes,
)

REPO = Path(__file__).resolve().parents[2]
PACKET = REPO / "packing/resources/web/wand125-point-and-mixed-2026-09-28"
SOURCE = PACKET / "square-packing-bounds"
MANIFEST = PACKET / "acquisition/sources.json"
SUBTREE = PACKET / "acquisition/upstream-subtree.sha256"
EXACT_RECEIPT = PACKET / "receipts/exact-audit.json"
REVISION = "39d8ecc74d651b54ec977c331c8f2015b442a6c4"
GIT_TREE = "936e2524c09ca137cf9e02dcd955d6737549253b"
SOURCE_URL = "https://github.com/wand125/square-packing-bounds"

#: The same repository's MIT licence, retained byte-identical with the rectangle packet.
RECTANGLE_LICENSE = (
    REPO / "packing/resources/web/wand125-rectangle-certificates-2026-09-27/wand125-rectangles"
) / "LICENSE"
#: Daniel's s(21) certificate, retained by the evand packet; the n21 support derives from it.
EVAND_S21 = (
    REPO / "packing/resources/web/evand-square-packing-2026-09-26/square-packing/s12"
) / "certificates/s21/s21_lower_4.9950.txt"

N45 = Path("point_n45_L7")
N21 = Path("point_n21_L5")
N50 = {
    "L740": Path("certificates/mixed_n50_L740"),
    "L735": Path("certificates/mixed_n50_L735"),
    "L7318": Path("certificates/mixed_n50_L7318"),
}
CLAIM_DIRS = (N45, N21, *N50.values())
TOP_FILES = (Path("README.md"), Path("LICENSE"))

#: zmx2 as the n45 verify.sh pins it: evand/square-packing commit and source digest.
ZMX2_COMMIT = "6e1223cf7ef2be4c70baaa36c0e7e7197076735a"
ZMX2_SOURCE_SHA256 = "6b7f0f79466bf25c9a85f8fe2f3866de734935f0521ea188136818c2fb5b3fed"

N45_COVER_SHA256 = "f7d706aa07506c351d9c4b76082cc391ae3f1fd20f6759496bd7c601bb0ca192"
N45_TOTAL = Fraction(12666371418707823, 2**48)
N21_HASHES = {
    "n21-original.txt": "84a7dae793f05ff72de52ddcd3058e8518c1f84c461f94d11305adefe6137679",
    "n21-capture-one.txt": "9f631fbae420e0376ea636a232b7680e937deebe205dc035cfb9c43a3d74b456",
    "upstream-s21-lower-4.9950.txt": (
        "c8e8f878205f2da9c213e4a87c06f17c5a759dce7e695e676dd5c50e0994f2ef"
    ),
}
N21_THRESHOLD = Fraction(249987, 250000)
N21_MASS = Fraction(2624862500021, 125000000000)
N21_GAP = Fraction(999979, 125000000000)

#: (side, rectangle count, manifest digest) the source states for each n = 50 rung.
N50_CLAIMS: dict[str, tuple[Fraction, int, str]] = {
    "L740": (
        Fraction(37, 5),
        553,
        "fdfaed937a788e0f2dcd45689927c59ffe62b1436aa06a4363a0ea6dd1a53fda",
    ),
    "L735": (
        Fraction(147, 20),
        499,
        "441c2612d81472a79f949f5cd453d2eb171c37faf0c34314ad309f77c0db0836",
    ),
    "L7318": (
        Fraction(3659, 500),
        355,
        "c0f46b688122f43b73e9ee63729900d6f2370b912452489ef2dd681ef9a67088",
    ),
}
N50_MASS = Fraction(4999999, 100000)
N50_STEP = Fraction(83, 40000)
N50_LAST = 200
#: ``code/mixed_rotated_verify.cpp``, the checker the L740 and L7318 manifests name.
N50_CHECKER_SHA256 = "89b674a6feabe24d91c29431de1624907c4bff83280ceb481475455686693652"
N50_TARBALLS = {
    "L740": "n50-L7.40-proof-bundle.tar.gz",
    "L735": "n50-L7.35-proof-bundle.tar.gz",
    "L7318": "n50-L7.318-proof-bundle.tar.gz",
}


def _pinned_only(path: Path) -> str | None:
    """Why an upstream file under the claim directories is pinned by digest and not copied."""
    parts = path.parts
    rules = (
        (
            path == Path("README.md"),
            "retained byte-identical by the 2026-09-28 rectangle packet",
        ),
        (
            path == Path("LICENSE"),
            "retained byte-identical by the 2026-09-27 rectangle packet",
        ),
        (
            parts[:2] == ("point_n21_L5", "data"),
            "n21 proof bundle archive part (463,568,316 bytes in 14 parts)",
        ),
        (
            parts[:2] == ("point_n21_L5", "verifier-source"),
            "readable copy of the bundle's Python, checked against it by unpack_bundle.py",
        ),
        (
            parts[:2] == ("point_n21_L5", "acceptance")
            and path.name.endswith("-linkage.json.gz"),
            "historical linkage record (about 5 MB compressed each)",
        ),
        (
            path == Path("point_n21_L5/lean/Sqpack/N21PtsData.lean"),
            "generated from n21-original.txt by the retained gen_n21pts_data.py",
        ),
        (
            parts[0] == "certificates" and path.name.endswith(".tar.gz"),
            "complete proof bundle (12.8 to 21.8 MB)",
        ),
        (
            parts[:3] == ("certificates", "mixed_n50_L7318", "code"),
            "byte-identical to certificates/mixed_n50_L740/code/",
        ),
    )
    return next((reason for matched, reason in rules if matched), None)


# --------------------------------------------------------------------------- helpers


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read(relative: Path, source: Path = SOURCE) -> bytes:
    return read_retained_bytes(source / relative)


def _json(relative: Path, source: Path = SOURCE) -> Any:
    return json.loads(_read(relative, source))


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_subtree_manifest(path: Path = SUBTREE) -> dict[Path, str]:
    """Parse the ``sha256sum``-style list of ``./``-relative upstream paths."""
    expected: dict[Path, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, separator, name = line.partition("  ")
        relative = Path(name.removeprefix("./"))
        _require(
            bool(separator)
            and re.fullmatch(r"[0-9a-f]{64}", digest) is not None
            and name.startswith("./")
            and not relative.is_absolute()
            and ".." not in relative.parts
            and relative not in expected,
            f"invalid or duplicate subtree entry: {line!r}",
        )
        expected[relative] = digest
    _require(bool(expected), "empty subtree manifest")
    return expected


def retained_files(source: Path = SOURCE) -> dict[Path, bytes]:
    """Every retained upstream file, keyed by its upstream path, decompressed."""
    files: dict[Path, bytes] = {}
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(source)
        if relative.name.endswith(GZIP_SUFFIX):
            relative = relative.with_name(relative.name.removesuffix(GZIP_SUFFIX))
        _require(relative not in files, f"retained twice, plain and compressed: {relative}")
        files[relative] = read_retained_bytes(path)
    return files


# --------------------------------------------------------------------------- n = 45


def n45_cover(data: bytes, provenance: dict[str, Any]) -> dict[str, Any]:
    """Format, nonnegativity, D4 invariance and exact total of the n45 point cover."""
    _require(_sha256(data) == N45_COVER_SHA256, "cover.txt SHA-256 differs from the pin")
    _require(
        provenance.get("cover_sha256") == N45_COVER_SHA256, "provenance pins another cover"
    )
    values = [int(token) for token in data.split()]
    side_num, side_den, denominator, weight_den, count = values[:5]
    _require((side_num, side_den) == (7, 1), "container side is not 7")
    _require(denominator > 0 and weight_den > 0, "nonpositive denominator")
    _require(len(values) == 5 + 3 * count, "entry count disagrees with the header")
    span = 7 * denominator
    mass: Counter[tuple[int, int]] = Counter()
    for index in range(5, len(values), 3):
        x, y, w = values[index : index + 3]
        _require(0 <= x <= span and 0 <= y <= span, f"point outside [0,7]^2: {(x, y)}")
        _require(w >= 0, "negative weight")
        mass[x, y] += w
    for (x, y), w in mass.items():
        for image in ((span - x, y), (x, span - y), (y, x)):
            _require(mass.get(image, 0) == w, f"not D4-invariant at {(x, y)}")
    total = Fraction(sum(mass.values()), weight_den)
    _require(total == N45_TOTAL, "total differs from 12666371418707823/2^48")
    _require(str(total) == provenance.get("total"), "total differs from provenance.json")
    _require(total < 45, "total is not below 45")
    return {
        "sha256": N45_COVER_SHA256,
        "entries": count,
        "distinct_points": len(mass),
        "positive_points": sum(1 for w in mass.values() if w > 0),
        "coordinate_denominator": denominator,
        "weight_denominator": weight_den,
        "total": str(total),
        "total_float": float(total),
        "margin_below_45": str(45 - total),
        "d4_invariant": True,
        "coverage_decided_here": False,
    }


_ROOT_LINE = re.compile(
    r"ROOT (\d+) pass (\d+) root (\S+) boxes (\d+) cert (\d+) empty (\d+) uncert (\d+) "
    r"maxdepth (\d+) capped (\d+) ms (\d+)"
)


def n45_compare(run_dir: Path, provenance: dict[str, Any]) -> dict[str, Any]:
    """Compare a ``verify.sh`` run directory with the source's reference run."""
    roots_log = read_retained_bytes(run_dir / "roots.log")
    lines = roots_log.decode("ascii").splitlines()
    rows = [_ROOT_LINE.fullmatch(line) for line in lines if line.startswith("ROOT ")]
    _require(all(rows), "unparsed ROOT line")
    matches = [row for row in rows if row is not None]
    roots = {(m[2], m[3]) for m in matches}
    run_log = read_retained_bytes(run_dir / "run.log").decode("utf-8")
    verdicts = [line for line in run_log.splitlines() if line.startswith("VERIFIED-D4:")]
    reference = provenance["reference_run"]
    summary = {
        "root_lines": len(matches),
        "distinct_roots": len(roots),
        "boxes": sum(int(m[4]) for m in matches),
        "certified_leaves": sum(int(m[5]) for m in matches),
        "empty_leaves": sum(int(m[6]) for m in matches),
        "uncertified": sum(int(m[7]) for m in matches),
        "max_depth": max(int(m[8]) for m in matches),
        "capped": sum(int(m[9]) for m in matches),
        "root_ms_sum": sum(int(m[10]) for m in matches),
        "verdict_line": verdicts[-1] if verdicts else None,
        "not_verified_lines": run_log.count("NOT VERIFIED"),
        "roots_log_sha256": _sha256(roots_log),
    }
    agreement = {
        "roots": summary["distinct_roots"] == reference["roots"] == len(matches),
        "uncertified": summary["uncertified"] == reference["uncertified"] == 0,
        "capped": summary["capped"] == reference["capped"] == 0,
        "boxes": summary["boxes"] == reference["boxes"],
        "max_depth": summary["max_depth"] == reference["max_depth"],
        "verdict": bool(verdicts) and summary["not_verified_lines"] == 0,
    }
    return {
        "status": "MATCHES_SOURCE_REFERENCE" if all(agreement.values()) else "DIFFERS",
        "replay": summary,
        "reference": reference,
        "agreement": agreement,
        "note": (
            "The roots log carries per-root milliseconds, so its digest cannot equal the "
            "source's roots_sha256; the box and depth totals are compared instead."
        ),
    }


# --------------------------------------------------------------------------- n = 21


def _points(data: bytes) -> tuple[Fraction, list[tuple[Fraction, Fraction, Fraction]]]:
    a, b, d, w, n, *values = (int(token) for token in data.split())
    _require(min(a, b, d, w) > 0 and n >= 0 and len(values) == 3 * n, "invalid point header")
    side = Fraction(a, b)
    points = [
        (Fraction(x, d), Fraction(y, d), Fraction(v, w))
        for x, y, v in zip(values[::3], values[1::3], values[2::3], strict=True)
    ]
    for x, y, v in points:
        _require(0 <= x <= side and 0 <= y <= side and v >= 0, "invalid point or weight")
    return side, points


def n21_certificates(source: Path = SOURCE) -> dict[str, Any]:
    """The n21 point measure's exact algebra, recomputed from the retained files."""
    raw = {name: _read(N21 / "certificates" / name, source) for name in N21_HASHES}
    for name, data in raw.items():
        _require(_sha256(data) == N21_HASHES[name], f"{name} SHA-256 differs from the pin")
    side, original = _points(raw["n21-original.txt"])
    normalized_side, normalized = _points(raw["n21-capture-one.txt"])
    upstream_side, upstream = _points(raw["upstream-s21-lower-4.9950.txt"])
    _require(side == normalized_side == 5, "container side is not 5")
    _require(upstream_side == Fraction(5000, 1001), "Daniel's side is not 5000/1001")
    _require(len(original) == len(normalized) == len(upstream) == 4604, "entry count")
    q = N21_THRESHOLD
    _require(
        normalized == [(x, y, v / q) for x, y, v in original], "normalized != original / q"
    )
    scale = Fraction(1001, 1000)
    _require(
        [(x, y) for x, y, _ in original] == [(x * scale, y * scale) for x, y, _ in upstream],
        "support is not Daniel's, scaled by 1001/1000 in the same order",
    )
    weights = {(x, y): v for x, y, v in original}
    _require(len(weights) == 4604, "coordinates are not distinct")
    for (x, y), v in weights.items():
        for image in ((5 - x, y), (x, 5 - y), (y, x)):
            _require(weights.get(image) == v, f"not D4-invariant at {(x, y)}")
    mass = sum(weights.values(), Fraction(0))
    _require(mass == N21_MASS, "mass differs from 2624862500021/125000000000")
    gap = 21 * q - mass
    _require(gap == N21_GAP and gap > 0, "21q - mass is not 999979/125000000000")
    evand = read_retained_bytes(EVAND_S21)
    _require(evand == raw["upstream-s21-lower-4.9950.txt"], "evand packet copy differs")
    check = _json(N21 / "certificate-data-check.json", source)
    _require(check["mass"] == str(mass) and check["strict_gap"] == str(gap), "data check")
    return {
        "hashes": N21_HASHES,
        "entries": len(original),
        "positive_entries": sum(1 for v in weights.values() if v > 0),
        "zero_entries": sum(1 for v in weights.values() if v == 0),
        "threshold": str(q),
        "mass": str(mass),
        "normalized_mass": str(mass / q),
        "strict_gap": str(gap),
        "strict_gap_float": float(gap),
        "d4_invariant": True,
        "support_is_evand_s21_scaled_by": str(scale),
        "evand_packet_copy_identical": True,
        "coverage_decided_here": False,
    }


#: The M1 run's complete linkage record, pinned by digest (compressed, decompressed).
M1_LINKAGE_SHA256 = (
    "0d93072b65c1b162e1cba99db64a14b7f85e21f50b98da720247d3234c665f02",
    "6efc5fe539db5a37ec1ac0851271cee4c51dc5912d886d059ef253769bf7e0dc",
)
_STAGE_DIR = re.compile(r"/(root|sieve|frontier-s\d+)/(.+)$")


def _stage_relative(bindings: dict[str, str]) -> dict[str, str]:
    """Output bindings keyed by the path below the stage directory, not the run root."""
    relative: dict[str, str] = {}
    for path, digest in bindings.items():
        match = _STAGE_DIR.search(path)
        _require(match is not None, f"output outside a stage directory: {path}")
        assert match is not None
        key = f"{match[1]}/{match[2]}"
        _require(key not in relative, f"output bound twice: {key}")
        relative[key] = digest
    return relative


def compare_outputs(linkage: Path, m1_linkage: Path) -> dict[str, Any]:
    """Every output file of a fresh run against the M1 run's, by stage-relative path."""
    packed = m1_linkage.read_bytes()
    raw = gzip.decompress(packed)
    _require((_sha256(packed), _sha256(raw)) == M1_LINKAGE_SHA256, "M1 linkage is not pinned")
    ours = _stage_relative(json.loads(linkage.read_text())["output_bindings"])
    theirs = _stage_relative(json.loads(raw)["output_bindings"])
    shared = set(ours) & set(theirs)
    differing = sorted(key for key in shared if ours[key] != theirs[key])
    return {
        "outputs_here": len(ours),
        "outputs_m1": len(theirs),
        "identical": len(shared) - len(differing),
        "differing": len(differing),
        "differing_names": sorted({Path(key).name for key in differing}),
        "differing_examples": differing[:12],
        "only_here": sorted(set(ours) - set(theirs))[:12],
        "only_m1": sorted(set(theirs) - set(ours))[:12],
    }


#: What a finished ``verify_portable.py`` output directory contributes to the receipts.
N21_RECEIPT_FILES = ("result.json", "run-inputs.json")


def n21_collect(out: Path, receipts: Path, m1_linkage: Path | None) -> dict[str, Any]:
    """Copy a finished run's summary, exit records and stage logs into ``receipts``.

    The comparison is written as ``comparison.json``; logs over the line threshold are
    stored as deterministic gzip. Proof objects and ``linkage.json`` stay in ``out``;
    the comparison records their digests. ``receipts`` may be relative to the working
    directory, as the packet README writes it; the table rows are relative to the packet.
    """
    result = n21_compare(out, m1_linkage=m1_linkage)
    receipts = receipts.resolve()
    receipts.mkdir(parents=True, exist_ok=True)
    names = [*N21_RECEIPT_FILES, *(p.name for p in sorted(out.glob("*-exit.json")))]
    names += [p.name for p in sorted(out.glob("*.log"))]
    stored: list[str] = []
    rows: list[str] = []
    for name in names:
        target = receipts / name
        shutil.copyfile(out / name, target)
        if (
            target.suffix in {".json", ".log"}
            and target.read_bytes().count(b"\n") > LINE_THRESHOLD
        ):
            target = compress(target)
            rows.append(describe(PACKET, target, "receipt").markdown())
        stored.append(target.name)
    atomic_write_text(
        receipts / "comparison.json", json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return result | {"stored": stored, "compressed_file_rows": rows}


def compare_stage_files(out: Path, m1_linkage: Path, stages: list[str]) -> dict[str, Any]:
    """Hash the files a run has written so far under ``stages`` and compare with M1's.

    Works on an unfinished run: only the named, completed stage directories are read.
    """
    packed = m1_linkage.read_bytes()
    raw = gzip.decompress(packed)
    _require((_sha256(packed), _sha256(raw)) == M1_LINKAGE_SHA256, "M1 linkage is not pinned")
    theirs = _stage_relative(json.loads(raw)["output_bindings"])
    report: dict[str, Any] = {}
    for stage in stages:
        ours = {
            f"{stage}/{path.relative_to(out / stage).as_posix()}": _sha256(path.read_bytes())
            for path in sorted((out / stage).rglob("*"))
            if path.is_file()
        }
        expected = {key: value for key, value in theirs.items() if key.startswith(f"{stage}/")}
        shared = set(ours) & set(expected)
        differing = sorted(key for key in shared if ours[key] != expected[key])
        report[stage] = {
            "files_here": len(ours),
            "files_m1": len(expected),
            "identical": len(shared) - len(differing),
            "differing": differing[:12],
            "only_here": sorted(set(ours) - set(expected))[:12],
            "only_m1": sorted(set(expected) - set(ours))[:12],
        }
    return {"status": "STAGE_FILES_COMPARED", "stages": report}


def n21_compare(
    out: Path, source: Path = SOURCE, m1_linkage: Path | None = None
) -> dict[str, Any]:
    """Compare a fresh ``verify_portable.py`` run with the source's M1 record."""
    reference = _json(N21 / "acceptance/m1-full-replay.json", source)
    result = json.loads((out / "result.json").read_text())
    run_inputs = json.loads((out / "run-inputs.json").read_text())
    exits = [json.loads(path.read_text()) for path in sorted(out.glob("*-exit.json"))]
    keys = (
        "status",
        "candidate_sha256",
        "root_count",
        "sieve_count",
        "frontier_count",
        "excluded_count",
        "threshold",
        "mass",
        "strict_gap",
        "independent_external_review",
        "formal_verification",
    )
    agreement = {key: result.get(key) == reference.get(key) for key in keys}
    agreement["all_stages_exit_zero"] = bool(exits) and all(
        item["exit_code"] == 0 for item in exits
    )
    linkage = out / "linkage.json"
    stages = [
        {
            "stage": item["stage"],
            "shard": item["shard"],
            "exit_code": item["exit_code"],
            "seconds": item["seconds"],
        }
        for item in exits
    ]
    outputs = compare_outputs(linkage, m1_linkage) if m1_linkage else None
    return {
        "status": "MATCHES_SOURCE_M1_RECORD" if all(agreement.values()) else "DIFFERS",
        "agreement": agreement,
        "outputs_against_m1": outputs,
        "replay": {key: result.get(key) for key in keys}
        | {
            "seconds": result.get("seconds"),
            "workers": run_inputs.get("workers"),
            "python": run_inputs.get("python"),
            "platform": run_inputs.get("platform"),
            "bindings": run_inputs.get("bindings"),
            "stages": stages,
            "linkage_sha256": _sha256(linkage.read_bytes()) if linkage.exists() else None,
            "result_sha256": _sha256((out / "result.json").read_bytes()),
        },
        "reference": {key: reference.get(key) for key in (*keys, "seconds", "linkage_sha256")}
        | {
            "stages": [
                {key: item[key] for key in ("stage", "shard", "exit_code", "seconds")}
                for item in reference["worker_exits"]
            ]
        },
        "note": (
            "Linkage records embed absolute output paths and per-run output digests, so "
            "their SHA-256 differs between runs; the certified quantities are compared."
        ),
    }


# --------------------------------------------------------------------------- n = 21 controls

#: Stage 4 of ``campaign/result-import.md`` for the ``s(21)`` replay: the source's
#: ``verify_portable.py``, run on two mutated covers, must refuse each.
N21_CONTROL_KIND = "wand125-n21-control/v1"
N21_MUTATIONS = ("drop-heaviest-point", "move-point")
#: ``move-point`` moves the entry at ``(1, 7/10)`` by ``(1/1000, 0)``, in the file's
#: units of 1/1000, and each D4 image of it by the image of that move.
N21_MOVE = ((1000, 700), (1, 0))
#: The witness: the closed unit square ``[0, 1]^2`` at angle zero, the one admissible
#: pose of root box 832 (centre ``[2/5, 1/2]^2``, ``t`` in ``[0, 1/16]``), which is the
#: first of the 5,000 root boxes, in the order the root stage runs them, to hold one.
N21_WITNESS_CORNER = (0, 0)
N21_WITNESS_ROOT = 832
N21_WORKERS = 2
N21_CONTROL_TIMEOUT = 1800
N21_CONTROLS = PACKET / "receipts/controls"
#: The cover inside the bundle, byte-identical to ``certificates/n21-original.txt``.
N21_BUNDLE_CANDIDATE = (
    "runs/evand_n21_n32_bridge_20260927/results/"
    "n21_L5_refit29_counterexample_trial/refit/candidate.txt"
)
#: The checker's own refusals of a root-stage witness (``replay_physical_point_witness``).
N21_REFUSALS = (
    re.compile(r"ValueError: Insufficient witness mass"),
    re.compile(r"ValueError: Point containment not proved: (?P<index>\d+)"),
)
#: A maximal run of lower-case hex; one of exactly 64 characters is a SHA-256 as the
#: records write one. (Faster than look-arounds, and the same tokens.)
_HEX_RUN = re.compile(rb"[0-9a-f]{64,}")
_FRAME = re.compile(r'^\s*File "(?P<file>[^"]+)", line (?P<line>\d+), in (?P<name>\S+)$')


@dataclass(frozen=True, slots=True)
class N21Mutation:
    """A mutated ``s(21)`` cover: its bytes, the entries it changed, and how."""

    kind: str
    data: bytes
    #: Entry indices changed, in file order; the proof records index entries by position,
    #: so no entry is ever removed.
    rows: tuple[int, ...]
    detail: str


def _n21_rows(data: bytes) -> tuple[list[bytes], int, tuple[int, ...], list[list[int]]]:
    """The file's lines, the line of entry 0, the five header integers, and the entries.

    Every entry must be alone on its own line, so that a mutation rewrites lines.
    """
    lines = data.splitlines(keepends=True)
    tokens = 0
    first = 0
    while tokens < 5:
        _require(first < len(lines), "the header is incomplete")
        tokens += len(lines[first].split())
        first += 1
    _require(tokens == 5, "the header shares a line with an entry")
    a, b, d, w, n, *values = (int(token) for token in data.split())
    _require(min(a, b, d, w) > 0 and len(values) == 3 * n, "invalid point header")
    entries = [values[3 * i : 3 * i + 3] for i in range(n)]
    _require(len(lines) == first + n, "an entry is not alone on its line")
    for i, entry in enumerate(entries):
        _require([int(t) for t in lines[first + i].split()] == entry, f"entry {i} is split")
    return lines, first, (a, b, d, w, n), entries


def mutate_n21(data: bytes, kind: str) -> N21Mutation:
    """Apply ``kind`` (one of `N21_MUTATIONS`) to an ``s(21)`` point file.

    ``drop-heaviest-point`` sets to zero the weight of every entry at a D4 image of the
    location carrying the most weight (ties to the least ``(X, Y)``); ``move-point``
    moves the entry at ``N21_MOVE`` and each of its D4 images by the image of the move.
    Both keep every entry in place, as ``FORMAT.md`` requires of a file the proof trees
    index, and keep the cover D4-invariant, so the replay's quarter-turn reduction still
    applies.
    """
    lines, first, (a, b, d, w, _n), entries = _n21_rows(data)
    edge, remainder = divmod(a * d, b)
    _require(remainder == 0, "the side is not a multiple of 1/D")
    where = {(x, y): i for i, (x, y, _v) in enumerate(entries)}
    _require(len(where) == len(entries), "coordinates are not distinct")
    changed: dict[int, list[int]] = {}
    if kind == "drop-heaviest-point":
        heaviest = min(where, key=lambda p: (-entries[where[p]][2], p))
        orbit = sorted({d4_image(heaviest, edge, g) for g in D4})
        for image in orbit:
            x, y, _v = entries[where[image]]
            changed[where[image]] = [x, y, 0]
        weight = entries[where[heaviest]][2]
        detail = (
            f"sets to zero the weights of the {len(orbit)} entries at the D4 images of "
            f"({heaviest[0]}, {heaviest[1]})/{d}, {weight}/{w} each"
        )
    elif kind == "move-point":
        (px, py), (dx, dy) = N21_MOVE
        moves: dict[tuple[int, int], tuple[int, int]] = {}
        for g in D4:
            image, moved = d4_image((px, py), edge, g), d4_image((px + dx, py + dy), edge, g)
            _require(moves.setdefault(image, moved) == moved, "the move is not D4-equivariant")
        for image, moved in sorted(moves.items()):
            _require(image in where, f"no entry at {image}")
            _require(all(0 <= v <= edge for v in moved), f"{moved} leaves the container")
            _require(moved not in where, f"{moved} is already an entry")
            changed[where[image]] = [*moved, entries[where[image]][2]]
        _require(len(set(moves.values())) == len(moves), "two images move to one place")
        detail = (
            f"moves the {len(moves)} entries at the D4 images of ({px}, {py})/{d} by the "
            f"images of ({dx}, {dy})/{d}, keeping their weights"
        )
    else:
        raise ValueError(f"unknown mutation: {kind}")
    out = list(lines)
    for i, entry in changed.items():
        line = lines[first + i]
        ending = line[len(line.rstrip(b"\r\n")) :]
        out[first + i] = " ".join(map(str, entry)).encode() + ending
    return N21Mutation(kind, b"".join(out), tuple(sorted(changed)), detail)


def n21_square_capture(data: bytes, corner: tuple[int, int]) -> Fraction:
    """The weight in the closed axis-parallel unit square with lower-left ``corner``."""
    _lines, _first, (_a, _b, d, w, _n), entries = _n21_rows(data)
    x0, y0 = corner
    inside = (v for x, y, v in entries if x0 <= x <= x0 + d and y0 <= y <= y0 + d)
    return Fraction(sum(inside), w)


def n21_cover_facts(data: bytes) -> dict[str, Any]:
    """Exact facts of a cover in the ``s(21)`` format: total, D4 invariance, distinctness."""
    _lines, _first, (a, b, d, w, _n), entries = _n21_rows(data)
    edge = a * d // b
    weights = {(x, y): v for x, y, v in entries}
    total = Fraction(sum(v for *_, v in entries), w)
    return {
        "sha256": _sha256(data),
        "entries": len(entries),
        "positive_entries": sum(1 for *_, v in entries if v > 0),
        "coordinates_distinct": len(weights) == len(entries),
        "nonnegative": all(v >= 0 for *_, v in entries),
        "d4_invariant": all(
            weights.get(d4_image(p, edge, g)) == v for p, v in weights.items() for g in D4
        ),
        "total": str(total),
        "below_21q": total < 21 * N21_THRESHOLD,
    }


@dataclass(slots=True)
class _BundleFile:
    """One bundle file as the re-binding sees it."""

    sha256: str
    #: SHA-256 of the decompressed bytes, for a ``.gz`` file.
    content_sha256: str | None
    tokens: frozenset[bytes]


def _payload(rel: str, raw: bytes) -> bytes:
    return gzip.decompress(raw) if rel.endswith(".gz") else raw


def scan_n21_bundle(bundle: Path) -> tuple[dict[str, Any], dict[str, _BundleFile]]:
    """Check an unpacked bundle against its manifest, and index the digests each file names.

    The manifest must be the one the retained ``archive-index.json`` pins, and every file
    it lists must have its size and SHA-256, as ``unpack_bundle.py`` checks; byte-code
    caches are the only other files allowed.
    """
    index = _json(N21 / "archive-index.json")
    raw_manifest = (bundle / "portable-manifest.json").read_bytes()
    _require(_sha256(raw_manifest) == index["manifest_sha256"], "the manifest is not pinned")
    manifest = json.loads(raw_manifest)
    files: dict[str, _BundleFile] = {}
    for rel, record in manifest["files"].items():
        raw = (bundle / rel).read_bytes()
        digest = _sha256(raw)
        _require(len(raw) == record["bytes"] and digest == record["sha256"], f"{rel} differs")
        payload = _payload(rel, raw)
        files[rel] = _BundleFile(
            digest,
            _sha256(payload) if rel.endswith(".gz") else None,
            frozenset(token for token in _HEX_RUN.findall(payload) if len(token) == 64),
        )
    present = {
        p.relative_to(bundle).as_posix()
        for p in bundle.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    }
    _require(present == set(files) | {"portable-manifest.json"}, "the bundle's file set")
    _require(files[N21_BUNDLE_CANDIDATE].sha256 == N21_HASHES["n21-original.txt"], "candidate")
    return manifest, files


def rebind_n21_bundle(
    bundle: Path,
    target: Path,
    data: bytes,
    scanned: tuple[dict[str, Any], dict[str, _BundleFile]] | None = None,
) -> dict[str, Any]:
    """Write ``target``: the bundle with its cover replaced by ``data`` and re-bound to it.

    The proof records name the cover by its SHA-256, and name other records by theirs. A
    file that names the cover's digest, or the digest of a file so rewritten (its own or,
    for ``.gz``, its decompressed bytes'), is rewritten with each such digest replaced by
    the new one, in dependency order, and the manifest is rewritten to the new sizes and
    digests. Every other file is a hard link to the pristine one. Python files are never
    rewritten: one that names a replaced digest is listed, and left as it is.
    """
    manifest, files = scanned or scan_n21_bundle(bundle)
    old = files[N21_BUNDLE_CANDIDATE].sha256
    by_digest: dict[str, list[str]] = {}
    naming: dict[bytes, list[str]] = {}
    for rel, item in files.items():
        for digest in filter(None, (item.sha256, item.content_sha256)):
            by_digest.setdefault(digest, []).append(rel)
        for token in item.tokens:
            naming.setdefault(token, []).append(rel)
    # Every file that names the cover's digest, or a digest of a file already in the set.
    affected = {N21_BUNDLE_CANDIDATE}
    code: set[str] = set()
    queue, seen = deque([old]), {old}
    while queue:
        for rel in naming.get(queue.popleft().encode(), []):
            if rel.endswith(".py"):
                code.add(rel)
            elif rel not in affected:
                affected.add(rel)
                fresh = {files[rel].sha256, files[rel].content_sha256} - {None} - seen
                seen |= fresh
                queue.extend(sorted(d for d in fresh if d is not None))
    # A file is rewritten once every affected file it names has its new digests.
    waiting: dict[str, set[str]] = {}
    named_by: dict[str, list[str]] = {}
    for rel in sorted(affected - {N21_BUNDLE_CANDIDATE}):
        deps = {
            other
            for token in files[rel].tokens
            for other in by_digest.get(token.decode(), [])
            if other in affected and other != rel
        }
        waiting[rel] = deps
        for other in deps:
            named_by.setdefault(other, []).append(rel)
    new: dict[str, str] = {}
    sizes: dict[str, tuple[str, int]] = {}
    if target.exists():
        shutil.rmtree(target)

    def substitute(payload: bytes) -> bytes:
        return _HEX_RUN.sub(lambda m: new.get(m[0].decode(), m[0].decode()).encode(), payload)

    def finish(rel: str, raw: bytes, payload: bytes) -> None:
        item = files[rel]
        for before, after in (
            (item.sha256, _sha256(raw)),
            (item.content_sha256, _sha256(payload)),
        ):
            if before is not None:
                _require(new.setdefault(before, after) == after, f"{rel}: two rewrites")
        path = target / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        sizes[rel] = (_sha256(raw), len(raw))
        for other in named_by.get(rel, []):
            waiting[other].discard(rel)
            if not waiting[other]:
                ready.append(other)

    ready = deque(sorted(rel for rel, deps in waiting.items() if not deps))
    finish(N21_BUNDLE_CANDIDATE, data, data)
    while ready:
        rel = ready.popleft()
        if rel in sizes:
            continue
        payload = substitute(_payload(rel, (bundle / rel).read_bytes()))
        packed = rel.endswith(".gz")
        finish(
            rel,
            gzip.compress(payload, compresslevel=9, mtime=0) if packed else payload,
            payload,
        )
    _require(set(sizes) == affected, "the records' digests form a cycle")
    rebound = json.loads(substitute(json.dumps(manifest).encode()))
    for rel, (digest, size) in sizes.items():
        rebound["files"][rel] = {"sha256": digest, "bytes": size}
    for rel in files:
        if rel not in sizes:
            path = target / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            os.link(bundle / rel, path)
    manifest_text = json.dumps(rebound, indent=2) + "\n"
    (target / "portable-manifest.json").write_text(manifest_text, encoding="utf-8")
    folders = Counter(rel.split("/")[3] if rel.startswith("runs/") else rel for rel in sizes)
    return {
        "pristine_manifest_sha256": _sha256((bundle / "portable-manifest.json").read_bytes()),
        "rebound_manifest_sha256": _sha256(manifest_text.encode()),
        "files": len(files),
        "files_rewritten": len(sizes),
        "gzip_rewritten": sum(1 for rel in sizes if rel.endswith(".gz")),
        "digests_replaced": len(new),
        "rewritten_by_folder": dict(sorted(folders.items())),
        "python_naming_a_replaced_digest": sorted(code),
    }


def _n21_outcome(run: Path, mutation: N21Mutation) -> dict[str, Any]:
    """What a ``verify_portable.py`` run on a mutated cover ended with, read from ``run``."""
    exits = [json.loads(p.read_text()) for p in sorted(run.glob("*-exit.json"))]
    failed = [item for item in exits if item["exit_code"] != 0]
    failure = run / "failure.json"
    outcome: dict[str, Any] = {
        "stage_exits": [
            {key: item[key] for key in ("stage", "shard", "exit_code", "seconds")}
            for item in exits
        ],
        "failure": json.loads(failure.read_text()) if failure.exists() else None,
        "result": json.loads((run / "result.json").read_text())
        if (run / "result.json").exists()
        else None,
    }
    if len(failed) != 1:
        return outcome | {"verdict": "ACCEPTED" if outcome["result"] else "CRASHED"}
    item = failed[0]
    name = item["stage"] if item["shard"] is None else f"frontier-s{item['shard']}"
    log = (run / f"{name}.log").read_text(encoding="utf-8")
    last = log.rstrip().splitlines()[-1]
    frames = [m for line in log.splitlines() if (m := _FRAME.match(line))]
    refusal = next((m for pattern in N21_REFUSALS if (m := pattern.fullmatch(last))), None)
    index = refusal.groupdict().get("index") if refusal else None
    refused = refusal is not None and (index is None or int(index) in mutation.rows)
    proofs = run / name / "proofs"
    return outcome | {
        "verdict": "REFUSED" if refused else "CRASHED",
        "stage": name,
        "stage_log": name + ".log",
        "parents_completed": len(list(proofs.glob("*.json"))) if proofs.is_dir() else None,
        "refusal": last,
        "raised_in": {
            "file": Path(frames[-1]["file"]).name,
            "function": frames[-1]["name"],
            "line": int(frames[-1]["line"]),
        }
        if frames
        else None,
    }


def n21_control(
    kind: str,
    bundle: Path,
    work: Path,
    out: Path = N21_CONTROLS,
    scanned: tuple[dict[str, Any], dict[str, _BundleFile]] | None = None,
) -> dict[str, Any]:
    """Run ``verify_portable.py`` on the ``kind`` mutation of the ``s(21)`` cover.

    The cover is regenerated from the retained ``n21-original.txt``; the witness square
    must hold at least the threshold before the mutation and less after it, so the
    mutated cover is provably not a certificate. ``bundle`` is a pristine unpacking,
    checked file by file against the pinned manifest (``scanned``, when one scan serves
    several controls); a hard-linked copy is re-bound to the mutated cover
    (`rebind_n21_bundle`), so that the source's digest checks pass and only the replay's
    arithmetic can refuse. The retained ``verify_portable.py`` and
    ``assemble_portable.py``, which must be the accepting run's, then run on it with the
    accepting run's ``--workers``, under ``devtools.replay_receipt``. The source's runner
    has no subset mode, so it runs to its first failure, which must be one of the
    witness replay's own refusals (`N21_REFUSALS`), not a crash. The re-bound copy is
    removed afterwards; the run's own directory is kept in ``work``.
    """
    accepted = json.loads((PACKET / "receipts/n21/run-inputs.json").read_text())["bindings"]
    by_name = {Path(path).name: digest for path, digest in accepted.items()}
    package = work / "package"
    package.mkdir(parents=True, exist_ok=True)
    for name in ("verify_portable.py", "assemble_portable.py"):
        script = _read(N21 / name)
        _require(_sha256(script) == by_name[name], f"{name} is not the accepting run's")
        (package / name).write_bytes(script)
    original = _read(N21 / "certificates/n21-original.txt")
    mutation = mutate_n21(original, kind)
    before = n21_square_capture(original, N21_WITNESS_CORNER)
    after = n21_square_capture(mutation.data, N21_WITNESS_CORNER)
    _require(before >= N21_THRESHOLD > after, "the witness square does not lose its cover")
    facts = n21_cover_facts(mutation.data)
    _require(
        facts["nonnegative"] and facts["d4_invariant"] and facts["coordinates_distinct"],
        "the mutated cover is not a well-formed D4-invariant measure",
    )
    _require(facts["below_21q"] and facts["sha256"] != _sha256(original), "mutated cover")
    scanned = scanned or scan_n21_bundle(bundle)
    _require(
        _sha256((bundle / "portable_replay.py").read_bytes()) == by_name["portable_replay.py"],
        "portable_replay.py is not the accepting run's",
    )
    folder = work / kind
    if folder.exists():
        shutil.rmtree(folder)
    rebinding = rebind_n21_bundle(bundle, folder / "bundle", mutation.data, scanned)
    run = folder / "run"
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    out.mkdir(parents=True, exist_ok=True)
    receipt = out / f"n21_control_{kind}.log"
    fields = replay_receipt.run(
        [
            sys.executable,
            "verify_portable.py",
            "--bundle",
            str(folder / "bundle"),
            "--workers",
            str(N21_WORKERS),
            "--out",
            str(run),
        ],
        receipt=receipt,
        cwd_label=(
            f"point_n21_L5/ staged by devtools.audit_wand125_point_and_mixed n21-control: "
            f"verify_portable.py {by_name['verify_portable.py']} and assemble_portable.py "
            f"{by_name['assemble_portable.py']} from {PACKET.relative_to(REPO)}; bundle "
            f"{rebinding['pristine_manifest_sha256']} re-bound to cover {facts['sha256']}, "
            f"the {kind} mutation of {N21_HASHES['n21-original.txt']}: {mutation.detail}"
        ),
        python_note=(
            f"the project interpreter, CPython {platform.python_version()} with NumPy "
            f"{_version('numpy')} and SciPy {_version('scipy')}"
        ),
        chdir=package,
        time_limit=N21_CONTROL_TIMEOUT,
    )
    outcome = _n21_outcome(run, mutation)
    shutil.rmtree(folder / "bundle")
    if "stage_log" in outcome:
        shutil.copyfile(
            run / outcome["stage_log"], out / f"n21_control_{kind}_{outcome['stage_log']}"
        )
    refused = outcome["verdict"] == "REFUSED" and fields["exit"] != 0
    result = {
        "kind": N21_CONTROL_KIND,
        "status": "CONTROL_REFUSED" if refused else "CONTROL_FAILED",
        "certificate": N21.as_posix(),
        "revision": REVISION,
        "mutation": {
            "kind": kind,
            "detail": mutation.detail,
            "rows": list(mutation.rows),
            "original_sha256": N21_HASHES["n21-original.txt"],
        }
        | facts,
        "witness": {
            "square": f"[{N21_WITNESS_CORNER[0]}, 1] x [{N21_WITNESS_CORNER[1]}, 1], closed, "
            "at angle zero",
            "root": N21_WITNESS_ROOT,
            "threshold": str(N21_THRESHOLD),
            "capture_original_exact": str(before),
            "capture_mutated_exact": str(after),
        },
        "checker": {
            "verify_portable_sha256": by_name["verify_portable.py"],
            "assemble_portable_sha256": by_name["assemble_portable.py"],
            "portable_replay_sha256": by_name["portable_replay.py"],
            "accepting_run": "receipts/n21/run-inputs.json",
            "workers": N21_WORKERS,
        },
        "rebinding": rebinding,
        "run": {
            key: fields[key]
            for key in ("started_utc", "ended_utc", "exit", "wall_seconds", "cpu_seconds")
        }
        | outcome,
        "receipt": receipt.name,
        "scope": (
            "A stage-4 negative control: the source's verify_portable.py, unchanged, on a "
            "copy of the pinned bundle whose cover is mutated and whose records are "
            "re-bound to it by digest. The witness square proves the mutated cover is not "
            "a certificate; the runner has no subset mode and runs to its first failure."
        ),
    }
    atomic_write_text(
        out / f"n21_control_{kind}.json", json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return result


def _version(distribution: str) -> str | None:
    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return None


# --------------------------------------------------------------------------- n = 50


def _n50_measure(data: dict[str, Any]) -> tuple[Fraction, Fraction, list[tuple[Any, ...]]]:
    """(L, B, [(x0, y0, x1, y1, mass)]) for either upstream candidate schema."""
    side, core = Fraction(data["L"]), Fraction(data["B"])
    if "rectangles" in data:
        _require(not data.get("points"), "unexpected point masses")
        records, key = data["rectangles"], "rectangle"
    else:
        _require(data.get("schema") == "point_line_rectangle_v1", "unknown candidate schema")
        records, key = data["primitives"], "geometry"
        _require(all(r["kind"] == "rectangle" for r in records), "non-rectangle primitive")
    items = [(*map(Fraction, r[key]), Fraction(r["mass"])) for r in records]
    return side, core, items


def _semantic_digest(data: dict[str, Any]) -> str:
    """The source's candidate digest (mixed_density_check.expand), recomputed."""
    keys = ["n", "L", "B", "rectangles", "points", "total_mass"]
    if "proof_net" in data:
        keys.append("proof_net")
    semantic = {key: data[key] for key in keys}
    text = json.dumps(semantic, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode()).hexdigest()


def exceeds_green(value: Fraction) -> bool:
    """Whether ``value > 2√2 + 101/25 + 3√14/25``, decided in exact rational arithmetic.

    With ``x = value - 101/25`` the claim is ``x > 2√2 + (3/25)√14``. Both sides are
    positive, so it is ``x > 0`` and ``x² - 8 - 126/625 > (12/25)√28``, and squaring once
    more removes the last root. Equality is impossible for a rational ``value``.
    """
    x = value - Fraction(101, 25)
    if x <= 0:
        return False
    y = x * x - 8 - Fraction(126, 625)
    return y > 0 and y * y > Fraction(144, 625) * 28


def green_bounds(digits: int = 30) -> tuple[Fraction, Fraction]:
    """Rational bounds on Green's value from integer square roots at ``digits`` places."""
    scale = 10**digits
    root2, root14 = isqrt(2 * scale * scale), isqrt(14 * scale * scale)
    low = Fraction(2 * root2, scale) + Fraction(101, 25) + Fraction(3 * root14, 25 * scale)
    high = low + Fraction(2, scale) + Fraction(3, 25 * scale)
    return low, high


def n50_net(core: Fraction) -> dict[str, str]:
    """The angle-net containment facts ``mixed_net_audit.net_certificate`` asserts."""
    end = N50_STEP * N50_LAST
    _require(0 < core < 1 and (1 + end) ** 2 >= 2, "net does not reach tan(pi/8)")
    _require((1 + (N50_LAST - Fraction(1, 2)) * N50_STEP) ** 2 < 2, "last node unassigned")
    bound = core * (1 + N50_STEP)
    _require(bound < 1, "core containment is not strict")
    return {
        "step": str(N50_STEP),
        "count": str(N50_LAST + 1),
        "endpoint_check": str((1 + end) ** 2 - 2),
        "rotated_side_upper": str(bound),
        "side_margin": str(1 - bound),
    }


def n50_centre_domains(side: Fraction, core: Fraction) -> dict[str, Any]:
    """How far the mixed checker's centre domain sits inside verify.cpp's, per net node.

    verify.cpp checks core centres in ``[L/2, L - a_core]`` with ``a_core = B(c+s)/2`` at
    the node. The mixed driver supplies ``E = L/2 - r`` instead, where ``r`` is the half
    axis extent of the containing unit square at the lower end of the node's bin, so it
    checks ``[L/2, L - r]``. Both are the quarter-turn reduction of the full domain.
    """
    widths: list[Fraction] = []
    for index in range(1, N50_LAST + 1):
        t = index * N50_STEP
        a = max(Fraction(0), t - N50_STEP / 2)
        radius = (1 + 2 * a - a * a) / (2 * (1 + a * a))
        core_radius = core * (1 + 2 * t - t * t) / (2 * (1 + t * t))
        _require(radius >= core_radius, f"unit-square radius below core radius at {index}")
        widths.append(radius - core_radius)
    return {
        "nodes": N50_LAST,
        "eliminated_width_min": str(min(widths)),
        "eliminated_width_min_float": float(min(widths)),
        "eliminated_width_max": str(max(widths)),
        "eliminated_width_max_float": float(max(widths)),
        "axis_domain": f"[{side / 2}, {side - Fraction(1, 2)}]^2",
    }


def _certificate_minimum(certificate: dict[str, Any]) -> tuple[float | None, str | None]:
    """The least per-angle lower bound the certificate records, if it records them."""
    records = certificate["results"]
    _require(len(records) == N50_LAST + 1, "certificate does not carry 201 records")
    lows = [
        (float(value), index)
        for index, record in records.items()
        if (value := record.get("lower", record.get("integer_minimum"))) is not None
    ]
    if not lows:
        return None, None
    _require(len(lows) == N50_LAST + 1, "some records carry no lower bound")
    return min(lows)


#: The source's own audit record for a rung, where it ships one.
N50_AUDITS = {"L740": "completion-audit.json", "L735": "final-audit.json"}


def _n50_source_audit(name: str, source: Path) -> dict[str, Any] | None:
    """Bind the source's audit record to the retained certificate and pinned tarball.

    Its Green upper bound must be a true upper bound (``exceeds_green``) and its
    improvement exactly ``L`` minus that bound.
    """
    if name not in N50_AUDITS:
        return None
    directory = N50[name]
    record = _json(directory / N50_AUDITS[name], source)
    side = N50_CLAIMS[name][0]
    upper = Fraction(record["green_upper"])
    certificate = _sha256(_read(directory / "certificate.json", source))
    tree = read_subtree_manifest()
    _require(record["certificate_sha256"] == certificate, "audit binds another certificate")
    _require(exceeds_green(upper), "the source's Green upper bound is not an upper bound")
    _require(Fraction(record["improvement_lower"]) == side - upper, "improvement differs")
    archive = record.get("archive_sha256")
    _require(
        archive is None or archive == tree[directory / N50_TARBALLS[name]],
        "audit binds another tarball",
    )
    return {
        "file": N50_AUDITS[name],
        "status": record["status"],
        "certificate_sha256_matches": True,
        "archive_sha256_checked": archive is not None,
        "green_upper_is_upper_bound": True,
        "improvement_lower_float": float(Fraction(record["improvement_lower"])),
    }


def n50_certificate(name: str, source: Path = SOURCE) -> dict[str, Any]:
    """Exact premises of one n50 rung; coverage is the source checker's."""
    side, count, digest = N50_CLAIMS[name]
    directory = N50[name]
    data = _json(directory / "candidate.json", source)
    manifest = _json(directory / "manifest.json", source)
    certificate = _json(directory / "certificate.json", source)
    candidate_side, core, items = _n50_measure(data)
    _require(candidate_side == side and core == Fraction(9977, 10000), "side or core differs")
    _require(len(items) == count, "rectangle count differs from the source's statement")
    for x0, y0, x1, y1, mass in items:
        _require(0 <= x0 < x1 <= side and 0 <= y0 < y1 <= side, "rectangle outside container")
        _require(mass >= 0, "negative mass")
    total = sum((item[4] for item in items), Fraction(0))
    _require(total == Fraction(data["total_mass"]) == N50_MASS, "total differs")
    _require(total < 50 and data["n"] == 50, "total is not below 50")
    _require(
        manifest["candidate_digest"] == certificate["candidate_digest"] == digest, "digest"
    )
    if "rectangles" in data:
        _require(_semantic_digest(data) == digest, "recomputed candidate digest differs")
        checker = N50["L740"] / "code/mixed_rotated_verify.cpp"
        _require(
            manifest["source_sha256"] == _sha256(_read(checker, source)) == N50_CHECKER_SHA256,
            "the manifest names another checker",
        )
    _require(exceeds_green(side), "side does not exceed Green's bound")
    low, high = green_bounds()
    minimum, at = _certificate_minimum(certificate)
    _require(minimum is None or minimum >= 1, "a recorded per-angle lower bound is below 1")
    audit_record = _n50_source_audit(name, source)
    return {
        "side": str(side),
        "side_float": float(side),
        "core": str(core),
        "rectangles": count,
        "total_mass": str(total),
        "budget_gap": str(50 - total),
        "candidate_digest": digest,
        "digest_recomputed": "rectangles" in data,
        "checker_sha256": manifest["source_sha256"],
        "exceeds_green": True,
        "excess_over_green_lower": str(side - high),
        "excess_over_green_lower_float": float(side - high),
        "green_interval_30_digits": [float(low), float(high)],
        "net": n50_net(core),
        "centre_domains": n50_centre_domains(side, core),
        "certificate_status": certificate["status"],
        "recorded_minimum_lower": minimum,
        "recorded_minimum_at": at,
        "source_audit": audit_record,
        "coverage_decided_here": False,
    }


def check_bundle_hashes(bundle: Path) -> dict[str, Any]:
    """Every entry of an n50 bundle's ``files-sha256.json`` against the unpacked files.

    Run it on a pristine unpacking: the shipped checker writes into ``proof/``.
    """
    listing = json.loads((bundle / "files-sha256.json").read_text())
    present = {
        str(path.relative_to(bundle)) for path in bundle.rglob("*") if path.is_file()
    } - {"files-sha256.json"}
    mismatched = sorted(
        name
        for name, digest in listing.items()
        if not (bundle / name).is_file() or _sha256((bundle / name).read_bytes()) != digest
    )
    unlisted = sorted(present - set(listing))
    return {
        "status": "BUNDLE_FILES_MATCH" if not mismatched and not unlisted else "DIFFERS",
        "listed": len(listing),
        "mismatched": mismatched[:20],
        "unlisted": unlisted[:20],
    }


def d4_images(side: Fraction, items: list[tuple[Any, ...]]) -> list[tuple[Fraction, ...]]:
    """Each rectangle's eight D4 images with density ``m/(8|R|)``, in the source's order.

    The order is the source's convention (``mixed_density_check.expand``); the values are
    computed here from the candidate.
    """
    images: list[tuple[Fraction, ...]] = []
    for x0, y0, x1, y1, mass in items:
        rho = mass / (8 * (x1 - x0) * (y1 - y0))
        for swap in (False, True):
            a, b, c, d = (y0, x0, y1, x1) if swap else (x0, y0, x1, y1)
            for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
                u, v = (a, c) if sx == 1 else (side - c, side - a)
                w, z = (b, d) if sy == 1 else (side - d, side - b)
                images.append((u, w, v, z, rho))
    return images


def encloses(text: str, exact: Fraction) -> bool:
    low, high = (Fraction(float.fromhex(token)) for token in text.split())
    return low <= exact <= high


def n50_inputs(bundle: Path) -> dict[str, Any]:
    """Bind all 200 oblique inputs of an n50 bundle to the exact candidate, independently.

    For each net index the input file must hash to the digest its ``result.json`` records,
    and every interval in it must enclose the exact rational recomputed here: the side, the
    core, ``E = L/2 - rho(a_r)``, the rotation ``c`` and ``s`` at ``t_r``, ``gamma = 1``
    exactly, and every coordinate and density of the D4-expanded rectangles. No source code
    is imported.
    """
    tree = read_subtree_manifest()
    return check_inputs(
        bundle / "proof", tree[N50["L740"] / "candidate.json"], range(1, N50_LAST + 1)
    )


def check_inputs(root: Path, candidate_sha256: str, indices: Iterable[int]) -> dict[str, Any]:
    """`n50_inputs` for any mixed bundle's ``proof/`` and any oblique net indices."""
    candidate = (root / "candidate.json").read_bytes()
    _require(_sha256(candidate) == candidate_sha256, "bundle candidate differs")
    side, core, items = _n50_measure(json.loads(candidate))
    images = d4_images(side, items)
    checked = 0
    for index in indices:
        _require(1 <= index <= N50_LAST, f"not an oblique net index: {index}")
        folder = root / f"net{index:03}"
        raw = (folder / "input.txt").read_bytes()
        spec = json.loads((folder / "result.json").read_text())["manifest"]
        _require(_sha256(raw) == spec["input_sha256"], f"input {index} is not the recorded one")
        t = index * N50_STEP
        a = max(Fraction(0), t - N50_STEP / 2)
        radius = (1 + 2 * a - a * a) / (2 * (1 + a * a))
        header = (
            side,
            core,
            side / 2 - radius,
            (1 - t * t) / (1 + t * t),
            2 * t / (1 + t * t),
            Fraction(1),
        )
        lines = raw.decode("ascii").splitlines()
        _require(len(lines) == 6 + 1 + len(images) + 1, f"input {index} line count")
        for line, exact in zip(lines[:6], header, strict=True):
            _require(encloses(line, exact), f"input {index} header does not enclose {exact}")
        _require(lines[5].split()[0] == lines[5].split()[1], "gamma is not a point interval")
        _require(Fraction(float.fromhex(lines[5].split()[0])) == 1, "gamma is not one")
        _require(int(lines[6]) == len(images) and int(lines[-1]) == 0, f"input {index} counts")
        for line, image in zip(lines[7:-1], images, strict=True):
            tokens = line.split()
            _require(len(tokens) == 10, f"input {index} rectangle line")
            for k, exact in enumerate(image):
                _require(
                    encloses(" ".join(tokens[2 * k : 2 * k + 2]), exact),
                    f"input {index} interval does not enclose its datum",
                )
        _require(
            spec["E"] == str(side / 2 - radius) and Fraction(spec["t"]) == t,
            f"angle {index} specification differs",
        )
        checked += 1
    return {
        "status": "ALL_INPUTS_ENCLOSE_THE_CANDIDATE",
        "inputs": checked,
        "rectangle_images": len(images),
        "gamma": "1",
        "scope": (
            "Each oblique input hashes to its recorded digest and every interval encloses "
            "the exact datum recomputed from the candidate; coverage is not decided here."
        ),
    }


def n50_compare(bundle: Path) -> dict[str, Any]:
    """Compare a complete run of the shipped L740 driver with the retained certificate.

    The run rewrites ``proof/certificate.json`` with ``results`` in completion order, so it
    is compared field by field; ``replay-progress.json`` and ``replay-verify``, which the
    shipped bundle lacks, show that the run happened. Every per-angle ``replayed.json``
    must carry the node count and lower bound of the shipped ``result.json``.
    """
    return compare_driver_run(bundle, json.loads(_read(N50["L740"] / "certificate.json")))


def compare_driver_run(bundle: Path, shipped: dict[str, Any]) -> dict[str, Any]:
    """`n50_compare` for any mixed bundle, against that certificate's retained record."""
    root = bundle / "proof"
    progress = json.loads((root / "replay-progress.json").read_text())
    _require((root / "replay-verify").is_file(), "no replay binary: the driver did not run")
    fresh = json.loads((root / "certificate.json").read_text())
    differing = sorted(
        key for key in set(fresh) | set(shipped) if fresh.get(key) != shipped.get(key)
    )
    angles_ok = 0
    for index in range(1, N50_LAST + 1):
        folder = root / f"net{index:03}"
        replayed = json.loads((folder / "replayed.json").read_text())
        saved = json.loads((folder / "result.json").read_text())
        if (
            replayed["status"] == "ANGLE_RESULT_REPLAYED"
            and replayed["nodes"] == saved["nodes"]
            and replayed["lower"] == saved["lower"]
        ):
            angles_ok += 1
    axis = json.loads((root / "axis" / "replayed.json").read_text())
    axis_ok = axis == shipped["results"]["0"]
    complete = (
        fresh.get("status") == "ALL_ANGLES_VERIFIED_AND_REPLAYED"
        and progress == {"done": N50_LAST + 1, "total": N50_LAST + 1}
        and not differing
        and angles_ok == N50_LAST
        and axis_ok
    )
    return {
        "status": "FULL_REPLAY_MATCHES_SHIPPED" if complete else "DIFFERS",
        "fresh_status": fresh.get("status"),
        "progress": progress,
        "differing_fields": differing,
        "oblique_angles_matching": angles_ok,
        "axis_matches": axis_ok,
        "certificate_sha256": _sha256((root / "certificate.json").read_bytes()),
    }


def _n50_angle(job: tuple[str, str, str, str]) -> dict[str, Any]:
    """Re-execute one oblique angle with the source's own replay function (worker)."""
    code, folder, binary, candidate = job
    if code not in sys.path:
        sys.path.insert(0, code)
    replay = importlib.import_module("verify_rotated_result").replay
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    start = time.monotonic()
    report = cast(dict[str, Any], replay(Path(folder), Path(binary), Path(candidate)))
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    return report | {
        "wall_seconds": time.monotonic() - start,
        "cpu_seconds": (after.ru_utime - before.ru_utime) + (after.ru_stime - before.ru_stime),
    }


def survey_n50_bundle(root: Path, count: int) -> dict[str, Any]:
    """What every recorded angle of a bundle's ``proof/`` says, without re-running any."""
    records = [
        json.loads((root / f"net{index:03}" / "result.json").read_text())
        for index in range(1, count)
    ]
    axis = json.loads((root / "axis" / "result.json").read_text())
    return {
        "oblique_records": len(records),
        "gammas": sorted({record["manifest"]["gamma"] for record in records} | {axis["gamma"]}),
        "statuses": sorted({record["status"] for record in records}),
        "axis_status": axis["status"],
        "frontier_boxes": sum(len(record["frontier"]) for record in records),
        "nodes": sum(record["nodes"] for record in records),
        "least_lower": min(record["lower"] for record in records),
        "upstream_oblique_seconds": sum(record["seconds"] for record in records),
        "upstream_axis_seconds": axis["seconds"],
    }


#: The modules of the shipped code that a replay imports; dropped from the cache first, so
#: one process never runs one bundle's checks with another bundle's modules.
SHIPPED_MODULES = (
    "endpoint_cells",
    "mixed_axis_cells",
    "mixed_density_check",
    "mixed_net_audit",
    "mixed_rotated_verify",
    "score",
    "verify_axis_certificate",
    "verify_mixed_full_proof",
    "verify_rotated_result",
)


@dataclass(frozen=True, slots=True)
class DriverPreconditions:
    """What ``verify_mixed_full_proof.verify`` establishes before it checks any angle."""

    root: Path
    code: str
    model: Any
    count: int
    domains: Any
    rotated: Any
    axis: Any

    def facts(self) -> dict[str, Any]:
        return {
            "status": "DRIVER_PRECONDITIONS_HOLD",
            "candidate_digest": self.model[-1],
            "angles": self.count,
            "total_mass": str(self.model[-2]),
            "checker_sha256": _sha256(Path(self.rotated.SOURCE).read_bytes()),
        }


def driver_preconditions(bundle: Path) -> DriverPreconditions:
    """Repeat the shipped full-proof driver's assertions, in its order, on its own code.

    The driver has no subset mode, so a partial or split replay calls the same per-angle
    functions after this: the candidate's D4 symmetry, the net and its centre domains,
    the summary and manifest, and the checker source against ``proof/verify.cpp`` and the
    manifest's digest. Nothing of the source is modified.
    """
    root = (bundle / "proof").resolve()
    code = str((bundle / "code").resolve())
    for name in SHIPPED_MODULES:
        sys.modules.pop(name, None)
    if code in sys.path:
        sys.path.remove(code)
    sys.path.insert(0, code)
    density = importlib.import_module("mixed_density_check")
    net_audit = importlib.import_module("mixed_net_audit")
    rotated = importlib.import_module("mixed_rotated_verify")
    axis_module = importlib.import_module("verify_axis_certificate")
    _require(
        Path(rotated.SOURCE).resolve().parent == Path(code),
        "the imported checker is not the bundle's own",
    )
    summary = json.loads((root / "summary.json").read_text())
    data = json.loads((root / "candidate.json").read_text())
    model = density.expand(data)
    net_audit.symmetry(model)
    step, last = net_audit.candidate_net(data)
    count = last + 1
    net = net_audit.net_certificate(model[1], step, last)
    domains = net_audit.centre_domains(model[0], model[1], step, last)
    manifest = json.loads((root / "manifest.json").read_text())
    source_bytes = Path(rotated.SOURCE).read_bytes()
    _require(summary["verified_angles"] == count == summary["complete_angles"], "summary")
    _require(manifest["net"] == net, "manifest net differs")
    _require(set(map(int, summary["records"])) == set(range(count)), "summary records")
    _require(summary["candidate_digest"] == manifest["candidate_digest"] == model[-1], "digest")
    _require((root / "verify.cpp").read_bytes() == source_bytes, "verify.cpp differs")
    _require(_sha256(source_bytes) == manifest["source_sha256"], "checker source digest")
    return DriverPreconditions(root, code, model, count, domains, rotated, axis_module)


def check_angle_record(root: Path, index: int, digest: str, domains: Any) -> dict[str, Any]:
    """The driver's assertions on one oblique angle's shipped record, before its replay."""
    saved = json.loads((root / f"net{index:03}" / "result.json").read_text())
    spec = saved["manifest"]
    _require(saved["status"] == "ANGLE_VERIFIED" and saved["frontier"] == [], "status")
    _require(
        spec["candidate_digest"] == digest
        and spec["net_index"] == index
        and spec["domain"] == domains[index]
        and Fraction(spec["gamma"]) >= 1,
        f"angle {index} specification",
    )
    return saved


def n50_replay(bundle: Path, indices: list[int], workers: int) -> dict[str, Any]:
    """Run the preconditions of ``verify_mixed_full_proof.verify`` and a chosen angle set.

    The shipped driver has no subset mode, so this repeats its assertions in order and
    then calls the same per-angle functions: ``verify_axis_certificate.replay`` for index
    0 and ``verify_rotated_result.replay`` for each oblique index, with the source's C++
    compiled by the source's ``compile_verifier``. Nothing of the source is modified.
    """
    driver = driver_preconditions(bundle)
    root, code, model, count, domains = (
        driver.root,
        driver.code,
        driver.model,
        driver.count,
        driver.domains,
    )
    rotated, axis_module = driver.rotated, driver.axis
    certificate = json.loads((root / "certificate.json").read_text())
    started = time.monotonic()
    rows: list[dict[str, Any]] = []
    if 0 in indices:
        before = resource.getrusage(resource.RUSAGE_SELF)
        start = time.monotonic()
        axis = axis_module.replay(root / "axis", root / "candidate.json")
        after = resource.getrusage(resource.RUSAGE_SELF)
        _require(axis["digest"] == model[-1] and Fraction(axis["gamma"]) >= 1, "axis replay")
        rows.append(
            {
                "index": 0,
                "status": axis["status"],
                "cells": axis["cells"],
                "integer_minimum": axis["integer_minimum"],
                "upstream": certificate["results"]["0"],
                "matches_upstream": axis == certificate["results"]["0"],
                "wall_seconds": time.monotonic() - start,
                "cpu_seconds": (after.ru_utime - before.ru_utime)
                + (after.ru_stime - before.ru_stime),
            }
        )
    oblique = sorted(index for index in set(indices) if index != 0)
    binary = root / "replay-verify"
    rotated.compile_verifier(binary)
    jobs: list[tuple[str, str, str, str]] = []
    for index in oblique:
        _require(1 <= index < count, f"index outside the net: {index}")
        folder = root / f"net{index:03}"
        check_angle_record(root, index, model[-1], domains)
        jobs.append((code, str(folder), str(binary), str(root / "candidate.json")))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for index, report in zip(oblique, pool.map(_n50_angle, jobs), strict=True):
            saved = json.loads((root / f"net{index:03}" / "result.json").read_text())
            rows.append(
                {
                    "index": index,
                    "status": report["status"],
                    "nodes": report["nodes"],
                    "lower": report["lower"],
                    "upstream_nodes": saved["nodes"],
                    "upstream_lower": saved["lower"],
                    "upstream_seconds": saved["seconds"],
                    "matches_upstream": report["nodes"] == saved["nodes"]
                    and report["lower"] == saved["lower"],
                    "wall_seconds": report["wall_seconds"],
                    "cpu_seconds": report["cpu_seconds"],
                }
            )
    survey = survey_n50_bundle(root, count)
    upstream_total = survey["upstream_oblique_seconds"]
    sampled_upstream = sum(row.get("upstream_seconds", 0.0) for row in rows)
    sampled_cpu = sum(row["cpu_seconds"] for row in rows if row["index"] != 0)
    ratio = sampled_cpu / sampled_upstream if sampled_upstream else None
    return {
        "status": "SAMPLE_REPLAYED" if all(r["matches_upstream"] for r in rows) else "DIFFERS",
        "candidate_digest": model[-1],
        "indices": sorted(set(indices)),
        "rows": sorted(rows, key=lambda row: row["index"]),
        "wall_seconds": time.monotonic() - started,
        "bundle_records": survey,
        "upstream_oblique_seconds_total": upstream_total,
        "sample_cpu_over_upstream_seconds": ratio,
        "estimated_full_oblique_cpu_hours": (upstream_total * ratio / 3600) if ratio else None,
        "scope": (
            "The source's per-angle replay functions and unchanged C++ checker on the "
            "listed indices, after the full driver's preconditions; not a complete replay."
        ),
    }


# --------------------------------------------------------------------------- mixed, any n

WEB = REPO / "packing/resources/web"
#: The code every mixed certificate ships, byte for byte; this packet retains it once.
MIXED_CODE = SOURCE / N50["L740"] / "code"
MIXED_REQUIREMENTS = SOURCE / N50["L740"] / "requirements.txt"
MIXED_CORE = Fraction(9977, 10000)
#: Each mixed measure's total is ``n`` less this.
MIXED_GAP = Fraction(1, 100000)
#: The source's own audit of a certificate, which binds its certificate and tarball digests.
SOURCE_AUDIT = "completion-audit.json"
#: The small files of a certificate directory that a packet retains and the audit reads.
MIXED_FILES = (
    "candidate.json",
    "certificate.json",
    "manifest.json",
    SOURCE_AUDIT,
    "README.md",
)
AXIS_REPLAYED = "AXIS_CERTIFICATE_REPLAYED"
ANGLE_REPLAYED = "ANGLE_RESULT_REPLAYED"
MAX_REPLAY_WORKERS = 4


@dataclass(frozen=True, slots=True)
class MixedCertificate:
    """One ``certificates/mixed_n*`` directory of the source, as the source states it.

    ``side``, ``rectangles`` and ``candidate_digest`` are the source's statements, which
    the audit holds the retained bytes to. The tarball's digest and size are read from the
    packet's acquisition files and never written here, so the pin has one home.
    ``source_audit`` says whether the directory at the pinned revision carries the source's
    ``completion-audit.json``; it follows from the revision (`WITHOUT_SOURCE_AUDIT`), never
    from whether the file is found.
    """

    name: str
    packet: Path
    revision: str
    directory: Path
    n: int
    side: Fraction
    rectangles: int
    candidate_digest: str
    tarball: str
    source_audit: bool

    @property
    def files(self) -> tuple[str, ...]:
        """The small files the packet retains for this certificate and the audit reads."""
        if self.source_audit:
            return MIXED_FILES
        return tuple(name for name in MIXED_FILES if name != SOURCE_AUDIT)

    @property
    def source(self) -> Path:
        return self.packet / "square-packing-bounds"

    @property
    def subtree(self) -> Path:
        return self.packet / "acquisition/upstream-subtree.sha256"

    @property
    def record(self) -> Path:
        return self.packet / "acquisition/sources.json"

    @property
    def upstream_tarball(self) -> Path:
        return self.directory / self.tarball

    @property
    def bundle(self) -> str:
        return self.tarball.removesuffix(".tar.gz")

    @property
    def url(self) -> str:
        return f"{SOURCE_URL}/raw/{self.revision}/{self.upstream_tarball.as_posix()}"

    @property
    def urls(self) -> tuple[str, str]:
        """The raw-file address, then the address it redirects to, which some proxies allow
        when they refuse the first."""
        host = SOURCE_URL.replace("https://github.com/", "https://raw.githubusercontent.com/")
        return self.url, f"{host}/{self.revision}/{self.upstream_tarball.as_posix()}"

    @property
    def receipts(self) -> Path:
        return self.packet / "receipts" / self.name


F_REVISION = "1a25a5ed745fdd905a52f48fcc48150a0669032d"
G_REVISION = "52af997dc91c579658f0828bc8304e306ad9d95b"
F_PACKET = WEB / "wand125-point-and-mixed-2026-10-01"
G_PACKET = WEB / "wand125-mixed-bounds-2026-10-02"
H_REVISION = "7975030a192607ef27edd1559aee4e98bd93047b"
H_PACKET = WEB / "wand125-mixed-bounds-n76-2026-10-02"
I_REVISION = "b00fc70f1904e9b1b567afee056d347f911209e8"
I_PACKET = WEB / "wand125-mixed-bounds-afternoon-2026-10-02"
J_REVISION = "2aff2076c492d62340e986c84f60a0a29eb668df"
J_PACKET = WEB / "wand125-mixed-bounds-2026-10-03"
K_REVISION = "8aa6a10b3b8f165d39c85b68982fed1de086516c"
K_PACKET = WEB / "wand125-mixed-bounds-2026-10-04"
L_REVISION = "797bdf6e10eba5f9dccca9da06f8352e81ba9dde"
L_PACKET = WEB / "wand125-mixed-bounds-evening-2026-10-04"
M_REVISION = "a541afbe7826ff75f6d3848e10279fd524d55af3"
M_PACKET = WEB / "wand125-mixed-bounds-2026-10-05"
N_REVISION = "43050edc5bdf5116fc5a073283128edd6749946b"
N_PACKET = WEB / "wand125-mixed-bounds-finer-net-2026-10-05"

#: The pinned revisions whose certificate directories carry no ``completion-audit.json``:
#: the source removed it from every directory of 3 October onward at ``150939e`` and
#: published none after. A certificate pinned at one is bound to its bundle by the
#: tarball's digest at the pinned tree, which `devtools.acquire_source` bound to the
#: tarball's Git blob at the pinned commit, by the size the acquisition record pins, and by
#: the digest its README states; every other row still needs the source's audit.
WITHOUT_SOURCE_AUDIT = frozenset({K_REVISION, L_REVISION, M_REVISION, N_REVISION})


#: Every mixed certificate this tool audits and replays: n = 50 (T-048), the five of
#: jlevy/squares#282 (T-069), the two of its comment of 2 October, the n = 76 of its
#: later comment the same day (pinned at ``7975030``, its own packet), the six the
#: source added that afternoon (UTC), pinned together at ``b00fc70``, the 22 it added
#: on 3 October, pinned together at ``2aff207``, the 16 it added from 3 October
#: 19:33 UTC to 4 October 07:17 UTC, pinned together at ``8aa6a10``, the 12 it added
#: from 4 October 07:51 UTC to 19:03 UTC, pinned together at ``797bdf6``, the two it
#: added on 5 October at 06:06 and 06:07 UTC, pinned together at ``a541afb``, and the
#: n = 66 it added later that morning at ``d73ce20``, pinned at ``43050ed``. Each row is the
#: packet, the pinned revision, n, the side as the directory names it, the side, the
#: rectangle count and the candidate digest, as the source states them.
_MIXED_ROWS: tuple[tuple[Path, str, int, str, Fraction, int, str], ...] = (
    (PACKET, REVISION, 50, "7.40", Fraction(37, 5), 553, N50_CLAIMS["L740"][2]),
    (
        F_PACKET,
        F_REVISION,
        37,
        "6.44",
        Fraction(161, 25),
        350,
        "6f854ead4bf928a491768f56590ef92a2b3c14fa345a9bb7edbd23e421e99fe1",
    ),
    (
        F_PACKET,
        F_REVISION,
        65,
        "8.35",
        Fraction(167, 20),
        787,
        "cc10ef9189731abaea77cf96b68b0a44743bb13d5b252d4559b6b65e5085beb6",
    ),
    (
        F_PACKET,
        F_REVISION,
        66,
        "8.42",
        Fraction(421, 50),
        631,
        "eb86256982300d42ada314676302394b433822b1673fafe8e3c53b3a4499a3e6",
    ),
    (
        F_PACKET,
        F_REVISION,
        90,
        "9.60",
        Fraction(48, 5),
        762,
        "99f1c45db199a0012da0617afc619857df108625c0f9263eef196df6ce2c7884",
    ),
    (
        F_PACKET,
        F_REVISION,
        92,
        "9.69",
        Fraction(969, 100),
        832,
        "2b2624e8d6ebdd620cb13c728634872a8a7d7c4b10313568af824750e7138eb0",
    ),
    (
        G_PACKET,
        G_REVISION,
        84,
        "9.40",
        Fraction(47, 5),
        661,
        "58dabcb47821d0113b20b33d904cd3f0e9b3d3f49e3c043d4e23d009d655f41c",
    ),
    (
        G_PACKET,
        G_REVISION,
        85,
        "9.42",
        Fraction(471, 50),
        587,
        "b95a0bb41a77cb00d8716c5256ae5bea71f1c668ce44047671e41e7f3f909a4c",
    ),
    (
        H_PACKET,
        H_REVISION,
        76,
        "8.94",
        Fraction(447, 50),
        317,
        "f2c2530552547a56a454c55bee99a196221ae1f4357570c3a0d524eddd5d9cdf",
    ),
    (
        I_PACKET,
        I_REVISION,
        83,
        "9.37",
        Fraction(937, 100),
        728,
        "a76336032928972d66d644c335cdfa62809ab2fef213474c86c36fd81ea7733a",
    ),
    (
        I_PACKET,
        I_REVISION,
        85,
        "9.46",
        Fraction(473, 50),
        525,
        "d99031dfded8ab07e5cec0520f8d9b04c9f983cf846e29c17382803d970aca94",
    ),
    (
        I_PACKET,
        I_REVISION,
        87,
        "9.48",
        Fraction(237, 25),
        299,
        "6b720d7b963bb104b45c5ad543a35c8fad4e1b70fd137969890d7645dd9179d4",
    ),
    (
        I_PACKET,
        I_REVISION,
        91,
        "9.70",
        Fraction(97, 10),
        288,
        "6745b3740e0fbd9d1be94770868829c0c76d8081b472d47d59a8a779f60d6564",
    ),
    (
        I_PACKET,
        I_REVISION,
        92,
        "9.75",
        Fraction(39, 4),
        324,
        "458d60ad8485c0e9aeabdfeefc21e93249e47666cbb60357465aa35d7e2e524c",
    ),
    (
        I_PACKET,
        I_REVISION,
        96,
        "9.96",
        Fraction(249, 25),
        279,
        "a0cbba40370f94a0125f323c839c75dcb5b6145c32b1b81e80665fb75f27d561",
    ),
    (
        J_PACKET,
        J_REVISION,
        51,
        "7.46",
        Fraction(373, 50),
        446,
        "503278fd59bd1f04d7563a77cb16d80aec47df36e1a9b79e329c6cbd97334872",
    ),
    (
        J_PACKET,
        J_REVISION,
        52,
        "7.55",
        Fraction(151, 20),
        455,
        "bc1ec3a1934ae09852d588da55b6a11183287000246c2522b2cdbbc72ded684d",
    ),
    (
        J_PACKET,
        J_REVISION,
        55,
        "7.728",
        Fraction(966, 125),
        303,
        "6131cd0a67d3499df1ca62abe1088a1b9d3bc5961b69656fb0f0cedb72a6e605",
    ),
    (
        J_PACKET,
        J_REVISION,
        58,
        "7.905",
        Fraction(1581, 200),
        319,
        "96727aa1681161ab21e0a9677739fd32badc0ddd8933f8c7daf1d6192ba14754",
    ),
    (
        J_PACKET,
        J_REVISION,
        69,
        "8.612",
        Fraction(2153, 250),
        556,
        "9965c638aa6dadaeb5fd08eadd905529c175116ff6c3d1d87447d947f20d1a1e",
    ),
    (
        J_PACKET,
        J_REVISION,
        70,
        "8.6475",
        Fraction(3459, 400),
        495,
        "41af9ea74a3bf12d1971832120fdba2526b899b789068ef706475f38c8312ab2",
    ),
    (
        J_PACKET,
        J_REVISION,
        71,
        "8.705",
        Fraction(1741, 200),
        471,
        "8d8f26610731ec3e553f20d46687339937967b057f4dff725bd4456addabaefa",
    ),
    (
        J_PACKET,
        J_REVISION,
        73,
        "8.809",
        Fraction(8809, 1000),
        450,
        "5684ebfd1f061a11ab9ae84c3568d22586a0acc3df1192df3dd08e2af38144f9",
    ),
    (
        J_PACKET,
        J_REVISION,
        74,
        "8.8675",
        Fraction(3547, 400),
        505,
        "d9b1c057c7e9337e041e96f662aa5c7b63de4124624aa69b70308487e8841d48",
    ),
    (
        J_PACKET,
        J_REVISION,
        75,
        "8.92",
        Fraction(223, 25),
        340,
        "cea59cc4cde834867b66a5c5b64d0affd9718172cee53ae92557c2874fed984e",
    ),
    (
        J_PACKET,
        J_REVISION,
        76,
        "8.96",
        Fraction(224, 25),
        341,
        "c990078499a592dccb6336f69b956077046ca1fde498577f511c8c43f2c78a40",
    ),
    (
        J_PACKET,
        J_REVISION,
        86,
        "9.50",
        Fraction(19, 2),
        509,
        "a042af995541097298a2c6b44970d072a1b7eb7bcbcc41d0e4d8965c3dcb82fa",
    ),
    (
        J_PACKET,
        J_REVISION,
        87,
        "9.55",
        Fraction(191, 20),
        509,
        "f1e27ede3e2b29a87f4da9493d17a2258334a28c01b81ecffd157d2b0eda6b76",
    ),
    (
        J_PACKET,
        J_REVISION,
        88,
        "9.60",
        Fraction(48, 5),
        443,
        "7a0f3594ce03191207646bcc2db5af878c5bbc390641625b7e0837d0d2ebb9ab",
    ),
    (
        J_PACKET,
        J_REVISION,
        89,
        "9.65",
        Fraction(193, 20),
        416,
        "fff74c43cbd5fe435f70b45b157b4d5da9fbd7bb17a11202bad37dab1a42aa77",
    ),
    (
        J_PACKET,
        J_REVISION,
        90,
        "9.725",
        Fraction(389, 40),
        571,
        "a251cc29c19c2a27b3458e2dac67aad8190050317d9f19c7f47099a45b924bd8",
    ),
    (
        J_PACKET,
        J_REVISION,
        91,
        "9.75",
        Fraction(39, 4),
        457,
        "c4c175eb7af4a7964758e89dc33d91bd3e375b35765b6511f4b33c8d8d28ff9d",
    ),
    (
        J_PACKET,
        J_REVISION,
        92,
        "9.77",
        Fraction(977, 100),
        345,
        "d1aafdd22771b24ada660b6f741044a6564a7921aaae95bb8bf5cb8d59bbb4d9",
    ),
    (
        J_PACKET,
        J_REVISION,
        93,
        "9.86",
        Fraction(493, 50),
        443,
        "dd3da64f729a011c79c9e570d53a4986bba80572d1cf42c15fc4b14d3cd0a858",
    ),
    (
        J_PACKET,
        J_REVISION,
        94,
        "9.92",
        Fraction(248, 25),
        488,
        "f974716d36c4a841610e80585b8d4d8ef5c62080a75d7bd770afbfd37f359ff9",
    ),
    (
        J_PACKET,
        J_REVISION,
        95,
        "9.96",
        Fraction(249, 25),
        438,
        "9e3220d8e292b7aa693cadf50b24c998f8a9d348c23afca9bb38e16d359a866e",
    ),
    (
        J_PACKET,
        J_REVISION,
        96,
        "9.97",
        Fraction(997, 100),
        376,
        "5e89a1ae869f6f4a12b2fadfffd7996048e856c1ec5206939fbb8ff9d6cf5b69",
    ),
    (
        K_PACKET,
        K_REVISION,
        42,
        "6.8475",
        Fraction(2739, 400),
        431,
        "9e7eb014afc29e5a35f274a79aeb952acd3669bb5bffb461969d32633a08518d",
    ),
    (
        K_PACKET,
        K_REVISION,
        43,
        "6.9075",
        Fraction(2763, 400),
        358,
        "a1e40a0d8c9c5432c8d9221a1ee1ca915be51ea520112d693632600fd6a712e8",
    ),
    (
        K_PACKET,
        K_REVISION,
        44,
        "6.9725",
        Fraction(2789, 400),
        399,
        "09ee7101528876199acef723b2c45f87fe2c302cc2685a80088a098dbce2d49e",
    ),
    (
        K_PACKET,
        K_REVISION,
        51,
        "7.47",
        Fraction(747, 100),
        489,
        "b3838f4074a9fbe378b8530aff07083b244f2859ca3178ae0d039502da9600f7",
    ),
    (
        K_PACKET,
        K_REVISION,
        56,
        "7.8025",
        Fraction(3121, 400),
        453,
        "1126c353faeedab0905af5ffd066b0b1c888b0cbc8bd0af56aebb13ff889f07c",
    ),
    (
        K_PACKET,
        K_REVISION,
        57,
        "7.8725",
        Fraction(3149, 400),
        532,
        "8010142da5aa69b4c7aa3e0a1e23cba296a80626e50369a61118377df7ae83a6",
    ),
    (
        K_PACKET,
        K_REVISION,
        67,
        "8.475",
        Fraction(339, 40),
        485,
        "83415f601f5b3a23cac24106bffdc4bedb617cffa1dee2cbfc08fe63c33c0bbb",
    ),
    (
        K_PACKET,
        K_REVISION,
        69,
        "8.62",
        Fraction(431, 50),
        547,
        "bf02d53b084e32bd585c15aab3e4c8348867ef7f4804e247ce8cb740cf34ad9e",
    ),
    (
        K_PACKET,
        K_REVISION,
        72,
        "8.76",
        Fraction(219, 25),
        488,
        "89c68b03423d9f63f6cb0eb18f39de484cbeff028e89ad504d16cf01157823d9",
    ),
    (
        K_PACKET,
        K_REVISION,
        75,
        "8.94",
        Fraction(447, 50),
        589,
        "0c068ef9b264c9e22096342e1aa6f010bce70689e881f3d46e527298e82ede07",
    ),
    (
        K_PACKET,
        K_REVISION,
        84,
        "9.4075",
        Fraction(3763, 400),
        569,
        "d2b4a5da8e1424f7588bcffd581da1bb298aa62f3b2c40e6ec95cec0bdf09db2",
    ),
    (
        K_PACKET,
        K_REVISION,
        86,
        "9.503",
        Fraction(9503, 1000),
        533,
        "e0341c92ef882933dcb47a42f3cca61eaaca3ccd7478cb55bd0a2dcae8006e25",
    ),
    (
        K_PACKET,
        K_REVISION,
        88,
        "9.6125",
        Fraction(769, 80),
        502,
        "b86e90170ae237a25e57940f877f8ffa0451ecdb93b92f06ee73e386364246c5",
    ),
    (
        K_PACKET,
        K_REVISION,
        93,
        "9.88",
        Fraction(247, 25),
        501,
        "3f241cbb719b90c99b956293bfd81cfd303c8496b7ffa022d04691943c3c9e8d",
    ),
    (
        K_PACKET,
        K_REVISION,
        94,
        "9.94",
        Fraction(497, 50),
        630,
        "bf8dd4a2909d41f7dc74508cdf85abe563b2e761f7611e7b38c3b9b0636484c5",
    ),
    (
        K_PACKET,
        K_REVISION,
        95,
        "9.965",
        Fraction(1993, 200),
        480,
        "c41da14c19784c764d14e50e8bb6cbb6c845193420ca8ef2b7f407c397d9975f",
    ),
    (
        L_PACKET,
        L_REVISION,
        53,
        "7.6275",
        Fraction(3051, 400),
        505,
        "796fcf86fa805b3d7c746aac1dd60f83b25bb0bcbee2ec3b3caf7f5f2532bd5a",
    ),
    (
        L_PACKET,
        L_REVISION,
        54,
        "7.685",
        Fraction(1537, 200),
        364,
        "50b804a1cd90fd4b2195457a9e2bb573993057df4b0f444eb2ce57f237ef0711",
    ),
    (
        L_PACKET,
        L_REVISION,
        58,
        "7.935",
        Fraction(1587, 200),
        543,
        "4c217e1c2ac9501de1375a6af9e598defafd2175066166a0b98adf96f0203014",
    ),
    (
        L_PACKET,
        L_REVISION,
        70,
        "8.6575",
        Fraction(3463, 400),
        513,
        "b3205458ad9527c78d82da762cad749f029d62f43e0c33412ef3c201ba589186",
    ),
    (
        L_PACKET,
        L_REVISION,
        71,
        "8.721",
        Fraction(8721, 1000),
        529,
        "d971e25537ee0208f8765bf049803e9d90554fc380bea468eb967279c814e3e2",
    ),
    (
        L_PACKET,
        L_REVISION,
        73,
        "8.813",
        Fraction(8813, 1000),
        462,
        "d3bf25e43d9462b93103415e8e30d0fe58893ed1bb0254afa03a2ada3d7fcb8a",
    ),
    (
        L_PACKET,
        L_REVISION,
        76,
        "8.965",
        Fraction(1793, 200),
        312,
        "8ffc457439cc2c7135ae4067e49f0cdafe9bdf810fa798ddf35d4fed4c8bf35f",
    ),
    (
        L_PACKET,
        L_REVISION,
        87,
        "9.58",
        Fraction(479, 50),
        594,
        "f239f41ce512a6649c147553e820ffcd5319a1a8387b0b690f9e51cb9f3da929",
    ),
    (
        L_PACKET,
        L_REVISION,
        88,
        "9.62",
        Fraction(481, 50),
        562,
        "28d92dc904d52d1451275d5e9b1634619762df47156bafdb300728635b33ac4f",
    ),
    (
        L_PACKET,
        L_REVISION,
        90,
        "9.73",
        Fraction(973, 100),
        525,
        "7f1e3e26371b4041672241971c2dc6e77f5024563c74080c8720d6b9af0ed158",
    ),
    (
        L_PACKET,
        L_REVISION,
        91,
        "9.7625",
        Fraction(781, 80),
        438,
        "7e22dda8bb3296f402b8165868a17f36906e60338cc57d72ed2ed57b06b778a6",
    ),
    (
        L_PACKET,
        L_REVISION,
        94,
        "9.95",
        Fraction(199, 20),
        853,
        "85213e6c8d6ade1e6be86648f569c5b931b08b2d19b39308ce1cd2b578acc185",
    ),
    (
        M_PACKET,
        M_REVISION,
        67,
        "8.48",
        Fraction(212, 25),
        536,
        "7ff5efc88ae68a17f96b0b608114a827ee90c9a3eb994d5492beab449b6f0727",
    ),
    (
        M_PACKET,
        M_REVISION,
        84,
        "9.411",
        Fraction(9411, 1000),
        686,
        "d497f375a3f84615aa5963c1fd306815d9870736fbc7e2f305cbaa187ba47e47",
    ),
    (
        N_PACKET,
        N_REVISION,
        66,
        "8.43",
        Fraction(843, 100),
        713,
        "24cdd5b6dbc67ce5c284ed8957f1a7b69af3627ca65d53401b4d103e0a4dd411",
    ),
)


def _mixed_table() -> dict[str, MixedCertificate]:
    """`_MIXED_ROWS` by name: ``n85``, or ``n85-L946`` for a later side at a named count."""
    table: dict[str, MixedCertificate] = {}
    for packet, revision, n, label, side, count, digest in _MIXED_ROWS:
        digits = label.replace(".", "")
        name = f"n{n}" if f"n{n}" not in table else f"n{n}-L{digits}"
        table[name] = MixedCertificate(
            name=name,
            packet=packet,
            revision=revision,
            directory=Path(f"certificates/mixed_n{n}_L{digits}"),
            n=n,
            side=side,
            rectangles=count,
            candidate_digest=digest,
            tarball=f"n{n}-L{label}-proof-bundle.tar.gz",
            source_audit=revision not in WITHOUT_SOURCE_AUDIT,
        )
    return table


MIXED: dict[str, MixedCertificate] = _mixed_table()


def _files_in(directory: Path) -> list[Path]:
    return sorted(path for path in directory.iterdir() if path.is_file())


def mixed_retained(certificate: MixedCertificate) -> dict[str, bytes]:
    """The retained small files of one certificate directory, decompressed."""
    return {
        name: read_retained_bytes(certificate.source / certificate.directory / name)
        for name in certificate.files
    }


def green_facts(n: int, side: Fraction, compared: Fraction | None) -> dict[str, Any]:
    """Side and the source's comparison value against Green's and Nagamochi's bounds.

    Green's is the strongest value of the DS7 envelope at ``n`` (Theorem 9 or 10, or a
    usable Table 2 row), from `devtools.audit_ds7_lower_bounds`, enclosed to 60 digits
    or as many more as a comparison needs.
    Nagamochi's is ``1 + sqrt(n - 2 floor(sqrt n) + 1)``, compared exactly by squaring.
    Imported here so a replay never loads the algebra system. A certificate with no
    source audit states no comparison value in a file the audit reads, so ``compared`` is
    then ``None`` and so is ``source_value_exceeds_green``.
    """
    ds7 = importlib.import_module("devtools.audit_ds7_lower_bounds")
    green = ds7.best_candidate(n)
    _require(green is not None, f"no DS7 bound applies at n = {n}")

    def sign(value: Fraction) -> int:
        for digits in (60, 120, 240):
            low, high = cast(tuple[Fraction, Fraction], ds7.enclosure(green.expression, digits))
            if not low <= value <= high:
                return 1 if value > high else -1
        raise ValueError("the comparison with Green's bound is not separated at 240 digits")

    low, high = cast(tuple[Fraction, Fraction], ds7.enclosure(green.expression, 60))

    radicand = n - 2 * isqrt(n) + 1
    return {
        "green": f"{green.label}, from n = {green.base_n}",
        "green_interval_float": [float(low), float(high)],
        "side_exceeds_green": sign(side) > 0,
        "source_value_exceeds_green": None if compared is None else sign(compared) > 0,
        "nagamochi": f"1 + sqrt({radicand})",
        "side_exceeds_nagamochi": side > 1 and (side - 1) ** 2 > radicand,
    }


def net_facts(net: dict[str, Any], core: Fraction) -> dict[str, str]:
    """The source's net record against the containment facts recomputed here."""
    facts = n50_net(core)
    end = N50_STEP * N50_LAST
    margin = Fraction(facts["side_margin"])
    _require(
        Fraction(net["step"]) == N50_STEP
        and net["count"] == N50_LAST + 1
        and Fraction(net["endpoint"]) == end
        and Fraction(net["endpoint_check"]) == Fraction(facts["endpoint_check"])
        and Fraction(net["rotated_side_upper"]) == Fraction(facts["rotated_side_upper"])
        and Fraction(net["side_margin"]) == margin
        and Fraction(net["per_edge_margin"]) == margin / 2,
        "the net record differs from the containment facts recomputed here",
    )
    return facts


def _angle_records(
    certificate: dict[str, Any], digest: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    """The 201 replay records a certificate carries, each well formed and at least one."""
    results = certificate["results"]
    _require(
        set(results) == {str(index) for index in range(N50_LAST + 1)},
        "the certificate does not carry exactly the 201 net angles",
    )
    axis = results["0"]
    _require(
        axis["status"] == AXIS_REPLAYED
        and axis["digest"] == digest
        and axis["gamma"] == "1"
        and isinstance(axis["cells"], int)
        and axis["cells"] > 0
        and axis["integer_minimum"] >= 1,
        "the axis record is not a replayed integer table at threshold one",
    )
    nodes = 0
    lows: list[tuple[float, int]] = []
    for index in range(1, N50_LAST + 1):
        record = results[str(index)]
        _require(
            record["status"] == ANGLE_REPLAYED
            and record["candidate_digest"] == digest
            and record["index"] == index
            and isinstance(record["nodes"], int)
            and record["nodes"] > 0
            and record["lower"] >= 1,
            f"angle {index} is not a replayed record with lower bound at least one",
        )
        nodes += record["nodes"]
        lows.append((record["lower"], index))
    least, at = min(lows)
    return axis, {"oblique_nodes": nodes, "least_lower": least, "least_lower_at": at}


def _code_facts(certificate: MixedCertificate, tree: Mapping[Path, str]) -> dict[str, Any]:
    """The directory's code/ and requirements.txt are the retained n = 50 copies."""
    shipped = {path.name: _sha256(path.read_bytes()) for path in _files_in(MIXED_CODE)}
    listed = {
        path.name: digest
        for path, digest in tree.items()
        if path.parent == certificate.directory / "code"
    }
    _require(listed == shipped, "code/ is not byte-identical to mixed_n50_L740/code/")
    requirements = tree[certificate.directory / "requirements.txt"]
    _require(
        requirements == _sha256(MIXED_REQUIREMENTS.read_bytes()),
        "requirements.txt differs from mixed_n50_L740/requirements.txt",
    )
    return {"code_files": len(listed), "code_identical_to_n50": True}


def _source_audit_facts(
    certificate: MixedCertificate,
    files: Mapping[str, bytes],
    archive: str,
    digest: str,
    total: Fraction,
) -> tuple[dict[str, Any], Fraction]:
    """The source's ``completion-audit.json``: the measure, the certificate and the tarball.

    It must name the recomputed candidate digest, state the measure and all 201 angles,
    bind the retained certificate's digest and the tarball's pinned digest, and state its
    improvement as the side less the value it compares with, which is returned.
    """
    audit = json.loads(files[SOURCE_AUDIT])
    n, side = certificate.n, certificate.side
    _require(audit["candidate_digest"] == digest, "recomputed candidate digest differs")
    _require(
        audit["status"] == "AUDITED_AND_PACKAGED"
        and audit["n"] == n
        and Fraction(audit["L"]) == side
        and Fraction(audit["total_mass"]) == total
        and audit["all_angles"] == N50_LAST + 1,
        "the source's audit states another measure",
    )
    _require(
        audit["certificate_sha256"] == _sha256(files["certificate.json"]),
        "the source's audit binds another certificate",
    )
    _require(audit["archive_sha256"] == archive, "the source's audit binds another tarball")
    field = "green_upper" if "green_upper" in audit else "compared_with"
    compared = Fraction(audit[field])
    improvement = Fraction(audit["improvement_lower"])
    _require(improvement == side - compared > 0, "the source's improvement is not L - value")
    facts = {
        "status": audit["status"],
        "certificate_sha256_matches": True,
        "archive_sha256_matches": True,
        "compared_field": field,
        "compared_with": str(compared),
        "compared_note": audit.get("compared_note"),
        "improvement_lower": str(improvement),
    }
    return facts, compared


def _pinned_bundle_facts(
    certificate: MixedCertificate, files: Mapping[str, bytes], tree: Mapping[Path, str]
) -> dict[str, Any]:
    """A certificate with no source audit, bound to its tarball by the digest at the pin.

    The pinned tree must hold no ``completion-audit.json`` in the directory, so a row is
    never read without an audit its tree carries. The tarball's digest at the pinned tree
    must be the one the acquisition record pins with its size, and the README must state
    the claim, the tarball's name and that digest. A fetched bundle is then bound to the
    retained candidate, certificate and manifest by `bundle_bindings`, as for any row.
    """
    directory = certificate.directory
    _require(
        directory / SOURCE_AUDIT not in tree,
        f"the pinned tree holds a {SOURCE_AUDIT} that this certificate's revision does not",
    )
    archive = tree[certificate.upstream_tarball]
    pinned, size = tarball_pin(certificate)
    _require(pinned == archive, "the acquisition record pins another tarball")
    readme = files["README.md"].decode()
    side = certificate.side
    claim = f"# s({certificate.n}) >= {side.numerator}/{side.denominator} "
    _require(readme.startswith(claim), "the README states another claim")
    _require(f"`{certificate.tarball}`" in readme, "the README names another tarball")
    return {
        "status": "BOUND_BY_PINNED_DIGEST",
        "revision": certificate.revision,
        "tarball_bytes": size,
        "readme_claim": readme.splitlines()[0].removeprefix("# "),
    }


def mixed_certificate(
    certificate: MixedCertificate,
    files: Mapping[str, bytes] | None = None,
    tree: Mapping[Path, str] | None = None,
) -> dict[str, Any]:
    """Exact premises of one mixed certificate from its retained files; coverage is not.

    Every retained file must have its pinned digest. The candidate must have the stated
    count, side, core ``9977/10000`` and rectangle count, nonnegative masses inside the
    container, and total ``n - 1/100000``; its digest, recomputed by the source's rule,
    must be the one the manifest, the certificate, the source's audit and the statement
    name. The net must be the 201-node net whose containment is recomputed here, the
    checker the one ``89b674a6...`` names, and code/ the retained n = 50 copy. The
    certificate must carry a replay record at threshold one for every angle, and the
    README must state the tarball's pinned digest. Where the source published an audit,
    it must bind the certificate's and the tarball's digests (`_source_audit_facts`);
    where it did not, the tarball is bound by its digest at the pin
    (`_pinned_bundle_facts`), and a missing audit is refused for every other row.
    """
    tree = tree if tree is not None else read_subtree_manifest(certificate.subtree)
    files = files if files is not None else mixed_retained(certificate)
    directory = certificate.directory
    for name in certificate.files:
        _require(
            name in files and directory / name in tree,
            f"{name} is missing, and this certificate's revision publishes it",
        )
        _require(
            _sha256(files[name]) == tree[directory / name], f"{name} is not the pinned file"
        )
    data = json.loads(files["candidate.json"])
    manifest = json.loads(files["manifest.json"])
    replay = json.loads(files["certificate.json"])
    side, core, items = _n50_measure(data)
    n = certificate.n
    _require(
        data["n"] == n and side == certificate.side and core == MIXED_CORE,
        "count, side or core differs from the statement",
    )
    _require(len(items) == certificate.rectangles, "rectangle count differs")
    for x0, y0, x1, y1, mass in items:
        _require(0 <= x0 < x1 <= side and 0 <= y0 < y1 <= side, "rectangle outside container")
        _require(mass >= 0, "negative mass")
    total = sum((item[4] for item in items), Fraction(0))
    _require(total == Fraction(data["total_mass"]) == n - MIXED_GAP, "total mass differs")
    digest = _semantic_digest(data)
    _require(
        digest
        == certificate.candidate_digest
        == manifest["candidate_digest"]
        == replay["candidate_digest"],
        "recomputed candidate digest differs",
    )
    _require(
        manifest["n"] == n
        and Fraction(manifest["L"]) == side
        and Fraction(manifest["B"]) == core
        and Fraction(manifest["budget"]) == total,
        "the manifest states another measure",
    )
    checker = _sha256((MIXED_CODE / "mixed_rotated_verify.cpp").read_bytes())
    _require(
        manifest["source_sha256"] == checker == N50_CHECKER_SHA256
        and tree[directory / "code/mixed_rotated_verify.cpp"] == checker,
        "the manifest names another checker",
    )
    code = _code_facts(certificate, tree)
    _require(manifest["net"] == replay["net"], "the manifest and certificate nets differ")
    net = net_facts(manifest["net"], core)
    _require(
        replay["status"] == "ALL_ANGLES_VERIFIED_AND_REPLAYED"
        and replay["n"] == n
        and Fraction(replay["L"]) == side
        and Fraction(replay["B"]) == core
        and Fraction(replay["total_mass"]) == total
        and Fraction(replay["budget_gap"]) == n - total
        and replay["angle_count"] == N50_LAST + 1
        and Fraction(replay["point_mass"]) == 0,
        "the certificate states another run",
    )
    axis, oblique = _angle_records(replay, digest)
    archive = tree[certificate.upstream_tarball]
    compared: Fraction | None = None
    binding: dict[str, Any] = {}
    if certificate.source_audit:
        source_audit, compared = _source_audit_facts(certificate, files, archive, digest, total)
    else:
        source_audit = None
        binding = {"tarball_binding": _pinned_bundle_facts(certificate, files, tree)}
    _require(archive in files["README.md"].decode(), "the README states another tarball")
    return {
        "directory": directory.as_posix(),
        "side": str(side),
        "side_float": float(side),
        "core": str(core),
        "rectangles": len(items),
        "total_mass": str(total),
        "budget_gap": str(n - total),
        "candidate_digest": digest,
        "checker_sha256": checker,
        **code,
        "net": net,
        "centre_domains": n50_centre_domains(side, core),
        "certificate_status": replay["status"],
        "axis_cells": axis["cells"],
        "axis_integer_minimum": axis["integer_minimum"],
        **oblique,
        "tarball": certificate.upstream_tarball.as_posix(),
        "tarball_sha256": archive,
        "source_audit": source_audit,
        **binding,
        "comparison": green_facts(n, side, compared),
        "coverage_decided_here": False,
    }


def mixed_audit(packet: Path) -> dict[str, Any]:
    """`mixed_certificate` for every mixed certificate a packet retains."""
    chosen = [certificate for certificate in MIXED.values() if certificate.packet == packet]
    _require(bool(chosen), f"no mixed certificate is registered for {packet.name}")
    revision = json.loads(chosen[0].record.read_text())["sources"][0]["source_commit"]
    _require(all(c.revision == revision for c in chosen), "the packet pins another revision")
    binding = (
        "the source audit's certificate and tarball digests"
        if revision not in WITHOUT_SOURCE_AUDIT
        else (
            "the tarball bound by its digest at the pinned tree, the size the acquisition "
            "record pins and the README's claim and digest, the source publishing no audit "
            "at this revision"
        )
    )
    return {
        "kind": "wand125-mixed-certificate-audit/v1",
        "packet": packet.name,
        "source_revision": revision,
        "certificates": {c.name: mixed_certificate(c) for c in chosen},
        "scope": (
            "Exact premises only, from the retained files: pinned digests, the measure's "
            "count, side, core, nonnegativity and total n - 1/100000, the candidate digest "
            "by the source's rule, the net containment, the checker and code identity, a "
            "replay record at threshold one for each of the 201 angles, and "
            f"{binding}. Coverage is decided by the source's checker, whose replay is "
            "recorded separately."
        ),
    }


# --------------------------------------------------------------------------- mixed replay


def _utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def tarball_pin(certificate: MixedCertificate) -> tuple[str, int]:
    """The tarball's SHA-256 and size as the packet's acquisition files pin them."""
    digest = read_subtree_manifest(certificate.subtree)[certificate.upstream_tarball]
    entries = json.loads(certificate.record.read_text())["sources"][0]["pinned_only"]
    sizes = [
        entry["bytes"]
        for entry in entries
        if entry["path"] == certificate.upstream_tarball.as_posix()
        and entry["sha256"] == digest
    ]
    _require(len(sizes) == 1, "the acquisition record does not pin the tarball")
    return digest, sizes[0]


#: How ``mixed-fetch`` and ``mixed-replay`` may obtain a tarball: ``auto`` tries each raw-file
#: address and then Git, and the digest decides whichever delivers.
TRANSPORTS = ("auto", "url", "git")


def _fetch_url(url: str, partial: Path) -> None:
    with urllib.request.urlopen(url, timeout=600) as response, partial.open("wb") as out:
        shutil.copyfileobj(response, out, 1 << 20)


def _fetch_git(certificate: MixedCertificate, partial: Path) -> str:
    """Fetch the pinned commit alone, without blobs, and read the tarball's one blob."""
    repository = partial.parent / "git"
    if not (repository / ".git").is_dir():
        repository.mkdir(parents=True, exist_ok=True)
        _git(repository, "init", "-q")
        _git(repository, "remote", "add", "origin", SOURCE_URL)
    _git(
        repository,
        "fetch",
        "-q",
        "--depth=1",
        "--filter=blob:none",
        "origin",
        certificate.revision,
    )
    blob = f"{certificate.revision}:{certificate.upstream_tarball.as_posix()}"
    with partial.open("wb") as out:
        subprocess.run(
            ["git", "cat-file", "blob", blob], cwd=repository, stdout=out, check=True
        )
    return f"git {SOURCE_URL} {blob}"


def _download(certificate: MixedCertificate, target: Path, via: str) -> tuple[str, list[str]]:
    """Write the tarball's bytes at the pinned revision to ``target``.

    Returns the route that delivered and every route that was refused before it. ``url``
    tries the raw-file address and then the address it redirects to; ``git`` fetches the
    pinned commit; ``auto`` tries both URLs and then Git. Nothing here trusts the route:
    `fetch_tarball` checks the bytes against the pin.
    """
    _require(via in TRANSPORTS, f"unknown transport: {via}")
    routes = [*(certificate.urls if via != "git" else ()), *(("git",) if via != "url" else ())]
    partial = target.with_name(target.name + ".part")
    refused: list[str] = []
    for route in routes:
        try:
            if route == "git":
                origin = _fetch_git(certificate, partial)
            else:
                _fetch_url(route, partial)
                origin = route
        except (OSError, subprocess.CalledProcessError) as e:
            refused.append(f"{route}: {type(e).__name__}: {e}")
            continue
        partial.replace(target)
        return origin, refused
    raise ValueError(f"no route delivered {certificate.tarball}: {'; '.join(refused)}")


def check_tarball(certificate: MixedCertificate, path: Path) -> dict[str, Any]:
    """A tarball file against the digest and size the packet pins, or a refusal."""
    digest, size = tarball_pin(certificate)
    found, length = _file_sha256(path), path.stat().st_size
    _require(
        found == digest and length == size,
        f"{path.name} has SHA-256 {found} and {length} bytes; "
        f"the pin is {digest} and {size} bytes",
    )
    return {
        "status": "TARBALL_MATCHES_PIN",
        "path": certificate.upstream_tarball.as_posix(),
        "revision": certificate.revision,
        "sha256": found,
        "bytes": length,
    }


def fetch_tarball(
    certificate: MixedCertificate, work: Path, supplied: Path | None = None, via: str = "auto"
) -> dict[str, Any]:
    """Put the pinned tarball in ``work`` and prove it is the pinned bytes before any use.

    The tarball is taken from ``supplied``, or from ``work`` if an earlier run left it
    there, or downloaded at the pinned revision (`_download`). A file with any other
    SHA-256 or size is renamed ``.rejected`` and refused.
    """
    work.mkdir(parents=True, exist_ok=True)
    target = work / certificate.tarball
    refused: list[str] = []
    if supplied is not None:
        if supplied.resolve() != target.resolve():
            shutil.copyfile(supplied, target)
        origin = "supplied"
    elif target.is_file():
        origin = "already in the work directory"
    else:
        origin, refused = _download(certificate, target, via)
    try:
        checked = check_tarball(certificate, target)
    except ValueError:
        target.replace(target.with_name(target.name + ".rejected"))
        raise
    return checked | {"origin": origin, "refused_routes": refused}


def unpack_bundle(certificate: MixedCertificate, tarball: Path, into: Path) -> Path:
    """Unpack the tarball afresh under ``into``; refuse any member outside its bundle."""
    if into.exists():
        shutil.rmtree(into)
    into.mkdir(parents=True)
    with tarfile.open(tarball, "r:gz") as archive:
        for member in archive.getmembers():
            name = PurePosixPath(member.name)
            _require(
                name.parts[0] == certificate.bundle
                and ".." not in name.parts
                and not name.is_absolute()
                and (member.isfile() or member.isdir()),
                f"unexpected archive member: {member.name}",
            )
        archive.extractall(into, filter="data")
    return into / certificate.bundle


def bundle_bindings(
    certificate: MixedCertificate, bundle: Path, tree: Mapping[Path, str] | None = None
) -> dict[str, Any]:
    """An unpacked bundle against its own file list and against the retained packet.

    Run it before anything imports or runs the bundle's code: every entry of
    ``files-sha256.json`` must match and nothing may be unlisted; the bundle's candidate,
    certificate and manifest must be the retained files; its ``code/``, ``proof/verify.cpp``
    and ``requirements.txt`` must be the retained ``mixed_n50_L740`` copies, which were read
    before they were run.
    """
    tree = tree if tree is not None else read_subtree_manifest(certificate.subtree)
    files = check_bundle_hashes(bundle)
    _require(files["status"] == "BUNDLE_FILES_MATCH", f"the bundle's file list fails: {files}")
    for name in ("candidate.json", "certificate.json", "manifest.json"):
        _require(
            _sha256((bundle / "proof" / name).read_bytes())
            == tree[certificate.directory / name],
            f"the bundle's proof/{name} is not the retained file",
        )
    shipped = {path.name: path.read_bytes() for path in _files_in(MIXED_CODE)}
    present = {path.name: path.read_bytes() for path in _files_in(bundle / "code")}
    _require(present == shipped, "the bundle's code/ is not the retained n = 50 code")
    _require(
        (bundle / "proof/verify.cpp").read_bytes() == shipped["mixed_rotated_verify.cpp"],
        "the bundle's proof/verify.cpp is not the retained checker",
    )
    _require(
        (bundle / "requirements.txt").read_bytes() == MIXED_REQUIREMENTS.read_bytes(),
        "the bundle's requirements.txt differs",
    )
    return {
        "status": "BUNDLE_BOUND_TO_PACKET",
        "listed_files": files["listed"],
        "code_files": len(shipped),
    }


def replay_runtime() -> dict[str, str | None]:
    """Refuse a run with asserts off, and fix the environment the replay runs in."""
    _require(
        __debug__ and not os.environ.get("PYTHONOPTIMIZE"),
        "assertions are off: the source's checks are asserts, so drop -O and PYTHONOPTIMIZE",
    )
    os.environ.update(
        {"OPENBLAS_NUM_THREADS": "1", "OMP_NUM_THREADS": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    )
    sys.dont_write_bytecode = True
    names = ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "PYTHONOPTIMIZE")
    return {name: os.environ.get(name) for name in names}


def _replay_direction(job: tuple[str, str, int, str]) -> dict[str, Any]:
    """Replay one net angle with the source's own function, unchanged (worker).

    Index 0 is ``verify_axis_certificate.replay``; any other is
    ``verify_rotated_result.replay`` with the compiled shipped checker. A refusal by the
    shipped checks is returned as ``FAILED`` with its message, never swallowed.
    """
    code, root, index, binary = job
    sys.dont_write_bytecode = True
    if code not in sys.path:
        sys.path.insert(0, code)
    folder = Path(root) / ("axis" if index == 0 else f"net{index:03}")
    candidate = Path(root) / "candidate.json"
    started = _utc()
    clock = time.monotonic()
    own = resource.getrusage(resource.RUSAGE_SELF)
    children = resource.getrusage(resource.RUSAGE_CHILDREN)
    report: dict[str, Any] | None = None
    error: str | None = None
    try:
        if index == 0:
            module = importlib.import_module("verify_axis_certificate")
            report = module.replay(folder, candidate)
        else:
            module = importlib.import_module("verify_rotated_result")
            report = module.replay(folder, Path(binary), candidate)
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
    written = folder / "replayed.json"
    return {
        "index": index,
        "status": "FAILED" if report is None else "REPLAYED",
        "report": report,
        "error": error,
        "replayed_sha256": _sha256(written.read_bytes()) if report is not None else None,
        "started": started,
        "finished": _utc(),
        "wall_seconds": round(time.monotonic() - clock, 3),
        "cpu_seconds": round(cpu, 3),
        "load": os.getloadavg(),
    }


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _append_jsonl(path: Path, row: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as out:
        out.write(json.dumps(row, default=str) + "\n")
        out.flush()
        os.fsync(out.fileno())


def drop_torn_line(path: Path) -> int:
    """Cut a last line an interruption left unfinished, and return the bytes cut.

    Every row is one line, written and synced at once, so only a session killed inside that
    write leaves one, and only at the end. Its angle was never recorded, so it is replayed.
    """
    if not path.is_file():
        return 0
    data = path.read_bytes()
    keep = data.rfind(b"\n") + 1
    if keep == len(data):
        return 0
    with path.open("r+b") as out:
        out.truncate(keep)
    return len(data) - keep


def _passes(row: dict[str, Any], shipped: dict[str, Any]) -> bool:
    """A direction passes when the shipped function returned the certificate's record.

    The row must also carry the digest of the ``replayed.json`` that function wrote: the
    record as ``json.dumps(record, indent=2)`` in the key order the function and the
    certificate share.
    """
    record = shipped[str(row["index"])]
    written = _sha256(json.dumps(record, indent=2).encode())
    return (
        row["status"] == "REPLAYED"
        and row["report"] == record
        and row.get("replayed_sha256") == written
    )


def range_name(first: int, last: int) -> str:
    return f"range-{first:03}-{last:03}"


def shipped_results(certificate: MixedCertificate) -> dict[str, Any]:
    return json.loads(mixed_retained(certificate)["certificate.json"])["results"]


def range_summary(
    certificate: MixedCertificate,
    folder: Path,
    first: int,
    last: int,
    shipped: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """What a range's receipts establish, across every run that wrote to them."""
    shipped = shipped if shipped is not None else shipped_results(certificate)
    rows = read_jsonl(folder / "directions.jsonl")
    runs = read_jsonl(folder / "runs.jsonl")
    passing = {row["index"]: row for row in rows if _passes(row, shipped)}
    refused = sorted({row["index"] for row in rows if not _passes(row, shipped)})
    wanted = set(range(first, last + 1))
    missing = sorted(wanted - set(passing))
    status = "DIFFERS" if refused else ("INCOMPLETE" if missing else "RANGE_REPLAYED")
    return {
        "status": status,
        "certificate": certificate.name,
        "range": [first, last],
        "directions": len(wanted),
        "replayed": len(wanted & set(passing)),
        "missing": missing,
        "refused": refused,
        "runs": [run["run"] for run in runs],
        "cpu_seconds": round(sum(row["cpu_seconds"] for row in passing.values()), 1),
        "scope": (
            "The source's per-angle replay functions and unchanged C++ checker, after the "
            "full driver's preconditions on a bundle bound to the pinned tarball; each "
            "direction passes only if the function returned the certificate's own record."
        ),
    }


def pending_directions(
    folder: Path, shipped: dict[str, Any], first: int, last: int
) -> list[int]:
    """The range's angles with no passing row yet, in the order a replay starts them.

    The axis comes first, then the oblique angles by the certificate's node counts, largest
    first, so that the longest angles do not finish last.
    """
    done = {
        row["index"] for row in read_jsonl(folder / "directions.jsonl") if _passes(row, shipped)
    }
    todo = [index for index in range(first, last + 1) if index not in done]
    return sorted(todo, key=lambda index: (index != 0, -shipped[str(index)].get("nodes", 0)))


def _write_summary(
    certificate: MixedCertificate, folder: Path, first: int, last: int, shipped: dict[str, Any]
) -> dict[str, Any]:
    summary = range_summary(certificate, folder, first, last, shipped)
    atomic_write_text(folder / "summary.json", json.dumps(summary, indent=2) + "\n")
    return summary


def replay_directions(
    certificate: MixedCertificate,
    folder: Path,
    span: tuple[int, int],
    todo: list[int],
    submit: Callable[[int], Future[dict[str, Any]]],
    *,
    workers: int,
    run: str,
    shipped: dict[str, Any],
    deadline: float | None = None,
) -> dict[str, Any]:
    """Run the angles ``todo`` through ``submit``, at most ``workers`` at once.

    Each finished angle is appended to ``directions.jsonl`` and synced, and ``summary.json``
    is rewritten, as soon as it finishes, so the receipts can be committed and pushed at any
    moment and an interruption loses only the angles still running. No angle starts once
    ``deadline`` (a `time.monotonic` value) has passed; the ones running finish.
    """
    first, last = span
    order = deque(todo)
    pending: set[Future[dict[str, Any]]] = set()
    summary = _write_summary(certificate, folder, first, last, shipped)
    while order or pending:
        while (
            order
            and len(pending) < workers
            and (deadline is None or time.monotonic() < deadline)
        ):
            pending.add(submit(order.popleft()))
        if not pending:
            break
        finished, pending = wait(pending, return_when=FIRST_COMPLETED)
        for future in finished:
            row = future.result() | {"run": run}
            row["matches_certificate"] = _passes(row, shipped)
            _append_jsonl(folder / "directions.jsonl", row)
            summary = _write_summary(certificate, folder, first, last, shipped)
            brief = ("index", "status", "matches_certificate", "cpu_seconds")
            print(json.dumps({key: row[key] for key in brief}), flush=True)
    return summary


def mixed_replay(
    certificate: MixedCertificate,
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

    The steps are the complete replay's, restricted to a range so that a certificate can
    be split across sessions: obtain the tarball and prove its pin, unpack it afresh,
    bind the bundle to the packet, repeat the driver's preconditions, bind each oblique
    input in the range to the candidate independently, compile the shipped checker with
    the shipped ``compile_verifier``, then replay each angle with the shipped function
    (`replay_directions`). Running the same command again replays only the angles with no
    passing row, and does nothing but rewrite the summary when there are none. With
    ``stop_after_hours`` no new angle starts after that much wall time.
    """
    runtime = replay_runtime()
    _require(0 <= first <= last <= N50_LAST, f"range outside 0..{N50_LAST}: {first}-{last}")
    _require(1 <= workers <= MAX_REPLAY_WORKERS, f"workers must be 1 to {MAX_REPLAY_WORKERS}")
    clock = time.monotonic()
    folder = receipts / range_name(first, last)
    folder.mkdir(parents=True, exist_ok=True)
    torn = sum(drop_torn_line(folder / name) for name in ("runs.jsonl", "directions.jsonl"))
    shipped = shipped_results(certificate)
    todo = pending_directions(folder, shipped, first, last)
    if not todo:
        return _write_summary(certificate, folder, first, last, shipped)
    tree = read_subtree_manifest(certificate.subtree)
    tarball = fetch_tarball(certificate, work, supplied, via)
    bundle = unpack_bundle(certificate, work / certificate.tarball, work / "unpacked")
    bindings = bundle_bindings(certificate, bundle, tree)
    driver = driver_preconditions(bundle)
    _require(driver.model[-1] == certificate.candidate_digest, "the bundle's candidate differs")
    oblique = [index for index in todo if index]
    for index in oblique:
        check_angle_record(driver.root, index, driver.model[-1], driver.domains)
    inputs = check_inputs(driver.root, tree[certificate.directory / "candidate.json"], oblique)
    binary = driver.root / "replay-verify"
    driver.rotated.compile_verifier(binary)
    run = {
        "run": f"{_utc()}-{os.getpid()}",
        "certificate": certificate.name,
        "range": [first, last],
        "todo": len(todo),
        "torn_bytes_dropped": torn,
        "argv": sys.argv,
        "load": os.getloadavg(),
        "environment": runtime,
        "host": host_facts(),
        "tarball": tarball,
        "bindings": bindings,
        "preconditions": driver.facts(),
        "inputs": {key: inputs[key] for key in ("status", "inputs", "rectangle_images")},
        "binary_sha256": _sha256(binary.read_bytes()),
        "compile": "the shipped compile_verifier: c++ -O2 -std=c++17 -ffp-contract=off "
        "-fno-fast-math",
    }
    _append_jsonl(folder / "runs.jsonl", run)
    print(
        json.dumps({"run": run["run"], "range": [first, last], "todo": len(todo)}), flush=True
    )
    deadline = None if stop_after_hours is None else clock + 3600 * stop_after_hours
    with ProcessPoolExecutor(max_workers=workers) as pool:

        def submit(index: int) -> Future[dict[str, Any]]:
            job = (driver.code, str(driver.root), index, str(binary))
            return pool.submit(_replay_direction, job)

        return replay_directions(
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


def mixed_fetch(
    certificate: MixedCertificate, work: Path, supplied: Path | None = None, via: str = "auto"
) -> dict[str, Any]:
    """Every check a replay makes before its first angle, over all 201, and nothing run.

    The tarball's pin, its fresh unpacking, the bundle's bindings to the packet, the
    driver's preconditions and the independent binding of all 200 oblique inputs to the
    candidate; then what the bundle's records say, with the source's own seconds.
    """
    runtime = replay_runtime()
    tree = read_subtree_manifest(certificate.subtree)
    tarball = fetch_tarball(certificate, work, supplied, via)
    bundle = unpack_bundle(certificate, work / certificate.tarball, work / "unpacked")
    bindings = bundle_bindings(certificate, bundle, tree)
    driver = driver_preconditions(bundle)
    _require(driver.model[-1] == certificate.candidate_digest, "the bundle's candidate differs")
    oblique = range(1, driver.count)
    for index in oblique:
        check_angle_record(driver.root, index, driver.model[-1], driver.domains)
    inputs = check_inputs(driver.root, tree[certificate.directory / "candidate.json"], oblique)
    return {
        "status": "BUNDLE_READY",
        "certificate": certificate.name,
        "environment": runtime,
        "tarball": tarball,
        "bindings": bindings,
        "preconditions": driver.facts(),
        "inputs": inputs,
        "bundle_records": survey_n50_bundle(driver.root, driver.count),
        "bundle": str(bundle),
    }


# --------------------------------------------------------------------------- controls

#: Stage 4 of ``campaign/result-import.md`` for the mixed checker: two mutated
#: certificates refused on one net direction, beside the original accepted again there.
MIXED_CONTROL_KIND = "wand125-mixed-control/v1"
MIXED_MUTATIONS = ("scale-masses", "drop-top-contributor")
MIXED_CONTROL_TIMEOUT = 3600


def mutate_mixed(data: dict[str, Any], kind: str, row: int) -> dict[str, Any]:
    """A copy of a mixed candidate with every mass scaled, or one rectangle row deleted.

    The total is restated exactly, as the shipped ``expand`` requires. A row is one orbit
    of eight images, so deleting it keeps the D4 symmetry the shipped export checks.
    """
    mutated = dict(data)
    if kind == "scale-masses":
        for key in ("rectangles", "points"):
            mutated[key] = [
                item | {"mass": str(Fraction(item["mass"]) * CONTROL_FACTOR)}
                for item in data[key]
            ]
    elif kind == "drop-top-contributor":
        mutated["rectangles"] = [
            item for index, item in enumerate(data["rectangles"]) if index != row
        ]
    else:
        raise ValueError(f"unknown mutation: {kind}")
    masses = (
        Fraction(item["mass"]) for key in ("rectangles", "points") for item in mutated[key]
    )
    mutated["total_mass"] = str(sum(masses, Fraction()))
    return mutated


def control_direction(binary: Path, folder: Path, nodes: int, timeout: int) -> dict[str, Any]:
    """One net direction under the compiled shipped checker, with the replay's node limit."""
    command = [str(binary), "input.txt", str(nodes)]
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    started = time.monotonic()
    try:
        result = subprocess.run(
            command, cwd=folder, capture_output=True, text=True, timeout=timeout, check=False
        )
    except subprocess.TimeoutExpired:
        return {"verdict": "TIMEOUT", "timeout_seconds": timeout}
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    run: dict[str, Any] = {
        "returncode": result.returncode,
        "stderr": result.stderr,
        "cpu_seconds": round(
            after.ru_utime - before.ru_utime + after.ru_stime - before.ru_stime, 3
        ),
        "wall_seconds": round(time.monotonic() - started, 3),
    }
    if result.returncode == 0:
        output = json.loads(result.stdout)
        frontier = output.pop("frontier")
        run |= {"output": output, "frontier_boxes": len(frontier)}
        if frontier:
            run["last_frontier_box"] = frontier[-1]
            run["stopped_at"] = "node limit" if output["nodes"] >= nodes else "depth floor"
    return run


def mixed_control(
    certificate: MixedCertificate,
    work: Path,
    supplied: Path | None = None,
    via: str = "auto",
    index: int | None = None,
) -> dict[str, Any]:
    """Run one mixed certificate and two mutations on one net direction: the receipt.

    The bundle is fetched, bound and checked as for a replay. The direction defaults to
    the oblique one with the least lower bound among the certificate's own records. A
    witness centre is found at that angle (`least_covered`) and evaluated exactly;
    ``scale-masses`` multiplies every mass by `CONTROL_FACTOR`, and
    ``drop-top-contributor`` deletes the rectangle orbit contributing most there. Each
    mutation must leave the witness covered below 1, so it is provably invalid at that
    angle. Each variant is exported by the shipped ``export`` and run by the checker the
    shipped ``compile_verifier`` builds, with the shipped record's node count as the
    limit, which is what the shipped replay passes; the original must return that
    record, and both mutations must stop unresolved.
    """
    runtime = replay_runtime()
    tree = read_subtree_manifest(certificate.subtree)
    tarball = fetch_tarball(certificate, work, supplied, via)
    bundle = unpack_bundle(certificate, work / certificate.tarball, work / "unpacked")
    bindings = bundle_bindings(certificate, bundle, tree)
    driver = driver_preconditions(bundle)
    _require(driver.model[-1] == certificate.candidate_digest, "the bundle's candidate differs")
    shipped = shipped_results(certificate)
    oblique = {i: shipped[str(i)] for i in range(1, driver.count)}
    chosen = min(oblique, key=lambda i: (oblique[i]["lower"], i)) if index is None else index
    _require(chosen in oblique, "a control runs one oblique net direction")
    saved = check_angle_record(driver.root, chosen, driver.model[-1], driver.domains)
    spec = saved["manifest"]
    density = importlib.import_module("mixed_density_check")
    net_audit = importlib.import_module("mixed_net_audit")
    side, core, rects, points = driver.model[:4]
    data = json.loads((driver.root / "candidate.json").read_text())
    _require(not points, "the witness search reads rectangle measures only")
    _require(len(rects) == 8 * len(data["rectangles"]), "eight images of each rectangle")
    c, s = net_rotation(Fraction(spec["t"]))
    domain = (side / 2, Fraction(spec["domain"]["centre_high"]))
    centre = least_covered(rects, (c, s), core, domain)
    orbits = {row: rects[8 * row : 8 * row + 8] for row in range(len(data["rectangles"]))}
    contributions = orbit_contributions(orbits, centre, c, s, core)
    top = heaviest(contributions)
    if CONTROL_FACTOR * Fraction(saved["lower"]) >= 1:
        raise ValueError("the scaling does not take the recorded least bound below 1")
    variants = {"original": data} | {
        kind: mutate_mixed(data, kind, top) for kind in MIXED_MUTATIONS
    }
    gamma = Fraction(spec["gamma"])
    binary = work / "control-verify"
    driver.rotated.compile_verifier(binary)
    shipped_input = (driver.root / f"net{chosen:03}" / "input.txt").read_bytes()
    runs: list[dict[str, Any]] = []
    for label, variant in variants.items():
        folder = work / "control" / label
        shutil.rmtree(folder, ignore_errors=True)
        folder.mkdir(parents=True)
        atomic_write_text(folder / "candidate.json", json.dumps(variant, indent=2) + "\n")
        model = density.expand(variant)
        manifest = driver.rotated.export(
            model, chosen, folder / "input.txt", gamma, net_audit.candidate_net(variant)
        )
        at_witness = coverage_exact(model[2], centre, c, s, core)
        item: dict[str, Any] = {
            "name": label,
            "candidate_digest": model[-1],
            "input_sha256": manifest["input_sha256"],
            "total_mass": str(model[-2]),
            "rectangle_rows": len(variant["rectangles"]),
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
        if label == "scale-masses":
            item["mutation"] = {
                "factor": str(CONTROL_FACTOR),
                "recorded_least_bound_scaled": float(CONTROL_FACTOR * Fraction(saved["lower"])),
            }
        elif label == "drop-top-contributor":
            item["mutation"] = {
                "row": top,
                "rectangle": data["rectangles"][top]["rectangle"],
                "mass": data["rectangles"][top]["mass"],
                "contribution_at_witness_exact": str(contributions[top]),
            }
        run = control_direction(binary, folder, saved["nodes"], MIXED_CONTROL_TIMEOUT)
        output = run.get("output") or {}
        if label == "original":
            matches = run.get("returncode") == 0 and run.get("frontier_boxes") == 0
            matches = matches and all(
                output.get(key) == saved[key] for key in ("status", "nodes", "leaves", "lower")
            )
            run["verdict"] = "ACCEPTED" if matches else "NOT_ACCEPTED"
        elif "verdict" not in run:
            unresolved = output.get("status") == "ANGLE_UNRESOLVED" and run["frontier_boxes"]
            run["verdict"] = "REFUSED" if unresolved else "ACCEPTED"
            if run.get("stopped_at") == "depth floor":
                z = [Fraction(v) for v in run["last_frontier_box"][:2]]
                stop = (
                    side / 2 + z[0] * Fraction(spec["E"]),
                    side / 2 + z[1] * Fraction(spec["E"]),
                )
                at_stop = coverage_exact(model[2], stop, c, s, core)
                run["stop_centre_coverage_exact"] = str(at_stop)
                run["stop_centre_coverage"] = float(at_stop)
        runs.append(item | {"run": run})
        print(json.dumps({"name": label, "verdict": run["verdict"]}), flush=True)
    original, *mutations = runs
    passed = original["run"]["verdict"] == "ACCEPTED"
    refused = all(item["run"]["verdict"] == "REFUSED" for item in mutations)
    return {
        "kind": MIXED_CONTROL_KIND,
        "status": "CONTROLS_REFUSED" if passed and refused else "CONTROL_FAILED",
        "certificate": certificate.name,
        "directory": certificate.directory.as_posix(),
        "revision": certificate.revision,
        "n": certificate.n,
        "side": str(certificate.side),
        "index": chosen,
        "index_choice": "the least lower bound of the certificate's oblique records"
        if index is None
        else "given",
        "shipped_record": {key: saved[key] for key in ("status", "nodes", "leaves", "lower")},
        "gamma": str(gamma),
        "checker": {
            "source_sha256": spec["source_sha256"],
            "compile": "the shipped compile_verifier: c++ -O2 -std=c++17 -ffp-contract=off "
            "-fno-fast-math",
            "binary_sha256": _sha256(binary.read_bytes()),
            "argv": ["verify", "input.txt", str(saved["nodes"])],
        },
        "witness": {
            "centre": [str(v) for v in centre],
            "t": spec["t"],
            "cos": str(c),
            "sin": str(s),
            "side": str(core),
            "domain": [str(v) for v in domain],
            "coverage_exact": str(sum(contributions.values(), Fraction())),
        },
        "runs": runs,
        "tarball": tarball,
        "bindings": bindings,
        "preconditions": driver.facts(),
        "environment": runtime,
        "host": host_facts(),
        "scope": (
            "Stage-4 negative controls: the shipped export and the C++ checker its "
            "compile_verifier builds, on one net direction with the shipped replay's node "
            "limit. Each mutation leaves an exact witness centre covered below 1 at that "
            "angle, so the checker must not verify it."
        ),
    }


def node_weight(index: int) -> float:
    """The relative cost of one checker node at a net index.

    The source's own seconds for n = 84 and 85, each certificate timed on one machine,
    rise from about 0.68 of the mean per node below index 20 to 1.12 above 150; this line
    follows both to within 4 per cent in every band of indices.
    """
    return 0.66 + 0.5 * min(index, 160) / 160


#: The axis direction costs this many weighted nodes per integer-table cell: n = 50's axis
#: replay against its oblique angles, both measured on 2026-09-28. It is under 1 per cent
#: of every certificate's cost.
AXIS_NODES_PER_CELL = 0.016

#: Single directions replayed one at a time (``mixed-replay --range 100-100 --workers 1``)
#: to price the replays, as (certificate, net index, CPU seconds): 2026-10-02 on a 4-core
#: KVM guest (Intel Xeon at 2.10 GHz) whose other three cores were busy, checker built by the
#: shipped ``compile_verifier``. The n = 84 and 85 receipts are in the 2026-10-02 packet.
PRICE_SAMPLES: tuple[tuple[str, int, float], ...] = (
    ("n65", 100, 237.143),
    ("n84", 100, 195.754),
    ("n85", 100, 182.033),
)


def direction_costs(certificate: MixedCertificate) -> list[float]:
    """Each net angle's cost in weighted nodes, from the counts the certificate records."""
    replay = shipped_results(certificate)
    costs = [replay["0"]["cells"] * AXIS_NODES_PER_CELL]
    costs += [replay[str(i)]["nodes"] * node_weight(i) for i in range(1, N50_LAST + 1)]
    return costs


def price_rate() -> tuple[float, list[dict[str, Any]]]:
    """CPU-seconds per weighted node per rectangle of the measure, from `PRICE_SAMPLES`.

    A checker node tests every rectangle image, so its cost scales with the rectangle
    count; the three samples, of 787, 661 and 587 rectangles, agree on the rate to within
    3 per cent of their mean, where the rate per node alone differs by 37 per cent.
    """
    samples = []
    for name, index, cpu in PRICE_SAMPLES:
        certificate = MIXED[name]
        nodes = shipped_results(certificate)[str(index)]["nodes"]
        rate = cpu / (nodes * node_weight(index) * certificate.rectangles)
        samples.append(
            {
                "certificate": name,
                "index": index,
                "cpu_seconds": cpu,
                "nodes": nodes,
                "rate": rate,
            }
        )
    return sum(sample["rate"] for sample in samples) / len(samples), samples


def estimated_cpu_hours(certificate: MixedCertificate, rate: float | None = None) -> float:
    """The complete replay's CPU-hours at `price_rate`, on the host the samples ran on."""
    rate = rate if rate is not None else price_rate()[0]
    return rate * certificate.rectangles * sum(direction_costs(certificate)) / 3600


def mixed_price() -> dict[str, Any]:
    """Every mixed certificate's estimated replay cost, and the samples it rests on."""
    rate, samples = price_rate()
    rows = {}
    for name, certificate in sorted(MIXED.items(), key=lambda item: item[1].n):
        hours = estimated_cpu_hours(certificate, rate)
        costs = direction_costs(certificate)
        rows[name] = {
            "packet": certificate.packet.name,
            "rectangles": certificate.rectangles,
            "weighted_nodes": round(sum(costs)),
            "axis_share": round(costs[0] / sum(costs), 4),
            "cpu_hours": round(hours, 1),
            "wall_hours_at_4_workers": round(hours / MAX_REPLAY_WORKERS, 1),
        }
    return {
        "seconds_per_node_rectangle": rate,
        "samples": samples,
        "certificates": rows,
        "scope": (
            "An estimate: CPU-hours = rate x rectangles x weighted nodes, the nodes and the "
            "axis cells being the certificate's own counts, at the samples' single-threaded "
            "rate. On a guest with busier neighbours n = 50's sampled angles of 2026-09-28 "
            "ran 1.2 to 1.45 times this rate, and its complete replay took 16 worker-hours "
            "of wall time, twice its estimate here; budget wall time accordingly."
        ),
    }


def balanced_ranges(costs: list[float], parts: int) -> list[tuple[int, int]]:
    """``parts`` contiguous ``(first, stop)`` index ranges of about equal summed cost."""
    _require(1 <= parts <= len(costs), f"parts must be between 1 and {len(costs)}")
    total = sum(costs)
    cuts = [0]
    running = 0.0
    for index, cost in enumerate(costs):
        target = total * len(cuts) / parts
        if len(cuts) < parts and running + cost / 2 > target and index > cuts[-1]:
            cuts.append(index)
        running += cost
    while len(cuts) < parts:
        cuts.append(cuts[-1] + 1)
    return list(itertools.pairwise([*cuts, len(costs)]))


def mixed_plan(certificate: MixedCertificate, parts: int) -> dict[str, Any]:
    """Split the 201 angles into ``parts`` contiguous ranges of about equal cost.

    Each range is one ``mixed-replay`` command, for one session or one of several running
    at once; the ranges' receipts merge with ``mixed-merge``.
    """
    costs = direction_costs(certificate)
    total = sum(costs)
    hours = estimated_cpu_hours(certificate)
    rows = []
    for first, stop in balanced_ranges(costs, parts):
        share = sum(costs[first:stop]) / total
        command = (
            "uv run --frozen --all-extras --group dev python -m "
            f"devtools.audit_wand125_point_and_mixed mixed-replay {certificate.name} "
            f"--range {first}-{stop - 1} --work /tmp/wand125-{certificate.name} --workers 4"
        )
        rows.append(
            {
                "range": [first, stop - 1],
                "angles": stop - first,
                "share": round(share, 4),
                "estimated_cpu_hours": round(hours * share, 2),
                "command": command,
            }
        )
    return {
        "certificate": certificate.name,
        "estimated_cpu_hours": round(hours, 1),
        "parts": rows,
        "merge": (
            "uv run --frozen --all-extras --group dev python -m "
            f"devtools.audit_wand125_point_and_mixed mixed-merge {certificate.name}"
        ),
    }


def observed_ratio() -> tuple[float | None, list[dict[str, Any]]]:
    """Measured replay CPU-hours over `estimated_cpu_hours`, over every merged replay.

    Each certificate whose ``merged.json`` holds a complete replay contributes its own
    measured CPU-hours, so the ratio is the record's, and moves as replays are merged.
    """
    rows = []
    for name, certificate in sorted(MIXED.items(), key=lambda item: item[1].n):
        merged = certificate.receipts / "merged.json"
        if not merged.is_file():
            continue
        result = json.loads(merged.read_text())
        if result.get("status") != "FULL_REPLAY_MATCHES_SHIPPED":
            continue
        rows.append(
            {
                "certificate": name,
                "measured_cpu_hours": result["cpu_hours"],
                "estimated_cpu_hours": round(estimated_cpu_hours(certificate), 2),
            }
        )
    if not rows:
        return None, rows
    measured = sum(row["measured_cpu_hours"] for row in rows)
    estimated = sum(row["estimated_cpu_hours"] for row in rows)
    return measured / estimated, rows


def mixed_shard(
    packet: Path, runners: int, workers: int = MAX_REPLAY_WORKERS
) -> dict[str, Any]:
    """Split every complete replay a packet needs across ``runners`` hosts of equal load.

    Each certificate is priced by `estimated_cpu_hours` scaled by `observed_ratio`; one
    larger than a quarter of a runner's share is cut by `balanced_ranges` into pieces of
    about a quarter of that share, and the pieces go, largest first, to the runner with
    the least load. Each runner's commands run one after another at ``workers`` workers;
    a certificate is merged once every piece of it has run.
    """
    chosen = [c for c in MIXED.values() if c.packet == packet]
    _require(bool(chosen), f"no mixed certificate is registered for {packet.name}")
    _require(runners >= 1, "runners must be at least 1")
    ratio, basis = observed_ratio()
    scale = ratio if ratio is not None else 1.0
    hours = {c.name: estimated_cpu_hours(c) * scale for c in chosen}
    share = sum(hours.values()) / runners
    pieces: list[tuple[float, str, int, int]] = []
    for certificate in chosen:
        costs = direction_costs(certificate)
        total = sum(costs)
        parts = max(1, min(len(costs), round(4 * hours[certificate.name] / share)))
        for first, stop in balanced_ranges(costs, parts):
            piece = hours[certificate.name] * sum(costs[first:stop]) / total
            pieces.append((piece, certificate.name, first, stop - 1))
    loads = [0.0] * runners
    assigned: list[list[tuple[float, str, int, int]]] = [[] for _ in range(runners)]
    for piece in sorted(pieces, key=lambda item: (-item[0], item[1], item[2])):
        target = loads.index(min(loads))
        assigned[target].append(piece)
        loads[target] += piece[0]
    prefix = "uv run --frozen --all-extras --group dev python -m "
    tool = "devtools.audit_wand125_point_and_mixed"
    plan = []
    for index, batch in enumerate(assigned, start=1):
        batch.sort(key=lambda item: (MIXED[item[1]].n, MIXED[item[1]].side, item[2]))
        plan.append(
            {
                "runner": index,
                "estimated_cpu_hours": round(loads[index - 1], 2),
                "estimated_wall_hours": round(loads[index - 1] / workers, 2),
                "commands": [
                    f"{prefix}{tool} mixed-replay {name} --range {first}-{last} "
                    f"--work /tmp/wand125-{name} --workers {workers} --via git"
                    for _, name, first, last in batch
                ],
                "pieces": [
                    {"certificate": name, "range": [first, last], "cpu_hours": round(cost, 2)}
                    for cost, name, first, last in batch
                ],
            }
        )
    return {
        "packet": packet.name,
        "runners": runners,
        "workers_per_runner": workers,
        "estimated_cpu_hours": round(sum(hours.values()), 1),
        "unscaled_cpu_hours": round(sum(estimated_cpu_hours(c) for c in chosen), 1),
        "observed_ratio": None if ratio is None else round(ratio, 3),
        "ratio_basis": basis,
        "certificates": {name: round(value, 2) for name, value in hours.items()},
        "plan": plan,
        "merges": [f"{prefix}{tool} mixed-merge {c.name}" for c in chosen],
        "scope": (
            "An estimate: mixed-price's rate, scaled by the ratio of measured to estimated "
            "CPU-hours over every replay already merged. Wall hours assume all workers "
            "stay busy; a rerun of any command replays only what has not passed."
        ),
    }


def mixed_merge(certificate: MixedCertificate, receipts: Path) -> dict[str, Any]:
    """Merge every range's receipts into the complete replay's verdict, or refuse it.

    Each run must have used the pinned tarball, a bundle bound to the packet and the
    driver's preconditions on the stated candidate; every direction row must belong to
    such a run. The replay is complete when every one of the 201 angles has a row on which
    the shipped function returned the certificate's own record, and no row anywhere was
    refused or returned anything else.
    """
    digest, _ = tarball_pin(certificate)
    shipped = shipped_results(certificate)
    passing: dict[int, dict[str, Any]] = {}
    refused: list[str] = []
    ranges: list[dict[str, Any]] = []
    hosts: set[str] = set()
    cpu_all = 0.0
    for folder in sorted(receipts.glob("range-*")):
        runs = {run["run"]: run for run in read_jsonl(folder / "runs.jsonl")}
        for run in runs.values():
            _require(
                run["certificate"] == certificate.name
                and run["tarball"]["sha256"] == digest
                and run["bindings"]["status"] == "BUNDLE_BOUND_TO_PACKET"
                and run["preconditions"]["status"] == "DRIVER_PRECONDITIONS_HOLD"
                and run["preconditions"]["candidate_digest"] == certificate.candidate_digest
                and run["inputs"]["status"] == "ALL_INPUTS_ENCLOSE_THE_CANDIDATE"
                and run["environment"]["PYTHONOPTIMIZE"] is None,
                f"{folder.name}: run {run['run']} is not bound to the pinned tarball",
            )
            hosts.add(str(run["host"]["cpu"]))
        rows = read_jsonl(folder / "directions.jsonl")
        for row in rows:
            _require(row["run"] in runs, f"{folder.name}: a direction row has no run record")
            cpu_all += row["cpu_seconds"]
            if _passes(row, shipped):
                passing.setdefault(row["index"], row)
            else:
                refused.append(f"{folder.name}: angle {row['index']} {row['status']}")
        ranges.append({"range": folder.name, "runs": len(runs), "rows": len(rows)})
    missing = sorted(set(range(N50_LAST + 1)) - set(passing))
    status = (
        "DIFFERS" if refused else ("INCOMPLETE" if missing else "FULL_REPLAY_MATCHES_SHIPPED")
    )
    cpu = sum(row["cpu_seconds"] for row in passing.values())
    return {
        "status": status,
        "certificate": certificate.name,
        "directory": certificate.directory.as_posix(),
        "tarball_sha256": digest,
        "candidate_digest": certificate.candidate_digest,
        "angles_replayed": len(passing),
        "missing": missing,
        "refused": refused,
        "ranges": ranges,
        "hosts": sorted(hosts),
        "axis_cpu_seconds": passing[0]["cpu_seconds"] if 0 in passing else None,
        "cpu_hours": round(cpu / 3600, 3),
        "cpu_hours_all_rows": round(cpu_all / 3600, 3),
        "scope": (
            "The complete replay, possibly split by angle across sessions: the source's "
            "driver preconditions and its per-angle replay functions with its unchanged C++ "
            "checker, every angle returning the record the source's certificate holds. The "
            "same outward-rounded algorithm as the source's run, not an independent one."
        ),
    }


def replay_receipts(
    certificate: MixedCertificate, receipts: Path | None = None
) -> dict[str, Any] | None:
    """Where a certificate's replay stands, when it has range receipts; ``None`` otherwise.

    The receipts are merged by `mixed_merge`, which refuses a run not bound to the pinned
    tarball; receipts with any refused or differing angle are refused here. A partial
    replay is reported as such.
    """
    receipts = receipts if receipts is not None else certificate.receipts
    if not any(receipts.glob("range-*")):
        return None
    merged = mixed_merge(certificate, receipts)
    _require(
        merged["status"] != "DIFFERS",
        f"{certificate.name}: the replay receipts differ: {merged['refused']}",
    )
    return {
        "status": merged["status"],
        "angles_replayed": merged["angles_replayed"],
        "angles_missing": len(merged["missing"]),
        "ranges": [entry["range"] for entry in merged["ranges"]],
        "cpu_hours": merged["cpu_hours"],
    }


def mixed_audit_supplements(packet: Path, tarballs: Iterable[Path] = ()) -> dict[str, Any]:
    """What the audit checks beyond the retained files, kept out of its receipt.

    Each supplied tarball must be one of the packet's, with the pinned digest and size;
    every certificate's replay receipts, when there are any, must merge without a refused
    angle. Neither is written to ``mixed-audit.json``, which stays a function of the
    retained bytes while a replay's receipts are committed range by range.
    """
    chosen = {c.tarball: c for c in MIXED.values() if c.packet == packet}
    checked: dict[str, Any] = {}
    for path in tarballs:
        certificate = chosen.get(path.name)
        if certificate is None:
            raise ValueError(f"{path.name} is not a tarball {packet.name} pins")
        checked[certificate.name] = check_tarball(certificate, path)
    replays = {c.name: replay_receipts(c) for c in chosen.values()}
    return {
        "tarballs": checked,
        "replays": {name: state for name, state in replays.items() if state is not None},
    }


# --------------------------------------------------------------------------- the audit


def provenance(source: Path = SOURCE) -> dict[str, Any]:
    """Every retained file against the subtree manifest, through the decompressed bytes."""
    tree = read_subtree_manifest()
    files = retained_files(source)
    _require(
        set(files) <= set(tree), f"retained outside the manifest: {set(files) - set(tree)}"
    )
    for relative, data in files.items():
        _require(_sha256(data) == tree[relative], f"SHA-256 mismatch: {relative}")
        _require(_pinned_only(relative) is None, f"pinned-only file retained: {relative}")
    missing = sorted(
        str(path)
        for path in set(tree) - set(files)
        if _pinned_only(path) is None and path.parts[0] != ".git"
    )
    _require(not missing, f"retained files missing: {missing}")
    record = json.loads(MANIFEST.read_text())["sources"][0]
    _require(
        record["source_commit"] == REVISION and record["git_tree"] == GIT_TREE, "pin differs"
    )
    _require(record["retained_file_count"] == len(files), "retained file count differs")
    return {
        "revision": REVISION,
        "git_tree": GIT_TREE,
        "subtree_files": len(tree),
        "retained_files": len(files),
        "retained_bytes": sum(len(data) for data in files.values()),
        "pinned_only_files": len(tree) - len(files),
    }


def exact_audit(source: Path = SOURCE) -> dict[str, Any]:
    """The whole first-party exact audit; no source code is imported or run."""
    return {
        "kind": "wand125-point-and-mixed-exact-audit/v1",
        "source_revision": REVISION,
        "provenance": provenance(source),
        "n45": n45_cover(
            _read(N45 / "cover.txt", source), _json(N45 / "provenance.json", source)
        ),
        "n21": n21_certificates(source),
        "n50": {name: n50_certificate(name, source) for name in N50},
        "scope": (
            "Exact premises only: digests, formats, nonnegativity, totals and strict "
            "budgets, D4 invariance of the point measures, the n21 threshold algebra, the "
            "n50 net containment and Green comparison. Coverage is decided by the "
            "source checkers, whose replays are recorded separately."
        ),
    }


# --------------------------------------------------------------------------- acquisition


def _git(checkout: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=checkout, capture_output=True, text=True, check=True
    ).stdout


def acquire(checkout: Path, retrieved_at: str) -> dict[str, Any]:
    """Pin the claim directories of a checkout at REVISION and retain the evidence subset.

    Only reads the checkout: the revision and tree come from ``rev-parse``, and each file's
    bytes are bound to the commit by comparing its Git blob with ``ls-tree``. A sparse
    checkout is enough; ``LICENSE`` is taken from the rectangle packet when its blob is
    the pinned one.
    """
    _require(
        _git(checkout, "rev-parse", "HEAD").strip() == REVISION, "checkout is not REVISION"
    )
    _require(_git(checkout, "rev-parse", "HEAD^{tree}").strip() == GIT_TREE, "tree differs")
    blobs: dict[Path, str] = {}
    for line in _git(checkout, "ls-tree", "-r", "HEAD").splitlines():
        meta, _, name = line.partition("\t")
        blobs[Path(name)] = meta.split()[2]
    wanted = sorted(
        path
        for path in blobs
        if path in TOP_FILES or any(path.is_relative_to(d) for d in CLAIM_DIRS)
    )
    contents: dict[Path, bytes] = {}
    for path in wanted:
        origin = RECTANGLE_LICENSE if path == Path("LICENSE") else checkout / path
        data = origin.read_bytes()
        _require(git_blob(data) == blobs[path], f"bytes are not the pinned blob: {path}")
        contents[path] = data
    code = sorted(
        p for p in wanted if p.parts[:3] == ("certificates", "mixed_n50_L7318", "code")
    )
    for path in code:
        twin = Path("certificates/mixed_n50_L740/code") / path.name
        _require(contents.get(twin) == contents[path], f"L7318 code differs from L740: {path}")
    atomic_write_text(
        SUBTREE, "".join(f"{_sha256(contents[p])}  ./{p}\n" for p in wanted), encoding="utf-8"
    )
    if SOURCE.exists():
        shutil.rmtree(SOURCE)
    retained = [path for path in wanted if _pinned_only(path) is None]
    compressed: list[str] = []
    for path in retained:
        target = SOURCE / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents[path])
        if (
            path.suffix in {".json", ".jsonl", ".txt", ".log"}
            and contents[path].count(b"\n") > LINE_THRESHOLD
        ):
            compressed.append(str(compress(target).relative_to(PACKET)))
    pinned = [
        {
            "path": str(path),
            "bytes": len(contents[path]),
            "sha256": _sha256(contents[path]),
            "reason": _pinned_only(path),
        }
        for path in wanted
        if _pinned_only(path) is not None
        and not path.is_relative_to(N21 / "verifier-source")
        and not path.is_relative_to(N21 / "data")
    ]
    grouped = {
        str(directory): {
            "files": len(members),
            "bytes": sum(len(contents[p]) for p in members),
        }
        for directory in (N21 / "data", N21 / "verifier-source")
        for members in [[p for p in wanted if p.is_relative_to(directory)]]
    }
    entry = {
        "id": "wand125-point-and-mixed",
        "source_url": SOURCE_URL,
        "source_ref": "refs/heads/main",
        "source_commit": REVISION,
        "git_tree": GIT_TREE,
        "archived_path": str(SOURCE.relative_to(REPO)),
        "subtree_manifest": str(SUBTREE.relative_to(REPO)),
        "subtree_scope": [str(path) for path in (*TOP_FILES, *CLAIM_DIRS)],
        "subtree_file_count": len(wanted),
        "subtree_total_bytes": sum(len(data) for data in contents.values()),
        "retained_file_count": len(retained),
        "retained_total_bytes": sum(len(contents[p]) for p in retained),
        "compressed": compressed,
        "pinned_only": pinned,
        "pinned_only_groups": grouped,
        "license": "MIT (wand125); point_n21_L5/UPSTREAM-LICENSE.txt is Evan Daniel's MIT",
        "claims": [
            "s(45) = 7 (point_n45_L7)",
            "s(21) = 5 (point_n21_L5)",
            "s(50) >= 37/5 (certificates/mixed_n50_L740)",
            "s(50) >= 147/20 (certificates/mixed_n50_L735, superseded)",
            "s(50) >= 3659/500 (certificates/mixed_n50_L7318, superseded)",
        ],
    }
    record = {
        "format": "external-source-acquisition-v1",
        "retrieved_at_utc": retrieved_at,
        "git_scope": (
            "A blob-filtered clone of the single public branch, sparse over README.md, "
            "docs/, src/ and the five claim directories; every file under the claim "
            "directories is digested, the rest of the tree is pinned by the commit."
        ),
        "sources": [entry],
    }
    atomic_write_text(MANIFEST, json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return entry


def host_facts() -> dict[str, Any]:
    """CPU, cores and the toolchain versions a replay ran under."""

    def first_line(*command: str) -> str | None:
        try:
            output = subprocess.run(command, capture_output=True, text=True, check=True)
        except OSError, subprocess.CalledProcessError:
            return None
        return output.stdout.splitlines()[0] if output.stdout else None

    cpu = None
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        for line in cpuinfo.read_text().splitlines():
            if line.startswith("model name"):
                cpu = line.split(":", 1)[1].strip()
                break
    return {
        "platform": platform.platform(),
        "cpu": cpu,
        "logical_cpus": os.cpu_count(),
        "python": sys.version,
        "c++": first_line("c++", "--version"),
        "rustc": first_line("rustc", "--version"),
        "cargo": first_line("cargo", "--version"),
    }


def parse_range(text: str) -> tuple[int, int]:
    first, _, last = text.partition("-")
    return int(first), int(last or first)


def _add_mixed_commands(commands: Any) -> None:
    names = sorted(MIXED, key=lambda name: (MIXED[name].n, MIXED[name].side))
    auditing = commands.add_parser(
        "mixed-audit", help="exact premises of a packet's mixed certs"
    )
    auditing.add_argument("packet", help="the packet's directory name under resources/web/")
    auditing.add_argument("--out", type=Path, help="default: PACKET/receipts/mixed-audit.json")
    auditing.add_argument(
        "--check", action="store_true", help="compare with --out, write nothing"
    )
    auditing.add_argument(
        "--tarball", type=Path, action="append", default=[], help="also check this tarball"
    )
    fetching = commands.add_parser("mixed-fetch", help="fetch, pin-check, unpack and bind")
    fetching.add_argument("certificate", choices=names)
    fetching.add_argument("--work", type=Path, required=True, help="a scratch directory")
    fetching.add_argument("--tarball", type=Path, help="use this file instead of downloading")
    fetching.add_argument("--via", choices=TRANSPORTS, default="auto")
    fetching.add_argument("--out", type=Path, required=True)
    replaying = commands.add_parser("mixed-replay", help="replay a range of net angles")
    replaying.add_argument("certificate", choices=names)
    replaying.add_argument("--range", required=True, help="A-B, inclusive; 0 is the axis")
    replaying.add_argument("--work", type=Path, required=True, help="a scratch directory")
    replaying.add_argument("--workers", type=int, default=3)
    replaying.add_argument("--receipts", type=Path, help="default: PACKET/receipts/NAME")
    replaying.add_argument("--tarball", type=Path, help="use this file instead of downloading")
    replaying.add_argument("--via", choices=TRANSPORTS, default="auto")
    replaying.add_argument("--stop-after-hours", type=float, help="start no angle after this")
    merging = commands.add_parser("mixed-merge", help="merge range receipts into a verdict")
    merging.add_argument("certificate", choices=names)
    merging.add_argument("--receipts", type=Path, help="default: PACKET/receipts/NAME")
    merging.add_argument("--out", type=Path, help="default: RECEIPTS/merged.json")
    merging.add_argument(
        "--check", action="store_true", help="compare with --out, write nothing"
    )
    comparing = commands.add_parser("mixed-compare", help="compare a full run of the driver")
    comparing.add_argument("certificate", choices=names)
    comparing.add_argument("bundle", type=Path)
    comparing.add_argument("--out", type=Path, required=True)
    controlling = commands.add_parser("mixed-control", help="refuse two mutations (stage 4)")
    controlling.add_argument("certificate", choices=names)
    controlling.add_argument("--work", type=Path, required=True, help="a scratch directory")
    controlling.add_argument("--index", type=int, help="default: the least recorded bound's")
    controlling.add_argument(
        "--tarball", type=Path, help="use this file instead of downloading"
    )
    controlling.add_argument("--via", choices=TRANSPORTS, default="auto")
    controlling.add_argument(
        "--out", type=Path, help="default: PACKET/receipts/NAME/control.json"
    )
    planning = commands.add_parser("mixed-plan", help="split a replay into balanced ranges")
    planning.add_argument("certificate", choices=names)
    planning.add_argument("--parts", type=int, default=1)
    commands.add_parser("mixed-price", help="estimate every replay's CPU-hours")
    sharding = commands.add_parser("mixed-shard", help="split a packet's replays by runner")
    sharding.add_argument("packet", help="the packet's directory name under resources/web/")
    sharding.add_argument("--runners", type=int, required=True)
    sharding.add_argument("--workers", type=int, default=MAX_REPLAY_WORKERS)


def write_or_check(path: Path, result: dict[str, Any], *, check: bool) -> int:
    text = json.dumps(result, indent=2, default=str) + "\n"
    if check:
        same = path.is_file() and path.read_text(encoding="utf-8") == text
        print("RECEIPT_MATCHES" if same else "RECEIPT_DIFFERS")
        return 0 if same else 1
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(path, text, encoding="utf-8")
    print(text, end="")
    return 0


def _mixed_main(args: argparse.Namespace) -> dict[str, Any] | int:
    """Run one mixed-* command: a result to write, or an exit status when already done."""
    if args.command == "mixed-audit":
        packet = WEB / args.packet
        out = args.out or packet / "receipts/mixed-audit.json"
        status = write_or_check(out, mixed_audit(packet), check=args.check)
        supplements = mixed_audit_supplements(packet, args.tarball)
        print(json.dumps(supplements, indent=2))
        return status
    certificate = MIXED[args.certificate]
    receipts = getattr(args, "receipts", None) or certificate.receipts
    if args.command == "mixed-merge":
        out = args.out or receipts / "merged.json"
        result = mixed_merge(certificate, receipts)
        status = write_or_check(out, result, check=args.check)
        return status or int(result["status"] != "FULL_REPLAY_MATCHES_SHIPPED")
    if args.command == "mixed-plan":
        print(json.dumps(mixed_plan(certificate, args.parts), indent=2))
        return 0
    if args.command == "mixed-replay":
        first, last = parse_range(args.range)
        return mixed_replay(
            certificate,
            args.work.resolve(),
            first,
            last,
            workers=args.workers,
            receipts=receipts.resolve(),
            supplied=args.tarball,
            via=args.via,
            stop_after_hours=args.stop_after_hours,
        )
    if args.command == "mixed-compare":
        shipped = json.loads(mixed_retained(certificate)["certificate.json"])
        return compare_driver_run(args.bundle, shipped)
    work = args.work.resolve()
    if args.command == "mixed-control":
        args.out = args.out or receipts / "control.json"
        args.out.parent.mkdir(parents=True, exist_ok=True)
    return (
        mixed_control(certificate, work, args.tarball, args.via, index=args.index)
        if args.command == "mixed-control"
        else mixed_fetch(certificate, work, args.tarball, args.via)
    )


def _run_mixed(args: argparse.Namespace) -> int:
    if args.command == "mixed-price":
        print(json.dumps(mixed_price(), indent=2))
        return 0
    if args.command == "mixed-shard":
        print(json.dumps(mixed_shard(WEB / args.packet, args.runners, args.workers), indent=2))
        return 0
    outcome = _mixed_main(args)
    if isinstance(outcome, int):
        return outcome
    text = json.dumps(outcome, indent=2, default=str) + "\n"
    if args.command != "mixed-replay":
        atomic_write_text(args.out, text, encoding="utf-8")
    print(text, end="")
    if outcome["status"] == "INCOMPLETE":
        return RESUMABLE
    return 0 if outcome["status"] in PASSING else 1


def _run_n21_control(args: argparse.Namespace) -> int:
    """``n21-control``: one bundle scan serves every mutation named; receipts in ``--out``."""
    bundle = args.bundle.resolve()
    scanned = scan_n21_bundle(bundle)
    statuses = []
    for kind in args.mutation:
        result = n21_control(kind, bundle, args.work.resolve(), args.out.resolve(), scanned)
        print(json.dumps({key: result[key] for key in ("status", "mutation", "run")}, indent=2))
        statuses.append(result["status"])
    return 0 if all(status in PASSING for status in statuses) else 1


#: The exit status of a ``mixed-replay`` that stopped with angles left and none refused:
#: the same command resumes it.
RESUMABLE = 3


#: Every status a command may end with that means it found what it was run to check.
PASSING = frozenset(
    {
        "MATCHES_SOURCE_REFERENCE",
        "MATCHES_SOURCE_M1_RECORD",
        "SAMPLE_REPLAYED",
        "BUNDLE_FILES_MATCH",
        "ALL_INPUTS_ENCLOSE_THE_CANDIDATE",
        "FULL_REPLAY_MATCHES_SHIPPED",
        "STAGE_FILES_COMPARED",
        "BUNDLE_READY",
        "RANGE_REPLAYED",
        "CONTROLS_REFUSED",
        "CONTROL_REFUSED",
    }
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    exact = commands.add_parser("exact", help="recompute the exact premises")
    exact.add_argument("--out", type=Path, default=EXACT_RECEIPT)
    exact.add_argument("--check", action="store_true", help="compare with --out, write nothing")
    getting = commands.add_parser("acquire", help="retain the subset from a pinned checkout")
    getting.add_argument("checkout", type=Path)
    getting.add_argument("--retrieved-at", default="")
    n45 = commands.add_parser("n45-compare", help="compare a verify.sh run directory")
    n45.add_argument("run_dir", type=Path)
    n45.add_argument("--out", type=Path, required=True)
    n21 = commands.add_parser("n21-compare", help="compare a verify_portable.py output")
    n21.add_argument("out_dir", type=Path)
    n21.add_argument("--out", type=Path, required=True)
    n21.add_argument("--m1-linkage", type=Path, help="the pinned m1-full-linkage.json.gz")
    n21.add_argument("--collect", type=Path, help="also copy the run's records here")
    n21.add_argument(
        "--stage", action="append", help="compare only these finished stage directories"
    )
    n21_controlling = commands.add_parser(
        "n21-control", help="run verify_portable.py on a mutated s(21) cover (stage 4)"
    )
    n21_controlling.add_argument("mutation", choices=N21_MUTATIONS, nargs="+")
    n21_controlling.add_argument(
        "--bundle", type=Path, required=True, help="a pristine unpack_bundle.py output"
    )
    n21_controlling.add_argument("--work", type=Path, required=True, help="a scratch directory")
    n21_controlling.add_argument(
        "--out", type=Path, default=N21_CONTROLS, help="default: PACKET/receipts/controls"
    )
    n50 = commands.add_parser("n50-replay", help="replay chosen angles of an n50 bundle")
    n50.add_argument("bundle", type=Path)
    n50.add_argument("--index", type=int, action="append", required=True)
    n50.add_argument("--workers", type=int, default=2)
    n50.add_argument("--out", type=Path, required=True)
    hashes = commands.add_parser("n50-bundle-check", help="check files-sha256.json")
    hashes.add_argument("bundle", type=Path)
    hashes.add_argument("--out", type=Path, required=True)
    inputs = commands.add_parser("n50-inputs", help="bind all 200 inputs to the candidate")
    inputs.add_argument("bundle", type=Path)
    inputs.add_argument("--out", type=Path, required=True)
    comparing = commands.add_parser("n50-compare", help="compare a complete L740 run")
    comparing.add_argument("bundle", type=Path)
    comparing.add_argument("--out", type=Path, required=True)
    hosting = commands.add_parser("host", help="print CPU, core and toolchain facts")
    hosting.add_argument("--out", type=Path)
    _add_mixed_commands(commands)
    args = parser.parse_args()
    if args.command == "acquire":
        print(json.dumps(acquire(args.checkout.resolve(), args.retrieved_at), indent=2))
        return 0
    if args.command == "exact":
        text = json.dumps(exact_audit(), indent=2) + "\n"
        if args.check:
            same = args.out.read_text(encoding="utf-8") == text
            print("EXACT_AUDIT_MATCHES_RECEIPT" if same else "EXACT_AUDIT_DIFFERS")
            return 0 if same else 1
        atomic_write_text(args.out, text, encoding="utf-8")
        print(text, end="")
        return 0
    if args.command == "host":
        text = json.dumps(host_facts(), indent=2) + "\n"
        if args.out:
            atomic_write_text(args.out, text, encoding="utf-8")
        print(text, end="")
        return 0
    own_tail = _run_mixed if args.command.startswith("mixed-") else None
    own_tail = {"n21-control": _run_n21_control}.get(args.command, own_tail)
    if own_tail is not None:
        return own_tail(args)
    if args.command == "n45-compare":
        result = n45_compare(args.run_dir, _json(N45 / "provenance.json"))
    elif args.command == "n21-compare":
        if args.stage:
            _require(args.m1_linkage is not None, "--stage needs --m1-linkage")
            result = compare_stage_files(args.out_dir, args.m1_linkage, args.stage)
        elif args.collect:
            result = n21_collect(args.out_dir, args.collect, args.m1_linkage)
        else:
            result = n21_compare(args.out_dir, m1_linkage=args.m1_linkage)
    elif args.command == "n50-bundle-check":
        result = check_bundle_hashes(args.bundle)
    elif args.command == "n50-inputs":
        result = n50_inputs(args.bundle)
    elif args.command == "n50-compare":
        result = n50_compare(args.bundle)
    else:
        if args.workers < 1 or args.workers > 2:
            parser.error("--workers must be 1 or 2 on a shared host")
        result = n50_replay(args.bundle, args.index, args.workers)
    text = json.dumps(result, indent=2, default=str) + "\n"
    atomic_write_text(args.out, text, encoding="utf-8")
    print(text, end="")
    return 0 if result["status"] in PASSING else 1


if __name__ == "__main__":
    raise SystemExit(main())
