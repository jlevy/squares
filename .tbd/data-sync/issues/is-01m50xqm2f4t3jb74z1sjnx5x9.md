---
type: is
id: is-01m50xqm2f4t3jb74z1sjnx5x9
title: "Regularize 3a: 176 first, then 105, 129, 146, 156, 204, 271, 272, 303 (re-housed by #614 60aa1d39e)"
kind: task
status: in_progress
priority: 1
version: 7
delegate: user-eb-reg-3b3c
labels:
  - regularization
dependencies: []
parent_id: is-01m50wdrbfnwsq05w150az5z88
hold: null
hold_until: null
created_at: 2026-10-15T23:18:07.183Z
updated_at: 2026-10-16T06:01:50.193Z
started_at: 2026-10-16T02:53:15.554Z
---

## Notes

Worker ecstatic-edison-reg-run-3a (claimed 2026-10-16T02:52Z). Branch claude/ecstatic-edison-8en33t-regularize-3a, now on main e2e018f32 (#636 merged, v0.7.14) by fast-forward (no commits of its own before that).

## 2026-10-16T05:10Z: generators and selection done; admission next

Run directories (outside the checkout, on this host):
/tmp/claude-0/-home-user-squares/b1f8ff4e-5e49-561e-aa0f-a76f1a5fe076/scratchpad/reg3a/
- runs/3a-deg05-1016, runs/3a-deg1-1016, runs/3a-deg5-1016: grid-slack at 0.5, 1, 5 degrees (run ids grid-slack-3a-deg05-1016 etc.), one invocation per count, nice 10, two lanes, 02:55:35Z-03:20:40Z; timing.tsv has wall/user/sys per count and threshold.
- runs/3a-1016: Evan Daniel driver (run id evand-regularize-3a-1016), --workers 2 --timeout 1800 --regularize-timeout 1800, 03:20:50Z-04:06:00Z, 2,710 s wall, 3,559.68 CPU-s (receipt.json).
- selection-2.json / selection-2.md / logs/select-2.out: regularize_select on main e2e018f32 (drawn-picture guard), --workers 2, 2,254 s wall on a host at load 10-11. An earlier selection on the pre-C1 branch was stopped after about 20 min wall (wasted).

Per count (grid CPU-s over three thresholds + evand CPU-s; outcome; drawn L/U/N/C/H/house/stage before -> after):
- 176: 46 + 66 = 112 CPU-s; evand same-side view chosen; house 70/71/52/83/19/33/393 -> 11/24/0/6/6/457/475
- 105: 219 + 158 = 377; grid-slack 0.5 deg chosen (evand row 7 refuse); axis 7/14/5/16/16/199/240 -> 6/7/0/11/11/226/248
- 129: 72 + 47 = 119; evand chosen; axis 0/0/0/23/19/362/366 -> 0/0/0/13/13/370/376
- 146: 275 + 250 = 525; evand chosen; axis 3/5/1/12/12/367/388 -> 1/0/0/6/6/402/410
- 156: 309 + 239 = 549; evand chosen; axis 2/8/4/19/19/328/376 -> 2/4/0/14/14/360/376
- 271: 106 + 560 = 667; evand chosen; axis 6/12/1/24/19/728/752 -> 6/10/0/21/19/738/760
- 204: 200 + 277 = 477; no better: grid ties the axis view on every goal at all three thresholds; evand row 7 refuse (22/105/0/5/5/431/515)
- 272: 1,111 + 260 = 1,371; no better: grid row 7 refuse, worse on stage_total (702/730 vs 700/732); evand row 4 held (solved side 1.7e-19 above U)
- 303: 289 + 1,702 = 1,991; no better: grid ties at all three thresholds; evand row 4 held (solved, 2.6e-31 above U), worse on L/U/house/stage

Next commands, from packing/ after `uv run --frozen --all-extras --group dev`:
  python -m devtools.regularize_evand layer --run-dir $R/runs/3a-1016 --repo-root ..
  python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. --grid-run $R/runs/3a-deg05-1016 --grid-counts 105
then render_regularized_atlas --update, default_drawings --update, regularized_drawings, render_results --update; settle 204/272/303 in default_drawings.SETTLED (runs: evand-regularize-3a-1016 and the three grid-slack-3a-* runs) and take the nine off PENDING_ALLOWED; atlas README paragraph; data commit, release_pin --update, re-pin commit; checks; draft PR; site cut after v0.7.14 last.

2026-10-16 ~05:40Z, coordinator user-eb (epic think-hg5s): the owner asked tonight that every remaining regularization be done, 176 first. This lane's 05:05Z note shows generators and selection done and admission next, so it keeps the bead. user-eb will take it over (and re-run on its own host) only if no branch claude/ecstatic-edison-8en33t-regularize-3a is pushed and no note is added here by about 07:30Z. Lanes of user-eb regularize think-kpm3/think-3zi3 (branch claude/intake-2026-10-16-regularize-3b, from main) and think-0ut1 (stacked on it); expect generated-file conflicts with this branch at merge.

2026-10-16 ~05:58Z OWNERSHIP TRANSFER by the owner's word to the overnight coordinator user-eb (epic think-hg5s): "We have some changes with the regularization and a couple other things from another agent that you should take over and incorporate into your work." The ecstatic-edison lanes should stop work on this bead and its branch, and record any unpushed state in a note here. user-eb's lanes fetch before every push and stop if the branch moved.

2026-10-16T06:08Z user-eb-reg-3b3c: took over by the owner's word (coordinator, ~05:55Z). PR #644 is the ecstatic-edison lane's (head 42ef42e5a); no second PR. Verifying read-only in detached worktree .claude/worktrees/reg-3a at 42ef42e5a: default_drawings --check-state passes (PENDING_ALLOWED 11; 64 regularized, 232 regular-as-published, 13 decided, 4 exempt, 11 pending), release_pin --check passes (pin 72666de89931). SETTLED 204/272/303 bind the witnesses' source/path/revision/side with the four 3a runs; README paragraph of 16 October present; index runs carry evand-regularize-3a-1016 and grid-slack-3a-deg05-1016. Running packing-validate --records and the focused tests next. think-kpm3/think-3zi3 will stack on this branch.
