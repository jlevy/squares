"""Unit-square capture on an NVIDIA GPU with CuPy. float32 for screening (default); dtype=float64 for the
dense scans of zmx2-failing roots. Same API as gpu.py."""
import numpy as np
import cupy as cp


class GPUMeasure:
    def __init__(self, pxy, pw, sxy, sw, dtype=cp.float32):
        f = self.f = dtype
        self.p = cp.asarray(pxy, dtype=f); self.pw = cp.asarray(pw, dtype=f)
        self.s = cp.asarray(sxy, dtype=f); self.sw = cp.asarray(sw, dtype=f)

    def capture(self, poses, tol=2e-6, chunk=512):
        h = self.f(0.5 + tol)
        out = []
        P = np.asarray(poses, dtype=self.f)
        for i in range(0, len(P), chunk):
            q = cp.asarray(P[i:i + chunk])
            cx, cy, th = q[:, 0:1], q[:, 1:2], q[:, 2:3]
            co, si = cp.cos(th), cp.sin(th)
            dx = self.p[None, :, 0] - cx; dy = self.p[None, :, 1] - cy
            u = co * dx + si * dy; v = -si * dx + co * dy
            ins = ((cp.abs(u) <= h) & (cp.abs(v) <= h)).astype(self.f)
            cap = ins @ self.pw
            del dx, dy, u, v, ins
            if self.sw.size:
                ax = self.s[None, :, 0] - cx; ay = self.s[None, :, 1] - cy
                bx = self.s[None, :, 2] - cx; by = self.s[None, :, 3] - cy
                lo = cp.zeros(ax.shape, self.f); hi = cp.ones(ax.shape, self.f)
                for a0, b0 in ((co * ax + si * ay, co * bx + si * by),
                               (-si * ax + co * ay, -si * bx + co * by)):
                    d = b0 - a0
                    nz = cp.abs(d) > 1e-12
                    dd = cp.where(nz, d, self.f(1))
                    t1 = (-h - a0) / dd; t2 = (h - a0) / dd
                    in0 = cp.abs(a0) <= h
                    big = self.f(1e9)
                    tl = cp.where(nz, cp.minimum(t1, t2), cp.where(in0, -big, big))
                    tr = cp.where(nz, cp.maximum(t1, t2), cp.where(in0, big, -big))
                    lo = cp.maximum(lo, tl); hi = cp.minimum(hi, tr)
                cap = cap + cp.maximum(hi - lo, 0) @ self.sw
            out.append(cp.asnumpy(cap).astype(np.float64))
        return np.concatenate(out)
