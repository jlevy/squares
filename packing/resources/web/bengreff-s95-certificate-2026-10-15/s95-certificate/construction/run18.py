"""Cross re-optimization for s(K^2 - 5) = K (K from env SQK), incremental version (backhouse).

run18: run17 with the dense scans of zmx2-failing roots on the GPU in float64 (one process, no pool).

run17: run16 with the LP solved by gpu_ipm (mixed-precision interior point on the GPU; HiGHS IPM as the
fallback when it does not report optimal), and NPROC (default 24) workers for row building.

run16: run15 with the GPU screen first and the zmx2 oracle gated on a nearly clean screen (ORACLE_AT),
and a zmx2 sweep that stops at its uncertified-box cap handled instead of fatal.

run15: run14 generalized to side K: the base is wand125's s(59) cover with a band of width K - 8
inserted (cut at 4), the cross is {x or y in [2.5, K - 2.5]}, and the target is N = K^2 - 5.

Keep the band-inserted s(59) cover fixed in the four corner regions; re-solve all mass in
the cross {x in [lo,hi]} u {y in [lo,hi]} on [0,K]^2. Candidates are the base's own
positions in the cross plus a lattice. HiGHS keeps its basis between rounds and only new
violated rows are added. Every round is saved, so the run can be killed at any time.

IPM version with row pruning: rows whose slack exceeds PRUNE are dropped each round
(they are re-added by the screen if they ever bind again).

run5: rows demand capture >= 1 + MU (built-in certification margin); extra rows are read
from extra_rows.npy (poses from the exact checker) at start-up.

run7: as run5, but lattice candidates lying on an integer line are short segments (2/1000) on that
line (both lines at a crossing), so no free point sits on a segment line (checker germ lemmas).
All extra_rows*.npy files are read.

run8: zmx2 in the loop. Every round: IPM solve -> exact export -> zmx2 D4 sweep -> rows from every
logged uncertified box (float-min pose, box centre, GPU descent from both, dense GPU samples in the
box's root cell) + a 2M-pose GPU screen. Stops when zmx2 finds no real violation off the tiny-angle
germs (those go to zm_mixed). Saves every round.

run9: run8 plus an upper bound CAP on every free point atom (diffuse measure).

run10: run9 with an active-set solve. All rows are kept; each round solves on the rows with slack
< TAU at the previous solution, then checks every stored row and re-solves with any violated ones
added, until none is violated. No pruning of the row store.

run11: run10 plus explicit tile-germ rows at tiny angles (1e-7..1e-5 rad, centre shifts down to
1e-6, clamped inside the walls), and float64 (CPU) screening of the checker poses at tiny angles.

run12: run11 with a reliable oracle. After each solve: exact export -> zmx2 sweep -> for every zmx2-failing
root, a dense float64 scan (walls, small angles, uniform) -> poses below 1 + MU become rows. Optional
EXCLUDE file: point candidates (x y per line) forced to weight 0 (breaks degenerate alignments).
Stops when the scans of all zmx2-failing roots stay >= 1 + MU/2.

run13: run12 plus wall-tile germ rows with a larger margin MU_W (env, default 0.012) at the bottom-wall
tiles of the cross (images by D4): theta in [1e-6, 3e-3], shifts theta*a (a in [-3,3]) along and theta*b
(b in [0,3]) away from the wall.

run14: run13 with the active-set loop stopped once <= 50 stored rows remain violated.

usage: SQK=10 python run18.py PITCH ROUNDS MU CAP [resume.npz]
"""
import numpy as np, time, sys, os
from multiprocessing import Pool
from scipy import sparse
import highspy
from cover import *
from lp import S, C, K, d4_images, candidates, element_capture, refine
from gpu_cuda import GPUMeasure

T0 = time.time()
def log(*a): print("[%6.0fs]" % (time.time() - T0), *a, flush=True)
lo, hi = 2.5, S - 2.5
N = K * K - 5
ZMX2 = os.environ.get("ZMX2", "/home/greff/s76/evand/s12/verify2/target/release/zmx2")
pitch = float(sys.argv[1]); rounds = int(sys.argv[2])
MU = float(sys.argv[3]); CAP = float(sys.argv[4])
resume = sys.argv[5] if len(sys.argv) > 5 else None
tag = "p%.3f_mu%.4f_cap%.4f" % (pitch, MU, CAP)
TAU = float(os.environ.get("TAU", "0.005"))
EXCL = np.zeros(0, dtype=int)
MU_W = float(os.environ.get("MU_W", "0.012"))
import subprocess, re as _re
PRUNE = float(os.environ.get("PRUNE", "0.03"))
ORACLE_AT = int(os.environ.get("ORACLE_AT", "2000"))
CAND_CAP = int(os.environ.get("CAND_CAP", "30000"))     # new rows per round   # run the zmx2 oracle once the screen finds at most this many violators
rng = np.random.default_rng(int(time.time()) % 100000)

