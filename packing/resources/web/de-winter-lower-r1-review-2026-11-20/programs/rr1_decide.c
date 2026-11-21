/* rr1_decide.c -- lane rR1-lower's clean-room coverage decider (C core).
 *
 * Written for the blind stage 4 review R1 of jlevy/squares issues 1041 and 1042 from
 * the mathematics in frozen/review-plan.md, without reading any program of the source.
 *
 * Every accepted bound is computed in exact integer arithmetic (int64 / __int128).
 * Floating point is used only to nominate the dual test point z (any z gives a valid
 * bound) and in the non-deciding float modes `fsearch` and `fcap`.
 *
 * Units.  Lengths are integers on a lattice of Q points per unit (Q is chosen by the
 * driver; it never enters this program).  The driver gives every rectangle k an integer
 * d_k = floor(rho_k * 2^G / (2 Q^2)), rho_k its exact density, so that for a lattice
 * polygon of doubled area A2 (integer) inside the rectangle the mass is at least
 * floor(d_k * A2 / 2^(G - 64)) units of 2^-64.  The threshold T is in the same units.
 *
 * Modes:
 *   decide RECTS BINS        one JSON line per bin: ACCEPT, or FAIL with the failing box
 *   pcap   RECTS POLY PTS    integer lower bound of mu(c + P) at lattice points c
 *   boxb   RECTS POLY BOXES  the node bound of each box (for the self-test)
 *   clip   RECTS POLY PTS    doubled hull area of R_k cap (c + P) for every k (self-test)
 *   fsearch RECTS SEARCH     float search for low captures of true unit squares
 *   fcap   RECTS POSES       float capture of true unit squares (cx cy t)
 */
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef __int128 i128;
typedef long long i64;

static void die(const char *m) {
  fprintf(stderr, "rr1_decide: %s\n", m);
  exit(2);
}

/* ---------- int128 helpers ---------- */
static i128 parse_i128(const char *s) {
  int neg = 0;
  i128 v = 0;
  if (*s == '-') { neg = 1; s++; }
  if (!*s) die("empty integer");
  for (; *s; s++) {
    if (*s < '0' || *s > '9') die("bad integer");
    v = v * 10 + (*s - '0');
  }
  return neg ? -v : v;
}
static void fmt_i128(i128 v, char *buf) {
  char t[64];
  int n = 0, neg = v < 0;
  unsigned __int128 u = neg ? (unsigned __int128)(-(v + 1)) + 1 : (unsigned __int128)v;
  do { t[n++] = (char)('0' + (int)(u % 10)); u /= 10; } while (u);
  int p = 0;
  if (neg) buf[p++] = '-';
  while (n) buf[p++] = t[--n];
  buf[p] = 0;
}
/* floor(a / b) and ceil(a / b) for b > 0 */
static i128 floordiv(i128 a, i128 b) {
  i128 q = a / b;
  if ((a % b != 0) && (a < 0)) q -= 1;
  return q;
}
static i128 ceildiv(i128 a, i128 b) { return -floordiv(-a, b); }
/* floor(sqrt(m)) for 0 <= m < 2^120 */
static i64 isqrt128(i128 m) {
  if (m <= 0) return 0;
  i64 s = (i64)sqrtl((long double)m);
  while (s > 0 && (i128)s * s > m) s--;
  while ((i128)(s + 1) * (s + 1) <= m) s++;
  return s;
}

/* ---------- data ---------- */
static int NR;
static i64 *RX0, *RY0, *RX1, *RY1, *RD;
static double *RRHO;
static int GSHIFT; /* G - 64 */

static int PM;
static i64 PX[64], PY[64];
static i64 PMINX, PMAXX, PMINY, PMAXY;

