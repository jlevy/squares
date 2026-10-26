"""Decide exact configurations a packet keeps as ``minpoly.json`` content facts, two routes.

Hyukdong Kim's exact configurations for T-244 (issue 804, 172 and 263) are kept by the
``hyukdongkim-t244-configurations-2026-10-25`` packet as derived facts in the format
``issue-804-configuration-fact-v1``: each certificate's content, in the ``minpoly.json``
format of Evan Daniel's ``verify_exact.py``, read as JSON data and kept under
``configuration``, with the attachment's and the member's digests. The packet has no
algebraic declaration and keeps no upstream byte, so
`devtools.algebraic_witness_reports`' ``derive-forms`` cannot read it (review B2 of #813).
This module is that reader, and it decides each configuration on both exact routes. It
decides nothing by itself: ``sqpack.witness.exact_verify`` and ``verify_exact.py`` do.

From ``packing/``, with the project interpreter::

    python -m devtools.minpoly_configuration_facts PACKET check
    python -m devtools.minpoly_configuration_facts PACKET side --ledger LEDGER [--write]
    python -m devtools.minpoly_configuration_facts PACKET certify --jobs-dir DIR [--n N ...]
    python -m devtools.minpoly_configuration_facts PACKET replay --scratch DIR [--n N ...]
    python -m devtools.minpoly_configuration_facts PACKET measure --against SPEC [--write]
    python -m devtools.minpoly_configuration_facts PACKET admit

- ``check``, custody: each fact is held to the packet's ``acquisition/sources.json``, its
  archive's SHA-256 and its member's, and its ``configuration`` serialized as
  ``json.dumps`` writes it must have the member's SHA-256, the digest the author's
  comment states. So the content is the author's certificate byte for byte, and route 2
  runs on the author's own bytes, rebuilt.
- ``side``: each ``S`` in ``K`` is the side the ledger (an ``exact-sides.json``) holds at
  its count: the fact's ``p`` is the ledger's polynomial, ``p(S) = 0`` in ``K``, and the
  enclosure of ``S(t*)`` lies in the ledger's interval, in which `sqpack.field` finds
  exactly one root of ``p``. Writes ``receipts/side.json``.
- ``certify``, route 1: `sqpack.witness.exact_verify` over ``K`` on the witness that
  `algebraic_witness_reports.evand_minpoly_geometry` builds from the configuration, a
  positive and the duplicate-square and outside-container controls, each job in its own
  child process (`algebraic_witness_reports.decide`, validated by its `validate_job`).
  Writes ``receipts/exact-verify-nNNN.json``.
- ``replay``, route 2: the retained ``verify_exact.py`` (`CHECKER`, read before it was
  run, and refused unless its SHA-256 is `CHECKER_SHA256`) run unchanged in a
  ``python -I`` child on the rebuilt certificate, which must print ``VALID.``, and on
  four mutated controls in the manner of T-193's replay driver, which must print ``NOT
  VERIFIED``. Writes ``receipts/verify-exact-replay.json``.
- ``measure``: each configuration against another packing of its count, by
  `devtools.measure_identity`, through a rational shadow of the configuration at
  `SHADOW_PLACES` places. A measurement for credit; it decides nothing. Writes
  ``measure/identity-nNNN.json``.
- ``admit``: every receipt above, held to the facts again without deciding anything.

An empty coefficient list is the field's zero, as ``verify_exact.py`` reads it; the
geometry reader takes it so (`algebraic_witness_reports._coefficients`).
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
import time
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

from devtools import algebraic_witness_reports as algebraic
from devtools import upper_bound_reports as reports
from sqpack.field import FieldElement, NumberField
from sqpack.witness import witness_envelope

MODULE = "devtools.minpoly_configuration_facts"
REPO = reports.REPO
FACT_FORMAT = "issue-804-configuration-fact-v1"
SOURCES = Path("acquisition/sources.json")
CHECKER = (
    REPO
    / "packing/resources/web/evand-exact-and-local-reports-2026-10-12/source/search/exact"
    / "verify_exact.py"
)
CHECKER_SHA256 = "a0f38ca87c13c7e1b1d6ca99d69adea47df6008a645e3b4dbb79e8e0af35bab4"
JOBS = algebraic.JOBS
ROUTE = algebraic.ROUTE
#: The controls route 2 runs, each refused by ``verify_exact.py`` on its own line.
CONTROLS = ("moved-square", "enlarged-side", "side-below-root", "duplicate-square")
STEP = Fraction(1, 10**6)
#: The places a rational shadow keeps, far below any displacement it measures.
SHADOW_PLACES = 40
#: The digits ``S(t*)`` is enclosed to before it is placed in the ledger's interval.
SIDE_DIGITS = 200
RECEIPT_FORMAT = "minpoly-configuration-route-v1"
SOURCE_KEY = "[Kim exact forms 2026-10-25]"
LIMITATIONS = (
    "The author's exact configuration, read from the packet's derived fact; verified here "
    "for feasibility at its side only. No lower bound, optimum or local minimality."
)


class FactError(ValueError):
    """Refuse a fact whose custody, form or receipt does not hold."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise FactError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# --------------------------------------------------------------------------- custody