c = load_mixed("n59_mixed_cover_8.txt"); b = insert_band(c, 4, K - 8)
qxy, qw, txy, tw = measure_arrays(b)
def in_cross(x, y): return ((x >= lo) & (x <= hi)) | ((y >= lo) & (y <= hi))
pc = in_cross(qxy[:, 0], qxy[:, 1]); mid = (txy[:, :2] + txy[:, 2:]) / 2; sc = in_cross(mid[:, 0], mid[:, 1])
fxy, fw, gxy, gw = qxy[~pc], qw[~pc], txy[~sc], tw[~sc]
fixed_mass = fw.sum() + gw.sum()
lp_pts, lp_segs, _, _, _ = candidates(pitch, lo=lo, hi=hi)
onx = np.isclose(lp_pts[:, 0], np.round(lp_pts[:, 0])); ony = np.isclose(lp_pts[:, 1], np.round(lp_pts[:, 1]))
short = []
for (x, y), a, b_ in zip(lp_pts, onx, ony):
    if a:
        y0 = min(max(y - 0.001, 0), S - 0.002); short.append((x, y0, x, y0 + 0.002))
    if b_:
        x0 = min(max(x - 0.001, 0), S - 0.002); short.append((x0, y, x0 + 0.002, y))
short = np.round(np.array(short), 6)
cand_p = np.unique(np.round(np.concatenate([qxy[pc], lp_pts[~(onx | ony)]]), 6), axis=0)
cand_s = np.unique(np.round(np.concatenate([txy[sc], lp_segs, short]), 6), axis=0)
keys = {}
p_orb = np.array([keys.setdefault(("p",) + tuple(sorted(set(im[0] for im in d4_images(x, y, x, y)))), len(keys)) for x, y in cand_p])
s_orb = np.array([keys.setdefault(("s",) + tuple(sorted(set(d4_images(*s)))), len(keys)) for s in cand_s])
n_orb = len(keys)
Mp = sparse.csr_matrix((np.ones(len(p_orb)), (np.arange(len(p_orb)), p_orb)), shape=(len(p_orb), n_orb))
Ms = sparse.csr_matrix((np.ones(len(s_orb)), (np.arange(len(s_orb)), s_orb)), shape=(len(s_orb), n_orb))
osize = np.asarray(Mp.sum(0)).ravel() + np.asarray(Ms.sum(0)).ravel()
log("fixed %.5f; cross budget < %.5f; %d pts %d segs, %d orbits" % (fixed_mass, N - fixed_mass, len(cand_p), len(cand_s), n_orb))
if os.path.exists("exclude_points.txt"):
    ex_pts = np.loadtxt("exclude_points.txt", ndmin=2)
    hit = set()
    for (ex_x, ex_y) in ex_pts:
        j = np.where((np.abs(cand_p[:, 0] - ex_x) < 1e-9) & (np.abs(cand_p[:, 1] - ex_y) < 1e-9))[0]
        hit |= set(p_orb[j].tolist())
    EXCL = np.array(sorted(hit), dtype=int)
    log("excluded point orbits: %d (from %d listed points)" % (len(EXCL), len(ex_pts)))


def meets_cross(P):
    w = np.abs(np.cos(P[:, 2])) + np.abs(np.sin(P[:, 2]))
    x0, x1, y0, y1 = P[:, 0] - w / 2, P[:, 0] + w / 2, P[:, 1] - w / 2, P[:, 1] + w / 2
    return ((x1 >= lo) & (x0 <= hi)) | ((y1 >= lo) & (y0 <= hi))


def poses(n):
    out = []
    while sum(len(o) for o in out) < n:
        P = random_poses(3 * n, S, rng); out.append(P[meets_cross(P)])
    return np.concatenate(out)[:n]


