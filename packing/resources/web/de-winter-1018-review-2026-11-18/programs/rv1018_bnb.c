/* rv1018_bnb.c: a clean-room branch and bound for the blind review of jlevy/squares#1018
 * (lane r108-1118). Written from the mathematics; it shares no code with sqverify_fast or
 * with the source, and neither was read.
 *
 * Claim decided, for one rotated direction with exact cosine c > 0 and sine s > 0: every
 * closed square Q(p) of half-side h at that angle, centred at any p in the box
 * [XA, XB] x [YA, YB], captures at least T of the measure g = sum_k d_k 1[R_k], a sum of
 * uniform axis-parallel rectangles.
 *
 * Lower bound over a box of centres C with float midpoint p0 and half-widths dx, dy that
 * cover C. Write u' = CF (qx - p0x) + SF (qy - p0y) and v' = -SF (qx - p0x) + CF (qy - p0y)
 * with (CF, SF) the floats given for (c, s), within EPSCS of them, and h' = h - DELTA. For
 * p in C, every q with |u' - du| <= h' and |v' - dv| <= h' lies in Q(p), where
 * du = CF (px - p0x) + SF (py - p0y), |du| <= bu = (c + EPSCS) dx + (s + EPSCS) dy, and dv
 * likewise with bv: the float frame moves points by at most EPSCS (|qx - p0x| + |qy - p0y|),
 * which DELTA covers. So with a = h' - bu and b = h' - bv, the set E = {|u'| <= a, |v'| <= b}
 * lies in every square of the box, and so do the strips S_u+ = (a, a + bu + du] x [-b, b],
 * S_u- = [-a - (bu - du), -a) x [-b, b], S_v+ and S_v- of the square at p (box_bound below
 * explains how the ring of strips is bounded over all p). As g >= 0, the capture at every
 * centre of C is at least g(E) plus that ring.
 *
 * g(E) and the strips are bounded below rectangle by rectangle. A rectangle whose outer-
 * rounded corners lie in E by more than TAU counts its whole mass (rounded down). Any other
 * rectangle counts lower bounds on the areas of its inner-rounded copy in E and in each
 * strip, from the concavity of chord lengths (integ below); EG bounds the float error of a
 * chord. Dropping a rectangle can only lower the bound, so the test that drops rectangles
 * outside every square of the box needs no rigour for soundness, only for efficiency.
 *
 * A child box is a subset of its parent, so a rectangle inside the parent's E lies in Q(p)
 * for every centre of the child: it is counted once, whole, and inherited. Splitting at the
 * float midpoint gives two closed boxes whose union is the parent.
 *
 * Accept when the bound, times (1 - 1e-11) for the rounding of the sums, is at least T.
 * A box that is not accepted is a counterexample candidate when the float estimate at its
 * centre is below T - 1e-12 (the driver then decides that centre exactly); one that reaches
 * the depth limit otherwise is unresolved, and the search goes on, up to 4096 of them. Any
 * candidate, unresolved box or exhausted budget means the direction is not decided.
 *
 * Input: little-endian doubles, a header of 19 values then K records of 10 values (and, in
 * mode 1, boxes of 4 values); see read_input. Output: "key value" lines on stdout.
 */
#define _POSIX_C_SOURCE 200809L
#include <float.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct {
    double x0i, y0i, x1i, y1i; /* inner-rounded corners: the rectangle contains this one */
    double x0o, y0o, x1o, y1o; /* outer-rounded corners: this one contains the rectangle */
    double d;                   /* density, rounded down */
    double m;                   /* exact mass, rounded down */
} Rect;

static int K;
static Rect *R;
static double CF, SF, EPSCS, H_DN, H_UP, DELTA, TAU, EG, T;
static double XA, XB, YA, YB;
static int MAXD;
static double NODECAP;
static int MODE; /* 0: decide; 1: bound each listed box with every rectangle active */

static double up(double x) { return nextafter(x, INFINITY); }
static double dn(double x) { return nextafter(x, -INFINITY); }

