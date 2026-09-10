# BC318 Adapter: Mathematical Source Admission

**Verdict, 2026-09-09:** The containment transfer, D4 transport, and tuple-count logic
are sound for the admitted frozen inputs.
Close the three bounded guards below before publishing the experiment and running target
relations. The fixes require exact comparisons and one deadline check; no additional
geometry engine or covering run is needed.

Reviewed source: [wall_owner_containment.py](../../devtools/wall_owner_containment.py)
and [its tests](../../tests/test_wall_owner_containment.py), against the
[admitted contract](wall-containment-contract.md).
Line references below identify the version inspected before these corrections.
This review ran no target relation, target transport check, wall construction, or
fixed-dot escape. Model and effort evidence belong to the coordinator’s dispatch
metadata.

**Correction checkpoint.** Sol closed all three guards before target execution.
The final synthetic suite passed 9 tests in 13.85 seconds; Ruff and BasedPyright passed.
The coordinator inspected the global half-plane predicate, both explicit baseline
identities, and the final clock check in the corrected source.
No target relation was used to establish these controls.
The review below retains the original findings and their basis.

## Required Corrections

1. **Medium: reject self-intersecting polygons.** At source line 192,
   `normalise_convex_polygon` checks consecutive turn signs, which do not prove that a
   polygon is a simple convex boundary.
   The rational vertex sequence `(0,0), (3,2), (-1,2), (2,0), (1,4)` is a
   self-intersecting star with positive shoelace area and positive consecutive turns.
   The current helper accepts it; I reproduced that result using only this synthetic
   input. This violates the admitted malformed-polygon guard and leaves the half-plane
   interpretation unsupported for accepted malformed inputs.
   After choosing counterclockwise winding, require every vertex to lie in every
   directed edge’s closed left half-plane.
   Keep the existing distinctness and positive-area checks, and add this star to the
   permanent refusal control.
   This is a validation predicate, not a request to replace the polygon by its convex
   hull.
2. **Medium: make the cross-input baseline identities explicit.** In
   `validate_transport` at line 717, the retained exp143 polygons and the wall receipt’s
   old polygons are checked within their separate families, but the contract’s equality
   between those inputs is not asserted.
   Require the normalized retained base E to equal `wall.classes[0].old_endpoint` and
   normalized S(E) to equal `wall.classes[15].old_endpoint`. Refuse a mismatch before
   target slots. This catches a mismatch in the two inputs that could otherwise survive
   their separate internal symmetry checks.
   A synthetic old-polygon mismatch is the sufficient new control; no actual wall
   containment is needed to exercise it.
3. **Medium: refuse a completed verdict after the internal deadline.** At lines
   1089–1114, the final slot and counting pass can finish after the last deadline check,
   and `run_target` still returns `status: complete`. Check the clock once after those
   operations and before constructing the completed result.
   An operation crossing the declared guard must produce the existing partial/incomplete
   disposition. A controlled synthetic clock can exercise this without sleeping or
   evaluating a target.

The first finding is an observed failing control.
The other two follow from the exact missing guard paths in the inspected source; neither
is a claim that the published exp143 or exp146 inputs are inconsistent.

## Admitted Mathematical Behavior

The driver computes `exact_containment(wall, old)` and tests every certified old vertex
against the wall polygon’s closed half-planes.
The inclusion direction is correct, boundary equality passes, and a negative cross
product retains an exact vertex/edge counterexample to that component relation.
Failed relations are not described as escaping residual cores or failed dot covers.
All 128 logical slots are evaluated in fixed family/corner/class order; impossible
classes skip only their polygon predicate.

The two families are generated from the saved E and S(E), with corner maps I, H, V, R.
The four certificate maps I, H, S, and S-after-H have the correct corner permutations,
including S’s exchange of BR and TL. They check dots and all four occupied components
together. Orientation transport uses Lr for orientation-preserving maps and L(Jr) for
reflections, resolves the canonical axis by exact lookup, retains the target source
list, and checks a bijection on all 361 orientations.
The S-induced class involution swaps marks and sends j to 7-j. These checks establish
the declared four patch-and-dot pairs; additional full-net coverage is unnecessary for
their symmetry transport.

