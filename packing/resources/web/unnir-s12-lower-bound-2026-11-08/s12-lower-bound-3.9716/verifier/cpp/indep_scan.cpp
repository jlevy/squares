// indep_check.cpp -- an independent checker for weighted closed covers of [0,s]^2
// (written from the statement, not from evand/square-packing's verify/ or xcheck.py).
//
// Claim checked:  every closed unit square Q with Q subset [0,s]^2 (any centre, any angle)
// contains certificate points of total weight >= 1.   Together with total weight < n this
// gives s(n) >= s (rescaling argument, see README).
//
// Method.
//  * Angles: full range [0deg, 90deg], bins [t_k, t_{k+1}], t_k = 2 atan(k/N), k = 0..N-1
//    (t_N = 90deg).  No symmetry of the point set is assumed.  cos/sin of t_k are rational.
//  * Shrink lemma: a unit square at any angle t in [t_k, t_{k+1}] contains the concentric square
//    of side sigma_k = 1/(cos d + sin d) at angle t_k, d = t_{k+1} - t_k (cos x + sin x is
//    increasing on [0,45deg]).  sigma_k is rational; we use it (almost) exactly.
//  * Admissible centres of a unit square at angle t: [w(t)/2, s - w(t)/2]^2, w = cos t + sin t,
//    which is concave on [0,90deg], so over the bin the union is [wmin/2, s - wmin/2]^2 with
//    wmin = min(w(t_k), w(t_{k+1})).
//  * Everything is mapped to an integer grid of pitch 1/Q in the rotated frame of t_k with
//    CONSERVATIVE rounding: atom positions are floored (error < 1 unit) and the half side h is
//    floored and then reduced by one unit, so a rounded box containment implies a true one;
//    the centre domain is rounded outward.  Rounding can therefore only lower the minimum.
//  * In the rotated frame every atom p is captured iff the centre u lies in the closed box
//    [P0-h, P0+h] x [P1-h, P1+h].  The captured weight is upper semicontinuous in u, so its
//    minimum over the (closed, convex) domain equals its infimum over open cells.  We sweep open
//    slabs in u0 between consecutive box edges, keep the active boxes in a segment tree over the
//    open elementary u1-intervals (range add / range min), and query, per slab, every elementary
//    interval that meets the u1-projection of (domain intersect closed slab) -- a superset.
//  * All arithmetic is exact __int128 with overflow checks; any overflow aborts.
#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <climits>
#include <cmath>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <utility>
using namespace std;
typedef __int128 I;
typedef long long ll;

static void die(const string& m) { fprintf(stderr, "ERROR: %s\n", m.c_str()); exit(2); }
static I mul(I a, I b) { I r; if (__builtin_mul_overflow(a, b, &r)) die("overflow (mul)"); return r; }
static I add(I a, I b) { I r; if (__builtin_add_overflow(a, b, &r)) die("overflow (add)"); return r; }
static I sub(I a, I b) { I r; if (__builtin_sub_overflow(a, b, &r)) die("overflow (sub)"); return r; }
static I fdiv(I a, I b) { if (b <= 0) die("fdiv: nonpositive denominator"); I q = a / b; if (a % b != 0 && a < 0) q--; return q; }
static I cdiv(I a, I b) { if (b <= 0) die("cdiv: nonpositive denominator"); I q = a / b; if (a % b != 0 && a > 0) q++; return q; }
static string s128(I x) { if (x == 0) return "0"; bool neg = x < 0; if (neg) x = -x; string s; while (x > 0) { s += char('0' + int(x % 10)); x /= 10; } if (neg) s += '-'; reverse(s.begin(), s.end()); return s; }

