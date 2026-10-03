"""Exact endpoint geometry over an independently verified H-255 root box.

The symbolic stage proves every asserted equality as a rational-function identity.
The interval stage proves one strict separating axis for every other square pair.
Neither stage searches or adjusts the preregistered two slider coordinates.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from dataclasses import dataclass
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from typing import Any, Self

import sympy as sp

from devtools.check_n17_contact_chart import ANCHORS, CONTACTS, SOURCE
from devtools.check_n17_root_certificate import (
    CertificateError,
    n17_polynomials,
)
from devtools.check_n17_root_certificate import (
    check as check_root,
)

ZERO, ONE, HALF = Q(0), Q(1), Q(1, 2)
EX, EY = "ex", "ey"
WALLS = ("left", "right", "bottom", "top")
AXIS_LABELS = frozenset((*range(1, 9), 15, 17))
THETA_LABELS = frozenset(range(9, 15))
ANCHOR_SET = frozenset(ANCHORS)
CONTACT_SET = frozenset(tuple(sorted((left, right))) for left, right, _, _ in CONTACTS)
ZERO_PAIRS = CONTACT_SET | {(2, 3)}
IDENTITY_MANIFEST = {
    tuple(sorted((left, right))): {
        "reason": "defining" if index < 17 else ("F1", "F2", "F3")[index - 17],
        "axes": [{"from": left, "to": right, "axis": axis}],
    }
    for index, (left, right, axis, _) in enumerate(CONTACTS)
}
IDENTITY_MANIFEST[(2, 3)] = {
    "reason": "corner",
    "axes": [
        {"from": 3, "to": 2, "axis": EX},
        {"from": 2, "to": 3, "axis": EY},
    ],
}
MAX_BYTES = 10 * 1024 * 1024
MAX_DECIMAL_DIGITS = 100_000
REPO = Path(__file__).resolve().parents[2]
FROZEN_ROOT_REF = (
    "7866e2623:packing/campaign/series/series-000-smoke-and-calibration/"
    "results/exp-237-n17-polynomial-root/run-001/certificate.json"
)


@dataclass(frozen=True)
class Box:
    """Closed interval with exact rational endpoints and outward arithmetic."""

    lo: Q
    hi: Q

    def __post_init__(self) -> None:
        if type(self.lo) is not Q or type(self.hi) is not Q or self.lo > self.hi:
            raise ValueError("invalid exact interval")

    @classmethod
    def point(cls, value: int | Q) -> Self:
        if type(value) not in (int, Q):
            raise ValueError("interval point must be exact integer or Fraction")
        return cls(Q(value), Q(value))

    @staticmethod
    def cast(value: Box | int | Q) -> Box:
        return value if isinstance(value, Box) else Box.point(value)

    def __add__(self, other: Box | int | Q) -> Box:
        rhs = self.cast(other)
        return Box(self.lo + rhs.lo, self.hi + rhs.hi)

    def __radd__(self, other: Box | int | Q) -> Box:
        return self + other

    def __neg__(self) -> Box:
        return Box(-self.hi, -self.lo)

    def __sub__(self, other: Box | int | Q) -> Box:
        return self + -self.cast(other)

    def __rsub__(self, other: Box | int | Q) -> Box:
        return self.cast(other) - self

    def __mul__(self, other: Box | int | Q) -> Box:
        rhs = self.cast(other)
        values = (self.lo * rhs.lo, self.lo * rhs.hi, self.hi * rhs.lo, self.hi * rhs.hi)
        return Box(min(values), max(values))

    def __rmul__(self, other: Box | int | Q) -> Box:
        return self * other

    def reciprocal(self) -> Box:
        if self.lo <= 0 <= self.hi:
            raise ValueError("interval denominator includes zero")
        return Box(1 / self.hi, 1 / self.lo)

    def __truediv__(self, other: Box | int | Q) -> Box:
        return self * self.cast(other).reciprocal()

    def __rtruediv__(self, other: Box | int | Q) -> Box:
        return self.cast(other) / self

    def as_json(self) -> list[str]:
        return [_fraction_string(self.lo), _fraction_string(self.hi)]

    def absolute(self) -> Box:
        if self.lo <= 0 <= self.hi:
            return Box(ZERO, max(-self.lo, self.hi))
        return Box(min(abs(self.lo), abs(self.hi)), max(abs(self.lo), abs(self.hi)))


def _integer_decimal(value: int) -> str:
    """Serialize large exact integers without Python's unrelated repr digit cap."""
    sign = "-" if value < 0 else ""
    remaining = abs(value)
    chunks: list[int] = []
    while remaining >= 10**9:
        remaining, chunk = divmod(remaining, 10**9)
        chunks.append(chunk)
        if len(chunks) * 9 > MAX_DECIMAL_DIGITS:
            raise ValueError("exact decimal exceeds serialization cap")
    result = sign + str(remaining) + "".join(f"{chunk:09d}" for chunk in reversed(chunks))
    if len(result.lstrip("-")) > MAX_DECIMAL_DIGITS:
        raise ValueError("exact decimal exceeds serialization cap")
    return result


