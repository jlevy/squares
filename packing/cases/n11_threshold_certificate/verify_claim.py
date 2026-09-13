#!/usr/bin/env python3
"""Decide a threshold certificate and its optional dilation-limit record, exactly.

Usage:  python verify_claim.py certificate.json
        python verify_claim.py t-025-verifiable-claim-191-50.md
        python verify_claim.py t-026-verifiable-claim-dilation-limit.md

This file uses only the Python 3.12 standard library.  A Markdown claim document embeds
this source, the certificate bytes, and, for a dilation-limit claim, the limit-record
bytes.  The verifier reads the marked data blocks, checks their SHA-256 identities, and
then decides the mathematical conditions from the embedded data.

For point atoms (x, y, w), a closed core receives w when it contains (x, y).  A
threshold atom (S, k, w) contributes w when the core contains at least k points of S.
Its budget is w floor(|S|/k), because pairwise-disjoint cores have disjoint traces on S.
The certificate is valid when both atom families are D4-invariant, their total budget is
below n, the direction net reaches pi/4, B(1+D)<1 for the largest half-gap tangent D,
and every admissible B-square at every net direction receives total weight at least one.

The last condition is a finite exact computation.  In coordinates rotated to a net
direction, each point is contained precisely on a closed axis-parallel rectangle of
core centres.  Rectangle edges cut the admissible centre domain into open cells.  A
core's trace is constant on each cell, while closedness and monotonicity make boundary
values no smaller.  The threshold indicator is expanded as

    [m >= k] = sum_(j=k)^r (-1)^(j-k) C(j-1,k-1) C(m,j).

Thus point and threshold charge is a signed sum of rectangle indicators.  The signs are
internal to that identity; the underlying atom weights remain nonnegative.  A slab
sweep evaluates the sum using exact integer arithmetic after one common weight scale.

The optional limit record is accepted only after its source certificate passes.  The
verifier then re-derives D, the strict dilation test, the factor supremum squared, the
exact algebraic side and its defining polynomial.  The theorem follows for the exact
supremum from all strict rational subfactors, rational density, upward embedding, and
the infimum definition of s(n).  No certificate at the algebraic endpoint is asserted.
"""

# ruff: noqa: E501, FBT003, N803, N806, PLR0917, TRY300, TRY301
# The long exact-value reports are kept legible, and L, B, D, U, V are proof symbols.

import argparse
import hashlib
import json
import re
import sys
from bisect import bisect_left, bisect_right
from collections import defaultdict
from collections.abc import Sequence
from fractions import Fraction
from itertools import combinations, pairwise
from math import comb, gcd, isqrt, lcm
from pathlib import Path

MAX_BYTES = 32 * 1024 * 1024
MAX_POINT_ATOMS = 2000
MAX_THRESHOLD_ATOMS = 1000
MAX_DIRECTIONS = 2000

CERT_BEGIN = "<!-- BEGIN THRESHOLD CERTIFICATE -->"
CERT_END = "<!-- END THRESHOLD CERTIFICATE -->"
LIMIT_BEGIN = "<!-- BEGIN DILATION LIMIT RECORD -->"
LIMIT_END = "<!-- END DILATION LIMIT RECORD -->"


