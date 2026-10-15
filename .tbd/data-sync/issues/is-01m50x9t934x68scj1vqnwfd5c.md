---
type: is
id: is-01m50x9t934x68scj1vqnwfd5c
title: Retain browser failure journals and add bounded manual diagnostics
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
labels: []
dependencies: []
parent_id: is-01m50kwed71nqmh914z0mh5103
created_at: 2026-10-15T23:10:34.774Z
updated_at: 2026-10-15T23:10:34.774Z
---
PR634 run38819302541 exposed900s frontend timeout and anonymous F. Native _run enables progress only for quick/slow marker strings; custom browser -k commands lack journals. Enable accurate browser phase/node journals and immediate failed trace retention without changing test selection, worker caps or hard limits. Extend existing dispatch-only browser diagnostic entry point with fixed120s known-node and180s forwarder-module observations, DEBUGP wire logs, required Chromium and retained artifacts. Preserve default font diagnostic and keep all new diagnostic work off ordinaryPR/push triggers. Diagnose actual Linux failure before another full-run iteration.
