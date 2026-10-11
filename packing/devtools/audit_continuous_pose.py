"""Audit Guzhou0806's continuous-pose bound, s(40) > 1340000/199529, and drive its replay.

The follow-up comment of 2026-10-10 on jlevy/squares#485 claims ``s(40) > 1340000/199529``
from wand125's ``rect_n40_L67`` density, which the 2026-10-01 rectangle packet retains,
by a continuous-pose interval kernel over 43 closed slabs of the half-angle tangent and an
exact horizontal certificate for the near-axis patch. The source is retained in
``resources/web/guzhou-n40-continuous-pose-2026-10-10/``; the argument and the replay
contract this tool answers are the review
``docs/project/reviews/review-2026-10-10-guzhou-n40-continuous-pose-bound.md``.

Four subcommands, each reading the retained files only:

- ``derive`` writes the two kernel inputs the release decided, regenerated here from the
  retained density (`pose_input`, `axis_input`), and the two inputs this repository's
  crate decides (`crate_input`), and prints their SHA-256. The digests, not the
  construction, bind the kernel inputs to the receipts, which name `POSE_SHA256` and
  `AXIS_SHA256`. `CRATE_SHA256` records the crate inputs the review wrote, which the
  tests hold; no run is refused on it, and the crate's admission premises are checked
  instead (`crate_premises`).
- ``check`` decides every finite step of the claim in exact rationals on the retained
  density (`audit`): the density's D4 expansion, both inputs' identity and the
  enclosure of every one of their numbers, the dominated measure the axis kernel reads,
  the counting margin ``40 tau - M = 1/500``, the slab partition, the near-axis
  containment ``A W(eps) <= B``, and the axis minimum against the threshold, which it
  evaluates again at the reported minimiser. It compares every value with both release
  receipts (`receipt_checks`) and refuses the finite controls (`FINITE_CONTROLS`).
- ``run`` builds both kernels from the retained source with the release's flags
  (`build_all`) and drives the replay: the axis kernel, the 43 slabs, the contract's
  kernel controls A to F and H (`kernel_controls`, `run_controls`), control G on the
  release's own ``exact.py`` (`run_release_g`), and the two runs of this repository's
  ``sqverify-fast`` (`run_crate`), each with its wall and CPU time. It writes receipts
  to a scratch directory; nothing in it reads the network.
- ``check-replay`` judges those receipts against the contract and both release
  receipts (`replay_report`).

**What its author read** (its independence record, for the finite steps' evidence).
Written on 2026-10-10 by an AI agent (Claude, the records lane of the #485
follow-up, ``think-xms6``) from the review named above, which states the argument, the
input formats and every finite quantity, and from that review's scratch measurements
(``exact_checks.py``, ``make_crate_inputs.py``, ``synthetic_tests*.py``,
``replay_slabs.sh``, ``receipts_summary.py``), themselves written apart from the
release's code. Of the release it read ``README.md``, ``SOURCES.md``,
``VERIFICATION.md``, ``REPRODUCIBILITY.md``, ``LICENSE``, ``certificate/parameters.json``,
the workflow, both C++ kernels and both C++ harnesses (in full, before building them),
``verifier/run.py`` (for the commands and control stages it runs), and the receipts as
data; it did not open ``PROOF.md``, ``verifier/exact.py``, ``verifier/audit.py``,
``tests/oracle.py``, ``tests/test_kernel.py`` or ``tests/test_admission.py`` while
writing the finite part. ``exact.py`` was read afterwards, in full, only to run control G
on the release's own code as the contract states it (`run_release_g`); nothing in the
finite part changed after that. It shares with ``exact.py`` the definition of the
density, its D4 expansion, the order the kernels read it in, the enclosure rule and the
inward rounding, which the review states, and no code. Of this repository's code it uses
`devtools.audit_clipped_corner_transfer` for reading the density exactly,
`devtools.check_sqverify_fast` and `devtools.sqverify_fast_census` for the crate's
reviewed-source digest.

The continuous cover itself is decided only by the release's kernel, which ``run``
builds and runs; no code here decides it (GC-4 of the review).

Usage, from ``packing/``, each after ``uv run --frozen --all-extras --group dev``::

    python -m devtools.audit_continuous_pose derive --out DIR
    python -m devtools.audit_continuous_pose check [--output OUT.json]
    python -m devtools.audit_continuous_pose run --out DIR --workers 2 \\
        --crate-binary sqverify_fast/target/release/sqverify-fast
    python -m devtools.audit_continuous_pose check-replay [--receipts DIR] [--output OUT]
"""

from __future__ import annotations

import argparse
import gzip
import itertools
import json
import math
import os
import shutil
import subprocess
import sys
import time
from collections import Counter
from collections.abc import Callable, Iterable, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools.audit_clipped_corner_transfer import (
    Density,
    area,
    invariant,
    read_density,
    sha256,
    text,
)
from devtools.check_sqverify_fast import crate_source_sha256
from devtools.retained_data import read_retained_bytes
from devtools.sqverify_fast_census import REVIEWED_SOURCES

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
PACKET = WEB / "guzhou-n40-continuous-pose-2026-10-10"
SOURCE = PACKET / "source"
CANDIDATE = (
    WEB / "wand125-rectangle-certificates-2026-10-01/wand125-rectangles/certificates"
    "/rect_n40_L67/certified_candidate.json"
)
PARAMETERS = SOURCE / "certificate/parameters.json"
MANIFEST = PACKET / "acquisition/upstream-subtree.sha256"
#: The release's two receipts: the producer's local run in the tree at the pin, and the
#: GitHub Actions run 38059878931 that the release ZIP carries instead (GC-3).
RECEIPTS = {"local": SOURCE / "results", "ci": PACKET / "release-ci/results"}
RECEIPT_DIR = PACKET / "receipts"

PIN = "71c97d07553d7d5ff5c5c82f0c9d1c75a150a4e3"
CANDIDATE_SHA256 = "71011d0356dd179c6e7e6e02c9a064ff30f6f13844016ce3b97463bf7ef53dc0"
POSE_SHA256 = "ccf7b68aa89fdcfcf0d78ac135cfa24e4a73b822eb412b2aac46e9c49e2b9925"
AXIS_SHA256 = "d57e8bb267dc1a17d57fa0f17f662bf552b6aef46427a0eb9308ae16539ed1cb"
#: The crate inputs of the contract's items 3 and 6, as the review wrote them (tests only).
CRATE_SHA256 = {
    "axis-A": "379193fff9402ac37582f331ae7431d47373dfefb19cec6ecabb1d607bdb2e0a",
    "net401-B": "94c3ab2e6a5da382278443fa4600528a83217279e9998e02554647f326a5009a",
}
#: The CI run's binaries, which g++ 13.3.0 reproduces from the tree's directory.
CI_BINARIES = {
    "pose": "69bc9e6485102d3636db5377884ba6304f749be94d6ca913d82d80108f1ed4ab",
    "axis": "cccecb9ab1ca0ecd88b0994c04ebf7965cf0982b7e400966702da6f7e893265c",
}
CI_COMPILER = "g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0"

type Term = tuple[Fraction, Fraction, Fraction, Fraction, Fraction]
type Row = tuple[int, int, int, int, int]


# --------------------------------------------------------------------------- the claim


ENDPOINTS = (1, 500, *range(10000, 410001, 10000), 415000)


@dataclass(frozen=True)
class Claim:
    """The claim's parameters, named as the release's ``parameters.json`` names them."""

    n: int = 40
    L: Fraction = Fraction(67, 10)
    B: Fraction = Fraction(199529, 200000)
    X: Fraction = Fraction(1340000, 199529)
    A: Fraction = Fraction(997643, 10**6)
    eps: Fraction = Fraction(1, 10**6)
    T: Fraction = Fraction(83, 200)
    tau: Fraction = Fraction(4999, 5000)
    mass: Fraction = Fraction(3999, 100)
    den: int = 10**6
    endpoints: tuple[int, ...] = ENDPOINTS
    budget: int = 30_000_000

    def parameters(self) -> dict[str, object]:
        return {
            "B": text(self.B),
            "L": text(self.L),
            "X": text(self.X),
            "axis_side": text(self.A),
            "denominator": self.den,
            "endpoints": list(self.endpoints),
            "epsilon": text(self.eps),
            "last_t": text(self.T),
            "mass": text(self.mass),
            "n": self.n,
            "node_budget": self.budget,
            "threshold": text(self.tau),
        }

    def slabs(self) -> list[tuple[int, int]]:
        return list(itertools.pairwise(self.endpoints))


CLAIM = Claim()
#: T-133's bound, which this claim raises by `RAISE`.
EARLIER = Fraction(335427, 50000)
RAISE = Fraction(72586117, 9976450000)
#: The kernel's upper bound for cos + sin when its maximum may lie in the box.
SQRT2_UP = Fraction(1414213562373096, 10**15)
#: The axis input's grid and density scale.
GRID = 10**9
#: The crate admits thresholds of at least one: capture >= tau of the density is capture
#: >= 1 of the density scaled by 1/tau (GC-4).
CRATE_SCALE = Fraction(5000, 4999)


def half_angle(t: Fraction) -> tuple[Fraction, Fraction]:
    """Cosine and sine of ``2 atan t``, exactly."""
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def extent(t: Fraction) -> Fraction:
    """``W = cos + sin`` at half-angle tangent ``t``: the side of a unit square's box."""
    c, s = half_angle(t)
    return c + s


def kernel_threshold(tau: Fraction) -> float:
    """What the kernel accepts a box at: ``up(fl(tn / td))``, the binary64 quotient
    rounded to nearest (as CPython's integer true division is) and stepped up once."""
    return math.nextafter(tau.numerator / tau.denominator, math.inf)


