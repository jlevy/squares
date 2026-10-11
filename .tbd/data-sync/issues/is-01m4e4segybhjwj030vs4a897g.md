---
type: is
id: is-01m4e4segybhjwj030vs4a897g
title: "n17 issue445: release BB full-node records after complete consumption"
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@spud10.local
labels:
  - n-17
dependencies: []
parent_id: is-01m4e47f19w8w1d7tyka9raahk
hold: null
hold_until: null
created_at: 2026-10-08T16:15:52.859Z
updated_at: 2026-10-08T19:06:17.339Z
started_at: 2026-10-08T16:18:38.427Z
closed_at: 2026-10-08T19:06:17.338Z
close_reason: "Bounded BB lifetime repair captured in PR #452; regression controls, current-head required CI and independent Astra review passed. Full replay and RSS scope remain separate."
resolution: null
duplicate_of: null
---
Implement Astra-reviewed lifecycle repair in maintained standing BB verifier. Release loaded node only after its own scheduled check and all selected direct children have consumed it; count selected children in sample mode. Preserve full/sample assurance, receipt counters, structural induction, and malformed-certificate refusal. Controls cover reverse node IDs within a chunk, descendants across chunks, sampled siblings, internal children, node-local failures and malformed trees. Measure fewer live full records while preserving verdicts; no claim of constant total memory or row33 scalability because pass1 index remains tree-sized. GitHub445 user-authorized issue followthrough.

## Notes

PR #452 at 540577d3d0c7806b481aa8a203a33ae51dfb4dec captures the selected-child-aware BB node lifetime repair. Seven new controls passed in 1.20 seconds; ten existing tiny controls passed in 6.43 seconds; sixteen old/new receipts match except their timing field. A 65-node comb retains at most one full record at measured chunk boundaries, versus 32 before the repair, while all 65 checks execute. Pass-one indexing remains O(N); this does not establish constant RSS, a whole-process memory bound, giant-certificate affordability or mathematical exclusions. Packing, Pages and mergeability all passed on this head. Independent Astra controls and the final bounded source review found no blocking correctness or mathematical-predicate findings. Bounded implementation is complete; draft review/merge, RSS sampling under think-b0ef and downstream full replay remain separate. The numerical frontier and admission ledger are unchanged.
