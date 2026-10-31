"""Audit the mixed covers for ``s(n)``, n = 21, 44, 45, 59, 60, 76, 77 and 95, independently.

A *mixed cover* is point masses plus mass spread uniformly along axis-parallel segments
of the grid lines, of total below ``n``, such that every closed unit square in
``[0, s]^2`` captures mass at least one. Two checkers by Daniel, ``zm_mixed.py`` and
``zmx2``, decide that coverage by subdividing pose space. The covers and records live in
three packets under ``resources/web/``:

- ``evand-square-packing-2026-09-28/``: ``s(21) = 5`` and ``s(45) = 7``, both checkers'
  records, this repository's replays, and the ``zmx2`` runs on the point covers ``13``
  and ``32``;
- ``evand-square-packing-2026-10-01/``: ``s(60) = 8`` with both checkers' records, and
  the ``s(32)`` point cover's ``zmx2 --full --pair-points --sym-atoms`` log;
- ``wand125-point-and-mixed-2026-10-01/``: Hosono's ``s(59) = 8`` and ``s(77) = 9``,
  whose ``zmx2`` logs and ``zm_mixed.py`` per-root records are not published, only the
  ``zm_mixed.py`` manifests;
- ``bengreff-s76-certificate-2026-10-14/`` and ``bengreff-s95-certificate-2026-10-15/``:
  Benjamin Greff's ``s(76) = 9`` and ``s(95) = 10``, whose D4 region is *split*: ``zmx2``
  decides every root but a few, and ``zm_mixed.py`` the sub-roots that tile those. Each
  packet holds the source's ``zmx2`` log and sub-root records and this repository's
  replay of both (``receipts/``);
- ``moh63-dev-s44-equals-7-2026-10-29/``: Mohsen Khalili and Sara Gharabaghi's
  ``s(44) = 7``, which ``zmx2`` decides *whole* in both modes; the packet holds the
  source's ``zmx2 --d4`` and ``--full`` logs and this repository's replay of each
  (``receipts/``).

This tool decides, with its own parser and exact integer arithmetic, the facts that do
not need a sweep, and re-reads the sweeps' records without the source's summarisers:

``cover``
    The file is mixed format v1 with no polygons. Every coordinate lies in ``[0, s]``,
    every mass is nonnegative, every segment is axis-parallel with positive length, and
    the total is the stated fraction and below ``n``. The measure is invariant under
    ``x -> s - x`` and ``x <-> y`` in two senses, both decided: entry by entry (points as
    a weighted multiset, segments as unordered endpoint pairs), which is the hypothesis
    of the source's Lean lemma ``MixedCover.d4InvM``, and as a measure (point masses by
    position, segment mass as a piecewise-constant density on each line). It also counts
    the points lying on a line that carries segment mass, of which a clean cover has
    none, and reports the census of segment lengths.
``zmx2``
    A ``zmx2 cert`` log covers exactly the region its mode names, once per root, with no
    uncertified and no capped box. The root grid is derived from the side: centre cells
    of pitch 1/10 over ``[0, s/2]^2`` (``d4``) or ``[0, s]^2`` (``full``, for pass 0, the
    cover, and pass 1, its mirror ``y -> s - y``), by four ``u`` bins of width 1/8 over
    ``[0, 1/2]``. Each ``ROOT`` line must be exactly as ``zmx2`` writes it, with the id
    ``zmx2`` numbers that root with; every header must name the mode and carry no field
    this tool does not know (a later ``zmx2`` appends ``umin``, which leaves angles out,
    and ``area``). The header's ``atoms`` field is reported as flags (``pair_points``,
    ``sym_atoms``, ...), and ``--atoms`` requires a value. Both header versions are read:
    ``zmx2.rs`` ``6b7f0f79``, and ``92a4cfe8``, which appends ``+sym`` under
    ``--sym-atoms``. Several logs are read as one record, and one file may hold several
    runs joined end to end: region runs (``--xlo``/``--xhi``/``--ylo``/``--yhi``/
    ``--bins``) made apart and joined. Then every header must be the same apart from
    ``region``, each run's roots must lie in the limits its own header names, and the
    union must hold every root of the region once; ``joined`` and ``runs`` say how the
    record was made. For ``s(59)`` and ``s(77)``, whose logs are not published, the box
    totals the source's README states are reported beside the audit, as are the
    ``atoms`` the source ran with. ``--case`` also takes the source's point covers,
    ``13`` and ``32``, whose ``d4`` logs must in addition reach the totals
    ``search/ZMX2.md`` section 9 reports.
``zm-mixed``
    A ``zm_mixed.py --resume`` record file names the checker files and cover by SHA-256,
    carries the certificate-mode D4 settings, covers exactly the root grid of pitch 1/20
    over ``[0, s/2]^2`` by sixteen ``u`` bins of width 1/32, once per root, and has no
    uncertified box. The file defaults to the source's complete run where it is
    published (``21``, ``45``, ``60``). With ``--deep``, a *composite*: the complete run
    may leave boxes uncertified, and is clean only if every root holding one is
    certified, whole and without an uncertified box, by a deeper run of the same checker
    files, cover and settings apart from ``depth`` and ``region``, itself complete over
    its region. The report says whether the files are the ones the source's manifests
    name by digest; a replay's are not, as they carry its own CPU times.
``zm-mixed-manifest``
    What a ``zm_mixed.py`` manifest states, read without its per-root records: checker
    and cover digests, settings, the number of roots against the region the settings
    declare, the census, the verdict, and whether the records are retained. It exits 0
    only if the manifests state a whole-region verification with no uncertified box,
    and its ``verdict`` is ``stated verified``, ``undecided`` or ``not clean``. For
    ``s(59)`` it is ``undecided``: the complete depth-24 run states 6 uncertified boxes,
    and a depth-34 run states the one root ``R = [27/20, 7/5] x [13/10, 27/20] x
    [1/4, 9/32]`` certified. Which roots hold the 6 boxes is written only in the
    complete run's per-root records and log, neither published, so whether ``R``
    contains them cannot be decided from the manifests; the report lists what they do
    decide, and the command exits 1. With the records, ``zm-mixed --deep`` decides it.
``composite``
    A split cover's two checkers read as one decision over the D4 region (``76``,
    ``95``). The ``zmx2 cert --d4`` log must be what the ``zmx2`` command requires apart
    from the roots it leaves open, those holding an uncertified or capped box, and every
    header must name this cover by the FNV-1a 64 hash ``zmx2`` computes over its bytes
    and carry the source's ``depth``, ``node_cap``, ``kappa`` and ``K``. Each
    ``zm_mixed.py`` record file must name the case's checker files and cover by SHA-256
    and state its total, carry the certificate-mode D4 settings at depth 24, all files
    the same apart from ``region``, record exactly the roots of the 1/20 by 1/32 grid its
    ``region`` holds, and certify each without an uncertified box. Clean when every
    sub-root of every open ``zmx2`` root is so certified. The report also says whether
    the open roots are the source's ``failing_roots.txt`` and the sub-roots its
    ``jobs.txt``, and whether the sub-roots tile the open roots exactly. Without paths it
    reads this repository's retained replay; ``--source`` reads the source's records.
``compare-sub-roots``
    Record file for record file, by name, a replay's ``zm_mixed.py`` sub-root records
    against the source's, as ``compare-zm-mixed`` compares one file.
``compare-zmx2``, ``compare-zm-mixed``
    Root for root, a replay's census equals the source's record of the same root, timing
    fields excepted. Source roots the replay did not run are counted, not failed, so a
    sample or a partial re-sweep compares as cleanly as a complete one. A ``zmx2``
    replay may be several logs or joined runs; its headers must equal the reference's in
    every field but ``region``, which a joined or partial replay legitimately names
    differently (``not_compared`` says why; ``headers_identical`` compares whole lines),
    each root must appear once, and its ``UNCERT`` lines must match the reference's.
    The default reference is the source's log (``21``, ``45``, ``60``, and ``d4`` for
    ``76`` and ``95``; for ``32 --mode full`` its ``--sym-atoms`` run) or, for the point
    covers' ``d4`` runs, this repository's retained run. For ``59`` and ``77`` the source
    publishes no log, so a reference must be named.
``check``
    All of the above on the retained files: the five covers; the shipped records and
    receipts of ``21``, ``45`` and ``60``, and the source's ``zmx2`` manifests of ``60``
    and of the ``s(32)`` ``--sym-atoms`` log, whose log digest, line counts, header and
    totals must be the audited log's; the retained ``zmx2`` runs on the source's
    ``s(13)`` and ``s(32)`` point covers, which must be present and whose totals must
    equal the ones ``search/ZMX2.md`` reports; the manifests; and, for the split covers,
    the source's composite and the replay's, the replay against the source root for
    root and file for file, and the wall control's census against the replay's; for a
    cover ``zmx2`` decides whole (``44``), the source's log and the replay's in each mode,
    each clean, naming this cover by its hash and carrying the source's settings, and
    the replay equal to the source root for root. What the
    retained files cannot decide (``s(59)``'s composite) is listed under ``undecided``
    and is not counted clean or failed.

Usage (from ``packing/``)::

    uv run --frozen --all-extras --group dev python -m devtools.audit_evand_mixed_covers check
    ... audit_evand_mixed_covers cover --case 77 [PATH]
    ... audit_evand_mixed_covers zmx2 --case 60 --mode full --atoms grid OUT/roots.log
    ... audit_evand_mixed_covers zmx2 --case 77 --mode full --atoms pairpts A.log B.log
    ... audit_evand_mixed_covers compare-zmx2 --case 32 --mode full --records OUT/roots.log
    ... audit_evand_mixed_covers zm-mixed --case 60
    ... audit_evand_mixed_covers zm-mixed --case 59 OUT/roots.jsonl --deep DEEP/roots.jsonl
    ... audit_evand_mixed_covers zm-mixed-manifest --case 59
    ... audit_evand_mixed_covers composite --case 76 [--source]
    ... audit_evand_mixed_covers composite --case 95 OUT/roots.log --zm-mixed OUT/zm_mixed/
    ... audit_evand_mixed_covers compare-sub-roots --case 95 OUT/zm_mixed/
    ... audit_evand_mixed_covers compare-zm-mixed --case 21 --records OUT/roots.jsonl

Every command prints JSON and exits 0 when the audit is clean, 1 otherwise. Files stored
as deterministic gzip are read through `devtools.retained_data.read_retained_bytes`, so a
path may name ``X`` or ``X.gz``; a path naming ``X.xz``, or ``X`` beside it, is read with
`lzma`. Every digest is that of the decompressed bytes.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import json
import lzma
import re
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools.retained_data import (
    MAX_DECOMPRESSED,
    compressed_path,
    read_retained_bytes,
    retained_exists,
)

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
#: The September 28 Daniel packet: the s(21) and s(45) bundles and this repository's receipts.
PACKET = WEB / "evand-square-packing-2026-09-28"
RECEIPTS = PACKET / "receipts"
#: Source trees, each holding ``certificates/<bundle>/`` at the source's relative paths.
EVAND_0928 = PACKET / "square-packing/s12"
EVAND_1001 = WEB / "evand-square-packing-2026-10-01/source/s12"
WAND125_1001 = WEB / "wand125-point-and-mixed-2026-10-01/square-packing-bounds"
BENGREFF_S76 = WEB / "bengreff-s76-certificate-2026-10-14"
BENGREFF_S95 = WEB / "bengreff-s95-certificate-2026-10-15"
KHALILI_S44 = WEB / "moh63-dev-s44-equals-7-2026-10-29"
CHECKER_FILES = ("zm_mixed.py", "mixed_cover.py", "zeromargin.py")
#: The checker files Hosono's ``verify.sh`` pins at evand ``b91d70b6`` (``zm_mixed.py``
#: ``ee3e2915``), which the s(59) and s(77) manifests name; ``zeromargin.py`` is retained
#: by the September 26 packet.
CHECKER_B91D70B6 = (
    EVAND_0928 / "search/zm_mixed.py",
    EVAND_0928 / "search/mixed_cover.py",
    WEB / "evand-square-packing-2026-09-26/square-packing/s12/search/zeromargin.py",
)
#: The checker files at evand ``08e8a5fa`` (``zm_mixed.py`` ``1fd20346``), the same blobs
#: as the s(60) bundle's ``zm_mixed_d4/checker/``, which the packet pins by digest only.
CHECKER_08E8A5FA = tuple(EVAND_1001 / "search" / name for name in CHECKER_FILES)
#: zmx2 census fields compared root for root; ``ms`` is timing and is left out.
ZMX2_CENSUS = ("boxes", "cert", "empty", "uncert", "maxdepth", "capped")
#: ``zmx2 cert`` roots: centre cells of this pitch, by this many ``u`` bins over [0, 1/2].
ZMX2_PITCH = Fraction(1, 10)
ZMX2_BINS = 4
#: The header fields ``zmx2 cert`` writes in every version read here, and the ``atoms``
#: values: a base, then ``+sym`` or ``+mirror`` and ``+fo`` from ``zmx2.rs`` ``92a4cfe8`` on.
ZMX2_HEADER_FIELDS = ("hash", "mode", "atoms", "depth", "node_cap", "kappa", "K", "region")
ZMX2_ATOM_BASES = ("grid", "pairpts", "none")
ZMX2_ATOM_SUFFIXES = {"sym": "sym_atoms", "mirror": "mirror_only", "fo": "first_order"}
#: ``zm_mixed.py`` roots: centre cells of this pitch over [0, s/2]^2, this many ``u`` bins.
ZM_MIXED_PITCH = Fraction(1, 20)
ZM_MIXED_BINS = 16
#: The zm_mixed.py settings every certificate-mode D4 record file must carry.
ZM_MIXED_SETTINGS: dict[str, Any] = {
    "mode": "D4",
    "depth": 24,
    "pitch": str(ZM_MIXED_PITCH),
    "ubins": ZM_MIXED_BINS,
    "chain": True,
    "chain_from": 0,
    "cert_mode": True,
    "split": True,
}


@dataclass(frozen=True, slots=True)
class Split:
    """Where a split cover's records are: the source's, and this repository's replay.

    The source's ``zmx2 cert --d4`` root log and the roots it leaves (``failing``), its
    ``zm_mixed.py`` sub-root records, one ``j<id>.jsonl`` per line of ``jobs``; the
    replay's root log and record directory; and the root log of ``zmx2`` run on the
    cover without its wall segments, where one was run.
    """

    zmx2: Path
    failing: Path
    zm_mixed: Path
    jobs: Path
    replay_zmx2: Path
    replay_zm_mixed: Path
    wall_control: Path | None = None
    #: The ``zmx2 cert`` header fields the source's run carries: ``zmx2.rs`` ``6b7f0f79``'s
    #: defaults, since the sources' ``verify.sh`` sets none of them.
    zmx2_settings: tuple[tuple[str, str], ...] = (
        ("depth", "40"),
        ("node_cap", "20000000"),
        ("kappa", "1.5"),
        ("K", "30"),
    )


@dataclass(frozen=True, slots=True)
class Whole:
    """Where a cover that ``zmx2`` decides whole keeps its runs, by mode.

    The source's ``zmx2 cert`` log in each mode it published, and this repository's
    replay's root log in the same mode.
    """

    source: tuple[tuple[str, Path], ...]
    replay: tuple[tuple[str, Path], ...]
    #: The ``zmx2 cert`` header fields the source's runs carry, as `Split.zmx2_settings`.
    zmx2_settings: tuple[tuple[str, str], ...] = (
        ("depth", "40"),
        ("node_cap", "20000000"),
        ("kappa", "1.5"),
        ("K", "30"),
    )

    def source_log(self, mode: str) -> Path | None:
        return dict(self.source).get(mode)

    def replay_log(self, mode: str) -> Path | None:
        return dict(self.replay).get(mode)


@dataclass(frozen=True, slots=True)
class Case:
    """One claim: the cover, the total the source states, and where the records live."""

    n: int
    side: int
    bundle: str
    cover: str
    total: Fraction
    points: int
    segments: int
    #: The source tree whose ``certificates/<bundle>/`` holds the cover and its records.
    source: Path = EVAND_0928
    #: The modes whose ``zmx2_<mode>/roots.log`` the bundle retains.
    zmx2_modes: tuple[str, ...] = ("d4", "full")
    #: Whether the bundle retains the ``zm_mixed_d4/roots.jsonl`` its manifest names.
    zm_mixed_records: bool = True
    #: The checker files, in `CHECKER_FILES` order; ``None``: ``checker/`` beside the records.
    checker: tuple[Path, ...] | None = None
    #: The manifest of a deeper ``zm_mixed.py`` run of part of the region, in the bundle.
    deep_manifest: str | None = None
    #: The ``atoms`` header value of the source's ``zmx2`` runs (``--pair-points``: pairpts).
    zmx2_atoms: str = "grid"
    #: Box totals the source states for ``zmx2`` runs whose logs it does not publish.
    zmx2_boxes_stated: tuple[tuple[str, int], ...] = ()
    #: The directory holding the cover where it is not ``source/certificates/<bundle>``.
    directory: Path | None = None
    #: A split cover's records (`Split`); ``None`` for a cover one checker decides whole.
    split: Split | None = None
    #: Where a cover ``zmx2`` decides whole keeps the source's logs and the replay's.
    whole: Whole | None = None

    @property
    def bundle_dir(self) -> Path:
        return self.directory or self.source / "certificates" / self.bundle

    @property
    def cover_path(self) -> Path:
        return self.bundle_dir / self.cover


#: The September 28 packet's two claims, with the totals and counts its READMEs state.
CASES = {
    21: Case(
        n=21,
        side=5,
        bundle="s21",
        cover="s21_mixed_cover_5.txt",
        total=Fraction(522368729933, 25 * 10**9),
        points=7536,
        segments=1872,
    ),
    45: Case(
        n=45,
        side=7,
        bundle="s45",
        cover="s45_mixed_cover_7.txt",
        total=Fraction(2238676387, 5 * 10**7),
        points=19989,
        segments=3912,
    ),
}
#: The 1 October imports, with the totals, counts and zmx2 box totals their READMEs state.
IMPORTED_CASES = {
    59: Case(
        n=59,
        side=8,
        bundle="k2m5_n59_L8",
        cover="n59_mixed_cover_8.txt",
        total=Fraction(1474762899, 25 * 10**6),
        points=26308,
        segments=5240,
        source=WAND125_1001,
        zmx2_modes=(),
        zm_mixed_records=False,
        checker=CHECKER_B91D70B6,
        deep_manifest="zm_mixed_root/manifest.json",
        zmx2_boxes_stated=(("d4", 9844124), ("full", 79108328)),
    ),
    60: Case(
        n=60,
        side=8,
        bundle="s60",
        cover="s60_mixed_cover_8.txt",
        total=Fraction(748233441, 125 * 10**5),
        points=23744,
        segments=5216,
        source=EVAND_1001,
        checker=CHECKER_08E8A5FA,
    ),
    77: Case(
        n=77,
        side=9,
        bundle="k2m4_n77_L9",
        cover="n77_mixed_cover_9.txt",
        total=Fraction(43347137744028965, 2**49),
        points=28273,
        segments=6420,
        source=WAND125_1001,
        zmx2_modes=(),
        zm_mixed_records=False,
        checker=CHECKER_B91D70B6,
        zmx2_atoms="pairpts",
        zmx2_boxes_stated=(("d4", 5810824), ("full", 46583600)),
    ),
}


def _split(packet: Path, n: int, zmx2_log: str) -> Split:
    """A Greff packet's layout: the source tree's ``records/`` and the intake's receipts."""
    records = packet / f"s{n}-certificate/records"
    receipts = packet / "receipts"
    return Split(
        zmx2=records / "zmx2" / zmx2_log,
        failing=records / "zmx2/failing_roots.txt",
        zm_mixed=records / "zm_mixed",
        jobs=records / "zm_mixed/jobs.txt",
        replay_zmx2=receipts / f"n{n}_zmx2_d4_roots.log",
        replay_zm_mixed=receipts / f"n{n}_zm_mixed",
        wall_control=receipts / f"controls/n{n}_control_nowall_zmx2_d4_roots.log",
    )