def ceil_div(p: int, q: int) -> int:
    return -(-p // q)


# --------------------------------------------------------------------------- the inputs


def enclose(x: Fraction) -> tuple[float, float]:
    """The binary64 pair that brackets ``x``: the nearest double, and its neighbour
    on the far side when it is not exact."""
    v = float(x)
    exact = Fraction(v)
    lo = v if exact <= x else math.nextafter(v, -math.inf)
    hi = v if exact >= x else math.nextafter(v, math.inf)
    return lo, hi


def hex_pair(x: Fraction) -> str:
    lo, hi = enclose(x)
    return f"{lo.hex()} {hi.hex()}"


def decimal_pair(x: Fraction) -> str:
    lo, hi = enclose(x)
    return f"{lo:.17g} {hi:.17g}"


def term_density(rect: tuple[Fraction, Fraction, Fraction, Fraction], w: Fraction) -> Fraction:
    """Each row of weight ``w`` puts density ``w / (8 |R|)`` on each of its eight images."""
    return w / (8 * area(rect))


def maps_terms(density: Density) -> list[Term]:
    """The D4 expansion from the eight symmetries of ``K`` as maps on points."""
    side = density.side
    maps: tuple[Callable[[Fraction, Fraction], tuple[Fraction, Fraction]], ...] = (
        lambda x, y: (x, y),
        lambda x, y: (side - x, y),
        lambda x, y: (x, side - y),
        lambda x, y: (side - x, side - y),
        lambda x, y: (y, x),
        lambda x, y: (side - y, x),
        lambda x, y: (y, side - x),
        lambda x, y: (side - y, side - x),
    )
    out: list[Term] = []
    for rect, w in density.rows:
        rho = term_density(rect, w)
        for f in maps:
            (x0, y0), (x1, y1) = f(rect[0], rect[1]), f(rect[2], rect[3])
            out.append((min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1), rho))
    return out


def pose_terms(density: Density) -> list[Term]:
    """The terms in the order the pose kernel reads them: per row, transpose in
    ``(no, yes)``, then the ``x`` flip, then the ``y`` flip."""
    side = density.side
    out: list[Term] = []
    for rect, w in density.rows:
        rho = term_density(rect, w)
        a, b, c, e = rect
        for swap in (False, True):
            x0, y0, x1, y1 = (b, a, e, c) if swap else (a, b, c, e)
            for flip_x in (False, True):
                for flip_y in (False, True):
                    xs = (side - x1, side - x0) if flip_x else (x0, x1)
                    ys = (side - y1, side - y0) if flip_y else (y0, y1)
                    out.append((xs[0], ys[0], xs[1], ys[1], rho))
    return out


def pose_input(density: Density, claim: Claim = CLAIM) -> bytes:
    """The pose kernel's ``certificate_input.txt``: ``L`` as a hexadecimal pair, ``B`` as
    a 17-digit decimal pair, the count, then each term's five values as hexadecimal
    pairs that bracket them."""
    terms = pose_terms(density)
    lines = [hex_pair(claim.L), decimal_pair(claim.B), str(len(terms))]
    lines += [" ".join(hex_pair(v) for v in term) for term in terms]
    return ("\n".join(lines) + "\n").encode()


def pose_enclosures(data: bytes, density: Density, claim: Claim = CLAIM) -> tuple[int, int]:
    """How many of the pose input's numbers there are, and how many bracket their value."""
    lines = data.decode().splitlines()
    held = total = 0

    def bracket(pair: Sequence[str], x: Fraction, parse: Callable[[str], float]) -> None:
        nonlocal held, total
        lo, hi = parse(pair[0]), parse(pair[1])
        total += 1
        held += math.isfinite(lo) and math.isfinite(hi) and Fraction(lo) <= x <= Fraction(hi)

    bracket(lines[0].split(), claim.L, float.fromhex)
    bracket(lines[1].split(), claim.B, float)
    terms = pose_terms(density)
    if int(lines[2]) != len(terms) or len(lines) != len(terms) + 3:
        return held, total + 1
    for term, line in zip(terms, lines[3:], strict=True):
        values = line.split()
        for k, x in enumerate(term):
            bracket(values[2 * k : 2 * k + 2], x, float.fromhex)
    return held, total


def quarter_terms(density: Density) -> list[Term]:
    """The terms in the order the axis kernel reads them: per row, the row and its
    reflection in ``x``, each followed by its three quarter-turns ``(x, y) -> (L - y, x)``."""
    side = density.side
    out: list[Term] = []
    for rect, w in density.rows:
        rho = term_density(rect, w)
        a, b, c, e = rect
        for reflect in (False, True):
            x0, y0, x1, y1 = (side - c, b, side - a, e) if reflect else (a, b, c, e)
            for _ in range(4):
                out.append((x0, y0, x1, y1, rho))
                x0, y0, x1, y1 = side - y1, x0, side - y0, x1
    return out


def dominated(term: Term) -> Row:
    """The integer row the axis kernel reads for a term: the support rounded inward to
    the ``1/GRID`` grid and the density rounded down to a multiple of ``1/GRID``."""
    a, b, c, e, rho = term
    return (
        ceil_div(a.numerator * GRID, a.denominator),
        ceil_div(b.numerator * GRID, b.denominator),
        (c.numerator * GRID) // c.denominator,
        (e.numerator * GRID) // e.denominator,
        (rho.numerator * GRID) // rho.denominator,
    )


def axis_rows(density: Density) -> list[Row]:
    """The dominated measure: every term's integer row that keeps a positive area and
    density, in the axis kernel's order."""
    rows = [dominated(term) for term in quarter_terms(density)]
    return [row for row in rows if row[0] < row[2] and row[1] < row[3] and row[4] > 0]


def axis_input(rows: Sequence[Row], claim: Claim = CLAIM, tau: Fraction | None = None) -> bytes:
    """The axis kernel's input: ``L``, ``A``, the grid and the density scale, the
    threshold, the count, then the rows."""
    threshold = claim.tau if tau is None else tau
    head = (
        f"{int(claim.L * GRID)} {int(claim.A * GRID)} {GRID} {GRID} "
        f"{threshold.numerator} {threshold.denominator} {len(rows)}"
    )
    return ("\n".join([head, *(" ".join(map(str, row)) for row in rows)]) + "\n").encode()


def crate_input(density: Density, side: Fraction, step: Fraction, count: int) -> bytes:
    """A format T input for ``sqverify-fast``: the 480 positive rows with their weights
    scaled by `CRATE_SCALE`, threshold one, and the net in the ``certificate`` block."""
    value = {
        "n": density.n,
        "L": text(density.side),
        "B": text(side),
        "rectangles": [[text(v) for v in rect] for rect, _ in density.rows],
        "weights": [text(w * CRATE_SCALE) for _, w in density.rows],
        "coverage_lower_bound_exact": "1",
        "certificate": {
            "L": text(density.side),
            "B": text(side),
            "D": text(step),
            "angle_count": count,
        },
    }
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def crate_inputs(density: Density, claim: Claim = CLAIM) -> dict[str, bytes]:
    """The contract's two crate inputs: the axis at side ``A`` on the standard net, and
    the 401-direction net at side ``B``."""
    return {
        "axis-A": crate_input(density, claim.A, Fraction(83, 40000), 201),
        "net401-B": crate_input(density, claim.B, Fraction(83, 80000), 401),
    }


# --------------------------------------------------------------------------- the axis


def grid_nodes(rows: Sequence[Row], length: int, side: int, axis: int) -> list[int]:
    """The breakpoints of one axis inside ``[l/2, l - A/2]``: its two ends and every
    support edge plus or minus ``A/2`` that falls inside, sorted and distinct."""
    low, high, half = length // 2, length - side // 2, side // 2
    nodes = {low, high}
    for row in rows:
        for edge in (row[axis], row[axis + 2]):
            nodes.update(v for v in (edge - half, edge + half) if low <= v <= high)
    return sorted(nodes)


def axis_capture(rows: Iterable[Row], x: int, y: int, side: int) -> int:
    """The dominated measure's capture by the horizontal side-``A`` square centred at
    ``(x, y)``, scaled by ``GRID^3``: exact integers."""
    half = side // 2
    total = 0
    for a, b, d, e, w in rows:
        dx = max(0, min(d, x + half) - max(a, x - half))
        dy = max(0, min(e, y + half) - max(b, y - half))
        total += w * dx * dy
    return total


def term_capture(terms: Iterable[Term], x: Fraction, y: Fraction, side: Fraction) -> Fraction:
    """The capture of a density given by terms, by the horizontal square of the side
    centred at ``(x, y)``: exact rationals."""
    half = side / 2
    total = Fraction(0)
    for a, b, d, e, rho in terms:
        dx = max(Fraction(0), min(d, x + half) - max(a, x - half))
        dy = max(Fraction(0), min(e, y + half) - max(b, y - half))
        total += rho * dx * dy
    return total


def parse_axis_stdout(record: dict[str, Any]) -> dict[str, Any]:
    value: dict[str, Any] = json.loads(str(record["stdout"]))
    return value


# --------------------------------------------------------------------------- the facts


@dataclass(frozen=True)
class Check:
    name: str
    held: bool
    detail: str

    def as_json(self) -> dict[str, object]:
        return {"name": self.name, "held": self.held, "detail": self.detail}


@dataclass(frozen=True)
class Facts:
    """What the density and the derived inputs give, computed once at the claim."""

    sha256: str
    n: int
    side: Fraction
    listed: int
    positive: int
    mass: Fraction
    terms: int
    distinct: int
    invariant: bool
    integral: Fraction
    pose_sha256: str
    pose_is_expansion: bool
    enclosures: tuple[int, int]
    axis_sha256: str
    axis_rows: int
    axis_dropped: int
    axis_is_expansion: bool
    axis_dominated: bool
    axis_quarter_invariant: bool
    dominated_mass: Fraction
    axis_weights: int
    evaluation_bound: int
    nodes: tuple[int, int]
    crate_sha256: dict[str, str]
    crate_mass: Fraction
    #: The receipts' axis minimiser and minimum, and the captures evaluated here there.
    minimiser: tuple[int, int] = (0, 0)
    minimum: int = 0
    minimiser_capture: int = 0
    minimiser_capture_g: Fraction = field(default=Fraction(0))


