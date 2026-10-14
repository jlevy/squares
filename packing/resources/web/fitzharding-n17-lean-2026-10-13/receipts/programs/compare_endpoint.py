"""Compare sq17-lean's endpoint constant with this repository's n = 17 chart, exactly.

Reads, as text, the packet's retained ``Sq17Lean/EndpointRootData.lean`` and
``Sq17Lean/EndpointGeometry.lean``, and this repository's own n = 17 records: exp-237's
frozen certificate, H-255's formulas as ``devtools.check_n17_root_certificate`` builds
them, H-256's layout in ``devtools.check_n17_endpoint_feasibility``, n-017's catalogue
polynomial and verified ceiling, and exp-245's enclosure of the side. Nothing from the
source is executed: its numbers are parsed from the Lean text by regular expressions and
every comparison is exact rational arithmetic written here. Prints one JSON object:

- ``identity``: the two polynomials term for term, the midpoint and the radius against
  exp-237's certificate and against H-255's formulas, and the side map against the
  record's, which together make ``EndpointGeometry.side`` the record's L by identity of
  definition;
- ``contraction``: the Lean's own Newton certificate recomputed, the preconditioner's
  determinant, the coefficient masses and slopes its ``check`` bounds, and both Newton
  identities by exact expansion of ``P(m + r p)``;
- ``side``: the common zero refined in the box by exact Newton steps, the side to 60
  places, the residuals there, the catalogue polynomial's sign change across it, the
  record's ceiling above it, and exp-245's enclosure around it.

Usage, from ``packing/``, with the project interpreter and ``-I``::

    .venv/bin/python3 -I PACKET/receipts/programs/compare_endpoint.py PACKET REPO

``PACKET`` is the packet directory and ``REPO`` the repository root; the output is the
packet's ``receipts/endpoint-comparison.json``.
"""

from __future__ import annotations

import json
import re
import sys
from fractions import Fraction as Q
from math import comb
from pathlib import Path

Poly = dict[tuple[int, int], Q]

packet, repo = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "packing"))

from devtools.build_bound_citations import load_case  # noqa: E402
from devtools.check_n17_catalogue_polynomial import CATALOGUE, load_catalogue  # noqa: E402
from devtools.check_n17_endpoint_feasibility import _layout  # noqa: E402
from devtools.check_n17_root_certificate import n17_polynomials  # noqa: E402

LEAN = packet / "sq17-lean" / "Sq17Lean"
RESULTS = repo / "packing/campaign/series/series-000-smoke-and-calibration/results"
EXP237 = RESULTS / "exp-237-n17-polynomial-root/run-001/certificate.json"
EXP245 = RESULTS / "exp-245-n17-catalogue-polynomial/run-001/receipt.json"
#: The record's side map, `(6 + 4t)/(1 + 2t - t^2)`, as the Lean writes it.
SIDE_TEXT = "(6+4*t)/(1+2*t-t*t)"
PLACES = 60
WORKING = 10**200

data = (LEAN / "EndpointRootData.lean").read_text(encoding="utf-8")
geometry = (LEAN / "EndpointGeometry.lean").read_text(encoding="utf-8")
TERM = re.compile(r"⟨(\d+),(\d+),\(?(-?\d+)(?:/(\d+))?\)?⟩")


def terms(name: str) -> Poly:
    match = re.search(r"def " + name + r" : List Term := \[(.*?)\]\n", data, re.S)
    if match is None:
        raise SystemExit(f"no {name} in EndpointRootData.lean")
    found: Poly = {}
    for i, j, numerator, denominator in TERM.findall(match.group(1)):
        key = (int(i), int(j))
        if key in found:
            raise SystemExit(f"{name} repeats the monomial {key}")
        found[key] = Q(int(numerator), int(denominator) if denominator else 1)
    return found


def rational(name: str) -> Q:
    match = re.search(r"def " + name + r" : ℚ := \((-?\d+)/(\d+)\)", data)
    if match is None:
        raise SystemExit(f"no {name} in EndpointRootData.lean")
    return Q(int(match.group(1)), int(match.group(2)))


found_midpoint = re.search(r"def midpoint : ℚ × ℚ := \(\((\d+)/(\d+)\),\((\d+)/(\d+)\)\)", data)
if found_midpoint is None:
    raise SystemExit("no midpoint in EndpointRootData.lean")
midpoint = (
    Q(int(found_midpoint.group(1)), int(found_midpoint.group(2))),
    Q(int(found_midpoint.group(3)), int(found_midpoint.group(4))),
)
radius = rational("radius")
first, second = terms("polynomial0"), terms("polynomial1")
newton0, newton1 = terms("newton0"), terms("newton1")
c00, c01, c10, c11 = (rational(name) for name in ("c00", "c01", "c10", "c11"))
found_side = re.search(r"^def side : ℝ := (.+)$", geometry, re.M)
side_text = found_side.group(1).strip() if found_side else None


def nonzero(poly: dict[tuple[int, int], int]) -> Poly:
    return {key: Q(value) for key, value in poly.items() if value}


# 1. Identity of definition with exp-237's certificate and H-255's formulas.
certificate = json.loads(EXP237.read_text(encoding="utf-8"))
frozen = [{(i, j): Q(c) for i, j, c in poly} for poly in certificate["polynomials"]]
formula_first, formula_second = (nonzero(poly) for poly in n17_polynomials())


def record_side(t: Q) -> Q:
    return (6 + 4 * t) / (1 + 2 * t - t * t)