def _fraction_string(value: Q) -> str:
    top = _integer_decimal(value.numerator)
    if value.denominator == 1:
        return top
    return f"{top}/{_integer_decimal(value.denominator)}"


def _dot(a: tuple[Any, Any], b: tuple[Any, Any]) -> Any:
    return a[0] * b[0] + a[1] * b[1]


def _minus(a: tuple[Any, Any], b: tuple[Any, Any]) -> tuple[Any, Any]:
    return a[0] - b[0], a[1] - b[1]


def _class(label: int) -> str:
    if label in AXIS_LABELS:
        return "axis"
    if label in THETA_LABELS:
        return "theta"
    if label == 16:
        return "beta"
    raise ValueError("square label outside 1..17")


def _layout(
    t: Any, b: Any, half: Any
) -> tuple[Any, dict[str, Any], tuple[tuple[Any, Any], ...]]:
    """The H-254 centres with the fixed interior slider barycentre."""
    d_t, d_b = 1 + t * t, 1 + b * b
    c, s = (1 - t * t) / d_t, 2 * t / d_t
    d, e = (1 - b * b) / d_b, 2 * b / d_b
    k_denom = 1 + 2 * t - t * t
    side = (6 + 4 * t) / k_denom
    h, k = (c + s) / 2, (d + e) / 2
    alpha, gamma = c * d - s * e, c * e + s * d
    x = half + (2 + c * s + 3 * s - s * side) / c
    y = 3 * half + (2 + 3 * c - c * side) / s
    aa = d * (x + half) - e * (side - 1) + half
    bb = (d + e) * (side - 1) - half
    u10, v10 = 3 * half + c * s + 2 * s, c * (side - 1) - s - half
    u11, v11 = c + 2 * s + half, 2 * c + (c * c - s * s) / 2 - 1
    u12, v12 = u11 + 1, v10 - 1
    u13 = 2 * c + s + half
    u14, v14 = u13 + 1, v10 - 2
    r, hh = side - 3 * half, v11 - 1
    ell = c + s / 2 + half
    slack = c * (c + 4 - side)
    lambda6, lambda13 = r - slack / (3 * s), hh - slack / 3

    def rotate(uu: Any, vv: Any) -> tuple[Any, Any]:
        return c * uu - s * vv, s * uu + c * vv

    centres = (
        (half, half),
        (3 * half, half),
        (half, 3 * half),
        (half, side - half),
        (side - half, half),
        (lambda6, half),
        (side - half, 3 * half),
        (side - half, side - half),
        (h, 2 + h),
        rotate(u10, v10),
        rotate(u11, v11),
        rotate(u12, v12),
        rotate(u13, lambda13),
        rotate(u14, v14),
        (x, side - half),
        (d * aa + e * bb, -e * aa + d * bb),
        (side - half, y),
    )
    aux = {
        "c": c,
        "s": s,
        "d": d,
        "e": e,
        "alpha": alpha,
        "gamma": gamma,
        "h": h,
        "k": k,
        "X": x,
        "Y": y,
        "A": aa,
        "B": bb,
        "u": (c, s),
        "v": (-s, c),
        "w": (s, -c),
        "p": (d, -e),
        "q": (e, d),
        "ex": (1, 0),
        "ey": (0, 1),
        "R": r,
        "H": hh,
        "L": ell,
        "T": slack,
        "lambda6": lambda6,
        "lambda13": lambda13,
    }
    return side, aux, centres


