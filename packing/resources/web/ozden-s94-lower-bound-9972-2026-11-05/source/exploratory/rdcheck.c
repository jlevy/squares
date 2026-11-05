/* rdcheck: branch-and-bound checker for rectangle-density certificates on an angle net.
 * Reads a prepared instance (prep.py) and, for each requested net direction, certifies
 *   min over centres c in [L/2, U_r]^2 of  mu(core_r(c))  >= 1
 * or reports a counterexample candidate / unresolved.  See results/SOUNDNESS.md. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define REAL double
#define SUF _d
#include "geom.h"
#undef REAL
#undef SUF
#define REAL long double
#define SUF _l
#include "geom.h"
#undef REAL
#undef SUF

typedef struct { double x1, y1, x2, y2, rho, mass, mx, my, wx, wy; long double lx1, ly1, lx2, ly2, lrho, lmass; } Rect;
typedef struct { int r; long long cn, sn, den; double U; } Dir;

static int NR, ND; static Rect *R; static Dir *DIRS;
static double L2, HIN, HOUT; static long double LHIN;   /* L/2 rounded down, core half side (shrunk) */

/* error constants (see SOUNDNESS.md, lemma F) */
#define TAU 1e-11
#define EAREA_D 2e-13     /* per unit density, per term, double */
#define EAREA_L 2e-16     /* per unit density, per term, long double */
#define ELEN 1e-11        /* absolute slack on edge-length enclosures (times density) */

static long double rdl(const char *s, int dir) { /* parse decimal, then nudge 1 ulp in direction dir (-1 down, +1 up, 0 none) */
    long double v = strtold(s, NULL);
    if (dir < 0) v = nextafterl(v, -INFINITY); else if (dir > 0) v = nextafterl(v, INFINITY);
    return v;
}
static double dn(long double v){ double d = (double)v; if ((long double)d > v) d = nextafter(d, -INFINITY); return d; }
static double up(long double v){ double d = (double)v; if ((long double)d < v) d = nextafter(d, INFINITY); return d; }

static void load(const char *fn) {
    FILE *f = fopen(fn, "r"); if (!f) { perror(fn); exit(2); }
    char a[6][128];
    if (fscanf(f, "%127s %127s", a[0], a[1]) != 2) exit(3);
    L2 = dn(rdl(a[0], -1)); LHIN = rdl(a[1], -1) - 1e-15L; HIN = dn(LHIN) - 2e-15; HOUT = up(rdl(a[1], 1)) + 2e-15;
    if (fscanf(f, "%d", &NR) != 1) exit(3);
    R = calloc(NR, sizeof(Rect));
    for (int i = 0; i < NR; i++) {
        if (fscanf(f, "%127s %127s %127s %127s %127s", a[0], a[1], a[2], a[3], a[4]) != 5) exit(4);
        Rect *q = &R[i];
        q->lx1 = rdl(a[0], 1); q->ly1 = rdl(a[1], 1); q->lx2 = rdl(a[2], -1); q->ly2 = rdl(a[3], -1); q->lrho = rdl(a[4], -1);
        q->x1 = up(q->lx1); q->y1 = up(q->ly1); q->x2 = dn(q->lx2); q->y2 = dn(q->ly2); q->rho = dn(q->lrho);
        if (!(q->x1 < q->x2 && q->y1 < q->y2 && q->rho >= 0)) { fprintf(stderr, "bad rect %d\n", i); exit(5); }
        long double m = q->lrho * (q->lx2 - q->lx1) * (q->ly2 - q->ly1);
        q->lmass = m * (1 - 1e-17L);
        q->mass = dn(q->lmass) * (1 - 1e-15);
        q->mx = 0.5 * (q->x1 + q->x2); q->my = 0.5 * (q->y1 + q->y2);
        q->wx = up(0.5L * ((long double)q->x2 - q->x1)) * (1 + 1e-15); q->wy = up(0.5L * ((long double)q->y2 - q->y1)) * (1 + 1e-15);
        /* the box [mx-wx, mx+wx] contains [x1,x2] up to rounding of mx: enlarge wx by |mx error| */
        q->wx += 4e-16 * fabs(q->mx); q->wy += 4e-16 * fabs(q->my);
    }
    if (fscanf(f, "%d", &ND) != 1) exit(3);
    DIRS = calloc(ND, sizeof(Dir));
    for (int i = 0; i < ND; i++) {
        if (fscanf(f, "%d %lld %lld %lld %127s", &DIRS[i].r, &DIRS[i].cn, &DIRS[i].sn, &DIRS[i].den, a[0]) != 5) exit(6);
        DIRS[i].U = up(rdl(a[0], 1));
    }
    fclose(f);
}

