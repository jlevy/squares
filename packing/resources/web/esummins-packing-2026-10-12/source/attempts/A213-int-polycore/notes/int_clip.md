# A213b -- the rectangle-obstacle clip in integer space (2026-09-14)

A213 moved the K' BUILD into integer space and the profile then said the node is dominated by the other half:
`multibox._clip_rect_obstacle` (A171's generalisation of A131's pin-clip) took 747 of the 955 s of the Y0202 pad-0
run.  This note does to the clip what `notes/int_polycore.md` did to the build, and by the same argument: every
decision the clip makes is the SIGN of a rational expression, and the sign of p/q with q > 0 is the sign of the
integer p.  `code/pinclip_int.py`; the library (A131 pinclip, A171 multibox) is untouched and READ-ONLY.

## 1. What the clip does, and where its cost was

`_clip_rect_obstacle(rect, obs, bn)` shrinks a rational rectangle against ONE obstacle over ONE tilt sub-bin, by
A131's four-slab bisection: test the four corners with the EXACT predicate `dead_poly`; if all four are dead the
rect is empty; otherwise, for each side whose two corners are dead, find the far edge of the dead slab by 44 float
bisection steps on the FLOAT twin `_dead_poly_f` and then CERTIFY the candidate with `dead_poly`, walking back by
1e-9 up to 4 times (`PIN._bisect_boundary`).  Convexity of the dead set turns "four corners dead" into "the slab is
dead", which is what the certificate cites.

So one clip is ~5-20 calls of the exact test and ~350 calls of the float twin, and BOTH were slow for avoidable
reasons: `dead_poly` is Fraction arithmetic (per edge two multiplications, an addition and two comparisons, each
normalising with `math.gcd`), and `_dead_poly_f` -- which never decides anything, it only steers the bisection --
re-converted the obstacle's Fractions to floats (`float(nx)`, `float(lo)`, `float(hi)` and the per-edge radius) on
EVERY call, i.e. ~4 big-integer divisions per edge per call, ~350 times per clip.

## 2. The representation

Compiled ONCE per (obstacle, tilt bin) pair (`IPair`, cached on `obs.uid` -- the A173 key, never reused):

* the obstacle K: its vertices over one common denominator VD, `(VX_i, VY_i)/VD`.  An edge normal is a difference of
  vertices, so `(NX, NY) = (nx VD, ny VD)` are integers; its support interval is a sum of products of vertices, so
  `(LO, HI) = (lo VD^2, hi VD^2)` are integers.
