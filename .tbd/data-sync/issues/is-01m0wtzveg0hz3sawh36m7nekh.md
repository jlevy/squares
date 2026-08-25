---
type: is
id: is-01m0wtzveg0hz3sawh36m7nekh
title: Give cases/trump11/incidence_cores.py an automated regression
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m0wtz4vb81vyh3665rt33xh2
created_at: 2026-08-25T16:10:26.127Z
updated_at: 2026-08-25T16:10:26.127Z
---
No gate step or pytest file exercises incidence_cores.py; its only validation is the session's manual '--branch 0 --selftest' command (22s). A fast structural regression (derive_branch + the structural selftest block with a stubbed oracle, no LP minimization) would run in seconds and protect the module against drift. Coordinate with think-oa96 (D-290 certificate replay) and think-j92q (D-291 golden/refutation separation) so one design serves all three.
