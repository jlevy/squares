#!/usr/bin/env python3
"""Run Evan Daniel's vendored regularizer on the known-best witnesses, deciding here.

The assessment ``docs/project/research/research-2026-10-11-evand-regularization-assessment.md``
(sections 3 and 5, slices 1 and 2) is the specification. The generator is Evan Daniel's
``search/exact/exactsolve.py`` and ``search/regularize/reg.py`` at the pin its manifest
``vendor/evand-regularize/vendored.yaml`` names (`revision`),
vendored unmodified under ``vendor/evand-regularize/`` (MIT). This driver never edits that
tree and never imports it: each stage copies the vendored ``search/`` subtree into a
replica inside the run directory, because upstream writes ``batch/work/...`` beside its
own files, and runs it there with ``python -I`` and this project's interpreter, from
outside the vendored directory, one process per count, with a timeout. Every decision is
this project's code: the certificates are read back through
`devtools.evand_exact_certificates`' parser and decided on both maintained exact routes.

Subcommands, from ``packing/``, each after
``uv run --frozen --all-extras --group dev python -m devtools.regularize_evand``:

``witness-input --n N... --run-dir DIR``
    Write each ``witnesses/known-best/n-NNN.yaml`` as upstream's input text, ``n S`` then
    one ``x y theta_deg`` row per square, centres (upstream's ``x y`` are centres, as its
    ``Pack.load`` and ``batch/register.py`` read them) about the lower-left corner, in the
    witness's square order. A rational or decimal scalar is printed exactly when its
    decimal expansion ends within `EXACT_LIMIT` significant digits and otherwise to
    `DIGITS` (``batch/register.py`` printed binary64); a number-field scalar from a
    rigorous enclosure. Records per count the scalar kind, the printed side and the exact
    side of a rational witness.

``exact-solve --n N... --run-dir DIR [--timeout S] [--procs K]``
    Run ``exactsolve.py`` on each input in the replica and keep its ``.exact.txt``,
    ``.json``, ``.contacts.json`` and ``.cert`` there; write ``exact/receipt.json``: the
    pin, the interpreter, and per count the status, ``S_exact``, ``cert_valid``,
    ``newton_converged``, the free squares and wall and CPU seconds.

``regularize --n N... --run-dir DIR [--policy P] [--style S] [--orient O]``
    Run ``reg.regularize`` per count through `devtools.regularize_evand_shim`, copied into
    the replica, since ``atlas.py`` does not expose ``orient``. Defaults: ``conservative``,
    ``coincide``, the source orientation (``orient = 0``); ``--policy fewest`` makes the
    alternates for comparison; ``--orient upstream`` is upstream's refit.

``import --n N... --run-dir DIR [--policy P] [...]``
    Read each regularized certificate, map it back to the source witness's frame (the
    inverse container symmetry where the orientation was refitted), check the square
    order, decide it on both maintained routes (`sqpack.witness.exact_verify` and
    `devtools.check_rational_witness_independent`), measure identity against the source
    witness (`devtools.check_half_angle_area.arrangement_gap`, and square by square in
    order), the house and stage contact shades before and after
    (`devtools.census_atlas_contact_shades`), the side relation against the witness's
    side and the register's verified upper bound, and attempt the exact same-side
    re-solve where `devtools.regularize_same_side` is available. Classifies each view:
    ``same`` (an exact view at the witness's side), ``solved`` (a dilated certificate
    whose side differs) or ``refused`` (with reasons).

``render --n N... --run-dir DIR [--out DIR]``
    Per count, a three-panel SVG at one scale -- the source witness, the project's
    ``regularize_axis_components/2`` view where the atlas layer keeps one, and the view
    made here -- with the squares that moved outlined, and the view drawn alone by the
    house renderer; every derived drawing says it is regularized. Writes ``summary.json``,
    one row per count of every measure and the per-stage timings.

``run --n N... --run-dir DIR``
    Every stage in order.

``table --summary PATH``
    The per-count table and the per-stage timings of a ``summary.json``, as Markdown.

``--n`` takes counts and ranges (``5 10 100-120``). ``--procs`` (default 2) is the number
of counts run at once; each child is pinned to one BLAS thread. Nothing is written under
``witnesses/``, ``atlas/`` or the vendored tree: the run directory is scratch (OR-18),
and the outputs are what a later slice retains, by digest, if the owner admits them.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import filecmp
import functools
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import threading
import time
from collections.abc import Callable, Iterable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from decimal import ROUND_CEILING, ROUND_DOWN, ROUND_HALF_EVEN, Decimal, localcontext
from fractions import Fraction
from importlib import import_module, metadata
from pathlib import Path
from types import ModuleType
from typing import Any
from xml.sax.saxutils import escape

import mpmath as mp

from devtools import census_atlas_contact_shades as shades
from devtools import evand_exact_certificates as certificates
from devtools.check_half_angle_area import AreaRouteError, arrangement_gap, decide_placed
from sqpack.field import FieldElement, NumberField
from sqpack.witness import witness_document
from sqpack.yamlio import load_yaml, safe_load

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
VENDORED = REPO / "vendor/evand-regularize"
VENDORED_SEARCH = VENDORED / "search"
SHIM = Path(__file__).with_name("regularize_evand_shim.py")
KNOWN_BEST = ROOT / "witnesses/known-best"
LAYER = ROOT / "atlas/known-best/regularized"
LAYER_INDEX = LAYER / "index.json"
FORBIDDEN_RUN_ROOTS = (ROOT / "witnesses", ROOT / "atlas", VENDORED)

SOURCE = "https://github.com/evand/square-packing"
MANIFEST = VENDORED / "vendored.yaml"
LICENSE = "MIT, Copyright (c) 2026 Evan Daniel (vendor/evand-regularize/LICENSE)"
FORMAT = "regularize-evand-receipt-v1"
GENERATOR = "python -m devtools.regularize_evand"

#: Significant digits of a scalar whose decimal expansion does not end soon enough.
DIGITS = 60
#: A rational's expansion is printed in full when it ends within this many digits.
EXACT_LIMIT = 100
#: Working precision, in decimal digits, for angles and number-field projections.
WORKING_DIGITS = 90
#: Per-count timeouts, upstream's own for its exact re-solves: 1800 s up to n = 200, 3600 s
#: above (``samepacking.py`` ``kkt_test``).
SMALL_TIMEOUT, LARGE_TIMEOUT, TIMEOUT_SPLIT = 1800, 3600, 200
DEFAULT_PROCS = 2
POLICIES = ("conservative", "fewest", "free")
STYLES = ("coincide", "pretty", "gravity")
ORIENTS = ("source", "upstream")
#: Child processes are held to one BLAS thread each, so `--procs` is the CPU they use.
THREAD_PINS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")
#: Identity is measured at this many decimal places (moves below 1e-20 are the dilation).
IDENTITY_PLACES = 30
#: Displacement and turn (degrees) above which a square counts as moved in a drawing.
VISIBLE_MOVE = 1e-4
VISIBLE_TURN_DEGREES = 1e-4
#: Thresholds at which moved squares are counted, in order of the identity frame.
MOVE_THRESHOLDS = (1e-9, 1e-6, 1e-3, 1e-1)
LABEL = "regularized"
VIEW_KIND = "regularized-view"
#: What a scratch run means at a count the owner holds (`evand_exact_certificates.HELD`).
HELD_NOTE = (
    "held by the owner for the n = 17 work (think-x4v4): measured in scratch only; nothing "
    "here is retained, registered or replayed for it"
)
#: A register value's exact form that is a rational literal, not a symbolic expression.
RATIONAL_LITERAL = re.compile(r"-?\d+(?:/[1-9]\d*|\.\d+)?")


class DriverError(ValueError):
    """An input or a run directory this driver refuses."""


# --------------------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------------------


def parse_counts(values: Iterable[str]) -> list[int]:
    """Counts from ``N`` and ``A-B`` tokens, each once, in order."""
    counts: list[int] = []
    for value in values:
        for token in value.replace(",", " ").split():
            low, _, high = token.partition("-")
            first, last = int(low), int(high or low)
            if first < 1 or last < first:
                raise DriverError(f"{token!r} is not a count or an increasing range")
            counts.extend(range(first, last + 1))
    if not counts:
        raise DriverError("no counts given")
    return sorted(set(counts))


def default_timeout(n: int) -> int:
    return SMALL_TIMEOUT if n <= TIMEOUT_SPLIT else LARGE_TIMEOUT


def guard_run_dir(run_dir: Path) -> Path:
    """The run directory, refused inside the record, the atlas or the vendored tree."""
    resolved = run_dir.resolve()
    for forbidden in FORBIDDEN_RUN_ROOTS:
        if resolved == forbidden.resolve() or forbidden.resolve() in resolved.parents:
            raise DriverError(f"refusing to write a run under {forbidden}")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=1, default=str) + "\n", encoding="utf-8")
    temporary.replace(path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def host() -> dict[str, Any]:
    """The machine a stage ran on, and how loaded it was when the stage began."""
    load = os.getloadavg()
    return {
        "platform": platform.platform(),
        "cpu_count": os.cpu_count(),
        "load_average_1_5_15": [round(value, 2) for value in load],
        "measured_at": now(),
    }


def interpreter() -> dict[str, Any]:
    versions = {name: metadata.version(name) for name in ("numpy", "scipy", "mpmath")}
    return {
        "executable": sys.executable,
        "python": platform.python_version(),
        "flags": "-I",
        **versions,
    }


@functools.cache
def revision() -> str:
    """The upstream commit the vendored copy is pinned at, read from its manifest."""
    manifest = load_yaml(MANIFEST.read_text(encoding="utf-8"))
    commit = str(manifest.get("source_commit", ""))
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise DriverError(f"{MANIFEST} names no 40-hex source_commit")
    return commit


def pin() -> dict[str, str]:
    return {
        "source": SOURCE,
        "revision": revision(),
        "vendored": VENDORED.relative_to(REPO).as_posix(),
        "license": LICENSE,
    }


def literal(value: Fraction) -> str:
    return certificates.literal(value)


def decimal_text(value: Fraction, *, rounding: str = ROUND_HALF_EVEN) -> tuple[str, bool]:
    """``value`` as a plain decimal, and whether the text is exactly ``value``.

    Exact when the expansion ends within `EXACT_LIMIT` significant digits, otherwise
    rounded to `DIGITS` in the direction ``rounding``.
    """
    exact = certificates.terminating_decimal(value)
    if exact is not None and len(Decimal(exact).as_tuple().digits) <= EXACT_LIMIT:
        return plain_decimal(Decimal(exact)), True
    with localcontext() as context:
        context.prec = DIGITS
        context.rounding = rounding
        rounded = Decimal(value.numerator) / Decimal(value.denominator)
    return plain_decimal(rounded), False


def decimal_digits(value: Fraction, digits: int = 40) -> str:
    """``value`` to ``digits`` significant digits, rounded toward zero, for reading."""
    with localcontext() as context:
        context.prec = digits
        context.rounding = ROUND_DOWN
        return plain_decimal(Decimal(value.numerator) / Decimal(value.denominator))


def plain_decimal(value: Decimal) -> str:
    text = format(value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return "0" if text in {"-0", ""} else text


def fixed(value: Any) -> str:
    """An mpmath number to `DIGITS` significant digits, never in exponent notation."""
    return str(mp.nstr(value, DIGITS, min_fixed=-math.inf, max_fixed=math.inf))


def mp_of(value: Fraction | FieldElement) -> Any:
    """``value`` at `WORKING_DIGITS` digits, from an exact rational or a field enclosure."""
    mp.mp.dps = WORKING_DIGITS
    if isinstance(value, FieldElement):
        value.field.refine_to(WORKING_DIGITS + 10)
        low, high = value.field.enclose(value)
        value = (low + high) / 2
    return mp.mpf(value.numerator) / value.denominator


def fraction_of_mp(value: Any, places: int = IDENTITY_PLACES + 10) -> Fraction:
    return Fraction(round(value * mp.mpf(10) ** places), 10**places)


def rounded(value: Fraction, places: int = IDENTITY_PLACES) -> Fraction:
    return Fraction(round(value * 10**places), 10**places)


# --------------------------------------------------------------------------------------
# Witnesses and the register
# --------------------------------------------------------------------------------------


def repo_relative(path: Path) -> str:
    """``path`` relative to the repository root, as the record writes paths, when it is
    inside it."""
    resolved = path.resolve()
    if REPO.resolve() in resolved.parents:
        return resolved.relative_to(REPO.resolve()).as_posix()
    return str(resolved)


def witness_path(n: int) -> Path:
    return KNOWN_BEST / f"n-{n:03d}.yaml"


def load_known_best(n: int) -> dict[str, Any]:
    document = safe_load(witness_path(n).read_text(encoding="utf-8"))
    witness = document["witness"]
    if witness["n"] != n:
        raise DriverError(f"{witness_path(n)} holds n = {witness['n']}")
    return witness


def number_field(witness: Mapping[str, Any]) -> NumberField | None:
    scalar = witness["scalar"]
    if scalar["kind"] != "algebraic-number-field":
        return None
    return NumberField(
        [Fraction(value) for value in scalar["minimal_polynomial"]],
        tuple(Fraction(value) for value in scalar["isolating_interval"]),
    )


def scalar_reader(witness: Mapping[str, Any]) -> Callable[[Any], Fraction | FieldElement]:
    """How this witness's scalars read exactly: decimals and ratios as fractions."""
    kind = witness["scalar"]["kind"]
    if kind not in {"rational", "decimal", "algebraic-number-field"}:
        raise DriverError(f"scalar kind {kind!r} has no exact input text here")
    field = number_field(witness)

    def read(value: Any) -> Fraction | FieldElement:
        if field is not None and isinstance(value, list):
            return field.element([Fraction(str(item)) for item in value])
        if field is not None:
            return field.rational(Fraction(str(value)))
        return Fraction(str(value))

    return read


def _text_of(
    value: Fraction | FieldElement, *, rounding: str = ROUND_HALF_EVEN
) -> tuple[str, bool]:
    if isinstance(value, FieldElement):
        if all(coefficient == 0 for coefficient in value.coeffs[1:]):
            return decimal_text(value.coeffs[0], rounding=rounding)
        return fixed(mp_of(value)), False
    return decimal_text(value, rounding=rounding)