def _support(label: int, axis: str, aux: dict[str, Any], half: Any) -> Any:
    square_class = _class(label)
    axis_class = "axis" if axis in (EX, EY) else "theta" if axis in ("u", "v", "w") else "beta"
    if square_class == axis_class:
        return half
    if square_class == "axis":
        return aux["h"] if axis_class == "theta" else aux["k"]
    if axis_class == "axis":
        return aux["h"] if square_class == "theta" else aux["k"]
    return (aux["alpha"] + aux["gamma"]) / 2


def _support_interval(label: int, axis: str, aux: dict[str, Any]) -> Box:
    """Enclose a unit-square support using rigorous absolute projections."""
    kind = _class(label)
    basis = (
        ((1, 0), (0, 1))
        if kind == "axis"
        else (aux["u"], aux["v"])
        if kind == "theta"
        else (aux["p"], aux["q"])
    )
    first, second = (Box.cast(_dot(aux[axis], direction)).absolute() for direction in basis)
    return (first + second) / 2


def _wall_gap(
    label: int,
    wall: str,
    side: Any,
    aux: dict[str, Any],
    centres: tuple[tuple[Any, Any], ...],
    *,
    half: Any,
) -> Any:
    x, y = centres[label - 1]
    if wall == "left":
        return x - _support(label, EX, aux, half)
    if wall == "right":
        return side - x - _support(label, EX, aux, half)
    if wall == "bottom":
        return y - _support(label, EY, aux, half)
    if wall == "top":
        return side - y - _support(label, EY, aux, half)
    raise ValueError("unknown wall")


def _wall_gap_interval(
    label: int, wall: str, side: Box, aux: dict[str, Any], centres: tuple[tuple[Any, Any], ...]
) -> Box:
    x, y = centres[label - 1]
    axis = EX if wall in ("left", "right") else EY
    extent = _support_interval(label, axis, aux)
    return {
        "left": x - extent,
        "right": side - x - extent,
        "bottom": y - extent,
        "top": side - y - extent,
    }[wall]


def _directed_gap(
    left: int,
    right: int,
    axis: str,
    aux: dict[str, Any],
    centres: tuple[tuple[Any, Any], ...],
    *,
    half: Any,
) -> Any:
    delta = _minus(centres[right - 1], centres[left - 1])
    return (
        _dot(aux[axis], delta)
        - _support(left, axis, aux, half)
        - _support(right, axis, aux, half)
    )


def _directed_gap_interval(
    left: int,
    right: int,
    axis: str,
    aux: dict[str, Any],
    centres: tuple[tuple[Any, Any], ...],
    *,
    direction: int,
) -> Box:
    delta = _minus(centres[right - 1], centres[left - 1])
    return (
        direction * _dot(aux[axis], delta)
        - _support_interval(left, axis, aux)
        - _support_interval(right, axis, aux)
    )


def _zero(expression: Any, name: str) -> None:
    if sp.cancel(expression) != 0:
        raise ValueError(f"symbolic identity failed: {name}")