def facts(density: Density, claim: Claim = CLAIM) -> Facts:
    expansion = Counter(maps_terms(density))
    pose = pose_input(density, claim)
    quarter = quarter_terms(density)
    rows = axis_rows(density)
    length, side = int(claim.L * GRID), int(claim.A * GRID)
    dominated_ok = all(
        Fraction(row[0], GRID) >= t[0]
        and Fraction(row[1], GRID) >= t[1]
        and Fraction(row[2], GRID) <= t[2]
        and Fraction(row[3], GRID) <= t[3]
        and 0 <= Fraction(row[4], GRID) <= t[4]
        for row, t in zip(map(dominated, quarter), quarter, strict=True)
    )
    turned = Counter((length - e, a, length - b, d, w) for a, b, d, e, w in rows)
    weights = sum(row[4] for row in rows)
    reach = length + side // 2
    inputs = crate_inputs(density, claim)
    axis = parse_axis_stdout(read_receipt(RECEIPTS["ci"], "axis.json"))
    x, y = int(axis["minimizer_x_integer"]), int(axis["minimizer_y_integer"])
    return Facts(
        sha256=density.sha256,
        n=density.n,
        side=density.side,
        listed=density.listed,
        positive=len(density.rows),
        mass=sum((w for _, w in density.rows), Fraction(0)),
        terms=density.terms,
        distinct=len(density.merged),
        invariant=invariant(density),
        integral=sum((area(r) * v for r, v in density.merged.items()), Fraction(0)),
        pose_sha256=sha256(pose),
        pose_is_expansion=Counter(pose_terms(density)) == expansion,
        enclosures=pose_enclosures(pose, density, claim),
        axis_sha256=sha256(axis_input(rows, claim)),
        axis_rows=len(rows),
        axis_dropped=len(quarter) - len(rows),
        axis_is_expansion=Counter(quarter) == expansion,
        axis_dominated=dominated_ok,
        axis_quarter_invariant=turned == Counter(rows),
        dominated_mass=sum(
            (Fraction(w * (d - a) * (e - b), GRID**3) for a, b, d, e, w in rows), Fraction(0)
        ),
        axis_weights=weights,
        evaluation_bound=16 * weights * (length + reach) ** 2,
        nodes=(
            len(grid_nodes(rows, length, side, 0)),
            len(grid_nodes(rows, length, side, 1)),
        ),
        crate_sha256={name: sha256(data) for name, data in inputs.items()},
        crate_mass=sum((w * CRATE_SCALE for _, w in density.rows), Fraction(0)),
        minimiser=(x, y),
        minimum=int(axis["minimum_numerator"]),
        minimiser_capture=axis_capture(rows, x, y, side),
        minimiser_capture_g=term_capture(
            maps_terms(density), Fraction(x, GRID), Fraction(y, GRID), claim.A
        ),
    )


def load_density() -> Density:
    return read_density(read_retained_bytes(CANDIDATE))


def read_receipt(folder: Path, name: str = "verification.json") -> dict[str, Any]:
    value: dict[str, Any] = json.loads((folder / name).read_text(encoding="utf-8"))
    return value


def read_slabs(folder: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in (folder / "slabs.jsonl").read_text(encoding="utf-8").splitlines()
        if line
    ]


# --------------------------------------------------------------------------- the audit


def density_checks(f: Facts, claim: Claim = CLAIM) -> list[Check]:
    """The density and both derived inputs, at the claim."""
    held, total = f.enclosures
    length = int(claim.L * GRID)
    return [
        Check("density: the release's candidate", f.sha256 == CANDIDATE_SHA256, f.sha256),
        Check(
            "density: n and L are the claim's",
            (f.n, f.side) == (claim.n, claim.L),
            f"n {f.n}, L {text(f.side)}",
        ),
        Check("density: 480 positive rows", f.positive == 480, f"{f.positive} of {f.listed}"),
        Check("density: mass M", f.mass == claim.mass, text(f.mass)),
        Check(
            "density: D4 expansion",
            (f.terms, f.distinct) == (3840, 3792),
            f"{f.terms} terms, {f.distinct} distinct rectangles",
        ),
        Check("density: D4-invariant", f.invariant, "under each of the eight maps"),
        Check("density: integral of g is M", f.integral == claim.mass, text(f.integral)),
        Check("pose input: the receipts' input", f.pose_sha256 == POSE_SHA256, f.pose_sha256),
        Check(
            "pose input: its terms are the D4 expansion",
            f.pose_is_expansion,
            "the same multiset as the eight maps give",
        ),
        Check(
            "pose input: every number brackets its rational",
            held == total == 2 + 5 * 3840,
            f"{held} of {total}",
        ),
        Check("axis input: the receipts' input", f.axis_sha256 == AXIS_SHA256, f.axis_sha256),
        Check(
            "axis input: its terms are the D4 expansion",
            f.axis_is_expansion,
            "quarter-turn order, the same multiset as the eight maps give",
        ),
        Check(
            "axis input: 3840 rows, none dropped",
            (f.axis_rows, f.axis_dropped) == (3840, 0),
            f"{f.axis_rows} rows, {f.axis_dropped} dropped",
        ),
        Check(
            "axis input: dominated by g",
            f.axis_dominated,
            "supports rounded inward to 1e-9, densities down to 1e-9",
        ),
        Check(
            "axis input: quarter-turn invariant",
            f.axis_quarter_invariant,
            "the integer rows map onto themselves under (x, y) -> (L - y, x)",
        ),
        Check(
            "axis input: the dominated mass is below M",
            0 < claim.mass - f.dominated_mass < Fraction(5, 10**6),
            f"M - mass = {float(claim.mass - f.dominated_mass):.6g}",
        ),
        Check(
            "axis input: the int128 guards",
            f.axis_weights < 10**15 and f.evaluation_bound < 2**125,
            f"16 sum w (l + l + A/2)^2 = {f.evaluation_bound}",
        ),
        Check(
            "axis input: the grid of breakpoints",
            f.nodes == (2213, 2213) and f.nodes[0] * f.nodes[1] <= 15_000_000,
            f"{f.nodes[0]} x {f.nodes[1]} = {f.nodes[0] * f.nodes[1]} vertices",
        ),
        Check(
            "axis: the minimiser is a vertex of the quadrant",
            length // 2 <= f.minimiser[0] <= length - int(claim.A * GRID) // 2
            and f.minimiser[1] == length - int(claim.A * GRID) // 2,
            f"({f.minimiser[0]}, {f.minimiser[1]}) / 1e9",
        ),
        Check(
            "axis: the capture at the minimiser, evaluated here",
            f.minimiser_capture == f.minimum,
            f"{f.minimiser_capture} / 1e27",
        ),
        Check(
            "axis: g captures at least as much there",
            f.minimiser_capture_g * GRID**3 >= f.minimiser_capture,
            f"{float(f.minimiser_capture_g):.12f}",
        ),
        Check(
            "crate inputs: the scaled mass is below n",
            f.crate_mass == claim.mass * CRATE_SCALE and f.crate_mass < claim.n,
            text(f.crate_mass),
        ),
    ]


def least_bound(slabs: Sequence[dict[str, Any]]) -> tuple[Fraction, int]:
    """The least leaf bound over the slabs, exactly, and the slab it is in."""
    bounds = [
        (Fraction(json.loads(row["stdout"])["lower_bound"]), i) for i, row in enumerate(slabs)
    ]
    return min(bounds)


def chain_checks(claim: Claim, f: Facts, least: Fraction) -> list[Check]:
    """The scalar chain at the claim's parameters, with the receipts' kernel outputs."""
    tip = claim.T * claim.T + 2 * claim.T - 1
    near = claim.eps * claim.eps + 2 * claim.eps - 1
    margin = claim.B - claim.A * extent(claim.eps)
    ends = claim.endpoints
    first, last = (ends[0], ends[-1]) if ends else (0, 0)
    threshold = kernel_threshold(claim.tau)
    scale = GRID**3
    required = ceil_div(scale * claim.tau.numerator, claim.tau.denominator)
    return [
        Check("claim: X = L / B", claim.X == claim.L / claim.B, text(claim.L / claim.B)),
        Check(
            "claim: X raises the earlier bound",
            claim.X - EARLIER == RAISE,
            text(claim.X - EARLIER),
        ),
        Check(
            "counting: n tau - M > 0",
            claim.n * claim.tau - claim.mass > 0,
            text(claim.n * claim.tau - claim.mass),
        ),
        Check(
            "domain: E > 0 at every angle",
            SQRT2_UP * SQRT2_UP > 2 and claim.L > claim.B * SQRT2_UP,
            f"L - B sqrt2_up = {text(claim.L - claim.B * SQRT2_UP)}",
        ),
        Check(
            "slabs: T passes pi/4",
            tip > 0 and Fraction(1, 2) >= claim.T,
            f"T^2 + 2T - 1 = {text(tip)}",
        ),
        Check(
            "slabs: the endpoints partition [eps, T]",
            len(ends) >= 2
            and all(p < q for p, q in itertools.pairwise(ends))
            and Fraction(first, claim.den) == claim.eps
            and Fraction(last, claim.den) == claim.T
            and first > 0
            and 2 * last <= claim.den <= 10**7,
            f"{len(ends) - 1} slabs from {first} to {last} over {claim.den}",
        ),
        Check(
            "slabs: the kernel's threshold is at least tau",
            Fraction(threshold) >= claim.tau
            and 0 < claim.tau.numerator < 10**8
            and 0 < claim.tau.denominator < 10**8,
            f"up(fl(tau)) - tau = {float(Fraction(threshold) - claim.tau):.3g}",
        ),
        Check(
            "slabs: the receipts' least leaf bound is at least the threshold",
            least >= Fraction(threshold),
            f"{text(least)}, above tau by {float(least - claim.tau):.3g}",
        ),
        Check(
            "near-axis: W increases on [0, eps] and A <= B",
            near < 0 and extent(claim.eps) >= 1 and claim.A <= claim.B,
            f"eps^2 + 2 eps - 1 = {float(near):.6g}",
        ),
        Check(
            "near-axis: A W(eps) <= B",
            margin >= 0,
            f"B - A W(eps) = {text(margin)}",
        ),
        Check(
            "axis: the receipts' minimum is at least tau",
            f.minimum >= required,
            f"{f.minimum} against ceil(1e27 tau) = {required}",
        ),
    ]


def audit(claim: Claim, f: Facts, least: Fraction) -> list[Check]:
    return density_checks(f, claim) + chain_checks(claim, f, least)


def scalar_block(claim: Claim) -> dict[str, str]:
    """The receipt's ``scalar`` block, as this tool computes it."""
    return {
        "X": text(claim.X),
        "axis_containment_margin": text(claim.B - claim.A * extent(claim.eps)),
        "claim": f"s({claim.n}) > {text(claim.X)}",
        "counting_margin": text(claim.n * claim.tau - claim.mass),
        "mass": text(claim.mass),
        "threshold": text(claim.tau),
    }


def coverage_block(slabs: Sequence[dict[str, Any]]) -> dict[str, object]:
    outputs = [json.loads(row["stdout"]) for row in slabs]
    least, _ = least_bound(slabs)
    return {
        "angle_bisections": sum(int(z["angle_splits"]) for z in outputs),
        "leaves": sum(int(z["leaves"]) for z in outputs),
        "minimum_capture_lower": text(least),
        "nodes": sum(int(z["nodes"]) for z in outputs),
        "slabs": len(outputs),
    }


