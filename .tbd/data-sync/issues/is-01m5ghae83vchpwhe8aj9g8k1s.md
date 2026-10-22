---
type: is
id: is-01m5ghae83vchpwhe8aj9g8k1s
title: Preserve profile integration through upstream T-223 and T-225 releases
kind: task
status: in_progress
priority: 1
version: 3
delegate: profiles-pr-coordinator
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-22T00:49:03.234Z
updated_at: 2026-10-22T01:04:45.747Z
started_at: 2026-10-22T00:49:10.707Z
---
Resolve newly landed origin/main d7923b8d8 conflicts after the button fix. Preserve upstream adoption and release history, reconcile profile identity joins and shared resource descriptions, regenerate URL/data views, validate, and keep PR578 reviewable without merging it.

## Notes

Merged origin/main d7923b8d8 as 8dd742b7e; data pin 9dd10fec9. Astra reviewed reconciliation, releases, attribution, and snapshot capacity. Full preview build and 69-step push gate running in external scratch. Initial bead-tree failure was unrelated closed intake parent think-qdcc with unfinished think-lrvl; reopened parent, restored its coordinator, standalone check passes. Latest requested Overview ordering tracked separately as think-17fv; worker updating template and rendered preview. Not yet pushed; remote PR head8077d8e54 is conflicted until integrated head is pushed. Do not merge PR.