#: Benjamin Greff's covers of 14 and 15 October, with the totals and counts their READMEs
#: state. ``zmx2`` leaves 4 and 19 D4 roots, and ``zm_mixed.py`` certifies their 64 and 304
#: sub-roots; the checker files are the ones their ``verify.sh`` pins at evand ``b91d70b6``.
SPLIT_CASES = {
    76: Case(
        n=76,
        side=9,
        bundle="s76-certificate",
        cover="s76_cover_v5.txt",
        total=Fraction(3788361049, 5 * 10**7),
        points=41633,
        segments=9744,
        zmx2_modes=(),
        zm_mixed_records=False,
        checker=CHECKER_B91D70B6,
        directory=BENGREFF_S76 / "s76-certificate/cover",
        split=_split(BENGREFF_S76, 76, "zmx2_v5.log"),
    ),
    95: Case(
        n=95,
        side=10,
        bundle="s95-certificate",
        cover="s95_cover_v2.txt",
        total=Fraction(3791753447, 4 * 10**7),
        points=48352,
        segments=11438,
        zmx2_modes=(),
        zm_mixed_records=False,
        checker=CHECKER_B91D70B6,
        directory=BENGREFF_S95 / "s95-certificate/cover",
        split=_split(BENGREFF_S95, 95, "zmx2_s95_v2.log"),
    ),
}
#: Mohsen Khalili and Sara Gharabaghi's cover of 26 October, with the total and counts its
#: README states. ``zmx2`` at evand ``659ee62`` (``zmx2.rs`` ``e2bb84e9``) certifies every
#: root in both modes, so no ``zm_mixed.py`` record is part of the decision; the source's
#: ``zm_mixed.py`` records are a second checker's, read by the review, not here.
WHOLE_CASES = {
    44: Case(
        n=44,
        side=7,
        bundle="s44-equals-7",
        cover="s44_cover_7.txt",
        total=Fraction(2199755099, 5 * 10**7),
        points=15525,
        segments=3912,
        zmx2_modes=(),
        zm_mixed_records=False,
        directory=KHALILI_S44 / "s44-equals-7/certificate",
        whole=Whole(
            source=tuple(
                (mode, KHALILI_S44 / f"s44-equals-7/verification/logs/zmx2_{mode}.log")
                for mode in ("d4", "full")
            ),
            replay=tuple(
                (mode, KHALILI_S44 / f"receipts/n44_zmx2_{mode}_roots.log")
                for mode in ("d4", "full")
            ),
        ),
    ),
}
MIXED_CASES = {**CASES, **IMPORTED_CASES, **SPLIT_CASES, **WHOLE_CASES}
#: A cover in the plain point format, audited by ``cover`` alone: its sweeps are the
#: ``PointCoverRun`` below. Hosono's s(61) total is the one its ``provenance.json`` states.
POINT_ONLY_CASES = {
    61: Case(
        n=61,
        side=8,
        bundle="point_n61_L8",
        cover="cover.txt",
        total=Fraction(8584985072679551, 2**47),
        points=15193,
        segments=0,
        directory=WEB / "wand125-point-n61-2026-09-30/square-packing-bounds/point_n61_L8",
    )
}


def _stored(path: Path) -> Path:
    """The file that stores ``path``: itself, its ``.gz`` sibling, or its ``.xz`` sibling."""
    if path.is_file():
        return path
    packed = compressed_path(path)
    if packed.is_file():
        return packed
    xz = path.with_name(path.name + ".xz")
    return xz if xz.is_file() else path


def _unxz(path: Path, limit: int = MAX_DECOMPRESSED) -> bytes:
    """The bytes of an ``.xz`` file, every stream of it, bounded like a retained gzip."""
    data, out = path.read_bytes(), bytearray()
    while data.strip(b"\0"):
        decompressor = lzma.LZMADecompressor(format=lzma.FORMAT_XZ)
        out += decompressor.decompress(data, max_length=limit + 1 - len(out))
        if len(out) > limit:
            raise ValueError(f"{path} decompresses to more than {limit} bytes")
        if not decompressor.eof:
            raise ValueError(f"{path} ends inside an xz stream")
        data = decompressor.unused_data
    return bytes(out)


def read_record_bytes(path: Path) -> bytes:
    """A record's bytes: plain, deterministic gzip, or ``.xz`` as the source ships it."""
    stored = _stored(path)
    if stored.name.endswith(".xz"):
        return _unxz(stored)
    return read_retained_bytes(path)


def _exists(path: Path) -> bool:
    return _stored(path).is_file()


def _sha256(path: Path) -> str:
    return _digest(path, _stamp(path))


@functools.lru_cache(maxsize=64)
def _digest(path: Path, stamp: tuple[int, int]) -> str:
    del stamp
    return hashlib.sha256(read_record_bytes(path)).hexdigest()


def _display(path: Path) -> str:
    return str(path.relative_to(REPO)) if path.is_relative_to(REPO) else str(path)


# --- the cover -------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class MixedCover:
    """A mixed format v1 file as integers: side, denominators, points and segments."""

    side: Fraction
    denominator: int
    mass_denominator: int
    points: tuple[tuple[int, int, int], ...]
    segments: tuple[tuple[int, int, int, int, int], ...]
    polygons: int