@lru_cache(maxsize=1)
def symbolic_identities() -> dict[str, Any]:
    """Recheck chart identities exactly, without a root or source sample."""
    t, b = sp.symbols("t b", real=True)
    side, aux, centres = _layout(t, b, sp.Rational(1, 2))
    for label, wall in ANCHORS:
        _zero(
            _wall_gap(label, wall, side, aux, centres, half=sp.Rational(1, 2)),
            f"wall.{label}.{wall}",
        )
    for left, right, axis, _ in CONTACTS[:17]:
        _zero(
            _directed_gap(left, right, axis, aux, centres, half=sp.Rational(1, 2)),
            f"pair.{left}.{right}",
        )
    _zero(_directed_gap(2, 3, "ey", aux, centres, half=sp.Rational(1, 2)), "pair.2.3.ey")
    _zero(_directed_gap(3, 2, "ex", aux, centres, half=sp.Rational(1, 2)), "pair.2.3.ex")
    c, s, d, e = (aux[key] for key in ("c", "s", "d", "e"))
    _zero(_dot(aux["u"], aux["u"]) - 1, "basis.theta.unit")
    _zero(_dot(aux["p"], aux["p"]) - 1, "basis.beta.unit")
    _zero(_dot(aux["u"], aux["v"]), "basis.theta.orthogonal")
    _zero(_dot(aux["p"], aux["q"]), "basis.beta.orthogonal")
    _zero(_dot(aux["v"], aux["v"]) - 1, "basis.theta.second_unit")
    _zero(_dot(aux["q"], aux["q"]) - 1, "basis.beta.second_unit")
    f1 = c * (side - 3) + s * (side - 2) - 3
    f2 = (
        d * (side - aux["X"] - sp.Rational(3, 2))
        - e * (aux["Y"] - side + sp.Rational(3, 2))
        - 1
    )
    f3 = (
        aux["alpha"] * (aux["A"] - sp.Rational(1, 2))
        + aux["gamma"] * (aux["B"] - sp.Rational(1, 2))
        - (c + 2 * s + 2)
    )
    _zero(f1, "F1.side")
    for (left, right, axis, _), fi in zip(CONTACTS[-3:], (f1, f2, f3), strict=True):
        _zero(
            _directed_gap(left, right, axis, aux, centres, half=sp.Rational(1, 2)) - fi,
            f"closing.{left}.{right}",
        )
    d_t, d_b, ell = 1 + t * t, 1 + b * b, (1 + t) * (1 + t * t)
    n_alpha = (1 - t * t) * (1 - b * b) - 4 * t * b
    pi2 = 2 * t * (1 - t) * (1 - b * b) + (1 - t) ** 2 * ell * b - t * ell * d_b
    pi3 = (
        (1 - t * t) * d_t * d_b**2
        - (1 + t) * d_t * d_b * (b * (1 - t * t) + t * (1 - b * b))
        - (1 - t) * (1 - b * b) * n_alpha
    )
    for name, local, independent in zip(
        ("Pi2", "Pi3"), (pi2, pi3), n17_polynomials(), strict=True
    ):
        expected = sum(
            (coefficient * t**i * b**j for (i, j), coefficient in independent.items()),
            sp.Integer(0),
        )
        _zero(local - expected, f"{name}.checker_binding")
    _zero(f2 - pi2 / (t * ell * d_b), "F2.normalization")
    _zero(f3 - 2 * pi3 / ((1 + t) * d_t**2 * d_b**2), "F3.normalization")
    _zero(aux["H"] + s * aux["R"] - aux["L"] - aux["T"], "slider.triangle")
    return {
        "wall_identities": len(ANCHORS),
        "pair_identities": len(ZERO_PAIRS),
        "normalizations": 3,
        "slider_identity": True,
    }


AXIS_ORDER = (EX, EY, "u", "v", "p", "q")


def validate_coverage(walls: list[dict[str, Any]], pairs: list[dict[str, Any]]) -> None:
    """Require each geometric obligation exactly once and with its frozen kind."""
    for row in walls:
        if (
            type(row["label"]) is not int
            or type(row["wall"]) is not str
            or type(row["kind"]) is not str
        ):
            raise ValueError("malformed wall coverage label")
    for row in pairs:
        if (
            type(row["left"]) is not int
            or type(row["right"]) is not int
            or type(row["kind"]) is not str
        ):
            raise ValueError("malformed pair coverage label")
    wall_keys = [(row["label"], row["wall"]) for row in walls]
    pair_keys = [(row["left"], row["right"]) for row in pairs]
    expected_walls = {(label, wall) for label in range(1, 18) for wall in WALLS}
    expected_pairs = set(itertools.combinations(range(1, 18), 2))
    if len(wall_keys) != 68 or set(wall_keys) != expected_walls:
        raise ValueError("incomplete or duplicate wall coverage")
    if len(pair_keys) != 136 or set(pair_keys) != expected_pairs:
        raise ValueError("incomplete or duplicate pair coverage")
    for row in walls:
        expected_kind = "identity" if (row["label"], row["wall"]) in ANCHOR_SET else "strict"
        if row["kind"] != expected_kind:
            raise ValueError("wall obligation kind differs from frozen roster")
    for row in pairs:
        expected_kind = "identity" if (row["left"], row["right"]) in ZERO_PAIRS else "strict"
        if row["kind"] != expected_kind:
            raise ValueError("pair obligation kind differs from frozen roster")