static FILE *xopen(const char *p) {
  FILE *f = fopen(p, "r");
  if (!f) die("cannot open input");
  return f;
}
static void read_rects(const char *path) {
  FILE *f = xopen(path);
  char tag[16], b0[64], b1[64], b2[64], b3[64], b4[64], b5[64];
  int g;
  if (fscanf(f, "%15s %d", tag, &g) != 2 || strcmp(tag, "G") != 0) die("rects header G");
  if (g < 64 || g > 126) die("G out of range");
  GSHIFT = g - 64;
  if (fscanf(f, "%15s %d", tag, &NR) != 2 || strcmp(tag, "N") != 0) die("rects header N");
  RX0 = malloc(sizeof(i64) * NR); RY0 = malloc(sizeof(i64) * NR);
  RX1 = malloc(sizeof(i64) * NR); RY1 = malloc(sizeof(i64) * NR);
  RD = malloc(sizeof(i64) * NR); RRHO = malloc(sizeof(double) * NR);
  for (int k = 0; k < NR; k++) {
    if (fscanf(f, "%63s %63s %63s %63s %63s %63s", b0, b1, b2, b3, b4, b5) != 6) die("rect line");
    RX0[k] = (i64)parse_i128(b0); RY0[k] = (i64)parse_i128(b1);
    RX1[k] = (i64)parse_i128(b2); RY1[k] = (i64)parse_i128(b3);
    RD[k] = (i64)parse_i128(b4); RRHO[k] = atof(b5);
    if (!(RX0[k] < RX1[k] && RY0[k] < RY1[k]) || RD[k] < 0) die("bad rectangle");
    if (llabs(RX0[k]) > (1LL << 42) || llabs(RX1[k]) > (1LL << 42) || llabs(RY0[k]) > (1LL << 42) ||
        llabs(RY1[k]) > (1LL << 42)) die("coordinate too large");
  }
  fclose(f);
}
static void set_poly(int m, const i64 *xs, const i64 *ys) {
  if (m < 3 || m > 64) die("polygon size");
  PM = m;
  PMINX = PMAXX = xs[0]; PMINY = PMAXY = ys[0];
  for (int i = 0; i < m; i++) {
    PX[i] = xs[i]; PY[i] = ys[i];
    if (llabs(xs[i]) > (1LL << 39) || llabs(ys[i]) > (1LL << 39)) die("polygon too large");
    if (xs[i] < PMINX) PMINX = xs[i];
    if (xs[i] > PMAXX) PMAXX = xs[i];
    if (ys[i] < PMINY) PMINY = ys[i];
    if (ys[i] > PMAXY) PMAXY = ys[i];
  }
  /* strictly convex and counterclockwise */
  for (int i = 0; i < m; i++) {
    int j = (i + 1) % m, l = (i + 2) % m;
    i128 c = (i128)(PX[j] - PX[i]) * (PY[l] - PY[j]) - (i128)(PY[j] - PY[i]) * (PX[l] - PX[j]);
    if (c <= 0) die("polygon not strictly convex ccw");
  }
}

/* (x, y) relative to the polygon's centre, closed containment */
static int in_poly(i64 x, i64 y) {
  for (int i = 0; i < PM; i++) {
    int j = (i + 1 == PM) ? 0 : i + 1;
    i128 c = (i128)(PX[j] - PX[i]) * (y - PY[i]) - (i128)(PY[j] - PY[i]) * (x - PX[i]);
    if (c < 0) return 0;
  }
  return 1;
}

/* ---------- the clip: lattice hull of R_k cap (c + P) ---------- */
static i64 CLIPS;
typedef struct { i64 x, y; } pt;
static int ptcmp(const void *a, const void *b) {
  const pt *p = a, *q = b;
  if (p->x != q->x) return p->x < q->x ? -1 : 1;
  if (p->y != q->y) return p->y < q->y ? -1 : 1;
  return 0;
}
static i128 cross3(pt o, pt a, pt b) {
  return (i128)(a.x - o.x) * (b.y - o.y) - (i128)(a.y - o.y) * (b.x - o.x);
}
/* Returns the doubled area of the convex hull of lattice points verified to lie in the
 * closed rectangle and the closed polygon c + P, so at most twice the area of the
 * intersection.  *full is set when all four rectangle corners lie in c + P. */
