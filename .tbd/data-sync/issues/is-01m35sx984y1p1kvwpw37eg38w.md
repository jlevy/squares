---
type: is
id: is-01m35sx984y1p1kvwpw37eg38w
title: Rebase PR222 after PR221 merges into main
kind: task
status: in_progress
priority: 1
version: 3
delegate: codex@spud10
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-09-23T00:16:06.902Z
updated_at: 2026-09-23T00:51:48.317Z
started_at: 2026-09-23T00:16:22.594Z
---
Resolve PR222 against current main after PR221 merged, preserving PR221 historical identifiers and PR222 stronger verified bounds, frozen external-source evidence, generated views and DATA_REVISION consistency. Validate the bounded affected surface and hold all pushes for root review.

## Notes

Resolved PR222 against main/PR221 in merge commit 603de81be530c0a5ae0f0cbf2c03dba786f5d0b8 and pinned/rebuilt exports in a8c5b4815927a73fa6f4c7a75f1677105db8c984. Preserved T033 and E-n011-threshold-net2880-{certificate,interval-decision,dilation-limit}; PR222 adds no T identifier and retains strict Kleddamag 31/8 plus all 20 promotions. Focused record, schema, case, release and atlas checks passed; pushed after root diff review. Hosted CI is pending under root heartbeat ownership.
