"""Diagnostic: which pairs a closing move of the least-gap pair also closes.

Decides nothing; prints, for each count and each choice of the moving square, the pairs
the integer route finds overlapping after moving it by gap + 1e-30 along the best axis.
Usage: python -I diag_pair_t225.py CERT_DIR N [N ...]
"""
import gzip
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import review_t225_check as mine  # noqa: E402

EPS = Fraction(1, 10**30)


def main(argv):
    folder = Path(argv[1])
    for n in map(int, argv[2:]):
        text = gzip.decompress((folder / f"n-{n:03d}.cert.gz").read_bytes()).decode("ascii")
        side, rows = mine.read_certificate(text, n)
        base = mine.route_integers(side, rows)
        i, j = base["least_gap"][2], base["least_gap"][3]
        sq = []
        for x, y, t in rows:
            x, y, t = Fraction(*x), Fraction(*y), Fraction(*t)
            sq.append((x, y, (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)))
        x, y, c, s = sq[i]
        X, Y, C, T = sq[j]
        best = None
        for u, v in ((c, s), (-s, c), (C, T), (-T, C)):
            hp = (abs(u * c + v * s) + abs(-u * s + v * c)) / 2
            hq = (abs(u * C + v * T) + abs(-u * T + v * C)) / 2
            proj = u * (X - x) + v * (Y - y)
            g = abs(proj) - hp - hq
            if best is None or g > best[0]:
                best = (g, u, v, proj)
        g, u, v, proj = best
        print(n, "pair", (i, j), "gap", float(g), "axis", (float(u), float(v)), "t_i", float(Fraction(*rows[i][2])), "t_j", float(Fraction(*rows[j][2])))
        for mover in (j, i):
            sign = (-1 if proj > 0 else 1) if mover == j else (1 if proj > 0 else -1)
            moved = list(rows)
            mx = Fraction(*rows[mover][0]) + sign * (g + EPS) * u
            my = Fraction(*rows[mover][1]) + sign * (g + EPS) * v
            moved[mover] = ((mx.numerator, mx.denominator), (my.numerator, my.denominator), rows[mover][2])
            r = mine.route_integers(side, moved)
            gaps = []
            for a, b in r["overlapping_pairs"]:
                one = mine.route_integers(side, [moved[a], moved[b]])
                gaps.append(((a, b), f"{float(Fraction(one['least_gap'][0], one['least_gap'][1])):.3e}"))
            print("   mover", mover, "overlaps", gaps, "walls_ok", r["walls_ok"])


if __name__ == "__main__":
    main(sys.argv)
