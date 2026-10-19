---
type: is
id: is-01m52v9pvsvzx6ggqq62563mj8
title: "Policy: the house is always the smallest validated packing, regularized in the same PR (owner, 16 Oct)"
kind: task
status: in_progress
priority: 2
version: 15
delegate: user-eb-policy-houses
labels: []
dependencies: []
parent_id: is-01m51hyxstsa9ptekd2ss26ksn
hold: null
hold_until: null
created_at: 2026-10-16T17:14:02.997Z
updated_at: 2026-10-17T04:17:20.742Z
started_at: 2026-10-16T17:17:09.781Z
---
Owner, 2026-10-16 afternoon: 'We should always be adopting the smallest packing and then regularizing it. That should be the policy, obviously.' and 'This should be built into our policy. It shouldn't even be a question. If there's any ambiguity on that, we should fix that in our process docs for intake.' Write it into result-import.md stage 5, the regularization guide, the frontier README, and select_houses/adopt_houses (owner holds such as HELD T-174, RP-3 algebraic left-outs, undecided orderings, regularized views below U), then adopt every smaller validated packing it reaches and regularize each.

## Notes

2026-10-16T17:38Z user-eb-policy-houses (lane P): claimed. Worktree /home/user/squares/.claude/worktrees/policy-house, branch claude/intake-2026-10-16-policy-smallest-house from #641's head 7aa4775ea. Survey done: on #641's base select_houses holds T-174 at 60 counts and leaves T-174's algebraic certificates out at 70/153/207/302; 17 case ceilings are closed forms; #658 adds a deferral-keyed exemption for T-193 (16 algebraic counts). Other questions found: stage 5/guide 'the adoption waits for the owner's word' (176 case); n=17 register candidates excluded by think-x4v4 (evand_exact_certificates.HELD, register_regularized_bounds.HELD). Next: exact-side module + select_houses rewrite + staging allowlist naming this bead.

