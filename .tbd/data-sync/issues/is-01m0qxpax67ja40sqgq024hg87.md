---
type: is
id: is-01m0qxpax67ja40sqgq024hg87
title: Repair the campaign trust boundary and run lifecycle
kind: bug
status: open
priority: 0
version: 11
spec_path: packing/campaign/agendas/agenda-016-results-first-continuation-rigidity-and-remediation.md
labels:
  - packing
  - review
  - pr-14
  - technical-error
  - focus-process
dependencies:
  - type: blocks
    target: is-01m0qxpc5jrdzfn205qfxfvg44
  - type: blocks
    target: is-01m0qxpd3pnhvjh5s55b2w5gq8
  - type: blocks
    target: is-01m0qxpe517zsenj91xmydctg5
  - type: blocks
    target: is-01m0r7rab2j8krgraey9a810x9
parent_id: is-01m1jv8hm5xka6ytdtjs47tb0a
hold: paused
created_at: 2026-08-23T18:21:27.845Z
updated_at: 2026-09-03T05:48:33.483Z
---
Category: technical errors. The PR runner writes JSONL before validating overlap, records guard-invalid archives through the normal success path, trusts proposer-reported overlap, hardcodes selftest_passed, permits terminal rounds to be rewritten, ignores git failures, and does not enforce prerequisites or remaining deadlines. Build one checked state machine and one validation boundary shared by execute and record. Invalid output must be quarantined atomically and must never enter result cells.

Acceptance: adversarial overlapping or truncated JSONL, false overlap zero, crashing commands, expired leases, non-UTC offsets, terminal reruns, dirty-engine provenance, failed commits, unmet prerequisites, and session deadline overruns all have negative tests. Successful rounds archive full poses, independently recompute validity, record a real engine selftest and immutable provenance, narrow-stage only their files, and fail if persistence fails. Reconcile with think-d5tc and think-qopm rather than leaving parallel contracts.

## Notes

2026-08-23 stacked-review progress: result records are validated before archival and on replay; undeclared cells and seeds are refused; guard failures are released instead of recorded; adversarial preflight passes. At c412b8c, D-032 and D-033 are finally logged but remain unguarded. The timezone crash is fixed for runner-produced UTC leases, while dropping tzinfo still mishandles non-UTC offsets. Remaining work includes stored poses, independent validity recomputation, immutable lifecycle states, prerequisite/deadline/lease enforcement, narrow checked persistence, and recovery-path tests.

Agenda 016 ownership: paused as the defect-specific child subsumed by W9 wave think-modk. BC-147 names one writer before unpausing; no work starts from this bead independently.
