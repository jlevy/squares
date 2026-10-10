#!/usr/bin/env python3
"""Exact verifier: n closed unit squares with pairwise disjoint interiors inside [0, S]^2 => s(n) <= S.

Standalone, stdlib only (Python 3.8+). Same code and verdicts as squarepack/verify.py in the
working repo, merged into one file with its geometry and certificate readers.

    python3 verify.py n0343/n0343.cert --strict          # evand text
    python3 verify.py n0343/n0343.cert.json --strict     # SQUISH json
    exit status 0 iff valid

Certificate: rational centre (x, y) and rational t = tan(theta/2) per square, so that
cos = (1 - t^2)/(1 + t^2) and sin = 2t/(1 + t^2) are rational and cos^2 + sin^2 = 1 exactly.
All arithmetic is Fraction, so a verdict carries no tolerance. Two conventions:

  * closed (default): squares lie in the closed box [0, S]^2 and have pairwise disjoint
    interiors; touching (margin exactly 0) is allowed. This is the definition of s(n) <= S.
  * strict (--strict): every wall and pair margin must be > 0, as in Evan Daniel's
    verify_cert.py. A strict pass implies a closed pass.

Pairs whose circumscribed discs are disjoint (|dc|^2 > 2) are separated without further work;
every other pair is checked by the separating-axis theorem over the four face normals.

Formats:
  * evand text : line 1 `n S`, then n lines `x y t`; `#` comments; every number a rational
                 such as 3/7 or an integer.
  * SQUISH json: {"n", "s_exact", "squares": [[x, y, t], ...]} with strings for rationals.
"""
import json
import sys
from fractions import Fraction as Fr

HALF = Fr(1, 2)


# ---- geometry --------------------------------------------------------------------------------
class Square:
    __slots__ = ("x", "y", "t", "c", "s")

    def __init__(self, x, y, t):
        self.x, self.y, self.t = x, y, t
        d = 1 + t * t
        self.c, self.s = (1 - t * t) / d, 2 * t / d

    def half_extent(self, nx, ny):
        """Half-width of the square's projection onto the (not necessarily unit) axis (nx, ny)."""
        c, s = self.c, self.s
        return HALF * (abs(nx * c + ny * s) + abs(-nx * s + ny * c))

    def axes(self):
        return (self.c, self.s), (-self.s, self.c)


def wall_margin(sq, S):
    """Smallest signed clearance of sq from the walls of [0, S]^2 (positive = strictly inside)."""
    e = sq.half_extent(Fr(1), Fr(0))  # = (|c| + |s|)/2, same for both axes
    return min(sq.x - e, S - sq.x - e, sq.y - e, S - sq.y - e)


def pair_margin(a, b):
    """Best separating-axis gap between a and b (positive = interiors disjoint with room to spare).
    None when the circumscribed discs are already disjoint (|dc|^2 > 2)."""
    dx, dy = b.x - a.x, b.y - a.y
    if dx * dx + dy * dy > 2:
        return None
    best = None
    for nx, ny in (*a.axes(), *b.axes()):
        g = abs(nx * dx + ny * dy) - a.half_extent(nx, ny) - b.half_extent(nx, ny)
        if best is None or g > best:
            best = g
    return best


# ---- certificate readers -----------------------------------------------------------------------
def read_text(text):
    rows = [l.split() for l in text.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    n, S = int(rows[0][0]), Fr(rows[0][1])
    sq = [Square(Fr(r[0]), Fr(r[1]), Fr(r[2])) for r in rows[1 : n + 1]]
    if len(sq) != n:
        raise ValueError(f"expected {n} squares, got {len(sq)}")
    return n, S, sq


def read_squish_json(text):
    d = json.loads(text)
    sq = [Square(Fr(x), Fr(y), Fr(t)) for x, y, t in d["squares"]]
    return int(d["n"]), Fr(d["s_exact"]), sq


def load(path):
    with open(path) as fh:
        text = fh.read()
    return read_squish_json(text) if path.endswith(".json") else read_text(text)


def leading_digits(v, sig=20):
    """The leading `sig` significant digits of v (v > 0), exact (truncated, not rounded; not float)."""
    if v <= 0:
        return str(float(v))
    ip = v.numerator // v.denominator
    places = max(sig - len(str(ip)), 0) if ip else sig
    q = v.numerator * 10**places // v.denominator
    s = str(q).rjust(places + 1, "0")
    return f"{s[:-places]}.{s[-places:]}" if places else s


# ---- verifier ----------------------------------------------------------------------------------
def verify(n, S, sq, strict=False):
    for q in sq:
        assert q.c * q.c + q.s * q.s == 1
    wall = min((wall_margin(q, S), i) for i, q in enumerate(sq))
    best_pair = None
    nsat = 0
    for i in range(n):
        for j in range(i + 1, n):
            g = pair_margin(sq[i], sq[j])
            if g is None:
                continue
            nsat += 1
            if best_pair is None or g < best_pair[0]:
                best_pair = (g, i, j)
    if strict:
        ok = wall[0] > 0 and (best_pair is None or best_pair[0] > 0)
    else:
        ok = wall[0] >= 0 and (best_pair is None or best_pair[0] >= 0)
    lines = [f"n = {n}, S = {S} (= {leading_digits(S)}...)"]
    lines.append(f"  min wall clearance  = {float(wall[0]):.3e}  (square #{wall[1]})")
    if best_pair is not None:
        g, i, j = best_pair
        lines.append(
            f"  min pair separation = {float(g):.3e}  (squares #{i}, #{j}; "
            f"{nsat} close pairs by separating axes, the rest by disc separation)"
        )
    mode = "strict" if strict else "closed"
    lines.append(f"  VALID ({mode}): s(n) <= S" if ok else f"  INVALID ({mode})")
    return ok, "\n".join(lines)


def main(argv):
    strict = "--strict" in argv
    argv = [a for a in argv if a != "--strict"]
    if len(argv) != 1:
        print(__doc__)
        return 2
    ok, report = verify(*load(argv[0]), strict=strict)
    print(report)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
