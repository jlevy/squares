# Two-Escape Sixth-Site Screen: Source Admission

**2026-09-09. Independent mathematical source review for H150/exp152.** **GO for the
frozen two-receipt screen.** No source correction is required.
This review performs no target intersection, cover, escape search, or target replay.

## Reviewed Scope and Bytes

- `packing/devtools/wall_owner_sixth_site_screen.py`: Git blob
  `1868f3df5297e93ce8a6d6c4d17ba475ee88b8d3`.
- `packing/tests/test_wall_owner_sixth_site_screen.py`: final reviewed blob
  `0cd1ce1bcdf4abcb4630343a332dcdbe9ea2488f`.
- The change consists of these two files.
  Reused endpoint, wall, selected-cover, six-dot, closed-clipping, and atomic-output
  helpers are unchanged.

The four-input CLI binds the clean current implementation revision and clean tracked
endpoint, wall, exp149, and exp151 receipt blobs.
The endpoint authority remains the retained exp143 blob.
The exp151 reader checks its implementation, endpoint and wall source chain, selected
receipt identity, exact five original sites plus x149, the four selected world polygons,
tuple and corner order, the complete 361-direction source manifest, and its consecutive
zero-prefix/first-positive-deficit receipt structure.
It checks exact area accounting, subset bounds, matching saved direction and label,
summary consistency, and a complete refutation status.
The frozen expected exp151 blob further fixes the actual seven-row prefix ending at
direction 6; the reusable parser need not separately hard-code that prefix length.

## Mathematical Admission

The first escape is independently replayed against original D and the selected owner
patches. The second is independently replayed against the augmented D plus x149 and the
same selected patches.
Both therefore supply valid D-missed closed B-cores in the selected relaxed tuple.
Each core is constructed using its own saved direction and centre, with exact rational
offsets at the frozen B.

The implementation uses the existing closed polygon intersection, then canonicalizes
with the exact convex hull.
This retains a segment or a single point.
For a nonempty intersection, the mean of the distinct vertices is checked independently
for closed membership in both cores.
Its dimension and exact vertices are retained.
No area-only test is used to decide nonemptiness.

For an empty intersection, an independent square-square separating-axis calculation must
find a strictly positive interval gap on an edge normal of either square.
Closed tangency cannot supply this certificate.
A clipping/SAT disagreement raises invalid instead of producing a negative answer.
The receipt’s separator order identifies which polygon supplies the lower projection
interval, including the reversed case.

Thus complete nonempty means only that the two retained witnesses admit a common site.
It does not prove that the reported site covers any full residual domain.
Complete empty refutes every choice of one extra site preserving D for this selected
footprint relaxation, because any such site must belong to both replayed cores.
It does not refute other six-site patterns, weighted certificates, the physical owner
tuple, or n11.

## Execution and Receipt Semantics

The internal 30-second clock starts after bound input loading and covers augmentation,
both independent replays, core construction, intersection, the terminal membership or
SAT check, and the final completion decision.
Cooperative replay expiry returns partial/incomplete with no geometry.
Expiry detected after geometry also returns partial/incomplete, retaining computed
geometry. Serialization and atomic output follow that decision and are inside the
coordinator’s 60-second external process guard.

An external kill can leave no receipt; there is no incremental checkpoint claim here.
Fresh-output and source-integrity guards are reused.
Invalid and partial runs exit 2; either complete geometric outcome exits 0. Consumers
must gate on complete status and the explicit outcome.
In a partial receipt, `summary.intersection_nonempty=false` is not evidence of
emptiness, and the static replay descriptions are not completion flags.
The complete empty outcome string `refute-empty-intersection` denotes refutation of
H150’s nonemptiness question; its exact empty polygon and positive SAT gap carry the
mathematical meaning.

## Independent Validation

The final screen, six-dot, and selected-cover synthetic suites passed independently: 23
tests in 0.99 seconds.
They cover area, segment, point and empty intersections, positive independent
separation, original-D versus augmented-D6 replay routing, cooperative expiry, exact
receipt/source/site mutation guards, and the retained canonical candidate.
Two requested controls additionally exercise distinct saved oblique directions and
expiry after geometry.
At a common synthetic centre, the axis-aligned core and the core with unit ray (3/5,4/5)
yield eight intersection vertices and that exact centre as their canonical mean.
Final expiry retains the geometry while returning partial/incomplete.
Both controls passed in the independent run.
Source and test blobs were rechecked after the run and match the final bytes listed
above. Sol independently reports ten focused tests, clean Ruff format/check, zero
BasedPyright findings, and a clean diff check.

This source admission is separate from the earlier design admission and the still-unrun
target. It authorizes only the registered frozen screen after source publication and the
parent’s required checks.
T023 and the global n11 bound remain unchanged.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
