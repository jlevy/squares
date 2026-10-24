---
type: is
id: is-01m5nfdtfyjpee1131zzb9g0w9
title: "Address PR #754 review B (B1-B4)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: c-fix-754b-1023
labels: []
dependencies: []
parent_id: is-01m5ndg7em7x0s0p5wehyfd90e
hold: null
hold_until: null
created_at: 2026-10-23T22:52:09.086Z
updated_at: 2026-10-23T23:53:48.266Z
started_at: 2026-10-23T22:52:20.160Z
---

## Notes

2026-10-23 c-fix-754b-1023: review B of PR #754 addressed at head bf28ab6dd; dispositions https://github.com/jlevy/squares/pull/754#issuecomment-6377099959.
- B1 fixed (7af63e755, bf28ab6dd): intake_ledger.answer_problems. From GOEBEL_FROM a ledger with claims beyond 324 applies the restatement ruling and Göbel's baseline (its ruling or a frozen start member) at every such count, or names the answer it leaves out under rulings_not_applied with the reason. The negative control passed check before the fix. #732's walk is saved by its classical-constructions ruling. All 12 walks pass check and render --check.
- B2 fixed (7af63e755): the runbook names #732's walk as the case frozen before the rule, and tree_drift is tested under both dates.
- B3 fixed (7af63e755): the --tree help text, and a note on think-llit.
- B4 fixed: think-q920's note rewritten. think-v022 is left open for the coordinator.
- D6 wording (8775445cd): only the selected label is quoted as the owner's answer, in the runbook, DELETION_ANSWER and its comment, and the two walks' notes; think-f2io's notes and think-kzme's description and notes are corrected the same way.
- Merged main 64b316b6c (62fe27861), re-pinned (bb1cd1338), and re-measured the papers' no-change record (be6184ba2).
- CI at bf28ab6dd: 31 pass, 28 skipped. The first attempt failed one site layout test, a flake that passed 12 of 12 locally and on the re-run.
