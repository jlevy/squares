---
type: is
id: is-01m49m137apdxtdrpp6n5g74r8
title: "Gate: wire build_exact_values --check at the tier its measured cost allows"
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: claude-code@vm
labels:
  - packing
dependencies:
  - type: blocks
    target: is-01m49m1tk3gwmq69h2k876033s
parent_id: is-01m49m0enx3qf7mm1kyrra0z10
hold: null
hold_until: null
created_at: 2026-10-06T22:05:59.914Z
updated_at: 2026-10-06T22:59:48.121Z
started_at: 2026-10-06T22:55:39.411Z
closed_at: 2026-10-06T22:59:48.121Z
close_reason: build_exact_values + frontier/exact-values.json + schema + 39 tests; gate step 'exact side values register' (fast+records, 4.3 s). Commit 20818eacf.
resolution: null
duplicate_of: null
---
Measure --check wall time. Fast tier if within ceiling (OR-13/OR-17); otherwise structure+record agreement in fast and certificates in --records, with the measurement recorded.
