"""Exact check of the L-shaped packings behind Ryu's c*(k) <= 8 ceil(sqrt(k-4)) - 1.

Sungjoon Ryu's preprint "Packing k^2-c unit squares: an upper bound of order k^{3/8} for
the deficiency" (issues #471 and #486; version 1.0 retained in
``packing/resources/web/squarepacker-k2-minus-c-upper-2026-10-09/source/paper/``, the
statements unchanged in version 1.1) bounds c*(k) = max{c : s(k^2 - c) = k} by an
explicit packing: a (k-b)^2 grid and two bands of rows of b unit squares tilted by the
rational angle of Lemma 4.2, which hold N(k,b) = (k-b)^2 + b(R(k) + R(k-b)) squares in a
square of side S < k (Theorem 1.3), so c*(k) <= k^2 - N(k,b) - 1 (Lemma 2.2).

Written from Sections 3-5 of the text and not from any program of the source, this
module does two things. For every 2 <= b <= k <= ``packings`` with (k,b) != (2,2) it
builds that packing in exact rationals and decides it: S < k, the length conditions (L1)
and (L2), every vertex in [0,S]^2, and the interiors of every two squares whose bounding
boxes overlap disjoint by an exact separating-axis test; the number of squares must be
N(k,b). For every 2 <= b <= k <= ``formulas`` it decides, in integers and fractions, the
count (5.1) with its equality case, Theorem 1.3's c*(k) < 6b + 4k/b - 3, Proposition
1.5's k^2 - N(k,b) > 8 sqrt(k) - 14, Theorem 1.4 with b = ceil(sqrt(k-4)), Corollary 5.1's
c*(k) < 4 sqrt(6) sqrt(k), and Remark 5.2's statement that both floors of (5.1) are 1 for
k >= 23. Every square root is compared by squaring integers, so nothing here is floating
point. The formulas beyond ``packings`` are arithmetic about N(k,b); that N(k,b) counts a
valid packing there is the paper's Lemma 4.3, which the built packings test only below.

Run from ``packing/``::

    uv run --frozen --all-extras --group dev python -m \\
        cases.asymptotic.ryu_upper_l_packing [--packings 30] [--formulas 2000]
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from fractions import Fraction
from math import isqrt

from cases.asymptotic.ryu_k2_minus_c_constants import Check

type Point = tuple[Fraction, Fraction]
type Square = tuple[Point, Point, Point, Point]


def ceil_sqrt(n: int) -> int:
    """The least integer b >= 0 with b^2 >= n."""
    root = isqrt(n)
    return root if root * root == n else root + 1


def rows(length: int, b: int) -> int:
    """R(L) = max(0, ceil((L - h0) gamma0)) with h0 = (3b^2-1)/D, gamma0 = (b^2-1)/D."""
    d = b * b + 1
    value = (Fraction(length) - Fraction(3 * b * b - 1, d)) * Fraction(b * b - 1, d)
    return max(0, -((-value.numerator) // value.denominator))


def count(k: int, b: int) -> int:
    """N(k,b) = (k-b)^2 + b (R(k) + R(k-b))."""
    return (k - b) ** 2 + b * (rows(k, b) + rows(k - b, b))


def eta(k: int, b: int) -> tuple[Fraction, Fraction]:
    """The eta and eta' of the proof of Theorem 1.3."""
    d = b * b + 1
    first = Fraction(2 * k - 10, d) + Fraction(8, d * d)
    return first, first - Fraction(2 * b, d)


def floor(value: Fraction) -> int:
    return value.numerator // value.denominator


def angle(k: int, b: int) -> tuple[Fraction, Fraction]:
    """Lemma 4.2's cos and sin of theta = 2 arctan(p/q), p = M, q = bM - 1, M = 14kb^2 + 1."""
    p = 14 * k * b * b + 1
    q = b * p - 1
    return Fraction(q * q - p * p, q * q + p * p), Fraction(2 * p * q, p * p + q * q)


def separated(first: Square, second: Square) -> bool:
    """Whether two rectangles have disjoint interiors, decided on their edge directions."""
    for rectangle in (first, second):
        (x0, y0), (x1, y1), _, (x3, y3) = rectangle
        for ax, ay in ((x1 - x0, y1 - y0), (x3 - x0, y3 - y0)):
            a = [x * ax + y * ay for x, y in first]
            b = [x * ax + y * ay for x, y in second]
            if max(a) <= min(b) or max(b) <= min(a):
                return True
    return False


@dataclass(frozen=True)
class Packing:
    k: int
    b: int
    side: Fraction
    squares: tuple[Square, ...]
    length_conditions: bool


