---
type: is
id: is-01m0qxpax67ja40sqgq024hg87
title: Repair the campaign trust boundary and run lifecycle
kind: bug
status: open
priority: 0
version: 5
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - pr-14
  - technical-error
dependencies:
  - type: blocks
    target: is-01m0qxpc5jrdzfn205qfxfvg44
  - type: blocks
    target: is-01m0qxpd3pnhvjh5s55b2w5gq8
  - type: blocks
    target: is-01m0qxpe517zsenj91xmydctg5
parent_id: is-01m0qxka8ebkztq7erex50vvr2
created_at: 2026-08-23T18:21:27.845Z
updated_at: 2026-08-23T18:52:22.929Z
---
Category: technical errors. The PR runner writes JSONL before validating overlap, records guard-invalid archives through the normal success path, trusts proposer-reported overlap, hardcodes selftest_passed, permits terminal rounds to be rewritten, ignores git failures, and does not enforce prerequisites or remaining deadlines. Build one checked state machine and one validation boundary shared by execute and record. Invalid output must be quarantined atomically and must never enter result cells.

Acceptance: adversarial overlapping or truncated JSONL, false overlap zero, crashing commands, expired leases, non-UTC offsets, terminal reruns, dirty-engine provenance, failed commits, unmet prerequisites, and session deadline overruns all have negative tests. Successful rounds archive full poses, independently recompute validity, record a real engine selftest and immutable provenance, narrow-stage only their files, and fail if persistence fails. Reconcile with think-d5tc and think-qopm rather than leaving parallel contracts.

## Notes

2026-08-23 stacked-review progress: result records are now validated before archival and revalidated on replay; undeclared cells and seeds are refused; guard failures are released instead of recorded; adversarial preflight checks pass. Remaining acceptance work includes stored full poses, independent validity recomputation, real selftest provenance, immutable state transitions, deadline and lease handling, narrow staging, and persistence-failure tests.
