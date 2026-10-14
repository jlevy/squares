# A213 -- the K' build in integer space (PI's idea, 2026-09-14)

PI: "if all of our stuff is rational, can't we just algebraically convert everything to integer space, do the high
cost compute, and then go back to rational when the results land back on the cpu?"  Yes -- and it is bit-exact,
because every decision the library makes is the SIGN of a rational expression, and the sign of p/q with q > 0 is the
sign of the integer p.  Nothing else about the build changes: the same halfplanes, the same clips in the same order,
the same rounding, the same certification, the same shrink ladder; Fractions are rebuilt only at the boundary (the
certified vertices, the axis core), so the certificates are the library's, bit for bit (tests/, results/timing213.md).

## 1. What the library does (A132 polycore.build, A171 multibox.rebuild) and where the cost was

A211d's profile of one coarse node (902 s): `MBox.rebuild` 566 s = 63%, of which `polycore.build` per piece 329 s
(the FLOAT pipeline `_clip` 107 + `_simplify` 159 -- pure-Python loops, `_simplify` O(m^2) per build -- and the exact
`vertex_ok` on its 16 vertices), `certify_verts` 137 s and `intersect_frac` 83 s, `axis_core_pieces` 30 s,
`exactcore.exact_core` 19 s (all exact Fraction arithmetic: `Fraction._mul`, `math.gcd`, `forward` = the cost).
So the exact part is ~300 s and the float part ~270 s; both are rewritten here, both bit-exactly.

`polycore.build(box)`: (F1) clip the square [c +- 1.2]^2 by the 4 n_grid half-planes of the sampled tilts, each
offset by `shrink` (doubles); (F2) drop the smallest-area vertex while > max_v or area < 2e-8 (doubles); (F3) round
every vertex to the 1e-9 grid (`round(x * 1e9)`); (E1) the exact hull; (E2) certify every vertex with the exact
`vertex_ok` against the box and [t0, t1] = [t_lo(th0), t_hi(th1)] (k/2^24); retry with the next shrink.
`multibox.pieces_poly(pieces)`: (E3) the exact intersection of the per-piece polygons (`intersect_frac`: Sutherland-
Hodgman clips by each edge line, `_simplify_frac` to 28 then 16 vertices); (E4) shrink about the centroid by 0, 1e-8,
1e-6, 1e-4, 1e-3, round half-even to the 1e-9 grid, re-hull, and (E5) certify every vertex against EVERY piece box.
`axis_core_pieces`: (E6) the largest square about the rounded centroid, floor to 1/2^28, its corners certified (E5).

## 2. The representation

* A rational point is a homogeneous integer triple (X, Y, W), W > 0, meaning (X/W, Y/W).  A line is (a, b, c)
  meaning a x + b y + c = 0.  join(p, q) = p x q, meet(l, m) = l x m (3-vectors cross products); a new point is
  gcd-normalised (one `math.gcd` per new vertex, where Fractions do one per arithmetic operation).
* A piece box is compiled ONCE (`polycore_int.IBox`): its four corners over one common denominator CW (the corners
  are floats -> dyadic; CW = 2^k, k <= 53), the tilt interval as T0, T1 over E = 2^24 (caselp.TDEN), and the products
  T0^2, T0 E, E^2 the tests reuse.  Vertices of a build sit on the 1/VDEN grid, VDEN = 10^9 < 2^30.
* `vertex_ok` (the certification).  With u = (X CW - CX W)/(W CW), w likewise, S = 2 W CW > 0, the library's
  quadratics  P1 = (1/2 + u) t^2 - 2 w t + (1/2 - u),  P2 = (1/2 - u) t^2 + 2 w t + (1/2 + u)  become
      S P1 = (W CW + 2U) t^2 - 4V t + (W CW - 2U),   S P2 = (W CW - 2U) t^2 + 4V t + (W CW + 2U)
  with U = X CW - CX W, V = Y CW - CY W integers -- and `_quad_nonneg(A, B, C, t0, t1)` is decided exactly as the
  library decides it:  A T0^2 + B T0 E + C E^2 >= 0  (the value at t0 times E^2),  the same at t1,  and when A > 0
  and  2 A T0 <= -B E <= 2 A T1  (the interior minimum, times E)  the discriminant  4AC - B^2 >= 0.  Every inequality
  of the library is multiplied through by a POSITIVE integer, so every truth value is the same.
