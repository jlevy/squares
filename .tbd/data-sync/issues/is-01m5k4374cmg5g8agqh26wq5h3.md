---
type: is
id: is-01m5k4374cmg5g8agqh26wq5h3
title: Repair semantic navigation CI expectations after final page and filter changes
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-ci-test-repairs
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T00:55:38.378Z
updated_at: 2026-10-23T01:08:45.789Z
started_at: 2026-10-23T00:55:49.041Z
closed_at: 2026-10-23T01:08:45.788Z
close_reason: Assigned stale test repairs validated and pushed; current-head CI and remaining product integration tracked by think-z3lz and think-kmpp.
resolution: null
duplicate_of: null
---
Update stale redirect-order, canonical Posters page, project preset controls, typography token scope and overlay viewport contracts in four assigned test files. Preserve behavior assertions; run targeted checks and commit/push only those files.

## Notes

Completed test-only repairs, pushed with normal hooks in13f265753,4ebb4604d,a211b63f9bbb9210e08b8b6ebe3f16d53cde2aa7. Seven semantic redirect/filter/token/overlay contracts pass14.16s. Remaining frontend: homepage2/menu1/Verification font9 all pass; font negative-control CLS unchanged, guide producer now Verification. Added-date1passes44.04s using actual Recent data-result/data-added rows, confirming no runtime filter defect. News desktop contract passed; mobile1passes65.94s after normal Escape dismissal before Reset, no force click. News-only probe checks neutral surfaces/colored-ink contrast independently from Results kind palette. Ruff/format/diff clean, scoped basedpyright0errors0warnings and tsconfig.probes tsc clean. Root retains integration acceptance; Frontier worker now owns navigation/result-filter test edits.