struct Seg {  // range add, range min over [0, n)
    int n; vector<ll> mn, lz;
    void init(int n_) { n = n_; mn.assign(4 * n, 0); lz.assign(4 * n, 0); }
    void upd(int o, int l, int r, int ql, int qr, ll v) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { mn[o] += v; lz[o] += v; return; }
        int m = (l + r) / 2; upd(2 * o, l, m, ql, qr, v); upd(2 * o + 1, m + 1, r, ql, qr, v);
        mn[o] = min(mn[2 * o], mn[2 * o + 1]) + lz[o];
    }
    ll qry(int o, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return LLONG_MAX / 4;
        if (ql <= l && r <= qr) return mn[o];
        int m = (l + r) / 2; return min(qry(2 * o, l, m, ql, qr), qry(2 * o + 1, m + 1, r, ql, qr)) + lz[o];
    }
    // leftmost index in [ql,qr] attaining value target (diagnostics only)
    int arg(int o, int l, int r, int ql, int qr, ll target, ll acc) {
        if (qr < l || r < ql) return -1;
        if (mn[o] + acc > target) return -1;
        if (l == r) return l;
        int m = (l + r) / 2; acc += lz[o];
        int x = arg(2 * o, l, m, ql, qr, target, acc); if (x >= 0) return x;
        return arg(2 * o + 1, m + 1, r, ql, qr, target, acc);
    }
    int argmin(int l, int r, ll v) { return arg(1, 0, n - 1, l, r, v, 0); }
    void add(int l, int r, ll v) { if (l <= r) upd(1, 0, n - 1, l, r, v); }
    ll query(int l, int r) { return qry(1, 0, n - 1, l, r); }
};

