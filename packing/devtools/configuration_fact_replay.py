"""Decide exact configurations a packet keeps as derived JSON facts, on both exact routes.

Hyukdong Kim attached exact configurations for T-244 at 172 and 263 to issue 804
(think-4rzl), in the ``minpoly.json`` format of Evan Daniel's ``verify_exact.py``. The
packet ``hyukdongkim-t244-configurations-2026-10-25`` keeps each as a derived fact,
``facts/nNNN.json.gz`` in ``issue-804-configuration-fact-v1``: the certificate's content
under ``configuration``, with the attachment's and the member's SHA-256. It has no
acquisition record and no import declaration, so neither
`devtools.algebraic_witness_reports` ``derive-forms`` nor `devtools.upper_bound_reports`
reads it (review B2 of #813). This is the small reader the bead names, and the decision:

- **custody.** ``json.dumps(configuration)`` rebuilds the author's file byte for byte, so
  its SHA-256 must be the member digest the comment states, which the fact and the
  packet's ``acquisition/sources.json`` both record; the fact's archive digest must be the
  attachment's there. Nothing is read from a fact that fails (`load`);
- **the side.** ``S.poly`` must be T-244's polynomial, as the issue-804 intake's
  ``exact-sides.json`` holds it, and ``S``'s interval must meet that row's isolating
  interval; ``S.in_K`` must be a root of ``S.poly`` exactly in ``K`` and lie in ``S``'s
  interval (`side_check`);
- **route 1**, ``sqpack.witness.exact_verify`` over ``K``: the configuration is turned
  into a centre-basis Witness/v2 over ``K`` by
  `algebraic_witness_reports.evand_minpoly_geometry`,
  as T-193's forms were, and a positive, a duplicate-square and an outside-container job
  are decided, each in its own child process, by `algebraic_witness_reports.decide`, and
  validated by its ``validate_job``. An angle parameter ``u`` stated as the empty list is
  read as zero, as ``verify_exact.py`` reads it (squares 127 and 184 at 172), and the
  receipt names each square so read;
- **route 2**, the source's ``verify_exact.py`` (`V-evand-verify-exact`), run unchanged
  from its retained copy, held to its digest, on the rebuilt file in a ``python -I`` child
  process, and on four mutated controls (``CONTROLS``, the mutations of T-193's replay
  driver, ``evand-exact-cur-2026-10-16/review/replay_verify_exact.py``): a square moved
  1e-6 through a wall it touches, ``S`` in ``K`` raised by 1e-6, ``S``'s interval moved
  wholly below the root, and square 1 replaced by square 0. Each control must be refused;
- **identity**, ``poses``: each configuration's binary64 text, ``n side`` and ``x y
  degrees`` rows, for ``devtools.measure_identity``'s ``binary64-xyd`` input.

A finite configuration certifies an upper bound and nothing more. The receipts are
``receipts/algebraic-route1-nNNN.json.xz``, ``receipts/route2-verify-exact.json`` and
``receipts/side-check.json`` in the packet; ``check`` admits them again. From
``packing/``, with the project interpreter::

    python -m devtools.configuration_fact_replay custody
    python -m devtools.configuration_fact_replay side [--write]
    python -m devtools.configuration_fact_replay route1 --jobs-dir DIR [--n N ...] [--workers 2]
    python -m devtools.configuration_fact_replay route2 --scratch DIR [--workers 2]
    python -m devtools.configuration_fact_replay poses --out DIR
    python -m devtools.configuration_fact_replay check
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

import sympy
from strif import atomic_output_file

from devtools import algebraic_witness_reports as algebraic
from devtools import evand_arrangement_reports as kernel
from sqpack.field import NumberField
from sqpack.witness import validate_witness_document

MODULE = "devtools.configuration_fact_replay"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PACKET = ROOT / "resources/web/hyukdongkim-t244-configurations-2026-10-25"
SOURCES = PACKET / "acquisition/sources.json"
FACT_FORMAT = "issue-804-configuration-fact-v1"
COUNTS = (172, 263)
#: T-244's sides as the issue-804 intake decided them from #804's polynomials.
SIDES = ROOT / "campaign/issue-intake/upper-bounds-issue804-20261025/exact-sides.json"
SIDE_RECEIPT = PACKET / "receipts/side-check.json"
ROUTE2_RECEIPT = PACKET / "receipts/route2-verify-exact.json"
RECEIPT_FORMAT = "issue-804-configuration-route1-v1"
ROUTE2_FORMAT = "issue-804-configuration-route2-v1"
SIDE_FORMAT = "issue-804-configuration-side-v1"
WITNESS_PREFIX = "W-kim-t244-configuration-n"
SOURCE_KEY = "[Kim exact forms 2026-10-25]"
COMMENT = "https://github.com/jlevy/squares/issues/804#issuecomment-6395743853"
CLAIM_LIMITATIONS = (
    "Hyukdong Kim's exact configuration of T-174's packing at T-244's side, reported on "
    "issue 804 and kept as a derived fact; a finite configuration certifies an upper bound "
    "and nothing more."
)
CHECKER = (
    ROOT
    / "resources/web/evand-exact-and-local-reports-2026-10-12"
    / "source/search/exact/verify_exact.py"
)
CHECKER_SHA256 = "a0f38ca87c13c7e1b1d6ca99d69adea47df6008a645e3b4dbb79e8e0af35bab4"
CHECKER_UPSTREAM = (
    "evand/square-packing@7d1407a0b66c46e32cdbcbd5619586fe2bdd52a1 search/exact/verify_exact.py"
)
#: The four mutated controls of T-193's replay driver, each of which must be refused.
CONTROLS = ("moved-square", "enlarged-side", "side-below-root", "duplicate-square")
STEP = Fraction(1, 10**6)
#: Which coordinate a wall contact pins, and which way moving through the wall goes.
THROUGH = {"L": ("x", -1), "R": ("x", 1), "B": ("y", -1), "T": ("y", 1)}
#: The digits each side is enclosed to before it is compared with T-244's interval.
DIGITS = 120


class ReplayError(ValueError):
    """Refuse a fact out of custody, a side that is not T-244's, or a receipt that differs."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ReplayError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fact_path(n: int) -> Path:
    return PACKET / f"facts/n{n}.json.gz"


