---
type: is
id: is-01m5ke3vh5cmc5svg0fk1xmsdf
title: Repair published-site verifier after navigation split
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: sol-upstream-final
labels: []
dependencies: []
parent_id: is-01m5kcfhfdmgfb03gn3drg43rc
hold: null
hold_until: null
created_at: 2026-10-23T03:50:45.017Z
updated_at: 2026-10-23T04:03:04.966Z
started_at: 2026-10-23T03:50:52.644Z
closed_at: 2026-10-23T04:03:04.966Z
close_reason: Merged PR737 deployed; follow-up PR743 checker repair pushed at c278006b3. Frontier case index and semantic Learn/Papers current navigation checks preserve strict assertions. Focused navigation tests 5 passed, full checker module 134 tests passed across two focused runs, Ruff clean; local live rerun against deployed merge 31584003e passed 5,245/5,245 checks in 507.51s. Hosted PR743 gates pending.
resolution: null
duplicate_of: null
---
Main Pages verify-deployment run 39896243132 exposed five stale assertions: Atlas case index moved to Frontier and four paper bars mark Learn/Papers under new navigation. Update only devtools/check_published_site.py and focused tests to assert real deployed links/current state, preserving strict full case and paper checks.
