"""Independent closed-triangle reader for the near-45-degree A3 forcing clause.

Only NumberField/Q(sqrt(2)) arithmetic and the bounded JSON loader are shared
project foundations. Geometry, denominator clearing and the unsplit Bernstein
transform below import no producer implementation. The two exact t-slabs are
bound here; their coverage of pi/4 +/- pi/720 is an external analytic premise.

For 2<q<4 and positive C,S with C²+S²=1, a contained square centered at
(x,y) in [1,q/2] x [0,1] has y>=h=(C+S)/2>1/2. Avoiding L=(1,1) leaves
U>U_L+1/2 or V<V_L-1/2; avoiding M=(q/2,1) leaves U<U_M-1/2 or
V>V_M+1/2. Since d=q/2-1<1, the incompatible U branches cannot coexist,
nor can the incompatible V branches. The unwanted pair U>U_L+1/2 and
V>V_M+1/2 forces y>1+h-CS*d>1. Thus U<u*=U_M-1/2 and V<v*=V_L-1/2.
Together with y=SU+CV>=h these imply membership in the closed set K used
below. Avoiding the unchanged P10 implies avoiding its members L and M.

K is empty, a singleton, or the triangle with formal vertices E,F,G. Every
point-membership margin is affine in U,V, so nonnegative margins at all three
formal vertices imply containment throughout K, even when K is empty. A failed
formal-vertex proof is not a counterexample to the forcing clause. This reader
never decides the full restricted-angle theorem or a square-packing bound.
"""

from __future__ import annotations

import argparse
import json
import signal
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from math import comb
from pathlib import Path
from typing import Any

from devtools.check_full_size_density_support_ceiling import load_packet
from sqpack.field import FieldElement, NumberField

type Polynomial = tuple[FieldElement, ...]
type Point = tuple[Fraction, Fraction]
type Slab = tuple[Fraction, Fraction]
type Failure = tuple[int, int, int]

FIXED_SIDE = Fraction(1939, 500)
FIXED_POINT = (Fraction(3, 2), Fraction(13, 10))
HALF_TANGENT = Fraction(110880, 50803079)
SLABS = ((-HALF_TANGENT, Fraction(0)), (Fraction(0), HALF_TANGENT))
VERTICES = ("E", "F", "G")
OBLIGATIONS = 24
PACKET_BYTE_CAP = 262144
WALL_CAP_SECONDS = 10
SCOPE = "fixed-side near45 A3 forcing clause on the two declared closed t-slabs only"
PACKET_KEYS = {
    "version",
    "kind",
    "side",
    "point",
    "half_angle_slabs",
    "vertices",
    "status",
    "inequalities_checked",
    "unresolved",
}


@dataclass(frozen=True)
class TriangleResult:
    vertices_checked: int
    inequalities_checked: int
    uncertified: tuple[Failure, ...]

    @property
    def proved(self) -> bool:
        return not self.uncertified


def target_input() -> tuple[Fraction, Point]:
    """Scientific binding; author controls replace or forbid this boundary."""
    return FIXED_SIDE, FIXED_POINT


def _sum(*polynomials: Polynomial) -> Polynomial:
    field = polynomials[0][0].field
    return tuple(
        sum((p[i] for p in polynomials if i < len(p)), field.zero)
        for i in range(max(map(len, polynomials)))
    )


def _times(polynomial: Polynomial, scalar: Fraction | FieldElement) -> Polynomial:
    return tuple(coefficient * scalar for coefficient in polynomial)


def _product(left: Polynomial, right: Polynomial) -> Polynomial:
    field = left[0].field
    return tuple(
        sum(
            (a * right[k - i] for i, a in enumerate(left) if 0 <= k - i < len(right)),
            field.zero,
        )
        for k in range(len(left) + len(right) - 1)
    )