* The polygon chain (E3, E4): the clip line of edge (A, B) of a ccw polygon is (NX, NY, NB) = (nx1 AW, ny1 AW,
  nx1 AX + ny1 AY) with nx1 = BY AW - AY BW, ny1 = AX BW - BX AW -- a positive multiple (AW^2 BW) of the library's
  (by - ay, -(bx - ax), n.a); the signed distance of (X, Y, W) is NX X + NY Y - NB W (a positive multiple of the
  library's dp), the crossing point is meet(join(p, q), (NX, NY, -NB)) = the SAME rational point the library's
  `p + t (q - p)`, t = dp/(dp - dq) produces (both are the intersection of the two lines).  `_simplify_frac`'s
  triangle area |cross(a, b, c)| is |det[a; b; c]| / (AW BW CW): the FIRST minimal one is found by cross-multiplied
  comparison (`n_i d_j < n_j d_i`, strict, first index kept).  The centroid shrink-and-round: x' = cx sh + x (1 - sh)
  as one integer numerator over n L Sd W (L = lcm of the W's), rounded half-to-even exactly as `Fraction.__round__`.
* The axis core (E6): the centroid rounding, the slack / support ratio (a = min over edges of SL Q / (den SUP), compared
  cross-multiplied), floor to 1/aden, the four corners over den aden Q with Q = TD^2 + TM^2 (cos, sin of tm as
  (TD^2 - TM^2, 2 TM TD)/Q), certified by the same `vertex_ok_h`; the 0.999999 retries as integer floor divisions.
* The float pipeline (F1-F3) is NOT converted -- its results are doubles by definition of the library, and the
  certificates depend on them.  It is re-issued operation for operation in numpy (`polycore_fast`): the signed
  distances of all vertices in one expression (numpy's multiply / add loops are the same binary64 operations as
  CPython's; no fused multiply-add), the <= 2 crossing points by the library's own scalar formula on the very same
  doubles, the output in the library's order; the simplify with the triangle areas kept in a heap of (area, original
  index) -- an area depends only on its three vertices, so a pop changes exactly two; the current list keeps the
  original order, so the smallest original index among equal areas IS the library's first-index argmin.

## 3. The bit bound (Python ints; what a fixed-width kernel must prove)

Inputs: |X|, |Y| < 2^34 over W <= VDEN < 2^30 (vertices of a build); CW <= 2^53, |CX|, |CY| < 2^56 (corner floats in
[0.5, 4)); T0, T1 < 2^25 over E = 2^24.  Then W CW < 2^83, |U|, |V| < 2^34 2^53 + 2^56 2^30 < 2^88, so the
coefficients A, B, C < 2^90:  the endpoint value A T0^2 + B T0 E + C E^2 < 3 2^90 2^50 < 2^142;  the interior test
2 A T0 and B E < 2^116;  the discriminant 4AC - B^2 < 2^183.  (Vertices with larger W -- the axis-core corners over
den aden Q < 2^30 2^28 2^52, the exactcore corners -- push these up by the extra bits of W; Python ints do not care.)
A two-limb int64 (126 bits) does not hold the endpoint value or the discriminant; __int128 does not either.  A C
kernel needs 192-bit accumulation (three 64-bit limbs) for the two larger tests, or the float filter of Phase 2 in
front of a bignum fallback.  In the polygon chain the sizes are intrinsic (the same rationals Fractions hold);
gcd-normalising each new vertex keeps them at the Fraction sizes.

## 4. Soundness

Nothing here is a new lemma.  Integer exactness: every integer computed is the exact value of a polynomial in the
inputs (Python ints are unbounded); every comparison the library makes on rationals p/q, q > 0, is made here on
p q' vs p' q (or p vs 0) with positive multipliers -- the same truth value.  The boundary conversion Fr(X, W) is the
library's rational (Fraction normalises).  The float pipeline is unchanged (the same IEEE-754 operations in the same
order, verified by the replay on 3,000+ builds and by the fuzz).  So the polygon certified, the shrink that certified
it, the core and its `k_info` are the library's: the certificates cite the same verts and the same a.  The
differential tests (tests/replay213.py on every rebuild of the recorded A211d-style run, tests/fuzz213.py) assert
exactly that -- and A213_VERIFY=1 keeps asserting it live, call by call, in any run.

## 5. Phase 2 -- the vectorised certification (polycore_vec)

Certifying nv vertices against N pieces is nv N 16 independent sign tests of the same three polynomials.  (a) FLOAT
FILTER: evaluate them in binary64 over (nv, N, 4) arrays with a rigorous forward error bound per element (the vertex is
correctly rounded, the corners and t0, t1 are exact doubles; the bound is the propagated input error plus one epsilon
per rounding on the magnitude sum, coded in `_quad_ok_f`), take the sign only where |value| > bound, and send every
(vertex, box) pair with an undecided test to the exact integer path.  Bit-exact by construction; the filter only
chooses who pays for exact arithmetic (results/timing213.md: fallbacks are a few per thousand pairs).  (b) OBJECT
DTYPE: the integer formulas on numpy object arrays -- exact, no bound, but no early exit and one bignum op per element
per step; measured slower than the scalar integer path.  Two-limb int64 cannot represent the tests (s.3).

## 6. Phase 3 -- a C kernel (design note; no compiler on this machine)

What it would add: the scalar integer path spends ~1 us per quadratic test in Python (interpreter + bignum objects);
a C loop over the same (vertex, box) pairs is ~10-20 ns per test with fixed-width arithmetic -- the certification and
the float pipeline's clip / simplify would drop below the JSON I/O.  Overflow bound it must prove (s.3): endpoint value
< 2^142, discriminant < 2^183 for grid vertices -- so `__int128` (GCC / Clang on x86-64; MSVC has no __int128, only
`_mul128` / `_umul128` for a 64x64 -> 128 product) holds the interior test and the U, V, A, B, C coefficients but NOT
the two larger tests.  Options: (i) a 3-limb (192-bit) signed accumulate written with `_mul128`-style primitives, or
(ii) the Phase-2 float filter in C (double + the same error bound) with a bignum fallback only on the undecided pairs
(GMP `mpz`, or hand back to Python).  (ii) is the one to build: it is ~all of the gain, and its soundness argument is
already written above.  Install (one line, PI's choice): MSYS2's mingw-w64 GCC -- `winget install MSYS2.MSYS2` then
`pacman -S mingw-w64-ucrt-x86_64-gcc` -- or LLVM `winget install LLVM.LLVM` (clang, __int128 available), and build
the kernel as a plain DLL loaded with ctypes (no build system, no Python headers needed); Visual Studio Build Tools
(`winget install Microsoft.VisualStudio.2022.BuildTools`) work too but lack __int128.