def axis_block(stdout: dict[str, Any], claim: Claim) -> dict[str, object]:
    minimum = Fraction(int(stdout["minimum_numerator"]), int(stdout["scale"]))
    return {
        "margin": text(minimum - claim.tau),
        "minimum_capture_lower": text(minimum),
        "vertices": int(stdout["x_nodes"]) * int(stdout["y_nodes"]),
    }


def admission_block(f: Facts) -> dict[str, object]:
    return {
        "axis_evaluation_bound": str(f.evaluation_bound),
        "axis_input_sha256": f.axis_sha256,
        "mass": text(f.mass),
        "pose_input_sha256": f.pose_sha256,
        "positive_representatives": f.positive,
        "source_sha256": f.sha256,
        "terms": f.terms,
    }


def manifest() -> dict[str, str]:
    """The packet's subtree manifest: upstream path to SHA-256."""
    out: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, path = line.split(maxsplit=1)
        out[path.removeprefix("./")] = digest
    return out


FLAGS = ("-O3", "-std=c++17", "-fno-fast-math", "-ffp-contract=off")
AXIS_FLAGS = ("-O2", "-std=c++17")
KERNEL_SOURCES = {
    "pose": "verifier/continuous_pose.cpp",
    "axis": "verifier/axis_integer_grid.cpp",
}
TIMING = frozenset({"seconds"})


def slab_output(row: dict[str, Any]) -> dict[str, Any]:
    value: dict[str, Any] = json.loads(str(row["stdout"]))
    return value


def without(value: dict[str, Any], keys: Iterable[str]) -> dict[str, Any]:
    drop = frozenset(keys)
    return {k: v for k, v in value.items() if k not in drop}


def slab_row_checks(name: str, rows: Sequence[dict[str, Any]], pose_binary: str) -> list[Check]:
    """Every slab row of one release receipt: the contract's arguments, exit 0, the
    identities, and a verified kernel output whose counts close the cover."""
    digests = manifest()
    good = 0
    problems: list[str] = []
    for index, ((lo, hi), row) in enumerate(zip(CLAIM.slabs(), rows, strict=False)):
        out = slab_output(row)
        args = [str(lo), str(hi), str(CLAIM.den), "4999", "5000", str(CLAIM.budget)]
        fine = (
            row.get("index") == index
            and row.get("arguments") == args
            and row.get("exit_code") == 0
            and row.get("timed_out") is False
            and row.get("input_sha256") == POSE_SHA256
            and row.get("source_sha256") == digests[KERNEL_SOURCES["pose"]]
            and row.get("binary_sha256") == pose_binary
            and row.get("stderr_sha256") == sha256(b"")
            and out.get("status") == "verified"
            and (out.get("pl"), out.get("ph"), out.get("den")) == (lo, hi, CLAIM.den)
            and int(out["nodes"]) == 2 * int(out["leaves"]) - 1
            and Fraction(out["lower_bound"]) >= Fraction(kernel_threshold(CLAIM.tau))
        )
        good += fine
        if not fine:
            problems.append(str(index))
    return [
        Check(
            f"{name} receipt: every slab verified as the contract runs it",
            good == len(rows) == len(CLAIM.slabs()),
            f"{good} of {len(rows)}" + (f"; not {', '.join(problems)}" if problems else ""),
        )
    ]


def receipt_checks(name: str, folder: Path, claim: Claim, f: Facts) -> list[Check]:
    """One release receipt against this tool's values."""
    receipt = read_receipt(folder)
    slabs = read_slabs(folder)
    axis = read_receipt(folder, "axis.json")
    stdout = parse_axis_stdout(axis)
    binaries = receipt.get("binaries") or {}
    digests = manifest()
    sources = receipt.get("source_sha256") or {}
    checks = [
        Check(
            f"{name} receipt: parameters", receipt.get("parameters") == claim.parameters(), ""
        ),
        Check(
            f"{name} receipt: scalar block",
            receipt.get("scalar") == scalar_block(claim),
            str(receipt.get("scalar", {}).get("counting_margin")),
        ),
        Check(
            f"{name} receipt: admission block",
            receipt.get("admission") == admission_block(f),
            "the derived inputs' digests and counts",
        ),
        Check(
            f"{name} receipt: coverage block is the slabs' totals",
            receipt.get("coverage") == coverage_block(slabs),
            json.dumps(coverage_block(slabs), sort_keys=True),
        ),
        Check(
            f"{name} receipt: axis block is the axis output's",
            receipt.get("axis") == axis_block(stdout, claim),
            json.dumps(axis_block(stdout, claim), sort_keys=True),
        ),
        Check(
            f"{name} receipt: slab and axis records by digest",
            receipt.get("slabs_sha256") == sha256((folder / "slabs.jsonl").read_bytes())
            and receipt.get("axis_sha256") == sha256((folder / "axis.json").read_bytes()),
            f"{receipt.get('slabs_sha256')}, {receipt.get('axis_sha256')}",
        ),
        Check(
            f"{name} receipt: the source it ran is the retained tree",
            bool(sources) and all(digests.get(path) == d for path, d in sources.items()),
            f"{sum(digests.get(p) == d for p, d in sources.items())} of {len(sources)} files",
        ),
        Check(
            f"{name} receipt: status and flags",
            receipt.get("status") == "REPLAYED_SAME_KERNEL"
            and receipt.get("claim") == f"s({claim.n}) > {text(claim.X)}"
            and receipt.get("compile_flags") == list(FLAGS),
            str(receipt.get("status")),
        ),
        Check(
            f"{name} receipt: the axis run",
            axis.get("exit_code") == 0
            and axis.get("input_sha256") == AXIS_SHA256
            and axis.get("source_sha256") == digests[KERNEL_SOURCES["axis"]]
            and axis.get("binary_sha256") == binaries.get("axis")
            and stdout.get("status") == "AXIS_COVERAGE_PROVED"
            and (stdout.get("x_nodes"), stdout.get("y_nodes")) == f.nodes
            and stdout.get("scale") == str(GRID**3)
            and stdout.get("direct_sum_matches") is True
            and stdout.get("evaluation_abs_bound") == str(f.evaluation_bound)
            and int(stdout["minimum_numerator"]) == f.minimum,
            str(stdout.get("status")),
        ),
        *slab_row_checks(name, slabs, str(binaries.get("pose"))),
    ]
    stages = {stage["stage"]: stage["exit_code"] for stage in receipt.get("stages", [])}
    checks.append(
        Check(
            f"{name} receipt: the fourteen stages exited as expected",
            stages == RELEASE_STAGES,
            ", ".join(f"{k} {v}" for k, v in stages.items()),
        )
    )
    return checks


#: The release's control stages and the exits ``run.py`` requires of them.
RELEASE_STAGES = {
    "build-pose": 0,
    "build-axis": 0,
    "unit-tests": 0,
    "exact-oracle": 0,
    "build-rounding": 0,
    "ieee-neighbors": 0,
    "wrong-rounding": -6,
    "ftz": -6,
    "reject-ndebug": 1,
    "reject-fastmath": 1,
    "synthetic-positive": 0,
    "synthetic-negative": 3,
    "limited-budget": 3,
    "axis": 0,
}