def vertex_polynomials(side: Fraction, point: Point) -> tuple[tuple[Polynomial, ...], ...]:
    """Derive the twelve cleared membership quartics, ordered E/F/G then +/- U/V.

    Put c=D*C, s=D*S, H=(c+s)/2, A=c*a+s*b, B=-s*a+c*b,
    u=c*q/2+s-D/2 and v=c-s-D/2. E=(u/D,v/D). At F the first
    coordinate is (H*D-c*v)/(s*D); at G the second is (H*D-s*u)/(c*D).
    E margins are multiplied by D², F margins by s*D, G margins by c*D.
    Each factor is positive for |t|<1/3, and each result has degree at most four.
    """
    if type(side) is not Fraction or not 2 < side < 4:
        raise ValueError("triangle reduction requires an exact side strictly between 2 and 4")
    if (
        type(point) is not tuple
        or len(point) != 2
        or any(type(value) is not Fraction or not 0 <= value <= side for value in point)
    ):
        raise ValueError("point must be an exact rational pair inside the container")
    field = NumberField((1, 0, -2), ("1", "2"))
    root_half = field.alpha / 2
    denominator = tuple(field.rational(value) for value in (1, 0, 1))
    cosine = tuple(root_half * value for value in (1, -2, -1))
    sine = tuple(root_half * value for value in (1, 2, -1))
    height = _times(_sum(cosine, sine), Fraction(1, 2))
    u = _sum(_times(cosine, side / 2), sine, _times(denominator, Fraction(-1, 2)))
    v = _sum(cosine, _times(sine, Fraction(-1)), _times(denominator, Fraction(-1, 2)))
    a = _sum(_times(cosine, point[0]), _times(sine, point[1]))
    b = _sum(_times(sine, -point[0]), _times(cosine, point[1]))
    e_u = _product(denominator, _sum(a, _times(u, Fraction(-1))))
    e_v = _product(denominator, _sum(b, _times(v, Fraction(-1))))
    f_u = _sum(
        _product(sine, a),
        _times(_product(height, denominator), Fraction(-1)),
        _product(cosine, v),
    )
    f_v = _product(sine, _sum(b, _times(v, Fraction(-1))))
    g_u = _product(cosine, _sum(a, _times(u, Fraction(-1))))
    g_v = _sum(
        _product(cosine, b),
        _times(_product(height, denominator), Fraction(-1)),
        _product(sine, u),
    )
    return tuple(
        tuple(
            _sum(_times(factor, Fraction(1, 2)), _times(offset, Fraction(sign)))
            for offset in (u_offset, v_offset)
            for sign in (1, -1)
        )
        for factor, u_offset, v_offset in (
            (_product(denominator, denominator), e_u, e_v),
            (_product(sine, denominator), f_u, f_v),
            (_product(cosine, denominator), g_u, g_v),
        )
    )


def bernstein_coefficients(
    polynomial: Polynomial, left: Fraction, right: Fraction
) -> Polynomial:
    """Degree-four Bernstein coefficients by the symmetric multilinear blossom.

    The i-th coefficient evaluates the blossom on 4-i copies of left and i
    copies of right. For t**k this is the elementary symmetric degree-k sum
    of those four arguments divided by binomial(4,k). This uses no producer
    basis-conversion or interval-subdivision routine.
    """
    if not 1 <= len(polynomial) <= 5 or not all(
        isinstance(coefficient, FieldElement) for coefficient in polynomial
    ):
        raise ValueError(
            "Bernstein input must be a nonempty algebraic polynomial of degree <=4"
        )
    field = polynomial[0].field
    if any(coefficient.field is not field for coefficient in polynomial):
        raise ValueError("polynomial coefficients must share one exact field")
    if type(left) is not Fraction or type(right) is not Fraction or left > right:
        raise ValueError("Bernstein interval needs ordered exact rational endpoints")
    return tuple(
        sum(
            (
                coefficient
                * sum(
                    (
                        Fraction(comb(4 - i, k - j) * comb(i, j), comb(4, k))
                        * left ** (k - j)
                        * right**j
                        for j in range(k + 1)
                    ),
                    Fraction(0),
                )
                for k, coefficient in enumerate(polynomial)
            ),
            field.zero,
        )
        for i in range(5)
    )


def certifies_nonnegative(polynomial: Polynomial, left: Fraction, right: Fraction) -> bool:
    """One unsplit sufficient proof; a negative coefficient means unresolved."""
    return all(value.sign() >= 0 for value in bernstein_coefficients(polynomial, left, right))


def check_triangle(side: Fraction, point: Point, slabs: Sequence[Slab]) -> TriangleResult:
    """Check every formal vertex on both closed slabs, including their common seam."""
    if (
        len(slabs) != 2
        or any(len(slab) != 2 or any(type(t) is not Fraction for t in slab) for slab in slabs)
        or not -Fraction(1, 3) < slabs[0][0] < slabs[0][1] == 0 == slabs[1][0]
        or not 0 < slabs[1][1] < Fraction(1, 3)
        or slabs[0][0] != -slabs[1][1]
    ):
        raise ValueError("two symmetric closed t-slabs strictly inside (-1/3,1/3) are required")
    # c,s >= sqrt(2)/2 * (1-2*T-T²)>0; D=1+t²>=1. No numerical signs.
    majorant = slabs[1][1]
    if 1 - 2 * majorant - majorant**2 <= 0:
        raise ValueError("the denominator positivity bound failed")
    polynomials = vertex_polynomials(side, point)
    failures: list[Failure] = []
    vertices = checked = 0
    for slab_index, (left, right) in enumerate(slabs):
        for vertex, margins in enumerate(polynomials):
            vertices += 1
            for margin, polynomial in enumerate(margins):
                checked += 1
                if not certifies_nonnegative(polynomial, left, right):
                    failures.append((slab_index, vertex, margin))
    return TriangleResult(vertices, checked, tuple(failures))