def receipt_path(n: int) -> Path:
    return PACKET / f"receipts/algebraic-route1-n{n:03d}.json.xz"


def certificate_bytes(fact: dict[str, Any]) -> bytes:
    """The author's file, rebuilt: the configuration as ``json.dumps`` writes it."""
    return json.dumps(fact["configuration"]).encode("utf-8")


def load(n: int) -> dict[str, Any]:
    """The fact at ``n``, refused unless it rebuilds the certificate the comment pins."""
    _require(n in COUNTS, f"n={n}: no configuration of this packet")
    fact = json.loads(gzip.decompress(fact_path(n).read_bytes()).decode("utf-8"))
    sources = json.loads(SOURCES.read_text(encoding="utf-8"))
    source = fact.get("source", {})
    _require(fact.get("format") == FACT_FORMAT, f"n={n}: not an issue-804 configuration fact")
    _require(
        source.get("archive_sha256") == sources["attachment"]["sha256"]
        and source.get("comment") == sources["comment"] == COMMENT,
        f"n={n}: the fact names another attachment than the packet's",
    )
    members = {row["path"]: row["sha256"] for row in sources["members"]}
    stated = source.get("member_sha256")
    _require(
        members.get(source.get("member")) == stated,
        f"n={n}: the member digest is not the one sources.json records",
    )
    _require(
        sha256(certificate_bytes(fact)) == stated,
        f"n={n}: the configuration does not rebuild the certificate the comment pins",
    )
    configuration = fact["configuration"]
    _require(
        configuration.get("n") == n and len(configuration.get("squares", [])) == n,
        f"n={n}: the configuration is not this count's",
    )
    return fact


def custody() -> list[dict[str, Any]]:
    rows = []
    for n in COUNTS:
        fact = load(n)
        rows.append(
            {
                "n": n,
                "member": fact["source"]["member"],
                "member_sha256": fact["source"]["member_sha256"],
                "rebuilt_bytes": len(certificate_bytes(fact)),
                "field_degree": len(fact["configuration"]["field"]["f"]) - 1,
            }
        )
    return rows


# ------------------------------------------------------------------------------ side


def _field(configuration: dict[str, Any]) -> NumberField:
    low_to_high = [Fraction(value) for value in configuration["field"]["f"]]
    low, high = (Fraction(value) for value in configuration["field"]["t_interval"])
    return NumberField(list(reversed(low_to_high)), (low, high))


