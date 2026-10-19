---
type: is
id: is-01m50wdvvpwz9asfq2gvaxfz5w
title: "Intake process: add a regularization step to result-import.md stages (on adoption/registration of a new best), with a gate that fails on an unregularized current drawing"
kind: task
status: in_progress
priority: 1
version: 17
delegate: user-eb-reg-intake
labels:
  - regularization
dependencies: []
parent_id: is-01m50wdrbfnwsq05w150az5z88
child_order_hints:
  - is-01m51kef47pgjm20f7988m9rzv
  - is-01m51wb7qswjsy83afdvrxyk3j
  - is-01m52ct0hx1ynh99j59jej4tze
hold: null
hold_until: null
created_at: 2026-10-15T22:55:18.902Z
updated_at: 2026-10-19T20:27:57.258Z
started_at: 2026-10-16T04:17:15.710Z
---

## Notes

2026-10-16T04:55Z (ecstatic-edison-reg-intake): branch claude/ecstatic-edison-8en33t-regularization-intake pushed to origin, head 09ba0c143, from origin/main e2e018f32. No PR yet.

Done (3 commits):
- c50444bfe feat(adopt_houses): regularization_owed(), printed after a write and --dry-run: re-housed counts, which are certain to read pending (strong view lapses / earlier lapse), PENDING_ALLOWED and SETTLED entries the new witness bears on, cost 5-15 CPU-min a count, and the "When a Witness Changes" commands (build_known_best_atlas --update, axis --update-atlas --n, default_drawings --update, grid-slack 0.5/1/5, evand run, regularize_select), ending with the --check-state gate. Docstring post-step now the guide's steps. Tests in test_house_adoption.py (2 new) and test_default_drawings.py (adoption replay extended: allowlisted with a bead passes, entry naming no bead fails).
- 8deda0776 docs: result-import.md stage 5 "Adopt a House, Then Regularize It" (cost from run receipts, compute cap, defer to PENDING_ALLOWED with bead in the same PR, gate); Running an Intake Pass step 3, The Prompt step 4, stage table. Guide "When a Witness Changes" and policy sections 5 and 8 cross-linked.
- 09ba0c143 chore(release): ReleaseNoPublicChange for packing/devtools/adopt_houses.py (4 papers + site).

Validated locally: packing-validate --edit pass (68/110, 569 s), --records pass (52/110, 107 s), focused pytest 67 passed, ruff/basedpyright zero on changed files, check_release_impact --baseline-ref origin/main ok, release_pin --check ok (288a1a52022f). packing-validate --push was running at push time.