def identity_checks() -> list[Check]:
    """What tells the two receipts apart (GC-3), and what they share."""
    local, ci = read_receipt(RECEIPTS["local"]), read_receipt(RECEIPTS["ci"])
    slabs = {name: read_slabs(folder) for name, folder in RECEIPTS.items()}
    axes = {name: read_receipt(folder, "axis.json") for name, folder in RECEIPTS.items()}
    same = sum(
        without(slab_output(a), TIMING) == without(slab_output(b), TIMING)
        and without(a, {"seconds", "stdout", "binary_sha256"})
        == without(b, {"seconds", "stdout", "binary_sha256"})
        for a, b in zip(slabs["local"], slabs["ci"], strict=True)
    )
    ci_sums = (PACKET / "release-ci/SHA256SUMS").read_text(encoding="utf-8").splitlines()
    tree_sums = (SOURCE / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    result_lines = {
        f"{sha256((RECEIPTS['ci'] / name).read_bytes())}  results/{name}"
        for name in ("axis.json", "slabs.jsonl", "verification.json")
    }
    return [
        Check(
            "local receipt: the producer's run, not CI",
            local.get("source_commit") is None and "15.2.0" in str(local.get("compiler")),
            f"{local.get('compiler')}, Python {local.get('python')}, {local.get('seconds')} s",
        ),
        Check(
            "ci receipt: run 38059878931 on the pin, the binaries g++ 13.3.0 rebuilds",
            ci.get("source_commit") == PIN
            and ci.get("compiler") == CI_COMPILER
            and ci.get("binaries") == CI_BINARIES,
            f"{ci.get('compiler')}, Python {ci.get('python')}, {ci.get('seconds')} s",
        ),
        Check(
            "receipts: every slab identical apart from timing and the binary",
            same == len(slabs["local"]) == len(slabs["ci"]) == len(CLAIM.slabs()),
            f"{same} of {len(slabs['ci'])}",
        ),
        Check(
            "receipts: the axis outputs identical",
            parse_axis_stdout(axes["local"]) == parse_axis_stdout(axes["ci"]),
            "every field",
        ),
        Check(
            "release-ci SHA256SUMS: the tree's but for the three results lines",
            len(ci_sums) == len(tree_sums) == 27
            and result_lines <= set(ci_sums)
            and len(set(ci_sums) - set(tree_sums)) == 3
            and len(set(tree_sums) - set(ci_sums)) == 3,
            "the CI receipts' digests",
        ),
    ]


# --------------------------------------------------------------------------- controls


@dataclass(frozen=True)
class FiniteControl:
    name: str
    change: str
    claim: Claim
    #: The checks of `chain_checks` that must fail on it.
    expect: tuple[str, ...]


FINITE_CONTROLS = (
    FiniteControl(
        "G",
        "A replaced by 997644/10^6 (the contract's)",
        replace(CLAIM, A=Fraction(997644, 10**6)),
        ("near-axis: A W(eps) <= B",),
    ),
    FiniteControl(
        "G2",
        "tau replaced by 3999/4000, where 40 tau = M",
        replace(CLAIM, tau=Fraction(3999, 4000)),
        ("counting: n tau - M > 0",),
    ),
    FiniteControl(
        "G3",
        "T replaced by 41/100, short of pi/4",
        replace(CLAIM, T=Fraction(41, 100)),
        ("slabs: T passes pi/4", "slabs: the endpoints partition [eps, T]"),
    ),
    FiniteControl(
        "G4",
        "eps replaced by 1/10^5",
        replace(CLAIM, eps=Fraction(1, 10**5)),
        ("near-axis: A W(eps) <= B", "slabs: the endpoints partition [eps, T]"),
    ),
)


def finite_controls(f: Facts, least: Fraction) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for control in FINITE_CONTROLS:
        failed = [c.name for c in chain_checks(control.claim, f, least) if not c.held]
        margin = control.claim.B - control.claim.A * extent(control.claim.eps)
        out.append(
            {
                "control": control.name,
                "change": control.change,
                "expect_failed": list(control.expect),
                "failed": failed,
                "refused": all(name in failed for name in control.expect),
                "near_axis_margin": text(margin),
                "near_axis_margin_decimal": f"{float(margin):.6g}",
            }
        )
    return out


def check_report(f: Facts) -> dict[str, Any]:
    least, at = least_bound(read_slabs(RECEIPTS["ci"]))
    checks = audit(CLAIM, f, least)
    parameters = json.loads(PARAMETERS.read_text(encoding="utf-8"))
    checks.append(
        Check(
            "retained parameters.json is the claim",
            parameters == CLAIM.parameters(),
            "all keys",
        )
    )
    for name, folder in RECEIPTS.items():
        checks += receipt_checks(name, folder, CLAIM, f)
    checks += identity_checks()
    controls = finite_controls(f, least)
    held = all(c.held for c in checks) and all(item["refused"] for item in controls)
    margin = CLAIM.B - CLAIM.A * extent(CLAIM.eps)
    return {
        "kind": "continuous-pose-finite-audit/v1",
        "claim": f"s(40) > {text(CLAIM.X)}",
        "candidate": str(CANDIDATE.relative_to(REPO)),
        "values": {
            "counting_margin": text(CLAIM.n * CLAIM.tau - CLAIM.mass),
            "raise_over_T133": text(RAISE),
            "near_axis_margin": text(margin),
            "near_axis_margin_decimal": f"{float(margin):.6g}",
            "kernel_threshold": float.hex(kernel_threshold(CLAIM.tau)),
            "least_leaf_bound": text(least),
            "least_leaf_bound_slab": at,
            "least_leaf_bound_minus_tau": f"{float(least - CLAIM.tau):.6g}",
            "axis_minimum": text(Fraction(f.minimum, GRID**3)),
            "axis_margin": text(Fraction(f.minimum, GRID**3) - CLAIM.tau),
            "axis_margin_decimal": f"{float(Fraction(f.minimum, GRID**3) - CLAIM.tau):.6g}",
            "axis_minimiser": [f.minimiser[0], f.minimiser[1]],
            "g_capture_at_axis_minimiser": f"{float(f.minimiser_capture_g):.15g}",
            "dominated_mass_deficit": f"{float(CLAIM.mass - f.dominated_mass):.6g}",
            "evaluation_bound": str(f.evaluation_bound),
            "pose_input_sha256": f.pose_sha256,
            "axis_input_sha256": f.axis_sha256,
            "crate_inputs_sha256": f.crate_sha256,
        },
        "checks": [c.as_json() for c in checks],
        "controls": controls,
        "status": "FINITE_STEPS_HOLD" if held else "FINITE_AUDIT_FAILED",
    }


# --------------------------------------------------------------------------- running


def clean_env() -> dict[str, str]:
    """The environment the release's runner requires: no compiler or loader overrides."""
    drop = {"CFLAGS", "CXXFLAGS", "LDFLAGS", "LD_PRELOAD", "LD_LIBRARY_PATH", "PYTHONPATH"}
    return {k: v for k, v in os.environ.items() if k not in drop}


def spawn(argv: Sequence[str], cwd: Path, stem: Path) -> dict[str, Any]:
    """Run one command in ``cwd`` with its output in ``stem.stdout`` and ``stem.stderr``;
    the exit code (a signal as its negative), wall and CPU time (wait4), and load."""
    before = os.getloadavg()
    started = datetime.now(UTC).isoformat(timespec="seconds")
    start = time.monotonic()
    with (
        stem.with_suffix(".stdout").open("wb") as out,
        stem.with_suffix(".stderr").open("wb") as err,
    ):
        process = subprocess.Popen(list(argv), cwd=cwd, env=clean_env(), stdout=out, stderr=err)
        _, status, usage = os.wait4(process.pid, 0)
        process.returncode = os.waitstatus_to_exitcode(status)
    return {
        "exit_code": process.returncode,
        "started_utc": started,
        "wall_seconds": round(time.monotonic() - start, 3),
        "cpu_seconds": round(usage.ru_utime + usage.ru_stime, 3),
        "loadavg_before": [round(v, 2) for v in before],
        "loadavg_after": [round(v, 2) for v in os.getloadavg()],
        "stdout": stem.with_suffix(".stdout").read_text(encoding="utf-8", errors="replace"),
        "stderr": stem.with_suffix(".stderr").read_text(encoding="utf-8", errors="replace"),
    }


@dataclass(frozen=True)
class Layout:
    """The scratch directory of one replay."""

    out: Path

    @property
    def tree(self) -> Path:
        return self.out / "tree"

    @property
    def build(self) -> Path:
        return self.out / "build"

    @property
    def pose(self) -> Path:
        return self.out / "pose"

    @property
    def logs(self) -> Path:
        return self.out / "logs"

    @property
    def receipts(self) -> Path:
        return self.out / "receipts"

    def binary(self, name: str) -> Path:
        return self.build / {"pose": "continuous", "axis": "axis", "rounding": "rounding"}[name]


#: The builds, each from the tree's directory with relative source paths, as the
#: release's runner does: ``__FILE__`` in an assertion is the path given, so a build
#: from another directory gives another pose binary (item 6 of the review).
def build_commands(layout: Layout) -> dict[str, list[str]]:
    return {
        "pose": ["g++", *FLAGS, KERNEL_SOURCES["pose"], "-o", str(layout.binary("pose"))],
        "axis": ["g++", *AXIS_FLAGS, KERNEL_SOURCES["axis"], "-o", str(layout.binary("axis"))],
        "rounding": [
            "g++",
            *FLAGS,
            "-I",
            "verifier",
            "tests/rounding_harness.cpp",
            "-o",
            str(layout.binary("rounding")),
        ],
    }


#: Control F's two compilations, which the kernel's ``#error`` must refuse.
def reject_commands(layout: Layout) -> dict[str, list[str]]:
    target = str(layout.build / "rejected.o")
    return {
        "reject-ndebug": [
            "g++",
            "-std=c++17",
            "-DNDEBUG",
            "-c",
            KERNEL_SOURCES["pose"],
            "-o",
            target,
        ],
        "reject-fastmath": [
            "g++",
            "-std=c++17",
            "-ffast-math",
            "-c",
            KERNEL_SOURCES["pose"],
            "-o",
            target,
        ],
    }


BUILD_FILES = (*KERNEL_SOURCES.values(), "tests/rounding_harness.cpp")


def build_all(layout: Layout) -> dict[str, Any]:
    """Copy the retained kernel sources into a scratch tree and build there."""
    digests = manifest()
    for path in BUILD_FILES:
        target = layout.tree / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE / path, target)
    layout.build.mkdir(parents=True, exist_ok=True)
    layout.logs.mkdir(parents=True, exist_ok=True)
    version = subprocess.run(
        ["g++", "--version"], capture_output=True, text=True, check=True
    ).stdout.splitlines()[0]
    full = subprocess.run(
        ["g++", "-dumpfullversion"], capture_output=True, text=True, check=True
    ).stdout.strip()
    builds: dict[str, Any] = {}
    for name, argv in build_commands(layout).items():
        record = spawn(argv, layout.tree, layout.logs / f"build-{name}")
        binary = layout.binary(name)
        record["binary_sha256"] = sha256(binary.read_bytes()) if binary.exists() else None
        builds[name] = {"argv": [*argv[:-1], binary.name], **record}
    return {
        "kind": "continuous-pose-replay-builds/v1",
        "compiler": version,
        "compiler_version": full,
        "sources": {path: digests[path] for path in BUILD_FILES},
        "cwd": "a copy of the retained verifier/ and tests/ files, at their upstream paths",
        "builds": builds,
    }


def write_inputs(layout: Layout, density: Density) -> dict[str, str]:
    layout.pose.mkdir(parents=True, exist_ok=True)
    pose = pose_input(density)
    axis = axis_input(axis_rows(density))
    (layout.pose / "certificate_input.txt").write_bytes(pose)
    (layout.out / "axis-input.txt").write_bytes(axis)
    return {"pose": sha256(pose), "axis": sha256(axis)}


def slab_args(lo: int, hi: int, claim: Claim = CLAIM) -> list[str]:
    tau = claim.tau
    return [
        str(lo),
        str(hi),
        str(claim.den),
        str(tau.numerator),
        str(tau.denominator),
        str(claim.budget),
    ]


def run_axis(layout: Layout, inputs: dict[str, str]) -> dict[str, Any]:
    binary = layout.binary("axis")
    argv = [str(binary), "axis-input.txt"]
    record = spawn(argv, layout.out, layout.logs / "axis")
    return {
        "kind": "continuous-pose-replay-axis/v1",
        "argv": ["axis", "axis-input.txt"],
        "binary_sha256": sha256(binary.read_bytes()),
        "input_sha256": inputs["axis"],
        **record,
    }


def run_slabs(layout: Layout, inputs: dict[str, str], workers: int) -> list[dict[str, Any]]:
    """The 43 slabs, each ``continuous PL PH 1000000 4999 5000 30000000`` in the
    directory holding the pose input, on at most ``workers`` processes."""
    binary = layout.binary("pose")
    binary_sha = sha256(binary.read_bytes())

    def one(item: tuple[int, tuple[int, int]]) -> dict[str, Any]:
        index, (lo, hi) = item
        args = slab_args(lo, hi)
        record = spawn([str(binary), *args], layout.pose, layout.logs / f"slab-{index:03d}")
        print(
            f"slab {index}: exit {record['exit_code']}, {record['wall_seconds']} s", flush=True
        )
        return {
            "index": index,
            "argv": ["continuous", *args],
            "binary_sha256": binary_sha,
            "input_sha256": inputs["pose"],
            **record,
        }

    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(one, enumerate(CLAIM.slabs())))


# --------------------------------------------------------------------------- kernel controls


type Rect = tuple[Fraction, Fraction, Fraction, Fraction, Fraction]


