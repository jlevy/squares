#!/usr/bin/env python3
"""s44lp.py -- line-cover LP at s = 7 closed by zmx2 UNCERT rows (target: total < 44).
Built on evand's line_cover.MixedModel (copied to tools/).  [measured] tool: nothing here is a proof;
the proof is a separate zmx2 / zm_mixed run on the exported, scaled file.

loop: LP (persistent HiGHS, dual simplex warm start; first solve IPM+crossover) -> export round cover R ->
      float separation (lattice 0.01 at angle_list, polish) -> zmx2 --d4 on R x f_t (f_t = TARGET/LP) ->
      UNCERT poses as permanent rows -> repeat.  Stops when zmx2 verifies R x f_t with total < 44.
"""
import sys, os, math, time, json, subprocess, re
sys.path.insert(0, '/home/claude/sq/work/s44/tools')
import numpy as np
import line_cover as LC, closed4 as C, family_rows as F, mixed_cover as MC

W = os.environ.get('WORK', '/home/claude/sq/work/s44')
Z = '/home/claude/sq/work/s44/tools/verify2/target/release/zmx2'
S = float(os.environ.get('SIDE', '7'))
TARGET = float(os.environ.get('TARGET', '43.995'))
TAG = sys.argv[1]
WARM = sys.argv[2]                       # mixed cover file used for columns + initial rows
EXTRA = sys.argv[3:]                     # files of extra permanent poses (cx cy th)
LOG = open(f'{W}/runs/{TAG}.log', 'a')


def log(m):
    m = time.strftime('%H:%M:%S ') + m
    print(m, flush=True); LOG.write(m + '\n'); LOG.flush()


pat = re.compile(r"x\[([-\d.]+),([-\d.]+)\] y\[([-\d.]+),([-\d.]+)\] u\[([-\d.]+),([-\d.]+)\].*float-min ([-\d.]+) at "
                 r"\(([-\d.]+),([-\d.]+),u ([-\d.]+)\)")


def uncert_poses(path):
    out = []
    for line in open(path):
        if not line.startswith('UNCERT'): continue
        m = pat.search(line)
        if not m: continue
        x0, x1, y0, y1, u0, u1, fm, fx, fy, fu = map(float, m.groups())
        um = (u0 + u1) / 2
        out.append((fx, fy, 2 * math.atan(fu)))
        out.append(((x0 + x1) / 2, (y0 + y1) / 2, 2 * math.atan(um)))
        out += [(x, y, 2 * math.atan(u)) for x in (x0, x1) for y in (y0, y1) for u in (u0, u1)]
    P = np.array(out).reshape(-1, 3)
    if len(P) == 0: return P
    CL = float(os.environ.get('CL', '0.002')); CLA = float(os.environ.get('CLA', '0.05'))
    key = np.c_[np.round(P[:, 0] / CL), np.round(P[:, 1] / CL), np.round(P[:, 2] / math.radians(CLA))]
    _, idx = np.unique(key, axis=0, return_index=True)
    return P[np.sort(idx)]


def read_poses(path):
    return np.array(C.read_poses(path, S)).reshape(-1, 3)


class A: pass


a = A(); a.s = S; a.q = 50; a.lines = None; a.col_pitch = float(os.environ.get('COLP','0.1')); a.cols_from = os.environ.get('COLS', None if WARM == 'none' else WARM); a.no_line_points = True; a.ban = None
m = LC.build_model(a, log)
prot = []
thetas = [math.radians(d) for d in C.angle_list(0.5)]
cov0 = None if WARM == 'none' else LC.cover_from_file(WARM)[0]


FILT = float(os.environ.get('FILT', '1.01'))


def add(P, protect, filt=True):
    P = np.asarray(P, float).reshape(-1, 3)
    if filt and len(P) and cov0 is not None:
        P = P[cov0.mass(P) < FILT]
    n = m.add_rows(LC.CS.clip_poses(np.asarray(P, float).reshape(-1, 3), S)); prot.extend([protect] * n); return n


t = time.time()
n0 = 0
for th in (thetas if cov0 is not None else []):
    p, v, g = LC._sep((cov0, th, 0.01, (0.0, 0.0), int(os.environ.get('NSEP0','150')), 0.05, 1.003)); n0 += add(p, False)
log(f'warm sep rows {n0} ({time.time() - t:.0f}s)')
for wf in [f for f in os.environ.get('WARMS', '').split(',') if f]:
    cw = LC.cover_from_file(wf)[0]; nw = 0
    for th in thetas:
        p, v, g = LC._sep((cw, th, 0.01, tuple(np.random.rand(2)), 150, 0.05, 1 - 1e-9)); nw += add(p, True, False)
    log(f'replayed lattice sep of {wf}: {nw} rows')