def parse_cover(text: str) -> MixedCover:
    """Parse the format line by line; ``#`` starts a comment; every count must match."""
    rows = [line.split("#", 1)[0].split() for line in text.splitlines()]
    rows = [row for row in rows if row]
    if rows[0] == ["mixed", "1"]:
        values = [[int(token) for token in row] for row in rows[1:]]
    else:
        # The plain point format (``certificates/FORMAT.md``): mixed v1 with no
        # ``mixed 1`` line and neither segment nor polygon counts.
        values = [[int(token) for token in row] for row in rows] + [[0], [0]]

    def take(count: int, width: int) -> list[list[int]]:
        nonlocal values
        block, values = values[:count], values[count:]
        if len(block) != count or any(len(row) != width for row in block):
            raise ValueError(f"expected {count} rows of {width} integers")
        return block

    (side_num, side_den), (denominator,), (mass_denominator,) = take(1, 2)[0], *take(2, 1)
    (point_count,) = take(1, 1)[0]
    points = tuple((x, y, w) for x, y, w in take(point_count, 3))
    (segment_count,) = take(1, 1)[0]
    segments = tuple((a, b, c, d, w) for a, b, c, d, w in take(segment_count, 5))
    (polygon_count,) = take(1, 1)[0]
    if values[polygon_count:]:
        raise ValueError("trailing rows after the polygons")
    if side_den <= 0 or denominator <= 0 or mass_denominator <= 0:
        raise ValueError("denominators must be positive")
    return MixedCover(
        Fraction(side_num, side_den),
        denominator,
        mass_denominator,
        points,
        segments,
        polygon_count,
    )


Line = tuple[str, int]  # ("x", c): the vertical line x = c; ("y", c): the horizontal y = c.
Density = tuple[tuple[int, Fraction], ...]  # breakpoints along the line and density jumps


def _segment_line(segment: tuple[int, int, int, int, int]) -> tuple[Line, int, int]:
    x0, y0, x1, y1, _ = segment
    if x0 == x1 and y0 != y1:
        return ("x", x0), min(y0, y1), max(y0, y1)
    if y0 == y1 and x0 != x1:
        return ("y", y0), min(x0, x1), max(x0, x1)
    raise ValueError(f"segment is not axis-parallel with positive length: {segment}")


def line_densities(segments: tuple[tuple[int, int, int, int, int], ...]) -> dict[Line, Density]:
    """Each line's segment measure as a canonical piecewise-constant density.

    A segment of mass ``w`` and length ``L`` has density ``w / L`` on its extent; the
    measure on a line is the sum, recorded as sorted breakpoints with nonzero jumps, so
    two segment families define the same measure exactly when these agree.
    """
    jumps: dict[Line, defaultdict[int, Fraction]] = defaultdict(lambda: defaultdict(Fraction))
    for segment in segments:
        line, lo, hi = _segment_line(segment)
        rate = Fraction(segment[4], hi - lo)
        jumps[line][lo] += rate
        jumps[line][hi] -= rate
    out: dict[Line, Density] = {}
    for line, table in jumps.items():
        canonical = tuple((t, v) for t, v in sorted(table.items()) if v)
        if canonical:
            out[line] = canonical
    return out


def _reflect_density(density: Density, edge: int) -> Density:
    return tuple(sorted((edge - t, -v) for t, v in density))


def audit_cover(case: Case, path: Path | None = None) -> dict[str, Any]:
    """Everything about the cover that is decided without a sweep."""
    path = path or case.cover_path
    data = read_record_bytes(path)
    cover = parse_cover(data.decode("ascii"))
    edge_fraction = cover.side * cover.denominator
    if edge_fraction.denominator != 1:
        raise ValueError("the side is not a multiple of 1/D")
    edge = edge_fraction.numerator
    problems: list[str] = []
    for x, y, w in cover.points:
        if not (0 <= x <= edge and 0 <= y <= edge and w >= 0):
            problems.append(f"point out of range or negative: {(x, y, w)}")
    lengths: Counter[int] = Counter()
    for segment in cover.segments:
        x0, y0, x1, y1, w = segment
        if not all(0 <= v <= edge for v in (x0, y0, x1, y1)) or w < 0:
            problems.append(f"segment out of range or negative: {segment}")
        _, lo, hi = _segment_line(segment)
        lengths[hi - lo] += 1
    point_mass = Fraction(sum(w for _, _, w in cover.points), cover.mass_denominator)
    segment_mass = Fraction(sum(s[4] for s in cover.segments), cover.mass_denominator)
    total = point_mass + segment_mass

    weights: Counter[tuple[int, int]] = Counter()
    for x, y, w in cover.points:
        weights[(x, y)] += w
    entries: Counter[tuple[tuple[int, int], tuple[int, int], int]] = Counter()
    for x0, y0, x1, y1, w in cover.segments:
        a, b = sorted(((x0, y0), (x1, y1)))
        entries[(a, b, w)] += 1

    def reflect(p: tuple[int, int]) -> tuple[int, int]:
        return (edge - p[0], p[1])

    def swap(p: tuple[int, int]) -> tuple[int, int]:
        return (p[1], p[0])

    def mapped_entries(g: Any) -> Counter[tuple[tuple[int, int], tuple[int, int], int]]:
        image: Counter[tuple[tuple[int, int], tuple[int, int], int]] = Counter()
        for (a, b, w), count in entries.items():
            ga, gb = sorted((g(a), g(b)))
            image[(ga, gb, w)] += count
        return image

    points_invariant = weights == Counter({reflect(p): w for p, w in weights.items()}) and (
        weights == Counter({swap(p): w for p, w in weights.items()})
    )
    entries_invariant = entries == mapped_entries(reflect) and entries == mapped_entries(swap)
    density = line_densities(cover.segments)
    reflected: dict[Line, Density] = {}
    swapped: dict[Line, Density] = {}
    for (axis, c), d in density.items():
        # x -> edge - x moves the vertical line x = c to x = edge - c and reverses the
        # horizontal lines' parameter; x <-> y exchanges the two families.
        reflected[("x", edge - c) if axis == "x" else ("y", c)] = (
            d if axis == "x" else _reflect_density(d, edge)
        )
        swapped[("y" if axis == "x" else "x", c)] = d
    measure_invariant = points_invariant and density == reflected and density == swapped

    vertical = {c for axis, c in density if axis == "x"}
    horizontal = {c for axis, c in density if axis == "y"}
    on_lines = sum(1 for x, y, _ in cover.points if x in vertical or y in horizontal)
    return {
        "cover": _display(path),
        "sha256": hashlib.sha256(data).hexdigest(),
        "side": str(cover.side),
        "coordinate_denominator": cover.denominator,
        "mass_denominator": cover.mass_denominator,
        "points": len(cover.points),
        "segments": len(cover.segments),
        "polygons": cover.polygons,
        "lines_carrying_segments": {
            "x": sorted(Fraction(c, cover.denominator).__str__() for c in vertical),
            "y": sorted(Fraction(c, cover.denominator).__str__() for c in horizontal),
        },
        "segment_lengths": {
            str(Fraction(length, cover.denominator)): count
            for length, count in sorted(lengths.items())
        },
        "point_mass": str(point_mass),
        "segment_mass": str(segment_mass),
        "total": str(total),
        "total_decimal": f"{float(total):.9f}",
        "total_equals_stated": total == case.total,
        "total_below_n": total < case.n,
        "counts_as_stated": (len(cover.points), len(cover.segments))
        == (case.points, case.segments),
        "d4_invariant_entry_by_entry": points_invariant and entries_invariant,
        "d4_invariant_as_measure": measure_invariant,
        "points_on_segment_lines": on_lines,
        "problems": problems,
    }


def cover_clean(result: dict[str, Any]) -> bool:
    return (
        not result["problems"]
        and result["polygons"] == 0
        and result["total_equals_stated"]
        and result["total_below_n"]
        and result["counts_as_stated"]
        and result["d4_invariant_entry_by_entry"]
        and result["d4_invariant_as_measure"]
        and result["points_on_segment_lines"] == 0
    )


# --- zmx2 logs ---------------------------------------------------------------------------

#: A ``ROOT`` line exactly as ``zmx2 cert`` writes it. Any other line starting ``ROOT``,
#: such as one torn by a killed run and continued by its resume, is counted unparsed.
ZMX2_ROOT_LINE = re.compile(
    r"ROOT (\d+) pass (\d+) root (\S+) boxes (\d+) cert (\d+) empty (\d+) uncert (\d+) "
    r"maxdepth (\d+) capped ([01]) ms (\d+)"
)
#: The header's ``region`` value: the ``--xlo``-``--xhi``, ``--ylo``-``--yhi`` and
#: ``--bins`` limits of the run, as centre-cell and ``u``-bin indices.
ZMX2_REGION = re.compile(r"x(\d+)-(\d+),y(\d+)-(\d+),bins(\d+)-(\d+)")
#: What a comparison leaves out, and why.
ZMX2_NOT_COMPARED = {
    "region": (
        "the header field naming the run's limits: a replay joined from region runs, or "
        "a partial re-sweep, names its own; the zmx2 command audits their union"
    ),
    "ms": "each ROOT line's wall-clock time",
}

Zmx2Key = tuple[int, str]  # (pass, root) as the log writes them


@dataclass(frozen=True, slots=True)
class Zmx2Run:
    """One run in a log: its header line and the roots recorded under it."""

    log: Path
    #: The header's line number, from 1; 0 for ROOT lines above any header.
    line: int
    header: str
    roots: tuple[Zmx2Key, ...]


@dataclass(frozen=True, slots=True)
class Zmx2Log:
    """One or more ``zmx2 cert`` logs read as one record: runs, and each root's census."""

    paths: tuple[Path, ...]
    runs: tuple[Zmx2Run, ...]
    #: Each root's census at its first ROOT line, in `ZMX2_CENSUS` order.
    census: dict[Zmx2Key, tuple[int, ...]]
    ids: dict[Zmx2Key, int]
    #: A root recorded again after its first ROOT line, once per further line.
    repeated: tuple[Zmx2Key, ...]
    uncert_lines: int
    unparsed_lines: int

    @property
    def header(self) -> str:
        return self.runs[0].header if self.runs else ""


def _stamp(path: Path) -> tuple[int, int]:
    """Size and mtime of the stored file, so a cached parse is dropped when it changes."""
    status = _stored(path).stat()
    return status.st_size, status.st_mtime_ns


def read_zmx2(paths: Path | Sequence[Path]) -> Zmx2Log:
    """The logs at ``paths``, in that order, as one record.

    A file may hold several runs joined end to end, each under the header its run wrote;
    a root recorded twice, in one file or across two, is listed in ``repeated``. Parses
    are cached per file state; callers treat the returned mappings as read-only.
    """
    logs = [_read_zmx2(path, _stamp(path)) for path in _as_paths(paths)]
    if not logs:
        raise ValueError("no zmx2 log named")
    if len(logs) == 1:
        return logs[0]
    census: dict[Zmx2Key, tuple[int, ...]] = {}
    ids: dict[Zmx2Key, int] = {}
    repeated: list[Zmx2Key] = []
    for log in logs:
        repeated.extend(log.repeated)
        for key, row in log.census.items():
            if key in census:
                repeated.append(key)
            else:
                census[key], ids[key] = row, log.ids[key]
    return Zmx2Log(
        tuple(path for log in logs for path in log.paths),
        tuple(run for log in logs for run in log.runs),
        census,
        ids,
        tuple(repeated),
        sum(log.uncert_lines for log in logs),
        sum(log.unparsed_lines for log in logs),
    )


def _as_paths(paths: Path | Sequence[Path]) -> tuple[Path, ...]:
    return (paths,) if isinstance(paths, Path) else tuple(paths)


@functools.lru_cache(maxsize=16)
def _read_zmx2(path: Path, stamp: tuple[int, int]) -> Zmx2Log:
    del stamp
    runs: list[Zmx2Run] = []
    header, start, roots = "", 0, list[Zmx2Key]()
    census: dict[Zmx2Key, tuple[int, ...]] = {}
    ids: dict[Zmx2Key, int] = {}
    repeated: list[Zmx2Key] = []
    uncert_lines = unparsed = 0
    lines = read_record_bytes(path).decode("ascii").splitlines()
    for number, line in enumerate(lines, start=1):
        if line.startswith("# zmx2 cert "):
            if header or roots:
                runs.append(Zmx2Run(path, start, header, tuple(roots)))
            header, start, roots = line, number, []
        elif line.startswith("UNCERT "):
            uncert_lines += 1
        elif (match := ZMX2_ROOT_LINE.fullmatch(line)) is not None:
            key = (int(match[2]), match[3])
            roots.append(key)
            if key in census:
                repeated.append(key)
            else:
                census[key] = tuple(int(match[i]) for i in range(4, 10))
                ids[key] = int(match[1])
        elif line.strip():
            unparsed += 1
    if header or roots:
        runs.append(Zmx2Run(path, start, header, tuple(roots)))
    return Zmx2Log((path,), tuple(runs), census, ids, tuple(repeated), uncert_lines, unparsed)