def object_without_duplicate_keys(pairs):
    """Construct a JSON object while refusing a duplicate key."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def marked_bytes(text, begin, end):
    """Return the exact bytes inside one marked fenced block."""
    pattern = re.escape(begin) + r"\n```json\n(.*?)```\n" + re.escape(end)
    matches = re.findall(pattern, text, re.DOTALL)
    if len(matches) != 1:
        raise ValueError(f"expected exactly one block between {begin!r} and {end!r}")
    return matches[0].encode("utf-8")


def read_input(path):
    """Return certificate bytes, optional limit bytes, and their document declarations."""
    raw = Path(path).read_bytes()
    if len(raw) > MAX_BYTES:
        raise ValueError(f"input is {len(raw)} bytes; ceiling is {MAX_BYTES}")
    if raw.lstrip().startswith(b"{"):
        return raw, None, {}
    text = raw.decode("utf-8")
    cert = marked_bytes(text, CERT_BEGIN, CERT_END)
    limit_is_mentioned = any(
        re.search(pattern, text, re.MULTILINE)
        for pattern in (
            rf"^{re.escape(LIMIT_BEGIN)}$",
            rf"^{re.escape(LIMIT_END)}$",
            r"^Limit Record SHA-256:",
        )
    )
    limit = marked_bytes(text, LIMIT_BEGIN, LIMIT_END) if limit_is_mentioned else None
    declarations = {}
    for name in ("certificate", "limit record"):
        match = re.search(
            rf"^{re.escape(name.title())} SHA-256: `([0-9a-f]{{64}})`; bytes: `([0-9]+)`\.$",
            text,
            re.MULTILINE,
        )
        if match:
            declarations[name] = (match.group(1), int(match.group(2)))
    if "certificate" not in declarations:
        raise ValueError("claim document has no certificate SHA-256 and byte declaration")
    if limit is not None and "limit record" not in declarations:
        raise ValueError("claim document has no limit-record SHA-256 and byte declaration")
    return cert, limit, declarations


def parse_json(raw):
    return json.loads(raw, object_pairs_hook=object_without_duplicate_keys)


def rational(value):
    if not isinstance(value, str):
        raise TypeError(f"rationals must be strings, got {value!r}")
    return Fraction(value)


def integer(value, name, *, at_least=0):
    if not isinstance(value, int) or isinstance(value, bool) or value < at_least:
        raise TypeError(f"{name} must be an integer >= {at_least}, got {value!r}")
    return value


def d4_images(point, L):
    x, y = point
    flips = [(p, q) for p in (x, L - x) for q in (y, L - y)]
    return tuple(flips + [(q, p) for p, q in flips])


def load_certificate(raw):
    """Parse and strictly validate the retained threshold-certificate schema."""
    record = parse_json(raw)
    if not isinstance(record, dict):
        raise TypeError("certificate must be one JSON object")
    if record.get("variant") != "threshold":
        raise ValueError("variant must be 'threshold'")
    if record.get("symmetry") != "D4":
        raise ValueError("symmetry must be 'D4'")
    n = integer(record["n"], "n", at_least=1)
    K = integer(record["direction_steps"], "direction_steps", at_least=1)
    if K + 1 > MAX_DIRECTIONS:
        raise ValueError(f"{K + 1} directions exceeds ceiling {MAX_DIRECTIONS}")
    L, B, T = (rational(record[name]) for name in ("outer_side", "square_side", "angle_limit"))
    if not (L > 0 and B > 0 and 0 < T < 1):
        raise ValueError("outer_side and square_side must be positive and 0 < angle_limit < 1")

    atoms = []
    sites = set()
    if len(record["atoms"]) > MAX_POINT_ATOMS:
        raise ValueError("too many point atoms")
    for item in record["atoms"]:
        if not isinstance(item, list) or len(item) != 3:
            raise ValueError("each point atom must be [x, y, weight]")
        x, y, w = map(rational, item)
        if w < 0 or not (0 <= x <= L and 0 <= y <= L):
            raise ValueError(
                "point atoms need nonnegative weight and sites inside the container"
            )
        if (x, y) in sites:
            raise ValueError(f"two point atoms share ({x}, {y})")
        sites.add((x, y))
        atoms.append((x, y, w))

    threshold_atoms = []
    keys = set()
    if len(record["threshold_atoms"]) > MAX_THRESHOLD_ATOMS:
        raise ValueError("too many threshold atoms")
    for item in record["threshold_atoms"]:
        if not isinstance(item, dict) or not isinstance(item.get("points"), list):
            raise TypeError("each threshold atom must be an object with a points array")
        if any(not isinstance(p, list) or len(p) != 2 for p in item["points"]):
            raise TypeError("each threshold point must be [x, y]")
        points = tuple((rational(p[0]), rational(p[1])) for p in item["points"])
        k = integer(item["threshold"], "threshold", at_least=1)
        w = rational(item["weight"])
        if len(points) != 3 or k != 2:
            raise ValueError(
                "this verifier intentionally accepts only two-of-three threshold atoms"
            )
        if len(set(points)) != len(points):
            raise ValueError("a threshold atom repeats a point")
        if w < 0 or any(not (0 <= x <= L and 0 <= y <= L) for x, y in points):
            raise ValueError(
                "threshold atoms need nonnegative weight and points inside the container"
            )
        key = (tuple(sorted(points)), k)
        if key in keys:
            raise ValueError("two threshold atoms share the same point set and threshold")
        keys.add(key)
        threshold_atoms.append((points, k, w))

    declared = {
        "claim": record["claim"],
        "point_mass": rational(record["point_mass"]),
        "threshold_budget": rational(record["threshold_budget"]),
        "total_budget": rational(record["total_budget"]),
        "least_cell_charge": (
            rational(record["least_cell_charge"]) if "least_cell_charge" in record else None
        ),
    }
    if not isinstance(declared["claim"], str):
        raise TypeError("claim must be a string")
    for k in range(K + 1):
        t = T * k / K
        c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
        if B * (c + s) >= L:
            raise ValueError(
                "a net direction has an empty or singleton admissible-center domain; "
                "this verifier accepts only domains with interior"
            )
    return record, n, L, B, T, K, tuple(atoms), tuple(threshold_atoms), declared


def point_symmetry(atoms, L):
    weights = {(x, y): w for x, y, w in atoms}
    for (x, y), w in weights.items():
        for image in d4_images((x, y), L):
            if weights.get(image) != w:
                return (
                    f"point atom at ({x}, {y}) has a missing or unequal image at {image}",
                    False,
                )
    return f"{len(atoms)} point atoms are D4-invariant", True


def threshold_symmetry(threshold_atoms, L):
    weights = {(tuple(sorted(points)), k): w for points, k, w in threshold_atoms}
    for points, k, w in threshold_atoms:
        per_point = [d4_images(point, L) for point in points]
        for g in range(8):
            image = (tuple(sorted(images[g] for images in per_point)), k)
            if weights.get(image) != w:
                return "a threshold atom has a missing or unequal D4 image", False
    return f"{len(threshold_atoms)} threshold atoms are D4-invariant", True


def clip(polygon, bound, *, greater):
    if not polygon:
        return ()
    output = []
    previous = polygon[-1]
    previous_inside = previous[0] >= bound if greater else previous[0] <= bound
    for current in polygon:
        current_inside = current[0] >= bound if greater else current[0] <= bound
        if current_inside != previous_inside:
            u1, v1 = previous
            u2, v2 = current
            factor = (bound - u1) / (u2 - u1)
            output.append((bound, v1 + factor * (v2 - v1)))
        if current_inside:
            output.append(current)
        previous, previous_inside = current, current_inside
    return tuple(output)


def centre_domain(L, B, c, s):
    h = B * (c + s) / 2
    corners = ((h, h), (L - h, h), (L - h, L - h), (h, L - h))
    return tuple((c * x + s * y, -s * x + c * y) for x, y in corners)


def cell_witness(domain, u0, u1, v0, v1):
    polygon = clip(clip(domain, u0, greater=True), u1, greater=False)
    transposed = tuple((v, u) for u, v in polygon)
    transposed = clip(clip(transposed, v0, greater=True), v1, greater=False)
    polygon = tuple((u, v) for v, u in transposed)
    if not polygon:
        raise AssertionError("reachable cell has no witness")
    count = len(polygon)
    witness = (
        sum((u for u, _ in polygon), start=Fraction()) / count,
        sum((v for _, v in polygon), start=Fraction()) / count,
    )
    if not (u0 < witness[0] < u1 and v0 < witness[1] < v1):
        raise AssertionError("reachable cell has no interior witness")
    return witness


def exact_charge(atoms, threshold_atoms, c, s, half, witness):
    Uc, Vc = witness

    def contains(x, y):
        u, v = c * x + s * y, -s * x + c * y
        return abs(u - Uc) <= half and abs(v - Vc) <= half

    total = sum((w for x, y, w in atoms if contains(x, y)), start=Fraction())
    for points, k, w in threshold_atoms:
        if sum(contains(x, y) for x, y in points) >= k:
            total += w
    return total


def expansion_terms(size, threshold):
    return tuple(
        (j, (-1) ** (j - threshold) * comb(j - 1, threshold - 1))
        for j in range(threshold, size + 1)
    )


class RangeMinimum:
    """Lazy range-add tree returning the least value and first index in an interval."""

    def __init__(self, size):
        self.size = size
        length = 4 * max(1, size)
        self.minimum = [0] * length
        self.lazy = [0] * length
        self.argmin = [0] * length
        self._build(1, 0, size - 1)

    def _build(self, node, left, right):
        self.argmin[node] = left
        if left == right:
            return
        middle = (left + right) // 2
        self._build(2 * node, left, middle)
        self._build(2 * node + 1, middle + 1, right)

    def _apply(self, node, value):
        self.minimum[node] += value
        self.lazy[node] += value

    def _push(self, node):
        value = self.lazy[node]
        if value:
            self._apply(2 * node, value)
            self._apply(2 * node + 1, value)
            self.lazy[node] = 0

    def _pull(self, node):
        a, b = 2 * node, 2 * node + 1
        if self.minimum[a] <= self.minimum[b]:
            self.minimum[node], self.argmin[node] = self.minimum[a], self.argmin[a]
        else:
            self.minimum[node], self.argmin[node] = self.minimum[b], self.argmin[b]

    def add(self, low, high, value, node=1, left=0, right=None):
        if right is None:
            right = self.size - 1
        if high < left or right < low:
            return
        if low <= left and right <= high:
            self._apply(node, value)
            return
        self._push(node)
        middle = (left + right) // 2
        self.add(low, high, value, 2 * node, left, middle)
        self.add(low, high, value, 2 * node + 1, middle + 1, right)
        self._pull(node)

    def query(self, low, high, node=1, left=0, right=None):
        if right is None:
            right = self.size - 1
        if low <= left and right <= high:
            return self.minimum[node], self.argmin[node]
        self._push(node)
        middle = (left + right) // 2
        candidates = []
        if low <= middle:
            candidates.append(self.query(low, high, 2 * node, left, middle))
        if high > middle:
            candidates.append(self.query(low, high, 2 * node + 1, middle + 1, right))
        return min(candidates)


def least_charge(L, B, t, atoms, threshold_atoms, scale):
    """Least exact charge at one direction, without allocating the dense event grid."""
    c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
    half = B / 2
    domain = centre_domain(L, B, c, s)
    point_records = [(c * x + s * y, -s * x + c * y, w) for x, y, w in atoms]
    threshold_records = [
        (tuple((c * x + s * y, -s * x + c * y) for x, y in points), k, w)
        for points, k, w in threshold_atoms
    ]
    all_points = [(u, v) for u, v, _ in point_records]
    all_points.extend(point for points, _, _ in threshold_records for point in points)
    umin, umax = min(u for u, _ in domain), max(u for u, _ in domain)
    vmin, vmax = min(v for _, v in domain), max(v for _, v in domain)
    U = sorted(
        {u - half for u, _ in all_points} | {u + half for u, _ in all_points} | {umin, umax}
    )
    V = sorted(
        {v - half for _, v in all_points} | {v + half for _, v in all_points} | {vmin, vmax}
    )
    ui, vi = {value: i for i, value in enumerate(U)}, {value: i for i, value in enumerate(V)}

    events = defaultdict(list)

    def rectangle(u0, u1, v0, v1, weight):
        if u0 < u1 and v0 < v1 and weight:
            j0, j1 = vi[v0], vi[v1]
            events[ui[u0]].append((j0, j1, weight))
            events[ui[u1]].append((j0, j1, -weight))

    for u, v, w in point_records:
        rectangle(u - half, u + half, v - half, v + half, int(w * scale))
    for points, k, w in threshold_records:
        scaled = int(w * scale)
        for size, coefficient in expansion_terms(len(points), k):
            for subset in combinations(points, size):
                u0 = max(u - half for u, _ in subset)
                u1 = min(u + half for u, _ in subset)
                v0 = max(v - half for _, v in subset)
                v1 = min(v + half for _, v in subset)
                rectangle(u0, u1, v0, v1, coefficient * scaled)

    tree = RangeMinimum(len(V) - 1)
    best = None
    best_cell = None
    cells = 0
    for i, (u0, u1) in enumerate(pairwise(U)):
        for j0, j1, weight in events.get(i, ()):
            tree.add(j0, j1 - 1, weight)
        if u1 <= umin or u0 >= umax:
            continue
        slab = clip(clip(domain, u0, greater=True), u1, greater=False)
        if not slab:
            continue
        low, high = min(v for _, v in slab), max(v for _, v in slab)
        if high <= low:
            continue
        j0 = max(0, bisect_right(V, low) - 1)
        j1 = min(len(V) - 2, bisect_left(V, high) - 1)
        score, j = tree.query(j0, j1)
        if best is None or score < best:
            best, best_cell = score, (i, j)
        cells += max(0, j1 - j0 + 1)
    if best is None or best_cell is None:
        raise ValueError("the centre domain produced no reachable event cell")
    i, j = best_cell
    witness = cell_witness(domain, U[i], U[i + 1], V[j], V[j + 1])
    direct = exact_charge(atoms, threshold_atoms, c, s, half, witness)
    if direct != Fraction(best, scale):
        raise AssertionError(
            f"slab score {Fraction(best, scale)} disagrees with direct charge {direct}"
        )
    return Fraction(best, scale), witness, cells


def sweep(L, B, T, K, atoms, threshold_atoms):
    scale = lcm(
        *(w.denominator for _, _, w in atoms), *(w.denominator for _, _, w in threshold_atoms)
    )
    found = []
    cells = 0
    for k in range(K + 1):
        t = T * k / K
        least, witness, count = least_charge(L, B, t, atoms, threshold_atoms, scale)
        found.append((least, k, t, witness))
        cells += count
        print(".", end="", file=sys.stderr, flush=True)
    least, k, t, witness = min(found)
    return least, k, t, witness, cells


def check_certificate(raw):
    record, n, L, B, T, K, atoms, threshold_atoms, declared = load_certificate(raw)
    verdicts = []

    def report(name, detail, holds):
        verdicts.append(holds)
        print(f"{name} {'holds' if holds else 'fails'}: {detail}", flush=True)

    detail, holds = point_symmetry(atoms, L)
    report("Condition 1", detail, holds)
    detail, holds = threshold_symmetry(threshold_atoms, L)
    report("Condition 1'", detail, holds)
    point_mass = sum((w for _, _, w in atoms), start=Fraction())
    threshold_budget = sum(
        (w * (len(points) // k) for points, k, w in threshold_atoms), start=Fraction()
    )
    total_budget = point_mass + threshold_budget
    report("Condition 2'", f"budget {total_budget} against n = {n}", total_budget < n)
    arc_slack = T * T + 2 * T - 1
    report("Condition 3", f"T^2 + 2T - 1 = {arc_slack}", arc_slack >= 0)
    tangents = tuple(T * k / K for k in range(K + 1))
    D = max((b - a) / (1 + a * b) for a, b in pairwise(tangents))
    containment = B * (1 + D)
    report("Condition 4", f"D = {D}; B(1 + D) = {containment}", containment < 1)
    least = None
    if all(verdicts):
        least, k, t, witness, cells = sweep(L, B, T, K, atoms, threshold_atoms)
        report(
            "Condition 5'",
            f"least charge {least} at direction {k} (t = {t}), rotated centre {witness}; {cells} cells",
            least >= 1,
        )
    else:
        print("Condition 5' not evaluated: a closed-form condition failed", flush=True)

    expected_claim = f"s({n}) >= {L}"
    expected = {
        "claim": expected_claim,
        "point_mass": point_mass,
        "threshold_budget": threshold_budget,
        "total_budget": total_budget,
    }
    wrong = [name for name, value in expected.items() if declared[name] != value]
    if (
        declared["least_cell_charge"] is not None
        and least is not None
        and declared["least_cell_charge"] != least
    ):
        wrong.append("least_cell_charge")
    report(
        "Declarations",
        "all computed fields agree" if not wrong else f"wrong fields: {', '.join(wrong)}",
        not wrong,
    )
    return all(verdicts), record, (n, L, B, T, K, total_budget, least, D)


def reduced_polynomial(square):
    a, b = square.denominator, square.numerator
    common = gcd(a, b)
    return a // common, b // common


def canonical_radical(coefficient, radicand):
    if coefficient.denominator == 1:
        prefix = "" if coefficient.numerator == 1 else f"{coefficient.numerator}*"
        return f"{prefix}sqrt({radicand})"
    return f"{coefficient.numerator}*sqrt({radicand})/{coefficient.denominator}"


def check_limit_record(raw, certificate_raw, certificate, facts):
    record = parse_json(raw)
    if not isinstance(record, dict):
        raise TypeError("dilation limit record must be one JSON object")
    n, L, B, _T, _K, total_budget, least, D = facts
    source = record["source"]
    conclusion = record["conclusion"]
    family = record["strict_dilation_family"]
    sharpened = record["sharpened_containment"]
    proof = record["proof"]
    if not all(
        isinstance(value, dict) for value in (source, conclusion, family, sharpened, proof)
    ):
        raise TypeError("dilation limit sections must be JSON objects")
    failures = []

    def same(name, actual, expected):
        if actual != expected:
            failures.append(f"{name}: {actual!r} != {expected!r}")

    same("schema", record.get("schema"), "packing.squares:FractionalDilationLimitCorollary/v3")
    same("source sha256", source.get("sha256"), hashlib.sha256(certificate_raw).hexdigest())
    same("source variant", source.get("variant"), "threshold")
    same("source n", source.get("n"), n)
    same("source outer_side", source.get("outer_side"), str(L))
    same("source square_side", source.get("square_side"), str(B))
    same("source half_gap_tangent", source.get("half_gap_tangent"), str(D))
    same("source total_budget", source.get("total_budget"), str(total_budget))
    same("source minimum_cell_charge", source.get("minimum_cell_charge"), str(least))
    same("source point_atoms", source.get("point_atoms"), len(certificate["atoms"]))
    same(
        "source threshold_atoms",
        source.get("threshold_atoms"),
        len(certificate["threshold_atoms"]),
    )
    same("source coarse_containment", source.get("coarse_containment"), str(B * (1 + D)))

    factor_squared = (1 + D * D) / (B * B * (1 + D) * (1 + D))
    side_squared = L * L * factor_squared
    gap_denominator = D.denominator
    radicand = D.numerator * D.numerator + gap_denominator * gap_denominator
    coefficient = L * B.denominator / (B.numerator * (D.numerator + D.denominator))
    exact_side = canonical_radical(coefficient, radicand)
    factor = canonical_radical(
        Fraction(B.denominator, B.numerator * (D.numerator + D.denominator)), radicand
    )
    a, b = reduced_polynomial(side_squared)
    fa, fb = reduced_polynomial(factor_squared)
    same("factor_supremum_squared", family.get("factor_supremum_squared"), str(factor_squared))
    same("factor_supremum", family.get("factor_supremum"), factor)
    same(
        "factor polynomial",
        family.get("factor_supremum_defining_polynomial"),
        f"{fa}*x^2 - {fb}",
    )
    same(
        "factor irrational",
        family.get("factor_supremum_irrational"),
        isqrt(radicand) ** 2 != radicand,
    )
    same(
        "factor domain",
        family.get("factor_domain"),
        f"q in Q with q > 0 and q^2 < {factor_squared}",
    )
    same(
        "scaled containment test",
        family.get("scaled_containment_test"),
        "q^2 B^2 (1 + D)^2 < 1 + D^2; this rational inequality is equivalent to strict geometric containment",
    )
    same("bounded_side_squared", conclusion.get("bounded_side_squared"), str(side_squared))
    same("bounded_side", conclusion.get("bounded_side"), exact_side)
    same(
        "bounded-side polynomial",
        conclusion.get("bounded_side_defining_polynomial"),
        f"{a}*x^2 - {b}",
    )
    same("relation", conclusion.get("relation"), ">=")
    same("endpoint_certificate", conclusion.get("endpoint_certificate"), False)
    same("requires_compactness", proof.get("requires_compactness"), False)
    expected_left = B * B * (1 + D) * (1 + D)
    expected_right = 1 + D * D
    same(
        "gap domain",
        sharpened.get("gap_domain"),
        f"0 <= t <= D = {D} < 1",
    )
    same(
        "support identity",
        sharpened.get("identity"),
        "cos(d) + sin(d) = (1 + t) / sqrt(1 + t^2), where t = tan(d)",
    )
    same(
        "monotonicity identity",
        sharpened.get("monotonicity_identity"),
        "(1 + D)^2(1 + t^2) - (1 + t)^2(1 + D^2) = 2(D - t)(1 - Dt) >= 0",
    )
    same("source gap below one", sharpened.get("source_gap_below_one"), D < 1)
    same(
        "strict test left",
        sharpened.get("strict_factor_test_left_multiplier"),
        str(expected_left),
    )
    same("strict test right", sharpened.get("strict_factor_test_right"), str(expected_right))
    same(
        "strict factor test",
        sharpened.get("strict_factor_test"),
        f"q^2 * {expected_left} < {expected_right}",
    )
    if certificate.get("claim") != f"s({n}) >= {L}":
        failures.append("source certificate's own claim is wrong")
    print(
        "Dilation limit "
        + (
            "holds: exact factor, side, polynomial, strict family, and endpoint status agree"
            if not failures
            else "fails: " + "; ".join(failures)
        ),
        flush=True,
    )
    return not failures, f"s({n}) >= {exact_side}"


def main(argv: Sequence[str] | None = None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "claim", help="a threshold certificate JSON file or a generated claim Markdown file"
    )
    args = parser.parse_args(argv)
    try:
        cert_raw, limit_raw, declarations = read_input(args.claim)
        for name, raw in (("certificate", cert_raw), ("limit record", limit_raw)):
            if raw is None:
                continue
            digest, size = hashlib.sha256(raw).hexdigest(), len(raw)
            if name in declarations and declarations[name] != (digest, size):
                raise ValueError(f"{name} byte or SHA-256 declaration does not match its block")
            print(f"{name.title()} bytes: {size}; SHA-256: {digest}")
        holds, certificate, facts = check_certificate(cert_raw)
        theorem = f"s({facts[0]}) >= {facts[1]}"
        if holds and limit_raw is not None:
            holds, theorem = check_limit_record(limit_raw, cert_raw, certificate, facts)
        print(f"VERIFIED: {theorem}" if holds else "REFUSED")
        return 0 if holds else 1
    except AssertionError as error:
        print(f"INTERNAL ERROR: {error}")
        return 2
    except (
        AttributeError,
        IndexError,
        OSError,
        UnicodeError,
        KeyError,
        TypeError,
        ValueError,
        ZeroDivisionError,
    ) as error:
        print(f"REFUSED: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
