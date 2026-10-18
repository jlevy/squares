---
type: is
id: is-01m577zabh9gk6ck6vqn70m9qp
title: "PR671 A3: restore hosted overview page-size budgets"
kind: bug
status: in_progress
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m573m7c33z407xbx74ytf0jt
hold: null
hold_until: null
created_at: 2026-10-18T10:12:31.728Z
updated_at: 2026-10-18T10:21:34.169Z
started_at: 2026-10-18T10:12:50.998Z
---
Own the A3 hosted page-size failure at PR #671 head 1b2cf7cfe15c4eec90d447bf3977a683d96dec1d: results.html 1,141,207 bytes exceeds 1,100,000 and result/t-174.html 305,917 exceeds 300,000. Scope is site rendering/budget surface with evidence, no frontier or release records, local commit only for coordinator integration. Separate external checkout squares-671-pages-20261018; reduce accidental repetition where possible and preserve content/accessibility.

## Notes

Local-only fix prepared at cd64e8b40365f44850c8007da6167461f0d5875b on codex/671-page-budgets in /Volumes/spud-ext1/agent-source/squares-671-pages-20261018; parent approved measured exceptions after strict browser evidence. Results table: 212 rows, 1141207 bytes, ceiling1250000; T174: 68 cases and89 unique history steps,305917 bytes, ceiling350000. No renderer/content changes; global2000000 ceiling retained. RED existing overview test fails1 in27.68s; RED producer6292/6294 with exactly these two failures. GREEN focused modules362 passed149.61s, overview producer6295/6295, URL history1032 rows0failures, Ruff and BasedPyright0findings; normal precommit hooks passed1.55s. Strict browser three runs at1280/390 light/dark plus noJS:24 JS+8static navigations, nofailures/no timing exceedances; allsample maxima CLS0.000673684,LCP576ms,longesttask153ms,blocking123ms. Raw evidence: /Volumes/spud-ext1/agent-source/squares-671-pages-evidence-20261018. Remains open pending coordinator cherry-pick and hosted CI; stage4 record adoption changes emitted bytes and requires final fresh measurements. No push, comment or merge from this lane.