def _degrees(dy: Fraction | FieldElement, dx: Fraction | FieldElement) -> tuple[str, bool]:
    """The direction of ``(dx, dy)`` in degrees, exact where it is an axis direction."""
    zero_y = dy == 0 if isinstance(dy, Fraction) else all(c == 0 for c in dy.coeffs)
    zero_x = dx == 0 if isinstance(dx, Fraction) else all(c == 0 for c in dx.coeffs)
    if zero_y or zero_x:
        return "0", True
    angle = mp.degrees(mp.atan2(mp_of(dy), mp_of(dx)))
    return fixed(angle), False


def _rounding(text: str, value: Fraction | FieldElement) -> float:
    """How far a printed centre lies from the witness's exact one."""
    if isinstance(value, FieldElement):
        return float(abs(mp.mpf(text) - mp_of(value)))
    return float(abs(Fraction(text) - value))


@dataclass(frozen=True, slots=True)
class InputText:
    """One witness as upstream's input text, with what the conversion kept exactly."""

    text: str
    side_text: str
    exact: bool
    info: dict[str, Any]


def witness_input(witness: Mapping[str, Any]) -> InputText:
    """``n S`` then ``x y theta_deg`` per square: centres about the lower-left corner."""
    read = scalar_reader(witness)
    side = read(witness["side"])
    side_text, side_exact = _text_of(side, rounding=ROUND_CEILING)
    representation = witness["representation"]
    unit = witness["coordinates"]["angle_unit"]
    shift = (
        side * Fraction(1, 2) if witness["coordinates"]["origin"] == "container-center" else 0
    )
    rows: list[str] = []
    centres_exact = angles_exact = True
    rounding = 0.0
    for square in witness["squares"]:
        if representation == "corners":
            points = [(read(x), read(y)) for x, y in square["corners"]]
            cx = (points[0][0] + points[1][0] + points[2][0] + points[3][0]) * Fraction(1, 4)
            cy = (points[0][1] + points[1][1] + points[2][1] + points[3][1]) * Fraction(1, 4)
            angle, angle_exact = _degrees(
                points[1][1] - points[0][1], points[1][0] - points[0][0]
            )
        else:
            cx, cy = (read(value) for value in square["center"])
            if representation == "center-basis":
                cosine, sine = (read(value) for value in square["basis"])
                angle, angle_exact = _degrees(sine, cosine)
            elif unit == "degrees":
                angle, angle_exact = plain_decimal(Decimal(str(square["angle"]))), True
            else:
                radians = mp_of(Fraction(str(square["angle"])))
                angle_exact = radians == 0
                angle = "0" if angle_exact else fixed(mp.degrees(radians))
        x_text, x_exact = _text_of(cx + shift)
        y_text, y_exact = _text_of(cy + shift)
        rounding = max(rounding, _rounding(x_text, cx + shift), _rounding(y_text, cy + shift))
        centres_exact = centres_exact and x_exact and y_exact
        angles_exact = angles_exact and angle_exact
        rows.append(f"{x_text} {y_text} {angle}")
    text = f"{witness['n']} {side_text}\n" + "\n".join(rows) + "\n"
    kind = witness["scalar"]["kind"]
    info = {
        "witness": repo_relative(witness_path(witness["n"])),
        "witness_id": witness["id"],
        "scalar_kind": kind,
        "representation": representation,
        "printed_side": witness["side"],
        "exact_side": literal(side)
        if isinstance(side, Fraction) and kind == "rational"
        else None,
        "side_text": side_text,
        "side_text_exact": side_exact,
        "centres_exact": centres_exact,
        "angles_exact": angles_exact,
        "text_exact": side_exact and centres_exact and angles_exact,
        "largest_centre_rounding": rounding,
        "digits": DIGITS,
    }
    return InputText(text, side_text, bool(info["text_exact"]), info)


def case_record(n: int) -> dict[str, Any]:
    return certificates.case_record(n)


def verified_bound(n: int) -> dict[str, Any]:
    """The register's verified upper bound ``U`` at ``n``: its value and exact form, and,
    for a ``root(P, value)`` form, the minimal polynomial the case states for ``P``."""
    record = case_record(n)
    bound = record.get("verified_upper_bound") or {}
    found = {"value": bound.get("value"), "exact_form": bound.get("exact_form")}
    if str(found["exact_form"] or "").startswith("root("):
        reported = record.get("reported_upper_bound") or {}
        found["minimal_polynomial"] = reported.get("minimal_polynomial")
    return found


def found_by(n: int) -> list[str]:
    return list((case_record(n).get("reported_upper_bound") or {}).get("found_by") or [])


def layer_entry(n: int) -> dict[str, Any] | None:
    if not LAYER_INDEX.is_file():
        return None
    for entry in read_json(LAYER_INDEX)["entries"]:
        if entry["n"] == n:
            return entry
    return None


def layer_status(n: int) -> dict[str, Any]:
    entry = layer_entry(n)
    if entry is None:
        return {"status": "absent"}
    status: dict[str, Any] = {"status": entry["status"]}
    if entry.get("refusal"):
        status["refusal"] = entry["refusal"]["kind"]
    if entry.get("changed_squares") is not None:
        status["changed_squares"] = entry["changed_squares"]
    if entry.get("view"):
        status["view"] = entry["view"]["path"]
    return status


# --------------------------------------------------------------------------------------
# The replica and the child processes
# --------------------------------------------------------------------------------------


def replica_root(run_dir: Path) -> Path:
    return run_dir / "replica"


def replica_search(run_dir: Path) -> Path:
    return replica_root(run_dir) / "search"


def work_dir(run_dir: Path, n: int) -> Path:
    return replica_search(run_dir) / "exact/batch/work" / f"n-{n}"


def _vendored_files() -> list[str]:
    return sorted(
        path.relative_to(VENDORED_SEARCH).as_posix()
        for path in VENDORED_SEARCH.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    )


def ensure_replica(run_dir: Path) -> Path:
    """A copy of the vendored ``search/`` subtree in the run directory.

    Made on first use; on reuse every vendored file must be byte-identical to the copy,
    so a run never mixes two pins. The replica's ``batch/results.json`` is replaced by
    this driver's own (`write_results`), so upstream's list never names an input here.
    """
    search = replica_search(run_dir)
    if not search.is_dir():
        shutil.copytree(VENDORED_SEARCH, search, ignore=shutil.ignore_patterns("__pycache__"))
        (search / "exact/batch/results.json").write_text("[]\n", encoding="utf-8")
    files = [name for name in _vendored_files() if name != "exact/batch/results.json"]
    _, mismatch, errors = filecmp.cmpfiles(VENDORED_SEARCH, search, files, shallow=False)
    if mismatch or errors:
        raise DriverError(
            f"the replica in {run_dir} differs from the vendored tree at "
            f"{(mismatch + errors)[:3]}; start a fresh run directory"
        )
    shutil.copyfile(SHIM, search / "regularize" / SHIM.name)
    return search


@dataclass(frozen=True, slots=True)
class ChildRun:
    returncode: int | None
    timed_out: bool
    wall_seconds: float
    cpu_seconds: float


def child_environment() -> dict[str, str]:
    environment = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "REG_REFRESH": "0"}
    environment.update(dict.fromkeys(THREAD_PINS, "1"))
    for key in ("HOME", "LANG", "TMPDIR"):
        if key in os.environ:
            environment[key] = os.environ[key]
    return environment


def run_child(command: Sequence[str], log: Path, *, cwd: Path, timeout: float) -> ChildRun:
    """One child process, killed at ``timeout``, with its own wall and CPU seconds.

    The child is reaped with ``os.wait4`` so its CPU time is its own even while other
    children run beside it.
    """
    log.parent.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    with log.open("w", encoding="utf-8") as stream:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            env=child_environment(),
            stdout=stream,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
        )
        expired = threading.Event()

        def kill() -> None:
            expired.set()
            with contextlib.suppress(ProcessLookupError):
                process.kill()

        timer = threading.Timer(timeout, kill)
        timer.start()
        try:
            _pid, status, usage = os.wait4(process.pid, 0)
        finally:
            timer.cancel()
    process.returncode = os.waitstatus_to_exitcode(status)
    return ChildRun(
        returncode=None if expired.is_set() else process.returncode,
        timed_out=expired.is_set(),
        wall_seconds=round(time.perf_counter() - started, 3),
        cpu_seconds=round(usage.ru_utime + usage.ru_stime, 3),
    )


def _parallel[T](function: Callable[[int], T], counts: Sequence[int], procs: int) -> list[T]:
    """``function`` over ``counts``, ``procs`` at a time, largest count first."""
    order = sorted(counts, reverse=True)
    if procs <= 1 or len(order) <= 1:
        results = {n: function(n) for n in order}
    else:
        with ThreadPoolExecutor(max_workers=procs) as pool:
            results = dict(zip(order, pool.map(function, order), strict=True))
    return [results[n] for n in sorted(counts)]


# --------------------------------------------------------------------------------------
# Stage 1: witness input
# --------------------------------------------------------------------------------------


def inputs_dir(run_dir: Path) -> Path:
    return run_dir / "inputs"


def input_path(run_dir: Path, n: int) -> Path:
    return inputs_dir(run_dir) / f"n-{n:03d}.txt"


def _merge_receipt(
    path: Path, header: dict[str, Any], rows: Sequence[dict[str, Any]]
) -> dict[str, Any]:
    """A receipt with ``rows`` replacing any earlier row of the same count."""
    previous = read_json(path)["rows"] if path.is_file() else []
    merged = {row["n"]: row for row in previous}
    merged.update({row["n"]: row for row in rows})
    receipt = {**header, "rows": [merged[n] for n in sorted(merged)]}
    write_json(path, receipt)
    return receipt


