"""Replay Khalili and Gharabaghi's ``s(k^2 - 5) = k`` release from retained bytes.

Mohsen Khalili and Sara Gharabaghi's k2m5-family release (jlevy/squares#973, packet
``moh63-dev-k2m5-family-2026-11-13``) reduces every ``k >= 10`` to one board,
``certificate/sol_exact_box11.txt``, and decides that board with Evan Daniel's ``zmx2``
and ``qx2_zm.py`` at evand/square-packing@659ee62 and with the authors' Tight-Tile
checker. This tool runs the source's own programs on the retained bytes, each under a
``devtools.replay_receipt`` receipt, and compares what they print with the source's
records. It decides nothing about the board itself: what a run shows is in its receipt
and in the comparison it writes.

``stage --work DIR --cov PATH``
    Writes the retained tree to ``DIR/k2m5-family``, with ``tight_tile/cov.tar.xz``
    (pinned by digest, not retained) copied from ``PATH`` once it holds the digest the
    packet's manifest pins; stages ``qx2_zm.py`` and the three files it imports in
    ``DIR/qx2`` from the evand packets, whose digests the table below records; and writes
    ``DIR/shim/python3``, which runs a script under the given interpreter with ``-I`` and
    the script's own directory appended to ``sys.path``, so the source's sibling imports
    resolve and nothing it ships can shadow the standard library.
``fast --work DIR --out OUT [--python PATH]``
    Runs ``verification/verify.sh`` (its fast mode, unmodified) with the shim first on
    ``PATH``; receipt ``OUT/verify_fast.log``.
``build --work DIR``
    Builds ``zmx2`` e2bb84e9 by ``devtools.replay_evand_zmx2`` and a second copy with the
    source's ``verification/zmx2_print_all.patch`` applied, after checking that the patch
    touches that one file and replaces one line; receipt ``DIR/zmx2/print-all/build.log``.
``zmx2 --work DIR --out OUT --columns LIST``
    ``zmx2 cert0`` and, per column, the source's ``verify.sh --full`` command for the
    first-order D4 sweep, with the unpatched binary: receipts ``OUT/zmx2/cert0.log`` and
    ``OUT/zmx2/colNN.log``. A column already holding a finished receipt is skipped.
``root9632 --work DIR --out OUT``
    The patched ``zmx2`` on root 9632 with ``ZMX2_PRINT_ALL`` set and ``--uncert-cap
    100000000``, the cap ``tight_tile/run_cov.sh`` passes for its dumps (``zmx2``'s default,
    200, abandons a root at its 200th uncertified box, which the sweep's own records do,
    and the source's dump lists 6,850; the header prints no cap), ``qx2_zm.py`` on the
    source's cropped cover with the source's arguments, and the source's
    ``check_9632.py`` on the two outputs this tool wrote; receipts under ``OUT/r9632/``.
``controls --work DIR --out OUT [--only NAME ...]``
    The source's controls (``CONTROLS``), each command as its record shows it, receipts
    under ``OUT/controls/``.
``tight --work DIR --out OUT --jobs JOB ...``
    The source's ``run_tt.py`` on named tight-tile jobs (the output names of
    ``tight_tile/out/``), receipts under ``OUT/tight/``.
``compare --work DIR --out OUT``
    Compares every receipt under ``OUT`` with the source's record of the same run and
    writes ``OUT/compare.json``: each zmx2 column's census and uncertified boxes, the
    root-9632 dump and qx2 summary, each control's summary, and each tight-tile job's
    chart lines, timings aside. ``check_9632.py`` and ``cropped`` facts are added too.

Run from ``packing/`` with the project interpreter, which needs numpy for ``qx2_zm.py``::

    .venv/bin/python3 -m devtools.replay_k2m5_family stage --work W --cov COV
    nice -n 19 .venv/bin/python3 -m devtools.replay_k2m5_family zmx2 --work W --out O \\
        --columns 0-13
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from devtools import replay_evand_zmx2, replay_receipt
from devtools.retained_data import read_retained_bytes

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
PACKET = WEB / "moh63-dev-k2m5-family-2026-11-13"
TREE = PACKET / "k2m5-family"
MANIFEST = PACKET / "acquisition/upstream-subtree.sha256"
COV = "tight_tile/cov.tar.xz"
BOARD = "certificate/sol_exact_box11.txt"
PATCH = "verification/zmx2_print_all.patch"
CHECKER = "e2bb84e9"
#: ``qx2_zm.py`` and its imports at 659ee62: the retained copy and, for the reader, its
#: SHA-256 (the copies' custody is ``devtools.acquire_source --check``'s).
QX2_FILES = {
    "qx2_zm.py": (
        WEB / "evand-square-packing-2026-10-03/square-packing/s12/certificates/k2m4/qx2_zm"
        "/checker/qx2_zm.py",
        "6294052a37ce66c5d84b55afd606e3a52f463e22b876bf44b5aa903aefb7e737",
    ),
    "zm_mixed.py": (
        WEB / "evand-square-packing-2026-10-03/square-packing/s12/certificates/k2m4/qx2_zm"
        "/checker/zm_mixed.py",
        "1fd203469bb43a55ca7ce376b9717437e0970eead31941ec7fa100ab24d5ba95",
    ),
    "mixed_cover.py": (
        WEB / "evand-square-packing-2026-10-03/square-packing/s12/certificates/k2m4/qx2_zm"
        "/checker/mixed_cover.py",
        "bb89de15ecf5821dd7e1a36ebab8a50d792a406b7fb0f5cb38059f99ef74aae5",
    ),
    "zeromargin.py": (
        WEB / "evand-square-packing-2026-10-24/square-packing/search/zeromargin.py",
        "3cb95fb74ce44666654d6cc193c3f255bd07ba6c9afd864a6f93e364d428c5cc",
    ),
}
#: The first-order D4 sweep's flags, as ``verify.sh --full`` runs each column.
SWEEP = ("--d4", "--first-order", "--threads", "1", "--depth", "40", "--node-cap", "20000000")
COLUMNS = 55
#: The window the source ran ``qx2_zm.py`` on for root 9632 (``verification/r9632/zm.out``).
WINDOW = (
    "--cx-lo", "4.3224", "--cx-hi", "4.3264", "--cy-lo", "4.3199", "--cy-hi", "4.3239",
    "--u-lo", "0.0229", "--u-hi", "0.0272",
)  # fmt: skip
#: Runs ``sys.argv[1]`` as ``__main__`` with its directory appended to ``sys.path``; with
#: ``-I`` neither the script's directory nor the working directory comes first, so a file
#: the source ships cannot shadow a standard module. ``fork`` keeps pool workers inside
#: the receipt's CPU count, as ``devtools.plan_valid7_replay.FORK_LAUNCH`` does.
LAUNCH = (
    "import multiprocessing, os, runpy, sys; multiprocessing.set_start_method('fork'); "
    "sys.argv = sys.argv[1:]; "
    "sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0]))); "
    "runpy.run_path(sys.argv[0], run_name='__main__')"
)


@dataclass(frozen=True, slots=True)
class Run:
    """One recorded run of the source: its command, where it ran, and its record."""

    argv: tuple[str, ...]
    #: Relative to the staged tree.
    cwd: str
    #: The source's record of the same run, relative to the staged tree.
    record: str
    env: tuple[tuple[str, str], ...] = ()


#: The source's controls (``docs/CHECKING.md``), each with the command its record shows.
#: ``{zmx2}`` and ``{python}`` are filled in at run time; the qx2 control runs in ``qx2/``.
CONTROLS: dict[str, Run] = {
    "zmx2-real-x15y36": Run(
        ("{zmx2}", "cert", BOARD, "--d4", "--first-order", "--threads", "1", "--depth", "24",
         "--node-cap", "2000000", "--xlo", "15", "--xhi", "15", "--ylo", "36", "--yhi", "36",
         "--bins", "0-0"),
        ".", "verification/controls/z_real_x15y36.out",
    ),
    "zmx2-scale0999-x15y36": Run(
        ("{zmx2}", "cert", "verification/controls/scale0999_box11.txt", "--d4", "--first-order",
         "--threads", "1", "--depth", "24", "--node-cap", "2000000", "--xlo", "15", "--xhi",
         "15", "--ylo", "36", "--yhi", "36", "--bins", "0-0"),
        ".", "verification/controls/z_scale0999_x15y36.out",
    ),
    "zmx2-scale0993-x15y36": Run(
        ("{zmx2}", "cert", "verification/controls/scale0993_box11.txt", "--d4", "--first-order",
         "--threads", "1", "--depth", "24", "--node-cap", "2000000", "--xlo", "15", "--xhi",
         "15", "--ylo", "36", "--yhi", "36", "--bins", "0-0"),
        ".", "verification/controls/z_scale0993_x15y36.out",
    ),
    "qx2-scale0999-r9632": Run(
        ("{python}", "qx2_zm.py", "c9632_scale0999.txt", "--nproc", "1", *WINDOW, "--progress",
         "60", "--unc-out", "{out}/q9632_scale0999_unc.txt"),
        "qx2", "verification/controls/q9632_scale0999.out",
    ),
    "locality-onemutation": Run(
        ("{python}", "verification/locality_check.py", BOARD,
         "verification/controls/box12_onemutation.txt"),
        ".", "",
    ),
    # The real board certifies the control's region in 155 cells; the mutant is run to
    # 2,000 of the script's default 20,000, enough to show refused cells without the hour
    # the default takes, every cell left at the cap counting as refused.
    "tight-ctl-rise": Run(
        ("{python}", "ctl_rise.py", "ctl_rise.txt", "2000"), "tight_tile", "",
    ),
    "tight-ctl-rise-real": Run(
        ("{python}", "ctl_rise.py", "../" + BOARD), "tight_tile", "",
    ),
}  # fmt: skip


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def manifest() -> dict[str, str]:
    """Upstream path to SHA-256, from the packet's subtree manifest."""
    rows: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, _, path = line.partition("  ")
        rows[path.removeprefix("./")] = digest
    return rows


