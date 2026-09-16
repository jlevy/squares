---
type: is
id: is-01m2m6z4jh56brnqfhyhgev557
title: "PR #181 addendum A3: enforce per-group probe declarations"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2m6xx00sabcq5zqkrneavd0
created_at: 2026-09-16T04:17:59.376Z
updated_at: 2026-09-16T04:17:59.376Z
---
tsconfig.packing-probes.json currently places all probe JS and d.ts files in one program, so cross-group globals are silently accepted. Enforce the group boundary or add an equivalent contract negative control.
