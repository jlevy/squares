#!/usr/bin/env python3
"""The construction of Theorem A (note in note/main.pdf), in exact rational arithmetic.

Standalone, stdlib only (Python 3.8+). Same arithmetic as squarepack/lband.py (proof_layout) in
the working repo; its certificates are byte-identical (regenerate.sh checks the hashes).

    python3 lband.py K [--out FILE]      # print the layout; write the strict certificate
    python3 lband.py --bound KMIN KMAX   # check k^2 - n < 4 sqrt(2k) + 2 exactly, without building

Layout: a (k - b)^2 aligned grid, a band of b tilted rows of length S in [k - b, S] x [0, S], and
the same band of length k - b reflected in y = x, in [0, k - b] x [k - b, S], with S = k - b + W.
b is the odd integer nearest sqrt(2k), tan(theta/2) = Q/(bQ - 1) just above 1/b, each band has the
most rows, lift 0 at one end and its free length at the other, and both ends are filled with
axis-parallel rows. The squeeze k - S starts at 1/(10^6 k^3) and is divided by 10 until conditions
(a)-(d) of the note and H(t) < 4 sqrt(2k) + 2 hold, decided exactly; Lemma 2 then gives the bound
for the layout returned. The certificate is the closed packing scaled once about the origin by
1 + (k - S)/(2S), so every margin is positive and the side is (S + k)/2 < k.
"""
import math
import sys
from fractions import Fraction as Fr

HALF = Fr(1, 2)


def floor(v):
    return v.numerator // v.denominator


class Band:
    def __init__(self, b, t):
        self.b, self.t = b, t
        d = 1 + t * t
        self.c, self.s = (1 - t * t) / d, 2 * t / d
        self.W = b * self.c + self.s
        self.sec = 1 / self.c
        self.tan = self.s / self.c
        self.h = b * self.s + self.c

    def rows_max(self, L):
        free = L - self.h
        return floor(free / self.sec) + 1 if free >= 0 else 0

    def fill(self, y):
        """Axis-parallel row lengths under the first row at lift y (row i has Y in [i, i + 1])."""
        out, i = [], 0
        while True:
            a = max(Fr(0), self.s + (i + 1 - y) / self.tan)
            m = floor(self.W - a)
            if m < 1:
                return out
            out.append(m)
            i += 1


def band_t(b, squeeze):
    if squeeze > Fr(2, 1 + (b - 1) ** 2):
        return None
    Q = max(1, math.ceil(2 / (b * b * squeeze)))
    while True:
        t = Fr(Q, b * Q - 1)
        if b - Band(b, t).W >= squeeze:
            return t
        Q = max(1, Q // 2)


def proof_b(k):
    r = math.isqrt(2 * k)
    cands = [b for b in (r - 1, r, r + 1, r + 2) if b % 2 == 1 and b >= 3]
    return min(cands, key=lambda b: abs(b * b - 2 * k) / (b + math.sqrt(2 * k)))


def proof_band(band, L):
    R = band.rows_max(L)
    free = L - (R - 1) * band.sec - band.h
    return (R, Fr(0), free, band.fill(Fr(0)), band.fill(free))


def band_bound(band, L):
    """Right side of (2) in the note."""
    b, c, s, W = band.b, band.c, band.s, band.W
    tau = c / s
    return b * L * (1 - c) + b * c * band.h - 2 * b + 2 - 2 * (W - s - 2 * tau) + 2 * (Fr(b, 2) - tau)


def admissible(k, band, S):
    b, c, s, W = band.b, band.c, band.s, band.W
    tau = c / s
    eta = Fr(b, 2) - tau
    if b % 2 == 0 or not (floor(W - s - tau) == (b - 1) // 2 and 0 <= eta < HALF
                          and 2 * tau - b * c >= 0 and band.h < 3):
        return False
    H = b * (k - S) + band_bound(band, S) + band_bound(band, Fr(k - b))
    return H < 2 or (H - 2) ** 2 < 32 * k


def proof_layout(k):
    b = proof_b(k)
    squeeze = Fr(1, 10**6 * k**3)
    for _ in range(40):
        t = band_t(b, squeeze)
        if t is not None:
            band = Band(b, t)
            S = k - b + band.W
            if admissible(k, band, S):
                return b, band, S, proof_band(band, S), proof_band(band, Fr(k - b))
        squeeze /= 10
    raise AssertionError(f"no admissible squeeze for k = {k}")


def count(k, b, right, top):
    return (k - b) ** 2 + sum(b * p[0] + sum(p[3]) + sum(p[4]) for p in (right, top))


def band_squares(band, L, p):
    R, y0, _, bottom, top = p
    c, s, W, sec = band.c, band.s, band.W, band.sec
    out = []
    for j in range(R):
        ox, oy = s, y0 + j * sec
        for i in range(band.b):
            out.append((ox + (i + HALF) * c - HALF * s, oy + (i + HALF) * s + HALF * c, band.t))
    for i, m in enumerate(bottom):
        for q in range(m):
            out.append((W - m + q + HALF, i + HALF, Fr(0)))
    for i, m in enumerate(top):
        for q in range(m):
            out.append((W - (W - m + q + HALF), L - (i + HALF), Fr(0)))
    return out


def describe(k, b, band, S, right, top, n):
    f = lambda p: f"R={p[0]} ends {list(p[3])}/{list(p[4])} y0={float(p[1]):.4f} y1={float(p[2]):.4f}"
    return (f"k={k} b={b} n={n} waste={k**2 - n} squeeze={float(k - S):.1e} t={band.t} right: {f(right)}; "
            f"top: {f(top)}")


def certificate(k):
    b, band, S, right, top = proof_layout(k)
    sq = [(i + HALF, j + HALF, Fr(0)) for j in range(k - b) for i in range(k - b)]
    sq += [(k - b + X, Y, t) for X, Y, t in band_squares(band, S, right)]
    sq += [(Y, k - b + X, -t) for X, Y, t in band_squares(band, Fr(k - b), top)]
    n = count(k, b, right, top)
    assert len(sq) == n
    lam = 1 + (k - S) / (2 * S)
    lines = [f"# {describe(k, b, band, S, right, top, n)} (Theorem A)", f"{n} {lam * S}"]
    lines += [f"{lam * x} {lam * y} {t}" for x, y, t in sq]
    return "\n".join(lines) + "\n"


def main(argv):
    if argv[:1] == ["--bound"]:
        lo, hi = int(argv[1]), int(argv[2])
        worst = None
        for k in range(lo, hi + 1):
            b, band, S, right, top = proof_layout(k)
            w = k * k - count(k, b, right, top)
            assert w < 2 or (w - 2) ** 2 < 32 * k, k
            r = w - 4 * math.sqrt(2 * k)
            worst = max(worst or (r, k), (r, k))
        print(f"k = {lo}..{hi}: k^2 - n < 4 sqrt(2k) + 2 at every k; largest k^2 - n - 4 sqrt(2k) = {worst[0]:.4f} at k = {worst[1]}")
        return 0
    k = int(argv[0])
    text = certificate(k)
    print(text.splitlines()[0][2:])
    if "--out" in argv:
        open(argv[argv.index("--out") + 1], "w").write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
