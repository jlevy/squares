"""Sufficient continuous A1 or A3 forcing for canonical near-45 P10 avoiders.

Only explicit --target-a1/--target-a3 dispatch evaluates target inequalities. Imports, toy
APIs, and packet parsing do not construct the target. The unchanged source
formulas are cases/stromquist/restricted_orientation.py:point_sets: L=(1,1),
M=(q/2,1), A1=(1,q-3), A3=(3/2,13/10), with q=1939/500, not a scaled source side.

The mathematical reduction requires a contained CLOSED unit square, its center
(x,y) in R=[1,q/2] x [0,1], 2<q<4, C,S>0 and C^2+S^2=1. Write
X=x-1, Y=1-y, W=q/2-1 and h=(C+S)/2. Then 0<=X<=W<1 and
0<=Y<=1-h<1/2. Avoiding L requires CX-SY>1/2 or SX+CY>1/2;
avoiding M requires C(W-X)+SY>1/2 or S(W-X)-CY>1/2. The three
unwanted pairs contradict CW<1, SW<1, or max(C,S)W<1, respectively.
Thus, with U=Cx+Sy,V=-Sx+Cy, every pair avoider satisfies U<u, V<v,
SU+CV>=h, where u=Cq/2+S-1/2 and v=C-S-1/2. P10 avoidance implies
pair avoidance, but failure of the stronger pair test is only unresolved.

Replace strict inequalities by closed ones and discard the other constraints.
The resulting set is empty or the closed triangle E=(u,v),
F=((h-Cv)/S,v), G=(u,(h-Su)/C). If Delta=Su+Cv-h is positive,
weights S(u-U)/Delta, C(v-V)/Delta, (SU+CV-h)/Delta prove complete
convex coverage. Delta=0 is a singleton; Delta<0 is empty. We require all
three formal vertices even in the empty case, which is a stronger sufficient
test and avoids any unproved sign choice for Delta.

Four affine square-membership margins at each vertex become degree <=4
polynomials over positive Q(sqrt(2)). With D=1+t^2 and C=c/D,S=s/D,
|t|<1/3 gives 1+/-2t-t^2>2/9, so D,cD,sD are strictly positive.
The fixed T=(11/5040)/(1-(11/5040)^2/2) exceeds tan(pi/1440), by
pi<22/7, sin(x)<=x, cos(x)>=1-x^2/2. Both closed slabs [-T,0],[0,T]
are checked without subdivision: 3 vertices x 4 margins x 2 slabs = 24.
Any failure is unresolved; a failed outer-sliver test is not a counterexample.
This supplies only the selected sufficient point-forcing clause, never H-036.

For the stronger L/M-avoidance statement, local reflection x -> 1+q/2-x
interchanges L and M, A1 and A2=(q/2,q-3), and t and -t. Canonical x
coordinates stay in [1,q/2], which lies in [h,q-h] since h<1 and q>2;
y and h are unchanged. Thus containment is retained. In square-frame
coordinates U'=V+S*(1+q/2), V'=U-C*(1+q/2); E maps to E at the
reflected angle, while F/G swap.
This reflection implication does not require P10 itself to be invariant.
"""

from __future__ import annotations

import argparse
import json
import resource
import signal
import subprocess
import sys
import time
from collections.abc import Iterator, Sequence
from fractions import Fraction
from functools import cache, partial
from pathlib import Path
from typing import Any, Literal

from devtools.angle_tile_certificate import Polynomial, Scalar, certify_nonnegative
from sqpack.cover import write_text_atomic
from sqpack.field import NumberField

type RationalPoint = tuple[Fraction, Fraction]
type Failure = tuple[int, int, int]
type VertexPolynomials = tuple[tuple[Polynomial, ...], ...]
type Clause = Literal["a3", "a1"]

ZERO = Fraction(0)
ONE = Fraction(1)
HALF = Fraction(1, 2)
SIDE = Fraction(1939, 500)
POINT = (Fraction(3, 2), Fraction(13, 10))
A1_POINT = (ONE, SIDE - 3)
OUTER_ARGUMENT = Fraction(11, 5040)
T = OUTER_ARGUMENT / (1 - OUTER_ARGUMENT**2 / 2)
SLABS = ((-T, ZERO), (ZERO, T))
KIND = "fixed-side-near45-a3-forcing-triangle"
A1_KIND = "fixed-side-near45-a1-forcing-triangle"
OBLIGATION_COUNT = 24
WALL_CAP_SECONDS = 10
PACKET_BYTE_CAP = 262144
MAX_INPUT_BITS = 2048


