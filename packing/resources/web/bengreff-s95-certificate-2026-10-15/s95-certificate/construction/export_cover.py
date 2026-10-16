"""Write an exact "mixed 1" cover for [0,K]^2 (K from env SQK) from a cross-LP solution.

fixed part: the band-inserted s(59) cover outside the cross (exact integers, weight unit 4e8)
free part : LP weights on the cross candidates, scaled by the safety factor f and rounded up
            on the same weight unit (rounding up only adds mass, so captures only grow)

usage: python export_cover.py cross_p0.100.npz F out.txt [--lineseg]

--lineseg: free points lying on an integer line (x or y in {0..9}) become segments of length 2/D
           on that line (half to each line at a crossing), as in wand125's s(77) construction
"""
import sys, os
import numpy as np
from cover import load_mixed, insert_band

z = np.load(sys.argv[1]); f = float(sys.argv[2]); out = sys.argv[3]
K = int(os.environ.get("SQK", "9")); N = K * K - 5
lo, hi = 2.5, K - 2.5
D = 8000                                    # coordinate unit 1/8000: fits 1/16 segments and the 1/20 lattice
c = load_mixed("n59_mixed_cover_8.txt"); b = insert_band(c, 4, K - 8)
assert b["D"] == 1000
W = b["W"]                                  # 4e8
P = b["ptsf"].copy(); Sg = b["segsf"].copy()   # base in units 1/1000 -> rescale to 1/D
P[:, :2] *= D // 1000; Sg[:, :4] *= D // 1000

def in_cross(x, y): return ((x >= lo * D) & (x <= hi * D)) | ((y >= lo * D) & (y <= hi * D))
pc = in_cross(P[:, 0], P[:, 1])
mid = (Sg[:, :2] + Sg[:, 2:4]) / 2; sc = in_cross(mid[:, 0], mid[:, 1])
fixed_p = P[~pc]; fixed_s = Sg[~sc]
assert np.all(fixed_p == np.round(fixed_p)) and np.all(fixed_s == np.round(fixed_s)), "fixed part not integral"

x = z["x"]; cp = z["cand_p"]; cs = z["cand_s"]
wp = x[z["p_orb"]] * f; ws = x[z["s_orb"]] * f
keep_p = wp > 0; keep_s = ws > 0
Xp = np.round(cp[keep_p] * D); Xs = np.round(cs[keep_s] * D)
assert np.allclose(Xp, cp[keep_p] * D, atol=1e-6) and np.allclose(Xs, cs[keep_s] * D, atol=1e-6), "candidate off the 1/D grid"
Wp = np.ceil(wp[keep_p] * W - 1e-9); Ws = np.ceil(ws[keep_s] * W - 1e-9)
if "--lineseg" in sys.argv:
    S9 = K * D
    onx = (Xp[:, 0] % D == 0); ony = (Xp[:, 1] % D == 0)
    newseg = []
    def seg_on(vertical, X, Y, w):
        if vertical:
            h = D // 1000; y0 = min(max(Y - h, 0), S9 - 2 * h); return (X, y0, X, y0 + 2 * h, w)
        h = D // 1000; x0 = min(max(X - h, 0), S9 - 2 * h); return (x0, Y, x0 + 2 * h, Y, w)
    for (X, Y), w, a, b in zip(Xp, Wp, onx, ony):
        if a and b:
            h = np.ceil(w / 2); newseg += [seg_on(True, X, Y, h), seg_on(False, X, Y, h)]
        elif a:
            newseg.append(seg_on(True, X, Y, w))
        elif b:
            newseg.append(seg_on(False, X, Y, w))
    off = ~(onx | ony)
    print("lineseg: %d points on lines -> %d short segments (mass %.4f)" % ((~off).sum(), len(newseg), Wp[~off].sum() / W))
    Xp, Wp = Xp[off], Wp[off]
    if newseg:
        ns = np.array(newseg, dtype=np.float64)
        Xs = np.concatenate([Xs, ns[:, :4]]); Ws = np.concatenate([Ws, ns[:, 4]])

pts = np.concatenate([fixed_p, np.column_stack([Xp, Wp])]).astype(np.int64)
segs = np.concatenate([fixed_s, np.column_stack([Xs, Ws])]).astype(np.int64)
total = (pts[:, 2].sum() + segs[:, 4].sum()) / W
with open(out, "w") as fh:
    fh.write("mixed 1\n# s(%d) candidate: band-inserted s(59) corners + cross LP, free part x %.6f\n" % (N, f))
    fh.write("%d 1\n%d\n%d\n%d\n" % (K, D, W, len(pts)))
    for r in pts: fh.write("%d %d %d\n" % tuple(r))
    fh.write("%d\n" % len(segs))
    for r in segs: fh.write("%d %d %d %d %d\n" % tuple(r))
    fh.write("0\n")
print("wrote %s: %d points, %d segments, total %.9f (%s %d)" % (out, len(pts), len(segs), total, "<" if total < N else ">=", N))
