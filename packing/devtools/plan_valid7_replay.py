"""Price, shard and check a full replay of either exact checker of Valid7.

T-064's lower half rests on Valid7: every closed unit square in ``[0, 7]^2`` has mass at
least 1 under Evan Daniel's k = 7 measure ``L4_k02_box7.txt``. Two separately written
exact checkers decide it, and stage 4 of the result import needs one of them replayed in
full here (``campaign/result-import.md``):

- ``qx2``, Daniel's ``qx2_zm.py`` run V3 over the D4 region, 9,800 roots, whose record
  ``runV3_6294052a_leaves.jsonl.gz`` the October 1 evand packet retains;
- ``wand125``, Hosono's independent checker over the whole pose space, 156,800 roots,
  whose two records the release ``records-v1`` holds and its packet pins by digest.

Each record carries every root's CPU time, so the replay can be priced and split before
anything runs. This tool decides nothing about a leaf; the checkers do.

``stage --checker C --work DIR [--guard-d1]``
    Copies the retained checker and cover into ``DIR``, refusing any file whose SHA-256
    is not the one the run's record names. ``--guard-d1`` (``wand125`` only) changes the
    one line of ``tier_b2.nonneg_open`` that accepts a polynomial vanishing at its sample
    point (finding D-1 of the 2 October review) into a refusal, so a replay with it
    differs from the published run exactly where that case arises.
``plan --checker C --shards N [--records DIR] [--speed S] [--cores K] [--json OUT]``
    Prices the replay and splits its roots into at most ``N`` shards of nearly equal
    recorded CPU. The unit is a centre cell: the roots of one 1/10 by 1/10 centre square
    over every angle bin. Cells are taken in x-major order and cut into runs of
    consecutive cells, so a shard is at most three rectangles, each one checker run with
    its own region flags and record. Each checker resumes from its own record, so an
    interrupted shard is finished by running the same command again. ``--speed`` is this
    host's CPU seconds per recorded CPU second, measured with ``region``. Hosono's
    ``run_all.py`` is launched under the ``fork`` start method (``FORK_LAUNCH``), so that
    the receipt counts its workers' CPU; its record's per-root time is wall time in the
    worker.
    For ``wand125`` the price is that of the published code, V2. The run's first 31,825
    roots ran under V1, whose earlier hand-off to Tier B cost more; each is priced at its
    mirror image under ``x -> 7 - x``, ``u -> -u``, which ran under V2.
``region --checker C --x LO HI --y LO HI [--records DIR]``
    The recorded CPU and root count of one region, to calibrate ``--speed`` against a
    receipt of the same region run here.
``compare --checker C SHARD... [--records DIR] [--partial] [--json OUT]``
    Checks a sharded replay against the published record, as the source's
    ``verify.sh --full`` does for an unsharded ``qx2_zm.py`` run: each shard names the
    retained checker and cover and the published settings plus region flags; no root is
    recorded twice; together they hold exactly the published roots; none has an
    uncertified box or a counterexample; and each root's leaf list equals the published
    one. For ``wand125`` that equality is asked of the V2 roots only, since V1 split
    differently. It also counts the shards' leaves and sums their per-root times
    (``root_hours``): CPU for ``qx2``, wall time in the worker for ``wand125``.

From ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.plan_valid7_replay \\
        plan --checker qx2 --shards 4 --speed 1.0
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import shutil
from collections import Counter, defaultdict
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import cast

from strif import atomic_write_text

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
K2M3 = WEB / "evand-square-packing-2026-10-01/source/s12/certificates/k2m3"
COVER = K2M3 / "L4_k02_box7.txt"
COVER_SHA256 = "c0a6750997897c21ffc693df6df97f89a248dd9eb588a2fe2b83bf359793694b"
QX2_RECORD = K2M3 / "qx2_zm/runV3_6294052a_leaves.jsonl.gz"
QX2_CHECKER = K2M3 / "qx2_zm/checker"
#: The files run V3's header names, by SHA-256 (``k2m3/SHA256SUMS``).
QX2_FILES = {
    "qx2_zm.py": "6294052a37ce66c5d84b55afd606e3a52f463e22b876bf44b5aa903aefb7e737",
    "zm_mixed.py": "1fd203469bb43a55ca7ce376b9717437e0970eead31941ec7fa100ab24d5ba95",
    "zeromargin.py": "640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab",
    "mixed_cover.py": "bb89de15ecf5821dd7e1a36ebab8a50d792a406b7fb0f5cb38059f99ef74aae5",
}
#: Run V3's settings, as its header's argv gives them; a shard adds only region flags.
QX2_SETTINGS = (
    "--depth", "18", "--exact-umax", "1/2", "--exact-from", "3", "--dump-leaves",
)  # fmt: skip
QX2_REGION_FLAGS = ("--cx-lo", "--cx-hi", "--cy-lo", "--cy-hi")
WAND125_TREE = WEB / "wand125-valid7-independent-check-2026-10-02/valid7-independent-check"
#: The V2 code, as ``full_b.jsonl``'s header names it; ``check_record.py`` is not named.
WAND125_FILES = {
    "run_all.py": "899144f999e69cb0b1e95063e6e9c208cca6eedca51d11c139cfd84d229ca476",
    "tier_a.py": "bb23e935a2e30901d1f9bc6e455ff60c6045826dfb8edf1807c065fdf1a4c9b1",
    "tier_b.py": "ca72a14909e3d242ad2006a782a795fb9cb5a27d81df1422f28aa882049505bb",
    "tier_b2.py": "ebd2a1d0a47a84815008deea35e684231e050f941445d9f6f6c400a7556d9941",
    "solver.py": "aa462c15f72309912da3ef231d443ea6690ecccf4cbc9f94a5bd7797681b674c",
    "rf.py": "c527689cec0072e3f1263b2cb5654b1df196b9295cd7e70a49c151276146e4a5",
    "cover.py": "bdaee4f0390d76d0286251660a4b3aba802f28935c64f9290eed8c52a50bf3e6",
    "check_record.py": "",
}
WAND125_RECORDS = ("full.jsonl.gz", "full_b.jsonl.gz")
#: ``full.jsonl``'s first 31,825 roots ran under V1 (``versions/VERSIONS.md``).
WAND125_V1_ROOTS = 31_825
D1_LINE = "    return p(s) >= 0\n"
D1_GUARD = (
    "    v = p(s)\n"
    "    if v == 0:  # D-1 guard: the sample is a root, so the sign test decides nothing\n"
    "        raise ArithmeticError('nonneg_open: the sample point is a root')\n"
    "    return v > 0\n"
)
#: ``run_all.py``, unmodified, under the ``fork`` start method. CPython 3.14 defaults to
#: ``forkserver`` on Linux, whose pool workers are no descendants the receipt waits for,
#: so their CPU would be missing from it; the start method changes no decision.
FORK_LAUNCH = (
    "import multiprocessing, runpy, sys; multiprocessing.set_start_method('fork'); "
    "sys.argv = sys.argv[1:]; sys.path.insert(0, 'src'); "
    "runpy.run_path(sys.argv[0], run_name='__main__')"
)
PITCH = Fraction(1, 10)
SIDE = Fraction(7)

Box = tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction]
Cell = tuple[Fraction, Fraction]
Rect = tuple[Fraction, Fraction, Fraction, Fraction]


@dataclass(frozen=True)
class Checker:
    """What differs between the two checkers: their domain and their command lines."""

    name: str
    x_max: Fraction
    roots: int

    def command(self, rect: Rect, record: str, cores: int, python: str) -> list[str]:
        """The checker's own command for one rectangle of centres, run from its work dir."""
        x0, x1, y0, y1 = (str(v) for v in rect)
        if self.name == "qx2":
            return [
                python, "checker/qx2_zm.py", "L4_k02_box7.txt",
                "--depth", "18", "--nproc", str(cores), "--exact-umax", "1/2",
                "--exact-from", "3", "--progress", "200",
                "--cx-lo", x0, "--cx-hi", x1, "--cy-lo", y0, "--cy-hi", y1,
                "--resume", record, "--dump-leaves",
            ]  # fmt: skip
        return [
            python, "-c", FORK_LAUNCH, "src/run_all.py", "cover/L4_k02_box7.txt",
            "--centers", x0, x1, y0, y1, "--nproc", str(cores),
            "--record", record, "--resume",
        ]  # fmt: skip


