"""A sample of #847's filled-end rows, written out and decided on both exact routes.

Mohsen Karimi's filled-end set V2.0 (#847; Zenodo 10.5281/zenodo.23819397, kept by the
``karimi-records-2026-10-31`` packet from his GitHub copy at ad8b094) states 5,134
upper bounds at n = 1182 to 9946, each an exact side and the seven parameters of a
two-band L packing whose band ends are filled with axis-parallel layers: Sungjoon Ryu's
L frame (Theorem 1.3), Evan Daniel's end fill as Kevin Fang's note writes it, and the
author's independent bands and search. No checker this project maintains decides that
construction from its parameters yet; W9 (think-fuwd) owns one. Until it lands, this
module is stage 4's priced sample (think-qczx): at `SAMPLE`'s counts it writes each row's
packing out and decides the certificate on both maintained exact routes of
`devtools.couzo_678_replay`, with their six controls, as
`devtools.two_strip_checker.replay_row` does for the two-strip family.

**Who wrote what.** The packing is written out by the author's own builder, ``build``
in his ``filled_ends.py``, read before it runs and made from the packet's copy. V2.0
states no digest for that file; when the packet was written its bytes were the
``filled_ends.py`` member of the V1.0 archive, ``karimi_filled_end_v2.zip``, whose own
SHA-256 the author stated on #836 on 27 October. From then on Git keeps the bytes and
``acquire_source --check`` holds them to the packet's manifest (OR-16), so this module
compares no digest. The decision is first-party: the routes and their controls are this
repository's, and they share nothing with the author's checker, ``check_cert.py``, which
does not run here. So each sampled certificate is the producer's construction, decided
by code that is not the producer's, and the run decides those certificates and nothing
else.

**The table.** ``filled_records.csv`` is another party's file, whose bytes had the
SHA-256 #847 states when retained, read as untrusted data: its header exactly
`COLUMNS`, each sampled row's literals matched whole, K equal to ceil(sqrt(n)), and each
count once. The builder's side must equal the row's ``side_exact``, and the certificate
must hold n squares; any other outcome is a `SampleError`.

**What it does not do.** A sample decides the counts it ran and says nothing about the
rest: 5 of 5,134 rows. Whether a row is below every earlier report at its count is the
walk's to decide (think-llit). The receipt, ``receipts/filled-end-replay-sample.json`` in
the packet, pins each written-out certificate by its SHA-256 and size and keeps none
(OR-18), and records each count's CPU, which re-prices think-qczx.

From ``packing/``, with the project interpreter::

    python -m devtools.filled_end_sample replay [--workers 2]
    python -m devtools.filled_end_sample check [--replay]
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import platform
import re
import time
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any

from strif import atomic_output_file

from devtools import evand_exact_certificates as legacy
from devtools.retained_data import read_retained_bytes
from sqpack.retained_json import dumps as retained_dumps

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent

PACKET_PATH = "packing/resources/web/karimi-records-2026-10-31"
PACKET = REPO / PACKET_PATH
ISSUE = "https://github.com/jlevy/squares/issues/847"
DOI = "10.5281/zenodo.23819397"
FORMAT = "filled-end-replay-sample-v1"
#: The author's table and builder in the packet, and the commit the packet pins.
TABLE = "source/filled_records.csv"
BUILDER = "source/filled_ends.py"
SOURCE_COMMIT = "ad8b094be0785ed47fd90f5b965bc84c077d5bb1"
#: The columns of V2.0's ``filled_records.csv``, exactly and in order.
COLUMNS = (
    "n",
    "K",
    "side_exact",
    "side",
    "previous_best_side",
    "previous_source",
    "bV",
    "tV",
    "yV",
    "bH",
    "tH",
    "yH",
)
#: The sampled counts: the first, the first at or after 2500, 4990 (V2.0 has no row from
#: 4996 to 5009), 7500, and the last.
SAMPLE = (1182, 2505, 4990, 7500, 9946)
RECEIPT = "receipts/filled-end-replay-sample.json"

_RATIONAL = re.compile(r"-?[0-9]{1,40}(/[1-9][0-9]{0,39})?")
_INTEGER = re.compile(r"[1-9][0-9]{0,5}")


class SampleError(ValueError):
    """The packet's files, a sampled row or its built packing is not what it must be."""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def builder() -> ModuleType:
    """The author's ``filled_ends`` module, made from the packet's copy: its bytes are
    read once from Git, compiled and run, so no bytecode is written into the packet."""
    path = PACKET / BUILDER
    data = read_retained_bytes(path)
    module = ModuleType("karimi_filled_ends")
    module.__file__ = str(path)
    exec(compile(data, str(path), "exec"), module.__dict__)
    return module