def zmx2_cells(side: int, mode: str) -> int:
    """Centre cells per axis: the swept span over the pitch, which must divide it."""
    cells = (Fraction(side, 2) if mode == "d4" else Fraction(side)) / ZMX2_PITCH
    if cells.denominator != 1:
        raise ValueError(f"side {side} is not a multiple of the {mode} pitch")
    return cells.numerator


def zmx2_roots(side: int, mode: str) -> dict[Zmx2Key, int]:
    """The region's roots as ``zmx2`` writes them, each with the id ``zmx2`` gives it."""
    cells = zmx2_cells(side, mode)
    passes = (0,) if mode == "d4" else (0, 1)
    d, b = ZMX2_PITCH.denominator, 2 * ZMX2_BINS
    return {
        (p, f"{i}/{d},{i + 1}/{d},{j}/{d},{j + 1}/{d},{k}/{b},{k + 1}/{b}"): (
            ((p * cells + i) * cells + j) * ZMX2_BINS + k
        )
        for p in passes
        for i in range(cells)
        for j in range(cells)
        for k in range(ZMX2_BINS)
    }


def zmx2_region(side: int, mode: str) -> set[Zmx2Key]:
    return set(zmx2_roots(side, mode))


def zmx2_limits(value: str, cells: int) -> tuple[int, ...] | None:
    """A header ``region`` as ``(x0, x1, y0, y1, b0, b1)``, or ``None`` unless it is
    well formed and within ``cells`` centre cells and the ``u`` bins."""
    match = ZMX2_REGION.fullmatch(value)
    if match is None:
        return None
    limits = tuple(int(v) for v in match.groups())
    x0, x1, y0, y1, b0, b1 = limits
    inside = x1 < cells and y1 < cells and b1 < ZMX2_BINS
    return limits if inside and x0 <= x1 and y0 <= y1 and b0 <= b1 else None


def _within(root_id: int, cells: int, limits: tuple[int, ...]) -> bool:
    """Whether the root ``zmx2`` numbers ``root_id`` lies in a run's limits."""
    cell, k = divmod(root_id, ZMX2_BINS)
    i, j = divmod(cell % (cells * cells), cells)
    x0, x1, y0, y1, b0, b1 = limits
    return x0 <= i <= x1 and y0 <= j <= y1 and b0 <= k <= b1


def parse_zmx2_header(header: str) -> tuple[dict[str, str], list[str]]:
    """The header's ``key=value`` fields, and every token this tool does not know."""
    fields: dict[str, str] = {}
    unknown: list[str] = []
    for token in header.split()[3:]:
        key, sep, value = token.partition("=")
        if sep and key in ZMX2_HEADER_FIELDS and key not in fields:
            fields[key] = value
        else:
            unknown.append(token)
    base, *suffixes = fields.get("atoms", "").split("+")
    if base not in ZMX2_ATOM_BASES or any(s not in ZMX2_ATOM_SUFFIXES for s in suffixes):
        unknown.append(f"atoms={fields.get('atoms', '')}")
    return fields, unknown


def _apart_from_region(header: str) -> str:
    return " ".join(token for token in header.split() if not token.startswith("region="))


def zmx2_flags(atoms: str) -> dict[str, bool]:
    """The command-line flags an ``atoms`` header value records."""
    base, *suffixes = atoms.split("+")
    flags = {"pair_points": base == "pairpts", "no_atoms": base == "none"}
    flags.update({flag: suffix in suffixes for suffix, flag in ZMX2_ATOM_SUFFIXES.items()})
    return flags


def _files(log: Zmx2Log, name: str = "log") -> dict[str, Any]:
    """The file a record was read from and its digest, or each file's when several."""
    files = [{"path": _display(p), "sha256": _sha256(p)} for p in log.paths]
    if len(files) != 1:
        return {f"{name}s": files}
    digest = "sha256" if name == "log" else f"{name}_sha256"
    return {name: files[0]["path"], digest: files[0]["sha256"]}


def _runs(log: Zmx2Log) -> list[dict[str, Any]]:
    return [
        {
            "log": _display(run.log),
            "line": run.line,
            "region": parse_zmx2_header(run.header)[0].get("region"),
            "roots": len(run.roots),
        }
        for run in log.runs
    ]


def audit_zmx2(
    case: Case | PointCoverRun, paths: Path | Sequence[Path], mode: str
) -> dict[str, Any]:
    """A log, or several read as one, against the region the side and mode derive.

    Several runs, in one file or several, are one record when every header is the same
    apart from ``region``, each run's roots lie within the limits its header names, and
    their union is the region with each root once.
    """
    log = read_zmx2(paths)
    roots = zmx2_roots(case.side, mode)
    cells = zmx2_cells(case.side, mode)
    present = roots.keys() & log.census.keys()
    parsed = [parse_zmx2_header(run.header) for run in log.runs]
    fields = parsed[0][0] if parsed else {}
    unknown = sorted({token for _, tokens in parsed for token in tokens})
    limits = [zmx2_limits(f.get("region", ""), cells) for f, _ in parsed]
    outside_run = sum(
        1
        for run, bound in zip(log.runs, limits, strict=True)
        for key in run.roots
        if key in roots and (bound is None or not _within(roots[key], cells, bound))
    )
    census = list(log.census.values())

    def total(name: str) -> int:
        index = ZMX2_CENSUS.index(name)
        return sum(row[index] for row in census)

    result: dict[str, Any] = {
        **_files(log),
        "header": log.header,
        "mode": mode,
        "atoms": fields.get("atoms", ""),
        "flags": zmx2_flags(fields.get("atoms", "")),
        "header_settings": {
            k: fields[k] for k in ("depth", "node_cap", "kappa", "K") if k in fields
        },
        "header_unrecognised": unknown,
        "headers_equal_apart_from_region": len(
            {_apart_from_region(run.header) for run in log.runs}
        )
        == 1,
        "mode_in_header": bool(parsed) and all(f.get("mode") == mode for f, _ in parsed),
        "region_in_header": bool(limits) and all(bound is not None for bound in limits),
        "joined": len(log.runs) > 1,
        "runs": _runs(log),
        "roots_in_region": len(roots),
        "roots_present": len(present),
        "roots_missing": len(roots.keys() - log.census.keys()),
        "roots_outside_region": len(log.census.keys() - roots.keys()),
        "roots_outside_their_runs_limits": outside_run,
        "roots_recorded_more_than_once": len(log.repeated),
        "repeated_roots": [f"pass {p} root {r}" for p, r in log.repeated[:20]],
        "root_ids_inconsistent": sum(1 for key in present if log.ids[key] != roots[key]),
        "unparsed_lines": log.unparsed_lines,
        "boxes": total("boxes"),
        "certified_leaves": total("cert"),
        "empty_leaves": total("empty"),
        "uncertified_boxes": total("uncert"),
        "uncert_lines": log.uncert_lines,
        "capped_roots": total("capped"),
        "max_depth": max((row[ZMX2_CENSUS.index("maxdepth")] for row in census), default=0),
    }
    if isinstance(case, Case):
        # What the source's own run recorded, where it publishes no log: informational,
        # since a run with other atoms that certifies every root verifies the cover too.
        result["atoms_source_ran"] = case.zmx2_atoms
        result["atoms_as_source_ran"] = result["atoms"] == case.zmx2_atoms
        stated = dict(case.zmx2_boxes_stated).get(mode)
        if stated is not None:
            result["boxes_stated_by_source"] = stated
            result["boxes_equal_source_statement"] = result["boxes"] == stated
    return result


def zmx2_clean(result: dict[str, Any]) -> bool:
    return (
        result["mode_in_header"]
        and result["region_in_header"]
        and not result["header_unrecognised"]
        and result["headers_equal_apart_from_region"]
        and result["roots_present"] == result["roots_in_region"]
        and result["roots_outside_region"] == 0
        and result["roots_outside_their_runs_limits"] == 0
        and result["roots_recorded_more_than_once"] == 0
        and result["root_ids_inconsistent"] == 0
        and result["unparsed_lines"] == 0
        and result["uncertified_boxes"] == 0
        and result["uncert_lines"] == 0
        and result["capped_roots"] == 0
        and result.get("atoms_as_required", True)
    )


def require_atoms(result: dict[str, Any], atoms: str | None) -> dict[str, Any]:
    """Record whether the header's ``atoms`` is the one required; ``None`` requires none."""
    if atoms is not None:
        result["atoms_required"] = atoms
        result["atoms_as_required"] = result["atoms"] == atoms
    return result


def zmx2_comparison_clean(result: dict[str, Any]) -> bool:
    """Every compared root's census equal, each root once, the same header apart from region."""
    return (
        comparison_clean(result)
        and result["headers_equal"]
        and result["root_ids_differ"] == 0
        and result["replay_roots_recorded_more_than_once"] == 0
        and result["shipped_roots_recorded_more_than_once"] == 0
        and result["replay_uncert_lines"] == result["shipped_uncert_lines"]
        and result["replay_unparsed_lines"] == result["shipped_unparsed_lines"] == 0
    )


def compare_zmx2(shipped: Path, replays: Path | Sequence[Path]) -> dict[str, Any]:
    """Root for root against a reference log; ``replays`` may be several, or joined, runs.

    ``headers_equal`` compares every header field but ``region`` (see `ZMX2_NOT_COMPARED`);
    ``headers_identical`` compares the whole line.
    """
    source_log, replay_log = read_zmx2(shipped), read_zmx2(replays)
    source, fresh = source_log.census, replay_log.census
    common = fresh.keys() & source.keys()
    differ = sorted(key for key in common if fresh[key] != source[key])
    reference = {_apart_from_region(run.header) for run in source_log.runs}
    replayed = {_apart_from_region(run.header) for run in replay_log.runs}
    lines = {run.header for run in (*source_log.runs, *replay_log.runs)}
    return {
        "shipped": _display(shipped),
        "shipped_sha256": _sha256(shipped),
        **_files(replay_log, "replay"),
        "replay_runs": _runs(replay_log),
        "not_compared": ZMX2_NOT_COMPARED,
        "headers_equal": len(reference) == 1 and replayed == reference,
        "headers_identical": len(lines) == 1,
        "shipped_roots": len(source),
        "replay_roots": len(fresh),
        "roots_compared": len(common),
        "roots_identical": len(common) - len(differ),
        "roots_whose_census_differs": [f"pass {p} root {r}" for p, r in differ[:50]],
        "root_ids_differ": sum(
            1 for key in common if source_log.ids[key] != replay_log.ids[key]
        ),
        "replay_roots_recorded_more_than_once": len(replay_log.repeated),
        "shipped_roots_recorded_more_than_once": len(source_log.repeated),
        "replay_roots_not_in_shipped": len(fresh.keys() - source.keys()),
        "shipped_roots_not_replayed": len(source.keys() - fresh.keys()),
        "shipped_uncert_lines": source_log.uncert_lines,
        "replay_uncert_lines": replay_log.uncert_lines,
        "shipped_unparsed_lines": source_log.unparsed_lines,
        "replay_unparsed_lines": replay_log.unparsed_lines,
    }


#: A ``zmx2`` run manifest's statements about its log, as the source's run scripts write
#: them (``search/s60_cert_runs.sh``, ``search/zmx2_sym_run.sh``).
ZMX2_MANIFEST_HEADER = re.compile(r"^log header:\s+(# zmx2 cert .*?)\s*$", re.MULTILINE)
ZMX2_MANIFEST_LOG = re.compile(
    r"^log sha256:\s+([0-9a-f]{64})\s+\((\d+) ROOT lines, (\d+) UNCERT lines\)", re.MULTILINE
)
ZMX2_MANIFEST_TOTALS = re.compile(
    r"roots (\d+) \(missing (\d+)\), boxes (\d+), certified (\d+), empty (\d+), "
    r"uncertified (\d+), max depth (\d+)"
)
ZMX2_MANIFEST_VERDICT = re.compile(r"\b(VERIFIED(?:-D4)?):")


def audit_zmx2_manifest(
    manifest: Path, log_path: Path, audited: dict[str, Any]
) -> dict[str, Any]:
    """A source's ``manifest.txt`` against the log it names and that log's audit."""
    text = read_record_bytes(manifest).decode("utf-8")
    log = read_zmx2(log_path)
    header = ZMX2_MANIFEST_HEADER.search(text)
    stated_log = ZMX2_MANIFEST_LOG.search(text)
    totals = ZMX2_MANIFEST_TOTALS.search(text)
    verdict = ZMX2_MANIFEST_VERDICT.search(text)
    lines = sum(len(run.roots) for run in log.runs)
    audited_totals = tuple(
        audited[k]
        for k in (
            "roots_in_region",
            "roots_missing",
            "boxes",
            "certified_leaves",
            "empty_leaves",
            "uncertified_boxes",
            "max_depth",
        )
    )
    report = {
        "manifest": _display(manifest),
        "header_as_stated": header is not None and header[1] == log.header,
        "log_sha256_as_stated": stated_log is not None and stated_log[1] == _sha256(log_path),
        "lines_as_stated": stated_log is not None
        and (int(stated_log[2]), int(stated_log[3])) == (lines, log.uncert_lines),
        "totals_as_stated": totals is not None
        and tuple(int(v) for v in totals.groups()) == audited_totals,
        "verdict_stated": verdict[1] if verdict else None,
    }
    expected = "VERIFIED-D4" if audited["mode"] == "d4" else "VERIFIED"
    report["consistent"] = (
        all(
            report[k]
            for k in (
                "header_as_stated",
                "log_sha256_as_stated",
                "lines_as_stated",
                "totals_as_stated",
            )
        )
        and report["verdict_stated"] == expected
    )
    return report


