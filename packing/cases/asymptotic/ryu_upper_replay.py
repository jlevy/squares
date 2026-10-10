"""Replay the programs of Ryu's k2-minus-c-upper preprint from the two retained packets.

Issues #471 (version 1.0) and #486 (version 1.1) are retained as
``resources/web/squarepacker-k2-minus-c-upper-2026-10-09`` and
``resources/web/squarepacker-k2-minus-c-upper-v11-2026-10-10``. This command rebuilds each
version's complete upstream tree in a scratch directory from those packets (the v1.1
packet binds its 28 unchanged files to the v1.0 packet) and from the two certificates
hosted outside Git (``hosted/squarepacker-k2-minus-c-upper-certificates.yaml``, read
through `sqpack.hosted_data.require`, which checks their SHA-256 on every read), runs the
source's own programs with the project interpreter under ``python -I`` through
`cases.asymptotic.ryu_upper_runner`, and compares each output with the output the source
records under ``code/checker_outputs/``.

A comparison is semantic: JSON is compared as parsed values with only the fields that
record wall time (``seconds``, ``sec``, ``t_build``, ``t_check``), the arithmetic backend
(``gmp``) or the caller's file paths (``files``) left out, and the checker's text output
is compared line by line with its timings and backend name removed. Nothing is fetched
from the network: the programs fetch nothing, and the hosted certificates must already be
present (``python -m devtools.hosted_data fetch --manifest
hosted/squarepacker-k2-minus-c-upper-certificates.yaml``).

The receipt is a summary per job (command, wall, exit status, comparison) and the
programs' complete output, written to ``receipts/replay/`` of the packet that holds the
program's version. The jobs are the stage-4 table of
``docs/project/reviews/review-2026-10-10-squarepacker-k2-minus-c-upper.md`` (section 10).
Nothing here decides a theorem: a passing replay says that the source's programs, run
again on the retained bytes, print what the source says they print.

Usage, from ``packing/``::

    uv run --frozen --all-extras --group dev python -m cases.asymptotic.ryu_upper_replay \
        --workers 2 [--only GLOB] [--list] [--receipts]
"""

from __future__ import annotations

import argparse
import fnmatch
import gzip
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable, Iterable, Sequence
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import gmpy2
import mpmath
import numpy as np

from sqpack import retained_json
from sqpack.hosted_data import require

REPO = Path(__file__).resolve().parents[3]
PACKING = REPO / "packing"
WEB = PACKING / "resources/web"
V10 = WEB / "squarepacker-k2-minus-c-upper-2026-10-09"
V11 = WEB / "squarepacker-k2-minus-c-upper-v11-2026-10-10"
HOSTED = PACKING / "hosted/squarepacker-k2-minus-c-upper-certificates.yaml"
RUNNER = Path(__file__).with_name("ryu_upper_runner.py")
PACKETS = {"v1.0": V10, "v1.1": V11}
RECEIPT_DIR = Path("receipts/replay")
FETCHED = (
    "nothing: the programs fetch nothing, and the two hosted certificates were read from "
    "their local copies through packing/hosted/squarepacker-k2-minus-c-upper-certificates.yaml"
)
#: Fields that record wall time, the arithmetic backend or the caller's paths.
VOLATILE = frozenset({"seconds", "sec", "build_sec", "t_build", "t_check", "gmp", "files"})
_TIMING = re.compile(r"\s*\(\d+(\.\d+)?\s*s\)")
_BACKEND = re.compile(r"; arithmetic (fractions\.Fraction|gmpy2\.mpq)")
_DATA_PATH = re.compile(r"certificate \S*?(data/stair_k\d+\.json\.gz)")