def fact_paths(packet: Path) -> dict[int, Path]:
    """The packet's facts, ``facts/nNNN.json.gz``, by count."""
    paths = {}
    for path in sorted((packet / "facts").glob("n*.json.gz")):
        count = path.name.removeprefix("n").removesuffix(".json.gz")
        _require(count.isdigit(), f"{path.name}: not a count's fact")
        paths[int(count)] = path
    _require(paths, f"{packet.name}: no facts")
    return paths


def certificate_bytes(configuration: dict[str, Any]) -> bytes:
    """The certificate rebuilt from the fact's content, as ``json.dumps`` writes it."""
    return json.dumps(configuration).encode("utf-8")


def read_fact(packet: Path, n: int) -> dict[str, Any]:
    """One fact, refused unless it is the packet's, this count's and the author's bytes."""
    path = fact_paths(packet).get(n)
    _require(path is not None, f"n={n}: the packet keeps no fact at this count")
    assert path is not None
    sources = json.loads((packet / SOURCES).read_text(encoding="utf-8"))
    loaded: object = json.loads(gzip.decompress(path.read_bytes()))
    _require(type(loaded) is dict, f"n={n}: not a fact")
    fact = cast("dict[str, Any]", loaded)
    _require(fact.get("format") == FACT_FORMAT, f"n={n}: not a fact")
    source = fact["source"]
    members = {member["path"]: member["sha256"] for member in sources["members"]}
    _require(
        source["archive_sha256"] == sources["attachment"]["sha256"]
        and source["attachment"] == sources["attachment"]["url"]
        and members.get(source["member"]) == source["member_sha256"],
        f"n={n}: the fact's source is not the packet's attachment and member",
    )
    configuration = fact["configuration"]
    _require(
        sha256(certificate_bytes(configuration)) == source["member_sha256"],
        f"n={n}: the content does not rebuild the member's bytes",
    )
    squares = configuration["squares"]
    degree = len(configuration["field"]["f"]) - 1
    _require(
        configuration["n"] == n == fact["squares"] == len(squares)
        and fact["field_degree"] == degree,
        f"n={n}: the fact's count or degree is not its configuration's",
    )
    return fact


def check(packet: Path) -> dict[int, dict[str, Any]]:
    """Custody of every fact: what ``check`` prints."""
    rows = {}
    for n in fact_paths(packet):
        fact = read_fact(packet, n)
        rows[n] = {
            "member": fact["source"]["member"],
            "member_sha256": fact["source"]["member_sha256"],
            "certificate_bytes": len(certificate_bytes(fact["configuration"])),
            "field_degree": fact["field_degree"],
        }
    return rows


# --------------------------------------------------------------------------- the witness


def witness(packet: Path, n: int) -> dict[str, Any]:
    """The configuration as a centre-basis Witness/v2 over ``K``, held to the schema."""
    fact = read_fact(packet, n)
    configuration = fact["configuration"]
    degree = fact["field_degree"]
    geometry = algebraic.evand_minpoly_geometry(
        gzip.compress(certificate_bytes(configuration), mtime=0),
        cast("algebraic.Witness", {"n": n, "degree": degree}),
    )
    stated = {
        "id": f"W-kim-804-n{n:03d}",
        "n": n,
        "side": geometry["side"],
        "square_size": "1",
        "representation": geometry["representation"],
        "scalar": geometry["scalar"],
        "coordinates": dict(reports.CORNER_FRAME),
        "squares": geometry["squares"],
        "claim": {
            "coordinate_provenance": "reported",
            "method": "exact-algebraic",
            "limitations": LIMITATIONS,
        },
        "source": {
            "key": SOURCE_KEY,
            "path": fact_paths(packet)[n].relative_to(REPO).as_posix(),
            "url": fact["source"]["comment"],
            "retrieved": "2026-10-25",
            "revision_sha256": fact["source"]["member_sha256"],
        },
    }
    return algebraic._validated(witness_envelope(stated), n)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]


