---
type: is
id: is-01m4xpwd1rtgx6ht2cqfm4qbm7
title: "Validate: Mishapolk 70a033f's 24 refined certificates, both exact routes, certify + check --replay, and decide 207 exactly (~0.8 CPU-h)"
kind: task
status: closed
priority: 1
version: 5
delegate: claude-code@vm
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4xmr0fhhynbfzj5vj0sh358
hold: null
hold_until: null
created_at: 2026-10-14T17:20:40.504Z
updated_at: 2026-10-15T06:23:08.751Z
started_at: 2026-10-14T23:04:32.810Z
closed_at: 2026-10-15T06:23:08.751Z
close_reason: "Done: replay complete and T-186 registers the 70a033f claims on main (c4c690a3e, #612)"
resolution: null
duplicate_of: null
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

## Notes

2026-10-14 evening lane (think-mq0k, branch `claude/wizardly-meitner-wqn4x3-intake-1014b`): **run.** Packet `packing/resources/web/mishapolk-kkt-refinements-2026-10-14/` (24 derived facts at 70a033f). `upper_bound_reports ... certify --jobs-dir SCRATCH --workers 1`: 22:53:02Z-23:30:38Z (37 min 36 s wall, load 2-2.5, another lane's replay alongside). All 24 positives pass both routes; all 48 controls refused on both. Least wall clearance / pair gap equal on both routes at every count: 5e-25 / 1e-24 at the ten 'Antigravity' counts; 5e-41 / 1e-40 at 129, 153, 154, 156, 302, 304; 5e-101 / 1e-100 at 204, 207, 232, 264, 271, 303; 3.63e-78 at 175; 3.62e-98 at 176. Receipts: receipts/exact-certification-nNNN.json.xz, one per count. check --replay 23:31:19Z-00:09:05Z (37 min 46 s, load 2-8): all 72 jobs equal to the retained rows; 4,186,086 pair decisions, 2,167.90 route CPU s, longest job 78.28 s. **207 decided exactly:** PR #574's degree-5 side (facts/alg-n-207.yaml.gz of the PR #574 packet) is below 70a033f's by 1.488e-99 (difference_bounds in acquisition/claims.json), so 207 is not recorded. Remaining for "done when": the ledger/records PR takes the 70a033f claims in report order (register plan kept in the packet as register-plan.yaml). Actual cost: about 1.2 CPU-h (2,168 route CPU s for certify and about as much for the replay), the top of the 0.8-1.2 CPU-h estimate.

**2026-10-15, done.** The records PR took the 70a033f claims in report order: #612 (records-1015) merged into main at c4c690a3e registers **T-186** at the twelve counts, citing this replay (24 positives, 48 controls, 4,186,086 pair decisions, receipts in mishapolk-kkt-refinements-2026-10-14), with 207 not recorded as decided exactly. Every "done when" item is met. Reply naming T-186 posted on #593: https://github.com/jlevy/squares/issues/593#issuecomment-6185872048. Closing.