def _write(target: Path, data: bytes) -> None:
    if target.exists() and target.read_bytes() == data:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)


def stage(work: Path, cov: Path, python: str) -> Path:
    """Write the staged tree, the qx2 directory and the shim; return the tree."""
    tree = work / "k2m5-family"
    for path, pinned in manifest().items():
        # Retained files come from Git, whose custody is acquire_source --check's; the one
        # file pinned by digest and not retained comes from outside and is held to the pin.
        if path != COV:
            _write(tree / path, read_retained_bytes(TREE / path))
            continue
        data = cov.read_bytes()
        if sha256(data) != pinned:
            raise SystemExit(f"{cov}: SHA-256 {sha256(data)}, the packet pins {pinned}")
        _write(tree / path, data)
    qx2 = work / "qx2"
    for name, (retained, _) in QX2_FILES.items():
        _write(qx2 / name, retained.read_bytes())
    for name in ("c9632.txt",):
        _write(qx2 / name, (tree / "verification/r9632" / name).read_bytes())
    control = tree / "verification/controls/c9632_scale0999.txt"
    _write(qx2 / "c9632_scale0999.txt", control.read_bytes())
    shim = work / "shim/python3"
    shim.parent.mkdir(parents=True, exist_ok=True)
    shim.write_text(f'#!/bin/sh\nexec {python} -I -c "{LAUNCH}" "$@"\n', encoding="utf-8")
    shim.chmod(0o755)
    return tree