def rows() -> dict[int, dict[str, str]]:
    """V2.0's rows by count, from the packet's table."""
    data = read_retained_bytes(PACKET / TABLE)
    try:
        lines = list(csv.reader(io.StringIO(data.decode("utf-8"), newline=""), strict=True))
    except (UnicodeDecodeError, csv.Error) as error:
        raise SampleError(f"{TABLE}: {error}") from error
    if not lines or tuple(lines[0]) != COLUMNS:
        raise SampleError(f"{TABLE}: the header is not {list(COLUMNS)}")
    found: dict[int, dict[str, str]] = {}
    for number, fields in enumerate(lines[1:], start=1):
        if len(fields) != len(COLUMNS):
            raise SampleError(f"{TABLE} row {number}: {len(fields)} fields")
        row: dict[str, str] = dict(zip(COLUMNS, fields, strict=True))
        if _INTEGER.fullmatch(row["n"]) is None:
            raise SampleError(f"{TABLE} row {number}: n is {row['n'][:20]!r}")
        n = int(row["n"])
        if n in found:
            raise SampleError(f"{TABLE}: n = {n} appears twice")
        found[n] = row
    return found


def parameters(
    row: Mapping[str, str],
) -> tuple[int, int, Fraction, Fraction, int, Fraction, Fraction]:
    """A sampled row's K, bV, tV, yV, bH, tH and yH, each literal matched whole."""
    n = int(row["n"])
    for name in ("K", "bV", "bH"):
        if _INTEGER.fullmatch(row[name]) is None:
            raise SampleError(f"n = {n}: {name} is {row[name][:20]!r}")
    for name in ("side_exact", "tV", "yV", "tH", "yH"):
        if _RATIONAL.fullmatch(row[name]) is None:
            raise SampleError(f"n = {n}: {name} is {row[name][:40]!r}")
    k = int(row["K"])
    if k != math.isqrt(n - 1) + 1:
        raise SampleError(f"n = {n}: K = {k} is not ceil(sqrt(n))")
    return (
        k,
        int(row["bV"]),
        Fraction(row["tV"]),
        Fraction(row["yV"]),
        int(row["bH"]),
        Fraction(row["tH"]),
        Fraction(row["yH"]),
    )


def certificate(n: int, build: Callable[..., Any] | None = None) -> legacy.Certificate:
    """The packing V2.0 states at n, written out by the author's builder: its side must be
    the row's exact side and it must hold n squares."""
    row = rows()[n]
    made = build or builder().build
    side, squares = made(*parameters(row), n)
    if Fraction(side) != Fraction(row["side_exact"]):
        raise SampleError(f"n = {n}: the builder's side is not the row's")
    if len(squares) != n:
        raise SampleError(f"n = {n}: the builder made {len(squares)} squares")
    poses = tuple(legacy.Pose(Fraction(x), Fraction(y), Fraction(t)) for x, y, t in squares)
    return legacy.Certificate(n, Fraction(side), poses)


def replay_row(n: int) -> dict[str, Any]:
    """One sampled count: the certificate written out, decided on both routes, and the six
    controls, with each part's CPU."""
    from devtools import couzo_678_replay as base  # noqa: PLC0415

    started = time.process_time()
    cert = certificate(n)
    built = time.process_time()
    text = legacy.serialize(cert).encode("utf-8")
    result = base.decide(base.geometry(cert))
    positive = time.process_time()
    checked = base.decide_controls(cert)
    ended = time.process_time()
    return {
        "n": n,
        "certificate_sha256": _sha256(text),
        "certificate_bytes": len(text),
        "exact_side": legacy.literal(cert.side),
        "verified": result["passed"],
        "decision": result,
        "controls": checked,
        "cpu_seconds": {
            "build": round(built - started, 2),
            "positive": round(positive - built, 2),
            "controls": round(ended - positive, 2),
        },
    }


