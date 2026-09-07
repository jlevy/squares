# BC-231 Slice 01 Independent Review

Verdict: **GO for the control-only implementation.** No Blocker, High, Medium, or Low
finding was identified within this slice.
This is not instrument readiness, a retained certificate verdict, completion of the
BC-230 control matrix, or acceptance of H-095.

## Scope and Evidence

W2 review for BC-231 / H-095 / `think-7mk4`, 2026-09-06, against the stable source
reported by the author at 19:28 UTC on base `c14451f5`. The review covered the
[BC-230 contract](bc-230-adaptive-core-contract.md),
[control matrix](bc-230-control-matrix.md),
[slice report](bc-231-next-phases-slice-01.md), and the complete contents of:

- [adaptive.py](../../../../../src/sqpack/fractional/adaptive.py), 184 lines
- [adaptive_interval.py](../../../../../src/sqpack/fractional/adaptive_interval.py), 106
  lines
- [test_fractional_adaptive.py](../../../../../tests/test_fractional_adaptive.py), 294
  lines

The relevant existing exact sweep, interval search, scalar certificate, and rotation
helpers were inspected where the new adapters call them.
All three new files were untracked at inspection; they were reviewed in full, not
treated as absent from a tracked diff.
No source file, shared record, bead, or Git state was changed by this review.
This review document is its only authored artifact.

## Mathematical Checks

The exact adapter’s `derive_cells` and `validate_cells` implement the frozen
`legacy-linear-v1` rule.
They check ordered half-tangents, the strict penultimate and nonstrict final fold
bracket, strictly increasing derived seams, declared endpoint mismatches, positive core
sides, and strict $B_k(1+D_k)<1$. The final seam is checked before it can leave a
folded-endpoint gap.
`owner_cell` selects the first closed upper endpoint containing the folded tangent, so
an interior seam belongs to its lower-index cell, zero to cell zero, and one to the last
cell.

The interval adapter does not call the exact cell derivation.
Its bracket test $(1+t)^2<2$ is algebraically equivalent to the contract’s $t^2+2t-1<0$,
and its rotation-based endpoint formula derives the same tangent mismatch without
reading the exact adapter’s result.
Both routines still use the same mathematical seam identity; separate implementations
are not evidence for different theorems.

Both coverage adapters retain **ordinary per-direction square coverage**. The exact
route invokes `minimum_covered_mass` separately at each $(\alpha_k,B_k)$. The interval
route’s doubled net also searches each direction separately; stripping the reflected
label’s suffix selects that direction’s original cell side.
It does not use the mass of a geometric union of two orientations, interpolate sides, or
borrow the neighboring cell’s side.
The reflected axis direction is omitted because it is the same square after a quarter
turn. The tests check all five labels of the three-direction control and their exact
lower and upper masses.

`AdaptiveCertificate` checks distinct sites, nonnegative exact weights, container
membership, complete equal-weight D4 orbits, total mass strictly below $n$, and the
axis-core method ceiling.
Explicit zero-weight orbits are subject to the same listed-site rule, as required by the
frozen presentation contract.
Their mass is counted once per distinct site.

The exact adapter rejects empty and singleton center domains before calling the legacy
polygon sweep.
This is a conservative supported-domain restriction, stated in the report;
it is not a proof that every rejected object violates a theorem premise.
The interval route also requires its directed-rounding bounds to establish a
positive-area domain.
A future decision command must preserve such refusals rather than translate them into a
negative research result.

## Direct Oracle and Boundary Checks

The direct oracle at `test_fractional_adaptive.py:106` is independent of production
clipping, reachable-span selection, and prefix-sum accumulation.
Its event coordinates include all atom entry and exit lines and the center-domain
bounding coordinates.
For each open event rectangle, it checks strict projection overlap along both rotated
axes and both container axes.
These are exactly the separating axes of the two rectangles.
With positive-area center domains, the checks characterize an intersection of their
interiors, rather than merely overlap of two bounding boxes in one frame.

The rectangle midpoint need not itself be an admissible center.
That is benign: membership of every atom is constant throughout the open event
rectangle, and the separate reachability test establishes that an admissible center
exists in that same rectangle.
Directly scoring the midpoint therefore scores that reachable cell.
The additional witness checks at `test_fractional_adaptive.py:171` transform each
production witness back to container coordinates, verify containment, and recompute its
mass by direct membership.

The boundary test at `test_fractional_adaptive.py:216` uses direct closed-square
membership for the boundary and for all two or four neighboring open cells in its two
fixtures. The chosen offsets remain within those incident cells.
Their set union and mass comparisons are valid.
This checks the stated boundary-union examples; it does not exercise a future
route-specific boundary receipt or complete P5. The author’s report makes that
distinction.

For a positive-area center domain, omitted boundary-only positions cannot lower the
minimum: nonnegative atoms covered in a nearby open cell remain covered at its closed
boundary. This reasoning does not license dropping singleton center domains, which the
new adapter explicitly refuses.

## Design and Documentation

The small adapters reuse the existing direction sweeps while keeping cell geometry
separate. No broader abstraction or arrangement engine is needed for the current
controls.
The scalar carrier inside `interval_minima` supplies atoms and mass scaling; it
does not run scalar coverage or substitute its one core side for the other cells.

The report correctly limits retained n=11, n=12, and n=17 checks to geometry, total
mass, and unchanged bytes.
It does not claim their complete coverage or retention decisions were replayed.
The new small scalar test does compare a complete small ordinary coverage decision,
which is useful evidence but does not replace P1–P3.

The closed bounded parser, independent standard-library route, pure endpoint and cover
mutations, full D4 folding controls, independently frozen T10 witness,
route-disagreement guards, and complete source replays remain BC-231 work.
Runtime type annotations and in-memory geometry equality are not substitutes for that
future serialized-input boundary.
No additional documentation correction is required for this slice’s stated claims.

## Validation and CI Status

Independent focused checks ran from `packing/` with the frozen Python 3.14 environment:

```bash
UV_CACHE_DIR=/private/tmp/squares-uv-bc231-cache uv run --frozen --all-extras --group dev python -m pytest -q tests/test_fractional_adaptive.py
UV_CACHE_DIR=/private/tmp/squares-uv-bc231-cache uv run --frozen --all-extras --group dev ruff check src/sqpack/fractional/adaptive.py src/sqpack/fractional/adaptive_interval.py tests/test_fractional_adaptive.py
UV_CACHE_DIR=/private/tmp/squares-uv-bc231-cache uv run --frozen --all-extras --group dev basedpyright src/sqpack/fractional/adaptive.py src/sqpack/fractional/adaptive_interval.py tests/test_fractional_adaptive.py
```

Results: `10 passed in 0.23s`; Ruff reported all checks passed; BasedPyright reported
zero errors, warnings, or notes.
The pytest launch also printed unrelated host startup warnings about Java and an
unwritable fnm state directory; all ten tests ran and the command exited zero.
The lint and type checks used a non-login shell.

The author’s reported `152 passed, 22 deselected` broader selection was inspected but
not rerun here. No full n=11/n=12/n=17 coverage replay, target search, whole-repository
gate, or CI-status query was performed.
The coordinator owns integration checks and PR publication.
No non-blocking changes are requested by this review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
