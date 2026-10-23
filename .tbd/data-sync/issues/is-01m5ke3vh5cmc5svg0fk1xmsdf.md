---
type: is
id: is-01m5ke3vh5cmc5svg0fk1xmsdf
title: Repair published-site verifier after navigation split
kind: task
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: sol-upstream-final
labels: []
dependencies: []
parent_id: is-01m5kcfhfdmgfb03gn3drg43rc
hold: null
hold_until: null
created_at: 2026-10-23T03:50:45.017Z
updated_at: 2026-10-23T03:50:52.645Z
started_at: 2026-10-23T03:50:52.644Z
---
Main Pages verify-deployment run 39896243132 exposed five stale assertions: Atlas case index moved to Frontier and four paper bars mark Learn/Papers under new navigation. Update only devtools/check_published_site.py and focused tests to assert real deployed links/current state, preserving strict full case and paper checks.