def side_check() -> dict[str, Any]:
    """Each configuration's side is T-244's: the same polynomial, a root of it in ``K``
    whose enclosure lies in the configuration's interval, and one root only of that
    polynomial, counted exactly (SymPy's Sturm count), in the hull of the enclosure and
    T-244's isolating interval, so the two name the same real root."""
    sides = {row["n"]: row for row in json.loads(SIDES.read_text(encoding="utf-8"))["rows"]}
    rows = []
    for n in COUNTS:
        configuration = load(n)["configuration"]
        stated = configuration["S"]
        poly_low_to_high = [int(value) for value in stated["poly"]]
        t244 = sides[n]
        expected = [int(value) for value in t244["polynomial_high_to_low"]]
        same_polynomial = list(reversed(poly_low_to_high)) == expected
        field = _field(configuration)
        degree = len(configuration["field"]["f"]) - 1
        side = field.element([Fraction(value) for value in stated["in_K"]] or [Fraction(0)])
        value = field.zero
        for coefficient in reversed(poly_low_to_high):
            value = value * side + field.rational(Fraction(coefficient))
        root_in_k = value.is_zero()
        field.refine_to(DIGITS)
        low, high = field.enclose(side)
        stated_low, stated_high = (Fraction(item) for item in stated["interval"])
        t_low, t_high = (Fraction(item) for item in t244["interval"])
        polynomial = sympy.Poly(expected, sympy.Symbol("s"))
        hull = (min(low, t_low), max(high, t_high))
        roots_in_hull = int(
            polynomial.count_roots(sympy.Rational(hull[0]), sympy.Rational(hull[1]))
        )
        rows.append(
            {
                "n": n,
                "field_degree": degree,
                "side_degree": len(poly_low_to_high) - 1,
                "same_polynomial_as_t244": same_polynomial,
                "root_of_polynomial_in_K": root_in_k,
                "enclosure_digits": DIGITS,
                "enclosure_in_stated_interval": stated_low <= low and high <= stated_high,
                "t244_interval_width": f"{float(t_high - t_low):.3e}",
                "roots_in_hull_of_enclosure_and_t244_interval": roots_in_hull,
                "decimal": field.decimal(side, 40),
            }
        )
    return {
        "format": SIDE_FORMAT,
        "tool": f"packing/devtools/{Path(__file__).name}",
        "sides": SIDES.relative_to(REPO).as_posix(),
        "rows": rows,
        "agrees": all(
            row["same_polynomial_as_t244"]
            and row["root_of_polynomial_in_K"]
            and row["enclosure_in_stated_interval"]
            and row["roots_in_hull_of_enclosure_and_t244_interval"] == 1
            for row in rows
        ),
    }


# ---------------------------------------------------------------------------- route 1


def zero_parameters(configuration: dict[str, Any]) -> list[int]:
    """The squares, by index from 0, whose angle parameter is stated as the empty list."""
    return [index for index, square in enumerate(configuration["squares"]) if square["u"] == []]


def witness(n: int) -> dict[str, Any]:
    """The configuration as a centre-basis Witness/v2 over ``K``, held to the schema."""
    fact = load(n)
    configuration = copy.deepcopy(fact["configuration"])
    for index in zero_parameters(configuration):
        configuration["squares"][index]["u"] = ["0"]
    degree = len(configuration["field"]["f"]) - 1
    row = cast(
        "algebraic.Witness",
        {"n": n, "path": fact["source"]["member"], "fact": "", "degree": degree},
    )
    raw = gzip.compress(json.dumps(configuration).encode("utf-8"), mtime=0)
    geometry = algebraic.evand_minpoly_geometry(raw, row)
    document = {
        "softschema": {
            "contract": "packing.squares:Witness/v2",
            "schema": "witness.schema.yaml",
            "envelope": "witness",
            "status": "enforced",
        },
        "witness": {
            "id": f"{WITNESS_PREFIX}{n:03d}",
            "n": n,
            "side": geometry["side"],
            "square_size": "1",
            "representation": geometry["representation"],
            "scalar": geometry["scalar"],
            "coordinates": {
                "origin": "lower-left",
                "axes": "x-right-y-up",
                "angle_unit": "not-applicable",
            },
            "squares": geometry["squares"],
            "claim": {
                "coordinate_provenance": "reported",
                "method": "exact-algebraic",
                "limitations": CLAIM_LIMITATIONS,
            },
            "source": {
                "key": SOURCE_KEY,
                "path": fact_path(n).relative_to(REPO).as_posix(),
                "url": fact["source"]["attachment"],
                "retrieved": "2026-10-25",
                "revision": fact["source"]["member"],
                "revision_sha256": fact["source"]["member_sha256"],
            },
        },
    }
    try:
        return validate_witness_document(
            document, path=algebraic.WITNESS_SCHEMA, fallback_schema=algebraic.WITNESS_SCHEMA
        )
    except ValueError as error:
        raise ReplayError(f"n={n}: not a valid witness: {error}") from error