def validate_packet(packet: Any) -> None:
    """Admit only the fixed nine-key wire; incomplete producer packets do no geometry."""
    if type(packet) is not dict or set(packet) != PACKET_KEYS:
        raise ValueError("packet has missing or unexpected keys")
    if type(packet["version"]) is not int or packet["version"] != 1:
        raise ValueError("packet version must be integer one")
    expected = {
        "kind": "fixed-side-near45-a3-forcing-triangle",
        "side": str(FIXED_SIDE),
        "point": [str(value) for value in FIXED_POINT],
        "half_angle_slabs": [[str(left), str(right)] for left, right in SLABS],
        "vertices": list(VERTICES),
    }
    for key, value in expected.items():
        if type(packet[key]) is not type(value) or packet[key] != value:
            raise ValueError(f"packet changes the canonical fixed {key}")
    if any(type(slab) is not list for slab in packet["half_angle_slabs"]):
        raise ValueError("packet slabs must be JSON arrays")
    status, count = packet["status"], packet["inequalities_checked"]
    if type(status) is not str or status not in ("proved", "unresolved"):
        raise ValueError("packet has an invalid producer status")
    if type(count) is not int or not 0 <= count <= OBLIGATIONS:
        raise ValueError("packet has an invalid completed-prefix count")
    failures = packet["unresolved"]
    if type(failures) is not list or len(failures) > count:
        raise ValueError("packet has an invalid unresolved inventory")
    previous = -1
    for entry in failures:
        if (
            type(entry) is not list
            or len(entry) != 3
            or any(
                type(index) is not int or not 0 <= index < limit
                for index, limit in zip(entry, (2, 3, 4), strict=True)
            )
        ):
            raise ValueError("packet unresolved coordinates are invalid")
        ordinal = (entry[0] * 3 + entry[1]) * 4 + entry[2]
        if not previous < ordinal < count:
            raise ValueError(
                "packet unresolved entries must be ordered unique checked-prefix members"
            )
        previous = ordinal
    if status == "proved" and (count != OBLIGATIONS or failures):
        raise ValueError("positive packet requires all 24 obligations and no failures")


def check_packet(packet: Any) -> dict[str, Any]:
    """Re-derive every obligation; producer counters are admission metadata only."""
    validate_packet(packet)
    base = {"scope": SCOPE, "h036_outcome": "unresolved"}
    if packet["status"] != "proved":
        return base | {"decision": "unresolved", "reason": "producer proof was incomplete"}
    side, point = target_input()
    result = check_triangle(side, point, SLABS)
    if result.vertices_checked != 6 or result.inequalities_checked != OBLIGATIONS:
        raise ValueError("reader did not check all 24 fixed obligations")
    return base | {
        "decision": "proved" if result.proved else "unresolved",
        "reason": "all formal-vertex margins certified on both closed slabs"
        if result.proved
        else "unsplit Bernstein proof left uncertified margins; not a refutation",
        "side": str(FIXED_SIDE),
        "point": [str(value) for value in FIXED_POINT],
        "half_angle_slabs": [[str(left), str(right)] for left, right in SLABS],
        "vertices_checked": result.vertices_checked,
        "inequalities_checked": result.inequalities_checked,
        "unresolved": [list(entry) for entry in result.uncertified],
        "method": "degree-four polarized Bernstein coefficients; no subdivision",
        "shared_foundations": ["NumberField Q(sqrt(2)) arithmetic", "bounded JSON loader"],
    }


def _expired(_signal: int, _frame: Any) -> None:
    raise TimeoutError("near45 reader reached its fixed ten-second internal alarm")


def main(argv: Sequence[str] | None = None) -> int:
    """Print proof receipt and costs; the future dispatcher must also cap the process at 10s.

    The alarm covers admission and proof calculation, not imports or final stream
    serialization. The caller must retain both streams and the actual exit status;
    a positive JSON object without a successful process exit is not accepted.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--target-a3", action="store_true", required=True)
    args = parser.parse_args(argv)
    if not args.packet.is_absolute():
        parser.error("packet path must be absolute")
    started, cpu_started = time.monotonic(), time.process_time()
    previous = signal.signal(signal.SIGALRM, _expired)
    signal.alarm(WALL_CAP_SECONDS)
    try:
        receipt = check_packet(load_packet(args.packet, max_bytes=PACKET_BYTE_CAP))
        code = 0 if receipt["decision"] == "proved" else 1
    except TimeoutError as error:
        receipt = {"decision": "unresolved", "scope": SCOPE, "reason": str(error)}
        code = 1
    except (OSError, ValueError, TypeError, KeyError, ArithmeticError, RecursionError) as error:
        receipt = {"decision": "refused", "scope": SCOPE, "reason": str(error)}
        code = 2
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)
    receipt["h036_outcome"] = "unresolved"
    print(json.dumps(receipt, sort_keys=True))
    print(
        json.dumps(
            {
                "input": str(args.packet),
                "exit_code": code,
                "wall_cap_seconds": WALL_CAP_SECONDS,
                "subdivisions": 0,
                "wall_seconds": time.monotonic() - started,
                "cpu_seconds": time.process_time() - cpu_started,
            },
            sort_keys=True,
        ),
        file=sys.stderr,
    )
    return code


if __name__ == "__main__":
    raise SystemExit(main())