probes = [Q(1, 3), Q(9, 25), Q(3, 8), midpoint[0]]
layout_side = [_layout(t, Q(1, 3), Q(1, 2))[0] for t in probes]
identity = {
    "polynomial0_equals_exp237": first == frozen[0],
    "polynomial1_equals_exp237": second == frozen[1],
    "midpoint_equals_exp237": midpoint == tuple(Q(x) for x in certificate["box"]["midpoint"]),
    "radius_equals_exp237": radius == Q(certificate["box"]["radius"]),
    "polynomial0_equals_H255_formula": first == formula_first,
    "polynomial1_equals_H255_formula": second == formula_second,
    "lean_side_definition": side_text,
    "lean_side_definition_is_the_record_map": side_text == SIDE_TEXT,
    "record_map_equals_H256_layout_side": layout_side == [record_side(t) for t in probes],
}


# 2. The Lean's contraction certificate, recomputed.
def mass(poly: Poly) -> Q:
    return sum((abs(c) for c in poly.values()), Q(0))


def slope(poly: Poly) -> Q:
    return sum((abs(c) * (i + j) for (i, j), c in poly.items()), Q(0))


def shifted(poly: Poly) -> Poly:
    """P(m + r p) expanded in p, exactly."""
    out: Poly = {}
    for (i, j), c in poly.items():
        for a in range(i + 1):
            for b in range(j + 1):
                term = c * comb(i, a) * midpoint[0] ** (i - a) * radius**a
                term *= comb(j, b) * midpoint[1] ** (j - b) * radius**b
                out[(a, b)] = out.get((a, b), Q(0)) + term
    return {key: value for key, value in out.items() if value}


first_shifted, second_shifted = shifted(first), shifted(second)


def newton(a: Q, b: Q, unit: tuple[int, int]) -> Poly:
    out: Poly = {}
    for key in set(first_shifted) | set(second_shifted):
        value = a * first_shifted.get(key, Q(0)) + b * second_shifted.get(key, Q(0))
        out[key] = -value / radius
    out[unit] = out.get(unit, Q(0)) + 1
    return {key: value for key, value in out.items() if value}


contraction = {
    "determinant_nonzero": c00 * c11 - c01 * c10 != 0,
    "mass_newton0": float(mass(newton0)),
    "mass_newton1": float(mass(newton1)),
    "slope_newton0": float(slope(newton0)),
    "slope_newton1": float(slope(newton1)),
    "check_passes": mass(newton0) <= 1
    and mass(newton1) <= 1
    and slope(newton0) <= Q(1, 2)
    and slope(newton1) <= Q(1, 2),
    "newton0_identity_exact": newton(c00, c01, (1, 0)) == newton0,
    "newton1_identity_exact": newton(c10, c11, (0, 1)) == newton1,
}


# 3. The side, by exact Newton refinement in the box.
def value(poly: Poly, t: Q, b: Q) -> Q:
    return sum((c * t**i * b**j for (i, j), c in poly.items()), Q(0))


def derivative(poly: Poly, variable: int) -> Poly:
    out: Poly = {}
    for (i, j), c in poly.items():
        power = (i, j)[variable]
        if power:
            out[(i - (variable == 0), j - (variable == 1))] = c * power
    return out


ft, fb, gt, gb = (derivative(p, v) for p in (first, second) for v in (0, 1))
t, b = midpoint
for _ in range(8):
    f, g = value(first, t, b), value(second, t, b)
    a11, a12, a21, a22 = (value(p, t, b) for p in (ft, fb, gt, gb))
    det = a11 * a22 - a12 * a21
    t = Q(round((t - (a22 * f - a12 * g) / det) * WORKING), WORKING)
    b = Q(round((b - (a11 * g - a21 * f) / det) * WORKING), WORKING)
side = record_side(t)


def decimal(x: Q, places: int) -> str:
    whole = x.numerator // x.denominator
    return f"{whole}.{str(int((x - whole) * 10**places)).rjust(places, '0')}"


coefficients, degree = load_catalogue(CATALOGUE)


def horner(x: Q) -> Q:
    out = Q(0)
    for coefficient in coefficients:
        out = out * x + coefficient
    return out


eps = Q(1, 10**40)
ceiling = Q(str(load_case(17)["verified_upper_bound"]["exact_form"]))
low, high = (Q(x) for x in json.loads(EXP245.read_text(encoding="utf-8"))["root_enclosure"])
side_report = {
    "root_in_box": abs(t - midpoint[0]) <= radius and abs(b - midpoint[1]) <= radius,
    "t_60": decimal(t, PLACES),
    "beta_60": decimal(b, PLACES),
    "side_60": decimal(side, PLACES),
    "residual_polynomial0": float(abs(value(first, t, b))),
    "residual_polynomial1": float(abs(value(second, t, b))),
    "catalogue_degree": degree,
    "catalogue_residual_at_side": float(abs(horner(side))),
    "catalogue_sign_change_across_side_pm_1e-40": (horner(side - eps) > 0)
    != (horner(side + eps) > 0),
    "verified_ceiling_minus_side": float(ceiling - side),
    "exp245_enclosure_width": float(high - low),
    "side_in_exp245_enclosure": low <= side <= high,
}

print(
    json.dumps(
        {
            "format": "sq17-lean-endpoint-comparison-v1",
            "inputs": {
                "lean": [
                    "sq17-lean/Sq17Lean/EndpointRootData.lean",
                    "sq17-lean/Sq17Lean/EndpointGeometry.lean",
                ],
                "record": [
                    str(EXP237.relative_to(repo)),
                    str(EXP245.relative_to(repo)),
                    str(CATALOGUE.relative_to(repo)),
                    "packing/devtools/check_n17_root_certificate.py",
                    "packing/devtools/check_n17_endpoint_feasibility.py",
                ],
            },
            "identity": identity,
            "contraction": contraction,
            "side": side_report,
        },
        indent=2,
        ensure_ascii=False,
    )
)
