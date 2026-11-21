#!/usr/bin/env python3
"""Replay Joost de Winter's integer rectangle-measure certificates direction by direction.

The certificates of jlevy/squares#1039, #1041 and #1042 (the
`de-winter-lower-bounds-2026-11-19` packet) each prove that every admissible unit square
captures mass at least one of a rectangle measure, one angular interval at a time, with
a compiled integer kernel of the author's (`proof/bmcheck.cpp`, `octagon.cpp` or
`gram.cpp`) and a Python wrapper (`proof/bm.py`, `proof/check.py`) that writes the
kernel's inputs. The source's own `proof/replay.py` reruns them and prints only a count.
This replays the same archived directions with the same programs, read from the pinned
source, and keeps what the source's driver discards: for every direction the kernel's
verdict, node and leaf totals and least certified bound, compared with the archived
receipt, and the CPU it took. It is a replay with the producer's code
(`same-implementation`), not a second implementation.

Before importing or compiling any producer program, the supplied source files must
match the retained packet's bytes. Only those validated bytes are copied into a private
working directory and used by the replay; caller-supplied bytecode is never loaded.

A certificate folder holds `manifest.json` and, per angular level, a gzip measure and a
gzip receipt file whose digests the manifest names. For each level this

- checks both digests, the kernel source's digest against `native_sha256`, the
  wrapper's against `wrapper_sha256`, and the integer rows' digest and count against
  `rects_sha256` and `rectangles`, all as the manifest states them;
- recomputes each receipt's kernel header with the source's `check.header` and requires
  it to equal the archived one; and
- runs the kernel at every archived direction with the archived header and the source
  driver's node cap, 2,100,000 (`--cap`), and records `PASS` with a least bound of at
  least `M` = 2^48 as verified, and agreement with the archived nodes, leaves and least
  bound as `matches_archive`.

A folder of #1039's `rectangles/evidence/` holds instead `measure.json.gz`,
`coverage.jsonl.gz` and `integer_run.json`. There the measure's, the rows' and the
kernel's digests are `integer_run.json`'s, the receipts are the coverage rows whose
method is `integer`, and since those archive no header it is computed as the zip's
`rectangles/code/bm.py` computes it (`set_header`): the square kernel's header of
`check.header`, except that a set whose `center_domain` is `contained_core` clears the
core's own half-width $B(C+H)/(2E)$ instead of the parent's.

`--mutant quarter` divides every row's density and mass by 4, the source driver's own
control, and `--mutant 99/100` scales them by 99/100 (rounded down), the record's
near-threshold control; a mutant run is refused at a direction when the kernel answers
`UNDECIDED`, and a refusal is on coverage when the kernel reports an unresolved box
rather than reaching the node cap. `--first-per-level` runs only each level's first
receipt, as the source driver runs its control. The certified premises other than the
kernel's (the angular coverage, the transfer, the comparisons) are the source's
`verify.py`, which this does not repeat.

Usage, from `packing/`, with the pinned source's `proof/` directory as `--source`:
    uv run --frozen --all-extras --group dev python -m devtools.replay_rectangle_receipts \\
        --source SOURCE/proof --out RECEIPT.jsonl FOLDER... [--workers 2] [--mutant M]
"""

from __future__ import annotations

import argparse
import concurrent.futures
import gzip
import hashlib
import importlib.util
import json
import resource
import subprocess
import sys
import tempfile
import time
from collections.abc import Mapping, Sequence
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any

KERNELS = {"square": "bmcheck.cpp", "octagon": "octagon.cpp", "octagon-gram": "gram.cpp"}
CAP = 2_100_000
M = 2**48
MUTANTS = {"none": Fraction(1), "quarter": Fraction(1, 4), "99/100": Fraction(99, 100)}
FORMAT = "rectangle-receipt-replay/v1"
PACKING = Path(__file__).resolve().parents[1]
RETAINED_SOURCE = (
    PACKING
    / "resources/web/de-winter-lower-bounds-2026-11-19/source/lower_bounds_2026_11_19/proof"
)
SOURCE_FILES = ("bm.py", "check.py", *KERNELS.values())


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stage_source(source: Path, workdir: Path) -> Path:
    """Authenticate the external execution inputs and retain exactly the checked bytes."""
    checked: dict[str, bytes] = {}
    for name in SOURCE_FILES:
        raw = (source / name).read_bytes()
        if raw != (RETAINED_SOURCE / name).read_bytes():
            raise SystemExit(f"{source / name}: differs from the retained source packet")
        checked[name] = raw
    staged = workdir / "source"
    staged.mkdir()
    for name, raw in checked.items():
        (staged / name).write_bytes(raw)
    return staged