CHECKERS = {
    "qx2": Checker("qx2", SIDE / 2, 9_800),
    "wand125": Checker("wand125", SIDE, 156_800),
}


@dataclass
class Root:
    """One root of a record: its box, CPU, leaves, and whether it may be compared."""

    box: Box
    cpu: float
    leaves: list[str]
    bad: int
    comparable: bool = True


@dataclass
class Record:
    """A run record, read into roots in file order."""

    header: dict[str, object] = field(default_factory=dict[str, object])
    roots: list[Root] = field(default_factory=list[Root])


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _lines(path: Path) -> Iterator[dict[str, object]]:
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            text = handle.read()
    else:
        text = path.read_text(encoding="utf-8")
    for raw in text.splitlines():
        if raw.strip():
            yield cast("dict[str, object]", json.loads(raw))


def _box(values: object) -> Box:
    return cast("Box", tuple(Fraction(str(v)) for v in cast("list[object]", values)))


def _leaf_key(leaf: object) -> str:
    box, kind = cast("list[object]", leaf)[:2]
    return f"{[str(v) for v in cast('list[object]', box)]} {kind}"


def read_record(path: Path, checker: str) -> Record:
    """Read a ``qx2_zm.py --resume`` record or a ``run_all.py`` record."""
    record = Record()
    for entry in _lines(path):
        if entry.get("kind") == "header":
            record.header = entry
            continue
        if "header" in entry:
            record.header = cast("dict[str, object]", entry["header"])
            continue
        leaves = sorted(_leaf_key(leaf) for leaf in cast("list[object]", entry["leaves"]))
        if checker == "qx2":
            stats = cast("dict[str, float]", entry["st"])
            cpu = float(stats["cpu"])
            bad = len(cast("list[object]", entry["unc"])) + int(stats.get("UNCERT", 0))
        else:
            cpu = float(cast("float", entry["cpu"]))
            bad = len(cast("list[object]", entry["uncert"]))
            bad += len(cast("list[object]", entry["cex"]))
        record.roots.append(Root(_box(entry["root"]), cpu, leaves, bad))
    return record


