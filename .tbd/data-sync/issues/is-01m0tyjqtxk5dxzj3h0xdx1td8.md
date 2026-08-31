---
type: is
id: is-01m0tyjqtxk5dxzj3h0xdx1td8
title: Correct the gate-aggregate mutation expectation semantics
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - bookkeeping
dependencies: []
parent_id: is-01m0t3n7z9fj0p7wwt1kn4nzqk
created_at: 2026-08-24T22:34:41.884Z
updated_at: 2026-08-24T22:38:52.764Z
closed_at: 2026-08-24T22:38:52.763Z
close_reason: D-204 records the reversed mutation expectation; the authoritative 12-of-204 diagnostic now matches controls.yaml. All 37 controls fire and all 30 normal-gate steps pass in 42 wall-seconds.
resolution: null
duplicate_of: null
---
The first frozen-state normal gate showed that the updated synopsis mutation control expected the mutated gate count rather than the authoritative count named by check_synopsis.py. Record as D-204, set the expected diagnostic to the actual defects.yaml aggregate, and require all 37 controls plus the normal gate to pass before push.