def _receipt(
    argv: Sequence[str],
    receipt: Path,
    *,
    chdir: Path,
    label: str,
    python: str,
    env: dict[str, str] | None = None,
) -> int:
    saved = {key: os.environ.get(key) for key in (env or {})}
    os.environ.update(env or {})
    try:
        fields = replay_receipt.run(
            argv, receipt=receipt, cwd_label=label, python_note=python, chdir=chdir
        )
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
    return int(fields["exit"])  # type: ignore[call-overload]


def _label(where: str) -> str:
    return (
        f"{where} of the k2m5-family tree staged by devtools.replay_k2m5_family from "
        f"{PACKET.relative_to(REPO)} (pinned 2c0b1b99), the pinned-only cov.tar.xz held "
        "to its digest"
    )


def fast(work: Path, out: Path, python: str) -> int:
    """``verify.sh`` in its fast mode, with the shim first on ``PATH``."""
    tree = work / "k2m5-family"
    path = f"{work / 'shim'}{os.pathsep}{os.environ.get('PATH', '')}"
    return _receipt(
        ["bash", "verification/verify.sh"],
        out / "verify_fast.log",
        chdir=tree,
        label=_label("the root"),
        python=f"{python} -I through the shim {work / 'shim/python3'} (script directory "
        "appended to sys.path)",
        env={"PATH": path},
    )


def patch_lines(text: str) -> tuple[list[str], list[str], list[str]]:
    """The files a unified diff touches, and its removed and added lines."""
    files = [line[4:].split("\t")[0] for line in text.splitlines() if line.startswith("+++ ")]
    body = [line for line in text.splitlines() if not line.startswith(("--- ", "+++ "))]
    removed = [line[1:] for line in body if line.startswith("-")]
    added = [line[1:] for line in body if line.startswith("+")]
    return files, removed, added


