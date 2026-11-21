// C5: an independent refutation attempt for one case of the s(18) argument (lane r1050).
//
// Reads an instance on stdin:
//   U  K  max_rounds  node_budget  seconds
//   nmarks, then per mark: x y occupied(0/1)
//   ntiles, then per tile: the index of its mark (an occupied mark)
// and prints one line: REFUTED or UNDECIDED, with counters.
//
// Model. Tile i is a closed unit square containing its mark m_i in its interior, lying in
// [0, U]^2, avoiding every other occupied mark (closed), with pairwise disjoint interiors.
// Angles are taken mod pi/2 in [-pi/4, pi/4] and split into K slices; each slice of each
// tile carries a convex polygon enclosing its possible centres.
//   R1 capture: c in m + R(phi)[-hout, hout]^2, hout = h (cos d + sin d) + eta
//   R2 walls: c in [wmin - eta, U - wmin + eta]^2, wmin the least half-width on the slice
//   R3 obstacles: remove centres whose inner square (half-side hin = h/(cos d + sin d) -
//      eta, mid-frame) contains another occupied mark: that mark would lie in the tile
//   R4 pairs: remove centres c_i such that for every live slice b of tile j and every
//      vertex v of its polygon, c_i - v lies in the Minkowski sum of the two inner squares
//      (shrunk by eta): the interiors would overlap for every pose of tile j
//   R5 the new polygon is the convex hull of what remains
// A case is refuted when some tile has no live slice, in every branch. Branching splits a
// tile's live slices into two sets, or bisects its one live slice (re-seeding each half
// inside the parent's polygon, so the inner squares grow as the slices narrow), or splits
// its centres by a line into two closed halves.
// Arithmetic is double precision. Every enclosure is padded by eta = 1e-9 and every
// forbidden region shrunk by eta, far above the rounding error of these short formulas
// on numbers below 10, so a refutation is sound up to that error model: independent
// evidence, not an exact certificate.

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <vector>

namespace {

struct Pt {
  double x, y;
};
using Poly = std::vector<Pt>;
struct HP {  // n.x <= c
  double nx, ny, c;
};

constexpr double ETA = 1e-9;
constexpr double HALF = 0.5;

double cross(const Pt& o, const Pt& a, const Pt& b) {
  return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x);
}

Poly hull(std::vector<Pt> p) {
  std::sort(p.begin(), p.end(),
            [](const Pt& a, const Pt& b) { return a.x < b.x || (a.x == b.x && a.y < b.y); });
  Poly u;
  for (const Pt& q : p) {
    if (!u.empty() && std::fabs(u.back().x - q.x) < 1e-13 && std::fabs(u.back().y - q.y) < 1e-13)
      continue;
    u.push_back(q);
  }
  if (u.size() <= 2) return u;
  Poly h(2 * u.size());
  size_t k = 0;
  for (size_t i = 0; i < u.size(); ++i) {
    while (k >= 2 && cross(h[k - 2], h[k - 1], u[i]) <= 0) --k;
    h[k++] = u[i];
  }
  for (size_t i = u.size() - 1, t = k + 1; i-- > 0;) {
    while (k >= t && cross(h[k - 2], h[k - 1], u[i]) <= 0) --k;
    h[k++] = u[i];
  }
  h.resize(k - 1);
  if (h.empty()) h.push_back(u[0]);
  return h;
}

Poly clip(const Poly& poly, const HP& hp) {
  Poly out;
  size_t n = poly.size();
  if (n == 0) return out;
  if (n == 1) {
    if (hp.nx * poly[0].x + hp.ny * poly[0].y <= hp.c) out.push_back(poly[0]);
    return out;
  }
  for (size_t i = 0; i < n; ++i) {
    const Pt& p = poly[i];
    const Pt& q = poly[(i + 1) % n];
    double fp = hp.nx * p.x + hp.ny * p.y - hp.c;
    double fq = hp.nx * q.x + hp.ny * q.y - hp.c;
    if (fp <= 0) out.push_back(p);
    if ((fp < 0 && fq > 0) || (fp > 0 && fq < 0)) {
      double t = fp / (fp - fq);
      out.push_back({p.x + t * (q.x - p.x), p.y + t * (q.y - p.y)});
    }
    if (n == 2) break;
  }
  if (n == 2) {  // segment: also test the far end
    const Pt& q = poly[1];
    if (hp.nx * q.x + hp.ny * q.y <= hp.c) out.push_back(q);
    return hull(out);
  }
  // Sutherland-Hodgman keeps a convex polygon in counter-clockwise order; drop repeats.
  Poly d;
  for (const Pt& p : out)
    if (d.empty() || std::fabs(d.back().x - p.x) > 1e-13 || std::fabs(d.back().y - p.y) > 1e-13)
      d.push_back(p);
  while (d.size() > 1 && std::fabs(d.front().x - d.back().x) <= 1e-13 &&
         std::fabs(d.front().y - d.back().y) <= 1e-13)
    d.pop_back();
  return d;
}

