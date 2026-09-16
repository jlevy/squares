---
type: is
id: is-01m2m6z4yhajge7d5shep5m3pt
title: "PR #181 addendum A4: align typography nullability"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m2m6xx00sabcq5zqkrneavd0
created_at: 2026-09-16T04:17:59.760Z
updated_at: 2026-09-16T04:17:59.760Z
---
Align inspect_explainer_typography/types.d.ts and its Python mirror: textContent can be null and the current str annotation can mis-key results. Preserve the runtime contract and add the narrow boundary assertion.
