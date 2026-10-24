---
type: is
id: is-01m5p3zeaxgseqzx8vxfcbtfbj
title: "PR #769 (merge): senior review"
kind: task
status: closed
priority: 2
version: 5
delegate: c-rev-769-1024
labels: []
dependencies: []
parent_id: is-01m5nrbfn316e9g0zfr03269fr
child_order_hints:
  - is-01m5p62aj72eqgcyvnne5eq0wq
hold: null
hold_until: null
created_at: 2026-10-24T04:51:17.981Z
updated_at: 2026-10-24T08:25:40.416Z
started_at: 2026-10-24T04:51:27.144Z
closed_at: 2026-10-24T08:25:40.415Z
close_reason: "PR #769 merged 2026-10-24T06:48:50Z (34eb8bb75) after senior review A."
resolution: null
duplicate_of: null
---

## Notes

2026-10-24 c-rev-769-1024 (senior review A, round 1, PR #769 at head 38c896bc2, base 14b14f2d1): https://github.com/jlevy/squares/pull/769#issuecomment-6380362746

Verdict: approve once A1 to A3 are addressed. No row, verdict or supersession is wrong. No Blocker or High findings.

- A1 (Medium): the key's credit "Polkovskyi after Couzo, Levy" drops antecedents that Couzo's own manifests name at counts this release refines (chain rule). 6b7391d names Muglich at 15 counts and Daniel/Fang at 343; 4e4c8ce names PingYou Ltd at 328 and Daniel at 365, 404 and 455, Fang at 651, and Fang/PingYou at 813.
- A2 (Medium): the 335 text has three problems.
  - It omits Couzo's own answer on #715 (6375833547, "the bound we stand behind is the certificate's").
  - It conflicts with #766 on the same result-requests block. The review gives a suggested merged text.
  - "Within one unit of the print on either reading" is false for the literal reading, which needs print + 1.465e-15.
- A3 (Medium): CONFLICTING with main 2c58b6373 (#745, #750, #771). Six files conflict, and no walked count moves.
- A4 to A10 (Low):
  - README wording: the index credit at 127/11, and "within 0.22", which should be 0.23.
  - The source README's credit is not recorded.
  - "No pair touches" rests on the filter. It is true: I checked all pairs out to d^2 < 2.01.
  - The order of #763's commits rests on the push rule, and PUSHED_LATER holds only one push per repository. fa6237e, committed 18:59Z, lies below f1ceee4 at 131 of 138 counts by header, so think-cnn7 must add the 23:38:42Z push.
  - think-f2io lacks the 11-count ask.
  - _start_highs is dead, and measured_identity has no test.
  - Draft nits.

Tests at 38c896bc2:
- pytest -n 2: 183 passed. The five modules were test_beyond_horizon_replay, test_intake_ledger, test_couzo_decimal_decisions, test_upper_bound_reports_715 and test_upper_bound_reports_702.
- These passed:
  - intake_ledger check and render --check; answer_problems [];
  - beyond_horizon_replay check, check --issue, and check --issue --replay --workers 2 (OK, 16m07s);
  - acquire_source --check;
  - check_added_blobs (PASS, 5,645,882 B);
  - check_source_coverage and release_pin --check.

Reviewer scripts are in scratchpad review-769/bin/: walk_check, rat_check, all_gaps, check335 and decide_alg.
