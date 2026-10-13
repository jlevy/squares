"""Audit, sample and price Hosono's independent run of ValidTilt9.

T-081's lower half at every ``k >= 8`` rests on ValidTilt9: every closed unit square in
``[0, 9]^2`` with centre in ``[0, 9/2]^2`` and angle ``theta = 2 arctan u``, ``u > 0``,
``u^2 + 2u <= 1``, has mass at least 1 under Evan Daniel's box cover ``K4_k008_box9.txt``.
Daniel's ``qx2_zm.py`` decides it in the source's run; wand125/valid7-independent-check
at ``c561dbb3`` reports a second decision by Hosono's separately written checker, the
one whose Valid7 run this repository replayed for T-064. Its run is published as three
JSON-lines records in the release ``records-tilt9-v1``, pinned by SHA-256 in the
2026-10-06 packet and not retained, so every subcommand that reads them takes the
directory of the downloaded ``.jsonl.gz`` files.

``audit --records DIR [--out JSON]``
    Checks what the source's ``check_record.py --claim tilt`` leaves out, and reads
    nothing it writes: each file, compressed and decompressed, has the digest of the
    retained ``release/records.sha256``; each header names the cover the evand packet
    retains and checker files this packet retains, by SHA-256; the roots of the three
    records are exactly the 45 x 45 x 14 grid over centres ``[0, 9/2]^2`` and ``u`` in
    ``[0, 7/16]``, each once, split by centre ``x`` as ``MERGE.md`` says; that grid covers
    the statement's region, ``7/16 > sqrt 2 - 1``; no root has an uncertified box or a
    counterexample; the leaf counts and CPU are the README's; and each root's leaves are
    consistent with the driver options ``MERGE.md`` and the run notes give for its place
    in its record (`PHASES`).
``stage --work DIR``
    Copies the retained checker and the decompressed cover into ``DIR/v1`` and
    ``DIR/v2``, one for each driver the run used, refusing any file whose SHA-256 is not
    the one the records' headers name.
``sample --records DIR --per-phase N [--heavy H] [--seed S] [--max-seconds T] [--python P]``
    Chooses up to ``N`` light roots of each phase, those of at most ``T`` recorded
    seconds, spread over the phase's recorded cost, and ``H`` heavy roots spread over
    the rest. It writes, for each light root, the command that re-runs that one root
    with its phase's driver and options (``replay``), and for a root of an earlier phase
    also the command under the last phase's options (``final``); a heavy root is re-run
    under the last phase's options only.
``run --sample JSON --work DIR [--jobs J] [--stratum light|heavy]``
    Runs the sampled commands in the staged work dirs, ``J`` at a time, each under
    ``devtools.replay_receipt``; a run whose receipt passed is not run again.
``compare --records DIR --sample JSON --work DIR [--out JSON]``
    Reads each sampled run's record and receipt: the header names the staged files; the
    argv sets exactly the phase's options; the run holds the one published root, with no
    uncertified box and no counterexample, and for a ``replay`` run the published leaf
    list; and the receipt ends with exit 0. It then prices a full replay: each phase's
    and stratum's recorded CPU times the ratio of this host's receipt CPU to the recorded
    CPU over its sample (`price`), once as published (``replay``) and once under the
    last phase's options (``final``). A run under its root's own options is a replay
    whatever its mode (`replays`). It also counts the distinct roots re-decided and the
    share of the run's recorded cost they hold.

``control --work DIR [--python P]``
    Writes two covers each lighter by a relative ``1e-4`` on one tight family (`mutants`)
    into ``DIR/v2/cover`` and runs the checker's own entry points on them and on the
    original: Tier B on a box at the wall family must accept the original and refuse M1,
    and the driver on roots inside the Lebesgue square must verify the original and
    find a counterexample under M2.

It decides nothing about a leaf: the checker does. From ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.audit_validtilt9_independent \\
        audit --records DIR --out RECEIPT.json
"""

from __future__ import annotations

import argparse
import contextlib
import gzip
import hashlib
import json
import random
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from collections.abc import Iterator, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from fractions import Fraction
from itertools import pairwise
from pathlib import Path
from typing import cast

