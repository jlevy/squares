---
type: is
id: is-01m4fshxxk07b0kwjx2zdphq53
title: Stabilize the malformed resident-response guard test
kind: bug
status: in_progress
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4fqjt02p8hxaxbgq056z2mq
hold: null
hold_until: null
created_at: 2026-10-09T07:38:01.009Z
updated_at: 2026-10-09T07:47:30.168Z
started_at: 2026-10-09T07:38:46.800Z
---
The completed full pre-push at be0ad196 records test_invalid_resident_response_refuses[wrong_sequence] failing with DID NOT RAISE CandidateError; the call took 2.21 seconds against a two-second allowance, but its return report was discarded. Test and relevant runtime are unchanged from base 3213d651b. Preserve strict resident sequence/protocol refusal and real transport. First perform a bounded diagnostic that captures any returned report, then make the existing malformed-response test examine its intended protocol path deterministically without broadening refusal, extending production deadlines, or removing independent timeout/snapshot controls. Senior agent owns this disjoint test diagnosis/repair; root and a peer review the resulting change and keep production untouched unless concrete evidence establishes a defect.

## Notes

Bounded diagnostics prove a deliberately delayed private snapshot can bypass the intended protocol phase via a fail-closed INCONCLUSIVE timeout, but the historical returned report was not retained and its precise cause remains unconfirmed. Senior authored the narrow test-only logical-clock separation and exact per-mode refusal assertions, retaining real transport, two-second select waits and all separate real-clock controls. Module 7/7 passed in 2.47 seconds; Ruff/format/BasedPyright clean; delayed-setup control reaches and rejects the malformed response. Root independent readback accepted; peer review and full pre-push remain pending.
