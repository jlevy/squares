---
type: is
id: is-01m5a8frn6a2fhvd9qar6v9ars
title: "PR #406 D1 fix: charge distinct retained blobs after shared history"
kind: bug
status: closed
priority: 1
version: 3
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m58dfyf99t7khbxj1th335af
hold: null
hold_until: null
created_at: 2026-10-19T14:19:13.957Z
updated_at: 2026-10-19T14:27:32.856Z
started_at: 2026-10-19T14:19:22.371Z
closed_at: 2026-10-19T14:27:32.855Z
close_reason: "Engineering fix handed off locally in e9d20e1ac84e8bedfd18e44ac6de552b6dafe316, tree 87ab4fee480960483c738dc1bd93fab8f19940ab. Shared-history committed/staged CLI regression failed twice before the fix; final sixteen focused cases pass in 4.18s, Ruff and scoped BasedPyright clean, normal hooks pass in 9.41s. Durable report and exact diff: /Users/levy/wrk/github/squares/.codex/intake-resume-20261019/406-d1-fix/report.md. This closes only the engineering child; D1 and think-dqmn remain open for coordinator-owned independent Astra follow-up and later census/full gates. No push, GitHub publication, CI dispatch, release or merge."
resolution: null
duplicate_of: null
---
Engineering fix child for local Review D finding D1 (High), report /Users/levy/wrk/github/squares/.codex/intake-resume-20261019/406-local-current-senior.md at c1e0182ba227dbb7451b876f8674a34144cb48fe. Preserve C1 selectors capture and churn/exact-copy/grandfather policy; record selected head/index retained membership and charge at least retained unique nonexempt blob bytes. Tiny real two-commit byte-cap red/green regression, scoped low-memory validation under W44 hold, local normal-hook commit only. Coordinator owns independent Astra follow-up and D1 disposition; parent think-dqmn remains open.