def field_of(configuration: dict[str, Any]) -> NumberField:
    low_to_high = [int(value) for value in configuration["field"]["f"]]
    interval = [Fraction(value) for value in configuration["field"]["t_interval"]]
    return NumberField(list(reversed(low_to_high)), (interval[0], interval[1]))


def element(field: NumberField, coefficients: list[str]) -> FieldElement:
    return field.element([Fraction(value) for value in coefficients] or [Fraction(0)])


# --------------------------------------------------------------------------- the side


def side(packet: Path, ledger: Path) -> dict[str, Any]:
    """Each ``S`` in ``K`` is the ledger's side at its count, decided exactly."""
    record = json.loads(ledger.read_text(encoding="utf-8"))
    ledger_rows = {row["n"]: row for row in record["rows"]}
    rows = []
    for n in fact_paths(packet):
        configuration = read_fact(packet, n)["configuration"]
        row = ledger_rows.get(n)
        _require(row is not None, f"n={n}: the ledger holds no side at this count")
        assert row is not None
        high = [int(value) for value in row["polynomial_high_to_low"]]
        stated = [int(value) for value in configuration["S"]["poly"]]
        _require(list(reversed(stated)) == high, f"n={n}: p is not the ledger's polynomial")
        low, high_end = (Fraction(value) for value in row["interval"])
        # The ledger's interval isolates one root of p: NumberField refuses otherwise.
        NumberField(high, (low, high_end))
        field = field_of(configuration)
        value = element(field, configuration["S"]["in_K"])
        total = field.zero
        for coefficient in high:
            total = total * value + coefficient
        _require(total.is_zero(), f"n={n}: p(S) is not zero in K")
        field.refine_to(SIDE_DIGITS)
        enclosed = field.enclose(value)
        _require(low < enclosed[0] and enclosed[1] < high_end, f"n={n}: S(t*) is not there")
        stated_interval = [Fraction(item) for item in configuration["S"]["interval"]]
        rows.append(
            {
                "n": n,
                "polynomial_degree": len(high) - 1,
                "field_degree": len(configuration["field"]["f"]) - 1,
                "p_is_the_ledgers": True,
                "p_of_S_is_zero_in_K": True,
                "ledger_interval_root_count": 1,
                "S_enclosure_within_ledger_interval": True,
                "S_enclosure_digits": SIDE_DIGITS,
                "fact_interval_holds_S": stated_interval[0] <= enclosed[0]
                and enclosed[1] <= stated_interval[1],
                "side_decimal": field.decimal(value, 100),
            }
        )
    return {
        "format": "minpoly-configuration-side-v1",
        "ledger": ledger.resolve().relative_to(REPO).as_posix(),
        "ledger_sha256": sha256(ledger.read_bytes()),
        "method": (
            "p equal to the ledger's polynomial; p(S) = 0 in K = Q[t]/f by exact arithmetic "
            "(sqpack.field); S(t*) enclosed by sqpack.field inside the ledger's interval, "
            "where a Sturm count finds exactly one root of p"
        ),
        "rows": rows,
    }


# --------------------------------------------------------------------------- route 1


def receipt_path(packet: Path, n: int) -> Path:
    return packet / f"receipts/exact-verify-n{n:03d}.json"


def decide_job(packet: Path, n: int, control: str, output: Path) -> None:
    _require(control in JOBS, "unknown job")
    _require(not output.exists(), "refusing to overwrite a deciding job")
    stated = witness(packet, n)
    row = algebraic.decide(stated, control)
    algebraic.validate_job(row, stated, control)
    output.write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")


