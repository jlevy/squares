"""Verify every replayed wand125 certificate with the clean-room verifier.

Two families, each covering every retained certificate of its formats, replayed by the
authors' checker here or not. `--family rectangles` (format T; Milestone A,
`think-d69e`) runs every `certified_candidate.json.gz` of the wand125 rectangle packets
and Tokoharu's three, at the threshold the files declare; `--family mixed` (formats M
and L; Milestone B, `think-4vf7`) runs every `mixed_n*` candidate of the wand125 mixed
and linear packets at the threshold they declare, with the authors' recorded CPU on the
directions they replayed beside ours on the same directions. `--summary` writes
`census-summary.json` and `census-summary.md` beside the two census folders: one row per
certificate with its verdict, CPU, least certified bound and whether the authors' replay
recorded here is complete, the input the records lane uses for evidence entries.

The replay receipts named below were the first census's case list; the rectangle
family now reads them only for the authors' replay status. They are
the ones this repository has already replayed with the authors' checker: every case in
the `receipts/replay/audit.json` of the wand125 rectangle packets, and Tokoharu's three
in the 22 September packet. Each runs through `sqverify-fast` at every direction of its
net, 201 unless a format M file declares its own (`proof_net`, jlevy/squares#366); its
per-direction receipts and summary are kept as `--out/PACKET/CERTIFICATE.jsonl.gz`.
The census records, per certificate, the verifier's status, node total, least
certified bound, CPU seconds (from `wait4`, user plus system), wall seconds and load
average, beside the binary's and the candidate's digests. On the least-bound
direction, the exact capture at the centre of the least-bound leaf is evaluated in
rationals and must clear the threshold.

A certificate counts as verified here only when the verifier's own summary says
`VERIFIED` (every direction verified and the direction set is the whole net) and its
exit status is zero. `--resume` keeps a case already `VERIFIED`, by whichever build: each
case records its own binary and source digests. `--check` re-reads the census and fails
unless every case is verified, exited zero, and passed the exact least-leaf test;
`--only` and `--packets` narrow it as they narrow a run.

`--control` puts negative controls on a verified certificate itself, at the threshold
its census row was decided at. It serves formats M and T and refuses any other row
before running.

For format M (receipt kind `sqverify-fast-control/v2`) the original must verify again at
its least-bound direction, a near-threshold mutant must be refused there, and every mass
scaled by 99/100 (the stage-4 control of the authors' replays) runs at every
direction of the net with `--confirm`, at `--threads`: it must be refused at one direction
at least, and every direction that does not verify it must be a refusal on coverage (a
counterexample candidate whose witness the crate confirmed below the threshold, or the
axis sweep's refusal; never `audit-failed`, `non-finite` or `unresolved`) at a pose in the
per-bin centre domain (lemma D, with lemma C1's quarter turn: the whole square
`[rho(a_r), L - rho(a_r)]^2`, computed here) where the mutant's capture, evaluated again
by `check_sqverify_fast.mixed_exact`, an exact evaluator written apart from the crate,
equals the crate's, is below 1, and is at least 1 divided by 99/100 for the original. The
pose is the refusal's witness, or at the axis the sweep's least vertex; rows and summary
must agree, and the mutant's premises restate the census row's. The mutant may verify
elsewhere, where the original captures at least 100/99: the least-bound direction is
chosen by the branch and bound's termination margin, so a run there alone can verify a
true mutant and fail closed (FC-1 of the 6 October re-check; v1 receipts ran it at the
least-bound direction only, where it was refused; the review of this fix is
docs/project/reviews/review-2026-10-06-sqverify-fast-census-control-fc1.md).
Every mass scaled so that the exact capture at the least-bound leaf's centre is at most
one part in a million below the threshold runs at that direction; that capture is
evaluated again by the same evaluator and must equal the crate's, and the refused mutant
must be a counterexample candidate whose witness the crate confirmed below the
threshold, with the crate's exact capture there equal to this tool's, and capture less
than 1 at that centre or at the witness, in the domain. The near-threshold
mutant is named for the centre it is scaled at: the verifier may refuse it at another
centre, and its discrimination near the threshold rests on the crate's own tests (IR-3
of the review of 5 October).

For format T (receipt kind `sqverify-fast-control/v1`, the route the review of 6 October
accepted) the original and both mutants run at one direction and at Tokoharu's
threshold 10001/10000, which the rectangle family passes: the original must verify there,
and two mutants must be refused, every weight scaled by 99/100 and every weight scaled so
that the exact capture at the control centre is at most one part in a million below that
threshold. That capture is evaluated again by
`sqpack.rectangle_density.coverage_at_point`, an exact evaluator written apart from the
crate, and must equal the crate's; each refused mutant must capture less than the
threshold at that centre or at the refusal's witness, evaluated the same way. The point is
not the least-bound leaf of the least-bound direction but the least-bound leaf centre of
least exact capture over the row's oblique directions (`tightest_centre`): at Tokoharu's
threshold every direction's least certified bound is about 1.0001, and at
`rect_n87_L941`'s least-bound direction the 99/100 mutant still verified.

Each receipt is `--out/PACKET/CERTIFICATE.control.json`, with status `CONTROLS_REFUSED`
only when all of that holds.

`--evidence` prints each selected certificate's replay evidence entry, for a records
lane to paste into the register; it refuses a row whose build is not of a crate source
in `REVIEWED_SOURCES`, or is on a declared net that the source's review did not read,
and names the reviewed source it was. A format T entry takes its source key from its
packet's reported entry, since the rectangle packets are registered by packet, and also
refuses controls run on a build no review accepted. `--source-digest` prints the tree's
crate `source_sha256` by `build.rs`'s rule and the review that accepted it, exiting 1
when none did, so a lane can check before it builds that a census run will be one of
reviewed source.

From `packing/`:

    .venv/bin/python3 -m devtools.sqverify_fast_census --source-digest
    .venv/bin/python3 -m devtools.sqverify_fast_census \\
        --binary sqverify_fast/target/release/sqverify-fast \\
        --out benchmarks/measure-verifier/census --threads 2 --resume
    .venv/bin/python3 -m devtools.sqverify_fast_census --family mixed \\
        --binary sqverify_fast/target/release/sqverify-fast \\
        --out benchmarks/measure-verifier/census-mixed --threads 2 --resume
    .venv/bin/python3 -m devtools.sqverify_fast_census --family mixed --control \\
        --binary sqverify_fast/target/release/sqverify-fast \\
        --out benchmarks/measure-verifier/census-mixed --only mixed_n67_L848
"""

from __future__ import annotations

import argparse
import functools
import gzip
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools.check_sqverify_fast import (
    STEP,
    crate_source_sha256,
    direction,
    metadata_net,
    mixed_exact,
    mixed_mutant,
    net_step,
    read_raw,
    scaled,
)
from sqpack import retained_json
from sqpack.rectangle_density import (
    RectangleDensityCandidate,
    coverage_at_point,
    load_candidate,
    load_candidate_bytes,
)
from sqpack.yamlio import safe_load

PROJECT = Path(__file__).resolve().parents[1]
WEB = PROJECT / "resources/web"
PACKETS = ("2026-09-27", "2026-09-28", "2026-10-01", "2026-10-02")
THRESHOLD = "10001/10000"
TOKOHARU_PACKET = "2026-09-22"
TOKOHARU = WEB / "external-square-certificates-2026-09-22/tokoharu-density/certificates"
# The packets of formats M and L.
MIXED_PACKETS = (
    "wand125-point-and-mixed-2026-09-28",
    "wand125-point-and-mixed-2026-10-01",
    "wand125-mixed-bounds-2026-10-02",
    "wand125-mixed-bounds-n76-2026-10-02",
    "wand125-mixed-bounds-afternoon-2026-10-02",
    "wand125-linear-certificates-2026-10-02",
    "wand125-linear-n82-2026-10-02",
    "wand125-mixed-bounds-2026-10-03",
    "wand125-mixed-bounds-2026-10-04",
    "wand125-mixed-bounds-evening-2026-10-04",
    "wand125-mixed-bounds-2026-10-05",
    "wand125-mixed-bounds-finer-net-2026-10-05",
    "wand125-mixed-bounds-finer-net-2026-10-06",
    "wand125-mixed-bounds-check2-2026-10-06",
)
#: The standard net's direction count; a format M file may declare another.
STANDARD_DIRECTIONS = 201
CENSUS_ROOT = PROJECT / "benchmarks/measure-verifier"
# Tokoharu's three certificates, replayed in the 22 September packet's density receipt.
TOKOHARU_CASES = (
    ("cert_n11_L381", 11, "381/100"),
    ("cert_n26_L5508", 26, "1377/250"),
    ("cert_n29_L571", 29, "571/100"),
)


@dataclass(frozen=True)
class Case:
    """One retained certificate."""

    packet: str
    certificate: str
    n: int
    side: str
    # Mixed family: the candidate's path, and None for the declared threshold.
    path: Path | None = None
    threshold: str | None = THRESHOLD

    @property
    def candidate(self) -> Path:
        if self.path is not None:
            return self.path
        if self.packet == TOKOHARU_PACKET:
            return TOKOHARU / self.certificate / "certified_candidate.json"
        for packet in (self.packet, *PACKETS):
            path = (
                WEB
                / f"wand125-rectangle-certificates-{packet}"
                / "wand125-rectangles/certificates"
                / self.certificate
                / "certified_candidate.json.gz"
            )
            if path.is_file():
                return path
        raise SystemExit(f"no retained candidate for {self.certificate}")


def side_digits(side: Fraction) -> str:
    """The digits of a side as certificate names spell it: `447/50` is `894`."""
    text = f"{float(side):.6f}".rstrip("0").rstrip(".")
    return text.replace(".", "")


def named_side(name: str, side: Fraction) -> bool:
    """Whether a certificate's name (`..._L894`) spells its side."""
    digits = name.rsplit("_L", 1)[1]
    return digits.rstrip("0") == side_digits(side).rstrip("0")


def rectangle_cases() -> list[Case]:
    """Tokoharu's three replayed certificates and every wand125 rectangle certificate."""
    receipt = WEB / "external-square-certificates-2026-09-22/receipts/density/audit.json"
    passed = {
        (int(case["n"]), str(case["L"]))
        for case in json.loads(receipt.read_text(encoding="utf-8"))["cases"]
        if case.get("status") == "PASS"
    }
    cases: list[Case] = [
        Case(TOKOHARU_PACKET, name, n, side)
        for name, n, side in TOKOHARU_CASES
        if (n, side) in passed
    ]
    for packet in PACKETS:
        root = WEB / f"wand125-rectangle-certificates-{packet}/wand125-rectangles/certificates"
        for path in sorted(root.glob("rect_n*_L*/certified_candidate.json.gz")):
            name = path.parent.name
            data = json.loads(gzip.decompress(path.read_bytes()), parse_float=str)
            side = Fraction(str(data["L"]))
            if not named_side(name, side):
                raise SystemExit(f"{name}: the name does not spell the side {side}")
            n = int(name.split("_")[1].removeprefix("n"))
            cases.append(Case(packet, name, n, str(side), path))
    return cases


def mixed_cases() -> list[Case]:
    """Every format M or L certificate of the wand125 mixed and linear packets."""
    cases: list[Case] = []
    for packet in MIXED_PACKETS:
        root = WEB / packet / "square-packing-bounds/certificates"
        for path in sorted(root.glob("mixed_n*_L*/candidate.json.gz")):
            name = path.parent.name
            data = json.loads(gzip.decompress(path.read_bytes()), parse_float=str)
            side = Fraction(str(data["L"]))
            n = int(data["n"])
            if not named_side(name, side) or name.split("_")[1] != f"n{n}":
                raise SystemExit(f"{name}: the name does not spell n = {n} and L = {side}")
            cases.append(Case(packet, name, n, str(side), path, None))
    return cases


