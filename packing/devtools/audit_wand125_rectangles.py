"""Audit Hosono's rectangle-density certificates and replay the reviewed checker.

wand125/square-packing-bounds publishes certificates in Tokoharu's rectangle-density
format, checked by Tokoharu's unchanged ``verify.cpp``. This tool binds them to the
same first-party exact preflight as ``audit_tokoharu_density``: every interval in the
checker input encloses the exact rational datum, the axis-event partition is complete,
the orbit normalization preserves mass, and the total mass is strictly below ``n``.

The packet retains the exact candidates, not the tens of megabytes of derived interval
input. Each input is regenerated here from the candidate and must hash to the SHA-256
the upstream accepting run recorded, so the bytes replayed are the bytes published. The
checker source is the byte-identical copy already retained with Tokoharu's packet.

Each candidate is stored as deterministic gzip (``certified_candidate.json.gz``, listed in
the packet README's Compressed Files table). Every retained read here goes through
`devtools.retained_data.read_retained_bytes`, so the digests checked are those of the
upstream bytes, and a tree restored with ``gunzip -k`` reads the same.

Each retained pin of the source is one `Packet`: a directory under ``resources/web/``,
the revision, and the standing (highest) certificate for each count at that revision.
A packet with a ``base`` retains only the files that are new at its pin. A file an
earlier packet already retains byte for byte is read from there, through the base and
that packet's own base in turn, and the provenance check requires the digest this pin's
tree manifest records for it. ``--packet`` chooses the packet by its date; the default is
the first, so the commands its records give still mean what they said.

Global rotated coverage is still decided by the external C++ checker, so a replay is
V4/C3 machine evidence, exactly as for Tokoharu's own certificates.

Replays take hours each, so they run in batches, often on other machines, each into its
own ``--out``. ``--merge DIR...`` folds such receipts into one (normally the packet's
``receipts/replay``). Every case must be a passed replay of all 201 directions of this
packet's standing certificate: its exact preflight equal to the packet's own preflight
receipt, its input and checker digests the published ones, and the files beside it
present and consistent with it in full (the summary file equal to the receipt's summary,
the runner's output ending with it, the per-angle rows covering every direction with the
summary's totals). A receipt failing any of that, or not of the packet's revision, or
recording a failed run, is refused whole, and so is a case two receipts replayed with
different results; a refusal writes nothing. A run interrupted between cases records no
status, and the cases it lists, each complete, are taken. Agreeing duplicates (the same
results, other timings) keep the case already held. The merged receipt lists cases by
count, each with the host it ran on, and is the same bytes whatever the order of its
inputs and however often it is rerun. ``--check`` checks the receipt in ``--out`` the
same way and writes nothing; with ``--merge`` it is a dry run.

``--control`` is stage 4 of ``campaign/result-import.md`` for this checker: it runs one
standing certificate (``--n``) and two mutations of it on one net direction, by default
the one with the least lower bound in the upstream run's per-angle rows, and writes
``--out/NAME.json``. Each mutation leaves an exact witness centre covered below 1 at
that angle; the original must be accepted with the upstream row's results and both
mutations refused (`control`).

Usage, from ``packing/``::

    .venv/bin/python3 -m devtools.audit_wand125_rectangles --packet 2026-09-28 \\
        --out resources/web/wand125-rectangle-certificates-2026-09-28/receipts/replay \\
        --merge BATCH_A/sep28 BATCH_B
    .venv/bin/python3 -m devtools.audit_wand125_rectangles --packet 2026-09-28 \\
        --out resources/web/wand125-rectangle-certificates-2026-09-28/receipts/replay --check
    .venv/bin/python3 -m devtools.audit_wand125_rectangles --packet 2026-10-01 --control \\
        --n 41 --out resources/web/wand125-rectangle-certificates-2026-10-01/receipts/controls
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import resource
import shutil
import subprocess
import sys
import tempfile
import time
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file, atomic_write_text

from devtools import audit_tokoharu_density as tokoharu
from devtools.retained_data import (
    DATA_SUFFIXES,
    GZIP_SUFFIX,
    LINE_THRESHOLD,
    compress,
    compressed_path,
    describe,
    read_retained_bytes,
    read_retained_text,
    retained_exists,
)

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
SOURCE_URL = "https://github.com/wand125/square-packing-bounds"
CHECKER = tokoharu.SOURCE / "certificates" / tokoharu.CASES[29]
VERIFY_SHA256 = "a75140df1b484ad104a214d2e8de87afda9fca5929341ec40121afde0c1af602"
RUNNER_SHA256 = "7bce246763cac8a2bda9aa4cfd9944aa5e14cde9ac965e00686c25f21ae78261"
CASE_FILES = (
    "certified_candidate.json",
    "certificate_metadata.json",
    "verification_summary.json",
    "verified_angles.jsonl",
)
#: Case files retained as deterministic gzip: every standing candidate is over 1,000 lines.
COMPRESSED_CASE_FILES = frozenset({"certified_candidate.json"})
#: Top-level upstream files and directories every packet's evidence includes.
RETAINED_TOP = ("LICENSE", "README.md", "requirements.txt", "docs")
DEFAULT_TIMEOUT = 24 * 3600
_CERTIFICATE_NAME = re.compile(r"rect_n(\d+)_L\d+")
KIND = "wand125-rectangle-audit/v1"
SCOPE = (
    "Independent exact preconditions and input binding; "
    "optional upstream global interval replay"
)
#: What a replay leaves in each certificate's directory beside the receipt.
REPLAY_FILES = (
    "stdout.log",
    "stderr.log",
    "verification_summary.json",
    "verified_angles.jsonl",
)
#: The top-level fields naming the host of a run; a merged case carries its own copy.
HOST_FIELDS = ("python", "platform", "compiler")

# The standing (highest) certificate for each n at ad43d29, and its exact side.
CASES: dict[int, tuple[str, Fraction]] = {
    18: ("rect_n18_L4695", Fraction(939, 200)),
    19: ("rect_n19_L4815", Fraction(963, 200)),
    20: ("rect_n20_L4895", Fraction(979, 200)),
    21: ("rect_n21_L4985", Fraction(997, 200)),
    26: ("rect_n26_L553", Fraction(553, 100)),
    27: ("rect_n27_L56", Fraction(28, 5)),
    28: ("rect_n28_L5695", Fraction(1139, 200)),
    29: ("rect_n29_L5785", Fraction(1157, 200)),
    30: ("rect_n30_L5865", Fraction(1173, 200)),
    31: ("rect_n31_L592", Fraction(148, 25)),
    32: ("rect_n32_L595", Fraction(119, 20)),
    37: ("rect_n37_L64", Fraction(32, 5)),
    38: ("rect_n38_L652", Fraction(163, 25)),
    39: ("rect_n39_L662", Fraction(331, 50)),
    40: ("rect_n40_L6695", Fraction(1339, 200)),
    41: ("rect_n41_L6745", Fraction(1349, 200)),
    42: ("rect_n42_L676", Fraction(169, 25)),
    43: ("rect_n43_L6855", Fraction(1371, 200)),
    44: ("rect_n44_L6925", Fraction(277, 40)),
    45: ("rect_n45_L6955", Fraction(1391, 200)),
    51: ("rect_n51_L743", Fraction(743, 100)),
    52: ("rect_n52_L7505", Fraction(1501, 200)),
    53: ("rect_n53_L758", Fraction(379, 50)),
    54: ("rect_n54_L7665", Fraction(1533, 200)),
    55: ("rect_n55_L77", Fraction(77, 10)),
    56: ("rect_n56_L776", Fraction(194, 25)),
    57: ("rect_n57_L78", Fraction(39, 5)),
    58: ("rect_n58_L788", Fraction(197, 25)),
    59: ("rect_n59_L7905", Fraction(1581, 200)),
    60: ("rect_n60_L792", Fraction(198, 25)),
    61: ("rect_n61_L796", Fraction(199, 25)),
    66: ("rect_n66_L8345", Fraction(1669, 200)),
    67: ("rect_n67_L844", Fraction(211, 25)),
    68: ("rect_n68_L846", Fraction(423, 50)),
    69: ("rect_n69_L8545", Fraction(1709, 200)),
    70: ("rect_n70_L861", Fraction(861, 100)),
    71: ("rect_n71_L8645", Fraction(1729, 200)),
    72: ("rect_n72_L8705", Fraction(1741, 200)),
    73: ("rect_n73_L874", Fraction(437, 50)),
    74: ("rect_n74_L8815", Fraction(1763, 200)),
    75: ("rect_n75_L889", Fraction(889, 100)),
    76: ("rect_n76_L89", Fraction(89, 10)),
    77: ("rect_n77_L888", Fraction(222, 25)),
    78: ("rect_n78_L8955", Fraction(1791, 200)),
}

# The standing certificate for each n at 39d8ecc. Twelve are unchanged since ad43d29
# (n = 18, 19, 20, 26, 27, 30, 32, 40, 45, 61, 75, 78); the others are raised or new.
CASES_2026_09_28: dict[int, tuple[str, Fraction]] = {
    18: ("rect_n18_L4695", Fraction(939, 200)),
    19: ("rect_n19_L4815", Fraction(963, 200)),
    20: ("rect_n20_L4895", Fraction(979, 200)),
    21: ("rect_n21_L49875", Fraction(399, 80)),
    26: ("rect_n26_L553", Fraction(553, 100)),
    27: ("rect_n27_L56", Fraction(28, 5)),
    28: ("rect_n28_L572", Fraction(143, 25)),
    29: ("rect_n29_L579", Fraction(579, 100)),
    30: ("rect_n30_L5865", Fraction(1173, 200)),
    31: ("rect_n31_L5935", Fraction(1187, 200)),
    32: ("rect_n32_L595", Fraction(119, 20)),
    37: ("rect_n37_L6425", Fraction(257, 40)),
    38: ("rect_n38_L654", Fraction(327, 50)),
    39: ("rect_n39_L663", Fraction(663, 100)),
    40: ("rect_n40_L6695", Fraction(1339, 200)),
    41: ("rect_n41_L6755", Fraction(1351, 200)),
    42: ("rect_n42_L679", Fraction(679, 100)),
    43: ("rect_n43_L6865", Fraction(1373, 200)),
    44: ("rect_n44_L6935", Fraction(1387, 200)),
    45: ("rect_n45_L6955", Fraction(1391, 200)),
    51: ("rect_n51_L74425", Fraction(2977, 400)),
    52: ("rect_n52_L7535", Fraction(1507, 200)),
    53: ("rect_n53_L7595", Fraction(1519, 200)),
    54: ("rect_n54_L76675", Fraction(3067, 400)),
    55: ("rect_n55_L771", Fraction(771, 100)),
    56: ("rect_n56_L777", Fraction(777, 100)),
    57: ("rect_n57_L7835", Fraction(1567, 200)),
    58: ("rect_n58_L789", Fraction(789, 100)),
    59: ("rect_n59_L792", Fraction(198, 25)),
    60: ("rect_n60_L794", Fraction(397, 50)),
    61: ("rect_n61_L796", Fraction(199, 25)),
    66: ("rect_n66_L8375", Fraction(67, 8)),
    67: ("rect_n67_L8455", Fraction(1691, 200)),
    68: ("rect_n68_L8495", Fraction(1699, 200)),
    69: ("rect_n69_L8575", Fraction(343, 40)),
    70: ("rect_n70_L862", Fraction(431, 50)),
    71: ("rect_n71_L8685", Fraction(1737, 200)),
    72: ("rect_n72_L874", Fraction(437, 50)),
    73: ("rect_n73_L878", Fraction(439, 50)),
    74: ("rect_n74_L884", Fraction(221, 25)),
    75: ("rect_n75_L889", Fraction(889, 100)),
    76: ("rect_n76_L892", Fraction(223, 25)),
    77: ("rect_n77_L891", Fraction(891, 100)),
    78: ("rect_n78_L8955", Fraction(1791, 200)),
    86: ("rect_n86_L9355", Fraction(1871, 200)),
    88: ("rect_n88_L945", Fraction(189, 20)),
    89: ("rect_n89_L955", Fraction(191, 20)),
    91: ("rect_n91_L9645", Fraction(1929, 200)),
    94: ("rect_n94_L9795", Fraction(1959, 200)),
    95: ("rect_n95_L98418", Fraction(49209, 5000)),
}

# The standing certificate for each n at 1a25a5e. Sixteen are unchanged since 39d8ecc
# (n = 18, 21, 32, 37, 45, 51, 52, 57, 58, 60, 61, 67, 71, 72, 73, 91); 34 are raised and
# three counts are new (n = 87, 90, 93).
CASES_2026_10_01: dict[int, tuple[str, Fraction]] = {
    18: ("rect_n18_L4695", Fraction(939, 200)),
    19: ("rect_n19_L48175", Fraction(1927, 400)),
    20: ("rect_n20_L48975", Fraction(1959, 400)),
    21: ("rect_n21_L49875", Fraction(399, 80)),
    26: ("rect_n26_L55325", Fraction(2213, 400)),
    27: ("rect_n27_L5635", Fraction(1127, 200)),
    28: ("rect_n28_L57225", Fraction(2289, 400)),
    29: ("rect_n29_L57975", Fraction(2319, 400)),
    30: ("rect_n30_L5875", Fraction(47, 8)),
    31: ("rect_n31_L59525", Fraction(2381, 400)),
    32: ("rect_n32_L595", Fraction(119, 20)),
    37: ("rect_n37_L6425", Fraction(257, 40)),
    38: ("rect_n38_L6545", Fraction(1309, 200)),
    39: ("rect_n39_L6635", Fraction(1327, 200)),
    40: ("rect_n40_L67", Fraction(67, 10)),
    41: ("rect_n41_L676", Fraction(169, 25)),
    42: ("rect_n42_L6815", Fraction(1363, 200)),
    43: ("rect_n43_L68875", Fraction(551, 80)),
    44: ("rect_n44_L69425", Fraction(2777, 400)),
    45: ("rect_n45_L6955", Fraction(1391, 200)),
    51: ("rect_n51_L74425", Fraction(2977, 400)),
    52: ("rect_n52_L7535", Fraction(1507, 200)),
    53: ("rect_n53_L76075", Fraction(3043, 400)),
    54: ("rect_n54_L76725", Fraction(3069, 400)),
    55: ("rect_n55_L77125", Fraction(617, 80)),
    56: ("rect_n56_L77825", Fraction(3113, 400)),
    57: ("rect_n57_L7835", Fraction(1567, 200)),
    58: ("rect_n58_L789", Fraction(789, 100)),
    59: ("rect_n59_L79325", Fraction(3173, 400)),
    60: ("rect_n60_L794", Fraction(397, 50)),
    61: ("rect_n61_L796", Fraction(199, 25)),
    66: ("rect_n66_L8385", Fraction(1677, 200)),
    67: ("rect_n67_L8455", Fraction(1691, 200)),
    68: ("rect_n68_L851", Fraction(851, 100)),
    69: ("rect_n69_L8585", Fraction(1717, 200)),
    70: ("rect_n70_L8625", Fraction(69, 8)),
    71: ("rect_n71_L8685", Fraction(1737, 200)),
    72: ("rect_n72_L874", Fraction(437, 50)),
    73: ("rect_n73_L878", Fraction(439, 50)),
    74: ("rect_n74_L88475", Fraction(3539, 400)),
    75: ("rect_n75_L89", Fraction(89, 10)),
    76: ("rect_n76_L8925", Fraction(357, 40)),
    77: ("rect_n77_L89325", Fraction(3573, 400)),
    78: ("rect_n78_L8965", Fraction(1793, 200)),
    86: ("rect_n86_L9365", Fraction(1873, 200)),
    87: ("rect_n87_L941", Fraction(941, 100)),
    88: ("rect_n88_L94775", Fraction(3791, 400)),
    89: ("rect_n89_L9565", Fraction(1913, 200)),
    90: ("rect_n90_L95775", Fraction(3831, 400)),
    91: ("rect_n91_L9645", Fraction(1929, 200)),
    93: ("rect_n93_L97225", Fraction(3889, 400)),
    94: ("rect_n94_L9805", Fraction(1961, 200)),
    95: ("rect_n95_L98518", Fraction(49259, 5000)),
}

# The standing certificate for each n at b00fc70. Seven are raised since 1a25a5e, by three
# commits of 2 October (06eeb40, 7d77022 and 4318bdf); the other 46 are unchanged and no
# count is new.
CASES_2026_10_02: dict[int, tuple[str, Fraction]] = CASES_2026_10_01 | {
    20: ("rect_n20_L49", Fraction(49, 10)),
    42: ("rect_n42_L68275", Fraction(2731, 400)),
    59: ("rect_n59_L79375", Fraction(127, 16)),
    70: ("rect_n70_L86275", Fraction(3451, 400)),
    77: ("rect_n77_L894", Fraction(447, 50)),
    91: ("rect_n91_L96475", Fraction(3859, 400)),
    93: ("rect_n93_L9735", Fraction(1947, 200)),
}


@dataclass(frozen=True, slots=True)
class Packet:
    """One retained pin of the source, and the standing certificates at that pin."""

    date: str
    revision: str
    cases: Mapping[int, tuple[str, Fraction]]
    git_scope: str
    retention_notes: str
    #: The earlier packet whose retained files this one reads instead of copying.
    base: Packet | None = None
    #: The checkout the packet lives in; a scratch root rebuilds a packet elsewhere.
    root: Path = REPO

    @property
    def relative(self) -> Path:
        """The packet directory relative to the repository root, as its records name it."""
        return WEB.relative_to(REPO) / f"wand125-rectangle-certificates-{self.date}"

    @property
    def directory(self) -> Path:
        return self.root / self.relative

    @property
    def source(self) -> Path:
        return self.directory / "wand125-rectangles"

    @property
    def manifest(self) -> Path:
        return self.directory / "acquisition/sources.json"

    @property
    def tree_manifest(self) -> Path:
        return self.directory / "acquisition/upstream-tree.sha256"

    def required(self, tree: Iterable[Path]) -> set[Path]:
        """The pinned files this packet's evidence consists of, here or in its base."""
        names = {name for name, _side in self.cases.values()}
        return {
            path
            for path in tree
            if path.parts[0] in RETAINED_TOP
            or (
                path.parts[0] == "certificates"
                and len(path.parts) == 3
                and path.parts[1] in names
                and path.parts[2] in CASE_FILES
            )
        }

    def holder(self, relative: Path) -> Packet | None:
        """The packet that retains an upstream path: this one, or the nearest base."""
        if retained_exists(self.source / relative):
            return self
        return None if self.base is None else self.base.holder(relative)

    def locate(self, relative: Path) -> Path | None:
        """The retained copy of an upstream path, in this packet or the nearest base."""
        holder = self.holder(relative)
        return None if holder is None else holder.source / relative

    def referenced_by_packet(self, paths: Iterable[Path]) -> dict[str, int] | None:
        """How many of ``paths`` each earlier packet holds, when the base has a base.

        A packet with one base reads every referenced file from it, which
        ``referenced_path`` already says, so there is nothing more to record.
        """
        if self.base is None or self.base.base is None:
            return None
        counts: dict[str, int] = {}
        for relative in paths:
            holder = self.base.holder(relative)
            if holder is None:
                raise ValueError(f"missing retained file: {relative}")
            name = str(holder.source.relative_to(holder.root))
            counts[name] = counts.get(name, 0) + 1
        return dict(sorted(counts.items()))

    def case_directory(self, source: Path, name: str) -> Path:
        """Where the audit reads a standing certificate from ``source``."""
        here = source / "certificates" / name
        if source.resolve() != self.source.resolve() or here.is_dir():
            return here
        found = self.locate(Path("certificates") / name / CASE_FILES[0])
        if found is None:
            raise ValueError(f"no packet retains {name}")
        return found.parent