def run_job(packet: Path, n: int, control: str, directory: Path) -> dict[str, Any]:
    """One job in its own child process; an interrupted run resumes from ``directory``."""
    output = directory / f"n{n}-{control}.json"
    if output.exists():
        return json.loads(output.read_text(encoding="utf-8"))
    command = [sys.executable, "-m", MODULE, packet.name, "decide-job"]
    command += ["--n", str(n), "--control", control, "--output", str(output)]
    completed = subprocess.run(command, capture_output=True, check=False)
    output.with_suffix(".stderr.log").write_bytes(completed.stderr)
    _require(completed.returncode == 0, f"n={n} {control}: child exited {completed.returncode}")
    return json.loads(output.read_text(encoding="utf-8"))


def certify(packet: Path, directory: Path, numbers: list[int] | None = None) -> None:
    """Decide each count's three jobs, one at a time, and write its receipt."""
    directory.mkdir(parents=True, exist_ok=True)
    for n in numbers or list(fact_paths(packet)):
        stated = witness(packet, n)
        rows = [run_job(packet, n, control, directory) for control in JOBS]
        for row, control in zip(rows, JOBS, strict=True):
            algebraic.validate_job(row, stated, control)
        target = receipt_path(packet, n)
        target.parent.mkdir(exist_ok=True)
        receipt = {
            "format": RECEIPT_FORMAT,
            "route": ROUTE,
            "n": n,
            "fact_member_sha256": read_fact(packet, n)["source"]["member_sha256"],
            "witness_id": stated["id"],
            "cases": rows,
        }
        target.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")


def admit_route1(packet: Path, n: int) -> dict[str, Any]:
    """A count's route 1 receipt, held to its fact and to each job's required outcome."""
    record = json.loads(receipt_path(packet, n).read_text(encoding="utf-8"))
    stated = witness(packet, n)
    _require(
        record.get("format") == RECEIPT_FORMAT
        and record.get("route") == ROUTE
        and record.get("n") == n
        and record.get("witness_id") == stated["id"]
        and record.get("fact_member_sha256") == read_fact(packet, n)["source"]["member_sha256"]
        and len(record.get("cases", [])) == len(JOBS),
        f"n={n}: not this fact's route 1 receipt",
    )
    for row, control in zip(record["cases"], JOBS, strict=True):
        algebraic.validate_job(row, stated, control)
    return record


# --------------------------------------------------------------------------- route 2


def checker_digest() -> str:
    return sha256(CHECKER.read_bytes())


def wall_contact(configuration: dict[str, Any]) -> tuple[int, str, int]:
    """The first axis-parallel square whose centre is 1/2 from the left or bottom wall,
    with the coordinate that pins it and the way through that wall."""
    for index, square in enumerate(configuration["squares"]):
        if any(Fraction(value) for value in square["u"]):
            continue
        for key in ("x", "y"):
            values = [Fraction(value) for value in square[key]]
            if values[:1] == [Fraction(1, 2)] and not any(values[1:]):
                return index, key, -1
    raise FactError("no axis-parallel square touches the left or bottom wall")


def mutate(configuration: dict[str, Any], kind: str) -> tuple[dict[str, Any], str]:
    """A control: the certificate changed so that ``verify_exact.py`` must refuse it."""
    mutated = copy.deepcopy(configuration)
    if kind == "moved-square":
        index, key, way = wall_contact(mutated)
        values = mutated["squares"][index][key]
        values[0] = str(Fraction(values[0]) + way * STEP)
        wall = "left" if key == "x" else "bottom"
        return mutated, f"square {index} moved 1e-6 through the {wall} wall it touches"
    if kind == "enlarged-side":
        values = mutated["S"]["in_K"]
        values[0] = str(Fraction(values[0]) + STEP)
        return mutated, "S in K raised by 1e-6, so p(S) is not 0 mod f"
    if kind == "side-below-root":
        low, high = (Fraction(value) for value in mutated["S"]["interval"])
        width = max(high - low, Fraction(1, 10**60))
        mutated["S"]["interval"] = [str(low - 3 * width), str(low - 2 * width)]
        return mutated, "S's interval replaced by one wholly below the author's"
    if kind == "duplicate-square":
        mutated["squares"][1] = copy.deepcopy(mutated["squares"][0])
        return mutated, "square 1 replaced by square 0"
    raise FactError(f"unknown control {kind}")