/* Integration in the float frame. Points are q = p0 + u' (CF, SF) + v' (-SF, CF). For the
 * rectangle's inner-rounded copy, shifted by -p0 and shrunk to [X0, X1] x [Y0, Y1], the
 * points with a given u' and v' in [V1, V2] form the interval of v' between
 *   max(V1, (CF u' - X1)/SF, (Y0 - SF u')/CF)  and  min(V2, (CF u' - X0)/SF, (Y1 - SF u')/CF),
 * whose length max(0, l(u')) has l concave in u' (a minimum of affine functions less a
 * maximum of affine functions). On any interval between consecutive nodes, the trapezoid of
 * lower bounds of l at its ends is at most the integral of max(0, l) there, and leaving a
 * piece out lowers the sum, so the positive trapezoids give a lower bound on every interval
 * between consecutive cuts (the cuts are nodes). The twelve breakpoints of l make the bound
 * nearly exact; they need not be exact. The map (u', v') -> q has Jacobian CF^2 + SF^2,
 * within 4 eps of 1, which the final factor covers; regions with disjoint parameter ranges
 * are disjoint. In estimate mode the routine estimates instead (no allowance).
 *
 * integ_u: v' in [V1, V2], cuts in u'. integ_v: u' in [U1, U2], cuts in v'. out[i] receives
 * the bound for the cut interval [cut[i], cut[i+1]]. */
#define NCUTMAX (2 * 16)
static void integ(int along_u, const Rect *r, double px, double py, double W1, double W2,
                  const double *cut, int ncut, double *out, int est) {
    double X0 = up(r->x0i - px), X1 = dn(r->x1i - px);
    double Y0 = up(r->y0i - py), Y1 = dn(r->y1i - py);
    for (int i = 0; i + 1 < ncut; i++) out[i] = 0.0;
    if (!(X0 < X1) || !(Y0 < Y1) || !(W1 < W2)) return;
    double bp[12];
    if (along_u) { /* l(u') with v' in [W1, W2] */
        bp[0] = CF * X0 + SF * Y1;
        bp[1] = CF * X1 + SF * Y0;
        bp[2] = CF * X0 + SF * Y0;
        bp[3] = CF * X1 + SF * Y1;
        bp[4] = (X0 + SF * W2) / CF;
        bp[5] = (Y1 - CF * W2) / SF;
        bp[6] = (X1 + SF * W1) / CF;
        bp[7] = (Y0 - CF * W1) / SF;
        bp[8] = (X1 + SF * W2) / CF;
        bp[9] = (Y0 - CF * W2) / SF;
        bp[10] = (X0 + SF * W1) / CF;
        bp[11] = (Y1 - CF * W1) / SF;
    } else { /* l(v') with u' in [W1, W2] */
        bp[0] = CF * Y1 - SF * X1;
        bp[1] = CF * Y0 - SF * X0;
        bp[2] = CF * Y0 - SF * X1;
        bp[3] = CF * Y1 - SF * X0;
        bp[4] = (CF * W2 - X1) / SF;
        bp[5] = (Y1 - SF * W2) / CF;
        bp[6] = (CF * W1 - X0) / SF;
        bp[7] = (Y0 - SF * W1) / CF;
        bp[8] = (CF * W2 - X0) / SF;
        bp[9] = (Y0 - SF * W2) / CF;
        bp[10] = (CF * W1 - X1) / SF;
        bp[11] = (Y1 - SF * W1) / CF;
    }
    double lo = cut[0], hi = cut[ncut - 1];
    for (int i = 0; i < 12; i++) {
        double v = bp[i];
        if (!(v >= lo)) v = lo; /* also maps NaN to lo */
        if (v > hi) v = hi;
        bp[i] = v;
    }
    for (int i = 1; i < 12; i++) {
        double v = bp[i];
        int j = i - 1;
        while (j >= 0 && bp[j] > v) {
            bp[j + 1] = bp[j];
            j--;
        }
        bp[j + 1] = v;
    }
    /* merge the cuts and the breakpoints; remember which cut interval each node opens */
    double z[12 + NCUTMAX];
    int bucket[12 + NCUTMAX];
    int n = 0, ic = 0, ib = 0, cur = -1;
    while (ic < ncut || ib < 12) {
        if (ib >= 12 || (ic < ncut && cut[ic] <= bp[ib])) {
            z[n] = cut[ic];
            cur = ic < ncut - 1 ? ic : ncut - 2;
            ic++;
        } else {
            z[n] = bp[ib];
            ib++;
        }
        bucket[n] = cur < 0 ? 0 : cur;
        n++;
    }
    double lam[12 + NCUTMAX];
    for (int i = 0; i < n; i++) {
        double t = z[i], top, bot;
        if (along_u) {
            top = fmin(fmin(W2, (CF * t - X0) / SF), (Y1 - SF * t) / CF);
            bot = fmax(fmax(W1, (CF * t - X1) / SF), (Y0 - SF * t) / CF);
        } else {
            top = fmin(fmin(W2, (X1 + SF * t) / CF), (Y1 - CF * t) / SF);
            bot = fmax(fmax(W1, (X0 + SF * t) / CF), (Y0 - CF * t) / SF);
        }
        if (est) {
            lam[i] = top - bot;
            if (lam[i] < 0) lam[i] = 0;
        } else {
            lam[i] = dn((top - bot) - EG);
        }
    }
    for (int i = 0; i + 1 < n; i++) {
        double piece = (z[i + 1] - z[i]) * (lam[i] + lam[i + 1]) * 0.5;
        if (piece > 0) out[bucket[i]] += est ? piece : piece * (1.0 - 64.0 * DBL_EPSILON);
    }
}