def _rows_chunk(P):
    base = capture_cpu(P, fxy, fw, gxy, gw, tol=1e-9)
    keep = base < 1 + MU - 1e-12
    P = P[keep]
    if len(P) == 0:
        return P, sparse.csr_matrix((0, n_orb)), np.zeros(0)
    Pm, Sm = element_capture(P, cand_p, cand_s)
    A = (sparse.csr_matrix(Pm) @ Mp + sparse.csr_matrix(Sm) @ Ms).tocsr()
    return P, A, 1 + MU - base[keep]


def rows_for(P, pool):
    parts = pool.map(_rows_chunk, [P[i:i + 48] for i in range(0, len(P), 48)])
    parts = [p for p in parts if len(p[0])]
    if not parts:
        return np.zeros((0, 3)), sparse.csr_matrix((0, n_orb)), np.zeros(0)
    return (np.concatenate([p[0] for p in parts]), sparse.vstack([p[1] for p in parts]).tocsr(),
            np.concatenate([p[2] for p in parts]))


def gpu_inputs(xv):
    wp_, ws_ = Mp @ xv, Ms @ xv; a_, b_ = wp_ > 1e-12, ws_ > 1e-12
    return (np.concatenate([fxy, cand_p[a_]]), np.concatenate([fw, wp_[a_]]),
            np.concatenate([gxy, cand_s[b_]]), np.concatenate([gw, ws_[b_]]))


SCAN_LOW = [0, S]


def _scan_poses(reg, seed):
    """The dense scan poses of one root: uniform, wall contact, small angles, structured tile germs."""
    from fractions import Fraction as Fr
    rg = np.random.default_rng(seed)
    x0, x1, y0, y1, u0, u1 = [float(Fr(v)) for v in reg.split(",")]
    N = 200000
    u = rg.uniform(u0, u1, N); h = N // 4
    u[2 * h:3 * h] = rg.uniform(u0, u0 + (u1 - u0) / 40, h)
    th = 2 * np.arctan(u); w = np.cos(th) + np.sin(th)
    cx = rg.uniform(x0, x1, N); cy = rg.uniform(y0, y1, N)
    cx[:h] = np.where(cx[:h] < C, w[:h] / 2, S - w[:h] / 2)
    cy[h:2 * h] = np.where(cy[h:2 * h] < C, w[h:2 * h] / 2, S - w[h:2 * h] / 2)
    cx = np.clip(cx, w / 2, S - w / 2); cy = np.clip(cy, w / 2, S - w / 2)
    Q = np.stack([cx, cy, th], 1)
    # structured tile-germ samples: (tile centre + th*a, tile centre + th*b, th), a, b in [-3, 3]
    G_ = []
    for kx in range(K):
        for ky in range(K):
            tx, ty = kx + 0.5, ky + 0.5
            if not (x0 - 0.06 <= tx <= x1 + 0.06 and y0 - 0.06 <= ty <= y1 + 0.06): continue
            for thg in np.geomspace(max(2 * np.arctan(u0), 1e-6), 2 * np.arctan(min(u1, 0.06)), 12):
                a_ = np.arange(-3, 3.0001, 0.05)
                A_, B_ = np.meshgrid(a_, a_)
                wg = np.cos(thg) + np.sin(thg)
                gx = np.clip(tx + thg * A_.ravel(), wg / 2, S - wg / 2); gy = np.clip(ty + thg * B_.ravel(), wg / 2, S - wg / 2)
                G_.append(np.stack([gx, gy, np.full(gx.shape, thg)], 1))
    if G_:
        Q = np.concatenate([Q] + G_)
    cx, cy = Q[:, 0], Q[:, 1]
    return Q[(cx >= x0) & (cx <= x1) & (cy >= y0) & (cy <= y1)]