# --- zm_mixed.py records -----------------------------------------------------------------


def read_zm_mixed(path: Path) -> tuple[dict[str, Any], dict[tuple[str, ...], dict[str, Any]]]:
    """The header line and each root's record; a torn last line is skipped.

    Parses are cached per file state; callers treat the returned mappings as read-only.
    """
    return _read_zm_mixed(path, _stamp(path))


@functools.lru_cache(maxsize=16)
def _read_zm_mixed(
    path: Path, stamp: tuple[int, int]
) -> tuple[dict[str, Any], dict[tuple[str, ...], dict[str, Any]]]:
    del stamp
    lines = [line for line in read_record_bytes(path).decode("utf-8").splitlines() if line]
    header = json.loads(lines[0])
    if header.get("kind") != "zm_mixed cert header":
        raise ValueError(f"{path}: the first line is not a zm_mixed header")
    records: dict[tuple[str, ...], dict[str, Any]] = {}
    for index, line in enumerate(lines[1:], start=2):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            if index == len(lines):
                continue
            raise
        key = tuple(record["root"])
        if key in records:
            raise ValueError(f"{path}: root {key} recorded twice")
        records[key] = record
    return header, records


def zm_mixed_region(
    side: int, region: Mapping[str, str | None] | None = None
) -> set[tuple[str, ...]]:
    """The D4 root grid over ``[0, side/2]^2 x [0, 1/2]``, or its roots meeting ``region``.

    A root is kept as ``zm_mixed.py`` keeps it: unless it lies on or beyond a bound, so
    a region aligned with the grid keeps exactly the roots inside it, whole.
    """
    cells = Fraction(side, 2) / ZM_MIXED_PITCH
    if cells.denominator != 1:
        raise ValueError(f"side {side} is not a multiple of the zm_mixed pitch")
    xs = [ZM_MIXED_PITCH * i for i in range(cells.numerator + 1)]
    us = [Fraction(k, 2 * ZM_MIXED_BINS) for k in range(ZM_MIXED_BINS + 1)]
    bounds = region or {}

    def kept(name: str, edges: list[Fraction]) -> list[int]:
        lo, hi = bounds.get(f"{name}_lo"), bounds.get(f"{name}_hi")
        return [
            i
            for i in range(len(edges) - 1)
            if (lo is None or edges[i + 1] > Fraction(lo))
            and (hi is None or edges[i] < Fraction(hi))
        ]

    return {
        (str(xs[i]), str(xs[i + 1]), str(xs[j]), str(xs[j + 1]), str(us[k]), str(us[k + 1]))
        for i in kept("cx", xs)
        for j in kept("cy", xs)
        for k in kept("u", us)
    }


def _census(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record["st"].items() if key != "cpu"}


def _differs(replay: dict[str, Any], source: dict[str, Any]) -> bool:
    """A root's leaf census or its uncertified boxes differ; CPU time is not compared."""
    return _census(replay) != _census(source) or replay["unc"] != source["unc"]


def checker_paths(
    case: Case, records: Path, checker_dir: Path | None = None
) -> dict[str, Path]:
    """The checker files a record must name: ``checker_dir``, the case's, or beside it."""
    if checker_dir is not None:
        return {name: checker_dir / name for name in CHECKER_FILES}
    if case.checker is not None:
        return dict(zip(CHECKER_FILES, case.checker, strict=True))
    return {name: records.parent / "checker" / name for name in CHECKER_FILES}


def _expected_digests(case: Case, checker: Mapping[str, Path]) -> dict[str, str]:
    expected = {name: _sha256(path) for name, path in checker.items()}
    expected["input"] = _sha256(case.cover_path)
    return expected


def _uncertified(record: dict[str, Any]) -> bool:
    return bool(record["st"]["UNCERT"] or record["unc"])


def audit_zm_mixed(case: Case, path: Path, checker_dir: Path | None = None) -> dict[str, Any]:
    header, records = read_zm_mixed(path)
    expected = _expected_digests(case, checker_paths(case, path, checker_dir))
    settings = header["settings"]
    region = zm_mixed_region(case.side)
    leaves: Counter[str] = Counter()
    max_depth = 0
    uncertified_roots = []
    cpu: list[float] = []
    for key, record in records.items():
        census = _census(record)
        max_depth = max(max_depth, census.pop("maxdepth"))
        leaves.update(census)
        cpu.append(float(record["st"]["cpu"]))
        if _uncertified(record):
            uncertified_roots.append(",".join(key))
    cpu.sort()
    return {
        "records": _display(path),
        "sha256": _sha256(path),
        "header_sha256_match_retained_files": header["sha256"] == expected,
        "header_total": header["total"],
        "header_total_equals_stated": Fraction(header["total"]) == case.total,
        "settings_as_required": all(settings.get(k) == v for k, v in ZM_MIXED_SETTINGS.items()),
        "region_unrestricted": not any(settings.get("region", {}).values()),
        "roots_in_region": len(region),
        "roots_present": len(region & records.keys()),
        "roots_missing": len(region - records.keys()),
        "roots_outside_region": len(records.keys() - region),
        "uncertified_roots": uncertified_roots[:50],
        "uncertified_root_count": len(uncertified_roots),
        "census": dict(sorted({**leaves, "maxdepth": max_depth}.items())),
        "cpu_seconds": round(sum(cpu), 1),
        "cpu_seconds_per_root_quantiles": {
            q: round(cpu[min(len(cpu) - 1, int(q * len(cpu)))], 3)
            for q in (0.5, 0.9, 0.99, 1.0)
        }
        if cpu
        else {},
    }


def _complete_run_sound(result: dict[str, Any]) -> bool:
    """A complete run's record is what it must be, uncertified boxes apart."""
    return (
        result["header_sha256_match_retained_files"]
        and result["header_total_equals_stated"]
        and result["settings_as_required"]
        and result["region_unrestricted"]
        and result["roots_present"] == result["roots_in_region"]
        and result["roots_outside_region"] == 0
    )


def zm_mixed_clean(result: dict[str, Any]) -> bool:
    return (
        _complete_run_sound(result)
        and not result["uncertified_roots"]
        and result["census"].get("UNCERT", 0) == 0
    )


def _settings_apart_from(header: dict[str, Any], keys: Sequence[str]) -> dict[str, Any]:
    return {k: v for k, v in header["settings"].items() if k not in keys}


def _box_inside(box: Sequence[str], root: Sequence[str]) -> bool:
    """A box ``(x0, x1, y0, y1, u0, u1)`` lies in the closed root of the same shape."""
    b, r = [Fraction(v) for v in box], [Fraction(v) for v in root]
    return len(b) == len(r) == 6 and all(
        r[2 * i] <= b[2 * i] <= b[2 * i + 1] <= r[2 * i + 1] for i in range(3)
    )


def audit_deep_zm_mixed(
    case: Case, complete: dict[str, Any], path: Path
) -> tuple[dict[str, Any], set[tuple[str, ...]]]:
    """A deeper run of part of the region, against the complete run's header.

    Returns the report and the roots it certifies: all its roots when it is clean (same
    checker files, cover and settings apart from ``depth`` and ``region``, complete over
    its region, no uncertified box), none otherwise.
    """
    header, records = read_zm_mixed(path)
    region = {k: v for k, v in header["settings"].get("region", {}).items() if v is not None}
    declared = zm_mixed_region(case.side, region)
    uncertified = sorted(",".join(k) for k, record in records.items() if _uncertified(record))
    report = {
        "records": _display(path),
        "header_sha256_equal_complete_run": header["sha256"] == complete["sha256"],
        "header_total_equal_complete_run": header["total"] == complete["total"],
        "settings_equal_apart_from_depth_and_region": _settings_apart_from(
            header, ("depth", "region")
        )
        == _settings_apart_from(complete, ("depth", "region")),
        "depth": header["settings"].get("depth"),
        "region": region,
        "roots_in_region": len(declared),
        "roots_present": len(declared & records.keys()),
        "roots_missing": len(declared - records.keys()),
        "roots_outside_region": len(records.keys() - declared),
        "uncertified_roots": uncertified[:50],
    }
    clean = (
        report["header_sha256_equal_complete_run"]
        and report["header_total_equal_complete_run"]
        and report["settings_equal_apart_from_depth_and_region"]
        and bool(region)
        and bool(declared)
        and report["roots_missing"] == 0
        and report["roots_outside_region"] == 0
        and not uncertified
    )
    report["clean"] = clean
    return report, set(records) if clean else set()


def audit_zm_mixed_composite(
    case: Case, complete: Path, deep: Sequence[Path], checker_dir: Path | None = None
) -> dict[str, Any]:
    """A complete run with uncertified boxes, and deeper runs of the roots that hold them.

    Clean only if the complete run is sound apart from its uncertified boxes and every
    root holding one is a root a clean deeper run certifies whole.
    """
    result = audit_zm_mixed(case, complete, checker_dir)
    header, records = read_zm_mixed(complete)
    open_roots = {key: record for key, record in records.items() if _uncertified(record)}
    boxes = [(key, box) for key, record in open_roots.items() for box in record["unc"]]
    certified: set[tuple[str, ...]] = set()
    runs = []
    for path in deep:
        report, roots = audit_deep_zm_mixed(case, header, path)
        runs.append(report)
        certified |= roots
    uncovered = sorted(",".join(key) for key in open_roots.keys() - certified)
    inside = all(_box_inside(box, key) for key, box in boxes)
    # Whether these are the records the source's manifests name, where it has them; a
    # replay's are not, since they carry its own CPU times.
    named = [_records_named(case.bundle_dir / "zm_mixed_d4/manifest.json", complete)]
    if case.deep_manifest is not None:
        deep_named = case.bundle_dir / case.deep_manifest
        named += [_records_named(deep_named, path) for path in deep]
    return {
        "complete_run": result,
        "deep_runs": runs,
        "records_named_by_source_manifests": named,
        "uncertified_roots_of_complete_run": sorted(",".join(key) for key in open_roots)[:50],
        "uncertified_boxes_listed": len(boxes),
        "uncertified_boxes_inside_their_roots": inside,
        "uncertified_roots_not_certified_by_a_deep_run": uncovered[:50],
        "composite_clean": _complete_run_sound(result)
        and all(run["clean"] for run in runs)
        and inside
        and not uncovered,
    }


def _records_named(manifest: Path, records: Path) -> dict[str, Any]:
    """Whether a manifest names ``records`` by digest; ``None`` without the manifest."""
    named = (
        json.loads(read_record_bytes(manifest))["records"]["sha256"]
        if _exists(manifest)
        else None
    )
    return {
        "records": _display(records),
        "manifest": _display(manifest),
        "sha256_as_named": None if named is None else named == _sha256(records),
    }


def audit_zm_mixed_manifest(
    case: Case, manifest: Path, checker_dir: Path | None = None
) -> tuple[dict[str, Any], dict[str, Any]]:
    """What one ``zm_mixed.py`` manifest states, and its header line.

    Its records are read only if retained beside it.
    """
    data = json.loads(read_record_bytes(manifest))
    header, result = data["header"], data["result"]
    settings = header["settings"]
    region = {k: v for k, v in settings.get("region", {}).items() if v is not None}
    records = manifest.parent / "roots.jsonl"
    expected = _expected_digests(case, checker_paths(case, records, checker_dir))
    report: dict[str, Any] = {
        "manifest": _display(manifest),
        "header_sha256_match_retained_files": header["sha256"] == expected,
        "header_total_equals_stated": Fraction(header["total"]) == case.total,
        "settings_as_required_apart_from_depth": all(
            settings.get(k) == v for k, v in ZM_MIXED_SETTINGS.items() if k != "depth"
        ),
        "depth": settings.get("depth"),
        "region": region,
        "roots_in_declared_region": len(zm_mixed_region(case.side, region)),
        "roots_stated": result["roots"],
        "uncertified_boxes_stated": result["census"]["UNCERT"],
        "verdict_stated": result["verdict"],
        "records_retained": _exists(records),
    }
    if report["records_retained"]:
        report["records_match_manifest"] = _sha256(records) == data["records"]["sha256"]
        report["manifest_header_equals_records_header"] = read_zm_mixed(records)[0] == header
    report["consistent"] = (
        report["header_sha256_match_retained_files"]
        and report["header_total_equals_stated"]
        and report["settings_as_required_apart_from_depth"]
        and report["roots_stated"] == report["roots_in_declared_region"]
        and result["uncertified"] == report["uncertified_boxes_stated"]
        and report.get("records_match_manifest", True)
        and report.get("manifest_header_equals_records_header", True)
    )
    return report, header