def published(checker: str, records: Path | None) -> list[Root]:
    """The published roots, with each V1 root of Hosono's checker marked as not comparable."""
    if checker == "qx2":
        return read_record(QX2_RECORD, "qx2").roots
    if records is None:
        msg = "Hosono's records are not retained: pass --records DIR"
        raise SystemExit(msg)
    roots: list[Root] = []
    for name in WAND125_RECORDS:
        part = read_record(records / name, "wand125").roots
        if name == WAND125_RECORDS[0]:
            for root in part[:WAND125_V1_ROOTS]:
                root.comparable = False
        roots += part
    return roots


def mirror(box: Box) -> Box:
    """The image of a root under ``x -> 7 - x``, which maps ``u`` to ``-u``."""
    x0, x1, y0, y1, u0, u1 = box
    return (SIDE - x1, SIDE - x0, y0, y1, -u1, -u0)


def priced(checker: str, roots: list[Root]) -> dict[Box, float]:
    """Each root's CPU under the published code: a V1 root of Hosono's at its V2 mirror."""
    cpu = {root.box: root.cpu for root in roots}
    if checker == "qx2":
        return cpu
    v2 = {root.box: root.cpu for root in roots if root.comparable}
    return {box: v2.get(box, v2.get(mirror(box), cost)) for box, cost in cpu.items()}


def cells(checker: Checker, cost: dict[Box, float]) -> list[tuple[Cell, float]]:
    """Every centre cell of the checker's domain in x-major order, with its cost."""
    total: defaultdict[Cell, float] = defaultdict(float)
    for box, seconds in cost.items():
        total[box[0], box[2]] += seconds
    count = int(checker.x_max / PITCH)
    return [
        ((PITCH * i, PITCH * j), total[PITCH * i, PITCH * j])
        for i in range(count)
        for j in range(count)
    ]


def partition(costs: Sequence[float], shards: int) -> list[tuple[int, int]]:
    """Cut ``costs`` into at most ``shards`` consecutive runs, minimising the largest sum."""
    lo, hi = max(costs, default=0.0), sum(costs)
    for _ in range(100):
        mid = (lo + hi) / 2
        if len(_greedy(costs, mid)) <= shards:
            hi = mid
        else:
            lo = mid
    return _greedy(costs, hi)


def _greedy(costs: Sequence[float], bound: float) -> list[tuple[int, int]]:
    runs: list[tuple[int, int]] = []
    start, acc = 0, 0.0
    for i, cost in enumerate(costs):
        if acc + cost > bound and i > start:
            runs.append((start, i))
            start, acc = i, 0.0
        acc += cost
    runs.append((start, len(costs)))
    return runs


