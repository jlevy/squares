---
type: is
id: is-01m22dpyxw89vp76w2w1623zay
title: Decide whether the 12.6 MB lane E completion receipt stays in the branch before merge
kind: chore
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-09-09T06:29:31.708Z
updated_at: 2026-09-09T06:29:31.708Z
---
results/agenda-032/lane-e-completion-61-16-receipt.json is 413,932 of the branch's 428,820 added lines: an unresolved run receipt whose input block (24,653 sites, 11,885 rows), site orbits and per-row exact/oracle dumps are 12.4 MB of its 12.6 MB; the decision-bearing content (parameters, status, row solution, round timings) is about 100 KB. Options: slim it to that content plus the full receipt's SHA-256 and rewrite the one commit that added it before merge, or keep it as the repository keeps 4-11 MB state files elsewhere. Owner's call.
