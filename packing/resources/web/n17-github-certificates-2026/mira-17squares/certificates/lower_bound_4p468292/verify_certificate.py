#!/usr/bin/env python3
"""Independent arbitrary-integer verifier for s(17) > 4.468292."""
from __future__ import annotations

import pathlib
import sys
from dataclasses import dataclass

ST = 1 << 40
SX = 1_000_000 * ST
PD = 10_000_000
LNUM = 4_468_292
LS = LNUM * ST
LO = 500_000 * ST
HI = (LNUM - 500_000) * ST

POINTS = (
    (9633740,9849850), (16317845,9829523), (25287879,9446006), (34682923,9443212),
    (9999997,17580956), (19993909,17929744), (29988027,18272588), (35451063,18219620),
    (9172158,26508741), (14694893,26410332), (24689011,26753176), (34682923,27101964),
    (9999997,35239708), (19395041,35236914), (28365087,34853407), (34687946,34687946),
)
TRIANGLES = (
    (0,1,4), (1,2,5), (1,4,5), (2,3,6), (2,5,6), (3,6,7),
    (4,5,9), (4,8,9), (5,6,10), (5,9,10), (6,7,11), (6,10,11),
    (8,9,12), (9,10,13), (9,12,13), (10,11,14), (10,13,14), (11,14,15),
)

@dataclass(frozen=True, slots=True)
class Box:
    x0: int; x1: int; y0: int; y1: int; t0: int; t1: int; depth: int


def min_abs_t(b: Box) -> int:
    if b.t0 <= 0 <= b.t1:
        return 0
    return min(abs(b.t0), abs(b.t1))


def less_than_half_extent(a: int, u: int) -> bool:
    if a < 0:
        return True
    return 4 * a * a * (ST * ST + u * u) < SX * SX * (ST + u) * (ST + u)


def infeasible(b: Box) -> bool:
    u = min_abs_t(b)
    return (
        less_than_half_extent(b.x1, u)
        or less_than_half_extent(LS - b.x0, u)
        or less_than_half_extent(b.y1, u)
        or less_than_half_extent(LS - b.y0, u)
    )


def point_covers(p: tuple[int, int], b: Box) -> bool:
    px, py = p
    dx0 = px * SX - b.x1 * PD
    dx1 = px * SX - b.x0 * PD
    dy0 = py * SX - b.y1 * PD
    dy1 = py * SX - b.y0 * PD

    products = (b.t0 * dy0, b.t0 * dy1, b.t1 * dy0, b.t1 * dy1)
    a0 = dx0 * ST + min(products)
    a1 = dx1 * ST + max(products)
    ma = max(abs(a0), abs(a1))

    nt0, nt1 = -b.t1, -b.t0
    products = (nt0 * dx0, nt0 * dx1, nt1 * dx0, nt1 * dx1)
    b0 = min(products) + dy0 * ST
    b1 = max(products) + dy1 * ST
    mb = max(abs(b0), abs(b1))

    u = min_abs_t(b)
    rhs = (ST * ST + u * u) * PD * PD * SX * SX
    return 4 * ma * ma < rhs and 4 * mb * mb < rhs


def cross(a: tuple[int, int], b: tuple[int, int], c: tuple[int, int]) -> int:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def triangle_edges_strict(tr: tuple[int, int, int]) -> bool:
    ps = [POINTS[i] for i in tr]
    for i in range(3):
        for j in range(i + 1, 3):
            dx = ps[i][0] - ps[j][0]
            dy = ps[i][1] - ps[j][1]
            if dx * dx + dy * dy >= PD * PD:
                return False
    return True


def edge_cross_center(a: tuple[int, int], b: tuple[int, int], qx: int, qy: int) -> int:
    ex, ey = b[0] - a[0], b[1] - a[1]
    rx = qx * PD - a[0] * SX
    ry = qy * PD - a[1] * SX
    return ex * ry - ey * rx


def triangle_covers(index: int, b: Box) -> bool:
    tr = list(TRIANGLES[index])
    if not triangle_edges_strict(tuple(tr)):
        return False
    if cross(POINTS[tr[0]], POINTS[tr[1]], POINTS[tr[2]]) < 0:
        tr[1], tr[2] = tr[2], tr[1]
    a, c, d = (POINTS[tr[0]], POINTS[tr[1]], POINTS[tr[2]])
    for qx in (b.x0, b.x1):
        for qy in (b.y0, b.y1):
            if edge_cross_center(a, c, qx, qy) <= 0:
                return False
            if edge_cross_center(c, d, qx, qy) <= 0:
                return False
            if edge_cross_center(d, a, qx, qy) <= 0:
                return False
    return True


def split(b: Box, dim: int) -> tuple[Box, Box]:
    depth = b.depth + 1
    if dim == 0:
        m = (b.x0 + b.x1) // 2
        if m in (b.x0, b.x1): raise ValueError("x grid exhausted")
        return Box(b.x0,m,b.y0,b.y1,b.t0,b.t1,depth), Box(m,b.x1,b.y0,b.y1,b.t0,b.t1,depth)
    if dim == 1:
        m = (b.y0 + b.y1) // 2
        if m in (b.y0, b.y1): raise ValueError("y grid exhausted")
        return Box(b.x0,b.x1,b.y0,m,b.t0,b.t1,depth), Box(b.x0,b.x1,m,b.y1,b.t0,b.t1,depth)
    if dim == 2:
        m = (b.t0 + b.t1) // 2
        if m in (b.t0, b.t1): raise ValueError("t grid exhausted")
        return Box(b.x0,b.x1,b.y0,b.y1,b.t0,m,depth), Box(b.x0,b.x1,b.y0,b.y1,m,b.t1,depth)
    raise ValueError("bad split dimension")


def verify(path: pathlib.Path) -> None:
    cert = path.read_bytes()
    stack = [Box(LO, HI, LO, HI, -ST, ST, 0)]
    cursor = nodes = branches = covered = triangles = impossible = max_depth = 0

    while stack:
        if cursor >= len(cert):
            raise ValueError(f"early EOF at node {nodes + 1}")
        op = cert[cursor]
        cursor += 1
        b = stack.pop()
        nodes += 1
        max_depth = max(max_depth, b.depth)

        if op == 0:
            if not infeasible(b): raise ValueError(f"false infeasible leaf at node {nodes}")
            impossible += 1
        elif 1 <= op <= 16:
            if not point_covers(POINTS[op - 1], b):
                raise ValueError(f"false point leaf {op} at node {nodes}")
            covered += 1
        elif 17 <= op <= 19:
            a, c = split(b, op - 17)
            stack.append(c); stack.append(a)
            branches += 1
        elif 20 <= op < 20 + len(TRIANGLES):
            if not triangle_covers(op - 20, b):
                raise ValueError(f"false triangle leaf {op - 20} at node {nodes}")
            triangles += 1
        else:
            raise ValueError(f"unknown opcode {op} at node {nodes}")

    if cursor != len(cert): raise ValueError(f"{len(cert)-cursor} trailing bytes")
    if covered + triangles + impossible != branches + 1:
        raise ValueError("certificate is not a full binary partition tree")

    print("PYTHON_INTEGER_CERTIFICATE_VALID_4P468292")
    print("L=4468292/1000000")
    print(f"nodes={nodes}")
    print(f"split={branches}")
    print(f"covered={covered}")
    print(f"triangle={triangles}")
    print(f"infeasible={impossible}")
    print(f"max_depth={max_depth}")


if __name__ == "__main__":
    verify(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "square17_lb_4p468292.cert"))