SEPTEMBER_27 = Packet(
    date="2026-09-27",
    revision="ad43d29d96d0d9740b34643b5ac3fb960909cf9c",
    cases=CASES,
    git_scope=(
        "The single public branch was fetched; the repository has no tags, releases, "
        "submodules or Git LFS attributes."
    ),
    retention_notes=(
        "The whole tracked tree is pinned by per-file SHA-256 in the tree manifest. "
        "Retained bytes are the top-level README, LICENSE, requirements and docs, "
        "and for each standing rectangle certificate its exact candidate, metadata, "
        "upstream verification summary and per-angle rows. Interval inputs are "
        "regenerated from the candidates and bound to the recorded input SHA-256; "
        "verify.cpp and run_verify.py are byte-identical to Tokoharu's retained copies. "
        "Lower rungs, matching certificates, the earlier point certificates and src/ "
        "(the point-certificate search and checker code) are pinned by digest only."
    ),
)
SEPTEMBER_28 = Packet(
    date="2026-09-28",
    revision="39d8ecc74d651b54ec977c331c8f2015b442a6c4",
    cases=CASES_2026_09_28,
    git_scope=(
        "The single public branch was fetched; git ls-remote lists only refs/heads/main, "
        "so there are no tags, and the tree has no .gitmodules or .gitattributes. The "
        "GitHub releases page was not reachable from the retrieving session; the "
        "2026-09-27 retrieval found no releases, and none is recorded here."
    ),
    retention_notes=(
        "The whole tracked tree is pinned by per-file SHA-256 in the tree manifest. "
        "Retained bytes are the top-level README, which changed since ad43d29, and for "
        "each standing rectangle certificate new or raised since ad43d29 its exact "
        "candidate, metadata, upstream verification summary and per-angle rows. The "
        "LICENSE, requirements, docs and the twelve standing certificates unchanged "
        "since ad43d29 are byte-identical to files the 2026-09-27 packet retains, and "
        "are read from there against this tree's digests. Interval inputs are "
        "regenerated from the candidates and bound to the recorded input SHA-256; "
        "verify.cpp and run_verify.py are byte-identical to Tokoharu's retained copies. "
        "Lower rungs, matching certificates, the point certificates, the point_n21_L5 "
        "and point_n45_L7 bundles, the mixed_n50 certificates and src/ are pinned by "
        "digest only."
    ),
    base=SEPTEMBER_27,
)
OCTOBER_1 = Packet(
    date="2026-10-01",
    revision="1a25a5ed745fdd905a52f48fcc48150a0669032d",
    cases=CASES_2026_10_01,
    git_scope=(
        "A depth-1 clone of the single public branch, so the checkout holds this revision's "
        "tree and no history; git ls-remote lists only refs/heads/main, so there are no "
        "tags, and the tree has no .gitmodules or .gitattributes. The GitHub API listed no "
        "releases and no tags at 2026-10-02T00:28Z, and it is the source of every commit "
        "date this packet states."
    ),
    retention_notes=(
        "The whole tracked tree is pinned by per-file SHA-256 in the tree manifest. "
        "Retained bytes are the top-level README, which changed since 39d8ecc, and for "
        "each standing rectangle certificate new or raised since 39d8ecc its exact "
        "candidate, metadata, upstream verification summary and per-angle rows. The "
        "LICENSE, requirements, docs and the sixteen standing certificates unchanged "
        "since 39d8ecc are byte-identical to files the 2026-09-28 and 2026-09-27 packets "
        "retain, and are read from there against this tree's digests. Interval inputs are "
        "regenerated from the candidates and bound to the recorded input SHA-256; "
        "verify.cpp and run_verify.py are byte-identical to Tokoharu's retained copies. "
        "Lower rungs, matching certificates, the point certificates, the point_n21_L5, "
        "point_n45_L7 and point_n61_L8 bundles, the mixed_n* certificates, the k2m5_n59_L8 "
        "and k2m4_n77_L9 covers and src/ are pinned by digest only."
    ),
    base=SEPTEMBER_28,
)
OCTOBER_2 = Packet(
    date="2026-10-02",
    revision="b00fc70f1904e9b1b567afee056d347f911209e8",
    cases=CASES_2026_10_02,
    git_scope=(
        "A depth-1 clone of the single public branch, so the checkout holds this revision's "
        "tree and no history; git ls-remote lists only refs/heads/main, so there are no "
        "tags, and the tree has no .gitmodules or .gitattributes. Commit dates are from a "
        "blob-filtered clone of the full history, fetched in the same session."
    ),
    retention_notes=(
        "The whole tracked tree is pinned by per-file SHA-256 in the tree manifest. "
        "Retained bytes are the top-level README, which changed since 1a25a5e, and for "
        "each standing rectangle certificate raised since 1a25a5e its exact candidate, "
        "metadata, upstream verification summary and per-angle rows. The LICENSE, "
        "requirements, docs and the 46 standing certificates unchanged since 1a25a5e are "
        "byte-identical to files the 2026-10-01, 2026-09-28 and 2026-09-27 packets retain, "
        "and are read from there against this tree's digests. Interval inputs are "
        "regenerated from the candidates and bound to the recorded input SHA-256; "
        "verify.cpp and run_verify.py are byte-identical to Tokoharu's retained copies. "
        "Lower rungs, matching certificates, the point certificates, the point-only, "
        "exact-cover, mixed and linear bundles and src/ are pinned by digest only."
    ),
    base=OCTOBER_1,
)
#: Every packet by its date, oldest first.
PACKETS: dict[str, Packet] = {
    packet.date: packet for packet in (SEPTEMBER_27, SEPTEMBER_28, OCTOBER_1, OCTOBER_2)
}
DEFAULT_PACKET = SEPTEMBER_27.date


