"""Audit the retained H256 receipt with independent exact interval arithmetic.

This is a receipt audit, not a standalone proof checker. It trusts the previously
accepted H255 root certificate and the separately reviewed analytic identities.
It reads that root from its retained path, requires the receipt to name it by the
revision and path it was accepted at (no byte comparison with a Git blob, OR-16),
checks the root's metadata against the source, checks the complete identity manifest,
and independently recomputes every recorded strict wall and pair bound.
No endpoint-producer or root-checker arithmetic is imported or executed.

The tuple arithmetic and reconstruction retain the independent output review's
algorithm; coverage extends its nine selected gaps to all 168 strict obligations.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
import time
from dataclasses import dataclass
from decimal import ROUND_CEILING, ROUND_FLOOR, Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

REPO = Path(__file__).resolve().parents[2]
RESULTS = "packing/campaign/series/series-000-smoke-and-calibration/results"
ROOT_RUN = f"{RESULTS}/exp-237-n17-polynomial-root/run-001"
ENDPOINT_RUN = f"{RESULTS}/exp-238-n17-endpoint-feasibility/run-001"
ROOT_REF = f"7866e2623:{ROOT_RUN}/certificate.json"
EXECUTION_COMMIT = "f77b3e0a7fdfec83ec7a4f6068404e23d91508b7"
SOURCE = (
    "packing/resources/web/n17-kleddamag-certified-bound-2026-09-21/"
    "kleddamag-17-squares-certified-bound/upper-packing-certificate.json"
)
# A real boundary (OR-16): SOURCE is Kleddamag's downloaded certified-bound release, and
# this is the digest its review pinned, so a retained copy that is not upstream's bytes
# is refused. It is not a check of a file this repository wrote.
SOURCE_SHA = "24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7"
LABELS = [1, 5, 2, 6, 3, 7, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
MAX_BYTES = 10 * 1024 * 1024
MAX_DIGITS = 100000
LITERAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")
Interval = tuple[Fraction, Fraction]
Vector = tuple[Interval, Interval]
ANCHORS = {
    (1, "left"),
    (1, "bottom"),
    (2, "bottom"),
    (3, "left"),
    (4, "left"),
    (4, "top"),
    (5, "right"),
    (5, "bottom"),
    (6, "bottom"),
    (7, "right"),
    (8, "right"),
    (8, "top"),
    (9, "left"),
    (15, "top"),
    (17, "right"),
}
CONTACTS = [
    (1, 2, "ex"),
    (1, 3, "ey"),
    (5, 7, "ey"),
    (3, 9, "ey"),
    (9, 10, "u"),
    (4, 10, "w"),
    (3, 11, "u"),
    (9, 11, "w"),
    (11, 12, "u"),
    (10, 12, "w"),
    (2, 13, "u"),
    (13, 14, "u"),
    (12, 14, "w"),
    (10, 15, "u"),
    (14, 17, "u"),
    (15, 16, "p"),
    (16, 8, "q"),
    (14, 7, "w"),
    (16, 17, "p"),
    (12, 16, "u"),
]
COUNTS = {
    "walls": 68,
    "wall_identities": 15,
    "wall_strict": 53,
    "pairs": 136,
    "pair_identities": 21,
    "pair_strict": 115,
}


class AuditError(ValueError):
    """The receipt does not satisfy the frozen audit contract."""


def require(condition: object, label: str) -> None:
    if not condition:
        raise AuditError(label)


def exact_structure(actual: Any, expected: Any) -> bool:
    """JSON structural equality with distinct integer, Boolean and float types."""
    if type(actual) is not type(expected):
        return False
    if type(expected) is dict:
        return set(actual) == set(expected) and all(
            exact_structure(actual[key], value) for key, value in expected.items()
        )
    if type(expected) is list:
        return len(actual) == len(expected) and all(
            exact_structure(a, b) for a, b in zip(actual, expected, strict=True)
        )
    return actual == expected


def integer(text: str) -> int:
    """Parse bounded decimal chunks without changing Python's global digit limit."""
    negative = text.startswith("-")
    digits = text[1:] if negative else text
    require(
        0 < len(digits) <= MAX_DIGITS and digits.isascii() and digits.isdigit(),
        "invalid or oversized integer",
    )
    result = 0
    for start in range(0, len(digits), 9):
        part = digits[start : start + 9]
        result = result * 10 ** len(part) + int(part)
    return -result if negative else result


