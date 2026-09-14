---
type: is
id: is-01m2gbq83nnn7vp64h679pyqzw
title: "PR #167: mark the implemented H-162 analyzer instrument ready"
kind: bug
status: in_progress
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2gce39ed9awfhdpaq8ed3rt
created_at: 2026-09-14T16:24:05.999Z
updated_at: 2026-09-14T17:03:59.352Z
---
packing/campaign/hypotheses/H-162-bc303-floor-normalized-t2-filter.md names the newly added and tested analyzer but sets instrument_ready: false. The schema defines false as the instrument not existing yet, and the campaign runner skips it for that reason. Set true; keep upstream receipt/control readiness in prereqs and experiment state.

## Notes

Fixed in ed68f644; focused tests and static checks pass. Awaiting clean checkpoint and hosted CI before closure.
