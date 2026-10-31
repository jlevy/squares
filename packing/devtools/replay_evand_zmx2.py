"""Build Evan Daniel's ``zmx2`` from retained bytes and replay a mixed or point cover.

Stage 4 of the result import process replays the source's own checker on the retained
bytes (``campaign/result-import.md``). For the covers in Daniel's format that checker is
the Rust ``zmx2``, and every input it needs is retained here: its source at the version a
run's manifest names, the crate files it builds with, and the cover. This tool assembles
them in a scratch directory, refusing any file whose SHA-256 is not the one the record
states, builds the binary with ``cargo``, and runs ``zmx2 cert`` under
``devtools.replay_receipt``, so every run leaves a receipt in one shape.

``build --checker 6b7f0f79|92a4cfe8|e2bb84e9 --work DIR``
    Writes ``DIR/<checker>/verify2/`` and builds ``target/release/zmx2``; the receipt is
    ``DIR/<checker>/build.log``. Rebuilding an existing directory is a no-op apart from
    re-checking the digests.
``run --case N --mode d4|full --work DIR --out OUT [--threads T] [--x LO-HI] [--y LO-HI]``
    Runs the case's cover with the flags its source used (``CASES``), writing the
    receipt ``OUT/<name>.log`` and the root log ``OUT/<name>_roots.log``. Where the
    source split the D4 region between ``zmx2`` and ``zm_mixed.py`` sub-roots (s(76) and
    s(95)), it also passes the source's ``--uncert-cap``, so the roots left to
    ``zm_mixed.py`` are listed in full, as the source's record lists them. ``--x`` and
    ``--y`` restrict the root region, so one sweep can be split across machines; the
    region is in the file name. ``--time-limit S`` stops the run after ``S`` seconds
    with exit 3, so a session can push partial receipts. Running the same command again
    resumes from the root log, which ``zmx2`` reads before it starts, so an interrupted
    run loses at most the roots in flight; the resumed run writes
    ``<name>_resume<k>.log`` beside the first receipt. ``zmx2`` itself exits 0 whatever
    its verdict, so the verdict is read from the receipt (``REGION CLEAN``,
    ``VERIFIED``, ``NOT VERIFIED``, ``INCOMPLETE``).
``control --case N --mutation KIND --work DIR --out OUT [--mode M] [--x LO-HI] [--y LO-HI]``
    Stage 4's negative control: stages a mutated copy of the case's cover (``mutate``)
    and runs the same ``zmx2 cert`` on it over a small root region where the mutation is
    refused, writing ``OUT/<name>_control_<KIND>_zmx2_...log`` and its root log. Each
    mutation in ``MUTATIONS`` removes whole D4 orbits or scales every mass, so a
    D4-invariant cover stays invariant and ``--d4`` still applies. The mode and region
    default to the retained control's (``CONTROLS``). The receipt's ``cwd`` line names
    the mutated cover's SHA-256 beside the retained one's and the mass removed; a
    retained control must read ``NOT VERIFIED`` with uncertified boxes, which
    ``tests/test_replay_controls.py`` holds.

``zm-mixed --case N --work DIR --out OUT [--only ID ...] [--python PATH]``
    For a split cover (``ZM_MIXED_JOBS``: s(76) and s(95)), stages ``zm_mixed.py`` and the
    two files it imports from the retained evand packets, refusing any whose SHA-256 is
    not the one the source's ``verify.sh`` pins, and runs ``zm_mixed.py cert`` on each
    sub-root of the source's ``jobs.txt`` with that script's flags, one job at a time,
    writing ``OUT/n<N>_zm_mixed/j<id>.log`` (the receipt) and ``j<id>.jsonl`` (the
    records, through ``--resume``). ``--only`` runs the named jobs, so the list can be
    split across processes. ``zm_mixed.py`` needs numpy, so ``--python`` (default: this
    interpreter) must have it; it runs with ``-I``.

What a run decides is read afterwards by ``devtools.audit_evand_mixed_covers``. This
tool decides nothing about a cover: it only guarantees which bytes were run.

It imports only the standard library and ``devtools.replay_receipt``, so it runs under
any CPython from 3.11 and needs no project environment, which is what a fresh cloud
batch session has; only ``zm-mixed``'s interpreter needs numpy. From ``packing/``::

    python3 -m devtools.replay_evand_zmx2 build --checker 6b7f0f79 --work /tmp/zmx2
    python3 -m devtools.replay_evand_zmx2 run --case 77 --mode full --x 45-89 \\
        --work /tmp/zmx2 --out /tmp/zmx2/out --threads 4
    .venv/bin/python3 -m devtools.replay_evand_zmx2 zm-mixed --case 95 \\
        --work /tmp/zmx2 --out /tmp/zmx2/out --only 000 001
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import shutil
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from devtools import replay_receipt

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
CRATE = WEB / "evand-square-packing-2026-09-26/square-packing/s12/verify2"
WAND125 = WEB / "wand125-point-and-mixed-2026-10-01/square-packing-bounds/certificates"
WAND125_N61 = WEB / "wand125-point-n61-2026-09-30/square-packing-bounds/point_n61_L8"
BENGREFF_S76 = WEB / "bengreff-s76-certificate-2026-10-14/s76-certificate/cover"
BENGREFF_S95 = WEB / "bengreff-s95-certificate-2026-10-15/s95-certificate/cover"
KHALILI_S44 = WEB / "moh63-dev-s44-equals-7-2026-10-29/s44-equals-7/certificate"

#: The crate files every checker version builds with: path in the crate, retained copy, SHA-256.
CRATE_FILES = (
    (
        "Cargo.toml",
        CRATE / "Cargo.toml",
        "4e0f078ea45b32802c21cb71413305e30cd062c3fa371c6ff6e62bda3d07a577",
    ),
    (
        "Cargo.lock",
        CRATE / "Cargo.lock",
        "e1daec4d9995e879ddbf4aa5fb89b6f03eaaa23157ef60feb72741e3a0ffa57e",
    ),
    (
        "src/main.rs",
        CRATE / "src/main.rs",
        "94b7d83ecf6aeea64c20aea9d4f5c210c28577fb3870581d79169204c980c12b",
    ),
)

#: ``zmx2.rs`` versions by the prefix of their SHA-256: the retained copy and the full digest.
CHECKERS = {
    "6b7f0f79": (
        WEB / "evand-square-packing-2026-09-28/square-packing/s12/verify2/src/bin/zmx2.rs",
        "6b7f0f79466bf25c9a85f8fe2f3866de734935f0521ea188136818c2fb5b3fed",
    ),
    "92a4cfe8": (
        WEB / "evand-zmx2-sym-atoms-2026-09-30/square-packing/s12/verify2/src/bin/zmx2.rs",
        "92a4cfe87b4e33d57ce132c9c517eded3fe62b4a5a2151b5ba250b8ee329fe64",
    ),
    # The version that also reads a side that is not a multiple of 1/10, unchanged from
    # b8157df to 659ee62, which Khalili and Gharabaghi's verify.sh pins for s(44).
    "e2bb84e9": (
        WEB / "evand-square-packing-2026-10-04/square-packing/s12/verify2/src/bin/zmx2.rs",
        "e2bb84e9e05938db416940ad608d2583ca9a0c248d59820937c4ce59d607ead7",
    ),
}


@dataclass(frozen=True, slots=True)
class Case:
    """One cover: where it is retained, its digest, and how its source ran ``zmx2``."""

    name: str
    cover: Path
    sha256: str
    checker: str
    flags: tuple[str, ...]
    #: Root cells per axis: the side over the centre pitch 1/10 (``full``); half in ``d4``.
    cells: int
    #: Flags that change only how many uncertified boxes ``zmx2`` lists in a root before
    #: it stops that root (``--uncert-cap``), never which roots it certifies: ``run``
    #: passes them, as the source's own sweep did; ``control`` and the file name leave
    #: them out, since the retained controls ran ``zmx2``'s default.
    listing: tuple[str, ...] = ()


CASES = {
    32: Case(
        "s32",
        WEB
        / "evand-square-packing-2026-09-26/square-packing/s12/certificates/s32"
        / "s32_closed_cover_6.txt.gz",
        "a0d2d38fc9a585a166b9e06c5069fdae9bdce44ca9fb64dda75abcc99e3c2144",
        "92a4cfe8",
        ("--pair-points", "--sym-atoms"),
        60,
    ),
    59: Case(
        "n59",
        WAND125 / "k2m5_n59_L8/n59_mixed_cover_8.txt.gz",
        "6f4d2b64f9a88ae49546f05fa28752382f9ebfa8b7f8b6e6c6f1a8e693177e19",
        "6b7f0f79",
        (),
        80,
    ),
    60: Case(
        "s60",
        WEB
        / "evand-square-packing-2026-10-01/source/s12/certificates/s60"
        / "s60_mixed_cover_8.txt.gz",
        "2d0e456ea86cceeadc92d9f8fa7d468ba570a16d00d7343ebfbfb0b3b3b12a41",
        "6b7f0f79",
        (),
        80,
    ),
    77: Case(
        "n77",
        WAND125 / "k2m4_n77_L9/n77_mixed_cover_9.txt.gz",
        "47b57cfe38cbfdbcf5320e59caffe712f4ef32df8aad42b0d7f697de6d26cdd7",
        "6b7f0f79",
        ("--pair-points",),
        90,
    ),
    61: Case(
        "n61",
        WAND125_N61 / "cover.txt.gz",
        "bcb66c7910ef844ce8d39c423d7a5a419bd530a344689331f7665ba6971d0374",
        "6b7f0f79",
        ("--pair-points",),
        80,
    ),
    # Benjamin Greff's covers, whose verify.sh runs zmx2 cert --d4 --uncert-cap 200000
    # and leaves the roots it does not certify to zm_mixed.py's sub-roots.
    76: Case(
        "n76",
        BENGREFF_S76 / "s76_cover_v5.txt.gz",
        "b6a1214b99f00e5dd136d74c8d87bccd178df38a1063b2c7be90517eb2b862b2",
        "6b7f0f79",
        (),
        90,
        ("--uncert-cap", "200000"),
    ),
    95: Case(
        "n95",
        BENGREFF_S95 / "s95_cover_v2.txt.gz",
        "8b2d2152867585c82920bc90c6c3ec2a2458ef2ba57311ccd7dd436d1344cb7c",
        "6b7f0f79",
        (),
        100,
        ("--uncert-cap", "200000"),
    ),
    # Mohsen Khalili and Sara Gharabaghi's cover, whose verify.sh runs zmx2 cert --d4 and
    # --full with no other flag at evand/square-packing@659ee62.
    44: Case(
        "n44",
        KHALILI_S44 / "s44_cover_7.txt.gz",
        "c9fde0f1e7013f3f61f4a8d673b6bcaf9c5e54c914b6462164d7326ba254cae0",
        "e2bb84e9",
        (),
        70,
    ),
}


class DigestError(RuntimeError):
    """A retained input does not have the SHA-256 the record states."""


def _checked(data: bytes, expected: str, what: str) -> bytes:
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected:
        raise DigestError(f"{what}: SHA-256 {actual}, expected {expected}")
    return data


def _write_checked(target: Path, data: bytes) -> None:
    if target.exists() and target.read_bytes() == data:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)


def build(checker: str, work: Path) -> Path:
    """Assemble the crate for ``checker`` under ``work`` and build it; return the binary."""
    source, digest = CHECKERS[checker]
    crate = work / checker / "verify2"
    for relative, retained, expected in CRATE_FILES:
        _write_checked(
            crate / relative, _checked(retained.read_bytes(), expected, str(retained))
        )
    _write_checked(
        crate / "src/bin/zmx2.rs", _checked(source.read_bytes(), digest, str(source))
    )
    binary = crate / "target/release/zmx2"
    receipt = work / checker / "build.log"
    if binary.exists() and receipt.exists():
        return binary
    fields = replay_receipt.run(
        ["cargo", "build", "--release", "--bin", "zmx2"],
        receipt=receipt,
        cwd_label=(
            f"verify2/ assembled from retained bytes: zmx2.rs {digest} "
            f"({source.relative_to(REPO)}), Cargo.toml, Cargo.lock and src/main.rs "
            f"from {CRATE.relative_to(REPO)}"
        ),
        python_note="not used by this command",
        chdir=crate,
    )
    if fields["exit"] != 0:
        raise SystemExit(f"cargo build failed; see {receipt}")
    toolchain = subprocess.run(
        ["rustc", "--version"], capture_output=True, text=True, check=True
    ).stdout
    with receipt.open("a", encoding="utf-8") as out:
        out.write(f"# rustc: {toolchain.strip()}\n")
        out.write(f"# binary sha256: {hashlib.sha256(binary.read_bytes()).hexdigest()}\n")
    return binary


def root_span(text: str | None, cells: int) -> tuple[int, int]:
    if text is None:
        return 0, cells - 1
    low, _, high = text.partition("-")
    first, last = int(low), int(high)
    if not 0 <= first <= last < cells:
        raise SystemExit(f"region {text!r} is not within 0-{cells - 1}")
    return first, last


def run_case(
    n: int,
    mode: str,
    *,
    work: Path,
    out: Path,
    threads: int,
    x: str | None,
    y: str | None,
    time_limit: float | None = None,
) -> int:
    """Run ``zmx2 cert`` on case ``n`` and return its exit status."""
    case = CASES[n]
    stage, data = _stage(case, work)
    cover = stage / "certificates" / case.cover.name.removesuffix(".gz")
    _write_checked(cover, data)
    return _sweep(
        case,
        mode,
        cover,
        name=case.name,
        cwd_label=(
            f"s12/ staged by devtools.replay_evand_zmx2: zmx2.rs "
            f"{CHECKERS[case.checker][1]} built from retained bytes; cover {case.sha256} "
            f"decompressed from {case.cover.relative_to(REPO)}"
        ),
        out=out,
        threads=threads,
        x=x,
        y=y,
        time_limit=time_limit,
        listing=case.listing,
    )


def _stage(case: Case, work: Path) -> tuple[Path, bytes]:
    """Build the case's checker, link it into ``work/s12``; return that and the cover."""
    binary = build(case.checker, work)
    stage = work / "s12"
    data = gzip.decompress(case.cover.read_bytes())
    _checked(data, case.sha256, f"{case.cover} (decompressed)")
    link = stage / "verify2"
    if link.is_symlink() or link.exists():
        link.unlink() if link.is_symlink() else shutil.rmtree(link)
    stage.mkdir(parents=True, exist_ok=True)
    link.symlink_to(binary.parents[2], target_is_directory=True)
    return stage, data