def build(work: Path) -> tuple[Path, Path]:
    """Build the unpatched and the print-all ``zmx2``; return both binaries."""
    plain = replay_evand_zmx2.build(CHECKER, work / "zmx2")
    text = (work / "k2m5-family" / PATCH).read_text(encoding="utf-8")
    files, removed, added = patch_lines(text)
    if files != ["b/verify2/src/bin/zmx2.rs"] or len(removed) != 1:
        raise SystemExit(f"{PATCH}: touches {files}, removes {len(removed)} lines")
    root = work / "zmx2/print-all"
    crate = root / "verify2"
    source = plain.parents[2]
    for relative in ("Cargo.toml", "Cargo.lock", "src/main.rs", "src/bin/zmx2.rs"):
        _write(crate / relative, (source / relative).read_bytes())
    binary = crate / "target/release/zmx2"
    receipt = root / "build.log"
    if binary.exists() and receipt.exists():
        return plain, binary
    applied = subprocess.run(
        ["patch", "-p1", "--forward", "-i", str(work / "k2m5-family" / PATCH)],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if applied.returncode != 0:
        raise SystemExit(f"patch failed: {applied.stdout}{applied.stderr}")
    status = _receipt(
        ["cargo", "build", "--release", "--bin", "zmx2"],
        receipt,
        chdir=crate,
        label=f"verify2/ of zmx2 {CHECKER} built from retained bytes with {PATCH} applied "
        f"({len(removed)} line removed, {len(added)} added; patched zmx2.rs "
        f"{sha256((crate / 'src/bin/zmx2.rs').read_bytes())})",
        python="not used by this command",
    )
    if status != 0:
        raise SystemExit(f"cargo build failed; see {receipt}")
    with receipt.open("a", encoding="utf-8") as handle:
        handle.write(f"# binary sha256: {sha256(binary.read_bytes())}\n")
    return plain, binary


def columns(text: str) -> list[int]:
    picked: set[int] = set()
    for part in text.split(","):
        low, _, high = part.partition("-")
        picked.update(range(int(low), int(high or low) + 1))
    if not picked <= set(range(COLUMNS)):
        raise SystemExit(f"columns outside 0-{COLUMNS - 1}: {text}")
    return sorted(picked)


def _finished(receipt: Path) -> bool:
    return receipt.exists() and "# finished " in receipt.read_text(encoding="utf-8")


def sweep(work: Path, out: Path, picked: Sequence[int]) -> int:
    """``cert0`` and the named columns of the first-order D4 sweep."""
    zmx2 = str((work / "zmx2" / CHECKER / "verify2/target/release/zmx2").resolve())
    tree, target = work / "k2m5-family", out / "zmx2"
    worst = 0
    jobs = [("cert0", [zmx2, "cert0", BOARD, "--d4"])]
    jobs += [
        (f"col{i:02d}", [zmx2, "cert", BOARD, *SWEEP, "--xlo", str(i), "--xhi", str(i),
                         "--log", str(target / f"col{i:02d}_roots.log")])
        for i in picked
    ]  # fmt: skip
    for name, argv in jobs:
        receipt = target / f"{name}.log"
        if _finished(receipt):
            continue
        status = _receipt(
            argv,
            receipt,
            chdir=tree,
            label=_label("the root"),
            python="not used by this command",
        )
        worst = max(worst, status)
    return worst


def root9632(work: Path, out: Path, python: str) -> int:
    """The patched dump, the qx2 run and ``check_9632.py`` on them."""
    patched = str((work / "zmx2/print-all/verify2/target/release/zmx2").resolve())
    tree, target = work / "k2m5-family", out / "r9632"
    target.mkdir(parents=True, exist_ok=True)
    status = 0
    dump = target / "dump.log"
    if not _finished(dump):
        status |= _receipt(
            [patched, "cert", BOARD, "--d4", "--first-order", "--threads", "1", "--depth", "40",
             "--node-cap", "20000000", "--uncert-cap", "100000000", "--xlo", "43", "--xhi",
             "43", "--ylo", "43", "--yhi", "43", "--bins", "0-0"],
            dump, chdir=tree, label=_label("the root") + "; zmx2 with the print-all patch",
            python="not used by this command", env={"ZMX2_PRINT_ALL": "1"},
        )  # fmt: skip
    zm = target / "zm.log"
    unc = target / "zm_unc.txt"
    if not _finished(zm):
        status |= _receipt(
            [python, "-I", "-c", LAUNCH, "qx2_zm.py", "c9632.txt", "--nproc", "1", *WINDOW,
             "--progress", "60", "--unc-out", str(unc.resolve())],
            zm, chdir=work / "qx2",
            label="qx2/: qx2_zm.py, zm_mixed.py, zeromargin.py and mixed_cover.py of evand/"
            "square-packing@659ee62 from the evand packets by SHA-256, and the source's "
            "verification/r9632/c9632.txt",
            python=f"{python} -I (script directory appended to sys.path)",
        )  # fmt: skip
    status |= _receipt(
        [python, "-I", "-c", LAUNCH, str(tree / "verification/r9632/check_9632.py"),
         str(dump.resolve()), str(zm.resolve()), str(unc.resolve())],
        target / "check_9632.log", chdir=target,
        label="receipts of this run: the dump and the qx2 run above, read by the source's "
        "check",
        python=f"{python} -I (script directory appended to sys.path)",
    )  # fmt: skip
    return status


def controls(work: Path, out: Path, python: str, only: Sequence[str]) -> int:
    zmx2 = str((work / "zmx2" / CHECKER / "verify2/target/release/zmx2").resolve())
    target = out / "controls"
    target.mkdir(parents=True, exist_ok=True)
    status = 0
    for name in only or CONTROLS:
        run = CONTROLS[name]
        receipt = target / f"{name}.log"
        if _finished(receipt):
            continue
        argv = [
            arg.format(zmx2=zmx2, python=python, out=str(target.resolve())) for arg in run.argv
        ]
        if argv[0] == python:
            argv[1:1] = ["-I", "-c", LAUNCH]
        chdir = work / "qx2" if run.cwd == "qx2" else work / "k2m5-family" / run.cwd
        status |= _receipt(argv, receipt, chdir=chdir, label=_label(run.cwd), python=python)
    if not only or "qx2-scale0999-r9632" in only:
        tree = work / "k2m5-family"
        status |= _receipt(
            [python, "-I", "-c", LAUNCH, str(tree / "verification/r9632/check_9632.py"),
             str((out / "r9632/dump.log").resolve()),
             str((target / "qx2-scale0999-r9632.log").resolve()),
             str((target / "q9632_scale0999_unc.txt").resolve())],
            target / "check_9632_scale0999.log", chdir=target,
            label="receipts of this run: the root-9632 dump and the scaled qx2 control",
            python=f"{python} -I (script directory appended to sys.path)",
        )  # fmt: skip
    return status


def tight(work: Path, out: Path, python: str, jobs: Sequence[str]) -> int:
    """``run_tt.py`` on named jobs of ``tight_tile/out``, as ``run_all2.sh`` runs them."""
    tree = work / "k2m5-family"
    target = out / "tight"
    status = 0
    for job in jobs:
        match = re.fullmatch(r"d([\d.]+)_s(-?1)_(line|strip)_(.+)", job)
        if match is None:
            raise SystemExit(f"not a job name: {job}")
        d0, sign, kind, rest = match.groups()
        args = rest.split("_")
        receipt = target / f"{job}.log"
        if _finished(receipt):
            continue
        status |= _receipt(
            [python, "-I", "-c", LAUNCH, "run_tt.py", "../" + BOARD, d0, sign, kind, *args],
            receipt, chdir=tree / "tight_tile", label=_label("tight_tile/"), python=python,
        )  # fmt: skip
    return status


# --- comparison --------------------------------------------------------------------------

DONE = re.compile(
    r"done in \S+ wall: roots (\d+) \(missing (\d+)\), boxes (\d+), certified (\d+), "
    r"empty (\d+), uncertified (\d+), max depth (\d+)"
)
DONE0 = re.compile(
    r"done0 in \S+: roots (\d+), boxes (\d+), certified (\d+), uncertified (\d+)"
)


def zmx2_summary(text: str) -> dict[str, object]:
    """The census, header settings and uncertified boxes of one ``zmx2`` run's output."""
    header = re.search(r"# zmx2 cert0? hash=(\S+) (.*)", text)
    done = DONE.search(text) or DONE0.search(text)
    uncert = sorted(re.findall(r"^UNCERT (\d+ pass \d+ box \S+)", text, re.MULTILINE))
    verdicts = [
        line for line in text.splitlines()
        if line.startswith(("VERIFIED", "NOT VERIFIED", "REGION CLEAN", "INCOMPLETE"))
    ]  # fmt: skip
    return {
        "hash": header.group(1) if header else None,
        "settings": header.group(2).split(" kappa")[0] if header else None,
        "census": list(map(int, done.groups())) if done else None,
        "uncert": uncert,
        "verdict": verdicts[-1] if verdicts else None,
    }


QX2_DONE = re.compile(r"done in \S+: boxes (\d+), max depth (\d+)")


def qx2_summary(text: str) -> dict[str, object]:
    done = QX2_DONE.search(text)
    leaves = re.search(r"leaves: (.*)", text)
    shas = sorted(re.findall(r"^sha256 (\S+)  (\S+)", text, re.MULTILINE))
    verdict = [line for line in text.splitlines() if "VERIFIED" in line]
    return {
        "census": list(map(int, done.groups())) if done else None,
        "leaves": leaves.group(1).split() if leaves else None,
        "sha256": shas,
        "verdict": verdict[-1] if verdict else None,
    }


#: Fields of a ``run_tt.py`` chart line that are not results: its seconds, and ``K``, which
#: the retained ``run_tt.py`` prints and the source's recorded outputs, written by an
#: earlier version of it, do not (the K they ran under is the job's default, 4).
TT_IGNORED = ("secs", "K")


def tt_lines(text: str) -> list[dict[str, object]]:
    rows = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("{", "CORNER {")):
            row = json.loads(stripped.removeprefix("CORNER "))
            for key in TT_IGNORED:
                row.pop(key, None)
            rows.append(row)
        elif stripped in {"ALL-OK", "NOT-OK"} or stripped.startswith("PARTIAL-"):
            rows.append({"final": stripped})
    return rows


