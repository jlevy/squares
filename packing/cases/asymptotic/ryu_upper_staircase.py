"""Exact build and check of the staircase end packing behind Ryu's k^{2/5} bound on c*(k).

Theorem 1.2 of Sungjoon Ryu's preprint "Packing k^2-c unit squares: an upper bound of
order k^{3/8} for the deficiency" (issues #471 and #486) fills each of the four band ends
Reg(y) of the L-shaped frame by the staircase (S1)-(S6) of Lemma 7.3: columns of one
common tilt t = ceil(t* Q)/Q whose lowest squares are replaced by horizontal layers, and
left-wall rows. Lemma 7.3 bounds the uncovered area by B*, and Corollary 7.4 bounds B* by
Phi(x) b^{2/3} with x = b^{-1/3} for every lift y in the window
[kappa b^{2/3}, kappa b^{2/3} + 2], kappa = 3/4, with sigma_0 = sin(theta),
mu = tan(theta), tan(theta/2) = b/(b^2-1) and Q the least power of 2 at least 16b.

Written from Section 7 of the text and not from the source's programs (the release does
not contain the author's construction of the proof; ``stair_dump.py`` builds a tuned
variant), this module builds that packing in exact rationals for given (b, y), decides it
(every piece a 1 x n rectangle, every vertex in Reg(y), interiors of every two pieces
with overlapping bounding boxes disjoint by an exact separating-axis test), computes the
uncovered area U exactly, and decides U <= B* exactly and B* <= Phi(x) b^{2/3} on
``mpmath`` intervals. The window is decided exactly. It tests the lemma at sizes the
proof does not need (Corollary 7.4 is stated for b >= 10^4); it is not the proof.

Run from ``packing/``::

    uv run --frozen --all-extras --group dev python -m \\
        cases.asymptotic.ryu_upper_staircase [B Y ...]   # Y as p/q; default: four runs
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from typing import Any

from gmpy2 import mpq

from cases.asymptotic.ryu_upper_constants import iv, phi_terms

type Point = tuple[mpq, mpq]
type Piece = tuple[int, tuple[Point, Point, Point, Point]]

#: The review's four runs: two small sizes and two lifts in the window at b = 10^4.
DEFAULT_RUNS = ((400, "41"), (1600, "103"), (10000, "1393/4"), (10000, "1399/4"))
KAPPA = mpq(3, 4)


def floor(value: mpq) -> int:
    return int(value.numerator) // int(value.denominator)


def parse(text: str) -> mpq:
    numerator, slash, denominator = text.partition("/")
    return mpq(int(numerator), int(denominator)) if slash else mpq(int(numerator))


def in_window(b: int, y: mpq) -> bool:
    """kappa b^{2/3} <= y <= kappa b^{2/3} + 2, decided by cubing."""
    low = y >= 0 and (y / KAPPA) ** 3 >= b * b
    high = y - 2 <= 0 or ((y - 2) / KAPPA) ** 3 <= b * b
    return bool(low and high)


@dataclass
class Staircase:
    b: int
    y: str
    in_window: bool
    m: int
    q: int
    t: str
    slabs: int
    columns: int
    layers: int
    wedge_rows: int
    squares: int
    pieces: int
    bad_shape: int
    bad_containment: int
    box_pairs: int
    overlaps: int
    uncovered: float
    b_star: float
    phi_bound: float
    uncovered_over_b23: float
    b_star_over_b23: float
    u_at_most_b_star: bool
    b_star_at_most_phi: bool
    passed: bool


def build(b: int, y: mpq, tilt_offset: int = 0) -> tuple[list[Piece], dict[str, Any]]:
    """(S1)-(S6) in Reg(y); ``tilt_offset`` moves the tilt that many grid steps (a control)."""
    t_band = mpq(b, b * b - 1)
    cos_b, sin_b = (1 - t_band**2) / (1 + t_band**2), 2 * t_band / (1 + t_band**2)
    width, mu, sigma = b * cos_b + sin_b, sin_b / cos_b, sin_b

    def ceiling(x: mpq) -> mpq:
        return y + (x - sigma) * mu

    g0, g_bar = ceiling(mpq(0)), ceiling(width)
    if not g0 > 1:
        raise ValueError("g0 <= 1: the lift is below Lemma 7.3's range")
    delta_ceiling = width * mu
    m = floor(g_bar) + 1  # (S1)
    delta = m - g0
    q = 1
    while q < 16 * b:
        q *= 2
    d_m = m + g0

    def f(t: mpq) -> mpq:
        return d_m * t * t - 2 * t - delta

    # (S2): t = ceil(t* Q)/Q is the least grid point with F(t) >= 0, since F < 0 on
    # [0, t*) and F >= 0 on [t*, 1] (Lemma 7.2); F(0) = -delta < 0 and F(1) = 2 g0 - 2 > 0.
    low, high = 0, q
    while high - low > 1:
        middle = (low + high) // 2
        if f(mpq(middle, q)) >= 0:
            high = middle
        else:
            low = middle
    u = high + tilt_offset
    t = mpq(u, q)
    if not 0 < t < 1:
        raise ValueError("the tilt is not in (0, 1)")
    ca, sa = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
    ta, se = sa / ca, 1 / ca
    if not m * ta + se <= width:
        raise ValueError("m tan(alpha) + sec(alpha) > w: no slab")
    xi: list[mpq] = []
    while m * ta + (len(xi) + 1) * se <= width:  # (S3)
        xi.append(m * ta + len(xi) * se)
    slabs = len(xi)
    xi_end = m * ta + slabs * se
    columns: list[tuple[mpq, int, int]] = []
    js: list[int] = []
    for x in xi:  # (S4)
        j = floor((ceiling(x - m * ta) - m * ca - sa) / (1 - ca))
        js.append(j)
        columns.append((x, j, m - j))

    def a_of(j: int) -> mpq:
        p = sum(1 for value in js if value <= j)
        return (xi[p] if p < slabs else xi_end) - j * ta

    last = -1  # (S5)
    for j in range(floor(g_bar) + 1):
        if ceiling(a_of(j)) >= j + 1:
            last = j
        else:
            break
    layers = [(a_of(j), j, floor(width - a_of(j))) for j in range(last + 1)]
    layers = [layer for layer in layers if layer[2] >= 1]
    wedge = [(r, floor((m - r - 1) * ta)) for r in range(floor(g0))]  # (S6)
    wedge = [row for row in wedge if row[1] >= 1]
    pieces: list[Piece] = []
    for x, j, n in columns:
        px, py = x - j * ta, mpq(j)
        corners = (
            (px, py),
            (px + ca, py + sa),
            (px + ca - n * sa, py + sa + n * ca),
            (px - n * sa, py + n * ca),
        )
        pieces.append((n, corners))
    for a, j, length in layers:
        pieces.append(
            (
                length,
                ((a, mpq(j)), (a, mpq(j + 1)), (a + length, mpq(j + 1)), (a + length, mpq(j))),
            )
        )
    for r, length in wedge:
        pieces.append(
            (
                length,
                (
                    (mpq(0), mpq(r)),
                    (mpq(0), mpq(r + 1)),
                    (mpq(length), mpq(r + 1)),
                    (mpq(length), mpq(r)),
                ),
            )
        )
    area = y * width + (width * width / 2 - sigma * width) * mu
    squares = sum(n for n, _ in pieces)
    omega = se + g_bar * ta
    b_star = (
        width * sa
        + width * (1 - ca)
        + delta_ceiling * (se + m * ta)
        + floor(g_bar) * (1 + ta / 2)
        + (1 + mu * omega) * omega
        + floor(g0) * (1 + ta / 2)
        + (delta + 1) * ta * (1 + mu * (delta + 1) * ta)
    )
    info: dict[str, Any] = {
        "width": width,
        "mu": mu,
        "sigma": sigma,
        "m": m,
        "q": q,
        "t": t,
        "slabs": slabs,
        "columns": len(columns),
        "layers": len(layers),
        "wedge_rows": len(wedge),
        "squares": squares,
        "uncovered": area - squares,
        "b_star": b_star,
    }
    return pieces, info


def separated(first: tuple[Point, ...], second: tuple[Point, ...]) -> bool:
    for rectangle in (first, second):
        (x0, y0), (x1, y1), _, (x3, y3) = rectangle
        for ax, ay in ((x1 - x0, y1 - y0), (x3 - x0, y3 - y0)):
            a = [x * ax + y * ay for x, y in first]
            b = [x * ax + y * ay for x, y in second]
            if max(a) <= min(b) or max(b) <= min(a):
                return True
    return False


def decide(
    pieces: list[Piece], width: mpq, sigma: mpq, mu: mpq, y: mpq
) -> tuple[int, int, int, int]:
    """Bad shapes, vertices outside Reg(y), bounding-box pairs and overlaps."""
    bad_shape = bad_containment = 0
    boxes: list[tuple[mpq, mpq, mpq, mpq]] = []
    for n, corners in pieces:
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = corners
        dx, dy, ex, ey = x1 - x0, y1 - y0, x3 - x0, y3 - y0
        if not (
            n >= 1
            and dx * dx + dy * dy == 1
            and dx * ex + dy * ey == 0
            and ex * ex + ey * ey == n * n
            and x2 == x1 + ex
            and y2 == y1 + ey
        ):
            bad_shape += 1
        if any(not (0 <= x <= width and 0 <= v <= y + (x - sigma) * mu) for x, v in corners):
            bad_containment += 1
        xs, ys = [p[0] for p in corners], [p[1] for p in corners]
        boxes.append((min(xs), max(xs), min(ys), max(ys)))
    order = sorted(range(len(boxes)), key=lambda index: boxes[index][0])
    pairs = overlaps = 0
    for position, i in enumerate(order):
        for j in order[position + 1 :]:
            if boxes[j][0] >= boxes[i][1]:
                break
            if boxes[j][2] >= boxes[i][3] or boxes[i][2] >= boxes[j][3]:
                continue
            pairs += 1
            overlaps += not separated(pieces[i][1], pieces[j][1])
    return bad_shape, bad_containment, pairs, overlaps


def run(b: int, y_text: str, tilt_offset: int = 0) -> Staircase:
    """Build, decide and bound one end packing."""
    iv.dps = 50
    y = parse(y_text)
    pieces, info = build(b, y, tilt_offset)
    bad_shape, bad_containment, pairs, overlaps = decide(
        pieces, info["width"], info["sigma"], info["mu"], y
    )
    x = iv.mpf(b) ** (iv.mpf(-1) / 3)
    phi = phi_terms(x)["Phi"] * iv.mpf(b) ** (iv.mpf(2) / 3)
    b_star = iv.mpf(int(info["b_star"].numerator)) / int(info["b_star"].denominator)
    u_ok = bool(info["uncovered"] <= info["b_star"])
    phi_ok = bool(b_star.b <= phi.a)
    valid = bad_shape == 0 and bad_containment == 0 and overlaps == 0
    return Staircase(
        b=b,
        y=y_text,
        in_window=in_window(b, y),
        m=info["m"],
        q=info["q"],
        t=str(info["t"]),
        slabs=info["slabs"],
        columns=info["columns"],
        layers=info["layers"],
        wedge_rows=info["wedge_rows"],
        squares=int(info["squares"]),
        pieces=len(pieces),
        bad_shape=bad_shape,
        bad_containment=bad_containment,
        box_pairs=pairs,
        overlaps=overlaps,
        uncovered=round(float(info["uncovered"]), 6),
        b_star=round(float(info["b_star"]), 6),
        phi_bound=round(float(phi.b), 6),
        uncovered_over_b23=round(float(info["uncovered"]) / b ** (2 / 3), 4),
        b_star_over_b23=round(float(info["b_star"]) / b ** (2 / 3), 4),
        u_at_most_b_star=u_ok,
        b_star_at_most_phi=phi_ok,
        passed=valid and u_ok and phi_ok,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("runs", nargs="*", help="pairs B Y, Y an integer or p/q")
    args = parser.parse_args(argv)
    if len(args.runs) % 2:
        parser.error("give B and Y in pairs")
    runs = [(int(args.runs[i]), args.runs[i + 1]) for i in range(0, len(args.runs), 2)]
    results = [run(b, y) for b, y in runs or DEFAULT_RUNS]
    passed = all(result.passed for result in results)
    print(json.dumps({"passed": passed, "runs": [asdict(r) for r in results]}, indent=1))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