from strif import atomic_write_text

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
PACKET = WEB / "wand125-valid7-independent-check-2026-10-06"
TREE = PACKET / "valid7-independent-check"
SUMS = PACKET / "release/records.sha256"
#: The cover is over 1,000 lines, so the evand packet stores it as deterministic gzip.
COVER_GZ = (
    WEB / "evand-square-packing-2026-10-03/square-packing/s12/certificates/k2m4"
    / "K4_k008_box9.txt.gz"
)  # fmt: skip
COVER_KEY = "cover/K4_k008_box9.txt"
COVER_SHA256 = "4151d7c4059d5dcf56130c9373e6b5b60635e1a4250f46562d7ecc4d64a27801"
#: The two drivers: v1 is the Valid7 run's V2 driver, which this packet keeps at
#: ``versions/V2/run_all.py``; v2 adds ``--bmid-u`` and ``--bmid-w`` and is ``src/``'s.
DRIVERS = {
    "v1": (
        "versions/V2/run_all.py",
        "899144f999e69cb0b1e95063e6e9c208cca6eedca51d11c139cfd84d229ca476",
    ),
    "v2": (
        "src/run_all.py",
        "cd6627de26d77dbf4876068612cf1bece9b52f66eeb0f7edbe5fa127dd5d9dda",
    ),
}
#: The checking code, the same throughout the run: ``src/`` at ``da469ec``, unchanged at
#: ``c561dbb``. ``check_record.py`` is not named by the headers and does not decide a leaf.
CODE = {
    "tier_a.py": "bb23e935a2e30901d1f9bc6e455ff60c6045826dfb8edf1807c065fdf1a4c9b1",
    "tier_b.py": "ca72a14909e3d242ad2006a782a795fb9cb5a27d81df1422f28aa882049505bb",
    "tier_b2.py": "5fb2a7cc0cb2b2a11832c37bda4fb5f6b0da093117348619a4e6b54daf3be12f",
    "solver.py": "aa462c15f72309912da3ef231d443ea6690ecccf4cbc9f94a5bd7797681b674c",
    "rf.py": "5a86a6a72700574d7ab5f730d86e1d48d6670c4c89b684c770553b5c29b55c1b",
    "cover.py": "939066811ba2539f77fe55670093c0643e91998206bd77a7b8c30dedc6e315dd",
}
#: Daniel's checker of the same statement, retained by the 2026-10-03 evand packet.
QX2_CHECKER = (
    WEB / "evand-square-packing-2026-10-03/square-packing/s12/certificates/k2m4/qx2_zm/checker"
)
RECORDS = ("tilt9_a.jsonl", "tilt9_b.jsonl", "tilt9_c.jsonl")
SIDE = Fraction(9)
HALF = SIDE / 2
PITCH = Fraction(1, 10)
U_MAX = Fraction(7, 16)
UBINS = 14
#: ``MERGE.md``: machine 1 kept ``x < 38/10``, machine 2 ``x >= 39/10`` and the column.
SPLIT = {
    "tilt9_a.jsonl": (Fraction(0), Fraction(38, 10)),
    "tilt9_b.jsonl": (Fraction(39, 10), HALF),
    "tilt9_c.jsonl": (Fraction(38, 10), Fraction(39, 10)),
}
#: What the source's README and release state for the run.
STATED_LEAVES = {"CORE": 6_565_165, "TIERB2": 2_940_689, "EMPTY": 31_489}
STATED_CORE_HOURS = 766
#: Driver options by phase, as ``MERGE.md`` and the run notes give them.
OPTIONS: dict[str, tuple[str, tuple[str, ...]]] = {
    "amin-1/320": ("v1", ()),
    "amin-1/1280": ("v1", ("--amin", "1/1280")),
    "bmid-3/16": ("v2", ("--amin", "1/1280", "--bmid-u", "3/16", "--bmid-w", "1/20")),
    "bmid-7/16": ("v2", ("--amin", "1/1280", "--bmid-u", "7/16", "--bmid-w", "1/20")),
}
FINAL = "bmid-7/16"
#: Each record's roots in file order, cut into phases by the root counts the run notes
#: give at each change of options. ``tilt9_a.jsonl`` is machine 1's record without the
#: 350 pilot roots of ``[4, 9/2]^2`` that its first lines held, so each of machine 1's
#: counts (16,755 at 10-04 06:10 and 23,012 and 23,014 at 10-05 11:34 and 13:07) is 350
#: less here; machine 2's (2,432 and 2,587) start after its 350 copied pilot roots.
PHASES: dict[str, tuple[tuple[int, str], ...]] = {
    "tilt9_a.jsonl": ((16_405, "amin-1/320"), (22_662, "amin-1/1280"),
                      (22_664, "bmid-3/16"), (23_940, "bmid-7/16")),
    "tilt9_b.jsonl": ((350, "amin-1/320"), (2_432, "amin-1/1280"),
                      (2_587, "bmid-3/16"), (3_780, "bmid-7/16")),
    "tilt9_c.jsonl": ((630, "bmid-7/16"),),
}  # fmt: skip
#: ``run_all.py`` under the ``fork`` start method, so that a receipt counts its workers'
#: CPU (``devtools.plan_valid7_replay.FORK_LAUNCH``); the start method decides nothing.
FORK_LAUNCH = (
    "import multiprocessing, runpy, sys; multiprocessing.set_start_method('fork'); "
    "sys.argv = sys.argv[1:]; sys.path.insert(0, 'src'); "
    "runpy.run_path(sys.argv[0], run_name='__main__')"
)
TIER_B_WIDTH = Fraction(1, 10)
BMIN = Fraction(1, 640)
BMID_WIDTH = Fraction(1, 20)

Box = tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction]


@dataclass
class Root:
    """One root of a published record, as the audit and the sample need it."""

    record: str
    index: int
    box: Box
    cpu: float
    leaves: int
    phase: str
    problem: str = ""
    #: Whether it has a Tier B leaf off ``u = 0``, the only leaves a phase constrains.
    signed: bool = False


@dataclass
class RecordStats:
    """What one record file holds, read line by line."""

    name: str
    sha256_compressed: str = ""
    sha256_decompressed: str = ""
    header: dict[str, object] = field(default_factory=dict[str, object])
    roots: list[Root] = field(default_factory=list[Root])
    kinds: Counter[str] = field(default_factory=Counter[str])
    uncertified: int = 0
    counterexamples: int = 0


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def read_sums(path: Path) -> dict[str, str]:
    """``sha256sum`` lines as {file name: digest}."""
    sums: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, name = line.split(maxsplit=1)
        sums[name.lstrip("*")] = digest
    return sums


def _box(values: object) -> Box:
    return cast("Box", tuple(Fraction(str(v)) for v in cast("list[object]", values)))


def phase_of(record: str, index: int) -> str:
    """The phase of a record's ``index``-th root, by `PHASES`."""
    for end, phase in PHASES[record]:
        if index < end:
            return phase
    msg = f"{record} has no phase for root {index}"
    raise ValueError(msg)


