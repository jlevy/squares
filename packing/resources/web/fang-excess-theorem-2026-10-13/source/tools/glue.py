#!/usr/bin/env python3
"""Glue a squeezable rectangle A, a second packing B (square or rectangle) and two integer blocks
into one square packing: Lemma 3 of the note, in exact rational arithmetic.

Standalone, standard library only (Python 3.8+). Same layout, count and strictification as
squarepack/glue.py in the research repo; on every certificate in this bundle the output is
identical to it apart from the `#` comment line.

    python3 tools/glue.py --rect A.cert --second B.cert --out C.cert [--closed] [--d 1/10000]

A: rectangle certificate `n W H` with box a x b = ceil W x ceil H, a > b, squeeze
   d_A = min(a - W, b - H) > 0.
B: square certificate `n S` with box m x m (m = ceil S, d_B = m - S), or rectangle certificate
   `n W H` with box a' x b' = ceil W x ceil H, a' > b', d_B = min(a' - W, b' - H) > 0.

With n = b + b', c = n - a' and d = min(d_A, d_B, 1/2) (Lemma 3; needs d > 0, n >= a, c >= 0,
c <= a - d), the square [0, n - d]^2 holds

    A  in [0, a - d] x [n - b, n - d]       (shifted up: its top at n - d)
    D  (n - a) x b aligned unit squares in [a - d, n - d] x [n - d - b, n - d]
    C  c x (n - b) aligned unit squares in [0, c] x [0, n - b]
    B  in [c, n - d] x [0, n - d - b]       (shifted right: its right side at n - d)

and the count is n^2 - waste_A - waste_B (asserted). The integer blocks touch each other, so
the composite at side n - d is valid only in the closed sense; by default every centre and the
side are scaled by 1 + 2^-64 about the origin, which makes every margin strictly positive while
the side stays below n (asserted: 2^-64 < d / (n - d)). --closed writes the side n - d instead.

--d D (a rational such as 1/10000) uses the squeeze D instead of min(d_A, d_B, 1/2); it needs
0 < D <= min(d_A, d_B, 1/2), so both pieces fit in their boxes shrunk by D, and a piece squeezed
by more than D sits flush in the corner of its box as above. The side is then exactly n - D
(--closed) or (1 + 2^-64)(n - D). Gluing closed with one common D at every step of a chain and
scaling once at the end (centres and side by 1 + D / (2(n - D)), side n - D/2) is the uniform
construction behind the theorem.

Nothing is verified here beyond the layout: run `python3 verify.py C.cert --strict` (and
tools/verify_cert_daniel.py, tools/rectcheck.py) on the output.
"""
import argparse
import math
import os
import sys
from fractions import Fraction as Fr

HALF = Fr(1, 2)
EPS = Fr(1, 1 << 64)


class GlueError(ValueError):
    pass


# ---- certificates ------------------------------------------------------------------------------
class Cert:
    """n squares (x, y, t) in [0, W] x [0, H]; a square container has H == W."""

    def __init__(self, n, W, H, squares):
        self.n, self.W, self.H, self.squares = n, W, H, squares

    @property
    def is_square(self):
        return self.H == self.W


def read_cert(path):
    with open(path) as fh:
        rows = [l.split() for l in fh if l.strip() and not l.lstrip().startswith("#")]
    n, W = int(rows[0][0]), Fr(rows[0][1])
    H = Fr(rows[0][2]) if len(rows[0]) > 2 else W
    sq = [(Fr(r[0]), Fr(r[1]), Fr(r[2])) for r in rows[1 : n + 1]]
    if len(sq) != n:
        raise ValueError(f"{path}: expected {n} squares, got {len(sq)}")
    return Cert(n, W, H, sq)


def cert_text(cert, comment=None):
    lines = [f"# {comment}"] if comment else []
    lines.append(f"{cert.n} {cert.W}" if cert.is_square else f"{cert.n} {cert.W} {cert.H}")
    lines += [f"{x} {y} {t}" for x, y, t in cert.squares]
    return "\n".join(lines) + "\n"


# ---- the four regions --------------------------------------------------------------------------
def regions(a, b, a2, b2, d=Fr(0)):
    """(name, x0, x1, y0, y1) for A in an a x b box and B in an a2 x b2 box, squeeze d (0: the tiling)."""
    n = b + b2
    c = n - a2
    return [
        ("A", Fr(0), a - d, Fr(n - b), n - d),
        ("D", a - d, n - d, n - d - b, n - d),
        ("C", Fr(0), Fr(c), Fr(0), Fr(n - b)),
        ("B", Fr(c), n - d, Fr(0), n - d - b),
    ]


def check_regions(rs, side):
    """Assert each region lies in [0, side]^2 and interiors are pairwise disjoint; return the area sum."""
    area = 0
    for name, x0, x1, y0, y1 in rs:
        assert 0 <= x0 <= x1 <= side and 0 <= y0 <= y1 <= side, name
        area += (x1 - x0) * (y1 - y0)
    for i in range(len(rs)):
        for j in range(i + 1, len(rs)):
            _, ax0, ax1, ay0, ay1 = rs[i]
            _, bx0, bx1, by0, by1 = rs[j]
            assert ax1 <= bx0 or bx1 <= ax0 or ay1 <= by0 or by1 <= ay0, (rs[i][0], rs[j][0])
    return area


