---
type: is
id: is-01m4e4segybhjwj030vs4a897g
title: "n17 issue445: release BB full-node records after complete consumption"
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@spud10.local
labels:
  - n-17
dependencies: []
parent_id: is-01m4e47f19w8w1d7tyka9raahk
hold: null
hold_until: null
created_at: 2026-10-08T16:15:52.859Z
updated_at: 2026-10-08T16:18:38.428Z
started_at: 2026-10-08T16:18:38.427Z
---
Implement Astra-reviewed lifecycle repair in maintained standing BB verifier. Release loaded node only after its own scheduled check and all selected direct children have consumed it; count selected children in sample mode. Preserve full/sample assurance, receipt counters, structural induction, and malformed-certificate refusal. Controls cover reverse node IDs within a chunk, descendants across chunks, sampled siblings, internal children, node-local failures and malformed trees. Measure fewer live full records while preserving verdicts; no claim of constant total memory or row33 scalability because pass1 index remains tree-sized. GitHub445 user-authorized issue followthrough.