def leaf_problem(phase: str, leaves: Sequence[tuple[Box, str]]) -> str:
    """Why a root's Tier B leaves cannot come from its phase's options, or ``""``.

    A box not touching ``u = 0`` reaches Tier B by the ``--amin`` rule, at a centre width
    of at most ``amin``, or by the ``--bmid-u`` rule, at most ``1/20``; a failed Tier B
    is split by its centre down to ``1/640``. So under ``--amin 1/320`` alone every such
    leaf is between 1/640 and 1/320 wide; under ``--amin 1/1280`` alone at most 1/1280;
    and under ``--bmid-u b`` one with ``|u| <= b`` is between 1/640 and 1/20, and any
    other at most 1/1280. Boxes touching ``u = 0`` follow the same rule in every phase.
    """
    _, options = OPTIONS[phase]
    amin = Fraction(options[options.index("--amin") + 1]) if "--amin" in options else None
    bmid = Fraction(options[options.index("--bmid-u") + 1]) if "--bmid-u" in options else None
    low = amin if amin is not None else Fraction(1, 320)
    for box, kind in leaves:
        if kind != "TIERB2":
            continue
        x0, x1, y0, y1, u0, u1 = box
        width = max(x1 - x0, y1 - y0)
        if u0 == 0 or u1 == 0:
            if width > TIER_B_WIDTH:
                return f"a Tier B leaf at u = 0 is {width} wide"
            continue
        if bmid is not None and max(abs(u0), abs(u1)) <= bmid:
            ok = BMIN <= width <= BMID_WIDTH
        elif amin is None:
            ok = BMIN <= width <= low
        else:
            ok = width <= low
        if not ok:
            return f"a Tier B leaf {width} wide at u in [{u0}, {u1}]"
    return ""


def _lines(path: Path) -> Iterator[tuple[bytes, dict[str, object]]]:
    with gzip.open(path, "rb") as handle:
        for raw in handle:
            yield raw, cast("dict[str, object]", json.loads(raw))


def read_record(path: Path) -> RecordStats:
    """Stream one ``.jsonl.gz`` record and keep what the audit and the sample need."""
    stats = RecordStats(path.name.removesuffix(".gz"), _sha256(path))
    digest = hashlib.sha256()
    for raw, entry in _lines(path):
        digest.update(raw)
        if "header" in entry:
            stats.header = cast("dict[str, object]", entry["header"])
            continue
        index = len(stats.roots)
        leaves = [
            (_box(leaf[0]), cast("str", leaf[1]))
            for leaf in cast("list[list[object]]", entry["leaves"])
        ]
        stats.kinds.update(kind for _, kind in leaves)
        stats.uncertified += len(cast("list[object]", entry["uncert"]))
        stats.counterexamples += len(cast("list[object]", entry["cex"]))
        phase = phase_of(stats.name, index)
        stats.roots.append(
            Root(
                stats.name,
                index,
                _box(entry["root"]),
                float(cast("float", entry["cpu"])),
                len(leaves),
                phase,
                leaf_problem(phase, leaves),
                any(k == "TIERB2" and b[4] != 0 and b[5] != 0 for b, k in leaves),
            )
        )
    stats.sha256_decompressed = digest.hexdigest()
    return stats


def expected_roots() -> set[Box]:
    """The grid of ``--centers 0 9/2 0 9/2 --u 0 7/16 --ubins 14`` at pitch 1/10."""
    cells = [(PITCH * i, PITCH * (i + 1)) for i in range(int(HALF / PITCH))]
    cuts = [U_MAX * k / UBINS for k in range(UBINS + 1)]
    return {
        (x0, x1, y0, y1, u0, u1)
        for x0, x1 in cells
        for y0, y1 in cells
        for u0, u1 in pairwise(cuts)
    }


def statement_problems(grid: set[Box]) -> list[str]:
    """The grid covers ValidTilt9's region: centres ``[0, 9/2]^2``, ``0 < u <= sqrt2 - 1``."""
    problems: list[str] = []
    xs = {(b[0], b[1]) for b in grid} | {(b[2], b[3]) for b in grid}
    if min(lo for lo, _ in xs) != 0 or max(hi for _, hi in xs) != HALF:
        problems.append("the centre grid is not [0, 9/2]")
    top = max(b[5] for b in grid)
    if min(b[4] for b in grid) != 0 or top * top + 2 * top < 1:
        problems.append(f"the u grid [0, {top}] does not reach sqrt 2 - 1")
    return problems


def grid_problems(records: Sequence[RecordStats]) -> list[str]:
    """All records' roots are the grid, each once, each record within its ``SPLIT``."""
    problems: list[str] = []
    seen: Counter[Box] = Counter()
    for stats in records:
        lo, hi = SPLIT[stats.name]
        seen.update(root.box for root in stats.roots)
        if outside := sum(1 for r in stats.roots if not lo <= r.box[0] < hi):
            problems.append(f"{stats.name}: {outside} roots outside {lo} <= x < {hi}")
    grid = expected_roots()
    if repeated := sum(1 for count in seen.values() if count > 1):
        problems.append(f"{repeated} roots appear more than once")
    if missing := len(grid - set(seen)):
        problems.append(f"{missing} grid roots are missing")
    if extra := len(set(seen) - grid):
        problems.append(f"{extra} roots are not grid roots")
    return problems


def header_problems(stats: RecordStats, tree: Path, cover_sha256: str) -> list[str]:
    """Every digest the header names is that of the retained file it names."""
    named = cast("dict[str, str]", stats.header.get("sha256", {}))
    if not named:
        return [f"{stats.name}: the header names no files"]
    problems: list[str] = []
    for key, digest in sorted(named.items()):
        base = Path(key).name
        if key == COVER_KEY:
            ok = digest == cover_sha256
        elif base == "run_all.py":
            ok = any(digest == want for _, want in DRIVERS.values())
        else:
            ok = CODE.get(base) == digest == _sha256(tree / "src" / base)
        if not ok:
            problems.append(f"{stats.name}: {key} is not a retained file ({digest[:16]})")
    if sorted(Path(k).name for k in named) != sorted([*CODE, "run_all.py", "K4_k008_box9.txt"]):
        problems.append(f"{stats.name}: the header names {sorted(named)}")
    return problems


def retained_problems(tree: Path) -> list[str]:
    """The packet's checker files are the ones the run's headers name."""
    problems = [
        f"{rel} is not {want[:16]}"
        for rel, want in DRIVERS.values()
        if _sha256(tree / rel) != want
    ]
    problems += [
        f"src/{name} is not {want[:16]}"
        for name, want in CODE.items()
        if _sha256(tree / "src" / name) != want
    ]
    return problems