def _environment() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "machine": platform.machine(),
    }


def replay(workers: int) -> dict[str, Any]:
    """Replay `SAMPLE` and write the receipt."""
    from devtools import couzo_678_replay as base  # noqa: PLC0415

    started, wall = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"), time.monotonic()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        found = list(pool.map(replay_row, SAMPLE))
    receipt = {
        "format": FORMAT,
        "issue": ISSUE,
        "doi": DOI,
        "packet": PACKET_PATH,
        "table": f"{PACKET_PATH}/{TABLE}",
        "builder": f"{PACKET_PATH}/{BUILDER}",
        "source_commit": SOURCE_COMMIT,
        "builder_note": (
            "the author's own build(), read before it ran; it writes the packing out and "
            "decides nothing. The routes decide, and they share no code with the author's "
            "check_cert.py, which did not run"
        ),
        "routes": "packing/devtools/couzo_678_replay.py (decide and decide_controls)",
        "filter_lemma": base.FILTER_LEMMA,
        "controls": list(base.CONTROLS),
        "coverage": {"checked": len(SAMPLE), "of": len(rows()), "unit": "rows"},
        "environment": _environment(),
        "started_utc": started,
        "wall_seconds": round(time.monotonic() - wall, 1),
        "workers": workers,
        "rows": found,
    }
    path = PACKET / RECEIPT
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_text(retained_dumps(receipt, sort_keys=True), encoding="utf-8")
    return receipt


def stable(row: Mapping[str, Any]) -> dict[str, Any]:
    """A replay row without its timings."""
    copy = json.loads(json.dumps(row))
    copy.pop("cpu_seconds", None)
    copy["decision"].pop("cpu_seconds", None)
    return copy


def check(*, again: bool = False) -> list[str]:
    """Problems with the receipt: its format and pin, the counts, every certificate
    verified on both routes and every control refused by both; with ``again``, each count
    replayed and compared, timings aside. Empty when it holds."""
    from devtools import couzo_678_replay as base  # noqa: PLC0415

    receipt = json.loads((PACKET / RECEIPT).read_text(encoding="utf-8"))
    problems = []
    if (receipt["format"], receipt.get("source_commit")) != (FORMAT, SOURCE_COMMIT):
        problems.append("the receipt's header is not this module's")
    if receipt["coverage"] != {"checked": len(SAMPLE), "of": len(rows()), "unit": "rows"}:
        problems.append("the receipt's coverage is not the sample's")
    if [item["n"] for item in receipt["rows"]] != list(SAMPLE):
        return [*problems, "the receipt's counts are not the sample"]
    if receipt["controls"] != list(base.CONTROLS):
        problems.append("the receipt's controls are not the routes' six")
    for kept in receipt["rows"]:
        n = kept["n"]
        if not kept["verified"]:
            problems.append(f"n={n}: the certificate failed a route")
        if [item["control"] for item in kept["controls"]] != list(base.CONTROLS) or not all(
            item["refused_by_sqpack"] and item["refused_by_independent"]
            for item in kept["controls"]
        ):
            problems.append(f"n={n}: a route accepted a control")
        if again and stable(replay_row(n)) != stable(kept):
            problems.append(f"n={n}: the replay differs from the receipt")
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n", 1)[0])
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("replay")
    run.add_argument("--workers", type=int, default=2)
    audit = commands.add_parser("check")
    audit.add_argument("--replay", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "check":
        problems = check(again=args.replay)
        for problem in problems:
            print(problem)
        print("FAILED" if problems else f"OK: {len(SAMPLE)} sampled counts verified")
        return 1 if problems else 0
    receipt = replay(args.workers)
    print(
        json.dumps(
            [
                {
                    key: row[key]
                    for key in ("n", "verified", "certificate_sha256", "cpu_seconds")
                }
                for row in receipt["rows"]
            ],
            indent=1,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
