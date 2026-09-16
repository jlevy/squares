---
type: is
id: is-01m2m6zrghb5dv2vjgbzhgxfn9
title: "PR #180 addendum A1: close resolved-Biome configuration bypasses"
kind: bug
status: in_progress
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2m6y4gw224dgrwf37bgqnhd
created_at: 2026-09-16T04:18:19.792Z
updated_at: 2026-09-16T04:18:54.355Z
---
The no-overrides contract must reject root extends and nested biome.json rule relaxations, make info diagnostics blocking or pin their severities, and include a live TypeScript noFloatingPromises rejection. Tests must reproduce the published bypasses before the fix.