def block(x0, y0, cols, rows):
    return [(x0 + HALF + i, y0 + HALF + j, Fr(0)) for i in range(cols) for j in range(rows)]


# ---- Lemma 3 -----------------------------------------------------------------------------------
def glue(A, B, strict=True, d=None):
    """(certificate, info). Raises GlueError if the hypotheses of Lemma 3 fail. d: the squeeze to
    use (default min(d_A, d_B, 1/2)); a given d needs 0 < d <= min(d_A, d_B, 1/2)."""
    a, b = math.ceil(A.W), math.ceil(A.H)
    if a <= b:
        raise GlueError(f"need a > b for the rectangle A, got a = {a}, b = {b}")
    if B.is_square:
        a2 = b2 = math.ceil(B.W)
        d_B = a2 - B.W
    else:
        a2, b2 = math.ceil(B.W), math.ceil(B.H)
        if not (B.W > B.H and a2 > b2):
            raise GlueError(f"need W_B > H_B and a' > b' for a rectangle B, got a' = {a2}, b' = {b2}")
        d_B = min(a2 - B.W, b2 - B.H)
    d_A = min(a - A.W, b - A.H)
    if d is None:
        d = min(d_A, d_B, HALF)
        if d <= 0:
            raise GlueError(f"need d = min(d_A, d_B, 1/2) > 0, got d_A = {float(d_A):.3e}, d_B = {float(d_B):.3e}")
    else:
        d = Fr(d)
        if not 0 < d <= min(d_A, d_B, HALF):
            raise GlueError(f"need 0 < d <= min(d_A, d_B, 1/2) for the given d = {d}, got d_A = {float(d_A):.3e}, "
                            f"d_B = {float(d_B):.3e}")
    n = b + b2
    c = n - a2
    if n < a:
        raise GlueError(f"need n = b + b' >= a, got b = {b}, b' = {b2}, a = {a}")
    if c < 0:
        raise GlueError(f"need c = n - a' >= 0, got n = {n}, a' = {a2}")
    if a - d < c:
        raise GlueError(f"need c <= a - d (C and D would overlap), got a = {a}, c = {c}, d = {float(d)}")
    assert check_regions(regions(a, b, a2, b2), n) == n * n  # A | D over C | B tiles [0, n]^2
    check_regions(regions(a, b, a2, b2, d), n - d)  # squeezed by d, inside [0, n - d]^2
    S = n - d
    sy = S - A.H  # A's top at n - d (A.H <= b - d)
    sx = S - B.W  # B's right side at n - d (B.W <= a' - d)
    sq = [(x, y + sy, t) for x, y, t in A.squares]
    sq += block(a - d, S - b, n - a, b)  # D
    sq += block(Fr(0), Fr(0), c, n - b)  # C
    sq += [(x + sx, y, t) for x, y, t in B.squares]
    cert = Cert(len(sq), S, S, sq)
    if strict:
        assert EPS < d / (n - d)  # keeps the scaled side below n
        lam = 1 + EPS
        cert = Cert(cert.n, lam * S, lam * S, [(lam * x, lam * y, t) for x, y, t in sq])
    waste_A, waste_B = a * b - A.n, a2 * b2 - B.n
    assert cert.n == n * n - waste_A - waste_B
    info = dict(n=n, a=a, b=b, a2=a2, b2=b2, c=c, d=d, d_A=d_A, d_B=d_B,
                waste_A=waste_A, waste_B=waste_B, count=cert.n, S=cert.W, B_square=B.is_square)
    return cert, info


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rect", required=True, help="rectangle certificate A (box a x b, a > b)")
    ap.add_argument("--second", required=True, help="certificate B: a square, or a rectangle a' x b' with a' > b'")
    ap.add_argument("--out", required=True)
    ap.add_argument("--closed", action="store_true", help="write side n - d exactly (closed-valid only)")
    ap.add_argument("--d", type=Fr, default=None,
                    help="squeeze to use, a rational such as 1/10000 (default min(d_A, d_B, 1/2))")
    o = ap.parse_args(argv)
    A, B = read_cert(o.rect), read_cert(o.second)
    try:
        cert, info = glue(A, B, strict=not o.closed, d=o.d)
    except GlueError as e:
        print(f"glue: refused: {e}", file=sys.stderr)
        return 2
    n, d = info["n"], info["d"]
    j = info["count"] - (n * n - n)
    side = "n - d" if o.closed else "(1 + 2^-64)(n - d)"
    comment = (f"n={info['count']} = {n}^2 - {n} + {j}, glued {os.path.basename(o.rect)} + "
               f"{os.path.basename(o.second)} + two integer blocks (Lemma 3), side {side}; tools/glue.py")
    with open(o.out, "w") as fh:
        fh.write(cert_text(cert, comment))
    print(f"count = {info['count']} = {n}^2 - {info['waste_A']} - {info['waste_B']} = {n}^2 - {n} + {j}"
          f"  (A box {info['a']} x {info['b']}, B box {info['a2']} x {info['b2']}, c = {info['c']})")
    dsrc = "min(d_A, d_B, 1/2)" if o.d is None else "--d"
    print(f"d = {dsrc} = {float(d):.15f}, side = {float(cert.W):.15f} = {side}")
    print(f"wrote {o.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