def stage_witness_input(counts: Sequence[int], run_dir: Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for n in counts:
        wall, cpu = time.perf_counter(), time.process_time()
        converted = witness_input(load_known_best(n))
        path = input_path(run_dir, n)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(converted.text, encoding="utf-8")
        rows.append(
            {
                "n": n,
                **converted.info,
                "input": path.relative_to(run_dir).as_posix(),
                "wall_seconds": round(time.perf_counter() - wall, 3),
                "cpu_seconds": round(time.process_time() - cpu, 3),
            }
        )
    header = {
        "format": FORMAT,
        "stage": "witness-input",
        "tool": f"{GENERATOR} witness-input",
        "what": "Each known-best witness as upstream's `n S` / `x y theta_deg` input text.",
        "host": host(),
    }
    return _merge_receipt(inputs_dir(run_dir) / "receipt.json", header, rows)


# --------------------------------------------------------------------------------------
# Stage 2: the exact solve
# --------------------------------------------------------------------------------------


def exact_receipt_path(run_dir: Path) -> Path:
    return run_dir / "exact" / "receipt.json"


def _decimal_difference(left: str | None, right: str | None) -> float | None:
    if left is None or right is None:
        return None
    try:
        return float(Fraction(left) - Fraction(right))
    except ValueError, ZeroDivisionError:
        return None


def solve_one(n: int, run_dir: Path, timeout: float) -> dict[str, Any]:
    """``exactsolve.py`` on one count's input, in the replica, and what it reported."""
    work = work_dir(run_dir, n)
    work.mkdir(parents=True, exist_ok=True)
    source = input_path(run_dir, n)
    if not source.is_file():
        return {"n": n, "status": "no-input", "reason": f"run witness-input first ({source})"}
    staged = work / "witness.txt"
    shutil.copyfile(source, staged)
    for stale in work.glob("witness.*"):
        if stale != staged:
            stale.unlink()
    script = replica_search(run_dir) / "exact/exactsolve.py"
    child = run_child(
        [sys.executable, "-I", str(script), str(staged), "--out", str(work)],
        work / "witness.log",
        cwd=run_dir,
        timeout=timeout,
    )
    row: dict[str, Any] = {
        "n": n,
        "timeout_seconds": timeout,
        "returncode": child.returncode,
        "wall_seconds": child.wall_seconds,
        "cpu_seconds": child.cpu_seconds,
        "log": (work / "witness.log").relative_to(run_dir).as_posix(),
    }
    report_path = work / "witness.json"
    if child.timed_out:
        return {**row, "status": "timeout"}
    if not report_path.is_file():
        return {**row, "status": "error", "reason": "exactsolve wrote no report"}
    report = read_json(report_path)
    second = report.get("second_order") or {}
    if report.get("status"):
        status = str(report["status"]).replace(" ", "-")
    elif report.get("cert_valid"):
        status = "certified"
    else:
        status = "certificate-invalid"
    witness = load_known_best(n)
    bound = verified_bound(n)
    printed = witness["side"] if isinstance(witness["side"], str) else None
    row.update(
        {
            "status": status,
            "exactsolve_status": report.get("status"),
            "second_order_status": second.get("status"),
            "S_input": report.get("S_input"),
            "S_exact": report.get("S_exact"),
            "S_cert": report.get("S_cert"),
            "S_cert_decimal": report.get("S_cert_decimal"),
            "cert_valid": report.get("cert_valid"),
            "newton_converged": report.get("newton_converged"),
            "free_squares": report.get("free_squares"),
            "contact_tol": report.get("contact_tol"),
            "jam_residual": report.get("jam_residual"),
            "lambda_A_maxmin": report.get("lambda_A_maxmin"),
            "vv_milp_dS": report.get("vv_milp_dS"),
            "cert_min_pair": report.get("cert_min_pair"),
            "exactsolve_seconds": report.get("seconds"),
            "S_exact_minus_printed": _decimal_difference(report.get("S_exact"), printed),
            "S_exact_minus_verified": _decimal_difference(
                report.get("S_exact"), bound["value"]
            ),
            "verified_bound": bound,
            "outputs": {
                suffix: (work / f"witness{suffix}").relative_to(run_dir).as_posix()
                for suffix in (".exact.txt", ".json", ".contacts.json", ".cert")
                if (work / f"witness{suffix}").is_file()
            },
        }
    )
    return row


RESULTS_LOCK = threading.Lock()


def write_results(run_dir: Path, counts: Iterable[int]) -> None:
    """The replica's ``batch/results.json``: what ``reg.load`` reads for each count.

    Rebuilt for ``counts`` from their work directories, so it is right whichever stage
    runs first: a count is listed when its exact solve wrote an 80-digit point
    (``work/n-N/witness.exact.txt`` and its report), and dropped otherwise. Upstream's own
    list is never consulted.
    """
    path = replica_search(run_dir) / "exact/batch/results.json"
    with RESULTS_LOCK:
        previous = {row["n"]: row for row in read_json(path)} if path.is_file() else {}
        for n in counts:
            work = work_dir(run_dir, n)
            if (
                not (work / "witness.exact.txt").is_file()
                or not (work / "witness.json").is_file()
            ):
                previous.pop(n, None)
                continue
            report = read_json(work / "witness.json")
            solved = report.get("status") or (
                "certified" if report.get("cert_valid") else "certificate invalid"
            )
            previous[n] = {
                "n": n,
                "register": load_known_best(n)["side"],
                "by": found_by(n),
                "status": f"project witness input; exactsolve: {solved}",
                "from_": "witness",
                "free": report.get("free_squares") or [],
                "input": "project known-best witness (devtools.regularize_evand)",
            }
        write_json(path, [previous[n] for n in sorted(previous)])


def stage_exact_solve(
    counts: Sequence[int], run_dir: Path, *, timeout: float | None, procs: int
) -> dict[str, Any]:
    ensure_replica(run_dir)
    header = {
        "format": FORMAT,
        "stage": "exact-solve",
        "tool": f"{GENERATOR} exact-solve",
        "what": (
            "Upstream exactsolve.py, at the pin, on each witness input: the 80-digit KKT "
            "point, its contact structure and its dilated rational certificate."
        ),
        "pin": pin(),
        "interpreter": interpreter(),
        "procs": procs,
        "host": host(),
    }
    rows = _parallel(
        lambda n: solve_one(n, run_dir, timeout or default_timeout(n)), counts, procs
    )
    write_results(run_dir, counts)
    header["host_after"] = host()
    return _merge_receipt(exact_receipt_path(run_dir), header, rows)


# --------------------------------------------------------------------------------------
# Stage 3: the regularizer
# --------------------------------------------------------------------------------------


def variant_name(policy: str, style: str, orient: str) -> str:
    """The output directory of one variant: the policy alone for the defaults."""
    if style == "coincide" and orient == "source":
        return policy
    return f"{policy}-{style}-{orient}"


def regularize_dir(run_dir: Path, variant: str) -> Path:
    return run_dir / "regularize" / variant


def regularize_one(
    n: int, run_dir: Path, *, policy: str, style: str, orient: str, timeout: float
) -> dict[str, Any]:
    variant = variant_name(policy, style, orient)
    out = regularize_dir(run_dir, variant)
    row: dict[str, Any] = {"n": n, "variant": variant, "timeout_seconds": timeout}
    exact = work_dir(run_dir, n) / "witness.exact.txt"
    if not exact.is_file():
        return {**row, "status": "no-exact-input", "reason": "the exact solve wrote no point"}
    for stale in (out / f"n-{n:03d}.cert", out / f"n-{n:03d}.json"):
        stale.unlink(missing_ok=True)
    shim = replica_search(run_dir) / "regularize" / SHIM.name
    command = [
        sys.executable, "-I", str(shim), "--n", str(n), "--policy", policy,
        "--style", style, "--orient", "0" if orient == "source" else "best",
        "--out", str(out),
    ]  # fmt: skip
    child = run_child(command, out / f"n-{n:03d}.log", cwd=run_dir, timeout=timeout)
    row.update(
        {
            "returncode": child.returncode,
            "wall_seconds": child.wall_seconds,
            "cpu_seconds": child.cpu_seconds,
            "log": (out / f"n-{n:03d}.log").relative_to(run_dir).as_posix(),
        }
    )
    record_path = out / f"n-{n:03d}.json"
    if child.timed_out:
        return {**row, "status": "timeout"}
    if child.returncode != 0 or not record_path.is_file():
        tail = (out / f"n-{n:03d}.log").read_text(encoding="utf-8").strip().splitlines()[-3:]
        return {**row, "status": "error", "reason": " | ".join(tail)}
    record = read_json(record_path)
    report = record["report"]
    row.update(
        {
            "status": "certified" if record["cert_valid"] else "certificate-invalid",
            "level": record["level"],
            "level_text": record["level_text"],
            "groups_before": record["groups_before"],
            "groups_after": record["groups_after"],
            "symmetry_imposed": record["symmetry"],
            "rigid_symmetry": report.get("rigid_sym"),
            "symmetry_dropped_for_coincidence": report.get("sym_dropped_for_coincidence"),
            "orientation_g": record["orientation_g"],
            "shape": record["shape"],
            "angle_changes": record["angle_changes"],
            "free_merges": record["free_merges"],
            "place": report.get("place"),
            "coincident": report.get("coincident"),
            "coinc_replace": report.get("coinc_replace"),
            "moved_by_generator": len(report.get("moved") or []),
            "verify_80": record["verify_80"],
            "S_exact": record["S_exact"],
            "S_cert": record["S_cert"],
            "cert_valid": record["cert_valid"],
            "generator_seconds": record["seconds"],
            "certificate": (out / f"n-{n:03d}.cert").relative_to(run_dir).as_posix(),
            "record": record_path.relative_to(run_dir).as_posix(),
        }
    )
    return row


def stage_regularize(
    counts: Sequence[int],
    run_dir: Path,
    *,
    policy: str,
    style: str,
    orient: str,
    timeout: float | None,
    procs: int,
) -> dict[str, Any]:
    ensure_replica(run_dir)
    write_results(run_dir, counts)
    variant = variant_name(policy, style, orient)
    header = {
        "format": FORMAT,
        "stage": "regularize",
        "tool": f"{GENERATOR} regularize",
        "what": (
            "Upstream reg.regularize, at the pin, through devtools.regularize_evand_shim, "
            "with atlas.level_of and reg.write_cert as atlas.compute_one runs them."
        ),
        "variant": {"name": variant, "policy": policy, "style": style, "orient": orient},
        "pin": pin(),
        "interpreter": interpreter(),
        "procs": procs,
        "host": host(),
    }
    rows = _parallel(
        lambda n: regularize_one(
            n,
            run_dir,
            policy=policy,
            style=style,
            orient=orient,
            timeout=timeout or default_timeout(n),
        ),
        counts,
        procs,
    )
    header["host_after"] = host()
    return _merge_receipt(regularize_dir(run_dir, variant) / "receipt.json", header, rows)


# --------------------------------------------------------------------------------------
# Stage 4: import, decision and measurement
# --------------------------------------------------------------------------------------

Placed = tuple[Fraction, Fraction, Fraction, Fraction]


def source_placed(witness: Mapping[str, Any]) -> tuple[Fraction, list[Placed]]:
    """The witness's squares as ``(x, y, c, s)`` about the lower-left corner.

    Exact for a rational witness; a decimal angle's basis and a number-field scalar are
    projections at `IDENTITY_PLACES` + 10 places. This feeds measurements, never a
    decision.
    """
    read = scalar_reader(witness)

    def frac(value: Fraction | FieldElement) -> Fraction:
        return value if isinstance(value, Fraction) else fraction_of_mp(mp_of(value))

    side = frac(read(witness["side"]))
    shift = side / 2 if witness["coordinates"]["origin"] == "container-center" else Fraction(0)
    unit = witness["coordinates"]["angle_unit"]
    placed: list[Placed] = []
    for square in witness["squares"]:
        if witness["representation"] == "corners":
            points = [(frac(read(x)), frac(read(y))) for x, y in square["corners"]]
            cx = sum((p[0] for p in points), Fraction(0)) / 4
            cy = sum((p[1] for p in points), Fraction(0)) / 4
            dx, dy = points[1][0] - points[0][0], points[1][1] - points[0][1]
            if dx * dx + dy * dy != 1:
                length = mp.sqrt(mp_of(dx * dx + dy * dy))
                dx, dy = fraction_of_mp(mp_of(dx) / length), fraction_of_mp(mp_of(dy) / length)
            placed.append((cx + shift, cy + shift, dx, dy))
            continue
        cx, cy = (frac(read(value)) for value in square["center"])
        if witness["representation"] == "center-basis":
            cosine, sine = (frac(read(value)) for value in square["basis"])
        else:
            turn = mp_of(Fraction(str(square["angle"])))
            turn = mp.radians(turn) if unit == "degrees" else turn
            cosine, sine = fraction_of_mp(mp.cos(turn)), fraction_of_mp(mp.sin(turn))
        placed.append((cx + shift, cy + shift, cosine, sine))
    return side, placed


def inverse_symmetry(
    side: Fraction, poses: Sequence[certificates.Pose], g: int
) -> list[certificates.Pose]:
    """Undo upstream's container symmetry ``g`` (``reg.d4``) on exact poses in ``[0, side]``.

    ``reg.d4`` applies ``g & 3`` quarter turns ``(x, y) -> (S - y, x)`` and then, when
    ``g & 4``, the mirror ``x -> S - x`` with ``theta -> -theta``. A quarter turn leaves a
    unit square's half-angle tangent as it is (the square is the same at ``theta + 90``),
    and the mirror negates it. Exact over Q, and ``[0, side]^2`` is mapped onto itself.
    """
    mapped: list[certificates.Pose] = []
    for pose in poses:
        x, y, t = pose.x, pose.y, pose.t
        if g & 4:
            x, t = side - x, -t
        for _turn in range(g & 3):
            x, y = y, side - x
        mapped.append(certificates.Pose(x, y, t))
    return mapped


def _rounded_placed(square: Placed) -> Placed:
    x, y, c, s = square
    return rounded(x), rounded(y), rounded(c), rounded(s)


def _turn_degrees(left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]) -> float:
    """The least rotation between two unit squares' orientations, modulo 90 degrees.

    The sine of that angle is ``min(|c b - s a|, |c a + s b|)`` over the two bases (the
    measure `arrangement_gap` reports), taken at `IDENTITY_PLACES` and converted with an
    arcsine at the working precision, so a turn far below binary64 resolution is not
    reported as rounding noise.
    """
    (c, s), (a, b) = (rounded(v) for v in left), (rounded(v) for v in right)
    sine = min(abs(c * b - s * a), abs(c * a + s * b))
    mp.mp.dps = WORKING_DIGITS
    return float(mp.degrees(mp.asin(min(mp_of(sine), mp.mpf(1)))))


def identity(
    view: tuple[Fraction, list[Placed]],
    source: tuple[Fraction, list[Placed]],
    ids: Sequence[Any],
) -> dict[str, Any]:
    """The view against its source witness: `arrangement_gap` under the best symmetry,
    and square by square in the shared order (the order the generator preserves)."""
    left = (view[0], [_rounded_placed(square) for square in view[1]])
    right = (source[0], [_rounded_placed(square) for square in source[1]])
    try:
        gap: dict[str, Any] = arrangement_gap(left, right)
        one_to_one = True
    except AreaRouteError as error:
        gap = {"unmatched": str(error)}
        one_to_one = False
    moves = [
        math.hypot(float(a[0] - b[0]), float(a[1] - b[1]))
        for a, b in zip(view[1], source[1], strict=True)
    ]
    turns = [
        _turn_degrees((a[2], a[3]), (b[2], b[3]))
        for a, b in zip(view[1], source[1], strict=True)
    ]
    nearest = [
        min(
            range(len(source[1])),
            key=lambda j, a=a: (
                (float(a[0] - source[1][j][0]) ** 2) + (float(a[1] - source[1][j][1]) ** 2)
            ),
        )
        for a in view[1]
    ]
    permuted = [i for i, j in enumerate(nearest) if i != j]
    visible = [
        i
        for i, (move, turn) in enumerate(zip(moves, turns, strict=True))
        if move > VISIBLE_MOVE or turn > VISIBLE_TURN_DEGREES
    ]
    return {
        "basis": "measured",
        "measured_in": f"{GENERATOR} import (devtools.check_half_angle_area.arrangement_gap)",
        "places": IDENTITY_PLACES,
        "one_to_one": one_to_one,
        "best_symmetry": gap.get("symmetry"),
        "arrangement_gap": gap,
        "order_preserved": not permuted,
        "nearest_not_in_order": [ids[i] for i in permuted][:20],
        "max_move": max(moves, default=0.0),
        "max_turn_degrees": max(turns, default=0.0),
        "moved": {
            f"{threshold:g}": sum(move > threshold for move in moves)
            for threshold in MOVE_THRESHOLDS
        },
        "turned_beyond_1e-6_degrees": sum(turn > 1e-6 for turn in turns),
        "turned_beyond_sine_1e-6": sum(turn > TURN_DEGREES for turn in turns),
        "angle_classes_equal": angle_classes(view[1]) == angle_classes(source[1]),
        "visible_moved_ids": [ids[i] for i in visible],
        "moved_ids": [ids[i] for i, move in enumerate(moves) if move > VISIBLE_MOVE],
        "turned_ids": [ids[i] for i, turn in enumerate(turns) if turn > VISIBLE_TURN_DEGREES],
    }


#: A turn whose sine is `TURN_SINE`, in degrees (the policy's threshold for "turned").
TURN_DEGREES = math.degrees(math.asin(1e-6))
#: Two squares share an angle class when their orientations agree to this many radians,
#: the house renderer's angle tolerance.
CLASS_RADIANS = 1e-6


def angle_classes(placed: Sequence[Placed]) -> set[frozenset[int]]:
    """The squares grouped by orientation modulo a quarter turn, as index sets."""
    angles = [math.atan2(float(s), float(c)) % (math.pi / 2) for _x, _y, c, s in placed]
    classes: list[tuple[float, list[int]]] = []
    for index, angle in enumerate(angles):
        for representative, members in classes:
            gap = abs(angle - representative) % (math.pi / 2)
            if min(gap, math.pi / 2 - gap) < CLASS_RADIANS:
                members.append(index)
                break
        else:
            classes.append((angle, [index]))
    return {frozenset(members) for _angle, members in classes}


def per_square_counts(witness: Mapping[str, Any]) -> tuple[list[int], list[int]]:
    """Each square's house and stage contact counts, as the census counts them."""
    exact, frame, _angles = shades.packings_from_witness(dict(witness))
    house = [min(4, len(found)) for found in shades.edge_rule_contacts(exact, shades.RULES[0])]
    stage = [
        min(4, len(found)) for found in shades.centre_rule_contacts(frame, shades.RULES[1])
    ]
    return house, stage