def interval_geometry(midpoint: tuple[Q, Q], radii: tuple[Q, Q]) -> dict[str, Any]:
    """A conditional feasibility screen; caller must separately verify root existence."""
    if (
        len(midpoint) != 2
        or len(radii) != 2
        or any(type(value) is not Q for value in (*midpoint, *radii))
        or any(radius <= 0 for radius in radii)
    ):
        raise ValueError("expected exact two-dimensional midpoint and positive radii")
    t, b = (
        Box(value - radius, value + radius)
        for value, radius in zip(midpoint, radii, strict=True)
    )
    side, aux, centres = _layout(t, b, Box.point(HALF))
    d_t, d_b = 1 + t * t, 1 + b * b
    k = 1 + 2 * t - t * t
    ell = (1 + t) * d_t
    guards = {name: aux[name] for name in ("c", "s", "d", "e", "alpha", "gamma", "T")}
    guards.update({"D": d_t, "E": d_b, "K": k, "poly_L": ell, "one_plus_t": 1 + t})
    guards.update({"t": t, "b": b, "side": side})
    failed: list[str] = []
    if not (Q(36, 100) < t.lo and t.hi < Q(37, 100)):
        failed.append("domain.t")
    if not (Q(33, 100) < b.lo and b.hi < Q(34, 100)):
        failed.append("domain.b")
    if not (Q(4675, 1000) < side.lo and side.hi < Q(4676, 1000)):
        failed.append("domain.side")
    for name, box in guards.items():
        if box.lo <= 0:
            failed.append(f"positive.{name}")
    walls: list[dict[str, Any]] = []
    for label in range(1, 18):
        for wall in WALLS:
            gap = _wall_gap_interval(label, wall, side, aux, centres)
            identity = (label, wall) in ANCHOR_SET
            passed = identity or gap.lo > 0
            if not passed:
                failed.append(f"wall.{label}.{wall}")
            walls.append(
                {
                    "label": label,
                    "wall": wall,
                    "kind": "identity" if identity else "strict",
                    "bound": ["0", "0"] if identity else gap.as_json(),
                    "bound_scope": "certified_root" if identity else "whole_box",
                    "passed": passed,
                }
            )
    pairs: list[dict[str, Any]] = []
    for left, right in itertools.combinations(range(1, 18), 2):
        if (left, right) in ZERO_PAIRS:
            pairs.append(
                {
                    "left": left,
                    "right": right,
                    "kind": "identity",
                    "identity": IDENTITY_MANIFEST[left, right],
                    "bound": ["0", "0"],
                    "bound_scope": "certified_root",
                    "passed": True,
                }
            )
            continue
        chosen: tuple[str, str, Box] | None = None
        for axis in AXIS_ORDER:
            for direction, sign in (("forward", 1), ("reverse", -1)):
                gap = _directed_gap_interval(left, right, axis, aux, centres, direction=sign)
                if gap.lo > 0:
                    chosen = axis, direction, gap
                    break
            if chosen is not None:
                break
        if chosen is None:
            failed.append(f"pair.{left}.{right}")
            pairs.append(
                {
                    "left": left,
                    "right": right,
                    "kind": "strict",
                    "axis": None,
                    "direction": None,
                    "bound": None,
                    "bound_scope": "whole_box",
                    "passed": False,
                }
            )
        else:
            axis, direction, gap = chosen
            pairs.append(
                {
                    "left": left,
                    "right": right,
                    "kind": "strict",
                    "axis": axis,
                    "direction": direction,
                    "bound": gap.as_json(),
                    "bound_scope": "whole_box",
                    "passed": True,
                }
            )
    validate_coverage(walls, pairs)
    if len(ANCHOR_SET) != 15 or len(ZERO_PAIRS) != 21:
        raise ValueError("incomplete endpoint geometry roster")
    return {
        "schema": "n17-endpoint-geometry/v1",
        "box": {
            "midpoint": [_fraction_string(value) for value in midpoint],
            "inclusion_bounds": [_fraction_string(value) for value in radii],
        },
        "side": side.as_json(),
        "sliders": {key: aux[key].as_json() for key in ("lambda6", "lambda13", "T")},
        "guards": {key: value.as_json() for key, value in guards.items()},
        "walls": walls,
        "pairs": pairs,
        "counts": {
            "walls": 68,
            "wall_identities": 15,
            "wall_strict": 53,
            "pairs": 136,
            "pair_identities": 21,
            "pair_strict": 115,
        },
        "geometry_passed": not failed,
        "failures": failed,
    }