double area(const Poly& p) {
  double a = 0;
  for (size_t i = 0; i < p.size(); ++i) {
    const Pt& u = p[i];
    const Pt& v = p[(i + 1) % p.size()];
    a += u.x * v.y - u.y * v.x;
  }
  return std::fabs(a) / 2;
}

// Hull of poly minus the closed convex region F (given by half-planes).
Poly minus_convex(const Poly& poly, const std::vector<HP>& F) {
  std::vector<Pt> keep;
  size_t n = poly.size();
  auto inF = [&](const Pt& p) {
    for (const HP& h : F)
      if (h.nx * p.x + h.ny * p.y > h.c) return false;
    return true;
  };
  if (n == 0) return {};
  if (n == 1) {
    if (!inF(poly[0])) keep.push_back(poly[0]);
    return keep;
  }
  size_t edges = (n == 2) ? 1 : n;
  for (size_t k = 0; k < edges; ++k) {
    const Pt& p = poly[k];
    const Pt& q = poly[(k + 1) % n];
    double lo = 0, hi = 1;
    bool empty = false;
    for (const HP& h : F) {
      double a = h.nx * p.x + h.ny * p.y;
      double d = h.nx * (q.x - p.x) + h.ny * (q.y - p.y);
      if (d == 0) {
        if (a > h.c) {
          empty = true;
          break;
        }
        continue;
      }
      double t = (h.c - a) / d;
      if (d > 0) {
        if (t < hi) hi = t;
      } else {
        if (t > lo) lo = t;
      }
      if (lo > hi) {
        empty = true;
        break;
      }
    }
    if (empty) {
      keep.push_back(p);
      keep.push_back(q);
      continue;
    }
    if (lo > 0) {
      keep.push_back(p);
      keep.push_back({p.x + lo * (q.x - p.x), p.y + lo * (q.y - p.y)});
    }
    if (hi < 1) {
      keep.push_back(q);
      keep.push_back({p.x + hi * (q.x - p.x), p.y + hi * (q.y - p.y)});
    }
  }
  if (keep.empty()) return {};
  return hull(keep);
}

struct SliceGeo {
  double lo, hi, phi, c, s, hin, hout, wmin;
};

SliceGeo make_geo(double lo, double hi) {
  double phi = (lo + hi) / 2, d = (hi - lo) / 2;
  double f = std::cos(d) + std::sin(d);
  double wlo = (std::cos(lo) + std::fabs(std::sin(lo))) / 2;
  double whi = (std::cos(hi) + std::fabs(std::sin(hi))) / 2;
  double wmin = (lo <= 0 && hi >= 0) ? HALF : std::min(wlo, whi);
  return {lo, hi, phi, std::cos(phi), std::sin(phi), HALF / f - ETA, HALF * f + ETA, wmin};
}

struct Slice {
  bool alive;
  Poly poly;
  SliceGeo g;
  long version = 0;
  std::vector<long> seen;       // seen[j]: version of tile j when this slice was last pruned
  std::vector<long> seen_self;  // this slice's version at that time
};

struct Tile {
  int mark;
  std::vector<Slice> sl;
  long version = 0;  // bumped whenever a slice of this tile changes
};

struct Ctx {
  double U;
  int K;
  int max_rounds;
  long node_budget;
  double seconds;
  std::vector<Pt> marks;
  std::vector<int> occupied;
  long nodes = 0;
  long rounds = 0;
  int max_depth = 0;
  std::chrono::steady_clock::time_point t0;
  bool out_of_budget = false;
};

constexpr int DEPTH_LIMIT = 400;