static i128 clip_area2(int k, i64 cx, i64 cy, int *full) {
  CLIPS++;
  i64 x0 = RX0[k] - cx, x1 = RX1[k] - cx, y0 = RY0[k] - cy, y1 = RY1[k] - cy;
  *full = 0;
  if (x1 < PMINX || x0 > PMAXX || y1 < PMINY || y0 > PMAXY) return 0;
  int c00 = in_poly(x0, y0), c10 = in_poly(x1, y0), c01 = in_poly(x0, y1), c11 = in_poly(x1, y1);
  if (c00 && c10 && c01 && c11) {
    *full = 1;
    return (i128)2 * (x1 - x0) * (y1 - y0);
  }
  pt cand[400];
  int nc = 0;
  if (c00) cand[nc++] = (pt){x0, y0};
  if (c10) cand[nc++] = (pt){x1, y0};
  if (c01) cand[nc++] = (pt){x0, y1};
  if (c11) cand[nc++] = (pt){x1, y1};
  for (int i = 0; i < PM; i++) {
    i64 ax = PX[i], ay = PY[i];
    if (ax >= x0 && ax <= x1 && ay >= y0 && ay <= y1) cand[nc++] = (pt){ax, ay};
  }
  for (int i = 0; i < PM; i++) {
    int j = (i + 1 == PM) ? 0 : i + 1;
    i64 ax = PX[i], ay = PY[i], bx = PX[j], by = PY[j];
    i64 dx = bx - ax, dy = by - ay;
    i64 lo, hi;
    if (dx != 0) {
      lo = ax < bx ? ax : bx; hi = ax < bx ? bx : ax;
      i64 xs[2] = {x0, x1};
      for (int s = 0; s < 2; s++) {
        i64 X = xs[s];
        if (X <= lo || X >= hi) continue;
        i128 num = (i128)dy * (X - ax), den = dx;
        if (den < 0) { num = -num; den = -den; }
        /* interior of the ccw polygon is to the left: d/dy of the edge test is dx */
        i128 q = (dx > 0) ? ceildiv(num, den) : floordiv(num, den);
        i64 Y = ay + (i64)q;
        if (Y >= y0 && Y <= y1) cand[nc++] = (pt){X, Y};
      }
    }
    if (dy != 0) {
      lo = ay < by ? ay : by; hi = ay < by ? by : ay;
      i64 ys[2] = {y0, y1};
      for (int s = 0; s < 2; s++) {
        i64 Y = ys[s];
        if (Y <= lo || Y >= hi) continue;
        i128 num = (i128)dx * (Y - ay), den = dy;
        if (den < 0) { num = -num; den = -den; }
        /* d/dx of the edge test is -dy */
        i128 q = (dy < 0) ? ceildiv(num, den) : floordiv(num, den);
        i64 X = ax + (i64)q;
        if (X >= x0 && X <= x1) cand[nc++] = (pt){X, Y};
      }
    }
  }
  /* verify every candidate exactly; keep the accepted ones */
  pt acc[400];
  int na = 0;
  for (int i = 0; i < nc; i++) {
    pt p = cand[i];
    if (p.x < x0 || p.x > x1 || p.y < y0 || p.y > y1) continue;
    if (!in_poly(p.x, p.y)) continue;
    acc[na++] = p;
  }
  if (na < 3) return 0;
  qsort(acc, (size_t)na, sizeof(pt), ptcmp);
  pt h[802];
  int m = 0;
  for (int i = 0; i < na; i++) {
    while (m >= 2 && cross3(h[m - 2], h[m - 1], acc[i]) <= 0) m--;
    h[m++] = acc[i];
  }
  for (int i = na - 2, t = m + 1; i >= 0; i--) {
    while (m >= t && cross3(h[m - 2], h[m - 1], acc[i]) <= 0) m--;
    h[m++] = acc[i];
  }
  m--; /* last equals first */
  if (m < 3) return 0;
  i128 a2 = 0;
  for (int i = 0; i < m; i++) {
    int j = (i + 1 == m) ? 0 : i + 1;
    a2 += (i128)h[i].x * h[j].y - (i128)h[j].x * h[i].y;
  }
  if (a2 < 0) die("negative hull area");
  return a2;
}
static i128 mass_units(int k, i128 a2) { return ((i128)RD[k] * a2) >> GSHIFT; }

/* ---------- the node bound ---------- */
typedef struct {
  i128 full;     /* mass of rectangles inside c_j + P at all four corners */
  i128 bm;       /* the dual bound of the Brunn-Minkowski term, >= 0 */
  i128 corner[4];/* lower bounds of mu(c_j + P) */
} nodeval;