def rational(value: Any) -> Fraction:
    require(
        type(value) is str
        and len(value) <= 2 * MAX_DIGITS + 2
        and LITERAL.fullmatch(value) is not None,
        "invalid rational string",
    )
    top, _, bottom = value.partition("/")
    numerator, denominator = integer(top), integer(bottom) if bottom else 1
    result = Fraction(numerator, denominator)
    require(
        result.numerator == numerator
        and result.denominator == denominator
        and value != "-0"
        and not (bottom and denominator == 1),
        "noncanonical rational string",
    )
    return result


def read_interval(value: Any) -> Interval:
    require(type(value) is list and len(value) == 2, "expected interval pair")
    lo, hi = rational(value[0]), rational(value[1])
    require(lo <= hi, "reversed interval")
    return lo, hi


def point(value: int | Fraction) -> Interval:
    return Fraction(value), Fraction(value)


def add(*values: Interval) -> Interval:
    return sum((x[0] for x in values), Fraction(0)), sum((x[1] for x in values), Fraction(0))


def negate(value: Interval) -> Interval:
    return -value[1], -value[0]


def subtract(left: Interval, right: Interval) -> Interval:
    return add(left, negate(right))


def multiply(left: Interval, right: Interval) -> Interval:
    products = [a * b for a in left for b in right]
    return min(products), max(products)


def divide(left: Interval, right: Interval) -> Interval:
    require(not right[0] <= 0 <= right[1], "interval denominator contains zero")
    return multiply(left, (1 / right[1], 1 / right[0]))


def absolute(value: Interval) -> Interval:
    hi = max(abs(value[0]), abs(value[1]))
    lo = Fraction(0) if value[0] <= 0 <= value[1] else min(abs(value[0]), abs(value[1]))
    return lo, hi


def dot(left: Vector, right: Vector) -> Interval:
    return add(multiply(left[0], right[0]), multiply(left[1], right[1]))


def difference(left: Vector, right: Vector) -> Vector:
    return subtract(left[0], right[0]), subtract(left[1], right[1])


@dataclass(frozen=True)
class Layout:
    centres: dict[int, Vector]
    axes: dict[str, Vector]
    guards: dict[str, Interval]
    sliders: dict[str, Interval]
    side: Interval

    def support(self, label: int, normal: Vector) -> Interval:
        names = ("p", "q") if label == 16 else ("u", "v") if 9 <= label <= 14 else ("ex", "ey")
        return divide(
            add(*(absolute(dot(normal, self.axes[name])) for name in names)), point(2)
        )

    def pair_gap(self, left: int, right: int, axis: str, direction: str) -> Interval:
        require(axis in self.axes and direction in ("forward", "reverse"), "invalid pair axis")
        normal = self.axes[axis]
        projection = dot(normal, difference(self.centres[right], self.centres[left]))
        if direction == "reverse":
            projection = negate(projection)
        return subtract(
            subtract(projection, self.support(left, normal)), self.support(right, normal)
        )

    def wall_gap(self, label: int, wall: str) -> Interval:
        require(wall in ("left", "right", "bottom", "top"), "invalid wall")
        horizontal = wall in ("left", "right")
        coordinate = self.centres[label][0 if horizontal else 1]
        extent = self.support(label, self.axes["ex" if horizontal else "ey"])
        return (
            subtract(coordinate, extent)
            if wall in ("left", "bottom")
            else subtract(subtract(self.side, coordinate), extent)
        )