Left: confirm --push result; open DRAFT PR (labels project + S1; body drafted at scratchpad g3q7_pr_body.md, passes check_pr_description); watch CI to green (#538 animate-view flake may be re-run once); never merge. Close think-g3q7 only after the PR merges.

2026-10-16T05:12Z: draft PR https://github.com/jlevy/squares/pull/641 opened at 09ba0c143, labels project + S1; CI running. Local packing-validate --push: 66/67 steps passed, reachable behavioral tests timed out at the 900 s cap (286 files, host load 9-10 on 4 cores with another push tier running); re-running that selection uncapped. Left: CI to green, reachable rerun result as a PR comment, never merge.

2026-10-16 ~05:40Z coordinator user-eb (epic think-hg5s): a senior review of PR #641 (strong tier, reviewer role, publishes a COMMENT review, does not push) is running. If this lane is done with the branch, say so in a note here; user-eb will then run the addressing pass on it. Until then nobody but this lane pushes to claude/ecstatic-edison-8en33t-regularization-intake.

2026-10-16 ~05:55Z coordinator user-eb: Review B (independent senior, strong tier) is on #641 at 09ba0c143, https://github.com/jlevy/squares/pull/641#pullrequestreview-5543563103: 0 blocker/0 high/2 medium/2 low (B1: the 14 PENDING_ALLOWED counts that lost a strong view before #636 (105, 129, 146, 153, 156, 175, 176, 211, 237, 241, 271, 272, 302, 304) carry no lapsed block, so a regular new house would read regular-as-published and drop the owed runs; B2: fixed run-directory names reuse run ids across adoptions; B3 placeholders; B4 #553 credit). It was started before Review A appeared; it adds only what A missed. user-eb leaves the addressing pass of #641 to this lane/coordinator and will not push here.

2026-10-16 ~05:58Z OWNERSHIP TRANSFER by the owner's word to the overnight coordinator user-eb (epic think-hg5s): "We have some changes with the regularization and a couple other things from another agent that you should take over and incorporate into your work." The ecstatic-edison lanes should stop work on this bead and its branch, and record any unpushed state in a note here. user-eb's lanes fetch before every push and stop if the branch moved.

2026-10-16T06:02Z user-eb-reg-intake (lane G): picked up the addressing pass of #641 Reviews A and B. Checked: branch head still 09ba0c143 (pushed 04:33Z, quiet >80 min), no disposition replies or new commits on the PR. Worktree .claude/worktrees/reg-intake. Next: fixes for B1 (count_state: an allowlisted count stays pending whatever its new house reads), B2/B3/B4, A-series docs; then the stacked sweep PR.

2026-10-16T06:31Z user-eb-reg-intake: #641 addressing commits pushed (head 46562eab0, from 09ba0c143 after a fetch confirmed it unmoved): 955c8214e adopt_houses printout (B2 unique run dirs adopt-<day>-*, B3 RUNS/WORKERS, B5 parser test, B6, A3, A7 5-25 CPU-min, A8, A11, A1/A2 deferral lines); c720d982b default_drawings (B1: count_state keeps a PENDING_ALLOWED count pending whatever its house reads -- no data change, --check byte-identical; A1 --compare EARLIER; A9 release record); 46562eab0 docs (A1 A2 A4 A5 A6 A7 B1 B2 B4). Local: focused pytest 73 passed, packing-validate --records 52/52 steps, ruff/basedpyright 0, check_release_impact ok, release_pin --check ok. Chose not to backfill lapsed blocks (272/304 never in the index; all 14 being decided by #644 and lane B). Next: CI to green, disposition replies, then the stacked sweep PR.

2026-10-16T06:53Z user-eb-reg-intake: #641 CI green at 46562eab0 (31 success, 28 skipped, 0 failed; Packing validation run 38861680046). Disposition replies posted: A https://github.com/jlevy/squares/pull/641#issuecomment-6209773869, B https://github.com/jlevy/squares/pull/641#issuecomment-6209774103 (all fixed except A12 declined; no deferrals). PR description updated (A10). Deferred checkpoint dispatch was refused (403), so labelled deep-gate: run 38862757844 in progress. Stacked PR #650. Closes at #641's merge (think-1644).

2026-10-16T07:24Z user-eb-reg-intake DONE for this lane: #641 head 46562eab0, CI green (run 38861680046), Deferred checkpoint passed 12/12 jobs (run 38862757844, via deep-gate label), dispositions posted for A and B (A12 declined, all else fixed; no deferral beads). Close think-g3q7 only after #641 merges (merge bead think-1644). Owner/coordinator decisions: A12 sequencing vs #574/T-174; whether persisted lapsed blocks are still wanted for the 12 derivable historical lapses (not done: 272/304 not derivable, all 14 being decided by #644 and the kpm3/3zi3 batch).

2026-10-16T08:21Z user-eb-addr-641-650: addressing Review C on #641. Pushed a59a6024a (C1 test: a decision outranks the allowlist; mutations M2-M5 now fail) and e9d5c01d8 (C3 run label names the counts; C4 one deferral wording and the --compare <(git show ...) command; C2 docs). C2's gate hardening deferred to think-k6rj (child of think-g3q7). Next: records tier, CI and deferred checkpoint, PR body, disposition reply; then #650.

2026-10-16T10:25Z user-eb-addr-641-650: #641 Review C addressed at 7aa4775ea (fixes a59a6024a, e9d5c01d8; empty CI re-run 7aa4775ea after a frontend Chromium timeout at e9d5c01d8). CI green incl. Deferred checkpoint (runs 38883824978, 38883825029). Reply: https://github.com/jlevy/squares/pull/641#pullrequestreview-5546364606. C2 gate hardening deferred to think-k6rj.
