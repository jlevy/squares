/* Geometry kernels, instantiated for REAL = double (suffix _d) and long double (suffix _l).
 * All coordinates passed in are RELATIVE to the core centre p0.
 * The core is the rotated rectangle {q : |c qx + s qy| <= a, |-s qx + c qy| <= b}, c,s >= 0. */
#define CAT2(x,y) x##y
#define CAT(x,y) CAT2(x,y)
#define FN(name) CAT(name, SUF)

static inline REAL FN(rmax)(REAL a, REAL b){ return a > b ? a : b; }
static inline REAL FN(rmin)(REAL a, REAL b){ return a < b ? a : b; }

/* Sutherland-Hodgman clip of polygon (X,Y,n) by  sgn*coord <= lim  (coord = X if axis==0 else Y). */
static int FN(clip1)(const REAL *X, const REAL *Y, int n, REAL *OX, REAL *OY, int axis, REAL sgn, REAL lim)
{
    int m = 0;
    for (int i = 0; i < n; i++) {
        int j = (i + 1 == n) ? 0 : i + 1;
        REAL vp = sgn * (axis ? Y[i] : X[i]);
        REAL vq = sgn * (axis ? Y[j] : X[j]);
        int ip = vp <= lim, iq = vq <= lim;
        if (ip) { OX[m] = X[i]; OY[m] = Y[i]; m++; }
        if (ip != iq) {
            REAL t = (lim - vp) / (vq - vp);
            if (t < 0) t = 0; if (t > 1) t = 1;
            OX[m] = X[i] + t * (X[j] - X[i]);
            OY[m] = Y[i] + t * (Y[j] - Y[i]);
            m++;
        }
    }
    return m;
}

/* area of axis rectangle [x1,x2]x[y1,y2] (relative coords) intersected with the rotated rectangle (c,s,a,b) */
static REAL FN(area_rr)(REAL x1, REAL x2, REAL y1, REAL y2, REAL c, REAL s, REAL a, REAL b)
{
    if (a <= 0 || b <= 0) return 0;
    REAL Hx = c * a + s * b, Hy = s * a + c * b;
    Hx = Hx * (REAL)(1 + 1e-12) + (REAL)1e-12;  /* any superset of the core's bounding box is fine */
    Hy = Hy * (REAL)(1 + 1e-12) + (REAL)1e-12;
    if (x1 < -Hx) x1 = -Hx; if (x2 > Hx) x2 = Hx;
    if (y1 < -Hy) y1 = -Hy; if (y2 > Hy) y2 = Hy;
    if (x1 >= x2 || y1 >= y2) return 0;
    REAL X[16], Y[16], X2[16], Y2[16];
    REAL px[4] = {x1, x2, x2, x1}, py[4] = {y1, y1, y2, y2};
    for (int i = 0; i < 4; i++) { X[i] = c * px[i] + s * py[i]; Y[i] = -s * px[i] + c * py[i]; }
    int n = 4;
    n = FN(clip1)(X, Y, n, X2, Y2, 0, 1, a);  if (n < 3) return 0;
    n = FN(clip1)(X2, Y2, n, X, Y, 0, -1, a); if (n < 3) return 0;
    n = FN(clip1)(X, Y, n, X2, Y2, 1, 1, b);  if (n < 3) return 0;
    n = FN(clip1)(X2, Y2, n, X, Y, 1, -1, b); if (n < 3) return 0;
    REAL A = 0, x0 = X[0], y0 = Y[0];
    for (int i = 1; i + 1 < n; i++)
        A += (X[i] - x0) * (Y[i + 1] - y0) - (X[i + 1] - x0) * (Y[i] - y0);
    A *= (REAL)0.5;
    return A > 0 ? A : 0;
}

/* length of segment P0->P1 (relative coords) inside the rotated rectangle (c,s,a,b) */
static REAL FN(seg_rr)(REAL x0, REAL y0, REAL x1, REAL y1, REAL c, REAL s, REAL a, REAL b)
{
    if (a < 0 || b < 0) return 0;
    {   REAL Hx = (c * a + s * b) * (REAL)(1 + 1e-12) + (REAL)1e-12, Hy = (s * a + c * b) * (REAL)(1 + 1e-12) + (REAL)1e-12;
        if (x0 == x1) { if (x0 > Hx || x0 < -Hx) return 0; if (y0 < -Hy) y0 = -Hy; if (y1 > Hy) y1 = Hy; if (y1 <= y0) return 0; }
        else { if (y0 > Hy || y0 < -Hy) return 0; if (x0 < -Hx) x0 = -Hx; if (x1 > Hx) x1 = Hx; if (x1 <= x0) return 0; } }
    REAL len = (x1 - x0) + (y1 - y0); /* axis-parallel segments only, x1>=x0, y1>=y0 */
    REAL X0 = c * x0 + s * y0, Y0 = -s * x0 + c * y0;
    REAL dX = c * (x1 - x0) + s * (y1 - y0), dY = -s * (x1 - x0) + c * (y1 - y0);
    REAL t0 = 0, t1 = 1;
    if (dX == 0) { if (X0 > a || X0 < -a) return 0; }
    else { REAL ta = (a - X0) / dX, tb = (-a - X0) / dX;
           if (ta > tb) { REAL tt = ta; ta = tb; tb = tt; }
           if (ta > t0) t0 = ta; if (tb < t1) t1 = tb; }
    if (dY == 0) { if (Y0 > b || Y0 < -b) return 0; }
    else { REAL ta = (b - Y0) / dY, tb = (-b - Y0) / dY;
           if (ta > tb) { REAL tt = ta; ta = tb; tb = tt; }
           if (ta > t0) t0 = ta; if (tb < t1) t1 = tb; }
    if (t1 <= t0) return 0;
    return (t1 - t0) * len;
}