def shade_measure(source_file: Path, view_file: Path) -> dict[str, Any]:
    """Light and green squares before and after (`witness_shades`), and every square whose
    house or stage count fell against the source witness."""
    before = shades.witness_shades(source_file)
    after = shades.witness_shades(view_file)
    source_doc = load_yaml(source_file.read_text(encoding="utf-8"))["witness"]
    view_doc = load_yaml(view_file.read_text(encoding="utf-8"))["witness"]
    house_before, stage_before = per_square_counts(source_doc)
    house_after, stage_after = per_square_counts(view_doc)
    ids = [square["id"] for square in source_doc["squares"]]
    fell = {
        "house": [
            i
            for i, (a, b) in zip(ids, zip(house_before, house_after, strict=True), strict=True)
            if b < a
        ],
        "stage": [
            i
            for i, (a, b) in zip(ids, zip(stage_before, stage_after, strict=True), strict=True)
            if b < a
        ],
    }
    return {
        "measured_by": "devtools.census_atlas_contact_shades.witness_shades",
        "house": {
            "green_before": before["house_green"],
            "light_before": before["house_light"],
            "green_after": after["house_green"],
            "light_after": after["house_light"],
        },
        "stage": {
            "green_before": before["stage_green"],
            "light_before": before["stage_light"],
            "green_after": after["stage_green"],
            "light_after": after["stage_light"],
        },
        "house_counts_equal": house_before == house_after,
        "regressions": {
            rule: {"count": len(found), "ids": found[:20]} for rule, found in fell.items()
        },
    }


def _exact_rational(text: str | None) -> Fraction | None:
    """A rational literal (integer, ``p/q`` or plain decimal), or None for a symbolic form."""
    if text is None or RATIONAL_LITERAL.fullmatch(str(text).strip()) is None:
        return None
    return Fraction(str(text).strip())


def _places(text: str) -> int:
    return len(text.partition(".")[2]) if "." in text else 0


@dataclass(frozen=True, slots=True)
class Surd:
    """``a + b sqrt(k)`` with rational ``a``, ``b`` and a positive integer ``k``."""

    a: Fraction
    b: Fraction = Fraction(0)
    k: int = 1


def _surd_node(node: ast.AST, text: str) -> Surd:
    """One node of a register exact form: numbers, ``+ - * /`` and ``sqrt(integer)``."""
    if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
        return Surd(Fraction(ast.get_source_segment(text, node) or "nan"))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        inner = _surd_node(node.operand, text)
        return Surd(-inner.a, -inner.b, inner.k)
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "sqrt"
        and len(node.args) == 1
    ):
        radicand = _surd_node(node.args[0], text)
        if radicand.b or radicand.a.denominator != 1 or radicand.a <= 0:
            raise DriverError("sqrt of a non-integer")
        return Surd(Fraction(0), Fraction(1), int(radicand.a))
    if isinstance(node, ast.BinOp):
        left, right = _surd_node(node.left, text), _surd_node(node.right, text)
        if left.b and right.b and left.k != right.k:
            raise DriverError("two different radicands")
        k = left.k if left.b else right.k
        if isinstance(node.op, ast.Add | ast.Sub):
            sign = 1 if isinstance(node.op, ast.Add) else -1
            return Surd(left.a + sign * right.a, left.b + sign * right.b, k)
        if isinstance(node.op, ast.Mult) and not (left.b and right.b):
            scalar, surd = (left.a, right) if not left.b else (right.a, left)
            return Surd(scalar * surd.a, scalar * surd.b, surd.k)
        if isinstance(node.op, ast.Div) and not right.b and right.a:
            return Surd(left.a / right.a, left.b / right.a, left.k)
    raise DriverError(f"unsupported exact form near {ast.dump(node)[:40]}")


def parse_surd(form: str | None) -> Surd | None:
    """A register exact form such as ``3 + (1/2)sqrt(2)`` or ``(16+5*sqrt(2))/3``, or None
    when it is not of the form ``a + b sqrt(k)`` (``root(P_trump11, ...)``, say)."""
    if form is None:
        return None
    rational = _exact_rational(form)
    if rational is not None:
        return Surd(rational)
    text = re.sub(r"(?<=[\d)])\s*(?=sqrt|\()", "*", str(form).strip())
    try:
        tree = ast.parse(text, mode="eval")
        return _surd_node(tree.body, text)
    except SyntaxError, DriverError, ValueError:
        return None


def surd_sign(value: Fraction, surd: Surd) -> int:
    """The exact sign of ``value - (a + b sqrt(k))``."""
    u, b = value - surd.a, surd.b
    if b == 0:
        return (u > 0) - (u < 0)
    v_sign = 1 if b > 0 else -1
    u_sign = (u > 0) - (u < 0)
    if u_sign != v_sign:
        return u_sign or -v_sign
    squares = u * u - b * b * surd.k
    return u_sign * ((squares > 0) - (squares < 0))


def parse_polynomial(text: str) -> list[Fraction] | None:
    """``s^8 - 20s^7 + ... - 6865`` as coefficients, highest degree first, or None."""
    terms = re.findall(r"([+-]?)\s*(\d*)\s*(s(?:\^(\d+))?)?", text.replace(" ", ""))
    coefficients: dict[int, Fraction] = {}
    for sign, digits, variable, power in terms:
        if not digits and not variable:
            continue
        value = Fraction(int(digits) if digits else 1) * (-1 if sign == "-" else 1)
        degree = (int(power) if power else 1) if variable else 0
        coefficients[degree] = coefficients.get(degree, Fraction(0)) + value
    if not coefficients:
        return None
    top = max(coefficients)
    return [coefficients.get(degree, Fraction(0)) for degree in range(top, -1, -1)]


def compare_root(view_side: Fraction, form: str, polynomial: str | None) -> int | None:
    """The exact sign of ``view_side - root(P, value)``, with ``P`` the case's stated
    minimal polynomial and the root isolated next to ``value`` (`sqpack.field` checks
    that the interval holds exactly one root); None when that cannot be set up."""
    match = re.fullmatch(r"root\(\s*\w+\s*,\s*(-?\d+\.\d+)\s*\)", form.strip())
    coefficients = parse_polynomial(polynomial) if polynomial else None
    if match is None or coefficients is None:
        return None
    value = Fraction(match.group(1))
    unit = Fraction(1, 10 ** _places(match.group(1)))
    try:
        field = NumberField(coefficients, (value - unit, value + unit))
    except ValueError:
        return None
    return (field.rational(view_side) - field.alpha).sign()


def compare_to(
    view_side: Fraction,
    value: str | None,
    exact_form: str | None,
    polynomial: str | None = None,
) -> dict[str, Any]:
    """The view's side against a register value: exactly when its exact form is rational,
    a quadratic surd or a stated algebraic root, otherwise against the printed decimal
    widened by one unit in its last place."""
    if exact_form is not None and str(exact_form).startswith("root("):
        sign = compare_root(view_side, str(exact_form), polynomial)
        if sign is not None and value is not None:
            relation = {0: "equal", 1: "above", -1: "below"}[sign]
            difference = float(view_side - Fraction(str(value)))
            return {"relation": relation, "difference": difference, "by": "exact root"}
    surd = parse_surd(exact_form)
    if surd is not None:
        sign = surd_sign(view_side, surd)
        relation = {0: "equal", 1: "above", -1: "below"}[sign]
        approximate = mp_of(view_side) - (
            mp_of(surd.a) + mp_of(surd.b) * mp.sqrt(surd.k) if surd.b else mp_of(surd.a)
        )
        return {"relation": relation, "difference": float(approximate), "by": "exact form"}
    if value is None:
        return {"relation": "unknown", "difference": None, "by": "no value"}
    printed = Fraction(str(value))
    unit = Fraction(1, 10 ** _places(str(value)))
    difference = view_side - printed
    if difference > unit:
        relation = "above"
    elif difference < -unit:
        relation = "below"
    else:
        relation = "within-printed-precision"
    return {"relation": relation, "difference": float(difference), "by": "printed value"}


def witness_side(witness: Mapping[str, Any]) -> tuple[Fraction | FieldElement, str]:
    """``s_W`` as the regularization policy defines it, and how it was obtained.

    A rational witness's exact side; a decimal witness's 36-digit rational promotion at
    dilation 1 (`devtools.regularize_same_side.source_frame`), whose side can differ from
    the printed decimal by the promotion's rounding; a number-field witness's exact side.
    """
    read = scalar_reader(witness)
    side = read(witness["side"])
    kind = witness["scalar"]["kind"]
    if kind != "decimal":
        return side, f"the witness's exact {kind} side"
    module = _same_side_module()
    frame = getattr(module, "source_frame", None) if module is not None else None
    found = frame(witness) if frame is not None else None
    promoted = getattr(found, "side", None)
    if isinstance(promoted, Fraction):
        return promoted, "the side of the witness's 36-digit rational promotion at dilation 1"
    return side, "the printed decimal side (the promotion was unavailable)"


def side_relation(n: int, view_side: Fraction, witness: Mapping[str, Any]) -> dict[str, Any]:
    """``s_V`` against ``s_W`` (``same`` or ``solved``) and against ``U``, exactly."""
    s_w, derivation = witness_side(witness)
    if isinstance(s_w, FieldElement):
        difference = s_w.field.rational(view_side) - s_w
        sign = difference.sign()
        s_w_text = s_w.field.decimal(s_w, 40)
        delta = float(mp_of(difference))
    else:
        sign = (view_side > s_w) - (view_side < s_w)
        s_w_text = literal(s_w)
        delta = float(view_side - s_w)
    bound = verified_bound(n)
    printed = witness["side"] if isinstance(witness["side"], str) else None
    return {
        "view_side": literal(view_side),
        "view_side_decimal": decimal_digits(view_side),
        "witness_side": s_w_text,
        "witness_side_derivation": derivation,
        "printed_side": printed,
        "view_minus_printed": float(view_side - Fraction(printed)) if printed else None,
        "witness_scalar_kind": witness["scalar"]["kind"],
        "relation": "same" if sign == 0 else "solved",
        "relation_to_witness": {0: "same", 1: "above", -1: "below"}[sign],
        "view_minus_witness": delta,
        "verified_bound": bound,
        "relation_to_verified": compare_to(
            view_side, bound["value"], bound["exact_form"], bound.get("minimal_polynomial")
        ),
    }


def _same_side_module() -> ModuleType | None:
    try:
        return import_module("devtools.regularize_same_side")
    except ModuleNotFoundError:
        return None


