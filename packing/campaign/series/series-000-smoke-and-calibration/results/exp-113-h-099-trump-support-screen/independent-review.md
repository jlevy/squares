# exp-113: Independent Protocol and Output Review

Protocol disposition: **GO.** Output review is pending the coordinator’s single frozen
producer invocation.
No target optimization, target row generation, or separate packet replay has been run by
this reviewer.

This review is tracked by `think-ez3v` under target commission `think-2rxf`, with a
commissioned window of `2026-09-06T20:45:50Z`–`2026-09-06T21:00:50Z`. The coordinator
owns Session 089 phase 7, experiment recording, hypothesis disposition, and acceptance.

## Protocol and Source Checks

The [prospective experiment](../../experiments/exp-113-h-099-trump-support-screen.md)
preserves
[H-099’s criterion](../../../../hypotheses/H-099-trump-d4-finite-support-dual.md) and
the limits established in the
[instrument review](../agenda-026/bc-254-target-readiness-independent-review.md).
The selected source is `trump11-v1`, and the engine revision is
`e70458a9c40cfab46d2f2233b0dfbb47501a4de8`. A read-only Git comparison found no
difference between that revision and the seven reviewed density implementation/test
files. The coordinator must commit the prospective protocol before the first target rows
or optimized weights and run the target from the frozen source checkout.

The protocol fixes the exact Trump D4 support, center-first sequence and conditional
dyadic extension, exact arithmetic, zero start with the negative identity active basis,
at most two solves with 64 pivots each, and a 60-second producer cap.
It separately allocates one file replay with its own 60-second cap.
Startup, teardown, and review costs are distinct from worker time.
No unchanged retry is authorized after timeout, pivot refusal, malformed output, or a
missing premise.

The reviewed source control preserves all 88 labelled preimages on 60 distinct
placements in eight orbits and has exact feasible mass eleven.
The protocol admits no new placement, direction, grid, basis, or solver.
A failed producer’s empty stdout is not a certificate.
Refusal or incomplete output remains unresolved and must not become a mathematical
negative.

The existing producer and checker are appropriate for this bounded discriminator; no
additional arrangement implementation or alternate solver is needed to test an upper
ceiling. Exact field arithmetic, source validation, scalar checks, and sequence
generation are shared.
The determinant incidence calculation and explicit D4 maps are separate, and file replay
never invokes optimization.
These are the independence limits already disclosed before execution, not an
execution-history attestation.

## Consequence Boundary

Every admitted incidence row has a certified positive-area neighborhood, so every
almost-everywhere feasible weighting on this support satisfies that row.
D4 averaging preserves feasibility and total weight, allowing one variable per orbit
without losing a feasible mass.
For a replayed nonnegative upper witness $y$,

$$
A^T y\geq m,\qquad m^Ta\leq y^TAa\leq\mathbf1^Ty=V.
$$

If $V=11$, this upper bound and the retained feasible mass-eleven average establish that
the maximal feasible mass on the specified finite support is exactly eleven.
That rejects H-099’s fixed-support claim.
It neither constructs a mass-eleven area density nor proves global packing optimality or
a global continuum-dual ceiling.

If $V>11$, even a matching feasible finite-row primal point leaves H-099 unresolved:
finite rows do not prove almost-everywhere depth.
A reported value below eleven contradicts the retained feasible control and must be
refused. These conclusions use the
[BC-242 semantics](../agenda-026/bc-242-full-size-density-proof-contract.md), without
assuming strong duality or attainment for the continuum problem.

## Output Review

Pending. The reviewer owns the one prospective separate file-checker invocation and will
run it only after the coordinator reports successful producer completion and dispatches
the packet and frozen checkout path.
If the producer fails or leaves no valid packet, the reviewer will inspect and retain
the refusal without spending the replay allowance or rerunning the producer.

No Blocker, High, Medium, or Low finding was identified in the prospective protocol.
This statement does not accept a target output that has not been independently checked.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