def net_directions(case: Case) -> int:
    """How many net directions a case's certificate has: its `proof_net`'s, else the
    count its format T metadata sets (`metadata_net`, GN-5 of jlevy/squares#485's
    review), else 201."""
    raw = case.candidate.read_bytes()
    data = json.loads(gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw)
    if not isinstance(data, dict):
        return STANDARD_DIRECTIONS
    net = data.get("proof_net")
    if isinstance(net, dict):
        return int(net["last"]) + 1
    declared = metadata_net(data)
    return STANDARD_DIRECTIONS if declared is None else declared[1]


def replay_folders(case: Case) -> list[Path]:
    """A mixed case's receipt folders: `n76`, or `n85-L946` where two sides share n."""
    receipts = WEB / case.packet / "receipts"
    digits = case.certificate.rsplit("_L", 1)[1]
    named = receipts / f"n{case.n}-L{digits}"
    plain = receipts / f"n{case.n}"
    if named.is_dir():
        return [named]
    return [plain] if plain.is_dir() else []


def has_siblings(case: Case) -> bool:
    """Whether another certificate of the packet has the same n (and so `nN` is shared)."""
    return any(
        other.name != case.certificate
        for other in (WEB / case.packet / "square-packing-bounds/certificates").glob(
            f"mixed_n{case.n}_L*"
        )
    )


def mixed_reference(case: Case) -> dict[str, Any]:
    """The authors' replayed directions of one mixed case, with their CPU seconds.

    A full replay recorded only as a comparison (`full/compare.json`, the 28 September
    packet) counts as every direction of the case's net when its certificate digest is
    this case's.
    """
    rows: dict[int, dict[str, Any]] = {}
    complete_without_rows = False
    shared = has_siblings(case) and not any(
        folder.name.startswith(f"n{case.n}-L") for folder in replay_folders(case)
    )
    for folder in replay_folders(case):
        # A folder shared by two sides of the same n binds only through a digest.
        for path in [] if shared else sorted(folder.glob("range-*/directions.jsonl")):
            for line in path.read_text(encoding="utf-8").splitlines():
                row = json.loads(line)
                if row.get("status") == "REPLAYED":
                    rows[int(row["index"])] = row
        compare = folder / "full/compare.json"
        if compare.is_file():
            record = json.loads(compare.read_text(encoding="utf-8"))
            certificate = case.candidate.parent / "certificate.json.gz"
            digest = (
                hashlib.sha256(gzip.decompress(certificate.read_bytes())).hexdigest()
                if certificate.is_file()
                else None
            )
            # The replay's own digest is of a file not retained here; its inputs
            # receipt binds it instead, by the number of rectangle images it enclosed.
            inputs = folder / "inputs.json"
            images = (
                json.loads(inputs.read_text(encoding="utf-8")).get("rectangle_images")
                if inputs.is_file()
                else None
            )
            rows_here = json.loads(gzip.decompress(case.candidate.read_bytes())).get(
                "rectangles", []
            )
            complete_without_rows = record.get("status") == "FULL_REPLAY_MATCHES_SHIPPED" and (
                record.get("certificate_sha256") == digest or images == 8 * len(rows_here)
            )
    return {
        "directions": (
            list(range(net_directions(case))) if complete_without_rows else sorted(rows)
        ),
        "cpu_seconds": sum(float(row.get("cpu_seconds") or 0.0) for row in rows.values()),
        "nodes": sum(int((row.get("report") or {}).get("nodes") or 0) for row in rows.values()),
        "per_direction_cpu": not complete_without_rows,
    }


def replay_status(directions: int, total: int = STANDARD_DIRECTIONS) -> str:
    """How much of a certificate's `total` directions the authors' replay here covers."""
    if directions >= total:
        return "complete"
    return f"partial ({directions} of {total})" if directions else "none"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def loadavg() -> float:
    return os.getloadavg()[0]


def run(binary: Path, case: Case, out: Path, threads: int) -> dict[str, Any]:
    """Run all directions of one case; keep the receipts as deterministic gzip JSONL."""
    out.mkdir(parents=True, exist_ok=True)
    argv = [
        str(binary.resolve()),
        "--candidate",
        str(case.candidate),
        "--n",
        str(case.n),
        "--side",
        case.side,
        "--directions",
        "all",
        *(["--threshold", case.threshold] if case.threshold is not None else []),
        "--threads",
        str(threads),
        "--confirm",
    ]
    before = loadavg()
    start = time.monotonic()
    # The live output goes to a file outside the tree: a commit hook that hides
    # unstaged changes once replaced a half-written receipt file under a running
    # verifier, which kept writing to the orphaned file (rect_n69_L8575, first run).
    scratch = tempfile.TemporaryDirectory(prefix="sqverify-fast-census-")
    raw = Path(scratch.name) / f"{case.certificate}.jsonl"
    with raw.open("wb") as stdout, tempfile.TemporaryFile() as stderr:
        pid = os.posix_spawn(
            argv[0],
            argv,
            os.environ,
            file_actions=[
                (os.POSIX_SPAWN_DUP2, stdout.fileno(), 1),
                (os.POSIX_SPAWN_DUP2, stderr.fileno(), 2),
            ],
        )
        _, status, usage = os.wait4(pid, 0)
        stderr.seek(0)
        error_text = stderr.read().decode(errors="replace")
    wall = time.monotonic() - start
    lines = [json.loads(line) for line in raw.read_text(encoding="utf-8").splitlines() if line]
    rows = sorted((line for line in lines if "r" in line), key=lambda row: int(row["r"]))
    summary = next(
        (line for line in lines if line.get("kind") == "sqverify-fast-summary/v1"), {}
    )
    body = "".join(json.dumps(line, sort_keys=True) + "\n" for line in [*rows, summary])
    with gzip.GzipFile(out / f"{case.certificate}.jsonl.gz", "wb", mtime=0) as packed:
        packed.write(body.encode())
    scratch.cleanup()
    bounds = [
        row["min_certified_lower_bound"]
        for row in rows
        if row.get("min_certified_lower_bound") is not None
    ]
    least = min(
        (row for row in rows if row.get("least_bound_box") is not None),
        key=lambda row: row["min_certified_lower_bound"],
        default=None,
    )
    threshold = Fraction(str(summary.get("threshold") or case.threshold or THRESHOLD))
    least_check: dict[str, Any] | None = None
    if least is not None:
        box = least["least_bound_box"]
        spec = f"{least['r']},{box['x']!r},{box['y']!r}"
        probe = subprocess.run(
            [argv[0], "--candidate", str(case.candidate), "--n", str(case.n), "--probe", spec],
            capture_output=True,
            text=True,
            check=False,
        )
        reading = json.loads(probe.stdout) if probe.returncode == 0 else {}
        exact = reading.get("exact_coverage")
        least_check = {
            "r": least["r"],
            "centre": [box["x"], box["y"]],
            "exact_coverage": exact,
            "clears_threshold": exact is not None and Fraction(exact) >= threshold,
        }
    return {
        "least_bound_leaf_exact": least_check,
        "threshold": str(threshold),
        "direction_cpu_seconds": {
            str(row["r"]): row.get("cpu_seconds") for row in rows if "cpu_seconds" in row
        },
        "packet": case.packet,
        "certificate": case.certificate,
        "n": case.n,
        "L": case.side,
        "returncode": os.waitstatus_to_exitcode(status),
        "stderr_tail": error_text[-2000:],
        "status": (
            summary.get("status")
            if len(rows)
            == int((summary.get("premises") or {}).get("angle_count") or STANDARD_DIRECTIONS)
            else "INCOMPLETE"
        ),
        "directions_verified": sum(1 for row in rows if row.get("verdict") == "verified"),
        "refused_directions": summary.get("refused_directions"),
        "nodes": summary.get("nodes"),
        "least_certified_bound": min(bounds) if bounds else None,
        "axis_vertices": next((row.get("vertices") for row in rows if row.get("r") == 0), None),
        "cpu_seconds": usage.ru_utime + usage.ru_stime,
        "wall_seconds": wall,
        "threads": threads,
        "load_before": before,
        "load_after": loadavg(),
        "candidate_sha256": sha256(case.candidate),
        "premises": summary.get("premises"),
        "build": summary.get("build"),
    }


#: The two mutations of `--control`: the stage-4 scaling, and a scaling to at most one
#: part in a million below the threshold at the least-bound leaf's centre.
CONTROL_SCALE = Fraction(99, 100)
NEAR_THRESHOLD = Fraction(1, 10**6)


def direction_row(
    binary: Path, candidate: Path, n: int, index: int, threshold: str | None = None
) -> dict[str, Any]:
    """One direction of one candidate, with `--confirm`: at its declared threshold, or at
    `threshold` where the census passed one (format T, Tokoharu's 10001/10000)."""
    argv = [str(binary.resolve()), "--candidate", str(candidate), "--n", str(n)]
    argv += ["--directions", str(index), "--confirm"]
    argv += ["--threshold", threshold] if threshold is not None else []
    start = time.monotonic()
    result = subprocess.run(argv, capture_output=True, text=True, check=False, timeout=7200)
    lines = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
    row = next((line for line in lines if line.get("r") == index), {})
    summary = next(
        (line for line in lines if line.get("kind") == "sqverify-fast-summary/v1"), {}
    )
    witness = row.get("witness") or {}
    return {
        "returncode": result.returncode,
        "verdict": row.get("verdict"),
        "nodes": row.get("nodes"),
        "min_certified_lower_bound": row.get("min_certified_lower_bound"),
        "exact_below_threshold": witness.get("exact_below_threshold"),
        "witness": witness or None,
        "seconds": round(time.monotonic() - start, 2),
        "stderr_tail": result.stderr[-500:],
        "build": summary.get("build"),
    }


def rectangle_family(case: Case) -> bool:
    """Whether a case is format T, a `certified_candidate.json` of a rectangle packet."""
    return case.candidate.name.startswith("certified_candidate.json")


def exact_capture(
    case: Case, raw: dict[str, Any], x: Fraction, y: Fraction, index: int
) -> Fraction:
    """The exact capture at one centre and net direction, by an evaluator written apart
    from the crate: `sqpack.rectangle_density` for format T, `mixed_exact` otherwise."""
    if rectangle_family(case):
        cosine, sine = direction(index, net_step(raw))
        return coverage_at_point(exact_candidate(case.candidate, case.n), x, y, cosine, sine)
    return mixed_exact(raw, x, y, index)


@functools.cache
def exact_candidate(path: Path, n: int) -> RectangleDensityCandidate:
    """A format T candidate read once by `sqpack.rectangle_density`, for its exact
    captures at many centres. That loader admits only the standard net in metadata,
    since its own verifier runs on it; a file whose metadata sets another net is read
    without the metadata, as `exact_capture` gives every angle from the file's net."""
    data = path.read_bytes()
    text = gzip.decompress(data) if data[:2] == b"\x1f\x8b" else data
    raw = json.loads(text, parse_float=str)
    if metadata_net(raw) in (None, (STEP, STANDARD_DIRECTIONS)):
        return load_candidate(path, n=n)
    raw.pop("certificate")
    return load_candidate_bytes(json.dumps(raw).encode(), n=n)


def mutant(case: Case, raw: dict[str, Any], factor: Fraction) -> dict[str, Any]:
    """The candidate with every mass scaled by `factor`: format T's weights, with its
    metadata dropped as the stage-4 controls drop it, or format M and L masses."""
    return scaled(raw, factor) if rectangle_family(case) else mixed_mutant(raw, factor=factor)


