---
type: is
id: is-01m50n7rhqd3nbcmzvdpet8m6b
title: "PR #629 B1: record the effective pytest worker count"
kind: bug
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m50kwed71nqmh914z0mh5103
hold: null
hold_until: null
created_at: 2026-10-15T20:49:38.870Z
updated_at: 2026-10-15T21:18:44.421Z
started_at: 2026-10-15T20:49:50.897Z
closed_at: 2026-10-15T21:18:44.420Z
close_reason: B1 fixed in 3b14dcbfd, independently confirmed by senior and security reviewers, and merged in PR629 as22a67ce4. Final-head Packing38807032473 and Pages38807032511 passed all applicable checks. Actual xdist runtime count and serial control are covered by the regression; no selection, resource or deadline change.
resolution: null
duplicate_of: null
---
Security review found a Low diagnostic correctness defect at head 75610bd10: a native command without explicit -n can receive -n 2 from PYTEST_ADDOPTS, while the journal reports one worker. Use pytest/xdist effective configuration rather than parsing environment options; preserve resource policy and add a real subprocess control. Moderate writer owns the progress writer and tests; root owns commits and review disposition.

## Notes

B1 fixed in 3b14dcbfd5fe185bbcd9e0270d8923e1f52c0ae7. Progress plugin uses xdist runtime workercount or serial one. Writer reproduced the failure, then all 14 progress tests passed in 5.66s; Ruff, formatting and targeted BasedPyright clean. These focused results are transcript evidence, without standalone logs. Both independent Astra reviewers confirmed the two-file delta and B1 resolution with no new findings. Posted disposition issuecomment-6202248777 on PR629. Final-head hosted CI remains pending; keep bead open until that result.
