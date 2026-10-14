# A213 -- INTEGER-SPACE POLYCORE: the core-polygon build without Fractions (PI, 2026-09-14 11:30). Fable. LAUNCH-AND-EXIT.

PI: "if all of our stuff is rational, can't we just algebraically convert everything to integer space, do the high cost
compute, and then go back to rational when the results land back on the cpu?" and "could we also get a material
speedup by kicking the math out to a library in a different language?"
A211d's profile: 67% of a coarse-tree run is MBox.rebuild -> polycore.build / vertex_ok / _quad_nonneg / _simplify /
_tri_area on Python Fractions (Fraction._mul, math.gcd, _from_coprime_ints, forward = the cost); 810 rebuilds x 1.2 s.

Ops (binding): short responses, files <= 250 lines, no monitors, no waiting turns: build, differential-test, measure,
commit, report, EXIT.  Explicit-pathspec commits; fetch + plain merge; no pull --rebase / reset; no recursive deletes;
PYTHONDONTWRITEBYTECODE=1; 1-2 processes, BLAS pinned, BelowNormal via A210's working fix; never touch the running
workers (A211 p2a/p2b, A212, k0), never edit the READ-ONLY libraries (A132 polycore.py, A171 multibox.py, A135
exactcore, A131 pinclip): write NEW modules and wire them through a patch module (the mbpatch178 pattern) that A211's
coarse211 can `install`.  Machine: Python 3.14, numpy 2.5; NO C compiler installed (no gcc/clang/cl) -- say in the
report what a compiler would add and which one to install.

## Phase 1 -- pure-Python integer space (bit-exact)
1. Every input of a core build (piece rect, tilt sub-bin as t = tan(theta/2) endpoints, the container side, shrink) is a
   rational with a denominator dividing D = 250000 * 2^k * (the t-grid denominator); take the common denominator ONCE
   per build and represent every coordinate as a Python int numerator over D (no gcd, no normalisation).  The halfplane
   normals, clips, vertex certification (`vertex_ok`: quadratic nonnegativity of A t^2 + B t + C on [t0, t1]) and the
   area/simplify tests are polynomials of bounded degree in these integers: implement them as integer sign tests
   (degree-2 in t, degree <= 4 in the coordinates), with the exact bit bound written down (input bits -> product bits).
2. Convert back to Fractions only at the boundary (the PolyCore vertices and the Core returned to multibox), so the
   certificates are UNCHANGED bit for bit.  Differential test: replay every rebuild of A211d's profile run (the caches
   record the piece sets: fastclip211 / logs/profile) through both builds and assert identical vertices, cores and
   k_info; plus a fuzz of random boxes / tilt bins.
3. Measure: rebuild time per call before / after on the replayed set; then the coarse tree's Y0202 pad-0 900 s run
   (isolated dirs as A211d) with the same stage table.
## Phase 2 -- vectorise the hot loop
Vertex certification against N pieces is N independent sign tests of the same polynomials: batch them in numpy with a
two-limb int64 representation (hi/lo, or object dtype where the bit bound exceeds 63 bits -- measure both), keeping
the Python-int path as the reference (differential test on the same replay).  Report the per-call gain.
## Phase 3 -- design note only (no build without a compiler)
What a C kernel (__int128 on x86-64 with GCC/Clang; MSVC needs _mul128) would add over Phase 2 on this loop, the
overflow bound it must prove, and the one-line install (e.g. MSYS2 mingw-w64 GCC, or LLVM) the PI would run.
## Deliverables
code/polycore_int.py (+ polycore_vec.py), code/mbpatch213.py (install into A211's coarse211 behind a flag, default ON
once the differential test passes), tests/ (replay + fuzz), notes/int_polycore.md (the representation, the bit bound,
the soundness argument = integer exactness + the boundary conversion; the PI credited), results/timing213.md (per-call
and per-run tables), registry row, LOG entry.  Report once (the bit bound, the differential test counts, the timing
tables before / after for Phase 1 and Phase 2, the compiler note, commits) and EXIT.