def monotone_bounds(
    cases: Mapping[int, Fraction], upto: int | None = None
) -> dict[int, tuple[Fraction, int]]:
    """Best side and its source count for every n from the least case to ``upto``.

    ``upto`` defaults to the largest case. Deleting squares from a packing proves
    s(m) <= s(n) for m <= n, and a certificate of total mass below k already refutes k
    squares, so each direct bound carries to every larger count.
    """
    result: dict[int, tuple[Fraction, int]] = {}
    best: tuple[Fraction, int] | None = None
    last = max(cases) if upto is None else max(*cases, upto)
    for n in range(min(cases), last + 1):
        if n in cases and (best is None or cases[n] > best[0]):
            best = (cases[n], n)
        if best is not None:
            result[n] = best
    return result


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _upstream_path(relative: Path, tree: Mapping[Path, str]) -> Path:
    """The pinned-tree path a retained file stands for: ``X.gz`` stores ``X``."""
    if relative.name.endswith(GZIP_SUFFIX) and relative not in tree:
        stored = relative.with_name(relative.name.removesuffix(GZIP_SUFFIX))
        if stored in tree:
            return stored
    return relative


def read_tree_manifest(path: Path) -> dict[Path, str]:
    """Parse a sorted ``sha256sum``-style list of ``./``-relative paths."""
    expected: dict[Path, str] = {}
    for line in path.read_text().splitlines():
        digest, separator, name = line.partition("  ")
        relative = Path(name)
        if (
            not separator
            or len(digest) != 64
            or any(char not in "0123456789abcdef" for char in digest)
            or not name.startswith("./")
            or relative.is_absolute()
            or ".." in relative.parts
            or relative in expected
        ):
            raise ValueError(f"invalid or duplicate tree checksum entry: {line!r}")
        expected[relative] = digest
    if not expected:
        raise ValueError("empty tree checksum manifest")
    return expected