def scan_roots(regs, xv):
    if not regs:
        SCAN_LOW[0] = 0; SCAN_LOW[1] = S; return np.zeros((0, 3))
    pxy_, pw_, sxy_, sw_ = gpu_inputs(xv)
    G64 = GPUMeasure(pxy_, pw_, sxy_, sw_, dtype=np.float64)
    lows, mins = [], []
    for i, r_ in enumerate(regs):
        Q = _scan_poses(r_, 100 + i)
        if len(Q) == 0: continue
        c = G64.capture(Q, tol=1e-12, chunk=256)
        lows.append(Q[c < 1 + MU][np.argsort(c[c < 1 + MU])[:3000]]); mins.append(float(c.min()))
    del G64
    lows = [a for a in lows if len(a)]
    P = np.concatenate(lows) if lows else np.zeros((0, 3))
    if not mins: mins = [S]
    if len(P):
        cP = capture_cpu(P, pxy_, pw_, sxy_, sw_, tol=1e-12); SCAN_LOW[0] = int((cP < 1 + MU / 2).sum())
    else:
        SCAN_LOW[0] = 0
    SCAN_LOW[1] = min(mins)
    return P


def wall_germ_poses():
    out = []
    for tx in np.arange(2.5, C + 1e-9, 1.0):
        for thg in np.geomspace(1e-6, 3e-3, 8):
            wg = np.cos(thg) + np.sin(thg)
            a_ = np.arange(-3, 3.0001, 0.1); b_ = np.arange(0, 3.0001, 0.1)
            A_, B_ = np.meshgrid(a_, b_)
            gx = tx + thg * A_.ravel(); gy = np.maximum(0.5 + thg * B_.ravel(), wg / 2)
            out.append(np.stack([gx, gy, np.full(gx.shape, thg)], 1))
    P = np.concatenate(out)
    return P[admissible(P, S) & meets_cross(P)]


def special():
    sp = []
    for i in range(K):
        for j in range(K):
            for th in [0, 1e-4, 1e-3, 0.01, 0.04]:
                for sx in [-0.2, -0.05, 0, 0.05, 0.2]:
                    for sy in [-0.2, 0, 0.2]:
                        sp.append((i + .5 + sx, j + .5 + sy, th)); sp.append((i + .5 + sy, j + .5 + sx, th))
    for i in range(K):
        for j in range(K):
            for th in [1e-7, 1e-6, 1e-5]:
                w = np.cos(th) + np.sin(th)
                for sx in [-1e-5, -1e-6, 0, 1e-6, 1e-5]:
                    for sy in [-1e-5, 0, 1e-5]:
                        for (a_, b_) in ((i + .5 + sx, j + .5 + sy), (i + .5 + sy, j + .5 + sx)):
                            sp.append((min(max(a_, w / 2), S - w / 2), min(max(b_, w / 2), S - w / 2), th))
    sp = np.array(sp)
    return sp[admissible(sp, S) & meets_cross(sp)]