// The 8 edge normals of the Minkowski sum of inner squares of slices A and B, with the sum's
// support value in each.
void sum_normals(const SliceGeo& A, const SliceGeo& B, double nx[8], double ny[8], double sup[8]) {
  const double ua[2] = {A.c, A.s}, va[2] = {-A.s, A.c};
  const double ub[2] = {B.c, B.s}, vb[2] = {-B.s, B.c};
  const double* dirs[4] = {ua, va, ub, vb};
  for (int k = 0; k < 4; ++k) {
    for (int sg = 0; sg < 2; ++sg) {
      double x = sg ? -dirs[k][0] : dirs[k][0];
      double y = sg ? -dirs[k][1] : dirs[k][1];
      int idx = 2 * k + sg;
      nx[idx] = x;
      ny[idx] = y;
      double ra = A.hin * (std::fabs(x * ua[0] + y * ua[1]) + std::fabs(x * va[0] + y * va[1]));
      double rb = B.hin * (std::fabs(x * ub[0] + y * ub[1]) + std::fabs(x * vb[0] + y * vb[1]));
      sup[idx] = ra + rb;
    }
  }
}

// R1, R2, R3 for one slice of tile i, intersected with an enclosing polygon (or none).
Poly seed_slice(const Ctx& C, const Tile& t, const SliceGeo& g, const Poly* within) {
  const Pt m = C.marks[t.mark];
  const double ux = g.c, uy = g.s, vx = -g.s, vy = g.c;
  Poly sq = hull({{m.x + g.hout * (ux + vx), m.y + g.hout * (uy + vy)},
                  {m.x + g.hout * (-ux + vx), m.y + g.hout * (-uy + vy)},
                  {m.x + g.hout * (-ux - vx), m.y + g.hout * (-uy - vy)},
                  {m.x + g.hout * (ux - vx), m.y + g.hout * (uy - vy)}});
  double lo = g.wmin - ETA, hi = C.U - g.wmin + ETA;
  sq = clip(sq, {-1, 0, -lo});
  sq = clip(sq, {1, 0, hi});
  sq = clip(sq, {0, -1, -lo});
  sq = clip(sq, {0, 1, hi});
  if (within != nullptr) {
    // Intersect with the parent's polygon: clip by each of its edges.
    const Poly& w = *within;
    if (w.size() >= 3) {
      for (size_t k = 0; k < w.size() && !sq.empty(); ++k) {
        const Pt& p = w[k];
        const Pt& q = w[(k + 1) % w.size()];
        double ex = q.x - p.x, ey = q.y - p.y;
        double len = std::sqrt(ex * ex + ey * ey);
        if (len == 0) continue;
        double nx = ey / len, ny = -ex / len;
        sq = clip(sq, {nx, ny, nx * p.x + ny * p.y + ETA});
      }
    }
  }
  for (size_t k = 0; k < C.marks.size() && !sq.empty(); ++k) {
    if (static_cast<int>(k) == t.mark || !C.occupied[k]) continue;
    const Pt q = C.marks[k];
    double r = g.hin - ETA;
    std::vector<HP> F = {{ux, uy, ux * q.x + uy * q.y + r},
                         {-ux, -uy, -(ux * q.x + uy * q.y) + r},
                         {vx, vy, vx * q.x + vy * q.y + r},
                         {-vx, -vy, -(vx * q.x + vy * q.y) + r}};
    sq = minus_convex(sq, F);
  }
  return sq;
}

void bbox(const Tile& t, double& x0, double& x1, double& y0, double& y1) {
  x0 = y0 = 1e300;
  x1 = y1 = -1e300;
  for (const Slice& s : t.sl) {
    if (!s.alive) continue;
    for (const Pt& p : s.poly) {
      x0 = std::min(x0, p.x);
      x1 = std::max(x1, p.x);
      y0 = std::min(y0, p.y);
      y1 = std::max(y1, p.y);
    }
  }
}

bool any_alive(const Tile& t) {
  for (const Slice& s : t.sl)
    if (s.alive) return true;
  return false;
}

void touch(Tile& t, Slice& s) {
  ++t.version;
  ++s.version;
}

