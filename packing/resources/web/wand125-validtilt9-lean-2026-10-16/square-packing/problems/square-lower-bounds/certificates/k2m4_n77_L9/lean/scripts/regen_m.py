#!/usr/bin/env python3
"""Re-certify leaves with the sub-bins chosen for the rows' minima test (`kmmirror.vertOkM`): a bin
is bisected only where that test (or, for few combinations, `vertOkK`) fails, instead of whenever
the combinations exceed 16.  Prints the sub-bin counts before and after.

    regen_m.py CERT.pkl LEAF [LEAF ...]      (V7_REGEN_OUT=DIR: write the root with these leaves replaced)
"""
import os, pickle, sys, time
sys.set_int_max_str_digits(0)
import gen_exact as G
import run_v7 as RV
import kmmirror as KM
from lemmae_mirror import detP, xP, yP, signOk, atV, checkPos, nat_sub
from kmirror import vertOkK
from gen_exact import ev, lowdeg, psmul


def sub_m(self, P, Qp, b0, b1, depth):
    R = self.R
    Dp = detP(P, Qp); X = xP(P, Qp); Y = yP(P, Qp)
    m = lowdeg(Dp) if b0 == 0 else 0
    q = Dp[m:]
    sig = ev(q, (b0 + b1) / 2 / R) > 0
    if signOk(sig, Dp, m, b0, b1, R):
        for k, Sd in enumerate(self.side):
            nm = atV((Sd, 0, 0, 0, 1), Dp, X, Y)[0]
            mm = lowdeg(nm) if b0 == 0 else 0
            q2 = nm[mm:]
            q2 = q2 if (not sig) else psmul(-1, q2)
            if checkPos(q2, nat_sub(len(nm[mm:]), 1), b0, b1, R):
                self.stat['out'] += 1
                return [(b1, sig, m, ('out', k, mm))]
        cert = self.choose(Dp, X, Y, b0, b1)
        args = (self.D, self.W, sig, Dp, X, Y, b0, b1, R, self.chs, self.cvs, self.crs, self.hbx, self.vbx)
        if KM.vertOkM(*args, cert):
            self.stat['val'] += 1
            return [(b1, sig, m, ('val', cert))]
        self.stat['mfail'] = self.stat.get('mfail', 0) + 1
        # `LemmaEKM.vertOkM` falls back, pattern by pattern, to the combinations (`vertOkK`, with the
        # factor certificates); passing `vertOkK` therefore passes it too
        if cert[0]:
            fcs = self.factor_certs(sig, Dp, X, Y, b0, b1, cert)
            if fcs:
                cert[1] = fcs
                if KM.vertOkM(*args, cert):
                    self.stat['val'] += 1; self.stat['fc'] = self.stat.get('fc', 0) + 1
                    return [(b1, sig, m, ('val', cert))]
        nc = 1
        for l, bx in list(zip(cert[2], self.hbx)) + list(zip(cert[3], self.vbx)):
            nc *= sum(len(bx[0]) * len(bx[1]) if x[0][0] == 'box' else
                      (len(x[0][1]) * len(x[0][2]) if x[0][0] == 'alt' else 1) for x in l)
        if (nc <= 16 or depth >= self.maxdepth or b1 - b0 < 2) and vertOkK(*args, cert):
            self.stat['val'] += 1; self.stat['kfb'] = self.stat.get('kfb', 0) + 1
            return [(b1, sig, m, ('val', cert))]
    if depth >= self.maxdepth or b1 - b0 < 2:
        return None
    mid = (b0 + b1) // 2
    a = self.sub(P, Qp, b0, mid, depth + 1)
    if a is None: return None
    b = self.sub(P, Qp, mid, b1, depth + 1)
    if b is None: return None
    self.stat['split'] += 1
    return a + b


def count(certs):
    v = o = 0
    for row in certs:
        for c in row:
            if isinstance(c, list):
                v += sum(1 for sb in c if sb[3][0] == 'val'); o += sum(1 for sb in c if sb[3][0] != 'val')
    return v, o


d = pickle.load(open(sys.argv[1], 'rb'))
RV._cov = RV.sorted_cover()
want = set(sys.argv[2:])
orig_sub = G.Leaf.sub
for b, c in d['leaves'].items():
    if c['name'] not in want or 'capk' in c:
        continue
    v0, o0 = count(c['certs'])
    t0 = time.time()
    G.Leaf.sub = sub_m
    lf, tag, Sl, Rl = RV.certify(b, limit=3600)
    t1 = time.time() - t0
    if lf is None or not hasattr(lf, 'certs'):
        print(c['name'], 'old val/out', v0, o0, 'new FAILED', tag, f'{t1:.0f}s', flush=True)
        continue
    v1, o1 = count(lf.certs)
    print(c['name'], 'old val/out', v0, o0, 'new val/out', v1, o1, 'tag', tag, f'{t1:.0f}s',
          'mfail', lf.stat.get('mfail', 0), 'split', lf.stat.get('split', 0), 'fc', lf.stat.get('fc', 0),
          'kfb', lf.stat.get('kfb', 0), flush=True)
    d['leaves'][b] = dict(name=c['name'], S=Sl, R=Rl, D=lf.D, W=lf.W, W0=lf.W0, cred=lf.cred, Q=lf.Q, box=lf.box,
                          wx=lf.wx, wy=lf.wy, ex=lf.ex, ey=lf.ey, chs=lf.chs, cvs=lf.cvs, crs=lf.crs, Ls=lf.Ls,
                          side=lf.side, hbx=lf.hbx, vbx=lf.vbx, certs=lf.certs)
out = os.environ.get('V7_REGEN_OUT')
if out:
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, f"R{d['idx']:05d}.pkl"), 'wb') as f:
        pickle.dump(d, f)