def tightest_centre(
    binary: Path, case: Case, raw: dict[str, Any], receipts: Path
) -> tuple[int, list[float], Fraction, Fraction, int]:
    """Format T's control point: of the least-bound leaf centres the census row's
    receipts record at its oblique directions, the one of least exact capture.

    The branch and bound stops a leaf once its bound clears the threshold, so at
    Tokoharu's 10001/10000 every direction's least certified bound is about 1.0001, and
    the least of them says little about where the density is tight: the exact capture at
    that leaf's centre ran from 1.0012 to 1.14 in the October 1 packet, and at
    rect_n87_L941's least-bound direction the 99/100 mutant still verified. So the
    centre is chosen by its exact capture, evaluated apart from the crate, and the
    crate's own exact capture there (`--probe`) is kept beside it. Returns the index, the
    centre, the independent and the crate's captures, and how many centres were weighed.
    """
    rows = [
        json.loads(line)
        for line in gzip.decompress(receipts.read_bytes()).decode().splitlines()
        if line
    ]
    weighed: list[tuple[Fraction, int, list[float]]] = []
    for row in rows:
        box = row.get("least_bound_box")
        if "r" not in row or int(row["r"]) < 1 or not box:
            continue
        index = int(row["r"])
        centre = [float(box["x"]), float(box["y"])]
        x, y = (Fraction(value) for value in centre)
        weighed.append((exact_capture(case, raw, x, y, index), index, centre))
    if not weighed:
        raise SystemExit(f"{case.certificate}: no least-bound leaf in the census receipts")
    exact, index, centre = min(weighed, key=lambda item: (item[0], item[1]))
    spec = f"{index},{centre[0]!r},{centre[1]!r}"
    binary_text = str(binary.resolve())
    probe = subprocess.run(
        [binary_text, "--candidate", str(case.candidate), "--n", str(case.n), "--probe", spec],
        capture_output=True,
        text=True,
        check=False,
    )
    reading = json.loads(probe.stdout) if probe.returncode == 0 else {}
    if reading.get("exact_coverage") is None:
        raise SystemExit(f"{case.certificate}: the crate's probe at {spec} failed")
    return index, centre, exact, Fraction(reading["exact_coverage"]), len(weighed)


#: The verdicts a control counts as a refusal on coverage (CC-1 of the review of the FC-1
#: fix): an oblique direction's counterexample candidate, whose exact witness the crate
#: confirmed below the threshold, and the axis vertex sweep's refusal. `audit-failed`,
#: `non-finite`, `unresolved` and `fault-injected` are not refusals a control may count.
CANDIDATE = "counterexample-candidate"
AXIS_REFUSED = "refused"
#: How far the axis sweep's certified lower bound on the capture at its least vertex may
#: sit below the exact capture there: its binary64 rounding over a few thousand terms.
AXIS_ROUNDING = Fraction(1, 10**9)


def domain_bounds(raw: dict[str, Any], index: int) -> tuple[Fraction, Fraction]:
    """Lemma D's per-bin centre domain at node `index` on either axis, `[rho(a_r), L -
    rho(a_r)]`, computed here apart from the crate (CC-2): `a_r = max(0, r D - D/2)` and
    `rho(t) = (cos phi + sin phi)/2 = (1 + 2t - t^2) / (2 (1 + t^2))` at `t = tan(phi/2)`.
    A capture below 1 refutes a format M claim only at a centre in this domain. It is the
    whole square, not the quadrant `[L/2, L - rho(a_r)]^2` the crate searches: lemma C1's
    quarter turn gives the capture the same values on it, so a capture below 1 anywhere in
    it refutes the claim at node r (CR-6 of the re-check). The crate rounds its search box
    outward, so a witness a few ulps outside the exact domain fails closed here."""
    step = net_step(raw)
    low = max(Fraction(0), index * step - step / 2)
    rho = (1 + 2 * low - low * low) / (2 * (1 + low * low))
    return rho, Fraction(raw["L"]) - rho


def in_domain(raw: dict[str, Any], index: int, pose: Any) -> bool:
    """Whether a pose lies in the per-bin centre domain at node `index`."""
    if not pose:
        return False
    low, high = domain_bounds(raw, index)
    return all(low <= Fraction(value) <= high for value in pose)


def refusal_record(
    raw: dict[str, Any], row: dict[str, Any], factor: Fraction, *, format_m: bool
) -> dict[str, Any]:
    """One direction where the scaled mutant was not verified, judged apart from the
    crate: a coverage refusal (CC-1), its pose in the per-bin domain (CC-2), the mutant's
    capture there below 1 and equal to the crate's (CC-5, kept exact), and the
    original's at least 1, as the census row says it is everywhere (CC-4)."""
    index = int(row["r"])
    verdict = row.get("verdict")
    witness = row.get("witness") or {}
    axis = index == 0 and row.get("method") == "axis-vertex-sweep"
    coverage = (axis and verdict == AXIS_REFUSED) or (
        index > 0 and verdict == CANDIDATE and witness.get("exact_below_threshold") is True
    )
    pose = row.get("argmin") if axis else witness.get("exact_pose")
    capture = (
        factor * mixed_exact(raw, Fraction(pose[0]), Fraction(pose[1]), index) if pose else None
    )
    crate = witness.get("exact_coverage")
    if axis:
        # The vertex sweep evaluates no capture exactly; it certifies a lower bound on the
        # capture at its least vertex, which the exact capture must meet, within the
        # sweep's rounding (CR-5 of the re-check).
        bound = row.get("min_certified_lower_bound")
        agree = (
            capture is not None
            and bound is not None
            and Fraction(bound) <= capture <= Fraction(bound) + AXIS_ROUNDING
        )
    else:
        agree = capture is not None and crate is not None and Fraction(crate) == capture
    return {
        "r": index,
        "verdict": verdict,
        "method": row.get("method"),
        "pose": pose,
        "coverage_refusal": coverage,
        "crate_exact_below_threshold": witness.get("exact_below_threshold"),
        "in_domain": format_m and in_domain(raw, index, pose),
        "capture": None if capture is None else str(capture),
        "capture_below_1": capture is not None and capture < 1,
        "crate_lower_bound": row.get("min_certified_lower_bound") if axis else None,
        "captures_agree": agree,
        "original_at_least_1": capture is not None and capture / factor >= 1,
    }


def scaled_sweep(
    binary: Path,
    raw: dict[str, Any],
    mutant: Path,
    n: int,
    *,
    factor: Fraction,
    threads: int,
    premises: dict[str, Any],
) -> dict[str, Any]:
    """The scaled mutant at every direction of its net, with `--confirm` (FC-1).

    A direction where the original captures more than 1/factor verifies the mutant too,
    so no single direction can be relied on to refuse it; the mutant's claim is refuted
    where some direction refuses it on coverage at a pose in the centre domain where its
    capture, evaluated again here apart from the crate, is below 1. Each refused
    direction's pose is the crate's exact witness, or at the axis, where the vertex sweep
    reports no witness, its least vertex (`argmin`); the mutant's capture there is the
    factor times the original's. `premises` are the census row's, which the mutant's must
    restate (CC-3).
    """
    argv = [str(binary.resolve()), "--candidate", str(mutant), "--n", str(n)]
    argv += ["--directions", "all", "--threads", str(threads), "--confirm"]
    start = time.monotonic()
    result = subprocess.run(argv, capture_output=True, text=True, check=False, timeout=14400)
    lines = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
    rows = sorted((line for line in lines if "r" in line), key=lambda row: int(row["r"]))
    summary = next(
        (line for line in lines if line.get("kind") == "sqverify-fast-summary/v1"), {}
    )
    stated = summary.get("premises") or {}
    count = int(stated.get("angle_count") or 0)
    format_m = premises.get("format") == "M"
    refused = [
        refusal_record(raw, row, factor, format_m=format_m)
        for row in rows
        if row.get("verdict") != "verified"
    ]
    return {
        "directions": len(rows),
        "net_directions": count,
        "indices_complete": [int(row["r"]) for row in rows] == list(range(count)),
        "returncode": result.returncode,
        "summary_status": summary.get("status"),
        "summary_refused_directions": summary.get("refused_directions"),
        "fault_injected_at_box": summary.get("fault_injected_at_box"),
        "premises_agree": all(
            str(stated.get(key)) == str(premises.get(key))
            for key in (
                "D",
                "B",
                "L",
                "n",
                "net_origin",
                "angle_count",
                "format",
                "centre_domain",
            )
        ),
        "mutant_input_sha256": stated.get("input_sha256"),
        "verified_directions": [
            int(row["r"]) for row in rows if row.get("verdict") == "verified"
        ],
        "refused": refused,
        "seconds": round(time.monotonic() - start, 2),
        "stderr_tail": result.stderr[-500:],
    }


def refusal_held(item: dict[str, Any]) -> bool:
    """A refusal the control may count (CC-1, CC-2, CC-4, CC-5)."""
    return all(
        item.get(key) is True
        for key in (
            "coverage_refusal",
            "in_domain",
            "capture_below_1",
            "captures_agree",
            "original_at_least_1",
        )
    )


def sweep_held(sweep: dict[str, Any]) -> bool:
    """A scaled sweep refutes its mutant: every direction of the net ran once, the binary
    and its summary agree that the mutant was refused and where, no fault was injected,
    the mutant's premises restate the census row's, at least one direction refused it,
    and every direction that did not verify it is a coverage refusal at a pose in the
    centre domain where its capture, evaluated apart from the crate, is below 1."""
    refused = sweep["refused"]
    return (
        sweep["directions"] == sweep["net_directions"] > 0
        and sweep["indices_complete"] is True
        and sweep["returncode"] == 1
        and sweep["summary_status"] == "REFUSED"
        and sweep["fault_injected_at_box"] is None
        and sweep["premises_agree"] is True
        and bool(refused)
        and sweep["summary_refused_directions"] == [item["r"] for item in refused]
        and len(sweep["verified_directions"]) + len(refused) == sweep["directions"]
        and all(map(refusal_held, refused))
    )


