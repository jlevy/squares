---
type: is
id: is-01m1tx0r0tfmqjq6fyxvxeta2k
title: "Deep gate: relation-reach negative control exceeds its 300-second timeout"
kind: bug
status: closed
priority: 2
version: 4
labels: []
dependencies: []
created_at: 2026-09-06T08:23:05.496Z
updated_at: 2026-09-06T08:36:25.713Z
closed_at: 2026-09-06T08:36:25.713Z
close_reason: Fixed in stacked PR 96 commit 8e0fba99. All required CI checks passed in run 34022006920; all45 selected pre-push steps and31 record steps passed locally, including558 reachable tests. Previously failing bounds audit and all affected negative controls now pass.
resolution: null
duplicate_of: null
---
Full local gate reported relation reach - probe sweeps to typed-in ceiling instead of digits timed out after 300 s. Reproduce focused under lower contention, determine whether mutant behavior or gate is at fault, and retain evidence.

## Notes

Fixed in follow-up PR 96 commit 8e0fba99: focused test checks requested degree before running real baseline search; mutant20 fails immediately rather than spending300s. Actual negative control fires, baseline passes in0.97s; removed unnecessary timeout override.
