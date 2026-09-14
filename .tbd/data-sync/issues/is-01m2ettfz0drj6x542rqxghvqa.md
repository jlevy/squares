---
type: is
id: is-01m2ettfz0drj6x542rqxghvqa
title: Merge the n11 stack with a merge commit and close out main
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - pr
  - landing
dependencies:
  - type: blocks
    target: is-01m2ettwze138wbhg772ekt1d4
parent_id: is-01m2etr75jfh3t3ry7kj1ccqrb
created_at: 2026-09-14T02:09:32.127Z
updated_at: 2026-09-14T04:27:43.111Z
---
Merge the n11 stack and close out main.

Preconditions: owner decisions recorded (think-bt5b: land now; think-zwlf: calibration deferred); checkpoint think-wkav green at the frozen top; descriptions refreshed (think-gidf); main still f2e24e07 (else rerun the checkpoint).

Steps, following #148/#149 (GitHub native stack merge; repo allows merge commits; delete_branch_on_merge true; auto-merge off):
1. Merge the chain top with a merge commit; #156 and #161–#165 are marked merged and their branches deleted.
2. Confirm #157 and #167 retarget to main automatically (automatic_base_change_succeeded).
3. Watch the main push `Packing validation` run (about 55 min) and the Pages deploy.
4. Append a post-merge closeout section to the merged PR descriptions citing the merge commit and main runs.
5. Do not start BC329 calibration or target work: deferred by the owner (think-zwlf). Record that deferral in the post-merge closeout.

## Notes

2026-09-14 04:30 UTC: gh stack merge of stack 158 merged #156, #161–#166 into main at 2f8865b6 (merge commit); #157 merged at 620e4731; #169 closed and its branch deleted; #167 retargeted to main and back-merged (6b075319), still draft and paused. Remaining: main push Packing validation runs 34805967105 (2f8865b6) and 34806011392 (620e4731), Certificate page runs, then post-merge closeout notes.
