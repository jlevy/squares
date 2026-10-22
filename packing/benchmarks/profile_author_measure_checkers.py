"""Profile the authors' measure checkers on recorded net directions, and the exact path.

The baseline for the independent measure verifier (`think-gpe0`): how fast the three
outward-rounded checkers this repository replays actually are, and where their time
goes. For one small certificate of each family, the tool

- builds Tokoharu's `verify.cpp` (rectangle density), and Hosono's
  `mixed_rotated_verify.cpp` and `unified_linear_verify.cpp`, from the retained packets
  at their pinned SHA-256, under the reviewed compile line plus `-g`;
- regenerates each direction's input from the retained exact candidate (by the
  repository's audit tool for rectangles, by the shipped export otherwise) and runs one
  process per direction, refusing the profile unless every complete run reproduces the
  recorded node count, and the recorded leaves and printed bound where the record has
  them;
- attributes time by `gprof` on a static `-pg` build (so that time spent in `libm` is
  sampled too) and by `callgrind` instruction counts on a bounded run, whose per-box
  count does not depend on host load (`perf` is not installed on the session hosts; the
  record says whether it was present);
- counts, on a grid of centres, how many pieces a box can neither prove inside every
  core nor outside every core: the work a spatial index with incremental classification
  would still have to do (a float diagnostic with no proof authority);
- times the exact Python path, `sqpack.rectangle_density`, on the same rectangle
  certificate and direction, capped by nodes.

Every number is a measurement of these implementations on this host, retained with the
host's load average; none is a proof, and the profiled builds are not the reviewed
binaries. The spec that reads this profile is
`docs/project/specs/active/plan-2026-10-02-independent-measure-verifier.md`.

It writes two outputs. `timings.json` holds times, counts, instruction totals and the
locality census, and is an implementer input under that plan's clean-room protocol.
`attribution/` holds the function-level profiles and their raw text, and is not. This
file is on the dirty side too: it imports the authors' export code.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib
import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import Callable, Iterable, Mapping, Sequence
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
from strif import atomic_write_bytes, atomic_write_text

from devtools import audit_tokoharu_density as tokoharu
from devtools import audit_wand125_linear as linear_audit
from devtools import audit_wand125_rectangles as rectangles_audit
from devtools.retained_data import read_retained_bytes

REPO = Path(__file__).resolve().parents[2]
PACKING = REPO / "packing"
WEB = PACKING / "resources/web"
KIND = "author-measure-checker-profile/v1"
DEFAULT_OUT = PACKING / "benchmarks/results/author-checker-profile-2026-10-02"

STEP = Fraction(83, 40000)
COMPILE_FLAGS = ("-O2", "-std=c++17", "-fno-fast-math", "-ffp-contract=off")
#: The reviewed compile line, plus debug information, which GCC emits without changing
#: the generated code.
REVIEWED_EXTRA = ("-g",)
#: The attribution build: a static `-pg` binary, so the sampling histogram covers the
#: statically linked `libm` (`nextafter`) as well as the checker. Not the reviewed binary.
GPROF_EXTRA = ("-g", "-pg", "-static")
#: The exact path's threshold: the binary64 enclosure of 10001/10000 the C++ compares
#: against, as `profile_rectangle_verifier_hotspots.py` uses it.
EXACT_THRESHOLD = Fraction(2252024993666617, 2251799813685248)

RECT_CASE = WEB / (
    "wand125-rectangle-certificates-2026-10-01/wand125-rectangles/certificates/rect_n20_L48975"
)
MIXED_CODE = WEB / (
    "wand125-point-and-mixed-2026-09-28/square-packing-bounds/certificates/mixed_n50_L740/code"
)
MIXED_DIR = WEB / (
    "wand125-mixed-bounds-n76-2026-10-02/square-packing-bounds/certificates/mixed_n76_L894"
)
LINEAR_DIR = WEB / (
    "wand125-linear-certificates-2026-10-02/square-packing-bounds/certificates/mixed_n101_L1028"
)
LINEAR_CODE = LINEAR_DIR / "code"
MIXED_SOURCE_SHA256 = "89b674a6feabe24d91c29431de1624907c4bff83280ceb481475455686693652"
LINEAR_SOURCE_SHA256 = "0249726ab1e67dc481e0c53f43b524902a48f95d051b1b08865a3cf3ef89a06d"
MIXED_CANDIDATE_DIGEST = "f2c2530552547a56a454c55bee99a196221ae1f4357570c3a0d524eddd5d9cdf"
LINEAR_CANDIDATE_DIGEST = "933aa46895a8cdfda1e3d0017b394a4de5d585d507a65472b2c4fe0165d0f79b"

type Piece = tuple[str, tuple[float, ...]]


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def net_rotation(index: int) -> tuple[Fraction, Fraction]:
    """The exact cosine and sine at net index ``index``."""
    t = index * STEP
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def load_average() -> list[float]:
    return [round(value, 3) for value in os.getloadavg()]


# --------------------------------------------------------------------------- processes


@dataclass
class Completed:
    """One child process: its exit, its own resource use, and where its output went."""

    returncode: int
    cpu_seconds: float
    wall_seconds: float
    max_rss_kib: int
    timed_out: bool
    stdout: str
    stderr: str


def run_child(
    command: Sequence[str], cwd: Path, timeout: float, logs: Path | None = None
) -> Completed:
    """Run ``command`` and read back that child's own rusage with ``wait4``.

    Its output goes to ``logs`` (default ``cwd``), which must be a scratch directory.
    """
    logs = cwd if logs is None else logs
    logs.mkdir(parents=True, exist_ok=True)
    out_path, err_path = logs / "child.stdout", logs / "child.stderr"
    with out_path.open("wb") as out, err_path.open("wb") as err:
        started = time.perf_counter()
        process = subprocess.Popen(
            list(command), cwd=cwd, stdout=out, stderr=err, start_new_session=True
        )
        expired = threading.Event()

        def kill() -> None:
            expired.set()
            os.killpg(process.pid, signal.SIGKILL)

        timer = threading.Timer(timeout, kill)
        timer.start()
        try:
            _pid, status, usage = os.wait4(process.pid, 0)
        finally:
            timer.cancel()
        wall = time.perf_counter() - started
    process.returncode = os.waitstatus_to_exitcode(status)
    return Completed(
        returncode=process.returncode,
        cpu_seconds=round(usage.ru_utime + usage.ru_stime, 3),
        wall_seconds=round(wall, 3),
        max_rss_kib=usage.ru_maxrss,
        timed_out=expired.is_set(),
        stdout=out_path.read_text(),
        stderr=err_path.read_text(),
    )


def compile_checker(source: Path, binary: Path, extra: Sequence[str]) -> dict[str, Any]:
    command = ["g++", *COMPILE_FLAGS, *extra, str(source), "-o", str(binary)]
    started = time.perf_counter()
    subprocess.run(command, check=True, capture_output=True)
    return {
        "argv": ["g++", *COMPILE_FLAGS, *extra, source.name, "-o", binary.name],
        "seconds": round(time.perf_counter() - started, 3),
        "binary_sha256": sha256(binary.read_bytes()),
    }


def toolchain() -> dict[str, Any]:
    def first_line(*command: str) -> str | None:
        if shutil.which(command[0]) is None:
            return None
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        return (result.stdout or result.stderr).splitlines()[0].strip()

    cpu = None
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.is_file():
        for line in cpuinfo.read_text().splitlines():
            if line.startswith("model name"):
                cpu = line.split(":", 1)[1].strip()
                break
    return {
        "platform": platform.platform(),
        "cpu": cpu,
        "logical_cpus": os.cpu_count(),
        "python": sys.version.split()[0],
        "gxx": first_line("g++", "--version"),
        "valgrind": first_line("valgrind", "--version"),
        "gprof": first_line("gprof", "--version"),
        "perf": first_line("perf", "--version"),
    }


# --------------------------------------------------------------------------- profilers

_GPROF_ROW = re.compile(
    r"^\s*(?P<pct>[\d.]+)\s+(?P<cum>[\d.]+)\s+(?P<self>[\d.]+)"
    r"(?:\s+(?P<calls>\d+)\s+[\d.]+\s+[\d.]+)?\s+(?P<name>\S.*)$"
)
_CALLGRIND_ROW = re.compile(r"^\s*(?P<ir>[\d,]+)\s+\(\s*(?P<pct>[\d.]+)%\)\s+(?P<name>\S.*)$")


def parse_gprof_flat(text: str, limit: int = 15) -> list[dict[str, Any]]:
    """The leading rows of a `gprof -b -p` flat profile."""
    rows: list[dict[str, Any]] = []
    for line in text.splitlines():
        match = _GPROF_ROW.match(line)
        if match is None:
            continue
        rows.append(
            {
                "function": match["name"].strip(),
                "percent_time": float(match["pct"]),
                "self_seconds": float(match["self"]),
                "calls": int(match["calls"]) if match["calls"] else None,
            }
        )
    return rows[:limit]


def parse_callgrind(text: str, limit: int = 15) -> tuple[int, list[dict[str, Any]]]:
    """Total instructions and the leading exclusive rows of `callgrind_annotate`."""
    total: int | None = None
    rows: list[dict[str, Any]] = []
    for line in text.splitlines():
        match = _CALLGRIND_ROW.match(line)
        if match is None:
            continue
        instructions = int(match["ir"].replace(",", ""))
        name = match["name"].strip()
        if name.startswith("PROGRAM TOTALS"):
            total = instructions
            continue
        # `file:function [binary]`: keep the function, drop the paths.
        function = name.split(" [", 1)[0]
        if ":" in function:
            function = function.split(":", 1)[1]
        rows.append(
            {
                "function": function,
                "instructions": instructions,
                "percent": float(match["pct"]),
            }
        )
    require(total is not None, "callgrind_annotate printed no program total")
    assert total is not None
    return total, rows[:limit]


# --------------------------------------------------------------------------- families


@dataclass
class Direction:
    """One net direction to time, with what the record says it must reproduce."""

    index: int
    recorded: dict[str, Any]
    node_limit: int | None = None
    complete: bool = True
    #: The recording run's own seconds for this direction, where the record has them.
    reference_seconds: float | None = None


@dataclass
class Family:
    """One certificate family: its checker, its prepared inputs and its directions."""

    name: str
    certificate: str
    source: Path
    source_sha256: str
    pieces: list[Piece]
    side: Fraction
    core: Fraction
    directions: list[Direction]
    prepare: Callable[[int, Path], dict[str, Any]]
    argv: Callable[[Path, Direction], list[str]]
    observe: Callable[[str], dict[str, Any]]
    domain_half_width: Callable[[int], Fraction]
    attribution_nodes: int | None
    callgrind_nodes: int | None
    #: Node limits for bounded prefixes of the least direction: how the cost per box
    #: changes with depth, and so how far a bounded profile represents a whole one.
    prefix_limits: tuple[int, ...] = ()
    notes: list[str] = field(default_factory=list)


def _pick(rows: Mapping[int, dict[str, Any]], key: str) -> list[int]:
    """The least, the median and the greatest oblique direction by ``key``."""
    ordered = sorted((i for i in rows if i >= 1), key=lambda i: (rows[i][key], i))
    return [ordered[0], ordered[len(ordered) // 2], ordered[-1]]


def _float_images(kind: str, geometry: Sequence[Fraction], side: Fraction) -> list[Piece]:
    """The eight D4 images of one primitive, in floats, for the locality census only."""
    pairs = [geometry[:2]] if kind == "point" else [geometry[:2], geometry[2:]]
    images: list[Piece] = []
    for swap in (False, True):
        for flip_x in (False, True):
            for flip_y in (False, True):
                moved: list[float] = []
                for x, y in pairs:
                    u, v = (y, x) if swap else (x, y)
                    moved += [
                        float(side - u if flip_x else u),
                        float(side - v if flip_y else v),
                    ]
                images.append((kind, tuple(moved)))
    return images


def rectangle_family(work: Path) -> Family:
    candidate = tokoharu.load_json(RECT_CASE / "certified_candidate.json")
    side, core, _total, rects = tokoharu.density(candidate)
    rows = _jsonl_by(RECT_CASE / "verified_angles.jsonl", "r")
    folder = work / "rectangle"
    prepared = rectangles_audit.materialize(RECT_CASE, folder)
    source = rectangles_audit.CHECKER / "verify.cpp"

    def prepare(_index: int, into: Path) -> dict[str, Any]:
        into.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(folder / "certificate_input.txt", into / "certificate_input.txt")
        return {"input_sha256": prepared["input_sha256"]}

    def observe(stdout: str) -> dict[str, Any]:
        found = [json.loads(line) for line in stdout.splitlines() if line.startswith("{")]
        require(len(found) == 1, "the rectangle checker printed other than one direction row")
        row = found[0]
        return {
            "status": row.get("status"),
            "nodes": row.get("nodes"),
            "leaves": row.get("leaves"),
            "lower": row.get("lower_bound"),
        }

    def half_width(index: int) -> Fraction:
        c, s = net_rotation(index)
        return side / 2 - core * (c + s) / 2

    return Family(
        name="rectangle",
        certificate="wand125 rect_n20_L48975 (2026-10-01 packet, T-068): s(20) >= 1959/400",
        source=source,
        source_sha256=rectangles_audit.VERIFY_SHA256,
        pieces=[("rectangle", tuple(float(v) for v in r[:4])) for r in rects],
        side=side,
        core=core,
        directions=[
            Direction(
                i,
                {k: rows[i][k] for k in ("status", "nodes", "leaves", "lower_bound")},
                reference_seconds=rows[i]["seconds"],
            )
            for i in _pick(rows, "nodes")
        ],
        prepare=prepare,
        argv=lambda binary, direction: [
            str(binary),
            str(direction.index),
            str(direction.index),
        ],
        observe=observe,
        domain_half_width=half_width,
        attribution_nodes=None,
        callgrind_nodes=None,
        notes=[
            (
                "The rectangle checker takes no node limit, so its bounded profiles run "
                "the least oblique direction to completion."
            ),
            (
                "Input regenerated from the retained candidate and required to hash to "
                f"the published input digest {prepared['input_sha256']}."
            ),
        ],
    )


def _jsonl_by(path: Path, key: str) -> dict[int, dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    return {int(row[key]): row for row in rows}


def _shipped_modules(*directories: Path) -> dict[str, Any]:
    for directory in reversed(directories):
        if str(directory) not in sys.path:
            sys.path.insert(0, str(directory))
    names = ("mixed_density_check", "mixed_net_audit", "mixed_rotated_verify")
    modules = {name: importlib.import_module(name) for name in names}
    if LINEAR_CODE in directories:
        modules["unified_linear_verify"] = importlib.import_module("unified_linear_verify")
    return modules


def _wand125_observe(stdout: str) -> dict[str, Any]:
    output = json.loads(stdout)
    return {
        "status": output.get("status"),
        "nodes": output.get("nodes"),
        "leaves": output.get("leaves"),
        "lower": output.get("lower"),
        "frontier_boxes": len(output.get("frontier") or []),
    }


def mixed_family(work: Path) -> Family:
    source = MIXED_CODE / "mixed_rotated_verify.cpp"
    require(sha256(source.read_bytes()) == MIXED_SOURCE_SHA256, "mixed checker drift")
    modules = _shipped_modules(MIXED_CODE)
    data = json.loads(read_retained_bytes(MIXED_DIR / "candidate.json"))
    certificate = json.loads(read_retained_bytes(MIXED_DIR / "certificate.json"))
    require(certificate["candidate_digest"] == MIXED_CANDIDATE_DIGEST, "n76 record drift")
    model = modules["mixed_density_check"].expand(data)
    require(model[5] == MIXED_CANDIDATE_DIGEST, "n76 candidate does not hash to its record")
    net = modules["mixed_net_audit"].candidate_net(data)
    records = {int(k): v for k, v in certificate["results"].items()}
    side, core = Fraction(data["L"]), Fraction(data["B"])
    pieces: list[Piece] = []
    for item in data["rectangles"]:
        if Fraction(item["mass"]):
            geometry = [Fraction(v) for v in item["rectangle"]]
            pieces += [
                ("rectangle", _bbox(g)) for _, g in _float_images("rectangle", geometry, side)
            ]
    widths: dict[int, Fraction] = {}

    def prepare(index: int, into: Path) -> dict[str, Any]:
        into.mkdir(parents=True, exist_ok=True)
        manifest = modules["mixed_rotated_verify"].export(
            model, index, into / "input.txt", Fraction(1), net
        )
        require(manifest["candidate_digest"] == MIXED_CANDIDATE_DIGEST, "export digest drift")
        require(manifest["source_sha256"] == MIXED_SOURCE_SHA256, "export source drift")
        widths[index] = Fraction(manifest["E"])
        return {"input_sha256": manifest["input_sha256"], "E": manifest["E"]}

    def half_width(index: int) -> Fraction:
        if index not in widths:
            prepare(index, work / "mixed-domain" / f"net{index:03}")
        return widths[index]

    oblique = {i: r for i, r in records.items() if i >= 1}
    chosen = _pick(oblique, "nodes")
    return Family(
        name="mixed",
        certificate="wand125 mixed_n76_L894 (2026-10-02, rectangles only): s(76) >= 447/50",
        source=source,
        source_sha256=MIXED_SOURCE_SHA256,
        pieces=pieces,
        side=side,
        core=core,
        directions=[
            Direction(
                i,
                {
                    "status": "ANGLE_VERIFIED",
                    "nodes": records[i]["nodes"],
                    "lower": records[i]["lower"],
                },
                node_limit=records[i]["nodes"],
            )
            for i in chosen
        ],
        prepare=prepare,
        argv=lambda binary, d: [str(binary), "input.txt", str(d.node_limit)],
        observe=_wand125_observe,
        domain_half_width=half_width,
        attribution_nodes=30_000,
        callgrind_nodes=30_000,
        prefix_limits=(3_000, 30_000),
        notes=[
            (
                "Inputs regenerated from the retained candidate at Gamma = 1; the "
                "record's node count is the node limit, as the shipped replay passes it. "
                "Angle zero is decided by a separate integer-table program and is not "
                "profiled."
            ),
        ],
    )


def _bbox(geometry: tuple[float, ...]) -> tuple[float, ...]:
    x0, y0, x1, y1 = geometry
    return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))


def linear_family(_work: Path) -> Family:
    source = LINEAR_CODE / "unified_linear_verify.cpp"
    require(sha256(source.read_bytes()) == LINEAR_SOURCE_SHA256, "linear checker drift")
    modules = _shipped_modules(LINEAR_CODE, MIXED_CODE)
    data = json.loads(read_retained_bytes(LINEAR_DIR / "candidate.json"))
    certificate = json.loads(read_retained_bytes(LINEAR_DIR / "certificate.json"))
    require(certificate["candidate_digest"] == LINEAR_CANDIDATE_DIGEST, "n101 record drift")
    records = {int(k): v for k, v in certificate["results"].items()}
    measure = linear_audit.linear_measure(data)
    pieces: list[Piece] = []
    for kind, images in measure.images.items():
        for geometry, _weight in images:
            floats = tuple(float(v) for v in geometry)
            pieces.append((kind, _bbox(floats) if kind == "rectangle" else floats))
    widths: dict[int, Fraction] = {}

    def prepare(index: int, into: Path) -> dict[str, Any]:
        into.mkdir(parents=True, exist_ok=True)
        manifest = modules["unified_linear_verify"].export(data, index, into / "input.txt")
        require(manifest["candidate_digest"] == LINEAR_CANDIDATE_DIGEST, "export digest drift")
        require(manifest["source_sha256"] == LINEAR_SOURCE_SHA256, "export source drift")
        require(
            manifest["input_sha256"] == records[index]["input_sha256"],
            f"regenerated input {index} differs from the certificate's record",
        )
        widths[index] = Fraction(manifest["E"])
        return {"input_sha256": manifest["input_sha256"], "E": manifest["E"]}

    def half_width(index: int) -> Fraction:
        c, s = net_rotation(index)
        return (measure.side - measure.core * (c + s)) / 2

    oblique = {i: r for i, r in records.items() if i >= 1}
    least, median, _largest = _pick(oblique, "nodes")
    directions = [
        Direction(
            i, {"status": "ANGLE_VERIFIED", "nodes": records[i]["nodes"]}, records[i]["nodes"]
        )
        for i in (least, median)
    ]
    # The axis branch is the costliest direction (2,072,307 nodes): time a bounded prefix.
    directions.append(
        Direction(0, {"nodes": records[0]["nodes"]}, node_limit=100_000, complete=False)
    )
    return Family(
        name="linear",
        certificate=(
            "wand125 mixed_n101_L1028 (2026-10-02; points, segments, rectangles): "
            "s(101) >= 257/25"
        ),
        source=source,
        source_sha256=LINEAR_SOURCE_SHA256,
        pieces=pieces,
        side=measure.side,
        core=measure.core,
        directions=directions,
        prepare=prepare,
        argv=lambda binary, d: [str(binary), "input.txt", str(d.node_limit)],
        observe=_wand125_observe,
        domain_half_width=half_width,
        attribution_nodes=20_000,
        callgrind_nodes=5_000,
        prefix_limits=(3_000, 30_000),
        notes=[
            (
                "Inputs regenerated from the retained candidate and required to hash to "
                "the certificate's per-direction input_sha256. The certificate records "
                "node counts only, so nodes are what is matched. Direction 0 is a bounded "
                "100,000-box prefix: a rate, not a match."
            ),
        ],
    )


# --------------------------------------------------------------------------- locality


def locality_census(
    family: Family, index: int, scales: Sequence[int] = (5, 9), grid: int = 15
) -> dict[str, Any]:
    """Per-box piece classes on a grid of centres of the checker's folded domain.

    A piece is *inside* when it lies in the closed core at every centre of the box,
    *outside* when a separating axis (the container's two or the core's two) parts it
    from every such core, and *straddling* otherwise. A spatial index with incremental
    classification touches only the straddling pieces of a box; *near* counts those
    whose bounding box meets the box's swept core bounding box, which is what a
    bounding-box index alone would visit. Float arithmetic, diagnostic only.
    """
    c_exact, s_exact = net_rotation(index)
    c, s = float(c_exact), float(s_exact)
    half = float(family.core) / 2
    origin = float(family.side) / 2
    width = float(family.domain_half_width(index))
    extreme: list[np.ndarray] = []
    lo = np.empty((len(family.pieces), 2))
    hi = np.empty((len(family.pieces), 2))
    for row, (kind, geometry) in enumerate(family.pieces):
        if kind == "rectangle":
            x0, y0, x1, y1 = geometry
            points = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        elif kind == "segment":
            points = [geometry[:2], geometry[2:]]
        else:
            points = [geometry[:2]]
        padded = points + [points[-1]] * (4 - len(points))
        extreme.append(np.array(padded, dtype=float))
        array = np.array(points, dtype=float)
        lo[row], hi[row] = array.min(axis=0), array.max(axis=0)
    corners = np.stack(extreme)  # pieces x 4 x 2
    reach = half * (c + s)
    result: dict[str, Any] = {
        "direction": index,
        "pieces": len(family.pieces),
        "domain_half_width": round(width, 6),
        "grid": grid,
    }
    for scale in scales:
        h = width / 2**scale
        motion = (c + s) * h
        counts: dict[str, list[int]] = {"near": [], "straddling": [], "inside": []}
        for gx in range(grid):
            for gy in range(grid):
                cx = origin + (gx + 0.5) * width / grid
                cy = origin + (gy + 0.5) * width / grid
                dx, dy = corners[..., 0] - cx, corners[..., 1] - cy
                u, v = c * dx + s * dy, -s * dx + c * dy
                inside = (np.abs(u).max(axis=1) + motion <= half) & (
                    np.abs(v).max(axis=1) + motion <= half
                )
                apart = (
                    (u.min(axis=1) - motion > half)
                    | (u.max(axis=1) + motion < -half)
                    | (v.min(axis=1) - motion > half)
                    | (v.max(axis=1) + motion < -half)
                )
                box_lo = np.array([cx - h - reach, cy - h - reach])
                box_hi = np.array([cx + h + reach, cy + h + reach])
                near = np.all((hi >= box_lo) & (lo <= box_hi), axis=1)
                outside = apart | ~near
                counts["near"].append(int(near.sum()))
                counts["inside"].append(int(inside.sum()))
                counts["straddling"].append(int((~inside & ~outside).sum()))
        result[f"half_width_E_over_2^{scale}"] = {
            key: {"mean": round(float(np.mean(v)), 2), "max": int(np.max(v))}
            for key, v in counts.items()
        }
    return result


# --------------------------------------------------------------------------- runs


def timed_run(family: Family, binary: Path, direction: Direction, work: Path) -> dict[str, Any]:
    folder = work / family.name / f"time-{direction.index:03}-{direction.node_limit or 0}"
    prepared = family.prepare(direction.index, folder)
    before = load_average()
    done = run_child(family.argv(binary, direction), folder, timeout=3600)
    record: dict[str, Any] = {
        "direction": direction.index,
        "scope": "complete"
        if direction.complete
        else f"bounded to {direction.node_limit} nodes",
        "node_limit": direction.node_limit,
        "input": prepared,
        "recorded": direction.recorded,
        "recording_run_seconds": direction.reference_seconds,
        "returncode": done.returncode,
        "timed_out": done.timed_out,
        "cpu_seconds": done.cpu_seconds,
        "wall_seconds": done.wall_seconds,
        "max_rss_kib": done.max_rss_kib,
        "load_before": before,
        "load_after": load_average(),
    }
    if done.returncode != 0 or done.timed_out:
        record["stderr_tail"] = done.stderr[-2000:]
        record["matches_record"] = False
        return record
    observed = family.observe(done.stdout)
    record["observed"] = observed
    nodes = observed["nodes"]
    if nodes:
        record["boxes_per_cpu_second"] = round(nodes / done.cpu_seconds, 1)
        record["microseconds_per_box"] = round(1e6 * done.cpu_seconds / nodes, 3)
        record["nanoseconds_per_box_piece"] = round(
            1e9 * done.cpu_seconds / nodes / len(family.pieces), 3
        )
    record["matches_record"] = matches(direction, observed)
    return record


def matches(direction: Direction, observed: Mapping[str, Any]) -> bool | None:
    """Whether a complete run reproduced its record; ``None`` for a bounded prefix."""
    if not direction.complete:
        return None
    recorded = direction.recorded
    status = str(observed.get("status", "")).upper()
    checks = [
        observed.get("nodes") == recorded.get("nodes"),
        status in {"VERIFIED", "ANGLE_VERIFIED"},
        observed.get("frontier_boxes", 0) == 0,
        "leaves" not in recorded or observed.get("leaves") == recorded["leaves"],
        *(
            observed.get("lower") == recorded[key]
            for key in ("lower_bound", "lower")
            if key in recorded
        ),
    ]
    return all(checks)


def prefixes(family: Family) -> list[Direction]:
    """Bounded prefixes of the least direction, one per limit in ``prefix_limits``."""
    least = family.directions[0]
    return [
        Direction(least.index, least.recorded, node_limit=limit, complete=False)
        for limit in family.prefix_limits
    ]


def attribution_direction(family: Family, nodes: int | None) -> Direction:
    least = family.directions[0]
    if nodes is None:
        return least
    return Direction(least.index, least.recorded, node_limit=nodes, complete=False)


def gprof_run(family: Family, work: Path, raw: Path) -> dict[str, Any]:
    folder = work / family.name / "gprof"
    folder.mkdir(parents=True, exist_ok=True)
    binary = folder / "checker.pg"
    build = compile_checker(family.source, binary, GPROF_EXTRA)
    direction = attribution_direction(family, family.attribution_nodes)
    family.prepare(direction.index, folder)
    done = run_child(family.argv(binary, direction), folder, timeout=3600)
    require(done.returncode == 0 and not done.timed_out, f"{family.name}: gprof run failed")
    flat = subprocess.run(
        ["gprof", "-b", "-p", str(binary), str(folder / "gmon.out")],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    atomic_write_bytes(
        raw / f"{family.name}-gprof-flat.txt.gz", gzip.compress(flat.encode(), mtime=0)
    )
    observed = family.observe(done.stdout)
    return {
        "build": build,
        "direction": direction.index,
        "node_limit": direction.node_limit,
        "nodes": observed["nodes"],
        "cpu_seconds": done.cpu_seconds,
        "flat_profile": parse_gprof_flat(flat),
        "note": "Sampled at 100 Hz on a static -pg build; mcount adds overhead to every "
        "non-inlined call, so shares are indicative and seconds exceed the reviewed build's.",
    }


def callgrind_run(family: Family, reviewed: Path, work: Path, raw: Path) -> dict[str, Any]:
    folder = work / family.name / "callgrind"
    direction = attribution_direction(family, family.callgrind_nodes)
    family.prepare(direction.index, folder)
    out = folder / "callgrind.out"
    command = [
        "valgrind",
        "--tool=callgrind",
        f"--callgrind-out-file={out}",
        *family.argv(reviewed, direction),
    ]
    done = run_child(command, folder, timeout=3600)
    require(done.returncode == 0 and not done.timed_out, f"{family.name}: callgrind run failed")
    annotated = subprocess.run(
        ["callgrind_annotate", "--inclusive=no", "--auto=no", str(out)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    atomic_write_bytes(
        raw / f"{family.name}-callgrind-annotate.txt.gz",
        gzip.compress(annotated.encode(), mtime=0),
    )
    total, rows = parse_callgrind(annotated)
    observed = family.observe(done.stdout)
    nodes = int(observed["nodes"])
    return {
        "direction": direction.index,
        "node_limit": direction.node_limit,
        "nodes": nodes,
        "instructions": total,
        "instructions_per_box": round(total / nodes),
        "instructions_per_box_piece": round(total / nodes / len(family.pieces), 2),
        "cpu_seconds_under_valgrind": done.cpu_seconds,
        "exclusive": rows,
        "note": "Instruction counts of the reviewed build (plus -g); they include input "
        "parsing and setup, which a bounded run amortises over fewer boxes.",
    }


def exact_python_run(family: Family, nodes: int, seconds: float, work: Path) -> dict[str, Any]:
    """The exact path on the rectangle certificate's least direction, capped by nodes."""
    direction = family.directions[0].index
    folder = work / "exact-python"
    folder.mkdir(parents=True, exist_ok=True)
    candidate = RECT_CASE / "certified_candidate.json.gz"
    command = [
        sys.executable,
        "-m",
        "devtools.verify_rectangle_density",
        str(candidate),
        "--n",
        "20",
        "--side",
        str(family.side),
        "--threshold",
        str(EXACT_THRESHOLD),
        "--angles",
        str(direction),
        "--max-nodes-per-angle",
        str(nodes),
        "--max-seconds",
        str(seconds),
        "--timing",
    ]
    done = run_child(command, PACKING, timeout=seconds + 120, logs=folder)
    require(done.returncode in {0, 1, 2} and not done.timed_out, "exact path did not finish")
    report = json.loads(done.stdout)
    angle = report["angles"][0]
    cpu = report["timing"]["phases"]["verification"]["process_cpu_seconds"]
    return {
        "checker": report["checker"],
        "checker_source_sha256": report["checker_source_sha256"],
        "bound_mode": report["bound_mode"],
        "direction": direction,
        "node_limit": nodes,
        "status": angle["status"],
        "stop_cause": angle.get("stop_cause"),
        "nodes": angle["nodes"],
        "accepted_leaves": angle["accepted_leaves"],
        "verification_cpu_seconds": round(cpu, 3),
        "microseconds_per_box": round(1e6 * cpu / angle["nodes"], 1),
        "process_cpu_seconds": done.cpu_seconds,
        "note": "Exact rationals, common-core bound (no derivative term), Python backend: "
        "a different bound and a different traversal, so the comparable figure is time "
        "per box, not nodes per direction.",
    }