def reconstruct(t: Interval, b: Interval) -> Layout:
    """Independent H254 formula transcription; no input or target reads on import."""
    one, two, half = point(1), point(2), point(Fraction(1, 2))
    dt, db = add(one, multiply(t, t)), add(one, multiply(b, b))
    c, s = divide(subtract(one, multiply(t, t)), dt), divide(multiply(two, t), dt)
    d, e = divide(subtract(one, multiply(b, b)), db), divide(multiply(two, b), db)
    kd = add(one, multiply(two, t), negate(multiply(t, t)))
    side = divide(add(point(6), multiply(point(4), t)), kd)
    h = divide(add(c, s), two)
    alpha = subtract(multiply(c, d), multiply(s, e))
    gamma = add(multiply(c, e), multiply(s, d))
    slack = multiply(c, add(c, point(4), negate(side)))
    u10 = add(point(Fraction(3, 2)), multiply(c, s), multiply(two, s))
    v10 = add(multiply(c, subtract(side, one)), negate(s), negate(half))
    u11 = add(c, multiply(two, s), half)
    v11 = add(
        multiply(two, c), divide(subtract(multiply(c, c), multiply(s, s)), two), point(-1)
    )
    u13 = add(multiply(two, c), s, half)
    aa = subtract(subtract(side, point(Fraction(3, 2))), divide(slack, multiply(point(3), s)))
    zz = subtract(subtract(v11, one), divide(slack, point(3)))
    xx = add(
        half,
        divide(add(two, multiply(c, s), multiply(point(3), s), negate(multiply(s, side))), c),
    )
    yy = add(
        point(Fraction(3, 2)),
        divide(add(two, multiply(point(3), c), negate(multiply(c, side))), s),
    )
    aa16 = add(multiply(d, add(xx, half)), negate(multiply(e, subtract(side, one))), half)
    bb16 = subtract(multiply(add(d, e), subtract(side, one)), half)

    def rotate(u: Interval, v: Interval) -> Vector:
        return subtract(multiply(c, u), multiply(s, v)), add(multiply(s, u), multiply(c, v))

    centres = {
        1: (half, half),
        2: (point(Fraction(3, 2)), half),
        3: (half, point(Fraction(3, 2))),
        4: (half, subtract(side, half)),
        5: (subtract(side, half), half),
        6: (aa, half),
        7: (subtract(side, half), point(Fraction(3, 2))),
        8: (subtract(side, half), subtract(side, half)),
        9: (h, add(two, h)),
        10: rotate(u10, v10),
        11: rotate(u11, v11),
        12: rotate(add(u11, one), subtract(v10, one)),
        13: rotate(u13, zz),
        14: rotate(add(u13, one), subtract(v10, two)),
        15: (xx, subtract(side, half)),
        16: (
            add(multiply(d, aa16), multiply(e, bb16)),
            add(negate(multiply(e, aa16)), multiply(d, bb16)),
        ),
        17: (subtract(side, half), yy),
    }
    axes = {
        "ex": (one, point(0)),
        "ey": (point(0), one),
        "u": (c, s),
        "v": (negate(s), c),
        "p": (d, negate(e)),
        "q": (e, d),
    }
    guards = {
        "t": t,
        "b": b,
        "c": c,
        "s": s,
        "d": d,
        "e": e,
        "alpha": alpha,
        "gamma": gamma,
        "T": slack,
        "D": dt,
        "E": db,
        "K": kd,
        "poly_L": multiply(add(one, t), dt),
        "one_plus_t": add(one, t),
        "side": side,
    }
    return Layout(centres, axes, guards, {"lambda6": aa, "lambda13": zz, "T": slack}, side)


def identity_manifest() -> dict[tuple[int, int], dict[str, Any]]:
    result = {
        (min(a, b), max(a, b)): {
            "reason": "defining" if i < 17 else ("F1", "F2", "F3")[i - 17],
            "axes": [{"from": a, "to": b, "axis": axis}],
        }
        for i, (a, b, axis) in enumerate(CONTACTS)
    }
    result[(2, 3)] = {
        "reason": "corner",
        "axes": [{"from": 3, "to": 2, "axis": "ex"}, {"from": 2, "to": 3, "axis": "ey"}],
    }
    return result


def coverage(geometry: dict[str, Any]) -> None:
    raw_walls, raw_pairs = geometry["walls"], geometry["pairs"]
    require(type(raw_walls) is list and type(raw_pairs) is list, "obligation arrays required")
    walls = cast(list[dict[str, Any]], raw_walls)
    pairs = cast(list[dict[str, Any]], raw_pairs)
    require(all(type(row["label"]) is int for row in walls), "integer wall labels required")
    require(
        all(type(row["left"]) is int and type(row["right"]) is int for row in pairs),
        "integer pair labels required",
    )
    wall_keys = [(row["label"], row["wall"]) for row in walls]
    pair_keys = [(row["left"], row["right"]) for row in pairs]
    require(
        len(wall_keys) == 68
        and set(wall_keys)
        == {(i, w) for i in range(1, 18) for w in ("left", "right", "bottom", "top")},
        "wall coverage differs",
    )
    require(
        len(pair_keys) == 136
        and set(pair_keys) == set(itertools.combinations(range(1, 18), 2)),
        "pair coverage differs",
    )
    require(exact_structure(geometry["counts"], COUNTS), "reported coverage counts differ")


