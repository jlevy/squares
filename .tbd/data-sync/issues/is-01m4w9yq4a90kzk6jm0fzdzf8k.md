---
type: is
id: is-01m4w9yq4a90kzk6jm0fzdzf8k
title: Return the quarter-turned n305 certificate test to PR coverage
kind: bug
status: closed
priority: 1
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4w9w2vc4p0j983wvvx8pybw
hold: null
hold_until: null
created_at: 2026-10-14T04:15:30.441Z
updated_at: 2026-10-14T07:21:25.526Z
started_at: 2026-10-14T04:16:43.425Z
closed_at: 2026-10-14T07:21:25.525Z
close_reason: Fixed, independently reviewed, and merged in regularization stack main9f48ccc80cee8dcf94c7cadbcaded01408f94fa2; exact-head Packing and Pages CI pass. Deployment tracked by parent think-azzv.
resolution: null
duplicate_of: null
---
Main run38503790618/job115656519709 passed all slow tests but rejected tests/test_check_half_angle_area.py::test_the_489_certificate_at_305_has_488s_side_in_a_quarter_turned_arrangement at0.66s below1s floor. Delete its slow marker and expected registry entry, retain unchanged behavior test on fast PR surface, refresh measurement note. Do not raise thresholds or timing budgets.
