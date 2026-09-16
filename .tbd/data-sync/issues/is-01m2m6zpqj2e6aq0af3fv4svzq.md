---
type: is
id: is-01m2m6zpqj2e6aq0af3fv4svzq
title: "PR #180 review R1: ratchet file-level suppressions"
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m2m6y4gw224dgrwf37bgqnhd
created_at: 2026-09-16T04:18:17.969Z
updated_at: 2026-09-16T05:38:56.965Z
closed_at: 2026-09-16T05:38:56.963Z
close_reason: "Exact suppression census and negative control landed at 969f5642. The live-bead requirement is explicitly rejected for permanent accessibility suppressions: each exception names the exact rule and reason, while a permanently open issue would be false tracking."
resolution: null
duplicate_of: null
---
Add a zero-or-declared census over owned JS/TS/CSS for biome-ignore, biome-ignore-all, eslint-disable, @ts-nocheck, @ts-ignore, and @ts-expect-error. Every retained exception must name a live bead and exact rule; add a negative contract case.
