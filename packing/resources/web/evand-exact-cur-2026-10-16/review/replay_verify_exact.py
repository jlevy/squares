#!/usr/bin/env python3
"""Replay Evan Daniel's verify_exact.py on the 23 exact forms of issue #639, with controls.

The checker is the source's own, run unchanged from its retained copy,
``packing/resources/web/evand-exact-and-local-reports-2026-10-12/source/search/exact/verify_exact.py``
(SHA-256 ``a0f38ca8...bab4``, byte-identical to ``search/exact/verify_exact.py`` at
``7d1407a``), which was read before it was run. Each data file is read from this packet,
or for the four the packet pins by digest only from ``--pinned``, and is refused unless
its SHA-256 is the one the packet's manifest records.

For each count the program runs the positive, and at each of the 19 counts whose form the
packet retains also the four controls, each in its own ``python -I`` child process, at
most ``--workers`` at a time (``--controls-at all`` adds the four pinned-only counts, whose
controls cost nearly a positive each):

- **the positive:** the file as published, which must print ``VALID.`` with the
  statement the source's ``data/verify.txt`` prints for it;
- **a moved square:** the first square the file's contact list puts against a wall,
  moved ``10^-6`` through that wall, which must be refused;
- **an enlarged side:** ``S`` in ``K`` raised by ``10^-6``, so ``p(S)`` is no longer
  ``0`` mod ``f``, which must be refused;
- **a side below the root:** ``S``'s interval replaced by one wholly below it, which
  must be refused;
- **a duplicate square:** square 1 replaced by square 0, which must be refused on that
  pair.

It also factors each ``p`` over the integers with SymPy (``factor_list``), which the
source asserts irreducible and none of its programs checks. ``p`` counts as irreducible
only when it is squarefree and its factorization is one factor, of multiplicity 1 and of
``p``'s degree, so a perfect power ``q^k`` is refused.

An interrupted invocation resumes from ``--scratch``'s cache. Each cached record is keyed
by the run it records: the input's SHA-256, the checker's SHA-256 and the control kind
(none for the positive). It is reused only when all three match; otherwise the run is
repeated.

The mutated files are written to ``--scratch`` and deleted after their run. The receipt
records every run's command, exit status, last line, wall and CPU time, and the
digests of every input. From ``packing/``::

    .venv/bin/python3 resources/web/evand-exact-cur-2026-10-16/review/replay_verify_exact.py \\
        --pinned DIR --scratch DIR [--workers 2]
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy

PACKET = Path(__file__).resolve().parents[1]
REPO = PACKET.parents[3]
DATA = PACKET / "source/search/exact/cur/data"
MANIFEST = PACKET / "acquisition/upstream-subtree.sha256"
CHECKER = (
    REPO
    / "packing/resources/web/evand-exact-and-local-reports-2026-10-12/source/search/exact/verify_exact.py"
)
CHECKER_SHA256 = "a0f38ca87c13c7e1b1d6ca99d69adea47df6008a645e3b4dbb79e8e0af35bab4"
RECEIPT = PACKET / "receipts/replay-verify-exact.json"
# fmt: off
COUNTS = (
    51, 70, 88, 102, 123, 126, 153, 172, 175, 199, 204, 207, 232, 258, 259, 263, 266, 267,
    292, 295, 297, 301, 302,
)
# fmt: on
STEP = Fraction(1, 10**6)
#: Which coordinate a wall contact pins, and which way moving through the wall goes.
THROUGH = {"L": ("x", -1), "R": ("x", 1), "B": ("y", -1), "T": ("y", 1)}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest() -> dict[str, str]:
    rows = (line.split() for line in MANIFEST.read_text(encoding="utf-8").splitlines())
    return {path.removeprefix("./"): digest for digest, path in rows}


def located(n: int, pinned: Path, digests: dict[str, str]) -> tuple[Path, str]:
    name = f"n-{n}.minpoly.json.gz"
    path = DATA / name
    where = "retained in the packet"
    if not path.is_file():
        path, where = pinned / name, "pinned by digest; read from a copy outside the repository"
    digest = sha256(path)
    expected = digests[f"search/exact/cur/data/{name}"]
    if digest != expected:
        sys.exit(f"{name}: SHA-256 {digest} is not the manifest's {expected}")
    return path, where


def source_lines() -> dict[int, str]:
    lines = (DATA / "verify.txt").read_text(encoding="utf-8").splitlines()
    return {int(line.split(":")[0].split("n-")[1].split(".")[0]): line for line in lines}


def statement(line: str) -> str:
    """The part of a checker's line after the file name, which names no path."""
    return line.split(": ", 1)[1] if ": " in line else line