def _git(checkout: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments], cwd=checkout, capture_output=True, text=True, check=True
    ).stdout.strip()


def _manifest_entry(packet: Packet) -> dict[str, Any]:
    entries = [
        entry
        for entry in tokoharu.load_json(packet.manifest).get("sources", [])
        if isinstance(entry, dict) and entry.get("id") == "wand125-rectangles"
    ]
    if len(entries) != 1:
        raise ValueError("acquisition manifest must identify exactly one wand125 source")
    return entries[0]


def _referenced(
    packet: Packet, missing: set[Path], tree: Mapping[Path, str]
) -> tuple[int, int]:
    """Check the files a packet reads from its base against this pin's digests."""
    total = 0
    for relative in sorted(missing):
        found = None if packet.base is None else packet.base.locate(relative)
        if found is None:
            raise ValueError(f"missing retained file: {relative}")
        data = read_retained_bytes(found)
        if hashlib.sha256(data).hexdigest() != tree[relative]:
            raise ValueError(f"referenced file differs from the pinned tree: {relative}")
        total += len(data)
    return len(missing), total


def source_provenance(packet: Packet, source: Path) -> dict[str, Any]:
    """Bind the source to a clean pinned checkout or to the retained, digest-checked subset."""
    tree = read_tree_manifest(packet.tree_manifest)
    if (source / ".git").exists():
        if _git(source, "rev-parse", "HEAD") != packet.revision or _git(
            source, "status", "--porcelain"
        ):
            raise ValueError("source checkout is dirty or differs from the pinned revision")
        kind = "clean-git-checkout"
    elif source.resolve() != packet.source.resolve():
        raise ValueError("non-checkout source must be the retained acquisition subset")
    else:
        kind = "verified-retained-subset"
    entry = _manifest_entry(packet)
    if (
        entry.get("source_commit") != packet.revision
        or entry.get("archived_path") != str(packet.source.relative_to(packet.root))
        or entry.get("tree_manifest") != str(packet.tree_manifest.relative_to(packet.root))
        or entry.get("upstream_file_count") != len(tree)
    ):
        raise ValueError("acquisition manifest does not bind the pinned revision and tree")
    # Each file on disk and the pinned path it stands for. A stored ``X.gz`` stands for
    # ``X`` and is decompressed; an upstream file that is itself gzip (the mixed_n50
    # bundles) is pinned, and read, as the bytes it is.
    stored: dict[Path, Path] = {}
    for path in source.rglob("*"):
        if ".git" in path.relative_to(source).parts:
            continue
        if path.is_symlink():
            raise ValueError(f"source contains an unexpected symlink: {path}")
        if path.is_file():
            stored[path.relative_to(source)] = _upstream_path(path.relative_to(source), tree)
    actual = set(stored.values())
    if kind == "clean-git-checkout" and actual != set(tree):
        raise ValueError("checkout file set differs from the pinned tree manifest")
    if not actual <= set(tree):
        raise ValueError(
            f"retained files outside the pinned tree: {sorted(actual - set(tree))}"
        )
    missing = packet.required(tree) - actual
    if missing and (kind == "clean-git-checkout" or packet.base is None):
        raise ValueError(f"missing retained case files: {sorted(map(str, missing))}")
    sizes: dict[Path, int] = {}
    for on_disk, relative in sorted(stored.items()):
        path = source / on_disk
        data = path.read_bytes() if on_disk == relative else read_retained_bytes(path)
        if hashlib.sha256(data).hexdigest() != tree[relative]:
            raise ValueError(f"SHA-256 mismatch against the pinned tree: {relative}")
        sizes[relative] = len(data)
    total_bytes = sum(sizes.values())
    referenced = _referenced(packet, missing, tree)
    if kind == "verified-retained-subset" and (
        len(actual) != entry.get("retained_file_count")
        or total_bytes != entry.get("retained_total_bytes")
    ):
        raise ValueError("retained file count or bytes differ from the acquisition manifest")
    if (
        packet.base is not None
        and kind == "verified-retained-subset"
        and (
            entry.get("referenced_path")
            != str(packet.base.source.relative_to(packet.base.root))
            or referenced
            != (entry.get("referenced_file_count"), entry.get("referenced_total_bytes"))
        )
    ):
        raise ValueError("referenced files differ from the acquisition manifest")
    by_packet = packet.referenced_by_packet(sorted(missing))
    if kind == "verified-retained-subset" and by_packet != entry.get(
        "referenced_files_by_packet"
    ):
        raise ValueError("referenced files per packet differ from the acquisition manifest")
    for name, _ in packet.cases.values():
        for file, digest in (("verify.cpp", VERIFY_SHA256), ("run_verify.py", RUNNER_SHA256)):
            if tree.get(Path("certificates") / name / file) != digest:
                raise ValueError(f"{name}/{file} is not the reviewed Tokoharu checker")
    for file, digest in (("verify.cpp", VERIFY_SHA256), ("run_verify.py", RUNNER_SHA256)):
        if _sha256(CHECKER / file) != digest:
            raise ValueError(f"retained Tokoharu {file} differs from the reviewed checker")
    result: dict[str, Any] = {
        "kind": kind,
        "revision": packet.revision,
        "tree_manifest": str(packet.tree_manifest.relative_to(packet.root)),
        "upstream_files": len(tree),
        "files_verified": len(actual),
        "bytes_verified": total_bytes,
        "checker": str(CHECKER.relative_to(REPO)),
    }
    if packet.base is not None:
        result |= {
            "referenced_path": str(packet.base.source.relative_to(packet.base.root)),
            "files_referenced": referenced[0],
            "bytes_referenced": referenced[1],
        }
    if by_packet is not None:
        result["files_referenced_by_packet"] = by_packet
    return result


def input_text(candidate: dict[str, Any]) -> str:
    """Regenerate the checker's interval input from the exact candidate."""
    side, shrink, _total, rectangles = tokoharu.density(candidate)
    centers = {side / 2, side - shrink / 2}
    for a, _b, d, _e, _rho in rectangles:
        for edge in (a, d):
            for center in (edge - shrink / 2, edge + shrink / 2):
                if side / 2 <= center <= side - shrink / 2:
                    centers.add(center)
    lines = [tokoharu.enclose(side), tokoharu.enclose(shrink), str(len(rectangles))]
    lines.extend(" ".join(tokoharu.enclose(value) for value in rect) for rect in rectangles)
    lines.append(str(len(centers)))
    lines.extend(tokoharu.enclose(center) for center in sorted(centers))
    return "\n".join(lines) + "\n"