2026-10-16T18:18Z lane P: code checkpoint 0a3d61850 pushed on claude/intake-2026-10-16-policy-smallest-house (base #641 7aa4775ea). New devtools/exact_sides.py (exact order of rational and algebraic sides, closed-form ceilings via regularize_evand.verified_bound); select_houses: HELD gone, algebraic certificates are candidates, PENDING_ADOPTION stages T-174's 63 smaller counts under think-sa5r (bead tree holds it open), --check fails on any unstaged smaller validated packing; adopt_houses replays records under the rule their pass ran under (recorded view), skips staged counts, keeps conjectures mechanically; default_drawings/printout: a falling strong view's runs are not deferred. test_house_adoption 41/42 (the docs test waits for the runbook text), test_exact_sides 8/8. T-174 real storage cost measured: 63 witnesses 23.25 MB raw vs 6.10 MB replaced (+17.16 MB checkout), 3.51 MB vs 1.02 MB as Git objects (+2.49 MB); largest 1.16 MB. Next: runbook rule + pointers, then validation, PR, then the plan table on main and on the stack.

2026-10-16T18:46Z lane P: draft PR #660 https://github.com/jlevy/squares/pull/660 (base #641's branch claude/ecstatic-edison-8en33t-regularization-intake, head a0594db96, labels intake/project/S2). Rule in result-import.md stage 5 'The House Rule'; gate select_houses --check live, 63 counts staged in PENDING_ADOPTION under think-sa5r (so think-sa5r must stay open until the adoption PR that empties it merges). Merged #641's badaf21f0 (D1: STRONG_VIEW_LOST) with the house rule's consequence (UNDEFERRED). Local: records tier 51/52 (only URL-registry history vs main: t-193/t-194 registered on main by #651 after #641 branched; base issue), 112 focused tests pass, release impact clean. Next: the adoption plan on main and on the stack (#641+#657+#658).

2026-10-16 ~19:20Z lane P (user-eb-policy-houses): ADOPTION PLAN under the house rule (PR #660, head a0594db96). Computed with #660's select_houses/exact_sides on main 7b34cd5bb, and on the stack = #657 head 5d5eb2dec merged with #658 head ccac86dd4 plus a scratch T-193 reader (16 Oct ledger exact-sides.json, every polynomial validated irreducible by sqpack.field). Scratch: laneP/plan-main.json, plan-657.json, plan-stack.json, plan-table.md.

TOTALS. Main: 63 counts move, all to T-174 (60 rational, 3 algebraic: 70 deg 5, 153 deg 7, 207 deg 5); witnesses 23.25 MB in a checkout (6.10 MB replaced), 3.51 MB as Git stores them (1.02 MB replaced); runs 63 x 0.2 = 12.6 CPU-h. Stack: 57 counts move: T-174 at 41 (38 rational + 70, 153, 207) and T-193 at 16 (88, 102, 123, 126, 175, 199, 204, 232, 258, 259, 266, 267, 292, 295, 301, 302; all algebraic, degree 2 to 41); witnesses 32.71 MB raw, 7.69 MB as Git stores them; runs 57 x 0.2 = 11.4 CPU-h (Daniel driver + grid-slack 0.5/1/5 + selection, the 3a receipts' 0.2 CPU-h a count). Both under the pass's 40 CPU-h item cap.

STAGING BY MERGE ORDER (select_houses.PENDING_ADOPTION). #660 lands 63 T-174 entries (think-sa5r). Whichever of #657 and #660 merges second removes the 10 #657 makes stale: 129, 146, 156, 175, 176, 204, 232, 264, 271, 303 (53 left). #658 (drop deferred_results; register T-193 in ALGEBRAIC_READERS) re-points 12 entries to T-193 (88, 102, 123, 126, 199, 258, 259, 266, 267, 292, 295, 301) and adds 175, 204, 232, 302 for T-193: 41 T-174 + 16 T-193 = 57. Either order converges there.

ADOPTION LANE SLICES. (1) Algebraic writer: adopt_houses writes rational houses only (refuses algebraic now); upper_bound_houses needs an algebraic source (PingYou alg facts are Witness/v2 already; T-193 needs its minpoly forms derived to Witness/v2), adopt_houses an exact_form for a root of p in an interval that parse_case/verified_bound read back, plus prose/coverage/check; blocks 19 counts on the stack (3 on main). (2) Storage: in Git under the rule's stored reading; T-174 +2.49 MB in Git/+17.16 MB checkout; T-193's 204 is 11.54 MB raw/3.53 MB gz (the one at OR-18's per-file line), 267 3.65/1.55 MB; publish #639's four pinned-only forms (204, 263, 267, 297; 20.75 MB) as a hosted data release; measure the negative-controls snapshot (213.9 MB, cap 216 MiB, 13.6 MB headroom) and raise its cap with the measurement. (3) Regularize every re-housed count in the same PR, runs not deferred where a strong view would be lost. (4) After the last staged count: delete LIFTED, the recorded view's pre-rule branch and RULE_PASSES_FROM; adopt_houses --refresh under the rule (rewrites e.g. 302's not-selected list). (5) Pass day >= 2026-10-17 (RULE_PASSES_FROM; #657's archive is 2026-10-16).

OWNER QUESTIONS RESOLVED BY THE RULE (evidence). 21: adopt whichever is smallest: on the stack T-193 at its 16, T-174 elsewhere; T-193 = T-174 exactly at 70/153/207 (same minimal polynomial and root), so report order keeps T-174. #639 vs T-186 at 175/204/232/302: ordered exactly, T-193 below by 1.0e-76, 1.5e-99, 1.6e-99, 1.8e-39. 24: lane B's 153/207 views (3b-1016) are below today's cases but 1.29e-19 / 1.49e-19 ABOVE T-174's algebraic sides, so T-174 is the house and the views are not recorded (report order); 154's row-7 view is at the house's side (row 7 needs same/bound): a drawing review, not an adoption. 28: 211's row-7 views likewise (T-188 house after #657; no move). T-174 hold: gone. 176: #657's T-186 (stays on the stack).

OWNER QUESTION FOUND (regularization policy, not adoption). 12 of the 19 algebraic-house counts on the stack draw a strong view today (88, 126, 153, 175, 204, 207, 259, 266, 301 evand; 199, 267, 292 grid-slack). No strong view can be admitted at an irrational side today (obligation 1: no second exact route over a number field; a rational view is above U, row 4; question 13 allows views above U only at its seven named counts), so after adoption they settle on the axis view or the house drawing. Either the layer gains a number-field second route, or the owner extends question 13's exceptions to a rational view just above an algebraic house.

OTHERS FOUND. n = 17: evand_exact_certificates.HELD and register_regularized_bounds.HELD keep n=17 out of T-101/T-155 for think-x4v4; T-155's selection lists a row-3 view there with no side kept in the record: under the rule a view below U is a report for intake. T-174's 37 other algebraic certificates (attaining reported closed forms below rational ceilings, not recorded under report order) are not validated here; not in the gate.

TABLE (n | house now on main | rule on main | house after #657/#658 | rule on the stack | margin | witness raw / in Git MB | runs):
| 68 | T-118 | T-174 | T-118 | T-174 | 4.6e-61 | 0.10 / 0.017 | driver + grid-slack 0.5/1/5 + select |
| 70 | T-146 | T-174 (degree 5) | T-146 | T-174 (degree 5) | 8.9e-20 | 0.016 / 0.003 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 84 | T-130 | T-174 | T-130 | T-174 | 9.7e-20 | 0.12 / 0.018 | driver + grid-slack 0.5/1/5 + select |
| 86 | T-130 | T-174 | T-130 | T-174 | 9.8e-20 | 0.17 / 0.022 | driver + grid-slack 0.5/1/5 + select |
| 88 | T-127 | T-174 | T-127 | T-193 (degree 7) | 9.9e-20 | 0.028 / 0.005 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 102 | T-146 | T-174 | T-146 | T-193 (degree 4) | 1.1e-19 | 0.030 / 0.005 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 103 | T-146 | T-174 | T-146 | T-174 | 1.1e-19 | 0.23 / 0.034 | driver + grid-slack 0.5/1/5 + select |
| 105 | T-170 | T-174 | T-170 | T-174 | 1.1e-79 | 0.15 / 0.030 | driver + grid-slack 0.5/1/5 + select |
| 108 | T-128 | T-174 | T-128 | T-174 | 1.1e-19 | 0.15 / 0.020 | driver + grid-slack 0.5/1/5 + select |
| 110 | evand exact optima 2026-10-05 | T-174 | evand exact optima 2026-10-05 | T-174 | 1.1e-19 | 0.33 / 0.050 | driver + grid-slack 0.5/1/5 + select |
| 123 | T-146 | T-174 | T-146 | T-193 (degree 6) | 1.2e-19 | 0.041 / 0.007 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 126 | T-139 | T-174 | T-139 | T-193 (degree 2) | 1.2e-19 | 0.030 / 0.005 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 127 | T-128 | T-174 | T-128 | T-174 | 1.2e-19 | 0.18 / 0.026 | driver + grid-slack 0.5/1/5 + select |
| 129 | T-162 | T-174 | T-186 | stays | 1.2e-19 | 0.31 / 0.051 | driver + grid-slack 0.5/1/5 + select |
| 130 | T-127 | T-174 | T-127 | T-174 | 1.2e-19 | 0.26 / 0.037 | driver + grid-slack 0.5/1/5 + select |
| 131 | T-136 | T-174 | T-136 | T-174 | 1.1e-31 | 0.18 / 0.030 | driver + grid-slack 0.5/1/5 + select |
| 132 | T-141 | T-174 | T-141 | T-174 | 1.2e-19 | 0.29 / 0.039 | driver + grid-slack 0.5/1/5 + select |
| 146 | T-168 | T-174 | T-187 | stays | 1.3e-79 | 1.16 / 0.30 | driver + grid-slack 0.5/1/5 + select |
| 153 | T-173 | T-174 (degree 7) | T-173 | T-174 (degree 7) | 1.6e-14 | 0.063 / 0.004 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 155 | T-149 | T-174 | T-149 | T-174 | 1.3e-19 | 0.30 / 0.038 | driver + grid-slack 0.5/1/5 + select |
| 156 | T-161 | T-174 | T-186 | stays | 1.3e-19 | 0.18 / 0.030 | driver + grid-slack 0.5/1/5 + select |
| 172 | evand exact optima 2026-10-05 | T-174 | evand exact optima 2026-10-05 | T-174 | 1.4e-19 | 0.57 / 0.14 | driver + grid-slack 0.5/1/5 + select |
| 175 | T-158 | T-174 | T-186 | T-193 (degree 7) | 1.0e-76 | 0.061 / 0.009 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 176 | T-165 | T-174 | T-186 | stays | 1.2e-02 | 0.32 / 0.055 | driver + grid-slack 0.5/1/5 + select |
| 179 | T-127 | T-174 | T-127 | T-174 | 1.4e-19 | 0.23 / 0.023 | driver + grid-slack 0.5/1/5 + select |
| 180 | T-128 | T-174 | T-128 | T-174 | 1.4e-19 | 0.24 / 0.030 | driver + grid-slack 0.5/1/5 + select |
| 181 | T-151 | T-174 | T-151 | T-174 | 1.3e-31 | 0.46 / 0.070 | driver + grid-slack 0.5/1/5 + select |
| 182 | evand exact optima 2026-10-05 | T-174 | evand exact optima 2026-10-05 | T-174 | 1.4e-19 | 0.40 / 0.049 | driver + grid-slack 0.5/1/5 + select |
| 199 | T-127 | T-174 | T-127 | T-193 (degree 16) | 1.5e-19 | 0.81 / 0.17 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 204 | T-162 | T-174 | T-186 | T-193 (degree 35) | 1.5e-99 | 11.54 / 3.53 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 206 | evand exact optima 2026-10-05 | T-174 | evand exact optima 2026-10-05 | T-174 | 1.5e-19 | 0.20 / 0.033 | driver + grid-slack 0.5/1/5 + select |
| 207 | T-173 | T-174 (degree 5) | T-173 | T-174 (degree 5) | 2.4e-12 | 0.040 / 0.004 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 208 | T-127 | T-174 | T-127 | T-174 | 1.5e-19 | 0.39 / 0.047 | driver + grid-slack 0.5/1/5 + select |
| 209 | T-140 | T-174 | T-140 | T-174 | 1.5e-19 | 0.37 / 0.052 | driver + grid-slack 0.5/1/5 + select |
| 210 | evand exact optima 2026-10-05 | T-174 | evand exact optima 2026-10-05 | T-174 | 1.5e-19 | 0.49 / 0.073 | driver + grid-slack 0.5/1/5 + select |
| 228 | T-128 | T-174 | T-128 | T-174 | 1.6e-19 | 0.46 / 0.047 | driver + grid-slack 0.5/1/5 + select |
| 232 | T-158 | T-174 | T-186 | T-193 (degree 7) | 1.6e-99 | 0.070 / 0.011 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 236 | T-146 | T-174 | T-146 | T-174 | 1.6e-19 | 0.30 / 0.029 | driver + grid-slack 0.5/1/5 + select |
| 238 | T-151 | T-174 | T-151 | T-174 | 1.5e-31 | 0.41 / 0.049 | driver + grid-slack 0.5/1/5 + select |
| 239 | T-151 | T-174 | T-151 | T-174 | 1.5e-31 | 0.60 / 0.090 | driver + grid-slack 0.5/1/5 + select |
| 240 | evand exact optima 2026-10-05 | T-174 | evand exact optima 2026-10-05 | T-174 | 1.6e-19 | 0.62 / 0.086 | driver + grid-slack 0.5/1/5 + select |
| 258 | T-146 | T-174 | T-146 | T-193 (degree 8) | 1.7e-19 | 0.13 / 0.023 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 259 | T-136 | T-174 | T-136 | T-193 (degree 6) | 1.6e-31 | 0.062 / 0.011 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 261 | T-169 | T-174 | T-169 | T-174 | 2.0e-21 | 0.39 / 0.056 | driver + grid-slack 0.5/1/5 + select |
| 263 | T-146 | T-174 | T-146 | T-174 | 1.7e-19 | 0.55 / 0.065 | driver + grid-slack 0.5/1/5 + select |
| 264 | T-158 | T-174 | T-186 | stays | 1.7e-19 | 0.38 / 0.050 | driver + grid-slack 0.5/1/5 + select |
| 266 | T-119 | T-174 | T-119 | T-193 (degree 32) | 1.7e-19 | 0.41 / 0.056 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 267 | T-134 | T-174 | T-134 | T-193 (degree 41) | 1.7e-19 | 3.65 / 1.55 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 268 | evand exact optima 2026-10-05 | T-174 | evand exact optima 2026-10-05 | T-174 | 1.7e-19 | 0.35 / 0.030 | driver + grid-slack 0.5/1/5 + select |
| 269 | T-146 | T-174 | T-146 | T-174 | 1.7e-19 | 0.35 / 0.040 | driver + grid-slack 0.5/1/5 + select |
| 270 | T-151 | T-174 | T-151 | T-174 | 1.6e-31 | 0.56 / 0.080 | driver + grid-slack 0.5/1/5 + select |
| 271 | T-161 | T-174 | T-186 | stays | 1.7e-19 | 0.26 / 0.034 | driver + grid-slack 0.5/1/5 + select |
| 272 | T-171 | T-174 | T-171 | T-174 | 1.7e-99 | 0.68 / 0.10 | driver + grid-slack 0.5/1/5 + select |
| 273 | evand exact optima 2026-10-05 | T-174 | evand exact optima 2026-10-05 | T-174 | 1.7e-19 | 0.39 / 0.048 | driver + grid-slack 0.5/1/5 + select |
| 292 | T-146 | T-174 | T-146 | T-193 (degree 6) | 1.8e-19 | 0.10 / 0.015 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 295 | T-146 | T-174 | T-146 | T-193 (degree 2) | 1.8e-19 | 0.094 / 0.015 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 297 | evand exact optima 2026-10-05 | T-174 | evand exact optima 2026-10-05 | T-174 | 1.8e-19 | 0.98 / 0.22 | driver + grid-slack 0.5/1/5 + select |
| 301 | evand exact optima 2026-10-05 | T-174 | evand exact optima 2026-10-05 | T-193 (degree 4) | 1.8e-19 | 0.062 / 0.011 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 302 | T-181 | stays | T-186 | T-193 (degree 7) | 1.8e-39 | 0.087 / 0.014 | driver + grid-slack 0.5/1/5 + select; algebraic: expect SETTLED |
| 303 | T-162 | T-174 | T-186 | stays | 1.8e-19 | 0.34 / 0.041 | driver + grid-slack 0.5/1/5 + select |
| 305 | T-152 | T-174 | T-152 | T-174 | 1.8e-19 | 0.29 / 0.042 | driver + grid-slack 0.5/1/5 + select |
| 306 | T-128 | T-174 | T-128 | T-174 | 1.8e-19 | 0.91 / 0.13 | driver + grid-slack 0.5/1/5 + select |
| 307 | T-136 | T-174 | T-136 | T-174 | 1.7e-31 | 0.78 / 0.11 | driver + grid-slack 0.5/1/5 + select |
| 308 | T-141 | T-174 | T-141 | T-174 | 1.8e-19 | 0.92 / 0.14 | driver + grid-slack 0.5/1/5 + select |

2026-10-16T19:24Z lane P: hosted CI on #660 at a0594db96: every job passed but validate (URL-registry history vs main: t-193/t-194 registered on main by #651 after #641 branched; base issue, clears when #641 takes main) and suite-b (test_verified_upper_bound_contract: test_exact_sides undeclared; fixed in cf85ddd4a, pushed). Local: 60 test files touching the changed modules, 3000 passed, 5 failed only in test_browser_floor_contract (ESLint cannot resolve typescript-eslint through this worktree's symlinked node_modules; CI's browser floor passed). Waiting on the rerun; then the worktree is removed so an address-pr lane can check the branch out.

Carry into #660's next addressing pass: #641 review F's F1 and F2 (https://github.com/jlevy/squares/pull/641#pullrequestreview-5552932945). F1: step 1 of the runbook and the guide still defers each pending count while the mark says 'its runs are not deferred'; exclude adopted counts from the deferral and word the mark as an obligation. F2: the docstring of test_the_comparison_lists_what_each_changed_count_draws still says 'for the owner'.

2026-10-16T19:55Z lane P: #641 moved to 453128d1c (merged main 7b34cd5bb; review E took #660's words: DEFERRAL_WAITS, UNDEFERRED, no owner hold in stage 5). Merged into #660 as 17b385bd1 (pushed); #660 mergeable again. At 17b385bd1: packing-validate --records --jobs 2 passes every step (130.5 s); 266 focused tests pass; select_houses --check exit 0 (63 staged); release impact clean. #658 guidance: whichever of #658 and #660 merges second drops deferred_results, registers T-193 in select_houses.ALGEBRAIC_READERS and stages its 16 counts in PENDING_ADOPTION (re-point 88,102,123,126,199,258,259,266,267,292,295,301 from T-174; add 175,204,232,302). Hosted run on 17b385bd1 in progress.

2026-10-16 ~21:00Z lane P (user-eb-policy-houses): #660 https://github.com/jlevy/squares/pull/660 ready for review at 8e53e5c65 (draft, base main, labels intake/project/S2; description updated). Merged main into the branch with merge commits at 68cdbc614 (#641), 96510ae7a (#648), 321d492c7 (#650; one conflict, in result-import.md) and c9038049c (#652). None of #648, #650 or #652 changes a register entry, case record or selection code.

F1 (review F of #641), done as the coordinator directed. No count an adoption re-houses is deferred to default_drawings.PENDING_ALLOWED. Above the pass's compute cap the adoption waits with its runs, staged in select_houses.PENDING_ADOPTION. adopt_houses --check fails while PENDING_ALLOWED names a count re-housed by a pass dated on or after RULE_PASSES_FROM, 17 Oct (adopt_houses.deferred_adoptions). The --compare mark is the obligation: default_drawings.RUNS_OWED = "its runs are owed in this pull request". UNDEFERRED is renamed, adopt_houses.DEFERRAL_WAITS is replaced by NEVER_DEFERRED, and the printout no longer offers a deferral. Reworded: the runbook (W1 step 3, prompt step 4, the stage table, the house rule's "Regularizing is part of adopting", stage 5), guide step 3 and policy section 8. Only a witness corrected or re-solved with its house's side unchanged may defer its runs, and never at a marked count. Review F's do-not-fix note (above the cap an adoption may defer its runs to a bead) is superseded. F2: the docstring now says the comparison names the goals and marks the obligation.

#650 merge: kept #650's imports that make a house (a register adoption, a Kingbird catalogue intake, an exact re-solve) and its bead labels, and applied the rule to all of them. Stage 0's bullet: the allowlist entry is made by the pull request that corrects a witness, never by one that re-houses the count. intake_sweep's step for an unlisted pending count says the same. Code enforces register adoptions only; a catalogue intake has no such check.

Validation (from packing/, uv run --frozen --all-extras --group dev): packing-validate --records --jobs 2, 52/52 steps at 5e2e13371 (151.0 s) and at a282ef726 (133.0 s). 314 focused tests pass, 1 skipped, across ten files including test_intake_sweep. select_houses --all --check exit 0 (63 staged). adopt_houses refresh(write=False), check() and deferred_adoptions() all empty. check_documentation (2060 documents), check_release_impact --baseline-ref origin/main and check_bead_tree pass. ruff, format and basedpyright: 0 findings on the 14 changed Python files. Hosted: every job passed at 17b385bd1 and at 37c1d827c. At 8e53e5c65 every hosted job passed (deferred checkpoint skipped); GitHub reports #660 mergeable (clean) against main c9038049c.

PLAN ADDENDUM (F1). The adoption PR runs every count it re-houses itself, and splits only by leaving counts staged. 14 of the 63 staged counts are already on main's PENDING_ALLOWED: 105, 129, 146, 153, 156, 175, 176, 204, 207, 232, 264, 271, 272, 303 (think-la7h, think-kpm3, think-3zi3). The adoption's runs decide them and its PR takes them off. On the stack, 232 and 302 are on #657's list and move to T-193. #657's pass is dated 16 Oct, so the check passes it, but its list names 8 of the 15 counts it re-houses. Seven (232, 237, 264, 271, 302, 303, 304) have their runs done and their selection and admission owed to think-r3cl; under the rule that finishing belongs in #657. 211 waits on the owner's row-7 review, an owner question. The stack's register is unchanged since the plan (#657 5d5eb2dec to 6d3ea4a3e touches only the regularization layer), so the numbers stand: main 63 counts, 12.6 CPU-h; stack 57, 11.4 CPU-h. Merge note: the stack lacks 68cdbc614, and whichever merges second resolves UNDEFERRED to RUNS_OWED in default_drawings.py and its test.

think-sa5r stays open until the adoption PR that empties PENDING_ADOPTION merges (bead tree holds it). The worktree is removed so an address-pr lane can check the branch out.

2026-10-16 ~23:00Z addressing pass on #660 (reviews A and B at 8e53e5c65), as user-eb-policy-houses: merged main 80b116ede (eef7e5741); code slice 9417d8a9c pushed (A1 staging beads think-3mry/think-ot5c with reasons, A3 cap text, A5/B1/B2 witness-keyed deferral check in default_drawings, A6 guard, A8-A10, B3-B7). Next: docs (A4, A7, A12-A14), A2 record changes, description, dispositions.

2026-10-16 ~23:50Z #660 addressing pass, after the container restart: pushed 1e0b8ac8a. Commits since 8e53e5c65: eef7e5741 (merge main 80b116ede), 9417d8a9c (code: A1 beads think-3mry/think-ot5c with STAGING_REASONS, A3, A5/B1/B2 witness-keyed default_drawings.deferral_problems, A6, A8-A10, B3-B7), 070420789 (docs: A4, A7 in OR-18, A12-A14), 3875e7eef (A2 records: 63 case records refreshed, results.yaml, source-coverage, requests, citation deferral to think-ot5c), 75915fe18 (pin), 72b8b50ac (merge main 3301a1cf6: #644, #653), c76e0dc5a (pin), 1e0b8ac8a (papers' no-change record by render). Deferral beads: think-mbdw (number-field second route), think-z6aj (n = 17 view). The site needs an edition for A2, cut in merge order. Next: validation, description, dispositions, CI.

2026-10-17 ~00:30Z user-eb-policy-houses: addressing pass on reviews A and B of PR #660 done at 53785a88d (main 5012a97d6 merged, #654). 21 fixed, 1 deferred (A11 to think-z6aj), 0 declined; A1's optional bead-label check left out. Replies: https://github.com/jlevy/squares/pull/660#pullrequestreview-5555015627 (A) and https://github.com/jlevy/squares/pull/660#pullrequestreview-5555016150 (B). Hosted CI at 53785a88d: every job passed except validate and its packing-required roll-up, on check_release_impact for the site alone (run 38985460814). The site's edition is cut in merge order, so the PR stays a draft. Beads: think-3mry and think-ot5c (the adoptions, open, unclaimed), think-mbdw and think-z6aj (claimed). #657 must take 211 off PENDING_ALLOWED: the witness-keyed check flags only 211 at 1f343b743 and passes with it off. #658 must drop deferred_results; the guard test fails if it merges. This bead closes when #660 merges.

2026-10-17 ~02:50Z user-eb-policy-houses: review C of PR #660 addressed at f76706d17, after merging main c593e2bfd (#656, #657). 12 fixed, C13 deferred to think-qu30 (claimed), 0 declined. Reply: https://github.com/jlevy/squares/pull/660#pullrequestreview-5555627574. CORRECTED entries are now held to the base record (--check-state --base-ref origin/main), and DEFERRED_AT_RULE is gone. T-174 is staged at 53 counts (50 rational under think-3mry, 70/153/207 under think-ot5c); #657 took ten below it. upper_bound_houses sizes measures the staged witnesses (50: 2.84 MB stored, 19.25 MB in a checkout). Hosted CI at f76706d17: green except validate and packing-required, which fail on the site's release impact alone (run 38995847476). The site edition is v0.7.25, cut after #663 on the coordinator's word. think-3mry's title and block still say 60 counts; the true number is now 50.

2026-10-17 ~04:20Z user-eb-policy-houses: review D of PR #660 addressed at a776a24c6. All 6 fixed (D1 a standing correction survives a rewrite of its witness's file or path; D2 OR-18 records base-branch reads as practice; D3 2.84 MB to history; D4/D5 the gate requires and tests its base, reads it only where a count is deferred, and tells a shallow clone to unshallow; D6 broadened guard). Reply: https://github.com/jlevy/squares/pull/660#pullrequestreview-5555898335. Merged main 6a3a7d8fe (#663); site v0.7.25 cut (PUBLICATION_REVISION 83b4720e). Labelled deep-gate. Hosted CI all green (run 38999827119), certificate page green (38999827111), deep gate 12/12 + deep-gate-required green (39000018232). mergeable_state clean. PATCH draft=false did not take (REST), so the PR is still a draft and needs marking ready.
