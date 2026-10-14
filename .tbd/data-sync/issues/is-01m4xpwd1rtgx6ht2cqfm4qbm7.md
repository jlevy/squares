---
type: is
id: is-01m4xpwd1rtgx6ht2cqfm4qbm7
title: "Validate: Mishapolk 70a033f's 24 refined certificates, both exact routes, certify + check --replay, and decide 207 exactly (~0.8 CPU-h)"
kind: task
status: in_progress
priority: 1
version: 2
delegate: claude-code@vm
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4xmr0fhhynbfzj5vj0sh358
hold: null
hold_until: null
created_at: 2026-10-14T17:20:40.504Z
updated_at: 2026-10-14T23:04:32.810Z
started_at: 2026-10-14T23:04:32.810Z
---
Validation part of think-o644 (Mishapolk/square-packing-records 70a033f, 2026-10-14T16:11:31Z; no issue). Record-changing: 12 counts below best now. Not gated: the owner decided 2026-10-14 that a watched-repository publication counts from its first commit.

## Validation
- Claim: the 24 certificates refined at 70a033f (census.json credits 14 counts to Mykhailo Polkovskyi and 10 re-cut counts to 'Antigravity'): below best now at 129, 154, 156, 175, 176, 204, 232, 264, 271, 302, 303, 304; undecided at 207 (1.46e-41 over PR #574's 40-place print); not below at 153, 155, 181, 209, 267, 270, 272, 305, 306, 307, 308 (exact comparison of the 2026-10-14 triage, scratchpad triage2/scripts/misha.py, against ledger.json).
- Run: stage 1-2 first (think-o644): a packet by devtools.acquire_source pinned at 70a033f, read through the Evan Daniel-format adapter as the mishapolk lane did at 46f638c. Then `devtools.upper_bound_reports PACKET certify --jobs-dir DIR --workers 1` (positive and two controls per count, both maintained exact routes), `certify --finished`, and `check --replay`. For 207: compare its exact side with PR #574's exact degree-5 side (claude/wizardly-meitner-wqn4x3-intake-1014-pr574 at 56cf868c6, algebraic-claims.json) past 41 places, by an exact sign test.
- Cost: about 0.8 CPU-h: 697,681 pairs (sum of n(n-1)/2 over the 24) x 0.69 ms x 3 jobs x 2 (certify and check --replay), at the rate of the 2026-10-14 Fang theorem sample; up to 1.2 CPU-h at the loaded 5.0e-4 s per route decision of the 380-382 replay. The 13 counts that matter (12 below plus 207) are about half of that. The 207 comparison is seconds.
- Budget status (owner, 2026-10-14): runnable (<= 40 CPU-h).
- Possible <= 40 CPU-h subset: n/a (runnable as a whole).
- Depends on: think-o644's stage 1-2 packet. Owner decided 2026-10-14: counts from first commit. Registration also needs the records lane; validation does not.
- Done when: all 24 positives pass both routes, all 48 controls are refused, check --replay equals the retained rows, 207 is decided, and the ledger takes the 70a033f claims in report order; noted on think-o644.
- Machine note: 4 CPUs shared with gates; a run > 2 wall-h should be scheduled outside a validation gate. About 1 wall-h on one worker under load.