/* lower bound of min over the simplex of l^T H l, by the dual test point */
static i128 dual_bound(i128 H[4][4]) {
  const i64 Z = 1 << 16;
  double h[4][4], sc = 0;
  for (int i = 0; i < 4; i++)
    for (int j = 0; j < 4; j++) {
      h[i][j] = (double)H[i][j];
      if (fabs(h[i][j]) > sc) sc = fabs(h[i][j]);
    }
  if (sc == 0) return 0;
  for (int i = 0; i < 4; i++)
    for (int j = 0; j < 4; j++) h[i][j] /= sc;
  double bestv = 1e300, bestl[4] = {0.25, 0.25, 0.25, 0.25};
  for (int S = 1; S < 16; S++) {
    int idx[4], n = 0;
    for (int i = 0; i < 4; i++)
      if (S >> i & 1) idx[n++] = i;
    double a[4][5];
    for (int r = 0; r < n; r++) {
      for (int c = 0; c < n; c++) a[r][c] = h[idx[r]][idx[c]];
      a[r][n] = 1.0;
    }
    int ok = 1;
    for (int c = 0; c < n && ok; c++) {
      int p = c;
      for (int r = c + 1; r < n; r++)
        if (fabs(a[r][c]) > fabs(a[p][c])) p = r;
      if (fabs(a[p][c]) < 1e-14) { ok = 0; break; }
      for (int cc = 0; cc <= n; cc++) { double t = a[c][cc]; a[c][cc] = a[p][cc]; a[p][cc] = t; }
      for (int r = 0; r < n; r++)
        if (r != c) {
          double f = a[r][c] / a[c][c];
          for (int cc = c; cc <= n; cc++) a[r][cc] -= f * a[c][cc];
        }
    }
    if (!ok) continue;
    double x[4] = {0, 0, 0, 0}, sx = 0;
    for (int r = 0; r < n; r++) {
      x[idx[r]] = a[r][n] / a[r][r];
      if (!(x[idx[r]] > 0)) ok = 0;
      sx += x[idx[r]];
    }
    if (!ok || !(sx > 0)) continue;
    double v = 1.0 / sx;
    if (v < bestv) {
      bestv = v;
      for (int i = 0; i < 4; i++) bestl[i] = x[i] / sx;
    }
  }
  /* candidates: the nominated point and the four vertices */
  i128 best = 0;
  for (int cnd = 0; cnd < 5; cnd++) {
    i64 z[4] = {0, 0, 0, 0};
    if (cnd < 4) {
      z[cnd] = Z;
    } else {
      i64 s = 0;
      double fr[4];
      for (int i = 0; i < 4; i++) {
        double v = bestl[i] < 0 ? 0 : bestl[i] * (double)Z;
        z[i] = (i64)floor(v);
        if (z[i] < 0) z[i] = 0;
        fr[i] = v - (double)z[i];
        s += z[i];
      }
      while (s < Z) {
        int bi = 0;
        for (int i = 1; i < 4; i++)
          if (fr[i] > fr[bi]) bi = i;
        z[bi]++; fr[bi] = -1; s++;
      }
      while (s > Z) {
        int bi = -1;
        for (int i = 0; i < 4; i++)
          if (z[i] > 0 && (bi < 0 || z[i] > z[bi])) bi = i;
        z[bi]--; s--;
      }
    }
    i128 hz[4], zhz = 0, mn = 0;
    for (int i = 0; i < 4; i++) {
      hz[i] = 0;
      for (int j = 0; j < 4; j++) hz[i] += H[i][j] * z[j];
      zhz += (i128)z[i] * hz[i];
      if (i == 0 || hz[i] < mn) mn = hz[i];
    }
    i128 num = (i128)2 * Z * mn - zhz;
    i128 b = floordiv(num, (i128)Z * Z);
    if (b > best) best = b;
  }
  return best;
}

typedef struct { int *a; int n, cap; } ilist;
static void il_push(ilist *l, int v) {
  if (l->n == l->cap) {
    l->cap = l->cap ? 2 * l->cap : 256;
    l->a = realloc(l->a, sizeof(int) * (size_t)l->cap);
    if (!l->a) die("out of memory");
  }
  l->a[l->n++] = v;
}

/* Evaluate a box: corners (xa,ya),(xb,ya),(xa,yb),(xb,yb).  Rectangles of `in` that
 * are inside c_j + P at all corners are added to *fullsum and not passed on; the rest
 * that can meet some c + P with c in the box go to `out`. */
