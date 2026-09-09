# Direct Sixth-Site Feasibility: Source Admission

**GO, 2026-09-09 19:07 UTC. H151/exp153 independent mathematical source review.** No
material source blocker remains in the frozen implementation.
No target geometry, support constraint, candidate cover, or saved-target replay has been
evaluated by this review.

## Scope

The reviewed files are `packing/devtools/wall_owner_sixth_site_feasibility.py` and
`packing/tests/test_wall_owner_sixth_site_feasibility.py`. The design authority is
`packing/cases/n11_five_dot_cover/direct-sixth-site-contract.md`; the separate exp152
source admission covers the two bound escape receipts and their closed intersection.

Final reviewed Git blobs:

- Source: `891bb3985cfbc584cb4e99e4edd2d0689c3ec104`.
- Tests: `ef5b420eae398a6946ff08c18051c8b708f42d01`.

Both were checked after the final independent run.
The change adds these two files; the reused loaders and geometry helpers remain
unchanged.

The CLI reuses clean-revision, fresh-output, and bound receipt loaders for endpoint,
wall, exp149, and exp151. It reconstructs I2 directly from those exact sources.
The complete frozen direction manifest, q, B, original D, selected tuple, world patches,
saved escapes, and source chains remain bound through those admitted loaders.
The existing replay routines validate exp149 against D and exp151 against D plus x149.
The direct support calculation then restores original D while retaining the actual
selected world patches.
Positive confirmation adds the new computed site explicitly; it does not modify exp149’s
saved escape evidence.

## Complete-Domain Premise

I independently reviewed `multi_owner_domains.vertical_decompose`. Its cuts include
every polygon vertex and isolated edge intersection.
Between adjacent cuts, all boundary orderings are fixed.
Merged occupied intervals include their boundaries; emitted free strips have positive
width and interiors contained in the strict free domain U. These interiors exhaust U
away from the finite set of vertical cut lines.
Every point of U on a cut line has a free open neighbourhood and is therefore a limit of
strip-interior points.
The finite union of the emitted polygon closures is exactly the closure of U. This is
stronger than a conservative cover and is the premise that permits an empty-site-set
conclusion.

Zero-area residual pieces can be omitted because U is open in the plane.
Boundary attainers need not themselves be strict escapes: continuity makes their
closed-core membership constraints equivalent to limits of the strict-centre
constraints. The receipt correctly identifies them as positive-area component closure
vertices.

The adapter projects every vertex of every component onto both exact unit axes.
With h=B/2 it uses `-u·p <= h-max(u·c)` and `u·p <= min(u·c)+h`, and likewise for v. The
minimum and maximum are taken globally across components with deterministic attainers.
An empty component list contributes no constraint.
No component mean substitutes for an extremum.

## Closed Geometry and Quantifiers

The local closed half-plane clipper separately handles a point and a segment and uses
exact rational edge intersections and convex hulls for an area polygon.
It never decides feasibility from area.
Tangency remains admissible.
I2 is compact and contains every feasible new site, since both replayed cores miss
original D. Each support row adds necessary and sufficient constraints for all strict
admissible centres at that direction.

An empty prefix therefore completely refutes this fixed-D-plus-one-site family without
checking the remaining directions.
A nonempty prefix is unresolved.
A nonempty region after all 361 support directions supplies its exact vertex mean; the
implementation checks that mean against I2 and every accumulated inequality.
It then runs the independent union engine at all 361 directions with exactly the four
selected patches and D plus the new site, ceiling 1023. Only complete zero deficits can
produce the positive result.
A positive confirmation deficit is an inconsistency, not another site-selection
opportunity or a family refutation.

The positive counting argument remains conditional: under the retained snapping and
four-distinct-owner premises, seven residual unit squares would require seven distinct
hits among six sites, because the contained snapped cores lie strictly inside their unit
parents. The selected owner branch and global routing gaps remain separate.
Neither old D witness masks nor D4 invariance are inherited by the new site set.

## Deadline, Checkpoint, and Invalid-Result Paths

One 240-second clock starts after loading and covers saved-escape replay, I2,
decomposition, supports, closed clipping, support checkpoints, final membership, and
positive confirmation.
There is no new clock per direction or for the candidate’s union checks.
Expiry is checked around decomposition, before terminal empty acceptance, through
union/replay calls, and after the final positive confirmation.
Late results remain partial.
Final serialization and output follow the checked decision within the 300-second
external whole-process guard and coordinator’s termination grace.

Atomic checkpoints retain each completed support direction.
They currently do not retain each confirmation direction incrementally; a cooperative
return writes the confirmation prefix, while an external kill can leave the last support
checkpoint. Before the first completed support, an external kill can leave no output.
A checkpoint is always partial/incomplete and must not be promoted merely from an empty
polygon or a count field.
Source publication and the internal clock are unchanged between checkpoints.

The one requested source correction is present and tested.
An expected `SixDotCoverError` during conflicting-escape extraction or replay now
returns invalid/inconsistent with the support rows, candidate, positive-area row, and
error preserved.
It sets the conflicting escape to null, so failed replay is not labelled
as a validated witness.
The ordinary successful conflicting-escape path retains its independently replayed
escape and also returns invalid/inconsistent.

## Synthetic Validation

Ten existing purely synthetic decomposition controls passed independently in 4.66
seconds: duplicates, overlap, containment, shared edges, tangencies, closing triangular
gaps, full cover, and samples on both sides of every boundary-order event.
No retained target configuration was evaluated by those controls.

The final independent suite passed **33 tests in 3.41 seconds**, comprising all new
feasibility tests and the predecessor screen, six-dot, and selected-cover controls.
The ten new focused controls exercise axis and oblique support signs, extrema in
different components, vacuous empty domains, point and segment retention, empty-prefix
acceptance without confirmation, a full positive path, inconsistent confirmation with
and without a replayable escape, and shared deadlines.
The predecessor controls cover the reused receipt/source binding and fixed-site replay
semantics.

The positive control uses a new candidate (17/8,2), different from its saved x149 centre
(2,2), and checks the exact derived site list, actual selected patches, all support and
confirmation indices/labels, and one support checkpoint per direction.
The final-clock control makes the 361st zero-deficit confirmation cross the deadline.
It checks the actual measured direction label, one shared deadline value, all 361
retained support and confirmation rows, and partial/incomplete terminal status.
Thus completed zero deficits cannot turn a late run into acceptance.

Sol separately reports ten focused tests in 2.46 seconds, clean Ruff format/check, and
zero BasedPyright findings over the two new files.
This review inspected the full CLI and receipt path; no target invocation or loader-only
target replay was used.

This source admission is separate from design admission and the unrun target.
T023 and the global n11 bound remain unchanged.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