# --------------------------------------------------------------------------- driver


def summarise(
    families: Mapping[str, dict[str, Any]], exact: Mapping[str, Any] | None
) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for name, block in families.items():
        complete = [r for r in block["runs"] if r.get("matches_record")]
        if not complete:
            continue
        nodes = sum(r["observed"]["nodes"] for r in complete)
        cpu = sum(r["cpu_seconds"] for r in complete)
        summary[name] = {
            "complete_directions": [r["direction"] for r in complete],
            "nodes": nodes,
            "cpu_seconds": round(cpu, 3),
            "microseconds_per_box": round(1e6 * cpu / nodes, 2),
            "pieces": block["pieces"],
        }
        if exact is not None and name == "rectangle":
            summary[name]["exact_python_microseconds_per_box"] = exact["microseconds_per_box"]
            summary[name]["exact_python_over_author_checker_per_box"] = round(
                exact["microseconds_per_box"] / summary[name]["microseconds_per_box"], 1
            )
    return summary


#: What the clean timings keep of a callgrind run: totals, never function rows.
CLEAN_CALLGRIND_KEYS = (
    "direction",
    "node_limit",
    "nodes",
    "instructions",
    "instructions_per_box",
    "instructions_per_box_piece",
    "cpu_seconds_under_valgrind",
)