def _sweep(
    case: Case,
    mode: str,
    cover: Path,
    *,
    name: str,
    cwd_label: str,
    out: Path,
    threads: int,
    x: str | None,
    y: str | None,
    time_limit: float | None = None,
    listing: Sequence[str] = (),
) -> int:
    """Run ``zmx2 cert`` on the staged ``cover`` under a receipt; return its exit status.

    ``listing`` (`Case.listing`) is passed after the case's flags and named in neither the
    file name nor the region.
    """
    cells = case.cells if mode == "full" else case.cells // 2
    (x0, x1), (y0, y1) = root_span(x, cells), root_span(y, cells)
    stage = cover.parents[1]
    flags = "".join("_" + flag.strip("-").replace("-", "") for flag in case.flags)
    region = "" if (x is None and y is None) else f"_x{x0}-{x1}_y{y0}-{y1}"
    name = f"{name}_zmx2_{mode}{flags}{region}"
    roots = out / f"{name}_roots.log"
    receipt = out / f"{name}.log"
    resume = 0
    while receipt.exists():
        resume += 1
        receipt = out / f"{name}_resume{resume}.log"
    command = [
        "verify2/target/release/zmx2",
        "cert",
        f"certificates/{cover.name}",
        f"--{mode}",
        *case.flags,
        *listing,
        "--threads",
        str(threads),
        "--log",
        str(roots),
    ]
    if region:
        command += ["--xlo", str(x0), "--xhi", str(x1), "--ylo", str(y0), "--yhi", str(y1)]
    fields = replay_receipt.run(
        command,
        receipt=receipt,
        cwd_label=cwd_label + (f"; resumes the root log of {name}.log" if resume else ""),
        python_note="not used by this command",
        chdir=stage,
        time_limit=time_limit,
    )
    return int(fields["exit"])  # type: ignore[call-overload]


