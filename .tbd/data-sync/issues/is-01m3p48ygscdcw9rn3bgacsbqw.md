---
type: is
id: is-01m3p48ygscdcw9rn3bgacsbqw
title: Enforce and exercise the sqsearch Rust quality floor
kind: task
status: closed
priority: 2
version: 6
labels: []
dependencies: []
parent_id: is-01m3nzy6gqfv60whzzvww0ffa0
created_at: 2026-09-29T08:25:05.816Z
updated_at: 2026-09-29T09:00:13.692Z
closed_at: 2026-09-29T09:00:13.691Z
close_reason: Implemented in 5d4e26de1 and repaired rustdoc integration in 45eaf8e75. Actual Rust gate passed locally and hosted; scoped documentation regression and 1,598 selected tests pass. Parent think-8cps retains the inherited Session 161 certification blocker.
resolution: null
duplicate_of: null
---
Apply pinned tbd Rust lint floor; run existing Rust integration/unit tests and rustdoc in CI; add contract and deliberate failing lint probes. Preserve mathematical search semantics and documented golden oracle.

## Notes

Hosted Rustdoc exposed generated font-license Markdown under packing/sqsearch/target. Narrow scanner exclusion and regression now prepared: only exact Cargo output prefix excluded, ordinary docs/target and target-not-generated remain checked. Focused tests2 pass, real documentation check1494documents passes, Ruff/type clean. Awaiting corrective commit and hosted CI.
