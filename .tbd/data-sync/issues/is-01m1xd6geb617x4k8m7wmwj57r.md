---
type: is
id: is-01m1xd6geb617x4k8m7wmwj57r
title: "Phase 5: re-argue the sweeps tier ceiling from measurement and keep every fast check on the PR surface"
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-atlas-expansion-to-324.md
labels: []
dependencies:
  - type: blocks
    target: is-01m1xd6grg7z892j713te59san
parent_id: is-01m1xd517vezdmp4hrmvs5c8bp
created_at: 2026-09-07T07:44:20.426Z
updated_at: 2026-09-07T15:24:43.466Z
closed_at: 2026-09-07T15:24:43.453Z
close_reason: "Two measured slices: the atlas builder and grid replay pooled through the worker policy (3.75x and 3.49x, byte-identical); the atlas rebuild, the escape screen and the full grid replay deferred to the deep gate on their own measurements with sampled stand-ins on the PR surface; sweeps 57 s at the CI shape, checks predicted 138 s; suite record refreshed from its hosted reading. Commits 74879848 and 543a1f2f; benchmark record under packing/benchmarks/gate-cost-at-324."
resolution: null
duplicate_of: null
---
Split the known-best validation step by range so each part is measured on its own; census/profile/overlay steps stay at 100 cases under D4; record measurements in gate-budgets.yaml; any step leaving the PR surface earns it by its own measured cost (OR-13). Never bump a ceiling without a measurement.
