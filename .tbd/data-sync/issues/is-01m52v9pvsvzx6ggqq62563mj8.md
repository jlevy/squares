---
type: is
id: is-01m52v9pvsvzx6ggqq62563mj8
title: "Policy: the house is always the smallest validated packing, regularized in the same PR (owner, 16 Oct)"
kind: task
status: in_progress
priority: 2
version: 5
delegate: user-eb-policy-houses
labels: []
dependencies: []
parent_id: is-01m51hyxstsa9ptekd2ss26ksn
hold: null
hold_until: null
created_at: 2026-10-16T17:14:02.997Z
updated_at: 2026-10-16T18:46:45.217Z
started_at: 2026-10-16T17:17:09.781Z
---
Owner, 2026-10-16 afternoon: 'We should always be adopting the smallest packing and then regularizing it. That should be the policy, obviously.' and 'This should be built into our policy. It shouldn't even be a question. If there's any ambiguity on that, we should fix that in our process docs for intake.' Write it into result-import.md stage 5, the regularization guide, the frontier README, and select_houses/adopt_houses (owner holds such as HELD T-174, RP-3 algebraic left-outs, undecided orderings, regularized views below U), then adopt every smaller validated packing it reaches and regularize each.

## Notes

2026-10-16T17:38Z user-eb-policy-houses (lane P): claimed. Worktree /home/user/squares/.claude/worktrees/policy-house, branch claude/intake-2026-10-16-policy-smallest-house from #641's head 7aa4775ea. Survey done: on #641's base select_houses holds T-174 at 60 counts and leaves T-174's algebraic certificates out at 70/153/207/302; 17 case ceilings are closed forms; #658 adds a deferral-keyed exemption for T-193 (16 algebraic counts). Other questions found: stage 5/guide 'the adoption waits for the owner's word' (176 case); n=17 register candidates excluded by think-x4v4 (evand_exact_certificates.HELD, register_regularized_bounds.HELD). Next: exact-side module + select_houses rewrite + staging allowlist naming this bead.

2026-10-16T18:18Z lane P: code checkpoint 0a3d61850 pushed on claude/intake-2026-10-16-policy-smallest-house (base #641 7aa4775ea). New devtools/exact_sides.py (exact order of rational and algebraic sides, closed-form ceilings via regularize_evand.verified_bound); select_houses: HELD gone, algebraic certificates are candidates, PENDING_ADOPTION stages T-174's 63 smaller counts under think-sa5r (bead tree holds it open), --check fails on any unstaged smaller validated packing; adopt_houses replays records under the rule their pass ran under (recorded view), skips staged counts, keeps conjectures mechanically; default_drawings/printout: a falling strong view's runs are not deferred. test_house_adoption 41/42 (the docs test waits for the runbook text), test_exact_sides 8/8. T-174 real storage cost measured: 63 witnesses 23.25 MB raw vs 6.10 MB replaced (+17.16 MB checkout), 3.51 MB vs 1.02 MB as Git objects (+2.49 MB); largest 1.16 MB. Next: runbook rule + pointers, then validation, PR, then the plan table on main and on the stack.

2026-10-16T18:46Z lane P: draft PR #660 https://github.com/jlevy/squares/pull/660 (base #641's branch claude/ecstatic-edison-8en33t-regularization-intake, head a0594db96, labels intake/project/S2). Rule in result-import.md stage 5 'The House Rule'; gate select_houses --check live, 63 counts staged in PENDING_ADOPTION under think-sa5r (so think-sa5r must stay open until the adoption PR that empties it merges). Merged #641's badaf21f0 (D1: STRONG_VIEW_LOST) with the house rule's consequence (UNDEFERRED). Local: records tier 51/52 (only URL-registry history vs main: t-193/t-194 registered on main by #651 after #641 branched; base issue), 112 focused tests pass, release impact clean. Next: the adoption plan on main and on the stack (#641+#657+#658).
