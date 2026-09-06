---
type: is
id: is-01m1w3p66wndg39qyhm4crvgn1
title: Repair operating-rule mutation after new rules are added
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-06T19:38:54.043Z
updated_at: 2026-09-06T19:38:54.043Z
---
PR97 addedOR16. The summary-drift mutation still injectsOR16, so it now failscontiguity before reachingits expectedsummaryrefusal. Mainrun34053183058 and PR98deferred34054616340 both failthis onecontrol. Derive a contiguous next rule in this specificcontrol withoutnewgenericmutationDSL, preservegreenbaselineand exactexpectedfailure, and testfuturevalidrulecounts.
