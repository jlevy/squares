---
type: is
id: is-01m4dj5c1eanf3jhea0vfk9m3j
title: Reuse prepared residue population while preserving all ten shard controls
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
labels: []
dependencies: []
parent_id: is-01m4dfhweng71qgnvs6ngvdbap
created_at: 2026-10-08T10:50:20.589Z
updated_at: 2026-10-08T10:50:20.589Z
---
Read-only attempt-2 triage of full checkpoint 37756689659 at a0ca63461 found repeated work in test_ten_shards_cover_the_distance_two_frame_once (12.71 seconds against 12). It invokes survey_n17_residue.main ten times; each reconstructs geometry/endpoint, enumerates all 346,104 states, computes the same survivor/features population and loads knowledge receipts before selecting a different shard. Investigate a real prepared-population fixture/API shared by the ten invocations, preserving all ten CLI, shard, partition and output assertions and the separate cold CLI control. Preserve complete partition coverage and no-duplicate checks; avoid substituting fabricated output or a global cache that ignores changed inputs.

Begin with a preregistered bounded comparison on adequate external storage and identical source/runner shape; benchmark savings and replay original mathematical assertions before declaring success. No patch, test, profile, or benchmark was performed during this triage. Paths and committed inputs are unchanged from a910a0e6 to a0ca6346; timing does not establish host cause. Files: packing/devtools/survey_n17_residue.py; packing/tests/test_survey_n17_residue.py. Keep future ownership disjoint from ongoing n17 work and retain both full-checkpoint attempt receipts and unchanged ceilings.
