---
type: is
id: is-01m5ghae83vchpwhe8aj9g8k1s
title: Preserve profile integration through upstream T-223 and T-225 releases
kind: task
status: closed
priority: 1
version: 9
delegate: upstream_integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-22T00:49:03.234Z
updated_at: 2026-10-22T09:19:51.030Z
started_at: 2026-10-22T00:49:10.707Z
closed_at: 2026-10-22T09:19:51.030Z
close_reason: "Implemented and validated in PR #578, merged as d660905ec81383d7ca89830ff23a68e1832426e5 at 2026-10-22T09:14:53Z. Accepted candidate a020a6a11: final delta 9/9, full pool 23 pass, ordinary CI 31 successes, full checkpoint 39751078588 all ten workers and aggregate passed, Reviews N/O accepted, fresh site and four PDFs built with 7333 publication checks. Historical population, coverage and Results-growth follow-ups remain open; deployment is separate."
resolution: null
duplicate_of: null
---
Resolve newly landed origin/main d7923b8d8 conflicts after the button fix. Preserve upstream adoption and release history, reconcile profile identity joins and shared resource descriptions, regenerate URL/data views, validate, and keep PR578 reviewable without merging it.

## Notes

Current integration: main7359fa8b6 merged as b6e062d61; data pin0755e2fe9; UI b3646ac72; test corrections14340216b. Preview rebuilt:7333checks,696HTMLpages,zero broken profile targets/labels,4PDFs/50profileannotations. Broad pushgate68/69 with19958tests passed;3obsolete expectations corrected and focused3pass42.29s. Astra accepted UI and corrections. Narrow pushgate and full skipped pool complement running; hosted CI not yet accepted. User now explicitly authorized final review then merge when ready; tracked think-18ic. Fresh fetch confirms7359fa8b6 current. Deployment separate.