`count_tuple_dispositions` uses the union of two Cartesian products, subtracts their
product intersection once, and keeps impossible labels outside accepted masks.
It counts baseline tuples once even if both certificate families cover them.
The first new tuple uses the declared lexicographic order and one complete certificate
family. The retained four slot indices in its witness match the family/corner/class row
order. The synthetic 175-impossible, 31-covered, 50-unresolved example exercises the
mixed-family counting trap.

`relation_sets` checks equality of the reflected corner rows and the S-induced relation
permutation. Its input is the complete list constructed by `evaluate_relations`;
incomplete execution raises before that list is passed on.
It is not being used here as an external arbitrary-matrix parser.

## Input Authority and Failure Semantics

The CLI binds itself to a clean exact revision and binds each input to its declared
clean tracked Git blob.
The exp143 blob is fixed.
The exp144 and exp145 receipt guards bind that same source and require the adopted
completed coverage summaries.
The wall loader checks exact settings, class identity and order, every required frame’s
ray/selector/index/source tuple, allowed versus empty dispositions, point and segment
dimensions, support intervals and rectangles, old endpoint identity, same-class nesting,
and summary counts. An impossible class requires a completed all-empty frame list and no
polygon.

This is consumption of previously admitted evidence.
The loader does not independently reconstruct every legal centre intersection or prove
that the stored wall polygon is their complete common intersection; the clean exp146
blob and constructor admission supply those premises.
Likewise, the adopted coverage receipts retain their prior verification authority.
Freeze the exact reviewed blob values in the prospective protocol.
Do not describe this adapter as a new independent verifier for arbitrary constructor or
coverage receipts. Recomputing those upstream targets is unnecessary for this bounded
transfer.

The existing typed deadline path writes `partial`/`incomplete` and returns a nonzero
exit; other caught input failures write `invalid`. A partial receipt does not preserve
the already computed prefix, so it supplies no completed matrix or tuple count.
Unexpected exceptions and an external kill can leave no receipt.
The coordinator must retain that absence and the process exit status as incomplete or
invalid evidence, never infer refutation from them.
Some borrowed helper errors, including `AuditError` from the frozen-input loader,
currently escape the CLI’s explicit catch list; they fail closed and cannot issue an
accepted result.
Wrapping those errors would improve the typed failure receipt but is not
an additional mathematical prerequisite for this frozen-input run.

The proposed 120-second external bound is the whole-process limit.
The 60-second internal clock starts inside `run_target`, after input loading, and checks
after controls/transport and between relation slots.
With correction 3, completion also checks that clock.
Describe it as a cooperative guard: one exact operation can cross a checkpoint, and the
external supervisor supplies the process ceiling.
Retain full process elapsed time separately from the adapter’s internal
`summary.wall_seconds`.

## Validation and Claim Scope

I ran the current target-blind test file with the project Python 3.14 interpreter: **8
passed in 4.60 seconds**. The suite covers exact inclusion, boundary and oblique
controls, malformed concavity, toy tuple counts, synthetic 128-slot execution,
impossible classes, deadline refusal, input mutations, point/segment frame receipts,
adopted source bindings, and output path refusal.
The additional star input was accepted, establishing correction
1. The implementation agent reports passing Ruff and BasedPyright; this review did not
   repeat those checks.

After the three corrections and their focused controls pass, publish the implementation
and fresh H145/exp147 protocol, then run the one bounded target.
No further mathematical design is needed before that experiment.

Any successful containment transfers a completed five-dot certificate to a smaller
residual domain. The physical implication still uses four distinct selected owners,
strict rational-core containment in each unit parent, the guaranteed wall footprint
inside its actual owner core, full-net direction coverage, closed dot incidence, and
seven pairwise disjoint residual cores.
The result counts labelled sufficient conditions, with overlap retained.
It proves neither joint owner feasibility nor exhaustive n11 exclusion.
T-023 stays V3/C3; this adapter does not independently confirm or mechanize the shared
analytic transfer.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
