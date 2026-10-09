---
type: is
id: is-01m4fshxxk07b0kwjx2zdphq53
title: Stabilize the malformed resident-response guard test
kind: bug
status: closed
priority: 1
version: 5
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4fqjt02p8hxaxbgq056z2mq
hold: null
hold_until: null
created_at: 2026-10-09T07:38:01.009Z
updated_at: 2026-10-09T13:44:10.798Z
started_at: 2026-10-09T07:38:46.800Z
closed_at: 2026-10-09T13:44:10.798Z
close_reason: Implemented, independently reviewed and qualified for PR474 source 6ccbbf000f0c9b48f2985c07c9893f98fe73ba92 against main 6a0499ba4; combined tree c65da41410e89a8dedffe93d3c1e153adb05096d. Local named push 65/65 and hosted 93 fast + 13 actual deferred (106) plus Pages passed; final readiness receipts recorded.
resolution: null
duplicate_of: null
---
The completed full pre-push at be0ad196 records test_invalid_resident_response_refuses[wrong_sequence] failing with DID NOT RAISE CandidateError; the call took 2.21 seconds against a two-second allowance, but its return report was discarded. Test and relevant runtime are unchanged from base 3213d651b. Preserve strict resident sequence/protocol refusal and real transport. First perform a bounded diagnostic that captures any returned report, then make the existing malformed-response test examine its intended protocol path deterministically without broadening refusal, extending production deadlines, or removing independent timeout/snapshot controls. Senior agent owns this disjoint test diagnosis/repair; root and a peer review the resulting change and keep production untouched unless concrete evidence establishes a defect.

## Notes

At bbd7 the full gate wrong-sequence case did raise CandidateError, but its reason was OS Errno1 Operation not permitted instead of identity refusal; this is distinct from the earlier missed deadline phase. The partial-line test returned timeout before admitted identities/angle census at unchanged0.5s. One bounded unchanged module rerun passed7/7 (pytest total64.14s versus JUnit interval3.160s; not a protocol benchmark); instrumented wrong-sequence passed exact refusal0.667s, readiness0.655s and cleanup, no EPERM reproduced. Root accepted existing exclusive-phase classification of six real subprocess cases with truthful marker wording, keeping all realbounds/assertions and adding caught-exception trace diagnostics. This is execution-context hardening, not proven EPERM repair or a guarantee0.5s startup always succeeds. Senior owns only native test file; root/web independent review and complete pre-push remain.