def synthetic_input(rects: Sequence[Rect], claim: Claim = CLAIM) -> bytes:
    """A pose-kernel input for a synthetic density, in the release's format."""
    lines = [hex_pair(claim.L), decimal_pair(claim.B), str(len(rects))]
    lines += [" ".join(hex_pair(v) for v in rect) for rect in rects]
    return ("\n".join(lines) + "\n").encode()


def cut_area(h: Fraction, t: Fraction, side: Fraction) -> Fraction:
    """The area of a side-``side`` square at half-angle tangent ``t`` beyond a line at
    depth ``h`` below its highest vertex: a triangle while ``h <= side sin``, then a strip
    while ``h <= side cos``. It decreases in the angle on ``(0, pi/4]``."""
    c, s = half_angle(t)
    if h <= side * s:
        return h * h / (2 * s * c)
    if h > side * c:
        raise ValueError("the cut reaches past the strip regime")
    return side / c * (h - side * s / 2)


#: Control C's slabs and depths (the review's seven slab-depth pairs).
CUT_CASES = (
    ((1, 500), Fraction(1, 2000)),
    ((1, 500), Fraction(1, 10000)),
    ((500, 10000), Fraction(1, 100)),
    ((500, 10000), Fraction(1, 1000)),
    ((10000, 20000), Fraction(1, 50)),
    ((200000, 210000), Fraction(1, 20)),
    ((410000, 415000), Fraction(1, 20)),
)
#: Control D's slabs and the gap's height.
GAP_SLABS = ((1, 500), (500, 10000), (100000, 110000), (300000, 310000), (400000, 410000))
GAP = Fraction(1, 100)
#: The budget the review's synthetic runs used; B runs on the full budget.
CONTROL_BUDGET = 1_500_000
BELOW = Fraction(-1, 10**9)
ABOVE = Fraction(1, 10**4)


@dataclass(frozen=True)
class KernelControl:
    """One run of the pose kernel on a synthetic density or a short budget."""

    name: str
    group: str
    slab: tuple[int, int]
    rects: tuple[Rect, ...] | None  # None: the real pose input
    budget: int
    expect_exit: int
    #: The exact least capture over the slab, where it is known in closed form.
    least: Fraction | None = None
    max_nodes: int | None = None


ZERO = Fraction(0)


def uniform(rho: Fraction, claim: Claim = CLAIM) -> tuple[Rect, ...]:
    """Density ``rho`` on the whole container."""
    return ((ZERO, ZERO, claim.L, claim.L, rho),)


def gap_area(t: Fraction, claim: Claim = CLAIM) -> Fraction:
    """A side-``B`` square centred on the gap loses ``g B / cos``, the most at the
    slab's right end."""
    c, _ = half_angle(t)
    return claim.B * claim.B - GAP * claim.B / c


def gap_control(
    name: str,
    slab: tuple[int, int],
    rho: Fraction,
    *,
    expect: int,
    claim: Claim = CLAIM,
    max_nodes: int | None = None,
) -> KernelControl:
    """Density ``rho`` off a horizontal gap of height `GAP` through the container's
    middle: the least capture is at the slab's right end, centred on the gap."""
    side = claim.L
    c1, s1 = half_angle(Fraction(slab[1], claim.den))
    if claim.B * (c1 - s1) < GAP:
        raise ValueError("the gap leaves the square's middle band")
    rects = (
        (ZERO, ZERO, side, side / 2 - GAP / 2, rho),
        (ZERO, side / 2 + GAP / 2, side, side, rho),
    )
    least = rho * gap_area(Fraction(slab[1], claim.den), claim)
    group = "D" if expect else "E"
    return KernelControl(name, group, slab, rects, CONTROL_BUDGET, expect, least, max_nodes)


def cut_controls(delta: Fraction, group: str, expect: int, claim: Claim) -> list[KernelControl]:
    """Density on the container less a strip of depth ``h`` at the top or the right,
    scaled so that the least capture, at the slab's left end, is ``tau (1 + delta)``."""
    side, core, tau = claim.L, claim.B, claim.tau
    out: list[KernelControl] = []
    for slab, h in CUT_CASES:
        t0 = Fraction(slab[0], claim.den)
        rho = tau * (1 + delta) / (core * core - cut_area(h, t0, core))
        edges: tuple[tuple[str, Rect], ...] = (
            ("top", (ZERO, ZERO, side, side - h, rho)),
            ("right", (ZERO, ZERO, side - h, side, rho)),
        )
        out += [
            KernelControl(
                f"{group}-cut-{edge}-{slab[0]}-{slab[1]}-h{h.denominator}",
                group,
                slab,
                (rect,),
                CONTROL_BUDGET,
                expect,
                least=tau * (1 + delta),
                max_nodes=260_000 if group == "E" else None,
            )
            for edge, rect in edges
        ]
    return out


def kernel_controls(claim: Claim = CLAIM) -> list[KernelControl]:
    """The contract's controls A to E as pose-kernel runs."""
    core, tau = claim.B, claim.tau
    out = [
        KernelControl(
            "A-synthetic-negative", "A", (1, 415000), uniform(Fraction(1, 2)), 10000, 3
        ),
        KernelControl("A-synthetic-positive", "A", (1, 415000), uniform(Fraction(2)), 10000, 0),
        KernelControl("A-limited-budget", "A", (100000, 110000), None, 1, 3),
    ]
    rho = tau * (1 + BELOW) / (core * core)
    out += [
        KernelControl(
            f"B-uniform-{slab[0]}-{slab[1]}",
            "B",
            slab,
            uniform(rho, claim),
            claim.budget,
            3,
            least=tau * (1 + BELOW),
            max_nodes=100,
        )
        for slab in ((1, 500), (100000, 110000), (410000, 415000))
    ]
    out += cut_controls(BELOW, "C", 3, claim) + cut_controls(ABOVE, "E", 0, claim)
    for slab in GAP_SLABS:
        rho = tau * (1 + BELOW) / gap_area(Fraction(slab[1], claim.den), claim)
        out.append(gap_control(f"D-gap-{slab[0]}-{slab[1]}", slab, rho, expect=3, claim=claim))
    slab = (400000, 410000)
    t0, t1 = Fraction(slab[0], claim.den), Fraction(slab[1], claim.den)
    spread = (gap_area(t0, claim) - gap_area(t1, claim)) / gap_area(t1, claim)
    rho = tau * (1 + ABOVE + spread) / gap_area(t1, claim)
    out.append(
        gap_control(
            f"E-gap-{slab[0]}-{slab[1]}", slab, rho, expect=0, claim=claim, max_nodes=141_000
        )
    )
    return out


#: Control H on the axis kernel: the contract's threshold, and a pair either side of the
#: minimum, ``999803584931... / 10^27``.
AXIS_CONTROLS = (
    ("H-tau-1-2", Fraction(1, 2)),
    ("H-tau-999804", Fraction(999804, 10**6)),
    ("H-tau-999803", Fraction(999803, 10**6)),
)


def run_controls(layout: Layout, density: Density, workers: int) -> list[dict[str, Any]]:
    """Controls A to F and H: the pose kernel on synthetic densities and a short budget,
    the rounding harness, the two compilations the kernel refuses, and the axis kernel
    at other thresholds."""
    controls_dir = layout.out / "controls"
    controls_dir.mkdir(parents=True, exist_ok=True)
    pose = layout.binary("pose")
    records: list[dict[str, Any]] = []

    def one(control: KernelControl) -> dict[str, Any]:
        if control.rects is None:
            cwd = layout.pose
        else:
            cwd = controls_dir / control.name
            cwd.mkdir(parents=True, exist_ok=True)
            (cwd / "certificate_input.txt").write_bytes(synthetic_input(control.rects))
        args = [
            str(control.slab[0]),
            str(control.slab[1]),
            str(CLAIM.den),
            "4999",
            "5000",
            str(control.budget),
        ]
        record = spawn([str(pose), *args], cwd, layout.logs / f"control-{control.name}")
        print(f"{control.name}: exit {record['exit_code']}", flush=True)
        return {
            "control": control.name,
            "group": control.group,
            "argv": ["continuous", *args],
            "input_sha256": sha256((cwd / "certificate_input.txt").read_bytes()),
            "expect_exit": control.expect_exit,
            "least_capture": None if control.least is None else text(control.least),
            "max_nodes": control.max_nodes,
            **record,
        }

    with ThreadPoolExecutor(max_workers=workers) as pool:
        records += list(pool.map(one, kernel_controls()))
    rounding = layout.binary("rounding")
    for name, argv, expect in (
        ("F-ieee-neighbors", [str(rounding)], 0),
        ("F-wrong-rounding", [str(rounding), "rounding"], -6),
        ("F-ftz", [str(rounding), "ftz"], -6),
    ):
        record = spawn(argv, layout.pose, layout.logs / f"control-{name}")
        records.append(
            {
                "control": name,
                "group": "F",
                "argv": ["rounding", *argv[1:]],
                "expect_exit": expect,
                **record,
            }
        )
    for name, argv in reject_commands(layout).items():
        record = spawn(argv, layout.tree, layout.logs / f"control-F-{name}")
        records.append(
            {
                "control": f"F-{name}",
                "group": "F",
                "argv": [*argv[:-1], "rejected.o"],
                "expect_exit": 1,
                **record,
            }
        )
    rows = axis_rows(density)
    for name, tau in AXIS_CONTROLS:
        path = layout.out / f"axis-input-{name}.txt"
        data = axis_input(rows, tau=tau)
        path.write_bytes(data)
        record = spawn(
            [str(layout.binary("axis")), path.name], layout.out, layout.logs / f"control-{name}"
        )
        records.append(
            {
                "control": name,
                "group": "H",
                "argv": ["axis", path.name],
                "tau": text(tau),
                "input_sha256": sha256(data),
                **record,
            }
        )
    return records


# --------------------------------------------------------------------------- the crate


CRATE_RUNS = (
    ("crate-axis-A", "axis-A", "0", 1),
    ("crate-net401-B", "net401-B", "all", 2),
)