def materialize(case: Path, scratch: Path) -> dict[str, Any]:
    """Write a replayable case directory whose input matches the published digest."""
    metadata = tokoharu.load_json(case / "certificate_metadata.json")
    summary = tokoharu.load_json(case / "verification_summary.json")
    text = input_text(tokoharu.load_json(case / "certified_candidate.json"))
    digest = hashlib.sha256(text.encode()).hexdigest()
    if digest != metadata.get("input_sha256") or digest != summary.get("input_sha256"):
        raise ValueError(f"regenerated input does not match the published SHA-256: {case.name}")
    if (case / "certificate_input.txt").exists() and _sha256(
        case / "certificate_input.txt"
    ) != digest:
        raise ValueError(f"published input differs from its own recorded SHA-256: {case.name}")
    if (
        summary.get("verifier_source_sha256") != VERIFY_SHA256
        or summary.get("status") != "VERIFIED"
    ):
        raise ValueError(f"upstream accepting run is not the reviewed checker: {case.name}")
    scratch.mkdir(parents=True)
    atomic_write_text(scratch / "certificate_input.txt", text)
    for name in ("certified_candidate.json", "certificate_metadata.json"):
        (scratch / name).write_bytes(read_retained_bytes(case / name))
    for name in ("verify.cpp", "run_verify.py"):
        shutil.copyfile(CHECKER / name, scratch / name)
    return {
        "input_sha256": digest,
        "input_bytes": len(text.encode()),
        "upstream_nodes": summary.get("nodes"),
        "upstream_wall_seconds": summary.get("wall_seconds"),
    }


def audit_case(
    packet: Packet,
    source: Path,
    n: int,
    out: Path,
    *,
    run_replay: bool,
    workers: int,
    timeout: int,
) -> dict[str, Any]:
    name, side = packet.cases[n]
    case = packet.case_directory(source, name)
    # The count the candidate names must be the pinned one (review WSC-1); the mass
    # check against the pinned n is what the bound rests on, and this is identity.
    if tokoharu.load_json(case / "certified_candidate.json").get("n") != n:
        raise ValueError(f"{name} does not declare n = {n}")
    with tempfile.TemporaryDirectory(prefix="wand125-rect-") as directory:
        scratch = Path(directory) / name
        binding = materialize(case, scratch)
        item = tokoharu.preflight(scratch, n, side)
        item |= {"certificate": name, **binding}
        if run_replay:
            if (out / name).exists():
                # Only accepted cases are kept on --resume; this is an interrupted run.
                shutil.rmtree(out / name)
            item["replay"] = tokoharu.replay(scratch, out / name, workers, timeout)
    return item


def standing(checkout: Path) -> dict[int, tuple[str, Fraction]]:
    """The highest rectangle certificate for each count in a checkout, read from the data.

    The count is the directory's; ten early n29 rungs carry no ``n`` of their own, and a
    candidate that does must agree. A tie at the top would leave the standing
    certificate ambiguous, so it is refused.
    """
    found: dict[int, list[tuple[Fraction, str]]] = {}
    for directory in sorted((checkout / "certificates").glob("rect_n*")):
        match = _CERTIFICATE_NAME.fullmatch(directory.name)
        if match is None or not directory.is_dir():
            raise ValueError(f"unexpected rectangle certificate entry: {directory.name}")
        n = int(match[1])
        candidate = tokoharu.load_json(directory / "certified_candidate.json")
        side = candidate.get("L")
        if candidate.get("n", n) != n or not isinstance(side, int | Fraction):
            raise ValueError(f"{directory.name} does not declare n = {n} and an exact side")
        found.setdefault(n, []).append((Fraction(side), directory.name))
    result: dict[int, tuple[str, Fraction]] = {}
    for n, rungs in sorted(found.items()):
        rungs.sort()
        if len(rungs) > 1 and rungs[-1][0] == rungs[-2][0]:
            raise ValueError(f"two certificates share the standing side at n = {n}")
        result[n] = (rungs[-1][1], rungs[-1][0])
    return result


