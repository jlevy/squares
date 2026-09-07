#!/usr/bin/env python3
"""Independent exact-integer checker for s(17) > 4.456575.

This intentionally does not import or reuse the C++ generator/checker code.
All predicates are recomputed with Python arbitrary-precision integers.
The traversal is written allocation-light because this certificate has >21M nodes.
"""
from __future__ import annotations

import pathlib
import sys

Q = 1 << 40
XS = 1_000_000 * Q
LS = 4_456_575 * Q
LO = 500_000 * Q
HI = 3_956_575 * Q
DEN = 1_000_000
Q2 = Q * Q
XS2 = XS * XS
COVER_SCALE = DEN * DEN * XS2

POINTS = (
    ( 963374,  984985), (1581796,  985592),
    (2476851,  926473), (3456650,  919147),
    ( 995406, 1792837), (1990669, 1796975),
    (2972834, 1793954), (3523331, 1792554),
    ( 922136, 2657284), (1491209, 2660029),
    (2483245, 2665147), (3456650, 2667556),
    ( 999352, 3529848), (1962693, 3518471),
    (2850255, 3462543), (3456920, 3456650),
)
PXS = tuple(x * XS for x, _ in POINTS)
PYS = tuple(y * XS for _, y in POINTS)


def min_abs_t(tl: int, th: int) -> int:
    if tl <= 0 <= th:
        return 0
    a = -tl if tl < 0 else tl
    b = -th if th < 0 else th
    return a if a < b else b


def half_extent_exceeds(a: int, u: int) -> bool:
    """True when available boundary margin a is strictly below h(u)."""
    if a < 0:
        return True
    return 4 * a * a * (Q2 + u * u) < XS2 * (Q + u) * (Q + u)


def verify(path: pathlib.Path) -> None:
    cert = path.read_bytes()
    nbytes = len(cert)
    cursor = 0

    # Preorder traversal. Stack stores only deferred right children; the current
    # left child lives in these scalar locals, avoiding millions of Box objects.
    xl, xh, yl, yh, tl, th, depth = LO, HI, LO, HI, -Q, Q, 0
    stack: list[tuple[int, int, int, int, int, int, int]] = []

    nodes = covered = impossible = branches = 0
    max_depth = 0
    witness_counts = [0] * 16

    while True:
        if cursor >= nbytes:
            raise ValueError(f"certificate ends early at node {nodes + 1}")
        op = cert[cursor]
        cursor += 1
        nodes += 1
        if depth > max_depth:
            max_depth = depth

        if op == 0:
            u = min_abs_t(tl, th)
            if not (
                half_extent_exceeds(xh, u)
                or half_extent_exceeds(LS - xl, u)
                or half_extent_exceeds(yh, u)
                or half_extent_exceeds(LS - yl, u)
            ):
                raise ValueError(f"false infeasibility claim at node {nodes}")
            impossible += 1

        elif 1 <= op <= 16:
            wi = op - 1
            pxs = PXS[wi]
            pys = PYS[wi]
            dx0 = pxs - xh * DEN
            dx1 = pxs - xl * DEN
            dy0 = pys - yh * DEN
            dy1 = pys - yl * DEN

            z0 = tl * dy0
            z1 = tl * dy1
            z2 = th * dy0
            z3 = th * dy1
            lo = min(z0, z1, z2, z3)
            hi = max(z0, z1, z2, z3)
            a0 = dx0 * Q + lo
            a1 = dx1 * Q + hi
            ma = max(abs(a0), abs(a1))

            nt0 = -th
            nt1 = -tl
            z0 = nt0 * dx0
            z1 = nt0 * dx1
            z2 = nt1 * dx0
            z3 = nt1 * dx1
            lo = min(z0, z1, z2, z3)
            hi = max(z0, z1, z2, z3)
            b0 = lo + dy0 * Q
            b1 = hi + dy1 * Q
            mb = max(abs(b0), abs(b1))

            u = min_abs_t(tl, th)
            rhs = (Q2 + u * u) * COVER_SCALE
            if not (4 * ma * ma < rhs and 4 * mb * mb < rhs):
                raise ValueError(f"false witness {op} at node {nodes}")
            covered += 1
            witness_counts[wi] += 1

        elif 17 <= op <= 19:
            d = depth + 1
            if op == 17:
                m = (xl + xh) // 2
                if m == xl or m == xh:
                    raise ValueError(f"x grid exhausted at node {nodes}")
                stack.append((m, xh, yl, yh, tl, th, d))
                xh = m
            elif op == 18:
                m = (yl + yh) // 2
                if m == yl or m == yh:
                    raise ValueError(f"y grid exhausted at node {nodes}")
                stack.append((xl, xh, m, yh, tl, th, d))
                yh = m
            else:
                m = (tl + th) // 2
                if m == tl or m == th:
                    raise ValueError(f"t grid exhausted at node {nodes}")
                stack.append((xl, xh, yl, yh, m, th, d))
                th = m
            depth = d
            branches += 1
            continue
        else:
            raise ValueError(f"unknown opcode {op} at node {nodes}")

        # Leaf: continue with the next deferred right subtree, or finish.
        if stack:
            xl, xh, yl, yh, tl, th, depth = stack.pop()
        else:
            break

    if cursor != nbytes:
        raise ValueError(f"{nbytes - cursor} trailing certificate bytes")
    if covered + impossible != branches + 1:
        raise ValueError("certificate is not a full binary partition tree")

    print("PYTHON_INTEGER_CERTIFICATE_VALID")
    print("L=4456575/1000000")
    print(f"nodes={nodes}")
    print(f"split={branches}")
    print(f"covered={covered}")
    print(f"infeasible={impossible}")
    print(f"max_depth={max_depth}")
    print("witness_counts=" + ",".join(map(str, witness_counts)))


if __name__ == "__main__":
    verify(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "square17_lb_4p456575.cert"))