def decide_job(n: int, control: str, output: Path) -> None:
    _require(not output.exists(), "refusing to overwrite a deciding job")
    built = witness(n)
    row = algebraic.decide(built, control)
    algebraic.validate_job(row, built, control)
    output.write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")


def run_job(n: int, control: str, directory: Path) -> dict[str, Any]:
    """One job in its own child process, resumed from ``directory`` where it finished."""
    output = directory / f"n{n}-{control}.json"
    if output.exists():
        return json.loads(output.read_text(encoding="utf-8"))
    command = [sys.executable, "-m", MODULE, "decide-job", "--n", str(n), "--control", control]
    command += ["--output", str(output)]
    completed = subprocess.run(command, capture_output=True, check=False)
    output.with_suffix(".stdout.log").write_bytes(completed.stdout)
    output.with_suffix(".stderr.log").write_bytes(completed.stderr)
    _require(completed.returncode == 0, f"n={n} {control}: child exited {completed.returncode}")
    return json.loads(output.read_text(encoding="utf-8"))


def route1(directory: Path, numbers: list[int], workers: int) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    tasks = [(n, control) for n in numbers for control in kernel.JOBS]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(lambda task: run_job(task[0], task[1], directory), tasks))
    done = dict(zip(tasks, results, strict=True))
    for n in numbers:
        built = witness(n)
        side = algebraic.side_of(built)
        rows = [done[(n, control)] for control in kernel.JOBS]
        for row, control in zip(rows, kernel.JOBS, strict=True):
            algebraic.validate_job(row, built, control, side=side)
        kernel.save_xz(
            receipt_path(n),
            {
                "format": RECEIPT_FORMAT,
                "routes": [algebraic.ROUTE],
                "zero_angle_parameters": zero_parameters(load(n)["configuration"]),
                "cases": rows,
            },
        )


def check_route1(n: int, *, replay: bool = False) -> dict[str, Any]:
    built = witness(n)
    side = algebraic.side_of(built)
    record = kernel.read_xz(receipt_path(n))
    _require(
        record.get("format") == RECEIPT_FORMAT
        and record.get("routes") == [algebraic.ROUTE]
        and record.get("zero_angle_parameters") == zero_parameters(load(n)["configuration"])
        and len(record.get("cases", [])) == len(kernel.JOBS),
        f"n={n}: not this packet's route-1 receipt",
    )
    for row, control in zip(record["cases"], kernel.JOBS, strict=True):
        algebraic.validate_job(row, built, control, side=side)
        if replay:
            again = algebraic.decide(built, control)
            _require(again[algebraic.ROUTE] == row[algebraic.ROUTE], f"n={n}: replay differs")
    return record


# ---------------------------------------------------------------------------- route 2


def _statement(line: str) -> str:
    """The part of a checker's line after the file name, which names no path."""
    return line.split(": ", 1)[1] if ": " in line else line


def run_checker(path: Path) -> dict[str, Any]:
    command = [sys.executable, "-I", str(CHECKER), str(path)]
    started = time.monotonic()
    child = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    assert child.stdout is not None
    output = child.stdout.read()
    child.stdout.close()
    _, status, usage = os.wait4(child.pid, 0)
    exit_code = os.waitstatus_to_exitcode(status)
    lines = output.strip().splitlines()
    return {
        "command": ["python", "-I", "verify_exact.py", path.name],
        "exit": exit_code,
        "last_line": _statement(lines[-1]) if lines else "",
        "wall_seconds": round(time.monotonic() - started, 2),
        "cpu_seconds": round(usage.ru_utime + usage.ru_stime, 2),
    }