def match(actual: Interval, reported: Any, label: str, *, positive: bool = False) -> None:
    require(actual == read_interval(reported), f"recomputed interval differs: {label}")
    require(not positive or actual[0] > 0, f"nonpositive strict interval: {label}")


def audit_geometry(geometry: dict[str, Any], root: dict[str, Any]) -> dict[str, int]:
    coverage(geometry)
    require(geometry["schema"] == "n17-endpoint-geometry/v1", "wrong geometry schema")
    require(
        geometry["geometry_passed"] is True and geometry["failures"] == [],
        "geometry did not pass",
    )
    expected_box = {
        "midpoint": root["box"]["midpoint"],
        "inclusion_bounds": root["inclusion_bounds"],
    }
    require(geometry["box"] == expected_box, "root enclosure differs")
    mid = [rational(value) for value in expected_box["midpoint"]]
    eta = [rational(value) for value in expected_box["inclusion_bounds"]]
    require(
        len(mid) == len(eta) == 2 and all(value > 0 for value in eta), "invalid root enclosure"
    )
    t, b = [(m - radius, m + radius) for m, radius in zip(mid, eta, strict=True)]
    require(
        Fraction(36, 100) < t[0] <= t[1] < Fraction(37, 100)
        and Fraction(33, 100) < b[0] <= b[1] < Fraction(34, 100),
        "angle enclosure outside H254 domain",
    )
    layout = reconstruct(t, b)
    require(
        Fraction(4675, 1000) < layout.side[0] <= layout.side[1] < Fraction(4676, 1000),
        "side enclosure outside H254 domain",
    )
    require(set(geometry["guards"]) == set(layout.guards), "guard manifest differs")
    require(set(geometry["sliders"]) == set(layout.sliders), "slider manifest differs")
    for name, value in layout.guards.items():
        match(value, geometry["guards"][name], f"guard.{name}", positive=True)
    for name, value in layout.sliders.items():
        match(value, geometry["sliders"][name], f"slider.{name}")
    match(layout.side, geometry["side"], "side")
    audit_obligations(geometry, layout)
    return {**COUNTS, "strict_intervals_recomputed": 168, "other_intervals_recomputed": 19}


def audit_obligations(geometry: dict[str, Any], layout: Layout) -> None:
    """Check all obligation records; root and analytic premises are checked separately."""
    coverage(geometry)
    manifest = identity_manifest()
    for row in geometry["walls"]:
        key = row["label"], row["wall"]
        identity = key in ANCHORS
        require(
            row["passed"] is True and row["kind"] == ("identity" if identity else "strict"),
            "wall status differs",
        )
        require(
            row["bound_scope"] == ("certified_root" if identity else "whole_box"),
            "wall scope differs",
        )
        if identity:
            require(row["bound"] == ["0", "0"], "wall identity bound differs")
        else:
            match(layout.wall_gap(*key), row["bound"], f"wall.{key}", positive=True)
    for row in geometry["pairs"]:
        pair = row["left"], row["right"]
        identity = pair in manifest
        require(
            row["passed"] is True and row["kind"] == ("identity" if identity else "strict"),
            "pair status differs",
        )
        require(
            row["bound_scope"] == ("certified_root" if identity else "whole_box"),
            "pair scope differs",
        )
        if identity:
            require(
                exact_structure(row["identity"], manifest[pair]) and row["bound"] == ["0", "0"],
                "pair identity manifest differs",
            )
        else:
            match(
                layout.pair_gap(*pair, row["axis"], row["direction"]),
                row["bound"],
                f"pair.{pair}",
                positive=True,
            )


def side_summary(side: Interval) -> dict[str, Any]:
    cap = Fraction(4675530093604551, 10**15)
    with localcontext() as context:
        context.prec = 35
        context.rounding = ROUND_FLOOR
        lower = str(Decimal(side[0].numerator) / Decimal(side[0].denominator))
        context.rounding = ROUND_CEILING
        upper = str(Decimal(side[1].numerator) / Decimal(side[1].denominator))
    return {
        "outward_decimal_enclosure": [lower, upper],
        "retained_rational_upper": "4675530093604551/1000000000000000",
        "exact_upper_at_most_retained_rational_upper": side[1] <= cap,
        "exact_upper_strictly_below_retained_rational_upper": side[1] < cap,
    }