* the per-edge radius LOWER bound `r_k = RN/RD` is taken from the library itself (`Bin.radii(obs)`, which is where
  `_radius_lo`'s `sqrt_lo` grid lives), so no new rounding is introduced -- only its numerator and denominator.
* the tilt bin: `cos, sin` at the two endpoints as `(C0, S0)/G0` and `(C1, S1)/G1` (`caselp.cos_sin_t`, exact).
* a query centre `c = (CX, CY)/CW` (one `math.gcd` per distinct point; the four rect corners share `CW`, and the
  products that depend only on `CW` are cached per pair, so a clip pays them once).

**Family A -- K's edge normals.**  `p = n.c = PN/(VD CW)` with `PN = NX CX + NY CY`.  The library's
`p - r < hi and p + r > lo`, multiplied by `VD^2 CW RD > 0`, is exactly

        EL_k CW  <  PN EA_k  <  EU_k CW,
        EA = VD RD,   EU = HI RD + RN VD^2,   EL = LO RD - RN VD^2

(the triple is divided by its gcd once at compile time: each inequality carries EA on the left and EU or EL on the
right exactly once, so a common positive divisor cancels).

**Family B -- the square's own axes.**  `P = p_i.x - c.x = Pn/M`, `Q = Qn/M`, `M = VD CW`, `Pn = VX_i CW - CX VD`.
A131's `_m_lt_half(P, Q)` becomes, with `X = Pn C + Qn S` and `Y = Qn C - Pn S` at each endpoint,

        if Y0 >= 0 and Y1 <= 0 and (Y0 > 0 or Y1 < 0):   4 (Pn^2 + Qn^2) < M^2            (the r^2 < 1/4 branch)
        else   compare X0 G1 vs X1 G0   and test   2 X < M G   on the larger one          (the endpoint branch)

and the FOUR one-sided statements the library makes per vertex (`(swap, sign)` in `(0,1), (0,-1), (1,1), (1,-1)`)
are the SAME four numbers with signs, because `(P, Q) -> (Q, -P)` sends `(X, Y) -> (Y, -X)` and `(P, Q) ->
(-P, -Q)` sends `(X, Y) -> (-X, -Y)`:

        (0, +1): d = +Y, v = +X      (0, -1): d = -Y, v = -X
        (1, +1): d = -X, v = +Y      (1, -1): d = +X, v = -Y

so four `_m_lt_half` calls cost one vertex's worth of arithmetic instead of four.

**The float twin.**  It is not converted -- it must stay bit-for-bit the library's `_dead_poly_f`, because it
chooses which rational candidate the exact predicate is then asked about, and a different candidate would be a
different (still certified, but different) rect.  It is re-issued operation for operation on values hoisted to the
compile step: `float(nx)`, `float(ny)`, `float(lo)`, `float(hi)` and the per-edge radius
`min(|u0|+|v0|, |u1|+|v1|)/2` computed with the library's own expression on the library's own floats, and
`obs.fV`'s rows as Python float pairs (`float(np.float64)` is the identity).  The four-sign identity of family B
holds in binary64 too -- negation is exact, `fl(-a-b) = -fl(a+b)` and `fl(x-y) = -fl(y-x)` -- so the twin reuses the
same four numbers as the integer kernel and still returns what four `_m_lt_half_f` calls return, bit for bit.

**One more thing that is not arithmetic.**  `_clip_rect_obstacle` asks about the same corner up to four times.
`pinclip_int.clip_rect_obstacle` memoises the ANSWER within the call but still increments `stats["exact_calls"]` on
every ask, so the counters the certificate carries are unchanged.

## 3. The bit bound

Write `b = max bit length of VD, CW, G0, G1, RD`.  The widest integers are `PN EA` and `EU CW` (family A),
`4(Pn^2 + Qn^2)` vs `M^2` and `X G'` (family B) -- every one of them a product of at most four of those quantities
plus a few bits of slack, so everything stays below `2^(4b + 6)`.  Measured on the recorded clips of the Y0202 runs
(`tests/replay_clip213.py` reports the widths actually reached; the table is the maximum over both recordings):

| quantity | bits reached |
|---|---|
| VD (obstacle denominator: 1e-9 grid for a K' polygon, `den*aden*Q` for an exact axis core) | 30 |
| CW (rect coordinate denominator: 1e-9, the bisection grid 1/(10^9 * 1024), the container's w_min grid) | 83 |
| G0, G1 (the tilt endpoints' `1 + t^2`; the coarse tree halves t at every t-split, so G grows ~2 bits per split) | 51 |
| EA = VD RD | 79 |
| EU, EL | 110 |
| **the widest product actually formed** | **229** |

Python ints are unbounded, so this is documentation, not a constraint -- but it is what a fixed-width kernel would
have to prove.  229 bits does not fit `__int128`; a C kernel needs 4-limb (256-bit) accumulation, or the float
filter of section 5 with a bignum fallback.  Note the bound GROWS with tree depth through G (t-splits) and CW
(repeated halvings of the rect), which is exactly why the Python-int path is the right reference implementation.

## 4. Soundness

Nothing here is a new lemma; the clip's geometry, its conservatisms and its certificate are A131's and A171's.

* **Integer exactness.**  Every integer computed is the exact value of a polynomial in the inputs (Python ints do
  not overflow).  Every comparison the library makes between rationals `p/q` and `p'/q'` with `q, q' > 0` is made
  here as `p q'` vs `p' q` (or against 0) after multiplying by a POSITIVE integer, so it has the same truth value.
  The multipliers are `VD^2 CW RD` (family A), `M^2`, `M G0 G1` (family B) -- positive by construction.
* **The radii are the library's.**  `_radius_lo`'s rational lower bound (including its `sqrt_lo` grid, the one
  place the library rounds in the sound direction) is READ from `Bin.radii(obs)`, not recomputed.
* **The float twin is the library's.**  The same IEEE-754 operations on the same values in the same order; the only
  change is WHEN the conversions happen.  So the bisection proposes the same candidate, `PIN._bisect_boundary`
  (reused verbatim) walks it back the same number of times, and the rect returned is built from the same rational
  candidates.
* **Boundary.**  The clip's inputs and outputs are the library's Fractions; only the interior of the predicate is
  integers.  `stats` and the replayable `trace` are produced by the same code path, so a checker replaying a slab
  step sees exactly what it saw before.

The differential tests assert precisely this, on the run's own data and on random data:
`tests/replay_clip213.py` (every recorded clip of a real 900 s run: same rect, same `stats` delta, same value the
run recorded) and `tests/fuzz_clip213.py` (random convex rational obstacles on the 1e-9 grid and on core-like
denominators, random sub-bins after up to 11 halvings, points ON the obstacle's vertices and one ulp off them:
`dead_poly`, `_dead_poly_f` and the whole clip with its trace).  Counts in `results/timing213.md`.
`A213_VERIFY=1` keeps asserting it live, clip by clip, in any run (`mbpatch213._verified_clip`).

## 5. Phase 2 -- the float filter (rigorous, exact fallback, default OFF)

Family A is `EL CW < PN EA < EU CW` per edge and it is the first thing every point test does, so it is the place a
filter pays.  `A213_CLIPFILTER=1` evaluates `t = (fNX fCX + fNY fCY) fEA` in binary64 and compares it with the
precomputed `float(EU CW)`, `float(EL CW)`, accepting the float verdict only when

        |t - bound| > 8u ( (|fNX fCX| + |fNY fCY|) |fEA| + |bound| ),      u = 2^-53

-- a bound that dominates the six roundings on the longest path (two input conversions, two products, one sum, one
product: `gamma_6 = 6u/(1-6u)` times the sum of the term magnitudes) plus one rounding of `float(bound)` and one of
the subtraction, with margin; any non-finite value falls through.  Undecided edges go to the exact integers, so the
answer is the exact answer by construction -- the filter only chooses who pays for bignum arithmetic.

MEASURED (results/timing213.md): on the replayed clips with the (obstacle, bin) pair warm it is 0.090 ms per clip
against 0.085 ms for the plain integer path -- **no gain**, 1,498 filtered and 4,689 exact fallbacks, 0 mismatches.
Once the pair is compiled, a ~150-bit integer multiply is not slower than two `float(bigint)` conversions plus the
error bound, and family A only decides a minority of the calls on its own.  It stays DEFAULT OFF: it is a second
mechanism to audit and it buys nothing here.  (Where it WOULD pay is a C kernel, s.6: there the float path is
hardware and only the fallbacks need bignums.)

## 6. Phase 3 -- a C kernel (design note; still no compiler on this machine)

Unchanged from `notes/int_polycore.md` s.6, with one number different: the clip's widest product is 229 bits (s.3),
not 183, and it grows with depth, so a fixed-width kernel is a 4-limb accumulate or a float filter in front of a
bignum fallback -- the latter is the one to build (its soundness argument is s.5, already written).  Install, one
line, the PI's choice: `winget install MSYS2.MSYS2` then `pacman -S mingw-w64-ucrt-x86_64-gcc`, or
`winget install LLVM.LLVM`; build it as a plain DLL loaded with ctypes (no build system, no Python headers).

## 7. Credit

The PI's question ("if all of our stuff is rational, can't we just algebraically convert everything to integer
space, do the high cost compute, and then go back to rational when the results land back on the cpu?") applied a
second time, to the half of the node A213 did not touch.