def wall_contact(data: dict[str, Any]) -> tuple[int, str]:
    """A square the configuration puts against a wall, and that wall.

    Evan Daniel's forms list their contacts (``equations``) and T-193's driver takes the
    first wall row; these configurations list none. An axis-aligned square (``u`` zero)
    whose centre coordinate is exactly 1/2 touches the left or bottom wall, exactly.
    """
    if "equations" in data:
        contact = next(item for item in data["equations"] if item[0] == "W")
        return int(contact[1]), str(contact[3])
    for index, square in enumerate(data["squares"]):
        if any(Fraction(value) != 0 for value in square["u"]):
            continue
        for coordinate, wall in (("x", "L"), ("y", "B")):
            values = [Fraction(value) for value in square[coordinate]]
            if values[:1] == [Fraction(1, 2)] and not any(values[1:]):
                return index, wall
    raise ReplayError("no axis-aligned square touches the left or bottom wall")


def mutate(data: dict[str, Any], kind: str) -> tuple[dict[str, Any], str]:
    """T-193's replay driver's mutation of one kind, applied to a copy of ``data``."""
    mutated = copy.deepcopy(data)
    if kind == "moved-square":
        square, wall = wall_contact(mutated)
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
        mutated["squares"][1] = copy.deepcopy(mutated["squares"][0])
        return mutated, "square 1 replaced by square 0"
    raise ReplayError(f"unknown control {kind}")


def route2_job(n: int, kind: str | None, scratch: Path) -> dict[str, Any]:
    fact = load(n)
    data = fact["configuration"]
    what = "the author's file, rebuilt byte for byte"
    if kind is not None:
        data, what = mutate(data, kind)
    target = scratch / f"n{n}.{kind or 'positive'}.minpoly.json"
    target.write_bytes(json.dumps(data).encode("utf-8"))
    try:
        record = run_checker(target)
    finally:
        target.unlink()
    record["control"] = kind or "positive"
    record["input"] = what
    if kind is None:
        record["input_sha256"] = fact["source"]["member_sha256"]
        record["valid"] = record["exit"] == 0 and record["last_line"].startswith("VALID")
    else:
        record["refused"] = record["exit"] == 1 and "NOT VERIFIED" in record["last_line"]
    return record


def route2(scratch: Path, workers: int) -> dict[str, Any]:
    _require(
        sha256(CHECKER.read_bytes()) == CHECKER_SHA256, "verify_exact.py is not the copy read"
    )
    scratch.mkdir(parents=True, exist_ok=True)
    tasks: list[tuple[int, str | None]] = [
        (n, kind) for n in COUNTS for kind in (None, *CONTROLS)
    ]
    started = datetime.now(UTC)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        records = list(pool.map(lambda task: route2_job(task[0], task[1], scratch), tasks))
    rows = []
    for n in COUNTS:
        mine = [record for (m, _), record in zip(tasks, records, strict=True) if m == n]
        rows.append({"n": n, "positive": mine[0], "controls": mine[1:]})
    receipt = {
        "format": ROUTE2_FORMAT,
        "bead": "think-4rzl",
        "issue": "https://github.com/jlevy/squares/issues/804",
        "ran_at_utc": started.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "program": {
            "path": CHECKER.relative_to(REPO).as_posix(),
            "sha256": CHECKER_SHA256,
            "upstream": CHECKER_UPSTREAM,
            "read_before_running": True,
            "relationship_to_generator": "shared-components",
            "where": (
                "run unchanged from the retained copy, each file in its own python -I child"
            ),
        },
        "driver": {
            "path": f"packing/devtools/{Path(__file__).name}",
            "sha256": sha256(Path(__file__).read_bytes()),
        },
        "environment": {"python": f"CPython {platform.python_version()}", "workers": workers},
        "cpu_seconds_of_runs": round(sum(record["cpu_seconds"] for record in records), 2),
        "rows": rows,
        "summary": {
            "positives_valid": sum(1 for row in rows if row["positive"]["valid"]),
            "controls_refused": sum(1 for row in rows for c in row["controls"] if c["refused"]),
            "controls": sum(len(row["controls"]) for row in rows),
        },
    }
    with atomic_output_file(ROUTE2_RECEIPT) as temporary:
        temporary.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    return receipt["summary"]