def acquire(packet: Packet, checkout: Path, retrieved_at: str) -> dict[str, Any]:
    """Pin a clean checkout: digest the whole tree, retain the evidence subset."""
    if _git(checkout, "rev-parse", "HEAD") != packet.revision or _git(
        checkout, "status", "--porcelain"
    ):
        raise ValueError("checkout is dirty or differs from the packet's revision")
    if standing(checkout) != dict(packet.cases):
        raise ValueError("the packet's case table is not the checkout's standing set")
    listing = _git(checkout, "ls-files", "-z").split("\0")
    files = sorted(Path(name) for name in listing if name)
    tree = {path: _sha256(checkout / path) for path in files}
    packet.tree_manifest.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(
        packet.tree_manifest, "".join(f"{tree[path]}  ./{path}\n" for path in files)
    )
    required = sorted(packet.required(files))
    referenced = [
        path
        for path in required
        if packet.base is not None
        and (found := packet.base.locate(path)) is not None
        and hashlib.sha256(read_retained_bytes(found)).hexdigest() == tree[path]
    ]
    for name, _side in packet.cases.values():
        shared = {path.parts[2] for path in referenced if path.parts[1:2] == (name,)}
        if shared and shared != set(CASE_FILES):
            raise ValueError(f"{name} is only partly byte-identical to the base packet")
    retained = [path for path in required if path not in referenced]
    if packet.source.exists():
        shutil.rmtree(packet.source)
    for path in retained:
        (packet.source / path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(checkout / path, packet.source / path)
        if path.name in COMPRESSED_CASE_FILES:
            compress(packet.source / path)
    entry: dict[str, Any] = {
        "id": "wand125-rectangles",
        "source_url": SOURCE_URL,
        "source_ref": "refs/heads/main",
        "source_commit": packet.revision,
        "git_tree": _git(checkout, "rev-parse", "HEAD^{tree}"),
        "archived_path": str(packet.source.relative_to(packet.root)),
        "tree_manifest": str(packet.tree_manifest.relative_to(packet.root)),
        "upstream_file_count": len(files),
        "upstream_total_bytes": sum((checkout / path).stat().st_size for path in files),
        "retained_file_count": len(retained),
        "retained_total_bytes": sum((checkout / path).stat().st_size for path in retained),
    }
    if packet.base is not None:
        entry |= {
            "referenced_path": str(packet.base.source.relative_to(packet.base.root)),
            "referenced_file_count": len(referenced),
            "referenced_total_bytes": sum(
                (checkout / path).stat().st_size for path in referenced
            ),
        }
    if (by_packet := packet.referenced_by_packet(referenced)) is not None:
        entry["referenced_files_by_packet"] = by_packet
    entry |= {
        "license": "MIT",
        "branches": {"main": packet.revision},
        "tags": [],
        "releases": [],
        "submodules": [],
        "claims": [f"s({n}) >= {side}" for n, (_name, side) in sorted(packet.cases.items())],
        "retention_notes": packet.retention_notes,
    }
    record = {
        "format": "external-source-acquisition-v1",
        "retrieved_at_utc": retrieved_at,
        "git_scope": packet.git_scope,
        "sources": [entry],
    }
    atomic_write_text(packet.manifest, json.dumps(record, indent=2) + "\n")
    return entry


def _load(out: Path) -> dict[str, Any] | None:
    path = out / "audit.json"
    return json.loads(read_retained_text(path)) if retained_exists(path) else None


def _write(out: Path, record: dict[str, Any]) -> None:
    """Write the receipt plain; a stale compressed copy would disagree with it, so it goes.

    A receipt past 1,000 lines is stored as deterministic gzip once the run ends
    (``python -m devtools.retained_data compress --origin receipt PACKET FILE``).
    """
    atomic_write_text(out / "audit.json", json.dumps(record, indent=2, default=str) + "\n")
    compressed_path(out / "audit.json").unlink(missing_ok=True)


def store_receipt(path: Path, data: bytes) -> Path | None:
    """Write receipt bytes plain, or as deterministic gzip past the retained-data threshold.

    Returns the ``.gz`` path when it compresses, whose row the packet README's Compressed
    Files table then needs (`devtools.retained_data`).
    """
    with atomic_output_file(path) as temporary:
        temporary.write_bytes(data)
    compressed_path(path).unlink(missing_ok=True)
    if path.suffix in DATA_SUFFIXES and data.count(b"\n") > LINE_THRESHOLD:
        return compress(path)
    return None


def _as_recorded(value: object) -> object:
    """A value as a receipt records it: exact rationals as their strings."""
    return json.loads(json.dumps(value, default=str))


def _preflight_cases(packet: Packet) -> dict[int, dict[str, Any]]:
    """The packet's own exact preflight of each standing certificate, by count."""
    record = json.loads(read_retained_text(packet.directory / "receipts/preflight/audit.json"))
    if record.get("status") != "PASS" or record.get("source_revision") != packet.revision:
        raise ValueError(f"the {packet.date} packet's preflight receipt is not a passing run")
    return {case["n"]: case for case in record["cases"]}


@dataclass(frozen=True, slots=True)
class Replayed:
    """One checked case of a replay receipt and the directory holding its files."""

    case: dict[str, Any]
    directory: Path
    #: Everything two replays of one certificate must share: all but timings and host.
    outcome: tuple[Any, ...]


def check_case(
    packet: Packet, directory: Path, case: dict[str, Any], preflight: Mapping[int, Any]
) -> tuple[Any, ...]:
    """Check one replayed case against the packet and its files; return its outcome."""
    n = case.get("n")
    replay = case.get("replay") or {}
    summary = replay.get("summary") or {}
    where = f"{directory}: n = {n}"
    if not isinstance(n, int) or n not in packet.cases or n not in preflight:
        raise ValueError(f"{where} is not a standing certificate of the {packet.date} packet")
    name, side = packet.cases[n]
    if (
        case.get("status") != "PASS"
        or replay.get("status") != "PASS"
        or summary.get("status") != "VERIFIED"
        or summary.get("angle_cases") != tokoharu.ANGLE_COUNT
    ):
        raise ValueError(f"{where} is not a passed replay of all {tokoharu.ANGLE_COUNT} angles")
    exact = {key: value for key, value in case.items() if key != "replay"}
    if exact != preflight[n] or case["certificate"] != name or Fraction(case["L"]) != side:
        raise ValueError(f"{where} differs from the packet's own preflight of {name}")
    if (
        summary.get("input_sha256") != case["input_sha256"]
        or summary.get("verifier_source_sha256") != VERIFY_SHA256
    ):
        raise ValueError(
            f"{where} did not replay the published input under the reviewed checker"
        )
    folder = directory / name
    if missing := [file for file in REPLAY_FILES if not retained_exists(folder / file)]:
        raise ValueError(f"{where}: missing {', '.join(missing)}")
    text = read_retained_text(folder / "verification_summary.json")
    if _as_recorded(tokoharu.load_json(folder / "verification_summary.json")) != summary:
        raise ValueError(f"{where}: verification_summary.json differs from the receipt")
    if not read_retained_text(folder / "stdout.log").endswith(text + "\n"):
        raise ValueError(f"{where}: stdout.log does not end with the run's summary")
    rows = [
        json.loads(line)
        for line in read_retained_text(folder / "verified_angles.jsonl").splitlines()
    ]
    if (
        sorted(row["r"] for row in rows) != list(range(tokoharu.ANGLE_COUNT))
        or any(
            row["status"] != "verified" or Fraction(row["lower_bound"]) < tokoharu.TARGET
            for row in rows
        )
        or sum(row["nodes"] for row in rows) != summary["nodes"]
        or sum(row["leaves"] for row in rows) != summary["leaves"]
        or min(row["lower_bound"] for row in rows)
        != float(Fraction(summary["minimum_printed_leaf_lower_bound"]))
    ):
        raise ValueError(f"{where}: verified_angles.jsonl is not the summary's accepted angles")
    return (
        exact,
        {key: value for key, value in summary.items() if key != "wall_seconds"},
        sorted((row["r"], row["nodes"], row["leaves"], row["lower_bound"]) for row in rows),
    )


def check_receipt(packet: Packet, directory: Path) -> dict[int, Replayed]:
    """Every case of the replay receipt in ``directory``, checked; any failure refuses it."""
    record = _load(directory)
    if record is None:
        raise ValueError(f"{directory} holds no audit.json")
    revision = record.get("source_revision")
    provenance = record.get("provenance") or {}
    if (
        record.get("kind") != KIND
        or revision != packet.revision
        or provenance.get("revision") != revision
    ):
        owner = [item.date for item in PACKETS.values() if item.revision == revision]
        raise ValueError(
            f"{directory} is a receipt of revision {revision}"
            + (f" (the {owner[0]} packet)" if owner else "")
            + f", not of the {packet.date} packet's {packet.revision}"
        )
    if provenance.get("tree_manifest") != str(packet.tree_manifest.relative_to(packet.root)):
        raise ValueError(f"{directory} was not checked against the {packet.date} tree manifest")
    # A run lists a case only once its replay has passed, and records its status only at
    # the end: no status is a run interrupted between cases, whose listed cases are whole.
    if record.get("status", "PASS") != "PASS":
        raise ValueError(
            f"{directory} records a run with status {record['status']!r}: {record.get('error')}"
        )
    preflight = _preflight_cases(packet)
    host = {key: record[key] for key in HOST_FIELDS if key in record}
    result: dict[int, Replayed] = {}
    for case in record.get("cases") or []:
        try:
            outcome = check_case(packet, directory, case, preflight)
        except (AttributeError, KeyError, TypeError) as error:
            raise ValueError(f"{directory}: malformed case: {error!r}") from error
        if case["n"] in result:
            raise ValueError(f"{directory} lists n = {case['n']} twice")
        replay = case["replay"]
        settled = case | {"replay": replay | {"host": replay.get("host") or host}}
        result[case["n"]] = Replayed(settled, directory, outcome)
    if not result:
        raise ValueError(f"{directory} lists no replayed case")
    return result


def matches_upstream(packet: Packet, item: Replayed) -> bool:
    """Whether the replay reproduced the upstream accepting run's results angle by angle."""
    name = item.case["certificate"]
    path = packet.case_directory(packet.source, name) / "verified_angles.jsonl"
    rows = [json.loads(line) for line in read_retained_text(path).splitlines()]
    return item.outcome[2] == sorted(
        (row["r"], row["nodes"], row["leaves"], row["lower_bound"]) for row in rows
    )


def merge(
    packet: Packet, out: Path, sources: Iterable[Path], *, write: bool = True
) -> dict[str, Any]:
    """Fold checked replay receipts into the one in ``out``; every check precedes any write."""
    held = check_receipt(packet, out) if retained_exists(out / "audit.json") else {}
    incoming = sorted(
        (
            (n, json.dumps(item.case, sort_keys=True), item)
            for source in sources
            for n, item in check_receipt(packet, source).items()
        ),
        key=lambda entry: entry[:2],
    )
    added: list[int] = []
    duplicates: list[dict[str, Any]] = []
    for n, _key, item in incoming:
        if n not in held:
            held[n] = item
            added.append(n)
        elif held[n].outcome != item.outcome:
            raise ValueError(
                f"n = {n}: {item.directory} disagrees with the replay in {held[n].directory}"
            )
        elif held[n].directory != item.directory:
            duplicates.append({"n": n, "agrees_with_held": str(item.directory)})
    record = {
        "kind": KIND,
        "source_revision": packet.revision,
        "source": str(packet.source.relative_to(packet.root)),
        "scope": SCOPE,
        "cases": [held[n].case for n in sorted(held)],
        "provenance": source_provenance(packet, packet.source),
        "status": "PASS",
    }
    compressed: list[Path] = []
    if write:
        out.mkdir(parents=True, exist_ok=True)
        for n in added:
            name = held[n].case["certificate"]
            staging = out / f".{name}.merging"
            shutil.rmtree(staging, ignore_errors=True)
            staging.mkdir()
            for file in REPLAY_FILES:
                data = read_retained_bytes(held[n].directory / name / file)
                if (stored := store_receipt(staging / file, data)) is not None:
                    compressed.append(out / name / stored.name)
            shutil.rmtree(out / name, ignore_errors=True)
            staging.rename(out / name)
        text = json.dumps(record, indent=2, default=str) + "\n"
        if (stored := store_receipt(out / "audit.json", text.encode())) is not None:
            compressed.append(stored)
    return {
        "packet": packet.date,
        "out": str(out),
        "written": write,
        "added": [
            {
                "n": n,
                "certificate": held[n].case["certificate"],
                "L": held[n].case["L"],
                "from": str(held[n].directory),
                "matches_upstream_angles": matches_upstream(packet, held[n]),
            }
            for n in added
        ],
        "held": sorted(set(held) - set(added)),
        "agreeing_duplicates": duplicates,
        "compressed_rows": [
            describe(packet.directory, path.resolve(), "receipt").markdown()
            for path in compressed
            if path.resolve().is_relative_to(packet.directory)
        ],
    }


# --------------------------------------------------------------------------- controls

#: Stage 4 of ``campaign/result-import.md``: mutated certificates refused by the checker
#: that accepted the original, beside the original accepted again on the same direction.
CONTROL_KIND = "wand125-rectangle-control/v1"
#: The ``scale-weights`` mutation multiplies every weight by this.
CONTROL_FACTOR = Fraction(99, 100)
MUTATIONS = ("scale-weights", "drop-top-contributor")
#: ``run_verify.py``'s compile command; the runner is pinned by `RUNNER_SHA256`.
RUNNER_COMPILE = (
    *("g++", "-O2", "-std=c++17", "-fno-fast-math", "-ffp-contract=off"),
    *("verify.cpp", "-o", "verify"),
)
CONTROL_TIMEOUT = 3600
FloatRect = tuple[float, float, float, float, float]


def net_rotation(t: Fraction) -> tuple[Fraction, Fraction]:
    """The exact cosine and sine of a net angle whose half-angle tangent is ``t``."""
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def _float_area(rect: FloatRect, polygon: list[tuple[float, float]]) -> float:
    """`audit_tokoharu_density.exact_area` in binary64: for a search, never for a claim."""
    for axis, edge, sign in (
        (0, rect[0], 1),
        (0, rect[2], -1),
        (1, rect[1], 1),
        (1, rect[3], -1),
    ):
        clipped: list[tuple[float, float]] = []
        if not polygon:
            return 0.0
        previous = polygon[-1]
        previous_depth = sign * (previous[axis] - edge)
        for current in polygon:
            depth = sign * (current[axis] - edge)
            if (depth >= 0) != (previous_depth >= 0):
                ratio = previous_depth / (previous_depth - depth)
                clipped.append(
                    (
                        previous[0] + ratio * (current[0] - previous[0]),
                        previous[1] + ratio * (current[1] - previous[1]),
                    )
                )
            if depth >= 0:
                clipped.append(current)
            previous, previous_depth = current, depth
        polygon = clipped
    pairs = zip(polygon, polygon[1:] + polygon[:1], strict=True)
    return abs(sum(p[0] * q[1] - p[1] * q[0] for p, q in pairs)) / 2


def _overlapping[T: (float, Fraction)](
    rects: Iterable[tuple[T, T, T, T, T]], polygon: list[tuple[T, T]]
) -> list[tuple[T, T, T, T, T]]:
    xs, ys = [p[0] for p in polygon], [p[1] for p in polygon]
    left, right, bottom, top = min(xs), max(xs), min(ys), max(ys)
    return [r for r in rects if r[2] > left and r[0] < right and r[3] > bottom and r[1] < top]


def coverage_exact(
    rects: Iterable[tokoharu.Rect],
    centre: tokoharu.Point,
    c: Fraction,
    s: Fraction,
    side: Fraction,
) -> Fraction:
    """The exact mass a square of ``side`` at ``centre``, turned by ``(c, s)``, captures."""
    polygon = tokoharu.square_polygon(*centre, c, s, side)
    return sum(
        (r[4] * tokoharu.exact_area(r, polygon) for r in _overlapping(rects, polygon)),
        Fraction(),
    )


def least_covered(
    rects: Iterable[tokoharu.Rect],
    rotation: tuple[Fraction, Fraction],
    side: Fraction,
    domain: tuple[Fraction, Fraction],
    *,
    grid: int = 33,
    rounds: int = 12,
) -> tokoharu.Point:
    """A centre in ``domain`` squared where the coverage at one angle is low.

    A binary64 grid over the domain, then a pattern search around its least point, and
    the result rounded to a rational in the domain. It is only a candidate: a control
    evaluates it exactly, and nothing rests on it being the minimum.
    """
    floats: list[FloatRect] = [
        (float(a), float(b), float(d), float(e), float(rho)) for a, b, d, e, rho in rects
    ]
    c, s, b = float(rotation[0]), float(rotation[1]), float(side)
    low, high = float(domain[0]), float(domain[1])

    def value(point: tuple[float, float]) -> float:
        x, y = point
        polygon = [
            (x + b * (c * u - s * v) / 2, y + b * (s * u + c * v) / 2)
            for u, v in ((-1, -1), (1, -1), (1, 1), (-1, 1))
        ]
        return sum(r[4] * _float_area(r, polygon) for r in _overlapping(floats, polygon))

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


def orbit_contributions(
    orbits: Mapping[int, Iterable[tokoharu.Rect]],
    centre: tokoharu.Point,
    c: Fraction,
    s: Fraction,
    side: Fraction,
) -> dict[int, Fraction]:
    """Each orbit's exact share of the coverage at ``centre``, for those with any."""
    found = {row: coverage_exact(images, centre, c, s, side) for row, images in orbits.items()}
    return {row: value for row, value in found.items() if value}


def heaviest(contributions: Mapping[int, Fraction]) -> int:
    """The orbit contributing most, the lowest row on a tie."""
    return min(contributions, key=lambda row: (-contributions[row], row))


def mutate_candidate(candidate: dict[str, Any], kind: str, row: int) -> dict[str, Any]:
    """A copy of a Tokoharu-format candidate with every weight scaled, or one row deleted.

    Deleting a row deletes its whole orbit, the eight images the checker expands it to,
    so the mutation keeps the symmetry the format assumes.
    """
    mutated = dict(candidate)
    if kind == "scale-weights":
        mutated["weights"] = [str(Fraction(w) * CONTROL_FACTOR) for w in candidate["weights"]]
    elif kind == "drop-top-contributor":
        for key in ("rectangles", "weights"):
            mutated[key] = [item for index, item in enumerate(candidate[key]) if index != row]
    else:
        raise ValueError(f"unknown mutation: {kind}")
    return mutated


def candidate_orbits(
    candidate: dict[str, Any], rects: list[tokoharu.Rect]
) -> dict[int, list[tokoharu.Rect]]:
    """Each positive-weight row's eight images, as `tokoharu.density` lists them."""
    rows = [index for index, w in enumerate(candidate["weights"]) if Fraction(w) != 0]
    if len(rects) != 8 * len(rows):
        raise ValueError("the density does not hold eight images of each positive row")
    return {row: rects[8 * k : 8 * k + 8] for k, row in enumerate(rows)}


def _run_direction(folder: Path, binary: Path, direction: int, timeout: int) -> dict[str, Any]:
    """One net direction under the compiled checker, as ``run_verify.py`` invokes it."""
    shutil.copyfile(binary, folder / "verify")
    (folder / "verify").chmod(0o755)
    command = ["./verify", str(direction), str(direction)]
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    started = time.monotonic()
    try:
        result = subprocess.run(
            command, cwd=folder, capture_output=True, text=True, timeout=timeout, check=False
        )
    except subprocess.TimeoutExpired:
        return {"command": command, "verdict": "TIMEOUT", "timeout_seconds": timeout}
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    rows = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "rows": rows,
        "cpu_seconds": round(
            after.ru_utime - before.ru_utime + after.ru_stime - before.ru_stime, 3
        ),
        "wall_seconds": round(time.monotonic() - started, 3),
    }


