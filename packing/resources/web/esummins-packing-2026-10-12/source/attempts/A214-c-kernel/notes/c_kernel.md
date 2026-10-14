# A214 -- the C kernel for the vertex certification (clang 22, installed by the PI 2026-09-14)

A213 s.6 said what to build: the Phase-2 float filter in C with an exact fallback, and the exact tests themselves in
three-limb 192-bit arithmetic so the fallback is in C too.  That is exactly what `code/ckernel214.c` is.  It is a
plain C DLL -- no Python.h, no extension module, no build system -- loaded with `ctypes`; A213's Python-int path
(`polycore_int.vertex_ok_h`) stays the reference and the fallback, and every answer of the kernel is checked against
it by `tests/diff214.py`, A213's `tests/replay213.py` (441 recorded rebuilds) and `tests/fuzz213.py`.

## 1. What is in C

One predicate: `polycore.vertex_ok(v, box, t0, t1)` -- "the square of side 1 centred at a corner of the box, at every
tilt in [t0, t1], covers v", which the library decides as 16 instances (4 corners x 2 orientations x 2 quadratics) of
`_quad_nonneg(A, B, C, t0, t1)`.  Two layers, in this order, per (vertex, box) pair:

1. **The float filter** (`filter_vertex` / `quad_ok_f` / `quad_f`), A213's `polycore_vec._quad_ok_f` ported operation
   for operation into scalar doubles.  Each of the 16 tests is evaluated in binary64 together with a rigorous
   forward error bound; the sign is taken only where `|value| > bound`.  Certainly-false short-circuits the pair
   (the vertex fails this box); anything the filter cannot decide falls through to (2).
2. **The exact test** (`a214_vertex_ok_exact` / `quad_ok_exact`), A213's integer formulation: with U = X CW - CX W,
   V = Y CW - CY W and S/2 = W CW, the two quadratics are `(WCW + 2U) t^2 - 4V t + (WCW - 2U)` and its mirror, and
   `A t^2 + B t + C >= 0 on [t0, t1]` is the two endpoint values `A T^2 + B T E + C E^2`, the interior test
   `2 A T0 <= -B E <= 2 A T1` and, when it holds, the discriminant `4AC - B^2 >= 0`.  `__int128` carries U, V, A, B,
   C and the interior test; the endpoint value and the discriminant do not fit 128 bits (A213 s.3: < 2^142 and
   < 2^183) and are accumulated in **three 64-bit limbs**, signed, two's complement (`code/i192.h`: `imul_128_64`,
   `imul_128_128`, add / sub / sign, all exact).

Entry points (all `__declspec(dllexport)`, all pure functions): `a214_vertex_ok` (filter then exact),
`a214_vertex_ok_exact`, `a214_vertex_filter` (the two layers separately, for the differential test),
`a214_cert_batch` (nv vertices x nb boxes in ONE call -- this is the one the hot path uses), `a214_box_ok`,
`a214_self_test`, `a214_counters` (coverage: quadratics decided exactly / endpoint negative / interior minimum
entered / discriminant negative / guard refusals), `a214_version`, `a214_sizeof_box`.

NOT in C: the polygon chain (`intersect_h`, `simplify_h`, `round_inward_h`) -- its integers are intrinsic (the same
rationals Fractions hold) and unbounded; and A213b's rectangle-obstacle clip, see s.5.

## 2. The error bound the filter uses (A213's, unchanged)