/* Classify the active rectangles of one box. Returns the bound; writes the rectangles a
 * child must still examine to keep[] and adds newly inside masses to *ins.
 *
 * With MP > 1 the bound adds a ring of strips outside E. In the float frame, every square
 * of the box contains Q'(du, dv) = {-h' + du <= u' <= h' + du, -h' + dv <= v' <= h' + dv},
 * h' = h - DELTA, for some |du| <= bu and |dv| <= bv. Q' holds E, the strips
 * S_u+ = (a, a + bu + du] x [-b, b] and S_u- = [-a - (bu - du), -a) x [-b, b], and S_v+,
 * S_v- likewise ([-a, a] x outside [-b, b]), all disjoint. Each strip's measure is
 * nondecreasing in its thickness, so for du in [-bu + 2bu i/MP, -bu + 2bu (i+1)/MP] the pair
 * captures at least Phi+(2bu i/MP) + Phi-(2bu (MP-1-i)/MP); the ring adds the least of these
 * over i, and the same along v. Every rectangle is counted once: whole if inherited or
 * inside E, and otherwise through its own areas in E and in the strips. */
#define MPMAX 16
static int MP = 1;
static double box_bound(double xa, double xb, double ya, double yb, double inherited,
                        const int *act, int nact, int *keep, int *nkeep, double *ins,
                        double *est_centre) {
    double px = 0.5 * (xa + xb), py = 0.5 * (ya + yb);
    double dx = up(up(fmax(xb - px, px - xa))), dy = up(up(fmax(yb - py, py - ya)));
    double cu = up(CF + EPSCS), su = up(SF + EPSCS);
    double bu = up(up(up(cu * dx) + up(su * dy))), bv = up(up(up(su * dx) + up(cu * dy)));
    double a = dn(dn(H_DN - bu) - DELTA), b = dn(dn(H_DN - bv) - DELTA);
    double ou = H_UP + bu + DELTA + TAU, ov = H_UP + bv + DELTA + TAU;
    double ext = H_UP * (CF + SF) + 1e-9;
    double insum = 0.0, strad = 0.0, est = 0.0;
    int m = (a > 0 && b > 0) ? MP : 1;
    double cutu[NCUTMAX], cutv[NCUTMAX], outb[NCUTMAX];
    double phi[4][MPMAX]; /* u+, u-, v+, v-: index j is thickness about 2 b j / m */
    int nc = 0;
    for (int j = m - 1; j >= 1; j--) cutu[nc++] = dn(-a - dn(2.0 * bu * j / m));
    cutu[nc++] = -a;
    cutu[nc++] = a;
    for (int j = 1; j < m; j++) cutu[nc++] = up(a + dn(2.0 * bu * j / m));
    nc = 0;
    for (int j = m - 1; j >= 1; j--) cutv[nc++] = dn(-b - dn(2.0 * bv * j / m));
    cutv[nc++] = -b;
    cutv[nc++] = b;
    for (int j = 1; j < m; j++) cutv[nc++] = up(b + dn(2.0 * bv * j / m));
    for (int q = 0; q < 4; q++)
        for (int j = 0; j < MPMAX; j++) phi[q][j] = 0.0;
    double ecut[2] = {-H_DN, H_DN};
    int nk = 0;
    for (int t = 0; t < nact; t++) {
        const Rect *r = &R[act[t]];
        if (r->x0o > px + dx + ext || r->x1o < px - dx - ext || r->y0o > py + dy + ext ||
            r->y1o < py - dy - ext)
            continue; /* misses every square of the box */
        double umin = CF * (r->x0o - px) + SF * (r->y0o - py);
        double umax = CF * (r->x1o - px) + SF * (r->y1o - py);
        double vmin = -SF * (r->x1o - px) + CF * (r->y0o - py);
        double vmax = -SF * (r->x0o - px) + CF * (r->y1o - py);
        if (umin > ou || umax < -ou || vmin > ov || vmax < -ov) continue; /* drop */
        if (a > 0 && b > 0 && umin >= -a + TAU && umax <= a - TAU && vmin >= -b + TAU &&
            vmax <= b - TAU) {
            insum += r->m;
            continue; /* inside E: counted here and inherited by the children */
        }
        keep[nk++] = act[t];
        if (a > 0 && b > 0) {
            if (vmax > -b && vmin < b && umax > cutu[0] && umin < cutu[2 * m - 1]) {
                integ(1, r, px, py, -b, b, cutu, 2 * m, outb, 0);
                strad += r->d * outb[m - 1]; /* E: u' in [-a, a], v' in [-b, b] */
                double acc = 0.0;
                for (int j = 1; j < m; j++) { /* u- strips: buckets m-2 down to m-1-j */
                    acc += outb[m - 1 - j];
                    phi[1][j] += r->d * acc;
                }
                acc = 0.0;
                for (int j = 1; j < m; j++) { /* u+ strips: buckets m to m-1+j */
                    acc += outb[m - 1 + j];
                    phi[0][j] += r->d * acc;
                }
            }
            if (m > 1 && umax > -a && umin < a && (vmax > b || vmin < -b)) {
                integ(0, r, px, py, -a, a, cutv, 2 * m, outb, 0);
                double acc = 0.0;
                for (int j = 1; j < m; j++) {
                    acc += outb[m - 1 - j];
                    phi[3][j] += r->d * acc;
                }
                acc = 0.0;
                for (int j = 1; j < m; j++) {
                    acc += outb[m - 1 + j];
                    phi[2][j] += r->d * acc;
                }
            }
        }
        if (est_centre) {
            double eo[1];
            integ(1, r, px, py, -H_DN, H_DN, ecut, 2, eo, 1);
            est += r->d * eo[0];
        }
    }
    double ringsum = 0.0;
    if (m > 1) {
        double mu = INFINITY, mv = INFINITY;
        for (int i = 0; i < m; i++) {
            double su_ = phi[0][i] + phi[1][m - 1 - i];
            double sv_ = phi[2][i] + phi[3][m - 1 - i];
            if (su_ < mu) mu = su_;
            if (sv_ < mv) mv = sv_;
        }
        ringsum = mu + mv;
    }
    *nkeep = nk;
    *ins = insum;
    if (est_centre) *est_centre = inherited + insum + est;
    return (inherited + insum + strad + ringsum) * (1.0 - 1e-11);
}

