---
type: is
id: is-01m4frns0ydtrme6kb0twx38e3
title: Make the late parent-readback guard test deterministic
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m4fqjt02p8hxaxbgq056z2mq
created_at: 2026-10-09T07:22:38.481Z
updated_at: 2026-10-09T07:22:38.481Z
---
The final whole-suite run at be0ad196 recorded test_parent_readback_that_finishes_after_deadline_revokes_admission failing because its real worker exceeded the unchanged 0.18-second deadline before the intended parent readback phase. The retained result correctly refuses admission and reaps the group; parent_final_readback_seconds is null, so the test's phase-specific error expectation fails. Test and runtime are unchanged from base 3213d651b. Use the existing controlled-clock/process-double pattern to guarantee entry into readback then cross the same deadline, preserving real receipt serialization, refusal/revocation assertions, both group cleanup checks, and all separate real-process controls. No production guard or deadline change. Moderate agent prepares an external patch while full gate continues; apply only after process drain and senior review.