int main(int argc, char** argv) {
    if (argc < 3) die("usage: indep_check CERT N [Q=1e15] [n=12]");
    ifstream f(argv[1]); if (!f) die("cannot open certificate");
    ll N = atoll(argv[2]);
    I Q = argc > 3 ? (I)atoll(argv[3]) : (I)1000000000000000LL;
    ll nsq = argc > 4 ? atoll(argv[4]) : 12;
    ll scan_thresh = argc > 5 ? atoll(argv[5]) : -1;   // print every bin whose minimum is below this numerator
    ll kmax = argc > 6 ? atoll(argv[6]) : -1;          // sweep only bins k < kmax (D4-symmetric certificates)
    ll kmin = argc > 7 ? atoll(argv[7]) : 0;           // and k >= kmin
    ll s_num, s_den, D, W, m;
    if (!(f >> s_num >> s_den >> D >> W >> m)) die("bad header");
    if (s_num <= 0 || s_den <= 0 || D <= 0 || W <= 0 || m <= 0 || N < 1) die("nonpositive header value");
    vector<ll> X(m), Y(m), w(m);
    I total = 0;
    for (ll i = 0; i < m; i++) {
        if (!(f >> X[i] >> Y[i] >> w[i])) die("short file");
        if (w[i] < 0) die("negative weight");
        // inside [0,s]^2 ?  X/D <= s_num/s_den  <=>  X*s_den <= s_num*D
        if (X[i] < 0 || Y[i] < 0 || mul(X[i], s_den) > mul(s_num, D) || mul(Y[i], s_den) > mul(s_num, D)) die("point outside container");
        total += w[i];
    }
    string extra; if (f >> extra) die("trailing data (this checker only handles plain point certificates)");
    printf("certificate: s = %lld/%lld = %.9f, D = %lld, W = %lld, m = %lld\n", s_num, s_den, (double)s_num / s_den, D, W, m);
    printf("total weight = %s/%lld = %.9f   (n = %lld: %s)\n", s128(total).c_str(), W, (double)total / W, nsq,
           total < (I)nsq * W ? "total < n" : "TOTAL NOT < n");
    printf("angle net N = %lld, bins k = 0..%lld covering [0,90] deg (no symmetry assumed), grid Q = %s\n", N, N - 1, s128(Q).c_str());

    I best = (I)LLONG_MAX; ll best_k = -1; double best_u0 = 0, best_u1 = 0;
    I NN = (I)N * N;
    vector<I> P0(m), P1(m);
    for (ll k = kmin; k < (kmax > 0 ? min(kmax, N) : N); k++) {
        I binbest = (I)LLONG_MAX;
        I c0 = NN - (I)k * k, s0 = (I)2 * k * N, g0 = NN + (I)k * k;
        I k1 = k + 1;
        I c1 = NN - k1 * k1, s1 = (I)2 * k1 * N, g1 = NN + k1 * k1;
        I cd = add(mul(c0, c1), mul(s0, s1));          // cos(d) * g0 g1
        I sd = sub(mul(c0, s1), mul(s0, c1));          // sin(d) * g0 g1  (> 0)
        if (sd <= 0 || cd <= 0) die("bad bin");
        // h = sigma/2 = g0 g1 / (2 (cd + sd)); grid half side, floored then minus one unit
        I hq = fdiv(mul(mul(g0, g1), Q), mul(2, add(cd, sd))) - 1;
        if (hq <= 0) die("Q too small");
        // wmin = min((c0+s0)/g0, (c1+s1)/g1)
        I wn, wd;
        if (mul(add(c0, s0), g1) <= mul(add(c1, s1), g0)) { wn = add(c0, s0); wd = g0; } else { wn = add(c1, s1); wd = g1; }
        // domain [L, U]^2 in grid units, rounded outward:  L = floor(wn Q / (2 wd)),  U = ceil((s - wn/(2wd)) Q)
        I L = fdiv(mul(wn, Q), mul(2, wd));
        I U = cdiv(mul(sub(mul(mul(2, wd), s_num), mul(wn, s_den)), Q), mul(mul(2, wd), s_den));
        if (L > U) continue;  // no admissible centre in this bin
        I cn = c0, sn = s0, g = g0;
        // atoms in the rotated frame (grid units, floored)
        I gD = mul(g, D);
        for (ll i = 0; i < m; i++) {
            P0[i] = fdiv(mul(add(mul(cn, X[i]), mul(sn, Y[i])), Q), gD);
            P1[i] = fdiv(mul(add(mul(-sn, X[i]), mul(cn, Y[i])), Q), gD);
        }
        // domain vertices (x,y) in {L,U}^2: u0 = (cn x + sn y)/g, u1 = (-sn x + cn y)/g
        I vx[4] = {L, U, U, L}, vy[4] = {L, L, U, U};
        I vu0[4], vu1[4];
        for (int j = 0; j < 4; j++) { vu0[j] = add(mul(cn, vx[j]), mul(sn, vy[j])); vu1[j] = add(mul(-sn, vx[j]), mul(cn, vy[j])); }
        I px0 = fdiv(*min_element(vu0, vu0 + 4), g), px1 = cdiv(*max_element(vu0, vu0 + 4), g);
        // u0 breakpoints: box edges and domain extremes
        vector<I> xs; xs.reserve(2 * m + 2);
        for (ll i = 0; i < m; i++) { xs.push_back(P0[i] - hq); xs.push_back(P0[i] + hq); }
        xs.push_back(px0); xs.push_back(px1);
        sort(xs.begin(), xs.end()); xs.erase(unique(xs.begin(), xs.end()), xs.end());
        // u1 elementary intervals
        vector<I> ys; ys.reserve(2 * m);
        for (ll i = 0; i < m; i++) { ys.push_back(P1[i] - hq); ys.push_back(P1[i] + hq); }
        sort(ys.begin(), ys.end()); ys.erase(unique(ys.begin(), ys.end()), ys.end());
        int M = ys.size();
        Seg st; st.init(M + 1);   // interval j: (ys[j-1], ys[j]), j = 0..M, with ys[-1] = -inf, ys[M] = +inf
        auto yidx = [&](I v) { return int(lower_bound(ys.begin(), ys.end(), v) - ys.begin()); };
        // events
        vector<pair<I, ll>> starts(m), ends(m);
        for (ll i = 0; i < m; i++) { starts[i] = {P0[i] - hq, i}; ends[i] = {P0[i] + hq, i}; }
        sort(starts.begin(), starts.end()); sort(ends.begin(), ends.end());
        size_t ps = 0, pe = 0;
        auto box_range = [&](ll i, int& l, int& r) { l = yidx(P1[i] - hq) + 1; r = yidx(P1[i] + hq); };
        for (size_t t = 0; t + 1 < xs.size(); t++) {
            I a = xs[t], b = xs[t + 1];
            while (ps < starts.size() && starts[ps].first == a) { int l, r; box_range(starts[ps].second, l, r); st.add(l, r, w[starts[ps].second]); ps++; }
            while (pe < ends.size() && ends[pe].first == a) { int l, r; box_range(ends[pe].second, l, r); st.add(l, r, -w[ends[pe].second]); pe++; }
            if (b <= px0 || a >= px1) continue;
            // u1 range of the domain over the CLOSED slab [a,b] (superset of the open slab)
            I vlo = 0, vhi = 0; bool any = false;
            auto cand = [&](I num, I den) {  // candidate u1 = num/den, den > 0
                I lo = fdiv(num, den), hi = cdiv(num, den);
                if (!any) { vlo = lo; vhi = hi; any = true; } else { vlo = min(vlo, lo); vhi = max(vhi, hi); }
            };
            for (int j = 0; j < 4; j++) if (mul(a, g) <= vu0[j] && vu0[j] <= mul(b, g)) cand(vu1[j], g);
            for (int e = 0; e < 2; e++) {
                I tt = e == 0 ? a : b;
                if (sn == 0) {  // identity rotation: domain is [L,U]^2 itself
                    if (L <= tt && tt <= U) { cand(L, 1); cand(U, 1); }
                    continue;
                }
                // edges x = X0 (X0 in {L,U}), y in [L,U]:  y = (tt g - cn X0)/sn,  u1 = (cn tt - g X0)/sn
                for (I X0 : {L, U}) {
                    I yn = sub(mul(tt, g), mul(cn, X0));
                    if (mul(L, sn) <= yn && yn <= mul(U, sn)) cand(sub(mul(cn, tt), mul(g, X0)), sn);
                }
                // edges y = Y0, x in [L,U]:  x = (tt g - sn Y0)/cn,  u1 = (g Y0 - sn tt)/cn
                for (I Y0 : {L, U}) {
                    I xn = sub(mul(tt, g), mul(sn, Y0));
                    if (mul(L, cn) <= xn && xn <= mul(U, cn)) cand(sub(mul(g, Y0), mul(sn, tt)), cn);
                }
            }
            if (!any) continue;
            // elementary intervals meeting [vlo, vhi]: right end > vlo and left end < vhi
            int jlo = int(upper_bound(ys.begin(), ys.end(), vlo) - ys.begin());
            int jhi = int(lower_bound(ys.begin(), ys.end(), vhi) - ys.begin());
            if (jlo > jhi) swap(jlo, jhi);   // degenerate: take both neighbours (superset)
            ll v = st.query(jlo, jhi);
            if ((I)v < binbest) binbest = v;
            if ((I)v < best) {
                best = v; best_k = k;
                best_u0 = (double)(a + b) / 2 / (double)Q;
                int j = st.argmin(jlo, jhi, v);
                double yl = j == 0 ? (double)vlo : (double)max(ys[j - 1], vlo), yr = j == M ? (double)vhi : (double)min(ys[j], vhi);
                best_u1 = (yl + yr) / 2 / (double)Q;
            }
        }
        if (scan_thresh >= 0 && binbest < (I)scan_thresh) { printf("BIN %lld %s\n", k, s128(binbest).c_str()); fflush(stdout); }
    }
    double deg = 2 * atan((double)best_k / N) * 180 / M_PI;
    (void)0;
    printf("min captured weight over all bins = %s/%lld = %.9f   (bin k=%lld, %.4f deg)\n", s128(best).c_str(), W, (double)best / W, best_k, deg);
    {   // approximate location of the minimising cell (centre in container coordinates), for diagnosis only
        double th = 2 * atan((double)best_k / N), cx = cos(th) * best_u0 - sin(th) * best_u1, cy = sin(th) * best_u0 + cos(th) * best_u1;
        printf("  near centre (%.6f, %.6f) at angle %.6f deg (diagnostic, floating point)\n", cx, cy, deg);
    }
    bool ok = best >= (I)W && total < (I)nsq * W;
    printf("%s\n", ok ? "VERIFIED: every closed unit square inside the container captures weight >= 1, and total weight < n"
                      : "NOT VERIFIED");
    return ok ? 0 : 1;
}
