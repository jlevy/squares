---
type: is
id: is-01m7kqn1kjvjkmqbcs4yfq84fc
title: "Lift the regularize-first hold (owner, 17 Nov, think-fibh): bring #953, #908 and #909 up to date with main, get CI green, senior review, merge in that order"
kind: task
status: in_progress
priority: 1
version: 9
delegate: w1-holds-1117r
labels: []
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
child_order_hints:
  - is-01m7nqbah2c7q74fzd4z4smt5w
  - is-01m7nxzge4950perv8zk1290n7
  - is-01m7nyxbsr24nq3xkfk7djkx9d
hold: null
hold_until: null
created_at: 2026-11-17T03:08:49.138Z
updated_at: 2026-11-18T00:37:54.699Z
started_at: 2026-11-17T03:08:51.346Z
---

## Notes

2026-11-17T21:55Z coord-intake-1117r: reclaimed from silent c-holds-1117 / bold-ritchie lanes; delegated to w1-holds-1117r (worktree /home/user/wt/w1): address #953 review A, merge #953 -> #908 -> #909 per think-fibh.

2026-11-17 w1-holds-1117r: #953 MERGED 22:40:55Z, merge commit e01cffa62d37bc768aaaac8fab775f2f1d242f69, at head 50ab340e1 after review A's addressing (fix 505b8ff0a, re-pin 50ab340e1; disposition reply https://github.com/jlevy/squares/pull/953#issuecomment-6963098308; CI at 50ab340e1: Packing validation 44182523765, Certificate page 44182523644, Branch mergeability 44182509128, all success). Pages deploy of e01cffa62: run 44192413608 success; check_published_site --commit e01cffa62...: 6387 of 6387 checks passed; results.html rows t-142/t-143 read V0/C1 reviewed, result/t-142.html and t-143.html carry the new wording. POSTED (for the records lane to record under replies, kind follow-up, date 2026-11-17, stating T-142 V0/C1 reviewed + E-wand125-fine-net-n28-57425-report reviewed; T-143 V0/C1 reviewed + E-wand125-fine-net-n30-58925-report reviewed; both corrections of the 2026-10-24 acknowledgement; no beads named): #776 https://github.com/jlevy/squares/issues/776#issuecomment-6963938807 and #777 https://github.com/jlevy/squares/issues/777#issuecomment-6963939109, each check_requests --draft N from main e01cffa62 as rendered. #908 at 2145ed64f green (44193864499, 44193864251, 44193850201), under senior review by the coordinator's reviewer. #909 at 03dce2355: one job failed on the bead-tree step from my think-f0pn close (fixed 23:05Z); rerun pending.

2026-11-18 w1-holds-1117r: #908 MERGED 2026-11-18T00:12:39Z, merge commit 2be743b07b235023d55a9cd7161fa17435c32069, at head 540e4a8be (review A https://github.com/jlevy/squares/pull/908#issuecomment-6964205921 addressed; disposition reply https://github.com/jlevy/squares/pull/908#issuecomment-6964876465; CI at head: Packing validation 44202620812, Certificate page 44202620802, Branch mergeability 44202615105, success). Pages run 44205944299 for 2be743b07: attempt 1 failed in font-loading (webkit) only (check_math_loading: 'native MathML was visible before enhancement: s(11)'), rerun of failed jobs, attempt 2 success; check_published_site --commit 2be743b07...: 6389 of 6389 passed; results.html rows t-142/t-143 V3/C3 confirmed current, t-107/t-109 not current; cases/28 and 30 carry 2297/400 and 2357/400. POSTED for the records lane (date 2026-11-18): #776 final https://github.com/jlevy/squares/issues/776#issuecomment-6965313743 (closed; states T-142 V3/C3 confirmed current, E-wand125-fine-net-n28-57425-report reviewed, E-wand125-fine-net-n28-57425-sqverify-fast-replay confirmed; corrects the 2026-10-24 acknowledgement; no beads named); #777 final https://github.com/jlevy/squares/issues/777#issuecomment-6965314300 (closed; T-143 V3/C3, E-wand125-fine-net-n30-58925-report reviewed, E-wand125-fine-net-n30-58925-sqverify-fast-replay confirmed); #532 follow-up https://github.com/jlevy/squares/issues/532#issuecomment-6965326217 (T-142/T-143 ask done at V3/C3, adopted; T-132 follows #909, think-r333; T-144 waits on compute, think-nd7g); #446 follow-up https://github.com/jlevy/squares/issues/446#issuecomment-6965326853 (n28 287/50 passed by T-142 at V3/C3 current, adopted; T-107 superseded). Note: #776 and #777 still carry the GitHub label blocked:compute, which my brief does not let me edit; the record dropped the block in #908.