def _read_limited(path: Path) -> bytes:
    with path.open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("input exceeds 10 MiB")
    return raw


def _object_unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def require_retained_path(path: Path, reference: str) -> None:
    """Refuse a file other than the retained one a `REVISION:PATH` reference names.

    A retained certificate is identified by the revision it was accepted at and its
    repository-relative path, and a receipt names it by that reference (OR-16). This
    checks only that the file read is that file, so the name in the receipt is true.
    Its content is Git's to keep and the reader's to check: nothing compares its bytes
    with a historical blob, and a re-serialized certificate is still the certificate.
    """
    relative = reference.partition(":")[2]
    if not relative or path.resolve() != (REPO / relative).resolve():
        raise ValueError(f"expected the retained {relative or reference}, not {path}")


def _encode_receipt(result: dict[str, Any]) -> str:
    encoded = json.dumps(result, sort_keys=True)
    if len(encoded.encode()) > MAX_BYTES:
        raise ValueError("endpoint receipt exceeds 10 MiB")
    return encoded


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path, help="accepted H-255 root certificate JSON")
    parser.add_argument("--source", type=Path, default=SOURCE)
    args = parser.parse_args(argv)
    started = time.monotonic()
    try:
        # The root is named by revision and path; `check_root` below decides its content.
        require_retained_path(args.certificate, FROZEN_ROOT_REF)
        source = _read_limited(args.source)
        certificate_raw = _read_limited(args.certificate)
        root_document = json.loads(certificate_raw, object_pairs_hook=_object_unique)
        root_started = time.monotonic()
        root_receipt = check_root(root_document, source)
        root_seconds = time.monotonic() - root_started
        midpoint_values = root_document["box"]["midpoint"]
        inclusion_values = root_document["inclusion_bounds"]
        midpoint = (Q(midpoint_values[0]), Q(midpoint_values[1]))
        radii = (Q(inclusion_values[0]), Q(inclusion_values[1]))
        symbolic_started = time.monotonic()
        identities = symbolic_identities()
        symbolic_seconds = time.monotonic() - symbolic_started
        interval_started = time.monotonic()
        geometry = interval_geometry(midpoint, radii)
        interval_seconds = time.monotonic() - interval_started
        result = {
            "schema": "n17-endpoint-feasibility/v1",
            "root_certificate_git_ref": FROZEN_ROOT_REF,
            "source_sha256": hashlib.sha256(source).hexdigest(),
            "root_verification": root_receipt,
            "identities": identities,
            "geometry": geometry,
            "criterion_passed": geometry["geometry_passed"],
            "timing_seconds": {
                "total": time.monotonic() - started,
                "root_checker": root_seconds,
                "symbolic": symbolic_seconds,
                "interval": interval_seconds,
                "orchestration": time.monotonic()
                - started
                - root_seconds
                - symbolic_seconds
                - interval_seconds,
            },
        }
        print(_encode_receipt(result))
        return 0 if result["criterion_passed"] else 1
    except (
        CertificateError,
        ValueError,
        OSError,
        KeyError,
        IndexError,
        TypeError,
        RecursionError,
    ) as error:
        print(
            json.dumps(
                {
                    "schema": "n17-endpoint-feasibility/v1",
                    "criterion_passed": False,
                    "error": str(error),
                },
                sort_keys=True,
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
