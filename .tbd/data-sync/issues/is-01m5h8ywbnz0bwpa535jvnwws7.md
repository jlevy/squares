---
type: is
id: is-01m5h8ywbnz0bwpa535jvnwws7
title: Make action ink alignment check portable across font rasterizers
kind: bug
status: closed
priority: 2
version: 4
delegate: upstream_integration
labels: []
dependencies: []
parent_id: is-01m5h7me41y7pa91sts7g214vg
hold: null
hold_until: null
created_at: 2026-10-22T07:42:10.291Z
updated_at: 2026-10-22T09:19:51.051Z
started_at: 2026-10-22T07:43:42.832Z
closed_at: 2026-10-22T09:19:51.051Z
close_reason: "Implemented and validated in PR #578, merged as d660905ec81383d7ca89830ff23a68e1832426e5 at 2026-10-22T09:14:53Z. Accepted candidate a020a6a11: final delta 9/9, full pool 23 pass, ordinary CI 31 successes, full checkpoint 39751078588 all ten workers and aggregate passed, Reviews N/O accepted, fresh site and four PDFs built with 7333 publication checks. Historical population, coverage and Results-growth follow-ups remain open; deployment is separate."
resolution: null
duplicate_of: null
---
Hosted frontend at02b4 failed two action-ink checks: ALL NEWS centerOffset0.140625px exceeds0.1px on Linux Chromium151, with479other tests passing. Diagnose layout versus font-rasterizer quantization; retain meaningful visible centering, icon alignment and hit-area guards. Do not blindly retry or change product styling without evidence. Use controlled offset sensitivity to establish any justified tolerance.