def audit_zm_mixed_manifests(
    case: Case,
    complete: Path | None = None,
    deep: Path | None = None,
    checker_dir: Path | None = None,
) -> dict[str, Any]:
    """The case's ``zm_mixed.py`` manifests, and what they decide without per-root records.

    ``states_complete_verification`` holds when the complete run's manifest is
    consistent, at depth 24 over the whole region, and states no uncertified box. A
    complete run that states uncertified boxes is never clean here, whatever a deeper
    run states: which roots hold the boxes is written only in the per-root records.
    """
    complete = complete or case.bundle_dir / "zm_mixed_d4/manifest.json"
    if deep is None and case.deep_manifest is not None:
        deep = case.bundle_dir / case.deep_manifest
    main, complete_header = audit_zm_mixed_manifest(case, complete, checker_dir)
    main["consistent"] = (
        main["consistent"]
        and main["depth"] == ZM_MIXED_SETTINGS["depth"]
        and not main["region"]
    )
    report: dict[str, Any] = {"records_audited": False, "complete_run": main}
    if deep is not None:
        run, deep_header = audit_zm_mixed_manifest(case, deep, checker_dir)
        run["header_sha256_equal_complete_run"] = (
            deep_header["sha256"] == complete_header["sha256"]
        )
        run["settings_equal_apart_from_depth_and_region"] = _settings_apart_from(
            deep_header, ("depth", "region")
        ) == _settings_apart_from(complete_header, ("depth", "region"))
        run["roots_of_declared_region"] = sorted(
            ",".join(key) for key in zm_mixed_region(case.side, run["region"])
        )[:50]
        run["consistent"] = (
            run["consistent"]
            and run["header_sha256_equal_complete_run"]
            and run["settings_equal_apart_from_depth_and_region"]
            and bool(run["region"])
            and run["uncertified_boxes_stated"] == 0
        )
        report["deep_run"] = run
    stated = main["uncertified_boxes_stated"]
    deep_run = report.get("deep_run")
    report["states_complete_verification"] = main["consistent"] and stated == 0
    report["consistent"] = main["consistent"] and (deep_run is None or deep_run["consistent"])
    report["verdict"] = (
        "stated verified" if report["states_complete_verification"] else "not clean"
    )
    if stated and report["consistent"] and deep_run is not None:
        # Consistent manifests decide everything but where the boxes lie.
        report["verdict"] = "undecided"
        report["decided_from_manifests"] = [
            (
                "both runs name the case's checker files and the retained cover by "
                "SHA-256 and state its total"
            ),
            (
                f"the complete run has the certificate-mode D4 settings at depth "
                f"{main['depth']} over the whole region and states "
                f"{main['roots_stated']} roots, the number the region holds, and "
                f"{stated} uncertified boxes"
            ),
            (
                f"the deeper run has the same settings apart from depth "
                f"({deep_run['depth']}) and region, its region holds "
                f"{deep_run['roots_stated']} root(s), "
                f"{', '.join(deep_run['roots_of_declared_region'])}, and it states no "
                "uncertified box"
            ),
        ]
        report["undecided"] = (
            f"whether the {stated} uncertified boxes lie in the deeper run's region: no "
            "manifest says which roots hold them; "
            + (
                "the complete run's per-root records are retained, and zm-mixed --deep "
                "decides it"
                if main["records_retained"]
                else "that is written only in the complete run's per-root records and "
                "log, neither published"
            )
        )
    return report


def compare_zm_mixed(shipped: Path, replays: Sequence[Path]) -> dict[str, Any]:
    """Root for root against the source; ``replays`` may be several partial runs."""
    source_header, source = read_zm_mixed(shipped)
    fresh: dict[tuple[str, ...], dict[str, Any]] = {}
    headers_equal = settings_equal = True
    regions = []
    for replay in replays:
        replay_header, records = read_zm_mixed(replay)
        headers_equal &= source_header["sha256"] == replay_header["sha256"]
        settings_equal &= _settings_apart_from(replay_header, ("region",)) == (
            _settings_apart_from(source_header, ("region",))
        )
        regions.append(replay_header["settings"].get("region"))
        if fresh.keys() & records.keys():
            raise ValueError(f"{replay}: a root is recorded in two replay files")
        fresh.update(records)
    common = fresh.keys() & source.keys()
    differ = sorted(key for key in common if _differs(fresh[key], source[key]))
    replay_cpu = sum(float(fresh[key]["st"]["cpu"]) for key in common)
    source_cpu = sum(float(source[key]["st"]["cpu"]) for key in common)
    return {
        "shipped": _display(shipped),
        "shipped_sha256": _sha256(shipped),
        "replays": [{"path": _display(r), "sha256": _sha256(r)} for r in replays],
        "header_sha256_equal": headers_equal,
        "settings_equal_apart_from_region": settings_equal,
        "replay_regions": regions,
        "shipped_roots": len(source),
        "replay_roots": len(fresh),
        "roots_compared": len(common),
        "roots_identical": len(common) - len(differ),
        "roots_whose_census_differs": [",".join(key) for key in differ[:50]],
        "replay_roots_not_in_shipped": len(fresh.keys() - source.keys()),
        "shipped_roots_not_replayed": len(source.keys() - fresh.keys()),
        "replay_cpu_seconds_on_compared_roots": round(replay_cpu, 1),
        "shipped_cpu_seconds_on_compared_roots": round(source_cpu, 1),
        "shipped_cpu_seconds_all_roots": round(
            sum(float(r["st"]["cpu"]) for r in source.values()), 1
        ),
    }


def comparison_clean(result: dict[str, Any]) -> bool:
    return (
        result["roots_compared"] > 0
        and result["roots_identical"] == result["roots_compared"]
        and result["replay_roots_not_in_shipped"] == 0
    )


# --- split covers: zmx2 roots and zm_mixed.py sub-roots read as one decision -------------


def record_files(paths: Path | Sequence[Path]) -> list[Path]:
    """Record files: each path itself, or the ``j*.jsonl`` files of a directory, by name."""
    out: list[Path] = []
    for path in _as_paths(paths):
        out += sorted(path.glob("j*.jsonl")) if path.is_dir() else [path]
    return out


def zmx2_open_roots(log: Zmx2Log, region: Mapping[Zmx2Key, int]) -> list[Zmx2Key]:
    """The roots of ``region`` whose census holds an uncertified box or a cap."""
    uncert, capped = ZMX2_CENSUS.index("uncert"), ZMX2_CENSUS.index("capped")
    return [
        key
        for key in region
        if key in log.census and (log.census[key][uncert] or log.census[key][capped])
    ]


def root_bounds(root: str) -> tuple[Fraction, ...]:
    """A root written ``x0,x1,y0,y1,u0,u1``, by ``zmx2`` or ``zm_mixed.py``, as fractions."""
    bounds = tuple(Fraction(v) for v in root.split(","))
    if len(bounds) != 6:
        raise ValueError(f"not a root: {root!r}")
    return bounds


def sub_roots(side: int, root: str) -> set[tuple[str, ...]]:
    """The ``zm_mixed.py`` roots, of the 1/20 by 1/32 grid, that tile a ``zmx2`` root."""
    x0, x1, y0, y1, u0, u1 = root_bounds(root)
    bounds = {"cx_lo": x0, "cx_hi": x1, "cy_lo": y0, "cy_hi": y1, "u_lo": u0, "u_hi": u1}
    return zm_mixed_region(side, {k: str(v) for k, v in bounds.items()})


def _zmx2_sound_apart_from_open_roots(result: dict[str, Any]) -> bool:
    """`zmx2_clean` without its uncertified and capped boxes, which the open roots hold."""
    return zmx2_clean({**result, "uncertified_boxes": 0, "uncert_lines": 0, "capped_roots": 0})


def audit_sub_root_file(
    case: Case, path: Path, expected: Mapping[str, str], reference: Mapping[str, Any] | None
) -> tuple[dict[str, Any], dict[tuple[str, ...], dict[str, Any]], dict[str, Any]]:
    """One ``zm_mixed.py`` record file of a split cover: report, records, header.

    ``reference`` is another file's settings; the file must equal it apart from region.
    """
    header, records = read_zm_mixed(path)
    settings = header["settings"]
    region = {k: v for k, v in settings.get("region", {}).items() if v is not None}
    declared = zm_mixed_region(case.side, region) if region else set()
    uncertified = sorted(",".join(k) for k, record in records.items() if _uncertified(record))
    report: dict[str, Any] = {
        "records": _display(path),
        "header_sha256_match_retained_files": header["sha256"] == dict(expected),
        "header_total_equals_stated": Fraction(header["total"]) == case.total,
        "settings_as_required": all(settings.get(k) == v for k, v in ZM_MIXED_SETTINGS.items()),
        "settings_equal_apart_from_region": reference is None
        or _settings_apart_from(header, ("region",))
        == {k: v for k, v in reference.items() if k != "region"},
        "region": region,
        "roots_in_region": len(declared),
        "roots_missing": len(declared - records.keys()),
        "roots_outside_region": len(records.keys() - declared),
        "uncertified_roots": uncertified[:20],
    }
    report["clean"] = (
        report["header_sha256_match_retained_files"]
        and report["header_total_equals_stated"]
        and report["settings_as_required"]
        and report["settings_equal_apart_from_region"]
        and bool(region)
        and bool(declared)
        and report["roots_missing"] == 0
        and report["roots_outside_region"] == 0
        and not uncertified
    )
    return report, records, header


def _jobs(path: Path) -> set[tuple[str, ...]]:
    """A ``jobs.txt``: ``id cx_lo cx_hi cy_lo cy_hi u_lo u_hi`` per line, as roots."""
    rows = [line.split() for line in read_record_bytes(path).decode("ascii").splitlines()]
    return {tuple(str(Fraction(v)) for v in row[1:]) for row in rows if row}


def _failing(path: Path) -> set[tuple[Fraction, ...]]:
    lines = read_record_bytes(path).decode("ascii").splitlines()
    return {root_bounds(line.strip()) for line in lines if line.strip()}


FNV_OFFSET, FNV_PRIME = 0xCBF29CE484222325, 0x100000001B3


def fnv1a64(data: bytes) -> str:
    """FNV-1a 64 of ``data`` in hex, the cover hash ``zmx2 cert`` writes into its header."""
    value = FNV_OFFSET
    for byte in data:
        value = ((value ^ byte) * FNV_PRIME) & 0xFFFFFFFFFFFFFFFF
    return f"{value:016x}"


@functools.lru_cache(maxsize=8)
def _cover_fnv1a64(path: Path, stamp: tuple[int, int]) -> str:
    del stamp
    return fnv1a64(read_record_bytes(path))


