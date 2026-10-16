---
type: is
id: is-01m50x9t934x68scj1vqnwfd5c
title: Retain browser failure journals and add bounded manual diagnostics
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m50kwed71nqmh914z0mh5103
hold: null
hold_until: null
created_at: 2026-10-15T23:10:34.774Z
updated_at: 2026-10-16T01:08:25.645Z
started_at: 2026-10-15T23:11:37.214Z
---
PR634 run38819302541 exposed900s frontend timeout and anonymous F. Native _run enables progress only for quick/slow marker strings; custom browser -k commands lack journals. Enable accurate browser phase/node journals and immediate failed trace retention without changing test selection, worker caps or hard limits. Extend existing dispatch-only browser diagnostic entry point with fixed120s known-node and180s forwarder-module observations, DEBUGP wire logs, required Chromium and retained artifacts. Preserve default font diagnostic and keep all new diagnostic work off ordinaryPR/push triggers. Diagnose actual Linux failure before another full-run iteration.

## Notes

2026-10-16 continuation: Maintained fixed-choice diagnostics and explicit browser progress now in PR634 heada85eb74a66c6e695faee8bc5e6c42a5cbb769a00. Linux diagnostics38823195740/38823480441 passed1/51 tests respectively, zero skips,25.871s/77.874s command wall; these observations do not identify original shared-process stall.35 diagnostic controls and19 existing controls passed; security/source review publication and ordinary current-head CI pending.