def control(
    binary: Path,
    case: Case,
    entry: dict[str, Any],
    out: Path | None = None,
    threads: int = 1,
) -> dict[str, Any]:
    """Negative controls on a verified certificate, at the threshold its census row was
    decided at. Format M (receipt kind v2): the original again and a near-threshold
    mutant at its least-bound direction, and the 99/100 mutant at every direction of its
    net (FC-1). Format T (receipt kind v1, `rectangle_control`): the original and both
    mutants at the tightest least-bound leaf centre the row's receipts in `out` record.
    Any other row is refused before running (CR-7)."""
    least = entry.get("least_bound_leaf_exact") or {}
    if entry.get("status") != "VERIFIED" or not least:
        raise SystemExit(f"{case.certificate}: control needs a verified census entry")
    if rectangle_family(case):
        return rectangle_control(binary, case, entry, out)
    index = int(least["r"])
    centre = [Fraction(value) for value in least["centre"]]
    crate = Fraction(least["exact_coverage"])
    raw = read_raw(case.candidate)
    premises = entry.get("premises") or {}
    # The exact evaluator takes the step from the file; the row was decided on the net
    # admission read. They must be one net, or the control is of another certificate.
    decided = premises.get("D")
    if decided is None or Fraction(str(decided)) != net_step(raw):
        raise SystemExit(
            f"{case.certificate}: the row's net step {decided} is not the file's "
            f"{net_step(raw)}; the control would evaluate another net"
        )
    format_m = premises.get("format") == "M"
    if not format_m:
        # The domain checks are lemma D's per-bin domain; format L's is Tokoharu's, which
        # this control does not compute, and its axis runs by branch and bound (CR-7).
        # Format T, a rectangle packet's, takes `rectangle_control` above.
        raise SystemExit(
            f"{case.certificate}: --control serves format M and format T rows only; this "
            f"row is format {premises.get('format')}"
        )
    exact = mixed_exact(raw, centre[0], centre[1], index)
    # Rounded down, so the capture at the centre is at most 1 - NEAR_THRESHOLD.
    near = Fraction(int((1 - NEAR_THRESHOLD) / exact * 10**15), 10**15)
    runs: list[dict[str, Any]] = []
    original = direction_row(binary, case.candidate, case.n, index)
    # The build the controls ran on, which may be later than the census row's.
    build = original.pop("build")
    runs.append({"name": "original", "expect": "verified", **original})
    with tempfile.TemporaryDirectory(prefix="sqverify-fast-control-") as scratch:
        # Every mass scaled by 99/100, at every direction of the net (FC-1 of the 6
        # October re-check): the least-bound direction is chosen by the branch and
        # bound's termination margin, and the certificate may have more than 1% slack
        # there, so a run at that direction alone may verify a true mutant.
        path = Path(scratch) / f"{case.certificate}-scaled-99-100.json"
        path.write_text(json.dumps(mixed_mutant(raw, factor=CONTROL_SCALE)), encoding="utf-8")
        sweep = scaled_sweep(
            binary,
            raw,
            path,
            case.n,
            factor=CONTROL_SCALE,
            threads=threads,
            premises=premises,
        )
        runs.append(
            {
                "name": "scaled-99-100",
                "mutation": {"factor": str(CONTROL_SCALE)},
                "expect": "refused at some direction",
                "sweep": sweep,
            }
        )
        # The near-threshold mutant at the least-bound leaf, as before.
        path = Path(scratch) / f"{case.certificate}-near-threshold.json"
        path.write_text(json.dumps(mixed_mutant(raw, factor=near)), encoding="utf-8")
        row = direction_row(binary, path, case.n, index)
        row.pop("build")
        # The refusal's witness, evaluated again apart from the crate: the mutant's
        # capture there is the factor times the original's.
        pose = (row.get("witness") or {}).get("exact_pose")
        witness = (
            near * mixed_exact(raw, Fraction(pose[0]), Fraction(pose[1]), index)
            if pose
            else None
        )
        runs.append(
            {
                "name": "near-threshold",
                "mutation": {
                    "factor": str(near),
                    "capture_at_centre": str(exact * near),
                    "capture_at_witness": None if witness is None else str(witness),
                    "witness_captures_agree": witness is not None
                    and (row.get("witness") or {}).get("exact_coverage") is not None
                    and Fraction((row.get("witness") or {})["exact_coverage"]) == witness,
                    "centre_in_domain": format_m and in_domain(raw, index, least["centre"]),
                    "witness_in_domain": format_m and in_domain(raw, index, pose),
                },
                "expect": "refused",
                **row,
            }
        )

    agree = exact == crate
    return {
        "kind": "sqverify-fast-control/v2",
        "packet": case.packet,
        "certificate": case.certificate,
        "n": case.n,
        "L": case.side,
        "candidate_sha256": sha256(case.candidate),
        "binary_sha256": sha256(binary),
        "build": build,
        "index": index,
        "centre": least["centre"],
        "exact_capture_crate": str(crate),
        "exact_capture_independent": str(exact),
        "captures_agree": agree,
        "runs": runs,
        "status": (
            "CONTROLS_REFUSED"
            if all(map(control_run_held, runs)) and agree
            else "CONTROL_FAILED"
        ),
    }


def rectangle_control(
    binary: Path, case: Case, entry: dict[str, Any], out: Path | None
) -> dict[str, Any]:
    """Negative controls on a verified format T certificate (receipt kind v1), as the
    review of the format T route accepted them: the original and both mutants at
    Tokoharu's threshold, which the census row records and the rectangle family passes,
    at the tightest least-bound leaf centre the row's receipts in `out` record
    (`tightest_centre`)."""
    if not entry.get("threshold"):
        raise SystemExit(
            f"{case.certificate}: a format T row records no threshold; re-run it on "
            "reviewed source before a control"
        )
    threshold = Fraction(str(entry["threshold"]))
    passed = str(threshold)
    raw = read_raw(case.candidate)
    # The exact evaluator takes the step from the file; the row was decided on the net
    # admission read. They must be one net, or the control is of another certificate.
    decided = (entry.get("premises") or {}).get("D")
    if decided is None or Fraction(str(decided)) != net_step(raw):
        raise SystemExit(
            f"{case.certificate}: the row's net step {decided} is not the file's "
            f"{net_step(raw)}; the control would evaluate another net"
        )
    if out is None:
        raise SystemExit(f"{case.certificate}: a format T control reads the receipts")
    receipts = out / case.packet / f"{case.certificate}.jsonl.gz"
    index, centre, exact, crate, weighed = tightest_centre(binary, case, raw, receipts)
    # Rounded down, so the capture at the centre is at most the threshold less
    # NEAR_THRESHOLD of it.
    near = Fraction(int(threshold * (1 - NEAR_THRESHOLD) / exact * 10**15), 10**15)
    runs: list[dict[str, Any]] = []
    original = direction_row(binary, case.candidate, case.n, index, passed)
    # The build the controls ran on, which may be later than the census row's.
    build = original.pop("build")
    runs.append({"name": "original", "expect": "verified", **original})
    with tempfile.TemporaryDirectory(prefix="sqverify-fast-control-") as scratch:
        for name, factor in (("scaled-99-100", CONTROL_SCALE), ("near-threshold", near)):
            path = Path(scratch) / f"{case.certificate}-{name}.json"
            path.write_text(json.dumps(mutant(case, raw, factor)), encoding="utf-8")
            row = direction_row(binary, path, case.n, index, passed)
            row.pop("build")
            # The refusal's witness, evaluated again apart from the crate: the mutant's
            # capture there is the factor times the original's.
            pose = (row.get("witness") or {}).get("exact_pose")
            witness = (
                factor * exact_capture(case, raw, Fraction(pose[0]), Fraction(pose[1]), index)
                if pose
                else None
            )
            runs.append(
                {
                    "name": name,
                    "mutation": {
                        "factor": str(factor),
                        "capture_at_centre": str(exact * factor),
                        "capture_at_witness": None if witness is None else str(witness),
                    },
                    "expect": "refused",
                    **row,
                }
            )

    def held(run: dict[str, Any]) -> bool:
        if run["expect"] == "verified":
            return run["returncode"] == 0 and run["verdict"] == "verified"
        # Refused, and the mutant's claim is false at a centre this tool evaluated
        # exactly: the control centre, or the refusal's witness.
        mutation = run["mutation"]
        uncovered = Fraction(mutation["capture_at_centre"]) < threshold or (
            mutation["capture_at_witness"] is not None
            and Fraction(mutation["capture_at_witness"]) < threshold
        )
        return run["returncode"] == 1 and run["verdict"] not in (None, "verified") and uncovered

    agree = exact == crate
    return {
        "kind": "sqverify-fast-control/v1",
        "packet": case.packet,
        "certificate": case.certificate,
        "n": case.n,
        "L": case.side,
        "threshold": str(threshold),
        "candidate_sha256": sha256(case.candidate),
        "binary_sha256": sha256(binary),
        "build": build,
        "index": index,
        "centre": centre,
        "selection": "tightest least-bound leaf centre",
        "centres_weighed": weighed,
        "exact_capture_crate": str(crate),
        "exact_capture_independent": str(exact),
        "captures_agree": agree,
        "runs": runs,
        "status": "CONTROLS_REFUSED" if all(map(held, runs)) and agree else "CONTROL_FAILED",
    }


def control_run_held(run: dict[str, Any]) -> bool:
    """One run of a v2 control receipt: the original verified; the 99/100 sweep held; the
    near-threshold mutant refused on coverage (a counterexample candidate whose witness
    the crate confirmed below the threshold, its exact capture there this tool's, CR-3),
    with its claim false at a centre in the domain that this tool evaluated exactly: the
    least-bound leaf's centre, or the refusal's witness (CC-1, CC-2)."""
    if run["expect"] == "verified":
        return run["returncode"] == 0 and run["verdict"] == "verified"
    if "sweep" in run:
        return sweep_held(run["sweep"])
    mutation = run["mutation"]
    at_centre = (
        mutation["centre_in_domain"] is True and Fraction(mutation["capture_at_centre"]) < 1
    )
    at_witness = (
        mutation["witness_in_domain"] is True
        and mutation["capture_at_witness"] is not None
        and Fraction(mutation["capture_at_witness"]) < 1
    )
    return (
        run["returncode"] == 1
        and run["verdict"] == CANDIDATE
        and run.get("exact_below_threshold") is True
        and mutation.get("witness_captures_agree") is True
        and (at_centre or at_witness)
    )


def control_status(case: Case, out: Path) -> str | None:
    """A control receipt's status, or None where none is kept."""
    path = out / case.packet / f"{case.certificate}.control.json"
    if not path.is_file():
        return None
    return str(json.loads(path.read_text(encoding="utf-8")).get("status"))


#: The register's evidence, read by `--evidence` for each certificate's reported entry.
EVIDENCE = PROJECT / "frontier/evidence.yaml"
#: The review that accepted a census row and a control receipt as a complete replay here,
#: and says which certificates the route carries to (Carrying the Route).
ROUTE_REVIEW = (
    "docs/project/reviews/review-2026-10-05-wand125-october-5-and-independent-replays.md"
)
#: The soundness review of the crate, with its re-review accepting it at 4ddf37d9c.
SOUNDNESS_REVIEW = "docs/project/reviews/review-2026-10-03-sqverify-fast-soundness.md"
#: The soundness review of the declared-net change (lemma N0, f007d7afd and 910b6b12c).
DECLARED_NET_REVIEW = (
    "docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-soundness.md"
)
#: The review that accepted a census row and a control receipt of a format T certificate,
#: at Tokoharu's threshold and centre domain, as a complete replay here, and says which
#: certificates that route carries to.
FORMAT_T_ROUTE_REVIEW = "docs/project/reviews/review-2026-10-06-sqverify-fast-format-t-route.md"


@dataclass(frozen=True)
class ReviewedSource:
    """A crate source a soundness review accepted, named by the digest `build.rs` takes."""

    #: The commit at which the reviewed source stands.
    commit: str
    #: The review that accepted it.
    review: str
    #: What `--evidence` says of a build of it, after its digest.
    statement: str
    #: Whether the review read the declared-net path (`proof_net`, lemma N0), so that a
    #: row on a declared net built from this source may stand as a replay.
    declared_nets: bool


#: Every crate source a soundness review accepted, by its `source_sha256`, which
#: `build.rs` takes over Cargo.toml, Cargo.lock, build.rs and src/*.rs and every receipt
#: names. `tests/test_sqverify_fast_census.py` admits a census row as evidence only for a
#: build of one of these, and `--evidence` names the one a row was built from.
#: `check_sqverify_fast.crate_source_sha256` computes a tree's digest by the same rule.
REVIEWED_SOURCES: dict[str, ReviewedSource] = {
    # The source the two reviews of 3 October accepted (the soundness review's 7, and the
    # testing and independence review).
    "9985c465116631570c873ecc33af126adc6f14c7429a5ed44d922254d3c7f8a7": ReviewedSource(
        commit="4ddf37d9c",
        review=SOUNDNESS_REVIEW,
        statement=(
            "the crate source at 4ddf37d9c, the build the two reviews of 3 October accepted"
        ),
        declared_nets=False,
    ),
    # The same src/, Cargo.lock and build.rs, with the gate's test profile in Cargo.toml,
    # which the release binary does not use (IR-4 of the route review); through e020eb1e2.
    "7c49cf79f2408e745d5a0759caf85768d92c502bb574b95dbc12b81a36e50300": ReviewedSource(
        commit="e020eb1e2",
        review=ROUTE_REVIEW,
        statement=(
            "its src/, Cargo.lock and build.rs are unchanged since 4ddf37d9c, the build the "
            "two reviews of 3 October accepted, and the digest differs from that build's "
            "9985c465... only because Cargo.toml gained the gate's test profile, which the "
            "release binary does not use"
        ),
        declared_nets=False,
    ),
    # main's crate at 910b6b12c (34e87a86b): the declared net of format M (proof_net,
    # lemma N0, f007d7afd) with the fixes of the 5 October declared-net review's DN-2,
    # DN-4 to DN-6 and DN-9 (910b6b12c). Its soundness review of 6 October read the whole
    # diff from e020eb1e2 and accepted the crate for standard-net certificates, and for a
    # format M certificate on a declared net once the control's evaluator read that net
    # (its DR-1, fixed at 36b52538a with DR-2 and DR-3) and the fix had been read, which
    # the same day's re-check did:
    # docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-fix-check.md.
    "d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88": ReviewedSource(
        commit="910b6b12c",
        review=DECLARED_NET_REVIEW,
        statement=(
            "the crate source at 910b6b12c: the source of e020eb1e2 (7c49cf79...) with the "
            "declared net of format M (proof_net, SOUNDNESS.md lemma N0) and its review fixes, "
            f"a diff the soundness review {DECLARED_NET_REVIEW} read in full and accepted"
        ),
        declared_nets=True,
    ),
}