def run_crate(layout: Layout, density: Density, binary: Path) -> dict[str, Any]:
    """The contract's first-party runs: the axis at side ``A`` (item 3) and the
    401-direction necessary condition at side ``B`` (item 6), threshold one on the
    scaled density. Refuses unless the tree's crate source is one a soundness review
    accepted for a declared net, as the census route does."""
    source = crate_source_sha256()
    reviewed = REVIEWED_SOURCES.get(source)
    if reviewed is None or not reviewed.declared_nets:
        raise SystemExit(f"{source} is not reviewed source for a declared net")
    crate = layout.out / "crate"
    crate.mkdir(parents=True, exist_ok=True)
    inputs = crate_inputs(density)
    runs: dict[str, Any] = {}
    for stem, name, directions, threads in CRATE_RUNS:
        (crate / f"{name}.json").write_bytes(inputs[name])
        argv = [
            str(binary),
            "--candidate",
            f"{name}.json",
            "--n",
            "40",
            "--side",
            "67/10",
            "--directions",
            directions,
            "--threshold",
            "1",
            "--threads",
            str(threads),
            "--confirm",
        ]
        record = spawn(argv, crate, layout.logs / stem)
        print(f"{stem}: exit {record['exit_code']}, {record['wall_seconds']} s", flush=True)
        runs[stem] = {
            "argv": ["sqverify-fast", *argv[1:]],
            "input_sha256": sha256(inputs[name]),
            **record,
        }
    return {
        "kind": "continuous-pose-replay-crate/v1",
        "binary_sha256": sha256(binary.read_bytes()),
        "crate_source_sha256": source,
        "reviewed_source": {"commit": reviewed.commit, "review": reviewed.review},
        "runs": runs,
    }


# --------------------------------------------------------------------------- control G


#: Control G as the contract states it, on the release's own finite code: ``exact.py``'s
#: ``scalar()`` on a copy whose axis side is the mutant, beside the unchanged copy.
RELEASE_G: tuple[tuple[str, tuple[str, str] | None], ...] = (
    ("G-release-unchanged", None),
    ("G-release-axis-side", ("'axis_side':'997643/1000000'", "'axis_side':'997644/1000000'")),
)
#: Runs one copy's ``scalar()`` and prints its block, or the tag it refused with.
SCALAR_DRIVER = """\
import json, runpy, sys
space = runpy.run_path(sys.argv[1], run_name="exact")
try:
    print(json.dumps({"scalar": space["scalar"]()}, sort_keys=True))
except ValueError as error:
    print(json.dumps({"refused": str(error)}))
    sys.exit(4)
"""


def run_release_g(layout: Layout) -> dict[str, Any]:
    """The release's ``scalar()`` on the unchanged and the mutated copy of its
    ``exact.py``, each copied into scratch and run there under ``python -I``, so that
    neither the source directory nor the working directory is on the import path."""
    folder = layout.out / "release"
    folder.mkdir(parents=True, exist_ok=True)
    original = (SOURCE / "verifier/exact.py").read_text(encoding="utf-8")
    runs: dict[str, Any] = {}
    for name, change in RELEASE_G:
        if change is not None and original.count(change[0]) != 1:
            raise SystemExit(f"{name}: the release's exact.py does not set the axis side once")
        body = original if change is None else original.replace(*change)
        path = folder / f"{name}.py"
        path.write_text(body, encoding="utf-8")
        argv = [sys.executable, "-I", "-c", SCALAR_DRIVER, path.name]
        record = spawn(argv, folder, layout.logs / f"control-{name}")
        runs[name] = {
            "argv": ["python", "-I", "-c", "SCALAR_DRIVER", path.name],
            "change": None if change is None else list(change),
            "copy_sha256": sha256(body.encode()),
            **record,
        }
    return {
        "kind": "continuous-pose-replay-release-g/v1",
        "exact_py_sha256": manifest()["verifier/exact.py"],
        "driver_sha256": sha256(SCALAR_DRIVER.encode()),
        "python": sys.version.split()[0],
        "runs": runs,
    }


STAGES = ("builds", "axis", "slabs", "controls", "crate", "release-g")


def pack_jsonl(rows: Iterable[dict[str, Any]]) -> bytes:
    body = "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows)
    return gzip.compress(body.encode(), compresslevel=9, mtime=0)


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def run_replay(out: Path, workers: int, stages: Sequence[str], crate: Path | None) -> None:
    """The contract's runs, receipts into ``out/receipts``. Each stage writes its own
    receipt, so a stage can be run again alone after ``builds``."""
    layout = Layout(out)
    layout.receipts.mkdir(parents=True, exist_ok=True)
    layout.logs.mkdir(parents=True, exist_ok=True)
    density = load_density()
    inputs = write_inputs(layout, density)
    print(f"inputs: pose {inputs['pose']}, axis {inputs['axis']}", flush=True)
    if "builds" in stages:
        builds = build_all(layout)
        write_json(layout.receipts / "builds.json", builds)
        for name, item in builds["builds"].items():
            print(
                f"build {name}: exit {item['exit_code']}, {item['binary_sha256']}", flush=True
            )
    if "axis" in stages:
        write_json(layout.receipts / "axis-run.json", run_axis(layout, inputs))
    if "slabs" in stages:
        start = time.monotonic()
        rows = run_slabs(layout, inputs, workers)
        (layout.receipts / "slabs.jsonl.gz").write_bytes(pack_jsonl(rows))
        print(f"slabs: {round(time.monotonic() - start, 1)} s wall", flush=True)
    if "controls" in stages:
        records = run_controls(layout, density, workers)
        (layout.receipts / "controls.jsonl.gz").write_bytes(pack_jsonl(records))
    if "crate" in stages:
        if crate is None:
            raise SystemExit("--crate-binary is required for the crate stage")
        write_json(layout.receipts / "crate-runs.json", run_crate(layout, density, crate))
    if "release-g" in stages:
        write_json(layout.receipts / "control-G-release.json", run_release_g(layout))


# --------------------------------------------------------------------------- judging it


#: What the contract states for the complete run, from the release's receipts.
EXPECT = {
    "nodes": 61_860_927,
    "leaves": 30_930_485,
    "angle_splits": 14_096_668,
    "least_bound": Fraction(2251349454150741, 2**51),
    "least_bound_slab": 1,
    "crate_axis_vertices": 4_897_369,
    "crate_axis_bound": 1.0000037044548487,
    "crate_net_nodes": 32_763_798,
    "crate_net_bound": 1.000000000357051,
    "crate_net_bound_r": 289,
}


def jsonl_rows(path: Path) -> list[dict[str, Any]]:
    """A JSON Lines receipt stored plain or as ``X.gz``."""
    return [
        json.loads(line) for line in read_retained_bytes(path).decode().splitlines() if line
    ]


def retained_json(path: Path) -> dict[str, Any]:
    """A JSON receipt stored plain or as ``X.gz``."""
    value: dict[str, Any] = json.loads(read_retained_bytes(path))
    return value


def build_checks(builds: dict[str, Any]) -> list[Check]:
    items = builds["builds"]
    on_ci_compiler = builds["compiler"] == CI_COMPILER
    return [
        Check(
            "builds: the release's flags, exit 0",
            all(items[name]["exit_code"] == 0 for name in ("pose", "axis", "rounding"))
            and items["pose"]["argv"][1:5] == list(FLAGS)
            and items["axis"]["argv"][1:3] == list(AXIS_FLAGS),
            builds["compiler"],
        ),
        Check(
            "builds: the CI run's binaries, on its compiler",
            not on_ci_compiler
            or (
                items["pose"]["binary_sha256"] == CI_BINARIES["pose"]
                and items["axis"]["binary_sha256"] == CI_BINARIES["axis"]
            ),
            f"pose {items['pose']['binary_sha256']}, axis {items['axis']['binary_sha256']}",
        ),
    ]


def axis_run_checks(record: dict[str, Any]) -> list[Check]:
    ours = json.loads(record["stdout"])
    checks = [
        Check(
            "axis run: exit 0",
            record["exit_code"] == 0 and record["stderr"] == "",
            f"{ours.get('status')}, {record['wall_seconds']} s",
        )
    ]
    for name, folder in RECEIPTS.items():
        theirs = parse_axis_stdout(read_receipt(folder, "axis.json"))
        checks.append(
            Check(
                f"axis run: every field equals the {name} receipt's",
                ours == theirs,
                f"minimum {ours.get('minimum_numerator')}",
            )
        )
    return checks


def slab_replay_checks(rows: list[dict[str, Any]]) -> list[Check]:
    outputs = [json.loads(row["stdout"]) for row in rows]
    order = [row["index"] for row in rows] == list(range(len(CLAIM.slabs())))
    argv = all(
        row["argv"] == ["continuous", *slab_args(lo, hi)]
        for row, (lo, hi) in zip(rows, CLAIM.slabs(), strict=False)
    )
    least = min((Fraction(z["lower_bound"]), i) for i, z in enumerate(outputs))
    checks = [
        Check(
            "slabs: 43 runs with the contract's arguments",
            order and argv,
            f"{len(rows)} runs",
        ),
        Check(
            "slabs: every one verified, exit 0",
            all(row["exit_code"] == 0 and row["stderr"] == "" for row in rows)
            and all(z.get("status") == "verified" for z in outputs),
            f"{sum(z.get('status') == 'verified' for z in outputs)} of {len(rows)}",
        ),
        Check(
            "slabs: every cover closes, nodes = 2 leaves - 1",
            all(int(z["nodes"]) == 2 * int(z["leaves"]) - 1 for z in outputs),
            "each slab",
        ),
        Check(
            "slabs: the totals",
            sum(int(z["nodes"]) for z in outputs) == EXPECT["nodes"]
            and sum(int(z["leaves"]) for z in outputs) == EXPECT["leaves"]
            and sum(int(z["angle_splits"]) for z in outputs) == EXPECT["angle_splits"],
            f"{sum(int(z['nodes']) for z in outputs)} nodes, "
            f"{sum(int(z['leaves']) for z in outputs)} leaves, "
            f"{sum(int(z['angle_splits']) for z in outputs)} angle splits",
        ),
        Check(
            "slabs: the least leaf bound",
            least == (EXPECT["least_bound"], EXPECT["least_bound_slab"]),
            f"{text(least[0])} = {float(least[0])!r} at slab {least[1]}",
        ),
    ]
    for name, folder in RECEIPTS.items():
        theirs = [slab_output(row) for row in read_slabs(folder)]
        same = sum(
            without(a, TIMING) == without(b, TIMING)
            for a, b in zip(outputs, theirs, strict=False)
        )
        checks.append(
            Check(
                f"slabs: every non-timing field equals the {name} receipt's",
                same == len(outputs) == len(theirs),
                f"{same} of {len(theirs)}",
            )
        )
    return checks