def same_side(
    n: int, witness: Mapping[str, Any], record: Mapping[str, Any]
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """The exact re-solve of the view at the witness's side, and its witness when it holds.

    Where `devtools.regularize_same_side` exists: its `evand_view` reads the generator's
    50-digit point at ``S*`` (not the dilated certificate) back into the witness's frame,
    undoing ``orientation_g``, and its `resolve_view` snaps every rotation to one the
    witness holds exactly (or the axis) and closes the tight contacts over Q at ``s_W``,
    deciding the pose on both maintained routes. It runs with ``on_conflict="relax"``, so
    a conflicting or ill-conditioned tight contact is left open (and listed with its
    gap) rather than refused, and with the register's verified bound as a fraction where
    its exact form is rational (a surd or root form has none; the driver's own side
    relation decides those exactly). Its contract is that module's.
    """
    module = _same_side_module()
    if module is None:
        return {
            "status": "not attempted",
            "reason": "devtools.regularize_same_side is absent",
        }, None
    resolve_view = getattr(module, "resolve_view", None)
    evand_view = getattr(module, "evand_view", None)
    if resolve_view is None or evand_view is None:
        reason = "devtools.regularize_same_side lacks resolve_view or evand_view"
        return {"status": "not attempted", "reason": reason}, None
    wall = time.perf_counter()
    bound = _exact_rational(verified_bound(n)["exact_form"])
    try:
        result = resolve_view(
            witness, evand_view(record), on_conflict="relax", verified_bound=bound
        )
        found = result.summary()
    except (ArithmeticError, KeyError, TypeError, ValueError) as error:
        return {"status": "error", "reason": f"{type(error).__name__}: {error}"}, None
    resolved = getattr(result, "resolved", None)
    side_basis = found.get("side_basis") or {}
    register = found.get("register") or {}
    trimmed = _trim(found)
    summary = {
        "status": "same" if resolved is not None else "refused",
        "algorithm": getattr(module, "ALGORITHM", None),
        "on_conflict": "relax",
        "verified_bound_passed": literal(bound) if bound is not None else None,
        "fields": {
            "status": found.get("status"),
            "kind": found.get("kind"),
            "detail": found.get("detail"),
            "relaxed_count": trimmed.get("relaxed_count", 0),
            "relaxed_largest_gap": trimmed.get("relaxed_largest_gap"),
            "max_move": found.get("max_move"),
            "side_minus_printed": side_basis.get("side_minus_printed_decimal"),
            "fits_printed_side": side_basis.get("fits_printed_side"),
            "below_verified_bound": register.get("below_verified_bound"),
        },
        "result": trimmed,
        "wall_seconds": round(time.perf_counter() - wall, 3),
    }
    return summary, (dict(resolved.witness) if resolved is not None else None)


def _trim(summary: Mapping[str, Any]) -> dict[str, Any]:
    """A same-side summary with its evidence lists cut to their first few items, and each
    item's exact certificate replaced by its length (the module re-derives it)."""
    trimmed = dict(summary)
    for key in ("items", "relaxed"):
        found = trimmed.get(key)
        if isinstance(found, list):
            trimmed[f"{key}_count"] = len(found)
            gaps = [
                abs(float(item["forced_gap_decimal"]))
                for item in found
                if isinstance(item, Mapping) and "forced_gap_decimal" in item
            ]
            if gaps:
                trimmed[f"{key}_largest_gap"] = max(gaps)
            trimmed[key] = [
                {
                    name: (len(value) if isinstance(value, list) else value)
                    for name, value in item.items()
                    if name != "forced_gap"
                }
                if isinstance(item, Mapping)
                else item
                for item in found[:5]
            ]
    return trimmed


def view_witness(
    n: int,
    poses: Sequence[certificates.Pose],
    side: Fraction,
    *,
    source: Mapping[str, Any],
    variant: str,
    verified: bool,
    provenance: dict[str, Any],
) -> dict[str, Any]:
    """The imported view as a rational center-basis Witness/v2, in the source's order."""
    base = certificates.basis_witness(certificates.Certificate(n, side, tuple(poses)))
    for square, original in zip(base["squares"], source["squares"], strict=True):
        square["id"] = original["id"]
    base["id"] = f"{source['id']}-regularized-evand-{variant}"
    base["claim"] = {
        "coordinate_provenance": "verified" if verified else "reported",
        "method": "exact-algebraic",
        "limitations": (
            "A regularized derived view for drawing, not the source witness: Evan Daniel's "
            "display regularizer at the pin, run by this project from the witness, written "
            "as his dilated rational certificate (every centre scaled by 1 + 1e-20 about the "
            "origin corner, the side rounded up), and decided here on both maintained exact "
            "routes. It changes no frontier value, promotes no evidence tier, and any "
            "drawing made from it must say it is regularized."
        ),
    }
    base["certificate"] = {
        "kind": VIEW_KIND,
        "label": LABEL,
        "derived_from": source["id"],
        "derived_from_path": repo_relative(witness_path(n)),
        "generator": provenance,
    }
    return base


def import_dir(run_dir: Path, variant: str) -> Path:
    return run_dir / "import" / variant


def _refusal(row: dict[str, Any], *reasons: str) -> dict[str, Any]:
    return {**row, "classification": "refused", "reasons": list(reasons)}


def import_one(job: tuple[int, str, str]) -> dict[str, Any]:
    """Read, map back, decide and measure one count's certificate. Runs in a worker."""
    n, run_text, variant = job
    run_dir = Path(run_text)
    wall, cpu = time.perf_counter(), time.process_time()
    row: dict[str, Any] = {"n": n, "variant": variant}
    if n in certificates.HELD:
        row["held"] = HELD_NOTE
    regularized = regularize_dir(run_dir, variant)
    certificate_file = regularized / f"n-{n:03d}.cert"
    record_file = regularized / f"n-{n:03d}.json"
    if not certificate_file.is_file() or not record_file.is_file():
        exact = _row_of(exact_receipt_path(run_dir), n) or {}
        generated = _row_of(regularized / "receipt.json", n) or {}
        reason = (
            f"exact solve: {exact.get('status', 'not run')}"
            if exact.get("status") != "certified"
            else f"regularizer: {generated.get('status', 'not run')}"
            + (f" ({generated['reason']})" if generated.get("reason") else "")
        )
        refused = _refusal(row, reason)
        refused["policy"] = policy(refused)
        return _timed(refused, wall, cpu)
    record = read_json(record_file)
    certificate = certificates.parse(certificate_file.read_text(encoding="utf-8"), expected_n=n)
    g = int(record["orientation_g"])
    poses = (
        inverse_symmetry(certificate.side, certificate.poses, g)
        if g
        else list(certificate.poses)
    )
    mapped = certificates.Certificate(n, certificate.side, tuple(poses))
    row["isometry"] = {
        "orientation_g": g,
        "inverse_applied": bool(g),
        "frame": "source" if g == 0 else f"source, after undoing reg.d4 g = {g}",
    }
    decided = certificates.decide(mapped)
    routes = {
        "exact_verify": decided["exact_verify"]["passed"],
        "independent": decided["independent"]["passed"],
    }
    view_poses = [(pose.x, pose.y, *pose.basis) for pose in mapped.poses]
    area = area_route(mapped.side, view_poses)
    row["decision"] = {
        **routes,
        "area": area["passed"],
        "both": all(routes.values()),
        "all": all(routes.values()) and area["passed"],
        "minimum_best_pair_gap": decided["exact_verify"]["minimum_best_pair_gap"],
        "minimum_containment_clearance": decided["exact_verify"][
            "minimum_containment_clearance"
        ],
        "cpu_seconds": {
            "exact_verify": decided["exact_verify"]["cpu_seconds"],
            "independent": decided["independent"]["cpu_seconds"],
            "area": area["cpu_seconds"],
        },
    }
    witness = load_known_best(n)
    ids = [square["id"] for square in witness["squares"]]
    source = source_placed(witness)
    row["identity"] = identity((mapped.side, view_poses), source, ids)
    solved = solved_angles(run_dir, n)
    unnamed, by_solve = unnamed_turns(view_poses, source[1], record, ids, solved)
    row["identity"]["unnamed_turn_ids"] = unnamed
    row["identity"]["exact_solve_turn_ids"] = by_solve
    provenance = {
        "source": SOURCE,
        "revision": revision(),
        "method": "reg.regularize via devtools.regularize_evand_shim",
        "policy": record["policy"],
        "style": record["style"],
        "orient_argument": record["orient_argument"],
        "level": record["level"],
        "level_text": record["level_text"],
        "groups": f"{record['groups_before']} -> {record['groups_after']}",
        "symmetry_imposed": record["symmetry"],
        "angle_changes": record["angle_changes"],
        "S_exact": record["S_exact"],
    }
    view = view_witness(
        n, mapped.poses, mapped.side, source=witness, variant=variant,
        verified=row["decision"]["both"], provenance=provenance,
    )  # fmt: skip
    out = import_dir(run_dir, variant)
    out.mkdir(parents=True, exist_ok=True)
    view_file = out / f"n-{n:03d}-view.yaml"
    view_file.write_text(witness_document(view, schema="witness.schema.yaml"), encoding="utf-8")
    row["view"] = view_file.relative_to(run_dir).as_posix()
    row["shades"] = shade_measure(witness_path(n), view_file)
    row["side"] = side_relation(n, mapped.side, witness)
    row["same_side"], resolved = same_side(n, witness, record)
    if resolved is not None:
        same_file = out / f"n-{n:03d}-same-side.yaml"
        same_file.write_text(
            witness_document(resolved, schema="witness.schema.yaml"), encoding="utf-8"
        )
        row["same_side"]["view"] = same_file.relative_to(run_dir).as_posix()
        same_side_, same_placed = source_placed(resolved)
        row["same_side"]["identity"] = identity((same_side_, same_placed), source, ids)
        unnamed, by_solve = unnamed_turns(same_placed, source[1], record, ids, solved)
        row["same_side"]["identity"]["unnamed_turn_ids"] = unnamed
        row["same_side"]["identity"]["exact_solve_turn_ids"] = by_solve
        row["same_side"]["shades"] = shade_measure(witness_path(n), same_file)
        row["same_side"]["side"] = side_relation(n, same_side_, witness)
        verification = (row["same_side"].get("result") or {}).get("verification") or {}
        row["same_side"]["decision"] = {
            "exact_verify": bool((verification.get("exact_verify") or {}).get("passed")),
            "independent": bool((verification.get("independent") or {}).get("passed")),
            "area": area_route(same_side_, same_placed)["passed"],
            "decided_by": "the two maintained routes as regularize_same_side ran them; the "
            "area route here",
        }
        row["same_side"]["decision"]["all"] = all(
            row["same_side"]["decision"][route] for route in ROUTES
        )
        row["same_side"]["pose_equals_witness"] = pose_equals_witness(resolved, witness)
    row["generator"] = {
        key: record[key]
        for key in (
            "level",
            "level_text",
            "groups_before",
            "groups_after",
            "symmetry",
            "policy",
        )
    }
    row["generator"]["determined_merges"] = [
        change for change in record["angle_changes"] or [] if change[0] == "determined-merge"
    ]
    row["generator"]["symmetry_dropped_for_coincidence"] = (record.get("report") or {}).get(
        "sym_dropped_for_coincidence"
    )
    classified = classify(row)
    classified["policy"] = policy(classified)
    return _timed(classified, wall, cpu)


ROUTES = ("exact_verify", "independent", "area")
#: A square counts as turned when the sine of its turn exceeds this (policy, section 3).
TURN_SINE = Fraction(1, 10**6)
#: Degrees within which a turned square's angles match a recorded angle change.
ANGLE_MATCH_DEGREES = 1e-5
#: The provisional move bound for automatic admission (policy, section 3).
MOVE_BOUND = 0.5
#: The recorded angle changes that move a group from one angle to another.
GROUP_MOVES = ("free-angle", "determined-merge", "ulp-merge")


def area_route(side: Fraction, placed: Sequence[Placed]) -> dict[str, Any]:
    """The third route, `check_half_angle_area.decide_placed`: each close pair clipped and
    required to meet in area zero, each square held inside the closed box."""
    started = time.process_time()
    try:
        decision = decide_placed(side, placed)
    except AreaRouteError as error:
        return {"passed": False, "error": str(error), "cpu_seconds": 0.0}
    return {
        "passed": decision.passed,
        "overlapping_pairs": decision.overlapping,
        "outside_squares": decision.outside,
        "cpu_seconds": round(time.process_time() - started, 3),
    }


def _fold(degrees: float) -> float:
    folded = degrees % 90.0
    return folded - 90.0 if folded > 45.0 else folded


def _close(left: float, right: float) -> bool:
    return abs(_fold(left - right)) < ANGLE_MATCH_DEGREES


def _named(
    start: list[float], target: float, edges: list[tuple[float, float]], *, straighten: bool
) -> bool:
    """Whether the recorded angle changes take a square from one of ``start`` to ``target``."""
    frontier: list[float] = list(start)
    seen: list[float] = []
    while frontier:
        angle = frontier.pop()
        if _close(angle, target):
            return True
        if any(_close(angle, other) for other in seen):
            continue
        seen.append(angle)
        frontier.extend(to for origin, to in edges if _close(origin, angle))
        if straighten and 0 < abs(angle) < 1.0 + ANGLE_MATCH_DEGREES:
            frontier.append(0.0)
    return False


def solved_angles(run_dir: Path, n: int) -> list[float] | None:
    """Each square's angle, degrees folded into (-45, 45], at the exact solve's point."""
    path = work_dir(run_dir, n) / "witness.exact.txt"
    if not path.is_file():
        return None
    rows = [line.split() for line in path.read_text(encoding="utf-8").splitlines()[1:]]
    return [_fold(float(row[2])) for row in rows if len(row) == 3]


def unnamed_turns(
    view: Sequence[Placed],
    source: Sequence[Placed],
    record: Mapping[str, Any],
    ids: Sequence[Any],
    solved: Sequence[float] | None = None,
) -> tuple[list[Any], list[Any]]:
    """The squares turned by more than `TURN_SINE` that the run's records do not name
    (policy, section 3, obligation 3), and those turned by the exact solve alone.

    A turn is named when the generator's records take the square's angle to its view
    angle: its free-square reassignment (``reg.merge_angles``, by square), then any chain
    of group moves (``free-angle``, ``determined-merge``, ``ulp-merge``, from angle to
    angle) and, where the run straightened near-axis groups, a group within one degree of
    the axis to the axis. The records are written against the exact solve's point, whose
    angles (``solved``, from its ``.exact.txt``) can differ from the witness's: a square
    the exact solve turned and the regularizer left is reported apart, as turned by the
    exact solve alone, and not as unnamed. Angles match within `ANGLE_MATCH_DEGREES`.
    """
    changes = record.get("angle_changes") or []
    edges = [
        (_fold(float(change[1])), _fold(float(change[2])))
        for change in changes
        if change[0] in GROUP_MOVES and len(change) >= 3
    ]
    straighten = any(change[0] == "free-angle straighten" for change in changes)
    reassigned = {
        int(item[0]): _fold(float(item[2])) for item in record.get("free_merges") or []
    }
    unnamed: list[Any] = []
    by_solve: list[Any] = []
    for index, (a, b) in enumerate(zip(view, source, strict=True)):
        c, s, sc, ss = rounded(a[2]), rounded(a[3]), rounded(b[2]), rounded(b[3])
        if min(abs(c * ss - s * sc), abs(c * sc + s * ss)) <= TURN_SINE:
            continue
        target = _fold(math.degrees(math.atan2(float(s), float(c))))
        origin = _fold(math.degrees(math.atan2(float(ss), float(sc))))
        at_solve = solved[index] if solved is not None else origin
        if index not in reassigned and _close(at_solve, target):
            by_solve.append(ids[index])
            continue
        start = [origin, at_solve] + ([reassigned[index]] if index in reassigned else [])
        if not _named(start, target, edges, straighten=straighten):
            unnamed.append(ids[index])
    return unnamed, by_solve


def pose_equals_witness(view: Mapping[str, Any], witness: Mapping[str, Any]) -> bool | None:
    """Whether a same-side view is exactly the witness's own pose (policy row 5): the
    rational frame `regularize_same_side.source_frame` derives, centre for centre and
    rotation for rotation up to a quarter turn. None when no rational frame exists."""
    module = _same_side_module()
    frame = getattr(module, "source_frame", None) if module is not None else None
    found = frame(witness) if frame is not None else None
    centres, rotations = getattr(found, "centres", None), getattr(found, "rotations", None)
    if centres is None or rotations is None:
        return None
    for square, centre, (c, s) in zip(view["squares"], centres, rotations, strict=True):
        if tuple(Fraction(str(value)) for value in square["center"]) != tuple(centre):
            return False
        basis = tuple(Fraction(str(value)) for value in square["basis"])
        if basis not in {(c, s), (-s, c), (-c, -s), (s, -c)}:
            return False
    return True


def _policy_entry(number: int, decision: str, record: str) -> dict[str, Any]:
    return {"row": number, "decision": decision, "record": record}


def policy_row(output: Mapping[str, Any]) -> dict[str, Any]:  # noqa: PLR0911 -- one per row
    """The first row of the policy's decision table (section 4) one output falls in.

    ``output`` carries what the rows read: whether the output exists and why not, its
    route verdicts, its side relation (``same`` or ``solved``) and relation to ``U``, its
    identity (one to one, unnamed turns, largest move), its regressions, whether its pose
    is the witness's own, and the generator's variant, level and determined merges.
    """
    entry = _policy_entry
    if not output.get("exists"):
        return entry(1, f"refuse: {output.get('status')}", "refused, generator-failed")
    if not all(output["decision"].get(route) for route in ROUTES):
        failed = ", ".join(route for route in ROUTES if not output["decision"].get(route))
        return entry(2, f"refuse, open a defect bead ({failed})", "refused, invalid")
    to_verified = output["side"]["relation_to_verified"]["relation"]
    if to_verified == "below":
        return entry(3, "register-result candidate; no drawing until registered", "receipt")
    if to_verified not in {"above", "equal"}:
        return entry(9, f"review: s_V against U is {to_verified}", "review queue")
    if output["side"]["relation"] != "same":
        return entry(4, "refuse as a drawing frame", "refused, dilated-side")
    if output.get("pose_equals_witness"):
        return entry(5, "no view", "unchanged")
    found = output["identity"]
    if not found["one_to_one"] or not found["order_preserved"]:
        return entry(6, "refuse as the packing; gallery alternate", "refused, not-one-to-one")
    if found.get("unnamed_turn_ids"):
        return entry(6, "refuse as the packing; gallery alternate", "refused, unnamed-turn")
    if any(rule["count"] for rule in output["shades"]["regressions"].values()):
        return entry(7, "refuse", "refused, regression")
    generator = output["generator"]
    if generator.get("determined_merges") or generator.get("level") == 3:
        return entry(8, "alternate: review only, never drawn as the packing", "review queue")
    if generator.get("policy") != "conservative":
        return entry(8, f"alternate: variant {generator.get('policy')}", "review queue")
    if found["max_move"] > MOVE_BOUND:
        return entry(9, f"review: a square moved {found['max_move']:.3g} > 1/2", "review queue")
    return entry(10, "admit", "regularized")


#: The word each decision-table row is reported in (policy, section 4, "How a decision
#: is reported"), before the "no change" override.
REPORTS = {
    1: "no view",
    2: "refused",
    3: "held",
    4: "held",
    5: "no change",
    6: "refused",
    7: "refused",
    8: "alternate",
    9: "review",
    10: "admitted",
}
#: The rows a view that draws the same picture is reported under as "no change".
NO_CHANGE_ROWS = frozenset({3, 4, 5, 6, 7, 10})


def visible_change(output: Mapping[str, Any]) -> bool:
    """Whether the view would draw a different picture: a square moved beyond 1e-3 or
    turned (sine above 1e-6), or the angle classes or the house counts differ."""
    found, shades_ = output["identity"], output["shades"]
    return bool(
        found["moved"].get("0.001")
        or found.get("turned_beyond_sine_1e-6")
        or not found.get("angle_classes_equal", True)
        or not shades_.get("house_counts_equal", True)
    )


def reported(output: Mapping[str, Any], entry: dict[str, Any]) -> dict[str, Any]:
    """The decision-table entry with the word it is reported in and the reason shown."""
    number = entry["row"]
    changes = bool(output.get("exists")) and visible_change(output)
    label = REPORTS[number]
    if number in NO_CHANGE_ROWS and output.get("exists") and not changes:
        label = "no change"
    reason = entry["decision"]
    if number == 3:
        difference = output["side"]["relation_to_verified"].get("difference")
        reason = f"register result first: s_V < U ({difference:+.2g})"
    elif number == 4:
        reason = (
            "a side the record does not hold: dilated certificate, s_V - s_W = "
            f"{output['side']['view_minus_witness']:+.2g}"
        )
    if label == "no change" and number == 3:
        reason += "; still a register-result candidate"
    return {**entry, "report": label, "reason": reason, "visible_change": changes}


def policy(row: Mapping[str, Any]) -> dict[str, Any]:
    """The decision-table rows of a count's two outputs, the certificate and the same-side
    view, each classified on its own, and the row the count's drawing falls in."""
    generator = row.get("generator") or {}
    certificate: dict[str, Any] = {
        "exists": "decision" in row,
        "status": "; ".join(row.get("reasons") or []),
    }
    if certificate["exists"]:
        certificate.update(
            {key: row[key] for key in ("decision", "side", "identity", "shades")}
        )
        certificate.update(generator=generator, pose_equals_witness=False)
    same = row.get("same_side") or {}
    if same.get("status") == "same" and same.get("decision"):
        resolved: dict[str, Any] = {
            "exists": True,
            **{key: same[key] for key in ("decision", "side", "identity", "shades")},
            "generator": generator,
            "pose_equals_witness": same.get("pose_equals_witness"),
        }
    else:
        result = same.get("result") or {}
        reason = result.get("kind") or same.get("reason") or same.get("status") or "not run"
        resolved = {"exists": False, "status": f"same side {same.get('status')}: {reason}"}
    rows = {
        "certificate": reported(certificate, policy_row(certificate)),
        "same_side": reported(resolved, policy_row(resolved)),
    }
    drawing = rows["same_side"] if resolved["exists"] else rows["certificate"]
    return {
        **rows,
        "drawing": drawing,
        "drawing_from": "same_side" if resolved["exists"] else "certificate",
        "report": drawing["report"],
        "row": drawing["row"],
        "register_candidate": any(found["row"] == 3 for found in rows.values()),
        "table": "docs/project/policies/regularization-policy.md#the-decision-table",
    }


ADMISSION = {
    "below": (
        "a dilated certificate below the verified bound: a register result, not yet a "
        "drawing frame"
    ),
    "above": (
        "a dilated certificate above the verified bound: not a drawing frame under the "
        "2026-10-02 atlas policy"
    ),
}


def certificate_reasons(row: Mapping[str, Any]) -> list[str]:
    """Why the dilated certificate's view may not be drawn: the obligations of the
    assessment's sections 3.1, 3.3 and 3.4 that it fails."""
    reasons: list[str] = []
    decision = row["decision"]
    failed = [route for route in ROUTES if not decision.get(route)]
    if failed:
        reasons.append(f"not exactly a packing on {', '.join(failed)}")
    if not row["identity"]["one_to_one"]:
        reasons.append("no container symmetry pairs nearest centres one to one")
    elif not row["identity"]["order_preserved"]:
        reasons.append("the square order is not preserved")
    fell = {
        rule: found["count"]
        for rule, found in row["shades"]["regressions"].items()
        if found["count"]
    }
    if fell:
        reasons.append(f"contact counts fell: {fell}")
    return reasons


def classify(row: dict[str, Any]) -> dict[str, Any]:
    """``same``, ``solved`` or ``refused``.

    ``same`` when the exact same-side re-solve holds and is drawable, or when the
    certificate's own side is the witness's; ``refused`` when the certificate's view
    fails an obligation; otherwise ``solved``, a dilated certificate, with what its side
    relation to the verified bound means for admission.
    """
    reasons = certificate_reasons(row)
    row["certificate_reasons"] = reasons
    if (row.get("generator") or {}).get("determined_merges"):
        row["alternate"] = ALTERNATE
    same = row["same_side"]
    if same.get("status") == "same":
        same["reasons"] = _same_side_reasons(same)
        if not same["reasons"]:
            relation = same["side"]["relation_to_verified"]["relation"]
            admission = SAME_ADMISSION.get(
                relation, f"an exact view at the witness's side, {relation} the verified bound"
            )
            return {**row, "classification": "same", "admission": admission}
    if reasons:
        return _refusal(row, *reasons)
    if row["side"]["relation_to_witness"] == "same":
        return {**row, "classification": "same"}
    relation = row["side"]["relation_to_verified"]["relation"]
    admission = ADMISSION.get(relation, f"a dilated certificate, {relation} the verified bound")
    return {**row, "classification": "solved", "admission": admission}


#: The assessment's recommendation on `fewest` merges of determined groups (owner
#: question 2): measured like every view, never drawn as the same packing in the
#: project's own voice.
ALTERNATE = (
    "the generator merged determined rotation groups (fewest): an alternate arrangement "
    "at the record side, not the same packing in the project's voice, whatever is measured"
)

SAME_ADMISSION = {
    "below": (
        "an exact view at the witness's printed side, below the verified bound: a drawing "
        "frame, and a new verified upper bound (a register result and an owner decision)"
    ),
    "equal": (
        "an exact view at the witness's side, which is the verified bound: a drawing frame"
    ),
    "above": (
        "an exact view at the witness's printed side, above the verified bound (the printed "
        "decimal rounds the optimum up): a drawing frame at that side, as the project layer "
        "draws"
    ),
}


def _same_side_reasons(same: Mapping[str, Any]) -> list[str]:
    """Why a same-side re-solve, exact as it is, would still not be drawn: its side is
    not the witness's (a decimal witness's 36-digit promotion can sit above the printed
    side), or its pose fails identity or loses contacts."""
    reasons: list[str] = []
    failed = [route for route in ROUTES if not (same.get("decision") or {}).get(route)]
    if failed:
        reasons.append(f"the same-side pose is refused on {', '.join(failed)}")
    side = same["side"]
    if side["relation_to_witness"] != "same":
        relation, by = side["relation_to_witness"], side["view_minus_witness"]
        reasons.append(
            f"the re-solve holds at the witness's rational frame side, {relation} its "
            f"printed side by {by:.2g}"
        )
    if not same["identity"]["one_to_one"] or not same["identity"]["order_preserved"]:
        reasons.append("the same-side pose is not the source's squares in order")
    fell = {rule: found["count"] for rule, found in same["shades"]["regressions"].items()}
    if any(fell.values()):
        reasons.append(f"the same-side pose loses contacts: {fell}")
    return reasons


def _timed(row: dict[str, Any], wall: float, cpu: float) -> dict[str, Any]:
    return {
        **row,
        "wall_seconds": round(time.perf_counter() - wall, 3),
        "cpu_seconds": round(time.process_time() - cpu, 3),
    }


def _row_of(path: Path, n: int) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    return next((row for row in read_json(path)["rows"] if row["n"] == n), None)


def stage_import(
    counts: Sequence[int], run_dir: Path, *, variant: str, procs: int
) -> dict[str, Any]:
    header = {
        "format": FORMAT,
        "stage": "import",
        "tool": f"{GENERATOR} import",
        "what": (
            "Each regularized certificate mapped to the source frame, decided on both "
            "maintained exact routes, measured against its source witness, and classified."
        ),
        "variant": variant,
        "procs": procs,
        "host": host(),
    }
    jobs = [(n, str(run_dir), variant) for n in sorted(counts, reverse=True)]
    if procs <= 1 or len(jobs) <= 1:
        found = [import_one(job) for job in jobs]
    else:
        with ProcessPoolExecutor(max_workers=procs) as pool:
            found = list(pool.map(import_one, jobs))
    header["host_after"] = host()
    rows = sorted(found, key=lambda row: row["n"])
    return _merge_receipt(import_dir(run_dir, variant) / "receipt.json", header, rows)


# --------------------------------------------------------------------------------------
# Stage 5: drawings and the summary
# --------------------------------------------------------------------------------------

PANEL = 360
MARGIN = 14
CAPTION = 60
LINE = 13
#: Outline of a square that moved, and the dot marking one that turned.
HIGHLIGHT = "#d81b60"
TURNED = "#1e40af"


@dataclass(frozen=True, slots=True)
class Panel:
    """One column of a comparison: a packing (or none), its caption and its measures,
    and the witness ids of the squares that moved and that turned."""

    witness: dict[str, Any] | None
    caption: tuple[str, ...]
    measures: tuple[str, ...] = ()
    moved: frozenset[str] = frozenset()
    turned: frozenset[str] = frozenset()


def _frame(witness: dict[str, Any]) -> Any:
    from devtools.build_known_best_atlas import frame_from_witness  # noqa: PLC0415

    return frame_from_witness(witness)


def _draw(panel: Panel, frame: Any, origin: tuple[float, float], scale: float) -> list[str]:
    """One packing at ``scale`` px per unit with the house renderer's fills; squares that
    moved outlined, squares that turned marked with a dot."""
    from sqpack.render.color import assign_square_colors  # noqa: PLC0415
    from sqpack.render.model import RenderSpec  # noqa: PLC0415

    assert panel.witness is not None
    colors = assign_square_colors(frame, RenderSpec(overlays=frozenset()))
    x0, top = origin[0] + MARGIN, origin[1] + CAPTION
    side = float(frame.container_side.projected)
    parts = [
        (
            f'<rect x="{x0:.2f}" y="{top:.2f}" width="{side * scale:.2f}" '
            f'height="{side * scale:.2f}" fill="#ffffff" stroke="#222222" stroke-width="1"/>'
        )
    ]
    dots: list[str] = []
    for square, record in zip(frame.squares, panel.witness["squares"], strict=True):
        corners = [
            (x0 + float(p.x.projected) * scale, top + (side - float(p.y.projected)) * scale)
            for p in square.corners
        ]
        points = " ".join(f"{x:.3f},{y:.3f}" for x, y in corners)
        ident = str(record["id"])
        stroke = (
            f'stroke="{HIGHLIGHT}" stroke-width="2.2"'
            if ident in panel.moved
            else 'stroke="#333333" stroke-width="0.4"'
        )
        parts.append(
            f'<polygon points="{points}" fill="{colors[square.square_id].fill}" {stroke}/>'
        )
        if ident in panel.turned:
            cx = sum(x for x, _ in corners) / 4
            cy = sum(y for _, y in corners) / 4
            radius = max(1.6, 0.14 * scale)
            dots.append(
                f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{radius:.2f}" fill="{TURNED}" '
                'stroke="#ffffff" stroke-width="0.6"/>'
            )
    return parts + dots


def _text(x: float, y: float, line: str, *, size: int = 10, fill: str = "#222222") -> str:
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" font-family="sans-serif" '
        f'fill="{fill}">{escape(line)}</text>'
    )


