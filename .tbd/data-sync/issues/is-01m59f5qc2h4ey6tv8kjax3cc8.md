---
type: is
id: is-01m59f5qc2h4ey6tv8kjax3cc8
title: Accept complete reviewed release chains for atomic main deliveries
kind: bug
status: in_progress
priority: 1
version: 3
assignee: codex-atomic-release-chain-20261018
delegate: codex-atomic-release-chain-20261018
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-19T06:56:50.561Z
updated_at: 2026-10-19T07:25:25.879Z
started_at: 2026-10-19T06:57:00.958Z
---
Merged main d167d4b86 fails the release-impact gate when its first-parent delivery compares site v0.7.25 to v0.7.27 across the reviewed atomic #661/#676 stack. Support complete fresh adjacent retained decisions only for explicit --base delivery comparisons; retain strict direct --baseline-ref PR checks. Regression coverage must reject missing, stale, malformed and backward chains. No public component content changes.

## Notes

Published draft PR #682 https://github.com/jlevy/squares/pull/682 at head 76e2ff9b456522c6b8b89cfbe5ac5633da4f7ad5, parent policy main 7d350455147e6df0618163272030b3cddd37affa. Only check_release_impact.py and test_release_impact.py changed; no edition or publication waiver. Original main delivery comparison failed before and passes after. Focused release suites: 41 passed in 13.61s; Ruff/format and normal precommit hook passed. Local pre-push: 24/25 passed, reachable quick tests timed out at unchanged 900s under 2-CPU serial shape, 1094.12s total; no broad local pass claimed and owned processes exited. Independent Astra source senior/correctness passes clean at matching blobs; formal publication and final hosted qualification remain with root coordinator. Packing run39215602317, Certificate page39215602361, Branch mergeability39215576810 pending. PR description corrected and verified through fresh GitHub read with actual timeout/counts. Root requested no second broad local run and is taking CI monitoring. Scratch receipts: /Volumes/spud-ext1/agent-scratch/squares-atomic-release-chain-20261018/before-fix.json, after-fix.json, push-gate-final.log.
