"""A209 COPY of A207 clip207 (7db40795; RES -> A207's results, read-only).  A207 -- the BASIN CLIP in F's frame (notes/basin.md, Lemma BASIN (ii)): on a page at s0 whose packing is F = Delta_lam P
for an unknown lam in [1, lam1], a non-pin square whose pose lies in
    B_F(p) := { (c, theta) : |c - lam c_p(m)|_inf <= lam r_c for EVERY lam in [1, lam1],  |tan(theta/2)| <= t_r (mod 90) }
is impossible (for the true lam its P-pose is within (r_c, t_r) of the simple pose of p, which the basin certificate kills).
B_F(p) is a box: per coordinate, c_p(m) = i + 1/2 measured from the corner's wall, so the F-coordinate lam (i + 1/2) sweeps a
segment; the intersection over lam of [lam (u - r_c), lam (u + r_c)] is [lam1 (u - r_c), u + r_c] on an unreflected axis and
[s0 - u - r_c, s0 - lam1 (u - r_c)] on a reflected one.  The clip removes rect x bin  minus  B_F(p) exactly (a tautologous
decomposition into <= 4 rects per tilt part; the tilt bin split at t_r and at t(90 deg - r_t)); nothing outside B_F is touched."""
import json
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import poly204 as P                                            # noqa: E402  (the A204 copy)
import slotmap207 as SM                                        # noqa: E402

MB, QP = P.MB, P.QP
S0 = Fr(969271, 250000)
RES = os.path.abspath(os.path.join(HERE, "..", "..", "A207-basin-clip", "results", "basin207.jsonl"))   # A209: A207's ledger, READ-ONLY
_BINS = {}


def mkbin(a, b):
    k = (a, b)
    if k not in _BINS:
        _BINS[k] = MB.Bin(a, b)
    return _BINS[k]


def basin_box(d, lam, rc):
    """B_F(p)'s centre box (Fractions) for slot-map entry d (corner, i, j), the page's lam1 and the basin radius r_c."""
    u, v = Fr(d["i"]) + Fr(1, 2), Fr(d["j"]) + Fr(1, 2)

    def iv(w, reflected):
        return (S0 - w - rc, S0 - lam * (w - rc)) if reflected else (lam * (w - rc), w + rc)

    x = iv(u, d["corner"] in ("BR", "TR"))
    y = iv(v, d["corner"] in ("TL", "TR"))
    return (x[0], x[1], y[0], y[1])


def load_basins(cls, pad, lam):
    """the certified basins of cls's forced slots valid on the page's window [s0/lam, s0]: per slot every certified (r_c, t_r)
    (a union of boxes), from results/basin207.jsonl; -> [dict(cell, ext, idx, rc, tr, box, cert, window, tag, r_t_deg)]."""
    m_lo = S0 / Fr(lam)
    out = []
    if not os.path.exists(RES):
        return out
    smap = SM.slot_map(cls)
    rows = [json.loads(l) for l in open(RES, encoding="utf-8") if l.strip()]
    for cell, d in smap.items():
        for r in rows:
            if not str(r.get("verdict", "")).startswith("BASIN") or r.get("ext") != d["ext"] or int(r.get("idx", -1)) != d["idx"]:
                continue
            w = r.get("window") or []
            if len(w) != 2 or Fr(w[0]) > m_lo or Fr(w[1]) < S0:
                continue
            rc, tr = Fr(str(r["r_c"])) if "/" in str(r["r_c"]) else Fr(r["r_c"]).limit_denominator(10 ** 6), Fr(r["t_r"])
            if any(b["cell"] == cell and b["rc"] >= rc and b["tr"] >= tr for b in out):
                continue
            out = [b for b in out if not (b["cell"] == cell and b["rc"] <= rc and b["tr"] <= tr)]
            out.append(dict(cell=cell, ext=d["ext"], idx=d["idx"], rc=rc, tr=tr, r_t_deg=r.get("r_t_deg"), box=basin_box(d, Fr(lam), rc), cert=r.get("certificate"),
                            window=w, tag=r.get("tag"), lam=float(lam)))
    return out


def tilt_parts(t0, t1, tr):
    """[(a, b, inside)]: the sub-bins of [t0, t1] inside the tilt basin [0, t_r] u [t(90 - r_t), 1] and the part outside."""
    if tr <= 0:
        return [(t0, t1, False)]
    trp = (1 - tr) / (1 + tr)
    parts = []
    if t0 < tr:
        parts.append((t0, min(t1, tr), True))
    if t1 > trp:
        parts.append((max(t0, trp), t1, True))
    lo, hi = max(t0, tr), min(t1, trp)
    if lo < hi:
        parts.append((lo, hi, False))
    return parts


def rect_minus(r, b):
    """rects covering r minus the closed box b (a superset of r \\ b; every dropped point lies in b)."""
    x0, x1, y0, y1 = r
    bx0, bx1, by0, by1 = b
    if x1 <= bx0 or x0 >= bx1 or y1 <= by0 or y0 >= by1:
        return [r]
    out = []
    if bx0 > x0:
        out.append((x0, bx0, y0, y1))
    if bx1 < x1:
        out.append((bx1, x1, y0, y1))
    mx0, mx1 = max(x0, bx0), min(x1, bx1)
    if by0 > y0:
        out.append((mx0, mx1, y0, by0))
    if by1 < y1:
        out.append((mx0, mx1, by1, y1))
    return out


def clip_pieces(pcs, basins):
    """the pieces minus every basin box x tilt basin; -> (pieces, [(cell, volume removed)])."""
    cur = list(pcs)
    rep = []
    for b in basins:
        box, tr = b["box"], b["tr"]
        v0 = P.vol(cur)
        nxt = []
        for bn, r in cur:
            x0, x1, y0, y1 = r
            if x1 <= box[0] or x0 >= box[1] or y1 <= box[2] or y0 >= box[3]:
                nxt.append((bn, r))
                continue
            for (a, c, inside) in tilt_parts(bn.t0, bn.t1, tr):
                b2 = bn if (a == bn.t0 and c == bn.t1) else mkbin(a, c)
                if not inside:
                    nxt.append((b2, r))
                    continue
                for r2 in rect_minus(r, box):
                    nxt.append((b2, r2))
        cur = nxt
        v1 = P.vol(cur)
        if v1 < v0:
            rep.append((b["cell"], float((v0 - v1) / v0) if v0 else 0.0))
    return cur, rep


def basin_json(b):
    return dict(cell=b["cell"], ext=b["ext"], idx=b["idx"], r_c=float(b["rc"]), t_r=str(b["tr"]), r_t_deg=b.get("r_t_deg"), box=[float(v) for v in b["box"]],
                cert=b.get("cert"), window=b.get("window"), tag=b.get("tag"), lam=b.get("lam"))


if __name__ == "__main__":
    cls, pad = (sys.argv[1] if len(sys.argv) > 1 else "k5_16"), (sys.argv[2] if len(sys.argv) > 2 else "g1")
    for b in load_basins(cls, pad, QP.PADS[pad]):
        print(json.dumps(basin_json(b)))
