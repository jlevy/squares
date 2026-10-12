// Square geometry shared by the double, MPFR and exact (mpq) paths.
//
// Unit square i: centre c_i, angle theta_i, (C_i, S_i) = (cos theta_i, sin theta_i);
// vertices c_i + R(theta_i)(+-1/2, +-1/2).
//
// Pair separation (SAT over the 4 edge normals). With d = c_b - c_a,
//   cD = C_a C_b + S_a S_b,  sD = S_a C_b - C_a S_b   (cos and sin of the relative angle),
// the half-extent of a along its own normals is 1/2 and the half-extent of b along a's normals
// is (|cD| + |sD|)/2 (and symmetrically), so on each of the 4 axes u_k the projection gap is
//   |d . u_k| - R,   R = (1 + |cD| + |sD|) / 2,
// and   sep = max_k |d . u_k| - R.
// sep >= 0 <=> interiors disjoint (two convex polygons with disjoint interiors have a separating
// line parallel to an edge of one of them); sep < 0 => penetration depth -sep along the best axis.
//
// Containment: half-extent along x and y is e = (|C| + |S|)/2; wall slacks are
//   left = cx - e, bottom = cy - e, right = s - cx - e, top = s - cy - e.
#pragma once

#include <gmpxx.h>

#include <algorithm>
#include <array>
#include <cmath>

namespace sqv {

inline double absval(double x) { return std::fabs(x); }
inline mpq_class absval(const mpq_class& x) { return sgn(x) < 0 ? mpq_class(-x) : x; }

// M = max_k |d . u_k| and R as above; sep = M - R. Split so the certify path can dilate cheaply
// (dilating centres by f scales d, hence M, by f while R is unchanged).
template <class T>
void sat_parts(const T& ax, const T& ay, const T& Ca, const T& Sa, const T& bx, const T& by, const T& Cb,
               const T& Sb, T& M, T& R) {
  T dx = bx - ax;
  T dy = by - ay;
  M = absval(T(dx * Ca + dy * Sa));
  T p = absval(T(dy * Ca - dx * Sa));
  if (p > M) M = p;
  p = absval(T(dx * Cb + dy * Sb));
  if (p > M) M = p;
  p = absval(T(dy * Cb - dx * Sb));
  if (p > M) M = p;
  T cd = Ca * Cb + Sa * Sb;
  T sd = Sa * Cb - Ca * Sb;
  R = (T(1) + absval(cd) + absval(sd)) / 2;
}

template <class T>
T sat_sep(const T& ax, const T& ay, const T& Ca, const T& Sa, const T& bx, const T& by, const T& Cb, const T& Sb) {
  T M, R;
  sat_parts(ax, ay, Ca, Sa, bx, by, Cb, Sb, M, R);
  return M - R;
}

// Reference implementation for tests: project all 8 vertices on the 4 normals.
inline double sat_sep_bruteforce(double ax, double ay, double tha, double bx, double by, double thb) {
  auto verts = [](double cx, double cy, double th) {
    std::array<std::array<double, 2>, 4> v{};
    double c = std::cos(th), s = std::sin(th);
    const double h[4][2] = {{-0.5, -0.5}, {0.5, -0.5}, {0.5, 0.5}, {-0.5, 0.5}};
    for (int k = 0; k < 4; ++k) v[k] = {cx + c * h[k][0] - s * h[k][1], cy + s * h[k][0] + c * h[k][1]};
    return v;
  };
  auto va = verts(ax, ay, tha), vb = verts(bx, by, thb);
  const double axes[4][2] = {{std::cos(tha), std::sin(tha)},
                             {-std::sin(tha), std::cos(tha)},
                             {std::cos(thb), std::sin(thb)},
                             {-std::sin(thb), std::cos(thb)}};
  double best = -1e300;
  for (const auto& u : axes) {
    double amin = 1e300, amax = -1e300, bmin = 1e300, bmax = -1e300;
    for (int k = 0; k < 4; ++k) {
      double pa = va[k][0] * u[0] + va[k][1] * u[1];
      double pb = vb[k][0] * u[0] + vb[k][1] * u[1];
      amin = std::min(amin, pa);
      amax = std::max(amax, pa);
      bmin = std::min(bmin, pb);
      bmax = std::max(bmax, pb);
    }
    best = std::max(best, std::max(bmin - amax, amin - bmax));
  }
  return best;
}

}  // namespace sqv