/* Float estimate of the capture at the box's centre: the inherited and inside masses, and
 * every straddling rectangle's estimated area in the square there. It decides nothing; a
 * value below T - 1e-12 makes the driver evaluate that centre exactly. */
static double centre_estimate(double xa, double xb, double ya, double yb, double counted,
                              const int *keep, int nk) {
    double px = 0.5 * (xa + xb), py = 0.5 * (ya + yb);
    double ecut[2] = {-H_DN, H_DN}, eo[1];
    double est = counted;
    for (int t = 0; t < nk; t++) {
        integ(1, &R[keep[t]], px, py, -H_DN, H_DN, ecut, 2, eo, 1);
        est += R[keep[t]].d * eo[0];
    }
    return est;
}

typedef struct {
    double xa, xb, ya, yb, inherited;
    int depth, off, cnt;
} Node;

static double cpu_now(void) {
    struct timespec ts;
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts);
    return ts.tv_sec + 1e-9 * ts.tv_nsec;
}

static int read_input(FILE *f) {
    double hdr[19];
    if (fread(hdr, sizeof(double), 19, f) != 19) return 0;
    if (hdr[0] != 1018.0) return 0;
    K = (int)hdr[1];
    CF = hdr[2];
    SF = hdr[3];
    EPSCS = hdr[4];
    H_DN = hdr[5];
    H_UP = hdr[6];
    DELTA = hdr[7];
    TAU = hdr[8];
    EG = hdr[9];
    T = hdr[10];
    XA = hdr[11];
    XB = hdr[12];
    YA = hdr[13];
    YB = hdr[14];
    MAXD = (int)hdr[15];
    NODECAP = hdr[16];
    MODE = (int)hdr[17];
    MP = (int)hdr[18];
    if (MP < 1 || MP > MPMAX) return 0;
    if (!(CF > 0 && SF > 0 && K > 0 && DELTA >= 2.2 * EPSCS + 1e-15)) return 0;
    R = malloc(sizeof(Rect) * (size_t)K);
    if (!R) return 0;
    for (int k = 0; k < K; k++) {
        double v[10];
        if (fread(v, sizeof(double), 10, f) != 10) return 0;
        R[k] = (Rect){v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8], v[9]};
    }
    return 1;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: rv1018_bnb INPUT.bin\n");
        return 2;
    }
    FILE *f = fopen(argv[1], "rb");
    if (!f || !read_input(f)) {
        fprintf(stderr, "bad input\n");
        return 2;
    }
    int *all = malloc(sizeof(int) * (size_t)K);
    for (int k = 0; k < K; k++) all[k] = k;
    if (MODE == 1) { /* box test: boxes follow the rectangles */
        double bx[4];
        int *keep = malloc(sizeof(int) * (size_t)K);
        while (fread(bx, sizeof(double), 4, f) == 4) {
            int nk;
            double ins, est;
            double bd = box_bound(bx[0], bx[1], bx[2], bx[3], 0.0, all, K, keep, &nk, &ins, &est);
            printf("box %a %a\n", bd, est);
        }
        return 0;
    }
    fclose(f);
    size_t poolcap = (size_t)K * (size_t)(MAXD + 4);
    int *pool = malloc(sizeof(int) * poolcap);
    Node *stack = malloc(sizeof(Node) * (size_t)(2 * MAXD + 8));
    if (!pool || !stack) return 3;
    memcpy(pool, all, sizeof(int) * (size_t)K);
    size_t top = (size_t)K;
    int sp = 0;
    stack[sp++] = (Node){XA, XB, YA, YB, 0.0, 0, 0, K};
    double t0 = cpu_now();
    double nodes = 0, leaves = 0, strad_evals = 0;
    double minb = INFINITY, mb_xa = 0, mb_xb = 0, mb_ya = 0, mb_yb = 0;
    int maxdepth = 0, unresolved = 0;
    const char *verdict = "DECIDED";
    double cand_x = NAN, cand_y = NAN, cand_est = NAN;
    while (sp > 0) {
        Node nd = stack[--sp];
        top = (size_t)nd.off + (size_t)nd.cnt; /* lists above belong to finished nodes */
        nodes += 1;
        if (nodes > NODECAP) {
            verdict = "BUDGET";
            break;
        }
        if (nd.depth > maxdepth) maxdepth = nd.depth;
        int *keep = pool + top;
        int nk;
        double ins;
        double bd = box_bound(nd.xa, nd.xb, nd.ya, nd.yb, nd.inherited, pool + nd.off, nd.cnt,
                              keep, &nk, &ins, NULL);
        strad_evals += nk;
        if (bd >= T) {
            leaves += 1;
            if (bd < minb) {
                minb = bd;
                mb_xa = nd.xa;
                mb_xb = nd.xb;
                mb_ya = nd.ya;
                mb_yb = nd.yb;
            }
            continue;
        }
        double wx = nd.xb - nd.xa, wy = nd.yb - nd.ya;
        double mx = 0.5 * (nd.xa + nd.xb), my = 0.5 * (nd.ya + nd.yb);
        if (nd.depth == 0) { /* every other centre was estimated when its parent split */
            double est = centre_estimate(nd.xa, nd.xb, nd.ya, nd.yb, nd.inherited + ins, keep, nk);
            if (est < T - 1e-12) {
                verdict = "CANDIDATE";
                cand_x = mx;
                cand_y = my;
                cand_est = est;
                break;
            }
        }
        int can_x = mx > nd.xa && mx < nd.xb, can_y = my > nd.ya && my < nd.yb;
        if (nd.depth >= MAXD || (!can_x && !can_y)) {
            leaves += 1;
            unresolved++;
            if (unresolved >= 4096) {
                verdict = "UNRESOLVED";
                break;
            }
            continue;
        }
        size_t off = top;
        top += (size_t)nk;
        double inh = nd.inherited + ins;
        int split_x = can_x && (!can_y || wx >= wy);
        Node lo_child, hi_child;
        if (split_x) {
            lo_child = (Node){nd.xa, mx, nd.ya, nd.yb, inh, nd.depth + 1, (int)off, nk};
            hi_child = (Node){mx, nd.xb, nd.ya, nd.yb, inh, nd.depth + 1, (int)off, nk};
        } else {
            lo_child = (Node){nd.xa, nd.xb, nd.ya, my, inh, nd.depth + 1, (int)off, nk};
            hi_child = (Node){nd.xa, nd.xb, my, nd.yb, inh, nd.depth + 1, (int)off, nk};
        }
        /* Order only: the child whose centre estimate is lower is explored first, so that a
         * search that cannot accept heads for low captures. The estimates also flag
         * candidates. The tree and every acceptance are the same in either order. */
        double e_lo = centre_estimate(lo_child.xa, lo_child.xb, lo_child.ya, lo_child.yb,
                                      inh, keep, nk);
        double e_hi = centre_estimate(hi_child.xa, hi_child.xb, hi_child.ya, hi_child.yb,
                                      inh, keep, nk);
        if (e_lo < T - 1e-12 || e_hi < T - 1e-12) {
            const Node *c = e_lo <= e_hi ? &lo_child : &hi_child;
            verdict = "CANDIDATE";
            cand_x = 0.5 * (c->xa + c->xb);
            cand_y = 0.5 * (c->ya + c->yb);
            cand_est = e_lo <= e_hi ? e_lo : e_hi;
            break;
        }
        if (e_lo <= e_hi) {
            stack[sp++] = hi_child;
            stack[sp++] = lo_child;
        } else {
            stack[sp++] = lo_child;
            stack[sp++] = hi_child;
        }
    }
    if (unresolved > 0 && strcmp(verdict, "DECIDED") == 0) verdict = "UNRESOLVED";
    double cpu = cpu_now() - t0;
    printf("verdict %s\n", verdict);
    printf("nodes %.0f\nleaves %.0f\nstraddler_evaluations %.0f\n", nodes, leaves, strad_evals);
    printf("max_depth %d\nunresolved %d\n", maxdepth, unresolved);
    printf("min_bound %a %.17g\n", minb, minb);
    printf("min_box %a %a %a %a\n", mb_xa, mb_xb, mb_ya, mb_yb);
    printf("candidate %a %a %.17g\n", cand_x, cand_y, cand_est);
    printf("cpu_seconds %.3f\n", cpu);
    return 0;
}