def check_route2() -> dict[str, Any]:
    receipt = json.loads(ROUTE2_RECEIPT.read_text(encoding="utf-8"))
    _require(receipt.get("format") == ROUTE2_FORMAT, "not this packet's route-2 receipt")
    _require(receipt["program"]["sha256"] == CHECKER_SHA256, "the receipt ran another checker")
    _require(
        [row["n"] for row in receipt["rows"]] == list(COUNTS), "the receipt's counts differ"
    )
    for row in receipt["rows"]:
        n = row["n"]
        positive = row["positive"]
        _require(
            positive["valid"]
            and positive["input_sha256"] == load(n)["source"]["member_sha256"],
            f"n={n}: route 2 did not accept the author's file",
        )
        _require(
            [c["control"] for c in row["controls"]] == list(CONTROLS)
            and all(c["refused"] for c in row["controls"]),
            f"n={n}: a route-2 control was not refused",
        )
    return receipt["summary"]


# ----------------------------------------------------------------------------- poses


def poses(directory: Path) -> list[Path]:
    """Each configuration in binary64, ``n side`` then ``x y degrees`` rows, for
    ``devtools.measure_identity``'s ``binary64-xyd`` input. A measurement, not a decision."""
    directory.mkdir(parents=True, exist_ok=True)
    written = []
    for n in COUNTS:
        configuration = load(n)["configuration"]
        field = _field(configuration)
        field.refine_to(40)

        def value(coefficients: list[str], field: NumberField = field) -> float:
            element = field.element([Fraction(item) for item in coefficients] or [Fraction(0)])
            return float(element)

        lines = [f"{n} {value(configuration['S']['in_K'])!r}"]
        for square in configuration["squares"]:
            u = value(square["u"])
            degrees = math.degrees(2 * math.atan(u)) + 90 * square["m"]
            lines.append(f"{value(square['x'])!r} {value(square['y'])!r} {degrees!r}")
        target = directory / f"kim-t244-n{n}.xyd.txt"
        target.write_text("\n".join(lines) + "\n", encoding="utf-8")
        written.append(target)
    return written


# --------------------------------------------------------------------------- command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("custody")
    sides = sub.add_parser("side")
    sides.add_argument("--write", action="store_true")
    first = sub.add_parser("route1")
    first.add_argument("--jobs-dir", type=Path, required=True)
    first.add_argument("--n", type=int, nargs="+", default=list(COUNTS))
    first.add_argument("--workers", type=int, default=2)
    second = sub.add_parser("route2")
    second.add_argument("--scratch", type=Path, required=True)
    second.add_argument("--workers", type=int, default=2)
    pose = sub.add_parser("poses")
    pose.add_argument("--out", type=Path, required=True)
    checking = sub.add_parser("check")
    checking.add_argument("--replay", action="store_true")
    job = sub.add_parser("decide-job")
    job.add_argument("--n", type=int, required=True)
    job.add_argument("--control", choices=kernel.JOBS, required=True)
    job.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.action == "custody":
            print(json.dumps(custody(), indent=1))
        elif args.action == "side":
            record = side_check()
            if args.write:
                SIDE_RECEIPT.parent.mkdir(exist_ok=True)
                with atomic_output_file(SIDE_RECEIPT) as temporary:
                    temporary.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
            else:
                stored = json.loads(SIDE_RECEIPT.read_text(encoding="utf-8"))
                _require(stored == record, "the side receipt is not what the facts derive")
            print(json.dumps(record, indent=1))
            _require(record["agrees"], "a configuration's side is not T-244's")
        elif args.action == "route1":
            route1(args.jobs_dir, args.n, args.workers)
            print(json.dumps({n: check_route1(n)["cases"][0]["cpu_seconds"] for n in args.n}))
        elif args.action == "route2":
            print(json.dumps(route2(args.scratch, args.workers)))
        elif args.action == "poses":
            for path in poses(args.out):
                print(path)
        elif args.action == "check":
            for n in COUNTS:
                check_route1(n, replay=args.replay)
            stored = json.loads(SIDE_RECEIPT.read_text(encoding="utf-8"))
            _require(stored == side_check() and stored["agrees"], "the side receipt differs")
            print(json.dumps({"route1": list(COUNTS), "route2": check_route2()}))
        else:
            decide_job(args.n, args.control, args.output)
    except (ReplayError, algebraic.ReportError, OSError, KeyError, ValueError) as error:
        print(f"{MODULE}: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