def _rational(value: Fraction) -> None:
    if type(value) is not Fraction:
        raise ValueError("exact Fraction inputs required; floats and booleans are refused")
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > MAX_INPUT_BITS:
        raise ValueError("rational input exceeds the declared bit limit")


def _add(left: Polynomial, right: Polynomial) -> Polynomial:
    return tuple(
        (left[i] if i < len(left) else ZERO) + (right[i] if i < len(right) else ZERO)
        for i in range(max(len(left), len(right)))
    )


def _scale(value: Polynomial, factor: Scalar) -> Polynomial:
    return tuple(factor * coefficient for coefficient in value)


def _multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: list[Scalar] = [ZERO] * (len(left) + len(right) - 1)
    for i, first in enumerate(left):
        for j, second in enumerate(right):
            result[i + j] += first * second
    return tuple(result)


def _signed_pair(base: Polynomial, difference: Polynomial) -> tuple[Polynomial, Polynomial]:
    return _add(base, difference), _add(base, _scale(difference, -ONE))


@cache
def chart_polynomials() -> tuple[Polynomial, Polynomial, Polynomial]:
    """Lazy source-free D,c,s for theta=pi/4+2 atan(t), in one exact field."""
    root_half = NumberField((1, 0, -2), ("1", "2")).alpha / 2
    return (
        (ONE, ZERO, ONE),
        (root_half, -2 * root_half, -root_half),
        (root_half, 2 * root_half, -root_half),
    )


def triangle_polynomials(side: Fraction, point: RationalPoint) -> VertexPolynomials:
    """Build E,F,G rows, each ordered U+,U-,V+,V-; no target defaults."""
    _rational(side)
    if not 2 < side < 4:
        raise ValueError("canonical pair-avoidance reduction requires 2 < side < 4")
    if type(point) is not tuple or len(point) != 2:
        raise ValueError("point must be a pair of exact Fraction coordinates")
    for coordinate in point:
        _rational(coordinate)
    d, c, s = chart_polynomials()
    u = _add(_add(_scale(c, side / 2), s), _scale(d, -HALF))
    v = _add(_add(c, _scale(s, -ONE)), _scale(d, -HALF))
    height = _scale(_add(c, s), HALF)
    point_u = _add(_scale(c, point[0]), _scale(s, point[1]))
    point_v = _add(_scale(s, -point[0]), _scale(c, point[1]))
    e_u = _signed_pair(_scale(d, HALF), _add(point_u, _scale(u, -ONE)))
    e_v = _signed_pair(_scale(d, HALF), _add(point_v, _scale(v, -ONE)))
    f_u = _signed_pair(
        _scale(_multiply(s, d), HALF),
        _add(_add(_multiply(s, point_u), _scale(_multiply(height, d), -ONE)), _multiply(c, v)),
    )
    g_v = _signed_pair(
        _scale(_multiply(c, d), HALF),
        _add(_add(_multiply(c, point_v), _scale(_multiply(height, d), -ONE)), _multiply(s, u)),
    )
    return (*e_u, *e_v), (*f_u, *e_v), (*e_u, *g_v)


def closed_triangle(
    cosine: Fraction, sine: Fraction, upper_u: Fraction, upper_v: Fraction, height: Fraction
) -> tuple[RationalPoint, ...]:
    """Exact rational control API for the empty/point/full closed half-plane triangle.

    Unit-normal identity is unnecessary for this affine lemma. Rational inputs
    permit unrelated constructive controls without loading source geometry.
    """
    for value in (cosine, sine, upper_u, upper_v, height):
        _rational(value)
    if cosine <= 0 or sine <= 0:
        raise ValueError("both coefficients must be positive")
    if sine * upper_u + cosine * upper_v < height:
        return ()
    return (
        (upper_u, upper_v),
        ((height - cosine * upper_v) / sine, upper_v),
        (upper_u, (height - sine * upper_u) / cosine),
    )