typedef struct { double lo[2], hi[2]; int off, len; double ins; long double lins; int depth; } Node;

typedef struct { long long nodes, ldre; double minbound, mincentre, argx, argy; int verdict; double cx, cy, cval; } Res;
enum { V_OK = 0, V_CEX = 1, V_UNRES = 2 };

static int *pool; static long pool_cap; static Node *stk; static int stk_cap = 1 << 16;

#define MINTOL 1e-7
static double CUTSZ = 0.004; static int MAXCUT = 4000, ncut = 0; static double cutx[100000], cuty[100000], cutv[100000];
static Res run_dir(const Dir *D, int stop_on_cex, double thr0) {
    double thr = thr0;
    Res res = {0}; res.minbound = INFINITY; res.mincentre = INFINITY;
    double c = (double)D->cn / (double)D->den, s = (double)D->sn / (double)D->den;
    long double lc = (long double)D->cn / (long double)D->den, ls = (long double)D->sn / (long double)D->den;
    /* (double)cn and (double)den are exact (< 2^53); division correctly rounded. */
    double Hb_out = (c + s) * HOUT * (1 + 1e-14);
    int sp = 0; long top = 0;
    for (int i = 0; i < NR; i++) pool[i] = i; top = NR;
    if (D->U <= L2) { res.verdict = V_OK; res.minbound = INFINITY; return res; }
    stk[sp++] = (Node){{L2, L2}, {D->U, D->U}, 0, NR, 0.0, 0.0L, 0};
    long unres = 0;
    while (sp > 0) {
        Node N = stk[--sp];
        top = N.off + N.len;
        res.nodes++;
        double px = 0.5 * (N.lo[0] + N.hi[0]), py = 0.5 * (N.lo[1] + N.hi[1]);
        double dx = fmax(N.hi[0] - px, px - N.lo[0]), dy = fmax(N.hi[1] - py, py - N.lo[1]); /* exact (Sterbenz) */
        double bu = (c * dx + s * dy) * (1 + 1e-15), bv = (s * dx + c * dy) * (1 + 1e-15);
        if (top + N.len > pool_cap) { fprintf(stderr, "pool overflow\n"); exit(7); }
        int *kept = pool + top; int nk = 0;
        double ins = N.ins; long double lins = N.lins;
        double A = 0, E = 0, gxl = 0, gxh = 0, gyl = 0, gyh = 0, srho = 0;
        double am = HIN - bu, bm = HIN - bv, ap = HOUT + bu, bp = HOUT + bv;
        for (int k = 0; k < N.len; k++) {
            int idx = pool[N.off + k]; const Rect *q = &R[idx];
            double Dx = q->mx - px, Dy = q->my - py;
            double du = fabs(c * Dx + s * Dy), dv = fabs(-s * Dx + c * Dy);
            double eu = c * q->wx + s * q->wy, ev = s * q->wx + c * q->wy;
            if (du + eu + bu <= HIN - TAU && dv + ev + bv <= HIN - TAU) { ins += q->mass; lins += q->lmass; continue; }
            if (du >= eu + HOUT + bu + TAU || dv >= ev + HOUT + bv + TAU ||
                fabs(Dx) >= q->wx + dx + Hb_out + TAU || fabs(Dy) >= q->wy + dy + Hb_out + TAU) continue; /* dropped: any subset is a lower bound */
            kept[nk++] = idx;
            double x1 = q->x1 - px, x2 = q->x2 - px, y1 = q->y1 - py, y2 = q->y2 - py, rho = q->rho;
            A += rho * area_rr_d(x1, x2, y1, y2, c, s, HIN, HIN);
            E += rho * area_rr_d(x1, x2, y1, y2, c, s, am, bm);
            double Ll = seg_rr_d(x1, y1, x1, y2, c, s, am, bm), Lh = seg_rr_d(x1, y1, x1, y2, c, s, ap, bp);
            double Rl = seg_rr_d(x2, y1, x2, y2, c, s, am, bm), Rh = seg_rr_d(x2, y1, x2, y2, c, s, ap, bp);
            double Bl = seg_rr_d(x1, y1, x2, y1, c, s, am, bm), Bh = seg_rr_d(x1, y1, x2, y1, c, s, ap, bp);
            double Tl = seg_rr_d(x1, y2, x2, y2, c, s, am, bm), Th = seg_rr_d(x1, y2, x2, y2, c, s, ap, bp);
            gxl += rho * (Ll - Rh - 2 * ELEN); gxh += rho * (Lh - Rl + 2 * ELEN);
            gyl += rho * (Bl - Th - 2 * ELEN); gyh += rho * (Bh - Tl + 2 * ELEN);
            srho += rho;
        }
        double Gx = fmax(fabs(gxl), fabs(gxh)) * (1 + 1e-12), Gy = fmax(fabs(gyl), fabs(gyh)) * (1 + 1e-12);
        double err = EAREA_D * srho + 1e-13 * ins + 1e-15 * nk;
        double mv = ins + A - Gx * dx - Gy * dy - 1e-12 * (Gx * dx + Gy * dy);
        double eb = ins + E;
        double bound = fmax(mv, eb) - err;
        double centre = ins + A;
        if (centre < res.mincentre) { res.mincentre = centre; res.argx = px; res.argy = py; }
        if (stop_on_cex == 2) thr = fmin(thr0, res.mincentre - MINTOL);
        if (bound < thr && bound + 2 * err + 1e-12 >= thr) {
            /* recompute in long double */
            res.ldre++;
            long double lA = 0, lE = 0, lgxl = 0, lgxh = 0, lgyl = 0, lgyh = 0, lsr = 0;
            long double lbu = ((long double)c * dx + (long double)s * dy), lbv = ((long double)s * dx + (long double)c * dy);
            lbu = (lbu + fabsl(lc - c) * dx + fabsl(ls - s) * dy) * (1 + 1e-18L); lbv = (lbv + fabsl(ls - s) * dx + fabsl(lc - c) * dy) * (1 + 1e-18L);
            long double lam = LHIN - lbu, lbm = LHIN - lbv, lap = LHIN + 2e-15L + lbu, lbp = LHIN + 2e-15L + lbv;
            for (int k = 0; k < nk; k++) {
                const Rect *q = &R[kept[k]];
                long double x1 = q->lx1 - px, x2 = q->lx2 - px, y1 = q->ly1 - py, y2 = q->ly2 - py, rho = q->lrho;
                lA += rho * area_rr_l(x1, x2, y1, y2, lc, ls, LHIN, LHIN);
                lE += rho * area_rr_l(x1, x2, y1, y2, lc, ls, lam, lbm);
                long double Ll = seg_rr_l(x1, y1, x1, y2, lc, ls, lam, lbm), Lh = seg_rr_l(x1, y1, x1, y2, lc, ls, lap, lbp);
                long double Rl = seg_rr_l(x2, y1, x2, y2, lc, ls, lam, lbm), Rh = seg_rr_l(x2, y1, x2, y2, lc, ls, lap, lbp);
                long double Bl = seg_rr_l(x1, y1, x2, y1, lc, ls, lam, lbm), Bh = seg_rr_l(x1, y1, x2, y1, lc, ls, lap, lbp);
                long double Tl = seg_rr_l(x1, y2, x2, y2, lc, ls, lam, lbm), Th = seg_rr_l(x1, y2, x2, y2, lc, ls, lap, lbp);
                lgxl += rho * (Ll - Rh - 2e-13L); lgxh += rho * (Lh - Rl + 2e-13L);
                lgyl += rho * (Bl - Th - 2e-13L); lgyh += rho * (Bh - Tl + 2e-13L);
                lsr += rho;
            }
            long double lGx = fmaxl(fabsl(lgxl), fabsl(lgxh)) * (1 + 1e-15L), lGy = fmaxl(fabsl(lgyl), fabsl(lgyh)) * (1 + 1e-15L);
            long double lerr = EAREA_L * lsr + 1e-16L * lins + 1e-18L * nk;
            long double lmv = lins + lA - lGx * dx - lGy * dy - 1e-15L * (lGx * dx + lGy * dy);
            long double leb = lins + lE;
            long double lb = fmaxl(lmv, leb) - lerr;
            if ((double)lb > bound) bound = (double)dn(lb);
            centre = (double)(lins + lA);
        }
        if (bound >= thr) { if (bound < res.minbound) res.minbound = bound; continue; }
        if (stop_on_cex == 3) {
            if (centre < thr && fmax(dx, dy) < CUTSZ) {
                if (ncut < MAXCUT) { cutx[ncut] = px; cuty[ncut] = py; cutv[ncut] = centre; ncut++; }
                else return res;
                continue;
            }
            if (fmax(dx, dy) < CUTSZ * 0.25) continue;
        }
        else if (stop_on_cex != 2 && centre < thr - 1e-9) {
            res.verdict = V_CEX; res.cx = px; res.cy = py; res.cval = centre;
            if (stop_on_cex) return res;
            continue;
        }
        int ax = (N.hi[0] - N.lo[0]) >= (N.hi[1] - N.lo[1]) ? 0 : 1;
        double mid = 0.5 * (N.lo[ax] + N.hi[ax]);
        if (!(mid > N.lo[ax] && mid < N.hi[ax]) || (N.hi[ax] - N.lo[ax]) < 1e-12 || N.depth > 120) {
            unres++; if (res.verdict == V_OK) res.verdict = V_UNRES;
            if (centre < res.minbound) res.minbound = centre;
            if (unres > 64) return res; continue;
        }
        if (sp + 2 > stk_cap) { stk_cap *= 2; stk = realloc(stk, stk_cap * sizeof(Node)); }
        Node A1 = N, B1 = N; A1.off = B1.off = (int)top; A1.len = B1.len = nk; A1.ins = B1.ins = ins; A1.lins = B1.lins = lins;
        A1.depth = B1.depth = N.depth + 1;
        A1.hi[ax] = mid; B1.lo[ax] = mid;
        stk[sp++] = B1; stk[sp++] = A1;
        top += nk;
    }
    return res;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: rdcheck inst.txt shard/nshards [stop_on_cex=1] [thr=1]\n"); return 1; }
    load(argv[1]);
    int sh = 0, nsh = 1; sscanf(argv[2], "%d/%d", &sh, &nsh);
    int stop = argc > 3 ? atoi(argv[3]) : 1; double thr = argc > 4 ? atof(argv[4]) : 1.0;
    if (argc > 5) CUTSZ = atof(argv[5]); if (argc > 6) MAXCUT = atoi(argv[6]);
    pool_cap = (long)NR * 200 + 1000000; pool = malloc(pool_cap * sizeof(int)); stk = malloc(stk_cap * sizeof(Node));
    for (int i = sh; i < ND; i += nsh) {
        clock_t t0 = clock();
        ncut = 0;
        Res r = run_dir(&DIRS[i], stop, thr);
        for (int k = 0; k < ncut; k++) printf("{\"cut\": %d, \"x\": %.15g, \"y\": %.15g, \"v\": %.12g}\n", DIRS[i].r, cutx[k], cuty[k], cutv[k]);
        double sec = (double)(clock() - t0) / CLOCKS_PER_SEC;
        const char *v = r.verdict == V_OK ? "VERIFIED" : r.verdict == V_CEX ? "COUNTEREXAMPLE" : "UNRESOLVED";
        printf("{\"r\": %d, \"verdict\": \"%s\", \"nodes\": %lld, \"ld\": %lld, \"min_bound\": %.12f, \"min_centre\": %.12f, \"arg\": [%.12f, %.12f], \"cex\": [%.17g, %.17g, %.12f], \"sec\": %.2f}\n",
               DIRS[i].r, v, r.nodes, r.ldre, r.minbound, r.mincentre, r.argx, r.argy, r.cx, r.cy, r.cval, sec);
        fflush(stdout);
    }
    return 0;
}