static nodeval eval_box(i64 xa, i64 xb, i64 ya, i64 yb, const ilist *in, ilist *out, i128 *fullsum,
                        int keep_zero_corners) {
  nodeval nv;
  i128 H[4][4];
  memset(H, 0, sizeof H);
  i64 cx[4] = {xa, xb, xa, xb}, cy[4] = {ya, ya, yb, yb};
  i128 inherited = *fullsum;
  for (int j = 0; j < 4; j++) nv.corner[j] = 0;
  i64 ux0 = xa + PMINX, ux1 = xb + PMAXX, uy0 = ya + PMINY, uy1 = yb + PMAXY;
  for (int t = 0; t < in->n; t++) {
    int k = in->a[t];
    if (RX1[k] < ux0 || RX0[k] > ux1 || RY1[k] < uy0 || RY0[k] > uy1) continue;
    i128 m[4];
    int fl[4], allfull = 1, allpos = 1;
    for (int j = 0; j < 4; j++) {
      i128 a2 = clip_area2(k, cx[j], cy[j], &fl[j]);
      m[j] = mass_units(k, a2);
      if (!fl[j]) allfull = 0;
      if (m[j] < 1) allpos = 0;
    }
    for (int j = 0; j < 4; j++) nv.corner[j] += m[j];
    if (allfull) {
      *fullsum += m[0]; /* the same full area at every corner */
      continue;
    }
    if (out) il_push(out, k);
    if (allpos || keep_zero_corners) {
      i64 s[4];
      for (int j = 0; j < 4; j++) s[j] = isqrt128(m[j]);
      for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++) H[i][j] += (i128)s[i] * s[j];
    }
  }
  nv.full = *fullsum;
  nv.bm = dual_bound(H);
  for (int j = 0; j < 4; j++) nv.corner[j] += inherited; /* the loop added every listed rectangle */
  return nv;
}

/* ---------- decide one bin ---------- */
typedef struct {
  i64 xa, xb, ya, yb;
  i128 full;
  ilist l;
  int depth;
} frame;

static int MUTANT_KEEPZERO = 0;

static void decide_bin(const char *id, i64 X0, i64 X1, i64 Y0, i64 Y1, i128 T, i64 nmax, i64 minw) {
  clock_t t0 = clock();
  i64 nodes = 0, leaves = 0;
  int maxdepth = 0;
  CLIPS = 0;
  i128 minacc = -1;
  frame *st = malloc(sizeof(frame) * 256);
  int sp = 0;
  st[0].xa = X0; st[0].xb = X1; st[0].ya = Y0; st[0].yb = Y1; st[0].full = 0; st[0].depth = 0;
  st[0].l.a = NULL; st[0].l.n = 0; st[0].l.cap = 0;
  for (int k = 0; k < NR; k++) il_push(&st[0].l, k);
  sp = 1;
  const char *verdict = "ACCEPT";
  i64 fb[4] = {0, 0, 0, 0};
  char fc[4][64];
  for (int j = 0; j < 4; j++) strcpy(fc[j], "0");
  char fbound[64] = "0";
  while (sp > 0) {
    frame f = st[--sp];
    nodes++;
    if (f.depth > maxdepth) maxdepth = f.depth;
    ilist out = {NULL, 0, 0};
    i128 full = f.full;
    nodeval nv = eval_box(f.xa, f.xb, f.ya, f.yb, &f.l, &out, &full, MUTANT_KEEPZERO);
    free(f.l.a);
    i128 bound = full + nv.bm;
    if (bound >= T) {
      leaves++;
      if (minacc < 0 || bound < minacc) minacc = bound;
      free(out.a);
      continue;
    }
    i64 wx = f.xb - f.xa, wy = f.yb - f.ya;
    if ((wx <= minw && wy <= minw) || nodes >= nmax || sp >= 250) {
      verdict = "FAIL";
      fb[0] = f.xa; fb[1] = f.xb; fb[2] = f.ya; fb[3] = f.yb;
      for (int j = 0; j < 4; j++) fmt_i128(nv.corner[j], fc[j]);
      fmt_i128(bound, fbound);
      free(out.a);
      while (sp > 0) free(st[--sp].l.a);
      break;
    }
    frame a = f, b = f;
    a.full = full; b.full = full;
    a.depth = b.depth = f.depth + 1;
    if (wx >= wy) {
      i64 mid = f.xa + wx / 2;
      a.xb = mid; b.xa = mid;
    } else {
      i64 mid = f.ya + wy / 2;
      a.yb = mid; b.ya = mid;
    }
    b.l.a = malloc(sizeof(int) * (size_t)(out.n > 0 ? out.n : 1));
    memcpy(b.l.a, out.a, sizeof(int) * (size_t)out.n);
    b.l.n = out.n; b.l.cap = out.n > 0 ? out.n : 1;
    a.l = out;
    st[sp++] = b;
    st[sp++] = a;
  }
  free(st);
  double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
  char ma[64];
  fmt_i128(minacc, ma);
  printf("{\"id\":\"%s\",\"verdict\":\"%s\",\"nodes\":%lld,\"leaves\":%lld,\"clips\":%lld,\"depth\":%d,"
         "\"min_accepted\":\"%s\",\"seconds\":%.3f",
         id, verdict, nodes, leaves, CLIPS, maxdepth, ma, secs);
  if (strcmp(verdict, "FAIL") == 0)
    printf(",\"fail_box\":[%lld,%lld,%lld,%lld],\"fail_bound\":\"%s\",\"fail_corners\":[\"%s\",\"%s\",\"%s\",\"%s\"]",
           fb[0], fb[1], fb[2], fb[3], fbound, fc[0], fc[1], fc[2], fc[3]);
  printf("}\n");
  fflush(stdout);
}