def triangle_obligations(
    side: Fraction, point: RationalPoint, *, low: Fraction, high: Fraction
) -> Iterator[tuple[tuple[int, int], bool]]:
    """Yield all twelve completed unsplit tests, including failed closed margins."""
    _rational(low)
    _rational(high)
    if not -Fraction(1, 3) < low <= high < Fraction(1, 3):
        raise ValueError("ordered closed slab must lie strictly inside (-1/3,1/3)")
    for vertex, row in enumerate(triangle_polynomials(side, point)):
        for margin, polynomial in enumerate(row):
            yield (
                (vertex, margin),
                certify_nonnegative(polynomial, low, high, max_depth=0).proved,
            )


def target_input() -> tuple[Fraction, RationalPoint]:
    """Return the unchanged q/A3 formulas only on explicit experiment dispatch."""
    return SIDE, POINT


def a1_target_input() -> tuple[Fraction, RationalPoint]:
    """Return unchanged q/A1 formulas only on explicit A1 experiment dispatch."""
    return SIDE, A1_POINT


def _identity(clause: Clause) -> tuple[str, RationalPoint]:
    if type(clause) is not str or clause not in ("a3", "a1"):
        raise ValueError("clause must be exactly a3 or a1")
    return (KIND, POINT) if clause == "a3" else (A1_KIND, A1_POINT)


def packet(
    checked: int, failures: list[Failure], *, interrupted: bool = False, clause: Clause = "a3"
) -> dict[str, Any]:
    """Fixed wire identity with a completed canonical prefix, never coefficients."""
    kind, point = _identity(clause)
    return {
        "version": 1,
        "kind": kind,
        "side": str(SIDE),
        "point": [str(value) for value in point],
        "half_angle_slabs": [[str(low), str(high)] for low, high in SLABS],
        "vertices": ["E", "F", "G"],
        "status": "proved"
        if checked == OBLIGATION_COUNT and not failures and not interrupted
        else "unresolved",
        "inequalities_checked": checked,
        "unresolved": [list(index) for index in failures],
    }


def run_target(*, clause: Clause = "a3") -> dict[str, Any]:
    """Worker-only evaluation; tests replace the selected constructor with unrelated toys."""
    _identity(clause)
    completed: list[tuple[Failure, bool]] = []
    interrupted = False
    try:
        side, point = target_input() if clause == "a3" else a1_target_input()
        for slab, (low, high) in enumerate(SLABS):
            in_slab = 0
            for index, proved in triangle_obligations(side, point, low=low, high=high):
                if (
                    in_slab >= 12
                    or type(index) is not tuple
                    or len(index) != 2
                    or any(type(value) is not int for value in index)
                    or index != divmod(in_slab, 4)
                    or type(proved) is not bool
                ):
                    raise ValueError("obligation generator changed the frozen complete order")
                completed.append(((slab, *index), proved))
                in_slab += 1
            if in_slab != 12:
                interrupted = True
                break
    except TimeoutError as error:
        interrupted = True
        print(
            f"unresolved: alarm after {len(completed)} inequalities: {error}", file=sys.stderr
        )
    return packet(
        len(completed),
        [index for index, proved in completed if not proved],
        interrupted=interrupted,
        clause=clause,
    )


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = dict(pairs)
    if len(result) != len(pairs):
        raise ValueError("packet contains duplicate object keys")
    return result


def _reject_constant(_value: str) -> None:
    raise ValueError("packet contains a non-finite JSON number")


def parse_worker(stdout: str, *, clause: Clause = "a3") -> dict[str, Any]:
    """Validate the bounded frozen envelope, not its mathematical conclusion."""
    if type(stdout) is not str:
        raise ValueError("packet must be UTF-8 JSON text")
    if len(stdout.encode()) > PACKET_BYTE_CAP:
        raise ValueError("packet exceeds 256 KiB")
    result = json.loads(
        stdout, object_pairs_hook=_unique_object, parse_constant=_reject_constant
    )
    template = packet(0, [], clause=clause)
    if type(result) is not dict or set(result) != set(template):
        raise ValueError("packet must have exactly the frozen nine keys")
    if type(result["version"]) is not int or result["version"] != 1:
        raise ValueError("packet version is invalid")
    if any(
        result[key] != template[key]
        for key in ("kind", "side", "point", "half_angle_slabs", "vertices")
    ):
        raise ValueError("packet changes the fixed source, vertices, or closed angle slabs")
    checked = result["inequalities_checked"]
    if type(checked) is not int or not 0 <= checked <= OBLIGATION_COUNT:
        raise ValueError("packet completed-prefix count is invalid")
    failures = result["unresolved"]
    if type(failures) is not list or len(failures) > checked:
        raise ValueError("packet unresolved inventory is invalid")
    previous = -1
    for index in failures:
        if (
            type(index) is not list
            or len(index) != 3
            or any(
                type(value) is not int or not 0 <= value < bound
                for value, bound in zip(index, (2, 3, 4), strict=True)
            )
        ):
            raise ValueError("packet unresolved index is invalid")
        slab, vertex, margin = index
        ordinal = (slab * 3 + vertex) * 4 + margin
        if not previous < ordinal < checked:
            raise ValueError("packet failures must be ordered unique members of the prefix")
        previous = ordinal
    if result["status"] not in ("proved", "unresolved") or (
        result["status"] == "proved" and (checked != OBLIGATION_COUNT or failures)
    ):
        raise ValueError("packet status exceeds its completed inventory")
    return result