# --- negative controls -----------------------------------------------------------------

#: The mutations ``control`` applies; each removes whole D4 orbits, keeping invariance.
MUTATIONS = ("drop-heaviest-point", "drop-second-heaviest-point", "drop-heaviest-segment")

#: The eight symmetries of the square: (swap x and y, then reflect x, then reflect y).
D4: tuple[tuple[bool, bool, bool], ...] = tuple(
    (swap, flip_x, flip_y)
    for swap in (False, True)
    for flip_x in (False, True)
    for flip_y in (False, True)
)


@dataclass(frozen=True, slots=True)
class Mutation:
    """A mutated cover: its text, the mass it lost, and what was done."""

    text: str
    #: The total mass removed, exactly, in the cover's own unit (the integers over ``W``).
    removed: Fraction
    #: The rows dropped.
    rows: int
    detail: str


@dataclass(frozen=True, slots=True)
class Control:
    """A retained control: the mode it ran in and the root region that refuses it."""

    mode: str
    x: str
    y: str


#: The retained controls, in ``receipts/controls/`` of the packet holding each case's
#: replay. Each region was found by running the mutated cover over the roots around the
#: removed mass and keeping one refused root cell; s(32) runs ``--full`` with its
#: source's flags, the configuration of the run that accepted it at ``92a4cfe8``.
CONTROLS: dict[tuple[int, str], Control] = {
    (32, "drop-heaviest-point"): Control("full", "27-27", "7-7"),
    (32, "drop-second-heaviest-point"): Control("full", "17-17", "7-7"),
    (59, "drop-heaviest-point"): Control("d4", "14-14", "24-24"),
    (59, "drop-heaviest-segment"): Control("d4", "5-5", "38-38"),
    (60, "drop-heaviest-point"): Control("d4", "16-16", "17-17"),
    (60, "drop-heaviest-segment"): Control("d4", "5-5", "38-38"),
    (77, "drop-heaviest-point"): Control("d4", "44-44", "44-44"),
    (77, "drop-heaviest-segment"): Control("d4", "5-5", "41-41"),
    (61, "drop-heaviest-point"): Control("d4", "26-26", "8-8"),
    (61, "drop-second-heaviest-point"): Control("d4", "36-36", "36-36"),
    # Run at intake by the packets' receipts/programs/run_control.sh, with this module's
    # mutate and the 6b7f0f79 binary its build made, before these cases were registered.
    (76, "drop-heaviest-point"): Control("d4", "15-15", "15-15"),
    (76, "drop-heaviest-segment"): Control("d4", "5-5", "35-35"),
    (95, "drop-heaviest-point"): Control("d4", "15-15", "15-15"),
    (95, "drop-heaviest-segment"): Control("d4", "5-5", "45-45"),
    # Run at intake on 31 October by this module's control command, the region found by
    # sweeping each mutant over the roots around its removed orbit.
    (44, "drop-heaviest-point"): Control("d4", "23-23", "17-17"),
    (44, "drop-heaviest-segment"): Control("d4", "8-8", "9-9"),
}


