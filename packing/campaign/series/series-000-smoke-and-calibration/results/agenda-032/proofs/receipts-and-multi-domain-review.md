# Exp139, Exp140, and Multi-Owner Domain Review

**Status, 2026-09-09:** read-only receipt and source review by the existing GPT-6 Astra
agent at extra-high reasoning.
No scientific target or test suite was run here.
Exact arithmetic below checks retained receipt values and source atom properties; it is
not a second execution of the 181-direction sweep.

## Exp139: A Feasible Conditional Cover, Above the Required Threshold

Read
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-139-exact-full-net-residual.json`
and its Exp136 source.
The receipt is complete, covers direction indices0 through180, and reports the unchanged
source mass

`M=7804903/1000000`, with `m=760979/800000`.

The minimum occurs at directions27 through32. It is below one, so the raw rounded
proposal is not a unit-demand cover on the full net.
The exact quotient is

`M/m = 31219612/3804895 ≈ 8.205117881045338`.

Its excess over the seven-core threshold is exactly `4585347/3804895`. It therefore
supplies no n=11 exclusion for the literal four-flush-unit branch.

I checked the source residual atoms directly: there are88 coalesced atoms, all weights
are nonnegative, all coordinates lie in K, horizontal reflection and diagonal reflection
preserve the exact weighted measure, and the total is M. Those two symmetries generate
D4. The mass in the closed union of the four fixed corner units is exactly zero, so
deleting obstacle atoms does not improve the normalized effective mass.

The transfer interpretation is sound, subject to the exact sweep’s recorded domain
result. D4 symmetry of the weighted measure and the four obstacles makes the181 folded
directions sufficient.
The retained net reaches45 degrees and has `D=207107/90000000`;
`B(1+D)=899996306539/900000000000<1` places each selected closed B-core strictly inside
its physical unit parent.
Actual remaining cores are strictly separated from the closed fixed unit obstacles.
Thus scaling by `1/m` gives an all-angle conditional cover for those remaining cores.
The receipt’s finite-net wording is cautious; the additional analytic symmetry/shrink
argument is what supplies this interpretation.

This is a feasible cover receipt, not an optimized full-net residual mass.
The original positive finite-direction score cannot be promoted to an exact optimum-gap
theorem, and the global arm was not replayed here.
Comparing the old global proposal with the new normalized residual mass would mix
scopes. A matching global dual lower bound is still required to certify a positive
optimum gap beyond the four-owner count.

## Exp140: The Interesting Arms Have Not Run

Read `exp-140-owner-footprint-cover.json`, its stdout, process log, and exit receipt.
It is a partial scientific result with clean process exit, not a completed four-arm
comparison.

| Arm | Result | Wall Time | Interpretation |
| --- | --- | --- | --- |
| Unrestricted | numerically converged at11.884615384615401; least surveyed mass0.9999999999999657 | 5.54s | A finite-nine-direction numerical proposal, without exact validation |
| Point | round limit60; objective11.570153761669404; least surveyed mass0.955338364468638 | 9.62s | Not a feasible settled cover; objective is not a scientific comparison result |
| Triangle | no proposal | not run | No numerical verdict |
| Endpoint | no proposal | not run | No numerical verdict |

The point arm hit the round cap, not its120-second wall deadline.
Its final round still added seven rows and found twelve violations.
The experiment stopped before both area-footprint arms; `comparison` is null.
The retained support has369 available independent sites, the nine selected orientations
include both reflected halves, and the owner footprints were built from the
full361-orientation manifest.
Those scope choices match the generic contract.

## Next Half Hour

First complete the inexpensive generic numerical comparison.
Allow the point control to use a meaningful fraction of its already-declared wall budget
by increasing the artificial60-round limit under the new protocol.
Keep support, direction subset, and footprint definitions fixed.
Resume retained rows if that interface exists; otherwise the recorded setup cost is
small. The point-extension lemma means the point-only arm cannot supply an optimum
improvement beyond one owner, so it should not indefinitely prevent the area arms from
running. If it remains unresolved, retain that status and run triangle/endpoint with
comparisons restricted to genuinely settled arms.

In parallel, finish integration controls for the four-obstacle engine.
Once they pass, a single predetermined four-reflected-m1/j0 pilot is more informative
than expanding to256 refined one-owner classes.
It uses all four proved owners and tests the residual-seven condition directly.
Keep it a bounded conditional pilot; neither that one branch nor the exact four-owner
compatibility witness establishes an exhaustive n=11 reduction.

Do not repeat Exp137 fixed-weight deletion filters: the point-only survivor results
already dominate them.
Do not enlarge support or the direction net before learning the triangle/endpoint effect
on the current matched setting.
Exp139 does not itself rule out the generic four-owner pilot: those guaranteed
footprints occupy different regions from the literal fixed unit corners, so the residual
domains are not nested simply by comparing footprint area.

## Multi-Owner Implementation Review

Reviewed `/private/tmp/squares-multi-owner-work/multi_owner_domains.py` and its test
source against `/private/tmp/n11-multiple-footprint-domain-contract.md`.

**No blocking mathematical omission found.** The implementation includes all polygon
vertex cuts and every cross-polygon segment-intersection abscissa, including
obstacle/container intersections.
Parallel and collinear edges correctly need no new isolated cut beyond existing
vertices. Exact affine sections are selected at rational slab midpoints; isolated
equality guards protect against a missing cut.
The interval union merges both overlaps and touches.
Free gaps are extended with their actual affine boundaries, and `_emit_strip` rejects a
crossing endpoint or a zero-area result.

The distinction between component closures and strict physical membership is preserved.
`centre_in_strict_multi_footprint_domain` requires the centre to be inside C and outside
every CLOSED forbidden polygon.
Consequently tangencies admitted on returned component boundaries cannot be mistaken for
strictly admissible placements.
Reflection normalizes polygons through exact convex hulls, and the default direction
list remains the full361 family for singleton weights.

The code assumes convex input polygons; its normalization takes convex hulls.
That is satisfied by the current container and Minkowski constructors.
This function should not later be presented as a general nonconvex Boolean operation.

The test source supplies the requested duplicate, containment, overlap, shared-edge,
tangent, crossing, closing-triangle, and event-side controls.
It compares strict membership with independent square/footprint SAT and includes the
fifteen-term exact inclusion-exclusion area check at three orientations.
I did not re-run those tests.

Two small follow-ups are worthwhile, neither invalidates the reviewed registered branch:

- The compatible-parent test uses `pairwise(centres)`, which checks three of the six
  parent pairs. Change that assertion to all unordered pairs.
  The explicit reflected-grid construction and separation formulas already prove
  compatibility, but the test should match the claim.
- Add a control where an obstacle contains the entire container.
  The geometry correctly returns an empty component tuple; the LP integration must treat
  an empty direction domain as having no constraints, or explicitly report that case,
  rather than inventing a zero minimum or silently declaring numerical failure.
  The current four-corner footprint branch is not shown to trigger this edge case.

Adjacent-trapezoid merging and separating mass events from geometry cuts are performance
options, not missing correctness requirements.
The first pilot should retain explicit complexity guards and cache the exact geometry
per direction.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