def _expired(_signum: int, _frame: Any, *, clause: Clause = "a3") -> None:
    raise TimeoutError(f"fixed ten-second near-45 {clause.upper()} cap")


def _text(value: str | bytes | None) -> str:
    return value.decode(errors="replace") if isinstance(value, bytes) else value or ""


def _run_child(*, clause: Clause = "a3") -> tuple[dict[str, Any], dict[str, Any], int]:
    _identity(clause)
    command = [
        sys.executable,
        "-m",
        "devtools.angle_near45_triangle_control",
        f"--target-{clause}",
        "--worker",
    ]
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    started = time.monotonic()
    note = "complete worker return"
    try:
        process = subprocess.run(
            command, capture_output=True, text=True, check=False, timeout=WALL_CAP_SECONDS
        )
        stdout, stderr, child_exit = process.stdout, process.stderr, process.returncode
        try:
            result = parse_worker(stdout, clause=clause)
            if child_exit != 0:
                result["status"] = "unresolved"
            code = 0 if child_exit == 0 and result["status"] == "proved" else 1
        except (ValueError, TypeError, RecursionError) as error:
            result, code = packet(0, [], clause=clause), 2
            note = f"worker packet refused: {error}"
    except subprocess.TimeoutExpired as error:
        stdout, stderr, child_exit = _text(error.stdout), _text(error.stderr), None
        result, code = packet(0, [], clause=clause), 1
        note = "child process cap; no complete packet retained"
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    log = {
        "command": command,
        "child_exit_code": child_exit,
        "parent_exit_code": code,
        "child_wall_cap_seconds": WALL_CAP_SECONDS,
        "process_wall_seconds": time.monotonic() - started,
        "child_cpu_seconds": after.ru_utime
        - before.ru_utime
        + after.ru_stime
        - before.ru_stime,
        "note": note,
        "stdout": stdout,
        "stderr": stderr,
    }
    return result, log, code


def main(argv: Sequence[str] | None = None) -> int:
    """Explicit fixed dispatch; atomic per-file publication is not a two-file transaction."""
    parser = argparse.ArgumentParser(description=__doc__)
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--target-a3", dest="clause", action="store_const", const="a3")
    selector.add_argument("--target-a1", dest="clause", action="store_const", const="a1")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--output", type=Path, help="atomically replace this proof packet")
    parser.add_argument("--log", type=Path, help="atomically replace this execution log")
    args = parser.parse_args(argv)
    clause: Clause = args.clause
    if args.worker and (args.output is not None or args.log is not None):
        parser.error("only the parent publishes output files")
    if (
        args.output is not None
        and args.log is not None
        and args.output.resolve() == args.log.resolve()
    ):
        parser.error("packet and log paths must differ")
    try:
        if args.worker:
            previous = signal.signal(signal.SIGALRM, partial(_expired, clause=clause))
            signal.alarm(WALL_CAP_SECONDS)
            try:
                result = run_target(clause=clause)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, previous)
            print(json.dumps(result, sort_keys=True))
            return 0 if result["status"] == "proved" else 1
        result, log, code = _run_child(clause=clause)
        if args.log is not None:
            write_text_atomic(args.log, json.dumps(log, indent=2, sort_keys=True) + "\n")
        if args.output is not None:
            write_text_atomic(args.output, json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(json.dumps(result, sort_keys=True))
    except TimeoutError as error:
        print(json.dumps(packet(0, [], clause=clause), sort_keys=True))
        print(f"unresolved: {error}", file=sys.stderr)
        return 1
    except (OSError, ValueError, TypeError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    else:
        return code


if __name__ == "__main__":
    raise SystemExit(main())
