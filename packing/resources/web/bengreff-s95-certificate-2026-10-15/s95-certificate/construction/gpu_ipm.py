"""Primal-dual interior-point LP solver on the GPU (CuPy), for LPs with few columns and many rows.

    min c.x   s.t.   A x >= b,   0 <= x <= u   (u may be +inf)

Mehrotra predictor-corrector on the normal equations. With n columns the system matrix
M = A^T (Y/S) A + X^-1 Z + (U-X)^-1 W is n x n. It is formed by a float32 GEMM over dense row
chunks of A kept on the GPU, then factored in float64; each Newton system is solved by
preconditioned CG with that factor and exact float64 sparse products, so the float32 rounding
in M only affects the preconditioner, not the direction.
(cuSPARSE SpGEMM overflows 32-bit counters on this product, so sparse A^T D A is not used.)
Returns (status, x) with status "optimal" or a short failure string; x is clipped to [0, u].
"""
import time
import numpy as np
import cupy as cp
import cupyx.scipy.sparse as csp


def solve(A, b, c, u, tol=1e-8, max_iter=200, verbose=False, row_chunk=60000, ptol=1e-7):
    """Columns with u <= 0 are fixed at zero and removed before the solve."""
    u = np.asarray(u, dtype=np.float64); keep = u > 0
    st, xk = _solve(A.tocsc()[:, keep], b, np.asarray(c)[keep], u[keep], tol, max_iter, verbose, row_chunk, ptol)
    x = np.zeros(len(u)); x[keep] = xk
    return st, x


