"""Audit Guzhou0806's clipped-corner transfer, s(40) > 335427/50000, in exact rationals.

Issue jlevy/squares#485 claims ``s(40) > 335427/50000`` from wand125's ``rect_n40_L67``
density, which the 2026-10-01 rectangle packet retains, by a continuous-angle transfer
from a 401-direction nodal statement with a clipped-corner loss bound, and the weaker
full-core bound ``s(40) > 67000 sqrt(6400006889)/798988091``. The source is retained in
``resources/web/guzhou-n40-clipped-corner-2026-10-10/``; the argument and the replay
contract are the review
``docs/project/reviews/review-2026-10-10-guzhou-n40-clipped-corner-bound.md``.

This tool decides the finite steps again with code written here, which shares none with
the release's ``verifier/finite.py`` (not opened while it was written) and reads only the
retained density and the release's parameters and receipts as data:

- ``derive`` writes the 401-direction input the crate decides: the density's 480
  positive rows in file order as exact fractions, with the net in its ``certificate``
  metadata. Its SHA-256 must be the one both release receipts name as the input.
- ``check`` recomputes the density's mass, its D4 expansion and invariance, the exact
  essential supremum of the density (`peak`) and the release's rounded-up bound ``H``,
  the net's premises, the transfer's scalar chain (`chain`) and the full-core closed
  form; compares every value with the ``finite`` block, the parameters and the nodal
  premises of both release receipts; and runs controls E to H (`finite_controls`), each
  of which must be refused.
- ``run`` drives a build of the reviewed crate source: the nodal replay at every
  direction of the derived input and controls A to D (`CONTROLS`, inputs from
  `mutants`), each with its wall and CPU time, beside the binary's digest and the
  crate source it embeds, the control point chosen as the census chooses it
  (`tightest_centre`). Its scratch directory is under ``TMPDIR``.
- ``check-replay`` judges those receipts: every row verified and identical apart from
  timing to both release receipts, the even rows to the retained 201-direction census
  row, the premises to the finite audit's, and each control's refusal re-evaluated apart
  from the crate by `sqpack.rectangle_density`.

The nodal statement is decided by the crate, which is the code the release itself ran
(vendored byte for byte); only the finite steps are re-implemented here.

Two SHA-256 values are compared, each across the download boundary of issue 485:
`CANDIDATE_SHA256`, the density the release pins (``SOURCES.md``, and
``source_candidate_sha256`` in its receipts), against the copy retained on 2026-10-01,
which detects deriving the input from another density; and `DERIVED_SHA256`, the input
both release receipts name, against the bytes ``derive`` writes, which detects a
derived file that is not the measure the receipts decided. Nothing here reads Git
history (OR-18).

Usage, from ``packing/``, each after ``uv run --frozen --all-extras --group dev``::

    python -m devtools.audit_clipped_corner_transfer check [--output OUT.json]
    python -m devtools.audit_clipped_corner_transfer derive --out derived-401.json
    python -m devtools.audit_clipped_corner_transfer run --binary BIN --out DIR --threads 2
    python -m devtools.audit_clipped_corner_transfer check-replay [--output OUT.json]
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
import time
from collections import Counter
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools.check_sqverify_fast import crate_source_sha256
from devtools.retained_data import read_retained_bytes
from devtools.sqverify_fast_census import REVIEWED_SOURCES
from sqpack.rectangle_density import (
    RectangleDensityCandidate,
    coverage_at_point,
    load_candidate_bytes,
)

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
PACKET = WEB / "guzhou-n40-clipped-corner-2026-10-10"
CANDIDATE = (
    WEB / "wand125-rectangle-certificates-2026-10-01/wand125-rectangles/certificates"
    "/rect_n40_L67/certified_candidate.json"
)
PARAMETERS = PACKET / "source/certificate/parameters.json"
#: The release's two receipts: the producer's local run in the tree at the pin, and the
#: GitHub Actions run 38032128403 that the release ZIP carries instead (GN-3).
RECEIPTS = {
    "local": PACKET / "source/results",
    "ci": PACKET / "release-ci/results",
}
RECEIPT_DIR = PACKET / "receipts"
CENSUS_ROW = (
    REPO / "packing/benchmarks/measure-verifier/census/2026-10-01/rect_n40_L67.jsonl.gz"
)

CANDIDATE_SHA256 = "71011d0356dd179c6e7e6e02c9a064ff30f6f13844016ce3b97463bf7ef53dc0"
DERIVED_SHA256 = "49f696a4533ded9532b879bf69706da35bc03a49db79718573760adc08cd458e"

type Rect = tuple[Fraction, Fraction, Fraction, Fraction]
type PointMap = Callable[[Fraction, Fraction], tuple[Fraction, Fraction]]


def text(value: Fraction) -> str:
    """A rational as the release writes it: ``p/q``, or ``p`` when it is whole."""
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def rational(value: object) -> Fraction:
    """An exact rational from a JSON value read with ``parse_float=Fraction``."""
    if isinstance(value, bool):
        raise TypeError("a boolean is not a number")
    if isinstance(value, Fraction | int | str):
        return Fraction(value)
    raise TypeError(f"not an exact number: {value!r}")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# --------------------------------------------------------------------------- the claim


@dataclass(frozen=True)
class Transfer:
    """The claim's parameters, named as the release's ``parameters.json`` names them."""

    n: int = 40
    L: Fraction = Fraction(67, 10)
    B: Fraction = Fraction(9977, 10000)
    D: Fraction = Fraction(83, 80000)
    last: int = 400
    X: Fraction = Fraction(335427, 50000)
    h: Fraction = Fraction(514946944479, 10**15)
    tau: Fraction = Fraction(10001, 10000)
    mass: Fraction = Fraction(3999, 100)
    H: Fraction = Fraction(2818711359413, 10**9)
    charge: Fraction = Fraction(99979, 100000)

    def as_json(self) -> dict[str, object]:
        return {
            key: value if isinstance(value, int) else text(value)
            for key, value in self.__dict__.items()
        }


CLAIM = Transfer()
#: The full-core bound's closed form, s(40) > 67000 sqrt(6400006889) / 798988091, and the
#: decimal the release states below it.
CLOSED_FORM = (Fraction(67000, 798988091), 6400006889)
CLOSED_FORM_DECIMAL = Fraction("6.70848908")


def half_angle(t: Fraction) -> tuple[Fraction, Fraction]:
    """Cosine and sine of ``2 atan t``, exactly."""
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


@dataclass(frozen=True)
class Chain:
    """The transfer's scalar chain at one parameter set (review items 3, 4, 6 and 7)."""

    q: Fraction  # the parent side L / X
    reach0: Fraction  # B (cos d0 + sin d0) at d0 = 2 atan h, the first branch's extent
    b: Fraction  # tan(beta / 2), with beta = 2 atan D - 2 atan h
    e: Fraction  # how far a corner reaches past each side of the parent at beta
    area: Fraction  # A = e^2 / (2 cos beta sin beta), the clipped-corner bound
    chi: Fraction  # tau - H A, what every parent captures
    counting: Fraction  # n chi - M
    simple: Fraction  # n charge - M
    uncut: Fraction  # (L / gamma)^2, the full-core bound squared


