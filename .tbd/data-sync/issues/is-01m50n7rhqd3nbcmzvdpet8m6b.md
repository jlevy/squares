---
type: is
id: is-01m50n7rhqd3nbcmzvdpet8m6b
title: "PR #629 B1: record the effective pytest worker count"
kind: bug
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m50kwed71nqmh914z0mh5103
hold: null
hold_until: null
created_at: 2026-10-15T20:49:38.870Z
updated_at: 2026-10-15T20:49:50.898Z
started_at: 2026-10-15T20:49:50.897Z
---
Security review found a Low diagnostic correctness defect at head 75610bd10: a native command without explicit -n can receive -n 2 from PYTEST_ADDOPTS, while the journal reports one worker. Use pytest/xdist effective configuration rather than parsing environment options; preserve resource policy and add a real subprocess control. Moderate writer owns the progress writer and tests; root owns commits and review disposition.
