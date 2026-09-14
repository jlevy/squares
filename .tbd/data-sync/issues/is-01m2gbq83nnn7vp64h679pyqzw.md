---
type: is
id: is-01m2gbq83nnn7vp64h679pyqzw
title: "PR #167: mark the implemented H-162 analyzer instrument ready"
kind: bug
status: closed
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m2gce39ed9awfhdpaq8ed3rt
created_at: 2026-09-14T16:24:05.999Z
updated_at: 2026-09-14T19:20:07.603Z
closed_at: 2026-09-14T19:20:07.603Z
close_reason: Fixed in ed68f644; 14 focused tests pass, Ruff/BasedPyright are clean, pre-push functional validation passes, and fresh hosted required CI is green on the exact head.
resolution: null
duplicate_of: null
---
packing/campaign/hypotheses/H-162-bc303-floor-normalized-t2-filter.md names the newly added and tested analyzer but sets instrument_ready: false. The schema defines false as the instrument not existing yet, and the campaign runner skips it for that reason. Set true; keep upstream receipt/control readiness in prereqs and experiment state.

## Notes

Fixed in ed68f644; focused tests and static checks pass. Awaiting clean checkpoint and hosted CI before closure.