def rectangles(start: int, stop: int, side: int) -> list[Rect]:
    """The cells ``start .. stop - 1`` of an x-major ``side x side`` grid, as rectangles."""
    out: list[Rect] = []
    i = start
    while i < stop:
        col, row = divmod(i, side)
        if row == 0 and stop - i >= side:
            cols = (stop - i) // side
            out.append((PITCH * col, PITCH * (col + cols), Fraction(0), PITCH * side))
            i += cols * side
            continue
        end = min(stop - i, side - row)
        out.append((PITCH * col, PITCH * (col + 1), PITCH * row, PITCH * (row + end)))
        i += end
    return out


def plan(
    checker_name: str,
    shards: int,
    records: Path | None,
    *,
    speed: float = 1.0,
    cores: int = 4,
    python: str = "python3",
) -> dict[str, object]:
    """The price of the replay and its shards, with each shard's commands."""
    checker = CHECKERS[checker_name]
    roots = published(checker_name, records)
    cost = priced(checker_name, roots)
    grid = cells(checker, cost)
    side = int(checker.x_max / PITCH)
    largest_in: defaultdict[Cell, float] = defaultdict(float)
    for box, seconds in cost.items():
        largest_in[box[0], box[2]] = max(largest_in[box[0], box[2]], seconds)
    out: list[dict[str, object]] = []
    for k, (start, stop) in enumerate(partition([c for _, c in grid], shards), 1):
        rects = rectangles(start, stop, side)
        recorded = sum(c for _, c in grid[start:stop])
        largest = max((largest_in[g] for g, _ in grid[start:stop]), default=0.0)
        runs: list[dict[str, object]] = []
        for j, rect in enumerate(rects, 1):
            name = f"{checker_name}_shard{k:02d}_{j}"
            runs.append({
                "rectangle": [str(v) for v in rect],
                "record": f"runs/{name}.jsonl",
                "receipt": f"receipts/{name}.log",
                "command": checker.command(rect, f"runs/{name}.jsonl", cores, python),
            })  # fmt: skip
        out.append({
            "shard": k,
            "cells": stop - start,
            "priced_cpu_hours": round(recorded / 3600, 2),
            "largest_root_seconds": round(largest, 1),
            "wall_hours_estimate": round(max(recorded / cores, largest) * speed / 3600, 2),
            "runs": runs,
        })  # fmt: skip
    recorded_total = sum(root.cpu for root in roots)
    result: dict[str, object] = {
        "kind": "valid7-replay-plan/v1",
        "checker": checker_name,
        "roots": len(roots),
        "recorded_cpu_hours": round(recorded_total / 3600, 2),
        "priced_cpu_hours": round(sum(cost.values()) / 3600, 2),
        "speed": speed,
        "cores_per_shard": cores,
        "host_cpu_hours_estimate": round(sum(cost.values()) * speed / 3600, 2),
        "shards": out,
    }
    if checker_name == "wand125":
        result["mirror_check"] = mirror_check(roots)
    return result


def mirror_check(roots: list[Root]) -> dict[str, float]:
    """How well mirror pricing works: V2 roots left of x = 7/2 against their V2 mirrors.

    ``spread`` is the sum of each pair's absolute difference over the left total, so it
    says how far one root's price can be from its own cost even when the totals agree.
    """
    v2 = {root.box: root.cpu for root in roots if root.comparable}
    pairs = [
        (cpu, v2[mirror(box)])
        for box, cpu in v2.items()
        if box[1] <= SIDE / 2 and mirror(box) in v2
    ]
    left = sum(a for a, _ in pairs)
    return {
        "pairs": len(pairs),
        "left_cpu_hours": round(left / 3600, 2),
        "mirror_cpu_hours": round(sum(b for _, b in pairs) / 3600, 2),
        "spread": round(sum(abs(a - b) for a, b in pairs) / left, 3) if left else 0.0,
    }


