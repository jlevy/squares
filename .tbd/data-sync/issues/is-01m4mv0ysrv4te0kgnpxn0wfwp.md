---
type: is
id: is-01m4mv0ysrv4te0kgnpxn0wfwp
title: "PR #406 (merge): refuse added bulk Git blobs using actual PR base"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
child_order_hints:
  - is-01m58dfyf99t7khbxj1th335af
hold: null
hold_until: null
created_at: 2026-10-11T06:39:54.162Z
updated_at: 2026-10-22T20:36:03.110Z
started_at: 2026-10-11T06:39:55.468Z
---
Owner request 2026-10-10 ~23:40 PT in the Claude Code session: review these PRs ("#398, #406, #497, #493, Stack #403 + #435") and "Yes, merge when gated"; then: "I would like to see a deep senior review on the regularization PR to make sure it is complete and reflects reasonable state before it is merged. Lets merge everything but not the regularization until I have a review of it myself."

## Notes

2026-10-22 20:45Z coord-intake-1021b: #406 (https://github.com/jlevy/squares/pull/406) at aaf39e816: main merged (78dc902c1); owner-approved change of the per-PR total to the thin pack (777dd2d48); census: only #461 refused (6 blobs >5 MiB), #578 passes at 2.39 MiB. Review K (https://github.com/jlevy/squares/pull/406#issuecomment-6350229576): change requested, K1 pin pack.threads=1/windowMemory=0 + test, K2-K4 docs/tests, K5 nits; lane c-lane-snapshot-policy-1022 fixing. Its site v0.9.2 cut (8d836ec6e) collides with #722's and is dropped after #729 merges. #726 (cap 512 MiB) merged e44a51f44.