def reviewed_source(entry: dict[str, Any]) -> ReviewedSource | None:
    """The reviewed source a census row's build was made from, or None."""
    return REVIEWED_SOURCES.get(str((entry.get("build") or {}).get("source_sha256", "")))


def net_assumption(premises: dict[str, Any]) -> str:
    """The net a format M replay entry assumes, as admission read it."""
    origin = premises.get("net_origin", "standard")
    which = (
        "the net its candidate declares (proof_net), lemma N0 of SOUNDNESS.md,"
        if origin == "proof_net"
        else "the standard net"
    )
    return (
        f"Every angle and legal centre is covered by {which} of {premises['angle_count']}"
        f" half-angles of step {premises['D']} at core side {premises['B']} and format M's"
        " per-bin centre domains, which admission checks in exact rationals."
    )


#: The assumptions every format M replay entry states beside its mass and its net.
ASSUMPTIONS = (
    (
        "Binary64 arithmetic has IEEE-754 semantics with directed rounding per operation,"
        " as SOUNDNESS.md's Floating Point section uses it."
    ),
    (
        "The candidate is the retained file whose decompressed SHA-256 the packet's"
        " acquisition record pins, which mixed-fetch found identical to the proof bundle's."
    ),
)


def folded(key: str, text: str, indent: int = 4) -> list[str]:
    """A YAML folded block, wrapped as the register's hand-written entries are."""
    body = textwrap.wrap(
        text, width=90 - indent, break_long_words=False, break_on_hyphens=False
    )
    return [f"{' ' * indent}{key}: >-", *(f"{' ' * (indent + 2)}{line}" for line in body)]


def thread_count(entry: dict[str, Any]) -> str:
    """The threads a census row ran at, in words: `one thread`, `two threads`."""
    threads = int(entry.get("threads") or 1)
    word = {1: "one", 2: "two", 3: "three", 4: "four"}.get(threads, str(threads))
    return f"{word} thread{'' if threads == 1 else 's'}"


def scaled_control_text(index: int, run: dict[str, Any]) -> str:
    """The 99/100 control in an evidence entry: at the least-bound direction in a
    `sqverify-fast-control/v1` receipt, at every direction of the net in v2 (FC-1)."""
    if "sweep" not in run:
        return (
            f"Controls at index {index}: the original verified again, every mass scaled by "
            f"99/100 refused ({run['verdict']}, {uncovered(run)}), "
        )
    sweep = run["sweep"]
    refused, verified = len(sweep["refused"]), len(sweep["verified_directions"])
    slack = (
        f"; the mutant verified at the other {verified}, where by the verifier's own "
        "decision the original captures at least 100/99"
        if verified
        else ""
    )
    return (
        f"Controls: the original verified again at index {index}; every mass scaled by "
        f"99/100 refused at {refused} of the {sweep['directions']} net directions, each a "
        "coverage refusal at a centre in the per-bin domain where the mutant's exact capture "
        "is below 1 (the crate's confirmed witness, or at the axis the vertex sweep's least "
        f"vertex){slack}; "
    )


def near_factor(run: dict[str, Any]) -> str:
    """The near-threshold mutant's scale, to four places (CC-8): it may cut deeper than
    99/100."""
    return f"{float(Fraction(run['mutation']['factor'])):.4f}"


def uncovered(run: dict[str, Any]) -> str:
    """Where a control's mutant was shown, exactly, to capture less than 1."""
    mutation = run["mutation"]
    if Fraction(mutation["capture_at_centre"]) < 1:
        return "exact capture below 1 at the least-bound leaf's centre"
    return "exact capture below 1 at its witness"


def evidence_entry(
    case: Case, out: Path, entry: dict[str, Any], *, audit_record: str, date: str
) -> str:
    """The replay evidence entry for one verified, controlled certificate, as YAML text.

    It names the certificate's reported entry, takes its source key and scope, and states
    the census row and the control receipt in its limitations. A records lane pastes it
    into `frontier/evidence.yaml` and widens the scope where the bound carries by mass.
    """
    if rectangle_family(case):
        return rectangle_evidence_entry(case, out, entry, audit_record=audit_record, date=date)
    register = safe_load(EVIDENCE.read_text(encoding="utf-8"))
    certificate = str(case.candidate.relative_to(PROJECT))
    (report,) = (
        item
        for item in register["evidence"]
        if item.get("assurance") == "reported" and item.get("certificate") == certificate
    )
    premises = entry["premises"]
    built = str((entry.get("build") or {}).get("source_sha256", ""))
    reviewed = reviewed_source(entry)
    declared = premises.get("net_origin") == "proof_net"
    if reviewed is None:
        raise SystemExit(
            f"{case.certificate}: built from crate source {built[:8]}..., which no review "
            "accepted (REVIEWED_SOURCES); rebuild from reviewed source and re-run the row"
        )
    if declared and not reviewed.declared_nets:
        raise SystemExit(
            f"{case.certificate}: a declared net, built from crate source {built[:8]}..., "
            "whose review did not read the declared net; no review of the declared net "
            "accepted it (REVIEWED_SOURCES)"
        )
    receipt = json.loads((out / case.packet / f"{case.certificate}.control.json").read_text())
    if entry.get("status") != "VERIFIED" or receipt.get("status") != "CONTROLS_REFUSED":
        raise SystemExit(f"{case.certificate}: not verified and controlled")
    rows = [
        json.loads(line)
        for line in gzip.decompress(
            (out / case.packet / f"{case.certificate}.jsonl.gz").read_bytes()
        )
        .decode()
        .splitlines()
    ]
    axis = next(row for row in rows if row.get("r") == 0)
    oblique = min(
        (row for row in rows if int(row.get("r", 0)) >= 1),
        key=lambda row: row["min_certified_lower_bound"],
    )
    directions = int(premises["angle_count"])
    runs = {run["name"]: run for run in receipt["runs"]}
    side = Fraction(case.side)
    mass = Fraction(premises["mass_exact"])
    identifier = str(report["id"]).removesuffix("-report") + "-sqverify-fast-replay"
    packet_path = f"benchmarks/measure-verifier/census-mixed/{case.packet}/{case.certificate}"
    replay = (
        "From packing/, in a tree whose crate is reviewed source (.venv/bin/python3 -m "
        "devtools.sqverify_fast_census --source-digest prints its source_sha256 and exits 0; "
        f"these receipts' build is {built[:8]}..., the source at {reviewed.commit}), after "
        "cargo build --release in sqverify_fast/ (toolchain 1.98.0): "
        ".venv/bin/python3 -m devtools.sqverify_fast_census --family mixed --binary "
        "sqverify_fast/target/release/sqverify-fast --out "
        f"benchmarks/measure-verifier/census-mixed --threads 2 --only {case.certificate} "
        f"runs sqverify-fast on the retained candidate at all {directions} directions of "
        f"{'the net it declares' if declared else 'the standard net'} at the "
        "threshold it declares, 1, and records the case in census.json there; "
        f"--check --only {case.certificate} must then print 1 of 1 retained certificates "
        "VERIFIED (every direction verified, summary VERIFIED, exit 0, and the exact capture "
        "at the least-bound leaf's centre at least 1). The same command with --control in "
        "place of --threads 2 must write status CONTROLS_REFUSED. The receipts are "
        f"{packet_path}.jsonl.gz and {packet_path}.control.json, held by "
        "tests/test_sqverify_fast_census.py, which admits the row only for a build of "
        "reviewed source."
    )
    least = entry["least_bound_leaf_exact"]
    stored = str(entry["candidate_sha256"])
    pinned = hashlib.sha256(gzip.decompress(case.candidate.read_bytes())).hexdigest()
    net = (
        f"the net its candidate declares (proof_net), of {directions} half-angles of step "
        f"{premises['D']}, with B(1 + D) = {premises.get('shrink_bound')} < 1 and the last "
        f"tangent {premises.get('net_last_tangent')} past tan(pi/8) and at most 1/2 "
        "(SOUNDNESS.md, lemma N0)"
        if declared
        else f"the net of {directions} half-angles of step {premises['D']}"
    )
    limitations = (
        "sqverify-fast, this repository's clean-room measure verifier, decided the retained "
        f"candidate {case.certificate} at all {directions} net directions on {date}. The "
        f"receipts name the stored gzip file's SHA-256 {stored[:8]}..., which decompresses "
        f"to the SHA-256 {pinned[:8]}... the packet's acquisition record pins "
        "(devtools.retained_data check ties the two). Admission recomputed in exact "
        f"rationals n = {case.n}, L = {side}, the total mass {mass} < {case.n}, the core "
        f"side {premises['B']} with B(1 + D/(1 - D^2/4)) < 1 and {net}, from "
        f"{premises['source_rectangles']} "
        f"rectangle rows ({premises['expanded_rectangles']:,} distinct images) and no point "
        "or segment, and took format M's per-bin centre domain, at threshold 1. The axis "
        f"direction was decided by an exact-event vertex sweep over {axis['vertices']:,} "
        f"vertices, least certified capture {axis['min_certified_lower_bound']!r}; the other "
        f"{directions - 1} by interval branch and bound over {entry['nodes']:,} boxes, least "
        f"certified lower bound {oblique['min_certified_lower_bound']!r} at index "
        f"{oblique['r']}; "
        f"the exact capture at the least-bound leaf's centre (index {least['r']}) is "
        f"{float(Fraction(least['exact_coverage'])):.10f}. Every direction verified, "
        f"summary VERIFIED, exit 0, {float(entry['cpu_seconds']):,.0f} CPU seconds at "
        f"{thread_count(entry)} and {float(entry['wall_seconds']):,.0f} seconds of wall time "
        "on a shared "
        "4-core x86-64 Linux container under load. The build is rustc 1.98.0, release, "
        f"x86-64 Linux, source_sha256 {built[:8]}...: {reviewed.statement}. "
        "It decides coverage independently of the source's checker: the crate was written "
        "without opening it (packing/sqverify_fast/INDEPENDENCE.md) and shares no code with "
        "it. It shares the theorem, the net, the core side, the per-bin domain lemma and the "
        "threshold, so a defect in that mathematics would affect both: a second "
        "implementation, not a second method. Its node counts and bounds are its own, not "
        "the certificate's records. "
        + scaled_control_text(receipt["index"], runs["scaled-99-100"])
        + f"and every mass scaled by {near_factor(runs['near-threshold'])} so that the exact "
        "capture at the least-bound leaf's centre is "
        f"at most 1 - 10^-6 refused ({runs['near-threshold']['verdict']}, "
        f"{uncovered(runs['near-threshold'])}); each capture below 1 was evaluated "
        "again by an exact evaluator written apart from the crate, and "
        "tests/test_sqverify_fast_census.py holds the receipts. The source's own checker "
        "was not run here on this certificate, and its tarball is pinned by digest and not "
        "retained."
    )
    scope = ", ".join(str(n) for n in report["scope"]["n_values"])
    # A standard-net row from a later reviewed source: the review that accepted that source.
    later_source = (
        f", and the crate source that ran, at {reviewed.commit}, by {reviewed.review}"
        if reviewed.review not in (SOUNDNESS_REVIEW, ROUTE_REVIEW)
        else ""
    )
    lines = [
        f"  - id: {identifier}",
        "    claim: lower-bound",
        f"    scope: {{n_values: [{scope}]}}",
        "    assurance: verified",
        "    method: interval-certified",
        "    performed_by: repository",
        "    relationship_to_generator: independent-implementation",
        "    origin: replayed-here",
        "    novelty: previously-published",
        f"    source_key: '{report['source_key']}'",
        f"    certificate: {certificate}",
        *folded("replay", replay),
        "    replay_status: passed",
        "    verifiers: [V-sqverify-fast]",
        "    proof:",
        "      source: packing/sqverify_fast/SOUNDNESS.md",
        *folded(
            "theorem",
            "The net-and-shrink measure-capture obstruction of SOUNDNESS.md (The Claim; "
            "Formats M and L, lemma D for format M's per-bin domain), applied to wand125's "
            f"{case.certificate}: no {case.n} unit squares pack in a square of side {side}, "
            f"so s({case.n}) >= {side}.",
            indent=6,
        ),
        (
            "      scope: Unrestricted square packing with disjoint interiors and arbitrary"
            " rotations."
        ),
        *folded(
            "pinpoints",
            f"SOUNDNESS.md's theorem and lemmas, accepted with the crate by {SOUNDNESS_REVIEW}"
            + (
                f", and lemma N0 and the declared-net change by {DECLARED_NET_REVIEW}"
                if declared
                else later_source
            )
            + f"; the certificate's mathematics read in {audit_record}; "
            + (
                ""
                if audit_record == ROUTE_REVIEW
                else f"the census route accepted as a complete replay here in {ROUTE_REVIEW}; "
            )
            + "the census row, receipts and control receipt named in replay.",
            indent=6,
        ),
        "      assumptions:",
        (
            f"        - The density is nonnegative and exact, of total mass {mass} < {case.n},"
            " which admission recomputes from the retained candidate."
        ),
        f"        - {net_assumption(premises)}",
        *(f"        - {assumption}" for assumption in ASSUMPTIONS),
        f"      audit_record: {audit_record}",
        *folded("limitations", limitations),
        f"    source_reviewed: '{date}'",
    ]
    return "\n".join(lines) + "\n"


