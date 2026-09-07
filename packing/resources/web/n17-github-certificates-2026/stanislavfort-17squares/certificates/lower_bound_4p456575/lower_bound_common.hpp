#pragma once
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>
#include <boost/multiprecision/cpp_int.hpp>

namespace square17lb {
using i128 = __int128_t;
using i256 = boost::multiprecision::int256_t;
constexpr std::int64_t ST = (std::int64_t{1} << 40);
constexpr std::int64_t SX = 1000000 * ST;
constexpr std::int64_t L_SCALED = 4456575 * ST;
constexpr std::int64_t CENTER_LO = 500000 * ST;
constexpr std::int64_t CENTER_HI = 3956575 * ST;
constexpr std::int64_t PD = 1'000'000;
struct Point { std::int64_t x; std::int64_t y; };
inline constexpr std::array<Point, 16> POINTS{{
    { 963374,  984985}, {1581796,  985592},
    {2476851,  926473}, {3456650,  919147},
    { 995406, 1792837}, {1990669, 1796975},
    {2972834, 1793954}, {3523331, 1792554},
    { 922136, 2657284}, {1491209, 2660029},
    {2483245, 2665147}, {3456650, 2667556},
    { 999352, 3529848}, {1962693, 3518471},
    {2850255, 3462543}, {3456920, 3456650},
}};
struct Box {
    std::int64_t x0, x1;
    std::int64_t y0, y1;
    std::int64_t t0, t1;
    std::uint16_t depth;
};
inline Box initial_box() { return {CENTER_LO, CENTER_HI, CENTER_LO, CENTER_HI, -ST, ST, 0}; }
inline i128 abs128(i128 x) { return x < 0 ? -x : x; }
inline std::int64_t min_abs_t(const Box& b) {
    if (b.t0 <= 0 && b.t1 >= 0) return 0;
    const std::int64_t a = b.t0 < 0 ? -b.t0 : b.t0;
    const std::int64_t c = b.t1 < 0 ? -b.t1 : b.t1;
    return std::min(a, c);
}
inline bool less_than_half_extent(std::int64_t a_num, std::int64_t u_num) {
    if (a_num < 0) return true;
    const i256 A = a_num;
    const i256 U = u_num;
    const i256 S_t = ST;
    const i256 S_x = SX;
    const i256 lhs = 4 * A * A * (S_t * S_t + U * U);
    const i256 rhs = S_x * S_x * (S_t + U) * (S_t + U);
    return lhs < rhs;
}
inline bool box_is_infeasible(const Box& b) {
    const std::int64_t u = min_abs_t(b);
    return less_than_half_extent(b.x1, u) ||
           less_than_half_extent(L_SCALED - b.x0, u) ||
           less_than_half_extent(b.y1, u) ||
           less_than_half_extent(L_SCALED - b.y0, u);
}
inline i128 min4(i128 a, i128 b, i128 c, i128 d) { return std::min(std::min(a,b), std::min(c,d)); }
inline i128 max4(i128 a, i128 b, i128 c, i128 d) { return std::max(std::max(a,b), std::max(c,d)); }
inline bool point_covers_box(const Point& p, const Box& b) {
    const i128 dx0 = static_cast<i128>(p.x) * SX - static_cast<i128>(b.x1) * PD;
    const i128 dx1 = static_cast<i128>(p.x) * SX - static_cast<i128>(b.x0) * PD;
    const i128 dy0 = static_cast<i128>(p.y) * SX - static_cast<i128>(b.y1) * PD;
    const i128 dy1 = static_cast<i128>(p.y) * SX - static_cast<i128>(b.y0) * PD;
    const i128 p00 = static_cast<i128>(b.t0) * dy0;
    const i128 p01 = static_cast<i128>(b.t0) * dy1;
    const i128 p10 = static_cast<i128>(b.t1) * dy0;
    const i128 p11 = static_cast<i128>(b.t1) * dy1;
    const i128 tdy_lo = min4(p00,p01,p10,p11);
    const i128 tdy_hi = max4(p00,p01,p10,p11);
    const i128 A0 = dx0 * ST + tdy_lo;
    const i128 A1 = dx1 * ST + tdy_hi;
    const i128 MA = std::max(abs128(A0), abs128(A1));
    const std::int64_t nt0 = -b.t1;
    const std::int64_t nt1 = -b.t0;
    const i128 q00 = static_cast<i128>(nt0) * dx0;
    const i128 q01 = static_cast<i128>(nt0) * dx1;
    const i128 q10 = static_cast<i128>(nt1) * dx0;
    const i128 q11 = static_cast<i128>(nt1) * dx1;
    const i128 ndx_lo = min4(q00,q01,q10,q11);
    const i128 ndx_hi = max4(q00,q01,q10,q11);
    const i128 B0 = ndx_lo + dy0 * ST;
    const i128 B1 = ndx_hi + dy1 * ST;
    const i128 MB = std::max(abs128(B0), abs128(B1));
    const std::int64_t u_num = min_abs_t(b);
    const i256 U = u_num;
    const i256 S_t = ST;
    const i256 S_x = SX;
    const i256 D = PD;
    const i256 rhs = (S_t*S_t + U*U) * D*D * S_x*S_x;
    const i256 lhsA = 4 * i256(MA) * i256(MA);
    if (!(lhsA < rhs)) return false;
    const i256 lhsB = 4 * i256(MB) * i256(MB);
    return lhsB < rhs;
}
inline int first_covering_point(const Box& b) {
    for (int i=0; i<16; ++i) if (point_covers_box(POINTS[static_cast<std::size_t>(i)], b)) return i;
    return -1;
}
inline int choose_split_dimension(const Box& b) {
    const i128 wx = static_cast<i128>(b.x1 - b.x0) * ST;
    const i128 wy = static_cast<i128>(b.y1 - b.y0) * ST;
    const i128 wt = static_cast<i128>(3) * (b.t1 - b.t0) * SX;
    if (wx >= wy && wx >= wt) return 0;
    if (wy >= wt) return 1;
    return 2;
}
inline std::pair<Box,Box> split_box(const Box& b, int dim) {
    Box a=b, c=b;
    a.depth=c.depth=static_cast<std::uint16_t>(b.depth+1);
    if (dim==0) {
        const std::int64_t m=(b.x0+b.x1)/2;
        if (m==b.x0 || m==b.x1) throw std::runtime_error("x grid exhausted");
        a.x1=m; c.x0=m;
    } else if (dim==1) {
        const std::int64_t m=(b.y0+b.y1)/2;
        if (m==b.y0 || m==b.y1) throw std::runtime_error("y grid exhausted");
        a.y1=m; c.y0=m;
    } else if (dim==2) {
        const std::int64_t m=(b.t0+b.t1)/2;
        if (m==b.t0 || m==b.t1) throw std::runtime_error("t grid exhausted");
        a.t1=m; c.t0=m;
    } else throw std::runtime_error("invalid split dimension");
    return {a,c};
}
struct Stats {
    std::uint64_t nodes=0, infeasible=0, covered=0, split=0;
    std::uint16_t max_depth=0;
    std::array<std::uint64_t,16> witness_count{};
};
} // namespace square17lb