def build(k: int, b: int) -> Packing:
    """The grid and the two bands of Section 4 with Lemma 4.2's angle."""
    cos, sin = angle(k, b)
    side = k - b + b * cos + sin
    height, spacing = b * sin + cos, 1 / cos
    squares: list[Square] = []
    for i in range(k - b):
        for j in range(k - b):
            fi, fj = Fraction(i), Fraction(j)
            squares.append(((fi, fj), (fi + 1, fj), (fi + 1, fj + 1), (fi, fj + 1)))
    r1, r2 = rows(k, b), rows(k - b, b)
    conditions = (r1 == 0 or (r1 - 1) * spacing + height <= side) and (
        r2 == 0 or (r2 - 1) * spacing + height <= k - b
    )
    for band_rows, reflect in ((r1, False), (r2, True)):
        for j in range(band_rows):
            px, py = k - b + sin, j * spacing
            for i in range(b):
                corners: list[Point] = []
                for alpha, beta in ((i, 0), (i + 1, 0), (i + 1, 1), (i, 1)):
                    x = px + alpha * cos - beta * sin
                    y = py + alpha * sin + beta * cos
                    corners.append((y, x) if reflect else (x, y))
                squares.append((corners[0], corners[1], corners[2], corners[3]))
    return Packing(k, b, side, tuple(squares), conditions)


def defects(packing: Packing) -> list[str]:
    """Everything that keeps the packing from being N(k,b) squares in [0,S]^2 with S < k."""
    found: list[str] = []
    if not packing.side < packing.k:
        found.append("S >= k")
    if not packing.length_conditions:
        found.append("(L1) or (L2) fails")
    if len(packing.squares) != count(packing.k, packing.b):
        found.append(f"{len(packing.squares)} squares, N(k,b) = {count(packing.k, packing.b)}")
    if any(
        not (0 <= c <= packing.side) for square in packing.squares for p in square for c in p
    ):
        found.append("a vertex outside [0,S]^2")
    boxes = [
        (min(p[0] for p in s), max(p[0] for p in s), min(p[1] for p in s), max(p[1] for p in s))
        for s in packing.squares
    ]
    order = sorted(range(len(boxes)), key=lambda index: boxes[index][0])
    for position, i in enumerate(order):
        for j in order[position + 1 :]:
            if boxes[j][0] >= boxes[i][1]:
                break
            if boxes[j][2] >= boxes[i][3] or boxes[i][2] >= boxes[j][3]:
                continue
            if not separated(packing.squares[i], packing.squares[j]):
                found.append(f"squares {i} and {j} overlap")
                return found
    return found


def check_packings(limit: int) -> tuple[Check, ...]:
    """Build and decide the packing for every 2 <= b <= k <= limit, (k,b) != (2,2)."""
    failures: list[str] = []
    built = 0
    for k in range(2, limit + 1):
        for b in range(2, k + 1):
            if (k, b) == (2, 2):
                continue
            built += 1
            failures += [f"(k,b) = ({k},{b}): {d}" for d in defects(build(k, b))]
    return (
        Check(
            f"Theorem 1.3 packings, 2 <= b <= k <= {limit}",
            "Lemmas 3.3, 4.1-4.3",
            not failures,
            f"{built} packings built exactly; failures: {failures[:5] or 'none'}",
        ),
    )


