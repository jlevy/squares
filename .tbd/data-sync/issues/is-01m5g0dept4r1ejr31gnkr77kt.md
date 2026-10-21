---
type: is
id: is-01m5g0dept4r1ejr31gnkr77kt
title: Reconcile result overview assertions with linked profile labels
kind: task
status: closed
priority: 2
version: 4
delegate: profiles-pr-coordinator
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T19:53:36.211Z
updated_at: 2026-10-21T20:19:29.365Z
started_at: 2026-10-21T19:53:46.207Z
closed_at: 2026-10-21T20:19:29.364Z
close_reason: All original result-overview and terminology failures pass; HTMLParser credit-link assertion reviewed by Astra and passes 8.05s. Committed in 7b566ae73.
resolution: null
duplicate_of: null
---
Review retained broad-suite result-overview failures against intended linked surname and typed GitHub issue presentation; update stale assertions without weakening actual attribution or URLs. Parent owns only the result-overview test file; frontend owns case/overview/nav changes.

## Notes

Updated result-overview expectations to canonical linked person labels while preserving claim prose, math, scope, chronology, credit markup and page budgets. The full module passed 62 cases initially; four remaining chain cases were repaired and passed focused reruns. Final T-056 passed in 20.61 seconds. Related exact terminology anchors now use the visible surname labels: 20 paper-term tests pass with one existing advisory xfail. Parent result/release files pass Ruff and BasedPyright. The final combined failed-node rerun remains under think-zpfo.