def _caption(x: float, y: float, lines: Sequence[str]) -> list[str]:
    """A larger first line and smaller detail lines, from ``y`` down."""
    return [
        _text(x, y + 16 + 14 * k, line, size=12 if k == 0 else 10)
        for k, line in enumerate(lines)
    ]


def comparison_svg(n: int, panels: Sequence[Panel], footer: Sequence[str]) -> str:
    """The panels side by side at one scale and in the source's orientation, each with its
    measures beneath, and the footer: self-contained SVG, no script, generic fonts."""
    frames = [_frame(panel.witness) if panel.witness is not None else None for panel in panels]
    sides = [float(frame.container_side.projected) for frame in frames if frame is not None]
    scale = (PANEL - 2 * MARGIN) / max(sides)
    width = PANEL * len(panels)
    measures_top = CAPTION + PANEL - MARGIN + 14
    longest = max((len(panel.measures) for panel in panels), default=0)
    footer_top = measures_top + LINE * longest + 10
    height = footer_top + 16 * len(footer) + 8
    body: list[str] = []
    for k, (panel, frame) in enumerate(zip(panels, frames, strict=True)):
        body.extend(_caption(PANEL * k + MARGIN, 0.0, panel.caption))
        if frame is not None:
            body.extend(_draw(panel, frame, (PANEL * k, 0.0), scale))
        body.extend(
            _text(PANEL * k + MARGIN, measures_top + LINE * j, _short(line, 62))
            for j, line in enumerate(panel.measures)
        )
    body.extend(
        _text(MARGIN, footer_top + 16 * j, line, fill="#444444")
        for j, line in enumerate(footer)
    )
    title = f"n = {n}: source witness and {LABEL} views"
    description = (
        f"Drawings of n = {n} at one scale and in the source's orientation: the retained "
        f"known-best witness, the project's {LABEL} view where its atlas layer keeps one, "
        f"and the {LABEL} views made by Evan Daniel's process at the pin and decided here, "
        "each with its measures and its row of the regularization policy's decision table. "
        "Outlined squares moved, dotted squares turned, against the source witness. Each "
        "derived view is a drawing, not the source witness; it changes no side, frontier "
        "value or evidence tier."
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height:.0f}" '
        f'viewBox="0 0 {width} {height:.0f}" role="img">'
        f"<title>{escape(title)}</title><desc>{escape(description)}</desc>"
        f'<rect width="100%" height="100%" fill="#fafafa"/>' + "".join(body) + "</svg>\n"
    )


