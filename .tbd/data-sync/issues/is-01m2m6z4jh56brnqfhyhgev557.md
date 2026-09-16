---
type: is
id: is-01m2m6z4jh56brnqfhyhgev557
title: "PR #181 addendum A3: enforce per-group probe declarations"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2m6xx00sabcq5zqkrneavd0
created_at: 2026-09-16T04:17:59.376Z
updated_at: 2026-09-16T06:53:38.946Z
closed_at: 2026-09-16T06:53:38.945Z
close_reason: "Completed at PR #181 head 7f990cbb: packing probes are type-checked per group by typecheck-probe-groups.mjs, with an isolated negative control proving foreign ambient declarations fail."
resolution: null
duplicate_of: null
---
tsconfig.packing-probes.json currently places all probe JS and d.ts files in one program, so cross-group globals are silently accepted. Enforce the group boundary or add an equivalent contract negative control.
