---
type: is
id: is-01m5nwbzgvqzrtskzde98td2xe
title: "PR #757 (merge): senior review"
kind: task
status: closed
priority: 2
version: 4
delegate: c-rev-757-1024
labels: []
dependencies: []
parent_id: is-01m5mr7439b7eqzqzccqrxnkxa
hold: null
hold_until: null
created_at: 2026-10-24T02:38:20.187Z
updated_at: 2026-10-24T05:56:53.820Z
started_at: 2026-10-24T02:38:25.308Z
closed_at: 2026-10-24T05:56:53.819Z
close_reason: "#757 merged at c5697c2f2 on 24 October UTC (head 21a0624cf; review A 6379038105 with dispositions 6380602439; CI green 40067196011, 40067195965, 40067192448)"
resolution: null
duplicate_of: null
---

## Notes

2026-10-24 c-rev-757-1024 (senior review lane, coordinator coord-intake-1023): Review A of PR #757 posted.

- Review A, senior, round 1, head 3e90022ab841955d73daeaf2efc4f2be899baf46, base 5664ac1e8e752ec4f4c00e7ffac22ff53e25a929 (merge base with main). PR comment: https://github.com/jlevy/squares/pull/757#issuecomment-6379038105
- Verdict: approve; nothing blocks merge (register id contiguity aside, the coordinator's).
- Findings: A1 to A8, all Low. No Blocker or High.
  - A1: #763 (Couzo, 23:35:51Z on 23 October; 303 at 17.906978, 2.784e-3 below T-239) is missing from the description. Polkovskyi's 7e82c64 is 1.81e-11 below T-230 and above T-239. Together they make "below every other report at 303" (description) and the packet README:163 sentence ("the only report below T-230") stale.
  - A2: the run README says the 1 and 5 degree views are "the same view or no better". The 5 degree view is the only candidate that cuts angle classes (46 to 45, turning free square 167 by 1.93 degrees), at the cost of 1 light and 2 uneven squares against the axis view. The admitted 0.5 degree view turns nothing. That trade-off is an owner question under the 23 October definition.
  - A3: think-ykgh is still open and has no note, although this PR removed SETTLED[303] and its owed entry.
  - A4: n-303.md:594-595 states the rung without the diversity note; the adoption writer omits it for T-230 too.
  - A5: n-303.md:576-577 says the packet "holds" a certificate that is derived-only.
  - A6: RF-1 "computes" (results.yaml:32453-32454, packet README:259) describes a checker that was read, not run.
  - A7: packet README:194-195 says "new arrangement" where RF-4 has "another arrangement of T-230's packing".
  - A8: "merge on 24 October UTC or later" should be "on 24 October", since passes are dated by the day their PR merges.
- Verified:
  - program digests 7/7, and 11 receipts' program_sha256;
  - the gist re-fetched at 511f56b with the issue's digests, and review_t238_check.py routes Z and E re-run, receipts equal apart from timing;
  - the T-238 sweep, compressed files included;
  - the 204 row of the 24 October prior-state archive equal to main's; the 303 row equal to the merge base's n-303.md;
  - the index differs from the base only at 303; T-231 equals main's;
  - custody(write=False) equal to the committed receipt (70 houses, 194 inputs, 46 refused);
  - merge-tree with main da117ad0b clean.
- Tests: house_adoption + 755: 97 passed. overview -k project: 8 passed, plus 2 gist and coverage-card tests passed. result_status: 20 passed and 1 failed, on contiguity only. adopt_houses, upper_bound_houses check, select_houses, default_drawings --check-state, regularized_drawings and flip_regularization --check all pass. ruff is clean.
- Dedicated reviews: none recommended.
- Committed, pushed and synced nothing; the worktree /home/user/wt-lean is unchanged.
