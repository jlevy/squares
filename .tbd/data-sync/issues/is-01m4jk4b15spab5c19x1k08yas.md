---
type: is
id: is-01m4jk4b15spab5c19x1k08yas
title: "Import Francisco Couzo: certificates at n = 132, 237, 263, 267, 270, 303 (#476)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
hold: null
hold_until: null
created_at: 2026-10-10T09:43:27.525Z
updated_at: 2026-10-10T11:39:06.871Z
started_at: 2026-10-10T09:49:25.990Z
---
Issue https://github.com/jlevy/squares/issues/476 (opened 2026-10-09). Five exact optima from Evan Daniel's exact contact solver (132, 237, 267, 270, 303) and a rational witness at 263, in franciscouzo/square-packing certificates/ at 02f969075f79d5e13fa21e09e381a44e8647b452, Evan Daniel's .cert format. Overlaps #465 (T-131) at 132, #481 at 237, 263, 270, 303, and #470 at 132 and 267. Stages 1-3 and maintained exact replays.

## Notes

2026-10-10 (sub-agent lane, commit 1f9ee1606): stage 2 packet packing/resources/web/couzo-exact-certificates-2026-10-09/ at 02f969075f79 (no licence; all 65 certificates retained as factual data under the 2026-10-09 owner decision; READMEs and 65 decimal poses pinned only). All six #476 sides round up to the issue's 12-place prints; all six first committed in 02f9690 (2026-10-09T20:28:52Z), so attribution.published 2026-10-09. claims.json compares all 65: smallest at 132 and 267 is this certificate; at 237, 263, 270 and 303 issue #481's sides are smaller. Of the 59 unnamed certificates: 23 equal their case ceiling (22 T-098, 1 T-127), 11 are byte-identical to T-128 (7) or T-130 (4) certificates and below their cases, 5 are above their cases (68, 102, 103, 272, 292), 20 are beyond the horizon (15 below the tracked row, including 375 by 4.29e-5 and 378 by 4.00e-4; 5 rational witnesses above it, 327, 335, 342, 364, 372). Replay of 17 counts (the six plus 68-131): 51 jobs, all pass/refuse as required; receipt receipts/exact-certification.json.xz. register-plan printed; nothing registered. Remaining: stage 3 records (coordinator), and any beyond-horizon updates under think-1545.
