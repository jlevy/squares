---
type: is
id: is-01m35sx984y1p1kvwpw37eg38w
title: Rebase PR222 after PR221 merges into main
kind: task
status: closed
priority: 1
version: 4
delegate: codex@spud10
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-09-23T00:16:06.902Z
updated_at: 2026-09-23T02:14:18.209Z
started_at: 2026-09-23T00:16:22.594Z
closed_at: 2026-09-23T02:14:18.208Z
close_reason: Completed PR 222 base reconciliation and CI repair at be736b0ef05ac2f256691bc3ded21873ad1f2ab1. PR 221 identifiers and PR 222's stronger external bounds are preserved; DATA_REVISION and atlas exports name data commit fe5b237c750424556b40a44f8173ac403b631e71. Packing run 35809174647, certificate-page run 35809174669, and mergeability run 35809171157 all pass; GitHub reports CLEAN/MERGEABLE. The disclosed local whole-suite timeout remains in the PR body as a limitation.
resolution: null
duplicate_of: null
---
Resolve PR222 against current main after PR221 merged, preserving PR221 historical identifiers and PR222 stronger verified bounds, frozen external-source evidence, generated views and DATA_REVISION consistency. Validate the bounded affected surface and hold all pushes for root review.

## Notes

Resolved PR222 against main/PR221 in merge commit 603de81be530c0a5ae0f0cbf2c03dba786f5d0b8 and pinned/rebuilt exports in a8c5b4815927a73fa6f4c7a75f1677105db8c984. Preserved T033 and E-n011-threshold-net2880-{certificate,interval-decision,dilation-limit}; PR222 adds no T identifier and retains strict Kleddamag 31/8 plus all 20 promotions. Focused record, schema, case, release and atlas checks passed; pushed after root diff review. Hosted CI is pending under root heartbeat ownership.
