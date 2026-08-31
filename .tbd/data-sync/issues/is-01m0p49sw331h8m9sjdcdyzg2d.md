---
type: is
id: is-01m0p49sw331h8m9sjdcdyzg2d
title: "atlas: the deduplicated basin store"
kind: task
status: closed
priority: 1
version: 6
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0p4askv3n2t3je7mefnhmsd
  - type: blocks
    target: is-01m0p4bvw558bbckcqp2nw11s9
  - type: blocks
    target: is-01m0pw85tzfrdrtxjnw05hkrdp
parent_id: is-01m0p49s01h862tq6wp0dd085c
created_at: 2026-08-23T01:38:28.354Z
updated_at: 2026-08-23T19:40:14.282Z
closed_at: 2026-08-23T19:40:14.282Z
close_reason: |
  Built as sqpack/atlas.py with atlas/atlas.schema.yaml and tools/atlas_check.py on claude/packing-overnight-strategy-queue (PR #14), wired into test.sh with negative controls.

  What landed: append-only store, one file per n, deduplicated by the two-level canonical identity from think-t1s9, carrying both keys, the polished side, angle signature, contact count, quench frequency, converged frequency and first-seen seed; header carries proposals, non_converged, distinct_basins and closest_pair. Mergeable by summing frequencies, so two machines running one census need no reconciliation. Six structural invariants checked, each negative-controlled.

  Two design decisions worth keeping:

  `add()` requires `converged` rather than defaulting it. Defaulting it is exactly how a census records a sweep limit as a discovery: measured at n = 5, 11 of 12 uniform multistarts hit the quench's cap and the store recorded twelve stopping points as twelve basins with every structural check green. That measurement is what surfaced D-030. A caller that has to type the word has to know the answer.

  `closest_pair` is carried in the header so a census can say whether it came near the ~1e-11 solver floor (D-021), which is the difference between a basin count and an upper bound on one.

  SCOPE DEFERRED from the original bead text, tracked separately: algebraic degree per basin, symmetry group, and neighbour links with merge-delta. The store is the minimum viable one that unblocks the H-011 census, not the full deliverable. See the follow-up bead.
resolution: null
duplicate_of: null
---
Append-only store keyed by canonical identity, carrying both keys, exact side and algebraic degree, quench frequency under a stated start distribution, contact graph, angle signature, symmetry group, and neighbour links with merge-delta. Soft-schema artifact under the same discipline as frontier/. This is the campaign's deliverable on the search-philosophy framing: the map, with records as corollaries.