def d4_image(
    point: tuple[int, int], edge: int, symmetry: tuple[bool, bool, bool]
) -> tuple[int, int]:
    """The image of ``point`` under one symmetry of ``[0, edge]^2`` (see ``D4``)."""
    swap, flip_x, flip_y = symmetry
    x, y = (point[1], point[0]) if swap else point
    return (edge - x if flip_x else x, edge - y if flip_y else y)


def _rewrite(line: str, values: Sequence[int]) -> str:
    """``line`` with its integers replaced, keeping any comment and the line ending."""
    content = line.rstrip("\r\n")
    _, mark, comment = content.partition("#")
    return " ".join(map(str, values)) + (f" #{comment}" if mark else "") + line[len(content) :]


def mutate(text: str, kind: str) -> Mutation:
    """Apply mutation ``kind`` (one of ``MUTATIONS``) to a cover in plain or mixed format.

    The rewrite is line-level, as ``zmx2`` reads the file: a row is a line with tokens
    once its ``#`` comment is removed, and only the rows the mutation removes and the
    count above them change. ``drop-heaviest-point`` removes every point at the D4
    images of the location carrying the most point mass (ties to the least ``(X, Y)``),
    ``drop-second-heaviest-point`` those of the heaviest location outside that orbit,
    and ``drop-heaviest-segment`` every segment that is a D4 image of the heaviest one
    with its weight. On a D4-invariant cover each removes the same mass at every image,
    so the result is still invariant.
    """
    lines = text.splitlines(keepends=True)
    rows = [(i, line.split("#", 1)[0].split()) for i, line in enumerate(lines)]
    rows = [(i, tokens) for i, tokens in rows if tokens]
    cursor = 1 if rows[0][1] == ["mixed", "1"] else 0
    mixed = cursor == 1

    def take(width: int) -> tuple[int, list[int]]:
        nonlocal cursor
        if cursor >= len(rows) or len(rows[cursor][1]) != width:
            raise ValueError(f"expected a row of {width} integers at row {cursor}")
        index, tokens = rows[cursor]
        cursor += 1
        return index, [int(token) for token in tokens]

    _, (side_num, side_den) = take(2)
    _, (denominator,) = take(1)
    _, (mass_denominator,) = take(1)
    point_count_row, (point_count,) = take(1)
    points = [take(3) for _ in range(point_count)]
    segment_count_row, segments = -1, []
    if mixed:
        segment_count_row, (segment_count,) = take(1)
        segments = [take(5) for _ in range(segment_count)]
        take(1)
    if cursor != len(rows):
        raise ValueError("trailing rows after the declared pieces")
    edge, remainder = divmod(side_num * denominator, side_den)
    if remainder:
        raise ValueError("the side is not a multiple of 1/D")

    if kind in ("drop-heaviest-point", "drop-second-heaviest-point"):
        weights: dict[tuple[int, int], int] = {}
        for _, (x, y, w) in points:
            weights[(x, y)] = weights.get((x, y), 0) + w
        ranked = sorted(weights, key=lambda p: (-weights[p], p))
        if not ranked:
            raise ValueError("the cover has no points")
        heaviest = ranked[0]
        orbit = {d4_image(heaviest, edge, g) for g in D4}
        if kind == "drop-second-heaviest-point":
            heaviest = next((p for p in ranked if p not in orbit), None)
            if heaviest is None:
                raise ValueError("the cover's points are one D4 orbit")
            orbit = {d4_image(heaviest, edge, g) for g in D4}
        dropped = [(i, v) for i, v in points if (v[0], v[1]) in orbit]
        count_row, remaining = point_count_row, len(points) - len(dropped)
        detail = (
            f"drops the {len(dropped)} point rows at the {len(orbit)} D4 images of "
            f"({heaviest[0]}, {heaviest[1]})/{denominator}, carrying "
            f"{weights[heaviest]}/{mass_denominator} each"
        )
    elif kind == "drop-heaviest-segment":
        if not segments:
            raise ValueError("the cover has no segments")

        def key(v: Sequence[int]) -> tuple[tuple[int, int], tuple[int, int], int]:
            a, b = sorted(((v[0], v[1]), (v[2], v[3])))
            return a, b, v[4]

        a, b, w = min((key(v) for _, v in segments), key=lambda k: (-k[2], k[0], k[1]))
        images = {(*sorted((d4_image(a, edge, g), d4_image(b, edge, g))), w) for g in D4}
        dropped = [(i, v) for i, v in segments if key(v) in images]
        count_row, remaining = segment_count_row, len(segments) - len(dropped)
        detail = (
            f"drops the {len(dropped)} segment rows at the {len(images)} D4 images of "
            f"{a}-{b}/{denominator}, carrying {w}/{mass_denominator} each"
        )
    else:
        raise ValueError(f"unknown mutation {kind!r}")
    new: dict[int, str] = {i: "" for i, _ in dropped}
    new[count_row] = _rewrite(lines[count_row], [remaining])
    out = "".join(new.get(i, line) for i, line in enumerate(lines))
    removed = sum(v[-1] for _, v in dropped)
    return Mutation(out, Fraction(removed, mass_denominator), len(dropped), detail)