def region(
    checker_name: str,
    x: tuple[Fraction, Fraction],
    y: tuple[Fraction, Fraction],
    records: Path | None,
) -> dict[str, object]:
    """The recorded and priced CPU of the roots whose centre box lies in one rectangle."""
    roots = published(checker_name, records)
    cost = priced(checker_name, roots)
    inside = [
        root for root in roots
        if x[0] <= root.box[0] and root.box[1] <= x[1]
        and y[0] <= root.box[2] and root.box[3] <= y[1]
    ]  # fmt: skip
    return {
        "checker": checker_name,
        "region": [str(v) for v in (*x, *y)],
        "roots": len(inside),
        "recorded_cpu_seconds": round(sum(root.cpu for root in inside), 1),
        "priced_cpu_seconds": round(sum(cost[root.box] for root in inside), 1),
        "v2_roots": sum(root.comparable for root in inside),
    }


def _argv_problems(name: str, header: dict[str, object], checker: str) -> list[str]:
    """The record's argv is the published settings, plus region and process flags only."""
    argv = [str(v) for v in cast("list[object]", header.get("argv", []))]
    if checker == "qx2":
        allowed = {"--nproc", "--progress", "--resume", *QX2_REGION_FLAGS, *QX2_SETTINGS}
        pairs = [argv[i : i + 2] for i in range(len(argv) - 1)]
        problems = [
            f"{name}: argv does not set {flag} {value}"
            for flag, value in zip(QX2_SETTINGS[:-1:2], QX2_SETTINGS[1:-1:2], strict=True)
            if [flag, value] not in pairs
        ]
        if QX2_SETTINGS[-1] not in argv:
            problems.append(f"{name}: argv lacks {QX2_SETTINGS[-1]}")
    else:
        allowed = {"--centers", "--nproc", "--record", "--resume"}
        problems = [] if argv[:1] == ["src/run_all.py"] else [f"{name}: not run_all.py"]
    problems += [
        f"{name}: argv changes a setting with {flag}"
        for flag in argv
        if flag.startswith("--") and flag not in allowed
    ]
    return problems


def _header_problems(name: str, record: Record, checker: str, *, guarded: bool) -> list[str]:
    if checker == "qx2":
        shas = cast("dict[str, str]", record.header.get("sha256", {}))
        want = {**QX2_FILES, "input": COVER_SHA256}
        return [] if shas == want else [f"{name}: header digests are not the retained files"]
    named = cast("dict[str, str]", record.header.get("sha256", {}))
    problems: list[str] = []
    for key, digest in named.items():
        base = Path(key).name
        if base == "L4_k02_box7.txt":
            ok = digest == COVER_SHA256
        elif guarded and base == "tier_b2.py":
            ok = digest == hashlib.sha256(guard_d1(WAND125_TREE / "src/tier_b2.py")).hexdigest()
        else:
            ok = WAND125_FILES.get(base) == digest
        if not ok:
            problems.append(f"{name}: {base} is not the retained V2 file")
    return problems or ([] if named else [f"{name}: the header names no files"])


def compare(
    checker: str,
    shards: Sequence[Path],
    records: Path | None,
    *,
    guarded: bool = False,
    partial: bool = False,
) -> dict[str, object]:
    """Check a sharded replay against the published record; ``ok`` and every problem.

    ``partial`` asks only that the shards' roots be published ones, not all of them: a
    calibration over one region, not a replay.
    """
    reference = {root.box: root for root in published(checker, records)}
    problems: list[str] = []
    seen: Counter[Box] = Counter()
    differ = matched = leaves = 0
    seconds = 0.0
    for path in shards:
        record = read_record(path, checker)
        problems += _header_problems(path.name, record, checker, guarded=guarded)
        problems += _argv_problems(path.name, record.header, checker)
        for root in record.roots:
            seen[root.box] += 1
            leaves += len(root.leaves)
            seconds += root.cpu
            if root.bad:
                problems.append(
                    f"{path.name}: root {[str(v) for v in root.box]} has {root.bad}"
                )
            ref = reference.get(root.box)
            if ref is None or not ref.comparable:
                continue
            if root.leaves == ref.leaves:
                matched += 1
            else:
                differ += 1
    if repeated := sum(1 for n in seen.values() if n > 1):
        problems.append(f"{repeated} roots recorded more than once")
    if not partial and (missing := len(set(reference) - set(seen))):
        problems.append(f"{missing} published roots are missing")
    if extra := len(set(seen) - set(reference)):
        problems.append(f"{extra} roots are not published roots")
    if differ:
        problems.append(f"{differ} roots have leaves other than the published ones")
    return {
        "kind": "valid7-sharded-replay-compare/v1",
        "checker": checker,
        "ok": not problems,
        "problems": problems,
        "shards": [p.name for p in shards],
        "roots": len(seen),
        "roots_matching_published_leaves": matched,
        "roots_not_compared": sum(not r.comparable for r in reference.values()),
        "partial": partial,
        "leaves": leaves,
        "root_hours": round(seconds / 3600, 2),
    }