def shared_code(tree: Path = TREE, checker: Path = QX2_CHECKER) -> dict[str, object]:
    """The lines of Hosono's checking code that also occur in Daniel's checker.

    Lines are compared with their indentation stripped. Blank lines, comments and lines
    shorter than 20 characters are left out, since every Python file shares them.
    """

    def lines(path: Path) -> set[str]:
        out: set[str] = set()
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if len(line) >= 20 and not line.startswith("#"):
                out.add(line)
        return out

    ours = {
        name: lines(tree / "src" / name) for name in [*CODE, "run_all.py", "check_record.py"]
    }
    theirs = set[str]().union(*(lines(path) for path in sorted(checker.glob("*.py"))))
    common = sorted(set[str]().union(*ours.values()) & theirs)
    return {
        "wand125_files": sorted(ours),
        "qx2_files": sorted(path.name for path in checker.glob("*.py")),
        "wand125_lines": sum(len(v) for v in ours.values()),
        "common_lines": common,
    }


def cover_bytes(path: Path = COVER_GZ) -> bytes:
    """The decompressed cover, refused unless it is ``4151d7c4``."""
    data = gzip.decompress(path.read_bytes())
    if hashlib.sha256(data).hexdigest() != COVER_SHA256:
        msg = f"{path} is not {COVER_SHA256[:16]}"
        raise SystemExit(msg)
    return data


def read_all(records_dir: Path) -> list[RecordStats]:
    """Read the three records in `RECORDS` order."""
    return [read_record(records_dir / f"{name}.gz") for name in RECORDS]


def phase_totals(records: Sequence[RecordStats]) -> dict[str, dict[str, float]]:
    """Each phase's root count and recorded CPU-hours."""
    roots: Counter[str] = Counter()
    seconds: defaultdict[str, float] = defaultdict(float)
    for stats in records:
        for root in stats.roots:
            roots[root.phase] += 1
            seconds[root.phase] += root.cpu
    return {
        phase: {"roots": roots[phase], "recorded_cpu_hours": round(seconds[phase] / 3600, 2)}
        for phase in OPTIONS
    }


def audit(records_dir: Path, *, tree: Path = TREE, sums: Path = SUMS) -> dict[str, object]:
    """Read the three records and return the receipt, with ``ok`` and every problem."""
    expected = read_sums(sums)
    cover_sha256 = hashlib.sha256(cover_bytes()).hexdigest()
    problems = retained_problems(tree)
    stats = read_all(records_dir)
    for record in stats:
        if expected.get(f"{record.name}.gz") != record.sha256_compressed:
            problems.append(f"{record.name}.gz does not have the release digest")
        if expected.get(record.name) != record.sha256_decompressed:
            problems.append(f"{record.name} does not have the release digest")
        problems += header_problems(record, tree, cover_sha256)
        if record.uncertified or record.counterexamples:
            bad = f"{record.uncertified} uncertified, {record.counterexamples} counterexamples"
            problems.append(f"{record.name}: {bad}")
        inconsistent = [root for root in record.roots if root.problem]
        problems += [
            f"{record.name} root {root.index} ({root.phase}): {root.problem}"
            for root in inconsistent[:10]
        ]
    grid = expected_roots()
    problems += statement_problems(grid)
    problems += grid_problems(stats)
    kinds = sum((record.kinds for record in stats), Counter[str]())
    if dict(kinds) != STATED_LEAVES:
        problems.append(f"leaf kinds {dict(kinds)}, the source states {STATED_LEAVES}")
    cpu = sum(root.cpu for record in stats for root in record.roots)
    return {
        "kind": "validtilt9-independent-records-audit/v1",
        "ok": not problems,
        "problems": problems,
        "records": [
            {
                "name": record.name,
                "sha256_compressed": record.sha256_compressed,
                "sha256_decompressed": record.sha256_decompressed,
                "header_argv": record.header.get("argv"),
                "header_sha256": record.header.get("sha256"),
                "roots": len(record.roots),
                "leaves": dict(sorted(record.kinds.items())),
                "uncertified": record.uncertified,
                "counterexamples": record.counterexamples,
                "cpu_core_hours": round(sum(r.cpu for r in record.roots) / 3600, 2),
            }
            for record in stats
        ],
        "grid_roots": len(grid),
        "region": {
            "centres": ["0", str(HALF)],
            "u": ["0", str(U_MAX)],
            "u_bins": UBINS,
            "covers_sqrt2_minus_1": U_MAX * U_MAX + 2 * U_MAX >= 1,
        },
        "leaves": kinds.total(),
        "leaf_kinds": dict(sorted(kinds.items())),
        "cpu_core_hours": round(cpu / 3600, 2),
        "stated": {"leaf_kinds": STATED_LEAVES, "core_hours": STATED_CORE_HOURS},
        "phases": phase_totals(stats),
        "shared_code": shared_code(tree),
        "roots_whose_leaves_test_their_phase": {
            phase: sum(
                1 for r in stats for root in r.roots if root.signed and root.phase == phase
            )
            for phase in OPTIONS
        },
        "not_checked": (
            "No leaf's bound is recomputed here; check_record.py --recheck/--recheck-b "
            "re-certify a sample, and the run itself is the source's. The phase of a root "
            "is read from its place in its record; its leaves can only refute it."
        ),
    }