// Propagate R4 to a fixed point. Returns false when some tile has no live slice.
bool propagate(Ctx& C, std::vector<Tile>& T) {
  size_t n = T.size();
  for (Tile& t : T)
    for (Slice& s : t.sl)
      if (s.seen.size() != n) {
        s.seen.assign(n, -1);
        s.seen_self.assign(n, -1);
      }
  for (int round = 0; round < C.max_rounds; ++round) {
    ++C.rounds;
    bool changed = false;
    std::vector<double> bx0(n), bx1(n), by0(n), by1(n);
    for (size_t i = 0; i < n; ++i) bbox(T[i], bx0[i], bx1[i], by0[i], by1[i]);
    for (size_t i = 0; i < n; ++i) {
      for (Slice& S : T[i].sl) {
        if (!S.alive) continue;
        for (size_t j = 0; j < n && S.alive; ++j) {
          if (j == i) continue;
          if (S.seen[j] == T[j].version && S.seen_self[j] == S.version) continue;
          S.seen[j] = T[j].version;
          S.seen_self[j] = S.version;
          // Tiles whose centres are at least sqrt 2 apart cannot overlap.
          double gx = std::max({0.0, bx0[j] - bx1[i], bx0[i] - bx1[j]});
          double gy = std::max({0.0, by0[j] - by1[i], by0[i] - by1[j]});
          if (gx * gx + gy * gy >= 2.0) continue;
          std::vector<HP> F;
          for (const Slice& R : T[j].sl) {
            if (!R.alive) continue;
            double nx[8], ny[8], sup[8];
            sum_normals(S.g, R.g, nx, ny, sup);
            for (int k = 0; k < 8; ++k) {
              double mn = 1e300;
              for (const Pt& v : R.poly) mn = std::min(mn, nx[k] * v.x + ny[k] * v.y);
              F.push_back({nx[k], ny[k], sup[k] + mn - ETA});
            }
          }
          if (F.empty()) continue;
          // F as a polygon: clip a box around this slice's polygon.
          double px0 = 1e300, px1 = -1e300, py0 = 1e300, py1 = -1e300;
          for (const Pt& p : S.poly) {
            px0 = std::min(px0, p.x);
            px1 = std::max(px1, p.x);
            py0 = std::min(py0, p.y);
            py1 = std::max(py1, p.y);
          }
          Poly fp = {{px0 - 1, py0 - 1}, {px1 + 1, py0 - 1}, {px1 + 1, py1 + 1}, {px0 - 1, py1 + 1}};
          for (const HP& h : F) {
            fp = clip(fp, h);
            if (fp.empty()) break;
          }
          if (fp.size() < 3) continue;  // nothing with interior to remove
          std::vector<HP> FE;
          for (size_t k = 0; k < fp.size(); ++k) {
            const Pt& p = fp[k];
            const Pt& q = fp[(k + 1) % fp.size()];
            double ex = q.x - p.x, ey = q.y - p.y;
            double len = std::sqrt(ex * ex + ey * ey);
            if (len == 0) continue;
            double nxx = ey / len, nyy = -ex / len;  // outward for a counter-clockwise polygon
            FE.push_back({nxx, nyy, nxx * p.x + nyy * p.y - ETA});
          }
          Poly np = minus_convex(S.poly, FE);
          if (np.empty()) {
            S.alive = false;
            changed = true;
            touch(T[i], S);
            break;
          }
          if (area(np) < area(S.poly) - 1e-9) {
            S.poly = np;
            changed = true;
            touch(T[i], S);
          }
        }
      }
      if (!any_alive(T[i])) return false;
    }
    if (!changed) break;
  }
  return true;
}

bool budget(Ctx& C) {
  double el = std::chrono::duration<double>(std::chrono::steady_clock::now() - C.t0).count();
  if (C.nodes >= C.node_budget || el >= C.seconds) C.out_of_budget = true;
  return C.out_of_budget;
}

