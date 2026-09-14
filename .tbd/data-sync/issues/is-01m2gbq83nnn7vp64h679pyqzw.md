---
type: is
id: is-01m2gbq83nnn7vp64h679pyqzw
title: "PR #167: mark the implemented H-162 analyzer instrument ready"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2gbcm4afdzz4r8x790g898q
created_at: 2026-09-14T16:24:05.999Z
updated_at: 2026-09-14T16:24:05.999Z
---
packing/campaign/hypotheses/H-162-bc303-floor-normalized-t2-filter.md names the newly added and tested analyzer but sets instrument_ready: false. The schema defines false as the instrument not existing yet, and the campaign runner skips it for that reason. Set true; keep upstream receipt/control readiness in prereqs and experiment state.