def stage(work: Path, *, tree: Path = TREE) -> dict[str, str]:
    """Copy each driver's checker and the cover into ``work/v1`` and ``work/v2``."""
    problems = retained_problems(tree)
    if problems:
        raise SystemExit("; ".join(problems))
    cover = cover_bytes()
    staged: dict[str, str] = {}
    for driver, (rel, _) in DRIVERS.items():
        root = work / driver
        (root / "src").mkdir(parents=True, exist_ok=True)
        (root / "cover").mkdir(exist_ok=True)
        (root / "runs").mkdir(exist_ok=True)
        (root / "receipts").mkdir(exist_ok=True)
        shutil.copyfile(tree / rel, root / "src/run_all.py")
        for name in CODE:
            shutil.copyfile(tree / "src" / name, root / "src" / name)
        (root / COVER_KEY).write_bytes(cover)
        for path in sorted(root.rglob("*")):
            if path.is_file() and "runs" not in path.parts and "receipts" not in path.parts:
                staged[path.relative_to(work).as_posix()] = _sha256(path)
    return staged


def root_command(box: Box, phase: str, record: str, python: str) -> list[str]:
    """``run_all.py`` on one root with a phase's options, run from that driver's work dir."""
    x0, x1, y0, y1, u0, u1 = (str(v) for v in box)
    _, options = OPTIONS[phase]
    return [
        python, "-c", FORK_LAUNCH, "src/run_all.py", COVER_KEY,
        "--centers", x0, x1, y0, y1, "--u", u0, u1, "--ubins", "1",
        *options, "--nproc", "1", "--record", record,
    ]  # fmt: skip


def run_id(root: Root, mode: str) -> str:
    """A file-name stem for one sampled run."""
    x0, _, y0, _, u0, _ = root.box
    cell = f"x{int(x0 * 10):02d}y{int(y0 * 10):02d}u{int(u0 * 32):02d}"
    return f"{mode}_{root.record.removesuffix('.jsonl')}_{root.index:05d}_{cell}"


def stratum(seconds: float, max_seconds: float) -> str:
    """``light`` for a root the sample may re-run as published, ``heavy`` above that."""
    return "light" if seconds <= max_seconds else "heavy"


def spread(pool: list[Root], count: int) -> list[Root]:
    """``count`` roots of ``pool``, sorted by cost, at evenly spaced cumulative cost.

    A root is taken where the running total of recorded CPU crosses ``(k + 1/2) / count``
    of the whole, so the sample follows where the replay's cost is, not where most roots
    are; a root is taken at most once.
    """
    total = sum(root.cpu for root in pool)
    picked: list[Root] = []
    acc, k = 0.0, 0
    for root in pool:
        acc += root.cpu
        while k < count and acc >= total * (k + 0.5) / count:
            if not picked or picked[-1] is not root:
                picked.append(root)
            k += 1
    return picked


def choose(
    records: Sequence[RecordStats],
    per_phase: int,
    heavy: int,
    seed: int,
    max_seconds: float,
) -> list[Root]:
    """Up to ``per_phase`` light roots of each phase, and ``heavy`` heavy roots overall.

    Light roots are those of at most ``max_seconds`` recorded, spread by `spread`. Heavy
    roots are spread the same way over every phase's heavy roots together; the sample
    re-runs them under the last phase's options only. Ties in cost are broken by
    ``seed``.
    """
    rng = random.Random(seed)
    roots = [root for record in records for root in record.roots if root.cpu > 0]
    rng.shuffle(roots)
    roots.sort(key=lambda root: root.cpu)
    chosen: list[Root] = []
    for phase in OPTIONS:
        pool = [r for r in roots if r.phase == phase and r.cpu <= max_seconds]
        chosen += spread(pool, per_phase)
    return chosen + spread([r for r in roots if r.cpu > max_seconds], heavy)


def strata_totals(
    records: Sequence[RecordStats], max_seconds: float
) -> dict[str, dict[str, float]]:
    """Each phase-and-stratum's root count and recorded CPU-hours, keyed ``phase/stratum``."""
    roots: Counter[str] = Counter()
    seconds: defaultdict[str, float] = defaultdict(float)
    for record in records:
        for root in record.roots:
            key = f"{root.phase}/{stratum(root.cpu, max_seconds)}"
            roots[key] += 1
            seconds[key] += root.cpu
    return {
        f"{phase}/{part}": {
            "roots": roots[f"{phase}/{part}"],
            "recorded_cpu_hours": round(seconds[f"{phase}/{part}"] / 3600, 3),
        }
        for phase in OPTIONS
        for part in ("light", "heavy")
    }


def sample(
    records_dir: Path,
    per_phase: int,
    *,
    heavy: int = 0,
    seed: int = 20261006,
    max_seconds: float = 600.0,
    python: str = "python3",
) -> dict[str, object]:
    """The sampled roots and the commands that re-run each, as published and finally."""
    stats = read_all(records_dir)
    runs: list[dict[str, object]] = []
    for root in choose(stats, per_phase, heavy, seed, max_seconds):
        part = stratum(root.cpu, max_seconds)
        if part == "heavy":
            modes = ["final"]
        elif root.phase == FINAL:
            modes = ["replay"]
        else:
            modes = ["replay", "final"]
        for mode in modes:
            phase = root.phase if mode == "replay" else FINAL
            name = run_id(root, mode)
            runs.append({
                "id": name,
                "mode": mode,
                "record": root.record,
                "index": root.index,
                "root": [str(v) for v in root.box],
                "published_phase": root.phase,
                "stratum": part,
                "phase": phase,
                "driver": OPTIONS[phase][0],
                "recorded_seconds": root.cpu,
                "run_record": f"runs/{name}.jsonl",
                "receipt": f"receipts/{name}.log",
                "command": root_command(root.box, phase, f"runs/{name}.jsonl", python),
            })  # fmt: skip
    return {
        "kind": "validtilt9-independent-sample/v1",
        "seed": seed,
        "per_phase": per_phase,
        "heavy": heavy,
        "max_seconds": max_seconds,
        "phases": phase_totals(stats),
        "strata": strata_totals(stats, max_seconds),
        "runs": runs,
    }


_FOOTER = re.compile(
    r"^# finished \S+; exit (?P<exit>-?\d+); wall (?P<wall>[\d.]+) s; CPU (?P<cpu>[\d.]+) s",
    re.MULTILINE,
)