def packet_report(case: Case, register: dict[str, Any]) -> dict[str, Any]:
    """The reported evidence entry of a format T certificate's packet.

    The rectangle packets are registered by packet, not by certificate: one reported
    entry whose `certificate` is the packet's certificate directory, beside a monotone
    entry for the counts its masses reach. This is the first, and its scope may be
    narrower than the packet, since `apply_wand125_rectangles` keeps it to the cases that
    cite it.
    """
    directory = str(case.candidate.parent.parent.relative_to(PROJECT))
    (report,) = (
        item
        for item in register["evidence"]
        if item.get("assurance") == "reported"
        and item.get("certificate") == directory
        and "monotone" not in str(item["id"])
    )
    return report


def rectangle_evidence_entry(
    case: Case, out: Path, entry: dict[str, Any], *, audit_record: str, date: str
) -> str:
    """The replay evidence entry for one verified, controlled format T certificate.

    The mixed family's entry, with format T's premises: Tokoharu's centre domain, the
    threshold 10001/10000 the census passes, and a mass of n - 1/100. Its source key is
    the packet's reported entry's, its scope the certificate's own count; a records lane
    widens it where the bound carries by mass and a result claims the larger count.
    """
    register = safe_load(EVIDENCE.read_text(encoding="utf-8"))
    certificate = str(case.candidate.relative_to(PROJECT))
    report = packet_report(case, register)
    premises = entry["premises"]
    built = str((entry.get("build") or {}).get("source_sha256", ""))
    reviewed = reviewed_source(entry)
    if reviewed is None:
        raise SystemExit(
            f"{case.certificate}: built from crate source {built[:8]}..., which no review "
            "accepted (REVIEWED_SOURCES); rebuild from reviewed source and re-run the row"
        )
    receipt = json.loads((out / case.packet / f"{case.certificate}.control.json").read_text())
    if entry.get("status") != "VERIFIED" or receipt.get("status") != "CONTROLS_REFUSED":
        raise SystemExit(f"{case.certificate}: not verified and controlled")
    controlled = str((receipt.get("build") or {}).get("source_sha256", ""))
    control_source = REVIEWED_SOURCES.get(controlled)
    if control_source is None:
        raise SystemExit(
            f"{case.certificate}: its controls ran on crate source {controlled[:8]}..., "
            "which no review accepted (REVIEWED_SOURCES)"
        )
    rows = [
        json.loads(line)
        for line in gzip.decompress(
            (out / case.packet / f"{case.certificate}.jsonl.gz").read_bytes()
        )
        .decode()
        .splitlines()
    ]
    axis = next(row for row in rows if row.get("r") == 0)
    oblique = min(
        (row for row in rows if int(row.get("r", 0)) >= 1),
        key=lambda row: row["min_certified_lower_bound"],
    )
    directions = int(premises["angle_count"])
    runs = {run["name"]: run for run in receipt["runs"]}
    side = Fraction(case.side)
    mass = Fraction(premises["mass_exact"])
    threshold = Fraction(entry["threshold"])
    digits = case.certificate.rsplit("_L", 1)[1]
    identifier = f"E-n{case.n:03d}-wand125-rect-{digits}-sqverify-fast-replay"
    packet_path = f"benchmarks/measure-verifier/census/{case.packet}/{case.certificate}"
    controls_built = (
        "the same build"
        if controlled == built
        else (
            f"a build of crate source {controlled[:8]}..., {control_source.statement}, "
            f"binary {str(receipt['binary_sha256'])[:8]}..., whose format T path is the "
            f"row's build's ({FORMAT_T_ROUTE_REVIEW} read the diff)"
        )
    )
    replay = (
        "From packing/, in a tree whose crate is reviewed source (.venv/bin/python3 -m "
        "devtools.sqverify_fast_census --source-digest prints its source_sha256 and exits 0; "
        f"this row's build is {built[:8]}..., the source at {reviewed.commit}), after "
        "cargo build --release in sqverify_fast/ (toolchain 1.98.0): "
        ".venv/bin/python3 -m devtools.sqverify_fast_census --binary "
        "sqverify_fast/target/release/sqverify-fast --out "
        f"benchmarks/measure-verifier/census --threads 2 --only {case.certificate} "
        f"runs sqverify-fast on the retained candidate at all {directions} directions of "
        f"the standard net at Tokoharu's threshold {threshold}, which the rectangle family "
        "passes, and records the case in census.json there; "
        f"--check --only {case.certificate} must then print 1 of 1 retained certificates "
        "VERIFIED (every direction verified, summary VERIFIED, exit 0, and the exact capture "
        "at the least-bound leaf's centre at least the threshold). The same command with "
        "--control in place of --threads 2 must write status CONTROLS_REFUSED. The receipts "
        f"are {packet_path}.jsonl.gz and {packet_path}.control.json, held by "
        "tests/test_sqverify_fast_census.py, which admits the row only for a build of "
        "reviewed source."
    )
    least = entry["least_bound_leaf_exact"]
    stored = str(entry["candidate_sha256"])
    pinned = hashlib.sha256(gzip.decompress(case.candidate.read_bytes())).hexdigest()
    limitations = (
        "sqverify-fast, this repository's clean-room measure verifier, decided the retained "
        f"candidate {case.certificate} at all {directions} net directions. The receipts "
        f"name the stored gzip file's SHA-256 {stored[:8]}..., which decompresses to the "
        f"SHA-256 {pinned[:8]}... the packet's README pins (devtools.retained_data check "
        "ties the two). Admission recomputed in exact rationals n = "
        f"{case.n}, L = {side}, the total mass {mass} < {case.n}, the core side "
        f"{premises['B']} with B(1 + D) < 1 and the net of {directions} half-angles of step "
        f"{premises['D']}, from {premises['source_rectangles']} rectangle orbits "
        f"({premises['expanded_rectangles']:,} distinct images) and no point or segment, and "
        f"took format T's centre domain (Tokoharu's), at threshold {threshold}; the file's "
        "metadata restates that net, and no other field of it but the weights and "
        "rectangles was read for the decision. The axis "
        f"direction was decided by an exact-event vertex sweep over {axis['vertices']:,} "
        f"vertices, least certified capture {axis['min_certified_lower_bound']!r}; the other "
        f"{directions - 1} by interval branch and bound over {entry['nodes']:,} boxes, least "
        f"certified lower bound {oblique['min_certified_lower_bound']!r} at index "
        f"{oblique['r']}; the exact capture at the least-bound leaf's centre (index "
        f"{least['r']}) is {float(Fraction(least['exact_coverage'])):.10f}. Every direction "
        f"verified, summary VERIFIED, exit 0, {float(entry['cpu_seconds']):,.0f} CPU "
        f"seconds at {entry['threads']} threads and {float(entry['wall_seconds']):,.0f} "
        "seconds of wall time on a shared x86-64 Linux host, load average "
        f"{float(entry['load_before']):.1f} when it began. The build is rustc 1.98.0, "
        f"release, x86-64 Linux, source_sha256 {built[:8]}...: {reviewed.statement}. "
        "It decides coverage independently of the source's checker: the crate was written "
        "without opening it (packing/sqverify_fast/INDEPENDENCE.md) and shares no code with "
        "it. It shares the theorem, the net, the core side, Tokoharu's centre domain and the "
        "threshold, so a defect in that mathematics would affect both: a second "
        "implementation, not a second method, and one that needs no smoothing margin. Its "
        "node counts and bounds are its own, not the certificate's records. Controls on "
        f"{date}, on {controls_built}, at threshold "
        f"{threshold} at index {receipt['index']}, at the least-bound leaf centre of least "
        f"exact capture over the {receipt['centres_weighed']} oblique directions "
        f"({float(Fraction(receipt['exact_capture_independent'])):.10f}): the original "
        "verified again there, every weight scaled by 99/100 refused "
        f"({runs['scaled-99-100']['verdict']}, "
        f"{uncovered_below(runs['scaled-99-100'], threshold)}), and every weight scaled so "
        "that the exact capture at that centre is at most the threshold less 10^-6 of it "
        f"refused ({runs['near-threshold']['verdict']}, "
        f"{uncovered_below(runs['near-threshold'], threshold)}); each capture was evaluated "
        "again by sqpack.rectangle_density, an exact evaluator written before the crate "
        "and sharing no code with it, which the crate's authors read in full "
        "(INDEPENDENCE.md), so the agreement does not exclude a misreading of the format "
        "common to both; the exact preflight pins that reading apart from either, since "
        "the checker input it regenerates from the candidate hashes to the digest the "
        "source's accepting run recorded. tests/test_sqverify_fast_census.py holds the "
        f"receipts. The review of the format T route, {FORMAT_T_ROUTE_REVIEW}, re-ran "
        "three directions on a binary of the control build, which reproduced the census "
        "receipts field for field, and recomputed two receipts' captures with its own exact "
        "code. "
        + (
            "The source's own checker was also replayed here in full on this certificate, "
            "a reproduction with the producer's code recorded in the packet's "
            "receipts/replay."
            if source_replayed(case)
            else "The source's own checker was not run here on this certificate, and its "
            "records are not reproduced."
        )
    )
    scope = str(case.n)
    lines = [
        f"  - id: {identifier}",
        "    claim: lower-bound",
        f"    scope: {{n_values: [{scope}]}}",
        "    assurance: verified",
        "    method: interval-certified",
        "    performed_by: repository",
        "    relationship_to_generator: independent-implementation",
        "    origin: replayed-here",
        "    novelty: previously-published",
        f"    source_key: '{report['source_key']}'",
        f"    certificate: {certificate}",
        *folded("replay", replay),
        "    replay_status: passed",
        "    verifiers: [V-sqverify-fast]",
        "    proof:",
        "      source: packing/sqverify_fast/SOUNDNESS.md",
        *folded(
            "theorem",
            "The net-and-shrink measure-capture obstruction of SOUNDNESS.md (The Claim; "
            "format T, with Tokoharu's centre domain), applied to wand125's "
            f"{case.certificate}: no {case.n} unit squares pack in a square of side {side}, "
            f"so s({case.n}) >= {side}.",
            indent=6,
        ),
        (
            "      scope: Unrestricted square packing with disjoint interiors and arbitrary"
            " rotations."
        ),
        *folded(
            "pinpoints",
            f"SOUNDNESS.md's theorem and lemmas, accepted with the crate by {SOUNDNESS_REVIEW}"
            f"; the certificate's mathematics read in {audit_record}; the census route for "
            f"format T accepted as a complete replay here in {FORMAT_T_ROUTE_REVIEW}; the "
            "census row, receipts and control receipt named in replay.",
            indent=6,
        ),
        "      assumptions:",
        (
            f"        - The density is nonnegative and exact, of total mass {mass} < {case.n},"
            " which admission recomputes from the retained candidate."
        ),
        (
            "        - Every angle and legal centre is covered by the standard net of "
            f"{directions} half-angles of step {premises['D']} at core side {premises['B']} "
            "and format T's centre domain, which admission checks in exact rationals."
        ),
        f"        - {ASSUMPTIONS[0]}",
        (
            "        - The candidate is the retained file whose decompressed SHA-256 the"
            " packet's README pins, from the source revision the packet's acquisition"
            " record names."
        ),
        f"      audit_record: {audit_record}",
        *folded("limitations", limitations),
        f"    source_reviewed: '{date}'",
    ]
    return "\n".join(lines) + "\n"