def check_formulas(limit: int) -> tuple[Check, ...]:
    """The counting statements of Sections 1 and 5 for every 2 <= b <= k <= limit."""
    count_51: list[tuple[int, int]] = []
    theorem_13: list[tuple[int, int]] = []
    proposition_15: list[tuple[int, int]] = []
    for k in range(2, limit + 1):
        for b in range(2, k + 1):
            deficit = k * k - count(k, b)
            first, second = eta(k, b)
            exact = 6 * b + b * (floor(first) + floor(second))
            if deficit > exact or (k - b >= 2 and deficit != exact):
                count_51.append((k, b))
            if not deficit - 1 < 6 * b + Fraction(4 * k, b) - 3:
                theorem_13.append((k, b))
            # deficit > 8 sqrt(k) - 14  <=>  deficit + 14 > 0 and (deficit + 14)^2 > 64 k.
            if not (deficit + 14 > 0 and (deficit + 14) ** 2 > 64 * k):
                proposition_15.append((k, b))
    theorem_14: list[int] = []
    corollary_51: list[int] = []
    remark_52: list[int] = []
    first_below_k_minus_1 = None
    not_below_k_minus_1: list[int] = []
    for k in range(6, limit + 1):
        b = ceil_sqrt(k - 4)
        bound = 8 * b - 1
        # 8b - 1 < 8 sqrt(k-4) + 7  <=>  b - 1 < sqrt(k-4)  <=>  (b-1)^2 < k - 4.
        if not (k * k - count(k, b) - 1 <= bound and (b - 1) ** 2 < k - 4):
            theorem_14.append(k)
        # Corollary 5.1 takes b = ceil(sqrt(2k/3)): the least b with 3b^2 >= 2k.
        b_star = ceil_sqrt(-((-2 * k) // 3))
        value = k * k - count(k, b_star) - 1
        if not (value < 0 or value * value < 96 * k):
            corollary_51.append(k)
        if k >= 23 and any(floor(x) != 1 for x in eta(k, b)):
            remark_52.append(k)
        if first_below_k_minus_1 is None and bound < k - 1:
            first_below_k_minus_1 = k
        if k >= 60 and not bound < k - 1:
            not_below_k_minus_1.append(k)
    at_22 = tuple(floor(x) for x in eta(22, ceil_sqrt(18)))
    return (
        Check(
            f"(5.1) with its equality case, 2 <= b <= k <= {limit}",
            "proof of Theorem 1.3, (5.1)",
            not count_51,
            f"failures {count_51[:5] or 'none'}",
        ),
        Check(
            f"Theorem 1.3: k^2 - N(k,b) - 1 < 6b + 4k/b - 3, 2 <= b <= k <= {limit}",
            "Theorem 1.3",
            not theorem_13,
            f"failures {theorem_13[:5] or 'none'}",
        ),
        Check(
            f"Proposition 1.5: k^2 - N(k,b) > 8 sqrt(k) - 14, 2 <= b <= k <= {limit}",
            "Proposition 1.5",
            not proposition_15,
            f"failures {proposition_15[:5] or 'none'}",
        ),
        Check(
            "Theorem 1.4: k^2 - N(k,b) - 1 <= 8b - 1 < 8 sqrt(k-4) + 7, b = ceil(sqrt(k-4)), "
            f"6 <= k <= {limit}",
            "Theorem 1.4 and its proof",
            not theorem_14,
            f"failures {theorem_14[:5] or 'none'}",
        ),
        Check(
            f"Corollary 5.1: c*(k) < 4 sqrt(6) sqrt(k), 6 <= k <= {limit}",
            "Corollary 5.1",
            not corollary_51,
            f"failures {corollary_51[:5] or 'none'}",
        ),
        Check(
            f"Remark 5.2: both floors of (5.1) are 1 for 23 <= k <= {limit}, not at k = 22",
            "Remark 5.2",
            not remark_52 and at_22 != (1, 1),
            f"failures {remark_52[:5] or 'none'}; floors at k = 22: {at_22}",
        ),
        Check(
            "first k with 8 ceil(sqrt(k-4)) - 1 < k - 1",
            "Section 1 (the comparison with c*(k) <= k - 1)",
            first_below_k_minus_1 == 65,
            str(first_below_k_minus_1),
        ),
        # The bound is below k - 1 at k = 65..68 and again only from k = 73 (where
        # ceil(sqrt(k-4)) = 9 gives 71 >= k - 1 for k <= 72); the review's "from k = 65
        # on" overstates it.
        Check(
            f"8 ceil(sqrt(k-4)) - 1 >= k - 1 for 60 <= k <= {limit} exactly at 60-64 and 69-72",
            "Section 1 (the comparison with c*(k) <= k - 1)",
            limit < 73 or not_below_k_minus_1 == [60, 61, 62, 63, 64, 69, 70, 71, 72],
            str(not_below_k_minus_1),
        ),
    )


def theorem_14_table(limit: int = 30) -> list[dict[str, int]]:
    """For 6 <= k <= limit: b, N(k,b), the construction's k^2 - N - 1 and the bound 8b - 1."""
    out: list[dict[str, int]] = []
    for k in range(6, limit + 1):
        b = ceil_sqrt(k - 4)
        n = count(k, b)
        out.append({"k": k, "b": b, "N": n, "construction": k * k - n - 1, "bound": 8 * b - 1})
    return out


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument(
        "--packings", type=int, default=30, help="build packings for k up to this"
    )
    parser.add_argument(
        "--formulas", type=int, default=2000, help="check formulas for k up to this"
    )
    args = parser.parse_args(argv)
    checks = (*check_packings(args.packings), *check_formulas(args.formulas))
    passed = all(check.holds for check in checks)
    report = {
        "passed": passed,
        "packings": args.packings,
        "formulas": args.formulas,
        "checks": [asdict(check) for check in checks],
        "theorem_1_4_table": theorem_14_table(),
    }
    print(json.dumps(report, indent=1))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