def audit_split_composite(
    case: Case,
    zmx2_logs: Path | Sequence[Path],
    zm_mixed: Path | Sequence[Path],
    checker_dir: Path | None = None,
) -> dict[str, Any]:
    """A ``zmx2 cert --d4`` log and ``zm_mixed.py`` sub-root records as one decision.

    Clean when the log is sound apart from its open roots (`zmx2_open_roots`), every
    header names this cover by the FNV-1a 64 hash ``zmx2`` writes and carries the
    source's settings (`Split.zmx2_settings`), every record file is clean
    (`audit_sub_root_file`), no sub-root is recorded twice, and every sub-root of every
    open root is a certified one.
    """
    zmx2 = require_atoms(audit_zmx2(case, zmx2_logs, "d4"), case.zmx2_atoms)
    log = read_zmx2(zmx2_logs)
    cover_hash = _cover_fnv1a64(case.cover_path, _stamp(case.cover_path))
    headers = [parse_zmx2_header(run.header)[0] for run in log.runs]
    required = dict(case.split.zmx2_settings) if case.split is not None else {}
    region = zmx2_roots(case.side, "d4")
    open_roots = zmx2_open_roots(log, region)
    files = record_files(zm_mixed)
    if not files:
        raise ValueError("no zm_mixed.py record file named")
    expected = _expected_digests(case, checker_paths(case, files[0], checker_dir))
    reference: dict[str, Any] | None = None
    certified: set[tuple[str, ...]] = set()
    seen: set[tuple[str, ...]] = set()
    repeated = 0
    unclean: list[dict[str, Any]] = []
    census: Counter[str] = Counter()
    max_depth = 0
    cpu = 0.0
    for path in files:
        report, records, header = audit_sub_root_file(case, path, expected, reference)
        reference = reference or header["settings"]
        if not report["clean"]:
            unclean.append(report)
        repeated += len(seen & records.keys())
        seen |= records.keys()
        for key, record in records.items():
            leaves = _census(record)
            max_depth = max(max_depth, leaves.pop("maxdepth"))
            census.update(leaves)
            cpu += float(record["st"]["cpu"])
            if not _uncertified(record):
                certified.add(key)
    needed: dict[Zmx2Key, set[tuple[str, ...]]] = {
        key: sub_roots(case.side, key[1]) for key in open_roots
    }
    tiling: set[tuple[str, ...]] = set()
    for cells in needed.values():
        tiling |= cells
    untiled = [f"pass {p} root {r}" for (p, r), cells in needed.items() if cells - certified]
    result: dict[str, Any] = {
        "zmx2": zmx2,
        "zmx2_sound_apart_from_open_roots": _zmx2_sound_apart_from_open_roots(zmx2),
        "cover_fnv1a64": cover_hash,
        "zmx2_header_hashes": sorted({fields.get("hash", "") for fields in headers}),
        "zmx2_headers_name_this_cover": bool(headers)
        and all(fields.get("hash") == cover_hash for fields in headers),
        "zmx2_settings_required": required,
        "zmx2_settings_as_required": bool(headers)
        and all(fields.get(k) == v for fields in headers for k, v in required.items()),
        "open_roots": [f"pass {p} root {r}" for p, r in open_roots],
        "open_root_count": len(open_roots),
        "roots_certified_by_zmx2": len(region) - len(open_roots),
        "zm_mixed_files": len(files),
        "zm_mixed_settings_apart_from_region": {
            k: v for k, v in (reference or {}).items() if k != "region"
        },
        "zm_mixed_files_not_clean": unclean[:20],
        "zm_mixed_files_not_clean_count": len(unclean),
        "zm_mixed_roots_certified": len(certified),
        "zm_mixed_roots_recorded_more_than_once": repeated,
        "zm_mixed_census": dict(sorted({**census, "maxdepth": max_depth}.items())),
        "zm_mixed_cpu_seconds": round(cpu, 1),
        "sub_roots_of_open_roots": len(tiling),
        "open_roots_not_tiled": untiled[:20],
        "zm_mixed_roots_outside_open_roots": len(certified - tiling),
        "sub_roots_tile_open_roots_exactly": certified == tiling,
    }
    result["composite_clean"] = (
        result["zmx2_sound_apart_from_open_roots"]
        and result["zmx2_headers_name_this_cover"]
        and result["zmx2_settings_as_required"]
        and not unclean
        and repeated == 0
        and not untiled
    )
    split = case.split
    if split is not None:
        result["open_roots_equal_source_list"] = {
            root_bounds(r) for _, r in open_roots
        } == _failing(split.failing)
        result["zm_mixed_roots_equal_source_jobs"] = certified == _jobs(split.jobs)
    return result


def compare_sub_roots(shipped: Path, replay: Path) -> dict[str, Any]:
    """A replay's sub-root record files against the source's, each by its file name."""
    source = {path.name: path for path in record_files(shipped)}
    fresh = {path.name: path for path in record_files(replay)}
    differ: list[str] = []
    roots = identical = 0
    replay_cpu = source_cpu = 0.0
    for name in sorted(source.keys() & fresh.keys()):
        result = compare_zm_mixed(source[name], [fresh[name]])
        roots += result["roots_compared"]
        identical += result["roots_identical"]
        replay_cpu += result["replay_cpu_seconds_on_compared_roots"]
        source_cpu += result["shipped_cpu_seconds_on_compared_roots"]
        if not (
            comparison_clean(result)
            and result["header_sha256_equal"]
            and result["settings_equal_apart_from_region"]
            and result["shipped_roots_not_replayed"] == 0
        ):
            differ.append(name)
    return {
        "shipped": _display(shipped),
        "replay": _display(replay),
        "shipped_files": len(source),
        "replay_files": len(fresh),
        "files_compared": len(source.keys() & fresh.keys()),
        "files_not_replayed": sorted(source.keys() - fresh.keys())[:20],
        "replay_files_not_in_shipped": sorted(fresh.keys() - source.keys())[:20],
        "files_that_differ": differ[:20],
        "roots_compared": roots,
        "roots_identical": identical,
        "replay_cpu_seconds": round(replay_cpu, 1),
        "shipped_cpu_seconds": round(source_cpu, 1),
    }


def sub_root_comparison_clean(result: dict[str, Any]) -> bool:
    return (
        result["files_compared"] > 0
        and result["files_compared"] == result["shipped_files"] == result["replay_files"]
        and not result["files_that_differ"]
        and result["roots_identical"] == result["roots_compared"] > 0
    )


# --- the packets -------------------------------------------------------------------------


def sample_records(n: int) -> list[Path]:
    """The packet's sampled zm_mixed.py replays for ``s(n)``, one file per centre cell."""
    return sorted(RECEIPTS.glob(f"s{n}_zm_mixed_sample_*.jsonl"))


@dataclass(frozen=True, slots=True)
class PointCoverRun:
    """A fresh ``zmx2 --d4`` run on one of the source's plain point covers."""

    n: int
    side: int
    receipt: str
    #: Totals ``search/ZMX2.md`` section 9 reports for the source's run; it ships no log.
    boxes: int
    certified_leaves: int | None
    empty_leaves: int | None
    max_depth: int
    #: The packet whose ``receipts/`` holds the log: the source's own, or a later replay's.
    directory: Path = RECEIPTS
    #: The source's own unreduced ``zmx2 cert --full`` log, where it ships one.
    full_log: Path | None = None
    #: The ``atoms`` header value of that log.
    full_atoms: str | None = None

    @property
    def log(self) -> Path:
        return self.directory / self.receipt


#: The source's ``s(13)`` and ``s(32)`` point covers, which the previous packet retains.
POINT_COVER_RUNS = (
    PointCoverRun(13, 4, "s13_zmx2_d4_roots.log", 47162, 22136, 2245, 20),
    PointCoverRun(
        32,
        6,
        "s32_zmx2_d4_pairpoints_roots.log",
        1405342,
        686886,
        17585,
        29,
        full_log=EVAND_1001 / "certificates/s32/zmx2_full_sym/roots.log.xz",
        full_atoms="pairpts+sym",
    ),
    # Hosono's point-only s(61) cover: its provenance.json reports 800,042 boxes at depth
    # 30 and no leaf split, which is left out of the comparison. Replayed here with the
    # zmx2 6b7f0f79 its verify.sh builds.
    PointCoverRun(
        61,
        8,
        "n61_zmx2_d4_pairpoints_roots.log",
        800042,
        None,
        None,
        30,
        directory=WEB / "wand125-point-n61-2026-09-30/receipts",
    ),
)
POINT_COVERS = {run.n: run for run in POINT_COVER_RUNS}


def shipped_zmx2(n: int, mode: str) -> Path | None:
    """The reference log for ``compare-zmx2``, or ``None`` where no log is retained."""
    run = POINT_COVERS.get(n)
    if run is not None:
        return run.log if mode == "d4" else run.full_log
    case = MIXED_CASES[n]
    if case.split is not None:
        return case.split.zmx2 if mode == "d4" else None
    if case.whole is not None:
        return case.whole.source_log(mode)
    return case.bundle_dir / f"zmx2_{mode}/roots.log" if mode in case.zmx2_modes else None


def audit_point_cover_run(
    run: PointCoverRun, path: Path | Sequence[Path] | None = None
) -> dict[str, Any]:
    """Region completeness, and the census totals against the ones the source reports.

    ``path`` defaults to the packet's retained log; a replayer passes their own, or the
    parts of a joined run.
    """
    result = audit_zmx2(run, path or run.log, "d4")
    stated = (run.boxes, run.certified_leaves, run.empty_leaves, run.max_depth)
    result["totals_equal_source_report"] = all(
        want is None or got == want
        for got, want in zip(
            (
                result["boxes"],
                result["certified_leaves"],
                result["empty_leaves"],
                result["max_depth"],
            ),
            stated,
            strict=True,
        )
    )
    return result


def point_cover_clean(result: dict[str, Any]) -> bool:
    return zmx2_clean(result) and result["totals_equal_source_report"]


def check_point_cover_runs(
    runs: Sequence[PointCoverRun] = POINT_COVER_RUNS,
) -> tuple[dict[str, Any], bool]:
    """Each retained point-cover log, which must exist: evidence entries replay from it."""
    report: dict[str, Any] = {}
    clean = True
    for run in runs:
        key = f"s{run.n}_point_cover_zmx2_d4"
        log = run.log
        if not retained_exists(log):
            report[key] = {"log": _display(log), "missing": True}
            clean = False
            continue
        report[key] = audit_point_cover_run(run)
        clean &= point_cover_clean(report[key])
    return report, clean


def check_september_case(n: int, case: Case) -> tuple[dict[str, Any], bool]:
    """The cover, the shipped records, and this repository's replays of them."""
    bundle = case.bundle_dir
    entry: dict[str, Any] = {"cover": audit_cover(case)}
    clean = cover_clean(entry["cover"])
    entry["shipped_zm_mixed"] = audit_zm_mixed(case, bundle / "zm_mixed_d4/roots.jsonl")
    clean &= zm_mixed_clean(entry["shipped_zm_mixed"])
    for mode in ("d4", "full"):
        shipped = bundle / f"zmx2_{mode}/roots.log"
        entry[f"shipped_zmx2_{mode}"] = audit_zmx2(case, shipped, mode)
        clean &= zmx2_clean(entry[f"shipped_zmx2_{mode}"])
        fresh = RECEIPTS / f"s{n}_zmx2_{mode}_roots.log"
        if not retained_exists(fresh):
            # The evidence entries replay from these receipts, so absence is a failure.
            entry[f"fresh_zmx2_{mode}"] = {"log": _display(fresh), "missing": True}
            clean = False
            continue
        entry[f"fresh_zmx2_{mode}"] = audit_zmx2(case, fresh, mode)
        compared = compare_zmx2(shipped, fresh)
        entry[f"fresh_zmx2_{mode}_vs_shipped"] = compared
        clean &= zmx2_clean(entry[f"fresh_zmx2_{mode}"])
        clean &= zmx2_comparison_clean(compared)
        clean &= compared["shipped_roots_not_replayed"] == 0
    samples = sample_records(n)
    if samples:
        entry["zm_mixed_sample_vs_shipped"] = compare_zm_mixed(
            bundle / "zm_mixed_d4/roots.jsonl", samples
        )
        clean &= comparison_clean(entry["zm_mixed_sample_vs_shipped"])
    return entry, clean


def check_imported_case(case: Case) -> tuple[dict[str, Any], bool, str | None]:
    """The cover, whatever source records the bundle retains, and its manifests.

    Returns the report, whether everything decided is clean, and what is undecided.
    """
    bundle = case.bundle_dir
    entry: dict[str, Any] = {"cover": audit_cover(case)}
    clean = cover_clean(entry["cover"])
    for mode in case.zmx2_modes:
        log = bundle / f"zmx2_{mode}/roots.log"
        audited = audit_zmx2(case, log, mode)
        entry[f"shipped_zmx2_{mode}"] = audited
        manifest = audit_zmx2_manifest(log.parent / "manifest.txt", log, audited)
        entry[f"shipped_zmx2_{mode}_manifest"] = manifest
        clean &= zmx2_clean(audited) and manifest["consistent"]
    if case.zm_mixed_records:
        entry["shipped_zm_mixed"] = audit_zm_mixed(case, bundle / "zm_mixed_d4/roots.jsonl")
        clean &= zm_mixed_clean(entry["shipped_zm_mixed"])
    manifests = audit_zm_mixed_manifests(case)
    entry["zm_mixed_manifests"] = manifests
    entry["zm_mixed_verdict"] = manifests["verdict"]
    clean &= manifests["consistent"]
    undecided = manifests.get("undecided")
    if undecided is None:
        clean &= manifests["states_complete_verification"]
    return entry, clean, undecided


def check_split_case(case: Case) -> tuple[dict[str, Any], bool]:
    """A split cover: the cover, the source's composite and the replay's, the replay against
    the source for both checkers, and the wall control against the replay."""
    split = case.split
    if split is None:
        raise ValueError(f"s({case.n}) is not a split cover")
    entry: dict[str, Any] = {"cover": audit_cover(case)}
    clean = cover_clean(entry["cover"])
    for name, zmx2, zm_mixed in (
        ("source", split.zmx2, split.zm_mixed),
        ("replay", split.replay_zmx2, split.replay_zm_mixed),
    ):
        composite = audit_split_composite(case, zmx2, zm_mixed)
        entry[f"{name}_composite"] = composite
        clean &= (
            composite["composite_clean"]
            and composite["open_roots_equal_source_list"]
            and composite["zm_mixed_roots_equal_source_jobs"]
            and composite["sub_roots_tile_open_roots_exactly"]
        )
    compared = compare_zmx2(split.zmx2, split.replay_zmx2)
    entry["replay_zmx2_vs_source"] = compared
    clean &= zmx2_comparison_clean(compared) and compared["shipped_roots_not_replayed"] == 0
    sub = compare_sub_roots(split.zm_mixed, split.replay_zm_mixed)
    entry["replay_zm_mixed_vs_source"] = sub
    clean &= sub_root_comparison_clean(sub)
    if split.wall_control is not None:
        # The cover without its wall segments has another hash, so its header differs;
        # every root's census and every UNCERT line must still be the replay's.
        wall = compare_zmx2(split.replay_zmx2, split.wall_control)
        entry["wall_control_vs_replay"] = wall
        clean &= (
            comparison_clean(wall)
            and wall["shipped_roots_not_replayed"] == 0
            and wall["replay_uncert_lines"] == wall["shipped_uncert_lines"]
            and wall["replay_unparsed_lines"] == wall["shipped_unparsed_lines"] == 0
        )
    return entry, clean