def uncovered_below(run: dict[str, Any], threshold: Fraction) -> str:
    """Where a control's mutant was shown, exactly, to capture less than the threshold."""
    mutation = run["mutation"]
    if Fraction(mutation["capture_at_centre"]) < threshold:
        return "exact capture below the threshold at that centre"
    return "exact capture below the threshold at its witness"


def source_replayed(case: Case) -> bool:
    """Whether the packet's receipt records a passed complete replay of this format T
    certificate by the source's own checker (`devtools.audit_wand125_rectangles`)."""
    receipt = case.candidate.parents[3] / "receipts/replay/audit.json"
    if not receipt.is_file():
        receipt = receipt.with_name("audit.json.gz")
    if not receipt.is_file():
        return False
    data = receipt.read_bytes()
    record = json.loads(gzip.decompress(data) if data[:2] == b"\x1f\x8b" else data)
    return any(
        item.get("certificate") == case.certificate
        and item.get("status") == "PASS"
        and (item.get("replay") or {}).get("status") == "PASS"
        and ((item.get("replay") or {}).get("summary") or {}).get("angle_cases")
        == STANDARD_DIRECTIONS
        for item in record.get("cases", [])
    )


def replay_reference() -> dict[str, dict[str, Any]]:
    """The authors' checker's replay summaries, by certificate name."""
    reference: dict[str, dict[str, Any]] = {}
    density = WEB / "external-square-certificates-2026-09-22/receipts/density/audit.json"
    names = {(n, side): name for name, n, side in TOKOHARU_CASES}
    for case in json.loads(density.read_text(encoding="utf-8"))["cases"]:
        name = names.get((int(case["n"]), str(case["L"])))
        if name is not None:
            reference[name] = case["replay"]
    for packet in PACKETS:
        folder = WEB / f"wand125-rectangle-certificates-{packet}/receipts/replay"
        for name in ("audit.json", "audit.json.gz"):
            receipt = folder / name
            if not receipt.is_file():
                continue
            raw = receipt.read_bytes()
            text = gzip.decompress(raw) if name.endswith(".gz") else raw
            for case in json.loads(text)["cases"]:
                replay = case.get("replay")
                if isinstance(replay, dict) and (
                    (replay.get("summary") or {}).get("status") == "VERIFIED"
                ):
                    reference[case["certificate"]] = replay
    return reference


def workers_of(command: object) -> str:
    if isinstance(command, list):
        words = [str(word) for word in command]
        if "--workers" in words:
            return words[words.index("--workers") + 1]
    return "?"


def render_report(census: dict[str, Any]) -> str:
    """The census as a Markdown table, generated from census.json and the receipts."""
    reference = replay_reference()
    lines = [
        "# Milestone A Census",
        "",
        "Generated by `python -m devtools.sqverify_fast_census --report`; do not edit by hand.",
        "",
        "Every retained rectangle-density certificate (format T), verified by",
        "`sqverify-fast` at all 201 net directions at the threshold",
        f"{census['threshold']}. *Authors' replay here* says whether this repository holds a",
        "complete replay by the authors' checker; where it holds none, this census is the",
        "first complete check here. *Nodes* counts boxes at $r \\ge 1$; the authors' count",
        "also includes the axis direction's vertices, given here as *axis vertices*.",
        "*Exact leaf* is the exact rational capture at the centre of the least-bound leaf",
        "of the least-bound direction, which must clear the threshold. CPU is user plus system",
        "time of the whole process (`wait4`), on a shared host whose load average is given.",
        "The replay wall is the authors' checker's recorded wall time with the worker count",
        "it ran with, so it is not a CPU figure.",
        "",
        (
            "| Certificate | n | Status | Directions | Nodes | Axis vertices | Authors' nodes"
            " | Least certified bound | Exact leaf | CPU s | Load | Authors' replay here"
            " | Authors' replay wall s (workers) |"
        ),
        "|" + "|".join(f" {align} " for align in RECT_ALIGN.split()) + "|",
    ]
    total_cpu = 0.0
    verified = 0
    for name in sorted(census["cases"], key=lambda key: (census["cases"][key]["n"], key)):
        case = census["cases"][name]
        replay = reference.get(name, {})
        summary = replay.get("summary", {})
        least = case.get("least_bound_leaf_exact") or {}
        wall = summary.get("wall_seconds")
        wall_text = (
            f"{float(Fraction(wall)):.0f} ({workers_of(replay.get('command'))})"
            if wall
            else "-"
        )
        total_cpu += float(case.get("cpu_seconds") or 0.0)
        verified += case.get("status") == "VERIFIED"
        cpu = float(case.get("cpu_seconds") or 0.0)
        cells = [
            f"`{name}`",
            str(case["n"]),
            str(case.get("status")),
            str(case.get("directions_verified")),
            f"{case.get('nodes'):,}",
            f"{case.get('axis_vertices') or 0:,}",
            f"{int(summary.get('nodes', 0)):,}" if summary else "-",
            str(case.get("least_certified_bound")),
            "clears" if least.get("clears_threshold") else "FAILS",
            f"{cpu:.1f}",
            f"{float(case.get('load_before') or 0.0):.1f}",
            "complete" if summary else "none: first complete check here",
            wall_text,
        ]
        lines.append("| " + " | ".join(cells) + " |")
    count = len(census["cases"])
    lines += [
        "",
        f"{verified} of {count} certificates verified; {total_cpu:.0f} CPU seconds in all.",
        "",
        "<!-- This document follows common-doc-guidelines.md.",
        "See github.com/jlevy/practical-prose and review guidelines before editing.",
        "-->",
        "",
    ]
    return "\n".join(lines)


RECT_ALIGN = "--- ---: --- ---: ---: ---: ---: --- --- ---: ---: --- ---:"
MIXED_ALIGN = "--- ---: --- --- ---: ---: --- --- ---: ---: --- ---: ---: ---: ---"


def render_mixed_report(census: dict[str, Any], out: Path) -> str:
    """The mixed census as a Markdown table, beside the authors' replays."""
    cases = {case.certificate: case for case in mixed_cases()}
    lines = [
        "# Milestone B Census",
        "",
        "Generated by `python -m devtools.sqverify_fast_census --family mixed --report`;",
        "do not edit by hand.",
        "",
        "Every retained certificate of formats M (rectangle rows, per-bin centre domain) and L",
        "(points, segments and rectangles, Tokoharu's domain), verified by `sqverify-fast` at",
        "every direction of its net (201, unless the file declares its own) at the threshold",
        "the certificate declares, 1. *Replayed directions* are those the authors' checker",
        "replayed in this repository; where there are none, this census is the first",
        "complete check here. *Exact leaf* is the exact rational capture at the centre of",
        "the least-bound leaf of the least-bound direction.",
        "*Authors' CPU* is the authors' checker's recorded CPU seconds on the directions this",
        "repository replayed; *ours, same directions* is `sqverify-fast`'s thread CPU on",
        "exactly those directions. CPU on a shared host whose load average is given.",
        "*Control* is the status of the `--control` receipt on the certificate itself, where",
        "one is kept: the original verified again and a near-threshold mutant refused at its",
        "least-bound direction, and the 99/100 mutant refused at one direction at least,",
        "every direction of the net run (v2), or at that direction alone (v1).",
        "",
        (
            "| Certificate | n | Format | Status | Directions | Nodes | Least certified bound"
            " | Exact leaf | CPU s, all directions | Load | Replayed directions"
            " | Authors' CPU s | Ours, same directions | Ratio | Control |"
        ),
        "|" + "|".join(f" {align} " for align in MIXED_ALIGN.split()) + "|",
    ]
    total_cpu = 0.0
    verified = 0
    for name in sorted(census["cases"], key=lambda key: (census["cases"][key]["n"], key)):
        entry = census["cases"][name]
        case = cases.get(name)
        reference: dict[str, Any] = (
            mixed_reference(case) if case is not None else {"directions": []}
        )
        replayed = reference["directions"]
        ours = sum(
            float((entry.get("direction_cpu_seconds") or {}).get(str(r)) or 0.0)
            for r in replayed
        )
        authors = float(reference.get("cpu_seconds") or 0.0)
        span = (
            f"all {len(replayed)}"
            if case is not None and len(replayed) == net_directions(case)
            else ", ".join(str(r) for r in replayed) or "none: first complete check here"
        )
        if not reference.get("per_direction_cpu", True):
            ours = 0.0
        least = entry.get("least_bound_leaf_exact") or {}
        cpu = float(entry.get("cpu_seconds") or 0.0)
        total_cpu += cpu
        verified += entry.get("status") == "VERIFIED"
        cells = [
            f"`{name}`",
            str(entry["n"]),
            str((entry.get("premises") or {}).get("format")),
            str(entry.get("status")),
            str(entry.get("directions_verified")),
            f"{entry.get('nodes'):,}",
            str(entry.get("least_certified_bound")),
            "clears" if least.get("clears_threshold") else "FAILS",
            f"{cpu:.1f}",
            f"{float(entry.get('load_before') or 0.0):.1f}",
            span,
            f"{authors:,.0f}" if authors > 0 else "-",
            f"{ours:.1f}" if ours > 0 else "-",
            f"{authors / ours:,.0f}x" if ours > 0 and authors > 0 else "-",
            (control_status(case, out) or "-") if case is not None else "-",
        ]
        lines.append("| " + " | ".join(cells) + " |")
    lines += [
        "",
        (
            f"{verified} of {len(census['cases'])} certificates verified;"
            f" {total_cpu:.0f} CPU seconds in all."
        ),
        "",
        "<!-- This document follows common-doc-guidelines.md.",
        "See github.com/jlevy/practical-prose and review guidelines before editing.",
        "-->",
        "",
    ]
    return "\n".join(lines)