#: The k of the five certificates of Theorem 1.6.
CERTIFICATE_KS = (100000, 1000000, 10000000, 38250000, 100000000)
#: b0 exponent, parameters and stated constants of the three tiers C of version 1.1
#: (code/README_code.txt, section 7). The stated constants are spelled as the recorded
#: merges echo them (``5220000000000``, ``2.95e+12``), which are the README's values.
TIERS_C = {
    "C1": (
        "7.3617",
        "0.153846,2.81426,3.00931,1.26,1.3608,1.35403,0.65",
        "14.473,41.19,5220000000000,0.04",
    ),
    "C2": (
        "7.2",
        "0.16,2.81426,3.00931,1.26,1.3608,1.35403,0.65",
        "14.805,41.78,2.95e+12,0.047",
    ),
    "C3": (
        "7.15",
        "0.165,2.81426,3.00931,1.26,1.3608,1.35403,0.65",
        "14.983,42.09,2.48e+12,0.05",
    ),
}
TIERS_AB = ("B1", "B1s", "B2", "A1", "A1s", "A2", "A3", "A4", "A5")
SLICES = ((0, 160), (160, 320))


# --------------------------------------------------------------------------- the trees


def _record(packet: Path) -> dict[str, Any]:
    return json.loads((packet / "acquisition/sources.json").read_text(encoding="utf-8"))


def hosted_path(name: str) -> Path:
    """The local copy of a hosted certificate, checked against its manifest."""
    relative = f"packing/cases/asymptotic/hosted/squarepacker-k2-minus-c-upper/{name}"
    return require(relative, HOSTED)