def run_checker(path: Path) -> dict[str, Any]:
    """``verify_exact.py`` on one file in a ``python -I`` child, with its own CPU time."""
    command = [sys.executable, "-I", str(CHECKER), str(path)]
    started = time.monotonic()
    child = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    assert child.stdout is not None
    output = child.stdout.read()
    child.stdout.close()
    _, status, usage = os.wait4(child.pid, 0)
    lines = output.strip().splitlines()
    last = lines[-1] if lines else ""
    return {
        "command": ["python", "-I", "verify_exact.py", path.name],
        "exit": os.waitstatus_to_exitcode(status),
        "last_line": last.split(": ", 1)[1] if ": " in last else last,
        "wall_seconds": round(time.monotonic() - started, 2),
        "cpu_seconds": round(usage.ru_utime + usage.ru_stime, 2),
    }


def replay(packet: Path, scratch: Path, numbers: list[int] | None = None) -> dict[str, Any]:
    """Route 2 on every count: the positive and the four controls, one child at a time."""
    _require(checker_digest() == CHECKER_SHA256, f"{CHECKER} is not the checker that was read")
    scratch.mkdir(parents=True, exist_ok=True)
    started = datetime.now(UTC)
    rows = []
    for n in numbers or list(fact_paths(packet)):
        fact = read_fact(packet, n)
        configuration = fact["configuration"]
        name = Path(fact["source"]["member"]).name
        target = scratch / name
        target.write_bytes(certificate_bytes(configuration))
        try:
            positive = run_checker(target)
        finally:
            target.unlink()
        controls = []
        for kind in CONTROLS:
            mutated, what = mutate(configuration, kind)
            target = scratch / f"n{n}.{kind}.minpoly.json"
            target.write_text(json.dumps(mutated), encoding="utf-8")
            try:
                record = run_checker(target)
            finally:
                target.unlink()
            record["control"] = kind
            record["mutation"] = what
            record["refused"] = record["exit"] == 1 and "NOT VERIFIED" in record["last_line"]
            controls.append(record)
        rows.append(
            {
                "n": n,
                "file": name,
                "sha256": fact["source"]["member_sha256"],
                "bytes": len(certificate_bytes(configuration)),
                "where": (
                    "rebuilt from the packet's fact, the author's certificate byte for byte"
                ),
                "positive": positive,
                "controls": controls,
            }
        )
        print(n, positive["exit"], positive["last_line"][:60], [c["refused"] for c in controls])
    receipt = {
        "format": "minpoly-configuration-verify-exact-replay-v1",
        "ran_at_utc": started.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cpu_seconds_of_runs": round(
            sum(row["positive"]["cpu_seconds"] for row in rows)
            + sum(control["cpu_seconds"] for row in rows for control in row["controls"]),
            1,
        ),
        "program": {
            "path": CHECKER.relative_to(REPO).as_posix(),
            "sha256": CHECKER_SHA256,
            "upstream": (
                "evand/square-packing@7d1407a0b66c46e32cdbcbd5619586fe2bdd52a1 "
                "search/exact/verify_exact.py"
            ),
            "read_before_running": True,
            "where": (
                "run unchanged from the retained copy, each file in its own python -I child"
            ),
        },
        "driver": {"module": MODULE},
        "environment": {
            "python": f"{platform.python_implementation()} {platform.python_version()}",
            "host": f"{os.cpu_count()} CPUs, shared",
        },
        "rows": rows,
    }
    target = packet / "receipts/verify-exact-replay.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    return receipt


def admit_route2(packet: Path) -> dict[str, Any]:
    """The route 2 receipt, held to the facts, the checker and the required outcomes."""
    record = json.loads((packet / "receipts/verify-exact-replay.json").read_text("utf-8"))
    _require(record["program"]["sha256"] == CHECKER_SHA256, "another checker ran")
    _require(
        {row["n"] for row in record["rows"]} == set(fact_paths(packet)),
        "the replay does not cover every fact",
    )
    for row in record["rows"]:
        n = row["n"]
        fact = read_fact(packet, n)
        _require(row["sha256"] == fact["source"]["member_sha256"], f"n={n}: another file")
        _require(
            row["positive"]["exit"] == 0 and row["positive"]["last_line"].startswith("VALID."),
            f"n={n}: the positive did not pass",
        )
        _require(
            [control["control"] for control in row["controls"]] == list(CONTROLS)
            and all(control["refused"] for control in row["controls"]),
            f"n={n}: a control was not refused",
        )
        for control in row["controls"]:
            _, what = mutate(fact["configuration"], control["control"])
            _require(control["mutation"] == what, f"n={n}: another mutation")
    return record


