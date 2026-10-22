---
type: is
id: is-01m5h59yzyqpx3fngankadwmn3
title: Make profile directory columns sortable
kind: task
status: closed
priority: 2
version: 4
delegate: upstream_integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-22T06:38:19.133Z
updated_at: 2026-10-22T09:19:51.001Z
started_at: 2026-10-22T06:38:26.386Z
closed_at: 2026-10-22T09:19:51.001Z
close_reason: "Implemented and validated in PR #578, merged as d660905ec81383d7ca89830ff23a68e1832426e5 at 2026-10-22T09:14:53Z. Accepted candidate a020a6a11: final delta 9/9, full pool 23 pass, ordinary CI 31 successes, full checkpoint 39751078588 all ten workers and aggregate passed, Reviews N/O accepted, fresh site and four PDFs built with 7333 publication checks. Historical population, coverage and Results-growth follow-ups remain open; deployment is separate."
resolution: null
duplicate_of: null
---
Reuse Results-page accessible table sorting for profile columns. Tally columns sort numerically by totals; names and remaining sortable fields use meaningful stable keys; preserve default surname order and empty-value behavior.