static void read_poly(FILE *f) {
  int m;
  if (fscanf(f, "%d", &m) != 1) die("poly size");
  if (m < 3 || m > 64) die("poly size range");
  i64 xs[64], ys[64];
  char b0[64], b1[64];
  for (int i = 0; i < m; i++) {
    if (fscanf(f, "%63s %63s", b0, b1) != 2) die("poly vertex");
    xs[i] = (i64)parse_i128(b0); ys[i] = (i64)parse_i128(b1);
  }
  set_poly(m, xs, ys);
}

/* ---------- float modes (non-deciding) ---------- */
static double *FX0, *FY0, *FX1, *FY1;
static double fclip_square(int k, double cx, double cy, double c, double s) {
  /* Sutherland-Hodgman of the square against the rectangle, in double */
  double px[16], py[16], qx[16], qy[16];
  int n = 4;
  double hx = 0.5 * c, hy = 0.5 * s; /* half of e */
  double gx = -0.5 * s, gy = 0.5 * c; /* half of e-perp */
  px[0] = cx + hx + gx; py[0] = cy + hy + gy;
  px[1] = cx - hx + gx; py[1] = cy - hy + gy;
  px[2] = cx - hx - gx; py[2] = cy - hy - gy;
  px[3] = cx + hx - gx; py[3] = cy + hy - gy;
  double lim[4];
  lim[0] = FX0[k]; lim[1] = FX1[k]; lim[2] = FY0[k]; lim[3] = FY1[k];
  for (int e = 0; e < 4; e++) {
    int m = 0;
    for (int i = 0; i < n; i++) {
      int j = (i + 1) % n;
      double vi, vj;
      if (e == 0) { vi = px[i] - lim[0]; vj = px[j] - lim[0]; }
      else if (e == 1) { vi = lim[1] - px[i]; vj = lim[1] - px[j]; }
      else if (e == 2) { vi = py[i] - lim[2]; vj = py[j] - lim[2]; }
      else { vi = lim[3] - py[i]; vj = lim[3] - py[j]; }
      if (vi >= 0) { qx[m] = px[i]; qy[m] = py[i]; m++; }
      if ((vi >= 0) != (vj >= 0)) {
        double tt = vi / (vi - vj);
        qx[m] = px[i] + tt * (px[j] - px[i]);
        qy[m] = py[i] + tt * (py[j] - py[i]);
        m++;
      }
    }
    n = m;
    for (int i = 0; i < n; i++) { px[i] = qx[i]; py[i] = qy[i]; }
    if (n < 3) return 0;
  }
  double a = 0;
  for (int i = 0; i < n; i++) {
    int j = (i + 1) % n;
    a += px[i] * py[j] - px[j] * py[i];
  }
  return 0.5 * fabs(a);
}
static double FQ;
/* grid of rectangles for the float modes */
static int GN;
static double GLO, GSZ;
static ilist *GCELL;
static void float_setup(double q) {
  FQ = q;
  FX0 = malloc(sizeof(double) * NR); FX1 = malloc(sizeof(double) * NR);
  FY0 = malloc(sizeof(double) * NR); FY1 = malloc(sizeof(double) * NR);
  double hi = 0;
  for (int k = 0; k < NR; k++) {
    FX0[k] = RX0[k] / q; FX1[k] = RX1[k] / q; FY0[k] = RY0[k] / q; FY1[k] = RY1[k] / q;
    if (FX1[k] > hi) hi = FX1[k];
    if (FY1[k] > hi) hi = FY1[k];
  }
  GLO = 0; GN = 64; GSZ = (hi + 1e-9) / GN;
  GCELL = calloc((size_t)GN * GN, sizeof(ilist));
  for (int k = 0; k < NR; k++) {
    int i0 = (int)(FX0[k] / GSZ), i1 = (int)(FX1[k] / GSZ), j0 = (int)(FY0[k] / GSZ), j1 = (int)(FY1[k] / GSZ);
    if (i1 >= GN) i1 = GN - 1;
    if (j1 >= GN) j1 = GN - 1;
    for (int i = i0; i <= i1; i++)
      for (int j = j0; j <= j1; j++) il_push(&GCELL[i * GN + j], k);
  }
}
static unsigned *SEEN;
static unsigned STAMP;
static double fcap(double cx, double cy, double t) {
  double c = (1 - t * t) / (1 + t * t), s = 2 * t / (1 + t * t);
  double r = 0.5 * (fabs(c) + fabs(s));
  int i0 = (int)((cx - r) / GSZ), i1 = (int)((cx + r) / GSZ), j0 = (int)((cy - r) / GSZ), j1 = (int)((cy + r) / GSZ);
  if (i0 < 0) i0 = 0;
  if (j0 < 0) j0 = 0;
  if (i1 >= GN) i1 = GN - 1;
  if (j1 >= GN) j1 = GN - 1;
  if (!SEEN) SEEN = calloc((size_t)NR, sizeof(unsigned));
  STAMP++;
  double tot = 0;
  for (int i = i0; i <= i1; i++)
    for (int j = j0; j <= j1; j++) {
      ilist *L = &GCELL[i * GN + j];
      for (int u = 0; u < L->n; u++) {
        int k = L->a[u];
        if (SEEN[k] == STAMP) continue;
        SEEN[k] = STAMP;
        if (FX1[k] < cx - r || FX0[k] > cx + r || FY1[k] < cy - r || FY0[k] > cy + r) continue;
        tot += RRHO[k] * fclip_square(k, cx, cy, c, s);
      }
    }
  return tot;
}