def duplicate_refusal(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def json_integer(value: str) -> int:
    require(len(value) <= 12, "oversized bare JSON integer")
    return int(value)


def reject_constant(value: str) -> Any:
    raise AuditError(f"nonfinite JSON constant: {value}")


def decode(raw: bytes) -> dict[str, Any]:
    require(len(raw) <= MAX_BYTES, "JSON exceeds 10 MiB")
    result = json.loads(
        raw,
        object_pairs_hook=duplicate_refusal,
        parse_int=json_integer,
        parse_constant=reject_constant,
    )
    require(type(result) is dict, "JSON object required")
    return result


def read_bytes(path: Path) -> bytes:
    with path.open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    require(len(raw) <= MAX_BYTES, f"file exceeds 10 MiB: {path.name}")
    return raw


def audit(run: Path, repo: Path = REPO) -> dict[str, Any]:
    started = time.monotonic()
    files = {
        name: read_bytes(run / name)
        for name in (
            "certificate.json",
            "command.txt",
            "ended-at.txt",
            "exit.txt",
            "memory-guard.log",
            "provenance.log",
            "timing.log",
        )
    }
    raw = files["certificate.json"]
    document = decode(raw)
    root_raw = read_bytes(repo / ROOT_RUN / "certificate.json")
    root = decode(root_raw)
    receipt = decode(read_bytes(repo / ROOT_RUN / "checker.json"))
    require(
        document["root_certificate_git_ref"] == ROOT_REF,
        "receipt names another root certificate",
    )
    require(
        document["schema"] == "n17-endpoint-feasibility/v1"
        and document["criterion_passed"] is True,
        "endpoint receipt did not pass",
    )
    require(document["root_verification"] == receipt, "accepted root receipt differs")
    require(
        root["criterion_passed"] is True
        and root["source"]["path"] == SOURCE
        and root["source"]["row_to_label"] == LABELS
        and rational(root["box"]["radius"]) == Fraction(1, 10**12),
        "frozen root metadata differs",
    )
    source_raw = read_bytes(repo / SOURCE)
    require(
        hashlib.sha256(source_raw).hexdigest()
        == document["source_sha256"]
        == root["source"]["sha256"]
        == SOURCE_SHA,
        "source identity differs",
    )
    source = decode(source_raw)
    by_label = dict(zip(LABELS, source["squares"], strict=True))
    require(
        [rational(value) for value in root["box"]["midpoint"]]
        == [Fraction(by_label[9]["t"]), -Fraction(by_label[16]["t"])],
        "source midpoint differs",
    )
    require(
        exact_structure(
            document["identities"],
            {
                "wall_identities": 15,
                "pair_identities": 21,
                "normalizations": 3,
                "slider_identity": True,
            },
        ),
        "analytic completion manifest differs",
    )
    require(
        files["exit.txt"].strip() == b"0" and raw.endswith(b"\n"),
        "incomplete or failed execution",
    )
    require(
        EXECUTION_COMMIT.encode() in files["provenance.log"],
        "execution provenance differs",
    )
    counts = audit_geometry(document["geometry"], root)
    return {
        "schema": "n17-endpoint-receipt-audit/v1",
        "audit_passed": True,
        "counts": counts,
        "root_certificate_git_ref": ROOT_REF,
        "producer_imported_or_rerun": False,
        "trust_premises": [
            "previously accepted H255 root existence certificate",
            "separately reviewed analytic identity proofs and polynomial normalizations",
        ],
        "scope": (
            "all strict intervals independently recomputed; identity manifests checked, "
            "analytic identities not reproved"
        ),
        "receipt_bytes": len(raw),
        "run_file_bytes": {name: len(content) for name, content in files.items()},
        "audited_receipt_sha256": hashlib.sha256(raw).hexdigest(),
        "accepted_root_sha256": hashlib.sha256(root_raw).hexdigest(),
        "side": side_summary(read_interval(document["geometry"]["side"])),
        "elapsed_seconds": time.monotonic() - started,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path, nargs="?", default=REPO / ENDPOINT_RUN)
    args = parser.parse_args()
    try:
        result = audit(args.run)
    except (
        ValueError,
        OSError,
        KeyError,
        TypeError,
        IndexError,
        RecursionError,
    ) as error:
        print(json.dumps({"audit_passed": False, "error": str(error)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