if __name__ == "__main__":
    pool = Pool(int(os.environ.get("NPROC", "24")))
    inf = highspy.kHighsInf
    import gpu_ipm, cupy

    def solve(A, rhs):
        ubv = np.full(n_orb, np.inf); ubv[np.unique(p_orb)] = CAP; ubv[EXCL] = 0.0
        if os.environ.get("LP_SOLVER", "gpu") == "gpu":
            cupy.get_default_memory_pool().free_all_blocks()
            t_ = time.time()
            try:
                st_, xg = gpu_ipm.solve(A, rhs, osize.astype(np.float64), ubv)
            except Exception as e:
                st_, xg = "error: %r" % (e,), None
            cupy.get_default_memory_pool().free_all_blocks()
            log("      gpu ipm: %s, %.1fs, %d rows" % (st_, time.time() - t_, A.shape[0]))
            if st_.startswith("optimal"):
                return highspy.HighsModelStatus.kOptimal, np.clip(xg, 0, ubv)
            log("      falling back to HiGHS")
        h = highspy.Highs(); h.setOptionValue("output_flag", False)
        h.setOptionValue("solver", "ipm"); h.setOptionValue("run_crossover", "off")
        ub = np.full(n_orb, inf); ub[np.unique(p_orb)] = CAP
        ub[EXCL] = 0.0
        h.addVars(n_orb, np.zeros(n_orb), ub)
        h.changeColsCost(n_orb, np.arange(n_orb, dtype=np.int32), osize.astype(np.float64))
        A = A.tocsr(); A.sort_indices()
        h.addRows(A.shape[0], rhs.astype(np.float64), np.full(A.shape[0], inf), A.nnz,
                  A.indptr[:-1].astype(np.int32), A.indices.astype(np.int32), A.data.astype(np.float64))
        h.run()
        return h.getModelStatus(), np.maximum(np.array(h.getSolution().col_value), 0)

    if resume:
        z = np.load(resume); P0 = np.concatenate([z["rowsP"], special()])
    import glob
    exl = [np.load(f) for f in sorted(glob.glob("extra_rows*.npy"))]
    if exl:
        ex = np.concatenate(exl); ex = ex[admissible(ex, S) & meets_cross(ex)]
        P0 = np.concatenate([P0, ex]); log("extra rows from checker: %d" % len(ex))
    elif not resume:
        P0 = np.concatenate([special(), poses(15000)])
    P0 = np.unique(np.round(P0, 9), axis=0)
    if resume and "x" in z.files and len(z["x"]) == n_orb:
        x0 = z["x"]; wp0, ws0 = Mp @ x0, Ms @ x0; s0, t0 = wp0 > 1e-12, ws0 > 1e-12
        G0 = GPUMeasure(np.concatenate([fxy, cand_p[s0]]), np.concatenate([fw, wp0[s0]]),
                        np.concatenate([gxy, cand_s[t0]]), np.concatenate([gw, ws0[t0]]))
        c0 = G0.capture(P0); keep0 = c0 < 1 + MU + PRUNE
        log("startup filter: %d of %d poses tight/violated under the resumed solution" % (keep0.sum(), len(P0)))
        P0 = np.concatenate([P0[keep0], special()])
        # deepen the checker's poses: GPU local descent from every violated checker pose
        if exl:
            exv = ex[G0.capture(ex) < 1 + MU]
            if len(exv):
                refd, rcd = refine(G0, exv, steps=30, scale=0.01, rng=rng, region=meets_cross)
                okd = admissible(refd, S) & meets_cross(refd) & (rcd < 1 + MU)
                P0 = np.concatenate([P0, refd[okd]])
                log("checker-pose descent: %d violated starts -> %d deepened rows (min %.5f)" % (len(exv), okd.sum(), rcd[okd].min() if okd.any() else 9))
    rowsP, A, rhs = rows_for(P0, pool)
    Pw = wall_germ_poses()
    Pw_, Aw, rw = rows_for(Pw, pool)
    rw = rw + (MU_W - MU)
    rowsP = np.concatenate([rowsP, Pw_]); A = sparse.vstack([A, Aw]).tocsr(); rhs = np.concatenate([rhs, rw])
    log("initial rows %d (PRUNE %.3f), incl. %d wall-germ rows at margin %.3f" % (len(rhs), PRUNE, len(rw), MU_W))
    hist = []
    for rd in range(rounds):
        t = time.time()
        if rd == 0 and not (resume and "x" in z.files and len(z["x"]) == n_orb):
            active = np.ones(len(rhs), bool)
        else:
            xp = x if rd > 0 else z["x"]
            active = (A @ xp - rhs) < TAU
        for inner in range(8):
            st, x = solve(A[active], rhs[active])
            if st != highspy.HighsModelStatus.kOptimal: break
            viol = (A @ x - rhs) < -1e-7
            log("   active-set solve %d: %d of %d rows, violated afterwards %d" % (inner, active.sum(), len(rhs), viol.sum()))
            if not viol.any(): break
            if viol.sum() <= 50:
                log("   (stopping the inner loop: %d violated rows left for the next round)" % viol.sum()); break
            active |= viol
        ts = time.time() - t
        if st != highspy.HighsModelStatus.kOptimal:
            log("LP status", st); break
        m = float(osize @ x)
        slack = A @ x - rhs
        wp, ws = Mp @ x, Ms @ x; sp_, ss_ = wp > 1e-12, ws > 1e-12
        G = GPUMeasure(np.concatenate([fxy, cand_p[sp_]]), np.concatenate([fw, wp[sp_]]),
                       np.concatenate([gxy, cand_s[ss_]]), np.concatenate([gw, ws[ss_]]))
        np.savez("cross_%s.npz" % tag, x=x, cand_p=cand_p, cand_s=cand_s, p_orb=p_orb, s_orb=s_orb,
                 rowsP=rowsP, rhs=rhs, hist=np.array(hist), fixed_mass=fixed_mass)
        # cheap GPU screen first; the zmx2 oracle runs only once the screen is nearly clean
        Rr = poses(2000000); cr = G.capture(Rr)
        worst = Rr[np.argsort(cr)[:20000]]; ref, rc = refine(G, worst, steps=40, rng=rng, region=meets_cross)
        ok = meets_cross(ref) & admissible(ref, S)
        scr = np.concatenate([Rr[cr < 1 + MU - 1e-6], ref[(rc < 1 + MU - 1e-6) & ok]])
        mn = min(cr.min(), rc[ok].min() if ok.any() else 9)
        zrows = np.zeros((0, 3))
        if len(scr) > ORACLE_AT:
            log("   screen: %d violators (min %.5f); zmx2 oracle skipped this round" % (len(scr), mn))
        else:
            subprocess.run(["python", "export_cover.py", "cross_%s.npz" % tag, "1.0", "cand%d_%s.txt" % (N, tag)], check=True,
                           stdout=subprocess.DEVNULL)
            zlog = "zmx2_%s.r%d.log" % (tag, rd)
            if os.path.exists(zlog): os.remove(zlog)          # zmx2 refuses an existing --log path
            zo = subprocess.run([ZMX2, "cert", "cand%d_%s.txt" % (N, tag), "--d4", "--threads", "20",
                                 "--uncert-cap", os.environ.get("ZCAP", "20000"), "--log", zlog], capture_output=True, text=True).stdout
            verified = "VERIFIED-D4" in zo and "NOT VERIFIED" not in zo
            unc = _re.search(r"uncertified (\d+)", zo); unc = int(unc.group(1)) if unc else -1
            fail_roots = sorted(set(mm_.group(1) for ln in open(zlog) if ln.startswith("ROOT")
                                    for mm_ in [_re.search(r"root (\S+) .*uncert (\d+)", ln)] if mm_ and int(mm_.group(2)) > 0))
            if unc < 0:
                log("   zmx2 stopped early (uncertified-box cap); %d failing roots logged so far, scanning at most 96" % len(fail_roots))
                fail_roots = fail_roots[:96]
            scanP = scan_roots(fail_roots, x)
            zp = scanP
            if len(zp):
                zp = zp[admissible(zp, S) & meets_cross(zp)]
                zc = capture_cpu(zp, *gpu_inputs(x), tol=1e-12)
                zv = zp[zc < 1 + MU - 1e-6]
                zref, zrc = refine(G, zv, steps=30, scale=0.01, rng=rng, region=meets_cross) if len(zv) else (zv, np.zeros(0))
                zok = admissible(zref, S) & meets_cross(zref) & (zrc < 1 + MU - 1e-6)
                zrows = np.concatenate([zv, zref[zok]])
            log("   zmx2: %s uncertified %d | checker rows %d" % ("VERIFIED" if verified else "not verified", unc, len(zrows)))
            log("   oracle: %d zmx2-failing roots, %d scanned poses below 1 + MU/2 (min %.6f)" % (len(fail_roots), SCAN_LOW[0], SCAN_LOW[1]))
            if unc >= 0 and (verified or SCAN_LOW[0] == 0) and mn >= 1 + MU / 2:
                log("screen min >= 1 + MU/2 and scans of all zmx2-failing roots stay >= 1 + MU/2: stop and hand to zm_mixed")
                np.savez("cross_%s.npz" % tag, x=x, cand_p=cand_p, cand_s=cand_s, p_orb=p_orb, s_orb=s_orb, rowsP=rowsP, rhs=rhs)
                break
        cand = np.concatenate([zrows, scr])
        hist.append((rd, m, fixed_mass + m, len(rhs), mn, len(cand)))
        log("round %2d: IPM %.1fs | cross %.5f -> total %.5f (need < %d) | rows %d (binding %d) | min cap %.5f | violators %d | support %d"
            % (rd, ts, m, fixed_mass + m, N, len(rhs), int((slack < 1e-6).sum()), mn, len(cand), sp_.sum() + ss_.sum()))
        np.savez("cross_%s.npz" % tag, x=x, cand_p=cand_p, cand_s=cand_s, p_orb=p_orb, s_orb=s_orb,
                 rowsP=rowsP, rhs=rhs, hist=np.array(hist), fixed_mass=fixed_mass)
        if len(cand) > CAND_CAP:
            cand = cand[np.argsort(G.capture(cand))[:CAND_CAP]]
        Pn, An, rn = rows_for(cand, pool)
        rowsP = np.concatenate([rowsP, Pn]); A = sparse.vstack([A, An]).tocsr(); rhs = np.concatenate([rhs, rn])
    log("done")