def guard_d1(path: Path) -> bytes:
    """``tier_b2.py`` with D-1's one accepting line made a refusal."""
    text = path.read_text(encoding="utf-8")
    if text.count(D1_LINE) != 1:
        msg = f"{path}: the line D-1 names is not there exactly once"
        raise SystemExit(msg)
    return text.replace(D1_LINE, D1_GUARD).encode()


def stage(checker: str, work: Path, *, guard: bool = False) -> dict[str, str]:
    """Copy the retained checker and cover into ``work``; return each file's SHA-256."""
    if _sha256(COVER) != COVER_SHA256:
        msg = "the retained cover is not c0a67509"
        raise SystemExit(msg)
    (work / "runs").mkdir(parents=True, exist_ok=True)
    (work / "receipts").mkdir(exist_ok=True)
    if checker == "qx2":
        files = {QX2_CHECKER / n: work / "checker" / n for n in QX2_FILES}
        cover = work / "L4_k02_box7.txt"
        want = dict(QX2_FILES)
    else:
        files = {WAND125_TREE / "src" / n: work / "src" / n for n in WAND125_FILES}
        cover = work / "cover/L4_k02_box7.txt"
        want = {n: d for n, d in WAND125_FILES.items() if d}
    staged: dict[str, str] = {}
    for source, target in files.items():
        digest = _sha256(source)
        if want.get(source.name, digest) != digest:
            msg = f"{source} is {digest[:16]}, the record names {want[source.name][:16]}"
            raise SystemExit(msg)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if guard and source.name == "tier_b2.py":
            target.write_bytes(guard_d1(source))
        staged[str(target.relative_to(work))] = _sha256(target)
    cover.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(COVER, cover)
    staged[str(cover.relative_to(work))] = COVER_SHA256
    return staged


def _fraction_pair(values: Sequence[str]) -> tuple[Fraction, Fraction]:
    return Fraction(values[0]), Fraction(values[1])


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    sub = parser.add_subparsers(dest="action", required=True)
    for action in ("stage", "plan", "region", "compare"):
        p = sub.add_parser(action)
        p.add_argument("--checker", choices=sorted(CHECKERS), required=True)
        p.add_argument("--records", type=Path, help="directory of Hosono's two .jsonl.gz")
        p.add_argument("--json", type=Path, help="also write the result here")
        p.add_argument("--guard-d1", action="store_true", help="wand125: refuse D-1's case")
        if action == "stage":
            p.add_argument("--work", type=Path, required=True)
        if action == "plan":
            p.add_argument("--shards", type=int, required=True)
            p.add_argument("--speed", type=float, default=1.0)
            p.add_argument("--cores", type=int, default=4)
            p.add_argument("--python", default="python3", help="interpreter in the commands")
        if action == "region":
            p.add_argument("--x", nargs=2, required=True)
            p.add_argument("--y", nargs=2, required=True)
        if action == "compare":
            p.add_argument("shards", nargs="+", type=Path)
            p.add_argument("--partial", action="store_true", help="one region, not the grid")
    args = parser.parse_args(argv)
    if args.guard_d1 and args.checker != "wand125":
        parser.error("--guard-d1 applies to Hosono's checker only")
    result: dict[str, object]
    if args.action == "stage":
        result = {"staged": stage(args.checker, args.work, guard=args.guard_d1)}
    elif args.action == "plan":
        result = plan(
            args.checker,
            args.shards,
            args.records,
            speed=args.speed,
            cores=args.cores,
            python=args.python,
        )
    elif args.action == "region":
        x, y = _fraction_pair(args.x), _fraction_pair(args.y)
        result = region(args.checker, x, y, args.records)
    else:
        result = compare(
            args.checker,
            args.shards,
            args.records,
            guarded=args.guard_d1,
            partial=args.partial,
        )
    text = json.dumps(result, indent=2) + "\n"
    if args.json:
        atomic_write_text(args.json, text)
    print(text, end="")
    return 0 if result.get("ok", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