def audit_whole_zmx2(case: Case, paths: Path | Sequence[Path], mode: str) -> dict[str, Any]:
    """A ``zmx2`` log of a cover it decides whole: clean, naming this cover, as the source ran.

    `audit_zmx2`, with the source's ``atoms``, plus every header naming this cover by the
    FNV-1a 64 hash ``zmx2`` computes over its bytes and carrying the source's settings
    (`Whole.zmx2_settings`). ``whole_clean`` is all of them.
    """
    if case.whole is None:
        raise ValueError(f"s({case.n}) is not a cover zmx2 decides whole")
    result = require_atoms(audit_zmx2(case, paths, mode), case.zmx2_atoms)
    log = read_zmx2(paths)
    cover_hash = _cover_fnv1a64(case.cover_path, _stamp(case.cover_path))
    headers = [parse_zmx2_header(run.header)[0] for run in log.runs]
    required = dict(case.whole.zmx2_settings)
    result["cover_fnv1a64"] = cover_hash
    result["headers_name_this_cover"] = bool(headers) and all(
        fields.get("hash") == cover_hash for fields in headers
    )
    result["settings_required"] = required
    result["settings_as_required"] = bool(headers) and all(
        fields.get(k) == v for fields in headers for k, v in required.items()
    )
    result["whole_clean"] = (
        zmx2_clean(result)
        and result["headers_name_this_cover"]
        and result["settings_as_required"]
    )
    return result


def check_whole_case(case: Case) -> tuple[dict[str, Any], bool]:
    """A cover ``zmx2`` decides whole: the cover, then in each mode the source's log and the
    replay's, each clean (`audit_whole_zmx2`), and the replay equal to the source root for
    root with every source root replayed."""
    whole = case.whole
    if whole is None:
        raise ValueError(f"s({case.n}) is not a cover zmx2 decides whole")
    entry: dict[str, Any] = {"cover": audit_cover(case)}
    clean = cover_clean(entry["cover"])
    for mode, source in whole.source:
        entry[f"source_zmx2_{mode}"] = audit_whole_zmx2(case, source, mode)
        clean &= entry[f"source_zmx2_{mode}"]["whole_clean"]
        replay = whole.replay_log(mode)
        if replay is None or not retained_exists(replay):
            # The evidence entry replays from these receipts, so absence is a failure.
            entry[f"replay_zmx2_{mode}"] = {"log": str(replay), "missing": True}
            clean = False
            continue
        entry[f"replay_zmx2_{mode}"] = audit_whole_zmx2(case, replay, mode)
        compared = compare_zmx2(source, replay)
        entry[f"replay_zmx2_{mode}_vs_source"] = compared
        clean &= entry[f"replay_zmx2_{mode}"]["whole_clean"]
        clean &= zmx2_comparison_clean(compared) and compared["shipped_roots_not_replayed"] == 0
    return entry, clean


def check_packet() -> dict[str, Any]:
    """The cover, shipped-record and receipt audits over the packets' retained files."""
    report: dict[str, Any] = {}
    clean = True
    undecided: dict[str, str] = {}
    for n, case in CASES.items():
        report[f"s{n}"], ok = check_september_case(n, case)
        clean &= ok
    point_covers, points_clean = check_point_cover_runs()
    report.update(point_covers)
    for n, case in POINT_ONLY_CASES.items():
        report[f"s{n}_point_cover"] = audit_cover(case)
        clean &= cover_clean(report[f"s{n}_point_cover"])
    for n, case in IMPORTED_CASES.items():
        report[f"s{n}"], ok, open_question = check_imported_case(case)
        clean &= ok
        if open_question is not None:
            undecided[f"s{n}_zm_mixed"] = open_question
    for n, case in SPLIT_CASES.items():
        report[f"s{n}"], ok = check_split_case(case)
        clean &= ok
    for n, case in WHOLE_CASES.items():
        report[f"s{n}"], ok = check_whole_case(case)
        clean &= ok
    for run in POINT_COVER_RUNS:
        if run.full_log is not None:
            key = f"s{run.n}_point_cover_zmx2_full_source"
            audited = require_atoms(audit_zmx2(run, run.full_log, "full"), run.full_atoms)
            manifest = audit_zmx2_manifest(
                run.full_log.parent / "manifest.txt", run.full_log, audited
            )
            report[key] = {**audited, "manifest": manifest}
            clean &= zmx2_clean(audited) and manifest["consistent"]
    report["undecided"] = undecided
    report["clean"] = clean and points_clean
    return report


def _emit(result: dict[str, Any], output: Path | None) -> None:
    text = json.dumps(result, indent=1) + "\n"
    if output is not None:
        with atomic_output_file(output) as handle:
            handle.write_text(text)
    print(text, end="")


def _zmx2_command(
    parser: argparse.ArgumentParser, args: argparse.Namespace
) -> tuple[dict[str, Any], bool]:
    """``zmx2`` and ``compare-zmx2``, for a mixed cover or one of the point covers."""
    run = POINT_COVERS.get(args.case)
    if args.command == "zmx2":
        if run is not None and args.mode == "d4":
            result = require_atoms(audit_point_cover_run(run, args.log), args.atoms)
            return result, point_cover_clean(result)
        # The source reports no totals for an unreduced run on a point cover.
        case = run if run is not None else MIXED_CASES[args.case]
        result = require_atoms(audit_zmx2(case, args.log, args.mode), args.atoms)
        return result, zmx2_clean(result)
    shipped = args.shipped or shipped_zmx2(args.case, args.mode)
    if shipped is None:
        parser.error(
            f"no {args.mode} zmx2 log of s({args.case}) is published; name one with --shipped"
        )
    result = compare_zmx2(shipped, args.records)
    return result, zmx2_comparison_clean(result)


def _zm_mixed_records(parser: argparse.ArgumentParser, args: argparse.Namespace) -> Path:
    """The record file named, or the source's complete run where the bundle retains it."""
    case = MIXED_CASES[args.case]
    if args.records is not None:
        return args.records
    if not case.zm_mixed_records:
        parser.error(f"no zm_mixed records of s({args.case}) are published; name a file")
    return case.bundle_dir / "zm_mixed_d4/roots.jsonl"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--output", type=Path, help="also write the JSON here")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser(
        "check", parents=[common], help="audit the packets' retained files and receipts"
    )
    mixed = sorted(MIXED_CASES)
    zmx2_cases = sorted({*MIXED_CASES, *POINT_COVERS})
    cover = commands.add_parser("cover", parents=[common], help="audit one mixed cover")
    cover.add_argument(
        "--case", type=int, choices=sorted({*mixed, *POINT_ONLY_CASES}), required=True
    )
    cover.add_argument("path", type=Path, nargs="?")
    zmx2 = commands.add_parser(
        "zmx2", parents=[common], help="audit zmx2 cert logs, several read as one"
    )
    zmx2.add_argument("--case", type=int, choices=zmx2_cases, required=True)
    zmx2.add_argument("--mode", choices=("d4", "full"), required=True)
    zmx2.add_argument("--atoms", help="require this header atoms value, e.g. pairpts+sym")
    zmx2.add_argument("log", type=Path, nargs="+", help="one log, or the parts of a joined run")
    zm = commands.add_parser(
        "zm-mixed", parents=[common], help="audit one zm_mixed.py record file"
    )
    zm.add_argument("--case", type=int, choices=mixed, required=True)
    zm.add_argument(
        "records", type=Path, nargs="?", help="default: the source's complete run, if published"
    )
    zm.add_argument(
        "--deep",
        type=Path,
        nargs="+",
        help="deeper runs of the roots the complete run leaves uncertified (a composite)",
    )
    zm.add_argument("--checker-dir", type=Path, help="default: the case's, or checker/ beside")
    manifest = commands.add_parser(
        "zm-mixed-manifest",
        parents=[common],
        help="what zm_mixed.py manifests state, without per-root records",
    )
    manifest.add_argument("--case", type=int, choices=mixed, required=True)
    manifest.add_argument("manifest", type=Path, nargs="?")
    manifest.add_argument("--deep", type=Path, help="default: the case's deeper run, if any")
    manifest.add_argument("--checker-dir", type=Path)
    split = sorted(SPLIT_CASES)
    composite = commands.add_parser(
        "composite",
        parents=[common],
        help="a split cover's zmx2 log and zm_mixed.py sub-roots as one decision",
    )
    composite.add_argument("--case", type=int, choices=split, required=True)
    composite.add_argument(
        "zmx2_log",
        type=Path,
        nargs="*",
        help="default: the replay's, or with --source the source's",
    )
    composite.add_argument(
        "--zm-mixed", type=Path, nargs="+", help="record files, or directories of j*.jsonl"
    )
    composite.add_argument(
        "--source", action="store_true", help="read the source's records, not the replay's"
    )
    composite.add_argument("--checker-dir", type=Path)
    sub = commands.add_parser(
        "compare-sub-roots",
        parents=[common],
        help="a replay's zm_mixed.py sub-root files against the source's, by name",
    )
    sub.add_argument("--case", type=int, choices=split, required=True)
    sub.add_argument("replay", type=Path, nargs="?", help="default: the retained replay's")
    for name, choices in (("compare-zmx2", zmx2_cases), ("compare-zm-mixed", mixed)):
        compare = commands.add_parser(
            name, parents=[common], help="root-for-root census against the source"
        )
        compare.add_argument("--case", type=int, choices=choices, required=True)
        compare.add_argument("--mode", choices=("d4", "full"), default="d4")
        compare.add_argument(
            "--records", type=Path, nargs="+", required=True, help="the replay's file(s)"
        )
        compare.add_argument(
            "--shipped",
            type=Path,
            help="default: the source's record, or for s(13) and s(32) d4 the retained run",
        )
    args = parser.parse_args(argv)
    if args.command == "check":
        result = check_packet()
        _emit(result, args.output)
        return 0 if result["clean"] else 1
    if args.command in {"zmx2", "compare-zmx2"}:
        result, ok = _zmx2_command(parser, args)
    elif args.command == "composite":
        case = SPLIT_CASES[args.case]
        assert case.split is not None
        zmx2_logs = args.zmx2_log or [
            case.split.zmx2 if args.source else case.split.replay_zmx2
        ]
        records = args.zm_mixed or [
            case.split.zm_mixed if args.source else case.split.replay_zm_mixed
        ]
        result = audit_split_composite(case, zmx2_logs, records, args.checker_dir)
        ok = result["composite_clean"]
    elif args.command == "compare-sub-roots":
        case = SPLIT_CASES[args.case]
        assert case.split is not None
        result = compare_sub_roots(
            case.split.zm_mixed, args.replay or case.split.replay_zm_mixed
        )
        ok = sub_root_comparison_clean(result)
    elif args.command == "cover":
        result = audit_cover({**MIXED_CASES, **POINT_ONLY_CASES}[args.case], args.path)
        ok = cover_clean(result)
    elif args.command == "zm-mixed" and args.deep:
        result = audit_zm_mixed_composite(
            MIXED_CASES[args.case], _zm_mixed_records(parser, args), args.deep, args.checker_dir
        )
        ok = result["composite_clean"]
    elif args.command == "zm-mixed":
        result = audit_zm_mixed(
            MIXED_CASES[args.case], _zm_mixed_records(parser, args), args.checker_dir
        )
        ok = zm_mixed_clean(result)
    elif args.command == "zm-mixed-manifest":
        result = audit_zm_mixed_manifests(
            MIXED_CASES[args.case], args.manifest, args.deep, args.checker_dir
        )
        ok = result["states_complete_verification"]
    else:
        case = MIXED_CASES[args.case]
        if args.shipped is None and not case.zm_mixed_records:
            parser.error(f"no zm_mixed records of s({args.case}) are published; use --shipped")
        shipped = args.shipped or case.bundle_dir / "zm_mixed_d4/roots.jsonl"
        result = compare_zm_mixed(shipped, args.records)
        ok = comparison_clean(result)
    _emit(result, args.output)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