def chain(t: Transfer) -> Chain:
    q = t.L / t.X
    c0, s0 = half_angle(t.h)
    b = (t.D - t.h) / (1 + t.D * t.h)
    cb, sb = half_angle(b)
    e = max(Fraction(0), t.B * (cb + sb) - q)
    area = e * e / (2 * cb * sb) if e else Fraction(0)
    chi = t.tau - t.H * area
    gamma_squared = t.B * t.B * (1 + t.D) ** 2 / (1 + t.D * t.D)
    return Chain(
        q=q,
        reach0=t.B * (c0 + s0),
        b=b,
        e=e,
        area=area,
        chi=chi,
        counting=t.n * chi - t.mass,
        simple=t.n * t.charge - t.mass,
        uncut=t.L * t.L / gamma_squared,
    )


# --------------------------------------------------------------------------- the density


def d4_maps(side: Fraction) -> tuple[PointMap, ...]:
    """The eight symmetries of ``[0, side]^2``, as maps on points."""
    return (
        lambda x, y: (x, y),
        lambda x, y: (side - x, y),
        lambda x, y: (x, side - y),
        lambda x, y: (side - x, side - y),
        lambda x, y: (y, x),
        lambda x, y: (side - y, x),
        lambda x, y: (y, side - x),
        lambda x, y: (side - y, side - x),
    )


def image(rect: Rect, f: PointMap) -> Rect:
    (a, b), (c, d) = f(rect[0], rect[1]), f(rect[2], rect[3])
    return (min(a, c), min(b, d), max(a, c), max(b, d))


def area(rect: Rect) -> Fraction:
    return (rect[2] - rect[0]) * (rect[3] - rect[1])


@dataclass(frozen=True)
class Density:
    """The retained candidate, read exactly: its positive rows in file order, expanded."""

    sha256: str
    side: Fraction
    core: Fraction
    n: int
    listed: int
    rows: tuple[tuple[Rect, Fraction], ...]
    terms: int
    merged: dict[Rect, Fraction]


def read_density(raw: bytes) -> Density:
    """Parse the candidate with every decimal exact and expand it through D4.

    Each positive row of weight ``w`` on rectangle ``R`` contributes density
    ``w / (8 |R|)`` on each of its eight images; images that coincide are merged.
    """
    data = json.loads(raw, parse_float=Fraction)
    side, core = rational(data["L"]), rational(data["B"])
    rects, weights = data["rectangles"], data["weights"]
    if len(rects) != len(weights):
        raise ValueError("rectangles and weights differ in length")
    rows: list[tuple[Rect, Fraction]] = []
    for coords, raw_weight in zip(rects, weights, strict=True):
        weight = rational(raw_weight)
        if weight < 0:
            raise ValueError(f"negative weight {weight}")
        if weight == 0:
            continue
        x1, y1, x2, y2 = (rational(v) for v in coords)
        if not (0 <= x1 < x2 <= side and 0 <= y1 < y2 <= side):
            raise ValueError(f"rectangle {coords} is not a proper rectangle in K")
        rows.append(((x1, y1, x2, y2), weight))
    maps = d4_maps(side)
    terms = [(image(rect, f), weight / (8 * area(rect))) for rect, weight in rows for f in maps]
    return Density(
        sha256=sha256(raw),
        side=side,
        core=core,
        n=int(data["n"]),
        listed=len(rects),
        rows=tuple(rows),
        terms=len(terms),
        merged=merge(terms),
    )


def merge(terms: Iterable[tuple[Rect, Fraction]]) -> dict[Rect, Fraction]:
    """Densities summed over coinciding rectangles."""
    merged: dict[Rect, Fraction] = {}
    for rect, value in terms:
        merged[rect] = merged.get(rect, Fraction(0)) + value
    return merged


def invariant(density: Density) -> bool:
    """Whether the merged density is its own image under each of the eight maps."""
    return all(
        merge((image(rect, f), value) for rect, value in density.merged.items())
        == density.merged
        for f in d4_maps(density.side)
    )


def stack_peak(items: Sequence[tuple[int, int, int, int, int]]) -> tuple[int, tuple[int, int]]:
    """The greatest sum of densities over an open cell of the arrangement, and its corner.

    Every open cell lies in the half-open stack ``{x1 <= x < x2, y1 <= y < y2}`` of the
    lower-left corner ``(max x1, max y1)`` of its members, so the maximum over cells is
    attained in a vertical slab that starts at some ``x1``: a slab that starts where
    rectangles only end holds a subset of the slab before it, and densities are
    nonnegative. Within a slab the open intervals between consecutive ``y`` events are
    swept. Integer coordinates and densities; the empty arrangement gives ``(0, (0, 0))``.
    """
    by_start = sorted(items)
    starts = sorted({item[0] for item in items})
    best, corner = 0, (0, 0)
    active: list[tuple[int, int, int, int, int]] = []
    taken = 0
    for xa in starts:
        while taken < len(by_start) and by_start[taken][0] <= xa:
            active.append(by_start[taken])
            taken += 1
        active = [item for item in active if item[2] > xa]
        events: Counter[int] = Counter()
        for _, y1, _, y2, value in active:
            events[y1] += value
            events[y2] -= value
        ys = sorted(events)
        running = 0
        for y in ys[:-1]:
            running += events[y]
            if running > best:
                best, corner = running, (xa, y)
    return best, corner


