---
type: is
id: is-01m59f5qc2h4ey6tv8kjax3cc8
title: Accept complete reviewed release chains for atomic main deliveries
kind: bug
status: in_progress
priority: 1
version: 2
assignee: codex-atomic-release-chain-20261018
delegate: codex-atomic-release-chain-20261018
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-19T06:56:50.561Z
updated_at: 2026-10-19T06:57:00.958Z
started_at: 2026-10-19T06:57:00.958Z
---
Merged main d167d4b86 fails the release-impact gate when its first-parent delivery compares site v0.7.25 to v0.7.27 across the reviewed atomic #661/#676 stack. Support complete fresh adjacent retained decisions only for explicit --base delivery comparisons; retain strict direct --baseline-ref PR checks. Regression coverage must reject missing, stale, malformed and backward chains. No public component content changes.
