/* A214 -- the C kernel for polycore.vertex_ok (A213 notes/int_polycore.md s.6).  Plain C, no Python.h: built as a
   DLL with clang -O2 -shared and loaded with ctypes; the Python-int path of A213 (polycore_int.vertex_ok_h) stays
   the reference and the fallback.

   Two layers, both of which decide the SAME predicate the library decides:
     (1) the PHASE-2 FLOAT FILTER (A213 polycore_vec._quad_ok_f, ported operation for operation): every test is the
         sign of a low-degree polynomial in doubles that are exact (the corners, t0, t1 = k/2^24) or correctly
         rounded (the vertex); the polynomial is evaluated in binary64 with a rigorous forward error bound (the
         propagated input error plus one epsilon per rounding on the magnitude sum) and the sign is taken only where
         |value| > bound.  A pair the filter cannot decide is UNDECIDED and goes to (2).
     (2) the EXACT TEST in integers: the library's inequalities multiplied through by the positive S = 2 W CW and
         E^2 -- __int128 for the coefficients and the interior test, three-limb 192-bit (i192.h) for the endpoint
         value (< 2^142) and the discriminant (< 2^183).  Every magnitude is CHECKED against the envelope this
         kernel is proved for; anything outside returns UNDECIDED and Python's unbounded ints settle it.
   So the kernel never decides anything it cannot prove: the only results it returns are OK, BAD, or "ask Python".

   Compiled with -ffp-contract=off: no FMA contraction, one rounding per operation exactly as the bound assumes.  */
#include "i192.h"

#define fabs(x) __builtin_fabs(x)   /* no libm, no CRT headers: the kernel needs nothing else */

/* Freestanding: this machine has clang but no MSVC CRT import libraries, so the DLL is linked with -nostdlib
   -Wl,-noentry and supplies the two symbols the code generator asks for itself.  `optnone` on memset keeps clang
   from recognising the loop as a call to memset (it is only ever the short tail fill of a row of `out`). */
int _fltused = 0;

__attribute__((optnone)) void *memset(void *dst, int c, __SIZE_TYPE__ n)
{
    unsigned char *p = (unsigned char *)dst;
    while (n--) *p++ = (unsigned char)c;
    return dst;
}

#define EXPORT __declspec(dllexport)
#define EPS 1.1102230246251565e-16              /* 2^-53 */
#define OK 1
#define BAD 0
#define UNDECIDED (-1)

typedef struct {
    double bx[4], by[4], t0, t1;                /* the four corners and the tilt interval as exact doubles */
    i64 cx[4], cy[4], cw, t0i, t1i, e;          /* the same, exactly: corners over cw, tilts over e */
} a214_box;

typedef struct { i64 t0sq, t0e, t1sq, t1e, esq, tt0, tt1, e; } tprod;

/* ---------------------------------------------------------------- the envelope this kernel is proved for */
#define LIM60 ((i64)1 << 60)
#define LIM31 ((i64)1 << 31)
#define LIM93 (((u128)1) << 93)

static inline int fits93(i128 v)
{
    int n;
    u128 a = u128_abs(v, &n);
    return a < LIM93;
}

static inline int i64_small(i64 v, i64 lim) { return v > -lim && v < lim; }

EXPORT int a214_box_ok(const a214_box *b)
{
    if (b->cw <= 0 || b->cw >= LIM60 || b->e <= 0 || !i64_small(b->e, LIM31)) return 0;
    if (!i64_small(b->t0i, LIM31) || !i64_small(b->t1i, LIM31)) return 0;
    for (int k = 0; k < 4; k++)
        if (!i64_small(b->cx[k], LIM60) || !i64_small(b->cy[k], LIM60)) return 0;
    return 1;
}

static inline int vert_ok_range(i64 X, i64 Y, i64 W)
{
    return W > 0 && W < LIM60 && i64_small(X, LIM60) && i64_small(Y, LIM60);
}

static tprod tprod_of(const a214_box *b)
{
    tprod p;
    p.t0sq = b->t0i * b->t0i;
    p.t0e = b->t0i * b->e;
    p.t1sq = b->t1i * b->t1i;
    p.t1e = b->t1i * b->e;
    p.esq = b->e * b->e;
    p.tt0 = 2 * b->t0i;
    p.tt1 = 2 * b->t1i;
    p.e = b->e;
    return p;
}

/* ---------------------------------------------------------------- (1) the float filter (three-valued) */
static inline int tv_ge0(double x, double err) { return x > err ? 1 : (x < -err ? -1 : 0); }
static inline int tv_and(int a, int b) { return (a == -1 || b == -1) ? -1 : ((a == 1 && b == 1) ? 1 : 0); }
static inline int tv_or(int a, int b) { return (a == 1 || b == 1) ? 1 : ((a == -1 && b == -1) ? -1 : 0); }

