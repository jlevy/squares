---
type: is
id: is-01m2hh8mbabpzhgym1f8zjmjeq
title: "PR #160 review D64: an imported snapshot with a huge container freezes the page"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T03:20:12.905Z
updated_at: 2026-09-15T03:32:52.892Z
closed_at: 2026-09-15T03:32:52.891Z
close_reason: "Fixed on PR #160 in 0b96e342: parsePackSnapshot refuses a container above (4 ceil(sqrt n) + 4) squares, and the kernel's broad-phase grid is capped at 512 cells with growing cells; Node tests, ordinary runs bit-identical."
resolution: null
duplicate_of: null
---
Canonical defect D64 from the 2026-09-14 stack triage (Medium). Source: #160 R15.

An imported snapshot with a huge container froze or killed the page: `parsePackSnapshot` accepted any positive finite side, and the kernel allocated a broad-phase grid of about ((side + 4) / 1.5)^2 cells per step (side 1e4: 33 ms per step; 3e4: 406 ms; 1e6: process killed).

Files: `packages/workbench/src/api/pack-api.ts` (:61-68); `packages/workbench/src/simulation/kernel.ts` (:732-738).
