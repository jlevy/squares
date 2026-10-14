"""Source-bound figures for Paper II, the review of Overbeck's s(11) > 31/8 (T-037).

Twelve static SVGs, II.1 to II.12 in reading order (plan
`plan-2026-10-05-n11-explainer-series.md` §6.2), and the facts their captions state.
Nothing here is another verifier: every drawing reads retained, hash-pinned data, checks
what it shows against it in exact arithmetic, and only then rounds to pixels.

The certificate is read with `sqpack.fractional.parent_core.load_kleddamag_parent_core`
and never through the archived `exact_mixed.py`, which imports numba and is not an
execution cache. The raw JSON is read beside it only for the orbit structure the loader
flattens, and the two readings are checked to agree charge for charge.

Inputs, each pinned by its SHA-256 and listed in `FIGURE_INPUTS` for the renderer's
`RENDER_INPUTS`:

- Overbeck's `global-certificate.json` (T-037) and its portable Python replay
  `evidence/portable/python.json`, in the archived release;
- T-026's retained certificate on the 1,440-step net;
- T-059's replay journal (all 12,028 exact row minima with replayed exact witnesses),
  pinned by its inflated bytes as its summary pins it;
- this repository's native row journal (session 153);
- the register, of which only the ladder's rung records are pinned
  (`paper_figures.LADDER_DIGEST`).

A changed input is refused before anything is drawn. Every caption number comes from
`caption_facts()`; a caption names a fact and never types it.

II.3, the roadmap, is the one schematic; its numbers are facts like any other. II.4 and
II.6 place illustrative cores by hand: the centres below are display choices, and every
capture, disjointness and legality claim made of them is checked exactly at render.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import math
from collections import Counter
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import pairwise
from math import comb
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from devtools import paper_figures as pf
from sqpack.fractional.certificate import d4_images
from sqpack.fractional.parent_core import (
    ParentCoreCertificate,
    ParentCoreRow,
    load_kleddamag_parent_core,
)

PACKING = Path(__file__).resolve().parents[1]
REPOSITORY = PACKING.parent
KLEDDAMAG = PACKING / "resources/web/external-square-certificates-2026-09-22/kleddamag-11"
CERTIFICATE = KLEDDAMAG / "global-certificate.json"
PYTHON_EVIDENCE = KLEDDAMAG / "evidence/portable/python.json"
T026_CERTIFICATE = PACKING / "cases/n11_threshold_certificate/certificate-191-50-net1440.json"
T059_JOURNAL = (
    PACKING / "resources/web/wand125-tools-2026-09-29/receipts/n11-bound-full.jsonl.gz"
)
NATIVE_ROWS = PACKING / "campaign/agent-sessions/session-153-native-full.rows.jsonl"
RESULTS = pf.RESULTS

CERTIFICATE_SHA = "57e9927da5c13f42dd8bcbf8f08c84363635fece626657ee63a810c61cd44458"
PYTHON_EVIDENCE_SHA = "68b6f360ecbc377c15d2ad95aad328b211716329a771c51f15e45bf2de127bc0"
T026_SHA = "dc2da20c75d952690c93d67fb4b3eb8552e879585902fde98eedc9b3179ed3d0"
#: Over the inflated journal, as T-059's summary records it (`journal_sha256`).
T059_SHA = "b7f3ebd4da4269d4ea74fc372f7d034a3855dc096de93a528800214b518ef7fc"
NATIVE_ROWS_SHA = "7058e4f0a8ff17b29683c97022273f88a764b1e7187e041ddb0f6ef910538fa2"

#: Repository-relative paths of every data file the figures read.
FIGURE_INPUTS: tuple[str, ...] = tuple(
    path.relative_to(REPOSITORY).as_posix()
    for path in (
        CERTIFICATE,
        PYTHON_EVIDENCE,
        T026_CERTIFICATE,
        T059_JOURNAL,
        NATIVE_ROWS,
        RESULTS,
    )
)

#: Plan figures II.1 to II.12, in reading order.
FIGURE_KEYS: tuple[str, ...] = (
    "CHANGES_SVG",
    "LADDER_SVG",
    "ROADMAP_SVG",
    "CHARGE_SVG",
    "BUDGET_SVG",
    "FAMILIES_SVG",
    "CORE_SVG",
    "CATALOGUE_SVG",
    "ENVELOPE_SVG",
    "SIGNED_SVG",
    "FIELD_SVG",
    "MINIMA_SVG",
)

#: The weight scale of every charge: one unit is 10⁻⁹.
UNITS = 10**9
N = 11
WIDTH = 360
#: Display choices, each checked against the data where it is used.
CHARGE_ORBIT = 72  # the largest weight in the certificate, a 3-of-5 charge
TRIPLE_ORBIT = 206  # the largest 2-of-3 charge
PAIR_ORBIT = 130  # the largest 2-of-5 charge
TIGHT_ROW = 11962  # the row of least minimum
TIGHT_PAIR = (8844, 8845)  # the two rows of the second-least minimum
#: II.4's two cores, on one row's core: the first holds three of orbit 72's sites, the
#: second, disjoint from it, two others. Found by a grid search, rounded, and checked.
CHARGE_ROW = 6600
CHARGE_CORES = (
    (Fraction(730, 1000), Fraction(2038, 1000)),
    (Fraction(1113, 1000), Fraction(1081, 1000)),
)
#: II.6(c)'s two disjoint cores, each holding two of orbit 130's sites.
PAIR_ROW = 2850
PAIR_CORES = (
    (Fraction(694, 1000), Fraction(1632, 1000)),
    (Fraction(1875, 1000), Fraction(2014, 1000)),
)
#: II.7 turns each core by this many times its true mismatch, and shrinks it to fit:
#: at true scale core and parent differ by less than a pixel.
CORE_EXAGGERATION = 2000
#: II.11's raster, in cells per side of the row's centre domain.
FIELD_GRID = 96
#: The upper bounds of the field raster's bands, as charges; the lowest band starts at
#: the row's minimum and the highest runs to its maximum.
FIELD_LEVELS = tuple(Fraction(value) for value in ("1.01", "1.02", "1.05", "1.1", "1.2", "1.4"))
SUM_FILL = "#bfe0dc"
FIELD_RAMP = ("#12385f", "#1f5a8f", "#2f78b7", "#5a9bd0", "#8fbde3", "#c3dcf0", "#eef5fb")

Point = tuple[Fraction, Fraction]
DASH = "\N{EN DASH}"
MINUS = "\N{MINUS SIGN}"


# Inputs -------------------------------------------------------------------------------


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _pinned(path: Path, expected: str, *, inflate: bool = False) -> bytes:
    data = path.read_bytes()
    if inflate:
        data = gzip.decompress(data)
    if _sha256(data) != expected:
        raise ValueError(f"changed figure input: {path}")
    return data


@dataclass(frozen=True, slots=True)
class Charge:
    """One physical k-of-m charge: its orbit, threshold, weight and member sites."""

    orbit: int
    threshold: int
    weight: Fraction
    members: tuple[int, ...]

    @property
    def family(self) -> str:
        return f"{self.threshold}-of-{len(self.members)}"


@dataclass(frozen=True)
class Sources:
    certificate: ParentCoreCertificate
    sites: tuple[Point, ...]
    site_orbit: tuple[int, ...]
    point_weight: tuple[Fraction, ...]
    point_orbit_weights: tuple[Fraction, ...]
    charges: tuple[Charge, ...]
    charge_orbits: int
    minima: tuple[int, ...]
    histogram: dict[int, int]
    python: dict[str, Any]
    t026: dict[str, Any]
    witness: Point
    witness_minimum: int
    native_lower: tuple[int, ...]
    ladder: str


_SOURCES: dict[tuple[str, ...], Sources] = {}
_RENDERED: dict[tuple[str, ...], dict[str, str]] = {}
_FACTS: dict[tuple[str, ...], dict[str, str]] = {}


def _pins() -> tuple[str, ...]:
    return (
        str(CERTIFICATE),
        CERTIFICATE_SHA,
        str(PYTHON_EVIDENCE),
        PYTHON_EVIDENCE_SHA,
        str(T026_CERTIFICATE),
        T026_SHA,
        str(T059_JOURNAL),
        T059_SHA,
        str(NATIVE_ROWS),
        NATIVE_ROWS_SHA,
        str(RESULTS),
        pf.LADDER_DIGEST,
    )


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _sources() -> Sources:
    """Every input, checked against its pin each call; parsed once per set of pins."""
    raw_bytes = _pinned(CERTIFICATE, CERTIFICATE_SHA)
    python_bytes = _pinned(PYTHON_EVIDENCE, PYTHON_EVIDENCE_SHA)
    t026_bytes = _pinned(T026_CERTIFICATE, T026_SHA)
    t059_bytes = _pinned(T059_JOURNAL, T059_SHA, inflate=True)
    native_bytes = _pinned(NATIVE_ROWS, NATIVE_ROWS_SHA)
    ladder = pf.bound_ladder("T-037", path=RESULTS)
    key = _pins()
    if key in _SOURCES:
        return _SOURCES[key]

    certificate = load_kleddamag_parent_core(CERTIFICATE, expected_sha256=CERTIFICATE_SHA)
    raw: dict[str, Any] = json.loads(raw_bytes)
    side = certificate.outer_side
    scale = raw["coordinate_denominator"]
    sites: list[Point] = []
    site_orbit: list[int] = []
    point_weight: list[Fraction] = []
    orbit_weights: list[Fraction] = []
    for index, (x, y, weight) in enumerate(raw["point_orbits"]):
        orbit = sorted(set(d4_images(Fraction(x, scale), Fraction(y, scale), side)))
        sites.extend(orbit)
        site_orbit.extend([index] * len(orbit))
        point_weight.extend([Fraction(weight, UNITS)] * len(orbit))
        orbit_weights.append(Fraction(weight, UNITS))
    weighted = [(sites[i], point_weight[i]) for i in range(len(sites)) if point_weight[i]]
    _require(
        weighted == [((atom.x, atom.y), atom.weight) for atom in certificate.atoms],
        "the certificate's point charges differ from its loader's",
    )
    charges = [
        Charge(orbit, row["threshold"], Fraction(row["weight"], UNITS), tuple(members))
        for orbit, row in enumerate(raw["charge_orbits"])
        for members in row["sets"]
        if row["weight"]
    ]
    _require(
        [(tuple(sites[i] for i in c.members), c.threshold, c.weight) for c in charges]
        == [(atom.points, atom.threshold, atom.weight) for atom in certificate.threshold_atoms],
        "the certificate's k-of-m charges differ from its loader's",
    )

    python: dict[str, Any] = json.loads(python_bytes)
    _require(python["status"] == "PASS_FULL_EXACT_PYTHON_REPLAY", "python replay not passed")
    _require(python["certificate_sha256"] == CERTIFICATE_SHA, "python replay of another file")
    _require(python["budget_units"] == certificate.budget * UNITS, "replay budget differs")
    _require(
        python["minimum_units"] == certificate.minimum_charge * UNITS, "replay minimum differs"
    )
    rows = python["rows"]
    _require([row["row"] for row in rows] == list(range(len(certificate.rows))), "replay rows")
    minima = tuple(int(row["minimum_units"]) for row in rows)
    histogram = {int(value): int(times) for value, times in python["histogram"].items()}
    _require(Counter(minima) == histogram, "replay histogram differs from its rows")

    t026: dict[str, Any] = json.loads(t026_bytes)
    _require(t026["outer_side"] == "191/50" and t026["variant"] == "threshold", "T-026 file")

    lines = t059_bytes.decode().splitlines()
    run = json.loads(lines[0])
    _require(run["kind"] == "run", "T-059 journal lacks its run record")
    _require(
        run["binding"]["certificate_sha256"] == CERTIFICATE_SHA, "T-059 binds another file"
    )
    _require(run["binding"]["reference_sha256"] == PYTHON_EVIDENCE_SHA, "T-059 reference")
    replayed = {record["row"]: record for record in map(json.loads, lines[1:])}
    _require(sorted(replayed) == list(range(len(minima))), "T-059 journal is incomplete")
    _require(
        all(
            replayed[row]["minimum"] == minima[row] and replayed[row]["witness_replayed"]
            for row in replayed
        ),
        "T-059 minima differ from the source's",
    )
    tight = replayed[TIGHT_ROW]
    witness = (Fraction(tight["witness"][0]), Fraction(tight["witness"][1]))

    native_lines = native_bytes.decode().splitlines()
    header = json.loads(native_lines[0])
    _require(
        header["provenance"]["certificate_sha256"] == CERTIFICATE_SHA, "native journal binding"
    )
    native = sorted((json.loads(line) for line in native_lines[1:]), key=lambda r: r["index"])
    _require([r["index"] for r in native] == list(range(len(minima))), "native rows incomplete")
    _require(
        all(
            r["status"] == "certified" and not r["stalled"] and not r["budget_exhausted"]
            for r in native
        ),
        "a native row is not certified",
    )

    sources = Sources(
        certificate=certificate,
        sites=tuple(sites),
        site_orbit=tuple(site_orbit),
        point_weight=tuple(point_weight),
        point_orbit_weights=tuple(orbit_weights),
        charges=tuple(charges),
        charge_orbits=len(raw["charge_orbits"]),
        minima=minima,
        histogram=histogram,
        python=python,
        t026=t026,
        witness=witness,
        witness_minimum=int(tight["minimum"]),
        native_lower=tuple(int(r["lower"]) for r in native),
        ladder=ladder,
    )
    _SOURCES.clear()
    _SOURCES[key] = sources
    return sources


# Exact geometry -------------------------------------------------------------------------


def _captured(src: Sources, row: ParentCoreRow, centre: Point) -> frozenset[int]:
    """The sites the closed core of `row` about `centre` contains, decided exactly."""
    cosine, sine = row.rotation
    half = row.core_side / 2
    fc, fs, fh = float(cosine), float(sine), float(half)
    cx, cy = centre
    fx, fy = float(cx), float(cy)
    found: set[int] = set()
    for index, (x, y) in enumerate(src.sites):
        dx, dy = float(x) - fx, float(y) - fy
        reach = max(abs(fc * dx + fs * dy), abs(-fs * dx + fc * dy))
        if reach > fh + 1e-6:
            continue
        if reach < fh - 1e-6:
            found.add(index)
            continue
        ex, ey = x - cx, y - cy
        if abs(cosine * ex + sine * ey) <= half and abs(-sine * ex + cosine * ey) <= half:
            found.add(index)
    return frozenset(found)


def _charge(src: Sources, captured: frozenset[int]) -> Fraction:
    """The charge C(Q) of a core that captures exactly `captured`."""
    total = sum((src.point_weight[i] for i in captured), Fraction(0))
    for charge in src.charges:
        if sum(member in captured for member in charge.members) >= charge.threshold:
            total += charge.weight
    return total


def _legal(src: Sources, row: ParentCoreRow, centre: Point) -> bool:
    """Whether `centre` lies strictly inside the row's centre domain (the envelope)."""
    radius = row.centre_margin(src.certificate.parent_side)
    side = src.certificate.outer_side
    return all(radius < value < side - radius for value in centre)


