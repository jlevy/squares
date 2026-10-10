---
type: is
id: is-01m4hh8qjqx61qfa5v50qjmx18
title: Diagnose local atlas hover pixel sampling failure
kind: bug
status: in_progress
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h9s465x7mphy1xxkmdyqc9
hold: null
hold_until: null
created_at: 2026-10-09T23:51:39.861Z
updated_at: 2026-10-10T00:24:45.373Z
started_at: 2026-10-09T23:51:47.613Z
---
Final H54153ad81 full push completed957.84s exit1:65 editchecks passed; twelve site_drawing_hover cases fail at their shared screenshot fixture because sampled frame ink is(28,37,47) instead of expected(23,32,42). Hosted Fast passes. Diagnose default Small drawing geometry, antialiasing, probe sampling and baseline behavior with retained actual images. Correct only the established defect without weakening true fixed-ink/white-canvas/hover behavior, skipping tests, or broadening production tolerances. Delegate narrow repair; root commits, updates PR and repeats required qualification. Preserve failed H receipt; no GitHub merge.

## Notes

Small DPR2 control lacks exact frame-ink pixels; DPR3 retains default Small geometry and all assertions. Focused module15passed/0skips; peer routine precommit inspection no findings. Broad selected gate: all65edit checks passed, normal4368passed/35skipped/4warnings in810.23s; whole reachable step timed out900s while pool composite test ran, total1373.94s. Failed receipt retained at external final/push-hover-precommit-artifacts. Existing whole-branch selection naturally grants1800s; final one-shot whole-branch gate will use the maintained implicit scheduler and include both normal and pool lanes. No time limits, assertions or skips changed. Candidate blob d33149e905bbfa9f887df81b7b9df93fe333ed1c; exact indexed tree will bind passing source to the normal commit, with fresh all107 hosted steps at published head.
