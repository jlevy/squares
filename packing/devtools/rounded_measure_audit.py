"""Exact audit of a scaled atomic measure on a rounded unit square.

All inputs are rational. The frame formula and an independent polygon-distance
formula must agree at every atom. This checks a claimed measure, not the existence
of some other fractional cover.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_write_text

type Point = tuple[Fraction, Fraction]
REPO = Path(__file__).resolve().parents[2]
MAX_ATOMS = 100_000
MAX_INPUT_BYTES = 16_000_000


def source_identity(tool: Path, historical_path: str) -> dict[str, Any]:
    """Capture Git identity without introducing a parallel integrity manifest."""
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}

    def git(*args: str) -> str:
        return subprocess.check_output(
            ["git", *args], cwd=REPO, env=env, text=True, timeout=10
        ).strip()

    return {
        "historical_commit": "c89c7646",
        "historical_path": historical_path,
        "tool_path": tool.resolve().relative_to(REPO).as_posix(),
        "checkout_commit": git("rev-parse", "HEAD"),
        "checkout_dirty": bool(git("status", "--porcelain")),
    }


def point_segment_distance_squared(p: Point, a: Point, b: Point) -> Fraction:
    direction = (b[0] - a[0], b[1] - a[1])
    norm = sum((value * value for value in direction), Fraction(0))
    parameter = sum(((p[k] - a[k]) * direction[k] for k in (0, 1)), Fraction(0)) / norm
    parameter = min(Fraction(1), max(Fraction(0), parameter))
    dx, dy = (p[k] - a[k] - parameter * direction[k] for k in (0, 1))
    return dx * dx + dy * dy


def polygon_distance_squared(p: Point, vertices: list[Point]) -> Fraction:
    inside = all(
        (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= 0
        for a, b in zip(vertices, vertices[1:] + vertices[:1], strict=True)
    )
    if inside:
        return Fraction(0)
    return min(
        point_segment_distance_squared(p, a, b)
        for a, b in zip(vertices, vertices[1:] + vertices[:1], strict=True)
    )


def audit(
    certificate: dict[str, Any],
    *,
    scale: Fraction,
    delta: Fraction,
    cx: Fraction,
    cy: Fraction,
    half_tangent: Fraction,
) -> dict[str, Any]:
    if scale <= 0 or delta < 0:
        raise ValueError("Scale must be positive and tolerance nonnegative")
    base_side = Fraction(certificate["outer_side"])
    outer_side = scale * base_side
    atoms = [(Fraction(x), Fraction(y), Fraction(w)) for x, y, w in certificate["atoms"]]
    if (
        not atoms
        or len(atoms) > MAX_ATOMS
        or any(w < 0 or not (0 <= x <= base_side and 0 <= y <= base_side) for x, y, w in atoms)
    ):
        raise ValueError("Certificate must have nonnegative in-container atoms")
    total = sum((w for _, _, w in atoms), Fraction(0))
    if total != Fraction(certificate["total_mass"]):
        raise ValueError("Atom mass disagrees with certificate total_mass")
    t = half_tangent
    cosine, sine = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
    if cosine * cosine + sine * sine != 1:
        raise AssertionError("Frame is not orthonormal")
    vertices = [
        (cx + (a * cosine - b * sine) / 2, cy + (a * sine + b * cosine) / 2)
        for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    ]
    if not all(0 <= x <= outer_side and 0 <= y <= outer_side for x, y in vertices):
        raise ValueError("Unit square is not contained in the scaled container")
    mass = Fraction(0)
    included = []
    for index, (base_x, base_y, weight) in enumerate(atoms):
        x, y = scale * base_x, scale * base_y
        u, v = (x - cx) * cosine + (y - cy) * sine, -(x - cx) * sine + (y - cy) * cosine
        frame_distance = (
            max(abs(u) - Fraction(1, 2), Fraction(0)) ** 2
            + max(abs(v) - Fraction(1, 2), Fraction(0)) ** 2
        )
        polygon_distance = polygon_distance_squared((x, y), vertices)
        if frame_distance != polygon_distance:
            raise AssertionError(f"Distance methods disagree at atom {index}")
        if frame_distance <= delta * delta:
            mass += weight
            included.append(index)
    return {
        "status": "counterexample" if mass < 1 else "covered_pose",
        "certificate_id": certificate["id"],
        "outer_side": str(outer_side),
        "scale": str(scale),
        "delta": str(delta),
        "unit_pose": {"cx": str(cx), "cy": str(cy), "half_tangent": str(t)},
        "total_mass": str(total),
        "rounded_square_mass": str(mass),
        "rounded_square_mass_decimal": float(mass),
        "mass_below_one": mass < 1,
        "independent_distance_agreement_count": len(atoms),
        "included_atom_indices": included,
    }


def load_certificate(path: Path) -> dict[str, Any]:
    """Bound the input before parsing a retained atomic measure."""
    with path.open("rb") as handle:
        raw = handle.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        raise ValueError("Certificate exceeds the bounded input size")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise TypeError("Certificate must be an object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--scale", type=Fraction, default=Fraction(1))
    parser.add_argument("--delta", type=Fraction, default=Fraction(0))
    parser.add_argument("--cx", type=Fraction, required=True)
    parser.add_argument("--cy", type=Fraction, required=True)
    parser.add_argument("--half-tangent", type=Fraction, default=Fraction(0))
    parser.add_argument("--expect", choices=("covered", "below-one"), default="covered")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        certificate = load_certificate(args.certificate)
        result = audit(
            certificate,
            scale=args.scale,
            delta=args.delta,
            cx=args.cx,
            cy=args.cy,
            half_tangent=args.half_tangent,
        )
        result["source"] = source_identity(
            Path(__file__), "packing/cases/n11_fractional_certificate/certificate.json"
        )
        result["certificate_path"] = str(args.certificate)
        expected = args.expect == "below-one"
        result["expectation"] = args.expect
        result["expectation_met"] = result["mass_below_one"] == expected
        code = 0 if result["expectation_met"] else 1
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        AssertionError,
        subprocess.SubprocessError,
    ) as error:
        result = {"status": "error", "error": str(error)}
        code = 2
    text = json.dumps(result, indent=2) + "\n"
    if args.output is not None:
        atomic_write_text(args.output, text)
    print(text, end="")
    return code


if __name__ == "__main__":
    sys.exit(main())