def run(path: Path) -> dict[str, Any]:
    command = [sys.executable, "-I", str(CHECKER), str(path)]
    started = time.monotonic()
    child = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    assert child.stdout is not None
    output = child.stdout.read()
    child.stdout.close()
    # Reap the child here, not in Popen, so its own resource usage is read.
    _, status, usage = os.wait4(child.pid, 0)
    child.returncode = os.waitstatus_to_exitcode(status)
    wall = time.monotonic() - started
    lines = output.strip().splitlines()
    return {
        "command": ["python", "-I", "verify_exact.py", path.name],
        "exit": child.returncode,
        "last_line": statement(lines[-1]) if lines else "",
        "wall_seconds": round(wall, 2),
        "cpu_seconds": round(usage.ru_utime + usage.ru_stime, 2),
    }


def cached(cache: Path, name: str, key: dict[str, Any], job: Any) -> dict[str, Any]:
    """A run's record, from ``cache`` when an earlier, interrupted invocation finished the
    same run: the same input digest, checker digest and control kind, all in ``key``."""
    path = cache / f"{name}.json"
    if path.is_file():
        stored = json.loads(path.read_text(encoding="utf-8"))
        if stored.get("key") == key:
            return stored["record"]
    record = job()
    path.write_text(json.dumps({"key": key, "record": record}), encoding="utf-8")
    return record


def run_key(digest: str, kind: str | None) -> dict[str, Any]:
    """What a cached run must match to be reused: input, checker and control kind."""
    return {"input_sha256": digest, "checker_sha256": CHECKER_SHA256, "control": kind}


def mutate(data: dict[str, Any], kind: str) -> tuple[dict[str, Any], str]:
    mutated = json.loads(json.dumps(data))
    if kind == "moved-square":
        contact = next(item for item in mutated["equations"] if item[0] == "W")
        square, wall = int(contact[1]), str(contact[3])
        coordinate, sign = THROUGH[wall]
        values = mutated["squares"][square][coordinate]
        values[0] = str(Fraction(values[0]) + sign * STEP)
        return mutated, f"square {square} moved 1e-6 through the {wall} wall it touches"
    if kind == "enlarged-side":
        values = mutated["S"]["in_K"]
        values[0] = str(Fraction(values[0]) + STEP)
        return mutated, "S in K raised by 1e-6, so p(S) is not 0 mod f"
    if kind == "side-below-root":
        low, high = (Fraction(value) for value in mutated["S"]["interval"])
        width = high - low
        mutated["S"]["interval"] = [str(low - 3 * width), str(low - 2 * width)]
        return mutated, "S's interval replaced by one wholly below the source's"
    if kind == "duplicate-square":
        mutated["squares"][1] = json.loads(json.dumps(mutated["squares"][0]))
        return mutated, "square 1 replaced by square 0"
    raise ValueError(kind)


CONTROLS = ("moved-square", "enlarged-side", "side-below-root", "duplicate-square")


def control(n: int, path: Path, kind: str, scratch: Path) -> dict[str, Any]:
    data = json.loads(gzip.decompress(path.read_bytes()).decode("utf-8"))
    mutated, what = mutate(data, kind)
    target = scratch / f"n-{n}.{kind}.minpoly.json.gz"
    target.write_bytes(gzip.compress(json.dumps(mutated).encode("utf-8"), mtime=0))
    try:
        record = run(target)
    finally:
        target.unlink()
    record["control"] = kind
    record["mutation"] = what
    record["refused"] = record["exit"] == 1 and "NOT VERIFIED" in record["last_line"]
    return record