static inline int quad_f(double A, double B, double C, double eA, double eB, double eC,
                         double t, double tt, double aA, double aB, double aC)
{
    double at = fabs(t);
    double S = aA * tt + aB * at + aC;
    double P = A * tt + B * t + C;
    double err = eA * tt + eB * at + eC + 5.0 * EPS * S;
    return tv_ge0(P, err);
}

/* polycore._quad_nonneg three-valued: the two endpoints, and the interior minimum when A > 0 and -B/(2A) in [t0,t1] */
static int quad_ok_f(double A, double B, double C, double eA, double eB, double eC,
                     double t0, double t1, double tt0, double tt1)
{
    double aA = fabs(A), aB = fabs(B), aC = fabs(C);
    int ok = tv_and(quad_f(A, B, C, eA, eB, eC, t0, tt0, aA, aB, aC),
                    quad_f(A, B, C, eA, eB, eC, t1, tt1, aA, aB, aC));
    int a_pos, inner;
    double A2 = 2.0 * A, eA2 = 2.0 * eA, aA2 = fabs(A2);
    double L = -B - A2 * t0;
    double eL = eB + eA2 * fabs(t0) + 3.0 * EPS * (aB + aA2 * fabs(t0));
    double R = A2 * t1 + B;
    double eR = eB + eA2 * fabs(t1) + 3.0 * EPS * (aA2 * fabs(t1) + aB);
    double D = 4.0 * (A * C) - B * B;
    double eD = 4.0 * (eA * aC + eC * aA + eA * eC) + (2.0 * aB * eB + eB * eB)
                + 4.0 * EPS * (4.0 * aA * aC + aB * aB);
    a_pos = tv_ge0(A, eA);                      /* A > 0 ?  (tv_ge0 with the same bound: > eA / < -eA) */
    inner = tv_and(a_pos, tv_and(tv_ge0(L, eL), tv_ge0(R, eR)));
    return tv_and(ok, tv_or(-inner, tv_ge0(D, eD)));
}

/* 1 = certainly certified, -1 = certainly not, 0 = the filter cannot decide */
static int filter_vertex(double vx, double vy, const a214_box *b)
{
    double t0 = b->t0, t1 = b->t1, tt0 = t0 * t0, tt1 = t1 * t1;
    double avxy = 2.0 * (fabs(vx) + fabs(vy));
    int ok = 1;
    for (int k = 0; k < 4; k++) {
        double dx = vx - b->bx[k], dy = vy - b->by[k];
        double delta = EPS * (avxy + 2.0 * (fabs(dx) + fabs(dy)));
        for (int o = 0; o < 2; o++) {
            double u = o ? dy : dx, w = o ? -dx : dy;
            double A = 0.5 + u, C = 0.5 - u, B = -2.0 * w;
            double eA = delta + EPS * fabs(A), eC = delta + EPS * fabs(C), eB = 2.0 * delta;
            ok = tv_and(ok, quad_ok_f(A, B, C, eA, eB, eC, t0, t1, tt0, tt1));
            if (ok == -1) return -1;
            ok = tv_and(ok, quad_ok_f(C, -B, A, eC, eB, eA, t0, t1, tt0, tt1));
            if (ok == -1) return -1;
        }
    }
    return ok;
}

/* ---------------------------------------------------------------- (2) the exact test (192-bit) */
/* coverage counters (diagnostics only -- the tests read them to show that the wide paths are really exercised):
   [0] quadratics decided exactly, [1] endpoint value negative, [2] interior minimum entered (the discriminant,
   the widest arithmetic in the kernel), [3] discriminant negative, [4] the envelope guard refused. */
static i64 g_cnt[5];
EXPORT void a214_counters(i64 *out) { for (int i = 0; i < 5; i++) out[i] = g_cnt[i]; }
EXPORT void a214_counters_reset(void) { for (int i = 0; i < 5; i++) g_cnt[i] = 0; }

/* A t^2 + B t + C >= 0 on [t0, t1], A B C the true coefficients times one positive scale.  1 / 0 / UNDECIDED. */
static int quad_ok_exact(i128 A, i128 B, i128 C, const tprod *p)
{
    i192 v;
    if (!fits93(A) || !fits93(B) || !fits93(C)) { g_cnt[4]++; return UNDECIDED; }
    g_cnt[0]++;
    v = i192_add(i192_add(imul_128_64(A, p->t0sq), imul_128_64(B, p->t0e)), imul_128_64(C, p->esq));
    if (i192_neg_p(v)) { g_cnt[1]++; return BAD; }
    v = i192_add(i192_add(imul_128_64(A, p->t1sq), imul_128_64(B, p->t1e)), imul_128_64(C, p->esq));
    if (i192_neg_p(v)) { g_cnt[1]++; return BAD; }
    if (A > 0) {                                /* the interior minimum: t0 2A <= -B <= t1 2A (times e) */
        i128 nb = -B * (i128)p->e;
        if ((i128)p->tt0 * A <= nb && nb <= (i128)p->tt1 * A) {
            i192 d = i192_sub(imul_128_128(4 * A, C), imul_128_128(B, B));
            g_cnt[2]++;
            if (i192_neg_p(d)) { g_cnt[3]++; return BAD; }
            return OK;
        }
    }
    return OK;
}

