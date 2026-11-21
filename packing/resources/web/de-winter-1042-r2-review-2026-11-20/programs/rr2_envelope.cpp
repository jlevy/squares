// Lane rR2 (issue 1042 derived bounds), check C3: rigorous integer bounds on the mass of
// the four-translated-region density g on the board [0, T]^2.
//
// g(P) = max over the regions containing P of f(P + t), where on each axis the regions
// are [0, Q + R] with offset 0 and [Q - R, T] with offset OFF = S - T, and f is the anchor
// density given as images with integer coordinates (units of 1e-8) and two integer
// densities each (rounded up and rounded down, units of 2^-E per unit area). With
// DISK = 1, a point in one quadrant about (Q, Q) drops the region of the opposite quadrant
// where its distance from (Q, Q) exceeds sqrt(1/2).
//
// The sweep runs over the whole board in x; between consecutive x events every region's
// profile in y is a step function, and every cell between consecutive y breakpoints is
// integrated exactly. Cells wholly inside or outside the disk are decided by integer tests;
// for a cell that straddles the circle, the area inside comes from the closed form in long
// double and is widened by MARGIN grid^2 units either way. Output: the integrals I_up and
// I_dn in units of 2^-E * 1e-16, so that mass = I / (2^E * 10^16).
//
// Usage: rr2_envelope sweep < input      (input format: see read_input)
//        rr2_envelope area < cells       (unit test of the disk area bounds)
// Build: g++ -O2 -std=c++17 -o rr2_envelope rr2_envelope.cpp

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>

typedef __int128 i128;
typedef long long i64;

static const i64 G = 100000000LL;           // grid units per unit length
static const i64 RHO2 = 5000000000000000LL;  // (sqrt(1/2) * G)^2 = G^2 / 2, exact
static const i64 MARGIN = 16;               // grid^2 units added around a float area

static void die(const char *msg) {
    std::fprintf(stderr, "rr2_envelope: %s\n", msg);
    std::exit(2);
}

static i128 mul(i128 a, i128 b) {
    i128 r;
    if (__builtin_mul_overflow(a, b, &r)) die("overflow in multiplication");
    return r;
}

static i128 add(i128 a, i128 b) {
    i128 r;
    if (__builtin_add_overflow(a, b, &r)) die("overflow in addition");
    return r;
}

static std::string str(i128 v) {
    if (v == 0) return "0";
    bool neg = v < 0;
    unsigned __int128 u = neg ? (unsigned __int128)(-(v + 1)) + 1 : (unsigned __int128)v;
    std::string s;
    while (u) {
        s.push_back(char('0' + int(u % 10)));
        u /= 10;
    }
    if (neg) s.push_back('-');
    std::reverse(s.begin(), s.end());
    return s;
}

// Integral of sqrt(RHO2 - t^2) over [0, n] in grid^2 units, 0 <= n, n^2 <= RHO2.
static long double phi(i64 n) {
    i64 rest = RHO2 - n * n;  // exact
    if (rest < 0) die("phi argument beyond the radius");
    long double root = sqrtl((long double)rest);
    long double ln = (long double)n;
    return 0.5L * (ln * root + (long double)RHO2 * atan2l(ln, root));
}

static long double phi_full() { return (long double)RHO2 * 3.14159265358979323846264338327950288L / 4.0L; }

// Area of the disk u^2 + v^2 <= RHO2 inside [0, u] x [0, v], grid^2 units, as an exact
// integer when the box lies inside the disk (exact = true) or as a long double otherwise.
static long double corner_area(i64 u, i64 v, bool &exact, i128 &exact_value) {
    exact = false;
    if (u <= 0 || v <= 0) {
        exact = true;
        exact_value = 0;
        return 0;
    }
    i128 uu = (i128)u * u, vv = (i128)v * v;
    if (uu + vv <= RHO2) {
        exact = true;
        exact_value = (i128)u * v;
        return 0;
    }
    long double pu = (2 * uu >= (i128)2 * RHO2) ? phi_full() : phi(u);
    if (2 * vv >= (i128)2 * RHO2) return pu;  // v >= rho: the arc stays below v
    i64 rest = RHO2 - (i64)vv;               // s1 = sqrt(rest), and s1 < u here
    long double s1 = sqrtl((long double)rest);
    long double lv = (long double)v;
    return pu + 0.5L * lv * s1 - 0.5L * (long double)RHO2 * atan2l(s1, lv);
}