def peak(
    density: Density, *, round_up_to: int | None = None
) -> tuple[Fraction, tuple[Fraction, Fraction]]:
    """The essential supremum of the density, exactly, or with every merged density
    rounded up to a multiple of ``1/round_up_to`` (the release's way of writing ``H``)."""
    scale = math.lcm(*(v.denominator for rect in density.merged for v in rect))
    values = list(density.merged.values())
    if round_up_to is None:
        unit = math.lcm(*(v.denominator for v in values))
        weights = [v.numerator * (unit // v.denominator) for v in values]
    else:
        unit = round_up_to
        weights = [-((-v.numerator * unit) // v.denominator) for v in values]
    items = [
        (int(x1 * scale), int(y1 * scale), int(x2 * scale), int(y2 * scale), weight)
        for (x1, y1, x2, y2), weight in zip(density.merged, weights, strict=True)
    ]
    best, (cx, cy) = stack_peak(items)
    return Fraction(best, unit), (Fraction(cx, scale), Fraction(cy, scale))


@dataclass(frozen=True)
class Facts:
    """What the density gives, computed once: no control changes it."""

    sha256: str
    side: Fraction
    core: Fraction
    n: int
    listed: int
    positive: int
    mass: Fraction
    terms: int
    distinct: int
    invariant: bool
    integral: Fraction
    peak: Fraction
    peak_at: tuple[Fraction, Fraction]
    rounded_peak: Fraction
    derived_sha256: str


def facts(density: Density) -> Facts:
    exact, where = peak(density)
    rounded, _ = peak(density, round_up_to=10**9)
    return Facts(
        sha256=density.sha256,
        side=density.side,
        core=density.core,
        n=density.n,
        listed=density.listed,
        positive=len(density.rows),
        mass=sum((w for _, w in density.rows), Fraction(0)),
        terms=density.terms,
        distinct=len(density.merged),
        invariant=invariant(density),
        integral=sum((area(r) * v for r, v in density.merged.items()), Fraction(0)),
        peak=exact,
        peak_at=where,
        rounded_peak=rounded,
        derived_sha256=sha256(derived_input(density, CLAIM)),
    )


def derived_input(density: Density, t: Transfer) -> bytes:
    """The 401-direction input: the positive rows with the net in the metadata, written
    as the review's replay contract states (sorted keys, no spaces, a final newline)."""
    value = {
        "n": density.n,
        "L": text(density.side),
        "B": text(density.core),
        "rectangles": [[text(v) for v in rect] for rect, _ in density.rows],
        "weights": [text(w) for _, w in density.rows],
        "coverage_lower_bound_exact": text(t.tau),
        "certificate": {
            "L": text(t.L),
            "B": text(t.B),
            "D": text(t.D),
            "angle_count": t.last + 1,
        },
    }
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def load_density() -> Density:
    return read_density(read_retained_bytes(CANDIDATE))


# --------------------------------------------------------------------------- the audit


@dataclass(frozen=True)
class Check:
    name: str
    held: bool
    detail: str

    def as_json(self) -> dict[str, object]:
        return {"name": self.name, "held": self.held, "detail": self.detail}


def audit(t: Transfer, f: Facts) -> list[Check]:
    """Every finite premise of the claim at parameters ``t``, on the density's facts."""
    c = chain(t)
    tip = t.last * t.D
    gaps = all(0 < t.D / (1 + j * (j + 1) * t.D * t.D) <= t.D for j in range(t.last))
    closed = CLOSED_FORM[0] ** 2 * CLOSED_FORM[1]
    c0, s0 = half_angle(t.h)
    cb, sb = half_angle(c.b)
    return [
        Check("density: the release's candidate", f.sha256 == CANDIDATE_SHA256, f.sha256),
        Check(
            "density: n, L and B are the claim's",
            (f.n, f.side, f.core) == (t.n, t.L, t.B),
            f"n {f.n}, L {text(f.side)}, B {text(f.core)}",
        ),
        Check(
            "density: 480 positive rows",
            f.positive == 480,
            f"{f.positive} of {f.listed} listed",
        ),
        Check("density: mass M", f.mass == t.mass, text(f.mass)),
        Check("density: M below n", f.mass < t.n, f"n - M = {text(t.n - f.mass)}"),
        Check(
            "density: D4 expansion",
            (f.terms, f.distinct) == (3840, 3792),
            f"{f.terms} terms, {f.distinct} distinct rectangles",
        ),
        Check("density: D4-invariant", f.invariant, "under each of the eight maps"),
        Check("density: integral of g is M", f.integral == t.mass, text(f.integral)),
        Check(
            "density: ess sup g <= H",
            f.peak <= t.H,
            f"ess sup {float(f.peak):.15g}, H - ess sup {float(t.H - f.peak):.6g}, "
            f"at ({float(f.peak_at[0]):.15g}, {float(f.peak_at[1]):.15g})",
        ),
        Check(
            "density: H is the peak with densities rounded up to 1e-9",
            f.rounded_peak == t.H,
            text(f.rounded_peak),
        ),
        Check(
            "derived input: the receipts' input",
            f.derived_sha256 == DERIVED_SHA256,
            f.derived_sha256,
        ),
        Check(
            "net: positive step, 2 to 65536 directions",
            t.D > 0 and 2 <= t.last + 1 <= 2**16,
            f"D {text(t.D)}, {t.last + 1} directions",
        ),
        Check("net: B (1 + D) < 1", t.B * (1 + t.D) < 1, text(t.B * (1 + t.D))),
        Check(
            "net: the last node passes pi/4",
            tip * tip + 2 * tip - 1 > 0,
            f"t_last {text(tip)}, t^2 + 2t - 1 = {text(tip * tip + 2 * tip - 1)}",
        ),
        Check("net: last tangent at most 1/2", tip <= Fraction(1, 2), text(tip)),
        Check("net: half-gap tangents at most D", gaps, f"j = 0..{t.last - 1}"),
        Check("transfer: X > L and q >= B", t.X > t.L and c.q >= t.B, f"q = {text(c.q)}"),
        Check(
            "transfer: 0 < h < D, delta0 <= pi/4",
            0 < t.h < t.D and 2 * t.h <= 1 - t.h * t.h,
            text(t.h),
        ),
        Check(
            "transfer: first-branch containment",
            c.reach0 <= c.q and c0 > 0 and s0 > 0,
            f"q - B (cos d0 + sin d0) = {float(c.q - c.reach0):.6g}",
        ),
        Check(
            "transfer: 0 < b, beta <= pi/4",
            c.b > 0 and 2 * c.b <= 1 - c.b * c.b and cb > 0 and sb > 0,
            text(c.b),
        ),
        Check("transfer: chi >= charge", c.chi >= t.charge, f"chi {float(c.chi):.12g}"),
        Check("transfer: n chi - M > 0", c.counting > 0, f"{float(c.counting):.10g}"),
        Check("transfer: n charge - M > 0", c.simple > 0, text(c.simple)),
        Check("full core: n tau - M > 0", t.n * t.tau - t.mass > 0, text(t.n * t.tau - t.mass)),
        Check(
            "full core: (L/gamma)^2 is the closed form",
            c.uncut == closed,
            text(c.uncut),
        ),
        Check(
            "full core: above 6.70848908",
            c.uncut > CLOSED_FORM_DECIMAL**2,
            f"L/gamma ~ {math.sqrt(c.uncut):.12f}",
        ),
    ]


def finite_values(t: Transfer) -> dict[str, Fraction]:
    """The receipt's ``finite`` block, as this tool computes it."""
    c = chain(t)
    return {
        "X": t.X,
        "parent_side": c.q,
        "h": t.h,
        "b": c.b,
        "density_upper": t.H,
        "cap_area_upper": c.area,
        "charge_lower": c.chi,
        "simple_charge": t.charge,
        "counting_margin": c.counting,
        "simple_counting_margin": c.simple,
        "uncut_side_squared": c.uncut,
    }


def premises(t: Transfer, f: Facts) -> dict[str, object]:
    """The nodal premises the crate must report on the derived input."""
    return {
        "B": text(t.B),
        "D": text(t.D),
        "L": text(t.L),
        "angle_count": t.last + 1,
        "centre_domain": "tokoharu",
        "expanded_points": 0,
        "expanded_rectangles": f.distinct,
        "expanded_segments": 0,
        "format": "T",
        "input_sha256": f.derived_sha256,
        "mass_below_n": text(t.n - f.mass),
        "mass_exact": text(f.mass),
        "n": t.n,
        "net_last_tangent": text(t.last * t.D),
        "net_origin": "metadata",
        "shrink_bound": text(t.B * (1 + t.D)),
        "source_rectangles": f.positive,
    }


def read_receipt(folder: Path) -> dict[str, Any]:
    value: dict[str, Any] = json.loads(
        (folder / "verification.json").read_text(encoding="utf-8")
    )
    return value


def receipt_checks(name: str, receipt: dict[str, Any], t: Transfer, f: Facts) -> list[Check]:
    """One release receipt against this tool's values: parameters, ``finite`` block,
    digests and nodal premises."""
    checks = [
        Check(
            f"{name} receipt: parameters",
            receipt.get("parameters") == t.as_json(),
            "the claim's",
        ),
    ]
    block = receipt.get("finite") or {}
    for key, value in finite_values(t).items():
        given = block.get(key)
        checks.append(
            Check(
                f"{name} receipt: finite.{key}",
                given is not None and Fraction(str(given)) == value,
                text(value),
            )
        )
    checks.append(
        Check(
            f"{name} receipt: finite block has no other field",
            set(block) == set(finite_values(t)),
            ", ".join(sorted(set(block) ^ set(finite_values(t)))) or "none",
        )
    )
    summary = receipt.get("node_summary") or {}
    checks += [
        Check(
            f"{name} receipt: candidate and input digests",
            receipt.get("source_candidate_sha256") == f.sha256
            and receipt.get("derived_candidate_sha256") == f.derived_sha256,
            f"{receipt.get('source_candidate_sha256')}, "
            f"{receipt.get('derived_candidate_sha256')}",
        ),
        Check(
            f"{name} receipt: net and threshold",
            receipt.get("continuous_domains") == t.last + 1
            and receipt.get("angle_step") == text(t.D)
            and receipt.get("threshold") == text(t.tau),
            f"{receipt.get('continuous_domains')} at {receipt.get('angle_step')}",
        ),
        Check(
            f"{name} receipt: nodal premises",
            summary.get("premises") == premises(t, f),
            "the derived input's",
        ),
        Check(
            f"{name} receipt: nodal summary",
            summary.get("status") == "VERIFIED"
            and summary.get("directions") == t.last + 1
            and summary.get("refused_directions") == []
            and summary.get("fault_injected_at_box") is None,
            f"{summary.get('status')}, {summary.get('directions')} directions",
        ),
    ]
    return checks


# --------------------------------------------------------------------------- controls E-H


def containment(t: Transfer, h: Fraction) -> bool:
    c, s = half_angle(h)
    return t.B * (c + s) <= t.L / t.X


def best_counting_margin(
    t: Transfer, *, steps: int = 160
) -> tuple[Fraction, Fraction, Fraction]:
    """An exact upper bound on ``n chi - M`` over every admissible ``h`` at ``t.X``.

    The admissible ``h`` are those where the first branch's containment holds, an
    interval ``[0, h_max]`` because ``B (cos d + sin d)`` increases on ``[0, pi/4]``; and
    ``chi`` is nondecreasing in ``h``, since ``b`` decreases in ``h`` and the clipped
    area is nondecreasing in ``beta`` (review item 4). Bisection in exact rationals finds
    ``h_lo`` admissible and ``h_hi`` not, so ``n chi(h_hi) - M`` bounds every admissible
    margin from above. Returns ``h_lo``, ``h_hi`` and that bound.
    """
    lo, hi = Fraction(0), t.D
    if not (containment(t, lo) and not containment(t, hi)):
        raise ValueError("the containment does not change between h = 0 and h = D")
    for _ in range(steps):
        middle = (lo + hi) / 2
        lo, hi = (middle, hi) if containment(t, middle) else (lo, middle)
    return lo, hi, chain(replace(t, h=hi)).counting


@dataclass(frozen=True)
class FiniteControl:
    name: str
    change: str
    claim: Transfer
    #: The checks of `audit` that must fail on it.
    expect: tuple[str, ...]


FINITE_CONTROLS = (
    FiniteControl(
        "E",
        "H replaced by H - 2/10^9",
        replace(CLAIM, H=CLAIM.H - Fraction(2, 10**9)),
        ("density: ess sup g <= H",),
    ),
    FiniteControl(
        "F",
        "X = 335428/50000, the next side on the release's grid",
        replace(CLAIM, X=Fraction(335428, 50000)),
        ("transfer: first-branch containment",),
    ),
    FiniteControl(
        "G",
        "h + 1/10^15",
        replace(CLAIM, h=CLAIM.h + Fraction(1, 10**15)),
        ("transfer: first-branch containment",),
    ),
    FiniteControl(
        "H",
        "the 201 net, D = 83/40000 with last index 200, the same h",
        replace(CLAIM, D=Fraction(83, 40000), last=200),
        ("transfer: chi >= charge", "transfer: n chi - M > 0"),
    ),
)


def finite_controls(f: Facts) -> list[dict[str, object]]:
    """Controls E to H: each mutated claim must fail the checks it names. F must also
    fail at every admissible ``h`` (`best_counting_margin`), and H must give ``chi < 0``."""
    out: list[dict[str, object]] = []
    for control in FINITE_CONTROLS:
        failed = [check.name for check in audit(control.claim, f) if not check.held]
        refused = all(name in failed for name in control.expect)
        extra: dict[str, object] = {}
        if control.name == "F":
            lo, hi, bound = best_counting_margin(control.claim)
            extra = {
                "h_admissible": text(lo),
                "h_inadmissible": text(hi),
                "margin_upper_bound": text(bound),
                "margin_upper_bound_decimal": f"{float(bound):.6g}",
            }
            refused = refused and bound < 0
        if control.name == "H":
            chi = chain(control.claim).chi
            extra = {"chi": text(chi), "chi_decimal": f"{float(chi):.6g}"}
            refused = refused and chi < 0
        out.append(
            {
                "control": control.name,
                "change": control.change,
                "expect_failed": list(control.expect),
                "failed": failed,
                "refused": refused,
                **extra,
            }
        )
    return out


def check_report(f: Facts) -> dict[str, Any]:
    """The finite audit: the claim, both receipts, the retained parameters, controls."""
    checks = audit(CLAIM, f)
    parameters = json.loads(PARAMETERS.read_text(encoding="utf-8"))
    checks.append(
        Check(
            "retained parameters.json is the claim", parameters == CLAIM.as_json(), "all keys"
        )
    )
    for name, folder in RECEIPTS.items():
        checks += receipt_checks(name, read_receipt(folder), CLAIM, f)
    controls = finite_controls(f)
    c = chain(CLAIM)
    held = all(check.held for check in checks) and all(item["refused"] for item in controls)
    return {
        "kind": "clipped-corner-transfer-audit/v1",
        "claim": "s(40) > 335427/50000; s(40) > 67000 sqrt(6400006889)/798988091",
        "candidate": str(CANDIDATE.relative_to(REPO)),
        "values": {
            **{key: text(value) for key, value in finite_values(CLAIM).items()},
            "ess_sup": text(f.peak),
            "ess_sup_decimal": f"{float(f.peak):.15g}",
            "H_minus_ess_sup_decimal": f"{float(CLAIM.H - f.peak):.6g}",
            "containment_slack_decimal": f"{float(c.q - c.reach0):.6g}",
            "chi_decimal": f"{float(c.chi):.12g}",
            "counting_margin_decimal": f"{float(c.counting):.10g}",
            "clipped_area_decimal": f"{float(c.area):.6g}",
            "full_core_decimal": f"{math.sqrt(c.uncut):.12f}",
        },
        "checks": [check.as_json() for check in checks],
        "controls": controls,
        "status": "FINITE_STEPS_HOLD" if held else "FINITE_AUDIT_FAILED",
    }


# --------------------------------------------------------------------------- the replay


@dataclass(frozen=True)
class Control:
    """A crate control on the derived input (the replay contract's A to D)."""

    name: str
    label: str
    directions: str
    expect_exit: int


CONTROLS = (
    Control("A", "scaled-99-100", "73,220", 1),
    Control("B", "near-threshold", "220", 1),
    Control("C", "no-metadata", "0", 0),
    Control("D", "short-net", "0", 2),
)
CONTROL_SCALE = Fraction(99, 100)
#: The census's near-threshold rule: the mutant's capture at the control centre at most
#: this fraction of the threshold below it.
NEAR_THRESHOLD = Fraction(1, 10**6)
REPLAY = "replay-401"
SELECTION = "control-selection.json"
RUNS = "runs.json"
#: What the contract states for the complete run, from the release's receipts.
EXPECT = {
    "nodes": 32970910,
    "least_bound": 1.000100000471634,
    "least_bound_r": 73,
    "axis_vertices": 4879681,
    "axis_events": 2209,
    "axis_bound": 1.0012141064171602,
    "max_depth": 30,
}
TIMING = frozenset({"cpu_seconds", "seconds"})


def direction_angle(t: Transfer, index: int) -> tuple[Fraction, Fraction]:
    """Cosine and sine of net direction ``index``, half-angle tangent ``index D``."""
    return half_angle(index * t.D)


def scaled_input(raw: bytes, factor: Fraction) -> bytes:
    value = json.loads(raw)
    value["weights"] = [text(Fraction(w) * factor) for w in value["weights"]]
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def evaluator(raw: bytes) -> RectangleDensityCandidate:
    """The derived input's measure read by `sqpack.rectangle_density`, written before
    the crate. Its loader admits only the standard net in metadata, since its own
    verifier runs on that net; `coverage_at_point` takes the angle from the caller, so
    the net block is dropped here and every angle is given from the 401 net."""
    value = json.loads(raw)
    value.pop("certificate", None)
    data = json.dumps(value).encode()
    return load_candidate_bytes(data, n=CLAIM.n, expected_side=CLAIM.L, target=CLAIM.tau)


def read_rows(data: bytes) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    lines = [json.loads(line) for line in data.decode().splitlines() if line.strip()]
    rows = sorted((line for line in lines if "r" in line), key=lambda row: int(row["r"]))
    summary = next(
        (line for line in lines if line.get("kind") == "sqverify-fast-summary/v1"), {}
    )
    return rows, summary


def tightest_centre(
    rows: Iterable[dict[str, Any]], candidate: RectangleDensityCandidate
) -> dict[str, Any]:
    """The census's control point: of the least-bound leaf centres at the oblique
    directions, the one of least exact capture, evaluated apart from the crate."""
    weighed: list[tuple[Fraction, int, float, float]] = []
    for row in rows:
        box = row.get("least_bound_box")
        if int(row["r"]) < 1 or not box:
            continue
        cosine, sine = direction_angle(CLAIM, int(row["r"]))
        x, y = float(box["x"]), float(box["y"])
        capture = coverage_at_point(candidate, Fraction(x), Fraction(y), cosine, sine)
        weighed.append((capture, int(row["r"]), x, y))
    capture, index, x, y = min(weighed, key=lambda item: (item[0], item[1]))
    return {"r": index, "centre": [x, y], "capture": text(capture), "weighed": len(weighed)}


def near_factor(capture: Fraction) -> Fraction:
    """Rounded down to 1e-15, so the mutant's capture at the centre is at most the
    threshold less `NEAR_THRESHOLD` of it (the census's rule)."""
    return Fraction(int(CLAIM.tau * (1 - NEAR_THRESHOLD) / capture * 10**15), 10**15)


def mutants(derived: bytes, selection: dict[str, Any]) -> dict[str, bytes]:
    """The inputs of controls A to D."""
    value = json.loads(derived)
    no_metadata = dict(value)
    del no_metadata["certificate"]
    short = json.loads(derived)
    short["certificate"]["angle_count"] = 201

    def dump(item: dict[str, Any]) -> bytes:
        return (json.dumps(item, sort_keys=True, separators=(",", ":")) + "\n").encode()

    return {
        "A": scaled_input(derived, CONTROL_SCALE),
        "B": scaled_input(derived, near_factor(Fraction(selection["capture"]))),
        "C": dump(no_metadata),
        "D": dump(short),
    }


def spawn(argv: Sequence[str], stdout: Path, stderr: Path) -> dict[str, Any]:
    """Run one command with its output in files; wall, CPU (wait4) and load around it."""
    before = os.getloadavg()
    started = datetime.now(UTC).isoformat(timespec="seconds")
    start = time.monotonic()
    with stdout.open("wb") as out, stderr.open("wb") as err:
        pid = os.posix_spawn(
            argv[0],
            list(argv),
            os.environ,
            file_actions=[
                (os.POSIX_SPAWN_DUP2, out.fileno(), 1),
                (os.POSIX_SPAWN_DUP2, err.fileno(), 2),
            ],
        )
        _, status, usage = os.wait4(pid, 0)
    return {
        "exit_code": os.waitstatus_to_exitcode(status),
        "started_utc": started,
        "wall_seconds": round(time.monotonic() - start, 3),
        "cpu_seconds": round(usage.ru_utime + usage.ru_stime, 3),
        "loadavg_before": [round(v, 2) for v in before],
        "loadavg_after": [round(v, 2) for v in os.getloadavg()],
    }


def command(binary_name: str, candidate: str, directions: str, *extra: str) -> list[str]:
    return [
        binary_name,
        "--candidate",
        candidate,
        "--n",
        str(CLAIM.n),
        "--side",
        text(CLAIM.L),
        "--directions",
        directions,
        "--threshold",
        text(CLAIM.tau),
        *extra,
    ]


def receipts_match(folder: Path, rows: list[dict[str, Any]], summary: dict[str, Any]) -> bool:
    """Whether ``--receipts`` wrote each stdout row, with the input's digest, and the
    summary."""
    for row in rows:
        written = json.loads(
            (folder / f"r{int(row['r']):03d}.json").read_text(encoding="utf-8")
        )
        if written != {**row, "certificate_sha256": DERIVED_SHA256}:
            return False
    files = sorted(path.name for path in folder.iterdir())
    written_summary = json.loads((folder / "summary.json").read_text(encoding="utf-8"))
    return written_summary == summary and len(files) == len(rows) + 1


def pack(rows: list[dict[str, Any]], summary: dict[str, Any]) -> bytes:
    body = "".join(json.dumps(line, sort_keys=True) + "\n" for line in [*rows, summary] if line)
    return gzip.compress(body.encode(), compresslevel=9, mtime=0)


def run_replay(binary: Path, out: Path, threads: int) -> dict[str, Any]:
    """The contract's nodal run and controls A to D, receipts into ``out``.

    Refuses unless the tree's crate source is one a soundness review accepted for a
    declared net and the binary embeds that source, as the census route does.
    """
    source = crate_source_sha256()
    reviewed = REVIEWED_SOURCES.get(source)
    if reviewed is None or not reviewed.declared_nets:
        raise SystemExit(f"{source} is not reviewed source for a declared net")
    density = load_density()
    derived = derived_input(density, CLAIM)
    if sha256(derived) != DERIVED_SHA256:
        raise SystemExit("the derived input is not the one the release receipts decided")
    out.mkdir(parents=True, exist_ok=True)
    binary_sha = sha256(binary.read_bytes())
    runs: dict[str, Any] = {}
    home = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="clipped-corner-replay-") as name:
        scratch = Path(name)
        # The live output stays outside the tree until the run ends (the census's lesson
        # from rect_n69_L8575), and the commands name their inputs as the contract does.
        os.chdir(scratch)
        try:
            runs = run_all(binary, scratch, out, derived, threads)
        finally:
            os.chdir(home)
    record = {
        "kind": "clipped-corner-replay-runs/v1",
        "binary_sha256": binary_sha,
        "crate_source_sha256": source,
        "reviewed_source": {"commit": reviewed.commit, "review": reviewed.review},
        "threads": threads,
        "runs": runs,
    }
    (out / RUNS).write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    return record


def run_all(
    binary: Path, scratch: Path, out: Path, derived: bytes, threads: int
) -> dict[str, Any]:
    """The nodal run, the control point and its probe, and controls A to D, each run in
    ``scratch`` and its receipt written to ``out``."""
    (scratch / "derived-401.json").write_bytes(derived)
    argv = command(
        str(binary), "derived-401.json", "all",
        "--threads", str(threads), "--confirm", "--receipts", "receipts",
    )  # fmt: skip
    record = spawn(argv, scratch / "stdout.jsonl", scratch / "stderr.log")
    rows, summary = read_rows((scratch / "stdout.jsonl").read_bytes())
    record["receipts_dir_matches_stdout"] = receipts_match(scratch / "receipts", rows, summary)
    record["stderr"] = (scratch / "stderr.log").read_text(encoding="utf-8")
    (out / f"{REPLAY}.jsonl.gz").write_bytes(pack(rows, summary))
    runs: dict[str, Any] = {REPLAY: {"argv": ["sqverify-fast", *argv[1:]], **record}}

    selection = tightest_centre(rows, evaluator(derived))
    r, (x, y) = selection["r"], selection["centre"]
    probe = subprocess.run(
        [str(binary), "--candidate", "derived-401.json", "--n", str(CLAIM.n),
         "--probe", f"{r},{x!r},{y!r}"],
        capture_output=True, text=True, check=True,
    )  # fmt: skip
    selection["crate_probe"] = json.loads(probe.stdout)["exact_coverage"]
    selection["factor"] = text(near_factor(Fraction(selection["capture"])))
    (out / SELECTION).write_text(json.dumps(selection, indent=1) + "\n", encoding="utf-8")

    inputs = mutants(derived, selection)
    for control in CONTROLS:
        stem = f"control-{control.name}-{control.label}"
        (scratch / f"{stem}.json").write_bytes(inputs[control.name])
        argv = command(
            str(binary), f"{stem}.json", control.directions,
            "--threads", str(threads), "--confirm",
        )  # fmt: skip
        record = spawn(argv, scratch / f"{stem}.jsonl", scratch / f"{stem}.err")
        rows, summary = read_rows((scratch / f"{stem}.jsonl").read_bytes())
        record["stderr"] = (scratch / f"{stem}.err").read_text(encoding="utf-8")
        record["input_sha256"] = sha256(inputs[control.name])
        (out / f"{stem}.jsonl.gz").write_bytes(pack(rows, summary))
        runs[stem] = {"argv": ["sqverify-fast", *argv[1:]], **record}
    return runs


# --------------------------------------------------------------------------- judging it


def same_apart_from_timing(
    a: dict[str, Any], b: dict[str, Any], *, ignore: frozenset[str] = frozenset()
) -> bool:
    skip = TIMING | ignore
    return {k: v for k, v in a.items() if k not in skip} == {
        k: v for k, v in b.items() if k not in skip
    }


def jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line) for line in read_retained_bytes(path).decode().splitlines() if line
    ]


def nodal_checks(rows: list[dict[str, Any]], summary: dict[str, Any], f: Facts) -> list[Check]:
    """The complete run against the contract, the release receipts and the census row."""
    bounds = [(row["min_certified_lower_bound"], int(row["r"])) for row in rows]
    least, least_r = min(bounds)
    axis = rows[0] if rows else {}
    checks = [
        Check(
            "replay: every direction verified",
            [int(row["r"]) for row in rows] == list(range(CLAIM.last + 1))
            and all(row["verdict"] == "verified" for row in rows)
            and all(row["threshold"] == text(CLAIM.tau) for row in rows),
            f"{sum(row['verdict'] == 'verified' for row in rows)} of {len(rows)}",
        ),
        Check(
            "replay: summary",
            summary.get("status") == "VERIFIED"
            and summary.get("directions") == CLAIM.last + 1
            and summary.get("refused_directions") == []
            and summary.get("fault_injected_at_box") is None
            and summary.get("threshold") == text(CLAIM.tau),
            str(summary.get("status")),
        ),
        Check(
            "replay: premises",
            summary.get("premises") == premises(CLAIM, f),
            "the finite audit's",
        ),
        Check(
            "replay: boxes", summary.get("nodes") == EXPECT["nodes"], str(summary.get("nodes"))
        ),
        Check(
            "replay: least certified bound",
            (least, least_r) == (EXPECT["least_bound"], EXPECT["least_bound_r"]),
            f"{least!r} at r = {least_r}",
        ),
        Check(
            "replay: the axis sweep",
            axis.get("method") == "axis-vertex-sweep"
            and axis.get("vertices") == EXPECT["axis_vertices"]
            and axis.get("x_events") == axis.get("y_events") == EXPECT["axis_events"]
            and axis.get("min_certified_lower_bound") == EXPECT["axis_bound"],
            f"{axis.get('vertices')} vertices",
        ),
        Check(
            "replay: oblique directions by branch and bound",
            all(row.get("method") == "interval-branch-and-bound" for row in rows[1:])
            and max(int(row.get("max_depth", 0)) for row in rows) == EXPECT["max_depth"],
            f"greatest depth {max(int(row.get('max_depth', 0)) for row in rows)}",
        ),
    ]
    build = summary.get("build") or {}
    reviewed = REVIEWED_SOURCES.get(str(build.get("source_sha256")))
    checks.append(
        Check(
            "replay: reviewed source for a declared net",
            reviewed is not None and reviewed.declared_nets,
            f"{build.get('source_sha256')} ({reviewed.commit if reviewed else 'unreviewed'})",
        )
    )
    for name, folder in RECEIPTS.items():
        theirs = {int(row["r"]): row for row in jsonl(folder / "nodes.jsonl")}
        same = sum(same_apart_from_timing(row, theirs.get(int(row["r"]), {})) for row in rows)
        checks.append(
            Check(
                f"replay: rows equal the {name} receipt's apart from timing",
                same == len(rows) == len(theirs),
                f"{same} of {len(theirs)}",
            )
        )
    # The standard net's direction k is the 401 net's direction 2k: the same angle, and
    # on the same source the same boxes, so the rows agree apart from timing and index.
    census, _ = read_rows(read_retained_bytes(CENSUS_ROW))
    even = {int(row["r"]) // 2: row for row in rows if int(row["r"]) % 2 == 0}
    same = sum(
        same_apart_from_timing(row, even.get(int(row["r"]), {}), ignore=frozenset({"r"}))
        for row in census
    )
    checks.append(
        Check(
            "replay: even rows equal the retained census row's",
            same == len(census) == len(even),
            f"{same} of {len(census)}",
        )
    )
    return checks


def domain(index: int) -> tuple[Fraction, Fraction]:
    """Tokoharu's centre domain at net node ``index`` on either axis, ``[a, L - a]`` with
    ``a = B (cos theta + sin theta) / 2``, computed here apart from the crate."""
    cosine, sine = direction_angle(CLAIM, index)
    low = CLAIM.B * (cosine + sine) / 2
    return low, CLAIM.L - low


def refusal_checks(
    name: str, rows: list[dict[str, Any]], factor: Fraction, original: RectangleDensityCandidate
) -> list[Check]:
    """Each refused row: a counterexample candidate whose witness lies in the domain and
    where the mutant's exact capture, evaluated by `sqpack.rectangle_density`, equals the
    crate's and is below the threshold."""
    checks: list[Check] = []
    for row in rows:
        index = int(row["r"])
        witness = row.get("witness") or {}
        pose = witness.get("exact_pose")
        if row.get("verdict") != "counterexample-candidate" or not pose:
            checks.append(
                Check(
                    f"control {name}: r = {index} refused",
                    held=False,
                    detail=str(row.get("verdict")),
                )
            )
            continue
        x, y = Fraction(float(pose[0])), Fraction(float(pose[1]))
        low, high = domain(index)
        cosine, sine = direction_angle(CLAIM, index)
        capture = factor * coverage_at_point(original, x, y, cosine, sine)
        crate = witness.get("exact_coverage")
        checks.append(
            Check(
                f"control {name}: r = {index} refused at an exact witness below tau",
                witness.get("exact_below_threshold") is True
                and low <= x <= high
                and low <= y <= high
                and crate is not None
                and Fraction(crate) == capture
                and capture < CLAIM.tau,
                f"capture {float(capture):.12g} at ({float(x)!r}, {float(y)!r})",
            )
        )
    return checks


def control_checks(folder: Path, f: Facts, *, rank: bool) -> tuple[list[Check], dict[str, Any]]:
    """Controls A to D from their receipts, and the control point they were built at."""
    derived = derived_input(load_density(), CLAIM)
    original = evaluator(derived)
    selection: dict[str, Any] = json.loads((folder / SELECTION).read_text(encoding="utf-8"))
    r, (x, y) = int(selection["r"]), selection["centre"]
    cosine, sine = direction_angle(CLAIM, r)
    capture = coverage_at_point(original, Fraction(float(x)), Fraction(float(y)), cosine, sine)
    checks = [
        Check(
            "control point: capture recorded, evaluated again",
            capture == Fraction(selection["capture"]) == Fraction(selection["crate_probe"]),
            f"r = {r}, capture {float(capture):.12g}",
        ),
        Check(
            "control point: the census rule's factor",
            Fraction(selection["factor"]) == near_factor(capture),
            str(selection["factor"]),
        ),
    ]
    if rank:
        rows, _ = read_rows(read_retained_bytes(folder / f"{REPLAY}.jsonl"))
        again = tightest_centre(rows, original)
        checks.append(
            Check(
                "control point: least exact capture over the oblique leaf centres",
                (again["r"], again["centre"], again["capture"])
                == (selection["r"], selection["centre"], selection["capture"]),
                f"{again['weighed']} centres weighed",
            )
        )
    runs = json.loads((folder / RUNS).read_text(encoding="utf-8"))["runs"]
    factors = {"A": CONTROL_SCALE, "B": Fraction(selection["factor"])}
    for control in CONTROLS:
        stem = f"control-{control.name}-{control.label}"
        rows, summary = read_rows(read_retained_bytes(folder / f"{stem}.jsonl"))
        record = runs[stem]
        exit_ok = record["exit_code"] == control.expect_exit
        if control.name in factors:
            factor = factors[control.name]
            refused = [int(index) for index in control.directions.split(",")]
            checks.append(
                Check(
                    f"control {control.name}: refused, on the 401 net",
                    exit_ok
                    and summary.get("status") == "REFUSED"
                    and summary.get("refused_directions") == refused
                    and (summary.get("premises") or {}).get("net_origin") == "metadata"
                    and (summary.get("premises") or {}).get("angle_count") == CLAIM.last + 1
                    and (summary.get("premises") or {}).get("mass_exact")
                    == text(f.mass * factor),
                    f"exit {record['exit_code']}, {summary.get('status')} "
                    f"at {summary.get('refused_directions')}",
                )
            )
            checks += refusal_checks(control.name, rows, factor, original)
        elif control.name == "C":
            given = summary.get("premises") or {}
            checks.append(
                Check(
                    "control C: admitted on the standard net, another claim",
                    exit_ok
                    and given.get("net_origin") == "standard"
                    and given.get("angle_count") == 201
                    and given.get("D") == "83/40000"
                    and all(row.get("verdict") == "verified" for row in rows),
                    f"exit {record['exit_code']}, "
                    f"{given.get('angle_count')} directions at {given.get('D')}",
                )
            )
        else:
            checks.append(
                Check(
                    "control D: refused at admission",
                    exit_ok
                    and not rows
                    and "the net does not reach past pi/4" in record["stderr"],
                    record["stderr"].strip(),
                )
            )
    return checks, selection


def replay_report(folder: Path, f: Facts, *, rank: bool) -> dict[str, Any]:
    rows, summary = read_rows(read_retained_bytes(folder / f"{REPLAY}.jsonl"))
    checks = nodal_checks(rows, summary, f)
    record = json.loads((folder / RUNS).read_text(encoding="utf-8"))
    nodal = record["runs"][REPLAY]
    checks.append(
        Check(
            "replay: exit 0, --receipts wrote the rows",
            nodal["exit_code"] == 0 and nodal["receipts_dir_matches_stdout"] is True,
            f"exit {nodal['exit_code']}",
        )
    )
    controls, selection = control_checks(folder, f, rank=rank)
    checks += controls
    return {
        "kind": "clipped-corner-replay-check/v1",
        "binary_sha256": record["binary_sha256"],
        "build": summary.get("build"),
        "wall_seconds": nodal["wall_seconds"],
        "cpu_seconds": nodal["cpu_seconds"],
        "control_point": {k: selection[k] for k in ("r", "centre", "weighed", "factor")},
        "checks": [check.as_json() for check in checks],
        "status": "REPLAY_HOLDS"
        if all(check.held for check in checks)
        else "REPLAY_CHECK_FAILED",
    }


# --------------------------------------------------------------------------- command


def emit(report: dict[str, Any], output: Path | None) -> int:
    text_out = json.dumps(report, indent=1) + "\n"
    if output is not None:
        output.write_text(text_out, encoding="utf-8")
    for item in report.get("checks", []):
        mark = "ok  " if item["held"] else "FAIL"
        print(f"{mark} {item['name']}: {item['detail']}")
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
    check = commands.add_parser("check", help="the finite audit and controls E to H")
    check.add_argument("--output", type=Path)
    derive = commands.add_parser("derive", help="write the derived 401-direction input")
    derive.add_argument("--out", type=Path, required=True)
    replay = commands.add_parser("run", help="the nodal replay and controls A to D")
    replay.add_argument("--binary", type=Path, required=True)
    replay.add_argument("--out", type=Path, required=True)
    replay.add_argument("--threads", type=int, default=2)
    judge = commands.add_parser("check-replay", help="judge the replay's receipts")
    judge.add_argument("--receipts", type=Path, default=RECEIPT_DIR)
    judge.add_argument("--rank", action="store_true", help="rank all 400 leaf centres again")
    judge.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if args.command == "derive":
        data = derived_input(load_density(), CLAIM)
        args.out.write_bytes(data)
        print(sha256(data))
        return 0 if sha256(data) == DERIVED_SHA256 else 1
    if args.command == "run":
        record = run_replay(args.binary.resolve(), args.out.resolve(), args.threads)
        for name, item in record["runs"].items():
            print(f"{name}: exit {item['exit_code']}, {item['wall_seconds']} s wall")
        return 0
    f = facts(load_density())
    if args.command == "check":
        return emit(check_report(f), args.output)
    return emit(replay_report(args.receipts, f, rank=args.rank), args.output)


if __name__ == "__main__":
    sys.exit(main())