EXPORT int a214_vertex_ok_exact(i64 X, i64 Y, i64 W, const a214_box *b)
{
    tprod p;
    i128 CW, S2, XW, YW;
    if (!vert_ok_range(X, Y, W) || !a214_box_ok(b)) return UNDECIDED;
    p = tprod_of(b);
    CW = (i128)b->cw;
    S2 = (i128)W * CW;
    XW = (i128)X * CW;
    YW = (i128)Y * CW;
    for (int k = 0; k < 4; k++) {
        i128 UX = XW - (i128)b->cx[k] * (i128)W;
        i128 UY = YW - (i128)b->cy[k] * (i128)W;
        for (int o = 0; o < 2; o++) {
            i128 U = o ? UY : UX, V = o ? -UX : UY;
            i128 P, M, B4;
            int r;
            P = S2 + 2 * U;
            M = S2 - 2 * U;
            B4 = 4 * V;
            r = quad_ok_exact(P, -B4, M, &p);
            if (r != OK) return r;
            r = quad_ok_exact(M, B4, P, &p);
            if (r != OK) return r;
        }
    }
    return OK;
}

/* ---------------------------------------------------------------- the entry points */
EXPORT int a214_vertex_filter(double vx, double vy, const a214_box *b)
{
    return filter_vertex(vx, vy, b);            /* 1 ok, -1 bad, 0 undecided (the filter alone, for the tests) */
}

/* the full kernel for one (vertex, box): the filter, then the exact test.  1 = OK, 0 = BAD, -1 = ask Python. */
EXPORT int a214_vertex_ok(double vx, double vy, i64 X, i64 Y, i64 W, const a214_box *b)
{
    int f = filter_vertex(vx, vy, b);
    if (f == 1) return OK;
    if (f == -1) return BAD;
    return a214_vertex_ok_exact(X, Y, W, b);
}

/* the batch: nv vertices x nb boxes.  out[i*nb + j] = 0 OK, 1 BAD, 2 ask Python, 3 not evaluated (a BAD box
   earlier in the row settled the vertex).  Returns the number of pairs handed back to Python. */
EXPORT i64 a214_cert_batch(int nv, int nb, const double *vx, const double *vy,
                           const i64 *VX, const i64 *VY, const i64 *VW,
                           const a214_box *boxes, unsigned char *out, i64 *stats)
{
    i64 pairs = 0, undec = 0, exact = 0, punt = 0;
    for (int i = 0; i < nv; i++) {
        double x = vx[i], y = vy[i];
        int i0 = i * nb, j;
        for (j = 0; j < nb; j++) {
            const a214_box *b = boxes + j;
            int f;
            pairs++;
            f = filter_vertex(x, y, b);
            if (f == 1) { out[i0 + j] = 0; continue; }
            if (f == -1) { out[i0 + j] = 1; j++; break; }
            undec++;
            f = a214_vertex_ok_exact(VX[i], VY[i], VW[i], b);
            if (f == UNDECIDED) { out[i0 + j] = 2; punt++; j++; break; }
            exact++;
            out[i0 + j] = (unsigned char)(f == OK ? 0 : 1);
            if (f != OK) { j++; break; }
        }
        for (; j < nb; j++) out[i0 + j] = 3;
    }
    if (stats) { stats[0] += pairs; stats[1] += undec; stats[2] += exact; stats[3] += punt; }
    return punt;
}

EXPORT int a214_self_test(void)
{
    /* i192: (2^90 + 1) * (2^90 + 1) - (2^90)^2 - 2 * 2^90 == 1, and the sign of a 189-bit difference. */
    i128 a = ((i128)1 << 90) + 1;
    i192 p = imul_128_128(a, a);
    i192 q = imul_128_128((i128)1 << 90, (i128)1 << 90);
    i192 r = i192_sub(i192_sub(p, q), imul_128_64((i128)1 << 91, 1));
    if (r.l[0] != 1 || r.l[1] || r.l[2]) return 1;
    if (!i192_neg_p(i192_sub(q, p))) return 2;
    if (i192_neg_p(i192_sub(p, q))) return 3;
    if (!i192_neg_p(imul_128_64(-((i128)1 << 100), 12345))) return 4;
    if (i192_neg_p(imul_128_64(-((i128)1 << 100), -12345))) return 5;
    return 0;
}

EXPORT int a214_sizeof_box(void) { return (int)sizeof(a214_box); }
EXPORT int a214_version(void) { return 1; }
