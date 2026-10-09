---
type: is
id: is-01m4frns0ydtrme6kb0twx38e3
title: Make the late parent-readback guard test deterministic
kind: bug
status: closed
priority: 1
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4fqjt02p8hxaxbgq056z2mq
hold: null
hold_until: null
created_at: 2026-10-09T07:22:38.481Z
updated_at: 2026-10-09T13:44:10.666Z
started_at: 2026-10-09T07:35:05.146Z
closed_at: 2026-10-09T13:44:10.666Z
close_reason: Implemented, independently reviewed and qualified for PR474 source 6ccbbf000f0c9b48f2985c07c9893f98fe73ba92 against main 6a0499ba4; combined tree c65da41410e89a8dedffe93d3c1e153adb05096d. Local named push 65/65 and hosted 93 fast + 13 actual deferred (106) plus Pages passed; final readiness receipts recorded.
resolution: null
duplicate_of: null
---
The final whole-suite run at be0ad196 recorded test_parent_readback_that_finishes_after_deadline_revokes_admission failing because its real worker exceeded the unchanged 0.18-second deadline before the intended parent readback phase. The retained result correctly refuses admission and reaps the group; parent_final_readback_seconds is null, so the test's phase-specific error expectation fails. Test and runtime are unchanged from base 3213d651b. Use the existing controlled-clock/process-double pattern to guarantee entry into readback then cross the same deadline, preserving real receipt serialization, refusal/revocation assertions, both group cleanup checks, and all separate real-process controls. No production guard or deadline change. Moderate agent prepares an external patch while full gate continues; apply only after process drain and senior review.

## Notes

Applied the reviewed test-only controlled-clock/process-double repair. Twenty focused controls passed in 3.09 seconds with zero skips, including terminal admission, interruption, cleanup and real-process deadlines. Same 0.18-second deadline and 0.05 grace; production is unchanged. Final lint/type receipt and full pre-push remain pending. Root independently read final diff; senior source review accepted.
