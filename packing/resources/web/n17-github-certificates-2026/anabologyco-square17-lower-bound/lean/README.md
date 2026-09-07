# Lean certificate (work in progress)

Lean 4 formalization of the finite computation layer of the s(17) ≥ 4.5705 proof.
Toolchain: Lean 4.33.0, no external dependencies (mathlib not yet required).

## What is proved in Lean today

All checkers are self-contained exact `Int` computations in
`Square17/Checker.lean`, with independently derived geometry (documented
inline; cross-check `../docs/PROOF.md`). Data modules are generated from the
release data files by `scripts/gen_data.py` with pinned sha256s, and re-parsed
inside Lean by a poisoned parser (malformed input can only cause checks to
*fail*).

| Theorem | Statement | Replaces | Status |
|---|---|---|---|
| `certificate_ok` | 560 atoms on-grid, nonnegative, duplicate-free, exactly D4-symmetric, mass = 16994734834452 < 17·10¹² | `check_certificate.py` | ✅ proved |
| `theta0_coverage_ok` | every open cell of the θ=0 arrangement inside the feasible box has coverage ≥ 10¹² | `verify_endpoints.cpp` (θ=0) | ✅ proved |
| `quarter_turn_coverage_ok` | θ=π/4 audit in exact ℤ[√2]: every subthreshold run is separated from the feasible diamond | `verify_endpoints.cpp` (θ=π/4) | ✅ proved |
| `sample_subset_coverage_ok` | the audited coverage property at a 152-sample subset of the 148,937 orientations | `verify_coverage_segment.cpp` (subset) | ✅ proved |
| `sample_full_coverage_ok` | same at **all 148,937** audited orientations | `verify_coverage_segment.cpp` (full) | ✅ proved (`FullTheorem.lean`; 8.5 h single-threaded `native_decide` build, measured on a 4-core EPYC-Milan VM) |

Build the default target (fast, includes the first four theorems; ~30 s):

```bash
lake build Square17
```

**Do not remove `precompileModules` from the lakefile.** `native_decide` only
calls natively compiled code for modules built into shared libraries; without
that setting the checkers run in Lean's interpreter at roughly 100× slower
(the full-set theorem goes from 8.5 hours, measured, to months of CPU, and
even the default target takes an hour). This applied silently to the 4.57
release's Lean layer, whose full-set build time was estimated, not measured.

Build the full-coverage theorem (single-threaded replay of the entire audit):

```bash
lake build FullTheorem
```

`lake exe fullrun [N]` benchmarks the checker outside the kernel.

## Trust model

These theorems use `native_decide`: the kernel accepts an evaluation performed
by the compiled checker, so the trust base is the Lean kernel **plus** the Lean
compiler/runtime. This already removes the C++/Python implementations, the
OpenMP runtime, and g++ from the trust base. A later hardening step can replace
`native_decide` with a verified-checker/kernel-reduction route.

The link between the Lean data modules and the release data files is the
generator's pinned sha256 plus the internal checks (mass, symmetry, counts):
the theorems are about the embedded data, and the embedded data is pinned to
`data/atoms.csv` and `data/orientation_samples.tsv`.

## What is NOT yet formalized (the "modulo" part)

1. **Event completeness + partition layer** — that the 148,937 sampled
   orientations cover all orientations: Bernstein prefilter (1,194,331 of the
   1,344,862 raw event polynomials discarded exactly), Sturm root partition of
   the remaining 150,531 (`exact_sturm.hpp`, `verify_event_partition.cpp`),
   and the event-stability theorem in `docs/PROOF.md`. Next concrete step:
   Lean Sturm chains over `Int` polynomials and a replay of the gap partition
   (data-heavy but mechanical); the stability theorem itself is the
   research-level part.
2. **The measure argument** — from the finite audit to "no 17 unit squares in
   side < 4.5705". Needs mathlib (ℝ, geometry, a null-set translation lemma).
   Planned as a separate mathlib-dependent package so this core stays
   dependency-free.

The corresponding roadmap for the earlier 4.57 release
(`docs/LEAN_ROADMAP.md` there) applies to this layer unchanged.