def cropped(tree: Path, name: str) -> dict[str, object]:
    """Whether every segment of a cropped cover is a segment of the board, with its mass."""

    def parse(path: Path) -> tuple[list[str], list[tuple[str, ...]], list[str]]:
        rows = [line.split() for line in path.read_text(encoding="utf-8").splitlines()]
        rows = [row for row in rows if row and not row[0].startswith("#")]
        count = int(rows[5][0])
        return (
            [" ".join(r) for r in rows[:5]],
            [tuple(r) for r in rows[6 : 6 + count]],
            [" ".join(r) for r in rows[6 + count :]],
        )

    head, segments, tail = parse(tree / BOARD)
    c_head, c_segments, c_tail = parse(tree / name)
    board = set(segments)
    return {
        "file": name,
        "segments": len(c_segments),
        "all_in_board": all(segment in board for segment in c_segments),
        "distinct": len(set(c_segments)) == len(c_segments),
        "header_equal": c_head == head,
        "tail_equal": c_tail == tail,
        "mass": str(sum((Fraction(int(s[4])) for s in c_segments), Fraction(0))),
    }


def compare(work: Path, out: Path) -> dict[str, object]:
    tree = work / "k2m5-family"
    logs = tree / "verification/logs/zmx2_box11"
    result: dict[str, object] = {"zmx2": {}, "controls": {}, "tight": {}}
    for receipt in sorted((out / "zmx2").glob("c*.log")):
        if receipt.name.endswith("_roots.log") or not _finished(receipt):
            continue
        name = receipt.stem
        ours = zmx2_summary(receipt.read_text(encoding="utf-8"))
        theirs = zmx2_summary((logs / f"{'cert0.txt' if name == 'cert0' else name + '.out'}")
                              .read_text(encoding="utf-8"))  # fmt: skip
        result["zmx2"][name] = {  # type: ignore[index]
            "ours": {k: v for k, v in ours.items() if k != "uncert"},
            "uncert_ours": len(ours["uncert"]),  # type: ignore[arg-type]
            "uncert_theirs": len(theirs["uncert"]),  # type: ignore[arg-type]
            "equal": ours == theirs,
        }
    r9632 = out / "r9632"
    if _finished(r9632 / "dump.log"):
        ours = zmx2_summary((r9632 / "dump.log").read_text(encoding="utf-8"))
        theirs = zmx2_summary(
            (tree / "verification/r9632/dump.out").read_text(encoding="utf-8")
        )
        q_ours = qx2_summary((r9632 / "zm.log").read_text(encoding="utf-8")) if _finished(
            r9632 / "zm.log") else None  # fmt: skip
        q_theirs = qx2_summary((tree / "verification/r9632/zm.out").read_text(encoding="utf-8"))
        unc = r9632 / "zm_unc.txt"
        result["r9632"] = {
            "dump_census": ours["census"],
            "dump_uncert": len(ours["uncert"]),  # type: ignore[arg-type]
            "dump_equal": ours == theirs,
            "qx2_ours": q_ours,
            "qx2_equal": q_ours is not None and q_ours == q_theirs,
            "zm_unc_equal": unc.exists()
            and unc.read_bytes() == (tree / "verification/r9632/zm_unc.txt").read_bytes(),
            "check": _last_line(r9632 / "check_9632.log"),
        }
    for name, run in CONTROLS.items():
        receipt = out / "controls" / f"{name}.log"
        if not _finished(receipt):
            continue
        text = receipt.read_text(encoding="utf-8")
        entry: dict[str, object] = {"last": _last_line(receipt)}
        if run.record:
            record = (tree / run.record).read_text(encoding="utf-8")
            if "zmx2" in name:
                ours, theirs = zmx2_summary(text), zmx2_summary(record)
                entry |= {"census": ours["census"], "verdict": ours["verdict"],
                          "uncert": len(ours["uncert"]),  # type: ignore[arg-type]
                          "equal": ours == theirs}  # fmt: skip
            else:
                ours_q, theirs_q = qx2_summary(text), qx2_summary(record)
                entry |= {"summary": ours_q, "equal": ours_q == theirs_q}
        result["controls"][name] = entry  # type: ignore[index]
    check = out / "controls/check_9632_scale0999.log"
    if _finished(check):
        result["controls"]["check_9632_scale0999"] = _last_line(check)  # type: ignore[index]
    for receipt in sorted((out / "tight").glob("*.log")):
        if not _finished(receipt):
            continue
        record = tree / "tight_tile/out" / f"{receipt.stem}.out"
        ours_t = tt_lines(receipt.read_text(encoding="utf-8"))
        theirs_t = tt_lines(record.read_text(encoding="utf-8")) if record.exists() else None
        text = receipt.read_text(encoding="utf-8")
        result["tight"][receipt.stem] = {  # type: ignore[index]
            "rows": len(ours_t), "final": ours_t[-1] if ours_t else None,
            "equal": ours_t == theirs_t, "prints_K": '"K": "4"' in text,
        }  # fmt: skip
    result["cropped"] = [
        cropped(tree, "verification/r9632/c9632.txt"),
        cropped(tree, "verification/controls/c9632_scale0999.txt"),
    ]
    target = out / "compare.json"
    target.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return result