// Bounds, in grid^2 units, on the area of [ua, ub] x [va, vb] inside the disk.
static void cell_disk_area(i64 ua, i64 ub, i64 va, i64 vb, i128 &lo, i128 &hi, bool &straddle) {
    i128 area = (i128)(ub - ua) * (vb - va);
    i128 far = (i128)ub * ub + (i128)vb * vb;
    i128 nearv = (i128)ua * ua + (i128)va * va;
    straddle = false;
    if (far <= RHO2) {
        lo = hi = area;
        return;
    }
    if (nearv >= RHO2) {
        lo = hi = 0;
        return;
    }
    straddle = true;
    bool e[4];
    i128 ev[4];
    long double f[4];
    f[0] = corner_area(ub, vb, e[0], ev[0]);
    f[1] = corner_area(ua, vb, e[1], ev[1]);
    f[2] = corner_area(ub, va, e[2], ev[2]);
    f[3] = corner_area(ua, va, e[3], ev[3]);
    i128 exact_part = 0;
    long double float_part = 0;
    const int sign[4] = {1, -1, -1, 1};
    for (int k = 0; k < 4; ++k) {
        if (e[k]) exact_part += sign[k] * ev[k];
        else float_part += sign[k] * f[k];
    }
    long double lo_f = floorl(float_part) - MARGIN;
    long double hi_f = ceill(float_part) + MARGIN;
    lo = exact_part + (i128)(i64)lo_f;
    hi = exact_part + (i128)(i64)hi_f;
    if (lo < 0) lo = 0;
    if (hi > area) hi = area;
    if (lo > hi) die("disk area bounds crossed");
}

struct Img {
    i64 x0, y0, x1, y1, up, dn;
};

struct Event {
    i64 x;
    int side;  // 0: L, 1: R
    int add;   // 1 insert, 0 remove
    int img;
};

struct Step {
    i64 y;
    i128 up, dn;  // value on [y, next y)
};

static i64 S, T, Q, R, OFF;
static int DISK, E;
static std::vector<Img> imgs;

static void read_input() {
    long long n;
    if (std::scanf("%lld %lld %lld %lld %d %d %lld", &S, &T, &Q, &R, &DISK, &E, &n) != 7)
        die("bad header");
    OFF = S - T;
    imgs.resize(n);
    for (long long i = 0; i < n; ++i) {
        Img &m = imgs[i];
        if (std::scanf("%lld %lld %lld %lld %lld %lld", &m.x0, &m.y0, &m.x1, &m.y1, &m.up, &m.dn) != 6)
            die("bad image line");
        if (!(m.x0 < m.x1 && m.y0 < m.y1)) die("degenerate image");
        if (m.dn < 0 || m.up < m.dn) die("bad densities");
        if (m.x0 < 0 || m.y0 < 0 || m.x1 > S || m.y1 > S) die("image outside the anchor board");
    }
    if (!(0 < Q - R && Q + R < T)) die("regions do not overlap inside the board");
}

// Profile of side s in anchor y: merged sorted steps from the active images.
static void build_profile(const std::vector<int> &active, std::vector<Step> &prof,
                          std::vector<std::pair<i64, int>> &ev) {
    ev.clear();
    for (int idx : active) {
        ev.push_back({imgs[idx].y0, idx + 1});
        ev.push_back({imgs[idx].y1, -(idx + 1)});
    }
    std::sort(ev.begin(), ev.end());
    prof.clear();
    i128 cu = 0, cd = 0;
    size_t k = 0;
    while (k < ev.size()) {
        i64 y = ev[k].first;
        while (k < ev.size() && ev[k].first == y) {
            int code = ev[k].second;
            if (code > 0) {
                cu += imgs[code - 1].up;
                cd += imgs[code - 1].dn;
            } else {
                cu -= imgs[-code - 1].up;
                cd -= imgs[-code - 1].dn;
            }
            ++k;
        }
        prof.push_back({y, cu, cd});
    }
}