def _disjoint(row: ParentCoreRow, first: Point, second: Point) -> bool:
    """Two cores of one row, the same closed square turned alike, are disjoint exactly
    when their centres differ by more than the side along one of the core's axes."""
    cosine, sine = row.rotation
    dx, dy = second[0] - first[0], second[1] - first[1]
    along = abs(cosine * dx + sine * dy)
    across = abs(-sine * dx + cosine * dy)
    return along > row.core_side or across > row.core_side


def _orbit(src: Sources, orbit: int) -> Charge:
    """The first physical copy of a charge orbit, as the source lists it."""
    return next(charge for charge in src.charges if charge.orbit == orbit)


def _degrees(half_tangent: Fraction) -> float:
    return math.degrees(2 * math.atan(float(half_tangent)))


def _printed_degrees(half_tangent: Fraction, places: int) -> str:
    """The parent angle at `half_tangent`, in degrees, rounded for print."""
    return _rounded_degrees(_degrees(half_tangent), places)


def _rounded_degrees(degrees: float, places: int) -> str:
    """An angle in degrees, rounded for print. An angle with a rational half-tangent is
    transcendental, so no exact rational prints it; it is refused instead when a float
    could round it either way."""
    value = degrees * 10**places
    if abs(value - math.floor(value) - 0.5) < 1e-6:
        raise ValueError("an angle sits on a rounding boundary")
    return f"{round(value) / 10**places:.{places}f}°"


def _units(value: Fraction) -> int:
    scaled = value * UNITS
    _require(scaled.denominator == 1, f"{value} is not on the weight scale")
    return scaled.numerator