def _submit_attribution(
    pool: ThreadPoolExecutor,
    args: argparse.Namespace,
    *,
    families: Mapping[str, Family],
    binaries: Mapping[str, Path],
    work: Path,
    raw: Path,
) -> list[tuple[str, str, Future[dict[str, Any]]]]:
    jobs: list[tuple[str, str, Future[dict[str, Any]]]] = []
    for name, family in families.items():
        if args.gprof:
            jobs.append((name, "gprof", pool.submit(gprof_run, family, work, raw)))
        wanted = family.callgrind_nodes is not None or args.callgrind_rectangle
        if args.callgrind and wanted:
            future = pool.submit(callgrind_run, family, binaries[name], work, raw)
            jobs.append((name, "callgrind", future))
    return jobs


def profile(args: argparse.Namespace) -> dict[str, Any]:
    """Run every measurement and write the clean timings and the dirty attribution."""
    started = time.perf_counter()
    tool_sha256 = sha256(Path(__file__).read_bytes())
    out: Path = args.out
    dirty = out / "attribution"
    raw = dirty / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="author-checker-profile-", dir=args.scratch))
    builders = {"rectangle": rectangle_family, "mixed": mixed_family, "linear": linear_family}
    families = {name: builders[name](work) for name in builders if name in args.families}
    binaries: dict[str, Path] = {}
    blocks: dict[str, dict[str, Any]] = {}
    for name, family in families.items():
        require(
            sha256(family.source.read_bytes()) == family.source_sha256, f"{name} source drift"
        )
        (work / name).mkdir(parents=True, exist_ok=True)
        binaries[name] = work / name / "checker"
        blocks[name] = {
            "certificate": family.certificate,
            "checker_sha256": family.source_sha256,
            "build": compile_checker(family.source, binaries[name], REVIEWED_EXTRA),
            "pieces": len(family.pieces),
            "piece_kinds": {
                kind: sum(1 for k, _ in family.pieces if k == kind)
                for kind in sorted({k for k, _ in family.pieces})
            },
            "notes": family.notes,
            "runs": [],
        }
    attribution: dict[str, dict[str, Any]] = {name: {} for name in families}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        timed = [
            (name, pool.submit(timed_run, family, binaries[name], direction, work))
            for name, family in families.items()
            for direction in [*family.directions, *prefixes(family)]
        ]
        attributed = _submit_attribution(
            pool, args, families=families, binaries=binaries, work=work, raw=raw
        )
        exact_future = (
            pool.submit(exact_python_run, families["rectangle"], args.exact_nodes, 600.0, work)
            if args.exact and "rectangle" in families
            else None
        )
        for name, future in timed:
            run = future.result()
            blocks[name]["runs"].append(run)
            summary = {
                "family": name,
                "direction": run["direction"],
                "matches": run.get("matches_record"),
                "cpu": run["cpu_seconds"],
                "us_per_box": run.get("microseconds_per_box"),
            }
            print(json.dumps(summary), flush=True)
        for name, label, future in attributed:
            attribution[name][label] = future.result()
            print(json.dumps({"family": name, "attribution": label}), flush=True)
        exact = exact_future.result() if exact_future is not None else None
    for name, family in families.items():
        indices = sorted({d.index for d in family.directions if d.index >= 1})
        blocks[name]["locality"] = [locality_census(family, i) for i in indices]
        if "callgrind" in attribution[name]:
            whole = attribution[name]["callgrind"]
            blocks[name]["callgrind_totals"] = {key: whole[key] for key in CLEAN_CALLGRIND_KEYS}
    require(
        sha256(Path(__file__).read_bytes()) == tool_sha256,
        "the profiling tool changed during its own run",
    )
    refusals = [
        f"{name} direction {run['direction']}"
        for name, block in blocks.items()
        for run in block["runs"]
        if run.get("matches_record") is False
    ]
    attribution_cpu = sum(
        entry.get("cpu_seconds", entry.get("cpu_seconds_under_valgrind", 0.0))
        for per_family in attribution.values()
        for entry in per_family.values()
    )
    timed_cpu = sum(run["cpu_seconds"] for block in blocks.values() for run in block["runs"])
    identity = {
        "kind": KIND,
        "status": "PROFILE_REFUSED" if refusals else "PROFILE_RETAINED",
        "refusals": refusals,
        "created": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tool": str(Path(__file__).relative_to(REPO)),
        "tool_sha256": tool_sha256,
        "host": toolchain(),
        "workers": args.workers,
    }
    timings = identity | {
        "clean_room": (
            "Implementer-readable: timings, counts and totals only. Function-level "
            "attribution of the authors' checkers is in attribution/, which implementers "
            "do not read."
        ),
        "families": blocks,
        "exact_python": exact,
        "summary": summarise(blocks, exact),
        "child_cpu_seconds": {
            "timed_runs": round(timed_cpu, 1),
            "attribution_runs": round(attribution_cpu, 1),
            "exact_python": exact["process_cpu_seconds"] if exact else 0.0,
        },
        "wall_seconds_total": round(time.perf_counter() - started, 1),
        "scope": (
            "Measurements of the authors' checkers and the repository's exact path on "
            "this host, one process per direction, child CPU from wait4. Complete "
            "directions must reproduce the recorded node counts; bounded runs are rates "
            "only. No bound is verified or moved by this profile."
        ),
    }
    dirty_record = identity | {
        "clean_room": "Dirty side: names the authors' functions. Not an implementer input.",
        "method": "gprof on a static -pg build, and callgrind on the reviewed build",
        "perf_on_host": shutil.which("perf") is not None,
        "families": attribution,
    }
    atomic_write_text(
        out / "timings.json", json.dumps(timings, indent=2, sort_keys=True) + "\n"
    )
    atomic_write_text(
        dirty / "attribution.json", json.dumps(dirty_record, indent=2, sort_keys=True) + "\n"
    )
    if not args.keep_work:
        shutil.rmtree(work, ignore_errors=True)
    return timings


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--scratch", type=Path, default=None, help="parent of the work dir")
    parser.add_argument(
        "--families",
        default="rectangle,mixed,linear",
        type=lambda text: [part for part in text.split(",") if part],
    )
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--exact-nodes", type=int, default=400)
    parser.add_argument("--no-gprof", dest="gprof", action="store_false")
    parser.add_argument("--no-callgrind", dest="callgrind", action="store_false")
    parser.add_argument(
        "--callgrind-rectangle",
        action="store_true",
        help="also run callgrind over a whole rectangle direction (minutes)",
    )
    parser.add_argument("--no-exact", dest="exact", action="store_false")
    parser.add_argument("--keep-work", action="store_true")
    return parser.parse_args(None if argv is None else list(argv))


def main() -> int:
    result = profile(parse_args())
    print(json.dumps({"status": result["status"], "summary": result["summary"]}, indent=2))
    return 0 if result["status"] == "PROFILE_RETAINED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