The inputs are exact doubles (the box corners; t0, t1 = k/2^24) or correctly rounded (the vertex, `X/W` under
CPython's correctly-rounded int division).  Write `delta = eps (2(|vx| + |vy|) + 2(|dx| + |dy|))` for the absolute
error of u = dx and w = dy (input error plus the rounding of the subtraction), `eps = 2^-53`.  Then
`A = 1/2 + u`, `C = 1/2 - u`, `B = -2w` carry `eA = delta + eps|A|`, `eC = delta + eps|C|`, `eB = 2 delta`, and for
each evaluation the propagated error plus one epsilon per rounding on the magnitude sum:

    value  P = A t^2 + B t + C            err = eA t^2 + eB |t| + eC + 5 eps (|A| t^2 + |B||t| + |C|)
    left   L = -B - 2A t0                 eL  = eB + 2 eA |t0| + 3 eps (|B| + |2A||t0|)
    right  R = 2A t1 + B                  eR  = eB + 2 eA |t1| + 3 eps (|2A||t1| + |B|)
    disc   D = 4(A C) - B^2               eD  = 4(eA|C| + eC|A| + eA eC) + (2|B|eB + eB^2) + 4 eps (4|A||C| + |B|^2)

A comparison `x >= 0` is decided only when `x > err` (true) or `x < -err` (false); otherwise the three-valued
combination (`tv_and` / `tv_or` / negation, Kleene) propagates "unknown" and the pair goes to the exact test.  The
bound is only valid with one rounding per operation, so the DLL is compiled `-ffp-contract=off -fno-fast-math`
(no FMA contraction, no reassociation).

## 3. The envelope, and the fallback protocol

The kernel is proved only inside a checked envelope, and it **never returns an answer it cannot prove**; the three
gates each fall back to A213's Python-int path (unbounded integers), which is also what the whole kernel is
differential-tested against:

| gate | condition | what happens |
|---|---|---|
| (1) load | no `build/ckernel214.dll`, another machine / ABI, self-test or struct-size mismatch | `ckernel214.AVAILABLE = False`, `install()` is a no-op, the Python path runs exactly as before |
| (2) envelope | `W, |X|, |Y|, CW, |CX|, |CY| >= 2^60`, `E, |T0|, |T1| >= 2^31`, or a coefficient `|A|, |B|, |C| >= 2^93` | the C function returns UNDECIDED; the caller runs `polycore_int.vertex_ok_h` |
| (3) model | a corner or t0 / t1 that is not an exact double | the box does not compile to a `CBox` at all; the whole call takes the Python path (the same guard `polycore_vec._compile` makes) |

Why those numbers: with `|A|, |B|, |C| < 2^93` and `T0sq, T1sq, E^2 < 2^62` the endpoint value is `< 3 . 2^155` and
the discriminant `< 2^189`, both inside signed 192 bits; the interior test `2 A T <= 2^94 . 2^31 = 2^125` is inside
`__int128`.  Real grid vertices sit far inside this (`W <= 10^9`, `CW <= 2^53`: coefficients `< 2^83`, endpoint
`< 2^142`).  The gate that actually fires in a run is the **axis core**: its corners have `W = den . aden . Q` up to
~2^110, so `axis_core_pieces` certifies its four corners in Python -- 419 of the 838 batch calls of a real 900 s
run, 0.7 s in total, not worth a wider kernel.

Nothing is edited on disk: `ckernel214.install()` rebinds `polycore_int.vertex_ok_h` and `polycore_int.certify_h`
(so `vertex_ok`, `certify_verts`, `pieces_poly`, `axis_core_pieces` and A135's `exactcore` all route through C) and
`polycore_vec.certify_verts`, in memory, and `mbpatch213.install()` calls it behind `A214_CKERNEL` (default ON).
`A214_CKERNEL=0` restores the Python-int path; `A214_VERIFY=1` asserts the kernel against it on every call.

## 4. Soundness

No new lemma.  The exact layer computes the same integers A213 computes (every product is exact inside the checked
envelope -- `i192.h` is plain schoolbook multiplication with no truncation), so its comparisons have the library's
truth values.  The float layer decides a sign only when the value exceeds a rigorous bound on its own error, so a
decision it makes is the exact decision; and the layers are ordered so that "cannot decide" always costs correctness
nothing -- it costs an exact test, and, past the envelope, a Python one.  The differential tests assert exactly this
(s.1 of `results/timing214.md`): the exact path alone, the filter alone, the full kernel, the batch, and the two
A213 test suites end to end.

## 5. The rectangle-obstacle clip: not in this kernel, and what its kernel would be

The brief's third target was A213b's `pinclip_int.py` once it landed.  It landed while this was being built, and
its numbers say clearly that it is a SEPARATE kernel, not an extension of this one:

* **Its integers are wider and they grow.**  A213b's measured bound (`notes/int_clip.md` s.3, over the recorded
  clips of the Y0202 runs) is 229 bits for the widest product -- four limbs, not the three this kernel uses -- and,
  unlike the certification's, the width is data-dependent and INCREASES with tree depth: G gains ~2 bits per
  t-split and CW per halving of the rect.  So a C clip kernel is perfectly possible (256-bit accumulation) but it
  must carry a runtime envelope guard and a Python fallback exactly like s.3 here, and the fallback would fire more
  often the deeper the tree goes.
* **Its float filter is not the way in.**  Here the filter is the whole win (it decided 160,580 of 160,580 pairs in
  a real run, s.3 of `results/timing214.md`).  A213b measured the analogous filter on the clip's family A at 0.090
  ms a clip against 0.085 ms for the plain integer path -- no gain, because the clip's float twin steers a
  bisection rather than answering one predicate.  So the clip's kernel is the INTEGER path in C, the opposite
  emphasis from this one.
* **The batch lesson transfers.**  A ctypes call costs ~1 us, a quarter of a Python-int certification; the win here
  came from `a214_cert_batch` amortising it over 192 pairs.  A clip kernel should likewise expose the inner loop
  (`dead_int` over an obstacle's edges and vertices for a whole rect, or a whole bisection step), never one sign
  test per call.

A213b's files were not touched here; the only shared surface is `mbpatch213`'s flag layer (`A214_CKERNEL`).