def _families(src: Sources) -> dict[str, tuple[int, int, Fraction]]:
    """Per family: orbits, physical charges, and total budget. Points first."""
    point_orbits = sum(1 for weight in src.point_orbit_weights if weight)
    point_sites = sum(1 for weight in src.point_weight if weight)
    result: dict[str, tuple[int, int, Fraction]] = {
        "point": (point_orbits, point_sites, sum(src.point_weight, Fraction(0)))
    }
    for family in ("2-of-3", "2-of-5", "3-of-5"):
        members = [c for c in src.charges if c.family == family]
        budget = sum((c.weight * (len(c.members) // c.threshold) for c in members), Fraction(0))
        result[family] = (len({c.orbit for c in members}), len(members), budget)
    _require(
        sum(budget for _, _, budget in result.values()) == src.certificate.budget,
        "family budgets do not sum to M",
    )
    return result


def _site_roles(src: Sources) -> tuple[int, int, int]:
    """Sites carrying point weight only, both point weight and a charge, a charge only."""
    in_charge = {member for charge in src.charges for member in charge.members}
    weighted = {i for i, weight in enumerate(src.point_weight) if weight}
    _require(in_charge | weighted == set(range(len(src.sites))), "an unused site")
    return len(weighted - in_charge), len(weighted & in_charge), len(in_charge - weighted)


def _abs_expansion(threshold: int, size: int) -> int:
    """Σ_j C(m, j) C(j-1, k-1): the absolute coefficient sum of a k-of-m charge's
    signed rectangle expansion."""
    return sum(comb(size, j) * comb(j - 1, threshold - 1) for j in range(threshold, size + 1))


def _coefficient(threshold: int, j: int) -> int:
    """The signed coefficient of a j-subset in the expansion of [m ≥ k]."""
    return (-1) ** (j - threshold) * comb(j - 1, threshold - 1)


def _point_bands(src: Sources) -> tuple[int, Fraction, Fraction]:
    """Point-weighted orbits within 0.005 of the four lines x, y ∈ {A, L₀-A}, and the
    share of point weight within 0.005 and within 0.05."""
    side, parent = src.certificate.outer_side, src.certificate.parent_side
    lines = (parent, side - parent)
    total = sum(src.point_weight, Fraction(0))
    near_orbits: set[int] = set()
    near = wide = Fraction(0)
    for index, (x, y) in enumerate(src.sites):
        weight = src.point_weight[index]
        if not weight:
            continue
        distance = min(abs(value - mark) for value in (x, y) for mark in lines)
        if distance <= Fraction(5, 1000):
            near_orbits.add(src.site_orbit[index])
            near += weight
        if distance <= Fraction(5, 100):
            wide += weight
    return len(near_orbits), near / total, wide / total


# Caption facts --------------------------------------------------------------------------


def _coordinates(point: Point, places: int = 4) -> str:
    return f"({pf.decimal(point[0], places)}, {pf.decimal(point[1], places)})"


def _facts(src: Sources) -> dict[str, str]:
    cert = src.certificate
    gamma, budget = cert.minimum_charge, cert.budget
    families = _families(src)
    point_only, shared, charge_only = _site_roles(src)
    near_orbits, near_share, wide_share = _point_bands(src)
    charge = _orbit(src, CHARGE_ORBIT)
    triple = _orbit(src, TRIPLE_ORBIT)
    pair = _orbit(src, PAIR_ORBIT)
    centre = (cert.outer_side / 2, cert.outer_side / 2)
    triple_distance = min(
        math.dist((float(src.sites[i][0]), float(src.sites[i][1])), (float(centre[0]),) * 2)
        for i in triple.members
    )
    sides = [row.core_side for row in cert.rows]
    tight = cert.rows[TIGHT_ROW]
    pair_rows = [cert.rows[i] for i in TIGHT_PAIR]
    radius = tight.centre_margin(cert.parent_side)
    t026_point = Fraction(src.t026["point_mass"]) / Fraction(src.t026["total_budget"])
    top = max(src.histogram)
    native_below = sum(1 for value in src.native_lower if value < UNITS)
    native_equal = sum(
        1
        for value, minimum in zip(src.native_lower, src.minima, strict=True)
        if value == minimum
    )
    largest_point = max(range(len(src.sites)), key=lambda i: (src.point_weight[i], -i))
    end = cert.rows[-1].right
    t060 = pf.ladder_records(RESULTS)["T-060"]["claim"].removeprefix("= ")
    gap = Fraction(t060.rstrip("…")) - cert.outer_side / cert.parent_side
    facts = {
        # The whole certificate.
        "CERT_GAMMA": pf.exact_decimal(gamma),
        "CERT_M": pf.exact_decimal(budget),
        "CERT_ELEVEN_GAMMA": pf.exact_decimal(N * gamma),
        "CERT_SURPLUS_UNITS": pf.count(_units(N * gamma - budget)),
        "CERT_ROWS": pf.count(len(cert.rows)),
        "CERT_SITES": pf.count(len(src.sites)),
        "CERT_POINT_SITES": pf.count(point_only + shared),
        "CERT_ORBITS": pf.count(len(src.point_orbit_weights)),
        "CERT_CHARGE_ORBITS": pf.count(src.charge_orbits),
        "CERT_FEATURES": pf.count(len(src.charges)),
        "CERT_A": str(cert.parent_side),
        "CERT_L0": str(cert.outer_side),
        "CERT_BOUND": str(cert.outer_side / cert.parent_side),
        # II.1
        "CHANGES_T026_POINTS": pf.count(len(src.t026["atoms"])),
        "CHANGES_T026_TRIPLES": pf.count(len(src.t026["threshold_atoms"])),
        "CHANGES_T026_POINT_SHARE": pf.percent(t026_point),
        "CHANGES_T037_POINT_SHARE": pf.percent(families["point"][2] / budget),
        "CHANGES_T026_B": str(src.t026["square_side"]),
        "CHANGES_T026_NET": pf.count(int(src.t026["direction_steps"])),
        # II.2
        "LADDER_GAP": pf.decimal(gap, 7),
        # II.4
        "CHARGE_ORBIT": str(CHARGE_ORBIT),
        "CHARGE_WEIGHT": pf.exact_decimal(charge.weight),
        "CHARGE_SITES": ", ".join(_coordinates(src.sites[i]) for i in charge.members),
        "CHARGE_ROW": str(CHARGE_ROW),
        # II.5
        "BUDGET_POINTS": pf.exact_decimal(families["point"][2]),
        "BUDGET_TWO_OF_THREE": pf.exact_decimal(families["2-of-3"][2]),
        "BUDGET_TWO_OF_FIVE": pf.exact_decimal(families["2-of-5"][2]),
        "BUDGET_THREE_OF_FIVE": pf.exact_decimal(families["3-of-5"][2]),
        "BUDGET_M": pf.exact_decimal(budget),
        "BUDGET_SURPLUS": pf.count(_units(N * gamma - budget)),
        "BUDGET_RATIO": pf.decimal(budget / gamma, 5),
        # II.6
        "FAMILIES_POINT_ORBITS": pf.count(families["point"][0]),
        "FAMILIES_POINT_ONLY": pf.count(point_only),
        "FAMILIES_SHARED": pf.count(shared),
        "FAMILIES_CHARGE_ONLY": pf.count(charge_only),
        "FAMILIES_IN_CHARGE": pf.count(shared + charge_only),
        "FAMILIES_NEAR_ORBITS": pf.count(near_orbits),
        "FAMILIES_NEAR_SHARE": pf.percent(near_share),
        "FAMILIES_WIDE_SHARE": pf.percent(wide_share),
        "FAMILIES_POINT_MAX": pf.exact_decimal(src.point_weight[largest_point]),
        "FAMILIES_POINT_MAX_SITE": _coordinates(src.sites[largest_point]),
        "FAMILIES_TABLE": _family_table(families),
        "FAMILIES_TRIPLE_ORBIT": str(TRIPLE_ORBIT),
        "FAMILIES_TRIPLE_WEIGHT": pf.exact_decimal(triple.weight),
        "FAMILIES_TRIPLE_CENTRE": f"{triple_distance:.3f}",
        "FAMILIES_PAIR_ORBIT": str(PAIR_ORBIT),
        "FAMILIES_PAIR_WEIGHT": pf.exact_decimal(pair.weight),
        # II.7
        "CORE_EXAGGERATION": pf.count(CORE_EXAGGERATION),
        # II.8
        "CATALOGUE_ROWS": pf.count(len(cert.rows)),
        "CATALOGUE_END": str(end),
        "CATALOGUE_B_MIN": pf.decimal(min(sides), 5),
        "CATALOGUE_B_MAX": pf.decimal(max(sides), 5),
        "CATALOGUE_TIGHT_ROW": str(TIGHT_ROW),
        "CATALOGUE_TIGHT_ANGLES": (
            f"{_printed_degrees(tight.left, 2)}{DASH}{_printed_degrees(tight.right, 2)}"
        ),
        "CATALOGUE_TIGHT_MIN": pf.exact_decimal(Fraction(src.minima[TIGHT_ROW], UNITS)),
        "CATALOGUE_PAIR_ROWS": f"{TIGHT_PAIR[0]}{DASH}{TIGHT_PAIR[1]}",
        "CATALOGUE_PAIR_ANGLES": (
            f"{_printed_degrees(pair_rows[0].left, 2)}{DASH}"
            f"{_printed_degrees(pair_rows[1].right, 2)}"
        ),
        "CATALOGUE_PAIR_MIN": pf.exact_decimal(Fraction(src.minima[TIGHT_PAIR[0]], UNITS)),
        # II.9
        "ENVELOPE_RHO": pf.decimal(radius, 6),
        "ENVELOPE_HALF": pf.decimal(cert.outer_side / 2 - radius, 6),
        # II.10
        "SIGNED_ORBIT": str(TRIPLE_ORBIT),
        "SIGNED_ABS_SUMS": ", ".join(
            str(_abs_expansion(k, m)) for k, m in ((2, 3), (2, 5), (3, 5))
        ),
        "SIGNED_EXPANSION_WEIGHT": pf.count(
            _units(sum(src.point_weight, Fraction(0)))
            + sum(
                _units(c.weight) * _abs_expansion(c.threshold, len(c.members))
                for c in src.charges
            )
        ),
        # II.11
        "FIELD_ROW": str(TIGHT_ROW),
        "FIELD_MIN": pf.exact_decimal(Fraction(src.witness_minimum, UNITS)),
        "FIELD_WITNESS": _coordinates(src.witness, 5),
        "FIELD_GRID": str(FIELD_GRID),
        # II.12
        "MINIMA_VALUES": pf.count(len(src.histogram)),
        "MINIMA_TOP": pf.exact_decimal(Fraction(top, UNITS)),
        "MINIMA_TOP_ROWS": pf.count(src.histogram[top]),
        "MINIMA_NATIVE_BELOW_ONE": pf.count(native_below),
        "MINIMA_NATIVE_EQUAL": pf.count(native_equal),
        "MINIMA_NATIVE_MIN": pf.exact_decimal(Fraction(min(src.native_lower), UNITS)),
    }
    _require(min(src.native_lower) >= _units(gamma), "a native lower bound is below Γ")
    _require(N * gamma > budget, "no counting surplus")
    _require(end * end + 2 * end > 1, "the catalogue stops short of 45°")
    return facts


def _family_table(families: dict[str, tuple[int, int, Fraction]]) -> str:
    """Family, orbits, physical charges, budget per charge, family budget (Markdown)."""
    rows = [
        "| Family | Orbits | Charges | Budget per charge | Family budget |",
        "| --- | ---: | ---: | --- | ---: |",
    ]
    for family, (orbits, members, budget) in families.items():
        if family == "point":
            per = "w"
            name = "point"
        else:
            k, m = (int(part) for part in family.split("-of-"))
            multiple = m // k
            per = "w" if multiple == 1 else f"{multiple}w"
            name = family
        rows.append(
            f"| {name} | {pf.count(orbits)} | {pf.count(members)} | {per} | "
            f"{pf.exact_decimal(budget)} |"
        )
    return "\n".join(rows)


def _degree_ticks(x_of: Callable[[int], float], y: float) -> list[str]:
    """Angle labels 0°, 15°, 30° and 45° under an axis of parent angle."""
    return [
        pf.text(x_of(degree), y, f"{degree}°", note=True, anchor="middle")
        for degree in (0, 15, 30, 45)
    ]


def _box_corners(
    box: tuple[Fraction, Fraction, Fraction, Fraction],
) -> list[tuple[Fraction, Fraction]]:
    x1, y1, x2, y2 = box
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]


# II.1 What changed --------------------------------------------------------------------


def _share_bar(y: float, label: str, shares: Sequence[tuple[str, Fraction]]) -> str:
    left, span = 78.0, 270.0
    parts = [pf.text(14, y + 14, label)]
    x = left
    for family, share in shares:
        width = span * float(share)
        parts.append(
            pf.rect(
                x,
                y,
                max(width - 2, 0.5),
                20,
                fill=pf.FAMILY_INKS[family],
                attributes=f'data-family="{family}" data-share="{share}"',
            )
        )
        x += width
    return "".join(parts)


def _changes_svg(src: Sources, facts: dict[str, str]) -> str:
    cert = src.certificate
    families = _families(src)
    t026_budget = Fraction(src.t026["total_budget"])
    t026_point = Fraction(src.t026["point_mass"]) / t026_budget
    t026_shares = [("point", t026_point), ("2-of-3", 1 - t026_point)]
    t037_shares = [(name, budget / cert.budget) for name, (_, _, budget) in families.items()]
    parts = [
        pf.text(14, 22, "Share of the budget"),
        _share_bar(36, "T-026", t026_shares),
        pf.text(78, 74, f"points {facts['CHANGES_T026_POINT_SHARE']}", note=True),
        _share_bar(88, "T-037", t037_shares),
        pf.text(78, 126, f"points {facts['CHANGES_T037_POINT_SHARE']}", note=True),
    ]
    legend_x = 14.0
    for family in pf.FAMILY_INKS:
        parts.append(pf.rect(legend_x, 140, 12, 12, fill=pf.FAMILY_INKS[family]))
        parts.append(pf.text(legend_x + 17, 151, family, note=True))
        legend_x += 86
    # Containment: a unit square and its core on a net direction; a parent and its row
    # core. Both to one scale, turned by the same parent angle.
    angle_row = cert.rows[TIGHT_PAIR[0]]
    cosine, sine = angle_row.rotation
    t026_core = Fraction(src.t026["square_side"])
    scale = 104.0
    panels = (
        (95.0, Fraction(1), t026_core, "unit square", f"core {pf.decimal(t026_core, 6)}"),
        (
            265.0,
            cert.parent_side,
            angle_row.core_side,
            f"parent {cert.parent_side}",
            f"core {pf.decimal(angle_row.core_side, 6)}",
        ),
    )
    parts.append(pf.text(14, 186, "Square and core"))
    for cx, outer, inner, top_label, bottom_label in panels:
        frame = pf.Frame(cx, 262, scale)
        outer_role = pf.PARENT if outer != 1 else pf.Role("#f1f5f9", pf.MUTED, 1.25)
        parts.append(
            pf.polygon(
                map(frame, pf.square_corners((Fraction(0), Fraction(0)), outer, cosine, sine)),
                outer_role,
                attributes=f'data-side="{outer}"',
            )
        )
        parts.append(
            pf.polygon(
                map(frame, pf.square_corners((Fraction(0), Fraction(0)), inner, cosine, sine)),
                pf.CORE,
                attributes=f'data-core-side="{inner}"',
            )
        )
        parts.append(pf.text(cx, 344, top_label, note=True, anchor="middle"))
        parts.append(pf.text(cx, 362, bottom_label, note=True, anchor="middle"))
    # Angle coverage: net directions per degree against rows per degree.
    t026_tangents = [
        Fraction(src.t026["angle_limit"]) * k / int(src.t026["direction_steps"])
        for k in range(int(src.t026["direction_steps"]) + 1)
    ]
    row_tangents = [row.half_tangent for row in cert.rows]
    parts.append(pf.text(14, 396, "Angles covered, per degree"))
    for top, label, tangents, family in (
        (408, f"T-026: {facts['CHANGES_T026_NET']} steps", t026_tangents, "point"),
        (480, f"T-037: {facts['CERT_ROWS']} rows", row_tangents, "3-of-5"),
    ):
        bins = Counter(min(int(_degrees(t)), 44) for t in tangents)
        peak = max(bins.values())
        parts.append(pf.text(14, top + 12, label, note=True))
        for degree in range(45):
            height = 40 * bins.get(degree, 0) / peak
            parts.append(
                pf.rect(
                    30 + 6.6 * degree,
                    top + 58 - height,
                    5.2,
                    height,
                    fill=pf.FAMILY_INKS[family],
                    attributes=f'data-degree="{degree}" data-count="{bins.get(degree, 0)}"',
                )
            )
        parts.append(pf.text(346, top + 12, f"peak {pf.count(peak)}", note=True, anchor="end"))
    parts.extend(_degree_ticks(lambda degree: 30 + 6.6 * degree, 556))
    return pf.svg(
        "threshold-changes",
        "What changed from T-026 to T-037",
        "Top: the share of the counting budget carried by point charges and by each "
        "k-of-m family, in T-026 and in T-037. Middle: a unit square with T-026's core, "
        "and a parent with one of T-037's row cores, to one scale. Bottom: how densely "
        "T-026's net and T-037's rows cover parent angles from 0 to 45 degrees.",
        width=WIDTH,
        height=568,
        body="".join(parts),
    )


# II.3 Roadmap (schematic) -------------------------------------------------------------


def _roadmap_svg(facts: dict[str, str]) -> str:
    # Each card names a section by its heading's words and gives the section's answer.
    cards = (
        ("From Points to k-of-m Charges", "the Budget lemma"),
        (
            "Parents and the One Inequality",
            f"{facts['CERT_ELEVEN_GAMMA']} > {facts['CERT_M']}",
        ),
        (
            "The Certificate\N{RIGHT SINGLE QUOTATION MARK}s Charges",
            f"{facts['CERT_SITES']} sites, {facts['CERT_FEATURES']} charges",
        ),
        ("Parents, Cores and the Angle Catalogue", f"{facts['CERT_ROWS']} angle rows"),
        ("Legal Centers Collect Enough Charge", "an exact sweep"),
        ("The Contradiction and the Strict Bound", "attainment"),
        ("What Was Verified", "replays and receipts"),
    )
    parts: list[str] = []
    top, step, height = 12, 66, 52
    for index, (heading, detail) in enumerate(cards):
        y = top + step * index
        accent = index in (1, 4)
        parts.append(
            pf.rect(
                12,
                y,
                336,
                height,
                fill=pf.GROUND,
                stroke=pf.ACCENT if accent else pf.RULE,
                attributes='stroke-width="1.5" rx="8"',
            )
        )
        parts.append(pf.text(24, y + 22, heading))
        parts.append(pf.text(24, y + 42, detail, note=True))
        if index < len(cards) - 1:
            parts.append(pf.line(180, y + height, 180, y + step, stroke=pf.MUTED, width=1.5))
            parts.append(
                f'<path d="M175 {y + step - 6}l5 6 5-6" fill="none" stroke="{pf.MUTED}" '
                'stroke-width="1.5"/>'
            )
    return pf.svg(
        "threshold-roadmap",
        "The proof's route, section by section",
        "A schematic of the proof's route, one card per section: what a k-of-m charge "
        "pays; why eleven parents cannot fit; what the certificate holds; which core each "
        "parent receives; why every legal center is charged enough; why the bound is "
        "strict; what was checked.",
        width=WIDTH,
        height=top + step * (len(cards) - 1) + height + 12,
        body="".join(parts),
    )


# II.4 One k-of-m charge ---------------------------------------------------------------


def _charge_svg(src: Sources, facts: dict[str, str]) -> str:
    cert = src.certificate
    charge = _orbit(src, CHARGE_ORBIT)
    _require(charge.weight == max(c.weight for c in src.charges), "orbit 72 is not the largest")
    _require(charge.family == "3-of-5", "orbit 72 is not 3-of-5")
    row = cert.rows[CHARGE_ROW]
    members = set(charge.members)
    held = [members & _captured(src, row, centre) for centre in CHARGE_CORES]
    _require(len(held[0]) == 3 and len(held[1]) == 2, "II.4's cores hold the wrong sites")
    _require(_disjoint(row, *CHARGE_CORES), "II.4's cores overlap")
    _require(all(_legal(src, row, c) for c in CHARGE_CORES), "II.4's cores are not legal")
    frame = pf.Frame(34, 312, 120.0, Fraction(0), Fraction(3, 10))
    cosine, sine = row.rotation
    parts = [
        # The container's corner: its left wall and floor, where the cores sit.
        pf.line(
            *frame((0, Fraction(27, 10))),
            *frame((0, Fraction(3, 10))),
            stroke=pf.MUTED,
            width=1.5,
        ),
    ]
    for index, centre in enumerate(CHARGE_CORES):
        role = pf.PAID_CORE if index == 0 else pf.UNPAID_CORE
        corners = pf.square_corners(centre, row.core_side, cosine, sine)
        parts.append(
            pf.polygon(
                map(frame, corners),
                role,
                attributes=(
                    f'data-core="{index}" data-holds="{len(held[index])}" '
                    f'data-paid="{str(len(held[index]) >= charge.threshold).lower()}"'
                ),
            )
        )
        right = max(frame(corner)[0] for corner in corners)
        _, cy = frame(centre)
        holds = len(held[index])
        paid = holds >= charge.threshold
        parts.append(
            pf.text(right + 6, cy - 4, f"holds {holds}", fill=pf.ACCENT if paid else pf.MUTED)
        )
        parts.append(pf.text(right + 6, cy + 14, "paid w" if paid else "unpaid", note=True))
    points = [frame(src.sites[i]) for i in charge.members]
    lowest = max(points, key=lambda point: point[1])
    parts.append(
        pf.hull(
            points,
            charge.threshold,
            badge_at=(lowest[0] + 4, lowest[1] + 22),
            attributes=f'data-orbit="{CHARGE_ORBIT}" data-weight="{charge.weight}"',
        )
    )
    # Inset: the same guarantee bought with points costs 5w/3; the charge costs w.
    y0 = 338.0
    parts.append(pf.rect(12, y0, 336, 92, fill="#f8fafc", stroke=pf.RULE, attributes='rx="8"'))
    for i in range(5):
        x = 34 + 22 * i
        parts.append(pf.point_charge(x, y0 + 32, 5.0, attributes='data-inset-point="1"'))
    parts.append(pf.text(78, y0 + 62, "five points of w/3", note=True, anchor="middle"))
    parts.append(pf.text(78, y0 + 80, "cost 5w/3", anchor="middle"))
    inset = [
        (
            220 + 28 * math.cos(2 * math.pi * i / 5 + 0.3),
            y0 + 34 + 18 * math.sin(2 * math.pi * i / 5 + 0.3),
        )
        for i in range(5)
    ]
    parts.append(pf.hull(inset, 3, badge_at=(292, y0 + 34)))
    parts.append(pf.text(250, y0 + 80, "cost w", anchor="middle"))
    return pf.svg(
        "threshold-charge",
        "One k-of-m charge",
        f"Charge orbit {CHARGE_ORBIT}, a 3-of-5 charge of weight {facts['CHARGE_WEIGHT']}, "
        "with two disjoint cores of one catalogue row: the first holds three of its "
        "five sites and is paid w; the second holds the other two and is paid nothing. "
        "Inset: point weights w/3 on five sites guarantee the same w to a core holding "
        "three of them at cost 5w/3; the charge costs w.",
        width=WIDTH,
        height=y0 + 104,
        body="".join(parts),
    )


# II.5 Budget bars -----------------------------------------------------------------------


def _budget_svg(src: Sources, facts: dict[str, str]) -> str:
    cert = src.certificate
    families = _families(src)
    need = N * cert.minimum_charge
    left, span = 18.0, 324.0
    scale = span / float(11)
    parts = [pf.text(left, 22, "Budget M, by family")]
    x = left
    for family, (_, _, budget) in families.items():
        width = scale * float(budget)
        parts.append(
            pf.rect(
                x,
                32,
                max(width - 2, 0.5),
                26,
                fill=pf.FAMILY_INKS[family],
                attributes=f'data-family="{family}" data-budget="{budget}"',
            )
        )
        x += width
    labels = list(families.items())
    for index, (family, (_, _, budget)) in enumerate(labels):
        column, line_ = index % 2, index // 2
        lx = left + 170 * column
        ly = 80 + 18 * line_
        parts.append(pf.rect(lx, ly - 10, 10, 10, fill=pf.FAMILY_INKS[family]))
        parts.append(pf.text(lx + 15, ly, f"{family} {pf.decimal(budget, 6)}", note=True))
    parts.append(pf.text(left, 140, "Eleven cores need"))
    parts.append(
        pf.rect(
            left, 150, scale * float(need), 26, fill=pf.MUTED, attributes=f'data-need="{need}"'
        )
    )
    # The zoom: the last 0.0003 of the axis, where budget and need end.
    low, high = Fraction(109994, 10000), Fraction(109997, 10000)
    _require(low < cert.budget < need < high, "the zoom window misses the two ends")
    zoom = pf.Frame(left, 0, span / float(high - low), low, 0)
    budget_x = zoom((cert.budget, 0))[0]
    need_x = zoom((need, 0))[0]
    top = 214.0
    axis = top + 40
    parts.append(pf.text(left, top, "Zoom near 11", note=True))
    parts.append(pf.line(left, axis, left + span, axis, stroke=pf.MUTED))
    parts.append(
        pf.rect(
            left,
            axis - 8,
            budget_x - left,
            8,
            fill=pf.FAMILY_INKS["3-of-5"],
            attributes='data-zoom="budget"',
        )
    )
    parts.append(
        pf.rect(left, axis + 1, need_x - left, 8, fill=pf.MUTED, attributes='data-zoom="need"')
    )
    parts.append(pf.line(budget_x, axis - 14, budget_x, axis, stroke=pf.INK, width=1.5))
    parts.append(pf.line(need_x, axis, need_x, axis + 14, stroke=pf.INK, width=1.5))
    parts.append(
        pf.text(
            budget_x,
            axis - 18,
            f"M {facts['CERT_M']}",
            note=True,
            attributes=f'data-budget-units="{_units(cert.budget)}"',
        )
    )
    parts.append(
        pf.text(
            need_x,
            axis + 30,
            f"need {facts['CERT_ELEVEN_GAMMA']}",
            note=True,
            anchor="end",
            attributes=f'data-need-units="{_units(need)}"',
        )
    )
    parts.append(pf.line(budget_x, axis + 40, budget_x, axis + 52, stroke=pf.INK))
    parts.append(pf.line(need_x, axis + 40, need_x, axis + 52, stroke=pf.INK))
    parts.append(pf.line(budget_x, axis + 46, need_x, axis + 46, stroke=pf.INK))
    parts.append(
        pf.text(
            (budget_x + need_x) / 2,
            axis + 68,
            f"surplus {facts['CERT_SURPLUS_UNITS']} units",
            note=True,
            anchor="middle",
            attributes=f'data-surplus="{_units(need - cert.budget)}"',
        )
    )
    parts.extend(
        pf.text(
            zoom((value, 0))[0],
            axis + 90,
            pf.decimal(value, 4),
            note=True,
            anchor="start" if value == low else "end",
        )
        for value in (low, high)
    )
    return pf.svg(
        "threshold-budget",
        "The budget against what eleven cores need",
        f"The four families' budgets stack to M = {facts['CERT_M']}; eleven cores each "
        f"charged at least the certified minimum need {facts['CERT_ELEVEN_GAMMA']}. At "
        f"full scale the bars end together; the zoom shows {pf.decimal(low, 4)} to "
        f"{pf.decimal(high, 4)}, where need exceeds the budget by "
        f"{facts['CERT_SURPLUS_UNITS']} units of one billionth.",
        width=WIDTH,
        height=axis + 102,
        body="".join(parts),
    )


# II.6 Site map and gallery --------------------------------------------------------------


def _families_svg(src: Sources, facts: dict[str, str]) -> str:
    cert = src.certificate
    side = cert.outer_side
    in_charge = {member for charge in src.charges for member in charge.members}
    frame = pf.Frame(14, 346, 332 / float(side))
    parts = [pf.text(14, 0 + 4, "(a) every site, by role", note=True)]
    corners = [frame(p) for p in ((0, 0), (side, 0), (side, side), (0, side))]
    parts.append(pf.polygon(corners, pf.CONTAINER, attributes='data-feature="container"'))
    for mark in (cert.parent_side, side - cert.parent_side):
        x, _ = frame((mark, 0))
        _, y = frame((0, mark))
        parts.append(pf.line(x, corners[2][1], x, corners[0][1], stroke=pf.RULE, dash="3 3"))
        parts.append(pf.line(corners[0][0], y, corners[1][0], y, stroke=pf.RULE, dash="3 3"))
    charge_only = [
        frame(s) for i, s in enumerate(src.sites) if i in in_charge and not src.point_weight[i]
    ]
    path = "".join(f"M{x - 0.8:.1f} {y - 0.8:.1f}h1.6v1.6h-1.6z" for x, y in charge_only)
    parts.append(
        f'<path d="{path}" fill="{pf.FAMILY_INKS["2-of-3"]}" data-role="charge-only" '
        f'data-count="{len(charge_only)}"/>'
    )
    largest = max(src.point_weight)
    for role, wanted in (("point-only", False), ("shared", True)):
        chosen = [
            i for i, w in enumerate(src.point_weight) if w and ((i in in_charge) == wanted)
        ]
        fill = pf.FAMILY_INKS["point"] if role == "point-only" else pf.FAMILY_INKS["2-of-5"]
        circles = "".join(
            f'<circle cx="{frame(src.sites[i])[0]:.1f}" cy="{frame(src.sites[i])[1]:.1f}" '
            f'r="{1.2 + 4.0 * math.sqrt(float(src.point_weight[i] / largest)):.2f}"/>'
            for i in chosen
        )
        parts.append(
            f'<g fill="{fill}" data-role="{role}" data-count="{len(chosen)}">{circles}</g>'
        )
    legend_y = 370.0
    for index, (fill, label) in enumerate(
        (
            (pf.FAMILY_INKS["point"], f"point only {facts['FAMILIES_POINT_ONLY']}"),
            (pf.FAMILY_INKS["2-of-5"], f"point and charge {facts['FAMILIES_SHARED']}"),
            (pf.FAMILY_INKS["2-of-3"], f"charge only {facts['FAMILIES_CHARGE_ONLY']}"),
        )
    ):
        y = legend_y + 18 * index
        parts.append(f'<circle cx="20" cy="{y - 4}" r="4" fill="{fill}"/>')
        parts.append(pf.text(30, y, label, note=True))
    # (b) the largest 2-of-3 charge, about the container's centre.
    triple = _orbit(src, TRIPLE_ORBIT)
    _require(
        triple.weight == max(c.weight for c in src.charges if c.family == "2-of-3"),
        "orbit 206 is not the largest 2-of-3",
    )
    centre = (side / 2, side / 2)
    small = pf.Frame(14, 524, 280.0, Fraction(147, 100), centre[1])
    top = 432.0
    parts.append(pf.text(14, top, "(b) largest 2-of-3", note=True))
    cx, cy = small(centre)
    parts.append(pf.line(cx - 6, cy, cx + 6, cy, stroke=pf.INK, width=1.5))
    parts.append(pf.line(cx, cy - 6, cx, cy + 6, stroke=pf.INK, width=1.5))
    parts.append(pf.text(cx, cy + 44, "center", note=True, anchor="middle"))
    parts.append(pf.line(cx, cy + 8, cx, cy + 30, stroke=pf.RULE))
    triple_points = [small(src.sites[i]) for i in triple.members]
    parts.append(
        pf.hull(
            triple_points,
            2,
            badge_at=(triple_points[0][0] + 20, cy - 34),
            attributes=f'data-orbit="{TRIPLE_ORBIT}" data-weight="{triple.weight}"',
        )
    )
    # (c) the largest 2-of-5 charge, with two disjoint paid cores.
    pair = _orbit(src, PAIR_ORBIT)
    _require(
        pair.weight == max(c.weight for c in src.charges if c.family == "2-of-5"),
        "orbit 130 is not the largest 2-of-5",
    )
    row = cert.rows[PAIR_ROW]
    held = [set(pair.members) & _captured(src, row, c) for c in PAIR_CORES]
    _require(all(len(h) == 2 for h in held), "II.6's cores do not each hold two sites")
    _require(_disjoint(row, *PAIR_CORES), "II.6's cores overlap")
    _require(all(_legal(src, row, c) for c in PAIR_CORES), "II.6's cores are not legal")
    gallery = pf.Frame(188, 600, 65.0, Fraction(0), Fraction(9, 10))
    parts.append(pf.text(196, top, "(c) largest 2-of-5", note=True))
    cosine, sine = row.rotation
    for index, c in enumerate(PAIR_CORES):
        parts.append(
            pf.polygon(
                map(gallery, pf.square_corners(c, row.core_side, cosine, sine)),
                pf.PAID_CORE,
                attributes=f'data-core="{index}" data-holds="{len(held[index])}"',
            )
        )
    pair_points = [gallery(src.sites[i]) for i in pair.members]
    parts.append(
        pf.hull(
            pair_points,
            2,
            badge_at=(330, top + 26),
            attributes=f'data-orbit="{PAIR_ORBIT}" data-weight="{pair.weight}"',
        )
    )
    parts.append(pf.text(272, 622, "two cores, both paid", note=True, anchor="middle"))
    return pf.svg(
        "threshold-families",
        "The certificate's sites and its largest charges",
        f"(a) All {facts['CERT_SITES']} sites in the container: point charges as dots of "
        "area proportional to weight, split by whether the site is also in a k-of-m "
        "charge, and sites in k-of-m charges only as small squares; dashed lines are "
        "x and y equal to A and to the container side minus A. (b) The largest 2-of-3 "
        "charge beside the container's center. (c) The largest 2-of-5 charge with two "
        "disjoint cores of one catalogue row, each holding two of its sites.",
        width=WIDTH,
        height=646,
        body="".join(parts),
        origin=(0, -12),
    )


# II.7 Parent and core ----------------------------------------------------------------


def _mismatch(row: ParentCoreRow, endpoint: Fraction) -> tuple[Fraction, Fraction]:
    """cos d and sin d of the mismatch between the parent at half-tangent `endpoint` and
    the row's core, exactly."""
    pc = (1 - endpoint**2) / (1 + endpoint**2)
    ps = 2 * endpoint / (1 + endpoint**2)
    cc, cs = row.rotation
    return pc * cc + ps * cs, ps * cc - pc * cs


def _core_svg(src: Sources, facts: dict[str, str]) -> str:
    cert = src.certificate
    parent = cert.parent_side
    parts: list[str] = []
    for panel, index in enumerate((0, TIGHT_ROW)):
        row = cert.rows[index]
        margins = []
        for endpoint in (row.left, row.right):
            cos_d, sin_d = _mismatch(row, endpoint)
            margins.append(parent - row.core_side * (cos_d + abs(sin_d)))
        _require(min(margins) > 0, f"row {index}'s core reaches its parent")
        # Drawn: the parent at the row's right endpoint; the core turned by the
        # exaggerated mismatch and shrunk until it fits.
        phi = 2 * math.atan(float(row.right))
        theta = 2 * math.atan(float(row.half_tangent))
        drawn_d = (theta - phi) * CORE_EXAGGERATION
        drawn_d = max(min(drawn_d, math.radians(12)), -math.radians(12))
        cx = 92.0 + 176 * panel
        cy = 128.0
        scale = 112.0

        def square(
            side: float, angle: float, cx: float = cx, cy: float = cy, scale: float = scale
        ) -> list[tuple[float, float]]:
            half = side / 2
            return [
                (
                    cx + scale * (u * math.cos(angle) - v * math.sin(angle)),
                    cy - scale * (u * math.sin(angle) + v * math.cos(angle)),
                )
                for u, v in ((-half, -half), (half, -half), (half, half), (-half, half))
            ]

        shown = float(parent) / (math.cos(drawn_d) + abs(math.sin(drawn_d))) * 0.96
        parts.append(
            pf.polygon(
                square(float(parent), phi),
                pf.PARENT,
                attributes=f'data-row="{index}" data-parent-side="{parent}"',
            )
        )
        parts.append(
            pf.polygon(
                square(shown, phi + drawn_d),
                pf.CORE,
                attributes=(
                    f'data-row="{index}" data-core-side="{row.core_side}" '
                    f'data-margin="{min(margins)}"'
                ),
            )
        )
        parts.append(pf.text(cx - 6, cy + 30, "B", anchor="middle"))
        # The mismatch d: the parent's axis and the core's, from the common centre.
        reach = 0.62 * scale * float(parent)
        for angle, ink in ((phi, pf.ACCENT), (phi + drawn_d, pf.INK)):
            parts.append(
                pf.line(
                    cx,
                    cy,
                    cx + reach * math.cos(angle),
                    cy - reach * math.sin(angle),
                    stroke=ink,
                    width=1.25,
                )
            )
        middle = phi + drawn_d / 2
        parts.append(
            pf.text(
                cx + (reach + 10) * math.cos(middle),
                cy - (reach + 10) * math.sin(middle) + 5,
                "d",
                anchor="middle",
                halo=True,
            )
        )
        corner = min(square(float(parent), phi), key=lambda point: (round(point[1]), -point[0]))
        parts.append(pf.text(corner[0] + 6, corner[1] - 2, "A"))
        parts.append(pf.text(cx, 222, f"row {index}", anchor="middle"))
        parts.append(
            pf.text(cx, 240, f"B {pf.decimal(row.core_side, 6)}", note=True, anchor="middle")
        )
        largest = max(
            abs(_degrees(e) - _degrees(row.half_tangent)) for e in (row.left, row.right)
        )
        parts.append(
            pf.text(
                cx, 258, f"d up to {_rounded_degrees(largest, 4)}", note=True, anchor="middle"
            )
        )
    parts.append(pf.text(180, 22, f"A {parent}", note=True, anchor="middle"))
    return pf.svg(
        "threshold-core",
        "A parent and its row's core",
        "Two catalogue rows, the first and the tightest. Each parent is drawn at the "
        "row's right end, with the row's core about the same center. The mismatch d "
        f"between parent and core is drawn {facts['CORE_EXAGGERATION']} times too large "
        "and the core shrunk to fit; at true scale the two differ by less than a pixel.",
        width=WIDTH,
        height=270,
        body="".join(parts),
    )


# II.8 Catalogue strip -------------------------------------------------------------------


def _catalogue_svg(src: Sources, facts: dict[str, str]) -> str:
    cert = src.certificate
    left, span = 20.0, 320.0
    bins = 90
    counts = Counter(
        min(int(_degrees((row.left + row.right) / 2) * bins / 45), bins - 1)
        for row in cert.rows
    )
    peak = max(counts.values())
    base, tall = 196.0, 100.0
    parts = [
        pf.text(left, 18, "Rows per half degree", note=True),
        pf.text(left + span, 18, f"peak {pf.count(peak)}", note=True, anchor="end"),
    ]
    for b in range(bins):
        height = tall * counts.get(b, 0) / peak
        parts.append(
            pf.rect(
                left + span * b / bins,
                base - height,
                span / bins - 0.6,
                height,
                fill=pf.FAMILY_INKS["point"],
                attributes=f'data-bin="{b}" data-count="{counts.get(b, 0)}"',
            )
        )
    parts.append(pf.line(left, base, left + span, base, stroke=pf.MUTED))
    parts.extend(_degree_ticks(lambda degree: left + span * degree / 45, base + 18))
    # The three rows whose least charge is below 1, labelled above the strip.
    marks = ((TIGHT_ROW,), TIGHT_PAIR)
    for rows, label_y in zip(marks, (44, 70), strict=True):
        angle = _degrees(cert.rows[rows[0]].left)
        x = left + span * angle / 45
        minimum = src.minima[rows[0]]
        _require(all(src.minima[r] == minimum and minimum < UNITS for r in rows), "tight rows")
        parts.append(pf.line(x, label_y + 6, x, base, stroke=pf.INK, width=1.25, dash="2 2"))
        name = f"row {rows[0]}" if len(rows) == 1 else f"rows {rows[0]}{DASH}{rows[-1]}"
        parts.append(
            pf.text(
                x + 4,
                label_y,
                f"{name}: {pf.exact_decimal(Fraction(minimum, UNITS))}",
                note=True,
                anchor="end",
                attributes=f'data-tight="{" ".join(map(str, rows))}" data-minimum="{minimum}"',
            )
        )
    below = [i for i, m in enumerate(src.minima) if m < UNITS]
    _require(below == [*TIGHT_PAIR, TIGHT_ROW], "the rows below 1 are not the three drawn")
    return pf.svg(
        "threshold-catalogue",
        "The angle catalogue",
        f"How the {facts['CATALOGUE_ROWS']} rows spread over parent angles from 0 to 45 "
        "degrees, per half degree, with the three rows whose least charge is below 1 "
        "marked.",
        width=WIDTH,
        height=226,
        body="".join(parts),
    )


# II.9 Envelope --------------------------------------------------------------------------


def _slice(
    src: Sources, row: ParentCoreRow, through: Point, window: Fraction
) -> tuple[list[Fraction], list[Fraction], list[Fraction]]:
    """The charge along the core's first axis through `through`, over ±`window`: event
    positions, the exact charge at each event, and the exact charge on each open piece
    between them (at its midpoint). Positions are offsets along the axis."""
    cosine, sine = row.rotation
    half = row.core_side / 2
    ux = (cosine, sine)
    vy = (-sine, cosine)
    wu = ux[0] * through[0] + ux[1] * through[1]
    wv = vy[0] * through[0] + vy[1] * through[1]
    events: set[Fraction] = set()
    for x, y in src.sites:
        if abs(vy[0] * x + vy[1] * y - wv) <= half:
            u = ux[0] * x + ux[1] * y - wu
            for edge in (u - half, u + half):
                if -window < edge < window:
                    events.add(edge)
    ordered = sorted(events)

    def at(offset: Fraction) -> Fraction:
        u = wu + offset
        centre = (cosine * u - sine * wv, sine * u + cosine * wv)
        return _charge(src, _captured(src, row, centre))

    bounds = [-window, *ordered, window]
    pieces = [at((a + b) / 2) for a, b in pairwise(bounds)]
    return ordered, [at(e) for e in ordered], pieces


def _envelope_svg(src: Sources, facts: dict[str, str]) -> str:
    cert = src.certificate
    row = cert.rows[TIGHT_ROW]
    side = cert.outer_side
    radius = row.centre_margin(cert.parent_side)
    cosine, sine = row.rotation
    middle = (side / 2, side / 2)

    def core_frame(point: tuple[Fraction | int, Fraction | int]) -> Point:
        dx, dy = point[0] - middle[0], point[1] - middle[1]
        return (cosine * dx + sine * dy, -sine * dx + cosine * dy)

    frame = pf.Frame(180, 170, 54.0)
    container = [core_frame(p) for p in ((0, 0), (side, 0), (side, side), (0, side))]
    centres = [
        core_frame(p)
        for p in (
            (radius, radius),
            (side - radius, radius),
            (side - radius, side - radius),
            (radius, side - radius),
        )
    ]
    pattern = "n11-threshold-envelope-hatch"
    parts = [
        pf.polygon(map(frame, container), pf.CONTAINER, attributes='data-feature="container"'),
        pf.domain(
            map(frame, centres),
            pattern,
            attributes=f'data-feature="envelope" data-inset="{radius}"',
        ),
    ]
    # Axes of the core frame, in which every capture set is an axis-aligned rectangle.
    parts.append(pf.line(20, 170, 340, 170, stroke=pf.RULE))
    parts.append(pf.line(180, 14, 180, 326, stroke=pf.RULE))
    parts.append(pf.text(338, 164, "x\N{PRIME}", note=True, anchor="end"))
    parts.append(pf.text(186, 24, "y\N{PRIME}", note=True))
    # The inset, from a container wall to the domain, along the wall's normal.
    wall = core_frame((side / 2, Fraction(0)))
    inner = core_frame((side / 2, radius))
    a, b = frame(wall), frame(inner)
    parts.append(pf.line(*a, *b, stroke=pf.INK, width=1.5))
    parts.append(
        pf.text(
            b[0] + 8,
            b[1] + 22,
            facts["ENVELOPE_RHO"],
            note=True,
            halo=True,
            attributes=f'data-rho="{radius}"',
        )
    )
    centre_px = frame((Fraction(0), Fraction(0)))
    mid_edge = frame(core_frame((side - radius, side / 2)))
    parts.append(pf.line(*centre_px, *mid_edge, stroke=pf.ACCENT, width=1.5, dash="4 3"))
    parts.append(
        pf.text(
            mid_edge[0] + 6,
            mid_edge[1] + 4,
            facts["ENVELOPE_HALF"],
            note=True,
            halo=True,
            attributes=f'data-half="{side / 2 - radius}"',
        )
    )
    # Inset: the charge along a line through the witness, as a step function. On an
    # event the closed core holds every site either side holds, so the charge there is
    # at least both neighbours: upper semicontinuity.
    window = Fraction(1, 200)
    events, at_events, pieces = _slice(src, row, src.witness, window)
    _require(
        all(
            value >= max(left, right)
            for value, left, right in zip(at_events, pieces[:-1], pieces[1:], strict=True)
        ),
        "a closed event value falls below a neighbour",
    )
    top = 350.0
    low = min(pieces)
    high = max(*pieces, *at_events)
    _require(low == Fraction(src.witness_minimum, UNITS), "the slice misses the minimum")
    plot = pf.Frame(30, top + 104, 300 / float(2 * window), -window, low - (high - low) / 6)
    vertical = 80 / float(high - low + (high - low) / 6)
    parts.append(
        pf.rect(12, top - 6, 336, 140, fill="#f8fafc", stroke=pf.RULE, attributes='rx="8"')
    )
    parts.append(
        pf.text(24, top + 14, "charge along x\N{PRIME} through the minimizer", note=True)
    )

    def y_of(value: Fraction) -> float:
        return top + 116 - vertical * float(value - low + (high - low) / 6)

    bounds = [-window, *events, window]
    for (a_, b_), value in zip(pairwise(bounds), pieces, strict=True):
        x1, x2 = plot((a_, 0))[0], plot((b_, 0))[0]
        parts.append(pf.line(x1, y_of(value), x2, y_of(value), stroke=pf.INK, width=2))
    for offset, value, left_value, right_value in zip(
        events, at_events, pieces[:-1], pieces[1:], strict=True
    ):
        if left_value == right_value:
            continue  # an event of a site that changes no charge: no jump to draw
        x = plot((offset, 0))[0]
        parts.extend(
            f'<circle cx="{x:.2f}" cy="{y_of(open_value):.2f}" r="3" '
            f'fill="{pf.GROUND}" stroke="{pf.INK}" stroke-width="1.25"/>'
            for open_value in (left_value, right_value)
            if open_value != value
        )
        parts.append(
            f'<circle cx="{x:.2f}" cy="{y_of(value):.2f}" r="3" fill="{pf.INK}" '
            f'data-event="{offset}" data-charge="{value}"/>'
        )
    parts.append(pf.text(30, top + 130, "filled: value on the event", note=True))
    return pf.svg(
        "threshold-envelope",
        "The center domain in the core frame",
        "The container and, hatched, the union of legal parent centers over the tightest "
        "row, drawn in the coordinates of the row's core, where every capture set is an "
        "axis-aligned rectangle. Inset: the charge along the core's first axis through "
        "the row's minimizer; at each jump the closed core takes the larger value.",
        width=WIDTH,
        height=top + 142,
        body="".join(parts),
        defs=pf.hatch(pattern),
    )


# II.10 Signed rectangles ---------------------------------------------------------------


def _signed_svg(src: Sources, facts: dict[str, str]) -> str:
    cert = src.certificate
    row = cert.rows[TIGHT_ROW]
    triple = _orbit(src, TRIPLE_ORBIT)
    cosine, sine = row.rotation
    half = row.core_side / 2
    # In the core frame a site's capture set is the closed square of side B about it.
    sites = [
        (cosine * x + sine * y, -sine * x + cosine * y)
        for x, y in (src.sites[i] for i in triple.members)
    ]
    boxes = [(u - half, v - half, u + half, v + half) for u, v in sites]

    def meet(indices: Sequence[int]) -> tuple[Fraction, Fraction, Fraction, Fraction]:
        x1 = max(boxes[i][0] for i in indices)
        y1 = max(boxes[i][1] for i in indices)
        x2 = min(boxes[i][2] for i in indices)
        y2 = min(boxes[i][3] for i in indices)
        _require(x1 < x2 and y1 < y2, "II.10's rectangles do not all meet")
        return x1, y1, x2, y2

    left = min(b[0] for b in boxes)
    bottom = min(b[1] for b in boxes)
    extent = max(max(b[2] for b in boxes) - left, max(b[3] for b in boxes) - bottom)
    terms = [((0, 1), 1), ((0, 2), 1), ((1, 2), 1), ((0, 1, 2), 2)]
    parts: list[str] = []
    size = 100.0
    panels = [(*term, i) for i, term in enumerate(terms)] + [((), 0, 4)]
    for subset, _, index in panels:
        column, line_ = index % 3, index // 3
        x0 = 14 + 116 * column
        y0 = 26 + 146 * line_
        frame = pf.Frame(x0, y0 + size, size / float(extent), left, bottom)
        parts.extend(
            pf.polygon(map(frame, _box_corners(box)), pf.Role("none", pf.RULE, 1))
            for box in boxes
        )
        if subset:
            coefficient = _coefficient(triple.threshold, len(subset))
            x1, y1, x2, y2 = meet(subset)
            fill = pf.FAMILY_INKS["2-of-3"] if coefficient > 0 else pf.MUTED
            parts.append(
                pf.polygon(
                    map(frame, [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]),
                    pf.Role(fill, fill, 1.25, fill_opacity=0.35),
                    attributes=(
                        f'data-subset="{"".join(str(i + 1) for i in subset)}" '
                        f'data-coefficient="{coefficient}"'
                    ),
                )
            )
            sign = "+" if coefficient > 0 else MINUS
            name = "pair" if len(subset) == 2 else "triple"
            parts.append(
                pf.text(
                    x0 + size / 2,
                    y0 + size + 20,
                    f"{sign}{abs(coefficient)} {name} {''.join(str(i + 1) for i in subset)}",
                    note=True,
                    anchor="middle",
                )
            )
        else:
            # The sum: one on every centre whose core holds at least two of the three.
            for pair_ in ((0, 1), (0, 2), (1, 2)):
                x1, y1, x2, y2 = meet(pair_)
                parts.append(
                    pf.polygon(
                        map(frame, [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]),
                        pf.Role(SUM_FILL, "none", 0),
                        attributes='data-sum="1"',
                    )
                )
            parts.append(
                pf.text(
                    x0 + size / 2, y0 + size + 20, "sum: 0 or 1", note=True, anchor="middle"
                )
            )
        middle = frame((sum(u for u, _ in sites) / 3, sum(v for _, v in sites) / 3))
        for number, (u, v) in enumerate(sites, start=1):
            px, py = frame((u, v))
            parts.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="2" fill="{pf.INK}"/>')
            if not subset:
                # Each number sits away from the sites' centroid, so two close sites'
                # numbers part.
                dx, dy = px - middle[0], py - middle[1]
                norm = math.hypot(dx, dy) or 1
                parts.append(
                    pf.text(
                        px + 9 * dx / norm,
                        py + 9 * dy / norm + 4,
                        str(number),
                        note=True,
                        anchor="middle",
                    )
                )
    # The identity on every open cell: Σ coefficient C(m, j) = [m ≥ 2].
    for held in range(4):
        total = sum(_coefficient(triple.threshold, j) * comb(held, j) for j in range(2, 4))
        _require(total == int(held >= triple.threshold), "the signed expansion is wrong")
    parts.append(pf.text(14, 12, f"orbit {TRIPLE_ORBIT}: three capture rectangles", note=True))
    return pf.svg(
        "threshold-signed",
        "A 2-of-3 charge as signed rectangles",
        f"The capture rectangles of charge orbit {facts['SIGNED_ORBIT']}'s three sites in "
        "the core frame of the tightest row. Each pair's intersection enters with "
        "coefficient +1 and the triple's with -2; summed, they give 1 exactly where a "
        "core holds at least two of the three sites and 0 elsewhere.",
        width=WIDTH,
        height=310,
        body="".join(parts),
        origin=(0, -6),
    )


# II.11 Charge field -------------------------------------------------------------------


def _field_values(
    src: Sources, row: ParentCoreRow, xs: NDArray[np.float64], ys: NDArray[np.float64]
) -> NDArray[np.float64]:
    """The charge, in units, at every centre of the grid `xs` by `ys`, by direct float
    evaluation of the captures. For pixels only; nothing printed comes from it."""
    sites = np.array([[float(x), float(y)] for x, y in src.sites])
    weights = np.array([_units(w) for w in src.point_weight], dtype=np.float64)
    cosine, sine = (float(v) for v in row.rotation)
    half = float(row.core_side) / 2
    reach = half * math.sqrt(2)
    grouped: dict[tuple[int, int], tuple[list[tuple[int, ...]], list[int]]] = {}
    for charge in src.charges:
        members, values = grouped.setdefault((charge.threshold, len(charge.members)), ([], []))
        members.append(charge.members)
        values.append(_units(charge.weight))
    families = {
        key: (np.array(members, dtype=np.int64), np.array(values, dtype=np.float64))
        for key, (members, values) in grouped.items()
    }
    out = np.empty((len(ys), len(xs)))
    tile = 16
    for j0 in range(0, len(ys), tile):
        for i0 in range(0, len(xs), tile):
            bx, by = xs[i0 : i0 + tile], ys[j0 : j0 + tile]
            near = np.where(
                (sites[:, 0] >= bx.min() - reach)
                & (sites[:, 0] <= bx.max() + reach)
                & (sites[:, 1] >= by.min() - reach)
                & (sites[:, 1] <= by.max() + reach)
            )[0]
            index = np.full(len(sites), -1)
            index[near] = np.arange(len(near))
            gx, gy = np.meshgrid(bx, by)
            dx = sites[near, 0][None, :] - gx.ravel()[:, None]
            dy = sites[near, 1][None, :] - gy.ravel()[:, None]
            captured = (np.abs(cosine * dx + sine * dy) <= half) & (
                np.abs(-sine * dx + cosine * dy) <= half
            )
            total = captured @ weights[near]
            padded = np.concatenate([captured, np.zeros((captured.shape[0], 1), bool)], axis=1)
            for (threshold, _), (members, values) in families.items():
                local = index[members]
                live = (local >= 0).sum(axis=1) >= threshold
                if not live.any():
                    continue
                counts = padded[:, local[live]].sum(axis=2)
                total += (counts >= threshold) @ values[live]
            out[j0 : j0 + tile, i0 : i0 + tile] = total.reshape(len(by), len(bx))
    return out


def _raster(
    values: NDArray[np.float64], levels: Sequence[float], x0: float, y0: float, cell: float
) -> str:
    """One path per level, each the union of its cells as horizontal runs."""
    band = np.searchsorted(np.asarray(levels), values, side="right")
    paths: dict[int, list[str]] = {}
    rows, columns = values.shape
    for j in range(rows):
        y = y0 + cell * (rows - 1 - j)
        start = 0
        for i in range(1, columns + 1):
            if i == columns or band[j, i] != band[j, start]:
                width = cell * (i - start)
                paths.setdefault(int(band[j, start]), []).append(
                    f"M{x0 + cell * start:.2f} {y:.2f}h{width:.2f}v{cell:.2f}h{-width:.2f}z"
                )
                start = i
    return "".join(
        f'<path d="{"".join(segments)}" fill="{FIELD_RAMP[level]}" data-level="{level}"/>'
        for level, segments in sorted(paths.items())
    )


def _field_svg(src: Sources, facts: dict[str, str]) -> str:
    cert = src.certificate
    row = cert.rows[TIGHT_ROW]
    side = cert.outer_side
    radius = row.centre_margin(cert.parent_side)
    _require(_legal(src, row, src.witness), "the witness is outside the row's domain")
    exact = _charge(src, _captured(src, row, src.witness))
    _require(exact * UNITS == src.witness_minimum, "the witness's charge is not the minimum")
    _require(src.witness_minimum == src.minima[TIGHT_ROW], "witness and replay disagree")
    low, high = float(radius), float(side - radius)
    step = (high - low) / FIELD_GRID
    xs = low + (np.arange(FIELD_GRID, dtype=np.float64) + 0.5) * step
    values = _field_values(src, row, xs, xs)
    _require(values.min() >= src.witness_minimum, "a raster cell is below the minimum")
    levels = [float(level) * UNITS for level in FIELD_LEVELS]
    size = 300.0
    cell = size / FIELD_GRID
    left, top = 30.0, 24.0
    parts = [pf.text(left, 14, f"row {TIGHT_ROW}: charge over the center domain", note=True)]
    parts.append(_raster(values, levels, left, top, cell))
    parts.append(
        pf.rect(
            left, top, size, size, fill="none", stroke=pf.MUTED, attributes='stroke-width="1"'
        )
    )
    to_px = pf.Frame(left, top + size, size / (high - low), low, low)
    wx, wy = to_px(src.witness)
    parts.append(
        f'<circle cx="{wx:.2f}" cy="{wy:.2f}" r="7" fill="none" stroke="{pf.GROUND}" '
        f'stroke-width="4"/><circle cx="{wx:.2f}" cy="{wy:.2f}" r="7" fill="none" '
        f'stroke="{pf.INK}" stroke-width="2" data-witness="{src.witness[0]} {src.witness[1]}" '
        f'data-charge="{src.witness_minimum}"/>'
    )
    parts.append(
        pf.text(
            wx + 12,
            wy - 10,
            f"minimum {facts['FIELD_MIN']}",
            note=True,
            anchor="start" if wx < 160 else "end",
            halo=True,
        )
    )
    legend_top = top + size + 18
    swatch = 46.0
    for index, fill in enumerate(FIELD_RAMP):
        parts.append(pf.rect(left - 10 + swatch * index, legend_top, swatch - 2, 12, fill=fill))
    for index, level in enumerate(FIELD_LEVELS, start=1):
        parts.append(
            pf.text(
                left - 11 + swatch * index,
                legend_top + 30,
                f"{level.numerator / level.denominator:g}",
                note=True,
                anchor="middle",
                attributes=f'data-level-bound="{level}"',
            )
        )
    return pf.svg(
        "threshold-field",
        "The charge field of the tightest row",
        f"The charge of the row's core at every legal center, sampled on a {FIELD_GRID} by "
        f"{FIELD_GRID} grid and shaded in seven bands, darker for less charge. The ring is "
        f"the row's exact minimizer, replayed by T-059, of charge {facts['FIELD_MIN']}.",
        width=WIDTH,
        height=legend_top + 40,
        body="".join(parts),
    )


# II.12 Per-row minima -----------------------------------------------------------------


def _minima_svg(src: Sources, facts: dict[str, str]) -> str:
    cert = src.certificate
    gamma = _units(cert.minimum_charge)
    top_value = max(src.histogram)
    low = gamma - 6000
    high = top_value + 6000
    left, span, top, height = 46.0, 300.0, 24.0, 200.0

    def x_of(index: int) -> float:
        row = cert.rows[index]
        return left + span * _degrees((row.left + row.right) / 2) / 45

    def y_of(value: int) -> float:
        return top + height * (high - value) / (high - low)

    parts = [pf.text(14, 14, "least charge per row", note=True)]
    # The native lower bounds as a band: per bin, from the least native bound to the
    # source's minimum.
    bins = 150
    band: dict[int, tuple[int, int]] = {}
    for index, (lower, minimum) in enumerate(zip(src.native_lower, src.minima, strict=True)):
        _require(gamma <= lower <= minimum, "a native lower bound is outside [Γ, minimum]")
        b = min(int((x_of(index) - left) / span * bins), bins - 1)
        lo, hi = band.get(b, (lower, lower))
        band[b] = (min(lo, lower), max(hi, lower))
    for b, (lo, hi) in sorted(band.items()):
        parts.append(
            pf.rect(
                left + span * b / bins,
                y_of(hi) - 0.5,
                span / bins + 0.2,
                y_of(lo) - y_of(hi) + 1,
                fill=pf.FAMILY_INKS["point"],
                attributes='fill-opacity="0.3"',
            )
        )
    # Γ.
    parts.append(
        pf.line(
            left, y_of(gamma), left + span, y_of(gamma), stroke=pf.ACCENT, width=1.5, dash="5 3"
        )
    )
    parts.append(
        pf.text(
            left + span,
            y_of(gamma) + 16,
            facts["CERT_GAMMA"],
            note=True,
            anchor="end",
            fill=pf.ACCENT,
        )
    )
    parts.append(pf.line(left, y_of(UNITS), left + span, y_of(UNITS), stroke=pf.RULE))
    parts.append(pf.text(left - 4, y_of(UNITS) + 4, "1", note=True, anchor="end"))
    # The source's minima, one mark per distinct pixel.
    seen: set[tuple[int, int]] = set()
    marks: list[str] = []
    for index, minimum in enumerate(src.minima):
        key = (round(x_of(index) * 2), round(y_of(minimum) * 2))
        if key in seen:
            continue
        seen.add(key)
        marks.append(f"M{x_of(index) - 1:.1f} {y_of(minimum) - 1:.1f}h2v2h-2z")
    parts.append(f'<path d="{"".join(marks)}" fill="{pf.INK}" data-series="python-minima"/>')
    parts.append(
        pf.text(
            left + span,
            y_of(top_value) - 6,
            pf.exact_decimal(Fraction(top_value, UNITS)),
            note=True,
            anchor="end",
            attributes=f'data-top="{top_value}"',
        )
    )
    for rows, dy in (((TIGHT_ROW,), -10), (TIGHT_PAIR, -10)):
        x = x_of(rows[0])
        y = y_of(src.minima[rows[0]])
        parts.append(
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="none" stroke="{pf.INK}" '
            'stroke-width="1.5"/>'
        )
        name = f"row {rows[0]}" if len(rows) == 1 else f"rows {rows[0]}{DASH}{rows[-1]}"
        parts.append(
            pf.text(
                x - 6,
                y + dy,
                name,
                note=True,
                anchor="end",
                attributes=f'data-tight="{" ".join(map(str, rows))}"',
            )
        )
    parts.extend(_degree_ticks(lambda degree: left + span * degree / 45, top + height + 18))
    legend = top + height + 40
    parts.append(
        pf.rect(
            14,
            legend - 10,
            14,
            10,
            fill=pf.FAMILY_INKS["point"],
            attributes='fill-opacity="0.3"',
        )
    )
    parts.append(pf.text(34, legend, "native lower bounds", note=True))
    parts.append(f'<path d="M190 {legend - 6}h4v4h-4z" fill="{pf.INK}"/>')
    parts.append(pf.text(200, legend, "exact minima", note=True))
    return pf.svg(
        "threshold-minima",
        "Every row's least charge",
        "The exact least charge of each of the source's rows against parent angle, with "
        "the certified minimum dashed and the three rows below 1 ringed. The shaded band "
        "spans, per sliver of angle, the lower bounds this repository's native interval "
        "check certified: an interval method certifies a lower bound, not the minimum.",
        width=WIDTH,
        height=legend + 12,
        body="".join(parts),
    )


# Public entry points ------------------------------------------------------------------


def caption_facts() -> dict[str, str]:
    """Every number a caption or the article states of these figures, from the data.

    Keys name a figure and a fact, `<FIGURE>_<FACT>`; facts of the whole certificate
    take `CERT_`. The renderer refuses one the article does not use."""
    src = _sources()
    key = _pins()
    if key not in _FACTS:
        _FACTS.clear()
        _FACTS[key] = _facts(src)
    return dict(_FACTS[key])


def render_figures() -> dict[str, str]:
    """One complete static SVG per key of `FIGURE_KEYS`, from the pinned inputs."""
    src = _sources()
    key = _pins()
    if key not in _RENDERED:
        facts = caption_facts()
        figures = {
            "CHANGES_SVG": _changes_svg(src, facts),
            "LADDER_SVG": src.ladder,
            "ROADMAP_SVG": _roadmap_svg(facts),
            "CHARGE_SVG": _charge_svg(src, facts),
            "BUDGET_SVG": _budget_svg(src, facts),
            "FAMILIES_SVG": _families_svg(src, facts),
            "CORE_SVG": _core_svg(src, facts),
            "CATALOGUE_SVG": _catalogue_svg(src, facts),
            "ENVELOPE_SVG": _envelope_svg(src, facts),
            "SIGNED_SVG": _signed_svg(src, facts),
            "FIELD_SVG": _field_svg(src, facts),
            "MINIMA_SVG": _minima_svg(src, facts),
        }
        _require(tuple(figures) == FIGURE_KEYS, "figure keys out of order")
        _RENDERED.clear()
        _RENDERED[key] = figures
    return dict(_RENDERED[key])