static void value_at(const std::vector<Step> &prof, size_t &ptr, i64 y, i128 &up, i128 &dn) {
    // prof is sorted by y; the value at y is that of the last step with step.y <= y.
    while (ptr < prof.size() && prof[ptr].y <= y) ++ptr;
    if (ptr == 0) {
        up = dn = 0;
        return;
    }
    up = prof[ptr - 1].up;
    dn = prof[ptr - 1].dn;
}

static int sweep() {
    read_input();
    const i64 xwin_lo[2] = {0, Q - R}, xwin_hi[2] = {Q + R, T};
    const i64 off[2] = {0, OFF};
    std::vector<Event> events;
    for (int s = 0; s < 2; ++s) {
        for (size_t i = 0; i < imgs.size(); ++i) {
            i64 a = imgs[i].x0 - off[s], b = imgs[i].x1 - off[s];
            if (a < xwin_lo[s]) a = xwin_lo[s];
            if (b > xwin_hi[s]) b = xwin_hi[s];
            if (a >= b) continue;
            events.push_back({a, s, 1, (int)i});
            events.push_back({b, s, 0, (int)i});
        }
    }
    std::vector<i64> xs = {0, Q - R, Q, Q + R, T};
    for (auto &e : events) xs.push_back(e.x);
    std::sort(xs.begin(), xs.end());
    xs.erase(std::unique(xs.begin(), xs.end()), xs.end());
    std::sort(events.begin(), events.end(), [](const Event &a, const Event &b) { return a.x < b.x; });

    std::vector<int> active[2];
    std::vector<int> pos[2];
    pos[0].assign(imgs.size(), -1);
    pos[1].assign(imgs.size(), -1);
    std::vector<Step> prof[2];
    std::vector<std::pair<i64, int>> scratch;
    std::vector<i64> ys;
    i128 total_up = 0, total_dn = 0;
    long long slabs = 0, cells = 0, straddles = 0;
    i128 max_value = 0;
    size_t ei = 0;
    for (size_t xi = 0; xi + 1 < xs.size(); ++xi) {
        i64 xa = xs[xi], xb = xs[xi + 1];
        while (ei < events.size() && events[ei].x == xa) {
            const Event &e = events[ei];
            std::vector<int> &act = active[e.side];
            std::vector<int> &ps = pos[e.side];
            if (e.add) {
                if (ps[e.img] != -1) die("image inserted twice");
                ps[e.img] = (int)act.size();
                act.push_back(e.img);
            } else {
                int p = ps[e.img];
                if (p == -1) die("image removed while inactive");
                int last = act.back();
                act[p] = last;
                ps[last] = p;
                act.pop_back();
                ps[e.img] = -1;
            }
            ++ei;
        }
        if (xa < 0 || xb > T) continue;
        if (xa >= xb) continue;
        bool sx[2] = {xb <= Q + R, xa >= Q - R};
        bool left = xb <= Q;  // x quadrant: left of Q, else right (Q is a breakpoint)
        ++slabs;
        for (int s = 0; s < 2; ++s)
            if (sx[s]) build_profile(active[s], prof[s], scratch);
        // y breakpoints of every stream (s, t), mapped to the board
        ys.clear();
        ys.push_back(0);
        ys.push_back(Q - R);
        ys.push_back(Q);
        ys.push_back(Q + R);
        ys.push_back(T);
        const i64 ywin_lo[2] = {0, Q - R}, ywin_hi[2] = {Q + R, T};
        for (int s = 0; s < 2; ++s) {
            if (!sx[s]) continue;
            for (const Step &st : prof[s])
                for (int t = 0; t < 2; ++t) {
                    i64 y = st.y - off[t];
                    if (y > ywin_lo[t] && y < ywin_hi[t]) ys.push_back(y);
                }
        }
        std::sort(ys.begin(), ys.end());
        ys.erase(std::unique(ys.begin(), ys.end()), ys.end());
        size_t ptr[2][2] = {{0, 0}, {0, 0}};
        i128 slab_up = 0, slab_dn = 0;  // sum of height * value (grid * 2^-E units)
        i128 extra_up = 0, extra_dn = 0;  // disk terms, already area-weighted
        i64 width = xb - xa;
        for (size_t yi = 0; yi + 1 < ys.size(); ++yi) {
            i64 ya = ys[yi], yb = ys[yi + 1];
            if (ya < 0 || yb > T || ya >= yb) continue;
            ++cells;
            bool sy[2] = {yb <= Q + R, ya >= Q - R};
            bool low = yb <= Q;
            i128 vu[2][2], vd[2][2];
            bool on[2][2];
            for (int s = 0; s < 2; ++s)
                for (int t = 0; t < 2; ++t) {
                    on[s][t] = sx[s] && sy[t];
                    if (on[s][t]) value_at(prof[s], ptr[s][t], ya + off[t], vu[s][t], vd[s][t]);
                }
            int os = left ? 1 : 0, ot = low ? 1 : 0;  // the opposite quadrant's region
            bool disk_here = DISK && on[0][0] && on[0][1] && on[1][0] && on[1][1];
            i128 mu = 0, md = 0;
            for (int s = 0; s < 2; ++s)
                for (int t = 0; t < 2; ++t) {
                    if (!on[s][t]) continue;
                    if (disk_here && s == os && t == ot) continue;
                    if (vu[s][t] > mu) mu = vu[s][t];
                    if (vd[s][t] > md) md = vd[s][t];
                }
            if (mu > max_value) max_value = mu;
            i64 h = yb - ya;
            slab_up = add(slab_up, mul(h, mu));
            slab_dn = add(slab_dn, mul(h, md));
            if (disk_here) {
                i128 ou = vu[os][ot], od = vd[os][ot];
                if (ou > max_value) max_value = ou;
                if (ou > mu || od > md) {
                    i64 ua, ub, va, vb;
                    if (left) {
                        ua = Q - xb;
                        ub = Q - xa;
                    } else {
                        ua = xa - Q;
                        ub = xb - Q;
                    }
                    if (low) {
                        va = Q - yb;
                        vb = Q - ya;
                    } else {
                        va = ya - Q;
                        vb = yb - Q;
                    }
                    i128 alo, ahi;
                    bool st;
                    cell_disk_area(ua, ub, va, vb, alo, ahi, st);
                    if (st) ++straddles;
                    if (ou > mu) extra_up = add(extra_up, mul(ahi, ou - mu));
                    if (od > md) extra_dn = add(extra_dn, mul(alo, od - md));
                }
            }
        }
        total_up = add(total_up, add(mul(slab_up, width), extra_up));
        total_dn = add(total_dn, add(mul(slab_dn, width), extra_dn));
    }
    while (ei < events.size()) {  // only removals at x = T may remain
        if (events[ei].x != xs.back() || events[ei].add) die("events left after the sweep");
        ++ei;
    }
    std::printf("I_up %s\nI_dn %s\nslabs %lld\ncells %lld\nstraddles %lld\nmax_value %s\nE %d\n",
                str(total_up).c_str(), str(total_dn).c_str(), slabs, cells, straddles,
                str(max_value).c_str(), E);
    return 0;
}

static int area_mode() {
    long long ua, ub, va, vb;
    while (std::scanf("%lld %lld %lld %lld", &ua, &ub, &va, &vb) == 4) {
        i128 lo, hi;
        bool st;
        cell_disk_area(ua, ub, va, vb, lo, hi, st);
        std::printf("%s %s %d\n", str(lo).c_str(), str(hi).c_str(), st ? 1 : 0);
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) die("usage: rr2_envelope sweep|area < input");
    std::string mode = argv[1];
    if (mode == "sweep") return sweep();
    if (mode == "area") return area_mode();
    die("unknown mode");
}
