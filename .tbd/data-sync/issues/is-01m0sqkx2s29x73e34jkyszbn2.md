---
type: is
id: is-01m0sqkx2s29x73e34jkyszbn2
title: Complete H-010's five-node contract and terminally reject the printed Figure 14 set
kind: bug
status: closed
priority: 1
version: 8
spec_path: docs/project/specs/paused/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4bxnqxb8dsv2rnqgyp0w8
created_at: 2026-08-24T11:13:45.560Z
updated_at: 2026-10-12T23:51:02.508Z
closed_at: 2026-10-06T08:23:34.303Z
close_reason: "Done: H-010 on main encodes all five nodes, and exp-016's verdict is 'rejected: the printed Figure 14 set is avoidable', with ten mutation controls (exp-016-h-010-stromquist-printed-figure14.md)."
resolution: null
duplicate_of: null
---
Validity recurrence of D-091. H-010 originally omitted the published Figure 14 unavoidability premise and then falsely described that premise as nonexistent. The source audit subsequently found the stronger fact that the printed premise is itself false (D-152): the complete contract must still name all five nodes so one decisive falsifier rejects the right claim. Acceptance: H-010 encodes Figure13 localization, representative exceptional region, same-box A1/A2/A3 forcing, printed Figure14 unavoidability, and the 3+9 count; the exact printed-set escape terminally rejects that source-faithful chain; D-091 and living summaries distinguish the omitted premise, its falsification, and H-041's separately preregistered repair.

## Notes

2026-08-24: description corrected after D-152. Do not close as a successful Figure14 certificate; close only when exp-016 rejects H-010 and the five-node contract remains visible.