n0 += add(LC.tile_poses(S, 0.004, 0.012, [0.0, 1e-4, 0.01, 0.03, 0.1, 0.3, 1.0]), False)
G = LC.germ_poses(S, int(os.environ.get('GERMQ', '50')), 1e-5, 1); ng = add(G, True)
# coarse uniform family (S60_COVER.md: prevents the LP collapsing onto the lines)
U = []
for d in np.linspace(0, 45, 10):
    th = math.radians(d); lo, hi = C.admissible_box(S, th); g = np.arange(lo, hi + 1e-9, 0.1)
    X, Y = np.meshgrid(g, g); U.append(np.c_[X.ravel(), Y.ravel(), np.full(X.size, th)])
U = np.concatenate(U); U = U[(U[:, 0] <= U[:, 1] + 1e-9) & (U[:, 1] <= S / 2 + 1e-9)]
nu = add(U, True, False)
ne = 0
for f in EXTRA:
    P = uncert_poses(f) if f.endswith('.log') else read_poses(f)
    ne += add(P, True, False)
log(f'rows: {len(m.rows)} (germ {ng}, uniform {nu}, extra {ne}); cols {len(m.sizes)}')


def solve_warm(m):
    import highspy
    A = m.matrix().tocsr(); nr, nc = A.shape; inf = highspy.kHighsInf; sz = np.array(m.sizes, float)
    h = getattr(m, 'hw', None)
    if h is None:
        h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('random_seed', 0); h.setOptionValue('threads', 1)
        h.setOptionValue('solver', 'ipm'); h.setOptionValue('run_crossover', 'on')
        m.hw = h; r0, c0 = 0, 0
    else:
        r0, c0 = m.hw_shape; h.setOptionValue('solver', 'simplex')
    if nc > c0:
        B = A[:r0, c0:].tocsc(); B.sort_indices()
        h.addCols(nc - c0, sz[c0:nc], np.zeros(nc - c0), np.full(nc - c0, inf),
                  int(B.nnz), B.indptr[:-1].astype(np.int32), B.indices.astype(np.int32), B.data.astype(float))
        if r0 > 0: h.setOptionValue('simplex_strategy', 4); h.run()
    if nr > r0:
        B = A[r0:, :].tocsr(); B.sort_indices()
        h.addRows(nr - r0, np.ones(nr - r0), np.full(nr - r0, inf),
                  int(B.nnz), B.indptr[:-1].astype(np.int32), B.indices.astype(np.int32), B.data.astype(float))
    m.hw_shape = (nr, nc)
    if r0 > 0: h.setOptionValue('simplex_strategy', 1)
    h.run()
    if h.getModelStatus() != highspy.HighsModelStatus.kOptimal: return None
    sol = h.getSolution(); x = np.maximum(np.array(sol.col_value), 0.0); y = np.maximum(np.array(sol.row_dual), 0.0)
    return float(sz @ x), x, y, A @ x


def solve_cold(m):
    import highspy
    A = m.matrix().tocsr(); nr, nc = A.shape; inf = highspy.kHighsInf; sz = np.array(m.sizes, float)
    h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('random_seed', 0)
    h.setOptionValue('threads', 1); h.setOptionValue('solver', 'ipm'); h.setOptionValue('run_crossover', 'off')
    h.addVars(nc, np.zeros(nc), np.full(nc, inf)); h.changeColsCost(nc, np.arange(nc, dtype=np.int32), sz)
    A.sort_indices()
    h.addRows(nr, np.ones(nr), np.full(nr, inf), int(A.nnz), A.indptr[:-1].astype(np.int32), A.indices.astype(np.int32), A.data.astype(float))
    h.run()
    if h.getModelStatus() != highspy.HighsModelStatus.kOptimal: return None
    sol = h.getSolution(); x = np.maximum(np.array(sol.col_value), 0.0); y = np.maximum(np.array(sol.row_dual), 0.0)
    x[x < 1e-10] = 0.0; y[y < 1e-10] = 0.0
    del h
    return float(sz @ x), x, y, A @ x


