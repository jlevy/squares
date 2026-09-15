---
type: is
id: is-01m2k9tx5ydxdk8ty7vj0mk728
title: Certify and merge the admitted Route S instrument
kind: task
status: in_progress
priority: 0
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels: []
dependencies: []
parent_id: is-01m2gt509a6wa4kqwbxjrq6exd
created_at: 2026-09-15T19:48:52.030Z
updated_at: 2026-09-15T20:32:35.927Z
---
Finalize Session 135 and generated views with the source-distinct ADMIT verdict, commit the no-target instrument checkpoint on PR 182, require exact-head fast and deferred gates, merge only the reviewed head, and verify origin/main. Do not allocate exp-161 or run an optimizer, candidate, or coverage target.

## Notes

Route S head 202ae51c is committed and pushed on PR 182 with 63 focused tests, deterministic admitted receipt replay, schemas, ledger, synopsis/session checks, 164 controls, Ruff, and BasedPyright green. The PR remains draft because main is advancing through the workbench stack. A conservative unpushed merge rehearsal against origin/main 21a68102 produced 252e9c0e: it unioned the Synopsis/ledger/control records, preserved H-163 and Session 135, Ruff-formatted three new Route files, and passed the same checks. A synthetic merge against current PR 180 found only disjoint edits. After the stack lands, propagate final origin/main, certify the exact head with fast and deferred gates, record that certification, and merge. No exp-161 or scientific target is authorized yet.