def receipt_cpu(path: Path) -> tuple[int, float]:
    """A ``devtools.replay_receipt`` log's exit status and CPU seconds."""
    found = _FOOTER.findall(path.read_text(encoding="utf-8"))
    if not found:
        msg = f"{path} has no receipt footer"
        raise ValueError(msg)
    exit_code, _, cpu = cast("tuple[str, str, str]", found[-1])
    return int(exit_code), float(cpu)


def _leaf_keys(leaves: object) -> list[str]:
    return sorted(
        f"{[str(v) for v in cast('list[object]', leaf[0])]} {leaf[1]}"
        for leaf in cast("list[list[object]]", leaves)
    )


def published_leaves(
    records_dir: Path, wanted: set[tuple[str, int]]
) -> dict[tuple[str, int], list[str]]:
    """The sorted leaf lists of the wanted ``(record, index)`` roots."""
    out: dict[tuple[str, int], list[str]] = {}
    for name in RECORDS:
        index = -1
        for _, entry in _lines(records_dir / f"{name}.gz"):
            if "header" in entry:
                continue
            index += 1
            if (name, index) in wanted:
                out[name, index] = _leaf_keys(entry["leaves"])
    return out


def replays(run: dict[str, object]) -> bool:
    """Whether a run used its root's published options, so its leaves must be the same.

    A heavy root of the last phase is planned under the last phase's options, which are
    its own, so it is a replay of that root whatever its mode says.
    """
    return run["mode"] == "replay" or run["phase"] == run["published_phase"]


