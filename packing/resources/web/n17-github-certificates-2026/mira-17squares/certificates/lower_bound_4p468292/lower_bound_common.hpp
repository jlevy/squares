#pragma once

#include <algorithm>
#include <array>
#include <boost/multiprecision/cpp_int.hpp>
#include <cstdint>
#include <cstdlib>
#include <stdexcept>
#include <utility>

namespace square17lb468292 {

using i128 = __int128_t;
using i256 = boost::multiprecision::int256_t;

constexpr std::int64_t ST = (std::int64_t{1} << 40);
constexpr std::int64_t SX = 1'000'000 * ST;
constexpr std::int64_t PD = 10'000'000;
constexpr std::int64_t LNUM = 4'468'292;
constexpr std::int64_t L_SCALED = LNUM * ST;
constexpr std::int64_t CENTER_LO = 500'000 * ST;
constexpr std::int64_t CENTER_HI = (LNUM - 500'000) * ST;

struct Point { std::int64_t x, y; };

inline constexpr std::array<Point, 16> POINTS{{
    { 9633740,  9849850}, {16317845,  9829523},
    {25287879,  9446006}, {34682923,  9443212},
    { 9999997, 17580956}, {19993909, 17929744},
    {29988027, 18272588}, {35451063, 18219620},
    { 9172158, 26508741}, {14694893, 26410332},
    {24689011, 26753176}, {34682923, 27101964},
    { 9999997, 35239708}, {19395041, 35236914},
    {28365087, 34853407}, {34687946, 34687946},
}};

struct Triangle { std::uint8_t a, b, c; };

inline constexpr std::array<Triangle, 18> TRIANGLES{{
    {0,1,4}, {1,2,5}, {1,4,5}, {2,3,6}, {2,5,6}, {3,6,7},
    {4,5,9}, {4,8,9}, {5,6,10}, {5,9,10}, {6,7,11}, {6,10,11},
    {8,9,12}, {9,10,13}, {9,12,13}, {10,11,14}, {10,13,14}, {11,14,15},
}};

struct Box {
    std::int64_t x0, x1;
    std::int64_t y0, y1;
    std::int64_t t0, t1;
    std::uint16_t depth;
};

inline Box initial_box() {
    return {CENTER_LO, CENTER_HI, CENTER_LO, CENTER_HI, -ST, ST, 0};
}

inline i128 abs128(i128 x) { return x < 0 ? -x : x; }
inline i128 min4(i128 a, i128 b, i128 c, i128 d) {
    return std::min(std::min(a, b), std::min(c, d));
}
inline i128 max4(i128 a, i128 b, i128 c, i128 d) {
    return std::max(std::max(a, b), std::max(c, d));
}

inline std::int64_t min_abs_t(const Box& b) {
    if (b.t0 <= 0 && b.t1 >= 0) return 0;
    return std::min(std::llabs(b.t0), std::llabs(b.t1));
}

inline bool less_than_half_extent(std::int64_t a_num, std::int64_t u_num) {
    if (a_num < 0) return true;
    const i256 A = a_num;
    const i256 U = u_num;
    const i256 T = ST;
    const i256 X = SX;
    return 4 * A * A * (T * T + U * U) < X * X * (T + U) * (T + U);
}

inline bool box_is_infeasible(const Box& b) {
    const std::int64_t u = min_abs_t(b);
    return less_than_half_extent(b.x1, u) ||
           less_than_half_extent(L_SCALED - b.x0, u) ||
           less_than_half_extent(b.y1, u) ||
           less_than_half_extent(L_SCALED - b.y0, u);
}

inline bool point_covers_box(const Point& p, const Box& b) {
    const i128 dx0 = i128(p.x) * SX - i128(b.x1) * PD;
    const i128 dx1 = i128(p.x) * SX - i128(b.x0) * PD;
    const i128 dy0 = i128(p.y) * SX - i128(b.y1) * PD;
    const i128 dy1 = i128(p.y) * SX - i128(b.y0) * PD;

    const i128 p00 = i128(b.t0) * dy0;
    const i128 p01 = i128(b.t0) * dy1;
    const i128 p10 = i128(b.t1) * dy0;
    const i128 p11 = i128(b.t1) * dy1;
    const i128 A0 = dx0 * ST + min4(p00, p01, p10, p11);
    const i128 A1 = dx1 * ST + max4(p00, p01, p10, p11);
    const i128 MA = std::max(abs128(A0), abs128(A1));

    const std::int64_t nt0 = -b.t1;
    const std::int64_t nt1 = -b.t0;
    const i128 q00 = i128(nt0) * dx0;
    const i128 q01 = i128(nt0) * dx1;
    const i128 q10 = i128(nt1) * dx0;
    const i128 q11 = i128(nt1) * dx1;
    const i128 B0 = min4(q00, q01, q10, q11) + dy0 * ST;
    const i128 B1 = max4(q00, q01, q10, q11) + dy1 * ST;
    const i128 MB = std::max(abs128(B0), abs128(B1));

    const i256 U = min_abs_t(b);
    const i256 T = ST;
    const i256 X = SX;
    const i256 D = PD;
    const i256 rhs = (T * T + U * U) * D * D * X * X;
    return 4 * i256(MA) * i256(MA) < rhs &&
           4 * i256(MB) * i256(MB) < rhs;
}

inline int first_covering_point(const Box& b) {
    for (int i = 0; i < 16; ++i) {
        if (point_covers_box(POINTS[static_cast<std::size_t>(i)], b)) return i;
    }
    return -1;
}

inline i128 point_cross(const Point& a, const Point& b, const Point& c) {
    return i128(b.x - a.x) * i128(c.y - a.y) -
           i128(b.y - a.y) * i128(c.x - a.x);
}

inline bool triangle_edges_strict(const Triangle& tr) {
    const Point* p[3] = {&POINTS[tr.a], &POINTS[tr.b], &POINTS[tr.c]};
    for (int i = 0; i < 3; ++i) {
        for (int j = i + 1; j < 3; ++j) {
            const i128 dx = i128(p[i]->x) - p[j]->x;
            const i128 dy = i128(p[i]->y) - p[j]->y;
            if (dx * dx + dy * dy >= i128(PD) * PD) return false;
        }
    }
    return true;
}

inline i128 edge_cross_center(const Point& a, const Point& b,
                              std::int64_t qx, std::int64_t qy) {
    const i128 ex = i128(b.x - a.x);
    const i128 ey = i128(b.y - a.y);
    const i128 rx = i128(qx) * PD - i128(a.x) * SX;
    const i128 ry = i128(qy) * PD - i128(a.y) * SX;
    return ex * ry - ey * rx;
}

inline bool triangle_covers_center_box(Triangle tr, const Box& b) {
    if (point_cross(POINTS[tr.a], POINTS[tr.b], POINTS[tr.c]) < 0) {
        std::swap(tr.b, tr.c);
    }
    const std::int64_t qx[2] = {b.x0, b.x1};
    const std::int64_t qy[2] = {b.y0, b.y1};
    for (int ix = 0; ix < 2; ++ix) {
        for (int iy = 0; iy < 2; ++iy) {
            const auto x = qx[ix];
            const auto y = qy[iy];
            if (edge_cross_center(POINTS[tr.a], POINTS[tr.b], x, y) <= 0) return false;
            if (edge_cross_center(POINTS[tr.b], POINTS[tr.c], x, y) <= 0) return false;
            if (edge_cross_center(POINTS[tr.c], POINTS[tr.a], x, y) <= 0) return false;
        }
    }
    return true;
}

inline bool triangle_covers_box(std::size_t index, const Box& b) {
    const Triangle tr = TRIANGLES.at(index);
    return triangle_edges_strict(tr) && triangle_covers_center_box(tr, b);
}

inline int first_covering_triangle(const Box& b) {
    for (int i = 0; i < static_cast<int>(TRIANGLES.size()); ++i) {
        if (triangle_covers_box(static_cast<std::size_t>(i), b)) return i;
    }
    return -1;
}

inline int choose_split_dimension(const Box& b) {
    const i128 wx = i128(b.x1 - b.x0) * ST;
    const i128 wy = i128(b.y1 - b.y0) * ST;
    const i128 wt = i128(3) * (b.t1 - b.t0) * SX;
    if (wx >= wy && wx >= wt) return 0;
    if (wy >= wt) return 1;
    return 2;
}

inline std::pair<Box, Box> split_box(const Box& b, int dim) {
    Box a = b, c = b;
    a.depth = c.depth = static_cast<std::uint16_t>(b.depth + 1);
    if (dim == 0) {
        const std::int64_t m = (b.x0 + b.x1) / 2;
        if (m == b.x0 || m == b.x1) throw std::runtime_error("x grid exhausted");
        a.x1 = m; c.x0 = m;
    } else if (dim == 1) {
        const std::int64_t m = (b.y0 + b.y1) / 2;
        if (m == b.y0 || m == b.y1) throw std::runtime_error("y grid exhausted");
        a.y1 = m; c.y0 = m;
    } else if (dim == 2) {
        const std::int64_t m = (b.t0 + b.t1) / 2;
        if (m == b.t0 || m == b.t1) throw std::runtime_error("t grid exhausted");
        a.t1 = m; c.t0 = m;
    } else {
        throw std::runtime_error("invalid split dimension");
    }
    return {a, c};
}

struct Stats {
    std::uint64_t nodes = 0;
    std::uint64_t split = 0;
    std::uint64_t covered = 0;
    std::uint64_t triangle = 0;
    std::uint64_t infeasible = 0;
    std::uint16_t max_depth = 0;
    std::array<std::uint64_t, 16> point_counts{};
    std::array<std::uint64_t, 18> triangle_counts{};
};

} // namespace square17lb468292