def control_case(
    n: int,
    kind: str,
    *,
    work: Path,
    out: Path,
    threads: int,
    mode: str | None = None,
    x: str | None = None,
    y: str | None = None,
) -> int:
    """Run ``zmx2 cert`` on case ``n``'s cover mutated by ``kind``; return its exit status.

    The region and mode default to the retained control's; a mutated cover's run is
    meant to end ``NOT VERIFIED``, which the caller reads from the receipt.
    """
    case = CASES[n]
    retained = CONTROLS.get((n, kind))
    mode = mode or (retained.mode if retained else "d4")
    x = x or (retained.x if retained else None)
    y = y or (retained.y if retained else None)
    if x is None or y is None:
        raise SystemExit("a control needs a region: give --x and --y")
    stage, data = _stage(case, work)
    mutation = mutate(data.decode("ascii"), kind)
    mutated = mutation.text.encode("ascii")
    digest = hashlib.sha256(mutated).hexdigest()
    if digest == case.sha256:
        raise SystemExit(f"{kind} left the cover's bytes unchanged")
    stem = case.cover.name.removesuffix(".gz").removesuffix(".txt")
    cover = stage / "certificates" / f"{stem}_{kind}.txt"
    _write_checked(cover, mutated)
    return _sweep(
        case,
        mode,
        cover,
        name=f"{case.name}_control_{kind}",
        cwd_label=(
            f"s12/ staged by devtools.replay_evand_zmx2 control: zmx2.rs "
            f"{CHECKERS[case.checker][1]} built from retained bytes; cover {digest}, the "
            f"{kind} mutation of {case.sha256} decompressed from "
            f"{case.cover.relative_to(REPO)}: {mutation.detail}, removing mass "
            f"{mutation.removed}"
        ),
        out=out,
        threads=threads,
        x=x,
        y=y,
    )


