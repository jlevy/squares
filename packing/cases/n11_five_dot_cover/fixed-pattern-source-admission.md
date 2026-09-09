# Fixed-Pattern Adapter: Source Admission

**GO for the single registered exp148 run, reviewed 2026-09-09 at 15:58 UTC.** The
stable adapter implements the declared witness bank and one-candidate discriminator
correctly.
No consequential mathematical blocker remains for a run bound to the published
exp143, exp146, and already reviewed exp147 receipts.
This review evaluates no target geometry, containment relation, witness bank, or
fixed-dot escape.

Reviewed source:
[wall_owner_fixed_pattern.py](../../devtools/wall_owner_fixed_pattern.py) and its
complete [12-control test file](../../tests/test_wall_owner_fixed_pattern.py), against
the [prospective strategy](after-wall-gain-strategy.md).
The reviewer independently ran the twelve synthetic controls using project Python 3.14:
**12 passed in 0.90 seconds**. The implementation agent additionally reports clean Ruff,
BasedPyright, and combined containment/fixed-pattern controls.

The coordinator reports exp147 completed validly with 128 relations, eight contained,
120 not contained, masks `[1,1,1,1]` and `[32768,32768,32768,32768]`, two covered
baseline tuples, zero new covered tuples, 65,534 unresolved tuples, and no impossible
class. That result selects this fallback; it does not refute direct dot coverage for any
unresolved tuple.

## Corrections Verified

The final source checks the seed deadline after each direction’s decomposition and
sampling, including an empty final decomposition.
An overdue final operation returns a partial bank before candidate selection.
A synthetic clock exercises that boundary.

A completed candidate escape is now unioned with the seed failure table.
Its useful witness remains attributable, distinct rejected counts come from the merged
bitset, and complete rejection of every tuple outside the certified set returns
`refute-expansion-by-d`. A synthetic bank with one remaining tuple verifies this path.

Both candidate construction and deficit extraction reflect the selected footprints using
`source.outer_side`, matching seed mask geometry.
A q=4 synthetic control verifies the right corner coordinates.
Additional exact (3/5,4/5) controls exercise separated and tangent owner polygons, a dot
on the closed core boundary, and a strictly exterior dot.

## Mathematical Findings

The seed stage subtracts only the five dot-hit polygons from the legal centre domain.
The 64 optional wall collisions remain label predicates.
The existing vertical decomposition supplies positive-area convex closures; the mean of
each closure’s distinct vertices is a rational interior point.
Every sample is replayed against the open container and direct closed-core dot
incidence.

Samples need not represent every owner-mask change within a dot-free component.
Completion of all nine seeds therefore produces a witness bank, not an exhaustive
arrangement census. Early complete refutation is nevertheless valid if the checked
witness products already cover every tuple outside the certified set; the receipt keeps
the checked seed prefix distinct from the nine expected seeds.

Each mask bit requires agreement between closed Minkowski collision avoidance and an
independent exact separating-axis calculation.
The latter uses the core axes and all wall edge normals.
Its support radius is h times the sum of the absolute projections of the two core axes.
Strict separation excludes contact.
Four masks define a Cartesian product of refuted label tuples; bitwise union
deduplicates overlapping products.
Empty masks add no tuple.
Any witness product meeting an already certified tuple is invalid.

The complete direction manifest is reconciled against independent exact axes and labels
before choosing the nine fixed folded-source seeds.
Candidate selection is the first base-16 tuple outside the certified and rejected sets,
with the last corner varying fastest.
Only that one candidate is attempted.

The candidate’s independent union input replaces exactly its four wall footprints and
retains their actual source references.
Each direction measures the union of four closed owner-collision polygons and five
closed dot-hit polygons, with all 511 nonempty subsets available.
All 361 zero deficits establish the finite fixed-pattern cover.
The first positive deficit triggers one exact decomposition escape, replay against the
chosen four patches and dots, and reusable mask broadcast.
A positive deficit does not establish a feasible packing.

## Input Authority and Receipts

The CLI checks the clean expected Git revision, requires a fresh output path, fixes the
retained exp143 blob, and uses the admitted wall loader for the sixteen possible
classes. The containment input is bound to its exact expected Git blob.
Its parser requires the completed no-gain status, matching endpoint and wall blobs,
implementation revision, orientation/class/corner settings, and relevant summary fields.
It derives the certified set from both Cartesian products of the masks and requires
exactly `{(0,0,0,0),(15,15,15,15)}`.

**This is a consumer of the admitted exp147 receipt, not an independent replay of its
128 relations.** The parser does not traverse the matrix or recompute its relation
counts, nor check every redundant baseline/unresolved summary field.
That is not a blocker for this frozen run: the coordinator must supply the exact
published exp147 blob whose complete matrix and counts were already inspected.
The launch and result record must preserve that binding.
General admission of a different containment receipt would require its own validation
rather than reliance on these summary checks alone.

Receipts retain rational coordinates and areas as strings, witness masks and failure
tables as hexadecimal, expected and checked seed indices, merged distinct rejection
counts, the selected candidate, completed direction rows, deficit escape, broadcast, and
source references. A successful candidate is identified by its covered status and 361
rows. The field `remaining_uncertified_labels` counts labels outside the original
two-tuple certified set and the rejection table; it must not be read as a post-success
unresolved count without removing the newly covered candidate.

Partial results and invalid inputs do not produce an accepted scientific verdict.
Some unexpected exceptions from borrowed input code can terminate without a JSON
receipt; this fails closed and is handled by the process-status protocol.

## Exact Deadline Scope

The 240-second shared internal clock begins inside `run_fixed_pattern`, after input
loading. The seed guard is 60 seconds within that clock.
The candidate checks the shared deadline before directions, inside union evaluation,
around escape extraction, and before full-net success.
The external 300-second process bound also covers input loading and publication.

`main` calls `atomic_write_json` only after `run_fixed_pattern` returns, or after a
caught exception. There are no incremental checkpoints.
A cooperative timeout can return and publish a partial receipt atomically; an external
kill before that return can leave no JSON. Preserve the exit status, elapsed time,
process log, and receipt absence.
Do not interpret a missing receipt as completed negative evidence.
No streaming writer is required for this bounded run.

## Physical Scope

The five fixed dots remain valid even when a selected wall footprint contains one of
them; such a dot is unavailable to a strict residual core.
The adapter correctly has no requirement that dots avoid all optional wall polygons.

A successful candidate excludes a conditional owner branch under the retained
four-owner, wall-footprint, strict-core, full-net, boundary, and seven-versus-five
counting premises. Global n11 still needs exhaustive owner-case disposition or a proved
selection rule routing every hypothetical packing into excluded cases.
Overlapping labels and a partial failure table do not supply that premise.
T-023 remains V3/C3; additional conditional branches do not automatically upgrade its
shared analytic proof.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
