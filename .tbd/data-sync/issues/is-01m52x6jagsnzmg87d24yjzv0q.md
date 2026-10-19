---
type: is
id: is-01m52x6jagsnzmg87d24yjzv0q
title: "PR #644 E2: regularization.changes leaves out the regularizer's free-angle turns (129: 21 re-angled squares unrecorded)"
kind: bug
status: in_progress
priority: 3
version: 2
delegate: user-eb-addr-644
labels:
  - regularization
dependencies: []
parent_id: is-01m51k8s0y2dbwnmvtwjv30zrx
hold: null
hold_until: null
created_at: 2026-10-16T17:47:17.199Z
updated_at: 2026-10-16T17:47:22.889Z
started_at: 2026-10-16T17:47:22.889Z
---
Review E2 (Low) of jlevy/squares#644, deferred there by the addressing pass (user-eb-addr-644, 16 October 2026). Review: https://github.com/jlevy/squares/pull/644#pullrequestreview-5550695663

`regularize_evand.regularization_record` (packing/devtools/regularize_evand.py, the `changes` block, about lines 2547-2560) counts `straightened` and `re_angled` from `regularize.merged` only, and `merged_rotation_groups_deg` from `determined-merge` angle changes only. The conservative pass's `free-angle` turns of undetermined groups (vendor/evand-regularize/search/regularize/reg.py:733-734) are counted by neither. At 129 the retained report (packing/cases/regularized_drawings/think-la7h-2026-10-16/3a-rerun-1016/n-129) has `merged` empty and 21 `free-angle` entries (up to -43.998 to -39.271 degrees), so the index entry, results.yaml, RESULTS.md and the case note record no `changes` at all; only identity's largest turn (4.72707 degrees) shows it. At 176, 3 of 82 changed squares are uncounted the same way. The admission decision is unaffected (`unnamed_turns` reads `changed_angles`).

Fix: count `free-angle` entries, by their square count, in `re_angled` or under a key of their own (results.schema.yaml's `regularizations` item and the index schema's `changes` would need the key), then regenerate every drawn Evan Daniel entry's `regularization` and the records generated from it.

Why not in #644: the fix regenerates all 49 drawn Evan Daniel entries, and this repository retains reports only for the five of the 3a batch; the other 44 need their runs' reports, which are not retained, or a fresh driver run at those counts (`regularize_evand rungs --check` can confirm a re-run reproduces each drawn view first). Fixing only the five would leave the index counting two ways. Waits on: a decision whether to re-run the driver at the 44 counts or retain their reports, in its own PR.