// 1 refuted, 0 undecided.
int refute(Ctx& C, std::vector<Tile> T, int depth) {
  ++C.nodes;
  C.max_depth = std::max(C.max_depth, depth);
  if (!propagate(C, T)) return 1;
  if (budget(C)) return 0;
  if (depth >= DEPTH_LIMIT) {
    C.out_of_budget = true;
    return 0;
  }
  // Choose the tile with the most freedom: centre extent, or angular extent of live slices.
  int best = -1;
  double score = -1;
  bool angle = false;
  for (size_t i = 0; i < T.size(); ++i) {
    double x0, x1, y0, y1;
    bbox(T[i], x0, x1, y0, y1);
    double lo = 1e300, hi = -1e300;
    for (const Slice& s : T[i].sl)
      if (s.alive) {
        lo = std::min(lo, s.g.lo);
        hi = std::max(hi, s.g.hi);
      }
    double span = hi - lo;
    double sc = std::max({x1 - x0, y1 - y0, 0.7 * span});
    if (sc > score) {
      score = sc;
      best = static_cast<int>(i);
      angle = 0.7 * span >= std::max(x1 - x0, y1 - y0);
    }
  }
  std::vector<Tile> A = T, B = T;
  Tile& tb = T[best];
  if (angle) {
    std::vector<size_t> live;
    for (size_t k = 0; k < tb.sl.size(); ++k)
      if (tb.sl[k].alive) live.push_back(k);
    if (live.size() >= 2) {
      size_t half = live.size() / 2;
      for (size_t k = 0; k < live.size(); ++k) {
        if (k < half)
          B[best].sl[live[k]].alive = false;
        else
          A[best].sl[live[k]].alive = false;
      }
    } else {
      // One live slice: bisect it, re-seeding each half inside the parent's polygon.
      const Slice& par = tb.sl[live[0]];
      double mid = (par.g.lo + par.g.hi) / 2;
      Slice s1, s2;
      s1.g = make_geo(par.g.lo, mid);
      s2.g = make_geo(mid, par.g.hi);
      s1.poly = seed_slice(C, tb, s1.g, &par.poly);
      s2.poly = seed_slice(C, tb, s2.g, &par.poly);
      s1.alive = !s1.poly.empty();
      s2.alive = !s2.poly.empty();
      A[best].sl = {s1};
      B[best].sl = {s2};
      A[best].sl[0].alive = s1.alive;
      B[best].sl[0].alive = s2.alive;
    }
  } else {
    double x0, x1, y0, y1;
    bbox(tb, x0, x1, y0, y1);
    bool vert = (x1 - x0) >= (y1 - y0);
    double mid = vert ? (x0 + x1) / 2 : (y0 + y1) / 2;
    HP la = vert ? HP{1, 0, mid + ETA} : HP{0, 1, mid + ETA};
    HP lb = vert ? HP{-1, 0, -mid + ETA} : HP{0, -1, -mid + ETA};
    for (size_t k = 0; k < tb.sl.size(); ++k) {
      if (!tb.sl[k].alive) continue;
      A[best].sl[k].poly = clip(tb.sl[k].poly, la);
      if (A[best].sl[k].poly.empty()) A[best].sl[k].alive = false;
      B[best].sl[k].poly = clip(tb.sl[k].poly, lb);
      if (B[best].sl[k].poly.empty()) B[best].sl[k].alive = false;
    }
  }
  for (std::vector<Tile>* X : {&A, &B}) {
    Tile& t = (*X)[best];
    ++t.version;
    for (Slice& s : t.sl) {
      ++s.version;
      s.seen.clear();
      s.seen_self.clear();
    }
  }
  // A branch whose split tile has no live slice is refuted outright.
  if (any_alive(A[best]) && refute(C, A, depth + 1) == 0) return 0;
  if (!any_alive(B[best])) return 1;
  return refute(C, B, depth + 1);
}

}  // namespace

int main() {
  Ctx C;
  int nm = 0;
  if (std::scanf("%lf %d %d %ld %lf", &C.U, &C.K, &C.max_rounds, &C.node_budget, &C.seconds) != 5)
    return 2;
  if (std::scanf("%d", &nm) != 1) return 2;
  for (int i = 0; i < nm; ++i) {
    double x, y;
    int o;
    if (std::scanf("%lf %lf %d", &x, &y, &o) != 3) return 2;
    C.marks.push_back({x, y});
    C.occupied.push_back(o);
  }
  int nt = 0;
  if (std::scanf("%d", &nt) != 1) return 2;
  std::vector<Tile> T(nt);
  for (int i = 0; i < nt; ++i)
    if (std::scanf("%d", &T[i].mark) != 1) return 2;
  // K slices over [-pi/4, pi/4], seeded by R1, R2, R3.
  for (int i = 0; i < nt; ++i) {
    T[i].sl.resize(C.K);
    for (int a = 0; a < C.K; ++a) {
      double lo = -M_PI / 4 + a * (M_PI / 2) / C.K, hi = -M_PI / 4 + (a + 1) * (M_PI / 2) / C.K;
      T[i].sl[a].g = make_geo(lo, hi);
      T[i].sl[a].poly = seed_slice(C, T[i], T[i].sl[a].g, nullptr);
      T[i].sl[a].alive = !T[i].sl[a].poly.empty();
    }
  }
  C.t0 = std::chrono::steady_clock::now();
  bool start_ok = true;
  for (const Tile& t : T)
    if (!any_alive(t)) start_ok = false;
  int r = start_ok ? refute(C, T, 0) : 1;
  double el = std::chrono::duration<double>(std::chrono::steady_clock::now() - C.t0).count();
  std::printf("%s nodes %ld rounds %ld depth %d seconds %.1f\n", r ? "REFUTED" : "UNDECIDED",
              C.nodes, C.rounds, C.max_depth, el);
  return 0;
}