def _solve(A, b, c, u, tol, max_iter, verbose, row_chunk, ptol):
    T0 = time.time()
    m, n = A.shape
    A = A.tocsr().astype(np.float64)
    # row chunks keep the A^T D A product within GPU memory
    # only the float64 CSR blocks live on the GPU; dense float32 row blocks for the GEMM are built on the fly
    chunks = []
    for i in range(0, m, row_chunk):
        chunks.append(csp.csr_matrix(A[i:i + row_chunk]))
    b_ = cp.asarray(b, dtype=cp.float64); c_ = cp.asarray(c, dtype=cp.float64)
    u_h = np.asarray(u, dtype=np.float64)
    fixed0 = u_h <= 0                       # columns forced to zero
    hasu = np.isfinite(u_h) & ~fixed0
    u_ = cp.asarray(np.where(hasu, u_h, 1.0)); hu = cp.asarray(hasu); free = cp.asarray(~fixed0)

    def Ax(v):
        return cp.concatenate([Ai @ v for Ai in chunks])

    def ATy(w):
        out = cp.zeros(n); o = 0
        for Ai in chunks:
            k = Ai.shape[0]; out += Ai.T @ w[o:o + k]; o += k
        return out

    def ATDA(d):
        M = cp.zeros((n, n), dtype=cp.float32)
        d32 = d.astype(cp.float32); o = 0
        for Ai in chunks:
            for j in range(0, Ai.shape[0], 8192):
                B = Ai[j:j + 8192].toarray().astype(cp.float32); k = B.shape[0]
                M += (B * d32[o:o + k, None]).T @ B
                o += k; del B
        return M

    # starting point: x in the box interior, slacks and duals positive
    x = cp.where(hu, u_ / 2, 0.01) * free
    s = cp.maximum(Ax(x) - b_, 1.0)
    y = cp.ones(m); z = cp.ones(n) * free; w = cp.where(hu, 1.0, 0.0) * free
    nb = 1 + float(cp.linalg.norm(b_)); nc = 1 + float(cp.linalg.norm(c_))
    hist = []
    for it in range(max_iter):
        xu = cp.where(hu, u_ - x, 1.0)
        rp = Ax(x) - s - b_                                   # primal residual (A x - s = b)
        rd = c_ - ATy(y) - z + w                              # dual residual (A^T y + z - w = c)
        rd = rd * free
        mu = (float(s @ y) + float(x @ z) + float((xu * w)[hu].sum())) / (m + int(free.sum()) + int(hu.sum()))
        pobj = float(c_ @ x); dobj = float(b_ @ y) - float((u_ * w)[hu].sum())
        relgap = abs(pobj - dobj) / (1 + abs(pobj))
        epri = float(cp.linalg.norm(rp)) / nb; edua = float(cp.linalg.norm(rd)) / nc
        if verbose:
            print("[%5.1fs] " % (time.time() - T0), end="")
            print("it %3d  pobj %.10f  dobj %.10f  gap %.2e  pri %.2e  dua %.2e  mu %.2e" % (it, pobj, dobj, relgap, epri, edua, mu), flush=True)
        hist.append(pobj)
        if relgap < tol and epri < tol and edua < tol:
            return "optimal", cp.asnumpy(cp.clip(x, 0, cp.where(hu, u_, cp.inf)) * free)
        if epri < 1e-10 and len(hist) > 6 and abs(hist[-6] - pobj) <= ptol * (1 + abs(pobj)) and relgap < 1e-4:
            return "optimal (primal stagnant)", cp.asnumpy(cp.clip(x, 0, cp.where(hu, u_, cp.inf)) * free)
        # normal matrix: A^T (Y/S) A + Z/X + W/(U-X)
        d = y / s
        theta = cp.where(free, z / cp.maximum(x, 1e-300) + cp.where(hu, w / xu, 0.0), 1.0)
        M = ATDA(d); M[cp.arange(n), cp.arange(n)] += theta.astype(cp.float32)
        # M is only a preconditioner (float32 GEMM); regularize it until the factorization succeeds
        dmax = float(M.diagonal().max()); reg = 0.0; L = None
        for _ in range(8):
            try:
                Mr = M if reg == 0 else M + cp.float32(reg) * cp.eye(n, dtype=cp.float32)
                L = cp.linalg.cholesky(Mr)
                if bool(cp.isfinite(L).all()):
                    break
            except Exception:
                pass
            L = None; reg = 1e-6 * dmax if reg == 0 else reg * 10
        if L is None:
            return "cholesky failed at it %d" % it, cp.asnumpy(x)
        del M

        def newton(rxz, rsy, rxw):
            # complementarity residuals: x z = rxz, s y = rsy, (u-x) w = rxw
            # eliminate: dz = (rxz - z dx)/x, dw = (rxw + w dx)/(u-x), dy = (rsy - y ds)/s, ds = A dx + rp
            # (A^T D A + Z/X + W/(U-X)) dx = -rd + A^T((rsy - y rp)/s) + rxz/x - rxw/(u-x)
            r = -rd + cp.where(free, rxz / cp.maximum(x, 1e-300), 0) - cp.where(hu, rxw / xu, 0)
            r = r + ATy((rsy - y * rp) / s)
            dx = _pcg(lambda v: ATy(d * Ax(v)) + theta * v, r, L)
            dx = dx * free
            ds = Ax(dx) + rp
            dy = (rsy - y * ds) / s
            dz = cp.where(free, (rxz - z * dx) / cp.maximum(x, 1e-300), 0)
            dw = cp.where(hu, (rxw + w * dx) / xu, 0)
            return dx, ds, dy, dz, dw

        def step(v, dv):
            neg = dv < 0
            if not bool(neg.any()):
                return 1.0
            return min(1.0, float(cp.min(-v[neg] / dv[neg])))

        def max_step(dx, ds, dy, dz, dw):
            ap = min(step(x[free], dx[free]), step(s, ds), step(xu[hu], -dx[hu]) if bool(hu.any()) else 1.0)
            ad = min(step(y, dy), step(z[free], dz[free]), step(w[hu], dw[hu]) if bool(hu.any()) else 1.0)
            return ap, ad

        # predictor (affine scaling)
        aff = newton(-x * z, -s * y, -xu * w)
        ap, ad = max_step(*aff)
        dx, ds, dy, dz, dw = aff
        xa, sa, ya, za, wa = x + ap * dx, s + ap * ds, y + ad * dy, z + ad * dz, w + ad * dw
        xua = cp.where(hu, u_ - xa, 1.0)
        mua = (float(sa @ ya) + float(xa @ za) + float((xua * wa)[hu].sum())) / (m + int(free.sum()) + int(hu.sum()))
        sigma = (mua / mu) ** 3
        # corrector
        cor = newton(sigma * mu * free - x * z - dx * dz, sigma * mu - s * y - ds * dy,
                     cp.where(hu, sigma * mu - xu * w + dx * dw, 0))
        ap, ad = max_step(*cor)
        ap *= 0.995; ad *= 0.995
        dx, ds, dy, dz, dw = cor
        x = x + ap * dx; s = s + ap * ds
        y = y + ad * dy; z = z + ad * dz; w = w + ad * dw
    return "iteration limit", cp.asnumpy(x)


def _pcg(Mv, r, L, tol=1e-12, maxit=50):
    """Solve M x = r by CG preconditioned with the Cholesky factor L of an approximation of M."""
    x = _chol_solve(L, r); res = r - Mv(x); nr = float(cp.linalg.norm(r)) or 1.0
    if float(cp.linalg.norm(res)) <= tol * nr:
        return x
    zz = _chol_solve(L, res); p = zz.copy(); rz = float(res @ zz)
    for _ in range(maxit):
        q = Mv(p); a = rz / float(p @ q)
        x += a * p; res -= a * q
        if float(cp.linalg.norm(res)) <= tol * nr:
            break
        zz = _chol_solve(L, res); rz2 = float(res @ zz); p = zz + (rz2 / rz) * p; rz = rz2
    return x


def _chol_solve(L, r):
    from cupyx.scipy.linalg import solve_triangular
    t = solve_triangular(L, r.astype(L.dtype), lower=True)
    return solve_triangular(L.T, t, lower=False).astype(cp.float64)