def house_svg(
    n: int, view: dict[str, Any], source: dict[str, Any], variant: str, *, same: bool
) -> str:
    """The view alone, drawn by the house renderer as `render_regularized_atlas` draws
    the project's views, under the record's evidence tier."""
    from sqpack.render import render_packing_svg  # noqa: PLC0415
    from sqpack.render.model import RenderSpec  # noqa: PLC0415

    side = (
        "re-solved exactly at the witness's own side"
        if same
        else "its side is the generator's dilated certificate's, not the witness's"
    )
    record = _frame(source)
    frame = replace(
        _frame(view),
        evidence=record.evidence,
        check=record.check,
        label=f"n={n} {LABEL}",
        source_id=str(view["id"]),
        source_url=record.source_url,
    )
    return render_packing_svg(
        frame,
        spec=RenderSpec(
            overlays=frozenset(),
            title=f"Known-best packing of {n} unit squares, {LABEL} (Evan Daniel's process)",
            description=(
                f"A {LABEL} derived view of the retained known-best n={n} construction, "
                f"never the source witness: Evan Daniel's display regularizer ({variant}) at "
                f"{revision()[:7]}, run here and decided over the rationals on three exact "
                f"routes; {side}. It changes no frontier value or evidence tier; the "
                "evidence stated is the record's."
            ),
        ),
    )


def _layer_view(n: int) -> dict[str, Any] | None:
    import gzip  # noqa: PLC0415

    entry = layer_entry(n)
    if entry is None or entry["status"] != "regularized":
        return None
    data = gzip.decompress((REPO / entry["view"]["path"]).read_bytes()).decode("utf-8")
    return load_yaml(data)["witness"]


def _side_text(witness: Mapping[str, Any]) -> str:
    side = scalar_reader(witness)(witness["side"])
    if isinstance(side, FieldElement):
        return side.field.decimal(side, 22)
    return decimal_digits(side, 22)


def _short(text: str, limit: int = 58) -> str:
    return text if len(text) <= limit else text[: limit - 3] + "..."


def _ok(value: object) -> str:
    return "ok" if value else "NO"


def _routes(decision: Mapping[str, Any] | None) -> str:
    if not decision:
        return "-"
    return ", ".join(f"{name} {_ok(decision.get(route))}" for route, name in ROUTE_NAMES)


ROUTE_NAMES = (("exact_verify", "exact_verify"), ("independent", "indep"), ("area", "area"))


def _relation_text(side: Mapping[str, Any] | None) -> str:
    """``s_V - s_W`` as a short signed decimal and the relation to ``U``."""
    if not side:
        return "-"
    to_verified = side["relation_to_verified"]
    difference = to_verified.get("difference")
    to_u = f"{to_verified['relation']} U" + (
        f" ({difference:+.2g})" if difference is not None else ""
    )
    return f"{side['relation']}: s_V - s_W = {side['view_minus_witness']:+.2g}; {to_u}"


def _identity_lines(found: Mapping[str, Any] | None) -> list[str]:
    if not found:
        return ["identity: -"]
    pairing = "one to one" if found["one_to_one"] and found["order_preserved"] else "NOT 1:1"
    unnamed = found.get("unnamed_turn_ids") or []
    return [
        (
            f"identity: {pairing}, moved > 1e-3: {found['moved'].get('0.001')}, "
            f"max move {found['max_move']:.3g}"
        ),
        f"max turn {found['max_turn_degrees']:.3g} deg; unnamed turns {len(unnamed)}, "
        f"by exact solve {len(found.get('exact_solve_turn_ids') or [])}"
        + (f" ({', '.join(map(str, unnamed[:6]))})" if unnamed else ""),
    ]


def _shade_line(shades_: Mapping[str, Any] | None) -> str:
    if not shades_:
        return "shades: -"
    house, stage = shades_["house"], shades_["stage"]
    fell = shades_["regressions"]
    return (
        f"light: house {house['light_before']}->{house['light_after']}, stage "
        f"{stage['light_before']}->{stage['light_after']}; fell h{fell['house']['count']} "
        f"s{fell['stage']['count']}"
    )


def _seconds_text(row: Mapping[str, Any] | None) -> str:
    if not row or row.get("wall_seconds") is None:
        return "-"
    return f"{row['wall_seconds']:.3g}"


def _source_panel(n: int, run_dir: Path, source: dict[str, Any]) -> Panel:
    inputs = _row_of(inputs_dir(run_dir) / "receipt.json", n) or {}
    exact = _row_of(exact_receipt_path(run_dir), n) or {}
    s_w, derivation = witness_side(source)
    s_w_text = (
        s_w.field.decimal(s_w, 24) if isinstance(s_w, FieldElement) else decimal_digits(s_w, 24)
    )
    bound = verified_bound(n)
    free = exact.get("free_squares") or []
    measures = [
        f"{inputs.get('scalar_kind', source['scalar']['kind'])}, {source['representation']}",
        f"s_W {s_w_text}",
        f"  ({_short(derivation, 56)})",
        f"U {str(bound['value'])[:24]} = {_short(str(bound['exact_form']), 34)}",
        f"exact solve: {exact.get('status', 'not run')}"
        + (
            f", S* - printed {exact['S_exact_minus_printed']:+.2g}"
            if exact.get("S_exact_minus_printed") is not None
            else ""
        ),
        f"free squares (0-based): {len(free)}"
        + (f" ({', '.join(map(str, free[:8]))})" if free else ""),
    ]
    return Panel(
        source,
        (f"source witness {source['id']}", f"side {_side_text(source)}"),
        tuple(measures),
    )


def _layer_panel(n: int, source: dict[str, Any]) -> Panel:
    entry = layer_entry(n) or {}
    view = _layer_view(n)
    status = layer_status(n)
    if view is None:
        detail = status.get("refusal") or status["status"]
        return Panel(None, ("project layer: no view", f"({status['status']}: {detail})"))
    found = identity(
        source_placed(view), source_placed(source), [s["id"] for s in source["squares"]]
    )
    house, stage = entry["shades"]["house"], entry["shades"]["stage"]
    residual = entry.get("non_regression", {}).get("residual_regressions", {})
    measures = [
        f"status {entry['status']}, changed squares {entry.get('changed_squares')}",
        f"largest move {entry.get('moves', {}).get('largest_move_decimal')}",
        (
            f"light: house {house['light_before']}->{house['light_after']}, stage "
            f"{stage['light_before']}->{stage['light_after']}; residual {residual}"
        ),
        f"side: view - reported {entry.get('side', {}).get('view_minus_reported')}",
        *_identity_lines(found),
    ]
    return Panel(
        view,
        (f"project layer: {LABEL}", "regularize_axis_components/2, side unchanged"),
        tuple(measures),
        frozenset(map(str, found["moved_ids"])),
        frozenset(map(str, found["turned_ids"])),
    )


def _variant_panel(n: int, run_dir: Path, variant: str) -> tuple[Panel, dict[str, Any] | None]:
    """The panel of a view made here, and the witness to draw alone if it is drawable.

    A count whose same-side re-solve holds is drawn from that exact pose at ``s_W``; any
    other from the dilated certificate the generator wrote. The measures name the
    decision-table rows of both outputs.
    """
    title = f"Evan Daniel's process: {LABEL} ({variant})"
    generated = _row_of(regularize_dir(run_dir, variant) / "receipt.json", n) or {}
    row = _row_of(import_dir(run_dir, variant) / "receipt.json", n)
    seconds = f"seconds: regularize {_seconds_text(generated)}, import {_seconds_text(row)}"
    if row is None or "view" not in row:
        reasons = "; ".join(row.get("reasons", [])) if row else "not imported"
        rules = (row or {}).get("policy") or {}
        drawing = rules.get("drawing") or {}
        measures = (
            (
                f"{drawing.get('report', 'no view')} (row {drawing.get('row', '-')}): "
                f"{drawing.get('reason', reasons)}"
            ),
            seconds,
        )
        return Panel(None, (title, "no view", _short(reasons)), measures), None
    rules = row.get("policy") or {}
    same = row.get("same_side") or {}
    use_same = bool(same.get("view")) and (rules.get("same_side") or {}).get("row", 1) != 1
    chosen = same if use_same else row
    generator = row.get("generator") or {}
    regularize = generated
    kind = "same-side pose at s_W" if use_same else "dilated certificate"
    drawing, certificate = rules.get("drawing") or {}, rules.get("certificate") or {}
    fields = same.get("fields") or {}
    if same.get("status") == "same":
        opened = fields.get("relaxed_count")
        same_text = "same side: holds" + (
            f", {opened} contacts left open <= {fields.get('relaxed_largest_gap') or 0:.2g}"
            if opened
            else ""
        )
        same_detail = (
            f"  max move {fields.get('max_move')}, side - printed "
            f"{fields.get('side_minus_printed')}, fits {fields.get('fits_printed_side')}, "
            f"below U {fields.get('below_verified_bound')}"
        )
    else:
        same_text = (
            f"same side: {same.get('status')} ({fields.get('kind') or same.get('reason')})"
        )
        same_detail = f"  {_short(str(fields.get('detail') or ''), 58)}"
    measures = [
        (
            f"{str(drawing.get('report')).upper()} (row {drawing.get('row')}): "
            f"{drawing.get('reason')}"
        ),
        (
            f"  index: {drawing.get('record')}; certificate: {certificate.get('report')} "
            f"(row {certificate.get('row')})"
        ),
        (
            f"level {generator.get('level')}, groups {generator.get('groups_before')} -> "
            f"{generator.get('groups_after')}, shape {regularize.get('shape')}"
        ),
        (
            f"symmetry imposed {generator.get('symmetry') or 'none'}, dropped "
            f"{regularize.get('symmetry_dropped_for_coincidence') or 'none'}"
        ),
        f"certificate {_relation_text(row.get('side'))}",
        f"certificate routes: {_routes(row.get('decision'))}",
        _short(same_text, 62),
        same_detail,
    ]
    if use_same:
        measures += [
            f"same-side pose {_relation_text(same.get('side'))}",
            f"same-side routes: {_routes(same.get('decision'))}",
        ]
    measures += [
        *_identity_lines(chosen.get("identity")),
        _shade_line(chosen.get("shades")),
        seconds,
    ]
    view = load_yaml((run_dir / chosen["view"]).read_text(encoding="utf-8"))["witness"]
    found = chosen["identity"]
    panel = Panel(
        view,
        (
            title,
            f"{kind}, side {chosen['side']['view_side_decimal'][:22]}",
            f"reported: {drawing.get('report')} (row {drawing.get('row')})",
        ),
        tuple(measures),
        frozenset(map(str, found["moved_ids"])),
        frozenset(map(str, found["turned_ids"])),
    )
    drawable = row["classification"] != "refused"
    return panel, (view if drawable else None)


def render_one(n: int, run_dir: Path, out: Path, variants: Sequence[str]) -> dict[str, Any]:
    wall, cpu = time.perf_counter(), time.process_time()
    source = load_known_best(n)
    drawn: dict[str, Any] = {}
    panels = [_source_panel(n, run_dir, source), _layer_panel(n, source)]
    for variant in variants_of(run_dir, n, variants):
        panel, house = _variant_panel(n, run_dir, variant)
        panels.append(panel)
        path = out / f"n-{n:03d}-evand-{variant}.svg"
        path.unlink(missing_ok=True)
        if house is not None:
            same = house.get("certificate", {}).get("side_relation") == "same"
            path.write_text(house_svg(n, house, source, variant, same=same), encoding="utf-8")
            drawn[f"house_{variant}"] = path.name
    inputs = _row_of(inputs_dir(run_dir) / "receipt.json", n)
    exact = _row_of(exact_receipt_path(run_dir), n)
    stages = [f"input {_seconds_text(inputs)}", f"exact solve {_seconds_text(exact)}"]
    for variant in variants_of(run_dir, n, variants):
        generated = _row_of(regularize_dir(run_dir, variant) / "receipt.json", n)
        imported = _row_of(import_dir(run_dir, variant) / "receipt.json", n)
        timing = f"regularize {_seconds_text(generated)}, import {_seconds_text(imported)}"
        stages.append(f"{variant}: {timing}")
    conservative = (_row_of(import_dir(run_dir, "conservative") / "receipt.json", n) or {}).get(
        "policy"
    ) or {}
    drawing = conservative.get("drawing") or {}
    footer = [
        (
            f"Outlined: moved more than {VISIBLE_MOVE:g}; dotted: turned more than "
            f"{VISIBLE_TURN_DEGREES:g} degrees, against the source witness. "
            "Fills: the house renderer's."
        ),
        (
            f"Derived views are labelled '{LABEL}': drawings, not the source witness; the "
            "evidence tier is the record's."
        ),
        "Per-stage wall seconds: " + "; ".join(stages),
        (
            "Policy (docs/project/policies/regularization-policy.md, section 4), "
            f"conservative: {drawing.get('report', 'no view')} "
            f"(row {drawing.get('row', '-')}): "
            f"{drawing.get('reason', '-')}; register candidate: "
            f"{'yes' if conservative.get('register_candidate') else 'no'}"
        ),
    ]
    if n in certificates.HELD:
        footer.append(f"n = {n}: {HELD_NOTE}.")
    comparison = out / f"n-{n:03d}-compare.svg"
    comparison.write_text(comparison_svg(n, panels, footer), encoding="utf-8")
    drawn["comparison"] = comparison.name
    drawn["house_source"] = f"packing/atlas/known-best/rendering/n-{n:03d}.svg"
    if panels[1].witness is not None:
        drawn["house_project_layer"] = (
            f"packing/atlas/known-best/regularized/rendering/n-{n:03d}.svg"
        )
    return {
        "n": n,
        "drawings": drawn,
        "wall_seconds": round(time.perf_counter() - wall, 3),
        "cpu_seconds": round(time.process_time() - cpu, 3),
    }


def _render_job(job: tuple[int, str, str, tuple[str, ...]]) -> dict[str, Any]:
    n, run_text, out_text, variants = job
    return render_one(n, Path(run_text), Path(out_text), variants)