# --- zm_mixed.py on a split cover's sub-roots --------------------------------------------

#: ``zm_mixed.py`` and the files it imports, as the s(76) and s(95) sources' ``verify.sh``
#: pins them at evand ``b91d70b6``: name, retained copy, SHA-256.
ZM_MIXED_FILES = (
    (
        "zm_mixed.py",
        WEB / "evand-square-packing-2026-09-28/square-packing/s12/search/zm_mixed.py",
        "ee3e2915349b8795128417bca6414b205d526db9f01f88cd4cd32c32e8d760ac",
    ),
    (
        "mixed_cover.py",
        WEB / "evand-square-packing-2026-09-28/square-packing/s12/search/mixed_cover.py",
        "bb89de15ecf5821dd7e1a36ebab8a50d792a406b7fb0f5cb38059f99ef74aae5",
    ),
    (
        "zeromargin.py",
        WEB / "evand-square-packing-2026-09-26/square-packing/s12/search/zeromargin.py",
        "640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab",
    ),
)
#: The flags those ``verify.sh`` scripts pass ``zm_mixed.py cert`` for every sub-root.
ZM_MIXED_FLAGS = (
    "--d4",
    "--cert-mode",
    "--disj",
    "--chain-from",
    "0",
    "--pitch",
    "1/20",
    "--ubins",
    "16",
    "--depth",
    "24",
    "--nproc",
    "1",
)
#: Each split cover's sub-roots, as its source lists them: ``id cx_lo cx_hi cy_lo cy_hi
#: u_lo u_hi`` per line.
ZM_MIXED_JOBS = {
    76: WEB / "bengreff-s76-certificate-2026-10-14/s76-certificate/records/zm_mixed/jobs.txt",
    95: WEB / "bengreff-s95-certificate-2026-10-15/s95-certificate/records/zm_mixed/jobs.txt",
}
#: The bounds' flags, in the order of a jobs line.
ZM_MIXED_BOUNDS = ("--cx-lo", "--cx-hi", "--cy-lo", "--cy-hi", "--u-lo", "--u-hi")


