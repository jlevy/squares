---
type: is
id: is-01m47mft7sk2zep70k48bmwf55
title: check_sqverify_fast.mixed_exact evaluates a declared-net candidate at the standard net's angle, so census --control fails on declared nets
kind: bug
status: closed
priority: 2
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m47hea1vkqx8h5wzdzcyqs5k
created_at: 2026-10-06T03:35:33.369Z
updated_at: 2026-10-06T04:42:50.922Z
closed_at: 2026-10-06T04:39:55.229Z
close_reason: Fixed by 36b52538a (the control's evaluator reads a declared net), merged into claude/ecstatic-pascal-pothtx at f342dff82
resolution: null
duplicate_of: null
---
devtools/check_sqverify_fast.py direction(index) uses STEP = 83/40000 for every candidate. mixed_exact, which sqverify_fast_census --control uses to evaluate the least-bound leaf's centre and to set the near-threshold factor, therefore evaluates a declared-net candidate (proof_net) at the wrong angle. Measured by lane R2 (think-qzh5) on a scratch copy of the census, 2026-10-06: --control on mixed_n18_L4704 and mixed_n19_L48229 returns CONTROL_FAILED, captures_agree false (n18 node 797: crate 1.0104418663, evaluator 1.2554184361 at t = 797 x 83/40000 instead of 797/2006; n19 node 198: 1.0145690979 against 1.1197124384). Fix: direction(index, step) with step from the candidate's proof_net (a 15-line patch, kept at the lane's scratchpad as check_sqverify_fast-declared-step.patch and quoted in the R2 report); with it both controls return CONTROLS_REFUSED with captures agreeing. Not applied by R2: check_sqverify_fast.py is part of V-sqverify-fast's source and its independence record, and R2's session read the source's checker code. Needed before an evidence entry rests on sqverify-fast for a declared-net certificate (T-096, T-099, T-100), since the census test asks for a census control receipt.

## Notes

2026-10-06: fixed by lane R1's DR-1 fix at 36b52538a (merged into claude/ecstatic-pascal-pothtx at f342dff82): check_sqverify_fast.mixed_exact reads the candidate's proof_net step. Lane R2 regenerated the census rows and controls of mixed_n18_L4704 and mixed_n19_L48229 with that tool (copied into its worktree). Close at the merge of R2.