def _last_line(receipt: Path) -> str | None:
    lines = [
        line for line in receipt.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("# ")
    ]  # fmt: skip
    return lines[-1] if lines else None


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("stage", "fast", "build", "zmx2", "root9632", "controls", "tight", "compare"):
        sub = commands.add_parser(name)
        sub.add_argument("--work", type=Path, required=True)
        sub.add_argument("--python", default=sys.executable)
        if name == "stage":
            sub.add_argument("--cov", type=Path, required=True)
        if name not in {"stage", "build"}:
            sub.add_argument("--out", type=Path, required=True)
        if name == "zmx2":
            sub.add_argument("--columns", required=True, help="e.g. 0-13,15,43")
        if name == "controls":
            sub.add_argument("--only", nargs="+", choices=sorted(CONTROLS), default=())
        if name == "tight":
            sub.add_argument("--jobs", nargs="+", required=True)
    args = parser.parse_args(argv)
    work = args.work.resolve()
    if args.command == "stage":
        print(stage(work, args.cov.resolve(), args.python))
        return 0
    if args.command == "build":
        print(*build(work), sep="\n")
        return 0
    out = args.out.resolve()
    commands_run: dict[str, Callable[[], int]] = {
        "fast": lambda: fast(work, out, args.python),
        "zmx2": lambda: sweep(work, out, columns(args.columns)),
        "root9632": lambda: root9632(work, out, args.python),
        "controls": lambda: controls(work, out, args.python, args.only),
        "tight": lambda: tight(work, out, args.python, args.jobs),
    }
    if args.command in commands_run:
        return commands_run[args.command]()
    print(json.dumps(compare(work, out), indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