def summary_rows() -> list[dict[str, Any]]:
    """One row per certificate of both censuses, for records and the summary table."""
    rows: list[dict[str, Any]] = []
    rectangles = json.loads((CENSUS_ROOT / "census/census.json").read_text(encoding="utf-8"))
    mixed = json.loads((CENSUS_ROOT / "census-mixed/census.json").read_text(encoding="utf-8"))
    reference = replay_reference()
    families = (
        ("census", rectangles, {case.certificate: case for case in rectangle_cases()}),
        ("census-mixed", mixed, {case.certificate: case for case in mixed_cases()}),
    )
    for folder, census, cases in families:
        for name, entry in census["cases"].items():
            case = cases.get(name)
            if folder == "census":
                replay = "complete" if name in reference else "none"
                source = (
                    "tokoharu-density"
                    if entry.get("packet") == TOKOHARU_PACKET
                    else f"wand125-rectangle-certificates-{entry.get('packet')}"
                )
            else:
                replayed = mixed_reference(case)["directions"] if case is not None else []
                replay = (
                    replay_status(len(replayed), net_directions(case))
                    if case is not None
                    else "none"
                )
                source = str(entry.get("packet"))
            least = entry.get("least_bound_leaf_exact") or {}
            verified = (
                entry.get("status") == "VERIFIED"
                and entry.get("returncode") == 0
                and least.get("clears_threshold") is True
            )
            rows.append(
                {
                    "certificate": name,
                    "packet": source,
                    "candidate": str(case.candidate.relative_to(PROJECT.parent))
                    if case is not None
                    else None,
                    "format": (entry.get("premises") or {}).get("format", "T"),
                    "n": entry.get("n"),
                    "L": entry.get("L"),
                    "verdict": "VERIFIED" if verified else str(entry.get("status")),
                    "directions_verified": entry.get("directions_verified"),
                    "threshold": entry.get("threshold") or census.get("threshold"),
                    "least_certified_bound": entry.get("least_certified_bound"),
                    "least_leaf_exact_clears": least.get("clears_threshold") is True,
                    "cpu_seconds": round(float(entry.get("cpu_seconds") or 0.0), 1),
                    "nodes": entry.get("nodes"),
                    "authors_replay_here": replay,
                    "first_complete_check_here": verified and replay != "complete",
                    "receipts": (
                        f"packing/benchmarks/measure-verifier/{folder}/"
                        f"{entry.get('packet')}/{name}.jsonl.gz"
                    ),
                    "candidate_sha256": entry.get("candidate_sha256"),
                    "binary_sha256": entry.get("binary_sha256"),
                    "source_sha256": (entry.get("build") or {}).get("source_sha256"),
                }
            )
    rows.sort(key=lambda row: (int(row["n"] or 0), str(row["certificate"])))
    return rows


def render_summary(rows: list[dict[str, Any]]) -> str:
    """The census summary as a Markdown table."""
    verified = sum(row["verdict"] == "VERIFIED" for row in rows)
    first = sum(bool(row["first_complete_check_here"]) for row in rows)
    lines = [
        "# Census Summary",
        "",
        "Generated by `python -m devtools.sqverify_fast_census --summary`; do not edit by",
        "hand. The same rows, with receipt paths and digests, are in `census-summary.json`.",
        "",
        "Every retained certificate that `sqverify-fast` decides (formats T, M and L), from",
        "the two census folders: [census/](census/README.md) and",
        "[census-mixed/](census-mixed/README.md). *Verdict* is `VERIFIED` only when every",
        "direction of its net verified, the process exited zero, and the exact capture at the",
        "least-bound leaf's centre cleared the threshold. *Authors' replay here* is what",
        "this repository holds of a replay by the authors' own checker; where it holds less",
        "than a complete replay, this census is the first complete check of the certificate",
        "here, which the last column says.",
        "",
        (
            "| Certificate | Format | n | L | Verdict | CPU s | Least certified bound"
            " | Authors' replay here | First complete check here |"
        ),
        "| --- | --- | ---: | --- | --- | ---: | --- | --- | --- |",
    ]
    for row in rows:
        cells = [
            f"`{row['certificate']}`",
            str(row["format"]),
            str(row["n"]),
            str(row["L"]),
            str(row["verdict"]),
            f"{row['cpu_seconds']:.1f}",
            str(row["least_certified_bound"]),
            str(row["authors_replay_here"]),
            "yes" if row["first_complete_check_here"] else "no",
        ]
        lines.append("| " + " | ".join(cells) + " |")
    lines += [
        "",
        f"{verified} of {len(rows)} certificates verified; {first} of them are the first",
        "complete check of their certificate in this repository.",
        "",
        "<!-- This document follows common-doc-guidelines.md.",
        "See github.com/jlevy/practical-prose and review guidelines before editing.",
        "-->",
        "",
    ]
    return "\n".join(lines)


def census_delta(old: dict[str, Any], new: dict[str, Any]) -> list[str]:
    """Every difference in verdict, nodes or least certified bound between two runs."""
    fields = ("status", "nodes", "least_certified_bound", "directions_verified")
    return [
        f"{name}: {field} {old['cases'][name].get(field)} -> {new['cases'][name].get(field)}"
        for name in sorted(set(old["cases"]) & set(new["cases"]))
        for field in fields
        if old["cases"][name].get(field) != new["cases"][name].get(field)
    ]


def records_mode(args: argparse.Namespace, census: dict[str, Any], selected: list[Case]) -> int:
    """`--evidence` prints each selected case's entry; `--control` writes its receipt."""
    if args.evidence:
        if not (args.audit_record and args.date):
            raise SystemExit("--evidence needs --audit-record and --date")
        for case in selected:
            entry = census["cases"].get(case.certificate, {})
            text = evidence_entry(
                case, args.out, entry, audit_record=args.audit_record, date=args.date
            )
            sys.stdout.write(text)
        return 0
    failed = 0
    for case in selected:
        receipt = control(
            args.binary,
            case,
            census["cases"].get(case.certificate, {}),
            args.out,
            args.threads,
        )
        target = args.out / case.packet / f"{case.certificate}.control.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(retained_json.dumps(receipt, sort_keys=True))
        failed += receipt["status"] != "CONTROLS_REFUSED"
        verdicts = ", ".join(
            f"{run['name']} refused at {len(run['sweep']['refused'])} of "
            f"{run['sweep']['directions']}"
            if "sweep" in run
            else f"{run['name']} {run['verdict']}"
            for run in receipt["runs"]
        )
        print(f"{case.certificate:18} {receipt['status']} r={receipt['index']}: {verdicts}")
    return 1 if failed else 0


def source_digest() -> int:
    """`--source-digest`: the tree's crate digest and the review that accepted it, if any."""
    digest = crate_source_sha256()
    reviewed = REVIEWED_SOURCES.get(digest)
    scope = (
        "standard and declared nets" if reviewed and reviewed.declared_nets else "standard net"
    )
    print(
        f"{digest} reviewed source for the {scope} ({reviewed.commit}; {reviewed.review})"
        if reviewed is not None
        else f"{digest} not reviewed source: no entry of REVIEWED_SOURCES"
    )
    return 0 if reviewed is not None else 1


def write_summary() -> int:
    """`--summary`: census-summary.json and census-summary.md from both census folders."""
    rows = summary_rows()
    (CENSUS_ROOT / "census-summary.json").write_text(
        json.dumps(
            {"kind": "sqverify-fast-census-summary/v1", "certificates": rows},
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    (CENSUS_ROOT / "census-summary.md").write_text(render_summary(rows), encoding="utf-8")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--family", choices=("rectangles", "mixed"), default="rectangles")
    parser.add_argument("--binary", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument(
        "--source-digest",
        action="store_true",
        help="print this tree's crate source_sha256 and the review that accepted it; "
        "exit 1 if none did",
    )
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--same-build",
        action="store_true",
        help="with --resume, keep only cases this binary verified (a re-run after a fix)",
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--control",
        action="store_true",
        help="negative controls on each selected verified certificate",
    )
    parser.add_argument(
        "--evidence",
        action="store_true",
        help="print each selected certificate's replay evidence entry",
    )
    parser.add_argument("--audit-record", help="with --evidence: the mapped review's path")
    parser.add_argument("--date", help="with --evidence: the day the replay ran")
    parser.add_argument(
        "--report", action="store_true", help="render --out/README.md from the census"
    )
    parser.add_argument("--only", default="", help="comma-separated certificate names")
    parser.add_argument(
        "--packets", default="", help="comma-separated packets (the folder under --out)"
    )
    parser.add_argument(
        "--delta",
        type=Path,
        help="an earlier census.json: print every case whose verdict, nodes or bound moved",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="write census-summary.json and census-summary.md from both census folders",
    )
    args = parser.parse_args(argv)
    if not args.source_digest and (args.binary is None or args.out is None):
        parser.error("--binary and --out are required")
    if args.source_digest or args.summary:
        return source_digest() if args.source_digest else write_summary()
    census_path = args.out / "census.json"
    binary_sha = sha256(args.binary)
    census: dict[str, Any] = (
        json.loads(census_path.read_text(encoding="utf-8"))
        if census_path.is_file()
        else {"kind": "sqverify-fast-census/v1", "threshold": THRESHOLD, "cases": {}}
    )
    if args.delta is not None:
        old = json.loads(args.delta.read_text(encoding="utf-8"))
        changes = census_delta(old, census)
        common = len(set(old["cases"]) & set(census["cases"]))
        print(f"{common} cases in both runs; {len(changes)} differences")
        for line in changes:
            print(f"  {line}")
        return 1 if changes else 0
    mixed = args.family == "mixed"
    if mixed:
        census["family"] = "mixed"
        census["threshold"] = "declared"
    cases = mixed_cases() if mixed else rectangle_cases()
    only = {name for name in args.only.split(",") if name}
    packets = {name for name in args.packets.split(",") if name}
    selected = [
        case
        for case in cases
        if (not only or case.certificate in only) and (not packets or case.packet in packets)
    ]
    if args.report:
        text = render_mixed_report(census, args.out) if mixed else render_report(census)
        (args.out / "README.md").write_text(text, encoding="utf-8")
        return 0
    if args.check:

        def passed(entry: dict[str, Any]) -> bool:
            least = entry.get("least_bound_leaf_exact") or {}
            return (
                entry.get("status") == "VERIFIED"
                and entry.get("returncode") == 0
                and least.get("clears_threshold") is True
            )

        missing = [
            case.certificate
            for case in selected
            if not passed(census["cases"].get(case.certificate, {}))
        ]
        print(
            f"{len(selected) - len(missing)} of {len(selected)} retained certificates VERIFIED"
        )
        for name in missing:
            print(f"  not verified: {name}")
        return 1 if missing else 0
    if args.evidence or args.control:
        return records_mode(args, census, selected)
    for case in selected:
        held = census["cases"].get(case.certificate)
        # A verified case is kept whichever build verified it: each case records its
        # own binary and source digests, so a census may span builds honestly.
        # --same-build keeps only this binary's, to re-run everything after a fix.
        if (
            args.resume
            and held is not None
            and held.get("status") == "VERIFIED"
            and (not args.same_build or held.get("binary_sha256") == binary_sha)
        ):
            continue
        result = run(args.binary, case, args.out / case.packet, args.threads)
        result["binary_sha256"] = binary_sha
        census["cases"][case.certificate] = result
        census_path.parent.mkdir(parents=True, exist_ok=True)
        census_path.write_text(retained_json.dumps(census, sort_keys=True))
        print(
            f"{case.certificate:18} {result['status']} dirs={result['directions_verified']} "
            f"nodes={result['nodes']} least={result['least_certified_bound']} "
            f"cpu={result['cpu_seconds']:.1f}s wall={result['wall_seconds']:.1f}s "
            f"load={result['load_before']:.1f}",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