int main(int argc, char **argv) {
  if (argc < 3) die("usage: rr1_decide MODE RECTS ...");
  const char *mode = argv[1];
  read_rects(argv[2]);
  if (strcmp(mode, "decide") == 0) {
    if (argc < 4) die("decide RECTS BINS");
    if (getenv("RR1_MUTANT_KEEPZERO")) MUTANT_KEEPZERO = 1;
    FILE *f = xopen(argv[3]);
    int nb;
    char tag[16];
    if (fscanf(f, "%15s %d", tag, &nb) != 2 || strcmp(tag, "BINS") != 0) die("bins header");
    for (int b = 0; b < nb; b++) {
      char id[128], s0[64], s1[64], s2[64], s3[64], st[64], sn[64], sw[64];
      if (fscanf(f, "%127s %63s %63s %63s %63s %63s %63s %63s", id, s0, s1, s2, s3, st, sn, sw) != 8) die("bin line");
      read_poly(f);
      decide_bin(id, (i64)parse_i128(s0), (i64)parse_i128(s1), (i64)parse_i128(s2), (i64)parse_i128(s3),
                 parse_i128(st), (i64)parse_i128(sn), (i64)parse_i128(sw));
    }
    fclose(f);
  } else if (strcmp(mode, "pcap") == 0 || strcmp(mode, "clip") == 0) {
    FILE *f = xopen(argv[3]);
    read_poly(f);
    fclose(f);
    FILE *g = xopen(argv[4]);
    char b0[64], b1[64];
    while (fscanf(g, "%63s %63s", b0, b1) == 2) {
      i64 cx = (i64)parse_i128(b0), cy = (i64)parse_i128(b1);
      if (strcmp(mode, "pcap") == 0) {
        i128 tot = 0;
        for (int k = 0; k < NR; k++) {
          int fl;
          tot += mass_units(k, clip_area2(k, cx, cy, &fl));
        }
        char buf[64];
        fmt_i128(tot, buf);
        printf("%s\n", buf);
      } else {
        for (int k = 0; k < NR; k++) {
          int fl;
          char buf[64];
          fmt_i128(clip_area2(k, cx, cy, &fl), buf);
          printf("%s%s", k ? " " : "", buf);
        }
        printf("\n");
      }
    }
    fclose(g);
  } else if (strcmp(mode, "boxb") == 0) {
    if (getenv("RR1_MUTANT_KEEPZERO")) MUTANT_KEEPZERO = 1;
    FILE *f = xopen(argv[3]);
    read_poly(f);
    fclose(f);
    FILE *g = xopen(argv[4]);
    char b0[64], b1[64], b2[64], b3[64];
    ilist all = {NULL, 0, 0};
    for (int k = 0; k < NR; k++) il_push(&all, k);
    while (fscanf(g, "%63s %63s %63s %63s", b0, b1, b2, b3) == 4) {
      i128 full = 0;
      nodeval nv = eval_box((i64)parse_i128(b0), (i64)parse_i128(b1), (i64)parse_i128(b2), (i64)parse_i128(b3), &all,
                            NULL, &full, MUTANT_KEEPZERO);
      char buf[64];
      fmt_i128(full + nv.bm, buf);
      printf("%s\n", buf);
    }
    fclose(g);
  } else if (strcmp(mode, "fcap") == 0 || strcmp(mode, "fsearch") == 0) {
    FILE *g = xopen(argv[3]);
    double q;
    if (fscanf(g, "%lf", &q) != 1) die("float Q");
    float_setup(q);
    if (strcmp(mode, "fcap") == 0) {
      double cx, cy, t;
      while (fscanf(g, "%lf %lf %lf", &cx, &cy, &t) == 3) printf("%.17g\n", fcap(cx, cy, t));
    } else {
      /* fsearch: L, then lines "t" (angles); grid G per side; keep K best; refine */
      double L;
      int gsz, kbest, na;
      if (fscanf(g, "%lf %d %d %d", &L, &gsz, &kbest, &na) != 4) die("fsearch header");
      double *ts = malloc(sizeof(double) * (size_t)na);
      for (int a = 0; a < na; a++)
        if (fscanf(g, "%lf", &ts[a]) != 1) die("fsearch angle");
      int tot = na * gsz * gsz;
      double *vx = malloc(sizeof(double) * (size_t)tot), *vy = malloc(sizeof(double) * (size_t)tot),
             *vt = malloc(sizeof(double) * (size_t)tot), *vv = malloc(sizeof(double) * (size_t)tot);
      int n = 0;
      for (int a = 0; a < na; a++) {
        double t = ts[a], c = (1 - t * t) / (1 + t * t), s = 2 * t / (1 + t * t);
        double w = 0.5 * (c + s), lo = L / 2, hi = L - w;
        for (int i = 0; i < gsz; i++)
          for (int j = 0; j < gsz; j++) {
            double x = lo + (hi - lo) * i / (gsz - 1), y = lo + (hi - lo) * j / (gsz - 1);
            vx[n] = x; vy[n] = y; vt[n] = t; vv[n] = fcap(x, y, t); n++;
          }
      }
      /* pick kbest distinct lowest (simple selection) */
      for (int r = 0; r < kbest && r < n; r++) {
        int bi = r;
        for (int i = r + 1; i < n; i++)
          if (vv[i] < vv[bi]) bi = i;
        double tx = vx[r], ty = vy[r], tt = vt[r], tv = vv[r];
        vx[r] = vx[bi]; vy[r] = vy[bi]; vt[r] = vt[bi]; vv[r] = vv[bi];
        vx[bi] = tx; vy[bi] = ty; vt[bi] = tt; vv[bi] = tv;
      }
      for (int r = 0; r < kbest && r < n; r++) {
        double x = vx[r], y = vy[r], t = vt[r], v = vv[r];
        double hs = (L / 2) / gsz, ht = 0.01;
        while (hs > 1e-9) {
          int moved = 0;
          double cand[6][3] = {{x + hs, y, t}, {x - hs, y, t}, {x, y + hs, t}, {x, y - hs, t}, {x, y, t + ht}, {x, y, t - ht}};
          for (int c = 0; c < 6; c++) {
            double cx = cand[c][0], cy = cand[c][1], ct = cand[c][2];
            if (ct < 0 || ct > 0.41421356) continue;
            double cc = (1 - ct * ct) / (1 + ct * ct), ss = 2 * ct / (1 + ct * ct), w = 0.5 * (cc + ss);
            if (cx < w || cx > L - w || cy < w || cy > L - w) continue;
            double cv = fcap(cx, cy, ct);
            if (cv < v) { x = cx; y = cy; t = ct; v = cv; moved = 1; break; }
          }
          if (!moved) { hs /= 2; ht /= 2; }
        }
        printf("%.17g %.17g %.17g %.17g\n", x, y, t, v);
      }
    }
    fclose(g);
  } else {
    die("unknown mode");
  }
  return 0;
}