def control_checks(records: list[dict[str, Any]]) -> list[Check]:
    """Each control's exit, and what the contract says it must show."""
    by_name = {record["control"]: record for record in records}
    checks: list[Check] = []
    for control in kernel_controls():
        record = by_name.get(control.name)
        if record is None:
            checks.append(Check(f"control {control.name}", held=False, detail="not run"))
            continue
        out = json.loads(record["stdout"]) if record["stdout"].strip() else {}
        status = "verified" if control.expect_exit == 0 else "unresolved"
        nodes = int(out.get("nodes", 0))
        held = (
            record["exit_code"] == control.expect_exit
            and out.get("status") == status
            and (control.max_nodes is None or nodes <= control.max_nodes)
        )
        least = "" if control.least is None else f", least capture {float(control.least):.12g}"
        checks.append(
            Check(
                f"control {control.name}",
                held,
                f"exit {record['exit_code']}, {out.get('status')}, {nodes} nodes{least}",
            )
        )
    for name, expect, needle in (
        ("F-ieee-neighbors", 0, '"status":"PASSED","values":1000008'),
        ("F-wrong-rounding", -6, "fegetround()==FE_TONEAREST"),
        ("F-ftz", -6, "_mm_getcsr()"),
        ("F-reject-ndebug", 1, "Assertions and IEEE semantics are required"),
        ("F-reject-fastmath", 1, "Assertions and IEEE semantics are required"),
    ):
        record = by_name.get(name, {"exit_code": None, "stdout": "", "stderr": ""})
        checks.append(
            Check(
                f"control {name}",
                record["exit_code"] == expect and needle in record["stdout"] + record["stderr"],
                f"exit {record['exit_code']}",
            )
        )
    minimum = Fraction(999803584931237207459144828, GRID**3)
    for name, tau in AXIS_CONTROLS:
        record = by_name.get(name, {"exit_code": None, "stdout": ""})
        out = json.loads(record["stdout"]) if record["stdout"].strip() else {}
        refused = tau > minimum
        checks.append(
            Check(
                f"control {name}",
                record["exit_code"] == (2 if refused else 0)
                and out.get("status")
                == ("AXIS_TEST_REFUSED" if refused else "AXIS_COVERAGE_PROVED")
                and out.get("minimum_numerator")
                == str(minimum.numerator * (GRID**3 // minimum.denominator)),
                f"tau {text(tau)}: exit {record['exit_code']}, {out.get('status')}",
            )
        )
    return checks


def crate_premises(summary: dict[str, Any], side: Fraction, step: Fraction, count: int) -> bool:
    """Whether the crate admitted the input the contract names: format T, the 480 rows of
    mass ``M`` scaled by `CRATE_SCALE`, and the net the metadata sets."""
    given = summary.get("premises") or {}
    return (
        given.get("format") == "T"
        and given.get("net_origin") == "metadata"
        and given.get("source_rectangles") == 480
        and given.get("expanded_rectangles") == 3792
        and given.get("mass_exact") == text(CLAIM.mass * CRATE_SCALE)
        and (given.get("B"), given.get("D"), given.get("angle_count"))
        == (text(side), text(step), count)
        and summary.get("threshold") == "1"
    )


def crate_checks(record: dict[str, Any]) -> list[Check]:
    runs = record["runs"]
    axis_rows_ = [
        json.loads(line) for line in runs["crate-axis-A"]["stdout"].splitlines() if line
    ]
    net_rows = [
        json.loads(line) for line in runs["crate-net401-B"]["stdout"].splitlines() if line
    ]
    axis_row = next((row for row in axis_rows_ if "r" in row), {})
    axis_summary = next((row for row in axis_rows_ if row.get("kind")), {})
    rows = sorted((row for row in net_rows if "r" in row), key=lambda row: int(row["r"]))
    summary = next((row for row in net_rows if row.get("kind")), {})
    built = {
        str((row.get("build") or {}).get("source_sha256")) for row in (axis_summary, summary)
    }
    reviewed = REVIEWED_SOURCES.get(next(iter(built))) if len(built) == 1 else None
    commit = reviewed.commit if reviewed else "unreviewed"
    least, least_r = (
        min((row["min_certified_lower_bound"], int(row["r"])) for row in rows)
        if rows
        else (None, None)
    )
    return [
        Check(
            "crate: reviewed source for a declared net, the binary embeds it",
            reviewed is not None and reviewed.declared_nets,
            f"{', '.join(sorted(built))} ({commit})",
        ),
        Check(
            "crate: the axis at side A by the exact vertex sweep",
            runs["crate-axis-A"]["exit_code"] == 0
            and crate_premises(axis_summary, CLAIM.A, Fraction(83, 40000), 201)
            and axis_row.get("verdict") == "verified"
            and axis_row.get("method") == "axis-vertex-sweep"
            and axis_row.get("vertices") == EXPECT["crate_axis_vertices"]
            and axis_row.get("min_certified_lower_bound") == EXPECT["crate_axis_bound"],
            f"{axis_row.get('verdict')}, {axis_row.get('vertices')} vertices, least "
            f"{axis_row.get('min_certified_lower_bound')!r} at {axis_row.get('argmin')}",
        ),
        Check(
            "crate: the 401-direction necessary condition at side B",
            runs["crate-net401-B"]["exit_code"] == 0
            and crate_premises(summary, CLAIM.B, Fraction(83, 80000), 401)
            and [int(row["r"]) for row in rows] == list(range(401))
            and all(row["verdict"] == "verified" for row in rows)
            and summary.get("status") == "VERIFIED"
            and summary.get("refused_directions") == []
            and summary.get("nodes") == EXPECT["crate_net_nodes"]
            and (least, least_r) == (EXPECT["crate_net_bound"], EXPECT["crate_net_bound_r"]),
            f"{summary.get('status')}, {len(rows)} directions, {summary.get('nodes')} boxes, "
            f"least {least!r} at r = {least_r}",
        ),
    ]


def release_g_checks(record: dict[str, Any]) -> list[Check]:
    """Control G on the release's own ``scalar()``: the unchanged copy returns the
    receipts' scalar block, and the mutant is refused at the near-axis containment."""
    runs = record["runs"]
    unchanged, mutant = runs["G-release-unchanged"], runs["G-release-axis-side"]
    told = json.loads(unchanged["stdout"]) if unchanged["stdout"].strip() else {}
    refused = json.loads(mutant["stdout"]) if mutant["stdout"].strip() else {}
    return [
        Check(
            "control G-release-unchanged: exact.py's scalar block is the receipts'",
            unchanged["exit_code"] == 0 and told.get("scalar") == scalar_block(CLAIM),
            f"exit {unchanged['exit_code']}",
        ),
        Check(
            "control G-release-axis-side: exact.py refuses NEAR_AXIS_CONTAINMENT",
            mutant["exit_code"] == 4 and refused.get("refused") == "NEAR_AXIS_CONTAINMENT",
            f"exit {mutant['exit_code']}, {refused.get('refused')}",
        ),
    ]


def replay_report(folder: Path) -> dict[str, Any]:
    builds = retained_json(folder / "builds.json")
    axis = retained_json(folder / "axis-run.json")
    slabs = jsonl_rows(folder / "slabs.jsonl")
    controls = jsonl_rows(folder / "controls.jsonl")
    crate = retained_json(folder / "crate-runs.json")
    checks = (
        build_checks(builds)
        + axis_run_checks(axis)
        + slab_replay_checks(slabs)
        + control_checks(controls)
        + release_g_checks(retained_json(folder / "control-G-release.json"))
        + crate_checks(crate)
    )
    starts = [datetime.fromisoformat(row["started_utc"]) for row in slabs]
    ends = [
        datetime.fromisoformat(row["started_utc"]).timestamp() + row["wall_seconds"]
        for row in slabs
    ]
    return {
        "kind": "continuous-pose-replay-check/v1",
        "compiler": builds["compiler"],
        "binaries": {name: item["binary_sha256"] for name, item in builds["builds"].items()},
        "slab_cpu_seconds": round(sum(row["cpu_seconds"] for row in slabs), 1),
        "slab_wall_seconds_sum": round(sum(row["wall_seconds"] for row in slabs), 1),
        "slab_stage_wall_seconds": round(max(ends) - min(starts).timestamp()),
        "slab_first_start_utc": min(starts).isoformat(),
        "crate_binary_sha256": crate["binary_sha256"],
        "checks": [check.as_json() for check in checks],
        "status": "REPLAY_HOLDS" if all(c.held for c in checks) else "REPLAY_CHECK_FAILED",
    }


# --------------------------------------------------------------------------- command


def emit(report: dict[str, Any], output: Path | None) -> int:
    if output is not None:
        write_json(output, report)
    for item in report.get("checks", []):
        print(f"{'ok  ' if item['held'] else 'FAIL'} {item['name']}: {item['detail']}")
    for item in report.get("controls", []):
        mark = "refused " if item["refused"] else "ADMITTED"
        print(f"{mark} control {item['control']} ({item['change']}): failed {item['failed']}")
    print(report["status"])
    return 0 if report["status"] in {"FINITE_STEPS_HOLD", "REPLAY_HOLDS"} else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    commands = parser.add_subparsers(dest="command", required=True)
    derive = commands.add_parser("derive", help="write the kernel and crate inputs")
    derive.add_argument("--out", type=Path, required=True)
    check = commands.add_parser("check", help="the finite audit and its controls")
    check.add_argument("--output", type=Path)
    replay = commands.add_parser("run", help="build the kernels and run the replay")
    replay.add_argument("--out", type=Path, required=True)
    replay.add_argument("--workers", type=int, default=2)
    replay.add_argument("--stages", default=",".join(STAGES))
    replay.add_argument("--crate-binary", type=Path)
    judge = commands.add_parser("check-replay", help="judge the replay's receipts")
    judge.add_argument("--receipts", type=Path, default=RECEIPT_DIR)
    judge.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if args.command == "derive":
        density = load_density()
        args.out.mkdir(parents=True, exist_ok=True)
        files = {
            "certificate_input.txt": pose_input(density),
            "axis-input.txt": axis_input(axis_rows(density)),
            **{f"{name}.json": data for name, data in crate_inputs(density).items()},
        }
        for name, data in files.items():
            (args.out / name).write_bytes(data)
            print(f"{sha256(data)}  {name}")
        return 0
    if args.command == "run":
        stages = [s for s in args.stages.split(",") if s]
        if not set(stages) <= set(STAGES) or not 1 <= args.workers <= 8:
            parser.error(f"--stages from {','.join(STAGES)}; --workers from 1 to 8")
        crate = args.crate_binary.resolve() if args.crate_binary else None
        run_replay(args.out.resolve(), args.workers, stages, crate)
        return 0
    if args.command == "check":
        return emit(check_report(facts(load_density())), args.output)
    return emit(replay_report(args.receipts), args.output)


if __name__ == "__main__":
    sys.exit(main())