def assemble(version: str, root: Path) -> Path:
    """Write the version's complete upstream tree under ``root`` and return it.

    Retained files come from the version's packet; a file the packet pins because another
    packet retains it comes from that copy; a certificate neither packet retains comes from
    the hosted manifest. Every file of the version's subtree manifest is written.
    """
    packet = PACKETS[version]
    (entry,) = _record(packet)["sources"]
    source = packet / "source"
    tree = root / version
    if tree.exists():
        shutil.rmtree(tree)
    for path in sorted(p for p in source.rglob("*") if p.is_file()):
        target = tree / path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    v10_source = V10 / "source"
    for item in entry["pinned_only"]:
        target = tree / item["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if "identical_to" in item:
            origin = REPO / item["identical_to"]
        elif (v10_source / item["path"]).is_file():
            origin = v10_source / item["path"]
        else:
            origin = hosted_path(Path(item["path"]).name)
        shutil.copyfile(origin, target)
    written = sum(1 for p in tree.rglob("*") if p.is_file())
    if written != entry["subtree_file_count"]:
        raise RuntimeError(
            f"{version}: wrote {written} files, manifest has {entry['subtree_file_count']}"
        )
    return tree


# --------------------------------------------------------------------------- comparisons


def strip_volatile(value: Any) -> Any:
    """``value`` without the fields that record time, backend or paths, at any depth."""
    if isinstance(value, dict):
        return {k: strip_volatile(v) for k, v in value.items() if k not in VOLATILE}
    if isinstance(value, list):
        return [strip_volatile(v) for v in value]
    return value


def differences(ours: Any, theirs: Any, where: str = "") -> list[str]:
    """Every path at which two parsed JSON values differ, after `strip_volatile`."""
    a, b = strip_volatile(ours), strip_volatile(theirs)
    if isinstance(a, dict) and isinstance(b, dict):
        found: list[str] = []
        for key in sorted(set(a) | set(b)):
            if key not in a or key not in b:
                found.append(f"{where}/{key}: present in only one")
            else:
                found.extend(differences(a[key], b[key], f"{where}/{key}"))
        return found
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return [
            d
            for i, (x, y) in enumerate(zip(a, b, strict=True))
            for d in differences(x, y, f"{where}[{i}]")
        ]
    return [] if a == b else [f"{where or '/'}: {a!r} != {b!r}"[:400]]


def last_json_line(text: str) -> Any:
    """The JSON value on the last non-empty line, which is how the coverings print."""
    lines = [line for line in text.strip().splitlines() if line.strip()]
    return json.loads(lines[-1].lstrip("﻿"))


def normalise_text(text: str) -> list[str]:
    """Checker text without its timings, backend name or the caller's data path prefix."""
    out: list[str] = []
    for raw in text.strip().splitlines():
        line = _BACKEND.sub("", _TIMING.sub("", raw)).rstrip()
        out.append(_DATA_PATH.sub(r"certificate \1", line))
    return out


def compare_text(ours: str, recorded: str) -> list[str]:
    a, b = normalise_text(ours), normalise_text(recorded)
    if a == b:
        return []
    shared = zip(a[: len(b)], b[: len(a)], strict=True)
    found = [f"line {i + 1}: {x!r} != {y!r}" for i, (x, y) in enumerate(shared) if x != y]
    if len(a) != len(b):
        found.append(f"{len(a)} lines against {len(b)}")
    return found[:20]


# --------------------------------------------------------------------------- jobs


@dataclass
class Job:
    """One program run and how its output is compared with the record."""

    name: str
    version: str
    script: str
    args: tuple[str, ...]
    #: The recorded output, relative to the version's tree, and how to read it.
    recorded: str | None
    #: "text", "json-line", "json-file", "merged-entry", or "independent" for a module of
    #: this repository (``script`` is then its dotted name) whose JSON must say it passed.
    kind: str
    #: A file the program writes, relative to the tree, to compare instead of stdout.
    written: str | None = None
    #: Inputs copied into the job's own working directory, relative to the tree.
    cwd_inputs: tuple[str, ...] = ()
    #: A key of the recorded JSON to compare against (merged_v3.json holds one per tier).
    recorded_key: str | None = None
    #: Expected substring of stdout, checked in addition to the comparison.
    expect: str | None = None
    #: Jobs whose output this job reads.
    after: tuple[str, ...] = ()


def jobs() -> list[Job]:
    """The replay table of the review's section 10, in the order it is listed."""
    out: list[Job] = [
        Job(
            "const_stair",
            "v1.0",
            "code/const_stair.py",
            ("@work/const_stair_out.json",),
            "code/checker_outputs/const_stair_out.json",
            "json-file",
            written="@work/const_stair_out.json",
            expect="ALL CHECKS: True",
        ),
    ]
    out += [
        Job(
            f"stair_check_k{k}",
            "v1.0",
            "code/stair_check.py",
            (f"@tree/data/stair_k{k}.json.gz", str(k)),
            f"code/checker_outputs/stair_check_k{k}.txt",
            "text",
            expect="OVERALL: PASS",
        )
        for k in CERTIFICATE_KS
    ]
    out += [
        Job(
            f"stair_check_k{k}_mutate",
            "v1.0",
            "code/stair_check.py",
            (f"@tree/data/stair_k{k}.json.gz", str(k), "mutate"),
            f"code/checker_outputs/stair_check_k{k}_mutate.txt",
            "text",
            expect="MUTATION TEST: PASS",
        )
        for k in (100000, 100000000)
    ]
    out += [
        Job(
            "cert3e_160_64",
            "v1.0",
            "code/cert3e.py",
            ("160", "64"),
            "code/checker_outputs/cert3e_out_160_64.json",
            "json-file",
            written="@tree/code/cert3e_out_160_64.json",
        ),
        Job(
            "run_z_10000",
            "v1.0",
            "code/run_z.py",
            ("10000", "1", "0.5", "4"),
            "code/checker_outputs/wall_check_m10000_B4.txt",
            "json-line",
        ),
    ]
    for tier in TIERS_AB:
        names = []
        for iz0, iz1 in SLICES:
            name = f"cert_v3_{tier}_{iz0}_{iz1}"
            names.append(name)
            out.append(
                Job(
                    name,
                    "v1.1",
                    "code/cert_v3/cert_v3.py",
                    (
                        "run",
                        "--tier",
                        tier,
                        "--nz",
                        "320",
                        "--nt",
                        "128",
                        "--iz0",
                        str(iz0),
                        "--iz1",
                        str(iz1),
                    ),
                    f"code/checker_outputs/cert_v3/c_{tier}_{iz0}_{iz1}.json",
                    "json-line",
                    cwd_inputs=("code/cert_v3/tiers_v3.json",),
                )
            )
        out.append(
            Job(
                f"cert_v3_{tier}_merge",
                "v1.1",
                "code/cert_v3/cert_v3.py",
                ("merge", "--tier", tier, *(f"@out/{n}" for n in names)),
                "code/checker_outputs/cert_v3/merged_v3.json",
                "merged-entry",
                cwd_inputs=("code/cert_v3/tiers_v3.json",),
                recorded_key=tier,
                after=tuple(names),
            )
        )
        out.append(
            Job(
                f"cert_v3_{tier}_merge_recorded",
                "v1.1",
                "code/cert_v3/cert_v3.py",
                (
                    "merge",
                    "--tier",
                    tier,
                    *(
                        f"@tree/code/checker_outputs/cert_v3/c_{tier}_{a}_{b}.json"
                        for a, b in SLICES
                    ),
                ),
                "code/checker_outputs/cert_v3/merged_v3.json",
                "merged-entry",
                cwd_inputs=("code/cert_v3/tiers_v3.json",),
                recorded_key=tier,
            )
        )
    out.append(
        Job(
            "cert_v3_regression_v10",
            "v1.1",
            "code/cert_v3/cert_v3.py",
            (
                "run",
                "--lb0",
                "16",
                "--params",
                "1/12,4,4,1.5,0.65",
                "--nz",
                "160",
                "--nt",
                "64",
                "--full",
                "1",
            ),
            "code/checker_outputs/cert_v3/regression_v10_160x64.json",
            "json-line",
            cwd_inputs=("code/cert_v3/tiers_v3.json",),
        )
    )
    for index, (tier, (lb0, params, stated)) in enumerate(TIERS_C.items(), start=1):
        names = []
        for part, (iz0, iz1) in enumerate(SLICES):
            name = f"cert_v4_{tier}_s{part}"
            names.append(name)
            out.append(
                Job(
                    name,
                    "v1.1",
                    "code/cert_v4/cert_v4.py",
                    (
                        "run",
                        "--lb0",
                        lb0,
                        "--params",
                        params,
                        "--nz",
                        "320",
                        "--nt",
                        "128",
                        "--iz0",
                        str(iz0),
                        "--iz1",
                        str(iz1),
                    ),
                    f"code/checker_outputs/cert_v4/{index}{part}_{tier}_s{part}.json",
                    "json-line",
                )
            )
        out.append(
            Job(
                f"cert_v4_{tier}_merge",
                "v1.1",
                "code/cert_v4/cert_v4.py",
                ("merge", "--stated", stated, *(f"@out/{n}" for n in names)),
                f"code/checker_outputs/cert_v4/{tier}.json",
                "json-line",
                after=tuple(names),
            )
        )
        out.append(
            Job(
                f"cert_v4_{tier}_merge_recorded",
                "v1.1",
                "code/cert_v4/cert_v4.py",
                (
                    "merge",
                    "--stated",
                    stated,
                    *(
                        f"@tree/code/checker_outputs/cert_v4/{index}{p}_{tier}_s{p}.json"
                        for p in (0, 1)
                    ),
                ),
                f"code/checker_outputs/cert_v4/{tier}.json",
                "json-line",
            )
        )
    out += [
        Job(
            "sl_t2_test",
            "v1.1",
            "code/cert_v4/sl_t2_test.py",
            ("3000", "500"),
            "code/checker_outputs/cert_v4/sl_t2_test.json",
            "json-line",
        ),
        Job(
            "p3test_10000",
            "v1.1",
            "code/zc_tests/p3test/p3test.py",
            ("10000", "0.5", "4", "3/2", "0.65", "1"),
            "code/checker_outputs/zc_tests/p3test/p3_2.json",
            "json-line",
        ),
        Job(
            "a10_b2_zcp_102400",
            "v1.1",
            "code/zc_tests/e38_zcprime/a10.py",
            ("102400", "1", "3", "292683", "100000", "1.26562", "0", "1"),
            "code/checker_outputs/zc_tests/e38_zcprime/b2_zcp_102400.json",
            "json-line",
        ),
    ]
    return out + independent_jobs()


def independent_jobs() -> list[Job]:
    """This repository's own checks of the same statements, written from the text."""
    names = ("column-longer", "column-right", "column-tilt", "layer-longer", "lift-raised")
    mutations = tuple(arg for name in (*names, "wedge-longer") for arg in ("--mutate", name))
    out = [
        Job(
            "indep_l_packing",
            "v1.0",
            "cases.asymptotic.ryu_upper_l_packing",
            ("--packings", "30", "--formulas", "2000"),
            None,
            "independent",
        ),
        Job(
            "indep_constants",
            "v1.0",
            "cases.asymptotic.ryu_upper_constants",
            ("--subdivisions", "4000"),
            None,
            "independent",
        ),
        Job(
            "indep_staircase",
            "v1.0",
            "cases.asymptotic.ryu_upper_staircase",
            (),
            None,
            "independent",
        ),
    ]
    out += [
        Job(
            f"indep_certificate_k{k}",
            "v1.0",
            "cases.asymptotic.ryu_upper_certificates",
            ("--k", str(k), *(mutations if k in (100000, 100000000) else ())),
            None,
            "independent",
        )
        for k in CERTIFICATE_KS
    ]
    return out


def _resolve(arg: str, tree: Path, work: Path, outputs: Path) -> str:
    for prefix, base in (("@tree/", tree), ("@work/", work), ("@out/", outputs)):
        if arg.startswith(prefix):
            target = base / arg.removeprefix(prefix)
            return str(target.with_suffix(".json") if prefix == "@out/" else target)
    return arg


def _display(arg: str) -> str:
    return arg.replace("@tree/", "").replace("@work/", "WORK/").replace("@out/", "OUT/")


def run_job(job: Job, trees: dict[str, Path], scratch: Path) -> dict[str, Any]:
    """Run one job and compare its output with the record; return the receipt entry."""
    tree = trees[job.version]
    work = scratch / "work" / job.name
    work.mkdir(parents=True, exist_ok=True)
    outputs = scratch / "out"
    outputs.mkdir(exist_ok=True)
    for item in job.cwd_inputs:
        shutil.copyfile(tree / item, work / Path(item).name)
    args = [_resolve(a, tree, work, outputs) for a in job.args]
    if job.kind == "independent":
        command = ["nice", "-n", "10", sys.executable, "-m", job.script, *args]
        shown = ["python", "-m", job.script, *job.args]
        cwd = PACKING
    else:
        command = [
            "nice",
            "-n",
            "10",
            sys.executable,
            "-I",
            str(RUNNER),
            str(tree / job.script),
        ]
        command += args
        shown = ["python", "-I", "cases/asymptotic/ryu_upper_runner.py", job.script]
        shown += map(_display, job.args)
        cwd = work
    start = time.monotonic()
    done = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
    wall = round(time.monotonic() - start, 2)
    (outputs / f"{job.name}.json").write_text(done.stdout, encoding="utf-8")
    entry: dict[str, Any] = {
        "job": job.name,
        "version": job.version,
        "command": " ".join(shown),
        "cwd": "packing/"
        if job.kind == "independent"
        else "a fresh directory"
        + (f" holding {', '.join(job.cwd_inputs)}" if job.cwd_inputs else ""),
        "wall_seconds": wall,
        "exit": done.returncode,
        "recorded": job.recorded,
    }
    problems: list[str] = []
    if done.returncode != 0:
        problems.append(f"exit {done.returncode}: {done.stderr.strip()[-400:]}")
    if job.expect and job.expect not in done.stdout:
        problems.append(f"stdout lacks {job.expect!r}")
    if job.kind == "independent" and not problems:
        try:
            if json.loads(done.stdout).get("passed") is not True:
                problems.append("the check did not pass")
        except ValueError as error:
            problems.append(f"output is not JSON: {error}")
    if job.recorded and not problems:
        recorded_text = (tree / job.recorded).read_text(encoding="utf-8-sig")
        try:
            problems += _compare(job, done.stdout, recorded_text, tree, work)
        except (ValueError, KeyError, IndexError) as error:
            problems.append(f"output could not be compared: {error}")
    entry["matches_record"] = not problems
    entry["differences"] = problems
    entry["stdout"] = done.stdout
    entry["stderr"] = done.stderr
    return entry


def _compare(job: Job, stdout: str, recorded_text: str, tree: Path, work: Path) -> list[str]:
    if job.kind == "text":
        return compare_text(stdout, recorded_text)
    if job.kind == "json-file":
        assert job.written is not None
        written = Path(_resolve(job.written, tree, work, work))
        return differences(
            json.loads(written.read_text(encoding="utf-8")), json.loads(recorded_text)
        )
    recorded = (
        json.loads(recorded_text)
        if job.kind == "merged-entry"
        else last_json_line(recorded_text)
    )
    if job.recorded_key is not None:
        recorded = recorded[job.recorded_key]
    return differences(last_json_line(stdout), recorded)


# --------------------------------------------------------------------------- the command


def environment() -> dict[str, Any]:
    """The interpreter and libraries the programs ran under, for the receipt."""
    return {
        "python": platform.python_version(),
        "mpmath": mpmath.__version__,
        "numpy": np.__version__,
        "gmpy2": gmpy2.version(),
        "cpus": os.cpu_count(),
        "load_average_at_start": [round(x, 2) for x in os.getloadavg()],
        "platform": platform.platform(),
    }


def rank(job: Job) -> int:
    """Cheapest first, so that a run cut short has replayed the most jobs."""
    if job.version == "v1.0" or job.name in ("sl_t2_test", "cert_v3_regression_v10"):
        return 0
    if job.name.endswith("_merge_recorded") or job.kind == "independent":
        return 1
    if job.name.startswith(("cert_v3_", "cert_v4_")):
        return 2
    return 3 if job.name.startswith("p3test") else 4


def schedule(
    selected: Sequence[Job],
    workers: int,
    work: Callable[[Job], dict[str, Any]],
    done: Callable[[dict[str, Any]], None] = lambda _entry: None,
) -> list[dict[str, Any]]:
    """Run the jobs on ``workers`` threads, each job after the jobs it names in ``after``.

    ``done`` sees every entry as its job finishes, from the scheduling thread.
    """
    results: dict[str, dict[str, Any]] = {}
    names = {job.name for job in selected}
    pending = list(selected)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        running: dict[Future[dict[str, Any]], str] = {}
        while pending or running:
            ready = [j for j in pending if all(a in results or a not in names for a in j.after)]
            while ready and len(running) < workers:
                job = ready.pop(0)
                pending.remove(job)
                running[pool.submit(work, job)] = job.name
            if not running:
                raise RuntimeError(
                    f"jobs wait on jobs that never run: {[j.name for j in pending]}"
                )
            finished, _ = wait(running, return_when=FIRST_COMPLETED)
            for future in finished:
                name = running.pop(future)
                entry = results[name] = future.result()
                state = "matches" if entry["matches_record"] else "DIFFERS"
                print(f"{entry['wall_seconds']:8.1f} s  {state:8}  {name}", flush=True)
                done(entry)
    return [results[job.name] for job in selected]


def _previous(path: Path, key: str) -> dict[str, dict[str, Any]]:
    """Earlier entries by job name, so that a partial run updates its own jobs only."""
    if not path.is_file():
        return {}
    if path.name.endswith(".jsonl.gz"):
        text = gzip.decompress(path.read_bytes()).decode("utf-8")
        rows = [json.loads(line) for line in text.splitlines() if line]
    else:
        rows = json.loads(path.read_text(encoding="utf-8"))[key]
    return {row["job"]: row for row in rows}


def write_receipts(
    entries: Iterable[dict[str, Any]], env: dict[str, Any], run: str
) -> list[Path]:
    """One summary and one complete-output file per packet, under ``receipts/replay/``.

    A run that selects some jobs replaces those jobs' entries and keeps the others, each
    with the environment and the start time of the run that produced it.
    """
    written: list[Path] = []
    by_version: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        by_version.setdefault(entry["version"], []).append(entry)
    order = [job.name for job in jobs()]
    for version, rows in by_version.items():
        directory = PACKETS[version] / RECEIPT_DIR
        directory.mkdir(parents=True, exist_ok=True)
        summary_path, outputs_path = directory / "replay.json", directory / "outputs.jsonl.gz"
        summaries = _previous(summary_path, "jobs")
        outputs = _previous(outputs_path, "")
        for row in rows:
            summaries[row["job"]] = {
                **{k: v for k, v in row.items() if k not in ("stdout", "stderr")},
                "environment": env,
                "run_started_utc": run,
            }
            outputs[row["job"]] = {
                "job": row["job"],
                "stdout": row["stdout"],
                "stderr": row["stderr"],
            }
        ranked = sorted(summaries, key=order.index)
        summary = {
            "format": "ryu-k2-minus-c-upper-replay/v1",
            "tool": "packing/cases/asymptotic/ryu_upper_replay.py",
            "version": version,
            "fetched": FETCHED,
            "all_match": all(summaries[name]["matches_record"] for name in ranked),
            "jobs": [summaries[name] for name in ranked],
        }
        summary_path.write_text(retained_json.dumps(summary), encoding="utf-8")
        # Deterministic gzip, as devtools.retained_data stores a packet's large files: no
        # name and mtime 0, so the same outputs always give the same bytes.
        text = "".join(json.dumps(outputs[name]) + "\n" for name in ranked)
        outputs_path.write_bytes(gzip.compress(text.encode("utf-8"), compresslevel=9, mtime=0))
        written += [summary_path, outputs_path]
    return written


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("--workers", type=int, default=2, help="processes at once (default 2)")
    parser.add_argument(
        "--only", action="append", metavar="GLOB", help="run the jobs whose name matches"
    )
    parser.add_argument("--list", action="store_true", help="list the jobs and stop")
    parser.add_argument(
        "--receipts", action="store_true", help="write the packets' replay receipts"
    )
    parser.add_argument("--scratch", type=Path, help="keep the trees and outputs here")
    args = parser.parse_args(argv)
    selected = sorted(
        (
            j
            for j in jobs()
            if not args.only or any(fnmatch.fnmatch(j.name, g) for g in args.only)
        ),
        key=rank,
    )
    if args.list:
        for job in selected:
            print(
                f"{job.name:32} {job.version}  {job.script} {' '.join(map(_display, job.args))}"
            )
        return 0
    scratch = args.scratch or Path(tempfile.mkdtemp(prefix="ryu-upper-replay-"))
    scratch.mkdir(parents=True, exist_ok=True)
    trees = {v: assemble(v, scratch / "trees") for v in sorted({j.version for j in selected})}
    env = environment()
    run = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    start = time.monotonic()

    def record(entry: dict[str, Any]) -> None:
        if args.receipts:
            write_receipts([entry], env, run)

    entries = schedule(selected, args.workers, lambda job: run_job(job, trees, scratch), record)
    total = round(time.monotonic() - start, 1)
    failed = [e["job"] for e in entries if not e["matches_record"]]
    differ = failed or "none"
    print(f"{len(entries)} jobs in {total} s on {args.workers} workers; differ: {differ}")
    if args.receipts:
        packets = ", ".join(sorted(packet.name for packet in PACKETS.values()))
        print(f"receipts under {RECEIPT_DIR} of {packets}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
