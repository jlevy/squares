---
type: is
id: is-01m5ghae83vchpwhe8aj9g8k1s
title: Preserve profile integration through upstream T-223 and T-225 releases
kind: task
status: in_progress
priority: 1
version: 4
delegate: profiles-pr-coordinator
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-22T00:49:03.234Z
updated_at: 2026-10-22T06:41:58.236Z
started_at: 2026-10-22T00:49:10.707Z
---
Resolve newly landed origin/main d7923b8d8 conflicts after the button fix. Preserve upstream adoption and release history, reconcile profile identity joins and shared resource descriptions, regenerate URL/data views, validate, and keep PR578 reviewable without merging it.

## Notes

Current merge includes fetched origin/main7359fa8b6 (#717/#718): T225 V3/C3/adoption at204/227/229/260, historicalT226–228,109new beyond-horizon rows. All six text conflicts resolved; publication history retained with proposed site0.9.0 and profile explainer0.4.16. Canonical result/sourcecoverage and73profiletests pass; current75profiles/217authoredResults/714Credits/112authoredRecords. Source snapshot measured265715597bytes; minimal254MiB cap preserves allinputs,4boundarytests pass. UIrequests tracked vg ad/jmuq/beyg/j7kn/gddk/33rl (exact sorting beadthink-vgad). Final seniorreview, mergedcommit,UIvalidation,build,pushandCI pending.
