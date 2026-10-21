---
type: is
id: is-01m5fremhm4c78ag7ht2ethyte
title: "PR #704 B4: the snapshot note in run_negative_controls.py records a stale figure"
kind: bug
status: closed
priority: 3
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m5fre23qy5rq285h9tsarhz0
created_at: 2026-10-21T17:34:26.355Z
updated_at: 2026-10-21T18:08:02.984Z
closed_at: 2026-10-21T18:08:02.984Z
close_reason: "fixed: figures recorded in 34cd6da71; after the merge of 51ac9d7ee the exclusion no longer held the cap, so fd7f939e5 withdraws the note and entry (branch no longer changes run_negative_controls.py; #714 answers the cap); figures in the PR description"
resolution: null
duplicate_of: null
---
Low. packing/devtools/run_negative_controls.py:236-242 at d2eca7108: the note records 232,767,018 bytes; --source-bytes read 232,768,595 at the head. Review B: https://github.com/jlevy/squares/pull/704#issuecomment-6306759614