r = 0; t0 = time.time()
while True:
    tl = time.time()
    out = solve_cold(m)
    if out is None: log('LP failed'); break
    val, x, y, Ax = out
    tlp = time.time() - tl
    path = f'{W}/runs/{TAG}_r{r}.txt'
    tot, npt, nsg = m.export(x, path, comment=f's44lp {TAG} round {r} LP {val:.6f}')
    cov = m.cover(x)
    # near-tile separation (tilesep.py): cheap, run every round; skip zmx2 while it still finds deep violations
    ts_out = f'{W}/runs/{TAG}_r{r}_tile.txt'
    so = subprocess.run(['python3', '/home/claude/sq/work/s44/tilesep.py', path, ts_out, '1.0'], capture_output=True, text=True).stdout
    tmin = float(so.strip().split()[-1]) if so.strip() else 0.0
    TP = np.loadtxt(ts_out).reshape(-1, 3) if os.path.getsize(ts_out) else np.zeros((0, 3))
    f_t = TARGET / tot
    log(f'[{TAG}] r{r} LP {val:.6f} tilesep min {tmin:.6f} ({len(TP)} viol); need >= {1 / f_t:.6f} for zmx2')
    if tmin < float(os.environ.get('ZGATE', '0.9985')) / f_t:
        cand = C.price(m, y, pitch=0.02, want=150) if os.environ.get("PRICE","1") == "1" else []; nc = 0
        for cv_, X, Y in cand:
            if (X % 1000 == 0 and 0 < Y < m.K) or (Y % 1000 == 0 and 0 < X < m.K): continue
            nc += m.add_point(X / m.D, Y / m.D, 'priced')
        ts = time.time(); nl = 0; gmin = 9
        for th in thetas:
            p, v, g = LC._sep((cov, th, 0.01, tuple(np.random.rand(2)), 150, 0.05, 1 - 1e-9)); nl += add(p, True, False); gmin = min(gmin, g)
        nt = add(TP, True, False)
        log(f'   +{nc} cols, +{nt} tile rows (perm), +{nl} lattice rows (lat min {gmin:.5f}, {time.time() - ts:.0f}s)')
        np.savetxt(f'{W}/runs/{TAG}_perm_rows.txt', np.array(m.rows)[np.array(prot, bool)], fmt='%.10f'); np.savetxt(f'{W}/runs/{TAG}_all_rows.txt', np.array(m.rows), fmt='%.10f')
        r += 1
        if time.time() - t0 > float(os.environ.get('TLIM', '30000')): log('time limit'); break
        continue
    # zmx2 at the target factor
    sc = f'{W}/runs/{TAG}_r{r}_x.txt'
    LC.scale_file(path, sc, f_t)
    zl = f'{W}/runs/{TAG}_r{r}_x.log'
    tz = time.time()
    zo = subprocess.run(['nice', '-n', '5', Z, 'cert', sc, '--d4', '--threads', os.environ.get('ZT','2'), '--uncert-cap', '400', '--log', zl],
                        capture_output=True, text=True).stdout
    verdict = [l for l in zo.splitlines() if l.startswith(('VERIFIED', 'NOT VERIFIED', 'INCOMPLETE'))]
    ztot = [l for l in subprocess.run([Z, 'info', sc], capture_output=True, text=True).stdout.splitlines() if l.startswith('total')]
    UP = uncert_poses(zl); nroots = sum(1 for l in open(zl) if l.startswith('ROOT') and int(l.split()[13]) > 0)
    log(f'[{TAG}] r{r} LP {val:.6f} exported {tot:.6f} ({npt} pts {nsg} segs) rows {len(m.rows)} ({sum(prot)} perm) '
        f'lp {tlp:.0f}s | zmx2 x{f_t:.6f}: {verdict} {ztot} bad roots {nroots} uncert poses {len(UP)} ({time.time() - tz:.0f}s)')
    if verdict and verdict[0].startswith('VERIFIED'):
        log(f'[{TAG}] CANDIDATE {sc}'); break
    # pricing (before adding rows: y matches m.rows) new point columns
    cand = C.price(m, y, pitch=0.02, want=150) if os.environ.get("PRICE","1") == "1" else []; nc = 0
    for cv_, X, Y in cand:
        if (X % 1000 == 0 and 0 < Y < m.K) or (Y % 1000 == 0 and 0 < X < m.K): continue
        nc += m.add_point(X / m.D, Y / m.D, 'priced')
    log(f'   +{nc} cols (dual cov {cand[0][0] if cand else 1:.4f})')
    # float separation
    ts = time.time(); nl = 0; gmin = 9
    for th in thetas:
        p, v, g = LC._sep((cov, th, 0.01, tuple(np.random.rand(2)), 150, 0.05, 1 - 1e-9)); nl += add(p, True, False); gmin = min(gmin, g)
    nz = add(UP, True, False) + add(TP, True, False)
    # stencil around uncert float-min poses
    log(f'   +{nz} zmx2 rows (perm), +{nl} lattice rows (lat min {gmin:.5f}, {time.time() - ts:.0f}s)')
    np.savetxt(f'{W}/runs/{TAG}_perm_rows.txt', np.array(m.rows)[np.array(prot, bool)], fmt='%.10f'); np.savetxt(f'{W}/runs/{TAG}_all_rows.txt', np.array(m.rows), fmt='%.10f')
    r += 1
    if time.time() - t0 > float(os.environ.get('TLIM', '30000')): log('time limit'); break
