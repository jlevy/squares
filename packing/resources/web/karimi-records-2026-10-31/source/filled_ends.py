#!/usr/bin/env python3
"""Exact generator for the filled-end two-band L packing with independent bands.

Construction
  - L-shaped frame of Sungjoon Ryu (doi:10.5281/zenodo.23278927, Theorem 1.3).
  - Band ends filled with axis-parallel layers: idea of Evan Daniel
    (evand/square-packing, certificates/k2-minus-c/, 18 Oct 2026); the band and
    fill are written as in Kevin Fang's note (doi:10.5281/zenodo.23624565,
    Sections 2-3).
  - Independent width b, tilt t and lift split for each band, and the per-n
    search: Mohsen Karimi.

Geometry (all arithmetic exact, fractions.Fraction)
  band(b, t, L, y0): band coordinates X in [0, W] across, Y in [0, L] along,
  c = cos, s = sin of the tilt theta with tan(theta/2) = t,
  W = b c + s, h = b s + c, sec = 1/c.
  Row j (0 <= j < R) is the 1 x b rectangle {0<=u<=b, 0<=v<=1} in the frame
  u ~ (c, s), v ~ (-s, c), with corner u = v = 0 at (s, y0 + j sec).
  R = floor((L - h)/sec) + 1, free length F = L - (R-1) sec - h, y1 = F - y0.
  Near-end fill with lift y: level i holds m_i = floor(W - a_i) axis squares
  [W - m_i + q, W - m_i + q + 1] x [i, i + 1], a_i = max(0, s + (i+1-y) c/s).
  Far-end fill: the near-end fill for lift y1 turned by 180 degrees about
  (W/2, L/2).

Container [0, S]^2, S = K - bV + WV:
  grid  (K - bV) x (K - bH) axis squares in [0, K-bV] x [0, K-bH];
  V band: x = K - bV + X, y = Y, length S, tilt +tV;
  H band: x = Y, y = K - bH + X, length K - bV, tilt -tH (reflection in y = x);
  needs K - bH + WH <= S.

Output: same certificate format as regenerate.py: '# comment', 'n S', then
one line 'x y t' per square (centre, tan of half the rotation angle).
"""
import math, sys
from fractions import Fraction as F


def trig(t):
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def band_dims(b, t):
    c, s = trig(t)
    return c, s, b * c + s, b * s + c, 1 / c   # c, s, W, h, sec


def rows_and_free(b, t, L):
    c, s, W, h, sec = band_dims(b, t)
    if L <= h:
        return None
    R = math.floor((L - h) / sec) + 1
    Fr = L - (R - 1) * sec - h
    return R, Fr


def fill_levels(b, t, y):
    """list of (level i, m_i) for the near-end fill with lift y"""
    c, s, W, h, sec = band_dims(b, t)
    tau = c / s
    out = []
    i = 0
    while True:
        a = max(F(0), s + (i + 1 - y) * tau)
        m = math.floor(W - a)
        if m <= 0 and a > 0:
            break
        if m > 0:
            out.append((i, m))
        i += 1
        if i > 10000:
            raise RuntimeError('fill did not stop')
    return out


def band_count(b, t, L, y0):
    rf = rows_and_free(b, t, L)
    if rf is None:
        return None
    R, Fr = rf
    if not (0 <= y0 <= Fr):
        return None
    y1 = Fr - y0
    return b * R + sum(m for _, m in fill_levels(b, t, y0)) \
                 + sum(m for _, m in fill_levels(b, t, y1))


def band_squares(b, t, L, y0):
    """squares of one band in band coordinates: list of (X, Y, tilt)"""
    c, s, W, h, sec = band_dims(b, t)
    R, Fr = rows_and_free(b, t, L)
    assert 0 <= y0 <= Fr
    y1 = Fr - y0
    half = F(1, 2)
    sq = []
    for j in range(R):
        for i in range(b):
            X = s + (i + half) * c - half * s
            Y = y0 + j * sec + (i + half) * s + half * c
            sq.append((X, Y, t))
    for i, m in fill_levels(b, t, y0):
        for q in range(m):
            sq.append((W - m + q + half, i + half, F(0)))
    for i, m in fill_levels(b, t, y1):
        for q in range(m):
            X, Y = W - m + q + half, i + half
            sq.append((W - X, L - Y, F(0)))      # 180 degree turn
    return sq


def build(K, bV, tV, yV, bH, tH, yH, n=None):
    cV, sV, WV, hV, secV = band_dims(bV, tV)
    cH, sH, WH, hH, secH = band_dims(bH, tH)
    S = K - bV + WV
    assert S < K, 'container side must be below K'
    assert K - bH + WH <= S, 'H band does not fit'
    half = F(1, 2)
    sq = []
    for X, Y, t in band_squares(bV, tV, S, yV):          # V band
        sq.append((K - bV + X, Y, t))
    for X, Y, t in band_squares(bH, tH, F(K - bV), yH):  # H band, reflected
        sq.append((Y, K - bH + X, -t))
    grid = [(i + half, j + half, F(0)) for i in range(K - bV) for j in range(K - bH)]
    sq = grid + sq          # grid first, so surplus squares come from the grid
    if n is not None:
        assert len(sq) >= n, f'construction holds only {len(sq)} squares'
        sq = sq[len(sq) - n:]
    return S, sq


def total_count(K, bV, tV, yV, bH, tH, yH):
    cV, sV, WV, hV, secV = band_dims(bV, tV)
    cH, sH, WH, hH, secH = band_dims(bH, tH)
    S = K - bV + WV
    if S >= K or K - bH + WH > S:
        return None
    a = band_count(bV, tV, S, yV)
    b_ = band_count(bH, tH, F(K - bV), yH)
    if a is None or b_ is None:
        return None
    return (K - bV) * (K - bH) + a + b_


def best_split(b, t, L, nsplit=20):
    """best lift y0 among nsplit+1 equally spaced values in [0, F]"""
    rf = rows_and_free(b, t, L)
    if rf is None:
        return None, None
    R, Fr = rf
    best = (-1, None)
    for q in range(nsplit + 1):
        y0 = Fr * q / nsplit
        cnt = band_count(b, t, L, y0)
        if cnt > best[0]:
            best = (cnt, y0)
    return best


def write_cert(path, K, n, S, sq, comment):
    def fr(q):
        q = F(q)
        return f'{q.numerator}/{q.denominator}'
    with open(path, 'w') as f:
        f.write(f'# N={n}, {comment}\n')
        f.write(f'{n} {fr(S)}\n')
        for x, y, t in sq:
            f.write(f'{fr(x)} {fr(y)} {fr(t)}\n')
