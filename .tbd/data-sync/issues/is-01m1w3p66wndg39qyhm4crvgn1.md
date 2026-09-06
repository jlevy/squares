---
type: is
id: is-01m1w3p66wndg39qyhm4crvgn1
title: Repair operating-rule mutation after new rules are added
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-06T19:38:54.043Z
updated_at: 2026-09-06T20:01:24.749Z
---
PR #97 added OR-16, but the summary-drift mutation injects another OR-16. It now fails the contiguity check before reaching its intended summary-drift refusal. Main run 34053183058 and PR98 deferred run 34054616340 both expose this failure. Derive the next contiguous rule inside this specific control, preserve a healthy baseline and the exact expected refusal, and test future rule counts.

## Notes

Fixed in fc72f05e and integrated in b3b7275f. The registered control uses a stable sentinel and derives the next source-rule number. Fixtures with 16, 17 and 25 rules verify a healthy baseline, the intended summary-drift refusal and restoration. The real control passed in 0.476s with a 2.517s full journal. Ordinary CI 34056428243 passed; full checkpoint 34056585319 is pending.