# --------------------------------------------------------------------------- identity


def _rational(value: FieldElement, places: int) -> Fraction:
    low, high = value.field.enclose(value)
    return Fraction(round((low + high) / 2 * 10**places), 10**places)


def shadow(configuration: dict[str, Any], places: int = SHADOW_PLACES) -> dict[str, Any]:
    """A rational centre-basis copy of the configuration, every number within
    ``10^-places`` of the exact one, each basis a rotation exactly."""
    field = field_of(configuration)
    field.refine_to(places + 20)
    squares = []
    for square in configuration["squares"]:
        u = _rational(element(field, square["u"]), places)
        cosine, sine = (1 - u * u) / (1 + u * u), 2 * u / (1 + u * u)
        for _turn in range(square["m"] % 4):
            cosine, sine = -sine, cosine
        squares.append(
            {
                "center": [str(_rational(element(field, square[key]), places)) for key in "xy"],
                "basis": [str(cosine), str(sine)],
            }
        )
    side_value = _rational(element(field, configuration["S"]["in_K"]), places)
    return {"n": configuration["n"], "side": str(side_value), "squares": squares}


def measure(packet: Path, against: str) -> dict[int, dict[str, Any]]:
    """Each configuration measured against ``against`` at its count, by measure_identity."""
    from devtools import measure_identity  # noqa: PLC0415

    receipts = {}
    with tempfile.TemporaryDirectory() as directory:
        for n in fact_paths(packet):
            configuration = read_fact(packet, n)["configuration"]
            path = Path(directory) / f"kim-n{n:03d}-shadow-{SHADOW_PLACES}.json"
            path.write_text(json.dumps(shadow(configuration)), encoding="utf-8")
            view = measure_identity.read_packing(f"Kim=center-basis-json:{path}", n)
            others = [measure_identity.read_packing(against, n)]
            receipts[n] = measure_identity.receipt(n, view, others)
    return receipts


# --------------------------------------------------------------------------- command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(__doc__ or "").splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("packet", help="the packet's directory name under resources/web/")
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("check")
    side_parser = sub.add_parser("side")
    side_parser.add_argument("--ledger", type=Path, required=True)
    side_parser.add_argument("--write", action="store_true")
    certify_parser = sub.add_parser("certify")
    certify_parser.add_argument("--jobs-dir", type=Path, required=True)
    certify_parser.add_argument("--n", type=int, nargs="+")
    job = sub.add_parser("decide-job")
    job.add_argument("--n", type=int, required=True)
    job.add_argument("--control", choices=JOBS, required=True)
    job.add_argument("--output", type=Path, required=True)
    replay_parser = sub.add_parser("replay")
    replay_parser.add_argument("--scratch", type=Path, required=True)
    replay_parser.add_argument("--n", type=int, nargs="+")
    measure_parser = sub.add_parser("measure")
    measure_parser.add_argument("--against", required=True)
    measure_parser.add_argument("--write", action="store_true")
    sub.add_parser("admit")
    args = parser.parse_args(argv)
    packet = reports.packet_path(args.packet)
    if args.action == "check":
        print(json.dumps(check(packet), indent=1))
    elif args.action == "side":
        record = side(packet, args.ledger)
        text = json.dumps(record, indent=1) + "\n"
        target = packet / "receipts/side.json"
        if args.write:
            target.parent.mkdir(exist_ok=True)
            target.write_text(text, encoding="utf-8")
        else:
            _require(target.read_text(encoding="utf-8") == text, f"{target.name} differs")
        print(text, end="")
    elif args.action == "certify":
        certify(packet, args.jobs_dir, args.n)
    elif args.action == "decide-job":
        decide_job(packet, args.n, args.control, args.output)
    elif args.action == "replay":
        replay(packet, args.scratch, args.n)
    elif args.action == "measure":
        for n, receipt in measure(packet, args.against).items():
            text = json.dumps(receipt, indent=1) + "\n"
            target = packet / f"measure/identity-n{n:03d}.json"
            if args.write:
                target.parent.mkdir(exist_ok=True)
                target.write_text(text, encoding="utf-8")
            print(text, end="")
    else:
        for n in fact_paths(packet):
            admit_route1(packet, n)
        admit_route2(packet)
        print("admitted: route 1 at", sorted(fact_paths(packet)), "and route 2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