def variants_of(run_dir: Path, n: int, variants: Sequence[str]) -> list[str]:
    """The variants the regularizer was run with at ``n``; the default always, so a count
    the generator never reached still shows why."""
    return [
        variant
        for variant in variants
        if variant == "conservative"
        or _row_of(regularize_dir(run_dir, variant) / "receipt.json", n) is not None
    ]


def imported_variants(run_dir: Path) -> list[str]:
    root = run_dir / "import"
    if not root.is_dir():
        return []
    found = [path.name for path in sorted(root.iterdir()) if (path / "receipt.json").is_file()]
    return sorted(found, key=lambda name: (name != "conservative", name))


#: What the summary keeps of each exact-solve and regularizer receipt row.
EXACT_FIELDS = (
    "status", "second_order_status", "S_exact", "S_cert", "cert_valid", "newton_converged",
    "free_squares", "S_exact_minus_printed", "S_exact_minus_verified",
)  # fmt: skip
REGULARIZE_FIELDS = (
    "status", "level", "level_text", "groups_before", "groups_after", "symmetry_imposed",
    "symmetry_dropped_for_coincidence", "orientation_g", "shape", "angle_changes",
    "free_merges", "coinc_replace", "verify_80", "generator_seconds",
)  # fmt: skip


def summary_row(
    n: int, run_dir: Path, variants: Sequence[str], drawings: dict[str, Any]
) -> dict[str, Any]:
    """Every measure of one count, from the stage receipts, with the per-stage timings."""
    inputs = _row_of(inputs_dir(run_dir) / "receipt.json", n) or {}
    exact = _row_of(exact_receipt_path(run_dir), n) or {}
    timings: dict[str, Any] = {
        "witness_input": _seconds(inputs),
        "exact_solve": _seconds(exact),
    }
    row: dict[str, Any] = {
        "n": n,
        "scalar_kind": inputs.get("scalar_kind"),
        "representation": inputs.get("representation"),
        "printed_side": inputs.get("printed_side"),
        "exact_side": inputs.get("exact_side"),
        "input_centres_exact": inputs.get("centres_exact"),
        "input_angles_exact": inputs.get("angles_exact"),
        "witness_side": _witness_side_record(n),
        "verified_bound": verified_bound(n),
        "held": HELD_NOTE if n in certificates.HELD else None,
        "project_layer": _layer_record(n),
        "exact_solve": {key: exact.get(key) for key in EXACT_FIELDS},
        "variants": {},
        "drawings": drawings,
    }
    for variant in variants_of(run_dir, n, variants):
        generated = _row_of(regularize_dir(run_dir, variant) / "receipt.json", n) or {}
        imported = _row_of(import_dir(run_dir, variant) / "receipt.json", n) or {}
        timings[f"regularize_{variant}"] = _seconds(generated)
        timings[f"import_{variant}"] = _seconds(imported)
        row["variants"][variant] = {
            "regularize": {key: generated.get(key) for key in REGULARIZE_FIELDS},
            "policy": imported.get("policy"),
            "classification": imported.get("classification"),
            "reasons": imported.get("reasons"),
            "certificate_reasons": imported.get("certificate_reasons"),
            "generator": imported.get("generator"),
            "admission": imported.get("admission"),
            "alternate": imported.get("alternate"),
            "held": imported.get("held"),
            "decision": imported.get("decision"),
            "side": imported.get("side"),
            "same_side": imported.get("same_side"),
            "identity": imported.get("identity"),
            "shades": imported.get("shades"),
            "isometry": imported.get("isometry"),
        }
    row["timings"] = timings
    return row


def _witness_side_record(n: int) -> dict[str, Any]:
    side, derivation = witness_side(load_known_best(n))
    text = side.field.decimal(side, 40) if isinstance(side, FieldElement) else literal(side)
    return {"s_W": text, "derivation": derivation}


def _layer_record(n: int) -> dict[str, Any]:
    """The project layer's status at ``n`` and, where it keeps a view, its measures."""
    record = layer_status(n)
    entry = layer_entry(n) or {}
    for key in ("moves", "shades", "non_regression", "side"):
        if key in entry:
            record[key] = entry[key]
    return record


def _seconds(row: Mapping[str, Any]) -> dict[str, Any] | None:
    if not row or "wall_seconds" not in row:
        return None
    return {"wall": row.get("wall_seconds"), "cpu": row.get("cpu_seconds")}


def stage_render(
    counts: Sequence[int], run_dir: Path, *, out: Path, procs: int
) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    variants = tuple(imported_variants(run_dir))
    started = host()
    jobs = [(n, str(run_dir), str(out), variants) for n in sorted(counts, reverse=True)]
    if procs <= 1 or len(jobs) <= 1:
        drawn = [_render_job(job) for job in jobs]
    else:
        with ProcessPoolExecutor(max_workers=procs) as pool:
            drawn = list(pool.map(_render_job, jobs))
    by_count = {row["n"]: row for row in drawn}
    rows = []
    for n in sorted(counts):
        row = summary_row(n, run_dir, variants, by_count[n]["drawings"])
        row["timings"]["render"] = _seconds(by_count[n])
        rows.append(row)
    summary_path = out / "summary.json"
    previous = read_json(summary_path)["rows"] if summary_path.is_file() else []
    merged = {row["n"]: row for row in previous}
    merged.update({row["n"]: row for row in rows})
    summary = {
        "format": FORMAT,
        "stage": "summary",
        "tool": f"{GENERATOR} render",
        "what": (
            "One row per count: the input, the exact solve, each regularizer variant's "
            "generator report, decision, side relation, identity, shades and timings."
        ),
        "pin": pin(),
        "interpreter": interpreter(),
        "run_dir": str(run_dir),
        "variants": list(variants),
        "host_before": started,
        "host_after": host(),
        "rows": [merged[n] for n in sorted(merged)],
    }
    write_json(summary_path, summary)
    return summary


# --------------------------------------------------------------------------------------
# Tables from the summary
# --------------------------------------------------------------------------------------


def _g(value: float | None, digits: int = 2) -> str:
    return "-" if value is None else f"{value:.{digits}g}"


def _layer_cell(layer: Mapping[str, Any]) -> str:
    status = str(layer.get("status"))
    if layer.get("refusal"):
        return f"{status} ({layer['refusal']})"
    if layer.get("changed_squares") is not None:
        return f"{status} ({layer['changed_squares']})"
    return status


def _side_cell(side: Mapping[str, Any] | None) -> str:
    if not side:
        return "-"
    to_verified = side["relation_to_verified"]
    return (
        f"{side['relation_to_witness']} witness ({_g(side['view_minus_witness'])}); "
        f"{to_verified['relation']} verified ({_g(to_verified['difference'])})"
    )


def _same_cell(same: Mapping[str, Any] | None) -> str:
    if not same:
        return "-"
    if same.get("status") == "same":
        result = same.get("result") or {}
        relaxed, gap = result.get("relaxed_count"), result.get("relaxed_largest_gap")
        note = f", {relaxed} left open (<= {_g(gap)})" if relaxed else ""
        reasons = same.get("reasons") or []
        return f"same{note}" + (f" but {'; '.join(reasons)}" if reasons else "")
    result = same.get("result") or {}
    return f"{same.get('status')}: {result.get('kind') or same.get('reason')}"


def _shade_cell(shades: Mapping[str, Any] | None) -> str:
    if not shades:
        return "-"
    house, stage = shades["house"], shades["stage"]
    return (
        f"house {house['light_before']}->{house['light_after']}, "
        f"stage {stage['light_before']}->{stage['light_after']}"
    )


def _class_cell(found: Mapping[str, Any]) -> str:
    rows = found.get("policy") or {}
    if not rows:
        return str(found.get("classification"))
    drawing, certificate = rows["drawing"], rows["certificate"]
    text = f"{drawing['report']} (row {drawing['row']}): {drawing['reason']}"
    if rows.get("drawing_from") == "same_side":
        text += f"; certificate {certificate['report']} (row {certificate['row']})"
    if rows.get("register_candidate"):
        text += "; register candidate"
    return text + ("; held n (think-x4v4)" if found.get("held") else "")


def summary_table(summary: Mapping[str, Any]) -> list[str]:
    """One Markdown row per count and variant: every measure of the spike table."""
    header = (
        "| n | kind | project layer | exact solve | variant | level, groups, symmetry | "
        "routes | class | side | same side | identity | light squares | moved ids |"
    )
    lines = [header, "|" + " --- |" * 13]
    for row in summary["rows"]:
        exact = row["exact_solve"]
        wall = (row["timings"].get("exact_solve") or {}).get("wall")
        solve = f"{exact.get('status')} ({_g(wall, 3)} s)"
        for variant, found in row["variants"].items():
            generated = found["regularize"]
            decision = found.get("decision") or {}
            same = found.get("same_side") or {}
            drawn = (
                same if found.get("classification") == "same" and same.get("view") else found
            )
            identity = drawn.get("identity") or {}
            routes = (
                "/".join("V" if decision.get(route) else "X" for route in ROUTES)
                if decision
                else "-"
            )
            level = (
                f"{generated.get('level')}, {generated.get('groups_before')}->"
                f"{generated.get('groups_after')}, {generated.get('symmetry_imposed') or '-'}"
                if generated.get("status") == "certified"
                else str(generated.get("status"))
            )
            ident = (
                "-"
                if not identity
                else (
                    f"{'1:1' if identity['one_to_one'] else 'not 1:1'}, "
                    f"{_g(identity['max_move'])}, {_g(identity['max_turn_degrees'])} deg"
                )
            )
            moved = identity.get("visible_moved_ids") or []
            moved_text = ", ".join(map(str, moved[:12])) + (" ..." if len(moved) > 12 else "")
            cells = [
                str(row["n"]), str(row["scalar_kind"]), _layer_cell(row["project_layer"]),
                solve, variant, level, routes, _class_cell(found),
                _side_cell(drawn.get("side")), _same_cell(same), ident,
                _shade_cell(drawn.get("shades")), moved_text or "-",
            ]  # fmt: skip
            lines.append("| " + " | ".join(cells) + " |")
    return lines


def timing_table(summary: Mapping[str, Any]) -> list[str]:
    """Wall and CPU seconds per stage and count."""
    stages = sorted({stage for row in summary["rows"] for stage in row["timings"]})
    lines = [
        "| n | " + " | ".join(f"{stage} wall/cpu" for stage in stages) + " |",
        "|" + " --- |" * (len(stages) + 1),
    ]
    for row in summary["rows"]:
        cells = []
        for stage in stages:
            seconds = row["timings"].get(stage)
            cells.append(
                "-" if not seconds else f"{_g(seconds['wall'], 3)}/{_g(seconds['cpu'], 3)}"
            )
        lines.append(f"| {row['n']} | " + " | ".join(cells) + " |")
    return lines


# --------------------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------------------


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        prog=GENERATOR,
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    stages = command.add_subparsers(dest="stage", required=True)

    def common(name: str, summary: str) -> argparse.ArgumentParser:
        stage = stages.add_parser(name, help=summary, description=summary)
        stage.add_argument(
            "--n", nargs="+", required=True, help="counts and ranges, e.g. 5 10 100-120"
        )
        stage.add_argument("--run-dir", type=Path, required=True, help="scratch run directory")
        stage.add_argument(
            "--procs", type=int, default=DEFAULT_PROCS, help="counts at once (default 2)"
        )
        return stage

    def generator(stage: argparse.ArgumentParser, *, timeout: bool = True) -> None:
        stage.add_argument("--policy", choices=POLICIES, default="conservative")
        stage.add_argument("--style", choices=STYLES, default="coincide")
        stage.add_argument("--orient", choices=ORIENTS, default="source")
        if timeout:
            stage.add_argument(
                "--timeout", type=float, default=None,
                help="seconds per count (default 1800 up to n = 200, 3600 above)",
            )  # fmt: skip

    common("witness-input", "write each witness as upstream's input text")
    solve = common("exact-solve", "run upstream exactsolve.py on each input")
    solve.add_argument("--timeout", type=float, default=None, help="seconds per count")
    generator(common("regularize", "run upstream reg.regularize on each exact point"))
    generator(
        common("import", "decide and measure each regularized certificate"), timeout=False
    )
    render = common("render", "draw the comparisons and write summary.json")
    render.add_argument("--out", type=Path, default=None, help="default: RUN_DIR/render")
    table = stages.add_parser(
        "table", help="print the spike tables from summary.json", description="print tables"
    )
    table.add_argument("--summary", type=Path, required=True, help="a summary.json")
    run = common("run", "every stage in order")
    generator(run)
    run.add_argument("--out", type=Path, default=None, help="default: RUN_DIR/render")
    return command


def _report(receipt: Mapping[str, Any], fields: Sequence[str]) -> None:
    for row in receipt["rows"]:
        print(" ".join(f"{field}={row.get(field)}" for field in ("n", *fields)))


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.stage == "table":
        summary = read_json(args.summary)
        print("\n".join([*summary_table(summary), "", *timing_table(summary)]))
        return 0
    counts = parse_counts(args.n)
    run_dir = guard_run_dir(args.run_dir)
    procs = max(1, args.procs)
    stage = args.stage
    if stage in {"witness-input", "run"}:
        receipt = stage_witness_input(counts, run_dir)
        _report(receipt, ("scalar_kind", "centres_exact", "angles_exact"))
    if stage in {"exact-solve", "run"}:
        receipt = stage_exact_solve(counts, run_dir, timeout=args.timeout, procs=procs)
        _report(receipt, ("status", "S_exact", "wall_seconds", "cpu_seconds"))
    variant = None
    if stage in {"regularize", "import", "run"}:
        variant = variant_name(args.policy, args.style, args.orient)
    if stage in {"regularize", "run"}:
        receipt = stage_regularize(
            counts, run_dir, policy=args.policy, style=args.style, orient=args.orient,
            timeout=args.timeout, procs=procs,
        )  # fmt: skip
        _report(receipt, ("status", "level", "groups_before", "groups_after", "wall_seconds"))
    if stage in {"import", "run"} and variant is not None:
        receipt = stage_import(counts, run_dir, variant=variant, procs=procs)
        _report(receipt, ("classification", "reasons", "wall_seconds"))
    if stage in {"render", "run"}:
        out = guard_run_dir(args.out) if args.out else run_dir / "render"
        summary = stage_render(counts, run_dir, out=out, procs=procs)
        print(f"summary: {out / 'summary.json'} ({len(summary['rows'])} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