def control(
    packet: Packet,
    n: int,
    out: Path,
    direction: int | None = None,
    timeout: int = CONTROL_TIMEOUT,
) -> dict[str, Any]:
    """Run one certificate and its two mutations on one net direction; write the receipt.

    The direction defaults to the one with the least lower bound in the upstream
    accepting run's per-angle rows. A witness centre is found at that angle
    (`least_covered`) and evaluated exactly; ``scale-weights`` multiplies every weight
    by `CONTROL_FACTOR`, and ``drop-top-contributor`` deletes the orbit contributing most
    at the witness. Each mutation must leave the witness covered below 1, so the
    mutated certificate is provably invalid at that angle before the checker runs; the
    checker, compiled with the runner's command, must then accept the original with the
    upstream row's results and refuse both mutations.
    """
    name, side = packet.cases[n]
    case = packet.case_directory(packet.source, name)
    rows = [
        json.loads(line)
        for line in read_retained_text(case / "verified_angles.jsonl").splitlines()
    ]
    least = min(rows, key=lambda row: (row["lower_bound"], row["r"]))
    r = least["r"] if direction is None else direction
    upstream = next(row for row in rows if row["r"] == r)
    if not 0 < r < tokoharu.ANGLE_COUNT:
        raise ValueError("a control runs one oblique net direction, 1 to 200")
    runner = (CHECKER / "run_verify.py").read_text()
    if (
        _sha256(CHECKER / "verify.cpp") != VERIFY_SHA256
        or _sha256(CHECKER / "run_verify.py") != RUNNER_SHA256
        or repr(list(RUNNER_COMPILE)).replace(", ", ",") not in runner
    ):
        raise ValueError("the retained checker or runner is not the pinned one")
    candidate = tokoharu.load_json(case / "certified_candidate.json")
    _side, shrink, total, rects = tokoharu.density(candidate)
    c, s = net_rotation(r * tokoharu.GAP)
    domain = (side / 2, side - shrink * (c + s) / 2)
    centre = least_covered(rects, (c, s), shrink, domain)
    contributions = orbit_contributions(
        candidate_orbits(candidate, rects), centre, c, s, shrink
    )
    covered = sum(contributions.values(), Fraction())
    top = heaviest(contributions)
    if CONTROL_FACTOR * Fraction(upstream["lower_bound"]) >= 1:
        raise ValueError("the scaling does not take the recorded least bound below 1")
    variants: dict[str, dict[str, Any]] = {"original": candidate}
    variants |= {kind: mutate_candidate(candidate, kind, top) for kind in MUTATIONS}
    runs: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="wand125-rect-control-") as directory:
        scratch = Path(directory)
        shutil.copyfile(CHECKER / "verify.cpp", scratch / "verify.cpp")
        subprocess.run(list(RUNNER_COMPILE), cwd=scratch, check=True)
        compiler = subprocess.run(
            ["g++", "--version"], capture_output=True, text=True, check=True
        )
        binding = materialize(case, scratch / "published")
        for label, variant in variants.items():
            folder = scratch / label
            folder.mkdir()
            text = input_text(variant)
            atomic_write_text(folder / "certificate_input.txt", text)
            _side, _shrink, mass, mutated = tokoharu.density(variant)
            at_witness = coverage_exact(mutated, centre, c, s, shrink)
            item: dict[str, Any] = {
                "name": label,
                "input_sha256": hashlib.sha256(text.encode()).hexdigest(),
                "mass_exact": str(mass),
                "rectangle_rows": len(variant["rectangles"]),
                "witness_coverage_exact": str(at_witness),
                "witness_coverage": float(at_witness),
            }
            if label == "original":
                if item["input_sha256"] != binding["input_sha256"]:
                    raise ValueError("the original's input is not the published one")
            elif at_witness >= 1:
                raise ValueError(f"{label} leaves the witness covered: {float(at_witness)}")
            if label == "scale-weights":
                item["mutation"] = {
                    "factor": str(CONTROL_FACTOR),
                    "recorded_least_bound_scaled": float(
                        CONTROL_FACTOR * Fraction(upstream["lower_bound"])
                    ),
                }
            elif label == "drop-top-contributor":
                item["mutation"] = {
                    "row": top,
                    "rectangle": [str(v) for v in candidate["rectangles"][top]],
                    "weight": str(candidate["weights"][top]),
                    "contribution_at_witness_exact": str(contributions[top]),
                }
            run = _run_direction(folder, scratch / "verify", r, timeout)
            verified = [row for row in run.get("rows", []) if row.get("status") == "verified"]
            if label == "original":
                accepted = (
                    run.get("returncode") == 0
                    and len(verified) == 1
                    and verified[0]["r"] == r
                    and Fraction(verified[0]["lower_bound"]) >= tokoharu.TARGET
                )
                run["matches_upstream"] = accepted and all(
                    verified[0][key] == upstream[key]
                    for key in ("nodes", "leaves", "lower_bound")
                )
                run["verdict"] = "ACCEPTED" if accepted else "NOT_ACCEPTED"
            elif "verdict" not in run:
                refusal = run["returncode"] != 0 and not verified
                run["verdict"] = "REFUSED" if refusal else "ACCEPTED"
            runs.append(item | {"run": run})
            print(json.dumps({"name": label, "verdict": run["verdict"]}), flush=True)
    original, *mutations = runs
    passed = original["run"]["verdict"] == "ACCEPTED" and original["run"]["matches_upstream"]
    refused = all(item["run"]["verdict"] == "REFUSED" for item in mutations)
    record = {
        "kind": CONTROL_KIND,
        "status": "CONTROLS_REFUSED" if passed and refused else "CONTROL_FAILED",
        "packet": packet.date,
        "source_revision": packet.revision,
        "certificate": name,
        "n": n,
        "L": str(side),
        "direction": r,
        "direction_choice": "the least lower bound of the upstream run's per-angle rows"
        if direction is None
        else "given",
        "upstream_row": upstream,
        "checker": {
            "verify_cpp_sha256": VERIFY_SHA256,
            "runner_sha256": RUNNER_SHA256,
            "compile": list(RUNNER_COMPILE),
            "argv": ["./verify", str(r), str(r)],
            "compiler": compiler.stdout.splitlines()[0],
        },
        "witness": {
            "centre": [str(v) for v in centre],
            "t": str(r * tokoharu.GAP),
            "cos": str(c),
            "sin": str(s),
            "side": str(shrink),
            "domain": [str(v) for v in domain],
            "coverage_exact": str(covered),
            "coverage": float(covered),
            "original_mass_exact": str(total),
        },
        "runs": runs,
        "python": sys.version,
        "platform": platform.platform(),
        "scope": (
            "Stage-4 negative controls: the source's unchanged verify.cpp, compiled with "
            "run_verify.py's command, on one net direction. Each mutation leaves an exact "
            "witness centre covered below 1 at that angle, so the checker must refuse it."
        ),
    }
    out.mkdir(parents=True, exist_ok=True)
    atomic_write_text(out / f"{name}.json", json.dumps(record, indent=2) + "\n")
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", choices=tuple(PACKETS), default=DEFAULT_PACKET)
    parser.add_argument("--source", type=Path, help="default: the packet's retained subset")
    parser.add_argument(
        "--acquire", type=Path, help="clean pinned checkout to digest and retain"
    )
    parser.add_argument("--retrieved-at", default="")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--n", type=int, action="append")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument(
        "--resume", action="store_true", help="keep PASS cases already in --out"
    )
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument(
        "--merge",
        type=Path,
        nargs="+",
        metavar="DIR",
        help="fold these replay receipts into --out",
    )
    parser.add_argument(
        "--check", action="store_true", help="check the replay receipt in --out; write nothing"
    )
    parser.add_argument(
        "--control",
        action="store_true",
        help="run one --n and its two mutations on one direction; write --out/NAME.json",
    )
    parser.add_argument("--direction", type=int, help="default: the least recorded bound's")
    args = parser.parse_args()
    packet = PACKETS[args.packet]
    source = packet.source if args.source is None else args.source
    if unknown := sorted(set(args.n or ()) - set(packet.cases)):
        parser.error(f"no standing certificate in the {packet.date} packet at n = {unknown}")
    if args.acquire:
        print(json.dumps(acquire(packet, args.acquire, args.retrieved_at), indent=2))
        return 0
    if args.out is None:
        parser.error("--out is required unless --acquire is given")
    if args.control:
        if len(args.n or ()) != 1 or args.replay or args.merge or args.check:
            parser.error("--control takes one --n, --out and optionally --direction")
        try:
            record = control(packet, args.n[0], args.out, args.direction)
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            print(str(error), file=sys.stderr)
            return 1
        print(json.dumps({key: record[key] for key in ("status", "certificate", "direction")}))
        return 0 if record["status"] == "CONTROLS_REFUSED" else 1
    if args.merge or args.check:
        if args.replay or args.resume or args.n or args.source:
            parser.error("--merge and --check take only --packet and --out")
        try:
            if args.merge:
                result = merge(packet, args.out, args.merge, write=not args.check)
            else:
                cases = check_receipt(packet, args.out)
                result = {
                    "packet": packet.date,
                    "checked": str(args.out),
                    "cases": {n: cases[n].case["L"] for n in sorted(cases)},
                }
        except (OSError, ValueError) as error:
            print(str(error), file=sys.stderr)
            return 1
        print(json.dumps(result, indent=2))
        return 0
    args.out.mkdir(parents=True, exist_ok=True)
    previous = _load(args.out) if args.resume else None
    done = {
        case["n"]: case
        for case in (previous or {}).get("cases", [])
        if case.get("status") == "PASS" and (case.get("replay") or not args.replay)
    }
    record: dict[str, Any] = {
        "kind": KIND,
        "source_revision": packet.revision,
        "source": str(source.resolve()),
        "python": sys.version,
        "scope": SCOPE,
        "cases": [done[n] for n in sorted(done)],
    }
    try:
        record["provenance"] = source_provenance(packet, source)
        record["platform"] = platform.platform()
        if args.replay:
            compiler = subprocess.run(
                ["g++", "--version"], capture_output=True, text=True, check=True
            )
            record["compiler"] = compiler.stdout
        for n in args.n or sorted(packet.cases):
            if n in done:
                continue
            item = audit_case(
                packet,
                source,
                n,
                args.out,
                run_replay=args.replay,
                workers=args.workers,
                timeout=args.timeout,
            )
            record["cases"] = sorted([*record["cases"], item], key=lambda case: case["n"])
            _write(args.out, record)
            print(
                json.dumps({"n": n, "status": item["status"], "replay": "replay" in item}),
                flush=True,
            )
        record["status"] = "PASS"
    except (OSError, TypeError, ValueError, subprocess.SubprocessError) as error:
        record["status"] = "FAIL"
        record["error"] = str(error)
        print(str(error), file=sys.stderr)
    _write(args.out, record)
    return 0 if record["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