def load_source(source: Path) -> tuple[ModuleType, ModuleType]:
    """The source's `bm` and `check` modules, loaded from the pinned copy by path."""
    sys.dont_write_bytecode = True
    modules: dict[str, ModuleType] = {}
    for name in ("bm", "check"):
        spec = importlib.util.spec_from_file_location(name, source / f"{name}.py")
        if spec is None or spec.loader is None:
            raise SystemExit(f"cannot load {source / name}.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        modules[name] = module
    return modules["bm"], modules["check"]


def compile_kernel(source: Path, kernel: str, workdir: Path) -> Path:
    cpp = source / KERNELS[kernel]
    binary = workdir / f"kernel-{kernel}"
    if not binary.exists():
        subprocess.run(["c++", "-O3", "-std=c++17", str(cpp), "-o", str(binary)], check=True)
    return binary


def scaled(rows: Sequence[Sequence[int]], factor: Fraction) -> list[tuple[int, ...]]:
    """Every row with its density and mass (the last two fields) scaled, rounded down."""
    out = []
    for row in rows:
        *head, density, mass = row
        out.append(
            (
                *head,
                density * factor.numerator // factor.denominator,
                mass * factor.numerator // factor.denominator,
            )
        )
    return out


def run_direction(job: tuple[Path, Path, Mapping[str, Any], Path, int, str]) -> dict[str, Any]:
    """One kernel run: binary, rows file, receipt, work directory, node cap and tag."""
    binary, rows_file, receipt, workdir, cap, tag = job
    header = workdir / f"h-{tag}-{receipt['r']}"
    header.write_text(" ".join(map(str, receipt["header"])) + "\n")
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    start = time.monotonic()
    done = subprocess.run(
        [str(binary), str(rows_file), str(header), str(cap)],
        capture_output=True,
        text=True,
        check=False,
    )
    wall = time.monotonic() - start
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    out = done.stdout.split()
    verdict = out[0] if out else f"ERROR_{done.returncode}"
    fields = [int(x) for x in out[1:6]] if len(out) >= 6 else [0] * 5
    nodes, leaves, clips, depth, least = fields
    unresolved = next(
        (line for line in done.stderr.splitlines() if line.startswith("unresolved")), None
    )
    return {
        "r": receipt["r"],
        "verdict": verdict,
        "exit": done.returncode,
        "nodes": nodes,
        "leaves": leaves,
        "clips": clips,
        "depth": depth,
        "lower_units": least,
        "unresolved": unresolved,
        "cpu_seconds_approx": round(
            (after.ru_utime - before.ru_utime) + (after.ru_stime - before.ru_stime), 3
        ),
        "wall_seconds": round(wall, 3),
    }


def set_header(measure: Mapping[str, Any], r: int, domain: str | None) -> list[int]:
    """The kernel header the zip's `rectangles/code/bm.py` writes for direction `r`."""
    g = 2**30
    step = Fraction(measure["proof_net"]["step"])
    side, core = Fraction(measure["L"]), Fraction(measure["B"])
    t = r * step
    a, b = t.numerator, t.denominator
    c, s, e = b * b - a * a, 2 * a * b, a * a + b * b
    left = max(Fraction(0), t - step / 2)
    v = (1 + 2 * left - left**2) / (2 * (1 + left**2))
    if domain == "contained_core":
        v = core * Fraction(c + s, 2 * e)
    lo = (g * side / 2).__floor__()
    hi = (g * (side - v)).__ceil__()
    cut = (e * g * core / 2).__floor__()
    return [c, s, e, cut // e, cut % e, lo, lo, hi, hi]


def load_set(folder: Path) -> dict[str, Any]:
    """A #1039 evidence set as a one-level manifest, its receipts the integer rows."""
    run = json.loads((folder / "integer_run.json").read_text())
    raw = (folder / "measure.json.gz").read_bytes()
    if sha256(raw) != run["measure_sha256"]:
        raise SystemExit(f"{folder}: measure digest differs from integer_run.json")
    measure = json.loads(gzip.decompress(raw))
    receipts = []
    for line in gzip.decompress((folder / "coverage.jsonl.gz").read_bytes()).splitlines():
        row = json.loads(line)
        if row.get("method") == "integer":
            receipt = dict(row["evidence"])
            receipt["header"] = set_header(measure, receipt["r"], run.get("center_domain"))
            receipts.append(receipt)
    return {
        "n": measure["n"],
        "side": str(measure["L"]),
        "kernel": "square",
        "native_sha256": run["source_sha256"],
        "levels": [
            {
                "K": measure["proof_net"]["last"],
                "measure": measure,
                "receipts": receipts,
                "rects_sha256": run["rects_sha256"],
                "rectangles": run["rectangles"],
            }
        ],
    }


def replay_folder(
    folder: Path,
    source: Path,
    check: ModuleType,
    bm: ModuleType,
    workdir: Path,
    *,
    mutant: str,
    first_per_level: bool,
    workers: int,
    cap: int,
) -> list[dict[str, Any]]:
    evidence_set = not (folder / "manifest.json").exists()
    manifest = (
        load_set(folder) if evidence_set else json.loads((folder / "manifest.json").read_text())
    )
    kernel = manifest.get("kernel") or "square"
    kernel_digest = sha256((source / KERNELS[kernel]).read_bytes())
    wrapper_digest = sha256((source / "bm.py").read_bytes())
    if kernel_digest != manifest["native_sha256"] or (
        not evidence_set and wrapper_digest != manifest["wrapper_sha256"]
    ):
        raise SystemExit(f"{folder}: kernel or wrapper digest differs from the manifest")
    binary = compile_kernel(source, kernel, workdir)
    rows_out: list[dict[str, Any]] = []
    for level in manifest["levels"]:
        if evidence_set:
            measure, receipts = level["measure"], level["receipts"]
        else:
            measure, receipts = check.read_level(folder, level)
        rows = list(bm.rows(measure))
        if (
            sha256(check.input_bytes(rows)) != level["rects_sha256"]
            or len(rows) != level["rectangles"]
        ):
            raise SystemExit(
                f"{folder}: integer rows differ from the manifest at K = {level['K']}"
            )
        factor = MUTANTS[mutant]
        used = rows if factor == 1 else scaled(rows, factor)
        rows_file = workdir / f"rows-{folder.name}-{level['K']}-{mutant.replace('/', 'in')}"
        rows_file.write_bytes(check.input_bytes(used))
        selected = receipts[:1] if first_per_level else receipts
        for receipt in [] if evidence_set else selected:
            if receipt["header"] != check.header(measure, receipt["r"], kernel):
                raise SystemExit(
                    f"{folder}: header differs at K = {level['K']}, r = {receipt['r']}"
                )
        tag = f"{folder.name}-{level['K']}-{mutant.replace('/', 'in')}"
        jobs = [(binary, rows_file, receipt, workdir, cap, tag) for receipt in selected]
        with concurrent.futures.ThreadPoolExecutor(workers) as pool:
            results = list(pool.map(run_direction, jobs))
        for receipt, got in zip(selected, results, strict=True):
            got.update(
                folder=folder.name,
                n=manifest["n"],
                side=manifest["side"],
                kernel=kernel,
                K=level["K"],
                mutant=mutant,
                verified=got["verdict"] == "PASS"
                and got["exit"] == 0
                and got["lower_units"] >= M,
                matches_archive=all(
                    got[key] == receipt[key] for key in ("nodes", "leaves", "lower_units")
                ),
            )
            rows_out.append(got)
    return rows_out


def summarize(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = f"{row['folder']}|{row['mutant']}"
        s = by.setdefault(
            key,
            {
                "n": row["n"],
                "side": row["side"],
                "kernel": row["kernel"],
                "mutant": row["mutant"],
                "directions": 0,
                "verified": 0,
                "matches_archive": 0,
                "refused_on_coverage": 0,
                "nodes": 0,
                "cpu_seconds_approx": 0.0,
            },
        )
        s["directions"] += 1
        s["verified"] += int(row["verified"])
        s["matches_archive"] += int(row["matches_archive"])
        s["refused_on_coverage"] += int(
            row["verdict"] == "UNDECIDED" and row["unresolved"] is not None
        )
        s["nodes"] += row["nodes"]
        s["cpu_seconds_approx"] = round(s["cpu_seconds_approx"] + row["cpu_seconds_approx"], 3)
    return by


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n", 1)[0])
    parser.add_argument("folders", nargs="+", type=Path)
    parser.add_argument("--source", type=Path, required=True, help="the pinned source's proof/")
    parser.add_argument(
        "--out", type=Path, required=True, help="append per-direction rows here"
    )
    parser.add_argument("--mutant", choices=sorted(MUTANTS), default="none")
    parser.add_argument("--first-per-level", action="store_true")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--cap", type=int, default=CAP)
    args = parser.parse_args(argv)
    status = 0
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        source = stage_source(args.source.resolve(), workdir)
        bm, check = load_source(source)
        if (bm.G, bm.DS, bm.M) != (2**30, 2**32, M):
            raise SystemExit("unexpected fixed-point units in the source wrapper")
        for folder in args.folders:
            rows = replay_folder(
                folder.resolve(),
                source,
                check,
                bm,
                workdir,
                mutant=args.mutant,
                first_per_level=args.first_per_level,
                workers=args.workers,
                cap=args.cap,
            )
            with args.out.open("a", encoding="utf-8") as out:
                for row in rows:
                    out.write(json.dumps({"format": FORMAT, **row}, sort_keys=True) + "\n")
            for key, s in summarize(rows).items():
                print(key, json.dumps(s, sort_keys=True), flush=True)
                if args.mutant == "none" and s["verified"] != s["directions"]:
                    status = 1
    return status


if __name__ == "__main__":
    raise SystemExit(main())