def factored(path: Path) -> dict[str, Any]:
    data = json.loads(gzip.decompress(path.read_bytes()).decode("utf-8"))
    coefficients = [int(c) for c in data["S"]["poly"]]
    x = sympy.Symbol("x")
    started = time.process_time()
    poly = sympy.Poly(list(reversed(coefficients)), x)
    _, factors = sympy.factor_list(poly)
    shape = sorted([int(sympy.Poly(factor, x).degree()), int(power)] for factor, power in factors)
    degree = len(coefficients) - 1
    squarefree = sympy.degree(sympy.gcd(poly, poly.diff(x)), x) == 0
    return {
        "degree": degree,
        "factors": shape,
        "squarefree": squarefree,
        "irreducible": squarefree and shape == [[degree, 1]],
        "cpu_seconds": round(time.process_time() - started, 2),
        "method": f"sympy {sympy.__version__} factor_list over the integers",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("--pinned", type=Path, required=True)
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--controls-at", choices=("retained", "all"), default="retained")
    args = parser.parse_args(argv)
    if sha256(CHECKER) != CHECKER_SHA256:
        sys.exit(f"{CHECKER} is not the checker that was read")
    args.scratch.mkdir(parents=True, exist_ok=True)
    cache = args.scratch / "cache"
    cache.mkdir(exist_ok=True)
    digests = manifest()
    expected = source_lines()
    inputs = {n: located(n, args.pinned, digests) for n in COUNTS}
    # located() refused any file whose digest is not the manifest's, so this is the input's.
    digest_of = {n: digests[f"search/exact/cur/data/{inputs[n][0].name}"] for n in COUNTS}
    started = datetime.now(UTC)
    clock = time.monotonic()
    jobs = sorted(inputs, key=lambda n: -inputs[n][0].stat().st_size)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        positives = dict(
            zip(
                jobs,
                pool.map(
                    lambda n: cached(
                        cache, f"n-{n}", run_key(digest_of[n], None),
                        lambda: run(inputs[n][0]),
                    ),
                    jobs,
                ),
                strict=True,
            )
        )
        controlled = [
            n for n in jobs if args.controls_at == "all" or inputs[n][1] == "retained in the packet"
        ]
        tasks = [(n, kind) for n in controlled for kind in CONTROLS]
        controls = list(
            pool.map(
                lambda item: cached(
                    cache,
                    f"n-{item[0]}.{item[1]}",
                    run_key(digest_of[item[0]], item[1]),
                    lambda: control(item[0], inputs[item[0]][0], item[1], args.scratch),
                ),
                tasks,
            )
        )
    rows = []
    for n in COUNTS:
        path, where = inputs[n]
        positive = positives[n]
        rows.append({
            "n": n,
            "file": path.name,
            "sha256": digests[f"search/exact/cur/data/{path.name}"],
            "bytes": path.stat().st_size,
            "where": where,
            "positive": positive,
            "matches_source_verify_txt": positive["exit"] == 0
            and positive["last_line"] == statement(expected[n]),
            "controls": [item for (m, _), item in zip(tasks, controls, strict=True) if m == n],
            "polynomial": factored(path),
        })
        print(n, positive["exit"], positive["wall_seconds"], rows[-1]["matches_source_verify_txt"],
              [c["refused"] for c in rows[-1]["controls"]], rows[-1]["polynomial"]["irreducible"])
    receipt = {
        "format": "evand-verify-exact-replay-v1",
        "bead": "think-g59l",
        "issue": "https://github.com/jlevy/squares/issues/639",
        "ran_at_utc": started.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "wall_seconds_this_invocation": round(time.monotonic() - clock, 1),
        "cpu_seconds_of_runs": round(
            sum(row["positive"]["cpu_seconds"] for row in rows)
            + sum(c["cpu_seconds"] for row in rows for c in row["controls"]),
            1,
        ),
        "workers": args.workers,
        "controls_at": (
            "every count"
            if args.controls_at == "all"
            else "the 19 counts whose form the packet retains"
        ),
        "program": {
            "path": str(CHECKER.relative_to(REPO)),
            "sha256": CHECKER_SHA256,
            "upstream": "evand/square-packing@7d1407a0b66c46e32cdbcbd5619586fe2bdd52a1 search/exact/verify_exact.py",
            "read_before_running": True,
            "relationship_to_generator": "same-implementation",
            "where": "run unchanged from the retained copy, each file in its own python -I child process",
        },
        "driver": {"path": str(Path(__file__).resolve().relative_to(REPO)), "sha256": sha256(Path(__file__))},
        "environment": {
            "python": f"CPython {platform.python_version()} (the project interpreter); the source runs python3",
            "sympy": sympy.__version__,
            "host": f"{os.cpu_count()} CPUs, shared; nice -n 10",
        },
        "summary": {
            "positives_valid": sum(1 for row in rows if row["positive"]["exit"] == 0),
            "positives_matching_source": sum(1 for row in rows if row["matches_source_verify_txt"]),
            "controls_refused": sum(1 for row in rows for c in row["controls"] if c["refused"]),
            "controls": sum(len(row["controls"]) for row in rows),
            "squarefree": sum(1 for row in rows if row["polynomial"]["squarefree"]),
            "irreducible": sum(1 for row in rows if row["polynomial"]["irreducible"]),
        },
        "rows": rows,
    }
    RECEIPT.parent.mkdir(exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(receipt["summary"]), receipt["cpu_seconds_of_runs"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