def zm_mixed_jobs(n: int) -> list[tuple[str, tuple[str, ...]]]:
    """The case's sub-roots: each job's id and its six bounds."""
    rows = [line.split() for line in ZM_MIXED_JOBS[n].read_text(encoding="ascii").splitlines()]
    jobs = [(row[0], tuple(row[1:])) for row in rows if row]
    if any(len(bounds) != len(ZM_MIXED_BOUNDS) for _, bounds in jobs):
        raise ValueError(f"{ZM_MIXED_JOBS[n]}: a line is not an id and six bounds")
    return jobs


def zm_mixed_command(
    python: str, stage: Path, cover: Path, bounds: Sequence[str], records: Path
) -> list[str]:
    """One sub-root's ``zm_mixed.py cert`` command line."""
    limits = [token for pair in zip(ZM_MIXED_BOUNDS, bounds, strict=True) for token in pair]
    return [
        python,
        "-I",
        "-u",
        str(stage / "zm_mixed.py"),
        "cert",
        str(cover),
        *ZM_MIXED_FLAGS,
        *limits,
        "--resume",
        str(records),
    ]


def zm_mixed_case(
    n: int,
    *,
    work: Path,
    out: Path,
    only: Sequence[str] | None = None,
    python: str = sys.executable,
) -> int:
    """Run ``zm_mixed.py cert`` on the case's sub-roots; return the largest exit status."""
    case = CASES[n]
    jobs = zm_mixed_jobs(n)
    if only:
        known = {job for job, _ in jobs}
        if unknown := sorted(set(only) - known):
            raise SystemExit(f"no such job: {', '.join(unknown)}")
        jobs = [(job, bounds) for job, bounds in jobs if job in set(only)]
    stage = work / "zm_mixed"
    for name, retained, expected in ZM_MIXED_FILES:
        _write_checked(stage / name, _checked(retained.read_bytes(), expected, str(retained)))
    data = _checked(
        gzip.decompress(case.cover.read_bytes()), case.sha256, f"{case.cover} (decompressed)"
    )
    cover = stage / case.cover.name.removesuffix(".gz")
    _write_checked(cover, data)
    target = out / f"{case.name}_zm_mixed"
    target.mkdir(parents=True, exist_ok=True)
    version = subprocess.run(
        [python, "--version"], capture_output=True, text=True, check=True
    ).stdout.strip()
    label = (
        "zm_mixed/ staged by devtools.replay_evand_zmx2 zm-mixed: "
        + ", ".join(f"{name} {digest}" for name, _, digest in ZM_MIXED_FILES)
        + f" (retained evand packets); cover {case.sha256} decompressed from "
        + str(case.cover.relative_to(REPO))
    )
    worst = 0
    for job, bounds in jobs:
        fields = replay_receipt.run(
            zm_mixed_command(python, stage, cover, bounds, target / f"j{job}.jsonl"),
            receipt=target / f"j{job}.log",
            cwd_label=label,
            python_note=f"{python} ({version}), run with -I",
            chdir=stage,
        )
        worst = max(worst, int(fields["exit"]))  # type: ignore[call-overload]
    return worst


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    build_parser = commands.add_parser("build", help="assemble and build one checker version")
    build_parser.add_argument("--checker", choices=sorted(CHECKERS), required=True)
    build_parser.add_argument("--work", type=Path, required=True)
    run_parser = commands.add_parser("run", help="replay one case's cover")
    run_parser.add_argument("--case", type=int, choices=sorted(CASES), required=True)
    run_parser.add_argument("--mode", choices=("d4", "full"), required=True)
    run_parser.add_argument("--work", type=Path, required=True)
    run_parser.add_argument("--out", type=Path, required=True)
    run_parser.add_argument("--threads", type=int, default=4)
    run_parser.add_argument("--x", help="root columns LO-HI (inclusive)")
    run_parser.add_argument("--y", help="root rows LO-HI (inclusive)")
    run_parser.add_argument(
        "--time-limit",
        type=float,
        help="stop after this many seconds with exit 3; the same command resumes",
    )
    control_parser = commands.add_parser("control", help="run a mutated cover (stage 4)")
    control_parser.add_argument("--case", type=int, choices=sorted(CASES), required=True)
    control_parser.add_argument("--mutation", choices=MUTATIONS, required=True)
    control_parser.add_argument("--mode", choices=("d4", "full"), help="default: CONTROLS")
    control_parser.add_argument("--work", type=Path, required=True)
    control_parser.add_argument("--out", type=Path, required=True)
    control_parser.add_argument("--threads", type=int, default=1)
    control_parser.add_argument("--x", help="root columns LO-HI (default: CONTROLS)")
    control_parser.add_argument("--y", help="root rows LO-HI (default: CONTROLS)")
    zm_parser = commands.add_parser(
        "zm-mixed", help="run zm_mixed.py on a split cover's sub-roots"
    )
    zm_parser.add_argument("--case", type=int, choices=sorted(ZM_MIXED_JOBS), required=True)
    zm_parser.add_argument("--work", type=Path, required=True)
    zm_parser.add_argument("--out", type=Path, required=True)
    zm_parser.add_argument("--only", nargs="+", help="job ids from the source's jobs.txt")
    zm_parser.add_argument("--python", default=sys.executable, help="an interpreter with numpy")
    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            print(build(args.checker, args.work.resolve()))
            return 0
        if args.command == "zm-mixed":
            return zm_mixed_case(
                args.case,
                work=args.work.resolve(),
                out=args.out.resolve(),
                only=args.only,
                python=args.python,
            )
        if args.command == "control":
            return control_case(
                args.case,
                args.mutation,
                work=args.work.resolve(),
                out=args.out.resolve(),
                threads=args.threads,
                mode=args.mode,
                x=args.x,
                y=args.y,
            )
        return run_case(
            args.case,
            args.mode,
            work=args.work.resolve(),
            out=args.out.resolve(),
            threads=args.threads,
            x=args.x,
            y=args.y,
            time_limit=args.time_limit,
        )
    except (DigestError, ValueError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