def run_problems(
    run: dict[str, object], work: Path, published: list[str]
) -> tuple[list[str], int]:
    """What is wrong with one sampled run's record, and how many leaves it holds."""
    name = cast("str", run["id"])
    root_dir = work / cast("str", run["driver"])
    lines = [
        cast("dict[str, object]", json.loads(line))
        for line in (root_dir / cast("str", run["run_record"]))
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    header = cast("dict[str, object]", lines[0].get("header", {})) if lines else {}
    problems: list[str] = []
    named = {
        Path(k).name: v for k, v in cast("dict[str, str]", header.get("sha256", {})).items()
    }
    want = {
        **CODE,
        "run_all.py": DRIVERS[cast("str", run["driver"])][1],
        "K4_k008_box9.txt": COVER_SHA256,
    }
    if named != want:
        problems.append(f"{name}: the header does not name the staged files")
    argv = [str(v) for v in cast("list[object]", header.get("argv", []))]
    if argv != cast("list[str]", run["command"])[3:]:
        problems.append(f"{name}: argv {argv} is not the sampled command's")
    roots = [entry for entry in lines[1:] if "root" in entry]
    if (
        len(roots) != 1
        or [str(v) for v in cast("list[object]", roots[0]["root"])] != run["root"]
    ):
        problems.append(f"{name}: the run does not hold exactly the sampled root")
        return problems, 0
    entry = roots[0]
    if cast("list[object]", entry["uncert"]) or cast("list[object]", entry["cex"]):
        problems.append(f"{name}: an uncertified box or a counterexample")
    leaves = _leaf_keys(entry["leaves"])
    if replays(run) and leaves != published:
        problems.append(f"{name}: leaves differ from the published root's")
    return problems, len(leaves)


def price(
    strata: dict[str, dict[str, float]],
    host: dict[tuple[str, str], float],
    recorded: dict[tuple[str, str], float],
    count: Counter[tuple[str, str]],
) -> dict[str, object]:
    """Host CPU-hours of a full replay, as published and under the last phase's options.

    Each phase-and-stratum's recorded CPU is scaled by the ratio of host receipt CPU to
    recorded CPU over its sampled runs in that mode, and ``ratio_from`` names the
    strata the ratio came from. A stratum with no sampled run takes the ratio of its
    phase's other stratum: heavy roots are not re-run as published. Under the last
    phase's options, the heavy roots re-run from earlier phases stand for every earlier
    phase's heavy roots, and the last phase's own roots are their replay sample.
    """
    out: dict[str, object] = {}
    for mode in ("replay", "final"):
        hours = 0.0
        rows: dict[str, object] = {}
        for key, total in strata.items():
            phase, part = key.rsplit("/", 1)
            other = "heavy" if part == "light" else "light"
            if phase == FINAL:
                candidates = [("replay", key)]
                fallback = [("replay", f"{phase}/{other}")]
            elif mode == "final" and part == "heavy":
                candidates = [("final", f"{p}/heavy") for p in OPTIONS if p != FINAL]
                fallback = [("final", f"{phase}/light")]
            else:
                candidates = [(mode, key)]
                fallback = [(mode, f"{phase}/{other}")]
            used = [c for c in candidates if recorded.get(c)] or [
                c for c in fallback if recorded.get(c)
            ]
            ratio = (
                sum(host[c] for c in used) / sum(recorded[c] for c in used) if used else None
            )
            estimate = None if ratio is None else ratio * total["recorded_cpu_hours"]
            hours += estimate or 0.0
            rows[key] = {
                "recorded_cpu_hours": total["recorded_cpu_hours"],
                "sampled": sum(count[c] for c in used),
                "ratio_from": [c[1] for c in used],
                "ratio": None if ratio is None else round(ratio, 3),
                "host_cpu_hours": None if estimate is None else round(estimate, 2),
            }
        out[mode] = {"host_cpu_hours": round(hours, 1), "strata": rows}
    return out


def compare(records_dir: Path, plan: dict[str, object], work: Path) -> dict[str, object]:
    """Check every sampled run and price the full replay from the sample."""
    runs = cast("list[dict[str, object]]", plan["runs"])
    wanted = {(cast("str", r["record"]), cast("int", r["index"])) for r in runs}
    published = published_leaves(records_dir, wanted)
    problems: list[str] = []
    host: defaultdict[tuple[str, str], float] = defaultdict(float)
    recorded: defaultdict[tuple[str, str], float] = defaultdict(float)
    count: Counter[tuple[str, str]] = Counter()
    rows: list[dict[str, object]] = []
    for run in runs:
        root_dir = work / cast("str", run["driver"])
        exit_code, cpu = receipt_cpu(root_dir / cast("str", run["receipt"]))
        if exit_code != 0:
            problems.append(f"{run['id']}: exit {exit_code}")
        found, leaves = run_problems(
            run, work, published[cast("str", run["record"]), cast("int", run["index"])]
        )
        problems += found
        key = (
            "replay" if replays(run) else "final",
            f"{cast('str', run['published_phase'])}/{cast('str', run['stratum'])}",
        )
        host[key] += cpu
        recorded[key] += cast("float", run["recorded_seconds"])
        count[key] += 1
        rows.append({
            "id": run["id"],
            "mode": "replay" if replays(run) else "final",
            "stratum": run["stratum"],
            "recorded_seconds": run["recorded_seconds"],
            "host_cpu_seconds": cpu,
            "leaves": leaves,
            "ok": not found and exit_code == 0,
        })  # fmt: skip
    strata = cast("dict[str, dict[str, float]]", plan["strata"])
    total = sum(t["recorded_cpu_hours"] for t in strata.values()) * 3600
    distinct = {
        (cast("str", r["record"]), cast("int", r["index"])): cast(
            "float", r["recorded_seconds"]
        )
        for r in runs
    }
    return {
        "kind": "validtilt9-independent-sample-compare/v1",
        "ok": not problems,
        "problems": problems,
        "runs": rows,
        "replays_matching_published_leaves": sum(
            1 for row in rows if row["mode"] == "replay" and row["ok"]
        ),
        "roots_re_decided": len(distinct),
        "share_of_recorded_cost": round(sum(distinct.values()) / total, 4) if total else 0.0,
        "sampled_host_cpu_hours": round(sum(host.values()) / 3600, 3),
        "sampled_recorded_hours": round(sum(recorded.values()) / 3600, 3),
        "recorded_cpu_hours": round(sum(t["recorded_cpu_hours"] for t in strata.values()), 2),
        "price": price(strata, host, recorded, count),
    }


def run_sample(
    plan: dict[str, object],
    work: Path,
    *,
    jobs: int = 2,
    strata: Sequence[str] = ("light", "heavy"),
) -> dict[str, object]:
    """Run each sampled command under ``devtools.replay_receipt``, ``jobs`` at a time.

    A run whose receipt already ends with exit 0 is skipped, so an interrupted sample is
    finished by running it again. Each run's record is removed first, since a run that
    did not finish would leave a partial one behind.
    """
    runs = [
        run for run in cast("list[dict[str, object]]", plan["runs"])
        if run["stratum"] in strata
    ]  # fmt: skip

    def one(run: dict[str, object]) -> tuple[str, int]:
        root_dir = work / cast("str", run["driver"])
        receipt = root_dir / cast("str", run["receipt"])
        if receipt.is_file():
            with contextlib.suppress(ValueError):
                if receipt_cpu(receipt)[0] == 0:
                    return cast("str", run["id"]), 0
        (root_dir / cast("str", run["run_record"])).unlink(missing_ok=True)
        label = (
            f"a work dir staged by devtools.audit_validtilt9_independent stage, driver "
            f"{run['driver']}; run_all.py unmodified, launched under the fork start method"
        )
        argv = [
            sys.executable, "-m", "devtools.replay_receipt", "--receipt", str(receipt),
            "--cwd-label", label,
            "--python-note", "a scratch venv: CPython 3.14.7 with python-flint 0.9.0",
            "--chdir", str(root_dir), "--", *cast("list[str]", run["command"]),
        ]  # fmt: skip
        done = subprocess.run(argv, check=False, cwd=REPO / "packing", capture_output=True)
        return cast("str", run["id"]), done.returncode

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        results = dict(pool.map(one, runs))
    failed = sorted(name for name, code in results.items() if code)
    return {
        "ok": not failed,
        "runs": len(results),
        "problems": [f"{n}: failed" for n in failed],
    }


#: The wall family's tightest squares at small tilt rest on the bottom wall with centre
#: ``x`` near 4.1, where the mass grows like ``1 + 0.158 u`` (found by a scan of
#: ``tier_a.core_bound`` at ``u = 1/2000``). M1 lightens every segment in their
#: footprint by a relative ``1e-4``; M2 lightens the Lebesgue square, inside which every
#: square has mass exactly 1. Each control runs one of the checker's own entry points on
#: the original cover, which must accept, and on the mutant, which must refuse.
WALL_REGION = (Fraction(18, 5), Fraction(23, 5), Fraction(0), Fraction(1))
WALL_BOX = ("81/20", "83/20", "1/2", "3/5", "0", "1/64")
LEBESGUE_ROOTS = ("--centers", "22/5", "9/2", "22/5", "9/2", "--u", "0", "1/16", "--ubins", "2")


def mutants(cover: bytes) -> dict[str, bytes]:
    """M1 (the wall family) and M2 (the Lebesgue square), each lighter by 1e-4."""
    lines = cover.decode().rstrip("\n").split("\n")
    denominator = int(lines[3].split("#")[0])
    x_lo, x_hi, y_lo, y_hi = WALL_REGION
    wall: list[str] = []
    changed = 0
    for line in lines:
        fields = line.split("#")[0].split()
        out = line
        if len(fields) == 5:
            x0, y0, x1, y1, w = (int(v) for v in fields)
            xs = (Fraction(x0, denominator), Fraction(x1, denominator))
            ys = (Fraction(y0, denominator), Fraction(y1, denominator))
            if all(x_lo <= x <= x_hi for x in xs) and all(y_lo <= y <= y_hi for y in ys):
                out = f"{x0} {y0} {x1} {y1} {w * 9999 // 10000}"
                changed += 1
        wall.append(out)
    region = f"[{x_lo}, {x_hi}] x [{y_lo}, {y_hi}]"
    wall.insert(1, f"# mutant M1: {changed} segments in {region} x (1 - 1e-4)")
    leb = list(lines)
    fields = leb[-1].split()
    if fields[0] != "4":
        msg = "the cover's last line is not its one polygon"
        raise SystemExit(msg)
    fields[1] = str(int(fields[1]) * 9999 // 10000)
    leb[-1] = " ".join(fields)
    leb.insert(1, "# mutant M2: Lebesgue square mass x (1 - 1e-4)")
    return {
        "M1_wall_1e-4.txt": ("\n".join(wall) + "\n").encode(),
        "M2_leb_1e-4.txt": ("\n".join(leb) + "\n").encode(),
    }


def control_commands(python: str) -> list[tuple[str, list[str], str]]:
    """Each control's name, command in ``v2``'s work dir, and what its output must hold."""
    tier_b = [python, "src/tier_b2.py"]
    driver = [python, "-c", FORK_LAUNCH, "src/run_all.py"]
    tail = ["--amin", "1/1280", "--nproc", "1", "--record", "/dev/null"]
    return [
        ("wall_original", [*tier_b, COVER_KEY, *WALL_BOX], "{'ok': True"),
        ("wall_M1", [*tier_b, "cover/M1_wall_1e-4.txt", *WALL_BOX], "{'ok': False"),
        ("lebesgue_original", [*driver, COVER_KEY, *LEBESGUE_ROOTS, *tail], "\nVERIFIED\n"),
        ("lebesgue_M2", [*driver, "cover/M2_leb_1e-4.txt", *LEBESGUE_ROOTS, *tail],
         "\nNOT VERIFIED\n"),
    ]  # fmt: skip


CONTROL_LABEL = (
    "a work dir staged by devtools.audit_validtilt9_independent stage, driver v2, "
    "with the mutant covers devtools.audit_validtilt9_independent control wrote"
)


def control(work: Path, *, python: str = "python3") -> dict[str, object]:
    """Write the two mutants into ``work/v2/cover`` and run the four controls."""
    root_dir = work / "v2"
    for name, data in mutants(cover_bytes()).items():
        (root_dir / "cover" / name).write_bytes(data)
    rows: list[dict[str, object]] = []
    problems: list[str] = []
    for name, command, expect in control_commands(python):
        receipt = root_dir / "receipts" / f"control_{name}.log"
        argv = [
            sys.executable, "-m", "devtools.replay_receipt", "--receipt", str(receipt),
            "--cwd-label", CONTROL_LABEL,
            "--python-note", "a scratch venv: CPython 3.14.7 with python-flint 0.9.0",
            "--chdir", str(root_dir), "--", *command,
        ]  # fmt: skip
        subprocess.run(argv, check=False, cwd=REPO / "packing", capture_output=True)
        text = receipt.read_text(encoding="utf-8")
        exit_code, cpu = receipt_cpu(receipt)
        found = expect in text
        if not found or exit_code != 0:
            problems.append(f"{name}: exit {exit_code}, expected {expect!r}")
        rows.append({"control": name, "expect": expect.strip(), "found": found,
                     "exit": exit_code, "cpu_seconds": cpu})  # fmt: skip
    return {
        "kind": "validtilt9-independent-controls/v1",
        "ok": not problems,
        "problems": problems,
        "mutants": {
            name: hashlib.sha256(data).hexdigest()
            for name, data in mutants(cover_bytes()).items()
        },
        "controls": rows,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    sub = parser.add_subparsers(dest="action", required=True)
    for action in ("audit", "stage", "sample", "run", "compare", "control"):
        p = sub.add_parser(action)
        p.add_argument("--out", type=Path, help="also write the result here")
        if action not in ("stage", "run", "control"):
            p.add_argument("--records", type=Path, required=True, help="the three .jsonl.gz")
        if action in ("stage", "run", "compare", "control"):
            p.add_argument("--work", type=Path, required=True)
        if action == "control":
            p.add_argument("--python", default="python3", help="interpreter of the checker")
        if action == "run":
            p.add_argument("--jobs", type=int, default=2)
            p.add_argument("--stratum", choices=["light", "heavy"], action="append")
        if action == "sample":
            p.add_argument("--per-phase", type=int, required=True)
            p.add_argument("--seed", type=int, default=20261006)
            p.add_argument("--heavy", type=int, default=0)
            p.add_argument("--max-seconds", type=float, default=600.0)
            p.add_argument("--python", default="python3", help="interpreter in the commands")
        if action in ("run", "compare"):
            p.add_argument("--sample", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.action == "audit":
        result = audit(args.records)
    elif args.action == "stage":
        result = {"staged": stage(args.work)}
    elif args.action == "sample":
        result = sample(
            args.records,
            args.per_phase,
            heavy=args.heavy,
            seed=args.seed,
            max_seconds=args.max_seconds,
            python=args.python,
        )
    elif args.action == "control":
        result = control(args.work, python=args.python)
    elif args.action == "run":
        plan = cast("dict[str, object]", json.loads(args.sample.read_text(encoding="utf-8")))
        strata = tuple(args.stratum or ("light", "heavy"))
        result = run_sample(plan, args.work, jobs=args.jobs, strata=strata)
    else:
        plan = cast("dict[str, object]", json.loads(args.sample.read_text(encoding="utf-8")))
        result = compare(args.records, plan, args.work)
    text = json.dumps(result, indent=2) + "\n"
    if args.out:
        atomic_write_text(args.out, text)
    for problem in cast("list[str]", result.get("problems", [])):
        print("PROBLEM", problem)
    if args.action == "audit":
        print(
            "VALIDTILT9_RECORDS_AUDIT_OK" if result["ok"] else "VALIDTILT9_RECORDS_AUDIT_FAILED"
        )
    elif not args.out:
        print(text, end="")
    return 0 if result.get("ok", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
